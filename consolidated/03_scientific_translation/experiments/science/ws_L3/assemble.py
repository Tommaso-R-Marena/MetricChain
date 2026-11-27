#!/usr/bin/env python3
"""Assemble TheoremA.lean = head + body of Compensation.lean (Parts 1-6, verbatim) + tail.

The files of this directory cannot import each other (they are not in the lake library), so
TheoremA.lean repeats Parts 1-6.  This script keeps the two copies identical.
Run from anywhere:  python3 experiments/science/ws_L3/assemble.py
"""
import os
here = os.path.dirname(os.path.abspath(__file__))
comp = open(os.path.join(here, "Compensation.lean")).read()
start = comp.index("/-! ## Part 1:")
end = comp.index("end ScienceL3")
body = comp[start:end]
head = open(os.path.join(here, "parts", "TheoremA_head.txt")).read()
tail = open(os.path.join(here, "parts", "TheoremA_tail.txt")).read()
marker = ("/-! # Parts 1–6: repeated verbatim from `Compensation.lean` -/\n\n")
out = head + marker + body + tail
open(os.path.join(here, "TheoremA.lean"), "w").write(out)
print("TheoremA.lean written:", out.count("\n"), "lines")
