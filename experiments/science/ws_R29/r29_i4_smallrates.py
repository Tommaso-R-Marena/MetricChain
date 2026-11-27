#!/usr/bin/env python3
"""r29_i4_smallrates.py [u] [KMAX]  --  Z_ADDENDUM A9/A9a (Lemma A9, Lemma A9', Proposition A11'): numerics with my own code.

 (A) The contraction factor of the orbits.  For B < h the map s -> Sigma(B, s) is convex with the stable fixed point
     t1(B) (J(t1) = B, t1 <= L) and derivative there  kappa(B) = 1 - J'/(B + (1 - t1) J'),  J' = J'(t1(B))  (re-derived;
     checked here against a difference quotient of my slope map).  Lemma A9:  kappa(B) <= lambda_eta = hL/(hL + eta)
     for B <= h - eta.  Lemma A9':  kappa(B) <= mu_eta = h/(h + sqrt(eta/vartheta)/2) for B <= h - eta, eta <= eta_0.
     Tested on a logarithmic grid of eta; the largest eta_0 for which A9' holds on the grid is reported, and the
     orbit bound  t1 - p_i <= t1 kappa^i  itself on a sample.
 (B) The defect D_k(g) = M_{W_k, b_k}(g) - theta_hint(g) of the envelope sequence (my semi-analytic envelope, doubles)
     at small rates g: its decay ratio D_{k+1}/D_k against  kappa_g = 1 - g/(J(t_g) + (1 - t_g) g), J'(t_g) = g  (the
     "true" rate of the addendum, e^{-g/h} to first order)  and against the PROVED rate mu_g = 1/(1 + g/(48h))
     (Proposition A11': D_k <= g mu_g^{k - k_2(g)} for k >= k_2(g), k_2(g) <= C_3/g).  For each rate: the least k_2
     for which the proved bound holds at all computed k >= k_2, and g*k_2 (must stay bounded as g -> 0).
 Controls (must fail): (A) a factor below the true multiplier, kappa(h - eta)^2, as a bound of the orbit;
     (B) the proved form with the rate kappa_g^2 (faster than the truth) and the same k_2.
"""
import math
import sys

import numpy as np

import r29lib as R
import r29env as E

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 400
P = E.CubeF(u)
a, h, L, es, vth = P.a, P.h, P.L, P.estar, P.thpp


def J(t):
    return P.J(t)


def Jp(t):
    return u / (1.0 + math.exp(t * u)) - P.lam1


def t1_of(B):
    lo, hi = 0.0, L
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if J(mid) < B:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kappa(B):
    t = t1_of(B)
    jp = Jp(t)
    return 1.0 - jp / (B + (1.0 - t) * jp)


def th_hint(x):
    r_ = (P.lam1 + x) / P.u
    return 0.0 if r_ >= 0.5 else E.CubeF.kl(r_, 0.5)


print("# cube u = %g: h = %.12f, L = %.9f, theta_hint''(0) = vartheta = %.9f, eps* = %.9f" % (u, h, L, vth, es))
# ---- (A)
# the multiplier against a difference quotient of the slope map
wq = 0.0
for B in (0.3 * h, 0.7 * h, 0.95 * h, 0.999 * h):
    t = t1_of(B)
    d = 1e-6
    dq = (P.Sigma(B, t) - P.Sigma(B, t - d)) / d
    wq = max(wq, abs(dq - kappa(B)))
print("(A) derivative of s -> Sigma(B, s) at the fixed point against the formula kappa(B): largest difference %.2e (difference quotient, step 1e-6)" % wq)
etas = np.geomspace(1e-9, 0.999, 400) * h
vA = vA2 = 0
eta0 = None
mono_bad = 0
prev = None
for eta in etas:
    k = kappa(h - eta)
    lam = h * L / (h * L + eta)
    mu = h / (h + 0.5 * math.sqrt(eta / vth))
    if k > lam * (1 + 1e-12):
        vA += 1
    if k > mu * (1 + 1e-12):
        vA2 += 1
        if eta0 is None:
            eta0 = eta
    if prev is not None and k > prev + 1e-12:          # kappa(h - eta) must decrease as eta grows (kappa increasing in B)
        mono_bad += 1
    prev = k
print("    Lemma A9 : kappa(h - eta) <= hL/(hL + eta) on 400 values of eta in [1e-9 h, h): %d violations;  kappa(B) not monotone in B: %d cases" % (vA, mono_bad))
print("    Lemma A9': kappa(h - eta) <= h/(h + sqrt(eta/vartheta)/2): %d violations on the grid; first failure at eta = %s  (so eta_0 %s)"
      % (vA2, ("%.4f h" % (eta0 / h)) if eta0 else "none", (">= %.4f h on this grid" % (eta0 / h)) if eta0 else "= h: no restriction is needed for this pair"))
for eta in (1e-6 * h, 1e-4 * h, 1e-2 * h):
    k = kappa(h - eta)
    print("      eta = %.0e h: kappa = %.9f;  1 - kappa = %.3e;  sqrt(2 eta/vartheta)/h = %.3e (asymptotic value);  A9' allows 1 - mu = %.3e;  A9 allows %.3e"
          % (eta / h, k, 1 - k, math.sqrt(2 * eta / vth) / h, 1 - h / (h + 0.5 * math.sqrt(eta / vth)), eta / (h * L + eta)))
# the orbit bound itself, and the control
vo = vc = no = 0
for eta in (0.3 * h, 0.05 * h, 0.005 * h):
    for frac in (1.0, 0.5, 0.1):
        B = (h - eta) * frac
        t = t1_of(B)
        kB = kappa(B)
        kbad = kappa(h - eta) ** 2
        mu = h / (h + 0.5 * math.sqrt(eta / vth))
        lam = h * L / (h * L + eta)
        s = 0.0
        for i in range(0, 400):
            no += 1
            gap = t - s
            if gap > t * lam ** i * (1 + 1e-9) + 1e-15 or gap > t * mu ** i * (1 + 1e-9) + 1e-15:
                vo += 1
            if gap > t * kbad ** i * (1 + 1e-9) + 1e-15:
                vc += 1
            s = P.Sigma(B, s)
print("    orbits: t1 - p_i <= t1 lambda_eta^i and <= t1 mu_eta^i for B <= h - eta (9 orbits x 400 steps): %d violations of %d;" % (vo, no))
print("    control (factor kappa(h - eta)^2, below the true multiplier): %d violations  [must be > 0]" % vc)

# ---- (B)
env = E.EnvSA(P, KMAX)
print("(B) envelope sequence to %d levels (semi-analytic, doubles): b_%d - h = %.6e, k^2 (b_k - h)/c_*^2 = %.5f" % (KMAX, KMAX, env.b[KMAX] - h, KMAX ** 2 * (env.b[KMAX] - h) / P.cs2))
ctrl_fail = 0
allok = True
gk2 = []
for q in (0.02, 0.05, 0.1, 0.25, 1.0):
    g = q * h
    rho_g = (P.lam1 + g) / u
    tg = math.log((1 - rho_g) / rho_g) / u
    kap_g = 1 - g / (J(tg) + (1 - tg) * g)
    mu_g = 1 / (1 + g / (48 * h))
    D = [None]
    for k in range(1, KMAX + 1):
        D.append(float(env.M(k, g)) - th_hint(g))
    D = np.array([np.nan] + D[1:])
    good = [k for k in range(1, KMAX) if D[k] > 3e-12 and D[k + 1] > 3e-12]
    ratios = np.array([D[k + 1] / D[k] for k in good])
    tail = ratios[-min(40, len(ratios)):]
    # least k_2 for the proved form D_k <= g mu^(k - k_2) at all computed k >= k_2 (only k with D_k above the noise)
    ck = {k: k - math.log(g / D[k]) / math.log(1 / mu_g) for k in good}
    k2 = None
    for cand in range(1, KMAX):
        if all(ck[k] <= cand for k in good if k >= cand):
            k2 = cand
            break
    # control: the same form with the rate kappa_g^2 (faster than the truth) and the SAME k_2 must be violated at some
    # computed level (a first version let k_2 grow up to KMAX/2: with D_k << g at the start that bound can hold over
    # the whole window, so the control could not fail -- NOTES.md)
    k2c = None
    if k2 is not None:
        bad_c = [k for k in good if k >= k2 and D[k] > g * (kap_g ** 2) ** (k - k2)]
        k2c = None if bad_c else k2
        first_bad = bad_c[0] if bad_c else None
    if k2c is None:
        ctrl_fail += 1
    neg = int(np.sum(D[1:] < -1e-13))
    allok = allok and (k2 is not None) and neg == 0 and float(np.max(ratios[len(ratios) // 2:])) <= mu_g
    gk2.append((q, k2))
    print("    g = %.2f h: defect D_k at k = 5, 20, 80, %d: %.3e %.3e %.3e %.3e;  levels with D_k > 3e-12: %d;  D_k < 0: %d"
          % (q, KMAX, D[5], D[20], D[min(80, KMAX)], D[KMAX], len(good) + 1, neg))
    print("        decay ratio D_{k+1}/D_k over the last %d usable levels: %.6f .. %.6f;  kappa_g = %.6f (e^{-g/h} = %.6f);  proved rate mu_g = %.6f;  ratio <= mu_g in the second half: %s"
          % (len(tail), float(tail.min()), float(tail.max()), kap_g, math.exp(-g / h), mu_g, bool(np.max(ratios[len(ratios) // 2:]) <= mu_g)))
    print("        least k_2 with D_k <= g mu_g^(k - k_2) for all computed k >= k_2: %s  (g k_2/h = %s);  control (rate kappa_g^2): %s"
          % (k2, ("%.2f" % (q * k2)) if k2 else "-", ("violated from k = %s on, as it must" % first_bad) if k2c is None else "HOLDS (control did not fail)"))
print("    controls failed (as they must): %d of 5;   g k_2/h over the rates: %s" % (ctrl_fail, ", ".join("%.2f" % (q * k2) for q, k2 in gk2 if k2)))
print("SMALLRATES: %s" % ("no violation; controls fail as they must" if (vA == 0 and vo == 0 and vc > 0 and allok and ctrl_fail >= 3) else "CHECK FAILED"))
R.finish("r29_i4_smallrates u=%g KMAX=%d" % (u, KMAX))
