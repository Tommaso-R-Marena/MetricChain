#!/usr/bin/env python3
"""R24, item 5 (iii): the sampled rows of the table of addendum item 90 / SCI-MSG-0032 re-measured with the referee's own
exact sampler (r24_common.OwnSampler: own elimination, not BandModel.sample), own evaluation of the item tables, other
seeds, more samples -- and with an error bar on EVERY column, taken from the scatter of independent batches (not from the
within-sample variance, which heavy tails make unreliable), with tail diagnostics.
Also the floor route of r24_item5_enum.py (Bonferroni with pair laws under the floor; the comonotone bound from
single-group laws under the floor), measured from samples of the floor (bounded variables).
Taken from the frame of first_order_recovery.main(): the items, their routes (groups), the two band models, the exact
group means A = sum <y_g> and C' (for the first order), the corrected bracket.  Nothing else of theirs is used.
Run: python3 -B r24_item5_sampled.py K12 4 4 --NB 100000 --BC 60 --BF 100 > r24_item5_sampled_K12_m4_w4.log
     python3 -B r24_item5_sampled.py K5 4 2 --NB 100000 --BC 20 --BF 20 > r24_item5_sampled_K5_m4_w2.log    (validation against enumeration)
"""
import os, sys, time, math, gc
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, PI); sys.path.insert(0, HERE)
import r24_common as C
from r24_item5_enum import esym2


def opt(a, key, default, cast=int):
    return cast(a[a.index(key) + 1]) if key in a else default


def mse(v):
    v = np.asarray(v, float); return float(v.mean()), float(v.std(ddof=1) / math.sqrt(len(v)))


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; NB = opt(a, "--NB", 100000); BC = opt(a, "--BC", 60); BF = opt(a, "--BF", 100); seed = opt(a, "--seed", 2401); t0 = time.time()
    U0_ref = opt(a, "--U0ref", None, float); U0_ref_se = opt(a, "--U0refse", 0.0, float)
    import first_order_recovery as FR
    got, text = C.capture(FR, [seq, m, w], "first_order_recovery.py")
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("| far pairs, terms and") or line.startswith("| nothing"): print("[theirs] " + line[:330], flush=True)
    BETA = FR.BETA
    items, kind, rts, CL, up, lo, GS, stages, res, k, n = (got[q] for q in ("items", "kind", "rts", "CL", "up", "lo", "GS", "stages", "res", "k", "n"))
    lnZup, lnZlo = float(got["lnZup"]), float(got["lnZlo"]); k = list(k); del got; gc.collect()
    name = stages[-1][0]; gks = sorted(GS[name]); Gn = len(gks); gi = {gk: q for q, gk in enumerate(gks)}; corrected = res[name]; width = corrected[1] - corrected[0]
    plus = [[] for _ in gks]; minus = [[] for _ in gks]
    for j in range(len(items)):
        if kind[j][0] in CL and rts[j] in gi:
            it = (tuple(items[j][0]), np.asarray(items[j][1], float))
            if kind[j][1] in (+1, 0): plus[gi[rts[j]]].append(it)
            if kind[j][1] in (-1, 0): minus[gi[rts[j]]].append(it)
    A_ex = sum(GS[name][gk]["e"] for gk in gks); C1_ex = sum(GS[name][gk]["cp"] for gk in gks)
    cu, fu = C.factors_of(up); cl, fl = C.factors_of(lo); Sup = C.OwnSampler(fu, k, -BETA); Slo = C.OwnSampler(fl, k, -BETA)
    print(f"(0) {Gn} groups, {sum(len(p) for p in plus)} plus-items and {sum(len(p) for p in minus)} minus-items with a route; ln Z(m_+): my elimination {Sup.lnZ - BETA * cu:.7f} (driver {lnZup:.7f}); "
          f"ln Z(m_-): {Slo.lnZ - BETA * cl:.7f} (driver {lnZlo:.7f}); corrected bracket [{corrected[0]:.7f}, {corrected[1]:.7f}], width {width:.6g}; exact first-order means of the driver: A = {A_ex:.6e}, C' = {C1_ex:.6e} "
          f"[{time.time() - t0:.0f}s, peak RSS {C.rss():.0f} MB]", flush=True)

    def gv(sets, X):
        out = np.zeros((Gn, len(X)))
        for g, its in enumerate(sets):
            for U, tab in its: out[g] += tab[tuple(X[:, u] for u in U)]
        return out
    rng = np.random.default_rng(seed)
    # ---------------------------------------------------------------- ceiling batches
    keys = ("A", "q", "d", "c1", "c2add", "cjadd", "sumP", "two"); bc = {q: [] for q in keys}; tops = {q: np.zeros(0) for q in ("q", "d", "c2add", "cjadd")}; sq = {q: 0.0 for q in ("q", "d", "c2add", "cjadd")}
    viol_order = 0
    for bno in range(BC):
        X = Sup.sample(NB, rng); Sp = gv(plus, X); Sm = gv(minus, X); y = np.expm1(BETA * Sp); z = np.expm1(BETA * Sm)
        e1, e2, hi = esym2(y); c1 = (z * (1.0 + y)).sum(axis=0)
        pre = np.cumsum(y, axis=0) - y; suf = np.cumsum(y[::-1], axis=0)[::-1] - y; zy = (z * (pre + suf)).sum(axis=0); zz = esym2(z)[1]; c2a = zz + zy
        cj = np.expm1(BETA * Sm.sum(axis=0)) * np.exp(BETA * Sp.sum(axis=0)); cja = cj - c1
        viol_order += int((cja < c2a * (1 - 1e-9) - 1e-9 * (1.0 + cj)).sum())
        for q, v in (("A", e1), ("q", e2), ("d", hi), ("c1", c1), ("c2add", c2a), ("cjadd", cja)): bc[q].append(float(v.mean()))
        bc["sumP"].append(float((Sp > 0).sum(axis=0).mean())); bc["two"].append(float(((Sp > 0).sum(axis=0) >= 2).mean()))
        for q, v in (("q", e2), ("d", hi), ("c2add", c2a), ("cjadd", cja)):
            sq[q] += float((v ** 2).sum()); t = np.concatenate([tops[q], v]); tops[q] = np.partition(t, len(t) - 100)[-100:] if len(t) > 100 else t
        del X, Sp, Sm, y, z, pre, suf
    NC = BC * NB
    print(f"(1) CEILING: {BC} batches of {NB} exact samples of my own sampler (seed {seed}) = {NC} samples [{time.time() - t0:.0f}s, peak RSS {C.rss():.0f} MB]; pointwise C_2-part <= C''-part violated at {viol_order} samples (must be 0)")
    st = {q: mse(bc[q]) for q in keys}
    print(f"    checks against the driver's exact means: A = {st['A'][0]:.6e} +- {st['A'][1]:.1e} ({(st['A'][0] - A_ex) / st['A'][1]:+.2f} s.e. from {A_ex:.6e}); "
          f"C' = {st['c1'][0]:.6e} +- {st['c1'][1]:.1e} ({(st['c1'][0] - C1_ex) / st['c1'][1]:+.2f} s.e. from {C1_ex:.6e}); sum_g P(S+_g > 0) = {st['sumP'][0]:.4f} +- {st['sumP'][1]:.4f}; P(two or more) = {st['two'][0]:.4e}")
    print("| second-order quantity under the ceiling | mean | s.e. from the scatter of batches | s.e. from the within-sample variance | share of the total carried by the 10 / 100 largest samples | largest single sample / total |")
    print("|---|---|---|---|---|---|")
    for q, lab in (("q", "<q> = sum_(g<h) <y_g y_h>"), ("d", "<d> = <prod(1 + y_g)> - 1 - A"), ("c2add", "C_2 - C'"), ("cjadd", "C'' - C'")):
        mu, se_b = st[q]; se_w = math.sqrt(max(sq[q] / NC - mu ** 2, 0.0) / NC); tp = np.sort(tops[q])[::-1]; tot = mu * NC
        print(f"| {lab} | {mu:.6e} | {se_b:.2e} ({100 * se_b / mu:.1f} %) | {se_w:.2e} | {tp[:10].sum() / tot:.3f} / {tp.sum() / tot:.3f} | {tp[0] / tot:.4f} |")
    # ---------------------------------------------------------------- floor batches
    fkeys = ("e", "S1", "S2", "rem", "como", "sumP", "two"); bf = {q: [] for q in fkeys}; viol_b = 0
    for bno in range(BF):
        X = Slo.sample(NB, rng); Sm = gv(minus, X); zeta = -np.expm1(-BETA * Sm); f1, f2, _ = esym2(zeta); e_ = np.exp(-BETA * Sm.sum(axis=0)); rem = (1.0 - f1 + f2) - e_
        viol_b += int((rem < -1e-12).sum())
        lp = np.zeros(NB)
        for g in range(Gn): lp += np.log1p(-np.sort(zeta[g]))                 # comonotone coupling of the empirical laws of this batch
        for q, v in (("e", e_), ("S1", f1), ("S2", f2), ("rem", rem)): bf[q].append(float(v.mean()))
        bf["como"].append(float(np.exp(lp).mean())); bf["sumP"].append(float((Sm > 0).sum(axis=0).mean())); bf["two"].append(float(((Sm > 0).sum(axis=0) >= 2).mean()))
        del X, Sm, zeta
    NF = BF * NB; sf = {q: mse(bf[q]) for q in fkeys}
    print(f"(2) FLOOR: {BF} batches of {NB} = {NF} exact samples [{time.time() - t0:.0f}s, peak RSS {C.rss():.0f} MB]; pointwise Bonferroni violated at {viol_b} samples (must be 0); "
          f"<e^(-beta s_-)> = {sf['e'][0]:.8f} +- {sf['e'][1]:.1e}; S1 = {sf['S1'][0]:.6e} +- {sf['S1'][1]:.1e}; S2 = {sf['S2'][0]:.6e} +- {sf['S2'][1]:.1e}; "
          f"Bonferroni remainder <(1 - S1 + S2) - prod> = {sf['rem'][0]:.3e} +- {sf['rem'][1]:.1e}; sum_g P_floor(S-_g > 0) = {sf['sumP'][0]:.4f}; P(two or more) = {sf['two'][0]:.4e}")
    # ---------------------------------------------------------------- the row, with an error bar on every column
    L = lambda extra: math.log1p(A_ex + extra); dL = 1.0 / (1.0 + A_ex)
    Zm = math.exp(lnZlo - lnZup); v = lambda Cv: lnZup + math.log(Zm - Cv); dv = 1.0 / (Zm - C1_ex)
    low_pair = (L(st["q"][0]) - L(0)) / width, st["q"][1] * dL / width; low_joint = (L(st["d"][0]) - L(0)) / width, st["d"][1] * dL / width
    v1 = v(C1_ex); up_pair = (v1 - v(C1_ex + st["c2add"][0])) / width, st["c2add"][1] * dv / width; up_joint = (v1 - v(C1_ex + st["cjadd"][0])) / width, st["cjadd"][1] * dv / width
    U0 = lnZlo + math.log(sf["e"][0]); U0_se = sf["e"][1] / sf["e"][0]
    dB = math.log1p(sf["rem"][0] / sf["e"][0]); dB_se = sf["rem"][1] / sf["e"][0]                          # Bonferroni upper end minus the put-back
    Uc = lnZlo + math.log(sf["como"][0]); Uc_se = sf["como"][1] / sf["como"][0]
    print(f"(3) (UP) from the driver's exact C' in closed form: {v1:.7f} (the driver's upper end {corrected[1]:.7f}); the put-back ln Z(m_- + s_-) from my floor samples: {U0:.7f} +- {U0_se:.1e}"
          + (f"; reference value given on the command line: {U0_ref:.9f} +- {U0_ref_se:.1e} (mine is {(U0 - U0_ref) / math.hypot(U0_se, U0_ref_se):+.2f} s.e. from it)" if U0_ref else ""))
    print("| column of the table (fraction of the corrected width) | this measurement | its s.e. (batches) |")
    print("|---|---|---|")
    print(f"| lower end: joint law | {low_joint[0]:.4f} | {low_joint[1]:.4f} |")
    print(f"| lower end: pair terms | {low_pair[0]:.4f} | {low_pair[1]:.4f} |")
    print(f"| upper end: joint law under the ceiling | {up_joint[0]:.4f} | {up_joint[1]:.4f} |")
    print(f"| upper end: pair terms under the ceiling | {up_pair[0]:.4f} | {up_pair[1]:.4f} |")
    print(f"| recoverable by the joint law under the ceiling | {low_joint[0] + up_joint[0]:.4f} | {math.hypot(low_joint[1], up_joint[1]):.4f} |")
    print(f"| **by pair terms alone (under the ceiling)** | **{low_pair[0] + up_pair[0]:.4f}** | **{math.hypot(low_pair[1], up_pair[1]):.4f}** |")
    for lab, u0, u0se in ((("my plain floor estimate", U0, U0_se),) + ((("the reference value", U0_ref, U0_ref_se),) if U0_ref else ())):
        tot = low_joint[0] + (v1 - u0) / width; tot_se = math.hypot(low_joint[1], u0se / width)
        rest = (v(C1_ex + st["cjadd"][0]) - u0) / width; rest_se = math.hypot(up_joint[1], u0se / width)
        bon = (v1 - (u0 + dB)) / width; bon_se = math.hypot(u0se, dB_se) / width
        print(f"| with {lab} of the put-back: the loss | {tot:.4f} | {tot_se:.4f} |")
        print(f"|   … the rest (after the joint law under the ceiling) | {rest:.4f} | {rest_se:.4f} |")
        print(f"|   … **upper end recovered by pair laws under the FLOOR (Bonferroni)** | **{bon:.4f}** | {bon_se:.4f} |")
        print(f"|   … total recovered with pair laws on both sides (ceiling pair terms below, Bonferroni-floor above) | {low_pair[0] + bon:.4f} | {math.hypot(low_pair[1], bon_se):.4f} |")
    print(f"| Bonferroni-floor upper end minus the put-back (third order; measured directly) | {dB / width:.5f} | {dB_se / width:.5f} |")
    print(f"| upper end from single-group laws under the floor (comonotone of the empirical laws, batch by batch; biased by the batch size): below (UP) by | {(v1 - Uc) / width:.4f} | {Uc_se / width:.4f} |")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
