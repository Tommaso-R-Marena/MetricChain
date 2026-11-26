"""P4 step 0: identify, from P2's stored analysis outputs (out/an_*.json, read-only), the instance
analyses of g_GB with at least two sites, and among them those in which
  (i)  the star at argmin E is an exact certificate (P2: certifies_exactly), and
  (ii) P2's plain row-sum condition fails (P2: rowsum_plain_ok == False).
P2_REPORT Statement 5(b): 110 exact of 181; row-sum holds in 97; violated in the other 13.

usage: python3 -B p4_00_find13.py            (prints; writes out/p4_00_find13.json)
This READS P2's numbers; nothing is recomputed here (that is p4_01_shares.py).
"""
import os, re, glob, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.normpath(os.path.join(HERE, "..", "ws_P2"))
rows = []
for p in sorted(glob.glob(os.path.join(P2, "out", "an_fb_*_R3_t0.60_tau*.json"))):
    m = re.match(r"an_(fb_([A-Z]+?)c?(\d+)_([A-Za-z0-9]+)_R3_t0\.60)_tau([0-9.]+)\.json", os.path.basename(p))
    if not m:
        continue
    r = json.load(open(p))
    tag, res, n, bb, tau = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5)
    if r.get("empty"):
        rows.append(dict(tag=tag, res=res, n=n, bb=bb, tau=tau, empty=True))
        continue
    for name in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB"):
        ifc = r.get(f"iface|{name}")
        if not ifc:
            continue
        s = ifc["star_argmin_E"]
        b = ifc.get("ball2")
        rows.append(dict(tag=tag, res=res, n=n, bb=bb, tau=tau, name=name, shape=r["shape_pruned"], size=r["size_pruned"],
                         size_raw=r["size"], clashfree=r["clashfree"],
                         exact=bool(s["certifies_exactly"]), eps_star=s["eps_star"], rowsum=bool(s["rowsum_plain_ok"]),
                         margin=s["rowsum_pairwise_margin"], half=max(s["half_rowsum"]), minexc=min(s["min_excitation"]),
                         ball_eps=(b["eps"] if b else None), has_c3=(r.get(f"Xp|{name}", {}).get("c3") is not None)))
out = {}
for name in ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB"):
    R = [r for r in rows if r.get("name") == name]
    ex = [r for r in R if r["exact"]]
    rs = [r for r in R if r["rowsum"]]
    both = [r for r in R if r["exact"] and r["rowsum"]]
    t13 = [r for r in R if r["exact"] and not r["rowsum"]]
    rs_not_exact = [r for r in R if r["rowsum"] and not r["exact"]]
    print(f"{name:16s}: analyses with >= 2 sites {len(R):4d}; star exact {len(ex):4d}; row-sum holds {len(rs):4d}; "
          f"both {len(both):4d}; exact & row-sum fails {len(t13):3d}; row-sum holds & not exact {len(rs_not_exact)}")
    out[name] = dict(n=len(R), exact=len(ex), rowsum=len(rs), both=len(both), exact_not_rowsum=[(r["tag"], r["tau"]) for r in t13])
print("\nThe instances of g_GB with the star exact and P2's plain row-sum condition failing:")
print(f"{'tag':28s} {'tau':5s} {'shape (X′)':40s} {'size':>8s} {'half rowsum max':>16s} {'min excit.':>10s} {'P2 pairwise margin':>19s}")
for r in rows:
    if r.get("name") == "GB" and r["exact"] and not r["rowsum"]:
        print(f"{r['tag']:28s} {r['tau']:5s} {str(r['shape']):40s} {r['size']:8d} {r['half']:16.4f} {r['minexc']:10.4f} {r['margin']:19.4f}")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
json.dump(dict(summary=out, rows=rows), open(os.path.join(HERE, "out", "p4_00_find13.json"), "w"), indent=0)
print("\nwrote out/p4_00_find13.json;  DONE p4_00_find13")
