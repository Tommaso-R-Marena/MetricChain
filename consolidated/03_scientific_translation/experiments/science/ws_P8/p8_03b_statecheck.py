"""
P8 step 3 -- the check that can actually fail for Theorem AH: every pair term, EVERY state, every order.

For every atom pair p <= q, every state x of the enumerated domain and every order m,

        | t_pq(x) - I_{m-1} t_pq(x) |   <=   sum_{T subset S(x), |T| = m}  (summand of the pair in the bound of T)

for the variants 'SA' (anchored hosts + state-resolved; Theorem AH), 'S' (state-resolved; Proposition S with P3's
Proposition 1) and 'P3'.  The left side is the exact remainder of the single pair term (no cancellation between pairs
can hide a violation); the right side is the pair's own envelope at x.  This is the per-pair, per-state form of the
inequality the certificate uses, |g - I_{m-1} g|(x) <= sum_{T subset S(x)} chat_T.

usage: python3 -B p8_03b_statecheck.py SEQ BB TAU [--budget SECONDS]
needs out/m1_<tag>.npz (P3 summands), out/sr_<tag>.npz (S, SA summands).  Writes logs/sc_<tag>.log, out/sc_<tag>.json
"""
import sys, os, json, time, itertools
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"sc_{tag}.json")) and "--force" not in a:
    print(f"out/sc_{tag}.json exists: this run is complete; nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"sc_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"sc_{tag}.log"), append=resume)
t0 = time.time()
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz")); Zs = np.load(os.path.join(HERE, "out", f"sr_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
st = G.product_states(); S = len(st)
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
orders = np.array([len(T) for T in Tlist]); maxorder = int(orders.max())
VAR = ("SA", "S", "P3")
pairm = dict(SA=Zs["p_SA"], S=Zs["p_S"], P3=Z["PBp"]); selfv = dict(SA=Zs["s_SA"], S=Zs["s_S"], P3=Z["PBs"])
chg = (st != np.array(x0)[None, :])
inS = {m: np.stack([chg[:, list(Tlist[ti])].all(axis=1) for ti in np.flatnonzero(orders == m)], axis=1).astype(float) for m in range(3, maxorder + 1) if (orders == m).any()}
sel = {m: np.flatnonzero(orders == m) for m in inS}
log(f"=== p8_03b_statecheck: {seq} on {bb}, tau {tau}: atoms {N}, {S} states, anchor {x0}; orders {sorted(inS)}; variants {VAR}" + ("; RESUMING" if resume else ""))
B = 1.0 / G.invB(G.descreening(st))
if resume:
    z = np.load(ckpt, allow_pickle=True); p_next = int(z["p_next"]); stat = z["stat"].item()
    log(f"    checkpoint read: rows 0..{p_next - 1} done")
else:
    p_next = 0
    stat = {v: dict(n=0, viol=0, minratio=float("inf"), worst=0.0) for v in VAR}
tol = 1e-11
tlast = time.time(); stopped = False
for p in range(p_next, N):
    cols = np.arange(p, N)
    M = kernel_row(G, st, p, B, cols)
    M *= pair_coef(G, p, cols)[None, :]
    F = M.reshape(shape + (len(cols),))
    acc = np.zeros_like(F)
    for r in range(0, maxorder):
        for U in itertools.combinations(range(n), r):
            if any(shape[i] < 2 for i in U):
                continue
            idx = tuple(slice(None) if i in U else x0[i] for i in range(n))
            dd = F[idx].copy()
            for a_, i in enumerate(U):
                dd = dd - np.take(dd, [x0[i]], axis=a_)
            acc += dd.reshape([shape[i] if i in U else 1 for i in range(n)] + [len(cols)])
        m = r + 1
        if m in inS:
            R = np.abs(F - acc).reshape(S, len(cols))
            for v in VAR:
                bnd = np.concatenate([selfv[v][sel[m]][:, p][:, None], pairm[v][sel[m]][:, p, p + 1:]], axis=1)      # (nsub, ncols): diagonal = self summand
                env = inS[m] @ bnd
                bad = R > env + tol
                stat[v]["n"] += int(R.size); stat[v]["viol"] += int(bad.sum())
                if bad.any():
                    stat[v]["worst"] = max(stat[v]["worst"], float((R - env)[bad].max()))
                mk = R > 1e-9
                if mk.any():
                    stat[v]["minratio"] = min(stat[v]["minratio"], float((env[mk] / R[mk]).min()))
            del R
    del M, F, acc
    now = time.time()
    if now - tlast > 60 or p == N - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, p_next=p + 1, stat=np.array(stat, dtype=object)); os.replace(tmp, ckpt); tlast = now
        log(f"    row {p + 1}/{N} done, checkpoint written, {now - t0:.0f} s, RSS {rss_mb():.0f} MB")
    if now - t0 > BUDGET and p < N - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at row {p + 1}/{N}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
for v in VAR:
    s_ = stat[v]
    log(f"    variant {v:2s}: {s_['n']} (pair, state, order) checks, {s_['viol']} violations (largest excess {s_['worst']:.2e} kcal/mol); smallest ratio envelope/|remainder| where the remainder exceeds 1e-9: {s_['minratio']:.4f}")
with open(os.path.join(HERE, "out", f"sc_{tag}.json"), "w") as fh:
    json.dump(dict(seq=seq, bb=bb, tau=tau, nstates=S, natoms=N, stat=stat), fh, indent=1)
log.done()
