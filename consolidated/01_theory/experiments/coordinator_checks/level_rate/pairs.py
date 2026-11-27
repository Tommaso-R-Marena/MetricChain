"""The two pairs of exponent functions (Gaussian small-slope limit; cube)."""
import math
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


