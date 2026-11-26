#!/usr/bin/env python3
"""Workstream N, check 3: Algorithm A (the abstract form of Algorithm 2L+, N_REPORT 2.2) run on small exact instances,
with every inequality of the proof of Theorem N1 checked on every run (nlib.check_run).

The outer integrand V(a) is computed exactly; the inner procedures are simulated by an oracle that returns a valid
bracket of the promised ratio around V(a), placed at random / at the top / at the bottom / adversarially (nlib._oracle),
so (V1) of the good event holds by construction and the outer loop -- the part of the algorithm that the abstract
theorem is about -- is run literally.  The Chernoff events (V2), (V3) are verified on the realised sample; a run with an
invalid bracket although they hold would be a counterexample to the theorem.

  S1  the cube: Q_{n_o} x Q_{n_i}, uniform, random u-Lipschitz psi (five kinds), V = fibre average by enumeration;
      Harper's tail functions; both with the abstract conventions (rule (c0)) and with the cube's (J of Theorem 11.56).
  S1b the negligible branch: radial outer landscapes sampled by shells, nu_1 = 1, small theta.
  S2  an abstract outer space: Q_4 with a biased product measure and a weighted Hamming envelope; exact tail functions
      by enumeration of all subsets (nlib.envelope_tails); V a random member of the envelope class; kappa_0 = 1 and
      kappa_0 = 0.02 (s_0 above min V: the ladder need not start below the integrand).
  S3  dependence with bounded influence (Theorem N4): mu(b|a) = Bernoulli(p(a))^k, p(a) = sigma(h + J(2|a|/m - 1));
      -ln V is Lipschitz with the slope u' = u + k max iota_1 (class-relative influence) on the outer cube; Harper with u'.
  S4  dependence with UNBOUNDED influence (Proposition N12): threshold coupling p(a) = sigma(J_c (tau - |a|)), residual
      psi = u|b|; the algorithm run (i) with the tail function of the assumed class (slope u): invalid brackets;
      (ii) with the tail function of the true class of V (slope = its largest edge ratio): valid, with the cost of an enumeration.
  S6  a nearest-neighbour chain (N_REPORT 4(f)): outer segment of 4 sites, inner of 6, symmetric binary chain; the outer
      law is the chain's marginal, the envelope has the one-sided slack at the boundary site; exact tail functions by
      enumeration; random u-Lipschitz psi on Q_10.
  M   mutations (the checks must have power): q without the factor 1/(1-eta); a tail function that is too small.

Run:  python3 n3_sim_abstract.py > out_n3_sim_abstract.txt        (about 3 minutes)
"""
import math
import sys
import time

import numpy as np

from nlib import (CubeTables, Consts, closing_level_steps, envelope_tails, run_level, check_run, INF)

t0 = time.time()
rng = np.random.default_rng(1126)
NAMES = ['good', 'valid', 'width', 'certs', 'closing', 'sizes', 'count', 'calls', 'term']


class FiniteOuter:
    def __init__(self, vals, probs):
        order = np.argsort(vals)
        self.vals = np.asarray(vals, dtype=float)[order]
        self.probs = np.asarray(probs, dtype=float)[order]
        self.cdf = np.cumsum(self.probs)
        self.A = float(np.dot(self.vals, self.probs))
        self.tailp = np.concatenate((np.cumsum(self.probs[::-1])[::-1], [0.0]))     # tailp[i] = sum_{k>=i} probs

    def draw(self, k):
        idx = np.minimum(np.searchsorted(self.cdf, rng.uniform(size=k) * self.cdf[-1]), len(self.vals) - 1)
        return self.vals[idx]

    def p(self, t):
        return float(self.tailp[int(np.searchsorted(self.vals, t, side='right'))])

    def p_at_truncation(self, target):
        """p(t_x - 0) for t_x = inf{t : E min(V, t) >= target}  (target < A)"""
        below = np.concatenate(([0.0], np.cumsum(self.vals * self.probs)))      # sum_{k<i} p_k v_k
        F = below[:-1] + self.vals * self.tailp[:-1]                            # E min(V, v_i)
        i = int(np.searchsorted(F, target, side='left'))
        return float(self.tailp[min(i, len(self.vals) - 1)])


def popc(x, m):
    c = np.zeros(x.shape, dtype=np.int64)
    for i in range(m):
        c += (x >> i) & 1
    return c


def random_lipschitz(n, u, kind):
    """a random member of L_u(Q_n), as an array over the 2^n points"""
    N = 1 << n
    x = np.arange(N)
    if kind == 0:
        psi = np.full(N, INF)
        for _ in range(int(rng.integers(1, 7))):
            psi = np.minimum(psi, rng.uniform(0, u * n) + u * popc(x ^ int(rng.integers(N)), n))
        return psi
    if kind == 1:
        psi = np.full(N, -INF)
        for _ in range(int(rng.integers(1, 7))):
            psi = np.maximum(psi, rng.uniform(0, u * n) - u * popc(x ^ int(rng.integers(N)), n))
        return psi
    if kind == 2:
        g = rng.uniform(-u, u, size=n)
        return sum(g[i] * ((x >> i) & 1) for i in range(n)).astype(float)
    if kind == 3:
        z = int(rng.integers(N))
        return u * np.maximum(popc(x ^ z, n), int(rng.integers(0, n + 1))).astype(float)
    if kind == 4:
        return np.zeros(N)
    psi = random_lipschitz(n, u, 0)
    z = int(rng.integers(N))
    return np.minimum(psi, psi[z] - rng.uniform(0, u * n / 2) + u * popc(x ^ z, n))


def lowered_cap(C, bp, val, ThetaBar):
    """the cap of N_REPORT 2.5, remark (R6):  max{K, 2 K nu0 kappa0 e^-b, 2 e^lam M_dagger, 2 M_ddagger},
    M_ddagger = K/((1-eta) pi_dd),  pi_dd = sup{pi : e^lam Xi(q) <= theta ThetaBar(c_eta pi_*) for all q < pi}"""
    thr = math.exp(-C.lam) * C.theta * ThetaBar(C.ceta * C.pi_star)
    pi_dd = 1.0
    for i in range(len(bp)):
        if val[i] > thr * (1 + 1e-12):
            pi_dd = bp[0] if i == 0 else bp[i - 1]
            break
    Mdd = C.K / ((1 - C.eta) * pi_dd)
    return max(C.K, 2 * C.K * C.nu0 * C.kappa0 * math.exp(-C.b), 2 * math.exp(C.lam) * C.Mdag, 2 * Mdd)


CAP = dict(worst=0.0, runs=0, viol=0)


def cap_check(res, cap):
    if 'npoints' in res and res['npoints'] > 0:
        Mmax = max(pa['M'] for lev in res['levels'] for pa in lev['passes'])
        CAP['runs'] += 1
        CAP['worst'] = max(CAP['worst'], Mmax / cap)
        CAP['viol'] += Mmax > cap * (1 + 1e-9)


LOW = dict(runs=0, viol=0, minratio=INF)


def lower_check(res, C, out, ell0, chk):
    """N_REPORT 2.5 (R7): on the good event the largest sample is at least K/((1+eta) p(t_x - 0)), where
    E min(V, t_x) = e^{-x_out} A  (if ell_0 < e^{-x_out} A)"""
    if chk is None or not chk['good'] or not chk['valid']:
        return
    target = math.exp(-C.xout) * out.A
    if ell0 >= target:
        return
    Mmax = max(pa['M'] for lev in res['levels'] for pa in lev['passes']) if res['levels'] and res['levels'][0]['passes'] else 0
    if Mmax == 0:
        return
    bound = C.K / ((1 + C.eta) * out.p_at_truncation(target))
    LOW['runs'] += 1
    LOW['minratio'] = min(LOW['minratio'], Mmax / bound)
    LOW['viol'] += Mmax < bound * (1 - 1e-9)


def tally(stats, key, chk, res):
    d = stats.setdefault(key, dict(runs=0, stopped=0, good=0, bad={k: 0 for k in NAMES}, bad_on_good={k: 0 for k in NAMES},
                                   maxM=0, levels=0, neg=0, pop=0, cap=0, maxratio=0.0, minslackL=INF, minslackU=INF))
    d['runs'] += 1
    if chk is None:
        return
    d['stopped'] += 1
    d['good'] += chk['good']
    for k in NAMES:
        if not chk[k]:
            d['bad'][k] += 1
            if chk['good']:
                d['bad_on_good'][k] += 1
    d['maxM'] = max(d['maxM'], res['npoints'])
    d['levels'] += len(res['levels'])
    d['neg'] += sum(1 for l in res['levels'] if l.get('kind') == 'neg')
    d['pop'] += sum(1 for l in res['levels'] if l.get('kind') == 'pop')
    d['cap'] += (res['stop'] == 'cap')
    d['maxratio'] = max(d['maxratio'], res['U'] / res['L'])


def report(stats, key, extra=""):
    d = stats[key]
    always = ['width', 'closing', 'sizes']                 # claims for every run
    b1 = sum(d['bad'][k] for k in always)
    b2 = sum(d['bad_on_good'][k] for k in NAMES if k not in always and k != 'good')
    print("  %-34s runs %4d  stopped %4d  good event %4d  | violations: every-run claims %d, on the good event %d | "
          "invalid brackets %d (on the good event %d) | levels left: %d populated, %d negligible; stops by the cap rule %d; "
          "largest sample %d; widest U/L %.3f %s"
          % (key, d['runs'], d['stopped'], d['good'], b1, b2, d['bad']['valid'], d['bad_on_good']['valid'], d['pop'], d['neg'],
             d['cap'], d['maxM'], d['maxratio'], extra))
    return b1 + b2


total_viol = 0

# ----------------------------------------------------------------------------------------------------------------
print("=" * 110)
print("S1. the cube Q_{n_o} x Q_{n_i}: Harper's tail functions, V = exact fibre averages of random members of L_u")
print("=" * 110)
stats = {}
param_sets = [
    # name, lam, eta, etap, theta, nu1 rule, b
    ("bounded  th=.3", 0.5, 0.5, 0.5, 0.3, 'b', 0.5),
    ("bounded  th=.1", 0.25, 0.25, 0.25, 0.1, 'b', 0.25),
    ("11.52 regime  ", 1.0, 0.5, 1.0, 20.0, 1.0, 1.0),
]
for (n_o, n_i, u) in [(8, 8, 1.0), (10, 8, 0.5), (9, 7, 2.0)]:
    n = n_o + n_i
    tab = CubeTables(n_o, u)
    bp, val = tab.steps()
    N_o, N_i = 1 << n_o, 1 << n_i
    for pname, lam, eta, etap, theta, nu1, b in param_sets:
        nu1v = 2 * math.exp(u) * n_o / theta if nu1 == 'b' else nu1
        x0 = 2 * u * n_i
        Lr = 6
        xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
        xs[-1] = b
        kappa0 = (2.0 / (1.0 + math.exp(u))) ** n
        lnD = n * (u + math.log(2.0 / (1.0 + math.exp(-u))))

        def closing(thrN, th, ce):
            return closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)[0]

        C_abs = Consts(lam, eta, etap, theta, nu1v, b, xs, 0.05, kappa0, closing, lnD=lnD)
        J_cube = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
        C_cube = Consts(lam, eta, etap, theta, nu1v, b, xs, 0.05, kappa0, closing, lnD=lnD, J=J_cube)
        for kind in range(6):
            for rep in range(3):
                psi = random_lipschitz(n, u, kind)
                psi2 = psi.reshape(N_i, N_o)                 # low bits = outer block
                V = np.exp(-psi2).mean(axis=0)
                psi0 = psi[0]
                ell0 = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
                Vmax = math.exp(-psi0 + u * n)
                out = FiniteOuter(V, np.full(N_o, 1.0 / N_o))
                assert ell0 <= out.A * (1 + 1e-12) and V.max() <= Vmax * (1 + 1e-12)
                for mode in range(4):
                    for (cname, C, mut) in (("abstract", C_abs, ()), ("cube J, no cap", C_cube, ('no_cap',))):
                        res = run_level(rng, out.draw, C, tab.Xi, tab.ThetaBar, ell0, Vmax=Vmax, oracle_mode=mode, mut=mut)
                        cap_check(res, lowered_cap(C, bp, val, tab.ThetaBar))
                        key = "u=%.1f n_o=%d %s %s" % (u, n_o, pname, cname)
                        if res['stop'] in ('closed', 'cap'):
                            chk = check_run(res, C, out.A, out.p)
                            tally(stats, key, chk, res)
                            lower_check(res, C, out, ell0, chk)
                        else:
                            tally(stats, key, None, res)
for key in stats:
    total_viol += report(stats, key)

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("S1b. the negligible branch: radial outer landscapes on Q_{n_o} (sampled by shells), nu_1 = 1 and a small theta, so that")
print("     levels above the bulk are left as negligible ([N] fails at small radii); psi(a,b) = g(|a|) + u|b|")
print("=" * 110)
stats = {}
for (n_o, n_i, u, theta) in [(12, 4, 0.5, 0.05), (13, 4, 0.5, 0.05), (16, 4, 0.4, 0.05), (12, 4, 0.7, 0.05), (11, 5, 0.6, 0.03),
                             (12, 4, 0.5, 2.0)]:
    n = n_o + n_i
    tab = CubeTables(n_o, u)
    bp, val = tab.steps()
    lam, eta, etap, b = 1.0, 0.5, 1.0, 0.5
    x0 = 2 * u * n_i
    xs = [x0, (x0 * b) ** 0.5, b]
    kappa0 = (2.0 / (1.0 + math.exp(u))) ** n
    lnD = n * (u + math.log(2.0 / (1.0 + math.exp(-u))))
    C = Consts(lam, eta, etap, theta, 1.0, b, xs, 0.05, kappa0,
               lambda thrN, th, ce: closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)[0], lnD=lnD)
    shells = np.arange(n_o + 1)
    probs = np.array([math.comb(n_o, j) for j in shells], dtype=float) / 2.0 ** n_o
    for prof in range(4):
        if prof == 0:
            g = u * shells.astype(float)                                  # cone
        elif prof == 1:
            g = u * np.maximum(shells - 2, 0).astype(float)               # cone with a flat bottom
        elif prof == 2:
            g = u * np.minimum(shells, n_o // 2).astype(float)            # cone on a plateau
        else:
            g = np.concatenate(([0.0], np.cumsum(rng.uniform(0, u, size=n_o))))      # random monotone profile
        vals = np.exp(-g) * ((1 + math.exp(-u)) / 2) ** n_i
        out = FiniteOuter(vals, probs)
        ell0 = math.exp(-g[0]) * ((1 + math.exp(-u)) / 2) ** n            # reference point 0: psi_0 = g(0)
        Vmax = math.exp(-g[0] + u * n)
        for mode in range(4):
            for rep in range(2):
                res = run_level(rng, out.draw, C, tab.Xi, tab.ThetaBar, ell0, Vmax=Vmax, oracle_mode=mode)
                cap_check(res, lowered_cap(C, bp, val, tab.ThetaBar))
                key = "n_o=%d u=%.1f theta=%.2f nu0=%.0f" % (n_o, u, theta, C.nu0)
                if res['stop'] in ('closed', 'cap'):
                    chk = check_run(res, C, out.A, out.p)
                    tally(stats, key, chk, res)
                    lower_check(res, C, out, ell0, chk)
                else:
                    tally(stats, key, None, res)
for key in stats:
    total_viol += report(stats, key)
print("  the lowered cap of N_REPORT 2.5 (R6) in the runs of S1 and S1b: %d runs, largest sample / cap = %.3f [<= 1], violations %d"
      % (CAP['runs'], CAP['worst'], CAP['viol']))
total_viol += CAP['viol']

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("S2. an abstract outer space: Q_4, biased product measure, weighted Hamming envelope, exact tail functions (65534 subsets)")
print("=" * 110)
stats = {}
m = 4
Nm = 1 << m
xo = np.arange(Nm)
for case in range(3):
    ps = rng.uniform(0.15, 0.6, size=m)
    us = rng.uniform(0.3, 1.5, size=m)
    mu = np.ones(Nm)
    for i in range(m):
        mu *= np.where((xo >> i) & 1, ps[i], 1 - ps[i])
    rho = np.zeros((Nm, Nm))
    for a in range(Nm):
        for c in range(Nm):
            rho[a, c] = sum(us[i] for i in range(m) if ((a ^ c) >> i) & 1)
    Xi, Th = envelope_tails(mu, rho)
    ThBar = lambda p, Th=Th: max(p, Th(p))
    for kappa0 in (1.0, 0.02):
        for pname, lam, eta, etap, theta, nu1, b in [("th=.5", 0.5, 0.5, 0.5, 0.5, 20.0, 0.5), ("th=5", 1.0, 0.5, 1.0, 5.0, 1.0, 1.0)]:
            xs = [6.0, 3.0, 1.5, b]
            for rep in range(12):
                # a random member of the envelope class: g = min_k [c_k + rho(., z_k)]  (g(x) - g(y) <= rho(x, y))
                g = np.full(Nm, INF)
                for _ in range(int(rng.integers(1, 5))):
                    g = np.minimum(g, rng.uniform(0, 4) + rho[:, int(rng.integers(Nm))])
                V = np.exp(-g)
                assert all(V[a] <= V[c] * math.exp(rho[a, c]) * (1 + 1e-12) for a in range(Nm) for c in range(Nm))
                a0 = int(rng.integers(Nm))
                ell0 = V[a0] * float(np.dot(mu, np.exp(-rho[a0, :])))       # V(a) >= V(a0) e^{-rho(a0, a)}
                Vmax = V[a0] * math.exp(float(rho[:, a0].max()))            # V(a) <= V(a0) e^{rho(a, a0)}
                out = FiniteOuter(V, mu)
                assert ell0 <= out.A * (1 + 1e-12) and V.max() <= Vmax * (1 + 1e-12)
                lnD = math.log(Vmax / ell0)

                def closing(thrN, th, ce):
                    return closing_level_steps(Xi.bp, Xi.val, ThBar, thrN, th, ce)[0]

                C = Consts(lam, eta, etap, theta, nu1, b, xs, 0.05, kappa0, closing, lnD=lnD)
                for mode in range(4):
                    res = run_level(rng, out.draw, C, Xi, ThBar, ell0, Vmax=Vmax, oracle_mode=mode)
                    key = "kappa0=%.2f %s" % (kappa0, pname)
                    if res['stop'] in ('closed', 'cap'):
                        chk = check_run(res, C, out.A, out.p)
                        tally(stats, key, chk, res)
                        lower_check(res, C, out, ell0, chk)
                    else:
                        tally(stats, key, None, res)
for key in stats:
    total_viol += report(stats, key)

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("S3. dependence, bounded influence: outer Q_m uniform, mu(b|a) = Bernoulli(p(a))^k, p(a) = sigma(h + J(2|a|/m - 1))")
print("    psi(a,b) = g(a) + sum_i gamma_i b_i with g in L_u(Q_m), |gamma_i| <= u:  V(a) = e^{-g(a)} prod_i (1 - p(a) + p(a) e^{-gamma_i})")
print("=" * 110)
stats = {}
sig = lambda z: 1.0 / (1.0 + math.exp(-z))


def iota1(p, pp, u):
    """class-relative influence of one Bernoulli coordinate: sup over log-u-Lipschitz w of ln(E_p w/E_pp w)"""
    return max(math.log((1 + p * math.expm1(c)) / (1 + pp * math.expm1(c))) for c in (u, -u))


for (m, k, u, h, Jc) in [(10, 16, 1.0, 0.0, 0.4), (10, 12, 0.5, -0.5, 1.0), (9, 20, 1.0, 0.3, 0.25)]:
    Nm = 1 << m
    xo = np.arange(Nm)
    wt = popc(xo, m)
    pj = np.array([sig(h + Jc * (2 * j / m - 1)) for j in range(m + 1)])
    i_class = max(max(iota1(pj[j], pj[j + 1], u), iota1(pj[j + 1], pj[j], u)) for j in range(m))
    L_point = k * max(max(abs(math.log(pj[j] / pj[j + 1])), abs(math.log((1 - pj[j]) / (1 - pj[j + 1])))) for j in range(m))
    u_eff = u + k * i_class
    tab = CubeTables(m, u_eff)
    bp, val = tab.steps()
    worst_edge = 0.0
    for pname, lam, eta, etap, theta, nu1, b in [("th=.3", 0.5, 0.5, 0.5, 0.3, 'b', 0.5), ("th=20", 1.0, 0.5, 1.0, 20.0, 1.0, 1.0)]:
        nu1v = 2 * math.exp(u_eff) * m / theta if nu1 == 'b' else nu1
        x0 = 2 * u * k
        xs = [x0, x0 / 3, x0 / 9, b] if x0 / 9 > b else [x0, (x0 * b) ** 0.5, b]

        def closing(thrN, th, ce):
            return closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)[0]

        for rep in range(10):
            g = random_lipschitz(m, u, int(rng.integers(6)))
            gam = rng.uniform(-u, u, size=k)
            if rep % 3 == 0:
                gam = np.full(k, u if rep % 2 else -u)       # the extremal fibre (uniform field)
            V = np.exp(-g) * np.prod(1 - pj[wt][:, None] + pj[wt][:, None] * np.exp(-gam)[None, :], axis=1)
            lv = np.log(V)
            for i in range(m):
                worst_edge = max(worst_edge, float(np.max(np.abs(lv - lv[xo ^ (1 << i)]))))
            a0 = 0
            # reference data from the envelope u_eff * Hamming on the outer cube:  V(a) in V(a0) e^{-+ u_eff d(a, a0)}
            ell0 = V[a0] * ((1 + math.exp(-u_eff)) / 2) ** m
            Vmax = V[a0] * math.exp(u_eff * m)
            out = FiniteOuter(V, np.full(Nm, 1.0 / Nm))
            C = Consts(lam, eta, etap, theta, nu1v, b, xs, 0.05, 0.05, closing, lnD=math.log(Vmax / ell0))
            for mode in (0, 3):
                res = run_level(rng, out.draw, C, tab.Xi, tab.ThetaBar, ell0, Vmax=Vmax, oracle_mode=mode)
                key = "m=%d k=%d u=%.1f J=%.2f %s" % (m, k, u, Jc, pname)
                if res['stop'] in ('closed', 'cap'):
                    chk = check_run(res, C, out.A, out.p)
                    tally(stats, key, chk, res)
                    lower_check(res, C, out, ell0, chk)
                else:
                    tally(stats, key, None, res)
    print("  m=%d k=%d u=%.1f h=%.1f J=%.2f:  slope of -ln V on the outer cube: observed max %.4f  <=  u + k*iota_1 = %.4f"
          "  (pointwise influence bound u + L = %.4f)" % (m, k, u, h, Jc, worst_edge, u_eff, u + L_point))
    total_viol += (worst_edge > u_eff * (1 + 1e-9))
for key in stats:
    total_viol += report(stats, key)

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("S4. dependence, UNBOUNDED influence (Proposition N12): outer Q_12 uniform, mu(b|a) = Bernoulli(p(a))^16,")
print("    p(a) = sigma(J_c (10.5 - |a|)), J_c = 4;  psi(a,b) = u|b|, u = 1 (additive, u-Lipschitz, does not depend on a)")
print("=" * 110)
m, k, u, Jc, tau = 12, 16, 1.0, 4.0, 10.5
Nm = 1 << m
xo = np.arange(Nm)
wt = popc(xo, m)
pj = np.array([sig(Jc * (tau - j)) for j in range(m + 1)])
Vj = (1 - pj + pj * math.exp(-u)) ** k
V = Vj[wt]
out = FiniteOuter(V, np.full(Nm, 1.0 / Nm))
edge = max(abs(math.log(Vj[j + 1] / Vj[j])) for j in range(m))
lp = lambda z: -math.log1p(math.exp(-z))               # ln sigma(z);  ln(1 - sigma(z)) = lp(-z)
zj = [Jc * (tau - j) for j in range(m + 1)]
L_point = k * max(max(abs(lp(zj[j]) - lp(zj[j + 1])), abs(lp(-zj[j]) - lp(-zj[j + 1]))) for j in range(m))
print("  V by outer weight |a| = 0..12: " + " ".join("%.3g" % v for v in Vj))
print("  A = %.6g;  bulk value V(|a| <= 9) <= %.3g;  mu_o(|a| >= 11) = %.5f carries %.1f%% of A" %
      (out.A, Vj[9], 13 / Nm, 100 * (12 * Vj[11] + Vj[12]) / Nm / out.A))
print("  largest edge ratio of V: e^{%.3f}  (u = %.1f;  pointwise influence bound L = %.1f, i.e. slope <= %.1f)" % (edge, u, L_point, u + L_point))
# (TU) with Harper's function for the slope u, at the levels between the bulk and the spike
tabu = CubeTables(m, u)
worst = 0.0
for s in np.unique(V):
    q = out.p(s)
    if 0 < q < 1:
        tail = float(np.mean(np.maximum(V - s, 0)))
        xi = tabu.Xi(q)
        if xi < INF:
            worst = max(worst, tail / (s * xi))
print("  (TU) for the slope u fails by the factor %.4g  (max over levels of E(V-s)_+ / (s Xi_u(q)))" % worst)
stats = {}
x0 = 2 * u * k
for (label, slope) in (("(i)  tail function of the assumed class, slope u", u), ("(ii) tail function of the true class, slope %.2f" % edge, edge)):
    tab = CubeTables(m, slope)
    bp, val = tab.steps()

    def closing(thrN, th, ce):
        return closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)[0]

    for pname, lam, eta, etap, theta, nu1, b in [("th=20", 1.0, 0.5, 1.0, 20.0, 1.0, 1.0), ("th=1", 0.5, 0.5, 0.5, 1.0, 'b', 0.5)]:
        nu1v = 2 * math.exp(slope) * m / theta if nu1 == 'b' else nu1
        xs = [x0, x0 / 3, x0 / 9, b]
        # reference data: psi does not depend on a, so the fibre's own bounds are valid for every a:
        # e^{-u k} <= V <= 1 and A >= ((1+e^{-u})/2)^k is NOT available under mu(.|a); use what holds: V >= e^{-uk}
        ell0 = math.exp(-u * k)
        Vmax = 1.0
        C = Consts(lam, eta, etap, theta, nu1v, b, xs, 0.05, 1.0, closing, lnD=math.log(Vmax / ell0))
        ratios = []
        Ms = []
        for rep in range(40):
            res = run_level(rng, out.draw, C, tab.Xi, tab.ThetaBar, ell0, Vmax=Vmax, oracle_mode=rep % 4)
            key = "%s  %s" % (label, pname)
            if res['stop'] in ('closed', 'cap'):
                chk = check_run(res, C, out.A, out.p)
                tally(stats, key, chk, res)
                ratios.append(out.A / res['U'])
                Ms.append(res['npoints'])
            else:
                tally(stats, key, None, res)
        d = stats[key]
        print("  %-60s runs %d  stopped %d  INVALID %d (good event held in %d of the runs)  "
              "A/U: median %.3g, max %.3g   points: median %d (pi_* = %.3g, Mbar = %.3g; 2^12 = 4096)"
              % (key, d['runs'], d['stopped'], d['bad']['valid'], d['good'], float(np.median(ratios)), max(ratios),
                 int(np.median(Ms)), C.pi_star, C.Mbar))
        if slope == edge:
            total_viol += d['bad_on_good']['valid'] + d['bad']['width'] + d['bad']['closing'] + d['bad']['sizes']

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("S6. a nearest-neighbour chain as known part: outer segment 4 sites, inner 6 sites, symmetric binary chain, flip p")
print("    V(a) = E[e^{-psi(a, .)} | a] under the chain;  envelope on the outer segment: slopes (u, u, u, v), v = u + g(v_k)")
print("=" * 110)
stats = {}
m, k = 4, 6
n = m + k
N = 1 << n
Nm, Nk = 1 << m, 1 << k
xo = np.arange(Nm)
for (p, u) in [(0.3, 1.0), (0.1, 1.0), (0.2, 0.5)]:
    gfun = lambda v: math.log(((1 - p) * math.exp(v) + p) / (p * math.exp(v) + 1 - p))
    v = u
    for _ in range(k - 1):                      # v^{(1)} = u (one inner site), v^{(j+1)} = u + g(v^{(j)})
        v = u + gfun(v)
    v_bound = u + gfun(v)                       # Lipschitz constant of -ln V in the boundary letter
    ustar = u
    for _ in range(200):
        ustar = u + gfun(ustar)
    Kc = math.log((1 - p) / p)
    # outer law: the marginal of the stationary chain on sites 1..m (site m = bit m-1 is the boundary)
    mu = np.full(Nm, 0.5)
    for i in range(m - 1):
        same = ((xo >> i) & 1) == ((xo >> (i + 1)) & 1)
        mu *= np.where(same, 1 - p, p)
    # conditional law of the inner segment given the boundary letter
    xb = np.arange(Nk)
    cond = np.zeros((2, Nk))
    for a in (0, 1):
        pr = np.where((xb & 1) == a, 1 - p, p).astype(float)
        for i in range(k - 1):
            same = ((xb >> i) & 1) == ((xb >> (i + 1)) & 1)
            pr = pr * np.where(same, 1 - p, p)
        cond[a] = pr
    us = [u] * (m - 1) + [v_bound]
    rho = np.zeros((Nm, Nm))
    rho_plain = np.zeros((Nm, Nm))
    for a in range(Nm):
        for c in range(Nm):
            rho[a, c] = sum(us[i] for i in range(m) if ((a ^ c) >> i) & 1)
            rho_plain[a, c] = u * bin(a ^ c).count("1")
    Xi, Th = envelope_tails(mu, rho)
    ThBar = lambda q, Th=Th: max(q, Th(q))
    Xi_pl, Th_pl = envelope_tails(mu, rho_plain)
    ThBar_pl = lambda q, Th_pl=Th_pl: max(q, Th_pl(q))
    worst_b = 0.0
    worst_o = 0.0
    viol_plain = 0
    tu_plain = 0.0
    for rep in range(60):
        kind = int(rng.integers(6))
        psi = random_lipschitz(n, u, kind)
        if rep < 4:                               # the extremal instance: the uniform field (attains v_bound)
            psi = (-u if rep % 2 else u) * popc(np.arange(N), n).astype(float)
        psi2 = psi.reshape(Nk, Nm)                # low bits = outer segment; inner bit 0 is adjacent to the boundary bit m-1
        Wt = np.exp(-(psi2 - psi2.min()))
        bl = (xo >> (m - 1)) & 1
        V = np.array([float(np.dot(cond[bl[a]], Wt[:, a])) for a in range(Nm)])
        lv = np.log(V)
        for i in range(m):
            d = float(np.max(np.abs(lv - lv[xo ^ (1 << i)])))
            if i == m - 1:
                worst_b = max(worst_b, d)
            else:
                worst_o = max(worst_o, d)
        # (TU) with the two enumerated tail functions
        for s in np.unique(V):
            q = float(mu[V > s].sum())
            if 0 < q < 1:
                tail = float(np.dot(mu, np.maximum(V - s, 0)))
                if tail > s * Xi(q) * (1 + 1e-9):
                    total_viol += 1
                tu_plain = max(tu_plain, tail / (s * Xi_pl(q)))
                viol_plain += tail > s * Xi_pl(q) * (1 + 1e-9)
        a0 = int(rng.integers(Nm))
        ell0 = V[a0] * float(np.dot(mu, np.exp(-rho[a0, :])))
        Vmax = V[a0] * math.exp(float(rho[:, a0].max()))
        out = FiniteOuter(V, mu)

        def closing(thrN, th, ce):
            return closing_level_steps(Xi.bp, Xi.val, ThBar, thrN, th, ce)[0]

        for pname, lam, eta, etap, theta, nu1, b in [("th=.5", 0.5, 0.5, 0.5, 0.5, 20.0, 0.5), ("th=5", 1.0, 0.5, 1.0, 5.0, 1.0, 1.0)]:
            xs = [2 * u * k, 4.0, 1.5, b] if 2 * u * k > 4.0 else [2 * u * k, 1.5, b]
            C = Consts(lam, eta, etap, theta, nu1, b, xs, 0.05, 0.1, closing, lnD=math.log(Vmax / ell0))
            res = run_level(rng, out.draw, C, Xi, ThBar, ell0, Vmax=Vmax, oracle_mode=rep % 4)
            key = "p=%.1f u=%.1f %s" % (p, u, pname)
            if res['stop'] in ('closed', 'cap'):
                chk = check_run(res, C, out.A, out.p)
                tally(stats, key, chk, res)
                lower_check(res, C, out, ell0, chk)
            else:
                tally(stats, key, None, res)
    print("  p=%.1f u=%.1f:  slope of -ln V in a non-boundary letter: max %.4f <= u = %.2f;   in the boundary letter: max %.6f, "
          "bound v = u + g(v_k) = %.6f (attained by the uniform field), u* = %.4f, u + K = %.4f"
          % (p, u, worst_o, u, worst_b, v_bound, ustar, u + Kc))
    print("              with the envelope WITHOUT the slack (slopes u,u,u,u): (TU) violated at %d levels, worst factor %.4f"
          % (viol_plain, tu_plain))
    total_viol += (worst_b > v_bound * (1 + 1e-9)) + (worst_o > u * (1 + 1e-9))
for key in stats:
    total_viol += report(stats, key)

# ----------------------------------------------------------------------------------------------------------------
print()
print("=" * 110)
print("M. mutations on the cube instances of S1 (u = 1, n_o = 8): the checks must detect them")
print("=" * 110)
n_o, n_i, u = 8, 8, 1.0
n = n_o + n_i
tab = CubeTables(n_o, u)
bp, val = tab.steps()
N_o, N_i = 1 << n_o, 1 << n_i
lam, eta, etap, theta, b = 0.5, 0.5, 0.5, 0.3, 0.5
nu1v = 2 * math.exp(u) * n_o / theta
x0 = 2 * u * n_i
xs = [x0 * (b / x0) ** (l / 6) for l in range(7)]
xs[-1] = b
kappa0 = (2.0 / (1.0 + math.exp(u))) ** n
lnD = n * (u + math.log(2.0 / (1.0 + math.exp(-u))))
C = Consts(lam, eta, etap, theta, nu1v, b, xs, 0.05, kappa0,
           lambda thrN, th, ce: closing_level_steps(bp, val, tab.ThetaBar, thrN, th, ce)[0], lnD=lnD)
for (mname, mut, Xi_m) in (("q without 1/(1-eta)", ('q_plain',), tab.Xi), ("tail function divided by 50", (), lambda q: tab.Xi(q) / 50.0),
                           ("none (control)", (), tab.Xi)):
    det = dict(runs=0, certs=0, valid=0, any=0)
    for rep in range(48):
        psi = random_lipschitz(n, u, rep % 6)
        psi2 = psi.reshape(N_i, N_o)
        V = np.exp(-psi2).mean(axis=0)
        ell0 = math.exp(-psi[0]) * ((1 + math.exp(-u)) / 2) ** n
        Vmax = math.exp(-psi[0] + u * n)
        out = FiniteOuter(V, np.full(N_o, 1.0 / N_o))
        res = run_level(rng, out.draw, C, Xi_m, tab.ThetaBar, ell0, Vmax=Vmax, oracle_mode=rep % 4, mut=mut)
        if res['stop'] in ('closed', 'cap'):
            chk = check_run(res, C, out.A, out.p)
            det['runs'] += 1
            det['certs'] += (not chk['certs'])
            det['valid'] += (not chk['valid'])
            det['any'] += (not all(chk[k] for k in NAMES if k != 'good'))
    print("  mutation %-28s runs %d: certificate failures %d, invalid brackets %d, any check failed %d"
          % (mname, det['runs'], det['certs'], det['valid'], det['any']))

print()
print("the lower bound of N_REPORT 2.5 (R7) on the outer sample, M_max >= K/((1+eta) p(t_x - 0)): %d runs of S1, S1b, S2, S3, S6 "
      "with ell_0 < e^{-x_out} A: smallest M_max/bound = %.3f [>= 1], violations %d" % (LOW['runs'], LOW['minratio'], LOW['viol']))
total_viol += LOW['viol']
print("violations of Theorem N1 in the valid settings (S1, S1b, S2, S3, S4(ii), S6):", total_viol, "   time %.1f s" % (time.time() - t0))
sys.exit(1 if total_viol else 0)
