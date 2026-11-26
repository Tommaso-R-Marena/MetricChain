#!/usr/bin/env python3
"""R19, item 3: the regression claim of addendum A17 (20), item 78, and the tables of items 78, 79 and of SCI-RES-0024, against the logs.

Old logs: commit 90abf0e (extracted with `git show 90abf0e:...` into old_logs_90abf0e/ -- a read-only git command).
New logs: experiments/science/pi_inference/first_order_recovery_*.log at the commit checked out (0930440), read in place.
READ ONLY: nothing is re-run here.  The claim tested: "same items, same digits; more items, a bracket inside the old one at
both ends", in all thirteen runs; then every number of the three tables that a log contains.

Run: python3 -B r19_item3_logs.py > r19_item3_logs.log
"""
import os, re, sys, resource
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.normpath(os.path.join(HERE, "..", "pi_inference")); OLD = os.path.join(HERE, "old_logs_90abf0e")
RUNS = ["K5_m4_w2_enum", "K5_m4_w3_enum", "K5_m5_w3_enum", "LKSEc5_m4_w2_enum", "K12_m3_w7", "K12_m4_w7", "K12_m5_w7", "K12_m4_w6", "K12_m4_w5", "K12_m4_w4",
        "LKSEc12_m4_w7", "LKSEc12_m5_w7", "S12_m5_w7"]
STAGES = ["nothing (the sandwich)", "far pairs", "far pairs and out-of-window terms", "far pairs, terms and the allocation of the penalty"]


def parse(path):
    t = open(path).read(); r = dict(path=path, complete=t.rstrip().splitlines()[-1].startswith("ALL DONE"))
    m = re.search(r"ALL DONE (\d+) s; peak RSS (\d+) MB", t); r["sec"], r["rss"] = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    m = re.search(r"sum of their maxima ([0-9.e+-]+) kT", t); r["summax"] = float(m.group(1))
    m = re.search(r"ball of radius (\d+): (\d+) values", t); r["ball"] = int(m.group(2))
    m = re.search(r"(\d+) evaluated terms exact in a window, (\d+) reduced, (\d+) pairs beyond the band", t); r["exact"], r["reduced"], r["far"] = map(int, m.groups())
    m = re.search(r"allocation of the floating-point allowance \(as P9 built it\): \[([0-9.]+), ([0-9.]+)\], width ([0-9.e+-]+)", t); r["p6"] = tuple(map(float, m.groups()))
    m = re.search(r"certified bracket \[([0-9.]+), ([0-9.]+)\], width D = ([0-9.e+-]+)", t); r["sandwich6"] = (m.group(1), m.group(2)); r["D"] = float(m.group(3))
    m = re.search(r"(\d+) items, (\d+) by the forward route, (\d+) on the mirrored chain(?: \((\d+) of the two through a window inside the chain\))?, (\d+) without a route", t)
    r["items"], r["fwd"], r["rev"], r["noroute"] = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(5)); r["inner"] = int(m.group(4)) if m.group(4) else 0
    m = re.search(r"(\d+) groups \(direction, held site, first site of the window\)", t); r["groups"] = int(m.group(1)) if m else None
    if r["groups"] is None:
        m = re.search(r"groups \(held sites\): ([^;]+);", t); r["groups"] = len(m.group(1).split(","))
    m = re.search(r"largest deviation of a clamped total mass from one: ([0-9.e+-]+)", t); r["mass"] = float(m.group(1))
    r["cls"] = {}
    for m in re.finditer(r"^\| (far|term|alloc) \| (ceiling|floor|both) \| (\d+) \| (\d+) \| ([0-9.e+-]+); ([0-9.e+-]+) \|", t, re.M):
        r["cls"][(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), float(m.group(5)), float(m.group(6)))
    r["rows"] = {}
    for m in re.finditer(r"^\| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| \[([0-9.]+), ([0-9.]+)\] \| \*\*([0-9.e+-]+)\*\* \| ([0-9.]+) \|", t, re.M):
        r["rows"][m.group(1)] = dict(LJ=m.group(2), LP=m.group(3), UE=m.group(4), UP=m.group(5), lo=m.group(6), up=m.group(7), width=m.group(8), ratio=m.group(9))
    m = re.search(r"total (\d+) states, (\d+) violations; controls that must fail on the same states: every item doubled: (\d+) violations; far items of floor and ceiling exchanged: (\d+) violations", t)
    if m: r["hyp"] = dict(states=int(m.group(1)), viol=int(m.group(2)), c1=int(m.group(3)), c2=int(m.group(4)))
    m = re.search(r"EVERY state \((\d+)\): hypotheses .* violated at (\d+) states \(smallest margin ([0-9.e+-]+) kcal/mol\); controls that must fail: every item doubled: (\d+) violations; far items of floor and ceiling exchanged: (\d+) violations; "
                  r"the group means \(a, e, b, c, cp\) by enumeration against the transfer matrix: largest relative deviation ([0-9.e+-]+)", t)
    if m: r["hyp"] = dict(states=int(m.group(1)), viol=int(m.group(2)), margin=float(m.group(3)), c1=int(m.group(4)), c2=int(m.group(5)), devm=float(m.group(6)))
    m = re.search(r"exact ln Z = ([0-9.]+): inside every corrected bracket: (True|False)", t)
    if m: r["exact_lnZ"], r["inside"] = float(m.group(1)), m.group(2) == "True"
    m = re.search(r"put back exactly \(by enumeration; no band model can hold them\): \[([0-9.]+), ([0-9.]+)\], width ([0-9.e+-]+)", t)
    if m: r["best"] = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
    r["z"] = [float(m.group(1)) for m in re.finditer(r"\(([+-][0-9.]+) standard errors\)", t)]
    m = re.search(r"\(4\) P9's raw tables entry by entry at (\d+) random states .* violations of abs\(remainder\) <= table entry: (\d+); largest remainder ([0-9.e+-]+) kcal/mol; ratio entry / remainder: smallest ([0-9.]+), "
                  r"median ([0-9.]+); control that must fail \(every table replaced by its minimum\): (\d+) violations", t)
    if m: r["tables"] = dict(n=int(m.group(1)), viol=int(m.group(2)), rmax=float(m.group(3)), ratio_min=float(m.group(4)), ratio_med=float(m.group(5)), ctrl=int(m.group(6)))
    return r


def main():
    old = {k: parse(os.path.join(OLD, f"first_order_recovery_{k}.log")) for k in RUNS}
    new = {k: parse(os.path.join(NEW, f"first_order_recovery_{k}.log")) for k in RUNS}
    k20 = parse(os.path.join(NEW, "first_order_recovery_K20_m4_w7.log"))
    print(f"all 13 old logs and all 14 new logs end with 'ALL DONE': {all(r['complete'] for r in list(old.values()) + list(new.values()) + [k20])}")
    print("\n=== (1) the regression claim, run by run ===")
    print("| run | items old/new | routed old -> new (inner) | per class routed, old -> new | stage rows 0-2 identical to the last digit (LJ, LP, UE, UP, bracket) | last stage: lower end old -> new | upper end old -> new | new inside old | width old -> new |")
    print("|---|---|---|---|---|---|---|---|---|")
    n_same = n_in = 0; bad = []
    for k in RUNS:
        o, n_ = old[k], new[k]
        ro, rn = o["fwd"] + o["rev"], n_["fwd"] + n_["rev"]
        same_static = (o["sandwich6"] == n_["sandwich6"] and o["D"] == n_["D"] and o["items"] == n_["items"] and o["p6"] == n_["p6"] and o["summax"] == n_["summax"] and o["ball"] == n_["ball"])
        cls_changed = {c: (o["cls"][c][1], n_["cls"][c][1]) for c in o["cls"] if o["cls"][c][1] != n_["cls"][c][1]}
        rows_same = [o["rows"].get(s) == n_["rows"].get(s) for s in STAGES]
        last_o, last_n = o["rows"][STAGES[3]], n_["rows"][STAGES[3]]
        inside = float(last_n["lo"]) >= float(last_o["lo"]) and float(last_n["up"]) <= float(last_o["up"])
        strictly = (float(last_n["lo"]) > float(last_o["lo"])) + (float(last_n["up"]) < float(last_o["up"]))
        # the claim: a stage whose routed items did not change has the same digits; otherwise the new bracket lies inside the old one at both ends
        stage_classes = [(), ("far",), ("far", "term"), ("far", "term", "alloc")]
        ok = same_static
        for q in range(4):
            changed = any(c[0] in stage_classes[q] for c in cls_changed)
            if not changed and not rows_same[q]: ok = False
            if changed:
                a, b = o["rows"][STAGES[q]], n_["rows"][STAGES[q]]
                if not (float(b["lo"]) >= float(a["lo"]) and float(b["up"]) <= float(a["up"])): ok = False
        n_same += int(all(rows_same)); n_in += int(inside)
        if not ok: bad.append(k)
        print(f"| {k} | {o['items']}/{n_['items']} | {ro} -> {rn} ({n_['inner']}) | {cls_changed if cls_changed else 'none changed'} | {rows_same[:3]} | {last_o['lo']} -> {last_n['lo']} | {last_o['up']} -> {last_n['up']} | "
              f"{inside} ({'both ends moved' if strictly == 2 else 'one end moved' if strictly == 1 else 'identical'}) | {last_o['width']} -> {last_n['width']} |")
    print(f"runs in which the claim fails: {bad if bad else 'none'}; runs with all four stage rows identical: {n_same}; runs with the new last bracket inside the old one (weakly): {n_in} of 13")
    print("    (what 'same items' can be read from: the per-class numbers of items with a route; the item tables themselves are not in the logs)")
    # other invariants between old and new
    print("\n=== (2) what else is identical / changed between old and new logs ===")
    for k in RUNS:
        o, n_ = old[k], new[k]; d = []
        for key in ("summax", "ball", "exact", "reduced", "far", "p6", "sandwich6", "D", "items"):
            if o[key] != n_[key]: d.append(f"{key}: {o[key]} -> {n_[key]}")
        h = (o["hyp"]["states"], o["hyp"]["viol"], o["hyp"]["c1"], o["hyp"]["c2"]) == (n_["hyp"]["states"], n_["hyp"]["viol"], n_["hyp"]["c1"], n_["hyp"]["c2"])
        print(f"  {k}: static part {'identical' if not d else '; '.join(d)}; hypothesis check (states, violations, control 1, control 2) old {tuple(o['hyp'][q] for q in ('states', 'viol', 'c1', 'c2'))} "
              f"new {tuple(n_['hyp'][q] for q in ('states', 'viol', 'c1', 'c2'))} {'same' if h else 'DIFFERENT'}; groups {o['groups']} -> {n_['groups']}; z-scores old {o['z']} new {n_['z']}; "
              f"tables check (new only): {n_.get('tables')}; time {o['sec']} -> {n_['sec']} s, RSS {o['rss']} -> {n_['rss']} MB")
    # ------------------------------------------------------------------ item 78 table
    print("\n=== (3) the table of item 78 against the logs ===")
    T78 = [  # run, routed before, now, inner, all, width before, width now, bracket now
        ("K5_m4_w2_enum", 14, 18, 4, 25, "0.002913", "0.002885", "251.3475876", "251.3504722"),
        ("K5_m4_w3_enum", 10, 10, 0, 11, "6.437e-05", "6.437e-05", "251.3484184", "251.3484828"),
        ("K5_m5_w3_enum", 12, 12, 0, 15, "7.104e-06", "7.104e-06", "251.3484424", "251.3484495"),
        ("LKSEc5_m4_w2_enum", 14, 18, 4, 25, "0.001611", "0.001558", "276.4669085", "276.4684663"),
        ("K12_m3_w7", 100, 100, 0, 100, "0.06112", "0.06112", "517.1160739", "517.1771913"),
        ("K12_m4_w7", 380, 415, 35, 465, "8.297e-05", "8.161e-05", "517.1285108", "517.1285924"),
        ("K12_m5_w7", 818, 996, 178, 1346, "2.184e-05", "2.178e-05", "517.1285396", "517.1285614"),
        ("K12_m4_w6", 420, 505, 85, 610, "0.0002786", "0.0002738", "517.1284560", "517.1287298"),
        ("K12_m4_w5", 352, 543, 191, 742, "0.0004217", "0.0003890", "517.1284232", "517.1288122"),
        ("K12_m4_w4", 262, 513, 251, 854, "0.0006875", "0.0006449", "517.1283300", "517.1289748"),
        ("LKSEc12_m4_w7", 380, 415, 35, 465, "0.001537", "0.001414", "655.6120305", "655.6134443"),
        ("LKSEc12_m5_w7", 818, 996, 178, 1346, "0.0001433", "0.0001407", "655.6126392", "655.6127798"),
        ("S12_m5_w7", 818, 996, 178, 1346, "0.001791", "0.001666", "227.3678932", "227.3695587")]
    nbad = 0
    for run, rb, rn, inner, allit, wb, wn, lo_, up_ in T78:
        o, n_ = old[run], new[run]; lo_o = o["rows"][STAGES[3]]; ln_ = n_["rows"][STAGES[3]]
        chk = dict(routed_before=(o["fwd"] + o["rev"], rb), routed_now=(n_["fwd"] + n_["rev"], rn), inner=(n_["inner"], inner), all=(n_["items"], allit),
                   width_before=(float(lo_o["width"]), float(wb)), width_now=(float(ln_["width"]), float(wn)), lo=(ln_["lo"], lo_), up=(ln_["up"], up_))
        wrong = [f"{q}: log {a} vs text {b}" for q, (a, b) in chk.items() if (abs(a - b) > 6e-4 * abs(b) if isinstance(a, float) else a != b)]
        nbad += len(wrong)
        print(f"  {run}: {'all eight numbers agree' if not wrong else 'DISAGREE: ' + '; '.join(wrong)}  (log: routed {o['fwd'] + o['rev']} -> {n_['fwd'] + n_['rev']} ({n_['inner']}) / {n_['items']}; width {lo_o['width']} -> {ln_['width']}; [{ln_['lo']}, {ln_['up']}])")
    print(f"  numbers of the table of item 78 that disagree with the logs: {nbad} of {8 * len(T78)}")
    allz = [abs(z) for k in RUNS for z in new[k]["z"]]; tb = [new[k]["tables"]["ctrl"] for k in RUNS if "tables" in new[k]]
    print(f"  'the means against exact samples within 1.6 standard errors': largest |z| in the nine sampled new logs {max(allz)} ({len(allz)} comparisons); 'the control failing at 343 to 2 733 states': {min(tb)} to {max(tb)} ({len(tb)} logs); "
          f"table violations: {[new[k]['tables']['viol'] for k in RUNS if 'tables' in new[k]]}; smallest ratio entry/remainder per log: {[new[k]['tables']['ratio_min'] for k in RUNS if 'tables' in new[k]]}")
    print(f"  hypothesis violations in the 13 new logs: {[new[k]['hyp']['viol'] for k in RUNS]}; control 1: {[new[k]['hyp']['c1'] for k in RUNS]}; control 2: {[new[k]['hyp']['c2'] for k in RUNS]}")
    print(f"  enumerated: exact ln Z inside every corrected bracket: {[new[k].get('inside') for k in RUNS[:4]]}; largest deviation of the group means: {[new[k]['hyp'].get('devm') for k in RUNS[:4]]}; largest |mass - 1|: {max(new[k]['mass'] for k in RUNS):.1e}")
    for k, gain in (("K12_m4_w5", "8"), ("K12_m4_w4", "6")):
        a, b = float(old[k]["rows"][STAGES[3]]["width"]), float(new[k]["rows"][STAGES[3]]["width"])
        print(f"  '{k}: tighten by {gain} per cent': {100 * (1 - b / a):.1f} % ({a} -> {b}); items newly routed {new[k]['fwd'] + new[k]['rev'] - old[k]['fwd'] - old[k]['rev']}")
    k4 = new["K12_m4_w4"]; print(f"  band 4: 'the subsets that still have none carry 1.1e-4 nats of first-order slack per side': log {k4['cls'][('alloc', 'both')][3]}; D^2/4 = {k4['D'] ** 2 / 4:.3g} for D = {k4['D']}")
    # ------------------------------------------------------------------ item 79
    print("\n=== (4) item 79 (Lys20) against its log ===")
    c = k20["cls"]; rw = k20["rows"]
    print(f"  sum of the table maxima {k20['summax']} (text 45.2); ball {k20['ball']} (text 385 566); sandwich D = {k20['D']} [{k20['sandwich6'][0]}, {k20['sandwich6'][1]}] (text 0.01814 [800.505214, 800.523352]); "
          f"corrected [{rw[STAGES[3]]['lo']}, {rw[STAGES[3]]['up']}] width {rw[STAGES[3]]['width']} (text [800.5150660, 800.5154710], 4.05e-4); stages {rw[STAGES[1]]['width']}, {rw[STAGES[2]]['width']}, {rw[STAGES[3]]['width']} "
          f"(text 7.6e-4, 7.0e-4, 4.05e-4); D/width {rw[STAGES[3]]['ratio']} (text 45)")
    far = c[("far", "ceiling")][0] + c[("far", "floor")][0]; term = c[("term", "ceiling")][0] + c[("term", "floor")][0]; al = c[("alloc", "both")][0]
    routed = sum(v[1] for v in c.values())
    print(f"  items {k20['items']} = {far} far + {term} terms + {al} subsets (text 6 175 = 156 + 1 664 + 4 355); with a route {routed} = {k20['fwd'] + k20['rev']} (text 3 823), inner {k20['inner']} (text 2 029); without {k20['noroute']} (text 2 352), "
          f"of them four-site subsets {al - c[('alloc', 'both')][1]} (text 2 240), their first-order slack {c[('alloc', 'both')][3]} (text 1.2e-5 per side); groups {k20['groups']} (text 156)")
    print(f"  hypotheses: {k20['hyp']} (text: 5 380 states, no violation, controls 8 029 and 3 501); z {k20['z']} (text: within 1.4); tables {k20['tables']} (text: 20 000 states, no violation, smallest ratio 10.9, median 240, control 5 556); "
          f"{k20['sec']} s, {k20['rss']} MB (text 1 390 s, 5.5 GB)")
    # ------------------------------------------------------------------ SCI-RES-0024
    print("\n=== (5) SCI-RES-0024 section 3 (a) and section 4 against the logs ===")
    T = {"4": ("517.1427360", "517.1139664"), "5": ("517.1411643", "517.1158165"), "6": ("517.1390752", "517.1176354"), "7": ("517.1329875", "517.1256580")}
    for b, (lo_txt, up_txt) in T.items():
        s = new[f"K12_m4_w{b}"]["rows"][STAGES[0]]
        print(f"  band {b}: ln Z(m-) log {s['up']} text {lo_txt} {'ok' if s['up'] == lo_txt else 'DISAGREE'}; ln Z(m+) log {s['lo']} text {up_txt} {'ok' if s['lo'] == up_txt else 'DISAGREE'}")
    f4, f7 = new["K12_m4_w4"]["rows"][STAGES[0]], new["K12_m4_w7"]["rows"][STAGES[0]]
    print(f"  'from band 4 to band 7: 0.0097 on the floor's side, 0.0117 on the ceiling's': {float(f4['up']) - float(f7['up']):.4f}, {float(f7['lo']) - float(f4['lo']):.4f}")
    print(f"  monotone in the band: floors {[new[f'K12_m4_w{b}']['rows'][STAGES[0]]['up'] for b in '4567']}, ceilings {[new[f'K12_m4_w{b}']['rows'][STAGES[0]]['lo'] for b in '4567']}")
    for k, txt in (("K12_m4_w7", "8.30e-5 -> 8.16e-5"), ("LKSEc12_m5_w7", "1.43e-4 -> 1.41e-4"), ("K12_m4_w4", "6.9e-4 -> 6.4e-4")):
        print(f"  section 4, {k}: log {old[k]['rows'][STAGES[3]]['width']} -> {new[k]['rows'][STAGES[3]]['width']} (text {txt})")
    print(f"  section 2: '20 groups for Lys12 at band 7 and 156 for Lys20': {new['K12_m4_w7']['groups']} (order 4), {new['K12_m5_w7']['groups']} (order 5), {k20['groups']}; "
          f"'D^2/4: 1.3e-5 of the 2.2e-5 left for Lys12 at order 5, 8e-5 of the 4e-4 for Lys20': D^2/4 = {new['K12_m5_w7']['D'] ** 2 / 4:.3g} (width {new['K12_m5_w7']['rows'][STAGES[3]]['width']}), {k20['D'] ** 2 / 4:.3g} (width {k20['rows'][STAGES[3]]['width']})")
    # ------------------------------------------------------------------ the D^2/4 rule on the enumerated instances
    print("\n=== (6) 'the loss between groups is about D^2/4': what the four enumerated logs say (loss = corrected width - width with the routed items put back exactly) ===")
    for k in RUNS[:4]:
        for tag, r in (("old", old[k]), ("new", new[k])):
            wcorr = float(r["rows"][STAGES[3]]["up"]) - float(r["rows"][STAGES[3]]["lo"]); loss = wcorr - r["best"][2]
            print(f"  {k} ({tag}): D = {r['D']}, corrected {wcorr:.4g}, exact treatment of the same items {r['best'][2]:.4g}, loss {loss:.3g} = {loss / (r['D'] ** 2 / 4):.2f} x D^2/4 ({r['groups']} groups)")
    print(f"ALL DONE; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
