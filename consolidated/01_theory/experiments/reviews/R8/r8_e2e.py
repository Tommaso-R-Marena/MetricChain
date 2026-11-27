#!/usr/bin/env python3
"""Referee R8 -- (A) Proposition K0 by simulation, (B) Algorithm 2L+ end to end with REAL inner brackets
(the two-sample bracket of Proposition K0 on every fibre), on cubes small enough to enumerate for the truth.
Own code, from the text of Proposition K0 and section 2.2.

usage: python3 r8_e2e.py A [seed]      Proposition K0 alone: coverage, width, the three events
       python3 r8_e2e.py B [nruns] [seed] [timelimit]   the two-level algorithm with real inner brackets
"""
import sys, time, math
from fractions import Fraction as Fr
import numpy as np
from r8_core import Tables, Consts, run_2Lplus, check_run, NEG_INF
from r8_pops import gen_psi, KINDS, PopEnum, popcounts

_tabs = {}


def get_tab(m, u):
    if (m, u) not in _tabs:
        _tabs[(m, u)] = Tables(m, u)
    return _tabs[(m, u)]


class K0Family:
    """the family of Proposition K0 in dimension d"""

    def __init__(self, d, u):
        self.d, self.u = d, u
        self.tab = get_tab(d, u)

    def plan(self, x, ldeltap):
        """parameters for accuracy x and failure probability e^{ldeltap}"""
        tab, d = self.tab, self.d
        eta = min(0.5, math.tanh(x / 4))
        etaF = Fr(eta)
        ceta = (1 - etaF) / (1 + etaF)
        K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) - ldeltap))
        budget = x - math.log((1 + eta) / (1 - eta))
        rstar = -1
        for r in range(0, d):
            if math.log1p(math.exp(tab.lGpp(r, ceta))) <= budget:
                rstar = r
            else:
                break
        if rstar < 0:
            return {'enum': True, 'cost': 1 << d, 'x': x}
        Mq = Fr(K * tab.two_m) / ((1 - etaF) * tab.ballr[rstar])
        M = -((-Mq.numerator) // Mq.denominator)                  # ceil(K 2^d / ((1-eta)|B(d,r*)|)), exact
        qplus = Fr(K) / ((1 - etaF) * M)
        if tab.two_m * qplus < 1:
            rhat = None
            ltailfac = NEG_INF
            lGpp = NEG_INF
        else:
            rhat = tab.radius_ge(qplus)
            assert rhat <= rstar <= d - 1
            ltailfac = tab.lE[rhat] - d * math.log(2)             # t^ * 2^{-d} E_rhat
            lGpp = tab.lGpp(rhat, ceta)
        cert = math.log((1 + eta) / (1 - eta)) + (math.log1p(math.exp(lGpp)) if lGpp > NEG_INF else 0.0)
        assert cert <= x + 1e-12
        return {'enum': False, 'eta': eta, 'K': K, 'M': M, 'rhat': rhat, 'rstar': rstar, 'ltailfac': ltailfac,
                'cost': 2 * M, 'x': x, 'cert': cert, 'qplus': float(qplus), 'qminus': K / ((1 + eta) * M)}

    def brackets(self, wrows, plan, rng, want_events=False):
        """wrows: array [k, 2^d] of fibre weights.  Returns log L, log U (and the three events)."""
        k, S = wrows.shape
        if plan['enum']:
            lw = np.log(wrows.mean(axis=1))
            return lw, lw.copy(), None
        K, M, eta = plan['K'], plan['M'], plan['eta']
        pv = np.full(S, 1.0 / S)
        c1 = rng.multinomial(M, pv, size=k)
        c2 = rng.multinomial(M, pv, size=k)
        order = np.argsort(-wrows, axis=1, kind='stable')
        ws = np.take_along_axis(wrows, order, axis=1)
        c1s = np.take_along_axis(c1, order, axis=1)
        cum = np.cumsum(c1s, axis=1)
        idx = np.argmax(cum >= K, axis=1)                     # first position where the count reaches K
        that = ws[np.arange(k), idx]
        Ahat = (c2 * np.minimum(wrows, that[:, None])).sum(axis=1) / M
        lL = np.log(Ahat) - math.log(1 + eta)
        U = Ahat / (1 - eta)
        if plan['rhat'] is not None:
            U = U + that * math.exp(plan['ltailfac'])
        ev = None
        if want_events:
            # the three events of the proof
            Pgt = (wrows > that[:, None]).mean(axis=1)
            Pge = (wrows >= that[:, None]).mean(axis=1)
            Emin = np.minimum(wrows, that[:, None]).mean(axis=1)
            e1 = Pgt <= plan['qplus'] * (1 + 1e-12)
            e2 = Pge >= plan['qminus'] * (1 - 1e-12)
            e3 = np.abs(Ahat - Emin) <= eta * Emin * (1 + 1e-12)
            ev = (e1, e2, e3)
        return lL, np.log(U), ev


def partA(seed):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    print("# Part A: Proposition K0 on u-Lipschitz functions of Q_d (own code)")
    print("#  d  u    x   delta'   brackets  invalid  too-wide  events-failed  invalid|events-ok  wide|events-ok  max ln(U/L)  cert   bound(4e^-..)  M")
    tot = dict(n=0, inv=0, wide=0, evf=0, inv_ok=0, wide_ok=0)
    for d in (9, 10, 11):
        for u in (0.5, 1.0, 2.0):
            fam = K0Family(d, u)
            for x in (0.5, 1.0, 2.0, 4.0):
                for dp in (0.3, 0.02):
                    plan = fam.plan(x, math.log(dp))
                    if plan['enum']:
                        print("%4d %.1f %4.1f %6.2f   enumeration (no radius qualifies)" % (d, u, x, dp))
                        continue
                    n_inv = n_wide = n_evf = n_inv_ok = n_wide_ok = n_tot = 0
                    maxw = 0.0
                    reps = 40
                    for kind in KINDS + ['mcshane_min', 'noise_reg', 'dips']:
                        psi = gen_psi(kind, d, max(1, d // 2), u, rng)
                        w = np.exp(-(psi - psi.min()))
                        wrows = np.repeat(w[None, :], reps, axis=0)
                        lL, lU, ev = fam.brackets(wrows, plan, rng, want_events=True)
                        lA = math.log(w.mean())
                        inv = (lL > lA + 1e-12) | (lU < lA - 1e-12)
                        wide = (lU - lL) > plan['cert'] + 1e-9
                        evok = ev[0] & ev[1] & ev[2]
                        n_tot += reps
                        n_inv += int(inv.sum())
                        n_wide += int(wide.sum())
                        n_evf += int((~evok).sum())
                        n_inv_ok += int((inv & evok).sum())
                        n_wide_ok += int((wide & evok).sum())
                        maxw = max(maxw, float((lU - lL)[evok].max()) if evok.any() else 0.0)
                    bound = 4 * math.exp(-plan['eta'] ** 2 * plan['K'] / (3 * (1 + plan['eta'])))
                    print("%4d %.1f %4.1f %6.2f  %7d  %7d  %7d  %10d  %14d  %14d   %8.4f  %6.4f  %9.3g  %d"
                          % (d, u, x, dp, n_tot, n_inv, n_wide, n_evf, n_inv_ok, n_wide_ok, maxw, plan['cert'], bound, plan['M']))
                    for k_, v_ in (('n', n_tot), ('inv', n_inv), ('wide', n_wide), ('evf', n_evf), ('inv_ok', n_inv_ok), ('wide_ok', n_wide_ok)):
                        tot[k_] += v_
    print("TOTAL: %d brackets; invalid %d; wider than certified %d; one of the three events failed %d; "
          "invalid on the three events %d; too wide on the three events %d   [%.0f s]"
          % (tot['n'], tot['inv'], tot['wide'], tot['evf'], tot['inv_ok'], tot['wide_ok'], time.time() - t0))


def partB(nruns, seed, tlimit):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    print("# Part B: Algorithm 2L+ with real inner brackets (Proposition K0 on each fibre), constants of the theorem")
    agg = dict(done=0, skipped=0, invalid=0, toowide=0, abort=0, viol=0, v1fail_calls=0, v1fail_runs=0, calls=0, enumrungs=0, rungs=0,
               gfail=0)
    maxw = 0.0
    minslack = 1e9
    maxfrac = 0.0
    violations = {}
    for it in range(nruns):
        if time.time() - t0 > tlimit:
            print("# time limit after %d runs" % it)
            break
        n_o, n_i = [(6, 6), (7, 6), (6, 7), (7, 5), (8, 5), (5, 7)][int(rng.integers(0, 6))]
        u = float(rng.choice([0.5, 1.0, 2.0]))
        n = n_o + n_i
        kind = KINDS[int(rng.integers(0, len(KINDS)))]
        psi = gen_psi(kind, n, n_o, u, rng)
        pop = PopEnum(psi, n, n_o, u, rng)
        lam = float(rng.uniform(0.3, 1.0))
        eta = [Fr(1, 2), Fr(1, 4)][int(rng.integers(0, 2))]
        etap = float(rng.choice([0.2, 1.0]))
        theta = float(rng.choice([0.2, 1.0, 5.0]))
        b = float(rng.choice([0.6, 1.0, 2.0]))
        nu1 = 2 * math.exp(u) * n_o / theta if rng.random() < 0.5 else 1.0
        L = int(rng.choice([1, 2, 3]))
        x0 = 2 * u * n_i
        xs = [x0] + [b * (x0 / b) ** (1 - (i + 1) / L) for i in range(L)]
        xs[-1] = b
        tab = get_tab(n_o, u)
        cs = Consts(tab, n, n_o, u, lam, eta, etap, theta, max(nu1, 1.0), b, 0.05, xs)
        fam = K0Family(n_i, u)
        plans = [None] + [fam.plan(xs[l], cs.ldeltap) for l in range(1, L + 1)]
        agg['rungs'] += L
        agg['enumrungs'] += sum(1 for p in plans[1:] if p['enum'])
        v1 = {'fail': 0, 'calls': 0, 'queries': 0}

        def orc(blk, sel, l, x, ls, bb):
            a = blk.aidx[sel]
            lL = np.empty(a.shape[0])
            lU = np.empty(a.shape[0])
            step = max(1, (1 << 22) // (1 << n_i))
            for s in range(0, a.shape[0], step):
                wr = pop.w[a[s:s + step]]
                l1, u1, _ = fam.brackets(wr, plans[l], rng)
                lL[s:s + step] = l1
                lU[s:s + step] = u1
            lw = blk.lW[sel]
            bad = (lL > lw + 1e-12) | (lU < lw - 1e-12) | (lU - lL > x + 1e-9)
            v1['fail'] += int(bad.sum())
            v1['calls'] += a.shape[0]
            v1['queries'] += a.shape[0] * plans[l]['cost']
            return lL, lU

        trace = run_2Lplus(cs, pop, pop.ls0, orc, rng, maxM_log2=22)
        if trace['skipped']:
            agg['skipped'] += 1
            continue
        agg['done'] += 1
        agg['calls'] += v1['calls']
        agg['v1fail_calls'] += v1['fail']
        agg['v1fail_runs'] += v1['fail'] > 0
        if trace['abort'] is not None:
            agg['abort'] += 1
            continue
        res = check_run(cs, pop, trace, pop.lA)
        st = trace['stop']
        if st['lL'] > pop.lA + 1e-9 or st['lU'] < pop.lA - 1e-9:
            agg['invalid'] += 1
        w = st['lU'] - st['lL']
        if w > cs.xout + 1e-9:
            agg['toowide'] += 1
        maxw = max(maxw, w)
        minslack = min(minslack, cs.xout - w)
        G = res.info['G_used'] and v1['fail'] == 0
        agg['gfail'] += (not G)
        if res.viol and G:
            agg['viol'] += 1
            for c in set(c for (c, d) in res.viol):
                violations[c] = violations.get(c, 0) + 1
        # number of evaluations against C_max
        lCmax_terms = [0.0, math.log(2) + cs.lMbar]
        for l in range(1, L + 1):
            lCmax_terms.append(min(math.log(2) + cs.lMbar, math.log(cs.J + 1) + cs.lcnt(xs[l - 1])) + math.log(plans[l]['cost']))
        mx = max(lCmax_terms)
        lCmax = mx + math.log(sum(math.exp(t - mx) for t in lCmax_terms))
        q = 1 + res.info['npoints'] + v1['queries']
        maxfrac = max(maxfrac, q / math.exp(lCmax))
        if q > math.exp(lCmax):
            agg['viol'] += 1
            violations['Cmax'] = violations.get('Cmax', 0) + 1
    print("runs completed %d (skipped %d); real inner brackets: %d; rungs served by enumeration: %d of %d"
          % (agg['done'], agg['skipped'], agg['calls'], agg['enumrungs'], agg['rungs']))
    print("final brackets invalid: %d; wider than x_out: %d; aborts: %d" % (agg['invalid'], agg['toowide'], agg['abort']))
    print("inner brackets invalid or wider than requested: %d (in %d runs); runs with the good event (V1)-(V3) failing: %d"
          % (agg['v1fail_calls'], agg['v1fail_runs'], agg['gfail']))
    print("runs with a violated claim of Theorem K1 on the good event: %d %s" % (agg['viol'], violations if violations else ''))
    print("widest final bracket ln(U/L) = %.3f; smallest distance to x_out = %.4f; largest (number of evaluations)/C_max = %.3g  [%.0f s]"
          % (maxw, minslack, maxfrac, time.time() - t0))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'A':
        partA(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
    else:
        partB(int(sys.argv[2]) if len(sys.argv) > 2 else 60, int(sys.argv[3]) if len(sys.argv) > 3 else 8,
              float(sys.argv[4]) if len(sys.argv) > 4 else 500.0)
