#!/usr/bin/env python3
"""R8 / script 10 -- independent replication of the coordinator's ten exact plateau twins.

Reads (read-only) experiments/science/pi_inference/plateau_twin_check.json and recomputes every
case with my own code (r8_02_twin.find_case): r1, r2, kappa*, gap.  Nothing is imported from
the coordinator's scripts.     Run: python3 r8_10_replicate_json.py     (about 2 minutes)
"""
import json, io, contextlib, os
from r8_lib import *
import r8_02_twin as TW

src = "/home/user/MetricChain/experiments/science/pi_inference/plateau_twin_check.json"
rows = json.load(open(src))
ok = True
print("   n    u   margin  eps1   D   | theirs: r1  r2  kappa*     gap      | mine: r1  r2  kappa*     gap      | agree")
for e in rows:
    n, u, e1, D = e["n"], e["u"], e["eps1"], e["D"]
    margin = e["r1"] / n - rho0(u)
    # their r1 = ceil((rho0 + margin) n) with margin in {0.01, 0.02, 0.03}
    m = min((0.01, 0.02, 0.03), key=lambda t: abs(math.ceil((rho0(u) + t) * n) - e["r1"]))
    with contextlib.redirect_stdout(io.StringIO()):
        r = TW.find_case(n, u, rho0(u) + m, e1, D / n)
    agree = (r["r1"] == e["r1"] and r["r2"] == e["r2"] and abs(r["kappa"] - e["kappa"]) < 1e-3 and abs(r["gap"] - e["gap"]) < 1e-3)
    ok &= agree
    print(f"  {n:5d} {u:3.1f}  {m:.2f}   {e1:.2f}  {D:4d} |  {e['r1']:4d} {e['r2']:4d} {e['kappa']:9.4f} {e['gap']:9.4f} |  "
          f"{r['r1']:4d} {r['r2']:4d} {r['kappa']:9.4f} {r['gap']:9.4f} | {agree}")
print("SUMMARY all ten cases reproduced:", ok)
