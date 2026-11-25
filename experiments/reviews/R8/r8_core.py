#!/usr/bin/env python3
"""Referee R8 -- own implementation of Algorithm 2L+ (report of workstream K, section 2.2),
written from the text of sections 2.1-2.3 only (none of the author's code was used).

Contents
  Tables      exact ball sizes of Q_m (python ints) and log-tables of E_r(m), T_m(k), Gamma~, Gamma''
  Consts      the constants J, nu_0, r_dagger, pi_dagger, m_max, K, nu, M_dagger, Mbar, delta', cnt, C_max
  run_2Lplus  the outer loop, over a "population" that delivers the outer points in the blocks of the
              doubling sequence; each block is a set of groups (a group = points with one fibre average
              that are treated alike by the inner oracle; in the per-point populations every group has
              one point)
  check_run   the good event (V2),(V3) on the realised sample and every claim (i)-(vi) of Theorem K1

All levels, bounds and tails are kept as logarithms; the certified probabilities q, p_underbar and all
radius computations are exact (Fractions against integer ball sizes), in particular q = 1 gives the
radius n_o exactly.
"""
import math
from fractions import Fraction as Fr
from bisect import bisect_left, bisect_right
import numpy as np

NEG_INF = float('-inf')
POS_INF = float('inf')


def logaddexp(a, b):
    if a == NEG_INF:
        return b
    if b == NEG_INF:
        return a
    if a < b:
        a, b = b, a
    return a + math.log1p(math.exp(b - a))


def logsumexp_list(v):
    v = [x for x in v if x != NEG_INF]
    if not v:
        return NEG_INF
    m = max(v)
    return m + math.log(sum(math.exp(x - m) for x in v))


class Tables:
    """Q_m, slope u.  ball[r+1] = |B(m,r)| exactly (ball[0] = |B(m,-1)| = 0)."""

    def __init__(self, m, u):
        self.m, self.u = m, u
        C = [math.comb(m, j) for j in range(m + 1)]
        self.C = C
        ball = [0]
        s = 0
        for j in range(m + 1):
            s += C[j]
            ball.append(s)
        self.ball = ball                       # length m+2
        self.ballr = ball[1:]                  # ballr[r] = |B(m,r)|, r = 0..m
        self.lC = [math.log(c) for c in C]
        self.lB = [math.log(x) for x in self.ballr]
        # E_r = F_r - |B(r)|,  F_r = e^u (F_{r-1} + C(m,r))
        lE = []
        lF = NEG_INF
        for r in range(m + 1):
            lF = u + logaddexp(lF, self.lC[r])
            lE.append(lF + math.log1p(-math.exp(self.lB[r] - lF)))
        self.lE = lE
        # T_k = |B(k)| + G_k,  G_k = e^{-u}(C(m,k+1) + G_{k+1})
        lT = [0.0] * (m + 1)
        lG = NEG_INF
        lT[m] = self.lB[m]
        for k in range(m - 1, -1, -1):
            lG = -u + logaddexp(self.lC[k + 1], lG)
            lT[k] = logaddexp(self.lB[k], lG)
        self.lT = lT
        self.two_m = 1 << m

    def radius_ge(self, q):
        """least r with |B(m,r)| >= 2^m q  (q a Fraction in (0,1]); r = m iff 2^m q > |B(m,m-1)|"""
        thr = -((-self.two_m * q.numerator) // q.denominator)      # ceil(2^m q)
        return bisect_left(self.ballr, thr)

    def k_le(self, p):
        """largest k >= 0 with |B(m,k)| <= max(1, 2^m p)"""
        fl = max(1, (self.two_m * p.numerator) // p.denominator)
        return bisect_right(self.ballr, fl) - 1

    def kappa(self, r, ceta):
        """largest k >= 0 with |B(m,k)| <= max(1, c_eta |B(m,r-1)|)"""
        x = ceta * self.ball[r]
        fl = max(1, x.numerator // x.denominator)
        return bisect_right(self.ballr, fl) - 1

    def lGt(self, r):
        """log Gamma~(r)"""
        if r == 0:
            return math.log(math.expm1(self.u))
        return self.lE[r] - self.lB[r - 1]

    def lGpp(self, r, ceta):
        """log Gamma''(r)"""
        return self.lE[r] - self.lT[self.kappa(r, ceta)]


class Consts:
    """Constants of section 2.2.  eta is a Fraction; lam, etap, theta, nu1, b, delta floats;
    xs = [x_0, x_1, ..., x_L] (x_0 = 2 u n_i)."""

    def __init__(self, tab, n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, Koverride=None):
        assert tab.m == n_o and 1 <= n_o <= n - 1
        self.tab = tab
        self.n, self.n_o, self.n_i, self.u = n, n_o, n - n_o, u
        self.lam, self.eta, self.etap, self.theta, self.nu1, self.b, self.delta = lam, eta, etap, theta, nu1, b, delta
        self.xs = list(xs)
        self.L = len(xs) - 1
        assert self.L >= 1 and abs(xs[0] - 2 * u * self.n_i) < 1e-12 and xs[-1] <= b + 1e-15
        assert all(xs[i] > xs[i + 1] for i in range(self.L))
        assert 0 < lam <= 1 and 0 < eta <= Fr(1, 2) and 0 < etap <= 1 and theta > 0 and nu1 >= 1 and b > 0
        e = float(eta)
        self.e = e
        self.ceta = (1 - eta) / (1 + eta)
        self.J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
        self.nu0 = max((self.J + 1) * math.expm1(lam) / etap, nu1) / (1 - e)
        # r_dagger: largest r in {0..m-1} with [N] and [P] for all r' <= r
        lN = math.log(theta * (1 - e) * self.nu0)
        lth = math.log(theta)
        lce = math.log(float(self.ceta))
        rd = -1
        for r in range(0, n_o):
            g = tab.lGt(r)
            if g > lN:
                break
            if min(g - lce, tab.lGpp(r, self.ceta)) > lth:
                break
            rd = r
        self.rdag = rd
        if rd >= 0:
            self.pidag = Fr(tab.ballr[rd], tab.two_m)
            self.lpidag = tab.lB[rd] - n_o * math.log(2)
        else:
            self.pidag = Fr(1, 2 * tab.two_m)
            self.lpidag = -(n_o + 1) * math.log(2)
        l2 = math.log(2)
        self.m_max = math.ceil((math.log(2 * (1 + e) / (1 - e)) + lam + math.log(self.nu0) - self.lpidag) / l2)
        self.K = math.ceil(3 * (1 + e) / e ** 2 * math.log(2 * (self.J + 1) * (self.m_max + 1) * (self.L + 2) / delta))
        self.K_theorem = self.K
        if Koverride is not None:
            self.K = int(Koverride)
        self.nu = self.K * self.nu0
        self.lMdag = math.log(self.K) - math.log(1 - e) - self.lpidag
        self.lMbar = math.log(2 * (1 + e)) + lam + math.log(self.nu0) + self.lMdag
        self.ldeltap = math.log(delta) - math.log(4 * self.L) - self.lMbar
        self.xout = math.log((2 / (1 + math.exp(u))) ** n + math.exp(b) * (math.exp(lam) * (1 + e) / (1 - e) + etap + theta))
        self.lell0_minus_ls0 = -n * math.log(2 / (1 + math.exp(u)))       # ell_0 = s_0 (2 p_u)^{-n}

    def lcnt(self, x):
        e = self.e
        return max(math.log(self.K), math.log(2 * (1 + e) ** 2 / (1 - e)) + self.lam + math.log(self.nu) + x)


# ----------------------------------------------------------------------------------------------
# simulated inner oracle: a valid bracket of ratio e^x around W, placed by one of several rules
# ----------------------------------------------------------------------------------------------
def oracle_sim(rule, lW, lL, lU, x, ls, b, rng):
    """returns (newL, newU) in logs with newL <= lW <= newU, newU - newL <= x.
    rules: 'rand', 'top' (value at the top of the bracket), 'bot', 'mid',
           'adv_hi' / 'adv_lo': keep the point unclassified at the current level if a valid bracket allows;
           otherwise make it high / low if possible."""
    k = lW.shape[0]
    if rule == 'rand':
        th = rng.random(k)
        return lW - th * x, lW + (1 - th) * x
    if rule == 'top':
        return lW - x, lW.copy()
    if rule == 'bot':
        return lW.copy(), lW + x
    if rule == 'mid':
        return lW - 0.5 * x, lW + 0.5 * x
    if rule in ('adv_hi', 'adv_lo'):
        # unclassified after intersection needs  newL <= ls - b  and  newL + x > ls,  newL in [lW - x, lW]
        cand = np.minimum(lW, ls - b)
        feas = (cand >= lW - x) & (cand + x > ls) & (x > b)
        newL = np.where(feas, cand, 0.0)
        newU = np.where(feas, cand + x, 0.0)
        nf = ~feas
        if nf.any():
            if rule == 'adv_hi':
                # as high as possible: value at the bottom -> L = W
                aL = lW
                aU = lW + x
            else:
                # as low as possible: value at the top -> U = W
                aL = lW - x
                aU = lW
            newL = np.where(nf, aL, newL)
            newU = np.where(nf, aU, newU)
        return newL, newU
    raise ValueError(rule)


class Block:
    __slots__ = ('cnt', 'lW', 'lL', 'lU', 'rung', 'aidx', 'order', 'cumtop')

    def finish(self):
        """sorted fibre averages with cumulative counts from the top (for the exact exceedance counts)"""
        self.order = np.argsort(self.lW, kind='stable')
        lw = self.lW[self.order]
        c = self.cnt[self.order]
        tot = int(c.sum())
        self.cumtop = (lw, np.concatenate(([0], np.cumsum(c))), tot)

    def exceed(self, lt):
        """number of points of the block with lW > lt  (lt scalar or array)"""
        lw, cum, tot = self.cumtop
        i = np.searchsorted(lw, lt, side='right')
        return tot - cum[i]


def run_2Lplus(cs, pop, ls0, oracle, rng, mutation=None, maxM_log2=61, record=True, C_inner=None):
    """Algorithm 2L+.  cs: Consts; pop: population with new_block(size) -> Block (trivial brackets set);
    ls0 = log s_0;  oracle(block, sel, l, x, ls, b) -> (newL, newU) for the groups sel of the block.
    Returns a dict (trace)."""
    tab = cs.tab
    n_o, lam, b, eta, K = cs.n_o, cs.lam, cs.b, cs.eta, cs.K
    e = cs.e
    L = cs.L
    xs = cs.xs
    ln2 = math.log(2)
    lell = ls0 + cs.lell0_minus_ls0
    lSigma = NEG_INF
    lnu = math.log(cs.nu)
    lth_b = math.log(cs.theta) + b
    l1mel = math.log(-math.expm1(-lam))          # log(1 - e^{-lam})
    lel1 = math.log(math.expm1(lam))             # log(e^{lam} - 1)
    blocks = []
    trace = {'levels': [], 'abort': None, 'stop': None, 'blocks': blocks, 'skipped': False}
    upper_terms = []                             # log of (s_{i+1}-s_i) q_i for the levels left, with kind
    queries = 1
    calls_total = [0] * (L + 1)

    def classify(mi, ls, calls):
        """classify block mi at the level ls; returns number of high points or None (abort)"""
        blk = blocks[mi]
        while True:
            mask = (blk.lU > ls) & (blk.lL <= ls - b)
            idx = np.nonzero(mask)[0]
            if idx.size == 0:
                break
            rr = blk.rung[idx] + 1
            if (rr > L).any():
                return None
            for l in np.unique(rr):
                sel = idx[rr == l]
                nL, nU = oracle(blk, sel, int(l), xs[int(l)], ls, b)
                blk.lL[sel] = np.maximum(blk.lL[sel], nL)
                blk.lU[sel] = np.minimum(blk.lU[sel], nU)
                blk.rung[sel] = l
                c = int(blk.cnt[sel].sum())
                calls[int(l)] += c
        return int(blk.cnt[blk.lU > ls].sum())

    for j in range(0, cs.J + 1):
        ls = ls0 + j * lam
        lell_entry = lell
        if mutation == 'neg_tol':
            lMneg = lnu + ls - lell_entry                  # mutation: threshold without e^{-b}
        else:
            lMneg = lnu + ls - lell_entry - b
        lev = {'j': j, 'ls': ls, 'lell_entry': lell_entry, 'lMneg': lMneg, 'passes': [], 'calls': [0] * (L + 1),
               'exit': None}
        trace['levels'].append(lev)
        m = 0
        N = 0
        nblk_done = 0
        while True:
            # classify a_1..a_M at level j  (blocks 0..m)
            while nblk_done <= m:
                if nblk_done >= len(blocks):
                    size = K if nblk_done == 0 else K << (nblk_done - 1)
                    blk = pop.new_block(size)
                    blk.finish()
                    blocks.append(blk)
                    queries += size
                h = classify(nblk_done, ls, lev['calls'])
                if h is None:
                    trace['abort'] = 'unclassified at rung L'
                    return trace
                N += h
                nblk_done += 1
            M = K << m
            if mutation == 'q_plain':
                q = min(Fr(1), Fr(max(N, K), M))
            else:
                q = min(Fr(1), Fr(max(N, K)) / ((1 - eta) * M))
            pbar = None
            kk = None
            if N >= K:
                pbar = Fr(N) / ((1 + eta) * M)
                kk = tab.k_le(pbar)
                c1 = ls - b + math.log(pbar)
                c2 = ls - b - n_o * ln2 + tab.lT[kk]
                if mutation == 'noharper':
                    lell = max(lell, c1)
                else:
                    lell = max(lell, c1, c2)
            # closure test
            if tab.two_m * q < 1:
                r = None
                ltail = NEG_INF
            else:
                r = tab.radius_ge(q)
                if r <= n_o - 1:
                    ltail = ls - n_o * ln2 + tab.lE[r]
                elif mutation == 'close_at_no':
                    ltail = ls - n_o * ln2 + tab.lE[n_o]       # mutation: tail lemma applied at r = n_o
                else:
                    ltail = POS_INF
            pas = {'m': m, 'M': M, 'N': N, 'q': q, 'pbar': pbar, 'k': kk, 'r': r, 'ltail': ltail, 'lell': lell}
            lev['passes'].append(pas)
            if ltail <= lth_b + lell:
                # stop
                lcur = NEG_INF
                if N >= K:
                    lcur = l1mel - b + ls + math.log(pbar)
                lsum = logaddexp(lSigma, lcur)
                if mutation == 'maxform':
                    lLout = lell                       # mutation: lower end without the sum
                else:
                    lLout = max(lell, lsum)
                lpop = logsumexp_list([t for (t, kind) in upper_terms if kind == 'pop'])
                lneg = logsumexp_list([t for (t, kind) in upper_terms if kind == 'neg'])
                lUout = logsumexp_list([ls0, lpop, lneg, ltail])
                lev['exit'] = 'stop'
                pas['out'] = 'stop'
                trace['stop'] = {'j': j, 'lL': lLout, 'lU': lUout, 'ls0': ls0, 'lpop': lpop, 'lneg': lneg,
                                 'ltail': ltail, 'lell': lell, 'lsum': lsum, 'populated': N >= K, 'r': r}
                break
            elif N >= K:
                lev['exit'] = 'pop'
                pas['out'] = 'pop'
                lev['q'] = q
                lev['pbar'] = pbar
                lSigma = logaddexp(lSigma, l1mel - b + ls + math.log(pbar))
                upper_terms.append((lel1 + ls + math.log(q), 'pop'))
                break
            elif math.log(M) >= lMneg:
                lev['exit'] = 'neg'
                pas['out'] = 'neg'
                lev['q'] = q
                upper_terms.append((lel1 + ls + math.log(q), 'neg'))
                break
            else:
                pas['out'] = 'double'
                m += 1
                if m > cs.m_max:
                    trace['abort'] = 'M would exceed K 2^m_max'
                    lev['exit'] = 'abort'
                    return trace
                if m > maxM_log2 - int(math.log2(K)) - 1:
                    trace['skipped'] = True          # not an abort of the algorithm: the simulation is too large
                    lev['exit'] = 'skip'
                    return trace
        lev['M_last'] = K << m
        lev['m_last'] = m
        for l in range(1, L + 1):
            calls_total[l] += lev['calls'][l]
        if lev['exit'] == 'stop':
            break
    else:
        trace['abort'] = 'level J left'
    trace['queries_points'] = queries
    trace['calls_total'] = calls_total
    return trace


# ----------------------------------------------------------------------------------------------
# checks
# ----------------------------------------------------------------------------------------------
class Result:
    def __init__(self):
        self.viol = []            # list of (claim, detail)
        self.info = {}

    def bad(self, claim, detail=''):
        self.viol.append((claim, detail))


def exceed_counts(blocks, mmax, lts):
    """X_t(K 2^m) for m = 0..mmax and thresholds lts (array): integer array [m, t]"""
    lts = np.asarray(lts, dtype=float)
    out = np.zeros((mmax + 1, lts.shape[0]), dtype=np.int64)
    acc = np.zeros(lts.shape[0], dtype=np.int64)
    for m in range(mmax + 1):
        acc = acc + blocks[m].exceed(lts)
        out[m] = acc
    return out


def check_run(cs, pop, trace, lA, tol=1e-9, xgrid=(0.05, 0.3, 1.0, 2.5, 6.0, 15.0, 40.0)):
    """Good event on the realised sample, and every claim of Theorem K1.
    pop.p_exceed(lt) -> exact Fraction P(W > e^lt);  pop.lp_exceed(lts) -> float logs (array).
    Returns Result with fields info['G_used'], info['G_full'] and the list of violated claims."""
    res = Result()
    tab = cs.tab
    eta, e, K, b, lam, L = cs.eta, cs.e, cs.K, cs.b, cs.lam, cs.L
    xs = cs.xs
    levels = trace['levels']
    blocks = trace['blocks']
    nb = len(blocks)
    Jreached = len(levels)
    ls0 = levels[0]['ls']
    ln2 = math.log(2)
    info = res.info

    # ---------------- good event ----------------
    # thresholds of (V2): s_j ; of (V3): s_j e^{-b}, s_j e^{-x_l}, l = 0..L-1
    def exact_p(lt):
        return pop.p_exceed(lt)

    def v2_ok(M, X, lt):
        p = exact_p(lt)
        return (M * p <= Fr(K) / (1 - eta)) or (X >= (1 - eta) * M * p)

    def v3_ok(M, X, lt):
        if X < K:
            return True
        p = exact_p(lt)
        return X <= (1 + eta) * M * p

    # G_used: exactly the events the proof uses on this run
    G_used = True
    used_fail = []
    for lev in levels:
        ls = lev['ls']
        ms = sorted(set(p['m'] for p in lev['passes']))
        if not ms:
            continue                      # level entered but aborted before its first pass
        Xs = exceed_counts(blocks, max(ms), [ls, ls - b])
        for p in lev['passes']:
            M = p['M']
            if not v2_ok(M, int(Xs[p['m'], 0]), ls):
                G_used = False
                used_fail.append(('V2', lev['j'], p['m']))
            if not v3_ok(M, int(Xs[p['m'], 1]), ls - b):
                G_used = False
                used_fail.append(('V3b', lev['j'], p['m']))
        if 'm_last' in lev:
            ml = lev['m_last']
            lts = [ls - xs[l] for l in range(0, L)]
            Xl = exceed_counts(blocks, ml, lts)
            for l in range(0, L):
                if not v3_ok(K << ml, int(Xl[ml, l]), lts[l]):
                    G_used = False
                    used_fail.append(('V3x', lev['j'], l))
    info['G_used'] = G_used
    info['used_fail'] = used_fail
    # G_full: all levels 0..J and all realised sizes
    G_full = True
    nfull_fail = 0
    allj = np.arange(0, cs.J + 1)
    thr_sets = [ls0 + allj * lam, ls0 + allj * lam - b] + [ls0 + allj * lam - xs[l] for l in range(0, L)]
    for ti, lts in enumerate(thr_sets):
        X = exceed_counts(blocks, nb - 1, lts)                 # [m, j]
        lp = pop.lp_exceed(lts)                                 # float log p
        for m in range(nb):
            M = K << m
            lM = math.log(M)
            Xm = X[m].astype(float)
            mu = np.exp(lM + lp)                                # M p
            if ti == 0:
                # suspicious if not (M p <= K/(1-eta)) and X < (1-eta) M p   (with a float margin)
                sus = (mu > K / (1 - e) * (1 - 1e-9)) & (Xm < (1 - e) * mu * (1 + 1e-9))
            else:
                sus = (Xm >= K) & (Xm > (1 + e) * mu * (1 - 1e-9))
            for jj in np.nonzero(sus)[0]:
                ok = v2_ok(M, int(X[m, jj]), float(lts[jj])) if ti == 0 else v3_ok(M, int(X[m, jj]), float(lts[jj]))
                if not ok:
                    G_full = False
                    nfull_fail += 1
    info['G_full'] = G_full
    info['nfull_fail'] = nfull_fail

    # ---------------- claims ----------------
    lMbar = cs.lMbar
    lc = math.log(float(1 / cs.ceta))
    # (i)
    if trace['abort'] is not None:
        res.bad('i', 'abort: ' + trace['abort'])
    st = trace['stop']
    if st is None and trace['abort'] is None:
        res.bad('i', 'no stop')
    # (ii) certificates, pass by pass
    for lev in levels:
        ls = lev['ls']
        for p in lev['passes']:
            pj = exact_p(ls)
            if pj > p['q']:
                res.bad('ii-q', 'level %d M=%d' % (lev['j'], p['M']))
            if p['pbar'] is not None:
                if p['pbar'] > exact_p(ls - b):
                    res.bad('ii-pbar', 'level %d M=%d' % (lev['j'], p['M']))
            if p['lell'] > lA + tol:
                res.bad('ii-ell', 'level %d: ell-A=%.3g' % (lev['j'], p['lell'] - lA))
    if st is not None:
        if st['lL'] > lA + tol:
            res.bad('ii-L', 'L-A=%.3g' % (st['lL'] - lA))
        if st['lU'] < lA - tol:
            res.bad('ii-U', 'A-U=%.3g' % (lA - st['lU']))
        # width and its components (these hold on or off the good event)
        w = st['lU'] - st['lL']
        info['width'] = w
        info['width_slack'] = cs.xout - w
        if w > cs.xout + tol:
            res.bad('width', 'ln(U/L)=%.6f > x_out=%.6f' % (w, cs.xout))
        lLo = st['lL']
        if st['ls0'] > cs.n * math.log(2 / (1 + math.exp(cs.u))) + lLo + tol:
            res.bad('width-s0')
        if st['lpop'] > lc + lam + b + lLo + tol:
            res.bad('width-pop', '%.4g' % (st['lpop'] - (lc + lam + b + lLo)))
        if st['lneg'] > math.log(cs.etap) + b + lLo + tol:
            res.bad('width-neg')
        if st['ltail'] > math.log(cs.theta) + b + lLo + tol:
            res.bad('width-tail')
        info['neg_share'] = math.exp(st['lneg'] - (math.log(cs.etap) + b + lLo)) if st['lneg'] > NEG_INF else 0.0
    # (iii) every level left without stopping has q_j > pi_dagger  (r(q_j) > r_dagger)
    npop = nneg = 0
    for lev in levels:
        if lev['exit'] in ('pop', 'neg'):
            npop += lev['exit'] == 'pop'
            nneg += lev['exit'] == 'neg'
            if not (lev['q'] > cs.pidag):
                res.bad('iii', 'level %d left (%s) with q<=pi_dagger' % (lev['j'], lev['exit']))
            rq = tab.radius_ge(lev['q'])
            if not (rq > cs.rdag):
                res.bad('iii-r', 'level %d left (%s) with r=%d <= r_dagger=%d' % (lev['j'], lev['exit'], rq, cs.rdag))
    info['npop'], info['nneg'] = npop, nneg
    # (iv) sample sizes
    lMneg_bound = math.log(1 + e) + lam + math.log(cs.nu0) + cs.lMdag
    maxM_over_Mdag = NEG_INF
    for lev in levels:
        if lev['lMneg'] > lMneg_bound + tol:
            res.bad('iv-Mneg', 'level %d: ln(Mneg/bound)=%.3g' % (lev['j'], lev['lMneg'] - lMneg_bound))
        for p in lev['passes']:
            lM = math.log(p['M'])
            if lM > max(math.log(K), ln2 + lev['lMneg']) + tol:
                res.bad('iv-M', 'level %d' % lev['j'])
            if lM > lMbar + tol:
                res.bad('iv-Mbar', 'level %d' % lev['j'])
            maxM_over_Mdag = max(maxM_over_Mdag, lM - cs.lMdag)
    info['maxM_over_Mdag'] = math.exp(maxM_over_Mdag)
    # (v) the count
    lcount_bound0 = lc + lam + math.log(cs.nu)                 # + x
    worst_count = NEG_INF
    xg = np.array(sorted(set(list(xgrid) + xs[:L])))
    for lev in levels:
        ls = lev['ls']
        lp = pop.lp_exceed(ls - xg)
        val = lev['lMneg'] + lp - (lcount_bound0 + xg)
        wv = float(val.max())
        worst_count = max(worst_count, wv)
        if wv > tol:
            res.bad('v-count', 'level %d: ln(ratio)=%.3g' % (lev['j'], wv))
        if 'm_last' in lev:
            ml = lev['m_last']
            lts = [ls - xs[l] for l in range(0, L)]
            Xl = exceed_counts(blocks, ml, lts)
            for l in range(0, L):
                if math.log(max(int(Xl[ml, l]), 1)) > cs.lcnt(xs[l]) + tol:
                    res.bad('v-cnt', 'level %d rung %d: %d points > cnt' % (lev['j'], l, int(Xl[ml, l])))
    info['worst_count'] = math.exp(worst_count)
    # (vi) calls
    tot_calls = [0] * (L + 1)
    for lev in levels:
        for l in range(1, L + 1):
            c = lev['calls'][l]
            tot_calls[l] += c
            if c > 0:
                lcb = min(lMbar, cs.lcnt(xs[l - 1]))
                if math.log(c) > lcb + tol:
                    res.bad('vi-level', 'level %d rung %d: %d calls' % (lev['j'], l, c))
    for l in range(1, L + 1):
        if tot_calls[l] > 0:
            lcb = min(lMbar, math.log(cs.J + 1) + cs.lcnt(xs[l - 1]))
            if math.log(tot_calls[l]) > lcb + tol:
                res.bad('vi-total', 'rung %d' % l)
    npts = sum(int(bk.cumtop[2]) for bk in blocks)
    if math.log(npts) > lMbar + tol:
        res.bad('vi-points')
    info['calls'] = tot_calls
    info['npoints'] = npts
    info['levels'] = Jreached
    if st is not None:
        info['stop_level'] = st['j']
        info['closure'] = ('empty' if st['ltail'] == NEG_INF else ('pop' if st['populated'] else 'unpop'))
        info['closure_r'] = st['r']
    return res
