#!/usr/bin/env python3
"""Referee replication 3: the flat hiding family with a field (report section 2.4 (3)); independent code.

Reference pi = Bernoulli(p)^n, class constant u, baseline w0 = exp(-gamma |x|) (gamma = 0: constant weight).
Relative cones (normalised to 1 at the centre), per site:  centre bit 0: (1, z0) at x = (0, 1), z0 = e^{-(u-gamma)};
centre bit 1: (z1, 1), z1 = e^{-(u+gamma)}.  mu_{w0} = Bernoulli(p')^n, logit p' = logit p - gamma.
Flat weights: lambda1/lambda0 = (1-z0)/(1-z1)  [derived: lambda0 + lambda1 z1 = lambda0 z0 + lambda1].
Column masses s0 = (1-p') + p' z0, s1 = p' + (1-p') z1; hiding law q = Bernoulli(theta)^n, theta = lambda1 s1/(lambda1 s1 + lambda0 s0).
The dip of centre c (|c| = k) covers x iff (u+gamma) i + (u-gamma) j < ln eps0 - k ln s1 - (n-k) ln s0,
i = #{x=0,c=1}, j = #{x=1,c=0}.   P_hit = max_x q({c : x in B_c}).

Part 1: exact P_hit at the constant baseline, all query types (n <= 480) and the mode query (n <= 10^6); the limit.
Part 2: tilted baselines: exponent of P_hit by (a) the dual formula max_t min(g_t(0), g_t(1)), (b) a brute-force grid,
        (c) exact sums at finite n; with the correct weights and with the report's inverted ratio.
Part 3: single-type dip families (centres uniform on a type class), brute-force grid.
Run: python3 -B r3_field.py
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.stats import binom
from scipy.optimize import minimize_scalar


def kl(x, y):
    x = min(max(x, 1e-300), 1 - 1e-16)
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def setup(p, u, gam, inverted=False):
    lp = math.log(p / (1 - p)) - gam
    pp = 1 / (1 + math.exp(-lp))
    z0, z1 = math.exp(-(u - gam)), math.exp(-(u + gam))
    s0, s1 = (1 - pp) + pp * z0, pp + (1 - pp) * z1
    lam = (1 - z0) / (1 - z1)            # lambda1/lambda0 (referee)
    if inverted:
        lam = 1 / lam                    # the report's line 286 / the coordinator's script
    th = lam * s1 / (lam * s1 + s0)
    return pp, z0, z1, s0, s1, th


def lC(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def log_binom_cdf(kmax, n, th):
    """ln P(Bin(n, th) <= kmax) by an explicit log-sum (no underflow for extreme tails)."""
    if kmax < 0:
        return -np.inf
    k = np.arange(max(0, kmax - 200000), kmax + 1)        # the tail is dominated by the last terms
    return float(logsumexp(lC(n, k) + k * math.log(th) + (n - k) * math.log(1 - th)))


def brute_force_checks():
    """Part 0: the type-counting code and the product formulas against brute force over all (x, c), n = 9."""
    n, eps0 = 9, 1.0
    N = 1 << n
    PC = np.array([bin(v).count("1") for v in range(N)])
    X = np.arange(N)
    D = PC[X[:, None] ^ X[None, :]]
    ok = True
    for (p, u, gam) in [(0.3, 1.0, 0.0), (0.3, 1.0, 0.4), (0.1, 2.0, -0.7), (0.5, 1.0, 0.3)]:
        pi = p ** PC * (1 - p) ** (n - PC)
        w0 = np.exp(-gam * PC)
        A0 = pi @ w0
        K = np.exp(-u * D)                                             # K[x, c]
        ratio = (math.exp(-gam) - math.exp(-u)) / (1 - math.exp(-(u + gam)))   # lambda1/lambda0 for cones e^{-u d}
        lam = ratio ** PC
        lam = lam * (w0[0] / (K @ lam)[0])                             # sum_c lam(c) e^{-u d(x,c)} = w0(x)
        assert np.allclose(K @ lam, w0)
        mcol = (pi @ K) / A0                                           # m(c) of Corollary A''
        q = lam * mcol
        H = eps0 / mcol
        pp, z0, z1, s0, s1, th = setup(p, u, gam)
        qprod = th ** PC * (1 - th) ** (n - PC)
        ok = ok and abs(q.sum() - 1) < 1e-10 and np.allclose(q, qprod, rtol=1e-9, atol=0)
        cover = H[None, :] * K > w0[:, None] * (1 + 1e-12)             # x in B_c
        hit = (cover * q[None, :]).sum(axis=1)
        v, w = phit_exact(n, p, u, gam, eps0)
        ok = ok and abs(math.log(hit.max()) - v) < 1e-9
        # flatness of the relative mixture
        rel = ((H[None, :] * K) @ q) / w0
        ok = ok and np.allclose(rel, eps0)
        # the report's inverted ratio: the same construction is not flat
        pp, z0, z1, s0, s1, thw = setup(p, u, gam, inverted=True)
        qw = thw ** PC * (1 - thw) ** (n - PC)
        relw = ((H[None, :] * K) @ qw) / w0
        print(f"   p={p} u={u} gamma={gam:+.1f}: q = Bernoulli({th:.4f})^n [brute force agrees]; ln P_hit brute force {math.log(hit.max()):.6f} "
              f"= type sums {v:.6f}; relative mixture / eps0 in [{rel.min():.6f}, {rel.max():.6f}];"
              f" with the report's ratio (theta={thw:.4f}): in [{relw.min():.4f}, {relw.max():.4f}]")
    print("   Part 0 all consistent:", ok)


def phit_exact(n, p, u, gam=0.0, eps0=1.0, inverted=False):
    """max over query types w of ln q({c : x in B_c}); returns (ln P_hit, worst w)."""
    pp, z0, z1, s0, s1, th = setup(p, u, gam, inverted)
    best = (-np.inf, None)
    lth, l1th = math.log(th), math.log(1 - th)
    for w in range(n + 1):
        i = np.arange(0, n - w + 1)[:, None]
        j = np.arange(0, w + 1)[None, :]
        k = w - j + i
        feas = (u + gam) * i + (u - gam) * j < math.log(eps0) - k * math.log(s1) - (n - k) * math.log(s0) - 1e-12
        if not feas.any():
            continue
        lt = lC(n - w, i) + lC(w, j) + k * lth + (n - k) * l1th
        val = logsumexp(lt[feas])
        if val > best[0]:
            best = (val, w)
    return best


def dual_exponent(p, u, gam, inverted=False):
    """lim -ln P_hit / n = max_{t>=0} min(g_t(0), g_t(1)),
    g_t(0) = -ln(th z1^t s1^-t + (1-th) s0^-t)   (query bit 0),
    g_t(1) = -ln((1-th) z0^t s0^-t + th s1^-t)   (query bit 1)."""
    pp, z0, z1, s0, s1, th = setup(p, u, gam, inverted)

    def g(t):
        g0 = -math.log(th * (z1 / s1) ** t + (1 - th) * s0 ** (-t))
        g1 = -math.log((1 - th) * (z0 / s0) ** t + th * s1 ** (-t))
        return min(g0, g1)
    res = minimize_scalar(lambda t: -g(t), bounds=(0.0, 60.0), method='bounded', options={'xatol': 1e-12})
    # guard against a local optimum: coarse scan
    ts = np.linspace(0, 60, 6001)
    scan = max(g(t) for t in ts)
    return max(-res.fun, scan, 0.0), th


def grid_exponent(p, u, gam, G=241, inverted=False):
    """brute force: min over (omega, A, B) feasible of (1-omega) KL(A||th) + omega KL(B||1-th)."""
    pp, z0, z1, s0, s1, th = setup(p, u, gam, inverted)
    W = np.linspace(0, 1, G)[:, None, None]
    A = np.linspace(0, 1, G)[None, :, None]
    B = np.linspace(0, 1, G)[None, None, :]

    def klv(x, y):
        x = np.clip(x, 1e-300, 1 - 1e-16)
        return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))
    i = A * (1 - W)
    j = B * W
    k = W - j + i
    feas = (u + gam) * i + (u - gam) * j <= -(k * math.log(s1) + (1 - k) * math.log(s0)) + 1e-12
    rate = (1 - W) * klv(A, th) + W * klv(B, 1 - th)
    return float(np.where(feas, rate, np.inf).min())


def single_type_exponent(p, u, gam, G=201):
    """centres uniform on the type class k: exponent(k) = min over feasible (omega, i, j) with that k of
    h2(k) - [(1-omega) h2(A) + omega h2(B)]; returns max over k and the maximiser.  (brute force)"""
    pp, z0, z1, s0, s1, th = setup(p, u, gam)

    def h2(x):
        x = np.clip(x, 1e-300, 1 - 1e-16)
        return -x * np.log(x) - (1 - x) * np.log(1 - x)
    ks = np.linspace(0, 1, G)
    W = np.linspace(0, 1, 2 * G - 1)[:, None]           # query type
    J = np.linspace(0, 1, 2 * G - 1)[None, :]           # B: fraction of the query's ones that are 0 in the centre
    best_k, best_val = None, -1.0
    for k in ks:
        j = J * W
        i = k - W + j                                   # from k = omega - j + i
        ok = (i >= -1e-12) & (i <= 1 - W + 1e-12)
        with np.errstate(divide='ignore', invalid='ignore'):
            A = np.where(1 - W > 1e-12, np.clip(i, 0, None) / np.maximum(1 - W, 1e-300), 0.0)
        A = np.clip(A, 0, 1)
        feas = ok & ((u + gam) * i + (u - gam) * j <= -(k * math.log(s1) + (1 - k) * math.log(s0)) + 1e-12)
        cnt = (1 - W) * h2(A) + W * h2(J)
        val = np.where(feas, h2(k) - cnt, np.inf).min()
        if not np.isfinite(val):
            val = 0.0
        val = max(float(val), 0.0)
        if val > best_val:
            best_val, best_k = val, k
    return best_val, best_k


if __name__ == "__main__":
    print("== Part 0: brute force over all pairs (x, c) at n = 9 ==")
    brute_force_checks()
    print()
    print("== Part 1: constant baseline (gamma = 0) ==")
    for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
        pp, z0, z1, s0, s1, th = setup(p, u, 0.0)
        print(f"p={p} u={u}: s0={s0:.6f} s1={s1:.6f} hiding law theta={th:.6f}")
        for n in (20, 40, 80, 160, 320, 480):
            v, w = phit_exact(n, p, u)
            print(f"   exact, all query types: n={n:4d}  ln P_hit={v:10.4f}  -ln P_hit/n={-v/n:.5f}  worst query weight/n={w/n:.3f}")
        # limit by the dual formula, and (field case) the closed form for the mode query
        lim, _ = dual_exponent(p, u, 0.0)
        print(f"   limit of -ln P_hit/n (dual formula max_t min) = {lim:.6f}")
        if p < 0.5:
            kstar = math.log(1 / s0) / (u + math.log(s1 / s0))
            print(f"   closed form for the mode query x=0: centre types k/n < kappa* = ln(1/s0)/(u+ln(s1/s0)) = {kstar:.6f} "
                  f"(typical type theta={th:.6f});  KL(kappa*||theta) = {kl(kstar, th):.6f}")
            for n in (160, 1000, 10000, 100000, 1000000):
                kmax = math.ceil((-n * math.log(s0)) / (u + math.log(s1 / s0)) - 1e-9) - 1      # k < ...  (eps0 = 1)
                lp = log_binom_cdf(kmax, n, th)
                print(f"   mode query only: n={n:8d}  -ln q(c: 0 in B_c)/n = {-lp/n:.6f}")
        else:
            # uniform cube: P_hit = V(n, R)/2^n with R ~ rho0 n; the limit is h
            rho0 = math.log(2 / (1 + math.exp(-u))) / u
            print(f"   uniform cube: limit should be h = KL(rho0||1/2) = {kl(rho0, 0.5):.6f}")
            for n in (160, 1000, 10000, 100000, 1000000):
                R = math.ceil(-n * math.log(s0) / u - 1e-9) - 1
                lp = log_binom_cdf(R, n, 0.5)
                print(f"   any query: n={n:8d}  -ln P_hit/n = {-lp/n:.6f}")

    print()
    print("== Part 1b: the Chernoff bound is non-asymptotic: P_hit <= eps0^t exp(-n min(g_t(0), g_t(1))) for every n, t >= 0 ==")
    for (p, u) in [(0.3, 1.0), (0.1, 2.0)]:
        pp, z0, z1, s0, s1, th = setup(p, u, 0.0)
        g0 = lambda t: -math.log(th * (z1 / s1) ** t + (1 - th) * s0 ** (-t))
        g1 = lambda t: -math.log((1 - th) * (z0 / s0) ** t + th * s1 ** (-t))
        ts = np.linspace(0, 5, 500001)
        tstar = float(ts[int(np.argmax([min(g0(t), g1(t)) for t in ts]))])
        rate = min(g0(tstar), g1(tstar))
        line = f"   p={p} u={u}: t*={tstar:.5f}  g_t*(0)={g0(tstar):.6f}  g_t*(1)={g1(tstar):.6f}  rate={rate:.6f};"
        for n in (160, 480):
            v, w = phit_exact(n, p, u)
            line += f"  n={n}: exact ln P_hit={v:.4f} <= {-n*rate:.4f}: {v <= -n*rate + 1e-9};"
        print(line)
    print()
    print("== Part 2: tilted baselines; exponent of P_hit for the flat family ==")
    print("   columns: gamma | correct weights: theta, dual exponent, grid(121^3) | report's inverted ratio: theta, dual exponent, grid(121^3)")
    print("   (a grid minimum over a coarse grid lies slightly above the true minimum; the dual formula is exact in the limit)")
    for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
        print(f"p={p} u={u}")
        gams = np.linspace(-0.95 * u, 0.95 * u, 39)
        rows = []
        for gi, gam in enumerate(gams):
            d, th = dual_exponent(p, u, gam)
            dinv, thinv = dual_exponent(p, u, gam, inverted=True)
            rows.append((gam, th, d, thinv, dinv))
            if gi % 3 == 0:
                g1 = grid_exponent(p, u, gam, G=121)
                g2 = grid_exponent(p, u, gam, G=121, inverted=True)
                print(f"   {gam:+.3f} | {th:.3f} {d:.5f} {g1:.5f} | {thinv:.3f} {dinv:.5f} {g2:.5f}")
        b = max(rows, key=lambda t: t[2])
        binv = max(rows, key=lambda t: t[4])
        print(f"   on the report's grid of 39 gammas:  max flat exponent, correct weights = {b[2]:.5f} at gamma={b[0]:+.3f};"
              f"   with the inverted ratio = {binv[4]:.5f} at gamma={binv[0]:+.3f}")
        # fine maximisation over gamma (correct weights)
        fine = max(((dual_exponent(p, u, g)[0], g) for g in np.linspace(-0.999 * u, 0.999 * u, 1999)))
        print(f"   fine grid of 1999 gammas, correct weights: max flat exponent = {fine[0]:.5f} at gamma={fine[1]:+.4f}")
        print(f"   at gamma = 0: {dual_exponent(p, u, 0.0)[0]:.5f}")

    print()
    print("== Part 2c: exact finite-n sums at a tilted baseline (correct weights), against the dual formula ==")
    for (p, u, gam) in [(0.3, 1.0, 0.25), (0.1, 2.0, 0.8), (0.5, 1.0, 0.4)]:
        d, th = dual_exponent(p, u, gam)
        out = []
        for n in (80, 160, 320):
            v, w = phit_exact(n, p, u, gam)
            out.append(f"n={n}: {-v/n:.5f} (w/n={w/n:.2f})")
        print(f"   p={p} u={u} gamma={gam:+.2f}: dual limit {d:.5f}; exact -ln P_hit/n: " + ";  ".join(out))

    print("   mode query (x = 0) at large n, tilted baselines (correct weights): -ln q(c: 0 in B_c)/n")
    for (p, u, gam) in [(0.3, 1.0, 0.25), (0.3, 1.0, -0.308), (0.1, 2.0, 0.8), (0.1, 2.0, -1.174)]:
        pp, z0, z1, s0, s1, th = setup(p, u, gam)
        d, _ = dual_exponent(p, u, gam)
        out = []
        for n in (1000, 10000, 100000):
            kmax = math.ceil((-n * math.log(s0)) / (u + gam + math.log(s1 / s0)) - 1e-9) - 1
            out.append(f"n={n}: {-log_binom_cdf(kmax, n, th)/n:.6f}")
        print(f"   p={p} u={u} gamma={gam:+.3f}: " + ";  ".join(out) + f"   [dual limit over all queries {d:.6f}]")
    print("   exact sums over ALL query types at the best tilts (correct weights), against the Chernoff rate (a lower bound for every n):")
    for (p, u, gam) in [(0.3, 1.0, -0.308), (0.1, 2.0, -1.174)]:
        pp, z0, z1, s0, s1, th = setup(p, u, gam)
        g0 = lambda t: -math.log(th * (z1 / s1) ** t + (1 - th) * s0 ** (-t))
        g1 = lambda t: -math.log((1 - th) * (z0 / s0) ** t + th * s1 ** (-t))
        d, _ = dual_exponent(p, u, gam)
        ts = np.linspace(0, 5, 50001)
        tstar = float(ts[int(np.argmax([min(g0(t), g1(t)) for t in ts]))])
        out = []
        for n in (160, 320, 640):
            v, w = phit_exact(n, p, u, gam)
            out.append(f"n={n}: {-v/n:.5f} (worst w/n={w/n:.2f})")
        print(f"   p={p} u={u} gamma={gam:+.3f}: " + ";  ".join(out) + f"   [rate {d:.6f}; at t*={tstar:.3f}: g(0)={g0(tstar):.6f}, g(1)={g1(tstar):.6f}]")
    print()
    print("== Part 3: single-type dip families (brute-force grid), max over the type and over gamma ==")
    for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
        best = (-1, None, None)
        for gam in np.linspace(-0.95 * u, 0.95 * u, 39):
            v, k = single_type_exponent(p, u, gam, G=101)
            if v > best[0]:
                best = (v, gam, k)
        print(f"   p={p} u={u}: best single-type exponent on the 39-gamma grid = {best[0]:.5f} at gamma={best[1]:+.3f}, type {best[2]:.3f}")
