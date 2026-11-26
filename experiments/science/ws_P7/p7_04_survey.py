"""
P7 item 4: how common is a gap, and how small is the tree, on all the enumerated instances P4 used.

Models (every one a pairwise function on P2's pruned product X'; grids built by P4's code):
  so|<res>   P4's second-order lower model  L = f + g_star - sum_{i<j changed} c_ij  for the five residuals
             (908 analyses);
  to|pair, to|site   P4's third-order pairwise lower models of g_GB (pair form, site form; 136 instances each);
  en|ff14SB, en|ff03, en|ff15ipq   the vacuum energy of a force field itself (pairwise; "the energy is its
             own model"): f, f + g_03, f + g_ipq.   [the ff99SB energy is so|ff99SB-ff14SB up to 1e-10]

For each model: the reference of the certificate is x0 = argmin E (P4's reference) if x0 minimises the
model ("criterion holds"; then the certificate certifies x0 for the whole class), and otherwise the
model's own minimiser (then a certificate proves min L = L(r), a lower bound for min E).
  depth 0   state-dependent shares at the reference (LP with slack t; integer certificate; exact check);
            t < 0: a GAP of the pairwise relaxation (its value is reported);
  depth 1   for a gap: which sites certify every leaf after one branching; fewest leaves; whether a
            single-state split (x_i = a | x_i != a: two leaves) certifies; whether one triple closes it;
  depth 2   if no site works: the smallest tree of depth two (within a budget of leaf programmes).
Brute force: the exact minimum of the published integer instance over the whole domain (must be 0 and
is compared with every root certificate) and over every leaf that is certified.

usage: python3 -B p7_04_survey.py [--only SUBSTR] > logs/p7_04_survey.log
       writes out/p7_04_survey.json (also after every instance: a checkpoint); last line "DONE p7_04_survey"
"""
import sys, os, json, time, itertools, math
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
a_ = sys.argv[1:]
only = a_[a_.index("--only") + 1] if "--only" in a_ else None
TOL = 1e-9
BUDGET = 6000                                   # leaf programmes per model for the depth-two search
print(f"p7_04_survey  started {L7.now()}", flush=True)
STAT = dict(models=0, root_cert=0, root_bf=0, root_viol=0, leaf_cert=0, leaf_bf=0, leaf_viol=0, leaf_truth=0)


def analyse(G, r, x0):
    """G: model grid (float); r: reference of the certificate; returns a dict (see module docstring)."""
    pm = PM.from_grid(G, r)
    pw = float(np.abs(pm.grid() - (G - G[r])).max())
    out = dict(shape=list(pm.shape), size=int(np.prod(pm.shape)), nact=len(pm.active()), ref=list(r), ref_is_x0=bool(tuple(r) == tuple(x0)), pairwise_err=pw)
    if pw > 1e-6:
        out["status"] = "not pairwise"
        return out
    STAT["models"] += 1
    ipm = IPM(pm); IG = ipm.grid()
    imin = int(IG.min())
    out["published_min"] = imin
    n = pm.n; Dfull = pm.full_domain(); act = pm.active()
    if not act:
        out.update(status="trivial", t=None, depth=0)
        return out
    s = L7.shares_lp(pm)
    t = s["t"]
    out["t"] = t
    if t is None:
        out["status"] = "LP failed"
        return out
    if t > TOL:
        m = L7.shares_to_messages(ipm, Dfull, s["s"])
        LB = L7.leaf_bound(ipm, Dfull, m)[0]
        ok = bool(LB >= 0)
        out.update(status="shares" if ok else "shares LP positive but integer check failed", depth=0 if ok else None, LB=int(LB))
        if ok:
            STAT["root_cert"] += 1; STAT["root_bf"] += 1
            if LB > imin:
                STAT["root_viol"] += 1
        return out
    if t >= -TOL:
        out.update(status="degenerate (|t| <= 1e-9)", depth=None)
        return out
    # ------------------------------------------------------------ a gap
    out["status"] = "gap"
    out["relaxation"] = L7.dual_lp(pm, Dfull)["val"]
    # exactness of "no shares": the primal LP vertex read as a rational point, re-checked in integers, value < 0
    pv = L7.primal_lp(pm)
    rp = L7.rationalise_point(pm, ipm, pv["mu1"], pv["mu2"])
    out["gap_exact"] = bool(rp is not None and rp["value_int"] < 0 and rp["value"] < 0)
    out["vertex_den"] = rp["den"] if rp is not None else None
    out["margin"] = L4.margin_at(G, r)
    cache = {}
    nlp = [0]

    def leaf(D):
        key = tuple(tuple(int(v) for v in d) for d in D)
        if key not in cache:
            c = L7.certify_leaf(pm, ipm, D)
            nlp[0] += 1
            b = int(L7.box_min(IG, D))
            if b < 0:
                STAT["leaf_truth"] += 1
            if c["ok"]:
                STAT["leaf_cert"] += 1; STAT["leaf_bf"] += 1
                if c["LB"] > b:
                    STAT["leaf_viol"] += 1
            cache[key] = dict(ok=c["ok"], kind=c["kind"], lp=c["lp"], LB=c["LB"], bf=b)
        return cache[key]

    working = []; ref_ok = []
    for i in act:
        oks = [leaf(L7.fix(Dfull, i, a))["ok"] for a in pm.dom[i]]
        if all(oks):
            working.append(i)
        if leaf(L7.fix(Dfull, i, r[i]))["ok"]:
            ref_ok.append(i)
    out["working"] = working; out["ref_leaf_ok"] = ref_ok
    out["least_leaves_depth1"] = min((pm.shape[i] for i in working), default=None)
    single = []
    for i in act:
        for a in pm.dom[i]:
            if a == r[i] or not leaf(L7.fix(Dfull, i, a))["ok"]:
                continue
            D = [d.copy() for d in Dfull]; D[i] = np.array([b for b in pm.dom[i] if b != a])
            if leaf(D)["ok"]:
                single.append((int(i), int(a)))
    out["single_state_splits"] = single
    if working:
        out["depth"] = 1
        out["least_leaves"] = 2 if single else out["least_leaves_depth1"]
    else:
        def best_tree(D, depth):
            c = leaf(D)
            if c["ok"]:
                return 1
            if depth == 0 or nlp[0] > BUDGET:
                return None
            best = None
            for i in range(n):
                if len(D[i]) < 2:
                    continue
                tot = 0
                for a in D[i]:
                    sub = best_tree(L7.fix(D, i, a), depth - 1)
                    if sub is None:
                        tot = None
                        break
                    tot += sub
                if tot is not None and (best is None or tot < best):
                    best = tot
            return best
        bt = best_tree(Dfull, 2)
        out["depth"] = 2 if bt is not None else (">2" if nlp[0] <= BUDGET else "budget")
        out["least_leaves"] = bt
    # one triple
    T_all = list(itertools.combinations(act, 3))
    if len(T_all) <= 600:
        good = []
        for T in T_all:
            rs = L7.shares_lp(pm, triple=T)
            if rs["t"] is not None and rs["t"] > TOL:
                m = L7.shares_to_messages(ipm, Dfull, rs["s"], triple=T)
                LB = L7.leaf_bound(ipm, Dfull, m, triple=T)[0]
                if LB >= 0:
                    good.append(list(T))
                    STAT["root_bf"] += 1
                    if LB > imin:
                        STAT["root_viol"] += 1
        out["ntriples"] = len(T_all); out["closing_triples"] = good
    out["leaf_programmes"] = nlp[0]
    return out


rows = []
files = L7.instance_files()
nf = 0
for (tag, fam, nres, bb, taus, p) in files:
    if only and only not in tag:
        continue
    J = json.load(open(p))
    if J.get("empty"):
        continue
    names = [nm for nm in L7.RESIDUALS if f"iface|{nm}" in J]
    if not names:
        continue
    t0 = time.time()
    inst = L4.load_instance(tag, float(taus))
    nf += 1
    shape = inst["shape"]
    f = inst["f"]
    todo = []
    for name in names:
        Lmod, x0, E, C = L7.second_order_grid(inst, name)
        todo.append((f"so|{name}", Lmod, x0, E))
    if "GB" in names and sum(1 for k in shape if k >= 2) >= 3 and len(shape) >= 3:
        m_pair, m_site, m_env, x0, E = L7.third_order_grids(inst)
        todo.append(("to|pair", m_pair, x0, E)); todo.append(("to|site", m_site, x0, E))
    todo.append(("en|ff14SB", f, L4.argmin_index(f), f))
    for ff, nm in (("ff03", "ff03-ff14SB"), ("ff15ipq", "ff15ipq-ff14SB")):
        if nm in inst["R"]:
            Eff = f + inst["R"][nm]
            todo.append((f"en|{ff}", Eff, L4.argmin_index(Eff), Eff))
    line = []
    for (model, G, x0, E) in todo:
        margin0 = L4.margin_at(G, x0)
        crit = bool(margin0 >= -1e-9)
        r = x0 if crit else L4.argmin_index(G)
        res = analyse(G, r, x0)
        res.update(tag=tag, family=fam, nres=nres, bb=bb, tau=taus, model=model, criterion=crit, margin_x0=margin0)
        rows.append(res)
        line.append(f"{model.split('|')[1][:6]}:{'S' if res['status'] == 'shares' else ('G' + str(res.get('depth')) if res['status'] == 'gap' else res['status'][:3])}{'' if crit else '*'}")
    print(f"[{time.time() - t00:6.0f}s] {fam}{nres}/{bb} tau {taus} X' {list(shape) if len(shape) <= 8 else str(len(shape)) + ' sites'}: " + " ".join(line) + f"  ({time.time() - t0:.1f}s)", flush=True)
    json.dump(dict(rows=rows, stat=STAT, complete=False), open(os.path.join(L7.HERE, "out", "p7_04_survey.partial.json"), "w"))

outname = "p7_04_survey.json" if not only else f"p7_04_survey_{only}.json"
json.dump(dict(rows=rows, stat=STAT, complete=True), open(os.path.join(L7.HERE, "out", outname), "w"), indent=0)

# ---------------------------------------------------------------- tables
def table(title, R):
    print(f"\n{title}")
    print(f"{'model':18s} {'models':>6s} | {'shares (depth 0)':>16s} {'GAP':>4s} {'degenerate':>10s} | gap: {'depth 1':>7s} {'depth 2':>7s} {'deeper/unknown':>14s} | {'two leaves suffice':>18s} {'one triple closes':>17s}")
    keys = sorted(set(r["model"] for r in R))
    for key in keys + ["ALL"]:
        Q = [r for r in R if key == "ALL" or r["model"] == key]
        Q = [r for r in Q if r.get("status") not in ("not pairwise",)]
        g = [r for r in Q if r["status"] == "gap"]
        print(f"{key:18s} {len(Q):6d} | {sum(r['status'] in ('shares', 'trivial') for r in Q):16d} {len(g):4d} {sum(r['status'].startswith('degenerate') for r in Q):10d} | "
              f"     {sum(r['depth'] == 1 for r in g):7d} {sum(r['depth'] == 2 for r in g):7d} {sum(r['depth'] not in (1, 2) for r in g):14d} | "
              f"{sum(bool(r['single_state_splits']) for r in g):18d} {sum(bool(r.get('closing_triples')) for r in g):17d}")


notpw = [r for r in rows if r.get("status") == "not pairwise"]
print(f"\n{nf} instance files; {len(rows)} models; not pairwise (skipped): {len(notpw)}: {sorted(set(r['model'] for r in notpw))}; largest pairwise error among the others {max(r['pairwise_err'] for r in rows if r.get('status') != 'not pairwise'):.1e}")
A = [r for r in rows if r["criterion"] and not r["model"].startswith("en|")]
table("(A) P4's population: lower models whose minimiser is the reference x0 = argmin E  (certificate of x0 for the class)", A)
B = [r for r in rows if not r["criterion"] and not r["model"].startswith("en|")]
table("(B) lower models NOT minimised at x0: certificate of the model's own minimum (a lower bound for min E)", B)
Cc = [r for r in rows if r["model"].startswith("en|")]
table("(C) the vacuum energy of a force field as its own (pairwise) model: certificate of its minimiser", Cc)
table("(A)+(B)+(C)", rows)
gp_all = [r for r in rows if r.get("status") == "gap"]
print(f"\ngaps proved exactly (a rational point of the local polytope, constraints re-checked in integers, with negative value): "
      f"{sum(r['gap_exact'] for r in gp_all)} of {len(gp_all)}; denominators {sorted(set(r['vertex_den'] for r in gp_all if r['vertex_den']))}")
print("\nEvery model with a gap:")
print(f"{'instance':11s} {'tau':4s} {'model':18s} {'x0 min.':>7s} {'sites':>5s} {'states':>8s} {'margin':>9s} {'gap':>10s} | {'sites that certify':24s} {'depth':>5s} {'least leaves':>12s} {'closing triples':>15s}")
for r in rows:
    if r.get("status") == "gap":
        print(f"{r['family'] + str(r['nres']) + '/' + r['bb']:11s} {r['tau']:4s} {r['model']:18s} {'yes' if r['criterion'] else 'no':>7s} {r['nact']:5d} {r['size']:8d} {r['margin']:9.5f} {-r['relaxation']:10.6f} | "
              f"{str(r['working']) if len(str(r['working'])) <= 24 else str(len(r['working'])) + ' sites':24s} {str(r['depth']):>5s} {str(r['least_leaves']):>12s} {str(len(r['closing_triples'])) + ' of ' + str(r['ntriples']) if 'ntriples' in r else 'n/a':>15s}")
fam = {}
for r in rows:
    if r.get("status") in ("shares", "gap", "trivial") or str(r.get("status")).startswith("degenerate"):
        k = r["family"]
        fam.setdefault(k, [0, 0])
        fam[k][0] += 1; fam[k][1] += (r["status"] == "gap")
print("\ngaps by family (models with a gap / models):", {k: f"{v[1]}/{v[0]}" for k, v in sorted(fam.items())})
print(f"\nBRUTE FORCE: {STAT['models']} models enumerated on their whole domain (exact minimum of the published instance); "
      f"root certificates (shares or one triple) accepted {STAT['root_bf']} and compared with it: violations {STAT['root_viol']}; "
      f"leaf certificates accepted {STAT['leaf_cert']}, compared with the exact leaf minimum {STAT['leaf_bf']}: violations {STAT['leaf_viol']}; leaves with a negative exact minimum {STAT['leaf_truth']}")
print(f"[{time.time() - t00:.0f}s] wrote out/{outname}   finished {L7.now()}")
print("DONE p7_04_survey")
