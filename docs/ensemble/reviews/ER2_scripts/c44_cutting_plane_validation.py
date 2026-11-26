#!/usr/bin/env python3
"""ER2: does experiments/ensemble/capacity_cutting_plane.py decide what it says?  (section 4.4)

The report's validation of the cutting-plane script against the full linear programme is a comparison of
two FREQUENCIES on different random instances (0.733 on 60 instances against 0.677 on 300).  Here the
decision of the repository function `is_face` (imported read-only, python -B) is compared INSTANCE BY
INSTANCE with two independent decisions of my own, in float64 over all 2^(n-1) states:

  primal  max t :  Q.phi(x) = c on S,  Q.phi(y) >= c + t off S,  |Q_ij| <= 1      (face  <=> t* > 0)
  dual    max sum_{y not in S} h(y) :  h orthogonal to span{1, phi},  h >= 0 off S,  sum_{off S} h <= 1
                                                                          (not a face <=> value 1; E1(a))

Exactly one of the two must certify.  Also recorded: the smallest positive margin t* of a face (against the
tolerances 1e-7 / 1e-5 of the script), LP solves of the script that end with status != 0 (the script counts
them as "not a face"), and the error of the script's float32 energies.

Usage: python3 c44_cutting_plane_validation.py n trials K [K ...]
"""
import sys, time, importlib.util
import numpy as np
import sys as _sys; _sys.dont_write_bytecode = True      # nothing is written next to the repository scripts
from er2_common import repo_root
REPO = repo_root()
from scipy.optimize import linprog

spec = importlib.util.spec_from_file_location("ccp", REPO + "/experiments/ensemble/capacity_cutting_plane.py")
ccp = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccp)

status_log = []
_orig = ccp.linprog


def _wrapped(*a, **k):
    res = _orig(*a, **k)
    status_log.append(res.status)
    return res


ccp.linprog = _wrapped


def my_decision(X, Yall):
    K, n = X.shape
    iu = np.triu_indices(n, 1); D = len(iu[0])
    F = (Yall[:, iu[0]].astype(float) * Yall[:, iu[1]])
    FS = (X[:, iu[0]].astype(float) * X[:, iu[1]])
    keys = ccp.key_of(X)
    mask = np.ones(len(Yall), dtype=bool); mask[keys] = False
    rank = np.linalg.matrix_rank(np.hstack([np.ones((K, 1)), FS]))
    if rank < K:
        return dict(indep=False, t=0.0, dual=1.0)
    # primal
    FO = F[mask]; M = FO.shape[0]
    c = np.zeros(D + 2); c[-1] = -1.0
    A_eq = np.hstack([FS, -np.ones((K, 1)), np.zeros((K, 1))])
    A_ub = np.hstack([-FO, np.ones((M, 1)), np.ones((M, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(M), A_eq=A_eq, b_eq=np.zeros(K),
                  bounds=[(-1, 1)] * D + [(None, None), (None, 10.0)], method="highs")
    assert res.status == 0
    t = res.x[-1]
    # dual certificate: h on all states; maximise mass off S
    N = len(Yall)
    G = np.hstack([np.ones((N, 1)), F]).T                       # (D+1) x N : h orthogonal to 1 and phi
    obj = -mask.astype(float)
    bounds = [(0, None) if mask[k] else (None, None) for k in range(N)]
    res2 = linprog(obj, A_ub=mask.astype(float)[None, :], b_ub=[1.0], A_eq=G, b_eq=np.zeros(D + 1), bounds=bounds,
                   method="highs")
    assert res2.status == 0
    return dict(indep=True, t=t, dual=-res2.fun)


def main():
    n = int(sys.argv[1]); trials = int(sys.argv[2]); Ks = [int(k) for k in sys.argv[3:]]
    rng = np.random.default_rng(4400 + n)
    Yall = ccp.all_states(n); N = len(Yall)
    iu = np.triu_indices(n, 1)
    print(f"n = {n}: {N} states modulo the flip; {trials} instances per K", flush=True)
    tot = agree = incons = 0; margins = []; undecided = 0; e32 = 0.0
    for K in Ks:
        t0 = time.time(); f_repo = f_mine = 0; dis = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            X = Yall[idx].astype(np.int64)
            ans, it = ccp.is_face(X, Yall)
            mine = my_decision(X, Yall)
            face_primal = mine["indep"] and mine["t"] > 1e-6
            notface_dual = (not mine["indep"]) or mine["dual"] > 0.5
            if face_primal == notface_dual:
                incons += 1
            if face_primal:
                margins.append(mine["t"])
            if ans is None:
                undecided += 1
            else:
                f_repo += bool(ans)
                if bool(ans) != face_primal:
                    dis += 1
            f_mine += face_primal; tot += 1
        agree += trials - dis
        print(f"   K = {K:3d} (K/n = {K / n:.2f}): faces by the script {f_repo}/{trials}, by the full LP {f_mine}/{trials}; "
              f"instance-wise disagreements {dis}   ({time.time() - t0:.0f} s)", flush=True)
    # float32 energies of the script against float64, for a random coupling with |Q_ij| <= 1
    Q = rng.uniform(-1, 1, size=(n, n)); Q = np.triu(Q, 1); Qm = Q + Q.T
    E32 = ccp.energies(Yall, Qm)
    E64 = 0.5 * np.einsum("ij,ij->i", Yall.astype(float) @ Qm, Yall.astype(float))
    e32 = np.abs(E32 - E64).max()
    margins = np.array(margins)
    print(f"   total {tot}: agreement script / full LP in {agree}; primal and dual certificates inconsistent in {incons}; undecided by the script {undecided}")
    if len(margins):
        print(f"   margins t* of the {len(margins)} faces (|Q_ij| <= 1): min {margins.min():.3e}, 1% quantile {np.quantile(margins, 0.01):.3e}, median {np.median(margins):.3e}"
              f"   (script: 'not a face' if t <= 1e-7; 'face' needs min energy - c > 1e-5)")
    print(f"   LP solves inside the script: {len(status_log)}; with status != 0 (counted as 'not a face' by the script): {sum(s != 0 for s in status_log)}")
    print(f"   float32 energies of the script against float64, random |Q_ij| <= 1: largest error {e32:.2e}")


if __name__ == "__main__":
    main()
