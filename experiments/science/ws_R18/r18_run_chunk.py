#!/usr/bin/env python3
"""R18 runner: execute ONE of the engineering division's two check scripts, verbatim (runpy), on one chunk made
by r18_make_chunks.py, in this process, under an address-space limit, and print a last line with the exit
status, the wall time, the number of mean runs made through the R18 adapter and the peak RSS.

usage: python3 -I -B r18_run_chunk.py <recheck_classification|nonproduct_bound> <job> <key> [limit_GB]
       <key> = the chunk's directory name, <job>_n<n> or <job>_n<n>_u<u>
       output json: logs/<script>_<key>.json   (their --out file)
The script reads results/x005_<job>.jsonl beside itself (only the lines of this chunk are there).
"""
import resource, runpy, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
script, job, key = sys.argv[1], sys.argv[2], sys.argv[3]
limit_gb = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
resource.setrlimit(resource.RLIMIT_AS, (int(limit_gb * 2 ** 30), int(limit_gb * 2 ** 30)))
chunk = HERE / "rerun_copy" / "chunks" / key / "experiments" / "eng" / "twolevel"
path = chunk / f"{script}.py"
out = HERE / "logs" / f"{script}_{key}.json"
if out.exists():
    raise SystemExit(f"R18-RUNNER refuses to overwrite {out}")
print(f"R18-RUNNER start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} script={path} job={job} chunk={key} "
      f"address-space limit {limit_gb} GB; python -I -B; kernel: R18 adapter over their meanrun.mean_run", flush=True)
sys.argv = [str(path), "--jobs", job, "--out", str(out)]
t = time.time()
status = "0"
try:
    runpy.run_path(str(path), run_name="__main__")
except SystemExit as e:
    status = str(e.code)
except MemoryError:
    status = "MemoryError"
except Exception as e:                       # their script failed: say how, do not hide it
    status = f"{type(e).__name__}: {e}"
from metricchain_eng.twolevel import ckernel
assert "R18 ADAPTER" in (ckernel.__doc__ or ""), "the adapter was not the module imported"
print(f"R18-RUNNER done {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} exit={status} wall={time.time() - t:.1f}s "
      f"mean_runs={ckernel.N_RUNS} peak RSS MB={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}", flush=True)
