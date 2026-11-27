#!/usr/bin/env python3
"""r26_influence.py -- workstream R26, Item 1 (ii): the influence of a band model across a cut, as a function of
the coupling scale J, of a clash energy C, of the inner block length k and of the bandwidth r.

Usage:  python3 -B r26_influence.py <block>      block in {T1q3, T1q4, T1q6, T2, T3, T3b, T4, T4b, T5}

Every table prints, over an ensemble of random models (seeds listed) and over ordered pairs of boundary states of
the outer block, the largest and the median value of
    osc    = max Delta - min Delta      (the bound that uses the cross-cut interaction only),
    pt     = pointwise influence        max_b ln[mu(b|a)/mu(b|a')],
    box D  = influence relative to the box class 1 <= w <= e^D,
    Lip u  = influence relative to the class of fibre weights that are log-u-Lipschitz for the Hamming distance
             (exact, LP on the whole inner block).
Controls (each can fail; the number of violations is printed with every table):
    C1  0 <= pt <= osc;   C2  box D <= min(D, pt);   C3  Lip u <= min(pt, u*k);   C4  Lip u, box D >= 0;
    C5  box D nondecreasing in D, Lip u nondecreasing in u;   C6  pt = 0 and all influences 0 when a = a'
        (by construction) and -- for r >= 1 -- the conditional law depends on the last r outer sites only
        (checked in T4 by enumerating a longer outer boundary).
"""
import resource
import sys
import time

import numpy as np

import r26_band as B

TOL = 1e-7


def stats(x):
    x = np.asarray(x, dtype=float)
    return f"{x.max():7.3f} {np.median(x):7.3f}"


def analyse(model, c, us, Ds, Acache, pairs_sel=None):
    """All influences across the cut c of one model.  Returns dict of matrices [alpha, alpha'] and violations."""
    q, n = model["q"], model["n"]
    k = n - c
    alphas, bconf, logmu = B.brute_conditionals(model, c)
    _, betas, Ex, logR, logpi = B.boundary_layer(model, c)
    pt_f, osc = B.iota_pointwise_formula(Ex, logpi)
    pt_b = B.iota_pointwise_brute(logmu)
    viol = 0
    if np.abs(pt_f - pt_b).max() > 1e-8:
        viol += 1
    out = dict(alphas=alphas, osc=osc, pt=pt_b)
    nA = len(alphas)
    off = ~np.eye(nA, dtype=bool)
    if ((pt_b < -1e-9) | (pt_b > osc + 1e-9))[off].any():
        viol += 1                                                    # C1
    prev = None
    for D in Ds:
        bx = B.iota_box_levelset(logpi, D)
        out[("box", D)] = bx
        if (bx[off] > np.minimum(D, pt_b[off]) + TOL).any() or (bx[off] < -TOL).any():
            viol += 1                                                # C2, C4
        if prev is not None and (bx[off] < prev[off] - TOL).any():
            viol += 1                                                # C5
        prev = bx
    prev = None
    for u in us:
        key = (q, k, u)
        if key not in Acache:
            Acache[key] = B.lipschitz_constraints(q, k, u)
        lp = B.iota_lipschitz_lp(logmu, Acache[key], pairs=pairs_sel)
        out[("lip", u)] = lp
        m = off & np.isfinite(lp)
        if (lp[m] > np.minimum(pt_b[m], u * k) + 1e-5).any() or (lp[m] < -1e-6).any():
            viol += 1                                                # C3, C4
        if prev is not None and (lp[m] < prev[m] - 1e-5).any():
            viol += 1                                                # C5
        prev = lp
    out["viol"] = viol
    return out


def collect(results, key, mask_fn=None):
    vals = []
    for res in results:
        M = res[key]
        nA = M.shape[0]
        off = ~np.eye(nA, dtype=bool)
        m = off & np.isfinite(M)
        if mask_fn is not None:
            m = m & mask_fn(res)
        vals.append(M[m])
    return np.concatenate(vals) if vals else np.array([np.nan])


def header(us, Ds):
    cols = ["osc", "pt"] + [f"box D={D:g}" for D in Ds] + [f"Lip u={u:g}" for u in us]
    return "".join(f"{c:>16s}" for c in cols) + "\n" + "".join(f"{'max  median':>16s}" for _ in cols)


def row(results, us, Ds, mask_fn=None):
    keys = ["osc", "pt"] + [("box", D) for D in Ds] + [("lip", u) for u in us]
    return "".join(f"{stats(collect(results, key, mask_fn)):>16s}" for key in keys)


def T1(qs=(3, 4), n=10, c=5, seeds=range(10), Js=(0.25, 0.5, 1.0, 2.0, 4.0, 8.0), us=(0.5, 1.0, 2.0),
       Ds=(1.0, 5.0, 20.0)):
    print("T1: nearest-neighbour chain (r = 1), no clash; influence of the last outer site on the inner block, "
          "against the coupling scale J")
    print(f"    n = {n} sites, cut after site {c} (inner length k = {n - c}); seeds {list(seeds)}; "
          f"all ordered pairs of boundary states")
    Acache, vtot = {}, 0
    for q in qs:
        print(f"  q = {q} states per site")
        print("     J " + header(us, Ds))
        for J in Js:
            results = []
            for seed in seeds:
                base = B.make_base(n, q, 1, np.random.default_rng(1000 + seed))
                res = analyse(B.energies(base, J), c, us, Ds, Acache)
                vtot += res["viol"]
                results.append(res)
            print(f"  {J:5.2f}" + row(results, us, Ds))
    print(f"T1 control violations: {vtot}")
    return vtot


def T2(q=3, n=10, c=5, seeds=range(10), Js=(1.0, 2.0), Cs=(None, 10.0, 20.0, 30.0), frac=0.15, us=(0.5, 1.0, 2.0),
       Ds=(1.0, 5.0, 20.0)):
    print("T2: nearest-neighbour chain with clashes: each pair-state entry is a clash with probability "
          f"{frac} (same positions for every clash energy C); other entries J*N(0,1)")
    print(f"    q = {q}, n = {n}, cut after site {c}; seeds {list(seeds)}; all ordered pairs of boundary states")
    Acache, vtot = {}, 0
    print("     J     C " + header(us, Ds))
    for J in Js:
        for C in Cs:
            results = []
            ncross = 0
            for seed in seeds:
                base = B.make_base(n, q, 1, np.random.default_rng(2000 + seed), clash_frac=frac)
                ncross += int(base["mask"][(c - 1, c)].sum())
                res = analyse(B.energies(base, J, C), c, us, Ds, Acache)
                vtot += res["viol"]
                results.append(res)
            cs = "none" if C is None else f"{C:4.0f}"
            print(f"  {J:5.2f} {cs:>5s} " + row(results, us, Ds))
        print(f"    (clash entries on the cross-cut pair, summed over the {len(list(seeds))} models: {ncross} of "
              f"{len(list(seeds)) * q * q})")
    print(f"T2 control violations: {vtot}")
    return vtot


def T3(q=3, c=4, seeds=range(6), ks_lp=(1, 2, 3, 4, 5, 6, 7), ks_tm=(1, 2, 3, 4, 5, 6, 7, 8, 12, 20, 40),
       cases=((1.0, None), (4.0, None), (1.0, 20.0)), us=(1.0,), Ds=(5.0,), frac=0.15):
    print("T3: nearest-neighbour chain, influence against the inner block length k (outer block fixed, c = 4)")
    print(f"    q = {q}; seeds {list(seeds)}; the models for different k are prefixes of one model of 44 sites")
    Acache, vtot = {}, 0
    nmax = c + max(max(ks_lp), max(ks_tm))
    for (J, C) in cases:
        print(f"  J = {J}, clash {'none' if C is None else C}:   (largest over pairs and seeds; "
              f"'rec' = pairwise recursion bound, polynomial time)")
        print("      k      pt   box D=5   Lip u=1 (LP)   Lip u=1 (rec)   u*k")
        bases = [B.make_base(nmax, q, 1, np.random.default_rng(3000 + seed), clash_frac=frac) for seed in seeds]
        for k in sorted(set(ks_lp) | set(ks_tm)):
            n = c + k
            pt_all, bx_all, lp_all, rec_all = [], [], [], []
            for base in bases:
                full = B.energies(base, J, C)
                model = dict(n=n, q=q, r=1, pair={kk: v for kk, v in full["pair"].items() if kk[1] < n},
                             h=full["h"][:n])
                _, betas, Ex, logR, logpi = B.boundary_layer(model, c)
                pt, osc = B.iota_pointwise_formula(Ex, logpi)
                off = ~np.eye(pt.shape[0], dtype=bool)
                pt_all.append(pt[off])
                bx_all.append(B.iota_box_levelset(logpi, Ds[0])[off])
                rec, _ = B.recursion_bound_nn(model, c, us[0])
                rec_all.append(rec[off])
                if k in ks_lp:
                    res = analyse(model, c, us, Ds, Acache)
                    vtot += res["viol"]
                    lp = res[("lip", us[0])]
                    lp_all.append(lp[off])
                    if (lp[off] > rec[off] + 1e-5).any():
                        vtot += 1                      # the recursion must be an upper bound of the LP value
            lp_s = f"{np.concatenate(lp_all).max():10.4f}" if lp_all else "         -"
            gap = ""
            if lp_all:
                gap = f"   (rec - LP: max {np.max(np.concatenate(rec_all) - np.concatenate(lp_all)):.2e})"
            print(f"  {k:5d} {np.concatenate(pt_all).max():7.3f} {np.concatenate(bx_all).max():9.4f}   {lp_s}"
                  f"      {np.concatenate(rec_all).max():10.4f}   {us[0] * k:5.1f}{gap}")
    print(f"T3 control violations: {vtot}")
    return vtot


def T3b(qs=(3, 4, 6), c=4, seeds=range(6), ks=(1, 2, 3, 4, 5, 6, 8, 12, 20, 40), Js=(1.0, 4.0, 8.0), u=1.0,
        Cs=(None, 20.0), frac=0.15):
    print("T3b: nearest-neighbour chain, the polynomial upper bound of the Lipschitz influence (pairwise recursion; "
          "exact for q = 2, an upper bound otherwise) against the inner block length k, for larger alphabets")
    print(f"    outer block of {c} sites; u = {u}; seeds {list(seeds)}; largest value over pairs and seeds; "
          "the chains for different k are prefixes of one chain")
    vtot = 0
    nmax = c + max(ks)
    for q in qs:
        for C in Cs:
            for J in Js:
                bases = [B.make_base(nmax, q, 1, np.random.default_rng(3500 + seed), clash_frac=frac)
                         for seed in seeds]
                vals, pts = [], []
                for k in ks:
                    n = c + k
                    best, bestpt = 0.0, 0.0
                    for base in bases:
                        full = B.energies(base, J, C)
                        model = dict(n=n, q=q, r=1, pair={kk: v for kk, v in full["pair"].items() if kk[1] < n},
                                     h=full["h"][:n])
                        rec, _ = B.recursion_bound_nn(model, c, u)
                        _, betas, Ex, logR, logpi = B.boundary_layer(model, c)
                        pt, osc = B.iota_pointwise_formula(Ex, logpi)
                        off = ~np.eye(q, dtype=bool)
                        if (rec[off] > np.minimum(pt[off], u * k) + 1e-6).any() or (rec[off] < -1e-9).any():
                            vtot += 1                      # the bound must respect min(pt, u k)
                        best = max(best, rec[off].max())
                        bestpt = max(bestpt, pt[off].max())
                    vals.append(best)
                    pts.append(bestpt)
                print(f"  q = {q}, J = {J:g}, clash {'none' if C is None else C:>4}: bound for k = {list(ks)}: "
                      + " ".join(f"{v:.2f}" for v in vals) + f"   (pointwise at k = {ks[-1]}: {pts[-1]:.1f})")
    print(f"T3b control violations: {vtot}")
    return vtot


def T4(q=3, n=10, c=5, seeds=range(4), rs=(1, 2, 3), cases=((1.0, None), (1.0, 20.0), (3.0, None)), us=(1.0,),
       Ds=(1.0, 5.0, 20.0), frac=0.15):
    print("T4: bandwidth r (pair interactions up to sequence separation r, each J*N(0,1)); "
          f"q = {q}, n = {n}, cut after site {c}; seeds {list(seeds)}")
    print("    rows: single-site changes at distance s from the cut (s = 0: the last outer site), and arbitrary "
          "pairs of boundary states")
    Acache, vtot = {}, 0
    for (J, C) in cases:
        print(f"  J = {J}, clash {'none' if C is None else C}")
        print("     r  pairs       " + header(us, Ds))
        for r in rs:
            results = []
            for seed in seeds:
                base = B.make_base(n, q, r, np.random.default_rng(4000 + seed), clash_frac=frac)
                model = B.energies(base, J, C)
                res = analyse(model, c, us, Ds, Acache)
                vtot += res["viol"]
                # C6: the conditional law of the inner block depends on the last r outer sites only: enumerate the
                # last min(r+1, c) outer sites instead (a model with bandwidth r+1 whose extra pairs are zero)
                if r < 3:
                    m2 = dict(n=n, q=q, r=r + 1, pair=dict(model["pair"]), h=model["h"])
                    for i in range(n):
                        j = i + r + 1
                        if j < n:
                            m2["pair"][(i, j)] = np.zeros((q, q))
                    al2, _, logmu2 = B.brute_conditionals(m2, c)
                    al1, _, logmu1 = B.brute_conditionals(model, c)
                    key = (al2[:, 1:] * (q ** np.arange(r - 1, -1, -1))[None, :]).sum(axis=1)
                    if np.abs(logmu2 - logmu1[key]).max() > 1e-9:
                        vtot += 1
                results.append(res)
            rb = min(r, c)

            def ham_mask(res, s=None):
                al = res["alphas"]
                diff = (al[:, None, :] != al[None, :, :])
                hd = diff.sum(axis=2)
                if s is None:
                    return hd >= 1
                t = rb - 1 - s
                return (hd == 1) & diff[:, :, t]
            for s in range(rb):
                print(f"  {r:4d}  s = {s}      " + row(results, us, Ds, lambda res, s=s: ham_mask(res, s)))
            print(f"  {r:4d}  arbitrary  " + row(results, us, Ds, lambda res: ham_mask(res, None)))
    print(f"T4 control violations: {vtot}")
    return vtot


def T4b(q=3, n=10, c=5, seeds=range(2), rs=(4, 5), cases=((1.0, None), (1.0, 20.0)), us=(1.0,),
        Ds=(1.0, 5.0, 20.0), frac=0.15, nrandom=300):
    print("T4b: bandwidth r = 4, 5 (as T4); the Lipschitz LP is solved for ALL single-site changes at s = 0 and "
          f"s = r-1, for a random sample of {nrandom} single-site changes at the other s, and for {nrandom} random "
          "arbitrary pairs per model (default_rng(4500 + seed)); pt and box for all pairs")
    print(f"    q = {q}, n = {n}, cut after site {c}; seeds {list(seeds)}")
    Acache, vtot = {}, 0
    for (J, C) in cases:
        print(f"  J = {J}, clash {'none' if C is None else C}")
        print("     r  pairs       " + header(us, Ds))
        for r in rs:
            results = []
            rb = min(r, c)
            for seed in seeds:
                base = B.make_base(n, q, r, np.random.default_rng(4000 + seed), clash_frac=frac)
                model = B.energies(base, J, C)
                al = B.configs(q, rb)
                nA = len(al)
                diff = (al[:, None, :] != al[None, :, :])
                hd = diff.sum(axis=2)
                prng = np.random.default_rng(4500 + seed)
                sel = set()
                for s_ in range(rb):
                    t = rb - 1 - s_
                    cand = np.argwhere((hd == 1) & diff[:, :, t])
                    if s_ not in (0, rb - 1) and len(cand) > nrandom:
                        cand = cand[prng.choice(len(cand), nrandom, replace=False)]
                    sel.update((int(a), int(b_)) for a, b_ in cand)
                while len(sel) < len(sel | set()) + 0 and False:
                    pass
                arb = set()
                while len(arb) < nrandom:
                    a, b_ = int(prng.integers(nA)), int(prng.integers(nA))
                    if a != b_:
                        arb.add((a, b_))
                res = analyse(model, c, us, Ds, Acache, pairs_sel=sorted(sel | arb))
                vtot += res["viol"]
                results.append(res)

            def ham_mask(res, s=None):
                al = res["alphas"]
                diff = (al[:, None, :] != al[None, :, :])
                hd = diff.sum(axis=2)
                if s is None:
                    return hd >= 1
                t = rb - 1 - s
                return (hd == 1) & diff[:, :, t]
            for s_ in range(rb):
                print(f"  {r:4d}  s = {s_}      " + row(results, us, Ds, lambda res, s_=s_: ham_mask(res, s_)))
            print(f"  {r:4d}  arbitrary  " + row(results, us, Ds, lambda res: ham_mask(res, None)))
    print(f"T4b control violations: {vtot}")
    return vtot


def T5():
    print("T5: is the influence a function of the cross-cut interaction only?  Two families with the SAME "
          "cross-cut energies and different inner blocks.")
    vtot = 0
    # (a) binary nearest-neighbour chain; cross pair fixed; a field h on the first inner site
    q, n, c = 2, 6, 3
    rng = np.random.default_rng(5000)
    base = B.make_base(n, q, 1, rng)
    model = B.energies(base, 1.0)
    model["pair"][(c - 1, c)] = np.array([[0.0, 3.0], [3.0, 0.0]])            # cross-cut energies, fixed
    print("  (a) binary chain, cross-cut pair energy [[0,3],[3,0]] kT (osc Delta = 6), field h on the first inner "
          "site (energy +h for state 1):")
    print("        h       pt(0->1)   box D=5   Lip u=1    osc")
    Acache = {}
    vals = []
    for hf in (-8.0, -4.0, -2.0, 0.0, 2.0, 4.0, 8.0):
        model["h"] = np.zeros((n, q))
        model["h"][c] = np.array([0.0, hf])
        res = analyse(model, c, (1.0,), (5.0,), Acache)
        vtot += res["viol"]
        vals.append(res["pt"][0, 1])
        print(f"    {hf:6.1f}   {res['pt'][0, 1]:9.4f} {res[('box', 5.0)][0, 1]:9.4f} {res[('lip', 1.0)][0, 1]:9.4f}"
              f"   {res['osc'][0, 1]:6.3f}")
    print(f"      the same cross-cut interaction gives pointwise influences from {min(vals):.4f} to {max(vals):.4f} "
          f"(bound: osc = 6)")
    if not (max(vals) - min(vals) > 1.0):
        vtot += 1
    # (b) Lipschitz class: the same cross-cut pair and the same law of the first inner site, a rigid or a free
    #     continuation of the inner chain
    print("  (b) binary chain, the same cross-cut pair, inner chain with flip probability p_in (rigid for p_in -> 0):")
    print("        p_in   k   pt(0->1)   Lip u=1   u*k")
    for p_in in (0.5, 0.2, 0.05, 0.005):
        for k in (2, 6):
            n = c + k
            Jc = 0.5 * np.log((1 - p_in) / p_in) if p_in < 0.5 else 0.0
            pair = {(i, i + 1): np.array([[-Jc, Jc], [Jc, -Jc]]) for i in range(n - 1)}
            pair[(c - 1, c)] = np.array([[0.0, 3.0], [3.0, 0.0]])
            model = dict(n=n, q=2, r=1, pair=pair, h=np.zeros((n, 2)))
            res = analyse(model, c, (1.0,), (5.0,), Acache)
            vtot += res["viol"]
            print(f"    {p_in:7.3f} {k:3d}  {res['pt'][0, 1]:9.4f} {res[('lip', 1.0)][0, 1]:9.4f}   {k:3d}")
    print(f"T5 control violations: {vtot}")
    return vtot


if __name__ == "__main__":
    t0 = time.time()
    block = sys.argv[1] if len(sys.argv) > 1 else "T1"
    print(f"r26_influence.py block {block}; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    if block == "T1":
        v = T1()
    elif block == "T1q3":
        v = T1(qs=(3,))
    elif block == "T1q4":
        v = T1(qs=(4,), seeds=range(5), us=(1.0,))
    elif block == "T1q6":
        v = T1(qs=(6,), n=8, c=4, seeds=range(3), us=(1.0,), Ds=(1.0, 5.0, 20.0))
    elif block == "T2":
        v = T2()
    elif block == "T3":
        v = T3()
    elif block == "T4":
        v = T4()
    elif block == "T4b":
        v = T4b()
    elif block == "T3b":
        v = T3b()
    elif block == "T5":
        v = T5()
    else:
        raise SystemExit("unknown block")
    print(f"total control violations: {v}")
    print(f"LP solves by method (fallbacks after a failure of the default solver): {B.LP_FALLBACKS}")
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
    sys.exit(1 if v else 0)
