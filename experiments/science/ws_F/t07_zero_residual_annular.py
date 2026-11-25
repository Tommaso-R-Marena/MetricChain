"""N7: certified finite-n lower bounds WITH the oracle AT THE ZERO RESIDUAL (and other additive bases), exact type sums.

Alternatives: zero residual + lambda*Delta_A + (1-lambda)*Delta_B, where Delta_A, Delta_B are the cyclically
symmetrised excesses of two *annular* dips with the same centre s (type k) around the shells
   Sh(j1,j0) = { y : #(y and s) = j1, #(y and not s) = j0 },   weight  max(1, exp(lift - u*d(x,Sh)))   (gamma = 0),
whose excess densities bracket p; lambda solves the (linear) one-body matching equation exactly.
Plain dips are the shells (j1,j0) = (k,0).  The bound: E|Q| >= (1-2 delta) / (n * max_x P_s(x in D_A u D_B)),
valid when ln(1 + lambda E_A + (1-lambda) E_B) > eps.
"""
import numpy as np, sys
from scipy.special import logsumexp
from sl import *
from ts import Grid
from prof import sup_profiles, tilt_bound
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()


def ann(G, gamma, j1, j0, lift):
    """annular dip around Sh(j1,j0) on the additive base gamma; returns E, c_E, mask"""
    u = G.u
    s = u * (np.abs(G.j - j1) + np.abs(G.kap - G.j - j0)) + gamma * ((j1 + j0) - G.kap)
    D = G.valid & (s < lift)
    if not D.any():
        return 0.0, np.nan, D
    lb = G.lprod(gamma)
    with np.errstate(divide='ignore', invalid='ignore'):
        lterm = np.where(D, G.lN + lb + np.log(np.expm1(np.minimum(lift - s, 700.0))), -np.inf)
    lE = logsumexp(lterm)
    cE = float((np.exp(lterm - lE) * G.kap).sum() / G.n)
    return float(np.exp(lE)), cE, D


def lhit(G, D):
    return float(logsumexp(np.where(D, G.lS, -np.inf), axis=1).max())


def pair_bound(G, gamma, shA, shB, eps, target):
    """two shells, common lift chosen minimal for separation > eps; returns (lnLB, info) or None if no bracket"""
    def build(lift):
        EA, cA, DA = ann(G, gamma, shA[0], shA[1], lift)
        EB, cB, DB = ann(G, gamma, shB[0], shB[1], lift)
        if EA == 0 or EB == 0: return None
        if (cA - target) * (cB - target) > 0: return ('nobracket', cA, cB)
        den = EA * abs(target - cA) + EB * abs(cB - target)
        lam = EB * abs(cB - target) / den if den > 0 else 0.5
        Etot = lam * EA + (1 - lam) * EB
        return (np.log1p(Etot), lam, cA, cB, DA | DB, EA, EB)
    lo, hi = 0.0, eps + 60.0
    for _ in range(45):
        mid = (lo + hi) / 2
        B = build(mid)
        if B is not None and B[0] != 'nobracket' and B[0] > eps: hi = mid
        elif B is not None and B[0] == 'nobracket':
            # treat as: use the larger of the two single excesses for the direction of the search
            EA = ann(G, gamma, shA[0], shA[1], mid)[0]
            if np.log1p(EA) > eps: hi = mid
            else: lo = mid
        else: lo = mid
    B = build(hi)
    if B is None or B[0] == 'nobracket' or B[0] <= eps: return None
    return -np.log(G.n) - lhit(G, B[4]), dict(lift=hi, lam=B[1], cA=B[2], cB=B[3], sep=B[0])


def best_annular(n, p, u, gamma, eps, kgrid, j0grid, target, plain=False):
    best = None
    for k in kgrid:
        G = Grid(n, p, u, k)
        for j0 in ([0] if plain else j0grid):
            if j0 > n - k: continue
            jc = (k if plain else int(round(target * n)) - j0)
            if plain:
                cands = [((k, 0), (k, 0))]
            else:
                cands = [((j1, j0), (j1 + 1, j0)) for j1 in range(max(0, jc - 3), min(k - 1, jc + 3) + 1)]
            for (shA, shB) in cands:
                R = pair_bound(G, gamma, shA, shB, eps, target)
                if R is None: continue
                if best is None or R[0] > best[0]:
                    best = (R[0], k, shA, shB, R[1])
    return best


if __name__ == '__main__':
    for (p, u, fr) in ((0.1, 2.0, 0.2), (0.3, 1.0, 0.2)):
        E0 = F_game(p, u, 0.0, 1e-6) / 1e-6
        e = fr * E0
        r0 = R_gamma(p, u, 0.0, e)
        m0 = m_forced(p, u, 0.0)
        rplain = Rcc(p, u, 0.0, m0, e)
        sc = sup_profiles(p, u, 0.0, e, constrained=True, grid=31)
        tb = tilt_bound(p, u, 0.0, e)
        mm, v0, v1 = sc[1]
        P(f"\n=== zero residual, p={p} u={u} eps1={fr}E_0={e:.6f}:  R_0 (no oracle)={r0:.6f};  WITH oracle: plain dips of the forced type m_0={m0:.4f}: {rplain:.6f};  annular profiles (single-letter): {sc[0]:.6f} at (m,v0,v1)=({mm:.3f},{v0:.4f},{v1:.4f});  tilt upper bound: {tb:.6f}")
        P("    n | annular pair: lnLB/n  [k, shells, lambda, densities]  |  plain dips, two adjacent centre types bracketing p: lnLB/n")
        for n in (200, 400, 800, 1600):
            eps = e * n
            k0 = int(round(mm * n)); j00 = v0 * (n - k0)
            step = max(1, n // 200)
            kgrid = range(max(2, k0 - 8 * step), min(n - 2, k0 + 8 * step) + 1, 2 * step)
            j0grid = sorted(set(max(0, int(round(j00)) + d) for d in range(-3, 6)))
            B = best_annular(n, p, u, 0.0, eps, kgrid, j0grid, p)
            # plain dips: centre types k, k+1 with excess densities bracketing p (different centres)
            bestp = None
            kf = int(round(m0 * n))
            for k in range(max(1, kf - 6), min(n - 2, kf + 6)):
                GA, GB = Grid(n, p, u, k), Grid(n, p, u, k + 1)
                def build(lift):
                    EA, cA, DA = ann(GA, 0.0, k, 0, lift); EB, cB, DB = ann(GB, 0.0, k + 1, 0, lift)
                    if EA == 0 or EB == 0 or (cA - p) * (cB - p) > 0: return None
                    lam = EB * abs(cB - p) / (EA * abs(p - cA) + EB * abs(cB - p))
                    return np.log1p(lam * EA + (1 - lam) * EB), lhit(GA, DA), lhit(GB, DB)
                lo, hi = 0.0, eps + 60
                for _ in range(45):
                    mid = (lo + hi) / 2; Bb = build(mid)
                    if Bb is None:
                        EA = ann(GA, 0.0, k, 0, mid)[0]
                        if np.log1p(EA) > eps: hi = mid
                        else: lo = mid
                    elif Bb[0] > eps: hi = mid
                    else: lo = mid
                Bb = build(hi)
                if Bb is None or Bb[0] <= eps: continue
                val = -np.log(n) - np.logaddexp(Bb[1], Bb[2])
                if bestp is None or val > bestp[0]: bestp = (val, k)
            sA = f"{B[0]/n:+.6f} [k={B[1]}, {B[2]}&{B[3]}, lam={B[4]['lam']:.3f}, c=({B[4]['cA']:.5f},{B[4]['cB']:.5f}), lnLB={B[0]:.2f}]" if B else "none"
            sP = f"{bestp[0]/n:+.6f} [k={bestp[1]},{bestp[1]+1}; lnLB={bestp[0]:.2f}]" if bestp else "none (no bracketing pair)"
            P(f"{n:5d} | {sA} | {sP}")
    open('out/t07_zero_residual_annular.txt', 'w').write('\n'.join(out) + '\n')
