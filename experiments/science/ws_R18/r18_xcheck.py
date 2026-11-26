#!/usr/bin/env python3
"""R18: my mean run (r18_mean.py, exact) against THEIR Python reference (meanrun.mean_run, scratch copy), on
random designs and random product instances, for the two uniform behaviours, for explicit positions, for places
anywhere in [0, x_0] (corners included), for the old convention, and for the placement-free bound.

This is at once (a) a test of my code, (b) a replication of their reference from the statements, and (c) a
re-run of their reference on instances they did not choose.

Compared per case: status, stopping level, closing radius, numbers of populated / negligible levels, the sample
size of EVERY level, ln calls of every rung, ln cost, ln C_max, and the constants J, K, r_dagger, m_max.

usage: python3 -I -B r18_xcheck.py [cases] [seed]
"""
import math
import random
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "rerun_copy" / "src"))
sys.path.insert(0, str(HERE))

import numpy as np                                                            # noqa: E402
import mpmath as mp                                                           # noqa: E402

import r18_mean as mine                                                       # noqa: E402
from metricchain_eng.twolevel import meanrun as their                         # noqa: E402
from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs, lC_max   # noqa: E402
from metricchain_eng.twolevel.tables import CubeTables                        # noqa: E402

ORIG_RP = their.rung_positions
TOLP = mine.POP_TOL_THEIRS          # their tolerance in the test "populated" (None: N >= K exactly); see main()


def their_run(P, tabs, C, lC, F, c_in, psi0, t0, oracle, positions=None, legacy=False, t0_range=None):
    inst = their.Instance(their.radial_law(np.array(F, dtype=float), tabs, shift=c_in), psi0=psi0, t0=t0)
    kw = dict(C=C, lC=lC, record=True, positions=positions, legacy_classification=legacy)
    if t0_range is None:
        return their.mean_run(P, tabs, inst, oracle, **kw)
    their.rung_positions = lambda P_, t0_, oracle_="bottom", positions_=None, legacy_=False: ORIG_RP(P_, t0_range, oracle_, positions_, legacy_)
    try:
        return their.mean_run(P, tabs, inst, oracle, **kw)
    finally:
        their.rung_positions = ORIG_RP


def draw_design(rng):
    u = rng.choice([Fr(1, 2), Fr(1), Fr(2)])
    n = rng.choice([24, 40, 60, 100, 150, 240])
    n_o = rng.randint(max(2, n // 5), max(3, 4 * n // 5))
    n_i = n - n_o
    b = rng.choice([Fr(1, 4), Fr(1, 2), Fr(1), Fr(3)])
    theta = rng.choice([0.05, 0.1, 0.5, 2.0, 20.0])
    lam = rng.choice([Fr(1, 5), Fr(1, 4), Fr(1, 2), Fr(1)])
    eta = rng.choice([Fr(1, 20), Fr(1, 4), Fr(1, 2)])
    etap = rng.choice([0.05, 0.1, 0.5, 1.0])
    nu1 = rng.choice([1.0, max(1.0, 2 * math.exp(float(u)) * n_o / theta)])
    x0 = 2 * u * n_i
    rates = sorted({Fr(rng.randint(1, 4000), 2000) * u for _ in range(rng.randint(0, 10))}, reverse=True)
    last = b if rng.random() < 0.7 else b * Fr(rng.randint(1, 9), 10)          # x_L = b, or below it
    xs = [x0] + [r * n_i for r in rates if last < r * n_i < x0] + [last]
    if not (len(xs) >= 2 and all(xs[i] > xs[i + 1] for i in range(len(xs) - 1))):
        return None
    return dict(u=u, n=n, n_o=n_o, lam=lam, eta=eta, etap=etap, theta=theta, nu1=nu1, b=b, delta=0.05, xs=xs)


def draw_profile(rng, u, n_o):
    """F(0..n_o) as Fractions with |F(d+1) - F(d)| <= u (multiples of u/16, so that the float image is exact)."""
    kind = rng.randint(0, 5)
    g = u / 16
    if kind == 0:
        steps = [rng.randint(-16, 16) for _ in range(n_o)]
    elif kind == 1:
        steps = [rng.randint(0, 16) for _ in range(n_o)]
    elif kind == 2:
        R = rng.randint(0, n_o)
        steps = [0 if d < R else 16 for d in range(n_o)]                       # plateau, then cone
    elif kind == 3:
        R = rng.randint(0, n_o)
        steps = [16 if d < R else 0 for d in range(n_o)]                       # cone, then flat ("dip")
    elif kind == 4:
        steps = [0] * n_o                                                       # flat
    else:
        steps = [16] * n_o                                                      # cone
    F = [Fr(0)]
    for s in steps:
        F.append(F[-1] + s * g)
    return F


def compare(tag, Rm, Rt, D, P, C, lCmax_their, stats, verbose):
    bad = []
    if Rm.status != Rt.status:
        bad.append(f"status {Rm.status} / {Rt.status}")
    if Rm.j_stop != Rt.j_stop:
        bad.append(f"j_stop {Rm.j_stop} / {Rt.j_stop}")
    if Rm.status.startswith("closed") and Rt.status.startswith("closed"):
        if Rm.r_close != Rt.r_close:
            bad.append(f"r_close {Rm.r_close} / {Rt.r_close}")
        if (Rm.npop, Rm.nneg) != (Rt.npop, Rt.nneg):
            bad.append(f"npop,nneg {(Rm.npop, Rm.nneg)} / {(Rt.npop, Rt.nneg)}")
    if Rm.j_stop == Rt.j_stop:
        lM_m = np.array([math.log(D.K) + mm * math.log(2) for mm in Rm.ms])
        if lM_m.shape != Rt.lM.shape or np.max(np.abs(lM_m - Rt.lM)) > 1e-9:
            j_bad = int(np.argmax(np.abs(lM_m - Rt.lM))) if lM_m.shape == Rt.lM.shape else -1
            bad.append(f"sample sizes differ (first at level {j_bad})")
        for l in range(1, D.L + 1):
            a, t = Rm.lcalls[l], float(Rt.lcalls[l])
            if (a == -mp.inf) != (t == -math.inf) or (a != -mp.inf and abs(float(a) - t) > 1e-8 * max(1.0, abs(t))):
                bad.append(f"ln calls of rung {l}: {mp.nstr(a, 14)} / {t!r}")
        if abs(float(Rm.lcost) - Rt.lcost) > 1e-8 * max(1.0, abs(Rt.lcost)):
            bad.append(f"ln cost {mp.nstr(Rm.lcost, 14)} / {Rt.lcost!r}")
    if abs(float(D.lCmax) - lCmax_their) > 1e-8 * max(1.0, abs(lCmax_their)):
        bad.append(f"ln C_max {mp.nstr(D.lCmax, 14)} / {lCmax_their!r}")
    stats["runs"] += 1
    stats["levels"] += Rt.j_stop + 1
    stats["closed"] += Rt.status.startswith("closed")
    if bad:
        stats["bad"] += 1
        if verbose:
            print("  MISMATCH", tag, "; ".join(bad), flush=True)
    return not bad


def main():
    global TOLP
    ncases = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if len(sys.argv) > 3 and sys.argv[3] == "exact":
        TOLP = None
    print("populated test of my run:", "N >= K exactly" if TOLP is None else "their tolerance, 2^m P(HIGH) >= 2^(-1e-12)")
    rng = random.Random(seed)
    t_start = time.time()
    print(f"r18_xcheck.py cases={ncases} seed={seed} start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    stats = {k: dict(runs=0, bad=0, levels=0, closed=0) for k in
             ("bottom", "top", "positions", "corner place", "old convention in range", "union bound in range")}
    const_bad = 0
    done = 0
    tolst = dict(runs=0, runs_changed=0, levels_changed=0, max_dlcost=0.0, max_dlcalls=0.0, n_o_min_changed=10 ** 9, n_o_max_unchanged=0)
    ctrl = dict(old_convention_in_corner=0, old_convention_in_corner_differs=0, union_swapped=0, union_swapped_below_instance=0,
                union_runs=0, union_below_instance=0)
    while done < ncases:
        dd = draw_design(rng)
        if dd is None:
            continue
        u, n, n_o = dd["u"], dd["n"], dd["n_o"]
        n_i = n - n_o
        xs = dd["xs"]
        P = Params(n=n, n_o=n_o, u=float(u), lam=float(dd["lam"]), eta=float(dd["eta"]), etap=dd["etap"], theta=dd["theta"],
                   nu1=dd["nu1"], b=float(dd["b"]), delta=dd["delta"], xs=tuple(float(x) for x in xs))
        tabs = CubeTables(n_o, float(u))
        C = constants(P, tabs)
        lC = inner_costs(P, C)
        lCmax_t = lC_max(P, C, lC)
        D = mine.Design(n, n_o, u, dd["lam"], dd["eta"], dd["etap"], dd["theta"], dd["nu1"], dd["b"], dd["delta"], xs,
                        lC=[None] + [float(x) for x in lC[1:]])
        if (D.J, D.K, D.r_dag, D.m_max) != (C.J, C.K, C.r_dag, C.m_max):
            const_bad += 1
            print("  CONSTANTS differ", (D.J, D.K, D.r_dag, D.m_max), (C.J, C.K, C.r_dag, C.m_max), flush=True)
        Lam1 = math.log(2 / (1 + math.exp(-float(u))))
        lo_f, hi_f = n_i * (float(u) - Lam1), n_i * (2 * float(u) - Lam1)
        for _ in range(2):
            F = draw_profile(rng, u, n_o)
            d0 = rng.randint(0, n_o)
            psi0 = F[d0]
            # the place: inside the feasible range of a u-Lipschitz fibre (c_in a multiple of 1/64), or anywhere in [0, x0]
            c_in = Fr(rng.randint(math.ceil(-n_i * Lam1 * 64), math.floor(n_i * (float(u) - Lam1) * 64)), 64)
            t0 = u * n_i + c_in
            Ff = [float(x) for x in F]
            # (1) the two uniform behaviours at a feasible place
            for orc in ("bottom", "top"):
                pos = mine.uniform_positions(D, orc)
                atoms, den = mine.radial_atoms(D, F, c_in, pos=pos)
                Rm = mine.mean_run(D, atoms, den, psi0, pop_tol=TOLP)
                Rt = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0), orc)
                compare(f"{orc} n={n} n_o={n_o} u={u}", Rm, Rt, D, P, C, lCmax_t, stats[orc], True)
                # how much does the tolerance of their test "populated" change the mean run?  (my run with N >= K exactly)
                Rx = mine.mean_run(D, atoms, den, psi0, pop_tol=None)
                tolst["runs"] += 1
                if Rx.ms != Rm.ms or Rx.j_stop != Rm.j_stop:
                    tolst["runs_changed"] += 1
                    tolst["levels_changed"] += sum(a != b_ for a, b_ in zip(Rx.ms, Rm.ms)) if Rx.j_stop == Rm.j_stop else -10 ** 9
                    tolst["max_dlcost"] = max(tolst["max_dlcost"], abs(float(Rx.lcost - Rm.lcost)))
                    for l in range(1, D.L + 1):
                        if Rx.calls_num[l] and Rm.calls_num[l]:
                            tolst["max_dlcalls"] = max(tolst["max_dlcalls"], abs(float(Rx.lcalls[l] - Rm.lcalls[l])))
                    tolst["n_o_min_changed"] = min(tolst["n_o_min_changed"], n_o)
                else:
                    tolst["n_o_max_unchanged"] = max(tolst["n_o_max_unchanged"], n_o)
                # (5) the old convention inside its range: must give the same run as the exact rule iff the two shifts agree
                A, B = mine.nested_positions(D, t0, pos)
                c_exact = mine.shift_c(D, A, B)
                c_old = D.b if orc == "bottom" else Fr(0)
                Rt_old = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0), orc, legacy=True)
                Rm_old = mine.mean_run(D, atoms, den, psi0, c_force=c_old, pop_tol=TOLP)
                compare(f"old convention {orc} n={n}", Rm_old, Rt_old, D, P, C, lCmax_t, stats["old convention in range"], True)
                # (6) the placement-free bound, their pair mode against my union of windows (classification untouched)
                c_lo = mine.shift_c(D, *mine.nested_positions(D, Fr(lo_f), pos))
                c_hi = mine.shift_c(D, *mine.nested_positions(D, Fr(hi_f), pos))
                if c_lo == c_hi == c_exact:                          # the shift does not depend on the place: §4 applies
                    Rt_u = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0), orc, t0_range=(lo_f, hi_f))
                    Rm_u = mine.mean_run(D, atoms, den, psi0, union=(Fr(lo_f), Fr(hi_f)), pop_tol=TOLP)
                    compare(f"union {orc} n={n}", Rm_u, Rt_u, D, P, C, lCmax_t, stats["union bound in range"], True)
                    ctrl["union_runs"] += 1
                    ctrl["union_below_instance"] += any(Rm_u.calls_num[l] < Rm.calls_num[l] for l in range(1, D.L + 1))
                    # control: lo and hi exchanged (A_0 = lo, B_0 = x_0 - hi): the intersection instead of the union
                    Rm_s = mine.mean_run(D, atoms, den, psi0, union=(Fr(hi_f), Fr(lo_f)), pop_tol=TOLP)
                    ctrl["union_swapped"] += 1
                    ctrl["union_swapped_below_instance"] += any(Rm_s.calls_num[l] < Rm.calls_num[l] for l in range(1, D.L + 1))
            # (2) explicit positions: a share t of every rung, and independent random admissible pairs
            t_share = Fr(rng.randint(0, 16), 16)
            pos = mine.uniform_positions(D, t_share)
            if rng.random() < 0.5:
                pos = []
                for x in xs[1:]:
                    a = x * Fr(rng.randint(0, 16), 16)
                    pos.append((a, (x - a) * Fr(rng.randint(0, 16), 16)))
            atoms, den = mine.radial_atoms(D, F, c_in, pos=pos)
            Rm = mine.mean_run(D, atoms, den, psi0, pop_tol=TOLP)
            Rt = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0), "bottom",
                           positions=([float(a) for a, _ in pos], [float(be) for _, be in pos]))
            compare(f"positions n={n} n_o={n_o}", Rm, Rt, D, P, C, lCmax_t, stats["positions"], True)
            # (3) a place in a corner of [0, x0] (not reachable by a Lipschitz fibre in general; their Instance accepts it)
            bq = D.b
            x0 = xs[0]
            t0c = rng.choice([Fr(0), bq / 4, bq / 2, bq * Fr(3, 4), x0 - bq / 4, x0 - bq / 2, x0])
            for orc in ("bottom", "top"):
                pos = mine.uniform_positions(D, orc)
                atoms, den = mine.radial_atoms(D, F, c_in, t0=t0c, pos=pos)
                Rm = mine.mean_run(D, atoms, den, psi0, pop_tol=TOLP)
                Rt = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0c), orc)
                compare(f"corner {orc} t0={t0c} n={n}", Rm, Rt, D, P, C, lCmax_t, stats["corner place"], True)
                # control: the old convention in the corner must NOT reproduce the exact run whenever the shifts differ
                A, B = mine.nested_positions(D, t0c, pos)
                c_exact = mine.shift_c(D, A, B)
                c_old = D.b if orc == "bottom" else Fr(0)
                if c_exact != c_old:
                    Rt_old = their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0c), orc, legacy=True)
                    ctrl["old_convention_in_corner"] += 1
                    ctrl["old_convention_in_corner_differs"] += (Rt_old.j_stop != Rt.j_stop or abs(Rt_old.lcost - Rt.lcost) > 1e-9
                                                                  or not np.array_equal(Rt_old.lM, Rt.lM))
        done += 1
        if done % 10 == 0:
            print(f"  {done} designs, {time.time() - t_start:.0f} s", flush=True)
    print("\nMY MEAN RUN AGAINST THEIR PYTHON REFERENCE (mismatches must be 0)")
    for k, s in stats.items():
        print(f"  {k:26s} runs {s['runs']:5d}  closed {s['closed']:5d}  levels compared {s['levels']:9d}  mismatches {s['bad']}")
    print(f"  designs with different constants (J, K, r_dagger, m_max): {const_bad} of {done}")
    print("CONTROLS")
    print(f"  old convention at a corner place where the exact shift differs: {ctrl['old_convention_in_corner']} runs of their reference, "
          f"of which the run changes (level, sample sizes or cost): {ctrl['old_convention_in_corner_differs']}")
    print(f"  union bound (A0 = hi, B0 = x0 - lo): {ctrl['union_runs']} runs; calls of some rung BELOW the product instance's: {ctrl['union_below_instance']} (must be 0)")
    print(f"  lo and hi exchanged (A0 = lo, B0 = x0 - hi): {ctrl['union_swapped']} runs; calls of some rung below the product instance's: "
          f"{ctrl['union_swapped_below_instance']} (must be > 0)")
    print(f"THE TOLERANCE OF THEIR TEST 'populated' (2^m P(HIGH) >= 2^(-1e-12) instead of N >= K): my run with and without it, {tolst['runs']} runs "
          f"(bottom/top, feasible place): sample sizes change in {tolst['runs_changed']} runs, at {tolst['levels_changed']} levels in all; "
          f"largest |change of ln cost| {tolst['max_dlcost']:.3e}; largest |change of ln calls of a rung| {tolst['max_dlcalls']:.3e}; "
          f"smallest n_o with a change {tolst['n_o_min_changed']}, largest n_o without {tolst['n_o_max_unchanged']}")
    tot_bad = sum(s["bad"] for s in stats.values()) + const_bad
    print(f"VERDICT: {'AGREEMENT on every compared quantity' if tot_bad == 0 else 'MISMATCHES: ' + str(tot_bad)}")
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t_start:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")


if __name__ == "__main__":
    main()
