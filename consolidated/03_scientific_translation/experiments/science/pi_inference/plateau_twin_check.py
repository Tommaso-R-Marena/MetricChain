"""Addendum A16: a thermodynamic datum at extensive accuracy -- the plateau twin, exactly.

Units beta = 1, c = u.  Cube Q_n, zero known part.
  base instance   g0(x) = -u (r1 - d(x,a0))_+                       (a visible cone basin that dominates Z)
  plateau twin    T(x)  = -u min(kappa, (r2 - d(x,a'))_+)            (a truncated cone: plateau of depth u*kappa)
  hidden instance g'    = min(g0, T),   d(a0,a') = D.
For every integer r2 we look for the real kappa* with  E_{mu_g'} g' = E_{mu_g0} g0  EXACTLY (the datum cannot
tell g' from g0), and report  gap = ln Z' - ln Z0.  An algorithm with the exact datum and accuracy gap/2 must
evaluate g inside B(a', r2 - 1) for (almost) every a':  E[#evaluations] >= (1-2 delta)(1-o(1)) 2^n / |B(n, r2-1)|.

Exact sums over the joint law of (d(x,a0), d(x,a')) for uniform x (overlapping supports included), as in
calorimetric_twin_exact.py.  Compared with
  * the no-datum lower bound for the same gap (theory report Theorem 11.25: smallest cone dip on the flat instance),
  * the asymptotic formulas of the addendum:
      plateau radius  rho2 = rho1 - sigma + hinv(h(sigma) + eps1),   sigma = 1/(1+e^u),
      hinted radius   rho0 + eps1/u,                                 rho0 = ln(2/(1+e^-u))/u.

Usage:  python3 plateau_twin_check.py            (about two minutes)
"""
from __future__ import annotations
import math, sys, json, os
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def logbinom(n, d):
    return gammaln(n + 1) - gammaln(d + 1) - gammaln(n - d + 1)

def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x*math.log(x) - (1 - x)*math.log(1 - x)

def hinv(y):
    """inverse of the binary entropy (nats) on [0, 1/2]"""
    return brentq(lambda x: h(x) - y, 1e-15, 0.5)

def log_ball(n, r):
    """ln |B(n, r)| = ln sum_{d<=r} C(n,d)"""
    d = np.arange(0, int(r) + 1)
    return float(logsumexp(logbinom(n, d)))

class Pair:
    """exact joint law of the two distances for d(a0,a') = D"""
    def __init__(self, n, u, r1, D):
        self.n, self.u, self.r1, self.D = n, u, r1, D
        t = np.arange(D + 1)[:, None]; q = np.arange(n - D + 1)[None, :]
        self.lm = logbinom(D, t) + logbinom(n - D, q) - n*math.log(2)
        self.d0 = (t + q).astype(float); self.d1 = (D - t + q).astype(float)
        self.depth0 = u*np.maximum(r1 - self.d0, 0.0)
        self.logZ0, self.U0 = self._ZU(self.depth0)

    def _ZU(self, depth):
        logZ = logsumexp(self.lm + depth)
        pos = depth > 0
        U = -math.exp(logsumexp((self.lm + depth)[pos] + np.log(depth[pos])) - logZ)
        return float(logZ), U

    def twin(self, r2, kappa):
        """(ln E, m): E = excess mass of the twin (units 2^n), m = mean energy of the excess mass.
        Cancellation-free (referee's Lemma R6.1): U' - U0 = (E/(Z0+E)) (m - U0), so U' = U0 iff m = U0."""
        depth2 = self.u*np.minimum(kappa, np.maximum(r2 - self.d1, 0.0))
        sel = depth2 > self.depth0
        d2 = depth2[sel]; d0 = self.depth0[sel]; lm = self.lm[sel]
        le = lm + d2 + np.log1p(-np.exp(d0 - d2))                 # ln of mu(x) (e^{d2} - e^{d0})
        logE = float(logsumexp(le))
        # sum of mu(x) (d2 e^{d2} - d0 e^{d0}) > 0, term by term
        num = float(logsumexp(lm + d2 + np.log(d2 - d0*np.exp(d0 - d2))))
        return logE, -math.exp(num - logE)

    def root(self, r2):
        """kappa* in (0, r2) with U' = U0 exactly, i.e. mean excess energy = U0 (kappa -> 0 is the trivial end)."""
        f = lambda k: self.twin(r2, k)[1] - self.U0
        lo, hi = 1e-3, float(r2)
        flo, fhi = f(lo), f(hi)
        if not (flo > 0 > fhi):
            return None
        k = brentq(f, lo, hi, xtol=1e-12, rtol=1e-15)
        logE, m = self.twin(r2, k)
        gap = math.log1p(math.exp(logE - self.logZ0)) if logE - self.logZ0 < 700 else logE - self.logZ0
        return k, gap, m - self.U0

def hinted_radius(n, u, gap):
    """smallest r such that the cone dip of radius r on the FLAT instance raises ln Z by more than gap"""
    d = np.arange(0, n//2 + 1)
    lb = logbinom(n, d) - n*math.log(2)
    for r in range(1, n//2 + 1):
        dd = d[:r]                                      # d < r
        W = math.exp(logsumexp(lb[:r] + u*(r - dd)))    # in units of 2^n
        V = math.exp(logsumexp(lb[:r]))
        if math.log1p(W - V) > gap:
            return r
    return None

def study(n, u, margin, eps1, D=None, out=None):
    sigma = 1/(1 + math.exp(u)); rho0 = math.log(2/(1 + math.exp(-u)))/u
    a = math.log(2) - h(sigma)
    rho1 = rho0 + margin; r1 = math.ceil(rho1*n)
    D = n//2 if D is None else D
    P = Pair(n, u, r1, D)
    target = eps1*n
    # smallest r2 whose root gives gap > target (the gap at the root increases with r2): bisection on r2
    rho2_asym = (r1/n - sigma) + hinv(min(h(sigma) + eps1, math.log(2) - 1e-12))
    lo = r1; hi = min(n//2 + n//8, int(rho2_asym*n) + 60)
    res_hi = P.root(hi)
    while res_hi is None or res_hi[1] <= target:
        hi += 40
        if hi > n - 2: return None
        res_hi = P.root(hi)
    while hi - lo > 1:
        mid = (lo + hi)//2
        r = P.root(mid)
        if r is not None and r[1] > target: hi, res_hi = mid, r
        else: lo = mid
    r2 = hi; kappa, gap, dU = res_hi
    S0 = P.logZ0 + n*math.log(2) + P.U0                     # Gibbs entropy of the base instance: ln Z0 + U0 (beta = 1)
    klo = (abs(P.U0) - 1)/u                                 # f(kappa) > 0 for kappa < klo (m >= -u kappa - 1), so kappa* > klo
    gap_bound = log_ball(n, math.floor(r2 - klo)) - S0 - 1  # proved: gap >= ln|B(n, floor(r2 - klo))| - S0 - 1 - o(1)
    assert kappa > klo, (kappa, klo)
    assert gap >= gap_bound - 1e-6, (gap, gap_bound)
    rh = hinted_radius(n, u, gap)
    ex_pl = math.log(2) - log_ball(n, r2 - 1)/n
    ex_hint = math.log(2) - log_ball(n, rh - 1)/n if rh else float("nan")
    ex_old = math.log(2) - log_ball(n, r1)/n - gap/n       # e^{gap} equal twins of radius r1
    row = dict(n=n, u=u, rho0=rho0, sigma=sigma, a=a, r1=r1, D=D, eps1=eps1, r2=r2, kappa=kappa, gap=gap,
               dU=dU, U0_over_n=P.U0/n, S0_over_n=S0/n, kappa_lo=klo, gap_lower_bound=gap_bound, plateau_radius_over_n=(r2 - kappa)/n, rho2=r2/n, rho2_asym=rho2_asym,
               hinted_r=rh, hinted_rho_asym=rho0 + gap/n/u,
               exponent_plateau=ex_pl, exponent_hinted=ex_hint, exponent_equal_twins=ex_old,
               exponent_plateau_asym=math.log(2) - h(min(0.5, rho0 - sigma + hinv(min(h(sigma) + eps1, math.log(2) - 1e-12)))),
               exponent_hinted_asym=math.log(2) - h(min(0.5, rho0 + eps1/u)))
    print(f"n={n} u={u} eps1={eps1:.3f} D={D}: r1={r1} r2={r2} kappa*={kappa:.4f} (m-U0={dU:+.1e}) gap/n={gap/n:.5f} "
          f"| plateau edge (r2-kappa)/n={(r2-kappa)/n:.4f} [hinv(h(sigma)+gap/n)={hinv(min(h(sigma)+gap/n, math.log(2)-1e-12)):.4f}] "
          f"rho2={r2/n:.4f} [asym {rho2_asym:.4f}] | hinted r={rh} "
          f"| exponents at this n: equal twins {ex_old:+.5f} <= plateau {ex_pl:.5f} <= no datum {ex_hint:.5f} "
          f"| S0/n={S0/n:.5f} [h(sigma)={h(sigma):.5f}] proved gap bound {gap_bound:.2f} <= gap {gap:.2f}", flush=True)
    if out is not None: out.append(row)
    return row

def entropy_bracket_check(seed=0, trials=400):
    """n h(sigma_u) <= ln Z_g + U_g <= n ln 2 for random u-Lipschitz g on small cubes (exact enumeration), and
    equality at the cone / at the flat function.  Random members: lower and upper McShane envelopes of random
    data, cones, dips, and their minima/maxima."""
    rng = np.random.default_rng(seed); worst_lo = math.inf; worst_hi = math.inf; cnt = 0
    for _ in range(trials):
        n = int(rng.integers(3, 12)); u = float(rng.choice([0.3, 1.0, 2.5, 5.0]))
        X = ((np.arange(2**n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
        m = int(rng.integers(1, 6)); idx = rng.integers(0, 2**n, size=m)
        dist = (X[:, None, :] != X[idx][None, :, :]).sum(axis=2).astype(float)       # N x m
        vals = rng.normal(0, u*n/3, size=m)
        kind = int(rng.integers(0, 4))
        if kind == 0:   g = np.min(vals[None, :] + u*dist, axis=1)                    # upper McShane envelope (Lipschitz)
        elif kind == 1: g = np.max(vals[None, :] - u*dist, axis=1)                    # lower envelope
        elif kind == 2: g = np.minimum(0.0, np.min(-u*np.maximum(rng.integers(1, n+1, size=m)[None, :] - dist, 0), axis=1))
        else:                                                                         # convex combination of a cone and dips
            al = rng.uniform(0, 1)
            g = al*u*dist[:, 0] + (1 - al)*np.min(-u*np.maximum(n//2 - dist, 0), axis=1)
        # verify membership (single flips suffice on the cube)
        for i in range(n):
            assert np.max(np.abs(g - g[np.arange(2**n) ^ (1 << i)])) <= u + 1e-9
        w = -g; lz = float(logsumexp(w)); mu = np.exp(w - lz); U = float(mu @ g); S = lz + U
        sig = 1/(1 + math.exp(u))
        worst_lo = min(worst_lo, S - n*h(sig)); worst_hi = min(worst_hi, n*math.log(2) - S); cnt += 1
        assert S >= n*h(sig) - 1e-9 and S <= n*math.log(2) + 1e-9
    # equality cases
    n, u = 10, 1.3; X = ((np.arange(2**n)[:, None] >> np.arange(n)[None, :]) & 1); d = X.sum(axis=1).astype(float)
    for name, g in (("cone", u*d), ("flat", 0*d)):
        lz = float(logsumexp(-g)); mu = np.exp(-g - lz); S = lz + float(mu @ g)
        print(f"# entropy bracket, {name}: S = {S:.10f}; n h(sigma) = {n*h(1/(1+math.exp(u))):.10f}; n ln 2 = {n*math.log(2):.10f}")
    print(f"# entropy bracket n h(sigma_u) <= ln Z + U <= n ln 2: {cnt} random members of the class (n = 3..11, u in 0.3..5), "
          f"no violation; smallest slack below {worst_lo:.1e}, above {worst_hi:.1e}")

if __name__ == "__main__":
    out = []
    entropy_bracket_check()
    print("# asymptotic table (per site): accuracy eps1 | equal twins h - eps1 | plateau twin | no datum theta_hint | window end a | ln cosh(u/2)")
    for u in (1.0, 2.0, 4.0):
        sigma = 1/(1 + math.exp(u)); rho0 = math.log(2/(1 + math.exp(-u)))/u; a = math.log(2) - h(sigma)
        hh = math.log(2) - h(rho0); thr = math.log(math.cosh(u/2))
        eps_c = h(0.5 - rho0 + sigma) - h(sigma)
        print(f"# u={u}: sigma={sigma:.4f} rho0={rho0:.4f} h={hh:.5f} a={a:.5f} ln cosh(u/2)={thr:.5f}  plateau bound void from eps1^c={eps_c:.5f}")
        for frac in (0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
            e1 = frac*a
            pl = math.log(2) - h(min(0.5, rho0 - sigma + hinv(min(h(sigma) + e1, math.log(2) - 1e-12))))
            hi_ = math.log(2) - h(min(0.5, rho0 + e1/u))
            print(f"#   eps1={e1:.5f} ({frac:.2f} a): {hh - e1:+.5f} | {pl:.5f} | {hi_:.5f}")
    print("# free accuracy per site: with the datum a(u) = KL(sigma||1/2); without it ln cosh(u/2) = KL(1/2||sigma); difference = sum_{k>=2} t^{2k}(k-1)/(k(2k-1)), t = tanh(u/2)")
    for u in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        sigma = 1/(1 + math.exp(u)); a = math.log(2) - h(sigma); t = math.tanh(u/2)
        klr = 0.5*math.log(1/(2*sigma)) + 0.5*math.log(1/(2*(1 - sigma)))
        # the series converges like t^{2k}/(2k); at u = 8 (t = 0.99933) 4000 terms are not enough -- the
        # first committed version truncated there, failed the assertion below and never reached the
        # twins (found by the referee, workstream R8, finding F7).  Sum until the tail bound is negligible.
        ser = 0.0; k = 2
        while True:
            term = t**(2*k)*(k - 1)/(k*(2*k - 1))
            ser += term
            if term/(1 - t*t) < 1e-13: break      # geometric bound on the remaining tail
            k += 1
        rho0 = math.log(2/(1 + math.exp(-u)))/u
        assert abs(klr - math.log(math.cosh(u/2))) < 1e-12 and abs((klr - a) - ser) < 1e-9
        print(f"#   u={u}: a={a:.6f}  ln cosh(u/2)={klr:.6f}  difference={klr - a:.6f} (series {ser:.6f})  "
              f"no-datum exponent at eps1 = a: {math.log(2) - h(min(0.5, rho0 + a/u)):.6f}")
    print("# exact finite-n checks (overlapping supports, D = n/2 unless stated)")
    for (n, u, margin, eps1) in [(1000, 1.0, 0.02, 0.02), (1000, 1.0, 0.02, 0.05), (2000, 1.0, 0.01, 0.02),
                                 (2000, 1.0, 0.01, 0.05), (1000, 2.0, 0.02, 0.05), (1000, 2.0, 0.02, 0.15),
                                 (600, 4.0, 0.03, 0.10), (600, 4.0, 0.03, 0.30)]:
        study(n, u, margin, eps1, out=out)
    for D in (450, 550):
        study(1000, 1.0, 0.02, 0.05, D=D, out=out)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plateau_twin_check.json"), "w"), indent=1)
