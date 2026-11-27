#!/usr/bin/env python3
"""Coordinator's reproduction check for the logs of serine_helix_reach.py (addendum A17 (16)).

Eight of the logs in this directory were written before the last edit of window_model.py (2026-11-26 05:55 UTC; the
edit added two optional rules for the terms that do not fit a window and left the default rule unchanged).  This
script compares them, line by line, with re-runs made with the final module:

    for a in "S6 4 5" "S12 4 6" "S12 5 6" "S12 5 7" "S12 5 8" "L12 4 11" "L12 5 11" "L12 6 11"; do set -- $a
        python3 -B serine_helix_reach.py $1 $2 $3 > <DIR>/serine_helix_reach_$1_m$2_w$3.log; done
    python3 -B serine_helix_reach_repro_check.py <DIR> > serine_helix_reach_repro_check.log

Removed before comparing: the timings "[12s]" and "ALL DONE 12 s", and the two provenance phrases that say whether
a quantity was computed in that run or read from the script's cache.  Everything else -- every number -- must agree.
"""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]


def norm(s):
    s = re.sub(r"\s*\[\d+s\]", "", s)
    s = re.sub(r"ALL DONE \d+ s", "ALL DONE", s)
    s = re.sub(r"closed-form sums, (computed, \d+s|read from this script's cache)\)", "closed-form sums)", s)
    s = re.sub(r"; (evaluated now|read from [\w.\-]+\.npz)\)", ")", s)
    return s


print("# logs written before the last edit of window_model.py against re-runs with the final module (timings and cache-provenance phrases removed)")
ok_all = True; n = 0
for fn in sorted(glob.glob(os.path.join(D, "serine_helix_reach_*.log"))):
    b = os.path.basename(fn); new = [norm(l) for l in open(fn)]; old = [norm(l) for l in open(os.path.join(HERE, b))]
    same = new == old; ok_all &= same; n += 1
    ndiff = sum(1 for x, y in zip(new, old) if x != y) + abs(len(new) - len(old))
    print(f"{b}: {len(old)} lines; identical: {same}" + ("" if same else f" ({ndiff} lines differ)"))
print(f"all {n} identical: {ok_all}")
print("ALL DONE")
