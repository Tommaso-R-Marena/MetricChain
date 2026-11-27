"""t15: the tail lemma relative to a reference instance, checked directly on the 4-cube (all subsets enumerated).

For a reference psi_ref in L_u (H, the zero residual, an additive instance), mu_ref = pi e^{-psi_ref}/Z_ref,
What = W/w_ref, s_ref(a,a') = u d(a,a') + psi_ref(a) - psi_ref(a'):
   (a) What(a) <= What(a') e^{s_ref(a,a')} for every W = e^{-psi}, psi u-Lipschitz (also for fibre averages);
   (b) E_mu (What - s)_+ <= s Xi_ref(mu_ref(What > s)) for every threshold s with {What > s} proper;
   (c) equality for the reference with the deepest dip on an arbitrary set D (so Xi_ref is the best possible);
   (d) mutations must fail: M2 slack with the wrong orientation; M4 the tail function of the uniform cube (Harper)
       evaluated at the same probability; M5 the tail function of the zero reference used for the reference H.
"""
import math, sys, time
import numpy as np
import t14_two_level_H as T

rng = np.random.default_rng(15)
T.rng = rng
n_o = 4
N = 2 ** n_o
pop, D = T.cube(n_o)
t0 = time.time()
tot = dict(checks=0, viol=0, lip_viol=0, tight=0, m2=0, m4=0, m5=0, worst=0.0)
for p in (0.05, 0.15, 0.3, 0.5, 0.7):
    for u in (0.6, 1.0, 2.0):
        for ref in ("H", "zero", round(float(rng.uniform(-u, u)), 3)):
            tab = T.tables(n_o, p, u, ref)
            tabM2 = T.tables(n_o, p, u, ref, "M2")
            tab0 = T.tables(n_o, p, u, "zero")
            mu, wR, sR = tab["muH"], tab["wH"], tab["sH"]
            for trial in range(40):
                kind = trial % 8
                if kind <= 5:
                    n_i = int(rng.integers(0, 3))
                    n = n_o + n_i
                    popn, Dn = T.cube(n)
                    psi = T.rand_lipschitz(n, u, Dn, popn, kind) + float(rng.uniform(-2, 2))
                    popi = popn[: 2 ** n_i]
                    pii = p ** popi * (1 - p) ** (n_i - popi)
                    W = (np.exp(-psi).reshape(N, 2 ** n_i) * pii[None, :]).sum(axis=1)
                    extremal = False
                else:
                    k = int(rng.integers(1, N - 1))
                    Dset = np.zeros(N, dtype=bool); Dset[rng.choice(N, size=k, replace=False)] = True
                    psiR = -np.log(wR)
                    low = (psiR[~Dset][None, :] - u * D[np.ix_(np.arange(N), ~Dset)]).max(axis=1)
                    W = np.exp(-np.where(Dset, low, psiR))
                    extremal = True
                What = W / wR
                # (a)
                if (np.log(What[:, None] / What[None, :]) > sR + 1e-9).any():
                    tot["lip_viol"] += 1
                for s in np.unique(What)[:-1]:
                    above = What > s
                    q = float(mu[above].sum())
                    lhs = float((mu * np.maximum(What - s, 0)).sum())
                    rhs = s * T.Xi(tab, q)
                    tot["checks"] += 1
                    tol = 1e-12 * float(What.max())          # rounding: levels that differ by one ulp are not levels
                    if lhs > rhs * (1 + 1e-9) + tol:
                        tot["viol"] += 1
                    tot["worst"] = max(tot["worst"], lhs / rhs if rhs > tol else 0.0)
                    if extremal and rhs > tol and lhs >= rhs * (1 - 1e-9):
                        tot["tight"] += 1
                    if lhs > s * T.Xi(tabM2, q) * (1 + 1e-9) + tol:
                        tot["m2"] += 1
                    if lhs > s * T.harper_tail(n_o, u, min(q, 1 - 1e-12)) * (1 + 1e-9) + tol:
                        tot["m4"] += 1
                    if ref == "H" and lhs > s * T.Xi(tab0, q) * (1 + 1e-9) + tol:
                        tot["m5"] += 1
print(tot)
print("tail lemma relative to the reference holds in all checks:", tot["viol"] == 0 and tot["lip_viol"] == 0,
      "; extremal instances attain equality:", tot["tight"] > 0,
      "; mutations detected (violations): wrong orientation", tot["m2"], ", Harper function", tot["m4"], ", zero-reference function for H", tot["m5"])
print("time %.0fs" % (time.time() - t0))
