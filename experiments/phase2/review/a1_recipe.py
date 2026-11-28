#!/usr/bin/env python3
"""a1_recipe.py -- referee A1: constants, the function hbar, the table of section 2.3, the
elementary inequalities in the proof of Corollary A', the recipe of that proof evaluated at
finite n in log-space, and the degenerate corner delta > 1/2 of Theorem A'.

Written from docs/phase2/PHASE2_REPORT.md (sections 1, 2.3) only; nothing imported from the repo.

    p_u = 1/(1+e^u),  a = KL(p_u || 1/2),  rho0 = ln(2/(1+e^-u))/u,  h = KL(rho0 || 1/2),
    ell = ln((1-rho0)/rho0)/u,   hbar(lam) = KL(rho0 - lam/u || 1/2) - lam,
    m_r = 2^-n sum_{j<r} C(n,j) (e^{u(r-j)} - 1),   V(n,r-1) = sum_{j<r} C(n,j).

Recipe (proof of Corollary A'):  r = largest radius with C (2 e^eps - 1) m_r ln(2M/eta) <= tau^2,
L = ceil(2 (e^eps - 1)/m_r), tau = e^{-gamma n};  claimed: the hypotheses of Theorem A' hold and
n^-1 ln(2^n/(L V(n,r-1))) -> hbar(2 gamma + beta), eta'' = L V(n,r-1)/2^n -> 0.
C = 8 in the text that was reviewed (commit 67956b7; parts E, F); C = 2 in the text as revised after the
review (commit ddae0c3; part E2).
"""
import math
import sys
import numpy as np
from scipy.special import gammaln, logsumexp
import mpmath as mp

mp.mp.dps = 40
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
    return "ok" if cond else "FAIL"


# ---------------------------------------------------------------- constants and hbar (mpmath)
def consts(u):
    u = mp.mpf(u)
    p = 1 / (1 + mp.e ** u)
    KLhalf = lambda x: mp.log(2) + x * mp.log(x) + (1 - x) * mp.log(1 - x)
    a = KLhalf(p)
    rho0 = mp.log(2 / (1 + mp.e ** (-u))) / u
    h = KLhalf(rho0)
    ell = mp.log((1 - rho0) / rho0) / u
    return dict(u=u, p=p, a=a, rho0=rho0, h=h, ell=ell, KLhalf=KLhalf)


def hbar(c, lam):
    return c["KLhalf"](c["rho0"] - lam / c["u"]) - lam


def part_A():
    print("== A. constants (40 digits, printed to 9) ==")
    for u in (0.5, 1, 2):
        c = consts(u)
        kl_pu = c["rho0"] * mp.log(c["rho0"] / c["p"]) + (1 - c["rho0"]) * mp.log((1 - c["rho0"]) / (1 - c["p"]))
        ok = check(abs(c["rho0"] - (c["p"] + c["a"] / c["u"])) < 1e-30 and abs(c["h"] - kl_pu) < 1e-30
                   and 0 < c["ell"] < 1 and c["p"] < c["rho0"] < 0.5, "constants identities u=%s" % u)
        print("   u=%-4s p_u=%.9f a=%.9f rho0=%.9f h=%.9f ell=%.9f 1-ell=%.9f | rho0=p_u+a/u, h=KL(rho0||p_u), 0<ell<1, p_u<rho0<1/2: %s"
              % (u, c["p"], c["a"], c["rho0"], c["h"], c["ell"], 1 - c["ell"], ok))
    c = consts(1)
    rep = dict(a=0.110944, rho0=0.379885, h=0.029139, ell=0.4900)
    for k, v in rep.items():
        d = abs(float(c[k]) - v)
        print("   report (u=1): %s = %s, referee %.9f  %s" % (k, v, float(c[k]), check(d < 0.6 * 10 ** (-len(str(v).split(".")[1])), "const " + k)))
    print("   a/2 = %.6f (report 0.0555, 0.05547)   h/2 = %.6f (report 0.01457)   1-ell = %.6f (report 0.5100)" % (
        float(c["a"] / 2), float(c["h"] / 2), float(1 - c["ell"])))


def part_B():
    print("== B. properties of hbar on [0, a] (grid of 2001 points, 40 digits) ==")
    for u in (0.5, 1, 2):
        c = consts(u)
        a = c["a"]
        G = 2000
        lam = [a * k / G for k in range(G + 1)]
        hb = [hbar(c, l) for l in lam]
        dec = all(hb[k + 1] < hb[k] for k in range(G))
        conv = all(hb[k + 1] - 2 * hb[k] + hb[k - 1] > 0 for k in range(1, G))
        pos = all(hb[k] > 0 for k in range(G))
        tang = all(hb[k] >= c["h"] - (1 - c["ell"]) * lam[k] - mp.mpf(10) ** (-35) for k in range(G + 1))
        thmA = all(c["h"] - (1 - c["ell"]) * lam[k] >= c["h"] - lam[k] for k in range(G + 1))
        d1 = lambda l: mp.log((1 - (c["rho0"] - l / c["u"])) / (c["rho0"] - l / c["u"])) / c["u"] - 1
        d2 = lambda l: 1 / (c["u"] ** 2 * (c["rho0"] - l / c["u"]) * (1 - (c["rho0"] - l / c["u"])))
        errs1 = max(abs(mp.diff(lambda l: hbar(c, l), l0) - d1(l0)) for l0 in (a / 7, a / 2, 0.9 * a))
        errs2 = max(abs(mp.diff(lambda l: hbar(c, l), l0, 2) - d2(l0)) for l0 in (a / 7, a / 2, 0.9 * a))
        ends = (abs(hb[0] - c["h"]) < 1e-30 and abs(hb[-1]) < 1e-30 and abs(d1(a)) < 1e-30
                and abs(d1(0) + (1 - c["ell"])) < 1e-30)
        st = check(dec and conv and pos and tang and thmA and ends and errs1 < 1e-25 and errs2 < 1e-20, "hbar properties u=%s" % u)
        print("   u=%-4s decreasing %s, convex %s, >0 on [0,a) %s, hbar>=h-(1-ell)lam>=h-lam %s, hbar(0)=h & hbar(a)=0 & hbar'(a)=0 & hbar'(0)=-(1-ell) %s,"
              " formulas for hbar', hbar'' (max err %.0e, %.0e)  %s" % (u, dec, conv, pos, tang and thmA, ends, float(errs1), float(errs2), st))
    c = consts(1)
    # consistency with the upper bound of the table and the old side condition
    up_ok = all(hbar(c, 2 * g) <= (1 - g / mp.log(2)) * c["h"] + mp.mpf(10) ** (-35) for g in [c["a"] / 2 * k / 400 for k in range(401)])
    g_old = mp.findroot(lambda g: hbar(c, 2 * g) - g, (mp.mpf('0.01'), mp.mpf('0.02')), solver='bisect')
    print("   u=1: hbar(2g) <= (1-g/ln2) h on [0, a/2]: %s;  old side condition hbar(2g) > g holds up to g = %.6f (Note: 0.0154)" % (
        check(up_ok, "lower<=upper"), float(g_old)))


def part_C():
    print("== C. the table after Corollary A' (u = 1, beta = 0) ==")
    c = consts(1)
    rows = [("0", 0.0, 0.029139, 0.029139, 0.029139), ("0.002", 0.002, 0.025139, 0.027133, 0.029055),
            ("0.005", 0.005, 0.019139, 0.024252, 0.028929), ("0.010", 0.010, 0.009139, 0.019795, 0.028719),
            ("0.0145", 0.0145, 0.000139, 0.016154, 0.028530), ("0.020", 0.020, None, 0.012188, 0.028298),
            ("0.030", 0.030, None, 0.006364, 0.027878), ("0.040", 0.040, None, 0.002380, 0.027458),
            ("0.050", 0.050, None, 0.000302, 0.027037), ("a/2", float(c["a"] / 2), None, 0.0, 0.026807)]
    print("   %-7s | %-22s | %-22s | %-22s" % ("gamma", "h-2g: report / referee", "hbar(2g): report / ref", "(1-g/ln2)h: report / ref"))
    for nm, g, c1, c2, c3 in rows:
        gm = c["a"] / 2 if nm == "a/2" else mp.mpf(str(g))
        v1 = c["h"] - 2 * gm
        v2 = hbar(c, 2 * gm)
        v3 = (1 - gm / mp.log(2)) * c["h"]
        ok = (c1 is None and v1 < 0 or c1 is not None and abs(float(v1) - c1) < 5.1e-7) and abs(float(v2) - c2) < 5.1e-7 and abs(float(v3) - c3) < 5.1e-7
        print("   %-7s | %-9s / %+.6f  | %.6f / %.6f   | %.6f / %.6f   %s" % (
            nm, "-" if c1 is None else "%.6f" % c1, float(v1), c2, float(v2), c3, float(v3), check(ok, "table row " + nm)))
    print("   hbar(0.09) = %.6f (brief: 0.001104)" % float(hbar(c, mp.mpf("0.09"))))


# ---------------------------------------------------------------- log-space sums
def ln_binom(n, j):
    return gammaln(n + 1.0) - gammaln(j + 1.0) - gammaln(n - j + 1.0)


def ln_m(n, u, r):
    """ln m_r"""
    j = np.arange(0, min(r, n + 1), dtype=np.float64)
    k = r - j
    return float(logsumexp(ln_binom(n, j) + u * k + np.log1p(-np.exp(-u * k)))) - n * math.log(2.0)


def ln_V(n, r):
    """ln V(n, r-1) = ln sum_{j<r} C(n,j)"""
    j = np.arange(0, min(r, n + 1), dtype=np.float64)
    return float(logsumexp(ln_binom(n, j)))


def m_exact(n, u, r):
    """m_r with 40 digits (small n)"""
    u = mp.mpf(u)
    return sum(mp.binomial(n, j) * (mp.e ** (u * (r - j)) - 1) for j in range(min(r, n + 1))) / mp.mpf(2) ** n


def part_D():
    print("== D. elementary steps in the proof of Corollary A' ==")
    # term by term
    worst = mp.mpf(0)
    for u in (0.01, 0.1, 0.5, 1, 2, 5):
        for k in range(1, 60):
            lhs = mp.e ** (mp.mpf(u) * (k + 1)) - 1
            rhs = (mp.e ** mp.mpf(u) + 1) * (mp.e ** (mp.mpf(u) * k) - 1)
            worst = max(worst, lhs / rhs)
    print("   e^{u(k+1)}-1 <= (e^u+1)(e^{uk}-1), k>=1: max lhs/rhs = %.12f %s (equality at k = 1)" % (float(worst), check(worst <= 1 + mp.mpf(10) ** (-30), "term by term")))
    worst = mp.mpf(0)
    arg = None
    mono = True
    small = True
    for u in (0.05, 0.5, 1, 2, 5):
        for n in (1, 2, 3, 5, 8, 13, 21, 34, 55, 80):
            prev = None
            for r in range(1, n + 4):
                m0 = m_exact(n, u, r)
                m1 = m_exact(n, u, r + 1)
                q = m1 / ((mp.e ** mp.mpf(u) + 1 + n) * m0)
                if q > worst:
                    worst, arg = q, (u, n, r)
                mono = mono and (m1 > m0)
    print("   m_{r+1} <= (e^u+1+n) m_r for u in {.05,.5,1,2,5}, n <= 80, 1 <= r <= n+3: max ratio %.6f at (u,n,r)=%s %s (equality at r = 1 for every n: m_2 = (e^u+1+n) m_1);  m_r strictly increasing: %s"
          % (float(worst), arg, check(worst <= 1 + mp.mpf(10) ** (-30), "m_{r+1} bound"), check(mono, "monotone m_r")))
    # log-space code against exact sums
    err = 0.0
    for (n, u, r) in ((40, 1.0, 9), (80, 0.5, 30), (60, 2.0, 5), (55, 1.0, 1)):
        err = max(err, abs(ln_m(n, u, r) - float(mp.log(m_exact(n, u, r)))),
                  abs(ln_V(n, r) - float(mp.log(sum(mp.binomial(n, j) for j in range(r))))))
    print("   log-space ln m_r, ln V against 40-digit sums (n <= 80): max error %.1e %s" % (err, check(err < 1e-10, "log-space code")))
    # asymptotics of section 1
    c = consts(1)
    print("   section 1 asymptotics, u = 1 (p_u = %.4f, rho0 = %.4f):  n^-1 ln m_r -> u(rho - rho0),  n^-1 ln(2^n/V(n,r)) -> KL(rho||1/2)" % (float(c["p"]), float(c["rho0"])))
    for rho in (0.29, 0.32, 0.36):
        line = "      rho=%.2f: limits %+.6f, %.6f;" % (rho, rho - float(c["rho0"]), float(c["KLhalf"](mp.mpf(rho))))
        for n in (1000, 10000, 100000, 1000000):
            r = int(round(rho * n))
            line += "  n=%d: %+.6f, %.6f" % (n, ln_m(n, 1.0, r) / n, math.log(2.0) - ln_V(n, r + 1) / n)
        print(line)


# ---------------------------------------------------------------- the recipe at finite n
def recipe(n, u, gamma, eps, lnln, cst=8.0):
    """lnln = ln ln(2M/eta); cst = the constant C in  C R m_r ln(2M/eta) <= tau^2  (8: the text reviewed; 2: the
    text as revised after the review).  Everything in logarithms.  R = L m_r lies in [2(e^eps-1), 2(e^eps-1)+m_r]
    by the choice of L (ceiling); the second hypothesis of Theorem A' is checked with the upper end."""
    ln_tau2 = -2.0 * gamma * n
    lnT = ln_tau2 - math.log(cst * (2.0 * math.exp(eps) - 1.0)) - lnln       # the condition is  m_r <= T
    if ln_m(n, u, 1) > lnT:
        return None
    lo, hi = 1, n + 2                      # invariant: ln m_lo <= lnT < ln m_hi
    while ln_m(n, u, hi) <= lnT:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ln_m(n, u, mid) <= lnT:
            lo = mid
        else:
            hi = mid
    r = lo
    lm = ln_m(n, u, r)
    x = math.log(2.0 * math.expm1(eps)) - lm            # ln(2(e^eps-1)/m_r)
    if x < 30:
        Lval = math.ceil(math.exp(x) * (1 - 1e-15))
        lnL = math.log(Lval)
        R_lo = Lval * math.exp(lm)
    else:
        lnL = x                                          # the ceiling changes ln L by less than e^-30
        R_lo = 2.0 * math.expm1(eps)
    m_r = math.exp(lm) if lm > -700 else 0.0
    R_up = 2.0 * math.expm1(eps) + m_r
    lv = ln_V(n, r)
    expo = math.log(2.0) - (lnL + lv) / n
    hypB_margin = ln_tau2 - (math.log(cst) + math.log(R_up) + lm + lnln)     # >= 0 required
    return dict(r=r, ln_m=lm, lnL=lnL, R=R_lo, m_lt_1=lm < 0, hypA=R_lo >= 2.0 * math.expm1(eps) * (1 - 1e-12),
                hypB_margin=hypB_margin, R_hi=R_up <= 2 * math.exp(eps) - 1 + 1e-12,
                expo=expo, ln_eta2=-n * expo, ln_eta_old=math.log(5.0 * R_lo / 2.0) + gamma * n - n * expo)


def part_E():
    print("== E. the recipe of Corollary A' at finite n (u = 1; log-space; eta = 0.1, delta = 0.1) ==")
    c = consts(1)
    u = 1.0
    eta, delta = 0.1, 0.1
    print("   hyp = [R >= 2(e^eps-1) by the ceiling] and [8 R m_r ln(2M/eta) <= tau^2, checked with R <= 2(e^eps-1)+m_r] and [m_r < 1] and [R <= 2e^eps-1];")
    print("   expo = n^-1 ln(2^n/(L V(n,r-1)));  bound = n^-1 ln[(1-2delta)(1-eta-eta'') 2^n/(L V)];  eta'(old) = (5 L m_r/(2 tau)) L V/2^n of the first version")
    for (gamma, beta, label) in ((0.01, 0.0, "M=1"), (0.02, 0.0, "M=1"), (0.03, 0.0, "M=1"), (0.045, 0.0, "M=1"), (0.05, 0.0, "M=1"),
                                 (0.005, 0.0, "M=100"), (0.03, 0.0, "M=100"), (0.045, 0.0, "M=100"),
                                 (0.03, 0.0, "M=2^n"), (0.045, 0.0, "M=2^n"), (0.01, 0.02, "lnlnM=beta*n"), (0.02, 0.05, "lnlnM=beta*n")):
        lam = 2 * gamma + beta
        hb = float(hbar(c, mp.mpf(str(lam))))
        print("   gamma=%.3f beta=%.3f (%s): lambda=%.3f, hbar(lambda)=%.6f, rho0-lambda/u=%.6f%s" % (
            gamma, beta, label, lam, hb, float(c["rho0"]) - lam, "   [first version void: hbar(lambda) <= gamma]" if hb <= gamma else ""))
        for eps in (0.1, 1.0):
            for n in (2000, 20000, 200000, 2000000):
                if label == "M=1":
                    lnln = math.log(math.log(2.0 / eta))
                elif label == "M=100":
                    lnln = math.log(math.log(2.0 * 100 / eta))
                elif label == "M=2^n":
                    lnln = math.log(math.log(2.0 / eta) + n * math.log(2.0))
                else:   # ln M = e^{beta n}:  ln ln(2M/eta) = beta n + log1p(ln(2/eta) e^{-beta n})
                    lnln = beta * n + math.log1p(math.log(2.0 / eta) * math.exp(-beta * n))
                res = recipe(n, u, gamma, eps, lnln)
                if res is None:
                    print("      eps=%.1f n=%-8d: no radius r >= 1 satisfies the condition" % (eps, n))
                    continue
                hyp = res["hypA"] and res["hypB_margin"] >= -1e-9 and res["m_lt_1"] and res["R_hi"]
                check(hyp, "recipe hypotheses gamma=%s beta=%s %s n=%d eps=%s" % (gamma, beta, label, n, eps))
                eta2 = math.exp(res["ln_eta2"]) if res["ln_eta2"] < 50 else float("inf")
                if eta + eta2 < 1:
                    fin_s = "%.6f" % ((math.log(1 - 2 * delta) + math.log(1 - eta - eta2) - res["ln_eta2"]) / n)
                else:
                    fin_s = "void    "
                print("      eps=%.1f n=%-8d: r/n=%.6f ln m_r/n=%+.6f ln L/n=%.6f R=%.4f hyp %s (margin %.2f) | expo %.6f = hbar %+.6f | ln eta''=%10.2f | bound %s | ln eta'(old)=%+.1f"
                      % (eps, n, res["r"] / n, res["ln_m"] / n, res["lnL"] / n, res["R"], "ok" if hyp else "FAIL", res["hypB_margin"],
                         res["expo"], res["expo"] - hb, res["ln_eta2"], fin_s, res["ln_eta_old"]))


def part_E2():
    print("== E2. the same recipe with the constant 2 (text as revised after this review: 2 R m_r ln(2M/eta) <= tau^2;")
    print("       radius = largest r with 2 (2e^eps - 1) m_r ln(2M/eta) <= tau^2);  u = 1, eps = 1, eta = 0.1 ==")
    c = consts(1)
    for (gamma, label, M) in ((0.005, "M=100", 100), (0.03, "M=100", 100), (0.045, "M=100", 100), (0.03, "M=1", 1), (0.045, "M=1", 1), (0.05, "M=1", 1)):
        hb = float(hbar(c, mp.mpf(str(2 * gamma))))
        lnln = math.log(math.log(2.0 * M / 0.1))
        line = "   gamma=%.3f %-6s hbar(2 gamma)=%.6f:" % (gamma, label, hb)
        for n in (2000, 20000, 200000, 2000000):
            res = recipe(n, 1.0, gamma, 1.0, lnln, cst=2.0)
            hyp = res["hypA"] and res["hypB_margin"] >= -1e-9 and res["m_lt_1"] and res["R_hi"]
            check(hyp, "recipe (constant 2) hypotheses gamma=%s %s n=%d" % (gamma, label, n))
            line += "  n=%d: expo %.6f, ln eta''=%.1f, ln eta'(old)=%+.1f, hyp %s;" % (n, res["expo"], res["ln_eta2"], res["ln_eta_old"], "ok" if hyp else "FAIL")
        print(line)


# ---------------------------------------------------------------- the corner delta > 1/2
def part_F():
    print("== F. degenerate corner: delta > 1/2 together with eta + eta'' > 1  (the statement of commit 67956b7, which had no")
    print("      restriction on delta; the revised text assumes delta <= 1/2.  With the revised constant 2 the same example works.) ==")
    n, u, r, L, eps, tau, M, eta = 4, 0.1, 1, 16, 0.05, 1.0, 1, 0.5
    m_r = math.expm1(u) / 2 ** n
    V = 1
    R = L * m_r
    eta2 = L * V / 2 ** n
    h1 = R >= 2 * math.expm1(eps)
    h2 = 8 * R * m_r * math.log(2 * M / eta) <= tau ** 2
    print("   n=%d u=%g r=%d L=%d eps=%g tau=%g M=%d eta=%g: m_r=%.6f R=%.6f >= 2(e^eps-1)=%.6f: %s;  8 R m_r ln(2M/eta)=%.5f <= tau^2: %s;  eta''=%g"
          % (n, u, r, L, eps, tau, M, eta, m_r, R, 2 * math.expm1(eps), h1, 8 * R * m_r * math.log(2 * M / eta), h2, eta2))
    # an (eps/2, delta)-correct algorithm with E|Q| = K (1 - delta):  with probability p = K(1-delta) evaluate w(x0)
    # and output ln w(x0) + a uniformly chosen point of a grid of K = ceil(n u/eps) points of mesh eps covering
    # [n ln((1+e^-u)/2), n ln((1+e^u)/2)] (length n u, which contains ln A(w) - ln w(x0) for every admissible w);
    # otherwise output 0 without any evaluation.  Success probability >= p/K = 1 - delta on the whole class.
    K = math.ceil(n * u / eps - 1e-12)
    lo_i, hi_i = n * math.log((1 + math.exp(-u)) / 2), n * math.log((1 + math.exp(u)) / 2)
    print("   interval for ln A(w) - ln w(x0): [%.5f, %.5f], length %.5f = n u = %.5f;  grid of K = %d points of mesh eps" % (lo_i, hi_i, hi_i - lo_i, n * u, K))
    # numerical sanity check of the interval on random admissible weights (inf-convolutions of random functions)
    rng = np.random.default_rng(7)
    N = 1 << n
    xs = np.arange(N)
    D = np.array([[bin(a ^ b).count("1") for b in range(N)] for a in range(N)])
    worst_lo, worst_hi = float("inf"), -float("inf")
    for _ in range(4000):
        g = rng.normal(0, rng.choice([0.05, 0.3, 3.0]), size=N)
        psi = (g[None, :] + u * D).min(axis=1)                 # u-Lipschitz
        assert np.all(np.abs(psi[:, None] - psi[None, :]) <= u * D + 1e-12)
        w = np.exp(-psi)
        d = math.log(w.mean()) - math.log(w[0])
        worst_lo, worst_hi = min(worst_lo, d), max(worst_hi, d)
    for sgn in (+1, -1):                                        # the two extreme weights
        w = np.exp(sgn * u * D[0])
        d = math.log(w.mean()) - math.log(w[0])
        worst_lo, worst_hi = min(worst_lo, d), max(worst_hi, d)
    print("   4002 admissible weights: ln A(w) - ln w(x0) in [%.5f, %.5f] %s" % (
        worst_lo, worst_hi, check(worst_lo >= lo_i - 1e-12 and worst_hi <= hi_i + 1e-12, "interval")))
    for delta in (0.96, 0.99, 1.0):
        p = K * (1 - delta)
        claimed = (1 - 2 * delta) * (1 - eta - eta2) / eta2
        print("   delta=%.2f: algorithm with E|Q| = K(1-delta) = %.3f is (eps/2, delta)-correct;  displayed bound (1-2delta)(1-eta-eta'')2^n/(L V) = %.3f  -> %s"
              % (delta, p, claimed, "DISPLAYED INEQUALITY FAILS" if p < claimed else "holds"))
    print("   (for delta <= 1/2 the bound is <= 0 whenever eta + eta'' >= 1, as the report says; the corner needs delta > 1/2)")


def main():
    print("a1_recipe.py -- referee A1")
    part_A()
    print()
    part_B()
    print()
    part_C()
    print()
    part_D()
    print()
    part_E()
    print()
    part_E2()
    print()
    part_F()
    print()
    print("failed checks: %d" % len(FAILS))
    for f in FAILS:
        print("   FAIL: " + f)


if __name__ == "__main__":
    main()
