"""
P7 item 3, continued: EXACT certificates with two triplet constraints where one does not suffice.

p7_03_triplet.py found (floating point) that for LKSE6/E and L16/P2 no single triple closes the gap and
that two triples do.  Here the sets of triples it reports (the closing pairs and the greedy set) are
turned into exact certificates: an LP with slack over shares and, for every triple and each of its
pairs, a table lam (the part of the reparametrised pair table handed to the triple); conversion to
integers with exact repairs; acceptance only by the integer checker p7lib.multi_triple_bound
    U_i  = min_a [H_i(a) + sum_j m_ij(a)]
    R_ij = min_{a,b} [J_ij(a,b) - m_ij(a) - m_ji(b) - sum_{T contains i,j} lam_{T,ij}(a,b)]
    Q_T  = min_{a,b,c} [lam_{T,pq}(a,b) + lam_{T,pr}(a,c) + lam_{T,qr}(b,c)]
    0 <= sum U + sum R + sum Q
and comparison with the exact minimum of the published instance over X' (int64 enumeration; = 0 at x0).
The single closing triples of p7_03 are re-verified through the same general checker.

usage: python3 -B p7_03b_multi.py > logs/p7_03b_multi.log   (writes out/p7_03b_multi.json; last line "DONE p7_03b_multi")
"""
import sys, os, json, time
sys.dont_write_bytecode = True
import numpy as np
import p7lib as L7
from p7lib import PM, IPM, L4

t00 = time.time()
print(f"p7_03b_multi  started {L7.now()}")
five = {(f"{g['family']}{g['nres']}/{g['bb']}", g["tau"]): g for g in json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]}
trip = json.load(open(os.path.join(L7.HERE, "out", "p7_03_triplet.json")))
out = []
nchk = nviol = ncert = 0
for r in trip:
    g = five[(r["instance"], r["tau"])]
    inst = L4.load_instance(g["tag"], float(g["tau"]))
    Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
    pm = PM.from_grid(Lmod, x0); ipm = IPM(pm); D = pm.full_domain()
    imin = int(ipm.grid().min())
    assert imin == 0
    sets = [[tuple(T)] for T in r["closing"]]
    if r["multi"] is not None:
        for pr in r["multi"].get("pairs_closing", []):
            sets.append([tuple(T) for T in pr])
        gs = [tuple(T) for T in r["multi"]["greedy"]]
        if sorted(gs) not in [sorted(s_) for s_ in sets]:
            sets.append(gs)
    print(f"\n=== {r['instance']} tau {r['tau']} split {r['split']}: X' = {list(pm.shape)}")
    for Ts in sets:
        t0 = time.time()
        res = L7.multi_triple_lp(pm, Ts)
        m, lam = L7.multi_triple_to_int(ipm, D, res["s"], res["lam"], Ts)
        LB, U, R, Q = L7.multi_triple_bound(ipm, D, m, lam, Ts)
        ok = bool(LB >= 0)
        ncert += ok
        if ok:
            nchk += 1
            nviol += (LB > imin)
        nnum = sum(len(v) for v in m.values()) + sum(v.size for v in lam.values())
        nops = sum(len(D[i]) * (pm.n - 1) for i in range(pm.n)) + sum(len(D[i]) * len(D[j]) * 3 for i in range(pm.n) for j in range(i + 1, pm.n)) \
            + sum(len(D[T[0]]) * len(D[T[1]]) * len(D[T[2]]) * 2 for T in Ts)
        print(f"  triples {Ts}: LP slack t = {res['t']:.9f}; exact integer bound {LB} -> {'CERTIFIED' if ok else 'not certified'}; "
              f"certificate: {nnum} integers; checker: about {nops} additions; LP {res['nvar']} x {res['nrow']} ({time.time() - t0:.1f}s)")
        out.append(dict(instance=r["instance"], tau=r["tau"], split=r["split"], triples=[list(T) for T in Ts], t=res["t"], LB=int(LB), certified=ok,
                        n_integers=int(nnum), n_additions=int(nops)))
json.dump(out, open(os.path.join(L7.HERE, "out", "p7_03b_multi.json"), "w"), indent=1)
print(f"\nTOTAL: {len(out)} sets of triples; {ncert} exact certificates; {nchk} compared with the exact minimum of the published instance; violations {nviol}")
print(f"[{time.time() - t00:.0f}s] wrote out/p7_03b_multi.json   finished {L7.now()}")
print("DONE p7_03b_multi")
