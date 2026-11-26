#!/usr/bin/env python3
"""Numerical checks for Part VI of docs/ensemble/ENSEMBLE_REPORT.md (lifted certificates; what a prior on the
number of conformers buys; the torus).

L1  Cube, degree-2 lift xi(x) = (1, x_i x_j): frequency with which the span of the lifted vectors of K random
    conformers contains no other lifted vertex ("lift-isolated"; Baldi-Vershynin 2019, Theorem 4.2, is the
    asymptotic statement), for K up to the number of pair observables.
L2  Cube n = 8, data = all correlations of even order <= 4: whenever K random conformers are lift-isolated for
    the degree-2 lift, a linear programme over all 128 states confirms that an ensemble on them is the only
    ensemble with its data (Theorem E19(b)); the certificate ||P^perp xi(x)||^2 vanishes exactly on them.
L3  Cube n = 5 (16 states, 10 pair observables), exhaustive: supports that are flat-isolated but not faces.
    Random weights: no other ensemble with at most K atoms has the same pair data (Proposition E18');
    among all ensembles: not identified.  Also: whether SOME weights admit a twin with at most K atoms.
L4  Torus: (a) the explicit two-state certificate sum_{k != l} |z_k - p_k|^2 |z_l - q_l|^2 vanishes exactly at
    the two states (r = 2..5 angles, states differing in at least two angles), and a grid linear programme
    confirms identification for r = 2; (b) generic K points on the 3-torus: the projector certificate has
    exactly K zeros for K = 4, exactly six for K = 5 (the sixth point of the secant 4-plane on the Segre
    variety), with linearly independent rank-one matrices on the zero set; r = 4, K = 11: exactly 11 zeros.
L5  Cube n = 6, all 4960 triples of states: the sign vectors in the span of three conformers are the three
    conformers and at most one more, with affinely independent pair features: an explicit certificate for
    "three conformers are always identified" (Proposition E9(a)).
Exit code 0 iff every check passes.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog, nnls, minimize

rng = np.random.default_rng(20261204)


def cube_mod_flip(n):
    Z = np.array(list(itertools.product((-1, 1), repeat=n - 1)))
    return np.hstack([np.ones((len(Z), 1), dtype=int), Z])


def pair_lift(Y):
    n = Y.shape[1]; iu = np.triu_indices(n, 1)
    return np.hstack([np.ones((len(Y), 1)), (Y[:, iu[0]] * Y[:, iu[1]]).astype(float)])


def even_monomials(Y, order):
    n = Y.shape[1]; cols = [np.ones(len(Y))]
    for k in range(2, order + 1, 2):
        for A in itertools.combinations(range(n), k):
            cols.append(np.prod(Y[:, A], axis=1).astype(float))
    return np.array(cols).T


def zero_set_of_projector(Xi, idx, tol=1e-7):
    """Indices y with Xi[y] in span Xi[idx]; None if Xi[idx] is rank deficient."""
    B = Xi[idx].T
    s = np.linalg.svd(B, compute_uv=False)
    if len(idx) > B.shape[0] or s[-1] < 1e-9 * s[0]:
        return None
    Q, _ = np.linalg.qr(B)
    res = np.linalg.norm(Xi - (Xi @ Q) @ Q.T, axis=1)
    return np.nonzero(res < tol)[0]


def fibre_is_point(F, idx, w):
    """Is the ensemble sum w_a delta_{idx[a]} the only probability vector on the N points with its data F^T mu?"""
    N = F.shape[0]
    mu = np.zeros(N); mu[idx] = w
    A_eq = F.T; b_eq = A_eq @ mu
    c = -np.ones(N); c[idx] = 0
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N, method="highs")
    if res.status != 0 or -res.fun > 1e-8:
        return False
    return np.linalg.matrix_rank(F[idx], tol=1e-9) == len(idx)


# ---------------------------------------------------------------- L1
def test_L1():
    out = []; ok = True
    for n, trials in ((10, 200), (12, 200)):
        Y = cube_mod_flip(n); Xi = pair_lift(Y); N = len(Y); m = n * (n - 1) // 2
        row = []
        for K in (2 * n, m // 2, (3 * m) // 4, m - n, m):
            iso = 0
            for _ in range(trials):
                idx = rng.choice(N, size=K, replace=False)
                Zs = zero_set_of_projector(Xi, idx)
                iso += Zs is not None and len(Zs) == K
            row.append((K, iso / trials))
        out.append(f"    n = {n} ({m} pair observables): lift-isolated frequency " +
                   ", ".join(f"K = {K}: {p:.3f}" for K, p in row))
        ok &= row[0][1] > 0.97 and row[1][1] > 0.97          # K = 2n and K = m/2: far beyond the face threshold
    return ok, out


# ---------------------------------------------------------------- L2
def test_L2():
    n = 8; Y = cube_mod_flip(n); Xi = pair_lift(Y); F4 = even_monomials(Y, 4); N = len(Y)
    tested = confirmed = not_isolated = 0
    for K in (12, 16, 20, 24):
        for _ in range(12):
            idx = rng.choice(N, size=K, replace=False)
            Zs = zero_set_of_projector(Xi, idx)
            if Zs is None or len(Zs) != K:
                not_isolated += 1; continue
            tested += 1
            confirmed += fibre_is_point(F4, idx, rng.dirichlet(np.ones(K)))
    return tested > 20 and confirmed == tested, \
        [f"    n = 8, 4-body data ({F4.shape[1]} features): {tested} lift-isolated supports with K = 12..24 "
         f"(the pair-data capacity is below 2n = 16): identification confirmed by the fibre LP in {confirmed}; "
         f"{not_isolated} supports not isolated (skipped)"]


# ---------------------------------------------------------------- L3
def test_L3():
    n = 5; Y = cube_mod_flip(n); G = pair_lift(Y); N = len(Y)

    def is_face(idx):
        mask = np.ones(N, bool); mask[idx] = False
        res = linprog(np.zeros(G.shape[1]), A_ub=-G[mask], b_ub=-np.ones(mask.sum()), A_eq=G[idx],
                      b_eq=np.zeros(len(idx)), bounds=[(None, None)] * G.shape[1], method="highs")
        return res.status == 0

    def twin_random_weights(idx, w):
        b = G[idx].T @ w; S = set(idx.tolist())
        for Sp in itertools.combinations(range(N), len(idx)):
            if set(Sp) == S:
                continue
            _, r = nnls(G[list(Sp)].T, b)
            if r < 1e-9:
                return True
        return False

    def twin_some_weights(idx):
        S = set(idx.tolist()); K = len(idx); GS = G[idx].T
        for Sp in itertools.combinations(range(N), K):
            if set(Sp) == S:
                continue
            GP = G[list(Sp)].T
            c = np.zeros(2 * K + 1); c[-1] = -1
            A_eq = np.hstack([GS, -GP, np.zeros((G.shape[1], 1))])
            A_ub = np.hstack([-np.eye(K), np.zeros((K, K)), np.ones((K, 1))])
            res = linprog(c, A_ub=A_ub, b_ub=np.zeros(K), A_eq=A_eq, b_eq=np.zeros(G.shape[1]),
                          bounds=[(0, 1)] * K + [(0, None)] * K + [(0, 1)], method="highs")
            if res.status == 0 and -res.fun > 1e-7:
                return True
        return False

    out = []; ok = True
    isolated_nonface = generic_twin = special_twin = faces = face_twin = 0
    for K, trials in ((6, 5), (7, 4)):
        for _ in range(trials):
            idx = np.sort(rng.choice(N, size=K, replace=False))
            Zs = zero_set_of_projector(G, idx)
            if Zs is None or len(Zs) != K:
                continue
            f = is_face(idx)
            ct = twin_random_weights(idx, rng.dirichlet(3 * np.ones(K)))
            generic_twin += ct
            if f:
                faces += 1
                continue
            isolated_nonface += 1
            st = twin_some_weights(idx)
            special_twin += st
    ok &= generic_twin == 0 and isolated_nonface >= 3
    out.append(f"    n = 5, K = 6, 7: {isolated_nonface} supports flat-isolated but not faces (not identified among all "
               f"ensembles), {faces} faces; random weights with a twin of at most K atoms: {generic_twin} (expected 0); "
               f"non-faces for which SOME weights have such a twin: {special_twin} of {isolated_nonface}")
    return ok, out


# ---------------------------------------------------------------- L4
def torus_lift(phi):
    """phi: (M, r) angles -> (M, 2^r) vectors  tensor_k (1, e^{i phi_k})."""
    M, r = phi.shape
    V = np.ones((M, 1), dtype=complex)
    for k in range(r):
        zk = np.exp(1j * phi[:, k])[:, None]
        V = np.hstack([V, V * zk])
    return V


def projector_certificate(points):
    B = torus_lift(points).T                                # 2^r x K
    Q, _ = np.linalg.qr(B)

    def f(phi):
        v = torus_lift(np.atleast_2d(phi))[0]
        return float(np.real(np.vdot(v, v) - np.vdot(Q.conj().T @ v, Q.conj().T @ v)))
    return f, Q


def zeros_on_torus(f, r, starts, tol=1e-10):
    """Distinct zeros of a non-negative function on the r-torus found by multi-start minimisation.  A run counts
    only if, after a second (polishing) minimisation, the value is below tol; zeros closer than 1e-2 in every
    angle are merged (a zero of a non-negative function is degenerate, so single runs stop at distance about
    sqrt(tol) from it)."""
    found = []
    for _ in range(starts):
        res = minimize(f, rng.uniform(0, 2 * np.pi, size=r), method="BFGS", options={"gtol": 1e-10})
        if res.fun > 1e-6:
            continue
        res = minimize(f, res.x, method="BFGS", options={"gtol": 1e-14})
        if res.fun < tol:
            p = np.mod(res.x, 2 * np.pi)
            if not any(np.max(np.abs(np.angle(np.exp(1j * (p - q))))) < 1e-2 for q in found):
                found.append(p)
    return found


def test_L4():
    out = []; ok = True
    # (a) explicit two-state certificate
    worst = np.inf; cases = 0
    for r in (2, 3, 4, 5):
        for _ in range(10):
            p = rng.uniform(0, 2 * np.pi, size=r); q = rng.uniform(0, 2 * np.pi, size=r)
            E = rng.random(r) < 0.3
            if r - E.sum() < 2:
                E[:] = False
            q[E] = p[E]                                     # the two states agree on the angles in E
            D = np.nonzero(~E)[0]

            def f(phi):
                a = 2 - 2 * np.cos(phi - p); b = 2 - 2 * np.cos(phi - q)
                val = a[E].sum()
                for k in D:
                    for l in D:
                        if k != l:
                            val += a[k] * b[l]
                return val
            zs = zeros_on_torus(f, r, 60)
            good = all(min(np.max(np.abs(np.angle(np.exp(1j * (z - p))))), np.max(np.abs(np.angle(np.exp(1j * (z - q)))))) < 1e-3
                       for z in zs)
            ok &= good and f(p) < 1e-12 and f(q) < 1e-12
            # smallest value on random points at distance >= 0.3 from both states
            R = rng.uniform(0, 2 * np.pi, size=(4000, r))
            far = [x for x in R if min(np.max(np.abs(np.angle(np.exp(1j * (x - p))))),
                                       np.max(np.abs(np.angle(np.exp(1j * (x - q)))))) > 0.3]
            worst = min(worst, min(f(x) for x in far)); cases += 1
    out.append(f"    two-state certificate on the r-torus, r = 2..5, {cases} random pairs (some angles shared): every zero "
               f"found is one of the two states; smallest value at distance > 0.3 from both: {worst:.3f}")
    ok &= worst > 1e-3
    # grid LP for r = 2
    Gd = 24; ang = 2 * np.pi * np.arange(Gd) / Gd
    grid = np.array([(a, b) for a in ang for b in ang])
    feats = np.array([[fa(x[0]) * fb(x[1]) for fa in (lambda t: 1.0, np.cos, np.sin) for fb in (lambda t: 1.0, np.cos, np.sin)]
                      for x in grid])
    ident = nonident = 0
    for _ in range(10):
        i, j = rng.choice(len(grid), size=2, replace=False)
        differ = int(grid[i][0] != grid[j][0]) + int(grid[i][1] != grid[j][1])   # int: numpy booleans do not add
        res = fibre_is_point(feats, np.array([i, j]), np.array([0.3, 0.7]))
        if differ == 2:
            ident += res
            ok &= res
        else:
            nonident += (not res)
            ok &= not res
    # pairs that differ in one angle only (grid points 0 and 5, 0 and 7*Gd share the other angle)
    for i, j in ((0, 5), (0, 7 * Gd)):
        res = fibre_is_point(feats, np.array([i, j]), np.array([0.3, 0.7])); ok &= not res; nonident += (not res)
    out.append(f"    2-torus, 24 x 24 grid, nine product observables: two states differing in both angles identified in "
               f"{ident} sampled cases; differing in one angle: not identified in {nonident} case(s)")
    # (b) generic points: zero set of the projector certificate
    for r, K, expect in ((3, 4, 4), (3, 5, 6), (4, 11, 11)):
        pts = rng.uniform(0, 2 * np.pi, size=(K, r))
        f, Q = projector_certificate(pts)
        zs = zeros_on_torus(f, r, 400 if r == 3 else 1500)
        V = torus_lift(np.array(zs))
        # real-linear independence of the rank-one matrices v v^* on the zero set
        mats = np.array([np.outer(v, v.conj()).ravel() for v in V])
        M = np.hstack([mats.real, mats.imag])
        indep = np.linalg.matrix_rank(M, tol=1e-8) == len(zs)
        out.append(f"    r = {r}, K = {K} generic points: {len(zs)} zeros of the projector certificate found "
                   f"(expected {expect}); rank-one matrices on the zero set linearly independent: {indep}")
        ok &= len(zs) == expect and indep
    return ok, out


# ---------------------------------------------------------------- L5
def test_L5():
    n = 6; Y = cube_mod_flip(n).astype(float); G = pair_lift(Y); N = len(Y)
    worst_extra = 0; dependent = 0; triples = 0; with_extra = 0
    for tri in itertools.combinations(range(N), 3):
        idx = np.array(tri)
        Zs = zero_set_of_projector(Y, idx, tol=1e-9)        # sign vectors (first coordinate +1) in the span
        Zs2 = zero_set_of_projector(-Y, idx, tol=1e-9)      # the same set (the span is symmetric); kept as a self-check
        assert Zs is not None and set(Zs) == set(Zs2)
        triples += 1
        extra = len(Zs) - 3; worst_extra = max(worst_extra, extra); with_extra += extra > 0
        dependent += np.linalg.matrix_rank(G[Zs], tol=1e-9) < len(Zs)
    return worst_extra <= 1 and dependent == 0, \
        [f"    n = 6: {triples} triples of conformers; sign vectors in the span beyond the three: at most {worst_extra} "
         f"(present in {with_extra} triples); zero sets with affinely dependent pair features: {dependent}"]


def main():
    allok = True
    for name, fn in (("L1 lift isolation on the cube", test_L1), ("L2 four-body data", test_L2),
                     ("L3 a prior on the number of conformers", test_L3), ("L4 torus", test_L4),
                     ("L5 three conformers", test_L5)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
        sys.stdout.flush()
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
