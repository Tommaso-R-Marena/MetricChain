#!/usr/bin/env python3
"""R17 re-run wrapper (ours).  Runs one of the theory division's scripts from the scratch copy
under `python3 -I -B` (isolated mode does not put the script's directory on sys.path, so this
wrapper inserts the scratch copy's directory, and nothing else), with sys.argv set as the
script expects, and prints wall time and peak RSS in the last line.

usage:  python3 -I -B rerun_wrapper.py <absolute path of script in the scratch copy> [args...]
"""
import os
import resource
import runpy
import sys
import time

script = os.path.abspath(sys.argv[1])
assert "/ws_R17/rerun_copy/" in script, "run only from the scratch copy"
sys.path.insert(0, os.path.dirname(script))
sys.argv = [script] + sys.argv[2:]
t0 = time.time()
status = "completed"
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit as e:  # a script may call sys.exit
    if e.code not in (None, 0):
        status = "SystemExit(%r)" % (e.code,)
sys.stdout.flush()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
print("R17-WRAPPER LAST LINE: %s; wall %.1f s; peak RSS %.1f MB" % (status, time.time() - t0, rss))
