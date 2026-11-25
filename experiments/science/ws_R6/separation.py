"""
separation.py -- workstream R6: at which n is the certified worst-case cost C_max of the two-level algorithm (every run, every
instance) below the certified lower bound for NON-ADAPTIVE algorithms (Theorem 11.45(b)) at the same accuracy and delta?
Everything is computed from exact binomial tables for the given n (everyn.py); no asymptotics.
usage: python3 separation.py <u> <n1,n2,...> [phi1,phi2,...] [design]
"""
import sys, json, time
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
import everyn as EV

u = float(sys.argv[1])
ns = [int(x) for x in sys.argv[2].split(",")]
phis = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
design = sys.argv[4] if len(sys.argv) > 4 else "K64"
print("u = %g, design %s; all entries are natural logarithms of numbers of evaluations; a = KL(p_u||1/2)" % (u, design))
print("%6s | %6s %9s %9s | %9s %9s %9s | %8s %8s %8s %8s | %s" % ("n", "phi*", "lnCmax", "lnCmax'", "ln plain", "ln LB_na", "ln LB_hint",
                                                                  "Cmax/na", "plain/na", "LBna/na", "LBh/na", "separation: ln(LB_na/Cmax), with cap'"))
for n in ns:
    t0 = time.time()
    best = None
    tabs = {}
    for phi in phis:
        o, P, xs, lnC = EV.two_level(n, u, phi, design, tabs=tabs)
        tabs = {n: tabs[n]}          # keep only the table of Q_n (the others depend on phi)
        if best is None or o["lnCmax"] < best["lnCmax"]:
            best = o
        with open(HERE + "/data/separation_%s_u%g.jsonl" % (design, u), "a") as f:
            f.write(json.dumps(o) + "\n")
    o = best
    print("%6d | %6.2f %9.1f %9.1f | %9.1f %9.1f %9.1f | %8.4f %8.4f %8.4f %8.4f | %+8.1f %+8.1f  (%.0fs)" % (
        n, o["phi"], o["lnCmax"], o["lnCmax_cap"], o["lnplain"], o["ln_na"], o["ln_hint"], o["Cmax_na"], o["plain_na"], o["na_na"], o["hint_na"],
        o["ln_na"] - o["lnCmax"], o["ln_na"] - o["lnCmax_cap"], time.time() - t0))
    sys.stdout.flush()
