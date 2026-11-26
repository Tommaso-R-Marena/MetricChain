"""
P8 step 2 -- what an IDEAL certificate of order m would have to pay on the true ensemble.

Any sandwich of the architecture  m_-/+ = [f + I_{m-1} g] -/+ pen  needs  pen(x) >= |g(x) - I_{m-1} g(x)| =: |R_m(x)|
at every state, so by Lemma A17.16 its bracket is at least about  2 beta <|R_m|>  (first order; <.> the true ensemble).
With exact anchored constants in place of chat_T and the envelope form the penalty is sum_{T subset S(x)} c_T^anch,
which is at least  A_m(x) := sum_{T subset S(x), |T| = m} |d_T(x_T)|  (the anchored terms in the anchor context).
Both R_m(x) and A_m(x) are computed EXACTLY at every state of the Gibbs sample (p8_05_gibbs.py; the sample itself is
uncertified): for a state with s changed sites the 2^s corner energies g(x_V, x0_{-V}), V subset S(x), give all anchored
terms d_U(x_U), U subset S(x), by Moebius inversion;  R_m = sum_{|U| >= m} d_U.

usage: python3 -B p8_08_ideal.py SEQ BB TAU [--smax 13]
needs out/gibbs_<tag>.npz.  Writes logs/ideal_<tag>.log, out/ideal_<tag>.json
"""
import sys, os, json, time, itertools
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
SMAX = int(a[a.index("--smax") + 1]) if "--smax" in a else 13
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"ideal_{tag}.log"))
t0 = time.time()
Zg = np.load(os.path.join(HERE, "out", f"gibbs_{tag}.npz"))
X = Zg["X"]; x0 = Zg["anchor"]; chain = Zg["chain"]; nch = int(chain.max()) + 1
G = GBModel(seq, bb, tau=tau)
n = G.ns
assert list(Zg["k"]) == list(G.k)
uniq, inv, cnt = np.unique(X, axis=0, return_inverse=True, return_counts=True)
inv = np.asarray(inv).reshape(-1)
ns_ = (uniq != x0[None, :]).sum(axis=1)
log(f"=== p8_08_ideal: {seq} on {bb}, tau {tau}: {len(X)} Gibbs states, {len(uniq)} distinct; changed sites per state: mean {(X != x0[None]).sum(1).mean():.3f}, max {ns_.max()}; "
    f"corner evaluations needed: {int((2.0 ** ns_).sum())}")
ORD = [3, 4, 5, 6]
R = np.zeros((len(uniq), len(ORD))); A = np.zeros((len(uniq), len(ORD)))
nev = 0; skipped = 0
for u in range(len(uniq)):
    x = uniq[u]
    Sx = [i for i in range(n) if x[i] != x0[i]]
    s = len(Sx)
    if s < 3:
        continue
    if s > SMAX:
        skipped += int(cnt[u]); R[u] = np.nan; A[u] = np.nan
        continue
    corners = np.tile(x0, (2 ** s, 1))
    bits = ((np.arange(2 ** s)[:, None] >> np.arange(s)[None, :]) & 1).astype(bool)
    for c_, i in enumerate(Sx):
        corners[bits[:, c_], i] = x[i]
    g = np.concatenate([G.bulk_energy(corners[s0:s0 + 2048]) for s0 in range(0, len(corners), 2048)])
    nev += len(corners)
    d = g.reshape([2] * s).copy()                      # axis c_ <-> bit (s - 1 - c_) in C order; the transform is symmetric in the axes
    for ax in range(s):                                # Moebius inversion over the subsets: d_U = sum_{V subset U} (-1)^{|U|-|V|} g_V
        d = np.concatenate([np.take(d, [0], axis=ax), np.take(d, [1], axis=ax) - np.take(d, [0], axis=ax)], axis=ax)
    size = np.indices([2] * s).sum(axis=0)             # |U| of every entry
    assert abs(d.sum() - (g.reshape([2] * s)[tuple([1] * s)])) < 1e-8 * max(1.0, abs(g).max())   # g(x) = sum_U d_U (context expansion)
    for mi, m in enumerate(ORD):
        R[u, mi] = d[size >= m].sum()
        A[u, mi] = np.abs(d[size == m]).sum()
    if (u + 1) % 200 == 0:
        log(f"    {u + 1}/{len(uniq)} distinct states, {nev} evaluations, {time.time() - t0:.0f} s")
log(f"    exact remainders at {len(uniq)} distinct states from {nev} evaluations of g, {time.time() - t0:.0f} s; states with more than {SMAX} changed sites skipped: {skipped} of {len(X)}")
Rs = np.abs(R[inv]); As = A[inv]
ok = ~np.isnan(Rs[:, 0])
res = dict(seq=seq, bb=bb, tau=tau, nsamples=int(len(X)), distinct=int(len(uniq)), skipped=int(skipped), evaluations=int(nev), orders={})


def mean_se(v, w):
    cm = np.array([v[(chain == c) & w].mean() for c in range(nch)])
    return float(v[w].mean()), float(cm.std(ddof=1) / np.sqrt(nch))


log("    order m | mean |R_m| (kcal/mol) | max |R_m| in the sample | FLOOR of any order-m certificate, 2 beta <|R_m|> (nats) | exact-term envelope 2 beta <A_m> (nats) | fraction of states with >= m changed sites")
for mi, m in enumerate(ORD):
    mr, ser = mean_se(Rs[:, mi], ok); ma, sea = mean_se(As[:, mi], ok)
    frac = float(((X != x0[None]).sum(1) >= m).mean())
    log(f"      {m} | {mr:.3e} | {np.nanmax(Rs[:, mi]):.3e} | {2 * BETA * mr:.3e} (+- {2 * BETA * ser:.1e}) | {2 * BETA * ma:.3e} (+- {2 * BETA * sea:.1e}) | {frac:.4f}")
    res["orders"][str(m)] = dict(mean_absR=mr, max_absR=float(np.nanmax(Rs[:, mi])), floor_nats=2 * BETA * mr, floor_se=2 * BETA * ser,
                                 envelope_exact_terms_nats=2 * BETA * ma, envelope_se=2 * BETA * sea, frac_ge_m=frac)
with open(os.path.join(HERE, "out", f"ideal_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
