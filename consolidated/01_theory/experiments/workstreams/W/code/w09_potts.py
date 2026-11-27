"""w09 (W7, optional): a known part that is a function of the joint type -- the mean-field three-state Potts model
f(x) = -n (bJ/2) sum_a P_x(a)^2, one site type, Hamming envelope u*[a != b], in the regime where the rate function
I(P) = -(bJ/2) sum_a P(a)^2 - H(P) - min is convex (bJ <= 2 for every number of states).

By the single-letter theorem (report, Theorem W2, which does not use a product structure) the exponent of every
algorithm at the flat-histogram instance is R_H(e) = sup over labelled profiles of
        r_mu(e) = min{ MI(nu) : dist(nu -> mu) + I(nubar) <= e + MI(mu) + I(mubar) }
('v or I': Lemma W2.2).  Tested here with the primal solver (a convex programme for convex I):
 (1) at the optimal profile mu* of the FLAT PRODUCT site (labels = the three dips with equal weights, letter laws =
     their Gibbs laws for the uniform site law) the value is the flat product site's exponent, for every coupling
     in the convex regime (Proposition W7.2: a colour-symmetric interaction does not change the value at the
     symmetric profile);
 (2) random labelled profiles and perturbations of mu* do not exceed it at e = 0 (R_H(0) = h_flat would follow
     from Proposition W7.3 and the numerical observation that the uniform law is the hardest site law at e = 0).
"""
import math
import sys
import time

import numpy as np

from wlib import *
from wprimal import *

t00 = time.time()
rng = np.random.default_rng(5)
u = 1.0
q = 3
flat = Site(np.ones(q) / q, u * (1 - np.eye(q)), "flat3")
ch = Chain([flat], [1.0])
E = ch.E()
print(f"=== w09: mean-field Potts, q = {q}, Hamming envelope u = {u}; flat product site: E = {E:.6f}, a = {ch.a()[0]:.6f} ===")


def potts(bJ):
    def raw(P):
        return -(bJ / 2) * float(np.sum(P * P)) + float(np.sum(P * np.log(P)))
    m0 = raw(np.ones(q) / q)              # for bJ <= q the uniform law is the minimiser of a convex symmetric function

    def Ifun(P):
        return raw(P) - m0, -bJ * P + np.log(P) + 1.0
    return Ifun


for e_frac in (0.0, 0.3):
    e = e_frac * E
    R, ts = ch.R(e, return_t=True)
    prof, phis, Ms, gam = dip_profile(ch, ts)
    # symmetrise the label weights (the optimal weights are uniform over the three dips by symmetry)
    print(f"\n e = {e_frac} E: flat product site R = {R:.8f} at t* = {ts:.4f}; labels {np.round(phis[0], 2).tolist()}, weights {np.round(prof.P[0], 4)}")
    for bJ in (0.0, 0.5, 1.0, 1.5, 1.9, -2.0):
        Ifun = potts(bJ)
        mubar = prof.mean()[0]
        B = e + MI(ch, prof) + Ifun(mubar)[0]
        val = r_primal(ch, prof, e, landscape="fun", Ifun=Ifun, B=B, starts=3)
        best = -1.0
        nfail = 0
        if e_frac == 0.0:
            for it in range(40):
                if it % 2:
                    pr = Profile([rng.dirichlet(np.ones(int(rng.integers(1, 4))))], None) if False else None
                k = int(rng.integers(1, 4))
                if it % 2 == 0:
                    pr = Profile([rng.dirichlet(np.ones(k))], [rng.dirichlet(rng.choice([0.5, 1.0, 3.0]) * np.ones(q), size=k)])
                else:
                    sc = float(rng.choice([0.05, 0.2, 0.5]))
                    pr = Profile([np.abs(prof.P[0] * np.exp(sc * rng.normal(size=prof.P[0].shape)))],
                                 [np.abs(prof.mu[0] * np.exp(sc * rng.normal(size=prof.mu[0].shape)))])
                Bp = e + MI(ch, pr) + Ifun(pr.mean()[0])[0]
                try:
                    best = max(best, r_primal(ch, pr, e, landscape="fun", Ifun=Ifun, B=Bp, starts=2))
                except RuntimeError:
                    nfail += 1
            extra = f"; largest value over 40 random/perturbed profiles: {best:.8f} (excess {best - R:+.1e}; solver failures {nfail})"
        else:
            extra = ""
        print(f"   bJ = {bJ:+.1f}: r_mu*(e) with the Potts rate function = {val:.8f} (difference to the flat product site: {val - R:+.1e}){extra}")
print(f"time {time.time()-t00:.0f} s")
