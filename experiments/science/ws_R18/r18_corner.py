#!/usr/bin/env python3
"""R18: the two places where the range condition of ENG-RES-0014 §1/§4 is NOT met.

Part 1 (control of item 1; "their own example says the cost ratio reaches e^{4.2}").  "top" with the value
within the tolerance of the lower end of the trivial bracket (t0 < b), flat landscape, the design of their
sampled runs (ENG-RES-0008 §6: b = 0.5, lambda = 0.5, eta = 1/4, eta' = theta = 0.1, delta = 0.05; ladder rates
0.9, 0.45, 0.2; n_i = 6; (u, n_o) = (1/2, 300), (1, 120), (2, 48)).
  mean runs : mine (exact) and their reference, each with the exact rule and with the old convention (c = 0);
  literal   : our r6lib on the same instance -- which of the two does the literal algorithm side with?

Part 2 (finding on §4 and on `rung_positions` with a pair).  Designs with lo < b or x_0 - hi < b.  The pair mode
takes its classification shift from A_0 = hi, B_0 = x_0 - lo; is its value still an upper bound on the cost of
every instance with places in [lo, hi]?  Searched with THEIR reference: product instances at feasible places
against the pair-mode value for the same law; the worst case is re-evaluated with my code.

usage: python3 -I -B r18_corner.py <part1|part2> [cases] [seed]      (their code is run: use ulimit -v)
"""
import json
import math
import random
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "rerun_copy" / "src"))
sys.path.insert(0, str(HERE.parent / "ws_R6"))
sys.path.insert(0, str(HERE))
import numpy as np                                                              # noqa: E402
import mpmath as mp                                                             # noqa: E402

import r18_mean as M                                                            # noqa: E402
from metricchain_eng.twolevel import meanrun as their                           # noqa: E402
from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs, lC_max   # noqa: E402
from metricchain_eng.twolevel.tables import CubeTables                          # noqa: E402

ORIG_RP = their.rung_positions


def their_run(P, tabs, C, lC, lw, lpr, psi0, t0, oracle, legacy=False, t0_range=None):
    inst = their.Instance(their.Law(np.array(lw, dtype=float), np.array(lpr, dtype=float)), psi0=psi0, t0=t0)
    kw = dict(C=C, lC=lC, record=True, legacy_classification=legacy)
    if t0_range is None:
        return their.mean_run(P, tabs, inst, oracle, **kw)
    their.rung_positions = lambda P_, t0_, oracle_="bottom", positions_=None, legacy_=False: ORIG_RP(P_, t0_range, oracle_, positions_, legacy_)
    try:
        return their.mean_run(P, tabs, inst, oracle, **kw)
    finally:
        their.rung_positions = ORIG_RP


def part1(runs, seed):
    import r6lib
    print("PART 1: the old convention (c = b for 'bottom', c = 0 for 'top') outside its range, i.e. t0 < b ('top') or x0 - t0 < b ('bottom')")
    print("  (A) their kind of test input: flat law ln W = 0, psi0 = 0, and a place t0 given independently (mean runs only: such a triple is")
    print("      not an instance -- a flat psi has psi(a, 0) = psi0 for every fibre, hence ln W = t0 - u n_i - psi0)")
    print("  (B) consistent instances with every fibre at the place t0: flat, and an outer cone of slope u/2; literal runs of r6lib against")
    print("      the two mean runs AT THE SAME instance")
    worstA = 0.0
    tot = dict(cases=0, differ=0, lit_runs=0, side_exact=0, side_old=0, side_neither=0)
    for (u, n_o, n_i) in ((Fr(1, 2), 300, 6), (Fr(1), 120, 6), (Fr(2), 48, 6)):
        for lam in (Fr(1, 2), Fr(1, 5)):
            n = n_o + n_i
            b, eta = Fr(1, 2), Fr(1, 4)
            x0 = 2 * u * n_i
            xs = [x0] + [r * n_i for r in (Fr(9, 10), Fr(9, 20), Fr(1, 5)) if b < r * n_i < x0] + [b]
            nu1 = max(1.0, 2 * math.exp(float(u)) * n_o / 0.1)
            P = Params(n=n, n_o=n_o, u=float(u), lam=float(lam), eta=0.25, etap=0.1, theta=0.1, nu1=nu1, b=0.5, delta=0.05, xs=tuple(float(x) for x in xs))
            tabs = CubeTables(n_o, float(u))
            C = constants(P, tabs)
            lC = inner_costs(P, C)
            D = M.Design(n, n_o, u, lam, eta, 0.1, 0.1, nu1, b, 0.05, xs, lC=[None] + [float(x) for x in lC[1:]])
            assert (D.J, D.K, D.r_dag, D.m_max) == (C.J, C.K, C.r_dag, C.m_max)
            costs = [float(mp.e ** mp.mpf(float(x))) for x in lC[1:]]
            P6 = r6lib.Params2LP(n, n_o, float(u), mp.mpf(lam.numerator) / lam.denominator, eta, 0.1, 0.1, nu1, 0.5, 0.05, [float(x) for x in xs], costs)
            assert (P6.J, P6.K, P6.rdag, P6.m_max) == (D.J, D.K, D.r_dag, D.m_max)
            lpr = (tabs.lbinom - n_o * math.log(2)).tolist()
            prob = [mp.mpf(D.cube.binom[d]) / 2 ** n_o for d in range(n_o + 1)]
            for orc, t0 in (("top", Fr(1, 8)), ("top", Fr(1, 4)), ("bottom", x0 - Fr(1, 4))):
                pos = M.uniform_positions(D, orc)
                c_exact = M.shift_c(D, *M.nested_positions(D, t0, pos))
                c_old = b if orc == "bottom" else Fr(0)
                # ---- (A)
                atoms = [(Fr(0), D.cube.binom[d], t0, pos) for d in range(n_o + 1)]
                Rm_e = M.mean_run(D, atoms, 1 << n_o, Fr(0), pop_tol=M.POP_TOL_THEIRS)
                Rm_o = M.mean_run(D, atoms, 1 << n_o, Fr(0), c_force=c_old, pop_tol=M.POP_TOL_THEIRS)
                Rt_e = their_run(P, tabs, C, lC, [0.0] * (n_o + 1), lpr, 0.0, float(t0), orc)
                Rt_o = their_run(P, tabs, C, lC, [0.0] * (n_o + 1), lpr, 0.0, float(t0), orc, legacy=True)
                agree = (Rm_e.j_stop == Rt_e.j_stop and abs(float(Rm_e.lcost) - Rt_e.lcost) < 1e-8 and
                         Rm_o.j_stop == Rt_o.j_stop and abs(float(Rm_o.lcost) - Rt_o.lcost) < 1e-8)
                dA = float(Rm_e.lcost - Rm_o.lcost)
                worstA = max(worstA, abs(dA))
                print(f"  u={float(u):g} n_o={n_o} lambda={lam} {orc:6s} t0={float(t0):6.3f} (exact c={float(c_exact):.3f}, old c={float(c_old):.1f})")
                print(f"     (A) ln cost exact {float(Rm_e.lcost):.4f} (level {Rm_e.j_stop}, m {Rm_e.m_top}) / old {float(Rm_o.lcost):.4f} (level {Rm_o.j_stop}, m {Rm_o.m_top}): "
                      f"difference {dA:+.4f}; my two runs = their reference's two runs: {agree}")
                # ---- (B)
                kapq = u * n_i - t0                                   # -psi(a,0) - ln W, the same for every fibre
                for land, Fq in (("flat", [Fr(0)] * (n_o + 1)), ("cone u/2", [u / 2 * d for d in range(n_o + 1)])):
                    d0 = n_o // 2
                    lnWq = [-Fq[d] - kapq for d in range(n_o + 1)]   # psi(a, 0) = F(d):  ln W = -F - kap
                    psi0q = Fq[d0]
                    atoms_l = [(lnWq[d], D.cube.binom[d], t0, pos) for d in range(n_o + 1)]
                    Rl_e = M.mean_run(D, atoms_l, 1 << n_o, psi0q)
                    Rl_o = M.mean_run(D, atoms_l, 1 << n_o, psi0q, c_force=c_old)
                    inst = r6lib.ClassInstance(n, n_o, float(u), [float(x) for x in lnWq], prob, float(kapq),
                                               r6lib.S_BOTTOM if orc == "bottom" else r6lib.S_TOP, d0, land)
                    assert abs(inst.psi0 - float(psi0q)) < 1e-12
                    differ = (Rl_e.ms != Rl_o.ms)
                    lit = dict(closed=0, e=0, o=0, le=0, lo_=0, lq=[])
                    ss = np.random.SeedSequence([seed, n_o, lam.denominator, int(float(t0) * 1000), 0 if orc == "bottom" else 1, len(land)])
                    for child in ss.spawn(runs):
                        rng = np.random.default_rng(child)
                        run = r6lib.Run(P6, inst, r6lib.SimOracle(P6.xs, rng), rng, variant="2L+", abort_on_cost=False).run()
                        if run.status != "closed":
                            continue
                        lit["closed"] += 1
                        tj = [rec["passes"][-1]["t"] for rec in run.levels]
                        lit["e"] += (tj == Rl_e.ms)                  # the sample size of EVERY level as in the exact-rule mean run
                        lit["o"] += (tj == Rl_o.ms)
                        lit["le"] += (len(tj) - 1 == Rl_e.j_stop)        # the stopping level alone
                        lit["lo_"] += (len(tj) - 1 == Rl_o.j_stop)
                        lit["lq"].append(float(mp.log(run.queries())))
                    tot["cases"] += 1
                    tot["differ"] += differ
                    if differ:
                        tot["lit_runs"] += lit["closed"]
                        tot["side_exact"] += lit["e"]
                        tot["side_old"] += lit["o"]
                        tot["side_neither"] += lit["closed"] - lit["e"] - lit["o"]
                        if Rl_e.j_stop != Rl_o.j_stop:
                            tot["lvl_cases"] = tot.get("lvl_cases", 0) + 1
                            tot["lvl_runs"] = tot.get("lvl_runs", 0) + lit["closed"]
                            tot["lvl_exact"] = tot.get("lvl_exact", 0) + lit["le"]
                            tot["lvl_old"] = tot.get("lvl_old", 0) + lit["lo_"]
                        dl = abs(float(Rl_e.lcost - Rl_o.lcost))
                        if dl > 0.05:
                            tot["cost_cases"] = tot.get("cost_cases", 0) + 1
                            me = float(np.mean(lit["lq"]))
                            tot["cost_closer_exact"] = tot.get("cost_closer_exact", 0) + (abs(me - float(Rl_e.lcost)) < abs(me - float(Rl_o.lcost)))
                    print(f"     (B) {land:8s}: mean runs exact {float(Rl_e.lcost):.4f} (level {Rl_e.j_stop}, m {Rl_e.m_top}) / old {float(Rl_o.lcost):.4f} (level {Rl_o.j_stop}, m {Rl_o.m_top})"
                          f"{' -- DIFFERENT sample sizes' if differ else ' -- the same run'}; literal: {lit['closed']} of {runs} closed, every level's sample size as "
                          f"exact in {lit['e']}, as old in {lit['o']}; stopping level as exact in {lit['le']}, as old in {lit['lo_']}; mean ln(queries) {np.mean(lit['lq']):.4f}", flush=True)
    print(f"  (A) largest |ln cost(exact) - ln cost(old convention)|: {worstA:.3f}   (the message: 'ratio of costs up to e^{{4.2}} at a flat landscape')")
    print(f"  (B) consistent instances: {tot['cases']}; on {tot['differ']} of them the two mean runs differ; there, of {tot['lit_runs']} literal runs: "
          f"every level as the EXACT rule's mean run in {tot['side_exact']}, as the OLD convention's in {tot['side_old']}, as neither in {tot['side_neither']}")
    print(f"      where the two mean runs stop at different levels ({tot.get('lvl_cases', 0)} instances, {tot.get('lvl_runs', 0)} literal runs): the literal run stops at the "
          f"EXACT rule's level in {tot.get('lvl_exact', 0)}, at the OLD convention's in {tot.get('lvl_old', 0)}")
    print(f"      where the two mean-run costs differ by more than 0.05 in ln ({tot.get('cost_cases', 0)} instances): the mean literal ln(queries) is closer to the EXACT rule's "
          f"in {tot.get('cost_closer_exact', 0)}")


def part2(ncases, seed):
    print("PART 2: designs with lo < b or x0 - hi < b; THEIR reference: product instances of their family (place t0 in [lo, hi], c_in = t0 - u n_i) against the pair mode (t0_range = (lo, hi)) for the same law")
    rng = random.Random(seed)
    S = dict(designs=0, cases=0, c_depends=0, above=0, above_runs=0, runs=0, max_ex=0.0, ex=None, by={"bottom": [0, 0.0], "top": [0, 0.0]})
    while S["designs"] < ncases:
        u = rng.choice([0.5, 1.0, 2.0])
        n_i = rng.randint(2, 8)
        n_o = rng.randint(30, 90)
        n = n_o + n_i
        L1 = math.log(2 / (1 + math.exp(-u)))
        lo, hi = n_i * (u - L1), n_i * (2 * u - L1)
        x0 = 2 * u * n_i
        b = rng.randint(2, 12) / 4
        if not (b < x0 and (lo < b or x0 - hi < b)):
            continue
        mids = sorted({b + (x0 - b) * rng.randint(1, 15) / 16 for _ in range(rng.randint(0, 2))}, reverse=True)
        xs = [x0] + mids + [b]
        lam = rng.choice([0.2, 0.5, 1.0])
        theta = rng.choice([0.05, 0.5, 2.0])
        P = Params(n=n, n_o=n_o, u=u, lam=lam, eta=0.25, etap=0.1, theta=theta, nu1=1.0, b=b, delta=0.05, xs=tuple(xs))
        tabs = CubeTables(n_o, u)
        C = constants(P, tabs)
        lC = inner_costs(P, C)
        # a radial law: cone below a radius, flat above, generic offset inside the feasible range of c_in
        R = rng.randint(0, n_o)
        slope = rng.choice([0.0, 0.5, 1.0]) * u
        F = [slope * min(d, R) for d in range(n_o + 1)]
        lpr = (tabs.lbinom - n_o * math.log(2)).tolist()
        psi0 = F[rng.randint(0, n_o)]
        S["designs"] += 1
        for orc in ("bottom", "top"):
            S["cases"] += 1
            cs = set()
            hit = False
            for i in range(9):
                # a PRODUCT instance of their family: every fibre at the place t0, hence the inner offset c_in = t0 - u n_i,
                # law ln W = c_in - F(d), reference value psi0 = F(d0); the pair mode is evaluated for the SAME law
                t0 = lo + (hi - lo) * i / 8
                c_in = t0 - u * n_i
                lw = [c_in - f for f in F]
                cs.add(round(ORIG_RP(P, t0, orc)[2], 12))
                Rp = their_run(P, tabs, C, lC, lw, lpr, psi0, t0, orc)
                Rpair = their_run(P, tabs, C, lC, lw, lpr, psi0, t0, orc, t0_range=(lo, hi))
                if not (Rpair.status.startswith("closed") and Rp.status.startswith("closed")):
                    continue
                S["runs"] += 1
                ex = Rp.lcost - Rpair.lcost
                if ex > 1e-9:
                    S["above_runs"] += 1
                    hit = True
                    S["by"][orc][1] = max(S["by"][orc][1], ex)
                    if ex > S["max_ex"]:
                        S["max_ex"] = ex
                        S["ex"] = dict(u=u, n=n, n_o=n_o, n_i=n_i, lam=lam, eta=0.25, etap=0.1, theta=theta, nu1=1.0, b=b, xs=xs, cone_radius=R, cone_slope=slope,
                                       c_in=c_in, psi0=psi0, oracle=orc, lo=lo, hi=hi, place=t0, c_at_place=float(ORIG_RP(P, t0, orc)[2]),
                                       c_pair_mode=float(ORIG_RP(P, (lo, hi), orc)[2]), lcost_product_at_place=Rp.lcost, lcost_pair_mode=Rpair.lcost,
                                       lM_max_product=Rp.lM_max, lM_max_pair_mode=Rpair.lM_max, j_stop_product=Rp.j_stop, j_stop_pair_mode=Rpair.j_stop,
                                       lCmax=float(lC_max(P, C, lC)))
            S["c_depends"] += (len(cs) > 1)
            S["above"] += hit
            S["by"][orc][0] += hit
    print(f"  designs {S['designs']}; (design, law, behaviour) cases {S['cases']}; the shift depends on the place in {S['c_depends']} of them")
    print(f"  cases in which a PRODUCT instance (every fibre at one feasible place) costs more than the pair mode returns for its law: {S['above']} "
          f"(bottom {S['by']['bottom'][0]}, largest ln excess {S['by']['bottom'][1]:.3f}; top {S['by']['top'][0]}, largest {S['by']['top'][1]:.3f}); "
          f"{S['above_runs']} of {S['runs']} product runs")
    if S["ex"]:
        ex = S["ex"]
        print("  worst example (their reference):", json.dumps(ex))
        # the same example with my code: exact, from the same floats
        u, n, n_o, n_i = Fr(ex["u"]), ex["n"], ex["n_o"], ex["n_i"]
        P = Params(n=n, n_o=n_o, u=ex["u"], lam=ex["lam"], eta=0.25, etap=0.1, theta=ex["theta"], nu1=1.0, b=ex["b"], delta=0.05, xs=tuple(ex["xs"]))
        tabs = CubeTables(n_o, ex["u"])
        C = constants(P, tabs)
        lC = inner_costs(P, C)
        D = M.Design(n, n_o, u, Fr(ex["lam"]).limit_denominator(10), Fr(1, 4), 0.1, ex["theta"], 1.0, Fr(ex["b"]), 0.05, [Fr(x) for x in ex["xs"]],
                     lC=[None] + [float(x) for x in lC[1:]])
        pos = M.uniform_positions(D, ex["oracle"])
        F = [Fr(ex["cone_slope"]) * min(d, ex["cone_radius"]) for d in range(n_o + 1)]
        c_in = Fr(ex["c_in"])
        lo, hi = Fr(ex["lo"]), Fr(ex["hi"])
        at = [(c_in - F[d], D.cube.binom[d], Fr(ex["place"]), pos) for d in range(n_o + 1)]
        Rp = M.mean_run(D, at, 1 << n_o, Fr(ex["psi0"]), pop_tol=M.POP_TOL_THEIRS)
        A, B = [hi], [D.xs[0] - lo]
        for (a, be) in pos:
            A.append(min(A[-1], a)); B.append(min(B[-1], be))
        c_pair = M.shift_c(D, A, B)
        Rpair = M.mean_run(D, at, 1 << n_o, Fr(ex["psi0"]), union=(lo, hi), c_force=c_pair, pop_tol=M.POP_TOL_THEIRS)
        Rtrue = M.mean_run(D, at, 1 << n_o, Fr(ex["psi0"]), union=(lo, hi), pop_tol=M.POP_TOL_THEIRS)   # union of windows with the instance's own shift
        print(f"  the same with my code: product at the place: ln cost {float(Rp.lcost):.6f} (theirs {ex['lcost_product_at_place']:.6f}); "
              f"pair mode (shift {float(c_pair):.4f} from A0 = hi, B0 = x0 - lo): {float(Rpair.lcost):.6f} (theirs {ex['lcost_pair_mode']:.6f}); "
              f"shift of the fibres at that place {float(M.shift_c(D, *M.nested_positions(D, Fr(ex['place']), pos))):.4f}; "
              f"union of windows with THAT shift: {float(Rtrue.lcost):.6f}")
        out = HERE / "data_corner_example_their_reference.json"
        if not out.exists():
            out.write_text(json.dumps(ex, indent=1) + "\n")
            print("  example written to", out.name)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "part1"
    ncases = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 18
    t = time.time()
    print(f"r18_corner.py {mode} cases/runs={ncases} seed={seed} start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    if mode == "part1":
        part1(ncases, seed)
    else:
        part2(ncases, seed)
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
