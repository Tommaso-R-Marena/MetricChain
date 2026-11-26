#!/usr/bin/env python3
"""P9 step 4 -- HOW MUCH DOES THE RESOLUTION GAIN, measured on the tables and on two Gibbs samples, BEFORE any model
is built (question 3 of the brief; the numbers the prediction is made from).

(A) site by site (the site form, gamma_i(b) = (1/m) sum_{T ni i} max{Theta_T : x_i = b}): the state-independent
    gamma_i^SAb = (1/m) sum_{T ni i} chat_T^SAb; for each stage the ratio to it of max_b gamma_i(b) (must be <= 1), of
    min_b gamma_i(b), and of the BOLTZMANN-TYPICAL value: the mean of gamma_i(x_i) over the states of the pooled
    Gibbs samples with x_i off the anchor.  The table by rotamer is printed for the report.
(B) the same aggregate for every share form F (S, B, T; W = window form) and source (P8's constants 'SAb', the joint
    maxima of stage 1 and 2 as constants, the resolved tables of stage 1 and 2), on each Gibbs sample:
    first-order number 2 beta <pen>, the estimate ln<e^{beta pen}> - ln<e^{-beta pen}>, and the largest beta pen.
(C) the fully resolved envelope sum_{T subset S(x)} Theta_T(x_T) on the samples, against the envelope of constants.
All sample numbers are UNCERTIFIED estimates (Lemma A17.16 of the addenda: lower estimates of a bracket wherever the
penalty reaches several kT).
usage: python3 -B p9_04_gain.py SEQ M [--w W]      writes logs/gain_<tag>_m<M>_w<W>.log, out/gain_....json
"""
import sys
from p9lib import *

a = sys.argv[1:]; seq, m = a[0], int(a[1]); bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
w = int(a[a.index("--w") + 1]) if "--w" in a else 7
stem = f"{tag}_m{m}_w{w}"
log = Log(os.path.join(LOGS, f"gain_{stem}.log"))
log(f"=== p9_04_gain {seq} on {bb}, tau {tau}: order m = {m}, band / window {w}; started {now()}")
LD = Loaded(os.path.join(OUT, f"tables_{stem}.npz")); n, k, x0 = LD.n, LD.k, LD.x0; subs = LD.TB[1].subs
S = {sd: load_gibbs(tag, sd)[0] for sd in (4242, 777)}; XP = np.concatenate([S[4242], S[777]], axis=0)
offP = XP != np.array(x0)[None]
sab, cJ1, cJ2 = LD.TB[1].sab, LD.TB[1].cJ, LD.TB[2].cJ
log(f"    {n} sites, states per site {k}, anchor {x0}; {len(subs)} subsets; Gamma_{m} (kT): SAb {BETA * sab.sum():.5g}, joint maxima stage 1 {BETA * cJ1.sum():.5g}, stage 2 {BETA * cJ2.sum():.5g}; "
    f"pooled Gibbs sample: {len(XP)} states, off-anchor frequencies " + " ".join(f"{v:.2f}" for v in offP.mean(0)))
res = dict(seq=seq, m=m, w=w, sites=[], forms={})
# ---- (A) site by site
gA = form_tables(LD.TB[1], "S", w, resolved=False, const=sab)[0]
g = {s: form_tables(LD.TB[s], "S", w)[0] for s in (1, 2)}
non = LD.TB[1].non
log("(A) SITE FORM, site by site.  gamma^SAb in kT; ratios to it.")
log("| site | states | off-anchor visits in the pooled sample | beta gamma_i^SAb | stage 1: max_b, typical, min_b | stage 2: max_b, typical, min_b |")
log("|---|---|---|---|---|---|")
for i in range(n):
    ref = float(gA[i][non[i]][0]); vis = offP[:, i]; cells = []; row = dict(site=i, k=k[i], visits=int(vis.sum()), gSAb_kT=BETA * ref)
    for s in (1, 2):
        t = g[s][i][non[i]]; typ = float(g[s][i][XP[vis, i]].mean()) / ref if vis.any() else float("nan")
        cells.append(f"{t.max() / ref:.3f}, {typ:.3f}, {t.min() / ref:.4f}")
        row[f"stage{s}"] = dict(max=float(t.max() / ref), typical=typ, min=float(t.min() / ref), by_state=[float(v / ref) for v in t])
    row["freq_by_state"] = [float((XP[:, i] == b).mean()) for b in non[i]]
    res["sites"].append(row)
    log(f"| {i} | {k[i]} | {int(vis.sum())} | {BETA * ref:.4g} | {cells[0]} | {cells[1]} |")
log("    by rotamer (non-anchor states in the order of the domain): frequency in the pooled sample / stage-1 ratio / stage-2 ratio")
for row in res["sites"]:
    log(f"      site {row['site']}: " + "  ".join(f"{f_:.3f}/{r1:.2f}/{r2:.3f}" for f_, r1, r2 in zip(row["freq_by_state"], row["stage1"]["by_state"], row["stage2"]["by_state"])))
# ---- (B) every form and source on the samples
poff = off_frequencies(S[4242], k, x0)


def wpen(X, tabs):
    """value of window-form tables (g1, g2, g3 as dicts over sub-tuples) at the rows of X."""
    out = np.zeros(len(X))
    for part in tabs:
        for K, t in part.items():
            out += t[tuple(X[:, u] for u in K)]
    return out


def est(pen):
    b = BETA * pen
    return dict(first=2.0 * float(b.mean()), expo=float(np.log(np.exp(b).mean()) - np.log(np.exp(-b).mean())), largest=float(b.max()))


log("(B) every share form and source on the two Gibbs samples: 2 beta <pen> [ln<e^(beta pen)> - ln<e^(-beta pen)>; largest beta pen].  Sample 777 first, then 4242.")
log("| form | P8's constants SAb | joint maxima of stage 1 (constants) | joint maxima of stage 2 (constants) | resolved, stage 1 | resolved, stage 2 | stage 2 / SAb (first order, sample 777; 4242) |")
log("|---|---|---|---|---|---|---|")
for form in ("S", "B", "T", "W"):
    cells = []; R = {}
    for name in ("SAb", "cJ1", "cJ2", "s1", "s2"):
        e = {}
        for sd in (777, 4242):
            X = S[sd]
            if name in ("s1", "s2"):
                s = int(name[1])
                pen = wpen(X, window_form(LD.W[s])) if form == "W" else pen_value(X, *form_tables(LD.TB[s], form, w))
            else:
                const = dict(SAb=sab, cJ1=cJ1, cJ2=cJ2)[name]
                pen = wpen(X, window_form_const(subs, const, k, x0, w, poff)) if form == "W" else pen_value(X, *form_tables(LD.TB[1], form, w, resolved=False, const=const))
            e[sd] = est(pen)
        R[name] = e
        cells.append(" / ".join(f"{e[sd]['first']:.3g} [{e[sd]['expo']:.3g}; {e[sd]['largest']:.3g}]" for sd in (777, 4242)))
    res["forms"][form] = R
    ratio = "; ".join(f"{R['s2'][sd]['first'] / max(R['SAb'][sd]['first'], 1e-300):.3g}" for sd in (777, 4242))
    log(f"| {form} | " + " | ".join(cells) + f" | {ratio} |")
# ---- (C) envelopes
log("(C) envelopes sum over T inside S(x): 2 beta <env> [exponential estimate; largest], sample 777 / 4242")
R = {}
for name in ("SAb", "cJ1", "cJ2", "s1", "s2"):
    e = {}
    for sd in (777, 4242):
        env = LD.env[int(name[1])][sd] if name in ("s1", "s2") else const_envelope(subs, dict(SAb=sab, cJ1=cJ1, cJ2=cJ2)[name], S[sd], x0)
        e[sd] = est(env)
    R[name] = e
    log(f"    {name}: " + " / ".join(f"{e[sd]['first']:.3g} [{e[sd]['expo']:.3g}; {e[sd]['largest']:.3g}]" for sd in (777, 4242)))
res["envelope"] = R
json.dump(res, open(os.path.join(OUT, f"gain_{stem}.json"), "w"), indent=1)
log.done()
