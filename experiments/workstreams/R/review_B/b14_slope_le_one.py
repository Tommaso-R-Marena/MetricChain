"""Referee B, check 14: a consequence of Proposition U + Proposition A that can be tested sharply.
If |theta'(0+)| = m <= 1 then Sigma(B, s) <= (1 - s) m <= 1 on the whole regular region (boundary included), every orbit
curve p_k is an admissible W of Proposition U (values in [0, 1], finite up to and including B_inf(k)), theta itself is
the envelope of its tangent lines (B, p_1(B)), and Corollary U' gives tau_k <= B_inf(k) by induction; with
Proposition A:  tau_k = B_inf(k) EXACTLY, for every k.   Test with the recursion itself (b6 code) against the orbit:
   m = 0.3 : 0.3 exp(-e);   m = 0.8 : exp(-0.8 e);   m = 1 : 0.5 exp(-2e);   m = 1 : max(1 - e, 0)  (affine!);
   contrast, m > 1 : exp(-1.5 e) (m = 1.5), exp(-3 e) (m = 3)  -- there tau_k > B_inf(k) is allowed.
"""
import math, sys, importlib.util
import numpy as np
import blib

spec = importlib.util.spec_from_file_location("b6", "b6_recursion.py")
b6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b6)


def expo(c, a):
    return (lambda e: a * np.exp(-c * e)), blib.TPair("%g exp(-%g e)" % (a, c), lambda e: a * math.exp(-c * e), lambda e: -a * c * math.exp(-c * e), a, finite_slope0=a * c)


cases = [("0.3 exp(-e)   (m = 0.3)",) + expo(1.0, 0.3) + (0.3, 40.0),
         ("exp(-0.8 e)   (m = 0.8)",) + expo(0.8, 1.0) + (1.0, 40.0),
         ("0.5 exp(-2e)  (m = 1)",) + expo(2.0, 0.5) + (0.5, 20.0),
         ("max(1 - e, 0) (m = 1, affine)", lambda e: np.maximum(1 - e, 0.0),
          blib.TPair("(1-e)+", lambda e: max(1 - e, 0.0), lambda e: -1.0 if e < 1 else 0.0, 1.0, finite_slope0=1.0), 1.0, 1.0),
         ("exp(-1.5 e)   (m = 1.5)",) + expo(1.5, 1.0) + (1.0, 30.0),
         ("exp(-3 e)     (m = 3)",) + expo(3.0, 1.0) + (1.0, 15.0)]
levels = int(sys.argv[1]) if len(sys.argv) > 1 else 9
for label, th_np, P, a, xmax in cases:
    P.h = P.fixed_point()
    Pd = dict(theta=th_np, a=a, xmax=xmax, h=P.h, c2=None, label=label)
    q, xmin = 1.01, 1e-9
    G = int(math.ceil(math.log(xmax / xmin) / math.log(q)))
    x = np.concatenate([[0.0], xmax * q ** np.arange(-G, 1.0)])
    T = th_np(x)
    T[0] = a
    bz = [-34.0, -20.0, -12.0, -8.0, -6.0, -4.5, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.5, 6.0]
    tau = a
    row = []
    for k in range(1, levels + 1):
        b = P.B_inf(k, tol=4e-16)
        row.append((k, tau, b))
        if k == levels:
            break
        R, _ = b6.step(x, T, Pd, 320, bz, 100)
        tz, _ = b6.tau_zero(x, T, a)
        newT = T.copy()
        newT[1:] = np.minimum(T[1:], R[1:])
        newT[1:] = np.minimum.accumulate(newT[1:])
        tau = min(tau, tz)
        newT[0] = max(tau, newT[1])
        T = newT
    print("%s:  a = %.4f, h = %.9f" % (label, a, P.h))
    print("    tau_k - B_inf(k), k = 2..%d:  %s" % (levels, "  ".join("%+.1e" % (t - b) for k, t, b in row[1:])))
    print("    (tau_k - B_inf)/(tau_k - h):   %s" % "  ".join("%.1e" % ((t - b) / (t - P.h)) if t > P.h + 1e-12 else "-" for k, t, b in row[1:]))
