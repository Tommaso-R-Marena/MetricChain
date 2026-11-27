#!/usr/bin/env python3
"""Is the transition of a floor a crossing of two states?  (A reading of the logs of floor_transition.py; no new run.)

The theory division reads a floor that leaves its reference as a first-order transition in the size of the penalty
tables (THY-RES-0016 section 5 (i)).  If, near the transition, the floor's ensemble is a mixture of two states -- the
reference state and a displaced state -- with a weight w(lambda), then every mean is linear in w: the exact slope
d ln Z / d lambda = beta <pen>_lambda and the sampled number of displaced sites lie on one straight line when plotted
against each other, and the excess of ln Z over the reference branch is -ln(1 - w).  This script takes, for each
of the four logs, the points (lambda, displaced sites, slope) of the grid and of the bisection, and reports
  (1) the two states: (displaced sites, slope) on the last grid point at which fewer than 2 % of the samples have half
      the chain displaced, and on the first at which more than 97 % have;
  (2) the straight-line test: the slope predicted from the displaced sites by the line through the two states,
      against the exact slope, at every point between them at which the weight read from the occupancy is between
      0.1 and 0.9 (outside that range the sampling error of the occupancy -- a mean of 1000 samples -- dominates);
  (3) the lever rule at the bracket of lambda_c: -ln(1 - w), with w from the occupancy, against ln Z - ln Z(m_0)
      minus the first-order growth of the reference branch;
  (4) the width of the transition in lambda against 1 / (slope of the displaced state minus slope of the reference).
Control for (2): the same prediction with lambda instead of the occupancy as the abscissa (a smooth one-state response
would make the slope linear in lambda between the two grid points); it must fail by a large factor.
Run: python3 -B floor_two_state.py > floor_two_state.log
"""
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [("floor_transition_K12_m4_w4.log", "Lys12, order 4, band 4"), ("floor_transition_K12_m4_w7.log", "Lys12, order 4, band 7"),
         ("floor_transition_K12_m3_w7.log", "Lys12, order 3, band 7"), ("floor_transition_LKSEc12_m3_w7.log", "(LKSE)3, order 3, band 7")]
print("| case | reference state: lambda, sites off, slope | displaced state: lambda, sites off, slope | lambda_c | points with weight 0.1-0.9 | slope predicted from the occupancy / exact slope: min, median, max | control, slope predicted from lambda / exact: min, max | lever rule -ln(1-w) at lambda_c | ln Z excess over the reference branch there | width in lambda of the 10-90 % range: predicted | span of the points found in that range |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for fn, name in CASES:
    txt = open(os.path.join(HERE, fn)).read(); assert "ALL DONE" in txt, fn
    grid = []
    for line in txt.split("\n"):
        if line.startswith("| ") and not line.startswith("| lambda"):
            c = [x.strip() for x in line.strip("|").split("|")]
            grid.append(dict(lam=float(c[0]), off=float(c[6]), slope=float(c[4]), exc=float(c[2]), fo=float(c[3]), half=float(c[9])))
    bis = [(float(a), float(b), float(c)) for a, b, c in re.findall(r"lambda ([0-9.]+): ([0-9.]+) off, slope ([0-9.e+-]+)", txt)]
    m = re.search(r"\(4\) lambda_c in \[([0-9.]+), ([0-9.]+)\].*?mean number of sites off the anchor ([0-9.]+) -> ([0-9.]+), slope ([0-9.]+) -> ([0-9.]+), ln Z - ln Z\(m_0\) there ([0-9.e+-]+) against the first-order number ([0-9.e+-]+)", txt)
    lo, hi, n1, n2, s1, s2, exc, fo = (float(v) for v in m.groups()); lc = 0.5 * (lo + hi)
    # the two states: the last grid point at which fewer than 2 % of the samples have half the chain displaced, and the first at which more than 97 % have
    ref = [g for g in grid if g["lam"] < lo and g["half"] < 0.02][-1]; dis = [g for g in grid if g["lam"] > hi and g["half"] > 0.97][0]
    w_of = lambda n: (n - ref["off"]) / (dis["off"] - ref["off"])
    allpts = sorted(set(bis + [(g["lam"], g["off"], g["slope"]) for g in grid]))
    pts = [(l, n, s) for (l, n, s) in allpts if ref["lam"] < l < dis["lam"] and 0.1 <= w_of(n) <= 0.9]
    ratios = sorted((ref["slope"] + w_of(n) * (dis["slope"] - ref["slope"])) / s for l, n, s in pts)
    ratios_c = [(ref["slope"] + (l - ref["lam"]) / (dis["lam"] - ref["lam"]) * (dis["slope"] - ref["slope"])) / s for l, n, s in pts]
    wc = w_of(0.5 * (n1 + n2)); lever = -math.log(1 - wc)
    ref_growth = ref["exc"] + ref["slope"] * (lc - ref["lam"])           # the reference branch continued linearly from its last pure grid point
    width = 2 * math.log(9) / (dis["slope"] - ref["slope"])
    span = (max(l for l, n, s in pts) - min(l for l, n, s in pts)) if len(pts) > 1 else float("nan")
    print(f"| {name} | {ref['lam']:g}, {ref['off']:.2f}, {ref['slope']:.3g} | {dis['lam']:g}, {dis['off']:.2f}, {dis['slope']:.4g} | {lc:.4g} | {len(pts)} | "
          f"{ratios[0]:.2f}, {ratios[len(ratios) // 2]:.2f}, {ratios[-1]:.2f} | {min(ratios_c):.2g}, {max(ratios_c):.2g} | {lever:.3f} | {exc - ref_growth:.3f} | {width:.3g} | {span:.3g} |")
print("\nReading.  If the floor's ensemble between the two grid points were a mixture of the two states, every mean would be linear in the weight: the sixth column would be 1 at every point")
print("and the two lever-rule columns equal.  The occupancy is a mean of 1000 exact samples (standard error about 0.15 sites near the transition, i.e. about 0.02 in the weight); the slope is exact.")
print("The displaced state is not one state: between its first pure grid point and the largest lambda its slope still grows (see the tables of the four logs), which limits the agreement.")
print("The control: with lambda as the abscissa (a smooth response between the same two grid points) the same points are off by the factors of the seventh column.")
print("ALL DONE")
