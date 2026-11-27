#!/usr/bin/env python3
"""a6_05_a9a.py [u]  --  section A9a of Z_ADDENDUM.md (Lemma A9', Proposition A11', the observation A8') in numbers.
FLOATING POINT; the referee's own code (a6lib.py).

 (A) the constants of Lemma A9': the largest r_0 with J(t) <= h - (L - t)^2/(4 vth) on [L - r_0, L], eta_0;
 (B) Lemma A9': the chain  J'(t_1(B)) >= J'(t_1(h - eta)) >= eta/(L - t_1(h - eta)) >= (1/2) sqrt(eta/vth),
     the contraction factor kappa(B) <= mu_eta, the orbits  0 <= t_1 - p_i <= t_1 mu_eta^i;  how conservative;
 (C) Proposition A11': g_0 for this pair, eta_g, the two conditions that define k_2(g), k_2(g) against C_3/g,
     the inequality  M_k(g) <= theta_hint(g) + g (1 + g/(48h))^-(k - k_2)  for k >= k_2,  and how conservative the
     geometric factor and the offset are (true decay per level; levels needed for n (M_k - theta_hint) <= 1);
 (D) the observation A8':  sup_g [M_k(g) - theta_hint(g)] = b_k - h,  its dual form, and the inequality that the
     'obvious induction' would need.
The envelope sequence is computed in two ways that err in opposite directions ('grid': tops and majorants err
downwards; 'lines': upwards).
"""
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a6lib as L                                               # noqa: E402

u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 450
t00 = time.time()
P = L.Cube(u)
a, h, Lm, vth = P.a, P.h, P.L, P.vth
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


print("# cube, u = %g:  a = %.12f, h = %.12f, L = %.9f, vth = theta_hint''(0) = -1/J''(L) = %.9f, eps* = %.9f, c_*^2 = %.9f" % (u, a, h, Lm, vth, P.eps, P.cs2))

# ------------------------------------------------------------------------------------------------------------
print("(A) Lemma A9': r_0 and eta_0")
t = np.linspace(0.0, Lm, 2000001)
D = h - (Lm - t) ** 2 / (4 * vth) - P.J(t)                     # >= 0 where J(t) <= h - (L - t)^2/(4 vth)
bad = np.nonzero(D < -1e-15)[0]
if len(bad) == 0:
    r0 = Lm
    print("    J(t) <= h - (L - t)^2/(4 vth) holds on ALL of [0, L] (least slack %.3e at t = %.4f): r_0 = L, and eta_0 may be any number below h" % (float(D[:-1000].min()), float(t[int(np.argmin(D[:-1000]))])))
    eta0 = h * (1 - 1e-9)
else:
    r0 = Lm - float(t[bad[-1] + 1])
    eta0 = h - float(P.J(Lm - r0))
    print("    r_0 = %.6f (the inequality fails at t = %.6f), eta_0 = h - J(L - r_0) = %.6e = %.4f h" % (r0, float(t[bad[-1]]), eta0, eta0 / h))
q = (Lm - t[:-1]) ** 2
print("    (h - J(t))/((L - t)^2/(2 vth)) at L - t = 1e-3, 1e-2, 0.1, 0.3, L: %s   (-> 1 as t -> L: (H1))" % ", ".join(
    "%.5f" % float((h - P.J(Lm - d)) / (d * d / (2 * vth))) for d in (1e-3, 1e-2, 0.1, 0.3, Lm)))
check("(H1) for this pair: the ratio tends to one, and stays above 1/2 on [L - r_0, L]", abs(float((h - P.J(Lm - 1e-3)) / (1e-6 / (2 * vth))) - 1) < 2e-3)

# ------------------------------------------------------------------------------------------------------------
print("(B) Lemma A9'")


def kappa(B):
    """the subgradient theta(e_1)/e_1 of s -> Sigma(B, s) at its fixed point t_1(B): 1 - J'/(B + (1 - t_1) J')"""
    t1 = P.t1(B)
    j1 = P.J1(t1)
    return 1.0 - j1 / (B + (1.0 - t1) * j1), t1, j1


okB = True
print("       eta/h      L - t1(h-eta)   2 sqrt(vth eta)   J'(t1(h-eta))   eta/(L-t1)   sqrt(eta/vth)/2   kappa(h-eta)   mu_eta    (1-kappa)/(1-mu)   max_i,B [t1 - p_i - t1 mu^i]")
for fr in (0.9, 0.5, 0.2, 0.05, 1e-2, 1e-3, 1e-4, 1e-6):
    eta = fr * h
    if eta > eta0:
        continue
    mu = h / (h + 0.5 * math.sqrt(eta / vth))
    kt, t1t, j1t = kappa(np.array([h - eta]))
    kt, t1t, j1t = float(kt[0]), float(t1t[0]), float(j1t[0])
    chain = (Lm - t1t <= 2 * math.sqrt(vth * eta) * (1 + 1e-12)) and (j1t >= eta / (Lm - t1t) * (1 - 1e-9)) and (eta / (Lm - t1t) >= 0.5 * math.sqrt(eta / vth) * (1 - 1e-12))
    Bs = np.concatenate([np.linspace(0.0, h - eta, 40), (h - eta) * (1 - np.geomspace(1e-9, 0.5, 10))])
    kB, t1B, j1B = kappa(Bs)
    mono = bool(np.all(j1B >= j1t * (1 - 1e-9))) and bool(np.all(kB[1:] <= mu + 1e-13))
    # orbits
    p = np.zeros(Bs.shape)
    worst = -math.inf
    for i in range(0, 400):
        worst = max(worst, float(np.max(t1B - p - t1B * mu ** i)))
        if np.any(p > t1B + 1e-12):
            okB = False
        p = P.sigma(Bs, p)
    okB &= chain and mono and worst <= 1e-12
    print("    %9.2e   %.6e   %.6e    %.6e   %.6e   %.6e    %.8f   %.8f   %8.3f          %+.2e" % (
        fr, Lm - t1t, 2 * math.sqrt(vth * eta), j1t, eta / (Lm - t1t), 0.5 * math.sqrt(eta / vth), kt, mu, (1 - kt) / (1 - mu), worst))
check("the chain of inequalities, kappa(B) <= mu_eta for all B <= h - eta, and 0 <= t_1 - p_i <= t_1 mu_eta^i (i < 400, 50 intercepts per eta)", okB)
print("    (1 - kappa)/(1 - mu) -> 2 sqrt 2 = 2.828 as eta -> 0: the contraction is 1 - sqrt(2 eta/vth)/h, the lemma has 1 - sqrt(eta/vth)/(2h))")

# ------------------------------------------------------------------------------------------------------------
print("(C) Proposition A11'")
gg = np.geomspace(1e-6 * h, 60 * h, 400001)
m = P.theta_hint(gg) - (h - Lm * gg)
c1 = m >= vth * gg ** 2 / 4
c2 = vth * gg ** 2 / 576 <= eta0
c3 = gg <= 48 * h
allc = c1 & c2 & c3
g0 = float(gg[np.argmin(allc)]) if not allc.all() else float(gg[-1])
print("    m(g)/(vth g^2/2) at g = 1e-3h, 0.1h, h, 2h, eps*: %s" % ", ".join("%.4f" % float((P.theta_hint(x) - (h - Lm * x)) / (vth * x * x / 2)) for x in (1e-3 * h, 0.1 * h, h, 2 * h, P.eps)))
print("    the three conditions on g_0 hold on (0, g_0] with g_0 = %.5f = %.3f h = %.3f eps*   (first to fail: %s)" % (
    g0, g0 / h, g0 / P.eps, "m(g) >= vth g^2/4" if not c1.all() and gg[np.argmin(c1)] <= g0 * 1.0001 else ("eta_g <= eta_0" if not c2.all() and gg[np.argmin(c2)] <= g0 * 1.0001 else "g <= 48 h")))
check("g_0 >= eps*: Proposition A11' applies at every rate at which theta_hint > 0 (this pair)" if g0 >= P.eps else "g_0 < eps* (noted)", True)

# the envelope sequence, both ways, with the majorant at the test rates recorded at every level
rates = [r * h for r in (2.0, 1.0, 0.5, 0.25) if r * h <= g0]
KF = 6000
print("    computing the envelope sequence to %d levels, both ways (K = %d, refined) ..." % (KMAX, KF), flush=True)
V = L.LCurve([], [], a)
ltop, lM = [a], [V.M(np.array(rates))]
keepL = {}
Bt = [0.0]                                                      # where the cap line leaves the curve (tangency point B_t(k))
for j in range(1, KMAX + 1):
    V = L.lines_step(P, V, KF, refine=300)
    ltop.append(V.c)
    lM.append(V.M(np.array(rates)))
    Bt.append(float(V.X[-1]) if (len(V.al) and V.al[-1] * V.c - V.be[-1] > 1 - 1e-9) else float("nan"))
    if j in (2, 3, 5, 8, 12, 20, 40, 60):
        keepL[j] = V
gtop, gcur = L.grid_sequence(P, KMAX, KF, keep={2, 3, 5, 8, 12, 20, 40, 60} | set(range(1, KMAX + 1)), refine=300)
gM = [L.grid_M(gcur[j][0], gcur[j][1], np.array(rates)) for j in range(0, KMAX + 1)]
ltop, gtop = np.array(ltop), np.array(gtop)
lM, gM = np.array(lM), np.array(gM)
print("    ... %.0f s;   bracket of b_k - h at k = 10, 100, %d:  [%.6e, %.6e], [%.6e, %.6e], [%.6e, %.6e]" % (
    time.time() - t00, KMAX, gtop[10] - h, ltop[10] - h, gtop[100] - h, ltop[100] - h, gtop[KMAX] - h, ltop[KMAX] - h))
ks = np.arange(len(ltop))
print("    sup_k k^2 (b_k - h)/c_*^2 over 1 <= k <= %d: %.4f (at k = %d)   [this is C''/c_*^2 of Proposition A7 as far as computed]" % (
    KMAX, float(np.max(ks[1:] ** 2 * (ltop[1:] - h) / P.cs2)), int(np.argmax(ks[1:] ** 2 * (ltop[1:] - h) / P.cs2)) + 1))

# the coordinator's certified tops far out (stored output of the run to 400 levels, u = 1) against this bracket
if u == 1.0:
    import re
    far = {}
    for line in open(os.path.join(os.path.dirname(HERE), "out_z6_certified_u1_J400.txt")):
        mm = re.match(r"\s*(\d+) \| ([0-9.]+) \| ([0-9.]+) \|", line)
        if mm:
            far[int(mm.group(1))] = float(mm.group(2))
    ks_far = [k for k in (50, 100, 200, 300, 400) if k in far and k <= KMAX]
    print("    the coordinator's certified c_k (run to 400 levels, K = 4000) against the bracket [grid, lines] of b_k, as k^2 (. - h)/c_*^2:")
    for k in ks_far:
        print("      k = %3d:  bracket [%.5f, %.5f]   certified %.5f" % (k, k * k * (gtop[k] - h) / P.cs2, k * k * (ltop[k] - h) / P.cs2, k * k * (far[k] - h) / P.cs2))
    check("the coordinator's certified tops at k = %s are above the floating-point lower bracket of the envelope tops" % ks_far,
          all(far[k] >= gtop[k] - 5e-13 for k in ks_far), "| least (c_k - grid_k)/(b_k - h): %.1e" % min((far[k] - gtop[k]) / (gtop[k] - h) for k in ks_far))
print("      g/h    eta_g/h     (L-t1(h-eta_g))g   vth g^2/12    m(g)/3      mu      k_2(g) [grid, lines]   k_2 g/h   104.5..   inequality at k_2..k_2+25   defect(k_2)")
okC = True
for ir, g in enumerate(rates):
    eta_g = vth * g * g / 576
    mu = 1.0 / (1.0 + g / (48 * h))
    mu_def = h / (h + 0.5 * math.sqrt(eta_g / vth))
    t1e = float(P.t1(np.array([h - eta_g]))[0])
    mg = float(P.theta_hint(g)) - (h - Lm * g)
    cond1 = eta_g * (1 - Lm) / Lm
    cond2 = vth * g * g / 12

    def k2_of(tops):
        okk = (tops - h < cond1) & (tops - h <= cond2)
        idx = np.nonzero(okk[1:])[0]
        return int(idx[0]) + 1 if len(idx) else None

    k2g, k2l = k2_of(gtop), k2_of(ltop)
    th_g = float(P.theta_hint(g))
    line = "    %5.2f   %.3e      %.4e      %.4e   %.4e   %.6f" % (g / h, eta_g / h, (Lm - t1e) * g, cond2, mg / 3, mu)
    pre = abs(mu - mu_def) < 1e-14 and (Lm - t1e) * g <= cond2 * (1 + 1e-12) and cond2 <= mg / 3 * (1 + 1e-12)
    okC &= pre
    if k2l is None:
        print(line + "   k_2 > %d (not reached)" % KMAX)
        continue
    k2 = k2l                                                     # the conservative one (upper bracket of the tops)
    hi = min(KMAX, k2 + 25)
    defect = lM[k2:hi + 1, ir] - th_g                            # upper bracket of M_{W_k, b_k}(g) - theta_hint(g)
    bound = g * mu ** (np.arange(k2, hi + 1) - k2)
    holds = bool(np.all(defect <= bound))
    okC &= holds
    pred = math.sqrt(576 * Lm / ((1 - Lm) * vth) * P.cs2) / h
    print(line + "   [%4d, %4d]          %7.2f   %7.2f      %s (bound %.3e .. %.3e)      %.2e" % (
        k2g, k2l, k2 * g / h, pred, "holds" if holds else "FAILS", bound[0], bound[-1], float(defect[0])))
check("for each rate: mu_{eta_g} = (1 + g/(48h))^-1, (L - t_1(h - eta_g)) g <= vth g^2/12 <= m/3, and the inequality of A11' for k_2 <= k <= k_2 + 25", okC)
# Lemma A10 as it is used: the envelope is the image itself on [0, h - eta_g] from k_2(g) on, i.e. B_t(k) > h - eta_g
Bt = np.array(Bt)
okT = True
for g in rates:
    eta_g = vth * g * g / 576
    okk = (ltop - h < eta_g * (1 - Lm) / Lm) & (ltop - h <= vth * g * g / 12)
    idx = np.nonzero(okk[1:])[0]
    if len(idx):
        k2 = int(idx[0]) + 1
        okT &= bool(np.all(Bt[k2:] > h - eta_g))
check("Lemma A10 as used: the tangency point B_t(k) of the cap line is beyond h - eta_g for all k >= k_2(g) computed", okT)
kk = np.arange(2, KMAX + 1)
print("    more is true numerically (the earlier referee): B_t(k) > h for every 2 <= k <= %d: %s;  B_t(1) = %.4f h;  (B_t(k) - h)/(b_k - h) at k = 2, 5, 20, 100: %s"
      % (KMAX, bool(np.all(Bt[2:] > h)), Bt[1] / h, ", ".join("%.4f" % ((Bt[k] - h) / (ltop[k] - h)) for k in (2, 5, 20, 100) if k <= KMAX)))
print("    so the first condition in the definition of k_2(g) is far from necessary for this pair: with the second alone, k_2 g/h would be sqrt(24) pi = %.1f instead of %.1f"
      % (math.sqrt(24) * math.pi, math.sqrt(576 * Lm / ((1 - Lm) * vth) * P.cs2) / h))

print("    how conservative (defect = M_k(g) - theta_hint(g); 'grid' and 'lines' bracket it):")
print("      g/h   true decay per level (ratio of consecutive defects, where 1e-4 > defect/g > 1e-8)   kappa_g = 1 - g/(J(t_g) + (1 - t_g) g)   e^{-g/h}   mu = (1 + g/(48h))^-1   ln(1/kappa_g)/ln(1/mu)")
for ir, g in enumerate(rates):
    th_g = float(P.theta_hint(g))
    dl, dg = lM[:, ir] - th_g, gM[:, ir] - th_g
    sel = np.nonzero((dl[1:-1] < 1e-4 * g) & (dg[1:-1] > 1e-8 * g))[0] + 1
    tg = float(P.t_hint(g))
    kg = 1.0 - g / (float(P.J(tg)) + (1 - tg) * g)
    mu = 1.0 / (1.0 + g / (48 * h))
    if len(sel) >= 3:
        rl = float(np.median(dl[sel[1:]] / dl[sel[:-1]]))
        rg = float(np.median(dg[sel[1:]] / dg[sel[:-1]]))
        obs = "lines %.5f, grid %.5f (k = %d..%d)" % (rl, rg, sel[0], sel[-1])
    else:
        obs = "(no levels in that window)"
    print("     %5.2f   %-52s   %.5f        %.5f     %.5f        %.1f" % (g / h, obs, kg, math.exp(-g / h), mu, math.log(1 / kg) / math.log(1 / mu)))
print("      g/h    n      levels needed for n (M_k(g) - theta_hint(g)) <= 1: computed [grid, lines]     the proof: k_2(g) + ceil(ln(g n)/ln(1 + g/(48h)))     ratio")
for ir, g in enumerate(rates):
    th_g = float(P.theta_hint(g))
    dl, dg = lM[:, ir] - th_g, gM[:, ir] - th_g
    mu = 1.0 / (1.0 + g / (48 * h))
    cond1 = (vth * g * g / 576) * (1 - Lm) / Lm
    okk = (ltop - h < cond1) & (ltop - h <= vth * g * g / 12)
    idx = np.nonzero(okk[1:])[0]
    if not len(idx):
        continue
    k2 = int(idx[0]) + 1
    for n in (1e4, 1e6, 1e9):
        need_l = int(np.argmax(dl <= 1.0 / n)) if np.any(dl <= 1.0 / n) else None
        need_g = int(np.argmax(dg <= 1.0 / n)) if np.any(dg <= 1.0 / n) else None
        proof = k2 + math.ceil(math.log(g * n) / math.log(1 + g / (48 * h)))
        if need_l:
            print("     %5.2f   %.0e   [%s, %d]%s%d%s%.1f" % (g / h, n, str(need_g), need_l, " " * 70, proof, " " * 40, proof / need_l))

# ------------------------------------------------------------------------------------------------------------
print("(D) the observation A8':  sup_{g >= 0} [M_k(g) - theta_hint(g)] = b_k - h")
gsc = np.concatenate([[0.0], np.geomspace(1e-9 * h, 5 * P.eps, 6000)])
thh = P.theta_hint(gsc)
t1all = None
okD = True
print("      k    b_k - h (grid, lines)        max_{g>0} [D_k(g) - D_k(0)]/(b_k - h)  (grid, lines)     dual form: sup_B [B - J(min(W_k(B), L))]/(b_k - h)  (grid, lines; = 1, at B = b_k)     second largest local value, at B/b_k (lines)")
for k in (2, 3, 5, 8, 12, 20, 40, 60):
    if k > KMAX:
        continue
    x, w = gcur[k]
    Dg = L.grid_M(x, w, gsc) - thh
    Vl = keepL[k]
    Dl = Vl.M(gsc) - thh
    eg = float(np.max(Dg[1:] - Dg[0])) / (gtop[k] - h)
    el = float(np.max(Dl[1:] - Dl[0])) / (ltop[k] - h)
    # the dual form: M_k <= theta_hint + (b_k - h) on [0, inf)  <=>  B - J(min(W_k(B), L)) <= b_k - h on [0, b_k]
    Bs = np.linspace(0.0, x[-1], 40001)
    Gg = Bs - P.J(np.minimum(np.interp(Bs, x, w), Lm))
    Bl = np.linspace(0.0, Vl.c, 40001)
    Wl = Vl.val(Bl)[0]
    Gl = Bl - P.J(np.minimum(Wl, Lm))
    sg, sl = float(np.max(Gg)) / (gtop[k] - h), float(np.max(Gl)) / (ltop[k] - h)
    below = Wl < Lm                                              # the part of the curve below slope L
    j2 = int(np.argmax(np.where(below, Gl, -np.inf)))
    okD &= (eg <= 1e-9) and (el <= 1e-9) and (sg <= 1 + 1e-9) and (sl <= 1 + 1e-9)
    print("    %3d   %.6e, %.6e          %+.2e, %+.2e                    %.9f, %.9f (at B/b_k = %.6f)                                   %.6f at %.4f" % (
        k, gtop[k] - h, ltop[k] - h, eg, el, sg, sl, Bl[int(np.argmax(Gl))] / Vl.c, float(Gl[j2]) / (ltop[k] - h), Bl[j2] / Vl.c))
check("the defect is largest at accuracy zero at k = 2, 3, 5, 8, 12, 20, 40, 60 (both brackets; 6000 rates up to 5 eps*), and the dual form holds", okD)
print("    the inequality that the 'obvious induction' needs near the top:  (b_k - h)^2/(vth h^2) >= b_k - b_{k+1}")
row = []
for k in (4, 6, 8, 9, 10, 11, 12, 15, 20):
    lhs = (gtop[k] - h) ** 2 / (vth * h * h)
    rhs = gtop[k] - gtop[k + 1]
    row.append("k = %d: %.2e %s %.2e" % (k, lhs, ">=" if lhs >= rhs else "<", rhs))
print("      " + ";  ".join(row))
first_fail = next(k for k in range(2, 60) if (gtop[k] - h) ** 2 / (vth * h * h) < gtop[k] - gtop[k + 1])
print("      it fails from k = %d on (the addendum: 'from about ten levels on';  asymptotically k > pi^2 = 9.87)" % first_fail)
print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
