"""R6-T3, supplement: the larger sizes of the science division's table (R6_REPORT.md, Corollary R6.2), phi = 0.50."""
import sys, os, time
from r6lib_coord import Tab, outfile
from t3_separation import two_level, DESIGN, nonadaptive_lb, hinted_lb

rows = [(1.0, 2000, 193.1, 221.1, 61.1), (1.0, 4000, 320.8, 441.3, 120.1), (1.0, 8000, 566.9, 883.1, 236.8), (1.0, 16000, 1045.1, 1767.6, 470.3),
        (2.0, 1000, 264.1, 327.2, 100.4), (2.0, 4000, 814.3, 1306.6, 393.2), (0.5, 8000, 197.4, 240.7, 64.5), (0.5, 11000, 249.3, 331.1, 87.5)]
out = ["larger sizes of the review's long table (phi = 0.50): u, n | ln C_max (review) | ln LB_na (review) | ln hinted (review)"]
for (u, n, c0, l0, h0) in rows:
    t0 = time.time()
    res = two_level(n, u, 0.5, {})
    tn = Tab(n, u)
    lb, R, D, Dm = nonadaptive_lb(tn, res["x_out"], DESIGN["delta"])
    hl, k = hinted_lb(tn, res["x_out"], DESIGN["delta"])
    out.append(f"{u:4.1f} {n:6d} | {float(res['lnC']):9.2f} ({c0:7.1f}) | {float(lb):9.2f} ({l0:7.1f}) | {float(hl):8.2f} ({h0:6.1f})   [{time.time() - t0:.0f} s]")
    print(out[-1]); sys.stdout.flush()
open(outfile("t3_large.txt"), "w").write("\n".join(out) + "\n")
