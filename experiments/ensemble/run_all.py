#!/usr/bin/env python3
"""Run every numerical check quoted in docs/ensemble/ENSEMBLE_REPORT.md and store the output.

Usage: python3 experiments/ensemble/run_all.py        (about fifteen minutes, single thread)
Exit code 0 iff every script ends with PASS.  The output is written to experiments/ensemble/output.txt.
"""
import pathlib, subprocess, sys, time

here = pathlib.Path(__file__).resolve().parent
scripts = ["exposedness_checks.py", "rigidity_checks.py", "pair_capacity_checks.py", "finite_temperature_checks.py",
           "platform_checks.py"]
lines, ok = [], True
for name in scripts:
    t0 = time.time()
    res = subprocess.run([sys.executable, str(here / name)], capture_output=True, text=True)
    lines.append(f"===== {name} (exit {res.returncode}, {time.time() - t0:.0f} s) =====")
    lines.append(res.stdout.rstrip())
    if res.stderr.strip():
        lines.append("--- stderr ---"); lines.append(res.stderr.rstrip())
    ok &= res.returncode == 0 and res.stdout.rstrip().endswith("PASS")
lines.append("ALL PASS" if ok else "SOME CHECK FAILED")
out = "\n".join(lines) + "\n"
(here / "output.txt").write_text(out)
print(out)
sys.exit(0 if ok else 1)
