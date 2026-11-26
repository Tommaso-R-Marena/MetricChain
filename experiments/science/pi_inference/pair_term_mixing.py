#!/usr/bin/env python3
"""The theory division's pair-term inequality (THY-MSG-0018 section 2) on our routing: how much of the pair term of
Proposition A17.19 can it reach?  (Prediction in the research log of 2026-11-26, 20:34 UTC, before this script existed.)

Their statement [P by them; re-read here: a pointwise density bound applied to a non-negative integrand]:
for non-negative y_g, y_h that are functions of two windows and of the held site(s) x,
    < y_g y_h >  >=  sum_x P(x) (1 - psi_x) < y_g | x > < y_h | x > ,
if, given x, the joint law of the two windows has density at least 1 - psi_x against the product of its conditional marginals.
It needs conditional means given the held sites and a LOWER MIXING COEFFICIENT psi_x, no joint law of two groups.

Our groups (first_order_recovery.py): (direction, held site, window); a group's variable y_g = e^{beta S+_g} - 1 depends on its
held site and on the sites of its items.  For a pair (g, h): x = the held sites of both; "windows" = the other sites of each
group.  If the two windows share a site the joint law is singular against the product and psi_x = 1: the inequality gives 0.
Per pair, on an enumerated instance (every state, ceiling weights):
    exact      < y_g y_h >
    product    < y_g > < y_h >                                   (group means only: what the driver already has)
    cond       sum_x P(x) < y_g | x > < y_h | x >                (psi = 0: conditional independence given the held sites)
    bound      sum_x P(x) (1 - psi_x) < y_g | x > < y_h | x >     with the TRUE psi_x, computed here by enumeration on the support of
               y_g (x) y_h given x -- the best any certificate of a mixing coefficient could give; and the same with psi_x
               taken over ALL pairs of window states (the statement as written).
Reported by category: windows overlap / windows disjoint with one common held site / disjoint with two held sites.
Checks: bound <= exact for every pair (the inequality itself; violations must be 0); the group means from the states against
the driver's exact means; control: the "bound" with psi_x replaced by -1 (i.e. twice the conditional product) must EXCEED
the exact value for some pair with disjoint windows (the test of the inequality can fail) -- where an instance has no such
pair the script says so.
Without --enum (Lys12): exact samples of the ceiling; only the split of the exact pair term by category and the plain
product are reported (psi cannot be computed from samples).
Run: python3 -B pair_term_mixing.py K5 4 2 --enum > pair_term_mixing_K5_m4_w2_enum.log
     python3 -B pair_term_mixing.py K12 4 4 > pair_term_mixing_K12_m4_w4.log
"""
import sys, time, math, resource
import numpy as np
import first_order_recovery as FR
from group_coupling import capture
SR = FR.SR; BETA = FR.BETA


def log(s): print(s, flush=True)


def codes(X, sites, k):
    c = np.zeros(len(X), dtype=np.int64); size = 1
    for u in sites: c = c * k[u] + X[:, u]; size *= k[u]
    return c, size


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; ENUM = "--enum" in a; N = int(a[a.index("--N") + 1]) if "--N" in a else 400000; t0 = time.time()
    got, text = capture([seq, m, w] + (["--enum"] if ENUM else []))
    for line in text.split("\n"):
        if line.startswith("=== "): log(line[:300])
    items, kind, rts, CL, up, GS, stages, n, k = (got[q] for q in ("items", "kind", "rts", "CL", "up", "GS", "stages", "n", "k")); k = [int(v) for v in k]
    name = stages[-1][0]; gks = sorted(GS[name]); jp = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (+1, 0)]
    groups = [[items[j] for j in jp if rts[j] == gk] for gk in gks]; G = len(gks)
    held = [int(gk[1]) for gk in gks]; U = [sorted(set(int(u) for it in g for u in it[0])) for g in groups]
    for gi in range(G): assert all(held[gi] in it[0] for it in groups[gi]), "every item of a group contains its held site"
    if ENUM:
        X = np.asarray(got["st"]); wt = np.asarray(got["wu"], dtype=float); how = f"every state ({len(X)}), ceiling weights"
    else:
        X = up.sample(N, np.random.default_rng(20261126), BETA); wt = np.full(N, 1.0 / N); how = f"{N} exact independent samples of the ceiling model (seed 20261126)"
    S = np.stack([SR.items_value(g, X) for g in groups]); assert (S >= 0).all(); y = np.expm1(BETA * S); ey = (y * wt[None]).sum(axis=1)
    eg = np.array([GS[name][gk]["e"] for gk in gks])
    log(f"(0) {G} groups (direction, held site, window start): {', '.join(f'{gk[0]}/{gk[1]}/{gk[2]}' for gk in gks[:12])}{' ...' if G > 12 else ''}; sites of each group's items: {U[:8]}{' ...' if G > 8 else ''}; "
        f"means <y_g> from {how} against the driver's exact means: largest relative deviation {float(np.abs(ey - eg).max() / eg.max()):.1e} [{time.time() - t0:.0f}s]")
    cat_names = ("windows overlap (the inequality gives 0)", "disjoint windows, one common held site", "disjoint windows, two held sites")
    tot = {c: dict(n=0, exact=0.0, product=0.0, cond=0.0, bound=0.0, boundall=0.0) for c in cat_names}; viol = 0; ctl = 0; rows = []; minpsi = []
    for gi in range(G):
        for hi in range(gi + 1, G):
            Hs = sorted({held[gi], held[hi]}); Wg = [u for u in U[gi] if u not in Hs]; Wh = [u for u in U[hi] if u not in Hs]
            exact = float((wt * y[gi] * y[hi]).sum()); prod = float(eg[gi] * eg[hi])
            if set(Wg) & set(Wh): cat = cat_names[0]; cond = bound = boundall = 0.0
            else:
                cat = cat_names[1] if len(Hs) == 1 else cat_names[2]; cond = bound = boundall = 0.0
                if ENUM:
                    cx, nx = codes(X, Hs, k); ca, na = codes(X, Wg, k); cb, nb = codes(X, Wh, k); psis = []
                    for xv in np.unique(cx):
                        sel = cx == xv; px = float(wt[sel].sum()); wv = wt[sel] / px; av = ca[sel]; bv = cb[sel]
                        Jm = np.zeros((na, nb)); np.add.at(Jm, (av, bv), wv); Pa = Jm.sum(axis=1); Pb = Jm.sum(axis=0)
                        ya = np.zeros(na); yb = np.zeros(nb); ya[av] = y[gi][sel]; yb[bv] = y[hi][sel]                   # y_g depends on (x, a) only, y_h on (x, b) only
                        mg = float(Pa @ ya); mh = float(Pb @ yb); cnd = px * mg * mh; cond += cnd
                        if mg > 0 and mh > 0:
                            with np.errstate(divide="ignore", invalid="ignore"): ratio = Jm / np.outer(Pa, Pb)
                            ok = np.outer(Pa > 0, Pb > 0); sup = ok & np.outer(ya > 0, yb > 0)
                            rs = float(ratio[sup].min()); ra = float(ratio[ok].min()); bound += cnd * min(rs, 1.0); boundall += cnd * min(ra, 1.0); psis.append((cnd, 1.0 - rs))
                    # the dependence check behind "y_g depends on (x, a) only": the conditional means must reproduce <y_g>
                    if psis: minpsi.append((exact, sum(c * p for c, p in psis) / max(sum(c for c, p in psis), 1e-300)))
                    viol += int(bound > exact * (1 + 1e-9) + 1e-300); ctl += int(2.0 * cond > exact * (1 + 1e-9))
            d = tot[cat]; d["n"] += 1; d["exact"] += exact; d["product"] += prod; d["cond"] += cond; d["bound"] += bound; d["boundall"] += boundall
            rows.append((exact, gks[gi], gks[hi], cat, prod, cond, bound))
    q_all = sum(d["exact"] for d in tot.values()); A = float(eg.sum())
    log(f"(1) the exact pair term sum_(g<h) <y_g y_h> = {q_all:.6e} over {G * (G - 1) // 2} pairs; ln(1 + A + q) - ln(1 + A) = {math.log1p(A + q_all) - math.log1p(A):.4e} nats; "
        f"the plain product of the group means, summed: {sum(d['product'] for d in tot.values()):.6e} ({sum(d['product'] for d in tot.values()) / q_all:.3f} of the exact)")
    log("| category of pairs | pairs | share of the exact pair term | product of means / exact | conditional product given the held sites (psi = 0) / exact | the inequality with the true psi on the support / exact | with psi over all window states / exact |")
    log("|---|---|---|---|---|---|---|")
    for c in cat_names:
        d = tot[c]; e = d["exact"]; f = (lambda v: f"{v / e:.3f}" if e > 0 else "—")
        log(f"| {c} | {d['n']} | **{e / q_all:.3f}** | {f(d['product'])} | {f(d['cond']) if ENUM and c != cat_names[0] else '—'} | {('**' + f(d['bound']) + '**') if ENUM and c != cat_names[0] else ('0' if c == cat_names[0] else '—')} | {f(d['boundall']) if ENUM and c != cat_names[0] else ('0' if c == cat_names[0] else '—')} |")
    if ENUM:
        reach = sum(d["bound"] for d in tot.values()); reach0 = sum(d["cond"] for d in tot.values())
        wpsi = sum(e * p for e, p in minpsi) / max(sum(e for e, p in minpsi), 1e-300) if minpsi else float("nan")
        log(f"(2) **the inequality with the best possible mixing coefficients recovers {reach / q_all:.3f} of the exact pair term** (with psi = 0, which no certificate gives: {reach0 / q_all:.3f}); "
            f"the mean true psi over the held states, weighted by their conditional product and then by the pairs' exact term: {wpsi:.3f}")
        ndis = tot[cat_names[1]]["n"] + tot[cat_names[2]]["n"]
        log(f"(3) checks: bound <= exact for every pair: {viol} violations (must be 0); control, twice the conditional product in place of the bound: exceeds the exact value for {ctl} of the {ndis} pairs "
            f"with disjoint windows ({'must be positive' if ndis else 'no such pair in this instance: the inequality is never applied and the control has nothing to test'})")
        assert viol == 0 and (ctl > 0 or ndis == 0)
    rows.sort(key=lambda r: -r[0])
    log("the five pairs with the largest exact term: " + "; ".join(f"{r[1][0]}/{r[1][1]}/{r[1][2]} x {r[2][0]}/{r[2][1]}/{r[2][2]}: exact {r[0]:.3e}, product {r[4]:.3e}, {r[3].split(',')[0].split(' (')[0]}" + (f", cond {r[5]:.3e}, bound {r[6]:.3e}" if ENUM and r[3] != cat_names[0] else "") for r in rows[:5]))
    # groups with a common held site: what merging them (one clamped computation) would give exactly
    same = sum(r[0] for r in rows if r[1][1] == r[2][1]); log(f"(4) pairs of groups with the SAME held site carry {same / q_all:.3f} of the exact pair term (their joint is exact at no extra clamping: merge them); "
                                                              f"pairs with different held sites: {1 - same / q_all:.3f} (exact only with both sites held: k_h k_h' clamped computations per pair of held sites)")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
