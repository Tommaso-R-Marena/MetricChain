#!/usr/bin/env python3
"""Referee's reproduction of Proposition N12 (N_REPORT section 5.2) -- written from the description alone.

Nothing is imported from the workstream's code.  Contents:
  1. the instance (m = 12, k = 16, u = 1, J = 4, tau = 10.5): V by outer weight, A, edge ratios, the constant c(J,u),
     the violation of (TU) for Harper's function of the assumed slope u, by exhaustive evaluation at all levels s
  2. my own implementation of Algorithm A of N_REPORT section 2.2 (outer loop literal; inner procedures = an oracle
     returning valid brackets of the promised ratio around the exact V(a))
  3. runs with the tail functions of the assumed class (slope u) and of the true class of V (slope = largest edge
     ratio), three parameter sets, four oracle placements; for every run: validity, width, truth of every sampled
     certificate, the Chernoff events (V2), (V3) on the realised sample, and where the false step is.
"""
import math
import sys
import time
from fractions import Fraction

import numpy as np

INF = float("inf")
ENTRIES = []


def sigma(z):
    return 1.0 / (1.0 + math.exp(-z))


# ------------------------------------------------------------------------------------------------------------------
# 1. the instance
# ------------------------------------------------------------------------------------------------------------------
m, k, u, Jc, tau = 12, 16, 1.0, 4.0, 10.5
NN = 2 ** m
binom = [math.comb(m, w) for w in range(m + 1)]
pw = [sigma(Jc * (tau - w)) for w in range(m + 1)]                 # P(b_l = 1 | a), |a| = w
Vw = [(1 - p + p * math.exp(-u)) ** k for p in pw]                 # V(a) = E[e^{-u|b|} | a]
A = sum(binom[w] * Vw[w] for w in range(m + 1)) / NN


def p_exact(s):
    """mu_o(V > s)"""
    return sum(binom[w] for w in range(m + 1) if Vw[w] > s) / NN


def excess_exact(s):
    """E (V - s)_+"""
    return sum(binom[w] * max(Vw[w] - s, 0.0) for w in range(m + 1)) / NN


class Harper:
    """Harper's two tail functions on Q_mm for the slope uu (Lemma 11.43(b),(c) as quoted in N_REPORT 2.5 (R4))"""

    def __init__(self, mm, uu):
        self.m, self.u, self.N = mm, uu, 2 ** mm
        c = [math.comb(mm, j) for j in range(mm + 1)]
        self.ball = [sum(c[:r + 1]) for r in range(mm + 1)]
        self.E = [sum(c[j] * math.expm1(uu * (r + 1 - j)) for j in range(r + 1)) for r in range(mm + 1)]
        self.T = [sum(c[j] * math.exp(-uu * max(j - kk, 0)) for j in range(mm + 1)) for kk in range(mm + 1)]

    def radius(self, q):                       # q a Fraction or float: least r with |B(r)| >= 2^m q
        t = q * self.N
        for r in range(self.m + 1):
            if self.ball[r] >= t:
                return r
        return self.m

    def Xi(self, q):
        if q * self.N < 1:
            return 0.0
        r = self.radius(q)
        return INF if r >= self.m else self.E[r] / self.N

    def kball(self, count):                    # largest k with |B(k)| <= max(1, count)
        t = max(1, count)
        kk = 0
        while kk + 1 <= self.m and self.ball[kk + 1] <= t:
            kk += 1
        return kk

    def Theta(self, p):
        return self.T[self.kball(p * self.N)] / self.N

    def ThetaBar(self, p):
        return max(float(p), self.Theta(p))

    def closing_level(self, thrN, theta, ceta):
        """sup of the admissible pi_* : [N] Xi(q) <= thrN q and [P] Xi(q) <= theta ThetaBar(ceta q) for all q < pi.
        On the step (|B(r-1)|, |B(r)|]/2^m both hold throughout iff they hold in the limit at the left end."""
        rdag = -1
        for r in range(self.m):
            left = 1 if r == 0 else self.ball[r - 1]           # r = 0: the step is the single point q = 2^-m
            okN = self.E[r] <= thrN * left
            kap = self.kball(ceta * left) if r > 0 else 0
            okP = self.E[r] <= theta * max(float(ceta * left), self.T[kap])
            if okN and okP:
                rdag = r
            else:
                break
        return (self.ball[rdag] / self.N if rdag >= 0 else 1.0 / self.N), rdag


# ------------------------------------------------------------------------------------------------------------------
# 2. Algorithm A (N_REPORT 2.2), own implementation
# ------------------------------------------------------------------------------------------------------------------
class Consts:
    def __init__(self, lam, eta, etap, theta, nu1, b, xs, delta, kappa0, ell0, Vmax, tail):
        self.lam, self.eta, self.etap, self.theta, self.nu1, self.b = lam, eta, etap, theta, nu1, b
        self.xs, self.L = xs, len(xs) - 1
        assert all(xs[i] > xs[i + 1] for i in range(self.L)) and xs[-1] <= b
        e = float(eta)
        self.ceta = (1 - eta) / (1 + eta)
        self.s0 = kappa0 * ell0
        self.ell0, self.Vmax, self.kappa0 = ell0, Vmax, kappa0
        self.J = math.ceil(math.log(Vmax / self.s0) / lam - 1e-12)
        self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - e)
        self.pi_star, self.rdag = tail.closing_level(theta * (1 - e) * self.nu0, theta, self.ceta)
        self.m_max = math.ceil(math.log2(2 * (1 + e) * math.exp(lam) * self.nu0 / ((1 - e) * self.pi_star)))
        self.K = math.ceil(3 * (1 + e) / e ** 2 * math.log(2 * (self.J + 1) * (self.m_max + 1) * (self.L + 2) / delta))
        self.nu = self.K * self.nu0
        self.Mdag = self.K / ((1 - e) * self.pi_star)
        self.Mbar = 2 * (1 + e) * math.exp(lam) * self.nu0 * self.Mdag
        self.x_out = math.log(kappa0 + math.exp(b) * (math.exp(lam) * (1 + e) / (1 - e) + etap + theta))

    def cnt(self, x):
        e = float(self.eta)
        return max(self.K, 2 * (1 + e) ** 2 / (1 - e) * math.exp(self.lam) * self.nu * math.exp(x))


def run_A(rng, C, tail, mode):
    """Algorithm A.  Outer points: uniform on Q_m (only |a| matters: Binomial(m, 1/2)).
    Oracle: rung l returns a valid bracket of ratio e^{x_l} around the exact V(a); mode 0 exact value (L = U = V),
    1 random placement, 2 V at the top end, 3 V at the bottom end.  C_0 = C_l = 1, c_ref = 0 for the query count."""
    eta = C.eta
    e = float(eta)
    lam, b, theta = C.lam, C.b, C.theta
    Vtab = np.array(Vw)
    cap = int(min(C.K * 2 ** C.m_max, 4e7))
    # storage grows by doubling
    Vv = np.empty(0)
    Lo = np.empty(0)
    Up = np.empty(0)
    rung = np.empty(0, dtype=np.int64)
    queries = 0
    Cmax = 2 * C.Mbar + sum(min(2 * C.Mbar, (C.J + 1) * C.cnt(C.xs[l - 1])) for l in range(1, C.L + 1))

    def bracket(vals, x):
        if mode == 0:
            return vals.copy(), vals.copy()
        if mode == 1:
            xi = rng.random(len(vals))
        elif mode == 2:
            xi = np.ones(len(vals))
        else:
            xi = np.zeros(len(vals))
        return vals * np.exp(-xi * x), vals * np.exp((1 - xi) * x)

    del ENTRIES[:]                       # (j, ell at the entry of level j, M_j^neg) of every level reached in this run
    ell = C.ell0
    Sig = 0.0
    upper_sum = 0.0                      # sum_{i<j} (s_{i+1} - s_i) q_i
    levels = []                          # (j, kind, M, N, q, plow)
    j = 0
    while True:
        sj = C.s0 * math.exp(j * lam)
        if sj >= C.Vmax:                 # rule (c0)
            return dict(stop='cap', j=j, L=max(ell, Sig), U=C.s0 + upper_sum, levels=levels, npoints=len(Vv),
                        last=None, queries=queries, V=Vv)
        ell_j = ell
        Mneg = C.nu * sj / (ell_j * math.exp(b))
        ENTRIES.append((j, ell_j, Mneg))
        M = C.K
        while True:
            if M > C.K * 2 ** C.m_max:
                return dict(stop='abort-M', j=j, L=C.ell0, U=C.Vmax, levels=levels, npoints=len(Vv), last=None,
                            queries=queries, V=Vv)
            if M > cap:
                return dict(stop='abort-memory', j=j, L=C.ell0, U=C.Vmax, levels=levels, npoints=len(Vv), last=None,
                            queries=queries, V=Vv)
            if len(Vv) < M:              # draw the new points, rung-0 brackets
                add = M - len(Vv)
                w = rng.binomial(m, 0.5, size=add)
                nv = Vtab[w]
                l0, u0 = bracket(nv, C.xs[0])
                Vv = np.concatenate([Vv, nv])
                Lo = np.concatenate([Lo, l0])
                Up = np.concatenate([Up, u0])
                rung = np.concatenate([rung, np.zeros(add, dtype=np.int64)])
                queries += add
            # classify a_1..a_M at level j
            while True:
                idx = np.nonzero((Up[:M] > sj) & (Lo[:M] <= sj * math.exp(-b)))[0]
                if len(idx) == 0:
                    break
                if np.any(rung[idx] >= C.L):
                    return dict(stop='abort-rung', j=j, L=C.ell0, U=C.Vmax, levels=levels, npoints=len(Vv),
                                last=None, queries=queries, V=Vv)
                rung[idx] += 1
                queries += len(idx)
                for l in np.unique(rung[idx]):
                    sub = idx[rung[idx] == l]
                    nl, nu_ = bracket(Vv[sub], C.xs[l])
                    Lo[sub] = np.maximum(Lo[sub], nl)
                    Up[sub] = np.minimum(Up[sub], nu_)
            if queries > Cmax:
                return dict(stop='abort-cost', j=j, L=C.ell0, U=C.Vmax, levels=levels, npoints=len(Vv), last=None,
                            queries=queries, V=Vv)
            Nh = int(np.count_nonzero(Up[:M] > sj))
            q = min(Fraction(1), Fraction(max(Nh, C.K)) / ((1 - eta) * M))
            populated = Nh >= C.K
            plow = None
            if populated:
                plow = Fraction(Nh) / ((1 + eta) * M)
                ell = max(ell, sj * math.exp(-b) * tail.ThetaBar(plow))
            xi = tail.Xi(q)
            tl = sj * xi if xi < INF else INF
            if tl <= theta * math.exp(b) * ell:
                Lret = max(ell, Sig + ((1 - math.exp(-lam)) * math.exp(-b) * sj * float(plow) if populated else 0.0))
                Uret = C.s0 + upper_sum + tl
                return dict(stop='closed', j=j, L=Lret, U=Uret, levels=levels, npoints=len(Vv),
                            last=(j, M, Nh, q, plow, tl, sj), queries=queries, V=Vv)
            if populated:
                levels.append((j, 'pop', M, Nh, q, plow))
                Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * float(plow)
                upper_sum += (C.s0 * math.exp((j + 1) * lam) - sj) * float(q)
                break
            if M >= Mneg:
                levels.append((j, 'neg', M, Nh, q, None))
                upper_sum += (C.s0 * math.exp((j + 1) * lam) - sj) * float(q)
                break
            M *= 2
        j += 1


def check(res, C):
    """validity, width, truth of every sampled certificate, the Chernoff events on the realised sample"""
    out = {}
    out['valid'] = (res['L'] <= A * (1 + 1e-12)) and (A <= res['U'] * (1 + 1e-12))
    out['width'] = res['U'] <= math.exp(C.x_out) * res['L'] * (1 + 1e-12)
    cert = True
    for (j, kind, M, Nh, q, plow) in res['levels']:
        sj = C.s0 * math.exp(j * C.lam)
        if p_exact(sj) > float(q) + 1e-15:
            cert = False
        if kind == 'pop' and p_exact(sj * math.exp(-C.b)) < float(plow) - 1e-15:
            cert = False
    false_tail = None
    if res['last'] is not None:
        (j, M, Nh, q, plow, tl, sj) = res['last']
        if p_exact(sj) > float(q) + 1e-15:
            cert = False
        if plow is not None and p_exact(sj * math.exp(-C.b)) < float(plow) - 1e-15:
            cert = False
        false_tail = excess_exact(sj) / tl if tl > 0 else (INF if excess_exact(sj) > 0 else 0.0)
    out['cert'] = cert
    out['excess_over_tail'] = false_tail          # > 1: the tail bound s_j Xi(q) is false at the closing pass
    # (V2), (V3) literally, on the realised sample, for all j <= J and all M = K 2^i <= number of points drawn
    Vv = res['V']
    good = True
    e = float(C.eta)
    sizes = []
    M = C.K
    while M <= len(Vv):
        sizes.append(M)
        M *= 2
    thr2, thr3 = [], []
    for j in range(C.J + 1):
        sj = C.s0 * math.exp(j * C.lam)
        thr2.append(sj)
        thr3.append(sj * math.exp(-C.b))
        for l in range(C.L):
            thr3.append(sj * math.exp(-C.xs[l]))
    srt = {M: np.sort(Vv[:M]) for M in sizes}
    for M in sizes:
        a = srt[M]
        for t in thr2:
            X = M - int(np.searchsorted(a, t, side='right'))
            pt = p_exact(t)
            if not (M * pt <= C.K / (1 - e) or X >= (1 - e) * M * pt):
                good = False
        for t in thr3:
            X = M - int(np.searchsorted(a, t, side='right'))
            pt = p_exact(t)
            if not (X < C.K or X <= (1 + e) * M * pt):
                good = False
    out['chernoff'] = good
    return out


# ------------------------------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("Referee's reproduction of Proposition N12   (m = %d, k = %d, u = %g, J = %g, tau = %g)" % (m, k, u, Jc, tau))
    print("=" * 100)
    print("1. the instance")
    print("  |a|  count  p(a)=sigma(J(tau-|a|))   V(a)")
    for w in range(m + 1):
        print("  %2d  %5d   %.6f               %.6e" % (w, binom[w], pw[w], Vw[w]))
    spike = (binom[11] * Vw[11] + binom[12] * Vw[12]) / NN
    print("  A = %.8e;  share of the 13 points with |a| >= 11: %.6f %%" % (A, 100 * spike / A))
    print("  V at |a| = 10: %.4e   V at |a| <= 9: at most %.4e" % (Vw[10], max(Vw[:10])))
    edges = [math.log(Vw[w + 1] / Vw[w]) for w in range(m)]
    c = math.log((1 - sigma(-Jc / 2) * (1 - math.exp(-u))) / (1 - sigma(Jc / 2) * (1 - math.exp(-u))))
    print("  ln V(w+1)/V(w), w = 0..11: " + " ".join("%.4f" % x for x in edges))
    print("  largest edge ratio e^{%.4f};  k c(J,u) = %.4f  (c = %.5f; assumed slope u = %g)" % (max(edges), k * c, c, u))
    H1 = Harper(m, u)
    worst, where = 0.0, None
    print("  (TU) with Harper's function of slope u, at the levels s = V-values (p(s) = q exactly at ball sizes):")
    for w in range(m, 0, -1):
        s = Vw[w - 1] if w >= 1 else None
        s = Vw[w - 1]
        q = p_exact(s)
        xi = H1.Xi(Fraction(round(q * NN), NN))
        ex = excess_exact(s)
        if xi < INF and q > 0:
            ratio = ex / (s * xi)
            print("    s = V(|a|=%2d) = %.4e   q = %4d/4096   E(V-s)+ = %.4e   s Xi_u(q) = %.4e   ratio %.4g"
                  % (w - 1, s, round(q * NN), ex, s * xi, ratio))
            if ratio > worst:
                worst, where = ratio, w - 1
    print("  largest violation factor of (TU): %.4g  (at s = V(|a| = %d))" % (worst, where))
    D = 13 / NN
    s = Vw[10]
    print("  part (c): E(V-s)+ = %.4e >= s mu(D)(e^{kc}-1) = %.4e;   s Xi_u(mu(D)) = %.4e <= s mu(D)(e^{u(m-tau+1/2)}-1) = %.4e"
          % (excess_exact(s), s * D * math.expm1(k * c), s * H1.Xi(Fraction(13, NN)), s * D * math.expm1(u * (m - tau + 0.5))))
    print()
    print("2./3. Algorithm A, own implementation; reference data ell0 = e^{-uk} (V >= e^{-uk}), V_max = 1, kappa0 = 1")
    slope_true = max(edges)
    x0 = 2 * u * k
    half = Fraction(1, 2)
    psets = [
        ("theta=20", dict(lam=1.0, eta=half, etap=1.0, theta=20.0, nu1=1.0, b=1.0, delta=0.05)),
        ("theta=1 ", dict(lam=0.5, eta=half, etap=0.5, theta=1.0, nu1='b', b=0.5, delta=0.05)),
        ("referee ", dict(lam=0.5, eta=Fraction(1, 4), etap=0.5, theta=2.0, nu1=1.0, b=0.25, delta=0.01)),
    ]
    rng = np.random.default_rng(20261126)
    nbad_assumed = nrun_assumed = 0
    viol_true = 0
    for (label, slope) in (("ASSUMED class (slope u = 1)", u), ("TRUE class (slope %.3f)" % slope_true, slope_true)):
        H = Harper(m, slope)
        print("-" * 100)
        print("  tail functions: Harper's for the " + label)
        for (pname, P) in psets:
            nu1 = 2 * math.exp(slope) * m / P['theta'] if P['nu1'] == 'b' else P['nu1']
            xs = [x0, x0 / 3, x0 / 9, P['b']]
            C = Consts(P['lam'], P['eta'], P['etap'], P['theta'], nu1, P['b'], xs, P['delta'], 1.0, math.exp(-u * k), 1.0, H)
            nrep = 40 if slope == u else 12
            stops = {}
            inval = widthbad = certbad = chernbad = 0
            ratios, pts, exc, levs = [], [], [], []
            for rep in range(nrep):
                res = run_A(rng, C, H, rep % 4)
                stops[res['stop']] = stops.get(res['stop'], 0) + 1
                ch = check(res, C)
                inval += (not ch['valid'])
                widthbad += (not ch['width']) and res['stop'] in ('closed', 'cap')
                certbad += (not ch['cert'])
                chernbad += (not ch['chernoff'])
                ratios.append(A / res['U'])
                pts.append(res['npoints'])
                levs.append(res['j'])
                if ch['excess_over_tail'] is not None:
                    exc.append(ch['excess_over_tail'])
            print("  %s  J=%d K=%d pi_*=%.4g (r_dag=%d) Mbar=%.3g x_out=%.3f | runs %d stops %s | INVALID %d | width bad %d |"
                  % (pname, C.J, C.K, C.pi_star, C.rdag, C.Mbar, C.x_out, nrep, stops, inval, widthbad))
            print("            sampled certificates false in %d runs; Chernoff events (V2),(V3) violated in %d runs" % (certbad, chernbad))
            print("            A/U: min %.4g median %.4g max %.4g | outer points: median %d max %d | closing level j: %d..%d"
                  % (min(ratios), float(np.median(ratios)), max(ratios), int(np.median(pts)), max(pts), min(levs), max(levs)))
            if exc:
                print("            true E(V-s_j)+ / certified tail s_j Xi(q) at the closing pass: min %.4g median %.4g max %.4g"
                      % (min(exc), float(np.median(exc)), max(exc)))
            if slope == u:
                nbad_assumed += inval
                nrun_assumed += nrep
            else:
                viol_true += inval + widthbad + certbad
    print("=" * 100)
    print("assumed class: %d invalid brackets in %d runs;   true class: %d violations   (%.1f s)"
          % (nbad_assumed, nrun_assumed, viol_true, time.time() - t0))
    return 1 if viol_true else 0          # status 1 only if the VALID setting (true class) shows a violation


if __name__ == "__main__":
    sys.exit(main())
