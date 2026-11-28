#!/usr/bin/env python3
"""p2_bridge.py -- falsification checks for docs/phase2/BRIDGE_NOTE.md (Phase II; relations with the
certified-MBAR division).

Cube {0,1}^n, uniform reference pi, admissible weights (w(x) <= e^{u d(x,y)} w(y)), A = E_pi w,
mu = w pi / A, g = w / A.  Notation of docs/phase2/PHASE2_REPORT.md section 1:
    m_r = 2^{-n} sum_{j<r} C(n,j) (e^{u(r-j)} - 1),   V(n,k) = sum_{j<=k} C(n,j).

Checks (each prints PASS/FAIL; exit code 1 if any fails):
  B1  Theorem F on members of the class (exact enumeration, n <= 12):
          Omega_s(w) := E_pi min(g, s) >= min(1/2, s (V(n, r_s) + 1) / 2^n),  r_s = max{r : s m_{r+1} <= 1/2}
      and the tail inequality behind it, E (g - s)_+ <= s m_{r+1} whenever |{g > s}| <= V(n, r).
  B2  the bound is attained up to a polynomial factor (cones and dips), and the exponents at large n:
      -(1/n) ln[bound] -> KL(rho_s || p_u) on the whole trade-off curve; Omega_1(cone) <= 2 e^{-nh}.
  B3  the bridge identity  A = E_pi[min(w, theta)] / E_mu[min(1, theta / w)]  for every theta, and the
      two-state MBAR conductance  l = s0 s1 int p0 p1 / (s0 p0 + s1 p1):  l(1/2,1/2) = (1 - Delta/2)/4
      (Delta the triangular discrimination),  Omega/4 <= l <= Omega/2.
  B4  the bridge estimator of Corollary F1 by simulation (exact sampling of mu by enumeration, n = 14):
      error rates at N = c / (eps^2 Omega) for several c, on cones, dips, maxima of dips, random members.
  B5  Proposition F3:  TV(mu_0, mu_1) >= mu_0(D^c) (1 - A_0/A_1)  for pairs that agree off D.
  B6  Proposition F2 (sampling): the counting identity  P_c(x in B(c, r-1)) = V(n, r-1)/2^n  and the
      numbers  (m_r/(1+m_r) - kappa) 2^n / V(n, r-1) - 1  at large n (exponent -> h).
  B7  Theorem J (observables of the energy): a dip at c against dips at c and at its antipode (disjoint
      balls): A0 = 1 + m_r, A1 = 1 + 2 m_r, and the laws of the weight under the two ensembles are at total
      variation distance (m_r + v)/((1 + m_r)(1 + 2 m_r)) <= 1/(1 + 2 m_r), v = V(n, r-1)/2^n (exact
      enumeration); exponents theta_hint(gamma) <= theta_na(gamma), both zero at gamma = ln cosh(u/2).
  B8  the MBAR division's Theorem A1 in its dual (Cramer-Rao) form, on random finite instances:
          c^T L(s)^+ c - sum_k c_k^2 / s_k  =  b^T M(s)^+ b,    b = sum_k c_k p_k,  M(s) = sum_k s_k (diag p_k - p_k p_k^T),
      their gradient formula dV/ds_k = -Var_k(z), convexity along random segments; and a search for a
      failure of convexity of the correlated-sample variance  sum_k C_k s_k Var_k(z_s)  (lazy chains).
  B9  the instance found by B8c, simulated: MBAR on raw samples of lazy chains (occupation counts of the
      chains, Newton solution of the MBAR equations, 1000 replicates per allocation) against the formula,
      and the convex alternative with effective counts s_k / C_k.
"""
import math
import sys
import itertools
import numpy as np

rng = np.random.default_rng(20261128)
FAILS = []


def report(name, ok, info=""):
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, info), flush=True)
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- exact small-n machinery
def cube(n):
    X = np.arange(2 ** n, dtype=np.int64)
    wt = np.zeros(2 ** n, dtype=np.int64)
    for i in range(n):
        wt += (X >> i) & 1
    return X, wt


def popcount(a):
    a = a.copy()
    c = np.zeros_like(a)
    while a.any():
        c += a & 1
        a >>= 1
    return c


def m_exact(n, u, r):
    return sum(math.comb(n, j) * (math.exp(u * (r - j)) - 1.0) for j in range(r)) / 2.0 ** n


def V(n, k):
    return sum(math.comb(n, j) for j in range(0, k + 1)) if k >= 0 else 0


def r_of_s(n, u, s):
    """r_s = max{ r in {0..n-1} : s m_{r+1} <= 1/2 }, or -1."""
    r = -1
    while r + 1 <= n - 1 and s * m_exact(n, u, r + 2) <= 0.5:
        r += 1
    return r


def bound_F(n, u, s):
    r = r_of_s(n, u, s)
    return min(0.5, s * (V(n, r) + 1) / 2.0 ** n)


def regularise(F, n, u, X):
    """largest u-Lipschitz minorant of F (ln w): F(x) = min_y F(y) + u d(x,y), by n rounds of relaxation."""
    F = F.copy()
    for _ in range(n):
        for i in range(n):
            F = np.minimum(F, F[X ^ (1 << i)] + u)
    return F


def members(n, u, X, how_many):
    """a list of (name, w) of admissible weights on the n-cube."""
    out = []
    d0 = popcount(X)
    out.append(("cone", np.exp(-u * d0)))
    for r in range(1, n):
        out.append(("dip r=%d" % r, np.maximum(1.0, np.exp(u * (r - d0)))))
    for _ in range(how_many):
        kind = rng.integers(0, 5)
        if kind == 0:      # maximum of dips at random centres, random radii
            k = int(rng.integers(2, 9))
            w = np.ones(2 ** n)
            for _j in range(k):
                c = int(rng.integers(0, 2 ** n))
                r = int(rng.integers(1, n))
                w = np.maximum(w, np.exp(u * (r - popcount(X ^ c))))
            out.append(("max of %d dips" % k, w))
        elif kind == 1:    # maximum of cones with random heights
            k = int(rng.integers(2, 12))
            lw = np.full(2 ** n, -np.inf)
            for _j in range(k):
                c = int(rng.integers(0, 2 ** n))
                a = rng.uniform(-u * n / 2, u * n / 2)
                lw = np.maximum(lw, a - u * popcount(X ^ c))
            out.append(("max of %d cones" % k, np.exp(lw - lw.max())))
        elif kind == 2:    # product weight with site slopes in [-u, u]
            ui = rng.uniform(-u, u, size=n)
            lw = np.zeros(2 ** n)
            for i in range(n):
                lw += ui[i] * ((X >> i) & 1)
            out.append(("product", np.exp(lw - lw.max())))
        elif kind == 3:    # random energy, regularised to slope u
            F = rng.normal(0, rng.uniform(0.5, 3.0) * u * math.sqrt(n), size=2 ** n)
            F = regularise(F, n, u, X)
            out.append(("regularised random", np.exp(-(F - F.min()))))
        else:              # sum of two members (the class is a convex cone)
            c1, c2 = int(rng.integers(0, 2 ** n)), int(rng.integers(0, 2 ** n))
            w = np.exp(-u * popcount(X ^ c1)) + rng.uniform(0.01, 100) * np.maximum(
                np.exp(-u * n), np.exp(-u * popcount(X ^ c2)) * rng.uniform(0.1, 10))
            out.append(("sum", w))
    return out


def is_admissible(w, n, u, X):
    lw = np.log(w)
    for i in range(n):
        if np.max(np.abs(lw - lw[X ^ (1 << i)])) > u + 1e-9:
            return False
    return True


# ---------------------------------------------------------------- B1
def check_B1():
    worst_ratio, worst_tail, count, bad_members = np.inf, -np.inf, 0, 0
    worst_info = ""
    for (n, u, how_many) in [(8, 1.0, 60), (10, 1.0, 40), (10, 0.5, 30), (10, 2.0, 30), (12, 1.0, 16), (12, 0.3, 10)]:
        X, _ = cube(n)
        for name, w in members(n, u, X, how_many):
            if not is_admissible(w, n, u, X):
                bad_members += 1
                continue
            A = w.mean()
            g = w / A
            sgrid = np.exp(np.linspace(math.log(g.min()) - 1.0, math.log(g.max()) + 1.0, 41))
            sgrid = np.concatenate([sgrid, [1.0, 0.5, 2.0]])
            for s in sgrid:
                om = np.minimum(g, s).mean()
                b = bound_F(n, u, s)
                count += 1
                if om / b < worst_ratio:
                    worst_ratio = om / b
                    worst_info = "n=%d u=%g %s s=%.3g Omega=%.4g bound=%.4g" % (n, u, name, s, om, b)
                # the tail inequality: E (g - s)_+ <= s m_{r+1} whenever |{g > s}| <= V(n, r), every such r <= n-1
                D = int((g > s).sum())
                if 0 < D < 2 ** n:
                    r = 0
                    while V(n, r) < D:
                        r += 1
                    if r <= n - 1:
                        exc = np.maximum(g - s, 0).mean() - s * m_exact(n, u, r + 1)
                        worst_tail = max(worst_tail, exc / max(s, 1e-300))
    report("B1a Theorem F: Omega_s >= min(1/2, s (V(n,r_s)+1)/2^n)", worst_ratio >= 1 - 1e-12 and bad_members == 0,
           "| %d (member, s) pairs; least Omega/bound = %.4f at %s" % (count, worst_ratio, worst_info))
    report("B1b tail inequality (Lemma 11.43(b)): E(g-s)_+ <= s m_{r+1}", worst_tail <= 1e-12,
           "| largest [E(g-s)_+ - s m_{r+1}]/s = %.3g" % worst_tail)


# ---------------------------------------------------------------- B2
def lgC(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def logsumexp(v):
    v = np.asarray(v, dtype=float)
    mx = v.max()
    return mx + math.log(np.exp(v - mx).sum())


_LGC = {}


def lgC_all(n):
    """ln C(n, j), j = 0..n."""
    if n not in _LGC:
        lg = np.array([math.lgamma(k + 1) for k in range(n + 1)])
        _LGC[n] = lg[n] - lg - lg[::-1]
    return _LGC[n]


_LM = {}


def log_m_all(n, u, rmax):
    """ln m_r for r = 1..rmax (log-space; index r-1)."""
    key = (n, u, rmax)
    if key not in _LM:
        lc = lgC_all(n)
        out = np.empty(rmax)
        for r in range(1, rmax + 1):
            x = u * (r - np.arange(0, r))
            out[r - 1] = logsumexp(lc[:r] + x + np.log1p(-np.exp(-x))) - n * math.log(2)
        _LM[key] = out
    return _LM[key]


def log_m_big(n, u, r):
    return log_m_all(n, u, n // 2 + 1)[r - 1]


def log_V_big(n, k):
    return logsumexp(lgC_all(n)[:k + 1])


def KL(a, b):
    return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))


def check_B2():
    ok = True
    lines = []
    for u in (0.5, 1.0, 2.0):
        pu = 1 / (1 + math.exp(u))
        a = KL(pu, 0.5)
        rho0 = math.log(2 / (1 + math.exp(-u))) / u
        h = KL(rho0, 0.5)
        estar = math.log(math.cosh(u / 2))
        # consistency of the constants
        ok &= abs(KL(rho0, pu) - h) < 1e-12 and abs(rho0 - (pu + a / u)) < 1e-12 and abs(KL(0.5, pu) - estar) < 1e-12
        for n in (2000, 20000):
            lm = log_m_all(n, u, n // 2 + 1)                                    # lm[r-1] = ln m_r
            for sigma in (0.5 * a, 0.0, -0.5 * estar):                           # s = e^{sigma n}
                ls = sigma * n
                # r_s = max{r : ln s + ln m_{r+1} <= ln(1/2)}
                idx = np.nonzero(ls + lm <= math.log(0.5))[0]
                r_s = int(idx.max())          # lm index r_s  <->  m_{r_s+1}
                lb = min(math.log(0.5), ls + log_V_big(n, r_s) - n * math.log(2))
                rho = rho0 - sigma / u
                lines.append("    u=%g n=%d sigma=%+.4f: r_s/n=%.4f (rho_s=%.4f)  -(1/n)ln bound=%.5f  KL(rho_s||p_u)=%.5f  KL(rho_s||1/2)=%.5f"
                             % (u, n, sigma, r_s / n, rho, -lb / n, KL(rho, pu), KL(rho, 0.5)))
                tol = 6 * math.log(n) / n
                ok &= abs(-lb / n - KL(rho, pu)) < tol
            # the cone at s = 1: Omega = pi(|x| <= k) + mu(|x| > k), {g >= 1} = {|x| <= k}, k = floor(rho0 n)
            k = int(math.floor(rho0 * n + 1e-12))
            lpi = log_V_big(n, k) - n * math.log(2)
            j = np.arange(k + 1, n + 1)
            lmu = logsumexp(lgC_all(n)[k + 1:] - u * j) - n * math.log(1 + math.exp(-u))
            lom = logsumexp([lpi, lmu])
            lines.append("    u=%g n=%d cone: -(1/n) ln Omega_1 = %.5f  (h = %.5f;  Omega_1 <= 2 e^{-nh}: %s)"
                         % (u, n, -lom / n, h, lom <= math.log(2) - n * h + 1e-9))
            ok &= lom <= math.log(2) - n * h + 1e-9 and abs(-lom / n - h) < 4 * math.log(n) / n
    # small n: ratio Omega/bound at the cone and at dips is polynomial
    rat = []
    for n in (8, 10, 12, 14):
        X, _ = cube(n)
        d0 = popcount(X)
        u = 1.0
        w = np.exp(-u * d0)
        g = w / w.mean()
        rat.append(np.minimum(g, 1).mean() / bound_F(n, u, 1.0))
    lines.append("    Omega_1(cone)/bound at n = 8, 10, 12, 14 (u = 1): " + ", ".join("%.2f" % x for x in rat))
    report("B2 exponents of the bound; the cone attains them", ok, "\n" + "\n".join(lines))


# ---------------------------------------------------------------- B3
def check_B3():
    ok, worst = True, 0.0
    n, u = 10, 1.0
    X, _ = cube(n)
    for name, w in members(n, u, X, 25):
        A = w.mean()
        mu = w / w.sum()
        for theta in A * np.exp(rng.uniform(-6, 6, size=6)):
            num = np.minimum(w, theta).mean()
            den = (mu * np.minimum(1.0, theta / w)).sum()
            worst = max(worst, abs(num / den / A - 1))
        # two-state conductance at s = 1/2: p0 = pi, p1 = mu (probability vectors)
        p0 = np.full(2 ** n, 2.0 ** -n)
        p1 = mu
        ell = 0.25 * (p0 * p1 / (0.5 * p0 + 0.5 * p1)).sum()
        Delta = ((p0 - p1) ** 2 / (p0 + p1)).sum()
        Om = np.minimum(p0, p1).sum()
        ok &= abs(ell - 0.25 * (1 - Delta / 2)) < 1e-12 and Om / 4 - 1e-15 <= ell <= Om / 2 + 1e-15
        for s0 in (0.1, 0.37, 0.9):
            s1 = 1 - s0
            ell_s = s0 * s1 * (p0 * p1 / (s0 * p0 + s1 * p1)).sum()
            Oms = np.minimum(s0 * p0, s1 * p1).sum()
            ok &= Oms / 2 - 1e-15 <= ell_s <= Oms + 1e-15
    report("B3 bridge identity; conductance = (1 - Delta/2)/4, Omega/4 <= l <= Omega/2, min/2 <= l(s) <= min", ok and worst < 1e-10,
           "| largest relative error of the identity %.2g" % worst)


# ---------------------------------------------------------------- B4
def bridge_estimate(w, X0, Y, w0, n, u, K0):
    """the estimator of Corollary F1.  X0: indices of uniform points, Y: indices of ensemble samples."""
    wx, wy = w[X0], w[Y]
    N0, N1 = len(X0), len(Y)
    best, out = -1.0, None
    for k in range(-K0, K0 + 1):
        th = w0 * math.exp(k)
        sa = np.minimum(wx / th, 1.0).sum()
        sb = np.minimum(1.0, th / wy).sum()
        if min(sa, sb) > best:
            best, out = min(sa, sb), math.log(th) + math.log(sa / N0) - math.log(sb / N1)
    return out


def check_B4():
    eps = 0.5
    reps = 300
    lines, ok = [], True
    for (n, u) in [(14, 1.0), (16, 4.0), (18, 6.0)]:
        X, _ = cube(n)
        d0 = popcount(X)
        rho0 = math.log(2 / (1 + math.exp(-u))) / u
        r0 = max(1, int(round(rho0 * n)))
        inst = [("cone", np.exp(-u * d0)),
                ("dip r=%d" % (r0 + 1), np.maximum(1.0, np.exp(u * (r0 + 1 - d0)))),
                ("dip r=%d" % (r0 + 3), np.maximum(1.0, np.exp(u * (r0 + 3 - d0))))]
        w = np.ones(2 ** n)
        for _ in range(40):
            w = np.maximum(w, np.exp(u * (r0 - popcount(X ^ int(rng.integers(0, 2 ** n))))))
        inst.append(("max of 40 dips r=%d" % r0, w))
        if n <= 16:
            F = regularise(rng.normal(0, 2.0 * u * math.sqrt(n), size=2 ** n), n, u, X)
            inst.append(("regularised random", np.exp(-(F - F.min()))))
        K0 = int(math.ceil(u * n)) + 1
        for name, w in inst:
            A = w.mean()
            g = w / A
            Om = np.minimum(g, 1).mean()
            mu = w / w.sum()
            cdf = np.cumsum(mu)
            cdf /= cdf[-1]
            row = []
            for cfac in (0.3, 3.0, 30.0, 300.0):
                N = max(2, int(math.ceil(cfac / (eps ** 2 * Om))))
                if N > 300000:
                    continue
                nrep = reps if N < 100000 else 60
                bad = 0
                for _ in range(nrep):
                    X0 = rng.integers(0, 2 ** n, size=N)
                    Y = np.minimum(np.searchsorted(cdf, rng.random(N)), 2 ** n - 1)
                    est = bridge_estimate(w, X0, Y, w[0], n, u, K0)
                    bad += abs(est - math.log(A)) > eps
                row.append((cfac, N, bad / nrep))
            lines.append("    n=%d u=%g %-20s Omega=%.5f bound=%.5f | " % (n, u, name, Om, bound_F(n, u, 1.0)) +
                         "; ".join("c=%g: N=%d err %.3f" % t for t in row))
            ok &= all(e <= 0.02 for (cf, N_, e) in row if cf >= 30) and all(e <= 0.30 for (cf, N_, e) in row if cf == 3.0)
    # the sufficient sample size of Corollary F1 (its constant), on the cone at n = 14, u = 1
    n, u, delta = 14, 1.0, 0.1
    X, _ = cube(n)
    w = np.exp(-u * popcount(X))
    K0 = int(math.ceil(u * n)) + 1
    Lam = 54 * math.e * math.log(4 * (2 * K0 + 1) / delta) / eps ** 2
    Nthm = int(math.ceil(max(2 * Lam, Lam / bound_F(n, u, 1.0))))
    A, mu = w.mean(), w / w.sum()
    bad = 0
    for _ in range(40):
        est = bridge_estimate(w, rng.integers(0, 2 ** n, size=Nthm), rng.choice(2 ** n, size=Nthm, p=mu), w[0], n, u, K0)
        bad += abs(est - math.log(A)) > eps
    lines.append("    Corollary F1's sample size at n=14, u=1, eps=0.5, delta=0.1: N0 = N1 = %d; errors on the cone in 40 runs: %d" % (Nthm, bad))
    ok &= bad == 0
    report("B4 bridge estimator: error rate small at N = 300/(eps^2 Omega) (failures at N = 0.3/(eps^2 Omega) are expected)", ok,
           "\n" + "\n".join(lines))


# ---------------------------------------------------------------- B5
def check_B5():
    n, u = 10, 1.0
    X, _ = cube(n)
    worst, cnt = np.inf, 0
    for name, w0 in members(n, u, X, 30):
        for _ in range(4):
            c = int(rng.integers(0, 2 ** n))
            r = int(rng.integers(1, n))
            lift = rng.uniform(0.5, 4.0) * w0[c]
            w1 = np.maximum(w0, lift * np.exp(u * (r - popcount(X ^ c))))
            D = w1 != w0
            if not D.any():
                continue
            A0, A1 = w0.mean(), w1.mean()
            mu0, mu1 = w0 / w0.sum(), w1 / w1.sum()
            tv = 0.5 * np.abs(mu0 - mu1).sum()
            lb = mu0[~D].sum() * (1 - A0 / A1)
            worst = min(worst, tv - lb)
            cnt += 1
    report("B5 Proposition F3: TV(mu0, mu1) >= mu0(D^c)(1 - A0/A1)", worst >= -1e-12, "| %d pairs, least TV - bound = %.3g" % (cnt, worst))


# ---------------------------------------------------------------- B6
def check_B6():
    ok = True
    n = 10
    X, _ = cube(n)
    for r in (1, 3, 5):
        x = int(rng.integers(0, 2 ** n))
        cnt = int((popcount(X ^ x) <= r - 1).sum())
        ok &= cnt == V(n, r - 1)
    lines = []
    for u in (0.5, 1.0, 2.0):
        rho0 = math.log(2 / (1 + math.exp(-u))) / u
        h = KL(rho0, 0.5)
        for n in (2000, 20000):
            lm = log_m_all(n, u, n // 2 + 1)
            r = int(np.nonzero(lm >= math.log(3.0))[0].min()) + 1          # least r with m_r >= 3
            lnum = math.log(0.5) + n * math.log(2) - log_V_big(n, r - 1)    # (3/4 - 1/4) 2^n / V
            lines.append("    u=%g n=%d: least r with m_r >= 3: r/n=%.4f; (1/n) ln[(1/2) 2^n/V(n,r-1)] = %.5f (h = %.5f)"
                         % (u, n, r / n, lnum / n, h))
            ok &= abs(lnum / n - h) < 6 * math.log(n) / n
    report("B6 Proposition F2 (sampling needs e^{nh} evaluations): counting identity and exponents", ok, "\n" + "\n".join(lines))


# ---------------------------------------------------------------- B7
def check_B7():
    ok = True
    lines = []
    # the pair of Theorem J: one dip at c against dips at c and at its antipode (disjoint balls when 2(r-1) < n).
    # Law of the weight under the ensemble: exact enumeration; claim: TV = |(1-v)/(1+m) - (1-2v)/(1+2m)| <= 1/(1+m).
    for (n, u, radii) in [(12, 1.0, (3, 5, 6)), (14, 2.0, (3, 5, 7)), (16, 4.0, (2, 4, 6))]:
        X, _ = cube(n)
        d0 = popcount(X)
        dbar = n - d0                                  # distance to the antipode of 0
        for r in radii:
            assert 2 * (r - 1) < n
            mr, v = m_exact(n, u, r), V(n, r - 1) / 2.0 ** n
            w0 = np.maximum(1.0, np.exp(u * (r - d0)))
            w1 = np.maximum(w0, np.exp(u * (r - dbar)))
            A0, A1 = w0.mean(), w1.mean()
            k0 = np.rint(np.log(w0) / u).astype(int)
            k1 = np.rint(np.log(w1) / u).astype(int)
            L0 = np.bincount(k0, weights=w0 / w0.sum(), minlength=r + 1)
            L1 = np.bincount(k1, weights=w1 / w1.sum(), minlength=r + 1)
            tv = 0.5 * np.abs(L0 - L1).sum()
            pred = abs((1 - v) / (1 + mr) - (1 - 2 * v) / (1 + 2 * mr))
            lines.append("    n=%d u=%g r=%d: m_r=%.4g v=%.4g | A1/A0=%.4f (=(1+2m)/(1+m): %s) | TV(energy laws)=%.6g, formula %.6g, 1/(1+m_r)=%.6g"
                         % (n, u, r, mr, v, A1 / A0, abs(A1 / A0 - (1 + 2 * mr) / (1 + mr)) < 1e-12, tv, pred, 1 / (1 + mr)))
            ok &= abs(tv - pred) < 1e-12 and tv <= 1 / (1 + mr) + 1e-15 and abs(A0 - (1 + mr)) < 1e-9 * A0 and abs(A1 - (1 + 2 * mr)) < 1e-9 * A1
    for u in (0.5, 1.0, 2.0):
        pu = 1 / (1 + math.exp(u))
        rho0 = math.log(2 / (1 + math.exp(-u))) / u
        h, a, estar = KL(rho0, 0.5), KL(pu, 0.5), math.log(math.cosh(u / 2))
        row = []
        for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
            gam = frac * estar
            hint = KL(min(0.5, rho0 + gam / u), 0.5)
            # theta_na(gam) = KL(rho || 1/2) with KL(rho || p_u) = gam, rho in [p_u, 1/2]
            lo, hi = pu, 0.5
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if KL(mid, pu) < gam:
                    lo = mid
                else:
                    hi = mid
            na = KL(0.5 * (lo + hi), 0.5)
            row.append("gamma=%.4f: [%.5f, %.5f]" % (gam, hint, min(h, na)))
            ok &= hint <= min(h, na) + 1e-9
        ok &= abs(KL(min(0.5, rho0 + estar / u), 0.5)) < 1e-12 and abs(rho0 + estar / u - 0.5) < 1e-12
        # the balanced bridge when a sample costs e^{kappa n} evaluations: b(kappa) = KL(rho0 - kappa/u || 1/2)
        bal = lambda kap: KL(rho0 - kap / u, 0.5)
        grid = np.linspace(pu, 0.5, 20001)[1:-1]
        for kap in (0.0, 0.5 * h, h, 0.5 * a):
            brute = min(max(KL(r_, 0.5), KL(r_, pu) + kap) for r_ in grid)
            ok &= -1e-12 <= brute - bal(kap) < 2e-5          # the grid can only overshoot the minimum
        ok &= abs(bal(0.0) - h) < 1e-12 and abs(bal(a) - a) < 1e-12
        lines.append("    u=%g: balanced bridge b(kappa) = KL(rho0 - kappa/u || 1/2): b(0)=%.5f, b(h)=%.5f, b(a)=%.5f" % (u, bal(0.0), bal(h), bal(a)))
        lines.append("    u=%g: h=%.5f a=%.5f ln cosh(u/2)=%.5f; [theta_hint(gamma), min(h, theta_na(gamma))]: " % (u, h, a, estar) + "; ".join(row))
    report("B7 Theorem J: energy laws of one dip and two dips; exponents and the threshold ln cosh(u/2)", ok, "\n" + "\n".join(lines))


# ---------------------------------------------------------------- B8
def mbar_objects(P, s):
    """P: K x m matrix of probability vectors; s: positive weights.  Returns L(s), M(s)."""
    K, m = P.shape
    mix = s @ P
    Pi = (s[:, None] * P) / mix[None, :]                    # pi_k(x)
    L = np.diag(s) - (Pi * mix[None, :]) @ Pi.T             # int m (diag pi - pi pi^T)
    M = np.zeros((m, m))
    for k in range(K):
        M += s[k] * (np.diag(P[k]) - np.outer(P[k], P[k]))
    return L, M, Pi, mix


def V_primal(P, s, c):
    L, M, Pi, mix = mbar_objects(P, s)
    v = np.linalg.pinv(L, rcond=1e-12) @ c
    return float(c @ v - np.sum(c ** 2 / s)), v, Pi


def V_dual(P, s, c):
    L, M, Pi, mix = mbar_objects(P, s)
    b = c @ P
    return float(b @ np.linalg.pinv(M, rcond=1e-12) @ b)


def check_B8():
    worst_id, worst_grad, worst_cvx, worst_sum = 0.0, 0.0, np.inf, 0.0
    cnt = 0
    for trial in range(300):
        K = int(rng.integers(2, 6))
        m = int(rng.integers(K + 1, 14))
        P = rng.dirichlet(np.full(m, rng.uniform(0.2, 2.0)), size=K) + 1e-6
        P /= P.sum(axis=1, keepdims=True)
        s = rng.dirichlet(np.ones(K)) * rng.uniform(0.5, 3.0) + 0.02
        c = rng.normal(size=K)
        c -= c.mean()
        Vp, v, Pi = V_primal(P, s, c)
        Vd = V_dual(P, s, c)
        worst_id = max(worst_id, abs(Vp - Vd) / max(1e-12, abs(Vp)))
        z = v @ Pi
        var = np.array([P[k] @ z ** 2 - (P[k] @ z) ** 2 for k in range(K)])
        worst_sum = max(worst_sum, abs(float(s @ var) - Vp) / max(1e-12, abs(Vp)))
        eps_fd = 1e-6
        for k in range(K):
            sp = s.copy()
            sp[k] += eps_fd
            sm = s.copy()
            sm[k] -= eps_fd
            fd = (V_primal(P, sp, c)[0] - V_primal(P, sm, c)[0]) / (2 * eps_fd)
            worst_grad = max(worst_grad, abs(fd + var[k]) / max(1e-9, abs(var[k]) + abs(fd)))
        t = rng.dirichlet(np.ones(K)) * rng.uniform(0.5, 3.0) + 0.02
        mid = V_primal(P, 0.5 * (s + t), c)[0]
        worst_cvx = min(worst_cvx, 0.5 * (Vp + V_primal(P, t, c)[0]) - mid)
        cnt += 1
    report("B8a MBAR A1 in dual form: c^T L^+ c - sum c_k^2/s_k = b^T M(s)^+ b", worst_id < 1e-7,
           "| %d random instances (K = 2..5), largest relative difference %.2g; sum_k s_k Var_k(z) = V_c: %.2g" % (cnt, worst_id, worst_sum))
    report("B8b MBAR A2: dV/ds_k = -Var_k(z); midpoint convexity", worst_grad < 1e-4 and worst_cvx > -1e-9,
           "| largest relative gradient error %.2g (central differences); least midpoint gap %.3g" % (worst_grad, worst_cvx))

    # correlated samples: lazy chains P_k = lam_k I + (1 - lam_k) 1 p_k^T have long-run variance C_k Var_k, C_k = (1+lam_k)/(1-lam_k);
    # the variance of the MBAR estimate (i.i.d. weights, correlated data) is  F(s) = sum_k C_k s_k Var_k(z_s).
    def F_corr(P, s, c, C):
        Vp, v, Pi = V_primal(P, s, c)
        z = v @ Pi
        var = np.array([P[k] @ z ** 2 - (P[k] @ z) ** 2 for k in range(P.shape[0])])
        return float((C * s) @ var)

    best = (0.0, None)
    for trial in range(4000):
        K = int(rng.integers(2, 4))
        m = int(rng.integers(K + 1, 8))
        P = rng.dirichlet(np.full(m, rng.uniform(0.1, 1.5)), size=K) + 1e-6
        P /= P.sum(axis=1, keepdims=True)
        c = np.zeros(K)
        c[0], c[1] = -1.0, 1.0
        C = np.exp(rng.uniform(0, math.log(200.0), size=K))
        s = rng.dirichlet(np.ones(K))
        t = rng.dirichlet(np.ones(K))
        s, t = 0.02 + 0.94 * s, 0.02 + 0.94 * t
        gap = 0.5 * (F_corr(P, s, c, C) + F_corr(P, t, c, C)) - F_corr(P, 0.5 * (s + t), c, C)
        rel = gap / max(1e-300, F_corr(P, 0.5 * (s + t), c, C))
        if rel < best[0]:
            best = (rel, (K, m, P.copy(), C.copy(), s.copy(), t.copy()))
    if best[1] is None:
        print("INFO B8c no failure of midpoint convexity of the correlated-sample variance found in 4000 random instances")
    else:
        K, m, P, C, s, t = best[1]
        c = np.zeros(K)
        c[0], c[1] = -1.0, 1.0
        print("INFO B8c the correlated-sample variance sum_k C_k s_k Var_k(z_s) is NOT convex in s: midpoint gap / value = %.4f" % best[0])
        print("     instance: K=%d, support %d, C=%s" % (K, m, np.array2string(C, precision=3)))
        print("     P=%s" % np.array2string(P, precision=4, separator=", ").replace("\n", " "))
        print("     s=%s  t=%s" % (np.array2string(s, precision=4), np.array2string(t, precision=4)))
        print("     F(s)=%.6g F(t)=%.6g F((s+t)/2)=%.6g" % (F_corr(P, s, c, C), F_corr(P, t, c, C), F_corr(P, 0.5 * (s + t), c, C)))
    return best


# ---------------------------------------------------------------- B9
def lazy_counts(p, lam, nlen, m):
    """occupation counts of a stationary lazy chain X_{t+1} = X_t w.p. lam, else a fresh draw from p.

    The chain is a sequence of fresh draws with independent geometric holding times; the draws are independent
    of the holding times, so the holding times of the complete visits are split among the states by a
    multinomial vector, and the last (truncated) visit gets a state of its own draw."""
    if lam <= 0:
        return rng.multinomial(nlen, p).astype(float)
    J = int(nlen * (1 - lam) * 1.3) + 200
    while True:
        hold = rng.geometric(1 - lam, size=J)
        cs = np.cumsum(hold)
        if cs[-1] >= nlen:
            break
        J *= 2
    last = int(np.searchsorted(cs, nlen))            # visits 0..last-1 are complete, visit `last` is truncated
    counts = np.zeros(m)
    if last > 0:
        parts = rng.multinomial(last, p)
        edges = np.concatenate([[0], np.cumsum(parts)])
        csum = np.concatenate([[0], cs[:last]])
        counts += csum[edges[1:]] - csum[edges[:-1]]
    counts[rng.choice(m, p=p)] += nlen - (cs[last - 1] if last > 0 else 0)
    return counts


def mbar_solve(P, frac, counts):
    """the MBAR estimate for unnormalised densities q_k = p_k (so f* = 0), pooled counts, sample fractions frac."""
    K = P.shape[0]
    N = counts.sum()
    f = np.zeros(K)
    for _ in range(60):
        E = frac[:, None] * np.exp(f)[:, None] * P
        Pi = E / E.sum(axis=0, keepdims=True)
        g = (Pi * counts[None, :]).sum(axis=1) / N - frac
        H = np.diag((Pi * counts[None, :]).sum(axis=1) / N) - (Pi * counts[None, :]) @ Pi.T / N
        step = np.linalg.pinv(H, rcond=1e-12) @ g
        f = f - step
        f -= f.mean()
        if np.abs(step).max() < 1e-13:
            break
    return f


def check_B9():
    # the instance found by B8c, rounded to four digits and re-evaluated
    P = np.array([[0.0344, 0.8010, 0.1182, 0.0463], [0.4817, 0.3260, 0.1709, 0.0215], [0.2941, 0.0319, 0.2172, 0.4568]])
    P /= P.sum(axis=1, keepdims=True)
    C = np.array([1.706, 135.105, 1.053])
    lam = (C - 1) / (C + 1)
    c = np.array([-1.0, 1.0, 0.0])
    s = np.array([0.2047, 0.0295, 0.7658])
    t = np.array([0.2387, 0.6463, 0.1149])
    s, t = s / s.sum(), t / t.sum()
    N, reps = 600000, 1000
    lines, ok, vals = [], True, []
    for name, alloc in (("s", s), ("(s+t)/2", 0.5 * (s + t)), ("t", t)):
        Vp, v, Pi = V_primal(P, alloc, c)
        z = v @ Pi
        var = np.array([P[k] @ z ** 2 - (P[k] @ z) ** 2 for k in range(3)])
        F_formula = float((C * alloc) @ var)
        nk = np.maximum(1, np.rint(alloc * N).astype(int))
        frac = nk / nk.sum()
        est = np.empty(reps)
        est_w = np.empty(reps)
        fw = frac / C
        fw = fw / fw.sum()                      # effective fractions s_k / C_k, normalised
        for i in range(reps):
            counts = np.zeros(4)
            wcounts = np.zeros(4)
            for k in range(3):
                ck = lazy_counts(P[k], lam[k], int(nk[k]), 4)
                counts += ck
                wcounts += fw[k] * ck / nk[k]   # every sample of state k weighted by (s_k/C_k)/n_k
            est[i] = c @ mbar_solve(P, frac, counts)
            est_w[i] = c @ mbar_solve(P, fw, wcounts)
        F_sim = nk.sum() * est.var(ddof=1)
        se = F_sim * math.sqrt(2.0 / (reps - 1))
        W_formula = V_primal(P, frac / C, c)[0]
        W_sim = nk.sum() * est_w.var(ddof=1)
        se_w = W_sim * math.sqrt(2.0 / (reps - 1))
        lines.append("    allocation %-8s: raw MBAR: formula sum_k C_k s_k Var_k(z_s) = %.3f (i.i.d. value V_c = %.3f), simulated N Var = %.3f +- %.3f | weights 1/C_k: formula V_c(s/C) = %.3f, simulated %.3f +- %.3f"
                     % (name, F_formula, Vp, F_sim, se, W_formula, W_sim, se_w))
        ok &= abs(F_sim - F_formula) < 4 * se and abs(W_sim - W_formula) < 4 * se_w
        vals.append((F_formula, F_sim, se))
    gap_formula = vals[1][0] - 0.5 * (vals[0][0] + vals[2][0])
    gap_sim = vals[1][1] - 0.5 * (vals[0][1] + vals[2][1])
    se_gap = math.sqrt(vals[1][2] ** 2 + 0.25 * vals[0][2] ** 2 + 0.25 * vals[2][2] ** 2)
    lines.append("    F((s+t)/2) - [F(s)+F(t)]/2: formula %+.3f, simulation %+.3f +- %.3f  (positive = convexity fails); F((s+t)/2) > max(F(s), F(t)): formula %s"
                 % (gap_formula, gap_sim, se_gap, vals[1][0] > max(vals[0][0], vals[2][0])))
    ok &= gap_formula > 0 and gap_sim > 3 * se_gap
    # the same data with effective counts: V_c(s/C) is convex; value at the three allocations
    eff = [V_primal(P, a_ / C, c)[0] for a_ in (s, 0.5 * (s + t), t)]
    lines.append("    with effective counts s_k/C_k (weights 1/C_k): V_c(s/C) = %.3f, %.3f, %.3f at s, (s+t)/2, t; midpoint gap %+.3f (convex)"
                 % (eff[0], eff[1], eff[2], eff[1] - 0.5 * (eff[0] + eff[2])))
    ok &= eff[1] <= 0.5 * (eff[0] + eff[2]) + 1e-9
    report("B9 correlated samples (lazy chains): the variance of MBAR on the raw samples follows sum_k C_k s_k Var_k(z_s) and is not convex in the allocation",
           ok, "\n" + "\n".join(lines))


if __name__ == "__main__":
    which = sys.argv[1:] or ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]
    for name in which:
        rng = np.random.default_rng(20261128 + int(name[1:]))     # every check has its own stream: a selection reproduces the full run
        globals()["check_" + name]()
    print("ALL PASS" if not FAILS else "FAILED: " + ", ".join(FAILS))
    sys.exit(1 if FAILS else 0)
