"""Referee A -- own definitions (independent of rlib.py): the non-adaptive exponent functions theta themselves
(not their dual J), the slope map Sigma by direct maximisation over e, upper envelopes of lines, and a brute-force
evaluation of the level operator

    R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma >= beta} [ min(gamma, phi theta((g-beta)/phi)) + (1-phi) T(gamma/(1-phi)) ].

Floating point; nothing certified.
"""
import math
import numpy as np


# ----------------------------------------------------------------------------------------------------------------
# theta families.  Each has: a = theta(0+), f(e) vectorised on e > 0, name, and (optionally) the exact list of
# vertices for piecewise-linear theta.
# ----------------------------------------------------------------------------------------------------------------
class Theta:
    name = "abstract"
    a = None
    vertices = None          # for piecewise-linear theta: sorted abscissae of the kinks
    emax = 1e4               # sup over e is searched on (0, emax]

    def f(self, e):
        raise NotImplementedError

    def __call__(self, e):
        return self.f(np.asarray(e, dtype=float))

    # fixed point theta(h) = h by bisection (theta nonincreasing, continuous)
    def fixed_point(self):
        lo, hi = 0.0, self.a
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if float(self.f(np.array(mid))) > mid:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    # --- slope map by brute force: sup_{e>0} [B - (1-s) theta(e)]/e ------------------------------------------
    _egrid = None

    def egrid(self):
        if self._egrid is None:
            self._egrid = np.exp(np.linspace(math.log(1e-12), math.log(self.emax), 6001))
        return self._egrid

    def sigma(self, B, s, refine=True):
        """Sigma(B, s) in [0, inf].  inf iff the ratio is unbounded as e -> 0 (B > (1-s) a)."""
        B = float(B); s = float(s)
        if B < 0:
            raise ValueError
        if B > (1.0 - s) * self.a * (1 + 1e-15) + 1e-300:
            return math.inf
        if B == 0.0:
            return 0.0
        y = 1.0 - s
        if self.vertices is not None:
            # piecewise-linear theta: N(e)/e is monotone between kinks except possibly ... (N concave pw-linear:
            # N/e on a linear piece  (c0 + c1 e)/e  is monotone) -> sup at a kink, or e -> 0+, or e -> infinity (0)
            v = np.asarray(self.vertices, dtype=float)
            vals = (B - y * self.f(v)) / v
            best = max(0.0, float(vals.max()))
            # e -> 0+: N(0+) = B - y a <= 0 here; if = 0 the limit is y * |theta'(0+)|
            if abs(B - y * self.a) <= 1e-15 * max(1.0, self.a):
                e0 = 1e-9 * v[0]
                best = max(best, float((B - y * self.f(np.array(e0))) / e0))
            return best
        e = self.egrid()
        r = (B - y * self.f(e)) / e
        i = int(np.argmax(r))
        best = float(r[i])
        if refine and 0 < i < len(e) - 1:
            lo, hi = e[i - 1], e[i + 1]
            gr = (math.sqrt(5) - 1) / 2
            fun = lambda x: (B - y * float(self.f(np.array(x)))) / x
            x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
            f1, f2 = fun(x1), fun(x2)
            for _ in range(60):
                if f1 >= f2:
                    hi, x2, f2 = x2, x1, f1
                    x1 = hi - gr * (hi - lo)
                    f1 = fun(x1)
                else:
                    lo, x1, f1 = x1, x2, f2
                    x2 = lo + gr * (hi - lo)
                    f2 = fun(x2)
            best = max(best, f1, f2)
        return max(best, 0.0)

    def argmax_sigma(self, B, s):
        """a maximiser e of [B - (1-s) theta(e)]/e (grid + golden section); None if sup is 0 or infinite."""
        y = 1.0 - s
        e = self.egrid()
        r = (B - y * self.f(e)) / e
        i = int(np.argmax(r))
        if i == 0 or i == len(e) - 1:
            return float(e[i])
        lo, hi = e[i - 1], e[i + 1]
        gr = (math.sqrt(5) - 1) / 2
        fun = lambda x: (B - y * float(self.f(np.array(x)))) / x
        x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = fun(x1), fun(x2)
        for _ in range(80):
            if f1 >= f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - gr * (hi - lo)
                f1 = fun(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + gr * (hi - lo)
                f2 = fun(x2)
        return 0.5 * (lo + hi)


class Gauss(Theta):
    name = "Gaussian (1 - sqrt e)^2"
    a = 1.0
    emax = 1e3

    def f(self, e):
        return np.where(e < 1.0, (1.0 - np.sqrt(np.minimum(e, 1.0))) ** 2, 0.0)


class Cube(Theta):
    """theta(e) = KL(rho || 1/2) at the rho in [p_u, 1/2] with KL(rho || p_u) = e; 0 for e >= KL(1/2 || p_u)."""
    emax = 1e3

    def __init__(self, u, ntab=200001):
        self.u = u
        self.name = "cube u=%g" % u
        pu = 1.0 / (1.0 + math.exp(u))
        self.pu = pu
        rho = np.linspace(pu, 0.5, ntab)
        with np.errstate(divide="ignore", invalid="ignore"):
            kl_pu = rho * np.log(rho / pu) + (1 - rho) * np.log((1 - rho) / (1 - pu))
            kl_half = rho * np.log(2 * rho) + (1 - rho) * np.log(2 * (1 - rho))
        kl_pu[0] = 0.0
        self.tab_e = kl_pu            # increasing in rho
        self.tab_t = kl_half          # decreasing in rho
        self.a = float(kl_half[0])
        self.estar = float(kl_pu[-1])

    def f(self, e):
        e = np.asarray(e, dtype=float)
        # invert e = KL(rho||pu) by Newton from the table (table interpolation then 3 Newton steps)
        pu = self.pu
        rho = np.interp(np.minimum(e, self.estar), self.tab_e, np.linspace(pu, 0.5, len(self.tab_e)))
        rho = np.clip(rho, pu + 1e-15, 0.5)
        for _ in range(4):
            val = rho * np.log(rho / pu) + (1 - rho) * np.log((1 - rho) / (1 - pu)) - np.minimum(e, self.estar)
            der = np.log(rho / pu) - np.log((1 - rho) / (1 - pu))
            step = np.where(der > 1e-12, val / np.maximum(der, 1e-12), 0.0)
            rho = np.clip(rho - step, pu + 1e-15, 0.5)
        out = rho * np.log(2 * rho) + (1 - rho) * np.log(2 * (1 - rho))
        return np.where(e >= self.estar, 0.0, out)


class Expo(Theta):
    """theta(e) = d + (a - d) exp(-e/c): strictly convex, finite slope at zero, theta(inf) = d >= 0."""

    def __init__(self, a=1.0, c=0.3, d=0.0):
        self.a, self.c, self.d = a, c, d
        self.name = "expo a=%g c=%g d=%g" % (a, c, d)
        self.emax = 1e4 * c

    def f(self, e):
        return self.d + (self.a - self.d) * np.exp(-e / self.c)


class Power(Theta):
    """theta(e) = a (1 - (e/c)^q)_+^r, q in (0, 1], r >= 1 : convex nonincreasing (q = 1/2, r = 2, c = a = 1: Gaussian);
    q < 1: infinite slope at zero; q = 1: finite slope -a r/c."""

    def __init__(self, a=1.0, c=1.0, q=0.5, r=2.0):
        self.a, self.c, self.q, self.r = a, c, q, r
        self.name = "power a=%g c=%g q=%g r=%g" % (a, c, q, r)
        self.emax = 1e3 * c

    def f(self, e):
        z = np.minimum(e / self.c, 1.0)
        return self.a * (1.0 - z ** self.q) ** self.r


class Recip(Theta):
    """theta(e) = a/(1 + e/c)^r : strictly convex, finite slope at zero, positive everywhere (theta(inf) = 0, never reached)."""

    def __init__(self, a=1.0, c=0.5, r=2.0):
        self.a, self.c, self.r = a, c, r
        self.name = "recip a=%g c=%g r=%g" % (a, c, r)
        self.emax = 1e6 * c

    def f(self, e):
        return self.a / (1.0 + e / self.c) ** self.r


class PwLin(Theta):
    """theta(e) = max_i (alpha_i - beta_i e, floor): convex piecewise linear, nonincreasing (beta_i >= 0), floor >= 0."""

    def __init__(self, lines, floor=0.0, name=None):
        self.lines = [(float(al), float(be)) for al, be in lines]
        self.floor = float(floor)
        self.a = max(max(al for al, _ in self.lines), self.floor)
        self.name = name or ("pwlin %s floor %g" % (self.lines, floor))
        # kinks: pairwise intersections (and with the floor) that lie on the upper envelope
        cand = []
        L = self.lines + [(self.floor, 0.0)]
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                (a1, b1), (a2, b2) = L[i], L[j]
                if b1 != b2:
                    x = (a1 - a2) / (b1 - b2)
                    if x > 0:
                        val = max(al - be * x for al, be in L)
                        if abs(val - (a1 - b1 * x)) < 1e-12 * max(1, abs(val)):
                            cand.append(x)
        self.vertices = sorted(set(cand))
        self.emax = 1e3 * max(self.vertices)

    def f(self, e):
        out = np.full(np.shape(e), self.floor, dtype=float)
        for al, be in self.lines:
            out = np.maximum(out, al - be * e)
        return out


# ----------------------------------------------------------------------------------------------------------------
# upper envelope of lines  B_i - w_i x  (x > 0)
# ----------------------------------------------------------------------------------------------------------------
class Envelope:
    """M(x) = max_i (B_i - w_i x), evaluated exactly (vectorised max over the lines in chunks)."""

    def __init__(self, B, w):
        self.B = np.asarray(B, dtype=float)
        self.w = np.asarray(w, dtype=float)
        # keep only lines on the upper hull (speeds up evaluation): sort by slope, standard hull trick
        order = np.lexsort((-self.B, self.w))           # by w ascending, then B descending
        Bs, ws = self.B[order], self.w[order]
        keepB, keepw = [], []
        for b, w_ in zip(Bs, ws):
            if keepw and w_ == keepw[-1]:
                continue                                 # same slope, smaller intercept
            # lines sorted by increasing w (flatter first: dominate for large x).  New line has larger w: it can
            # only be on top for small x, so it needs a larger intercept than the last kept line.
            if keepB and b <= keepB[-1]:
                continue
            while len(keepB) >= 2:
                # intersection of new with keep[-2] vs keep[-1] with keep[-2]
                x_new = (b - keepB[-2]) / (w_ - keepw[-2])
                x_old = (keepB[-1] - keepB[-2]) / (keepw[-1] - keepw[-2])
                if x_new >= x_old:
                    keepB.pop(); keepw.pop()
                else:
                    break
            keepB.append(b); keepw.append(w_)
        self.hB = np.array(keepB)
        self.hw = np.array(keepw)
        # breakpoints: line i is on top for x in [xb[i], xb[i-1]] (x decreasing with i)
        if len(self.hB) > 1:
            self.xb = (self.hB[1:] - self.hB[:-1]) / (self.hw[1:] - self.hw[:-1])   # decreasing sequence
        else:
            self.xb = np.array([])

    def __call__(self, x):
        x = np.asarray(x, dtype=float)
        if len(self.xb) == 0:
            return self.hB[0] - self.hw[0] * x
        # index of the top line: number of breakpoints >= x  (xb decreasing)
        idx = np.searchsorted(-self.xb, -x, side="right")
        return self.hB[idx] - self.hw[idx] * x

    def direct(self, x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        return np.max(self.B[None, :] - self.w[None, :] * x[:, None], axis=1)


# ----------------------------------------------------------------------------------------------------------------
# brute force on R itself
# ----------------------------------------------------------------------------------------------------------------
def bracket_sup_gamma(theta, T, g, phi, beta, ngam=400, Tsup_hint=None):
    """sup_{gamma >= beta} [min(gamma, mu) + (1-phi) T(gamma/(1-phi))], mu = phi theta((g-beta)/phi), by brute force on a
    gamma-grid: [beta, 3 max(mu, beta)] (linear + the special points beta, mu) and a geometric tail.  No shortcut.
    Returns (value, argmax gamma, mu)."""
    mu = phi * float(theta(np.array((g - beta) / phi)))
    top = max(mu, beta)
    gam = np.concatenate([
        np.linspace(beta, max(3 * top, beta * (1 + 1e-9)), ngam),
        np.array([beta, mu if mu >= beta else beta, top]),
        top * np.exp(np.linspace(0, math.log(1e6), 60)),
        beta + (top - beta) * (1 - np.exp(-np.linspace(0, 30, 60))),          # accumulate towards mu from below
    ])
    val = np.minimum(gam, mu) + (1 - phi) * T(gam / (1 - phi))
    i = int(np.argmax(val))
    return float(val[i]), float(gam[i]), mu


def R_bruteforce(theta, T, g, nphi=160, nbeta=24, ngam=240, refine=True, beta_fracs=None, return_arg=False, refine_iters=400):
    """Upper estimate of the infimum over (phi, beta) on a grid (phi on a logit grid, beta/g on a mixed grid), with the
    supremum over gamma by brute force; then a local refinement (coordinate golden-section) around the best points.
    Returns the best value (and its (phi, beta, gamma*, mu))."""
    z = np.linspace(-14, 14, nphi)
    phis = 1.0 / (1.0 + np.exp(-z))
    if beta_fracs is None:
        beta_fracs = np.concatenate([10.0 ** np.linspace(-10, -1, nbeta // 2), np.linspace(0.15, 0.999, nbeta - nbeta // 2)])
    best = (math.inf, None)
    table = []
    for phi in phis:
        if phi >= 1.0 or phi <= 0.0:
            continue
        for bf in beta_fracs:
            beta = bf * g
            v, gam, mu = bracket_sup_gamma(theta, T, g, phi, beta, ngam)
            table.append((v, phi, beta))
            if v < best[0]:
                best = (v, (phi, beta, gam, mu))
    if refine:
        table.sort()
        for v0, phi0, beta0 in table[:6]:
            zc, lb = math.log(phi0 / (1 - phi0)), math.log(beta0 / g)
            dz, dl = (z[1] - z[0]), 1.0
            cur = v0
            for it in range(refine_iters):
                improved = False
                for (ddz, ddl) in [(dz, 0), (-dz, 0), (0, dl), (0, -dl)]:
                    z2, l2 = zc + ddz, min(lb + ddl, math.log(0.9999))
                    phi2, beta2 = 1.0 / (1.0 + math.exp(-z2)), math.exp(l2) * g
                    if not (0 < phi2 < 1) or beta2 <= 0:
                        continue
                    v, gam, mu = bracket_sup_gamma(theta, T, g, phi2, beta2, ngam)
                    if v < cur - 1e-15:
                        cur, zc, lb, improved = v, z2, l2, True
                        if v < best[0]:
                            best = (v, (phi2, beta2, gam, mu))
                if not improved:
                    dz *= 0.5; dl *= 0.5
                    if dz < 1e-10:
                        break
    return (best if return_arg else best[0])
