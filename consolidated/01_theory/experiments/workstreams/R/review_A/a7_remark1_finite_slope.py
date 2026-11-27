"""Referee A, test 7: remark (1) of section 5 for a theta with a FINITE slope at zero.

theta(e) = (1 - 0.8 e)_+ : a = 1, theta'(0+) = -0.8.  Sigma(B, 0) = 0.8 B for all B <= a = 1, INCLUDING the boundary
point B = (1 - s) a = 1 (the supremum over e is finite there, not attained as e -> 0).
Remark (1) says: S_1 = lower convex envelope of min(1, Sigma(B, S_0(B))) on [0, tau_1] 'with the value one at tau_1'
(tau_1 = a, S_0 = 0), i.e. 'cut by the tangent line through (tau_1, 1)'.  Taken literally this gives S_1(B) = B
(the line through (0, 0) and (1, 1)) and the 'majorant' M_{S_1, 1}(x) = (1 - x)_+, which is BELOW T_1 = theta.
The correct rule (Corollary U': W' <= Sigma(., W(.)) on all of [0, b'], endpoint included) gives S_1 = 0.8 B and
M_{S_1,1} = theta.
"""
import numpy as np
from ralib import PwLin

th = PwLin([(1.0, 0.8)], 0.0, "(1 - 0.8 e)_+")
Bs = np.array([0.1, 0.5, 0.9, 0.999, 1.0])
print("Sigma(B, 0) for B =", Bs, ":", [round(th.sigma(float(B), 0.0), 6) for B in Bs], " (0.8 B; finite at B = a = 1)")
x = np.array([0.05, 0.2, 0.5, 1.0, 1.2])
theta = th(x)
lit = np.maximum(0.0, 1 - x)                    # M for S_1(B) = B on [0, 1]
cor = np.maximum(0.0, 1 - 0.8 * x)              # M for S_1(B) = 0.8 B on [0, 1]
print("x                      :", x)
print("T_1 = theta(x)         :", theta)
print("literal rule  M(x)     :", lit, " -> theta - M =", theta - lit, " (positive: NOT a majorant)")
print("corrected rule M(x)    :", cor, " -> theta - M =", theta - cor)
