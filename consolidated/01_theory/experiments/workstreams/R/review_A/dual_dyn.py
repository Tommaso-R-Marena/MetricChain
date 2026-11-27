"""Referee A: the exact dynamics of convex majorants (remark (1) of section 5) as a small class (same algorithm as
a3_dual_dynamics.py).  sig3(B, s) -> (Sigma, dSigma/dB, dSigma/ds), inf if not regular."""
import math


class DualDyn:
    def __init__(self, sig3, a, nbis=70):
        self.sig3, self.a, self.nbis = sig3, a, nbis
        self.cuts = []          # cuts[k-1] = (Bc, Sc, m, tau) of S_k
        self.tau = a

    def S(self, k, B):
        i = k
        while i >= 1 and B < self.cuts[i - 1][0]:
            i -= 1
        if i == 0:
            val, der = 0.0, 0.0
        else:
            Bc, Sc, m, _ = self.cuts[i - 1]
            val, der = Sc + m * (B - Bc), m
        for _ in range(i, k):
            v, dB, ds = self.sig3(B, val)
            if not math.isfinite(v):
                return math.inf, math.inf
            val, der = v, dB + ds * der
        return val, der

    def H(self, k, B):
        v, d = self.S(k, B)
        if not math.isfinite(v):
            return math.inf, math.inf
        w, dB, ds = self.sig3(B, v)
        if not math.isfinite(w):
            return math.inf, math.inf
        return w, dB + ds * d

    def step(self):
        k = len(self.cuts) + 1
        a = self.a
        lo, hi = 0.0, self.tau
        for _ in range(self.nbis):
            mid = 0.5 * (lo + hi)
            if self.S(k - 1, mid)[0] + mid / a < 1.0:
                lo = mid
            else:
                hi = mid
        tau = 0.5 * (lo + hi)

        def Gf(B):
            v, d = self.H(k - 1, B)
            if not math.isfinite(v):
                return math.inf
            return v + d * (tau - B) - 1.0
        eps0 = 1e-13 * tau
        if Gf(eps0) >= 0:
            Bc, Sc, m = 0.0, 0.0, 1.0 / tau
        else:
            lo, hi = eps0, tau
            for _ in range(self.nbis):
                mid = 0.5 * (lo + hi)
                if Gf(mid) < 0:
                    lo = mid
                else:
                    hi = mid
            Bc = lo
            Sc, m = self.H(k - 1, Bc)
            m = (1.0 - Sc) / (tau - Bc)
        self.cuts.append((Bc, Sc, m, tau))
        self.tau = tau
        return tau


def gauss_sig3(B, s):
    y = 1.0 - s
    if y - B <= 0:
        return math.inf, math.inf, math.inf
    d = y - B
    return B * y / d, y * y / (d * d), B * B / (d * d)
