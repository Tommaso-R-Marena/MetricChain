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

Integers only, and nothing cached (review STRUCTBIO-REV-0001, findings 4, 16, 17).  The
constructor refuses every entry that is not an integer (`from_float` is the only way from
floats: nothing is truncated silently) and every pair key that is not a tuple of two sites
`i < j`.  A `PairModel` stays a mutable object — arrays can be written and tables replaced after
construction — so nothing derived from the tables is stored on it (`neighbors` is recomputed at
every call), and the checkers and the checksum read an instance only through `integer_tables`,
which re-establishes what the constructor established, at the time of the check.
"""
from __future__ import annotations

import itertools
import operator
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Iterable, Sequence

import numpy as np

__all__ = ["PairModel", "exact_int", "integer_tables", "MAX_SCALE_BITS", "brute_force_min", "brute_force_energies"]

#: Largest `scale_bits` the checkers evaluate (`mincheck`, `zcheck`).  They refuse a finer unit
#: before computing any power of two; `PairModel` itself only requires a natural number.
MAX_SCALE_BITS = 1024

_INT64_LIMIT = 2 ** 62          # tables with an entry of this magnitude are kept as Python integers


def exact_int(v, what: str = "value") -> int:
    """The Python `int` equal to `v`, for an `int` or a NumPy integer.

    Everything else is refused with `TypeError` — `bool`, `float`, `str`, `Fraction`, ... — so
    that no value is truncated or read in two ways, and so that whatever is computed with the
    result is exact (NumPy integers have a fixed width and wrap around silently)."""
    if type(v) is int:
        return v
    if isinstance(v, bool) or not isinstance(v, (int, np.integer)):
        raise TypeError(f"{what} must be an integer, got {type(v).__name__}")
    return int(operator.index(v))


def _exact_entries(table, ndim: int, what: str):
    """`(shape, entries)` of an integer table with `ndim` axes: the entries as a flat list of
    Python integers in C order.  A table that holds anything but integers is refused."""
    if isinstance(table, np.ndarray) and table.dtype != object:
        arr = np.asarray(table)                           # (a plain array, whatever subclass was given)
    else:
        # Lists, and object arrays (which may hold their rows as objects), are read element by
        # element: left to itself NumPy turns a list such as [2**64 - 2, 5] into floats.
        arr = np.array(table.tolist() if isinstance(table, np.ndarray) else table, dtype=object)
    if arr.ndim != ndim:
        raise ValueError(f"{what} must have {ndim} dimension(s), got shape {arr.shape}")
    if arr.dtype.kind in "iu" or arr.size == 0:           # (an empty table has no entry to refuse)
        return arr.shape, arr.reshape(-1).tolist()
    if arr.dtype != object:
        raise TypeError(f"{what}: PairModel tables must be integers (units of 2**-scale_bits); use from_float to round")
    return arr.shape, [exact_int(v, f"an entry of {what}") for v in arr.reshape(-1).tolist()]


def _as_int_array(table, ndim: int, what: str = "a table") -> np.ndarray:
    """A new array holding the integer table exactly: int64, or Python integers (dtype object)
    when an entry is 2**62 or more in absolute value."""
    shape, flat = _exact_entries(table, ndim, what)
    if flat and (max(flat) >= _INT64_LIMIT or min(flat) <= -_INT64_LIMIT):
        out = np.empty(shape, dtype=object)
        out.reshape(-1)[:] = flat
        return out
    return np.array(flat, dtype=np.int64).reshape(shape)


def _pair_key(key, n: int):
    """The pair `(i, j)` named by a key of `PairModel.pair`: a tuple of two sites with `i < j`."""
    if not (isinstance(key, tuple) and len(key) == 2):
        raise ValueError(f"pair key {key!r}: need a tuple (i, j) of two sites")
    try:
        i, j = exact_int(key[0], "a site"), exact_int(key[1], "a site")
    except TypeError:
        raise ValueError(f"pair key {key!r}: the sites must be integers") from None
    if not 0 <= i < j < n:
        raise ValueError(f"pair key {key!r}: need 0 <= i < j < n")
    return i, j


@dataclass
class PairModel:
    """Pairwise model with exact dyadic tables (integers in units of ``2**-scale_bits``)."""

    unary: list
    pair: dict
    scale_bits: int = 0
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        try:
            self.scale_bits = exact_int(self.scale_bits, "scale_bits")
        except TypeError:
            raise ValueError("scale_bits must be a natural number") from None
        if self.scale_bits < 0:
            raise ValueError("scale_bits must be a natural number")
        if not isinstance(self.pair, dict):
            raise TypeError("pair must be a dict {(i, j): table}")
        self.unary = [_as_int_array(u, 1, f"the one-body table of site {i}") for i, u in enumerate(self.unary)]
        if any(u.shape[0] == 0 for u in self.unary):
            raise ValueError("every site needs at least one state")
        pair = {}
        for key, table in self.pair.items():
            i, j = _pair_key(key, len(self.unary))
            if (i, j) in pair:
                raise ValueError(f"pair {key!r} listed twice")
            arr = _as_int_array(table, 2, f"pair table {(i, j)}")
            if arr.shape != (self.unary[i].shape[0], self.unary[j].shape[0]):
                raise ValueError(f"pair table {(i, j)} has shape {arr.shape}, expected "
                                 f"{(self.unary[i].shape[0], self.unary[j].shape[0])}")
            pair[(i, j)] = arr
        self.pair = dict(sorted(pair.items()))

    # ------------------------------------------------------------------ basic structure
    @property
    def n(self) -> int:
        return len(self.unary)

    @property
    def sizes(self) -> list:
        return [int(u.shape[0]) for u in self.unary]

    def neighbors(self, i: int) -> list:
        """Sites that share a pair table with site `i`, in increasing order.  Recomputed from `pair`
        at every call: a table added after construction is seen (nothing is cached)."""
        return sorted(b if a == i else a for (a, b) in self.pair if i in (a, b))

    def full_domains(self) -> list:
        return [list(range(k)) for k in self.sizes]

    def pair_table(self, i: int, j: int) -> np.ndarray:
        """Table of the unordered pair `{i, j}` indexed `[state of i, state of j]` (whatever the order of `i, j`)."""
        return self.pair[(i, j)] if i < j else self.pair[(j, i)].T

    # ------------------------------------------------------------------ energies
    def configuration(self, x) -> tuple:
        """`x` as a tuple of Python integers, one existing state per site.  `ValueError` for
        anything else: a wrong length, a state that is not an integer, a state out of range — in
        particular a negative index, which NumPy would read as "the last state"."""
        if not isinstance(x, (tuple, list, np.ndarray)):
            raise ValueError("a configuration is a sequence with one state per site")
        try:
            states = tuple(exact_int(a, "a state") for a in x)
        except TypeError as exc:
            raise ValueError(f"configuration: {exc}") from None
        if len(states) != self.n or any(not 0 <= a < k for a, k in zip(states, self.sizes)):
            raise ValueError("configuration must assign an existing state to every site")
        return states

    def energy_int(self, x: Sequence[int]) -> int:
        """Exact energy of the configuration `x`, in units of ``2**-scale_bits`` (Python integer).
        `ValueError` unless `x` assigns an existing state to every site (see `configuration`)."""
        x = self.configuration(x)
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


def integer_tables(model: PairModel) -> tuple:
    """`(scale_bits, unary, pair)`: the instance as it is *now*, in Python integers.

    `unary[i]` is the list of the one-body entries of site `i`; `pair[(i, j)]`, for `i < j` and
    with the keys in increasing order, is the list of the rows of a pair table.  The function
    re-establishes what the constructor established — `scale_bits` a natural number, integer
    entries only, pair keys `(i, j)` with `0 <= i < j < n`, tables of the shape of their state
    sets — and raises `ValueError` or `TypeError` otherwise.  Both checkers and the instance
    checksum (`mincert.model_sha256`) read an instance through this function, once per check,
    and use nothing else of the object: no cached neighbour list, no array of fixed width."""
    if not isinstance(model, PairModel):
        raise TypeError("the instance must be a PairModel")
    if not isinstance(model.unary, (list, tuple)) or not isinstance(model.pair, dict):
        raise TypeError("the instance must hold a list of one-body tables and a dict of pair tables")
    scale_bits = exact_int(model.scale_bits, "scale_bits")
    if scale_bits < 0:
        raise ValueError("scale_bits must be a natural number")
    unary = [_exact_entries(u, 1, f"the one-body table of site {i}")[1] for i, u in enumerate(model.unary)]
    if any(not u for u in unary):
        raise ValueError("every site needs at least one state")
    pair = {}
    for key, table in model.pair.items():
        i, j = _pair_key(key, len(unary))
        shape, flat = _exact_entries(table, 2, f"pair table {(i, j)}")
        if shape != (len(unary[i]), len(unary[j])):
            raise ValueError(f"pair table {(i, j)} has shape {shape}, expected {(len(unary[i]), len(unary[j]))}")
        if (i, j) in pair:
            raise ValueError(f"pair {(i, j)} listed twice")
        pair[(i, j)] = [flat[r * shape[1]:(r + 1) * shape[1]] for r in range(shape[0])]
    return scale_bits, unary, dict(sorted(pair.items()))


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
