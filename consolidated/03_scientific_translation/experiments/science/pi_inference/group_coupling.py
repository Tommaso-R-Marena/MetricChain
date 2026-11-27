#!/usr/bin/env python3
"""What the GROUP LAWS allow, what the joint law adds, and what pair terms would recover -- open problem D15
(prediction in the research log of 2026-11-26 before this script existed).

Proposition A17.19 (LP):  Z(E) / Z(m_+)  >=  < prod_g (1 + y_g) >  >=  1 + sum_g < y_g >,   y_g = e^{beta S+_g} - 1 >= 0,
means under the ceiling model; only the LAWS of the single groups enter the right-hand side.
(1) [the theory division, THY-RES-0016 section 4; the Ensemble division, ENSEMBLE-RES-0002 section 1; proof in three lines here]
    Over all couplings of the given group laws, the least value of < prod_g (1 + y_g) > is exactly 1 + sum_g <y_g> if
    sum_g P(S+_g > 0) <= 1 (put the events on disjoint parts of the unit interval), and strictly larger otherwise.  So when
    that sum is at most one, NO certificate built from the group laws alone improves (LP).
(2) The largest value over couplings is the comonotone one (all groups driven by one uniform variable) [K, cited there].
(3) Second order:  prod_g (1 + y_g) >= 1 + sum_g y_g + sum_{g<h} y_g y_h  (all terms non-negative), which needs the joint law
    of PAIRS of groups.
Per case this script takes the items, routes and models of first_order_recovery.py from its frame (nothing is rebuilt
here) and reports, for the groups of the last stage (far pairs, terms, allocation), in nats above ln Z(m_+):
    LJ = beta sum <S+_g>;   LP = ln(1 + A), A = sum <y_g>  (A exact, from the driver's transfer-matrix means);
    with pair terms: ln(1 + A + <q>), q = sum_{g<h} y_g y_h;   exact joint law: ln(1 + A + <d>), d = prod (1 + y_g) - 1 - sum y_g;
    comonotone;   sum_g P(S+_g > 0);   P(two or more groups have slack);   <q> / <d>.
<d>, <q> and the probabilities: exactly (every state, ceiling weights) for the enumerated instances; otherwise from N exact
independent samples of the ceiling model, with standard errors (d and q vanish unless two groups have slack at once, so their
variance is small).  Checks: A from the states against the driver's exact A; d >= q >= 0 at every state; the driver's own (LP)
reproduced; control: the same d with the groups' slacks SHUFFLED independently across states (a product coupling of the same
laws) -- it must differ from the true d if the groups are dependent, and its pair term must then equal sum_{g<h} <y_g><y_h>.
[As run: the product coupling is evaluated exactly from the group means, the comonotone one exactly from the laws; the laws are
heavy-tailed (slack of 20 kT and more at rare states), which defeated a shuffle and a grid tried first.]
Run: python3 -B group_coupling.py K5 4 2 --enum > group_coupling_K5_m4_w2_enum.log
     python3 -B group_coupling.py K12 4 4 [--N 400000] > group_coupling_K12_m4_w4.log
"""
import os, sys, io, time, math, contextlib, resource
import numpy as np
import first_order_recovery as FR
SR = FR.SR; BETA = FR.BETA


def log(s): print(s, flush=True)


def capture(argv):
    got = {}

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is FR.main.__code__: got.update(frame.f_locals)
    old = sys.argv; sys.argv = ["first_order_recovery.py"] + argv; buf = io.StringIO(); sys.setprofile(prof)
    try:
        with contextlib.redirect_stdout(buf): FR.main()
    finally:
        sys.setprofile(None); sys.argv = old
    return got, buf.getvalue()


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; ENUM = "--enum" in a; N = int(a[a.index("--N") + 1]) if "--N" in a else 400000; t0 = time.time()
    got, text = capture([seq, m, w] + (["--enum"] if ENUM else []))
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("| far pairs, terms") or line.startswith("| nothing"): log(line[:420])
    items, kind, rts, CL, up, GS, stages, lnZup, lnZlo, res = (got[q] for q in ("items", "kind", "rts", "CL", "up", "GS", "stages", "lnZup", "lnZlo", "res"))
    name = stages[-1][0]; gks = sorted(GS[name]); jp = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (+1, 0)]
    groups = [[items[j] for j in jp if rts[j] == gk] for gk in gks]; G = len(gks)
    A_exact = sum(GS[name][gk]["e"] for gk in gks); LJ_exact = BETA * sum(GS[name][gk]["a"] for gk in gks)
    corrected = res[name]; width = corrected[1] - corrected[0]
    log(f"(0) {G} groups with plus-items ({sum(len(g) for g in groups)} items with a route); from the driver's exact means: LJ = {LJ_exact:.6e}, A = sum <y_g> = {A_exact:.6e}, "
        f"LP = ln(1 + A) = {math.log1p(A_exact):.6e} nats above ln Z(m_+); the driver's corrected bracket [{corrected[0]:.7f}, {corrected[1]:.7f}], width {width:.4g}; "
        f"its lower end minus ln Z(m_+) = {corrected[0] - lnZup:.6e} [{time.time() - t0:.0f}s]")
    if ENUM:
        X = got["st"]; wt = got["wu"]; how = f"every state ({len(X)}), ceiling weights"
    else:
        X = up.sample(N, np.random.default_rng(20261126), BETA); wt = np.full(N, 1.0 / N); how = f"{N} exact independent samples of the ceiling model (seed 20261126)"
    S = np.stack([SR.items_value(g, X) for g in groups]); assert (S >= 0).all()

    def dq(S_):
        """d = prod (1 + y_g) - 1 - sum y_g = sum_g y_g (prod_{h<g} (1 + y_h) - 1)  and  q = sum_g y_g sum_{h<g} y_h, both as sums of
        non-negative terms (the direct formulas cancel: y reaches e^25 at rare states)."""
        y_ = np.expm1(BETA * S_); d_ = np.zeros(S_.shape[1]); q_ = np.zeros(S_.shape[1]); cs = np.zeros(S_.shape[1]); cy = np.zeros(S_.shape[1])
        for gi in range(S_.shape[0]):
            d_ += y_[gi] * np.expm1(BETA * cs); q_ += y_[gi] * cy; cs += S_[gi]; cy += y_[gi]
        return y_, d_, q_
    y, d, q = dq(S); sy = y.sum(axis=0)
    assert (d >= q * (1 - 1e-12)).all() and (q >= 0).all()

    def mean_se(v):
        mu = float((wt * v).sum())
        return (mu, 0.0) if ENUM else (mu, float(np.sqrt(((v - mu) ** 2).mean() / len(v))))
    A_x, A_se = mean_se(sy); d_m, d_se = mean_se(d); q_m, q_se = mean_se(q)
    pos = S > 0; Pg = (pos * wt[None]).sum(axis=1); sumP = float(Pg.sum()); two = float((wt * (pos.sum(axis=0) >= 2)).sum())
    log(f"(1) from {how}: A = {A_x:.6e}{'' if ENUM else f' +- {A_se:.1e}'} (the driver's exact value {A_exact:.6e}: {'relative deviation ' + format(abs(A_x - A_exact) / A_exact, '.1e') if ENUM else format((A_x - A_exact) / A_se, '+.2f') + ' standard errors away'})")
    if ENUM: assert abs(A_x - A_exact) <= 2e-8 * A_exact
    else: assert abs(A_x - A_exact) <= 5 * A_se
    log(f"(2) **sum_g P(S+_g > 0) = {sumP:.4f}** (largest single group {float(Pg.max()):.4f}; groups that ever have slack: {int((Pg > 0).sum())} of {G}); P(two or more groups have slack at once) = {two:.4e}"
        f"  ->  the events {'CAN be made disjoint: (LP) is the exact optimum from the group laws; no certificate from the laws alone improves it' if sumP <= 1 else 'can NOT be made disjoint: (LP) is not exactly the optimum from the group laws; that optimum lies between (LP) and the exact joint value below (the true coupling is one coupling), not computed here'}")
    # comonotone coupling of the same laws, EXACT for the laws in hand: between consecutive breakpoints of the cumulative weights every
    # group's quantile is constant.  (A grid in u was tried first and lost the rare states with slack of 20 kT and more: the value came
    # out BELOW (LP), which no coupling can be.)
    if ENUM:
        srt = [np.argsort(S[gi], kind="stable") for gi in range(G)]; cws = [np.cumsum(wt[o]) for o in srt]
        br = np.unique(np.concatenate([c for c in cws] + [np.array([1.0])])); br = br[br > 0]; lo_ = np.concatenate([[0.0], br[:-1]]); mid = 0.5 * (lo_ + br); tot = np.zeros(len(br))
        for gi in range(G):
            tot += S[gi][srt[gi]][np.minimum(np.searchsorted(cws[gi], mid), len(srt[gi]) - 1)]
        como = float(((br - lo_) * np.exp(BETA * tot)).sum())
    else:
        como = float(np.exp(BETA * np.sort(S, axis=1).sum(axis=0)).mean())
    # the product coupling of the same laws, exactly, from the group means (a shuffle of the states was tried first and is too noisy: heavy tails)
    eg = np.array([GS[name][gk]["e"] for gk in gks]); d_prod = float(np.prod(1.0 + eg) - 1.0 - eg.sum()); q_prod = float(sum(eg[gi] * eg[:gi].sum() for gi in range(G)))
    # check of d: 1 + A + <d> against the direct mean of exp(beta sum_g S_g)
    direct = float((wt * np.exp(BETA * S.sum(axis=0))).sum()); ident = abs(direct - (1.0 + A_x + d_m)) / direct
    # how much of <d> rests on few states (heavy tails): the share of the 100 largest contributions
    contrib = np.sort(wt * d)[::-1]; top100 = float(contrib[:100].sum() / max(contrib.sum(), 1e-300))
    L = lambda extra: math.log1p(A_exact + extra)
    log("| bound on ln Z(E) - ln Z(m_+) from the routed plus-items | nats | as a fraction of the corrected bracket's width |")
    log("|---|---|---|")
    log(f"| (LJ): first order | {LJ_exact:.6e} | |")
    log(f"| (LP): the product inequality, group laws only | {L(0):.6e} | |")
    log(f"| + pair terms sum_(g<h) <y_g y_h> (joint laws of pairs of groups) | {L(q_m):.6e}{'' if ENUM else f' +- {q_se / (1 + A_exact):.1e}'} | **+{(L(q_m) - L(0)) / width:.3f}** |")
    log(f"| the exact joint law of the groups: ln <prod (1 + y_g)> | {L(d_m):.6e}{'' if ENUM else f' +- {d_se / (1 + A_exact):.1e}'} | **+{(L(d_m) - L(0)) / width:.3f}** |")
    log(f"| for comparison, the comonotone coupling of the same laws (the largest value the laws allow) | {math.log(como):.6e} | +{(math.log(como) - L(0)) / width:.3f} |")
    log(f"(3) the pair terms recover <q> / <d> = **{q_m / d_m:.4f}** of what the exact joint law adds to (LP){'' if ENUM else f' (standard errors of <q>, <d>: {q_se:.1e}, {d_se:.1e})'}; "
        f"where the exact joint value sits between the two extremes the laws allow: (joint - LP) / (comonotone - LP) = {(L(d_m) - L(0)) / (math.log(como) - L(0)):.3f}")
    log(f"(4) checks: 1 + A + <d> against the direct mean of exp(beta sum_g S+_g): relative deviation {ident:.1e} (must be < 1e-9); (LP) <= exact joint <= comonotone: "
        f"{L(0) <= L(d_m) + 1e-15 and L(d_m) <= math.log(como) + (1e-12 if ENUM else 5 * d_se)}; the product coupling of the same laws (independent groups), exactly from the group means: "
        f"<d> = {d_prod:.4e}, <q> = {q_prod:.4e}; **the true <d> is {d_m / d_prod:.2f} times the product coupling's** (1 would mean independent groups); "
        f"the 100 largest of the {len(wt)} contributions carry {top100:.3f} of <d>")
    assert ident < 1e-9 and L(0) <= L(d_m) + 1e-15 and L(d_m) <= math.log(como) + (1e-12 if ENUM else 5 * d_se)
    # ------------------------------------------------------------------ the upper side
    # (UP):  Z(m_-) / Z(E) >= < prod_g (1 + z_g) >_E >= 1 + sum_g <z_g>_E,  z_g = e^{beta S-_g} - 1,  and  <z_g>_E >= (Z(m_+) / Z(E)) < z_g e^{beta S+_g} >_+ ;
    # with the JOINT law of all groups under the ceiling the same route gives  C'' = < (e^{beta s_-} - 1) e^{beta s_+} >_+  in place of
    # C' = sum_g < z_g (1 + y_g) >_+ ;  to second order (pairs of groups):  C_2 = C' + < sum_{g<h} z_g z_h + sum_{g != h} z_g y_h >_+ .
    lo = got["lo"]; jm = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (-1, 0)]
    groups_m = [[items[j] for j in jm if rts[j] == gk] for gk in gks]
    Sm = np.stack([SR.items_value(g, X) for g in groups_m]); assert (Sm >= 0).all(); z = np.expm1(BETA * Sm)
    C1_exact = sum(GS[name][gk]["cp"] for gk in gks); c1 = (z * (1.0 + y)).sum(axis=0); C1_x, C1_se = mean_se(c1)
    # second order, as sums of non-negative terms
    szy = z.sum(axis=0) * y.sum(axis=0) - (z * y).sum(axis=0)                      # sum_{g != h} z_g y_h
    zz = np.zeros(S.shape[1]); cz = np.zeros(S.shape[1])
    for gi in range(G): zz += z[gi] * cz; cz += z[gi]                               # sum_{g<h} z_g z_h
    c2add = zz + np.maximum(szy, 0.0); C2add, C2_se = mean_se(c2add)
    cjoint = np.expm1(BETA * Sm.sum(axis=0)) * np.exp(BETA * S.sum(axis=0)); Cj, Cj_se = mean_se(cjoint - c1)   # C'' - C' >= 0, as a mean of the difference
    assert (cjoint - c1 >= -1e-9 * (1.0 + cjoint)).all() and (cjoint - c1 - c2add >= -1e-9 * (1.0 + cjoint)).all()

    def solve(C):
        v = lnZlo
        for _ in range(400): v = lnZlo - math.log1p(C * math.exp(lnZup - v))
        return v
    v1, v2, vj = solve(C1_exact), solve(C1_exact + C2add), solve(C1_exact + Cj)
    if ENUM:
        U0 = got["best"][1]; U0_se = 0.0; L0 = got["best"][0]; howU = "every state"
        assert abs((L0 - lnZup) - L(d_m)) < 1e-9, "the driver's exact put-back lower end must equal ln(1 + A + <d>)"
    else:
        # ln Z(m_- + s_-) = ln Z(m_-) + ln < e^{-beta s_-} >_floor : ten times as many samples as for the ceiling, in chunks (a bounded variable; 400 000 gave a
        # standard error of 6 % of the bracket's width at Lys12, too coarse for line (6))
        rngf = np.random.default_rng(20261127); acc = []; NF = 10 * N
        for _ in range(10):
            Xf = lo.sample(N, rngf, BETA); acc.append(np.exp(-BETA * sum(SR.items_value(g, Xf) for g in groups_m)))
        e_ = np.concatenate(acc); U0 = lnZlo + math.log(float(e_.mean())); U0_se = float(e_.std() / math.sqrt(len(e_)) / e_.mean()); howU = f"{NF} exact samples of the floor model (seed 20261127)"
    log(f"(5) UPPER side.  C' = sum_g <z_g (1 + y_g)>: {C1_x:.6e}{'' if ENUM else f' +- {C1_se:.1e}'} from the states (the driver's exact value {C1_exact:.6e}); "
        f"(UP) with it: {v1:.7f} (the driver's upper end {corrected[1]:.7f})")
    assert (abs(C1_x - C1_exact) <= 2e-8 * C1_exact) if ENUM else (abs(C1_x - C1_exact) <= 5 * C1_se)
    assert v1 <= corrected[1] + 2e-7 or abs(v1 - corrected[1]) < 2e-6
    log("| upper end from the routed items | value | below (UP), as a fraction of the corrected bracket's width |")
    log("|---|---|---|")
    log(f"| (UP): group laws only (the driver) | {v1:.7f} | 0 |")
    log(f"| + pair terms (joint laws of pairs of groups under the ceiling) | {v2:.7f} | **{(v1 - v2) / width:.3f}** |")
    log(f"| the exact joint law of all groups under the ceiling, same route | {vj:.7f} | **{(v1 - vj) / width:.3f}** |")
    log(f"| the same items put back exactly: ln Z(m_- + s_-), from {howU} | {U0:.7f}{'' if ENUM else f' +- {U0_se:.1e}'} | **{(v1 - U0) / width:.3f}** |")
    lower_gain = (L(d_m) - L(0)) / width; pm = "" if ENUM else f" +- {U0_se / width:.3f}"
    log(f"(6) the loss between groups in the sense of workstream R19 (corrected width minus the width with the same routed items put back exactly), as a fraction of the corrected width: "
        f"lower side {lower_gain:.3f} + upper side {(v1 - U0) / width:.3f}{pm} = **{lower_gain + (v1 - U0) / width:.3f}**{pm}; of it, what the joint law of the groups UNDER THE CEILING would recover by the "
        f"same inequalities: {lower_gain:.3f} + {(v1 - vj) / width:.3f} = **{lower_gain + (v1 - vj) / width:.3f}** (**pair terms alone: {(L(q_m) - L(0)) / width:.3f} + {(v1 - v2) / width:.3f} = "
        f"{(L(q_m) - L(0)) / width + (v1 - v2) / width:.3f}**); the rest, {(vj - U0) / width:.3f}{pm}, is the price of bounding a mean under the true ensemble by one under the ceiling and is not a matter of joint laws")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
