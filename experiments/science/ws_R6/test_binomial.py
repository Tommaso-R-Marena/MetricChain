"""
test_binomial.py -- workstream R6: the samplers behind the literal runs.
(1) numpy's Generator.binomial at huge n and tiny p (the regime where the legacy sampler is known to fail): mean and variance.
(2) r6lib.big_binomial beyond 2^61 (chunked): mean.
(3) r6lib.ClassInstance.new_block on the shells of Q_300 at a block of 2^59 points: far-tail shells against their exact expectations.
"""
import math
import numpy as np
import mpmath as mp
import r6lib as R

rng = np.random.default_rng(12345)
print("(1) numpy Generator.binomial, 20000 draws each")
for n, p in [(10 ** 18, 1e-17), (10 ** 18, 1e-19), (10 ** 18, 3e-18), (2 ** 62, 1e-15), (2 ** 62, 2e-17), (10 ** 18, 5e-16)]:
    x = rng.binomial(n, p, size=20000)
    mu = n * p
    z = (x.mean() - mu) / math.sqrt(mu / 20000)
    print("   n=%.3g p=%.1e: mean %.5g (exact %.5g, z=%+.2f), variance/mean %.3f" % (n, p, x.mean(), mu, z, x.var() / x.mean()))
print("(2) r6lib.big_binomial, 300 draws each")
for n, p in [(2 ** 70, 2.0 ** -60), (2 ** 66, 1e-18), (2 ** 64 + 12345, 0.25)]:
    xs = [R.big_binomial(n, p, rng) for _ in range(300)]
    m = sum(xs) / len(xs)
    mu = n * p
    sd = math.sqrt(n * p * (1 - p) / 300)
    print("   n=2^%.1f p=%.3g: mean %.8g (exact %.8g, z=%+.2f)" % (math.log2(n), p, m, mu, (m - mu) / sd))
print("(3) ClassInstance.new_block: shells of Q_300, block of 2^59 points, 40 blocks; tail shells with expectation between 1e-3 and 1e7")
m = 300
two = mp.mpf(2) ** m
prob = [mp.mpf(math.comb(m, d)) / two for d in range(m + 1)]
inst = R.ClassInstance(2 * m, m, 1.0, np.zeros(m + 1), prob, 0.0, np.zeros(m + 1, dtype=int), 0)
size = 2 ** 59
tot = np.zeros(m + 1, dtype=object)
nb = 40
for _ in range(nb):
    d = inst.new_block(size, rng)
    assert int(sum(d["cnt"].tolist())) == size
    for c, k in zip(d["cls"], d["cnt"]):
        tot[c] += int(k)
worst = 0.0
used = 0
for dsh in range(m + 1):
    ex = float(prob[dsh] * size)
    if 1e-3 <= ex <= 1e7:
        z = (float(tot[dsh]) - nb * ex) / math.sqrt(nb * ex)
        worst = max(worst, abs(z))
        used += 1
print("   block totals preserved; %d tail shells checked; largest |z| of the summed counts: %.2f" % (used, worst))
