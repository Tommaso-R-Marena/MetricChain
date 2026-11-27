#!/usr/bin/env python3
"""Addendum A17, Proposition A17.8 -- coordinator's check script.

Reference: a Markov chain pi on S_1 x ... x S_n (a nearest-neighbour Gibbs measure), kernels P_k from x_k to x_{k+1},
Dobrushin coefficients theta_k = max_{a,a'} TV(P_k(a,.), P_k(a',.)).  Remainder r with one-site oscillations c_j.
With  C_i := sum_{j >= i} c_j prod_{k=i}^{j-1} theta_k :
    Var_pi(r) <= (1/4) sum_i C_i^2 ,     ln E exp(lam (r - E r)) <= lam^2 sum_i C_i^2 / 8   for every real lam,
hence  D_p(pi_g || pi) <= p^2 sum C_i^2 / (8 (p-1)),  D_2 <= sum C_i^2 / 2   (pi_g proportional to pi exp(-r)).
Checked by exact enumeration on random chains (n <= 9, alphabets 2-4) and random r (smooth, spiky, additive,
adversarial 'last-site' functions).  For theta = 1 (no mixing) C_i = sum_{j>=i} c_j; for a product measure C_i = c_i.
"""
import itertools, math, json
import numpy as np
rng = np.random.default_rng(424242)

def random_chain(n, sizes, coupling):
    init = rng.dirichlet(np.ones(sizes[0]))
    Ps = []
    for k in range(n - 1):
        logits = coupling * rng.normal(size=(sizes[k], sizes[k + 1]))
        P = np.exp(logits); P /= P.sum(1, keepdims=True)
        Ps.append(P)
    return init, Ps

def joint(init, Ps, sizes):
    states = list(itertools.product(*[range(s) for s in sizes]))
    pr = np.empty(len(states))
    for t, x in enumerate(states):
        v = init[x[0]]
        for k, P in enumerate(Ps): v *= P[x[k], x[k + 1]]
        pr[t] = v
    return np.array(states), pr

def dobrushin(P):
    m = 0.0
    for a in range(P.shape[0]):
        for b in range(a + 1, P.shape[0]):
            m = max(m, 0.5 * np.abs(P[a] - P[b]).sum())
    return m

def one_site_osc(states, r, sizes):
    idx = {tuple(x): t for t, x in enumerate(states)}
    n = len(sizes); c = np.zeros(n)
    for t, x in enumerate(states):
        for j in range(n):
            for v in range(sizes[j]):
                if v != x[j]:
                    y = list(x); y[j] = v
                    c[j] = max(c[j], abs(r[t] - r[idx[tuple(y)]]))
    return c

worst_var = worst_mgf = worst_d2 = 0.0; cases = 0
for trial in range(700):
    n = int(rng.integers(3, 10))
    sizes = [int(rng.integers(2, 5)) for _ in range(n)]
    if np.prod(sizes) > 60000: sizes = [2] * n
    coupling = float(rng.choice([0.0, 0.3, 1.0, 2.5]))
    init, Ps = random_chain(n, sizes, coupling)
    states, pr = joint(init, Ps, sizes)
    kind = rng.choice(["smooth", "spiky", "additive", "last"])
    if kind == "additive":
        r = sum(rng.normal(size=sizes[j])[states[:, j]] for j in range(n))
    elif kind == "smooth":
        r = np.sin(states @ rng.normal(size=n)) * rng.uniform(0.2, 2.0)
    elif kind == "last":
        r = rng.normal(size=sizes[-1])[states[:, -1]] * 2.0 + 0.1 * rng.normal(size=len(states))
    else:
        r = rng.normal(size=len(states)) * rng.uniform(0.1, 1.5)
    c = one_site_osc(states, r, sizes)
    th = [dobrushin(P) for P in Ps]
    C = np.zeros(n)
    for i in range(n):
        prod = 1.0
        for j in range(i, n):
            C[i] += c[j] * prod
            if j < n - 1: prod *= th[j]
    S = float(C @ C)
    if S < 1e-14: continue
    Er = float(pr @ r); rc = r - Er
    var = float(pr @ rc**2)
    assert var <= S / 4 * (1 + 1e-9) + 1e-12, (var, S / 4)
    worst_var = max(worst_var, var / (S / 4))
    for lam in (-3.0, -1.0, -0.3, 0.3, 1.0, 3.0):
        mgf = math.log(float(pr @ np.exp(lam * rc)))
        assert mgf <= lam * lam * S / 8 * (1 + 1e-9) + 1e-12, (mgf, lam * lam * S / 8)
        worst_mgf = max(worst_mgf, mgf / (lam * lam * S / 8))
    w = np.exp(-rc); w /= float(pr @ w)
    d2 = math.log(float(pr @ w**2))
    assert d2 <= S / 2 * (1 + 1e-9) + 1e-12
    worst_d2 = max(worst_d2, d2 / (S / 2)); cases += 1
print(f"{cases} random (chain, remainder) pairs by exact enumeration: no violation")
print(f"largest ratios: Var/(sum C^2/4) = {worst_var:.4f};  ln MGF/(lam^2 sum C^2/8) = {worst_mgf:.4f};  D_2/(sum C^2/2) = {worst_d2:.4f}")
# the two limiting cases
n = 6; sizes = [2] * n
init = np.array([0.3, 0.7]); Ps = [np.tile(np.array([[0.3, 0.7]]), (2, 1)) for _ in range(n - 1)]      # product measure: theta = 0
print("product measure: theta =", [round(dobrushin(P), 12) for P in Ps], "-> C_i = c_i (McDiarmid / Efron-Stein)")
Ps = [np.eye(2) for _ in range(n - 1)]                                                              # frozen chain: theta = 1
print("frozen chain:    theta =", [dobrushin(P) for P in Ps], "-> C_i = sum_{j>=i} c_j (all sites move together)")
json.dump(dict(cases=cases, worst_var=worst_var, worst_mgf=worst_mgf, worst_d2=worst_d2), open("markov_reference_check.json", "w"))
