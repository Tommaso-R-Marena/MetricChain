#!/usr/bin/env python3
"""R22 Item 3(a): the conic condition (CC) for generic pairs and triples at and below the Geometry division's
thresholds n0(2) = 12, n0(3) = 23 (and n0(1) = 5), own code (r22lib), exact rational arithmetic for the threshold
cases, floating point for random samples.

(CC): dim N(z) = K - 1, N(z) = {S in Sym(3K): e^T S e = 0 for the E0-edge vectors of the stacked configuration}.
Exact part: unit bonds, bond-angle cosine -5/13, torsions with rational half-angle tangents; the UNWEIGHTED stack
(the report says the dimension does not depend on the weights; tested in floating point below); rank over Q by
fraction-free elimination.
Controls: (c1) the trivial quadrics w_l E_k - w_k E_l lie in N(z) (residual); (c2) a pair of congruent states must
violate (CC); (c3) a planar chain (all torsions 0 or pi) must violate (CC) at K = 1; (c4) weight independence.
Run: OMP_NUM_THREADS=1 python3 -B t3a_cc_thresholds.py > t3a_cc_thresholds.log
"""
import time
from fractions import Fraction
import numpy as np
import r22lib as L

t0 = time.time()
rng = np.random.default_rng(2201)
viol = 0


def DK(K):
    return (9 * K * K + K + 2) // 2


print("=== R22 3(a): (CC) at and below the thresholds; seed 2201")
print("--- exact (Q), bond-angle cosine -5/13, unweighted stack; expected rank = min(2n-3, D_K), D_K = (9K^2+K+2)/2")
print("| K | n | 2n-3 | D_K | exact rank | dim N = dim Sym(3K) - rank | K-1 | (CC) |")
print("|---|---|---|---|---|---|---|---|")
for K, ns in ((1, (4, 5, 6)), (2, (10, 11, 12, 13)), (3, (21, 22, 23, 24))):
    for n in ns:
        for rep in range(2):
            states = []
            for k in range(K):
                tans = [Fraction(int(a), int(b)) for a, b in zip(rng.integers(-30, 31, n - 3), rng.integers(1, 12, n - 3))]
                states.append(L.chain_exact(tans))
            z = [sum((states[k][i] for k in range(K)), []) for i in range(n)]
            rows = L.conic_rows_exact(z)
            r = L.rank_exact(rows)
            m = 3 * K
            dimN = m * (m + 1) // 2 - r
            exp = min(2 * n - 3, DK(K))
            ok = (r == exp)
            viol += int(not ok)
            print(f"| {K} | {n} | {2 * n - 3} | {DK(K)} | {r} | {dimN} | {K - 1} | {'holds' if dimN == K - 1 else 'fails'} |"
                  + ("" if ok else "  <-- NOT the expected rank"))
print(f"exact part: {viol} cases with a rank different from min(2n-3, D_K)   [{time.time() - t0:.1f} s]")

print("--- floating point: random K-tuples, three bond angles; weights random; dim N(z) histogram over 20 tuples")
print("| K | cos(bond angle) | n | dims found (count) | smallest kept s.v./largest | largest dropped s.v./largest |")
print("|---|---|---|---|---|---|")
fl_viol = 0
for K, ns in ((1, (4, 5, 6)), (2, (9, 10, 11, 12, 13, 16)), (3, (21, 22, 23, 24, 28))):
    for cosang in (-1.0 / 3.0, -5.0 / 13.0, float(np.cos(np.deg2rad(111.0)))):
        for n in ns:
            dims, keep, drop = {}, 1.0, 0.0
            for rep in range(20):
                states = [L.chain(rng.uniform(-np.pi, np.pi, n - 3), cosang) for _ in range(K)]
                w = rng.dirichlet(np.ones(K) * 3.0)
                d, k_, d_ = L.conic_nullity(L.stack(states, w))
                dims[d] = dims.get(d, 0) + 1
                keep, drop = min(keep, k_), max(drop, d_)
                m = 3 * K
                expd = m * (m + 1) // 2 - min(2 * n - 3, DK(K))
                fl_viol += int(d != expd)
            print(f"| {K} | {cosang:+.4f} | {n} | " + ", ".join(f"{d} ({c})" for d, c in sorted(dims.items())) + f" | {keep:.1e} | {drop:.1e} |")
print(f"floating part: {fl_viol} tuples with dim N different from dim Sym(3K) - min(2n-3, D_K)   [{time.time() - t0:.1f} s]")

print("--- controls")
# (c1) trivial quadrics are in N(z)
c1 = 0.0
for K in (2, 3):
    n = 14
    states = [L.chain(rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(K)]
    w = rng.dirichlet(np.ones(K) * 3.0)
    z = L.stack(states, w)
    for k in range(K):
        for l in range(k + 1, K):
            S = np.zeros((3 * K, 3 * K))
            S[3 * k:3 * k + 3, 3 * k:3 * k + 3] = w[l] * np.eye(3)
            S[3 * l:3 * l + 3, 3 * l:3 * l + 3] = -w[k] * np.eye(3)
            for (i, j) in L.E0(n):
                e = z[j] - z[i]
                c1 = max(c1, abs(e @ S @ e))
print(f"(c1) largest |e^T S e| over trivial quadrics S = w_l E_k - w_k E_l and E0-edges (K = 2, 3; n = 14): {c1:.1e} (must be ~1e-16)")
# (c2) congruent states
n = 14
X = L.chain(rng.uniform(-np.pi, np.pi, n - 3))
Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
d2, _, _ = L.conic_nullity(L.stack([X, X @ Q.T + 1.0], [0.4, 0.6]))
print(f"(c2) two congruent states, n = 14: dim N = {d2} (must be > 1: (CC) must fail)")
# (c3) planar chain
dpl = []
for n in (6, 10, 20):
    tors = rng.choice([0.0, np.pi], n - 3)
    dpl.append(L.conic_nullity(L.chain(tors))[0])
print(f"(c3) planar chains (torsions 0 or pi), K = 1, n = 6, 10, 20: dim N = {dpl} (must be > 0)")
# (c4) weight independence
n = 12
states = [L.chain(rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(2)]
ds = [L.conic_nullity(L.stack(states, [w1, 1 - w1]))[0] for w1 in (0.5, 0.37, 0.05, 0.001)]
n = 11
states = [L.chain(rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(2)]
ds11 = [L.conic_nullity(L.stack(states, [w1, 1 - w1]))[0] for w1 in (0.5, 0.37, 0.05, 0.001)]
print(f"(c4) the same pair with weights w1 = 0.5, 0.37, 0.05, 0.001: dim N at n = 12: {ds}; at n = 11: {ds11} (must not depend on w)")
ctrl_viol = int(c1 > 1e-12) + int(d2 <= 1) + int(min(dpl) <= 0) + int(len(set(ds)) != 1 or len(set(ds11)) != 1)
print(f"control violations: {ctrl_viol}")
print(f"TOTAL violations: exact {viol}, floating {fl_viol}, controls {ctrl_viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
