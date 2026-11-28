"""Supplementary experiment S2 - NOT pre-registered.  Proposition 9.7 of CERTIFIED_INFERENCE.md, which rests on
an inequality of the theory division (THY-MSG-0023 section 3(2)): for a reference that is not a product, the
site-wise computation of Corollary 9.3 with the constants u + kappa_i around the one-site marginals of the
reference is a sound outer bound for additive observables.

Checked against the exact programme over the bounded-influence class on Ising rings of ten sites (1024
configurations).  Target: the fraction of up sites.  Data: the fraction of up sites among the first five, known
to +-0.02 around its reference value.  kappa_i is computed exactly from the enumerated reference (the largest
log-ratio of the conditional laws of the other sites given the two states of site i); the analytic bound for the
ring is 8|J|.  The column "naive" applies Corollary 9.3 with kappa = 0, i.e. as if the reference were a product:
it is NOT sound, and the table shows by how much the exact interval sticks out of it.

    python experiments/eng/phase2_nonproduct/marginal_bound.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))
from metricchain_eng import certinf as ci  # noqa: E402

N_SITES, FIELD = 10, 0.1


def main():
    states, edges, _ = ci.hypercube(N_SITES)
    spins = 2 * states - 1
    idx = np.arange(1 << N_SITES)
    f = states.mean(axis=1)
    phi = states[:, :5].mean(axis=1)[:, None]
    f_sites = [np.array([0.0, 1.0 / N_SITES])] * N_SITES
    phi_sites = [np.array([[0.0], [0.2 if i < 5 else 0.0]]) for i in range(N_SITES)]
    rows = []
    for J in (0.0, 0.02, 0.05, 0.1, 0.2, 0.4):
        e = -(J * (spins * np.roll(spins, -1, axis=1)).sum(axis=1) + FIELD * spins.sum(axis=1))
        pi = np.exp(-(e - e.min()))
        pi /= pi.sum()
        marg, kappa = np.zeros(N_SITES), np.zeros(N_SITES)
        for i in range(N_SITES):
            up = (idx >> i) & 1 == 1
            marg[i] = pi[up].sum()
            hi, lo = idx[up], idx[up] ^ (1 << i)
            kappa[i] = np.abs(np.log(pi[hi] / marg[i]) - np.log(pi[lo] / (1 - marg[i]))).max()
        site_pi = [np.array([1 - q, q]) for q in marg]
        box = ci.Box([float(pi @ phi[:, 0])], 0.02)
        for u in (0.3, 1.0):
            for label, ph, ps, reg in (("no data", None, None, None), ("with data", phi, phi_sites, box)):
                exact = ci.lp_ratio_class(pi, edges, math.exp(u), f, ph, reg)
                outer = ci.additive_interval(site_pi, u + kappa, f_sites, ps, reg)
                naive = ci.additive_interval(site_pi, u, f_sites, ps, reg)
                rows.append(dict(J=J, u=u, case=label, kappa=float(kappa.max()), kappa_analytic=8 * J, exact=list(exact),
                                 outer=[outer["lo"], outer["hi"]], naive=[naive["lo"], naive["hi"]],
                                 outer_sound=bool(outer["lo"] <= exact[0] + 1e-9 and outer["hi"] >= exact[1] - 1e-9),
                                 naive_violation=float(max(naive["lo"] - exact[0], exact[1] - naive["hi"], 0.0)),
                                 width_ratio=float((outer["hi"] - outer["lo"]) / (exact[1] - exact[0]))))
                r = rows[-1]
                print("J %.2f u %.1f %-9s kappa %.3f (8J = %.2f) exact [%.4f, %.4f] outer [%.4f, %.4f] ratio %.2f sound %s | naive violated by %.4f"
                      % (J, u, label, r["kappa"], 8 * J, *exact, *r["outer"], r["width_ratio"], r["outer_sound"], r["naive_violation"]), flush=True)
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "marginal_bound.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
