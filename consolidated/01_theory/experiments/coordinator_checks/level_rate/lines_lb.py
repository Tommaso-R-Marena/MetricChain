"""Lower bounds of the level recursion from minorant lines (Lemma L of docs/workstreams/R_brief.md, section 2.2).

A tangent line (B, s0) of theta_na is a minorant of T_1 = theta_na (convex).  By Lemma L, with the slope map
    Sigma_B(s) = sup_{e>0} [B - (1 - s) theta_na(e)]/e          (finite iff B < (1 - s) a),
T_{j+1}(x) >= B - s_j x  with  s_j = Sigma_B(s_{j-1}),  as long as the slopes are finite.  Hence
    tau_k >= B   whenever   s_0, ..., s_{k-2} < 1 - B/a,
and tau_k^LB := sup of such B (the set is an interval: the map and s_0 increase with B).
Gaussian pair: Sigma_B(s) = B (1 - s)/(1 - s - B) (a Moebius map), s_0 = B/(1 - B).
Cube: tangent line at rho: s0 = lam/(u - lam), lam = ln((1-rho)/rho), B = kappa(rho) + s0 e(rho); Sigma by maximisation.

Output: k, tau_k^LB, k^2 (tau_k^LB - h), its ratio to 2 pi^2 h^2 theta_hint''(0), and tau_k of the interpolating grid
recursion (iterate_exact.py; an approximation, not a bound) where stored.
Usage: python3 lines_lb.py > out_lines_lb.txt
"""
import math, os, re
import numpy as np
from pairs import Gauss, Cube, kl

HERE = os.path.dirname(os.path.abspath(__file__))
KS = list(range(2, 13)) + [15, 20, 30, 40, 55, 80, 100, 120, 160, 240, 320]


def grid_values(fname):
    out = {}
    p = os.path.join(HERE, fname)
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r"^(\d+) (\d\.\d+) ", line)
            if m:
                out[int(m.group(1))] = float(m.group(2))
    return out


class GaussLines:
    def __init__(self):
        self.P = Gauss()

    def s0(self, B):
        return B / (1 - B)

    def sigma(self, B, s):
        return B * (1 - s) / (1 - s - B)


class CubeLines:
    def __init__(self, u):
        self.P = Cube(u)
        self.u = u
        P = self.P
        # rho-grid on (p_u, 1/2]: e(rho) = KL(rho||p_u), kappa(rho) = KL(rho||1/2)
        t = np.linspace(1e-3, 1.0, 200001)                 # rho - p_u >= 2e-7: KL(rho||p_u) is computed stably
        self.rho = P.pu + (0.5 - P.pu) * t ** 2            # dense near p_u
        self.kap = kl(self.rho, 0.5)
        self.e = kl(self.rho, P.pu)

    def s0(self, B):
        """slope of the tangent line of theta_na with intercept B (bisection on the tangency point)."""
        P = self.P
        lo, hi = P.pu, 0.5
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            lam = math.log((1 - mid) / mid)
            s = lam / (self.u - lam)
            Bm = float(kl(mid, 0.5)) + s * float(kl(mid, P.pu))
            if Bm > B:                                      # intercept decreases with rho
                lo = mid
            else:
                hi = mid
        lam = math.log((1 - lo) / lo)
        return lam / (self.u - lam)

    def sigma(self, B, s):
        r = (B - (1 - s) * self.kap) / self.e
        j = int(np.argmax(r))
        best = float(r[j])
        if 0 < j < len(r) - 1:                              # golden-section refinement in rho
            a_, b_ = float(self.rho[j - 1]), float(self.rho[j + 1])
            f = lambda x: (B - (1 - s) * float(kl(x, 0.5))) / float(kl(x, self.P.pu))
            gr = (math.sqrt(5) - 1) / 2
            c, d = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
            fc, fd = f(c), f(d)
            for _ in range(60):
                if fc > fd:
                    b_, d, fd = d, c, fc
                    c = b_ - gr * (b_ - a_)
                    fc = f(c)
                else:
                    a_, c, fc = c, d, fd
                    d = a_ + gr * (b_ - a_)
                    fd = f(d)
            best = max(best, fc, fd)
        return best


def survives(L, B, k):
    a = L.P.a
    s = L.s0(B)
    for _ in range(k - 1):                                   # s_0 .. s_{k-2} must be regular
        if not (s < 1 - B / a):
            return False
        s = L.sigma(B, s)
    return True


def tau_lb(L, k):
    h, a = L.P.h, L.P.a
    lo, hi = h, a
    if not survives(L, h * (1 + 1e-13), k):
        return float("nan")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if survives(L, mid, k):
            lo = mid
        else:
            hi = mid
    return lo


for L, gridfile in [(GaussLines(), "out_iterate_gauss_160.txt"), (CubeLines(1.0), "out_iterate_cube1_120.txt"),
                    (CubeLines(0.5), None), (CubeLines(2.0), None)]:
    P = L.P
    C = 2 * math.pi ** 2 * P.h ** 2 * P.hint2
    gv = grid_values(gridfile) if gridfile else {}
    print("# %s:  a = %.8f  h = %.8f  L_h = %.6f  theta_hint''(0) = %.6f   2 pi^2 h^2 theta_hint''(0) = %.8f = %.5f a" %
          (P.name, P.a, P.h, P.Lh, P.hint2, C, C / P.a))
    print("#   k   tau_k^LB       k^2(tau^LB - h)   ratio    tau_k (grid recursion)   k^2(tau - h)/const")
    ks = KS if isinstance(L, GaussLines) else [k for k in KS if k <= 120]
    for k in ks:
        t = tau_lb(L, k)
        g = gv.get(k)
        print("  %4d  %.10f   %.6f        %.5f   %s" % (k, t, k * k * (t - P.h), k * k * (t - P.h) / C,
              ("%.10f              %.5f" % (g, k * k * (g - P.h) / C)) if g else "      -"), flush=True)
    print()
