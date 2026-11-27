#!/usr/bin/env python3
"""Workstream R27, Item 4 -- the classes of the assumptions of Theorem L, each with a computed example.

 (A) "no four consecutive points coplanar":
     (A1) an INTERIOR four-point window (W_i, 2 <= i <= n-4) exactly coplanar: the reflected tail has the same data (eta = 0) and is not
          congruent -> the conclusion is false: essential.
     (A2) the two END windows W_1, W_{n-3} coplanar (five-point end windows still non-flat): the proof never uses tau_1, tau_{n-3};
          (local) and the uniform bound with tau* = min over the interior windows are checked on arbitrary Y: no violation expected.
 (B) "complete data of separation <= 4":
     (B1) one pair of separation 4 unmeasured: a reflection changes only that pair -> false.
     (B2) the pair (1,2) unmeasured (x_1 held by three distances): reflect x_1 in the plane of x_3, x_4, x_5 -> false.
     (B3) an interior pair of separation 1, 2 or 3 unmeasured: the first-order constant stays finite (infinitesimal rigidity survives);
          no proof and no counterexample here -- "needed only by the proof, constants change" is a conjecture, labelled as such.
 (C) "Y in R^3": Y allowed in R^4 (an unprojected relaxation): y_i = (x_i, eps w_i), w the affine dependency of a five-point window:
     ||eta|| = O(eps^2), d_P ~ eps -> no linear bound: essential.
 (D) dimension and range: the analogue with windows of K and K+1 points in R^d (K >= d+1), '1/2' replaced by 1/sqrt(K): (local) checked on
     arbitrary Y for (d, K) = (2, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 5).  [Remarks 4 and 6 of the note.]
 (E) "the chain structure of X": bonds enter only through b in Step 4; (local) holds for any X whose windows are non-flat (checked in the battery
     on point clouds).

Controls: in (A2) the same check with an interior window flattened must fail (it is (A1)); in (D) the bound with the lever-arm term dropped must fail.
Run:  OMP_NUM_THREADS=1 python3 -B item4_examples.py > item4_examples_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from r27lib import (cap_memory, peak_mb, now, KAPPA, angle_chain, random_unit_chain, helix, chain_consts, pair_arrays, eta_vec,
                    procrustes, half_jacobian)

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27119)
print(f"R27 item4_examples.py started {now()}")


def dP(X, Y):
    return np.linalg.norm(procrustes(X, Y)[2])


def flatten(X, i, tail=True):
    """make the four points X[i..i+3] exactly coplanar by moving X[i+3] (and, rigidly, everything after it) into the plane of X[i], X[i+1], X[i+2]"""
    X = X.copy()
    nrm = np.cross(X[i + 1] - X[i], X[i + 2] - X[i]); nrm /= np.linalg.norm(nrm)
    h = (X[i + 3] - X[i]) @ nrm
    X[i + 3:] -= h * nrm
    return X


def reflect_beyond(X, i):
    """reflect the points after X[i+3] in the plane of X[i+1], X[i+2], X[i+3]"""
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


# ---- (A1) ---------------------------------------------------------------------------------------------------------------
print("\n(A1) interior four-point window exactly coplanar: Y = points beyond it reflected in its plane")
for n in (6, 8, 12):
    for i in (1, n // 2 - 2, n - 5):               # 0-based start of the coplanar window; interior means 1 <= i <= n-5
        X = flatten(angle_chain(n, rng), i)
        tau, s, b = chain_consts(X)
        nrm = np.cross(X[i + 1] - X[i], X[i + 2] - X[i]); nrm /= np.linalg.norm(nrm)
        Y = X.copy()
        Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i]) @ nrm)[:, None] * nrm[None, :]
        J, K = pair_arrays(n)
        et = eta_vec(X, Y, J, K)
        print(f"     n = {n:2d}, coplanar window W_{i + 1} (1-based): tau = {tau[i]:.1e}, ||eta||_2 = {np.linalg.norm(et):.1e}, d_P(X, Y) = {dP(X, Y):.4f}  -> d_P/||eta|| unbounded: conclusion FALSE")

# ---- (A2) ---------------------------------------------------------------------------------------------------------------
print("\n(A2) the END windows W_1 and W_{n-3} exactly coplanar (interior windows generic): (local) and the uniform bound with tau* := min over interior windows")


def local_check(X, Y, interior_only=True):
    """max over k of |y_k - g1 x_k| / local_k and  ||Y - g1 X||_F / uniform(tau* over interior windows)"""
    n = len(X)
    tau, s, b = chain_consts(X)
    J, K = pair_arrays(n)
    et = eta_vec(X, Y, J, K)
    idx = {(int(j), int(k)): q for q, (j, k) in enumerate(zip(J, K))}
    e = np.array([np.sqrt(sum(et[idx[(p, q)]] ** 2 for p in range(i, i + 5) for q in range(p + 1, i + 5))) for i in range(n - 4)])
    delta = KAPPA * e / s
    R1, t1, _ = procrustes(X[:5], Y[:5])
    dist = np.linalg.norm(Y - X @ R1 - t1, axis=1)
    cW = np.array([X[i:i + 4].mean(0) for i in range(n - 3)])
    worst = 0.0
    scale = max(1.0, np.abs(X).max(), np.abs(Y).max())
    for k in range(n):
        i = min(k, n - 5)
        bound = delta[i] + sum((delta[j] + delta[j + 1]) * (np.linalg.norm(X[k] - cW[j + 1]) / tau[j + 1] + 0.5) for j in range(i))
        if bound > 1e-7 * scale:
            worst = max(worst, dist[k] / bound)
        elif dist[k] > 1e-9 * scale:
            worst = np.inf
    tau_int = tau[1:n - 4].min() if n > 5 else np.inf
    if n > 5:
        U = 1.2 * b * (n + 2) ** 2 / (s.min() * tau_int) * np.linalg.norm(et)
        uni = np.linalg.norm(dist) / U if U > 1e-7 * scale else 0.0
    else:
        uni = 0.0
    return worst, uni, tau


def some_Y(X, rng, q):
    n = len(X)
    kind = q % 7
    if kind == 0:
        return X + 10.0 ** rng.uniform(-4, 1) * rng.normal(size=X.shape)
    if kind == 1:
        return rng.normal(size=X.shape) * 10.0 ** rng.uniform(-1, 1)
    if kind == 2:
        i = rng.integers(0, n - 4)
        try:
            return reflect_beyond(X, i) + (0 if q % 2 else 1e-3) * rng.normal(size=X.shape)
        except Exception:
            return X + rng.normal(size=X.shape)
    if kind == 3:
        Y = X.copy(); k = rng.integers(n); Y[k] += rng.normal(size=3) * 10.0 ** rng.uniform(-1, 3); return Y
    if kind == 4:
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        return X @ (np.eye(3) - np.outer(u, u))
    if kind == 5:
        return angle_chain(n, rng)
    return np.zeros_like(X)


tot = 0; viol = 0; w1 = 0.0; w2 = 0.0; ctl_viol = 0; ctl_tot = 0
for n in (6, 7, 9, 12, 20):
    for rep in range(12):
        X = angle_chain(n, rng)
        X = flatten(X, 0)                       # W_1 coplanar: move x_4.. into the plane of x_1, x_2, x_3
        # W_{n-3} coplanar: move the LAST point into the plane of the three before it
        nrm = np.cross(X[n - 3] - X[n - 4], X[n - 2] - X[n - 4]); nrm /= np.linalg.norm(nrm)
        X[n - 1] -= ((X[n - 1] - X[n - 4]) @ nrm) * nrm
        tau, s, b = chain_consts(X)
        assert tau[0] < 1e-12 and tau[-1] < 1e-12, (tau, s)            # both end windows are coplanar
        if tau[1:n - 4].min() < 1e-9 or s.min() < 1e-9:                 # (an interior window degenerate by accident: not the case under test)
            continue
        for q in range(60):
            Y = some_Y(X, rng, q)
            a, u, _ = local_check(X, Y)
            tot += 1
            w1 = max(w1, a); w2 = max(w2, u)
            if a > 1 + 1e-9 or u > 1 + 1e-9:
                viol += 1
        # control: additionally flatten an interior window: the reflected tail must violate (local) -- it is (A1)
        if n >= 7:
            Xc = flatten(X, 2)
            nrmc = np.cross(Xc[3] - Xc[2], Xc[4] - Xc[2]); nrmc /= np.linalg.norm(nrmc)
            Yc = Xc.copy(); Yc[6:] = Xc[6:] - 2 * ((Xc[6:] - Xc[2]) @ nrmc)[:, None] * nrmc[None, :]
            J, K = pair_arrays(n)
            ctl_tot += 1
            if np.linalg.norm(eta_vec(Xc, Yc, J, K)) < 1e-9 and dP(Xc, Yc) > 1e-3:
                ctl_viol += 1
print(f"     {tot} pairs (X with both end windows coplanar, tau_1 = tau_(n-3) = 0; Y arbitrary): violations {viol};  max per-point (local) ratio {w1:.4f};"
      f"  max ||Y - g1 X||_F / uniform bound with interior tau*: {w2:.5f}")
print(f"     control (an interior window flattened as well): eta = 0 and d_P > 0 in {ctl_viol} of {ctl_tot} cases (must be all)")

# ---- (B) ----------------------------------------------------------------------------------------------------------------
print("\n(B1) one pair of separation 4 unmeasured: reflection of the points beyond x_{i+3} in the plane of x_{i+1}, x_{i+2}, x_{i+3}")
for n in (5, 8, 12):
    X = angle_chain(n, rng)
    J, K = pair_arrays(n)
    for i in sorted(set([0, (n - 5) // 2, n - 5])):
        Y = reflect_beyond(X, i)
        et = eta_vec(X, Y, J, K)
        mask = ~((J == i) & (K == i + 4))
        print(f"     n = {n:2d}, pair ({i + 1},{i + 5}) unmeasured: ||eta|| over the measured pairs = {np.linalg.norm(et[mask]):.1e}, the unmeasured one changed by {et[~mask][0]:+.4f}, d_P = {dP(X, Y):.4f} -> FALSE")
print("(B2) the pair (1,2) unmeasured: x_1 reflected in the plane of x_3, x_4, x_5")
for n in (6, 12):
    X = angle_chain(n, rng)
    J, K = pair_arrays(n)
    nrm = np.cross(X[3] - X[2], X[4] - X[2]); nrm /= np.linalg.norm(nrm)
    Y = X.copy(); Y[0] = X[0] - 2 * ((X[0] - X[2]) @ nrm) * nrm
    et = eta_vec(X, Y, J, K)
    mask = ~((J == 0) & (K == 1))
    print(f"     n = {n:2d}: ||eta|| over the measured pairs = {np.linalg.norm(et[mask]):.1e}, pair (1,2) changed by {et[~mask][0]:+.4f}, d_P = {dP(X, Y):.4f} -> FALSE")
print("(B3) one INTERIOR pair of separation 1, 2 or 3 unmeasured: the (3n-6)-th singular value of the half-Jacobian of the remaining pairs (first-order rigidity)")
for n in (8, 12):
    X = angle_chain(n, rng)
    J, K = pair_arrays(n)
    A = half_jacobian(X, J, K)
    S0 = np.linalg.svd(A, compute_uv=False)
    S0 = np.concatenate([S0, np.zeros(max(0, 3 * n - len(S0)))])
    line = [f"all pairs: mu = {S0[3 * n - 7]:.4f}"]
    for sep in (1, 2, 3):
        j = n // 2 - 1
        mask = ~((J == j) & (K == j + sep))
        S = np.linalg.svd(A[mask], compute_uv=False)
        S = np.concatenate([S, np.zeros(max(0, 3 * n - len(S)))])
        line.append(f"without ({j + 1},{j + 1 + sep}): {S[3 * n - 7]:.4f}")
    print(f"     n = {n:2d}: " + ";  ".join(line) + "   (positive: still infinitesimally rigid; whether a global bound survives is NOT settled here)")

# ---- (C) ----------------------------------------------------------------------------------------------------------------
print("\n(C) Y in R^4:  y_i = (x_i, eps w_i), w = the affine dependency of the five points (unit vector orthogonal to 1 and to the coordinates)")
X = helix(5, 2.3, 1.5, 100.0)
Xc = X - X.mean(0)
U, S, Vt = np.linalg.svd(np.c_[np.ones(5), Xc], full_matrices=True)
w = U[:, 4]
X4 = np.c_[X, np.zeros(5)]
iu = np.triu_indices(5, 1)
for eps in (1.0, 1e-1, 1e-2, 1e-3, 1e-4):
    Y4 = np.c_[X, eps * w]
    et = ((Y4[iu[0]] - Y4[iu[1]]) ** 2).sum(1) - ((X4[iu[0]] - X4[iu[1]]) ** 2).sum(1)
    A0 = X4 - X4.mean(0); B0 = Y4 - Y4.mean(0)
    sv = np.linalg.svd(A0.T @ B0, compute_uv=False)
    Um, Sm, Vm = np.linalg.svd(A0.T @ B0)
    d4 = np.linalg.norm(B0 - A0 @ (Um @ Vm))
    print(f"     eps = {eps:7.0e}: ||eta||_2 = {np.linalg.norm(et):.3e}   d_P in R^4 = {d4:.3e}   d_P/||eta|| = {d4 / np.linalg.norm(et):.3e}   (Lemma Q in R^3 would allow at most {KAPPA / np.linalg.svd(Xc, compute_uv=False)[2]:.3f})")
print("     -> d_P/||eta|| grows like 1/eps: with Y outside R^3 there is no Lipschitz bound (only a Hoelder-1/2 one): 'Y in R^3' is ESSENTIAL")


# ---- (D) ----------------------------------------------------------------------------------------------------------------
def general_local(X, Y, K, d, lever=True):
    """the analogue of (local) for separation <= K in R^d: windows of K+1 points (complete data), shared windows of K points,
    thickness = d-th singular value of the centred window, mean factor 1/sqrt(K), i(k) = min(k, n-K-1) (0-based)."""
    n = len(X)
    nF = n - K
    sF = np.array([np.linalg.svd(X[i:i + K + 1] - X[i:i + K + 1].mean(0), compute_uv=False)[d - 1] for i in range(nF)])
    tW = np.array([np.linalg.svd(X[i:i + K] - X[i:i + K].mean(0), compute_uv=False)[d - 1] for i in range(n - K + 1)])
    cW = np.array([X[i:i + K].mean(0) for i in range(n - K + 1)])
    e = np.zeros(nF)
    for i in range(nF):
        P = X[i:i + K + 1]; Q = Y[i:i + K + 1]
        iu = np.triu_indices(K + 1, 1)
        dx = P[iu[0]] - P[iu[1]]; dy = Q[iu[0]] - Q[iu[1]]
        e[i] = np.linalg.norm(np.einsum("ij,ij->i", dy - dx, dy + dx))
    delta = KAPPA * e / sF
    A0 = X[:K + 1] - X[:K + 1].mean(0); B0 = Y[:K + 1] - Y[:K + 1].mean(0)
    Um, Sm, Vm = np.linalg.svd(A0.T @ B0)
    R1 = Um @ Vm
    t1 = Y[:K + 1].mean(0) - X[:K + 1].mean(0) @ R1
    dist = np.linalg.norm(Y - X @ R1 - t1, axis=1)
    worst = 0.0
    scale = max(1.0, np.abs(X).max(), np.abs(Y).max())
    for k in range(n):
        i = min(k, nF - 1)
        bound = delta[i] + sum((delta[j] + delta[j + 1]) * ((np.linalg.norm(X[k] - cW[j + 1]) / tW[j + 1] if lever else 0.0) + 1 / np.sqrt(K)) for j in range(i))
        if bound > 1e-7 * scale:
            worst = max(worst, dist[k] / bound)
        elif dist[k] > 1e-9 * scale:
            worst = np.inf
    return worst, min(tW.min(), sF.min())


print("\n(D) the analogue in R^d with separations <= K (windows of K and K+1 points; 1/2 -> 1/sqrt(K)); X = random chains with unit steps in R^d; Y arbitrary")
for d, K in ((2, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 5)):
    worst = 0.0; viol = 0; tot = 0; ctl = 0
    for rep in range(40):
        n = int(rng.integers(K + 2, 16))
        st = rng.normal(size=(n - 1, d)); st /= np.linalg.norm(st, axis=1)[:, None]
        X = np.vstack([np.zeros(d), np.cumsum(st, axis=0)])
        for q in range(25):
            kind = q % 5
            if kind == 0:
                Y = X + 10.0 ** rng.uniform(-4, 1) * rng.normal(size=X.shape)
            elif kind == 1:
                Y = rng.normal(size=X.shape) * 10.0 ** rng.uniform(-1, 1)
            elif kind == 2:
                # reflect a tail in a random hyperplane through a random point
                u = rng.normal(size=d); u /= np.linalg.norm(u); k0 = rng.integers(1, n - 1)
                Y = X.copy(); Y[k0:] = X[k0:] - 2 * ((X[k0:] - X[k0]) @ u)[:, None] * u[None, :]
            elif kind == 3:
                Y = X.copy(); k0 = rng.integers(n); Y[k0] += rng.normal(size=d) * 10.0 ** rng.uniform(-1, 2)
            else:
                Q, _ = np.linalg.qr(rng.normal(size=(d, d)))
                Y = X.copy(); k0 = rng.integers(1, n - 1); Y[k0:] = (X[k0:] - X[k0]) @ Q + X[k0]
            r, thick = general_local(X, Y, K, d)
            if thick < 1e-6:
                continue
            tot += 1
            worst = max(worst, r)
            viol += int(r > 1 + 1e-9)
            ctl += int(general_local(X, Y, K, d, lever=False)[0] > 1 + 1e-9)
    print(f"     d = {d}, K = {K}: pairs {tot}, violations {viol}, max per-point ratio {worst:.4f};  control (lever-arm term dropped) violated by {ctl} pairs")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
