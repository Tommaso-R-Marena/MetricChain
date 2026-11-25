#!/usr/bin/env python3
"""Workstream A1 -- independent numerical check of the odds-ratio lemma (theory report Lemma 11.89)
and of the short proof by monotone margin flows (Hasenclever & Scholz 2013, Prop. 8(a)).

Statement.  For a strictly positive 2x2 probability table P with log odds ratio
ln[P11 P00 / (P10 P01)] = 2s:   I(B;X) <= ln 2 - h(sigma(|s|)),  sigma(s) = 1/(1+e^{-s}),
with equality iff s = 0 or both margins are uniform.

Checks (all with code written here, sharing nothing with the theory division's scripts):
  T1  random tables: the inequality, and the equality case;
  T2  the derivative formula  dI/dt = Cov(iota, phi) = (p11-p00) I + p00 p11 [g(p00) - g(p11)],
      g(x) = ln(1 - c x)/x, c = 1 - 1/lambda, along P_t ~ P * exp(t(1[00]-1[11])), against finite differences;
      and its sign (= sign(p11 - p00) when lambda > 1);  the same for the off-diagonal flow;
  T3  monotonicity of I along both flows on a grid (global, not only infinitesimal);
  T4  the capacity reformulation: capacity of the binary channel (a, b) [P(1|0)=a, P(1|1)=b] equals the
      largest chord gap of -h between a and b, and is <= the capacity of the BSC with the same odds ratio;
  T5  exhaustive grid over (odds ratio, both margins) in high precision (mpmath) for the worst slack;
  T6  mutation tests: the "lemma" with a wrong right-hand side must FAIL (shows the test has power);
  T7  the lemma fails for 3x3 Potts-type tables (uniform margins do not maximise I) -- consistency with the
      theory report's remark, so the 2x2 restriction matters.
Run:  python3 odds_ratio_check.py        (about 20 s)
"""
import math
import random
import sys

import numpy as np

try:
    import mpmath as mp
except Exception:  # pragma: no cover
    mp = None

rng = np.random.default_rng(20261125)
random.seed(20261125)


def h2(p):
    """binary entropy, nats"""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log1p(-p)


def mi(P):
    """mutual information of a 2x2 (or kxk) table, nats"""
    P = np.asarray(P, dtype=float)
    pb = P.sum(axis=1, keepdims=True)
    px = P.sum(axis=0, keepdims=True)
    mask = P > 0
    return float((P[mask] * np.log(P[mask] / (pb @ px)[mask])).sum())


def bound(s):
    s = abs(s)
    return math.log(2.0) - h2(1.0 / (1.0 + math.exp(-s)))


def table_from(s, y, z):
    """Hasenclever-Scholz margin-transformation coordinates: x = s = half log odds ratio."""
    P = np.array([[math.exp(s + y + z), math.exp(y)], [math.exp(z), math.exp(s)]])
    return P / P.sum()


def half_log_odds(P):
    return 0.5 * math.log(P[0, 0] * P[1, 1] / (P[0, 1] * P[1, 0]))


fails = 0


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    if not ok:
        fails += 1


# ---------------------------------------------------------------- T1
worst = -1.0
worst_tab = None
n1 = 400000
for _ in range(n1):
    kind = rng.integers(0, 3)
    if kind == 0:
        P = rng.dirichlet([1, 1, 1, 1]).reshape(2, 2)
    elif kind == 1:
        P = rng.dirichlet([0.2, 0.2, 0.2, 0.2]).reshape(2, 2)
    else:
        P = table_from(rng.normal(0, 3), rng.normal(0, 3), rng.normal(0, 3))
    if P.min() < 1e-300:
        continue
    s = half_log_odds(P)
    slack = mi(P) - bound(s)
    if slack > worst:
        worst, worst_tab = slack, P.copy()
check("T1  I <= ln2 - h(sigma(s)) on %d random tables" % n1, worst <= 1e-12,
      "largest (I - bound) = %.3e" % worst)

eq_gap = max(abs(mi(table_from(s, 0.0, 0.0)) - bound(s)) for s in np.linspace(-8, 8, 161))
check("T1b equality at uniform margins", eq_gap < 1e-12, "max |I - bound| = %.2e" % eq_gap)
strict = min(bound(s) - mi(table_from(s, y, z))
             for s in (0.3, 1.0, 2.5) for (y, z) in ((0.05, 0), (0, 0.05), (0.05, 0.05), (0.05, -0.05)))
check("T1c strict inequality off the origin", strict > 0, "min slack at |(y,z)|=0.05: %.3e" % strict)


# ---------------------------------------------------------------- T2
def flow_diag(P, t):
    Q = P.copy()
    Q[0, 0] *= math.exp(t)
    Q[1, 1] *= math.exp(-t)
    return Q / Q.sum()


def flow_off(P, t):
    Q = P.copy()
    Q[0, 1] *= math.exp(t)
    Q[1, 0] *= math.exp(-t)
    return Q / Q.sum()


def dI_diag_formula(P):
    lam = P[0, 0] * P[1, 1] / (P[0, 1] * P[1, 0])
    c = 1.0 - 1.0 / lam
    g = lambda x: math.log1p(-c * x) / x
    return (P[1, 1] - P[0, 0]) * mi(P) + P[0, 0] * P[1, 1] * (g(P[0, 0]) - g(P[1, 1]))


def dI_off_formula(P):
    lam = P[0, 0] * P[1, 1] / (P[0, 1] * P[1, 0])
    a = lam - 1.0
    g = lambda x: math.log1p(a * x) / x
    return (P[1, 0] - P[0, 1]) * mi(P) + P[0, 1] * P[1, 0] * (g(P[0, 1]) - g(P[1, 0]))


def dI_cov(P, phi):
    pb = P.sum(axis=1, keepdims=True)
    px = P.sum(axis=0, keepdims=True)
    iota = np.log(P / (pb @ px))
    return float((P * iota * phi).sum() - (P * iota).sum() * (P * phi).sum())


maxerr = 0.0
sign_ok = True
for _ in range(20000):
    P = table_from(rng.normal(0, 1.5), rng.normal(0, 1.5), rng.normal(0, 1.5))
    eps = 1e-5
    fd = (mi(flow_diag(P, eps)) - mi(flow_diag(P, -eps))) / (2 * eps)
    f1 = dI_diag_formula(P)
    f2 = dI_cov(P, np.array([[1.0, 0.0], [0.0, -1.0]]))
    fo = (mi(flow_off(P, eps)) - mi(flow_off(P, -eps))) / (2 * eps)
    g1 = dI_off_formula(P)
    g2 = dI_cov(P, np.array([[0.0, 1.0], [-1.0, 0.0]]))
    maxerr = max(maxerr, abs(fd - f1), abs(f1 - f2), abs(fo - g1), abs(g1 - g2))
    # signs: toward balance of each diagonal (for any odds ratio != 1)
    if abs(P[1, 1] - P[0, 0]) > 1e-6 and abs(half_log_odds(P)) > 1e-3:
        sign_ok &= (f1 * (P[1, 1] - P[0, 0]) > 0)
    if abs(P[1, 0] - P[0, 1]) > 1e-6 and abs(half_log_odds(P)) > 1e-3:
        sign_ok &= (g1 * (P[1, 0] - P[0, 1]) > 0)
check("T2  derivative formula = covariance formula = finite differences (both flows)", maxerr < 2e-8,
      "max discrepancy %.2e" % maxerr)
check("T2b sign of dI/dt = sign(p11 - p00) [diag flow], sign(p10 - p01) [off-diag flow]", sign_ok)

# ---------------------------------------------------------------- T3
mono_ok = True
for _ in range(3000):
    P = table_from(rng.normal(0, 2), rng.normal(0, 2), rng.normal(0, 2))
    # diagonal flow reaches p00 = p11 at t* = 0.5 ln(p11/p00)
    tstar = 0.5 * math.log(P[1, 1] / P[0, 0])
    vals = [mi(flow_diag(P, tstar * k / 40.0)) for k in range(41)]
    mono_ok &= all(vals[k + 1] >= vals[k] - 1e-13 for k in range(40))
    Q = flow_diag(P, tstar)
    ustar = 0.5 * math.log(Q[1, 0] / Q[0, 1])
    vals2 = [mi(flow_off(Q, ustar * k / 40.0)) for k in range(41)]
    mono_ok &= all(vals2[k + 1] >= vals2[k] - 1e-13 for k in range(40))
    R = flow_off(Q, ustar)
    mono_ok &= abs(R[0, 0] - R[1, 1]) < 1e-12 and abs(R[0, 1] - R[1, 0]) < 1e-12
    mono_ok &= abs(half_log_odds(R) - half_log_odds(P)) < 1e-9
    mono_ok &= abs(mi(R) - bound(half_log_odds(P))) < 1e-10
check("T3  I is nondecreasing along diag flow then off-diag flow; endpoint = symmetric table with the same odds ratio",
      mono_ok)


# ---------------------------------------------------------------- T4
def capacity(a, b, grid=20001):
    """capacity of the binary channel P(X=1|B=0)=a, P(X=1|B=1)=b by direct maximisation over the input"""
    lam = np.linspace(0.0, 1.0, grid)
    m = lam * b + (1 - lam) * a

    def H(p):
        p = np.clip(p, 1e-300, 1 - 1e-16)
        return -p * np.log(p) - (1 - p) * np.log1p(-p)

    vals = H(m) - lam * H(np.array([b]))[0] - (1 - lam) * H(np.array([a]))[0]
    k = int(np.argmax(vals))
    # golden refinement around the grid maximum
    lo, hi = lam[max(k - 1, 0)], lam[min(k + 1, grid - 1)]
    f = lambda l: h2(l * b + (1 - l) * a) - l * h2(b) - (1 - l) * h2(a)
    for _ in range(80):
        m1, m2 = lo + (hi - lo) * 0.382, lo + (hi - lo) * 0.618
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return f(0.5 * (lo + hi))


def capacity_closed(a, b):
    """chord-gap form: C = h(m*) - [chord of h between a and b at m*], h'(m*) = slope of the chord"""
    slope = (h2(b) - h2(a)) / (b - a)
    mstar = 1.0 / (1.0 + math.exp(slope))  # h'(m) = ln((1-m)/m) = slope
    return h2(mstar) - (h2(a) + slope * (mstar - a))


cap_ok, cap_err, worst_cap = True, 0.0, -1.0
for _ in range(4000):
    a, b = sorted(rng.uniform(0.001, 0.999, size=2))
    if b - a < 1e-3:
        continue
    C = capacity(a, b)
    Cc = capacity_closed(a, b)
    cap_err = max(cap_err, abs(C - Cc))
    s = 0.5 * (math.log(b / (1 - b)) - math.log(a / (1 - a)))  # half log odds ratio of the channel
    worst_cap = max(worst_cap, C - bound(s))
    cap_ok &= (C <= bound(s) + 1e-10)
check("T4  capacity(a,b) = largest chord gap of the binary entropy; <= capacity of the BSC with the same odds ratio",
      cap_ok and cap_err < 1e-8, "max |C - chord gap| = %.1e, max (C - BSC) = %.2e" % (cap_err, worst_cap))

# ---------------------------------------------------------------- T5
if mp is not None:
    mp.mp.dps = 40

    def mi_mp(s, y, z):
        e = [mp.e ** (s + y + z), mp.e ** y, mp.e ** z, mp.e ** s]
        tot = sum(e)
        p = [x / tot for x in e]
        pb = [p[0] + p[1], p[2] + p[3]]
        px = [p[0] + p[2], p[1] + p[3]]
        return (p[0] * mp.log(p[0] / (pb[0] * px[0])) + p[1] * mp.log(p[1] / (pb[0] * px[1]))
                + p[2] * mp.log(p[2] / (pb[1] * px[0])) + p[3] * mp.log(p[3] / (pb[1] * px[1])))

    def bound_mp(s):
        sg = 1 / (1 + mp.e ** (-abs(s)))
        return mp.log(2) + sg * mp.log(sg) + (1 - sg) * mp.log(1 - sg)

    worst5 = mp.mpf(-1)
    cnt = 0
    for s in [mp.mpf(k) / 4 for k in range(1, 41)]:
        for y in [mp.mpf(k) / 2 for k in range(-12, 13)]:
            for z in [mp.mpf(k) / 2 for k in range(-12, 13)]:
                d = mi_mp(s, y, z) - bound_mp(s)
                cnt += 1
                if not (y == 0 and z == 0):
                    worst5 = max(worst5, d)
                else:
                    assert abs(d) < mp.mpf(10) ** (-30)
    check("T5  40-digit grid (%d tables, s in (0,10], |y|,|z| <= 6): I < bound strictly off the origin" % cnt,
          worst5 < 0, "largest (I - bound) off the origin = %s" % mp.nstr(worst5, 5))
else:
    print("SKIP T5 (mpmath missing)")

# ---------------------------------------------------------------- T6 (mutations)
mut1 = max(mi(table_from(s, y, z)) - (bound(s) - 0.05 * (y * y + z * z))  # a bound that is too small off the origin
           for s in (0.5, 1, 2) for y in (-0.3, 0.3) for z in (-0.3, 0.3))
# wrong right-hand side: sigma(2s) would be the bound for log odds ratio 4s
mut2 = max(bound(0.9 * s) - mi(table_from(s, 0, 0)) for s in (0.5, 1, 2))
# wrong statement "I is largest when ONE margin is uniform": compare a table with one uniform margin
def one_margin_uniform(s, z):
    # choose y so that the row margin is uniform
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        P = table_from(s, mid, z)
        if P[0].sum() > 0.5:
            hi = mid
        else:
            lo = mid
    return table_from(s, 0.5 * (lo + hi), z)
mut3 = bound(1.0) - mi(one_margin_uniform(1.0, 1.0))
check("T6  mutations detected (tighter bound fails; 0.9s-bound fails; one uniform margin is not enough)",
      mut1 > 0 and mut2 < 0 and mut3 > 1e-3,
      "tighter-bound violation %.2e; 0.9s-bound slack %.2e (<0); one-margin slack %.3e (>0)" % (mut1, mut2, mut3))

# ---------------------------------------------------------------- T7 (3 letters: the lemma is a 2x2 fact)
def potts(a, c, s):
    P = np.outer(a, c) * (1.0 + (math.exp(s) - 1.0) * np.eye(len(a)))
    return P / P.sum()

s = 0.3
uni3 = mi(potts(np.ones(3), np.ones(3), s))
best = uni3
for _ in range(20000):
    a = rng.dirichlet(np.ones(3) * 0.7) + 1e-9
    c = rng.dirichlet(np.ones(3) * 0.7) + 1e-9
    best = max(best, mi(potts(a, c, s)))
two = mi(potts(np.array([1.0, 1.0, 1e-9]), np.array([1.0, 1.0, 1e-9]), s))
# (the random search is only a sanity check that nothing beats the two-letter table by much; it need not find it)
check("T7  three letters, Potts pair at slope s=0.3: uniform weights do NOT maximise I (two letters do better)",
      two > uni3 * 1.05 and best <= two + 1e-9,
      "I(uniform on 3) = %.6f, I(uniform on 2 letters) = %.6f, best random = %.6f" % (uni3, two, best))

print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
