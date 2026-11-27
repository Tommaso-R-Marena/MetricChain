#!/usr/bin/env python3
"""ER3 review, Theorem E18 and its Remark 1 (three conformers).  Reviewer's own code.

A. Remark 1, exhaustively for n = 3..7: for every triple of sign vectors pairwise different modulo sign
   (a) they are linearly independent;
   (b) at least three of the four coordinate patterns occur;
   (c) the sign vectors in their span are the three and at most one more, and the fourth exists exactly when three
       patterns occur and is then  y = -(m1 x1 + m2 x2 + m3 x3)  with m the missing pattern;
   (d) the matrices x x^T on the zero set Z_S are linearly independent;
   (e) (linear programme) the ensemble on the three conformers, and the ensemble on all of Z_S, are the only
       ensembles on the cube modulo flip with their pair correlations.  n <= 6: all triples; n = 7: all triples
       through a fixed vertex (the symmetry group is transitive on vertices).
   Membership in the span is decided in floating point; this is safe because for integer vectors the squared
   distance to the span is det Gram(x1,x2,x3,y) / det Gram(x1,x2,x3) >= 1/n^3 when it is not zero.
B. Theorem E18 on random finite instances with random lifts (q = 1 and q = 2, real and complex): whenever Z_S is
   finite (automatic) and the matrices v v^* on Z_S are independent, a linear programme confirms that ensembles
   supported in Z_S are identified by the entries of v v^*; and the two edge cases the statement does not mention
   (a state with v = 0; dependent matrices on Z_S).
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(31101)


def cube_mod_flip(n):
    Z = np.array(list(itertools.product((1, -1), repeat=n - 1)))
    return np.hstack([np.ones((len(Z), 1), dtype=int), Z])


def pair_features(Y):
    n = Y.shape[1]; iu = np.triu_indices(n, 1)
    return np.hstack([np.ones((len(Y), 1)), (Y[:, iu[0]] * Y[:, iu[1]]).astype(float)])


def fibre_is_point(F, idx, w):
    """Is sum_a w_a delta_{idx[a]} the only probability vector on the rows of F with the data F^T mu?
    Decided by maximising the mass off the support and, on the support, by the rank."""
    N = F.shape[0]
    mu = np.zeros(N); mu[idx] = w
    c = -np.ones(N); c[idx] = 0
    res = linprog(c, A_eq=F.T, b_eq=F.T @ mu, bounds=[(0, None)] * N, method="highs")
    assert res.status == 0, res.message
    return (-res.fun < 1e-9) and np.linalg.matrix_rank(F[idx], tol=1e-9) == len(idx)


def part_A():
    print("A. Remark 1 to Theorem E18, exhaustive")
    allok = True
    for n in range(3, 8):
        Y = cube_mod_flip(n); N = len(Y); G = pair_features(Y); Yf = Y.astype(float)
        triples = with4 = bad_indep = bad_patterns = bad_count = bad_formula = bad_matrices = 0
        lp_tested = lp_fail3 = lp_fail4 = lp_fail_sub = 0
        min_gap = np.inf
        for tri in itertools.combinations(range(N), 3):
            X = Y[list(tri)]                               # 3 x n
            triples += 1
            if abs(np.linalg.det((X @ X.T).astype(float))) < 0.5:
                bad_indep += 1; continue
            # patterns modulo a global sign: classes of (x1 x2, x1 x3)
            pats = set(zip((X[0] * X[1]).tolist(), (X[0] * X[2]).tolist()))
            if len(pats) < 3:
                bad_patterns += 1
            Q, _ = np.linalg.qr(Yf[list(tri)].T)
            res2 = np.sum((Yf - (Yf @ Q) @ Q.T) ** 2, axis=1)
            inspan = np.nonzero(res2 < 1e-8)[0]
            off = res2[res2 >= 1e-8]
            if len(off):
                min_gap = min(min_gap, off.min())
            extra = [y for y in inspan if y not in tri]
            if len(extra) > 1:
                bad_count += 1
            if (len(extra) == 1) != (len(pats) == 3):
                bad_formula += 1
            if len(extra) == 1:
                with4 += 1
                missing = ({(1, 1), (1, -1), (-1, 1), (-1, -1)} - pats).pop()   # (x1x2, x1x3) of the missing pattern
                m = np.array([1, missing[0], missing[1]])                      # the pattern (+, m2, m3)
                y = -(m @ X)
                if not (np.all(np.abs(y) == 1) and (np.array_equal(y, Y[extra[0]]) or np.array_equal(-y, Y[extra[0]]))):
                    bad_formula += 1
            Zs = np.array(sorted(inspan))
            if np.linalg.matrix_rank(G[Zs], tol=1e-9) < len(Zs):
                bad_matrices += 1
            if n <= 6 or tri[0] == 0:
                lp_tested += 1
                lp_fail3 += not fibre_is_point(G, np.array(tri), rng.dirichlet(np.ones(3)))
                lp_fail_sub += not fibre_is_point(G, np.array(tri[:2]), rng.dirichlet(np.ones(2)))
                if len(Zs) == 4:
                    lp_fail4 += not fibre_is_point(G, Zs, rng.dirichlet(np.ones(4)))
        ok = (bad_indep + bad_patterns + bad_count + bad_formula + bad_matrices + lp_fail3 + lp_fail4 + lp_fail_sub) == 0
        allok &= ok
        print(f"   n = {n}: {triples} triples; dependent: {bad_indep}; fewer than three patterns: {bad_patterns}; "
              f"more than one extra sign vector: {bad_count}; extra vertex present in {with4} "
              f"(wrong prediction of its presence or of y: {bad_formula}); dependent x x^T on Z_S: {bad_matrices}; "
              f"smallest non-zero squared residual {min_gap:.4f} (>= 1/n^3 = {1 / n ** 3:.4f}); "
              f"LP: {lp_tested} triples, ensemble on 3 not identified: {lp_fail3}, on a pair: {lp_fail_sub}, "
              f"on the 4 points of Z_S: {lp_fail4}   [{'ok' if ok else 'FAILED'}]")
    return allok


def lift_instance(Nx, Nv, q, complex_):
    """Random lift on Nx states with small integer entries (so that coincidences occur)."""
    V = rng.integers(-1, 2, size=(Nx, Nv, q)).astype(complex if complex_ else float)
    if complex_:
        V = V + 1j * rng.integers(-1, 2, size=(Nx, Nv, q))
    return V


def features_from_lift(V):
    """Real observables spanning the entries of v v^*: real and imaginary parts of all entries."""
    M = np.einsum("xaq,xbq->xab", V, V.conj())
    F = np.hstack([np.ones((V.shape[0], 1)), M.real.reshape(len(V), -1), M.imag.reshape(len(V), -1)])
    return F, M


def part_B():
    print("B. Theorem E18 on random finite instances")
    tested = applicable = confirmed = dep = dep_notident = zero_v = 0
    ok = True
    for trial in range(3000):
        Nx = int(rng.integers(6, 13)); Nv = int(rng.integers(2, 5)); q = int(rng.integers(1, 3))
        V = lift_instance(Nx, Nv, q, complex_=bool(trial % 2))
        K = int(rng.integers(1, 4)); S = rng.choice(Nx, size=K, replace=False)
        F, M = features_from_lift(V)
        B = np.hstack([V[x] for x in S])                    # N x (K q): sum of the column spaces
        U, s, _ = np.linalg.svd(B, full_matrices=True)
        r = int((s > 1e-9).sum())
        Pperp = np.eye(Nv) - U[:, :r] @ U[:, :r].conj().T
        fS = np.array([np.linalg.norm(Pperp @ V[x]) ** 2 for x in range(Nx)])
        fS_from_features = np.array([np.real(np.trace(Pperp @ M[x])) for x in range(Nx)])
        ok &= np.allclose(fS, fS_from_features, atol=1e-9)   # f_S is a real combination of entries of v v^*
        Z = np.nonzero(fS < 1e-9)[0]
        tested += 1
        mats = np.hstack([M[Z].real.reshape(len(Z), -1), M[Z].imag.reshape(len(Z), -1)])
        indep = np.linalg.matrix_rank(mats, tol=1e-9) == len(Z)
        if any(np.abs(V[x]).max() == 0 for x in S):
            zero_v += 1
        if indep:
            applicable += 1
            w = np.zeros(len(Z)); w[: len(Z)] = rng.dirichlet(np.ones(len(Z)))
            good = fibre_is_point(F, Z, w)
            confirmed += good; ok &= good
            # sub-support S itself
            ok &= fibre_is_point(F, S, rng.dirichlet(np.ones(K)))
        else:
            dep += 1
            # is an ensemble with full support on Z_S identified?  (the theorem says nothing)
            dep_notident += not fibre_is_point(F, Z, np.ones(len(Z)) / len(Z))
    print(f"   {tested} instances; hypothesis of E18 holds in {applicable}, identification confirmed by LP in {confirmed}; "
          f"dependent matrices on Z_S in {dep} (full-support ensemble on Z_S then not identified in {dep_notident}); "
          f"instances with a state of S having v = 0: {zero_v}   [{'ok' if ok else 'FAILED'}]")
    # the edge case of case (i): states with v = 0
    V = np.zeros((3, 2, 1)); V[1, 0, 0] = 1; V[2, 1, 0] = 1  # v(x0) = 0, v(x1) = e1, v(x2) = e2
    F, M = features_from_lift(V)
    S = np.array([0, 1])
    print("   edge case 1: X = {x0,x1,x2}, v = 0, e1, e2, S = {x0,x1}: Z_S = S, the column spaces {0}, span(e1) are "
          "independent as subspaces, yet v(x0)v(x0)^* = 0 (the matrices are dependent); ensemble on S identified:",
          fibre_is_point(F, S, np.array([0.5, 0.5])), "(by the constant observable, not by the lift)")
    V = np.zeros((3, 1, 1)); V[2, 0, 0] = 1                  # v(x0) = v(x0') = 0, v(x1) = 1
    F, M = features_from_lift(V)
    S = np.array([0, 1])
    fS = np.array([np.linalg.norm(V[x]) ** 2 for x in range(3)])   # U = {0}, P = 0
    print("   edge case 2: X = {x0,x0',x1}, v = 0, 0, 1, S = {x0,x0'}: f_S = |v|^2 has zero set", np.nonzero(fS < 1e-12)[0].tolist(),
          "= S, the column spaces {0}, {0} have direct sum; ensemble on S identified:",
          fibre_is_point(F, S, np.array([0.5, 0.5])), " -> case (i) of E18 needs v(x) != 0 on S")
    return ok


if __name__ == "__main__":
    a = part_A(); b = part_B()
    print("PASS" if (a and b) else "FAIL")
    sys.exit(0 if (a and b) else 1)
