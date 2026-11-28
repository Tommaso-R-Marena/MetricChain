"""Review checks for Propositions 9.5 and 9.6 of CERTIFIED_INFERENCE.md (added to the note after the
review had started), against a brute-force programme over the whole cone.

9.5: monotone targets, binary sites: sup over the class = expectation under the extreme product tilt.
9.6: the sequential bound SEQ(g) = T_1 ... T_n g: soundness for arbitrary g; equality for additive g and for
     coordinatewise monotone g - for binary sites, and for sites with three ordered states; how loose the
     bound can be (the note reports factors 1.13 - 1.40 on its own cases).

Run:  python check_sec9b.py
"""
from __future__ import annotations

import itertools

import numpy as np

import ref
from check_sec9 import cone_extreme, hamming_edges, product_space

rng = np.random.default_rng(9596)


def seq_bound(pis, slopes, g):
    """T_1 ... T_n g for g given as an array over the product space (axis i = site i)."""
    g = np.asarray(g, float)
    n = g.ndim
    for i in reversed(range(n)):
        out = np.empty(g.shape[:-1])
        for idx in itertools.product(*[range(k) for k in g.shape[:-1]]):
            out[idx] = ref.threshold_max(pis[i], np.exp(slopes[i]) * pis[i], g[idx])
        g = out
    return float(g)


def setup(sizes):
    states = product_space(sizes)
    pis = [rng.dirichlet(np.ones(k) * 2) for k in sizes]
    pi = np.array([np.prod([pis[i][s[i]] for i in range(len(sizes))]) for s in states])
    slopes = rng.uniform(0.1, 1.2, len(sizes))
    edges, C = hamming_edges(states, slopes)
    return states, pis, pi, slopes, edges, C


def random_monotone(sizes):
    """A function on the product of chains that is non-decreasing in every coordinate."""
    kind = rng.integers(0, 3)
    grids = np.meshgrid(*[np.arange(k) for k in sizes], indexing="ij")
    if kind == 0:                 # threshold of a positive combination
        a = rng.uniform(0.2, 1.0, len(sizes))
        lin = sum(ai * gi for ai, gi in zip(a, grids))
        return (lin >= rng.uniform(lin.min(), lin.max())).astype(float)
    if kind == 1:                 # convex increasing transform of a positive combination
        a = rng.uniform(0.2, 1.0, len(sizes))
        lin = sum(ai * gi for ai, gi in zip(a, grids))
        return np.exp(rng.uniform(0.2, 1.5) * lin)
    # running maximum of noise along every axis (monotone, no additive structure)
    g = rng.normal(size=sizes)
    for ax in range(len(sizes)):
        g = np.maximum.accumulate(g, axis=ax)
    return g


def check_95_96_binary():
    worst_95 = worst_seq_mono = worst_seq_add = 0.0
    unsound = 0
    loosest = 0.0
    for _ in range(120):
        n = int(rng.integers(2, 6))
        sizes = [2] * n
        states, pis, pi, slopes, edges, C = setup(sizes)
        # 9.5: monotone target
        g = random_monotone(sizes)
        gv = np.array([g[s] for s in states])
        hi = cone_extreme(pi, edges, C, gv, sense=+1)
        lo = cone_extreme(pi, edges, C, gv, sense=-1)
        theta = [np.log(p[1] / p[0]) for p in pis]
        sig = lambda z: 1 / (1 + np.exp(-z))
        def prod_mean(sign):
            q = [sig(t + sign * u) for t, u in zip(theta, slopes)]
            w = np.array([np.prod([q[i] if s[i] else 1 - q[i] for i in range(n)]) for s in states])
            return float(w @ gv)
        worst_95 = max(worst_95, abs(hi - prod_mean(+1)), abs(lo - prod_mean(-1)))
        worst_seq_mono = max(worst_seq_mono, abs(seq_bound(pis, slopes, g) - hi), abs(-seq_bound(pis, slopes, -g) - lo))
        # 9.6: additive target
        parts = [rng.uniform(-1, 1, 2) for _ in range(n)]
        ga = np.zeros(sizes)
        for i in range(n):
            shape = [1] * n
            shape[i] = 2
            ga = ga + parts[i].reshape(shape)
        hi_a = cone_extreme(pi, edges, C, np.array([ga[s] for s in states]), sense=+1)
        worst_seq_add = max(worst_seq_add, abs(seq_bound(pis, slopes, ga) - hi_a))
        # 9.6: arbitrary target - soundness and looseness
        gr = rng.normal(size=sizes)
        grv = np.array([gr[s] for s in states])
        hi_r = cone_extreme(pi, edges, C, grv, sense=+1)
        lo_r = cone_extreme(pi, edges, C, grv, sense=-1)
        s_hi, s_lo = seq_bound(pis, slopes, gr), -seq_bound(pis, slopes, -gr)
        if s_hi < hi_r - 1e-9 or s_lo > lo_r + 1e-9:
            unsound += 1
        loosest = max(loosest, (s_hi - s_lo) / (hi_r - lo_r))
    print(f"[9.5] binary sites, monotone targets: |sup over class - E under the product tilt| <= {worst_95:.2e}")
    print(f"[9.6] binary sites: SEQ = exact for monotone targets ({worst_seq_mono:.2e}) and additive targets ({worst_seq_add:.2e});"
          f" random targets: unsound cases = {unsound}, largest width ratio SEQ/exact = {loosest:.3f}")


def check_96_three_states():
    worst = 0.0
    example = None
    unsound = 0
    count = 0
    for _ in range(300):
        nsite = int(rng.integers(2, 4))
        sizes = [3] * nsite
        states, pis, pi, slopes, edges, C = setup(sizes)
        g = random_monotone(sizes)
        gv = np.array([g[s] for s in states])
        hi = cone_extreme(pi, edges, C, gv, sense=+1)
        sq = seq_bound(pis, slopes, g)
        if sq < hi - 1e-9:
            unsound += 1
        gap = (sq - hi) / max(1e-12, gv.max() - gv.min())
        if gap > 1e-7:
            count += 1
        if gap > worst:
            worst = gap
            example = (sizes, [np.round(p, 4).tolist() for p in pis], np.round(slopes, 4).tolist(), np.round(g, 4).tolist(),
                       round(hi, 6), round(sq, 6))
    print(f"[9.6] sites with three ordered states, coordinatewise monotone targets: SEQ > exact in {count}/300 instances"
          f" (unsound: {unsound}); largest gap = {worst:.4f} of the range of g")
    if example is not None:
        print(f"      example: sizes {example[0]}, site laws {example[1]}, slopes {example[2]},")
        print(f"               g = {example[3]}")
        print(f"               sup over the class = {example[4]}, SEQ = {example[5]}")
    print("      -> 'equality for coordinatewise monotone g' holds for binary sites (Proposition 9.5) and is FALSE as stated"
          " 'in the setting of Proposition 9.2' (sites with more than two states)")


def check_96_looseness():
    print("[9.6] how loose the sequential bound can be: parity-type and band targets of one additive statistic, binary sites")
    print("   n   reference p_i   slope   target                 exact interval          SEQ interval           width ratio")
    for n, p1, u, name in ((4, 0.75, 0.6, "parity"), (5, 0.75, 0.6, "parity"), (6, 0.75, 0.6, "parity"), (8, 0.75, 0.6, "parity"),
                           (6, 0.5, 0.6, "S == n/2"), (8, 0.5, 0.6, "S == n/2"), (8, 0.5, 0.3, "S == n/2"), (8, 0.3, 0.6, "S mod 3 == 0")):
        sizes = [2] * n
        states = product_space(sizes)
        pis = [np.array([1 - p1, p1])] * n
        pi = np.array([np.prod([p1 if b else 1 - p1 for b in s]) for s in states])
        slopes = np.full(n, u)
        edges, C = hamming_edges(states, slopes)
        S = np.indices(sizes).sum(axis=0)
        if name == "parity":
            g = np.where(S % 2 == 0, 1.0, -1.0)
        elif name == "S == n/2":
            g = (S == n // 2).astype(float)
        else:
            g = (S % 3 == 0).astype(float)
        gv = np.array([g[s] for s in states])
        hi = cone_extreme(pi, edges, C, gv, sense=+1)
        lo = cone_extreme(pi, edges, C, gv, sense=-1)
        s_hi, s_lo = seq_bound(pis, slopes, g), -seq_bound(pis, slopes, -g)
        print(f"   {n}   {p1:.2f}            {u:.1f}     {name:20s}  [{lo:8.5f}, {hi:8.5f}]    [{s_lo:8.5f}, {s_hi:8.5f}]    {(s_hi - s_lo) / (hi - lo):6.2f}")
    # random functions of ONE additive statistic S = number of ones (the use case named in the note)
    best = (0.0, None)
    for _ in range(150):
        n = 6
        sizes = [2] * n
        states = product_space(sizes)
        p1 = float(rng.uniform(0.15, 0.85))
        u = float(rng.uniform(0.2, 1.5))
        pis = [np.array([1 - p1, p1])] * n
        pi = np.array([np.prod([p1 if b else 1 - p1 for b in s]) for s in states])
        slopes = np.full(n, u)
        edges, C = hamming_edges(states, slopes)
        S = np.indices(sizes).sum(axis=0)
        table = rng.normal(size=n + 1) if rng.random() < 0.5 else rng.choice([0.0, 1.0], n + 1)
        if np.ptp(table) == 0:
            continue
        g = table[S]
        gv = np.array([g[s] for s in states])
        hi = cone_extreme(pi, edges, C, gv, sense=+1)
        lo = cone_extreme(pi, edges, C, gv, sense=-1)
        ratio = (seq_bound(pis, slopes, g) + seq_bound(pis, slopes, -g)) / (hi - lo)
        if ratio > best[0]:
            best = (ratio, (round(p1, 3), round(u, 3), np.round(table, 3).tolist()))
    print(f"   random functions of S on 6 binary sites (150 draws): largest width ratio SEQ/exact = {best[0]:.2f}"
          f"   at (p, slope, values of g by S) = {best[1]}")


if __name__ == "__main__":
    check_95_96_binary()
    check_96_three_states()
    check_96_looseness()
