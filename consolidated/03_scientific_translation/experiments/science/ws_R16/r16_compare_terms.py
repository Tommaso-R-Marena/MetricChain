#!/usr/bin/env python3
"""
r16_compare_terms.py -- workstream R16: rung-by-rung comparison of my per-rung tables (logs/rep_terms_<n>.log, produced by
r16_cert.py --terms) with the theory division's stored tables (out_terms_<n>.txt in the read-only export; only READ).

usage: python3 r16_compare_terms.py <my log> <their out_terms file>
Compared per (phi_1, mode, rung): accuracy (4 significant digits as printed), multiplier kind and value, cost of the base
bracket, certified bound of the best two-level candidate, its design string, the server, and the term of C_max.
Stopping condition of the brief: the first number that differs, with the rung.
"""
import re
import sys

HEAD = re.compile(r"n=(\d+) phi_1=([0-9.]+) mode (\w+): ln\(C_max\)/\(na\) = ([0-9.]+); cap 2 Mbar ([0-9.]+); fibre dimension (\d+);"
                  r".*rungs served by a two-level run: (\d+) of (\d+)(?: \(rungs ([^)]*)\))?")
ROW = re.compile(r"\s+(\d+)\s+([0-9.e+]+)\s+(cap|count)\s+([0-9.]+)\s+([0-9.]+)\s+(\(none tried\)|[0-9.]+, [0-9.e+-]+, .*?)\s+-> (\S+), ([0-9.]+)\s*$")


def parse(path):
    out = {}
    cur = None
    for line in open(path):
        m = HEAD.match(line)
        if m:
            cur = (int(m.group(1)), float(m.group(2)), m.group(3))
            out[cur] = dict(cmax=m.group(4), cap=m.group(5), dim=int(m.group(6)), n2=int(m.group(7)), rungs=(m.group(9) or "-").strip(),
                            rows={})
            continue
        m = ROW.match(line)
        if m and cur is not None:
            cand = m.group(6)
            if cand.startswith("("):
                cb, design = None, None
            else:
                parts = cand.split(", ", 2)
                cb, design = parts[0], parts[2].strip()
            out[cur]["rows"][int(m.group(1))] = dict(x=m.group(2), mk=m.group(3), mult=m.group(4), base=m.group(5), cb=cb,
                                                     design=design, server=m.group(7), term=m.group(8))
    return out


mine = parse(sys.argv[1])
theirs = parse(sys.argv[2])
print("# r16_compare_terms.py: mine = %s ; theirs = %s" % (sys.argv[1], sys.argv[2]))
total = diff = 0
first = None
for key in sorted(mine):
    if key not in theirs:
        print("section %s: not in their file (not compared)" % (key,))
        continue
    a, b = mine[key], theirs[key]
    sec_total = sec_diff = 0
    for f in ("cmax", "cap", "dim", "n2", "rungs"):
        sec_total += 1
        if str(a[f]) != str(b[f]):
            sec_diff += 1
            if first is None:
                first = (key, "header", f, a[f], b[f])
    assert sorted(a["rows"]) == sorted(b["rows"]) == list(range(1, 41)), (key, len(a["rows"]), len(b["rows"]))
    for l in range(1, 41):
        for f in ("x", "mk", "mult", "base", "cb", "design", "server", "term"):
            sec_total += 1
            if a["rows"][l][f] != b["rows"][l][f]:
                sec_diff += 1
                print("   DIFFERENT: section %s rung %d field %s: mine %r, theirs %r" % (key, l, f, a["rows"][l][f], b["rows"][l][f]))
                if first is None:
                    first = (key, l, f, a["rows"][l][f], b["rows"][l][f])
    print("section n=%d phi_1=%.3f mode %s: %d fields compared (5 header fields + 40 rungs x 8), %d differ; servers: mine %s | theirs %s"
          % (key[0], key[1], key[2], sec_total, sec_diff, a["rungs"], b["rungs"]))
    total += sec_total
    diff += sec_diff
print("TOTAL: %d fields compared, %d differ; first difference: %s" % (total, diff, first))
import resource
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
