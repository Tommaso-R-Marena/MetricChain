"""
P5 -- Proposition 11 of the report: what a SIGNED term at the reference context buys.

For every subset T and state y_T, with d_T(y_T) = Delta_T g(x0; y_T) the mixed difference in the
anchor context (signed, exact; it costs the evaluations of the ball of radius |T|):

    sup_z |Delta_T g(z; y_T)|  <=  |d_T(y_T)| + sum_{j not in T} c^anch_{T u {j}},                      (*)
    sum_{|T|=m} c_T^anch       <=  sum_{|T|=m} max_y |d_T(y)| + (m+1) sum_{|T'|=m+1} c_T'^anch.            (**)

Checked here by exact enumeration at every (T, y_T, context) of the instances; then the certified version
(P3's chat for the (m+1)-sets) is compared with P3's Gamma_m and Gamma_{m+1}.

usage: python3 -B s4_refbound.py      (needs out/s1_*.json; log: logs/s4_refbound.log; about 2 min)
"""
import sys, os, json, itertools, time
import numpy as np
from p5lib import *

log = Tee(os.path.join(HERE, "logs", "s4_refbound.log"))
nchk = nviol = 0
rmin, rmax = np.inf, 0.0
out = {}
for seq, bb, tau in (("L6", "H", 0.60), ("L8", "H", 0.60), ("S4", "H", 0.70), ("S5", "H", 0.70), ("S6", "H", 0.70)):
    tag = f"{seq}_{bb}_{tau:.2f}"
    s1 = json.load(open(os.path.join(HERE, "out", f"s1_{tag}.json")))
    G, st, shape, f, g, E, x0 = build(seq, bb, tau)
    n = G.ns
    mo = min(5, n)
    cs = {}       # T -> array over y_T (reduced axes of T) of sup over contexts |D_T|
    dref = {}     # T -> array over y_T of |d_T(y_T)| (anchor context)

    def cb(T, D):
        other = tuple(i for i in range(n) if i not in T)
        A = np.abs(D)
        cs[T] = A.max(axis=other, keepdims=True) if other else A
        idx = [slice(None)] * n
        for i in other:
            idx[i] = slice(x0[i], x0[i] + 1) if D.shape[i] == shape[i] else slice(0, 1)
        dref[T] = A[tuple(idx)]
    anch_walk(g, x0, n, mo, cb, minorder=3)
    cT = {T: float(v.max()) for T, v in cs.items()}
    states_checked = 0
    for m in range(3, mo):
        Tm = [T for T in cs if len(T) == m]
        lhs_sum = sum(cT[T] for T in Tm)
        dsum = sum(float(dref[T].max()) for T in Tm)
        hi_sum = sum(cT[T] for T in cs if len(T) == m + 1)
        for T in Tm:
            extra = sum(cT[tuple(sorted(T + (j,)))] for j in range(n) if j not in T and shape[j] >= 2)
            bound = dref[T] + extra                      # array over y_T
            bad = cs[T] > bound + 1e-10
            nchk += bound.size; nviol += int(bad.sum())
            states_checked += bound.size * int(np.prod([shape[i] for i in range(n) if i not in T]))
            pos = cs[T] > 1e-12
            if pos.any():
                rr = (bound[pos] / cs[T][pos])
                rmin = min(rmin, float(rr.min())); rmax = max(rmax, float(rr.max()))
        ok = lhs_sum <= dsum + (m + 1) * hi_sum + 1e-10
        nchk += 1; nviol += 0 if ok else 1
        Gm = sum(s1["Gamma"][str(m)]); Gm1 = sum(s1["Gamma"][str(m + 1)])
        out[f"{tag}_{m}"] = dict(truth=lhs_sum, dref=dsum, exact_bound=dsum + (m + 1) * hi_sum, cert_bound=dsum + (m + 1) * Gm1, Gamma_m=Gm, Gamma_m1=Gm1)
        log(f"  {seq}/{bb} m = {m}: sum_T c_T = {lhs_sum:.4e}; sum_T max|d_T| (signed reference terms) = {dsum:.4e}; (**) with exact (m+1)-constants = {dsum + (m + 1) * hi_sum:.4e}; "
            f"certified version sum max|d_T| + (m+1) Gamma_(m+1) = {dsum + (m + 1) * Gm1:.4e}  vs  Gamma_m = {Gm:.4e}  and  Gamma_(m+1) = {Gm1:.4e} kcal/mol")
    log(f"  {seq}/{bb}: {g.size} states; (*) checked for every (T, y_T) against the sup over all contexts ({states_checked} (T, y_T, context) triples)")
log(f"checks of (*) and (**): {nchk}, violations: {nviol}; ratio bound/exact in [{rmin:.3g}, {rmax:.3g}]")
json.dump(out, open(os.path.join(HERE, "out", "s4_refbound.json"), "w"), indent=1)
log.done()
