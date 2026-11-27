"""w02: the single-letter claims of W2/W3, tested with the PRIMAL solver of wprimal.py (minimisation over
couplings; shares nothing with the game / Renyi formulas of wlib.py used in the search).

For each chain and accuracy e:
 T1  R(e) = max_t [sum_j lam_j F*_j(t) - t e]  (variational form), with t*, gamma*, M*;
 T2  re-evaluation of the optimum: r_{mu*}(e) for the generalised-dip profile mu* (labels = vertices of the
     Lipschitz polytopes, weights M*, letter laws = Gibbs laws of the vertices), with the landscape
     'H' (v by a second-stage coupling), 'I' (the rate function itself: Lemma 'v or I'), and 'add' (gamma*);
 T3  the collapse to additive instances (Sion): r_mu(e; H) = max_gamma V(mu, e + alpha(mu); gamma) on random
     labelled profiles (outer maximisation over gamma by Nelder-Mead);
 T4  evaluation lemma: r_mu(e; H) <= R(e) for random labelled profiles (1-3 labels per site type) and for
     perturbations of mu* (so mu* is at least a local maximiser), e of both signs;
 T5  non-adaptive side: cone formula min{MI : D(nu || pi^phi | M*) <= x} against R(S^{-1}(x)) and the pair
     identity theta_na(e + R(e)) = R(e) through the cone formula; random label laws never exceed.
usage: python3 w02_single_letter.py <chain> [nrand]
"""
import sys
import time

import numpy as np
from scipy.optimize import minimize

from wlib import *
from wprimal import *
from wsites import chains

np.set_printoptions(precision=5, suppress=True, linewidth=160)
name = sys.argv[1] if len(sys.argv) > 1 else "path"
nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 40
t00 = time.time()
ch = chains()[name] if name != "bin01" else Chain([binary_site(0.1, 2.0)], [1.0], "bin01")
rng = np.random.default_rng(20261125)
E = ch.E()
a = ch.a()[0]
print(f"=== w02 single-letter tests: chain {ch.name}; fractions {ch.lam}; E = {E:.6f}; a = {a:.6f} ===")
for s in ch.sites:
    print(f"  site {s.name}: pi = {s.pi}, vertices of L (rows; * = distance function):")
    for k in range(s.nv):
        print(f"     {'*' if s.is_dist[k] else ' '} {s.V[k]}")


def random_profile(kmax=3, conc=1.0):
    P, mu = [], []
    for s in ch.sites:
        k = int(rng.integers(1, kmax + 1))
        P.append(rng.dirichlet(np.ones(k)))
        mu.append(rng.dirichlet(conc * np.ones(s.q), size=k))
    return Profile(P, mu)


def perturbed(prof, scale):
    P = [np.abs(p * np.exp(scale * rng.normal(size=p.shape))) for p in prof.P]
    mu = [np.abs(m * np.exp(scale * rng.normal(size=m.shape))) for m in prof.mu]
    return Profile(P, mu)


worst_T2 = 0.0
for frac in (0.0, 0.3, 0.6):
    e = frac * E
    R, ts = ch.R(e, return_t=True)
    gam = ch.gammas(ts)
    prof, phis, Ms, _ = dip_profile(ch, ts)
    up = ch.Fstar_upper(ts) - ts * e
    print(f"\n--- e = {frac} E = {e:.6f}:  R = {R:.9f} (upper certificate at t*: {up:.9f})  t* = {ts:.5f}")
    for j, s in enumerate(ch.sites):
        print(f"    type {j} ({s.name}): gamma* = {gam[j]},  M* = {Ms[j]},  Gibbs law of gamma* = {s.gibbs(gam[j])}")
    vals = {}
    for land in ("H", "I", "add"):
        vals[land] = r_primal(ch, prof, e, landscape=land, gammas=gam, starts=3)
    print(f"    T2 primal at mu*: H {vals['H']:.9f}   I {vals['I']:.9f}   additive gamma* {vals['add']:.9f}"
          f"   (differences to R: {vals['H']-R:+.1e}, {vals['I']-R:+.1e}, {vals['add']-R:+.1e})")
    worst_T2 = max(worst_T2, *(abs(vals[k] - R) for k in vals))

    # T4: random profiles and perturbations of mu*
    best_rand, best_pert, nfail = -1.0, -1.0, 0
    for it in range(nrand):
        pr = random_profile(conc=float(rng.choice([0.3, 1.0, 3.0])))
        try:
            val = r_primal(ch, pr, e, landscape="H", starts=2)
        except RuntimeError:
            nfail += 1
            continue
        best_rand = max(best_rand, val)
    for it in range(nrand):
        pr = perturbed(prof, float(rng.choice([0.02, 0.1, 0.3])))
        try:
            val = r_primal(ch, pr, e, landscape="H", starts=2)
        except RuntimeError:
            nfail += 1
            continue
        best_pert = max(best_pert, val)
    print(f"    T4 largest r_mu(e;H) over {nrand} random profiles: {best_rand:.9f}; over {nrand} perturbations of mu*: {best_pert:.9f};"
          f" R = {R:.9f}; excess {max(best_rand, best_pert) - R:+.2e}; solver failures {nfail}")

    # T5: non-adaptive side through the cone formula
    x = e + R
    th_tr = ch.theta_na_direct(x)[0]
    th_cone = cone_primal(ch, prof.P, phis, x)
    best_cone = -1.0
    for it in range(nrand):
        Pr = [rng.dirichlet(np.ones(s.nv)) for s in ch.sites]
        Pr = [np.where(rng.random(len(p)) < 0.3, 0.0, p) + 1e-12 for p in Pr]
        Pr = [p / p.sum() for p in Pr]
        best_cone = max(best_cone, cone_primal(ch, Pr, [s.V for s in ch.sites], x, starts=1))
    print(f"    T5 pair identity: x = e + R = {x:.6f}: cone formula at M*: {th_cone:.9f}; max_tau (F*-tau x)/(1-tau) = {th_tr:.9f}; R = {R:.9f};"
          f" largest cone value over {nrand} random label laws on all vertices: {best_cone:.9f}")

# T4 at a negative accuracy
e = -0.25 * a
R = ch.R(e)
best = -1.0
cnt = 0
for it in range(3 * nrand):
    pr = random_profile(conc=1.0)
    al = alpha(ch, pr)
    vmu = v_dual(ch, pr.mean())
    if e + al < vmu + 1e-9:
        continue                                   # not admissible at this (negative) accuracy
    cnt += 1
    try:
        best = max(best, r_primal(ch, pr, e, landscape="H", starts=2))
    except RuntimeError:
        pass
print(f"\n--- e = -0.25 a = {e:.5f} (negative): R^ = {R:.9f} (>= -e = {-e:.5f}); largest r_mu over {cnt} admissible random profiles: {best:.9f}")

# T3: collapse to additive instances on labelled profiles with a positive value
print("\n--- T3: V(mu, B; v) against max_gamma V(mu, B; gamma)  (B = e + alpha(mu)).  'V(v) >= V(gamma)' is trivial (v >= v_gamma);")
print("    equality is the collapse (Sion).  gamma0 is read off the exit type of the H-problem; the blind search can miss a small positive region.")
import itertools
free = [s.q - 1 for s in ch.sites]
offs = np.cumsum([0] + free)
ngrid = 9 if len(ch.sites) == 1 else 6
axes = []
for s in ch.sites:
    lo, hi = s.V.min(axis=0)[1:], s.V.max(axis=0)[1:]
    axes += [np.linspace(lo[i], hi[i], ngrid + 2)[1:-1] for i in range(s.q - 1)]
grid = [np.array(z) for z in itertools.product(*axes)]
grid = [z for z in grid if all(s.in_L(np.concatenate([[0.0], z[offs[j]: offs[j + 1]]]), tol=1e-12) for j, s in enumerate(ch.sites))]
worst_T3 = 0.0
blind = len(ch.sites) == 1 or (len(sys.argv) > 3 and sys.argv[3] == "blind")     # the blind search is slow for two site types
nT3 = 6
done = 0
tries = 0
prof0, _, _, _ = dip_profile(ch, ch.R(0.1 * E, return_t=True)[1])
while done < nT3 and tries < 200:
    tries += 1
    e = float(rng.choice([0.0, 0.1 * E, 0.3 * E]))
    pr = perturbed(prof0, 0.5) if tries % 2 else random_profile(kmax=3, conc=2.0)
    try:
        vH, nus, _, _ = r_primal(ch, pr, e, landscape="H", starts=2, full=True)
    except RuntimeError:
        continue
    if vH < 1e-4:
        continue
    B = e + alpha(ch, pr)
    # the additive instance selected by the exit type of the H-problem: gamma0 = argmax_gamma v_gamma(nubar*)
    gam0 = [s.v(P_ @ nu_)[1] for s, P_, nu_ in zip(ch.sites, pr.P, nus)]
    v0 = r_primal(ch, pr, e, landscape="add", gammas=gam0, starts=2, B=B)

    def negV(z):
        gam = [np.concatenate([[0.0], z[offs[j]: offs[j + 1]]]) for j in range(len(ch.sites))]
        if not all(s.in_L(g, tol=1e-12) for s, g in zip(ch.sites, gam)):
            return 1.0
        try:
            return -r_primal(ch, pr, e, landscape="add", gammas=gam, starts=1, B=B)
        except RuntimeError:
            return 1.0

    if blind:
        gv = np.array([negV(z) for z in grid])
        order = np.argsort(gv)[:2]
        best = 1.0
        for k in order:
            res = minimize(negV, grid[k], method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-12, "maxiter": 800})
            best = min(best, res.fun)
    else:
        best = float("nan")
    worst_T3 = max(worst_T3, abs(v0 - vH))
    done += 1
    print(f"    profile {done}: e = {e:.4f}, labels {[len(p) for p in pr.P]}: V(mu,B;v) = {vH:.9f}; V(mu,B;gamma0) at gamma0 = argmax v_gamma(exit type) = {v0:.9f}"
          f" (difference {vH - v0:+.1e}); blind search over gamma (grid of {len(grid)}, then Nelder-Mead): {-best:.9f}")
print(f"\nsummary {ch.name}: worst |primal - R| at mu* (T2): {worst_T2:.1e}; worst |collapse| (T3): {worst_T3:.1e}; time {time.time()-t00:.0f} s")
