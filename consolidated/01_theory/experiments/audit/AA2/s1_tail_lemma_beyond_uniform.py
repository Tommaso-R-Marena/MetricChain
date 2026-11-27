#!/usr/bin/env python3
"""AA2 audit, script S1 -- the exact tail lemma (theory report Lemma 11.43(b)) beyond its hypotheses.

Lemma 11.43(b): on the n-cube with the UNIFORM measure and ONE slope u, for every proper non-empty D
with |D| <= |B(r)|:   sum_{x in D} (e^{u dist(x, D^c)} - 1)  <=  sum_{j<=r} C(n,j)(e^{u(r+1-j)} - 1),
with equality for Hamming balls (Harper).  The lemma is the only isoperimetric input of Theorems 11.44,
11.52, 11.56, 11.58, 11.58a.

This script enumerates ALL 65 534 proper non-empty subsets of Q_4 and asks what survives when one
hypothesis is dropped:

  CONTROL  uniform measure, one slope: the maximum over |D| <= |B(r)| equals the ball value (must hold).
  TEST A   a p-biased product measure (a field as known part, reference instance psi_0 = 0), one slope:
           is  Xi_0(q) = max{ sum_{x in D} pi(x)(e^{u dist(x,D^c)} - 1) : pi(D) <= q }  attained by a Hamming
           ball?  by a "ball with type-dependent radii around one centre"?
  TEST B   uniform measure, site-dependent slopes u_i (weighted Hamming metric): is the maximum over
           |D| <= m attained by a ball of the weighted metric?

Deterministic (the slope vectors of TEST B are drawn with a fixed seed).  Run:
    python3 experiments/audit/AA2/s1_tail_lemma_beyond_uniform.py > experiments/audit/AA2/out_s1.txt
"""
import itertools
import math
import numpy as np

n = 4
N = 1 << n
pts = np.arange(N)
bits = np.array([[(x >> i) & 1 for i in range(n)] for x in range(N)])      # N x n
wt = bits.sum(axis=1)

# all proper non-empty subsets as membership matrix
masks = np.arange(1, (1 << N) - 1, dtype=np.int64)                         # 65 534 subsets
inD = ((masks[:, None] >> pts[None, :]) & 1).astype(bool)                   # S x N
size = inD.sum(axis=1)
BIG = 1e9


def dist_matrix(slopes):
    diff = bits[:, None, :] != bits[None, :, :]
    return (diff * np.asarray(slopes)[None, None, :]).sum(axis=2)           # N x N


def functional(dm, pi):
    """Phi(D) = sum_{x in D} pi(x) (exp(dist(x, D^c)) - 1) for every subset D (slopes are inside dm)."""
    out = np.zeros(len(masks))
    for x in range(N):
        # distance from x to the complement of D
        dd = np.where(inD, BIG, dm[x][None, :]).min(axis=1)
        out += np.where(inD[:, x], pi[x] * np.expm1(dd), 0.0)
    return out


def mask_of(points):
    m = 0
    for x in points:
        m |= 1 << int(x)
    return m


print("AA2 / S1: exact tail lemma on Q_4, all 65 534 proper non-empty subsets")
print()

# ------------------------------------------------------------------ CONTROL
print("CONTROL  uniform measure, one slope u (Lemma 11.43(b) must hold with equality at balls)")
ok_control = True
for u in (0.5, 1.0, 2.0):
    dm = dist_matrix([u] * n)
    phi = functional(dm, np.ones(N))
    for r in range(0, n):
        ball = sum(math.comb(n, j) for j in range(r + 1))
        best = phi[size <= ball].max()
        want = sum(math.comb(n, j) * math.expm1(u * (r + 1 - j)) for j in range(r + 1))
        good = abs(best - want) <= 1e-9 * max(1.0, want)
        ok_control &= good
        print(f"  u={u:3.1f} r={r} |B(r)|={ball:2d}  max over |D|<=|B(r)| = {best:.10f}   ball value = {want:.10f}   {'ok' if good else 'MISMATCH'}")
print("  control", "PASSED" if ok_control else "FAILED")
print()

# ------------------------------------------------------------------ TEST A
print("TEST A  p-biased product measure, one slope u, reference psi_0 = 0")
print("  Xi_0(q) = max{Phi(D): pi(D) <= q}  against  (i) Hamming balls, (ii) balls with type-dependent radii")
# families: Hamming balls and type-dependent balls around every centre
d_ham = dist_matrix([1] * n)
ball_masks = set()
for s in range(N):
    for r in range(0, n):
        ball_masks.add(mask_of([x for x in range(N) if d_ham[s, x] <= r]))
ball_masks.discard((1 << N) - 1)
tdep_masks = set()
for s in range(N):
    for radii in itertools.product(range(-1, n + 1), repeat=n + 1):
        m = mask_of([x for x in range(N) if d_ham[s, x] <= radii[wt[x]]])
        if 0 < m < (1 << N) - 1:
            tdep_masks.add(m)
ball_idx = np.array(sorted(ball_masks)) - 1          # index into masks (mask m is at position m-1)
tdep_idx = np.array(sorted(tdep_masks)) - 1
print(f"  families: {len(ball_idx)} Hamming balls, {len(tdep_idx)} type-dependent balls")
worstA = (1.0, None)
worstA2 = (1.0, None)
for p in (0.5, 0.4, 0.3, 0.2, 0.1):
    for u in (0.5, 1.0, 2.0, 4.0):
        pi = np.array([p ** wt[x] * (1 - p) ** (n - wt[x]) for x in range(N)])
        dm = dist_matrix([u] * n)
        phi = functional(dm, pi)
        meas = inD @ pi
        r_ball, r_tdep, arg = 1.0, 1.0, None
        # thresholds: the measures of all Hamming balls (the natural analogue of |D| <= |B(r)|)
        for q in sorted(set(np.round(meas[ball_idx], 15))):
            feas = meas <= q + 1e-13
            top = phi[feas].max()
            bb = phi[ball_idx][meas[ball_idx] <= q + 1e-13].max()
            tt = phi[tdep_idx][meas[tdep_idx] <= q + 1e-13].max()
            if top / bb > r_ball:
                r_ball = top / bb
                k = np.flatnonzero(feas)[phi[feas].argmax()]
                arg = (q, int(masks[k]), top, bb)
            r_tdep = max(r_tdep, top / tt)
        line = f"  p={p:3.1f} u={u:3.1f}  max_q Xi_0/best Hamming ball = {r_ball:.6f}   max_q Xi_0/best type-dependent ball = {r_tdep:.6f}"
        if arg is not None and r_ball > 1 + 1e-9:
            q, mk, top, bb = arg
            D = [x for x in range(N) if (mk >> x) & 1]
            line += f"   [q={q:.6f}: D={{{','.join(format(x, '04b') for x in D)}}}, Phi(D)={top:.6f}, best ball {bb:.6f}]"
        print(line)
        if r_ball > worstA[0]:
            worstA = (r_ball, (p, u))
        if r_tdep > worstA2[0]:
            worstA2 = (r_tdep, (p, u))
print(f"  RESULT A: largest ratio to the best Hamming ball {worstA[0]:.6f} at (p,u)={worstA[1]};"
      f" to the best type-dependent ball {worstA2[0]:.6f} at (p,u)={worstA2[1]}")
print("  (ratio 1.000000 at p = 0.5 is Lemma 11.43(b); a ratio > 1 for p != 0.5 means: with a field, Hamming balls are")
print("   NOT the extremal sets of the tail lemma relative to psi_0 = 0 -- the every-n form of the lemma is specific to the uniform measure)")
print()

# ------------------------------------------------------------------ TEST B
print("TEST B  uniform measure, site-dependent slopes u_i (weighted Hamming metric)")
print("  max{Phi(D): |D| <= m}  against balls {x: d_w(x,s) <= rho} of the weighted metric, m = the sizes of such balls")
rng = np.random.default_rng(20261126)
slope_sets = [(1.0, 1.0, 1.0, 1.0), (0.5, 1.0, 1.5, 2.0), (0.2, 0.2, 2.0, 2.0), (0.3, 0.6, 1.2, 2.4), (1.0, 1.0, 1.0, 3.0)]
slope_sets += [tuple(np.round(rng.uniform(0.2, 2.5, size=n), 3)) for _ in range(15)]
worstB = (1.0, None)
count_fail = 0
for slopes in slope_sets:
    dm = dist_matrix(slopes)
    phi = functional(dm, np.ones(N))
    wb = set()
    for s in range(N):
        for rho in sorted(set(np.round(dm[s], 12))):
            m = mask_of([x for x in range(N) if dm[s, x] <= rho + 1e-12])
            if 0 < m < (1 << N) - 1:
                wb.add(m)
    widx = np.array(sorted(wb)) - 1
    ratio, where = 1.0, None
    # thresholds: the sizes of the weighted balls (the analogue of "|D| <= |B(r)|"); comparing at other
    # sizes would be unfair to the balls
    for m in sorted(set(int(v) for v in size[widx])):
        top = phi[size <= m].max()
        bb = phi[widx][size[widx] <= m].max()
        if top / bb > ratio:
            ratio = top / bb
            k = np.flatnonzero(size <= m)[phi[size <= m].argmax()]
            where = (m, int(masks[k]), top, bb)
    line = f"  slopes={tuple(float(s) for s in slopes)}  max_m ratio to best weighted ball = {ratio:.6f}"
    if where is not None and ratio > 1 + 1e-9:
        m, mk, top, bb = where
        D = [x for x in range(N) if (mk >> x) & 1]
        line += f"   [m={m}: D={{{','.join(format(x, '04b') for x in D)}}}, Phi={top:.6f}, best ball {bb:.6f}]"
        count_fail += 1
    print(line)
    if ratio > worstB[0]:
        worstB = (ratio, slopes)
print(f"  RESULT B: weighted balls fail to be extremal for {count_fail} of {len(slope_sets)} slope vectors;"
      f" largest ratio {worstB[0]:.6f} at slopes {tuple(float(s) for s in worstB[1]) if worstB[1] is not None else None}")
print("  (the first vector, equal slopes, is the control and must give 1.000000)")
