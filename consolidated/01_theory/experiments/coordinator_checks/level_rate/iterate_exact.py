"""Exploration (coordinator): the level recursion T_{k+1} = min(T_k, R[T_k]) iterated on a geometric grid with
linear interpolation (NOT one-sided: an approximation, not a bound), to test the conjecture
    k^2 (tau_k - h)  ->  2 pi^2 h^2 theta_hint''(0).
R[T](g) = inf_{phi, beta} sup_{gamma >= beta} [min(gamma, mu) + (1 - phi) T(gamma/(1 - phi))],  mu = phi theta_na((g - beta)/phi)
        = inf max{ (1 - phi) sup_{[beta/(1-phi), mu/(1-phi)]} S   (mu >= beta),   mu + (1 - phi) T(beta/(1 - phi))   (mu < beta) },
S(x) = x + T(x).  At accuracy zero: tau' = inf_phi (1 - phi) sup_{0 < x <= phi a/(1 - phi)} S(x).
Usage: python3 iterate_exact.py pair levels [ratio] [ne] > out
  pair: gauss | cube:<u>
"""
import sys, math, time
import numpy as np


def kl(x, y):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(x > 0, x * np.log(x / y), 0.0)
        t2 = np.where(x < 1, (1 - x) * np.log((1 - x) / (1 - y)), 0.0)
    return t1 + t2


class Gauss:
    name = "gauss"
    a, h, estar = 1.0, 0.25, 1.0
    hint2 = 0.5                      # theta_hint''(0)
    Lh = 0.5

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        return np.where(x >= 1, 0.0, (1 - np.sqrt(np.clip(x, 0, 1))) ** 2)

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        return np.where(e >= 1, 0.0, (1 - np.clip(e, 0, 1)) ** 2 / 4)


class Cube:
    def __init__(self, u):
        self.name = "cube u=%g" % u
        self.u = u
        self.pu = 1 / (1 + math.exp(u))
        self.lam1 = math.log(2 / (1 + math.exp(-u)))
        self.estar = math.log(math.cosh(u / 2))
        self.a = float(kl(self.pu, 0.5))
        self.rho_h = self.lam1 / u
        self.h = float(kl(self.rho_h, 0.5))
        self.hint2 = 1 / (u * u * self.rho_h * (1 - self.rho_h))
        self.Lh = math.log((1 - self.rho_h) / self.rho_h) / u

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        rho = (self.lam1 + e) / self.u
        return np.where(rho < 0.5, kl(np.minimum(rho, 0.5), 0.5), 0.0)

    def theta_na(self, x):
        x = np.asarray(x, dtype=float)
        lo = np.full(x.shape, self.pu)
        hi = np.full(x.shape, 0.5)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ok = kl(mid, self.pu) <= x
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        out = kl(0.5 * (lo + hi), 0.5)
        return np.where(x >= self.estar, 0.0, np.where(x <= 0, self.a, out))


class RangeMax:
    def __init__(self, v):
        n = len(v)
        self.tab = [np.asarray(v, dtype=float)]
        j = 1
        while (1 << j) <= n:
            prev = self.tab[-1]
            half = 1 << (j - 1)
            self.tab.append(np.maximum(prev[:n - (1 << j) + 1], prev[half:half + n - (1 << j) + 1]))
            j += 1

    def query(self, lo, hi):
        """max v[lo..hi] inclusive, arrays; requires lo <= hi."""
        length = hi - lo + 1
        j = np.floor(np.log2(np.maximum(length, 1))).astype(int)
        out = np.empty(lo.shape)
        for jj in np.unique(j):
            m = j == jj
            t = self.tab[jj]
            out[m] = np.maximum(t[lo[m]], t[hi[m] - (1 << jj) + 1])
        return out


def main():
    pair = sys.argv[1]
    levels = int(sys.argv[2])
    ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 1.01
    ne = int(sys.argv[4]) if len(sys.argv) > 4 else 500
    P = Gauss() if pair == "gauss" else Cube(float(pair.split(":")[1]))
    a, h, estar = P.a, P.h, P.estar
    Cpred = 2 * math.pi ** 2 * h * h * P.hint2
    print("# pair %s  a=%.10g h=%.10g eps*=%.10g  L_h=%.6g  theta_hint''(0)=%.8g" % (P.name, a, h, estar, P.Lh, P.hint2))
    print("# conjectured limit of k^2 (tau_k - h): 2 pi^2 h^2 theta_hint''(0) = %.8g  (= %.6g a)" % (Cpred, Cpred / a))
    xmin = 1e-11
    G = int(math.ceil(math.log(estar / xmin) / math.log(ratio)))
    x = np.concatenate([[0.0], estar * ratio ** (np.arange(-G, 1.0))])      # x[0] = 0 (meaning 0+), x[-1] = eps*
    n = len(x)
    T = P.theta_na(x)
    T[0] = a
    T[-1] = 0.0
    th = P.theta_hint(x)
    # parameter grids
    e_grid = np.unique(np.concatenate([
        np.exp(np.linspace(math.log(1e-5), math.log(estar), ne // 2)),
        h * np.exp(np.linspace(-0.5, 0.5, ne)),
        h * np.exp(np.linspace(-0.05, 0.05, ne // 2))]))
    e_grid = e_grid[e_grid <= estar]
    tna_e = P.theta_na(e_grid)
    bfr = np.array([0.0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9])
    phi0 = np.concatenate([np.exp(np.linspace(math.log(1e-12), math.log(1e-3), 1200)), np.linspace(1e-3, 0.999, 1500)[1:]])
    print("# grid: %d points, ratio %g; e-grid %d; beta fractions %d" % (n, ratio, len(e_grid), len(bfr)))
    print("# k  tau_k  (tau_k-h)/a  k^2 (tau_k-h)  ratio_to_conjecture  [profile D_k(zeta h/k)/(q h) k^2 at zeta = .25 .5 1 2 3 5]  secs")
    q = h * P.hint2
    t0 = time.time()
    for k in range(1, levels + 1):
        tau = T[0]
        if k == 1 or k % 5 == 0 or k <= 12:
            zs = np.array([0.25, 0.5, 1, 2, 3, 5.0])
            xs = zs * h / k
            Dk = np.interp(xs, x, T) - P.theta_hint(xs)
            prof = " ".join("%.4f" % v for v in Dk * k * k / (q * h))
            print("%d %.10f %.6f %.6f %.5f  [%s]  %.0f" % (k, tau, (tau - h) / a, k * k * (tau - h), k * k * (tau - h) / Cpred, prof,
                                                          time.time() - t0), flush=True)
        if k == levels:
            break
        S = x + T
        S[0] = tau
        rm = RangeMax(S)
        newT = T.copy()
        # accuracy zero
        X = phi0 * a / (1 - phi0)
        jhi = np.searchsorted(x, X, side="right") - 1
        mx = np.maximum(rm.query(np.zeros_like(jhi), jhi), X + np.interp(X, x, T))
        newT[0] = min(tau, float(np.min((1 - phi0) * mx)))
        # positive accuracies, chunked over beta fractions
        g = x[1:, None]                                           # (n-1, 1)
        best = np.full(n - 1, np.inf)
        for bf in bfr:
            beta = bf * g
            phi = (g - beta) / e_grid[None, :]                     # (n-1, ne)
            ok = phi < 0.999
            phi = np.where(ok, phi, 0.5)
            mu = phi * tna_e[None, :]
            lo = beta / (1 - phi) * np.ones_like(phi)
            hi = mu / (1 - phi)
            caseA = hi >= lo
            # case A: (1 - phi) max S over [lo, hi]
            hiA = np.where(caseA, hi, lo)
            jlo = np.searchsorted(x, lo.ravel(), side="left").reshape(lo.shape)
            jhi = (np.searchsorted(x, hiA.ravel(), side="right") - 1).reshape(lo.shape)
            jlo = np.minimum(jlo, n - 1)
            Slo = lo + np.interp(lo.ravel(), x, T).reshape(lo.shape)
            if bf == 0.0:
                Slo = np.full_like(lo, tau)
            Shi = hiA + np.interp(hiA.ravel(), x, T).reshape(lo.shape)
            inner = np.maximum(Slo, Shi)
            has = jhi >= jlo
            if has.any():
                inner_grid = rm.query(jlo[has], jhi[has])
                tmp = inner[has]
                inner[has] = np.maximum(tmp, inner_grid)
            VA = (1 - phi) * inner
            VB = mu + (1 - phi) * (Slo - lo)
            V = np.where(caseA, VA, VB)
            V = np.where(ok, V, np.inf)
            best = np.minimum(best, V.min(axis=1))
        newT[1:] = np.minimum(T[1:], best)
        newT = np.minimum.accumulate(newT)                         # nonincreasing in the accuracy
        newT = np.maximum(newT, th)                                # never below the hinted exponent (true for the exact recursion)
        newT[0] = max(newT[0], h)
        T = newT


main()
