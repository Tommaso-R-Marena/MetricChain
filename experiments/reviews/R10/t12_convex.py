"""Theorem T9 numerically (own code).
 A. T9(b): for convex I no multi-block profile beats the binary optimum (SLP + Nelder-Mead from
    random multi-atom starts); the remark: for an additive instance (here the zero residual) binary
    centres suffice also for a NON-convex I.
 B. T9(a): V(mu,B;v) = max_gamma V(mu,B;lambda_gamma) at random profiles (convex I).
 C. T9(e): r_mu(e) <= R_unif(e) for ferromagnets (one phase and two), random multi-block profiles,
    accuracies of both signs.
 D. T9(c): pair identity n_mu*(e + R_H(e)) = R_H(e), convexity and slopes of R_H (one convex case).
usage: python3 t12_convex.py [A|B|C|D] [seed]"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10slp import *
from r10tab import *
t0 = time.time()
which = sys.argv[1] if len(sys.argv) > 1 else "ABCD"
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
rng = np.random.default_rng(seed)
zero = lambda k: 0.0 * np.asarray(k, float)

def rand_profile(kmax=6):
    k = int(rng.integers(2, kmax + 1))
    lam = rng.dirichlet(np.ones(k))
    mode = int(rng.integers(0, 3))
    mu = rng.random(k) if mode == 0 else (np.clip(0.5 + 0.25 * rng.standard_normal(k), 0.02, 0.98) if mode == 1 else rng.beta(0.6, 0.6, size=k))
    return lam, mu

if "A" in which:
    cases = [("bJ=0.5 bB=0.3 (convex, ferro)", Model(0.5, 0.3, 1.0), None, True, 0.0),
             ("bJ=0.5 bB=0.3 (convex, ferro)", Model(0.5, 0.3, 1.0), None, True, 0.03),
             ("bJ=1.0 bB=0.1 (critical)", Model(1.0, 0.1, 1.0), None, True, 0.0),
             ("bJ=-2 bB=0.3 (antiferro; mean fixed in the LP)", Model(-2.0, 0.3, 1.0), None, False, 0.0),
             ("bJ=1.5 B=0, ZERO RESIDUAL (non-convex I, affine landscape)", Model(1.5, 0.0, 1.0), zero, True, 0.0)]
    sel = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else list(range(len(cases)))
    for ci, (name, M, land, ferro, e) in enumerate(cases):
        if ci not in sel:
            continue
        if land is not None:
            M.v = land                                # the SLP and r_mu use model.v as the landscape
        bJ, bB = M.bJ, M.bB
        phip = (lambda k: -2 * bJ * (2 * k - 1) - 2 * bB) if ferro else None
        Rb, lb, mb = R_binary(M, e, starts=[(0.5, 0.3, 0.3), (0.3, 0.25, 0.2), (0.7, 0.2, 0.3), (0.2, 0.2, 0.15), (0.85, 0.1, 0.4)])
        best = -1
        nst = 0
        tcase = time.time()
        while time.time() - tcase < 75:
            lam, mu = rand_profile()
            val, l1, m1, hist = slp(M, lam, mu, e, phip)
            l2, m2 = coarsen(l1, m1)
            if len(m2) <= 6:
                v3, l3, m3 = nm(M, e, l2, m2, maxiter=1200)
            else:
                v3, l3, m3 = val, l1, m1
            v3 = max(v3, val)
            nst += 1
            if v3 > best:
                best, bl, bm = v3, l3, m3
        print(f"A. {name}, e={e}: binary optimum {Rb:.9f} [{fmt(lb, mb)}]; best of {nst} multi-atom SLP+NM runs {best:.9f} [{fmt(bl, bm)}]; excess over binary {best - Rb:+.2e}   t={time.time()-t0:.0f}", flush=True)

if "B" in which:
    for (bJ, bB) in ((0.5, 0.3), (-1.0, 0.3), (1.0, 0.1)):
        M = Model(bJ, bB, 1.0)
        worst = 0.0
        for rep in range(6):
            lam, mu = rand_profile(4)
            B = alpha(M, lam, mu) + float(rng.choice([0.0, 0.01, -0.01]))
            if B < float(M.v(lam @ mu)):
                continue
            Vv = inner_clip(M, lam, mu, B)[0]
            f = lambda g: -inner_clip(M, lam, mu, B, land=landscape_gamma(M, g))[0]
            gs = np.linspace(-1, 1, 41)
            vals = [f(g) for g in gs]
            i = int(np.argmin(vals))
            rg = optimize.minimize_scalar(f, bounds=(gs[max(i - 1, 0)], gs[min(i + 1, 40)]), method='bounded', options={'xatol': 1e-7})
            Vg = max(-rg.fun, -vals[i])
            worst = max(worst, abs(Vv - Vg))
        print(f"B. T9(a) bJ={bJ} bB={bB}: max |V(mu,B;v) - max_gamma V(mu,B;lambda_gamma)| over random profiles = {worst:.2e}   t={time.time()-t0:.0f}", flush=True)

if "C" in which:
    for (bJ, bB, u) in ((0.5, 0.0, 1.0), (0.8, 0.2, 1.0), (1.5, 0.0, 1.0), (1.5, 0.05, 1.0), (2.5, 0.0, 1.0), (1.3, 0.0, 0.4), (3.0, 0.0, 3.0)):
        M = Model(bJ, bB, u, N=200001)
        worst = -np.inf; n = 0
        for rep in range(120):
            lam, mu = rand_profile(5)
            e = float(rng.choice([0.0, 0.3, -0.5, 0.7])) * float(np.log(np.cosh(u / 2)))
            val = r_mu(M, lam, mu, e)
            if not np.isfinite(val):
                continue
            n += 1
            worst = max(worst, val - max(R_unif(e, u), -e))
        # also the locally optimised binary profile
        Rb, lb, mb = R_binary(M, 0.0)
        print(f"C. T9(e) bJ={bJ} bB={bB} u={u}: {n} random profiles, max[r_mu(e) - Rhat_unif(e)] = {worst:+.3e};  binary optimum at e=0: {Rb:.7f} <= R_unif(0) = {R_unif(0.0,u):.7f}: {Rb <= R_unif(0.0,u) + 1e-9}   t={time.time()-t0:.0f}", flush=True)

if "D" in which:
    M = Model(0.5, 0.3, 1.0)
    es = np.array([-0.04, -0.02, -0.01, 0.0, 0.01, 0.02, 0.04, 0.06])
    R = []
    st = None
    for e in es:
        Rb, lb, mb = R_binary(M, e, starts=st)
        nmu, emax = n_mu(M, lb, mb, e + Rb)
        R.append(Rb)
        st = [(lb[0], 1 - mb[0], mb[1])]
        print(f"D. bJ=0.5 bB=0.3 e={e:+.3f}: R_H {Rb:.8f}  n_mu*(e+R_H) {nmu:.8f}  difference {nmu - Rb:+.1e}", flush=True)
    R = np.array(R)
    sl = np.diff(R) / np.diff(es)
    print("D. slopes of R_H between the grid points:", np.round(sl, 4), " (convex: slopes nondecreasing:", bool(np.all(np.diff(sl) > -1e-6)), "; in [-1,0]:", bool(np.all((sl >= -1) & (sl <= 0))), ")")
print("time", time.time() - t0)
