#!/usr/bin/env python3
"""Reviewer's finite-n checks of the proof of Theorem H6 (HIERARCHY_ADDENDUM.md, section A4).  Own code.

  S  the elementary bounds (S), (U), (B)
  I  the inequalities (1) and (2) with exact binomial probabilities, random fine classes (sizes down to 1)
  E  step (e) carried out literally: the real-type construction, the rounding E', M'', P'', BOTH exchange paths with
     the hypotheses of (X2) and (X1) evaluated exactly at every single exchange, and the final inequality
  Q  unbiasedness of the output for an arbitrary partition G2, exhaustively on Q_10; never-separated classes
  N  the smallest n for which all "for large n" of the proof hold (explicit n_0), and Remark 1 (m growing)
"""
import sys, time
import numpy as np
from scipy.special import gammaln
from scipy.stats import binom
from p1_chain import f, consts, rate, cost, dist, chain, random_y, LN2


def lnbin(N, k):
    """ln [ C(N,k) 2^-N ]"""
    return gammaln(N + 1.0) - gammaln(k + 1.0) - gammaln(N - k + 1.0) - N * LN2


# ------------------------------------------------------------------ S
def part_S():
    print("PART S: elementary bounds")
    w = -np.inf
    for N in range(1, 801):
        a = np.arange(N + 1)
        mid = N * LN2 - (gammaln(N + 1.0) - gammaln(a + 1.0) - gammaln(N - a + 1.0))
        lo = N * f(a / N)
        w = max(w, float(np.max(lo - mid)), float(np.max(mid - lo - np.log(N + 1.0))))
    print("   (S) N f(a/N) <= N ln2 - ln C(N,a) <= N f(a/N) + ln(N+1), N = 1..800, all a:   worst violation %+.2e" % w)
    w2 = -np.inf
    rng = np.random.default_rng(1)
    for N in (1, 2, 3, 4, 7, 10, 30, 100, 1000, 10 ** 4, 10 ** 6):
        t = np.concatenate([np.linspace(0, 1, 20001), rng.random(20000), [0.0, 1.0, 1.0 / N, 1 - 1.0 / N]])
        for frac in (1.0, 0.5, 0.1):
            tp = np.clip(t + frac / N, 0, 1)
            tm = np.clip(t - frac / N, 0, 1)
            w2 = max(w2, float(np.max(N * np.abs(f(tp) - f(t)) - (np.log(N + 1.0) + 1))),
                     float(np.max(N * np.abs(f(tm) - f(t)) - (np.log(N + 1.0) + 1))))
    print("   (U) N|f(t) - f(t')| <= ln(N+1) + 1 for |t - t'| <= 1/N, N = 1..10^6:             worst violation %+.2e" % w2)
    w3 = -np.inf
    for M in (1, 2, 3, 5, 10, 37, 100, 1000, 10 ** 5):
        for p in np.concatenate([np.logspace(-6, 0, 61), np.linspace(0.01, 1, 100)]):
            # P[Bin < Mp/2] = P[Bin <= ceil(Mp/2) - 1]
            w3 = max(w3, float(binom.cdf(np.ceil(M * p / 2) - 1, M, p) - np.exp(-M * p / 8)),
                     float((1 - p) ** M - np.exp(-M * p)))
    print("   (B) P[Bin(M,p) < Mp/2] <= e^{-Mp/8},  P[Bin(M,p) = 0] <= e^{-Mp}:                 worst violation %+.2e" % w3)
    return max(w, w2, w3) <= 1e-9


# ------------------------------------------------------------------ instances for I and E
def instance(rng, m, n):
    """fine classes = nonempty (cell of G2) x (true class); returns sizes and the three labelings"""
    mt = int(rng.integers(2, m + 1))
    g1 = int(rng.integers(1, m + 1))
    sub = [int(rng.integers(1, m + 1)) for _ in range(g1)]
    c1_of_c2 = np.repeat(np.arange(g1), sub)
    g2 = len(c1_of_c2)
    cls = [(g, j) for g in range(g2) for j in range(mt) if rng.random() < 0.7]
    for g in range(g2):
        if not any(c[0] == g for c in cls):
            cls.append((g, int(rng.integers(mt))))
    cls.sort()
    Dp = len(cls)
    prop = rng.dirichlet(np.full(Dp, 0.7))
    sizes = np.maximum(1, np.round(prop * n)).astype(np.int64)
    tiny = rng.random(Dp) < 0.15
    sizes[tiny] = rng.integers(1, 4, size=int(tiny.sum()))
    cell2 = np.array([c[0] for c in cls])
    true = np.array([c[1] for c in cls])
    cell1 = c1_of_c2[cell2]
    return dict(m=m, sizes=sizes, n=int(sizes.sum()), cell2=cell2, cell1=cell1, true=true, g1=g1, g2=g2, mt=mt,
                G2=[[int(i) for i in np.flatnonzero(cell2 == g)] for g in range(g2)],
                G1=[[int(i) for i in np.flatnonzero(cell1 == g)] for g in range(g1)])


class Prob:
    def __init__(self, I):
        self.I = I
        s = I['sizes'].astype(float)
        self.s = s
        self.lab11 = I['cell1'] * I['mt'] + I['true']
        self.N_true = np.bincount(I['true'], weights=s, minlength=I['mt'])
        self.N_2 = np.bincount(I['cell2'], weights=s, minlength=I['g2'])
        self.N_1 = np.bincount(I['cell1'], weights=s, minlength=I['g1'])
        self.N_11 = np.bincount(self.lab11, weights=s, minlength=I['g1'] * I['mt'])

    def fine(self, k):
        return float(np.sum(lnbin(self.s, k)))

    def true(self, k):
        return float(np.sum(lnbin(self.N_true, np.bincount(self.I['true'], weights=k, minlength=len(self.N_true)))))

    def pi2(self, k):
        return float(np.sum(lnbin(self.N_2, np.bincount(self.I['cell2'], weights=k, minlength=len(self.N_2)))))

    def pi1(self, k):
        return float(np.sum(lnbin(self.N_1, np.bincount(self.I['cell1'], weights=k, minlength=len(self.N_1)))))

    def c1type(self, k):
        return float(np.sum(lnbin(self.N_11, np.bincount(self.lab11, weights=k, minlength=len(self.N_11)))))


def part_I():
    print("PART I: inequalities (1), (2) with exact binomials (D = m^3, L = ln(n+1)); 'worst' = largest violation, must be <= 0")
    rng = np.random.default_rng(5)
    w = {k: -np.inf for k in ('1a', '1b', '1c', '1d', '1e', '1f', '2r', '2c1', '2c2')}
    used = -np.inf
    for it in range(6000):
        m = int(rng.integers(2, 5))
        n = int(rng.choice([30, 100, 1000, 20000]))
        I = instance(rng, m, n)
        n = I['n']
        P = Prob(I)
        s = P.s
        wts = s / n
        D = m ** 3
        L = np.log(n + 1.0)
        mode = rng.integers(3)
        k = (rng.integers(0, I['sizes'] + 1) if mode == 0 else
             np.round(s * rng.choice([0, 1, 0.5, 0.1, 0.9], size=len(s))) if mode == 1 else rng.binomial(I['sizes'], 0.5)).astype(float)
        z = k / s
        nr = n * rate(z, wts)
        nc1 = n * cost(z, wts, I['G1'])
        nc2 = n * cost(z, wts, I['G2'])
        lf, lt = -P.fine(k), -P.true(k)
        lkb = lf + P.pi2(k)
        l1a = -P.c1type(k) + P.pi1(k)
        w['1a'] = max(w['1a'], nr - lf)
        w['1b'] = max(w['1b'], lf - nr - D * L)
        w['1c'] = max(w['1c'], lt - nr - D * L)
        w['1d'] = max(w['1d'], nc2 - D * L - lkb)
        w['1e'] = max(w['1e'], lkb - nc2 - D * L)
        w['1f'] = max(w['1f'], l1a - nc1 - D * L)
        used = max(used, (lf - nr) / (D * L), (lkb - nc2) / (D * L), (nc2 - lkb) / (D * L))
        rho = int(rng.integers(1, 4))
        zs = np.clip((k + rho * rng.uniform(-1, 1, size=len(s))) / s, 0, 1)
        w['2r'] = max(w['2r'], abs(nr - n * rate(zs, wts)) - D * rho * (L + 1))
        w['2c1'] = max(w['2c1'], abs(nc1 - n * cost(zs, wts, I['G1'])) - 2 * D * rho * (L + 1))
        w['2c2'] = max(w['2c2'], abs(nc2 - n * cost(zs, wts, I['G2'])) - 2 * D * rho * (L + 1))
    names = {'1a': "n r <= -ln P(k)", '1b': "-ln P(k) <= n r + DL", '1c': "-ln P(kappa(k)) <= n r + DL",
             '1d': "n cost_2 - DL <= -ln P(k|b)", '1e': "-ln P(k|b) <= n cost_2 + DL", '1f': "-ln P(k^1|a) <= n cost_1 + DL",
             '2r': "|n r(z(k)) - n r(z*)| <= D rho (L+1)", '2c1': "|n cost_1(z(k)) - n cost_1(z*)| <= 2 D rho (L+1)",
             '2c2': "|n cost_2(z(k)) - n cost_2(z*)| <= 2 D rho (L+1)"}
    for k_ in w:
        print("   %-48s worst %+.3e" % (names[k_], w[k_]))
    print("   largest fraction of the allowance DL actually used in (1): %.3f" % used)
    return max(w.values()) <= 1e-7


# ------------------------------------------------------------------ E
def round_to_sum(x, cells, sums, sizes):
    k = np.floor(x + 1e-9).astype(np.int64)
    for g, Bg in zip(cells, sums):
        deficit = int(Bg - k[g].sum())
        assert deficit >= 0, "cell sum below all floors"
        cand = sorted([c for c in g if x[c] - k[c] > 1e-9], key=lambda c: -(x[c] - k[c]))
        assert deficit <= len(cand), "cell sum above all ceilings"
        for c in cand[:deficit]:
            k[c] += 1
    assert np.all(k >= 0) and np.all(k <= sizes)
    return k


def exchanges(k0, k1, cells, rng):
    """single exchanges inside the cells, every coordinate moving monotonically from k0 to k1 (random order)"""
    k = k0.copy()
    for g in cells:
        assert k[g].sum() == k1[g].sum()
        up = [c for c in g if k[c] < k1[c]]
        dn = [c for c in g if k[c] > k1[c]]
        while up:
            d = up[int(rng.integers(len(up)))]
            dp = dn[int(rng.integers(len(dn)))]
            yield k, d, dp
            k[d] += 1
            k[dp] -= 1
            if k[d] == k1[d]:
                up.remove(d)
            if k[dp] == k1[dp]:
                dn.remove(dp)
        assert not dn
    assert np.array_equal(k, k1)


def conditions(u, m, n, eta, delta=0.1):
    """the 'for large n' requirements of the proof; returns the list of slacks (all must be >= 0)"""
    pu, L1, kap, h, a = consts(u)
    D = m ** 3
    rho0 = m * m + 2
    L = np.log(n + 1.0)
    Theta = n * (h + eta / 2)
    lnM = Theta + eta * n / 4
    c = []
    c.append(n * (h + eta) - (np.log(3.0) + (m * m + 1) * L + lnM + np.log1p(np.exp(-min(lnM, 700)))))      # (a) cost
    t = np.exp(min(eta * n / 4, 700.0))
    lnfail12 = np.log(2.0) + (m * m + 2) * L - t / n ** 2
    lnfail3 = D * L - t / 8
    c.append(np.log(delta / 2) - np.logaddexp(lnfail12, lnfail3))                                            # (b) events
    c.append(Theta - 9 * D * (L + 1) - n * h)                                                                # theta_c >= h
    c.append(Theta - D * L - (n * h + D * (rho0 + 2) * (L + 1)))                                             # core visible to round 1
    c.append(eta * n / 2 - D * (rho0 + 10) * (L + 1) - u * D - 2 * D * L)                                    # A_hid <= A_vis
    c.append(Theta - D * L - m * L)                                                                          # nu_0 well defined
    return c


def part_E():
    print("PART E: step (e) literally (real types -> rounding -> two exchange paths -> final inequality), exact binomials")
    rng = np.random.default_rng(9)
    settings = [(1.0, 2, 20000, 0.2, 14), (4.0, 2, 20000, 0.2, 14), (2.0, 2, 60000, 0.1, 6), (2.0, 3, 110000, 0.2, 5), (4.0, 3, 110000, 0.2, 5)]
    allok = True
    for u, m, n0, eta, want in (settings if len(sys.argv) < 3 else [settings[int(sys.argv[2])]]):
        pu, L1, kap, h, a = consts(u)
        D = m ** 3
        rho0 = m * m + 2
        W = dict(four=-np.inf, x2=-np.inf, x1=-np.inf, c2=-np.inf, c1=-np.inf, rt=-np.inf, near=-np.inf, vis=-np.inf, fin=-np.inf,
                 dE=-np.inf, pP=-np.inf)
        used = -np.inf
        done = 0
        nx2 = nx1 = 0
        tries = 0
        t0 = time.time()
        while done < want and tries < 4000 and time.time() - t0 < 110:
            tries += 1
            I = instance(rng, m, n0)
            n = I['n']
            if min(conditions(u, m, n, eta)) < 0:
                continue
            P = Prob(I)
            s = P.s
            sizes = I['sizes']
            wts = s / n
            L = np.log(n + 1.0)
            Theta = n * (h + eta / 2)
            yd = random_y(rng, len(s), u, I['G2'], int(rng.choice([1, 2, 2, 3, 4])))
            y = np.round(s * yd)
            if not (-(P.fine(y) - P.pi2(y)) > Theta):          # y must be outside V
                continue
            yh = y / s
            thc = (Theta - 9 * D * (L + 1)) / n
            assert thc >= h and cost(yh, wts, I['G2']) > thc
            out, c = chain(yh, wts, I['G1'], I['G2'], u, thc)
            e_, mp, p = c['ep'], c['mp'], c['p']
            W['four'] = max(W['four'], out['vis'], out['core'], out['mean'], out['B'])                       # (4)
            # rounding
            B = np.array([int(np.rint(np.dot(s[g], mp[g]))) for g in I['G2']])
            E = round_to_sum(s * e_, I['G2'], B, sizes)
            Bc = np.empty(len(s))
            for g, Bg in zip(I['G2'], B):
                Bc[g] = Bg / s[g].sum()
            M2 = round_to_sum(s * Bc, I['G2'], B, sizes)
            A1 = np.array([int(M2[g].sum()) for g in I['G1']])
            Ac = np.empty(len(s))
            for g, Ag in zip(I['G1'], A1):
                Ac[g] = Ag / s[g].sum()
            P2 = round_to_sum(s * Ac, I['G1'], A1, sizes)
            W['near'] = max(W['near'], float(np.max(np.abs(E - s * e_))) - 1 - 1e-6, float(np.max(np.abs(M2 - s * mp))) - rho0,
                            float(np.max(np.abs(P2 - s * p))) - rho0)
            nc2_e = n * cost(e_, wts, I['G2'])
            # path E' -> M'' inside cells of G2 : hypothesis of (X2) at every exchange between different true classes
            for k, d, dp in exchanges(E, M2, I['G2'], rng):
                assert k[d] <= sizes[d] - 1 and k[dp] >= 1
                if I['true'][d] == I['true'][dp]:
                    continue
                nx2 += 1
                km = k.astype(float)
                km[dp] -= 1
                W['x2'] = max(W['x2'], -(P.c1type(km) - P.pi1(km)) - Theta)                                  # P(k^- | a(k^-)) >= e^-Theta
                if nx2 % 7 == 0:                                                                             # the intermediate claims
                    W['c2'] = max(W['c2'], n * cost(k / s, wts, I['G2']) - nc2_e - 4 * D * (L + 1))
                    W['c1'] = max(W['c1'], n * cost(km / s, wts, I['G1']) - n * thc - 8 * D * (L + 1))
            # path M'' -> P'' inside cells of G1 : hypothesis of (X1)
            for k, d, dp in exchanges(M2, P2, I['G1'], rng):
                assert k[d] <= sizes[d] - 1 and k[dp] >= 1
                if I['true'][d] == I['true'][dp]:
                    continue
                nx1 += 1
                km = k.astype(float)
                km[dp] -= 1
                lt = -P.true(km)
                W['x1'] = max(W['x1'], lt - Theta)                                                           # P(kappa(k) - e_j') >= e^-Theta
                W['rt'] = max(W['rt'], lt - (n * h + D * (rho0 + 2) * (L + 1)))
            W['vis'] = max(W['vis'], -P.true(P2.astype(float)) - (Theta - D * L))                            # P(kappa(P'')) >= e^{-Theta + DL}
            l1 = float(np.sum(np.abs(y - E)))
            W['dE'] = max(W['dE'], l1 - n * dist(yh, e_, wts) - D)
            W['pP'] = max(W['pP'], -P.fine(P2.astype(float)) - (n * rate(p, wts) + D * rho0 * (L + 1) + D * L))
            lhs = P.fine(y) - P.fine(P2.astype(float)) + u * l1
            W['fin'] = max(W['fin'], lhs - (n * h - Theta + D * (rho0 + 10) * (L + 1) + u * D))
            used = max(used, (lhs - (n * h - Theta)) / (D * (rho0 + 10) * (L + 1) + u * D))
            done += 1
        ok = max(W.values()) <= 1e-6 and done > 0
        allok &= ok
        print("   u=%g m=%d n~%d eta=%g: %d hidden types (%d draws), %d + %d exchanges between different true classes checked" % (u, m, n0, eta, done, tries, nx2, nx1))
        print("      (4) violated by %+.2e | rounding distances beyond the claims %+.2e | (X2) hypothesis: max[-ln P(k^-|a) - Theta] = %+.1f | (X1): max[-ln P(kappa - e_j') - Theta] = %+.1f"
              % (W['four'], W['near'], W['x2'], W['x1']))
        print("      claimed bounds: n cost_2 along path 1 %+.1f | n cost_1(k - e_d') %+.1f | rate along path 2 %+.1f | P(kappa(P'')) %+.1f | ||y-E'|| %+.1f | -ln P(P'') %+.1f | final %+.1f   (all must be <= 0)"
              % (W['c2'], W['c1'], W['rt'], W['vis'], W['dE'], W['pP'], W['fin']))
        print("      fraction of the error allowance D(rho_0+10)(L+1)+uD used by the final inequality: %+.3f   -> %s" % (used, "OK" if ok else "FAIL"))
        sys.stdout.flush()
    return allok


# ------------------------------------------------------------------ Q
def part_Q():
    print("PART Q: exhaustive check on Q_10: (i) sum_b pi(b) mean_{shell b} e^{-psi} = A for arbitrary partitions G2;")
    print("        (ii) two coordinates of one class of C are never separated; (iii) never-separated <=> psi invariant under the transposition")
    rng = np.random.default_rng(3)
    n = 10
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(np.int64)
    worst = 0.0
    bad = 0
    for it in range(300):
        m = int(rng.integers(2, 4))
        lab = rng.integers(0, m, size=n)
        u = float(rng.choice([0.5, 1.0, 3.0]))
        K = np.stack([X[:, lab == j].sum(1) for j in range(m)], 1)
        cen = rng.integers(0, n + 1, size=(4, m))
        off = rng.uniform(-3, 3, size=4)
        psi = np.min(off[None, :] + u * np.abs(K[:, None, :] - cen[None, :, :]).sum(2), axis=1)     # u-Lipschitz function of the counts
        A = np.mean(np.exp(-psi))
        g2 = rng.integers(0, int(rng.integers(1, 6)), size=n)
        cells = [np.flatnonzero(g2 == v) for v in np.unique(g2)]
        key = np.zeros(2 ** n, dtype=np.int64)
        for c in cells:
            key = key * (n + 1) + X[:, c].sum(1)
        est = 0.0
        for kv in np.unique(key):
            sel = key == kv
            est += sel.mean() * np.mean(np.exp(-psi[sel]))                                           # pi(b) = |shell|/2^n
        worst = max(worst, abs(est - A) / A)
        idx = np.arange(2 ** n)
        for i in range(n):
            for j in range(i + 1, n):
                same = X[:, i] == X[:, j]
                sep = np.any(psi[idx[same] ^ (1 << i)] != psi[idx[same] ^ (1 << j)])
                sw = idx.copy()
                diff = X[:, i] != X[:, j]
                sw[diff] = idx[diff] ^ (1 << i) ^ (1 << j)
                inv = np.array_equal(psi, psi[sw])
                if lab[i] == lab[j] and sep:
                    bad += 1
                if sep == inv:
                    bad += 1
    print("   300 random members of HP_3(Q_10): max relative error of the shell identity %.1e; violations of (ii)/(iii): %d" % (worst, bad))
    return worst < 1e-12 and bad == 0


# ------------------------------------------------------------------ N
def part_N():
    print("PART N: smallest n with all 'for large n' requirements of the proof (delta = 0.1); u = 1")
    for m in (2, 3, 4, 6):
        row = []
        for eta in (1.0, 0.1, 0.01):
            lo, hi = 2, 10 ** 13
            while hi - lo > 1:                      # all requirements are eventually monotone; bisect on the last failure
                mid = (lo + hi) // 2
                if min(conditions(1.0, m, mid, eta)) >= 0 and min(conditions(1.0, m, 2 * mid, eta)) >= 0:
                    hi = mid
                else:
                    lo = mid
            c = conditions(1.0, m, lo, eta)
            row.append("eta=%g: n0 ~ %.2e (binding: #%d)" % (eta, hi, int(np.argmin(c))))
        print("   m=%d (D=%d, rho0=%d): %s" % (m, m ** 3, m * m + 2, " | ".join(row)))
    print("   Remark 1 (m growing): largest m with all requirements satisfied (eta = 1, u = 1), and m^5 ln n / n there:")
    for n in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12):
        mm = 1
        while min(conditions(1.0, mm + 1, n, 1.0)) >= 0:
            mm += 1
        print("      n = %.0e: m <= %d   (m^5 ln n / n = %.3f;  (n/ln n)^(1/5) = %.1f)" % (n, mm, mm ** 5 * np.log(n) / n, (n / np.log(n)) ** 0.2))
    return True


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "SIQNE"
    ok = True
    for ch, fn in (("S", part_S), ("I", part_I), ("Q", part_Q), ("N", part_N), ("E", part_E)):
        if ch in which:
            r = fn()
            ok &= r
            sys.stdout.flush()
    print("OVERALL: %s" % ("all checks passed" if ok else "A CHECK FAILED"))
