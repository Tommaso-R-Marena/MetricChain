"""Exact checks of the cross-divisional statements of docs/mbar/SYNTHESIS.md (population level).

S1  path bound:  V_c(s) <= sum_j chi2(P_{j+1} || P_j)/s_j along any path of states from a to b
    (the telescoping tuple r_j = p_{j+1}/p_j - 1 lies in the affine set F_c of Theorem A1), and
    V*_c(B) <= (sum_j sqrt(a_j chi2_j))^2 / B  ("thermodynamic length").
S2  tempering ladder on the cube class of the programme: u-Lipschitz psi on {0,1}^n, states
    exp(-j psi/K'), K' = ceil(osc psi): every step has chi2 <= (e-1)^2/(4e), hence
    V_c(uniform) <= 0.2716 K'^2 -- polynomial in n, against exp(n h) evaluations without samplers.
S3  the envelope-ratio cost of the certified-inference division (its Theorem 6.1(a) instance):
    with reference draws only the variance of the target average grows like Gamma; a ladder of
    ceil(log Gamma) intermediate ensembles brings it to O((log Gamma)^2).
S4  one round of allocation: on the 'bridge' instance only one state is informative, so a fixed
    allocation s has efficiency exactly s_m; uniform allocation attains the worst case 1/K.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar import population as pop  # noqa: E402

rng = np.random.default_rng(909)
report = {}
CHI_STEP = (np.e - 1) ** 2 / (4 * np.e)


def chi2(Pa, Pb):
    """chi2(Pb || Pa) = E_a[(p_b/p_a - 1)^2]; +inf if Pb is not dominated by Pa."""
    if np.any((Pa == 0) & (Pb > 0)):
        return np.inf
    m = Pa > 0
    return float(np.sum(Pb[m] ** 2 / Pa[m]) - 1.0)


# ---------------------------------------------------------------- S1
worst = 0.0
worst_len = 0.0
for trial in range(300):
    K, J = int(rng.integers(2, 7)), int(rng.integers(5, 14))
    P = rng.dirichlet(np.full(J, rng.uniform(0.5, 3.0)), size=K)
    s = rng.dirichlet(np.ones(K)) + 0.05
    perm = rng.permutation(K)
    L = int(rng.integers(2, K + 1))
    path = perm[:L]
    c = np.zeros(K)
    c[path[0]], c[path[-1]] = 1.0, -1.0
    V = pop.variance(P, s, pop.contrast_measure(P, c))
    chis = np.array([chi2(P[path[j]], P[path[j + 1]]) for j in range(L - 1)])
    bound = float(np.sum(chis / s[path[:-1]]))
    worst = max(worst, V / bound)
    assert V <= bound * (1 + 1e-9)
    a = np.exp(rng.normal(0, 0.7, K))
    sopt, Vopt, _ = pop.optimal_allocation(P, pop.contrast_measure(P, c), cost=a, budget=1.0, tol=1e-8, kind="measure")
    length2 = float(np.sum(np.sqrt(a[path[:-1]] * chis)) ** 2)
    worst_len = max(worst_len, Vopt / length2)
    assert Vopt <= length2 * (1 + 1e-6)
report["S1"] = dict(max_V_over_path_bound=worst, max_Vopt_over_length_bound=worst_len)
print("S1 path bound: max V/bound =", round(worst, 4), "; max V*/(thermodynamic length)^2 =", round(worst_len, 4))


# ---------------------------------------------------------------- S2
def lipschitz_psi(n, u):
    """A random u-Lipschitz function on the n-cube (Hamming metric): the McShane envelope
    psi(x) = min_j (v_j + u d(x, c_j)) of a few random centres and values."""
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(float)
    m = int(rng.integers(1, 5))
    C = X[rng.integers(0, 2 ** n, m)]
    v = rng.uniform(0, u * n, m)
    d = np.abs(X[:, None, :] - C[None, :, :]).sum(axis=2)
    return np.min(v[None, :] + u * d, axis=1)


rows = []
for n in (8, 10, 12):
    for u in (0.5, 1.0, 2.0):
        for rep in range(3):
            psi = lipschitz_psi(n, u)
            psi -= psi.min()
            osc = psi.max()
            Kp = max(1, int(np.ceil(osc)))
            P = np.exp(-np.outer(np.arange(Kp + 1) / Kp, psi))
            P /= P.sum(axis=1, keepdims=True)
            chis = np.array([chi2(P[j], P[j + 1]) for j in range(Kp)])
            assert chis.max() <= CHI_STEP + 1e-12, chis.max()
            c = np.zeros(Kp + 1)
            c[0], c[-1] = 1.0, -1.0
            nu = pop.contrast_measure(P, c)
            Vu = pop.variance(P, np.full(Kp + 1, 1.0 / (Kp + 1)), nu)
            sopt, Vopt, _ = pop.optimal_allocation(P, nu, tol=1e-7, kind="measure")
            # telescoping estimator samples states 0..K'-1 uniformly: bound CHI_STEP * K'^2
            assert Vopt <= np.sum(np.sqrt(chis)) ** 2 * (1 + 1e-6) <= CHI_STEP * Kp ** 2 * (1 + 1e-6)
            rows.append(dict(n=n, u=u, osc=float(osc), ladder_states=Kp + 1, V_uniform=Vu, V_optimal=Vopt,
                             length_bound=float(np.sum(np.sqrt(chis)) ** 2), class_bound=CHI_STEP * Kp ** 2))
report["S2"] = rows
r = rows[-1]
print("S2 tempering ladders on the cube: all steps chi2 <=", round(CHI_STEP, 4),
      "; e.g. n=%d u=%.1f: K'=%d  V_uniform=%.1f  V*=%.1f  length^2=%.1f  0.2716K'^2=%.1f"
      % (r["n"], r["u"], r["ladder_states"] - 1, r["V_uniform"], r["V_optimal"], r["length_bound"], r["class_bound"]))
print("   ratio V_uniform/(0.2716 K'^2): min %.3f max %.3f over %d instances"
      % (min(x["V_uniform"] / x["class_bound"] for x in rows), max(x["V_uniform"] / x["class_bound"] for x in rows), len(rows)))

# ---------------------------------------------------------------- S3
rows = []
for Gamma in (4.0, 16.0, 64.0, 256.0, 1024.0):
    a = 1.0 / Gamma                       # reference pi on {0,1}: pi(1) = a; weights 1 on 0, Gamma on 1
    pi = np.array([1 - a, a])
    w = np.array([1.0, Gamma])
    f = np.array([0.0, 1.0])              # target average E_p f = p(1)
    Kp = int(np.ceil(np.log(Gamma)))
    P = np.array([pi * w ** (j / Kp) for j in range(Kp + 1)])
    P /= P.sum(axis=1, keepdims=True)
    nu = pop.observable_measure(P, Kp, f)
    only_ref = np.zeros(Kp + 1)
    only_ref[0] = 1.0
    only_tgt = np.zeros(Kp + 1)
    only_tgt[-1] = 1.0
    V_ref = pop.variance(P, only_ref, nu)
    V_tgt = pop.variance(P, only_tgt, nu)
    # free energy of the target relative to the reference (log of the normalising constant)
    c = np.zeros(Kp + 1)
    c[0], c[-1] = 1.0, -1.0
    nuF = pop.contrast_measure(P, c)
    VF_ref = pop.variance(P, only_ref, nuF)                      # exponential averaging from the reference
    VF_ladder = pop.optimal_allocation(P, nuF, tol=1e-8, kind="measure")[1]
    rows.append(dict(Gamma=Gamma, ladder_states=Kp + 1, V_average_reference_only=V_ref, V_average_target_only=V_tgt,
                     V_free_energy_reference_only=VF_ref, V_free_energy_optimal_ladder=VF_ladder,
                     ratio_ref_over_Gamma=V_ref / Gamma, ladder_over_log2=VF_ladder / np.log(Gamma) ** 2))
    print("S3 Gamma=%6.0f: average from reference draws V=%.2f (V/Gamma=%.3f), from target draws V=%.3f; "
          "free energy: reference only V=%.1f, optimal ladder V=%.2f (V/log^2 Gamma=%.3f)"
          % (Gamma, V_ref, V_ref / Gamma, V_tgt, VF_ref, VF_ladder, VF_ladder / np.log(Gamma) ** 2))
report["S3"] = rows

# ---------------------------------------------------------------- S4
K = 5
# points: block A = {0,1}, block B = {2,3}; state m uniform on A u B; a uniform on A; b uniform on B;
# two further states identical to a (uninformative).  Contrast f_b - f_a.
P = np.array([[0.5, 0.5, 0, 0], [0, 0, 0.5, 0.5], [0.25, 0.25, 0.25, 0.25], [0.5, 0.5, 0, 0], [0.5, 0.5, 0, 0]])
c = np.array([-1.0, 1.0, 0, 0, 0])
nu = pop.contrast_measure(P, c)
Vbest = pop.variance(P, np.array([0, 0, 1.0, 0, 0]), nu)
effs = []
for _ in range(200):
    s = rng.dirichlet(np.ones(K))
    V = pop.variance(P, s, nu)
    effs.append(abs(Vbest / V - s[2]))
sopt, Vopt, _ = pop.optimal_allocation(P, nu, tol=1e-9, kind="measure")
report["S4"] = dict(V_bridge_only=Vbest, V_optimal=Vopt, max_abs_efficiency_minus_s_m=float(max(effs)),
                    uniform_efficiency=float(Vbest / pop.variance(P, np.full(K, 1 / K), nu)))
print("S4 bridge instance: V(e_m) = %.3f = V* = %.3f; |efficiency(s) - s_m| <= %.1e; uniform efficiency = %.3f = 1/K"
      % (Vbest, Vopt, max(effs), report["S4"]["uniform_efficiency"]))
with open(os.path.join(HERE, "..", "results", "synthesis_checks.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print("ALL SYNTHESIS CHECKS PASSED")
