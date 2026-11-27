#!/usr/bin/env python3
"""R24, item 5 (i)-(ii): one row of the table of addendum item 90 / SCI-MSG-0032, every number recomputed by the referee by
enumeration from the TABLES (the driver's items, routes and the two band models are taken from the frame of
first_order_recovery.main(); every energy, weight, mean and bound below is computed here from their tables by
r24_common -- none of the driver's evaluators, means or solvers is used except for comparison).

Also computed, because the brief asks whether "the rest" is "not a matter of joint laws":
  * the identity  (Z_- - C'' Z_+) - Z(m_- + s_-) = sum_x (e^{beta s_-} - 1)(e^{-beta (m_- + s_-)} - e^{-beta (m_+ - s_+)})   [the rest, exactly]
  * the FLOOR route:  Z(E) <= Z(m_- + s_-) = Z(m_-) < prod_g (1 - zeta_g) >_floor,  zeta_g = 1 - e^{-beta S-_g} in [0, 1):
        exact joint law of the minus groups under the floor  ->  the put-back itself (an identity);
        pair laws under the floor (Bonferroni)                ->  Z(E) <= Z(m_-) (1 - sum <zeta_g> + sum_{g<h} <zeta_g zeta_h>);
        single-group laws under the floor                     ->  the comonotone value (the largest the laws allow).
Run: python3 -B r24_item5_enum.py K5 4 2 > r24_item5_enum_K5_m4_w2.log
"""
import os, sys, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, PI); sys.path.insert(0, HERE)
import r24_common as C


def lse(a):
    m = a.max(); return float(m + math.log(np.exp(a - m).sum()))


def esym2(Y):
    """(e_1, e_2, sum_{k>=2} e_k) of the rows of Y >= 0, columnwise, as sums of non-negative terms"""
    G, N = Y.shape; e1 = np.zeros(N); e2 = np.zeros(N); hi = np.zeros(N)       # hi = sum_{k>=2} e_k
    for g in range(G):
        hi = hi + Y[g] * (e1 + hi); e2 = e2 + Y[g] * e1; e1 = e1 + Y[g]
    return e1, e2, hi


def comonotone_mean_of_product(V, wt, fun):
    """E fun(Q_1(U), ..., Q_G(U)) for U uniform, Q_g the quantile function of the law of V[g] under the weights wt (exact:
    piecewise constant between the merged breakpoints of the G cumulative laws)."""
    G = V.shape[0]; order = [np.argsort(V[g], kind="stable") for g in range(G)]; cum = [np.cumsum(wt[o]) for o in order]
    for c in cum: c[-1] = 1.0
    br = np.unique(np.concatenate(cum)); lo_ = np.concatenate([[0.0], br[:-1]]); mid = 0.5 * (lo_ + br)
    vals = np.stack([V[g][order[g]][np.minimum(np.searchsorted(cum[g], mid, side="left"), len(wt) - 1)] for g in range(G)])
    return float(((br - lo_) * fun(vals)).sum())


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; t0 = time.time()
    import first_order_recovery as FR
    got, text = C.capture(FR, [seq, m, w, "--enum"], "first_order_recovery.py")
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("| far pairs, terms and") or line.startswith("| nothing"): print("[theirs] " + line[:330], flush=True)
    BETA = FR.BETA
    items, kind, rts, CL, up, lo, GS, stages, res = (got[q] for q in ("items", "kind", "rts", "CL", "up", "lo", "GS", "stages", "res"))
    st, EE, k, n = got["st"], np.asarray(got["EE"], float), list(got["k"]), got["n"]; N = len(st)
    name = stages[-1][0]; gks = sorted(GS[name]); Gn = len(gks); corrected = res[name]; width = corrected[1] - corrected[0]
    # ---------------------------------------------------------------- own evaluation of the two models and of the items
    cu, fu = C.factors_of(up); cl, fl = C.factors_of(lo)
    Eu = C.energy_all(cu, fu, k).ravel(); El = C.energy_all(cl, fl, k).ravel()
    dev = max(float(np.abs(Eu - got["eu"]).max()), float(np.abs(El - got["el"]).max()))
    jp = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (+1, 0)]; jm = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (-1, 0)]
    val = lambda j: np.asarray(items[j][1], float)[tuple(st[:, u] for u in items[j][0])]
    Sp = np.stack([sum((val(j) for j in jp if rts[j] == gk), np.zeros(N)) for gk in gks]); Sm = np.stack([sum((val(j) for j in jm if rts[j] == gk), np.zeros(N)) for gk in gks])
    sp_all = sum((val(j) for j in jp), np.zeros(N)); sm_all = sum((val(j) for j in jm), np.zeros(N)); sp = Sp.sum(axis=0); sm = Sm.sum(axis=0)
    nor = (sum(1 for j in jp if rts[j] is None), sum(1 for j in jm if rts[j] is None))
    v_r = int((Eu - EE < sp - 1e-9).sum() + (EE - El < sm - 1e-9).sum()); v_a = int((Eu - EE < sp_all - 1e-9).sum() + (EE - El < sm_all - 1e-9).sum())
    v_c = int((Eu - EE < 2 * sp - 1e-9).sum() + (EE - El < 2 * sm - 1e-9).sum())
    print(f"(0) {N} states; my evaluation of the models' tables against the driver's energies: {dev:.1e} kcal/mol; {Gn} groups {gks}; plus-items {len(jp)} ({nor[0]} without a route), minus-items {len(jm)} ({nor[1]} without a route); "
          f"hypotheses m_+ - E >= s_+, E - m_- >= s_-: violations with the routed items {v_r}, with all items {v_a} (must be 0); control, routed items doubled: {v_c} (must be positive); "
          f"least entry of S+ {Sp.min():.2e}, of S- {Sm.min():.2e} [{time.time() - t0:.0f}s]", flush=True)
    lnZp, lnZm, lnZ = lse(-BETA * Eu), lse(-BETA * El), lse(-BETA * EE)
    wp = np.exp(-BETA * Eu - lnZp); wm = np.exp(-BETA * El - lnZm)             # ceiling and floor ensembles
    print(f"(1) ln Z(m_+) = {lnZp:.7f}, ln Z(E) = {lnZ:.7f}, ln Z(m_-) = {lnZm:.7f} (the driver: {got['lnZup']:.7f}, {got['lnZ']:.7f}, {got['lnZlo']:.7f}); D = {lnZm - lnZp:.6g}; "
          f"the driver's corrected bracket [{corrected[0]:.7f}, {corrected[1]:.7f}], width {width:.6g}")
    # ---------------------------------------------------------------- lower end
    y = np.expm1(BETA * Sp); e1, e2, hi = esym2(y)
    A = float((wp * e1).sum()); q = float((wp * e2).sum()); d = float((wp * hi).sum())
    direct = float((wp * np.exp(BETA * sp)).sum()); L0 = lnZp + math.log(direct)                 # ln Z(m_+ - s_+), the exact put-back
    Pg = (wp[None] * (Sp > 0)).sum(axis=1); sumP = float(Pg.sum()); two = float((wp * ((Sp > 0).sum(axis=0) >= 2)).sum())
    LP = lnZp + math.log1p(A); LPd = lnZp + math.log1p((1 - 1e-9) * A)
    low_pair = (math.log1p(A + q) - math.log1p(A)) / width; low_joint = (L0 - LP) / width
    print(f"(2) LOWER end (means under the ceiling): A = sum <y_g> = {A:.6e}; (LP) = {LP:.7f} (with the driver's factor 1 - 1e-9: {LPd:.7f}; the driver's lower end {corrected[0]:.7f}); "
          f"sum_g P(S+_g > 0) = **{sumP:.4f}**; P(two or more groups) = {two:.4e}; identity 1 + A + <d> = <e^(beta s_+)>: relative deviation {abs(1 + A + d - direct) / direct:.1e}; "
          f"exact joint law adds **{low_joint:.3f}** of the width, pair terms **{low_pair:.3f}**; <q>/<d> = {q / d:.4f}")
    # ---------------------------------------------------------------- upper end, the route of Proposition A17.19
    z = np.expm1(BETA * Sm); Ysum = y.sum(axis=0)
    c1 = (z * (1.0 + y)).sum(axis=0)
    # sum_{g != h} z_g y_h as a sum of non-negative terms: z_g times (sum of the other y)
    pre = np.cumsum(y, axis=0) - y; suf = np.cumsum(y[::-1], axis=0)[::-1] - y; zy = (z * (pre + suf)).sum(axis=0)
    zz = esym2(z)[1]; c2 = c1 + zz + zy; cj = np.expm1(BETA * sm) * np.exp(BETA * sp)
    ord_bad = int((c2 < c1 * (1 - 1e-12) - 1e-300).sum() + (cj < c2 * (1 - 1e-9) - 1e-12).sum())
    C1, C2, Cj = float((wp * c1).sum()), float((wp * c2).sum()), float((wp * cj).sum())
    Zp, Zm = 1.0, math.exp(lnZm - lnZp)                                         # in units of Z(m_+)
    vclosed = lambda Cv: lnZp + math.log(Zm - Cv)

    def viter(Cv, it):
        v = lnZm
        for _ in range(it): v = lnZm - math.log1p(Cv * math.exp(lnZp - v))
        return v
    v1, v2, vj = vclosed(C1), vclosed(C2), vclosed(Cj)
    U0 = lse(-BETA * (El + sm))                                                  # ln Z(m_- + s_-), the exact put-back
    print(f"(3) UPPER end.  C' = {C1:.6e}, C_2 = {C2:.6e}, C'' = {Cj:.6e}; pointwise C' <= C_2 <= C'' violated at {ord_bad} states (must be 0); "
          f"the fixed point of the iteration in closed form, v(C) = ln(Z(m_-) - C Z(m_+)): v(C') = {v1:.7f} (60 iterations: {viter(C1, 60):.7f}; 400: {viter(C1, 400):.7f}; the driver's upper end {corrected[1]:.7f}), "
          f"v(C_2) = {v2:.7f}, v(C'') = {vj:.7f}; exact put-back ln Z(m_- + s_-) = {U0:.7f} (the driver's: {got['best'][1]:.7f}); v is decreasing in C by the closed form")
    up_pair, up_joint, up_tot = (v1 - v2) / width, (v1 - vj) / width, (v1 - U0) / width
    loss = (width - (U0 - L0)) / width
    print(f"(4) **THE ROW** (fractions of the corrected width {width:.4g}): groups {Gn} | sum P {sumP:.2f} | lower end: joint law {low_joint:.3f} (pair terms {low_pair:.3f}) | upper end: joint law {up_joint:.3f} (pair terms {up_pair:.3f}) | "
          f"the loss {loss:.3f} (= {low_joint:.3f} + {up_tot:.3f} + rounding of the driver's ends {loss - low_joint - up_tot:+.1e}) | recoverable by the joint law under the ceiling {low_joint + up_joint:.3f} | by pair terms {low_pair + up_pair:.3f} | the rest {up_tot - up_joint:.3f}")
    # ---------------------------------------------------------------- what "the rest" is
    rest_abs = math.exp(vj - lnZp) - math.exp(U0 - lnZp)                         # (Z_- - C'' Z_+ - Z(m_- + s_-)) / Z_+
    ident = float((np.expm1(BETA * sm) * (np.exp(-BETA * (El + sm) - lnZp) - np.exp(-BETA * (Eu - sp) - lnZp))).sum())
    print(f"(5) the rest, exactly: [Z_- - C'' Z_+ - Z(m_- + s_-)] / Z_+ = {rest_abs:.6e}; sum_x (e^(beta s_-) - 1)(e^(-beta (m_- + s_-)) - e^(-beta (m_+ - s_+))) / Z_+ = {ident:.6e} "
          f"(relative deviation {abs(rest_abs - ident) / max(abs(ident), 1e-300):.1e}): the minus-slack weighted by the width of the CORRECTED sandwich [m_- + s_-, m_+ - s_+]")
    # ---------------------------------------------------------------- the floor route
    zeta = -np.expm1(-BETA * Sm); f1, f2, fhi = esym2(zeta)                       # zeta in [0, 1)
    S1, S2 = float((wm * f1).sum()), float((wm * f2).sum()); prodm = float((wm * np.exp(-BETA * sm)).sum())
    U_exact = lnZm + math.log(prodm); U_bonf = lnZm + math.log(1 - S1 + S2); U_first = lnZm + math.log(1 - S1)
    como = comonotone_mean_of_product(zeta, wm, lambda V: np.prod(1.0 - V, axis=0)); U_como = lnZm + math.log(como)
    bonf_bad = int((np.exp(-BETA * sm) > 1 - f1 + f2 + 1e-12).sum()); first_bad = int((np.exp(-BETA * sm) > 1 - f1 + 1e-12).sum())
    Pm = (wm[None] * (Sm > 0)).sum(axis=1); twom = float((wm * ((Sm > 0).sum(axis=0) >= 2)).sum())
    # third order (a lower bound of the product, for the size of what Bonferroni gives away)
    e3 = np.zeros(N); a1 = np.zeros(N); a2 = np.zeros(N)
    for g in range(Gn): e3 = e3 + zeta[g] * a2; a2 = a2 + zeta[g] * a1; a1 = a1 + zeta[g]
    S3 = float((wm * e3).sum())
    print(f"(6) FLOOR route (means under the floor, bounded variables): identity Z(m_- + s_-) = Z(m_-) <prod (1 - zeta_g)>_floor: {U_exact:.7f} against {U0:.7f} (difference {U_exact - U0:.1e}); "
          f"sum_g P_floor(S-_g > 0) = {float(Pm.sum()):.4f}, P(two or more) = {twom:.4e}; S1 = {S1:.6e}, S2 = {S2:.6e}, S3 = {S3:.3e}; "
          f"pointwise Bonferroni prod(1 - zeta) <= 1 - S1 + S2 violated at {bonf_bad} states (must be 0); control, the first order 1 - S1 as an UPPER bound: violated at {first_bad} states (must be positive: it is a lower bound)")
    print("| upper end from the routed minus-items | value | below (UP), as a fraction of the corrected width | what it needs |")
    print("|---|---|---|---|")
    print(f"| (UP), the driver | {v1:.7f} | 0 | single-group laws under the ceiling |")
    print(f"| + pair terms under the ceiling (C_2) | {v2:.7f} | {up_pair:.3f} | pair laws under the ceiling |")
    print(f"| joint law under the ceiling (C'') | {vj:.7f} | {up_joint:.3f} | the joint law of all groups under the ceiling |")
    print(f"| **Bonferroni under the floor: ln Z(m_-) + ln(1 - S1 + S2)** | {U_bonf:.7f} | **{(v1 - U_bonf) / width:.3f}** | pair laws of the minus groups under the FLOOR |")
    print(f"| the exact put-back ln Z(m_- + s_-) = joint law under the floor | {U0:.7f} | {up_tot:.3f} | the joint law of the minus groups under the floor |")
    print(f"| single-group laws under the floor only (comonotone: the largest value the laws allow) | {U_como:.7f} | {(v1 - U_como) / width:.3f} | single-group laws under the floor |")
    print(f"| [not a bound] first order under the floor, ln Z(m_-) + ln(1 - S1) | {U_first:.7f} | {(v1 - U_first) / width:.3f} | — (lies BELOW the put-back by {(U0 - U_first) / width:.3f} of the width) |")
    print(f"(7) so of 'the rest' ({up_tot - up_joint:.3f} of the width), pair laws under the floor recover {(vj - U_bonf) / width:.3f}; with pair laws on both sides (lower end: ceiling pair terms; upper end: the better of C_2 and Bonferroni-floor) "
          f"the loss recovered is {low_pair + (v1 - min(v2, U_bonf)) / width:.3f} of the width, against {low_pair + up_pair:.3f} in the row; exact ln Z inside [LP, Bonferroni-floor]: {LP <= lnZ <= U_bonf}")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
