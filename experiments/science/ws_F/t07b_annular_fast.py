"""N7 (fast version): certified finite-n lower bounds with the oracle at the zero residual from pairs of annular dips,
on a bounding box of the (kappa, j) grid that contains the dip supports (checked: the supports do not touch the box).
Same definitions as t07_zero_residual_annular.py; exact finite sums."""
import numpy as np, sys
from scipy.special import logsumexp
from sl import *
from ts import lbinom
from prof import sup_profiles, tilt_bound
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()


class Box:
    def __init__(self, n, p, u, k, K, J):
        self.n, self.p, self.u, self.k, self.K, self.J = n, p, u, k, K, J
        kap = np.arange(K + 1)[:, None]; j = np.arange(J + 1)[None, :]
        self.kap, self.j = kap, j
        self.valid = (j <= kap) & (kap - j <= n - k)
        self.lN = lbinom(k, j) + lbinom(n - k, kap - j)
        self.lS = lbinom(kap, j) + lbinom(n - kap, k - j) - lbinom(n, k)
        self.lpi = kap * np.log(p) + (n - kap) * np.log(1 - p) + 0 * j

    def ann(self, j1, j0, lift):
        s = self.u * (np.abs(self.j - j1) + np.abs(self.kap - self.j - j0))
        D = self.valid & (s < lift)
        if not D.any(): return 0.0, np.nan, D
        with np.errstate(divide='ignore', invalid='ignore'):
            lterm = np.where(D, self.lN + self.lpi + np.log(np.expm1(np.minimum(lift - s, 700.0))), -np.inf)
        lE = logsumexp(lterm)
        return float(np.exp(lE)), float((np.exp(lterm - lE) * self.kap).sum() / self.n), D

    def inside(self, D):
        ok = not D[-1, :].any() if self.K < self.n else True
        ok2 = not D[:, -1].any() if self.J < self.k else True
        return ok and ok2

    def lhit(self, D):
        return float(logsumexp(np.where(D, self.lS, -np.inf), axis=1).max())


def pair(B, shA, shB, eps, target):
    def build(lift):
        EA, cA, DA = B.ann(shA[0], shA[1], lift); EB, cB, DB = B.ann(shB[0], shB[1], lift)
        if EA == 0 or EB == 0: return None
        if (cA - target) * (cB - target) > 0: return ('nb', EA)
        den = EA * abs(target - cA) + EB * abs(cB - target)
        lam = EB * abs(cB - target) / den if den > 0 else 0.5
        return (np.log1p(lam * EA + (1 - lam) * EB), lam, cA, cB, DA | DB)
    lo, hi = 0.0, float(B.u * B.n)      # the lift of an annular dip is n(e + D(core||pi)), not eps + O(1)
    for _ in range(48):
        mid = (lo + hi) / 2; R = build(mid)
        if R is None: lo = mid
        elif R[0] == 'nb':
            if np.log1p(R[1]) > eps: hi = mid
            else: lo = mid
        elif R[0] > eps: hi = mid
        else: lo = mid
    R = build(hi)
    if R is None or R[0] == 'nb' or R[0] <= eps or not B.inside(R[4]): return None
    return -np.log(B.n) - B.lhit(R[4]), dict(lift=hi, lam=R[1], cA=R[2], cB=R[3], sep=R[0])


for (p, u, fr) in ((0.1, 2.0, 0.2), (0.3, 1.0, 0.3), (0.25, 1.0, None)):
    E0 = F_game(p, u, 0.0, 1e-6) / 1e-6
    e = 0.02 if fr is None else fr * E0
    r0 = R_gamma(p, u, 0.0, e); m0 = m_forced(p, u, 0.0); rplain = Rcc(p, u, 0.0, m0, e)
    sc = sup_profiles(p, u, 0.0, e, constrained=True, grid=31); tb = tilt_bound(p, u, 0.0, e)
    mm, v0, v1 = sc[1]
    pg = p
    Bud = e + (1 - mm) * kl2(v0, pg) + mm * kl2(v1, pg)
    P(f"\n=== zero residual, p={p} u={u} e={e:.6f}: R_0={r0:.6f} | forced-type plain dips {rplain:.6f} | V (shells, single-letter) {sc[0]:.6f} at (m,v0,v1)=({mm:.3f},{v0:.4f},{v1:.4f}) | U (tilt) {tb:.6f}")
    P("    n | ln LB/n | ln LB | centre type k, shells, mixing weight, excess densities | (V - lnLB/n) n/ln n")
    for n in (400, 800, 1600, 3200):
        eps = e * n
        k0 = int(round(mm * n)); best = None
        rad = int(1.4 * Bud * n / u) + 25 + max(6, n // 20)
        for k in sorted(set(k0 + d * max(1, n // 200) for d in (-4, -2, 0, 2, 4))):
            j0c = v0 * (n - k)
            for j0 in sorted(set(max(0, int(round(j0c)) + d) for d in (-2, -1, 0, 1, 2, 4))):
                jc = int(round(p * n)) - j0
                J = min(k, jc + rad); K = min(n, jc + j0 + 2 * rad)
                B = Box(n, p, u, k, K, J)
                # the excess density is increasing in j1: locate the adjacent pair that brackets p at the predicted lift
                lo_j, hi_j = max(0, jc - max(6, n // 20)), min(k - 1, jc + max(6, n // 20))
                liftp = n * Bud
                while hi_j - lo_j > 1:
                    mid_j = (lo_j + hi_j) // 2
                    Em, cm, _ = B.ann(mid_j, j0, liftp)
                    if Em > 0 and cm <= p: lo_j = mid_j
                    else: hi_j = mid_j
                for j1 in range(max(0, lo_j - 2), min(k - 1, lo_j + 2) + 1):
                    R = pair(B, (j1, j0), (j1 + 1, j0), eps, p)
                    if R is None: continue
                    if best is None or R[0] > best[0]: best = (R[0], k, (j1, j0), R[1])
        if best is None:
            P(f"{n:5d} | none"); continue
        P(f"{n:5d} | {best[0]/n:+.6f} | {best[0]:+.2f} | k={best[1]}, shells {best[2]}&({best[2][0]+1},{best[2][1]}), lam={best[3]['lam']:.3f}, c=({best[3]['cA']:.5f},{best[3]['cB']:.5f}) | {(sc[0]-best[0]/n)*n/np.log(n):.3f}")
open('out/t07b_annular_fast.txt', 'w').write('\n'.join(out) + '\n')
