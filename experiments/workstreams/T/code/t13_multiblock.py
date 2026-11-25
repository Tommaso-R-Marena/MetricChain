#!/usr/bin/env python3
"""t13 -- beyond binary centres (symmetric case B = 0): structured searches over block profiles, i.e. over the law rho of the
block types mu_U on [0,1].
  S2 : two atoms {1-x, x}, weights 1/2                                      (the binary centre; 1 parameter)
  S3 : {1-x, 1/2, x} with a 'free' block of weight lf at 1/2                 (2 parameters)
  S4 : {1-x, 1/2+d, 1/2-d, x}, the middle pair of total weight lf            (3 parameters)
  S5 : {1-x, 1-y, 1/2, y, x}, weights (l1, l2, lf, l2, l1)                    (4 parameters)
  S6 : {1-x, 1-y, 1-z, z, y, x}, weights (l1, l2, l3, l3, l2, l1)             (5 parameters)
  G3, G4, G5 : general (asymmetric) profiles with 3, 4, 5 blocks, Nelder-Mead from the symmetric optimum, perturbed
Every value is re-evaluated with the fine inner solver (ng = 2001).  For the best profile: the two/three tied exits and the
pair identity residual n_mu(e + R) - R.
usage: python3 t13_multiblock.py bJ u e1,e2,... [full]
"""
import sys, time, math
import numpy as np
from scipy.optimize import minimize
import tlib as T

bJ, u = float(sys.argv[1]), float(sys.argv[2])
es = [float(x) for x in sys.argv[3].split(",")]
full = len(sys.argv) > 4 and sys.argv[4] == "full"
t0 = time.time()
K = T.Known(T.phi_cw(bJ, 0.0), u)
rng = np.random.default_rng(31)
print(f"Curie-Weiss bJ={bJ} B=0 u={u}; contact set {[(round(a,4),round(b,4)) for a,b in K.contact_pieces()]}")


def prof(kind, p):
    if kind == "S2":
        x, = p
        return np.array([0.5, 0.5]), np.array([1 - x, x])
    if kind == "S3":
        lf, x = p
        l = (1 - lf) / 2
        return np.array([l, lf, l]), np.array([1 - x, 0.5, x])
    if kind == "S4":
        lf, x, d = p
        l = (1 - lf) / 2
        return np.array([l, lf / 2, lf / 2, l]), np.array([1 - x, 0.5 + d, 0.5 - d, x])
    if kind == "S5":
        l2, lf, x, y = p
        l1 = (1 - lf - 2 * l2) / 2
        return np.array([l1, l2, lf, l2, l1]), np.array([1 - x, 1 - y, 0.5, y, x])
    if kind == "S6":
        l2, l3, x, y, z = p
        l1 = 0.5 - l2 - l3
        return np.array([l1, l2, l3, l3, l2, l1]), np.array([1 - x, 1 - y, 1 - z, z, y, x])
    raise ValueError(kind)


def ok(lams, mus):
    return lams.min() > 1e-5 and mus.min() >= 0 and mus.max() <= 1


def nm(f, x0, step=0.02, it=1500):
    x0 = np.array(x0, dtype=float)
    sim = [x0] + [x0 + step * np.eye(len(x0))[i] * (1 if x0[i] < 0.5 else -1) for i in range(len(x0))]
    r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-13, "maxiter": it, "initial_simplex": np.array(sim)})
    sim = [r.x] + [r.x + 0.2 * step * np.eye(len(x0))[i] for i in range(len(x0))]
    r = minimize(f, r.x, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-14, "maxiter": it, "initial_simplex": np.array(sim)})
    return r.x, -r.fun


def gen_pack(lams, mus):
    return np.r_[np.log(lams[:-1] / lams[-1]), mus]


def gen_unpack(z, k):
    w = np.r_[z[:k - 1], 0.0]
    w = np.exp(w - w.max())
    return w / w.sum(), np.asarray(z[k - 1:], dtype=float)


for e in es:
    def fS(kind):
        def f(p):
            lams, mus = prof(kind, p)
            if not ok(lams, mus):
                return 0.0
            return -T.obj_blocks(K, e, K.v, lams, mus)
        return f

    def fine(lams, mus):
        return T.obj_blocks(K, e, K.v, lams, mus, ng=2001, zoom=6)

    res = {}
    p2, _ = nm(fS("S2"), [0.3])
    res["S2"] = (fine(*prof("S2", p2)), prof("S2", p2), p2)
    best3 = (-1, None)
    for lf0 in (0.05, 0.15, 0.3):
        p3, v3 = nm(fS("S3"), [lf0, p2[0] - 0.01])
        if v3 > best3[0]:
            best3 = (v3, p3)
    p3 = best3[1]
    res["S3"] = (fine(*prof("S3", p3)), prof("S3", p3), p3)
    p4, _ = nm(fS("S4"), [p3[0], p3[1], 0.06])
    res["S4"] = (fine(*prof("S4", p4)), prof("S4", p4), p4)
    p5, _ = nm(fS("S5"), [0.1, max(p3[0] - 0.05, 0.02), p3[1] - 0.02, p3[1] + 0.08])
    res["S5"] = (fine(*prof("S5", p5)), prof("S5", p5), p5)
    lf4, x4, d4 = p4
    best6 = (-1, None)
    for (l2_0, y0) in ((0.08, x4 + 0.06), (0.15, 0.5 * (x4 + 0.5 - d4))):
        p6, v6 = nm(fS("S6"), [l2_0, max(lf4 / 2, 0.03), x4 - 0.01, y0, 0.5 - max(d4, 0.03)])
        if v6 > best6[0]:
            best6 = (v6, p6)
    p6 = best6[1]
    res["S6"] = (fine(*prof("S6", p6)), prof("S6", p6), p6)
    print(f"\ne = {e:+.4f}   [{time.time()-t0:.0f}s]")
    for kname in ("S2", "S3", "S4", "S5", "S6"):
        v, (lams, mus), p = res[kname]
        print(f"  {kname}: R = {v:.8f}   lams {np.round(lams,4)}  mus {np.round(mus,4)}")
    if full:
        for kname, k in (("S3", 3), ("S4", 4), ("S5", 5)):
            v, (lams, mus), p = res[kname]
            bestg = (v, lams, mus)
            for trial in range(2):
                z0 = gen_pack(lams, np.clip(mus + rng.normal(0, 0.015, k), 0.01, 0.99))
                def fg(z):
                    l_, m_ = gen_unpack(z, k)
                    if not ok(l_, m_):
                        return 0.0
                    return -T.obj_blocks(K, e, K.v, l_, m_)
                zz, _ = nm(fg, z0, step=0.03, it=2500)
                l_, m_ = gen_unpack(zz, k)
                vg = fine(l_, m_)
                if vg > bestg[0]:
                    bestg = (vg, l_, m_)
            print(f"  G{k} (general, from {kname}): R = {bestg[0]:.8f}   lams {np.round(bestg[1],4)}  mus {np.round(bestg[2],4)}   [{time.time()-t0:.0f}s]", flush=True)
            res[f"G{k}"] = (bestg[0], (bestg[1], bestg[2]), None)
    # best profile: exits and pair identity
    kbest = max(res, key=lambda q: res[q][0])
    v, (lams, mus), p = res[kbest]
    B = e + T.alpha_blocks(K, lams, mus)
    # all local minima along the boundary curve (tied exits)
    Vv, (cl, ch) = T.V_clip(K, lams, mus, B, K.v, ng=2001, zoom=6, full=True)
    nu = np.minimum(np.maximum(mus, cl), ch)
    X = e + v
    nmu = T.n_mu(K, lams, mus, X, K.v) if X > 1e-9 else float("nan")
    print(f"  best: {kbest}, R = {v:.8f}; gain over the binary centre {v - res['S2'][0]:+.2e} ({100*(v/max(res['S2'][0],1e-300)-1):+.2f} %); "
          f"one optimal exit: clip to [{cl:.4f}, {ch:.4f}] -> types {np.round(nu,4)}, kappa' = {float(lams@nu):.4f};"
          f" pair identity n_mu(e+R) - R = {nmu - v:+.1e}   [{time.time()-t0:.0f}s]", flush=True)
print(f"time {time.time()-t0:.0f}s")
