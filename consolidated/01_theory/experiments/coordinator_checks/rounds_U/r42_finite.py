#!/usr/bin/env python3
"""Assistant C -- Corollary R4.2 at finite n: E' = -ln max(p1, p2)/n against the printed
E = -ln(p1 + p2)/n of the table of Theorem 11.86.  Own code from the statement:
W1 = {c1(d1) + c2(d2) <= T}, W2 = {c2(d2) <= T}, c_j = -ln Bin(n_j, 1/2), p1 = P((D1, D2) not in W1),
p2 = P(D2 not in W2).  (n, n1, T) from out_u_check2.txt (T/n to 5 digits) and, for three rows, the
reviewer's bisected budgets.  Tail probabilities are summed in log space over the complement."""
import numpy as np
from scipy.special import gammaln, logsumexp


def logpmf(m):
    d = np.arange(m + 1)
    return gammaln(m + 1) - gammaln(d + 1) - gammaln(m - d + 1) - m * np.log(2.0)


def p1p2(n, n1, T):
    n2 = n - n1
    l1, l2 = logpmf(n1), logpmf(n2)
    S = l1[:, None] + l2[None, :]                 # ln P1 P2 ;  c1 + c2 = -S
    out1 = (-S) > T
    lp1 = logsumexp(S[out1])
    lp2 = logsumexp(l2[(-l2) > T])
    return lp1, lp2


# last entry: True if T is the reviewer's bisected budget (4 decimals), False if T = (printed T/n) * n (5 digits of T/n)
rows = [(1, 400, 180, 0.04434 * 400, 0.03005, False), (1, 800, 360, 33.7288, 0.03411, True),
        (1, 1600, 800, 0.03987 * 1600, 0.03543, False), (1, 3200, 1760, 125.6841, 0.03684, True),
        (2, 200, 90, 0.13748 * 200, 0.11294, False), (2, 400, 180, 0.12916 * 400, 0.11520, False),
        (2, 1600, 880, 200.8750, 0.12117, True)]
print("# u     n    n1        T    E=-ln(p1+p2)/n  printed   E'=-ln max(p1,p2)/n   E'-E      p2/p1    "
      "ln p1 + T - ln((n1+1)(n2+1)) <= 0   ln p2 + T - ln(n2+1) <= 0")
ok = True
worst = 0.0
for (u, n, n1, T, Eprint, exact) in rows:
    lp1, lp2 = p1p2(n, n1, T)
    E = -np.logaddexp(lp1, lp2) / n
    Ep = -max(lp1, lp2) / n
    b1 = lp1 + T - np.log((n1 + 1) * (n - n1 + 1))
    b2 = lp2 + T - np.log(n - n1 + 1)
    ok &= abs(E - Eprint) < (6e-6 if exact else 2e-4) and b1 <= 0 and b2 <= 0 and Ep >= E
    worst = max(worst, Ep - E)
    print(f"  {u}  {n:5d}  {n1:5d}  {T:9.4f}   {E:.5f}       {Eprint:.5f}     {Ep:.5f}          {Ep - E:.2e}   "
          f"{np.exp(lp2 - lp1):.2e}   {b1:9.3f}                            {b2:9.3f}")
print("# all rows: E agrees with the printed value (to 6e-6 at the three bisected budgets, to 2e-4 where T is only"
      " known through T/n), E' >= E, p1 <= (n1+1)(n2+1)e^{-T}, p2 <= (n2+1)e^{-T}:", bool(ok))
print(f"# largest E' - E over the seven rows: {worst:.2e}")
