#!/usr/bin/env python3
"""ER3 review, Proposition E21 (the permanent certificate) and its Remarks.  Reviewer's own code.

H.  Finite product spaces X = {0..q-1}^r, exhaustive over families of K states (sampled only where noted):
      (a)  f(x) = 0  iff  some set I of states has fewer than |I| coordinates at which x differs from a state of I
           (permanent against a brute-force search over all I);
      (b)  Hall condition on the states  =>  zero set = the states;  if it fails for I, every configuration that
           agrees with the states of I where they coincide is a zero;  how often the zero set is nevertheless the
           set of states (binary AND ternary coordinates);
      (c') the system of distinct representatives used in the proof of (c): for every i there are distinct
           coordinates k_j (j != i) with s^i_{k_j} != s^j_{k_j}  (bipartite matching), in every Hall family; and how
           often it exists when the Hall condition fails.
N.  What is known for finite product spaces (Kahle 2010: the marginal polytope of all margins of order <= t is
    (2^t - 1)-neighbourly): on {0,1}^4 with all correlations of order <= t, EVERY set of at most 2^t - 1 states is
    a simplicial face (LP), with no Hall condition; the even half of a (t+1)-cube (2^t states) is not.
    So on a cube or any finite product space, data of order K identify every ensemble with at most 2^K - 1 atoms,
    and E21 (K atoms under a Hall condition, data of order K) is weaker than a published theorem there.
T.  Torus:
      (i)   K = 3 states on the 3-torus that SHARE angles pairwise but satisfy the Hall condition: zeros of the
            permanent on a 90^3 grid (shifted off the states) plus polishing: only the states;
      (ii)  Hall condition fails (three states that coincide in two of four angles; a pair differing in one angle):
            the permanent vanishes identically on the predicted subtorus;
      (iii) part (c) on a 10^3 grid: Hall triples of grid states are identified by the products over at most three
            angles (LP; a necessary consequence of (c), not a proof); four states on the 3-torus (Hall fails) are
            identified on the grid by the 26 multilinear observables (consistent with Remark 3);
            Remark 3, three states on the 2-torus: the report's count says "three double points impose nine
            conditions on the nine-dimensional span".  Computed here: the 9 x 9 matrix has rank 8 for every triple
            (the squared modulus of the bilinear form through the three points is in the kernel).  The conclusion
            of the remark is nevertheless true, and for every triple: any measure with the same data lives on the
            curve where that bilinear form vanishes, and on the curve the data are the trigonometric moments of
            degree <= 2 of a weighted measure; an explicit twin is computed by an LP on the curve.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog, minimize

rng = np.random.default_rng(31105)
TWO_PI = 2 * np.pi


def hall_violations(St):
    """Sets I (|I| >= 2) of states violating the Hall condition; returns list of (I, mask of coinciding coords)."""
    K = len(St); out = []
    for m in range(2, K + 1):
        for I in itertools.combinations(range(K), m):
            coincide = np.all(St[list(I)] == St[I[0]], axis=0)
            if np.sum(~coincide) < m:
                out.append((I, coincide))
    return out


def perm_zero_set(X, St):
    """Zero set over all configurations X of the permanent of a^i_k = 1[x_k != s^i_k]."""
    K, r = St.shape
    A = (X[:, None, :] != St[None, :, :]).astype(np.int64)   # N x K x r
    vals = np.zeros(len(X), dtype=np.int64)
    for kap in itertools.permutations(range(r), K):
        t = np.ones(len(X), dtype=np.int64)
        for i in range(K):
            t = t * A[:, i, kap[i]]
        vals += t
    return vals == 0, A


def deficient(A):
    """For each configuration: is there a set I of states with |N(I)| < |I| ?"""
    N, K, r = A.shape; out = np.zeros(N, bool)
    for m in range(1, K + 1):
        for I in itertools.combinations(range(K), m):
            nb = (A[:, list(I), :].max(axis=1)).sum(axis=1)   # coordinates where x differs from some state of I
            out |= nb < m
    return out


def sdr_exists(St, i):
    """Distinct coordinates k_j (j != i) with s^i_{k_j} != s^j_{k_j}?  (simple augmenting-path matching)"""
    K, r = St.shape; others = [j for j in range(K) if j != i]
    adj = {j: [k for k in range(r) if St[i, k] != St[j, k]] for j in others}
    match = {}
    def aug(j, seen):
        for k in adj[j]:
            if k in seen:
                continue
            seen.add(k)
            if k not in match or aug(match[k], seen):
                match[k] = j; return True
        return False
    return all(aug(j, set()) for j in others)


def test_H():
    print("H. finite product spaces {0..q-1}^r")
    ok = True
    for q, r, K, sample in ((2, 3, 2, None), (2, 3, 3, None), (2, 4, 2, None), (2, 4, 3, None), (2, 4, 4, None),
                            (2, 5, 3, None), (2, 6, 3, None), (2, 5, 4, None), (3, 3, 2, None), (3, 3, 3, None),
                            (3, 4, 3, None), (3, 4, 4, 30000), (4, 3, 3, None), (2, 6, 4, 30000)):
        X = np.array(list(itertools.product(range(q), repeat=r)))
        N = len(X)
        fams = itertools.combinations(range(N), K) if sample is None else \
            (tuple(sorted(rng.choice(N, size=K, replace=False))) for _ in range(sample))
        n = n_hall = bad_a = bad_b = bad_sub = fail_exact = sdr_bad = sdr_fail_nohall = 0
        for fam in fams:
            St = X[list(fam)]; n += 1
            zero, A = perm_zero_set(X, St)
            bad_a += not np.array_equal(zero, deficient(A))
            viol = hall_violations(St)
            is_states = (zero.sum() == K) and bool(zero[list(fam)].all())
            sdr = all(sdr_exists(St, i) for i in range(K))
            if not viol:
                n_hall += 1
                bad_b += not is_states
                sdr_bad += not sdr
            else:
                for I, coincide in viol:
                    sub = np.all(X[:, coincide] == St[I[0]][coincide], axis=1)
                    bad_sub += not zero[sub].all()
                fail_exact += is_states
                sdr_fail_nohall += not sdr
        ok &= (bad_a + bad_b + bad_sub + sdr_bad) == 0
        print(f"   q = {q}, r = {r}, K = {K}: {n} families{' (sampled)' if sample else ''}; (a) wrong: {bad_a}; Hall holds in "
              f"{n_hall}: zero set != states: {bad_b}, no SDR: {sdr_bad}; Hall fails in {n - n_hall}: predicted "
              f"sub-product not in the zero set: {bad_sub}, zero set = states nevertheless: {fail_exact}, no SDR: {sdr_fail_nohall}")
    return ok


def monomial_features(X, t):
    """All monomials of degree <= t in the +-1 coordinates (constant included)."""
    Y = 1 - 2 * X; n = X.shape[1]; cols = [np.ones(len(X))]
    for k in range(1, t + 1):
        for S in itertools.combinations(range(n), k):
            cols.append(np.prod(Y[:, S], axis=1).astype(float))
    return np.array(cols).T


def is_simplicial_face(G, S):
    S = list(S)
    if np.linalg.matrix_rank(G[S], tol=1e-9) < len(S):
        return False
    mask = np.ones(len(G), bool); mask[S] = False
    res = linprog(np.zeros(G.shape[1]), A_ub=-G[mask], b_ub=-np.ones(mask.sum()), A_eq=G[S], b_eq=np.zeros(len(S)),
                  bounds=[(None, None)] * G.shape[1], method="highs")
    return res.status == 0


def test_N():
    print("N. neighbourliness of the polytope of correlations of order <= t on {0,1}^4 (16 states)")
    X = np.array(list(itertools.product(range(2), repeat=4))); ok = True
    for t in (2, 3):
        G = monomial_features(X, t); m = 2 ** t - 1
        tot = fails = 0; hall_fail = 0
        for S in itertools.combinations(range(16), m):
            tot += 1; fails += not is_simplicial_face(G, S)
        # K = t states: how many violate the Hall condition (and are faces all the same)
        cntK = hallK = 0
        for S in itertools.combinations(range(16), t):
            cntK += 1; hallK += len(hall_violations(X[list(S)])) > 0
        # the even half of a (t+1)-dimensional sub-cube: 2^t states
        sub = [i for i in range(16) if all(X[i, k] == 0 for k in range(t + 1, 4)) and X[i, : t + 1].sum() % 2 == 0]
        nonface = not is_simplicial_face(G, sub)
        ok &= fails == 0 and nonface
        print(f"   order t = {t} ({G.shape[1] - 1} observables): all {tot} sets of {m} = 2^t - 1 states are simplicial faces "
              f"(failures: {fails}); the {len(sub)} even states of a {t + 1}-cube are a face: {not nonface}; "
              f"of the {cntK} families of K = t states, {hallK} violate the Hall condition of E21 and are identified all the same")
    # even-order data modulo the flip (the setting of E19): n = 5 sites, order <= 2 (pairs) and n = 6, order <= 4
    for n, d in ((5, 1), (6, 1)):
        Z = np.array(list(itertools.product(range(2), repeat=n - 1)))
        G = monomial_features(Z, 2 * d); m = 2 ** (2 * d) - 1
        tot = fails = 0
        for S in itertools.combinations(range(len(Z)), m):
            tot += 1; fails += not is_simplicial_face(G, S)
        print(f"   cube modulo flip, n = {n}, even correlations of order <= {2 * d}: all {tot} sets of {m} conformers are faces "
              f"(failures: {fails})  [d = 1 is Proposition E9(a); for general d the bound 2^(2d) - 1 is Kahle's theorem]")
        ok &= fails == 0
    # four-body data modulo the flip (E19 with d = 2): 2^4 - 1 = 15 conformers, sampled
    for n in (6, 7, 8):
        Z = np.array(list(itertools.product(range(2), repeat=n - 1)))
        G = monomial_features(Z, 4)
        fails = 0; trials = 300
        for _ in range(trials):
            fails += not is_simplicial_face(G, rng.choice(len(Z), size=15, replace=False))
        # 16 conformers that are not a face: the even half of a 5-dimensional sub-cube of the z-variables
        sub = [i for i in range(len(Z)) if all(Z[i, k] == 0 for k in range(5, n - 1)) and Z[i, :5].sum() % 2 == 0]
        nonface = not is_simplicial_face(G, sub)
        print(f"   cube modulo flip, n = {n}, even correlations of order <= 4 ({G.shape[1] - 1} observables): {trials} random "
              f"sets of 15 conformers: not a face in {fails}; an explicit set of {len(sub)} conformers (even half of a "
              f"5-cube in z) is a face: {not nonface}")
        ok &= fails == 0 and nonface
    return ok


def perm_torus(phi, S):
    """Permanent of the K x r matrix 2 - 2 cos(phi_k - s^i_k); phi: (M, r)."""
    K, r = S.shape
    A = 2 - 2 * np.cos(phi[:, None, :] - S[None, :, :])
    vals = np.zeros(len(phi))
    for kap in itertools.permutations(range(r), K):
        t = np.ones(len(phi))
        for i in range(K):
            t = t * A[:, i, kap[i]]
        vals += t
    return vals


def test_T():
    print("T. torus")
    ok = True
    # (i) Hall holds with shared angles
    nonstate = 0; cases = 0; min_far = np.inf
    g = 90; ax = TWO_PI * (np.arange(g) + 0.5) / g
    mesh = np.array(list(itertools.product(ax, repeat=3)))
    for _ in range(8):
        S = rng.uniform(0, TWO_PI, size=(3, 3))
        S[1, 0] = S[0, 0]; S[2, 1] = S[1, 1]; S[2, 2] = S[0, 2]      # each pair shares one angle
        assert not hall_violations(np.round(S, 9))
        vals = perm_torus(mesh, S)
        dist = np.min([np.abs(np.angle(np.exp(1j * (mesh - S[i])))).max(axis=1) for i in range(3)], axis=0)
        min_far = min(min_far, vals[dist > 0.15].min())
        for i in np.argsort(vals)[:40]:
            res = minimize(lambda x: perm_torus(x[None, :], S)[0], mesh[i], method="BFGS", options={"gtol": 1e-12})
            if res.fun < 1e-9:
                d = min(np.abs(np.angle(np.exp(1j * (res.x - S[i2])))).max() for i2 in range(3))
                nonstate += d > 1e-3
        cases += 1
    ok &= nonstate == 0 and min_far > 1e-6
    print(f"   (i) three states on the 3-torus, every pair sharing one angle (Hall condition holds): {cases} random "
          f"families; zeros that are not states: {nonstate}; smallest value on the 90^3 grid at distance > 0.15 from "
          f"the states: {min_far:.2e}")
    # (ii) Hall fails
    S = rng.uniform(0, TWO_PI, size=(3, 4)); S[1, 2:] = S[0, 2:]; S[2, 2:] = S[0, 2:]
    probe = np.hstack([rng.uniform(0, TWO_PI, size=(2000, 2)), np.tile(S[0, 2:], (2000, 1))])
    v1 = np.abs(perm_torus(probe, S)).max()
    S2 = rng.uniform(0, TWO_PI, size=(3, 4)); S2[1, 1:] = S2[0, 1:]                 # states 0, 1 differ in one angle only
    probe2 = np.hstack([rng.uniform(0, TWO_PI, size=(2000, 1)), np.tile(S2[0, 1:], (2000, 1))])
    v2 = np.abs(perm_torus(probe2, S2)).max()
    ok &= v1 < 1e-12 and v2 < 1e-12
    print(f"   (ii) Hall fails: three states coinciding in two of four angles: max |f| on 2000 points of the predicted "
          f"2-subtorus = {v1:.1e}; a pair differing in one angle (third state generic): max |f| on the circle = {v2:.1e}")
    # (iii) part (c) by LP on a grid
    g = 10; ax = TWO_PI * np.arange(g) / g
    X = np.array(list(itertools.product(ax, repeat=3)))
    fs = (lambda t: np.ones_like(t), np.cos, np.sin)
    F3 = np.array([fs[a](X[:, 0]) * fs[b](X[:, 1]) * fs[c](X[:, 2]) for a, b, c in itertools.product(range(3), repeat=3)]).T

    def identified(F, idx, w):
        N = F.shape[0]; mu = np.zeros(N); mu[idx] = w
        c = -np.ones(N); c[idx] = 0
        res = linprog(c, A_eq=F.T, b_eq=F.T @ mu, bounds=[(0, None)] * N, method="highs")
        return res.status == 0 and -res.fun < 1e-8 and np.linalg.matrix_rank(F[idx], tol=1e-9) == len(idx)
    hall_ok = hall_n = 0
    while hall_n < 25:
        idx = rng.choice(len(X), size=3, replace=False)
        if hall_violations(np.round(X[idx], 9)):
            continue
        hall_n += 1; hall_ok += identified(F3, idx, rng.dirichlet(np.ones(3)))
    ok &= hall_ok == hall_n
    print(f"   (iii) part (c): {hall_n} Hall triples of grid states on the 10^3 grid: identified by the 26 products over at "
          f"most three angles in {hall_ok}")
    four_n = four_ok = 0
    while four_n < 25:
        idx = rng.choice(len(X), size=4, replace=False)
        P = X[idx]
        if any(np.sum(np.abs(P[i] - P[j]) > 1e-9) < 3 for i in range(4) for j in range(i)):
            continue                                         # keep the four states pairwise different in every angle
        four_n += 1; four_ok += identified(F3, idx, rng.dirichlet(np.ones(4)))
    print(f"         Remark 3: four grid states on the 3-torus, pairwise different in every angle (Hall fails: four states, "
          f"three coordinates): identified by the 26 multilinear observables in {four_ok}/{four_n}")
    # three states on the 2-torus: nine double-point conditions on the nine-dimensional span
    smin = []; s8 = []
    for _ in range(2000):
        P = rng.uniform(0, TWO_PI, size=(3, 2)); rows = []
        for (x, y) in P:
            u = np.array([1, np.cos(x), np.sin(x)]); du = np.array([0, -np.sin(x), np.cos(x)])
            v = np.array([1, np.cos(y), np.sin(y)]); dv = np.array([0, -np.sin(y), np.cos(y)])
            rows += [np.outer(u, v).ravel(), np.outer(du, v).ravel(), np.outer(u, dv).ravel()]
        sv = np.linalg.svd(np.array(rows), compute_uv=False); smin.append(sv[-1] / sv[0]); s8.append(sv[-2] / sv[0])
    print(f"         Remark 3, the count: for 2000 random triples on the 2-torus the 9 x 9 matrix of the double-point "
          f"conditions (value and gradient of the nine products at three points) has smallest relative singular value "
          f"at most {max(smin):.1e} and second smallest at least {min(s8):.1e}: RANK 8, NOT 9 -- the kernel is "
          f"|B|^2, B the bilinear form through the three points")
    ok &= max(smin) < 1e-10
    # the curve Gamma = {B = 0} on the torus and an explicit twin on it
    mass_off = []; resid = []; curve_err = []
    for _ in range(20):
        P = rng.uniform(0, TWO_PI, size=(3, 2)); Zp = np.exp(1j * P)
        V = np.array([[1, z1, z2, z1 * z2] for z1, z2 in Zp])
        uvec = np.linalg.svd(V)[2][-1].conj()                 # V u = 0:  u0 + u1 z1 + u2 z2 + u3 z1 z2 = 0 at the states
        th = TWO_PI * (np.arange(3000) + 0.5) / 3000
        z1 = np.concatenate([np.exp(1j * th), Zp[:, 0]])
        z2 = -(uvec[0] + uvec[1] * z1) / (uvec[2] + uvec[3] * z1)
        curve_err.append(np.abs(np.abs(z2) - 1).max())        # the Moebius map preserves the unit circle
        feats = []
        for f1 in (np.ones_like(z1), z1.real, z1.imag):
            for f2 in (np.ones_like(z2), z2.real, z2.imag):
                feats.append((f1 * f2).real)
        F = np.array(feats)                                   # 9 x (3003): the nine products on the curve
        w = rng.dirichlet(2 * np.ones(3)); mu = np.zeros(F.shape[1]); mu[-3:] = w
        c = -np.ones(F.shape[1]); c[-3:] = 0
        res = linprog(c, A_eq=F, b_eq=F @ mu, bounds=[(0, None)] * F.shape[1], method="highs")
        mass_off.append(-res.fun); resid.append(np.abs(F @ res.x - F @ mu).max())
    print(f"         Remark 3, the truth: a measure with the data of three states lives on the curve B = 0 (a circle on the "
          f"torus: | |z2| - 1 | <= {max(curve_err):.1e} on it); 20 random triples, LP over measures on 3000 points of the "
          f"curve: a twin with mass {min(mass_off):.3f}..{max(mass_off):.3f} off the three states and the same nine data "
          f"(residual {max(resid):.1e}): NOT identified, for every triple (truncated trigonometric moment problem of "
          f"degree 2 on the curve)")
    ok &= min(mass_off) > 0.5 and max(resid) < 1e-9
    # the same triples on a product grid: the grid contains no point of the curve but the states -> 'identified' (artefact)
    g2 = 24; ax2 = TWO_PI * np.arange(g2) / g2
    X2 = np.array(list(itertools.product(ax2, repeat=2)))
    F2 = np.array([fs[a](X2[:, 0]) * fs[b](X2[:, 1]) for a, b in itertools.product(range(3), repeat=2)]).T
    three_n = three_id = 0
    while three_n < 40:
        idx = rng.choice(len(X2), size=3, replace=False); P = X2[idx]
        steps = [int(round(abs(P[i][k] - P[j][k]) / (TWO_PI / g2))) for i in range(3) for j in range(i) for k in range(2)]
        if any(s_ in (0, 1, g2 - 1) for s_ in steps):
            continue
        three_n += 1; three_id += identified(F2, idx, rng.dirichlet(np.ones(3)))
    print(f"         (grid artefact: three states of a 24 x 24 product grid are 'identified' among measures on the grid in "
          f"{three_id}/{three_n} cases, because the grid has no other point on the curve; a product-grid LP cannot test "
          f"non-identification here)")
    return ok


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = True
    if part in ("H", "all"):
        res &= test_H()
    if part in ("N", "all"):
        res &= test_N()
    if part in ("T", "all"):
        res &= test_T()
    print("PASS" if res else "FAIL")
