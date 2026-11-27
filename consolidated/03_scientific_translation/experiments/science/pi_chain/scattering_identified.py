"""Identified sets from a scattering curve of finite range and finite precision (OPEN_PROBLEMS.md C4).

Diamond-lattice chain of N = n + 3 beads (identical point scatterers).  Debye intensity of a conformation,
    I_x(q) = N + 2 * sum_{i<j} sin(q r_ij)/(q r_ij),
a linear functional of its pair-distance histogram (workstream A2, Proposition A2.1).  Data: the
ensemble-averaged intensity at the first K Shannon channels q_k = k*pi/D_max (D_max = contour-limited
largest distance), each known within a relative tolerance tau (tau = 0: exact).  Question: the exact
range of an unmeasured ensemble average over ALL ensembles of chain conformations consistent with the
data (model-free identified set), as a function of K and tau.

Why a tolerance is essential: I(q) is an entire function of q, so exact knowledge on any interval
determines the whole averaged histogram.  What a finite-precision curve determines is the question.
"""
from __future__ import annotations
import sys, os, json, math, time
import numpy as np
from scipy.optimize import linprog
from identified_sets import get

def sinc(x):
    return np.where(x == 0, 1.0, np.sin(x)/np.where(x == 0, 1.0, x))

def setup(n):
    d, pair = get(n); N = n + 3
    sv = d["svals"].astype(float); H = d["hist"].astype(float)
    g = d["gauche"].astype(float); rg2 = d["rg2"].astype(float)/N**2; ree2 = d["ree2"].astype(float)
    return dict(n=n, N=N, sv=sv, H=H, g=g, rg2=rg2, ree2=ree2)

def intensity(S, q):
    """I_x(q) for all conformations x; q in units of 1/(lattice unit), distances r = sqrt(s)."""
    N = S["N"]
    const = N + 2*((N-1)*sinc(q*math.sqrt(3.0)) + (N-2)*sinc(q*math.sqrt(8.0)))
    return const + 2*(S["H"] @ sinc(q*np.sqrt(S["sv"])))

def interval(F, psi, m, tol):
    """exact [min, max] of E psi over probability vectors mu with |E F_k - m_k| <= tol*m_k (F: M x K)."""
    key = np.round(F, 9)
    uniq, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel(); C = len(uniq)
    hi = np.full(C, -np.inf); lo = np.full(C, np.inf)
    np.maximum.at(hi, inv, psi); np.minimum.at(lo, inv, psi)
    Fc = np.zeros((C, F.shape[1])); Fc[inv] = F
    scale = np.maximum(np.abs(m), 1e-12)
    A = (Fc/scale).T; b = m/scale
    out = []
    for c in (lo, -hi):
        if tol == 0:
            res = linprog(c, A_eq=np.vstack([A, np.ones(C)]), b_eq=np.concatenate([b, [1.0]]), bounds=(0, None),
                          method="highs", options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
        else:
            res = linprog(c, A_ub=np.vstack([A, -A]), b_ub=np.concatenate([b*(1+tol), -b*(1-tol)]),
                          A_eq=np.ones((1, C)), b_eq=[1.0], bounds=(0, None), method="highs",
                          options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
        if res.status != 0: return None
        out.append(res.fun)
    return out[0], -out[1]

def analyse(n, Ks=(1, 2, 3, 4, 6, 8, 12), tols=(0.0, 0.01, 0.05), truth="athermal"):
    S = setup(n); N = S["N"]; M = len(S["g"])
    w = np.ones(M) if truth == "athermal" else np.exp(S["H"][:, list(S["sv"]).index(3.0)] if 3.0 in S["sv"] else 0)
    p = w/w.sum()
    Dmax = math.sqrt(S["ree2"].max())                     # largest end-to-end distance = largest distance
    rg0 = math.sqrt(p @ S["rg2"])
    thr = np.quantile(S["rg2"], 0.10)
    targets = {"Rg2 / <Rg2>": S["rg2"]/(p @ S["rg2"]), "gauche fraction": S["g"]/n,
               "end-to-end R2 / <R2>": S["ree2"]/(p @ S["ree2"]), "P(compact decile)": (S["rg2"] <= thr).astype(float)}
    rows = []
    print(f"# n = {n} torsions, N = {N} beads, {M} conformations, truth = {truth}; D_max = {Dmax:.2f}, Rg = {rg0:.2f} (lattice units); "
          f"Shannon channel k at q_k Rg = k * {math.pi*rg0/Dmax:.3f}")
    for K in Ks:
        qs = np.array([k*math.pi/Dmax for k in range(1, K+1)])
        F = np.stack([intensity(S, q) for q in qs], axis=1); m = p @ F
        for tol in tols:
            line = f"K={K:2d} (q_max Rg = {K*math.pi*rg0/Dmax:5.2f}) tol={tol:4.2f}:"
            for name, psi in targets.items():
                iv = interval(F, psi, m, tol)
                a0, a1 = float(psi.min()), float(psi.max()); tv = float(p @ psi)
                if iv is None:
                    line += f"  {name}: LP failed"; continue
                lo, hi = iv; frac = (hi - lo)/(a1 - a0)
                rows.append(dict(n=n, N=N, truth=truth, K=K, qmaxRg=K*math.pi*rg0/Dmax, tol=tol, target=name, truth_value=tv,
                                 lo=lo, hi=hi, apriori_lo=a0, apriori_hi=a1, unidentified_fraction=frac))
                line += f"  {name.split(' ')[0]} [{lo:.3f},{hi:.3f}] ({frac:.2f})"
            print(line, flush=True)
    return rows

if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1:]] or [8, 10]
    allrows = []
    for n in ns:
        t0 = time.time(); allrows += analyse(n); print(f"# n={n}: {time.time()-t0:.0f} s")
    json.dump(allrows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"scattering_identified_n{'_'.join(map(str, ns))}.json"), "w"), indent=1)
