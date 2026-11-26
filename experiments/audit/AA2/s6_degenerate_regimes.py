#!/usr/bin/env python3
"""AA2 audit, script S6 -- two hypotheses of the lower bounds of theory report sections 11.16-11.19 and
11.27 whose removal collapses the complexity from exponential to ONE evaluation.

(i)  The confidence.  Theorems 11.25(a), 11.45, 11.54, 11.58, 11.58a(c) carry a factor (1 - 2 delta) and
     are stated for delta < 1/2.  For delta >= 1 - 1/ceil(n u / eps) ONE evaluation suffices on the whole
     class L_u(Q_n): evaluate psi at one point x0; then ln A + psi(x0) lies in an interval of length n u
     (Lipschitz), and a uniformly random point of an eps-grid of that interval is within eps/2 of ln A with
     probability at least 1/ceil(n u / eps).  Checked here by exact enumeration on Q_8.

(ii) The order of the marginal oracle.  Proposition 11.104 (free exact k-body marginals of the Gibbs measure
     mu_psi ~ e^{-psi} do not change the exponents) is stated for k = o(n / ln n).  For k = n the oracle
     returns mu_psi itself, and ONE evaluation gives ln A exactly: A = e^{-psi(x0)} / (2^n mu_psi(x0)).

Members of L_u are drawn as psi = min_j [c_j + u d(., s_j)] (lower envelopes of cones: u-Lipschitz), seeded.
Run:  python3 experiments/audit/AA2/s6_degenerate_regimes.py > experiments/audit/AA2/out_s6.txt
"""
import math
import numpy as np

rng = np.random.default_rng(20261126)
n, u = 8, 1.0
N = 1 << n
xs = np.arange(N)
popcnt = np.array([bin(x).count("1") for x in range(N)])


def random_member():
    k = int(rng.integers(1, 6))
    psi = np.full(N, np.inf)
    for _ in range(k):
        s = int(rng.integers(N))
        c = float(rng.uniform(-3, 3)) * n * u / 4
        psi = np.minimum(psi, c + u * popcnt[xs ^ s])
    return psi + float(rng.uniform(-50, 50))            # an arbitrary additive constant: the class has no scale


def is_lipschitz(psi):
    return all(np.abs(psi[xs ^ (1 << i)] - psi).max() <= u + 1e-12 for i in range(n))


print("AA2 / S6: two hypotheses whose removal makes one evaluation suffice")
print()
print(f"(i) confidence close to one: cube Q_{n}, u = {u}")
lo = n * math.log((1 + math.exp(-u)) / 2)
hi = n * math.log((1 + math.exp(u)) / 2)
print(f"    after one evaluation: ln A + psi(x0) in [{lo:.4f}, {hi:.4f}], length {hi - lo:.4f} = n u = {n * u:.4f}")
for eps in (0.5, 1.0, 2.0):
    J = math.ceil((hi - lo) / eps)
    grid = lo + eps / 2 + eps * np.arange(J)
    worst = 1.0
    inside = True
    for _ in range(400):
        psi = random_member()
        assert is_lipschitz(psi)
        x0 = int(rng.integers(N))
        val = math.log(np.exp(-(psi - psi[x0])).mean())             # ln A + psi(x0)
        inside &= (lo - 1e-9 <= val <= hi + 1e-9)
        good = np.sum(np.abs(grid - val) <= eps / 2 + 1e-12)        # number of grid points that are correct outputs
        worst = min(worst, good / J)
    print(f"    eps = {eps}: grid of J = {J} points; over 400 random members the success probability of a uniformly random"
          f" grid point is at least {worst:.4f} (>= 1/J = {1 / J:.4f}); value always inside the interval: {inside}")
    print(f"             => (eps/2, delta)-correct with ONE evaluation for every delta >= {1 - 1 / J:.4f};"
          f" the lower bound (1 - 2 delta) 2^n/|B(n, k*)| of Theorem 11.25(a) is void there, and cannot be repaired")
print()
print(f"(ii) a marginal oracle of full order k = n: cube Q_{n}")
err = 0.0
for _ in range(400):
    psi = random_member()
    w = np.exp(-psi)
    A = w.mean()
    mu = w / w.sum()                                                # what the oracle of order n returns
    x0 = int(rng.integers(N))
    A_rec = math.exp(-psi[x0]) / (N * mu[x0])                       # one evaluation of psi
    err = max(err, abs(math.log(A_rec) - math.log(A)))
print(f"    largest |ln A_reconstructed - ln A| over 400 random members: {err:.2e}  (one evaluation, zero error)")
print("    => the hypothesis 'k small' of Proposition 11.104 cannot be dropped: between k = o(n / ln n) (exponents unchanged)")
print("       and k = n (one evaluation) the complexity must fall from exponential to 1; where is not known.")
print()
# what the proof of Proposition 11.104 gives for k proportional to n (Gilbert-Varshamov codes instead of BCH duals)
print("(iii) what the proof of Proposition 11.104 still gives for k = kappa n (arithmetic; our remark, not in the report):")
print("      a linear code C whose dual has minimum distance > k exists with |C| = 2^{n h2(k/n)} at most (dual of rate")
print("      1 - h2(k/n), Gilbert-Varshamov); the proposition then loses ln|C| = n ln2 h2(kappa) in the count AND in the accuracy.")
h2 = lambda x: 0.0 if x in (0.0, 1.0) else -(x * math.log2(x) + (1 - x) * math.log2(1 - x))
a = math.log(2) + (lambda q: q * math.log(q) + (1 - q) * math.log(1 - q))(1 / (1 + math.exp(u)))
for kappa in (0.001, 0.005, 0.01, 0.02, 0.05):
    loss = math.log(2) * h2(kappa)
    print(f"      kappa = {kappa}: loss per site {loss:.4f}  against  a = {a:.4f} (u = 1): "
          + ("the bound keeps a positive exponent at vanishing accuracy" if loss < a else "the bound is void"))
