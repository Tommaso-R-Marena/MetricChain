"""T5 — how close do generic ensembles come to having a chimera?  (own code)

chimera gap     g1 = min over non-constant colourings a of  dist_2( q^a , image of the squared-length map )
switching gap   g2 = min over a of max( dist(q^a), dist(q^abar) )          (K = 2; abar = complementary colouring)
Both in units in which conformer coordinates are standard normal (mean squared length of an edge = 4).
dist is computed by LM multistart (an upper bound of the true distance: every value reported is realised
by an explicit framework); candidates are pre-selected by the exact defect when there are too many.
If every edge-length law is known only up to a band tau (sup norm on squared lengths), a splice with
dist_inf <= tau is a framework that the data cannot tell from "lengths borrowed from different conformers";
dist_inf <= dist_2 <= sqrt(m) dist_inf.
usage: python3 -B t5_gap_scaling.py <graph> <K> <n_ens> <starts> [seed]
"""
import sys
import numpy as np
from r21_common import *

name = sys.argv[1]
K = int(sys.argv[2])
n_ens = int(sys.argv[3])
starts = int(sys.argv[4])
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 2105
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
m = len(E)
codim = m - (2 * N - 3)
R = Realiser(N, E)
C = Constructor(name, N, E)
CAP = 1000
print(f"T5 gap  graph={name} N={N} m={m} codim of the measurement variety={codim} K={K} ensembles={n_ens} LM starts={starts} seed={seed} start {now()}")
total = K ** m - K
g1s, g2s, exs, rel = [], [], [], []
for ens in range(n_ens):
    X = rng.standard_normal((K, N, 2))
    Tc = sqlen(X, E)
    if K ** m <= 2_000_000:
        col = all_colourings(K, m)
        mode = "all"
    else:
        col = rng.integers(0, K, size=(2_000_000, m)).astype(np.int8)
        mode = "sample"
    col = col[nonconstant(col)]
    T = splice_targets(Tc, col)
    ex, _ = C.defect(T)
    if len(col) > 2 * CAP:
        sel = np.unique(np.concatenate([np.argsort(ex)[:CAP], rng.choice(len(col), CAP, replace=False)]))
    else:
        sel = np.arange(len(col))
    best, bestZ, _ = R.multistart(T[sel], starts, rng)
    i = int(np.argmin(best))
    g1 = best[i]
    # verify: the framework found has squared lengths within g1 (2-norm) of the splice
    Pb = embed(bestZ[i:i + 1], N)
    chk = np.linalg.norm(sqlen(Pb, E)[0] - T[sel][i])
    dinf = np.max(np.abs(sqlen(Pb, E)[0] - T[sel][i]))
    g1s.append(g1)
    exs.append(ex.min())
    rel.append(dinf / np.mean(Tc))
    line = f"ens {ens}: {len(col)} colourings ({mode}); g1 = {g1:.3e} (re-checked {chk:.3e}; sup-norm {dinf:.3e}; relative to mean sq. length {dinf/np.mean(Tc):.2e}); min exact defect {ex.min():.3e}"
    if K == 2 and len(sel) == len(col):
        comp = 1 - col
        key = {tuple(c): q for q, c in enumerate(col)}
        idx = np.array([key[tuple(c)] for c in comp])
        g2 = np.min(np.maximum(best, best[idx]))
        g2s.append(g2)
        line += f"; switching gap g2 = {g2:.3e}"
    print(line)
g1s = np.array(g1s)
print(f"SUMMARY graph={name} m={m} codim={codim} K={K} splices={total}: g1 median {np.median(g1s):.3e}, min {g1s.min():.3e}, max {g1s.max():.3e}; "
      f"sup-norm gap relative to the mean squared length: median {np.median(rel):.2e}, min {np.min(rel):.2e}"
      + (f"; g2 median {np.median(g2s):.3e}, min {np.min(g2s):.3e}" if g2s else "")
      + f"; heuristic splices^(-1/codim) = {total ** (-1.0 / codim):.3e}")
print("DONE t5_gap_scaling", name, K, now())
