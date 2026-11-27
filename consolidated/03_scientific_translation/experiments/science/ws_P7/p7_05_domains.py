"""
P7 item 4, the "if cheap" part: the aromatic and charged instances on their CLASH-FREE (non-product)
domains.  P4 ran no share certificate on a non-product domain.

For every analysis of g_GB whose pair-clash-free domain X_tau is not a product (P4's 40: Phe, Lys, LKSE):
reference x* = argmin E over X_tau, domain D'(x*) = the largest reset-closed part of X_tau at x*
(= a product of the states compatible with the reference, minus the clashing pairs of states), class
constants over the rectangles / boxes inside D'(x*) (P4's routines), and the lower models
    so      f + g_star - sum_{i<j changed} c_ij                (second order; P4's p4_04_domains.py)
    to|pair, to|site   f + I_2 g - penalties                  (third order; P4's p4_07_dprime3.py)
restricted to D'(x*).  Where x* minimises the model over D'(x*) (enumeration):
  shares     state-dependent shares with the cover constraints imposed for ADMISSIBLE pairs of states only
             (LP with slack; integer certificate; exact check with the forbidden pairs excluded);
  gap        if there are none: the value of the pairwise relaxation with the forbidden pairs removed, and
             branching on one site (leaves certified as in p7_02; an empty leaf is vacuous).
Brute force: exact minimum of the published integer instance over D'(x*) and over every certified leaf.

usage: python3 -B p7_05_domains.py > logs/p7_05_domains.log   (writes out/p7_05_domains.json; last line "DONE p7_05_domains")
"""
import sys, os, json, time, itertools
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
print(f"p7_05_domains  started {L7.now()}", flush=True)
TOL = 1e-9
BIG = np.int64(2 ** 62)
STAT = dict(models=0, minimised=0, root_cert=0, root_viol=0, leaf_cert=0, leaf_viol=0, leaf_truth=0, empty_leaves=0)
rows = []
for (tag, fam, nres, bb, taus, p) in L7.instance_files():
    J = json.load(open(p))
    if J.get("empty") or "iface|GB" not in J or J["clashfree"] == J["size"]:
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    Xt = inst["Xt"]; shape = Xt.shape; n = len(shape)
    f = inst["Rraw"]["f"]; g = inst["Rraw"]["GB"]
    E = np.where(Xt, f + g, np.inf)
    xs = L4.argmin_index(E)
    D = L4.dprime_mask(Xt, xs)
    gm = np.where(D, g, 0.0)
    act = [i for i in range(n) if L4.line(D, xs, i).sum() >= 2]
    C = L4.c2_matrix_masked(g, D)
    models = [("so", f + L4.star_part(gm, xs) - L4.pair_penalty(shape, xs, C))]
    if len(act) >= 3:
        c3 = L4.c3_dict_masked(g, D)
        gam = np.zeros(n); gam2 = np.zeros((n, n))
        for (i, j, k), v in c3.items():
            for s_ in (i, j, k):
                gam[s_] += v / 3.0
            for (u, w) in ((i, j), (i, k), (j, k)):
                gam2[u, w] += v / 3.0; gam2[w, u] += v / 3.0
        base = f + L4.interp2(gm, xs)
        models += [("to|pair", base - L4.pair_penalty(shape, xs, gam2)), ("to|site", base - L4.site_penalty(shape, xs, gam))]
    line = []
    for (mname, G) in models:
        STAT["models"] += 1
        Gm = np.where(D, G, np.inf)
        v = Gm[xs]; G2 = Gm.copy(); G2[xs] = np.inf
        margin = float(G2.min() - v) if D.sum() > 1 else float("inf")
        row = dict(tag=tag, family=fam, nres=nres, bb=bb, tau=taus, model=mname, shape_raw=list(shape), nD=int(D.sum()), nXt=int(Xt.sum()),
                   product=int(np.prod([L4.line(D, xs, i).sum() for i in range(n)])), nact=len(act), margin=margin, minimised=bool(margin >= -TOL))
        if not row["minimised"]:
            row["status"] = "reference does not minimise the model"
            rows.append(row); line.append(f"{mname}:-")
            continue
        STAT["minimised"] += 1
        pm = PM.from_grid(G, xs, mask=D)
        mk = pm.mask()
        assert mk is None or np.array_equal(mk, D), "D' is not (states compatible with the reference) minus forbidden pairs"
        row["pairwise_err"] = float(np.abs(np.where(D, pm.grid() - (G - G[xs]), 0.0)).max())
        ipm = IPM(pm)
        IG = np.where(D, ipm.grid(), BIG)
        imin = int(IG.min())
        assert imin == 0, "the published instance is not minimised at the reference on D'"
        Dfull = pm.full_domain()
        s = L7.shares_lp(pm)
        row["t"] = s["t"]
        if s["t"] is not None and s["t"] > TOL:
            m = L7.shares_to_messages(ipm, Dfull, s["s"])
            LB = L7.leaf_bound(ipm, Dfull, m)[0]
            row["status"] = "shares" if LB >= 0 else "integer check failed"
            if LB >= 0:
                STAT["root_cert"] += 1; STAT["root_viol"] += (LB > imin)
            row["depth"] = 0
            line.append(f"{mname}:S")
            rows.append(row)
            continue
        if s["t"] is not None and s["t"] >= -TOL:
            row["status"] = "degenerate"
            rows.append(row); line.append(f"{mname}:deg")
            continue
        # ---------------------------------------------------- a gap on the non-product domain
        row["status"] = "gap"
        row["relaxation"] = L7.dual_lp(pm, Dfull)["val"]
        cache = {}

        def leaf(Dl):
            key = tuple(tuple(int(v_) for v_ in d) for d in Dl)
            if key not in cache:
                b = int(L7.box_min(IG, Dl))
                if b >= BIG // 2:                                  # no admissible state in the box: nothing to certify
                    STAT["empty_leaves"] += 1
                    cache[key] = dict(ok=True, empty=True, lp=None)
                else:
                    c = L7.certify_leaf(pm, ipm, Dl)
                    if b < 0:
                        STAT["leaf_truth"] += 1
                    if c["ok"]:
                        STAT["leaf_cert"] += 1; STAT["leaf_viol"] += (c["LB"] > b)
                    cache[key] = dict(ok=c["ok"], empty=False, lp=c["lp"])
            return cache[key]
        working = []
        for i in pm.active():
            if all(leaf(L7.fix(Dfull, i, a))["ok"] for a in pm.dom[i]):
                working.append(i)
        row["working"] = working
        row["least_leaves"] = min((len(pm.dom[i]) for i in working), default=None)
        row["depth"] = 1 if working else ">1"
        line.append(f"{mname}:G{row['depth']}")
        rows.append(row)
    print(f"[{time.time() - t00:5.0f}s] {fam}{nres}/{bb} tau {taus}: |X_tau| {int(Xt.sum())} |D'(x*)| {int(D.sum())} (product hull {rows[-1]['product']}): " + " ".join(line) + f" ({time.time() - t0:.1f}s)", flush=True)
    json.dump(dict(rows=rows, stat=STAT, complete=False), open(os.path.join(L7.HERE, "out", "p7_05_domains.partial.json"), "w"))

json.dump(dict(rows=rows, stat=STAT, complete=True), open(os.path.join(L7.HERE, "out", "p7_05_domains.json"), "w"), indent=0, default=int)
print(f"\n{len(set((r['tag'], r['tau']) for r in rows))} analyses of g_GB with a non-product clash-free domain; {len(rows)} models on D'(x*)")
print(f"{'model':8s} {'models':>6s} {'x* minimises':>12s} | {'shares':>6s} {'GAP':>4s} {'degenerate':>10s} | gap certified by one branching")
for key in ("so", "to|pair", "to|site", "ALL"):
    Q = [r for r in rows if key == "ALL" or r["model"] == key]
    M = [r for r in Q if r["minimised"]]
    gp = [r for r in M if r["status"] == "gap"]
    print(f"{key:8s} {len(Q):6d} {len(M):12d} | {sum(r['status'] == 'shares' for r in M):6d} {len(gp):4d} {sum(r['status'] == 'degenerate' for r in M):10d} | {sum(r['depth'] == 1 for r in gp)}")
print("by family (x* minimises / shares / gap):", {fam: f"{sum(r['minimised'] for r in rows if r['family'] == fam)}/{sum(r.get('status') == 'shares' for r in rows if r['family'] == fam)}/{sum(r.get('status') == 'gap' for r in rows if r['family'] == fam)}" for fam in ("F", "K", "LKSE")})
for r in rows:
    if r.get("status") == "gap":
        print(f"  GAP: {r['family']}{r['nres']}/{r['bb']} tau {r['tau']} {r['model']}: |D'| {r['nD']}, margin {r['margin']:.5f}, gap {-r['relaxation']:.6f}, sites that certify {r['working']}, least leaves {r['least_leaves']}")
print(f"\nBRUTE FORCE: {STAT['minimised']} models enumerated on D'(x*); root certificates accepted {STAT['root_cert']}, violations {STAT['root_viol']}; "
      f"leaf certificates accepted {STAT['leaf_cert']}, violations {STAT['leaf_viol']}; leaves with a negative exact minimum {STAT['leaf_truth']}; empty leaves {STAT['empty_leaves']}")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_05_domains.json   finished {L7.now()}")
print("DONE p7_05_domains")
