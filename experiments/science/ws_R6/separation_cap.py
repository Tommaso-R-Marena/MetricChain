"""
separation_cap.py -- workstream R6: the finite-n separation of Corollary R6.2 WITH the lowered sample-size cap of the remark of
checkpoint 40c5bd7 (M-bar replaced by 2 max{e^lam M-dagger, M-ddagger} in C_max; K, m_max, delta' unchanged), on a wider range of
outer fractions phi.  For each n: min over phi of ln C_max (theorem as at 5ed4072) and of ln C_max^cap, against ln LB_na.
Everything from exact binomial tables (everyn.two_level).  Writes data/separation_cap_<design>_u<u>.jsonl (one line per cell).
usage: python3 separation_cap.py <u> <n1,n2,...> [phi1,phi2,...] [design]
"""
import sys, json, time
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
import everyn as EV

u = float(sys.argv[1])
ns = [int(x) for x in sys.argv[2].split(",")]
phis = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.50, 0.55, 0.60, 0.65, 0.70]
design = sys.argv[4] if len(sys.argv) > 4 else "K64"
print("u = %g, design %s; natural logarithms of numbers of evaluations" % (u, design))
print("%6s | %-22s | %-22s | %9s | %s" % ("n", "min ln C_max (phi)", "min ln C_max^cap (phi)", "ln LB_na", "LB_na - C_max, LB_na - C_max^cap"))
for n in ns:
    t0 = time.time()
    tabs = {}
    cells = []
    for phi in phis:
        o, P, xs, lnC = EV.two_level(n, u, phi, design, tabs=tabs)
        tabs = {n: tabs[n]}
        o["Delta"] = int(P.Delta)
        o["rdag_ge_Delta"] = bool(P.rdag >= P.Delta)
        cells.append(o)
        with open(HERE + "/data/separation_cap_%s_u%g.jsonl" % (design, u), "a") as f:
            f.write(json.dumps(o) + "\n")
    b1 = min(cells, key=lambda o: o["lnCmax"])
    b2 = min(cells, key=lambda o: o["lnCmax_cap"])
    print("%6d | %9.2f (phi %.2f)      | %9.2f (phi %.2f)      | %9.2f | %+7.2f %+7.2f   (%.0fs)  per phi, with cap: %s" % (
        n, b1["lnCmax"], b1["phi"], b2["lnCmax_cap"], b2["phi"], b1["ln_na"], b1["ln_na"] - b1["lnCmax"], b2["ln_na"] - b2["lnCmax_cap"],
        time.time() - t0, " ".join("%.2f:%.1f" % (o["phi"], o["lnCmax_cap"]) for o in cells)))
    sys.stdout.flush()
