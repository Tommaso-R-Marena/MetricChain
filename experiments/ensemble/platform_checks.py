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
P4  The second half of Theorem E7'(b), in the plane, by an exact count of the real poses (a one-dimensional
    root search in the rotation angle; the translation is then linear): with three generic legs the fibre of a
    generic pose has an even number, at least two, of poses; a fourth leg singles out the true one.  And the
    excluded case (internal review ER2, F6): for two *planar* bodies (here: collinear attachment points on
    both) every pose has a mirror twin with the same leg lengths, whatever the number of legs.
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


def planar_poses(U, V, L):
    """All poses (theta, t) of the plane with |u_e - R_theta v_e - t|^2 = L_e for the first three legs e, by a
    root search in theta: for fixed theta the differences of the equations are linear in t."""
    def residual(theta):
        c, s_ = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s_], [s_, c]])
        C = U[:3] - V[:3] @ R.T                                          # centres: |t - C_e|^2 = L_e
        A = 2 * (C[0] - C[1:3]); rhs = L[1:3] - L[0] - np.sum(C[1:3] ** 2, axis=1) + np.sum(C[0] ** 2)
        t = np.linalg.solve(A, rhs)
        return np.sum((t - C[0]) ** 2) - L[0], t
    grid = np.linspace(-np.pi, np.pi, 20001)
    vals = np.array([residual(th)[0] for th in grid])
    poses = []
    for k in range(len(grid) - 1):
        if vals[k] == 0 or vals[k] * vals[k + 1] < 0:
            lo, hi = grid[k], grid[k + 1]; flo = vals[k]
            for _ in range(60):
                mid = 0.5 * (lo + hi); fm = residual(mid)[0]
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            th = 0.5 * (lo + hi)
            poses.append(np.concatenate([[th], residual(th)[1]]))
    return poses


def test_P4():
    out = []; ok = True
    counts = {}; unique = 0; trials = 100; smallest_other = np.inf
    for _ in range(trials):
        U = rng.normal(size=(4, 2)); V = rng.normal(size=(4, 2)); x = random_pose(2)
        L = feats(2, U, V, x)
        poses = planar_poses(U, V, L)
        counts[len(poses)] = counts.get(len(poses), 0) + 1
        match = 0
        for q in poses:
            mis = abs(feats(2, U, V, q)[3] - L[3])
            if mis < 1e-7:
                match += 1
            else:
                smallest_other = min(smallest_other, mis)
        unique += match == 1
    ok &= unique == trials and all(k % 2 == 0 and k >= 2 for k in counts)
    out.append(f"    d = 2, three generic legs, {trials} instances: number of real poses with the three lengths -> "
               f"{dict(sorted(counts.items()))} (always even, never one)")
    out.append(f"    a fourth leg singles out the true pose in {unique}/{trials}; smallest mismatch of the fourth "
               f"length at another pose of the fibre: {smallest_other:.2e}")
    # the excluded case: collinear attachment points on both bodies (planar bodies, d = 2)
    worst = 0.0
    for _ in range(20):
        m = 6
        U = np.column_stack([rng.normal(size=m), np.zeros(m)]); V = np.column_stack([rng.normal(size=m), np.zeros(m)])
        x = random_pose(2)
        twin = np.array([-x[0], x[1], -x[2]])                             # (S R S, S t), S the reflection y -> -y
        worst = max(worst, np.max(np.abs(feats(2, U, V, x) - feats(2, U, V, twin))))
        ok &= np.linalg.norm(twin - x) > 1e-3
    ok &= worst < 1e-10
    out.append(f"    collinear attachment points on both bodies, six legs, 20 poses: the mirror pose has the same six leg "
               f"lengths (largest difference {worst:.1e}) — no number of legs determines the pose")
    return ok, out


def main():
    allok = True
    for name, fn in (("P1 matroid of the legs", test_P1), ("P2 planar platform", test_P2), ("P3 spatial platform", test_P3),
                     ("P4 pose uniqueness, and planar bodies", test_P4)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
