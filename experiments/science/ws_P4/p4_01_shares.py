"""
P4 item 1: the share certificate of Proposition 11.18b(d) (theory report at 24a3c27, section 11.7)
on every instance analysis of workstream P2 (all tags and both thresholds for which P2 wrote
out/an_*.json; residuals g_GB, coul+g_GB, ff03-ff14SB, ff15ipq-ff14SB, ff99SB-ff14SB).

Per instance and residual g (known part f = ff14SB vacuum energy, E = f + g, domain = P2's pruned
clash-free product X', reference x0 = argmin of E over X'):

  c_ij     P2's class constants: the exact maximum over ALL rectangles of X' of the second mixed
           difference of g -- recomputed here with my own routine (p4lib.c2_matrix) and compared
           with the matrix stored by P2.  Measured by enumeration, not certified.
  A_i(a)   = E(x0; i->a) - E(x0);  Delta_i = min over a != x0_i  (single-site excitation energies of the full energy)
  T_ij     = second difference of the known part f at x0 (its pair table at the reference)
  L        = f + g_star - sum_{i<j changed} c_ij   (lower model of Theorem 11.16/11.17)
  exact    : x0 minimises L  (enumeration of L over X'; margin = min_{x != x0} L(x) - L(x0))
  rowsum_c : P2's plain row-sum condition  (1/2) sum_j c_ij <= Delta_i   (the condition that defines "the 13")
  w_ij     = max_{a != x0_i, b != x0_j} [c_ij - T_ij(a, b)]_+               (deficits, Prop. 11.18b(d))
  rowsum_w : (1/2) sum_j w_ij <= Delta_i for every i                         (row-sum condition for the deficits)
  shares   : s >= 0, s_ij + s_ji >= w_ij, sum_j s_ij <= Delta_i  -- existence by a maximum flow
             (my Edmonds-Karp, exact rationals); every certificate is re-verified by additions
             (p4lib.verify_shares), every refusal by an over-dense set (p4lib.verify_overdense) and
             by brute force over all sets of sites (p4lib.densest_excess).
  sshares  : state-dependent shares (an LP; my refinement) -- computed where exact holds and shares fail.

usage: python3 -B p4_01_shares.py [--only TAG_SUBSTRING] [--names GB,...]
writes out/p4_01_shares.json ; prints a summary and the headline table; last line "DONE p4_01_shares".
"""
import sys, os, re, glob, json, time, math
import numpy as np
import p4lib as L4
from p4lib import Fraction

t00 = time.time()
a = sys.argv[1:]
only = a[a.index("--only") + 1] if "--only" in a else None
names = a[a.index("--names") + 1].split(",") if "--names" in a else list(L4.RESIDUALS)
P2OUT = os.path.join(L4.P2, "out")
files = sorted(glob.glob(os.path.join(P2OUT, "an_fb_*_R3_t0.60_tau*.json")))
rows = []
nfiles = 0
for p in files:
    m = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not m:
        continue
    tag, res, nres, bb, taus = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5)
    if only and only not in tag:
        continue
    J = json.load(open(p))
    if J.get("empty"):
        continue
    if not any(f"iface|{nm}" in J for nm in names):
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    nfiles += 1
    shape = inst["shape"]; n = len(shape)
    assert list(shape) == list(J["shape_pruned"]), (tag, shape, J["shape_pruned"])
    f = inst["f"]
    for name in names:
        ifc = J.get(f"iface|{name}")
        if not ifc:
            continue
        g = inst["R"][name]
        E = f + g
        x0 = L4.argmin_index(E)
        assert list(x0) == list(ifc["argmin_E"]), (tag, name, x0, ifc["argmin_E"])
        C = L4.c2_matrix(g)
        Cp2 = np.array(J[f"Xp|{name}"]["C"])
        dC = float(np.abs(C - Cp2).max())
        A = L4.excitations(E, x0)
        Delta = L4.min_excitation(A, x0)
        nact = sum(1 for k in shape if k >= 2)
        # exact criterion
        Lmod = f + L4.star_part(g, x0) - L4.pair_penalty(shape, x0, C)
        margin = L4.margin_at(Lmod, x0)
        exact = bool(margin >= -1e-9)
        s2 = ifc["star_argmin_E"]
        # P2's plain row-sum condition
        rowsum_c = L4.rowsum_ok(C, Delta)
        # deficits and shares
        Tpair = lambda i, j: L4.second_diff(f, x0, i, j)
        w = L4.deficits(C, Tpair, x0, shape)
        rowsum_w = L4.rowsum_ok(w, Delta)
        fl = L4.share_flow(w, Delta)
        if fl["ok"]:
            assert L4.verify_shares(w, Delta, fl["s"]), (tag, name, "share certificate did not verify")
            # the conclusion of the proposition, checked on the instance (soundness): x0 minimises L
            assert exact, (tag, name, "shares exist but x0 does not minimise L: would refute 11.18b(d)")
        else:
            assert L4.verify_overdense(w, Delta, fl["S"]), (tag, name, "over-dense witness did not verify")
        bf, bfS = L4.densest_excess(w, Delta) if nact <= 18 else (float("nan"), None)
        if nact <= 18:
            assert (bf <= 1e-12) == fl["ok"] or abs(bf) < 1e-9, (tag, name, bf, fl["ok"])
        # shares with P2's constants and an additive view (plain c_ij instead of deficits): Prop. 11.18b(a)/(b) as if f were additive
        flc = L4.share_flow(C, Delta)
        # anchored constants (variant, not P2's): rectangles with one corner state = reference state at both sites
        Ca = L4.c2_anchored(g, x0)
        La = f + L4.star_part(g, x0) - L4.pair_penalty(shape, x0, Ca)
        margin_a = L4.margin_at(La, x0)
        sound_a = float((E - La).min())
        wa = L4.deficits(Ca, Tpair, x0, shape)
        fla = L4.share_flow(wa, Delta)
        if fla["ok"]:
            assert L4.verify_shares(wa, Delta, fla["s"]) and margin_a >= -1e-9
        # state-dependent shares where the flow fails although the criterion holds
        tss = None; tss_exact = None
        if exact and not fl["ok"]:
            tss, ss = L4.state_shares_lp(C, Tpair, A, x0, shape)
            if ss is not None:
                sl = L4.verify_state_shares(C, Tpair, A, x0, shape, ss)
                tss_exact = float(sl) if sl is not None else None
        row = dict(tag=tag, res=res, nres=nres, bb=bb, tau=taus, name=name, shape=list(shape), size=int(np.prod(shape)), n=n, nact=nact,
                   x0=list(x0), dC_vs_P2=dC, cmax=float(C.max()), Delta=[d if d != math.inf else None for d in Delta],
                   half_c=[float(v) for v in 0.5 * C.sum(1)], w=w.tolist(), half_w=[float(v) for v in 0.5 * w.sum(1)],
                   margin=margin, exact=exact, exact_P2=bool(s2["certifies_exactly"]), eps_star_P2=s2["eps_star"],
                   rowsum_c=rowsum_c, rowsum_c_P2=bool(s2["rowsum_plain_ok"]), rowsum_w=rowsum_w,
                   shares=fl["ok"], overdense=fl["S"], excess=(float(fl["excess"]) if fl["excess"] is not None else None),
                   bf_excess=bf, bf_S=bfS, shares_plain_c=flc["ok"],
                   margin_anch=margin_a, sound_anch=sound_a, shares_anch=fla["ok"], cmax_anch=float(Ca.max()),
                   sshares_t=tss, sshares_slack_exact=tss_exact,
                   shares_s=({f"{i},{j}": float(v) for (i, j), v in fl["s"].items()} if fl["ok"] and n <= 16 else None))
        rows.append(row)
    print(f"[{time.time() - t00:6.0f}s] {tag} tau {taus}: X' {list(shape)}  ({time.time() - t0:.1f}s)", flush=True)

os.makedirs(os.path.join(L4.HERE, "out"), exist_ok=True)
outname = "p4_01_shares.json" if not only else f"p4_01_shares_{only}.json"
json.dump(rows, open(os.path.join(L4.HERE, "out", outname), "w"), indent=0)


def yn(b):
    return "yes" if b else "no"


print(f"\n{nfiles} instance files, {len(rows)} (instance, residual) analyses; "
      f"largest |c_ij(mine) - c_ij(P2 stored)| = {max(r['dC_vs_P2'] for r in rows):.2e} kcal/mol")
print(f"disagreements with P2's stored flags: exact criterion {sum(r['exact'] != r['exact_P2'] for r in rows)}, "
      f"plain row-sum {sum(r['rowsum_c'] != r['rowsum_c_P2'] for r in rows)}")
print("\nSummary by residual (analyses with at least two sites; 'multi' = at least two sites with more than one state)")
print(f"{'residual':16s} {'all':>4s} {'multi':>5s} | {'exact':>5s} {'rowsum(c)':>9s} {'rowsum(w)':>9s} {'shares(w)':>9s} | "
      f"{'exact&!rowsum(c)':>16s} {'..of which rowsum(w)':>20s} {'..shares(w)':>11s} {'..state-shares':>14s} | {'shares&!exact':>13s}")
for name in names:
    R = [r for r in rows if r["name"] == name]
    if not R:
        continue
    t13 = [r for r in R if r["exact"] and not r["rowsum_c"]]
    print(f"{name:16s} {len(R):4d} {sum(r['nact'] >= 2 for r in R):5d} | {sum(r['exact'] for r in R):5d} {sum(r['rowsum_c'] for r in R):9d} "
          f"{sum(r['rowsum_w'] for r in R):9d} {sum(r['shares'] for r in R):9d} | {len(t13):16d} {sum(r['rowsum_w'] for r in t13):20d} "
          f"{sum(r['shares'] for r in t13):11d} {sum(1 for r in t13 if (r['shares'] or (r['sshares_slack_exact'] is not None and r['sshares_slack_exact'] >= 0))):14d} | "
          f"{sum(r['shares'] and not r['exact'] for r in R):13d}")

if "GB" in names:
    print("\nHEADLINE TABLE -- g_GB, the instances in which P2's row-sum condition fails and the exact second-order criterion holds")
    print(f"{'instance':12s} {'tau':4s} {'X′ (states per site)':34s} {'min Δ_i':>8s} {'max ½Σc':>8s} {'max ½Σw':>8s} | {'exact (margin)':>15s} | {'rowsum(c)':>9s} {'rowsum(w)':>9s} "
          f"{'SHARES(w)':>9s} {'over-dense set: excess':>28s} | {'state-shares (exact slack)':>26s} | {'anchored c: exact/shares':>24s}")
    for r in rows:
        if r["name"] == "GB" and r["exact"] and not r["rowsum_c"]:
            D = [d for d in r["Delta"] if d is not None]
            od = "" if r["shares"] else f"{r['overdense']}: {r['excess']:.4f}"
            st = "" if r["shares"] else (f"{yn(r['sshares_slack_exact'] is not None and r['sshares_slack_exact'] >= 0)} ({r['sshares_slack_exact']:.2e})" if r["sshares_slack_exact"] is not None else "LP failed")
            print(f"{r['res'] + str(r['nres']) + '/' + r['bb']:12s} {r['tau']:4s} {str(r['shape']):34s} {min(D):8.4f} {max(r['half_c']):8.4f} {max(r['half_w']):8.4f} | "
                  f"{yn(r['exact']):>5s} ({r['margin']:7.4f}) | {yn(r['rowsum_c']):>9s} {yn(r['rowsum_w']):>9s} {yn(r['shares']):>9s} {od:>28s} | {st:>26s} | "
                  f"{yn(r['margin_anch'] >= -1e-9):>10s} / {yn(r['shares_anch']):<10s}")
    T = [r for r in rows if r["name"] == "GB" and r["exact"] and not r["rowsum_c"]]
    print(f"\n==> of the {len(T)} instances, the share certificate of Proposition 11.18b(d) certifies {sum(r['shares'] for r in T)}; "
          f"the row-sum condition for the deficits holds in {sum(r['rowsum_w'] for r in T)}; "
          f"state-dependent shares certify {sum(1 for r in T if r['shares'] or (r['sshares_slack_exact'] is not None and r['sshares_slack_exact'] >= 0))}.")
print(f"\n[{time.time() - t00:.0f}s] wrote out/{outname}")
print("DONE p4_01_shares")
