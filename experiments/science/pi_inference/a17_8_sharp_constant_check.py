#!/usr/bin/env python3
"""Addendum A17, remark to Proposition A17.8 (prompted by workstream R10, SCI-REV-0010 §5) -- coordinator's check.

In the martingale proof of A17.8 the step "conditional range C_i  =>  conditional variance <= C_i^2/4" can be
replaced by the variance of the worst two-point split of the conditional law q = P_{i-1}(b, .) of site i:
        v(q) := max_A q(A) (1 - q(A))  <= 1/4          (the variance is convex in the function, so on the box
                                                        [0, C]^S it is largest at an indicator),
so that      Var_pi(r) <= sum_i v_i C_i^2 ,   v_i := max_b v(P_{i-1}(b, .))   (v_1 from the initial law).
For a binary alphabet v(q) = q(0) q(1), and the conditional moment generating function of the increment is that of
a two-point law, for which the Kearns-Saul inequality gives the constant
        ks(q) := (1 - 2q) / (4 ln((1 - q)/q))  <= 1/8      (-> 1/8 as q -> 1/2; Hoeffding's lemma is ks = 1/8):
        ln E exp(lam (r - E r)) <= lam^2 sum_i ks_i C_i^2 ,   ks_i := max_b ks(P_{i-1}(b, 1)).
Checked here: (1) the Kearns-Saul inequality itself on a grid; (2) both bounds by exact enumeration on random chains
(the same generator as markov_reference_check.py); (3) the symmetric two-state chain with flip probability p and the
uniform field r = (u/2) sum_i s_i: Var/n -> p(1-p) (u/(2p))^2 = (u^2/4)(1-p)/p, i.e. the constant p(1-p) is attained
per site (workstream R10, Proposition R10.2), where the constant 1/4 overshoots by 1/(4p(1-p)).
"""
import itertools, math, json
import numpy as np
rng = np.random.default_rng(20261126)

def ks(q):
    q = min(max(q, 1e-300), 1 - 1e-300)
    if abs(q - 0.5) < 1e-9: return 0.125
    return (1 - 2 * q) / (4 * math.log((1 - q) / q))

# (1) Kearns-Saul on a grid:  ln( q e^{t(1-q)} + (1-q) e^{-tq} ) <= ks(q) t^2
worst = 0.0
for q in np.linspace(0.001, 0.999, 999):
    for t in np.concatenate([np.linspace(-40, 40, 1601), np.linspace(-1, 1, 401)]):
        if t == 0: continue
        lhs = np.logaddexp(math.log(q) + t * (1 - q), math.log(1 - q) - t * q)
        rhs = ks(float(q)) * t * t
        assert lhs <= rhs * (1 + 1e-12) + 1e-15, (q, t, lhs, rhs)
        worst = max(worst, lhs / rhs)
print(f"(1) Kearns-Saul inequality on a grid of 999 x 2001 points (q, t): no violation; largest ratio lhs/rhs = {worst:.6f}")
print(f"    ks(0.5) = {ks(0.5):.4f}, ks(0.3) = {ks(0.3):.6f}, ks(0.1) = {ks(0.1):.6f}, ks(0.01) = {ks(0.01):.6f}   (Hoeffding's lemma: 0.125)")

def vsplit(q):
    """max over subsets A of q(A)(1-q(A))"""
    k = len(q); best = 0.0
    for mask in range(1, 2 ** k - 1):
        a = sum(q[j] for j in range(k) if mask >> j & 1)
        best = max(best, a * (1 - a))
    return best

def random_chain(n, sizes, coupling):
    init = rng.dirichlet(np.ones(sizes[0]))
    Ps = []
    for k in range(n - 1):
        logits = coupling * rng.normal(size=(sizes[k], sizes[k + 1]))
        P = np.exp(logits); P /= P.sum(1, keepdims=True)
        Ps.append(P)
    return init, Ps

def joint(init, Ps, sizes):
    states = np.array(list(itertools.product(*[range(s) for s in sizes])))
    pr = init[states[:, 0]].copy()
    for k, P in enumerate(Ps): pr *= P[states[:, k], states[:, k + 1]]
    return states, pr

def dobrushin(P):
    return max([0.0] + [0.5 * np.abs(P[a] - P[b]).sum() for a in range(P.shape[0]) for b in range(a + 1, P.shape[0])])

def one_site_osc(states, r, sizes):
    n = len(sizes); c = np.zeros(n)
    mult = np.ones(n, dtype=np.int64)
    for j in range(n - 2, -1, -1): mult[j] = mult[j + 1] * sizes[j + 1]
    R = r.reshape(sizes)
    for j in range(n):
        c[j] = float((R.max(axis=j) - R.min(axis=j)).max())
    return c

def Cvec(c, th):
    n = len(c); C = np.zeros(n)
    for i in range(n):
        prod = 1.0
        for j in range(i, n):
            C[i] += c[j] * prod
            if j < n - 1: prod *= th[j]
    return C

# (2) random chains
cases = bin_cases = 0; w_var_sharp = w_var_quarter = w_mgf_ks = 0.0; gain = []
for trial in range(700):
    n = int(rng.integers(3, 10))
    sizes = [int(rng.integers(2, 5)) for _ in range(n)]
    if np.prod(sizes) > 60000 or trial % 2 == 0: sizes = [2] * n
    coupling = float(rng.choice([0.0, 0.3, 1.0, 2.5]))
    init, Ps = random_chain(n, sizes, coupling)
    states, pr = joint(init, Ps, sizes)
    kind = rng.choice(["smooth", "spiky", "additive", "last", "count"])
    if kind == "additive":
        r = sum(rng.normal(size=sizes[j])[states[:, j]] for j in range(n))
    elif kind == "smooth":
        r = np.sin(states @ rng.normal(size=n)) * rng.uniform(0.2, 2.0)
    elif kind == "last":
        r = rng.normal(size=sizes[-1])[states[:, -1]] * 2.0 + 0.1 * rng.normal(size=len(states))
    elif kind == "count":
        r = (states == 0).sum(1) * rng.uniform(0.2, 2.0)
    else:
        r = rng.normal(size=len(states)) * rng.uniform(0.1, 1.5)
    c = one_site_osc(states, r, sizes)
    th = [dobrushin(P) for P in Ps]
    C = Cvec(c, th)
    v = np.array([vsplit(init)] + [max(vsplit(P[b]) for b in range(P.shape[0])) for P in Ps])
    S_sharp = float(v @ (C * C)); S_quarter = float(C @ C) / 4
    if S_quarter < 1e-14: continue
    assert S_sharp <= S_quarter * (1 + 1e-12)
    Er = float(pr @ r); rc = r - Er; var = float(pr @ rc**2)
    assert var <= S_sharp * (1 + 1e-9) + 1e-12, (var, S_sharp)
    w_var_sharp = max(w_var_sharp, var / S_sharp); w_var_quarter = max(w_var_quarter, var / S_quarter)
    gain.append(S_quarter / S_sharp); cases += 1
    if all(s == 2 for s in sizes):
        k = np.array([ks(float(init[1]))] + [max(ks(float(P[b, 1])) for b in range(2)) for P in Ps])
        Sk = float(k @ (C * C))
        for lam in (-3.0, -1.0, -0.3, 0.3, 1.0, 3.0):
            mgf = math.log(float(pr @ np.exp(lam * rc)))
            assert mgf <= lam * lam * Sk * (1 + 1e-9) + 1e-12, (mgf, lam * lam * Sk)
            w_mgf_ks = max(w_mgf_ks, mgf / (lam * lam * Sk))
        bin_cases += 1
gain = np.array(gain)
print(f"(2) {cases} random (chain, remainder) pairs by exact enumeration (n <= 9, alphabets 2-4): Var <= sum v_i C_i^2 never violated;")
print(f"    largest Var/(sum v_i C_i^2) = {w_var_sharp:.4f}   (with the constant 1/4: {w_var_quarter:.4f});")
print(f"    gain (sum C^2/4)/(sum v_i C_i^2): median {np.median(gain):.3f}, range {gain.min():.3f} .. {gain.max():.3f}")
print(f"    {bin_cases} of them binary: ln MGF <= lam^2 sum ks_i C_i^2 never violated; largest ratio {w_mgf_ks:.4f}")

# (3) the symmetric two-state chain, uniform field r = (u/2) sum s_i  (c_j = u):  exact variance from corr(s_i, s_j) = (1-2p)^|i-j|
print("(3) symmetric two-state chain, r = (u/2) sum_i s_i, u = 1:   Var/n   against   p(1-p) C^2 = (1/4)(1-p)/p   and   C^2/4,  C = 1/(2p)")
for p in (0.4, 0.3, 0.2, 0.1):
    lam = 1 - 2 * p; row = []
    for n in (8, 64, 512, 4096):
        var_m = n + 2 * sum((n - k) * lam ** k for k in range(1, n))
        # finite-n bound: sum_i v_i C_i^2 with C_i = sum_{j>=i} lam^{j-i}, v_1 = 1/4 (uniform initial law), v_i = p(1-p)
        Ci = np.array([(1 - lam ** (n - i)) / (1 - lam) for i in range(n)])
        bound = 0.25 * Ci[0] ** 2 + p * (1 - p) * float((Ci[1:] ** 2).sum())
        assert 0.25 * var_m <= bound * (1 + 1e-12)
        row.append(f"n={n}: {0.25 * var_m / n:.5f} (bound/n {bound / n:.5f})")
    print(f"    p = {p}: " + "; ".join(row) + f";   limit (1/4)(1-p)/p = {0.25 * (1 - p) / p:.5f};  with 1/4: {0.25 / (2 * p) ** 2:.5f}  (overshoot {1 / (4 * p * (1 - p)):.3f})")
json.dump(dict(cases=cases, binary_cases=bin_cases, worst_var_sharp=w_var_sharp, worst_var_quarter=w_var_quarter, worst_mgf_ks=w_mgf_ks,
               gain_median=float(np.median(gain)), gain_min=float(gain.min()), gain_max=float(gain.max())), open("a17_8_sharp_constant_check.json", "w"))
print("ALL OK")
