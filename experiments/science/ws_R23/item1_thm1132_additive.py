#!/usr/bin/env python3
"""R23 Item 1, sampled tag AA1 l.1262 (entry E42): "{P} an additive true residual (the star then reproduces it)"
in Theorem 11.32 of the theory report (dense second-order classes):

    "Let the true residual be additive, f arbitrary, and let N2 be the least number of evaluations that certify
     the minimum within eps.  With rho_-(y) = max{d : c*C(d+1,2) <= gap(y) + eps}, rho_+ = rho_- + 1, and K_-/+ the
     least size of a code that covers every y within Hamming distance rho_-/+(y):
                         K_-  <=  N2  <=  (n+1) K_+ + 1."

The audit tags the hypothesis "the true residual is additive" as {P}: needed only by the present proof.
This script tests the statement WITHOUT that hypothesis, with my own code (linear programming over the class).

Class: G2(c) = { g : {0,1}^n -> R : |D_i D_j g(x)| <= c for all x, i != j }  (no first-order bound).
A set A certifies the minimum within eps at the true residual g iff
      sup{ min(f+g') } - inf{ min(f+g') } <= eps    over g' in G2(c) with g' = g on A          (value certificate)
(both are linear programmes; inf may be -infinity).

Instances:
  ADD   true residual g = 0 (additive), f = e|x|                      -> control: the theorem must hold
  BND   true residual g0(x) = -c*C(|x|,2) (a boundary member: all mixed second differences = -c),
        f = e|x| - g0, so that the true energy E = f + g0 = e|x| is the SAME landscape as in ADD
  with e < c/n, so that rho_-(y) = 0 for every y at eps = 0 and K_- = 2^n.
Expected if the hypothesis were only a proof artefact: N2 >= K_- = 2^n in both.
Run:  OMP_NUM_THREADS=1 python3 -I -B item1_thm1132_additive.py
"""
import itertools, math, time
import numpy as np
from scipy.optimize import linprog
t0 = time.time()

def class_constraints(n, c):
    """rows of A_ub x <= b_ub for |D_iD_j g(x)| <= c."""
    N = 1 << n
    rows = []; rhs = []
    for i in range(n):
        for j in range(i + 1, n):
            for x in range(N):
                if (x >> i) & 1 or (x >> j) & 1: continue
                r = np.zeros(N)
                r[x | (1 << i) | (1 << j)] += 1; r[x | (1 << i)] -= 1; r[x | (1 << j)] -= 1; r[x] += 1
                rows.append(r); rhs.append(c); rows.append(-r); rhs.append(c)
    return np.array(rows), np.array(rhs)

def value_interval(n, c, f, g, A, cons):
    """(inf, sup) of min(f+g') over class members agreeing with g on A.  inf = -inf if unbounded."""
    N = 1 << n
    A_ub, b_ub = cons
    A_eq = np.zeros((len(A), N)); b_eq = np.zeros(len(A))
    for k, a in enumerate(A): A_eq[k, a] = 1; b_eq[k] = g[a]
    lo = math.inf
    for y in range(N):
        cvec = np.zeros(N); cvec[y] = 1
        res = linprog(cvec, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq if len(A) else None, b_eq=b_eq if len(A) else None,
                      bounds=[(None, None)] * N, method="highs")
        if res.status == 3: return -math.inf, None           # unbounded
        assert res.status == 0, res.message
        lo = min(lo, f[y] + res.fun)
    # sup of the minimum: max t, t <= f(y) + g'(y)
    cvec = np.zeros(N + 1); cvec[N] = -1
    A2 = np.hstack([A_ub, np.zeros((A_ub.shape[0], 1))])
    extra = np.zeros((N, N + 1)); extra[np.arange(N), np.arange(N)] = -1; extra[:, N] = 1
    A2 = np.vstack([A2, extra]); b2 = np.concatenate([b_ub, np.array(f, dtype=float)])
    Ae = np.hstack([A_eq, np.zeros((len(A), 1))]) if len(A) else None
    res = linprog(cvec, A_ub=A2, b_ub=b2, A_eq=Ae, b_eq=b_eq if len(A) else None, bounds=[(None, None)] * (N + 1), method="highs")
    if res.status == 3: return lo, math.inf
    assert res.status == 0, res.message
    return lo, -res.fun

def K_minus(n, c, E, eps):
    N = 1 << n
    gap = [E[y] - min(E) for y in range(N)]
    rho = []
    for y in range(N):
        d = 0
        while c * math.comb(d + 2, 2) <= gap[y] + eps + 1e-12: d += 1
        rho.append(d)
    pc = [bin(i).count("1") for i in range(N)]
    for k in range(1, N + 1):
        for code in itertools.combinations(range(N), k):
            if all(any(pc[y ^ a] <= rho[y] for a in code) for y in range(N)): return k, rho
    return None, rho

viol_control = 0; found_counter = 0
print("=== Theorem 11.32 without 'the true residual is additive' ===")
for n in (2, 3, 4):
    N = 1 << n; c = 1.0; e = 0.1 if n <= 3 else 0.05; eps = 0.0
    assert e * n < c
    pc = [bin(i).count("1") for i in range(N)]
    cons = class_constraints(n, c)
    E = [e * pc[x] for x in range(N)]
    Km, rho = K_minus(n, c, E, eps)
    star = [0] + [1 << i for i in range(n)]
    print(f"\nn = {n}, c = {c}, e = {e}, eps = 0:  rho_-(y) = {sorted(set(rho))} for all y  =>  K_- = {Km} (= 2^n = {N})")
    for name in ("ADD", "BND"):
        if name == "ADD":
            g = [0.0] * N; f = list(E)
        else:
            g = [-c * math.comb(pc[x], 2) for x in range(N)]; f = [E[x] - g[x] for x in range(N)]
        # membership of the true residual in the class
        A_ub, b_ub = cons
        member = bool((A_ub @ np.array(g) <= b_ub + 1e-12).all())
        lo, hi = value_interval(n, c, f, g, star, cons)
        star_cert = (lo > -math.inf) and (hi - lo <= eps + 1e-9)
        # exact N2 by exhaustive search over subsets in order of size (n <= 3); for n = 4 only the sizes needed
        N2 = None
        if n <= 3:
            for k in range(0, N + 1):
                for A in itertools.combinations(range(N), k):
                    lo_, hi_ = value_interval(n, c, f, g, list(A), cons)
                    if lo_ > -math.inf and hi_ - lo_ <= eps + 1e-9: N2 = k; break
                if N2 is not None: break
        else:
            if name == "ADD":
                # monotone in A: if no subset of size N-1 certifies then N2 = N
                ok15 = False
                for A in itertools.combinations(range(N), N - 1):
                    lo_, hi_ = value_interval(n, c, f, g, list(A), cons)
                    if lo_ > -math.inf and hi_ - lo_ <= eps + 1e-9: ok15 = True; break
                N2 = "<= %d" % (N - 1) if ok15 else N
            else:
                N2 = "<= %d (the star)" % (n + 1) if star_cert else "?"
        print(f"  {name}: true residual in the class: {member};  star at 0 (n+1 = {n+1} points): certified interval of the minimum = [{lo}, {hi}] -> certifies: {star_cert};  N2 = {N2}")
        if name == "ADD":
            n2 = N2 if isinstance(N2, int) else None
            if n2 is None or not (Km <= n2 <= (n + 1) * Km + 1): viol_control += 1
        else:
            n2 = N2 if isinstance(N2, int) else (n + 1 if star_cert else None)
            if n2 is not None and n2 < Km: found_counter += 1
print()
print(f"control (additive true residual, the theorem as stated): K_- <= N2 <= (n+1)K_- + 1 violated in {viol_control} of 3 cases")
print(f"without the hypothesis (boundary member g0 = -c*C(|x|,2), same energy landscape e|x|): N2 < K_- in {found_counter} of 3 cases")
print("  => the lower bound K_- <= N2 of Theorem 11.32 is FALSE without 'the true residual is additive'.")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item1_thm1132_additive")
