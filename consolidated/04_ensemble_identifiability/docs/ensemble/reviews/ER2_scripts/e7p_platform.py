#!/usr/bin/env python3
"""ER2: attack on Theorem E7' (two rigid bodies joined by m legs).

Poses g = (R, t) in SE(d); squared leg lengths F_e(g) = |u_e - (R v_e + t)|^2.

G1  matroid: ranks of all subsets of the legs at a random pose (Jacobian by finite differences of my own
    parametrisation), generic attachment points: uniform of rank min(m, D_d)?
G2  d = 2, the fibre of a generic pose, EXACT real-solution count: eliminate the translation (two linear
    equations), then all real roots in the rotation angle of one equation (dense sampling + bisection).
    m = 3: how many poses share the three leg lengths of a generic pose?   m = 4: is the pose unique?
G3  d = 2, m = 4, (b): non-constant splices of two random poses: is any realised?  (exact: roots of the first
    three legs, then the residual of the fourth); distribution of the smallest residual.
G4  d = 2, m = 3, (c): fraction of random pairs of poses for which both complementary splices are realised
    (exact root count), and one explicit twin ensemble.
G5  d = 3: m = 6: distinct real poses with the six leg lengths of a generic pose (multi-start least squares:
    a lower bound on the number); m = 7: any second pose?  splices for m = 7.
G6  failures of 'generic':
    (i)   three legs at one base point (d = 2, m = 4): matroid, and an explicit twin ensemble;
    (ii)  all u_e on a line and all v_e on a line (d = 2), all u_e in a plane and all v_e in a plane (d = 3):
          the mirror pose has the same leg lengths, for every m;
    (iii) four legs at one base point (d = 3, m = 7): matroid disconnected, splices realised.
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import least_squares, brentq
from scipy.spatial.transform import Rotation

rng = np.random.default_rng(703)


def R2(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])


def feats(d, U, V, x):
    if d == 2:
        R = R2(x[0]); t = x[1:]
    else:
        R = Rotation.from_rotvec(x[:3]).as_matrix(); t = x[3:]
    return np.sum((U - (V @ R.T + t)) ** 2, axis=1)


def rand_pose(d):
    if d == 2:
        return np.concatenate([[rng.uniform(-np.pi, np.pi)], rng.normal(size=2)])
    return np.concatenate([Rotation.random(random_state=int(rng.integers(1 << 31))).as_rotvec(), rng.normal(size=3)])


def jac(d, U, V, x, h=1e-6):
    f0 = feats(d, U, V, x); J = np.zeros((len(f0), len(x)))
    for k in range(len(x)):
        e = np.zeros(len(x)); e[k] = h
        J[:, k] = (feats(d, U, V, x + e) - feats(d, U, V, x - e)) / (2 * h)
    return J


def rank_function(J, tol=1e-6):
    m = J.shape[0]
    return {S: (int(np.linalg.matrix_rank(J[list(S)], tol=tol)) if S else 0)
            for k in range(m + 1) for S in itertools.combinations(range(m), k)}


def is_connected(r, m):
    full = r[tuple(range(m))]
    for k in range(1, m):
        for S in itertools.combinations(range(m), k):
            T = tuple(j for j in range(m) if j not in S)
            if r[S] + r[T] == full:
                return False
    return True


def same_pose(d, x, y, tol=1e-6):
    if d == 2:
        return abs(np.angle(np.exp(1j * (x[0] - y[0])))) < tol and np.abs(x[1:] - y[1:]).max() < tol
    Rx = Rotation.from_rotvec(x[:3]).as_matrix(); Ry = Rotation.from_rotvec(y[:3]).as_matrix()
    return np.abs(Rx - Ry).max() < tol and np.abs(x[3:] - y[3:]).max() < tol


# ---------------------------------------------------------------- exact planar solver (three legs)
def planar_roots(U, V, L, ngrid=3000):
    """All poses (theta, t) of the plane with |u_e - R v_e - t|^2 = L_e, e = 1, 2, 3 (generic position).
    t is eliminated by the two differences (linear in t); the remaining equation, multiplied by det^2, is a
    trigonometric polynomial G(theta); its sign changes are bracketed on a grid and refined by bisection."""
    def parts(th):
        th = np.atleast_1d(th)
        c, s = np.cos(th)[:, None], np.sin(th)[:, None]
        Px = c * V[None, :, 0] - s * V[None, :, 1]; Py = s * V[None, :, 0] + c * V[None, :, 1]
        Wx = U[None, :, 0] - Px; Wy = U[None, :, 1] - Py                       # w_e = u_e - R v_e, shape (K, 3)
        n2 = Wx ** 2 + Wy ** 2
        m11 = -2 * (Wx[:, 1] - Wx[:, 0]); m12 = -2 * (Wy[:, 1] - Wy[:, 0])
        m21 = -2 * (Wx[:, 2] - Wx[:, 0]); m22 = -2 * (Wy[:, 2] - Wy[:, 0])
        r1 = (L[1] - L[0]) - (n2[:, 1] - n2[:, 0]); r2 = (L[2] - L[0]) - (n2[:, 2] - n2[:, 0])
        det = m11 * m22 - m12 * m21
        tx = m22 * r1 - m12 * r2; ty = -m21 * r1 + m11 * r2                    # t = (tx, ty) / det
        G = (Wx[:, 0] * det - tx) ** 2 + (Wy[:, 0] * det - ty) ** 2 - L[0] * det ** 2
        return G, det, tx, ty
    ths = np.linspace(-np.pi, np.pi, ngrid + 1)
    Gs = parts(ths)[0]
    sols = []
    for k in np.nonzero((Gs[:-1] == 0) | (Gs[:-1] * Gs[1:] < 0))[0]:
        th = ths[k] if Gs[k] == 0 else brentq(lambda t: parts(t)[0][0], ths[k], ths[k + 1], xtol=1e-15, rtol=1e-15)
        G, det, tx, ty = parts(th)
        if abs(det[0]) < 1e-9:
            continue
        x = np.array([th, tx[0] / det[0], ty[0] / det[0]])
        res = least_squares(lambda z: feats(2, U, V, z) - L, x, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.linalg.norm(res.fun) < 1e-10 and not any(same_pose(2, res.x, y) for y in sols):
            sols.append(res.x)
    return sols


def multistart(d, U, V, q, starts, first=None, stop_at_first=False):
    """Distinct poses with residual < 1e-10, and the smallest residual seen."""
    sols = []; best = np.inf
    for s in range(starts):
        x0 = first.copy() if (s == 0 and first is not None) else rand_pose(d)
        res = least_squares(lambda x: feats(d, U, V, x) - q, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=400)
        r = np.linalg.norm(res.fun); best = min(best, r)
        if r < 1e-10 and not any(same_pose(d, res.x, y) for y in sols):
            sols.append(res.x)
            if stop_at_first:
                break
    return sols, best


def G1():
    print("G1  matroid of the legs, generic attachment points (ranks of all subsets at a random pose)")
    ok = True
    for d, ms in ((2, (1, 2, 3, 4, 5)), (3, (1, 2, 5, 6, 7, 8))):
        D = d * (d + 1) // 2
        for m in ms:
            uniform = True; conn = None
            for _ in range(3):
                U = rng.normal(size=(m, d)); V = rng.normal(size=(m, d))
                r = rank_function(jac(d, U, V, rand_pose(d)), )
                uniform &= all(r[S] == min(len(S), D) for S in r)
                c = is_connected(r, m); conn = c if conn is None else (conn and c)
            expect = (m >= D + 1) or m == 1
            print(f"    d = {d}, m = {m}: uniform of rank min(m, {D}): {uniform}; connected: {conn}   (m = 1 is connected: U_(1,1))" if m == 1
                  else f"    d = {d}, m = {m}: uniform of rank min(m, {D}): {uniform}; connected: {conn}")
            ok &= uniform and conn == expect
    return ok


def G2():
    print("G2  d = 2: exact number of real poses with the leg lengths of a generic pose")
    hist3 = {}; hist4 = {}; gap4 = np.inf; missed = 0; refined = 0
    for _ in range(300):
        U = rng.normal(size=(4, 2)); V = rng.normal(size=(4, 2)); x = rand_pose(2)
        L = feats(2, U, V, x)
        sols = planar_roots(U[:3], V[:3], L[:3])
        if not any(same_pose(2, s, x) for s in sols) or len(sols) % 2:
            sols = planar_roots(U[:3], V[:3], L[:3], ngrid=400000)       # two roots closer than the first grid
            refined += 1
        if not any(same_pose(2, s, x) for s in sols):
            missed += 1
        hist3[len(sols)] = hist3.get(len(sols), 0) + 1
        ok4 = [s for s in sols if abs(feats(2, U, V, s)[3] - L[3]) < 1e-8]
        hist4[len(ok4)] = hist4.get(len(ok4), 0) + 1
        for s in sols:
            if not same_pose(2, s, x):
                gap4 = min(gap4, abs(feats(2, U, V, s)[3] - L[3]))
    print(f"    m = 3, 300 generic (attachment points, pose): number of real poses in the fibre -> count: {dict(sorted(hist3.items()))}; true pose not recovered: {missed} (instances re-solved on a finer grid: {refined})")
    print(f"    m = 4: number of poses of the three-leg fibre that also match the fourth leg -> count: {dict(sorted(hist4.items()))}; "
          f"smallest fourth-leg mismatch at another pose of the fibre: {gap4:.3e}")
    return missed == 0 and set(hist4) == {1} and all(k % 2 == 0 and k >= 2 for k in hist3)


def G3():
    print("G3  d = 2, m = 4: non-constant splices of two random poses (exact: roots of legs 1-3, residual of leg 4)")
    res = []
    for _ in range(60):
        U = rng.normal(size=(4, 2)); V = rng.normal(size=(4, 2))
        x1, x2 = rand_pose(2), rand_pose(2)
        Lm = np.array([feats(2, U, V, x1), feats(2, U, V, x2)])
        for a in itertools.product(range(2), repeat=4):
            if len(set(a)) == 1:
                continue
            q = Lm[list(a), range(4)]
            sols = planar_roots(U[:3], V[:3], q[:3])
            r = min((abs(feats(2, U, V, s)[3] - q[3]) for s in sols), default=np.inf)
            res.append(r)
    res = np.array(res); fin = res[np.isfinite(res)]
    qs = np.quantile(fin, [0.0, 0.01, 0.1, 0.5])
    print(f"    {len(res)} splices; first three legs have no real pose in {np.sum(~np.isfinite(res))}; otherwise the smallest |F_4 - q_4| over the real poses: "
          f"min {qs[0]:.3e}, 1% {qs[1]:.3e}, 10% {qs[2]:.3e}, median {qs[3]:.3e}; below 1e-6: {int(np.sum(fin < 1e-6))}")
    return int(np.sum(fin < 1e-6)) == 0


def G4():
    print("G4  d = 2, m = 3 (= dim SE(2)): complementary splices of two poses along ({1}, {2,3})")
    both = 0; tot = 200; example = None
    U = V = None
    for k in range(tot):
        U = rng.normal(size=(3, 2)); V = rng.normal(size=(3, 2))
        x1, x2 = rand_pose(2), rand_pose(2)
        L1, L2 = feats(2, U, V, x1), feats(2, U, V, x2)
        qa = np.array([L1[0], L2[1], L2[2]]); qb = np.array([L2[0], L1[1], L1[2]])
        sa = planar_roots(U, V, qa); sb = planar_roots(U, V, qb)
        if sa and sb:
            both += 1
            if example is None:
                example = (U, V, x1, x2, sa[0], sb[0], L1, L2)
    print(f"    {tot} independent random pairs of poses (random attachment points): both complementary splices realised in {both}")
    U, V, x1, x2, y1, y2, L1, L2 = example
    np.set_printoptions(precision=6, suppress=True)
    print("    explicit twin ensemble (first hit):")
    print(f"      u = {U.tolist()}")
    print(f"      v = {V.tolist()}")
    print(f"      poses (theta, t):  g1 = {x1},  g2 = {x2}")
    print(f"                         h1 = {y1},  h2 = {y2}")
    print(f"      squared leg lengths: g1 {L1}, g2 {L2}; h1 {feats(2, U, V, y1)}, h2 {feats(2, U, V, y2)}")
    print("      => (1/2)(delta_g1 + delta_g2) and (1/2)(delta_h1 + delta_h2) have the same three leg-length laws")
    return both > 0


def G5():
    print("G5  d = 3")
    counts = []; t0 = time.time()
    for _ in range(4):
        U = rng.normal(size=(7, 3)); V = rng.normal(size=(7, 3)); x = rand_pose(3)
        L = feats(3, U, V, x)
        sols, _ = multistart(3, U[:6], V[:6], L[:6], 250, first=x)
        mism = [abs(feats(3, U, V, s)[6] - L[6]) for s in sols if not same_pose(3, s, x)]
        counts.append((len(sols), min(mism) if mism else np.inf))
    print("    m = 6, 4 generic instances, 250 starts each: distinct real poses found with the six leg lengths of the pose: "
          + ", ".join(str(c[0]) for c in counts) + f"   [{time.time() - t0:.0f} s]")
    print("    m = 7: smallest mismatch of the seventh leg at another pose of the six-leg fibre: "
          + ", ".join(f"{c[1]:.2e}" for c in counts))
    worst = np.inf; n = 0
    for _ in range(3):
        U = rng.normal(size=(7, 3)); V = rng.normal(size=(7, 3)); x1, x2 = rand_pose(3), rand_pose(3)
        Lm = np.array([feats(3, U, V, x1), feats(3, U, V, x2)])
        cols = [c for c in itertools.product(range(2), repeat=7) if len(set(c)) > 1]
        for k in rng.choice(len(cols), size=12, replace=False):
            q = Lm[list(cols[k]), range(7)]
            _, best = multistart(3, U, V, q, 40)
            worst = min(worst, best); n += 1
    print(f"    m = 7: {n} non-constant splices of two random poses, 40 starts each: smallest least-squares residual {worst:.3e}   [{time.time() - t0:.0f} s]")
    return all(c[0] >= 2 for c in counts) and all(c[1] > 1e-6 for c in counts) and worst > 1e-6


def G6():
    print("G6  failures of 'generic'")
    np.set_printoptions(precision=6, suppress=True)
    # (i) three legs at one base point, d = 2, m = 4
    U = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [2.0, 0.5]])
    V = np.array([[1.0, 0.0], [0.0, 1.0], [-0.7, -0.4], [0.3, 1.5]])
    x1 = np.array([0.3, 0.8, -0.4]); x2 = np.array([-0.9, -0.6, 1.1])
    r = rank_function(jac(2, U, V, x1))
    print(f"    (i) d = 2, m = 4, u_1 = u_2 = u_3: rank of legs {{1,2,3}} = {r[(0, 1, 2)]}, of {{4}} = {r[(3,)]}, of all = {r[(0, 1, 2, 3)]}; connected: {is_connected(r, 4)}")
    L1, L2 = feats(2, U, V, x1), feats(2, U, V, x2)
    qa = np.array([L1[0], L1[1], L1[2], L2[3]]); qb = np.array([L2[0], L2[1], L2[2], L1[3]])
    sa, ra = multistart(2, U, V, qa, 200); sb, rb = multistart(2, U, V, qb, 200)
    print(f"        g1 = {x1}, g2 = {x2}: squared lengths {L1} and {L2}")
    print(f"        splice (legs 1-3 of g1, leg 4 of g2): {len(sa)} real poses (residual {ra:.1e}); splice (legs 1-3 of g2, leg 4 of g1): {len(sb)} real poses (residual {rb:.1e})")
    if sa and sb:
        print(f"        h1 = {sa[0]}, h2 = {sb[0]}: squared lengths {feats(2, U, V, sa[0])} and {feats(2, U, V, sb[0])}")
        print("        => twin ensemble with the same four leg-length laws although m = 4 = dim SE(2) + 1")
    hit = 0
    for _ in range(100):
        y1, y2 = rand_pose(2), rand_pose(2); M1, M2 = feats(2, U, V, y1), feats(2, U, V, y2)
        a, _ = multistart(2, U, V, np.array([M1[0], M1[1], M1[2], M2[3]]), 12, stop_at_first=True)
        b, _ = multistart(2, U, V, np.array([M2[0], M2[1], M2[2], M1[3]]), 12, stop_at_first=True)
        hit += bool(a) and bool(b)
    print(f"        100 random pairs of poses with these attachment points: both splices realised in {hit}")
    # (ii) collinear / coplanar attachment points: mirror pose
    for d, m in ((2, 6), (3, 9)):
        U = rng.normal(size=(m, d)); V = rng.normal(size=(m, d)); U[:, -1] = 0.0; V[:, -1] = 0.0
        x = rand_pose(d)
        S = np.diag([1.0] * (d - 1) + [-1.0])
        if d == 2:
            R = R2(x[0]); t = x[1:]
        else:
            R = Rotation.from_rotvec(x[:3]).as_matrix(); t = x[3:]
        Rm = S @ R @ S; tm = S @ t
        Lx = np.sum((U - (V @ R.T + t)) ** 2, axis=1); Lm = np.sum((U - (V @ Rm.T + tm)) ** 2, axis=1)
        r = rank_function(jac(d, U, V, x)) if m <= 9 else None
        D = d * (d + 1) // 2
        unif = all(r[Sx] == min(len(Sx), D) for Sx in r)
        print(f"    (ii) d = {d}, m = {m}, all u_e and all v_e in a hyperplane: mirror pose (S R S, S t): det = {np.linalg.det(Rm):+.3f}, "
              f"different from the pose: {np.abs(Rm - R).max() + np.abs(tm - t).max() > 1e-6}, largest difference of the {m} squared leg lengths: {np.abs(Lx - Lm).max():.1e}; "
              f"leg matroid still uniform of rank {D}: {unif}")
    # (iii) four legs at one base point, d = 3, m = 7
    U = rng.normal(size=(7, 3)); U[1] = U[0]; U[2] = U[0]; U[3] = U[0]
    V = rng.normal(size=(7, 3)); x1 = rand_pose(3)
    r = rank_function(jac(3, U, V, x1))
    J = (0, 1, 2, 3); Jc = (4, 5, 6)
    print(f"    (iii) d = 3, m = 7, u_1 = ... = u_4: rank of legs {{1..4}} = {r[J]}, of {{5,6,7}} = {r[Jc]}, of all = {r[tuple(range(7))]}; connected: {is_connected(r, 7)}")
    hit = 0
    for _ in range(10):
        x1 = rand_pose(3); x2 = x1 + 0.05 * rng.normal(size=6)
        L1, L2 = feats(3, U, V, x1), feats(3, U, V, x2)
        qa = np.concatenate([L1[:4], L2[4:]]); qb = np.concatenate([L2[:4], L1[4:]])
        a, _ = multistart(3, U, V, qa, 6, first=x1, stop_at_first=True); b, _ = multistart(3, U, V, qb, 6, first=x2, stop_at_first=True)
        hit += bool(a) and bool(b)
    print(f"        10 pairs of poses at distance ~0.05: both splices along ({{1..4}}, {{5,6,7}}) realised in {hit}")
    return True


def G7():
    print("G7  shared attachment points that do not disconnect the matroid (the theorem's genericity is sufficient, not necessary)")
    D2 = 3
    for label, share in (("u_1 = u_2", "a"), ("u_1 = u_2 and v_3 = v_4", "b")):
        uniform = True; hist = {}; worst = np.inf; nspl = 0
        for _ in range(40):
            U = rng.normal(size=(4, 2)); V = rng.normal(size=(4, 2)); U[1] = U[0]
            if share == "b":
                V[3] = V[2]
            x = rand_pose(2); L = feats(2, U, V, x)
            r = rank_function(jac(2, U, V, x)); uniform &= all(r[S] == min(len(S), D2) for S in r)
            sols = planar_roots(U[:3], V[:3], L[:3])
            if not any(same_pose(2, y, x) for y in sols) or len(sols) % 2:
                sols = planar_roots(U[:3], V[:3], L[:3], ngrid=400000)
            k = sum(abs(feats(2, U, V, y)[3] - L[3]) < 1e-8 for y in sols); hist[k] = hist.get(k, 0) + 1
            x2 = rand_pose(2); Lm = np.array([L, feats(2, U, V, x2)])
            for a in itertools.product(range(2), repeat=4):
                if len(set(a)) > 1:
                    q = Lm[list(a), range(4)]
                    rr = min((abs(feats(2, U, V, y)[3] - q[3]) for y in planar_roots(U[:3], V[:3], q[:3])), default=np.inf)
                    worst = min(worst, rr); nspl += 1
        print(f"    d = 2, m = 4, {label}: matroid uniform of rank 3: {uniform}; poses with the four leg lengths of a random pose -> count {dict(sorted(hist.items()))}; "
              f"smallest fourth-leg residual over {nspl} non-constant splices: {worst:.2e}")
    U = rng.normal(size=(7, 3)); U[1] = U[0]; U[3] = U[2]; U[5] = U[4]; V = rng.normal(size=(7, 3))
    x = rand_pose(3); r = rank_function(jac(3, U, V, x))
    sols, _ = multistart(3, U[:6], V[:6], feats(3, U, V, x)[:6], 150, first=x)
    mism = [abs(feats(3, U, V, y)[6] - feats(3, U, V, x)[6]) for y in sols if not same_pose(3, y, x)]
    print(f"    d = 3, m = 7, three pairs of legs sharing a base point: matroid uniform of rank 6: {all(r[S] == min(len(S), 6) for S in r)}; connected: {is_connected(r, 7)}; "
          f"{len(sols)} real poses found for legs 1-6; smallest seventh-leg mismatch at another one: {min(mism) if mism else float('nan'):.2e}")
    return True


def main():
    t0 = time.time()
    sel = sys.argv[1:]
    for fn in (G1, G2, G3, G4, G5, G6, G7):
        if sel and fn.__name__ not in sel:
            continue
        ok = fn()
        print(f"    -> {'as claimed' if ok else 'NOT AS EXPECTED'}   [{time.time() - t0:.0f} s]", flush=True)


if __name__ == "__main__":
    main()
