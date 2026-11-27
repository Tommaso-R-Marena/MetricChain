#!/usr/bin/env python3
"""R13 / item 2, Proposition 11.117(b) as worded ("for every finite (X, pi) and envelope u d_0", in a Setting where envelopes
are "not necessarily symmetric"): our Proposition R10.1 assumes d_0 SYMMETRIC.  Is the hypothesis needed?  Yes.

Counter-example (own code; F* by the certified bracket of r13_05_blocks_recursion.Fstar).  X = {0, 1}, pi = (q, 1-q),
d_0(0,1) = 1, d_0(1,0) = 0  (zero diagonal, triangle inequality).  The class {psi : psi(x)-psi(y) <= u d_0(x,y)} is
{psi(0) - psi(1) in [0, u]}: two vertices, psi = (0,0) and psi = (u, 0).  V = max Var_pi f over 1-Lipschitz f = q(1-q).
Claimed:  F*(t) = (t(1-t)/2) u^2 V + O(u^3).   True: the labels form the segment {c 1[x=0] : 0 <= c <= u}, whose Chebyshev
radius in L^2(pi) is u/2 times sqrt(q(1-q)), so F*(t) = (t(1-t)/2) u^2 V/4 + O(u^3): a factor 4 smaller.
For comparison the symmetric envelope d_0(0,1) = d_0(1,0) = 1 on the same space (ratio -> 1).
"""
import numpy as np, math
from r13_05_blocks_recursion import Fstar

def site_channel(q, lo, hi):
    """two-point space, pi = (q, 1-q); vertices psi(0) - psi(1) in {lo, hi}."""
    pi = np.array([q, 1 - q])
    V = np.array([[lo, 0.0], [hi, 0.0]])
    W = pi[None, :] * np.exp(-V)
    return W / W.sum(axis=1, keepdims=True)

print("# r13_06_small_slope_asym.py")
print("  q    t    u      F*(t)/((t(1-t)/2) u^2 V): asymmetric d_0 (claim of 11.117(b) as worded: -> 1) | symmetric d_0 (R10.1: -> 1)")
for q in (0.5, 0.3):
    V = q * (1 - q)
    for t in (0.3, 0.5):
        for u in (0.4, 0.2, 0.1, 0.05, 0.025):
            lo_a, hi_a, _ = Fstar(site_channel(q, 0.0, u), t, tol=1e-15, iters=200000)
            lo_s, hi_s, _ = Fstar(site_channel(q, -u, u), t, tol=1e-15, iters=200000)
            den = (t * (1 - t) / 2) * u * u * V
            print(f"  {q}  {t}  {u:<6g} asym: [{lo_a/den:.5f}, {hi_a/den:.5f}]    sym: [{lo_s/den:.5f}, {hi_s/den:.5f}]")
print("# END")
