"""Theorem T9 for convex rate functions that are NOT of Curie-Weiss type (own code):
 (b) binary centres suffice (SLP with fixed mean + Nelder-Mead from random multi-atom starts);
 (d) is the cone formula equal to the sup-min over binary centres?  (the report: numerical, ten
     Curie-Weiss cases).
phi_1(k) = -1.5 (k-0.4)^2 + 0.8 k^4   (phi'' >= -3 > -4: I convex; phi neither concave nor convex)
phi_2(k) = 2 |k - 0.35|^1.5 + 0.5 k    (convex phi with a kink in phi'' ; I convex)
phi_3(k) = -1.9 (k-0.5)^2 + 0.3 sin(6k)/6  (phi'' in [-3.8-1.8, ...]: check convexity numerically)"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10slp import *
from r10tab import *
t0 = time.time()
rng = np.random.default_rng(11)
phis = [("phi1 = -1.5(k-0.4)^2 + 0.8k^4", lambda k: -1.5 * (k - 0.4) ** 2 + 0.8 * k ** 4),
        ("phi2 = 2|k-0.35|^1.5 + 0.5k", lambda k: 2.0 * np.abs(k - 0.35) ** 1.5 + 0.5 * k),
        ("phi3 = -1.2(k-0.5)^2 + 0.05 sin(6k)", lambda k: -1.2 * (k - 0.5) ** 2 + 0.05 * np.sin(6 * k))]
sel = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [0, 1, 2]
for pi_, (name, phi) in enumerate(phis):
    if pi_ not in sel:
        continue
    for u in (1.0, 2.0):
        M = Model(phi=phi, u=u, N=200001)
        kk = np.linspace(0.001, 0.999, 99801)
        d2 = np.gradient(np.gradient(M.I(kk), kk), kk)
        convex = bool(d2[5:-5].min() > -1e-3)
        Eu = float(np.log(np.cosh(u / 2)))
        for e in (0.0, 0.3 * Eu):
            starts = [(0.3, 0.3, 0.3), (0.5, 0.3, 0.3), (0.7, 0.3, 0.3), (0.5, 0.2, 0.35), (0.5, 0.35, 0.2)]
            Rb, lb, mb = R_binary(M, e, starts=starts)
            Rc, mc = R_cone(M, e, convex=True)
            best = -1.0
            nst = 0
            tcase = time.time()
            while time.time() - tcase < 35:
                k = int(rng.integers(3, 6))
                lam = rng.dirichlet(np.ones(k))
                mu = np.clip(float(lb @ mb) + 0.25 * rng.standard_normal(k), 0.02, 0.98)
                val, l1, m1, hist = slp(M, lam, mu, e, None)            # mean fixed in the LP
                l2, m2 = coarsen(l1, m1)
                if len(m2) <= 6:
                    v3, l3, m3 = nm(M, e, l2, m2, maxiter=1200)
                else:
                    v3, l3, m3 = val, l1, m1
                v3 = max(v3, val if np.isfinite(val) else -1)
                nst += 1
                if v3 > best:
                    best, bl, bm = v3, l3, m3
            print(f"{name}, u={u}, e={e:.4f}: I convex: {convex} (min I'' = {d2[5:-5].min():.3f});  binary sup-min {Rb:.9f} (m; a, b) = ({lb[0]:.4f}; {1-mb[0]:.4f}, {mb[1]:.4f});  cone formula {Rc:.9f} (m = {mc:.4f});  cone - binary = {Rc - Rb:+.2e};  best of {nst} multi-atom runs {best:.9f} (excess {best - Rb:+.2e})   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
