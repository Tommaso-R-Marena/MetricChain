"""T2 — chimera search on generically globally rigid graphs in the plane (own code).

For random ("generic") ensembles of K conformers (i.i.d. standard normal coordinates) and every
non-constant colouring a of the edges by the conformers (all of them when K^m <= 2e6, otherwise a
random sample), look for a framework whose squared edge lengths are the splice q^a, by two
independent methods:
  LM     batched Levenberg-Marquardt on || sqlen(p) - q^a ||_2 from `starts` random starts
         (the method prescribed by the brief; a local search, so it can miss);
  EXACT  ruler-and-compass enumeration of all realisations of a spanning subgraph and comparison
         of the remaining edges (exhaustive; defect = 0 iff realisable).
Theorems E5(a)/E7 predict: no zero for generic ensembles.

Controls (each reported with its violations):
  C-const   the conformers themselves (constant colourings) must be found by both methods;
  C-plant   200 targets that ARE realisable (lengths of fresh random frameworks) must be found:
            measures the power of the search (LM: also the per-start success rate).
usage: python3 -B t2_chimera_search.py <graph> <K> <n_ens> <starts> [max_colourings] [seed] [lm_cap]
"""
import sys
import numpy as np
from r21_common import *

name = sys.argv[1]
K = int(sys.argv[2])
n_ens = int(sys.argv[3])
starts = int(sys.argv[4])
max_col = int(sys.argv[5]) if len(sys.argv) > 5 else 0
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 2102
lm_cap = int(sys.argv[7]) if len(sys.argv) > 7 else 0      # LM only on the lm_cap colourings with the smallest exact defect + lm_cap random ones
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
m = len(E)
R = Realiser(N, E)
C = Constructor(name, N, E)
print(f"T2 chimera search  graph={name} N={N} m={m} K={K} ensembles={n_ens} LM starts={starts} seed={seed}  start {now()}")
print(f"   thresholds: LM residual < 1e-6 or exact defect < 1e-9 counts as a chimera found")

tot_found = 0
tot_viol = 0
tot_col = 0
g_lm, g_ex = [], []
for ens in range(n_ens):
    X = rng.standard_normal((K, N, 2))
    Tc = sqlen(X, E)                                        # (K, m)
    iu = np.triu_indices(K, 1)
    mingap_len = np.min(np.abs(Tc[:, None, :] - Tc[None, :, :])[iu]) if K > 1 else np.nan
    if K ** m <= 2_000_000 and (max_col == 0 or K ** m <= max_col):
        col = all_colourings(K, m)
        mode = "all"
    else:
        ncol = max_col if max_col else 50000
        col = rng.integers(0, K, size=(ncol, m)).astype(np.int8)
        mode = "random sample"
    col = col[nonconstant(col)]
    T = splice_targets(Tc, col)
    tot_col += len(col)
    # EXACT
    ex, _ = C.defect(T)
    exc, _ = C.defect(Tc)
    Y = rng.standard_normal((200, N, 2))
    Tp = sqlen(Y, E)
    exp_, _ = C.defect(Tp)
    n_ex = int(np.sum(ex < 1e-9))
    v_ex = int(np.sum(exc >= 1e-9)) + int(np.sum(exp_ >= 1e-9))
    # LM
    if lm_cap and len(col) > 2 * lm_cap:
        sel = np.unique(np.concatenate([np.argsort(ex)[:lm_cap], rng.choice(len(col), lm_cap, replace=False)]))
        lm_note = f"LM on {len(sel)} colourings (the {lm_cap} smallest exact defects + {lm_cap} random)"
    else:
        sel = np.arange(len(col))
        lm_note = "LM on all colourings examined"
    best, bestZ, hits = R.multistart(T[sel], starts, rng)
    bc, _, hc = R.multistart(Tc, starts, rng)
    bp, _, hp = R.multistart(Tp, starts, rng)
    n_lm = int(np.sum(best < 1e-6))
    v_lm = int(np.sum(bc >= 1e-9)) + int(np.sum(bp >= 1e-9))
    i_ex = int(np.argmin(ex))
    i_lm = int(sel[np.argmin(best)])
    g_lm.append(best.min())
    g_ex.append(ex[np.isfinite(ex)].min() if np.isfinite(ex).any() else np.inf)
    print(f"ens {ens}: {len(col)} non-constant colourings ({mode}); min over pairs/edges |len_i - len_j| = {mingap_len:.3f}")
    print(f"    EXACT: min defect = {ex.min():.3e}; infeasible (no realisation of the spanning subgraph) "
          f"{int(np.sum(~np.isfinite(ex)))}; found (<1e-9): {n_ex}.   C-const max {exc.max():.1e}, C-plant max {exp_.max():.1e}; "
          f"control violations {v_ex}/{K + 200}")
    print(f"    LM   : {lm_note}; min residual = {best.min():.3e}, q01 = {np.quantile(best, 0.01):.3e}, "
          f"median = {np.median(best):.3e}; found (<1e-6): {n_lm}")
    print(f"           C-const max {bc.max():.1e} (violations {int(np.sum(bc >= 1e-9))}/{K}); C-plant: violations "
          f"{int(np.sum(bp >= 1e-9))}/200, per-start success {hp.sum() / (200 * starts):.3f}, least successful target {hp.min()}/{starts}")
    print(f"    agreement: LM residual at the EXACT minimiser = "
          f"{(best[np.searchsorted(sel, i_ex)] if i_ex in sel else np.nan):.3e}; exact defect at the LM minimiser = {ex[i_lm]:.3e}")
    tot_found += n_ex + n_lm
    tot_viol += v_ex + v_lm
print(f"SUMMARY graph={name} K={K}: ensembles={n_ens}; non-constant colourings examined={tot_col}; chimeras found={tot_found}; "
      f"control violations={tot_viol}; smallest LM residual={min(g_lm):.3e} (median over ensembles {np.median(g_lm):.3e}); "
      f"smallest exact defect={min(g_ex):.3e} (median over ensembles {np.median(g_ex):.3e})")
print("DONE t2_chimera_search", name, K, now())
