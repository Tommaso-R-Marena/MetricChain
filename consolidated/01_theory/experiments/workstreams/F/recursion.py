"""Workstream F -- the level recursion T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]),
   R[T](g) = inf_{phi, beta} sup_{gamma >= beta} [ min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) T(gamma/(1-phi)) ],
for an arbitrary pair (theta_na, theta_hint) given as callables (own implementation; grid + piecewise-linear
interpolation, as in the repository's LvRecursion, which is for the uniform cube)."""
import math
import numpy as np


class Recursion:
    def __init__(self, th_na, hint, a, h, E, G=120, P=48, B=18, C=48, start=None):
        self.a, self.h, self.E = a, h, E
        self.g = np.unique(np.concatenate([np.geomspace(1e-4, 0.05, G // 3), np.linspace(0.05, 1.0, 2 * G // 3)])) * E
        self.nax = np.concatenate([[0.0], np.geomspace(1e-9, 1.0, 3000) * E])
        self.nay = np.array([a] + [th_na(x) for x in self.nax[1:]])
        self.hint = np.array([hint(x) for x in self.g])
        self.T = np.interp(self.g, self.nax, self.nay) if start is None else np.array([start(x) for x in self.g])
        self.P, self.B, self.C = P, B, C
        self.levels = 1

    def th_na(self, x):
        return np.interp(x, self.nax, self.nay, right=0.0)

    def Tv(self, x):
        out = np.interp(x, self.g, self.T, left=self.T[0], right=0.0)
        return np.where(x >= self.E, 0.0, out)

    def step_value(self, g, phi, beta):
        mu = phi * self.th_na((g - beta) / phi)
        top = np.maximum(mu, beta)
        frac = np.concatenate([np.linspace(0, 1, self.C), np.geomspace(1e-5, 1, 16)])[None, None, :]
        gam = beta[..., None] + (top - beta)[..., None] * frac
        val = np.minimum(gam, mu[..., None]) + (1 - phi)[..., None] * self.Tv(gam / (1 - phi)[..., None])
        return val.max(axis=2)

    def step(self):
        new = self.T.copy()
        for i, g in enumerate(self.g):
            phis = list(np.linspace(0.01, 0.99, self.P))
            th = self.hint[i]
            if th > 0:
                phis.append(g / (g + th))
            if g < self.h:
                phis.append(g / self.h)
            phi = np.array(phis)[:, None]
            beta = (g * np.geomspace(1e-5, 0.999, self.B))[None, :]
            new[i] = min(new[i], float(self.step_value(g, phi, beta).min()))
        self.T = np.minimum.accumulate(new)
        self.levels += 1
