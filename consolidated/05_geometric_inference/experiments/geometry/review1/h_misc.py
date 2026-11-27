"""(h) Miscellaneous independent checks.

 1. Lemma R: the set of angular distances reachable in m steps of angle alpha, by direct
    simulation on the sphere, against the claimed intervals J_m (alpha <= pi/2 and alpha > pi/2),
    and the threshold m0 = max(2, ceil(pi/beta)).
 2. Theorem C(a): evaluation functionals at random points of (S^2)^K: rank D_K with D_K points,
    nullity K with D_K - 1 points.
 3. Theorem C(c): explicit chains (consecutive angle alpha) whose every m0-th bond direction is
    prescribed (constructive Lemma R), rank D_K from those bonds alone at n = m0 (D_K - 1) + 2.
 4. The constant in the proof of Theorem G(d):  ||D(Delta)||_F <= 4 ||Delta||^2 ?
 5. Corollary 9.1: Haar average of (g x)(g y)^T.
 6. Theorem F' hypothesis: every 3K+1 consecutive stacked points affinely independent?
 7. Theorem G(d) bracket: full column rank of the K-state parametrisation at a (CC) point.
"""
import itertools
import numpy as np
from mylib import build_chain, sqdist, stack, e0_pairs, conic_system, nullspace, vech_quadratic

rng = np.random.default_rng(1234)


def unit(v):
    return v / np.linalg.norm(v)


# ------------------------------------------------------------------ 1. Lemma R
def reach_sim(alpha, m, N=200000):
    """angular distances from u_0 after m steps of angle alpha (random azimuths)."""
    u = np.tile(np.array([0.0, 0, 1.0]), (N, 1))
    u0 = u.copy()
    for _ in range(m):
        # random unit vector at angle alpha from u
        r = rng.normal(size=(N, 3))
        r -= np.einsum("ij,ij->i", r, u)[:, None] * u
        r /= np.linalg.norm(r, axis=1)[:, None]
        u = np.cos(alpha) * u + np.sin(alpha) * r
    return np.arccos(np.clip(np.einsum("ij,ij->i", u, u0), -1, 1))


def J_claim(alpha, m):
    if m == 1:
        return alpha, alpha
    if alpha <= np.pi / 2:
        return 0.0, min(m * alpha, np.pi)
    beta = np.pi - alpha
    if m % 2 == 0:
        return 0.0, min(m * beta, np.pi)
    return max(0.0, np.pi - m * beta), np.pi


def lemma_R():
    print("1. Lemma R: simulated range of the angular distance after m steps vs claimed J_m")
    worst = 0.0
    bad = []
    for deg in (25.0, 40.0, 60.0, 83.0, 90.0, 97.0, 120.0, 140.0, 165.0):
        alpha = np.deg2rad(deg)
        beta = min(alpha, np.pi - alpha)
        m0 = max(2, int(np.ceil(np.pi / beta - 1e-12)))
        line = []
        for m in range(1, m0 + 2):
            ang = reach_sim(alpha, m, 100000)
            lo, hi = J_claim(alpha, m)
            # simulated values must lie inside J_m and come close to both ends
            inside = ang.min() >= lo - 1e-9 and ang.max() <= hi + 1e-9
            # extreme points are attained exactly by planar zig-zag/straight sequences; a random
            # sample approaches them only slowly, so test attainment by explicit planar sequences
            attained = []
            for signs in itertools.product((1, -1), repeat=m):
                tot = sum(s * alpha for s in signs)
                a = np.arccos(np.cos(tot))                 # angular distance of a planar sequence
                attained.append(a)
            # for m >= 2 the end points of J_m are attained by planar sequences only if they are
            # of the form |sum +-alpha| mod 2pi; 0 and pi may need a non-planar sequence
            if not inside:
                bad.append((deg, m))
            line.append(f"m={m}: sim [{np.rad2deg(ang.min()):6.1f},{np.rad2deg(ang.max()):6.1f}] claim [{np.rad2deg(lo):6.1f},{np.rad2deg(hi):6.1f}]")
            worst = max(worst, lo - ang.min(), ang.max() - hi)
        full_at_m0 = J_claim(alpha, m0) == (0.0, np.pi)
        full_before = J_claim(alpha, m0 - 1) == (0.0, np.pi) if m0 > 2 else False
        print(f"   alpha={deg:5.1f} (m0={m0}; J_m0 = [0,pi]: {full_at_m0}; already at m0-1: {full_before}): " + "; ".join(line))
    print("   violations of 'simulated subset of claimed':", bad)


def lemma_R_recursion():
    """Exact check of the interval recursion against the closed formulas on a fine grid of alpha."""
    bad = 0
    for alpha in np.linspace(0.05, np.pi - 0.05, 400):
        lo, hi = alpha, alpha
        for m in range(1, 40):
            cl, ch = J_claim(alpha, m)
            if abs(lo - cl) > 1e-9 or abs(hi - ch) > 1e-9:
                bad += 1
            # J_{m+1} = union over rho in [lo, hi] of [|rho - alpha|, min(rho + alpha, 2pi - rho - alpha)]
            nlo = 0.0 if lo <= alpha <= hi else min(abs(lo - alpha), abs(hi - alpha))
            cands = [lo, hi] + ([np.pi - alpha] if lo <= np.pi - alpha <= hi else [])
            nhi = max(min(r + alpha, 2 * np.pi - r - alpha) for r in cands)
            lo, hi = nlo, nhi
    print(f"   interval recursion vs closed formulas for 400 values of alpha, m <= 39: mismatches {bad}")
    # threshold: J_m = [0, pi] iff m >= max(2, ceil(pi / beta))
    badthr = 0
    for alpha in np.linspace(0.05, np.pi - 0.05, 400):
        beta = min(alpha, np.pi - alpha)
        m0 = max(2, int(np.ceil(np.pi / beta - 1e-12)))
        for m in range(1, 80):
            full = (J_claim(alpha, m) == (0.0, np.pi))
            if full != (m >= m0):
                badthr += 1
    print(f"   'J_m = [0,pi] iff m >= m0': mismatches {badthr}")


# ------------------------------------------------------------------ 2. Theorem C(a)
def thm_Ca():
    print("2. Theorem C(a): rank of the conic conditions at N random points of (S^2)^K")
    for K in (1, 2, 3, 4):
        m = 3 * K
        dim = m * (m + 1) // 2
        DK = dim - (K - 1)
        for N in (DK - 1, DK, DK + 3):
            P = rng.normal(size=(N, K, 3))
            P /= np.linalg.norm(P, axis=2)[:, :, None]
            A = np.array([vech_quadratic(p.ravel()) for p in P])
            Nn, s, rank = nullspace(A, dim)
            print(f"   K={K} D_K={DK}: N={N:3d} points -> rank {rank}, nullity {dim - rank} (trivial quadrics: {K-1})")


# ------------------------------------------------------------------ 3. Theorem C(c), constructive
def connect(u, v, alpha, m):
    """A sequence u = w_0, ..., w_m = v of unit vectors with consecutive angles alpha
    (exists iff angle(u, v) in J_m).  Greedy: at each step go to a point at angle alpha from the
    current one whose distance to v lies in J_{remaining}."""
    seq = [u]
    cur = u
    for step in range(m, 0, -1):
        if step == 1:
            assert abs(np.arccos(np.clip(cur @ v, -1, 1)) - alpha) < 1e-7, "last step impossible"
            seq.append(v)
            break
        lo, hi = J_claim(alpha, step - 1)
        rho = np.arccos(np.clip(cur @ v, -1, 1))
        # distances to v attainable in one step from cur: [|rho-alpha|, min(rho+alpha, 2pi-rho-alpha)]
        a, b = abs(rho - alpha), min(rho + alpha, 2 * np.pi - rho - alpha)
        lo2, hi2 = max(a, lo), min(b, hi)
        assert lo2 <= hi2 + 1e-12, "unreachable"
        target = 0.5 * (lo2 + hi2) if step - 1 > 1 else alpha
        target = min(max(target, lo2), hi2)
        # point w with angle(cur, w) = alpha and angle(w, v) = target: spherical triangle
        # w = cos(alpha) cur + sin(alpha) (cos(psi) e1 + sin(psi) e2), e1 = component of v orthogonal to cur
        if np.sin(rho) < 1e-9:
            e1 = unit(np.cross(cur, rng.normal(size=3)))
            w = np.cos(alpha) * cur + np.sin(alpha) * e1
        else:
            e1 = unit(v - (v @ cur) * cur)
            e2 = np.cross(cur, e1)
            cpsi = (np.cos(target) - np.cos(alpha) * np.cos(rho)) / (np.sin(alpha) * np.sin(rho))
            cpsi = np.clip(cpsi, -1, 1)
            psi = np.arccos(cpsi) * rng.choice([-1, 1])
            w = np.cos(alpha) * cur + np.sin(alpha) * (np.cos(psi) * e1 + np.sin(psi) * e2)
        seq.append(w)
        cur = w
    return seq


def thm_Cc():
    print("3. Theorem C(c): chains with prescribed every m0-th bond direction; rank from those bonds alone")
    for deg_bond, K in ((97.0, 1), (97.0, 2), (150.0, 1), (40.0, 1), (130.0, 2)):
        alpha = np.pi - np.deg2rad(deg_bond)
        beta = min(alpha, np.pi - alpha)
        m0 = max(2, int(np.ceil(np.pi / beta - 1e-12)))
        m = 3 * K
        dim = m * (m + 1) // 2
        DK = dim - (K - 1)
        nb = m0 * (DK - 1) + 1                      # bonds
        U = []
        for k in range(K):
            pres = rng.normal(size=(DK, 3))
            pres /= np.linalg.norm(pres, axis=1)[:, None]
            seq = [pres[0]]
            for a in range(DK - 1):
                seq += connect(pres[a], pres[a + 1], alpha, m0)[1:]
            U.append(np.array(seq))
        U = np.array(U)                              # K x nb x 3
        assert U.shape[1] == nb
        cons = max(np.abs(np.einsum("kai,kai->ka", U[:, :-1], U[:, 1:]) - np.cos(alpha)).max(),
                   np.abs(np.linalg.norm(U, axis=2) - 1).max())
        X = [np.vstack([np.zeros(3), np.cumsum(Uk, axis=0)]) for Uk in U]
        Z = np.hstack(X)                             # unweighted stack
        rows_pres = np.array([vech_quadratic(Z[a + 1] - Z[a]) for a in range(0, nb, m0)])
        r_pres = nullspace(rows_pres, dim)[2]
        r_all = nullspace(conic_system(Z, e0_pairs(nb + 1)), dim)[2]
        print(f"   bond angle {deg_bond:5.1f}, K={K}: m0={m0}, n = m0(D_K-1)+2 = {nb+1}; constraint violation {cons:.1e}; "
              f"rank from the {DK} prescribed bonds = {r_pres} (D_K = {DK}); rank of the full E0 system = {r_all}")


# ------------------------------------------------------------------ 4. constant in G(d)
def const_Gd():
    print("4. Proof of Theorem G(d): is ||D(Delta)||_F <= 4 ||Delta||_F^2 ?")
    for n in (6, 9, 10, 12, 14, 40):
        Delta = np.zeros((n, 3))
        Delta[0] = [1.0, 0, 0]
        lhs = np.linalg.norm(sqdist(Delta))
        sup = 0.0
        for _ in range(2000):
            D2 = rng.normal(size=(n, 3)) * (rng.random((n, 1)) < 0.2)
            if np.abs(D2).sum() == 0:
                continue
            sup = max(sup, np.linalg.norm(sqdist(D2)) / np.sum(D2 ** 2))
        print(f"   n={n:2d}: Delta = one displaced atom: ||D(Delta)||_F / ||Delta||^2 = {lhs:.4f} (= sqrt(2(n-1)) = {np.sqrt(2*(n-1)):.4f}); "
              f"random sparse Delta sup {sup:.3f}; bound 4 {'VIOLATED' if max(lhs, sup) > 4 else 'ok'}; max-entry norm ratio {np.abs(sqdist(Delta)).max():.1f}")


# ------------------------------------------------------------------ 5. Corollary 9.1
def cor91():
    print("5. Corollary 9.1: average of (g x)(g y)^T over a finite irreducible subgroup (= Haar average for a quadratic)")
    # octahedral rotation group: signed permutation matrices with det +1 (24), full group with det +-1 (48)
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for i, p in enumerate(perm):
                M[i, p] = signs[i]
            mats.append(M)
    x, y = rng.normal(size=3), rng.normal(size=3)
    for name, grp in (("O (24 rotations, subgroup of SO(3))", [M for M in mats if np.linalg.det(M) > 0]), ("O_h (48, subgroup of O(3))", mats)):
        avg = sum(np.outer(g @ x, g @ y) for g in grp) / len(grp)
        print(f"   {name}: max|avg - <x,y>/3 I| = {np.abs(avg - (x @ y) / 3 * np.eye(3)).max():.1e}")
    # Monte Carlo over Haar SO(3) as a cross-check
    Qs = []
    A = rng.normal(size=(200000, 3, 3))
    Q, R = np.linalg.qr(A)
    Q = Q * np.sign(np.einsum("nii->ni", R))[:, None, :]
    det = np.linalg.det(Q)
    Qso = Q * det[:, None, None]                     # flip to det +1
    avg = np.einsum("nij,j,nkl,l->ik", Qso, x, Qso, y) / len(Qso)
    print(f"   Monte Carlo Haar SO(3), 2e5 samples: max|avg - <x,y>/3 I| = {np.abs(avg - (x @ y) / 3 * np.eye(3)).max():.1e}")
    # chirality: second moment cannot see a reflection of one state
    print("   (second moments are invariant under an independent reflection of each state: for SO(3) data the")
    print("    handedness of the states is NOT determined by the second moment)")


# ------------------------------------------------------------------ 6. Theorem F' hypothesis
def Fprime_hyp():
    print("6. Theorem F' hypothesis: smallest singular value over all windows of 3K+1 consecutive stacked points")
    for K, n in ((2, 14), (3, 25), (4, 40)):
        bonds = np.ones(n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(97.0))
        worst = np.inf
        for rep in range(20):
            w = rng.dirichlet(np.ones(K) * 3)
            Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
            Z = stack(Xs, w)
            m = 3 * K
            for i in range(n - m):
                P = Z[i:i + m + 1]
                s = np.linalg.svd(P[1:] - P[0], compute_uv=False)
                worst = min(worst, s[-1] / s[0])
        print(f"   K={K}, n={n}: min over 20 random ensembles and all windows of sigma_min/sigma_max = {worst:.2e} (> 0: hypothesis holds)")
    # degenerate family: helices (constant torsion) violate it for K >= 2 and also violate (CC)
    for K, n in ((2, 14), (3, 25)):
        bonds = np.ones(n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(97.0))
        w = rng.dirichlet(np.ones(K) * 3)
        Xs = [build_chain(np.full(n - 3, rng.uniform(-np.pi, np.pi)), bonds, alphas) for _ in range(K)]
        Z = stack(Xs, w)
        m = 3 * K
        worst = min(np.linalg.svd(Z[i + 1:i + m + 1] - Z[i], compute_uv=False)[-1] for i in range(n - m))
        dim = m * (m + 1) // 2
        nul = dim - nullspace(conic_system(Z, e0_pairs(n)), dim)[2]
        print(f"   K={K}, n={n}, all states helices: min sigma_min over windows = {worst:.1e}; dim N(z) = {nul} (trivial would be {K-1})")


# ------------------------------------------------------------------ 7. G(d) bracket
def Gd_bracket():
    print("7. Theorem G(d) bracket: Jacobian of (torsions, weights) -> M at (CC) points")
    from b_direct import Problem
    for n, seed in ((12, 0), (12, 1), (13, 0), (14, 0)):
        r = np.random.default_rng(seed)
        prob = Problem(n, 2, r)
        p = np.concatenate([np.concatenate(prob.tors), [np.log(prob.w[1] / prob.w[0])]])
        J = prob.jac(p, 2)
        s = np.linalg.svd(J, compute_uv=False)
        print(f"   n={n} seed={seed}: Jacobian {J.shape}, singular values max {s[0]:.3f} min {s[-1]:.4f} -> rank {int((s > 1e-9 * s[0]).sum())} of {J.shape[1]}")


if __name__ == "__main__":
    lemma_R()
    lemma_R_recursion()
    thm_Ca()
    thm_Cc()
    const_Gd()
    cor91()
    Fprime_hyp()
    Gd_bracket()
