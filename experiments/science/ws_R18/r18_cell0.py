#!/usr/bin/env python3
"""R18: the stored maximisers of the bound search (job M-014, x005_anyplacement.jsonl), each taken as the PRODUCT
instance it decodes to (their `Family.decode`, their `Instance`, their Python reference through the R18 adapter,
exact rule), against the worst product instance found by the product search (job M-008, x005_cost.jsonl).

If the product search were converged, no product instance of the same family could cost more than its "worst found".

usage: python3 -I -B r18_cell0.py [--u <u>] <n> [<n> ...]        (their code: use ulimit -v)
"""
import json, sys, time, resource
from pathlib import Path
HERE = Path(__file__).resolve().parent
COPY = HERE / "rerun_copy"
sys.path.insert(0, str(COPY / "src")); sys.path.insert(0, str(COPY / "experiments" / "eng" / "twolevel"))
import numpy as np
import run_search
from metricchain_eng.twolevel.adversary import Family
from metricchain_eng.twolevel.ckernel import Evaluator
RES = Path("/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c/experiments/eng/twolevel/results")
args = sys.argv[1:]
only_u = None
if args and args[0] == "--u":
    only_u = float(args[1])
    args = args[2:]
ns = [int(x) for x in args]
t0 = time.time()
prod = {}
for line in (RES / "x005_cost.jsonl").read_text().splitlines():
    c = json.loads(line)
    prod[(c["u"], c["n"], c["phi"])] = max(s["best_value"] for s in c["searches"])
rows = []
for line in (RES / "x005_anyplacement.jsonl").read_text().splitlines():
    c = json.loads(line)
    if c["n"] not in ns or (only_u is not None and c["u"] != only_u):
        continue
    key = (c["u"], c["n"], c["phi"])
    na = c["n"] * c["a"]
    P, _ = run_search.design_params(c["n"], c["u"], c["phi"], c["design"])
    ev = Evaluator(P)
    best_prod, viol = -1e300, 0
    for s in c["searches"]:
        fam = Family(ev, k=c["k"], monotone=(s["family"] == "monotone"))
        F, d0, c_in = fam.decode(np.array(s["best_x"]))
        R = ev.run(fam.instance(F, d0, c_in), s["oracle"])
        viol += bool(R.violations())
        best_prod = max(best_prod, R.lcost)
    bound = max(s["best_value"] for s in c["searches"])
    rows.append(dict(u=c["u"], n=c["n"], phi=c["phi"], na=na, worst_product_found=prod[key], bound_searched=bound, product_from_bound_maximisers=best_prod, violations=viol))
    r = rows[-1]
    print(f"u={r['u']:g} n={r['n']} phi={r['phi']:.2f}: worst product found {r['worst_product_found']:.6f}; bound searched {(bound - prod[key]) / na:+.5f} n a; "
          f"best product instance among the 4 stored bound-maximisers {(best_prod - prod[key]) / na:+.5f} n a  ({best_prod - prod[key]:+.4f} in ln)", flush=True)
out = HERE / "logs" / ("cell0_n" + "_".join(str(x) for x in ns) + ("" if only_u is None else f"_u{only_u:g}") + ".json")
if not out.exists():
    out.write_text(json.dumps(rows, indent=0) + "\n")
d = [(r["product_from_bound_maximisers"] - r["worst_product_found"]) / r["na"] for r in rows]
e = [(r["bound_searched"] - r["worst_product_found"]) / r["na"] for r in rows]
print(f"cells {len(rows)} (n in {ns}); a stored bound-maximiser, as a product instance, costs MORE than the worst product instance found: "
      f"in {sum(x > 1e-9 for x in d)} cells (by more than 1e-4 n a: {sum(x > 1e-4 for x in d)}; more than 1e-3 n a: {sum(x > 1e-3 for x in d)}); largest {max(d):+.5f} n a")
print(f"cells where the bound searched exceeds the worst product found by more than 1e-4 n a: {sum(x > 1e-4 for x in e)}; of these, with a product instance among the stored "
      f"bound-maximisers that reaches the bound to within 1e-6 n a: {sum(1 for x, y in zip(d, e) if y > 1e-4 and abs(x - y) < 1e-6)}")
print(f"runs violating a claim of the theorem: {sum(r['violations'] for r in rows)}")
print(f"wall {time.time() - t0:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
