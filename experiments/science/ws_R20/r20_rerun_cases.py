#!/usr/bin/env python3
"""r20_rerun_cases.py -- RE-RUN of the cases of the reviewed division's big test, one case per process.

Their script `test_partition_reduction_big.py` run as a whole stops with MemoryError under a 2 GB cap at its 11th case
(their function `run` keeps every structure in a set).  Here the list `cases` is read from their script (ast, the file is
not executed), and for every case a fresh interpreter (python3 -I -B, 2 GB address-space cap) imports their unmodified
`test_partition_reduction.run` and calls it exactly as their script does: run(items, m, B, "stack") and
run(items, m, B, "random", seed=7, sigma=3).  A case that does not fit in 2 GB is reported, not worked around.
Usage: python3 -I -B r20_rerun_cases.py"""
import ast
import os
import subprocess
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
copy = os.path.join(here, "rerun_copy")
src = open(os.path.join(copy, "test_partition_reduction_big.py")).read()
cases = None
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "cases":
        cases = ast.literal_eval(node.value)
assert cases is not None and len(cases) == 12, cases

CHILD = r'''
import sys, resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 ** 3, 2 * 1024 ** 3))
sys.path.insert(0, %r)
from test_partition_reduction import run
items, m, B = %r
try:
    ok1 = run(items, m, B, "stack")
    ok2 = run(items, m, B, "random", seed=7, sigma=3)
    print("CASE-RESULT", "OK" if (ok1 and ok2) else "MISMATCH", "maxrss_MB=%%d" %% (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), flush=True)
except MemoryError:
    print("CASE-RESULT MEMORYERROR under the 2 GB cap", flush=True)
'''

print("r20_rerun_cases.py: %d cases read from their script; start %s" % (len(cases), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), flush=True)
n_ok = n_mem = n_bad = 0
t0 = time.time()
for case in cases:
    p = subprocess.run([sys.executable, "-I", "-B", "-c", CHILD % (copy, tuple(case))], capture_output=True, text=True)
    out = p.stdout.strip()
    print(out, flush=True)
    if "CASE-RESULT OK" in out:
        n_ok += 1
    elif "MEMORYERROR" in out or "MemoryError" in p.stderr:
        n_mem += 1
        if "CASE-RESULT" not in out:
            print("CASE-RESULT MEMORYERROR under the 2 GB cap (raised outside run): %s" % (case,), flush=True)
    else:
        n_bad += 1
        print("CASE-RESULT FAILED rc=%d stderr tail: %s" % (p.returncode, p.stderr[-300:]), flush=True)
print("SUMMARY: cases OK (both models): %d; cases stopped by MemoryError under 2 GB: %d; other failures or mismatches: %d; elapsed %.1f s" % (
    n_ok, n_mem, n_bad, time.time() - t0))
print("END r20_rerun_cases.py")
