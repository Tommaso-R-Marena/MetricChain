#!/usr/bin/env python3
"""Workstream R27, Item 4 -- independent re-evaluation of the configurations found by item4_worstcase.py (file item4_worstcase_found.npz),
and a finer scan for the helix-like trace of 20 points: at which accuracy of the distances does a DISTANT configuration first fit them?

Part 1 (verification, different code path: plain loops, no shared helper for the distances): for every stored Y
   rms and max of the distance errors over the 4n-10 pairs of separation <= 4, RMSD after the best superposition (improper allowed, and proper
   only), the chirality (sign of the signed volume) of every window of four consecutive points of Y against that of X.
Part 2 (scan): for targets r = 0.5 ... 10 A: minimise the rms distance error subject to RMSD >= r (quadratic penalty with increasing weight,
   L-BFGS), from soft-mode starts and from the distant configurations of Part 1.  (Two earlier versions of this part used SLSQP with the
   constraint the other way round and returned 'none' for most rows -- SLSQP ended slightly infeasible; their logs, _run1 and _run2, are not to
   be cited for Part 2.)
Controls: Part 1 recomputes the constraint that the search imposed (a stored Y that violates it would show); at the smallest target the scan must return the
first-order value.
Run:  OMP_NUM_THREADS=1 python3 -B item4_worstcase_verify.py > item4_worstcase_verify_<stamp>.log
"""
import os, sys, time, math
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import cap_memory, peak_mb, now, helix, procrustes, procrustes_proper, pair_arrays, half_jacobian

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27123)
print(f"R27 item4_worstcase_verify.py started {now()}")
here = os.path.dirname(os.path.abspath(__file__))
found = np.load(os.path.join(here, "item4_worstcase_found.npz"))
refs = {"helix-like n=12": helix(12, 2.3, 1.5, 100.0), "helix-like n=20": helix(20, 2.3, 1.5, 100.0),
        "strand-like 160 n=12": helix(12, 0.94, 3.3, 160.0), "strand-like 160 n=20": helix(20, 0.94, 3.3, 160.0)}


def errors_plain(X, Y):
    n = len(X); out = []
    for j in range(n):
        for k in range(j + 1, min(n, j + 5)):
            dx = math.sqrt(sum((X[j][a] - X[k][a]) ** 2 for a in range(3)))
            dy = math.sqrt(sum((Y[j][a] - Y[k][a]) ** 2 for a in range(3)))
            out.append(dy - dx)
    return np.array(out)


def chirality(P):
    return np.array([np.sign(np.dot(P[i + 1] - P[i], np.cross(P[i + 2] - P[i], P[i + 3] - P[i]))) for i in range(len(P) - 3)])


print("\nPart 1.  columns: case | sigma imposed | rms, max distance error recomputed | RMSD (improper allowed) | RMSD (proper only) | R_g |"
      " windows of Y with the chirality of X / opposite (after the optimal isometry) | radius of gyration of Y")
bad = 0
for key in found.files:
    name, sig = key.split("|"); sig = float(sig)
    X = refs[name]; Y = found[key]; n = len(X)
    de = errors_plain(X, Y)
    rms = math.sqrt((de ** 2).mean())
    R, t, res = procrustes(X, Y)
    Rp, tp, resp = procrustes_proper(X, Y)
    cx = chirality(X) * np.sign(np.linalg.det(R)); cy = chirality(Y)
    same = int((cx == cy).sum()); opp = int((cx != cy).sum())
    rg = math.sqrt(((X - X.mean(0)) ** 2).sum() / n); rgy = math.sqrt(((Y - Y.mean(0)) ** 2).sum() / n)
    if rms > sig * (1 + 1e-6):
        bad += 1
    print(f"   {name:22s} | {sig:5.2f} | {rms:.4f} {np.abs(de).max():.3f} | {np.linalg.norm(res) / math.sqrt(n):7.3f} | {np.linalg.norm(resp) / math.sqrt(n):7.3f} | {rg:6.2f} | {same:2d} / {opp:2d} | {rgy:6.2f}")
print(f"   stored configurations that violate the constraint they were found under: {bad}")

# ---- Part 2 ---------------------------------------------------------------------------------------------------------------
X = refs["helix-like n=20"]; n = 20
J, K = pair_arrays(n)
d0 = np.linalg.norm(X[J] - X[K], axis=1); N = len(J)
A = half_jacobian(X, J, K)
U, S, Vt = np.linalg.svd(A / d0[:, None], full_matrices=True)
s7 = S[3 * n - 7]; soft = Vt[3 * n - 7].reshape(n, 3)


def derr(Y):
    return np.linalg.norm(Y[J] - Y[K], axis=1) - d0


def neg_d2(y):
    res = procrustes(X, y.reshape(n, 3))[2]
    return -(res * res).sum(), (-2 * res).ravel()


def con(y, sig):
    de = derr(y.reshape(n, 3))
    return 1.0 - (de @ de) / (N * sig * sig)


def con_jac(y, sig):
    Y = y.reshape(n, 3); dv = Y[J] - Y[K]; L = np.linalg.norm(dv, axis=1)
    v = (2 * (L - d0) / L)[:, None] * dv
    G = np.zeros_like(Y); np.add.at(G, J, v); np.add.at(G, K, -v)
    return (-G / (N * sig * sig)).ravel()


def pull_back(Y, sig, frac=0.97):
    y = Y.ravel().copy()

    def fg(z):
        de = derr(z.reshape(n, 3))
        return de @ de, -con_jac(z, 1.0) * N

    for _ in range(400):
        de = derr(y.reshape(n, 3))
        if math.sqrt((de @ de) / N) <= frac * sig:
            break
        y = minimize(fg, y, jac=True, method="L-BFGS-B", options=dict(maxiter=2 if frac < 0.99 else 1)).x
    return y.reshape(n, 3)


def solve(Y0, sig):
    res = minimize(neg_d2, Y0.ravel(), jac=True, method="SLSQP", constraints=[dict(type="ineq", fun=con, jac=con_jac, args=(sig,))],
                   options=dict(maxiter=600, ftol=1e-13))
    Y = res.x.reshape(n, 3); de = derr(Y)
    if math.sqrt((de @ de) / N) > sig * (1 + 1e-9):
        # SLSQP stopped slightly outside the constraint set: move back inside (this can only lower d_P) -- the reported Y is always feasible
        Y = pull_back(Y, sig, frac=0.999)
        de = derr(Y)
        if math.sqrt((de @ de) / N) > sig * (1 + 1e-9):
            return None
    return np.linalg.norm(procrustes(X, Y)[2]) / math.sqrt(n), Y


print("\nPart 2.  the smallest rms distance error found at which some configuration lies at RMSD >= r from the trace (penalty method, L-BFGS; an UPPER bound")
print("         for the true minimum: every row is an explicit configuration, re-evaluated).  columns: r (A) | rms distance error | RMSD achieved | max |distance error| |")
print("         first-order value r / (sqrt(N/n)/s_7) | windows with opposite chirality | start that gave it")


def scan(name, X, far_keys):
    n = len(X)
    J, K = pair_arrays(n)
    d0 = np.linalg.norm(X[J] - X[K], axis=1); N = len(J)
    A = half_jacobian(X, J, K)
    U, S, Vt = np.linalg.svd(A / d0[:, None], full_matrices=True)
    s7 = S[3 * n - 7]
    soft = [Vt[3 * n - 7 - q].reshape(n, 3) for q in range(3)]
    fo = math.sqrt(N / n) / s7
    rg = math.sqrt(((X - X.mean(0)) ** 2).sum() / n)

    def fg(y, r, w):
        Y = y.reshape(n, 3)
        dv = Y[J] - Y[K]; L = np.linalg.norm(dv, axis=1); de = L - d0
        v = (2 * de / L)[:, None] * dv / N
        G = np.zeros_like(Y); np.add.at(G, J, v); np.add.at(G, K, -v)
        f = (de @ de) / N
        res = procrustes(X, Y)[2]
        rmsd = np.linalg.norm(res) / math.sqrt(n)
        if rmsd < r:
            f += w * (r - rmsd) ** 2
            if rmsd > 1e-12:
                G += -2 * w * (r - rmsd) * res / (rmsd * n)
        return f, G.ravel()

    def run(Y0, r):
        y = Y0.ravel().copy()
        for w in (1.0, 10.0, 100.0, 1e3, 1e4):
            y = minimize(fg, y, args=(r, w), jac=True, method="L-BFGS-B", options=dict(maxiter=3000, maxfun=6000)).x
        Y = y.reshape(n, 3)
        de = np.linalg.norm(Y[J] - Y[K], axis=1) - d0
        return math.sqrt((de @ de) / N), np.linalg.norm(procrustes(X, Y)[2]) / math.sqrt(n), np.abs(de).max(), Y

    print(f"   {name}:  R_g = {rg:.2f} A, first-order RMSD per unit rms distance error = {fo:.3f}")
    prev = None
    out_rows = []
    for r in (0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0):
        starts = []
        for q in range(3):
            for sg in (1, -1):
                starts.append((f"soft mode {q + 1}", X + sg * r * math.sqrt(n) * soft[q]))
        for key in far_keys:
            starts.append((f"distant configuration found at sigma = {key.split('|')[1]}", found[key]))
        if prev is not None:
            starts.append(("previous r", prev))
        best = None
        for kind, Y0 in starts:
            sg_, rm, mx, Y = run(Y0, r)
            if rm >= r * (1 - 2e-3) and (best is None or sg_ < best[0]):
                best = (sg_, rm, mx, Y, kind)
        if best is None:
            print(f"      {r:5.1f} | no end point reached the target")
            continue
        sg_, rm, mx, Y, kind = best
        prev = Y
        R, t, res = procrustes(X, Y)
        opp = int((chirality(X) * np.sign(np.linalg.det(R)) != chirality(Y)).sum())
        print(f"      {r:5.1f} | {sg_:.4f} | {rm:7.3f} | {mx:.3f} | {r / fo:.4f} | {opp:2d} of {n - 3} | {kind}")
        out_rows.append((r, sg_, rm))
        sys.stdout.flush()
    return out_rows, fo, rg


rowsH, foH, rgH = scan("helix-like n=20", refs["helix-like n=20"], ["helix-like n=20|0.3", "helix-like n=20|0.5"])
rowsH12, foH12, rgH12 = scan("helix-like n=12", refs["helix-like n=12"], ["helix-like n=12|0.5"])
rowsS, foS, rgS = scan("strand-like 160 n=20", refs["strand-like 160 n=20"], ["strand-like 160 n=20|0.1", "strand-like 160 n=20|0.3"])
print(f"   control: at the smallest r the rms error found must equal the first-order value: helix n=20: {rowsH[0][1]:.4f} vs {rowsH[0][0] / foH:.4f};"
      f"  helix n=12: {rowsH12[0][1]:.4f} vs {rowsH12[0][0] / foH12:.4f};  strand n=20: {rowsS[0][1]:.4f} vs {rowsS[0][0] / foS:.4f}  (<= by at most a few per cent: second-order effects)")
for nm, rows_, rg_ in (("helix-like n=20", rowsH, rgH), ("helix-like n=12", rowsH12, rgH12), ("strand-like 160 n=20", rowsS, rgS)):
    over = [r for r in rows_ if r[2] >= rg_]
    half = [r for r in rows_ if r[2] >= 0.5 * rg_]
    print(f"   {nm}: an rms distance error of {min(r[1] for r in half):.3f} A already admits a configuration at RMSD >= R_g/2"
          + (f"; {min(r[1] for r in over):.3f} A admits one at RMSD >= R_g = {rg_:.2f} A" if over else f"; none at RMSD >= R_g = {rg_:.2f} A among the targets"))
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
