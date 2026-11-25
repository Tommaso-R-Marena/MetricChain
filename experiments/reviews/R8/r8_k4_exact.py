#!/usr/bin/env python3
"""Referee R8 -- Lemma K.4 (a)-(d) and the binomial-median fact (Me) in EXACT arithmetic.

Own code, written from the statement of Lemma K.4 in the report (section 3.1) only.

e^u is taken rational (e^u = A/B), so that E_r(m), T_m(k), Gamma~, Gamma'', P(Bin(m,p_u)<=r)
are rational numbers; all comparisons of (a), (b) and (Me) are exact (python Fractions / ints).
The two places where an irrational function enters -- the Hoeffding bound exp(-2t^2/m) and the
radius r_+ (a floor of an expression with ln and sqrt) and the right-hand side of (d) -- are
evaluated with mpmath at 60 digits, and the distance of the argument of the floor from the
nearest integer is reported (so the floor is certain).

usage: python3 r8_k4_exact.py [quick]
"""
import sys, time
from fractions import Fraction as Fr
from math import comb
import mpmath as mp

mp.mp.dps = 60


def tables(m, A, B):
    """exact tables on Q_m for e^u = A/B: ball sizes, E_r, T_k as Fractions"""
    eu = Fr(A, B)
    C = [comb(m, j) for j in range(m + 1)]
    ball = [0] * (m + 2)          # ball[r+1] = |B(m,r)|, ball[0] = |B(m,-1)| = 0
    s = 0
    for j in range(m + 1):
        s += C[j]
        ball[j + 1] = s
    # E_r = sum_{j<=r} C(m,j) (e^{u(r+1-j)} - 1) ;  F_r = e^u (F_{r-1} + C(m,r))
    E = []
    F = Fr(0)
    for r in range(m + 1):
        F = eu * (F + C[r])
        E.append(F - ball[r + 1])
    # T_k = |B(k)| + G_k,  G_k = sum_{j>k} C(m,j) e^{-u(j-k)},  G_k = e^{-u}(C(m,k+1)+G_{k+1})
    T = [None] * (m + 1)
    G = Fr(0)
    T[m] = Fr(ball[m + 1])
    for k in range(m - 1, -1, -1):
        G = (C[k + 1] + G) / eu
        T[k] = ball[k + 1] + G
    return C, ball, E, T


def brute_ET(m, A, B, r, k):
    """direct evaluation of the two definitions (for the self-test)"""
    eu = Fr(A, B)
    E = sum(comb(m, j) * (eu ** (r + 1 - j) - 1) for j in range(0, r + 1))
    T = sum(comb(m, j) * (Fr(1) / eu ** max(j - k, 0)) for j in range(0, m + 1))
    return E, T


def kappa_table(m, ball, ceta):
    """kappa(r) = largest k>=0 with |B(m,k)| <= max(1, c_eta |B(m,r-1)|), r = 0..m"""
    kap = []
    k = 0
    for r in range(m + 1):
        bound = max(Fr(1), ceta * ball[r])     # ball[r] = |B(m,r-1)|
        while k + 1 <= m and ball[k + 2] <= bound:
            k += 1
        kap.append(k)
    return kap


def check(m, A, B, eta, thetas, out):
    """returns number of violations; out = dict of statistics"""
    eu = Fr(A, B)
    pu = Fr(B, A + B)
    C, ball, E, T = tables(m, A, B)
    ceta = (1 - eta) / (1 + eta)
    # m0 = ceil(ln(1/c_eta)/u) = least integer m0 with e^{u m0} >= 1/c_eta   (m0 >= 1)
    m0 = 1
    while eu ** m0 < 1 / ceta:
        m0 += 1
    kap = kappa_table(m, ball, ceta)
    viol = 0
    # Gamma tilde
    def gt(r):
        return eu - 1 if r == 0 else E[r] / ball[r]
    # (a)
    worst_a = Fr(0)
    r = 0
    while r <= m and r * (A + B) <= B * (m + 1):
        g = gt(r)
        ratio = g / (2 * eu * m)
        if ratio > worst_a:
            worst_a = ratio
        if g > 2 * eu * m:
            viol += 1
            print("VIOLATION (a)", m, A, B, r)
        r += 1
    out['a'] = max(out.get('a', 0.0), float(worst_a))
    # (b1) kappa(r) >= r-1-m0 for 1 <= r <= p_u(m+1)+1
    r = 1
    while r <= m and (r - 1) * (A + B) <= B * (m + 1):
        if kap[r] < r - 1 - m0:
            viol += 1
            print("VIOLATION (b1)", m, A, B, eta, r, kap[r], m0)
        r += 1
    # binomial law with p_u = B/(A+B): P(X=j) = C(m,j) B^j A^(m-j) / (A+B)^m
    den = (A + B) ** m
    cdf_num = []
    s = 0
    for j in range(m + 1):
        s += C[j] * B ** j * A ** (m - j)
        cdf_num.append(s)
    # (Me): P(Bin(m,p_u) >= k) >= 1/2 for every integer k <= m p_u   (enough: k = floor(m p_u))
    k = (m * B) // (A + B)
    tail_num = den - (cdf_num[k - 1] if k >= 1 else 0)
    if 2 * tail_num < den:
        viol += 1
        print("VIOLATION (Me)", m, A, B, k)
    out['me'] = min(out.get('me', 1.0), float(Fr(tail_num, den)))
    # (b2) Gamma''(r) <= 2 e^{u(m0+2)} P(Bin<=r)   and Hoeffding, for 0 <= r <= p_u m
    worst_b = 0.0
    Gpp = []
    r = 0
    while r <= m and r * (A + B) <= B * m:
        gpp = E[r] / T[kap[r]]
        P = Fr(cdf_num[r], den)
        rhs = 2 * eu ** (m0 + 2) * P
        if gpp > rhs:
            viol += 1
            print("VIOLATION (b2)", m, A, B, eta, r)
        worst_b = max(worst_b, float(gpp / rhs))
        # Hoeffding  P(Bin <= r) <= exp(-2 (p m - r)^2 / m)
        t = mp.mpf(m * B) / (A + B) - r
        hoef = mp.e ** (-2 * t * t / m)
        Pm = mp.mpf(cdf_num[r]) / mp.mpf(den)
        if Pm > hoef:
            viol += 1
            print("VIOLATION (Ho)", m, A, B, r)
        r += 1
    out['b'] = max(out.get('b', 0.0), worst_b)
    # (c), (d)
    u = mp.log(mp.mpf(A) / B)
    a = mp.log(2) + (mp.mpf(B) / (A + B)) * mp.log(mp.mpf(B) / (A + B)) + (mp.mpf(A) / (A + B)) * mp.log(mp.mpf(A) / (A + B))
    for theta in thetas:
        if theta > 2 * eu ** (m0 + 2):
            continue
        nu0min = 2 * eu * m / (theta * (1 - eta))      # the smallest nu_0 allowed in (c)
        # r_dagger: largest r in {0..m-1} with [N] and [P] for all r' <= r
        rd = -1
        for rr in range(0, m):
            g = gt(rr)
            okN = g <= theta * (1 - eta) * nu0min
            if not okN:
                break
            okP = (g / ceta <= theta) or (E[rr] / T[kap[rr]] <= theta)
            if not okP:
                break
            rd = rr
        root = mp.sqrt((mp.mpf(m) / 2) * mp.log(2 * (mp.mpf(A) / B) ** (m0 + 2) / mp.mpf(theta.numerator) * theta.denominator))
        val = mp.mpf(m * B) / (A + B) - root
        rplus = int(mp.floor(val))
        dist = float(min(val - mp.floor(val), mp.ceil(val) - val))
        out['floor_margin'] = min(out.get('floor_margin', 1.0), dist)
        if rplus >= 0:
            out['c_cases'] = out.get('c_cases', 0) + 1
            if rd < rplus:
                viol += 1
                print("VIOLATION (c)", m, A, B, eta, theta, rd, rplus)
            out['c_slack'] = min(out.get('c_slack', 10 ** 9), rd - rplus)
            if 2 * rplus * (A + B) >= m * B:      # r_+ >= p_u m / 2
                out['d_cases'] = out.get('d_cases', 0) + 1
                pidag = mp.mpf(ball[rd + 1]) / mp.mpf(2) ** m
                lhs = -mp.log(pidag)
                rhs = m * a + (u + mp.log(4)) * (1 + root) + mp.log(m + 1)
                if lhs > rhs:
                    viol += 1
                    print("VIOLATION (d)", m, A, B, eta, theta, float(lhs), float(rhs))
                out['d'] = max(out.get('d', -1e9), float(lhs - rhs))
                # how much of the O(sqrt m) is real:  (ln(1/pi) - m a)/sqrt(m)
                out['d_sqrt'] = max(out.get('d_sqrt', -1e9), float((lhs - m * a) / mp.sqrt(m)))
    return viol


def selftest():
    bad = 0
    for (A, B) in [(2, 1), (3, 2), (5, 4), (3, 1)]:
        for m in range(1, 13):
            C, ball, E, T = tables(m, A, B)
            for r in range(0, m + 1):
                e, t = brute_ET(m, A, B, r, r)
                if e != E[r] or t != T[r]:
                    bad += 1
            assert ball[m + 1] == 2 ** m and ball[0] == 0
    print("self-test of the tables against the definitions (m<=12, 4 values of e^u): mismatches =", bad)
    return bad


def main():
    quick = len(sys.argv) > 1 and sys.argv[1] == 'quick'
    t0 = time.time()
    assert selftest() == 0
    eus = [(5, 4), (3, 2), (2, 1), (3, 1), (8, 1)]            # e^u ; u = 0.223, 0.405, 0.693, 1.099, 2.079
    etas = [Fr(1, 2), Fr(1, 4), Fr(1, 10), Fr(1, 50)]
    thetas = [Fr(1, 100), Fr(1, 20), Fr(1, 3), Fr(1), Fr(5), Fr(40)]
    ms_all = list(range(1, 61 if quick else 161))
    ms_big = [250, 400, 700, 1000] if quick else [200, 250, 333, 400, 500, 700, 1000, 1500, 2000, 3000, 4000]
    total = 0
    for (A, B) in eus:
        for eta in etas:
            out = {}
            v = 0
            nm = 0
            for m in ms_all + ms_big:
                if m > 1000 and eta != Fr(1, 4) and eta != Fr(1, 2):
                    continue
                v += check(m, A, B, eta, thetas, out)
                nm += 1
            total += v
            print("e^u=%d/%d eta=%s: %d values of m (max %d), violations=%d | max Gt/(2e^u m)=%.3f  "
                  "max G''/bound=%.3f  min P(Bin>=floor(mp))=%.4f | (c): %d cases, min(r_dag-r_plus)=%s | "
                  "(d): %d cases, max(lhs-rhs)=%.3f, max (ln(1/pi_dag)-ma)/sqrt(m)=%.3f | floor margin %.2e  [%.0fs]"
                  % (A, B, eta, nm, max(ms_all + ms_big), v, out.get('a', 0), out.get('b', 0), out.get('me', 1),
                     out.get('c_cases', 0), out.get('c_slack'), out.get('d_cases', 0), out.get('d', float('nan')),
                     out.get('d_sqrt', float('nan')), out.get('floor_margin', 1), time.time() - t0))
            sys.stdout.flush()
    print("TOTAL VIOLATIONS:", total)


if __name__ == '__main__':
    main()
