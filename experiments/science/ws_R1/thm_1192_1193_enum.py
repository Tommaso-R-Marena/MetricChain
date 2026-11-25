#!/usr/bin/env python3
"""R1: Theorem 11.92 (a), (b) and Lemma 11.93 (i), (ii) by exact enumeration on small cubes (own code).
 (a) for a u-Lipschitz psi: t -> ln A_t is u-Lipschitz; d_t >= J_t - V_n(t), equality at the flat-histogram instance;
 (b) optimistic refinement with brackets placed at random AND adversarially (valid, of the prescribed widths):
     output valid, width <= x_m + ln(n+1), a class is refined from width x_{l-1} only if d_t <= x_{l-1},
     number of refinements <= sum_t #{l >= 1 : x_{l-1} >= d_t};
 Lemma 11.93: A_k = sum_j H(j) A_{k;j}(O) for every O; E_O A_{k;j}(O) = A_k for every j; Markov/Hoeffding statement."""
import itertools, math
import numpy as np
from math import comb
rng = np.random.default_rng(1192)

def cube(n):
    X = np.arange(2 ** n)
    w = np.array([bin(x).count("1") for x in X])
    D = np.array([[bin(x ^ y).count("1") for y in X] for x in X])
    return X, w, D

def random_lipschitz(n, D, u):
    g = rng.normal(0, rng.choice([0.5, 2.0, 6.0]), 2 ** n)
    return np.min(g[None, :] + u * D, axis=1)          # inf-convolution: u-Lipschitz

ok = True
# ---------------- (a) ----------------
worst_lip = -math.inf; worst_def = math.inf; eqH = 0.0
for n in (6, 8):
    X, w, D = cube(n)
    for trial in range(60):
        u = float(rng.choice([0.3, 1.0, 2.5]))
        psi = random_lipschitz(n, D, u)
        assert np.max(np.abs(psi[:, None] - psi[None, :]) - u * D) < 1e-12
        p = rng.dirichlet(np.ones(n + 1) * rng.choice([0.3, 1.0, 5.0]))          # exchangeable: weights of the type classes
        J = -np.log(p)
        A = np.array([np.mean(np.exp(-psi[w == t])) for t in range(n + 1)])
        worst_lip = max(worst_lip, np.max(np.abs(np.diff(np.log(A)))) - u)
        V = np.array([np.min(J + u * np.abs(np.arange(n + 1) - t)) for t in range(n + 1)])
        d = np.log(np.max(p * A)) - np.log(p * A)
        worst_def = min(worst_def, np.min(d - (J - V)))
        # flat-histogram instance psi_H = -V(|x|)
        AH = np.exp(V)
        dH = np.log(np.max(p * AH)) - np.log(p * AH)
        eqH = max(eqH, np.max(np.abs(dH - (J - V))))
print(f"(a) max over cases of [max_t |ln A_(t+1) - ln A_t| - u] = {worst_lip:.2e} (<= 0);  min[d_t - (J_t - V_n(t))] = {worst_def:.2e} (>= 0);  "
      f"equality at the flat-histogram instance: {eqH:.1e}")
ok &= worst_lip <= 1e-12 and worst_def >= -1e-12 and eqH < 1e-12

# ---------------- (b) ----------------
def refine_run(p, A, ladder, mode):
    n1 = len(p)
    def oracle(t, l):
        x = ladder[l]
        th = {"random": rng.uniform(0, 1), "low": 0.0, "high": 1.0, "alt": float((t + l) % 2)}[mode]
        L = A[t] * math.exp(-th * x); U = L * math.exp(x)
        return L, U
    rung = [0] * n1
    Ls = np.zeros(n1); Us = np.full(n1, np.inf)
    for t in range(n1):
        L, U = oracle(t, 0); Ls[t], Us[t] = L, U
    log = []
    while True:
        k = int(np.argmax(p * Us))
        if rung[k] == len(ladder) - 1:
            return (np.max(p * Ls), n1 * p[k] * Us[k]), log, k
        log.append((k, rung[k]))
        rung[k] += 1
        L, U = oracle(k, rung[k])
        Ls[k], Us[k] = max(Ls[k], L), min(Us[k], U)

viol = 0; runs = 0; max_excess_width = -math.inf; cost_ok = True
for n in (8, 12, 20):
    for trial in range(300):
        p = rng.dirichlet(np.ones(n + 1) * rng.choice([0.3, 1.0, 5.0]))
        A = np.exp(rng.normal(0, 2.0, n + 1))                      # any positive class means (the statement is deterministic)
        m = int(rng.integers(2, 7))
        ladder = np.sort(rng.uniform(0.05, 6.0, m + 1))[::-1]
        d = np.log(np.max(p * A)) - np.log(p * A)
        for mode in ("random", "low", "high", "alt"):
            (lo, hi), log, k = refine_run(p, A, ladder, mode)
            Atot = float(np.sum(p * A)); runs += 1
            if not (lo <= Atot * (1 + 1e-12) and Atot <= hi * (1 + 1e-12)): viol += 1
            max_excess_width = max(max_excess_width, math.log(hi / lo) - (ladder[-1] + math.log(n + 1)))
            for (t, l_from) in log:
                if d[t] > ladder[l_from] + 1e-12: viol += 1
            bound = sum(1 for t in range(n + 1) for l in range(1, m + 1) if ladder[l - 1] >= d[t] - 1e-12)
            cost_ok &= (len(log) <= bound)
print(f"(b) {runs} runs of optimistic refinement (4 bracket placements): violations of validity or of 'refined only if d_t <= x_(l-1)': {viol}; "
      f"max[width - (x_m + ln(n+1))] = {max_excess_width:.2e} (<= 0); number of refinements <= sum_t #{{l: x_(l-1) >= d_t}}: {cost_ok}")
ok &= viol == 0 and max_excess_width <= 1e-12 and cost_ok

# ---------------- Lemma 11.93 ----------------
n, k, no = 10, 4, 5
X, w, D = cube(n)
u = 1.0
e1 = e2 = 0.0; markov_ok = True
for trial in range(4):
    psi = random_lipschitz(n, D, u)
    wt = np.exp(-psi)
    Tk = X[w == k]
    Ak = float(np.mean(wt[Tk]))
    js = [j for j in range(0, no + 1) if 0 <= k - j <= n - no]
    H = {j: comb(no, j) * comb(n - no, k - j) / comb(n, k) for j in js}
    acc = {j: [] for j in js}
    for O in itertools.combinations(range(n), no):
        mask = sum(1 << i for i in O)
        inO = np.array([bin(x & mask).count("1") for x in Tk])
        tot = 0.0
        for j in js:
            sel = Tk[inO == j]
            Akj = float(np.mean(wt[sel]))
            acc[j].append(Akj)
            tot += H[j] * Akj
        e1 = max(e1, abs(tot - Ak) / Ak)
    for j in js:
        e2 = max(e2, abs(np.mean(acc[j]) - Ak) / Ak)
    # Markov statement for S = {j = 2} (complement {0,1,3,4}), delta'' = 0.25
    S = [2]; dl = 0.25; HSc = sum(H[j] for j in js if j not in S)
    cnt = 0; total = 0
    for idx in range(len(acc[js[0]])):
        val = sum(H[j] * acc[j][idx] for j in js if j not in S)
        cnt += (val <= HSc / dl * Ak); total += 1
    markov_ok &= (cnt / total >= 1 - dl)
print(f"Lemma 11.93 (n={n}, k={k}, n_o={no}, all {comb(n, no)} sets O, 4 random Lipschitz psi): (i) |sum_j H(j)A_(k;j)(O) - A_k|/A_k <= {e1:.1e} for every O; "
      f"(ii) |E_O A_(k;j)(O) - A_k|/A_k <= {e2:.1e} for every j; Markov statement holds: {markov_ok}")
ok &= e1 < 1e-12 and e2 < 1e-12 and markov_ok
# Hoeffding step: H(S^c) <= delta''/2 for S = {|j - n_o k/n| <= sqrt(n ln(4/delta'')/2)}
hoeff_ok = True
for (n_, k_, no_) in ((200, 80, 100), (1000, 300, 400), (5000, 2500, 1000)):
    for dl in (0.5, 0.1, 0.01):
        r = math.sqrt(n_ * math.log(4 / dl) / 2)
        from scipy.stats import hypergeom
        rv = hypergeom(n_, k_, no_)
        mean = no_ * k_ / n_
        tail = rv.cdf(math.ceil(mean - r) - 1) + rv.sf(math.floor(mean + r))
        hoeff_ok &= (tail <= dl / 2)
print(f"Lemma 11.93 (ii), last sentence: hypergeometric mass outside the window <= delta''/2 in 9 cases: {hoeff_ok}")
ok &= hoeff_ok
print("SUMMARY:", "ALL PASS" if ok else "FAILURES")
