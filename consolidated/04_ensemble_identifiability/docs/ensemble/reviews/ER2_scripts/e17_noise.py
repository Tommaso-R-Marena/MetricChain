#!/usr/bin/env python3
"""ER2: attack on Theorem E17 (modulus = dual certificate = estimator; Gaussian noise, l2 data norm).

N1  the constants: Phi_N(-1)/4 against 1/25.3; sqrt(Phi_N(-1))/2 against 0.199.
N2  (a): the modulus computed both ways with the l2 norm (the repository check F5 uses the l_inf norm and the
    class of all ensembles only): primal second-order-cone programme by cutting planes on the ball, dual by
    cutting planes on the epigraph of the norm; for P = all ensembles and for an envelope class (vertices of
    the class polytope by brute force).
N3  (b): the affine estimator T^ = lam.y + c with lam optimal at eps = 2 sigma: exact worst-case risk
    sigma^2 |lam|^2 + R^2/4 against omega(2 sigma)^2 / 4, and a Monte Carlo simulation at the worst member.
N4  (c): the two-hypothesis problem (mu0, mu1) attaining omega(2 sigma): exact minimax risk of the pair
    (Bayes risk of the symmetric prior, by quadrature) and a simulation of the Bayes rule, against the
    claimed lower bound Phi_N(-1) omega(2 sigma)^2 / 4.
N5  toy model X = {0,1}, P = all ensembles (a bounded normal mean): omega(eps) = min(eps, 1); the chain
        Phi_N(-1) w^2/4  <=  two-point minimax  <=  minimax  <=  affine minimax (Donoho's formula)  <=  risk of T^  <=  w^2/4,
    w = omega(2 sigma); with the bound from the cited theory, minimax >= affine minimax / 1.25 >= w^2/10.
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.stats import norm
from scipy.integrate import quad
from er2_common import class_rows_mu, vertices_bruteforce, shortest_path_closure

rng = np.random.default_rng(1701)


def modulus_primal(psi, Phi, eps, R=None, tol=1e-10, maxit=400):
    """sup psi.(mu1 - mu0), mu0, mu1 in P (simplex, plus rows R mu <= 0 if given), |Phi (mu1-mu0)|_2 <= eps.
    Returns (lower bound from a feasible pair, upper bound from the relaxation, mu0, mu1)."""
    m, N = Phi.shape
    cuts = [np.eye(m)[k] * s for k in range(m) for s in (1.0, -1.0)]
    A_eq = np.zeros((2, 2 * N)); A_eq[0, :N] = 1; A_eq[1, N:] = 1
    if R is not None:
        Z = np.zeros_like(R); Rblock = np.vstack([np.hstack([R, Z]), np.hstack([Z, R])])
    best_lo = -np.inf; arg = None
    for it in range(maxit):
        U = np.array(cuts)
        A_ub = np.hstack([-U @ Phi, U @ Phi])                 # u.Phi(mu1 - mu0) <= eps ; variables (mu0, mu1)
        b_ub = eps * np.ones(len(U))
        if R is not None:
            A_ub = np.vstack([A_ub, Rblock]); b_ub = np.concatenate([b_ub, np.zeros(len(Rblock))])
        res = linprog(-np.concatenate([-psi, psi]), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1, 1],
                      bounds=[(0, None)] * (2 * N), method="highs")
        mu0, mu1 = res.x[:N], res.x[N:]; up = -res.fun
        v = Phi @ (mu1 - mu0); nv = np.linalg.norm(v)
        t = 1.0 if nv <= eps else eps / nv
        lo = t * psi @ (mu1 - mu0)
        if lo > best_lo:
            best_lo = lo; arg = (mu0.copy(), (1 - t) * mu0 + t * mu1)
        if up - best_lo < tol or nv <= eps * (1 + 1e-13):
            return best_lo, up, arg[0], arg[1]
        cuts.append(v / nv)
    return best_lo, up, arg[0], arg[1]


def modulus_dual(psi, Phi, eps, V, tol=1e-10, maxit=400):
    """min_lam eps |lam|_2 + range over conv(V) of E(psi - lam.Phi).  V: rows = vertices of P.
    Returns (lower bound from the relaxation, upper bound = value at the best lam, lam, hi, lo)."""
    m, N = Phi.shape
    a = V @ psi; B = V @ Phi.T                         # E_v psi, E_v Phi
    cuts = [np.eye(m)[k] * s for k in range(m) for s in (1.0, -1.0)]
    best_up = np.inf; arg = None
    for it in range(maxit):
        U = np.array(cuts)
        # variables: lam (m), s, hi, lo ; minimise eps*s + hi - lo
        c = np.concatenate([np.zeros(m), [eps, 1.0, -1.0]])
        A1 = np.hstack([-B, np.zeros((len(V), 1)), -np.ones((len(V), 1)), np.zeros((len(V), 1))])    # a - B lam <= hi
        A2 = np.hstack([B, np.zeros((len(V), 1)), np.zeros((len(V), 1)), np.ones((len(V), 1))])      # lo <= a - B lam
        A3 = np.hstack([U, -np.ones((len(U), 1)), np.zeros((len(U), 2))])                            # u.lam <= s
        res = linprog(c, A_ub=np.vstack([A1, A2, A3]), b_ub=np.concatenate([-a, a, np.zeros(len(U))]),
                      bounds=[(None, None)] * m + [(0, None), (None, None), (None, None)], method="highs")
        lam = res.x[:m]; low = res.fun
        f = a - B @ lam
        val = eps * np.linalg.norm(lam) + f.max() - f.min()
        if val < best_up:
            best_up = val; arg = (lam.copy(), f.max(), f.min())
        if best_up - low < tol or np.linalg.norm(lam) < 1e-14:
            return low, best_up, arg
        cuts.append(lam / np.linalg.norm(lam))
    return low, best_up, arg


def polish_primal(psi, Phi, eps, R, mu0, mu1):
    """SLSQP from the cutting-plane point; returns a FEASIBLE pair (re-projected by the scaling argument)."""
    from scipy.optimize import minimize
    m, N = Phi.shape
    x0 = np.concatenate([mu0, mu1])
    cons = [{"type": "eq", "fun": lambda x: x[:N].sum() - 1.0}, {"type": "eq", "fun": lambda x: x[N:].sum() - 1.0},
            {"type": "ineq", "fun": lambda x: eps ** 2 - np.sum((Phi @ (x[N:] - x[:N])) ** 2),
             "jac": lambda x: np.concatenate([2 * Phi.T @ (Phi @ (x[N:] - x[:N])), -2 * Phi.T @ (Phi @ (x[N:] - x[:N]))])}]
    if R is not None:
        cons.append({"type": "ineq", "fun": lambda x: -(R @ x[:N]), "jac": lambda x: np.hstack([-R, np.zeros_like(R)])})
        cons.append({"type": "ineq", "fun": lambda x: -(R @ x[N:]), "jac": lambda x: np.hstack([np.zeros_like(R), -R])})
    res = minimize(lambda x: -psi @ (x[N:] - x[:N]), x0, jac=lambda x: np.concatenate([psi, -psi]),
                   bounds=[(0, None)] * (2 * N), constraints=cons, method="SLSQP", options=dict(ftol=1e-15, maxiter=500))
    a, b = np.maximum(res.x[:N], 0), np.maximum(res.x[N:], 0)
    a /= a.sum(); b /= b.sum()
    # exact feasibility: membership (tiny violations are removed by mixing with the cutting-plane pair) and the ball
    for _ in range(60):
        if R is None or ((R @ a).max() <= 0 and (R @ b).max() <= 0):
            break
        a = 0.5 * (a + mu0); b = 0.5 * (b + mu1)
    nv = np.linalg.norm(Phi @ (b - a)); t = 1.0 if nv <= eps else eps / nv
    b = (1 - t) * a + t * b
    return psi @ (b - a), a, b


def polish_dual(psi, Phi, eps, V, lam0):
    from scipy.optimize import minimize
    a = V @ psi; B = V @ Phi.T
    g = lambda lam: eps * np.linalg.norm(lam) + (a - B @ lam).max() - (a - B @ lam).min()
    best = (g(lam0), lam0)
    m = len(lam0)
    f0 = a - B @ lam0
    x0 = np.concatenate([lam0, [f0.max(), f0.min()]])
    cons = [{"type": "ineq", "fun": lambda x: x[m] - (a - B @ x[:m])}, {"type": "ineq", "fun": lambda x: (a - B @ x[:m]) - x[m + 1]}]
    res = minimize(lambda x: eps * np.sqrt(x[:m] @ x[:m] + 1e-300) + x[m] - x[m + 1], x0, constraints=cons, method="SLSQP",
                   options=dict(ftol=1e-15, maxiter=500))
    if g(res.x[:m]) < best[0]:
        best = (g(res.x[:m]), res.x[:m])
    f = a - B @ best[1]
    return best[0], best[1], f.max(), f.min()


def modulus_both(psi, Phi, eps, R, V):
    """(primal value at a feasible pair, dual value at a lam, mu0, mu1, lam, hi, lo) after cutting planes + polishing."""
    plo, pup, mu0, mu1 = modulus_primal(psi, Phi, eps, R, maxit=150)
    dlo, dup, (lam, hi, lo) = modulus_dual(psi, Phi, eps, V, maxit=150)
    if dup - plo > 1e-9:
        val, a, b = polish_primal(psi, Phi, eps, R, mu0, mu1)
        if val > plo:
            plo, mu0, mu1 = val, a, b
        dval, lam2, hi2, lo2 = polish_dual(psi, Phi, eps, V, lam)
        if dval < dup:
            dup, lam, hi, lo = dval, lam2, hi2, lo2
    return plo, dup, mu0, mu1, lam, hi, lo


def two_point_minimax(u):
    """Minimax risk, in units of Delta^2/4, of estimating T in {T0, T0 + Delta} from y ~ N(A mu_j, sigma^2 I),
    u = |A(mu1 - mu0)| / (2 sigma):  E sech^2(u (u + Z))."""
    f = lambda z: norm.pdf(z) / np.cosh(min(u * (u + z), 300.0)) ** 2 if u * (u + z) > 0 else norm.pdf(z) / np.cosh(max(u * (u + z), -300.0)) ** 2
    return quad(f, -12, 12, limit=200)[0]


def N1():
    p = norm.cdf(-1.0)
    print(f"N1  Phi_N(-1) = {p:.6f}; Phi_N(-1)/4 = {p / 4:.6f} = 1/{4 / p:.3f}  (claimed >= 1/25.3 = {1 / 25.3:.6f}: {p / 4 >= 1 / 25.3});"
          f" sqrt(Phi_N(-1))/2 = {np.sqrt(p) / 2:.5f} (claimed 0.199)")
    print(f"    total variation of N(0,1) and N(2,1): {2 * norm.cdf(1) - 1:.6f} = 2 Phi_N(1) - 1")
    return p / 4 >= 1 / 25.3 and np.sqrt(p) / 2 >= 0.199


def random_class(N):
    d = shortest_path_closure(rng.uniform(0.2, 2.0, size=(N, N)))
    pi = rng.dirichlet(np.ones(N) * 3)
    R, _ = class_rows_mu(pi, d)
    V = vertices_bruteforce(pi, d)
    return R, V


def ray_values(psi, Phi, eps, R, V, u):
    """For a unit direction u in data space: L(u) = sup psi.(mu1-mu0) with Phi(mu1-mu0) = t u, 0 <= t <= eps (a primal
    value: feasible pair) and G(u) = min_{s>=0} eps s + range(psi - s u.Phi) (a dual value at lam = s u).  Two LPs."""
    m, N = Phi.shape
    # primal: variables mu0, mu1, t
    c = np.concatenate([psi, -psi, [0.0]])
    A_eq = np.zeros((2 + m, 2 * N + 1)); A_eq[0, :N] = 1; A_eq[1, N:2 * N] = 1
    A_eq[2:, :N] = -Phi; A_eq[2:, N:2 * N] = Phi; A_eq[2:, -1] = -u
    b_eq = np.concatenate([[1.0, 1.0], np.zeros(m)])
    A_ub = b_ub = None
    if R is not None:
        Z = np.zeros_like(R); z1 = np.zeros((len(R), 1))
        A_ub = np.vstack([np.hstack([R, Z, z1]), np.hstack([Z, R, z1])]); b_ub = np.zeros(2 * len(R))
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * (2 * N) + [(0, eps)], method="highs")
    L = -res.fun
    a = V @ psi; bu = V @ (Phi.T @ u)
    res2 = linprog([eps, 1.0, -1.0], A_ub=np.vstack([np.column_stack([-bu, -np.ones(len(V)), np.zeros(len(V))]),
                                                    np.column_stack([bu, np.zeros(len(V)), np.ones(len(V))])]),
                   b_ub=np.concatenate([-a, a]), bounds=[(0, None), (None, None), (None, None)], method="highs")
    return L, res2.fun


def precise_m2(psi, Phi, eps, R, V):
    """m = 2: omega(eps) as max over directions of L and as min over directions of G (one-dimensional searches)."""
    from scipy.optimize import minimize_scalar
    ths = np.linspace(0, 2 * np.pi, 361)[:-1]
    vals = [ray_values(psi, Phi, eps, R, V, np.array([np.cos(t), np.sin(t)])) for t in ths]
    Ls = np.array([v[0] for v in vals]); Gs = np.array([v[1] for v in vals])
    h = ths[1] - ths[0]
    kL = int(np.argmax(Ls)); kG = int(np.argmin(Gs))
    fL = lambda t: -ray_values(psi, Phi, eps, R, V, np.array([np.cos(t), np.sin(t)]))[0]
    fG = lambda t: ray_values(psi, Phi, eps, R, V, np.array([np.cos(t), np.sin(t)]))[1]
    rL = minimize_scalar(fL, bounds=(ths[kL] - h, ths[kL] + h), method="bounded", options=dict(xatol=1e-13))
    rG = minimize_scalar(fG, bounds=(ths[kG] - h, ths[kG] + h), method="bounded", options=dict(xatol=1e-13))
    return max(-rL.fun, Ls.max()), min(rG.fun, Gs.min())


def N2():
    print("N2  (a) duality with the l2 norm: primal (feasible pair / relaxation) against dual (relaxation / value at lam)")
    worst = 0.0; cnt = 0; worst_bracket = 0.0
    for kind in ("all ensembles", "envelope class"):
        for _ in range(25 if kind == "all ensembles" else 12):
            N = int(rng.integers(5, 9)) if kind == "all ensembles" else 5
            m = int(rng.integers(1, 4))
            Phi = rng.normal(size=(m, N)); psi = rng.normal(size=N)
            if kind == "all ensembles":
                R = None; V = np.eye(N)
            else:
                R, V = random_class(N)
            for eps in (0.02, 0.1, 0.4, 1.5):
                plo, dup, mu0, mu1, lam, hi, lo = modulus_both(psi, Phi, eps, R, V)
                worst = max(worst, abs(plo - dup)); cnt += 1
                assert plo <= dup + 1e-9                       # weak duality (feasible pair against a dual value)
    print(f"    {cnt} (instance, eps) pairs, m = 1..3: largest (dual value at a lam) - (primal value at a feasible pair) = {worst:.2e}"
          "  (cutting planes + SLSQP; accuracy of this solver about 1e-6)")
    # high precision for m = 1 (exact LPs) and m = 2 (one-dimensional searches over the direction)
    w1 = w2 = 0.0; c1 = c2 = 0
    for kind in ("all ensembles", "envelope class"):
        for _ in range(8):
            N = 6 if kind == "all ensembles" else 5
            if kind == "all ensembles":
                R = None; V = np.eye(N)
            else:
                R, V = random_class(N)
            psi = rng.normal(size=N)
            for m in (1, 2):
                Phi = rng.normal(size=(m, N))
                for eps in (0.05, 0.3, 1.0):
                    if m == 1:
                        Lp, Gp = ray_values(psi, Phi, eps, R, V, np.array([1.0])); Lm, Gm = ray_values(psi, Phi, eps, R, V, np.array([-1.0]))
                        w1 = max(w1, abs(max(Lp, Lm) - min(Gp, Gm))); c1 += 1
                    else:
                        L, G = precise_m2(psi, Phi, eps, R, V)
                        w2 = max(w2, abs(G - L)); c2 += 1
    print(f"    second method: m = 1 ({c1} cases, two LPs each side): largest |primal - dual| = {w1:.2e};  "
          f"m = 2 ({c2} cases, max over directions of the primal ray value against min over directions of the dual ray value): {w2:.2e}"
          "  (both signs occur: this is the 1e-7 feasibility tolerance of the LP solver)")
    return worst < 5e-6 and w1 < 1e-7 and w2 < 1e-6


def N3_N4():
    print("N3/N4  (b) the affine estimator; (c) the two-point lower bound  (random instances: all ensembles and an envelope class)")
    ok = True; rows = []; failed = []; gapmax = 0.0
    p1 = norm.cdf(-1.0)
    for kind in ("all ensembles", "envelope class"):
        for rep in range(6):
            N = 6 if kind == "all ensembles" else 5; m = 2
            Phi = rng.normal(size=(m, N)); psi = rng.normal(size=N)
            if kind == "all ensembles":
                R = None; V = np.eye(N)
            else:
                R, V = random_class(N)
            sigma = float(rng.choice([0.03, 0.1, 0.3, 1.0]))
            w, dval, mu0, mu1, lam, hi, lo = modulus_both(psi, Phi, 2 * sigma, R, V)
            c = 0.5 * (hi + lo); Rg = hi - lo
            risk_formula = sigma ** 2 * lam @ lam + Rg ** 2 / 4
            # exact worst-case risk over the vertices (risk is convex in mu: variance + squared affine bias)
            bias = c - V @ (psi - lam @ Phi)
            risk_exact = sigma ** 2 * lam @ lam + (bias ** 2).max()
            # Monte Carlo at the worst vertex
            k = int(np.argmax(bias ** 2)); mu = V[k]
            ys = Phi @ mu + sigma * rng.normal(size=(200000, m))
            mc = np.mean((ys @ lam + c - psi @ mu) ** 2)
            # two-point problem at the pair attaining omega(2 sigma)
            Delta = psi @ (mu1 - mu0); dist = np.linalg.norm(Phi @ (mu1 - mu0)); u = dist / (2 * sigma)
            tp = two_point_minimax(u) * Delta ** 2 / 4
            # simulation of the Bayes rule of the symmetric prior at mu0 and mu1
            dirn = Phi @ (mu1 - mu0)
            sims = []
            for mu_true, Ttrue in ((mu0, psi @ mu0), (mu1, psi @ mu1)):
                ys = Phi @ mu_true + sigma * rng.normal(size=(200000, m))
                llr = (ys - Phi @ (0.5 * (mu0 + mu1))) @ dirn / sigma ** 2
                That = psi @ mu0 + Delta / (1 + np.exp(-llr))
                sims.append(np.mean((That - Ttrue) ** 2))
            rows.append((kind, sigma, w, dval, risk_formula, risk_exact, mc, w ** 2 / 4, tp, max(sims), p1 * w ** 2 / 4, u))
            conds = dict(duality=abs(w - dval) < 5e-6, exact_le_formula=risk_exact <= risk_formula + 1e-12,
                         formula_le_quarter=risk_formula <= dval ** 2 / 4 + 1e-9, twopoint_ge_claim=tp >= p1 * w ** 2 / 4 - 1e-12,
                         twopoint_le_risk=tp <= risk_exact + 1e-9, simulation_T=abs(mc - risk_exact) < 0.02 * risk_exact + 1e-9,
                         simulation_bayes=abs(max(sims) - tp) < 0.03 * tp + 1e-9)
            gapmax = max(gapmax, abs(w - dval))
            for k, v in conds.items():
                if not v:
                    failed.append((kind, rep, k))
            ok &= all(conds.values())
    print("    kind            sigma   omega(2s)   sup risk of T^ (formula / exact / simulated)   omega^2/4    two-point minimax (exact / simulated)   Phi(-1) omega^2/4   |A dmu|/2s")
    for r in rows:
        print(f"    {r[0]:15s} {r[1]:5.2f}   {r[2]:8.5f}   {r[4]:.6f} / {r[5]:.6f} / {r[6]:.6f}              {r[7]:.6f}    {r[8]:.6f} / {r[9]:.6f}                 {r[10]:.6f}          {r[11]:.4f}")
    print(f"    two-point minimax in units of omega^2/4 when |A dmu| = 2 sigma: E sech^2(1 + Z) = {two_point_minimax(1.0):.4f}  (the report's constant: Phi_N(-1) = {p1:.4f})")
    print(f"    largest |primal - dual| for omega(2 sigma) in these instances: {gapmax:.1e} (solver accuracy); conditions violated: {failed if failed else 'none'}")
    return ok


def N5():
    print("N5  toy model X = {0,1}, all ensembles, Phi = psi = x:  T = p in [0,1], y = p + sigma xi;  omega(eps) = min(eps, 1)")
    ok = True; p1 = norm.cdf(-1.0)
    print("    sigma    w=omega(2s)   Phi(-1)w^2/4   w^2/25.3    best two-point   affine minimax (Donoho)   risk of T^ (E17b)   w^2/4     RMSE band [0.199 w, 0.5 w] vs sqrt(two-point), sqrt(affine)")
    for sigma in (0.02, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0):
        psi = np.array([0.0, 1.0]); Phi = np.array([[0.0, 1.0]])
        w, _, mu0, mu1 = modulus_primal(psi, Phi, 2 * sigma)
        _, dval, (lam, hi, lo) = modulus_dual(psi, Phi, 2 * sigma, np.eye(2))
        assert abs(w - min(2 * sigma, 1.0)) < 1e-9 and abs(dval - w) < 1e-9
        risk_hat = sigma ** 2 * lam @ lam + (hi - lo) ** 2 / 4
        # affine minimax risk: bounded normal mean on an interval of half-length 1/2: tau^2 s^2/(tau^2+s^2)
        aff = 0.25 * sigma ** 2 / (0.25 + sigma ** 2)
        # Donoho's formula sup_eps (omega(eps)^2/4) sigma^2/(sigma^2 + eps^2/4)
        es = np.linspace(1e-6, 1.0, 20001)
        don = np.max((np.minimum(es, 1.0) ** 2 / 4) * sigma ** 2 / (sigma ** 2 + es ** 2 / 4))
        # best two-point lower bound: sup over pairs p0 < p1, distance e = p1 - p0 <= 1
        tp = max(two_point_minimax(e / (2 * sigma)) * e ** 2 / 4 for e in np.linspace(0.01, 1.0, 100))
        # simulation: risk of T^ at p = 0 and p = 1, risk of the Bayes rule of the prior {0,1} at both ends
        z = rng.normal(size=400000)
        sim_hat = max(np.mean((lam[0] * (p + sigma * z) + 0.5 * (hi + lo) - p) ** 2) for p in (0.0, 1.0))
        print(f"    {sigma:5.2f}    {w:.4f}        {p1 * w ** 2 / 4:.6f}       {w ** 2 / 25.3:.6f}    {tp:.6f}         {aff:.6f} ({don:.6f})       {risk_hat:.6f} (sim {sim_hat:.6f})   {w ** 2 / 4:.6f}    "
              f"[{0.199 * w:.4f}, {0.5 * w:.4f}]  {np.sqrt(tp):.4f}, {np.sqrt(aff):.4f}")
        ok &= p1 * w ** 2 / 4 <= tp + 1e-12 and tp <= aff + 1e-9 and aff <= risk_hat + 1e-9 and risk_hat <= w ** 2 / 4 + 1e-9
        ok &= abs(aff - don) < 1e-6 and aff / 1.25 >= w ** 2 / 10 - 1e-12 and abs(sim_hat - risk_hat) < 0.02 * risk_hat
    print("    (the cited theory gives more than E17(c): minimax >= affine minimax / 1.25 >= omega(2 sigma)^2 / 10, i.e. RMSE >= 0.316 omega(2 sigma))")
    return ok


def main():
    t0 = time.time(); allok = True
    for fn in (N1, N2, N3_N4, N5):
        ok = fn(); allok &= ok
        print(f"    -> {'consistent' if ok else 'INCONSISTENT'}   [{time.time() - t0:.0f} s]", flush=True)
    print("E17: NO COUNTEREXAMPLE" if allok else "E17: SEE ABOVE")


if __name__ == "__main__":
    main()
