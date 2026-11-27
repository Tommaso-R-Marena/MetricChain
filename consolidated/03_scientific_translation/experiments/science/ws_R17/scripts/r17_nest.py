#!/usr/bin/env python3
"""R17 replication, item 5(b): the exact certified cost of the nested design G_M(n, eps, delta) of the theory
division's Q_REPORT.md (sections 3, 4.1, 4.2, 5.1), evaluated level by level with the exact constants of
Theorem 11.56, with OUR code: the level constants and the base bracket come from the science division's
r16lib.py (workstream R16: written from the statements of Theorem 11.56 / Proposition K0), the families
S[.] and D[.] are written here from the text of Q_REPORT sections 4.1, 4.2, 5.1.  The theory division's
qscheme.py / qlib.py were NOT read before this file was written.

Variants:
  'min'   -- section 4 of the report: S[F](n,x,delta) = F(n,x,delta) if xhat < X0(n), else the cheaper of the
             level as built and F(n,x,delta);  D[F;c,alpha] = the cheapest of the level with shift (if defined),
             the level without shift (if n >= n_D'(c) and floor(phi n) >= 1) and F(n, alpha, delta).
  'proof' -- my reading of "every level is the level as built and nothing else" (report section 7.3):
             S: the level as built whenever xhat >= X0(n), else pass-through;  D: the level with shift whenever
             it is defined, else pass-through.

At every node the induction inequality  cost <= d B - sigma min(x, R d) + E(d, x; ln(1/delta) + d ln 2)  of the
family it belongs to is checked (E from r17_formula.py, i.e. from the report's formulas), and at every level
built: the certified accuracy, Lemma Q4 / Lemma Q3, (4.1) / (4.2), the bound of Proposition Q6 / Q7.

usage: python3 r17_nest.py <n> <M> [eps] [delta] [u]
"""
import math
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ws_R16"))     # the science division's own R16 library
import numpy as np            # noqa: E402
import r16lib as R            # noqa: E402
import r17_formula as F       # noqa: E402

LN2 = math.log(2.0)
INF = float("inf")
TOL = 1e-9

stats = dict(nodes=0, viol=0, min_slack_ind=INF, min_slack_Q4=INF, min_slack_Q3=INF, min_slack_Q6=INF,
             min_slack_Q7=INF, S_built=0, D_shift=0, D_noshift=0, base=0, max_xout_err=0.0,
             min_slack_41=INF, min_slack_42=INF, min_slack_base=INF, min_base_lid=INF, max_base_lid=0.0,
             base_enum=0, min_base_d=INF, max_lid_over_d=0.0, min_slack_nonbase=INF, min_slack_sampled=INF,
             n_sampled=0)
viol_log = []


def violation(msg):
    stats['viol'] += 1
    if len(viol_log) < 20:
        viol_log.append(msg)


# ----------------------------------------------------------------------------------------------------------
# base bracket: Proposition K0 as in r16lib.k0, with the prefix maximum of ln(1 + Gamma'') cached per (d, eta)
# (same definition; r16lib.k0 recomputes the array at every call).  Cross-checked against r16lib.k0 below.
# ----------------------------------------------------------------------------------------------------------
_pm = {}


def base_cost(u, d, x, ld):
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ld))
    budget = x - math.log((1 + eta) / (1 - eta))
    key = (d, eta)
    if key not in _pm:
        t = R.tab(d, u)
        lg = t.lGpp(math.log((1 - eta) / (1 + eta)))[:d]
        _pm[key] = np.maximum.accumulate(np.logaddexp(0.0, lg))
    pm = _pm[key]
    # r* = the largest radius <= d-1 with ln(1+Gamma''(r')) <= budget for all r' <= r*
    cnt = int(np.searchsorted(pm, budget, side="right"))      # number of radii that qualify
    if cnt == 0:
        return d * LN2, "enum"
    rstar = cnt - 1
    t = R.tab(d, u)
    lM = math.log(K) + d * LN2 - math.log(1 - eta) - t.lB[rstar]
    if lM < 40:
        lM = math.log(math.ceil(math.exp(lM) - 1e-9))
    lcost = LN2 + lM
    if lcost >= d * LN2:
        return d * LN2, "enum"
    return lcost, "K0"


def sample_base(C, d, xvec, ld):
    """emulation of the sampling of the theory division's qscheme.py (l.96-98: for a vector of accuracies served by the
    base bracket it checks 'the two ends and the middle'): least slack of  cost <= d a + E_base  over those three entries"""
    if not xvec:
        return
    for i in sorted(set([0, len(xvec) // 2, len(xvec) - 1])):
        x = xvec[i]
        c, kind = base_cost(C.u, d, x, ld)
        sl = d * C.a + F.E_base(C, d, x, -ld + d * LN2) - c
        stats['min_slack_sampled'] = min(stats['min_slack_sampled'], sl)
        stats['n_sampled'] += 1


class Base:
    def __init__(self, C):
        self.C, self.u = C, C.u
        self.B, self.sigma, self.Rr = C.a, 0.0, INF
        self.name = "G_0"
        self.memo = {}

    def E(self, d, x, Lam):
        return F.E_base(self.C, d, x, Lam)

    def cost(self, d, x, ld, variant):
        key = (d, x, ld)
        if key not in self.memo:
            c, kind = base_cost(self.u, d, x, ld)
            self.memo[key] = c
            stats['nodes'] += 1
            stats['base'] += 1
            stats['base_enum'] += kind == "enum"
            stats['min_base_lid'] = min(stats['min_base_lid'], -ld)
            stats['max_base_lid'] = max(stats['max_base_lid'], -ld)
            stats['min_base_d'] = min(stats['min_base_d'], d)
            stats['max_lid_over_d'] = max(stats['max_lid_over_d'], -ld / d)
            Lam = -ld + d * LN2
            slack = d * self.C.a + self.E(d, x, Lam) - c
            stats['min_slack_base'] = min(stats['min_slack_base'], slack)
            stats['min_slack_ind'] = min(stats['min_slack_ind'], slack)
            if slack < -TOL:
                violation("base induction d=%d x=%g ld=%g slack=%g" % (d, x, ld, slack))
        return self.memo[key]


class Slope:
    """S[F], section 4.1."""

    def __init__(self, C, inner):
        self.C, self.u, self.inner = C, C.u, inner
        self.B = inner.B
        assert self.B >= C.h - 1e-15 and 0 <= inner.sigma <= 1 + 1e-12
        if inner.Rr == INF:
            assert inner.sigma == 0.0
            self.Rr = C.h
        else:
            assert 0 < inner.Rr <= C.h + 1e-15
            self.Rr = inner.Rr * C.h / (C.h + inner.Rr)
        self.sigma = inner.sigma + self.B / C.h - 1
        self.name = "S[%s]" % inner.name
        self.memo = {}

    def E(self, d, x, Lam):
        return self.inner.E(d, min(x, 1.0), Lam + F.q_S(self.C, d, Lam)) + F.c_S(self.C, d, Lam, self.B)

    def level(self, d, xhat, ld, variant):
        C, u = self.C, self.u
        n_o = math.floor((xhat - 1 - F.c_log(C, d)) / C.h)
        n_i = d - n_o
        y = xhat - 1
        ltheta = y + math.log1p(-(3 * math.e + 1 + (2 * C.p) ** d / math.e) * math.exp(-y))
        x1 = min(math.ceil(xhat), math.ceil(2 * u * n_i) - 1)
        xs = [2 * u * n_i] + [float(v) for v in range(x1, 0, -1)]
        lev = R.Level(u, d, n_o, 1.0, 0.5, 1.0, ltheta, 1.0, 1.0, ld, xs)
        lC = [None] + [self.inner.cost(n_i, xs[l], lev.ldeltap, variant) for l in range(1, lev.L + 1)]
        lcm = lev.lCmax(lC)
        if isinstance(self.inner, Base):
            sample_base(C, n_i, xs[1:], lev.ldeltap)
        stats['S_built'] += 1
        if len(R._tabs) > 40:                      # memory: tables are rebuilt on demand (a Level keeps no table)
            R.clear_tabs(keep=[(d, u)])
            for kk in [kk for kk in _pm if kk[0] != d]:
                del _pm[kk]
        # --- checks of the level as built ---
        stats['max_xout_err'] = max(stats['max_xout_err'], abs(lev.xout - xhat))
        if abs(lev.xout - xhat) > 1e-7:
            violation("slope x_out != xhat: d=%d xhat=%g xout=%g" % (d, xhat, lev.xout))
        # Lemma Q4(b) at m = n_o, e = h, eta = 1/2:  r_dag >= min{m-1, floor(rho_h m)+1},  ln(1/pi) <= m h + ln(m+1)
        r1 = min(n_o - 1, math.floor(C.rho_h * n_o) + 1)
        s4 = n_o * C.h + math.log(n_o + 1) + lev.lpidag
        stats['min_slack_Q4'] = min(stats['min_slack_Q4'], s4)
        if lev.rdag < r1 or s4 < -TOL:
            violation("Lemma Q4: d=%d n_o=%d rdag=%d r1=%d slack=%g" % (d, n_o, lev.rdag, r1, s4))
        # (4.1): ln 2Mbar <= xhat - 1 + P_M,  P_M = ln(J+1) + ln(24 e (e-1)) + ln K
        PM = math.log(lev.J + 1) + math.log(24 * math.e * (math.e - 1)) + lev.lK
        s41 = xhat - 1 + PM - (LN2 + lev.lMbar)
        stats['min_slack_41'] = min(stats['min_slack_41'], s41)
        if s41 < -TOL:
            violation("(4.1): d=%d xhat=%g slack=%g" % (d, xhat, s41))
        # (2.1): ln(1/delta') + n_i ln 2 <= Lam + q_S(d, Lam)
        Lam = -ld + d * LN2
        if -lev.ldeltap + n_i * LN2 > Lam + F.q_S(C, d, Lam) + TOL:
            violation("(2.1) slope: d=%d" % d)
        # Proposition Q6:  ln C_max <= d B - sigma' xhat + E'(d, xhat; Lam)
        bq6 = d * self.B - self.sigma * xhat + self.E(d, xhat, Lam)
        stats['min_slack_Q6'] = min(stats['min_slack_Q6'], bq6 - lcm)
        if bq6 - lcm < -TOL:
            violation("Prop Q6: d=%d xhat=%g slack=%g" % (d, xhat, bq6 - lcm))
        return lcm, lev

    def cost(self, d, x, ld, variant):
        key = (d, x, ld, variant)
        if key in self.memo:
            return self.memo[key]
        C = self.C
        xhat = min(x, self.Rr * d)
        if xhat < F.c_log(C, d) + 1 + C.h:                    # X_0(d): pass-through
            c = self.inner.cost(d, x, ld, variant)
        else:
            lcm, lev = self.level(d, xhat, ld, variant)
            if variant == 'min':
                c = min(lcm, self.inner.cost(d, x, ld, variant))
            else:
                c = lcm
        self.memo[key] = c
        stats['nodes'] += 1
        Lam = -ld + d * LN2
        slack = d * self.B - self.sigma * min(x, self.Rr * d) + self.E(d, x, Lam) - c
        stats['min_slack_ind'] = min(stats['min_slack_ind'], slack)
        stats['min_slack_nonbase'] = min(stats['min_slack_nonbase'], slack)
        if slack < -TOL:
            violation("slope induction d=%d x=%g slack=%g" % (d, x, slack))
        return c


class Drop:
    """D[F; c, alpha], section 4.2."""

    def __init__(self, C, inner, c, alpha, xmin_inner):
        self.C, self.u, self.inner, self.c, self.alpha = C, C.u, inner, c, alpha
        assert inner.sigma >= 1 - 1e-12 and 0 < inner.Rr <= C.h + 1e-15 and C.h <= inner.B + 1e-15
        assert 0 < c <= 1 / 3 and 0 < alpha <= 1
        self.Bin, self.Rin = inner.B, inner.Rr
        self.beta = alpha - F.w_of_c(c)
        assert self.beta >= xmin_inner - 1e-12, "beta >= x_min of the inner family"
        self.phi = self.Rin / (C.a + self.Rin)
        self.B = (1 - self.phi) * self.Bin
        self.sigma, self.Rr = 0.0, INF
        self.name = "D[%s]" % inner.name
        self.memo = {}
        self.top_info = None

    def E(self, d, x, Lam):
        C = self.C
        return (self.inner.E(d, self.beta, Lam + F.q_D(C, d, Lam, self.c))
                + F.c_D(C, d, Lam, self.Bin, self.Rin, self.phi, self.c))

    def level(self, d, n_o, ld, variant, shift):
        C, u, c = self.C, self.u, self.c
        n_i = d - n_o
        x1 = math.ceil(self.Rin * n_i)
        xs = [2 * u * n_i] + [float(v) for v in range(x1, 0, -1)] + [self.beta]
        lev = R.Level(u, d, n_o, c, c, c, math.log(c), 2 * math.exp(u) * n_o / c, self.beta, ld, xs)
        lC = [None] + [self.inner.cost(n_i, xs[l], lev.ldeltap, variant) for l in range(1, lev.L + 1)]
        lcm = lev.lCmax(lC)
        if isinstance(self.inner, Slope) and isinstance(self.inner.inner, Base):
            vec = xs[1:]
            if variant != 'min':       # their 'proof' mode asks the base family only where the slope step passes through
                X0 = F.c_log(C, n_i) + 1 + C.h
                vec = [x for x in vec if min(x, self.inner.Rr * n_i) < X0]
            sample_base(C, n_i, vec, lev.ldeltap)
        if lev.xout > self.alpha + 1e-12:
            violation("drop accuracy: d=%d xout=%g alpha=%g" % (d, lev.xout, self.alpha))
        # Lemma Q3: ln(1/pi) <= n_o a + cpi_bar(n_o; ell_c)
        lc = F.ell_c(C, c)
        s3 = n_o * C.a + F.cpi_bar(C, n_o, lc) + lev.lpidag
        stats['min_slack_Q3'] = min(stats['min_slack_Q3'], s3)
        if s3 < -TOL:
            violation("Lemma Q3: d=%d n_o=%d slack=%g" % (d, n_o, s3))
        Lam = -ld + d * LN2
        if -lev.ldeltap + n_i * LN2 > Lam + F.q_D(C, d, Lam, c) + TOL:
            violation("(2.1) drop: d=%d" % d)
        # Proposition Q7: with shift  ln C_max <= d B' + E'(d; Lam);  without shift the same with cpi_bar in place of
        # B*sigma(n)  (report l.479)
        Ein = self.inner.E(d, self.beta, Lam + F.q_D(C, d, Lam, c))
        cD = F.c_D(C, d, Lam, self.Bin, self.Rin, self.phi, c)
        cp = F.cpi_bar(C, math.floor(self.phi * d), lc)
        if shift:
            # (4.2): ln 2Mbar <= P_M + R n_i
            PM = (math.log(4 * (1 + c) * math.exp(c) / (1 - c)) + math.log(lev.nu0) + lev.lK)
            s42 = PM + self.Rin * n_i - (LN2 + lev.lMbar)
            stats['min_slack_42'] = min(stats['min_slack_42'], s42)
            if s42 < -TOL:
                violation("(4.2): d=%d slack=%g" % (d, s42))
            b7 = d * self.B + Ein + cD
            stats['D_shift'] += 1
        else:
            b7 = d * self.B + Ein + cD - self.Bin * cp / (C.a + self.Rin) + cp
            stats['D_noshift'] += 1
        stats['min_slack_Q7'] = min(stats['min_slack_Q7'], b7 - lcm)
        if b7 - lcm < -TOL:
            violation("Prop Q7 (%s): d=%d slack=%g" % ("shift" if shift else "noshift", d, b7 - lcm))
        return lcm, lev

    def cost(self, d, x, ld, variant):
        key = (d, ld, variant)                     # accuracy-blind
        if key in self.memo:
            return self.memo[key]
        C, c = self.C, self.c
        cands = {}
        levs = {}
        if d >= F.nD_prime(C, c):
            sig = F.cpi_bar(C, math.floor(self.phi * d), F.ell_c(C, c)) / (C.a + self.Rin)
            no_s = math.floor(self.phi * d - sig)
            no_n = math.floor(self.phi * d)
            if no_s >= 1:
                cands['shift'], levs['shift'] = self.level(d, no_s, ld, variant, True)
            if variant == 'min' and no_n >= 1:
                cands['noshift'], levs['noshift'] = self.level(d, no_n, ld, variant, False)
        if variant == 'min' or 'shift' not in cands:
            cands['passthrough'] = self.inner.cost(d, self.alpha, ld, variant)
        best = min(cands, key=cands.get)
        cst = cands[best]
        self.memo[key] = cst
        self.top_info = dict(best=best, cands=dict(cands), lev=levs.get(best))
        stats['nodes'] += 1
        Lam = -ld + d * LN2
        slack = d * self.B + self.E(d, x, Lam) - cst
        stats['min_slack_ind'] = min(stats['min_slack_ind'], slack)
        stats['min_slack_nonbase'] = min(stats['min_slack_nonbase'], slack)
        if slack < -TOL:
            violation("drop induction d=%d slack=%g" % (d, slack))
        return cst


def build(C, eps, M):
    d, J, k, B, Rm, phi = C.epochs(M)
    eh, cs, alpha = F.accuracies(eps, M)
    fam = Base(C)
    for m in range(M):
        for j in range(J[m]):
            fam = Slope(C, fam)
        fam = Drop(C, fam, cs[m], alpha[m + 1], alpha[m])
        assert abs(fam.B - B[m + 1]) < 1e-12 * B[m + 1]
    return fam, alpha, k, B


def crosscheck_base(u):
    """my cached base_cost against r16lib.k0 (same definition, two code paths)"""
    worst = 0.0
    for d in (1, 2, 5, 17, 100, 733, 2500):
        for x in (0.05, 0.56, 0.8715, 1.0, 2.0, 3.0, 7.0, 25.0, 0.1 * d, 0.5 * d):
            for ld in (math.log(0.05), -40.0, -0.7 * d - 5):
                a1 = base_cost(u, d, x, ld)
                a2 = R.k0(u, d, x, ld)
                worst = max(worst, abs(a1[0] - a2[0]))
                assert a1[1] == a2[1], (d, x, ld, a1, a2)
    return worst


def main():
    t0 = time.time()
    n = int(sys.argv[1])
    M = int(sys.argv[2])
    eps = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8715
    delta = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
    u = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    C = F.Cube(u)
    ld = math.log(delta)
    print("r17_nest: u=%g n=%d M=%d eps=%g delta=%g   (a=%.6f h=%.6f)" % (u, n, M, eps, delta, C.a, C.h))
    print("cross-check of the cached base bracket against r16lib.k0 (210 cases): max |difference| = %.2e"
          % crosscheck_base(u))
    R.clear_tabs()
    _pm.clear()
    out = {}
    for variant in ('min', 'proof'):
        for key in list(stats):
            stats[key] = INF if key.startswith('min_') else 0
        stats['max_xout_err'] = 0.0
        stats['max_base_lid'] = 0.0
        stats['max_lid_over_d'] = 0.0
        del viol_log[:]
        fam, alpha, k, B = build(C, eps, M)
        tv = time.time()
        cst = fam.cost(n, min(eps, 1.0), ld, variant)
        Etot = F.E_total(C, n, eps, -ld, M)
        bound = n * B[M] + Etot
        out[variant] = cst
        print("\nvariant '%s': family %s, %d nested levels (k_M), alpha_0 = %.6f" % (variant, fam.name, k[M], alpha[0]))
        print("  exact certified ln cost = %.2f  = %.4f n a      Theorem Q8 bound n B_M + E_M = %.2f = %.4f n a"
              "      n B_M = %.2f (B_M/a = %.4f)" % (cst, cst / (n * C.a), bound, bound / (n * C.a), n * B[M], B[M] / C.a))
        print("  top-level check  cost <= n B_M + E_M: %s (slack %.2f)" % (cst <= bound + TOL, bound - cst))
        if M > 0 and fam.top_info is not None:
            ti = fam.top_info
            lev = ti['lev']
            print("  top drop: chosen '%s'; candidates %s" % (ti['best'], {kk: round(v, 2) for kk, v in ti['cands'].items()}))
            if lev is not None:
                print("  top level as chosen: n_o = %d, r_dag = %d, K = %d, ln 2Mbar = %.1f, ln(1/delta') = %.1f, L = %d"
                      % (lev.n_o, lev.rdag, lev.K, LN2 + lev.lMbar, -lev.ldeltap, lev.L))
        print("  nodes: %d (base %d); levels built: slope %d, drop with shift %d, drop without shift %d"
              % (stats['nodes'], stats['base'], stats['S_built'], stats['D_shift'], stats['D_noshift']))
        print("  violations: %d;  least slack: induction %.2f, Lemma Q4 %.3f, Lemma Q3 %.2f, (4.1) %.2f, (4.2) %.2f, "
              "Prop Q6 %.2f, Prop Q7 %.2f;  max |x_out - xhat| of slope levels %.1e"
              % (stats['viol'], stats['min_slack_ind'], stats['min_slack_Q4'], stats['min_slack_Q3'],
                 stats['min_slack_41'], stats['min_slack_42'], stats['min_slack_Q6'], stats['min_slack_Q7'],
                 stats['max_xout_err']))
        print("  base family (Proposition Q5(a)): %d calls (%d by enumeration), dimensions >= %d, ln(1/delta) from %.1f to %.1f "
              "(largest ln(1/delta)/d = %.2f); least slack of  cost <= d a + E_base(d, x; ln(1/delta) + d ln 2): %.2f"
              % (stats['base'], stats['base_enum'], stats['min_base_d'], stats['min_base_lid'], stats['max_base_lid'],
                 stats['max_lid_over_d'], stats['min_slack_base']))
        print("  least slack of the induction inequality over the nodes that are not base brackets (slope and drop families): %.2f"
              % stats['min_slack_nonbase'])
        print("  emulation of the sampling of their qscheme.py (base bracket checked at the two ends and the middle of every "
              "ladder; only where a slope family sits directly on the base family): %d base nodes sampled, least slack %.2f; "
              "with the slope and drop nodes: %.2f"
              % (stats['n_sampled'], stats['min_slack_sampled'], min(stats['min_slack_sampled'], stats['min_slack_nonbase'])))
        for v in viol_log:
            print("    VIOLATION: " + v)
        print("  [%.0f s; tables cached now: %d]" % (time.time() - tv, len(R._tabs)))
        R.clear_tabs()
        _pm.clear()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("LAST LINE r17_nest.py n=%d M=%d: completed; min %.2f proof %.2f; wall %.1f s; peak RSS %.1f MB"
          % (n, M, out['min'], out['proof'], time.time() - t0, rss))


if __name__ == "__main__":
    main()
