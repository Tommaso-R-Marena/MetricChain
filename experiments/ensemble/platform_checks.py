#!/usr/bin/env python3
"""Numerical checks for Theorem E7' (docs/ensemble/ENSEMBLE_REPORT.md §3.3): ensembles of relative poses of
two rigid bodies seen through the laws of m inter-body distances (a parallel platform with m legs).

The parameter variety is the group of proper rigid motions SE(d); the features are the squared leg
lengths |u_e - (R v_e + t)|^2 for fixed attachment points u_e (body A) and v_e (body B).

P1  Matroid of the legs (rank function from the Jacobian at a random pose): free for m = dim SE(d)
    (3 in the plane, 6 in space), uniform of that rank and connected for m = dim SE(d) + 1.
P2  d = 2, m = 4 and 5: no non-constant splice of the leg lengths of two random poses is realised by any
    pose (multi-start least squares); m = 3: splices of nearby poses are realised.
P3  d = 3, m = 7: the same; m = 6: splices of nearby poses are realised.
Exit code 0 iff every check passes.
"""
import itertools, sys
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

rng = np.random.default_rng(20261203)


def rot(d, w):
    if d == 2:
        c, s = np.cos(w[0]), np.sin(w[0])
        return np.array([[c, -s], [s, c]])
    return Rotation.from_rotvec(w).as_matrix()


def nrot(d):
    return 1 if d == 2 else 3


def feats(d, U, V, x):
    R = rot(d, x[:nrot(d)]); t = x[nrot(d):]
    return np.sum((U - (V @ R.T + t)) ** 2, axis=1)


def random_pose(d):
    if d == 2:
        return np.concatenate([[rng.uniform(-np.pi, np.pi)], rng.normal(size=2)])
    return np.concatenate([Rotation.random(random_state=rng.integers(1 << 31)).as_rotvec(), rng.normal(size=3)])


def jac(d, U, V, x, h=1e-6):
    f0 = feats(d, U, V, x); J = np.zeros((len(f0), len(x)))
    for k in range(len(x)):
        e = np.zeros(len(x)); e[k] = h
        J[:, k] = (feats(d, U, V, x + e) - feats(d, U, V, x - e)) / (2 * h)
    return J


def connected(J):
    m = J.shape[0]
    r = lambda S: 0 if not S else int(np.linalg.matrix_rank(J[list(S)], tol=1e-6))
    full = r(range(m))
    for mask in range(1, 2 ** (m - 1)):
        S = [k for k in range(m) if mask >> k & 1]; T = [k for k in range(m) if not mask >> k & 1]
        if r(S) + r(T) == full:
            return False, full
    return True, full


def realise(d, U, V, q, starts, first=None):
    best = np.inf
    for s in range(starts):
        x0 = first.copy() if (s == 0 and first is not None) else random_pose(d)
        res = least_squares(lambda x: feats(d, U, V, x) - q, x0, method="trf", xtol=1e-14, ftol=1e-14, gtol=1e-14)
        best = min(best, np.linalg.norm(res.fun))
        if best < 1e-10:
            break
    return best


def test_P1():
    out = []; ok = True
    for d, m, expect_conn in ((2, 3, False), (2, 4, True), (2, 5, True), (3, 6, False), (3, 7, True), (3, 8, True)):
        U = rng.normal(size=(m, d)); V = rng.normal(size=(m, d))
        c, full = connected(jac(d, U, V, random_pose(d)))
        out.append(f"    d = {d}, {m} legs: rank {full}, connected = {c}")
        ok &= (c == expect_conn) and full == min(m, d * (d + 1) // 2)
    return ok, out


def splice_test(d, m, instances, starts, max_cols):
    worst = np.inf; sanity = 0.0; count = 0
    for _ in range(instances):
        U = rng.normal(size=(m, d)); V = rng.normal(size=(m, d))
        x1, x2 = random_pose(d), random_pose(d)
        L = np.array([feats(d, U, V, x1), feats(d, U, V, x2)])
        sanity = max(sanity, realise(d, U, V, L[0], starts))
        cols = [c for c in itertools.product(range(2), repeat=m) if len(set(c)) > 1]
        if len(cols) > max_cols:
            cols = [cols[k] for k in rng.choice(len(cols), size=max_cols, replace=False)]
        for a in cols:
            q = L[list(a), range(m)]
            worst = min(worst, realise(d, U, V, q, starts)); count += 1
    return worst, sanity, count


def nearby_test(d, m, trials):
    hit = 0
    for _ in range(trials):
        U = rng.normal(size=(m, d)); V = rng.normal(size=(m, d))
        x1 = random_pose(d); x2 = x1 + 1e-3 * rng.normal(size=len(x1))
        L = np.array([feats(d, U, V, x1), feats(d, U, V, x2)])
        a = np.array([0] * (m // 2) + [1] * (m - m // 2))
        hit += realise(d, U, V, L[a, range(m)], 3, first=x1) < 1e-10
    return hit


def test_P2():
    out = []; ok = True
    for m in (4, 5):
        worst, sanity, count = splice_test(2, m, 6, 30, 40)
        out.append(f"    d = 2, {m} legs: smallest residual over {count} non-constant splices = {worst:.3e} "
                   f"(true pose: {sanity:.1e})")
        ok &= worst > 1e-5 and worst > 1e5 * sanity and sanity < 1e-9
    hit = nearby_test(2, 3, 20)
    out.append(f"    d = 2, 3 legs (free matroid): splices of nearby poses realised in {hit}/20 cases")
    ok &= hit == 20
    return ok, out


def test_P3():
    out = []; ok = True
    worst, sanity, count = splice_test(3, 7, 2, 40, 40)
    out.append(f"    d = 3, 7 legs: smallest residual over {count} non-constant splices = {worst:.3e} "
               f"(true pose: {sanity:.1e})")
    ok &= worst > 1e-5 and worst > 1e5 * sanity and sanity < 1e-9
    hit = nearby_test(3, 6, 20)
    out.append(f"    d = 3, 6 legs (free matroid): splices of nearby poses realised in {hit}/20 cases")
    ok &= hit == 20
    return ok, out


def main():
    allok = True
    for name, fn in (("P1 matroid of the legs", test_P1), ("P2 planar platform", test_P2), ("P3 spatial platform", test_P3)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
