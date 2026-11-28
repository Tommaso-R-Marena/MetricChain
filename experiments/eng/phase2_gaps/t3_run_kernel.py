"""T3: one run of engineering's ``RunKernel.lean`` (unchanged) on a list of token files, with time limits.

    python experiments/eng/phase2_gaps/t3_run_kernel.py --log LOG [--load-limit S] [--per-file-limit S] TOKENS...

Runs, from the repository root, ``lake env lean --run experiments/eng/sb_review/lean_kernel/RunKernel.lean full TOKENS...``
with ``LEAN_NUM_THREADS=4`` and no memory limit.  Every output line is written to LOG prefixed by the seconds since the
start.  The process is killed if nothing has been printed within ``--load-limit`` seconds (loading and elaborating the
file, including the proof of ``verifyM_eq``), or if one token file has not finished (the next ``file`` line or the end)
within ``--per-file-limit`` seconds of its own ``file`` line (default 1200: the task's 20-minute limit per
certificate).  A kill is recorded in LOG as ``timeout <name>``.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", type=Path, required=True)
    ap.add_argument("--load-limit", type=float, default=900)
    ap.add_argument("--per-file-limit", type=float, default=1200)
    ap.add_argument("tokens", nargs="+")
    args = ap.parse_args()
    env = dict(os.environ, LEAN_NUM_THREADS="4")
    cmd = ["lake", "env", "lean", "--run", "experiments/eng/sb_review/lean_kernel/RunKernel.lean", "full", *args.tokens]
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    state = {"deadline": t0 + args.load_limit, "current": "(loading)", "killed": None}
    lock = threading.Lock()

    def watchdog():
        while proc.poll() is None:
            with lock:
                if time.monotonic() > state["deadline"]:
                    state["killed"] = state["current"]
                    proc.kill()
                    return
            time.sleep(2)

    threading.Thread(target=watchdog, daemon=True).start()
    with args.log.open("w") as log:
        log.write(f"# cmd lake env lean --run experiments/eng/sb_review/lean_kernel/RunKernel.lean full {' '.join(Path(t).name for t in args.tokens)}\n")
        for line in proc.stdout:
            now = time.monotonic() - t0
            if line.startswith("file "):
                with lock:
                    state["deadline"] = time.monotonic() + args.per_file_limit
                    state["current"] = Path(line.split()[1]).name
                line = f"file {Path(line.split()[1]).name}\n"           # no local paths in the log
            log.write(f"{now:9.1f} {line}")
            log.flush()
        rc = proc.wait()
        if state["killed"]:
            log.write(f"{time.monotonic() - t0:9.1f} timeout {state['killed']}\n")
        log.write(f"{time.monotonic() - t0:9.1f} exit {rc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
