"""Analysis 3b (decisive version): the pair-distance-profile class on OFF-GRID conformations,
with transfer across chain length.  Fit on the continuous ensemble C of one chain length
(train half), test on the held-out half, on other chain lengths (intercept refitted: one
parameter), and on the torsion grids.
usage: python3 an5_profile_transfer.py <n_train> [--lp]"""
import sys, os, json, math, time
import numpy as np
from analysis_lib import *
from pepbuild import Peptide
from enumerate_grid import grid_angles

ntr = int(sys.argv[1]); do_lp = "--lp" in sys.argv
KNOTS = np.concatenate([np.arange(1.5, 6.0, 0.25), np.arange(6.0, 12.0, 0.5), np.arange(12.0, 40.1, 2.0)])
RES = ["GB", "coul", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "OBC2-GBn2", "lj"]
peps = {}

def pep(n):
    if n not in peps:
        peps[n] = Peptide(n, extra_ffs=(), solvent=False, platform="Reference")
    return peps[n]

def cont(n):
    d = dict(np.load(os.path.join(HERE, "data", f"cont_n{n}.npz")))
    f = d["tors"] + d["lj"] + d["coul"]
    y = {"GB": d["gbn2"], "coul": d["coul"], "coul+GB": d["coul"] + d["gbn2"], "lj": d["lj"],
         "ff03-ff14SB": d["ff03_tors"] + d["ff03_lj"] + d["ff03_coul"] - f,
         "ff15ipq-ff14SB": d["ff15ipq_tors"] + d["ff15ipq_lj"] + d["ff15ipq_coul"] - f,
         "OBC2-GBn2": d["obc2"] - d["gbn2"]}
    return d["phi"], d["psi"], y

def grid(alphabet, n, maxm=6000):
    d = load(alphabet, n); R = residuals(d)
    mask = d["clash"] > 0.7
    flat = np.flatnonzero(mask.reshape(-1))
    rng = np.random.default_rng(5)
    if len(flat) > maxm:
        flat = np.sort(rng.choice(flat, maxm, replace=False))
    phi, psi, _ = grid_angles(n, alphabet, flat.astype(np.int64))
    y = {k: R[k].reshape(-1)[flat] for k in RES if k in R}
    y["lj"] = d["lj"].reshape(-1)[flat]
    return phi, psi, y

def feats(n, phi, psi, scheme):
    P = pep(n)
    F, meta = profile_features(P, P.coords(phi, psi), scheme, KNOTS)
    return F, meta

phi, psi, ytr_all = cont(ntr)
M = len(phi); half = M // 2
tests = {}
for n2 in (3, 4, 5, 6, 8):
    if os.path.exists(os.path.join(HERE, "data", f"cont_n{n2}.npz")) and n2 != ntr:
        tests[f"C n={n2}"] = (n2,) + cont(n2)
for alphabet, n2 in (("A3", 4), ("A3", 5), ("A2", 8)):
    if os.path.exists(os.path.join(HERE, "data", f"grid_{alphabet}_n{n2}.npz")):
        tests[f"{alphabet} n={n2}"] = (n2,) + grid(alphabet, n2)
res_path = os.path.join(HERE, "out", "an5_profile_transfer.json")
results = json.load(open(res_path)) if os.path.exists(res_path) else {}
print(f"=== profile class fitted on ensemble C, n={ntr}: {half} training conformations; knots: {len(KNOTS)-1} bins up to {KNOTS[-1]} A; kT={KT300:.4f} kcal/mol")
for scheme in ("one", "elem", "amber"):
    F, meta = feats(ntr, phi, psi, scheme)
    nz = F[:half].std(axis=0) > 1e-9
    A = np.hstack([np.ones((M, 1)), F[:, nz]])
    Ft = {}
    for key, (n2, p2, s2, y2) in tests.items():
        F2, meta2 = feats(n2, p2, s2, scheme)
        assert meta2["types"] == meta["types"], (meta2["types"], meta["types"])
        Ft[key] = F2[:, nz]
    rmid = np.tile(0.5 * (KNOTS[:-1] + KNOTS[1:]), len(meta["types"]))[nz]
    print(f"--- typing '{scheme}': {len(meta['types'])} pair types, {A.shape[1]} parameters")
    for name in RES:
        y = ytr_all[name]
        G = A[:half].T @ A[:half]; G[np.diag_indices_from(G)] += 1e-9 * np.trace(G) / len(G)
        th = np.linalg.solve(G, A[:half].T @ y[:half])
        rtr = y[:half] - A[:half] @ th; rte = y[half:] - A[half:] @ th
        L_s = float(np.abs(th[1:]).max()); L_r = float((2 * rmid * np.abs(th[1:])).max())
        line = (f"{name:15s} std {y.std():6.2f} | train RMS {np.sqrt((rtr**2).mean()):6.3f} max {np.abs(rtr).max():6.2f} | "
                f"held-out RMS {np.sqrt((rte**2).mean()):6.3f} max {np.abs(rte).max():6.2f} | L_s {L_s:6.3f} L_r {L_r:6.2f} |")
        rec = dict(std=float(y.std()), train_rms=float(np.sqrt((rtr**2).mean())), train_max=float(np.abs(rtr).max()),
                   test_rms=float(np.sqrt((rte**2).mean())), test_max=float(np.abs(rte).max()), L_s=L_s, L_r=L_r,
                   npar=int(A.shape[1]), transfer={})
        for key, (n2, p2, s2, y2) in tests.items():
            if name not in y2:
                continue
            pred = Ft[key] @ th[1:]
            r2 = y2[name] - pred
            r2 = r2 - r2.mean()            # intercept refitted (one parameter)
            rec["transfer"][key] = (float(np.sqrt((r2 ** 2).mean())), float(np.abs(r2).max()), float(y2[name].std()))
            line += f" {key}: {np.sqrt((r2**2).mean()):.2f}/{np.abs(r2).max():.2f}"
        print(line, flush=True)
        results[f"{ntr}|{scheme}|{name}"] = rec
        if do_lp and name in ("GB", "coul+GB") and scheme in ("elem", "amber"):
            import scipy.sparse as sp
            sub = np.arange(min(half, 2500))
            for L in (None, 1.0, 0.3, 0.1, 0.03):
                bound = None if L is None else np.concatenate([[np.inf], np.full(A.shape[1] - 1, L)])
                t0 = time.time()
                eta, thl = fit_sup(sp.csr_matrix(A[sub]), y[sub], bound=bound, time_limit=400)
                if thl is None:
                    print(f"      LP L={L}: no solution in time"); continue
                rt = np.abs(y[half:] - A[half:] @ thl)
                rec.setdefault("eta", {})[str(L)] = (eta, float(rt.max()), float(np.sqrt((rt ** 2).mean())))
                print(f"      sup-norm LP ({len(sub)} training conf.), slope bound L_s={L}: eta_train = {eta:.3f} kcal/mol; held-out max {rt.max():.2f}, RMS {np.sqrt((rt**2).mean()):.3f}  [{time.time()-t0:.0f}s]", flush=True)
json.dump(results, open(res_path, "w"), indent=0)
