#!/usr/bin/env python3
"""r29_wrap.py <script.py> [args ...]  --  run a script (theirs or mine) under the rules of workstream R29.

Sets the address-space limit to 3 GB before anything is imported by the target, runs the target with
runpy as __main__ (so that its own `__file__`-relative imports work and nothing is written next to it:
start this wrapper with `python3 -B`), and prints the wall time and the peak resident memory in the last
line.  The exit status of the target is passed on.  Nothing of the target is modified.
"""
import os
import resource
import runpy
import sys
import time

LIMIT = 3 * 1024 ** 3
resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True

if len(sys.argv) < 2:
    print("usage: r29_wrap.py <script.py> [args ...]")
    sys.exit(2)

target = os.path.abspath(sys.argv[1])
sys.argv = [target] + sys.argv[2:]
t0 = time.time()
status = 0
try:
    runpy.run_path(target, run_name="__main__")
except SystemExit as ex:                      # the target called sys.exit
    status = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 1)
except BaseException as ex:                   # report and pass on: an assertion of the target is a result here
    import traceback
    traceback.print_exc(file=sys.stdout)
    print("R29-WRAP: target raised %s: %s" % (type(ex).__name__, ex))
    status = 1
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
print("R29-WRAP: target %s  exit status %d  wall %.1f s  address-space cap 3 GB  peak RSS %.1f MB"
      % (os.path.basename(target), status, time.time() - t0, peak))
sys.exit(status)
