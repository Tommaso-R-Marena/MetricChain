#!/usr/bin/env python3
"""AA2 audit, script S8 -- fact (F2) of Theorem 11.52 ("a -> -ln W(a) is u-Lipschitz on the outer block")
with a known part that is not a product measure.  A one-screen confirmation of the report's own remark
(section 11.23, "what fails in the nested algorithm": the constant is u + osc phi', L8093-8101); the systematic
treatment (bounded influence, an explicit obstruction) is the commission of workstream N (N_brief.md, N5(b)).

Curie-Weiss known part f(x) = n phi(|x|/n), phi(k) = -(beta J / 2)(2k - 1)^2, on Q_n = Q_o x Q_i.
Residual psi(a, b) = gamma |b|, |gamma| <= u: a member of L_u that does not depend on the outer point at all.
Fibre average W(a) = E[ e^{-psi(a, b)} | a ] under the conditional law of the inner block.
For a product reference W does not depend on a.  Here: the largest change of -ln W under ONE outer flip, in units of u (the 'excess').

Run:  python3 experiments/audit/AA2/s8_fibre_averages_with_interactions.py > experiments/audit/AA2/out_s8.txt
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def worst_flip(n_o, n_i, bJ, gamma):
    n = n_o + n_i
    j = np.arange(n_i + 1)
    lc = gammaln(n_i + 1) - gammaln(j + 1) - gammaln(n_i - j + 1)
    lnW = []
    for k in range(n_o + 1):                                   # type of the outer point
        kap = (k + j) / n
        logw = lc + n * (bJ / 2) * (2 * kap - 1) ** 2          # ln of the conditional weight of inner type j
        lnW.append(logsumexp(logw - gamma * j) - logsumexp(logw))
    lnW = np.array(lnW)
    return float(np.abs(np.diff(lnW)).max())


print("AA2 / S8: fibre averages are not u-Lipschitz when the known part has interactions")
print("excess := largest |ln W(a) - ln W(a')| over one outer flip, divided by u, for the member psi(a, b) = gamma |b| of L_u")
print("(gamma = -u or +u), which ignores the outer block; for a product reference the excess is 0.")
print("The member psi(a, b) = gamma |b| + s u |a| (s = +1 or -1, also in L_u) then has a fibre average that changes by")
print("u (1 + excess) per outer flip: fact (F2) of Theorem 11.52, with the constant u, fails as soon as the excess is positive;")
print("with excess <= c it holds with the constant (1 + c) u ('bounded influence'), and where the excess grows with n it")
print("holds with no constant of the order of u.")
print()
print("  n_o  n_i  beta J     u    excess(gamma=-u)  excess(gamma=+u)")
worst = 0.0
rows = {}
for n_o, n_i in ((8, 8), (20, 20), (50, 50), (200, 200)):
    for bJ in (0.0, 0.5, 1.0, 1.5, 3.0, -1.0, -3.0):
        for u in (0.2, 1.0):
            r1 = worst_flip(n_o, n_i, bJ, -u) / u
            r2 = worst_flip(n_o, n_i, bJ, +u) / u
            worst = max(worst, r1, r2)
            rows[(n_o, bJ, u)] = max(r1, r2)
            print(f"  {n_o:3d}  {n_i:3d}  {bJ:6.1f}  {u:4.1f}   {r1:14.4f}  {r2:16.4f}")
print()
# direct check of the combined member on a small cube, by enumeration of types
n_o, n_i, bJ, u = 8, 8, 1.5, 0.2
n = n_o + n_i
j = np.arange(n_i + 1)
lc = gammaln(n_i + 1) - gammaln(j + 1) - gammaln(n_i - j + 1)
best = 0.0
for gamma in (-u, u):
    for sgn in (-1.0, 1.0):
        lnW = []
        for k in range(n_o + 1):
            kap = (k + j) / n
            logw = lc + n * (bJ / 2) * (2 * kap - 1) ** 2
            lnW.append(logsumexp(logw - gamma * j - sgn * u * k) - logsumexp(logw))
        best = max(best, float(np.abs(np.diff(lnW)).max()) / u)
print(f"direct check, n_o = n_i = 8, beta J = 1.5, u = 0.2: the member gamma |b| + s u |a| has a fibre average that changes by"
      f" {best:.4f} u per outer flip  (1 + excess = {1 + rows[(8, 1.5, 0.2)]:.4f})")
print()
print(f"largest excess found: {worst:.3f}")
print("Reading: beta J = 0 (a product measure): excess 0, (F2) holds with u.  One phase away from criticality (beta J = 0.5)")
print("and antiferromagnets: excess 0.3 to 0.6, stable in n -- (F2) holds with a constant below 2u, a quantitative weakening.")
print("At the critical coupling (beta J = 1) the excess is 0.76 to 0.98 and still rising with n.  Two phases")
print("(beta J = 1.5, 3): the excess grows with n at a small slope (the conditional law of the inner block switches wells) and")
print("saturates only at osc(phi')/u -- the closure test of the two-level algorithm, which applies the tail lemma to W with the")
print("slope u, then certifies nothing.")
