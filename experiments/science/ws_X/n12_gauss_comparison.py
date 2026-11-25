"""N12 — falsification test for Proposition 5'(a):
    ln E_unif exp( (1/2) s^T J s )  <=  phi(||J||_F),   phi(F) = -1/2 ln(1-F) - F/2,
for every symmetric zero-diagonal J with ||J||_F = F < 1 (s uniform on {+-1}^n), and the
intermediate inequality  E_s exp(s^T J s/2) <= det(I - J)^{-1/2}  (Rademacher chaos of order
two with zero diagonal is dominated by the Gaussian one).
Families: Gaussian J, sparse J, Curie-Weiss, antiferromagnet, random-sign rank one, k-cliques.
Run: python3 n12_gauss_comparison.py
"""
import json
import math

import numpy as np

rng = np.random.default_rng(1212)
phi = lambda F: -0.5 * math.log(1 - F) - F / 2


def lnE(J, n):
    idx = np.arange(1 << n)
    s = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
    q = 0.5 * np.einsum("xi,ij,xj->x", s, J, s)
    m = q.max()
    return m + math.log(np.mean(np.exp(q - m)))


def families(n):
    G = rng.standard_normal((n, n)); G = (G + G.T) / 2
    yield "gaussian", G
    S = G * (rng.random((n, n)) < 0.2); S = np.triu(S, 1); yield "sparse", S + S.T
    yield "curie-weiss", np.ones((n, n))
    yield "antiferro", -np.ones((n, n))
    u = rng.choice([-1.0, 1.0], n); yield "gauged CW", np.outer(u, u)
    k = max(2, n // 2); C = np.zeros((n, n)); C[:k, :k] = 1; yield f"{k}-clique", C
    v = rng.standard_normal(n); yield "rank one", np.outer(v, v)


worst_gap, worst_gauss, count = math.inf, math.inf, 0
closest = None
for trial in range(400):
    n = int(rng.integers(3, 11))
    for name, J in families(n):
        J = J.copy()
        np.fill_diagonal(J, 0.0)
        nf = np.linalg.norm(J)
        if nf < 1e-12:
            continue
        F = float(rng.uniform(0.05, 0.98))
        J *= F / nf
        val = lnE(J, n)
        lam = np.linalg.eigvalsh(J)
        gauss = -0.5 * np.sum(np.log(1 - lam))            # ln det(I-J)^{-1/2}
        count += 1
        assert val <= gauss + 1e-10, (name, n, F, val, gauss)
        assert gauss <= phi(F) + 1e-10, (name, n, F, gauss, phi(F))
        worst_gauss = min(worst_gauss, gauss - val)
        if phi(F) - val < worst_gap:
            worst_gap, closest = phi(F) - val, (name, n, F, val, phi(F))
print(count, "instances; no violation.")
print("smallest slack phi(F) - ln E:", worst_gap, " at", closest)
print("smallest slack Gaussian - Rademacher:", worst_gauss)
json.dump({"instances": count, "smallest_slack": worst_gap, "closest": closest,
           "smallest_slack_gauss_minus_rademacher": worst_gauss}, open("n12_gauss_comparison.json", "w"), indent=1)
