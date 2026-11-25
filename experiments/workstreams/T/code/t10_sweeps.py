#!/usr/bin/env python3
"""t10 -- two sweeps for the two-phase case (Curie-Weiss, B = 0 unless given):
 mode J: the coupling bJ through the critical value 1 at fixed u, accuracy e  (do the two-phase exponents join the convex ones?)
 mode U: the Lipschitz constant u through the slopes of the barrier at fixed bJ  (the window {v = I} breaks into pieces)
For every point: R_H(e) (binary sup-min) with its Gibbs shell, the uniform-cube value, the cone formula, the pair identity
residual n_mu*(e + R_H) - R_H, and a_sym = MI of the smallest globally self-consistent symmetric shell (1/2, x, x)
(a lower bound for a = theta_na(0+); the uniform cube has a = KL(p_u || 1/2)).
usage: python3 t10_sweeps.py J u e bJ1,bJ2,...  [bB]      |      python3 t10_sweeps.py U bJ e u1,u2,... [bB]
"""
import sys, time, math
import numpy as np
import tlib as T

last_sym = ""

mode = sys.argv[1]
t0 = time.time()
bB = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0


def unif(u, e):
    Lam1 = math.log(2 / (1 + math.exp(-u)))
    rho = (Lam1 + e) / u
    return T.kl1(rho, 0.5) if rho < 0.5 else 0.0


def a_sym(K):
    """smallest x >= p_u such that the shell (1/2, x, x) is its own Gibbs shell (V(mu) = alpha(mu)); returns (x, MI)"""
    pu = 1 / (1 + math.exp(K.u))
    lams = np.array([0.5, 0.5])
    def gap(x):
        mus = np.array([1 - x, x])
        return T.alpha_blocks(K, lams, mus) - T.cone_free_energy(K, lams, mus, G=301, zoom=5)
    xs = np.linspace(pu + 1e-6, 0.499, 60)
    g = np.array([gap(x) for x in xs])
    ok = g < 1e-10
    if not ok.any():
        return float("nan"), float("nan")
    i = int(np.argmax(ok))
    if i > 0:
        lo, hi = xs[i - 1], xs[i]
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if gap(mid) < 1e-10:
                hi = mid
            else:
                lo = mid
        x = hi
    else:
        x = xs[0]
    return float(x), float(T.MI_blocks(lams, np.array([1 - x, x])))


def one(bJ, u, e):
    K = T.Known(T.phi_cw(bJ, bB), u)
    R, arg = T.R_bin(K, e, K.v, nrand=2, ms=np.linspace(0.2, 0.8, 5))
    lams, mus = T.bin_blocks(*arg)
    Rf = T.obj_blocks(K, e, K.v, lams, mus, ng=2001, zoom=6)
    Rc = T.R_cone(K, e, K.v)
    X = e + Rf
    nmu = T.n_mu(K, lams, mus, X, K.v) if X > 1e-9 else float("nan")
    xs, asy = a_sym(K) if abs(bB) < 1e-12 else (float("nan"), float("nan"))
    pieces = [(round(a, 4), round(b, 4)) for a, b in K.contact_pieces()]
    global last_sym
    last_sym = ""
    if abs(bB) < 1e-12:
        rs = T.R_sym(K, e, K.v, kinds=("S2", "S3", "S4"))
        k = max(rs, key=lambda q: rs[q][0])
        last_sym = (f"   | symmetric profiles: S2 {rs['S2'][0]:.7f}  S3 {rs['S3'][0]:.7f}  S4 {rs['S4'][0]:.7f};"
                    f" best {k}: lams {np.round(rs[k][1],3)} mus {np.round(rs[k][2],3)}")
    return K, Rf, arg, Rc, nmu, xs, asy, pieces


if mode == "J":
    u, e = float(sys.argv[2]), float(sys.argv[3])
    Ru = unif(u, e)
    pu = 1 / (1 + math.exp(u))
    rho = (math.log(2 / (1 + math.exp(-u))) + e) / u
    bJstar = 1 + u * (-2 + 1 / (2 * rho * (1 - rho))) / (2 * math.log((1 - rho) / rho))
    print(f"sweep in bJ at u={u}, e={e}, bB={bB}; uniform cube: R = {Ru:.7f}, a = {T.kl1(pu, 0.5):.6f};  local stability of the symmetric exit up to bJ* = {bJstar:.4f}")
    print("   bJ     I(1/2)-min I  R_H(e)      R_H/R_unif   Gibbs shell (m,a,b)            R_cone      pair resid.  a_sym (x)            contact set   [s]")
    for bJ in [float(x) for x in sys.argv[4].split(",")]:
        K, Rf, arg, Rc, nmu, xs, asy, pieces = one(bJ, u, e)
        Ib = float(K.I(0.5))
        print(f"  {bJ:.3f}  {Ib:.6f}      {Rf:.7f}   {Rf/Ru:.5f}      ({arg[0]:.4f},{arg[1]:.4f},{arg[2]:.4f})   {Rc:.7f}   {nmu-Rf:+.1e}     {asy:.6f} ({xs:.4f})   {pieces}   [{time.time()-t0:.0f}s]{last_sym}", flush=True)
else:
    bJ, e_rel = float(sys.argv[2]), float(sys.argv[3])
    print(f"sweep in u at bJ={bJ}, bB={bB}; accuracy e = {e_rel} * (uniform-cube threshold ln cosh(u/2))")
    K0 = T.Known(T.phi_cw(bJ, bB), 1.0)
    kg = K0.grid[1:-1]
    dI = np.gradient(K0.Ig, K0.grid)[1:-1]
    kw = min(x for x, _ in K0.minima)
    sel = (kg > kw) & (kg < 0.5)
    print(f"   barrier: I(1/2) = {float(K0.I(0.5)):.6f}, well at {kw:.5f}; largest slope of I on the barrier = {dI[sel].max():.5f}; mean slope = {float(K0.I(0.5))/(0.5-kw):.5f}")
    print("   u      e          R_H(e)       R_unif(e)    ratio     Gibbs shell (m,a,b)           R_cone       pair resid.  a_sym (x) / a_unif            contact set   [s]")
    for u in [float(x) for x in sys.argv[4].split(",")]:
        e = e_rel * math.log(math.cosh(u / 2))
        K, Rf, arg, Rc, nmu, xs, asy, pieces = one(bJ, u, e)
        Ru = unif(u, e)
        pu = 1 / (1 + math.exp(u))
        print(f"  {u:.3f}  {e:.6f}   {Rf:.8f}   {Ru:.8f}   {Rf/Ru:.5f}   ({arg[0]:.4f},{arg[1]:.4f},{arg[2]:.4f})   {Rc:.8f}   {nmu-Rf:+.1e}    {asy:.6f} ({xs:.4f}) / {T.kl1(pu,0.5):.6f}   {pieces}   [{time.time()-t0:.0f}s]{last_sym}", flush=True)
print(f"time {time.time()-t0:.0f}s")
