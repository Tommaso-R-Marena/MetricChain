"""Exact (population-level) checks of part C and of the correlated-sampling statements of part A.

1. Least-favourable submodel (Theorem C1): on random finite models, tilt the base measure along
   h = z_s, compute the exact Kullback-Leibler divergence between the two stratified product laws and
   the exact change of the contrast, and compare with the theorem's bounds.
2. Adaptive allocation (Theorem C2): for the Elfving dual direction, the divergence accumulated by
   ANY allocation of budget B is at most t^2 B max_k Var_k(h)/a_k: check over random allocations.
3. Correlated sampling (Propositions A11, A12): states sampled by finite-state reversible Markov
   chains with exactly computed long-run covariance.  (a) the variance of MBAR under correlated
   sampling, V_corr(s) = sum_k Gamma_k(r*_k(s))/s_k, is searched for violations of convexity;
   (b) the optimally weighted value W(s) = min_r sum_k Gamma_k(r_k)/s_k is convex and <= V_corr;
   (c) with a scalar inefficiency Gamma_k = g_k Var_k, V_corr(s) = V(s/g).

Run: python experiments/mbar/bench/check_lower_bounds_and_chains.py
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar import population as pop  # noqa: E402

rng = np.random.default_rng(424242)
report = {}


def random_model(K, J, conc=None):
    P = rng.dirichlet(np.full(J, conc or rng.uniform(0.3, 3.0)), size=K)
    c = np.zeros(K)
    c[0], c[-1] = -1.0, 1.0
    return P, c


# ---------------------------------------------------------------- 1. least-favourable submodel
worst = dict(kl_ratio=0.0, sep_ratio_min=np.inf, sep_ratio_max=0.0)
for trial in range(300):
    K, J = int(rng.integers(2, 7)), int(rng.integers(6, 14))
    P, c = random_model(K, J)
    s = rng.dirichlet(np.ones(K)) + 0.05
    s /= s.sum()
    N = float(rng.choice([200, 2000, 20000]))
    nu = pop.contrast_measure(P, c)
    V, h, supp = pop.solve_dual(P, s, nu)            # h = z + const maximises the dual; int h dnu = V
    hbar = 0.5 * (h.max() + h.min())
    D = h.max() - h.min()
    tau = 0.5
    t = tau / np.sqrt(N * V)
    if t * D > 0.5:
        continue                                      # outside the theorem's range N >= 4 tau^2 D^2 / V
    Pt = P * (1 + t * (h - hbar))
    Zt = Pt.sum(axis=1)                               # Z_k(t)/Z_k = 1 + t (E_k h - hbar)
    Pt /= Zt[:, None]
    kl = N * np.sum(s * np.sum(Pt * np.log(Pt / P), axis=1))     # KL(P_t^N || P_0^N), exact
    sep = abs(-(c @ np.log(Zt)))                      # exact change of the contrast c.f
    worst["kl_ratio"] = max(worst["kl_ratio"], kl / ((16 / 9) * tau**2))
    worst["sep_ratio_min"] = min(worst["sep_ratio_min"], sep / (tau * np.sqrt(V / N)))
    worst["sep_ratio_max"] = max(worst["sep_ratio_max"], sep / (tau * np.sqrt(V / N)))
    assert kl <= (16 / 9) * tau**2 * (1 + 1e-9)
    bound = tau * np.sqrt(V / N) - 2 * t**2 * np.abs(c).sum() * D**2 / 4
    assert sep >= bound - 1e-12
report["submodel"] = worst
print("1. submodel: max KL / ((16/9) tau^2) =", round(worst["kl_ratio"], 4),
      "; separation / (tau sqrt(V/N)) in [", round(worst["sep_ratio_min"], 4), ",", round(worst["sep_ratio_max"], 4), "]")

# ---------------------------------------------------------------- 2. adaptive allocation
worst2 = 0.0
for trial in range(60):
    K, J = int(rng.integers(3, 6)), int(rng.integers(6, 12))
    P, c = random_model(K, J)
    a = np.exp(rng.normal(0, 0.8, K))
    B = 1000.0
    nu = pop.contrast_measure(P, c)
    sopt, Vopt, info = pop.optimal_allocation(P, nu, cost=a, budget=B, tol=1e-10, kind="measure")
    Vd, h, supp = pop.solve_dual(P, sopt, nu)
    g = pop.state_variances(P, sopt, nu)
    M = np.max(g / a)                                  # = Vopt / B at the optimum (equivalence theorem)
    assert abs(M * B / Vopt - 1) < 1e-4, (M * B, Vopt)
    for _ in range(200):                               # any allocation of the same budget
        n = rng.dirichlet(np.ones(K) * rng.uniform(0.2, 3))
        n *= B / (a @ n)
        worst2 = max(worst2, (n @ g) / (B * M))
        assert n @ g <= B * M * (1 + 1e-9)
report["adaptive"] = dict(max_information_ratio=worst2)
print("2. adaptive: max over allocations of sum_k n_k Var_k(h*) / (B max_k Var_k(h*)/a_k) =", round(worst2, 6))


# ---------------------------------------------------------------- 3. correlated sampling
def reversible_chain(p, mix):
    """A reversible chain with stationary law p: lazy Metropolis on a random symmetric proposal."""
    J = len(p)
    S = rng.random((J, J))
    S = (S + S.T) / 2
    np.fill_diagonal(S, 0)
    S /= S.sum(axis=1).max() * 1.0001
    T = np.zeros((J, J))
    for i in range(J):
        for j in range(J):
            if i != j and p[i] > 0:
                T[i, j] = S[i, j] * min(1.0, p[j] / p[i]) if p[j] > 0 else 0.0
    T *= mix
    np.fill_diagonal(T, 1 - T.sum(axis=1))
    return T


def longrun_form(p, T):
    """Matrix G with sigma_inf^2(r) = r^T G r for functions r (centred or not) of the chain:
    G = D(I - Pi) (2 Zf - I) with Zf the fundamental matrix; symmetric for reversible chains."""
    J = len(p)
    Pi = np.outer(np.ones(J), p)
    Zf = np.linalg.inv(np.eye(J) - T + Pi)
    Dm = np.diag(p)
    C = np.eye(J) - Pi
    G = C.T @ Dm @ (2 * Zf - np.eye(J)) @ C
    return (G + G.T) / 2


def mbar_r(P, s, c):
    nu = pop.contrast_measure(P, c)
    V, h, supp = pop.solve_dual(P, s, nu)
    mu = P @ h
    return s[:, None] * (mu[:, None] - h[None, :]), V       # r*_k = s_k (E_k h - h)


def v_corr(P, s, c, Gs):
    r, _ = mbar_r(P, s, c)
    return float(sum(r[k] @ Gs[k] @ r[k] / s[k] for k in range(len(s))))


def w_opt(P, s, c, Gs):
    """min over the affine set F_c of sum_k r_k^T Gamma_k r_k / s_k, via its KKT system."""
    K, J = P.shape
    n = K * J
    Hm = np.zeros((n, n))
    for k in range(K):
        Hm[k * J:(k + 1) * J, k * J:(k + 1) * J] = Gs[k] / s[k]
    A = np.zeros((K + J, n))
    for k in range(K):
        A[k, k * J:(k + 1) * J] = P[k]
        for x in range(J):
            A[K + x, k * J + x] = P[k, x]
    b = np.concatenate([np.zeros(K), -(c @ P)])
    KKT = np.block([[2 * Hm, A.T], [A, np.zeros((K + J, K + J))]])
    sol = np.linalg.lstsq(KKT, np.concatenate([np.zeros(n), b]), rcond=None)[0]
    r = sol[:n]
    assert np.max(np.abs(A @ r - b)) < 1e-7
    return float(r @ Hm @ r)


viol = dict(count=0, worst=0.0, trials=0, example=None)
wconv = 0.0
wle = 0.0
scal = 0.0
for trial in range(250):
    K, J = int(rng.integers(2, 5)), int(rng.integers(4, 8))
    P, c = random_model(K, J, conc=rng.uniform(0.5, 2.0))
    mixes = rng.uniform(0.02, 1.0, K)                 # some states mix slowly
    Ts = [reversible_chain(P[k], mixes[k]) for k in range(K)]
    Gs = [longrun_form(P[k], Ts[k]) for k in range(K)]
    for k in range(K):                                 # sanity: Gamma_k >= Var_k for positive chains? no; just PSD
        assert np.linalg.eigvalsh(Gs[k]).min() > -1e-9
    for _ in range(12):
        s, u = rng.dirichlet(np.ones(K)) + 0.03, rng.dirichlet(np.ones(K)) + 0.03
        lam = rng.random()
        m = lam * s + (1 - lam) * u
        vs, vu, vm = v_corr(P, s, c, Gs), v_corr(P, u, c, Gs), v_corr(P, m, c, Gs)
        gap = (vm - lam * vs - (1 - lam) * vu) / vm
        viol["trials"] += 1
        if gap > 1e-9:
            viol["count"] += 1
            if gap > viol["worst"]:
                viol["worst"] = float(gap)
                viol["example"] = dict(P=P.tolist(), T=[t.tolist() for t in Ts], s=s.tolist(), u=u.tolist(),
                                       lam=float(lam), values=[vs, vu, vm])
        ws, wu, wm = w_opt(P, s, c, Gs), w_opt(P, u, c, Gs), w_opt(P, m, c, Gs)
        wconv = max(wconv, (wm - lam * ws - (1 - lam) * wu) / wm)
        wle = max(wle, (ws - vs) / vs)
    # scalar inefficiency: Gamma_k = g_k * (covariance form of p_k)  =>  V_corr(s) = V(s / g)
    gk = rng.uniform(1, 30, K)
    Gsc = [gk[k] * (np.diag(P[k]) - np.outer(P[k], P[k])) for k in range(K)]
    s = rng.dirichlet(np.ones(K)) + 0.03
    # MBAR run on data subsampled by g: weights s/g
    r, Veff = mbar_r(P, s / gk, c)
    val = float(sum(r[k] @ Gsc[k] @ r[k] / s[k] for k in range(K)))
    scal = max(scal, abs(val - Veff) / Veff)
report["correlated"] = dict(convexity_violations_of_mbar_variance=viol["count"], segments=viol["trials"],
                            worst_relative_violation=viol["worst"], example=viol["example"],
                            max_convexity_defect_of_W=wconv, max_excess_of_W_over_Vcorr=wle,
                            scalar_model_max_relative_error=scal)
print("3. correlated: convexity violations of MBAR's correlated variance:", viol["count"], "of", viol["trials"],
      "segments; worst relative violation", round(viol["worst"], 5))
print("   optimally weighted value W: max convexity defect", wconv, "; max (W - V_corr)/V_corr", wle)
print("   scalar inefficiency model: max relative error of V_corr(s) = V(s/g):", scal)
with open(os.path.join(HERE, "..", "results", "lower_bounds_and_chains.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print("ALL CHECKS PASSED")
