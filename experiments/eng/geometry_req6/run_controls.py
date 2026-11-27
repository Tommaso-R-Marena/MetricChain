"""Validation controls of GEOMETRY-REQ-0006 -> results/controls.json.

    python run_controls.py

NOT TRUSTED (orchestration); the controls are described in gr6_controls.py.
"""
from __future__ import annotations

import sys
import time

import gr6_common as common

common.limit_memory()

import gr6_controls as controls  # noqa: E402
import gr6_kernel as kernel  # noqa: E402


def main():
    kernel.set_precision()
    t0 = time.perf_counter()
    rec = controls.run_all()
    rec["seconds"] = time.perf_counter() - t0
    path = common.write_json("controls.json", rec)
    for k, v in rec.items():
        if isinstance(v, dict):
            print(f"{k}: certified = {v['certified']} (expected {v['expected_certified']}) -> {'PASS' if v['passed'] else 'FAIL'}")
    print(f"all controls passed: {rec['all_passed']};  wrote results/{path.name}")
    return 0 if rec["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
