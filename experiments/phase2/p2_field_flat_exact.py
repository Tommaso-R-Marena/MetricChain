#!/usr/bin/env python3
"""Phase II [N]: exact hit probability P_hit = max_x q({c : x in B_c}) of the flat hiding family of
Theorem A'' at the CONSTANT baseline, for pi = Bernoulli(p)^n (exact sums over types), and its limit.

HISTORY.  From the values at n <= 160 the first version of this script concluded that -ln P_hit / n
tends to 0 with a field ("the theorem is void at the exponential scale").  That extrapolation was
WRONG (internal referee, docs/phase2/PHASE2_REVIEW.md section 4.3): the limit is KL(kappa*||theta) > 0,
by a Chernoff bound valid at every n; the convergence is slow (a (ln n)/n correction), as it is on
the uniform cube, where the limit is h.  This version prints the limit and the mode query up to n = 10^5.

Output: out_p2_field_flat_exact.txt
"""
import math
from math import exp, lgamma, log


def lC(n, k):
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def lse(ts):
    mx = max(ts)
    return mx + log(sum(exp(t - mx) for t in ts))


def consts(p, u):
    s1 = p + (1 - p) * exp(-u)
    s0 = 1 - p + p * exp(-u)
    return s1, s0, s1 / (s0 + s1)


def phit_all(n, p, u, eps0=1.0):
    """max over the weight w of the query of ln q({c : x in B_c}), exact"""
    s1, s0, th = consts(p, u)
    lS0 = n * log(1 + exp(-u))
    best = (-1e300, None)
    for w in range(n + 1):
        terms = []
        for i in range(0, n - w + 1):
            for j in range(0, w + 1):
                k = w - j + i
                Rk = (log(eps0) - k * log(s1) - (n - k) * log(s0)) / u
                if i + j < Rk:
                    terms.append(lC(n - w, i) + lC(w, j) + k * log(s1) + (n - k) * log(s0) - lS0)
        if terms:
            val = lse(terms)
            if val > best[0]:
                best = (val, w)
    return best


def phit_mode(n, p, u, eps0=1.0):
    """ln q({c : 0 in B_c}) for the query x = 0 (the mode of pi for p < 1/2), exact"""
    s1, s0, th = consts(p, u)
    terms = [lC(n, k) + k * log(th) + (n - k) * log(1 - th) for k in range(n + 1)
             if k < (log(eps0) - k * log(s1) - (n - k) * log(s0)) / u]
    return lse(terms)


def kl(x, q):
    return x * log(x / q) + (1 - x) * log((1 - x) / (1 - q))


for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
    s1, s0, th = consts(p, u)
    print("p = %.2f, u = %.1f, theta = %.5f" % (p, u, th))
    for n in (20, 40, 80, 160):
        v, w = phit_all(n, p, u)
        print("   n = %6d  all queries: -ln P_hit / n = %.5f   (worst query weight / n = %.3f)" % (n, -v / n, w / n))
    if p != 0.5:
        ks = log(1 / s0) / (u + log(s1 / s0))
        for n in (10 ** 3, 10 ** 4, 10 ** 5):
            print("   n = %6d  mode query:  -ln P / n     = %.5f" % (n, -phit_mode(n, p, u) / n))
        print("   limit KL(kappa*||theta) = %.6f   (kappa* = %.5f)" % (kl(ks, th), ks))
    else:
        rho0 = log(2 / (1 + exp(-u))) / u
        print("   limit h = %.6f" % kl(rho0, 0.5))
