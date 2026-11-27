#!/usr/bin/env python3
"""Workstream M — small numerical sanity checks of the *statements compared in the report*.

These are not new results.  They check, on small random instances, that the published
formulas quoted in SM_REPORT.md say what the report claims they say, so that the comparison
"statement in literature A == statement in literature B == the division's Q1/Q2 sketch" is not
made on notation alone.

  N1  MaxOcc / maximal mass: primal LP  ==  Gardner-Longinetti-Sgheri ray-shooting formula
      ==  di Dio-Schmuedgen conic dual kappa;  minOR(A) == 1 - maxOR(complement of A).
  N2  KL ball + moment constraints: direct convex optimisation  ==  the dual formula of
      Christensen-Connault Prop. 2.1 (KL case);  rho -> infinity recovers the prior-free LP
      whose dual is  min_lambda [ max_x (psi - lambda.phi)(x) + lambda.m ]  (their Lemma B.3).
  N3  The coordinator's Q2 sketch (M_brief.md): mu ~ exp(-u*dist(x,C)), C linear with dual
      distance > k: all <=k-site marginals exactly uniform; entropy per site against the class
      bound h(1/(1+e^u)) and against ln 2.
  N4  Envelope cone (theory report Thm 11.12 remark) intersected with moment constraints is a
      plain LP in the weights; nesting of the three identified sets.

Run:  python3 experiments/science/ws_M/check_statements.py
      (about 2 min CPU; 6.5 min wall on the shared 4-core machine on 2026-11-25; < 300 MB;
       fixed seed 20261125, so the output is reproducible)
Output is also written to experiments/science/ws_M/check_statements.out
"""
import itertools
import sys
import numpy as np
from scipy.optimize import linprog, minimize

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


rng = np.random.default_rng(20261125)

# ---------------------------------------------------------------------------------------
# N1  maximal mass at a point / of a region
# ---------------------------------------------------------------------------------------


def primal_range(phi, m, psi, sense):
    """max (sense=+1) or min (sense=-1) of sum mu*psi over mu>=0, sum mu = 1, sum mu*phi = m."""
    n = phi.shape[0]
    A = np.vstack([np.ones(n), phi.T])
    b = np.concatenate([[1.0], m])
    r = linprog(-sense * psi, A_eq=A, b_eq=b, bounds=[(0, None)] * n, method="highs")
    assert r.status == 0, r.message
    return sense * (-r.fun)


def dual_upper(phi, m, psi):
    """min lam0 + lam.m  s.t.  lam0 + lam.phi(x) >= psi(x) for all x  (the 'hard-max' dual)."""
    n, K = phi.shape
    c = np.concatenate([[1.0], m])
    A = -np.hstack([np.ones((n, 1)), phi])
    r = linprog(c, A_ub=A, b_ub=-psi, bounds=[(None, None)] * (K + 1), method="highs")
    assert r.status == 0, r.message
    return r.fun, r.x


def in_hull(phi, v):
    n = phi.shape[0]
    A = np.vstack([np.ones(n), phi.T])
    b = np.concatenate([[1.0], v])
    r = linprog(np.zeros(n), A_eq=A, b_eq=b, bounds=[(0, None)] * n, method="highs")
    return r.status == 0


def ray_shoot(phi, m, x0, tol=1e-10):
    """Gardner-Longinetti-Sgheri Thm 3.8 / di Dio-Schmuedgen Prop. 75 (first formula):
    sup{ t in [0,1) : (m - t*phi(x0))/(1-t) in conv phi(X) }  by bisection."""
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        t = 0.5 * (lo + hi)
        if in_hull(phi, (m - t * phi[x0]) / (1 - t)):
            lo = t
        else:
            hi = t
    return lo


def kappa(phi, m, x0):
    """di Dio-Schmuedgen eq. (32): inf{ L_s(p) : p >= 0 on X, p(x0) = 1 }, p = p0 + lam.phi."""
    n, K = phi.shape
    c = np.concatenate([[1.0], m])
    A_ub = -np.hstack([np.ones((n, 1)), phi])
    A_eq = np.concatenate([[1.0], phi[x0]])[None, :]
    r = linprog(c, A_ub=A_ub, b_ub=np.zeros(n), A_eq=A_eq, b_eq=[1.0],
                bounds=[(None, None)] * (K + 1), method="highs")
    assert r.status == 0, r.message
    return r.fun


say("=" * 88)
say("N1  MaxOcc == maximal mass function == ray shooting == conic dual (random instances)")
worst = 0.0
worst_reg = 0.0
ntest = 0
for trial in range(40):
    n = int(rng.integers(12, 60))
    K = int(rng.integers(1, 6))
    phi = rng.normal(size=(n, K))
    mu_true = rng.dirichlet(np.ones(n) * 0.3)
    m = mu_true @ phi
    for x0 in rng.choice(n, size=3, replace=False):
        e = np.zeros(n)
        e[x0] = 1.0
        p = primal_range(phi, m, e, +1)
        d, _ = dual_upper(phi, m, e)
        rs = ray_shoot(phi, m, x0)
        kp = kappa(phi, m, x0)
        worst = max(worst, abs(p - d), abs(p - rs), abs(p - kp))
        assert mu_true[x0] <= p + 1e-9
        ntest += 1
    # regions: minOR(A) = 1 - maxOR(A^c)
    A_ind = (rng.random(n) < 0.4).astype(float)
    lo = primal_range(phi, m, A_ind, -1)
    hi_c = primal_range(phi, m, 1 - A_ind, +1)
    worst_reg = max(worst_reg, abs(lo - (1 - hi_c)))
say(f"   {ntest} point instances: max |primal - dual|, |primal - ray|, |primal - kappa| = {worst:.2e}")
say(f"   40 region instances:  max |minOR(A) - (1 - maxOR(A^c))| = {worst_reg:.2e}")

# ---------------------------------------------------------------------------------------
# N2  KL ball + moment constraints
# ---------------------------------------------------------------------------------------


def kl(mu, mu0):
    mask = mu > 0
    return float(np.sum(mu[mask] * np.log(mu[mask] / mu0[mask])))


def kl_primal(mu0, phi, m, psi, rho):
    """max sum mu psi s.t. KL(mu||mu0) <= rho, sum mu phi = m, mu in simplex (SLSQP)."""
    n = len(mu0)
    cons = [
        {"type": "eq", "fun": lambda w: np.sum(w) - 1.0},
        {"type": "eq", "fun": lambda w: w @ phi - m},
        {"type": "ineq", "fun": lambda w: rho - np.sum(w * np.log(np.maximum(w, 1e-300) / mu0))},
    ]
    best = -np.inf
    for start in range(6):
        w0 = rng.dirichlet(np.ones(n)) if start else mu0.copy()
        r = minimize(lambda w: -(w @ psi), w0, constraints=cons, bounds=[(1e-12, 1)] * n,
                     method="SLSQP", options={"maxiter": 2000, "ftol": 1e-13})
        w = r.x
        ok = abs(w.sum() - 1) < 1e-7 and np.max(np.abs(w @ phi - m)) < 1e-7 and kl(w, mu0) <= rho + 1e-7
        if ok:
            best = max(best, float(w @ psi))
    return best


def kl_dual(mu0, phi, m, psi, rho):
    """Christensen-Connault Prop. 2.1, KL case:
    inf_{eta>0, lam} eta*log E_mu0 exp((psi - lam.phi)/eta) + eta*rho + lam.m"""
    K = phi.shape[1]

    def f(z):
        eta = np.exp(z[0])
        lam = z[1:]
        a = (psi - phi @ lam) / eta
        amax = a.max()
        return eta * (amax + np.log(np.sum(mu0 * np.exp(a - amax)))) + eta * rho + lam @ m

    best = np.inf
    for start in range(8):
        z0 = np.concatenate([[rng.normal()], rng.normal(size=K)])
        r = minimize(f, z0, method="BFGS", options={"gtol": 1e-10, "maxiter": 5000})
        best = min(best, r.fun)
    return best


def min_kl(mu0, phi, m):
    """I-projection value: min KL(mu||mu0) s.t. moments = max_lam [ -log E exp(-lam.(phi-m)) ]."""
    K = phi.shape[1]

    def g(lam):
        a = -(phi - m) @ lam
        amax = a.max()
        return amax + np.log(np.sum(mu0 * np.exp(a - amax)))

    r = minimize(g, np.zeros(K), method="BFGS", options={"gtol": 1e-12})
    return -r.fun


say("=" * 88)
say("N2  KL ball + moments: primal (SLSQP) vs dual (Christensen-Connault Prop. 2.1); rho -> inf")
worst_gap = 0.0
rows = []
for trial in range(12):
    n = int(rng.integers(8, 25))
    K = int(rng.integers(1, 3))
    mu0 = rng.dirichlet(np.ones(n))
    phi = rng.normal(size=(n, K))
    psi = rng.normal(size=n)
    mu_true = rng.dirichlet(np.ones(n) * 0.7)
    m = mu_true @ phi
    dstar = min_kl(mu0, phi, m)
    lp_hi = primal_range(phi, m, psi, +1)
    vals = []
    for mult in (1.5, 4.0):
        rho = dstar * mult + 0.05
        pv = kl_primal(mu0, phi, m, psi, rho)
        dv = kl_dual(mu0, phi, m, psi, rho)
        worst_gap = max(worst_gap, abs(pv - dv))
        vals.append((rho, pv, dv))
    d_big = kl_dual(mu0, phi, m, psi, 60.0)
    rows.append((n, K, dstar, vals, d_big, lp_hi))
say(f"   12 instances x 2 radii: max |primal - dual| = {worst_gap:.2e}")
say("   n  K  D*=minKL   [rho, primal, dual] x2                         dual(rho=60)  prior-free LP")
for (n, K, dstar, vals, d_big, lp_hi) in rows[:6]:
    s = "   ".join(f"[{r:.3f}, {p:.5f}, {d:.5f}]" for r, p, d in vals)
    say(f"   {n:2d} {K}  {dstar:.4f}   {s}   {d_big:.5f}      {lp_hi:.5f}")
say("   (dual at rho=60 approaches the LP value from below; the LP value has the hard-max dual)")

# ---------------------------------------------------------------------------------------
# N3  the Q2 sketch: code-based Gibbs measures with uniform <=k marginals
# ---------------------------------------------------------------------------------------


def span(gens, n):
    words = set()
    for coeffs in itertools.product([0, 1], repeat=len(gens)):
        w = 0
        for c, g in zip(coeffs, gens):
            if c:
                w ^= g
        words.add(w)
    return sorted(words)


def dual_distance(code, n):
    """minimum weight of a nonzero vector orthogonal to every codeword (brute force)."""
    best = n + 1
    for v in range(1, 1 << n):
        wt = bin(v).count("1")
        if wt >= best:
            continue
        if all(bin(v & c).count("1") % 2 == 0 for c in code):
            best = wt
    return best


def dist_to_code(code, n):
    """Hamming distance of every x in {0,1}^n to the code (multi-source BFS)."""
    dist = np.full(1 << n, -1, dtype=np.int16)
    frontier = np.array(code, dtype=np.int64)
    dist[frontier] = 0
    d = 0
    while frontier.size:
        d += 1
        nxt = []
        for i in range(n):
            y = frontier ^ (1 << i)
            y = y[dist[y] < 0]
            if y.size:
                y = np.unique(y)
                dist[y] = d
                nxt.append(y)
        frontier = np.unique(np.concatenate(nxt)) if nxt else np.array([], dtype=np.int64)
    return dist


def marginal_dev(p, n, k):
    """max over |S| = k of the sup-distance of the S-marginal from uniform."""
    xs = np.arange(1 << n)
    bits = ((xs[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
    worst = 0.0
    for S in itertools.combinations(range(n), k):
        idx = np.zeros(1 << n, dtype=np.int64)
        for j, s in enumerate(S):
            idx |= bits[:, s].astype(np.int64) << j
        marg = np.bincount(idx, weights=p, minlength=1 << k)
        worst = max(worst, float(np.max(np.abs(marg - 2.0 ** (-k)))))
    return worst


def h2(q):
    return float(-q * np.log(q) - (1 - q) * np.log(1 - q))


def rm1(mm):
    """generators of the first-order Reed-Muller code RM(1,mm), length 2^mm."""
    n = 1 << mm
    gens = [(1 << n) - 1]
    for j in range(mm):
        g = 0
        for pos in range(n):
            if (pos >> j) & 1:
                g |= 1 << pos
        gens.append(g)
    return gens, n


def simplex(mm):
    """generators of the simplex code, length 2^mm - 1 (dual of Hamming)."""
    n = (1 << mm) - 1
    gens = []
    for j in range(mm):
        g = 0
        for pos in range(1, n + 1):
            if (pos >> j) & 1:
                g |= 1 << (pos - 1)
        gens.append(g)
    return gens, n


say("=" * 88)
say("N3  mu ~ exp(-u*dist(x,C)): marginals and entropy (u = beta*c; natural logarithms)")
say("    code            n  |C|  dual-dist   max dev of k-marginals from uniform (k=1,2,3,4)      "
    "u    H/n     class bound h(1/(1+e^u))   ln2")
for name, (gens, n) in [("simplex[7,3]", simplex(3)), ("RM(1,3)[8,4]", rm1(3)),
                        ("simplex[15,4]", simplex(4)), ("RM(1,4)[16,5]", rm1(4))]:
    code = span(gens, n)
    dd = dual_distance(code, n) if n <= 16 else -1
    dist = dist_to_code(code, n).astype(float)
    for u in (1.0, 2.0, 4.0):
        w = np.exp(-u * dist)
        p = w / w.sum()
        H = float(-(p * np.log(p)).sum())
        devs = [marginal_dev(p, n, k) for k in (1, 2, 3, 4)] if u == 2.0 else None
        # single-site bounded differences of the energy: |dist(x) - dist(x^e_i)| <= 1
        if u == 2.0:
            xs = np.arange(1 << n)
            lip = max(float(np.max(np.abs(dist - dist[xs ^ (1 << i)]))) for i in range(n))
            assert lip <= 1.0
            say(f"    {name:14s} {n:2d} {len(code):3d}    {dd}       "
                + "  ".join(f"{d:.1e}" for d in devs)
                + f"            {u:.0f}   {H / n:.4f}   {h2(1 / (1 + np.exp(u))):.4f}"
                + f"                     {np.log(2):.4f}")
        else:
            say(f"    {name:14s} {n:2d} {len(code):3d}    {dd}       "
                + " " * 44 + f"            {u:.0f}   {H / n:.4f}   {h2(1 / (1 + np.exp(u))):.4f}")
        # class lower bound sum_i H(X_i | X_-i) >= n h(1/(1+e^u)) must hold
        assert H / n >= h2(1 / (1 + np.exp(u))) - 1e-12
say("    (k-marginals are uniform to rounding exactly for k < dual distance, and not beyond;")
say("     H/n lies strictly between the class bound and ln 2 at these small n; the excess over the")
say("     class bound is the finite-size cost  (ln|C| + overlap of the wells)/n .)")

# ---------------------------------------------------------------------------------------
# N4  envelope cone + moment constraints as an LP in the weights
# ---------------------------------------------------------------------------------------
say("=" * 88)
say("N4  identified sets of E_mu[psi]: prior-free moments | envelope cone + moments | cone only")
for trial in range(4):
    n = 14
    K = 2
    beta = 1.0
    pts = rng.normal(size=(n, 2))
    dmat = 0.6 * np.abs(pts[:, None, :] - pts[None, :, :]).sum(axis=2)   # a metric (weighted l1)
    mu0 = rng.dirichlet(np.ones(n) * 2.0)
    phi = rng.normal(size=(n, K))
    psi = rng.normal(size=n)
    # a "true" ensemble inside the class: w = exp(-beta g), g Lipschitz for dmat
    g = np.min(dmat[:, rng.choice(n, 3, replace=False)], axis=1) * rng.uniform(0.2, 0.9)
    w_true = np.exp(-beta * g)
    mu_true = mu0 * w_true / np.sum(mu0 * w_true)
    m = mu_true @ phi
    # cone constraints  w(y) - exp(beta d(x,y)) w(x) <= 0
    rows_, rhs = [], []
    for x in range(n):
        for y in range(n):
            if x != y:
                r = np.zeros(n)
                r[y] = 1.0
                r[x] = -np.exp(beta * dmat[x, y])
                rows_.append(r)
                rhs.append(0.0)
    A_ub = np.array(rows_)
    b_ub = np.array(rhs)

    def cone_range(with_moments):
        A_eq = [mu0]
        b_eq = [1.0]
        if with_moments:
            for k in range(K):
                A_eq.append(mu0 * phi[:, k])
                b_eq.append(m[k])
        out = []
        for sense in (+1, -1):
            r = linprog(-sense * mu0 * psi, A_ub=A_ub, b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq,
                        bounds=[(0, None)] * n, method="highs")
            assert r.status == 0, r.message
            out.append(sense * (-r.fun))
        return out[1], out[0]

    free = (primal_range(phi, m, psi, -1), primal_range(phi, m, psi, +1))
    cm = cone_range(True)
    co = cone_range(False)
    truth = float(mu_true @ psi)
    assert free[0] - 1e-9 <= cm[0] <= truth + 1e-9 and truth - 1e-9 <= cm[1] <= free[1] + 1e-9
    assert co[0] - 1e-9 <= cm[0] and cm[1] <= co[1] + 1e-9
    say(f"   truth {truth:+.4f} | moments only [{free[0]:+.4f}, {free[1]:+.4f}] | "
        f"cone+moments [{cm[0]:+.4f}, {cm[1]:+.4f}] | cone only [{co[0]:+.4f}, {co[1]:+.4f}]")
say("   (cone+moments is nested in both, as it must be; it is one LP per end, no Charnes-Cooper")
say("    transformation is needed once the normalisation is written as a linear equality in w.)")

with open(__file__.replace(".py", ".out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
