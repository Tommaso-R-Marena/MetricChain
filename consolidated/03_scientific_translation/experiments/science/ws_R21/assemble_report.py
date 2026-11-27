"""Assembles docs/science/workstreams/R21_REPORT.md from the part files in this directory (no computation)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
parts = ["report_part_header.md", "report_part_0.md", "report_part_1_2.md", "report_part_3.md", "report_part_4.md",
         "report_part_5_6_7.md", "report_part_8.md", "report_part_9.md"]
out = []
for p in parts:
    f = os.path.join(here, p)
    if not os.path.exists(f):
        print("missing (skipped):", p)
        continue
    out.append(open(f).read().rstrip() + "\n")
target = os.path.join(here, "..", "..", "..", "docs", "science", "workstreams", "R21_REPORT.md")
open(target, "w").write("\n".join(out))
print("written", os.path.abspath(target), sum(len(x) for x in out), "characters")
