#!/usr/bin/env python3
"""R4 (SCI-REV-0003) -- the twins of Theorem 11.86 as functions on WHOLE small cubes, and an
end-to-end exact test of Lemma 11.85 (two rounds) against a real two-round algorithm.

Own code (uses my twins_exact.Twins); written before reading any of the authors' code.

Part A.  For several (n1, n2, u, T): psi_D, psi_S on all 2^n points (centre s; psi_s(x) = Psi(x xor s)):
   A1  largest difference over all n 2^n / 2 edges of the cube is <= u            (membership in L_u);
   A2  ln A by enumeration of the cube == sum over types (10 digits);
   A3  psi_D = psi_S on every point whose type is in V2, and = g1(d1) on every point with type in W1;
   A4  the fraction of points outside W1 / outside V2 equals p1 / p2 (the hypotheses h1, h2 of the
       Lean lemma hold with equality, by translation invariance of the cube).
Part B.  A real two-round algorithm ("posterior-greedy distinguisher"): batch 1 = M1 fixed points
   (random, or random points together with all their neighbours); after the answers it knows the
   set of centres consistent with them, and chooses batch 2 (M2 points) greedily so as to hit, for
   as many of these centres as possible, a point where the twins differ.  For EVERY centre s
   (all 2^n of them) we determine whether the transcripts on psi_{D,s} and psi_{S,s} differ.
   Lemma 11.85 / card_distinguished_le says:  (#centres distinguished)/2^n <= M1 p1 + M2 p2.
   Reported: the exact fraction, the bound, and the fraction for one blind batch of M1+M2 points.
"""
import math
import sys
import numpy as np
from scipy.special import logsumexp
from twins_exact import Twins


def popcount(a):
    return np.bitwise_count(a.astype(np.uint32)).astype(np.int64)


def cube_tables(tw):
    n1, n2 = tw.n1, tw.n2
    n = n1 + n2
    N = 1 << n
    z = np.arange(N, dtype=np.int64)
    d1 = popcount(z & ((1 << n1) - 1))
    d2 = popcount(z >> n1)
    return tw.FD[d1, d2], tw.FS[d1, d2], tw.g1[d1], d1, d2


def part_A(n1, n2, u, T, rng):
    tw = Twins(n1, n2, u, T)
    n = n1 + n2
    N = 1 << n
    PsiD, PsiS, G1, d1, d2 = cube_tables(tw)
    z = np.arange(N, dtype=np.int64)
    out = {}
    for name, Psi in (("D", PsiD), ("S", PsiS)):
        s = int(rng.integers(N))
        psi = Psi[z ^ s]                        # the function with centre s
        mx = 0.0
        for i in range(n):
            mx = max(mx, float(np.abs(psi - psi[z ^ (1 << i)]).max()))
        out[f"A1_maxedge_{name}"] = mx
        lnA_enum = float(logsumexp(-psi)) - n * math.log(2.0)
        lnA_type = tw.lnA_D if name == "D" else tw.lnA_S
        out[f"A2_lnA_{name}"] = (lnA_enum, lnA_type)
    inV2 = tw.W2[d2]
    inW1 = tw.W1[d1, d2]
    out["A3_equal_on_V2"] = bool(np.all(PsiD[inV2] == PsiS[inV2]))
    out["A3_equal_g1_on_W1"] = bool(np.all(np.abs(PsiD[inW1] - G1[inW1]) < 1e-12)
                                    and np.all(np.abs(PsiS[inW1] - G1[inW1]) < 1e-12))
    out["A4_p1"] = (float((~inW1).mean()), math.exp(tw.lnp1) if np.isfinite(tw.lnp1) else 0.0)
    out["A4_p2"] = (float((~inV2).mean()), math.exp(tw.lnp2) if np.isfinite(tw.lnp2) else 0.0)
    out["gap"] = tw.gap
    out["frac_differ"] = float((PsiD != PsiS).mean())
    return tw, out


def first_batch(n, M1, mode, rng):
    N = 1 << n
    if mode == "random":
        return rng.choice(N, size=M1, replace=False)
    # points with all their neighbours: floor(M1/(n+1)) stars
    k = max(1, M1 // (n + 1))
    centres = rng.choice(N, size=k, replace=False)
    pts = []
    for c in centres:
        pts.append(int(c))
        pts.extend(int(c) ^ (1 << i) for i in range(n))
    return np.unique(np.array(pts, dtype=np.int64))


def distinguisher(PsiD, PsiS, n, B1, M2):
    """Exact number of centres s for which the transcripts of the posterior-greedy two-round
    algorithm differ between psi_{D,s} and psi_{S,s}."""
    N = 1 << n
    isDelta = PsiD != PsiS
    Delta = np.nonzero(isDelta)[0].astype(np.int64)
    S = np.arange(N, dtype=np.int64)
    idx = B1[None, :] ^ S[:, None]
    YD, YS = PsiD[idx], PsiS[idx]
    dist1 = np.any(YD != YS, axis=1)
    und = np.nonzero(~dist1)[0]
    covered = np.zeros(N, dtype=bool)
    nclasses = 0
    if len(und) and len(Delta) and M2 > 0:
        keys = np.round(YD[und], 9)
        _, inv = np.unique(keys, axis=0, return_inverse=True)
        inv = np.asarray(inv).ravel()
        order = np.argsort(inv, kind="stable")
        bounds = np.flatnonzero(np.diff(inv[order])) + 1
        groups = np.split(und[order], bounds)
        nclasses = len(groups)
        for Sc in groups:
            unc = Sc
            for _ in range(M2):
                if len(unc) == 0:
                    break
                cov = np.bincount((unc[:, None] ^ Delta[None, :]).ravel(), minlength=N)
                x = int(np.argmax(cov))
                if cov[x] == 0:
                    break
                hit = isDelta[unc ^ x]
                covered[unc[hit]] = True
                unc = unc[~hit]
    return int(dist1.sum()), int(covered.sum()), nclasses


def blind(PsiD, PsiS, n, M, rng):
    N = 1 << n
    isDelta = PsiD != PsiS
    B = rng.choice(N, size=M, replace=False)
    S = np.arange(N, dtype=np.int64)
    return int(np.any(isDelta[B[None, :] ^ S[:, None]], axis=1).sum())


def main():
    rng = np.random.default_rng(20261125)
    print("# R4 own computation: twins on whole cubes and Lemma 11.85 end to end")
    print("# Part A")
    configs = [(6, 6, 1.0, 4.0), (8, 6, 1.0, 4.5), (6, 8, 1.0, 5.5), (7, 7, 2.0, 4.8), (7, 9, 1.0, 6.0),
               (9, 7, 0.5, 4.8), (8, 8, 3.0, 5.5)]
    built = []
    for (n1, n2, u, T) in configs:
        tw, o = part_A(n1, n2, u, T, rng)
        ok = (o["A1_maxedge_D"] <= u + 1e-12 and o["A1_maxedge_S"] <= u + 1e-12
              and abs(o["A2_lnA_D"][0] - o["A2_lnA_D"][1]) < 1e-9
              and abs(o["A2_lnA_S"][0] - o["A2_lnA_S"][1]) < 1e-9
              and o["A3_equal_on_V2"] and o["A3_equal_g1_on_W1"]
              and abs(o["A4_p1"][0] - o["A4_p1"][1]) < 1e-12 and abs(o["A4_p2"][0] - o["A4_p2"][1]) < 1e-12)
        print(f"(n1,n2,u,T)=({n1},{n2},{u},{T}): max edge diff D/S = {o['A1_maxedge_D']:.6f}/"
              f"{o['A1_maxedge_S']:.6f} (u={u}); lnA_D enum/type = {o['A2_lnA_D'][0]:.10f}/{o['A2_lnA_D'][1]:.10f}; "
              f"lnA_S = {o['A2_lnA_S'][0]:.10f}/{o['A2_lnA_S'][1]:.10f}; equal on V2: {o['A3_equal_on_V2']}; "
              f"= g1 on W1: {o['A3_equal_g1_on_W1']}; p1 = {o['A4_p1'][0]:.6f}; p2 = {o['A4_p2'][0]:.6f}; "
              f"P(differ) = {o['frac_differ']:.6f}; gap = {o['gap']:.4f};  ALL OK: {ok}")
        built.append((n1, n2, u, T, tw, o))
    print()
    print("# Part B: exact fraction of centres distinguished by a real two-round algorithm vs M1 p1 + M2 p2")
    print("# cols: config | mode | |B1| | M2 | dist. in batch 1 | dist. in batch 2 | fraction | bound | ratio | "
          "blind one batch of |B1|+M2 | posterior classes")
    worst = 0.0
    nviol = 0
    ntests = 0
    for (n1, n2, u, T, tw, o) in built:
        n = n1 + n2
        if n > 14:
            continue
        N = 1 << n
        PsiD, PsiS, G1, d1, d2 = cube_tables(tw)
        p1, p2 = o["A4_p1"][0], o["A4_p2"][0]
        for mode in ("random", "stars"):
            for (M1, M2) in ((4, 4), (8, 8), (16, 8), (n + 1, 8), (2 * (n + 1), 16), (4 * (n + 1), 4)):
                for rep in range(3):
                    B1 = first_batch(n, M1, mode, rng)
                    a, b, ncl = distinguisher(PsiD, PsiS, n, B1, M2)
                    frac = (a + b) / N
                    bound = len(B1) * p1 + M2 * p2
                    bl = blind(PsiD, PsiS, n, len(B1) + M2, rng) / N
                    ntests += 1
                    if frac > bound + 1e-12:
                        nviol += 1
                    worst = max(worst, frac / bound)
                    if rep == 0:
                        print(f"({n1},{n2},{u},{T}) {mode:6s} {len(B1):4d} {M2:3d}  {a:6d} {b:6d}  {frac:.5f}  "
                              f"{bound:.5f}  {frac/bound:.3f}   {bl:.5f}   {ncl}")
                sys.stdout.flush()
    print(f"# tests: {ntests}; violations of the bound: {nviol}; largest fraction/bound: {worst:.3f}")


if __name__ == "__main__":
    main()
