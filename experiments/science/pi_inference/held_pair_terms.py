#!/usr/bin/env python3
"""Pair terms that ARE exact on a band model: groups merged per held site, and pairs of held sites (open problem D15 (a)).

Proposition (the coordinator's; addendum item 93).  For each held site h let S+_h, S-_h be the sums of the routed plus- and
minus-items of all groups held at h, b_h = e^{beta S+_h} - 1 >= 0, a_h = e^{beta S-_h} - 1 >= 0.  Under the ceiling model:
  lower end   < prod_h (1 + b_h) >  >=  1 + sum_h <b_h> + sum_{h<h'} < b_h b_h' >                                              (L2)
  upper end   < (prod_h (1 + a_h) - 1) prod_h (1 + b_h) >  >=  sum_h < a_h (1 + b_h) >
                 + sum_{h<h'} < a_h a_h' (1 + b_h)(1 + b_h') + a_h (1 + b_h) b_h' + a_h' (1 + b_h') b_h >                       (C2h)
and every term may be restricted to any set of pairs of held sites and of held states (all terms are non-negative).
Proof: the left sides are polynomials in the a's and b's with non-negative coefficients; the right sides keep the
monomials supported on one held site or on one pair.  Each mean on the right is a combination of partition functions of
the band model with ONE or TWO sites held at given states (with the held sites fixed, the tables of their groups are
tables on windows) -- sum_h k_h and sum_{h<h'} k_h k_h' clamped computations, times the number of table sets.
This script does NOT implement the clamped computations.  It evaluates both sides from the states (every state of the
enumerable instances; exact samples of the ceiling for Lys12) to say what the proposition would give:
  lower end:  (LP) by groups  <=  by held sites  <=  + pairs of held sites  <=  the exact joint law;
  upper end:  the same four values of C and the upper ends they give (the driver's fixed-point iteration);
  the cost in clamped computations; how the pair terms concentrate on few (h, h', s, t).
Checks: the four inequalities at EVERY state (violations must be 0); the group-level values against the driver's exact
ones; control: with the pair term of the lower end doubled the chain of inequalities must break at some state.
Run: python3 -B held_pair_terms.py K5 4 2 --enum > held_pair_terms_K5_m4_w2_enum.log
     python3 -B held_pair_terms.py K12 4 4 > held_pair_terms_K12_m4_w4.log
"""
import sys, time, math, resource
import numpy as np
import first_order_recovery as FR
from group_coupling import capture
SR = FR.SR; BETA = FR.BETA


def log(s): print(s, flush=True)


def main():
    a = sys.argv[1:]; seq, m, w = a[0], a[1], a[2]; ENUM = "--enum" in a; N = int(a[a.index("--N") + 1]) if "--N" in a else 400000; t0 = time.time()
    got, text = capture([seq, m, w] + (["--enum"] if ENUM else []))
    for line in text.split("\n"):
        if line.startswith("=== "): log(line[:300])
    items, kind, rts, CL, up, GS, stages, n, k, lnZup, lnZlo, res = (got[q] for q in ("items", "kind", "rts", "CL", "up", "GS", "stages", "n", "k", "lnZup", "lnZlo", "res")); k = [int(v) for v in k]
    name = stages[-1][0]; gks = sorted(GS[name]); G = len(gks); corrected = res[name]; width = corrected[1] - corrected[0]
    jp = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (+1, 0)]; jm = [j for j in range(len(items)) if kind[j][0] in CL and kind[j][1] in (-1, 0)]
    if ENUM:
        X = np.asarray(got["st"]); wt = np.asarray(got["wu"], dtype=float); how = f"every state ({len(X)}), ceiling weights"
    else:
        X = up.sample(N, np.random.default_rng(20261126), BETA); wt = np.full(N, 1.0 / N); how = f"{N} exact independent samples of the ceiling model (seed 20261126)"
    Sp = np.stack([SR.items_value([items[j] for j in jp if rts[j] == gk], X) for gk in gks]); Sm = np.stack([SR.items_value([items[j] for j in jm if rts[j] == gk], X) for gk in gks])
    assert (Sp >= 0).all() and (Sm >= 0).all(); y = np.expm1(BETA * Sp); z = np.expm1(BETA * Sm)
    hs = sorted({int(gk[1]) for gk in gks}); H = len(hs); idx = {h: [gi for gi, gk in enumerate(gks) if int(gk[1]) == h] for h in hs}
    SpH = np.stack([Sp[idx[h]].sum(axis=0) for h in hs]); SmH = np.stack([Sm[idx[h]].sum(axis=0) for h in hs]); b = np.expm1(BETA * SpH); a_ = np.expm1(BETA * SmH)
    mean = lambda v: float((wt * v).sum())
    # ---- lower end, pointwise chain
    l1 = y.sum(axis=0); l2 = b.sum(axis=0); pair_l = np.zeros(len(X)); cb = np.zeros(len(X))
    for i in range(H): pair_l += b[i] * cb; cb += b[i]
    l4 = np.expm1(BETA * SpH.sum(axis=0))                                               # prod (1 + b_h) - 1
    tol = lambda v: 1e-9 * (1.0 + np.abs(v))
    v_low = int((l1 > l2 + tol(l2)).sum() + (l2 + pair_l > l4 + tol(l4)).sum()); ctl_low = int((l2 + 2.0 * pair_l > l4 + tol(l4)).sum())
    A_g = sum(GS[name][gk]["e"] for gk in gks); Lg = math.log1p(A_g); Lh = math.log1p(mean(l2)); Lp = math.log1p(mean(l2 + pair_l)); Lj = math.log1p(mean(l4))
    # ---- upper end, pointwise chain
    c1 = (z * (1.0 + y)).sum(axis=0); c2 = (a_ * (1.0 + b)).sum(axis=0); pair_u = np.zeros(len(X)); ab = a_ * (1.0 + b)
    for i in range(H):
        for j in range(i + 1, H): pair_u += a_[i] * a_[j] * (1.0 + b[i]) * (1.0 + b[j]) + ab[i] * b[j] + ab[j] * b[i]
    c4 = np.expm1(BETA * SmH.sum(axis=0)) * np.exp(BETA * SpH.sum(axis=0))
    v_up = int((c1 > c2 + tol(c2)).sum() + (c2 + pair_u > c4 + tol(c4)).sum())
    C_g = sum(GS[name][gk]["cp"] for gk in gks)

    def solve(C):
        v = lnZlo
        for _ in range(400): v = lnZlo - math.log1p(C * math.exp(lnZup - v))
        return v
    # the group-level C from the driver is exact; the other three are taken as (exact group value) + (mean of the pointwise difference), so that sampling noise enters the differences only
    Ch = C_g + mean(c2 - c1); Cp = Ch + mean(pair_u); Cj = C_g + mean(c4 - c1); ug, uh, upair, uj = solve(C_g), solve(Ch), solve(Cp), solve(Cj)
    Lh_ = Lg + (math.log1p(A_g + mean(l2 - l1)) - Lg); Lp_ = math.log1p(A_g + mean(l2 - l1) + mean(pair_l)); Lj_ = math.log1p(A_g + mean(l4 - l1))
    log(f"(0) {G} groups on {H} held sites {hs}; from {how}; group-level values from the states against the driver's exact ones: A {mean(l1):.6e} / {A_g:.6e}, C' {mean(c1):.6e} / {C_g:.6e}; "
        f"the driver's corrected bracket [{corrected[0]:.7f}, {corrected[1]:.7f}], width {width:.4g} [{time.time() - t0:.0f}s]")
    log("| what enters | lower end above ln Z(m_+), nats | gain, as a fraction of the corrected width | upper end | gain, as a fraction of the corrected width |")
    log("|---|---|---|---|---|")
    for lab, L_, u_ in (("groups, one by one (the driver: (LP), (UP))", Lg, ug), ("groups merged per held site (one held site)", Lh_, uh), ("+ pairs of held sites (two held sites) -- the proposition", Lp_, upair),
                        ("the exact joint law of all groups", Lj_, uj)):
        log(f"| {lab} | {L_:.6e} | **{(L_ - Lg) / width:+.3f}** | {u_:.7f} | **{(ug - u_) / width:+.3f}** |")
    tot_gain = (Lp_ - Lg) / width + (ug - upair) / width; joint_gain = (Lj_ - Lg) / width + (ug - uj) / width
    log(f"(1) **the proposition would narrow the corrected bracket by {tot_gain:.3f} of its width** (merging per held site alone: {(Lh_ - Lg) / width + (ug - uh) / width:.3f}; the exact joint law of all groups: {joint_gain:.3f}); "
        f"new width {width * (1 - tot_gain):.4g} against {width:.4g}")
    log(f"(2) checks at every {'state' if ENUM else 'sample'}: lower chain (groups <= held sites; held sites + pairs <= joint): {v_low} violations; upper chain: {v_up} violations (both must be 0); "
        f"control, the lower pair term doubled: {ctl_low} violations (must be positive)")
    assert v_low == 0 and v_up == 0 and ctl_low > 0
    # ---- cost and concentration
    kk = [k[h] for h in hs]; single = sum(kk); double = sum(kk[i] * kk[j] for i in range(H) for j in range(i + 1, H))
    contrib = []
    for i in range(H):
        for j in range(i + 1, H):
            t_l = wt * b[i] * b[j]; t_u = wt * (a_[i] * a_[j] * (1.0 + b[i]) * (1.0 + b[j]) + ab[i] * b[j] + ab[j] * b[i]); code = X[:, hs[i]] * k[hs[j]] + X[:, hs[j]]
            bl = np.bincount(code, weights=t_l, minlength=k[hs[i]] * k[hs[j]]); bu = np.bincount(code, weights=t_u, minlength=k[hs[i]] * k[hs[j]])
            contrib += [(float(bl[c]), float(bu[c])) for c in range(len(bl)) if bl[c] > 0 or bu[c] > 0]
    cl = np.sort(np.array([c[0] for c in contrib]))[::-1]; cu = np.sort(np.array([c[1] for c in contrib]))[::-1]
    need = lambda v, f: int(np.searchsorted(np.cumsum(v), f * v.sum()) + 1) if v.sum() > 0 else 0
    log(f"(3) cost: {single} computations with one site held and {double} with two (per set of tables: one for the lower end, two for the upper); of the {len(contrib)} pairs of held states with a non-zero pair term "
        f"{'' if ENUM else '(among the samples) '}the largest {need(cl, 0.9)} carry 90 % of the lower pair term and {need(cl, 0.99)} carry 99 %; upper pair term: {need(cu, 0.9)} and {need(cu, 0.99)}")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
