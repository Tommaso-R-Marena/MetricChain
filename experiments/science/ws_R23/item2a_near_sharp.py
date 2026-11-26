#!/usr/bin/env python3
"""R23 Item 2(a) — own code, written before opening the audit's script aa1_03.

Claim checked (synthesis §6, first bullet; AA1 §0 item 4): two-state sites, zero residual, known part
f(x) = sum_i e_i x_i, weighted Hamming envelope d(x,y) = sum_i c_i [x_i != y_i]; if every margin
c_i/e_i - 1 lies in (0, 1/n) then every site is non-sharp (c_i > e_i) and the smallest exact point
certificate has exactly n + 1 points.

Definitions used (theory report l.1795-1821, zero residual g = 0, eps = 0):
  UB(A) = min_{a in A} f(a),  L_A(y) = max_{a in A} ( g(a) - d(a,y) ) = - min_a d(a,y),
  LB(A) = min_y ( f(y) + L_A(y) ),   A is an exact point certificate  iff  UB(A) - LB(A) <= 0.
Cover reformulation (Theorem 11.4): A is a certificate iff x* in A and every y has a in A with d(a,y) <= gap(y).

Checks (all exact integer arithmetic: energies are integers):
  T1  direct definition: A0 = {0, e_1..e_n} is an exact certificate                      (n <= NMAX)
  T2  forced points: each point of A0 is covered by no other centre (exhaustive over all 2^n centres),
      hence every certificate contains A0 and N = n + 1                                  (n <= NMAX)
  T3  brute force over ALL subsets of size <= n with the direct definition: none certifies   (n <= 4)
  T4  exact minimum set cover by integer programming (HiGHS) = n + 1                        (n <= 10)
  T5  heterogeneous sites (random integer e_i, margins in (0,1/n)): T1, T2 and the fooling-set
      property (no centre covers two points of A0); ILP for n <= 8
Controls (must behave differently):
  C1  sharp sites (c_i <= e_i): the single evaluation {0} certifies (UB-LB = 0)
  C2  homogeneous margin just above 1/(n-1): A0 is NOT a certificate and min cover >= n + 2
  C3  margin 1 (c = 2e), the report's example: min cover grows like >= (6/5)^n (machine-checked bound of the report)
  C4  negative control for T2/T3 code: a deliberately wrong claim "A0 minus one unit vector certifies" must fail.
Every test prints its number of violations.
Run:  OMP_NUM_THREADS=1 python3 -I -B item2a_near_sharp.py
"""
import itertools, math, sys, time, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix

NMAX = 12
t0 = time.time()
viol_total = 0
def report(name, nviol, extra=""):
    global viol_total
    viol_total += nviol
    print(f"{name}: violations = {nviol} {extra}")

def popcount_table(n):
    return np.array([bin(i).count("1") for i in range(1 << n)], dtype=np.int64)

def energies(n, e):
    """f(x) = sum_i e_i x_i for all x (bit i of the index is x_i)."""
    f = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        f[(np.arange(1 << n) >> i) & 1 == 1] += e[i]
    return f

def dist_matrix_rows(n, c, centres):
    """d(a, y) for a in centres (list of ints) and all y: array (len(centres), 2^n), integer."""
    ys = np.arange(1 << n)
    D = np.zeros((len(centres), 1 << n), dtype=np.int64)
    for i in range(n):
        yi = (ys >> i) & 1
        for r, a in enumerate(centres):
            ai = (a >> i) & 1
            D[r] += c[i] * (yi != ai)
    return D

def is_certificate_direct(n, e, c, A, f=None):
    """Direct definition: UB(A) - LB(A) <= 0 at the zero residual."""
    if f is None: f = energies(n, e)
    D = dist_matrix_rows(n, c, list(A))
    LB = int((f - D.min(axis=0)).min())
    UB = int(f[list(A)].min())
    return UB - LB <= 0, UB - LB

def cover_matrix(n, e, c):
    """M[a, y] = True iff d(a,y) <= gap(y) (zero residual, eps = 0)."""
    f = energies(n, e)
    gap = f - f.min()
    N = 1 << n
    M = np.zeros((N, N), dtype=bool)
    ys = np.arange(N)
    for a in range(N):
        d = np.zeros(N, dtype=np.int64)
        x = ys ^ a
        for i in range(n):
            d += c[i] * ((x >> i) & 1)
        M[a] = d <= gap
    return M

def min_cover_ilp(M, time_limit=120):
    N = M.shape[0]
    A = csr_matrix(M.T.astype(np.float64))      # row y: centres that cover y
    res = milp(c=np.ones(N), constraints=LinearConstraint(A, lb=np.ones(N), ub=np.inf),
               integrality=np.ones(N), bounds=Bounds(0, 1), options={"time_limit": time_limit})
    return res

print("=== R23 item 2(a): near-sharp two-state sites, zero residual ===")
print("homogeneous family: e_i = 10 n, c_i = 10 n + 9  (margin 0.9/n < 1/n), integers")
A0 = lambda n: [0] + [1 << i for i in range(n)]

# ---- T1, T2 (n <= NMAX), T4 (n <= 10)
v1 = v2 = v4 = 0
for n in range(1, NMAX + 1):
    e = [10 * n] * n; c = [10 * n + 9] * n
    assert all(ci > ei for ci, ei in zip(c, e))          # every site non-sharp
    ok, gapcert = is_certificate_direct(n, e, c, A0(n))
    v1 += (not ok)
    # forced points: which centres a cover y, for y in A0 ?
    f = energies(n, e); gap = f - f.min()
    forced_bad = 0
    for y in A0(n):
        ys = np.arange(1 << n) ^ y                      # a xor y for all a
        d = np.zeros(1 << n, dtype=np.int64)
        for i in range(n): d += c[i] * ((ys >> i) & 1)
        coverers = np.nonzero(d <= gap[y])[0]
        if list(coverers) != [y]: forced_bad += 1
    v2 += forced_bad
    line = f"  n={n:2d}: A0 certifies (UB-LB={gapcert}) ; points of A0 covered only by themselves: {forced_bad==0}"
    if n <= 10:
        M = cover_matrix(n, e, c)
        res = min_cover_ilp(M)
        Nmin = int(round(res.fun)) if res.success else None
        v4 += (Nmin != n + 1)
        line += f" ; ILP min cover = {Nmin} (status {res.status})"
    print(line)
report("T1 A0={0,e_i} is an exact certificate by the direct definition, n=1..12", v1)
report("T2 each point of A0 is covered by no other centre (exhaustive over 2^n centres), n=1..12", v2)
report("T4 ILP exact minimum cover equals n+1, n=1..10", v4)

# ---- T3 brute force over all subsets of size <= n (direct definition), n <= 4
v3 = 0
for n in range(1, 5):
    e = [10 * n] * n; c = [10 * n + 9] * n
    f = energies(n, e)
    N = 1 << n
    Dall = dist_matrix_rows(n, c, list(range(N)))
    small = 0; found_small = 0; cnt_np1 = 0
    for k in range(1, n + 2):
        for A in itertools.combinations(range(N), k):
            LB = int((f - Dall[list(A)].min(axis=0)).min()); UB = int(f[list(A)].min())
            cert = (UB - LB <= 0)
            if k <= n:
                small += 1; found_small += cert
            elif cert:
                cnt_np1 += 1
    v3 += found_small + (cnt_np1 != 1)
    print(f"  n={n}: subsets of size <= n tested: {small}, certificates among them: {found_small}; certificates of size n+1: {cnt_np1} (expected exactly 1, namely A0)")
report("T3 no subset of size <= n certifies; exactly one of size n+1 (all subsets, direct definition), n=1..4", v3)

# ---- T5 heterogeneous
rng = random.Random(20261126)
v5a = v5b = v5c = v5d = 0; ninst = 0
for n in range(2, 11):
    for rep in range(20):
        # integer energies; margins strictly inside (0, 1/n): c_i = e_i + m_i with 0 < m_i < e_i/n
        e = [rng.randrange(n + 1, 60 * n) for _ in range(n)]
        c = [ei + rng.randrange(1, (ei - 1) // n + 1) for ei in e]
        assert all(ei < ci and (ci - ei) * n < ei for ei, ci in zip(e, c))
        ninst += 1
        ok, _ = is_certificate_direct(n, e, c, A0(n)); v5a += (not ok)
        f = energies(n, e); gap = f - f.min()
        # fooling set: no centre covers two points of A0
        cov_count = np.zeros(1 << n, dtype=np.int64)
        for y in A0(n):
            ys = np.arange(1 << n) ^ y
            d = np.zeros(1 << n, dtype=np.int64)
            for i in range(n): d += c[i] * ((ys >> i) & 1)
            cov_count += (d <= gap[y])
        v5b += int((cov_count > 1).any())
        if n <= 8 and rep < 6:
            res = min_cover_ilp(cover_matrix(n, e, c)); Nmin = int(round(res.fun)) if res.success else None
            v5c += (Nmin != n + 1)
report(f"T5a heterogeneous (random integer e_i, margins in (0,1/n)), {ninst} instances n=2..10: A0 certifies", v5a)
report("T5b same instances: {0,e_1..e_n} is a fooling set (no centre covers two of them) => N >= n+1", v5b)
report("T5c ILP exact minimum cover = n+1 (n=2..8, 6 instances each)", v5c)
# fooling set for arbitrary non-sharp margins (not small): N >= n+1 always
v5d = 0; ninst2 = 0
for n in range(2, 11):
    for rep in range(20):
        e = [rng.randrange(1, 50) for _ in range(n)]
        c = [ei + rng.randrange(1, 100) for ei in e]            # any margin > 0
        ninst2 += 1
        f = energies(n, e); gap = f - f.min()
        cov_count = np.zeros(1 << n, dtype=np.int64)
        for y in A0(n):
            ys = np.arange(1 << n) ^ y
            d = np.zeros(1 << n, dtype=np.int64)
            for i in range(n): d += c[i] * ((ys >> i) & 1)
            cov_count += (d <= gap[y])
        v5d += int((cov_count > 1).any())
report(f"T5d arbitrary non-sharp two-state sites ({ninst2} random instances, any margins): fooling set => N >= n+1", v5d)

# ---- Controls
print("--- controls ---")
vc1 = 0
for n in range(1, NMAX + 1):
    e = [10 * n] * n; c = [10 * n] * n                     # c = e: sharp
    ok, g_ = is_certificate_direct(n, e, c, [0]); vc1 += (not ok)
report("C1 sharp sites (c = e): the single evaluation {0} is an exact certificate, n=1..12", vc1)

vc2 = 0
for n in range(3, 11):
    # margin just above 1/(n-1):  e = 10(n-1), c = 10(n-1) + 11  -> margin 1.1/(n-1)
    e = [10 * (n - 1)] * n; c = [10 * (n - 1) + 11] * n
    ok, g_ = is_certificate_direct(n, e, c, A0(n))
    res = min_cover_ilp(cover_matrix(n, e, c)); Nmin = int(round(res.fun)) if res.success else None
    bad = ok or (Nmin is None) or (Nmin < n + 2)
    vc2 += bad
    print(f"  C2 n={n:2d} margin=1.1/(n-1): A0 certifies? {ok} (UB-LB={g_}); ILP min cover = {Nmin}")
report("C2 margin just above 1/(n-1): A0 fails and min cover >= n+2, n=3..10 (violation = control did not react)", vc2)
# exact boundary: margin = 1/(n-1) exactly  -> still n+1
vb = 0
for n in range(2, 11):
    e = [n - 1] * n; c = [n] * n                            # c/e - 1 = 1/(n-1)
    ok, g_ = is_certificate_direct(n, e, c, A0(n)); vb += (not ok)
report("B  boundary margin = 1/(n-1) exactly: A0 still certifies, n=2..10 (so '< 1/n' is sufficient, '<= 1/(n-1)' is the exact threshold)", vb)

vc3 = 0
print("  C3 margin 1 (e=1, c=2): ILP minimum cover vs the report's machine-checked lower bound (6/5)^n and the trivial 2^n")
for n in range(1, 9):
    e = [1] * n; c = [2] * n
    res = min_cover_ilp(cover_matrix(n, e, c), time_limit=300); Nmin = int(round(res.fun)) if res.success else None
    lb = (6 / 5) ** n
    bad = (Nmin is None) or (Nmin < lb - 1e-9)
    vc3 += bad
    print(f"     n={n}: min cover = {Nmin}  (6/5)^n = {lb:.3f}  n+1 = {n+1}  status {res.status}")
report("C3 margin 1: min cover >= (6/5)^n, n=1..8", vc3)

vc4 = 0
for n in range(2, 9):
    e = [10 * n] * n; c = [10 * n + 9] * n
    A = A0(n)[:-1]                                           # drop one unit vector: must NOT certify
    ok, g_ = is_certificate_direct(n, e, c, A)
    vc4 += ok
report("C4 negative control: A0 minus one unit vector does not certify, n=2..8 (violation = it certified)", vc4)

# ---- the linear vanishing of the exponent in the margin (synthesis §4 item 9: 'about 0.28 (c/e - 1)')
from scipy.optimize import minimize_scalar
def Rstar(rho):
    g = lambda x: -(math.log1p(x) - math.log1p(x ** (1 / rho)))
    r = minimize_scalar(g, bounds=(1e-9, 1 - 1e-9), method="bounded", options={"xatol": 1e-12})
    return -r.fun
print("--- exponent of a two-state site, R*(rho) = max_x [ln(1+x) - ln(1+x^(1/rho))], rho = e/c ---")
for m in (1.0, 0.1, 0.01, 0.001):
    print(f"  margin {m:6.3f}: R* = {Rstar(1/(1+m)):.6f}   R*/margin = {Rstar(1/(1+m))/m:.4f}")
print(f"  control rho=1/2: R* = {Rstar(0.5):.4f} (report: 0.1882)")
from scipy.special import lambertw
print(f"  limit of R*/margin as margin -> 0: W(1/e) = {lambertw(1/math.e).real:.5f}")

print(f"TOTAL violations (tests + controls that did not react): {viol_total}")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item2a_near_sharp")
