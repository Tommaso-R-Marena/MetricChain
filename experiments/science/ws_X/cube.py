"""Workstream X — core library for functions on the Boolean cube F_2^n.

Conventions
-----------
* A configuration x in {0,1}^n is an integer bitmask (bit i = x_i); a subset S of sites likewise.
* Walsh character  chi_S(x) = (-1)^{popcount(S & x)}.
* Every g : X -> R is  g(x) = sum_S ghat_S chi_S(x),  ghat = fwht(g) / 2^n,  g = fwht(ghat).
* A *spectrum* is an array v[S] >= 0.  Kernel  k(x,y) = sum_S v_S chi_S(x xor y) = fwht(v)[x xor y].
  Gaussian prior: ghat_S ~ N(0, v_S) independent.   RKHS norm: ||g||^2 = sum_S ghat_S^2 / v_S.
* A *linear design* is A = rowspace(H) (H an r x n binary matrix given as r bitmasks);
  its annihilator is the code C = {c : <h,c> = 0 for all rows h}.  Two frequencies U, U' are
  aliased on A iff they have the same syndrome  syn(U) = (parity(U & h_j))_j.
"""
from __future__ import annotations

import itertools
import math

import numpy as np


# ----------------------------------------------------------------------------- basics
def popcount(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.uint64)
    c = np.zeros(a.shape, dtype=np.int64)
    while True:
        nz = a != 0
        if not nz.any():
            break
        c += (a & np.uint64(1)).astype(np.int64)
        a = a >> np.uint64(1)
    return c


def weights(n: int) -> np.ndarray:
    """|S| for every bitmask S < 2^n."""
    w = np.zeros(1, dtype=np.int64)
    for _ in range(n):
        w = np.concatenate([w, w + 1])
    return w


def fwht(a: np.ndarray) -> np.ndarray:
    """Unnormalised Walsh-Hadamard transform: out[S] = sum_x a[x] chi_S(x)."""
    a = np.array(a, dtype=float)
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(-1, 2, h)
        a = np.stack([a[:, 0, :] + a[:, 1, :], a[:, 0, :] - a[:, 1, :]], axis=1)
        a = a.reshape(N)
        h *= 2
    return a


def chi(S, x) -> np.ndarray:
    return 1 - 2 * (popcount(np.bitwise_and(np.asarray(S, dtype=np.uint64),
                                            np.asarray(x, dtype=np.uint64))) & 1)


# ----------------------------------------------------------------------------- spectra
def iso_spectrum(n: int, sigma2_by_order) -> np.ndarray:
    """Isotropic spectrum with total variance sigma2_by_order[m] at interaction order m."""
    w = weights(n)
    v = np.zeros(1 << n)
    for m, s2 in enumerate(sigma2_by_order):
        if m <= n and s2 > 0:
            v[w == m] = s2 / math.comb(n, m)
    return v


def product_spectrum(n: int, sigma2: float, rho) -> np.ndarray:
    """Spectrum of k(x,y) = sigma2 * prod_i rho_i^{[x_i != y_i]} (rho scalar or length n)."""
    rho = np.broadcast_to(np.asarray(rho, dtype=float), (n,))
    v = np.array([sigma2])
    for i in range(n):
        a, b = (1 + rho[i]) / 2, (1 - rho[i]) / 2
        v = np.concatenate([v * a, v * b])
    return v


def sample_gp(v: np.ndarray, rng) -> np.ndarray:
    ghat = rng.standard_normal(v.shape[0]) * np.sqrt(v)
    return fwht(ghat)


def rkhs_norm2(g: np.ndarray, v: np.ndarray) -> float:
    ghat = fwht(g) / g.shape[0]
    bad = (v == 0) & (np.abs(ghat) > 1e-9)
    if bad.any():
        return math.inf
    ok = v > 0
    return float(np.sum(ghat[ok] ** 2 / v[ok]))


# ----------------------------------------------------------------------------- linear designs
def span(rows, n: int) -> np.ndarray:
    """All elements of the F_2-span of the bitmask rows (sorted, unique)."""
    pts = np.zeros(1, dtype=np.int64)
    for h in rows:
        if not np.any(pts == h):  # h not yet in span  (span is closed, so test membership)
            pts = np.concatenate([pts, pts ^ h])
    return np.sort(pts)


def syndromes(rows, n: int) -> np.ndarray:
    """syn[U] in [0, 2^r) for every U < 2^n (r = len(rows))."""
    U = np.arange(1 << n, dtype=np.uint64)
    syn = np.zeros(1 << n, dtype=np.int64)
    for j, h in enumerate(rows):
        syn |= (popcount(U & np.uint64(h)) & 1) << j
    return syn


def gf2_rank(rows) -> int:
    rows = list(rows)
    rank = 0
    while rows:
        piv = rows.pop()
        if piv == 0:
            continue
        rank += 1
        low = piv & -piv
        rows = [r ^ piv if r & low else r for r in rows]
    return rank


_PRIM = {1: 0b11, 2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101, 6: 0b1000011, 7: 0b10000011,
         8: 0b100011101}


def gf_pow_table(r: int):
    """alpha^i for i = 0 .. 2^r - 2 in GF(2^r) (elements as r-bit integers)."""
    poly = _PRIM[r]
    out, x = [], 1
    for _ in range((1 << r) - 1):
        out.append(x)
        x <<= 1
        if x >> r:
            x ^= poly
    return out


def bch_rows(n: int, m: int):
    """Parity-check rows (as n-bit masks) of a (shortened) narrow-sense binary BCH code of
    designed distance 2m+1 and length n: column i is (alpha^i, alpha^{3i}, ..., alpha^{(2m-1)i}).
    The design A = rowspace has at most 2^{m r} points, r = ceil(log2(n+1))."""
    if m == 0:
        return []
    r = max(1, math.ceil(math.log2(n + 1)))
    tab = gf_pow_table(r)
    q = (1 << r) - 1
    rows = []
    for j in range(m):
        e = 2 * j + 1
        for bit in range(r):
            mask = 0
            for i in range(n):
                if (tab[(e * i) % q] >> bit) & 1:
                    mask |= 1 << i
            rows.append(mask)
    return rows


def min_distance_at_least(rows, n: int, d: int) -> bool:
    """True iff no nonzero U with |U| < d has zero syndrome (brute force over small weights)."""
    for w in range(1, d):
        for comb in itertools.combinations(range(n), w):
            U = 0
            for i in comb:
                U |= 1 << i
            if all((bin(U & h).count("1") & 1) == 0 for h in rows):
                return False
    return True


# ----------------------------------------------------------------------------- posterior, direct
def kernel_matrix(v: np.ndarray, pts_a, pts_b) -> np.ndarray:
    kap = fwht(v)
    a = np.asarray(pts_a, dtype=np.int64)[:, None]
    b = np.asarray(pts_b, dtype=np.int64)[None, :]
    return kap[a ^ b]


def posterior_direct(v: np.ndarray, A, y=None, jitter: float = 0.0):
    """Posterior mean (if y given) and variance on the whole cube by dense linear algebra.
    Uses a pseudo-inverse, so singular K_AA (rank-deficient priors) are allowed."""
    N = v.shape[0]
    allx = np.arange(N)
    KA = kernel_matrix(v, A, A)
    KxA = kernel_matrix(v, allx, A)
    KAinv = np.linalg.pinv(KA + jitter * np.eye(len(A)), hermitian=True)
    W = KxA @ KAinv                       # prediction weights lambda_a(x)
    var = fwht(v)[0] - np.einsum("xa,xa->x", W, KxA)
    mean = None if y is None else W @ np.asarray(y)
    return mean, np.maximum(var, 0.0), W


def posterior_cov_direct(v: np.ndarray, A) -> np.ndarray:
    N = v.shape[0]
    allx = np.arange(N)
    K = kernel_matrix(v, allx, allx)
    KA = kernel_matrix(v, A, A)
    KxA = K[:, np.asarray(A)]
    return K - KxA @ np.linalg.pinv(KA, hermitian=True) @ KxA.T


# ----------------------------------------------------------------------------- posterior, cosets
def posterior_linear(v: np.ndarray, rows, n: int, g=None):
    """Posterior on the whole cube for the linear design A = rowspace(rows), by aliasing classes.

    Returns (mean or None, var, info) where var[x] = sum_T [V_T - (sum_{U in T} v_U chi_U(x))^2 / V_T]
    and info has the non-leader mass  NL = sum_T (V_T - max_{U in T} v_U).
    Cost: (number of cosets) FWHTs of size 2^n.
    """
    size = 1 << n
    syn = syndromes(rows, n)
    ncos = 1 << len(rows)
    V = np.bincount(syn, weights=v, minlength=ncos)
    vmax = np.zeros(ncos)
    np.maximum.at(vmax, syn, v)
    NL = float(np.sum(V - vmax))
    var = np.full(size, float(v.sum()))
    mean = None
    if g is not None:
        ghat = fwht(g) / size
        G = np.bincount(syn, weights=ghat, minlength=ncos)   # aliased sums: what the data determine
        mean_hat = np.zeros(size)
    for T in range(ncos):
        if V[T] <= 0:
            continue
        sel = syn == T
        vT = np.where(sel, v, 0.0)
        sT = fwht(vT)                                   # x -> sum_{U in T} v_U chi_U(x)
        var -= sT ** 2 / V[T]
        if g is not None:
            mean_hat += np.where(sel, v * (G[T] / V[T]), 0.0)
    if g is not None:
        mean = fwht(mean_hat)
    return mean, np.maximum(var, 0.0), {"NL": NL, "V": V, "vmax": vmax, "ncosets": ncos}


def non_leader_mass(v: np.ndarray, rows, n: int) -> float:
    syn = syndromes(rows, n)
    ncos = 1 << len(rows)
    V = np.bincount(syn, weights=v, minlength=ncos)
    vmax = np.zeros(ncos)
    np.maximum.at(vmax, syn, v)
    return float(np.sum(V - vmax))


def eig_tail(v: np.ndarray, N: int) -> float:
    """Sum of all but the N largest eigenvalues of the covariance operator (= entries of v)."""
    s = np.sort(v)[::-1]
    return float(s[N:].sum())


# ----------------------------------------------------------------------------- functionals
def logZ(E: np.ndarray, beta: float) -> float:
    """ln( 2^{-n} sum_x exp(-beta E(x)) )  (uniform reference measure)."""
    a = -beta * E
    mx = a.max()
    return float(mx + np.log(np.mean(np.exp(a - mx))))
