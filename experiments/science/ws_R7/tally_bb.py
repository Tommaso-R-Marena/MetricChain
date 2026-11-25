import json
a = json.load(open("out_own_certified_bb_optima_14_16.json")) + json.load(open("out_own_certified_bb_optima_17_24.json"))
done = [r for r in a if r["complete"] and not r["smaller_cover_found"]]
notdone = [r for r in a if not r["complete"]]
print("cells attempted:", len(a), "| certified by exact branch and bound:", len(done), "| not finished:", len(notdone))
for r in done: print("  PROVED >=", r["target"], "n =", r["n"], r["key"], "nodes", r["nodes"], "s", r["seconds"], r.get("same_instance_as", ""))
for r in notdone: print("  open   target", r["target"], "n =", r["n"], r["key"], "nodes", r["nodes"], r.get("same_instance_as", ""))
