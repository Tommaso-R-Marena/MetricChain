#!/usr/bin/env python3
"""ER3 review, E20''(a): the constant c_D = min beta_k / 4 (|D| >= 3) degenerates when ONE differing angle nearly
coincides, although the certificate does not.  From the same two cases as in the proof, for any two differing
angles k != l:   F >= min( min(theta_k, theta_l),  theta_k theta_l / (4 |D|) ) min(A, B),   theta = beta / 4,
(same type: the two-far lemma; different types: F >= a_k b_l >= theta_k theta_l and min(A, B) <= 4 |D|), hence
    c_D' = max( min_k beta_k / 4 ,  beta_(1) beta_(2) / (64 |D|) )        (beta_(1), beta_(2) the two largest)
is also a valid growth constant.  Checked here against the true constant on grids, |D| = 3.
"""
import numpy as np
import er3_e20pp as E

rng = np.random.default_rng(31109)
print("|D| = 3: gaps -> c_D (report), c_D' (improved), c_true (grid 161^3 + polishing)")
ok = True
for gaps in ((1e-3, np.pi, np.pi), (1e-2, 3.0, 2.5), (0.05, 0.05, 3.1), (0.3, 2.0, 2.9), (1e-2, 1e-2, np.pi),
             (1.0, 1.0, 1.0), (np.pi, np.pi, np.pi)):
    p = rng.uniform(0, 2 * np.pi, 3); q = p + np.array(gaps)
    beta = 2 - 2 * np.cos(p - q); bs = np.sort(beta)[::-1]
    cD = beta.min() / 4; cDp = max(cD, bs[0] * bs[1] / (64 * 3))
    ct = E.ctrue_D(p, q, 161)[0]
    ok &= ct >= cDp * (1 - 1e-9)
    print(f"   gaps {tuple(round(float(g), 4) for g in gaps)}: c_D = {cD:.3e}, c_D' = {cDp:.3e}, c_true = {ct:.3e}  "
          f"(c_true/c_D = {ct / cD:.1f}, c_true/c_D' = {ct / cDp:.1f})")
print("PASS" if ok else "FAIL")
