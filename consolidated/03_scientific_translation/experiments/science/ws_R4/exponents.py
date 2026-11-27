#!/usr/bin/env python3
"""R4 (SCI-REV-0003) -- own re-computation of the exponents of theory report section 11.24.

Written from the STATEMENTS in THEORY_REPORT.md section 11.24 (Theorems 11.84(b), 11.86) only;
none of the authors' code was read before this file was written.  (A first, scalar version of
this file was too slow on the shared machine and was replaced by this vectorised one; the
formulas are the same.)

Quantities (natural logarithms throughout):
  p_u = 1/(1+e^u),  Lambda1 = ln(2/(1+e^{-u})),
  f(rho) = KL(rho || 1/2),  k(rho) = KL(rho || p_u) = f(rho) + u rho - Lambda1,
  a = f(p_u),  h = f(Lambda1/u),
  theta_na(e) = min{ f(rho) : k(rho) <= e }   (0 for e >= eps* = ln cosh(u/2)),
  D(theta) = u f^{-1}(theta) - Lambda1,  x_na(theta) = D(theta) + theta,
  Xi(theta, phi1) = min_{0<=c<=min(theta, phi1 a)} [ phi1 x_na(c/phi1) + phi2 D((theta-c)/phi2) ],
  theta2*(u) = sup{ theta : Xi(theta,phi1) > 0 and theta < phi2 a for some phi1 },
  T2(0) = min_{phi, xi} max{ phi a + (1-phi) theta_na(xi),  min(phi a, (1-phi) xi) + (1-phi) a }.
"""
import math
import sys
import numpy as np

LN2 = math.log(2.0)


def f(rho):
    """KL(rho || 1/2), vectorised, for 0 <= rho <= 1."""
    rho = np.asarray(rho, dtype=float)
    r = np.clip(rho, 1e-300, 1 - 1e-16)
    return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)


def finv(theta):
    """Inverse of f on [0, 1/2] (vectorised bisection; f is decreasing there)."""
    theta = np.asarray(theta, dtype=float)
    lo = np.zeros_like(theta)
    hi = np.full_like(theta, 0.5)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        big = f(mid) > theta          # f(mid) too large -> root is to the right
        lo = np.where(big, mid, lo)
        hi = np.where(big, hi, mid)
    out = 0.5 * (lo + hi)
    out = np.where(theta <= 0, 0.5, out)
    out = np.where(theta >= LN2, 0.0, out)
    return out


class Cube:
    def __init__(self, u):
        self.u = u
        self.pu = 1.0 / (1.0 + math.exp(u))
        self.Lam = math.log(2.0 / (1.0 + math.exp(-u)))
        self.a = float(f(self.pu))
        self.h = float(f(self.Lam / u))
        self.epsstar = math.log(math.cosh(u / 2.0))

    def k(self, rho):
        return f(rho) + self.u * np.asarray(rho) - self.Lam

    def D(self, theta):
        return self.u * finv(theta) - self.Lam

    def x_na(self, theta):
        return self.D(theta) + np.asarray(theta)

    def E(self, theta, phi1, c):
        phi2 = 1.0 - phi1
        return phi1 * self.x_na(c / phi1) + phi2 * self.D((theta - c) / phi2)

    def Xi(self, theta, phi1, ngrid=4001, zooms=4):
        """min over c in [0, min(theta, phi1 a)] of E; grid (clustered at both ends, where E has
        square-root behaviour) followed by repeated local zooms."""
        cmax = min(theta, phi1 * self.a)
        t = np.linspace(0.0, 1.0, ngrid)
        s = 0.5 * (1 - np.cos(math.pi * t))            # clustered at 0 and 1
        cs = cmax * s
        vals = self.E(theta, phi1, cs)
        i = int(np.argmin(vals))
        best, cbest = float(vals[i]), float(cs[i])
        lo, hi = cs[max(i - 1, 0)], cs[min(i + 1, ngrid - 1)]
        for _ in range(zooms):
            if hi <= lo:
                break
            cc = np.linspace(lo, hi, 401)
            vv = self.E(theta, phi1, cc)
            j = int(np.argmin(vv))
            if vv[j] < best:
                best, cbest = float(vv[j]), float(cc[j])
            lo, hi = cc[max(j - 1, 0)], cc[min(j + 1, 400)]
        return best, cbest

    def theta2_of_phi1(self, phi1):
        """sup{theta : Xi(theta,phi1) > 0 and theta < phi2 a}; {Xi > 0} is checked (elsewhere in
        this file, function check_monotone) to be an initial interval in theta."""
        cap = (1.0 - phi1) * self.a
        if self.Xi(cap, phi1)[0] > 0:
            return cap, "cap"
        lo, hi = 1e-13, cap
        for _ in range(48):
            mid = 0.5 * (lo + hi)
            if self.Xi(mid, phi1)[0] > 0:
                lo = mid
            else:
                hi = mid
        return lo, "root"

    def theta2_star(self):
        phis = np.linspace(0.02, 0.98, 97)
        vals = [self.theta2_of_phi1(p)[0] for p in phis]
        i = int(np.argmax(vals))
        lo, hi = phis[max(i - 1, 0)], phis[min(i + 1, len(phis) - 1)]
        best = (vals[i], phis[i])
        for _ in range(4):
            pp = np.linspace(lo, hi, 21)
            vv = [self.theta2_of_phi1(p)[0] for p in pp]
            j = int(np.argmax(vv))
            if vv[j] > best[0]:
                best = (vv[j], pp[j])
            lo, hi = pp[max(j - 1, 0)], pp[min(j + 1, 20)]
        return best

    def check_monotone(self, phi1, n=60):
        """Is theta -> Xi(theta, phi1) decreasing on (0, phi2 a)?  (Used only to justify bisection.)"""
        ths = np.linspace(1e-6, (1 - phi1) * self.a, n)
        xs = np.array([self.Xi(t, phi1, ngrid=1501, zooms=2)[0] for t in ths])
        return bool(np.all(np.diff(xs) < 1e-12)), xs

    # ---- upper bound T2(0), directly from the statement (2-d grid) and by the balance formula
    def T2_direct(self, nrho=3001, nphi=4001):
        a = self.a
        rho = np.linspace(self.pu, 0.5, nrho)            # xi = k(rho), theta_na(xi) = f(rho)
        xi = self.k(rho)
        tna = f(rho)
        phi = np.linspace(1e-5, 1 - 1e-5, nphi)
        P, X = np.meshgrid(phi, xi, indexing="ij")
        _, Tn = np.meshgrid(phi, tna, indexing="ij")
        val = np.maximum(P * a + (1 - P) * Tn, np.minimum(P * a, (1 - P) * X) + (1 - P) * a)
        i, j = np.unravel_index(int(np.argmin(val)), val.shape)
        best = float(val[i, j])
        # local zoom
        plo, phi_ = phi[max(i - 2, 0)], phi[min(i + 2, nphi - 1)]
        rlo, rhi = rho[max(j - 2, 0)], rho[min(j + 2, nrho - 1)]
        for _ in range(3):
            pp = np.linspace(plo, phi_, 801)
            rr = np.linspace(rlo, rhi, 801)
            P, R = np.meshgrid(pp, rr, indexing="ij")
            X = self.k(R)
            Tn = f(R)
            val = np.maximum(P * a + (1 - P) * Tn, np.minimum(P * a, (1 - P) * X) + (1 - P) * a)
            i, j = np.unravel_index(int(np.argmin(val)), val.shape)
            best = min(best, float(val[i, j]))
            pbest, rbest = pp[i], rr[j]
            plo, phi_ = pp[max(i - 3, 0)], pp[min(i + 3, 800)]
            rlo, rhi = rr[max(j - 3, 0)], rr[min(j + 3, 800)]
        return best, float(pbest), float(self.k(rbest))

    def T2_balance(self, nrho=2000001):
        """min over xi of a(a+xi)/(2a+xi-theta_na(xi))  (the two terms balanced in phi)."""
        a = self.a
        rho = np.linspace(self.pu, 0.5, nrho)
        xi = self.k(rho)
        tna = f(rho)
        val = a * (a + xi) / (2 * a + xi - tna)
        i = int(np.argmin(val))
        return float(val[i]), float(xi[i])


# ---------------- small-slope limit, units a = 1 -------------------------------------------
# rho = 1/2 - (u/4) t :  f = t^2 a,  k = (1-t)^2 a,  h = a/4,  theta_na(e) = (1-sqrt e)^2,
# D(theta) = 1 - 2 sqrt(theta),  x_na(theta) = (1 - sqrt(theta))^2.
def gauss_Xi(theta, phi1, ngrid=200001):
    phi2 = 1.0 - phi1
    cmax = min(theta, phi1)
    t = np.linspace(0.0, 1.0, ngrid)
    cs = cmax * 0.5 * (1 - np.cos(math.pi * t))
    vals = 1.0 + cs - 2.0 * np.sqrt(phi1 * cs) - 2.0 * np.sqrt(np.clip(phi2 * (theta - cs), 0.0, None))
    return float(vals.min())


def gauss_theta2_of_phi1(phi1):
    cap = 1.0 - phi1
    if gauss_Xi(cap, phi1) > 0:
        return cap
    lo, hi = 1e-13, cap
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        if gauss_Xi(mid, phi1) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def gauss_theta2_star():
    phis = np.linspace(0.02, 0.98, 97)
    vals = [gauss_theta2_of_phi1(p) for p in phis]
    i = int(np.argmax(vals))
    best = (vals[i], phis[i])
    lo, hi = phis[max(i - 1, 0)], phis[min(i + 1, 96)]
    for _ in range(4):
        pp = np.linspace(lo, hi, 21)
        vv = [gauss_theta2_of_phi1(p) for p in pp]
        j = int(np.argmax(vv))
        if vv[j] > best[0]:
            best = (vv[j], pp[j])
        lo, hi = pp[max(j - 1, 0)], pp[min(j + 1, 20)]
    return best


def gauss_T2():
    xi = np.linspace(1e-9, 1.0, 4000001)
    tna = (1 - np.sqrt(xi)) ** 2
    val = (1 + xi) / (2 + xi - tna)
    i = int(np.argmin(val))
    return float(val[i]), float(xi[i])


def main():
    us = [0.25, 0.5, 1.0, 2.0, 3.0]
    if len(sys.argv) > 1:
        us = [float(x) for x in sys.argv[1:]]
    print("# R4 own computation; exponents of section 11.24")
    print("# small-slope limit (units a = 1; h = 1/4)")
    t2, p1 = gauss_theta2_star()
    T2g, xig = gauss_T2()
    print(f"gauss: theta2*/a = {t2:.6f}  theta2*/h = {t2/0.25:.5f}  best phi1 = {p1:.4f}   "
          f"T2(0)/a = {T2g:.6f} (golden ratio (sqrt5-1)/2 = {(math.sqrt(5)-1)/2:.6f}) at xi/a = {xig:.5f}"
          f" (sqrt(xi/a) = {math.sqrt(xig):.5f})")
    for phi1 in (0.1, 0.3, 0.5, 0.65):
        print(f"   gauss Xi(h, phi1={phi1}) = {gauss_Xi(0.25, phi1):+.5f}")
    print()
    print("#   u      a          h          h/a      theta2*    theta2*/a  theta2*/h  phi1*    "
          "T2(0)dir  T2/a(dir) T2/a(bal) phi_ub  xi_ub     (a+h)/2a")
    sys.stdout.flush()
    for u in us:
        C = Cube(u)
        th2, p1 = C.theta2_star()
        T2, phi, xi = C.T2_direct()
        T2b, xib = C.T2_balance()
        print(f"{u:6.3f} {C.a:.8f} {C.h:.8f} {C.h/C.a:.5f}  {th2:.8f} {th2/C.a:.5f}   {th2/C.h:.5f}   "
              f"{p1:.4f}  {T2:.8f} {T2/C.a:.5f}   {T2b/C.a:.5f}   {phi:.4f}  {xi:.5f}   {(C.a+C.h)/(2*C.a):.5f}")
        sys.stdout.flush()
    print()
    print("# identities used in the proofs:  D(h)=0,  theta_na(h)=h,  a + u p_u = Lambda1")
    for u in us:
        C = Cube(u)
        # theta_na(h): rho with k(rho) = h
        rho = np.linspace(C.pu, 0.5, 2000001)
        j = int(np.argmin(np.abs(C.k(rho) - C.h)))
        print(f"u={u}: D(h)={float(C.D(C.h)):+.2e}  theta_na(h)-h={float(f(rho[j]))-C.h:+.2e}  "
              f"a+u*pu-Lam={C.a+u*C.pu-C.Lam:+.2e}")
    print()
    print("# is theta -> Xi(theta,phi1) decreasing on (0, phi2 a)?  and Xi(h, phi1) > 0 ?")
    for u in us:
        C = Cube(u)
        res = []
        for phi1 in (0.1, 0.3, 0.5, 0.64, 0.8):
            mono, xs = C.check_monotone(phi1)
            xih = C.Xi(C.h, phi1)[0] if C.h < (1 - phi1) * C.a else float("nan")
            res.append(f"phi1={phi1}: decreasing={mono}, Xi(h)={xih:+.5f}")
        print(f"u={u}: " + "; ".join(res))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
