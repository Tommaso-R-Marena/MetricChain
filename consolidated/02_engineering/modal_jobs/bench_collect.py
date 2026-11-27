"""Collect the results of a detached run of ``modal_jobs/bench_app.py::launch`` from the modal.Dict into the result
files of the repository.  Safe to run at any time and repeatedly; a successor can run it after an interruption.

    python modal_jobs/bench_collect.py --driver nested_bench --job certified1+instances1 [--delete]

``--delete`` removes the collected entries from the Dict (entries expire after seven days without access anyway).
Failures recorded by a task are printed and written to ``<result file>.failed``; they are not result rows.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "modal_jobs"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--driver", default="nested_bench")
    ap.add_argument("--job", required=True)
    ap.add_argument("--delete", action="store_true")
    args = ap.parse_args()
    import bench_app

    sub, module, _, _ = bench_app.DRIVERS[args.driver]
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "experiments" / "eng" / sub))
    mod = importlib.import_module(module)
    store = modal.Dict.from_name(bench_app.STORE, create_if_missing=True)
    keys = set(store.keys())
    for jb in args.job.split("+"):
        out = bench_app.result_path(args.driver, jb)
        done = bench_app.stored_ids(out)
        ids = [t["id"] for t in mod.tasks(jb)]
        new, failed = 0, 0
        for tid in ids:
            key = f"{jb}|{tid}"
            if key not in keys:
                continue
            if tid not in done:
                r = store[key]
                if "error" in r:
                    failed += 1
                    with Path(str(out) + ".failed").open("a") as fh:
                        fh.write(json.dumps(r) + "\n")
                    print(f"FAILED {tid}: {r['error']}")
                else:
                    with out.open("a") as fh:
                        fh.write(json.dumps(r) + "\n")
                    done.add(tid)
                    new += 1
            if args.delete:
                store.pop(key)
        missing = [tid for tid in ids if tid not in done]
        print(f"{jb}: {new} new rows, {failed} failures, {len(done)} of {len(ids)} stored, {len(missing)} outstanding")
        for tid in missing[:40]:
            print("   outstanding:", tid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
