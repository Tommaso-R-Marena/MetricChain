#!/usr/bin/env python3
"""Three nested levels of Algorithm 2L+: the CERTIFIED cost bound, with the server of every rung chosen by certified cost.

Background (theory report section 11.19, remark (1); THY-RES-0013).  Our referee R8 computed the exact cost of three
nested levels at the flat instance (experiments/reviews/R8/r8_flat3.py): every rung of the outer ladder is served by
the cheaper of the base bracket (Proposition K0) and a two-level run on the fibre, "cheaper" meaning cheaper AT THE
FLAT FIBRE.  The Computational Research Division then showed (ENG-RES-0014) that away from the flat instance most of
the advantage of the third level disappears, and that with every middle run charged its own certified bound C_max
this three-level design gains nothing over two levels at n = 1000, 4000, 16000.

This script evaluates, with the referee's own routines (r8_flat.flat_run, k0_plan_flat; nothing is re-implemented),
the certified bound C_max of the outer level (Theorem 11.56; it depends on the inner procedures through their cost
bounds only, not through where their brackets fall) for three ways of choosing the server of a rung:

  flat      - the referee's design: servers chosen and charged at the flat fibre.  Its C_max is the referee's column
              "C_max of three levels" and is NOT a certified bound (the engineering division's remark);
  cert      - the same servers, every middle run charged its own C_max: the engineering division's certified column
              (reproduced here to the digit: a check of both implementations);
  tuned     - servers chosen BY CERTIFIED COST among the referee's candidates: a rung is served by a two-level run
              only if that run's C_max is below the (deterministic) cost of the base bracket, and of the candidate
              middle designs the one with the smallest C_max is taken;
  searched  - the same rule with more candidates: in addition to the referee's, the bounded-accuracy design
              (lam = eta = eta' = theta = c = min(x/12, 1/3)) is offered at EVERY accuracy x, with the tolerance of
              the middle run either x/2 or as large as the accuracy allows (b = x - ln(e^c (1+c)/(1-c) + 2c)), and
              with the outer fraction of the middle run found by descent on a grid of step 0.05 from 0.50;
  tunedflat, searchedflat - the exact cost AT THE FLAT INSTANCE of the algorithms of 'tuned' and 'searched' (not
              bounds; for comparison with the referee's flat-instance figures, and a consistency check: a cost must
              not exceed its bound).

Why 'tuned' and 'searched' are certified bounds: Theorem 11.56 states its cost bound for arbitrary inner bracket
procedures "with costs C_l", and the bound holds in every run (the algorithm aborts with the trivial bracket before
a call would exceed it); so a two-level run is itself an inner procedure with cost C_max, and the theorem applies
again one level up.  The cost of the base bracket K0 is fixed by its design (two samples of prescribed sizes) and is
its own bound.  Which procedure serves which rung is decided here, before any evaluation, from the design alone.
Every candidate is checked to have certified accuracy at most x (r['xout'] <= x); offering more candidates can only
lower the bound.

usage:  python3 cert3.py <n,n,...> <phi1,phi1,...> [modes, default flat,cert,tuned,tunedflat]      (u = 1)
Run from this directory or from anywhere; output lines give ln(cost or bound)/(n a), a = ln 2 - H(1/(1 + e^u)).
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reviews", "R8"))
import r8_flat as F          # noqa: E402
import r8_flat3 as F3        # noqa: E402

ALL_MODES = ('flat', 'cert', 'tuned', 'tunedflat', 'searched', 'searchedflat')
_cache = {}


def run2(u, d, p2, name, **kw):
    """a two-level run in dimension d (r8_flat.flat_run), cached; 'name' describes the design in the output"""
    key = (u, d, p2) + tuple(sorted(kw.items()))
    if key not in _cache:
        r = F.flat_run(u, d, p2, **kw)
        r['design'] = name
        _cache[key] = r
    return _cache[key]


def acc_const(c):
    """what one level adds to its tolerance at lam = eta = eta' = theta = c:  ln(e^lam (1+eta)/(1-eta) + eta' + theta)"""
    return math.log(math.exp(c) * (1 + c) / (1 - c) + 2 * c)


def referee_candidates(u, d, x, ldeltap):
    """the middle designs of r8_flat3.py for a rung of accuracy x in dimension d"""
    cands = []
    g = x / d
    if x >= 8:
        bm = x / 4
        lth = (x - bm) + math.log1p(-(3 * math.e + 1 + (2 / (1 + math.exp(u))) ** d * math.exp(-bm)) * math.exp(-(x - bm)))
        p0 = min(0.7, max(0.05, g / (g + F3.theta_hint(u, g))))
        for p2 in (p0, min(0.8, 1.5 * p0)):
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                continue
            cands.append(run2(u, d, p2, 'extensive (lam=1, eta=1/2, b=x/4), phi_2=%.3f' % p2, lam=1.0, eta=0.5, etap=1.0,
                              b=bm, Lr=30, bounded=False, ltheta=lth, ldelta=ldeltap))
    else:
        c = min(x / 12, 1 / 3)
        cands.append(run2(u, d, 0.55, 'bounded (c=%.3f, b=x/2), phi_2=0.55' % c, lam=c, eta=c, etap=c, theta=c, b=x / 2,
                          Lr=30, bounded=True, ldelta=ldeltap))
    return cands


def bounded_candidates(u, d, x, ldeltap):
    """added here: the bounded-accuracy design at every accuracy x; two tolerances; outer fraction by descent from 0.50"""
    c = min(x / 12, 1 / 3)
    bmax = x - acc_const(c) - 1e-6
    cands = []
    for bm, bname in ((x / 2, 'x/2'), (bmax, 'max')):
        if bm <= 0 or bm > bmax:
            continue
        prev = None
        for p2 in (0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20):
            if 2 * u * (d - int(p2 * d)) <= bm * 1.5:
                break
            r = run2(u, d, p2, 'bounded (c=%.3f, b=%s), phi_2=%.2f' % (c, bname, p2), lam=c, eta=c, etap=c, theta=c, b=bm,
                     Lr=30, bounded=True, ldelta=ldeltap)
            if r['xout'] > x + 1e-9:
                break
            if prev is not None and r['lCmax'] >= prev:
                break
            cands.append(r)
            prev = r['lCmax']
    return cands


def make_inner(u, mode, chosen=None):
    """the inner family of the outer level: for a rung (dimension d, accuracy x, failure probability e^ldeltap) the
    tuple (log cost charged, log L, log U, kind) that r8_flat.flat_run expects.  'chosen', if a list, receives one
    entry (x, log cost of K0, design of the best two-level candidate or None, its log C_max, its log flat cost,
    served by it?) per rung."""
    est = math.log(math.cosh(u / 2))
    pu = 1 / (1 + math.exp(u))
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    by_bound = mode in ('tuned', 'tunedflat', 'searched', 'searchedflat')
    charge_bound = mode in ('cert', 'tuned', 'searched')

    def inner(d, x, ldeltap):
        c0, a0, b0, kind0 = F.k0_plan_flat(d, u, x, ldeltap)
        best = (c0, a0, b0, kind0)
        g = x / d
        if g >= 0.9 * est or d < 50:
            if chosen is not None:
                chosen.append((x, c0, None, None, None, False))
            return best
        cands = list(referee_candidates(u, d, x, ldeltap))
        # a two-level run with outer fraction phi_2 >= 0.2 and bounded theta has a sample cap of at least e^{0.2 d a}:
        # where the base bracket is cheaper than that, the added candidates cannot win and are not computed
        if mode in ('searched', 'searchedflat') and c0 > 0.2 * d * a:
            cands += bounded_candidates(u, d, x, ldeltap)
        for r in cands:
            assert r['xout'] <= x + 1e-9, (r['xout'], x)
            assert r['width'] <= r['xout'] + 1e-9 and r['lL'] <= 1e-12 and r['lU'] >= -1e-12
            assert r['lcost'] <= r['lCmax'] + 1e-9
        if not cands:
            if chosen is not None:
                chosen.append((x, c0, None, None, None, False))
            return best
        cm = min(cands, key=lambda r: r['lCmax'] if by_bound else r['lcost'])
        use = (cm['lCmax'] if by_bound else cm['lcost']) < c0
        if chosen is not None:
            chosen.append((x, c0, cm['design'], cm['lCmax'], cm['lcost'], use))
        if use:
            return (cm['lCmax'] if charge_bound else cm['lcost'], cm['lL'], cm['lU'], '2L+')
        return best
    return inner


def main():
    u = 1.0
    pu = 1 / (1 + math.exp(u))
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    ns = [int(v) for v in sys.argv[1].split(',')]
    phis = [float(v) for v in sys.argv[2].split(',')]
    modes = sys.argv[3].split(',') if len(sys.argv) > 3 else ['flat', 'cert', 'tuned', 'tunedflat']
    assert all(m in ALL_MODES for m in modes), modes
    nan = float('nan')
    for n in ns:
        t0 = time.time()
        rows = []
        for phi in phis:
            _cache.clear()
            r2 = F.flat_run(u, n, phi)
            na = n * a
            o = dict(two_flat=r2['lcost'] / na, two_cmax=r2['lCmax'] / na, ref_flat=nan, ref_cmax_flat=nan, cert=nan,
                     tuned=nan, tuned_flat=nan, searched=nan, searched_flat=nan)
            if 'flat' in modes:
                r = F.flat_run(u, n, phi, inner=make_inner(u, 'flat'))
                o['ref_flat'], o['ref_cmax_flat'] = r['lcost'] / na, r['lCmax'] / na
            if 'cert' in modes:
                o['cert'] = F.flat_run(u, n, phi, inner=make_inner(u, 'cert'))['lCmax'] / na
            for mode, key in (('tuned', 'tuned'), ('searched', 'searched')):
                if mode in modes:
                    o[key] = F.flat_run(u, n, phi, inner=make_inner(u, mode))['lCmax'] / na
                if mode + 'flat' in modes:
                    r = F.flat_run(u, n, phi, inner=make_inner(u, mode + 'flat'))
                    o[key + '_flat'] = r['lcost'] / na
                    assert r['lL'] <= 1e-12 and r['lU'] >= -1e-12 and r['width'] <= r['xout'] + 1e-9   # a valid bracket of Z = 1
                    if mode in modes:
                        assert o[key + '_flat'] <= o[key] + 1e-12, (o[key + '_flat'], o[key])          # cost <= its bound
            if 'tuned' in modes and 'searched' in modes:
                assert o['searched'] <= o['tuned'] + 1e-12                                              # more candidates
            if 'tuned' in modes:
                assert o['tuned'] <= o['two_cmax'] + 1e-12          # chosen by certified cost, a level cannot raise the bound
            rows.append(o)
            print("n=%d phi_1=%.3f: two levels: flat %.4f, C_max %.4f | three levels, servers chosen at the flat fibre:"
                  " flat %.4f, C_max with flat middle costs %.4f, certified C_max %.4f | servers chosen by certified cost:"
                  " flat %.4f, certified C_max %.4f | the same with more middle designs: flat %.4f, certified C_max %.4f"
                  "   [%.0f s]"
                  % (n, phi, o['two_flat'], o['two_cmax'], o['ref_flat'], o['ref_cmax_flat'], o['cert'], o['tuned_flat'],
                     o['tuned'], o['searched_flat'], o['searched'], time.time() - t0), flush=True)

        def best(key):
            vals = [r[key] for r in rows if r[key] == r[key]]
            return min(vals) if vals else nan

        print("n=%d best over these outer fractions: two levels: flat %.4f, C_max %.4f | three levels, servers chosen at"
              " the flat fibre: flat %.4f, certified C_max %.4f | servers chosen by certified cost: flat %.4f,"
              " certified C_max %.4f | the same with more middle designs: flat %.4f, certified C_max %.4f"
              % (n, best('two_flat'), best('two_cmax'), best('ref_flat'), best('cert'), best('tuned_flat'), best('tuned'),
                 best('searched_flat'), best('searched')), flush=True)


if __name__ == '__main__':
    main()
