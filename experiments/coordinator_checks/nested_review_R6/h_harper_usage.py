"""Harness remark of SCI-REV-0007: how often do harness tests XVI.3 and XVI.4 exercise the Harper step of
Algorithm 2L+ (the third term of the update of the running lower bound at a populated pass)?

The harness file is NOT modified.  Its text (argv[1]; in the repository ../../falsify_conjectures.py) is loaded with
two textual additions inside the function of the outer loop -- the record of a pass also stores the Markov-only value
of the running bound and the tail, and a module flag switches the Harper term off -- and the two tests are run exactly
as the harness runs them (seed 20261124, 60 trials in quick mode, 400 in full mode).  For every run of the outer loop
the script reports

  * populated passes at which the Harper term is the strict maximum of the three terms ("active");
  * runs that close at a populated pass which would fail the closure test with the Markov-only bound of that pass
    ("the Harper term decides the closure");
  * the reviewer's statistic: populated passes with closing radius r <= r_dagger at which condition [P] holds
    through Gamma'' only (Gamma~(r)/c_eta > theta >= Gamma''(r));
  * the same run repeated from the same generator state WITHOUT the Harper term (the mutation "XVI.3 M5"): does the
    trajectory change, and is a claim of Theorem 11.56 violated (the harness's own check of a run)?

Usage: python3 h_harper_usage.py <falsify_conjectures.py>          (40 s)
"""
import sys, os, math, types, time
import numpy as np
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


OLD1 = "                ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term\n"
NEW1 = ("                _markov, _harper = s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No\n"
        "                _ell_no = max(ell, _markov)\n"
        "                _act = _harper > _ell_no\n"
        "                ell = _ell_no if NO_HARPER else max(_ell_no, _harper)\n")
OLD2 = "            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg)\n"
NEW2 = ("            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg, tail=tail, ell_out=ell,\n"
        "                       ell_no=(_ell_no if pop else ell), harper_active=(_act if pop else False))\n")


def load_instrumented(src_path):
    """The harness text with the two additions, executed as a module of its own (the file itself is only read)."""
    text = open(src_path).read()
    assert text.count(OLD1) == 1 and text.count(OLD2) == 1, "the outer loop of the harness has changed: update OLD1/OLD2"
    text = text.replace(OLD1, NEW1).replace(OLD2, NEW2)
    m = types.ModuleType("harness_copy")
    m.__dict__["NO_HARPER"] = False
    sys.modules["harness_copy"] = m
    exec(compile(text, src_path, "exec"), m.__dict__)
    return m


mod = None
_orig = None
RUNS = []


def install(src_path):
    """Load the instrumented harness and put the recording wrapper in place of its outer loop."""
    global mod, _orig
    mod = load_instrumented(src_path)
    _orig = mod.ba_two_level_plus
    mod.ba_two_level_plus = wrapper
    return mod


def wrapper(rng, vals, probs, lnw_ref, n_o, n, u, par, mode, max_points=4_200_000):
    state = rng.bit_generator.state
    run = _orig(rng, vals, probs, lnw_ref, n_o, n, u, par, mode, max_points=max_points)
    rec = dict(n_o=n_o, n=n, u=u, par=dict(par), mode=mode, error=run.get("error"))
    if "error" not in run:
        C = run["C"]
        lam, eta, theta, b = par["lam"], par["eta"], par["theta"], par["b"]
        c_eta = (1 - eta) / (1 + eta)
        ball, E, Tk = C["ball"], C["E"], C["Tk"]
        cfrac = Fraction(1 - Fraction(eta)) / (1 + Fraction(eta))
        seq = run["levels"] + [run["last"]]
        pops = [lv for lv in seq if lv["pop"]]
        rec["populated"] = len(pops)
        rec["unpopulated"] = len(seq) - len(pops)
        rec["active"] = sum(1 for lv in pops if lv["harper_active"])
        last = run["last"]
        rec["closed_populated"] = bool(last["pop"])
        rec["decisive"] = bool(last["pop"] and last["tail"] <= theta * math.exp(b) * last["ell_out"]
                               and last["tail"] > theta * math.exp(b) * last["ell_no"])
        # the reviewer's statistic
        byG2 = 0
        for lv in pops:
            r = lv["r"]
            if 0 <= r <= C["rdag"]:
                g1 = (math.exp(u) - 1) if r == 0 else E[r] / ball[r]
                g2 = E[r] / Tk[mod.ba_kappa(ball, cfrac, r)]
                if g1 / c_eta > theta >= g2:
                    byG2 += 1
        rec["P_by_Gamma2"] = byG2
        rec["rdag"] = C["rdag"]
        # the mutant from the same state
        g2rng = np.random.Generator(np.random.PCG64())
        g2rng.bit_generator.state = state
        mod.NO_HARPER = True
        try:
            mrun = _orig(g2rng, vals, probs, lnw_ref, n_o, n, u, par, mode, max_points=max_points)
        finally:
            mod.NO_HARPER = False
        if "error" in mrun:
            rec["mutant"] = "error: " + mrun["error"]
            rec["mutant_differs"] = True
            rec["mutant_detected"] = not mrun["error"].startswith("sample beyond")
        else:
            mseq = mrun["levels"] + [mrun["last"]]
            same = len(mseq) == len(seq) and all(a["M"] == c["M"] and a["r"] == c["r"] and a["pop"] == c["pop"] for a, c in zip(seq, mseq)) \
                and mrun["lower"] == run["lower"] and mrun["upper"] == run["upper"]
            st = dict(runs=0, widest=0.0, tightest_count=0.0, populated=0, unpopulated=0, skipped=0)
            bad = mod.ba_check_run(mrun, vals, probs, n_o, n, u, par, st)
            rec["mutant_differs"] = not same
            rec["mutant_detected"] = bad is not None
            rec["mutant"] = bad["reason"] if bad else "no claim violated"
    RUNS.append(rec)
    return run


def report(tag, out):
    done = [r for r in RUNS if r["error"] is None]
    n = len(done)
    out(f"  {tag}: {len(RUNS)} runs of the outer loop, {n} completed")
    out(f"    populated passes {sum(r['populated'] for r in done)} (unpopulated level-ending passes {sum(r['unpopulated'] for r in done)})")
    out(f"    Harper term active (strict maximum) at {sum(r['active'] for r in done)} populated passes, in {sum(1 for r in done if r['active'] > 0)} of {n} runs")
    out(f"    runs that close at a populated pass: {sum(1 for r in done if r['closed_populated'])}; "
        f"of these, the Harper term decides the closure (fails with the Markov-only bound of that pass): {sum(1 for r in done if r['decisive'])}")
    out(f"    populated passes with r <= r_dagger at which [P] holds through Gamma'' only: {sum(r['P_by_Gamma2'] for r in done)}, in {sum(1 for r in done if r['P_by_Gamma2'] > 0)} of {n} runs")
    out(f"    the same runs without the Harper term: trajectory or bracket changes in {sum(1 for r in done if r['mutant_differs'])} of {n} runs; "
        f"a claim of Theorem 11.56 is violated in {sum(1 for r in done if r['mutant_detected'])} of {n}")
    kinds = {}
    for r in done:
        if r["mutant_detected"]:
            kinds[r["mutant"]] = kinds.get(r["mutant"], 0) + 1
    if kinds:
        out(f"      violated claims: {kinds}")
    cells = {}
    for r in done:
        key = (r["n_o"], r["u"])
        c = cells.setdefault(key, [0, 0, 0, 0])
        c[0] += 1; c[1] += r["active"] > 0; c[2] += r["decisive"]; c[3] += r["mutant_detected"]
    out("    per (n_o, u): runs / runs with the Harper term active / closure decided by it / mutant detected: " +
        "; ".join(f"({k[0]}, {k[1]:g}): {v[0]}/{v[1]}/{v[2]}/{v[3]}" for k, v in sorted(cells.items())))


def main():
    install(os.path.abspath(sys.argv[1]))
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    out("How often harness tests XVI.3, XVI.4 exercise the Harper step of Algorithm 2L+ (seed 20261124 as in the harness)")
    for name, fn in (("XVI.3", mod.t_two_level_plus), ("XVI.4", mod.t_two_level_plus_sample_sizes)):
        for mode, trials in (("quick", 60), ("full", 400)):
            RUNS.clear()
            t0 = time.time()
            ok, info = fn(np.random.default_rng(20261124), trials)
            out(f"{name}, {mode} mode ({trials} trials): test result {ok}   ({time.time() - t0:.0f} s)")
            report(f"{name} {mode}", out)
    open(outfile("h_harper_usage.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
