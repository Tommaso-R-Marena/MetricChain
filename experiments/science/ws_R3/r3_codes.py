#!/usr/bin/env python3
"""R3 — own code, written before opening the author's scripts.

Linear codes over F_2 as lists of Python ints (bit i = coordinate i).

Checks for the "Codes" paragraph after Lemma 1 of INFERENCE_LIMITS.md:
  for every n and k there is a linear code C of length n, dual distance > k, |C| <= (2n)^ceil(k/2).

What is done here (exact, brute force):
  * narrow-sense primitive BCH codes of length n' = 2^m - 1, designed distance 2t+1, built from
    GF(2^m) arithmetic (generator polynomial = lcm of minimal polynomials of alpha^1..alpha^2t);
  * C := dual of BCH; restricted (punctured) to n coordinates; dual distance of the restriction
    computed by brute force (minimum weight of the dual of the punctured code);
  * the bound |C| <= (2n)^ceil(k/2) for all n <= NMAX and all k <= n (also the degenerate cases);
  * the improvement for odd k via the extended code (add an overall parity coordinate to BCH,
    i.e. C_ext = dual of extended BCH): dual distance >= 2t+2, |C_ext| <= 2 (n'+1)^t;
  * Rao's lower bound |C| >= M_t = sum_{j<=floor(k/2)} binom(n,j) for comparison.
"""
import itertools, math, sys, random

# ---------------------------------------------------------------- GF(2) linear algebra
def rref(rows):
    """Row-reduce a list of ints; return list of independent rows (reduced), pivots descending."""
    basis = []          # list of (pivot_bit, row)
    for r in rows:
        for p, b in basis:
            if r >> p & 1:
                r ^= b
        if r:
            p = r.bit_length() - 1
            # reduce existing rows
            basis = [(q, (c ^ r) if (c >> p & 1) else c) for q, c in basis]
            basis.append((p, r))
    basis.sort(reverse=True)
    return [b for _, b in basis]

def dual_basis(basis, n):
    """Basis of the dual code of span(basis) in F_2^n."""
    basis = rref(basis)
    pivots = [b.bit_length() - 1 for b in basis]
    piv = set(pivots)
    free = [i for i in range(n) if i not in piv]
    out = []
    for f in free:
        v = 1 << f
        for p, b in zip(pivots, basis):
            if b >> f & 1:
                v |= 1 << p
        out.append(v)
    return out

def span(basis):
    """All codewords (list of ints) of span(basis) — Gray-code enumeration."""
    words = [0]
    for b in basis:
        words += [w ^ b for w in words]
    return words

def min_weight(basis, cap=None):
    """Minimum nonzero weight of span(basis) (brute force); math.inf for the zero code."""
    if not basis:
        return math.inf
    best = math.inf
    w = 0
    k = len(basis)
    # Gray code walk
    for i in range(1, 1 << k):
        w ^= basis[(i & -i).bit_length() - 1]
        c = w.bit_count()
        if c < best:
            best = c
            if cap is not None and best <= cap:
                return best
    return best

def puncture(basis, coords):
    """Restrict codewords to the listed coordinates (in the given order) -> new basis (rref)."""
    out = []
    for b in basis:
        v = 0
        for j, c in enumerate(coords):
            if b >> c & 1:
                v |= 1 << j
        out.append(v)
    return rref(out)

# ---------------------------------------------------------------- GF(2^m) and BCH codes
PRIM = {2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101, 6: 0b1000011, 7: 0b10001001}

def gf_tables(m):
    n = (1 << m) - 1
    exp = [0] * (2 * n)
    log = [0] * (n + 1)
    x = 1
    for i in range(n):
        exp[i] = x
        log[x] = i
        x <<= 1
        if x >> m & 1:
            x ^= PRIM[m]
    for i in range(n, 2 * n):
        exp[i] = exp[i - n]
    return exp, log

def poly_mul_gf(a, b, exp, log, n):
    """Polynomials with coefficients in GF(2^m), lists low->high."""
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] ^= exp[log[x] + log[y]]
    return out

def bch_generator(m, t):
    """Generator polynomial (int, bit i = coeff of x^i) of the narrow-sense primitive BCH code
    of length 2^m-1 with zeros alpha^1..alpha^{2t}.  If the zeros cover all of Z_n the generator
    is x^n - 1 and the code is {0}."""
    n = (1 << m) - 1
    exp, log = gf_tables(m)
    zeros = set()
    for i in range(1, 2 * t + 1):
        j = i % n
        while j not in zeros:
            zeros.add(j)
            j = (2 * j) % n
    g = [1]
    for z in sorted(zeros):
        g = poly_mul_gf(g, [exp[z], 1], exp, log, n)
    assert all(c in (0, 1) for c in g), "generator not over F_2"
    gi = 0
    for i, c in enumerate(g):
        if c:
            gi |= 1 << i
    return gi, len(zeros)

def bch_basis(m, t):
    n = (1 << m) - 1
    g, deg = bch_generator(m, t)
    return [g << i for i in range(n - deg)], n

def bch_dual(m, t):
    """C = dual of the BCH code: length n' = 2^m - 1, |C| = 2^deg(g) <= 2^{mt}."""
    basis, n = bch_basis(m, t)
    return dual_basis(basis, n), n

def bch_ext_dual(m, t):
    """C_ext = dual of the extended BCH code (overall parity bit appended): length 2^m."""
    basis, n = bch_basis(m, t)
    ext = [b | ((b.bit_count() & 1) << n) for b in basis]
    return dual_basis(ext, n + 1), n + 1

def golay24():
    """Extended binary Golay code [24,12,8] from the cyclic [23,12,7] code with generator
    x^11+x^10+x^6+x^5+x^4+x^2+1, plus overall parity."""
    g = 0b110001110101
    basis23 = [g << i for i in range(12)]
    return [b | ((b.bit_count() & 1) << 23) for b in basis23]

def rm(r, m):
    """Reed-Muller code RM(r,m): evaluations of monomials of degree <= r on F_2^m."""
    n = 1 << m
    rows = []
    for deg in range(r + 1):
        for S in itertools.combinations(range(m), deg):
            v = 0
            for x in range(n):
                if all(x >> i & 1 for i in S):
                    v |= 1 << x
            rows.append(v)
    return rref(rows)

def weight_distribution(basis, n):
    """Exact weight distribution of span(basis) (numpy enumeration; dim <= ~24)."""
    import numpy as np
    words = np.zeros(1, dtype=np.uint64)
    for b in basis:
        words = np.concatenate([words, words ^ np.uint64(b)])
    cnt = np.bincount(np.bitwise_count(words).astype(np.int64), minlength=n + 1)
    return [int(c) for c in cnt]

def krawtchouk(n, j, d):
    return sum((-1) ** i * math.comb(d, i) * math.comb(n - d, j - i) for i in range(0, j + 1))

def dual_distance(C, D, n):
    """Minimum nonzero weight of the dual D of C, exactly."""
    if len(D) == 0:
        return math.inf
    if len(D) <= len(C):
        A = weight_distribution(D, n)
        return next(j for j in range(1, n + 1) if A[j])
    A = weight_distribution(C, n)
    size = 1 << len(C)
    for j in range(1, n + 1):
        Bj = sum(A[i] * krawtchouk(n, j, i) for i in range(n + 1))
        assert Bj % size == 0 and Bj >= 0
        if Bj:
            return j
    return math.inf

def binom_sum(n, t):
    return sum(math.comb(n, j) for j in range(t + 1))

# ---------------------------------------------------------------- the checks
def main():
    random.seed(1)
    print("== BCH codes: parameters, true minimum distance, dual sizes")
    for m in (3, 4, 5):
        npr = (1 << m) - 1
        for t in range(1, (npr + 1) // 2 + 1):
            basis, n = bch_basis(m, t)
            dim = len(basis)
            d = min_weight(basis) if dim <= 22 else None
            assert dim >= n - m * t or dim == 0, (m, t, dim)
            if dim > 0 and d is not None:
                assert d >= min(2 * t + 1, n), (m, t, d)
            print(f"  m={m} n'={npr} t={t}: BCH dim={dim} (>= n'-mt={n - m * t}), "
                  f"d_min={d}, |C|=|dual|=2^{n - dim} <= (n'+1)^t=2^{m * t}: {n - dim <= m * t}")

    print("== Claim: for every n, k: linear C of length n, dual distance > k, |C| <= (2n)^ceil(k/2)")
    NMAX = 31
    worst = 0.0
    nfail = 0
    for n in range(1, NMAX + 1):
        m = max(1, math.ceil(math.log2(n + 1)))
        if (1 << m) - 1 < n:
            m += 1
        for k in range(0, n + 1):
            t = (k + 1) // 2
            if m == 1:           # n = 1: C = F_2 for k >= 1
                size_log2, dd = (1 if k >= 1 else 0), math.inf if k >= 1 else 1
                ok = (2 ** size_log2 <= (2 * n) ** t) and dd > k
            else:
                if t == 0:
                    C = []
                else:
                    C, npr = bch_dual(m, t)
                # (i) first n coordinates, (ii) a random n-subset
                ok = True
                for trial in range(2):
                    coords = list(range(n)) if trial == 0 else sorted(random.sample(range((1 << m) - 1), n))
                    Cp = puncture(C, coords)
                    D = dual_basis(Cp, n)
                    # exact dual distance: brute force on the dual if it is small, otherwise
                    # MacWilliams transform of the (small) weight distribution of C itself
                    dd = dual_distance(Cp, D, n)
                    size_ok = (1 << len(Cp)) <= (2 * n) ** t
                    if not (dd > k and size_ok):
                        ok = False
                        print("  FAIL", n, k, t, len(Cp), dd)
                    worst = max(worst, len(Cp) * math.log(2) - t * math.log(2 * n))
            nfail += (not ok)
    print(f"  n <= {NMAX}, all k <= n, two coordinate choices each: failures = {nfail}; "
          f"max of ln|C| - ceil(k/2) ln(2n) = {worst:.3f} (<= 0 means the bound holds)")

    print("== Odd k: extended-BCH duals have dual distance >= 2t+2 > k = 2t+1 and size <= 2 (2^m)^t")
    for m in (3, 4, 5):
        for t in (1, 2, 3):
            if 2 * t + 2 > (1 << m):
                continue
            C, n = bch_ext_dual(m, t)
            D = dual_basis(C, n)
            dd = min_weight(D) if len(D) <= 22 else None
            k = 2 * t + 1
            print(f"  m={m} t={t}: length {n}, |C_ext|=2^{len(C)} (<= 2*{n}^{t}=2^{1 + m * t}), dual distance={dd} "
                  f"(> k={k}: {dd is None or dd > k}); note's bound (2n)^ceil(k/2) = {(2 * n) ** (t + 1)}; "
                  f"Rao M_t = {binom_sum(n, t)}")

    print("== Codes used later")
    G = golay24()
    Gd = dual_basis(G, 24)
    print("  Golay24: dim", len(rref(G)), "min weight", min_weight(G), "dual dim", len(Gd),
          "dual min weight", min_weight(Gd), "-> k = 7; (2n)^4 =", 48 ** 4, "; M_3 =", binom_sum(24, 3))
    C, n = bch_dual(4, 2)
    print("  dual of BCH(15,t=2): dim", len(C), "min weight", min_weight(C), "dual distance",
          min_weight(dual_basis(C, n)), "-> k = 4; (2n)^2 =", (2 * n) ** 2, "; M_2 =", binom_sum(n, 2))
    C, n = bch_dual(5, 2)
    print("  dual of BCH(31,t=2): dim", len(C), "min weight", min_weight(C), "dual distance",
          min_weight(dual_basis(C, n)), "-> k = 4; (2n)^2 =", (2 * n) ** 2, "; M_2 =", binom_sum(n, 2))
    C, n = bch_dual(5, 3)
    print("  dual of BCH(31,t=3): dim", len(C), "min weight", min_weight(C), "dual distance",
          min_weight(dual_basis(C, n)), "-> k = 6; (2n)^3 =", (2 * n) ** 3, "; M_3 =", binom_sum(n, 3))

    print("== Puncturing can destroy the MINIMUM distance of C (not used in the note, but needed")
    print("   for any argument that wants the basins of nu_{C,b} to be distinguishable):")
    C, n = bch_dual(4, 1)        # simplex [15,4,8]
    c0 = rref(C)[0]
    zero_set = [i for i in range(n) if not (c0 >> i & 1)]            # 7 coordinates
    one_set = [i for i in range(n) if (c0 >> i & 1)]
    coords = zero_set + one_set[:1]                                   # n = 8 = 2^{m-1}
    Cp = puncture(C, coords)
    print("  simplex[15,4,8] restricted to 8 coordinates (zero set of a word + 1): dim", len(Cp),
          "min weight", min_weight(Cp), "dual distance", min_weight(dual_basis(Cp, len(coords))))

if __name__ == "__main__":
    main()
