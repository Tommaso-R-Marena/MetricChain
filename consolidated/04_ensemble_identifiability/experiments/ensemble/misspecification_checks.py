#!/usr/bin/env python3
"""Checks for docs/ensemble/ENSEMBLE_REPORT.md, Part VIII (section 4e: Propositions E27-E29) and Proposition E23.1.

M1  Several unknown gains and offsets (Proposition E23.1): the criterion (Theorem E1(a) for the projected
    features) against a direct search for a second compatible ensemble, on random instances with integer data.
M2  Convex data and two time scales (Proposition E27): convexity of D_B(nu) = sum_k nu(B_k) g(E_nu[phi | B_k]),
    the bracket g(E phi) <= D_B <= E g(phi), monotonicity under refinement of the partition, and the convex
    outer bound, for g = square, g = exp and g = |.|^3; the variance is concave.
M3  A library that misses configurations (Proposition E28): the certified lower bound on the missing mass
    against the linear programme, with the exact support function and with box bounds on the observables.
M4  The number of conformers (Proposition E29): K_max = size of the preimage of the minimal face, K_min by
    exhaustive search, the rank bound for pair data on a small cube, and the reduction from exact cover.

Random seeds are fixed.  Linear programmes: scipy HiGHS.  About one minute.
"""
import itertools
import sys

import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261126)
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"  {name}: {'ok' if cond else 'FAILED'}")


def lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, n=None):
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method="highs")


# ---------------------------------------------------------------------------------------------------------- M1
def proj_orth(vectors, dim):
    """orthogonal projector onto the orthogonal complement of span(vectors) in R^dim"""
    if len(vectors) == 0:
        return np.eye(dim)
    Q, _ = np.linalg.qr(np.array(vectors, dtype=float).T)
    return np.eye(dim) - Q @ Q.T


def exposed_and_independent(Feat, S, tol=1e-8):
    """Theorem E1(a) for the features Feat (N x k): affine independence on S and an exposing certificate."""
    N = Feat.shape[0]
    Aff = np.hstack([np.ones((N, 1)), Feat])
    if np.linalg.matrix_rank(Aff[S], tol=1e-7) < len(S):
        return False
    off = [x for x in range(N) if x not in S]
    if not off:
        return True
    # find coefficients a with Aff[S] a = 0 and Aff[off] a >= 1
    k = Aff.shape[1]
    res = linprog(np.zeros(k), A_ub=-Aff[off], b_ub=-np.ones(len(off)), A_eq=Aff[S], b_eq=np.zeros(len(S)),
                  bounds=[(None, None)] * k, method="highs")
    return res.status == 0


def second_compatible(Feat, dirs, mu, tol=1e-7):
    """Is there an ensemble nu != mu with  E_nu Feat = 0  and  dirs_g . E_nu Psi_g >= 0 (closure of the compatible
    set; a point of the closure different from mu gives a compatible one by convexity)?  Feat: N x k (the projected
    features, whose means vanish for compatible ensembles); dirs: list of vectors on X (y_g . Psi_g(x))."""
    N = Feat.shape[0]
    A_eq = np.vstack([Feat.T, np.ones((1, N))])
    b_eq = np.concatenate([np.zeros(Feat.shape[1]), [1.0]])
    A_ub = -np.array(dirs) if dirs else None
    b_ub = np.zeros(len(dirs)) if dirs else None
    for x in range(N):
        for sign in (1.0, -1.0):
            c = np.zeros(N)
            c[x] = sign
            res = lp(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, n=N)
            if res.status != 0:
                return None
            if abs(res.x[x] - mu[x]) > tol:
                return True
    return False


def test_M1():
    print("M1  several unknown gains and offsets (Proposition E23.1)")
    agree = total = determined = 0
    while total < 300:
        N = int(rng.integers(4, 8))
        groups = [int(rng.integers(2, 5)) for _ in range(int(rng.integers(1, 4)))]
        offsets = [bool(rng.integers(0, 2)) and mg >= 3 for mg in groups]       # offset space R.1 in some groups
        Phis = [rng.integers(-2, 3, size=(N, mg)).astype(float) for mg in groups]
        K = int(rng.integers(1, 4))
        S = sorted(rng.choice(N, size=K, replace=False).tolist())
        mu = np.zeros(N)
        mu[S] = rng.integers(1, 5, size=K)
        mu /= mu.sum()
        feats, dirs, bad = [], [], False
        for Phi, mg, off in zip(Phis, groups, offsets):
            P = proj_orth([np.ones(mg)] if off else [], mg)
            Psi = Phi @ P                                                   # rows: P Phi_g(x)
            yhat = mu @ Psi                                                 # P y_g up to the unknown factor
            if np.linalg.norm(yhat) < 1e-9:
                bad = True
                break
            Qg = proj_orth([yhat], mg)
            feats.append(Psi @ Qg)
            dirs.append(Psi @ yhat)
        if bad:
            continue
        Feat = np.hstack(feats)
        crit = exposed_and_independent(Feat, S)
        direct = second_compatible(Feat, dirs, mu)
        if direct is None:
            continue
        total += 1
        agree += (crit == (not direct))
        determined += crit
    print(f"    {total} random instances (1 to 3 groups of 2 to 4 integer observables, an unknown gain in every group and"
          f" an unknown common offset in some): the criterion and the direct search agree in {agree}/{total}"
          f" ({determined} determined up to the gains and offsets)")
    check("criterion of E23.1 against the direct search", agree == total and 0 < determined < total)
    # worked example: two groups of two data with separate gains; one common gain identifies, two do not
    Phi = np.array([[1.0, 0, 1, 0], [0, 1, 0, 1], [1, 1, 2, 1], [1, 0, 0, 2]])
    mu = np.array([0.5, 0.5, 0, 0])
    one = proj_orth([mu @ Phi], 4)
    two = [proj_orth([mu @ Phi[:, :2]], 2), proj_orth([mu @ Phi[:, 2:]], 2)]
    crit1 = exposed_and_independent(Phi @ one, [0, 1])
    crit2 = exposed_and_independent(np.hstack([Phi[:, :2] @ two[0], Phi[:, 2:] @ two[1]]), [0, 1])
    print(f"    example (four configurations, four data): determined with one common gain: {crit1}; with a separate gain"
          f" for each pair of data: {crit2}")
    check("the example: one gain keeps identification, two gains lose it", crit1 and not crit2)


# ---------------------------------------------------------------------------------------------------------- M2
def D_partition(nu, phi, blocks, g):
    tot = 0.0
    for B in blocks:
        s = nu[B].sum()
        if s > 0:
            tot += s * g((nu[B] @ phi[B]) / s)
    return tot


def random_partition(N, k):
    lab = rng.integers(0, k, size=N)
    return [np.where(lab == j)[0] for j in range(k) if np.any(lab == j)]


def test_M2():
    print("M2  convex data and two time scales (Proposition E27)")
    gs = [("square", lambda m: m * m), ("exp", np.exp), ("cube of the modulus", lambda m: abs(m) ** 3)]
    worst_conv = worst_low = worst_up = worst_ref = 0.0
    cases = 0
    for name, g in gs:
        for _ in range(400):
            N = int(rng.integers(4, 11))
            phi = rng.normal(size=N)
            blocks = random_partition(N, int(rng.integers(1, 5)))
            nu0, nu1 = rng.dirichlet(np.ones(N)), rng.dirichlet(np.ones(N))
            if rng.random() < 0.3:                                     # an ensemble that misses a block
                nu0[blocks[0]] = 0
                if nu0.sum() == 0:
                    continue
                nu0 /= nu0.sum()
            lam = rng.random()
            mix = lam * nu0 + (1 - lam) * nu1
            Dm = D_partition(mix, phi, blocks, g)
            worst_conv = max(worst_conv, Dm - lam * D_partition(nu0, phi, blocks, g) - (1 - lam) * D_partition(nu1, phi, blocks, g))
            worst_low = max(worst_low, g(mix @ phi) - Dm)
            worst_up = max(worst_up, Dm - mix @ np.array([g(v) for v in phi]))
            # refinement: split the first block in two
            B = blocks[0]
            if len(B) >= 2:
                cut = int(rng.integers(1, len(B)))
                finer = [B[:cut], B[cut:]] + blocks[1:]
                worst_ref = max(worst_ref, Dm - D_partition(mix, phi, finer, g))
            cases += 1
    print(f"    {cases} random cases (g = square, exp, cube of the modulus; random partitions): largest violation of"
          f" convexity {max(worst_conv, 0):.1e}, of g(E phi) <= D {max(worst_low, 0):.1e}, of D <= E g(phi)"
          f" {max(worst_up, 0):.1e}, of monotonicity under refinement {max(worst_ref, 0):.1e}")
    check("D_B is convex, bracketed by the two limits, and increases under refinement",
          max(worst_conv, worst_low, worst_up, worst_ref) < 1e-10)
    # the convex outer bound for g = square is a polytope: |E phi| <= sqrt(y + tau), E phi^2 >= y - tau
    inside = total = 0
    width_true = width_outer = 0.0
    for _ in range(200):
        N = int(rng.integers(5, 10))
        phi = rng.normal(size=N)
        psi = rng.normal(size=N)
        blocks = random_partition(N, int(rng.integers(1, 5)))
        nu = rng.dirichlet(np.ones(N))
        y = D_partition(nu, phi, blocks, lambda m: m * m)
        A_ub = np.vstack([phi, -phi, -(phi ** 2)])
        b_ub = np.array([np.sqrt(y), np.sqrt(y), -y])
        lo = lp(psi, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, N)), b_eq=[1.0], n=N)
        hi = lp(-psi, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, N)), b_eq=[1.0], n=N)
        total += 1
        inside += (lo.status == 0 and hi.status == 0 and lo.fun - 1e-9 <= nu @ psi <= -hi.fun + 1e-9)
    print(f"    g = square: the ensemble that generated the datum (with a random, 'unknown' partition) lies in the convex"
          f" outer bound, and its target value in the interval computed from it, in {inside}/{total} cases")
    check("the outer bound contains the truth whatever the partition", inside == total)
    # variance is concave
    worst = 0.0
    for _ in range(1000):
        N = int(rng.integers(3, 9))
        phi = rng.normal(size=N)
        nu0, nu1 = rng.dirichlet(np.ones(N)), rng.dirichlet(np.ones(N))
        lam = rng.random()
        var = lambda nu: nu @ phi ** 2 - (nu @ phi) ** 2
        worst = max(worst, lam * var(nu0) + (1 - lam) * var(nu1) - var(lam * nu0 + (1 - lam) * nu1))
    print(f"    variance: largest violation of concavity in 1000 random cases {max(worst, 0):.1e}")
    check("the variance is concave in the ensemble", worst < 1e-12)


# ---------------------------------------------------------------------------------------------------------- M3
def test_M3():
    print("M3  a library that misses configurations (Proposition E28)")
    gap_exact = gap_box = 0.0
    valid = falsified = cases = 0
    tight = 0
    while cases < 150:
        N = int(rng.integers(8, 15))
        m = int(rng.integers(2, 5))
        Phi = rng.uniform(-1, 1, size=(N, m))
        lib = sorted(rng.choice(N, size=int(rng.integers(3, N - 2)), replace=False).tolist())
        out = [x for x in range(N) if x not in lib]
        mu = np.zeros(N)
        eps_true = rng.uniform(0.05, 0.6)
        mu[lib] = rng.dirichlet(np.ones(len(lib))) * (1 - eps_true)
        mu[out] = rng.dirichlet(np.ones(len(out))) * eps_true
        y = mu @ Phi
        tau = 0.01                                              # tolerance in the sup norm
        # primal: least mass outside the library among ensembles on X_true with |E Phi - y|_inf <= tau
        c = np.zeros(N)
        c[out] = 1.0
        A_ub = np.vstack([Phi.T, -Phi.T])
        b_ub = np.concatenate([y + tau, -(y - tau)])
        res = lp(c, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, N)), b_eq=[1.0], n=N)
        eps_min = res.fun
        # dual bound: maximise over lambda  (lambda.y - |lambda|_1 tau - h_lib(lambda)) / (h_true(lambda) - h_lib(lambda)),
        # normalised by h_true - h_lib <= 1: variables lambda = p - q (p, q >= 0), a = h_lib, b = h_true
        nv = 2 * m + 2
        cost = np.concatenate([-(y - tau), (y + tau), [1.0, 0.0]])        # minimise -(lam.y - tau|lam|_1 - a)
        rows, rhs = [], []
        for x in lib:                                                     # lam.Phi(x) <= a
            rows.append(np.concatenate([Phi[x], -Phi[x], [-1.0, 0.0]])); rhs.append(0.0)
        for x in range(N):                                                # lam.Phi(x) <= b
            rows.append(np.concatenate([Phi[x], -Phi[x], [0.0, -1.0]])); rhs.append(0.0)
        rows.append(np.concatenate([np.zeros(2 * m), [-1.0, 1.0]])); rhs.append(1.0)   # b - a <= 1
        dres = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs),
                       bounds=[(0, None)] * (2 * m) + [(None, None)] * 2, method="highs")
        dual = max(0.0, -dres.fun)
        # the same with box bounds on the observables in place of the exact support function of X_true
        lo_box, hi_box = -np.ones(m), np.ones(m)
        rows2, rhs2 = [], []
        for x in lib:
            rows2.append(np.concatenate([Phi[x], -Phi[x], [-1.0, 0.0]])); rhs2.append(0.0)
        # h_box(lam) = sum_i max(lam_i lo_i, lam_i hi_i) = sum_i (p_i hi_i - q_i lo_i) for p, q >= 0 (an upper bound) <= b
        rows2.append(np.concatenate([hi_box, -lo_box, [0.0, -1.0]])); rhs2.append(0.0)
        rows2.append(np.concatenate([np.zeros(2 * m), [-1.0, 1.0]])); rhs2.append(1.0)
        bres = linprog(cost, A_ub=np.array(rows2), b_ub=np.array(rhs2),
                       bounds=[(0, None)] * (2 * m) + [(None, None)] * 2, method="highs")
        box = max(0.0, -bres.fun)
        cases += 1
        gap_exact = max(gap_exact, abs(dual - eps_min))
        valid += (box <= eps_min + 1e-9 and eps_min <= eps_true + 1e-9)
        gap_box = max(gap_box, eps_min - box)
        falsified += eps_min > 1e-9
        tight += box > 1e-9
    print(f"    {cases} random instances: the library is falsified (no ensemble on it fits) in {falsified}; the certified"
          f" bound with the exact support function equals the least missing mass (largest difference {gap_exact:.1e});"
          f" with box bounds on the observables it is a valid lower bound in {valid}/{cases} (positive in {tight};"
          f" largest loss {gap_box:.3f})")
    check("lower bounds on the missing mass: tight with the support function, valid with box bounds",
          gap_exact < 1e-7 and valid == cases and falsified > 0)


# ---------------------------------------------------------------------------------------------------------- M4
def support_union(Phi, y):
    """X_G: the configurations that some compatible ensemble charges (finite X): one LP per configuration."""
    N = Phi.shape[0]
    A_eq = np.vstack([Phi.T, np.ones((1, N))])
    b_eq = np.concatenate([y, [1.0]])
    S = []
    for x in range(N):
        c = np.zeros(N)
        c[x] = -1.0
        res = lp(c, A_eq=A_eq, b_eq=b_eq, n=N)
        if res.status == 0 and -res.fun > 1e-9:
            S.append(x)
    return S


def feasible_on(Phi, y, sub):
    A_eq = np.vstack([Phi[sub].T, np.ones((1, len(sub)))])
    b_eq = np.concatenate([y, [1.0]])
    return lp(np.zeros(len(sub)), A_eq=A_eq, b_eq=b_eq, n=len(sub)).status == 0


def k_min(Phi, y, candidates):
    for k in range(1, len(candidates) + 1):
        for sub in itertools.combinations(candidates, k):
            if feasible_on(Phi, y, list(sub)):
                return k
    return None


def test_M4():
    print("M4  the number of conformers (Proposition E29)")
    okk = cases = interior = boundary = 0
    for trial in range(120):
        N = int(rng.integers(5, 10))
        m = int(rng.integers(1, 4))
        Phi = rng.integers(-2, 3, size=(N, m)).astype(float)
        K = int(rng.integers(1, 4))
        S = sorted(rng.choice(N, size=K, replace=False).tolist())
        mu = np.zeros(N)
        mu[S] = rng.dirichlet(np.ones(K))
        y = mu @ Phi
        XG = support_union(Phi, y)
        kmin = k_min(Phi, y, XG)
        # a relative interior point of the fibre charges all of X_G: average of the LP maximisers
        kmax_attained = len(XG)
        dimG = np.linalg.matrix_rank(np.hstack([np.ones((len(XG), 1)), Phi[XG]])) - 1
        cases += 1
        okk += (set(S) <= set(XG) and kmin is not None and kmin <= K <= kmax_attained and kmin <= dimG + 1)
        interior += len(XG) == N
        boundary += len(XG) < N
    print(f"    {cases} random instances (integer observables): supp(mu) in X_G and K_min <= |supp mu| <= K_max = |X_G|,"
          f" K_min <= dim G + 1, in {okk}/{cases}; the data bound the number of conformers from above"
          f" (|X_G| < |X|) in {boundary}")
    check("K_min <= |supp| <= K_max = |X_G| and the Caratheodory bound", okk == cases and boundary > 0 and interior > 0)
    # rank bound: pair data on the cube {+-1}^5 modulo the flip; K >= rank E[x x^T]
    n = 5
    states = np.array([s for s in itertools.product((1, -1), repeat=n) if s[0] == 1], dtype=float)
    pairs = list(itertools.combinations(range(n), 2))
    Phi = np.array([[s[i] * s[j] for i, j in pairs] for s in states])
    good = sharp = cases2 = 0
    for _ in range(40):
        K = int(rng.integers(1, 6))
        S = sorted(rng.choice(len(states), size=K, replace=False).tolist())
        mu = np.zeros(len(states))
        mu[S] = rng.dirichlet(np.ones(K))
        y = mu @ Phi
        M = np.eye(n)
        for (i, j), v in zip(pairs, y):
            M[i, j] = M[j, i] = v
        rank = int(np.sum(np.linalg.eigvalsh(M) > 1e-9))
        kmin = k_min(Phi, y, support_union(Phi, y))
        cases2 += 1
        good += rank <= kmin <= K
        sharp += rank == kmin
        # noise: Weyl -- the number of eigenvalues of a perturbed matrix above the size of the perturbation
        Epert = rng.normal(size=(n, n)) * 1e-3
        Epert = (Epert + Epert.T) / 2
        eta = np.linalg.norm(Epert, 2)
        good_noise = int(np.sum(np.linalg.eigvalsh(M + Epert) > eta)) <= kmin
        good += 0 if good_noise else -1000
    print(f"    pair data on the cube with five sites: rank of the correlation matrix <= K_min <= number of conformers"
          f" in {good}/{cases2} (rank = K_min in {sharp}); the noisy version (eigenvalues above the norm of the"
          f" perturbation) never exceeds K_min")
    check("the rank bound and its noisy version", good == cases2)
    # NP-hardness: exact cover by 3-sets -> 'is there a compatible ensemble with at most q conformers?'
    rx = np.random.default_rng(329)
    agree = yes = 0
    fam = 40
    for trial in range(fam):
        q = 2
        U = 3 * q
        nT = int(rx.integers(3, 8))
        triples = [tuple(sorted(int(v) for v in rx.choice(U, 3, replace=False))) for _ in range(nT)]
        if trial % 3 == 0:
            perm = [int(v) for v in rx.permutation(U)]
            triples[0] = tuple(sorted(perm[:3]))
            triples[1] = tuple(sorted(perm[3:]))
        cover = any(sorted(x for j in sub for x in triples[j]) == list(range(U))
                    for k in range(nT + 1) for sub in itertools.combinations(range(nT), k))
        Phi = np.array([[1.0 if u in T else 0.0 for u in range(U)] for T in triples])
        y = np.ones(U) / q
        few = any(feasible_on(Phi, y, list(sub)) for k in range(1, q + 1) for sub in itertools.combinations(range(nT), k))
        agree += few == cover
        yes += cover
    print(f"    exact cover by 3-sets: {fam} random families: 'an ensemble with at most q conformers has the data' agrees with"
          f" the existence of an exact cover in {agree}/{fam} ({yes} with a cover)")
    check("the reduction from exact cover", agree == fam and 0 < yes < fam)


if __name__ == "__main__":
    test_M1()
    test_M2()
    test_M3()
    test_M4()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
