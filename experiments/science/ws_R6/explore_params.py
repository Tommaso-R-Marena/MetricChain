# explore feasible parameter cells for the harness: prints r-dagger, the largest radius r_N with [N], Y_N (width of the window
# of negligible levels above a flat bulk), ln M-dagger, ln cap, ln Mbar; all from r6lib (exact tables).
import sys, numpy as np, mpmath as mp
from fractions import Fraction
import r6lib as R

def cell(n, n_o, u, b, lam, eta, etap, theta, nu1, delta=0.05, Kov=None):
    n_i = n - n_o
    xs = [2 * u * n_i, max(b * 1.0001, 0.5 * u * n_i), b] if 0.5 * u * n_i > b else [2 * u * n_i, b]
    P = R.Params2LP(n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, [1] * (len(xs) - 1), K_override=Kov)
    tab = P.tab
    rN = -1
    for r in range(n_o):
        if tab.gamma_tilde(r) <= P.theta * (1 - P.etaf) * P.nu0: rN = r
        else: break
    YN = mp.mpf(tab.two_m) / (tab.ball[max(rN, 0)] * (1 - P.etaf) * P.nu0)
    return P, rN, YN

if __name__ == "__main__":
    print("%5s %4s %4s %5s %5s %5s | %5s %6s %5s %4s %4s %7s %8s %7s %7s %7s %6s" % ("n", "n_o", "u", "b", "lam", "eta", "J", "K", "nu0", "rdag", "r_N", "lnY_N", "lnMdag", "lncap", "lnMbar", "p_u*m", "x_out"))
    for (n, n_o, u, b, lam, eta, etap, theta, nu1f) in [
        (300, 120, 1.0, 0.5, 1/12, Fraction(1, 12), 1/12, 1/12, None),
        (300, 120, 1.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, None),
        (500, 250, 1.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, None),
        (500, 250, 1.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, 1.0),
        (600, 300, 1.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5, None),
        (200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, None),
        (200, 100, 2.0, 0.5, 0.5, Fraction(1, 4), 0.5, 0.5, None),
        (160, 80, 2.0, 0.5, 0.25, Fraction(1, 4), 0.25, 0.25, None),
        (120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5, None),
        (120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5, 1.0),
        (1000, 500, 0.5, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, None),
        (80, 40, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, 1.0),
        (48, 24, 0.5, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5, 1.0),
    ]:
        nu1 = 2 * np.e ** u * n_o / theta if nu1f is None else nu1f
        P, rN, YN = cell(n, n_o, u, b, lam, eta, etap, theta, nu1)
        print("%5d %4d %4.1f %5.2f %5.2f %5s | %5d %6d %5.1f %4d %4d %7.2f %8.2f %7.2f %7.2f %7.1f %6.3f" % (
            n, n_o, u, b, lam, str(eta), P.J, P.K, float(mp.log(P.nu0)), P.rdag, rN, float(mp.log(YN)), float(mp.log(P.Mdag)),
            float(mp.log(P.cap_new)), float(mp.log(P.Mbar)), n_o / (1 + np.e ** u), float(P.x_out)))
