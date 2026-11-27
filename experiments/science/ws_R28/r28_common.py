"""R28 common helpers: thread limits, 3 GB address-space cap, peak-memory line.

Every R28 script imports this FIRST (before numpy), calls cap() and ends with finish(t0).
"""
import os
import resource
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

CAP_GB = 3.0


def cap(gb=CAP_GB):
    lim = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    return lim


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def finish(t0):
    """Last line of every script: wall time and peak memory."""
    print(f"END {utc()}  wall {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB "
          f"(ru_maxrss; address space capped at {CAP_GB:g} GB)")
    sys.stdout.flush()
