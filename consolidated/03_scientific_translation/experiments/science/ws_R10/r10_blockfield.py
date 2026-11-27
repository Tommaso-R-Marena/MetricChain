"""r10_blockfield.py: a lower bound for F_inf(t) that works for ANY block length L (own
addition, not in Y_REPORT): Proposition I with the two labels "uniform field +h / -h on the
block", weights (1/2, 1/2).  Everything is a function of (first letter, last letter,
magnetisation of the block), whose joint law under the stationary L-marginal is computed by
a dynamic programme of size O(L^2).

    F_inf(t) >= [ G_t^(L) + Lambda_blk(t) ] / L,
    G_t^(L)  = t ln z - t ln E_{pi_L}[ cosh(t h m)^(1/t) ],   z = E_{pi_L} e^{h m},
    Lambda_blk(t) = moment Lyapunov exponent of order t of the product of the i.i.d. matrices
                    A_+- = B_+- rho0 (prob. 1/2 each),  B_+-(a,b) = E_{pi_L}[e^{+-h m}; first=a,last=b]/z,
    (lam_max(B_Q rho0) = 1 because the label law is symmetric under the global flip).
"""
import numpy as np
from r10_lyap import cheb_nodes, cheb_interp_matrix


def joint_first_last_m(L, p):
    """f[a, b, k] = P(first = a, last = b, m = k - L) for the stationary binary symmetric chain;
    letters 0 -> spin +1, 1 -> spin -1."""
    sp = np.array([1, -1])
    f = np.zeros((2, 2, 2 * L + 1))
    for a in (0, 1):
        f[a, a, L + sp[a]] = 0.5
    P = np.array([[1 - p, p], [p, 1 - p]])
    for _ in range(L - 1):
        g = np.zeros_like(f)
        for b2 in (0, 1):
            for b in (0, 1):
                shifted = np.roll(f[:, b, :], sp[b2], axis=1)
                g[:, b2, :] += P[b, b2] * shifted
        f = g
    return f


def mom_lyap2(A_list, weights, t, N=48):
    wn, xn = cheb_nodes(N, 0.0, 1.0)
    T = np.zeros((N, N))
    for A, m in zip(A_list, weights):
        y0 = wn * A[0, 0] + (1 - wn) * A[1, 0]
        y1 = wn * A[0, 1] + (1 - wn) * A[1, 1]
        g = y0 + y1
        T += m * (g ** t)[:, None] * cheb_interp_matrix(xn, np.clip(2 * y0 / g - 1, -1, 1))
    return float(np.log(np.max(np.linalg.eigvals(T).real)))


def blockfield_bound(p, u, L, t, f=None, N=48):
    """Lower bound for F_inf(t) per site from uniform +-h fields on blocks of length L."""
    h = u / 2
    if f is None:
        f = joint_first_last_m(L, p)
    m = np.arange(-L, L + 1).astype(float)
    # work with logs to avoid overflow
    lz = np.log((f * np.exp(h * m - h * L)[None, None, :]).sum()) + h * L
    lc = (1 / t) * (np.logaddexp(t * h * m, -t * h * m) - np.log(2))        # ln cosh(t h m)^(1/t)
    lE = np.log((f * np.exp(lc - lc.max())[None, None, :]).sum()) + lc.max()
    G = t * lz - t * lE
    Bp = (f * np.exp(h * m - h * L)[None, None, :]).sum(axis=2) * np.exp(h * L - lz)
    Bm = (f * np.exp(-h * m - h * L)[None, None, :]).sum(axis=2) * np.exp(h * L - lz)
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    Lam = mom_lyap2([Bp @ rho0, Bm @ rho0], [0.5, 0.5], t, N)
    return (G + Lam) / L, G / L, Lam / L


def best_blockfield(p, u, tgrid=None, Lmax=None):
    """max over L and t of the bound; returns (value, L, t)."""
    from r10lib import golden_max
    K = np.log((1 - p) / p)
    Lmax = Lmax or int(min(600, max(12, 8 * K / u + 12)))
    best = (-1.0, None, None)
    fs = {}
    for L in range(1, Lmax + 1):
        fs[L] = joint_first_last_m(L, p)
        tb, vb = golden_max(lambda t: blockfield_bound(p, u, L, t, fs[L])[0], 0.05, 0.95, tol=1e-4)
        if vb > best[0]:
            best = (vb, L, tb)
    return best
