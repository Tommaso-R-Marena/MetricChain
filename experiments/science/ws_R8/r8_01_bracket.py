#!/usr/bin/env python3
"""R8 / script 01 -- Proposition A16.1 (entropy bracket) and Corollary A16.2 (numbers).

Own code; the coordinator's scripts were not opened before this was written.

Part A  n*h(sigma_u) <= S(mu_g) <= n ln 2 on members of the class by exact enumeration:
        (A1) random McShane members of several kinds, n = 4..12;
        (A2) adversarial: direct minimisation of the entropy over the class polytope
             (SLSQP from many starts, n = 3,4,5) and a greedy extreme-point descent (n = 6..10);
        (A3) the chain-rule step itself: every conditional probability lies in [sigma_u, 1-sigma_u],
             for random orders of the coordinates;
        (A4) product reference Bern(p)^n:  -U - n max(KL(a0||p),KL(a1||p)) <= ln(Z_g/Z_0) <= -U,
             U the mean of g under mu_g ~ pi e^{-g}.
        (A5) mutation: a 1.5u-Lipschitz function violates the lower end (the test can fail).
Part B  A16.2: ln cosh(u/2) = KL(1/2||sigma_u); the two series; the table of the addendum.

Run:  python3 r8_01_bracket.py            (about 1 minute)
"""
import math, sys, time
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20261125)


def hbin(p):
    p = np.asarray(p, dtype=float)
    out = np.zeros_like(p)
    m = (p > 0) & (p < 1)
    out[m] = -p[m] * np.log(p[m]) - (1 - p[m]) * np.log1p(-p[m])
    return out if out.shape else float(out)


def sigma(u):
    return 1.0 / (1.0 + math.exp(u))


def popcount(n):
    x = np.arange(1 << n, dtype=np.int64)
    w = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        w += (x >> i) & 1
    return w


def lower_env(phi, n, u):
    """McShane lower envelope  g(x) = min_y phi(y) + u d_H(x,y)  (one pass per coordinate)."""
    g = phi.copy()
    x = np.arange(1 << n)
    for i in range(n):
        g = np.minimum(g, g[x ^ (1 << i)] + u)
    return g


def upper_env(phi, n, u):
    g = phi.copy()
    x = np.arange(1 << n)
    for i in range(n):
        g = np.maximum(g, g[x ^ (1 << i)] - u)
    return g


def lip_const(g, n):
    x = np.arange(1 << n)
    return max(np.max(np.abs(g - g[x ^ (1 << i)])) for i in range(n))


def gibbs(g):
    m = g.min()
    w = np.exp(-(g - m))
    Z = w.sum()
    p = w / Z
    U = float((p * g).sum())
    lnZ = math.log(Z) - m
    S = lnZ + U
    return lnZ, U, S, p


def random_member(n, u, kind):
    N = 1 << n
    w = popcount(n)
    x = np.arange(N)
    if kind == 0:      # lower envelope of white noise of scale s
        s = rng.choice([0.3, 1.0, 3.0, 10.0]) * u
        return lower_env(rng.normal(0, s, N), n, u)
    if kind == 1:      # upper envelope of white noise
        s = rng.choice([0.3, 1.0, 3.0, 10.0]) * u
        return upper_env(rng.normal(0, s, N), n, u)
    if kind == 2:      # a few anchors with random depths: min of cones
        k = rng.integers(1, 6)
        phi = np.full(N, 1e9)
        idx = rng.integers(0, N, k)
        phi[idx] = rng.uniform(-n * u, 0, k)
        return np.minimum(lower_env(phi, n, u), 0.0)
    if kind == 3:      # truncated cones / plateaus at random centres, min and max combined
        g = np.zeros(N)
        for _ in range(rng.integers(1, 4)):
            a = int(rng.integers(0, N))
            d = popcount(n)[x ^ a]
            r = rng.uniform(0, n)
            kap = rng.uniform(0, r)
            sgn = rng.choice([-1.0, 1.0])
            t = sgn * u * np.minimum(kap, np.maximum(r - d, 0))
            g = np.minimum(g, t) if sgn < 0 else np.maximum(g, t)
        return g
    if kind == 4:      # additive with slopes in [-u,u], plus an envelope of noise
        sl = rng.uniform(-u, u, n)
        g = np.zeros(N)
        for i in range(n):
            g += sl[i] * ((x >> i) & 1)
        return g
    if kind == 5:      # extreme: the full cone, slope exactly u
        a = int(rng.integers(0, N))
        return u * popcount(n)[x ^ a].astype(float)
    if kind == 6:      # distance to a random code (several polarised basins)
        k = rng.integers(2, 9)
        phi = np.full(N, 1e9)
        phi[rng.integers(0, N, k)] = 0.0
        return lower_env(phi, n, u)
    if kind == 7:      # slope-u envelope of a +-1 random field times large scale: rugged, saturating
        return lower_env(rng.choice([-1.0, 1.0], N) * n * u, n, u)
    raise ValueError


def cond_probs_ok(p, n, u, tol=1e-12):
    """Chain-rule step: for a random order, P(x_i = 1 | earlier) in [sigma, 1-sigma]."""
    order = rng.permutation(n)
    s = sigma(u)
    x = np.arange(1 << n)
    worst = 0.0
    # marginal over the 'later' coordinates, successively
    q = p.copy().reshape([2] * n)       # axis k corresponds to bit n-1-k
    axes = list(range(n))
    # sum out coordinates from the last of the order to the first
    for pos in range(n - 1, -1, -1):
        i = order[pos]
        ax = axes.index(i)
        # conditional of coordinate i given the earlier ones: q has axes = remaining coords
        tot = q.sum(axis=ax, keepdims=True)
        with np.errstate(invalid="ignore", divide="ignore"):
            c = np.take(q, 1, axis=ax) / np.squeeze(tot, axis=ax)
        c = c[np.isfinite(c)]
        worst = max(worst, float(np.max(s - c)), float(np.max(c - (1 - s))))
        q = np.squeeze(tot, axis=ax)
        axes.pop(ax)
    return worst


def part_A1():
    print("== A1/A3: random members, exact enumeration ==")
    tot = 0
    worst_low = np.inf
    worst_up = np.inf
    worst_cond = -np.inf
    min_ratio = {}
    for n in (4, 6, 8, 10, 12):
        for u in (0.25, 1.0, 2.0, 4.0):
            s = sigma(u)
            lo = n * hbin(s)
            for kind in range(8):
                for rep in range(4 if n < 12 else 2):
                    g = random_member(n, u, kind)
                    L = lip_const(g, n)
                    assert L <= u * (1 + 1e-12) + 1e-12, (n, u, kind, L)
                    lnZ, U, S, p = gibbs(g)
                    tot += 1
                    worst_low = min(worst_low, S - lo)
                    worst_up = min(worst_up, n * math.log(2) - S)
                    if n <= 10:
                        worst_cond = max(worst_cond, cond_probs_ok(p, n, u))
                    key = (kind,)
                    min_ratio[key] = min(min_ratio.get(key, np.inf), (S - lo) / (n * (math.log(2) - hbin(s))))
    print(f"  members tested: {tot}")
    print(f"  min over members of  S - n h(sigma_u)   = {worst_low:.3e}   (must be >= 0)")
    print(f"  min over members of  n ln2 - S          = {worst_up:.3e}   (must be >= 0)")
    print(f"  max excursion of a conditional probability outside [sigma,1-sigma] = {worst_cond:.3e}")
    print("  least (S - n h)/(n a) per family (0 = lower end attained):")
    names = ["lower env noise", "upper env noise", "min of cones", "plateaus", "additive", "full cone",
             "dist to code", "rugged saturating"]
    for k in range(8):
        print(f"     {names[k]:20s} {min_ratio[(k,)]:.6f}")
    return worst_low >= -1e-9 and worst_up >= -1e-9 and worst_cond <= 1e-9


def entropy_of(g):
    return gibbs(g)[2]


def part_A2():
    print("== A2: adversarial minimisation of the entropy over the class ==")
    ok = True
    for n in (3, 4, 5):
        N = 1 << n
        x = np.arange(N)
        # constraints  |g(x) - g(x^i)| <= u   as  A g <= u
        rows = []
        for i in range(n):
            for a in range(N):
                b = a ^ (1 << i)
                if a < b:
                    r = np.zeros(N); r[a] = 1; r[b] = -1
                    rows.append(r); rows.append(-r)
        A = np.array(rows)
        for u in (0.5, 1.0, 2.0, 4.0):
            lo = n * hbin(sigma(u))
            best = np.inf
            nstart = 60 if n < 5 else 25
            for st in range(nstart):
                g0 = random_member(n, u, int(rng.integers(0, 8)))
                g0 = g0 - g0.mean()
                cons = [{"type": "ineq", "fun": lambda g, A=A, u=u: u - A @ g, "jac": lambda g, A=A: -A},
                        {"type": "eq", "fun": lambda g: g[0], "jac": lambda g: np.eye(N)[0]}]
                res = minimize(entropy_of, g0 - g0[0], constraints=cons, method="SLSQP",
                               options={"maxiter": 500, "ftol": 1e-13})
                g = res.x
                viol = max(0.0, float(np.max(A @ g - u)))
                if viol < 1e-9:
                    best = min(best, entropy_of(g))
            print(f"  n={n} u={u:4.2f}: min entropy found {best:.10f}   n h(sigma_u) = {lo:.10f}   diff {best - lo:+.2e}")
            ok &= best - lo >= -1e-8
    # greedy extreme-point descent for larger n: push single values to an extreme allowed value
    for n in (6, 8, 10):
        N = 1 << n
        x = np.arange(N)
        nb = np.stack([x ^ (1 << i) for i in range(n)], axis=1)
        for u in (1.0, 3.0):
            lo = n * hbin(sigma(u))
            best = np.inf
            for st in range(6):
                g = random_member(n, u, int(rng.integers(0, 8)))
                S = entropy_of(g)
                for sweep in range(40):
                    improved = False
                    for a in rng.permutation(N)[: min(N, 400)]:
                        lo_a = np.max(g[nb[a]]) - u
                        hi_a = np.min(g[nb[a]]) + u
                        old = g[a]
                        for cand in (lo_a, hi_a):
                            g[a] = cand
                            S2 = entropy_of(g)
                            if S2 < S - 1e-13:
                                S = S2; old = cand; improved = True
                            g[a] = old
                    if not improved:
                        break
                best = min(best, S)
            print(f"  n={n} u={u:4.2f}: greedy descent, least entropy {best:.8f}   n h(sigma_u) = {lo:.8f}   diff {best - lo:+.2e}")
            ok &= best - lo >= -1e-8
    return ok


def klb(a, b):
    return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))


def part_A4():
    print("== A4: product reference Bern(p)^n ==")
    worst_lo = np.inf; worst_up = np.inf; cnt = 0
    for n in (6, 9, 11):
        N = 1 << n
        w = popcount(n)
        for p in (0.2, 0.35, 0.5, 0.8):
            lnpi = w * math.log(p) + (n - w) * math.log(1 - p)
            for u in (0.5, 1.5, 3.0):
                a0 = p * math.exp(-u) / (1 - p + p * math.exp(-u))
                a1 = p * math.exp(u) / (1 - p + p * math.exp(u))
                R = max(klb(a0, p), klb(a1, p))
                for kind in range(8):
                    g = random_member(n, u, kind)
                    lw = lnpi - g
                    m = lw.max()
                    ww = np.exp(lw - m)
                    lnratio = m + math.log(ww.sum())          # ln(Z_g/Z_0), Z_0 = 1
                    mu = ww / ww.sum()
                    U = float((mu * g).sum())
                    worst_up = min(worst_up, -U - lnratio)
                    worst_lo = min(worst_lo, lnratio - (-U - n * R))
                    cnt += 1
    print(f"  cases {cnt}: min( -U - ln(Z_g/Z_0) ) = {worst_up:.3e} ; min( ln(Z_g/Z_0) + U + n max KL ) = {worst_lo:.3e}  (both >= 0)")
    # equality at the two extreme cones
    n, p, u = 9, 0.35, 1.5
    w = popcount(n)
    lnpi = w * math.log(p) + (n - w) * math.log(1 - p)
    for sgn, nm in ((+1, "cone around 0^n (g = u|x|)"), (-1, "cone around 1^n (g = -u|x|)")):
        g = sgn * u * w.astype(float)
        lw = lnpi - g; m = lw.max(); ww = np.exp(lw - m)
        lnratio = m + math.log(ww.sum()); mu = ww / ww.sum(); U = float((mu * g).sum())
        a0 = p * math.exp(-u) / (1 - p + p * math.exp(-u)); a1 = p * math.exp(u) / (1 - p + p * math.exp(u))
        print(f"  {nm}: -U - ln(Z/Z0) = {-U - lnratio:.10f} ; n KL(a0||p) = {n*klb(a0,p):.10f} ; n KL(a1||p) = {n*klb(a1,p):.10f}")
    return worst_lo >= -1e-9 and worst_up >= -1e-9


def part_A5():
    print("== A5: mutation (the test must be able to fail) ==")
    n, u = 10, 1.0
    g = 1.5 * u * popcount(n).astype(float)      # 1.5u-Lipschitz cone
    S = gibbs(g)[2]
    lo = n * hbin(sigma(u))
    print(f"  1.5u-cone: S = {S:.6f} < n h(sigma_u) = {lo:.6f} : violation detected = {S < lo}")
    return S < lo


def part_B():
    print("== B: Corollary A16.2 ==")
    import mpmath as mp
    mp.mp.dps = 40
    ok = True
    for u in (0.5, 1, 2, 4):
        u = mp.mpf(u)
        s = 1 / (1 + mp.e ** u)
        h = lambda p: -p * mp.log(p) - (1 - p) * mp.log(1 - p)
        a = mp.log(2) - h(s)
        KLhalf = mp.mpf(1) / 2 * mp.log((mp.mpf(1) / 2) / s) + mp.mpf(1) / 2 * mp.log((mp.mpf(1) / 2) / (1 - s))
        lc = mp.log(mp.cosh(u / 2))
        t = mp.tanh(u / 2)
        ser1 = mp.nsum(lambda k: t ** (2 * k) / (2 * k), [1, mp.inf])
        ser2 = mp.nsum(lambda k: t ** (2 * k) / (2 * k * (2 * k - 1)), [1, mp.inf])
        serd = mp.nsum(lambda k: t ** (2 * k) * (k - 1) / (k * (2 * k - 1)), [2, mp.inf])
        rho0 = mp.log(2 / (1 + mp.e ** (-u))) / u
        expo = mp.log(2) - h(rho0 + a / u)        # exponent without the datum at eps1 = a(u)
        ok &= abs(KLhalf - lc) < mp.mpf(10) ** (-30) and abs(ser1 - lc) < mp.mpf(10) ** (-25)
        ok &= abs(ser2 - a) < mp.mpf(10) ** (-25) and abs(serd - (lc - a)) < mp.mpf(10) ** (-25)
        ok &= abs(a - u * (rho0 - s)) < mp.mpf(10) ** (-30)       # a(u) = u (rho0 - sigma_u)
        print(f"  u={float(u):3.1f}: a(u)={float(a):.5f}  ln cosh(u/2)={float(lc):.5f}  "
              f"KL(1/2||s)-lncosh={float(KLhalf-lc):.1e}  series ok  "
              f"exponent without datum at eps1=a: {float(expo):.3e}  rho0+a/u={float(rho0+a/u):.5f}")
    return ok


if __name__ == "__main__":
    t0 = time.time()
    res = {}
    res["A1"] = part_A1()
    res["A2"] = part_A2()
    res["A4"] = part_A4()
    res["A5"] = part_A5()
    res["B"] = part_B()
    print("SUMMARY", res, f"  time {time.time()-t0:.1f}s")
    sys.exit(0 if all(res.values()) else 1)
