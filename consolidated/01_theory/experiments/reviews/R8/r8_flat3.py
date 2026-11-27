#!/usr/bin/env python3
"""Referee R8 -- THREE nested levels at the flat instance psi = 0: the exact number of evaluations of
Algorithm 2L+ whose inner family is, rung by rung, the cheaper of the two-sample bracket (Proposition K0)
and Algorithm 2L+ itself (with Proposition-K0 brackets inside), against two levels and against the hinted
lower bound.  Own code (uses r8_flat.flat_run, which is cross-checked against the pass-by-pass implementation).

At psi = 0 the middle algorithm is deterministic too (its bracket of a flat fibre and its number of
evaluations are those of r8_flat.flat_run), so the three-level run is again exact.

Middle algorithm for an outer rung of accuracy x in dimension d (failure probability delta' of the outer run):
  x >= 8 :  Corollary-K1.b style: lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance b = x/4,
            theta = e^{x-b} - (3e+1) - (2p_u)^d e^{-b}  (certified accuracy exactly x), 30 inner rungs,
            outer fraction phi_2 = g/(g + theta_hint(g)), g = x/d (clipped to [0.05, 0.7]), and 1.5 times that;
  x <  8 :  Theorem-K2 style: lam = eta = eta' = theta = min(x/12, 1/3), b = x/2, nu_1 = 2e^u n_o/theta, phi_2 = 0.55.
The outer algorithm has the parameters of the report's section 6.4 (b = 0.5, lam = 0.2, eta = eta' = theta = 0.05,
delta = 0.05, 40 rungs).

usage: python3 r8_flat3.py <u> <n> <phi1,phi1,...>
"""
import sys, math, time
import numpy as np
import r8_flat as F


def theta_hint(u, g):
    lam1 = math.log(2 / (1 + math.exp(-u)))
    est = math.log(math.cosh(u / 2))
    if g >= est:
        return 0.0
    r = (lam1 + g) / u
    return math.log(2) + r * math.log(r) + (1 - r) * math.log(1 - r)


def make_inner(u, stats):
    est = math.log(math.cosh(u / 2))

    def inner(d, x, ldeltap):
        c0, a0, b0, kind0 = F.k0_plan_flat(d, u, x, ldeltap)
        best = (c0, a0, b0, kind0)
        g = x / d
        if g >= 0.9 * est or d < 50:
            stats.append((x, 'K0 (not tried)', c0, None))
            return best
        cands = []
        if x >= 8:
            bm = x / 4
            lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
            p0 = min(0.7, max(0.05, g / (g + theta_hint(u, g))))
            for p2 in (p0, min(0.8, 1.5 * p0)):
                if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                    continue
                r = F.flat_run(u, d, p2, lam=1.0, eta=0.5, etap=1.0, b=bm, Lr=30, bounded=False, ltheta=lth, ldelta=ldeltap)
                cands.append(r)
        else:
            c = min(x / 12, 1 / 3)
            r = F.flat_run(u, d, 0.55, lam=c, eta=c, etap=c, theta=c, b=x / 2, Lr=30, bounded=True, ldelta=ldeltap)
            cands.append(r)
        cm = None
        for r in cands:
            assert r['xout'] <= x + 1e-9, (r['xout'], x)
            assert r['width'] <= r['xout'] + 1e-9 and r['lL'] <= 1e-12 and r['lU'] >= -1e-12
            assert r['lcost'] <= r['lCmax'] + 1e-9
            if cm is None or r['lcost'] < cm['lcost']:
                cm = r
        if cm is not None and cm['lcost'] < best[0]:
            best = (cm['lcost'], cm['lL'], cm['lU'], '2L+')
        stats.append((x, best[3], c0, cm['lcost'] if cm is not None else None))
        return best
    return inner


if __name__ == '__main__':
    u = float(sys.argv[1])
    n = int(sys.argv[2])
    phis = [float(x) for x in sys.argv[3].split(',')]
    pu = 1 / (1 + math.exp(u))
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    t0 = time.time()
    print("# u = %.1f, n = %d: number of evaluations at psi = 0, in units ln(cost)/(n a)" % (u, n))
    for phi in phis:
        r2 = F.flat_run(u, n, phi)
        stats = []
        r3 = F.flat_run(u, n, phi, inner=make_inner(u, stats))
        lb, kstar = F.hinted_lower_bound(u, n, r3['xout'], 0.05)
        used = [(x, kind) for (x, kind, c0, cm) in stats]
        n2 = sum(1 for (x, kind) in used if kind == '2L+')
        xs2 = [x for (x, kind) in used if kind == '2L+']
        print("phi_1 = %.2f: two levels %.4f | three levels %.4f | hinted lower bound %.4f | C_max(3 levels) %.4f | 3 levels: valid %s, width %.3f <= x_out %.3f: %s, cost >= LB: %s, cost <= C_max: %s"
              % (phi, r2['lcost'] / (n * a), r3['lcost'] / (n * a), lb / (n * a), r3['lCmax'] / (n * a),
                 r3['lL'] <= 1e-12 and r3['lU'] >= -1e-12, r3['width'], r3['xout'], r3['width'] <= r3['xout'] + 1e-9,
                 r3['lcost'] >= lb, r3['lcost'] <= r3['lCmax'] + 1e-9))
        print("     rungs served by the middle 2L+: %d of 40 (accuracies %.3g ... %.3g); deepest rung reached by an outer point: %d   [%.0f s]"
              % (n2, min(xs2) if xs2 else float('nan'), max(xs2) if xs2 else float('nan'), r3['maxrung'], time.time() - t0))
        sys.stdout.flush()
