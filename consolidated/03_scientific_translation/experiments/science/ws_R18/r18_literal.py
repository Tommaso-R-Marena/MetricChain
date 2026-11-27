#!/usr/bin/env python3
"""R18, item 2 -- LITERAL runs (random outer sample, the loop as written) on instances that are not products,
against the windows of ENG-RES-0014 §4 and against the mean run.

Literal engine: our division's `experiments/science/ws_R6/r6lib.py` (written from the specification by workstream
R6; exact constants, exact sampling of the outer sample, the loop of K_REPORT §2.2 as written).  It is not the
engineering division's code.  Mean runs: `r18_mean.py` (mine).

Instances (per outer shell d: fibre average W(d), probability C(n_o, d)/2^{n_o}, place t0(d)):
  psi+   an actual psi(a, b) = sigma(|a|) u |b|, sigma from +1 to -1 across the shells (places from lo to hi, high W
         at hi), u-Lipschitz on every edge -- the first family of `r18_nonproduct.py explicit`;
  psi-   the same fibres on top of F(d) = u d (high W at lo);
  two    a radial law with two places, hi for the upper half of the law of W and lo for the lower half ("simulated":
         given by its classes; no psi is exhibited for it);
  prod   the product instance with the same law as psi+/psi-/two (one place: that of the reference fibre).

Per literal run, with the REALISED sample sizes (t_j = number of doublings at level j):
  identity   calls of rung l+1  ==  #{points i : some level j <= j_stop with i <= M_j lies in the point's own window}
  union      calls of rung l+1  <=  the same count with the union window  [b - min(hi, A_l), min(x0 - lo, B_l))
  control    the same count with lo and hi exchanged -- must be exceeded
  (a)        with the same seed the product instance draws the same outer sample: its sample sizes must be the same
             at every level
and against the mean run: the mean over runs of the literal calls, and how often a single literal run exceeds the
MEAN-RUN bound (which is a statement about means, not about samples).

usage: python3 -I -B r18_literal.py [runs_per_case] [seed]
"""
import math
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ws_R6"))
sys.path.insert(0, str(HERE))
import numpy as np                                                              # noqa: E402
import mpmath as mp                                                             # noqa: E402

import r6lib                                                                    # noqa: E402  (ours, read-only)
import r18_mean as M                                                            # noqa: E402


def lam1(u):
    return math.log(2 / (1 + math.exp(-u)))


def explicit_psi(u, n_o, n_i, fslope):
    """ln W(d) and place t0(d) of psi(a, b) = fslope u |a| + sigma(|a|) u |b|; sigma: +1 -> -1 by 1/(2 n_i) per shell."""
    step, s, sig = 1.0 / (2 * n_i), 1.0, []
    for d in range(n_o + 1):
        sig.append(s)
        if d >= (n_o - 4 * n_i) // 2 and s > -1.0 + 1e-12:
            s -= step
    psi = lambda d, e: fslope * u * d + sig[d] * u * e                          # noqa: E731
    worst = 0.0
    for d in range(n_o + 1):
        for e in range(n_i + 1):
            if d < n_o:
                worst = max(worst, abs(psi(d + 1, e) - psi(d, e)))
            if e < n_i:
                worst = max(worst, abs(psi(d, e + 1) - psi(d, e)))
    assert worst <= u + 1e-12
    lnW = [float(mp.log(mp.fsum(math.comb(n_i, e) * mp.e ** (-mp.mpf(psi(d, e))) for e in range(n_i + 1)) / 2 ** n_i)) for d in range(n_o + 1)]
    t0 = [psi(d, 0) + u * n_i + lnW[d] for d in range(n_o + 1)]
    return lnW, t0


def two_places(u, n_o, n_i, lo, hi):
    """A cone-then-flat radial law with a generic offset; place hi for the upper half of the law of W, lo for the lower."""
    R = int(0.42 * n_o)
    F = [u * min(d, R) for d in range(n_o + 1)]
    lnW = [0.137 - f for f in F]
    binom = [math.comb(n_o, d) for d in range(n_o + 1)]
    order = sorted(range(n_o + 1), key=lambda d: lnW[d])
    acc, t0 = 0, [None] * (n_o + 1)
    for d in order:
        t0[d] = hi if (2 * acc + binom[d]) >= 2 ** n_o else lo
        acc += binom[d]
    return lnW, t0


def run_case(name, u, n_o, n_i, lnW, t0, d0, orc, lamq, runs, seed, out):
    n = n_o + n_i
    b = Fr(1, 2)
    uq = Fr(u).limit_denominator(64)
    xs = [2 * uq * n_i] + [x for x in (Fr(3 * n_i, 8) * uq, Fr(n_i, 8) * uq) if b < x < 2 * uq * n_i] + [b]
    L = len(xs) - 1
    eta, etap, theta, nu1, delta = Fr(1, 4), 0.1, 0.1, 1.0, 0.05
    P = r6lib.Params2LP(n, n_o, float(uq), float(lamq), eta, etap, theta, nu1, float(b), delta, [float(x) for x in xs], [1.0] * L)
    D = M.Design(n, n_o, uq, lamq, eta, etap, theta, nu1, b, delta, xs, lC=[None] + [0.0] * L)
    assert (P.J, P.K, P.rdag, P.m_max) == (D.J, D.K, D.r_dag, D.m_max), "constants: r6lib and r18_mean differ"
    L1 = lam1(u)
    lo, hi = n_i * (u - L1), n_i * (2 * u - L1)
    x0 = float(xs[0])
    bf = float(b)
    prob = [mp.mpf(math.comb(n_o, d)) / 2 ** n_o for d in range(n_o + 1)]
    strat = r6lib.S_BOTTOM if orc == "bottom" else r6lib.S_TOP
    kap = [u * n_i - t for t in t0]
    inst = r6lib.ClassInstance(n, n_o, u, lnW, prob, kap, strat, d0, name)
    # the product instance with the same law and the same reference value: every fibre at the reference fibre's place
    inst_p = r6lib.ClassInstance(n, n_o, u, lnW, prob, [kap[d0]] * (n_o + 1), strat, d0, name + " (product)")
    assert inst.psi0 == inst_p.psi0
    al = [0.0 if orc == "bottom" else float(x) for x in xs[1:]]                  # alpha_l, l = 1..L
    be = [float(x) if orc == "bottom" else 0.0 for x in xs[1:]]
    # ---- mean runs (exact): the instance, the product instance, the bound, the control
    pos = M.uniform_positions(D, orc)
    lnWq = [Fr(w) for w in lnW]
    atoms = [(lnWq[d], D.cube.binom[d], uq * n_i - Fr(kap[d]), pos) for d in range(n_o + 1)]
    atoms_p = [(lnWq[d], D.cube.binom[d], uq * n_i - Fr(kap[d0]), pos) for d in range(n_o + 1)]
    psi0q = Fr(inst.psi0)
    Rm = M.mean_run(D, atoms, 1 << n_o, psi0q)
    Rmp = M.mean_run(D, atoms_p, 1 << n_o, psi0q)
    Rmb = M.mean_run(D, atoms, 1 << n_o, psi0q, union=(Fr(lo), Fr(hi)))
    shifts = {M.shift_c(D, *M.nested_positions(D, a[2], pos)) for a in atoms}
    assert len(shifts) == 1 and Rm.ms == Rmp.ms
    rng_seed = np.random.SeedSequence([seed, abs(hash(name)) % 10 ** 6, 0 if orc == "bottom" else 1])
    st = dict(runs=0, closed=0, identity_bad=0, union_bad=0, control_bad_runs=0, same_sizes_as_product=0, same_level_as_mean=0,
              above_mean_bound_runs=0, max_ratio_to_mean_bound=0.0, sum_calls=np.zeros(L + 1), sum_calls_p=np.zeros(L + 1),
              sum_union=np.zeros(L + 1), calls_gt_product_runs=0)
    for k in range(runs):
        ss = rng_seed.spawn(1)[0]
        rng = np.random.default_rng(ss)
        rng_p = np.random.default_rng(ss)                                        # the same stream: the same outer sample
        oracle = r6lib.SimOracle(P.xs, rng)
        run = r6lib.Run(P, inst, oracle, rng, variant="2L+", abort_on_cost=False).run()
        runp = r6lib.Run(P, inst_p, r6lib.SimOracle(P.xs, rng_p), rng_p, variant="2L+", abort_on_cost=False).run()
        st["runs"] += 1
        if run.status != "closed":
            continue
        st["closed"] += 1
        tj = np.array([rec["passes"][-1]["t"] for rec in run.levels])
        tjp = np.array([rec["passes"][-1]["t"] for rec in runp.levels])
        Nj = [rec["passes"][-1]["N"] for rec in run.levels]
        Njp = [rec["passes"][-1]["N"] for rec in runp.levels]
        st["same_sizes_as_product"] += (len(tj) == len(tjp) and np.array_equal(tj, tjp) and Nj == Njp)
        st["same_level_as_mean"] += (len(tj) - 1 == Rm.j_stop and int(tj.max()) == Rm.m_top)
        ls = np.array([run.ln_s(j) for j in range(len(tj))])
        w = run.lnW
        place = u * n_i - ((run.lnL0 + run.lnU0) / 2 - w)                        # t0 of every unit, from its trivial bracket
        cnt = np.array([int(c) for c in run.cnt], dtype=object)
        blk = run.blk
        calls_own = [0] * (L + 1)
        calls_uni = [0] * (L + 1)
        calls_swp = [0] * (L + 1)
        A_own, B_own = place.copy(), x0 - place
        A_uni, B_uni = np.full(len(w), hi), np.full(len(w), x0 - lo)
        A_swp, B_swp = np.full(len(w), lo), np.full(len(w), x0 - hi)
        for l in range(L):
            if l >= 1:
                A_own, B_own = np.minimum(A_own, al[l - 1]), np.minimum(B_own, be[l - 1])
                A_uni, B_uni = np.minimum(A_uni, al[l - 1]), np.minimum(B_uni, be[l - 1])
                A_swp, B_swp = np.minimum(A_swp, al[l - 1]), np.minimum(B_swp, be[l - 1])
            for (A, B, acc) in ((A_own, B_own, calls_own), (A_uni, B_uni, calls_uni), (A_swp, B_swp, calls_swp)):
                j_lo = np.searchsorted(ls, w + bf - A, side="left")              # first level with ln s_j >= ln W + b - A_l
                j_hi = np.searchsorted(ls, w + B, side="left") - 1               # last level with ln s_j < ln W + B_l
                tot = 0
                for i in range(len(w)):
                    if j_lo[i] <= j_hi[i] and tj[j_lo[i]:j_hi[i] + 1].max() >= blk[i]:
                        tot += cnt[i]
                acc[l + 1] = tot
        lit = run.calls
        st["identity_bad"] += any(lit[l] != calls_own[l] for l in range(1, L + 1))
        st["union_bad"] += any(lit[l] > calls_uni[l] for l in range(1, L + 1))
        st["control_bad_runs"] += any(lit[l] > calls_swp[l] for l in range(1, L + 1))
        st["calls_gt_product_runs"] += any(lit[l] > runp.calls[l] for l in range(1, L + 1))
        ratio = max((float(lit[l]) / float(Rmb.calls[l])) for l in range(1, L + 1) if Rmb.calls[l] > 0)
        st["above_mean_bound_runs"] += (ratio > 1.0)
        st["max_ratio_to_mean_bound"] = max(st["max_ratio_to_mean_bound"], ratio)
        for l in range(1, L + 1):
            st["sum_calls"][l] += float(lit[l])
            st["sum_calls_p"][l] += float(runp.calls[l])
            st["sum_union"][l] += float(calls_uni[l])
    c = max(st["closed"], 1)
    print(f"\n{name}  u={u:g} n_o={n_o} n_i={n_i} lambda={lamq} {orc}:  K={P.K}  L={L}  places in [{min(t0):.3f}, {max(t0):.3f}] of [{lo:.3f}, {hi:.3f}]", file=out)
    print(f"  literal runs {st['runs']}, closed {st['closed']}; stopping level and largest sample equal to the mean run's in {st['same_level_as_mean']}", file=out)
    print(f"  (a) sample sizes and counts of every level identical to the product instance on the same outer sample: {st['same_sizes_as_product']} of {st['closed']}", file=out)
    print(f"  identity (own windows, realised sizes) violated in {st['identity_bad']} runs;  union window violated in {st['union_bad']} runs   (both must be 0)", file=out)
    print(f"  CONTROL lo/hi exchanged: exceeded in {st['control_bad_runs']} of {st['closed']} runs   (must be > 0)", file=out)
    print(f"  runs with more calls at some rung than the product instance on the same sample: {st['calls_gt_product_runs']}", file=out)
    print(f"  calls per rung:   literal mean {['%.5g' % (x / c) for x in st['sum_calls'][1:]]}", file=out)
    print(f"                    mean run     {['%.5g' % float(x) for x in Rm.calls[1:]]}", file=out)
    print(f"      product:      literal mean {['%.5g' % (x / c) for x in st['sum_calls_p'][1:]]}", file=out)
    print(f"                    mean run     {['%.5g' % float(x) for x in Rmp.calls[1:]]}", file=out)
    print(f"      union bound:  literal mean (realised sizes) {['%.5g' % (x / c) for x in st['sum_union'][1:]]}", file=out)
    print(f"                    mean run     {['%.5g' % float(x) for x in Rmb.calls[1:]]}", file=out)
    print(f"  single literal runs above the MEAN-RUN bound at some rung: {st['above_mean_bound_runs']} of {st['closed']}; largest ratio {st['max_ratio_to_mean_bound']:.4f}", file=out)
    out.flush()
    return st


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    t = time.time()
    out = sys.stdout
    print(f"r18_literal.py runs per case = {runs} seed = {seed} start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    tot = dict(runs=0, closed=0, identity_bad=0, union_bad=0, control_bad_runs=0, same=0, above=0)
    cases = []
    for (u, n_o, n_i) in ((1.0, 30, 6), (2.0, 24, 4), (0.5, 40, 8)):
        L1 = lam1(u)
        lo, hi = n_i * (u - L1), n_i * (2 * u - L1)
        for fs, tag in ((0, "psi+ (actual psi, high W at hi)"), (1, "psi- (actual psi, high W at lo)")):
            lnW, t0 = explicit_psi(u, n_o, n_i, fs)
            cases.append((tag, u, n_o, n_i, lnW, t0, n_o // 2))
        lnW, t0 = two_places(u, n_o, n_i, lo, hi)
        cases.append(("two (simulated: hi for the upper half of W, lo for the lower)", u, n_o, n_i, lnW, t0, n_o // 2))
    for (tag, u, n_o, n_i, lnW, t0, d0) in cases:
        for orc in ("bottom", "top"):
            st = run_case(tag, u, n_o, n_i, lnW, t0, d0, orc, Fr(1, 5), runs, seed, out)
            tot["runs"] += st["runs"]; tot["closed"] += st["closed"]; tot["identity_bad"] += st["identity_bad"]; tot["union_bad"] += st["union_bad"]
            tot["control_bad_runs"] += st["control_bad_runs"]; tot["same"] += st["same_sizes_as_product"]; tot["above"] += st["above_mean_bound_runs"]
    print(f"\nTOTAL literal runs {tot['runs']} (closed {tot['closed']}): identity violated {tot['identity_bad']}, union window violated {tot['union_bad']} (must be 0); "
          f"control exceeded in {tot['control_bad_runs']} runs (must be > 0); sample sizes identical to the product instance in {tot['same']}; "
          f"single runs above the mean-run bound: {tot['above']}")
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")


if __name__ == "__main__":
    main()
