#!/usr/bin/env python3
"""R23 Item 1 — the two sampled {F} counterexamples rebuilt with own code (chosen by the pre-registered
shuffle: AA2 l.1357 (Entry 72) and AA2 l.1114 (Entry 57)), plus two one-screen checks of sampled {F} tags
whose named evidence is an argument (AA1 l.743, AA2 l.606) and the hand computation behind AA1 l.1110.

R1  AA2 l.1357, Theorem 11.115(d): "two boxes contain the two ends of a single-site move iff both are
    non-empty and at most one site has disjoint domains"; tag {F} for the non-emptiness clause
    (Lean: sep_card_le_one_not_sufficient).  Rebuild: ALL pairs of boxes (site domains = arbitrary subsets
    of the alphabet, empty ones included) for (n,k) in {(1,2),(2,1),(2,2),(2,3),(3,2)}: truth by enumeration of
    configurations, criterion with and without the clause.
R2  AA2 l.1114, Proposition 11.103(d): for three letters with the Hamming envelope the uniform site law is
    not the hardest: threshold E = 0.119499 (uniform) against 0.120196 for pi = (0.05, 0.5, 0.45) at u = 1.
    Own formula (derived in NOTES.md from Theorem 11.99 / the remark (f) of the report):
        E(pi) = lim_{t->0} F*(t)/t = min_Q max_phi KL(Q || pi_phi),   pi_phi ~ pi * exp(-phi),
    phi over the vertices of the Lipschitz polytope of the site; for the Hamming envelope with slope u these
    are u*1_A, A a nonempty proper subset of the letters.  Primal: any Q gives an upper bound.  Dual: any
    weights w on the vertices give the lower bound  -ln sum_x prod_A pi_A(x)^{w_A}.  The two are closed to 1e-9.
    Controls: two letters -> E(1/2) = ln cosh(u/2) and the uniform law is the hardest on a grid of fields;
    three letters uniform -> the closed form Psi_3(u) = ln((e^u+2)/3) - u/3 of the report.
R3  AA1 l.743, Theorem 11.14: "ln E_mu e^{beta(g-E_mu g)} <= beta*sum gamma d - KL(nu||mu) for any coupling"
    needs beta >= 0: two-point example.
R4  AA2 l.606, Lemma 11.62 at q = 1 (D = X allowed): constant hat-w.
R5  AA1 l.1110 (D38): flat k-state site, the two numbers 0.02841 (single dips) and 0.02914 (boxes of pairs)
    at k = 4, u = 1, eps1 = 0 from the displayed formula of Theorem 11.27.
Run:  OMP_NUM_THREADS=1 python3 -I -B item1_rebuild_F_two.py
"""
import itertools, math, time
import numpy as np
from scipy.optimize import minimize
t0 = time.time()
viol = 0
def report(name, n, extra=""):
    global viol; viol += n
    print(f"{name}: violations = {n} {extra}")

# ------------------------------------------------------------------ R1
print("=== R1: adjacency of boxes (Theorem 11.115(d)) ===")
def r1(n, k):
    letters = range(k)
    subsets = [frozenset(s) for r in range(k + 1) for s in itertools.combinations(letters, r)]
    boxes = list(itertools.product(subsets, repeat=n))
    bad_with = bad_without = 0; npairs = 0; first = None
    for D in boxes:
        confD = list(itertools.product(*[sorted(s) for s in D]))
        for Dp in boxes:
            confDp = list(itertools.product(*[sorted(s) for s in Dp]))
            truth = any(sum(a != b for a, b in zip(x, y)) <= 1 for x in confD for y in confDp)
            sep = sum(1 for i in range(n) if not (D[i] & Dp[i]))
            nonempty = all(len(s) > 0 for s in D) and all(len(s) > 0 for s in Dp)
            crit_with = nonempty and sep <= 1
            crit_without = sep <= 1
            npairs += 1
            bad_with += (crit_with != truth)
            if crit_without != truth:
                bad_without += 1
                if first is None: first = (D, Dp)
    return npairs, bad_with, bad_without, first
tot_with = 0; tot_without = 0
for (n, k) in ((1, 2), (2, 1), (2, 2), (2, 3), (3, 2)):
    npairs, bw, bwo, first = r1(n, k)
    tot_with += bw; tot_without += bwo
    ex = "" if first is None else "  e.g. " + " x ".join("{" + ",".join(map(str, sorted(s))) + "}" for s in first[0]) + "  vs  " + " x ".join("{" + ",".join(map(str, sorted(s))) + "}" for s in first[1])
    print(f"  n={n} k={k}: pairs of boxes {npairs}; criterion WITH non-emptiness wrong in {bw}; WITHOUT it wrong in {bwo}{ex}")
report("R1a the criterion with the non-emptiness clause is exact (all pairs)", tot_with)
report("R1b the criterion without the clause fails somewhere (violation = it never fails)", int(tot_without == 0), f"(failures: {tot_without})")
# the Lean example itself: n = 2, k = 1, boxes  {} x {0}  and  {0} x {0}
D = (frozenset(), frozenset({0})); Dp = (frozenset({0}), frozenset({0}))
sep = sum(1 for i in range(2) if not (D[i] & Dp[i]))
print(f"  the Lean example ({{}} x {{0}} against {{0}} x {{0}}): separating sites = {sep} (<= 1), first box empty -> no move: counterexample confirmed = {sep <= 1}")

# ------------------------------------------------------------------ R2
print("=== R2: three letters, Hamming envelope: is the uniform site law the hardest? (threshold E) ===")
def vertices_hamming(q, u):
    vs = []
    for r in range(1, q):
        for A in itertools.combinations(range(q), r):
            v = np.zeros(q); v[list(A)] = u; vs.append(v)
    return vs
def tilted(pi, phi):
    w = pi * np.exp(-phi); return w / w.sum()
def E_site(pi, u):
    """returns (primal upper bound, dual lower bound) of min_Q max_phi KL(Q || pi_phi)."""
    q = len(pi); V = vertices_hamming(q, u); P = np.array([tilted(pi, v) for v in V])   # (m, q)
    m = len(V)
    def primal_val(Q):
        Q = np.clip(Q, 1e-300, None); Q = Q / Q.sum()
        return max(float(np.sum(Q * (np.log(Q) - np.log(P[a])))) for a in range(m))
    def dual_val(w):
        w = np.clip(w, 0, None); w = w / w.sum()
        return -math.log(float(np.sum(np.exp(w @ np.log(P)))))
    # dual maximisation (concave in w): softmax parametrisation, several starts
    best_d = -1; best_w = None
    rng = np.random.default_rng(0)
    starts = [np.zeros(m)] + [rng.normal(size=m) for _ in range(12)]
    for s in starts:
        res = minimize(lambda z: -dual_val(np.exp(z - z.max())), s, method="Nelder-Mead",
                       options={"xatol": 1e-13, "fatol": 1e-15, "maxiter": 40000, "maxfev": 40000})
        if -res.fun > best_d: best_d = -res.fun; best_w = np.exp(res.x - res.x.max()); best_w /= best_w.sum()
    # primal point from the dual: Q ~ prod_A pi_A^{w_A}
    Q = np.exp(best_w @ np.log(P)); Q /= Q.sum()
    res = minimize(lambda z: primal_val(np.exp(z - z.max())), np.log(Q), method="Nelder-Mead",
                   options={"xatol": 1e-13, "fatol": 1e-15, "maxiter": 40000, "maxfev": 40000})
    best_p = min(primal_val(Q), res.fun)
    return best_p, best_d
u = 1.0
up_u, lo_u = E_site(np.array([1/3, 1/3, 1/3]), u)
up_f, lo_f = E_site(np.array([0.05, 0.5, 0.45]), u)
psi3 = math.log((math.e ** u + 2) / 3) - u / 3
print(f"  three letters, u = 1, uniform law      : E in [{lo_u:.9f}, {up_u:.9f}]   closed form Psi_3(1) = {psi3:.9f}   (report: 0.119499)")
print(f"  three letters, u = 1, pi=(0.05,0.5,0.45): E in [{lo_f:.9f}, {up_f:.9f}]   (report: 0.120196)")
print(f"  two-letter cube, u = 1                  : ln cosh(1/2) = {math.log(math.cosh(0.5)):.9f}   (report: 0.120115)")
report("R2a duality gaps below 1e-8", int(up_u - lo_u > 1e-8) + int(up_f - lo_f > 1e-8))
report("R2b the uniform value equals the closed form to 1e-8", int(abs(lo_u - psi3) > 1e-8))
report("R2c the counterexample: certified LOWER bound for (0.05,0.5,0.45) exceeds certified UPPER bound for uniform (violation = it does not)", int(not (lo_f > up_u)),
       f"({lo_f:.6f} > {up_u:.6f}; report 0.120196 > 0.119499)")
report("R2d the report's two numbers reproduced to 6 decimals", int(abs(lo_f - 0.120196) > 1.5e-6) + int(abs(lo_u - 0.119499) > 1.5e-6))
# control: two letters, the uniform law is the hardest
bad2 = 0; e_half = None
for p in [0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05, 0.6, 0.7, 0.9]:
    upp, low = E_site(np.array([1 - p, p]), u)
    if p == 0.5: e_half = (upp, low)
    elif low > e_half[1] + 1e-9: bad2 += 1
print(f"  control, two letters u = 1: E(1/2) in [{e_half[1]:.9f}, {e_half[0]:.9f}] against ln cosh(1/2) = {math.log(math.cosh(0.5)):.9f}")
report("R2e control: for two letters no field makes E larger than at p = 1/2 (9 fields)", bad2 + int(abs(e_half[1] - math.log(math.cosh(0.5))) > 1e-8))
# how widespread: grid of three-letter laws at u = 1
cnt = 0; tot = 0; mx = (0, None)
for i in range(1, 20):
    for j in range(1, 20 - i):
        pi = np.array([i / 20, j / 20, 1 - (i + j) / 20]); tot += 1
        upp, low = E_site(pi, u)
        if low > up_u + 1e-9: cnt += 1
        if low > mx[0]: mx = (low, pi)
print(f"  grid of {tot} three-letter laws (mesh 0.05) at u = 1: {cnt} have a certified E above the uniform law's; largest {mx[0]:.6f} at {mx[1]}")

# ------------------------------------------------------------------ R3
print("=== R3: Theorem 11.14 with beta < 0 (AA1 l.743) ===")
mu = np.array([0.5, 0.5]); g = np.array([0.0, 0.0]); d = np.array([[0, 1.0], [1.0, 0]]); beta = -1.0
nu = mu * np.exp(beta * g); nu /= nu.sum()
lhs = math.log(float(np.sum(mu * np.exp(beta * (g - mu @ g)))))
gamma = np.outer(nu, mu)                                   # the product coupling of (nu, mu)
rhs = beta * float(np.sum(gamma * d)) - float(np.sum(nu * np.log(nu / mu)))
print(f"  two points, d = 1, g = 0, beta = -1, product coupling: lhs = {lhs:.3f}, rhs = {rhs:.3f}  ->  lhs <= rhs is {lhs <= rhs}")
report("R3 the inequality fails for beta < 0 (violation = it holds)", int(lhs <= rhs))
beta = 1.0; rhs = beta * float(np.sum(gamma * d)); report("R3 control beta = +1: inequality holds", int(not (lhs <= rhs)))

# ------------------------------------------------------------------ R4
print("=== R4: Lemma 11.62 at q = 1 (AA2 l.606) ===")
n = 3; N = 1 << n; uu = 1.0
pcn = [bin(i).count("1") for i in range(N)]
mu0 = np.full(N, 1.0 / N)                                   # reference psi0 = 0, uniform cube, slack = u*Hamming
def Xi(q):
    best = 0.0
    for mask in range(1, (1 << N) - 1):                     # D proper nonempty
        Dset = [x for x in range(N) if (mask >> x) & 1]
        if sum(mu0[x] for x in Dset) > q + 1e-12: continue
        comp = [y for y in range(N) if not (mask >> y) & 1]
        val = sum(mu0[x] * (math.exp(uu * min(pcn[x ^ y] for y in comp)) - 1) for x in Dset)
        best = max(best, val)
    return best
xi_max = Xi(1.0)                                            # the largest value the lemma can ever give (D proper)
C = 2.0 * (1 + xi_max) + 1; t = 1.0
what = np.full(N, C)                                        # hat-w = C: psi = psi0 - ln C, a member of the class
lhs = float(np.sum(mu0 * np.maximum(what - t, 0)))
print(f"  Q_3, u = 1: sup over proper D of the tail functional = {xi_max:.4f}; constant hat-w = {C:.4f}, t = 1: E(hat-w - t)_+ = {lhs:.4f} > t*Xi = {xi_max:.4f}")
report("R4 with mu0(hat-w > t) = 1 the bound E(hat-w - t)_+ <= t*Xi fails (violation = it holds)", int(lhs <= t * xi_max))

# ------------------------------------------------------------------ R5
print("=== R5: flat 4-state site, u = 1, eps1 = 0 (Theorem 11.27, D38; AA1 l.1110) ===")
def Dbin(a, b): return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
k = 4; vals = {}
for m in range(1, k):
    rho = -math.log(m / k + (1 - m / k) * math.exp(-1.0)) / 1.0
    vals[m] = max(Dbin(rho, 1 - m / k), 0.0) if 0 < rho < 1 else 0.0
print("  D(rho_m || 1 - m/k) for m = 1,2,3:", {m: round(v, 5) for m, v in vals.items()}, " (report: single dips m=1: 0.02841; boxes of pairs m=2: 0.02914)")
report("R5 the two numbers of the report reproduced", int(abs(vals[1] - 0.02841) > 6e-6) + int(abs(vals[2] - 0.02914) > 6e-6) + int(not vals[2] > vals[1]))

print(f"TOTAL violations: {viol}")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item1_rebuild_F_two")
