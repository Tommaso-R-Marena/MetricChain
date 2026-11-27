#!/usr/bin/env python3
"""Workstream R27 -- common functions, written from the STATEMENTS of the Geometry division's note
(LOCAL_DATA_STABILITY.md at 9f164f9, section 3).  None of their code was available or used.

Conventions (theirs): points are ROW vectors; an isometry is x -> x R + t with R in O(3) (improper allowed).
Indices in the code are 0-based; the note is 1-based.  With j0 = j - 1:
    W_j = {j..j+3}   <->  X[j0:j0+4],   tau[j0] = sigma_3 of the centred 4-point window
    F_j = {j..j+4}   <->  X[j0:j0+5],   s[j0]   = sigma_3 of the centred 5-point window
    i(k) = min(k, n-4)  <->  i0(k0) = min(k0, n-5)
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import resource, sys, time
import numpy as np

KAPPA = 1.0 / (2.0 * np.sqrt(np.sqrt(2.0) - 1.0))          # 0.776887...


def cap_memory(gb=2.0):
    lim = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ----------------------------------------------------------------------------------------------------------------------
# configurations
# ----------------------------------------------------------------------------------------------------------------------
def helix(n, radius, rise, turn_deg, phase=0.0):
    t = np.arange(n) * np.deg2rad(turn_deg) + phase
    return np.c_[radius * np.cos(t), radius * np.sin(t), rise * np.arange(n)]


def random_unit_chain(n, rng):
    """freely jointed chain, unit bonds, directions uniform on the sphere (no constraint: thin windows can occur)"""
    d = rng.normal(size=(n - 1, 3))
    d /= np.linalg.norm(d, axis=1)[:, None]
    return np.vstack([np.zeros(3), np.cumsum(d, axis=0)])


def angle_chain(n, rng, th=(95.0, 125.0), ph=(40.0, 140.0)):
    """unit bonds, bond angle in th (degrees), |torsion| in ph (degrees), random sign: avoids near-coplanar windows"""
    X = [np.zeros(3), np.array([1.0, 0.0, 0.0])]
    X.append(X[1] + np.array([np.cos(1.2), np.sin(1.2), 0.0]))
    for _ in range(3, n):
        a, b_, c_ = X[-3], X[-2], X[-1]
        t = np.deg2rad(rng.uniform(*th))
        p = np.deg2rad(rng.uniform(*ph)) * rng.choice([-1, 1])
        bc = (c_ - b_) / np.linalg.norm(c_ - b_)
        nn = np.cross(b_ - a, bc)
        nn /= np.linalg.norm(nn)
        m = np.cross(nn, bc)
        d = np.array([-np.cos(t), np.sin(t) * np.cos(p), np.sin(t) * np.sin(p)])
        X.append(c_ + d[0] * bc + d[1] * m + d[2] * nn)
    return np.array(X[:n])


def torsion_chain(n, bond, theta_deg, torsions_deg):
    """chain with constant bond length and bond angle and a given list of n-3 torsion angles (degrees)"""
    th = np.deg2rad(theta_deg)
    X = [np.zeros(3), np.array([bond, 0.0, 0.0])]
    X.append(X[1] + bond * np.array([-np.cos(th), np.sin(th), 0.0]))
    for q in range(n - 3):
        a, b_, c_ = X[-3], X[-2], X[-1]
        p = np.deg2rad(torsions_deg[q])
        bc = (c_ - b_) / np.linalg.norm(c_ - b_)
        nn = np.cross(b_ - a, bc)
        nn /= np.linalg.norm(nn)
        m = np.cross(nn, bc)
        d = np.array([-np.cos(th), np.sin(th) * np.cos(p), np.sin(th) * np.sin(p)])
        X.append(c_ + bond * (d[0] * bc + d[1] * m + d[2] * nn))
    return np.array(X[:n])


# ----------------------------------------------------------------------------------------------------------------------
# the quantities of the note
# ----------------------------------------------------------------------------------------------------------------------
def sigma3(P):
    """third singular value of the centred matrix of the rows of P (thickness)"""
    Pc = P - P.mean(0)
    sv = np.linalg.svd(Pc, compute_uv=False)
    return sv[2] if len(sv) > 2 else 0.0


def chain_consts(X):
    n = len(X)
    tau = np.array([sigma3(X[i:i + 4]) for i in range(n - 3)])
    s = np.array([sigma3(X[i:i + 5]) for i in range(n - 4)])
    b = np.linalg.norm(np.diff(X, axis=0), axis=1).max()
    return tau, s, b


def pair_list(n, K=4):
    return [(j, k) for j in range(n) for k in range(j + 1, min(n, j + K + 1))]


def pair_arrays(n, K=4):
    pr = pair_list(n, K)
    J = np.array([p[0] for p in pr])
    Kk = np.array([p[1] for p in pr])
    return J, Kk


def eta_vec(X, Y, J, Kk):
    dy = Y[J] - Y[Kk]
    dx = X[J] - X[Kk]
    # (|dy|^2 - |dx|^2) computed as (dy - dx).(dy + dx): no cancellation of two large squares when Y is close to X
    return np.einsum("ij,ij->i", dy - dx, dy + dx)


def window_pair_index(n, J, Kk):
    """for each 5-point window i0 the indices (into the pair list) of its ten pairs"""
    idx = {(int(j), int(k)): q for q, (j, k) in enumerate(zip(J, Kk))}
    out = []
    for i in range(n - 4):
        out.append(np.array([idx[(p, q)] for p in range(i, i + 5) for q in range(p + 1, i + 5)]))
    return out


def procrustes(A, B):
    """R in O(3) (improper allowed) and t minimising ||B - A R - 1 t||_F; returns R, t, residual matrix"""
    ca, cb = A.mean(0), B.mean(0)
    A0, B0 = A - ca, B - cb
    U, S, Vt = np.linalg.svd(A0.T @ B0)
    R = U @ Vt
    t = cb - ca @ R
    return R, t, B - A @ R - t


def procrustes_proper(A, B):
    """the same with R restricted to SO(3) (used only for a control)"""
    ca, cb = A.mean(0), B.mean(0)
    A0, B0 = A - ca, B - cb
    U, S, Vt = np.linalg.svd(A0.T @ B0)
    D = np.diag([1.0, 1.0, np.sign(np.linalg.det(U @ Vt))])
    R = U @ D @ Vt
    t = cb - ca @ R
    return R, t, B - A @ R - t


def dP(X, Y):
    """min over all isometries g (proper and improper) of ||Y - gX||_F, computed from the aligned residual (no cancellation)"""
    return np.linalg.norm(procrustes(X, Y)[2])


def local_weights(X, tau=None, s=None):
    """matrix M (n x (n-4)) with  local_k = sum_j M[k, j] e_j  -- the right-hand side of (local) as a linear function of the
    window errors e_j;  M[k, j] = kappa/s_j * w_kj,  w_kj = [j = i(k)] + [j < i(k)] a_kj + [1 <= j <= i(k)] a_k,j-1,
    a_kj = |x_k - c_{j+1}| / tau_{j+1} + 1/2  (0-based: centroid of X[j+1:j+5], tau[j+1])."""
    n = len(X)
    if tau is None:
        tau, s, _ = chain_consts(X)
    cW = np.array([X[i:i + 4].mean(0) for i in range(n - 3)])          # centroid of W_{i+1}
    M = np.zeros((n, n - 4))
    for k in range(n):
        i = min(k, n - 5)
        M[k, i] += 1.0
        for j in range(i):                                             # j < i(k)
            a = np.linalg.norm(X[k] - cW[j + 1]) / tau[j + 1] + 0.5
            M[k, j] += a
            M[k, j + 1] += a
    return M * (KAPPA / s)[None, :]


def uniform_constant(X, consts=None):
    """C_L = 1.2 b (n+2)^2 / (s_* tau_*)"""
    tau, s, b = consts if consts is not None else chain_consts(X)
    n = len(X)
    return 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())


def half_jacobian(X, J, Kk):
    """the matrix A of Theorem L+: one row per pair, (x_j - x_k) in the block of j and its negative in the block of k"""
    n = len(X)
    A = np.zeros((len(J), 3 * n))
    d = X[J] - X[Kk]
    for q in range(len(J)):
        A[q, 3 * J[q]:3 * J[q] + 3] = d[q]
        A[q, 3 * Kk[q]:3 * Kk[q] + 3] = -d[q]
    return A


def mu_and_mode(X, J, Kk):
    """mu = (3n-6)-th singular value of A (the smallest non-zero one if the framework is infinitesimally rigid), the next one
    (should be ~0) and the corresponding right singular vector (softest mode, n x 3, unit Frobenius norm)"""
    n = len(X)
    A = half_jacobian(X, J, Kk)
    U, S, Vt = np.linalg.svd(A, full_matrices=True)
    S = np.concatenate([S, np.zeros(max(0, 3 * n - len(S)))])
    mu = S[3 * n - 7]
    nxt = S[3 * n - 6]
    V = Vt[3 * n - 7].reshape(n, 3)
    return mu, nxt, V, S


def band_laplacian_max(n, K=4):
    L = np.zeros((n, n))
    for j in range(n):
        for k in range(j + 1, min(n, j + K + 1)):
            L[j, j] += 1
            L[k, k] += 1
            L[j, k] -= 1
            L[k, j] -= 1
    return np.linalg.eigvalsh(L)[-1]
