"""R7: numbers quoted in ENG-RES-0007 / -0008 / -0009 and in the compute ledger, traced to the stored outputs (own code)."""
import json, math
from pathlib import Path
E = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng"
cost = [json.loads(l) for l in open(E / "twolevel/results/x005_cost.jsonl")]
claims = [json.loads(l) for l in open(E / "twolevel/results/x005_claims.jsonl")]
conv = [json.loads(l) for l in open(E / "twolevel/results/x005_converge.jsonl")]
for name, rows in (("M-008 cost", cost), ("M-009 claims", claims), ("M-010 converge", conv)):
    print(f"{name}: tasks {len(rows)}, instances evaluated {sum(s['n_eval'] for r in rows for s in r['searches'])}, "
          f"task time {sum(r['seconds'] for r in rows) / 3600:.1f} core-hours, longest task {max(r['seconds'] for r in rows):.0f} s, "
          f"searches {sum(len(r['searches']) for r in rows)}, violations recorded {sum(s['n_violations'] for r in rows for s in r['searches'])}")
# extremes over all searches (ENG-RES-0008 table 'claims')
allrows = cost + claims + conv
for u in (0.5, 1.0, 2.0):
    ex = {}
    for r in allrows:
        if r["u"] != u: continue
        runs = [r["flat"]["bottom"], r["flat"]["top"]]
        for s in r["searches"]:
            for k, v in s["extremes"].items():
                if k == "margin_iii": ex[k] = min(ex.get(k, math.inf), v)
                else: ex[k] = max(ex.get(k, -math.inf), v)
    print(f"u={u}: " + ", ".join(f"{k}={v:.3g}" for k, v in sorted(ex.items())))
# generic chain: timings and statistics quoted in ENG-RES-0007 / -0009
g = json.load(open(E / "chain_cover/results/generic_Sc16.json"))["rows"]
print("generic cover rows, seconds:", {k: g[k]["seconds"] for k in g})
e = json.load(open(E / "chain_cover/results/generic_Sc16_entropy.json"))["rows"]
print("entropy seconds (total):", {k: round(e[k]["seconds"]["total"], 1) for k in e}, " sum n=5..12:", round(sum(e[k]["seconds"]["total"] for k in e if int(k) <= 12), 1))
dmax = {k: max(max(abs(v["median"] - v["mean"]), abs(v["mean_weighted"] - v["mean"])) for v in e[k]["sigma"].values()) for k in e}
print("largest |median - mean| or |weighted - mean| of sigma per n:", {k: round(v, 3) for k, v in dmax.items()})
last = {r: round(e["14"]["sigma"][r]["mean"] - e["13"]["sigma"][r]["mean"], 4) for r in e["14"]["sigma"]}
print("increment of sigma from 13 to 14 torsions:", last)
print("pairs per bead at 17 beads:", e["14"]["pairs_per_bead"], " increase per bead from 16 to 17:", round(e["14"]["pairs_per_bead"]["mean_over_classes"] - e["13"]["pairs_per_bead"]["mean_over_classes"], 3))
