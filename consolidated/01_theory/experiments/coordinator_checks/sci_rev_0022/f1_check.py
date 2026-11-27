"""Coordinator's check of finding F1 of SCI-REV-0022 (science division, workstream R23).

Claim checked: Theorem 11.32 of the theory report (K_- <= N_2 <= (n+1) K_+ + 1 for the class of
residuals with mixed second differences bounded by c) needs its hypothesis "the true residual is
additive": at the class member g0 = -c*C(|x|,2) (all mixed second differences equal to -c) with
E = f + g0 = e|x|, e < c/n, the star at the origin certifies the minimum exactly, so N_2 <= n + 1,
while K_- = 2^n.  And the substitute: if |D_i D_j g| <= kappa*c, kappa < 1, then
K_-[(1-kappa)c] <= N_2 <= (n+1) K_+[(1+kappa)c] + 1.

Own code (linear programmes over the whole class with scipy), written from the statement; the
science division's scripts were not read.  Exhaustive over evaluation sets for n = 2, 3.
"""
import itertools, math, sys
import numpy as np
from scipy.optimize import linprog

def cube(n):
    return list(itertools.product((0, 1), repeat=n))

def constraints(n, c):
    """|D_i D_j g(x)| <= c for all i < j and all base points x with x_i = x_j = 0."""
    pts = cube(n); idx = {p: k for k, p in enumerate(pts)}
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            for p in pts:
                if p[i] == 0 and p[j] == 0:
                    pi = list(p); pi[i] = 1; pj = list(p); pj[j] = 1; pij = list(p); pij[i] = 1; pij[j] = 1
                    r = np.zeros(len(pts)); r[idx[tuple(pij)]] += 1; r[idx[tuple(pi)]] -= 1; r[idx[tuple(pj)]] -= 1; r[idx[p]] += 1
                    rows.append(r)
    A = np.array(rows)
    return pts, idx, np.vstack([A, -A]), np.full(2 * len(rows), c)

def lower_envelope(n, c, f, g0, Aset):
    """min over class members g' with g' = g0 on Aset of (f + g')(y), for every y."""
    pts, idx, Aub, bub = constraints(n, c)
    Aeq = np.zeros((len(Aset), len(pts))); beq = np.zeros(len(Aset))
    for r, a in enumerate(Aset):
        Aeq[r, idx[a]] = 1; beq[r] = g0[idx[a]]
    out = []
    for y in pts:
        cvec = np.zeros(len(pts)); cvec[idx[y]] = 1
        res = linprog(cvec, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * len(pts), method="highs")
        if res.status == 0:
            out.append(f[idx[y]] + res.fun)
        else:               # unbounded below (status 3) or reported infeasible for a free LP
            out.append(-math.inf)
    return np.array(out)

def certifies(n, c, f, g0, Aset, eps):
    pts = cube(n); idx = {p: k for k, p in enumerate(pts)}
    E = f + g0
    best = min(E[idx[a]] for a in Aset)
    low = lower_envelope(n, c, f, g0, Aset)
    return best - low.min() <= eps + 1e-9

def N2(n, c, f, g0, eps):
    pts = cube(n)
    for size in range(1, len(pts) + 1):
        for Aset in itertools.combinations(pts, size):
            if certifies(n, c, f, g0, Aset, eps):
                return size, Aset
    return None

def K_cover(n, c, E, eps, plus=False):
    """Least size of a code covering every y within rho_-(y) (or rho_+ = rho_- + 1)."""
    pts = cube(n); gap = E - E.min()
    def rho(y):
        d = 0
        while c * math.comb(d + 2, 2) <= gap[y] + eps + 1e-12:
            d += 1
        return d + (1 if plus else 0)
    R = [rho(k) for k in range(len(pts))]
    ham = lambda p, q: sum(a != b for a, b in zip(p, q))
    for size in range(1, len(pts) + 1):
        for C in itertools.combinations(range(len(pts)), size):
            if all(any(ham(pts[y], pts[cc]) <= R[y] for cc in C) for y in range(len(pts))):
                return size
    return None

ok = True
print("# Part 1: the boundary member g0 = -c*C(|x|,2), E = e|x|, c = 1, e = 0.1, eps = 0")
for n in (2, 3):
    pts = cube(n); w = np.array([sum(p) for p in pts], dtype=float)
    c, e = 1.0, 0.1
    g0 = -c * np.array([math.comb(int(k), 2) for k in w], dtype=float)
    E = e * w; f = E - g0
    size, Aset = N2(n, c, f, g0, 0.0)
    Km = K_cover(n, c, E, 0.0)
    print("n = %d: N_2 = %d (a certifying set: %s);  K_- = %d;  K_- <= N_2 %s" % (n, size, Aset, Km, "HOLDS" if Km <= size else "FAILS"))
    ok &= (size < Km)
    # control: the additive (zero) residual, where the theorem applies
    g00 = np.zeros(len(pts)); size0, _ = N2(n, c, E, g00, 0.0)
    Km0 = K_cover(n, c, E, 0.0); Kp0 = K_cover(n, c, E, 0.0, plus=True)
    print("   control, zero residual: N_2 = %d, K_- = %d, (n+1)K_+ + 1 = %d: sandwich %s" % (size0, Km0, (n + 1) * Kp0 + 1, "holds" if Km0 <= size0 <= (n + 1) * Kp0 + 1 else "FAILS"))
    ok &= (Km0 <= size0 <= (n + 1) * Kp0 + 1)

print("# Part 2: the substitute K_-[(1-kappa)c] <= N_2 <= (n+1)K_+[(1+kappa)c] + 1 for |D_iD_j g| <= kappa*c; n = 3")
rng = np.random.default_rng(20261126)
n = 3; pts = cube(n); idx = {p: k for k, p in enumerate(pts)}; w = np.array([sum(p) for p in pts], dtype=float)
viol_sub = 0; viol_orig = 0; cases = 0
for kappa in (0.0, 0.5, 0.9):
    for trial in range(6):
        c = 1.0
        a = rng.uniform(-kappa * c, kappa * c, size=(n, n))
        lin = rng.uniform(-0.3, 0.3, size=n)
        g = np.array([sum(lin[i] * p[i] for i in range(n)) + sum(a[i, j] * p[i] * p[j] for i in range(n) for j in range(i + 1, n)) for p in pts])
        e = rng.uniform(0.05, 1.6)
        E = e * w + rng.uniform(0, 0.05, size=len(pts)); f = E - g
        size, _ = N2(n, c, f, g, 0.0)
        lo = K_cover(n, (1 - kappa) * c, E, 0.0) if kappa < 1 else 1
        hi = (n + 1) * K_cover(n, (1 + kappa) * c, E, 0.0, plus=True) + 1
        lo_orig = K_cover(n, c, E, 0.0)
        cases += 1
        if not (lo <= size <= hi): viol_sub += 1
        if not (lo_orig <= size): viol_orig += 1
    print("kappa = %.1f: cases so far %d; violations of the substitute %d; of the original lower bound K_-[c] <= N_2: %d" % (kappa, cases, viol_sub, viol_orig))
ok &= (viol_sub == 0)
print("RESULT:", "ALL CHECKS PASS (the counterexample is confirmed; the substitute holds in every case)" if ok else "SOME CHECK FAILED")
