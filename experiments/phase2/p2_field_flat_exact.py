#!/usr/bin/env python3
"""Phase II, exploratory [N]: exact hit probability P_hit = max_x q({c : x in B_c}) of the flat hiding
family of Theorem A'' at the CONSTANT baseline, for pi = Bernoulli(p)^n (exact sums over types).
Uniform cube: -ln P_hit / n decreases towards h = 0.0291 (u = 1).  With a field it tends to 0: the
theorem is void at the exponential scale there (PHASE2_REPORT.md, section 2.4 (3)).
Output: out_p2_field_flat_exact.txt
"""
import math
from math import lgamma, log, exp
def lC(n,k): return lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)
def phit(n, p, u, eps0=1.0):
    s1 = p + (1-p)*exp(-u); s0 = 1-p + p*exp(-u)
    lS0 = n*log(1+exp(-u))
    best = (-1e300, None)
    for w in range(n+1):
        terms = []
        for i in range(0, n-w+1):
            for j in range(0, w+1):
                k = w - j + i
                Rk = (log(eps0) - k*log(s1) - (n-k)*log(s0))/u
                if i + j < Rk:
                    terms.append(lC(n-w,i)+lC(w,j)+k*log(s1)+(n-k)*log(s0)-lS0)
        if terms:
            mx = max(terms); val = mx + log(sum(exp(t-mx) for t in terms))
            if val > best[0]: best = (val, w)
    return best
for (p,u) in [(0.5,1.0),(0.3,1.0),(0.1,2.0)]:
    print("p=%.2f u=%.1f" % (p,u))
    for n in (20,40,80,160):
        v,w = phit(n,p,u)
        print("   n=%4d  ln P_hit = %9.4f   -ln P_hit / n = %.5f   worst query weight/n = %.3f" % (n, v, -v/n, w/n))
