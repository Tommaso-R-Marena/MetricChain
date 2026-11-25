"""
t01_identity.py -- Theorem 11.99, first identity, by three independent routes, on the sites of the worked example
and on random sites (asymmetric envelopes included).

route 1: max over gamma in L of the LINEAR-PROGRAMMING value of the game (blind Nelder-Mead search) -- the definition
route 2: primal Renyi programme  max_M -t ln sum_a (sum_phi M pi_phi^t)^(1/t)
route 3: dual  min_Q max_phi (1-t) D_t(pi_phi||Q)  (epigraph programme, no M)
plus:    the LP value of the game AT the Renyi centre gamma* (must equal route 2), and gamma* in L.
"""
import sys, time
import numpy as np
from r5lib import *

np.set_printoptions(precision=6, suppress=True, linewidth=150)

def sites_example():
    path = Site([0.5, 0.3, 0.2], [[0, 0.8, 2.4], [0.8, 0, 1.6], [2.4, 1.6, 0]], "path")
    binr = Site([0.7, 0.3], [[0, 1], [1, 0]], "bin")
    tri = Site([0.2, 0.5, 0.3], [[0, 1, 2], [1, 0, 1.5], [2, 1.5, 0]], "tri")
    asym = Site([0.5, 0.3, 0.2], [[0, 1, 2], [0.5, 0, 1.5], [1, 0.5, 0]], "asym")
    return dict(bin=binr, path=path, tri=tri, asym=asym)


def random_site(rng, q, asym=True):
    """random quasi-metric by shortest-path closure of random nonnegative weights."""
    w = rng.uniform(0.2, 2.5, size=(q, q))
    if not asym:
        w = (w + w.T) / 2
    np.fill_diagonal(w, 0)
    for k in range(q):
        w = np.minimum(w, w[:, [k]] + w[[k], :])
    pi = rng.dirichlet(np.ones(q) * 2) * 0.9 + 0.1 / q
    pi /= pi.sum()
    return Site(pi, w, f"rand{q}")


if __name__ == "__main__":
    t0 = time.time()
    S = sites_example()
    print("== vertices of the Lipschitz polytopes (normalised phi[0]=0) ==")
    for nm, s in S.items():
        print(nm, "q=%d" % s.q, "#vertices=%d" % len(s.V))
        print(s.V)
    print()
    print("== identity F*(t): route1 (LP game, blind search over gamma) | route2 primal | route3 dual | LP at centre ==")
    worst = 0.0
    rows = []
    for nm, s in S.items():
        for t in (0.1, 0.3, 0.5, 0.7, 0.9):
            lo, M, hi = renyi_primal(s, t)
            dual, Qd = renyi_dual(s, t)
            Qc = centre_of(s, M, t)
            gstar = -np.log(Qc / s.pi)
            gstar -= gstar[0]
            okL = in_L(gstar, s.d)
            lp_at_centre = F_game(s, gstar, t)[0]
            blind, gb = Fstar_blind(s, t, n_starts=4, seed=1)
            dev = max(abs(lo - dual), abs(lo - lp_at_centre), hi - lo)
            worst = max(worst, dev)
            rows.append((nm, t, blind, lo, dual, lp_at_centre, hi - lo, okL, lo - blind))
            print(f"{nm:5s} t={t:.1f}  blind={blind:.10f}  primal={lo:.10f}  dual={dual:.10f}  LP@centre={lp_at_centre:.10f}"
                  f"  gap={hi-lo:.1e}  centre_in_L={okL}  primal-blind={lo-blind:+.2e}")
    print("largest |primal-dual|, |primal-LP@centre|, duality gap:", f"{worst:.2e}")
    print("blind search never exceeds the Renyi value:", all(r[8] > -1e-9 for r in rows),
          " largest shortfall of the blind search:", f"{max(r[8] for r in rows):.2e}")
    print()
    print("== random sites, asymmetric envelopes, q = 2,3,4 ==")
    rng = np.random.default_rng(20261125)
    worst = 0.0
    worst_blind_excess = -1.0
    nfail_L = 0
    ncases = 0
    for q in (2, 3, 4):
        for rep in range(8 if q < 4 else 4):
            s = random_site(rng, q, asym=True)
            for t in (0.15, 0.5, 0.85):
                lo, M, hi = renyi_primal(s, t)
                dual, Qd = renyi_dual(s, t)
                Qc = centre_of(s, M, t)
                gstar = -np.log(Qc / s.pi)
                okL = in_L(gstar, s.d, tol=1e-8)
                nfail_L += (not okL)
                lp = F_game(s, gstar, t)[0]
                blind, _ = Fstar_blind(s, t, n_starts=3, seed=rep)
                worst = max(worst, abs(lo - dual), abs(lo - lp), hi - lo)
                worst_blind_excess = max(worst_blind_excess, blind - lo)
                ncases += 1
    print(f"cases: {ncases};  largest deviation among (primal, dual, LP at centre, duality gap): {worst:.2e}")
    print(f"centres outside L: {nfail_L};  largest (blind - primal) [must be <= ~0]: {worst_blind_excess:+.2e}")
    print()
    print("== F(gamma,t) <= F*(t) also for gamma OUTSIDE L (the inequality needs only that pi_gamma is a probability) ==")
    exc = -1
    for nm, s in S.items():
        for t in (0.3, 0.6):
            lo = renyi_primal(s, t)[0]
            for k in range(200):
                g = rng.normal(size=s.q) * 3
                exc = max(exc, F_game(s, g, t)[0] - lo)
    print(f"largest F(gamma,t) - F*(t) over 1600 random gamma (unconstrained): {exc:+.3e}")
    print()
    print("== E_0(rho,M) (Gallager, raw definition) = rho * I_t^Sibson(M) = G_t(M)/t, t = 1/(1+rho) ==")
    dv = 0
    for nm, s in S.items():
        for rho in (0.25, 1.0, 3.0):
            M = rng.dirichlet(np.ones(len(s.V)))
            t = 1 / (1 + rho)
            dv = max(dv, abs(E0_gallager_raw(s, rho, M) - G_primal(s, M, t) / t))
    print(f"largest |E_0(rho,M) - G_t(M)/t|: {dv:.2e}")
    print(f"[{time.time()-t0:.1f} s]")
