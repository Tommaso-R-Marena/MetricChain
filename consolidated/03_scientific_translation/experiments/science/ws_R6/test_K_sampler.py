"""
test_K_sampler.py -- workstream R6: does the bias of numpy's binomial (finding m8) reach the "exact" sampler of workstream K?
Written and run AFTER all my own runs were finished.  It imports experiments/workstreams/K/stable_multinomial.py READ-ONLY
(run with `python3 -B` so that no bytecode is written into that directory) and repeats that file's own self-test law -- the
shells of Q_200 ordered as for a cone -- at the block sizes of K_REPORT section 6.8 (2^59 ... 2^62), with enough repetitions
to see a bias of a fraction of a percent (the self-test of that file uses 300 repetitions and a tolerance |z| < 4.5).
Reported: mean of the far-tail count / its expectation, and z = (mean - mu)/sqrt(mu/reps).
usage: python3 -B test_K_sampler.py [reps]
"""
import sys, os, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "workstreams", "K"))
from stable_multinomial import StableMultinomial

reps = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
print("numpy", np.__version__, "| reps", reps)
n_o = 200
probs = np.array([math.comb(n_o, k) for k in range(n_o + 1)], dtype=float) / 2.0 ** n_o
pc = probs[np.arange(n_o, -1, -1)]
tail = np.cumsum(pc[::-1])[::-1]
sm = StableMultinomial(pc)
# census of the tree: which nodes could be in the regime where numpy's binomial is biased (count >= 1e16, expected left count 60..1e4)?
for lg in (50, 59, 61, 62):
    n = 2.0 ** lg
    bad, spine, cnt = 0, [], n
    for lev in range(len(sm.levels) - 2, -1, -1):
        mass = sm.levels[lev]
        left, right = mass[0::2], mass[1::2]
        tot = left + right
        pl = np.where(tot > 0, left / np.where(tot > 0, tot, 1.0), 0.0)
        node = n * tot
        bad += int(np.sum((node >= 1e16) & (node * pl >= 60) & (node * pl <= 1e4)))
        spine.append("%.2g" % (cnt * pl[-1]))
        cnt *= 1 - pl[-1]
    print("block 2^%d: nodes with expected count >= 1e16 and expected left count in [60, 1e4]: %d; expected left counts along the right spine "
          "(from the root): %s" % (lg, bad, " ".join(spine)))
for seed in (1, 2):
    rng = np.random.default_rng(seed)
    for lg in (50, 59, 61, 62):
        size = 2 ** lg
        row = []
        for target_mu in (20.0, 92.0, 500.0, 5000.0):
            i = int(np.searchsorted(-tail * size, -target_mu))          # first index with size*tail[i] <= target
            mu = size * tail[i]
            a = np.array([float(sm.sample(rng, size)[i:].sum()) for _ in range(reps)])
            z = (a.mean() - mu) / math.sqrt(mu / reps)
            row.append("mu=%8.1f: mean/mu %.4f (z %+6.1f)" % (mu, a.mean() / mu, z))
        print("seed %d  block 2^%d | " % (seed, lg) + " | ".join(row))
        sys.stdout.flush()
