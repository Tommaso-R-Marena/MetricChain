"""Exact pairwise discrete models.

A :class:`PairModel` is the *published instance* of every certificate of this package: `n` sites,
site `i` with states `0 .. k_i - 1`, and tables of exact dyadic rationals

    E(x) = sum_i unary[i][x_i] + sum_{(i, j) listed, i < j} pair[(i, j)][x_i, x_j].

All tables are stored as integers in units of ``2**-scale_bits`` (of whatever energy unit the
producer of the tables used; kcal/mol for the molecular layer).  A table entry is therefore an
exact rational number, and every statement certified about a `PairModel` is a statement about
these rationals — never about the floating-point or physical energy function they were rounded
from (label **[M]**, `docs/structural_biology/VERIFICATION_REPORT.md`).

Correspondence with the theory division's objects (`docs/BLUEPRINT.md` §2): a `PairModel` is a
`PairInstance` whose unordered pair tables are stored in one orientation (`J[i][j]` for `i < j`,
`J[j][i] = 0`), with ragged state sets realised as domains inside a common alphabet of size
`max_i k_i`.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Sequence

import numpy as np

__all__ = ["PairModel", "brute_force_min", "brute_force_energies"]


def _as_int_array(table, shape_len: int) -> np.ndarray:
    arr = np.asarray(table)
    if arr.dtype == object:
        arr = np.array(arr.tolist(), dtype=object)
    if arr.ndim != shape_len:
        raise ValueError(f"table must have {shape_len} dimension(s), got shape {arr.shape}")
    if arr.dtype.kind not in "iuO":
        raise TypeError("PairModel tables must be integers (units of 2**-scale_bits); use from_float to round")
    flat = [int(v) for v in arr.reshape(-1).tolist()]
    if any(abs(v) >= 2 ** 62 for v in flat):
        # keep exact Python integers; numpy int64 could not hold them
        out = np.empty(arr.shape, dtype=object)
        out.reshape(-1)[:] = flat
        return out
    return np.array(flat, dtype=np.int64).reshape(arr.shape)


@dataclass
class PairModel:
    """Pairwise model with exact dyadic tables (integers in units of ``2**-scale_bits``)."""

    unary: list
    pair: dict
    scale_bits: int = 0
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.scale_bits, int) or self.scale_bits < 0:
            raise ValueError("scale_bits must be a natural number")
        self.unary = [_as_int_array(u, 1) for u in self.unary]
        if any(u.shape[0] == 0 for u in self.unary):
            raise ValueError("every site needs at least one state")
        pair = {}
        for key, table in self.pair.items():
            i, j = (int(key[0]), int(key[1]))
            if not (0 <= i < j < len(self.unary)):
                raise ValueError(f"pair key {key!r}: need 0 <= i < j < n")
            if (i, j) in pair:
                raise ValueError(f"pair {key!r} listed twice")
            arr = _as_int_array(table, 2)
            if arr.shape != (self.unary[i].shape[0], self.unary[j].shape[0]):
                raise ValueError(f"pair table {(i, j)} has shape {arr.shape}, expected "
                                 f"{(self.unary[i].shape[0], self.unary[j].shape[0])}")
            pair[(i, j)] = arr
        self.pair = dict(sorted(pair.items()))
        self._neighbors = [[] for _ in self.unary]
        for (i, j) in self.pair:
            self._neighbors[i].append(j)
            self._neighbors[j].append(i)

    # ------------------------------------------------------------------ basic structure
    @property
    def n(self) -> int:
        return len(self.unary)

    @property
    def sizes(self) -> list:
        return [int(u.shape[0]) for u in self.unary]

    def neighbors(self, i: int) -> list:
        return list(self._neighbors[i])

    def full_domains(self) -> list:
        return [list(range(k)) for k in self.sizes]

    def pair_table(self, i: int, j: int) -> np.ndarray:
        """Table of the unordered pair `{i, j}` indexed `[state of i, state of j]` (whatever the order of `i, j`)."""
        return self.pair[(i, j)] if i < j else self.pair[(j, i)].T

    # ------------------------------------------------------------------ energies
    def energy_int(self, x: Sequence[int]) -> int:
        """Exact energy of the configuration `x`, in units of ``2**-scale_bits`` (Python integer)."""
        if len(x) != self.n:
            raise ValueError("configuration must assign a state to every site")
        e = 0
        for i, a in enumerate(x):
            e += int(self.unary[i][a])
        for (i, j), table in self.pair.items():
            e += int(table[x[i], x[j]])
        return e

    def energy(self, x: Sequence[int]) -> Fraction:
        return Fraction(self.energy_int(x), 2 ** self.scale_bits)

    def max_abs_entry(self) -> int:
        m = 0
        for u in self.unary:
            m = max(m, max(abs(int(v)) for v in u.tolist()))
        for t in self.pair.values():
            m = max(m, max(abs(int(v)) for v in t.reshape(-1).tolist()))
        return m

    # ------------------------------------------------------------------ construction
    @classmethod
    def from_float(cls, unary: Iterable, pair: dict, scale_bits: int = 20, meta: dict | None = None) -> "PairModel":
        """Round floating-point tables to the nearest multiple of ``2**-scale_bits``.

        The result *is* the model from then on.  The rounding error per entry is at most
        ``2**-(scale_bits + 1)`` relative to the floating-point table; nothing in this package
        certifies anything about the unrounded numbers.
        """
        scale = 2 ** scale_bits

        def rnd(table):
            arr = np.asarray(table, dtype=np.float64)
            if not np.all(np.isfinite(arr)):
                raise ValueError("tables must be finite (clip clash energies before rounding)")
            out = np.empty(arr.shape, dtype=object)
            out.reshape(-1)[:] = [int(round(Fraction(float(v)) * scale)) for v in arr.reshape(-1).tolist()]
            return out

        info = dict(meta or {})
        info.setdefault("rounding", f"nearest multiple of 2**-{scale_bits} of the float64 table entries")
        return cls(unary=[rnd(u) for u in unary], pair={k: rnd(t) for k, t in pair.items()},
                   scale_bits=scale_bits, meta=info)

    def to_float(self):
        """Float64 copies of the tables in energy units (for untrusted numerical work only)."""
        s = float(2 ** self.scale_bits)
        unary = [np.array([int(v) for v in u.tolist()], dtype=np.float64) / s for u in self.unary]
        pair = {k: np.array([[int(v) for v in row] for row in t.tolist()], dtype=np.float64) / s
                for k, t in self.pair.items()}
        return unary, pair


def brute_force_energies(model: PairModel, domains: Sequence[Sequence[int]] | None = None):
    """Yield `(x, energy_int)` for every configuration of the box (exhaustive; small instances only)."""
    domains = model.full_domains() if domains is None else [list(d) for d in domains]
    for x in itertools.product(*domains):
        yield x, model.energy_int(x)


def brute_force_min(model: PairModel, domains: Sequence[Sequence[int]] | None = None):
    """Exact minimum over the box by enumeration: `(energy_int, lexicographically first minimiser)`."""
    best = None
    for x, e in brute_force_energies(model, domains):
        if best is None or e < best[0]:
            best = (e, tuple(x))
    if best is None:
        raise ValueError("empty box")
    return best
