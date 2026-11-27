#!/usr/bin/env python3
"""Referee R8 -- THREE nested levels, end to end, on cubes small enough to enumerate for the truth
(not done by the author nor by the earlier referee).  Own code.

  Q_n = Q_{n_o} x Q_{n_i},  Q_{n_i} = Q_{n_o'} x Q_{n_i'}.
  outer : Algorithm 2L+ in dimension n; its inner procedure I_l for the rung of accuracy x_l is
  middle: Algorithm 2L+ in dimension n_i, with parameters chosen so that its certified accuracy x_out is
          at most x_l (Corollary-K1.b style, theta large, when x_l is large; Theorem-K2 style, all four
          constants equal to c_0 = min(x_l/12, 1/3) and tolerance x_l/2, otherwise), failure probability
          delta' = delta/(4 L Mbar) of the outer algorithm, and as its own inner procedure
  bottom: the two-sample bracket of Proposition K0 on Q_{n_i'} (or enumeration where no radius qualifies).
All constants are those of the theorems.  The middle runs are real runs of Algorithm 2L+ on the fibres; to keep
the run time down, for every (fibre, rung) a pool of POOL independent middle runs is made and each outer point
draws its bracket from the pool of its fibre (so the outer points do not have fully independent inner
randomness; every bracket is a real output of the middle algorithm).

Checked: every middle run (validity, width <= its x_out <= x_l, all claims of Theorem K1 on its good event, abort
never); the outer run (validity, width, all claims of Theorem K1 on its good event); number of evaluations of
the outer run (with the costs of the middle runs actually made for the brackets drawn) against the outer C_max
computed with C_l = C_max of the middle algorithm.

usage: python3 r8_three.py [ninstances] [seed] [timelimit_s]
"""
import sys, time, math
from fractions import Fraction as Fr
import numpy as np
from r8_core import Tables, Consts, run_2Lplus, check_run, Block, NEG_INF
from r8_pops import gen_psi, KINDS, PopEnum
from r8_e2e import K0Family

POOL = 40
_tabs = {}


def get_tab(m, u):
    if (m, u) not in _tabs:
        _tabs[(m, u)] = Tables(m, u)
    return _tabs[(m, u)]


def middle_params(x, u, n_i, n_o2):
    """parameters of the middle 2L+ with certified accuracy <= x"""
    n_i2 = n_i - n_o2
    pu2 = 2 / (1 + math.exp(u))
    x0 = 2 * u * n_i2
    b = min(x / 2, 0.9 * x0)
    if x - b >= math.log(3 * math.e + 2) + 0.05:
        lam, eta, etap, nu1 = 1.0, Fr(1, 2), 1.0, 1.0
        theta = math.exp(x - b) - (3 * math.e + 1) - pu2 ** n_i * math.exp(-b)
        style = 'K1.b'
    else:
        c0 = min((x - b) / 6, 1 / 3)
        eta = Fr(max(1, int(c0 * 64)), 64)
        lam, etap, theta = c0, c0, c0
        nu1 = 2 * math.exp(u) * n_o2 / theta
        style = 'K2'
    xs = [x0, b]
    return lam, eta, etap, theta, nu1, b, xs, style


def lCmax(cs, lcosts):
    """log C_max of Theorem K1 for inner costs with logs lcosts[1..L]"""
    terms = [0.0, math.log(2) + cs.lMbar]
    for l in range(1, cs.L + 1):
        terms.append(min(math.log(2) + cs.lMbar, math.log(cs.J + 1) + cs.lcnt(cs.xs[l - 1])) + lcosts[l])
    m = max(terms)
    return m + math.log(sum(math.exp(t - m) for t in terms))


def main():
    ninst = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    tlimit = float(sys.argv[3]) if len(sys.argv) > 3 else 520.0
    rng = np.random.default_rng(seed)
    t0 = time.time()
    agg = dict(inst=0, mid_runs=0, mid_invalid=0, mid_wide=0, mid_abort=0, mid_viol=0, mid_gfail=0, out_invalid=0, out_wide=0,
               out_abort=0, out_viol=0, out_gfail=0, bottom_real=0, bottom_enum=0, bottom_calls=0, bottom_bad=0, cost_viol=0)
    maxfrac = 0.0
    print("# three nested levels: outer 2L+ / middle 2L+ / bottom K0; constants of the theorems; pool of %d middle runs per (fibre, rung)" % POOL)
    for it in range(ninst):
        if time.time() - t0 > tlimit:
            print("# time limit after %d instances" % it)
            break
        n_o, n_o2, n_i2 = [(3, 3, 3), (3, 3, 4), (4, 3, 3), (3, 4, 3)][int(rng.integers(0, 4))]
        n_i = n_o2 + n_i2
        n = n_o + n_i
        u = float(rng.choice([0.5, 1.0]))
        kind = KINDS[int(rng.integers(0, len(KINDS)))]
        psi = gen_psi(kind, n, n_o, u, rng)
        pop = PopEnum(psi, n, n_o, u, rng)
        # outer parameters
        lam = float(rng.uniform(0.5, 1.0))
        eta = [Fr(1, 2), Fr(1, 3)][int(rng.integers(0, 2))]
        etap = float(rng.choice([0.5, 1.0]))
        theta = float(rng.choice([0.5, 2.0]))
        b = float(rng.choice([2.5, 3.5]))
        x0 = 2 * u * n_i
        Lout = int(rng.choice([1, 2])) if x0 > 2.2 * b else 1
        if b >= x0:
            b = 0.8 * x0
        xs = [x0, b] if Lout == 1 else [x0, math.sqrt(x0 * b), b]
        nu1 = 2 * math.exp(u) * n_o / theta if rng.random() < 0.5 else 1.0
        cs = Consts(get_tab(n_o, u), n, n_o, u, lam, eta, etap, theta, nu1, b, 0.05, xs)
        # middle algorithm for every rung, bottom family
        fam = K0Family(n_i2, u)
        mids = [None]
        for l in range(1, Lout + 1):
            mlam, meta, metap, mtheta, mnu1, mb, mxs, style = middle_params(xs[l], u, n_i, n_o2)
            mcs = Consts(get_tab(n_o2, u), n_i, n_o2, u, mlam, meta, metap, mtheta, mnu1, mb, math.exp(cs.ldeltap), mxs)
            assert mcs.xout <= xs[l] + 1e-9, (mcs.xout, xs[l])
            plans = [None] + [fam.plan(mxs[k], mcs.ldeltap) for k in range(1, mcs.L + 1)]
            lc = lCmax(mcs, [None] + [math.log(p['cost']) for p in plans[1:]])
            mids.append(dict(cs=mcs, plans=plans, lCmax=lc, style=style))
            for p in plans[1:]:
                agg['bottom_enum' if p['enum'] else 'bottom_real'] += 1
        # pools of middle runs
        fib = psi.reshape(1 << n_o, 1 << n_i)
        pools = {}
        for a in range(1 << n_o):
            mpop_psi = fib[a]
            for l in range(1, Lout + 1):
                md = mids[l]
                res_list = []
                for rep in range(POOL):
                    mpop = PopEnum(mpop_psi, n_i, n_o2, u, rng)
                    q = {'n': 0, 'bad': 0, 'calls': 0}

                    def orc(blk, sel, k, x, ls, bb, mpop=mpop, md=md, q=q):
                        aa = blk.aidx[sel]
                        l1, u1, _ = fam.brackets(mpop.w[aa], md['plans'][k], rng)
                        lw = blk.lW[sel]
                        q['bad'] += int(((l1 > lw + 1e-12) | (u1 < lw - 1e-12) | (u1 - l1 > x + 1e-9)).sum())
                        q['n'] += aa.shape[0] * md['plans'][k]['cost']
                        q['calls'] += aa.shape[0]
                        return l1, u1
                    tr = run_2Lplus(md['cs'], mpop, mpop.ls0, orc, rng, maxM_log2=24)
                    agg['mid_runs'] += 1
                    agg['bottom_calls'] += q['calls']
                    agg['bottom_bad'] += q['bad']
                    if tr['stop'] is None:
                        agg['mid_abort'] += 1
                        lo, hi = mpop.ls0, mpop.ls0 + 2 * u * n_i
                        cost = 1 + q['n']
                    else:
                        chk = check_run(md['cs'], mpop, tr, mpop.lA)
                        st = tr['stop']
                        lo, hi = st['lL'], st['lU']
                        G = chk.info['G_used'] and q['bad'] == 0
                        agg['mid_gfail'] += (not G)
                        if lo > mpop.lA + 1e-9 or hi < mpop.lA - 1e-9:
                            agg['mid_invalid'] += 1
                        if hi - lo > md['cs'].xout + 1e-9:
                            agg['mid_wide'] += 1
                        if chk.viol and G:
                            agg['mid_viol'] += 1
                            print("   middle violation:", chk.viol[:3])
                        cost = 1 + chk.info['npoints'] + q['n']
                        if math.log(cost) > md['lCmax'] + 1e-9:
                            agg['cost_viol'] += 1
                    res_list.append((lo, hi, cost))
                pools[(a, l)] = res_list
        # outer run with brackets drawn from the pools
        oq = {'n': 0, 'bad': 0}

        def oorc(blk, sel, l, x, ls, bb):
            aa = blk.aidx[sel]
            pick = rng.integers(0, POOL, aa.shape[0])
            lL = np.empty(aa.shape[0])
            lU = np.empty(aa.shape[0])
            for i in range(aa.shape[0]):
                lo, hi, cost = pools[(int(aa[i]), l)][int(pick[i])]
                lL[i] = lo
                lU[i] = hi
                oq['n'] += cost
            lw = blk.lW[sel]
            oq['bad'] += int(((lL > lw + 1e-9) | (lU < lw - 1e-9) | (lU - lL > x + 1e-9)).sum())
            return lL, lU
        tr = run_2Lplus(cs, pop, pop.ls0, oorc, rng, maxM_log2=22)
        agg['inst'] += 1
        if tr['skipped']:
            print("   outer run skipped (too many points)")
            continue
        if tr['stop'] is None:
            agg['out_abort'] += 1
            continue
        chk = check_run(cs, pop, tr, pop.lA)
        st = tr['stop']
        G = chk.info['G_used'] and oq['bad'] == 0
        agg['out_gfail'] += (not G)
        if st['lL'] > pop.lA + 1e-9 or st['lU'] < pop.lA - 1e-9:
            agg['out_invalid'] += 1
        if st['lU'] - st['lL'] > cs.xout + 1e-9:
            agg['out_wide'] += 1
        if chk.viol and G:
            agg['out_viol'] += 1
            print("   outer violation:", chk.viol[:3])
        lco = lCmax(cs, [None] + [mids[l]['lCmax'] for l in range(1, Lout + 1)])
        tot = 1 + chk.info['npoints'] + oq['n']
        frac = math.exp(math.log(tot) - lco)
        maxfrac = max(maxfrac, frac)
        if frac > 1:
            agg['cost_viol'] += 1
        print("  instance %2d: %s Q%dx(Q%dxQ%d) u=%.1f | outer: L=%d b=%.2f x_out=%.3f width=%.3f points=%d stop level %d | middle styles %s, x_out %s | evaluations/C_max = %.2e  [%.0f s]"
              % (it, kind, n_o, n_o2, n_i2, u, Lout, b, cs.xout, st['lU'] - st['lL'], chk.info['npoints'], st['j'],
                 [mids[l]['style'] for l in range(1, Lout + 1)], ['%.2f' % mids[l]['cs'].xout for l in range(1, Lout + 1)], frac,
                 time.time() - t0))
        sys.stdout.flush()
    print("instances %d; middle runs %d: invalid %d, wider than certified %d, aborts %d, claim violations on the good event %d, good event failed %d"
          % (agg['inst'], agg['mid_runs'], agg['mid_invalid'], agg['mid_wide'], agg['mid_abort'], agg['mid_viol'], agg['mid_gfail']))
    print("bottom brackets %d (rungs with a real two-sample bracket %d, by enumeration %d), invalid or too wide %d"
          % (agg['bottom_calls'], agg['bottom_real'], agg['bottom_enum'], agg['bottom_bad']))
    print("outer runs: invalid %d, wider than x_out %d, aborts %d, claim violations on the good event %d, good event failed %d; "
          "cost above C_max %d (largest evaluations/C_max = %.2e)   [%.0f s]"
          % (agg['out_invalid'], agg['out_wide'], agg['out_abort'], agg['out_viol'], agg['out_gfail'], agg['cost_viol'], maxfrac, time.time() - t0))


if __name__ == '__main__':
    main()
