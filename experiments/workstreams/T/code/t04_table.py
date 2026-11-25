#!/usr/bin/env python3
"""t04 -- type-level exponents over a range of accuracies (both signs), any Curie-Weiss known part.
For every e:
  R_H(e)     = sup over binary centres (m,a,b) of V(mu, e + alpha(mu); v)             (dips of the flat-histogram instance)
  R_cone(e)  = max_m min{ MI : u rho + v - Lam_m <= e }                               (the brief's cone formula)
  R_0(e)     = the same sup-min with the exit landscape of the zero residual (lam = 0)
  S(e) = e + R_H(e);  non-adaptive side at X = S(e):
     n_mu*(X)       (robust, through r_mu)       -- equals R_H(e) iff the pair identity holds at the optimal profile
     theta_shell(X) (direct 2-d search, shell-cone around mu0 = mu*)   -- an independent computation of the same number
     theta_cone(X)  (cone around the centre of type m*, truncated)
usage: python3 t04_table.py bJ bB u e1,e2,...  [de]      (de = 1: also a differential-evolution cross-check of R_H)
"""
import sys, time, math
import numpy as np
import tlib as T

bJ, bB, u = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
es = [float(x) for x in sys.argv[4].split(",")]
do_de = len(sys.argv) > 5 and sys.argv[5] == "1"
t0 = time.time()
K = T.Known(T.phi_cw(bJ, bB), u)
print(f"Curie-Weiss bJ={bJ} bB={bB} u={u}: minima of I {[(round(x,5), round(v,6)) for x,v in K.minima]}, I(1/2)={float(K.I(0.5)):.6f}, contact set of v: {[(round(a,4),round(b,4)) for a,b in K.contact_pieces()]}")
print("      e        R_H(e)      (m, a, b) of the Gibbs shell      R_cone(e)   R_0(e)      S(e)        n_mu*(S)    shell(S)    cone(S)    | R_H - n_mu*   [s]")
prev = None
for e in es:
    starts = [prev] if prev is not None else []
    R, arg = T.R_bin(K, e, K.v, starts=starts, nrand=2, ms=np.linspace(0.2, 0.8, 5))
    lams, mus = T.bin_blocks(*arg)
    Rfine = T.obj_blocks(K, e, K.v, lams, mus, ng=2001, zoom=6)
    prev = arg
    Rc = T.R_cone(K, e, K.v) if e > -1e-12 else float("nan")
    R0, _ = T.R_bin(K, e, K.lam_zero(), nrand=1, ms=np.linspace(0.2, 0.8, 5)) if e > -1e-12 else (float("nan"), None)
    X = e + Rfine
    if X > 1e-9:
        nmu = T.n_mu(K, lams, mus, X, K.v)
        sh = T.theta_shell(K, lams, mus, X)
        co = T.theta_shell(K, np.array([arg[0], 1 - arg[0]]), np.array([1.0, 0.0]), X)
    else:
        nmu = sh = co = float("nan")
    line = (f"  {e:+.5f}   {Rfine:.7f}   ({arg[0]:.5f}, {arg[1]:.5f}, {arg[2]:.5f})   {Rc:.7f}   {R0:.7f}   {X:.7f}   {nmu:.7f}   {sh:.7f}   {co:.7f}"
            f"  | {Rfine - nmu:+.1e}   [{time.time()-t0:.0f}s]")
    if do_de:
        from scipy.optimize import differential_evolution
        f = lambda x: -T.obj_bin(K, e, K.v, x)
        res = differential_evolution(f, bounds=[(0.05, 0.95), (0.0, 0.6), (0.0, 0.6)], seed=7, maxiter=60, popsize=12, tol=1e-12,
                                     polish=False, init="sobol")
        line += f"   DE: {-res.fun:.7f} at ({res.x[0]:.4f},{res.x[1]:.4f},{res.x[2]:.4f})  [{time.time()-t0:.0f}s]"
    print(line, flush=True)
print(f"time {time.time()-t0:.0f}s")
