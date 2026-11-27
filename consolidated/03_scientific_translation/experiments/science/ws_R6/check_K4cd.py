"""
check_K4cd.py -- workstream R6: Lemma K.4 (= Lemma 11.55) parts (c), (d) and the binomial-median fact (Me) on exact tables.
(c) if 0 < theta <= 2e^{u(m0+2)} and nu0 >= 2e^u m/(theta(1-eta)) then r-dagger >= r_+ := floor(p_u m - sqrt((m/2) ln(2e^{u(m0+2)}/theta))) (if r_+ >= 0)
(d) if moreover r_+ >= p_u m/2:  ln(1/pi-dagger) <= m a + (u + ln 4)(1 + sqrt((m/2) ln(2e^{u(m0+2)}/theta))) + ln(m+1)
(Me) P(Bin(m, p_u) >= k) >= 1/2 for every integer k <= m p_u
"""
import math
from fractions import Fraction
import mpmath as mp
import r6lib as R

mp.mp.dps = 40
viol = cases_c = cases_d = cases_me = 0
worst_c = 10 ** 9
worst_d = -1e9
min_me = 1.0
for u in (0.5, 1.0, 2.0):
    pu = mp.mpf(1) / (1 + mp.e ** u)
    a = mp.log(2) + pu * mp.log(pu) + (1 - pu) * mp.log(1 - pu)
    for m in (10, 30, 60, 120, 250, 500, 1000, 2000, 4000):
        tab = R.Tables(m, u)
        # (Me)
        logpm = [mp.log(tab.binom[j]) + j * mp.log(pu) + (m - j) * mp.log(1 - pu) for j in range(0, int(pu * m) + 2)]
        k = int(mp.floor(pu * m))
        lower = mp.fsum(mp.e ** x for x in logpm[:k])          # P(Bin <= k-1)
        pge = 1 - lower
        cases_me += 1
        min_me = min(min_me, float(pge))
        if pge < mp.mpf(1) / 2:
            viol += 1
        for eta in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 12), Fraction(1, 20)):
            ef = mp.mpf(eta.numerator) / eta.denominator
            c_eta = (1 - ef) / (1 + ef)
            m0 = int(mp.ceil(mp.log(1 / c_eta) / u))
            for theta in (mp.mpf(1) / 100, mp.mpf(1) / 20, mp.mpf(1) / 3, mp.mpf(1), mp.mpf(5)):
                if theta > 2 * mp.e ** (u * (m0 + 2)):
                    continue
                nu0 = 2 * mp.e ** u * m / (theta * (1 - ef))          # the smallest allowed
                root = mp.sqrt(mp.mpf(m) / 2 * mp.log(2 * mp.e ** (u * (m0 + 2)) / theta))
                rplus = int(mp.floor(pu * m - root))
                if rplus < 0:
                    continue
                rd = -1
                for r in range(0, m):
                    gt = tab.gamma_tilde(r)
                    if gt <= theta * (1 - ef) * nu0 and min(gt / c_eta, tab.gamma_pp(r, eta)) <= theta:
                        rd = r
                    else:
                        break
                cases_c += 1
                worst_c = min(worst_c, rd - rplus)
                if rd < rplus:
                    viol += 1
                if rplus >= pu * m / 2:
                    lhs = mp.log(mp.mpf(tab.two_m) / tab.ball[rd])
                    rhs = m * a + (u + mp.log(4)) * (1 + root) + mp.log(m + 1)
                    cases_d += 1
                    worst_d = max(worst_d, float(lhs - rhs))
                    if lhs > rhs:
                        viol += 1
print("Lemma K.4(c): %d cases, min(r-dagger - r_+) = %d;  (d): %d cases, max(lhs - rhs) = %.2f;  (Me): %d cases, min P(Bin >= floor(m p_u)) = %.5f;  violations: %d"
      % (cases_c, worst_c, cases_d, worst_d, cases_me, min_me, viol))
