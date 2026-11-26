"""Two states that share rigid segments (GEOMETRY-RES-0003; answers the Science division's
SCI-RES-0029 section 3).

Two conformations X1, X2 of a chain with fixed bond lengths and angles that differ in exactly
s torsions ("hinges") share s + 1 rigid segments.  For s = 2 this script checks, numerically,
the statements of docs/geometry/HINGE_ENSEMBLES.md:

 (1) the stacked configuration spans R^6 and dim N(z) = 6 (the conic condition fails);
 (2) the chains that are linear images of the stack are exactly EIGHT: with rho_A, rho_B, sigma
     the reflections in the planes spanned by (a1, a2), (a1, a02), (a2, a02) -- a1, a2 the
     hinge directions, a02 the axis of the rotation that carries the third segment of X1 to
     that of X2 relative to the first -- the candidates are, for (alpha, beta, gamma) in
     {0,1}^3,   segment 1 moved by rho_B^beta rho_A^alpha,  segment 2 by rho_B^beta sigma^gamma;
     X1 = (0,0,0), X2 = (1,1,1)   (R1 = rho_B rho_A, R2 = rho_A sigma, R1 R2 = rho_B sigma);
 (3) their squared-distance matrices satisfy exactly one affine relation, the parity
     sum (-1)^(alpha+beta+gamma) D(Y) = 0;
 (4) hence (linear programme) the only ensemble with the averaged squared distances of
     w1 X1 + w2 X2 is that mixture: identifiable although (CC) fails;
 (5) a multi-start search over ALL chains for affine images of the stack finds these eight
     classes and no other.
It also prints dim N(z) for s = 1, 2, 3, 4 hinges (the Science division's count 10, 6, 3 and
then 1) and repeats (4)-(5) for s = 3.

Usage: python3 hinge_pairs.py [seed] [nstart]
"""
import itertools
import sys
import numpy as np
from scipy.optimize import least_squares, linprog
from geomlib import chain, edm, stack, conic_matrix

THETA = np.deg2rad(111.0)


def nullity(A, ncols, tol=1e-9):
    s = np.linalg.svd(A, compute_uv=False)
    return ncols - int((s > tol * s[0]).sum())


def reflection(u, v):
    """Reflection in the plane spanned by u and v."""
    nrm = np.cross(u, v)
    nrm /= np.linalg.norm(nrm)
    return np.eye(3) - 2 * np.outer(nrm, nrm)


def rotation_between(P, Q):
    """Proper rotation R with Q_c = P_c R^T for congruent point sets (Kabsch)."""
    Pc, Qc = P - P.mean(0), Q - Q.mean(0)
    U, _, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(U @ Vt))
    R = (U @ np.diag([1, 1, d]) @ Vt).T
    return R, np.abs(Qc - Pc @ R.T).max()


def axis_of(R):
    w, V = np.linalg.eig(R)
    a = np.real(V[:, np.argmin(np.abs(w - 1))])
    return a / np.linalg.norm(a)


def hinge_states(n, hinges, rng, deltas=None):
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    t2 = t1.copy()
    deltas = deltas if deltas is not None else rng.uniform(0.6, 2.4, len(hinges)) * rng.choice([-1, 1], len(hinges))
    for h, d in zip(hinges, deltas):
        t2[h] += d
    return chain(n, t1, theta=THETA), chain(n, t2, theta=THETA), t1, t2


def segments(n, hinges):
    """0-based atom ranges of the rigid segments; the hinge bond (h+1, h+2) belongs to both."""
    cuts = [0] + [h + 1 for h in hinges]
    ends = [h + 2 for h in hinges] + [n - 1]
    return [list(range(a, b + 1)) for a, b in zip(cuts, ends)]


def e0_ok(X, tol=1e-9):
    n = len(X)
    b = [np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1)]
    c = [np.linalg.norm(X[i + 2] - X[i]) for i in range(n - 2)]
    c0 = np.sqrt(2 - 2 * np.cos(THETA))
    return max(abs(np.array(b) - 1).max(), abs(np.array(c) - c0).max()) < tol


def affine_residual(X, z):
    """Distance of the columns of X from span(1, z)."""
    B = np.hstack([np.ones((len(z), 1)), z])
    Q, _ = np.linalg.qr(B)
    return np.linalg.norm(X - Q @ (Q.T @ X))


def cube_candidates(X1, X2, hinges, wrong_mirror=False):
    n = len(X1)
    seg = segments(n, hinges)
    h1, h2 = hinges
    a1 = X1[h1 + 2] - X1[h1 + 1]
    a1 /= np.linalg.norm(a1)
    a2 = X1[h2 + 2] - X1[h2 + 1]
    a2 /= np.linalg.norm(a2)
    # orientation of each segment of X2 relative to X1, with segment 0 aligned
    R0, e0 = rotation_between(X1[seg[0]], X2[seg[0]])
    X2a = (X2 - X2[0]) @ R0 + X1[0]            # X2 moved so that segment 0 coincides with X1's
    Q1, e1 = rotation_between(X1[seg[1]], X2a[seg[1]])
    Q2, e2 = rotation_between(X1[seg[2]], X2a[seg[2]])
    a02 = axis_of(Q2)
    rA, rB, sg = reflection(a1, a2), reflection(a1, a02), reflection(a2, a02)
    if wrong_mirror:                      # planted error: sigma taken in the plane of the hinges
        sg = reflection(a1, a2)
    ident = max(np.abs(Q1 - rB @ rA).max(), np.abs(Q2 - rB @ sg).max(),
                np.abs(Q1.T @ Q2 - rA @ sg).max())
    out = {}
    for al, be, ga in itertools.product((0, 1), repeat=3):
        B1 = np.linalg.matrix_power(rB, be) @ np.linalg.matrix_power(rA, al)
        B2 = np.linalg.matrix_power(rB, be) @ np.linalg.matrix_power(sg, ga)
        Y = X1.copy()
        c1 = X1[h1 + 1]
        for i in seg[1]:
            Y[i] = c1 + B1 @ (X1[i] - c1)
        c2 = X1[h2 + 1]
        c2new = Y[h2 + 1]
        for i in seg[2]:
            if i > h2 + 2 or i in (h2 + 1, h2 + 2):
                Y[i] = c2new + B2 @ (X1[i] - c2)
        out[(al, be, ga)] = Y
    return out, ident, max(e0, e1, e2)


def lp_unique(Ds, M, states, w):
    """Range of each weight over {v >= 0 : sum v_c D_c = M}."""
    iu = np.triu_indices(M.shape[0], 1)
    A = np.array([D[iu] for D in Ds]).T
    b = M[iu]
    A = np.vstack([A, np.ones(len(Ds))])
    b = np.append(b, 1.0)
    rng = []
    for c in range(len(Ds)):
        lo = linprog(np.eye(len(Ds))[c], A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        hi = linprog(-np.eye(len(Ds))[c], A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        if lo.status != 0 or hi.status != 0:
            return None
        rng.append((lo.fun, -hi.fun))
    return rng


def search_affine_images(z, n, rng, nstart, known):
    """Zeros of X -> Pi_perp X over all chains (torsion space), clustered by distance matrix."""
    B = np.hstack([np.ones((n, 1)), z])
    Qb, _ = np.linalg.qr(B)

    def res(t):
        X = chain(n, t, theta=THETA)
        return (X - Qb @ (Qb.T @ X)).ravel()
    found = [edm(Y) for Y in known]
    new, conv = 0, 0
    for _ in range(nstart):
        r = least_squares(res, rng.uniform(-np.pi, np.pi, n - 3), method="lm", xtol=1e-15, ftol=1e-15)
        if np.abs(r.fun).max() < 1e-9:
            conv += 1
            D = edm(chain(n, r.x, theta=THETA))
            if min(np.abs(D - F).max() for F in found) > 1e-6:
                found.append(D)
                new += 1
    return conv, new


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    nstart = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = np.random.default_rng(seed)
    ok = True

    print("A. dim N(z) for two states that differ in s torsions (segments of 6 or more atoms):")
    for s, want in ((1, 10), (2, 6), (3, 3), (4, 1), (5, 1)):
        hinges = [4 + 5 * j for j in range(s)]
        n = hinges[-1] + 8
        X1, X2, _, _ = hinge_states(n, hinges, rng)
        z = stack([X1, X2], [0.4, 0.6])
        dimN = nullity(conic_matrix(z), 21)
        rk = np.linalg.matrix_rank(z - z.mean(0), tol=1e-9)
        print(f"   s = {s}: n = {n}, rank of the stack {rk}, dim N(z) = {dimN} (expected {want})")
        ok &= dimN == want

    print("B. two hinges: the cube of eight linear images, the parity relation, the linear programme")
    for trial in range(3):
        n, hinges = (11, [2, 5]) if trial == 0 else (16, [4, 9]) if trial == 1 else (14, [3, 7])
        X1, X2, _, _ = hinge_states(n, hinges, rng)
        w = np.array([0.35, 0.65])
        z = stack([X1, X2], w)
        zc = z - z.mean(0)
        cand, ident, cong = cube_candidates(X1, X2, hinges)
        Ds = {k: edm(Y) for k, Y in cand.items()}
        valid = all(e0_ok(Y) for Y in cand.values())
        aff = max(affine_residual(Y - Y.mean(0), zc) for Y in cand.values())
        is1 = np.abs(Ds[(0, 0, 0)] - edm(X1)).max()
        is2 = np.abs(Ds[(1, 1, 1)] - edm(X2)).max()
        keys = list(cand)
        distinct = min(np.abs(Ds[a] - Ds[b]).max() for a in keys for b in keys if a < b)
        parity = sum((-1) ** sum(k) * Ds[k] for k in keys)
        iu = np.triu_indices(n, 1)
        rank_aff = np.linalg.matrix_rank(np.array([Ds[k][iu] - Ds[keys[0]][iu] for k in keys[1:]]), tol=1e-8)
        M = w[0] * edm(X1) + w[1] * edm(X2)
        rngs = lp_unique([Ds[k] for k in keys], M, None, w)
        off = max(hi for k, (lo, hi) in zip(keys, rngs) if k not in ((0, 0, 0), (1, 1, 1)))
        w1 = rngs[keys.index((0, 0, 0))]
        w2 = rngs[keys.index((1, 1, 1))]
        conv, new = search_affine_images(zc, n, rng, nstart, list(cand.values()))
        good = (ident < 1e-9 and valid and aff < 1e-9 and is1 < 1e-9 and is2 < 1e-9 and distinct > 1e-3
                and np.abs(parity).max() < 1e-9 and rank_aff == 6 and off < 1e-8
                and abs(w1[0] - w[0]) < 1e-8 and abs(w1[1] - w[0]) < 1e-8
                and abs(w2[0] - w[1]) < 1e-8 and new == 0 and conv > 0)
        ok &= good
        print(f"   n = {n}, hinges at torsions {hinges}: R1 = rB rA, R2 = rA sg, R1R2 = rB sg to {ident:.1e}; "
              f"8 valid chains: {valid}; affine images of the stack to {aff:.1e}; "
              f"(0,0,0) = X1 to {is1:.1e}, (1,1,1) = X2 to {is2:.1e}; pairwise distinct (min max|dD| = {distinct:.2f}); "
              f"parity relation to {np.abs(parity).max():.1e}; affine rank {rank_aff}; "
              f"LP: weights on the six others at most {off:.1e}, w1 in [{w1[0]:.6f}, {w1[1]:.6f}], w2 in [{w2[0]:.6f}, {w2[1]:.6f}]; "
              f"search: {conv} of {nstart} starts converged, {new} new classes   {'OK' if good else 'FAIL'}")

    print("C. three hinges: affine images of the stack by search, linear programme")
    n, hinges = 21, [3, 8, 13]
    X1, X2, _, _ = hinge_states(n, hinges, rng)
    w = np.array([0.5, 0.5])
    z = stack([X1, X2], w)
    zc = z - z.mean(0)
    B = np.hstack([np.ones((n, 1)), zc])
    Qb, _ = np.linalg.qr(B)
    found = [edm(X1), edm(X2)]
    conv = 0
    for _ in range(nstart):
        r = least_squares(lambda t: (chain(n, t, theta=THETA) - Qb @ (Qb.T @ chain(n, t, theta=THETA))).ravel(),
                          rng.uniform(-np.pi, np.pi, n - 3), method="lm", xtol=1e-15, ftol=1e-15)
        if np.abs(r.fun).max() < 1e-9:
            conv += 1
            D = edm(chain(n, r.x, theta=THETA))
            if min(np.abs(D - F).max() for F in found) > 1e-6:
                found.append(D)
    M = 0.5 * found[0] + 0.5 * found[1]
    rngs = lp_unique(found, M, None, w)
    off = max([hi for (lo, hi) in rngs[2:]] + [0.0])
    good = rngs is not None and off < 1e-8 and abs(rngs[0][0] - 0.5) < 1e-8 and abs(rngs[0][1] - 0.5) < 1e-8
    ok &= good
    print(f"   n = {n}, hinges {hinges}: {conv} of {nstart} starts converged; {len(found)} classes of affine images "
          f"(the two states and {len(found) - 2} others); LP: weight off the states at most {off:.1e}   {'OK' if good else 'FAIL'}")
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
