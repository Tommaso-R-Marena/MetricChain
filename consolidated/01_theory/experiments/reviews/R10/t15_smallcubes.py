"""All proper nonempty subsets of Q_3 and Q_4 (bJ = 1.5, B = 0, u = 1), instance H:
e_D = ln(Phi_H^+(D))/n, theta_D = -ln(maxdens(D))/n.  How informative is the inequality
theta_D <= Rbar(e_D - omega) + omega of Theorem T3(b) at these sizes?  (own code)"""
import time, math, itertools
import numpy as np
from r10lib import *
from r10fin import *
t0 = time.time()
bJ, u = 1.5, 1.0
phi = lambda k: -(bJ / 2.0) * (2 * k - 1) ** 2
M = Model(bJ=bJ, bB=0.0, u=u)
# reference: binary shells (a lower bound of R_H) and R_unif (a proved upper bound)
sh = lambda x: binary(0.5, x, x)
def R2(e):
    xs = np.linspace(0.2, 0.45, 26)
    v = [r_mu(M, *sh(x), e) for x in xs]
    v = [x if np.isfinite(x) else 0.0 for x in v]
    return max(v)
eg = np.linspace(-0.11, 0.09, 41)
Rg = np.array([R2(e) for e in eg])
Rg = np.maximum.accumulate(Rg[::-1])[::-1]
def Rb_ref(e):
    if e <= eg[0]: return -e
    if e >= eg[-1]: return 0.0
    return max(float(np.interp(e, eg, Rg)), -e)
def Rb_unif(e):
    return max(R_unif(e, u), -e)
def omega(eD, thD, Rb):
    if thD <= Rb(eD) + 1e-12: return 0.0
    lo, hi = 0.0, 5.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if thD <= Rb(eD - mid) + mid: hi = mid
        else: lo = mid
    return hi
for n in (3, 4):
    J = exchangeable(n, phi); Vn = lip_minorant(J, u)
    br = Brute(n, J, u)
    psiH = -Vn[br.wt]
    w = br.pi * np.exp(-psiH); mu_ = w / w.sum()
    S = u * br.d + psiH[:, None] - psiH[None, :]
    N = 1 << n
    cnt_pos = 0; cnt_nontriv = 0; worst = (0.0, None); worst_u = 0.0; nsets = 0
    eDs = []; ths = []
    tot = np.bincount(br.wt, minlength=n + 1)
    for code in range(1, (1 << N) - 1):
        mask = np.array([(code >> i) & 1 for i in range(N)], dtype=bool)
        s_out = np.min(np.where(mask[None, :], np.inf, S), axis=1)
        PhiP = float(np.sum(mu_[mask] * np.exp(s_out[mask])))
        md = float(np.max(np.bincount(br.wt[mask], minlength=n + 1) / tot))
        eD = math.log(PhiP) / n; thD = -math.log(md) / n
        nsets += 1
        cnt_pos += (eD > 0)
        cnt_nontriv += (eD > 0 and thD > 0)
        o = omega(eD, thD, Rb_ref)
        if o > worst[0]: worst = (o, (code, eD, thD))
        worst_u = max(worst_u, omega(eD, thD, Rb_unif))
        eDs.append(eD); ths.append(thD)
    eDs = np.array(eDs); ths = np.array(ths)
    print(f"n={n}: {nsets} subsets; with Phi+ > 1 (e_D > 0): {cnt_pos}; with e_D > 0 and maxdens < 1: {cnt_nontriv};"
          f" largest omega w.r.t. the binary curve: {worst[0]:.4f} {worst[1]}; w.r.t. R_unif: {worst_u:.4f};"
          f" range of e_D [{eDs.min():.3f}, {eDs.max():.3f}]; among sets with e_D > 0: max theta_D = {ths[eDs > 0].max() if (eDs > 0).any() else float('nan'):.4f}"
          f" (ln n/n = {math.log(n)/n:.3f});  t={time.time()-t0:.0f}", flush=True)
    # where does the inequality bind?  sets with e_D < 0 are in the 'volume regime' Rbar >= -e
    neg = eDs < 0
    print(f"      sets with e_D < 0: {neg.sum()}; among them max of theta_D + e_D (must be <= omega-ish): {np.max((ths + eDs)[neg]):+.4f}")
print("time", time.time() - t0)
