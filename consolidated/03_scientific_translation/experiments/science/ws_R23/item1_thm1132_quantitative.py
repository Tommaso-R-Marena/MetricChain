#!/usr/bin/env python3
"""R23: the quantitative substitute for "the true residual is additive" in Theorem 11.32 (replacement tag {F}{Q} for AA1 l.1262).

Statement S [P, proved in R23_REPORT.md §2; tested here]:  let the true residual g be in G2(c) with |D_iD_j g| <= kappa*c, kappa < 1, f arbitrary.  Then
        K_-[(1-kappa) c]  <=  N2(g)        (and N2(g) <= (n+1) K_+[(1+kappa) c] + 1),
where K_-[c'] is the covering number of Theorem 11.32 computed with the constant c' (rho_-(y) = max{d : c' C(d+1,2) <= gap(y)+eps}).
Proof of the lower bound: g - (1-kappa)*b_{y,r} is a member (|D_iD_j| <= kappa c + (1-kappa) c), agrees with g outside B(y, r-2) and is lower by (1-kappa) c C(r,2) at y.

Test: n = 3, c = 1, random f, random residual g = additive + sum_{i<j} a_ij x_i x_j with |a_ij| <= kappa (so D_iD_j g = a_ij), eps = 0;
N2 exactly by linear programming over the class for every evaluation set (as in item1_thm1132_additive_v2.py); K_- by brute force.
Controls: kappa = 0 is the theorem as stated (K_-[c] <= N2); at kappa = 1 the bound K_-[c] <= N2 may fail (it does at the boundary member).
Run: OMP_NUM_THREADS=1 python3 -I -B item1_thm1132_quantitative.py     (about 2-4 minutes)
"""
import itertools, math, time
import numpy as np
from scipy.optimize import linprog
t0 = time.time()
n = 3; N = 1 << n; c = 1.0; eps = 0.0
pc = [bin(i).count("1") for i in range(N)]
rows = []; rhs = []
for i in range(n):
    for j in range(i + 1, n):
        for x in range(N):
            if (x >> i) & 1 or (x >> j) & 1: continue
            r = np.zeros(N); r[x | (1 << i) | (1 << j)] += 1; r[x | (1 << i)] -= 1; r[x | (1 << j)] -= 1; r[x] += 1
            rows.append(r); rhs.append(c); rows.append(-r); rhs.append(c)
A_ub = np.array(rows); b_ub = np.array(rhs)
def certifies(f, g, A):
    A_eq = np.zeros((len(A), N)); b_eq = np.array([g[a] for a in A])
    for k, a in enumerate(A): A_eq[k, a] = 1
    lo = math.inf
    for y in range(N):
        cv = np.zeros(N); cv[y] = 1
        res = linprog(cv, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq if len(A) else None, b_eq=b_eq if len(A) else None, bounds=[(None, None)] * N, method="highs")
        if res.status in (2, 3): return False
        lo = min(lo, f[y] + res.fun)
    cv = np.zeros(N + 1); cv[N] = -1
    A2 = np.vstack([np.hstack([A_ub, np.zeros((A_ub.shape[0], 1))]), np.hstack([-np.eye(N), np.ones((N, 1))])])
    b2 = np.concatenate([b_ub, np.array(f, dtype=float)])
    Ae = np.hstack([A_eq, np.zeros((len(A), 1))]) if len(A) else None
    res = linprog(cv, A_ub=A2, b_ub=b2, A_eq=Ae, b_eq=b_eq if len(A) else None, bounds=[(None, None)] * (N + 1), method="highs")
    if res.status in (2, 3): return False
    return (-res.fun) - lo <= eps + 1e-9
def N2(f, g):
    for k in range(1, N + 1):
        for A in itertools.combinations(range(N), k):
            if certifies(f, g, list(A)): return k
def Kminus(E, cc):
    gap = [E[y] - min(E) for y in range(N)]
    rho = []
    for y in range(N):
        d = 0
        while cc * math.comb(d + 2, 2) <= gap[y] + eps + 1e-12 and d < n: d += 1
        rho.append(d)
    for k in range(1, N + 1):
        for code in itertools.combinations(range(N), k):
            if all(any(pc[y ^ a] <= rho[y] for a in code) for y in range(N)): return k
rng = np.random.default_rng(20261126)
print("kappa   instances   violations of K_-[(1-kappa)c] <= N2   violations of K_-[c] <= N2 (the theorem's display with the full constant)   min(N2 - K_-[(1-kappa)c])")
tot_viol = 0
for kappa in (0.0, 0.5, 0.9, 1.0):
    vS = vT = 0; mins = 99; ninst = 12
    for rep in range(ninst):
        a = {(i, j): rng.uniform(-kappa, kappa) * c for i in range(n) for j in range(i + 1, n)}
        if rep == 0: a = {k: -kappa * c for k in a}            # the extreme member used in the counterexample
        lin = rng.normal(size=n)
        g = np.array([sum(lin[i] for i in range(n) if (x >> i) & 1) + sum(v for (i, j), v in a.items() if (x >> i) & 1 and (x >> j) & 1) for x in range(N)])
        assert (A_ub @ g <= b_ub + 1e-12).all()
        e = rng.uniform(0.05, 0.6)
        E = np.array([e * pc[x] for x in range(N)]) if rep % 2 == 0 else rng.uniform(0, 1.5, size=N)
        f = E - g
        n2 = N2(f, g)
        kS = Kminus(E, (1 - kappa) * c) if kappa < 1 else 1
        kT = Kminus(E, c)
        vS += n2 < kS; vT += n2 < kT; mins = min(mins, n2 - kS)
    if kappa < 1: tot_viol += vS
    if kappa == 0.0: tot_viol += vT
    print(f"{kappa:5.2f}   {ninst:9d}   {vS:36d}   {vT:38d}   {mins:27d}")
    if kappa == 1.0: ctrl = vT
print(f"statement S violated: {tot_viol} times (kappa = 0, 0.5, 0.9; includes the theorem as stated at kappa = 0)")
print(f"control kappa = 1 (boundary members allowed): the theorem's display K_-[c] <= N2 fails in {ctrl} of 12 instances (violation of the control if 0)")
print(f"TOTAL violations: {tot_viol + int(ctrl == 0)}")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item1_thm1132_quantitative")
