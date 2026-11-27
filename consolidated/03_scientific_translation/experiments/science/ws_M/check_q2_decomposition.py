#!/usr/bin/env python3
"""Workstream M — exact form of the entropy in the coordinator's Q2 sketch (M_brief.md).

For a linear code C and mu(x) ~ exp(-u*dist(x,C)):  x -> (coset of x) is |C|-to-one and mu is
constant on each coset-translate, so mu = (uniform on C) x nu, where nu(coset) ~ exp(-u*w(coset))
and w = weight of the coset leader.  Hence  H(mu) = ln|C| + H(nu)  exactly  [P, one line].
This script evaluates both sides and compares H(nu) with n*h(1/(1+e^u)), the entropy of the
unrestricted product measure pi(e) ~ exp(-u|e|) (the class minimum, by
H(X) >= sum_i H(X_i | X_-i) >= n h(1/(1+e^u)) for energies with single-site differences <= c).
Run:  python3 experiments/science/ws_M/check_q2_decomposition.py   (seconds)
"""
import itertools
import numpy as np


def span(gens, n):
    words = set()
    for coeffs in itertools.product([0, 1], repeat=len(gens)):
        w = 0
        for c, g in zip(coeffs, gens):
            if c:
                w ^= g
        words.add(w)
    return sorted(words)



def dist_to_code(code, n):
    """Hamming distance of every x in {0,1}^n to the code (multi-source BFS)."""
    dist = np.full(1 << n, -1, dtype=np.int16)
    frontier = np.array(code, dtype=np.int64)
    dist[frontier] = 0
    d = 0
    while frontier.size:
        d += 1
        nxt = []
        for i in range(n):
            y = frontier ^ (1 << i)
            y = y[dist[y] < 0]
            if y.size:
                y = np.unique(y)
                dist[y] = d
                nxt.append(y)
        frontier = np.unique(np.concatenate(nxt)) if nxt else np.array([], dtype=np.int64)
    return dist



def h2(q):
    return float(-q * np.log(q) - (1 - q) * np.log(1 - q))



def rm1(mm):
    """generators of the first-order Reed-Muller code RM(1,mm), length 2^mm."""
    n = 1 << mm
    gens = [(1 << n) - 1]
    for j in range(mm):
        g = 0
        for pos in range(n):
            if (pos >> j) & 1:
                g |= 1 << pos
        gens.append(g)
    return gens, n



def simplex(mm):
    """generators of the simplex code, length 2^mm - 1 (dual of Hamming)."""
    n = (1 << mm) - 1
    gens = []
    for j in range(mm):
        g = 0
        for pos in range(1, n + 1):
            if (pos >> j) & 1:
                g |= 1 << (pos - 1)
        gens.append(g)
    return gens, n




lines = []
lines.append("code            n  |C|   u    H(mu)     ln|C|+H(nu)   H(nu)/n   h(1/(1+e^u))   (H(mu)-n*h)/ln|C|   E_nu|e|/n   p_u")
for name, (gens, n) in [("simplex[7,3]", simplex(3)), ("RM(1,3)[8,4]", rm1(3)),
                        ("simplex[15,4]", simplex(4)), ("RM(1,4)[16,5]", rm1(4))]:
    code = span(gens, n)
    dist = dist_to_code(code, n).astype(float)
    # one representative weight per coset: every coset has |C| elements with the same dist
    for u in (1.0, 2.0, 4.0, 8.0):
        w = np.exp(-u * dist)
        Z = w.sum()
        p = w / Z
        H = float(-(p * np.log(p)).sum())
        # nu: mass of a coset = |C| * exp(-u d)/Z ; number of cosets with leader weight d = (#x with dist d)/|C|
        ds, counts = np.unique(dist, return_counts=True)
        ncos = counts / len(code)
        q = len(code) * np.exp(-u * ds) / Z
        Hnu = float(-(ncos * q * np.log(q)).sum())
        Ew = float((ncos * q * ds).sum())
        pu = 1 / (1 + np.exp(u))
        assert abs(H - (np.log(len(code)) + Hnu)) < 1e-9
        assert H >= n * h2(pu) - 1e-12
        lines.append(f"{name:14s} {n:2d} {len(code):3d}   {u:.0f}   {H:8.4f}   {np.log(len(code)) + Hnu:8.4f}     "
                     f"{Hnu / n:.4f}    {h2(pu):.4f}         {(H - n * h2(pu)) / np.log(len(code)):.4f}            "
                     f"{Ew / n:.4f}     {pu:.4f}")
out = "\n".join(lines)
print(out)
open(__file__.replace(".py", ".out"), "w").write(out + "\n")
