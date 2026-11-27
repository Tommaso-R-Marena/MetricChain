# SCRATCH — preserved at the consolidation of 2026-11-27; NOT part of run_all.py, NOT reviewed, NOT quoted as a
# result in the report (E20e mentions it as scratch).  Prototype for fourteen or fifteen states on a torus of four
# angles.  Usage: python3 experiments/ensemble/scratch/torus_four_angles_k14.py <K> <first seed> <last seed + 1>
# The survey of seeds 0..15 at K = 14 made in the session is in k14_survey_seeds0-15.log (15 NOT IDENTIFIED with
# an explicit second ensemble, seed 4 undecided).  To make this a result: verify the twins independently, add
# the case to torus_four_angles.py, store the survey through run_all.py / output_threshold.txt.
# K = 14 or 15 states on T^4: the zero set Z of the lifted certificate has dimension e = K - 12 (a surface, a
# threefold).  Candidates: functions of the data span with value and tangential gradient zero at the states, modulo
# those vanishing on Z.  LP over a random sample of Z; positives verified on the torus, negatives by a twin.
import numpy as np, sys, time, itertools
from scipy.optimize import linprog, minimize
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import torus_four_angles as t4
F, dF, w, dw, wrap, gval, gjac, R4 = t4.F, t4.dF, t4.w, t4.dw, t4.wrap, t4.gval, t4.gjac, t4.R4
def project(N, phi):
    for _ in range(60):
        res = gval(N, phi)
        if np.linalg.norm(res) < 1e-13: break
        phi = phi - np.linalg.lstsq(gjac(N, phi), res, rcond=None)[0]
    return phi
def tangent_basis(N, phi):
    return np.linalg.svd(gjac(N, phi))[2][N.shape[0]:]          # e x 4, orthonormal
def analyse(seed, K, nsample=3000, verbose=True):
    t0 = time.time(); rng = np.random.default_rng(seed)
    e = K - 12; nf = 16 - K
    P = rng.uniform(-np.pi, np.pi, size=(K, R4))
    N = np.linalg.svd(np.array([w(p) for p in P]))[2][K:]
    Z = []
    while len(Z) < nsample:
        z = project(N, rng.uniform(-np.pi, np.pi, R4))
        if np.linalg.norm(gval(N, z)) < 1e-10: Z.append(wrap(z))
    # extra points of Z near every state (a second measure with the same data needs mass near the states)
    for p in P:
        Tb0 = tangent_basis(N, p)
        for rho in (0.07, 0.12, 0.2):
            for _ in range(12):
                c = rng.normal(size=e); c /= np.linalg.norm(c)
                z = project(N, p + rho*(c @ Tb0))
                if np.linalg.norm(gval(N, z)) < 1e-10: Z.append(wrap(z))
    Z = np.array(Z)
    dist = np.min(np.linalg.norm(wrap(Z[:, None, :] - P[None, :, :]), axis=2), axis=1)
    Fz = np.array([F(z) for z in Z])
    sv = np.linalg.svd(Fz, compute_uv=False); dimR = int(np.sum(sv > 1e-8*sv[0])); Rb = np.linalg.svd(Fz)[2][:dimR].T
    rows = []
    for p in P:
        rows.append(F(p))
        for u in tangent_basis(N, p): rows.append(u @ dF(p))
    M = np.array(rows) @ Rb
    svM = np.linalg.svd(M, compute_uv=False); rankM = int(np.sum(svM > 1e-8*svM[0]))
    cand = Rb @ np.linalg.svd(M)[2][rankM:].T; nc = cand.shape[1]
    # second derivatives along several tangent directions at each state
    h = 2e-3; d2 = []
    dirs = [np.eye(e)[i] for i in range(e)] + [(np.eye(e)[i] + s*np.eye(e)[j])/np.sqrt(2) for i in range(e) for j in range(i+1, e) for s in (1, -1)]
    for p in P:
        Tb = tangent_basis(N, p)
        for c in dirs:
            u = c @ Tb; a = project(N, p + h*u); b = project(N, p - h*u)
            d2.append((F(a) + F(b) - 2*F(p))/h**2)
    d2 = np.array(d2) @ cand
    far = dist > 0.3
    A_ub = np.vstack([-np.hstack([Fz[far] @ cand, -np.ones((far.sum(), 1))]), -np.hstack([d2, -np.ones((d2.shape[0], 1))])])
    res = linprog(np.concatenate([np.zeros(nc), [-1.0]]), A_ub=A_ub, b_ub=np.zeros(A_ub.shape[0]), bounds=[(-1, 1)]*nc + [(None, None)], method="highs")
    out = dict(seed=seed, K=K, dimR=dimR, conditions=M.shape[0], rank=rankM, candidates=nc, t=(-res.fun if res.status == 0 else float('nan')))
    if out['t'] > 1e-6:
        q = cand @ res.x[:-1]
        rs = np.random.default_rng(999); smp = rs.uniform(-np.pi, np.pi, size=(600, R4)); Fs = np.array([F(s) for s in smp])
        coeffs = lambda fun: np.linalg.lstsq(Fs, np.array([fun(s) for s in smp]), rcond=None)[0]
        Lc = coeffs(lambda s: np.sum(gval(N, s)**2))
        rws, rhs = [], []
        for p in P:
            ab = np.linalg.lstsq(gjac(N, p).T, dF(p) @ q, rcond=None)[0]
            for j in range(nf):
                row = np.zeros(16*nf); row[16*j:16*(j+1)] = w(p); rws.append(row); rhs.append(-ab[j])
        ell = np.linalg.lstsq(np.array(rws), np.array(rhs), rcond=None)[0]
        ic = coeffs(lambda s: sum((ell[16*j:16*(j+1)] @ w(s))*gval(N, s)[j] for j in range(nf)))
        hfun = q + ic
        out['grad'] = float(max(np.linalg.norm(dF(p) @ hfun) for p in P)); out['qmin_sample'] = float((Fz @ q).min()); out['cert'] = None
        for A in (1e3, 1e4, 1e5, 1e6, 1e7):
            fc = A*Lc + hfun
            vals, g = t4.grid_values(fc)
            fmin, away = float(vals.min()), np.inf
            for i in np.argsort(vals, axis=None)[:40]:
                x0 = np.array([g[k] for k in np.unravel_index(i, vals.shape)])
                rr = minimize(lambda s: F(s) @ fc, x0, jac=lambda s: dF(s) @ fc, method="BFGS", options={"gtol": 1e-11})
                fmin = min(fmin, rr.fun)
                if min(np.linalg.norm(wrap(rr.x - p)) for p in P) > 1e-3: away = min(away, rr.fun)
            eig = []
            for p in P:
                H = np.zeros((R4, R4))
                for a in range(R4):
                    ee = np.zeros(R4); ee[a] = 1e-4
                    H[:, a] = (dF(p + ee) @ fc - dF(p - ee) @ fc)/2e-4
                eig.append(np.linalg.eigvalsh((H + H.T)/2)[0])
            if fmin > -1e-11*A and min(eig) > 1e-6 and (not np.isfinite(away) or away > 1e-12*A + 1e-9):
                out['cert'] = dict(A=A, minimum=fmin, hessian=float(min(eig)), away=float(away)); break
            out['last'] = dict(A=A, minimum=fmin, hessian=float(min(eig)), away=float(away))
        out['verdict'] = 'IDENTIFIED' if out['cert'] else 'UNDECIDED (candidate on the sample; torus check failed)'
    else:
        sel = np.vstack([Z[dist > 0.05][:1500], Z[(dist > 0.05) & (dist < 0.3)]])
        cols = np.array([F(z) for z in sel] + [F(p) for p in P]).T
        y = np.mean([F(p) for p in P], axis=0)
        rt = linprog(np.concatenate([np.zeros(len(sel)), np.ones(K)]), A_eq=cols, b_eq=y, bounds=[(0, None)]*cols.shape[1], method="highs")
        out['least_mass_on_states'] = float(rt.fun) if rt.status == 0 else None
        out['verdict'] = 'NOT IDENTIFIED' if (rt.status == 0 and rt.fun < 1 - 1e-6) else 'UNDECIDED (no candidate; no twin found)'
    out['secs'] = round(time.time() - t0, 1)
    if verbose: print(out, flush=True)
    return out
if __name__ == "__main__":
    K = int(sys.argv[1])
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        analyse(seed, K)
