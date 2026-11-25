"""
mut_summary.py -- workstream R6: the negative controls (five mutations of the algorithm, campaign.py MUT_*), from the data files.
For each mutation: completed runs, runs in which the check that the mutation should break is violated, and what else is violated.
usage: python3 mut_summary.py [subdirectory of data/, e.g. pass1]
"""
import json, glob, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sub = sys.argv[1] if len(sys.argv) > 1 else ""
EXPECT = {"neg_tol": "('v:", "noharper": "('iii:", "maxform": "('width", "close_at_no": "L>U", "q_no_eta": "('ii: p(s_j) > q"}
out = {}
for name in ("neg_tol", "noharper", "maxform", "close_at_no", "q_no_eta"):
    recs = []
    for f in sorted(glob.glob(os.path.join(HERE, "data", sub, "MUT_%s_*.jsonl" % name))):
        recs += [json.loads(l) for l in open(f) if l.strip()]
    ok = [r for r in recs if "harness_limit" not in r]
    c = collections.Counter()
    for r in ok:
        viol = [str(x) for x in r["det"] + r["good"]]
        if name == "close_at_no":
            hit = r["status"] == "closed_L>U"
        else:
            hit = any(v.startswith(EXPECT[name]) for v in viol)
        c["detected"] += hit
        c["any_violation"] += bool(viol) or r["status"] == "closed_L>U"
        c["every_run_claim_violated"] += bool(r["det"])
        c["good_event_claim_violated"] += bool(r["good"])
        c["iv"] += any(v.startswith("('iv") for v in viol)
        c["cap"] += any(v.startswith("('cap") for v in viol)
        c["big"] += r["lnM"] > 36.84
        if r["status"] == "closed":
            c["invalid_final"] += (r["lo"] > 1e-9 or r["up"] < -1e-9)
    out[name] = dict(runs=len(ok), requested=len(recs), **c)
    print("%-12s runs %2d (of %2d) | detected by its own check: %2d | any violation: %2d | (iv) violated: %d | cap of 40c5bd7 violated: %d | "
          "invalid final bracket: %d | runs with more than 1e16 points: %d" % (name, len(ok), len(recs), c["detected"], c["any_violation"], c["iv"], c["cap"],
                                                                               c["invalid_final"], c["big"]))
json.dump(out, open(os.path.join(HERE, "data", sub, "mut_summary.json"), "w"), indent=1)
