"""R6-T5 (ii), supplement: high-statistics test of `binomial_exact` (the corrected sampler's reduction) -- 2 000 000
draws per cell, three seeds: z-scores of the mean and of the variance, and a chi-square test of the whole law against
the Poisson law (which Bin(n, mu/n) equals up to a total-variation distance mu/n < 1e-10 in these cells)."""
import sys, os, math, time
import numpy as np
try:
    from stable_multinomial import binomial_exact, _zmean_zvar, _poisson_chi2
except ImportError:                      # repository layout: the corrected sampler lives in experiments/workstreams/K
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "workstreams", "K"))
    from stable_multinomial import binomial_exact, _zmean_zvar, _poisson_chi2

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


lines = []
def out(s=""):
    print(s); lines.append(s); sys.stdout.flush()
N = 2000000
t0 = time.time()
worst = 0.0
out(f"binomial_exact, {N} draws per cell: z of the mean, z of the variance, chi-square z against Poisson(mu)")
for seed in (11, 12, 13):
    rng = np.random.default_rng(seed)
    for (nn, mu) in ((2 ** 50, 92.0), (2 ** 61, 92.0), (10 ** 17, 92.0), (2 ** 53 - 1, 500.0), (6 * 10 ** 15, 92.0), (10 ** 18, 500.0), (2 ** 62 - 1, 5000.0), (3 * 10 ** 15, 45.0)):
        y = binomial_exact(rng, np.full(N, nn, dtype=np.int64), np.full(N, mu / nn))
        zm, zv = _zmean_zvar(y, mu, mu)
        zc = _poisson_chi2(y, mu)
        worst = max(worst, abs(zm), abs(zv), abs(zc))
        out(f"  seed {seed}  n = {nn:22d}  mu = {mu:6.0f}:  mean {y.mean():10.4f}  z_mean {zm:6.2f}  z_var {zv:6.2f}  z_chi2 {zc:6.2f}")
ok = worst < 4.5
out(f"largest |z| over {3 * 8 * 3} statistics: {worst:.2f}   (passed: {ok};  {time.time() - t0:.0f} s)")
open(outfile("t5_exact_highstat.txt"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
