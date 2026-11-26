"""R6-T5 (iii): every run of the published suite of sim_grouped.py repeated with the corrected sampler.

Input: t5_saved_runs.pkl written by t5_trace_old_runs.py -- for every run of the published suite (seeds 31, 32) the
state of the random generator at the entry of the run and the arguments of the run.  Each run is started again from
that state with the SECOND version of stable_multinomial.py (argv[2]) in place of the first.  A run that never has a
node with more than 2^31 points consumes the generator exactly as before and must reproduce the old outcome; the
others are the same instance and parameters with a correct sample.  The checks are the workstream's own
(sim_grouped.check_grouped, unchanged).

Usage:  python3 t5_rerun_new.py <dir with the corrected stable_multinomial.py> <dir with klib.py, sim_outer_loop.py, sim_grouped.py> [main|mut]
        (in the repository, after t5_trace_old_runs.py:  python3 -B t5_rerun_new.py ../../workstreams/K ../../workstreams/K main ;
         five minutes for "main", three for "mut")
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


newdir, src = (os.path.abspath(a) for a in sys.argv[1:3])
which = sys.argv[3] if len(sys.argv) > 3 else "main"
sys.path.insert(0, src)
sys.path.insert(0, newdir)                                   # the corrected stable_multinomial.py is found first
import stable_multinomial as SM                             # noqa: E402
assert hasattr(SM, "binomial_exact"), "the corrected sampler was not loaded"
import sim_grouped as SG                                    # noqa: E402
from sim_outer_loop import Params                           # noqa: E402
assert SG.StableMultinomial is SM.StableMultinomial


def post(stats):
    """The post-processing at the end of sim_grouped.suite."""
    cl = stats.pop("closing")
    lm = sorted(stats.pop("log10_M"))
    stats["closed_at_r<=p_u*n_o"] = sum(1 for (r, rd, pn) in cl if 0 <= r <= pn)
    stats["closed_at_r<=r_dagger"] = sum(1 for (r, rd, pn) in cl if 0 <= r <= rd)
    if lm:
        stats["log10_M(min,median,max)"] = (round(lm[0], 2), round(lm[len(lm) // 2], 2), round(lm[-1], 2))
        stats["runs_with_M>1e12"] = sum(1 for v in lm if v > 12)
    for key in ("widest", "width_slack", "tightest_count", "largest_M_over_Mdag", "neg_share"):
        stats[key] = round(stats[key], 4)
    return stats


def main():
    saved = pickle.load(open(outfile("t5_saved_runs.pkl"), "rb"))
    suites = ["main"] if which == "main" else ["noharper", "maxform", "neg_tol", "q_plain"]
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    t0 = time.time()
    out(f"Every run of the published suite of sim_grouped.py repeated from the same generator state with the corrected sampler ({which})")
    paired = []
    for suite in suites:
        recs = [r for r in saved if r["suite"] == suite]
        stats = SG.new_stats()
        allfails = []
        same = changed = 0
        for r in recs:
            a = r["P"]
            P = Params(a["n"], a["n_o"], a["u"], a["lam"], a["eta"], a["etap"], a["theta"], a["b"], a["ladder"], delta=a["delta"])
            assert P.K == r["K"] and P.rdag == r["rdag"]
            g = np.random.Generator(np.random.PCG64())
            g.bit_generator.state = r["state"]
            run = SG.run_grouped(g, r["vals"], r["probs"], r["psi0"], P, mode=r["mode"], mut=r["mut"])
            new = None
            if "error" in run:
                if run["error"].startswith("sample too large"):
                    stats["skipped"] += 1
                else:
                    allfails.append((a["u"], a["n_o"], [(run["error"],)]))
                new = dict(error=run["error"])
            else:
                g0 = stats["good"]
                f = SG.check_grouped(run, r["vals"], r["probs"], P, stats)
                if f:
                    allfails.append((a["u"], a["n_o"], f[:3]))
                seq = run["levels"] + [run["last"]]
                new = dict(maxM=max(lv["M"] for lv in seq), npop=sum(1 for lv in run["levels"] if lv["populated"]),
                           nneg=sum(1 for lv in run["levels"] if not lv["populated"]), last_r=run["last"]["r"],
                           last_pop=run["last"]["populated"], lower=run["lower"], upper=run["upper"],
                           good=(stats["good"] - g0 == 1), fails=[x[0] for x in f])
            old = r["old"]
            keys = ("maxM", "npop", "nneg", "last_r", "last_pop", "lower", "upper", "good")
            identical = ("error" in old and "error" in new and old["error"] == new["error"]) or \
                        ("error" not in old and "error" not in new and all(old[k] == new[k] for k in keys) and old["fails"] == new["fails"])
            same += identical
            changed += not identical
            paired.append(dict(suite=suite, run=r["run"], u=a["u"], n_o=a["n_o"], old=old, new=new, identical=identical))
        stats = post(stats)
        if suite == "main":
            out(f"  stats: {stats}")
            out(f"  failures: {len(allfails)}" + ("" if not allfails else f"   first: {allfails[:3]}"))
        else:
            kinds = {}
            for (_, _, fl) in allfails:
                for f in fl:
                    kinds[f[0]] = kinds.get(f[0], 0) + 1
            out(f"  mutation {suite:9s}: {len(allfails):3d} of {stats['runs']:3d} runs fail; kinds {kinds}")
        out(f"  suite '{suite}': {len(recs)} runs; outcome identical to the first-version run in {same}, different in {changed}   ({time.time() - t0:.0f} s)")
    pickle.dump(paired, open(outfile(f"t5_paired_{which}.pkl"), "wb"))
    open(outfile(f"t5_new_sim_grouped_{which}.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
