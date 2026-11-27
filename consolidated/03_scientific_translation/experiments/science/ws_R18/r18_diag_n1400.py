#!/usr/bin/env python3
"""R18: which stored maximiser of chunk cost_n1400 is not reproduced by the convention of the published runs, by how
much, and is it the tie rule?  (their code through the adapter: old convention with the tie rule, and with plain
floating-point comparisons, tie = 0)          usage: python3 -I -B r18_diag_n1400.py [chunk]"""
import json, sys, resource
from pathlib import Path
HERE = Path(__file__).resolve().parent
COPY = HERE / "rerun_copy"
sys.path.insert(0, str(COPY / "src")); sys.path.insert(0, str(COPY / "experiments" / "eng" / "twolevel"))
import numpy as np
import run_search
from metricchain_eng.twolevel.adversary import Family, objective_value
from metricchain_eng.twolevel.ckernel import Evaluator
chunk = sys.argv[1] if len(sys.argv) > 1 else "cost_n1400"
job = chunk.split("_")[0]
path = COPY / "chunks" / chunk / "experiments" / "eng" / "twolevel" / "results" / f"x005_{job}.jsonl"
n_s = n_bad = 0
for line in path.read_text().splitlines():
    c = json.loads(line)
    P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
    ev, ev0 = Evaluator(P), Evaluator(P, tie=0.0)
    for s in c["searches"]:
        fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
        F, d0, c_in = fam.decode(np.array(s["best_x"]))
        inst = fam.instance(F, d0, c_in)
        n_s += 1
        v = objective_value(ev.run(inst, s["oracle"], legacy_classification=True), s["objective"])
        if abs(v - s["best_value"]) >= 1e-6:
            n_bad += 1
            v0 = objective_value(ev0.run(inst, s["oracle"], legacy_classification=True), s["objective"])
            ve = objective_value(ev.run(inst, s["oracle"]), s["objective"])
            best_cell = max(x["best_value"] for x in c["searches"] if x["objective"] == "cost")
            print(f"u={c['u']} n={c['n']} phi={c['phi']} {s['family']}/{s['oracle']}: stored {s['best_value']!r}; old convention with the tie rule {v!r} "
                  f"(difference {v - s['best_value']:+.3e}); with tie = 0: {v0!r} (difference {v0 - s['best_value']:+.3e}); exact rule {ve!r}; "
                  f"c_in={c_in!r} d0={d0}; is the cell's worst stored search: {s['best_value'] == best_cell} (cell's worst {best_cell!r})")
print(f"chunk {chunk}: searches {n_s}; not reproduced within 1e-6: {n_bad}")
print("peak RSS MB: %.1f" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
