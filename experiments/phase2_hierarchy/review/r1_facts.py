"""Review item 1a: the elementary facts (F1)-(F4), (R) of section 1, checked exactly.

For every slope u in a list and every block size n_j in a range (starting at N_u) every integer d
is checked with exact binomial costs.  L is taken as ln(n_j + 1) (<= ln(n + 1), so this is the
harder version of each inequality).  Also checked: the auxiliary numerical claims used inside the
proof of Lemma B (t_j(w_j) <= ln 3 for w_j in {d*, d*-1}; jumps of t_j at most L; t_j(k_j) <= n_j h + L).
"""
import math
import sys
import numpy as np
from rv_common import consts, fKL, kKL, tcost

EPS = 1e-9


def check_block(n, c, viol):
    u, pu, Lam, kap, h = c['u'], c['pu'], c['Lam'], c['kap'], c['h']
    t = tcost(n)
    L = math.log(n + 1.0)
    d = np.arange(n + 1)
    dstar = n // 2
    fvals = np.array([fKL(x / n) for x in d])
    # (F1)
    dev = np.max(np.abs(t - n * fvals))
    if dev > L + EPS:
        viol.append(('F1 bound', u, n, dev, L))
    if np.max(np.abs(t - t[::-1])) > 1e-9:
        viol.append(('F1 symmetry', u, n))
    if np.any(np.diff(t[:dstar + 1]) > EPS):
        viol.append(('F1 monotone', u, n))
    if t.min() < -EPS:
        viol.append(('t >= 0', u, n))
    # (F2)
    gam = t + u * d
    slack2 = np.min(gam) - (n * Lam - L)
    if slack2 < -EPS:
        viol.append(('F2', u, n, slack2))
    # (F3): gamma nonincreasing along integers y <= e <= (n+1) p_u
    emax = int(math.floor((n + 1) * pu + 1e-12))
    if emax >= 1:
        if np.any(np.diff(gam[:emax + 1]) > EPS):
            viol.append(('F3', u, n))
    # (F4)
    kj = int(math.ceil(kap * n - 1e-12))
    ok_k = kj <= dstar - 1
    if not ok_k:
        viol.append(('F4 k_j <= d*-1', u, n, kj, dstar))
    worst4a = -1e300
    worst4b = -1e300
    for e in range(emax + 1, kj + 1):
        kk = kKL(e / n, u)
        v1 = gam[e] - (n * (Lam + kk) + L)
        v2 = (n * (Lam + kk) + L) - (n * Lam + n * h + u + L)
        worst4a = max(worst4a, v1)
        worst4b = max(worst4b, v2)
    if worst4a > EPS:
        viol.append(('F4 first', u, n, worst4a))
    if worst4b > EPS:
        viol.append(('F4 second', u, n, worst4b))
    # (R): max over y <= e <= k_j of gamma(e) - gamma(y)
    pref = np.minimum.accumulate(gam[:kj + 1])
    worstR = np.max(gam[:kj + 1] - pref)
    slackR = (n * h + u + 2 * L) - worstR
    if slackR < -EPS:
        viol.append(('R', u, n, worstR, n * h + u + 2 * L))
    # auxiliary claims of the proof of Lemma B
    if dstar >= 1 and max(t[dstar], t[dstar - 1]) > math.log(3.0) + EPS:
        viol.append(('t(w) <= ln 3', u, n))
    if np.max(np.abs(np.diff(t))) > L + EPS:
        viol.append(('jump <= L', u, n))
    if t[kj] > n * h + L + EPS:
        viol.append(('t(k_j) <= n h + L', u, n, t[kj], n * h + L))
    return dev / L, slack2, worstR - n * h, slackR


def main():
    us = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 20.0]
    nmax = 2500
    viol = []
    print('# (F1)-(F4), (R): exact check, every d, block sizes N_u .. %d' % nmax)
    print('# u, N_u, kappa, h, a | max |t - n f|/L | min slack in (F2) | max_{y<=e<=k} [gamma(e)-gamma(y)] - n h | min slack in (R)')
    for u in us:
        c = consts(u)
        Nu = c['Nu']
        m1 = 0.0
        m2 = 1e300
        m3 = -1e300
        m4 = 1e300
        n = Nu
        cnt = 0
        while n <= nmax:
            r = check_block(n, c, viol)
            m1 = max(m1, r[0])
            m2 = min(m2, r[1])
            m3 = max(m3, r[2])
            m4 = min(m4, r[3])
            cnt += 1
            # all sizes up to 400, then a sparser sweep
            n += 1 if n < 400 else 37
        print('u=%5.2f N_u=%4d kappa=%.5f h=%.6f a=%.6f | %.4f | %.4f | %.4f | %.4f   (%d block sizes)'
              % (u, Nu, c['kap'], c['h'], c['a'], m1, m2, m3, m4, cnt))
    # is N_u needed?  smallest n for which k_j <= d*-1 fails below N_u
    print('# below N_u: block sizes n < N_u with k_j > d*-1 (so (F4)/(R) would be used outside their range)')
    for u in us:
        c = consts(u)
        bad = [n for n in range(1, c['Nu']) if int(math.ceil(c['kap'] * n - 1e-12)) > n // 2 - 1]
        print('u=%5.2f N_u=%d  sizes with k_j > d*-1: %s' % (u, c['Nu'], bad if len(bad) < 30 else str(bad[:30]) + '...'))
    print('violations:', len(viol))
    for v in viol[:50]:
        print('  ', v)
    return 0 if not viol else 1


if __name__ == '__main__':
    sys.exit(main())
