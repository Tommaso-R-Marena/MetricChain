#!/usr/bin/env python3
"""Phase II [N; the limits are P]: the flat hiding family (PHASE2_REPORT.md, Theorem A'' and Corollary A'')
for a product reference Bernoulli(p)^n around the baselines w0 = exp(-gamma |x|).

HISTORY.  The first version of this script used the reciprocal of the correct product weights (the
family it evaluated was not flat) and a crude grid; its numbers (0.0236, 0.0203 against 0.0253, 0.0489)
were wrong.  Found by the internal referee (docs/phase2/PHASE2_REVIEW.md, section 4); this version
follows the referee's formulas and was written independently of its code.

Notation (per site).  mu_{w0} = Bernoulli(p'), logit p' = logit p - gamma.  Relative cones (cone / w0,
normalised to 1 at the centre): k(x, c) = 1 if x = c, z0 = e^{-(u - gamma)} if (x, c) = (1, 0),
z1 = e^{-(u + gamma)} if (x, c) = (0, 1).  Their masses under mu_{w0}: s0 = 1 - p' + p' z0 (centre letter 0),
s1 = p' + (1 - p') z1.  Flat mixture: weights lambda_1 / lambda_0 = (1 - z0) / (1 - z1); hiding law
Bernoulli(theta), theta = (1 - z0) s1 / (1 - z0 z1).  A query x lies in the dip of c iff
eps0 * prod_i k(x_i, c_i) / s_{c_i} > 1.  Chernoff, for every n and t >= 0:
    P_hit <= eps0^t * max(rho_t(0), rho_t(1))^n,
    rho_t(0) = theta (z1/s1)^t + (1 - theta) s0^{-t},   rho_t(1) = (1 - theta) (z0/s0)^t + theta s1^{-t},
and the exponent of P_hit is  E_flat(gamma) = max_t min_a ( -ln rho_t(a) )  (Cramer; the minimax is attained
at a pure query type because the bound is log-linear in the type of the query).

Class exponent with a field (theory report, Theorem 11.59 (b)): max over gamma and 0 < t < 1 of
    F(gamma, t) = ln{ [sinh(t(lam+ - lam)/2) C(lam-)^t + sinh(t(lam - lam-)/2) C(lam+)^t] / sinh(t u) } - t ln C(lam),
lam = th + gamma, lam± = th ± u, C(x) = 2 cosh(x/2), th = ln((1-p)/p).

Output: out_p2_field_flat.txt
"""
import math

import numpy as np


def site(p, u, gam):
    lp = math.log(p / (1 - p)) - gam
    pp = 1 / (1 + math.exp(-lp))
    z0, z1 = math.exp(-(u - gam)), math.exp(-(u + gam))
    s0, s1 = 1 - pp + pp * z0, pp + (1 - pp) * z1
    th = (1 - z0) * s1 / (1 - z0 * z1)
    return z0, z1, s0, s1, th


def e_flat(p, u, gam):
    z0, z1, s0, s1, th = site(p, u, gam)
    ts = np.linspace(0.0, 1.0, 20001)
    r0 = th * (z1 / s1) ** ts + (1 - th) * s0 ** (-ts)
    r1 = (1 - th) * (z0 / s0) ** ts + th * s1 ** (-ts)
    val = np.minimum(-np.log(r0), -np.log(r1))
    return float(val.max()), th


def flat_check(p, u, gam, n=9):
    """exact check on a cube of n sites that the relative mixture is flat with these weights"""
    z0, z1, s0, s1, th = site(p, u, gam)
    lam1, lam0 = (1 - z0), (1 - z1)
    vals = []
    for w in range(n + 1):                      # x of weight w; sum over centres by (i, j) = flips
        tot = 0.0
        for i in range(n - w + 1):              # x = 0, c = 1 on i sites
            for j in range(w + 1):              # x = 1, c = 0 on j sites
                k = w - j + i
                tot += math.comb(n - w, i) * math.comb(w, j) * lam1 ** k * lam0 ** (n - k) * z1 ** i * z0 ** j
        vals.append(tot)
    return max(vals) / min(vals)


def class_exponent(p, u):
    th = math.log((1 - p) / p)
    C = lambda x: 2 * math.cosh(x / 2)
    best = (-1.0, None, None)
    for gam in np.linspace(-u, u, 801):
        lam, lp, lm = th + gam, th + u, th - u
        for t in np.linspace(0.002, 0.998, 499):
            num = math.sinh(t * (lp - lam) / 2) * C(lm) ** t + math.sinh(t * (lam - lm) / 2) * C(lp) ** t
            F = math.log(num / math.sinh(t * u)) - t * math.log(C(lam))
            if F > best[0]:
                best = (F, gam, t)
    return best


def kl(x, q):
    return x * math.log(x / q) + (1 - x) * math.log((1 - x) / (1 - q))


for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
    print("p = %.2f, u = %.1f" % (p, u))
    ratio = max(flat_check(p, u, g) for g in (-0.4 * u, 0.0, 0.4 * u))
    print("   flatness of the relative mixture on a cube of 9 sites (max/min over query types, three tilts): %.12f" % ratio)
    z0, z1, s0, s1, th = site(p, u, 0.0)
    e0, _ = e_flat(p, u, 0.0)
    if p != 0.5:
        ks = math.log(1 / s0) / (u + math.log(s1 / s0))
        print("   constant baseline: theta = %.5f, kappa* = %.5f, KL(kappa*||theta) = %.6f, max_t min_a = %.6f" % (th, ks, kl(ks, th), e0))
    else:
        print("   constant baseline: theta = %.5f, max_t min_a = %.6f (= h)" % (th, e0))
    best = max(((e_flat(p, u, g)[0], g) for g in np.linspace(-0.98 * u, 0.98 * u, 393)), key=lambda t: t[0])
    Fc, gc, tc = class_exponent(p, u)
    print("   best tilt: E_flat = %.5f at gamma = %+.3f" % best)
    print("   class exponent (Theorem 11.59 (b)): %.5f at gamma = %+.3f, t = %.3f;   flat/class = %.0f %% (constant baseline %.0f %%)"
          % (Fc, gc, tc, 100 * best[0] / Fc, 100 * e0 / Fc))
