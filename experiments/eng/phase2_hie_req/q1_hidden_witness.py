#!/usr/bin/env python3
"""Re-check, by routes independent of the class code of q1_lemma_b, the cases where the bracket over the hidden
types (t_T > Theta) exceeds +0.01 at Theta >= 1.1 nh (their expectation: <= 0.01; report: <= 0.002).

(1) Large case: the computed G is checked to be FEASIBLE with dict-based classes (q1_crosscheck.class_dicts),
    np.diff Lipschitz and nu <= 0 on V_0 -- feasibility alone makes the witness value a valid lower bound for
    the pointwise maximum, so the excess is real if this check passes.
(2) Smaller analogues: Dijkstra (and HiGHS LP where small enough) recompute the bracket.
"""
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import q1_lemma_b as q  # noqa: E402
import q1_crosscheck as xc  # noqa: E402

out = []
pr = lambda s: (print(s, flush=True), out.append(s))


def bracket_from(Gd, ns, roles, u, th):
    c = q.consts(u)
    n = sum(ns)
    Theta = th * n * c["h"]
    tj = [q.tcost(x) for x in ns]
    T = [j for j, r in enumerate(roles) if r == "T"]
    nP = sum(ns[j] for j, r in enumerate(roles) if r == "P")
    best = -math.inf
    arg = None
    for d, g in Gd.items():
        tT = sum(tj[j][d[j]] for j in T)
        if tT > Theta:
            b = g - sum(tj[j][d[j]] for j in range(len(ns))) - nP * c["h"] + min(tT, Theta - (n - nP) * c["h"])
            if b > best:
                best, arg = b, d
    return best, arg


t0 = time.time()
for ns, roles, u, th, par in [((30, 30, 50, 70), "QQTT", 1.0, 1.1, True), ((120, 120, 120), "QQT", 0.5, 1.1, True)]:
    r = q.evaluate(ns, roles, u, th, use_parity=par)
    sol = q.solve(ns, roles, u, th * sum(ns) * q.consts(u)["h"], use_parity=par)
    G = sol["G"]
    groups = xc.class_dicts(ns, roles, u, th)
    worst_cls = max(max(G[d] for d in mem) - min(G[d] for d in mem) for g in groups for mem in g.values())
    lip = max(np.max(np.abs(np.diff(G, axis=ax))) for ax in range(G.ndim))
    nu0max = float(np.max((G - sol["t"])[sol["V0"]]))
    pr(f"[feasibility] ns={ns} roles={roles} u={u} th/h={th}: Vhid={r['Vhid']:+.5f}; dict-class spread={worst_cls:.1e}, "
       f"max step={lip:.6f} (u={u}), max nu on V0={nu0max:+.1e}  -> witness is feasible: "
       f"{worst_cls <= 1e-9 and lip <= u + 1e-9 and nu0max <= 1e-9}")

pr("[small analogues] Dijkstra / LP recomputation of the hidden bracket at Theta >= 1.1 nh")
for ns, roles, u, th in [((12, 12, 20, 28), "QQTT", 1.0, 1.1), ((15, 15, 25, 35), "QQTT", 1.0, 1.1),
                         ((10, 10, 16, 24), "QQTT", 2.0, 1.1), ((8, 8, 12, 16), "QQTT", 4.0, 1.1),
                         ((6, 6, 10, 14), "QQTT", 4.0, 1.1), ((20, 20, 30), "QQT", 0.5, 1.1)]:
    r = q.evaluate(ns, roles, u, th)
    dist = xc.dijkstra(ns, roles, u, th)
    bd, argd = bracket_from(dist, ns, roles, u, th)
    s = f"ns={ns} roles={roles} u={u} th/h={th}: Vhid(min-plus)={r['Vhid']:+.5f} Vhid(Dijkstra)={bd:+.5f} at y={argd}"
    if np.prod([x + 1 for x in ns]) <= 8100:
        Gsum, _, size = xc.lp(ns, roles, u, th)
        bl, argl = bracket_from(Gsum, ns, roles, u, th)
        s += f" Vhid(LP)={bl:+.5f} [LP size {size}]"
    pr(s)
pr(f"# time {time.time() - t0:.0f}s")
(HERE / "out" / "q1_hidden_witness.txt").write_text("\n".join(out) + "\n")
