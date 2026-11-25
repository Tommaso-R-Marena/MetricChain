#!/usr/bin/env python3
"""R3 — independent check of Theorem 3 (basin bound) of INFERENCE_LIMITS.md.

Own formulation.  For a centre a, the largest value of mu(B(a,r)) over ALL probability
measures mu on {0,1}^n with uniform marginals of order <= k is a linear programme in the
distance distribution p_d = mu(d_H(x,a) = d):

    maximise  sum_{d<=r} p_d   s.t.   sum_d p_d K_j(d) = 0  (j = 1..k),  sum_d p_d = 1,  p >= 0

(symmetrise mu over the stabiliser of a: the constraints and the objective are invariant; a
measure that is invariant under coordinate permutations around a has Fourier coefficients
E chi_T = E K_|T|(d)/binom(n,|T|)).  So the EXACT answer is computable for every n, k, r, and
Theorem 3 is one dual-feasible point of this LP (the polynomial F_t^2 / min F_t^2).

Checks:
  1. exact integer arithmetic: f(x) = F_t(d(x,a)), E f^2 = M_t under k-wise uniformity
     (as an identity of Krawtchouk expansions: F_t^2 = M_t + sum_{1<=j<=2t} c_j K_j);
     F_t(d) = K_t^{(n-1)}(d-1) for d >= 1 (so positivity of F_t <=> below the first root);
  2. bound vs exact LP vs attained (Unif(C), nu_{C,b}) on Golay24 (k=7), dual-BCH [15,8] (k=4),
     [31,10] (k=4), [31,15] (k=6), RM(1,5) (k=3) — all centres through coset tables where feasible;
  3. the asymptotic statement  bound * n^t (1-2rho)^{2t} / t! -> 1;
  4. comparison with the textbook 2t-th moment bound  (2t-1)!! / (n^t (1-2 rho)^{2t}).
"""
import math, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from r3_codes import golay24, bch_dual, bch_ext_dual, rref, span, rm, dual_basis, weight_distribution

def K(n, j, d):
    return sum((-1) ** i * math.comb(d, i) * math.comb(n - d, j - i) for i in range(0, j + 1))

def F(n, t, d):
    return sum(K(n, j, d) for j in range(t + 1))

def M(n, t):
    return sum(math.comb(n, j) for j in range(t + 1))

def thm3_bound(n, t, r):
    """M_t / min_{d<=r} F_t(d)^2 as an exact Fraction (None if F_t vanishes on [0,r])."""
    vals = [F(n, t, d) for d in range(r + 1)]
    m = min(v * v for v in vals)
    pos = all(v > 0 for v in vals)
    return (Fraction(M(n, t), m) if m else None), pos

def lp_exact_ball(n, k, r):
    """max mu(B(a,r)) over k-wise uniform measures: LP in the distance distribution."""
    c = np.zeros(n + 1); c[: r + 1] = -1.0
    A = np.zeros((k + 1, n + 1)); b = np.zeros(k + 1)
    A[0, :] = 1.0; b[0] = 1.0
    for j in range(1, k + 1):
        cj = math.comb(n, j)
        A[j, :] = [K(n, j, d) / cj for d in range(n + 1)]
    res = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * (n + 1), method="highs")
    assert res.status == 0, res.message
    return -res.fun, res.x

def check_identities():
    print("== 1. identities (exact integers)")
    ok1 = ok2 = True
    for n in (5, 8, 13, 24, 31):
        for t in range(0, 5):
            if 2 * t > n:
                continue
            # expansion of F_t^2 in the Krawtchouk basis: constant term = 2^-n sum_d binom(n,d) F_t(d)^2
            c0 = Fraction(sum(math.comb(n, d) * F(n, t, d) ** 2 for d in range(n + 1)), 2 ** n)
            ok1 &= (c0 == M(n, t))
            # degree of F_t^2 is 2t, so it is orthogonal to K_j for j > 2t
            for j in range(2 * t + 1, n + 1):
                s = sum(math.comb(n, d) * F(n, t, d) ** 2 * K(n, j, d) for d in range(n + 1))
                ok1 &= (s == 0)
            for d in range(1, n + 1):
                ok2 &= (F(n, t, d) == K(n - 1, t, d - 1))
    print(f"   E_unif F_t^2 = M_t and F_t^2 has Krawtchouk degree 2t: {ok1};  F_t(d) = K_t^(n-1)(d-1): {ok2}")
    # direct brute-force of E_mu f^2 = M_t on a k-wise uniform measure that is NOT C-invariant:
    # a random convex combination of uniform measures on cosets of two different codes
    n = 15
    C1, _ = bch_dual(4, 2)
    C2 = [((c << 1) | (c >> 14)) & 0x7FFF for c in C1]          # cyclic shift: same code (cyclic)
    perm = list(range(n)); rng = np.random.default_rng(3); rng.shuffle(perm)
    C3 = []
    for c in C1:
        v = 0
        for i in range(n):
            if c >> i & 1:
                v |= 1 << perm[i]
        C3.append(v)
    mu = np.zeros(1 << n)
    for C, wgt in ((C1, 0.3), (C3, 0.7)):
        words = np.array(span(rref(C)), dtype=np.int64)
        shift = int(rng.integers(0, 1 << n))
        mu[words ^ shift] += wgt / len(words)
    x = np.arange(1 << n, dtype=np.uint64)
    worst = 0.0
    for a in rng.integers(0, 1 << n, size=20):
        d = np.bitwise_count(x ^ np.uint64(a)).astype(np.int64)
        for t in (1, 2):
            Ft = np.array([F(n, t, dd) for dd in range(n + 1)], dtype=float)
            worst = max(worst, abs(float(mu @ (Ft[d] ** 2)) - M(n, t)))
    print(f"   mixture of cosets of two different [15,8] codes (4-wise uniform, not invariant under one code): "
          f"max |E f^2 - M_t| over 20 centres, t=1,2: {worst:.2e}")

def code_report(name, C, n, k, bs=(2.0, 4.0), all_centres=True):
    t = k // 2
    R = rref(C)
    A = weight_distribution(R, n)
    size = 1 << len(R)
    print(f"== {name}: n={n}, |C|={size}, k={k}, t={t}, M_t={M(n, t)}, Rao: |C| >= M_t: {size >= M(n, t)}")
    print("    r | F_t>0 | Thm3 bound | exact LP max | Unif(C) at a codeword | "
          + " | ".join(f"nu_(C,b={b}) at codeword" for b in bs) + " | moment bound")
    for r in range(0, n // 2 + 1):
        bd, pos = thm3_bound(n, t, r)
        lp, _ = lp_exact_ball(n, k, r)
        att_inf = sum(A[: r + 1]) / size
        atts = []
        for b in bs:
            sig = 1 / (1 + math.exp(-b))
            # d(x,a) for x ~ P_{a'}, d(a,a') = w : Bin(w, sig) + Bin(n-w, 1-sig)
            tot = 0.0
            for w in range(n + 1):
                if A[w] == 0:
                    continue
                p1 = np.array([math.comb(w, i) * sig ** i * (1 - sig) ** (w - i) for i in range(w + 1)])
                p2 = np.array([math.comb(n - w, i) * (1 - sig) ** i * sig ** (n - w - i) for i in range(n - w + 1)])
                conv = np.convolve(p1, p2)
                tot += A[w] * conv[: r + 1].sum()
            atts.append(tot / size)
        # textbook moment bound: E (sum Y)^{2t} / (n-2r)^{2t} with the exact 2t-th moment of a
        # Rademacher sum (valid if n - 2r > 0)
        if n - 2 * r > 0 and t >= 1:
            mom = sum(math.comb(n, d) * (n - 2 * d) ** (2 * t) for d in range(n + 1)) / 2 ** n
            mb = mom / (n - 2 * r) ** (2 * t)
        else:
            mb = float("nan")
        bdf = float(bd) if bd is not None else float("inf")
        flag = "" if (att_inf <= lp + 1e-9 and lp <= bdf + 1e-9) else "  <-- ORDER VIOLATED"
        print(f"   {r:2d} | {str(pos):5s} | {bdf:10.6f} | {lp:10.6f} | {att_inf:10.6f} | "
              + " | ".join(f"{a:10.6f}" for a in atts) + f" | {mb:10.6f}{flag}")
    return A

def all_centres_check(name, C, n, k):
    """max over ALL centres a and all radii of mu(B(a,r)) / bound, for Unif(C) and exp-weights."""
    from r3_thm2 import coset_distance_table
    t = k // 2
    reps, counts, free, piv, words = coset_distance_table(C, n)
    size = len(words)
    worst = 0.0; arg = None
    cum = np.cumsum(counts, axis=1)                 # #codewords within distance r of the coset rep
    for r in range(0, n // 2 + 1):
        bd, pos = thm3_bound(n, t, r)
        if bd is None:
            continue
        att = cum[:, r].max() / size                # Unif(C)(B(a,r)) maximised over a
        ratio = att / float(bd)
        if ratio > worst:
            worst, arg = ratio, r
        assert att <= float(bd) + 1e-12, (name, r, att, float(bd))
    print(f"   [{name}] Unif(C), ALL centres (every coset), all radii <= n/2: max attained/bound = {worst:.4f} at r = {arg}")

def asymptotics():
    print("== 3./4. asymptotics: bound * n^t (1-2rho)^(2t) / t!  (should tend to 1), and the moment bound's constant")
    for t in (1, 2, 3):
        for rho in (0.1, 0.3, 0.45):
            row = []
            for n in (100, 1000, 10000, 100000):
                r = int(rho * n)
                # min over d<=r of F_t(d): F_t is decreasing on [0, first root); verify monotone by sampling
                Fr = F(n, t, r)
                samples = [F(n, t, d) for d in sorted(set([0, 1, r // 3, r // 2, max(r - 1, 0), r]))]
                assert all(s >= Fr for s in samples) and Fr > 0, (n, t, rho, samples)
                bd = Fraction(M(n, t), Fr * Fr)
                row.append(float(bd) * n ** t * (1 - 2 * r / n) ** (2 * t) / math.factorial(t))
            dbl = math.prod(range(1, 2 * t, 2))
            print(f"   t={t} rho={rho}: " + " ".join(f"{v:.4f}" for v in row)
                  + f"   | (2t-1)!!/t! = {dbl / math.factorial(t):.3f} (factor by which the moment bound is weaker)")

def odd_k():
    print("== odd k: with the extended code the bound of Theorem 3 is attained up to a constant as well")
    for m in (4, 5, 6):
        C, n = bch_ext_dual(m, 1)                  # RM(1,m): k = 3, t = 1
        size = 1 << len(rref(C))
        print(f"   RM(1,{m}): n={n}, k=3, t=1: 1/|C| = 1/{size}, Rao bound 1/M_1 = 1/{M(n, 1)}, "
              f"note's construction would have |C| <= (2n)^2 = {(2 * n) ** 2}")

if __name__ == "__main__":
    check_identities()
    C, n = bch_dual(4, 2)
    code_report("dual BCH(15,2) [15,8,4]", C, n, 4)
    all_centres_check("[15,8,4]", C, n, 4)
    G = golay24()
    code_report("extended Golay [24,12,8]", G, 24, 7)
    all_centres_check("Golay24", G, 24, 7)
    C, n = bch_dual(5, 2)
    code_report("dual BCH(31,2) [31,10,12]", C, n, 4)
    C, n = bch_dual(5, 3)
    code_report("dual BCH(31,3) [31,15,8]", C, n, 6)
    C, n = bch_ext_dual(5, 1)
    code_report("RM(1,5) [32,6,16] (odd k = 3)", C, n, 3)
    asymptotics()
    odd_k()
