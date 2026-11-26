#!/usr/bin/env python3
"""The Complexity division's zero-temperature threshold on our four floors (their COMPLEXITY-RES-0005 and
docs/complexity/PENALTY_THRESHOLD.md at ff04e5e, Theorem 2 and Proposition 3; nothing of their code is used).

Their setting: a PRODUCT reference with off-probabilities q_i, non-negative tables gamma_U that vanish unless all sites of U
are off the anchor.  Then
    lambda_0 = min over site sets S of  sum_{i in S} ln(1/q_i) / sum_{U subset of S} max gamma_U          (a minimum cut),
    lambda*  = lambda_0 (1 - ln(e Delta) / ln(1/q_max)),   Delta = largest degree of the graph "two sites share a table",
and below lambda* a polymer sum bounds the gain.  Their lambda_1 (least ratio with the actual tables and states) is, for
the true reference, our lambda_gs of floor_ground_state.py.
Our reference is a band model, NOT a product: this script applies their formula with the band model's own one-site
off-probabilities -- a heuristic use of a theorem outside its hypothesis, reported as such -- to see how far the binary
relaxation is from the measured transition.  Per case (the driver floor_transition.py is run in-process and its objects taken
from its frame, as in floor_ground_state.py):
  q_i     exact: ln Z of the floor without penalty with site i restricted to its anchor state (one pass per site);
  tables  the window-form penalty tables (one-site, pair, larger), in kT; their maxima;
  lambda_0 by brute force over all 2^n - 1 site sets, with the minimising set; lambda*; the site graph's degree;
  the factor lambda_gs / lambda_0 split exactly into three, at the extremal state x* (recomputed here by one (min,+) pass
  just above lambda_gs; its penalty and cost must reproduce the committed ground-state log) with displaced sites S*:
      A = [sum_{S*} ln(1/q_i) / (table maxima inside S*)] / lambda_0       (S* is not the binary minimiser),
      B = c* / sum_{S*} ln(1/q_i) = B1 x B2,   B1 = ln(1/P_0(all of S* off)) / sum_{S*} ln(1/q_i)   (correlation under the band
          reference: 1 for a product),   B2 = c* / ln(1/P_0(all of S* off))   (one state against all states with that set),
      C = (table maxima inside S*) / b*                                    (maxima against the penalty the state pays);
  and the product assumption at the full set: ln(1/P_0(all sites off)) against sum ln(1/q_i).
Check: the off-probabilities against exact samples of the floor (must agree within sampling); gamma_max(all sites) against
the sum of the table maxima printed by the driver.  Control: lambda_0 must not exceed the ratio at any single set (trivial)
and must be reproduced by a second implementation (subset sums by inclusion over table keys instead of over sets).
Output: a line per case and a JSON file with q_i and the table maxima, for the Complexity division.
Run: python3 -B product_threshold.py K12 4 4 > product_threshold_K12_m4_w4.log
"""
import os, sys, io, re, json, time, math, contextlib, itertools, resource
import numpy as np
import floor_transition as FT
HERE = os.path.dirname(os.path.abspath(__file__)); BIG = 1.0e5


def capture(argv):
    got = {}

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is FT.main.__code__: got.update(frame.f_locals)
    old = sys.argv; sys.argv = ["floor_transition.py"] + argv; buf = io.StringIO(); sys.setprofile(prof)
    try:
        with contextlib.redirect_stdout(buf): FT.main()
    finally:
        sys.setprofile(None); sys.argv = old
    return got, buf.getvalue()


def main():
    seq, m, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); t0 = time.time(); BETA = FT.BETA
    got, text = capture([seq, str(m), str(w), "--grid", "0,0.01", "--N", "4"])
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("(1)"): print(line[:420], flush=True)
    lo0, g1, g2, g3, n, k, x0 = got["lo0"], got["g1"], got["g2"], got["g3"], got["n"], list(got["k"]), [int(v) for v in got["x0"]]
    # ---- off-probabilities under the floor without penalty (exact) and from exact samples
    lz = lo0.lnZ(); q = np.zeros(n)
    for i in range(n):
        old = lo0.one[i]; pen = np.full(len(old), BIG); pen[x0[i]] = 0.0; lo0.one[i] = old + pen; q[i] = 1.0 - math.exp(lo0.lnZ() - lz); lo0.one[i] = old
    X = lo0.sample(20000, np.random.default_rng(99)); qs = (X != np.array(x0)[None]).mean(axis=0); se = np.sqrt(q * (1 - q) / len(X))      # the standard error from the EXACT q
    zdev = float(np.abs((qs - q) / np.maximum(se, 1e-300)).max())            # (a first version used the sampled frequency, which is 0 at a site that is almost never off, and divided by it)
    print(f"(a) off-probabilities q_i under the floor without penalty (exact, one restricted pass per site): {', '.join(f'{v:.3g}' for v in q)}; mean number of sites off: {q.sum():.3f}; "
          f"against 20000 exact samples: largest deviation {zdev:.2f} standard errors (must be below 5) [{time.time() - t0:.0f}s]", flush=True)
    assert zdev < 5
    # ---- table maxima in kT
    tab = {}
    for i in range(n):
        if g1[i].any(): tab[(i,)] = BETA * float(g1[i].max())
    for K, v in list(g2.items()) + list(g3.items()): tab[tuple(int(u) for u in K)] = BETA * float(v.max())
    total = sum(tab.values()); sizes = sorted(set(len(K) for K in tab))
    deg = [len(set(u for K in tab if i in K for u in K) - {i}) for i in range(n)]; Delta = max(deg)
    drv = float(re.search(r"sum of their maxima ([0-9.e+]+) kT \[", text).group(1))
    print(f"(b) {len(tab)} window-form tables on site sets of sizes {sizes}; sum of their maxima {total:.5g} kT (the driver printed {drv:.5g}); site graph: degrees {min(deg)} to {Delta}")
    assert abs(total - drv) <= 2e-4 * drv
    # ---- lambda_0 by brute force over site sets, two implementations
    lq = np.log(1.0 / q); masks = {K: sum(1 << u for u in K) for K in tab}; best = (math.inf, None); gm = np.zeros(1 << n)
    for S in range(1, 1 << n):
        g = sum(v for K, v in tab.items() if masks[K] & S == masks[K]); gm[S] = g
        if g > 0:
            r = sum(lq[i] for i in range(n) if S >> i & 1) / g
            if r < best[0]: best = (r, S)
    lam0, S0 = best; Sset = [i for i in range(n) if S0 >> i & 1]
    # second implementation: zeta transform (sum over subsets) of the table weights
    f = np.zeros(1 << n)
    for K, v in tab.items(): f[masks[K]] += v
    for b in range(n):
        idx = np.arange(1 << n); hasb = (idx >> b & 1).astype(bool); f[hasb] += f[idx[hasb] ^ (1 << b)]
    cost = np.zeros(1 << n)
    for b in range(n):
        idx = np.arange(1 << n); cost[(idx >> b & 1).astype(bool)] += lq[b]
    with np.errstate(divide="ignore", invalid="ignore"): ratio = np.where(f > 0, cost / f, np.inf)
    lam0b = float(ratio[1:].min()); assert abs(lam0b - lam0) <= 1e-9 * lam0 and np.abs(f - gm).max() <= 1e-9 * total
    qmax = float(q.max()); fac = 1.0 - math.log(math.e * Delta) / math.log(1.0 / qmax)
    print(f"(c) **lambda_0 = {lam0:.4f}** (both implementations agree to {abs(lam0b - lam0) / lam0:.1e}); minimising set: {len(Sset)} of {n} sites {Sset}, sum ln(1/q_i) = {sum(lq[i] for i in Sset):.3f}, "
          f"table maxima inside it {gm[S0]:.4g} kT; at the full set the ratio is {lq.sum() / total:.4f}")
    print(f"(d) their explicit criterion: q_max = {qmax:.4f}, 1/(e Delta) = {1 / (math.e * Delta):.4f}: the entropy factor is {fac:.3f} -> "
          f"{'VOID (q_max >= 1/(e Delta))' if fac <= 0 else f'lambda* = {lam0 * fac:.4f}'}")
    # ---- against the measured transition and the least ratio over states (committed logs)
    tag = f"{seq.replace(':', 'c')}_m{m}_w{w}"; lam_c = lam_gs = bstar = cstar = None; soff = None
    fn = os.path.join(HERE, f"floor_ground_state_{tag}.log")
    if os.path.exists(fn):
        t = open(fn).read(); lam_c = float(re.search(r"measured lambda_c there ([0-9.]+)", t).group(1))
        mm = re.search(r"\(d\) lambda_gs in \[([0-9.]+), [0-9.]+\] \(G = 0\): minimiser with (\d+) of \d+ sites off the anchor, penalty b\* = ([0-9.]+) kT, cost c\* = ([0-9.]+)", t)
        lam_gs, soff, bstar, cstar = float(mm.group(1)), int(mm.group(2)), float(mm.group(3)), float(mm.group(4))
        print(f"(e) from floor_ground_state_{tag}.log: measured lambda_c = {lam_c}, least ratio over states lambda_gs = {lam_gs} (extremal state: {soff} sites off, penalty {bstar} kT, cost {cstar} kT);  "
              f"**lambda_0 / lambda_c = {lam0 / lam_c:.3f}**, lambda_0 / lambda_gs = {lam0 / lam_gs:.3f}")
    # ---- where the factor lambda_gs / lambda_0 comes from: the extremal state itself (one (min,+) pass just above lambda_gs)
    extra = {}
    if lam_gs is not None:
        import floor_ground_state as FG
        model, pen, z0 = got["model"], got["pen"], got["z0"]; m0 = model(0.0); x0a = np.array(x0)
        e_, xs = FG.argmin_state(model(lam_gs * 1.0005)); xs = np.array(xs, dtype=int)
        b_here = BETA * FT.RND * float(pen(xs[None])[0]); c_here = z0 + BETA * float(m0.energy(xs[None])[0]); Sstar = [i for i in range(n) if xs[i] != x0a[i]]
        print(f"(f) the extremal state recomputed here (one (min,+) pass at 1.0005 lambda_gs): state {[int(v) for v in xs]}, displaced sites S* = {Sstar}; penalty {b_here:.5g} kT, cost {c_here:.5g} kT, "
              f"ratio {c_here / b_here:.5g} (the committed log: {bstar}, {cstar}, {lam_gs}; must agree to 2e-4)", flush=True)
        assert abs(b_here - bstar) <= 2e-4 * bstar and abs(c_here - cstar) <= 2e-4 * cstar and len(Sstar) == soff

        def set_cost(S):                                           # ln(1 / P_0(every site of S is off its anchor)) under the floor without penalty: one restricted pass
            olds = {i: lo0.one[i] for i in S}
            for i in S:
                pen_ = np.zeros(len(olds[i])); pen_[x0[i]] = BIG; lo0.one[i] = olds[i] + pen_
            v = lz - lo0.lnZ()
            for i in S: lo0.one[i] = olds[i]
            return v
        mS = sum(1 << i for i in Sstar); gS = float(gm[mS]); lqS = float(sum(lq[i] for i in Sstar)); cS = set_cost(Sstar); call = set_cost(list(range(n)))
        chk = abs(set_cost([0]) - lq[0])                           # control of set_cost: a single site must give ln(1/q_0)
        rS = lqS / gS; A = rS / lam0; B = c_here / lqS; B1 = cS / lqS; B2 = c_here / cS; C = gS / b_here; lam_here = c_here / b_here
        assert abs(A * B * C - lam_here / lam0) <= 1e-9 * lam_here / lam0 and abs(B1 * B2 - B) <= 1e-9 * B and chk < 1e-6 and lo0.lnZ() == lz
        print(f"(g) lambda_gs / lambda_0 = {lam_here / lam0:.3f} = A x B x C exactly, with\n"
              f"    A = {A:.3f}: the binary ratio at the extremal state's own displaced set, sum_(S*) ln(1/q_i) / (table maxima inside S*) = {lqS:.3f} / {gS:.5g} = {rS:.5g}, against its minimum lambda_0 = {lam0:.5g};\n"
              f"    B = {B:.3f}: the cost of the state, {c_here:.5g}, against sum_(S*) ln(1/q_i) = {lqS:.3f}; of it  B1 = {B1:.3f}: ln(1 / P_0(all of S* off)) = {cS:.3f} against that sum "
              f"(1 for a product reference; below 1: displaced sites come together under the band reference),  B2 = {B2:.3f}: one state against all states with that displaced set;\n"
              f"    C = {C:.3f}: the table maxima inside S*, {gS:.5g} kT, against the penalty the state pays, {b_here:.5g} kT")
        print(f"(h) the product assumption at the full set: ln(1 / P_0(all {n} sites off)) = {call:.3f} against sum ln(1/q_i) = {lq.sum():.3f}; with the true probability the binary ratio at the full set is "
              f"{call / total:.5g} (with the product of the one-site probabilities: {lq.sum() / total:.5g}); control of the restricted pass: one site against ln(1/q_0): {chk:.1e}")
        extra = dict(extremal_state=[int(v) for v in xs], displaced_sites=Sstar, penalty_kT=b_here, cost_kT=c_here, factor_A=A, factor_B=B, factor_B1=B1, factor_B2=B2, factor_C=C,
                     ln_inv_P_all_of_Sstar_off=cS, ln_inv_P_all_sites_off=call)
    out = dict(case=tag, sites=n, states_per_site=k, anchor=x0, q=[float(v) for v in q], lambda_0=lam0, minimising_set=Sset, Delta=Delta, q_max=qmax, entropy_factor=fac,
               measured_lambda_c=lam_c, lambda_gs=lam_gs, table_maxima_kT={",".join(str(u) for u in K): v for K, v in sorted(tab.items())},
               **extra,
               note="q: off-anchor probabilities under the floor without penalty (a band model, not a product); table_maxima_kT: beta times the maximum of each window-form penalty table")
    json.dump(out, open(os.path.join(HERE, f"product_threshold_{tag}.json"), "w"), indent=1)
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
