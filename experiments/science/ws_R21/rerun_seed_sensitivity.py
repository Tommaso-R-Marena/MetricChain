"""Re-run of THEIR code (rerun_copy/rigidity_checks.py, a570520) with other seeds: only the line
`rng = np.random.default_rng(20261127)` is changed; their functions test_R5 (and test_R3 for a few seeds) are
called unchanged.  Purpose: do their checks R3 and R5 pass for reasons that do not depend on the seed?
usage: python3 -I -B rerun_seed_sensitivity.py <path to rigidity_checks.py> <n_seeds_R5> <n_seeds_R3>
"""
import sys, time
src = open(sys.argv[1]).read()
n5, n3 = int(sys.argv[2]), int(sys.argv[3])
assert src.count("rng = np.random.default_rng(20261127)") == 1
print("seed sensitivity of their R5 and R3  start", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
passed5 = 0
for seed in range(1, n5 + 1):
    ns = {"__name__": "their_module"}
    exec(compile(src.replace("default_rng(20261127)", "default_rng(%d)" % seed), "rigidity_checks_seed%d" % seed, "exec"), ns)
    ok, out = ns["test_R5"]()
    passed5 += bool(ok)
    print("R5 seed %2d: %s |%s" % (seed, "ok    " if ok else "FAILED", out[0].strip()))
print("R5: passed with %d of %d seeds" % (passed5, n5))
passed3 = 0
for seed in range(1, n3 + 1):
    ns = {"__name__": "their_module"}
    exec(compile(src.replace("default_rng(20261127)", "default_rng(%d)" % seed), "rigidity_checks_seed%d" % seed, "exec"), ns)
    t0 = time.time()
    ok, out = ns["test_R3"]()
    passed3 += bool(ok)
    print("R3 seed %2d: %s |%s  (%.0f s)" % (seed, "ok    " if ok else "FAILED", out[0].strip(), time.time() - t0))
print("R3: passed with %d of %d seeds" % (passed3, n3))
print("DONE rerun_seed_sensitivity", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
