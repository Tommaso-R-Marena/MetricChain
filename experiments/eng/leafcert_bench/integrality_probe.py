"""Exploratory, written AFTER the protocol was frozen (PROTOCOL.txt, section 9): why does the producer branch
on instances whose relaxation is tight at the root?

    python experiments/eng/leafcert_bench/integrality_probe.py        # writes results/exploratory_integrality.json

For every instance of the main pass that was certified, whose relaxation is tight at the root (value of
the linear programme = optimum) and for which the producer (integer message passing) needed more than one
leaf, three things are tried, each a full producer run whose certificate both engines check:

  1. the leaf bound from the rounded linear programme ("lp") on the same instance: one leaf means that
     integer messages that certify the optimum at the root exist and the message passing stalled below them;
  2. if the rounded programme also needs more than one leaf: the instance with every table multiplied by
     2, and by 6 (the certificate is then for another instance, in a finer unit).  One leaf there means
     that messages exist in halves or sixths of the unit, i.e. that the integrality of the messages in the
     instance's own unit is what forces the branching;
  3. the message passing on the scaled instances, for comparison.

Nothing here changes a number of the benchmark; the instances are regenerated from their stored seeds.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "src"))

import config  # noqa: E402
from metricchain_eng.leafprod import families, produce  # noqa: E402


def scaled(inst, factor):
    return {"H": [[factor * v for v in row] for row in inst["H"]],
            "J": {key: [[factor * v for v in row] for row in table] for key, table in inst["J"].items()}}


def run(inst, bound):
    res = produce(inst, bound=bound, branching=config.MAIN["branching"], order=config.MAIN["order"],
                  seed=config.MAIN["seed"], time_limit=config.TIME_LIMIT, partial=False, **config.CAPS)
    return {"status": res.status, "L": res.L, "leaf_boxes": res.stats["leaf_boxes"], "depth": res.stats["depth"],
            "root_value": res.stats["root_value"], "root_lp_value": res.stats["root_lp_value"],
            "seconds": res.stats["time_total"]}


def main():
    results = HERE / "results"
    rows = []
    t0 = time.time()
    for path in sorted((results / "main").glob("*.json")):
        if path.name.startswith("_"):
            continue
        doc = json.loads(path.read_text())
        for rec in doc["instances"]:
            prod = rec.get("producer")
            opt, lp = rec["agreement"]["optimum"], rec["root_lp"]["value"]
            if not prod or prod["status"] != "certified" or opt is None or lp is None:
                continue
            if (opt - lp) / max(1.0, abs(opt)) >= 1e-9 or prod["stats"]["leaf_boxes"] < 2:
                continue
            inst = families.make(doc["family"], doc["n"], doc["k"], rec["seed"])
            assert families.digest(inst) == rec["digest"]
            row = {"family": doc["family"], "k": doc["k"], "n": doc["n"], "index": rec["index"], "optimum": opt,
                   "root_lp": lp, "mp": {"leaf_boxes": prod["stats"]["leaf_boxes"], "root_value": prod["stats"]["root_value"]},
                   "lp": run(inst, "lp"), "scaled": {}}
            if row["lp"]["leaf_boxes"] > 1:
                for factor in (2, 6):
                    twice = scaled(inst, factor)
                    row["scaled"][str(factor)] = {"lp": run(twice, "lp"), "mp": run(twice, "mp")}
            rows.append(row)
    out = {"protocol_version": config.PROTOCOL_VERSION, "exploratory": True, "seconds": time.time() - t0, "rows": rows}
    (results / "exploratory_integrality.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    one = sum(r["lp"]["leaf_boxes"] == 1 for r in rows)
    print(f"{len(rows)} instances: tight at the root, more than one leaf with message passing; "
          f"one leaf with the rounded programme: {one}")
    for factor in ("2", "6"):
        got = [r for r in rows if factor in r["scaled"]]
        print(f"  tables x{factor}: {len(got)} tried; one leaf with the rounded programme: "
              f"{sum(r['scaled'][factor]['lp']['leaf_boxes'] == 1 for r in got)}; with message passing: "
              f"{sum(r['scaled'][factor]['mp']['leaf_boxes'] == 1 for r in got)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
