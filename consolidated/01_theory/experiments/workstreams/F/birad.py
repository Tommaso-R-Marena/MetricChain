"""Workstream F -- exact finite-n computations for functions on {0,1}^n that depend on x only through its
profile relative to a centre s with k ones:
    i = #{l : s_l = 1, x_l = 0} in [0, k],      j = #{l : s_l = 0, x_l = 1} in [0, n-k].
Number of points with profile (i, j): C(k,i) C(n-k,j); type (number of ones) t = k - i + j; Hamming distance between
the nearest points of two profile classes: |i - i'| + |j - j'|.  A function of (i, j) is u-Lipschitz on the cube iff
it is u-Lipschitz on the grid for the l1 distance.  Everything is done with exact binomials in log space.
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def lnC(n, k):
    k = np.asarray(k, dtype=float)
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


class Centre:
    def __init__(self, n, k, p):
        self.n, self.k, self.p, self.q = n, k, p, 1 - p
        self.i = np.arange(k + 1)[:, None]
        self.j = np.arange(n - k + 1)[None, :]
        self.t = k - self.i + self.j                                  # type of the point
        self.dist = self.i + self.j                                    # distance to the centre
        self.logcount = lnC(k, self.i) + lnC(n - k, self.j)
        self.logpi = self.t * math.log(p) + (n - self.t) * math.log(1 - p)   # ln pi(x) for one point
        self.logmass = self.logcount + self.logpi                     # ln pi(profile class)
        self.logdens = self.logcount - lnC(n, self.t)                 # density of the profile class in its type class
        self.cum = None

    # ---- sets ---------------------------------------------------------------------------------------------
    def _cumdens(self):
        """ln of the cumulative density along every type diagonal, in the order of increasing distance to s"""
        if getattr(self, "cum", None) is None:
            k, n = self.k, self.n
            cum = np.full(self.logcount.shape, np.inf)
            for t in range(n + 1):
                i0 = max(0, k - t)
                i1 = min(k, n - t)
                if i0 > i1:
                    continue
                ii = np.arange(i0, i1 + 1)
                jj = t - k + ii
                cum[ii, jj] = np.logaddexp.accumulate(self.logdens[ii, jj])
            self.cum = cum
        return self.cum

    def density_ball(self, logq):
        """the largest set of the form {x : d(x,s) <= r_{type(x)}} whose density in every type class is at most q.
        Returns the boolean mask over (i, j) and the exact largest density (log)."""
        cum = self._cumdens()
        inside = cum <= logq + 1e-12
        maxlog = float(cum[inside].max()) if inside.any() else -math.inf
        return inside, maxlog

    def hamming_ball(self, r):
        inside = self.dist <= r
        return inside, self.max_logdens(inside)

    def max_logdens(self, inside):
        """exact ln max_t density of the set in the type class t"""
        k, n = self.k, self.n
        best = -math.inf
        vals = np.where(inside, self.logdens, -np.inf)
        # sum along diagonals j - i = const
        for off in range(-k, n - k + 1):
            d = np.diagonal(vals, offset=off)
            if d.size and np.isfinite(d).any():
                best = max(best, float(logsumexp(d[np.isfinite(d)])))
        return best

    # ---- envelopes ----------------------------------------------------------------------------------------
    @staticmethod
    def _sweep_min(F, u):
        """F[i,j] <- min_{i',j'} F[i',j'] + u (|i-i'| + |j-j'|)   (separable l1 distance transform)"""
        F = F.copy()
        for ax in (0, 1):
            idx = np.arange(F.shape[ax])
            shape = [1, 1]
            shape[ax] = -1
            ramp = u * idx.reshape(shape)
            fwd = np.minimum.accumulate(F - ramp, axis=ax) + ramp
            Fr = np.flip(F, axis=ax)
            bwd = np.flip(np.minimum.accumulate(Fr - ramp, axis=ax) + ramp, axis=ax)
            F = np.minimum(fwd, bwd)
        return F

    def lower_envelope_logw(self, logw, inside, u):
        """ln of the LARGEST weight w' = e^{-psi'} on `inside` among u-Lipschitz psi' that agree with psi off `inside`:
        w'(x) = min_{y not in D} w(y) e^{u d(x,y)}   (McShane lower envelope of psi)."""
        F = np.where(inside, np.inf, logw + 0.0 * self.logcount)
        return self._sweep_min(F, u)

    def upper_envelope_logw(self, logw, inside, u):
        """ln of the SMALLEST weight on `inside`: w'(x) = max_{y not in D} w(y) e^{-u d(x,y)}."""
        F = np.where(inside, np.inf, -(logw + 0.0 * self.logcount))
        return -self._sweep_min(F, u)

    def logA(self, logw):
        return float(logsumexp(self.logmass + logw))


def is_lipschitz_grid(logw, u, tol=1e-9):
    return (np.abs(np.diff(logw, axis=0)).max(initial=0) <= u + tol) and (np.abs(np.diff(logw, axis=1)).max(initial=0) <= u + tol)


def logw_H(n, p, u, t, ngam=4001):
    """ln w_H at type t (array): max over additive instances |gamma| <= u of the normalised weight
    -gamma t - n ln(q + p e^{-gamma});  psi_H = -ln w_H is u-Lipschitz (a minimum of u-Lipschitz functions)."""
    q = 1 - p
    t = np.asarray(t, dtype=float)
    # closed form: the maximiser has Gibbs mean t/n when that is in the window, else gamma = -+u
    kap = np.clip(t / n, 1e-300, 1 - 1e-300)
    with np.errstate(divide="ignore", invalid="ignore"):
        gam = -(np.log(kap / (1 - kap)) - math.log(p / q))            # Gibbs mean of gamma is kappa
    gam = np.clip(np.nan_to_num(gam, nan=0.0, posinf=u, neginf=-u), -u, u)
    return -gam * t - n * np.log(q + p * np.exp(-gam))
