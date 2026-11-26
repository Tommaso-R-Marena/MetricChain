#!/usr/bin/env python3
"""Addendum A17 (13): CERTIFIED ROTAMER POPULATIONS FROM A CERTIFIED SANDWICH -- coordinator's script.

If  m_- <= E <= m_+  at every state (workstream P3's certificate; workstream P6's banded pair form of it), then for
every event A the restricted sums satisfy  Z(A; m_+) <= Z(A; E) <= Z(A; m_-),  and since the odds
Z_E(A)/Z_E(A^c) increase in Z_E(A) and decrease in Z_E(A^c),

     P_E(A)  in  [ Z+(A) / (Z+(A) + Z-(A^c)),   Z-(A) / (Z-(A) + Z+(A^c)) ],        Z+- := Z( . ; m_+-)          (*)

an interval of width  D_A + D_{A^c}  in log-odds,  D_S = ln Z-(S) - ln Z+(S).  It cannot be improved from the
sandwich alone (A and A^c are disjoint, so the energy function equal to m_- on A and m_+ on A^c lies in the sandwich).
For A = {x_i = a} the restricted sums are transfer-matrix sums of the same banded models with the other states of
site i removed.  NO sampling and NO further evaluation of the solvent term: everything is read off the certificate.

What is whose: the sandwich models are workstream P6's (ws_P6/p6lib.make_models, which calls workstream P3's
pwmodel.build_band_models), imported read-only; the cached ball values and pair sums are theirs.  Mine: (*), the
restricted sums, the validation against enumeration below.

Part 1 (validation): on enumerated instances the exact populations must lie inside (*) at every site and state.
Part 2: Ace-Val20-NMe on PPII (3.5e9 assignments), orders 3, 4, 5, and Ace-Val30-NMe on the strand (2.1e14), order 4;
site form (P3) and banded pair form (P6), band 8.

Model-relative throughout: populations of the rotamer model (ff14SB known part + GBn2 solvent term, fixed backbone,
P2's rotamer grid) -- not of a molecule.
Run:  python3 -B certified_populations.py > certified_populations.log      (one core, about a minute)
"""
import os, sys, math, json, time
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, "..", "ws_P6"))
sys.path.insert(0, P6)
import p6lib as L                      # workstream P6 (read-only)
pw = L.pw; BETA = L.BETA
BIG = 1.0e5                            # kcal/mol added to the removed states of one site (exp(-beta*BIG) = 0 exactly)


def log(s): print(s, flush=True)


def restricted(model, i):
    """ln sum_{x: x_i = a} exp(-beta model(x)) for every a, by the model's own transfer matrix."""
    old = model.one[i]; out = np.empty(len(old))
    for a in range(len(old)):
        pen = np.full(len(old), BIG); pen[a] = 0.0
        model.one[i] = old + pen
        out[a] = model.lnZ()
    model.one[i] = old
    return out


def brackets(lo, up):
    """per site: arrays (p_low, p_high, log-odds width) over the states of the site; plus consistency defects."""
    n = lo.n; res = []; defect = 0.0
    lzl, lzu = lo.lnZ(), up.lnZ()
    for i in range(n):
        a_lo = restricted(lo, i); a_up = restricted(up, i)          # ln Z-(x_i = a) >= ln Z+(x_i = a)
        defect = max(defect, abs(logsumexp(a_lo) - lzl), abs(logsumexp(a_up) - lzu))
        k = len(a_lo); pl = np.empty(k); ph = np.empty(k); wd = np.empty(k)
        for a in range(k):
            if k == 1:                                              # a site with one state: the population is 1
                pl[a] = ph[a] = 1.0; wd[a] = 0.0; continue
            rest = [b for b in range(k) if b != a]
            lo_odds = a_up[a] - logsumexp(a_lo[rest])               # ln [Z+(A) / Z-(A^c)]
            hi_odds = a_lo[a] - logsumexp(a_up[rest])               # ln [Z-(A) / Z+(A^c)]
            pl[a] = 1.0 / (1.0 + math.exp(-lo_odds)); ph[a] = 1.0 / (1.0 + math.exp(-hi_odds)); wd[a] = hi_odds - lo_odds
        res.append((pl, ph, wd))
    return res, lzl, lzu, defect


def have(seq, bb, tau, m, w):
    stem = os.path.join(P6, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}")
    return os.path.exists(stem + ".npz") or os.path.exists(f"{stem}_w{w}.npz")


def summary(tag, m, form, w, lo, up, x0, exact=None):
    t1 = time.time()
    res, lzl, lzu, defect = brackets(lo, up)
    n = lo.n; x0 = list(x0)
    D = lzl - lzu
    # the anchor configuration: e^{-beta E(x0)} lies between the two models' Boltzmann factors at x0
    st0 = np.array([x0]); e_lo = float(lo.energy(st0)[0]); e_up = float(up.energy(st0)[0])
    pa_lo = math.exp(-BETA * e_up - lzl); pa_hi = math.exp(-BETA * e_lo - lzu)
    off_lo = sum(1.0 - res[i][1][x0[i]] for i in range(n)); off_hi = sum(1.0 - res[i][0][x0[i]] for i in range(n))
    wd_all = np.concatenate([r[2] for r in res])
    wd_anchor = np.array([res[i][2][x0[i]] for i in range(n)])
    minors = [(res[i][1][a], res[i][0][a], i, a) for i in range(n) for a in range(len(res[i][0])) if a != x0[i]]
    minors.sort(reverse=True)
    top = minors[0]
    # relative half-width of the minor populations: (p_high - p_low) / (p_high + p_low)
    rel = np.array([(h - l) / (h + l) for h, l, _, _ in minors])
    row = dict(tag=tag, m=m, form=form, w=w, n=n, lnZ_lo=lzu, lnZ_hi=lzl, D=D, anchor_prob=[pa_lo, pa_hi], n_off=[off_lo, off_hi],
               logodds_width_max=float(wd_all.max()), logodds_width_median=float(np.median(wd_all)),
               largest_minor=dict(site=int(top[2]), state=int(top[3]), p_low=float(top[1]), p_high=float(top[0])),
               minor_rel_halfwidth_max=float(rel.max()), minor_rel_halfwidth_median=float(np.median(rel)), consistency_defect=defect,
               sites=[dict(p_low=[float(v) for v in r[0]], p_high=[float(v) for v in r[1]]) for r in res])
    s = (f"  {tag:<10} m={m} {form} w={w}: ln Z in [{lzu:.6f}, {lzl:.6f}] (D = {D:.2e});  P(anchor configuration) in [{pa_lo:.6f}, {pa_hi:.6f}];  "
         f"mean number of sites off the anchor in [{off_lo:.5f}, {off_hi:.5f}];  log-odds width of a site population: max {wd_all.max():.2e}, "
         f"median {np.median(wd_all):.2e} (anchor states: max {wd_anchor.max():.2e});  largest minor population: site {top[2]} state {top[3]} "
         f"in [{top[1]:.6f}, {top[0]:.6f}];  relative half-width of minor populations: max {rel.max():.2e}, median {np.median(rel):.2e}")
    if exact is not None:
        nchk = 0; nviol = 0; worst = 0.0
        for i in range(n):
            for a in range(len(res[i][0])):
                nchk += 1; p = exact[i][a]
                if not (res[i][0][a] <= p * (1 + 1e-10) + 1e-300 and p <= res[i][1][a] * (1 + 1e-10)):
                    nviol += 1
                # where the exact value sits inside the bracket (0 = lower end, 1 = upper end)
                if res[i][1][a] > res[i][0][a]:
                    worst = max(worst, abs((p - res[i][0][a]) / (res[i][1][a] - res[i][0][a]) - 0.5))
        row.update(checks=nchk, violations=nviol)
        s += f";  EXACT populations inside: {nchk - nviol} of {nchk} (violations {nviol})"
    log(s + f"  [{time.time() - t1:.1f}s]")
    return row


def exact_populations(G, seq, bb, tau, c0, h, J):
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False)
    E = pw.f_energy(st, c0, h, J) + g
    p = np.exp(-BETA * (E - E.min())); Z = p.sum(); p /= Z
    pops = [np.bincount(st[:, i], weights=p, minlength=G.k[i]) for i in range(G.ns)]
    return pops, float(math.log(Z) - BETA * E.min()), E, st, src


t0 = time.time(); out = dict(validation=[], large=[])
log("=== Part 1: validation on enumerated instances (exact populations against the bracket (*))")
tot_chk = tot_viol = 0
for seq, bb, tau, ms in (("V8", "E", 0.70, (3, 4, 5)), ("V8", "P2", 0.70, (3, 4, 5)), ("V10", "E", 0.70, (3, 4, 5)), ("V10", "P2", 0.70, (3, 4, 5)),
                         ("V12", "E", 0.70, (4, 5)), ("V12", "P2", 0.70, (4, 5)), ("L8", "E", 0.60, (3, 4, 5)), ("L8", "H", 0.60, (4, 5, 6)),
                         ("S6", "E", 0.70, (3, 4)), ("F6", "E", 0.60, (3, 4, 5))):
    sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd
    w = min(8, G.ns - 1)
    todo = [m for m in ms if have(seq, bb, tau, m, w)]
    if not todo:
        log(f"  {seq}/{bb}: no cached pair sums of workstream P6 -- skipped"); continue
    pops, lnZE, E, st, src = exact_populations(G, seq, bb, tau, c0, h, J)
    log(f"  {seq}/{bb} tau {tau}: {len(st)} states enumerated ({src}); ln Z(E) = {lnZE:.6f}; exact P(anchor state) per site: "
        f"min {min(pops[i][x0[i]] for i in range(G.ns)):.4f}, max {max(pops[i][x0[i]] for i in range(G.ns)):.4f}")
    for m in todo:
        for form in ("S", "B"):
            lo, up, info = L.make_models(seq, bb, tau, m, w, form, setup_data=sd)
            ml, mu = lo.energy(st), up.energy(st)
            nbad = int((ml > E + 1e-9).sum() + (mu < E - 1e-9).sum())
            row = summary(f"{seq}/{bb}", m, form, w, lo, up, x0, exact=pops)
            row.update(states=int(len(st)), sandwich_violations=nbad, lnZ_E=lnZE, inside=bool(row["lnZ_lo"] <= lnZE <= row["lnZ_hi"]))
            assert nbad == 0 and row["inside"], "sandwich violated"
            tot_chk += row["checks"]; tot_viol += row["violations"]
            out["validation"].append(row)
log(f"  TOTAL: {tot_chk} population checks, {tot_viol} violations")
assert tot_viol == 0

log("=== Part 2: twenty and thirty residues (no enumeration possible; nothing sampled, nothing evaluated)")
for seq, bb, tau, ms in (("V20", "P2", 0.70, (3, 4, 5)), ("V30", "E", 0.70, (4,))):
    sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd
    log(f"  {seq}/{bb} tau {tau}: {G.ns} sites, states per site {min(G.k)}..{max(G.k)}, 10^{sum(math.log10(k) for k in G.k):.2f} assignments; anchor {''.join(str(v) for v in x0)}")
    for m in ms:
        if not have(seq, bb, tau, m, 8):
            log(f"    m = {m}: no cached pair sums -- skipped"); continue
        for form in ("S", "B"):
            lo, up, info = L.make_models(seq, bb, tau, m, 8, form, setup_data=sd)
            row = summary(f"{seq}/{bb}", m, form, 8, lo, up, x0)
            row.update(nball=info["nball"]); out["large"].append(row)
    best = [r for r in out["large"] if r["tag"] == f"{seq}/{bb}" and r["form"] == "B"][-1]
    log(f"    per-site certified populations at the highest order (banded pair form, m = {best['m']}), state by state [low, high]:")
    for i, srow in enumerate(best["sites"]):
        log(f"      site {i:2d} (anchor state {x0[i]}): " + "  ".join(f"{a}: [{l:.6f}, {h:.6f}]" for a, (l, h) in enumerate(zip(srow["p_low"], srow["p_high"]))))

log("=== Part 3: the same populations with the theory division's sandwich sampler (their Proposition 11.113), from the 50 000 accepted "
    "points and energies STORED by workstream P6 (no new sample, no new evaluation, except the spot check (e))")
seq, bb, tau, m, form, w = "V20", "P2", 0.70, 5, "B", 8
fn = os.path.join(P6, "out", f"sampler_{L.tagname(seq, bb, tau)}_m{m}_{form}_w{w}.npz")
if not os.path.exists(fn):
    log("  stored sampler output of workstream P6 not found -- part 3 skipped")
else:
    z = np.load(fn); st = z["states"].astype(int); Es = z["E"]; N = len(st)
    sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd
    lo, up, info = L.make_models(seq, bb, tau, m, w, form, setup_data=sd)
    lzl, lzu = lo.lnZ(), up.lnZ(); D = lzl - lzu; n = lo.n
    # (a) the stored model energies against my model objects
    ml, mu = lo.energy(st), up.energy(st)
    log(f"  (a) {N} stored points ({len(np.unique(st, axis=0))} distinct); stored m_- and m_+ against the models rebuilt here: largest differences "
        f"{np.abs(ml - z['m_lo']).max():.1e}, {np.abs(mu - z['m_up']).max():.1e} kcal/mol; m_- > E at {int((ml > Es).sum())} points, m_+ < E at {int((mu < Es).sum())}")
    # (b) is the stored sample a sample of q?  exact site marginals of q = (e^{-m_-} - e^{-m_+}) / (Z_- - Z_+) against the frequencies
    zs = []; qex = []
    for i in range(n):
        a_lo = restricted(lo, i); a_up = restricted(up, i)
        q = (np.exp(a_lo - lzl) - np.exp(a_up - lzl)) / (-math.expm1(-D))
        f = np.bincount(st[:, i], minlength=len(q)) / N
        zs.extend(((f - q) / np.sqrt(q * (1 - q) / N)).tolist()); qex.append((a_lo, a_up))
    zs = np.array(zs)
    log(f"  (b) frequencies of the {len(zs)} site states in the stored sample against the exact marginals of q (restricted transfer-matrix sums): "
        f"z-scores max |z| = {np.abs(zs).max():.2f}, root mean square {math.sqrt(float((zs ** 2).mean())):.2f} (independent standard normals would give about 1; "
        f"the {len(zs)} are not independent)")
    # (c) W recomputed from the stored energies; the bracket of ln Z
    r = BETA * (Es - ml); U = BETA * (mu - ml)
    W = np.expm1(-(r - U)) / np.expm1(U)            # (e^{-r} - e^{-U}) / (1 - e^{-U})
    delta = 0.05; t = math.sqrt(math.log(2 / delta) / (2 * N)); mW = float(W.mean())
    lnz = lambda v: lzu + math.log1p(math.expm1(D) * v)
    log(f"  (c) W recomputed: in [{W.min():.4f}, {W.max():.4f}], mean {mW:.6f} (sd {W.std(ddof=1):.4f}); Hoeffding half-width {t:.6f} at level {1 - delta}: "
        f"ln Z(E) in [{lnz(mW - t):.6f}, {lnz(mW + t):.6f}], point estimate {lnz(mW):.6f} +- {math.expm1(D) * W.std(ddof=1) / math.sqrt(N) / (1 + math.expm1(D) * mW):.6f} (one standard error)")
    # (d) simultaneous brackets of all site populations: P(A) = [Z+(A) + (Z- - Z+) E_q(1_A W)] / [Z+ + (Z- - Z+) E_q W]
    nint = sum(len(a) for a, _ in qex) + 1; tt = math.sqrt(math.log(2 * nint / delta) / (2 * N))
    rows = []; worst_rel = 0.0
    for i in range(n):
        a_lo, a_up = qex[i]; row = []
        for a in range(len(a_lo)):
            ea = float((W * (st[:, i] == a)).mean())
            num = lambda v: math.exp(a_up[a] - lzu) + math.expm1(D) * v          # in units of Z+
            den = lambda v: 1.0 + math.expm1(D) * v
            pl = num(max(ea - tt, 0.0)) / den(min(mW + tt, 1.0)); ph = num(min(ea + tt, 1.0)) / den(max(mW - tt, 0.0))
            row.append((pl, ph)); worst_rel = max(worst_rel, (ph - pl) / (ph + pl))
        rows.append(row)
    log(f"  (d) all {nint - 1} site populations simultaneously with probability >= {1 - delta} (Hoeffding, half-width {tt:.6f} for each of {nint} means): "
        f"largest relative half-width {worst_rel:.2e}")
    for i in (0, 1, 9, 18, 19):
        log(f"      site {i:2d}: " + "  ".join(f"{a}: [{l:.6f}, {h:.6f}]" for a, (l, h) in enumerate(rows[i])))
    # (e) spot check of the stored energies with workstream P3's evaluator
    rng = np.random.default_rng(20261126); idx = rng.choice(N, 300, replace=False)
    Echk = pw.f_energy(st[idx], c0, h, J) + G.bulk_energy(st[idx])
    log(f"  (e) E re-evaluated at 300 of the stored points (P3's evaluator, called here): largest difference from the stored value {np.abs(Echk - Es[idx]).max():.1e} kcal/mol")
    out["sampler"] = dict(N=N, D=D, mean_W=mW, t=t, lnZ=[lnz(mW - t), lnz(mW + t)], z_max=float(np.abs(zs).max()), z_rms=math.sqrt(float((zs ** 2).mean())),
                          simultaneous_halfwidth=tt, populations=[[list(v) for v in row] for row in rows], worst_rel_halfwidth=worst_rel)
json.dump(out, open(os.path.join(HERE, "certified_populations.json"), "w"), indent=1)
log(f"ALL DONE {time.time() - t0:.0f} s")
