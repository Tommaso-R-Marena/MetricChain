"""
P4 item 3, Proposition 11.18c(b) on P2's real domains: are P2's pruned products X' "the largest
reset-closed part"?  For every instance analysis of g_GB whose pair-clash-free domain X_tau is not a
product (two rotamers can clash):

  X      product of the one-site admissible states;   X_tau = X minus pair clashes (P2's s2min > tau)
  X'     P2's greedily pruned clash-free product (an_main.pruned_product, re-run);  x0 = argmin E over X'
  D'(x0) = {x in X_tau : every changed state is compatible with every reference state}   (Prop. 11.18c(b))
  x*     = argmin of E over X_tau;   D'(x*)

reported: sizes; X' subset D'(x0) subset X_tau (asserted); whether x0 minimises E over D'(x0) and
over X_tau; and the second-order star ON THE NON-PRODUCT DOMAIN D' (Proposition 11.18c(a)):
constants over the rectangles inside D' (p4lib.c2_matrix_masked), the remainder bound
|g - g_star| <= sum c_ij checked at every state of D', and the exact criterion on D'
(the reference minimises f + g_star - sum c_ij over D') for both references.

usage: python3 -B p4_04_domains.py  -> out/p4_04_domains.json ; last line "DONE p4_04_domains"
"""
import sys, os, re, glob, json, time, math
import numpy as np
import p4lib as L4

t00 = time.time()
rows = []
for p in sorted(glob.glob(os.path.join(L4.P2, "out", "an_fb_*_R3_t0.60_tau*.json"))):
    mm = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not mm:
        continue
    tag, res, nres, bb, taus = mm.group(1), mm.group(2), int(mm.group(3)), mm.group(4), mm.group(5)
    J = json.load(open(p))
    if J.get("empty") or "iface|GB" not in J or J["clashfree"] == J["size"]:
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    Xt = inst["Xt"]; keep = inst["keep"]; shape = inst["shape"]
    f = inst["Rraw"]["f"]; g = inst["Rraw"]["GB"]
    E = np.where(Xt, f + g, np.inf)
    Ep = inst["f"] + inst["R"]["GB"]
    x0p = L4.argmin_index(Ep)
    x0 = tuple(int(keep[i][x0p[i]]) for i in range(len(shape)))
    assert abs(E[x0] - Ep[x0p]) < 1e-9
    Xp = np.zeros(Xt.shape, dtype=bool); Xp[np.ix_(*keep)] = True
    Dp = L4.dprime_mask(Xt, x0)
    assert (Xp <= Xt).all() and (Xp <= Dp).all() and (Dp <= Xt).all()
    xs = L4.argmin_index(E)
    Ds = L4.dprime_mask(Xt, xs)
    out = dict(tag=tag, res=res, nres=nres, bb=bb, tau=taus, shape_raw=list(Xt.shape), shape_pruned=list(shape), nX=int(Xt.size), nXt=int(Xt.sum()),
               nXp=int(Xp.sum()), nDp=int(Dp.sum()), nDs=int(Ds.sum()), x0=list(x0), xstar=list(xs),
               regret_Dp=float(E[x0] - np.where(Dp, E, np.inf).min()), regret_Xt=float(E[x0] - E[xs]),
               xstar_in_Xp=bool(Xp[xs]), xstar_in_Dp=bool(Dp[xs]))
    for nm, ref, D in (("x0", x0, Dp), ("xstar", xs, Ds)):
        gm = np.where(D, g, 0.0); fm = np.where(D, f, 0.0)
        C = L4.c2_matrix_masked(g, D)
        gs = L4.star_part(gm, ref)                               # star points of the reference inside D': they are in D' whenever used
        W = L4.pair_penalty(Xt.shape, ref, C)
        slack = np.where(D, W - np.abs(g - gs), np.inf)
        Lm = np.where(D, f + gs - W, np.inf)
        v = Lm[ref]; Lm2 = Lm.copy(); Lm2[ref] = np.inf
        out[nm] = dict(cmax=float(C.max()), bound_slack_min=float(slack.min()), margin=float(Lm2.min() - v) if D.sum() > 1 else None,
                       ref_min_E_on_D=bool(np.where(D, E, np.inf).min() >= E[ref] - 1e-12))
    Cp = L4.c2_matrix(inst["R"]["GB"])
    out["cmax_Xp"] = float(Cp.max())
    rows.append(out)
    print(f"[{time.time() - t00:5.0f}s] {res}{nres}/{bb} tau {taus}: |X| {out['nX']} |X_tau| {out['nXt']} |D'(x0)| {out['nDp']} |X'| {out['nXp']} |D'(x*)| {out['nDs']}; "
          f"x0 minimises E on D'(x0): {out['x0']['ref_min_E_on_D']} (regret {out['regret_Dp']:.3f}; on X_tau {out['regret_Xt']:.3f}); "
          f"star on D'(x0): slack {out['x0']['bound_slack_min']:.1e}, margin {out['x0']['margin']}; star on D'(x*): margin {out['xstar']['margin']}", flush=True)
json.dump(rows, open(os.path.join(L4.HERE, "out", "p4_04_domains.json"), "w"), indent=0)
n = len(rows)
print(f"\n{n} instance analyses of g_GB with a non-product X_tau")
print(f"X' = D'(x0) in {sum(r['nXp'] == r['nDp'] for r in rows)}; X' strictly smaller than D'(x0) in {sum(r['nXp'] < r['nDp'] for r in rows)}; D'(x0) = X_tau in {sum(r['nDp'] == r['nXt'] for r in rows)}")
fr = [r["nXp"] / r["nDp"] for r in rows]; fr2 = [r["nDp"] / r["nXt"] for r in rows]; fr3 = [r["nXp"] / r["nXt"] for r in rows]
print(f"|X'|/|D'(x0)|: min {min(fr):.3f} median {np.median(fr):.3f} max {max(fr):.3f};  |D'(x0)|/|X_tau|: min {min(fr2):.3f} median {np.median(fr2):.3f} max {max(fr2):.3f};  "
      f"|X'|/|X_tau|: min {min(fr3):.3f} median {np.median(fr3):.3f} max {max(fr3):.3f}")
print(f"x0 (argmin over X') is the minimiser of E over D'(x0) in {sum(r['x0']['ref_min_E_on_D'] for r in rows)} of {n}; over X_tau in {sum(r['regret_Xt'] < 1e-12 for r in rows)}; "
      f"largest regret over D'(x0) {max(r['regret_Dp'] for r in rows):.3f}, over X_tau {max(r['regret_Xt'] for r in rows):.3f} kcal/mol")
print(f"x* (argmin over X_tau) lies in X' in {sum(r['xstar_in_Xp'] for r in rows)}, in D'(x0) in {sum(r['xstar_in_Dp'] for r in rows)} of {n}")
print(f"remainder bound of Theorem 11.16 on the non-product domains (constants over rectangles inside the domain): smallest slack over all states of all domains "
      f"{min(min(r['x0']['bound_slack_min'], r['xstar']['bound_slack_min']) for r in rows):.2e} (>= -1e-9 means no violation)")
m0 = [r for r in rows if r["x0"]["margin"] is not None]
print(f"star on D'(x0) certifies (reference minimises the lower model over D'(x0)): {sum(r['x0']['margin'] >= -1e-9 for r in m0)} of {len(m0)}; "
      f"star on D'(x*): {sum(r['xstar']['margin'] is not None and r['xstar']['margin'] >= -1e-9 for r in rows)} of {n}")
print("by family (instances | X'=D'(x0) | star certifies on D'(x0) | on D'(x*)):",
      {fam: (sum(1 for r in rows if r["res"] == fam), sum(r["nXp"] == r["nDp"] for r in rows if r["res"] == fam),
             sum(r["x0"]["margin"] is not None and r["x0"]["margin"] >= -1e-9 for r in rows if r["res"] == fam),
             sum(r["xstar"]["margin"] is not None and r["xstar"]["margin"] >= -1e-9 for r in rows if r["res"] == fam)) for fam in ("F", "K", "LKSE", "S", "V", "L")})
# comparison with the star on the pruned product X' (flags of p4_01_shares.py, if present)
p1 = os.path.join(L4.HERE, "out", "p4_01_shares.json")
if os.path.exists(p1):
    ex = {(r["tag"], r["tau"]): r["exact"] for r in json.load(open(p1)) if r["name"] == "GB"}
    both = [(r, ex.get((r["tag"], r["tau"]))) for r in rows]
    print("star at x0: certifies on X' / on D'(x0) / on both:", sum(bool(e) for _, e in both), "/",
          sum(r["x0"]["margin"] is not None and r["x0"]["margin"] >= -1e-9 for r, _ in both), "/",
          sum(bool(e) and r["x0"]["margin"] is not None and r["x0"]["margin"] >= -1e-9 for r, e in both), f"of {n};",
          "certifies on X' although x0 does not even minimise E over D'(x0):", sum(bool(e) and not r["x0"]["ref_min_E_on_D"] for r, e in both),
          "; certifies on X', x0 minimises E over D'(x0), and the star fails on D'(x0):",
          sum(bool(e) and r["x0"]["ref_min_E_on_D"] and not (r["x0"]["margin"] >= -1e-9) for r, e in both))
    print("largest c_ij: on X' against on D'(x0), instances where the star certifies on X':",
          [f"{r['res']}{r['nres']}/{r['bb']}({r['tau'][1:]}): {r['cmax_Xp']:.2f} -> {r['x0']['cmax']:.2f}, |X'|/|D'| = {r['nXp']}/{r['nDp']}, regret on D' {r['regret_Dp']:.2f}, margin on D' {r['x0']['margin']:.2f}" for r, e in both if e])
print(f"[{time.time() - t00:.0f}s] DONE p4_04_domains")
