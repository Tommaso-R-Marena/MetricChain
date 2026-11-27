#!/usr/bin/env python3
"""Referee R8 -- the exact number of evaluations of Algorithm 2L+ (with the two-sample brackets of
Proposition K0 as inner procedures) at the flat instance psi = 0, against the hinted lower bound
(1 - 2 delta) 2^n / |B(n, k*(eps))| of Theorem 11.25(a) for eps = x_out (item 14 of the brief).  Own code.

At psi = 0 every fibre average is 1 and the two-sample bracket of a flat fibre is deterministic
(t^ = A^ = 1):  [1/(1+eta_l), 1/(1-eta_l) + 2^{-d} E_rhat(d)],  so the whole run is deterministic and its
number of evaluations can be computed exactly for any n: all points of one block of the doubling sequence
have the same rung.  The simulation below follows section 2.2 pass by pass where points can be high
(s_j e^{-b} < 1) and in closed form per level above (there N = 0 at every pass, the closure test is monotone
in M, and the level ends at the first size that closes or is negligible).

usage: python3 r8_flat.py table            the table (u = 1, 2; n = 250 ... 64000; grid of phi)
       python3 r8_flat.py cross            cross-check of the closed-form run against the pass-by-pass
                                           implementation r8_core.run_2Lplus with real brackets (small n)
"""
import sys, time, math
from fractions import Fraction as Fr
import numpy as np

NEG_INF = float('-inf')


class TablesF:
    """log-tables of Q_m in floating point (for large m)"""

    def __init__(self, m, u):
        self.m, self.u = m, u
        j = np.arange(m + 1, dtype=float)
        lg = np.array([math.lgamma(k + 1.0) for k in range(m + 1)])
        self.lC = lg[m] - lg - lg[::-1]
        self.lB = np.logaddexp.accumulate(self.lC)
        lF = u * (j + 1) + np.logaddexp.accumulate(self.lC - u * j)
        self.lE = lF + np.log1p(-np.exp(self.lB - lF))
        # T_k = B_k + e^{uk} sum_{j>k} C(m,j) e^{-uj}
        suf = np.logaddexp.accumulate((self.lC - u * j)[::-1])[::-1]       # log sum_{j>=k}
        lG = np.full(m + 1, NEG_INF)
        lG[:m] = u * j[:m] + suf[1:]
        self.lT = np.logaddexp(self.lB, lG)
        self.mln2 = m * math.log(2)

    def radius_ge_log(self, lq):
        """least r with |B(m,r)| >= 2^m q  (log q given, q <= 1)"""
        return int(np.searchsorted(self.lB, self.mln2 + lq - 1e-12, side='left'))

    def k_le_log(self, lp):
        """largest k >= 0 with |B(m,k)| <= max(1, 2^m p)"""
        v = max(0.0, self.mln2 + lp)
        return max(0, int(np.searchsorted(self.lB, v + 1e-12, side='right')) - 1)

    def kappa_all(self, lceta):
        """kappa(r), r = 0..m"""
        prev = np.concatenate(([NEG_INF], self.lB[:-1]))
        v = np.maximum(0.0, lceta + prev)
        return np.maximum(0, np.searchsorted(self.lB, v + 1e-12, side='right') - 1)


_tf = {}


def tabF(m, u):
    if (m, u) not in _tf:
        _tf[(m, u)] = TablesF(m, u)
    return _tf[(m, u)]


def k0_plan_flat(d, u, x, ldeltap):
    """Proposition K0's family in dimension d at accuracy x: (log cost, log L, log U) of the bracket of a flat fibre"""
    t = tabF(d, u)
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ldeltap))
    budget = x - math.log((1 + eta) / (1 - eta))
    kap = t.kappa_all(math.log((1 - eta) / (1 + eta)))
    lGpp = t.lE - t.lT[kap]
    ok = np.logaddexp(0.0, lGpp[:d]) <= budget                    # ln(1 + Gamma'') <= budget
    if not ok[0]:
        return d * math.log(2), 0.0, 0.0, 'enum'
    bad = np.nonzero(~ok)[0]
    rstar = (int(bad[0]) - 1) if bad.size else d - 1
    lM = math.log(K) + t.mln2 - math.log(1 - eta) - t.lB[rstar]
    lM = max(lM, math.log(K / (1 - eta)))
    lcost = math.log(2) + lM
    if lcost >= d * math.log(2):
        return d * math.log(2), 0.0, 0.0, 'enum'           # enumeration is cheaper and exact
    lq = math.log(K) - math.log(1 - eta) - lM              # q_+  (M taken without rounding up)
    if t.mln2 + lq < -1e-12:
        ltail = NEG_INF
    else:
        rhat = min(t.radius_ge_log(lq), rstar)
        ltail = t.lE[rhat] - t.mln2
    lL = -math.log(1 + eta)
    lU = np.logaddexp(-math.log(1 - eta), ltail)
    assert lU - lL <= x + 1e-9
    return lcost, lL, float(lU), 'K0'


def flat_run(u, n, phi, lam=0.2, eta=0.05, etap=0.05, theta=0.05, b=0.5, delta=0.05, Lr=40, bounded=True,
             verbose=False, ltheta=None, ldelta=None, inner=None):
    """deterministic run of Algorithm 2L+ at psi = 0.  Returns a dict with log cost etc."""
    n_o = int(math.floor(phi * n))
    n_o = min(max(n_o, 1), n - 1)
    n_i = n - n_o
    t = tabF(n_o, u)
    ln2 = math.log(2)
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    if ltheta is None:
        ltheta = math.log(theta)
    if ldelta is None:
        ldelta = math.log(delta)
    J = math.ceil((2 * u * n + b + n_o * ln2) / lam)
    nu1 = 2 * math.exp(u) * n_o / math.exp(ltheta) if bounded else 1.0
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    lceta = math.log((1 - eta) / (1 + eta))
    kap = t.kappa_all(lceta)
    lGt = np.concatenate(([math.log(math.expm1(u))], t.lE[1:] - t.lB[:-1]))
    lGpp = t.lE - t.lT[kap]
    okN = lGt <= ltheta + math.log((1 - eta) * nu0)
    okP = np.minimum(lGt - lceta, lGpp) <= ltheta
    okb = (okN & okP)[:n_o]
    badi = np.nonzero(~okb)[0]
    rdag = (int(badi[0]) - 1) if badi.size else n_o - 1
    lpidag = (t.lB[rdag] - n_o * ln2) if rdag >= 0 else -(n_o + 1) * ln2
    m_max = math.ceil((math.log(2 * (1 + eta) / (1 - eta)) + lam + math.log(nu0) - lpidag) / ln2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(2 * (J + 1) * (m_max + 1) * (Lr + 2)) - ldelta))
    lK = math.log(K)
    lnu = lK + math.log(nu0)
    lMdag = lK - math.log(1 - eta) - lpidag
    lMbar = math.log(2 * (1 + eta)) + lam + math.log(nu0) + lMdag
    ldeltap = ldelta - math.log(4 * Lr) - lMbar
    xout = float(np.logaddexp(n * math.log(2 / (1 + math.exp(u))),
                              b + np.logaddexp(math.log(math.exp(lam) * (1 + eta) / (1 - eta) + etap), ltheta)))
    # inner brackets of the flat fibre, intersected along the ladder
    lcost = [NEG_INF] * (Lr + 1)
    lLr = [-u * n_i] + [0.0] * Lr
    lUr = [u * n_i] + [0.0] * Lr
    kinds = ['triv']
    for l in range(1, Lr + 1):
        if inner is None:
            c, a_, b_, kind = k0_plan_flat(n_i, u, xs[l], ldeltap)
        else:
            c, a_, b_, kind = inner(n_i, xs[l], ldeltap)
        lcost[l] = c
        lLr[l] = max(lLr[l - 1], a_)
        lUr[l] = min(lUr[l - 1], b_)
        kinds.append(kind)
    lLr = np.array(lLr)
    lUr = np.array(lUr)
    ls0 = -u * n
    lell = n * math.log((1 + math.exp(-u)) / 2)
    lSigma = NEG_INF
    up_terms = [ls0]
    l1mel = math.log(-math.expm1(-lam))
    lel1 = math.log(math.expm1(lam))
    lth_b = ltheta + b
    rung = np.zeros(1, dtype=np.int64)            # rung of block m (block 0: K points; block m: K 2^{m-1})
    nblocks = 1
    npop = nneg = 0
    stop = None
    max_calls_ratio = NEG_INF

    def need_rung(ls):
        cl = (lUr <= ls) | (lLr > ls - b)
        return int(np.argmax(cl))

    def grow(m):
        nonlocal rung, nblocks
        if m + 1 > nblocks:
            rung = np.concatenate((rung, np.zeros(m + 1 - nblocks, dtype=np.int64)))
            nblocks = m + 1

    def lsize(m):
        return lK if m == 0 else lK + (m - 1) * ln2

    for j in range(0, J + 1):
        ls = ls0 + j * lam
        rj = need_rung(ls)
        lMneg = lnu + ls - lell - b
        if ls - b >= 0.0:
            # nobody can be high (L <= 1 <= s_j e^{-b}): N = 0 at every pass
            m_neg = max(0, math.ceil((lMneg - lK) / ln2 - 1e-12))
            # largest radius r <= n_o - 1 whose tail closes
            lim = lth_b + lell - ls + n_o * ln2
            rc = int(np.searchsorted(t.lE[:n_o], lim + 1e-12, side='right')) - 1
            if rc >= 0:
                lMclose = lK + n_o * ln2 - math.log(1 - eta) - t.lB[rc]
                m_close = max(0, math.ceil((lMclose - lK) / ln2 - 1e-12))
            else:
                lMclose = lK + n_o * ln2 - math.log(1 - eta)
                m_close = max(0, math.floor((lMclose - lK) / ln2 + 1e-12) + 1)      # 2^{n_o} q < 1 strictly
            if m_close <= m_neg:
                grow(m_close)
                rung[:m_close + 1] = np.maximum(rung[:m_close + 1], rj)
                lM = lK + m_close * ln2
                lq = min(0.0, lK - math.log(1 - eta) - lM)
                if n_o * ln2 + lq < -1e-12:
                    ltail = NEG_INF
                    rcl = None
                else:
                    rcl = t.radius_ge_log(lq)
                    ltail = ls - n_o * ln2 + t.lE[rcl]
                stop = dict(j=j, m=m_close, r=rcl, ltail=ltail, populated=False)
                break
            grow(m_neg)
            rung[:m_neg + 1] = np.maximum(rung[:m_neg + 1], rj)
            lM = lK + m_neg * ln2
            lq = min(0.0, lK - math.log(1 - eta) - lM)
            up_terms.append(lel1 + ls + lq)
            nneg += 1
            continue
        # pass by pass
        m = 0
        closed = False
        while True:
            grow(m)
            rung[:m + 1] = np.maximum(rung[:m + 1], rj)
            high = lUr[rung[:m + 1]] > ls
            # N = sum of the sizes of the high blocks
            hb = [mm for mm in range(m + 1) if high[mm]]
            Nint = sum((K if mm == 0 else K << (mm - 1)) for mm in hb)
            Mint = K << m
            lM = lK + m * ln2
            if Nint >= K:
                lq = min(0.0, math.log(Nint) - math.log(1 - eta) - lM)
                lpbar = math.log(Nint) - math.log(1 + eta) - lM
                kk = t.k_le_log(lpbar)
                lell = max(lell, ls - b + lpbar, ls - b - n_o * ln2 + t.lT[kk])
            else:
                lq = min(0.0, lK - math.log(1 - eta) - lM)
            if n_o * ln2 + lq < -1e-12:
                ltail = NEG_INF
                rcl = None
            else:
                rcl = t.radius_ge_log(lq) if lq < 0.0 else n_o
                ltail = (ls - n_o * ln2 + t.lE[rcl]) if rcl <= n_o - 1 else float('inf')
            if ltail <= lth_b + lell:
                stop = dict(j=j, m=m, r=rcl, ltail=ltail, populated=Nint >= K, lpbar=(lpbar if Nint >= K else None))
                closed = True
                break
            elif Nint >= K:
                lSigma = np.logaddexp(lSigma, l1mel - b + ls + lpbar)
                up_terms.append(lel1 + ls + lq)
                npop += 1
                break
            elif lM >= lMneg:
                up_terms.append(lel1 + ls + lq)
                nneg += 1
                break
            else:
                m += 1
        if closed:
            break
    assert stop is not None, "no stop within J levels"
    # output and cost
    ls = ls0 + stop['j'] * lam
    lcur = (l1mel - b + ls + stop['lpbar']) if stop.get('lpbar') is not None else NEG_INF
    lL = max(lell, float(np.logaddexp(lSigma, lcur)))
    lU = float(np.logaddexp.reduce(np.array(up_terms + [stop['ltail']])))
    # number of evaluations: 1 + points + sum over blocks size * sum_{l<=rung} cost_l
    cum = np.logaddexp.accumulate(np.array([NEG_INF] + lcost[1:]))          # log sum_{l<=r} cost_l
    terms = [0.0]
    for m in range(nblocks):
        terms.append(lsize(m))
        if rung[m] >= 1:
            terms.append(lsize(m) + cum[rung[m]])
    lcost_total = float(np.logaddexp.reduce(np.array(terms)))
    # C_max
    def lcnt(x):
        return max(lK, math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + lnu + x)
    cm = [0.0, ln2 + lMbar]
    for l in range(1, Lr + 1):
        cm.append(min(ln2 + lMbar, math.log(J + 1) + lcnt(xs[l - 1])) + lcost[l])
    lCmax = float(np.logaddexp.reduce(np.array(cm)))
    return dict(n=n, n_o=n_o, n_i=n_i, lcost=lcost_total, lCmax=lCmax, lL=lL, lU=lU, width=lU - lL, xout=xout,
                stop=stop, npop=npop, nneg=nneg, K=K, J=J, rdag=rdag, lMbar=lMbar, nblocks=nblocks,
                maxrung=int(rung.max()), lMlast=lK + stop['m'] * ln2, kinds=kinds, lcosts=lcost, rung=rung.copy(),
                ldeltap=ldeltap, xs=xs)


def hinted_lower_bound(u, n, eps, delta):
    """log of (1 - 2 delta) 2^n / |B(n, k*(eps))|, k* the least k with 2^{-n} E_k(n) > e^eps - 1"""
    t = tabF(n, u)
    target = n * math.log(2) + math.log(math.expm1(eps))
    kstar = int(np.searchsorted(t.lE, target, side='right'))          # least k with lE[k] > target
    kstar = min(kstar, n)
    return math.log(1 - 2 * delta) + n * math.log(2) - t.lB[kstar], kstar


def table(us=(1.0, 2.0), ns=(250, 1000, 4000, 16000, 64000)):
    t0 = time.time()
    print("# exact number of evaluations of Algorithm 2L+ with Proposition-K0 brackets inside, at psi = 0")
    print("# parameters of the report's section 6.4: b=0.5, lam=0.2, eta=eta'=theta=0.05, delta=0.05, 40 rungs, nu_1 = 2e^u n_o/theta")
    for u in us:
        pu = 1 / (1 + math.exp(u))
        a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
        lam1 = math.log(2 / (1 + math.exp(-u)))
        rho = lam1 / u
        h = math.log(2) + rho * math.log(rho) + (1 - rho) * math.log(1 - rho)
        print("u = %.1f: a = %.5f, h = %.5f, h/a = %.4f" % (u, a, h, h / a))
        print("     n   best phi   ln(cost)/(na)   ln(C_max)/(na)   hinted LB/(na)   cost>=LB   cost<=C_max   width<=x_out  all phi: ln(cost)/(na)")
        for n in ns:
            best = None
            row = []
            okLB = True
            okC = True
            okW = True
            for phi in (0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.85):
                r = flat_run(u, n, phi)
                lb, kstar = hinted_lower_bound(u, n, r['xout'], 0.05)
                okLB &= r['lcost'] >= lb
                okC &= r['lcost'] <= r['lCmax'] + 1e-9
                okW &= r['width'] <= r['xout'] + 1e-9
                row.append(r['lcost'] / (n * a))
                if best is None or r['lcost'] < best[0]['lcost']:
                    best = (r, phi, lb)
            r, phi, lb = best
            print("%6d   %5.2f      %8.4f        %8.4f        %8.4f       %s       %s        %s      %s   [%.0fs]"
                  % (n, phi, r['lcost'] / (n * a), r['lCmax'] / (n * a), lb / (n * a), okLB, okC, okW,
                     ' '.join('%.3f' % v for v in row), time.time() - t0))
            sys.stdout.flush()


def cross():
    """the closed-form flat run against the pass-by-pass implementation with real two-sample brackets"""
    from r8_core import Tables, Consts, run_2Lplus, check_run
    from r8_pops import PopEnum
    from r8_e2e import K0Family
    rng = np.random.default_rng(3)
    print("# cross-check at psi = 0: closed-form run (this file) against r8_core.run_2Lplus with real K0 brackets")
    print("#  u  n_o n_i  phi-run: stop level, last M, closing radius, populated, negligible, ln(evaluations) | real run: the same")
    nbad = 0
    for (u, n_o, n_i, lam, eta, etap, theta, b, Lr) in [(1.0, 6, 6, 0.3, 0.25, 0.5, 0.5, 1.0, 3), (1.0, 7, 5, 0.45, 0.5, 1.0, 1.0, 2.0, 2),
                                                        (0.5, 8, 6, 0.6, 0.25, 0.2, 0.3, 0.7, 4), (2.0, 6, 5, 0.37, 0.25, 0.5, 2.0, 1.5, 3),
                                                        (1.0, 8, 4, 0.8, 0.5, 0.3, 0.2, 1.0, 2), (0.5, 7, 7, 0.25, 0.25, 1.0, 5.0, 0.6, 5)]:
        n = n_o + n_i
        phi = (n_o + 0.5) / n
        r = flat_run(u, n, phi, lam=lam, eta=eta, etap=etap, theta=theta, b=b, delta=0.05, Lr=Lr, bounded=True)
        assert r['n_o'] == n_o
        psi = np.zeros(1 << n)
        pop = PopEnum(psi, n, n_o, u, rng)
        tab = Tables(n_o, u)
        xs = r['xs']
        cs = Consts(tab, n, n_o, u, lam, Fr(eta), etap, theta, 2 * math.exp(u) * n_o / theta, b, 0.05, xs)
        fam = K0Family(n_i, u)
        plans = [None] + [fam.plan(xs[l], cs.ldeltap) for l in range(1, Lr + 1)]
        # make the real family take enumeration where it is cheaper, as the closed-form run does
        for l in range(1, Lr + 1):
            if (not plans[l]['enum']) and plans[l]['cost'] >= (1 << n_i):
                plans[l] = {'enum': True, 'cost': 1 << n_i, 'x': xs[l]}
        q = {'n': 0}

        def orc(blk, sel, l, x, ls, bb):
            a = blk.aidx[sel]
            l1, u1, _ = fam.brackets(pop.w[a], plans[l], rng)
            q['n'] += a.shape[0] * plans[l]['cost']
            return l1, u1
        tr = run_2Lplus(cs, pop, pop.ls0, orc, rng, maxM_log2=24)
        st = tr['stop']
        npts = sum(int(bk.cumtop[2]) for bk in tr['blocks'])
        real_cost = 1 + npts + q['n']
        npop = sum(1 for lev in tr['levels'] if lev['exit'] == 'pop')
        nneg = sum(1 for lev in tr['levels'] if lev['exit'] == 'neg')
        lastM = tr['levels'][-1]['passes'][-1]['M']
        same = (st['j'] == r['stop']['j'] and abs(math.log(lastM) - r['lMlast']) < 1e-9 and st['r'] == r['stop']['r']
                and npop == r['npop'] and nneg == r['nneg'] and abs(math.log(real_cost) - r['lcost']) < 2e-3
                and abs(st['lU'] - st['lL'] - r['width']) < 1e-6)
        nbad += (not same)
        print("u=%.1f n_o=%d n_i=%d | closed form: j=%d M=%.6g r=%s pop=%d neg=%d ln(eval)=%.5f width=%.5f | real: j=%d M=%d r=%s pop=%d neg=%d ln(eval)=%.5f width=%.5f | %s"
              % (u, n_o, n_i, r['stop']['j'], math.exp(r['lMlast']), r['stop']['r'], r['npop'], r['nneg'], r['lcost'], r['width'],
                 st['j'], lastM, st['r'], npop, nneg, math.log(real_cost), st['lU'] - st['lL'], 'AGREE' if same else 'DIFFER'))
    print("parameter sets that differ:", nbad)


if __name__ == '__main__':
    if sys.argv[1] == 'table':
        us = tuple(float(x) for x in sys.argv[2].split(',')) if len(sys.argv) > 2 else (1.0, 2.0)
        ns = tuple(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 else (250, 1000, 4000, 16000, 64000)
        table(us, ns)
    else:
        cross()
