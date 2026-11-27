#!/usr/bin/env python3
"""Workstream A1 -- independent numerical review of the PROOF of Lemma 11.89 as written in the theory report
(Ising-pair parametrisation, steps (1)-(6)), with own code.  This is a check of the report's intermediate
formulas, not of the statement (for the statement see odds_ratio_check.py).

  R1  step (2): dI/dh1 = (1/2)(1-mu^2)[T(h2) - delta(h1) Delta(h2)]   against finite differences
  R2  step (3): T(h) < 0 for h > 0
  R3  step (4): -T(h) < delta(h) Delta(h) for h > 0, and the closed form of the difference
  R4  step (5): the maximiser in h1 at fixed h2 > 0 is h1 = -k with 0 < k < h2, delta(k) = -T(h2)/Delta(h2),
               and the capacity C(h2) is decreasing in h2 > 0
  R5  step (6): I(h1,h2) <= C(h2) <= C(0) = ln 2 - h(sigma(2J))
Run: python3 odds_ratio_report_proof_check.py
"""
import math
import sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar

rng = np.random.default_rng(11)
fails = 0


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    fails += (not ok)


lc = lambda x: math.log(math.cosh(x))


def table(J, h1, h2):
    P = np.array([[math.exp(J * b * x + h1 * b + h2 * x) for x in (-1, 1)] for b in (-1, 1)])
    return P / P.sum()


def I(J, h1, h2):
    P = table(J, h1, h2)
    pb, px = P.sum(1, keepdims=True), P.sum(0, keepdims=True)
    return float((P * np.log(P / (pb @ px))).sum())


delta = lambda h, J: 0.5 * (lc(h + J) - lc(h - J))
T = lambda h, J: J * (math.tanh(h + J) + math.tanh(h - J)) - 2 * delta(h, J)
Delta = lambda h, J: math.tanh(h + J) - math.tanh(h - J)

# R1
err = 0.0
for _ in range(5000):
    J, h1, h2 = rng.uniform(0.05, 2.5), rng.normal(0, 1.2), rng.normal(0, 1.2)
    P = table(J, h1, h2)
    mu = P[1].sum() - P[0].sum()
    nu = P[:, 1].sum() - P[:, 0].sum()
    e = 1e-5
    fd1 = (I(J, h1 + e, h2) - I(J, h1 - e, h2)) / (2 * e)
    fd2 = (I(J, h1, h2 + e) - I(J, h1, h2 - e)) / (2 * e)
    f1 = 0.5 * (1 - mu * mu) * (T(h2, J) - delta(h1, J) * Delta(h2, J))
    f2 = 0.5 * (1 - nu * nu) * (T(h1, J) - delta(h2, J) * Delta(h1, J))
    err = max(err, abs(fd1 - f1), abs(fd2 - f2))
check("R1  gradient formulas of step (2)", err < 5e-9, "max discrepancy with finite differences %.1e" % err)

# R2, R3
ok2 = ok3 = True
iderr = 0.0
for _ in range(20000):
    J, h = rng.uniform(0.01, 4), rng.uniform(1e-3, 6)
    ok2 &= T(h, J) < 0
    ok3 &= -T(h, J) < delta(h, J) * Delta(h, J)
    a, b = h + J, h - J
    al, be = math.exp(2 * a), math.exp(2 * b)
    closed = ((al * be + 2 * be + 1) * math.log((al + 1) / (be + 1)) - be * (al + 1) * math.log(al / be)) / ((al + 1) * (be + 1))
    lhs = -T(h, J) - delta(h, J) * Delta(h, J)
    if max(al, be) < 1e12:
        iderr = max(iderr, abs(lhs - closed) / (1 + abs(lhs)))
check("R2  T(h) < 0 for h > 0 (20000 samples)", ok2)
check("R3  -T < delta*Delta for h > 0, and the closed form of step (4)", ok3 and iderr < 1e-9, "max relative identity error %.1e" % iderr)

# R4, R5
ok4 = ok5 = True
for J in (0.2, 0.7, 1.5):
    Cprev = None
    for h2 in np.linspace(0.0, 4.0, 41):
        res = minimize_scalar(lambda h1: -I(J, h1, h2), bounds=(-12, 12), method="bounded", options={"xatol": 1e-11})
        C, h1s = -res.fun, res.x
        if h2 > 1e-9:
            k = -h1s
            g = -T(h2, J) / Delta(h2, J)
            ok4 &= (0 < k < h2) and abs(delta(k, J) - g) < 1e-6
        if Cprev is not None:
            ok4 &= C < Cprev + 1e-12
        Cprev = C
        if h2 == 0.0:
            C0 = C
            sig = 1 / (1 + math.exp(-2 * J))
            ok5 &= abs(C0 - (math.log(2) + sig * math.log(sig) + (1 - sig) * math.log(1 - sig))) < 1e-9
        ok5 &= C <= C0 + 1e-12
check("R4  maximiser h1 = -k, 0 < k < h2, delta(k) = -T(h2)/Delta(h2); capacity decreasing in h2 > 0", ok4)
check("R5  C(h2) <= C(0) = ln 2 - h(sigma(2J))", ok5)
print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
