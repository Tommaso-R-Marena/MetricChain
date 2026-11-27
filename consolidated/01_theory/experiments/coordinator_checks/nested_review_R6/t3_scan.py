"""R6-T3, supplement: every n in a window around the crossover (the review computed a grid of sizes).

For the design of K_REPORT 6.4 at phi = 0.50 (n_o = floor(n/2)), with the cap M_bar of Theorem 11.56:
the sign of  ln LB_na - ln C_max  for EVERY n of the window.  Reported: the least n of the window with
C_max < LB_na, the largest n of the window with C_max >= LB_na, and the smallest margin beyond it.

Usage: python3 t3_scan.py <u> <n_from> <n_to>
"""
import sys, os, time
from r6lib_coord import Tab, outfile
from t3_separation import two_level, DESIGN, nonadaptive_lb


def main():
    u, n1, n2 = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    t0 = time.time()
    rows = []
    tabs = {}
    for n in range(n1, n2 + 1, step):
        if len(tabs) > 6:
            tabs.clear()
        res = two_level(n, u, 0.5, tabs)
        lb, R, D, Dm = nonadaptive_lb(Tab(n, u), res["x_out"], DESIGN["delta"])
        rows.append((n, float(res["lnC"]), float(lb), R))
    below = [r for r in rows if r[1] < r[2]]
    above = [r for r in rows if r[1] >= r[2]]
    lines = [f"u = {u}: every n in [{n1}, {n2}] (step {step}), phi = 0.50, design of K_REPORT 6.4, delta = 0.05   ({time.time() - t0:.0f} s)"]
    lines.append(f"  sizes with C_max <  LB_na: {len(below)};  least: {below[0][0] if below else None}")
    lines.append(f"  sizes with C_max >= LB_na: {len(above)};  largest: {above[-1][0] if above else None}")
    if above and below:
        last_bad = above[-1][0]
        tail = [r for r in rows if r[0] > last_bad]
        if tail:
            mn = min(tail, key=lambda r: r[2] - r[1])
            lines.append(f"  beyond n = {last_bad}: smallest margin ln LB_na - ln C_max = {mn[2] - mn[1]:.3f} at n = {mn[0]}")
        first_good = below[0][0]
        mixed = [r for r in rows if first_good <= r[0] <= last_bad]
        lines.append(f"  window in which the sign changes back and forth: [{first_good}, {last_bad}]"
                     f" ({sum(1 for r in mixed if r[1] < r[2])} of {len(mixed)} sizes below)" if last_bad > first_good else
                     f"  the sign changes once: C_max >= LB_na up to n = {last_bad}, C_max < LB_na from n = {first_good} on (within the window)")
    lines.append("  n, ln C_max, ln LB_na, R, margin  (rows near the crossover)")
    if below:
        c = below[0][0]
        for r in rows:
            if abs(r[0] - c) <= 12 * step or (above and abs(r[0] - above[-1][0]) <= 3 * step):
                lines.append(f"    {r[0]:6d} {r[1]:10.3f} {r[2]:10.3f} {r[3]:5d} {r[2] - r[1]:+8.3f}")
    print("\n".join(lines))
    open(outfile(f"t3_scan_u{u:g}_{n1}_{n2}.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
