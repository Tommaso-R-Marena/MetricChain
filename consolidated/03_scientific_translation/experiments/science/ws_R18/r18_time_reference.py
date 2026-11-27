#!/usr/bin/env python3
"""R18: how long does THEIR Python reference (meanrun.mean_run) take per stored maximiser?  (planning only)
usage: python3 -I -B r18_time_reference.py <n> [<n> ...]"""
import json, sys, time, resource
from pathlib import Path
HERE = Path(__file__).resolve().parent
COPY = HERE / "rerun_copy"
sys.path.insert(0, str(COPY / "src")); sys.path.insert(0, str(COPY / "experiments" / "eng" / "twolevel"))
import numpy as np
import run_search
from metricchain_eng.twolevel.adversary import Family
from metricchain_eng.twolevel.ckernel import Evaluator      # the R18 adapter (Python reference)
ns = [int(x) for x in sys.argv[1:]] or [1000]
for line in (COPY / "experiments/eng/twolevel/results/x005_cost.jsonl").read_text().splitlines():
    c = json.loads(line)
    if c["n"] not in ns or c["phi"] != 0.5:
        continue
    t = time.time()
    P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
    ev = Evaluator(P)
    t_setup = time.time() - t
    s = c["searches"][0]
    fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
    F, d0, c_in = fam.decode(np.array(s["best_x"]))
    inst = fam.instance(F, d0, c_in)
    t = time.time(); R = ev.run(inst, s["oracle"]); t_run = time.time() - t
    print(f"u={c['u']} n={c['n']} phi={c['phi']} J={ev.C.J} j_stop={R.j_stop} L={P.L} setup {t_setup:.2f}s run {t_run:.2f}s "
          f"lcost {R.lcost:.6f} stored {s['best_value']:.6f}", flush=True)
print("peak RSS MB:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
