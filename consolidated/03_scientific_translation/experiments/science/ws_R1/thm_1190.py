#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- independent replication of Theorem 11.90 (b), (c) and of the table of numbers.

Objects (theory report section 11.25, "Slices").  kappa in (0,1) the density of the slice, u > 0, a centre of
type m.  Two-block profiles of type kappa form the ray  (a, b) = (kappa + l/2m, kappa - l/(2(1-m))),
    F(l)    = m KL(a || kappa) + (1-m) KL(b || kappa)            (= MI of the profile)
    Psi(s)  = max_{l >= 0} [s l - F(l)]
    F*(t)   = t Psi(u) - Psi(t u),      F*_c(t) = t ln cosh(u/2) - ln cosh(t u/2).
Claims replicated here:
 (b)  V_{m,kappa}(e) := sup_{shells l} min{F(l'): u|l'-l| <= e + F(l)}  = F((Psi(u)-e)_+/u) = max_{0<=t<=1}[F*(t) - t e]
      N_{m,kappa}(X) := sup_{shells l} min{F(l'): F(l') + u|l'-l| - F(l) <= X} = F(l_X) = max_{0<=tau<1}(F*(tau) - tau X)/(1-tau)
      -- the left-hand sides by BRUTE FORCE (dense grids over the whole ray, both signs of l, then local polishing),
         with no use of monotonicity or duality;
 (c)  F*_{m,kappa}(t) <= F*_c(t), equality only at m = kappa = 1/2; the behaviour near the equality case;
      the referee's stronger statement Psi''_{m,kappa}(s) <= Psi_c''(s) (curvature domination);
 table: R^kappa(0), the best centre type, N^kappa(0+) for u = 1 (and u = 2).
Run:  python3 thm_1190.py        (about 2-3 minutes)
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar

LOG2 = math.log(2.0)


def xlogy(x, y):
    return 0.0 if x <= 0.0 else x * math.log(y)


def kl(y, k):
    """binary KL(y || k), 0 <= y <= 1, 0 < k < 1"""
    return xlogy(y, y / k) + xlogy(1.0 - y, (1.0 - y) / (1.0 - k))


def logit(x):
    return math.log(x) - math.log1p(-x)


class Ray:
    """two-block profiles of type kappa for a centre of type m, parametrised by l in [l_lo, l_hi]"""

    def __init__(self, m, kappa):
        self.m, self.k = m, kappa
        self.l_hi = min(2 * m * (1 - kappa), 2 * (1 - m) * kappa)
        self.l_lo = -min(2 * m * kappa, 2 * (1 - m) * (1 - kappa))

    def ab(self, l):
        return self.k + l / (2 * self.m), self.k - l / (2 * (1 - self.m))

    def F(self, l):
        a, b = self.ab(l)
        a = min(max(a, 0.0), 1.0)
        b = min(max(b, 0.0), 1.0)
        return self.m * kl(a, self.k) + (1 - self.m) * kl(b, self.k)

    def Fp(self, l):
        a, b = self.ab(l)
        return 0.5 * (logit(a) - logit(b))

    def l_of_s(self, s):
        """the point of the ray with slope F'(l) = s >= 0, i.e. the 2x2 table with marginals (m, kappa) and log odds
        ratio 2s (closed form, Plackett's quadratic written without cancellation); l = 2 (P11 - m kappa)"""
        if s == 0.0:
            return 0.0
        m, k = self.m, self.k
        w = math.expm1(2 * s)                      # psi - 1
        B = 1.0 + w * (m + k)
        disc = 1.0 + 2.0 * w * (m + k - 2 * m * k) + w * w * (m - k) ** 2
        # P11 - m k = [2(1+w) m k - m k (B + sqrt(disc))] / (B + sqrt(disc)); expand the numerator analytically:
        # 2(1+w) - B - sqrt(disc) = (1 + 2w - w(m+k)) - sqrt(disc) = (A^2 - disc)/(A + sqrt(disc)), A = 1 + w(2 - m - k)
        A = 1.0 + w * (2.0 - m - k)
        num = A * A - disc                           # = 4 w (1+w) (1-m)(1-k)   (exact identity, checked below)
        num = 4.0 * w * (1.0 + w) * (1 - m) * (1 - k)
        sq = math.sqrt(disc)
        return 2.0 * m * k * num / ((A + sq) * (B + sq))

    def l_of_s_root(self, s):
        """the same point by root finding on F'(l) = s (independent check)"""
        hi = self.l_hi
        f = lambda l: self.Fp(l) - s
        lo_, hi_ = 0.0, hi
        for _ in range(200):                         # bisection that never evaluates at the end point
            mid = 0.5 * (lo_ + hi_)
            if mid <= lo_ or mid >= hi_:
                break
            if f(mid) < 0:
                lo_ = mid
            else:
                hi_ = mid
        return 0.5 * (lo_ + hi_)

    def Psi(self, s):
        l = self.l_of_s(s)
        return s * l - self.F(l)

    def Psi_dual(self, s):
        """independent formula: min{ m Lam(th1) + (1-m) Lam(th2) : th1 - th2 = 2 s }"""
        k = self.k
        Lam = lambda th: (th + math.log((1 - k) * math.exp(-th) + k) if th > 0 else math.log(1 - k + k * math.exp(th))) - k * th
        g = lambda th2: self.m * Lam(th2 + 2 * s) + (1 - self.m) * Lam(th2)
        # the minimiser lies in [-2s, 0]: the derivative m Lam'(th2+2s) + (1-m) Lam'(th2) changes sign there
        r = minimize_scalar(g, bounds=(-2 * s, 0.0), method="bounded", options={"xatol": 1e-14})
        return min(r.fun, g(-2 * s), g(0.0))

    def Fstar(self, t, u):
        return t * self.Psi(u) - self.Psi(t * u)

    # ---------------- closed forms of Theorem 11.90(b) ----------------
    def V_closed(self, e, u):
        return self.F(max(self.Psi(u) - e, 0.0) / u)

    def V_game(self, e, u):
        f = lambda t: -(self.Fstar(t, u) - t * e)
        r = minimize_scalar(f, bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-13})
        return max(-r.fun, -f(0.0), -f(1.0))

    def N_closed(self, X, u):
        psi = self.Psi(u)
        lstar = self.l_of_s(u)
        if X >= psi:
            return 0.0
        g = lambda l: u * l - self.F(l) - (psi - X)
        if g(lstar) <= 0:          # X = 0
            return self.F(lstar)
        lX = brentq(g, 0.0, lstar, xtol=1e-16, rtol=1e-15)
        return self.F(lX)

    def N_game(self, X, u):
        f = lambda tau: -(self.Fstar(tau, u) - tau * X) / (1 - tau)
        best = 0.0
        # the maximiser may sit close to tau = 1 when X is small; scan then polish
        taus = np.concatenate([np.linspace(0, 0.99, 100), 1 - np.logspace(-2, -9, 60)])
        vals = [-f(t) for t in taus]
        i = int(np.argmax(vals))
        lo, hi = taus[max(i - 1, 0)], taus[min(i + 1, len(taus) - 1)]
        r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-14})
        return max(best, vals[i], -r.fun)

    # ---------------- brute force (no monotonicity, no duality) ----------------
    def _minF_on(self, lo, hi):
        lo, hi = max(lo, self.l_lo), min(hi, self.l_hi)
        if hi < lo:
            return math.inf
        if hi - lo < 1e-15:
            return self.F(lo)
        r = minimize_scalar(self.F, bounds=(lo, hi), method="bounded", options={"xatol": 1e-15})
        return min(r.fun, self.F(lo), self.F(hi))

    def r_shell(self, l, e, u):
        """min{F(l') : u |l' - l| <= e + F(l)} over the whole ray"""
        w = (e + self.F(l)) / u
        if w < 0:
            return -math.inf           # infeasible shell
        return self._minF_on(l - w, l + w)

    def V_brute(self, e, u, ngrid=401, side=+1):
        # shells with l >= 0 are those of the centre m; the part l <= 0 of the ray consists of the shells of the
        # antipodal centre (type 1-m).  The EXITS always range over the whole ray.
        ls = np.linspace(0.0, self.l_hi, ngrid) if side > 0 else np.linspace(self.l_lo, 0.0, ngrid)
        vals = np.array([self.r_shell(l, e, u) for l in ls])
        i = int(np.argmax(vals))
        lo, hi = ls[max(i - 1, 0)], ls[min(i + 1, ngrid - 1)]
        r = minimize_scalar(lambda l: -self.r_shell(l, e, u), bounds=(lo, hi), method="bounded",
                            options={"xatol": 1e-15})
        return max(vals[i], -r.fun)

    def n_shell(self, l, X, u):
        """min{F(l') : F(l') + u|l'-l| - F(l) <= X} over the whole ray.  phi(l') := F(l') + u|l'-l| - F(l) - X is convex,
        so the feasible set is an interval; it is located from a minimiser of phi (NOT from l itself: for X = 0,
        phi(l) = 0 and a root finder started at l returns l -- a bug of the first version of this script)."""
        c = X + self.F(l)
        phi = lambda x: self.F(x) + u * abs(x - l) - c
        if phi(l) > 1e-15:
            return -math.inf
        # minimiser of the convex phi: either the kink l or a point on one side
        cands = [l]
        for (lo, hi) in ((self.l_lo, l), (l, self.l_hi)):
            if hi - lo > 1e-15:
                r = minimize_scalar(phi, bounds=(lo, hi), method="bounded", options={"xatol": 1e-15})
                cands.append(r.x)
        x0 = min(cands, key=phi)
        if phi(x0) > -1e-14:                 # the feasible set is (numerically) the single point l
            return self.F(l)
        lo = self.l_lo if phi(self.l_lo) <= 0 else brentq(phi, self.l_lo, x0, xtol=1e-14, maxiter=500)
        hi = self.l_hi if phi(self.l_hi) <= 0 else brentq(phi, x0, self.l_hi, xtol=1e-14, maxiter=500)
        return self._minF_on(lo, hi)

    def N_brute(self, X, u, ngrid=401, side=+1):
        ls = np.linspace(0.0, self.l_hi, ngrid) if side > 0 else np.linspace(self.l_lo, 0.0, ngrid)
        vals = np.array([self.n_shell(l, X, u) for l in ls])
        i = int(np.argmax(vals))
        lo, hi = ls[max(i - 1, 0)], ls[min(i + 1, ngrid - 1)]
        r = minimize_scalar(lambda l: -self.n_shell(l, X, u), bounds=(lo, hi), method="bounded",
                            options={"xatol": 1e-15})
        return max(vals[i], -r.fun)


def Psi_c(s):
    a = abs(s) / 2
    return a + math.log1p(math.exp(-2 * a)) - LOG2


def Fstar_c(t, u):
    return t * Psi_c(u) - Psi_c(t * u)


def R_unif(e, u):
    """KL(1/2 + (Psi_c(u) - e)_+/u || 1/2)"""
    x = max(Psi_c(u) - e, 0.0) / u
    return kl(0.5 + x, 0.5)


def theta_na_cube(X, u):
    """min{KL(rho||1/2) : KL(rho||p_u) <= X},  p_u = sigma(u)  (mismatch form), by its own definition"""
    pu = 1 / (1 + math.exp(-u))
    if kl(0.5, pu) <= X:
        return 0.0
    rho = brentq(lambda r: kl(r, pu) - X, 0.5, pu, xtol=1e-16)
    return kl(rho, 0.5)


results = {}


def report(name, ok, detail):
    results[name] = ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    sys.stdout.flush()


# ------------------------------------------------------------------------------------------------------------
def test_definitions():
    """m = kappa = 1/2 reduces to the cube; the two formulas for Psi agree"""
    rng = np.random.default_rng(1)
    err = 0.0
    for u in (0.3, 1.0, 2.5):
        ray = Ray(0.5, 0.5)
        for s in np.linspace(0.01, 6, 25):
            err = max(err, abs(ray.Psi(s) - Psi_c(s)))
        for e in (-0.05, 0.0, 0.02, 0.1):
            err = max(err, abs(ray.V_closed(e, u) - R_unif(e, u))) if e > -0.01 else err
        for X in (0.0, 0.01, 0.05, 0.2):
            err = max(err, abs(ray.N_closed(X, u) - theta_na_cube(X, u)))
    err2 = err3 = 0.0
    for _ in range(300):
        m, k, s = rng.uniform(0.03, 0.97), rng.uniform(0.03, 0.97), rng.uniform(0.01, 6)
        ray = Ray(m, k)
        err2 = max(err2, abs(ray.Psi(s) - ray.Psi_dual(s)))
        err3 = max(err3, abs(ray.l_of_s(s) - ray.l_of_s_root(s)), abs(ray.Fp(ray.l_of_s(s)) - s) * 1e-3)
    print(f"      l_of_s closed form vs bisection on F'(l)=s: {err3:.2e}")
    report("defs", err < 1e-12 and err2 < 1e-9 and err3 < 1e-12,
           f"m=kappa=1/2: |Psi - ln cosh(s/2)|, |V - R_unif|, |N - theta_na^cube| <= {err:.2e}; "
           f"Psi (primal root) vs Psi (dual formula with Lambda_kappa), 300 random (m,kappa,s): <= {err2:.2e}")


def test_closed_forms(n_cases=24, seed=11):
    """Theorem 11.90(b): brute force over the ray against the closed form and the game form"""
    rng = np.random.default_rng(seed)
    eV = eVg = eN = eNg = eMir = 0.0
    worst = None
    cases = [(0.5, 0.5, 1.0), (0.408, 0.3, 1.0), (0.3, 0.3, 1.0), (0.7, 0.3, 2.0), (0.1, 0.9, 0.5), (0.9, 0.9, 3.0)]
    cases += [(rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95), float(rng.choice([0.25, 0.5, 1.0, 2.0, 4.0])))
              for _ in range(n_cases - len(cases))]
    n_neg = 0
    for (m, k, u) in cases:
        ray = Ray(m, k)
        psi = ray.Psi(u)
        Fstar_l = ray.F(ray.l_of_s(u))
        # accuracies: e >= 0 (claimed closed form), and negative e down to below -F(l*) (claimed game form, value -e)
        es = [0.0, 0.25 * psi, 0.6 * psi, 0.999 * psi, 1.5 * psi, -0.5 * Fstar_l, -0.999 * Fstar_l]
        Fmax = max(ray.F(ray.l_hi), ray.F(ray.l_lo))
        if 1.3 * Fstar_l < ray.F(ray.l_hi):
            es.append(-1.3 * Fstar_l)
        mirror = Ray(1 - m, k)
        for e in es[:3]:
            eMir = max(eMir, abs(ray.V_brute(e, u, side=-1) - mirror.V_game(e, u)))
        for e in es:
            vb = ray.V_brute(e, u)
            vg = ray.V_game(e, u)
            if e >= 0:
                vc = ray.V_closed(e, u)
                d = abs(vb - vc)
                if d > eV:
                    eV, worst = d, (m, k, u, e, vb, vc)
            else:
                n_neg += 1
            eVg = max(eVg, abs(vb - vg))
        for X in [0.0, 1e-6, 0.1 * psi, 0.5 * psi, 0.95 * psi, 1.2 * psi]:
            nb = ray.N_brute(X, u)
            nc = ray.N_closed(X, u)
            ng = ray.N_game(X, u)
            eN = max(eN, abs(nb - nc))
            if X > 0:
                eNg = max(eNg, abs(nc - ng))
    report("11.90(b)", eV < 5e-9 and eVg < 5e-8 and eN < 5e-6 and eNg < 5e-6 and eMir < 5e-9,
           f"{len(cases)} centres (m,kappa,u): |V_brute - V_closed| <= {eV:.2e} (e>=0); |V_brute - V_game| <= {eVg:.2e} "
           f"(incl. {n_neg} negative accuracies); |N_brute - N_closed| <= {eN:.2e}; |N_closed - N_game| <= {eNg:.2e} (X>0); "
           f"negative half of the ray = shells of the antipodal centre 1-m: |V_brute(l<=0) - V_(1-m,kappa)| <= {eMir:.2e}")
    if worst and eV > 1e-9:
        print("      worst V case:", worst)


def test_domination(seed=5):
    """Theorem 11.90(c) on a grid, the equality case, and curvature domination"""
    ms = np.concatenate([np.linspace(0.02, 0.98, 49), [0.499, 0.501, 0.5]])
    ks = np.concatenate([np.linspace(0.02, 0.98, 49), [0.499, 0.501, 0.5]])
    ts = np.linspace(0.02, 0.98, 25)
    min_gap = math.inf
    arg = None
    n = 0
    for u in (0.25, 1.0, 3.0, 8.0):
        for m in ms:
            for k in ks:
                ray = Ray(float(m), float(k))
                psi_u = ray.Psi(u)
                for t in ts:
                    gap = Fstar_c(t, u) - (t * psi_u - ray.Psi(t * u))
                    n += 1
                    if not (abs(m - 0.5) < 1e-12 and abs(k - 0.5) < 1e-12):
                        if gap < min_gap:
                            min_gap, arg = gap, (u, float(m), float(k), float(t))
                    else:
                        assert abs(gap) < 1e-13, gap
    report("11.90(c) grid", min_gap > 0,
           f"{n} points (u in .25,1,3,8; m,kappa on a 52x52 grid incl. 0.499/0.501; t in (0,1)): "
           f"min over (m,kappa)!=(1/2,1/2) of F*_c - F*_(m,kappa) = {min_gap:.3e} at (u,m,kappa,t)={arg} (>0); "
           f"= 0 to 1e-13 at m=kappa=1/2")
    # near the equality case: gap / (dm^2 + dk^2) should stay bounded away from 0 (quadratic, positive definite)
    print("      near equality (u=1, t=0.5): gap/(dm^2+dk^2) along directions")
    u, t = 1.0, 0.5
    rows = []
    for ang in np.linspace(0, math.pi, 9)[:-1]:
        vals = []
        for r in (1e-2, 1e-3, 1e-4):
            m, k = 0.5 + r * math.cos(ang), 0.5 + r * math.sin(ang)
            ray = Ray(m, k)
            gap = Fstar_c(t, u) - ray.Fstar(t, u)
            vals.append(gap / r ** 2)
        rows.append((ang, vals))
        print(f"        direction {ang:5.3f} rad: " + ", ".join(f"{v:.6f}" for v in vals))
    pos = all(v[-1] > 1e-4 for _, v in rows)
    report("11.90(c) equality case", pos, "gap is quadratic and positive in every direction around m=kappa=1/2 "
                                           "(ratios above converge to positive constants)")
    # curvature domination (referee's strengthening): Psi''(s) = 4 / sum(1/T) <= (1/4) sech^2(s/2)
    rng = np.random.default_rng(seed)
    worst = -math.inf
    err_id = 0.0
    for _ in range(4000):
        m, k, s = rng.uniform(0.02, 0.98), rng.uniform(0.02, 0.98), rng.uniform(0.01, 8)
        ray = Ray(m, k)
        l = ray.l_of_s(s)
        a, b = ray.ab(l)
        T = np.array([m * a, m * (1 - a), (1 - m) * b, (1 - m) * (1 - b)])
        curv = 4.0 / np.sum(1.0 / T)
        ref = 0.25 / math.cosh(s / 2) ** 2
        worst = max(worst, curv - ref)
        # identity check Psi'' = dl/ds by central differences
        h = 1e-4 * max(1.0, s)
        if s > 2 * h:
            fd = (ray.l_of_s(s + h) - ray.l_of_s(s - h)) / (2 * h)
            err_id = max(err_id, abs(fd - curv) / ref)
    report("curvature domination", worst <= 1e-15 and err_id < 1e-5,
           f"4000 random (m,kappa,s): max[Psi''_(m,kappa)(s) - Psi_c''(s)] = {worst:.3e} (<= 0); "
           f"identity Psi'' = dl/ds = 4/sum(1/T) to rel. {err_id:.1e}")


def best_centre(kappa, u, e, what="V", X=None):
    """sup over centre types m (dense grid, then golden section)"""
    f = (lambda m: Ray(m, kappa).V_closed(e, u)) if what == "V" else (lambda m: Ray(m, kappa).N_closed(X, u))
    ms = np.linspace(0.005, 0.995, 397)
    vals = [f(float(m)) for m in ms]
    i = int(np.argmax(vals))
    r = minimize_scalar(lambda m: -f(m), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]), method="bounded",
                        options={"xatol": 1e-12})
    return (-r.fun, r.x) if -r.fun >= vals[i] else (vals[i], float(ms[i]))


def test_table():
    """the table of numbers of Theorem 11.90 (u = 1, e = 0) and the same for u = 2"""
    claimed = {0.5: (0.029139, 0.500, 0.110944), 0.45: (0.028856, 0.477, 0.109898), 0.4: (0.028005, 0.454, 0.106755),
               0.3: (0.024588, 0.408, 0.094080), 0.2: (0.018842, 0.362, 0.072574), 0.1: (0.010688, 0.316, 0.041588)}
    ok = True
    for u in (1.0, 2.0):
        print(f"      u = {u}:  kappa   R^kappa(0)   best m    N^kappa(0+)  best m(N)   R_unif(0)={R_unif(0, u):.6f} "
              f"theta_na^cube(0+)={theta_na_cube(0.0, u):.6f}")
        for kappa in (0.5, 0.45, 0.4, 0.3, 0.2, 0.1):
            R, mR = best_centre(kappa, u, 0.0, "V")
            N, mN = best_centre(kappa, u, None, "N", X=0.0)
            line = f"               {kappa:5.2f}   {R:.6f}   {mR:.3f}    {N:.6f}   {mN:.3f}"
            if u == 1.0:
                c = claimed[kappa]
                good = abs(R - c[0]) < 6e-7 and abs(mR - c[1]) < 6e-4 and abs(N - c[2]) < 6e-7
                ok &= good
                line += f"    claimed {c[0]:.6f} {c[1]:.3f} {c[2]:.6f}  {'ok' if good else 'MISMATCH'}"
            ok &= (R <= R_unif(0, u) + 1e-12) and (N <= theta_na_cube(0.0, u) + 1e-12)
            # "the best centre of an off-centre slice does not lie in the slice: its type is between kappa and 1/2"
            if kappa < 0.5:
                ok &= (kappa < mR < 0.5)
            print(line)
    report("table", ok, "all six rows of the u=1 table reproduced to the digits printed; best centre type strictly "
                        "between kappa and 1/2 for kappa<1/2; all values <= the cube's")


def test_sup_m_domination():
    """R^kappa(e) <= R_unif(e), N^kappa(X) <= theta_na^cube(X) on a grid, strictness for kappa != 1/2"""
    worstR = worstN = -math.inf
    min_strict = math.inf
    for u in (0.5, 1.0, 2.0):
        for kappa in (0.05, 0.2, 0.35, 0.45, 0.49, 0.5, 0.55, 0.8):
            for frac in (0.0, 0.2, 0.5, 0.8, 0.95):
                e = frac * Psi_c(u)
                R, _ = best_centre(kappa, u, e, "V")
                gapR = R_unif(e, u) - R
                X = frac * kl(0.5, 1 / (1 + math.exp(-u)))   # theta_na^cube > 0 for X < KL(1/2 || p_u)
                N, _ = best_centre(kappa, u, None, "N", X=X)
                gapN = theta_na_cube(X, u) - N
                worstR, worstN = max(worstR, -gapR), max(worstN, -gapN)
                if kappa != 0.5:
                    min_strict = min(min_strict, gapR, gapN)
                else:
                    assert abs(gapR) < 1e-9 and abs(gapN) < 1e-9, (u, e, gapR, gapN)
    report("sup_m domination", worstR <= 1e-12 and worstN <= 1e-12 and min_strict > 0,
           f"max(R^kappa - R_unif) = {worstR:.2e}, max(N^kappa - theta_na^cube) = {worstN:.2e}; equality at kappa=1/2 "
           f"to 1e-9; smallest strict gap for kappa != 1/2 on the grid: {min_strict:.3e}")


if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in (("defs", test_definitions), ("closed", test_closed_forms), ("dom", test_domination),
                     ("table", test_table), ("supm", test_sup_m_domination)):
        if not only or name in only:
            fn()
    print()
    print("SUMMARY:", "ALL PASS" if all(results.values()) else "FAILURES: " + ", ".join(k for k, v in results.items() if not v))
