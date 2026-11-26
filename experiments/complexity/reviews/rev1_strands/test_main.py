# test_main.py -- check Theorem 1 / Theorem 3 on small instances with the brute-force enumerator.
import sys, math, time
from multiprocessing import Pool
from lib import *

# (items, m, B, mode)   mode: "F" full enumeration (every non-crossing pair set),
#                              "P" pruned (cut when a closed face has >=2 nicks)
INSTANCES = [
    # --- degenerate / tiny
    ((1,), 1, 1, "F"), ((2,), 1, 2, "F"), ((1, 1), 1, 2, "F"), ((1, 1), 2, 1, "F"),
    ((1, 1, 1), 3, 1, "F"), ((2, 1), 1, 3, "F"), ((1, 1, 1), 1, 3, "F"), ((3,), 1, 3, "F"),
    ((2,), 2, 1, "F"), ((2, 1), 3, 1, "F"), ((3,), 3, 1, "F"), ((1, 1, 1, 1), 4, 1, "F"), ((3, 1), 4, 1, "F"),
    ((2, 2), 4, 1, "F"), ((1, 1, 1, 1, 1), 5, 1, "F"), ((2, 1, 1, 1), 5, 1, "F"),
    # --- m=1 (always packable)
    ((2, 2), 1, 4, "F"), ((1, 3), 1, 4, "F"), ((1, 1, 2), 1, 4, "F"), ((1, 1, 1, 1), 1, 4, "F"), ((4,), 1, 4, "F"),
    ((2, 3), 1, 5, "F"), ((1, 2, 2), 1, 5, "F"), ((1, 1, 1, 1, 1), 1, 5, "F"), ((2, 2, 2), 1, 6, "F"),
    ((1, 2, 3), 1, 6, "F"), ((3, 3), 1, 6, "F"), ((1, 1, 2, 2), 1, 6, "F"),
    # --- B=2
    ((2, 2), 2, 2, "F"), ((1, 1, 2), 2, 2, "F"), ((1, 1, 1, 1), 2, 2, "F"), ((3, 1), 2, 2, "F"), ((4,), 2, 2, "F"),
    ((2, 2, 2), 3, 2, "F"), ((2, 2, 1, 1), 3, 2, "F"), ((2, 1, 1, 1, 1), 3, 2, "F"), ((1, 1, 1, 1, 1, 1), 3, 2, "F"),
    ((3, 3), 3, 2, "F"), ((3, 2, 1), 3, 2, "F"), ((3, 1, 1, 1), 3, 2, "F"), ((4, 2), 3, 2, "F"), ((4, 1, 1), 3, 2, "F"),
    ((2, 2, 2, 2), 4, 2, "F"), ((3, 3, 2), 4, 2, "F"), ((3, 3, 1, 1), 4, 2, "F"), ((2, 2, 2, 1, 1), 4, 2, "F"),
    ((3, 2, 2, 1), 4, 2, "F"), ((2, 2, 1, 1, 1, 1), 4, 2, "F"),
    ((2, 2, 2, 2, 2), 5, 2, "F"), ((3, 3, 2, 2), 5, 2, "F"), ((3, 3, 3, 1), 5, 2, "F"), ((2, 2, 2, 2, 1, 1), 5, 2, "F"),
    # --- B=3
    ((3, 3), 2, 3, "F"), ((1, 2, 1, 2), 2, 3, "F"), ((2, 2, 2), 2, 3, "F"), ((4, 2), 2, 3, "F"), ((5, 1), 2, 3, "F"),
    ((4, 1, 1), 2, 3, "F"), ((6,), 2, 3, "F"), ((1, 1, 1, 1, 1, 1), 2, 3, "F"), ((3, 2, 1), 2, 3, "F"), ((2, 2, 1, 1), 2, 3, "F"),
    ((3, 1, 1, 1), 2, 3, "F"), ((2, 1, 1, 1, 1), 2, 3, "F"),
    ((3, 3, 3), 3, 3, "F"), ((1, 2, 1, 2, 1, 2), 3, 3, "F"), ((3, 2, 1, 2, 1), 3, 3, "F"), ((2, 2, 2, 2, 1), 3, 3, "F"),
    ((2, 2, 2, 3), 3, 3, "F"), ((4, 4, 1), 3, 3, "F"), ((4, 2, 3), 3, 3, "F"), ((4, 2, 2, 1), 3, 3, "F"), ((5, 2, 2), 3, 3, "F"),
    ((3, 3, 2, 1), 3, 3, "F"), ((2, 2, 2, 1, 1, 1), 3, 3, "F"), ((3, 2, 2, 2), 3, 3, "F"),
    # --- B=4
    ((2, 2, 2, 2), 2, 4, "F"), ((3, 1, 2, 2), 2, 4, "F"), ((3, 1, 3, 1), 2, 4, "F"), ((4, 2, 2), 2, 4, "F"), ((4, 4), 2, 4, "F"),
    ((1, 1, 2, 2, 2), 2, 4, "F"), ((3, 3, 2), 2, 4, "F"), ((5, 3), 2, 4, "F"), ((5, 1, 1, 1), 2, 4, "F"), ((3, 3, 1, 1), 2, 4, "F"),
    ((1, 1, 1, 1, 2, 2), 2, 4, "F"), ((6, 2), 2, 4, "F"), ((7, 1), 2, 4, "F"), ((3, 2, 2, 1), 2, 4, "F"), ((5, 2, 1), 2, 4, "F"),
    # --- B=5
    ((2, 3, 2, 3), 2, 5, "F"), ((1, 4, 2, 3), 2, 5, "F"), ((5, 5), 2, 5, "F"), ((2, 2, 2, 2, 2), 2, 5, "F"), ((4, 4, 2), 2, 5, "F"),
    ((3, 3, 4), 2, 5, "F"), ((3, 3, 3, 1), 2, 5, "F"), ((4, 4, 1, 1), 2, 5, "F"), ((2, 2, 2, 4), 2, 5, "F"), ((6, 4), 2, 5, "F"),
    ((6, 2, 2), 2, 5, "F"), ((7, 3), 2, 5, "F"), ((1, 2, 2, 2, 3), 2, 5, "F"), ((2, 2, 1, 2, 3), 2, 5, "F"), ((1, 1, 3, 2, 3), 2, 5, "F"),
    ((3, 3, 2, 2), 2, 5, "F"), ((4, 3, 2, 1), 2, 5, "F"), ((4, 2, 2, 2), 2, 5, "F"), ((4, 4, 2), 2, 5, "F"), ((1, 1, 1, 2, 2, 3), 2, 5, "P"),
    ((2, 2, 2, 2, 1, 1), 2, 5, "P"), ((1, 1, 1, 1, 3, 3), 2, 5, "P"),
    # --- mB = 12 (at most 4 items: beyond that the exact-signature table is too large)
    ((4, 4, 4), 3, 4, "F"), ((5, 4, 3), 3, 4, "F"), ((8, 4), 3, 4, "F"), ((6, 6), 3, 4, "F"),
    ((4, 4, 4), 2, 6, "F"), ((5, 5, 2), 2, 6, "F"), ((5, 4, 3), 2, 6, "F"), ((6, 6), 2, 6, "F"), ((7, 5), 2, 6, "F"),
    ((4, 4, 4), 4, 3, "F"), ((6, 3, 3), 4, 3, "F"), ((6, 6), 6, 2, "F"), ((4, 4, 4), 6, 2, "F"),
    ((2, 2, 4, 4), 3, 4, "P"), ((3, 3, 3, 3), 3, 4, "P"), ((3, 3, 3, 3), 4, 3, "P"),
    ((3, 3, 3, 3), 2, 6, "P"), ((4, 4, 2, 2), 2, 6, "P"), ((5, 1, 3, 3), 2, 6, "P"),
    # --- 7 items
    ((1, 1, 1, 1, 2, 2, 2), 5, 2, "L"), ((1, 1, 1, 1, 1, 2, 2), 3, 3, "L"), ((2, 2, 1, 1, 1, 1, 1), 3, 3, "L"),
]


def work(inst):
    a, m, B, mode = inst
    t0 = time.time()
    n = len(a)
    grp = mu_fact(a)
    lean = (mode == "L")
    res = run_enum(system(a, m, B), prune=(mode in "PL"), orbit=(not lean and grp <= 24 and m * B <= 10), lean=lean)
    out = []
    fails = []
    pk = packable(a, m, B)
    M = m * B - n
    tb, tp = til_by_beta(a, m, B), til_by_perm(a, m, B)
    L = num_set_partitions(a, m, B)
    if tb != tp:
        fails.append("Til mismatch beta/perm %d %d" % (tb, tp))
    if (tb > 0) != pk:
        fails.append("Til>0 != packable")
    # global invariants
    for k in ("FACT1_MISMATCH", "EXTCOUNT_MISMATCH", "DUP_LABELLED", "PHYS_SIG_CLASH"):
        if lean and k in ("DUP_LABELLED", "PHYS_SIG_CLASH"):
            continue
        if res[k] != 0:
            fails.append("%s=%d" % (k, res[k]))
    if res["MAXR"] != 1:
        fails.append("MAXR=%d" % res["MAXR"])
    if "ORBIT" in res and res["ORBIT"] != res["PHYS"]:
        fails.append("ORBIT %d != PHYS %d" % (res["ORBIT"], res["PHYS"]))
    if not lean and res["LABELLED"] != res["CONNECTED"]:
        fails.append("LABELLED != CONNECTED")
    if not lean and res["LABELLED"] != res["PHYS"] * grp:
        fails.append("LABELLED %d != PHYS %d * prod mu! %d" % (res["LABELLED"], res["PHYS"], grp))
    if res["TILING"] != tb:
        fails.append("tiling structures %d != Til %d" % (res["TILING"], tb))
    faces = {i: Face(s) for i, s in res["desc"].items()}
    kinds = Counter(f.kind for f in faces.values())
    tight = None
    for mod in models_H():
        hist = evaluate(res, mod, faces)
        mfe = min(hist)
        lab, phys, til = hist[mfe]
        s = mod.sigma
        if pk:
            if mfe != s * M:
                fails.append("[%s] YES but MFE %s != sigma*M %s" % (mod.name, mfe, s * M))
            if lab != tb:
                fails.append("[%s] #min labelled %d != Til %d" % (mod.name, lab, tb))
            if til != lab:
                fails.append("[%s] min-energy structures not all tilings (%d of %d)" % (mod.name, til, lab))
            if not lean and phys * grp != tb:
                fails.append("[%s] #min physical %d != Til/prod mu! = %s" % (mod.name, phys, Fraction(tb, grp)))
        else:
            if mfe == s * M:
                fails.append("[%s] NO but MFE == sigma*M" % mod.name)
            if mfe < s * (M - 1):
                fails.append("[%s] NO but MFE %s < sigma*(M-1) %s" % (mod.name, mfe, s * (M - 1)))
            if mod.name.startswith("stack-only"):
                tight = (mfe == s * (M - 1))
        # tiling structures must have energy sigma*M in every model
        for e, (l_, p_, t_) in hist.items():
            if t_ and e != s * M:
                fails.append("[%s] a tiling structure has energy %s != sigma*M" % (mod.name, e))
    # stack-only histogram (physical ensemble)
    h = evaluate(res, models_H()[0], faces)
    row = dict(a=a, m=m, B=B, mode=mode, n=n, N=sum(len(x) for x in system(a, m, B)), pk=pk, M=M, Til=tb, L=L, grp=grp,
               visited=res["VISITED"], conn=res["CONNECTED"], phys=res["PHYS"], nsig=res["NSIG"], kinds=dict(kinds),
               mfe=min(h), nmin_lab=h[min(h)][0], nmin_phys=h[min(h)][1], tight=tight, fails=fails, secs=time.time() - t0,
               orbit=("ORBIT" in res))
    return row


if __name__ == "__main__":
    insts = INSTANCES
    if len(sys.argv) > 1:
        insts = [i for i in INSTANCES if i[3] in sys.argv[1]]
    seen = set()
    uniq = []
    for i in insts:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    with Pool(4) as p:
        rows = p.map(work, uniq, chunksize=1)
    nf = 0
    print("%-22s %2s %2s %1s %3s %-3s %3s %6s %4s %5s %11s %9s %8s %5s %5s %7s %7s %-5s %s" % (
        "items", "m", "B", "md", "N", "pk", "M", "Til", "L", "mu!", "visited", "connected", "physical", "MFE", "sM", "#minL", "#minP", "tight", "fails"))
    for r in rows:
        print("%-22s %2d %2d %1s %3d %-3s %3d %6d %4d %5d %11d %9d %8d %5d %5d %7d %7d %-5s %s" % (
            str(r["a"]), r["m"], r["B"], r["mode"], r["N"], "YES" if r["pk"] else "NO", r["M"], r["Til"], r["L"], r["grp"],
            r["visited"], r["conn"], r["phys"], r["mfe"], -r["M"], r["nmin_lab"], r["nmin_phys"],
            "" if r["tight"] is None else str(r["tight"]), "; ".join(r["fails"]) if r["fails"] else "ok"))
        nf += len(r["fails"])
    print("instances: %d   YES: %d   NO: %d   total failures: %d" % (len(rows), sum(r["pk"] for r in rows), sum(not r["pk"] for r in rows), nf))
    print("models per instance: %d" % len(models_H()))
    print("total connected labelled structures checked: %d ; total pair sets visited: %d" % (sum(r["conn"] for r in rows), sum(r["visited"] for r in rows)))
    allk = Counter()
    for r in rows:
        allk.update(r["kinds"])
    print("face kinds over all descriptor tables:", dict(allk))
