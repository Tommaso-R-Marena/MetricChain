#!/usr/bin/env python3
"""Certified pair terms with TWO held sites: the clamped computations of the proposition in held_pair_terms.py
(addendum item 93; open problem D15 (a)).

For held sites h < h' at states (s, t) the tables of the groups held at h and h' become tables on windows, so that
    r_T(s, t) = Z(ceiling with x_h = s, x_h' = t, energy lowered by the tables T) / Z(ceiling)
is one transfer-matrix pass for each of seven sets of tables T (B: the plus-items, A: the minus-items of a held site):
    1, B_h, B_h', B_h B_h', A_h B_h, A_h' B_h', A_h A_h' B_h B_h' .
With b = e^{beta S+} - 1, a = e^{beta S-} - 1 per held site:
    lower pair term  < b_h b_h' 1{s,t} >  =  r_BB - r_Bh - r_Bh' + r_1 ,
    upper pair term  < [a_h a_h' (1+b_h)(1+b_h') + a_h (1+b_h) b_h' + a_h' (1+b_h') b_h] 1{s,t} >
                     =  r_AABB - r_BB - (r_ABh - r_Bh) - (r_ABh' - r_Bh') .
And a second upper end, under the FLOOR (open problem D15 (b)): with c_h = 1 - e^{-beta S-_h} in [0, 1),
    Z(E) <= Z(m_- + s_-) = Z(m_-) < prod_h (1 - c_h) >_floor <= Z(m_-) [1 - sum_h <c_h> + sum_{h<h'} <c_h c_h'>]      (second Bonferroni sum),
all means exact under the floor with one or two held sites (one pass per held state or pair of held states; here EVERY
pair is needed).  No change of measure: this end does not pay "the price of bounding a mean under the true ensemble
through the ceiling" of addendum item 90.
Certified use of the ceiling route (every term non-negative, so ANY set of (h, h', s, t) gives valid bounds):
    ln Z(E) >= ln Z(m_+) + ln(1 + A + sum of the lower pair terms),      A = sum_h <b_h>   (groups merged per held site: one held site),
    ln Z(E) <= the fixed point of  v = ln Z(m_-) - ln(1 + (C + sum of the upper pair terms) e^{ln Z(m_+) - v}),   C = sum_h <a_h (1 + b_h)> .
Each pair term is lowered by 1e-9 times the sum of the absolute values of its four (six) ratios before use and dropped if
that leaves nothing; the driver's safety factors on A and C' are kept.
--enum: every (h, h', s, t); each pair term against its value from the states (largest absolute deviation must be below
1e-11: the terms are combinations of ratios of size up to 1); the new bracket must contain the exact ln Z and lie inside
the old one; control: the same with the tables sliced at a WRONG held state must disagree with the states.
Without --enum (Lys12): the (h, h', s, t) are chosen from N exact samples of the ceiling (the largest estimated terms, up to
--budget pairs of held states); the exact terms are then compared with their sample estimates.
--all: every (h, h', s, t) without --enum.  --nofloor: the ceiling route only.
Run: python3 -B held_pair_exact.py K5 4 2 --enum > held_pair_exact_K5_m4_w2_enum.log
     python3 -B held_pair_exact.py K12 4 4 --all > held_pair_exact_K12_m4_w4.log
     python3 -B held_pair_exact.py K12 4 4 --budget 60 --nofloor > held_pair_exact_K12_m4_w4_b60.log     (the prediction of 20:47 UTC)
"""
import sys, time, math, copy, resource
import multiprocessing as mp
import numpy as np
import first_order_recovery as FR
from group_coupling import capture
SR = FR.SR; BETA = FR.BETA; BIG = 1.0e5; SAFE = 1e-9
CTX = {}


def log(s): print(s, flush=True)


def add_tables(mdl, its, fixed, wrong=None, sign=-1.0):
    """add sign * (the items `its`) to the energy of mdl, the sites of `fixed` (dict site -> state) being at their states
    (sign -1: the weight is multiplied by e^{beta S}; sign +1: by e^{-beta S})"""
    for it in its:
        U = tuple(int(u) for u in it[0]); fx = dict(fixed)
        if wrong is not None and wrong[0] in U: fx[wrong[0]] = wrong[1]                    # the control: slice at another state of one held site
        t = np.asarray(it[1][tuple(fx[u] if u in fx else slice(None) for u in U)]); rem = tuple(u for u in U if u not in fx)
        assert all(rem[i] < rem[i + 1] for i in range(len(rem) - 1))
        t = sign * t
        if len(rem) == 0: mdl.const += float(t)
        elif len(rem) == 1: mdl.one[rem[0]] = mdl.one[rem[0]] + t
        elif len(rem) == 2: mdl.pair[(rem[0], rem[1])] = mdl.pair.get((rem[0], rem[1]), 0.0) + t; assert 0 < rem[1] - rem[0] <= mdl.w
        else: mdl.add_multi(rem, t)


def restrict(model, fixed):
    """the band model on the states with x_u = fixed[u]: the held sites keep ONE state (their axes have length 1), so that a pass
    costs what the remaining sites cost.  (A first version added 1e5 kcal/mol to the other states of the held sites instead: the
    same numbers, at the full cost of a pass.)"""
    new = type(model)([1 if i in fixed else model.k[i] for i in range(model.n)], model.w); new.const = model.const

    def cut(tab, sites):
        for ax, u in enumerate(sites):
            if u in fixed: tab = np.take(tab, [fixed[u]], axis=ax)
        return np.array(tab, dtype=float)
    new.one = [cut(model.one[i], (i,)) for i in range(model.n)]
    for (i, j), tab in model.pair.items(): new.pair[(i, j)] = cut(np.asarray(tab), (i, j))
    for U, tab in getattr(model, "multi", {}).items(): new.multi[U] = cut(np.asarray(tab), U)
    return new


def ratios(task):
    """the seven ratios r_T(s, t) for one (h, h', s, t)"""
    h, h2, s, t, wrong = task; up, P, M, lnZup = CTX["up"], CTX["P"], CTX["M"], CTX["lnZup"]
    fixed = {h: s, h2: t}; out = {}
    if CTX.get("big"):                                                                  # the first version, kept as a cross-check (--big)
        base = copy.deepcopy(up)
        for site, st in ((h, s), (h2, t)):
            pen = np.full(len(base.one[site]), BIG); pen[st] = 0.0; base.one[site] = base.one[site] + pen
    else: base = restrict(up, fixed)
    for name, sets in (("1", ()), ("Bh", (P[h],)), ("Bh2", (P[h2],)), ("BB", (P[h], P[h2])), ("ABh", (P[h], M[h])), ("ABh2", (P[h2], M[h2])), ("AABB", (P[h], M[h], P[h2], M[h2]))):
        mdl = copy.deepcopy(base)
        for its in sets: add_tables(mdl, its, fixed, wrong)
        out[name] = math.exp(mdl.lnZ() - lnZup)
    pl = out["BB"] - out["Bh"] - out["Bh2"] + out["1"]; pu = out["AABB"] - out["BB"] - (out["ABh"] - out["Bh"]) - (out["ABh2"] - out["Bh2"])
    pl_c = max(0.0, pl - SAFE * (out["BB"] + out["Bh"] + out["Bh2"] + out["1"])); pu_c = max(0.0, pu - SAFE * (out["AABB"] + out["BB"] + out["ABh"] + out["Bh"] + out["ABh2"] + out["Bh2"]))
    return (h, h2, s, t), pl, pu, pl_c, pu_c, out["1"]


def single_pass(task):
    """one held site h at state s under the ceiling: the ratios r_1, r_B, r_AB"""
    h, s = task; up, P, M, lnZup = CTX["up"], CTX["P"], CTX["M"], CTX["lnZup"]; fixed = {h: s}; base = restrict(up, fixed); out = {}
    for name, sets in (("1", ()), ("B", (P[h],)), ("AB", (P[h], M[h]))):
        mdl = copy.deepcopy(base)
        for its in sets: add_tables(mdl, its, fixed)
        out[name] = math.exp(mdl.lnZ() - lnZup)
    return out


def floor_pass(task):
    """Z(floor with the held sites at their states and the minus-items of those held sites ADDED to the energy) / Z(floor)"""
    fixed = dict(task); lo, M, lnZlo = CTX["lo"], CTX["M"], CTX["lnZlo"]; mdl = restrict(lo, fixed)
    for h in fixed: add_tables(mdl, M[h], fixed, None, +1.0)
    return math.exp(mdl.lnZ() - lnZlo)


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; ENUM = "--enum" in a; N = int(a[a.index("--N") + 1]) if "--N" in a else 400000
    budget = int(a[a.index("--budget") + 1]) if "--budget" in a else 60; procs = int(a[a.index("--procs") + 1]) if "--procs" in a else 1; t0 = time.time()
    got, text = capture([seq, m, w] + (["--enum"] if ENUM else []))
    for line in text.split("\n"):
        if line.startswith("=== "): log(line[:300])
    items, kind, rts, CL, up, GS, stages, n, k, lnZup, lnZlo, res = (got[q] for q in ("items", "kind", "rts", "CL", "up", "GS", "stages", "n", "k", "lnZup", "lnZlo", "res")); k = [int(v) for v in k]
    name = stages[-1][0]; gks = sorted(GS[name]); corrected = res[name]; width = corrected[1] - corrected[0]
    jp = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (+1, 0) and rts[j] is not None]; jm = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (-1, 0) and rts[j] is not None]
    hs = sorted({int(gk[1]) for gk in gks}); H = len(hs)
    P = {h: [items[j] for j in jp if int(rts[j][1]) == h] for h in hs}; M = {h: [items[j] for j in jm if int(rts[j][1]) == h] for h in hs}
    for h in hs: assert all(h in tuple(it[0]) for it in P[h] + M[h])
    A_g = sum(GS[name][gk]["e"] for gk in gks); C_g = sum(GS[name][gk]["cp"] for gk in gks)
    CTX.update(up=up, P=P, M=M, lnZup=lnZup, big="--big" in a)
    assert abs(up.lnZ() - lnZup) < 1e-9

    def solve(C):
        v = lnZlo
        for _ in range(400): v = lnZlo - math.log1p(C * math.exp(lnZup - v))
        return v
    lo_old = lnZup + math.log1p(A_g * (1 - SAFE)); up_old = solve(C_g * (1 - SAFE))
    log(f"(0) {len(gks)} groups on {H} held sites {hs}; the driver's corrected bracket [{corrected[0]:.7f}, {corrected[1]:.7f}], width {width:.4g}; (LP) and (UP) recomputed here from its exact group means: "
        f"[{lo_old:.7f}, {up_old:.7f}] [{time.time() - t0:.0f}s]")
    # ---- the states: all of them, or samples of the ceiling
    if ENUM:
        X = np.asarray(got["st"]); wt = np.asarray(got["wu"], dtype=float); how = f"every state ({len(X)})"
    else:
        X = up.sample(N, np.random.default_rng(20261126), BETA); wt = np.full(N, 1.0 / N); how = f"{N} exact samples of the ceiling (seed 20261126)"
    b = {h: np.expm1(BETA * SR.items_value(P[h], X)) for h in hs}; a_ = {h: np.expm1(BETA * SR.items_value(M[h], X)) for h in hs}
    est = {}
    for i in range(H):
        for j in range(i + 1, H):
            h, h2 = hs[i], hs[j]; tl = wt * b[h] * b[h2]; tu = wt * (a_[h] * a_[h2] * (1 + b[h]) * (1 + b[h2]) + a_[h] * (1 + b[h]) * b[h2] + a_[h2] * (1 + b[h2]) * b[h])
            code = X[:, h] * k[h2] + X[:, h2]; bl = np.bincount(code, weights=tl, minlength=k[h] * k[h2]); bu = np.bincount(code, weights=tu, minlength=k[h] * k[h2])
            for c in range(k[h] * k[h2]):
                if ENUM or bl[c] > 0 or bu[c] > 0: est[(h, h2, c // k[h2], c % k[h2])] = (float(bl[c]), float(bu[c]))
    tot_l = sum(v[0] for v in est.values()); tot_u = sum(v[1] for v in est.values())
    if ENUM or "--all" in a:
        chosen = [(hs[i], hs[j], s_, t_) for i in range(H) for j in range(i + 1, H) for s_ in range(k[hs[i]]) for t_ in range(k[hs[j]])]
        for q in chosen: est.setdefault(q, (0.0, 0.0))
    else:
        byl = sorted(est, key=lambda q: -est[q][0]); byu = sorted(est, key=lambda q: -est[q][1]); chosen = []
        for q1, q2 in zip(byl, byu):
            for q in (q1, q2):
                if q not in chosen and len(chosen) < budget: chosen.append(q)
    log(f"(1) from {how}: {len(est)} pairs of held states (h, h', s, t){'' if ENUM else ' with a non-zero estimated pair term'}; estimated totals: lower {tot_l:.4e}, upper {tot_u:.4e}; "
        f"computed exactly: {len(chosen)} of them ({7 * len(chosen)} passes), carrying {sum(est[q][0] for q in chosen) / max(tot_l, 1e-300):.3f} / {sum(est[q][1] for q in chosen) / max(tot_u, 1e-300):.3f} of the estimated totals")
    tasks = [(q[0], q[1], q[2], q[3], None) for q in chosen]; t_start = time.time()
    if procs > 1:
        with mp.get_context("fork").Pool(procs) as pool: out = pool.map(ratios, tasks, chunksize=1)
    else: out = [ratios(tk) for tk in tasks]
    t_pass = time.time()
    PL = sum(o[3] for o in out); PU = sum(o[4] for o in out); raw_l = sum(o[1] for o in out); raw_u = sum(o[2] for o in out)
    neg = sum(1 for o in out if o[1] < -1e-12 or o[2] < -1e-12)
    # the first-order terms with the groups MERGED per held site: sum_h <b_h> >= sum_g <y_g> and sum_h <a_h (1 + b_h)> >= sum_g <z_g (1 + y_g)>, one held site
    t1c = [(h, s_) for h in hs for s_ in range(k[h])]; r1c = [single_pass(tk) for tk in t1c]
    A_h = sum(max(0.0, r["B"] - r["1"] - SAFE * (r["B"] + r["1"])) for r in r1c); C_h = sum(max(0.0, r["AB"] - r["B"] - SAFE * (r["AB"] + r["B"])) for r in r1c)
    mass = sum(r["1"] for r in r1c) / H; A_use = max(A_g, A_h); C_use = max(C_g, C_h)
    lo_new = lnZup + math.log1p((A_use + PL) * (1 - SAFE)); up_new = solve((C_use + PU) * (1 - SAFE))
    log(f"    first-order terms with the groups merged per held site ({3 * len(t1c)} passes with one held site; the held states of a site carry total mass {mass:.12f}): sum_h <b_h> = {A_h:.6e} "
        f"(by groups: {A_g:.6e}), sum_h <a_h (1 + b_h)> = {C_h:.6e} (by groups: {C_g:.6e})")
    assert abs(mass - 1.0) < 1e-9
    log(f"(2) exact pair terms from the clamped passes: lower {raw_l:.6e} (after the safety margin {PL:.6e}), upper {raw_u:.6e} ({PU:.6e}); terms that came out negative beyond rounding: {neg} (must be 0); {t_pass - t_start:.0f} s for {7 * len(chosen)} passes with {procs} process(es) [{time.time() - t0:.0f}s]")
    if ENUM:
        devl = max(abs(o[1] - est[o[0]][0]) for o in out); devu = max(abs(o[2] - est[o[0]][1]) for o in out)       # absolute: each term is a combination of ratios of size up to 1
        # control: tables sliced at a wrong state of the first held site, for the pair of held states with the largest lower term
        q = max(est, key=lambda q_: est[q_][0]); wr = (q[0], (q[2] + 1) % k[q[0]]); oc = ratios((q[0], q[1], q[2], q[3], wr)); ctl = abs(oc[1] - est[q][0]) / max(est[q][0], 1e-300)
        log(f"(3) each exact pair term against its value from the states: largest absolute deviation {devl:.1e} (lower), {devu:.1e} (upper) -- the terms are combinations of ratios of size up to 1 computed in double "
            f"precision (must be below 1e-11; the totals are {tot_l:.2e} and {tot_u:.2e}; a first version of this check was relative to the totals and failed at 2e-8 on rounding of terms that are exactly zero); "
            f"sums: {raw_l:.9e} against {tot_l:.9e}, {raw_u:.9e} against {tot_u:.9e}; control, tables sliced at a wrong state of one held site: the largest lower term is off by {ctl:.2f} of itself (must be far from 0)")
        assert devl < 1e-11 and devu < 1e-11 and ctl > 1e-3
        bsum = sum(float((wt * b[h]).sum()) for h in hs); absum = sum(float((wt * a_[h] * (1 + b[h])).sum()) for h in hs)
        log(f"    the merged first-order terms against the states: {abs(A_h - bsum):.1e}, {abs(C_h - absum):.1e} below their exact values {bsum:.6e}, {absum:.6e} (the safety margins; must be between 0 and 1e-6)")
        assert 0 <= bsum - A_h < 1e-6 and 0 <= absum - C_h < 1e-6
        lnZ = got["lnZ"]; best = got["best"]
        log(f"(4) exact ln Z = {lnZ:.7f}; inside the new bracket: {lo_new <= lnZ <= up_new}; the new bracket inside the old one: {lo_new >= lo_old - 1e-12 and up_new <= up_old + 1e-12}; "
            f"the routed items put back exactly (enumeration): [{best[0]:.7f}, {best[1]:.7f}]")
        assert lo_new <= lnZ <= up_new and lo_new >= lo_old - 1e-12 and up_new <= up_old + 1e-12
    else:
        # the exact terms against their sample estimates (standard errors from the samples)
        zs = []
        for o in out[:10]:
            h, h2, s, t = o[0]; sel = (X[:, h] == s) & (X[:, h2] == t); v = np.where(sel, b[h] * b[h2], 0.0); se = float(v.std() / math.sqrt(len(v))); zs.append((o[1] - float(v.mean())) / se if se > 0 else 0.0)
        log(f"(3) the ten largest exact lower terms against their sample estimates: deviations in standard errors {', '.join(f'{z:+.1f}' for z in zs)} (heavy-tailed variables: a rough check); "
            f"sum of the exact terms / estimated total over the chosen pairs: {raw_l / max(sum(est[q][0] for q in chosen), 1e-300):.3f} (lower), {raw_u / max(sum(est[q][1] for q in chosen), 1e-300):.3f} (upper)")
        assert neg == 0 and lo_new >= lo_old - 1e-12 and up_new <= up_old + 1e-12
    assert neg == 0
    log(f"(5) certified bracket with pair terms of held sites under the ceiling: [{lo_new:.7f}, {up_new:.7f}], width {up_new - lo_new:.4g}, against [{lo_old:.7f}, {up_old:.7f}], width {up_old - lo_old:.4g}: "
        f"narrowed by {1 - (up_new - lo_new) / (up_old - lo_old):.3f} of the width (lower end +{(lo_new - lo_old) / (up_old - lo_old):.3f}, upper end -{(up_old - up_new) / (up_old - lo_old):.3f})")
    # ---- the floor side: Z(E) <= Z(m_- + s_-) = Z(m_-) < prod_h (1 - c_h) >_floor,  c_h = 1 - e^{-beta S-_h} in [0, 1), and by the second
    # Bonferroni inequality  prod_h (1 - c_h) <= 1 - sum_h c_h + sum_{h<h'} c_h c_h'  (every pair is needed: none can be dropped).
    # < e^{-beta S-_h} >_floor = sum_s Z(floor, x_h = s, + S-_h) / Z(floor);  < e^{-beta (S-_h + S-_h')} >_floor likewise with two held sites.
    if "--nofloor" not in a:
        lo = got["lo"]; CTX.update(lo=lo, lnZlo=lnZlo); assert abs(lo.lnZ() - lnZlo) < 1e-9; t_f = time.time()
        t1 = [((h, s_),) for h in hs for s_ in range(k[h])]; t2 = [((hs[i], s_), (hs[j], t_)) for i in range(H) for j in range(i + 1, H) for s_ in range(k[hs[i]]) for t_ in range(k[hs[j]])]
        if procs > 1:
            with mp.get_context("fork").Pool(procs) as pool: r1 = pool.map(floor_pass, t1, chunksize=8); r2 = pool.map(floor_pass, t2, chunksize=64)
        else: r1 = [floor_pass(tk) for tk in t1]; r2 = [floor_pass(tk) for tk in t2]
        u1 = {h: 0.0 for h in hs}; u2 = {}
        for tk, v in zip(t1, r1): u1[tk[0][0]] += v
        for tk, v in zip(t2, r2): u2[(tk[0][0], tk[1][0])] = u2.get((tk[0][0], tk[1][0]), 0.0) + v
        c1 = {h: 1.0 - u1[h] for h in hs}; c2 = {q: 1.0 - u1[q[0]] - u1[q[1]] + u2[q] for q in u2}
        negf = sum(1 for v in list(c1.values()) + list(c2.values()) if v < -1e-11)
        B1 = 1.0 - sum(c1.values()); B2 = B1 + sum(c2.values()); margin = SAFE * (1 + len(c1) + 4 * len(c2)); up_floor = lnZlo + math.log(B2 + margin)
        log(f"(6) the floor side, {len(t1)} passes with one held site and {len(t2)} with two ({time.time() - t_f:.0f} s): sum_h <c_h> = {sum(c1.values()):.6e}, sum_(h<h') <c_h c_h'> = {sum(c2.values()):.6e} "
            f"(means that came out negative beyond rounding: {negf}, must be 0); Z(m_- + s_-) / Z(m_-) lies in [{B1:.9f}, {B2:.9f}] (first and second Bonferroni sums); "
            f"**upper end from the second sum: {up_floor:.7f}** (the ceiling route with pair terms: {up_new:.7f}; (UP): {up_old:.7f})")
        assert negf == 0
        if ENUM:
            el = lo.energy(X); wl = np.exp(-BETA * (el - el.min())); wl /= wl.sum(); Sm = {h: SR.items_value(M[h], X) for h in hs}
            d1 = max(abs(float((wl * np.exp(-BETA * Sm[h])).sum()) - u1[h]) for h in hs); d2 = max(abs(float((wl * np.exp(-BETA * (Sm[q[0]] + Sm[q[1]]))).sum()) - u2[q]) for q in u2)
            ex = float((wl * np.exp(-BETA * sum(Sm.values()))).sum()); putback = lnZlo + math.log(ex)
            # control: the FIRST Bonferroni sum taken as an upper end must fall below the exact put-back value (it is a lower bound of it)
            log(f"    against every state: the one-site and two-site means deviate by at most {d1:.1e} and {d2:.1e} (must be below 1e-11); the exact value of Z(m_- + s_-) / Z(m_-) is {ex:.9f} "
                f"(inside the two sums: {B1 - 1e-12 <= ex <= B2 + 1e-12}); the items put back exactly give {putback:.7f} (the driver: {got['best'][1]:.7f}); exact ln Z = {got['lnZ']:.7f} <= the new upper end: {got['lnZ'] <= up_floor}; "
                f"control, the first sum used as an upper end, {lnZlo + math.log(B1):.7f}: below the put-back value by {putback - (lnZlo + math.log(B1)):.2e} (must be >= 0: it is not an upper end)")
            assert d1 < 1e-11 and d2 < 1e-11 and B1 - 1e-12 <= ex <= B2 + 1e-12 and got["lnZ"] <= up_floor and abs(putback - got["best"][1]) < 1e-9
        up_best = min(up_new, up_floor)
    else: up_best = up_new
    log(f"(7) **certified bracket: [{lo_new:.7f}, {up_best:.7f}], width {up_best - lo_new:.4g}** against the driver's [{lo_old:.7f}, {up_old:.7f}], width {up_old - lo_old:.4g}: "
        f"narrowed by **{1 - (up_best - lo_new) / (up_old - lo_old):.3f}** of the width (lower end +{(lo_new - lo_old) / (up_old - lo_old):.3f}, upper end -{(up_old - up_best) / (up_old - lo_old):.3f})")
    if ENUM: assert lo_new <= got["lnZ"] <= up_best
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
