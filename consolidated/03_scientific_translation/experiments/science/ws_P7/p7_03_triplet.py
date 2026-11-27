"""
P7 item 3: the alternative named by the theory division -- a triplet constraint.

For each gap analysis of out/p7_01_five.json (F = L - L(x0) >= 0 to be certified on X'):

 (a) ONE TRIPLE.  For every triple T of sites: the relaxation with the local-consistency constraints of T
     (a joint marginal on T that reproduces its three pair marginals).  Certificate = state-dependent
     shares in which the sign and cover constraints of the three pairs inside T are replaced by one
     condition per joint state of T (the sum of the three reparametrised pair terms is >= 0).  Found by
     an LP with slack, converted to integers, accepted only by the exact integer checker
     (p7lib.leaf_bound with triple=T: the bound must be 0 = the exact minimum of the published instance,
     which is known by enumeration from p7_01).  Also the value of the relaxation with T (primal LP,
     floating point) -- how much of the gap one triple closes.
 (b) BRANCHING = ALL TRIPLES THROUGH THE SITE (Proposition P7.3, checked numerically): for every site i,
     min over the leaves of i of the pairwise relaxation value of the leaf  against  the value of the
     relaxation with the constraints of all triples that contain i.
 (c) where no single triple suffices: the smallest sets of triples that close the gap -- pairs of triples
     exhaustively (and all triples through one site); floating-point LP values, tolerance 1e-8, NOT exact.

usage: python3 -B p7_03_triplet.py > logs/p7_03_triplet.log   (writes out/p7_03_triplet.json; last line "DONE p7_03_triplet")
"""
import sys, os, json, time, itertools
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
print(f"p7_03_triplet  started {L7.now()}")
five = json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]
branch = {(r["instance"], r["tau"]): r for r in json.load(open(os.path.join(L7.HERE, "out", "p7_02_branch.json")))}
TOLV = 1e-8
results = []
TOT = dict(triples=0, certified=0, bf_checks=0, bf_violations=0)
for g in five:
    t0 = time.time()
    tag, tau, name = g["tag"], float(g["tau"]), g["split"]
    inst = L4.load_instance(tag, tau)
    Lmod, x0, E, C = L7.second_order_grid(inst, name)
    pm = PM.from_grid(Lmod, x0); ipm = IPM(pm)
    IGmin = int(ipm.grid().min())                           # exact minimum of the published instance over X' (= 0, at x0)
    assert IGmin == 0
    n = pm.n; act = pm.active(); Dfull = pm.full_domain()
    iname = f"{g['family']}{g['nres']}/{g['bb']}"
    br = branch[(iname, g["tau"])]
    print(f"\n=== {iname} tau {g['tau']} split {name}: X' = {list(pm.shape)}; gap {-g['relaxation']:.6f}; sites that certify by one branching: {br['working']}")
    # ------------------------------------------------------------ (a) one triple
    T_all = list(itertools.combinations(act, 3))
    rows = []
    for T in T_all:
        rs = L7.shares_lp(pm, triple=T)
        ok = False; LB = None
        if rs["t"] is not None and rs["t"] > 0:
            m = L7.shares_to_messages(ipm, Dfull, rs["s"], triple=T)
            LB = L7.leaf_bound(ipm, Dfull, m, triple=T)[0]
            ok = bool(LB >= 0)
            if ok:
                TOT["bf_checks"] += 1
                if LB > IGmin:
                    TOT["bf_violations"] += 1
        val = L7.primal_lp(pm, triples=[T])["val"] if len(T_all) <= 60 or ok else None
        rows.append(dict(triple=list(T), t=rs["t"], certified=ok, LB=LB, value=val))
    TOT["triples"] += len(rows); TOT["certified"] += sum(r["certified"] for r in rows)
    good = [r["triple"] for r in rows if r["certified"]]
    print(f"  (a) {len(rows)} triples; single triples whose constraints close the gap (exact integer certificate): {len(good)}: {good}")
    if good:
        print(f"      slack t of those certificates: {[round(r['t'], 6) for r in rows if r['certified']]}")
    best = sorted(rows, key=lambda r: -r["t"])[:5]
    print(f"      best triples by LP slack t: {[(r['triple'], round(r['t'], 6)) for r in best]}")
    if len(T_all) <= 60:
        vals = sorted(((r["value"], r["triple"]) for r in rows), reverse=True)
        print(f"      relaxation value with one triple (plain relaxation {g['relaxation']:.6f}): best {[(tuple(t), round(v, 6)) for v, t in vals[:4]]}; "
              f"triples that change the value at all: {sum(1 for v, t in vals if v > g['relaxation'] + 1e-7)} of {len(vals)}")
    # consistency with Proposition P7.3: every site of a closing triple must certify by branching
    for T in good:
        assert all(i in br["working"] for i in T), "a closing triple contains a site whose branching fails: contradicts P7.3"
    # ------------------------------------------------------------ (b) branching on i  =  all triples through i
    eq = []
    for i in act:
        leafvals = []
        for a in pm.dom[i]:
            leafvals.append(L7.dual_lp(pm, L7.fix(Dfull, i, a))["val"])
        vb = min(leafvals)
        others = [j for j in act if j != i]
        Ti = [tuple(sorted((i, j, k))) for j, k in itertools.combinations(others, 2)]
        vt = L7.primal_lp(pm, triples=Ti)["val"] if Ti else None
        eq.append(dict(site=i, branch_value=vb, triples_value=vt, ntriples=len(Ti)))
    dmax = max(abs(e["branch_value"] - e["triples_value"]) for e in eq if e["triples_value"] is not None)
    print(f"  (b) min over leaves of the leaf relaxation value  vs  relaxation with all triples through the site: largest difference over {len(eq)} sites {dmax:.2e}")
    print("      site: value (certifies iff >= 0):  " + "  ".join(f"{e['site']}: {e['branch_value']:.6f}" for e in eq))
    assert dmax < 1e-6
    # ------------------------------------------------------------ (c) more than one triple
    multi = None
    if not good:
        multi = dict()
        if len(T_all) <= 60:
            pairs = []
            for T1, T2 in itertools.combinations(T_all, 2):
                v = L7.primal_lp(pm, triples=[T1, T2])["val"]
                if v > -TOLV:
                    pairs.append((list(T1), list(T2)))
            multi["pairs_checked"] = len(T_all) * (len(T_all) - 1) // 2
            multi["pairs_closing"] = pairs
            print(f"  (c) pairs of triples (floating point, value > -{TOLV:g}): {len(pairs)} of {multi['pairs_checked']} close the gap: {pairs[:12]}")
        # greedy: add the triple that raises the relaxation value most, until the gap is closed
        chosen = []
        v = g["relaxation"]
        cand = T_all
        while v < -TOLV and len(chosen) < 12:
            if len(T_all) > 60:                             # many triples: only those that meet the fractional sites of the current solution
                p = L7.primal_lp(pm, triples=chosen)
                frac = [i for i in range(n) if p["mu1"][i].max() < 1 - 1e-6]
                cand = [T for T in T_all if sum(1 for i in T if i in frac) >= 3 and T not in chosen]
            bestT, bestv = None, v
            for T in cand:
                if T in chosen:
                    continue
                vv = L7.primal_lp(pm, triples=chosen + [T])["val"]
                if vv > bestv + 1e-12:
                    bestT, bestv = T, vv
            if bestT is None:
                break
            chosen.append(bestT); v = bestv
            print(f"      greedy: + triple {bestT} -> relaxation value {v:.9f}")
        multi["greedy"] = [list(T) for T in chosen]; multi["greedy_value"] = v
        print(f"  (c) greedy set of triples (floating point): {len(chosen)} triples {chosen}, final value {v:.2e}")
    results.append(dict(instance=iname, tau=g["tau"], split=name, ntriples=len(rows), closing=good, rows=rows, equivalence=eq, multi=multi))
    print(f"  ({time.time() - t0:.1f}s)")

json.dump(results, open(os.path.join(L7.HERE, "out", "p7_03_triplet.json"), "w"), indent=1)
print("\nSUMMARY")
print(f"{'instance':10s} {'tau':4s} {'split':15s} {'triples':>7s} | {'one triple closes the gap':40s} | {'if not: triples needed (floating point)':40s}")
for r in results:
    m = r["multi"]
    extra = "" if m is None else (f"pairs: {len(m['pairs_closing'])} of {m['pairs_checked']}; " if "pairs_closing" in m else "") + f"greedy: {len(m['greedy'])} triples"
    print(f"{r['instance']:10s} {r['tau']:4s} {r['split']:15s} {r['ntriples']:7d} | {(str(r['closing']) if r['closing'] else 'NO'):40s} | {extra:40s}")
print(f"\nTOTAL: {TOT['triples']} single-triple programmes; {TOT['certified']} exact triplet certificates; {TOT['bf_checks']} compared with the exact minimum of the published instance; violations {TOT['bf_violations']}")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_03_triplet.json   finished {L7.now()}")
print("DONE p7_03_triplet")
