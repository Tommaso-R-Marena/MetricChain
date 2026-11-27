"""The dependence of the vertex set on the slope ratio: symbolic vertices, intervals of validity, chambers.

Weights ``(u, ..., u, u*)`` with ``r = u*/u`` (``u* > u`` in the application, so ``r > 1``).  In units of ``u`` the
polytope is ``P(r) = P(1, ..., 1, r)``; its inequalities have the right-hand sides 1 (the ``L - 1`` "horizontal"
directions) and ``r`` (the "vertical" direction ``L - 1``, the last site of the block).  ``r`` is an
irrational number in general, but:

* A vertex is determined by a spanning tree of tight edges (fact (V) in ``polytope``), so it is of the form
  ``phi = A + r B`` with INTEGER arrays ``A, B`` (``A(0) = B(0) = 0``): along a tight horizontal edge
  ``(dA, dB) = (+-1, 0)``, along a tight vertical edge ``(0, +-1)``.  Call ``(A, B)`` a symbolic vertex; its
  identically tight edges are those with these differences.
* For a symbolic vertex whose identically tight graph is connected, the set of ``r`` at which it is feasible is
  a closed interval with rational end points (every other edge gives a linear inequality in ``r``), its
  interval of validity.
* Chamber lemma.  Let ``V`` be the set of symbolic vertices found at a ratio ``r0`` at which, for every vertex,
  every tight edge is identically tight.  Then the vertex set of ``P(r)`` is exactly ``{A + r B : (A, B) in V}``
  for every ``r`` in the open interval ``J = (max lower end, min upper end)`` of the intervals of validity, and
  it is a different set immediately beyond either end.  ``J`` is the chamber of ``r0``; its end points are the
  walls.
  Proof.  (a) Two different symbolic vertices that coincide at ``r1`` cannot both be feasible on both sides of
  ``r1``: if ``(A, B)`` is feasible around ``r1`` and ``e`` is an identically tight edge of ``(A', B')``, the slack
  of ``e`` for ``(A, B)`` is affine near ``r1``, non-negative and zero at ``r1``, hence identically zero; so all
  edges of the spanning tight graph of ``(A', B')`` have the same differences in ``(A, B)``, i.e. the two are
  equal.  (b) Every vertex of ``P(r1)`` is a limit of vertices of ``P(r)``, ``r -> r1`` (the normals are fixed and
  ``P(r)`` depends continuously on ``r``: a linear functional maximised only at that vertex has maximisers on
  ``P(r)`` that converge to it).  (c) Every member of ``V`` is a vertex on ``J`` by the vertex criterion.  If
  another symbolic vertex were feasible somewhere in ``J``, take the one whose interval of validity comes
  closest to ``r0``, ending at ``r1`` in ``J`` (it cannot contain ``r0`` by (a)); between ``r0`` and ``r1`` the
  vertex set is ``V``, so by (b) the new vertex coincides at ``r1`` with a member of ``V``, which is feasible
  around ``r1``: contradiction with (a).  At an end of ``J`` a member of ``V`` becomes infeasible.

* The unbounded chamber.  For ``r > L - 1`` there are exactly ``2 N^2`` vertices, ``N`` the number of height
  functions of the cube of dimension ``L - 1`` (``2, 6, 38, 990``): two vertical edges tight with opposite signs
  at ``x+``, ``x-`` would force ``2r <= 2 d(x+, x-) <= 2 (L - 1)``; with one sign only, parity (``A(x)`` is
  congruent to the number of unit letters of ``x``) makes every horizontal edge tight, so both layers are height
  functions and the offset is fixed by the first contact.  (72, 2888, 1960200 for ``L = 3, 4, 5``.)

So an enumeration at one rational ``r0 = P/Q`` in integer arithmetic (weights ``(Q, ..., Q, P)``) gives the
exact vertex set for every real ratio of its chamber, and whether a given real ``r`` lies in the chamber is
decided by comparing ``r`` with two rationals.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

import numpy as np

from .polytope import cube_edges, node_perm_table


def site_perms(L: int):
    """The coordinate permutations that fix the weighted site ``L - 1``."""
    import itertools

    return [s + (L - 1,) for s in itertools.permutations(range(L - 1))]


def group_table(L: int) -> np.ndarray:
    return node_perm_table(L, site_perms(L))


def generic_ratio(lo: Fraction, hi: Fraction | None = None, Q: int = 101):
    """Integer weights ``(Q, P)`` with ``lo < P/Q`` as close to ``lo`` as the denominator allows (and below
    ``hi``), ``gcd(P, Q) = 1``."""
    lo = Fraction(lo)
    P = (lo.numerator * Q) // lo.denominator + 1
    while gcd(P, Q) != 1:
        P += 1
    if hi is not None and Fraction(P, Q) >= hi:
        raise ValueError("denominator too small for this interval")
    return Q, P


def to_symbolic(reps: np.ndarray, Q: int, P: int):
    """Integer vertices ``N`` at the weights ``(Q, ..., Q, P)`` -> symbolic vertices ``(A, B)`` with
    ``N = Q A + P B``, ``|B| < Q/2``.  (Decoding only: that the result is a symbolic vertex is checked by
    ``check_symbolic``.)"""
    if gcd(P, Q) != 1:
        raise ValueError("P and Q must be coprime")
    N = np.asarray(reps, dtype=np.int64)
    N = N - N[:, :1]
    Pinv = pow(P, -1, Q)
    B = (N * Pinv) % Q
    B = np.where(B > Q // 2, B - Q, B)
    A = (N - P * B) // Q
    if not np.array_equal(Q * A + P * B, N):
        raise AssertionError("decoding failed")
    if np.abs(A).max(initial=0) > 120 or np.abs(B).max(initial=0) > 120:
        raise AssertionError("symbolic coordinates out of the int8 range")
    return A.astype(np.int8), B.astype(np.int8)


def evaluate(A: np.ndarray, B: np.ndarray, Q: int, P: int) -> np.ndarray:
    return Q * A.astype(np.int64) + P * B.astype(np.int64)


def _edge_arrays(L: int):
    ed = cube_edges(L)
    hx = np.array([x for (x, y, i) in ed if i < L - 1], dtype=np.int64)
    hy = np.array([y for (x, y, i) in ed if i < L - 1], dtype=np.int64)
    vx = np.array([x for (x, y, i) in ed if i == L - 1], dtype=np.int64)
    vy = np.array([y for (x, y, i) in ed if i == L - 1], dtype=np.int64)
    return hx, hy, vx, vy


def identically_tight_connected(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """For every row: is the graph of identically tight edges connected?  (Label propagation, exact.)"""
    A = np.asarray(A, dtype=np.int16)
    B = np.asarray(B, dtype=np.int16)
    m, n = A.shape
    L = n.bit_length() - 1
    hx, hy, vx, vy = _edge_arrays(L)
    th = (np.abs(A[:, hy] - A[:, hx]) == 1) & (B[:, hy] == B[:, hx])
    tv = (np.abs(B[:, vy] - B[:, vx]) == 1) & (A[:, vy] == A[:, vx])
    ex = np.concatenate([hx, vx])
    ey = np.concatenate([hy, vy])
    tight = np.concatenate([th, tv], axis=1)
    lab = np.broadcast_to(np.arange(n, dtype=np.int16), (m, n)).copy()
    for _ in range(n):
        before = lab.sum(dtype=np.int64)
        for k in range(len(ex)):
            x, y = ex[k], ey[k]
            mn = np.minimum(lab[:, x], lab[:, y])
            t = tight[:, k]
            lab[:, x] = np.where(t, mn, lab[:, x])
            lab[:, y] = np.where(t, mn, lab[:, y])
        if lab.sum(dtype=np.int64) == before:
            break
    return (lab == 0).all(axis=1)


def check_symbolic(A: np.ndarray, B: np.ndarray, Q: int, P: int) -> None:
    """Raise unless every row is a symbolic vertex that is feasible at ``r0 = P/Q`` and has no tight edge at
    ``r0`` other than its identically tight ones (the hypotheses of the chamber lemma)."""
    A16 = np.asarray(A, dtype=np.int64)
    B16 = np.asarray(B, dtype=np.int64)
    n = A16.shape[1]
    L = n.bit_length() - 1
    if np.any(A16[:, 0] != 0) or np.any(B16[:, 0] != 0):
        raise AssertionError("rows are not normalised at node 0")
    hx, hy, vx, vy = _edge_arrays(L)
    dAh, dBh = A16[:, hy] - A16[:, hx], B16[:, hy] - B16[:, hx]
    dAv, dBv = A16[:, vy] - A16[:, vx], B16[:, vy] - B16[:, vx]
    dh = np.abs(Q * dAh + P * dBh)
    dv = np.abs(Q * dAv + P * dBv)
    if np.any(dh > Q) or np.any(dv > P):
        raise AssertionError("a row is infeasible at r0")
    if np.any((dh == Q) & ~((np.abs(dAh) == 1) & (dBh == 0))) or np.any((dv == P) & ~((np.abs(dBv) == 1) & (dAv == 0))):
        raise AssertionError("r0 is not generic: an edge is tight at r0 but not identically")
    if not identically_tight_connected(A, B).all():
        raise AssertionError("a row is not a symbolic vertex (identically tight graph disconnected)")


def _horizontal_interval(dA: int, dB: int):
    """``{r > 0 : |dA + r dB| <= 1}`` as ``(lo, hi)``; ``hi`` None = unbounded; returns None if empty."""
    if dB == 0:
        return (Fraction(0), None) if abs(dA) <= 1 else None
    a, b = Fraction(-1 - dA, dB), Fraction(1 - dA, dB)
    lo, hi = min(a, b), max(a, b)
    lo = max(lo, Fraction(0))
    return (lo, hi) if hi >= lo else None


def _vertical_interval(dA: int, dB: int):
    """``{r > 0 : |dA + r dB| <= r}`` as ``(lo, hi)``; ``hi`` None = unbounded; returns None if empty."""
    lo, hi = Fraction(0), None

    def upper(v):
        nonlocal hi
        hi = v if hi is None else min(hi, v)

    # dA + r (dB - 1) <= 0
    if dB - 1 > 0:
        upper(Fraction(-dA, dB - 1))
    elif dB - 1 == 0:
        if dA > 0:
            return None
    else:
        lo = max(lo, Fraction(dA, 1 - dB))
    # dA + r (dB + 1) >= 0
    if dB + 1 > 0:
        lo = max(lo, Fraction(-dA, dB + 1))
    elif dB + 1 == 0:
        if dA < 0:
            return None
    else:
        upper(Fraction(dA, -dB - 1))
    if hi is not None and hi < lo:
        return None
    return lo, hi


def validity_interval(A, B):
    """Interval of validity ``(lo, hi)`` (``hi`` None = unbounded) of ONE symbolic vertex."""
    n = len(A)
    L = n.bit_length() - 1
    lo, hi = Fraction(0), None
    for (x, y, i) in cube_edges(L):
        dA, dB = int(A[y]) - int(A[x]), int(B[y]) - int(B[x])
        iv = _horizontal_interval(dA, dB) if i < L - 1 else _vertical_interval(dA, dB)
        if iv is None:
            raise ValueError("nowhere feasible")
        lo = max(lo, iv[0])
        if iv[1] is not None:
            hi = iv[1] if hi is None else min(hi, iv[1])
    if hi is not None and hi < lo:
        raise ValueError("nowhere feasible")
    return lo, hi


def chamber_of(A: np.ndarray, B: np.ndarray):
    """The chamber ``(lo, hi)`` of a set of symbolic vertices: the intersection of their intervals of validity
    (exact rationals; ``hi`` None = unbounded).  Also returns, for every row, whether it attains the lower /
    upper wall (those are the vertices that cease to exist beyond it)."""
    A16 = np.asarray(A, dtype=np.int64)
    B16 = np.asarray(B, dtype=np.int64)
    m, n = A16.shape
    L = n.bit_length() - 1
    hx, hy, vx, vy = _edge_arrays(L)
    lo, hi = Fraction(0), None
    off = 512
    per_kind = []
    for kind, (ex, ey) in (("h", (hx, hy)), ("v", (vx, vy))):
        code = (A16[:, ey] - A16[:, ex] + off) * (2 * off) + (B16[:, ey] - B16[:, ex] + off)
        uniq = np.unique(code)
        table = {}
        for c in uniq:
            dA, dB = int(c) // (2 * off) - off, int(c) % (2 * off) - off
            iv = _horizontal_interval(dA, dB) if kind == "h" else _vertical_interval(dA, dB)
            if iv is None:
                raise ValueError("a symbolic vertex is nowhere feasible")
            table[int(c)] = iv
            lo = max(lo, iv[0])
            if iv[1] is not None:
                hi = iv[1] if hi is None else min(hi, iv[1])
        per_kind.append((code, table))
    at_lo = np.zeros(m, dtype=bool)
    at_hi = np.zeros(m, dtype=bool)
    for code, table in per_kind:
        lo_codes = [c for c, iv in table.items() if iv[0] == lo]
        hi_codes = [c for c, iv in table.items() if hi is not None and iv[1] == hi]
        if lo_codes:
            at_lo |= np.isin(code, lo_codes).any(axis=1)
        if hi_codes:
            at_hi |= np.isin(code, hi_codes).any(axis=1)
    return lo, hi, at_lo, at_hi


def valid_at(A: np.ndarray, B: np.ndarray, inside) -> np.ndarray:
    """Which symbolic vertices are vertices at a given (possibly irrational) ratio ``r``?  ``inside(lo, hi)`` must
    decide rigorously whether ``lo < r < hi`` for rationals ``lo, hi`` (``hi`` may be None).  A row is accepted
    iff ``r`` lies strictly inside the feasibility interval of every one of its edges; rows are assumed to be
    symbolic vertices (connected identically tight graph), so the accepted rows are vertices of ``P(r)``."""
    A16 = np.asarray(A, dtype=np.int64)
    B16 = np.asarray(B, dtype=np.int64)
    m, n = A16.shape
    L = n.bit_length() - 1
    hx, hy, vx, vy = _edge_arrays(L)
    ok = np.ones(m, dtype=bool)
    off = 512
    for kind, (ex, ey) in (("h", (hx, hy)), ("v", (vx, vy))):
        if len(ex) == 0:
            continue
        code = (A16[:, ey] - A16[:, ex] + off) * (2 * off) + (B16[:, ey] - B16[:, ex] + off)
        good = []
        for c in np.unique(code):
            dA, dB = int(c) // (2 * off) - off, int(c) % (2 * off) - off
            iv_ = _horizontal_interval(dA, dB) if kind == "h" else _vertical_interval(dA, dB)
            if iv_ is None:
                continue
            identically = (abs(dA) <= 1 and dB == 0) if kind == "h" else (dA == 0 and abs(dB) <= 1)
            if identically or inside(iv_[0], iv_[1]):
                good.append(int(c))
        ok &= np.isin(code, good).all(axis=1)
    return ok


def image_rows(A: np.ndarray, B: np.ndarray, table: np.ndarray, rep: np.ndarray, g: np.ndarray):
    """The images ``g`` (kernel convention ``g = (eps * n + t) * nperm + k``) of the rows ``rep`` of ``(A, B)``,
    normalised at node 0."""
    nperm, n = table.shape
    rep = np.asarray(rep, dtype=np.int64)
    g = np.asarray(g, dtype=np.int64)
    k = g % nperm
    t = (g // nperm) % n
    eps = np.where(g // (nperm * n) == 1, -1, 1).astype(np.int16)
    idx = table[k].astype(np.int64) ^ t[:, None]
    Ai = np.take_along_axis(A[rep].astype(np.int16), idx, axis=1) * eps[:, None]
    Bi = np.take_along_axis(B[rep].astype(np.int16), idx, axis=1) * eps[:, None]
    return (Ai - Ai[:, :1]).astype(np.int8), (Bi - Bi[:, :1]).astype(np.int8)


def expand_orbits(A: np.ndarray, B: np.ndarray, table: np.ndarray):
    """All distinct vertices of the orbits of the rows (normalised at node 0), as two int8 arrays, and for
    every row the size of its orbit.  Memory: ``2 * nperm * n`` images per row before deduplication."""
    nperm, n = table.shape
    m = A.shape[0]
    ng = 2 * nperm * n
    out_A, out_B, sizes = [], [], []
    g = np.arange(ng)
    for r in range(m):
        Ai, Bi = image_rows(A, B, table, np.full(ng, r), g)
        both = np.concatenate([Ai, Bi], axis=1)
        uniq = np.unique(both, axis=0)
        out_A.append(uniq[:, :n])
        out_B.append(uniq[:, n:])
        sizes.append(len(uniq))
    return np.concatenate(out_A), np.concatenate(out_B), np.array(sizes, dtype=np.int64)


def multiset_checksum(A: np.ndarray, B: np.ndarray, table: np.ndarray):
    """Order-independent checksum of the FULL vertex list of the orbits of the rows: the sum modulo ``2^256`` of
    the SHA-256 digests of all distinct vertices (each as the 2n bytes ``A || B`` of int8 values, normalised at
    node 0).  Returns ``(hex string, number of vertices)``."""
    import hashlib

    nperm, n = table.shape
    ng = 2 * nperm * n
    g = np.arange(ng)
    total, count = 0, 0
    for r in range(A.shape[0]):
        Ai, Bi = image_rows(A, B, table, np.full(ng, r), g)
        uniq = np.unique(np.concatenate([Ai, Bi], axis=1), axis=0)
        for row in uniq:
            total += int.from_bytes(hashlib.sha256(row.tobytes()).digest(), "big")
        count += len(uniq)
    return format(total % (1 << 256), "064x"), count


@dataclass
class Chamber:
    """The exact vertex set of ``P(1, ..., 1, r)`` for every ``r`` in the open interval ``(lo, hi)``."""
    L: int
    lo: Fraction
    hi: Fraction | None
    Q: int
    P: int
    A: np.ndarray          # orbit representatives, symbolic
    B: np.ndarray
    stab: np.ndarray       # orders of the stabilisers
    deg: np.ndarray        # number of polytope edges at the representative
    n_vertices: int
    at_lo: np.ndarray
    at_hi: np.ndarray

    @property
    def n_orbits(self) -> int:
        return len(self.stab)

    @property
    def orbit_sizes(self) -> np.ndarray:
        return (2 * len(site_perms(self.L)) * (1 << self.L)) // self.stab.astype(np.int64)

    def contains(self, r) -> bool:
        return self.lo < r and (self.hi is None or r < self.hi)


def chamber_at(L: int, Q: int, P: int, max_orbits: int = 4_000_000, max_vertices: int = 10 ** 7) -> Chamber | None:
    """Enumerate at ``r0 = P/Q`` with the kernel and return the chamber of ``r0`` (None if the enumeration was
    stopped by a limit; raises if ``r0`` is not generic, i.e. lies on a wall)."""
    from . import ckernel

    wts = (Q,) * (L - 1) + (P,)
    res = ckernel.enumerate_orbits(wts, perms=site_perms(L), max_orbits=max_orbits, max_vertices=max_vertices)
    if res.status in (1, 2):
        return None
    if res.status != 0:
        raise RuntimeError("kernel: " + ckernel.STATUS[res.status])
    A, B = to_symbolic(res.reps, Q, P)
    check_symbolic(A, B, Q, P)
    lo, hi, at_lo, at_hi = chamber_of(A, B)
    r0 = Fraction(P, Q)
    if not (lo < r0 and (hi is None or r0 < hi)):
        raise AssertionError("r0 is not inside its chamber")
    return Chamber(L, lo, hi, Q, P, A, B, res.stab, res.deg, res.n_vertices, at_lo, at_hi)


def walk_chambers(L: int, start: Fraction = Fraction(1), stop: Fraction | None = None, Q: int = 101,
                  max_orbits: int = 4_000_000, max_vertices: int = 10 ** 7, verbose: bool = False):
    """All chambers of ``P(1, ..., 1, r)`` from the wall ``start`` upwards (until the unbounded chamber, or
    until the lower wall reaches ``stop``).  Each step enumerates just above the previous wall and checks that
    the chamber found begins exactly at that wall (otherwise the denominator is increased)."""
    out = []
    c = Fraction(start)
    while True:
        q = Q
        while True:
            Qq, Pp = generic_ratio(c, None, q)
            ch = chamber_at(L, Qq, Pp, max_orbits=max_orbits, max_vertices=max_vertices)
            if ch is None:
                return out, c
            if ch.lo <= c:
                break
            q = 2 * q + 1          # a wall lies between c and r0: look closer to c
        if verbose:
            print(f"L={L}: chamber ({ch.lo}, {ch.hi}): {ch.n_vertices} vertices, {ch.n_orbits} orbits", flush=True)
        out.append(ch)
        if ch.hi is None or (stop is not None and ch.hi >= stop):
            return out, None
        c = ch.hi
