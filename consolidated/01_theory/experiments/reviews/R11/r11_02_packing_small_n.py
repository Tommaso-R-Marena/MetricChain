"""R11 / 02 -- a sanity check of the headline that does not use the report's game-function machinery:
hard packing / indistinguishability (Theorem 11.22(c) [V]) by exact enumeration at small n.

For an instance g in C_d and admissible alternatives g_j in C_d with ln A(g_j) - ln A(g) > eps,
every (eps/2, delta)-correct algorithm satisfies  E|Q(g)| >= (1 - 2 delta) * V,
   V = max { sum_j w_j : w >= 0, sum_j w_j 1[x in D_j] <= 1 for all x },   D_j = {g_j != g}
(the fractional packing number of the difference sets).  Everything below is computed from the
definitions on the full configuration space: membership of g and of every g_j in the class (all
edges), the gain in ln A, the difference sets, and the LP (scipy/HiGHS).

Product reference (uniform cube): g = 0, dips of depth u(k+1) at every centre; V = 2^n/|B(k*)|
(closed form; reproduced by the same code path at n = 10).
Markov reference: g = gamma*(M) = soft minimum of the cones u*d(., sigma) around DOMAIN-LIKE
centres sigma (at most 2 walls; all centres for n = 10), alternatives g_sigma = min(g, cone_sigma - const)
with the smallest depth whose gain exceeds eps.  Also: the zero residual with plain dips.

Run:  python3 r11_02_packing_small_n.py        (about 3-5 minutes)
"""
import sys, time
from math import comb
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from r11lib import *

T0 = time.time()
u = 1.0
h = u / 2


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def cube_closed_form(n, eps):
    """k* = least k with Delta_k > eps;  V = 2^n / |B(k*)|  (Theorem 11.25(a))."""
    for k in range(n + 1):
        tot = sum(comb(n, j) * (np.exp(u * (k + 1 - j)) - 1) for j in range(k + 1))
        if np.log1p(tot / 2 ** n) > eps:
            return k, 2 ** n / sum(comb(n, j) for j in range(k + 1))
    return n, 1.0


def packing_lp(member):
    """member: boolean (alternatives x points).  Returns the LP value."""
    na, N = member.shape
    cols = np.unique(member, axis=1)                    # identical constraints removed
    A = csr_matrix(cols.T.astype(float))                # constraints x variables
    res = linprog(-np.ones(na), A_ub=A, b_ub=np.ones(A.shape[0]), bounds=(0, None), method='highs')
    assert res.status == 0, res.message
    return -res.fun


def study(n, p, eps, centres, instance='softmin', t=0.43, check_members=True):
    s, pi = chain_law(n, p)
    logpi = np.log(pi)
    sf = s.T.astype(float)
    phis = -h * centres.astype(float) @ sf               # cones u d(., sigma) up to constants
    lnZ = logsumexp(logpi[None, :] - phis, axis=1)
    phit = phis + lnZ[:, None]                           # normalised: E_pi e^{-phi~} = 1
    logP = logpi[None, :] - phit
    if instance == 'softmin':
        lo, up, M = maximise_G_fast(logP, t)
        lq = centre_of_M(logP, M, t)
        g = logpi - lq                                   # gamma~*
    else:
        M = np.full(centres.shape[0], 1.0 / centres.shape[0])
        g = np.zeros(2 ** n)
        lo = np.nan
    slopes = [u] * n
    viol_g = is_lipschitz(g, n, slopes) if check_members else np.nan
    lnA0 = logsumexp(logpi - g)
    member = np.zeros((centres.shape[0], 2 ** n), dtype=bool)
    worst = -np.inf
    mingain = np.inf
    for a in range(centres.shape[0]):
        Phi = phit[a] - g
        # gain(r) = ln E_{pi_g} exp((r - Phi)_+): find r0 with gain(r0) = eps by bisection
        w = np.exp(logpi - g - lnA0)
        f = lambda r: np.log((w * np.exp(np.maximum(r - Phi, 0.0))).sum())
        lo_r, hi_r = Phi.min(), Phi.max() + eps + 1.0
        for _ in range(100):
            mid = 0.5 * (lo_r + hi_r)
            if f(mid) > eps:
                hi_r = mid
            else:
                lo_r = mid
        r = hi_r                                         # gain(r) > eps
        alt = g - np.maximum(r - Phi, 0.0)
        if check_members:
            worst = max(worst, is_lipschitz(alt, n, slopes))
        mingain = min(mingain, logsumexp(logpi - alt) - lnA0)
        member[a] = alt < g - 1e-13
    V = packing_lp(member)
    Vm = 1.0 / (M @ member).max()                        # feasible solution w = M / max load
    return dict(V=V, Vm=Vm, viol_g=viol_g, viol_alt=worst, mingain=mingain, G=lo,
                sizes=(member.sum(axis=1).min(), member.sum(axis=1).max()))


print("== validation of the code path on the uniform cube (n = 10, all 1024 centres, g = 0) ==")
for eps in (0.25, 0.5, 1.0):
    k, V = cube_closed_form(10, eps)
    d = study(10, 0.5, eps, configs(10), instance='zero')
    print(f"eps={eps}: closed form k* = {k}, 2^n/|B(k*)| = {V:.4f};  enumeration + LP: V = {d['V']:.4f}  (|D| = {d['sizes']}, members ok: {max(d['viol_g'], d['viol_alt']) < 1e-9}, min gain {d['mingain']:.4f})")

print("\n== Markov reference against the uniform cube, same n, u = 1, same eps ==")
print("columns: V = fractional packing number (E|Q| >= (1-2 delta) V);  cube: closed form with ALL centres (its optimum);")
print("         Markov: soft-min instance, domain-like centres only (a restriction, so V is a valid but not optimal bound)")
for n in (10, 12, 14, 16):
    cen = configs(n) if n <= 10 else walls_labels(n, 2)
    for eps in (0.25, 0.5, 1.0):
        k, Vc = cube_closed_form(n, eps)
        line = f"n={n:2d} eps={eps:4.2f}: cube V = {Vc:8.4f} (k*={k})"
        for p in (0.4, 0.3):
            d = study(n, p, eps, cen, instance='softmin', check_members=(n <= 14))
            ok = "" if n > 14 else f", members ok: {max(d['viol_g'], d['viol_alt']) < 1e-9}"
            line += f" | p={p}: V = {d['V']:8.4f} (min gain {d['mingain']:.3f}{ok})"
            if n <= 12:
                d0 = study(n, p, eps, cen, instance='zero', check_members=False)
                line += f", zero residual: V = {d0['V']:7.4f}"
        print(line + f"   [{time.time()-T0:.0f} s]", flush=True)
print(f"{time.time()-T0:.1f} s")
