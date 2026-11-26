#!/usr/bin/env python3
"""r26_cost.py -- workstream R26, Item 1 (iii): what a boundary influence iota costs, on the one family for which
the theory division has a cost theory (the uniform outer cube Q_m with slope u; Theorem N1 with Harper's functions).

Three routes for an outer block of m binary sites one of which (the boundary site) carries the influence iota:
  (P) product known part (iota = 0): Harper's functions of slope u on Q_m;
  (E) the envelope of Theorem N4: slopes u on m-1 sites and u + iota on the boundary site.  Valid tail functions:
        upper: the sorted-slope Harper bound of N_REPORT Lemma N14 with U_j = iota + j u:
               Xi(q) = 2^-m [ (e^{u+iota} - 1)|B(m,r)| + e^iota sum_{j=2}^{r+1} (e^{ju} - e^{(j-1)u}) |B(m, r+1-j)| ],
               r the least radius with |B(m,r)| >= 2^m q   (0 below the atom, +inf at r = m);
        lower: Theta(p) = (1 - e^-iota) p + e^-iota Theta_u(p)     (because rho <= u d_H + iota off the set);
  (C) conditioning on the boundary site: two product sub-problems on Q_{m-1}, each with half of delta.
For each route: the closing level pi_* of N_REPORT 2.2 and the outer-sample scale M_dagger = K/((1-eta) pi_*);
route (C) is charged 2 M_dagger(m-1).  Parameters lam = 1, eta = 1/2, eta' = 1, nu1 = 1, b = 0.5, delta = 0.05,
ln(Vmax/s0) = 2 u m (the cube's value).
Checks (each can fail): (E) with iota = 0 equals (P); Xi_E >= Xi_P and Theta_E <= Theta_P pointwise; the sorted-slope
bound dominates the exact Lemma N.0 function on Q_3 and Q_4 (all subsets) for the one-hot-site envelope.
"""
import math
import resource
import sys
import time

import numpy as np

import r26_alg as A


class OneHot:
    def __init__(self, m, u, iota):
        self.H = A.HarperCube(m, u)
        self.m, self.u, self.iota = m, u, iota
        H = self.H
        self.E = np.zeros(m + 1)
        for r in range(m + 1):
            tot = math.expm1(u + iota) * H.ball[r]
            for j in range(2, r + 2):
                tot += math.exp(iota) * (math.exp(j * u) - math.exp((j - 1) * u)) * H.ball[r + 1 - j]
            self.E[r] = tot

    def Xi(self, q):
        r = self.H.radius(q)
        if r < 0:
            return 0.0
        if r >= self.m:
            return math.inf
        return self.E[r] / self.H.size

    def Theta(self, p):
        return (1 - math.exp(-self.iota)) * p + math.exp(-self.iota) * self.H.Theta(p)

    def closing_level(self, theta, eta, nu0):
        c = (1 - eta) / (1 + eta)
        H = self.H
        best = 1.0 / H.size
        for r in range(0, self.m):
            qleft = (H.ball[r - 1] if r >= 1 else 1.0) / H.size
            xi = self.E[r] / H.size
            if xi <= theta * (1 - eta) * nu0 * qleft and xi <= theta * max(c * qleft, self.Theta(c * qleft)):
                best = H.ball[r] / H.size
            else:
                break
        return best


def consts(m, u, theta, delta, pi_fn):
    lam, eta, etap, nu1, b = 1.0, 0.5, 1.0, 1.0, 0.5
    J = math.ceil(2 * u * m / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    pi = pi_fn(theta, eta, nu0)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * 4 / delta))
    return pi, K / ((1 - eta) * pi)


def main():
    viol = 0
    # checks
    for m in (8, 20):
        for u in (0.5, 1.0):
            O0 = OneHot(m, u, 0.0)
            H = A.HarperCube(m, u)
            O2 = OneHot(m, u, 2.0)
            for q in np.linspace(0.001, 0.999, 300):
                x0, xh, x2 = O0.Xi(q), H.Xi(q), O2.Xi(q)
                if np.isfinite(xh):
                    if abs(x0 - xh) > 1e-12 * max(1.0, xh) or x2 < xh - 1e-12:
                        viol += 1
                elif not (np.isinf(x0) and np.isinf(x2)):
                    viol += 1
                if abs(O0.Theta(q) - H.Theta(q)) > 1e-12:
                    viol += 1
                # the lower functions are compared after the maximum with the Markov bound (Harper's step function
                # can lie below p; the first version of this check compared the raw functions: 300 false alarms)
                if max(q, O2.Theta(q)) > max(q, H.Theta(q)) + 1e-12:
                    viol += 1
    print(f"check 1 (iota = 0 reproduces Harper; monotone in iota): violations {viol}")
    v2, worst = 0, 0.0
    for m in (3, 4):
        pts = np.arange(1 << m)
        ham = np.array([[bin(int(a) ^ int(c)).count("1") for c in pts] for a in pts], dtype=float)
        hot = np.array([[float(((a ^ c) >> (m - 1)) & 1) for c in pts] for a in pts])
        mu = np.full(1 << m, 1.0 / (1 << m))
        for u, iota in ((1.0, 0.5), (1.0, 3.0), (0.5, 8.0)):
            En = A.EnumeratedEnvelope(mu, u * ham + iota * hot)
            O = OneHot(m, u, iota)
            for q in np.linspace(0.02, 0.98, 97):
                xe, xo = En.Xi(q), O.Xi(q)
                te, to = En.Theta(q), O.Theta(q)
                if xe > xo * (1 + 1e-10) or max(q, te) < max(q, to) * (1 - 1e-10):
                    v2 += 1
                if xo > 0 and np.isfinite(xo):
                    worst = max(worst, xo / max(xe, 1e-300))
    print(f"check 2 (sorted-slope bound and the lower function against the exact Lemma N.0 functions of the "
          f"one-hot-site envelope, all subsets of Q_3 and Q_4, 3 parameter pairs): violations {v2}; "
          f"largest bound/exact for Xi: {worst:.2f}")
    viol += v2
    print()
    print("outer-sample scale M_dagger = K/((1-eta) pi_*): product (P), envelope of Theorem N4 (E), conditioning (C)")
    print("    m    u  theta  iota |  ln M_dag(P)  ln M_dag(E)  ln M_dag(C) |  E/P      C/P    | cheaper")
    for m in (12, 20, 40, 80):
        for u in (1.0,):
            for theta in (1.0, 20.0):
                piP, MP = consts(m, u, theta, 0.05, A.HarperCube(m, u).closing_level)
                piC, MC1 = consts(m - 1, u, theta, 0.025, A.HarperCube(m - 1, u).closing_level)
                MC = 2 * MC1
                for iota in (0.5, 1.0, 2.5, 5.0, 8.0, 11.5):
                    piE, ME = consts(m, u, theta, 0.05, OneHot(m, u, iota).closing_level)
                    print(f"  {m:3d} {u:4.1f} {theta:5.1f} {iota:5.1f} |  {math.log(MP):10.2f}  {math.log(ME):10.2f}  "
                          f"{math.log(MC):10.2f}  | {ME / MP:9.3g} {MC / MP:7.3g} | {'E' if ME < MC else 'C'}")
    print()
    print("the same with the accuracy re-tuned instead of the cost: the threshold theta_E at which route (E) has the "
          "closing level of route (P) at theta (so the certified ratio e^x_out grows by about theta_E/theta)")
    print("    m  theta  iota | theta_E   theta_E/theta   e^iota")
    for m in (20, 40):
        for theta in (1.0, 20.0):
            piP, MP = consts(m, 1.0, theta, 0.05, A.HarperCube(m, 1.0).closing_level)
            for iota in (0.5, 1.0, 2.5, 5.0, 8.0):
                O = OneHot(m, 1.0, iota)
                lo, hi = theta, theta * math.exp(iota + 3)
                for _ in range(60):
                    mid = math.sqrt(lo * hi)
                    piE, _ = consts(m, 1.0, mid, 0.05, O.closing_level)
                    if piE >= piP:
                        hi = mid
                    else:
                        lo = mid
                print(f"  {m:3d} {theta:5.1f} {iota:5.1f} | {hi:9.3g}  {hi / theta:9.3g}      {math.exp(iota):9.3g}")
    print(f"total violations: {viol}")
    return viol


if __name__ == "__main__":
    t0 = time.time()
    print(f"r26_cost.py; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    v = main()
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
    sys.exit(1 if v else 0)
