"""Workstream K, numerical check (i): the level recursion INCLUDING the bounded-accuracy point g = 0.

Exponent functions T_k on [0, eps*]:  T_k(g), g > 0, is the exponent at the extensive accuracy g n, and
tau_k := T_k(0) is the exponent at every fixed accuracy (Theorem K2 of REPORT.md).

    T_1 = theta_na  (T_1(0) = a),        T_{k+1} = min(T_k, R[T_k]),
    R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma >= beta} [ min(gamma, phi theta_na((g-beta)/phi)) + (1-phi) T(gamma/(1-phi)) ]   (g > 0)
    R[T](0) = inf_{0<phi<1}           sup_{gamma >= 0}    [ min(gamma, phi a)                      + (1-phi) T(gamma/(1-phi)) ]

Two evaluations on a grid 0 = g_0 < g_1 < ... :
  mode "lin"  : piecewise-linear interpolation of T_k (accurate, not one-sided);
  mode "step" : T_k replaced by the step function T(g_i) on [g_i, g_{i+1}) (an upper bound because T_k is nonincreasing),
                the supremum over gamma evaluated at the right ends of the steps and the infimum over a finite set of
                (phi, beta): every number produced is a RIGOROUS UPPER BOUND of the exact recursion (up to float rounding
                and the bisection for theta_na, which is evaluated exactly at each call).
Checks: nonincreasing in k and g; never below theta_hint (necessary condition of DEAD_ENDS D45; at g = 0: never below h);
tau_k = T_k(0) against T_k(g_1) (continuity at 0);  tau_2 against the closed form
min_phi max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi)));  tau_k -> h.
"""
import math, sys, time
import numpy as np
from klib import consts, theta_na, theta_hint, kl


class Recursion:
    def __init__(self, u, mode="lin", G=160, P=72, B=20):
        self.u, self.mode = u, mode
        self.pu, self.lam, self.estar, self.a, self.h = consts(u)
        gpos = np.unique(np.concatenate([np.geomspace(1e-6, 0.03, G // 2), np.linspace(0.03, 1.0, G // 2 + 1)])) * self.estar
        self.g = np.concatenate([[0.0], gpos])                 # g_0 = 0 is the bounded-accuracy point
        # theta_na on a fine table for interpolation in mode "lin"; exact calls in mode "step"
        self.nax = np.concatenate([[0.0], np.geomspace(1e-10, 1.0, 4000) * self.estar])
        self.nay = np.array([theta_na(u, x) for x in self.nax])
        self.T = np.array([theta_na(u, x) for x in self.g])
        self.hint = np.array([theta_hint(u, x) for x in self.g])
        self.P, self.B = P, B
        self.levels = 1
        self.argphi0 = None

    def th_na(self, x):
        if self.mode == "step":
            # rigorous upper bound: theta_na is nonincreasing, evaluate the table at the grid point to the LEFT
            idx = np.clip(np.searchsorted(self.nax, x, side="right") - 1, 0, len(self.nax) - 1)
            return np.where(x >= self.estar, 0.0, self.nay[idx])
        return np.where(x >= self.estar, 0.0, np.interp(x, self.nax, self.nay))

    def bracket(self, g, phi, beta):
        """sup over gamma >= beta of min(gamma, mu) + (1-phi) T(gamma/(1-phi)), mu = phi theta_na((g-beta)/phi);
        phi[P,1], beta[1,B] arrays -> values [P,B].  For g = 0 pass beta = [[0.0]]."""
        mu = phi * self.th_na((g - beta) / phi)                                   # [P,B]
        one = (1 - phi)
        gi = self.g                                                               # breakpoints of T
        if self.mode == "step":
            # on the step [g_i, g_{i+1}) (in units gamma = (1-phi) x):  value <= min((1-phi) g_{i+1}, mu) + (1-phi) T(g_i)
            right = np.concatenate([gi[1:], [np.inf]])                            # right ends; T = 0 beyond the last grid point
            hi = one[..., None] * right[None, None, :]                            # [P,1,G]
            val = np.minimum(hi, mu[..., None]) + one[..., None] * self.T[None, None, :]
            val = np.where(hi > beta[..., None], val, -np.inf)                    # steps entirely below beta are not in the range
            return val.max(axis=2)
        # mode "lin": evaluate at gamma = beta, at the kink gamma = mu (if >= beta), and at all breakpoints in [beta, max(beta,mu)]
        top = np.maximum(mu, beta)
        cand = one[..., None] * gi[None, None, :]                                 # [P,1,G]
        cand = np.clip(cand, beta[..., None], top[..., None])                     # [P,B,G]
        gam = np.concatenate([cand, top[..., None], np.broadcast_to(beta[..., None], top[..., None].shape)], axis=2)
        Tv = np.interp(gam / one[..., None], self.g, self.T, right=0.0)
        val = np.minimum(gam, mu[..., None]) + one[..., None] * Tv
        return val.max(axis=2)

    def step(self):
        new = self.T.copy()
        geo = np.geomspace(1e-4, 0.5, self.P // 2)
        lin = np.linspace(0.01, 0.99, self.P // 2)
        for i, g in enumerate(self.g):
            phis = list(geo) + list(lin)
            if g > 0:
                th = self.hint[i]
                if th > 0:
                    phis.append(g / (g + th))
                if g < self.h:
                    phis.append(g / self.h)
                betas = g * np.geomspace(1e-6, 0.999, self.B)
            else:
                betas = np.zeros(1)
            phis = np.array(sorted(set(phis)))
            best = new[i]
            for rnd in range(3):                                  # coarse grid, then two local refinements around the best cell
                v = self.bracket(g, phis[:, None], betas[None, :])
                jp, jb = np.unravel_index(int(np.argmin(v)), v.shape)
                if float(v[jp, jb]) < best:
                    best = float(v[jp, jb])
                    if g == 0:
                        self.argphi0 = float(phis[jp])
                lo, hi = phis[max(jp - 1, 0)], phis[min(jp + 1, len(phis) - 1)]
                phis = np.linspace(lo, hi, 11)
                if g > 0:
                    blo, bhi = betas[max(jb - 1, 0)], betas[min(jb + 1, len(betas) - 1)]
                    betas = np.geomspace(blo, bhi, 7)
            new[i] = min(new[i], best)
        self.T = np.minimum.accumulate(new)       # T_k is nonincreasing in the accuracy (T(0) is the first entry)
        self.levels += 1


def closed_tau2(u):
    pu, lam, estar, a, h = consts(u)
    phis = np.linspace(1e-3, 0.999, 4000)
    return min(max((1 - p) * a, p * a + (1 - p) * theta_na(u, p * a / (1 - p))) for p in phis)


def main(depth=40, quick=False):
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    ok = True
    t0 = time.time()
    for u in (0.5, 1.0, 2.0):
        pu, lam, estar, a, h = consts(u)
        out(f"\n=== u = {u}:  a = {a:.6f},  h = {h:.6f},  h/a = {h / a:.5f},  eps* = {estar:.6f}")
        c2 = closed_tau2(u)
        res = {}
        for mode in ("lin", "step"):
            r = (Recursion(u, mode=mode, G=160 if mode == "lin" else 240) if not quick
                 else Recursion(u, mode=mode, G=80, P=40, B=12))
            prev = r.T.copy()
            out(f"mode {mode}:   k | tau_k/a = T_k(0)/a | T_k(g_1)/a (g_1 = 1e-6 eps*) | (tau_k - h)/a | max_g (T_k - theta_hint)/a | argmin phi at g=0")
            for k in range(2, depth + 1):
                r.step()
                if np.any(r.T > prev + 1e-12) or np.any(np.diff(r.T) > 1e-12):
                    ok = False; out("   NOT nonincreasing in k / in g")
                if np.any(r.T < r.hint - (2e-4 * a if mode == "lin" else 1e-12)):
                    ok = False; out(f"   a level is BELOW theta_hint by {float(np.max(r.hint - r.T)) / a:.2e} a")
                if r.T[0] < h - (2e-4 * a if mode == "lin" else 1e-12):
                    ok = False; out("   tau_k BELOW h")
                if k == 2 and abs(r.T[0] - c2) > (2e-3 * a if mode == "lin" else 1e-2 * a):
                    ok = False; out(f"   tau_2 = {r.T[0] / a:.5f} a differs from the closed form {c2 / a:.5f} a")
                if k in (2, 3, 4, 5, 6, 8, 10, 14, 20, 30, 40, 60, 80) or k == depth:
                    out(f"          {k:3d} | {r.T[0] / a:18.5f} | {r.T[1] / a:29.5f} | {(r.T[0] - h) / a:13.5f} | {float(np.max(r.T - r.hint)) / a:26.5f} | {r.argphi0:.4f}")
                prev = r.T.copy()
            res[mode] = r
        out(f"closed form tau_2 = min_phi max((1-phi)a, phi a + (1-phi) theta_na(phi a/(1-phi))) = {c2 / a:.5f} a")
        out(f"after {depth} levels:  tau_k/h = {res['lin'].T[0] / h:.4f} (lin),  {res['step'].T[0] / h:.4f} (step: rigorous upper bound of the exact recursion)")
        if not (res["step"].T[0] >= res["lin"].T[0] - 1e-3 * a):
            ok = False; out("   the one-sided evaluation is below the piecewise-linear one")
        if res["lin"].T[0] > h + 0.02 * a:
            ok = False; out("   tau_k does not approach h")
    out(f"\nall checks passed: {ok}    ({time.time() - t0:.0f} s)")
    open("out_recursion_bounded.txt", "w").write("\n".join(lines) + "\n")
    return ok


if __name__ == "__main__":
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    sys.exit(0 if main(depth=12 if quick else 40, quick=quick) else 1)
