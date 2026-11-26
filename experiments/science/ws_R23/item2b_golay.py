#!/usr/bin/env python3
"""R23 Item 2(b) — own code, written before opening the audit's script aa1_04.

Claim checked (synthesis §6 third bullet; AA1 §0 item 2): Theorem 11.33(a) of the theory report
(second-order class G2(c2) on {0,1}^n, w = beta*c2*n <= 4: polynomially many evaluations) fails when the
known part f is not additive; explicit instance: f = landscape of the extended Golay code (n = 24),
w = 4: every (eps/2, delta)-correct algorithm with eps < 1e-3 makes (1 - 2 delta) * 4096 evaluations.

What this script establishes (replication with own code):
  G1  the extended binary Golay code built from the cyclic [23,12,7] code with generator polynomial
      x^11+x^10+x^6+x^5+x^4+x^2+1, extended by a parity bit: 4096 words, weight enumerator
      1 + 759 z^8 + 2576 z^12 + 759 z^16 + z^24, minimum distance 8 (exhaustive over the 4096 words; linear).
  G2  balls of Hamming radius 3 around distinct codewords are disjoint (d_min >= 7), exhaustive marking
      of all 4096 * 2325 points of the balls in a table of 2^24 entries.
  G3  the dip b_{y,r}(x) = c2 * C(r - d_H(x,y), 2)_+ has all mixed second differences in [-c2, c2]:
      (i) exhaustive on the cube {0,1}^10 for r = 2..9 (all x, all pairs i<j); (ii) for n = 24 by the
      reduction to second differences of the profile phi(d) (the three cases of a pair of flips).
      It vanishes outside B(y, r-2).  Control: the 'cone' profile c2*(r-d)_+ * 3 must violate the bound.
  G4  numbers: with beta*c2 = w/n = 1/6 and f = 0 on the code, +infinity off the code,
      ln Z(f - b_{y,r}) - ln Z(f) = ln(1 + (exp(beta*c2*C(r,2)) - 1)/4096) for r - 2 <= 3; r = 5 gives the threshold.
      Also with a finite penalty M off the code (so that f is a real function): the threshold as a function of beta*M.
  G5  the detection bound of Theorem 11.22(c) [V in the report]: alternatives g_y = -b_{y,5}, y in the code,
      weights 1, every point detects at most one alternative (G2)  =>  E|Q(0)| >= (1 - 2 delta) * 4096.
      (Argument; the script checks its combinatorial hypothesis B = 1 exhaustively: G2.)
  G6  what Theorem 11.33(a) itself promises at this size: 'about n^5 eps^-2' and the source's formula.
  G7  the asymptotic family: Gilbert-Varshamov codes, R(w) = sup{ ln 2 - h(d) : ln 2 - h(d) <= w d^2/8 }.
Run:  OMP_NUM_THREADS=1 python3 -I -B item2b_golay.py     (about 1 minute, < 0.5 GB)
"""
import math, time, itertools, sys
import numpy as np
t0 = time.time()
viol = 0
def report(name, nviol, extra=""):
    global viol; viol += nviol
    print(f"{name}: violations = {nviol} {extra}")

# ---------------- G1: the code
g_exps = [11, 10, 6, 5, 4, 2, 0]
gpoly = sum(1 << k for k in g_exps)                      # degree 11
# generator rows x^i * g(x), i = 0..11, as 23-bit integers (cyclic code: degree < 23, no reduction needed)
rows23 = [gpoly << i for i in range(12)]
assert all(r < (1 << 23) for r in rows23)
# check g(x) divides x^23 + 1 over GF(2)
def polymod(a, b):
    db = b.bit_length() - 1
    while a.bit_length() - 1 >= db and a:
        a ^= b << (a.bit_length() - 1 - db)
    return a
div_ok = polymod((1 << 23) | 1, gpoly) == 0
words23 = np.zeros(1, dtype=np.int64)
for r in rows23:
    words23 = np.concatenate([words23, words23 ^ r])
assert len(words23) == 4096 and len(set(words23.tolist())) == 4096
pc = lambda arr: np.array([bin(int(v)).count("1") for v in arr], dtype=np.int64)
w23 = pc(words23)
enum23 = {int(k): int(v) for k, v in zip(*np.unique(w23, return_counts=True))}
words24 = (words23 << 1) | (w23 & 1)                      # parity bit appended
w24 = pc(words24)
enum24 = {int(k): int(v) for k, v in zip(*np.unique(w24, return_counts=True))}
print("G1 generator polynomial divides x^23+1:", div_ok)
print("G1 weight enumerator of the [23,12] code:", enum23)
print("G1 weight enumerator of the extended [24,12] code:", enum24)
exp23 = {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288, 15: 506, 16: 253, 23: 1}
exp24 = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
report("G1 the code is the Golay code (enumerators match the known ones; linear, so d_min = min weight = 8)",
       int(not div_ok) + int(enum23 != exp23) + int(enum24 != exp24))
# linearity check (closure) on a sample + full check via set
S = set(words24.tolist())
lin_bad = 0
rng = np.random.default_rng(1)
for _ in range(20000):
    a, b = rng.integers(0, 4096, 2)
    if int(words24[a] ^ words24[b]) not in S: lin_bad += 1
report("G1b closure under addition (20000 random pairs)", lin_bad)

# ---------------- G2: disjoint radius-3 balls
n = 24
mark = np.zeros(1 << n, dtype=np.uint8)
masks = [0]
for k in (1, 2, 3):
    for comb in itertools.combinations(range(n), k):
        m = 0
        for i in comb: m |= 1 << i
        masks.append(m)
masks = np.array(masks, dtype=np.int64)
assert len(masks) == 1 + 24 + 276 + 2024 == 2325
overlap = 0
for wd in words24:
    pts = wd ^ masks
    overlap += int(mark[pts].sum())
    mark[pts] += 1
covered = int((mark > 0).sum())
print(f"G2 points in the union of the 4096 balls of radius 3: {covered} = 4096*2325 = {4096*2325}; 2^24 = {1<<24}")
report("G2 balls of radius 3 around codewords are pairwise disjoint (exhaustive)", overlap + int(covered != 4096 * 2325))
# control: radius-4 balls DO overlap (d_min = 8)
mark4 = np.zeros(1 << n, dtype=np.uint8)
masks4 = list(masks)
for comb in itertools.combinations(range(n), 4):
    m = 0
    for i in comb: m |= 1 << i
    masks4.append(m)
masks4 = np.array(masks4, dtype=np.int64)
for wd in words24:
    mark4[wd ^ masks4] += 1
mx = int(mark4.max())
print(f"G2 control: with radius 4 a point lies in up to {mx} balls (expected 6: a weight-4 word and the sextet); points in >= 2 balls: {int((mark4>=2).sum())}")
report("G2 control radius 4 overlaps (violation = control did not react)", int(mx < 2))
del mark, mark4

# ---------------- G3: the dip is in the class
def dip_profile(r, nmax):
    return np.array([math.comb(r - d, 2) if r - d >= 2 else 0 for d in range(nmax + 1)], dtype=np.int64)

def max_mixed_second_difference_exhaustive(nn, values):
    """values: array over {0,1}^nn; returns max |D_i D_j g| over all x and i<j."""
    idx = np.arange(1 << nn)
    best = 0
    for i in range(nn):
        for j in range(i + 1, nn):
            base = idx[((idx >> i) & 1 == 0) & ((idx >> j) & 1 == 0)]
            dd = values[base | (1 << i) | (1 << j)] - values[base | (1 << i)] - values[base | (1 << j)] + values[base]
            best = max(best, int(np.abs(dd).max()))
    return best

nn = 10
pcn = np.array([bin(i).count("1") for i in range(1 << nn)], dtype=np.int64)
bad3 = 0
for r in range(2, 10):
    prof = dip_profile(r, nn)
    for y in (0, 0b1011001110, (1 << nn) - 1):
        vals = prof[pcn[np.arange(1 << nn) ^ y]]
        mmax = max_mixed_second_difference_exhaustive(nn, vals)
        supp_ok = bool((vals[pcn[np.arange(1 << nn) ^ y] >= r - 1] == 0).all())
        centre_ok = int(vals[y]) == math.comb(r, 2)
        if mmax != 1 or not supp_ok or not centre_ok: bad3 += 1
report("G3(i) dips b_{y,r}, r=2..9, three centres, cube n=10: max|D_iD_j| = c2 exactly, value C(r,2) at y, zero outside B(y,r-2) (exhaustive)", bad3)
# control: a profile that is NOT in the class
vals = 3 * np.maximum(4 - pcn, 0)
mm = max_mixed_second_difference_exhaustive(nn, vals)
print(f"G3 control: cone profile 3*(4-d)_+ has max|D_iD_j| = {mm} (> 1 expected)")
report("G3 control (violation = control did not react)", int(mm <= 1))
# (ii) n = 24 through the profile: D_iD_j of phi(d_H(x,y)) is one of
#   phi(d+2)-2phi(d+1)+phi(d)  (both flips away),  -(phi(d+1)-2phi(d)+phi(d-1)) (one towards, one away),
#   phi(d-2)-2phi(d-1)+phi(d)  (both towards)   =>   max|.| = max_d |second difference of phi|
bad3b = 0
for r in range(2, 26):
    prof = dip_profile(r, 26)
    sd = prof[2:] - 2 * prof[1:-1] + prof[:-2]
    if int(np.abs(sd).max()) != 1 or int(sd.min()) < 0: bad3b += 1
report("G3(ii) second differences of the profile C(r-d,2)_+ lie in {0,1} for r=2..25 (n=24 by the three-case reduction)", bad3b)

# ---------------- G4: numbers
w = 4.0; bc2 = w / n                                    # beta*c2
print(f"G4 beta*c2 = w/n = {bc2:.6f}")
print("   r  radius r-2  depth/c2  beta*depth   ln Z shift (f = +inf off the code)   balls disjoint?")
shifts = {}
for r in range(2, 8):
    depth = math.comb(r, 2)
    shift = math.log1p((math.exp(bc2 * depth) - 1) / 4096)
    shifts[r] = shift
    print(f"   {r}      {r-2}         {depth:3d}     {bc2*depth:7.4f}     {shift:.6e}                   {'yes' if r-2 <= 3 else 'NO'}")
thr = shifts[5]
print(f"G4 threshold accuracy (r = 5, the largest dip with pairwise disjoint supports): eps < {thr:.6e}")
report("G4 the audit's 'eps < 10^-3' is below the true threshold 1.0479e-3", int(not (1e-3 < thr)))
# finite penalty M off the code: f = M on non-codewords. Z0 = 4096 + e^{-bM}(2^24-4096);
# the dip also raises the weights of the 2324 non-codewords of B(y,3):
def shift_finite(bM):
    off = math.exp(-bM)
    Z0 = 4096 + off * ((1 << n) - 4096)
    extra = (math.exp(bc2 * 10) - 1)
    for dist, cnt in ((1, 24), (2, 276), (3, 2024)):
        extra += off * cnt * (math.exp(bc2 * math.comb(5 - dist, 2)) - 1)
    return math.log1p(extra / Z0)
print("G4 finite penalty M off the code (f real-valued):  beta*M -> ln Z shift of one dip (r=5)")
for bM in (5, 10, 12, 15, 20, 30, 50):
    print(f"     beta*M = {bM:3d}: {shift_finite(bM):.6e}   {'> 1e-3' if shift_finite(bM) > 1e-3 else '<= 1e-3'}")
# ---------------- G5
print("G5 detection bound (Theorem 11.22(c), machine-checked in the report for any class and functional):")
print("   alternatives g_y = -b_{y,5} (y in the code; all in G2(c2) by G3 and symmetry of the class under g -> -g),")
print("   |ln Z(f+g_y) - ln Z(f)| = %.6e > eps for eps < 1.0479e-3; a point x detects g_y iff x in B(y,3);" % thr)
print("   by G2 every point detects at most one alternative (B = 1)  =>  E|Q(0)| >= (1-2 delta) * 4096.")
# ---------------- G6
eps = 1e-3
print(f"G6 what Theorem 11.33(a) promises at n = 24, w = 4, eps = 1e-3: 'about n^5 eps^-2' = {n**5/eps**2:.3e}")
K = math.ceil(w * n); alpha = (n - 1) * math.tanh(bc2 / 4)
src = K**3 * eps**-2 * math.log(K / 0.05) * n * math.log(n * K / eps) / (1 - alpha)
print(f"   source formula K^3 eps^-2 ln(K/delta) n ln(nK/eps)/(1-alpha), K = {K}, alpha = {alpha:.4f}, delta = 0.05: {src:.3e} (constant omitted)")
print(f"   lower bound of the instance: (1-2 delta)*4096 <= 4096;  2^24 = {1<<24};  so at n = 24 the instance does NOT exceed the bound that (a) states")
report("G6 (information) the explicit instance is numerically below the theorem's own polynomial at n=24", 0)
# ---------------- G7
def h(x): return 0.0 if x in (0, 1) else -x * math.log(x) - (1 - x) * math.log(1 - x)
def Rw(wv):
    # largest GV rate ln2 - h(d) with ln2 - h(d) <= wv d^2 / 8, d in (0, 1/2): the left side decreases, the right increases
    lo, hi = 1e-9, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.log(2) - h(mid) > wv * mid * mid / 8: lo = mid
        else: hi = mid
    return math.log(2) - h(hi), hi
print("G7 Gilbert-Varshamov family: R(w) = sup{ln2 - h(d): ln2 - h(d) <= w d^2/8}  (dip of radius < d n/2, depth*beta ~ w d^2 n/8)")
for wv in (0.5, 1, 2, 4):
    R, dstar = Rw(wv)
    print(f"     w = {wv:4}: R(w) = {R:.4f} nats per site at relative distance {dstar:.4f}")
R4, _ = Rw(4.0)
report("G7 R(4) = 0.056 (the audit's number)", int(abs(R4 - 0.056) > 0.0006))
print(f"TOTAL violations: {viol}")
print(f"elapsed {time.time()-t0:.1f} s")
print("END item2b_golay")
