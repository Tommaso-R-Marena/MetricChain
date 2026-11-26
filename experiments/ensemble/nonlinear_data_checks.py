#!/usr/bin/env python3
"""Numerical checks for Part VII of docs/ensemble/ENSEMBLE_REPORT.md (data that are not linear in the ensemble).

Q1  Ratio data (Proposition E23): a ratio of two means with a positive denominator, known within a tolerance, is a
    pair of linear constraints; the range of a target under ratio data, by linear programming, against a brute-force
    search over all vertices of the feasible polytope.
Q2  The norm of a mean vector (Theorem E25): for point clouds Phi(X) whose hull misses the origin, the ensemble of
    least norm: certificate z*.Phi(x) - r^2 >= 0 with zero set Z; uniqueness when the features are affinely
    independent on Z; stability — the mass that an ensemble with norm <= r + tau can put off Z is at most
    r tau / gamma (linear), its mean is within sqrt(2 r tau + tau^2) of z* (square root, attained along the face).
    At the other end: the farthest point; mass off it at most tau / gamma'.  In between: explicit twins.
Q3  Squared means (Theorem E26): the instance built from positive integers a_1..a_m (2m configurations, m squared
    means and one mean) is consistent iff the integers can be split into two parts of equal sum; decided here by
    2^m linear feasibility problems and compared with a subset-sum table.
Q4  A reverse-convex constraint as a union over directions (Proposition E24): the range of a target under a lower
    bound on the norm of a mean vector in the plane, by linear programmes over a net of directions with the
    certified enlargement, against a fine direct search.
Q5  Data known up to one unknown positive factor (Proposition E23(b)): the criterion — linear independence on the
    support and a non-negative combination of the observables without a constant term whose zero set is the
    support — against a direct test by linear programming, on random instances with integer observables.

Usage: python3 experiments/ensemble/nonlinear_data_checks.py      (about a minute; exit code 0 iff all hold)
Numerical evidence only [N]; seeds fixed.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog, nnls

rng = np.random.default_rng(20261127)


def lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, n=None):
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method="highs")


# ---------------------------------------------------------------------------------------------------------- Q1
def test_Q1():
    worst = 0.0; cases = 0; ok = True
    for _ in range(60):
        M = int(rng.integers(4, 7))
        phi = rng.normal(size=M); psi = rng.uniform(0.5, 2.0, size=M); tgt = rng.normal(size=M)
        mu0 = rng.dirichlet(np.ones(M)); y = (mu0 @ phi) / (mu0 @ psi); tau = rng.choice((0.0, 0.05, 0.2))
        # |E phi / E psi - y| <= tau   <=>   E(phi - (y + tau) psi) <= 0 <= E(phi - (y - tau) psi)
        A = np.vstack([phi - (y + tau) * psi, -(phi - (y - tau) * psi)])
        hi = -lp(-tgt, A_ub=A, b_ub=np.zeros(2), A_eq=np.ones((1, M)), b_eq=[1.0], n=M).fun
        lo = lp(tgt, A_ub=A, b_ub=np.zeros(2), A_eq=np.ones((1, M)), b_eq=[1.0], n=M).fun
        # brute force: sample many ensembles, keep those that satisfy the RATIO constraint, compare ranges
        W = rng.dirichlet(np.ones(M) * 0.3, size=40000)
        r = (W @ phi) / (W @ psi); keep = np.abs(r - y) <= tau + 1e-12
        if tau > 0 and keep.sum() > 50:
            vals = W[keep] @ tgt
            ok &= vals.max() <= hi + 1e-9 and vals.min() >= lo - 1e-9
            worst = max(worst, max(vals.max() - hi, lo - vals.min())); cases += 1
        # vertices of the linear description: every vertex satisfies the ratio constraint
        for sgn in (1, -1):
            res = lp(sgn * tgt, A_ub=A, b_ub=np.zeros(2), A_eq=np.ones((1, M)), b_eq=[1.0], n=M)
            w = res.x; ok &= abs((w @ phi) / (w @ psi) - y) <= tau + 1e-9
    return ok, [f"    ratio data: 60 instances; the optimal ensembles of the linear programme satisfy the ratio constraint; "
                f"{cases} instances with tolerance compared with 40 000 sampled ensembles each: no sampled feasible "
                f"ensemble outside the LP range (largest excess {worst:+.1e})"]


# ---------------------------------------------------------------------------------------------------------- Q2
def nearest_point(P):
    """Nearest point of conv(P) to the origin and its weights: the non-negative least-squares problem
    min |[P^T; 1^T] w - (0, 1)|, w >= 0, has a solution proportional to the weights of the nearest point
    (Lawson-Hanson; an active-set method, exact up to round-off)."""
    M, dim = P.shape
    A = np.vstack([P.T, np.ones((1, M))]); b = np.zeros(dim + 1); b[-1] = 1.0
    w, _ = nnls(A, b)
    w = w / w.sum()
    return w @ P, w


def test_Q2():
    out = []; ok = True
    worst_mass = 0.0; worst_mean = 0.0; sharp = 0.0; unique = 0; cases = 0; worst_far = 0.0
    for _ in range(40):
        dim = int(rng.choice((2, 3))); M = int(rng.integers(6, 10))
        P = rng.normal(size=(M, dim)); P[:, 0] = np.abs(P[:, 0]) + rng.uniform(0.3, 1.0)       # hull misses the origin
        zs, w = nearest_point(P); r = np.linalg.norm(zs)
        f = P @ zs - r * r                                           # certificate: >= 0 on X
        ok &= f.min() > -1e-9
        Z = np.nonzero(f < 1e-8)[0]; off = np.nonzero(f >= 1e-8)[0]
        if len(off) == 0:
            continue
        gamma = f[off].min()
        indep = np.linalg.matrix_rank(np.hstack([np.ones((len(Z), 1)), P[Z]]), tol=1e-8) == len(Z)
        unique += indep; cases += 1
        for tau in (1e-3, 1e-2):
            # largest mass off Z over ensembles with |E Phi| <= r + tau: outer approximation of the ball by 720 (dim 2)
            # or 2000 random (dim 3) half-spaces — a relaxation, so its value is an upper bound of the true maximum
            if dim == 2:
                ang = 2 * np.pi * np.arange(360) / 360; U = np.stack([np.cos(ang), np.sin(ang)], axis=1)
            else:
                U = rng.normal(size=(800, 3)); U /= np.linalg.norm(U, axis=1, keepdims=True)
            U = np.vstack([U, zs / r])                               # the direction of z* itself: the one the bound uses
            c = np.zeros(M); c[off] = -1.0
            res = lp(c, A_ub=U @ P.T, b_ub=(r + tau) * np.ones(len(U)), A_eq=np.ones((1, M)), b_eq=[1.0], n=M)
            mass = -res.fun
            worst_mass = max(worst_mass, mass / (r * tau / gamma))
            # the mean of a feasible ensemble: distance from z*, against sqrt(2 r tau + tau^2); maximise along 12 directions
            best = 0.0
            for v in U[:: max(1, len(U) // 12)]:
                res2 = lp(-(P @ v), A_ub=U @ P.T, b_ub=(r + tau) * np.ones(len(U)), A_eq=np.ones((1, M)), b_eq=[1.0], n=M)
                z = res2.x @ P
                if np.linalg.norm(z) <= r + tau + 1e-6:              # truly feasible (the relaxation is outer)
                    best = max(best, np.linalg.norm(z - zs))
            worst_mean = max(worst_mean, best / np.sqrt(2 * r * tau + tau * tau))
            if len(Z) >= 2:
                sharp = max(sharp, best / np.sqrt(2 * r * tau + tau * tau))
        # the farthest point
        norms = np.linalg.norm(P, axis=1); k = int(np.argmax(norms)); gp = norms[k] - np.sort(norms)[-2]
        tau = 0.5 * gp
        ang = 2 * np.pi * np.arange(90) / 90
        best = 0.0
        dirs = np.stack([np.cos(ang), np.sin(ang)], axis=1) if dim == 2 else np.vstack([rng.normal(size=(90, 3))])
        dirs = np.vstack([dirs, P[k] / norms[k]])
        dirs = dirs / np.linalg.norm(dirs, axis=1, keepdims=True)
        for u in dirs:                                               # |E Phi| >= R - tau  <=  union over directions
            c = np.zeros(M); c[k] = 1.0                              # minimise the population of the farthest point
            res = lp(c, A_ub=-(P @ u)[None, :], b_ub=[-(norms[k] - tau)], A_eq=np.ones((1, M)), b_eq=[1.0], n=M)
            if res.status == 0:
                best = max(best, 1 - res.fun)
        worst_far = max(worst_far, best / (tau / gp))
    flags = (worst_mass <= 1 + 1e-5, worst_mean <= 1 + 1e-3, worst_far <= 1 + 1e-6, sharp > 0.9)
    if not all(flags):
        out.append(f"    DIAGNOSTIC: {flags}; worst_mass = {worst_mass!r}, worst_mean = {worst_mean!r}, worst_far = {worst_far!r}")
    ok &= all(flags)
    out.append(f"    least norm: {cases} clouds in dimension 2 and 3; certificate z*.Phi - r^2 >= 0 on every cloud; features "
               f"affinely independent on its zero set in {unique} (then the ensemble of least norm is unique)")
    out.append(f"    stability at the least norm (tau = 1e-3, 1e-2): largest (mass off the zero set)/(r tau/gamma) = "
               f"{worst_mass:.3f}; largest |mean - z*|/sqrt(2 r tau + tau^2) = {worst_mean:.3f} "
               f"(with a face of positive dimension: {sharp:.3f} — the square root is attained)")
    out.append(f"    largest norm: largest (mass off the farthest configuration)/(tau/gamma') over the clouds = {worst_far:.3f}")
    # in between: twins.  Unit square corners, target norm 1: (1,0)-type means from different ensembles
    P = np.array([[1.0, 1.0], [1.0, -1.0], [-1.0, 1.0], [-1.0, -1.0]])
    w1 = np.array([0.5, 0.5, 0.0, 0.0]); w2 = np.array([0.5, 0.0, 0.5, 0.0])
    tw = abs(np.linalg.norm(w1 @ P) - 1.0) < 1e-15 and abs(np.linalg.norm(w2 @ P) - 1.0) < 1e-15
    ok &= tw
    out.append(f"    in between: corners of a square, |E Phi| = 1: the ensembles (1/2, 1/2, 0, 0) and (1/2, 0, 1/2, 0) both have it: {tw}")
    return ok, out


# ---------------------------------------------------------------------------------------------------------- Q3
def consistent_squared_data(a):
    """Is there an ensemble on {1..m} x {+,-} with (E phi_i)^2 = a_i^2 and E(sum phi_i) = 0?  phi_i(j, +-) = +-A [i = j]."""
    m = len(a); A = float(sum(a)); n = 2 * m
    for s in itertools.product((1, -1), repeat=m - 1):
        s = (1,) + s                                                 # global sign is a symmetry
        # variables w(i,+), w(i,-); constraints: A (w(i,+) - w(i,-)) = s_i a_i for all i; sum_i that = 0; total mass 1
        Aeq = np.zeros((m + 2, n)); beq = np.zeros(m + 2)
        for i in range(m):
            Aeq[i, 2 * i] = A; Aeq[i, 2 * i + 1] = -A; beq[i] = s[i] * a[i]
            Aeq[m, 2 * i] = A; Aeq[m, 2 * i + 1] = -A
        Aeq[m + 1, :] = 1.0; beq[m + 1] = 1.0
        if linprog(np.zeros(n), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * n, method="highs").status == 0:
            return True
    return False


def partition_exists(a):
    tot = sum(a)
    if tot % 2:
        return False
    reach = {0}
    for v in a:
        reach |= {x + v for x in reach}
    return tot // 2 in reach


def test_Q3():
    agree = yes = 0; cases = 60
    for _ in range(cases):
        m = int(rng.integers(3, 9)); a = [int(v) for v in rng.integers(1, 12, size=m)]
        c, p = consistent_squared_data(a), partition_exists(a)
        agree += c == p; yes += p
    fixed = [([3, 1, 1, 2, 2, 1], True), ([5, 4, 2], False), ([7, 3, 2, 1, 1], True), ([8, 6, 5], False)]
    okf = all(consistent_squared_data(a) == ans == partition_exists(a) for a, ans in fixed)
    return agree == cases and okf and 0 < yes < cases, \
        [f"    squared means: {cases} random instances (3 to 8 integers): consistency of the data, decided by up to 2^(m-1) "
         f"linear feasibility problems, agrees with the subset-sum table in {agree}/{cases} ({yes} consistent); "
         f"four fixed instances: {okf}"]


# ---------------------------------------------------------------------------------------------------------- Q4
def test_Q4():
    worst_gap = 0.0; ok = True; cases = 0
    for _ in range(12):
        M = int(rng.integers(5, 9)); P = rng.normal(size=(M, 2)); tgt = rng.normal(size=M)
        R = np.linalg.norm(P, axis=1).max(); rho = rng.uniform(0.3, 0.8) * R
        # exact (fine search): range of E tgt over ensembles with |E Phi| >= rho  =  max over directions u of the LP
        def best_over(G, enlarge):
            best = -np.inf
            for k in range(G):
                u = np.array([np.cos(2 * np.pi * k / G), np.sin(2 * np.pi * k / G)])
                res = lp(-tgt, A_ub=-(P @ u)[None, :], b_ub=[-(rho - enlarge)], A_eq=np.ones((1, M)), b_eq=[1.0], n=M)
                if res.status == 0:
                    best = max(best, -res.fun)
            return best
        fine = best_over(1440, 0.0)                                  # inner: every direction gives feasible ensembles
        for G in (24, 96):
            h = np.pi / G                                            # every direction is within h of a net direction
            outer = best_over(G, R * h)                              # certified outer bound (Proposition E24)
            if np.isfinite(fine):
                ok &= outer >= fine - 1e-9
                if G == 96:
                    worst_gap = max(worst_gap, outer - fine)
        cases += np.isfinite(fine)
    return ok and cases > 5, \
        [f"    lower bound on the norm of a mean vector in the plane, {cases} feasible instances: the net of 24 or 96 directions "
         f"with the certified enlargement never falls below the fine search (1 440 directions); largest overestimate with "
         f"96 directions: {worst_gap:.3f}"]


# ---------------------------------------------------------------------------------------------------------- Q5
def determined_up_to_factor(Phi, mu):
    """Direct test: is mu the only ensemble nu with E_nu Phi = t E_mu Phi for some t > 0?  (2M linear programmes.)"""
    m, M = Phi.shape; z = Phi @ mu
    Aeq = np.zeros((m + 1, M + 1)); Aeq[:m, :M] = Phi; Aeq[:m, M] = -z; Aeq[m, :M] = 1.0
    beq = np.zeros(m + 1); beq[m] = 1.0
    for x in range(M):
        for sgn in (1.0, -1.0):
            c = np.zeros(M + 1); c[x] = sgn
            res = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M + [(1e-9, None)], method="highs")
            if res.status != 0 or abs(res.x[x] - mu[x]) > 1e-7:
                return False
    return True


def homogeneous_certificate(Phi, S):
    """Criterion of Proposition E23(b): Phi linearly independent on S and some lambda.Phi >= 0 with zero set S."""
    m, M = Phi.shape
    if np.linalg.matrix_rank(Phi[:, S], tol=1e-9) < len(S):
        return False
    off = [x for x in range(M) if x not in S]
    if not off:
        return True
    c = np.zeros(m + 1); c[-1] = -1.0                      # maximise the margin t
    A_ub = np.hstack([-Phi[:, off].T, np.ones((len(off), 1))])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(len(off)), A_eq=np.hstack([Phi[:, S].T, np.zeros((len(S), 1))]),
                  b_eq=np.zeros(len(S)), bounds=[(-1, 1)] * m + [(None, 1.0)], method="highs")
    return res.status == 0 and res.x[-1] > 1e-7


def test_Q5():
    agree = 0; yes = 0; cases = 400; skipped = 0
    for _ in range(cases):
        M = int(rng.integers(3, 7)); m = int(rng.integers(1, 4))
        Phi = rng.integers(-2, 3, size=(m, M)).astype(float)
        K = int(rng.integers(1, min(M, 3) + 1)); S = sorted(int(v) for v in rng.choice(M, size=K, replace=False))
        mu = np.zeros(M); mu[S] = rng.dirichlet(np.ones(K))
        if np.linalg.norm(Phi @ mu) < 1e-9:                # the statement is for non-zero data
            skipped += 1; continue
        a, b = determined_up_to_factor(Phi, mu), homogeneous_certificate(Phi, S)
        agree += a == b; yes += a
    Phi = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])     # the example of the text: a, b, c
    ex = (determined_up_to_factor(Phi, np.array([1.0, 0.0, 0.0])) and homogeneous_certificate(Phi, [0])
          and not determined_up_to_factor(Phi, np.array([0.5, 0.5, 0.0])) and not homogeneous_certificate(Phi, [0, 1]))
    used = cases - skipped
    return agree == used and ex and 0 < yes < used, \
        [f"    data known up to a factor: {used} random instances with integer observables ({skipped} with zero data set aside): "
         f"the direct test (is another ensemble compatible?) and the criterion of E23(b) agree in {agree}/{used} "
         f"({yes} determined up to the factor); the three-point example of the text: {ex}"]


def main():
    allok = True
    for name, fn in (("Q1 ratio data are linear (Proposition E23)", test_Q1),
                     ("Q2 the norm of a mean vector (Theorem E25)", test_Q2),
                     ("Q3 squared means and subset sums (Theorem E26)", test_Q3),
                     ("Q4 a reverse-convex constraint as a union over directions (Proposition E24)", test_Q4),
                     ("Q5 data known up to a factor (Proposition E23(b))", test_Q5)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
