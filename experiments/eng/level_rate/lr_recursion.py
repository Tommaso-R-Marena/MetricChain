"""The level recursion itself (method (a)), two ways.

    T_1 = theta,   T_{k+1} = min(T_k, R[T_k]),   tau_k = sup T_k = T_k(0+),
    R[T](g) = inf_{0<phi<1, 0<beta<g}  sup_{gamma >= beta} [ min(gamma, mu) + (1 - phi) T(gamma/(1 - phi)) ],
    mu = phi * theta((g - beta)/phi)                                            (THEORY_REPORT (11.18.2)).

Elementary reductions used by both implementations (c = 1 - phi, x_lo = beta/c, x_hi = mu/c,
S(x) = x + T(x); T nonincreasing):

    sup_{gamma >= beta} [...] = c * sup{ S(x) : x_lo <= x <= x_hi }        if x_lo <= x_hi   ("regime 1")
                              = mu + c * T(x_lo)                           if x_lo >  x_hi   ("regime 2")

(for gamma >= mu the bracket mu + c T(gamma/c) is nonincreasing in gamma), and at accuracy zero

    tau_{k+1} = min(tau_k, inf_phi c * sup{ S(x) : 0 < x <= phi a/c })

(the bracket at any (phi, beta, g) is at most the value with mu replaced by phi*a and beta by 0: "<=", which is
all the upper bound needs; ">=" by continuity of theta at 0).

(a1) ``GeneralRecursion`` -- no structural assumption: T_k on a grid, linear interpolation in sqrt(x), the
     supremum over gamma exactly for the interpolant (range maximum over nodes), the infimum over (phi, beta) by
     a dense two-dimensional scan in logit variables followed by nested golden-section refinement, and by a
     second search along the balance curve (see ``GeneralRecursion.apply``).  A plain numerical
     approximation: neither an upper nor a lower bound.  Its interpolation error is of second order in the
     grid and negative (T_k is concave in sqrt(x) on most of the range): about -2e-6 a at N = 1000 after 40
     levels, a quarter of that at N = 2000 -- enough to fall below the proved lower bound where the sandwich
     is tight.  It is a check of structure (convexity, quasi-convexity of S, no "regime 2"), not of digits.

(a2) ``ConvexUpperBound`` -- a rigorous upper bound (up to floating-point rounding; see ``fp_margin``).
     Claim (proved in the report text of this check, not by the theory division): let M be convex and
     nonincreasing with M >= T_k, S_M(x) = x + M(x), x_m a minimiser of S_M, S~(x) = S_M(max(x, x_m)), and

         H1(phi, beta; g) = max( beta + c M(beta/c),  c S~(mu/c) ).

     Then (i) H <= H1 pointwise (in regime 1 they agree because S_M is convex; in regime 2, H = mu + c M(x_lo)
     < beta + c M(x_lo)); (ii) H1 is jointly convex in (phi, beta, g) -- perspectives of the convex functions M,
     S~ and theta, S~ nondecreasing; hence R1[M](g) := inf_{phi, beta} H1 is convex in g and
     T_{k+1} <= R[T_k] <= R[M] <= R1[M].  (iii) A convex function lies below the chords of its graph, so the
     lower convex hull of points (g_i, v_i) with v_i >= R1[M](g_i) -- v_i = H1 at ANY feasible (phi, beta) -- is
     a convex majorant of T_{k+1}.  Every approximation is on the safe side: restricted infimum, chords of M,
     chords of theta.
     Moreover, if T_k is convex and T_k <= theta then regime 2 never helps: there
     H = phi theta(x1) + c T_k(x2) >= T_k(phi x1 + c x2) = T_k(g).  So T_{k+1} = min(T_k, R1[T_k]) exactly, and
     the scheme converges to the recursion itself as the grid is refined (as long as R1[T_k] <= T_k, which is
     monitored: ``n_above``).

Grids: x = G(xi), xi uniform on [0, 1], G(xi) = E (1 + eps0) xi^4/(xi^2 + eps0): like xi^4 near 0 (all T_k
have a square-root singularity at 0), like xi^2 at the top.  G has a closed-form inverse, which gives the cell
of a point without a search.
"""
from __future__ import annotations

import math
import time

import numpy as np

GR = (math.sqrt(5) - 1) / 2


# ----------------------------------------------------------------------------------------------------------------
# graded grids and piecewise-linear functions on them
# ----------------------------------------------------------------------------------------------------------------
def make_grid(N: int, E: float, eps0: float = 0.02):
    xi = np.arange(N + 1) / N
    x = E * (1 + eps0) * xi**4 / (xi**2 + eps0)
    x[0], x[-1] = 0.0, E
    return x


class Graded:
    """A function on [0, infinity) given by its values at the nodes of a graded grid: piecewise linear in x
    (``mode='x'``) or in sqrt(x) (``mode='s'``) on [0, E], and zero from E on."""

    def __init__(self, N: int, E: float, eps0: float = 0.02, mode: str = "x"):
        self.N, self.E, self.eps0, self.mode = N, float(E), eps0, mode
        self.x = make_grid(N, E, eps0)
        self.z = self.x if mode == "x" else np.sqrt(self.x)       # the variable of interpolation
        self.dz = np.diff(self.z)
        self.scale = 1.0 / (self.E * (1 + eps0))
        self.v = None

    def set(self, v):
        self.v = np.array(v, dtype=float)
        self.slope = np.diff(self.v) / self.dz

    def cell(self, y):
        """i with x[i] <= y < x[i+1] (clipped to 0..N-1), from the inverse of G plus one correction step."""
        xp = y * self.scale
        xi2 = 0.5 * (xp + np.sqrt(xp * xp + 4.0 * self.eps0 * xp))
        i = (np.sqrt(xi2) * self.N).astype(np.intp)
        np.clip(i, 0, self.N - 1, out=i)
        i -= self.x[i] > y
        np.clip(i, 0, self.N - 1, out=i)
        i += (self.x[i + 1] <= y) & (i < self.N - 1)
        return i

    def __call__(self, y):
        y = np.asarray(y, dtype=float)
        i = self.cell(y)
        zz = y if self.mode == "x" else np.sqrt(y)
        out = self.v[i] + (zz - self.z[i]) * self.slope[i]
        return np.where(y >= self.E, 0.0, out)


def build_theta(pair, n: int, eps0: float = 0.02) -> Graded:
    """Chords of theta_na through its exact values at the nodes of a graded grid: a majorant of theta_na
    (theta_na is convex), equal to it within about 1e-11 a for n = 1 000 000."""
    tab = Graded(n, pair.E, eps0, "x")
    v = np.asarray(pair.theta_na(tab.x), dtype=float)
    v[0], v[-1] = pair.a, 0.0
    tab.set(v)
    return tab


def lower_hull_values(x, v):
    """Values at the nodes x of the lower convex hull of the points (x_i, v_i) (x increasing).  The result is
    the piecewise-linear interpolant through a subset of the points that contains the first and the last."""
    n = len(x)
    idx = [0, 1]
    for i in range(2, n):
        while len(idx) >= 2:
            i0, i1 = idx[-2], idx[-1]
            if (v[i1] - v[i0]) * (x[i] - x[i0]) >= (v[i] - v[i0]) * (x[i1] - x[i0]):
                idx.pop()
            else:
                break
        idx.append(i)
    idx = np.array(idx)
    return np.interp(x, x[idx], v[idx]), idx


def _expit(p):
    return 1.0 / (1.0 + np.exp(-p))


def golden_min(f, lo, hi, nscan: int, niter: int):
    """Vectorised minimisation of f over [lo, hi] (arrays): a scan of ``nscan`` points, then golden section on
    the two cells next to the best scan point.  Exact (in the limit) for unimodal f.  Returns (argmin, min);
    the minimum returned is the smallest value of f seen, hence always a value of f at a point of [lo, hi]."""
    shape = np.broadcast(lo, hi).shape
    ts = np.linspace(0.0, 1.0, nscan)
    best = np.full(shape, np.inf)
    xbest = np.zeros(shape)
    kb = np.zeros(shape, dtype=int)
    for k, t in enumerate(ts):
        xk = lo + (hi - lo) * t
        fv = f(xk)
        m = fv < best
        best = np.where(m, fv, best)
        xbest = np.where(m, xk, xbest)
        kb = np.where(m, k, kb)
    A = lo + (hi - lo) * ts[np.maximum(kb - 1, 0)]
    B = lo + (hi - lo) * ts[np.minimum(kb + 1, nscan - 1)]
    return _golden(f, A, B, niter, xbest, best)


def golden_min_grid(f, grid, niter: int):
    """The same with a given (possibly non-uniform) scan grid common to all components."""
    best = kb = xbest = None
    for k, q in enumerate(grid):
        fv = f(q)
        if best is None:
            best = np.array(fv, dtype=float, copy=True)
            kb = np.zeros(best.shape, dtype=int)
            xbest = np.full(best.shape, q)
        else:
            m = fv < best
            best = np.where(m, fv, best)
            kb = np.where(m, k, kb)
            xbest = np.where(m, q, xbest)
    A = grid[np.maximum(kb - 1, 0)]
    B = grid[np.minimum(kb + 1, len(grid) - 1)]
    return _golden(f, A, B, niter, xbest, best)


def _golden(f, A, B, niter, xbest, best):
    x1 = B - GR * (B - A)
    x2 = A + GR * (B - A)
    f1 = f(x1)
    f2 = f(x2)
    for _ in range(niter):
        m = f1 <= f2                               # keep [A, x2]
        B = np.where(m, x2, B)
        A = np.where(m, A, x1)
        xe = np.where(m, B - GR * (B - A), A + GR * (B - A))      # the one new point
        fe = f(xe)
        x1, x2, f1, f2 = (np.where(m, xe, x2), np.where(m, x1, xe), np.where(m, fe, f2), np.where(m, f1, fe))
    for xc, fc in ((x1, f1), (x2, f2)):
        m = fc < best
        best = np.where(m, fc, best)
        xbest = np.where(m, xc, xbest)
    return xbest, best


def balance_min(t12, phi, c, g, xm, n_illinois: int, tol_f: float):
    """min over beta in [0, min(g, c x_m)] of max(t1, t2)(beta), where (t1, t2) = t12(phi, c, beta, g),
    t1 is nonincreasing on that interval and t2 is nondecreasing: the minimum is at beta = 0, at the right end,
    or where t1 = t2 in between (Illinois' method in sqrt(beta), with an occasional bisection step).
    Returns (value, beta); the value is max(t1, t2) at the beta returned, whatever the root finder does."""
    bhi = np.minimum(g, c * xm)
    zero = np.zeros(g.shape)
    a1, a2 = t12(phi, c, zero, g)
    b1, b2 = t12(phi, c, bhi, g)
    va, vb = np.maximum(a1, a2), np.maximum(b1, b2)
    best = np.minimum(va, vb)
    bbest = np.where(va <= vb, zero, bhi)
    fa, fb = a1 - a2, b1 - b2
    idx = np.nonzero((fa > 0) & (fb < 0))[0]         # a sign change: a crossing inside
    if idx.size == 0:
        return best, bbest
    phi, c, bhi, gg, fa, fb = phi[idx], c[idx], bhi[idx], g[idx], fa[idx], fb[idx]
    ra, rb = np.zeros(idx.size), np.ones(idx.size)
    side = np.zeros(idx.size, dtype=int)
    bst, bbt = best[idx], bbest[idx]
    for it in range(n_illinois):
        r = (ra * fb - rb * fa) / (fb - fa)
        if it % 5 == 4:
            r = 0.5 * (ra + rb)
        r = np.minimum(np.maximum(r, ra), rb)
        beta = bhi * r * r
        t1, t2 = t12(phi, c, beta, gg)
        v = np.maximum(t1, t2)
        m = v < bst
        bst = np.where(m, v, bst)
        bbt = np.where(m, beta, bbt)
        fr = t1 - t2
        pos = fr > 0
        # Illinois: halve the stale end value when the same end is replaced twice in a row
        fb = np.where(pos & (side == 1), 0.5 * fb, fb)
        fa = np.where(~pos & (side == -1), 0.5 * fa, fa)
        ra = np.where(pos, r, ra)
        fa = np.where(pos, fr, fa)
        rb = np.where(pos, rb, r)
        fb = np.where(pos, fb, fr)
        side = np.where(pos, 1, -1)
        live = (np.abs(fr) > tol_f) & (rb - ra > 1e-15)
        if not np.all(live):
            best[idx[~live]] = bst[~live]
            bbest[idx[~live]] = bbt[~live]
            if not np.any(live):
                idx = idx[:0]
                break
            idx, phi, c, bhi, gg = idx[live], phi[live], c[live], bhi[live], gg[live]
            ra, rb, fa, fb, side, bst, bbt = ra[live], rb[live], fa[live], fb[live], side[live], bst[live], bbt[live]
    if idx.size:
        best[idx] = bst
        bbest[idx] = bbt
    return best, bbest


# ----------------------------------------------------------------------------------------------------------------
# (a2) the convex upper bound
# ----------------------------------------------------------------------------------------------------------------
class ConvexUpperBound:
    """Convex piecewise-linear majorants M_k >= T_k on the grid; ``tau`` is an upper bound of tau_k."""

    def __init__(self, pair, N: int = 4000, eps0: float = 0.02, n_theta: int = 1_000_000, fp_margin: float = 1e-13,
                 P: float = 34.0, nscan: int = 21, niter: int = 44, n_illinois: int = 40, theta: Graded | None = None,
                 x_top: float | None = None):
        self.pair = pair
        self.a, self.E = float(pair.a), float(pair.E)
        self.theta_bar = theta if theta is not None else build_theta(pair, n_theta)
        # the grid of M ends at E (every T_k vanishes from E on); ``x_top`` > E is for other convex functions
        self.Mf = Graded(N, self.E if x_top is None else float(x_top), eps0, "x")
        self.x = self.Mf.x
        self.N = N
        M = np.asarray(self.theta_bar(self.x), dtype=float)   # chords of a majorant of theta: convex, >= theta
        M[0], M[-1] = self.a, 0.0
        M, _ = lower_hull_values(self.x, M)                    # convex to rounding
        self.Mf.set(M)
        self.k = 1
        self.fp_margin = fp_margin * self.a
        self.P, self.nscan, self.niter, self.n_illinois = P, nscan, niter, n_illinois
        self.history = [dict(k=1, tau=self.a, seconds=0.0)]

    @property
    def M(self):
        return self.Mf.v

    def _prep(self):
        S = self.x + self.Mf.v
        im = int(np.argmin(S))
        self.xm, self.Smin = float(self.x[im]), float(S[im])

    def _t12(self, phi, c, beta, g):
        """The two terms of H1 at (phi, beta; g)."""
        t1 = beta + c * self.Mf(beta / c)
        mu = phi * self.theta_bar((g - beta) / phi)
        xh = mu / c
        t2 = np.where(xh >= self.xm, mu + c * self.Mf(xh), c * self.Smin)
        return t1, t2

    def _inner(self, p, g):
        """min over beta in [0, g] of H1(phi, beta; g) at phi = expit(p) (see ``balance_min``)."""
        phi = _expit(p)
        c = _expit(-p)
        return balance_min(self._t12, phi, c, g, self.xm, self.n_illinois, 1e-15 * self.a)[0]

    def apply(self, g):
        """Upper bounds of R1[M](g) for an array g of accuracies in (0, E): the value of H1 at a feasible point
        found by scan + golden section in logit(phi) (the partial minimum over beta is convex in phi)."""
        g = np.asarray(g, dtype=float)
        self._prep()
        lo = np.full(g.shape, -self.P)
        hi = np.full(g.shape, self.P)
        pb, vb = golden_min(lambda p: self._inner(p, g), lo, hi, self.nscan, self.niter)
        return vb, pb

    def apply_zero(self):
        """Upper bound of R1[M](0+): inf_phi max(c M(0), c S~(phi a/c))."""
        self._prep()

        def f0(p):
            phi = _expit(p)
            c = _expit(-p)
            xh = phi * self.a / c
            t2 = np.where(xh >= self.xm, phi * self.a + c * self.Mf(xh), c * self.Smin)
            return np.maximum(c * self.Mf.v[0], t2)

        p0, v0 = golden_min(f0, np.array([-self.P]), np.array([self.P]), 2001, 70)
        return float(v0[0]), float(p0[0])

    def step(self):
        t0 = time.time()
        g = self.x[1:-1]
        vb, pb = self.apply(g)
        v0, p0 = self.apply_zero()
        raw = np.concatenate([[v0], vb, [0.0]])
        raw[:-1] += self.fp_margin
        above = raw[:-1] - self.Mf.v[:-1]
        n_above = int(np.sum(above > 2 * self.fp_margin))
        newM, idx = lower_hull_values(self.x, raw)
        self.raw, self.popt, self.p0 = raw, pb, p0
        self.Mf.set(newM)
        self.k += 1
        rec = dict(k=self.k, tau=float(newM[0]), n_above=n_above, max_above=float(above.max()),
                   n_hull=int(len(idx)), seconds=time.time() - t0)
        self.history.append(rec)
        return rec

    def run(self, K: int, verbose: bool = False):
        while self.k < K:
            rec = self.step()
            if verbose:
                print(rec, flush=True)
        return self.history

    def taus(self):
        return {r["k"]: r["tau"] for r in self.history}


# ----------------------------------------------------------------------------------------------------------------
# (a1) the recursion without structural assumptions
# ----------------------------------------------------------------------------------------------------------------
class GeneralRecursion:
    """T_k at the grid nodes, linear interpolation in sqrt(x); no convexity is assumed anywhere."""

    def __init__(self, pair, N: int = 1000, eps0: float = 0.02, n_theta: int = 1_000_000,
                 p_grid=None, q_grid=None, niter: int = 30, theta: Graded | None = None):
        self.pair = pair
        self.a, self.E = float(pair.a), float(pair.E)
        self.theta_f = theta if theta is not None else build_theta(pair, n_theta)
        self.Tf = Graded(N, self.E, eps0, "s")
        self.x = self.Tf.x
        self.N = N
        T = np.asarray(self.theta_f(self.x), dtype=float)
        T[0], T[-1] = self.a, 0.0
        self.Tf.set(T)
        self.k = 1
        self.p_grid = np.arange(-30.0, 30.01, 0.5) if p_grid is None else np.asarray(p_grid, dtype=float)
        qg = np.arange(-30.0, 10.01, 0.5) if q_grid is None else np.asarray(q_grid, dtype=float)
        self.q_grid = np.concatenate([[-45.0], qg, [45.0]])   # the ends stand for beta -> 0 and beta -> g
        self.niter = niter
        self.history = [dict(k=1, tau=self.a, seconds=0.0)]

    @property
    def T(self):
        return self.Tf.v

    def _prep(self):
        Sn = self.x + self.Tf.v
        L = len(Sn)
        tabs = [Sn]
        j = 1
        while (1 << j) <= L:
            prev, half = tabs[-1], 1 << (j - 1)
            m = L - (1 << j) + 1
            tabs.append(np.maximum(prev[:m], prev[half:half + m]))
            j += 1
        self.tab = np.full((len(tabs), L), -np.inf)
        for j, t in enumerate(tabs):
            self.tab[j, :len(t)] = t
        d = np.diff(Sn)
        sg = np.sign(np.where(np.abs(d) < 1e-14 * self.a, 0.0, d))
        sg = sg[sg != 0]
        self.S_quasiconvex = bool(np.all(np.diff(sg) >= 0))
        im = int(np.argmin(Sn))
        self.xm, self.Smin = float(self.x[im]), float(Sn[im])
        sl = np.diff(self.Tf.v) / np.diff(self.x)
        # largest decrease of the slope at a node times the smaller adjacent cell: > 0 means a concave corner
        self.max_concavity = float(np.max(-np.diff(sl) * np.minimum(np.diff(self.x)[1:], np.diff(self.x)[:-1])))

    def rmax(self, x1, x2):
        """max of S(x) = x + T(x) over [x1, x2] (x1 <= x2): between two nodes S is convex in sqrt(x), so the
        maximum is at an end point or at a node inside."""
        out = np.maximum(x1 + self.Tf(x1), x2 + self.Tf(x2))
        c1 = self.Tf.cell(x1)
        i1 = c1 + (self.x[c1] < x1)                 # first node >= x1
        i2 = self.Tf.cell(x2)                       # last node <= x2 (for x2 < E)
        i2 = np.where(x2 >= self.E, self.N, i2)
        ok = i2 >= i1
        i1c = np.where(ok, i1, 0)
        i2c = np.where(ok, i2, 0)
        j = np.frexp((i2c - i1c + 1).astype(float))[1] - 1
        m = np.maximum(self.tab[j, i1c], self.tab[j, i2c - (1 << j) + 1])
        return np.where(ok, np.maximum(out, m), out)

    def H_beta(self, phi, c, beta, g, want_regime: bool = False):
        """The supremum over gamma of the bracket of (11.18.2) at (phi, beta; g), for the interpolant."""
        mu = phi * self.theta_f((g - beta) / phi)
        xlo = beta / c
        xhi = mu / c
        reg1 = xlo <= xhi
        r1 = c * self.rmax(np.minimum(xlo, xhi), xhi)
        r2 = mu + c * self.Tf(xlo)
        val = np.where(reg1, r1, r2)
        if want_regime:
            return val, reg1
        return val

    def H(self, p, q, g, want_regime: bool = False):
        """The same at phi = expit(p), beta = g * expit(q)."""
        return self.H_beta(_expit(p), _expit(-p), g * _expit(q), g, want_regime)

    def _t12(self, phi, c, beta, g):
        """c S(x_lo) and c S(max(x_hi, x_m)) for the interpolant: used only to FIND candidate points."""
        t1 = beta + c * self.Tf(beta / c)
        mu = phi * self.theta_f((g - beta) / phi)
        xh = mu / c
        t2 = np.where(xh >= self.xm, mu + c * self.Tf(xh), c * self.Smin)
        return t1, t2

    def _balance(self, p, g):
        """(surrogate value max(t1, t2), beta) on the balance curve at phi = expit(p)."""
        return balance_min(self._t12, _expit(p), _expit(-p), g, self.xm, 40, 1e-15 * self.a)

    def apply(self, g):
        """R[T](g) for an array g, as the smallest value of the bracket found by two searches:
        (S1) the full grid of (p, q) = (logit phi, logit beta/g), then golden section in p between the
             neighbours of the best p, the inner minimum over q being taken each time by a scan of the whole
             q grid followed by golden section -- no structure assumed, but blind to valleys narrower than
             the grid;
        (S2) golden section in p along the curve beta = beta_bal(p) where S(x_lo) = S(max(x_hi, x_m)) (the
             minimiser over beta when S is quasi-convex), searching on max(c S(x_lo), c S(max(x_hi, x_m)));
             the value recorded is the bracket itself at the point found.
        Returns (value, p, beta, regime-1 flag, S2-wins flag)."""
        g = np.asarray(g, dtype=float)
        self._prep()
        n, nq = g.shape[0], len(self.q_grid)
        Q = np.broadcast_to(self.q_grid[None, :], (n, nq))
        G2 = np.broadcast_to(g[:, None], (n, nq))
        best = np.full(n, np.inf)
        ip = np.zeros(n, dtype=int)
        for k, p in enumerate(self.p_grid):
            vm = self.H(np.full((n, nq), p), Q, G2).min(axis=1)
            m = vm < best
            best = np.where(m, vm, best)
            ip = np.where(m, k, ip)
        plo = self.p_grid[np.maximum(ip - 1, 0)]
        phi_ = self.p_grid[np.minimum(ip + 1, len(self.p_grid) - 1)]

        def outer(p):
            return golden_min_grid(lambda q: self.H(p, q, g), self.q_grid, self.niter)[1]

        pb, vb = golden_min(outer, plo, phi_, 3, self.niter)
        qb, vb2 = golden_min_grid(lambda q: self.H(pb, q, g), self.q_grid, self.niter)
        v1 = np.minimum(np.minimum(vb, vb2), best)
        beta1 = g * _expit(qb)
        # (S2)
        lo = np.full(n, -34.0)
        hi = np.full(n, 34.0)
        pb2, _ = golden_min(lambda p: self._balance(p, g)[0], lo, hi, 21, 44)     # search on the surrogate
        beta2 = self._balance(pb2, g)[1]
        v2 = self.H_beta(_expit(pb2), _expit(-pb2), beta2, g)                     # value: the bracket itself
        s2 = v2 < v1
        val = np.where(s2, v2, v1)
        pbest = np.where(s2, pb2, pb)
        bbest = np.where(s2, beta2, beta1)
        _, reg1 = self.H_beta(_expit(pbest), _expit(-pbest), bbest, g, True)
        self.v_scan, self.v_balance = v1, v2
        return val, pbest, bbest, reg1, s2

    def apply_zero(self):
        self._prep()

        def f0(p):
            phi = _expit(p)
            c = _expit(-p)
            xh = phi * self.a / c
            return c * self.rmax(np.zeros_like(xh), xh)

        p0, v0 = golden_min(f0, np.array([-34.0]), np.array([34.0]), 4001, 70)
        return float(v0[0]), float(p0[0])

    def step(self):
        t0 = time.time()
        g = self.x[1:-1]
        val, pb, bb, reg1, s2 = self.apply(g)
        qc, conc = self.S_quasiconvex, self.max_concavity
        v0, p0 = self.apply_zero()
        raw = np.concatenate([[v0], val, [0.0]])
        old = self.Tf.v
        improved = raw < old - 1e-13 * self.a
        imp = improved[1:-1]
        frac2 = float(np.mean(~reg1[imp])) if np.any(imp) else 0.0
        # how far the structure-free search (S1) stays above / gets below the balance-curve search (S2)
        d12 = (self.v_scan - self.v_balance) / self.a
        self.raw, self.popt, self.bopt, self.reg1 = raw, pb, bb, reg1
        self.Tf.set(np.minimum(old, raw))
        self.k += 1
        rec = dict(k=self.k, tau=float(self.Tf.v[0]), S_quasiconvex_in=qc, max_concavity_in=conc,
                   frac_regime2_among_improved=frac2, n_not_improved=int(np.sum(~improved[:-1])),
                   n_scan_wins=int(np.sum(~s2)), scan_minus_balance_min=float(d12.min()),
                   scan_minus_balance_max=float(d12.max()), seconds=time.time() - t0)
        self.history.append(rec)
        return rec

    def run(self, K: int, verbose: bool = False):
        while self.k < K:
            rec = self.step()
            if verbose:
                print(rec, flush=True)
        return self.history

    def taus(self):
        return {r["k"]: r["tau"] for r in self.history}


# ----------------------------------------------------------------------------------------------------------------
# closed forms and helpers
# ----------------------------------------------------------------------------------------------------------------
def tau2_closed(pair, n: int = 20001) -> float:
    """tau_2 = min_phi max{ (1 - phi) a,  phi a + (1 - phi) theta(phi a/(1 - phi)) }  (THEORY_REPORT 11.19,
    remark (1)), with theta_na evaluated by inversion of its curve."""
    a = float(pair.a)

    def f(phi):
        phi = np.asarray(phi, dtype=float)
        return np.maximum((1 - phi) * a, phi * a + (1 - phi) * pair.theta_na(phi * a / (1 - phi)))

    ph = (np.arange(n) + 0.5) / n
    v = f(ph)
    k = int(np.argmin(v))
    lo, hi = ph[max(k - 1, 0)], ph[min(k + 1, n - 1)]
    c, d = hi - GR * (hi - lo), lo + GR * (hi - lo)
    fc, fd = float(f(c)), float(f(d))
    for _ in range(80):
        if fc <= fd:
            hi, d, fd = d, c, fc
            c = hi - GR * (hi - lo)
            fc = float(f(c))
        else:
            lo, c, fc = c, d, fd
            d = lo + GR * (hi - lo)
            fd = float(f(d))
    return min(fc, fd, float(v[k]))


def richardson_limit(ks, rs):
    """Fit r_k = r_inf + alpha/k + beta/k^2 through three points (k, r_k); returns (r_inf, alpha, beta)."""
    A = np.array([[1.0, 1.0 / k, 1.0 / k**2] for k in ks])
    sol = np.linalg.solve(A, np.asarray(rs, dtype=float))
    return float(sol[0]), float(sol[1]), float(sol[2])
