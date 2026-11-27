#!/usr/bin/env python3
"""Numerical checks for Part VI of docs/ensemble/ENSEMBLE_REPORT.md (lifted certificates; what a prior on the
number of conformers buys; the torus).

L1  Cube, degree-2 lift xi(x) = (1, x_i x_j): frequency with which the span of the lifted vectors of K random
    conformers contains no other lifted vertex ("lift-isolated"; Baldi-Vershynin 2019, Theorem 4.2, is the
    asymptotic statement), for K up to the number of pair observables.
L2  Cube n = 8, data = all correlations of even order <= 4: whenever K random conformers are lift-isolated for
    the degree-2 lift, a linear programme over all 128 states confirms that an ensemble on them is the only
    ensemble with its data (Theorem E19(b)); the certificate ||P^perp xi(x)||^2 vanishes exactly on them.
L3  Cube n = 5 (16 states, 10 pair observables): NINE SAMPLED supports with 6 or 7 conformers, each tested
    against ALL competing supports of the same size (exhaustive in the competitors only; the exhaustive
    computation over all supports is in docs/ensemble/reviews/ER3_scripts/er3_e18prime.py).  For those that are
    flat-isolated but not faces: random weights — no other ensemble with at most K atoms has the same pair data
    (Proposition E18'); among all ensembles: not identified.  Also: whether SOME weights admit a twin.
L4  Torus: (a) the explicit two-state certificate sum_{k != l} |z_k - p_k|^2 |z_l - q_l|^2 vanishes exactly at
    the two states (r = 2..5 angles, states differing in at least two angles), and a grid linear programme
    confirms identification for r = 2; (b) generic K points on the 3-torus: the projector certificate has
    exactly K zeros for K = 4, exactly six for K = 5 (the sixth point of the secant 4-plane on the Segre
    variety), with linearly independent rank-one matrices on the zero set; r = 4, K = 11: exactly 11 zeros.
L5  Cube n = 6, all 4960 triples of states: the sign vectors in the span of three conformers are the three
    conformers and at most one more, with affinely independent pair features: an explicit certificate for
    "three conformers are always identified" (Proposition E9(a)).
L6  Proposition E20'': (a) the growth inequality f >= c* min(d_p^2, d_q^2) of the two-state certificate with
    the explicit constant c* = min(1, c_D), c_D = beta_min/4 if at least three angles differ and
    beta_1 beta_2 / (4 (beta_1 + beta_2)) if two do, on random and on adversarially minimised points of tori
    with r = 2..5 angles; (b) on a grid of the 2-torus, the largest value of
    int min(d_p^2, d_q^2) dnu over all measures whose eight product means are within tau of those of a
    two-state ensemble (a linear programme) against the bound Lambda tau / c*.
L7  Proposition E21 (the permanent certificate): (a) K = 3, 4 states on tori with r >= K angles that differ
    pairwise in every angle: every zero of the permanent found by multi-start minimisation is a state;
    (b) three states that coincide in all but two angles (the Hall condition fails): zeros away from the
    states exist; (c) the cube with n = 6: for all triples of conformers, the zero set of the energy
    perm(1 - x_k s^i_k) over the 64 states is the triple when the Hall condition holds; when it fails for a
    set I of states, the energy vanishes on every state that agrees with I where the states of I coincide
    (on binary sites that sub-cube may contain nothing but the states themselves).
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


# ---------------------------------------------------------------- L6
def two_state_setup(r, shared):
    """Random states p, q on the r-torus agreeing on `shared` angles; returns p, q, E (bool), constants."""
    p = rng.uniform(0, 2 * np.pi, size=r); q = rng.uniform(0, 2 * np.pi, size=r)
    E = np.zeros(r, dtype=bool); E[rng.choice(r, size=shared, replace=False)] = True
    q[E] = p[E]
    D = np.nonzero(~E)[0]
    beta = 2 - 2 * np.cos(p[D] - q[D])                      # squared chordal distances of the two states
    cD = beta.min() / 4 if len(D) >= 3 else beta[0] * beta[1] / (4 * (beta[0] + beta[1]))
    cstar = min(1.0, cD)
    return p, q, E, D, beta, cstar


def two_state_f(phi, p, q, E, D):
    a = 2 - 2 * np.cos(phi - p); b = 2 - 2 * np.cos(phi - q)
    F = a[D].sum() * b[D].sum() - (a[D] * b[D]).sum()        # sum over k != l in D of a_k b_l
    return a[E].sum() + F, a.sum(), b.sum()


def test_L6():
    out = []; ok = True
    worst = np.inf; cases = 0; skipped = 0
    for r in (2, 3, 4, 5):
        for shared in range(0, r - 1):
            for _ in range(6):
                p, q, E, D, beta, cstar = two_state_setup(r, shared)
                if beta.min() < 0.05:
                    skipped += 1
                    continue                                 # nearly coincident angles: constant tiny, skip

                def ratio(phi):
                    f, dp, dq = two_state_f(phi, p, q, E, D)
                    return f / max(min(dp, dq), 1e-300)
                best = min(ratio(x) for x in rng.uniform(0, 2 * np.pi, size=(3000, r)))
                for _ in range(12):                          # adversarial: minimise the ratio from random starts
                    res = minimize(ratio, rng.uniform(0, 2 * np.pi, size=r), method="Nelder-Mead",
                                   options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 4000})
                    f, dp, dq = two_state_f(res.x, p, q, E, D)
                    if min(dp, dq) > 1e-8:                   # away from the two states (there the ratio is a limit)
                        best = min(best, res.fun)
                worst = min(worst, best / cstar); cases += 1
                ok &= best >= cstar * (1 - 1e-9)
    out.append(f"    growth inequality, r = 2..5, {cases} random pairs of states ({skipped} further pairs with some "
               f"beta < 0.05 set aside): smallest observed f / (c* min(d_p^2, d_q^2)) = {worst:.2f} (must be >= 1)")
    # (b) stability on a grid of the 2-torus
    Gd = 30; ang = 2 * np.pi * np.arange(Gd) / Gd
    grid = np.array([(x, y) for x in ang for y in ang])
    fs = (np.cos, np.sin)
    feats = [f1(grid[:, 0]) for f1 in fs] + [f1(grid[:, 1]) for f1 in fs] + \
            [f1(grid[:, 0]) * f2(grid[:, 1]) for f1 in fs for f2 in fs]
    Fm = np.array(feats)                                     # 8 x N
    ratios = []
    for _ in range(4):
        i = rng.integers(len(grid))
        j = rng.choice([t for t in range(len(grid))
                        if min(abs(grid[t][0] - grid[i][0]), 2 * np.pi - abs(grid[t][0] - grid[i][0])) > 0.6
                        and min(abs(grid[t][1] - grid[i][1]), 2 * np.pi - abs(grid[t][1] - grid[i][1])) > 0.6])
        p, q = grid[i], grid[j]
        beta = 2 - 2 * np.cos(p - q); cstar = min(1.0, beta[0] * beta[1] / (4 * (beta[0] + beta[1])))
        # coefficient norm of f = a_1 b_2 + a_2 b_1 in the eight product observables
        cp, sp, cq, sq = np.cos(p), np.sin(p), np.cos(q), np.sin(q)
        lam = np.zeros(8)
        lam[0:2] += -4 * np.array([cp[0], sp[0]]) - 4 * np.array([cq[0], sq[0]])      # cos phi_1, sin phi_1
        lam[2:4] += -4 * np.array([cq[1], sq[1]]) - 4 * np.array([cp[1], sp[1]])      # cos phi_2, sin phi_2
        prod = 4 * (np.outer([cp[0], sp[0]], [cq[1], sq[1]]) + np.outer([cq[0], sq[0]], [cp[1], sp[1]]))
        lam[4:8] += prod.ravel()
        Lam = np.abs(lam).sum()
        a = 2 - 2 * np.cos(grid - p); b = 2 - 2 * np.cos(grid - q)
        fvals = a[:, 0] * b[:, 1] + a[:, 1] * b[:, 0]
        ok &= np.allclose(fvals, 8 + Fm.T @ lam, atol=1e-9)                           # the expansion is right
        target = np.minimum(a.sum(axis=1), b.sum(axis=1))
        mu = np.zeros(len(grid)); mu[i], mu[j] = 0.35, 0.65
        y = Fm @ mu
        for tau in (1e-3, 1e-2):
            A_ub = np.vstack([Fm, -Fm]); b_ub = np.concatenate([y + tau, -(y - tau)])
            res = linprog(-target, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, len(grid))), b_eq=[1.0],
                          bounds=[(0, None)] * len(grid), method="highs")
            val = -res.fun; bound = Lam * tau / cstar
            ok &= res.status == 0 and val <= bound * (1 + 1e-6)
            ratios.append(val / bound)
    out.append(f"    2-torus, 30 x 30 grid, four pairs of states, tau = 1e-3 and 1e-2: largest int min(d_p^2, d_q^2) dnu "
               f"over data-compatible measures is between {min(ratios):.3f} and {max(ratios):.3f} of the bound "
               f"Lambda tau / c* (must be <= 1)")
    return ok, out


# ---------------------------------------------------------------- L7
def permanent_rect(M):
    """Permanent of a K x r matrix (K <= r): sum over injective maps of the products."""
    K, r = M.shape
    return sum(np.prod([M[i, kap[i]] for i in range(K)]) for kap in itertools.permutations(range(r), K))


def test_L7():
    out = []; ok = True
    # (a) torus, states differing pairwise in every angle
    cases = 0; bad = 0
    for K, r in ((3, 3), (3, 4), (3, 5), (4, 4), (4, 5)):
        for _ in range(3):
            S = rng.uniform(0, 2 * np.pi, size=(K, r))

            def f(phi):
                return permanent_rect(2 - 2 * np.cos(phi[None, :] - S))
            zs = zeros_on_torus(f, r, 60)
            for z in zs:
                dist = min(np.max(np.abs(np.angle(np.exp(1j * (z - S[i]))))) for i in range(K))
                bad += dist > 1e-3
            ok &= all(f(S[i]) < 1e-12 for i in range(K))
            cases += 1
    ok &= bad == 0
    out.append(f"    torus, K = 3, 4 states differing pairwise in every angle ({cases} random cases, r = K..5): "
               f"zeros of the permanent that are not states: {bad}")
    # (b) Hall condition fails: three states that coincide in all but two of four angles
    S = rng.uniform(0, 2 * np.pi, size=(3, 4)); S[1, 2:] = S[0, 2:]; S[2, 2:] = S[0, 2:]

    def g(phi):
        return permanent_rect(2 - 2 * np.cos(phi[None, :] - S))
    probe = np.concatenate([rng.uniform(0, 2 * np.pi, size=2), S[0, 2:]])       # free in the two differing angles
    far = min(np.max(np.abs(np.angle(np.exp(1j * (probe - S[i]))))) for i in range(3))
    ok &= g(probe) < 1e-12 and far > 0.05
    out.append(f"    three states coinciding in two of four angles (Hall condition fails): the permanent vanishes at a "
               f"configuration at distance {far:.2f} from every state (value {g(probe):.1e})")
    # (c) cube, n = 6: all triples
    n = 6; X = np.array(list(itertools.product((-1, 1), repeat=n)))
    perms = list(itertools.permutations(range(n), 3))
    exact_when_hall = True; subcube_in_zero = True; n_hall = 0; n_fail = 0; n_fail_larger = 0; triples = 0
    for tri in itertools.combinations(range(len(X)), 3):
        St = X[list(tri)]; triples += 1
        A = 1 - X[:, None, :] * St[None, :, :]                                   # states x 3 x n, entries 0 or 2
        vals = np.zeros(len(X))
        for kap in perms:
            vals += A[:, 0, kap[0]] * A[:, 1, kap[1]] * A[:, 2, kap[2]]
        zero = set(np.nonzero(vals < 1e-12)[0].tolist())
        # the sets I of at least two states that violate the Hall condition
        violating = []
        for I in ((0, 1), (0, 2), (1, 2), (0, 1, 2)):
            coincide = np.all(St[list(I)] == St[I[0]], axis=0)                   # sites where the states of I agree
            if np.sum(~coincide) < len(I):
                violating.append((I, coincide))
        if not violating:
            n_hall += 1
            exact_when_hall &= zero == set(tri)
        else:
            n_fail += 1; n_fail_larger += len(zero) > 3
            for I, coincide in violating:
                sub = np.nonzero(np.all(X[:, coincide] == St[I[0]][coincide], axis=1))[0]
                subcube_in_zero &= set(sub.tolist()) <= zero
    ok &= exact_when_hall and subcube_in_zero and n_hall > 0 and n_fail > 0
    out.append(f"    cube n = 6, all {triples} triples: Hall condition holds in {n_hall}, zero set of the permanent "
               f"energy = the triple in all of them: {exact_when_hall}; fails in {n_fail}, the predicted sub-cube is "
               f"in the zero set in all of them: {subcube_in_zero} (zero set strictly larger than the triple in "
               f"{n_fail_larger})")
    return ok, out


def main():
    allok = True
    for name, fn in (("L1 lift isolation on the cube", test_L1), ("L2 four-body data", test_L2),
                     ("L3 a prior on the number of conformers", test_L3), ("L4 torus", test_L4),
                     ("L5 three conformers", test_L5), ("L6 certified stability on the torus", test_L6),
                     ("L7 the permanent certificate", test_L7)):
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
