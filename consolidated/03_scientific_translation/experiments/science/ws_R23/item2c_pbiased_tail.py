#!/usr/bin/env python3
"""R23 Item 2(c) — own code, written before opening the audit's script s1_tail_lemma_beyond_uniform.py.

Claim checked (synthesis §6 fourth bullet; AA2 Entry 1, l.101-108): on Q_4 with pi = Bernoulli(p)^{x4} and all
65 534 nonempty proper subsets D, the tail functional
        T(D) = sum_{x in D} pi(x) ( exp(u * dist(x, D^c)) - 1 )            (Hamming distance to the complement)
is NOT maximised by Hamming balls among the sets of at most the measure of a ball: "the maximum over
pi(D) <= pi(ball) exceeds the best Hamming ball by the factor 2.08 at (p,u) = (0.2, 2) (1.42 at (0.3, 4);
exactly 1 at p = 1/2, the control)".

Lemma 11.43(b) of the theory report (uniform measure): |D| <= |B(r)|  =>  T(D) <= T(B(r)), equality for balls.
The p-biased analogue has several possible readings; this script computes all of them (definitions below) for
a grid of (p, u), exhaustively over the 65 534 subsets, in exact rational arithmetic for the measures
(comparisons pi(D) <= pi(B) are exact) and floating point for exp(u*.).

  Xi(q)      = max { T(D) : D proper nonempty, pi(D) <= q }
  balls      = all Hamming balls B(c, r), any centre c in Q_4, radius 0 <= r <= 3 with B != Q_4
  ratio_A    = max over balls B of  Xi(pi(B)) / max{ T(B') : B' a ball (any centre), pi(B') <= pi(B) }
               ("the maximum over pi(D) <= pi(ball) against the best Hamming ball of at most that measure")
  ratio_B    = max over balls B of  Xi(pi(B)) / T(B)        (the verbatim analogue of the lemma: a ball of the
               given measure is extremal)
  ratio_C    = max over ALL sets D of  T(D) / max{ T(B') : B' a ball, pi(B') <= pi(D) }
               (every set is dominated by some ball of at most its measure)
  ratio_A0   = as ratio_A but with balls centred at 0000 or 1111 only (threshold sets of the type)
Control: p = 1/2 must give ratio_A = ratio_B = ratio_C = 1 (Harper).  Second control: the uniform-measure
lemma itself, |D| <= |B(r)| => T(D) <= T(B(r)), checked for all subsets (violations must be 0), and a
deliberately false variant (radius r-1 on the right) must be violated.
Run:  OMP_NUM_THREADS=1 python3 -I -B item2c_pbiased_tail.py      (about 1 minute)
"""
import math, time, itertools
from fractions import Fraction
import numpy as np
t0 = time.time()
n = 4; N = 1 << n
pc = [bin(i).count("1") for i in range(N)]
hd = [[pc[a ^ b] for b in range(N)] for a in range(N)]
FULL = (1 << N) - 1

# dist(x, D^c) for every subset D (bitmask over the 16 points) and x in D
t_setup = time.time()
subsets = np.arange(1, FULL, dtype=np.int64)             # 65 534 nonempty proper subsets
assert len(subsets) == 65534
member = ((subsets[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)     # (65534, 16)
HD = np.array(hd)
# dist to complement: min over y not in D of hd(x,y)
big = 99
distc = np.full((len(subsets), N), big, dtype=np.int64)
for y in range(N):
    notin = ~member[:, y]
    cand = np.where(notin[:, None], HD[y][None, :], big)
    distc = np.minimum(distc, cand)
distc = np.where(member, distc, 0)                      # 0 for x not in D
assert distc.max() <= n and (distc[member] >= 1).all()

# balls
balls = {}
for c in range(N):
    for r in range(0, n):
        mask = 0
        for x in range(N):
            if hd[c][x] <= r: mask |= 1 << x
        if mask != FULL: balls[(c, r)] = mask
ball_masks = sorted(set(balls.values()))
ball_idx = np.array([m - 1 for m in ball_masks])        # index into subsets (subset value m is at index m-1)
ball_idx0 = np.array([balls[(c, r)] - 1 for c in (0, N - 1) for r in range(n) if (c, r) in balls])
print(f"subsets: {len(subsets)}; distinct Hamming balls != Q_4: {len(ball_masks)}; balls centred at 0000/1111: {len(ball_idx0)}")

def run(p_frac, u):
    p = float(p_frac)
    pi = np.array([p ** pc[x] * (1 - p) ** (n - pc[x]) for x in range(N)])
    # exact measures as integers: numerator of pi(x) with common denominator
    den = p_frac.denominator ** n
    pi_int = np.array([(p_frac.numerator ** pc[x]) * ((p_frac.denominator - p_frac.numerator) ** (n - pc[x])) for x in range(N)], dtype=np.int64)
    mu_int = member.astype(np.int64) @ pi_int             # exact pi(D) * den
    T = ((np.exp(u * distc) - 1.0) * member) @ pi
    # Xi as a function of the exact measure: sort by measure, running maximum
    order = np.argsort(mu_int, kind="stable")
    mu_sorted = mu_int[order]; T_sorted = T[order]
    runmax = np.maximum.accumulate(T_sorted)
    def Xi(q_int):
        k = np.searchsorted(mu_sorted, q_int, side="right")   # sets with measure <= q
        return runmax[k - 1], order[np.argmax(T_sorted[:k])]
    def best_ball(q_int, idx):
        ok = idx[mu_int[idx] <= q_int]
        return T[ok].max() if len(ok) else 0.0
    rA = rB = rA0 = 0.0; argA = None
    for bi in ball_idx:
        xi, arg = Xi(mu_int[bi])
        a = xi / best_ball(mu_int[bi], ball_idx)
        if a > rA: rA, argA = a, (int(subsets[bi]), int(subsets[arg]))
        rB = max(rB, xi / T[bi])
    for bi in ball_idx0:
        xi, arg = Xi(mu_int[bi])
        rA0 = max(rA0, xi / best_ball(mu_int[bi], ball_idx0))
    # ratio_C over all sets: best ball of at most the measure of D
    bm = mu_int[ball_idx]; bT = T[ball_idx]
    o = np.argsort(bm, kind="stable"); bm_s = bm[o]; bT_run = np.maximum.accumulate(bT[o])
    k = np.searchsorted(bm_s, mu_int, side="right")
    assert (k >= 1).all()                               # every set contains a point; its singleton is a ball of smaller measure? not nec. -> checked
    rC = float((T / bT_run[k - 1]).max())
    return rA, rB, rC, rA0, argA

def fmt_set(mask):
    return "{" + ",".join(format(x, "04b") for x in range(N) if (mask >> x) & 1) + "}"

print("    p      u    ratio_A   ratio_B   ratio_C   ratio_A0   (argmax of ratio_A: ball -> maximising set)")
grid_p = [Fraction(1, 2), Fraction(2, 5), Fraction(3, 10), Fraction(1, 5), Fraction(1, 10)]
grid_u = [0.5, 1.0, 2.0, 4.0]
res = {}
for pf in grid_p:
    for u in grid_u:
        rA, rB, rC, rA0, argA = run(pf, u)
        res[(pf, u)] = (rA, rB, rC, rA0)
        print(f"  {float(pf):5.2f}  {u:4.1f}   {rA:8.4f}  {rB:8.4f}  {rC:8.4f}  {rA0:8.4f}    {fmt_set(argA[0])} -> {fmt_set(argA[1])}")
viol = 0
# control p = 1/2
c_bad = sum(1 for u in grid_u for v in res[(Fraction(1, 2), u)][:3] if abs(v - 1) > 1e-12)
viol += c_bad
print(f"control p = 1/2: ratio_A = ratio_B = ratio_C = 1 for all u in the grid: violations = {c_bad}")
print(f"claim '2.08 at (p,u) = (0.2, 2)':   ratio_A = {res[(Fraction(1,5),2.0)][0]:.4f}   ratio_C = {res[(Fraction(1,5),2.0)][2]:.4f}")
print(f"claim '1.42 at (p,u) = (0.3, 4)':   ratio_A = {res[(Fraction(3,10),4.0)][0]:.4f}   ratio_C = {res[(Fraction(3,10),4.0)][2]:.4f}")
mx = max(v[0] for v in res.values()); mxk = [k for k, v in res.items() if v[0] == mx][0]
print(f"largest ratio_A on the grid: {mx:.4f} at (p,u) = ({float(mxk[0])}, {mxk[1]})")
nonextremal = sum(1 for k, v in res.items() if k[0] != Fraction(1, 2) and v[0] > 1 + 1e-9)
print(f"grid points with p != 1/2 at which balls are not extremal (ratio_A > 1): {nonextremal} of {len(grid_u)*(len(grid_p)-1)}")

# second control: the uniform lemma itself for all subsets
pi_u = np.full(N, 1.0 / N)
bad_lemma = 0; bad_false = 0
for u in grid_u:
    T = ((np.exp(u * distc) - 1.0) * member) @ pi_u
    size = member.sum(axis=1)
    for r in range(0, n):
        Bsize = sum(math.comb(n, j) for j in range(r + 1))
        TB = T[balls[(0, r)] - 1]
        bad_lemma += int((T[size <= Bsize] > TB * (1 + 1e-12)).sum())
        if r >= 1:
            TBm = T[balls[(0, r - 1)] - 1]
            bad_false += int((T[size <= Bsize] > TBm * (1 + 1e-12)).sum())
viol += bad_lemma + int(bad_false == 0)
print(f"control (Lemma 11.43(b), uniform measure, all subsets, r=0..3, four slopes): violations = {bad_lemma}")
print(f"negative control (the same with the ball of radius r-1 on the right must fail): number of failures = {bad_false} (violation of the control if 0)")
print(f"TOTAL violations: {viol}")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item2c_pbiased_tail")
