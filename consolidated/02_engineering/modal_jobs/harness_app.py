"""Modal job: the theory division's falsification harness, full mode, under seeds other than its default.

Ephemeral app (``modal run`` only).  Part of the independent replication asked for in
THY-REQ-0005 (item 2): ``python3 experiments/falsify_conjectures.py --seed N`` must report 79
tests "survived" and 17 "REFUTED (as documented)" for every seed.

    modal run modal_jobs/harness_app.py --seeds 101,202,303

The upstream files under ``experiments/`` are mounted unchanged; library versions are pinned to
those of the local research environment, so that the remote runs differ from the local ones in
hardware and operating system only.  Verdict lines are written to
``experiments/eng/audit_replication/harness_full_seed<N>.txt``.

Resource bounds: 2 cores and 4 GiB per seed, one container per seed, ``TIMEOUT_S`` seconds, no retries.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT_S = 3 * 3600

app = modal.App("metricchain-eng-harness")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("numpy==2.5.5", "scipy==1.18.1", "mpmath==1.3.0")
    .add_local_dir(ROOT / "experiments", "/root/mc/experiments",
                   ignore=["eng/**", "out/**", "**/__pycache__/**", "certs/**"])
)


@app.function(image=image, cpu=2.0, memory=4096, timeout=TIMEOUT_S, max_containers=4, retries=0)
def run_harness(seed: int, quick: bool = False) -> dict:
    import platform
    import subprocess
    import sys

    t0 = time.time()
    cmd = [sys.executable, "experiments/falsify_conjectures.py", "--seed", str(seed)] + (["--quick"] if quick else [])
    proc = subprocess.run(cmd, cwd="/root/mc", capture_output=True, text=True)
    lines = proc.stdout.splitlines()
    import numpy
    import scipy
    return {
        "seed": seed, "quick": quick, "returncode": proc.returncode, "seconds": round(time.time() - t0, 1),
        "stdout": proc.stdout, "stderr_tail": proc.stderr[-4000:],
        "survived": sum(1 for ln in lines if ln.startswith("[") and "survived" in ln.split("]")[0]),
        "refuted_as_documented": sum(1 for ln in lines if "REFUTED (as documented)" in ln.split("]")[0]),
        "verdict_lines": sum(1 for ln in lines if ln.startswith("[")),
        "last_line": lines[-1] if lines else "",
        "platform": {"python": platform.python_version(), "machine": platform.machine(),
                     "system": platform.platform(), "numpy": numpy.__version__, "scipy": scipy.__version__},
    }


@app.local_entrypoint()
def main(seeds: str = "101,202,303", quick: bool = False):
    out_dir = ROOT / "experiments" / "eng" / "audit_replication"
    out_dir.mkdir(parents=True, exist_ok=True)
    seed_list = [int(s) for s in seeds.split(",")]
    for res in run_harness.map(seed_list, kwargs={"quick": quick}, order_outputs=False):
        tag = "quick" if quick else "full"
        (out_dir / f"harness_{tag}_seed{res['seed']}.txt").write_text(res.pop("stdout"))
        (out_dir / f"harness_{tag}_seed{res['seed']}.meta.json").write_text(json.dumps(res, indent=1) + "\n")
        print(json.dumps({k: v for k, v in res.items() if k != "stderr_tail"}), flush=True)
