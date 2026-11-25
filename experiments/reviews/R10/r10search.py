"""outer searches over block profiles (own code).  Parametrisation: k blocks,
theta = (w_1..w_{k-1}, t_1..t_k): weights = softmax(0, w), values = sigmoid(t)."""
import numpy as np
from scipy import optimize
from r10lib import *


def prof(theta, k):
    theta = np.asarray(theta, float)
    w = np.concatenate(([0.0], theta[:k - 1]))
    w = w - w.max()
    lam = np.exp(w)
    lam /= lam.sum()
    mu = 1.0 / (1.0 + np.exp(-np.clip(theta[k - 1:], -40, 40)))
    return lam, mu


def unprof(lam, mu):
    lam = np.asarray(lam, float)
    mu = np.clip(np.asarray(mu, float), 1e-12, 1 - 1e-12)
    w = np.log(lam[1:] / lam[0])
    return np.concatenate((w, np.log(mu / (1 - mu))))


def make_obj(model, e, k, **kw):
    def f(theta):
        lam, mu = prof(theta, k)
        if lam.min() < 1e-9:
            return 0.0
        val = r_mu(model, lam, mu, e, **kw)
        if not np.isfinite(val):
            return 0.0
        return -val
    return f


def nm(model, e, lam, mu, kw=None, xatol=1e-9, fatol=1e-13, maxiter=4000, step=0.05):
    kw = kw or {}
    k = len(mu)
    f = make_obj(model, e, k, **kw)
    x0 = unprof(lam, mu)
    sim = np.vstack([x0] + [x0 + step * np.eye(len(x0))[i] for i in range(len(x0))])
    res = optimize.minimize(f, x0, method='Nelder-Mead',
                            options={'xatol': xatol, 'fatol': fatol, 'maxiter': maxiter,
                                     'maxfev': maxiter, 'initial_simplex': sim})
    lam2, mu2 = prof(res.x, k)
    return -res.fun, lam2, mu2


def fmt(lam, mu):
    o = np.argsort(mu)
    return "  ".join(f"{mu[i]:.5f}@{lam[i]:.5f}" for i in o)
