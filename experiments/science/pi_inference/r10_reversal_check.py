#!/usr/bin/env python3
"""Coordinator's own exact check of the main finding of workstream R10 (review of the theory division's workstream Y):
for a two-state chain with nearest-neighbour coupling as known part, the capacity exponent `a` is RAISED above the
uniform cube's at slope u = 1 and LOWERED at slopes u = 3, 4.

Written independently of experiments/science/ws_R10 and of the theory division's code (nothing imported).

Setting.  Sites x in {0,1}^n; reference measure pi = stationary symmetric two-state Markov chain with flip
probability p (pi(x) = (1/2) prod (1-p if x_i = x_{i+1} else p)); residual class: |phi(x) - phi(x^i)| <= u for every
single flip.  The extreme members of the class ("vertices") for one common slope are u times the integer height
functions h on the cube (|h(x) - h(x^i)| = 1, h(0...0) = 0).  The capacity exponent of n sites is the Shannon
capacity a_n (nats) of the channel  vertex h  ->  configuration x ~ pi(x) e^{-u h(x)} / Z_h  (Blahut-Arimoto, with
the standard duality bracket  max_h KL(P_h || q) >= C >= I(w)).  For the uniform cube (p = 1/2) a_n = n (ln 2 - H(sigma_u)).

Reported: a_n for n = 1..4 over ALL vertices (2, 6, 38, 990), the increments a_n - a_{n-1}, and the cube's a.
Run:  python3 r10_reversal_check.py > r10_reversal_check.log        (about a minute)
"""
import itertools, math, sys
import numpy as np


def height_functions(n):
    """all h : {0,1}^n -> Z with h(0) = 0 and |h(x) - h(x with one bit flipped)| = 1."""
    pts = list(itertools.product((0, 1), repeat=n))
    idx = {x: k for k, x in enumerate(pts)}
    order = sorted(pts, key=sum)                       # by Hamming weight: lower neighbours are assigned first
    out = []
    h = {}

    def rec(k):
        if k == len(order):
            out.append(np.array([h[x] for x in pts], dtype=float))
            return
        x = order[k]
        if sum(x) == 0:
            h[x] = 0
            rec(k + 1)
            del h[x]
            return
        lows = [h[x[:i] + (0,) + x[i + 1:]] for i in range(n) if x[i] == 1]
        cand = set((lows[0] - 1, lows[0] + 1))
        for v in lows[1:]:
            cand &= set((v - 1, v + 1))
        for c in sorted(cand):
            h[x] = c
            rec(k + 1)
            del h[x]

    rec(0)
    return pts, out


def chain_measure(pts, p):
    w = np.array([0.5 * np.prod([(1 - p) if x[i] == x[i + 1] else p for i in range(len(x) - 1)]) for x in pts])
    return w / w.sum()


def capacity(P, tol=1e-12, itmax=200000):
    """Shannon capacity (nats) of the channel with rows P; returns (lower, upper) duality bracket."""
    m = P.shape[0]
    w = np.full(m, 1.0 / m)
    logP = np.log(P)
    for it in range(itmax):
        q = w @ P
        d = np.sum(P * (logP - np.log(q)), axis=1)      # KL(P_h || q)
        lo = float(w @ d); up = float(d.max())
        if up - lo < tol:
            break
        w = w * np.exp(d - d.max()); w /= w.sum()
    return lo, up


def a_cube(u):
    s = 1.0 / (1.0 + math.exp(-u))
    return math.log(2) + s * math.log(s) + (1 - s) * math.log(1 - s)


if __name__ == "__main__":
    counts = []
    for n in (1, 2, 3, 4):
        pts, H = height_functions(n)
        counts.append(len(H))
    print("number of vertices (height functions with h(0) = 0) for n = 1..4:", counts, " (expected 2, 6, 38, 990)")
    assert counts == [2, 6, 38, 990]
    for u in (1.0, 3.0, 4.0):
        print(f"# slope u = {u}: cube a = ln 2 - H(sigma_u) = {a_cube(u):.6f} per site")
        for p in (0.5, 0.3, 0.2, 0.1):
            prev = 0.0
            line = []
            for n in (1, 2, 3, 4):
                pts, H = height_functions(n)
                pi = chain_measure(pts, p)
                P = np.array([pi * np.exp(-u * (h - h.min())) for h in H])
                P /= P.sum(axis=1, keepdims=True)
                lo, up = capacity(P)
                assert up - lo < 1e-9, (n, p, u, lo, up)
                line.append((n, up, up - prev))
                prev = up
            txt = ";  ".join(f"a_{n} = {a:.6f} (increment {inc:.6f}, {inc / a_cube(u):.4f} of the cube)" for n, a, inc in line)
            print(f"   p = {p}: {txt}")
            if p == 0.5:
                for n, a, inc in line:
                    assert abs(a - n * a_cube(u)) < 1e-8, "control failed: the cube must be additive"
    print("ALL OK (control p = 1/2: a_n = n * cube, to 1e-8)")
