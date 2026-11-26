#!/usr/bin/env python3
"""R18: one of THEIR cells in which the placement-free bound (searched, job M-014) exceeds the worst product
instance (searched, job M-008): is the excess "a bound and not the cost of an instance" (ENG-RES-0014 §4,
Reading), or the cost of an instance?

Cell: (u, n, phi) from the command line (default 2, 250, 0.85: the largest excess of their table `anyplacement`,
+0.02005 n a).  Inputs taken from their files, as data: the stored maximiser of the bound (x005_anyplacement.jsonl,
decoded with their `Family.decode`), the stored worst product value of the cell (x005_cost.jsonl), and their inner
costs (`alg2l.inner_costs`).  Everything else is my code (r18_mean.py):

  (1) my mean run at the law of their bound-maximiser: the product instance and the bound, against their stored values;
  (2) JOINT LAW: for every shell the place of a grid in [lo, hi] that maximises the shell's own cost -- an instance
      given by its classes (law of (W, place)); its mean-run cost against the bound and against the worst product
      instance found;
  (3) AN ACTUAL psi: psi(a, b) = G(|a|) + sigma(|a|) u |b| with the same fibre averages W(d), the same reference value,
      and slopes sigma(d) that follow the places of (2) as far as u-Lipschitz continuity on every edge allows
      (|G(d+1) - G(d)| <= u and |G(d+1) - G(d) + (sigma(d+1) - sigma(d)) u n_i| <= u; the reference shell keeps the
      product's place, so that psi_0 is unchanged); every edge is then checked, and the fibre averages are
      recomputed from psi.

usage: python3 -I -B r18_cell.py [u n phi]          (their code is imported for decoding and costs: use ulimit -v)
"""
import json
import math
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY = HERE / "rerun_copy"
sys.path.insert(0, str(COPY / "src"))
sys.path.insert(0, str(COPY / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))
import numpy as np                                                              # noqa: E402
import mpmath as mp                                                             # noqa: E402

import r18_mean as M                                                            # noqa: E402
from r18_nonproduct import atom_cost, make_rmax                                 # noqa: E402

ENG = Path("/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c")
RES = ENG / "experiments" / "eng" / "twolevel" / "results"


def main():
    u_f, n, phi = (float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (2.0, 250, 0.85)
    t_start = time.time()
    import run_search
    from metricchain_eng.twolevel.adversary import Family
    from metricchain_eng.twolevel.alg2l import inner_costs
    from metricchain_eng.twolevel.ckernel import Evaluator                      # the R18 adapter (no kernel)

    def cell_of(fname):
        for line in (RES / fname).read_text().splitlines():
            c = json.loads(line)
            if (c["u"], c["n"], c["phi"]) == (u_f, n, phi):
                return c
        raise SystemExit("cell not found in " + fname)

    c_any, c_cost = cell_of("x005_anyplacement.jsonl"), cell_of("x005_cost.jsonl")
    na = n * c_any["a"]
    worst_product_found = max(s["best_value"] for s in c_cost["searches"] if s["objective"] == "cost")
    s_any = max(c_any["searches"], key=lambda s: s["best_value"])
    P, _ = run_search.design_params(n, u_f, phi, c_any["design"])
    ev = Evaluator(P)
    fam = Family(ev, k=c_any["k"], monotone=(s_any["family"] == "monotone"))
    F_f, d0, c_in_f = fam.decode(np.array(s_any["best_x"]))
    lC = inner_costs(P, ev.C)
    orc = s_any["oracle"]
    print(f"cell u={u_f:g} n={n} phi={phi}: n_o={P.n_o} n_i={P.n_i} L={P.L}; n a = {na:.4f}")
    print(f"  their files: worst product instance found (M-008) ln cost {worst_product_found:.6f}; bound searched (M-014) {s_any['best_value']:.6f} "
          f"({s_any['family']}/{orc}); excess {(s_any['best_value'] - worst_product_found):+.6f} = {(s_any['best_value'] - worst_product_found) / na:+.5f} n a")
    # ---- my design, from the same numbers
    u = Fr(u_f)
    xs = [Fr(x) for x in P.xs]
    xs[0] = 2 * u * P.n_i
    D = M.Design(n, P.n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, P.nu1, Fr(1, 2), 0.05, xs, lC=[None] + [float(x) for x in lC[1:]])
    assert (D.J, D.K, D.r_dag, D.m_max) == (ev.C.J, ev.C.K, ev.C.r_dag, ev.C.m_max)
    n_o, n_i = D.n_o, D.n_i
    L1 = math.log(2 / (1 + math.exp(-u_f)))
    lo, hi = Fr(n_i * (u_f - L1)), Fr(n_i * (2 * u_f - L1))
    F = [Fr(float(x)) for x in F_f]
    c_in = Fr(float(c_in_f))
    psi0 = F[d0]
    t_ref = u * n_i + c_in
    pos = M.uniform_positions(D, orc)
    lnW = [c_in - F[d] for d in range(n_o + 1)]
    binom = D.cube.binom
    den = 1 << n_o
    TOL = M.POP_TOL_THEIRS
    Rp = M.mean_run(D, [(lnW[d], binom[d], t_ref, pos) for d in range(n_o + 1)], den, psi0, pop_tol=TOL)
    Rb = M.mean_run(D, [(lnW[d], binom[d], t_ref, pos) for d in range(n_o + 1)], den, psi0, union=(lo, hi), pop_tol=TOL)
    Rt_prod = ev.run(fam.instance(F_f, d0, c_in_f), orc)                       # their decode, their Instance, their reference
    print(f"  (0) THEIR reference on the stored maximiser of the bound, taken as the product instance it decodes to (their family: {s_any['family']}, 8 knots): "
          f"ln cost {Rt_prod.lcost:.6f} = worst product instance found {Rt_prod.lcost - worst_product_found:+.6f} ({(Rt_prod.lcost - worst_product_found) / na:+.5f} n a); "
          f"claims violated: {Rt_prod.violations()}")
    print(f"  (1) my mean run at their bound-maximiser's law: product instance ln cost {float(Rp.lcost):.6f}; bound {float(Rb.lcost):.6f} "
          f"(their stored bound {s_any['best_value']:.6f}; difference {float(Rb.lcost) - s_any['best_value']:+.2e}); "
          f"level {Rp.j_stop}, largest sample K 2^{Rp.m_top}; reference shell d0 = {d0}, product place {float(t_ref):.4f} in [{float(lo):.4f}, {float(hi):.4f}]")
    print(f"      calls per rung, product: {[('%.4g' % float(x)) for x in Rp.calls[1:4]]} ...; bound: {[('%.4g' % float(x)) for x in Rb.calls[1:4]]} ...; "
          f"ln C_1 = {float(lC[1]):.3f}, ln C_L = {float(lC[-1]):.3f}")
    # ---- (2) the dearest place for every shell
    rmax = make_rmax(Rp.ms)
    grid = [lo + (hi - lo) * Fr(i, 32) for i in range(33)]
    best_place = []
    for d in range(n_o + 1):
        best_place.append(max(grid, key=lambda t: atom_cost(D, lnW[d], t, pos, Rp.ms, Rp.ls0, Rp.j_stop, rmax)))
    Rj = M.mean_run(D, [(lnW[d], binom[d], best_place[d], pos) for d in range(n_o + 1)], den, psi0, pop_tol=TOL)
    assert Rj.ms == Rp.ms
    # the same with the reference shell kept at the product's place (then psi_0 is that of the product instance exactly)
    bp2 = list(best_place)
    bp2[d0] = t_ref
    Rj2 = M.mean_run(D, [(lnW[d], binom[d], bp2[d], pos) for d in range(n_o + 1)], den, psi0, pop_tol=TOL)
    print(f"  (2) joint law, the dearest place per shell: ln cost {float(Rj.lcost):.6f} = bound {float(Rj.lcost - Rb.lcost):+.2e}; "
          f"with the reference shell at the product's place: {float(Rj2.lcost):.6f}; above the worst product instance found by "
          f"{float(Rj2.lcost) - worst_product_found:+.6f} = {(float(Rj2.lcost) - worst_product_found) / na:+.5f} n a")
    places_f = [float(t) for t in bp2]
    ch = [d for d in range(1, n_o + 1) if places_f[d] != places_f[d - 1]]
    print(f"      places used: {sorted(set(round(x, 3) for x in places_f))[:6]}{' ...' if len(set(places_f)) > 6 else ''}; shells at which the place changes: {ch[:12]}{' ...' if len(ch) > 12 else ''}")
    # ---- (3) an actual psi: cone fibres of slope sigma(d) u; place tau(sigma) = u n_i + n_i ln((1 + e^{-sigma u})/2)
    def tau(sig):
        return u_f * n_i + n_i * math.log((1 + math.exp(-sig * u_f)) / 2)

    def sigma_of(t):                                        # inverse of tau on [-1, 1]
        y = math.exp((t - u_f * n_i) / n_i) * 2 - 1         # e^{-sigma u}
        return max(-1.0, min(1.0, -math.log(max(y, 1e-300)) / u_f))

    lnW_f = [float(x) for x in lnW]
    target = [sigma_of(float(t)) for t in bp2]
    sig = [None] * (n_o + 1)
    sig[d0] = sigma_of(float(t_ref))

    def G(d, s):                                            # psi(a, 0) for a in shell d with fibre slope s
        return -lnW_f[d] + tau(s) - u_f * n_i

    def feasible(d_from, s_from, d_to, s_to):
        # the same slope on both shells: psi differs by -(ln W(d_to) - ln W(d_from)) at every b, at most u because the law is
        # u-Lipschitz (exact).  A change of slope is accepted only with a margin of 1e-9 u, far above the rounding of floats.
        if s_to == s_from:
            return True
        dG = G(d_to, s_to) - G(d_from, s_from)
        return abs(dG) <= u_f * (1 - 1e-9) and abs(dG + (s_to - s_from) * u_f * n_i) <= u_f * (1 - 1e-9)

    for rng_ in (range(d0 + 1, n_o + 1), range(d0 - 1, -1, -1)):
        for d in rng_:
            prev = d - 1 if d > d0 else d + 1
            s_prev = sig[prev]
            want = target[d]
            # the slope closest to the target that keeps every edge between the two shells u-Lipschitz (bisection from s_prev)
            if feasible(prev, s_prev, d, want):
                sig[d] = want
                continue
            a, b_ = s_prev, want                             # a = s_prev is feasible (the law itself is u-Lipschitz), b_ is not
            for _ in range(60):
                mid = (a + b_) / 2
                if feasible(prev, s_prev, d, mid):
                    a = mid
                else:
                    b_ = mid
            sig[d] = a
    psi = lambda d, e: G(d, sig[d]) + sig[d] * u_f * e      # noqa: E731
    worst_edge = 0.0
    for d in range(n_o + 1):
        for e in range(n_i + 1):
            if d < n_o:
                worst_edge = max(worst_edge, abs(psi(d + 1, e) - psi(d, e)))
            if e < n_i:
                worst_edge = max(worst_edge, abs(psi(d, e + 1) - psi(d, e)))
    lnW_psi, t0_psi = [], []
    for d in range(n_o + 1):
        w = mp.log(mp.fsum(math.comb(n_i, e) * mp.e ** (-mp.mpf(psi(d, e))) for e in range(n_i + 1)) / 2 ** n_i)
        lnW_psi.append(Fr(float(w)))
        t0_psi.append(Fr(psi(d, 0)) + u * n_i + Fr(float(w)))
    dev = max(abs(float(lnW_psi[d]) - lnW_f[d]) for d in range(n_o + 1))
    psi0_psi = Fr(psi(d0, 0))
    Rpsi = M.mean_run(D, [(lnW_psi[d], binom[d], t0_psi[d], pos) for d in range(n_o + 1)], den, psi0_psi, pop_tol=TOL)
    Rpsi_prod = M.mean_run(D, [(lnW_psi[d], binom[d], t0_psi[d0], pos) for d in range(n_o + 1)], den, psi0_psi, pop_tol=TOL)
    Rpsi_b = M.mean_run(D, [(lnW_psi[d], binom[d], t0_psi[d0], pos) for d in range(n_o + 1)], den, psi0_psi, union=(lo, hi), pop_tol=TOL)
    print(f"  (3) an actual psi (cone fibres, slopes following (2) under the Lipschitz constraint): largest |psi(x) - psi(y)| over all edges {worst_edge:.9f} (u = {u_f:g}); "
          f"largest |ln W(psi) - ln W(law)| {dev:.2e}; |psi_0 - product's| {abs(float(psi0_psi) - float(psi0)):.2e}; places from {float(min(t0_psi)):.3f} to {float(max(t0_psi)):.3f}")
    print(f"      mean run of psi: ln cost {float(Rpsi.lcost):.6f}; the product instance with its law: {float(Rpsi_prod.lcost):.6f}; the bound at its law: {float(Rpsi_b.lcost):.6f}; "
          f"sample sizes equal to the product's: {Rpsi.ms == Rpsi_prod.ms}; calls of I_1: psi {float(Rpsi.calls[1]):.4g}, product {float(Rpsi_prod.calls[1]):.4g}, bound {float(Rpsi_b.calls[1]):.4g}")
    ex = float(Rpsi.lcost) - worst_product_found
    print(f"      psi against the worst product instance FOUND in this cell by their search: {ex:+.6f} in ln cost = {ex / na:+.5f} n a   "
          f"({'AN INSTANCE THAT IS NOT A PRODUCT COSTS MORE than the worst product instance found' if ex > 1e-6 else 'not above'}); below C_max: {bool(Rpsi.lcost <= D.lCmax)}")
    assert worst_edge <= u_f * (1 + 1e-12), worst_edge
    worst_changing = max([abs(psi(d + 1, e) - psi(d, e)) for d in range(n_o) for e in range(n_i + 1) if sig[d + 1] != sig[d]] or [0.0])
    law_lip = max(abs(lnW_f[d + 1] - lnW_f[d]) for d in range(n_o))
    print(f"      (edges: where the slope changes between shells the largest difference is {worst_changing:.9f} <= u (1 - 1e-9); elsewhere the difference is |ln W(d+1) - ln W(d)| "
          f"<= {law_lip:.12f} across shells and |sigma| u <= u inside a fibre -- exact; float evaluation gives max - u = {worst_edge - u_f:+.1e})")
    # ---- (4) can a PRODUCT instance do the same?  Every fibre at the place t of the bulk of (2) (c_in' = t - u n_i), the outer
    #          profile chosen so that ln W + psi_0 is that of the bound-maximiser on the bulk, and the reference point moved
    #          to the shell d1 where that costs the least probability:  with T(d) = ln W(d) + psi_0 of the maximiser,
    #          Fnat(d) = c_in' - T(d), the product instance needs F'(d1) = 0 = its reference value; so
    #          F'(d) = max(Fnat(d), -u |d - d1|) if Fnat(d1) <= 0, min(Fnat(d), u |d - d1|) otherwise
    #          (u-Lipschitz as a maximum / minimum of u-Lipschitz functions).  The law changes only on the shells where F' != Fnat.
    from collections import Counter
    t_bulk = Counter(bp2[d] for d in range(n_o + 1) if d != d0).most_common(1)[0][0]
    c_in2 = t_bulk - u * n_i
    T = [lnW[d] + psi0 for d in range(n_o + 1)]
    Fnat = [c_in2 - T[d] for d in range(n_o + 1)]
    best4 = None
    for d1 in range(n_o + 1):
        if Fnat[d1] <= 0:
            cand = [max(Fnat[d], -u * abs(d - d1)) for d in range(n_o + 1)]
        else:
            cand = [min(Fnat[d], u * abs(d - d1)) for d in range(n_o + 1)]
        mass = sum(binom[d] for d in range(n_o + 1) if cand[d] != Fnat[d])
        if best4 is None or mass < best4[0]:
            best4 = (mass, d1, cand)
    mass4, d1, F2 = best4
    lip = max(abs(F2[d + 1] - F2[d]) for d in range(n_o))
    mono = all(F2[d + 1] >= F2[d] for d in range(n_o))
    changed = [d for d in range(n_o + 1) if F2[d] != Fnat[d]]
    ln_mass = float(mp.log(mp.mpf(mass4) / den)) if mass4 else -math.inf
    at4 = [(c_in2 - F2[d], binom[d], t_bulk, pos) for d in range(n_o + 1)]
    R4 = M.mean_run(D, at4, den, F2[d1], pop_tol=TOL)
    slopes = [round(float((F2[d + 1] - F2[d]) / u), 6) for d in range(n_o)]
    nseg = 1 + sum(slopes[i] != slopes[i - 1] for i in range(1, len(slopes)))
    ex4 = float(R4.lcost) - worst_product_found
    print(f"  (4) a PRODUCT instance: every fibre at {float(t_bulk):.4f} (c_in = {float(c_in2):.4f}), reference point in shell d1 = {d1}, profile = the maximiser's law with a ramp of slope u "
          f"to the reference shell ({len(changed)} shells changed, d = {changed[0] if changed else '-'}..{changed[-1] if changed else '-'}, ln of their probability {ln_mass:.1f}); "
          f"largest |F'(d+1) - F'(d)| = {float(lip):.6f} (u = {u_f:g}); monotone: {mono}; runs of constant slope: {nseg}")
    print(f"      its mean run: ln cost {float(R4.lcost):.6f} (level {R4.j_stop}, largest sample K 2^{R4.m_top}); against the worst product instance found: {ex4:+.6f} = {ex4 / na:+.5f} n a; "
          f"against the bound searched: {float(R4.lcost) - s_any['best_value']:+.6f}")
    # ---- (5) the same two inputs through THEIR reference
    from metricchain_eng.twolevel.meanrun import Instance, Law, radial_law
    lpr = ev.outer.lbinom - n_o * math.log(2)
    Rt3 = ev.run(Instance(Law(np.array([float(x) for x in lnW]), lpr.copy()), psi0=float(psi0), t0=float(t_bulk)), orc)
    Rt4 = ev.run(Instance(radial_law(np.array([float(x) for x in F2]), ev.outer, shift=float(c_in2)), psi0=float(F2[d1]), t0=float(u * n_i + c_in2)), orc)
    print(f"  (5) THEIR reference: the law of (1) with every fibre at {float(t_bulk):.4f} (the psi of (3) up to the shells near the reference): ln cost {Rt3.lcost:.6f}; "
          f"the product instance of (4): {Rt4.lcost:.6f} (mine {float(R4.lcost):.6f}); violations of the theorem's claims in that run: {Rt4.violations()}; ln C_max {Rt4.lCmax:.6f}")
    out = HERE / f"data_cell_u{u_f:g}_n{n}_phi{phi:g}.json"
    if not out.exists():
        out.write_text(json.dumps(dict(u=u_f, n=n, phi=phi, n_o=n_o, n_i=n_i, oracle=orc, d0=d0, na=na, worst_product_found=worst_product_found,
                                       bound_searched=s_any["best_value"], psi=dict(lnW=[float(x) for x in lnW_psi], place=[float(x) for x in t0_psi],
                                                                                    sigma=sig, psi0=float(psi0_psi), lcost=float(Rpsi.lcost)),
                                       product=dict(F=[float(x) for x in F2], c_in=float(c_in2), d1=d1, psi0=float(F2[d1]), lcost_mine=float(R4.lcost),
                                                    lcost_their_reference=Rt4.lcost)), indent=0) + "\n")
        print("  instances written to", out.name)
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t_start:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")


if __name__ == "__main__":
    main()
