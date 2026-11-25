#!/usr/bin/env python3
"""Exhaustive checks on small cubes (own code).

(1) The pair (F_D, F_S) of Theorem U3 as functions on the whole cube Q_{n1} x Q_{n2} (n = n1 + n2 <= 16) for random
    centres: psi(x) = F(d(x^1,s^1), d(x^2,s^2)) is u-Lipschitz on every edge of the cube; A(psi) computed by summing
    over all 2^n points equals the sum over types; the two functions coincide exactly on the points whose type lies
    in V2, and equal g_1(d_1) on the points whose type lies in W1 cap V2.
(2) Lemma U2 by simulation: random two-round "algorithms" (round 1: a batch of M1 uniformly random points; round 2:
    M2 points whose first block is placed at chosen distances from the true centre s^1 -- more than any algorithm
    can do -- and whose second block is uniform); frequency with which some answer differs between the twins,
    against the bound M1 (p1 + p2) + M2 p2.
(3) The radial algorithm RAD of workstream H (Theorem 11.51) in exactly two rounds on Q_14: random radial
    instances, exact outputs / brackets.
usage: small_cube_checks.py
"""
import math, itertools, sys
import numpy as np
from lb2_exact import build, lnA
from ulib import logsumexp

rng = np.random.default_rng(20261125)


def popcount(a):
    a = a.copy()
    c = np.zeros(a.shape, dtype=np.int64)
    while np.any(a):
        c += (a & 1)
        a >>= 1
    return c


def check_pair(u, n1, n2, T):
    n = n1 + n2
    B = build(u, n1, n2, T, balance=True, cap=True)
    if B is None:
        return None
    FD, FS, g = B["F"], B["Fs"], B["g"]
    s1 = int(rng.integers(0, 1 << n1)); s2 = int(rng.integers(0, 1 << n2))
    x = np.arange(1 << n, dtype=np.int64)
    x1, x2 = x >> n2, x & ((1 << n2) - 1)
    d1, d2 = popcount(x1 ^ s1), popcount(x2 ^ s2)
    out = {}
    for name, F in (("F_D", FD), ("F_S", FS)):
        psi = F[d1, d2]
        mx = 0.0
        for bit in range(n):
            mx = max(mx, float(np.max(np.abs(psi - psi[x ^ (1 << bit)]))))
        lnA_cube = logsumexp(-psi) - n * math.log(2)
        out[name] = (mx, lnA_cube, lnA(B, "F" if name == "F_D" else "Fs"))
    inV2 = (d2 >= B["lo2"]) & (d2 <= B["hi2"])
    same_on_V2 = bool(np.all(FD[d1, d2][inV2] == FS[d1, d2][inV2]))
    inW1 = B["valid"][d1] & (d2 >= B["lo"][d1]) & (d2 <= B["hi"][d1]) & inV2
    eq_g = bool(np.all(np.abs(FD[d1, d2][inW1] - g[d1][inW1]) < 1e-12))
    return B, out, same_on_V2, eq_g, (s1, s2)


def lemma_sim(u, n1, n2, T, M1, M2, trials):
    B = build(u, n1, n2, T, balance=True, cap=True)
    FD, FS = B["F"], B["Fs"]
    p1, p2 = math.exp(B["lnp1"]), math.exp(B["lnp2"])
    differ = 0
    for _ in range(trials):
        # types of the round-1 points: independent Bin(n1,1/2) x Bin(n2,1/2); round 2: d1 chosen freely (adversarially:
        # uniformly over all distances), d2 ~ Bin(n2, 1/2)
        d1 = rng.binomial(n1, 0.5, M1); d2 = rng.binomial(n2, 0.5, M1)
        e1 = rng.integers(0, n1 + 1, M2); e2 = rng.binomial(n2, 0.5, M2)
        differ += bool(np.any(FD[d1, d2] != FS[d1, d2]) or np.any(FD[e1, e2] != FS[e1, e2]))
    return differ / trials, M1 * (p1 + p2) + M2 * p2, lnA(B, "F") - lnA(B, "Fs")


def rad_two_rounds(n, u, M, trials):
    """Theorem 11.51 (workstream H), algorithm RAD: round 1 = M uniform points and their n neighbours; round 2 = a
    monotone path from the candidate centre.  Returns (#exact outputs correct, #exact, #bracket outputs within
    the stated factor, #bracket)."""
    N = 1 << n
    x = np.arange(N, dtype=np.int64)
    lb = np.array([math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) for j in range(n + 1)])
    res = dict(exact_ok=0, exact=0, flat_ok=0, flat=0, rounds=set())
    for _ in range(trials):
        s = int(rng.integers(0, N))
        kind = rng.choice(["walk", "flat", "dip", "alt", "trunc"])
        if kind == "walk":
            fprof = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, n))])
        elif kind == "flat":
            fprof = np.zeros(n + 1)
        elif kind == "dip":
            R = int(rng.integers(1, n // 3 + 1)); fprof = -u * np.maximum(R - np.arange(n + 1), 0.0)
        elif kind == "alt":
            fprof = (u / 2) * (-1.0) ** np.arange(n + 1)
        else:
            R = int(rng.integers(1, n // 2)); fprof = u * np.maximum(np.arange(n + 1), R).astype(float)
        psi = fprof[popcount(x ^ s)]
        lnA_true = logsumexp(lb - fprof) - n * math.log(2)
        # round 1
        pts = rng.integers(0, N, M)
        cand = None
        for p in pts:
            nb = psi[p ^ (1 << np.arange(n))]
            vals = np.unique(np.round(nb, 12))
            if len(vals) >= 2:
                cls = np.round(nb, 12) == vals[0]
                cand = int(p)
                for bit in np.nonzero(cls)[0]:
                    cand ^= (1 << int(bit))
                break
        if cand is not None:
            # round 2: monotone path from cand to its antipode
            path = [cand]
            for bit in range(n):
                path.append(path[-1] ^ (1 << bit))
            F = psi[np.array(path)]                       # psi as a function of d(x, cand)
            est = logsumexp(lb - F) - n * math.log(2)
            res["exact"] += 1
            res["exact_ok"] += abs(est - lnA_true) < 1e-9
            res["rounds"].add(2)
        else:
            alpha = psi[pts[0]]; beta = psi[pts[0] ^ 1]
            est = math.log((math.exp(-alpha) + math.exp(-beta)) / 2)
            res["flat"] += 1
            res["flat_ok"] += abs(est - lnA_true) < 1.0     # crude: the bracket of Theorem 11.51 at this M
            res["rounds"].add(1)
    return res


if __name__ == "__main__":
    u = 1.0
    print("(1) the twins on whole cubes")
    for (n1, n2, T) in ((6, 6, 3.0), (8, 6, 4.0), (8, 8, 4.5), (9, 7, 5.0), (7, 9, 5.5)):
        r = check_pair(u, n1, n2, T)
        if r is None:
            print(f"  n1={n1} n2={n2} T={T}: W1 empty"); continue
        B, out, same, eqg, cen = r
        print(f"  n1={n1} n2={n2} T={T}: lo2={B['lo2']} | "
              + " | ".join(f"{k}: max edge diff {v[0]:.6f} (u={u}), lnA cube {v[1]:.10f} types {v[2]:.10f}" for k, v in out.items())
              + f" | F_D=F_S on V2: {same} | =g_1 on W1 cap V2: {eqg} | gap {out['F_D'][1]-out['F_S'][1]:.4f}")
    print("(2) Lemma U2 by simulation (types only; round 2 may choose d1 freely)")
    for (n1, n2, T, M1, M2) in ((30, 30, 9.0, 3, 3), (30, 30, 9.0, 10, 10), (40, 40, 11.0, 10, 10), (40, 40, 11.0, 40, 40), (60, 50, 12.0, 30, 30)):
        fr, bd, gap = lemma_sim(u, n1, n2, T, M1, M2, 4000)
        print(f"  n1={n1} n2={n2} T={T} M1={M1} M2={M2}: P(some answer differs) = {fr:.4f} <= bound {bd:.4f} : {fr <= bd + 3*math.sqrt(max(bd,1e-4)/4000)}   (gap of the twins {gap:.3f})")
    print("(3) RAD in two rounds on Q_14")
    res = rad_two_rounds(14, 1.0, 40, 300)
    print("  ", res)
