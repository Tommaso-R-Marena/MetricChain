"""Referee B, check 9: an adversarial test of Proposition A (tau_k >= B_inf(k)) on unusual (H0) functions, with the
recursion iterated by b6_recursion's code (grid) and B_inf(k) from the orbit of the slope map (blib).
A violation  tau_k(numerical) < B_inf(k) - tolerance  would refute Proposition A (the numerical tau_k can only be too
LARGE through the minimisation; interpolation errors are ~1e-6).  Also prints h and whether p_k(h) <= L-type bounds hold.
Pairs: (i) 0.3 exp(-e)            (a barely above h)
       (ii) max(1 - 10 e, 0.05)   (steep, then flat at a positive value; kink at 0.095, just to the right of h = 1/11)
       (iii) (1 + e)^-4            (slow decay, never zero)
       (iv) 0.1 + 0.9 exp(-3e)     (theta(inf) > 0)
       (v) max((1 - sqrt e)^2, 1/4 + 0.4 (1/4 - e))   (kink at h, strictly convex left piece)
       (vi) 1 - sqrt(e) for e < 1  (convex, infinite slope at 0, kink at 1 where it reaches 0)
"""
import math, sys, importlib.util
import numpy as np
import blib

spec = importlib.util.spec_from_file_location("b6", "b6_recursion.py")
b6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b6)

cases = []
cases.append(("0.3 exp(-e)", lambda e: 0.3 * np.exp(-e), blib.TPair("0.3 exp(-e)", lambda e: 0.3 * math.exp(-e), lambda e: -0.3 * math.exp(-e), 0.3, finite_slope0=0.3), 0.3, 40.0))
cases.append(("max(1 - 10e, 0.05)", lambda e: np.maximum(1 - 10 * e, 0.05),
              blib.TPair("max(1-10e,0.05)", lambda e: max(1 - 10 * e, 0.05), lambda e: -10.0 if e < 0.095 else 0.0, 1.0, finite_slope0=10.0), 1.0, 2.0))
cases.append(("(1 + e)^-4", lambda e: (1 + e) ** -4.0, blib.TPair("(1+e)^-4", lambda e: (1 + e) ** -4.0, lambda e: -4 * (1 + e) ** -5.0, 1.0, finite_slope0=4.0), 1.0, 60.0))
cases.append(("0.1 + 0.9 exp(-3e)", lambda e: 0.1 + 0.9 * np.exp(-3 * e), blib.shifted(), 1.0, 20.0))
cases.append(("kink at h, smooth left piece", b6.make_pair("kinksmooth")["theta"], blib.kink_smooth(0.4), 1.0, 1.0))
cases.append(("1 - sqrt(e)", lambda e: np.where(e < 1.0, 1.0 - np.sqrt(np.clip(e, 0, 1)), 0.0),
              blib.TPair("1 - sqrt e", lambda e: 1 - math.sqrt(e) if e < 1 else 0.0, lambda e: -0.5 / math.sqrt(e) if e < 1 else 0.0, 1.0), 1.0, 1.0))

levels = int(sys.argv[1]) if len(sys.argv) > 1 else 9
for label, th_np, P, a, xmax in cases:
    P.h = P.fixed_point()
    Pd = dict(theta=th_np, a=a, xmax=xmax, h=P.h, c2=None, label=label)
    q, xmin = 1.015, 1e-9
    G = int(math.ceil(math.log(xmax / xmin) / math.log(q)))
    x = np.concatenate([[0.0], xmax * q ** np.arange(-G, 1.0)])
    T = th_np(x)
    T[0] = a
    bz = [-34.0, -20.0, -12.0, -8.0, -6.0, -4.5, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.5, 6.0]
    tau = a
    print("%s:  a = %.6f, h = %.9f" % (label, a, P.h))
    worst = 1e9
    for k in range(1, levels + 1):
        b = P.B_inf(k, tol=4e-16)
        worst = min(worst, tau - b)
        print("   k = %d: tau_k = %.9f   B_inf(k) = %.9f   tau_k - B_inf(k) = %+.3e   tau_k - h = %.3e" % (k, tau, b, tau - b, tau - P.h))
        if k == levels:
            break
        R, _ = b6.step(x, T, Pd, 240, bz, 150)
        tz, _ = b6.tau_zero(x, T, a)
        newT = T.copy()
        newT[1:] = np.minimum(T[1:], R[1:])
        newT[1:] = np.minimum.accumulate(newT[1:])
        tau = min(tau, tz)
        newT[0] = max(tau, newT[1])
        T = newT
    print("   min over k of tau_k - B_inf(k): %+.3e  -> %s" % (worst, "Proposition A holds" if worst > -1e-6 else "VIOLATION"))
