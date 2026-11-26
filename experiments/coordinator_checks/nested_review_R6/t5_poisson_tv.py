"""R6-T5, supplement: the total-variation distance between Bin(n, p) and Poisson(n p) against the bound
p (1 - e^{-n p}) <= min(p, n p^2)  (Le Cam / Barbour-Hall, cited from memory in NOTES.md and in the corrected sampler's
text) -- exact sums with scipy, a sanity check of the citation, not a proof."""
import sys, os, math
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)

lines = ["TV(Bin(n,p), Poisson(np)) against p(1 - e^{-np}), and the ratio TV/p"]
ok = True
for n, p in ((10 ** 4, 1e-3), (10 ** 4, 1e-2), (10 ** 6, 1e-4), (10 ** 6, 1e-6), (10 ** 7, 5e-5), (10 ** 8, 1e-6), (10 ** 9, 9.2e-8), (10 ** 3, 0.05), (50, 0.2)):
    mu = n * p
    hi = int(mu + 12 * math.sqrt(mu) + 30)
    k = np.arange(0, hi + 1)
    tv = 0.5 * (np.abs(stats.binom.pmf(k, n, p) - stats.poisson.pmf(k, mu)).sum() + stats.poisson.sf(hi, mu) + stats.binom.sf(hi, n, p))
    bound = p * (1 - math.exp(-mu))
    ok = ok and tv <= bound * (1 + 1e-9) + 1e-15
    lines.append(f"  n = {n:>10d}, p = {p:8.1e}, np = {mu:9.2f}:  TV = {tv:.3e}   bound = {bound:.3e}   TV/p = {tv / p:.3f}")
lines.append(f"TV <= p(1 - e^(-np)) in all cases: {ok}")
print("\n".join(lines))
open(outfile("t5_poisson_tv.txt"), "w").write("\n".join(lines) + "\n")
