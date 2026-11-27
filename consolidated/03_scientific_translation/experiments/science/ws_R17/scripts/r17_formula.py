#!/usr/bin/env python3
"""R17 replication, item 5(a): the bound of Theorem Q8 / formula (5.2) of the theory division's
Q_REPORT.md, written from the formulas printed in that report ONLY (sections 0, 2.3, 3, 4.1, 4.2,
5.1, 5.2, 5.3, 6.1).  Their code (qlib.py) was NOT read before this file was written; the
ambiguities met are listed in NOTES.md / the report.

Every formula below carries the place of the report it was typed from.

usage: python3 r17_formula.py [table|scan|series|all]
"""
import math
import resource
import sys
import time

LN2 = math.log(2.0)
E_ = math.e


# ----------------------------------------------------------------------------------------------
# constants of the cube (Q_REPORT "Notation", l.57-60)
# ----------------------------------------------------------------------------------------------
def Hbin(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


def KLhalf(x):
    return LN2 - Hbin(x)


class Cube:
    def __init__(self, u):
        self.u = u
        self.p = 1.0 / (1.0 + math.exp(u))               # p_u
        self.Lam1 = math.log(2.0 / (1.0 + math.exp(-u)))  # Lambda_1
        self.eps_star = math.log(math.cosh(u / 2.0))
        self.a = KLhalf(self.p)                          # a = KL(p_u || 1/2)
        self.rho_h = self.Lam1 / u
        self.h = KLhalf(self.rho_h)                      # h = KL(rho_h || 1/2)
        self.Hp = Hbin(self.p)
        a, h = self.a, self.h
        # Theorem Q (l.72-74), (R) (l.188-192), Theorem Q(b) (l.91)
        self.kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
        self.c1 = h * (1 + self.kappa) / self.kappa
        self.c2 = (a + h) * (2 * a - h) / (h * a) - 2
        self.rbar = (2 * a - h) / (a - h)
        self.Cstar = 2 * math.sqrt((1 + self.rbar) * self.c1 * (a / h + 4))

    def epochs(self, M):
        """d_m, J_m, k_m, B_m, R_m, phi_m for m = 0..M (Theorem Q l.72-74; section 5.1 l.520)."""
        a, h = self.a, self.h
        d = [h / (a - h)]
        J, k, B, R, phi = [], [1], [], [], []
        for m in range(M + 1):
            Jm = math.ceil(d[m])
            J.append(Jm)
            B.append(h * (1 + 1 / d[m]))
            R.append(h / Jm)
            phi.append(h / (Jm * a + h))
            d.append(d[m] * (Jm * a + h) / (Jm * a - h * d[m]))
            k.append(k[m] + Jm + 1)
        return d, J, k, B, R, phi


# ----------------------------------------------------------------------------------------------
# error terms
# ----------------------------------------------------------------------------------------------
def w_of_c(c):
    """section 4.2, l.457"""
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c) + c


def A_n(C, n):
    """section 4 definition, l.377"""
    return (2 * C.u + LN2) * n + 3


def c_log(C, n):
    """l.377"""
    return math.log(n + 1) + math.log(6) + 2 * C.u + math.exp(C.u)


def m_star(C, ell):
    """Lemma Q3, l.250"""
    return ((math.sqrt(ell / 2) + math.sqrt(ell / 2 + 2 * C.p)) / C.p) ** 2


def cpi_bar_parts(C, m, ell):
    """Lemma Q3, l.252: the two entries of the maximum."""
    e1 = LN2 + m_star(C, ell) * C.Hp
    e2 = C.u * (1 + math.sqrt(m * ell / 2)) + (4 / (3 * C.p)) * (ell + 2) + math.log(m + 1)
    return e1, e2


def cpi_bar(C, m, ell):
    return max(cpi_bar_parts(C, m, ell))


# --- slope step, Proposition Q6, l.398-401 ---
def mbar_S(C, n):
    return n + 2 + math.log2(12 * E_ * (E_ - 1) * A_n(C, n))


def Kbar_S(C, n, Lam):
    return 18 * (Lam + math.log(2 * A_n(C, n) * mbar_S(C, n) * (n + 3))) + 1


def c_S(C, n, Lam, B):
    return ((1 + c_log(C, n) + C.h) * B / C.h + 1 + 2 * math.log(A_n(C, n))
            + math.log(18 * E_ * (E_ - 1)) + math.log(Kbar_S(C, n, Lam)) + math.log(n + 3))


def q_S(C, n, Lam):
    return (math.log(4 * (n + 1)) + math.log(A_n(C, n)) + math.log(24 * E_ * (E_ - 1))
            + math.log(Kbar_S(C, n, Lam)))


# --- drop, Proposition Q7, l.457-459, 473-477 ---
def ell_c(C, c):
    return LN2 + 3 * C.u + 2.25 * c + math.log(1 / c)


def nD_prime(C, c):
    return max(2 / C.u + 2, math.log(6 / (5 * c)) / math.log((1 + math.exp(C.u)) / 2))


def nubar_D(C, n, c):
    return (1.8 * A_n(C, n) + 3 * math.exp(C.u) * n) / c


def mbar_D(C, n, c):
    return n + 2 + math.log2(5.6 * nubar_D(C, n, c))


def Kbar_D(C, n, Lam, c):
    return 4 / c ** 2 * (Lam + math.log(2 * (A_n(C, n) / c) * mbar_D(C, n, c) * (n + 4))) + 1


def Pbar_cnt(C, n, Lam, c):
    return (math.log(A_n(C, n) / c) + math.log(7.45) + math.log(nubar_D(C, n, c))
            + math.log(Kbar_D(C, n, Lam, c)))


def Pbar_M(C, n, Lam, c):
    return math.log(11.17) + math.log(nubar_D(C, n, c)) + math.log(Kbar_D(C, n, Lam, c))


def c_D(C, n, Lam, B, R, phi, c):
    """l.474; B*sigma(n) = cpi_bar(floor(phi n); ell_c) * B/(a+R)."""
    cp = cpi_bar(C, math.floor(phi * n), ell_c(C, c))
    return (B * (1 + phi * nD_prime(C, c)) + B * cp / (C.a + R) + math.log(n + 4) + 1
            + Pbar_cnt(C, n, Lam, c))


def c_D_sqrt_part(C, n, B, R, phi, c):
    """the leading sqrt term u*sqrt(phi n ell_c/2)*B'/a of c_D (l.480, l.586), B' = B a/(a+R)."""
    return C.u * math.sqrt(phi * n * ell_c(C, c) / 2) * B / (C.a + R)


def q_D(C, n, Lam, c):
    return math.log(4 * (n + 2)) + Pbar_M(C, n, Lam, c)


# --- base, Proposition Q5(a), l.329-331 ---
def eta_x(x):
    return min(0.5, math.tanh(x / 4))


def ell0_x(C, x):
    v = math.log(2 * math.exp(3 * C.u + min(x / 2, math.log(3))) / math.expm1(x / 2))   # expm1: v1 had exp(x/2) - 1 (0 for x < 1e-15)
    return max(v, 0.0)


def Kbar_0(x, Lam):
    e = eta_x(x)
    return 3 * (1 + e) / e ** 2 * (math.log(4) + Lam) + 1


def E_base(C, d, x, Lam):
    l0 = ell0_x(C, x)
    return math.log(8 * Kbar_0(x, Lam)) + max(
        m_star(C, l0) * C.Hp,
        C.u * (1 + math.sqrt(d * l0 / 2)) + (4 / (3 * C.p)) * (l0 + 2) + math.log(d + 1))


# ----------------------------------------------------------------------------------------------
# the schedule (section 5.1) and formula (5.2)
# ----------------------------------------------------------------------------------------------
def accuracies(eps, M):
    """eps_hat, c_m (m < M), alpha_m (m = 0..M); l.521-523."""
    eh = min(eps, 1.0)
    c = [eh / (13.0 * (m + 1) * (m + 2)) for m in range(M)]
    alpha = [0.0] * (M + 1)
    alpha[M] = eh
    for m in range(M - 1, -1, -1):
        alpha[m] = alpha[m + 1] - w_of_c(c[m])
    return eh, c, alpha


def E_total(C, n, eps, ln_inv_delta, M, ep=None, detail=False):
    """formula (5.2), l.547-555: levels numbered from the top; level 0 is the drop that ends epoch
    M-1, then the J_{M-1} slope steps of that epoch, then the drop of epoch M-2, ..., down to the
    J_0 slope steps of epoch 0; Lam_0 = ln(1/delta) + n ln 2, Lam_{t+1} = Lam_t + q_t(n, Lam_t)."""
    if ep is None:
        ep = C.epochs(M)
    d, J, k, B, R, phi = ep
    eh, c, alpha = accuracies(eps, M)
    Lam = ln_inv_delta + n * LN2
    Lam0 = Lam
    s_slope = 0.0
    s_drop = 0.0
    s_drop_sqrt = 0.0
    s_drop_shift = 0.0
    nslope = 0
    for m in range(M - 1, -1, -1):
        # the drop that ends epoch m
        s_drop += c_D(C, n, Lam, B[m], R[m], phi[m], c[m])
        s_drop_sqrt += c_D_sqrt_part(C, n, B[m], R[m], phi[m], c[m])
        s_drop_shift += B[m] * cpi_bar(C, math.floor(phi[m] * n), ell_c(C, c[m])) / (C.a + R[m])
        Lam += q_D(C, n, Lam, c[m])
        # the J_m slope steps of epoch m
        for _ in range(J[m]):
            s_slope += c_S(C, n, Lam, B[m])
            Lam += q_S(C, n, Lam)
            nslope += 1
    base = E_base(C, n, alpha[0], Lam)
    tot = base + s_slope + s_drop
    if detail:
        return dict(E=tot, base=base, slope=s_slope, nslope=nslope, drop=s_drop,
                    drop_sqrt=s_drop_sqrt, drop_shift=s_drop_shift, LamT=Lam, Lam0=Lam0, alpha0=alpha[0], T=k[M] - 1)
    return tot


def best_M(C, n, eps, ln_inv_delta, Mcap=60):
    """minimise n B_M + E_M over M >= 0.  Stop rule (v2; v1 used 3 nats per level and was too slow for a scan):
    bound_M - n h >= E_M >= (number of slope steps) * c_S(n, Lam_0; h), because B_m >= h and Lam_t >= Lam_0 and
    c_S is nondecreasing in Lam and B; the number of slope steps k_M - 1 - M increases with M; so once
    (k_M - 1 - M) * c_S(n, Lam_0; h) exceeds the best excess found, no larger M can be better."""
    ep = C.epochs(Mcap)
    d, J, k, B, R, phi = ep
    best = None
    rows = []
    cmin = c_S(C, n, ln_inv_delta + n * LN2, C.h)
    for M in range(Mcap + 1):
        if best is not None and (k[M] - 1 - M) * cmin > best[1] - n * C.h:
            break
        Etot = E_total(C, n, eps, ln_inv_delta, M, ep=ep)
        bound = n * B[M] + Etot
        rows.append((M, k[M], bound))
        if best is None or bound < best[1]:
            best = (M, bound, Etot)
    return best, rows, ep


def C1_series(C, eps, M):
    """C_1 of Proposition Q9a, l.586: u*[sqrt(ell0_{alpha_0}/2) + sum_{m<M} sqrt(phi_m ell_{c_m}/2) B_{m+1}/a]."""
    d, J, k, B, R, phi = C.epochs(M + 1)
    eh, c, alpha = accuracies(eps, M)
    base = C.u * math.sqrt(ell0_x(C, alpha[0]) / 2)
    drops = C.u * sum(math.sqrt(phi[m] * ell_c(C, c[m]) / 2) * B[m + 1] / C.a for m in range(M))
    return base, drops, alpha[0]


# ----------------------------------------------------------------------------------------------
def part_constants():
    print("== constants (report: h/a = 0.2626 at u=1; C_* = 4.65, 8.64, 13.5 at u = 1/2, 1, 2; c1 = 6.4a,")
    print("   1+kappa = 1.043, a/(a-h) = 1.36 at u = 1) ==")
    for u in (0.5, 1.0, 2.0, 4.0):
        C = Cube(u)
        print("u=%-4g p_u=%.6f a=%.6f h=%.6f h/a=%.6f rho_h=%.6f eps*=%.6f kappa=%.6f c1/a=%.4f c2=%.4f "
              "rbar=%.4f a/(a-h)=%.4f C_*=%.4f" % (u, C.p, C.a, C.h, C.h / C.a, C.rho_h, C.eps_star,
                                                     C.kappa, C.c1 / C.a, C.c2, C.rbar, C.a / (C.a - C.h),
                                                     C.Cstar))


def part_epochs():
    print("\n== epoch table at u = 1 (report section 5.1, l.533-539) ==")
    C = Cube(1.0)
    d, J, k, B, R, phi = C.epochs(44)
    print("  m      d_m        J_m     k_m    B_m/a      phi_m     (B_m-h)*(k_m+c2)/c1  d_{m+1}/d_m")
    for m in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 44):
        print("%3d %12.4f %8d %8d %9.5f %10.6f %12.4f %12.4f" % (
            m, d[m], J[m], k[m], B[m] / C.a, phi[m], (B[m] - C.h) * (k[m] + C.c2) / C.c1, d[m + 1] / d[m]))
    print("\n== the relations of (R) and of Proposition Q9a / Theorem Q9, 300 epochs, five slopes ==")
    for u in (0.1, 0.5, 1.0, 2.0, 5.0):
        C = Cube(u)
        Mx = 300
        d, J, k, B, R, phi = C.epochs(Mx)
        worst = dict(rate=-1e300, gain=1e300, phi=-1e300, ratio=-1e300, kjump=-1e300, Brec=0.0, Jd=True)
        for m in range(Mx):
            worst['rate'] = max(worst['rate'], (B[m] - C.h) - C.c1 / (k[m] + C.c2))          # <= 0
            worst['gain'] = min(worst['gain'], (d[m + 1] + 1) - (d[m] + 1) * (1 + C.kappa))  # >= 0
            worst['phi'] = max(worst['phi'], phi[m] * C.rbar * (1 + C.kappa) ** m)           # <= 1
            worst['ratio'] = max(worst['ratio'], d[m + 1] / d[m] - C.rbar)                   # <= 0
            worst['kjump'] = max(worst['kjump'], k[m + 1] / k[m] - (1 + C.rbar))             # < 0
            worst['Brec'] = max(worst['Brec'], abs(B[m + 1] - B[m] * J[m] * C.a / (J[m] * C.a + C.h)) / B[m])
            if d[m] < 2.0 ** 50:   # beyond 2^53 a float cannot tell d from d + 1 (v1 of this script reported False for that reason)
                worst['Jd'] = worst['Jd'] and (d[m] <= J[m] < d[m] + 1) and (J[m] * C.a - C.h * d[m] > 0)
                worst['nJd'] = worst.get('nJd', 0) + 1
        print("u=%-4g max[(B_m-h) - c1/(k_m+c2)]=%.3e  min[d_{m+1}+1-(d_m+1)(1+kappa)]=%.3e  "
              "max[phi_m rbar (1+kappa)^m]=%.4f  max[d_{m+1}/d_m - rbar]=%.3e  max[k_{m+1}/k_m-(1+rbar)]=%.3e  "
              "max rel err B-recursion=%.1e  d<=J<d+1 & Ja-hd>0 (the %d epochs with d_m < 2^50): %s  last d_{m+1}/d_m=%.5f (a/(a-h)=%.5f)"
              % (u, worst['rate'], worst['gain'], worst['phi'], worst['ratio'], worst['kjump'],
                 worst['Brec'], worst.get('nJd', 0), worst['Jd'], d[Mx] / d[Mx - 1], C.a / (C.a - C.h)))


def part_series():
    print("\n== C_1 (Proposition Q9a; report: 1.6 + 3.9 = 5.5 at u=1, eps=1, 44 epochs; referee: base 1.597,")
    print("   drops 2.34, 3.47, 3.931, 3.936, 3.936 after 5, 13, 44, 120, 400 epochs; eps=0.1: 6.31; u=1/2: 2.43; u=2: 11.87) ==")
    for (u, eps) in ((1.0, 1.0), (1.0, 0.1), (0.5, 1.0), (2.0, 1.0)):
        C = Cube(u)
        out = []
        for M in (5, 13, 44, 120, 400):
            b, dr, a0 = C1_series(C, eps, M)
            out.append("M=%d: base %.4f drops %.4f sum %.4f (alpha_0=%.4f)" % (M, b, dr, b + dr, a0))
        print("u=%g eps=%g: " % (u, eps) + "; ".join(out))
    # the crude geometric majorant of Prop Q9a (drops part), u = 1, eps = 1
    C = Cube(1.0)
    lbar = LN2 + 3 * C.u + 0.1 + math.log(13.0)
    crude = C.u * C.rbar ** -0.5 * sum((1 + C.kappa) ** (-m / 2) * math.sqrt((lbar + 2 * math.log(m + 2)) / 2)
                                         for m in range(20000))
    print("crude geometric majorant of the drops part (u=1, eps=1; referee: 81): %.2f" % crude)


def part_table(u=1.0, eps=1.0, delta=0.05):
    C = Cube(u)
    lid = math.log(1 / delta)
    print("\n== the bound of Theorem Q8 at u=%g, eps=%g, delta=%g, best M (report section 7.4) ==" % (u, eps, delta))
    print("targets (report): n=6.4e4: 0.707 (M=5, 13 levels); 1e6: 0.371 (M=10, 43); 1e8: 0.2731 (M=17, 268); "
          "1e10: 0.2637 (M=25, 2868)")
    print("        n   bestM   k_M   bound/(na)   B_M/a   (bound-nh)/sqrt(n ln n)  (bound-nh)/n^0.75   "
          "E_M = base + nslope x mean c_S + drops(sqrt part + rest)   Lam_T/Lam_0  alpha_0")
    for n in (1e3, 1e4, 1.6e4, 3.2e4, 6.4e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e12):
        n = int(n)
        best, rows, ep = best_M(C, n, eps, lid)
        M, bound, Etot = best
        det = E_total(C, n, eps, lid, M, ep=ep, detail=True)
        d, J, k, B, R, phi = ep
        per = det['slope'] / det['nslope'] if det['nslope'] else float('nan')
        print("%9.3g %6d %6d %11.4f %8.4f %14.3f %18.4f      %.0f = %.0f + %d x %.0f + (%.0f + %.0f) [shift reading: (%.0f + %.0f)]   %8.3f  %.4f"
              % (n, M, k[M], bound / (n * C.a), B[M] / C.a, (bound - n * C.h) / math.sqrt(n * math.log(n)),
                 (bound - n * C.h) / n ** 0.75, det['E'], det['base'], det['nslope'], per,
                 det['drop_sqrt'], det['drop'] - det['drop_sqrt'], det['drop_shift'], det['drop'] - det['drop_shift'],
                 det['LamT'] / det['Lam0'], det['alpha0']))
    return C


def part_scan(u=1.0, eps=1.0, delta=0.05, per_decade=40):
    C = Cube(u)
    lid = math.log(1 / delta)
    print("\n== scan of (bound - nh)/sqrt(n ln n), u=%g eps=%g delta=%g, %d sizes per decade, 1.6e4 <= n <= 1e12 =="
          % (u, eps, delta, per_decade))
    print("   (report: 'between 2.4 and 3.8'; referee O1: sup 3.77 at n = 16 788 (M=2), 2.41 at 1e12; crossover with n*a at 2.07e4)")
    lo = (1e300, None)
    hi = (-1e300, None)
    cross = None
    last_not_below = None
    x = math.log10(1.6e4)
    xs = []
    while x <= 12.0 + 1e-9:
        xs.append(x)
        x += 1.0 / per_decade
    # also the decade below, for the crossover with n a
    xs2 = [4.0 + i / 200.0 for i in range(0, 121)]
    for x in xs:
        n = int(round(10 ** x))
        best, rows, ep = best_M(C, n, eps, lid)
        r = (best[1] - n * C.h) / math.sqrt(n * math.log(n))
        if r < lo[0]:
            lo = (r, n, best[0])
        if r > hi[0]:
            hi = (r, n, best[0])
    for x in xs2:
        n = int(round(10 ** x))
        best, rows, ep = best_M(C, n, eps, lid)
        if best[1] >= n * C.a:
            last_not_below = n
    print("min ratio %.4f at n=%d (M=%d); max ratio %.4f at n=%d (M=%d)" % (lo[0], lo[1], lo[2], hi[0], hi[1], hi[2]))
    print("crossover with n*a on the grid 10^(4 + i/200): last n with bound >= n a: %s" % last_not_below)


def part_variants():
    print("\n== other parameters (report section 7.4 (iv)): eps = 0.1: 0.741, 0.379, 0.2738; delta = e^-n: 0.7088, 0.3717, 0.2731;")
    print("   u = 1/2: 1.029, 0.444, 0.2717; u = 2: 0.561, 0.363, 0.3036 at n = 6.4e4, 1e6, 1e8 ==")
    for (u, eps, dl) in ((1.0, 0.1, 'p05'), (1.0, 1.0, 'en'), (0.5, 1.0, 'p05'), (2.0, 1.0, 'p05')):
        C = Cube(u)
        out = []
        for n in (64000, 10 ** 6, 10 ** 8):
            lid = math.log(20.0) if dl == 'p05' else float(n)
            best, rows, ep = best_M(C, n, eps, lid)
            out.append("%.4f (M=%d)" % (best[1] / (n * C.a), best[0]))
        print("u=%g eps=%g delta=%s: %s" % (u, eps, '0.05' if dl == 'p05' else 'e^-n', ", ".join(out)))


def part_closed_form(u=1.0, eps=1.0, delta=0.05):
    """Proposition Q9a / Theorem Q9(b), l.582-591 and l.626, 636: with k_dag = sqrt((1+rbar) c1 n / l_S),
    M = max{m: k_m <= k_dag}; l_S = c_S(n, 2 Lam_0; a); l_D = max_m [c_D(n, 2Lam_0) - sqrt part];
    l_B = E_base(n, alpha_0; 2Lam_0) - u sqrt(n ell0/2)."""
    C = Cube(u)
    print("\n== closed form of Theorem Q9(b) with the M of its proof (referee m4: 1.813, 0.663, 0.3055, 0.2673 with M = 9, 14, 21, 29) ==")
    for n in (64000, 10 ** 6, 10 ** 8, 10 ** 10):
        Lam0 = math.log(1 / delta) + n * LN2
        lS = c_S(C, n, 2 * Lam0, C.a)
        kd = math.sqrt((1 + C.rbar) * C.c1 * n / lS)
        d, J, k, B, R, phi = C.epochs(80)
        M = max(m for m in range(80) if k[m] <= kd)
        eh, c, alpha = accuracies(eps, M)
        lD = max([c_D(C, n, 2 * Lam0, B[m], R[m], phi[m], c[m]) - c_D_sqrt_part(C, n, B[m], R[m], phi[m], c[m])
                  for m in range(M)] or [0.0])
        lB = E_base(C, n, alpha[0], 2 * Lam0) - C.u * math.sqrt(n * ell0_x(C, alpha[0]) / 2)
        b, dr, a0 = C1_series(C, eps, M)
        val = n * C.h + 2 * math.sqrt((1 + C.rbar) * C.c1 * n * lS) + (b + dr) * math.sqrt(n) + M * lD + lB
        # hypothesis T q* <= Lam_0 of Prop Q9a
        qstar = max([q_S(C, n, 2 * Lam0)] + [q_D(C, n, 2 * Lam0, c[m]) for m in range(M)])
        print("n=%.3g: l_S=%.2f ((a/h+4) ln n = %.2f; difference %.2f)  k_dag=%.1f  M=%d k_M=%d  l_D=%.1f l_B=%.1f C1=%.3f  "
              "closed form/(na)=%.4f   T q*/Lam_0 = %.4f (q*=%.1f)"
              % (n, lS, (C.a / C.h + 4) * math.log(n), lS - (C.a / C.h + 4) * math.log(n), kd, M, k[M], lD, lB,
                 b + dr, val / (n * C.a), (k[M] - 1) * qstar / Lam0, qstar))


if __name__ == "__main__":
    t0 = time.time()
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "table"):
        part_constants()
        part_epochs()
        part_table()
        part_variants()
        part_closed_form()
    if what in ("all", "series"):
        part_series()
    if what in ("all", "scan"):
        part_scan()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("LAST LINE r17_formula.py %s: completed; wall %.1f s; peak RSS %.1f MB" % (what, time.time() - t0, rss))
