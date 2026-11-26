#!/usr/bin/env python3
"""Workstream L4: try to falsify the FORMAL statements (as stated in the Lean files, which are
slightly more general than the paper statements) on small random instances before proving them.
Own code, fixed seed, a few seconds.  Nothing here is evidence for a theorem: the theorems are
proved in Lean.  Usage: python3 experiments/science/ws_L4/sanity_numerics.py
"""
import itertools
import math
import random

random.seed(20261126)


def subsets(S):
    S = list(S)
    for r in range(len(S) + 1):
        for c in itertools.combinations(S, r):
            yield frozenset(c)


def mix(x, b, U):
    return tuple(b[i] if i in U else x[i] for i in range(len(x)))


def mixed_diff(g, x, T, b):
    return sum((-1) ** (len(T) - len(U)) * g[mix(x, b, U)] for U in subsets(T))


# ---------------------------------------------------------------- Part A
def check_identity():
    worst = 0.0
    cases = 0
    for sizes in [(3, 2, 3, 2), (2, 2, 2, 2, 2), (3, 4, 2, 3)]:
        n = len(sizes)
        X = list(itertools.product(*[range(k) for k in sizes]))
        for _ in range(4):
            g = {x: random.uniform(-1, 1) for x in X}
            for _ in range(6):
                x = random.choice(X)
                b = random.choice(X)
                for S in subsets(range(n)):
                    for m in range(0, n + 2):
                        lhs = g[mix(x, b, S)] - sum(
                            mixed_diff(g, x, T, b) for T in subsets(S) if len(T) < m)
                        rhs = 0.0
                        for T in subsets(S):
                            if len(T) != m:
                                continue
                            below = frozenset(i for i in S if all(i < t for t in T))
                            rhs += mixed_diff(g, mix(x, b, below), T, b)
                        worst = max(worst, abs(lhs - rhs))
                        cases += 1
    return cases, worst


def check_identity_wrong_order():
    """Control: with 'i > max T' in place of 'i < min T' the identity also holds (reverse order);
    with the base point x⁰ for every T it fails.  Returns the largest defect of the latter."""
    sizes = (3, 2, 3, 2)
    n = len(sizes)
    X = list(itertools.product(*[range(k) for k in sizes]))
    g = {x: random.uniform(-1, 1) for x in X}
    worst_rev, worst_plain = 0.0, 0.0
    for _ in range(20):
        x = random.choice(X)
        b = random.choice(X)
        S = frozenset(range(n))
        for m in range(1, n + 1):
            lhs = g[mix(x, b, S)] - sum(mixed_diff(g, x, T, b) for T in subsets(S) if len(T) < m)
            rev = 0.0
            plain = 0.0
            for T in subsets(S):
                if len(T) != m:
                    continue
                above = frozenset(i for i in S if all(i > t for t in T))
                rev += mixed_diff(g, mix(x, b, above), T, b)
                plain += mixed_diff(g, x, T, b)
            worst_rev = max(worst_rev, abs(lhs - rev))
            worst_plain = max(worst_plain, abs(lhs - plain))
    return worst_rev, worst_plain


def check_allocation():
    worst = -1e9
    cases = 0
    for n in range(1, 7):
        sites = range(n)
        for m in range(1, n + 1):
            for _ in range(20):
                Ts = [frozenset(c) for c in itertools.combinations(sites, m)]
                lam = {(T, i): random.uniform(0, 1) for T in Ts for i in sites}
                # c T <= sum of the shares over the sites of T; c may be negative
                c = {T: sum(lam[(T, i)] for i in T) - random.uniform(0, 0.5) for T in Ts}
                gamma = [sum(lam[(T, i)] for T in Ts if i in T) for i in sites]
                for S in subsets(sites):
                    lhs = sum(c[T] for T in Ts if T <= S)
                    rhs = sum(gamma[i] for i in S)
                    worst = max(worst, lhs - rhs)
                    cases += 1
    return cases, worst


# ---------------------------------------------------------------- Part B
def B(b, v):
    return (b * b * math.exp(-v / b) + v * math.exp(b)) / (b * b + v)


def check_key():
    worst = -1e9
    for _ in range(200000):
        u = random.uniform(-8, 8)
        c = random.uniform(-8, 8)
        if u > c:
            u, c = c, u
        lhs = c * c * (math.exp(u) - 1 - u)
        rhs = u * u * (math.exp(c) - 1 - c)
        scale = max(1.0, abs(lhs), abs(rhs))
        worst = max(worst, (lhs - rhs) / scale)
    return worst


def check_bennett():
    worst_sharp, worst_weak, worst_low, worst_ceiling = -1e9, -1e9, -1e9, -1e9
    cases = 0
    for _ in range(40000):
        k = random.randint(1, 6)
        w = [random.random() ** random.choice([1, 3]) for _ in range(k)]
        if random.random() < 0.2:
            w[random.randrange(k)] = 0.0
        s = sum(w)
        if s == 0:
            continue
        p = [a / s for a in w]
        scale = random.choice([0.05, 0.5, 2.0, 6.0])
        X = [random.uniform(-1, 1) * scale for _ in range(k)]
        mean = sum(pi * xi for pi, xi in zip(p, X))
        X = [xi - mean - random.choice([0.0, 0.0, random.random() * scale]) for xi in X]  # E X <= 0
        EX = sum(pi * xi for pi, xi in zip(p, X))
        EX2 = sum(pi * xi * xi for pi, xi in zip(p, X))
        support = [xi for pi, xi in zip(p, X) if pi > 0]
        b = max(max(support), 0.0) + random.choice([1e-3, 0.1, 1.0])
        v = EX2 + random.choice([0.0, 0.1, 1.0])
        mgf = sum(pi * math.exp(xi) for pi, xi in zip(p, X))
        worst_sharp = max(worst_sharp, mgf - B(b, v))
        worst_weak = max(worst_weak, B(b, v) - (1 + v / b ** 2 * (math.exp(b) - 1 - b)))
        if abs(EX) < 1e-12:
            worst_low = max(worst_low, 1 - mgf)
            a = max(-min(support), 0.0) + random.choice([1e-3, 0.1, 1.0])
            low = 1 + EX2 * (math.exp(-a) - 1 + a) / a ** 2
            worst_ceiling = max(worst_ceiling, low - mgf)
        cases += 1
    return cases, worst_sharp, worst_weak, worst_low, worst_ceiling


def check_two_point_and_monotone():
    worst_tp = 0.0
    worst_mono = -1e9
    for _ in range(20000):
        b = math.exp(random.uniform(-4, 2.5))
        v = math.exp(random.uniform(-6, 3)) if random.random() < 0.95 else 0.0
        p1, p0 = v / (b * b + v), b * b / (b * b + v)
        y1, y0 = b, -v / b
        worst_tp = max(worst_tp, abs(p1 + p0 - 1), abs(p1 * y1 + p0 * y0),
                       abs(p1 * y1 ** 2 + p0 * y0 ** 2 - v) / max(1, v),
                       abs(p1 * math.exp(y1) + p0 * math.exp(y0) - B(b, v)) / B(b, v))
        b2 = b + math.exp(random.uniform(-5, 1))
        v2 = v + math.exp(random.uniform(-5, 1))
        worst_mono = max(worst_mono, (B(b, v) - B(b2, v)) / B(b, v), (B(b, v) - B(b, v2)) / B(b, v),
                         (B(b, v) - B(b2, v2)) / B(b, v))
    return worst_tp, worst_mono


def check_bracket():
    worst_up, worst_lo = -1e9, -1e9
    for _ in range(20000):
        k = random.randint(1, 6)
        w = [random.random() for _ in range(k)]
        s = sum(w)
        p = [a / s for a in w]
        r = [random.uniform(-3, 3) for _ in range(k)]
        Er = sum(pi * ri for pi, ri in zip(p, r))
        var = sum(pi * (ri - Er) ** 2 for pi, ri in zip(p, r))
        eta = random.uniform(0, 0.5)
        rbar = Er + random.uniform(-eta, eta)
        lo = min(r) - random.choice([0.0, 0.3])
        v = var + random.choice([0.0, 0.2])
        width = rbar + eta - lo
        if width <= 0:
            continue
        lnE = math.log(sum(pi * math.exp(-ri) for pi, ri in zip(p, r)))
        worst_up = max(worst_up, lnE - (-rbar + eta + math.log(B(width, v))))
        worst_lo = max(worst_lo, (-rbar - eta) - lnE)
    return worst_up, worst_lo


def check_shift_and_sharp_bracket():
    """New statements (not in the sources): B(b2,v) <= e^{b2-b1} B(b1,v) for 0 < b1 <= b2, i.e.
    b -> W(b,v) - b nonincreasing; and the certificate with W(rbar - eta - lo, v)."""
    worst_shift = -1e9
    for _ in range(40000):
        b1 = math.exp(random.uniform(-5, 2.5))
        b2 = b1 + math.exp(random.uniform(-6, 2))
        v = math.exp(random.uniform(-7, 3)) if random.random() < 0.95 else 0.0
        worst_shift = max(worst_shift, (math.log(B(b2, v)) - b2) - (math.log(B(b1, v)) - b1))
    worst_sharp, gain_max, n = -1e9, 0.0, 0
    for _ in range(40000):
        k = random.randint(1, 6)
        w = [random.random() ** random.choice([1, 4]) for _ in range(k)]
        s = sum(w)
        p = [a / s for a in w]
        r = [random.uniform(-1, 1) * random.choice([0.3, 3, 8]) for _ in range(k)]
        Er = sum(pi * ri for pi, ri in zip(p, r))
        var = sum(pi * (ri - Er) ** 2 for pi, ri in zip(p, r))
        eta = random.uniform(0, 0.5)
        rbar = Er + random.uniform(-eta, eta)
        lo = min(r) - random.choice([0.0, 0.3, 2.0])
        v = var + random.choice([0.0, 0.2])
        if not lo < rbar - eta:
            continue
        lnE = math.log(sum(pi * math.exp(-ri) for pi, ri in zip(p, r)))
        sharp = -rbar + eta + math.log(B(rbar - eta - lo, v))
        paper = -rbar + eta + math.log(B(rbar + eta - lo, v))
        worst_sharp = max(worst_sharp, lnE - sharp, sharp - paper)
        gain_max = max(gain_max, (paper - sharp) / (2 * eta) if eta > 0 else 0.0)
        n += 1
    return worst_shift, n, worst_sharp, gain_max


def check_unnormalised():
    """bennett_bracket_weights: unnormalised weights, the format of the theory division."""
    worst = -1e9
    for _ in range(20000):
        k = random.randint(1, 6)
        w = [random.random() * random.choice([0.0, 1.0, 5.0]) for _ in range(k)]
        W0 = sum(w)
        if W0 <= 0:
            continue
        r = [random.uniform(-3, 3) for _ in range(k)]
        m = sum(a * b for a, b in zip(w, r)) / W0
        var = sum(a * (b - m) ** 2 for a, b in zip(w, r)) / W0
        bfloor = max(m - min(b for a, b in zip(w, r) if a > 0), 0.0) + random.choice([1e-3, 0.5])
        v = var + random.choice([0.0, 0.3])
        lnZ = math.log(sum(a * math.exp(-b) for a, b in zip(w, r)))
        worst = max(worst, (math.log(W0) - m) - lnZ, lnZ - (math.log(W0) - m + math.log(B(bfloor, v))))
    return worst


def check_anchored_statements():
    """Corollary with anchored / ordered anchored constants computed by brute force, sandwich with
    site penalties, one-site oscillation of the remainder (P3 3.7)."""
    worst_cor, worst_ord, worst_sand, worst_reset, worst_osc = -1e9, -1e9, -1e9, -1e9, -1e9
    ratio_min = 1e9
    for sizes in [(3, 2, 3, 2), (2, 2, 2, 2, 2)]:
        n = len(sizes)
        X = list(itertools.product(*[range(k) for k in sizes]))
        for _ in range(2):
            g = {x: random.uniform(-1, 1) for x in X}
            x0 = random.choice(X)
            for m in range(1, n + 1):
                Ts = [frozenset(c) for c in itertools.combinations(range(n), m)]
                c_anch, c_ord = {}, {}
                for T in Ts:
                    tmin = min(T)
                    best_a, best_o = 0.0, 0.0
                    for z in X:
                        if any(z[i] != x0[i] for i in T):
                            continue
                        ordered = all(z[i] == x0[i] for i in range(n) if i >= tmin)
                        for b in X:
                            d = abs(mixed_diff(g, z, T, b))
                            best_a = max(best_a, d)
                            if ordered:
                                best_o = max(best_o, d)
                    c_anch[T], c_ord[T] = best_a, best_o
                gamma = [sum(c_anch[T] for T in Ts if i in T) / m for i in range(n)]

                def R(y):
                    S = frozenset(i for i in range(n) if y[i] != x0[i])
                    return g[y] - sum(mixed_diff(g, x0, T, y) for T in subsets(S) if len(T) < m), S

                for y in X:
                    Ry, S = R(y)
                    worst_cor = max(worst_cor, abs(Ry) - sum(c_anch[T] for T in Ts if T <= S))
                    worst_ord = max(worst_ord, abs(Ry) - sum(c_ord[T] for T in Ts if T <= S))
                    worst_sand = max(worst_sand, abs(Ry) - sum(gamma[i] for i in S))
                    for i in range(n):
                        y0 = tuple(x0[j] if j == i else y[j] for j in range(n))
                        worst_reset = max(worst_reset, abs(Ry - R(y0)[0]) - m * gamma[i])
                        for a in range(sizes[i]):
                            y2 = tuple(a if j == i else y[j] for j in range(n))
                            worst_osc = max(worst_osc, abs(Ry - R(y2)[0]) - 2 * m * gamma[i])
                tot_a, tot_o = sum(c_anch.values()), sum(c_ord.values())
                if tot_a > 0:
                    ratio_min = min(ratio_min, tot_o / tot_a)
    return worst_cor, worst_ord, worst_sand, worst_reset, worst_osc, ratio_min


def check_iid_and_prop6():
    worst_mse, worst_cov, worst_p6 = 0.0, -1e9, -1e9
    for _ in range(300):
        k = random.randint(1, 3)
        N = random.randint(1, 4)
        w = [random.random() for _ in range(k)]
        sw = sum(w)
        p = [a / sw for a in w]
        r = [random.uniform(-2, 2) for _ in range(k)]
        Er = sum(pi * ri for pi, ri in zip(p, r))
        var = sum(pi * (ri - Er) ** 2 for pi, ri in zip(p, r))
        lnE = math.log(sum(pi * math.exp(-ri) for pi, ri in zip(p, r)))
        lo = min(r) - random.choice([0.0, 0.5])
        v = var + random.choice([0.0, 0.3])
        eta = random.uniform(0.05, 1.5)
        mse, cover = 0.0, 0.0
        for om in itertools.product(range(k), repeat=N):
            P = math.prod(p[a] for a in om)
            rbar = sum(r[a] for a in om) / N
            mse += P * (rbar - Er) ** 2
            width = rbar + eta - lo
            W = math.log(B(width, v)) if width > 0 else 0.0
            if -rbar - eta <= lnE + 1e-12 and lnE <= -rbar + eta + W + 1e-12:
                cover += P
        worst_mse = max(worst_mse, abs(mse - var / N))
        worst_cov = max(worst_cov, (1 - v / (N * eta ** 2)) - cover)
        # Proposition 6 (i): 0 <= r <= u ;  (ii): |r| <= u/2, u <= U
        rr = [abs(x) for x in r]
        u = [x + random.choice([0.0, 0.4]) for x in rr]
        Eu = sum(pi * ui for pi, ui in zip(p, u))
        Eu2 = sum(pi * ui * ui for pi, ui in zip(p, u))
        if Eu > 0:
            K = math.log(sum(pi * math.exp(-x) for pi, x in zip(p, rr))) + sum(pi * x for pi, x in zip(p, rr))
            worst_p6 = max(worst_p6, -K, K - math.log(B(Eu, Eu2)))
        u2 = [2 * abs(x) + random.choice([0.0, 0.4]) for x in r]
        U = max(u2) + random.choice([0.0, 0.3])
        Eu, Eu2 = sum(pi * ui for pi, ui in zip(p, u2)), sum(pi * ui * ui for pi, ui in zip(p, u2))
        if Eu + U > 0:
            K = lnE + Er
            worst_p6 = max(worst_p6, -K, K - math.log(B((Eu + U) / 2, Eu2 / 4)))
    return worst_mse, worst_cov, worst_p6


if __name__ == "__main__":
    c, w = check_identity()
    print(f"A1 general remainder identity (all S, m = 0..n+1, arbitrary base and target): "
          f"{c} cases, worst |lhs - rhs| = {w:.2e}")
    wr, wp = check_identity_wrong_order()
    print(f"A1' controls: reversed order ('i > max T') worst defect = {wr:.2e} (also an identity); "
          f"base point x0 for every T: worst defect = {wp:.2e} (not an identity)")
    c, w = check_allocation()
    print(f"A2 allocation lemma, general shares, c possibly negative: {c} cases, "
          f"max(lhs - rhs) = {w:.2e} (must be <= 0)")
    print(f"B0 key lemma c^2(e^u-1-u) <= u^2(e^c-1-c) for u <= c, all signs: "
          f"max relative violation = {check_key():.2e} (must be <= ~1e-16)")
    c, ws, ww, wl, wc = check_bennett()
    print(f"B1 two-point bound: {c} random laws; max(E e^X - B(b,v)) = {ws:.2e}; "
          f"max(B - 1 - (v/b^2)(e^b-1-b)) = {ww:.2e}; max(1 - E e^X | EX=0) = {wl:.2e}; "
          f"ceiling lower bound max violation = {wc:.2e} (all must be <= ~1e-12)")
    wt, wm = check_two_point_and_monotone()
    print(f"B2 two-point law: worst defect of (mass, mean, second moment, mgf) = {wt:.2e}; "
          f"monotonicity of B in b, in v, in both: max relative decrease = {wm:.2e}")
    wu, wl = check_bracket()
    print(f"B3 deterministic bracket: max violation upper = {wu:.2e}, lower = {wl:.2e}")
    ws, n, wb, g = check_shift_and_sharp_bracket()
    print(f"B4 (new) W(b2,v) - b2 <= W(b1,v) - b1 for b1 <= b2: max violation = {ws:.2e}; "
          f"sharper certificate W(rbar - eta - lo): {n} cases, max violation = {wb:.2e}; "
          f"largest gain (paper - sharp)/(2 eta) = {g:.3f}")
    print(f"B5 unnormalised weights (bennett_bracket_weights): max violation = {check_unnormalised():.2e}")
    print("B6 size of the gain of the sharper upper end, W(b + 2 eta, v) - W(b, v), b = rbar - eta - lo:")
    for (b, v, eta, label) in [(0.061, 4.8e-3, math.sqrt(4.8e-3 / (50000 * 0.05)), "P3 m=5 inputs, N=50000, delta=0.05"),
                               (3.7, 0.036 ** 2, 0.036 / math.sqrt(1000 * 0.05), "theory example W(3.7, 0.036^2), N=1000, delta=0.05"),
                               (8.0, 0.25, 0.5 / math.sqrt(1000 * 0.05), "deep floor b=8, v=0.25, N=1000, delta=0.05")]:
        W0, W1 = math.log(B(b, v)), math.log(B(b + 2 * eta, v))
        print(f"   {label}: W(b,v) = {W0:.4e}, eta = {eta:.3e}, gain = {W1 - W0:.3e} "
              f"= {(W1 - W0) / (2 * eta):.4f} * 2 eta")
    wc, wo, wsd, wr, wos, rmin = check_anchored_statements()
    print(f"A3 anchored constants by brute force (two grids, all m >= 1, all y): corollary max violation = {wc:.2e}; "
          f"with ordered anchored constants = {wo:.2e}; sandwich with site penalties = {wsd:.2e}; "
          f"|R(y) - R(y reset at i)| - m gamma_i = {wr:.2e}; |R(y) - R(y')| - 2 m gamma_i = {wos:.2e} "
          f"(all must be <= ~1e-15); smallest ratio (sum of ordered anchored constants)/(sum of anchored constants) = {rmin:.3f}")
    wm, wcv, wp6 = check_iid_and_prop6()
    print(f"B7 N iid samples, exact enumeration of Omega^N: |mse - Var/N| max = {wm:.2e}; "
          f"(1 - v/(N eta^2)) - coverage max = {wcv:.2e} (must be <= 0); "
          f"Proposition 6 (i), (ii) max violation = {wp6:.2e}")
