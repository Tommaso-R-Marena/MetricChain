#!/usr/bin/env python3
"""
r16_compare_all.py -- workstream R16: every certified number of the theory division's stored outputs
(out_*.txt of experiments/coordinator_checks/three_levels_certified in the read-only export; only READ) against my
replication logs logs/rep_<n>.log (own code).  Compared, per (n, phi_1), as printed strings with four decimals:
   two levels: C_max  |  servers chosen by certified cost: certified C_max  |  the same with more middle designs: certified C_max
usage: python3 r16_compare_all.py <directory of their out_*.txt> <my logs directory>
"""
import glob
import os
import re
import sys

THEIRS = re.compile(r"n=(\d+) phi_1=([0-9.]+): two levels: flat ([0-9.na]+), C_max ([0-9.na]+) \|.*?"
                    r"servers chosen by certified cost: flat ([0-9.na]+), certified C_max ([0-9.na]+) \| the same with more "
                    r"middle designs: flat ([0-9.na]+), certified C_max ([0-9.na]+)")
MINE = re.compile(r"n=(\d+) phi_1=([0-9.]+): two ([0-9.]+) \[.*?\] \| tuned ([0-9.]+) \[.*?\] \| searched ([0-9.]+) \[")

theirs = {}
files = sorted(f for f in glob.glob(os.path.join(sys.argv[1], "out_*.txt"))
               if not os.path.basename(f).startswith(("out_terms", "out_summary")))
for f in files:
    for line in open(f):
        m = THEIRS.match(line)
        if m:
            key = (int(m.group(1)), "%.3f" % float(m.group(2)))
            d = theirs.setdefault(key, {})
            for name, v in (("two", m.group(4)), ("tuned", m.group(6)), ("searched", m.group(8))):
                if v != "nan":
                    assert d.get(name, v) == v, (f, key, name)
                    d[name] = v
mine = {}
for f in sorted(glob.glob(os.path.join(sys.argv[2], "rep_[0-9]*.log"))):
    for line in open(f):
        m = MINE.match(line)
        if m:
            mine[(int(m.group(1)), "%.3f" % float(m.group(2)))] = dict(two=m.group(3), tuned=m.group(4), searched=m.group(5))

print("# their files read: " + ", ".join(os.path.basename(f) for f in files))
total = agree = 0
missing = []
first = None
per_n = {}
for key in sorted(theirs):
    if key not in mine:
        missing.append(key)
        continue
    for name, v in theirs[key].items():
        total += 1
        ok = mine[key][name] == v
        agree += ok
        c = per_n.setdefault(key[0], [0, 0])
        c[0] += 1
        c[1] += ok
        if not ok:
            print("DIFFERENT at n=%d phi_1=%s, %s: mine %s, theirs %s" % (key[0], key[1], name, mine[key][name], v))
            if first is None:
                first = (key, name)
for n in sorted(per_n):
    print("n = %6d: %2d of %2d numbers equal to the four digits printed" % (n, per_n[n][1], per_n[n][0]))
print("TOTAL: %d of %d certified numbers (two levels, tuned, searched; all (n, phi_1) of their stored outputs) equal to the four"
      " digits printed; first difference: %s; (n, phi_1) of theirs not in my logs: %s" % (agree, total, first, missing))
extra = sorted(k for k in mine if k in theirs and set(mine[k]) - set(theirs[k]))
print("numbers of mine that their outputs do not contain (not compared): " +
      "; ".join("n=%d phi_1=%s: %s" % (k[0], k[1], ", ".join("%s %s" % (nm, mine[k][nm]) for nm in sorted(set(mine[k]) - set(theirs[k]))))
                for k in extra))
import resource
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
