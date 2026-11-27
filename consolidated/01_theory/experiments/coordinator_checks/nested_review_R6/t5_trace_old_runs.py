"""R6-T5 (i): which draws of the published run of experiments/workstreams/K/sim_grouped.py went through numpy's
binomial in the regime where that sampler is wrong.

The script re-runs the published suite UNCHANGED (same code, same seeds 31 and 32) with the FIRST version of the
sampler (argv[1]: the directory that holds it -- first_version/ here) and the workstream's other files (argv[2]:
experiments/workstreams/K); the random generator is wrapped in a proxy that passes every call through and records
the calls of `binomial` with a count of at least 10^14.  Before every run the state of the generator and the
arguments of the run are saved (t5_saved_runs.pkl, 9 MB, not stored in the repository), so that t5_rerun_new.py
can repeat each run from the same state with the corrected sampler.  Its first 19 lines of output must be the
published out_sim_grouped.txt of the first version (first_version/out_sim_grouped.txt) up to the timings.

Regimes recorded (n = count of the node, mean = n p; BTPE is numpy's branch for mean > 30):
    A   n >= 2^53 (9.0e15),  42 < mean <= 1e4     the regime of the review: bias of the mean up to 0.8 %, variance up to 8 %
    B   n >= 2^53,           1e4 < mean <= 1e6    mean shift below one count, variance wrong by up to about 1 %
    C   1e15 <= n < 2^53,    42 < mean <= 1e6     our scan: distortion measurable from n = 1e15 on (either sign)
    D   n >= 1e15,           mean > 1e6           relative errors below 1e-3 (variance) and 1e-6 (mean): harmless
Usage:  python3 t5_trace_old_runs.py <dir with the first version of stable_multinomial.py> <dir with klib.py, sim_outer_loop.py, sim_grouped.py>
        (in the repository:  python3 -B t5_trace_old_runs.py first_version ../../workstreams/K ;  five minutes)
        python3 t5_trace_old_runs.py <...> <...> summary       only the summary, from the saved trace
"""
import sys, os, math, time, pickle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


firstdir, src = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
sys.path.insert(0, src)
sys.path.insert(0, firstdir)                                 # the first-version sampler is found first
import stable_multinomial as SM_FIRST                       # noqa: E402
assert not hasattr(SM_FIRST, "binomial_exact"), "this is not the first version of the sampler"
import sim_grouped as SG                                    # noqa: E402  (the workstream's file, unchanged)
assert SG.StableMultinomial is SM_FIRST.StableMultinomial

TRACE = []                                                   # (suite, run index, n, p)
CUR = dict(suite="main", run=-1)


class LoggingRng:
    """Passes everything to the generator; records binomial(n, p) calls with n >= 1e14."""
    def __init__(self, g):
        self._g = g

    def __getattr__(self, name):
        return getattr(self._g, name)

    def binomial(self, n, p, size=None):
        na, pa = np.atleast_1d(np.asarray(n)), np.atleast_1d(np.asarray(p, dtype=float))
        big = na >= 10 ** 14
        if big.any():
            for nn, pp in zip(na[big].tolist(), pa[big].tolist()):
                TRACE.append((CUR["suite"], CUR["run"], int(nn), float(pp)))
        return self._g.binomial(n, p, size)


SAVED = []                                                   # one record per run: state before the run, arguments, old outcome
_orig_run, _orig_check = SG.run_grouped, SG.check_grouped


def run_wrapper(rng, vals, probs, psi0, P, mode, max_log2=62, mut=()):
    CUR["run"] += 1
    rec = dict(suite=CUR["suite"], run=CUR["run"], state=rng.bit_generator.state, vals=np.array(vals), probs=np.array(probs),
               psi0=psi0, mode=mode, mut=tuple(mut),
               P=dict(n=P.n, n_o=P.n_o, u=P.u, lam=P.lam, eta=P.eta, etap=P.etap, theta=P.theta, b=P.b, ladder=list(P.x[1:]), delta=P.delta),
               K=P.K, rdag=P.rdag, Mdag=P.Mdag)
    run = _orig_run(rng, vals, probs, psi0, P, mode, max_log2=max_log2, mut=mut)
    if "error" in run:
        rec["old"] = dict(error=run["error"])
    else:
        seq = run["levels"] + [run["last"]]
        rec["old"] = dict(maxM=max(lv["M"] for lv in seq), npop=sum(1 for lv in run["levels"] if lv["populated"]),
                          nneg=sum(1 for lv in run["levels"] if not lv["populated"]), last_r=run["last"]["r"],
                          last_pop=run["last"]["populated"], lower=run["lower"], upper=run["upper"], nblocks=len(run["counts"]),
                          largest_block=int(max(int(c.sum()) for c in run["counts"])))
    SAVED.append(rec)
    return run


def check_wrapper(run, vals, probs, P, stats):
    g0, b0 = stats["good"], stats["bad_event"]
    fails = _orig_check(run, vals, probs, P, stats)
    SAVED[-1]["old"]["good"] = (stats["good"] - g0 == 1)
    SAVED[-1]["old"]["fails"] = [f[0] for f in fails]
    return fails


SG.run_grouped, SG.check_grouped = run_wrapper, check_wrapper


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    t0 = time.time()
    cases = [(0.5, 300), (0.5, 400), (0.5, 600), (1.0, 100), (1.0, 150), (1.0, 200), (2.0, 36), (2.0, 48), (2.0, 60)]
    out("Outer loop of Algorithm 2L+ at medium size, grouped exact sample, bounded regime nu_1 = 2 e^u n_o/theta")
    out("[first-version sampler; the published run repeated with a recording generator]")
    stats, allfails = SG.suite(LoggingRng(np.random.default_rng(31)), cases, 20, out)
    out(f"  stats: {stats}")
    out(f"  failures: {len(allfails)}" + ("" if not allfails else f"   first: {allfails[:3]}"))
    ok = len(allfails) == 0 and stats["negligible"] > 0 and stats["runs_with_negligible_levels"] > 0
    out(f"medium-size suite passed (no failure; levels are left as negligible in the bounded regime): {ok}   ({time.time() - t0:.0f} s)")
    out("")
    out("Power of the test at this size (mutated algorithm, same checks, 3 repetitions per case and profile):")
    expected = {"noharper": "C4 closure radius", "maxform": "C2 width", "neg_tol": "C6 count lemma", "q_plain": "C3 q < p(s)"}
    for mname, exp_check in expected.items():
        CUR["suite"], CUR["run"] = mname, -1
        st, fl = SG.suite(LoggingRng(np.random.default_rng(32)), cases, 3, out, mut=(mname,), verbose=False)
        kinds = SG.fail_kinds(fl)
        det = kinds.get(exp_check, 0) > 0
        out(f"  mutation {mname:9s}: {len(fl):3d} of {st['runs']:3d} runs fail; kinds {kinds};  expected check '{exp_check}' fires: {det}")
        ok = ok and det
    out(f"all mutations detected and unmutated suite clean: {ok}   ({time.time() - t0:.0f} s)")
    open(outfile("t5_old_sim_grouped.txt"), "w").write("\n".join(lines) + "\n")
    pickle.dump(SAVED, open(outfile("t5_saved_runs.pkl"), "wb"))
    pickle.dump(TRACE, open(outfile("t5_trace.pkl"), "wb"))
    summarise()


def summarise():
    tr = pickle.load(open(outfile("t5_trace.pkl"), "rb"))
    saved = pickle.load(open(outfile("t5_saved_runs.pkl"), "rb"))
    two53 = 2 ** 53
    def regime(n, p):
        mean = n * p
        if mean <= 30:
            return "inv"                                    # numpy's inversion branch
        if mean <= 42:
            return "ok"                                     # BTPE never reaches its last test
        if mean > 1e6:
            return "D" if n >= 10 ** 15 else "ok"
        if n >= two53:
            return "A" if mean <= 1e4 else "B"
        return "C" if n >= 10 ** 15 else "ok"
    lines = ["Calls of numpy's Generator.binomial with a count >= 1e14 in the published run of sim_grouped.py (first-version sampler)"]
    for suite in ("main", "noharper", "maxform", "neg_tol", "q_plain"):
        recs = [r for r in saved if r["suite"] == suite]
        t = [x for x in tr if x[0] == suite]
        byrun = {}
        for (_, run, n, p) in t:
            byrun.setdefault(run, []).append((n, p, regime(n, p)))
        lines.append(f"suite '{suite}': {len(recs)} runs ({sum(1 for r in recs if 'error' not in r['old'])} completed), "
                     f"{len(t)} binomial calls with n >= 1e14 in {len(byrun)} runs")
        for reg in ("A", "B", "C", "D", "inv", "ok"):
            calls = [(run, n, p) for run, v in byrun.items() for (n, p, g) in v if g == reg]
            runs = sorted({c[0] for c in calls})
            comp = [r for r in runs if "error" not in recs[r]["old"]]
            lines.append(f"    regime {reg:3s}: {len(calls):6d} calls in {len(runs):4d} runs ({len(comp)} of them completed)")
        cells = {}
        for r in recs:
            key = (r["P"]["u"], r["P"]["n_o"])
            c = cells.setdefault(key, dict(runs=0, completed=0, A=0, AB=0, ABC=0, maxblock=0, big=0))
            c["runs"] += 1
            if "error" not in r["old"]:
                c["completed"] += 1
                c["maxblock"] = max(c["maxblock"], r["old"]["largest_block"])
                c["big"] += r["old"]["largest_block"] >= 10 ** 15
            regs = {g for (_, _, g) in byrun.get(r["run"], [])}
            c["A"] += "A" in regs
            c["AB"] += bool(regs & {"A", "B"})
            c["ABC"] += bool(regs & {"A", "B", "C"})
        lines.append("    per cell (u, n_o): runs, completed, largest block of a completed run, completed runs with a block >= 1e15, runs with a call in regime A / A or B / A, B or C")
        for key in sorted(cells):
            c = cells[key]
            lines.append(f"      u = {key[0]}, n_o = {key[1]:3d}: {c['runs']:3d} {c['completed']:3d}   {c['maxblock']:.2e}   {c['big']:3d}   {c['A']:3d} / {c['AB']:3d} / {c['ABC']:3d}")
        if suite == "main":
            aff = sorted({run for run, v in byrun.items() if any(g in ("A", "B", "C") for (_, _, g) in v)})
            lines.append(f"    runs of the main suite with at least one call in regime A, B or C: {len(aff)}; of these completed: "
                         f"{sum(1 for r in aff if 'error' not in recs[r]['old'])}")
            worst = sorted(((n, p, n * p, run) for run, v in byrun.items() for (n, p, g) in v if g == "A"), key=lambda z: z[2])[:12]
            lines.append("    the calls of regime A with the smallest means (n, p, n p, run): " + "; ".join(f"({n:.2e}, {p:.2e}, {m:.0f}, {run})" for n, p, m, run in worst))
    print("\n".join(lines))
    open(outfile("t5_trace_summary.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "summary":
        summarise()
    else:
        main()
