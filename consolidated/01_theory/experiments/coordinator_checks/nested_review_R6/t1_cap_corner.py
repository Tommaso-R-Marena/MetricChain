"""R6-T1: the remark "the sample-size cap can be lowered" after Theorem 11.56 -- the pass with M = M_ddag exactly.

Part A (exact tables, no randomness).  For a grid of (n_o, u, lambda, eta, theta, nu_0) the script computes r_dagger,
Delta = ceil(lambda/u) and the factor  F* = max{c_eta |B(n_o, r_dagger)|, T_{n_o}(kappa(r_dagger + 1))}  (after a populated
level that was left, the running bound satisfies  ell >= s_{j-1} e^{-b} 2^{-n_o} F*  -- for r_dagger = -1 the first entry is
c_eta/2), and checks the deterministic inequalities of the proof:
   (A1)  E_{r-1} <= e^{-u} E_r  and  E_1 >= (n_o + 2) E_0;
   (A2)  main branch, r_dagger >= Delta:  e^lambda E_r <= theta F*  for every r <= r_dagger - Delta  (so every
         unpopulated pass with M >= M_ddag, equality included, passes the closure test);
   (A3)  the corner of the review, 1 <= r_dagger < Delta, the pass with 2^{n_o} q = 1 (r = 0):
         e^lambda E_0 < E_{r_dagger} <= theta F*  whenever lambda <= 1  (more precisely e^lambda < n_o + 2);
   (A4)  r_dagger in {0, -1}:  M_dag >= M_ddag (so the cap is 2 e^lambda M_dag > 2 M_ddag), and the inequality
         e^lambda E_0 <= theta F* can FAIL: the pass with M = M_ddag need not close;
   (A5)  that lambda <= 1 is not decorative: with lambda > ln(n_o + 2) (outside the theorem) (A3) fails in some cells.

Part B (runs).  The outer loop of Algorithm 2L+ as implemented in the harness (function ba_two_level_plus of
experiments/falsify_conjectures.py, loaded from a copy; one line added that logs every pass), eta = 1/2 (the only
value for which M_ddag = K 2^{n_o}/(1 - eta) lies in the doubling sequence), small cubes, random radial landscapes:
how often does an unpopulated pass with M = M_ddag exactly occur, does it close, and how large do samples get.

Usage: python3 t1_cap_corner.py <falsify_conjectures.py> [runs=4500]          (20 s; in the repository the argument
       is ../../falsify_conjectures.py -- the file is only read)
"""
import sys, os, math, types, time, itertools
from fractions import Fraction
import numpy as np
import mpmath as mp
from r6lib_coord import Tab, rdagger, frac, outfile

src_path = os.path.abspath(sys.argv[1])
NRUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 4500
lines = []
def out(s=""):
    print(s); lines.append(s); sys.stdout.flush()


# ------------------------------------------------------------------------------------------------ Part A
def part_a():
    out("Part A: exact tables")
    cnt = dict(cells=0, A1=0, main=0, main_pairs=0, corner=0, corner_strict=0, low=0, low_can_fail=0, lam_big_fail=0, lam_big=0)
    ok = True
    worst_main, worst_corner = mp.mpf(0), mp.mpf(0)
    for n_o in (2, 3, 4, 5, 6, 8, 10, 12, 16, 24, 40, 80):
        for u in (0.1, 0.25, 0.5, 1.0, 2.0, 3.0):
            tab = Tab(n_o, u)
            eu = mp.exp(mp.mpf(u))
            for r in range(1, n_o + 1):
                cnt["A1"] += 1
                # E_r = e^u E_{r-1} + (e^u - 1)|B(r)|; at 60 digits the last term can be below the rounding of E_r
                if not (tab.E[r - 1] * eu <= tab.E[r] * (1 + mp.mpf(10) ** -50)):
                    ok = False; cnt["A1bad"] = cnt.get("A1bad", 0) + 1; out(f"   (A1) fails: n_o={n_o}, u={u}, r={r}")
            cnt["A1tabs"] = cnt.get("A1tabs", 0) + 1
            if not (tab.E[1] >= (n_o + 2) * tab.E[0]):
                ok = False; cnt["A1bad"] = cnt.get("A1bad", 0) + 1; out(f"   (A1') fails: n_o={n_o}, u={u}")
            for eta in (0.5, 0.25, 0.1):
                eta_f = frac(eta)
                c_eta = (1 - eta_f) / (1 + eta_f)
                for theta in (0.01, 0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 20.0, 200.0):
                    for nu0 in (2.0, 20.0, 500.0, 1e5):
                        rd = rdagger(tab, eta, theta, mp.mpf(nu0))
                        first = (mp.mpf(c_eta.numerator) / c_eta.denominator) * (tab.ball[rd] if rd >= 0 else mp.mpf(1) / 2)
                        Fstar = max(first, tab.T[tab.kappa(rd + 1, c_eta)])
                        for lam in (0.1, 0.25, 0.5, 1.0):
                            cnt["cells"] += 1
                            Delta = math.ceil(lam / u - 1e-12)
                            el = mp.exp(mp.mpf(lam))
                            if rd >= Delta:                              # (A2)
                                cnt["main"] += 1
                                for r in range(0, rd - Delta + 1):
                                    cnt["main_pairs"] += 1
                                    ratio = el * tab.E[r] / (mp.mpf(theta) * Fstar)
                                    worst_main = max(worst_main, ratio)
                                    if ratio > 1:
                                        ok = False; out(f"   (A2) fails: n_o={n_o}, u={u}, eta={eta}, theta={theta}, nu0={nu0}, lam={lam}, r_dag={rd}, r={r}")
                            elif rd >= 1:                                # (A3): the corner of the review
                                cnt["corner"] += 1
                                a = el * tab.E[0] < tab.E[rd]
                                bq = tab.E[rd] <= mp.mpf(theta) * Fstar
                                worst_corner = max(worst_corner, el * tab.E[0] / (mp.mpf(theta) * Fstar))
                                cnt["corner_strict"] += bool(a and bq)
                                if not (a and bq):
                                    ok = False; out(f"   (A3) fails: n_o={n_o}, u={u}, eta={eta}, theta={theta}, nu0={nu0}, lam={lam}, r_dag={rd}")
                            else:                                        # (A4): r_dagger in {0, -1}
                                cnt["low"] += 1
                                pidag = mp.mpf(tab.ball[rd]) / 2 ** n_o if rd >= 0 else mp.mpf(1) / 2 ** (n_o + 1)
                                Mdag_over_K = 1 / ((1 - mp.mpf(eta)) * pidag)
                                Mdd_over_K = mp.mpf(2) ** n_o / (1 - mp.mpf(eta))
                                if not (Mdag_over_K >= Mdd_over_K):
                                    ok = False; out(f"   (A4) M_dag < M_ddag: n_o={n_o}, u={u}, r_dag={rd}")
                                cnt["low_can_fail"] += bool(el * tab.E[0] > mp.mpf(theta) * Fstar)
                        for lam in (1.5, 2.0, 3.0, 5.0):               # (A5) outside the theorem: lambda > 1
                            Delta = math.ceil(lam / u - 1e-12)
                            if 1 <= rd < Delta:
                                cnt["lam_big"] += 1
                                cnt["lam_big_fail"] += bool(mp.exp(mp.mpf(lam)) * tab.E[0] > mp.mpf(theta) * Fstar)
    out(f"  (A1) E_(r-1) <= e^-u E_r in {cnt['A1']} cases and E_1 >= (n_o + 2) E_0 in {cnt['A1tabs']} tables: {cnt.get('A1bad', 0)} violations")
    out(f"  cells (n_o, u, eta, theta, nu_0, lambda <= 1): {cnt['cells']}")
    out(f"  (A2) main branch r_dagger >= Delta: {cnt['main']} cells, {cnt['main_pairs']} radii r <= r_dagger - Delta; largest e^lambda E_r/(theta F*) = {float(worst_main):.4f} (<= 1)")
    out(f"  (A3) corner 1 <= r_dagger < Delta: {cnt['corner']} cells; e^lambda E_0 < E_(r_dagger) <= theta F* in {cnt['corner_strict']} of them; largest e^lambda E_0/(theta F*) = {float(worst_corner):.4f}")
    out(f"  (A4) r_dagger in {{0, -1}}: {cnt['low']} cells; M_dag >= M_ddag in all; e^lambda E_0 > theta F* (the pass with M = M_ddag need not close) in {cnt['low_can_fail']} of them")
    out(f"  (A5) lambda in {{1.5, 2, 3, 5}} (outside the theorem), 1 <= r_dagger < Delta: {cnt['lam_big']} cells; e^lambda E_0 > theta F* in {cnt['lam_big_fail']} of them")
    out(f"  Part A passed: {ok}")
    return ok


# ------------------------------------------------------------------------------------------------ Part B
def part_b():
    text = open(src_path).read()
    OLD = "            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg)\n"
    NEW = OLD + "            PASS_LOG.append(dict(j=j, M=M, N=N, pop=pop, r=r, tail=tail, closes=(tail <= theta * math.exp(b) * ell), Mneg=Mneg))\n"
    assert text.count(OLD) == 1
    mod = types.ModuleType("harness_copy_t1")
    mod.__dict__["PASS_LOG"] = []
    sys.modules["harness_copy_t1"] = mod
    exec(compile(text.replace(OLD, NEW), src_path, "exec"), mod.__dict__)
    rng = np.random.default_rng(20261126)
    st = dict(runs=0, skipped=0, corner_runs=0, corner_passes=0, corner_closed=0, corner_open=0, exact_2Mdd=0, above_2Mdd=0, cap_reached=0,
              largest_over_cap=0.0)
    by = {"r_dag >= Delta": [0, 0, 0, 0], "1 <= r_dag < Delta": [0, 0, 0, 0], "r_dag in {0,-1}": [0, 0, 0, 0]}   # runs, corner passes, closed, not closed
    t0 = time.time()
    for it in range(NRUNS):
        n_o = int(rng.integers(3, 10))
        u = float(rng.choice([0.2, 0.3, 0.5, 1.0, 2.0]))
        lam = float(rng.choice([0.5, 1.0]))
        par = dict(lam=lam, eta=0.5, etap=float(rng.choice([0.5, 1.0])), theta=float(rng.choice([0.02, 0.1, 0.5, 2.0, 10.0])),
                   b=float(rng.choice([0.25, 0.5, 1.0])), delta=0.05, nu1=float(rng.choice([1.0, 4.0, 30.0])))
        kind = int(rng.integers(5))
        d = np.arange(n_o + 1, dtype=float)
        if kind == 0:
            f = np.zeros(n_o + 1)
        elif kind == 1:
            f = u * d
        elif kind == 2:
            f = u * float(rng.uniform(0.2, 1.0)) * np.maximum(d - int(rng.integers(0, n_o)), 0.0)
        elif kind == 3:
            f = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])
        else:
            f = -u * float(rng.uniform(0.2, 1.0)) * np.minimum(d, int(rng.integers(1, n_o + 1)))     # a dip around the centre
        vals = np.exp(-f)
        probs = np.array([math.comb(n_o, k) for k in range(n_o + 1)], dtype=float) / 2 ** n_o
        lnw_ref = -float(f[int(rng.integers(0, n_o + 1))])
        mod.PASS_LOG.clear()
        run = mod.ba_two_level_plus(rng, vals, probs, lnw_ref, n_o, n_o + 2, u, par, int(rng.integers(3)), max_points=6_000_000)
        if "error" in run:
            st["skipped"] += 1
            continue
        C = run["C"]
        K, rd = C["K"], C["rdag"]
        Delta = math.ceil(lam / u - 1e-12)
        Mdd = K * 2 ** (n_o + 1) if rd < Delta else K / (0.5 * (C["ball"][rd - Delta + 1] / 2 ** n_o))
        cap = 2 * max(math.exp(lam) * C["Mdag"], Mdd)
        key = "r_dag >= Delta" if rd >= Delta else ("1 <= r_dag < Delta" if rd >= 1 else "r_dag in {0,-1}")
        by[key][0] += 1
        st["runs"] += 1
        Mmax = max(p["M"] for p in mod.PASS_LOG)
        if rd < Delta:
            corner = [p for p in mod.PASS_LOG if (not p["pop"]) and p["M"] == Mdd]
            st["corner_runs"] += bool(corner)
            for p in corner:
                st["corner_passes"] += 1
                by[key][1] += 1
                by[key][2 if p["closes"] else 3] += 1
                st["corner_closed" if p["closes"] else "corner_open"] += 1
            st["exact_2Mdd"] += (Mmax == 2 * Mdd)
            st["above_2Mdd"] += (Mmax > 2 * Mdd)
        big = [p["M"] for p in mod.PASS_LOG if p["M"] > K]
        if big:
            st["largest_over_cap"] = max(st["largest_over_cap"], max(big) / cap)
            st["cap_reached"] += (max(big) >= cap)
    out(f"Part B: {NRUNS} runs of the harness's outer loop with eta = 1/2 on Q_3 ... Q_9 ({st['skipped']} skipped: sample beyond the cap of the test)   ({time.time() - t0:.0f} s)")
    out(f"  completed {st['runs']}; by branch (runs, unpopulated passes with M = M_ddag exactly, closed, not closed): {by}")
    out(f"  runs with r_dagger < Delta in which the largest sample is exactly 2 M_ddag: {st['exact_2Mdd']}; larger than 2 M_ddag: {st['above_2Mdd']}")
    out(f"  samples (other than K) at or above the cap 2 max(e^lambda M_dag, M_ddag): {st['cap_reached']} runs; largest sample/cap = {st['largest_over_cap']:.3f}")
    ok = st["cap_reached"] == 0 and st["above_2Mdd"] == 0 and by["1 <= r_dag < Delta"][3] == 0
    out(f"  Part B as predicted (cap never reached; no sample above 2 M_ddag when r_dagger < Delta; the corner pass always closes for r_dagger >= 1): {ok}")
    return ok


ok = part_a()
ok = part_b() and ok
out(f"all checks passed: {ok}")
open(outfile("t1_cap_corner.txt"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
