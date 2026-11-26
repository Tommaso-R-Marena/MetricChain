#!/usr/bin/env python3
"""RA04 -- Lemma A1 on the envelope curves, and Proposition A8 at the second level by brute force on the operator R.

 (i)  For levels j and rates g:   inf_{0<phi<1} max_{B <= b_j} Psi_g(phi; B, W_j(B))        (computed from theta_na itself)
      against   U_j(g) := sup{B - Sigma(B, W_j(B)) g : Sigma < infinity}   (the minimax value of Proposition U)
      and       M_{W_{j+1}, b_{j+1}}(g).
      Lemma A1:  inf_phi max Psi  <=  M_{W_{j+1}, b_{j+1}}(g);  the proof gives  inf = U_j <= M.
      Negative control: the same with W_{j+2} in place of W_{j+1} (two levels' gain claimed for one).
 (ii) T_2 = min(theta, R[theta]) by brute force on (11.18.2):
          R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma >= beta} [min(gamma, mu) + (1 - phi) T(gamma/(1 - phi))],   mu = phi theta((g - beta)/phi).
      For the convex T = theta the supremum over gamma is at gamma = beta if beta >= mu, and at gamma in {beta, mu} otherwise.
      Every (phi, beta) gives an UPPER bound for R[theta](g); the script minimises over a grid with zooms.  Compared with
      M_{W_2, b_2}(g)  (Proposition A8: T_2 <= M_{W_2, b_2}) and with the non-adaptive theta(g).
Usage: python3 -B ra04_lemmaA1.py [pair]      pair in {cube1, cube2, gauss}; default cube1
"""
import math
import sys

import numpy as np

import ra_lib as R

which = sys.argv[1] if len(sys.argv) > 1 else "cube1"
P = (R.Gauss() if which == "gauss" else R.Cube(float(which[4:]))).setup()
a, h, L, c2 = P.a, P.h, P.L, P.cstar2
print("# %s: a = %.8f, h = %.8f, L = %.6f, eps* = %.6f" % (P.name, a, h, L, P.epsstar))
JE = 42
S = R.EnvSeq(P, JE)
GOLD = R.GOLD

theta_cache = {}


def theta(e):
    return P.theta(e)


def curve_grid(j, n=20001):
    """a grid of [0, b_j] containing the junction B_t(j) and the top, and the values of W_j"""
    if j == 0:
        xs = np.linspace(0.0, S.b[0], 3)
        return xs, np.zeros(3)
    s = np.linspace(0.0, 1.0, n)
    xs = S.Bt[j] * (1.0 - (1.0 - s) ** 2) if S.Bt[j] > 0 else np.array([0.0])
    xs = np.concatenate((xs, [S.b[j]]))
    Ws = S.Wvec(j, xs)
    Ws[-1] = 1.0
    return xs, Ws


def inf_F(j, g, xs, Ws):
    """inf over e > g of F(e) = max_B [(1 - g/e) B + (1 - W_j(B)) (g/e) theta(e)]  (quasi-convex in e)"""
    def F(e):
        phi = g / e
        return float(np.max((1.0 - phi) * xs + (1.0 - Ws) * phi * theta(e)))
    # e = g/phi, phi in (0, 1): scan phi on a grid, then golden section in phi around the best
    # (the infimum need not be attained: for j = 0 it is the limit phi -> 1, so the scan goes up to 1 - 1e-12)
    phis = np.concatenate((np.linspace(1e-4, 0.999, 400), np.exp(np.linspace(math.log(1e-9), math.log(1e-4), 60)),
                           1.0 - np.exp(np.linspace(math.log(1e-12), math.log(1e-3), 80))))
    phis.sort()
    vals = np.array([F(g / p) for p in phis])
    k = int(np.argmin(vals))
    lo, hi = phis[max(k - 1, 0)], phis[min(k + 1, len(phis) - 1)]
    for _ in range(80):
        m1 = hi - GOLD * (hi - lo)
        m2 = lo + GOLD * (hi - lo)
        if F(g / m1) > F(g / m2):
            lo = m1
        else:
            hi = m2
    pm = 0.5 * (lo + hi)
    return min(float(vals[k]), F(g / pm)), pm


def U(j, g):
    """sup{B - H_j(B) g : H_j(B) < infinity}, H_j = Sigma(., W_j(.)); concave in B: bisection on H_j' = 1/g"""
    lo, hi = 0.0, S.b[j + 1]
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        Hm, dHm = S.H(j, mid)
        if math.isfinite(Hm) and dHm * g <= 1.0:
            lo = mid
        else:
            hi = mid
    Bs = lo
    return (Bs - S.H(j, Bs)[0] * g if Bs > 0 else 0.0), Bs


print("\n== (i) Lemma A1 on the envelope curves ==")
print("#  j    g/h       inf_phi max Psi    U_j(g)          M_{j+1}(g)       inf - U      U - M_{j+1}   [control: inf - M_{j+2}(g)]   phi*     where the max of U sits (B/a)")
worst_iu, worst_um, worst_im, ctrl_fail, ncase = 0.0, -math.inf, -math.inf, 0, 0
for j in (0, 1, 2, 3, 5, 8, 12, 20, 40):
    xs, Ws = curve_grid(j)
    for gh in (0.003, 0.03, 0.1, 0.3, 1.0, 2.0, P.epsstar / h * 0.9, P.epsstar / h * 1.5):
        g = gh * h
        iF, pm = inf_F(j, g, xs, Ws)
        Uj, Bs = U(j, g)
        M1 = S.M(j + 1, g)[0]
        M2 = S.M(j + 2, g)[0]
        ncase += 1
        worst_iu = max(worst_iu, abs(iF - Uj) / a)
        worst_um = max(worst_um, (Uj - M1) / a)
        worst_im = max(worst_im, (iF - M1) / a)
        if iF > M2 + 1e-9 * a:
            ctrl_fail += 1
        if gh in (0.03, 0.3, 2.0) or j in (0, 1):
            print("  %2d  %7.4f   %.10f    %.10f    %.10f    %9.2e    %9.2e     %9.2e                  %.5f   %.5f"
                  % (j, gh, iF, Uj, M1, iF - Uj, Uj - M1, iF - M2, pm, Bs / a))
print("%d cases:  max |inf - U|/a = %.2e (the minimax identity);  max (U - M_{j+1})/a = %.2e (must be <= 0);  max (inf - M_{j+1})/a = %.2e (Lemma A1: <= 0)"
      % (ncase, worst_iu, worst_um, worst_im))
print("negative control (W_{j+2} in place of W_{j+1}): the inequality fails in %d of %d cases" % (ctrl_fail, ncase))

# ---------------------------------------------------------------------------------------------------------------
print("\n== (ii) T_2 = min(theta, R[theta]) by brute force on the operator R, against M_{W_2, b_2} ==")


def bracket_theta(g, phi, beta):
    """the bracket of R at (phi, beta) for T = theta (convex): sup over gamma >= beta"""
    mu = phi * theta((g - beta) / phi)
    om = 1.0 - phi
    if beta >= mu:
        return mu + om * theta(beta / om)
    return max(beta + om * theta(beta / om), mu + om * theta(mu / om))


def R_theta(g):
    """an upper bound for R[theta](g): grid over (phi, beta/g) with zooms"""
    best = (math.inf, None, None)
    plo, phi_hi, blo, bhi = 1e-4, 1.0 - 1e-4, 1e-6, 1.0 - 1e-6
    for zoom in range(7):
        ps = np.linspace(plo, phi_hi, 41)
        bs = np.linspace(blo, bhi, 41)
        for p in ps:
            for bfrac in bs:
                v = bracket_theta(g, p, bfrac * g)
                if v < best[0]:
                    best = (v, p, bfrac)
        dp, db = (phi_hi - plo) / 8.0, (bhi - blo) / 8.0
        plo, phi_hi = max(1e-6, best[1] - dp), min(1.0 - 1e-6, best[1] + dp)
        blo, bhi = max(1e-9, best[2] - db), min(1.0 - 1e-9, best[2] + db)
    return best


print("#   g/h        theta(g)      R[theta](g) <=    T_2(g) <=      M_{W_2,b_2}(g)    T_2 - M_2 (in units of a)    phi      beta/g")
worst = -math.inf
for gh in (1e-4, 1e-3, 0.01, 0.03, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, P.epsstar / h * 0.9, P.epsstar / h * 1.2):
    g = gh * h
    v, p, bf = R_theta(g)
    T2 = min(theta(g), v)
    M2 = S.M(2, g)[0]
    worst = max(worst, (T2 - M2) / a)
    print("  %8.4f   %.8f    %.8f     %.8f     %.8f      %10.3e              %.5f   %.2e" % (gh, theta(g), v, T2, M2, (T2 - M2) / a, p, bf))
print("max of (T_2 - M_{W_2,b_2})/a over the rates above: %.3e   (Proposition A8 at j = 2: must be <= 0 up to the accuracy of the search)" % worst)
print("b_2/a = %.6f;   upper bound for tau_2/a from the smallest rate: %.6f" % (S.b[2] / a, min(theta(1e-4 * h), R_theta(1e-4 * h)[0]) / a))
