"""
Certificates of the minimum in the FIRST-ORDER (per-site) format on an enumerated instance --
the same computation as ws_P/an7_sharpness.py (covering problem of theory report Thm 11.4;
lower bounds: forced points, volume bound, partition bound (Thm 11.6); upper bound: greedy
cover), generalised to sites with different numbers of states.

usage: python3 -B an_cover.py TAG TAU RESIDUAL [X|Xtau]

Instance: domain X (product) or X_tau (pair-clash-free), known part f = ff14SB vacuum energy,
residual g, E = f + g, envelope d(x,y) = sum_i c_i [x_i != y_i] with the exact constants of the
domain (rescaled by kappa_max if on a non-product domain single flips do not dominate).
An anchor a covers y iff  d(a,y) - g(a) + g(y) <= E(y) - min E + eps.
Output: out/cover_<tag>_tau<TAU>_<residual>_<domain>.json
"""
import sys, os, json, math, time
import numpy as np
import scipy.sparse as sp
from anlib import *

tag, tau, rname = sys.argv[1], float(sys.argv[2]), sys.argv[3]
dname = sys.argv[4] if len(sys.argv) > 4 else "Xtau"
d0 = load_fb(tag)
d = restrict(d0, tau) if tau > d0["tau_enum"] + 1e-12 else d0
shape = d["shape"]; n = len(shape)
R = residuals(d)
mask = (d["s2min"] > tau) if dname == "Xtau" else np.ones(shape, dtype=bool)
st = np.argwhere(mask)
M = len(st)
f = R["f"][mask]; g = R[rname][mask]; E = f + g
c, rms, _ = first_order(R[rname], mask)
out = dict(tag=tag, tau=tau, residual=rname, domain=dname, M=int(M), c=c.tolist(), shape=list(shape))
print(f"=== {tag} tau={tau} residual {rname} on {dname}: {M} assignments, states/site {list(shape)}")
print(f"c_i = {np.round(c, 3)} kcal/mol")
off = np.concatenate([[0], np.cumsum(shape)])
H = np.zeros((M, off[-1]), dtype=np.float32)
H[np.arange(M)[:, None], off[:-1][None, :] + st] = 1.0
cw = np.repeat(c, shape).astype(np.float64)
Hc = (H * cw[None, :]).astype(np.float64)
H64 = H.astype(np.float64)
csum = c.sum()


def dist_rows(rows):
    return csum - Hc[rows] @ H64.T


if M > 45000:
    print("domain too large for the O(M^2) cover computation")
    sys.exit(0)
kap = 0.0
for s0 in range(0, M, 512):
    rows = np.arange(s0, min(M, s0 + 512))
    D = dist_rows(rows)
    num = np.abs(g[rows][:, None] - g[None, :])
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(D > 1e-12, num / D, 0.0)
    kap = max(kap, float(ratio.max()))
scale = max(1.0, kap)
print(f"validity of the weighted-Hamming envelope on the domain: max |g(x)-g(y)|/d(x,y) = {kap:.4f}"
      + ("" if kap <= 1 + 1e-9 else "  -> constants rescaled by this factor"))
out["kappa_max"] = kap
gap = E - E.min()


def slack_rows(rows):
    return dist_rows(rows) * scale - g[rows][:, None] + g[None, :]


for eps in (0.0, KT300, 2.0):
    t0 = time.time()
    ncover_of_y = np.zeros(M); size_of_a = np.zeros(M)
    for s0 in range(0, M, 512):
        rows = np.arange(s0, min(M, s0 + 512))
        cov = slack_rows(rows) <= gap[None, :] + eps + 1e-9
        ncover_of_y += cov.sum(axis=0); size_of_a[rows] = cov.sum(axis=1)
    forced = ncover_of_y == 1
    sparse_case = size_of_a.sum() < 3e7
    vol = float("nan"); best_pf = float("nan")
    if sparse_case:
        rows_l, cols_l = [], []
        for s0 in range(0, M, 512):
            rows = np.arange(s0, min(M, s0 + 512))
            r_, c_ = np.nonzero(slack_rows(rows) <= gap[None, :] + eps + 1e-9)
            rows_l.append(rows[r_]); cols_l.append(c_)
        rr = np.concatenate(rows_l); cc_ = np.concatenate(cols_l)
        Cm = sp.csr_matrix((np.ones(len(rr), dtype=np.float32), (rr, cc_)), shape=(M, M))
        Ccsc = Cm.tocsc()
        My = np.array([size_of_a[Ccsc.indices[Ccsc.indptr[y]:Ccsc.indptr[y + 1]]].max() for y in range(M)])
        vol = float((1.0 / My).sum())
        best_pf = 0.0
        for t in (0.1, 0.4, 1.6):
            numer = np.exp(-t * gap).sum(); den = 0.0
            for s0 in range(0, M, 512):
                rows = np.arange(s0, min(M, s0 + 512))
                den = max(den, float(np.exp(-t * slack_rows(rows)).sum(axis=1).max()))
            best_pf = max(best_pf, math.exp(-t * eps) * numer / den)
        chosen = np.flatnonzero(forced).tolist()
        covered = np.zeros(M, dtype=bool)
        if chosen:
            covered |= np.asarray(Cm[chosen].sum(axis=0)).ravel() > 0
        while not covered.all():
            gain = Cm @ (~covered).astype(np.float32)
            a_ = int(np.argmax(gain)); chosen.append(a_)
            covered[Cm.indices[Cm.indptr[a_]:Cm.indptr[a_ + 1]]] = True
    else:
        cand = np.unique(np.concatenate([np.flatnonzero(forced), np.argsort(-size_of_a)[:1500]]))
        Cd = np.zeros((len(cand), M), dtype=bool)
        for s0 in range(0, len(cand), 512):
            rows = cand[s0:s0 + 512]
            Cd[s0:s0 + 512] = slack_rows(rows) <= gap[None, :] + eps + 1e-9
        fidx = np.flatnonzero(np.isin(cand, np.flatnonzero(forced)))
        chosen = cand[fidx].tolist()
        covered = Cd[fidx].any(axis=0) if len(fidx) else np.zeros(M, dtype=bool)
        while not covered.all():
            gain = (Cd & ~covered[None, :]).sum(axis=1)
            a_ = int(np.argmax(gain))
            if gain[a_] == 0:
                chosen += np.flatnonzero(~covered).tolist(); break
            chosen.append(int(cand[a_])); covered |= Cd[a_]
    lbs = [int(forced.sum()), 1]
    if vol == vol: lbs.append(math.ceil(vol - 1e-9))
    if best_pf == best_pf: lbs.append(math.ceil(best_pf - 1e-9))
    lb = max(lbs)
    if lb == 1 and len(chosen) > 1 and size_of_a.max() < M:
        lb = 2
    print(f"cover at eps = {eps:.3f} kcal/mol: forced points {int(forced.sum())}, volume bound {vol:.1f}, partition bound {best_pf:.1f} "
          f"=> N_cov >= {lb};  greedy cover {len(chosen)}  (of M = {M}; mean set size {size_of_a.mean():.1f}, max {int(size_of_a.max())}; "
          f"{'sparse' if sparse_case else 'dense'} path)  [{time.time() - t0:.0f}s]", flush=True)
    out[f"cover_eps{eps:.3f}"] = dict(forced=int(forced.sum()), volume=vol, partition=best_pf, lower=lb, greedy=len(chosen))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "out", f"cover_{tag}_tau{tau:.2f}_{rname}_{dname}.json"), "w"), indent=0)
