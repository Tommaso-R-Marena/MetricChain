#!/usr/bin/env python3
"""R8 / script 02 -- Proposition A16.3 (plateau twin) by exact sums, own code.

The cube is summed exactly through the joint law of the two distances: if d_H(a0,a') = D and x
differs from a' in i of the D coordinates where a0 and a' differ and in j of the other n-D,
then d(x,a') = i+j, d(x,a0) = D-i+j, and there are C(D,i) C(n-D,j) such x.  (Validated against
a full enumeration of the cube at n = 16 in part 0.)

  g0   = -u (r1 - d(x,a0))_+                       visible basin
  T_k  = -u min(kappa, (r2 - d(x,a'))_+)           truncated cone (plateau of depth u kappa)
  g'_k = min(g0, T_k)

Excess identity (R6.1):  Z' = Z0 + E,   U' - U0 = F/(Z0 + E),
  E = sum (e^{-T} - e^{-g0})_+ ,   F = sum_{T<g0} [ e^{-T}(T - U0) - e^{-g0}(g0 - U0) ].
The root kappa* is the zero of F (no cancellation of two large mean energies).

Parts:
 0  validation of the joint-law sums against brute force (n = 16), and of the excess identity
 1  cases of my own choosing (n, u, rho1, target gap, distance of the centres):
    (a) sign of F at kappa_lo and at kappa = r2, the root, number of sign changes on a grid;
    (b) gap against ln|B(n, floor(r2 - kappa_lo))| - S0 - 1;
    (c) support of the difference inside B(a', r2-1);
    the deep-end condition written out in the report:  omega/W2 < 1/r2;
    predicted radii  (r2 - kappa*)/n ~ sigma2(gap/n),  r2/n ~ rho1 - sigma_u + sigma2(gap/n)
 2  for which n is there a root (u = 1, rho1 = rho0 + 0.01, r2 = r1 + 1 and a wide twin)
 3  centres that are NOT far apart (D = 0.1 n, 0.2 n): what happens to the statement

Run:  python3 r8_02_twin.py        (about 3 minutes)
"""
import math, sys, time
import numpy as np
from scipy.special import logsumexp
from r8_lib import *


class Twin:
    def __init__(self, n, u, r1, r2, D):
        self.n, self.u, self.r1, self.r2, self.D = n, u, r1, r2, D
        i = np.arange(D + 1)[:, None]
        j = np.arange(n - D + 1)[None, :]
        self.lc = lnC(D)[:, None] + lnC(n - D)[None, :]
        self.dp = (i + j).astype(float)              # distance to a'
        self.d0 = (D - i + j).astype(float)          # distance to a0
        self.g0 = -u * np.maximum(r1 - self.d0, 0.0)
        self.lnZ0, self.U0, self.S0 = basin_stats(n, u, r1)
        self.kappa_lo = (abs(self.U0) - 1.0) / u

    def T(self, kappa):
        return -self.u * np.minimum(kappa, np.maximum(self.r2 - self.dp, 0.0))

    def sums(self, kappa):
        """returns (ln E, F/E)  with F/E = m(kappa) - U0 ; also the mask"""
        T = self.T(kappa)
        mask = T < self.g0
        if not mask.any():
            return -np.inf, np.nan, mask
        lc = self.lc[mask]; Tm = T[mask]; gm = self.g0[mask]
        lwT = lc - Tm
        lw0 = lc - gm
        lE_terms = lwT + np.log1p(-np.exp(Tm - gm))
        lE = float(logsumexp(lE_terms))
        s = lE
        F = float(np.sum(np.exp(lwT - s) * (Tm - self.U0) - np.exp(lw0 - s) * (gm - self.U0)))
        return lE, F, mask

    def root(self):
        lo, hi = self.kappa_lo, float(self.r2)
        _, Flo, _ = self.sums(lo)
        _, Fhi, _ = self.sums(hi)
        if not (Flo > 0 and Fhi < 0):
            return None, Flo, Fhi
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            _, Fm, _ = self.sums(mid)
            if Fm > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi), Flo, Fhi

    def gap(self, kappa):
        lE, _, _ = self.sums(kappa)
        return float(np.logaddexp(0.0, lE - self.lnZ0))      # ln(1 + E/Z0)

    def deep_end(self):
        """omega/W2 at kappa = r2 (weight of the full cone of radius r2 inside the visible basin)"""
        T = self.T(float(self.r2))
        sup = T < 0
        ov = sup & (self.g0 < 0)
        lW2 = float(logsumexp((self.lc - T)[sup]))
        lom = float(logsumexp((self.lc - T)[ov])) if ov.any() else -np.inf
        return lom - lW2


def brute(n, u, r1, r2, D, kappa):
    N = 1 << n
    x = np.arange(N)
    pc = np.zeros(N, dtype=np.int64)
    for b in range(n):
        pc += (x >> b) & 1
    a0 = 0
    ap = (1 << D) - 1
    d0 = pc[x ^ a0]; dp = pc[x ^ ap]
    g0 = -u * np.maximum(r1 - d0, 0.0)
    T = -u * np.minimum(kappa, np.maximum(r2 - dp, 0.0))
    g = np.minimum(g0, T)
    out = []
    for f in (g0, g):
        w = np.exp(-f); Z = w.sum(); out += [math.log(Z), float((w * f).sum() / Z)]
    return out      # lnZ0, U0, lnZ', U'


def part0():
    print("== part 0: validation at n = 16 (full enumeration) ==")
    ok = True
    for (n, u, r1, r2, D, kappa) in [(16, 1.0, 7, 9, 8, 3.3), (16, 2.0, 6, 8, 5, 2.7), (16, 0.7, 8, 10, 11, 6.0),
                                     (16, 1.3, 7, 12, 3, 4.1)]:
        tw = Twin(n, u, r1, r2, D)
        lE, F, _ = tw.sums(kappa)
        lnZ0, U0, lnZp, Up = brute(n, u, r1, r2, D, kappa)
        # predictions of the excess identity
        Zp = math.exp(tw.lnZ0) + math.exp(lE)
        dU = F * math.exp(lE) / Zp
        e1 = abs(lnZ0 - tw.lnZ0); e2 = abs(U0 - tw.U0); e3 = abs(math.log(Zp) - lnZp); e4 = abs((Up - U0) - dU)
        print(f"  n={n} u={u} r1={r1} r2={r2} D={D} kappa={kappa}: errors lnZ0 {e1:.1e} U0 {e2:.1e} lnZ' {e3:.1e} "
              f"U'-U0 {e4:.1e}   (U'-U0 = {Up-U0:+.6f})")
        ok &= max(e1, e2, e3, e4) < 1e-10
    return ok


def find_case(n, u, rho1, eps1, Dfrac, verbose=True):
    """smallest r2 whose exact twin has gap > eps1*n; all checks"""
    s = sig(u)
    r1 = math.ceil(rho1 * n)
    D = int(round(Dfrac * n))
    lnZ0, U0, S0 = basin_stats(n, u, r1)
    s2 = sigma2(u, eps1)
    r2_pred = (r1 / n - s + s2) * n
    lbt = ln_ball_table(n)
    res = None
    r2 = max(r1 + 1, int(r2_pred) - 12)
    prev_gap = None
    while r2 < n // 2 + 5:
        tw = Twin(n, u, r1, r2, D)
        k, Flo, Fhi = tw.root()
        if k is None:
            r2 += 1
            continue
        gp = tw.gap(k)
        if gp > eps1 * n:
            res = (tw, k, gp, Flo, Fhi, prev_gap)
            break
        prev_gap = gp
        r2 += 1
    if res is None:
        print(f"  n={n} u={u} rho1={rho1:.4f} eps1={eps1:.4f} D={D}: NO twin found below n/2")
        return None
    tw, k, gp, Flo, Fhi, prev_gap = res
    # number of sign changes of F on a grid in (kappa_lo, r2]
    grid = np.linspace(tw.kappa_lo, r2, 121)
    Fs = np.array([tw.sums(kk)[1] for kk in grid])
    nsign = int(np.sum(np.sign(Fs[1:]) != np.sign(Fs[:-1])))
    rb = math.floor(r2 - tw.kappa_lo)
    bound_b = float(lbt[rb]) - tw.S0 - 1.0
    _, _, mask = tw.sums(k)
    c_ok = bool(np.all(tw.dp[mask] <= r2 - 1))
    lov = tw.deep_end()
    # support overlap: fraction of B(a', r2-1) inside the visible basin
    ball = tw.dp <= r2 - 1
    lfr = float(logsumexp(tw.lc[ball & (tw.g0 < 0)])) - float(logsumexp(tw.lc[ball])) if (ball & (tw.g0 < 0)).any() else -np.inf
    g1 = gp / n
    out = dict(n=n, u=u, rho1=rho1, r1=r1, r2=r2, D=D, kappa=k, kappa_lo=tw.kappa_lo, gap=gp, bound_b=bound_b,
               nsign=nsign, c_ok=c_ok, lnov=lov, lnsupov=lfr, U0=tw.U0, S0=tw.S0, lnZ0=tw.lnZ0, prev_gap=prev_gap)
    if verbose:
        print(f"  n={n} u={u} rho1=rho0+{rho1-rho0(u):.3f} r1={r1} D={D} target eps1={eps1:.4f} (eps={eps1*n:.2f}):")
        print(f"     S0-n h(sig)={tw.S0-n*hb(s):+.3e}  |U0|-u(r1-sig n)={abs(tw.U0)-u*(r1-s*n):+.3e}")
        print(f"     r2={r2} (formula {r2_pred:.1f})  kappa*={k:.4f} > kappa_lo={tw.kappa_lo:.4f}: {k>tw.kappa_lo}"
              f"   F(kappa_lo)>0: {Flo>0}  F(r2)<0: {Fhi<0}  sign changes on grid: {nsign}")
        print(f"     gap={gp:.4f}  bound (b)={bound_b:.4f}  gap-bound={gp-bound_b:+.3f}   gap at r2-1: "
              f"{'%.4f' % prev_gap if prev_gap is not None else 'n/a'}")
        print(f"     plateau edge (r2-kappa*)/n={(r2-k)/n:.5f} vs sigma2(gap/n)={sigma2(u,g1):.5f};  r2/n={r2/n:.5f} vs "
              f"rho1'-sig+sigma2={r1/n-s+sigma2(u,g1):.5f}")
        print(f"     (c) difference inside B(a',r2-1): {c_ok};  deep end: ln(omega/W2)={lov:.1f} against ln(1/r2)={-math.log(r2):.1f}"
              f" -> condition holds: {lov < -math.log(r2)};  ln(frac of B(a',r2-1) in V)={lfr:.1f}")
        print(f"     exponent  n^-1 ln(2^n/|B(n,r2-1)|) = {(n*LN2-float(lbt[r2-1]))/n:.5f} ;  asymptotic ln2-h(rho1-sig+sigma2(eps1)) = "
              f"{theta_pl(u,eps1,rho1):.5f} ; theta_hint(eps1)={theta_hint(u,eps1):.5f}")
    return out


def part1():
    print("== part 1: exact plateau twins (own cases) ==")
    ok = True
    cases = [
        (400, 1.0, rho0(1.0) + 0.03, 0.02, 0.5),
        (800, 1.0, rho0(1.0) + 0.02, 0.03, 0.5),
        (800, 1.0, rho0(1.0) + 0.02, 0.03, 0.42),
        (800, 1.0, rho0(1.0) + 0.02, 0.03, 0.58),
        (1500, 1.0, rho0(1.0) + 0.01, 0.05, 0.5),
        (1000, 2.0, rho0(2.0) + 0.01, 0.10, 0.5),
        (1000, 2.0, rho0(2.0) + 0.01, 0.20, 0.47),
        (700, 4.0, rho0(4.0) + 0.01, 0.30, 0.5),
        (700, 4.0, rho0(4.0) + 0.01, 0.45, 0.53),
        (1200, 0.5, rho0(0.5) + 0.01, 0.006, 0.5),
        (900, 3.0, rho0(3.0) + 0.015, 0.25, 0.5),
        (2400, 1.0, rho0(1.0) + 0.005, 0.02, 0.5),
    ]
    rows = []
    for c in cases:
        r = find_case(*c)
        if r is None:
            ok = False
            continue
        rows.append(r)
        ok &= r["kappa"] > r["kappa_lo"] and r["gap"] >= r["bound_b"] and r["c_ok"]
    return ok, rows


def part2():
    print("== part 2: for which n is there a root (u=1, rho1=rho0+0.01, D=n/2) ==")
    u = 1.0
    for n in (60, 100, 150, 200, 250, 300, 350, 400, 500, 600, 800):
        r1 = math.ceil((rho0(u) + 0.01) * n)
        lnZ0, U0, S0 = basin_stats(n, u, r1)
        line = f"  n={n:4d} r1={r1:3d} U0={U0:+8.3f} kappa_lo={(abs(U0)-1)/u:7.3f} ln(W/2^n)~{u*(r1-rho0(u)*n):5.2f}:"
        for k in (1, max(2, int(0.03 * n))):
            r2 = r1 + k
            if r2 >= n // 2:
                continue
            tw = Twin(n, u, r1, r2, n // 2)
            kap, Flo, Fhi = tw.root()
            line += f"  r2=r1+{k}: " + ("root %.3f gap %.3f" % (kap, tw.gap(kap)) if kap is not None else
                                         f"NO ROOT (F(kappa_lo)>0:{Flo>0}, F(r2)<0:{Fhi<0})")
        print(line)
    return True


def part3():
    print("== part 3: centres that are close (the statement asks for |D - n/2| <= sqrt(n ln n)) ==")
    n, u = 800, 1.0
    r1 = math.ceil((rho0(u) + 0.02) * n)
    for Dfrac in (0.5, 0.35, 0.25, 0.15, 0.08):
        D = int(Dfrac * n)
        line = f"  n={n} D={D} (sqrt(n ln n)={math.sqrt(n*math.log(n)):.0f}):"
        for k in (1, 30):
            tw = Twin(n, u, r1, r1 + k, D)
            kap, Flo, Fhi = tw.root()
            lov = tw.deep_end()
            line += f"  r2=r1+{k}: ln(omega/W2)={lov:7.1f} " + (f"root {kap:.3f} gap {tw.gap(kap):.3f}" if kap is not None
                                                             else f"NO ROOT (Flo>0:{Flo>0},Fhi<0:{Fhi<0})")
        print(line)
    return True


if __name__ == "__main__":
    t0 = time.time()
    ok0 = part0()
    ok1, rows = part1()
    part2()
    part3()
    print("SUMMARY part0", ok0, "part1 (a),(b),(c) in all cases:", ok1, f" time {time.time()-t0:.0f}s")
    sys.exit(0 if (ok0 and ok1) else 1)
