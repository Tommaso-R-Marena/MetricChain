"""Analysis 3b: best approximation of each residual in the pair-distance-profile class of
theory report 11.17 (pair-additive, radial functions piecewise linear in s = r^2 with bounded
slope L, zero beyond the cutoff), for several typings.  Clash-free domain.
usage: python3 an4_profile.py alphabet n [--lp] [--names a,b] [--max M]"""
import sys, os, json, time, math
import numpy as np
from analysis_lib import *
from pepbuild import Peptide
from enumerate_grid import grid_angles

alphabet, n = sys.argv[1], int(sys.argv[2])
do_lp = "--lp" in sys.argv
names = ["GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "OBC2-GBn2", "coul"]
if "--names" in sys.argv:
    names = sys.argv[sys.argv.index("--names") + 1].split(",")
MAXM = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 30000
TAU = 0.7
d = load(alphabet, n); R = residuals(d); m = d["m"]; k = d["k"]
mask = d["clash"] > TAU
flat = np.flatnonzero(mask.reshape(-1))
rng = np.random.default_rng(11)
if len(flat) > MAXM:
    flat = np.sort(rng.choice(flat, MAXM, replace=False))
M = len(flat)
P = Peptide(n, extra_ffs=(), solvent=False, platform="Reference")
phi, psi, st = grid_angles(n, alphabet, flat.astype(np.int64))
X = P.coords(phi, psi)
rmax = 0.0
iu = np.triu_indices(P.natoms, 1)
for s0 in range(0, M, 4096):
    x = X[s0:s0 + 4096]
    rmax = max(rmax, float(np.sqrt(((x[:, iu[0]] - x[:, iu[1]]) ** 2).sum(2)).max()))
perm = rng.permutation(M); half = M // 2
tr, te = perm[:half], perm[half:]
res_path = os.path.join(HERE, "out", "an4_profile.json")
results = json.load(open(res_path)) if os.path.exists(res_path) else {}
print(f"=== {alphabet} n={n}: {M} clash-free conformations used (of {int(mask.sum())}); max interatomic distance {rmax:.1f} A; kT={KT300:.4f}")
print(f"{'residual':15s} {'types':7s} {'rc':>5s} {'dr':>4s} {'npar':>5s} {'std':>6s} {'RMS':>6s} {'maxLS':>6s} {'teRMS':>6s} {'teMax':>6s} {'L_s':>8s} {'L_r':>7s} | eta_sup(L=inf) and eta*(L) [kcal/mol]")
configs = [("one", None, 0.5), ("heavy", None, 0.5), ("charge", None, 0.5), ("elem", None, 0.5), ("amber", None, 0.5),
           ("amber", 8.0, 0.5), ("amber", 12.0, 0.5), ("elem", None, 0.25), ("amber", None, 1.0)]
feats = {}
for scheme, rc, dr in configs:
    rc_eff = rc if rc is not None else math.ceil(rmax + 0.5)
    knots = np.arange(1.5, rc_eff + 1e-9, dr)
    F, meta = profile_features(P, X, scheme, knots)
    feats[(scheme, rc, dr)] = (F, meta)
for name in names:
    if name not in R:
        continue
    y = R[name].reshape(-1)[flat]
    for (scheme, rc, dr), (F, meta) in feats.items():
        nz = F.std(axis=0) > 1e-9
        A = np.hstack([np.ones((M, 1)), F[:, nz]])
        npar = A.shape[1]
        # least squares (tiny ridge for the null directions)
        def ls(Am, ym):
            G = Am.T @ Am; G[np.diag_indices_from(G)] += 1e-8 * np.trace(G) / len(G)
            return np.linalg.solve(G, Am.T @ ym)
        th = ls(A, y); r = y - A @ th
        thtr = ls(A[tr], y[tr]); rte = y[te] - A[te] @ thtr
        # Lipschitz constants of the fitted radial functions: slopes are -theta (kcal/mol/A^2)
        wid = np.tile(meta["width_s"], len(meta["types"]))[nz]
        rmid = np.tile(0.5 * (meta["knots_r"][:-1] + meta["knots_r"][1:]), len(meta["types"]))[nz]
        L_s = float(np.abs(th[1:]).max()); L_r = float((2 * rmid * np.abs(th[1:])).max())
        line = f"{name:15s} {scheme:7s} {str(rc):>5s} {dr:4.2f} {npar:5d} {y.std():6.2f} {np.sqrt((r**2).mean()):6.3f} {np.abs(r).max():6.2f} {np.sqrt((rte**2).mean()):6.3f} {np.abs(rte).max():6.2f} {L_s:8.3f} {L_r:7.2f} |"
        rec = dict(npar=int(npar), M=int(M), std=float(y.std()), rms=float(np.sqrt((r**2).mean())), max_ls=float(np.abs(r).max()),
                   test_rms=float(np.sqrt((rte**2).mean())), test_max=float(np.abs(rte).max()), L_s=L_s, L_r=L_r, ntypes=len(meta["types"]),
                   eta=dict())
        if do_lp and (scheme, rc, dr) in (("one", None, 0.5), ("elem", None, 0.5), ("amber", None, 0.5), ("amber", 8.0, 0.5)) \
                and name in ("GB", "coul+GB", "ff03-ff14SB"):
            sub = tr[:min(len(tr), 2500)]
            import scipy.sparse as sp
            for L in (None, 3.0, 1.0, 0.3, 0.1, 0.03):
                bound = None if L is None else np.concatenate([[np.inf], np.full(npar - 1, L)])
                eta, thl = fit_sup(sp.csr_matrix(A[sub]), y[sub], bound=bound, time_limit=300)
                if thl is None:
                    continue
                rt = np.abs(y[te] - A[te] @ thl)
                rec["eta"][str(L)] = (eta, float(rt.max()), float(np.sqrt((rt ** 2).mean())))
                line += f" L={L}: {eta:.2f} (test max {rt.max():.2f}, rms {np.sqrt((rt**2).mean()):.2f});"
        print(line, flush=True)
        results[f"{alphabet}|{n}|{name}|{scheme}|{rc}|{dr}"] = rec
json.dump(results, open(res_path, "w"), indent=0)
