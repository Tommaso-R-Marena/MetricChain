#!/usr/bin/env python3
"""R18, item 2 -- ENG-RES-0014 §4 at the level it is stated (mean runs), with my own evaluator (r18_mean.py).

Claim under test.  For an instance with the same law of fibre averages (and the same reference value) whose
fibres sit at places t0(a) in [lo, hi], with either uniform inner behaviour:
  (a) the classification shift is the same, so the sample sizes are those of the product instance;
  (b) the window of an atom at rung l -> l+1 is inside  W e^{b - min(hi, A_l)} <= s_j < W e^{min(x_0 - lo, B_l)};
  (c) the mean run with A_0 = hi, B_0 = x_0 - lo counts at least as many calls at every rung;
for [lo, hi] = [n_i (u - Lambda_1), n_i (2u - Lambda_1)].

Instances.  The law is that of a radial outer landscape, ln W = c_in - F(d), reference value psi_0 = F(d0).  The
places are NOT one number: seven patterns, among them two and three places correlated with the fibre average in
both directions, shells split between places, and for every atom the place (of a grid of 17 in [lo, hi]) that
maximises the atom's own contribution to the cost given the sample sizes of the run ("adversarial"; the joint
law of place and average that is worst for this design -- whether a Lipschitz psi realises it is another
matter, see `explicit` below).

Per instance: the sample size of every level against the product instance's; calls per rung against the bound;
the control with lo and hi exchanged (A_0 = lo, B_0 = x_0 - hi: must be violated); how much of the bound the worst
pattern attains.

`explicit`: an actual psi on Q_{n_o} x Q_{n_i}, psi(a, b) = F(|a|) + sigma(|a|) u |b| with a slope sigma that varies
with the outer shell, checked to be u-Lipschitz on every edge of the product cube; its fibre averages and places
are computed from psi (closed form checked against the sum over the fibre).

`corner`: designs with lo < b or x_0 - hi < b (outside "every design used"): what the statement and the
evaluator's pair mode do there.

usage: python3 -I -B r18_nonproduct.py <main|explicit|corner> [cases] [seed]
"""
import math
import random
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mpmath as mp                                                            # noqa: E402

import r18_mean as M                                                           # noqa: E402


def lam1(u):
    return math.log(2 / (1 + math.exp(-float(u))))


def x005_design(n, u, phi, lC_model="steps"):
    """The design of ENG-RES-0008 §1: b = 0.5, lambda = 0.2, eta = eta' = theta = 0.05, nu_1 = 2 e^u n_o/theta,
    delta = 0.05, ladder x_0 = 2 u n_i, then n_i eps* 0.85^i (i < 40) strictly between b and x_0, then b."""
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    b = Fr(1, 2)
    eps = math.log(math.cosh(float(u) / 2))
    xs = [2 * u * n_i] + [Fr(eps * 0.85 ** i * n_i) for i in range(40) if 0.5 < eps * 0.85 ** i * n_i < 2 * float(u) * n_i] + [b]
    lC = [None] + [2.0 + 3.0 * l for l in range(1, len(xs))]                  # a model of increasing inner costs (inputs)
    return M.Design(n, n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, max(1.0, 2 * math.exp(float(u)) * n_o / 0.05), b, 0.05, xs, lC=lC)


def random_design(rng):
    u = rng.choice([Fr(1, 2), Fr(1), Fr(2)])
    n = rng.choice([40, 60, 100, 150])
    n_o = rng.randint(max(2, n // 4), max(3, 3 * n // 4))
    n_i = n - n_o
    b = rng.choice([Fr(1, 4), Fr(1, 2), Fr(1)])
    lam = rng.choice([Fr(1, 5), Fr(1, 4), Fr(1, 2), Fr(1)])
    eta = rng.choice([Fr(1, 20), Fr(1, 4), Fr(1, 2)])
    theta = rng.choice([0.05, 0.1, 0.5, 2.0])
    x0 = 2 * u * n_i
    rates = sorted({Fr(rng.randint(1, 4000), 2000) * u for _ in range(rng.randint(1, 8))}, reverse=True)
    xs = [x0] + [r * n_i for r in rates if b < r * n_i < x0] + [b]
    lC = [None] + [2.0 + 3.0 * l for l in range(1, len(xs))]
    return M.Design(n, n_o, u, lam, eta, rng.choice([0.05, 0.5, 1.0]), theta, rng.choice([1.0, max(1.0, 2 * math.exp(float(u)) * n_o / theta)]),
                    b, 0.05, xs, lC=lC)


def draw_profile(rng, u, n_o):
    kind = rng.randint(0, 5)
    g = u / 16
    if kind == 0:
        steps = [rng.randint(-16, 16) for _ in range(n_o)]
    elif kind == 1:
        steps = [rng.randint(0, 16) for _ in range(n_o)]
    elif kind == 2:
        R = rng.randint(0, n_o)
        steps = [0 if d < R else 16 for d in range(n_o)]
    elif kind == 3:
        R = rng.randint(0, n_o)
        steps = [16 if d < R else 0 for d in range(n_o)]
    elif kind == 4:
        steps = [0] * n_o
    else:
        steps = [16] * n_o
    F = [Fr(0)]
    for s in steps:
        F.append(F[-1] + s * g)
    return F


def shift_of(D, t0, pos):
    return M.shift_c(D, *M.nested_positions(D, t0, pos))


def atom_cost(D, lnW, t0, pos, ms, ls0, jstop, rmax):
    """ln-free cost contribution of one unit of probability at (lnW, t0): sum_l C_l 2^{max m_j over the window of rung l-1}."""
    A, B = M.nested_positions(D, t0, pos)
    tot = mp.mpf(0)
    base = lnW - ls0
    for l in range(D.L):
        lo = max(M._ceil((base + D.b - A[l]) / D.lam), 0)
        hi = min(M._ceil((base + B[l]) / D.lam) - 1, jstop)
        if lo <= hi:
            tot += mp.e ** D.lC[l + 1] * (1 << rmax(lo, hi))
    return tot


def make_rmax(ms):
    table = [ms[:]]
    k = 1
    while (1 << k) <= len(ms):
        prev, half = table[-1], 1 << (k - 1)
        table.append([max(prev[i], prev[i + half]) for i in range(len(ms) - (1 << k) + 1)])
        k += 1

    def rmax(lo, hi):
        kk = (hi - lo + 1).bit_length() - 1
        return max(table[kk][lo], table[kk][hi - (1 << kk) + 1])
    return rmax


def patterns(rng, D, F, c_in, pos, lo, hi, Rprod):
    """name -> (atoms, den) with the law of the product instance and places that differ between fibres."""
    n_o = D.n_o
    binom = D.cube.binom
    lnW = [Fr(c_in) - F[d] for d in range(n_o + 1)]
    mid = (lo + hi) / 2
    # weighted median / terciles of ln W
    order = sorted(range(n_o + 1), key=lambda d: lnW[d])
    tot, acc, rank = 1 << n_o, 0, {}
    for d in order:
        rank[d] = Fr(2 * acc + binom[d], 2 * tot)                               # mid-rank of the shell in the law of W
        acc += binom[d]
    out = {}
    out["2 places: high W at hi, low W at lo"] = ([(lnW[d], binom[d], hi if rank[d] >= Fr(1, 2) else lo, pos) for d in range(n_o + 1)], tot)
    out["2 places: high W at lo, low W at hi"] = ([(lnW[d], binom[d], lo if rank[d] >= Fr(1, 2) else hi, pos) for d in range(n_o + 1)], tot)
    three = lambda r, a, b_, c: a if r < Fr(1, 3) else b_ if r < Fr(2, 3) else c   # noqa: E731
    out["3 places: lo / mid / hi by rising W"] = ([(lnW[d], binom[d], three(rank[d], lo, mid, hi), pos) for d in range(n_o + 1)], tot)
    out["3 places: hi / mid / lo by rising W"] = ([(lnW[d], binom[d], three(rank[d], hi, mid, lo), pos) for d in range(n_o + 1)], tot)
    at = []
    for d in range(n_o + 1):                                                     # every shell split 1 : 2 between lo and hi
        at.append((lnW[d], binom[d], lo, pos))
        at.append((lnW[d], 2 * binom[d], hi, pos))
    out["every shell split 1:2 between lo and hi"] = (at, 3 * tot)
    out["a random place per shell"] = ([(lnW[d], binom[d], lo + (hi - lo) * Fr(rng.randint(0, 64), 64), pos) for d in range(n_o + 1)], tot)
    # adversarial: for every atom the place of a grid that maximises its own cost, given the sample sizes of the run
    rmax = make_rmax(Rprod.ms)
    grid = [lo + (hi - lo) * Fr(i, 16) for i in range(17)]
    at = []
    for d in range(n_o + 1):
        best = max(grid, key=lambda t: atom_cost(D, lnW[d], t, pos, Rprod.ms, Rprod.ls0, Rprod.j_stop, rmax))
        at.append((lnW[d], binom[d], best, pos))
    out["adversarial: the dearest place for every atom"] = (at, tot)
    return out


def run_main(ncases, seed):
    rng = random.Random(seed)
    t_start = time.time()
    S = dict(instances=0, levels=0, sample_size_differs=0, rung_checks=0, above_bound=0, cost_above_bound=0, bound_below_product=0,
             swapped_checks=0, above_swapped=0, instances_above_swapped=0, skipped_not_in_range=0, designs=0, places_matter_beyond_rung1=0,
             bound_gt_cmax=0)
    worst = {}                    # pattern -> largest ln(cost_instance / cost_product)
    attain = {}                   # pattern -> largest fraction calls_instance/calls_bound over rungs where the bound exceeds the product
    gap_bound = 0.0
    done = 0
    while done < ncases:
        if done % 4 == 0:
            D = x005_design(rng.choice([60, 100, 150, 250]), rng.choice([Fr(1, 2), Fr(1), Fr(2)]), rng.choice([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85]))
        else:
            D = random_design(rng)
        u, n_i, n_o = D.u, D.n_i, D.n_o
        L1 = lam1(u)
        lo, hi = Fr(n_i * (float(u) - L1)), Fr(n_i * (2 * float(u) - L1))
        F = draw_profile(rng, u, n_o)
        d0 = rng.randint(0, n_o)
        psi0 = F[d0]
        c_in = Fr(rng.randint(math.ceil(-n_i * L1 * 64), math.floor(n_i * (float(u) - L1) * 64)), 64)
        for orc in ("bottom", "top"):
            pos = M.uniform_positions(D, orc)
            c_lo, c_hi = shift_of(D, lo, pos), shift_of(D, hi, pos)
            if c_lo != c_hi or any(shift_of(D, lo + (hi - lo) * Fr(i, 8), pos) != c_lo for i in range(1, 8)):
                S["skipped_not_in_range"] += 1                                    # the shift depends on the place: `corner` treats these
                continue
            atoms, den = M.radial_atoms(D, F, c_in, pos=pos)
            Rp = M.mean_run(D, atoms, den, psi0)
            if not Rp.status.startswith("closed"):
                continue
            Rb = M.mean_run(D, atoms, den, psi0, union=(lo, hi))
            Rs = M.mean_run(D, atoms, den, psi0, union=(hi, lo))                  # control: lo and hi exchanged
            assert Rb.ms == Rp.ms and Rs.ms == Rp.ms
            S["bound_below_product"] += any(Rb.calls_num[l] < Rp.calls_num[l] for l in range(1, D.L + 1))
            S["bound_gt_cmax"] += (Rb.lcost > D.lCmax)
            gap_bound = max(gap_bound, float(Rb.lcost - Rp.lcost))
            S["places_matter_beyond_rung1"] += any(Rb.calls_num[l] != Rp.calls_num[l] for l in range(2, D.L + 1))
            for name, (at, dn) in patterns(rng, D, F, c_in, pos, lo, hi, Rp).items():
                R = M.mean_run(D, at, dn, psi0)
                S["instances"] += 1
                S["levels"] += len(R.ms)
                S["sample_size_differs"] += (R.ms != Rp.ms or R.j_stop != Rp.j_stop)
                sw_bad = False
                for l in range(1, D.L + 1):
                    S["rung_checks"] += 1
                    # calls_l = K calls_num/den with different denominators: compare as fractions
                    if R.calls_num[l] * den > Rb.calls_num[l] * dn:
                        S["above_bound"] += 1
                    S["swapped_checks"] += 1
                    if R.calls_num[l] * den > Rs.calls_num[l] * dn:
                        S["above_swapped"] += 1
                        sw_bad = True
                    if Rb.calls_num[l] > Rp.calls_num[l] and Rb.calls_num[l] > 0:
                        fr = float(Fr(R.calls_num[l] * den, Rb.calls_num[l] * dn))
                        attain[name] = max(attain.get(name, 0.0), fr)
                S["instances_above_swapped"] += sw_bad
                S["cost_above_bound"] += (R.lcost > Rb.lcost + mp.mpf(10) ** (-30))
                worst[name] = max(worst.get(name, -1e9), float(R.lcost - Rp.lcost))
        done += 1
        S["designs"] += 1
        if done % 10 == 0:
            print(f"  {done} designs, {time.time() - t_start:.0f} s", flush=True)
    print(f"\nITEM 2 AT THE LEVEL OF MEAN RUNS: {S['designs']} designs x (profile, reference, offset) x 2 behaviours; "
          f"{S['skipped_not_in_range']} (design, behaviour) pairs left to `corner` because the shift depends on the place")
    print(f"  instances that are not products: {S['instances']}  ({S['levels']} levels)")
    print(f"  (a) sample size of some level differs from the product instance with the same law: {S['sample_size_differs']}   (must be 0)")
    print(f"  (c) calls of a rung above the bound (A0 = hi, B0 = x0 - lo): {S['above_bound']} of {S['rung_checks']} rung checks   (must be 0)")
    print(f"      cost above the bound's cost: {S['cost_above_bound']}   (must be 0);  bound below the product instance at some rung: {S['bound_below_product']}   (must be 0)")
    print(f"      bound above C_max: {S['bound_gt_cmax']} runs;  largest ln(bound cost / product cost): {gap_bound:.4f}")
    print(f"      (design, behaviour) pairs in which the union changes the calls of a rung beyond the first: {S['places_matter_beyond_rung1']}")
    print(f"  CONTROL lo and hi exchanged (A0 = lo, B0 = x0 - hi): calls above it in {S['above_swapped']} of {S['swapped_checks']} rung checks, "
          f"in {S['instances_above_swapped']} of {S['instances']} instances   (must be > 0)")
    print("  pattern: largest ln(cost / product cost);  largest share of the bound's calls attained at a rung where the bound exceeds the product")
    for name in worst:
        print(f"    {name:48s} {worst[name]:+.4f}   {attain.get(name, float('nan')):.6f}")
    ok = S["sample_size_differs"] == 0 and S["above_bound"] == 0 and S["cost_above_bound"] == 0 and S["bound_below_product"] == 0
    print(f"VERDICT: the bound {'HOLDS' if ok else 'FAILS'} on every instance; the control {'FAILED as it must' if S['above_swapped'] > 0 else 'did NOT fail'}")
    return t_start


def run_explicit():
    """An actual non-product psi and its mean run."""
    t_start = time.time()
    rows = []
    # fslope = 0: flat outer part, so ln W rises with the place (high W at hi);  fslope = 1: F(d) = u d on top of the
    # same fibres, so ln W FALLS while the place rises (high W at lo) -- both correlations by an actual psi
    for (u, n_o, n_i, direction, fslope) in ((Fr(1), 30, 6, +1, 0), (Fr(1), 30, 6, +1, 1), (Fr(2), 24, 4, +1, 0), (Fr(2), 24, 4, +1, 1),
                                             (Fr(1, 2), 40, 8, -1, 0), (Fr(1, 2), 40, 8, +1, 1)):
        uf = float(u)
        # slope sigma(d) of the fibre over the outer shell d: from +1 (cone up, place lo) to -1 (cone down, place hi), by steps of
        # at most 1/(2 n_i) per shell, with a flat outer part F = 0 ... then every edge of the product cube is checked
        step = Fr(1, 2 * n_i)
        sig = []
        s = Fr(direction)
        for d in range(n_o + 1):
            sig.append(s)
            if d >= (n_o - 4 * n_i) // 2 and abs(s - direction) < 2:
                s -= direction * step
        F = [fslope * u * d for d in range(n_o + 1)]
        psi = lambda d, e: float(F[d]) + float(sig[d]) * uf * e                  # noqa: E731
        # u-Lipschitz on every edge: an edge changes |a| or |b| by one
        worst_edge = 0.0
        for d in range(n_o + 1):
            for e in range(n_i + 1):
                if d < n_o:
                    worst_edge = max(worst_edge, abs(psi(d + 1, e) - psi(d, e)))
                if e < n_i:
                    worst_edge = max(worst_edge, abs(psi(d, e + 1) - psi(d, e)))
        assert worst_edge <= uf + 1e-12, worst_edge
        # fibre averages: closed form against the sum over the fibre
        lnW, t0s = [], []
        for d in range(n_o + 1):
            direct = mp.log(mp.fsum(math.comb(n_i, e) * mp.e ** (-mp.mpf(psi(d, e))) for e in range(n_i + 1)) / 2 ** n_i)
            closed = -mp.mpf(float(F[d])) + n_i * mp.log((1 + mp.e ** (-mp.mpf(float(sig[d])) * uf)) / 2)
            assert abs(direct - closed) < mp.mpf(10) ** (-11)      # psi is evaluated in floats: agreement to rounding
            lnW.append(Fr(float(direct)))
            t0s.append(Fr(psi(d, 0)) + u * n_i + Fr(float(direct)))             # t0 = psi(a, 0) + u n_i + ln W(a)
        L1 = lam1(u)
        lo, hi = Fr(n_i * (uf - L1)), Fr(n_i * (2 * uf - L1))
        assert all(lo - Fr(1, 10 ** 9) <= t <= hi + Fr(1, 10 ** 9) for t in t0s)
        n = n_o + n_i
        b = Fr(1, 2)
        xs = [2 * u * n_i] + [x for x in (Fr(3 * n_i, 8) * u, Fr(n_i, 8) * u) if b < x < 2 * u * n_i] + [b]
        D = M.Design(n, n_o, u, Fr(1, 5), Fr(1, 4), 0.1, 0.1, 1.0, b, 0.05, xs, lC=[None] + [2.0 + 3.0 * l for l in range(1, len(xs))])
        d0 = n_o // 2
        psi0 = Fr(psi(d0, 0))
        for orc in ("bottom", "top"):
            pos = M.uniform_positions(D, orc)
            cs = {shift_of(D, t, pos) for t in t0s}
            at = [(lnW[d], D.cube.binom[d], t0s[d], pos) for d in range(n_o + 1)]
            R = M.mean_run(D, at, 1 << n_o, psi0)
            Rb = M.mean_run(D, at, 1 << n_o, psi0, union=(lo, hi))
            Rs = M.mean_run(D, at, 1 << n_o, psi0, union=(hi, lo))
            # the product instance with the same law and the reference fibre's place
            atp = [(lnW[d], D.cube.binom[d], t0s[d0], pos) for d in range(n_o + 1)]
            Rp = M.mean_run(D, atp, 1 << n_o, psi0)
            corr = sum(D.cube.binom[d] * (float(lnW[d]) - float(lnW[d0])) * (float(t0s[d]) - float(t0s[d0])) for d in range(n_o + 1))
            rows.append((float(u), n_o, n_i, (direction, fslope, corr), orc, len(cs), float(min(t0s)), float(max(t0s)), float(lo), float(hi), R.status, R.j_stop,
                         R.ms == Rp.ms, [float(c) for c in R.calls[1:]], [float(c) for c in Rp.calls[1:]], [float(c) for c in Rb.calls[1:]],
                         [float(c) for c in Rs.calls[1:]], float(R.lcost), float(Rp.lcost), float(Rb.lcost)))
    print("\nAN ACTUAL psi THAT IS NOT A PRODUCT: psi(a, b) = sigma(|a|) u |b|, sigma from +1 to -1 (or back) across the outer shells; u-Lipschitz on every edge (checked)")
    for r in rows:
        (uf, n_o, n_i, direction, orc, ncs, tmin, tmax, lo, hi, status, jstop, same, calls, callsp, callsb, callss, lc, lcp, lcb) = r
        direction, fslope, corr = direction
        print(f"  u={uf:g} n_o={n_o} n_i={n_i} sigma {'+1 -> -1' if direction > 0 else '-1 -> +1'}, F = {fslope} u d ({'high W at hi' if corr > 0 else 'high W at lo'}) {orc:6s}: places in [{tmin:.3f}, {tmax:.3f}] of [{lo:.3f}, {hi:.3f}]; "
              f"distinct shifts {ncs}; {status} at level {jstop}; sample sizes equal to the product instance's: {same}")
        print(f"      calls per rung: this instance {['%.4g' % c for c in calls]}")
        print(f"                      product (reference fibre's place) {['%.4g' % c for c in callsp]}")
        print(f"                      bound A0=hi, B0=x0-lo {['%.4g' % c for c in callsb]}   holds: {all(a <= b_ * (1 + 1e-12) for a, b_ in zip(calls, callsb))}")
        print(f"                      CONTROL lo/hi exchanged {['%.4g' % c for c in callss]}   violated: {any(a > b_ * (1 + 1e-12) for a, b_ in zip(calls, callss))}")
        print(f"      ln cost: instance {lc:.4f}  product {lcp:.4f}  bound {lcb:.4f}")
    return t_start


def run_corner(ncases, seed):
    """Designs with lo < b or x_0 - hi < b.  (i) is the shift still the same for all places?  (ii) what does the pair
    mode of the evaluator compute (its c comes from A_0 = hi, B_0 = x_0 - lo), and is it an upper bound?"""
    rng = random.Random(seed)
    t_start = time.time()
    S = dict(cases=0, shift_depends_on_place=0, sample_sizes_depend_on_place=0, product_above_pairmode=0, max_excess=0.0, example=None,
             calls_above_pairmode=0, by_orc={"bottom": [0, 0, 0.0], "top": [0, 0, 0.0]})
    done = 0
    while done < ncases:
        u = rng.choice([Fr(1, 2), Fr(1), Fr(2)])
        n_i = rng.randint(2, 8)
        n_o = rng.randint(30, 90)
        n = n_o + n_i
        L1 = lam1(u)
        lo, hi = Fr(n_i * (float(u) - L1)), Fr(n_i * (2 * float(u) - L1))
        x0 = 2 * u * n_i
        b = Fr(rng.randint(2, 12), 4)
        if not (b < x0 and (lo < b or x0 - hi < b)):
            continue
        mids = sorted({b + (x0 - b) * Fr(rng.randint(1, 15), 16) for _ in range(rng.randint(0, 2))}, reverse=True)
        xs = [x0] + mids + [b]
        D = M.Design(n, n_o, u, rng.choice([Fr(1, 5), Fr(1, 2), Fr(1)]), Fr(1, 4), 0.1, rng.choice([0.05, 0.5, 2.0]), 1.0, b, 0.05, xs,
                     lC=[None] + [2.0 + 3.0 * l for l in range(1, len(xs))])
        F = draw_profile(rng, u, n_o)
        psi0 = F[rng.randint(0, n_o)]
        c_in = Fr(rng.randint(math.ceil(-n_i * L1 * 64), math.floor(n_i * (float(u) - L1) * 64)), 64)
        for orc in ("bottom", "top"):
            pos = M.uniform_positions(D, orc)
            # the shift the pair mode uses: max_l min(b - A_l, B_l) with A_0 = hi, B_0 = x_0 - lo
            A, B = [hi], [x0 - lo]
            for (a, be) in pos:
                A.append(min(A[-1], a)); B.append(min(B[-1], be))
            c_pair = M.shift_c(D, A, B)
            places = [lo + (hi - lo) * Fr(i, 8) for i in range(9)]
            shifts = [shift_of(D, t, pos) for t in places]
            S["cases"] += 1
            S["by_orc"][orc][0] += 1
            S["shift_depends_on_place"] += (len(set(shifts)) > 1)
            ms_set = set()
            for t in places:                                         # PRODUCT instances: every fibre at the place t, c_in = t - u n_i
                ci = t - u * n_i
                at, dn = M.radial_atoms(D, F, ci, t0=t, pos=pos)
                R = M.mean_run(D, at, dn, psi0)
                Rpair = M.mean_run(D, at, dn, psi0, union=(lo, hi), c_force=c_pair)        # what `t0_range` evaluates for this law
                if not (R.status.startswith("closed") and Rpair.status.startswith("closed")):
                    continue
                # the same law with the fibres at the two ends of the range: do the sample sizes depend on the place?
                for t2 in (lo, hi):
                    at2 = [(a[0], a[1], t2, pos) for a in at]
                    ms_set.add((t, tuple(M.mean_run(D, at2, dn, psi0).ms)))
                ex = float(R.lcost - Rpair.lcost)
                if any(R.calls_num[l] > Rpair.calls_num[l] for l in range(1, D.L + 1)) or R.m_top > Rpair.m_top:
                    S["calls_above_pairmode"] += 1
                if ex > 1e-12:
                    S["product_above_pairmode"] += 1
                    S["by_orc"][orc][1] += 1
                    S["by_orc"][orc][2] = max(S["by_orc"][orc][2], ex)
                    if ex > S["max_excess"]:
                        S["max_excess"] = ex
                        S["example"] = dict(u=str(u), n=n, n_o=n_o, n_i=n_i, lam=str(D.lam), eta=str(D.eta), etap=float(D.etap), theta=float(D.theta),
                                            nu1=float(D.nu1), b=str(b), xs=[str(x) for x in xs], F=[str(x) for x in F], psi0=str(psi0), c_in=str(ci),
                                            oracle=orc, place=str(t), place_float=float(t), lo=float(lo), hi=float(hi), c_place=str(shift_of(D, t, pos)),
                                            c_pair=str(c_pair), lcost_instance=float(R.lcost), lcost_pairmode=float(Rpair.lcost),
                                            m_top_instance=R.m_top, m_top_pairmode=Rpair.m_top)
            by_law = {}
            for (t, ms) in ms_set:
                by_law.setdefault(t, set()).add(ms)
            S["sample_sizes_depend_on_place"] += any(len(v) > 1 for v in by_law.values())
        done += 1
    print(f"\nOUTSIDE THE RANGE (lo < b or x0 - hi < b): {S['cases']} (design, law, behaviour) cases, each with product instances at 9 feasible places")
    print(f"  the shift c depends on the place in {S['shift_depends_on_place']} cases; for one and the same law the sample sizes differ between fibres-at-lo and fibres-at-hi in {S['sample_sizes_depend_on_place']} cases")
    print(f"  product instances (every fibre at one feasible place, c_in = t0 - u n_i) whose cost EXCEEDS what the pair mode returns for their law: {S['product_above_pairmode']} "
          f"(bottom {S['by_orc']['bottom'][1]}, largest ln excess {S['by_orc']['bottom'][2]:.3f}; top {S['by_orc']['top'][1]}, largest {S['by_orc']['top'][2]:.3f}); "
          f"with a rung's calls or the sample above it: {S['calls_above_pairmode']}")
    print(f"  largest excess of ln cost: {S['max_excess']:.4f}")
    if S["example"]:
        import json
        ex = dict(S["example"])
        Fs = ex.pop("F")
        print("  example:", json.dumps(ex))
        out = Path(__file__).resolve().parent / "data_corner_example.json"
        if not out.exists():
            ex["F"] = Fs
            out.write_text(json.dumps(ex, indent=1) + "\n")
            print("  example written to", out.name)
    return t_start


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    ncases = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    print(f"r18_nonproduct.py {mode} cases={ncases} seed={seed} start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    if mode == "main":
        t0_ = run_main(ncases, seed)
    elif mode == "explicit":
        t0_ = run_explicit()
    else:
        t0_ = run_corner(ncases, seed)
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t0_:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
