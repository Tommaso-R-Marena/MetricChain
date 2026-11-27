#!/usr/bin/env python3
"""ER2: attack on Theorem E16 (the double cone).  Cube {-1,1}^n, uniform reference, envelope b*d_H.

For n = 2..7 and several b, and for a non-trivial gauge a:
  * LP  max E[M_a^2] over the class polytope; compare with the value of D_a ~ exp((b/2)|M_a|);
  * the optimal face: range of every weight on it (two LPs per state) and its dimension
    (rank of the set of points found), compared with the prediction:
        even n: the single point D_a;      odd n: the segment D_{a,theta}, |theta| <= tanh(b/2);
  * D_a is a member; its tight graph (edges of the cube that are tight) is connected for even n and has
    exactly two components for odd n;
  * odd n: E[sign M_a] on the optimal face ranges over [-tanh(b/2), tanh(b/2)].
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog


def cube(n):
    return np.array(list(itertools.product((-1, 1), repeat=n)))


def rows(n, b):
    X = cube(n); N = len(X); index = {tuple(x): k for k, x in enumerate(X)}
    R = []; E = []
    for k, x in enumerate(X):
        for i in range(n):
            y = x.copy(); y[i] = -y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0; r[k] = -np.exp(b); R.append(r); E.append((k, ky))
    return X, np.array(R), E


def components(N, edges):
    parent = list(range(N))

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]; u = parent[u]
        return u
    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(u) for u in range(N)})


def main():
    t0 = time.time(); allok = True
    rng = np.random.default_rng(1601)
    print("E16: max E[M_a^2] over the cube class; optimal face")
    for n in (2, 3, 4, 5, 6, 7):
        for b in ((0.3, 1.0, 2.5) if n <= 6 else (1.0,)):
            a = rng.choice((-1, 1), size=n) if n > 2 else np.ones(n, dtype=int)
            X, R, E = rows(n, b); N = len(X)
            M = (X * a).sum(axis=1).astype(float)
            kw = dict(A_ub=R, b_ub=np.zeros(len(R)), bounds=[(0, None)] * N, method="highs")
            res = linprog(-(M ** 2), A_eq=np.ones((1, N)), b_eq=[1.0], **kw)
            opt = -res.fun
            D = np.exp(0.5 * b * np.abs(M)); D /= D.sum()
            member = (R @ D).max() < 1e-12
            tight = [(u, v) for (u, v), r in zip(E, R) if abs(r @ D) < 1e-12 * np.exp(b)]
            comp = components(N, tight)
            # optimal face
            A_eq = np.vstack([np.ones((1, N)), M ** 2]); b_eq = np.array([1.0, opt])
            pts = [res.x]; spread = 0.0
            for k in range(N):
                lo = linprog(np.eye(N)[k], A_eq=A_eq, b_eq=b_eq, **kw)
                hi = linprog(-np.eye(N)[k], A_eq=A_eq, b_eq=b_eq, **kw)
                spread = max(spread, hi.x[k] - lo.x[k]); pts += [lo.x, hi.x]
            P = np.array(pts); dim = np.linalg.matrix_rank(P - P[0], tol=1e-7)
            line = (f"  n = {n}, b = {b}, a = {''.join('+' if v > 0 else '-' for v in a)}: LP max = {opt:.9f}, E_D[M^2] = {D @ M ** 2:.9f}; "
                    f"D member: {member}; tight-graph components of D: {comp}; optimal face: dimension {dim}, largest weight spread {spread:.3e}")
            ok = abs(opt - D @ M ** 2) < 1e-7 and member
            if n % 2 == 0:
                ok &= comp == 1 and dim == 0 and spread < 1e-7 and np.abs(P - D).max() < 1e-7
            else:
                th = np.tanh(b / 2)
                Dp = D * (1 + th * np.sign(M)); Dm = D * (1 - th * np.sign(M))
                ends_member = (R @ Dp).max() < 1e-12 and (R @ Dm).max() < 1e-12
                beyond = D * (1 + (th + 1e-3) * np.sign(M))
                # every point found on the face is of the form D (1 + theta sign M) with |theta| <= tanh(b/2)
                thetas = (P @ np.sign(M)); resid = max(np.abs(p - D * (1 + t * np.sign(M))).max() for p, t in zip(P, thetas))
                sgn_hi = -linprog(-np.sign(M), A_eq=A_eq, b_eq=b_eq, **kw).fun
                sgn_lo = linprog(np.sign(M), A_eq=A_eq, b_eq=b_eq, **kw).fun
                line += (f"\n        odd n: tanh(b/2) = {th:.6f}; E[sign M] on the face in [{sgn_lo:.6f}, {sgn_hi:.6f}]; "
                         f"end points D_(+-tanh(b/2)) members: {ends_member}; D_(theta) just beyond is a member: {(R @ beyond).max() < 1e-12}; "
                         f"largest deviation of a face point from D(1 + theta sign M): {resid:.1e}")
                ok &= (comp == 2 and dim == 1 and ends_member and abs(sgn_hi - th) < 1e-7 and abs(sgn_lo + th) < 1e-7
                       and resid < 1e-7 and not (R @ beyond).max() < 1e-12)
                if n == 1:
                    pass
            print(line + ("" if ok else "   <-- MISMATCH"), flush=True)
            allok &= ok
    # n = 1 (odd): M^2 = 1 identically; the 'maximisers' are the whole class
    print("  n = 1: M^2 = 1, every member maximises; the class is {|E x| <= tanh(b/2)} = the segment D_theta: consistent with (b)")
    print(("E16: NO COUNTEREXAMPLE" if allok else "E16: MISMATCH FOUND") + f"   [{time.time() - t0:.0f} s]")


if __name__ == "__main__":
    main()
