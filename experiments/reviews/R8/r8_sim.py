#!/usr/bin/env python3
"""Referee R8 -- Algorithm 2L+ with a simulated inner oracle (own code; D.12(i) and (iii) of the brief).

usage:  python3 r8_sim.py <engine> <nruns> <seed> [mutation|none] [Kdiv] [timelimit_s]
  engine  'enum'    : u-Lipschitz functions (15 non-radial and radial families) on enumerated cubes
                      Q_{n_o} x Q_{n_i}, n_o in 6..9, every outer point with its own bracket
          'radial'  : radial outer landscapes, n_o in 10..26, every point with its own bracket
          'grouped' : radial outer landscapes of medium size (u, n_o as listed below), exact samples of up to
                      2^61 points stored as counts per shell and block; bounded regime nu_1 = 2 e^u n_o / theta
          'neg'     : like 'radial'/'grouped' but with nu_1 = 1 and parameters aimed at the negligible branch
  mutation 'maxform' (lower end without the sum), 'noharper' (no Harper term), 'close_at_no' (tail lemma at
           r = n_o), 'neg_tol' (negligibility threshold without e^{-b}), 'q_plain' (q without 1/(1-eta))
  Kdiv    the constant K of the theorem is divided by Kdiv (>1: the good event fails often; the claims are
          then tested on the runs on which the events used by the proof hold)

Every run: the constants of section 2.2 from the formulas; the good event (V2),(V3) evaluated exactly on the
realised sample; every claim (i)-(vi) of Theorem K1 and the width; statistics of the branches taken.
"""
import sys, time, math
from fractions import Fraction as Fr
import numpy as np
from r8_core import Tables, Consts, run_2Lplus, check_run, oracle_sim, NEG_INF
from r8_pops import (gen_psi, KINDS, PopEnum, gen_profile, PROFILES, PopRadialPoints, PopRadialGroups)

RULES = ['rand', 'top', 'bot', 'mid', 'adv_hi', 'adv_lo', 'mixed']
_tab_cache = {}


def get_tab(m, u):
    key = (m, u)
    if key not in _tab_cache:
        _tab_cache[key] = Tables(m, u)
    return _tab_cache[key]


def make_oracle(rule, rng):
    def orc(blk, sel, l, x, ls, b):
        r = rule
        if r == 'mixed':
            r = RULES[int(rng.integers(0, 6))]
        return oracle_sim(r, blk.lW[sel], blk.lL[sel], blk.lU[sel], x, ls, b, rng)
    return orc


def ladder(rng, u, n_i, b, L):
    x0 = 2 * u * n_i
    xL = b * (1.0 if rng.random() < 0.6 else rng.uniform(0.5, 1.0))
    if L == 1:
        return [x0, xL]
    # geometric interior rungs between xL and x0
    t = np.sort(rng.uniform(0.15, 0.85, L - 1))[::-1]
    mid = [xL * (x0 / xL) ** float(tt) for tt in t]
    xs = [x0] + mid + [xL]
    for i in range(len(xs) - 1):
        assert xs[i] > xs[i + 1]
    return xs


def one_run(engine, rng, mutation, Kdiv, maxlog2):
    desc = {}
    if engine == 'enum':
        n_o = int(rng.choice([6, 7, 8, 9]))
        n_i = int(rng.choice([3, 4, 5]))
        u = float(rng.choice([0.5, 1.0, 1.5, 2.0]))
        kind = KINDS[int(rng.integers(0, len(KINDS)))]
        n = n_o + n_i
        psi = gen_psi(kind, n, n_o, u, rng)
        pop = PopEnum(psi, n, n_o, u, rng)
        desc['inst'] = '%s Q%dxQ%d u=%.1f' % (kind, n_o, n_i, u)
        nu1_bounded = rng.random() < 0.5
    elif engine in ('radial', 'grouped', 'neg'):
        if engine == 'radial':
            n_o = int(rng.choice([10, 12, 14, 16, 18, 20, 22, 26]))
            u = float(rng.choice([0.5, 1.0, 1.5, 2.0]))
            nu1_bounded = rng.random() < 0.5
        elif engine == 'grouped':
            u, n_o = [(0.5, 240), (0.5, 380), (0.5, 520), (1.0, 90), (1.0, 130), (1.0, 170), (2.0, 34), (2.0, 44), (2.0, 54)][int(rng.integers(0, 9))]
            nu1_bounded = True
        else:
            u, n_o = [(1.5, 34), (1.5, 40), (2.0, 34), (2.0, 40), (2.0, 46), (1.0, 60)][int(rng.integers(0, 6))]
            nu1_bounded = False
        n_i = int(rng.choice([3, 4]))
        n = n_o + n_i
        kind = PROFILES[int(rng.integers(0, len(PROFILES)))]
        if engine == 'neg':
            kind = ['flat', 'flatbottom', 'mesa', 'dip', 'walk', 'periodic'][int(rng.integers(0, 6))]
        f = gen_profile(kind, n_o, u, rng)
        inner = ['zero', 'cone', 'anticone'][int(rng.integers(0, 3))]
        cls = PopRadialPoints if engine == 'radial' else PopRadialGroups
        pop = cls(f, n_o, n_i, u, rng, inner)
        desc['inst'] = '%s n_o=%d n_i=%d u=%.1f inner=%s d0=%d' % (kind, n_o, n_i, u, inner, pop.d0)
    elif engine in ('k1b', 'unif'):
        # 'k1b': the parameters of Corollary K1.b (lam=1, eta=1/2, eta'=1, nu_1=1, theta exponentially large)
        # 'unif': the parameters of Theorem K2 (lam=eta=eta'=theta=c0 small, nu_1=2e^u n_o/theta)
        u, n_o = [(0.5, 200), (1.0, 70), (1.0, 110), (2.0, 34), (2.0, 46)][int(rng.integers(0, 5))]
        n_i = int(rng.choice([3, 4]))
        n = n_o + n_i
        kind = PROFILES[int(rng.integers(0, len(PROFILES)))]
        f = gen_profile(kind, n_o, u, rng)
        inner = ['zero', 'cone', 'anticone'][int(rng.integers(0, 3))]
        pop = PopRadialGroups(f, n_o, n_i, u, rng, inner)
        desc['inst'] = '%s n_o=%d n_i=%d u=%.1f inner=%s d0=%d' % (kind, n_o, n_i, u, inner, pop.d0)
        if engine == 'k1b':
            lam, eta, etap, nu1 = 1.0, Fr(1, 2), 1.0, 1.0
            b = float(rng.choice([0.5, 2.0, 6.0]))
            theta = math.exp(float(rng.choice([2.0, 5.0, 10.0, 20.0, 40.0])))
        else:
            c0 = float(rng.choice([0.1, 0.05, 0.025]))
            lam, eta, etap, theta = c0 * (1 + 0.013 * rng.random()), Fr(c0).limit_denominator(1000), c0, c0
            b = 6 * c0            # (lam is perturbed so that no fibre average sits exactly on a level: a
                                  #  floating-point tie would make the simulated bracket [W, W e^b] straddle)
            nu1 = 2 * math.exp(u) * n_o / theta
        L = int(rng.choice([1, 2, 3]))
        x0 = 2 * u * n_i
        b = min(b, 0.5 * x0)
        tt = np.sort(rng.uniform(0.15, 0.85, L - 1))[::-1]
        xs = [x0] + [b * (x0 / b) ** float(t_) for t_ in tt] + [b]
        tab = get_tab(n_o, u)
        cs = Consts(tab, n, n_o, u, lam, eta, etap, theta, nu1, b, 0.05, xs)
        if Kdiv > 1:
            cs = Consts(tab, n, n_o, u, lam, eta, etap, theta, nu1, b, 0.05, xs, Koverride=max(2, cs.K // Kdiv))
        rule = RULES[int(rng.integers(0, len(RULES)))]
        desc['par'] = 'lam=%.3f eta=%s etap=%.3f theta=%.3g b=%g L=%d K=%d J=%d rdag=%d rule=%s xout=%.3f' % (
            lam, eta, etap, theta, b, L, cs.K, cs.J, cs.rdag, rule, cs.xout)
        trace = run_2Lplus(cs, pop, pop.ls0, make_oracle(rule, rng), rng, mutation=mutation, maxM_log2=maxlog2)
        return cs, pop, trace, desc
    else:
        raise ValueError(engine)
    # parameters
    lam = float(rng.uniform(0.2, 1.0))
    eta = [Fr(1, 2), Fr(1, 4), Fr(1, 3)][int(rng.integers(0, 3))]
    etap = float(rng.choice([0.1, 0.5, 1.0]))
    b = float(rng.choice([0.2, 0.5, 1.0, 2.5]))
    if engine == 'grouped':
        theta = float(rng.choice([0.1, 0.3, 1.0]))
        lam = float(rng.uniform(0.4, 1.0))
        b = float(rng.choice([0.2, 0.5, 1.0]))
    elif engine == 'neg':
        theta = float(rng.choice([0.5, 2.0, 8.0]))
    else:
        theta = float(rng.choice([0.05, 0.3, 1.0, 5.0, 50.0]))
    nu1 = 2 * math.exp(u) * n_o / theta if nu1_bounded else 1.0
    nu1 = max(nu1, 1.0)
    L = int(rng.choice([1, 2, 3]))
    xs = ladder(rng, u, n_i, b, L)
    delta = 0.05
    tab = get_tab(n_o, u)
    cs = Consts(tab, n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs)
    if Kdiv > 1:
        cs = Consts(tab, n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, Koverride=max(2, cs.K // Kdiv))
    rule = RULES[int(rng.integers(0, len(RULES)))]
    desc['par'] = 'lam=%.2f eta=%s etap=%.1f theta=%g b=%g nu1=%s L=%d K=%d J=%d rdag=%d rule=%s' % (
        lam, eta, etap, theta, b, 'bdd' if nu1_bounded else '1', L, cs.K, cs.J, cs.rdag, rule)
    trace = run_2Lplus(cs, pop, pop.ls0, make_oracle(rule, rng), rng, mutation=mutation, maxM_log2=maxlog2)
    return cs, pop, trace, desc


def main():
    engine = sys.argv[1]
    nruns = int(sys.argv[2])
    seed = int(sys.argv[3])
    mutation = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != 'none' else None
    Kdiv = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    tlimit = float(sys.argv[6]) if len(sys.argv) > 6 else 540.0
    rng = np.random.default_rng(seed)
    maxlog2 = 61 if engine in ('grouped', 'neg', 'k1b', 'unif') else 23
    t0 = time.time()
    agg = dict(done=0, skipped=0, G_used_fail=0, G_full_fail=0, viol_runs_G=0, viol_runs_notG=0, npop=0, nneg=0,
               runs_with_neg=0, clos_empty=0, clos_pop=0, clos_unpop=0, clos_le_rdag=0, clos_le_no2=0)
    by_claim_G = {}
    by_claim_notG = {}
    max_width = -1e9
    min_slack = 1e9
    worst_count = 0.0
    max_neg_share = 0.0
    maxM_Mdag = 0.0
    max_points = 0
    examples = []
    print("# engine=%s nruns=%d seed=%d mutation=%s Kdiv=%d" % (engine, nruns, seed, mutation, Kdiv))
    for it in range(nruns):
        if time.time() - t0 > tlimit:
            print("# time limit reached after %d runs" % it)
            break
        cs, pop, trace, desc = one_run(engine, rng, mutation, Kdiv, maxlog2)
        if trace['skipped']:
            agg['skipped'] += 1
            continue
        res = check_run(cs, pop, trace, pop.lA)
        agg['done'] += 1
        info = res.info
        G = info['G_used']
        agg['G_used_fail'] += (not G)
        agg['G_full_fail'] += (not info['G_full'])
        claims = sorted(set(c for (c, d) in res.viol))
        if claims:
            if G:
                agg['viol_runs_G'] += 1
                for c in claims:
                    by_claim_G[c] = by_claim_G.get(c, 0) + 1
            else:
                agg['viol_runs_notG'] += 1
                for c in claims:
                    by_claim_notG[c] = by_claim_notG.get(c, 0) + 1
            if len(examples) < 6:
                examples.append((desc, res.viol[:3], G))
        agg['npop'] += info['npop']
        agg['nneg'] += info['nneg']
        agg['runs_with_neg'] += info['nneg'] > 0
        if 'closure' in info:
            agg['clos_' + info['closure']] += 1
            r = info['closure_r']
            if r is not None:
                agg['clos_le_rdag'] += (r <= cs.rdag)
                agg['clos_le_no2'] += (r <= cs.n_o - 2)
            max_width = max(max_width, info['width'])
            min_slack = min(min_slack, info['width_slack'])
            max_neg_share = max(max_neg_share, info['neg_share'])
        worst_count = max(worst_count, info['worst_count'])
        maxM_Mdag = max(maxM_Mdag, info['maxM_over_Mdag'])
        max_points = max(max_points, info['npoints'])
    el = time.time() - t0
    print("runs completed %d, skipped (sample too large for the simulation) %d   [%.0f s]" % (agg['done'], agg['skipped'], el))
    print("good event: events used by the proof failed in %d runs; (V2),(V3) at all levels and realised sizes failed in %d runs"
          % (agg['G_used_fail'], agg['G_full_fail']))
    print("runs with a violated claim: %d on the good event, %d off it" % (agg['viol_runs_G'], agg['viol_runs_notG']))
    print("  violated claims on the good event: %s" % (by_claim_G if by_claim_G else 'none'))
    print("  violated claims off the good event: %s" % (by_claim_notG if by_claim_notG else 'none'))
    print("levels left as populated %d, as negligible %d (in %d runs)" % (agg['npop'], agg['nneg'], agg['runs_with_neg']))
    print("closures: empty tail %d, at a populated pass %d, at an unpopulated pass %d; by the tail lemma at r <= n_o-2: %d, at r <= r_dagger: %d"
          % (agg['clos_empty'], agg['clos_pop'], agg['clos_unpop'], agg['clos_le_no2'], agg['clos_le_rdag']))
    print("widest bracket ln(U/L) = %.3f; smallest distance to the width bound = %.4f; count/bound max = %.3f; "
          "negligible part / budget max = %.4f; max M/M_dagger = %.2f; largest sample = %.3g points"
          % (max_width, min_slack, worst_count, max_neg_share, maxM_Mdag, max_points))
    for (desc, v, G) in examples:
        print("  example (good event %s): %s | %s | %s" % (G, desc['inst'], desc['par'], v))


if __name__ == '__main__':
    main()
