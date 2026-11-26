#!/usr/bin/env python3
"""Coordinator's independent check of numbers in the engineering division's report X-013 (their answer to our request
R10-E1; experiments/eng/weighted_cube/REPORT.md at c81166b), written from the definitions in its section 1, without
their code.

Their block quantity:  cap_L = max_M I(M; phi -> pi_phi)  over the polytope of residuals with slopes (u, ..., u, u*) on a
block of L sites of the binary symmetric chain (flip probability p), pi_L(x) = prod_i P(x_{i-1}, x_i) with x_0 = 0,
pi_phi = pi_L e^{-phi} / Z.  They certify cap_L / L from complete vertex lists and state (section 4.2) that for p >= 0.3
the capacity is attained by the 2^L site-wise labels phi_sigma(x) = sum_i w_i [x_i != sigma_i] alone.
Here: the capacity of the channel with ONLY those 2^L inputs, by Blahut-Arimoto in plain numpy (lower end = I(M) at the
iterate, upper end = max_sigma KL(pi_sigma || Q) at the same iterate; the two meet at the optimum).  It is a LOWER bound
of cap_L for every (p, u), and must equal their certified value where they say site-wise labels are optimal.
Checked cells: every value of their tables `a` (L = 3 and 4) at p in {0.45, 0.4, 0.3} (24 + 24 cells), and the five
cells at L = 3 where they report site-wise optimum / capacity < 1 (there ours must be BELOW theirs by that factor).
Also: u* at their four quoted values; the cube's closed form; the increment (cap_4 - cap_3) / a_cube at (0.3, 1.5).
Control: the same computation with u* placed on the FIRST site of the block instead of the last (their section 1.5 says
which reading is used) -- it must NOT reproduce their numbers.
Run: python3 -B x013_sitewise_check.py > x013_sitewise_check.log
"""
import itertools, math
import numpy as np


def ustar(p, u):
    x = u
    for _ in range(500): x = u + math.log(((1 - p) * math.exp(x) + p) / (p * math.exp(x) + 1 - p))
    return x


def block_law(p, L):
    X = list(itertools.product((0, 1), repeat=L)); pi = np.array([math.prod((1 - p) if a == b else p for a, b in zip((0,) + x[:-1], x)) for x in X])
    return X, pi


def sitewise_capacity(p, u, L, last=True, iters=20000, tol=1e-13):
    us = ustar(p, u); w = [u] * (L - 1) + [us] if last else [us] + [u] * (L - 1); X, pi = block_law(p, L)
    W = np.array([[pi[j] * math.exp(-sum(w[i] for i in range(L) if X[j][i] != s[i])) for j in range(len(X))] for s in X]); W /= W.sum(axis=1, keepdims=True)
    M = np.full(len(X), 1.0 / len(X))
    for _ in range(iters):
        Q = M @ W; D = (W * np.log(W / Q[None])).sum(axis=1); lo, hi = float(M @ D), float(D.max())
        if hi - lo < tol: break
        M = M * np.exp(D); M /= M.sum()
    return lo, hi


def a_cube(u): return (u / 2) * math.tanh(u / 2) - math.log(math.cosh(u / 2))


def main():
    US = (0.5, 1, 1.5, 2, 2.5, 3, 4, 6)
    A3 = {0.45: (0.034366, 0.118768, 0.227569, 0.336926, 0.432148, 0.507949, 0.605801, 0.676351), 0.4: (0.040824, 0.129698, 0.236806, 0.342802, 0.434926, 0.508653, 0.605012, 0.675931),
          0.3: (0.058225, 0.154012, 0.253516, 0.345590, 0.427435, 0.495806, 0.591983, 0.671581)}
    A4 = {0.45: (0.034034, 0.117367, 0.225208, 0.334245, 0.429658, 0.505895, 0.604656, 0.676101), 0.4: (0.039654, 0.126996, 0.232176, 0.337491, 0.429957, 0.504515, 0.602655, 0.675401),
          0.3: (0.055187, 0.148377, 0.244575, 0.335653, 0.417817, 0.487418, 0.586713, 0.670235)}
    print("X-013, values copied from its tables `a` (six decimals, per site), against the site-wise capacity computed here")
    worst = 0.0; gap = 0.0; n = 0
    for L, T in ((3, A3), (4, A4)):
        for p, row in T.items():
            for u, theirs in zip(US, row):
                lo, hi = sitewise_capacity(p, u, L); worst = max(worst, abs(hi / L - theirs)); gap = max(gap, hi - lo); n += 1
    print(f"(1) {n} cells with p in (0.45, 0.4, 0.3), L = 3 and 4: largest |ours - theirs| = {worst:.2e} (their values have six decimals: must be below 1e-6); largest gap between our two ends {gap:.1e}")
    assert worst < 1e-6 and gap < 1e-9
    # the validation value and the cells where site-wise labels are NOT optimal (L = 3)
    lo, hi = sitewise_capacity(0.3, 3, 3); print(f"(2) (0.3, 3), L = 3: site-wise capacity per site in [{lo / 3:.12f}, {hi / 3:.12f}]; theirs, certified with all 96 vertices: [0.495805524594, 0.495805524595]")
    assert abs(hi / 3 - 0.4958055245945) < 2e-11
    exc = {(0.2, 2): (0.340137, 0.99943), (0.1, 1): (0.196777, 0.99915), (0.1, 2): (0.323642, 0.99998), (0.1, 2.5): (0.381519, 0.99949), (0.1, 3): (0.432593, 0.99955)}
    dev = 0.0
    for (p, u), (theirs, ratio) in exc.items():
        lo, hi = sitewise_capacity(p, u, 3); r = hi / 3 / theirs; dev = max(dev, abs(r - ratio)); assert hi / 3 < theirs
        print(f"    ({p}, {u}), L = 3: site-wise / their capacity = {r:.5f} (they print {ratio:.5f}); ours is below theirs, as a lower bound must be")
    print(f"(3) the five cells where they report that site-wise labels are not optimal: largest deviation of the ratio from theirs {dev:.1e} (their ratios have five decimals; the capacities six)")
    assert dev < 2e-5
    print(f"(4) u*: {', '.join(f'{ustar(p, 1.0):.3f}' for p in (0.45, 0.4, 0.3, 0.2))} at u = 1, p = 0.45, 0.4, 0.3, 0.2 (the theory report's values quoted by them: 1.218, 1.526, 1.981, 2.750 -- for p = 0.4, 0.3, 0.2, 0.1); "
          f"at p = 0.1: {ustar(0.1, 1.0):.3f}; u*(0.3, 3) = {ustar(0.3, 3):.10f} (theirs 3.8062061299)")
    assert abs(ustar(0.3, 3) - 3.8062061299414) < 1e-9 and abs(ustar(0.1, 1.0) - 2.750) < 5e-4 and abs(ustar(0.4, 1.0) - 1.218) < 5e-4
    print(f"(5) the cube: a_cube = {', '.join(f'{a_cube(u):.6f}' for u in US)} (their last row: 0.030299, 0.110944, 0.218095, 0.327813, 0.424611, 0.502282, 0.603052, 0.675835)")
    assert all(abs(a_cube(u) - t) < 1e-6 for u, t in zip(US, (0.030299, 0.110944, 0.218095, 0.327813, 0.424611, 0.502282, 0.603052, 0.675835)))
    c3, c4 = sitewise_capacity(0.3, 1.5, 3)[1], sitewise_capacity(0.3, 1.5, 4)[1]
    print(f"(6) increment at (0.3, 1.5): (cap_4 - cap_3) / a_cube = {(c4 - c3) / a_cube(1.5):.4f} (theirs 0.9984): the crossover of the increment sits within 2e-3 of this slope")
    assert abs((c4 - c3) / a_cube(1.5) - 0.9984) < 1e-4
    # control: u* on the first site
    bad = 0
    for p, row in A4.items():
        for u, theirs in zip(US, row): bad += int(abs(sitewise_capacity(p, u, 4, last=False)[1] / 4 - theirs) > 1e-6)
    print(f"(7) control, u* on the first site of the block instead of the last: {bad} of 24 cells (L = 4) disagree with their table by more than 1e-6 (must be positive)")
    assert bad > 0
    print("ALL DONE")


if __name__ == "__main__":
    main()
