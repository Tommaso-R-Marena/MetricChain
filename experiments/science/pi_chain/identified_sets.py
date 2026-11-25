"""Identified sets on the diamond-lattice chain (science division, PI thread).

Question.  An ensemble mu on the self-avoiding conformations of a chain with n torsions is
unknown.  Exact ensemble-averaged data E_mu[Phi] = m are given for a feature vector Phi.
What is the exact range of E_mu[psi] for another observable psi over ALL ensembles
consistent with the data (the model-free identified set)?  This is the linear programme
    max / min  sum_x mu(x) psi(x)   s.t.  sum_x mu(x) Phi(x) = m,  mu a probability vector,
solved exactly here after aggregating conformations with equal Phi.

Data types:  D1 = Rg^2 (one number: Guinier-level scattering),
             D2 = pair counts in the three shortest non-bonded shells (the programme's profile, S_c = 12),
             D3 = the full pair-distance histogram (idealised complete scattering curve).
Targets:     gauche fraction, end-to-end R^2, one internal pair distance^2 (a single-pair, FRET-like
             observable), the weight of the all-trans conformation, the population of the most
             compact decile (by Rg^2 in the athermal ensemble).
Truths:      athermal, stiff (weight exp(-gauche)), attractive (weight exp(+c3)).
"""
from __future__ import annotations
import sys, os, json, time
import numpy as np
from scipy.optimize import linprog
from dia_chain import enumerate_chain, short_profile

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(CACHE, exist_ok=True)

def get(n):
    f = os.path.join(CACHE, f"dia_n{n}.npz")
    N = n + 3
    pair = (N // 4, (3 * N) // 4)
    if os.path.exists(f):
        z = np.load(f)
        return {k: z[k] for k in z.files}, pair
    d = enumerate_chain(n, track_pairs=[pair])
    np.savez_compressed(f, **{k: v for k, v in d.items() if isinstance(v, np.ndarray)},
                        n_torsions=n, N=N)
    return d, pair

def identified_interval(Phi, psi, m):
    """exact [min, max] of E psi over probability vectors with E Phi = m (aggregated by Phi)."""
    uniq, inv = np.unique(Phi, axis=0, return_inverse=True)
    inv = inv.ravel()
    K = len(uniq)
    hi = np.full(K, -np.inf); lo = np.full(K, np.inf)
    np.maximum.at(hi, inv, psi); np.minimum.at(lo, inv, psi)
    # remove redundant feature columns for numerical health
    A = np.vstack([uniq.T.astype(float), np.ones(K)])
    b = np.concatenate([np.asarray(m, float), [1.0]])
    scale = np.maximum(np.abs(A).max(axis=1), 1.0)
    A = A / scale[:, None]; b = b / scale
    out = []
    for c in (lo, -hi):
        res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        if res.status != 0:
            return None, K
        out.append(res.fun)
    return (out[0], -out[1]), K

def analyse(n, verbose=True):
    d, pair = get(n)
    N = n + 3
    g = d["gauche"].astype(float); rg2 = d["rg2"].astype(float) / N**2
    ree2 = d["ree2"].astype(float); pd2 = d["pairs"][:, 0].astype(float)
    prof = short_profile(d).astype(float)
    full = d["hist"].astype(float)
    M = len(g)
    alltrans = (g == 0).astype(float)
    thr = np.quantile(rg2, 0.10)
    compact = (rg2 <= thr).astype(float)
    targets = {"gauche fraction": g / n, "end-to-end R2": ree2, f"pair({pair[0]},{pair[1]}) d2": pd2,
               "P(all-trans)": alltrans, "P(compact decile)": compact}
    datas = {"D1 Rg2": rg2[:, None], "D2 three-shell profile": prof, "D3 full distance histogram": full}
    truths = {"athermal": np.ones(M), "stiff": np.exp(-g), "attractive": np.exp(prof[:, 0])}
    rows = []
    for tname, w in truths.items():
        p = w / w.sum()
        for dname, Phi in datas.items():
            m = p @ Phi
            for sname, psi in targets.items():
                t0 = time.time()
                iv, K = identified_interval(Phi, psi, m)
                truth = float(p @ psi); a0, a1 = float(psi.min()), float(psi.max())
                if iv is None:
                    rows.append(dict(n=n, truth=tname, data=dname, target=sname, status="lp failed")); continue
                lo, hi = iv
                rows.append(dict(n=n, N=N, conformations=M, truth=tname, data=dname, target=sname,
                                 distinct_feature_vectors=K, truth_value=truth, lo=lo, hi=hi,
                                 apriori_lo=a0, apriori_hi=a1,
                                 unidentified_fraction=(hi - lo) / (a1 - a0) if a1 > a0 else 0.0,
                                 seconds=round(time.time() - t0, 2)))
                if verbose:
                    r = rows[-1]
                    print(f"n={n:2d} {tname:10s} | {dname:26s} | {sname:20s} truth {truth:10.4f}  "
                          f"identified [{lo:10.4f}, {hi:10.4f}]  a priori [{a0:8.3f}, {a1:8.3f}]  "
                          f"unidentified fraction {r['unidentified_fraction']:.3f}  (K={K})", flush=True)
    return rows

if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1:]] or [6, 8, 10]
    allrows = []
    for n in ns:
        allrows += analyse(n)
        json.dump(allrows, open(os.path.join(CACHE, "..", f"identified_sets_n{'_'.join(map(str, ns))}.json"), "w"), indent=1)
