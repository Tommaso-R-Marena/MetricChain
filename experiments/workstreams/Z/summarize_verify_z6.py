#!/usr/bin/env python3
"""summarize_verify_z6.py RUN_OUTPUT CHUNK_LOG [CHUNK_LOG ...]  --  what the chunk logs of verify_z6_chunk.py establish.

Reads the stored outputs of `verify_z6_chunk.py` (the independent exact checker run on consecutive ranges
of levels) and the committed output of the run they verify, and prints

  * the levels covered (every level of the run must be covered exactly once);
  * for each of the checker's tests (T) top, (F) family, (L) lines, (C) cap: how many levels passed and failed;
  * the number of stored lines certified by a single (line, pair), and of lines verified by the cap test;
  * at how many levels the cap test needed the refinement loop of the wrapper, the largest number of rounds,
    and the least slack with which a refined cap test passed;
  * the narrowest witness window;
  * whether the tops and the numbers of lines regenerated in the verification runs are those of the committed
    output (tops compared after rounding to the 12 decimals the committed output prints);
  * whether every chunk ended with the checker's own "ALL CHECKS PASS".

Exit code 1 unless every level is covered once, no test failed, every chunk passed and the tops agree.
This script only reads text; it proves nothing by itself.

Used for the 400-level run (u = 1, K = 4000):
    python3 summarize_verify_z6.py out_z6_certified_u1_J400.txt out_verify_z6_u1_K4000_levels_*.txt
Output: out_verify_z6_u1_K4000_summary.txt
"""
import re
import sys

run_path, logs = sys.argv[1], sys.argv[2:]

# ---- the committed output of the run: j | c_j | c_j/a | lines | ...
run = {}
for ln in open(run_path):
    m = re.match(r"\s*(\d+) \| (\d+\.\d+) \| (\d+\.\d+) \|\s*(\d+) \|", ln)
    if m:
        run[int(m.group(1))] = (m.group(2), int(m.group(4)))
JRUN = max(run)
print("# summary of the independent exact verification of %s (%d levels)" % (run_path.split("/")[-1], JRUN))

covered = {}
tests = {k: [0, 0] for k in "TFLC"}
certified = unmatched = zero_gen = total_lines = 0
refined_levels, max_rounds, least_refined_slack, least_cap_slack = 0, 0, None, None
minwin = None
all_pass = True
tops_ok = True
problems = []
for path in logs:
    name = path.split("/")[-1]
    txt = open(path).read().splitlines()
    head = [l for l in txt if l.startswith("# verify_z6_chunk.py")]
    tops = [l for l in txt if l.startswith("# the script's tops c_j:")]
    nlin = [l for l in txt if l.startswith("# lines per level:")]
    if not (head and tops and nlin):
        problems.append("%s: header lines missing" % name)
        all_pass = False
        continue
    m = re.search(r"levels (\d+)\.\.(\d+)", head[0])
    j0, j1 = int(m.group(1)), int(m.group(2))
    tvals = [float(x) for x in tops[0].split(":", 1)[1].split(",")]
    nvals = [int(x) for x in nlin[0].split(":", 1)[1].split(",")]
    for j in range(1, len(tvals) + 1):                          # the construction is re-run from level 1 in every chunk
        if j in run:
            if ("%.12f" % tvals[j - 1]) != run[j][0] or nvals[j - 1] != run[j][1]:
                tops_ok = False
                problems.append("%s: level %d regenerated as c = %.12f with %d lines; the committed output has %s with %d"
                                % (name, j, tvals[j - 1], nvals[j - 1], run[j][0], run[j][1]))
    levels_here = set()
    for l in txt:
        m = re.match(r"level (\d+): .*\| (\d+) lines: (\d+) certified by a single \(line, pair\) \[(\d+) from the zero line\], (\d+) not of that form", l)
        if m:
            j = int(m.group(1))
            covered[j] = covered.get(j, 0) + 1
            levels_here.add(j)
            total_lines += int(m.group(2)); certified += int(m.group(3)); zero_gen += int(m.group(4)); unmatched += int(m.group(5))
            if nvals[j - 1] != int(m.group(2)):
                problems.append("%s: level %d has %s lines in the check and %d in the header" % (name, j, m.group(2), nvals[j - 1]))
            continue
        m = re.match(r"\s*\[(ok|FAIL)\] level (\d+) \((T|F|L|C)\)", l)
        if m:
            tests[m.group(3)][0 if m.group(1) == "ok" else 1] += 1
            if m.group(1) != "ok":
                problems.append("%s: level %s test (%s) FAILED" % (name, m.group(2), m.group(3)))
            w = re.search(r"narrowest witness window rho_b - rho_a: ([0-9.e+-]+)", l)
            if w:
                v = float(w.group(1))
                minwin = v if minwin is None else min(minwin, v)
            if m.group(3) == "C":
                rounds = [int(x) for x in re.findall(r"\[refined: (\d+) round\(s\)\]", l)]
                slacks = [float(x) for x in re.findall(r"over \d+ vertices: ([0-9.e+-]+) at B", l)]
                if slacks:
                    s_ = min(slacks)
                    least_cap_slack = s_ if least_cap_slack is None else min(least_cap_slack, s_)
                if rounds:
                    refined_levels += 1
                    max_rounds = max(max_rounds, max(rounds))
                    if slacks:
                        least_refined_slack = min(slacks) if least_refined_slack is None else min(least_refined_slack, min(slacks))
    ended = any(l.strip() == "ALL CHECKS PASS" for l in txt[-3:])
    all_pass &= ended
    missing = [j for j in range(j0, j1 + 1) if j not in levels_here]
    print("  %s: levels %d..%d, %d verified%s; ended with %s" % (
        name, j0, j1, len(levels_here), "" if not missing else " (MISSING: %s)" % missing[:10],
        "ALL CHECKS PASS" if ended else "NO PASS LINE (failed or unfinished)"))

missing = [j for j in range(1, JRUN + 1) if covered.get(j, 0) == 0]
twice = [j for j in covered if covered[j] > 1]
print("levels covered: %d of %d%s%s" % (JRUN - len(missing), JRUN,
                                         "" if not missing else "; missing %s%s" % (missing[:12], " ..." if len(missing) > 12 else ""),
                                         "" if not twice else "; covered more than once: %s" % sorted(twice)[:12]))
for k, nm in (("T", "(T) top"), ("F", "(F) family and exact hull"), ("L", "(L) every other line has a proved pair"), ("C", "(C) cap line dominated")):
    print("  test %-40s passed at %4d levels, failed at %d" % (nm, tests[k][0], tests[k][1]))
print("stored lines: %d; certified by a single (line, pair) with a rational witness: %d (%d from the zero line); verified by the cap test: %d"
      % (total_lines, certified, zero_gen, unmatched))
print("cap test: refinement loop used at %d levels (at most %d round(s)); least slack of a passed cap test: %s; least slack after a refinement: %s"
      % (refined_levels, max_rounds, "%.3g" % least_cap_slack if least_cap_slack is not None else "-",
         "%.3g" % least_refined_slack if least_refined_slack is not None else "-"))
print("narrowest witness window: %s" % ("%.2g" % minwin if minwin is not None else "-"))
print("regenerated tops and line counts equal to the committed output (tops to the 12 decimals it prints): %s" % tops_ok)
for p_ in problems[:40]:
    print("  PROBLEM: " + p_)
good = (not missing) and (not twice) and all(tests[k][1] == 0 for k in tests) and all_pass and tops_ok and not problems
print("VERIFIED IN FULL" if good else "NOT VERIFIED IN FULL")
sys.exit(0 if good else 1)
