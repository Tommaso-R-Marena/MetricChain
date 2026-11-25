#!/usr/bin/env python3
"""t01 -- control: the field case of theory report section 11.20, re-computed two independent ways.
(A) closed (cosh) game function of Theorem 11.59(b);  (B) the single-letter sup-min of this report
    R_lam(e) = sup_mu min{ MI(nu) : u dist(nu,mu) + lam(kappa(nu)) <= e + alpha(mu) }  (binary centres, clipping solver),
    and the brief's cone formula.  Known values: p=0.1,u=2: R^max(0)=0.048130, E=0.21227, R^max(0.3E)=0.023273,
    R_0(0.3E)=0.019497, theta_na(0.3E)=0.036246;  p=1/2,u=1: R^max(0)=0.029139.
usage: python3 t01_control.py
"""
import math, sys, time
import numpy as np
import tlib as T

t0 = time.time()
print("== control (field), closed forms (A) against the single-letter solver (B)")
for (p, u) in ((0.1, 2.0), (0.5, 1.0)):
    th = math.log((1 - p) / p)
    K = T.Known(T.phi_field(p), u)
    E = T.E_field(th, u)
    print(f"\np = {p}, u = {u}:  E (closed form) = {E:.6f};  contact set of v: {K.contact_pieces()}")
    for frac in (0.0, 0.3):
        e = frac * E
        RA = T.Rmax_field(th, u, e)
        R0A = T.Rmax_field(th, u, e, gamma=0.0)
        # (B) binary sup-min with the flat-histogram landscape v, and with the zero landscape
        RB, argB = T.R_bin(K, e, K.v, starts=[(0.4, 0.1, 0.05), (0.5, 0.15, 0.15)], nrand=3)
        R0B, arg0 = T.R_bin(K, e, K.lam_zero(), starts=[(0.4, 0.1, 0.05), (0.5, 0.15, 0.15)], nrand=3)
        RC, mC = T.R_cone(K, e, K.v, full=True)
        R0C, m0C = T.R_cone(K, e, K.lam_zero(), full=True)
        print(f"  e = {frac}E = {e:.6f}")
        print(f"    R^max: closed {RA:.7f} | sup-min (binary) {RB:.7f} at (m,a,b)=({argB[0]:.4f},{argB[1]:.4f},{argB[2]:.4f})"
              f" | cone formula {RC:.7f} (m={mC:.4f})   diffs {RB-RA:+.1e} {RC-RA:+.1e}")
        print(f"    R_0  : closed {R0A:.7f} | sup-min (binary) {R0B:.7f} | cone formula {R0C:.7f} (m={m0C:.4f})"
              f"   diffs {R0B-R0A:+.1e} {R0C-R0A:+.1e}")
        # non-adaptive partner at x = e + R^max(e): pair identity; and theta_na(0.3E)
        for x, tag in ((e + RA, "e+R^max(e)"),) + (((e, "e"),) if e > 0 else ()):
            naA = T.thetana_field(th, u, x)
            lams, mus = T.bin_blocks(*argB)
            naB = T.n_mu(K, lams, mus, x, K.v)                      # n_mu at the optimal Gibbs shell of the dip
            # cone truncated (centre shell = the centre): the brief's theta_na formula at the optimal centre type
            best = (-1, None)
            for m in np.linspace(max(mC - 0.08, 0.02), min(mC + 0.08, 0.98), 9):
                tc = T.theta_shell(K, np.array([m, 1 - m]), np.array([1.0, 0.0]), x)
                if tc > best[0]:
                    best = (tc, m)
            print(f"    theta_na({tag} = {x:.6f}): closed {naA:.7f} | n_mu at dip optimum {naB:.7f} | truncated cone (m={best[1]:.3f}) {best[0]:.7f}"
                  + (f"   [pair identity: R^max(e) = {RA:.7f}]" if tag != "e" else ""))
print(f"\ntime {time.time()-t0:.1f}s")
