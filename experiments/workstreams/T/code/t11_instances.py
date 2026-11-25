#!/usr/bin/env python3
"""t11 -- is the flat-histogram instance the hardest symmetric instance?  (Theorem T4 says yes; this is the numerical side.)
Dip exponents R_lam(e) (binary sup-min) for families of exit landscapes lam <= v of symmetric instances:
  add   : additive instances gamma|x|,  lam = -gamma*kappa - I*(-gamma);
  flat  : lam = min(v, c)  (the barrier flattened at height c; c = 0: zero residual, c = max v: H);
  roof  : lam = min(v, I(1/2) - s*u*|kappa - 1/2|) (instances that concentrate on the barrier top);
  rand  : lam = min(v, upward cones with random apices below v), renormalised to touch I   (fixed seed).
usage: python3 t11_instances.py bJ bB u e family
"""
import sys, time, math
import numpy as np
import tlib as T

bJ, bB, u, e = [float(x) for x in sys.argv[1:5]]
fam = sys.argv[5]
t0 = time.time()
K = T.Known(T.phi_cw(bJ, bB), u)
RH, argH = T.R_bin(K, e, K.v, nrand=2, ms=np.linspace(0.2, 0.8, 5))
print(f"bJ={bJ} bB={bB} u={u} e={e}: R_H = {RH:.7f} at {tuple(round(x,5) for x in argH)}   [{time.time()-t0:.0f}s]", flush=True)
Ib = float(K.I(0.5))
vmax = float(K.v(np.linspace(0, 1, 2001)).max())


def norm(lam):
    """shift a u-Lipschitz function below I so that it touches I"""
    c = float(np.min(K.Ig - lam(K.grid)))
    return (lambda kap: lam(kap) + c), c


cases = []
if fam == "add":
    for g in (0.0, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0):
        if g <= u:
            cases.append((f"gamma = {g:+.2f}", K.lam_additive(g)))
elif fam == "flat":
    for c in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0):
        cc = c * vmax
        cases.append((f"min(v, {c:.2f} max v)", (lambda cc_: (lambda kap: np.minimum(K.v(kap), cc_)))(cc)))
elif fam == "roof":
    for s in (0.25, 0.5, 0.75, 1.0):
        lam0 = (lambda s_: (lambda kap: np.minimum(K.v(kap), Ib - s_ * u * np.abs(np.asarray(kap, dtype=float) - 0.5))))(s)
        lam1, c = norm(lam0)
        cases.append((f"roof slope {s:.2f}u (shift {c:+.4f})", lam1))
else:
    rng = np.random.default_rng(5)
    for i in range(6):
        ks = rng.uniform(0.05, 0.95, 3)
        aps = K.v(ks) - rng.exponential(0.03, 3)
        lam0 = (lambda ks_, aps_: (lambda kap: np.minimum(K.v(kap), np.min(aps_[:, None] + u * np.abs(np.asarray(kap, dtype=float).ravel()[None, :] - ks_[:, None]), axis=0).reshape(np.shape(kap)))))(ks, aps)
        lam1, c = norm(lam0)
        cases.append((f"random cones at {np.round(ks,2)} depth {np.round(K.v(ks)-aps,3)}", lam1))

worst = -1.0
for name, lam in cases:
    # sanity: landscape below v, u-Lipschitz
    kg = np.linspace(0, 1, 4001)
    lv = lam(kg)
    assert np.all(lv <= K.v(kg) + 1e-9), name
    assert np.all(np.abs(np.diff(lv)) <= u * (kg[1] - kg[0]) + 1e-9), name
    R, arg = T.R_bin(K, e, lam, starts=[argH], nrand=1, ms=np.linspace(0.2, 0.8, 5))
    lams, mus = T.bin_blocks(*arg)
    Rf = T.obj_blocks(K, e, lam, lams, mus, ng=2001, zoom=6)
    worst = max(worst, Rf - RH)
    print(f"  {name:55s}: R = {Rf:.7f} at ({arg[0]:.4f},{arg[1]:.4f},{arg[2]:.4f});  R - R_H = {Rf-RH:+.2e}   [{time.time()-t0:.0f}s]", flush=True)
print(f"largest R_lam - R_H in family '{fam}': {worst:+.2e}   (time {time.time()-t0:.0f}s)")
