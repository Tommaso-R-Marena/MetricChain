#!/usr/bin/env python3
"""R1: a possible generalisation of Lemma 11.89 (referee's question, numerical evidence only).
Ferromagnetic Ising model on n spins, couplings J_ij >= 0, arbitrary fields h.  For two spins u, v:
   omega(h) := ln[P(++)P(--)/(P(+-)P(-+))]  (log odds ratio of the pair marginal),   I(h) := I(sigma_u; sigma_v).
Questions:  (Q1) omega(h) <= omega(0)?   (Q2) I(h) <= I(0)?
By Lemma 11.89, I(h) <= K(omega(h)/4), and at h = 0 the pair marginal has uniform margins, I(0) = K(omega(0)/4);
so (Q1) implies (Q2).  For n = 3 (Q1) is elementary: omega = 4 J_uv + ln[(cosh 2h_w + cosh 2(J_uw+J_vw))/(cosh 2h_w + cosh 2(J_uw-J_vw))].
Related published statement: Ding, Song, Sun (arXiv:2107.09243): spin-spin correlations of ferromagnetic Ising models are
maximal at zero field.  Also tested: what happens WITHOUT ferromagnetism (mixed signs)."""
import itertools, math
import numpy as np

def pair_stats(Jm, h, u, v):
    n = len(h)
    P = np.zeros((2, 2))
    for s in itertools.product((1, -1), repeat=n):
        s = np.array(s)
        E = 0.5 * s @ Jm @ s + h @ s
        P[(1 - s[u]) // 2, (1 - s[v]) // 2] += math.exp(E)
    P /= P.sum()
    omega = math.log(P[0, 0] * P[1, 1] / (P[0, 1] * P[1, 0]))
    pu, pv = P.sum(1), P.sum(0)
    I = float(np.sum(P * np.log(P / np.outer(pu, pv))))
    return omega, I

rng = np.random.default_rng(89)
for label, signed in (("ferromagnetic (J_ij >= 0)", False), ("mixed signs", True)):
    worst_om = worst_I = -math.inf; n_cases = 0; viol_om = viol_I = 0
    for trial in range(3000):
        n = int(rng.integers(3, 7))
        Jm = rng.exponential(0.5, (n, n)) * (rng.random((n, n)) < 0.7)
        if signed:
            Jm = Jm * rng.choice([-1, 1], (n, n))
        Jm = np.triu(Jm, 1); Jm = Jm + Jm.T
        h = rng.normal(0, 1.0, n) * rng.choice([0.2, 1.0, 3.0])
        u, v = 0, 1
        om_h, I_h = pair_stats(Jm, h, u, v)
        om_0, I_0 = pair_stats(Jm, np.zeros(n), u, v)
        n_cases += 1
        worst_om = max(worst_om, abs(om_h) - abs(om_0)); worst_I = max(worst_I, I_h - I_0)
        viol_om += (abs(om_h) > abs(om_0) + 1e-10); viol_I += (I_h > I_0 + 1e-12)
    print(f"{label}: {n_cases} random models (n = 3..6): max[|omega(h)| - |omega(0)|] = {worst_om:.3e} ({viol_om} violations); "
          f"max[I(h) - I(0)] = {worst_I:.3e} ({viol_I} violations)")
