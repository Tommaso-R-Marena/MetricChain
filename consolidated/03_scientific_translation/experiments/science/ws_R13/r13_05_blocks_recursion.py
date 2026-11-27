#!/usr/bin/env python3
"""R13 / item 2, section 11.32: the theory division's addition "with blocks of ONE site the recursion does not show
the reversal" -- own code, written from the statement of Theorem 11.116(d) and the Setting of section 11.32 of the
theory report at 63e36f7 (no file of experiments/workstreams/Y, of the harness, or of our ws_R10 was opened or imported).

Statement used.  Symmetric binary chain, flip probability p, Hamming envelope of slope u.  For blocks of L sites
    F_inf(t) <= (1/L) max_b F*[ P^(L)(.|b) ; (u, ..., u, u*) ](t),   u* = u + ln[((1-p)e^{u*} + p)/(p e^{u*} + 1 - p)],
where for a finite space (X, pi, d)
    F*_X(t) = max_M  -t ln sum_x ( sum_phi M(phi) pi_phi(x)^t )^{1/t} = min_Q max_phi (1-t) D_t(pi_phi || Q),
pi_phi ~ pi e^{-phi}, M a law on the vertices of the class {psi: psi(x)-psi(y) <= d(x,y)};  a_X = lim_{t->1} F*_X(t)/(1-t)
(= the Shannon capacity of the channel phi -> pi_phi), h_X = max_t F*_X(t).  Hence
    a_inf <= C_L/L,   h_inf <= max_t F*_L(t)/L.
The cube: a = KL(p_u||1/2), h = KL(Lam1/u||1/2).

What this script does.
 * vertices of the class of a weighted cube (slopes w_1..w_L): every vertex has a spanning tree of tight edge
   constraints (the edge constraints generate all others because the weighted Hamming distance is a path metric),
   so the vertices are the feasible functions among {spanning tree of Q_L} x {signs}.  L <= 3.
 * Shannon capacity by Blahut-Arimoto with the dual bound max_phi KL(pi_phi||Q)  (bracket printed);
 * F*(t): minimise the convex function M -> sum_x (sum_phi M pi_phi^t)^{1/t} by exponentiated-gradient steps; the
   bracket is [G_t(M), max_phi (1-t) D_t(pi_phi||Q_M)] with Q_M the Sibson centre  (both ends printed for max over t);
   max over t on a grid: the LOWER end of h is the grid maximum of certified lower values, the UPPER end is NOT
   certified between grid points (stated in the output; t-grid step 0.005 plus local refinement).
 * controls: p = 1/2 reproduces the cube (L = 1 and L = 3); u* at u = 1 against the four values printed in the report.

Usage: python3 r13_05_blocks_recursion.py
"""
import itertools, math, sys
import numpy as np


def kl2(r, q):
    return r * math.log(r / q) + (1 - r) * math.log((1 - r) / (1 - q))


def cube_a_h(u):
    p = 1 / (1 + math.exp(u))
    lam = math.log(2 / (1 + math.exp(-u)))
    return kl2(p, 0.5), kl2(lam / u, 0.5)


def ustar(u, p):
    x = u
    for _ in range(100000):
        xn = u + math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))
        if abs(xn - x) < 1e-15:
            break
        x = xn
    return xn


def vertices(L, w):
    """vertices (normalised psi(0..0) = 0) of {psi on {0,1}^L : |psi(x)-psi(y)| <= w_i for x,y differing in site i}."""
    X = list(itertools.product((0, 1), repeat=L))
    idx = {x: i for i, x in enumerate(X)}
    edges = []
    for x in X:
        for i in range(L):
            if x[i] == 0:
                y = x[:i] + (1,) + x[i + 1:]
                edges.append((idx[x], idx[y], w[i]))
    n = len(X)
    found = {}
    for tree in itertools.combinations(range(len(edges)), n - 1):
        # spanning tree test by union-find
        par = list(range(n))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        ok = True
        for e in tree:
            a, b = find(edges[e][0]), find(edges[e][1])
            if a == b:
                ok = False
                break
            par[a] = b
        if not ok:
            continue
        adj = {i: [] for i in range(n)}
        for e in tree:
            a, b, ww = edges[e]
            adj[a].append((b, ww, e))
            adj[b].append((a, ww, e))
        order = [(0, None)]
        seen = {0}
        steps = []                       # (child, parent, weight, position in tree)
        pos = {e: j for j, e in enumerate(tree)}
        q = [0]
        while q:
            a = q.pop()
            for b, ww, e in adj[a]:
                if b not in seen:
                    seen.add(b)
                    steps.append((b, a, ww, pos[e]))
                    q.append(b)
        for signs in itertools.product((1.0, -1.0), repeat=n - 1):
            psi = [0.0] * n
            for b, a, ww, j in steps:
                psi[b] = psi[a] + signs[j] * ww
            if all(abs(psi[a] - psi[b]) <= ww + 1e-12 for a, b, ww in edges):
                key = tuple(round(v, 9) for v in psi)
                found[key] = psi
    return X, np.array(list(found.values()))


def block_law(L, p, b):
    X = list(itertools.product((0, 1), repeat=L))
    pr = []
    for x in X:
        prev, v = b, 1.0
        for s in x:
            v *= (p if s != prev else 1 - p)
            prev = s
        pr.append(v)
    return np.array(pr)


def channel(L, p, u, b=0):
    us = ustar(u, p)
    w = [u] * (L - 1) + [us]
    X, V = vertices(L, w)
    pi = block_law(L, p, b)
    W = pi[None, :] * np.exp(-V)
    W /= W.sum(axis=1, keepdims=True)
    return W, us, len(V)


def capacity(W, iters=200000, tol=1e-12):
    m = np.full(W.shape[0], 1.0 / W.shape[0])
    logW = np.log(W)
    for it in range(iters):
        Q = m @ W
        D = (W * (logW - np.log(Q)[None, :])).sum(axis=1)   # KL(pi_phi || Q)
        lo, hi = float(m @ D), float(D.max())
        if hi - lo < tol:
            break
        m = m * np.exp(D - D.max())
        m /= m.sum()
    return lo, hi


def Fstar(W, t, iters=20000, tol=1e-11, m0=None):
    """bracket [lo, hi] of F*(t) = max_M G_t(M) = min_Q max_phi (1-t) D_t(pi_phi||Q)."""
    Wt = W ** t
    m = np.full(W.shape[0], 1.0 / W.shape[0]) if m0 is None else m0.copy()
    lo_best, hi_best = -np.inf, np.inf
    for it in range(iters):
        s = m @ Wt                               # sum_phi M pi_phi^t, per x
        S = float((s ** (1.0 / t)).sum())
        lo = -t * math.log(S)                    # G_t(M)
        Q = s ** (1.0 / t) / S                   # Sibson centre
        # (1-t) D_t(pi_phi||Q) = -ln sum_x pi_phi^t Q^{1-t}
        val = -np.log(Wt @ (Q ** (1.0 - t)))
        hi = float(val.max())
        lo_best, hi_best = max(lo_best, lo), min(hi_best, hi)
        if hi_best - lo_best < tol:
            break
        m = m * np.exp((val - val.max()) / (1.0 - t) * 0.5) if t < 0.9 else m * np.exp((val - val.max()) * 5.0)
        m /= m.sum()
    return lo_best, hi_best, m


def h_bracket(W, tgrid):
    best = (-1.0, None, None)
    m = None
    for t in tgrid:
        lo, hi, m = Fstar(W, float(t), m0=m)
        if lo > best[0]:
            best = (lo, hi, float(t))
    return best


if __name__ == '__main__':
    print("# r13_05_blocks_recursion.py")
    print("## controls")
    for p, want in ((0.4, 1.218), (0.3, 1.526), (0.2, 1.981), (0.1, 2.750)):
        print(f"   u*(u=1, p={p}) = {ustar(1.0, p):.4f}   (report: {want})")
    for u in (1.0, 3.0):
        a_c, h_c = cube_a_h(u)
        for L in (1, 3):
            W, us, nv = channel(L, 0.5, u)
            clo, chi = capacity(W)
            hb = h_bracket(W, np.arange(0.02, 0.99, 0.02))
            print(f"   p=1/2, u={u}, L={L}: vertices {nv}; capacity/L in [{clo/L:.9f}, {chi/L:.9f}] (cube a = {a_c:.9f}); "
                  f"max_t F*/L >= {hb[0]/L:.7f} at t={hb[2]:.2f} (bracket top there {hb[1]/L:.7f}; cube h = {h_c:.7f})")
    print("## the cells: upper bounds of a_inf and h_inf from blocks of L = 1, 2, 3 sites, against the cube")
    print("   (a: Shannon capacity per site, duality bracket; h: max over a t-grid of step 0.005 of the certified bracket of F*(t)/L)")
    rows = []
    cells = [(0.3, 3.0), (0.2, 3.0), (0.1, 4.0), (0.3, 1.0), (0.1, 6.0)]
    for p, u in cells:
        a_c, h_c = cube_a_h(u)
        for L in (1, 2, 3):
            W, us, nv = channel(L, p, u)
            clo, chi = capacity(W)
            hb = h_bracket(W, np.arange(0.05, 0.96, 0.005))
            rows.append((p, u, L, chi / L, a_c, hb[1] / L, h_c))
            print(f"   (p,u)=({p},{u:g}) L={L}: u*={us:.4f}, {nv:3d} vertices | a_inf <= {chi/L:.6f} (bracket width {chi-clo:.1e}) cube {a_c:.6f} ratio {chi/L/a_c:.4f} "
                  f"{'BELOW' if chi/L < a_c else 'above'} | h_inf <= ~{hb[1]/L:.6f} (grid max, lower end {hb[0]/L:.6f}, t={hb[2]:.3f}) cube {h_c:.6f} ratio {hb[1]/L/h_c:.4f} "
                  f"{'BELOW' if hb[1]/L < h_c else 'above'}", flush=True)
    print("## blocks of ONE site, the whole grid p in {0.3, 0.2, 0.1}, u in {1, 1.5, 2, 2.5, 3, 4, 5, 6}: ratio of the L = 1 bound to the cube")
    worst_a, worst_h = 10.0, 10.0
    for p in (0.3, 0.2, 0.1):
        line_a, line_h = [], []
        for u in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
            a_c, h_c = cube_a_h(u)
            W, us, nv = channel(1, p, u)
            clo, chi = capacity(W)
            hb = h_bracket(W, np.arange(0.05, 0.96, 0.005))
            line_a.append(f"{clo/a_c:.4f}")
            line_h.append(f"{hb[0]/h_c:.4f}")
            worst_a, worst_h = min(worst_a, clo / a_c), min(worst_h, hb[0] / h_c)
        print(f"   p={p}: a-bound/cube = {', '.join(line_a)}")
        print(f"   p={p}: h-bound/cube = {', '.join(line_h)}")
    print(f"   smallest ratio over the grid (lower ends of my brackets, so the L = 1 bound is at least this): a {worst_a:.4f}, h {worst_h:.4f}")
    print("# END")
