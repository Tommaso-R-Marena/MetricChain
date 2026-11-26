#!/usr/bin/env python3
"""Run every numerical check quoted in docs/ensemble/ENSEMBLE_REPORT.md and store the output.

Usage: python3 experiments/ensemble/run_all.py        (about twelve minutes, single thread; the last script,
benchmark_controls.py, regenerates and verifies the reference instances of docs/ensemble/BENCHMARK_CONTROLS.md)
Exit code 0 iff every script ends with PASS and check_quotes.py (run last) finds every number quoted in the
report in the output just written.  The output is written to experiments/ensemble/output.txt.
"""
import pathlib, subprocess, sys, time

here = pathlib.Path(__file__).resolve().parent
scripts = ["exposedness_checks.py", "rigidity_checks.py", "pair_capacity_checks.py", "finite_temperature_checks.py",
           "platform_checks.py", "lifted_checks.py", "benchmark_controls.py"]
lines, ok = [], True
for name in scripts:
    t0 = time.time()
    res = subprocess.run([sys.executable, str(here / name)], capture_output=True, text=True)
    lines.append(f"===== {name} (exit {res.returncode}, {time.time() - t0:.0f} s) =====")
    lines.append(res.stdout.rstrip())
    if res.stderr.strip():
        lines.append("--- stderr ---"); lines.append(res.stderr.rstrip())
    ok &= res.returncode == 0 and res.stdout.rstrip().endswith("PASS")
out = "\n".join(lines) + "\n"
(here / "output.txt").write_text(out)
# last: do the numbers quoted in the report still agree with the output just written?  (check_quotes.py reads
# output.txt and output_threshold.txt and the report; its own block is appended afterwards)
res = subprocess.run([sys.executable, str(here / "check_quotes.py")], capture_output=True, text=True)
tail = [f"===== check_quotes.py (exit {res.returncode}) =====", res.stdout.rstrip()]
if res.stderr.strip():
    tail += ["--- stderr ---", res.stderr.rstrip()]
ok &= res.returncode == 0 and res.stdout.rstrip().endswith("PASS")
tail.append("ALL PASS" if ok else "SOME CHECK FAILED")
out += "\n".join(tail) + "\n"
(here / "output.txt").write_text(out)
print(out)
sys.exit(0 if ok else 1)
