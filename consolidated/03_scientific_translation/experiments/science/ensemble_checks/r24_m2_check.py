#!/usr/bin/env python3
"""Coordinator's check of workstream R24's finding M2 (addendum item 89 (b) is false as printed).

R24's counterexample: four states, sandwich l = (0.5, 0.5, 2, 1) <= w <= u = (1, 1, 3, 2), member w = (1, 1, 2, 1.5), which is
strictly inside the box at the fourth state.  Data: the mean of f = (2, 2, 0, 1) and the population of the fourth state.
Claim: these TWO means identify the member (the range of every mu(x) over the members with the same two means is 0),
although it is not a threshold ("bang-bang") member -- against "data pin only bang-bang members" (SCI-RES-0032 section 4 (b)).
Here, with linear programmes of the coordinator's own (Charnes-Cooper: v = alpha w, alpha l <= v <= alpha u, sum v = 1):
  (1) the upper end of E f over the sandwich is t* = 1 = E_mu f, and the fourth state lies on the level set {f = t*};
  (2) the range of mu(x), x = 1..4, over members with E f = E_mu f and mu(4) fixed: must be 0;
  (3) controls: with the first mean alone the ranges must be positive; a member strictly inside at EVERY state must NOT be
      identified by the same two functions.
Run: python3 -B r24_m2_check.py > r24_m2_check.log
"""
import numpy as np
from scipy.optimize import linprog

l = np.array([0.5, 0.5, 2.0, 1.0]); u = np.array([1.0, 1.0, 3.0, 2.0]); f = np.array([2.0, 2.0, 0.0, 1.0]); e4 = np.array([0.0, 0.0, 0.0, 1.0])


def ranges(w, data):
    """range of mu(x) over the members with the same means of the functions in `data`; variables (v_1..v_4, alpha)"""
    mu = w / w.sum(); A_eq = [np.append(np.ones(4), 0.0)]; b_eq = [1.0]
    for g in data: A_eq.append(np.append(g, 0.0)); b_eq.append(float(mu @ g))
    A_ub = []; b_ub = []
    for i in range(4):
        r = np.zeros(5); r[i] = 1.0; r[4] = -u[i]; A_ub.append(r); b_ub.append(0.0)       # v_i <= alpha u_i
        r = np.zeros(5); r[i] = -1.0; r[4] = l[i]; A_ub.append(r); b_ub.append(0.0)       # v_i >= alpha l_i
    out = []
    for i in range(4):
        c = np.zeros(5); c[i] = 1.0
        lo = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * 5, method="highs"); hi = linprog(-c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * 5, method="highs")
        assert lo.status == 0 and hi.status == 0; out.append(-hi.fun - lo.fun)
    return np.array(out)


w = np.array([1.0, 1.0, 2.0, 1.5]); mu = w / w.sum()
# (1) the upper end of E f over the sandwich
c = np.append(-f, 0.0); A_ub = []; b_ub = []
for i in range(4):
    r = np.zeros(5); r[i] = 1.0; r[4] = -u[i]; A_ub.append(r); b_ub.append(0.0)
    r = np.zeros(5); r[i] = -1.0; r[4] = l[i]; A_ub.append(r); b_ub.append(0.0)
top = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=[np.append(np.ones(4), 0.0)], b_eq=[1.0], bounds=[(0, None)] * 5, method="highs")
print(f"(1) upper end of E f over the sandwich: {-top.fun:.12f}; E_mu f = {mu @ f:.12f} (must be equal: the member is a maximiser); f at the fourth state = {f[3]} = t*; "
      f"the member's weights against the box: {', '.join(f'{l[i]} <= {w[i]} <= {u[i]}' for i in range(4))} (strictly inside at the fourth state)")
assert abs(-top.fun - 1.0) < 1e-9 and abs(mu @ f - 1.0) < 1e-12
r2 = ranges(w, [f, e4]); r1 = ranges(w, [f])
print(f"(2) ranges of mu(x) over members with the same E f and the same population of the fourth state: {', '.join(f'{v:.1e}' for v in r2)} (must be 0: identified by two means)")
print(f"(3) control, the first mean alone: {', '.join(f'{v:.3f}' for v in r1)} (must be positive somewhere)")
w_in = np.array([0.8, 0.7, 2.5, 1.5]); r_in = ranges(w_in, [f, e4])
print(f"    control, a member strictly inside at every state, w = {w_in.tolist()}, the same two functions: ranges {', '.join(f'{v:.3f}' for v in r_in)} (must be positive: not identified)")
assert r2.max() < 1e-9 and r1.max() > 1e-3 and r_in.max() > 1e-3
print("ALL DONE")
