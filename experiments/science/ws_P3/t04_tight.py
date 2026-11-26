"""
P3 -- how tight is the ANALYSIS-ONLY bound?  Rigorous term-by-term bound (class mode: all state pairs,
all contexts; termwise.TermBound with the interval enclosures of encl.EnvelopeSup) on the third-order
constants c_ijk of g_GB, against the constants that P2 measured by exact enumeration
(ws_P2/out/an_fb_<tag>_tau<tau>.json, key "Xp|GB" -> c3, product domain X').
No joint state is enumerated here: the inputs are the descreening tables and coordinates.

usage: python3 -B t04_tight.py OUTJSON SEQ:BB:TAU [...]
"""
import sys, os, json, time, itertools
import numpy as np
from p3core import GBModel, P2DIR
from encl import EnvelopeSup
from termwise import TermBound

RND = 1.0 + 1e-9
out = {}
fn_out = sys.argv[1]
for spec in sys.argv[2:]:
    seq, bb, tau = spec.split(":")[0], spec.split(":")[1], float(spec.split(":")[2])
    tag = f"fb_{seq}_{bb}_R3_t0.60"
    pj = os.path.join(P2DIR, "out", f"an_{tag}_tau{tau:.2f}.json")
    if not os.path.exists(pj):
        print(f"{spec}: no P2 output {pj}"); continue
    r = json.load(open(pj))
    if r.get("empty") or "Xp|GB" not in r or not r["Xp|GB"].get("c3"):
        print(f"{spec}: no per-triple constants in P2's output"); continue
    c3 = r["Xp|GB"]["c3"]
    t0 = time.time()
    G = GBModel(r["seq"], bb, tau=tau)
    assert list(G.k) == r["shape_pruned"], (G.k, r["shape_pruned"])
    sup = EnvelopeSup(G)
    TB = TermBound(G, sup=sup, kmax=3, pad_I=G.ns * 2e-10)
    rows = []
    for key, meas in c3.items():
        T = tuple(int(v) for v in key.split(","))
        if min(G.k[i] for i in T) < 2:
            continue
        bs = TB.self_bound(T) * RND; bc = TB.cross_bound(T) * RND
        rows.append((T, meas, bs, bc))
        assert bs + bc >= meas, (T, meas, bs, bc)
    if not rows:
        continue
    a = np.array([[x[1], x[2], x[3]] for x in rows])
    pos = a[:, 0] > 1e-9
    ratios = (a[pos, 1] + a[pos, 2]) / a[pos, 0]
    out[spec] = dict(n=G.ns, k=list(map(int, G.k)), ntriples=len(rows), sum_meas=float(a[:, 0].sum()), sum_self=float(a[:, 1].sum()),
                     sum_cross=float(a[:, 2].sum()), max_meas=float(a[:, 0].max()), max_bound=float((a[:, 1] + a[:, 2]).max()),
                     ratio_min=float(ratios.min()), ratio_med=float(np.median(ratios)), ratio_max=float(ratios.max()), seconds=time.time() - t0)
    o = out[spec]
    print(f"{spec}: n {G.ns}, states {list(G.k)}, {len(rows)} triples; measured (P2): max {o['max_meas']:.3e} sum {o['sum_meas']:.3e} | certified by analysis: "
          f"max {o['max_bound']:.3e} sum {o['sum_self'] + o['sum_cross']:.3e} (self {o['sum_self']:.2e}) | ratio of sums {(o['sum_self'] + o['sum_cross']) / o['sum_meas']:.0f}, "
          f"per triple min/median/max {o['ratio_min']:.0f}/{o['ratio_med']:.0f}/{o['ratio_max']:.0f}; self part alone / measured sum {o['sum_self'] / o['sum_meas']:.1f}  [{o['seconds']:.0f}s]", flush=True)
    json.dump(out, open(fn_out, "w"), indent=1)
