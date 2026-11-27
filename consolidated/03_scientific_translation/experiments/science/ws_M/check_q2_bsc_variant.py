#!/usr/bin/env python3
"""Workstream M — the convolution ("noisy codeword") variant of the Q2 sketch.

m = law of X = Y xor E,  Y uniform on a linear code C,  E i.i.d. Bernoulli(p_u), p_u = 1/(1+e^u).
Claims checked here (each has a one-line proof, see SM_REPORT.md K10(f)):
  (i)   -ln m has single-site differences <= u  (so m is in the bounded-difference Gibbs class);
  (ii)  all marginals on fewer than d(C^perp) sites are exactly uniform;
  (iii) H(m) = n h(p_u) + I(Y; X),  hence  n h(p_u) <= H(m) <= n h(p_u) + ln|C|.
Run:  python3 experiments/science/ws_M/check_q2_bsc_variant.py     (seconds)
"""
import itertools
import numpy as np


def span(gens):
    words = set()
    for coeffs in itertools.product([0, 1], repeat=len(gens)):
        w = 0
        for c, g in zip(coeffs, gens):
            if c:
                w ^= g
        words.add(w)
    return sorted(words)


def simplex(mm):
    n = (1 << mm) - 1
    return [sum(1 << (pos - 1) for pos in range(1, n + 1) if (pos >> j) & 1) for j in range(mm)], n


def rm1(mm):
    n = 1 << mm
    return [(1 << n) - 1] + [sum(1 << pos for pos in range(n) if (pos >> j) & 1) for j in range(mm)], n


def h2(q):
    return float(-q * np.log(q) - (1 - q) * np.log(1 - q))


def popcount(a):
    a = a.copy()
    c = np.zeros_like(a)
    while a.any():
        c += a & 1
        a >>= 1
    return c


def marginal_dev(p, n, k):
    xs = np.arange(1 << n)
    worst = 0.0
    for S in itertools.combinations(range(n), k):
        idx = np.zeros(1 << n, dtype=np.int64)
        for j, s in enumerate(S):
            idx |= ((xs >> s) & 1) << j
        marg = np.bincount(idx, weights=p, minlength=1 << k)
        worst = max(worst, float(np.max(np.abs(marg - 2.0 ** (-k)))))
    return worst


lines = ["code            n  |C|  d_perp   u   max|dlog m|/u   dev k=d_perp-1   dev k=d_perp   H/n      h(p_u)   (H-n h)/ln|C|"]
for name, (gens, n), dperp in [("simplex[7,3]", simplex(3), 3), ("RM(1,3)[8,4]", rm1(3), 4),
                               ("simplex[15,4]", simplex(4), 3), ("RM(1,4)[16,5]", rm1(4), 4)]:
    code = np.array(span(gens), dtype=np.int64)
    xs = np.arange(1 << n, dtype=np.int64)
    for u in (1.0, 2.0, 4.0):
        pu = 1 / (1 + np.exp(u))
        m = np.zeros(1 << n)
        for c in code:
            w = popcount(xs ^ c)
            m += pu ** w * (1 - pu) ** (n - w)
        m /= len(code)
        assert abs(m.sum() - 1) < 1e-12
        lip = max(float(np.max(np.abs(np.log(m) - np.log(m[xs ^ (1 << i)])))) for i in range(n))
        H = float(-(m * np.log(m)).sum())
        ratio = (H - n * h2(pu)) / np.log(len(code))
        assert lip <= u + 1e-9 and -1e-9 <= ratio <= 1 + 1e-9
        d1 = marginal_dev(m, n, dperp - 1)
        d2 = marginal_dev(m, n, dperp)
        lines.append(f"{name:14s} {n:2d} {len(code):3d}    {dperp}     {u:.0f}     {lip / u:.4f}        {d1:.1e}         "
                     f"{d2:.1e}      {H / n:.4f}   {h2(pu):.4f}   {ratio:.4f}")
out = "\n".join(lines)
print(out)
open(__file__.replace(".py", ".out"), "w").write(out + "\n")
