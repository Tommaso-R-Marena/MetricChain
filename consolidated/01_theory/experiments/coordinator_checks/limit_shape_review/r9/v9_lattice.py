#!/usr/bin/env python3
"""V9 -- Theorem R9.1(e): the clean bridges generate Z^5 (grading: M = N + 3; vectors (h3, h8, h11, g; N + 3)).

Input: the dump of `v9_cobound single 11 0 1 11` (every (bridge, c1) with N <= 11 in the reduced set, with the clean
flag of the C program); every clean bridge used below is re-verified here from coordinates with the Python
implementation v9_lib.py (walk, bridge, clean, (h,g) by two counts).

 1. the Z-span of the vectors of the clean bridges with at most Nmax beads, Nmax = 3..11: rank and index in Z^5
    (integer row reduction, exact integers);
 2. R9's five vectors (0,0,1,1;7), (0,0,1,1;8), (0,2,6,5;12), (0,3,6,4;12), (1,6,11,7;14): do clean bridges with
    4, 5, 9, 9, 11 beads have them?  determinant (exact, by Bareiss elimination and by the Leibniz formula);
 3. R9's four profile vectors (0,0,1;7), (0,0,1;8), (0,1,3;10), (1,6,10;13): the same;
 4. an own unimodular choice: the five clean bridges with the smallest total number of beads whose vectors have
    determinant +-1 (exhaustive over the distinct vectors with N <= 10 and N <= 11).
usage: v9_lattice.py DUMPFILE
"""
import sys, itertools
sys.dont_write_bytecode = True
from fractions import Fraction
from v9_lib import *


def row_reduce(rows):
    """integer row echelon form (a basis of the Z-span), by Euclid on each column"""
    rows = [list(r) for r in rows if any(r)]
    basis = []
    ncol = len(rows[0])
    for col in range(ncol):
        piv = [r for r in rows if r[col] != 0]
        rest = [r for r in rows if r[col] == 0]
        while len(piv) > 1:
            piv.sort(key=lambda r: abs(r[col]))
            p = piv[0]
            new = [p]
            for r in piv[1:]:
                q = r[col] // p[col]
                r2 = [a - q * b for a, b in zip(r, p)]
                if r2[col] != 0:
                    new.append(r2)
                elif any(r2):
                    rest.append(r2)
            piv = new
        if piv:
            basis.append(piv[0])
        rows = rest
        if not rows:
            break
    return basis


def index_of_span(basis, ncol):
    if len(basis) < ncol:
        return None
    d = 1
    for i, r in enumerate(basis):
        d *= abs(r[i])       # echelon form: the pivot of row i is in column i when the rank is full
    return d


def det_bareiss(M):
    M = [list(r) for r in M]
    n = len(M)
    sign = 1
    prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def det_leibniz(M):
    n = len(M)
    tot = 0
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        p = 1
        for i in range(n):
            p *= M[i][perm[i]]
        tot += (-1) ** inv * p
    return tot


clean = {}      # vector -> first clean bridge (coordinates) found with it
byN = {}
seen = set()
for line in open(sys.argv[1]):
    if not line.startswith("D "):
        continue
    f = line[2:].split("|")
    head = [int(t) for t in f[0].split()]
    N = head[0]
    co = [int(t) for t in f[5].split()]
    x = tuple(tuple(co[3 * i:3 * i + 3]) for i in range(N))
    if x in seen:
        continue
    seen.add(x)
    if int(f[4]) != 1:
        continue
    xl = list(x)
    check_bridge(xl)
    assert is_clean(xl)
    hg = ML.profile_hash(xl)
    assert hg == ML.profile_bruteforce(xl) == tuple(head[1:5])
    v = hg + (N + 3,)
    clean.setdefault(v, xl)
    byN.setdefault(N, set()).add(v)
print("clean bridges re-verified from coordinates (Python): distinct vectors (h3,h8,h11,g; N+3) per N:", {N: len(s) for N, s in sorted(byN.items())})

print("\n1. Z-span of the vectors of the clean bridges with at most Nmax beads")
acc = set()
for N in sorted(byN):
    acc |= byN[N]
    B = row_reduce(sorted(acc))
    ix = index_of_span(B, 5)
    print(f"   Nmax = {N:2d}: {len(acc):3d} distinct vectors; rank {len(B)}; index in Z^5: {ix if ix is not None else '(rank < 5)'}; echelon basis {B}")
    P = row_reduce(sorted(set(v[:3] + (v[4],) for v in acc)))
    ixp = index_of_span(P, 4)
    print(f"              profiles (h3,h8,h11; N+3): rank {len(P)}; index in Z^4: {ixp if ixp is not None else '(rank < 4)'}")

print("\n2. the five vectors of R9_REPORT 4.3(e)")
R9 = [((0, 0, 1, 1, 7), 4), ((0, 0, 1, 1, 8), 5), ((0, 2, 6, 5, 12), 9), ((0, 3, 6, 4, 12), 9), ((1, 6, 11, 7, 14), 11)]
for v, N in R9:
    assert v[4] == N + 3
    ok = v in clean
    print(f"   {v}: N = {N}; a clean bridge with this vector exists: {ok}" + (f"; e.g. {clean[v]}" if ok else ""))
    assert ok
M = [list(v) for v, _ in R9]
print(f"   determinant: {det_bareiss(M)} (Bareiss), {det_leibniz(M)} (Leibniz)")
assert abs(det_bareiss(M)) == 1 and det_bareiss(M) == det_leibniz(M)

print("\n3. the four profile vectors of R9_REPORT 4.3(e)  (h3,h8,h11; N+3)")
R9p = [(0, 0, 1, 7), (0, 0, 1, 8), (0, 1, 3, 10), (1, 6, 10, 13)]
prof = {}
for v, x in clean.items():
    prof.setdefault(v[:3] + (v[4],), x)
for v in R9p:
    ok = v in prof
    print(f"   {v}: a clean bridge with this profile vector exists: {ok}" + (f"; e.g. {prof[v]}" if ok else ""))
    assert ok
Mp = [list(v) for v in R9p]
print(f"   determinant: {det_bareiss(Mp)} (Bareiss), {det_leibniz(Mp)} (Leibniz)")
assert abs(det_bareiss(Mp)) == 1 and det_bareiss(Mp) == det_leibniz(Mp)

print("\n4. own unimodular choices (smallest total number of beads)")
import numpy as np
for Nmax in (9, 10, 11):
    vecs = sorted(set().union(*[byN[N] for N in byN if N <= Nmax]), key=lambda v: (v[4], v))
    V = np.array(vecs, dtype=np.int64)
    n = len(vecs)
    beads = V[:, 4] - 3
    idx4 = np.array(list(itertools.combinations(range(n), 4)), dtype=np.int32)
    best = None
    nuni = 0
    for lo in range(0, len(idx4), 200000):
        I = idx4[lo:lo + 200000]
        mats = V[I].astype(float)                               # (m, 4, 5)
        W = np.empty((len(I), 5), dtype=np.int64)
        for k in range(5):                                      # cofactor vector: det[rows; v] = W . v
            W[:, k] = (-1) ** (4 + k) * np.rint(np.linalg.det(np.delete(mats, k, axis=2))).astype(np.int64)
        Dm = W @ V.T                                            # (m, n) exact in int64
        later = np.arange(n)[None, :] > I[:, 3][:, None]        # fifth index beyond the fourth: each 5-subset once
        hit = (np.abs(Dm) == 1) & later
        nuni += int(hit.sum())
        if hit.any():
            tot = beads[I].sum(1)[:, None] + beads[None, :]
            tot = np.where(hit, tot, 10 ** 9)
            a, b = np.unravel_index(np.argmin(tot), tot.shape)
            if best is None or tot[a, b] < best[0]:
                best = (int(tot[a, b]), tuple(int(t) for t in I[a]) + (int(b),))
    if best is None:
        print(f"   N <= {Nmax}: no five vectors with determinant +-1 among the {n} distinct vectors (C({n},5) subsets)")
        continue
    comb = [vecs[t] for t in best[1]]
    d = det_bareiss([list(v) for v in comb])
    assert abs(d) == 1 and d == det_leibniz([list(v) for v in comb])
    print(f"   N <= {Nmax}: {nuni} unimodular 5-subsets of the {n} distinct vectors; one with the fewest beads ({best[0]} in all), determinant {d} (exact):")
    for v in comb:
        print(f"      {v}  N = {v[4]-3}: {clean[v]}")
