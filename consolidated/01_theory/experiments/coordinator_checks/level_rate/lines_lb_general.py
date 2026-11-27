"""The lower bound from lines for a general pair given by its dual function J (coordinator's check).

Everything in the line lemma is a statement about J(t) = inf_e [(1 - t) theta_na(e) + t e] on [0, 1] (the "game
function" F* of theory report 11.21):  h = max J = J(t*),  a = lim_{t -> 1} J(t)/(1 - t),  theta_hint''(0) = -1/J''(t*),
and with Q(t) = J(t)/(1 - t) (increasing) the slope map is
        t' = Q^{-1}(B/(1 - sigma)),      sigma' = t' (1 - sigma)/(1 - t');
the tangent line of theta_na with intercept B is the image of the flat line (B, 0).  Hence
        tau_k >= B   whenever the orbit of sigma = 0 stays below 1 - B/a for k - 1 steps,
and the conjectured law is k^2 (tau_k - h) -> 2 pi^2 h^2 / (-J''(t*)).

Pairs: the cube (J(t) = Lambda(t u) - t Lambda(u)), the Gaussian pair (J = t - t^2), and the p-biased cube of theory
report 11.20, whose J is the game function F*(t) = max_gamma F(gamma, t) (closed form of Theorem 11.59(b), copied
from the harness helper fd_game).
Usage: python3 lines_lb_general.py > out_lines_lb_general.txt
"""
import math
import numpy as np


def J_cube(u):
    L = lambda v: np.log(2 / (1 + np.exp(-v)))
    return lambda t: L(t * u) - t * L(u)


def J_gauss():
    return lambda t: t - t * t


def J_field(p, u, ngam=1201):
    q = 1 - p
    L0, L1 = -math.log(q + p * math.exp(-u)), -math.log(p + q * math.exp(-u))
    gam = np.linspace(-u * (1 - 1e-9), u * (1 - 1e-9), ngam)

    def J(t):
        t = np.atleast_1d(np.asarray(t, dtype=float))
        out = np.zeros_like(t)
        idx = np.where(t > 1e-12)[0]
        for c0 in range(0, len(idx), 1000):                  # in chunks: the table gamma x t must stay small in memory
            ii = idx[c0:c0 + 1000]
            G, TT = np.meshgrid(gam, t[ii], indexing="ij")
            Fv = (-TT * np.log(q + p * np.exp(-G)) + np.log((1 - np.exp(-TT * (u + G))) * np.exp(-TT * L0)
                  + (1 - np.exp(-TT * (u - G))) * np.exp(-TT * (L1 + G))) - np.log(1 - np.exp(-2 * TT * u)))
            out[ii] = Fv.max(axis=0)
        return out
    return J


def analyse(name, J, ks):
    t = np.linspace(0.0, 1.0, 200001)[1:-1]
    Jt = np.asarray(J(t), dtype=float)
    i = int(np.argmax(Jt))
    # refine the maximum and the second derivative by a local quartic fit
    w = slice(max(i - 2000, 0), min(i + 2001, len(t)))
    co = np.polyfit(t[w] - t[i], Jt[w], 4)
    d = np.roots(np.polyder(co))
    d = d[np.isreal(d)].real
    d = d[np.argmin(np.abs(d))]
    tstar = t[i] + d
    h = float(np.polyval(co, d))
    J2 = float(np.polyval(np.polyder(co, 2), d))
    Q = Jt / (1 - t)
    a = float(Q[-1])                       # J(t)/(1 - t) at t -> 1
    if not np.all(np.diff(Q) > -1e-12):
        print("# %s: Q = J/(1-t) is not increasing on the grid (max decrease %.2e)" % (name, float(-np.diff(Q).min())))
    const = 2 * math.pi ** 2 * h * h / (-J2)
    print("# %s:  h = %.8f  t* = L_h = %.6f  a = %.6f  theta_hint''(0) = -1/J''(t*) = %.6f   2 pi^2 h^2 theta_hint''(0) = %.8f" %
          (name, h, tstar, a, -1 / J2, const))

    def survives(B, k):
        s = 0.0
        for _ in range(k):                 # the flat line, then k - 1 further steps: s_0 .. s_{k-2} must stay regular
            if not s < 1 - B / a:
                return False
            target = B / (1 - s)
            if target >= Q[-1]:
                return False
            j = int(np.searchsorted(Q, target))
            if j == 0:
                tp = t[0] * target / Q[0]
            else:
                tp = t[j - 1] + (t[j] - t[j - 1]) * (target - Q[j - 1]) / (Q[j] - Q[j - 1])
            s = tp * (1 - s) / (1 - tp)
        return True

    print("#    k   tau_k^LB       k^2 (tau_k^LB - h)   ratio to the constant")
    for k in ks:
        lo, hi = h * (1 + 1e-9), a
        if not survives(lo, k):
            print("  %4d   (a line with intercept h does not stay regular: grid resolution)" % k)
            continue
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if survives(mid, k) else (lo, mid)
        print("  %4d   %.10f   %.8f          %.5f" % (k, lo, k * k * (lo - h), k * k * (lo - h) / const))
    print()


KS = [2, 3, 5, 10, 20, 40, 80, 160]
analyse("Gaussian pair", J_gauss(), KS)
analyse("cube u = 1", J_cube(1.0), KS)
for p, u in [(0.3, 1.0), (0.1, 1.0), (0.1, 2.0), (0.02, 2.0)]:
    analyse("biased cube p = %g, u = %g" % (p, u), J_field(p, u), KS)
