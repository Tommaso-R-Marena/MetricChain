"""Workstream K, numerical check (iii): the closure window.

For the n-cube (the OUTER block of the two-level algorithm) and slope u:
  Gt(r) = E_r/|B(r-1)|  -- the ratio that the closure test of Theorem 11.52 needs to be O(1) when the lower end is the
                           layer-cake bound only (sketch, step (2));
  G2(r) = E_r/T(kappa(r)) -- the ratio that appears when the lower end also contains the Harper lower bound
                           (two-sided tail lemma 11.43(c));  kappa(r) = largest k with |B(k)| <= max(1, c|B(r-1)|).
Checked:
 (a) Gt(r) <= 2 e^u n for 0 <= r <= p_u (n+1)                               [Lemma K.4(a)]
 (b) min_r Gt(r) -> 4 e^u (e^u - 1), attained near rho = 1/(2e^u + 1)        [the "window" of the sketch is centred there]
 (c) Gt(floor(p_u n)) grows like sqrt(n): the one-sided ratio is NOT bounded up to p_u n
 (d) G2(r) <= 2 e^{u(m0+2)} P(Bin(n,p_u) <= r) for 1 <= r <= p_u n           [Lemma K.4(b)],  m0 = ceil(ln((1+eta)/(1-eta))/u)
 (e) the window {r : Gt(r) <= e^{G-b}/4} of the sketch for G - b = 2,4,6,8 and the exponent KL(rho_+||1/2) it would give
 (f) r_dagger of Theorem K1 in the bounded regime (theta, eta, eta' constants) against r_+ = floor(p_u n - sqrt((n/2) ln(2 e^{u(m0+2)}/theta)))
     and the exponent n^{-1} ln(2^n/|B(r_dagger)|) against a.
"""
import math, sys
import numpy as np
from klib import Cube, consts, kl, rdagger

def run(out):
    ok = True
    for u in (0.5, 1.0, 2.0):
        pu, lam, estar, a, h = consts(u)
        out(f"\n=== u = {u}: p_u = {pu:.4f}, a = {a:.5f}, h = {h:.5f}, 4e^u(e^u-1) = {4*math.exp(u)*math.expm1(u):.4f}, rho_min = 1/(2e^u+1) = {1/(2*math.exp(u)+1):.4f}")
        out(f"{'n':>6} | {'max Gt/(2e^u n)':>15} | {'min Gt':>8} | {'argmin/n':>8} | {'Gt(p_u n)/sqrt n':>16} | {'max G2/bound':>12} | r_dag  r_+   (ln(2^n/|B(r_dag)|) / n) / a | (same - a) sqrt(n)/u")
        for n in (50, 100, 200, 400, 800, 1600, 3200, 6400, 12800):
            c = Cube(n, u)
            rmax = int(math.floor(pu * (n + 1)))
            # (a)
            ma = float(np.max(c.lGt[: rmax + 1])) - math.log(2 * math.exp(u) * n)
            if ma > 1e-9: ok = False
            # (b)
            i = int(np.argmin(c.lGt[1:])) + 1
            mn = math.exp(c.lGt[i])
            # (c)
            gp = math.exp(c.lGt[int(pu * n)]) / math.sqrt(n)
            # (d)
            eta = 0.25
            m0 = math.ceil(math.log((1 + eta) / (1 - eta)) / u)
            lower, upper = c.log_binom_cdf(pu)
            worst = -math.inf
            for r in range(1, int(math.floor(pu * n)) + 1):
                bound = math.log(2) + u * (m0 + 2) + lower[r]
                worst = max(worst, c.lG2(r, eta) - bound)
                if c.kappa(r, eta) < max(0, r - 1 - m0): ok = False; out(f"   kappa(r) < r-1-m0 at n={n} r={r}")
            if worst > 1e-9: ok = False
            # (f) bounded regime: theta = eta' = 0.1, lambda = 0.25, b = 1, J from n_total = 2 n (phi = 1/2)
            theta, etap, lamb, b = 0.1, 0.1, 0.25, 1.0
            J = math.ceil((2 * u * 2 * n + b + n * math.log(2)) / lamb)
            nu0 = max((J + 1) * math.expm1(lamb) / etap, 2 * math.exp(u) * n / theta) / (1 - eta)
            rd = rdagger(c, eta, theta, nu0)
            rplus = math.floor(pu * n - math.sqrt(n / 2 * math.log(2 * math.exp(u * (m0 + 2)) / theta)))
            if rd < rplus: ok = False
            ex = (n * math.log(2) - c.lball_r(rd)) / n if rd >= 0 else float('nan')
            out(f"{n:6d} | {math.exp(ma):15.4f} | {mn:8.4f} | {i/n:8.4f} | {gp:16.4f} | {math.exp(worst):12.4f} | {rd:5d} {rplus:5d}   {ex/a:10.4f}                 | {(ex-a)*math.sqrt(n)/u:8.3f}")
        # (e) the window of the sketch: {r : Gt(r) <= e^{G-b}/4}.  Limit n -> infinity at fixed rho < p_u:
        #     Gt -> (e^u - 1)/(y (1 - y e^u)),  y = rho/(1-rho);  so the limit window is z_- <= y e^u <= z_+,
        #     z_+- = (1 +- sqrt(1 - 4 c))/2,  c = 4 e^u (e^u - 1) e^{-(G-b)}  (empty if c > 1/4), and its upper end is BELOW p_u.
        out(f"  window of the sketch, radii with Gt(r) <= e^(G-b)/4:   limit window (n -> infinity)   |   n = 6400   |   n = 100000")
        cubes = {nn: Cube(nn, u) for nn in (6400, 100000)}
        for Gb in (2.0, 4.0, 6.0, 8.0, 10.0, 12.0):
            cc = 4 * math.exp(u) * math.expm1(u) * math.exp(-Gb)
            if cc > 0.25:
                lim = "empty (needs G-b >= ln(16 e^u (e^u-1)) = %.2f)" % math.log(16 * math.exp(u) * math.expm1(u))
            else:
                zs = [(1 - math.sqrt(1 - 4 * cc)) / 2, (1 + math.sqrt(1 - 4 * cc)) / 2]
                rhos = [z * math.exp(-u) / (1 + z * math.exp(-u)) for z in zs]
                lim = f"rho in [{rhos[0]:.4f}, {rhos[1]:.4f}], KL(rho_+||1/2)/a = {kl(rhos[1], 0.5) / a:.4f}"
            cells = []
            for nn, c in cubes.items():
                okr = np.nonzero(c.lGt[1:nn] <= Gb - math.log(4))[0] + 1
                if len(okr) == 0:
                    cells.append("empty")
                else:
                    lo, hi = int(okr[0]), int(okr[-1])
                    if len(okr) != hi - lo + 1: ok = False; out("   window not an interval")
                    cells.append(f"[{lo / nn:.4f}, {hi / nn:.4f}], KL(rho_+)/a = {kl(hi / nn, 0.5) / a:.4f}")
            out(f"   G-b = {Gb:4.1f}: {lim:62s} | {cells[0]:42s} | {cells[1]}")
    out(f"\nall inequalities (a), (d), kappa >= r-1-m0, r_dagger >= r_+ hold: {ok}")
    return ok

if __name__ == "__main__":
    lines = []
    def out(s):
        print(s); lines.append(s)
    ok = run(out)
    open("out_closure_window.txt", "w").write("\n".join(lines) + "\n")
    sys.exit(0 if ok else 1)
