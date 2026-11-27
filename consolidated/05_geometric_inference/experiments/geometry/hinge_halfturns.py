"""Degenerate torsion changes for two states at two hinges (HINGE_ENSEMBLES.md, Theorem M (b), (d);
the Science division's Proposition R22-1 (d)).

With R_1, R_2 the two hinge rotations, the mixture is identifiable iff at most one of
R_1, R_2, R_1 R_2 is a half-turn.  Cases checked by the linear programme over the eight
candidates of the cube (largest total weight a competing ensemble can put off the two states;
theory: 0 if identifiable, 2 min(w) otherwise):
    generic;  R_1 a half-turn;  R_1 R_2 a half-turn;  R_1 and R_2 half-turns (Science division);
    R_1 and R_1 R_2 half-turns (competitor: the cube vertices (0,1,0) and (1,0,1)).
"""
import sys
import numpy as np
from scipy.optimize import brentq, linprog
from geomlib import chain, edm
from hinge_pairs import THETA, cube_candidates, rotation_between, segments


def product_angle(n, t1, hinges, d1, d2):
    """Rotation angle of R_1 R_2 for torsion changes d1, d2."""
    t2 = t1.copy()
    t2[hinges[0]] += d1
    t2[hinges[1]] += d2
    X1, X2 = chain(n, t1, theta=THETA), chain(n, t2, theta=THETA)
    seg = segments(n, hinges)
    R0, _ = rotation_between(X1[seg[0]], X2[seg[0]])
    X2a = (X2 - X2[0]) @ R0 + X1[0]
    Q2, _ = rotation_between(X1[seg[2]], X2a[seg[2]])
    return np.arccos(np.clip((np.trace(Q2) - 1) / 2, -1, 1))


def off_state_weight(n, t1, hinges, d1, d2, w):
    t2 = t1.copy()
    t2[hinges[0]] += d1
    t2[hinges[1]] += d2
    X1, X2 = chain(n, t1, theta=THETA), chain(n, t2, theta=THETA)
    cand, ident, _ = cube_candidates(X1, X2, hinges)
    keys = list(cand)
    Ds = [edm(cand[k]) for k in keys]
    M = w[0] * edm(X1) + w[1] * edm(X2)
    iu = np.triu_indices(n, 1)
    A = np.vstack([np.array([D[iu] for D in Ds]).T, np.ones(8)])
    b = np.append(M[iu], 1.0)
    c = np.array([0.0 if k in ((0, 0, 0), (1, 1, 1)) else -1.0 for k in keys])
    r = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    used = [keys[i] for i in range(8) if r.x[i] > 1e-7 and keys[i] not in ((0, 0, 0), (1, 1, 1))]
    return -r.fun, used


def main():
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    n, hinges = 14, [3, 7]
    w = np.array([0.37, 0.63])
    ok = True
    for inst in range(3):
        t1 = rng.uniform(-np.pi, np.pi, n - 3)
        d1, d2 = rng.uniform(0.6, 2.4, 2)
        # a torsion change d2* that makes R_1 R_2 a half-turn (for d1 generic, and for d1 = pi)
        def find(d1v):
            f = lambda x: product_angle(n, t1, hinges, d1v, x) - (np.pi - 1e-9)
            grid = np.linspace(0.05, 2 * np.pi - 0.05, 400)
            vals = [product_angle(n, t1, hinges, d1v, x) for x in grid]
            i = int(np.argmax(vals))
            return grid[i], vals[i]
        cases = [("generic", d1, d2, 0.0),
                 ("R1 a half-turn", np.pi, d2, 0.0),
                 ("R1 and R2 half-turns", np.pi, np.pi, 2 * w.min())]
        x, ang = find(d1)
        if ang > np.pi - 1e-3:
            cases.append(("R1R2 a half-turn (R1, R2 generic)", d1, x, 0.0))
        x, ang = find(np.pi)
        if ang > np.pi - 1e-3:
            cases.append(("R1 and R1R2 half-turns", np.pi, x, 2 * w.min()))
        for name, a, b, want in cases:
            off, used = off_state_weight(n, t1, hinges, a, b, w)
            good = abs(off - want) < 2e-3
            ok &= good
            print(f"instance {inst}: {name:36s} off-state weight {off:.4f} (theory {want:.4f}) "
                  f"competitor vertices {used}   {'OK' if good else 'FAIL'}")
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
