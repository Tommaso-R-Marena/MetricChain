# R9 test 14: (i) 1 <= Z_H <= n+1 and mu_H on type classes; (ii) the fields of HintPair for (theta_na, R^max, a, h, E)
# on grids; (iii) the sanity check of item 14 of the brief: the every-n lower bound at gamma*|x| against e^{n R_0}.
import numpy as np, time
from math import log, exp
from r9lib import Par
from r9prof import Grid
t0 = time.time()
print("(i) ln Z_H and the largest / smallest mu_H(T_kappa)(n+1) over the types of the window")
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.5, 1.0), (0.9, 3.0)]:
    P = Par(p, u)
    for n in (10, 100, 1000):
        gr = Grid(P, (n // 2, n - n // 2)); tt = np.arange(n + 1.0)
        lw = gr.logT + tt * log(P.p) + (n - tt) * log(P.q) - gr.psiH_t - gr.lnZH      # ln mu_H(T_t)
        win = (tt / n >= P.kminus) & (tt / n <= P.kplus)
        ok = 0 <= gr.lnZH <= log(n + 1) + 1e-12
        print(f"   p={p} u={u} n={n}: ln Z_H = {gr.lnZH:.4f} (ln(n+1) = {log(n+1):.4f}) ok={ok}; mu_H(T) (n+1) in the window: min {np.exp(lw[win]).min()*(n+1):.3f}, max {np.exp(lw[win]).max()*(n+1):.3f}; mass of the window: {np.exp(lw[win]).sum():.4f}")
print("(ii) HintPair fields on grids")
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.5, 1.0), (0.05, 2.0), (0.2, 4.0), (0.8, 0.5)]:
    P = Par(p, u); E = P.E()[0]; a = -P.ec(); ts, Fs, _ = P.table()
    es = np.linspace(-1.5 * a, 1.2 * E, 4001)
    R = np.maximum((Fs[None, :] - ts[None, :] * es[:, None]).max(axis=1), np.maximum(0.0, -es))
    slopes = np.diff(R) / np.diff(es); S = es + R
    hval = P.Rmax(0.0)
    conv = np.min(np.diff(slopes)); smin, smax = slopes.min(), slopes.max()
    Smono = np.min(np.diff(S)); zero_from_E = np.max(np.abs(R[es >= E])); pos_below = np.min(R[es < E - 1e-3])
    eq_left = np.max(np.abs(R[es <= -a] + es[es <= -a]))
    xs = np.linspace(1e-4, 1.3 * E, 300); tn = np.array([P.theta_na(x) for x in xs])
    ident = max(abs(P.theta_na(e + P.Rmax(e)) - P.Rmax(e)) for e in np.linspace(1e-4, E - 1e-4, 40))
    lower = min(P.Rmax(e) - (hval - e) for e in np.linspace(1e-4, E - 1e-4, 40))
    print(f"   p={p} u={u}: slopes of R^max in [{smin:.4f}, {smax:.4f}], min second difference {conv:.1e}; S nondecreasing (min increment {Smono:.1e}); R^max = 0 beyond E ({zero_from_E:.1e}), > 0 below ({pos_below:.1e}); R^max(e) = -e for e <= -a ({eq_left:.1e}); "
          f"theta_na nonincreasing ({np.max(np.diff(tn)):.1e}), <= a ({tn.max() - a:.1e}), max jump {np.max(np.abs(np.diff(tn))):.1e}; theta_na(h) - h = {P.theta_na(hval) - hval:.1e}; ident {ident:.1e}; min[R^max(e) - (h - e)] = {lower:.1e}")
print("(iii) every-n lower bound at gamma*|x| (Theorem F1(a): E|Q| >= (1-2 delta) exp(n [F(gamma*,t*) - t* eps1])) against exp(n R_0)")
for (p, u, f) in [(0.1, 2.0, 0.3), (0.3, 1.0, 0.3), (0.2, 4.0, 0.3), (0.05, 2.0, 0.1)]:
    P = Par(p, u); e1 = f * P.E()[0]; Rm, tst, gst = P.Rmax(e1, True); R0 = P.R0(e1)
    chk = float(P.F(gst, tst)) - tst * e1
    n0 = log(2.0) / (Rm - R0)
    print(f"   p={p} u={u} eps1={f}E: R^max = {Rm:.6f} = F(gamma*,t*) - t* eps1 = {chk:.6f} at gamma* = {gst:+.4f}, t* = {tst:.4f} (game value by LP: {P.F_game(gst, tst) - tst*e1:.6f}); R_0 = {R0:.6f}; "
          f"the bound exceeds e^(n R_0) for n > ln(1/(1-2 delta))/(R^max - R_0) = {n0:.0f} (delta = 1/4)")
print(f"[{time.time()-t0:.0f}s]")
