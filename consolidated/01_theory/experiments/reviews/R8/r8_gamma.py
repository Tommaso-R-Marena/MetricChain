#!/usr/bin/env python3
"""Referee R8 -- side claims of sections 5(2) and 6.3 of the report about the one-sided ratio Gamma~ and the
two-sided ratio Gamma'' (own tables, floating point): min_r Gamma~(r) -> 4e^u(e^u-1); Gamma~(floor(p_u n))/sqrt(n);
r_dagger against r_+ and ln(2^n/|B(n,r_dagger)|)/(n a) (the O(sqrt n) correction of the outer sample);
the limit window of the sketch: KL(rho_+||1/2)/a for G-b = 6, 8, 10 at u = 1."""
import math, numpy as np
from r8_flat import tabF
for u in (0.5, 1.0, 2.0):
    pu = 1 / (1 + math.exp(u)); a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    for n in (800, 12800, 100000):
        t = tabF(n, u)
        lGt = np.concatenate(([math.log(math.expm1(u))], t.lE[1:] - t.lB[:-1]))
        rmin = 1 + int(np.argmin(lGt[1:]))       # minimum over r >= 1 (Gt(0) = e^u - 1 is smaller, by convention)
        eta = 0.25
        lceta = math.log((1 - eta) / (1 + eta))
        kap = t.kappa_all(lceta)
        lGpp = t.lE - t.lT[kap]
        theta = 0.1
        m0 = math.ceil(math.log((1 + eta) / (1 - eta)) / u)
        nu0 = 2 * math.exp(u) * n / (theta * (1 - eta))
        ok = (lGt <= math.log(theta * (1 - eta) * nu0)) & (np.minimum(lGt - lceta, lGpp) <= math.log(theta))
        bad = np.nonzero(~ok[:n])[0]
        rdag = int(bad[0]) - 1 if bad.size else n - 1
        rplus = math.floor(pu * n - math.sqrt(n / 2 * math.log(2 * math.exp(u * (m0 + 2)) / theta)))
        print("u=%.1f n=%6d: Gt(0) = e^u - 1 = %.3f; min_{r>=1} Gt = %.3f at rho=%.4f (4e^u(e^u-1) = %.3f, 1/(2e^u+1) = %.4f); "
              "Gt(floor(p_u n))/sqrt(n) = %.3f; "
              "max_{r<=p_u(n+1)} Gt/(2e^u n) = %.3f; eta=1/4, theta=0.1: r_dag=%d >= r_+=%d (p_u n = %.0f); ln(2^n/|B(r_dag)|)/(n a) = %.3f"
              % (u, n, math.expm1(u), math.exp(lGt[rmin]), rmin / n, 4 * math.exp(u) * (math.exp(u) - 1), 1 / (2 * math.exp(u) + 1),
                 math.exp(lGt[int(pu * n)]) / math.sqrt(n), math.exp(float(np.max(lGt[:int(pu * (n + 1)) + 1]))) / (2 * math.exp(u) * n),
                 rdag, rplus, pu * n, (n * math.log(2) - t.lB[rdag]) / (n * a)))
u = 1.0; pu = 1 / (1 + math.e); a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
for Gb in (6, 8, 10):
    c = 4 * (math.e - 1) / math.exp(Gb)          # y(1 - y e^u) = 4(e^u-1) e^{-(G-b)}
    y = (1 + math.sqrt(1 - 4 * math.e * c)) / (2 * math.e)
    rho = y / (1 + y)
    kl = math.log(2) + rho * math.log(rho) + (1 - rho) * math.log(1 - rho)
    print("limit window of the sketch, u=1, G-b=%d: rho_+ = %.5f < p_u = %.5f, KL(rho_+||1/2)/a = %.4f" % (Gb, rho, pu, kl / a))
print("window empty unless G-b >= ln(16 e^u (e^u-1)):", [round(math.log(16 * math.exp(u) * (math.exp(u) - 1)), 2) for u in (0.5, 1.0, 2.0)])
