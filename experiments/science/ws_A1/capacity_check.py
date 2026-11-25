#!/usr/bin/env python3
"""Workstream A1 -- the non-adaptive exponent at bounded accuracy as a channel capacity / minimax redundancy.

Setting (theory report sect. 11.20): reference pi = Bernoulli(p)^n on {0,1}^n (P(x_i = 1) = p), slope u.
The cone u*d_H(., s) around a centre s has the product Gibbs law  W^n(.|s),  W(x|b) ~ pi(x) e^{-u [x != b]},
i.e. the family of cone laws is the family of output laws of a MEMORYLESS CHANNEL  s_i -> x_i.

Claims checked here (all [K] in substance: capacity = information radius, Gallager 1968 Thm 4.5.1 / Csiszar-Koerner;
redundancy-capacity theorem; their use for the theory report's formulas is my remark):
  C1  a(p,u) := max_m I(S;X)  (theory report Thm 11.59(c): 'a = max_m I_{pi_s}(S;X)')  equals the channel capacity
      and equals the information radius  min_r max_b D(W(.|b) || Bern(r))  -- so at vanishing accuracy the best single
      PRODUCT proposal Bern(r*)^n, r* the capacity-achieving output law, has worst-case KL exponent exactly a;
      r* != p when p != 1/2 (the optimal product proposal is not the Gibbs measure of the known part);
  C2  uniform cube (p = 1/2):  a = ln 2 - h(p_u) = KL(p_u || 1/2) = capacity of BSC(p_u), r* = 1/2;
  C3  plain Monte Carlo from pi itself: worst-case KL exponent max_b D(W(.|b) || Bern(p)) > a; ratio reported;
  C4  finite n: for the type-uniform ('flat-histogram') mixture mu_H(x) = 1/((n+1) C(n,|x|)) and a centre of type m,
      KL(W^n(.|s) || mu_H)/n -> I_m(S;X) (exact computation by convolution of two binomials), so the flat histogram
      attains max_m I = a as well -- it is the universal (mixture) proposal; at bounded accuracy it ties with Bern(r*)^n;
  C5  mutation: with r = p in place of r* the 'information radius' exceeds the capacity (detected).
Run: python3 capacity_check.py   (a few seconds)
"""
import math
import sys

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gammaln, logsumexp

fails = 0


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    if not ok:
        fails += 1


def h(p):
    return 0.0 if p <= 0 or p >= 1 else -p * math.log(p) - (1 - p) * math.log1p(-p)


def kl(a, b):
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out


def channel(p, u):
    """a_b = P(X = 1 | S = b) for the cone channel: weight pi(x) e^{-u [x != b]}"""
    q = 1 - p
    a1 = p / (p + q * math.exp(-u))
    a0 = p * math.exp(-u) / (q + p * math.exp(-u))
    return a0, a1


def mutual_info(m, a0, a1):
    return h(m * a1 + (1 - m) * a0) - m * h(a1) - (1 - m) * h(a0)


def capacity(p, u):
    a0, a1 = channel(p, u)
    res = minimize_scalar(lambda m: -mutual_info(m, a0, a1), bounds=(1e-9, 1 - 1e-9), method="bounded",
                          options={"xatol": 1e-13})
    m = res.x
    return -res.fun, m, m * a1 + (1 - m) * a0


def info_radius(p, u):
    a0, a1 = channel(p, u)
    f = lambda r: max(kl(a0, r), kl(a1, r))
    res = minimize_scalar(f, bounds=(min(a0, a1) + 1e-12, max(a0, a1) - 1e-12), method="bounded",
                          options={"xatol": 1e-13})
    return res.fun, res.x


rows = []
ok1 = ok3 = True
worst_ratio = 0.0
for (p, u) in ((0.1, 2.0), (0.3, 1.0), (0.1, 1.0), (0.05, 3.0), (0.4, 0.5), (0.5, 1.0)):
    C, mstar, rstar = capacity(p, u)
    R, rr = info_radius(p, u)
    a0, a1 = channel(p, u)
    plain = max(kl(a0, p), kl(a1, p))
    ok1 &= abs(C - R) < 1e-8 and abs(rstar - rr) < 1e-5
    ok3 &= plain >= C - 1e-12
    worst_ratio = max(worst_ratio, plain / C)
    rows.append("(p,u)=(%.2f,%.1f): a=C=%.5f, radius=%.5f, m*=%.3f, r*=%.4f (p=%.2f), plainMC/a=%.2f"
                % (p, u, C, R, mstar, rstar, p, plain / C))
check("C1  max_m I(S;X) = min_r max_b D(W_b || Bern(r))  (capacity = information radius); r* is the optimal product proposal",
      ok1, "\n      " + "\n      ".join(rows))
C, mstar, rstar = capacity(0.5, 1.0)
pu = 1 / (1 + math.e)
check("C2  uniform cube: a = ln2 - h(p_u) = KL(p_u||1/2), m* = r* = 1/2",
      abs(C - (math.log(2) - h(pu))) < 1e-10 and abs(mstar - 0.5) < 1e-5 and abs(rstar - 0.5) < 1e-5,
      "a = %.6f" % C)
check("C3  plain MC from the Gibbs measure of the known part (r = p) is worse than a whenever p != 1/2", ok3,
      "largest ratio among the examples: %.2f" % worst_ratio)


# ------------------------------------------------------------------ C4 finite n
def kl_cone_vs_flat(n, p, u, m):
    """exact KL( W^n(.|s) || mu_H ) for a centre with round(m n) ones; mu_H = uniform over types, uniform inside."""
    a0, a1 = channel(p, u)
    n1 = int(round(m * n))
    n0 = n - n1

    def logbin(N, a):
        k = np.arange(N + 1)
        with np.errstate(divide="ignore"):
            return gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1) + k * math.log(a) + (N - k) * math.log1p(-a)

    l1, l0 = logbin(n1, a1), logbin(n0, a0)
    # law of |x| = Bin(n1,a1) + Bin(n0,a0): convolution in log space
    lt = np.full(n + 1, -np.inf)
    for k1 in range(n1 + 1):
        seg = l1[k1] + l0
        lt[k1:k1 + n0 + 1] = np.logaddexp(lt[k1:k1 + n0 + 1], seg)
    pt = np.exp(lt)
    t = np.arange(n + 1)
    logC = gammaln(n + 1) - gammaln(t + 1) - gammaln(n - t + 1)
    entropy_cone = n1 * h(a1) + n0 * h(a0)
    # KL = -H(cone) - E ln mu_H(x) = -H(cone) + ln(n+1) + E ln C(n,|x|)
    return (-entropy_cone + math.log(n + 1) + float((pt * logC).sum())) / n


ok4 = True
rows = []
for (p, u) in ((0.1, 2.0), (0.3, 1.0)):
    C, mstar, _ = capacity(p, u)
    a0, a1 = channel(p, u)
    vals = [kl_cone_vs_flat(n, p, u, mstar) for n in (200, 800, 3200)]
    # worst centre type on a grid at n = 800
    worst = max(kl_cone_vs_flat(800, p, u, m) for m in np.linspace(0.02, 0.98, 49))
    rows.append("(p,u)=(%.1f,%.0f): KL(cone_{m*}||mu_H)/n = %.5f, %.5f, %.5f (n=200,800,3200) -> a=%.5f; max over centre types at n=800: %.5f"
                % (p, u, vals[0], vals[1], vals[2], C, worst))
    ok4 &= abs(vals[-1] - C) < 3e-3 and worst < C + 6e-3
check("C4  the flat-histogram mixture has worst-case KL exponent -> a  (exact finite-n computation)", ok4,
      "\n      " + "\n      ".join(rows))

# ------------------------------------------------------------------ C5 mutation
C, _, _ = capacity(0.1, 2.0)
a0, a1 = channel(0.1, 2.0)
mut = max(kl(a0, 0.1), kl(a1, 0.1))
check("C5  mutation detected: r = p instead of r* gives a radius above the capacity", mut > C * 1.5,
      "radius at r=p: %.4f against a = %.4f" % (mut, C))

print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
