"""Numerical check of the lifting identity of CHAIN_GEOMETRY_HARDNESS.md, section 2a.

For a graph H with n vertices and maximum degree Delta, k >= 1 and L >= 4.5 (k+1) Delta let H' be the graph with
clusters  U_v (3 copies, v in V),  Z_l (4 copies, l = 1..L),  R_{v,l} (5 copies),  and all edges between
U_v and U_w (vw in E),  U_v and Z_l,  R_{v,l} and U_v,  R_{v,l} and Z_l.   Claim:

        OPT_{k+1}(H')  =  25 n L  +  9 OPT_k(H),        OPT_k(G) = max over unit vectors in R^k of  - sum_{ij in E} <x_i, x_j>.

The STATEMENT (vector Max-Cut is NP-hard in every fixed dimension) is known: Kallaugher, Parekh, Thompson, Wang,
Yirka (arXiv:2401.06725) for k = 3 and Piddock (arXiv:2510.07995) for every k.  This file only checks our short
derivation.  Nothing here is a proof: (1) is an exact check of a polynomial inequality on a grid, (2)-(5) are
numerical maximisations from random starts, which can only fail to find a violation.
"""
import itertools, math, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import minimize

RNG = np.random.default_rng(20261126)


# ---------------------------------------------------------------- (1) the gadget inequality
def check_gadget():
    """g(t) = 5 sqrt(25+24t) - 12 t <= 25 - t^2 on [-1,1]  <=>  t^2 (94 - 24 t + t^2) >= 0  (after squaring;
    25 + 12 t - t^2 >= 12 > 0 on [-1,1])."""
    ok = True
    for i in range(-1000, 1001):
        t = Fraction(i, 1000)
        ok &= (25 + 12 * t - t * t) >= 12
        ok &= (25 + 12 * t - t * t) ** 2 - 25 * (25 + 24 * t) == t * t * (94 - 24 * t + t * t)
        ok &= t * t * (94 - 24 * t + t * t) >= 0
        ok &= (t == 0) == (t * t * (94 - 24 * t + t * t) == 0)
    worst = max(5 * math.sqrt(25 + 24 * t) - 12 * t - (25 - t * t) for t in np.linspace(-1, 1, 20001))
    return ok, worst


def g(t):
    return 5.0 * np.sqrt(25.0 + 24.0 * t) - 12.0 * t


def dg(t):
    return 60.0 / np.sqrt(25.0 + 24.0 * t) - 12.0


# ---------------------------------------------------------------- generic maximiser on products of spheres
def maximise(fun_grad, shape, starts, x0s=()):
    """fun_grad(X) -> (value, gradient wrt X) for X of the given shape with unit rows; returns the best value."""
    def wrapped(y):
        Y = y.reshape(shape)
        nrm = np.linalg.norm(Y, axis=1, keepdims=True)
        X = Y / nrm
        val, G = fun_grad(X)
        G = (G - np.sum(G * X, axis=1, keepdims=True) * X) / nrm
        return -val, -G.ravel()
    best, bestX = -np.inf, None
    inits = [np.asarray(x0, float) for x0 in x0s] + [RNG.normal(size=shape) for _ in range(starts)]
    for Y0 in inits:
        res = minimize(wrapped, Y0.ravel(), jac=True, method="L-BFGS-B", options={"maxiter": 20000, "ftol": 1e-15, "gtol": 1e-10})
        if -res.fun > best:
            Y = res.x.reshape(shape)
            best, bestX = -res.fun, Y / np.linalg.norm(Y, axis=1, keepdims=True)
    return best, bestX


def adjacency(n, edges):
    A = np.zeros((n, n))
    for i, j in edges:
        assert i != j and A[i, j] == 0, "not a simple graph"
        A[i, j] = A[j, i] = 1
    return A


def opt_k(n, edges, k, starts=200):
    """OPT_k of an unweighted graph: exact for k = 1 (all sign vectors), numerical otherwise."""
    if k == 1:
        return max(-sum(s[i] * s[j] for i, j in edges) for s in itertools.product((1, -1), repeat=n)), None
    A = adjacency(n, edges)
    return maximise(lambda X: (-0.5 * np.sum(X * (A @ X)), -(A @ X)), (n, k), starts)


# ---------------------------------------------------------------- the reduced objective of the lifted instance
def lifted(n, edges, L):
    A = adjacency(n, edges)

    def fun_grad(X):                      # rows 0..n-1: u_v ; rows n..n+L-1: z_l   (the R-spins are maximised out)
        U, Z = X[:n], X[n:]
        T = U @ Z.T
        val = -4.5 * np.sum(U * (A @ U)) + np.sum(g(T))          # -9 sum_E <u_v,u_w> + sum g
        D = dg(T)
        return val, np.vstack([-9.0 * (A @ U) + D @ Z, D.T @ U])
    return fun_grad


def structured_start(n, k, L, Xopt):
    """u_v = (optimal vector of H in R^k, 0), z_l = e_{k+1}."""
    X = np.zeros((n + L, k + 1))
    X[:n, :k] = Xopt
    X[n:, k] = 1.0
    return X


def check_lifting(name, n, edges, k, L=None, starts=40):
    deg = [sum(1 for e in edges if v in e) for v in range(n)]
    Lmin = math.ceil(4.5 * (k + 1) * max(deg))
    if L is None:
        L = Lmin
    base, Xopt = opt_k(n, edges, k)
    if k == 1:                             # an optimal sign vector
        s = max(itertools.product((1, -1), repeat=n), key=lambda s: -sum(s[i] * s[j] for i, j in edges))
        Xopt = np.array(s, float).reshape(n, 1)
    target = 25 * n * L + 9 * base
    fg = lifted(n, edges, L)
    at_structured = fg(structured_start(n, k, L, Xopt))[0]
    best, _ = maximise(fg, (n + L, k + 1), starts, x0s=[structured_start(n, k, L, Xopt) + 0.05 * RNG.normal(size=(n + L, k + 1))])
    ok_formula = abs(at_structured - target) < 1e-6
    ok_upper = best <= target + 1e-5
    print(f"   {name:8s} k={k}->{k+1}  L={L:3d} (bound {Lmin:3d})  OPT_k(H)={base:9.6f}  target={target:12.6f}  "
          f"structured={at_structured:12.6f}  best of {starts + 1} maximisations={best:12.6f}  "
          f"{'formula attained' if ok_formula else 'FORMULA NOT ATTAINED'}; {'never exceeded' if ok_upper else 'EXCEEDED'}", flush=True)
    return ok_formula, ok_upper, best - target


# ---------------------------------------------------------------- the explicit unweighted graph H'
def explicit_graph(n, edges, L):
    idx, clusters = 0, {}
    for v in range(n):
        clusters[("U", v)] = list(range(idx, idx + 3)); idx += 3
    for l in range(L):
        clusters[("Z", l)] = list(range(idx, idx + 4)); idx += 4
    for v in range(n):
        for l in range(L):
            clusters[("R", v, l)] = list(range(idx, idx + 5)); idx += 5
    E = []
    def join(a, b):
        E.extend((i, j) for i in clusters[a] for j in clusters[b])
    for v, w in edges:
        join(("U", v), ("U", w))
    for v in range(n):
        for l in range(L):
            join(("U", v), ("Z", l)); join(("R", v, l), ("U", v)); join(("R", v, l), ("Z", l))
    return idx, E


def check_explicit(name, n, edges, k, starts=8):
    deg = [sum(1 for e in edges if v in e) for v in range(n)]
    L = math.ceil(4.5 * (k + 1) * max(deg))
    base, _ = opt_k(n, edges, k)
    N, E = explicit_graph(n, edges, L)
    A = adjacency(N, E)                                            # asserts that H' is a simple graph
    target = 25 * n * L + 9 * base
    best, _ = maximise(lambda X: (-0.5 * np.sum(X * (A @ X)), -(A @ X)), (N, k + 1), starts)
    ok = abs(best - target) < 1e-4
    print(f"   {name:8s} k={k}->{k+1}  H' is a simple graph with {N} vertices and {len(E)} edges (L={L});  "
          f"target={target:.6f}  best of {starts} maximisations over all {N} unit vectors={best:.6f}  {'OK' if ok else 'MISMATCH'}", flush=True)
    return ok


GRAPHS = {
    "K2": (2, [(0, 1)]),
    "P3": (3, [(0, 1), (1, 2)]),
    "K3": (3, [(0, 1), (1, 2), (0, 2)]),
    "C5": (5, [(i, (i + 1) % 5) for i in range(5)]),
    "K4": (4, [(i, j) for i in range(4) for j in range(i + 1, 4)]),
    "K4-e": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]),
}

if __name__ == "__main__":
    allok = True
    ok, worst = check_gadget()
    print(f"(1) gadget inequality g(t) <= 25 - t^2 (exact on a grid of 2001 rationals): {ok};  max of g(t) - (25 - t^2) on a float grid: {worst:.3e}")
    allok &= ok and worst <= 1e-12

    print("(2) lifting from k = 1 (Max-Cut) to k = 2:")
    for name in ("K2", "P3", "K3", "C5", "K4", "K4-e"):
        a, b, _ = check_lifting(name, *GRAPHS[name], 1)
        allok &= a and b
    print("(3) lifting from k = 2 to k = 3 and from k = 3 to k = 4:")
    for name, k in (("K3", 2), ("C5", 2), ("K4", 2), ("K4", 3), ("C5", 3)):
        a, b, _ = check_lifting(name, *GRAPHS[name], k, starts=25)
        allok &= a and b
    print("(4) power of the test: with too few poles the identity must fail where OPT_2(H) > OPT_1(H):")
    for name, L in (("K3", 1), ("C5", 1), ("K3", 2)):
        a, b, excess = check_lifting(name, *GRAPHS[name], 1, L=L, starts=25)
        print(f"        excess over the formula: {excess:.6f}  ({'violation detected, as expected' if excess > 1e-3 else 'no violation found'})")
    print("(5) the explicit unweighted graph H' (no assumption that copies in a cluster are equal):")
    for name, k in (("K2", 1), ("K3", 1), ("K3", 2)):
        allok &= check_explicit(name, *GRAPHS[name], k)
    print("ALL OK" if allok else "SOME CHECK FAILED")
    sys.exit(0 if allok else 1)
