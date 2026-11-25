"""Step 4 -- structure on short chains (binary symmetric chain, u = 1).
(1) which vertices carry weight in the optimal M (n = 4; h-type t = 0.45, capacity) -- in particular the non-additive ones at p = 0.1;
(2) the Renyi centre Q* (hardest instance): is it a Markov chain?  Walsh expansion of gamma* = -ln(Q*/pi) by order;
(3) optional (argument 5): n = 5 with all 395094 vertices at p = 0.3: F*_5(0.45), E_5 against site-wise labels and ln Z_5(h)/Z_5(0)."""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *

t0 = time.time(); u = 1.0
do5 = len(sys.argv) > 1 and sys.argv[1] == "5"
n = 4; H = height_functions(n) * u
add = sitewise_labels([u] * n); add = add - add[:, :1]
keys = {tuple(np.round(f, 6)) for f in add}
addmask = np.array([tuple(np.round(f, 6)) in keys for f in H])
S = np.array([[1 - 2 * b for b in bits(x, n)] for x in range(2 ** n)], float)          # spins, site i = column i

def walsh(g):
    """Walsh coefficients of a function on {+-1}^n, grouped by order; returns dict subset -> coefficient"""
    out = {}
    for k in range(n + 1):
        for A in itertools.combinations(range(n), k):
            chi = np.prod(S[:, list(A)], axis=1) if A else np.ones(2 ** n)
            out[A] = float((g * chi).mean())
    return out

def cond_mi_13_given_2(Q):
    """I(x1; x3 | x2) under Q (zero for a Markov chain)"""
    tot = 0.0
    for b in (1, -1):
        idx = S[:, 1] == b; pb = Q[idx].sum()
        J = np.zeros((2, 2))
        for a in (0, 1):
            for c in (0, 1):
                J[a, c] = Q[idx & (S[:, 0] == 1 - 2 * a) & (S[:, 2] == 1 - 2 * c)].sum() / pb
        m1 = J.sum(axis=1); m3 = J.sum(axis=0)
        tot += pb * float((J * np.log(J / np.outer(m1, m3))).sum())
    return tot

def describe(f):
    """a vertex as a function: is it additive? is it a function of the bonds only (even under the global flip)?"""
    w = walsh(f)
    orders = {k: math.sqrt(sum(v * v for A, v in w.items() if len(A) == k)) for k in range(1, n + 1)}
    return "Walsh norms by order " + " ".join("%d:%.3f" % (k, v) for k, v in orders.items())

for p in (0.4, 0.3, 0.1):
    pi = bsc_block_law(n, p); P = gibbs_rows(pi, H)
    print("\n=== p = %.1f, n = %d" % (p, n))
    for kind in ("t=0.45", "capacity", "E"):
        if kind == "t=0.45": lo, up, M, Q = renyi_F(P, 0.45, tol=1e-11)
        elif kind == "capacity": lo, up, M, Q = capacity(P, tol=1e-11, itmax=400000)
        else: lo, up, M, Q = E_threshold(P, tol=1e-11, itmax=400000)
        supp = np.where(M > 1e-6)[0]
        print(" %-8s value [%.7f, %.7f]; support %d vertices, of which non-additive %d with total weight %.4f" % (
            kind, lo, up, len(supp), int((~addmask[supp]).sum()), M[supp][~addmask[supp]].sum()))
        if kind != "E":
            g = -np.log(Q / pi); g -= g.mean(); w = walsh(g)
            orders = {k: math.sqrt(sum(v * v for A, v in w.items() if len(A) == k)) for k in range(1, n + 1)}
            print("          centre Q*: I(x1;x3|x2) = %.3e (pi: %.1e) | gamma* = -ln(Q*/pi): Walsh norms by order %s | nn pair coefficients %s | max|gamma*(x)-gamma*(y)| over edges = %.4f" % (
                cond_mi_13_given_2(Q), cond_mi_13_given_2(pi), " ".join("%d:%.4f" % (k, v) for k, v in orders.items()),
                " ".join("%.4f" % w[(i, i + 1)] for i in range(n - 1)),
                max(abs(g[a] - g[b]) for (a, b, i) in cube_edges(n))))
        if (~addmask[supp]).any() or kind == "capacity":
            order = supp[np.argsort(-M[supp])][:8]
            for k in order:
                print("          M=%.4f %s  f=%s  %s" % (M[k], "additive    " if addmask[k] else "NON-additive", " ".join("%+d" % round(v) for v in H[k]), describe(H[k] - H[k].mean())))
print("%.1f s" % (time.time() - t0))

if do5:
    n = 5; t1 = time.time()
    H5 = height_functions(5) * u
    print("\nn = 5: %d vertices (%.1f s)" % (len(H5), time.time() - t1))
    add = sitewise_labels([u] * n); add = add - add[:, :1]
    for p in (0.3,):
        pi = bsc_block_law(n, p); P = gibbs_rows(pi, H5); Pa = gibbs_rows(pi, add)
        lo, up, M, Q = renyi_F(P, 0.45, tol=1e-8, itmax=3000)
        loa, upa, Ma, Qa = renyi_F(Pa, 0.45, tol=1e-11)
        # dual certificate with the site-wise centre: max over ALL 395094 vertices of (1-t) D_t(pi_phi || Q_sitewise)
        cert = float((-np.log((P ** 0.45) @ (Qa ** 0.55))).max())
        print("p=%.1f: F*_5(0.45): all vertices [%.7f, %.7f]; site-wise only [%.7f, %.7f]; dual value of the site-wise centre over ALL vertices: %.7f  (%.1f s)" % (
            p, lo, up, loa, upa, cert, time.time() - t1))
        Ea = E_threshold(Pa, tol=1e-11, itmax=400000)
        certE = float(((Ea[3] * np.log(Ea[3])).sum() - np.log(P) @ Ea[3]).max())
        T = np.array([[1 - p, p], [p, 1 - p]]); D = np.diag([math.exp(u / 2), math.exp(-u / 2)])
        x = D @ np.ones(2)
        for _ in range(n - 1): x = D @ (T @ x)
        EF = math.log(0.5 * x.sum())
        print("p=%.1f: E_5: site-wise only [%.7f, %.7f]; max over ALL vertices of KL(Q_sitewise || pi_phi) = %.7f; ln Z_5(h)/Z_5(0) = %.7f  (%.1f s)" % (
            p, Ea[0], Ea[1], certE, EF, time.time() - t1))
        aa = capacity(Pa, tol=1e-11, itmax=400000)
        certa = float((P * (np.log(P) - np.log(aa[3])[None, :])).sum(axis=1).max())
        print("p=%.1f: a_5: site-wise only [%.7f, %.7f]; max over ALL vertices of KL(pi_phi || Q_sitewise) = %.7f (if larger, non-additive vertices matter)  (%.1f s)" % (
            p, aa[0], aa[1], certa, time.time() - t1))
    for p in (0.1,):
        pi = bsc_block_law(n, p); P = gibbs_rows(pi, H5); Pa = gibbs_rows(pi, add)
        for t in (0.45, 0.65, 0.85):
            loa, upa, Ma, Qa = renyi_F(Pa, t, tol=1e-11)
            cert = float((-np.log((P ** t) @ (Qa ** (1 - t)))).max())
            print("p=%.1f t=%.2f: site-wise only [%.7f, %.7f]; dual value of the site-wise centre over ALL vertices: %.7f  (%.1f s)" % (p, t, loa, upa, cert, time.time() - t1))
    print("%.1f s" % (time.time() - t0))
