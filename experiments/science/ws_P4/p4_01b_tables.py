"""P4 item 1, tables from out/p4_01_shares.json (no computation beyond counting).
usage: python3 -B p4_01b_tables.py   -> prints Markdown; last line 'DONE p4_01b_tables'."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "out", "p4_01_shares.json")))
yn = lambda b: "yes" if b else "no"
ss_ok = lambda r: r["shares"] or (r["sshares_slack_exact"] is not None and r["sshares_slack_exact"] >= 0)
lab = lambda r: f"{r['res']}{r['nres']}/{r['bb']} ({r['tau'][1:]})"

print("### T1 -- per residual: all instance analyses with at least two sites\n")
print("| residual | analyses | exact criterion holds | P2's plain row-sum (c) | row-sum for the deficits (w) | share certificate 11.18b(d) | state-dependent shares (LP) | shares exist but criterion fails |")
print("|---|---|---|---|---|---|---|---|")
for name in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB"):
    R = [r for r in rows if r["name"] == name]
    ex = [r for r in R if r["exact"]]
    print(f"| {name} | {len(R)} | {len(ex)} | {sum(r['rowsum_c'] for r in R)} | {sum(r['rowsum_w'] for r in R)} | {sum(r['shares'] for r in R)} | "
          f"{sum(ss_ok(r) for r in ex)} | {sum(r['shares'] and not r['exact'] for r in R)} |")

print("\n### T2 -- g_GB: by family (exact = the reference minimises the lower model L on X')\n")
print("| family | analyses | exact | plain row-sum (c) | row-sum (w) | shares (w) | exact and no shares | not exact (star fails) | of these: shares exist |")
print("|---|---|---|---|---|---|---|---|---|")
G = [r for r in rows if r["name"] == "GB"]
for fam, nm in (("S", "Ser"), ("K", "Lys"), ("LKSE", "LKSE"), ("V", "Val"), ("L", "Leu"), ("F", "Phe")):
    R = [r for r in G if r["res"] == fam]
    ne = [r for r in R if not r["exact"]]
    print(f"| {nm} | {len(R)} | {sum(r['exact'] for r in R)} | {sum(r['rowsum_c'] for r in R)} | {sum(r['rowsum_w'] for r in R)} | {sum(r['shares'] for r in R)} | "
          f"{sum(r['exact'] and not r['shares'] for r in R)} | {len(ne)} | {sum(r['shares'] for r in ne)} |")

print("\n### T3 -- g_GB: the polar and charged instances in which the star fails (the reference does not minimise L)\n")
print("| instance | X' | min Delta_i | L(x0) - min L | max half row sum of w | shares | smallest violated set (flow): excess | densest set (brute force): excess |")
print("|---|---|---|---|---|---|---|---|")
for r in G:
    if r["res"] in ("S", "K", "LKSE") and not r["exact"]:
        D = [d for d in r["Delta"] if d is not None]
        print(f"| {lab(r)} | {r['size']} | {min(D):.3f} | {-r['margin']:.2f} | {max(r['half_w']):.2f} | {yn(r['shares'])} | {r['overdense']}: {r['excess']:.2f} | {r['bf_S']}: {r['bf_excess']:.2f} |")

print("\n### T4 -- all (instance, residual) analyses in which the criterion holds and the share certificate fails\n")
print("| residual | instance | X' | margin of the criterion | over-dense set: excess | row-sum (w) | state-dependent shares: exact slack |")
print("|---|---|---|---|---|---|---|")
cnt = {}
for r in rows:
    if r["exact"] and not r["shares"]:
        cnt[r["name"]] = cnt.get(r["name"], 0) + 1
        if r["name"] in ("GB",):
            sl = r["sshares_slack_exact"]
            print(f"| {r['name']} | {lab(r)} | {r['shape']} | {r['margin']:.4f} | {r['overdense']}: {r['excess']:.4f} | {yn(r['rowsum_w'])} | {'%.4f' % sl if sl is not None else 'LP failed'} |")
print("\ncounts by residual:", cnt)
print("state-dependent shares fail although the criterion holds:",
      {nm: sum(1 for r in rows if r["name"] == nm and r["exact"] and not ss_ok(r)) for nm in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB")})
print("smallest exact slack of an accepted state-share certificate:", min((r["sshares_slack_exact"] for r in rows if r["sshares_slack_exact"] is not None and r["sshares_slack_exact"] >= 0), default=None))
print("plain row-sum (c) holds and shares (w) fail [the plain condition is not a theorem for a pairwise known part]:",
      {nm: sum(1 for r in rows if r["name"] == nm and r["rowsum_c"] and not r["shares"]) for nm in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB")})
print("plain row-sum (c) holds and the criterion fails:",
      {nm: [lab(r) for r in rows if r["name"] == nm and r["rowsum_c"] and not r["exact"]] for nm in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB")})
print("anchored constants (variant): criterion holds",
      {nm: sum(1 for r in rows if r["name"] == nm and r["margin_anch"] >= -1e-9) for nm in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB")},
      "; shares", {nm: sum(1 for r in rows if r["name"] == nm and r["shares_anch"]) for nm in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB")},
      "; min over all analyses of min_x (E - L_anchored) =", min(r["sound_anch"] for r in rows))
print("analyses with fewer than two multi-state sites (GB):", sum(1 for r in G if r["nact"] < 2), "; with |X'| = 1:", sum(1 for r in G if r["size"] == 1))
print("DONE p4_01b_tables")
