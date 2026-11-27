#!/usr/bin/env python3
"""r20_rerun_driver.py -- runs one of the reviewed division's scripts UNMODIFIED from the scratch copy
`rerun_copy/`, under `python3 -I -B`: isolated mode does not put the script's directory on sys.path, so this
driver inserts it (their test does `from ref_enum import *`) and executes the script with runpy.
A memory cap (address space, default 2 GB) is applied so that the process cannot exceed the workstream's limit.
Usage: python3 -I -B r20_rerun_driver.py <script name in rerun_copy/> [cap in GB]"""
import os
import resource
import runpy
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
copy = os.path.join(here, "rerun_copy")
script = sys.argv[1]
cap_gb = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
cap = int(cap_gb * 1024 ** 3)
resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
sys.path.insert(0, copy)
print("[driver] running %s from %s under python %s, isolated, address-space cap %.1f GB, start %s" % (
    script, copy, sys.version.split()[0], cap_gb, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), flush=True)
t0 = time.time()
try:
    runpy.run_path(os.path.join(copy, script), run_name="__main__")
    status = "completed"
except MemoryError:
    status = "STOPPED: MemoryError under the %.1f GB cap" % cap_gb
except BaseException as e:  # noqa: BLE001
    status = "STOPPED: %s: %s" % (type(e).__name__, e)
ru = resource.getrusage(resource.RUSAGE_SELF)
print("[driver] %s; elapsed %.1f s; max RSS %.0f MB; end %s" % (
    status, time.time() - t0, ru.ru_maxrss / 1024.0, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())), flush=True)
print("[driver] END")
