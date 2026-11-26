#!/usr/bin/env python3
"""R23: own brute-force check of one line of the audit's S8 (AA2 l.352): Curie-Weiss known part on Q_16 = Q_8 x Q_8,
beta J = 1.5, u = 0.2, member psi(a,b) = gamma|b| (gamma = -u, +u): largest change of -ln W(a) under one outer flip, in units of u.
Brute force over all 2^16 configurations (no type lumping).  Stored value of the audit: 1.6204; and beta J = 0 must give 0 (control).
Also the member gamma|b| + s*u*|a|: 2.6204 u per outer flip, and its membership in L_u (|psi(x)-psi(y)| <= u d_H) is checked exhaustively
over all single flips.  Run: python3 -I -B item1_s8_owncheck.py"""
import math, numpy as np
no = ni = 8; n = no + ni
x = np.arange(1 << n); a = x >> ni; b = x & ((1 << ni) - 1)
pc = np.array([bin(i).count("1") for i in range(1 << n)])
wa = pc[a]; wb = pc[b]
def excess(bJ, u, gamma, s=0.0):
    logpi = n * (bJ / 2) * (2 * (wa + wb) / n - 1) ** 2
    psi = gamma * wb + s * u * wa
    num = np.zeros(1 << no); den = np.zeros(1 << no)
    np.add.at(num, a, np.exp(logpi - psi)); np.add.at(den, a, np.exp(logpi))
    lnW = np.log(num / den)
    best = 0.0
    for av in range(1 << no):
        for i in range(no):
            best = max(best, abs(lnW[av] - lnW[av ^ (1 << i)]))
    # membership of psi in L_u: all single flips of the full cube
    lip = 0.0
    for i in range(n):
        lip = max(lip, float(np.abs(psi - psi[x ^ (1 << i)]).max()))
    return best / u, lip / u
viol = 0
for gamma in (-0.2, 0.2):
    e, lip = excess(1.5, 0.2, gamma)
    print(f"beta J = 1.5, u = 0.2, gamma = {gamma:+.1f}: excess = {e:.4f} (audit: 1.6204); Lipschitz constant of psi / u = {lip:.4f}")
    viol += abs(e - 1.6204) > 6e-5 or lip > 1 + 1e-12
e0, _ = excess(0.0, 0.2, 0.2); print(f"control beta J = 0: excess = {e0:.2e}"); viol += e0 > 1e-12
best = 0
for gamma in (-0.2, 0.2):
    for s in (-1.0, 1.0):
        e, lip = excess(1.5, 0.2, gamma, s); best = max(best, e); viol += lip > 1 + 1e-12
print(f"member gamma|b| + s u|a|: fibre average changes by {best:.4f} u per outer flip (audit: 2.6204); all four members are in L_u")
viol += abs(best - 2.6204) > 6e-5
print("violations =", int(viol)); print("END item1_s8_owncheck")
