#!/usr/bin/env python3
"""R12 item 1, second script — is the hypothesis "no single state can change ln Z by eps" needed
for the display of Theorem 11.110(e),

    (1 - 2 delta) k  <=  min_alg E|Q(r)|  <=  4 ln(1/delta) (e^{eps/2} + 1) (k + 1) + 1 ,

with k the largest number of pairwise disjoint heavy sets?  Claim tested here (my own, R12): NO,
if the check is done in two stages.  Let H be the set of states that are heavy on their own
(dip(x) > (e^eps - 1) z or bump(x) > (1 - e^{-eps}) z) and R the rest.

  stage 1: evaluate every state of H (|H| <= k evaluations; a disagreement => evaluate everything);
  stage 2: spot check on R with the sampler 1/2 dip_R/U_R + 1/2 bump_R/V_R (a half is dropped if
           its total is zero), N_R = ceil(ln(1/delta) max(1, 2 U_R/((e^{eps/2}-1) z), 2 V_R/((1-e^{-eps/2}) z))).

Every member that agrees with r on H and whose ln Z is off by more than eps/2 differs from r on a
subset of R of dip weight >= (e^{eps/2}-1) z or bump weight >= (1-e^{-eps/2}) z, so stage 2 misses
it with probability <= delta.  On R no single state is heavy, so the greedy packings of (d) apply
to R, and k >= |H| + max(k_R^dip, k_R^bump); hence |H| + N_R <= C (k + 1) + 1 with
C = 4 ln(1/delta)(e^{eps/2} + 1) >= 1.

The script checks, by exhaustive enumeration on random boxes with 6-10 states:
  (1) |H| + N_R <= C (k_mix + 1) + 1 in every case, whether or not the single-state condition holds;
  (2) the exact worst-case miss probability of stage 2 is <= delta;
  (3) how often the one-stage bound N of part (c) exceeds C (k_mix + 1) + 1 (it may: that is why
      the report states the hypothesis).

One command, no arguments:  python3 r12_01b_twostage.py
"""
import math
import time

import numpy as np

T0 = time.time()
rng = np.random.default_rng(2026112602)


def subset_sums(v):
    n = len(v)
    s = np.zeros(1 << n)
    for i in range(n):
        s[1 << i:1 << (i + 1)] = s[0:1 << i] + v[i]
    return s


def packing_number(heavy):
    size = len(heavy)
    f = np.zeros(size, dtype=np.int32)
    for S in range(1, size):
        low = S & (-S)
        rest = S ^ low
        best = f[rest]
        sub = rest
        while True:
            T = sub | low
            if heavy[T]:
                c = 1 + f[S ^ T]
                if c > best:
                    best = c
            if sub == 0:
                break
            sub = (sub - 1) & rest
        f[S] = best
    return int(f[size - 1])


delta = 0.05
L = math.log(1 / delta)
cases = single_fail = onestage_exceeds = twostage_exceeds = onestage_exceeds_without_heavy = 0
worst_miss = 0.0
worst_ratio = 0.0
examples = []
for n in (6, 8, 10):
    for inst in range(40 if n < 10 else 15):
        pi = rng.dirichlet(np.ones(n) * rng.choice([0.2, 1.0, 5.0]))
        lo = -rng.exponential(2.0, n)
        hi = rng.exponential(2.0, n)
        for pl in range(3):
            if pl == 0:
                r = lo + rng.random(n) * (hi - lo)
            elif pl == 1:
                r = lo + 1e-3 * (hi - lo)
            else:
                r = hi - 1e-3 * (hi - lo)
            z = float(np.sum(pi * np.exp(-r)))
            dip = np.maximum(pi * (np.exp(-lo) - np.exp(-r)), 0)
            bump = np.maximum(pi * (np.exp(-r) - np.exp(-hi)), 0)
            sd, sb = subset_sums(dip), subset_sums(bump)
            for eps in (0.05, 0.2, 0.5, 1.0, 2.0):
                td, tb = (math.exp(eps) - 1) * z, (1 - math.exp(-eps)) * z
                heavy = (sd > td) | (sb > tb)
                k = packing_number(heavy)
                C = 4 * L * (math.exp(eps / 2) + 1)
                upper = C * (k + 1) + 1
                H = [i for i in range(n) if dip[i] > td or bump[i] > tb]
                R = [i for i in range(n) if i not in H]
                eta = eps / 2
                td2, tb2 = (math.exp(eta) - 1) * z, (1 - math.exp(-eta)) * z
                UR, VR = float(dip[R].sum()), float(bump[R].sum())
                M = max(1.0, 2 * UR / td2, 2 * VR / tb2)
                N_R = math.ceil(L * M - 1e-12)
                total = len(H) + N_R
                # one-stage N of part (c)
                U, V = float(dip.sum()), float(bump.sum())
                N1 = math.ceil(L * max(1.0, 2 * U / td2, 2 * V / tb2) - 1e-12)
                # exact miss probability of stage 2: members agreeing with r on H, far at level eps/2
                dR = np.array([dip[i] if i in R else 0.0 for i in range(n)])
                bR = np.array([bump[i] if i in R else 0.0 for i in range(n)])
                q = np.zeros(n)
                halves = (UR > 0) + (VR > 0)
                if UR > 0:
                    q += dR / UR / halves
                if VR > 0:
                    q += bR / VR / halves
                maskH = sum(1 << i for i in H)
                allS = np.arange(1 << n)
                insideR = (allS & maskH) == 0
                heavy2 = ((sd > td2) | (sb > tb2)) & insideR
                if heavy2.any():
                    sq = subset_sums(q)
                    pmin = float(sq[heavy2].min())
                    miss = (1 - min(1.0, pmin)) ** N_R
                else:
                    miss = 0.0
                cases += 1
                worst_miss = max(worst_miss, miss)
                if H:
                    single_fail += 1
                if N1 > upper + 1e-9:
                    onestage_exceeds += 1
                    if not H:
                        onestage_exceeds_without_heavy += 1
                if total > upper + 1e-9:
                    twostage_exceeds += 1
                    examples.append((n, inst, pl, eps, k, len(H), N_R, upper))
                worst_ratio = max(worst_ratio, total / upper)
print("cases: %d; single-state condition violated (H non-empty) in %d" % (cases, single_fail))
print("one-stage N of part (c) exceeds C(k+1)+1 in %d cases; of these with H empty (no single state heavy): %d "
      "(the display of (e) as stated: must be 0)" % (onestage_exceeds, onestage_exceeds_without_heavy))
print("two-stage count |H| + N_R exceeds C(k+1)+1 in %d cases (claim: never)" % twostage_exceeds)
for e in examples[:5]:
    print("  COUNTER-EXAMPLE to my claim:", e)
print("largest (|H| + N_R) / (C(k+1)+1): %.4f" % worst_ratio)
print("worst exact miss probability of stage 2 over all cases: %.5f (delta = %g)" % (worst_miss, delta))
print("elapsed %.1f s" % (time.time() - T0))
print("R12_01B_DONE")
