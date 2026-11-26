#!/usr/bin/env python3
"""ER3 review, Theorem E20 and its torus corollary.  Reviewer's own code (no multi-start minimisation: the zeros of
the projector certificate are computed algebraically).

The projector certificate of K points of the r-torus vanishes at z iff  W^* v(z) = 0,  v(z) = tensor_k (1, z_k),
W an orthonormal basis of the orthogonal complement of span{v(points)}: 2^r - K multilinear equations.

T3.  r = 3.  Write v(z) = (w, z3 w), w = (1, z1, z2, z1 z2):  M(z3) w = 0 with M = A + z3 B of size (8-K) x 4, and
     w on the quadric w0 w3 = w1 w2.
       K = 4: det M(z3) (degree 4) -> at most 4 solutions: exactly the 4 points.
       K = 5: kernel vector by cofactors (cubics in z3), quadric condition of degree 6 -> 6 complex solutions.
              How many lie on the torus?  Is the sixth distinct from the five?  Are the six rank-one matrices
              v v^* independent (smallest singular value; by the reviewer's argument they always are)?
       K = 6: a curve; fraction of z3 on the unit circle over which the certificate has zeros on the torus.
     Also: special configurations, and an adversarial search for a 5-point configuration with nearly dependent
     rank-one matrices.
T4.  r = 4.  K = 11: all 24 solutions of four random combinations of the five equations, filtered by the fifth.
             K = 12: the 24 solutions of the four equations (batched Newton from random complex starts; complete-
             ness checked by the count 24 = 4! and by the Euler-Jacobi identity sum g(x)/J(x) = 0); how many are on
             the torus; are the rank-one matrices on the torus zeros independent?
             K = 10, 13 for comparison (13: a curve).
"""
import itertools, sys
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(31103)


def lift(z):
    """z: (M, r) complex -> (M, 2^r), index = sum a_k 2^k  (z_1 least significant)."""
    z = np.atleast_2d(z)
    V = np.ones((z.shape[0], 1), dtype=complex)
    for k in range(z.shape[1]):
        V = np.hstack([V, V * z[:, [k]]])
    return V


def complement(points):
    """Rows c_j with c_j . v(z) = 0 on the span: conj of an orthonormal basis of the complement of span v(points)."""
    V = lift(np.exp(1j * points)).T                          # 2^r x K
    U, s, _ = np.linalg.svd(V, full_matrices=True)
    K = points.shape[0]
    assert s[-1] > 1e-9 * s[0], "lifted points dependent"
    return U[:, K:].conj().T                                 # (2^r - K) x 2^r


def on_torus(z, tol=1e-7):
    return bool(np.all(np.abs(np.abs(z) - 1) < tol))


def cof_kernel(M):
    """Kernel vector of a 3 x 4 matrix by cofactors (polynomial in the entries)."""
    return np.array([(-1) ** b * np.linalg.det(np.delete(M, b, axis=1)) for b in range(4)])


def solve_r3_K5(C):
    A, B = C[:, :4], C[:, 4:]
    def g(t):
        w = cof_kernel(A + t * B)
        return w[0] * w[3] - w[1] * w[2]
    # degree-6 polynomial in t: interpolate on 7 roots of unity
    ts = np.exp(2j * np.pi * np.arange(7) / 7)
    vals = np.array([g(t) for t in ts])
    coef = np.fft.fft(vals) / 7                              # coef[k] of t^k
    roots = np.roots(coef[::-1])
    sols = []
    for t in roots:
        for _ in range(3):                                   # polish the root with Newton on g
            h = 1e-6
            dg = (g(t + h) - g(t - h)) / (2 * h)
            t = t - g(t) / dg
        w = cof_kernel(A + t * B)
        sols.append(np.array([w[1] / w[0], w[2] / w[0], t]))
    return np.array(sols)


def rank_one_sigma(Z):
    """Smallest singular value of the (normalised) real matrix whose rows are the Hermitian matrices v v^*."""
    V = lift(Z)
    mats = np.array([np.outer(v, v.conj()).ravel() for v in V])
    M = np.hstack([mats.real, mats.imag])
    M = M / np.linalg.norm(M, axis=1, keepdims=True)
    return np.linalg.svd(M, compute_uv=False)[-1]


def test_T3():
    print("T3. three angles (Segre threefold in P^7, codimension 4, degree 6)")
    ok = True
    # K = 4
    bad = 0; trials = 2000
    for _ in range(trials):
        P = rng.uniform(0, 2 * np.pi, size=(4, 3)); C = complement(P)
        A, B = C[:, :4], C[:, 4:]
        ts = np.exp(2j * np.pi * np.arange(5) / 5)
        coef = np.fft.fft(np.array([np.linalg.det(A + t * B) for t in ts])) / 5
        roots = np.roots(coef[::-1])
        z3 = np.exp(1j * P[:, 2])
        d = np.abs(roots[:, None] - z3[None, :]).min(axis=1).max()
        bad += d > 1e-6
    print(f"   K = 4: {trials} random 4-tuples; det M(z3) has degree 4 and its roots are the four given z3 in all but "
          f"{bad} cases -> the zero set is the 4 points (no search needed)")
    ok &= bad == 0
    # K = 5
    trials = 5000; n_torus = {}; worst_res = 0; min_sig = np.inf; min_sep = np.inf; sixth_off = 0; worst_mod = 0
    sig_all = []
    for _ in range(trials):
        P = rng.uniform(0, 2 * np.pi, size=(5, 3)); C = complement(P)
        sols = solve_r3_K5(C)
        worst_res = max(worst_res, np.abs(C @ lift(sols).T).max())
        tor = [s for s in sols if on_torus(s, 1e-6)]
        n_torus[len(tor)] = n_torus.get(len(tor), 0) + 1
        given = np.exp(1j * P)
        d = np.abs(sols[:, None, :] - given[None, :, :]).max(axis=2)       # 6 x 5
        match = d.min(axis=1) < 1e-6
        extra = sols[~match]
        if len(extra) != 1:
            sixth_off += 1; continue
        worst_mod = max(worst_mod, np.abs(np.abs(extra[0]) - 1).max())
        min_sep = min(min_sep, np.abs(extra[0][None, :] - given).max(axis=1).min())
        s6 = rank_one_sigma(np.vstack([given, extra]))
        sig_all.append(s6); min_sig = min(min_sig, s6)
    print(f"   K = 5: {trials} random 5-tuples; complex solutions per instance: 6; number on the torus: {n_torus}; "
          f"instances without exactly one extra solution: {sixth_off}; largest | |z_k| - 1 | of the sixth point: "
          f"{worst_mod:.1e}; largest residual {worst_res:.1e}")
    print(f"          smallest singular value of the six normalised rank-one matrices: min {min_sig:.2e}, "
          f"median {np.median(sig_all):.2e}; smallest distance of the sixth point from the five: {min_sep:.2e}")
    ok &= set(n_torus) == {6} and sixth_off == 0
    # adversarial: minimise the smallest singular value over 5-point configurations kept apart
    def sig_of(x):
        P = x.reshape(5, 3)
        try:
            C = complement(P); sols = solve_r3_K5(C)
        except AssertionError:
            return 1.0
        given = np.exp(1j * P)
        d = np.abs(sols[:, None, :] - given[None, :, :]).max(axis=2)
        extra = sols[d.min(axis=1) > 1e-7]
        if len(extra) != 1:
            return 1.0
        # penalty keeps the five points pairwise apart and the lifted vectors well conditioned
        sep = min(np.abs(given[i] - given[j]).min() for i in range(5) for j in range(i))
        pen = max(0.0, 0.5 - sep) * 10
        return rank_one_sigma(np.vstack([given, extra])) + pen
    best = (np.inf, None)
    for _ in range(12):
        res = minimize(sig_of, rng.uniform(0, 2 * np.pi, size=15), method="Nelder-Mead",
                       options={"maxiter": 2500, "xatol": 1e-7, "fatol": 1e-12})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    P = best[1].reshape(5, 3); C = complement(P); sols = solve_r3_K5(C); given = np.exp(1j * P)
    d = np.abs(sols[:, None, :] - given[None, :, :]).max(axis=2); extra = sols[d.min(axis=1) > 1e-7]
    V5 = lift(given); s5 = np.linalg.svd(V5 / np.linalg.norm(V5, axis=1, keepdims=True), compute_uv=False)[-1]
    dist6 = np.abs(extra[0][None, :] - given).max(axis=1).min() if len(extra) == 1 else float("nan")
    print(f"   adversarial search (12 Nelder-Mead runs, five points kept >= 0.5 apart in every angle): smallest "
          f"singular value reached {best[0]:.2e}; at that configuration: smallest singular value of the five lifted "
          f"vectors {s5:.2e}, distance of the sixth point from the nearest given point {dist6:.2e}")
    # special configurations
    print("   special configurations (K = 5):")
    base = rng.uniform(0, 2 * np.pi, size=(5, 3))
    specials = {}
    Q = base.copy(); Q[1, 0] = Q[0, 0]; specials["two points share one angle"] = Q
    Q = base.copy(); Q[1, :2] = Q[0, :2]; specials["two points share two angles (differ in one)"] = Q
    Q = base.copy(); Q[1] = Q[0] + 1e-3; specials["two points 1e-3 apart"] = Q
    Q = base.copy(); Q[:, 2] = Q[:, 0] + Q[:, 1]; specials["all on the subgroup phi3 = phi1 + phi2"] = Q
    Q = base.copy(); Q[:, 0] = Q[0, 0]; specials["all five share the first angle"] = Q
    for name, Q in specials.items():
        try:
            C = complement(Q)
        except AssertionError:
            print(f"      {name}: the five lifted vectors are linearly dependent (E18 does not apply)"); continue
        # count torus zeros through z3: for each root; also detect a positive-dimensional zero set
        A, B = C[:, :4], C[:, 4:]
        ts = np.exp(2j * np.pi * np.arange(7) / 7)
        def g(t):
            w = cof_kernel(A + t * B); return w[0] * w[3] - w[1] * w[2]
        coef = np.fft.fft(np.array([g(t) for t in ts])) / 7
        scale = np.abs(coef).max()
        if scale < 1e-9:
            print(f"      {name}: the degree-6 resultant vanishes identically -> the certificate vanishes on a curve "
                  f"(Z_S infinite; E18 does not apply)"); continue
        sols = solve_r3_K5(C)
        tor = np.array([s for s in sols if on_torus(s, 1e-5)])
        uniq = []
        for s in tor:
            if not any(np.abs(s - u).max() < 1e-4 for u in uniq):
                uniq.append(s)
        sig = rank_one_sigma(np.array(uniq)) if len(uniq) else float("nan")
        print(f"      {name}: {len(uniq)} distinct zeros on the torus; smallest singular value of their rank-one "
              f"matrices {sig:.2e}")
    # K = 6: a curve
    P = rng.uniform(0, 2 * np.pi, size=(6, 3)); C = complement(P); A, B = C[:, :4], C[:, 4:]
    hits = 0; grid = 3600
    for t in np.exp(2j * np.pi * (np.arange(grid) + 0.5) / grid):
        M = A + t * B                                        # 2 x 4, kernel of dimension 2
        _, _, Vh = np.linalg.svd(M); N2 = Vh[2:].conj().T    # 4 x 2
        # points a N2[:,0] + b N2[:,1] on the quadric w0 w3 - w1 w2 = 0: a binary quadratic form
        q = lambda w: w[0] * w[3] - w[1] * w[2]
        n0, n1 = N2[:, 0], N2[:, 1]
        qa, qc = q(n0), q(n1); qb = q(n0 + n1) - qa - qc
        for s_ in np.roots([qa, qb, qc]):
            w = s_ * n0 + n1
            z = np.array([w[1] / w[0], w[2] / w[0]])
            hits += on_torus(z, 1e-6)
    print(f"   K = 6: for z3 on a grid of {grid} points of the unit circle the certificate has {hits} zeros on the "
          f"torus (two per z3 on arcs of total length {hits / (2 * grid):.2f} of the circle): a curve of zeros")
    ok &= hits > 6
    return ok


def newton_all_solutions(C, r, starts=6000, iters=80, seed=0):
    """All isolated solutions of C v(z) = 0 (r equations, r unknowns) by batched Newton from random complex starts."""
    g = np.random.default_rng(seed)
    z = np.exp(g.uniform(-1.5, 1.5, size=(starts, r))) * np.exp(1j * g.uniform(0, 2 * np.pi, size=(starts, r)))
    def dlift(z, k):
        zz = z.copy()
        V = np.ones((z.shape[0], 1), dtype=complex)
        for j in range(r):
            V = np.hstack([V, V * zz[:, [j]]]) if j != k else np.hstack([np.zeros_like(V), V])
        return V
    for _ in range(iters):
        F = lift(z) @ C.T                                    # starts x r
        J = np.stack([dlift(z, k) @ C.T for k in range(r)], axis=2)   # starts x r(eq) x r(var)
        try:
            dz = np.linalg.solve(J, F[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            dz = np.zeros_like(F)
        step = np.linalg.norm(dz, axis=1, keepdims=True)
        dz = dz * np.minimum(1.0, 2.0 / np.maximum(step, 1e-300))     # damp wild steps
        z = z - dz
    F = np.abs(lift(z) @ C.T).max(axis=1)
    good = z[(F < 1e-10) & np.isfinite(F)]
    sols = []
    for s in good:
        if not any(np.abs(s - u).max() < 1e-6 * (1 + np.abs(u).max()) for u in sols):
            sols.append(s)
    return np.array(sols)


def jac_det(C, z):
    r = len(z); cols = []
    for k in range(r):
        V = np.ones(1, dtype=complex)
        for j in range(r):
            V = np.concatenate([V, V * z[j]]) if j != k else np.concatenate([np.zeros_like(V), V])
        cols.append(C @ V)
    return np.linalg.det(np.array(cols).T)


def test_T4(instances=40):
    print("T4. four angles (Segre fourfold in P^15, codimension 11, degree 24)")
    ok = True
    # K = 11 and K = 10
    for K in (10, 11):
        extra_total = 0; incomplete = 0; n = 12
        for it in range(n):
            P = rng.uniform(0, 2 * np.pi, size=(K, 4)); C = complement(P)
            Rm = rng.normal(size=(4, C.shape[0])) + 1j * rng.normal(size=(4, C.shape[0]))
            sols = newton_all_solutions(Rm @ C, 4, seed=it)
            incomplete += len(sols) != 24
            common = [s for s in sols if np.abs(C @ lift(s)[0]).max() < 1e-8]
            given = np.exp(1j * P)
            extra_total += sum(np.abs(s[None, :] - given).max(axis=1).min() > 1e-6 for s in common)
            ok &= len(common) == K
        print(f"   K = {K}: {n} random instances; four random combinations of the {16 - K} equations have 24 solutions "
              f"(incomplete solves: {incomplete}); common zeros of all equations that are not given points: {extra_total}")
        ok &= extra_total == 0
    # K = 12
    counts = {}; dep_when_all = []; sig_proper = []; ej = 0; incomplete = 0; cone24 = []
    for it in range(instances):
        P = rng.uniform(0, 2 * np.pi, size=(12, 4)); C = complement(P)
        sols = newton_all_solutions(C, 4, seed=1000 + it)
        if len(sols) != 24:
            incomplete += 1; continue
        # Euler-Jacobi completeness check: sum_i x^m / J(x_i) = 0 for exponents m in {0,1,2}^4
        Jd = np.array([jac_det(C, s) for s in sols])
        worst = 0
        for m in itertools.product(range(3), repeat=4):
            terms = np.prod(sols ** np.array(m), axis=1) / Jd
            worst = max(worst, abs(terms.sum()) / np.abs(terms).sum())
        ej = max(ej, worst)
        tor = np.array([s for s in sols if on_torus(s, 1e-6)])
        counts[len(tor)] = counts.get(len(tor), 0) + 1
        sig = rank_one_sigma(tor)
        (dep_when_all if len(tor) == 24 else sig_proper).append(sig)
        if len(tor) == 24:
            # all 24 zeros real: one relation sum h_i v_i v_i^* = 0 (Euler-Jacobi).  A twin of an ensemble with full
            # support on the 12 states exists iff some relation is non-negative on the 12 extra zeros.
            given = np.exp(1j * P)
            isS = np.array([np.abs(s_[None, :] - given).max(axis=1).min() < 1e-6 for s_ in tor])
            V = lift(tor); mats = np.array([np.outer(v, v.conj()).ravel() for v in V])
            Mr = np.hstack([mats.real, mats.imag])
            sv, Vt = np.linalg.svd(Mr.T, full_matrices=False)[1:]
            nullity = int((sv < 1e-9 * sv[0]).sum()); hx = Vt[-1][~isS]
            cone24.append((nullity, int((hx > 0).sum()), int((hx < 0).sum())))
    print(f"   K = 12: {instances} random instances ({incomplete} incomplete solves discarded); 24 complex solutions each; "
          f"Euler-Jacobi residual (relative) at most {ej:.1e}")
    print(f"           number of solutions on the torus -> instances: {dict(sorted(counts.items()))}")
    if sig_proper:
        print(f"           fewer than 24 on the torus: smallest singular value of the rank-one matrices on the torus "
              f"zeros: min {min(sig_proper):.2e}, median {np.median(sig_proper):.2e}  (independent: E18(ii) applies)")
    if dep_when_all:
        print(f"           all 24 on the torus: smallest singular value max {max(dep_when_all):.2e} "
              f"(dependent, as the Euler-Jacobi identity predicts: E18(ii) does NOT apply)")
        for nullity, pos, neg in cone24:
            print(f"              relations: {nullity}; coefficients on the 12 extra zeros: {pos} positive, {neg} negative "
                  f"-> a relation that is non-negative off the states (a twin) exists: {nullity == 1 and (pos == 0 or neg == 0)}")
    # K = 13: curve; count torus zeros of the certificate along a one-parameter slice z4 = e^{i t}
    P = rng.uniform(0, 2 * np.pi, size=(13, 4)); C = complement(P); hits = 0; grid = 240
    for t in np.exp(2j * np.pi * (np.arange(grid) + 0.5) / grid):
        # substitute z4 = t: three equations in (z1, z2, z3): rows C[:, :8] + t C[:, 8:]
        C3 = C[:, :8] + t * C[:, 8:]
        sols = solve_r3_K5(C3)
        hits += sum(on_torus(s, 1e-6) for s in sols)
    print(f"   K = 13: on {grid} slices z4 = const of the torus the certificate has {hits} zeros in total: a curve of zeros")
    ok &= hits > 13
    return ok


if __name__ == "__main__":
    # usage: er3_e20_torus.py T3   |   er3_e20_torus.py T4 [instances]     (each part runs in under ten minutes)
    part = sys.argv[1] if len(sys.argv) > 1 else "T3"
    res = test_T3() if part == "T3" else test_T4(int(sys.argv[2]) if len(sys.argv) > 2 else 40)
    print("PASS" if res else "FAIL")
