#!/usr/bin/env python3
"""Referee R12, check 3: the two inductive steps of Q_REPORT (Proposition Q6: slope step, Proposition Q7: drop),
one level at a time, with the exact constants of Theorem K1 (own evaluator r12lib.level_consts / level_cmax).

Part 0  my evaluator of one level against the earlier referee's r8_flat.flat_run (design of K_REPORT 6.4, base
        brackets inside): J, K, r_dagger, ln Mbar, ln delta', x_out, ln C_max.
Part A  Proposition Q6.  The inner family is given the cost  d B - sigma min(x, R d) + E(d, x; ln(1/delta) + d ln 2)
        EXACTLY (the largest cost that H(B, sigma, R; E) allows; C_max is nondecreasing in the inner costs), with
        E = 0 and with three non-trivial error functions (increasing in d, in Lambda, decreasing in x).  The level as
        built is evaluated exactly and compared with  n B - sigma' xhat + c_S(n, Lam; B) + E(n, 1; Lam + q_S(n, Lam)).
        Parameters far outside the epoch schedule are included (any B >= h, 0 <= sigma <= 1, R <= h or infinite),
        the smallest dimensions at which a level is built, accuracies at both ends, failure probabilities from
        0.999 down to e^{-50 n}, slopes u = 0.1 ... 4.
Part B  Proposition Q7, in the same way (inner cost d B - min(x, R d) + E), with and without the shift; every n from
        the first admissible one to 200 and sizes up to 10^6; c from 1/3 to 10^{-8}.
Part C  the small facts used: w(c) <= 6.25 c, the numerical constants 1.2, 1.5, 5.6, 7.45, 11.17, 4 of Q7(3),
        (F3) h <= u^2/16, (F4), the identity B_{m+1} = B_m J_m a/(J_m a + h), the epoch arithmetic (R).

usage: python3 r12_03_steps.py > out_03_steps.txt       (about 6 minutes)
"""
import sys, os, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import (Cube, Tab, TabCache, Formula, Stats, Family, Base, Slope, Drop, level_consts, level_cmax,
                    LN2, INF, kl, kl_half)

t0 = time.time()


class Synthetic(Family):
    """a family whose certified cost EQUALS the majorant  d B - sigma min(x, R d) + E(d, x; ln(1/delta) + d ln 2)"""

    def __init__(self, cube, st, fm, B, sigma, R, Efun=None, xmin=0.0, tag=''):
        self.c, self.st, self.fm, self.tag = cube, st, fm, tag
        self.tabs = None
        self.B, self.sigma, self.R, self.xmin = B, sigma, R, xmin
        self.Efun = Efun

    def E(self, d, x, Lam):
        return 0.0 if self.Efun is None else self.Efun(d, x, Lam)

    def cost(self, d, x, ld):
        return d * self.B - self.sigma * min(x, self.R * d if self.R < INF else INF) + self.E(d, x, -ld + d * LN2)

    def cost_many(self, d, xs, ld):
        return [self.cost(d, x, ld) for x in xs]


print("# Referee R12, check 3: Propositions Q6 and Q7, one level at a time, exact constants")

# -------------------------------------------------------------------------------------------- Part 0
print("\n# Part 0: own level evaluator against r8_flat.flat_run (K_REPORT 6.4: b=0.5, lam=0.2, eta=eta'=theta=0.05, delta=0.05,")
print("#         geometric ladder of 40 rungs, n_o = n/2, nu_1 = 2e^u n_o/theta, base brackets inside)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'R8'))
import r8_flat
print("#  u      n     J      K     r_dag   ln Mbar    ln delta'    x_out    ln C_max     ln C_max/(na)   | largest difference to flat_run")
worst = 0.0
for u in (1.0, 2.0, 0.5):
    cu = Cube(u)
    fm = Formula(cu)
    st = Stats()
    tabs = TabCache(u, 8)
    base = Base(cu, tabs, st, fm)
    for n in (1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000) if u == 1.0 else (1000, 4000, 16000):
        n_o = n // 2
        n_i = n - n_o
        b, lam, eta, etap, theta, delta, Lr = 0.5, 0.2, 0.05, 0.05, 0.05, 0.05, 40
        x0 = 2 * u * n_i
        xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
        xs[-1] = b
        cs = level_consts(cu, tabs.get(n_o), n, n_o, lam, eta, etap, math.log(theta), 2 * math.exp(u) * n_o / theta, b,
                          math.log(delta), Lr)
        lC = [base.raw(n_i, x, cs['ldeltap'])[0] for x in xs[1:]]
        lCmax, arg = level_cmax(cs, xs, lC)
        r = r8_flat.flat_run(u, n, 0.5)
        dif = max(abs(cs['J'] - r['J']), abs(cs['K'] - r['K']), abs(cs['rdag'] - r['rdag']), abs(cs['lMbar'] - r['lMbar']),
                  abs(cs['ldeltap'] - r['ldeltap']), abs(cs['xout'] - r['xout']), abs(lCmax - r['lCmax']))
        worst = max(worst, dif)
        print("  %.1f  %6d  %6d  %6d  %6d  %9.3f  %10.3f   %.4f  %10.3f      %.4f          | %.2e"
              % (u, n, cs['J'], cs['K'], cs['rdag'], cs['lMbar'], cs['ldeltap'], cs['xout'], lCmax, lCmax / (n * cu.a), dif))
print("# largest difference over all rows: %.2e   (theory report 11.19(1b), two levels certified, u = 1:"
      " 1.1384 0.9933 0.8721 0.7262 0.6415 0.5899 0.5646 0.5407)" % worst)
sys.stdout.flush()

# -------------------------------------------------------------------------------------------- Part A
print("\n# Part A: Proposition Q6 (slope step) with a saturating inner family")
EFUNS = {
    'E=0': None,
    'E=3sqrt(d)': lambda d, x, Lam: 3 * math.sqrt(d),
    'E=Lam/7': lambda d, x, Lam: Lam / 7,
    'E=5/x+ln(Lam)': lambda d, x, Lam: 5 / x + math.log(Lam),
}


def first_n(fm, Rp):
    """least n with Rp n >= X_0(n)"""
    n = 2
    while Rp * n < fm.X0(n):
        n = max(n + 1, int(n * 1.05))
    while n > 2 and Rp * (n - 1) >= fm.X0(n - 1):
        n -= 1
    return n


print("#  u    triples (B,sigma,R)   levels built   violations   least slack of Q6 [nats] at (B/h, sigma, R/h, n, xhat, ln delta, E)"
      "   range of c_S   least slack of Lemma Q4   largest |x_out - xhat|   cases with x_1 < xhat (second case of step (5))")
grand = 0
grand_viol = 0
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    cu = Cube(u)
    fm = Formula(cu)
    h, a = cu.h, cu.a
    ep = cu.epochs(12)
    triples = []
    for m in range(12):
        for j in range(ep['J'][m]):
            triples.append((ep['B'][m], j / ep['d'][m], INF if j == 0 else h / j))
    for Bf in (1.0, 1.01, 2.0, 11.0, 101.0):
        triples.append((h * Bf, 0.0, INF))
        for sg in (0.0, 0.3, 1.0):
            for Rf in (1.0, 1 / 3, 1 / 50):
                triples.append((h * Bf, sg, h * Rf))
    st = Stats()
    tabs = TabCache(u, 4)
    nlev = 0
    minsl = (INF, None)
    cs_rng = [INF, -INF]
    case2 = 0
    for (B, sg, R) in triples:
        Rp = h if R == INF else R * h / (h + R)
        n1 = first_n(fm, Rp)
        ns = sorted(set([n1, n1 + 1, n1 + 7, 2 * n1, 5 * n1] + [n for n in (1000, 10000, 100000, 1000000) if n >= n1]))
        ns = [n for n in ns if n <= 1000000]
        if len(triples) > 60 and R != INF and R < h / 20:
            ns = ns[:4]                                    # the dimensions are large there; keep the run short
        for n in ns:
            X0 = fm.X0(n)
            top = Rp * n
            xset = sorted(set([X0, X0 + 1e-9, X0 + 0.5, float(math.ceil(X0)), 0.5 * (X0 + top), top - 1e-9, top]))
            xset = [x for x in xset if X0 <= x <= top]
            for xh in xset:
                for ld in (math.log(0.999), math.log(0.05), math.log(1e-12), -float(n), -50.0 * n):
                    for ename, ef in EFUNS.items():
                        if ename != 'E=0' and (n not in (ns[0], ns[-1]) or ld not in (math.log(0.05), -float(n))):
                            continue
                        inner = Synthetic(cu, st, fm, B, sg, R, ef, tag=ename)
                        S = Slope(cu, tabs, st, fm, inner)
                        before = st.min_q6
                        st.min_q6 = INF
                        lcm = S.level(n, xh, ld)
                        nlev += 1
                        if st.min_q6 < minsl[0]:
                            minsl = (st.min_q6, (round(B / h, 3), round(sg, 3), (R / h if R < INF else INF), n, round(xh, 4), round(ld, 2), ename))
                        st.min_q6 = min(before, st.min_q6)
                        cS = fm.cS(n, -ld + n * LN2, B)
                        cs_rng = [min(cs_rng[0], cS), max(cs_rng[1], cS)]
                        n_o = math.floor((xh - 1 - fm.clog(n)) / h + 1e-12)
                        if math.ceil(2 * u * (n - n_o)) - 1 < xh:
                            case2 += 1
    print("  %.1f   %4d   %7d   %4d   %8.3f at %s   [%.0f, %.0f]   %.4f   %.1e   %d   [%.0f s]"
          % (u, len(triples), nlev, len(st.viol), minsl[0], minsl[1], cs_rng[0], cs_rng[1], st.min_q4, st.max_xout_err, case2, time.time() - t0))
    for v in st.viol[:10]:
        print("     VIOLATION: " + v)
    sys.stdout.flush()
    grand += nlev
    grand_viol += len(st.viol)
print("# Part A total: %d levels, %d violations" % (grand, grand_viol))

# -------------------------------------------------------------------------------------------- Part B
print("\n# Part B: Proposition Q7 (drop) with a saturating inner family (slope one on (0, R))")
print("#  u    levels with shift / without   violations   least slack with shift at (B/h, R/h, c, alpha, n, ln delta, E)"
      "   least slack without shift   range of c_D   least slack of Lemma Q3   pass-through cases checked (n phi B <= c_D)")
grand = 0
grand_viol = 0
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    cu = Cube(u)
    fm = Formula(cu)
    h, a = cu.h, cu.a
    st = Stats()
    tabs = TabCache(u, 6)
    nshift = nnos = npass = 0
    mins = (INF, None)
    minn = (INF, None)
    cd_rng = [INF, -INF]
    for Bf in (1.0, a / h, 3 * a / h):
        B = h * Bf
        for Rf in (1.0, 0.5, 1 / 7, 1 / 100):
            R = h * Rf
            phi = R / (a + R)
            for cc in (1 / 3, 1 / 26, 1e-2, 1e-4, 1e-8):
                w = fm.w(cc)
                for alpha in (1.0, 0.5, min(1.0, 1.5 * w), min(1.0, 1.0001 * w)):
                    if alpha - w <= 0:
                        continue
                    ns = list(range(2, 201)) + [300, 500, 1000, 3000, 10000, 30000, 100000, 300000, 1000000]
                    if Rf < 0.2:
                        ns = [n for n in ns if n >= 100 or n % 20 == 0]
                    if Bf != a / h or cc in (1e-2,):
                        ns = [n for n in ns if n <= 200 and n % 3 == 0] + [1000, 100000]
                    for n in ns:
                        for ld in (math.log(0.999), math.log(0.05), math.log(1e-12), -float(n)):
                            if n > 200 and ld == math.log(1e-12):
                                continue
                            for ename, ef in EFUNS.items():
                                if ename != 'E=0' and (ld != math.log(0.05) or n % 50 != 0):
                                    continue
                                inner = Synthetic(cu, st, fm, B, 1.0, R, ef, xmin=0.0, tag=ename)
                                D = Drop(cu, tabs, st, fm, inner, cc, alpha)
                                Lam = -ld + n * LN2
                                cD = fm.cD(n, Lam, B, R, cc)
                                ok_n = n >= fm.nDp(cc)
                                no_s = math.floor(phi * n - fm.varsigma(n, cc, R))
                                no_n = math.floor(phi * n)
                                if ok_n and no_s >= 1:
                                    st.min_q7 = INF
                                    D.level(n, no_s, ld, True)
                                    nshift += 1
                                    cd_rng = [min(cd_rng[0], cD), max(cd_rng[1], cD)]
                                    if st.min_q7 < mins[0]:
                                        mins = (st.min_q7, (round(Bf, 3), round(Rf, 4), cc, round(alpha, 5), n, round(ld, 2), ename))
                                else:
                                    npass += 1
                                    if n * phi * B > cD + 1e-9:
                                        st.bad("pass-through: n phi B = %.4f > c_D = %.4f at n=%d" % (n * phi * B, cD, n))
                                if ok_n and no_n >= 1:
                                    st.min_q7ns = INF
                                    D.level(n, no_n, ld, False)
                                    nnos += 1
                                    if st.min_q7ns < minn[0]:
                                        minn = (st.min_q7ns, (round(Bf, 3), round(Rf, 4), cc, round(alpha, 5), n, round(ld, 2), ename))
    print("  %.1f   %6d / %6d   %4d   %8.3f at %s   %8.3f at %s   [%.0f, %.0f]   %.3f   %d   [%.0f s]"
          % (u, nshift, nnos, len(st.viol), mins[0], mins[1], minn[0], minn[1], cd_rng[0], cd_rng[1], st.min_q3, npass, time.time() - t0))
    for v in st.viol[:10]:
        print("     VIOLATION: " + v)
    sys.stdout.flush()
    grand += nshift + nnos
    grand_viol += len(st.viol)
print("# Part B total: %d levels, %d violations" % (grand, grand_viol))

# -------------------------------------------------------------------------------------------- Part C
print("\n# Part C: small facts")
# w(c) <= 6.25 c, and the numerical constants of Q7(3), on a fine grid of c in (0, 1/3]
cs_ = np.concatenate((np.logspace(-7, -2, 400), np.linspace(0.01, 1 / 3, 4000)))        # below 1e-7 float64 cannot resolve w(c)/c
w = np.log(np.exp(cs_) * (1 + cs_) / (1 - cs_) + 2 * cs_) + cs_
print("  max of w(c)/c on [1e-7, 1/3]: %.5f (claimed <= 6.25; the supremum, at c -> 0, is 6);  w(1/3) = %.4f" % (float(np.max(w / cs_)), float(w[-1])))
print("  max (e^c-1)/c = %.5f (<= 1.2);  1/(1-c) = %.3f (<= 1.5);  2(1+c)e^c/(1-c) = %.4f (<= 5.6);  2(1+c)^2 e^c/(1-c) = %.4f (<= 7.45);"
      "  4(1+c)e^c/(1-c) = %.4f (<= 11.17);  3(1+c) = %.3f (<= 4)"
      % (float(np.max(np.expm1(cs_) / cs_)), float(np.max(1 / (1 - cs_))), float(np.max(2 * (1 + cs_) * np.exp(cs_) / (1 - cs_))),
         float(np.max(2 * (1 + cs_) ** 2 * np.exp(cs_) / (1 - cs_))), float(np.max(4 * (1 + cs_) * np.exp(cs_) / (1 - cs_))),
         float(np.max(3 * (1 + cs_)))))
print("  min of (1 - e^{-c}) - 5c/6 on (0,1/3]: %.3e (>= 0 needed);  max of ln((1+c)/(1-c)) - 2.25c: %.3e (<= 0 needed)"
      % (float(np.min(-np.expm1(-cs_) - 5 * cs_ / 6)), float(np.max(np.log((1 + cs_) / (1 - cs_)) - 2.25 * cs_))))
bad = 0
worst_F4 = INF
for u in np.concatenate((np.logspace(-3, 0, 60), np.linspace(1, 40, 200))):
    cu = Cube(float(u))
    if not (0 < cu.h < cu.a < LN2 and cu.h <= u * u / 16 * (1 + 1e-9) + 1e-18 and cu.h <= u and cu.p < cu.rho_h < 0.5):
        bad += 1
    if abs(kl(cu.rho_h, cu.p) - cu.h) > 1e-12 or abs(cu.theta_na(cu.h) - cu.h) > 1e-9:
        bad += 1
    # (F4): a - theta_na(t) <= u sqrt(t/2); convexity on a grid
    ts = np.linspace(0, cu.eps_star * 1.2, 60)
    th = np.array([cu.theta_na(float(t)) for t in ts])
    worst_F4 = min(worst_F4, float(np.min(u * np.sqrt(ts / 2) - (cu.a - th))))
    if np.any(np.diff(th) > 1e-12) or np.any(np.diff(th, 2) < -1e-9):
        bad += 1
    # the epoch arithmetic (R) and B_{m+1} = B_m J_m a/(J_m a + h)
    ep = cu.epochs(30)
    for m in range(30):
        d, J, k, B = ep['d'][m], ep['J'][m], ep['k'][m], ep['B'][m]
        if d < 1e12 and not (d <= J < d + 1 and J * cu.a - cu.h * d > 0):      # beyond 1e12 float64 cannot tell J from d + 1
            bad += 1
        if ep['d'][m + 1] - d < (J + 1) * cu.kappa * (1 - 1e-12):
            bad += 1
        if abs(ep['B'][m + 1] - B * J * cu.a / (J * cu.a + cu.h)) > 1e-12 * B:
            bad += 1
        for kk in (k, ep['k'][m + 1] - 1):
            if cu.h / d > cu.c1 / (kk + cu.c2) * (1 + 1e-12):
                bad += 1
        if ep['k'][m + 1] > (1 + cu.rbar) * k * (1 + 1e-12):
            bad += 1
print("  260 slopes u in [0.001, 40]: (F2), (F3) (h <= u^2/16, h <= u, 0 < h < a < ln 2), theta_na(h) = h, (F4) (convex, nonincreasing,"
      " a - theta_na(t) <= u sqrt(t/2): least slack %.2e), (R) for 30 epochs, B_{m+1} = B_m J_m a/(J_m a + h), k_{m+1} <= (1 + rbar) k_m:"
      " %d failures" % (worst_F4, bad))
print("\n# done in %.0f s" % (time.time() - t0))
