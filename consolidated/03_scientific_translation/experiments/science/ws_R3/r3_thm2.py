#!/usr/bin/env python3
"""R3 — independent check of Theorem 2 (invisible order) of INFERENCE_LIMITS.md on codes the
author did not use: the extended Golay code [24,12,8] (self-dual, k = 7), the dual of the
two-error-correcting BCH code of length 15 ([15,8], k = 4) and of length 31 ([31,10], k = 4).

Method (exact, own code):
  * nu_{C,b}(x) = |C|^-1 sum_{a in C} sigma^{n-d(x,a)} (1-sigma)^{d(x,a)} is evaluated on one
    representative per coset of C by direct summation over all codewords;
  * n <= 24: expanded to the whole cube; ALL Fourier coefficients computed by a fast
    Walsh-Hadamard transform, so marginal uniformity is checked on every subset of every order
    at once (no use of Lemma 1); cone inequalities checked on every (x, i);
  * spot check of the coset expansion against direct summation at random points;
  * entropy against the two ends of (c); the path b' in [0,b] of (e);
  * the variant mu ~ exp(-b d_H(x,C)) used by the author, on the same codes;
  * (d): entropy >= n h(sigma(b)) on random members of the class (small n) and an adversarial
    descent on n = 4.
"""
import math, sys, time
import numpy as np
from r3_codes import golay24, bch_dual, rref, dual_basis, span, min_weight

def h2(p):
    return 0.0 if p in (0.0, 1.0) else -p * math.log(p) - (1 - p) * math.log(1 - p)

def coset_reps(C, n):
    """A complement of span(C): vectors supported on the non-pivot coordinates of rref(C)."""
    R = rref(C)
    piv = {b.bit_length() - 1 for b in R}
    free = [i for i in range(n) if i not in piv]
    reps = np.zeros(1, dtype=np.uint64)
    for f in free:
        reps = np.concatenate([reps, reps | np.uint64(1 << f)])
    return reps, free, sorted(piv)

def coset_distance_table(C, n, chunk=1 << 13):
    """For every coset representative r: counts[r, w] = #{a in C : wt(r + a) = w}."""
    words = np.array(span(rref(C)), dtype=np.uint64)
    reps, free, piv = coset_reps(C, n)
    counts = np.zeros((len(reps), n + 1), dtype=np.int64)
    for s in range(0, len(reps), chunk):
        blk = reps[s:s + chunk]
        d = np.bitwise_count(blk[:, None] ^ words[None, :]).astype(np.int64)
        # row-wise bincount
        off = (np.arange(len(blk))[:, None] * (n + 1) + d).ravel()
        counts[s:s + len(blk)] = np.bincount(off, minlength=len(blk) * (n + 1)).reshape(len(blk), n + 1)
    return reps, counts, free, piv, words

def fwht_inplace(a):
    """Unnormalised Walsh-Hadamard transform over F_2^n (len(a) = 2^n)."""
    n = a.size.bit_length() - 1
    a = a.reshape([2] * n)
    for ax in range(n):
        lo = np.take(a, 0, axis=ax)
        hi = np.take(a, 1, axis=ax)
        s = lo + hi
        d = lo - hi
        idx0 = [slice(None)] * n; idx0[ax] = 0
        idx1 = [slice(None)] * n; idx1[ax] = 1
        a[tuple(idx0)] = s
        a[tuple(idx1)] = d
    return a.reshape(-1)

def full_cube_from_cosets(C, n, reps, vals_coset, free, piv):
    """Expand a function of the coset to the whole cube: x -> rep(x) by eliminating pivots."""
    R = rref(C)
    # index of a representative = its bits on the free coordinates, in the order of `free`
    # for x: reduce by rows of R according to pivot bits, then read off free bits.
    N = 1 << n
    x = np.arange(N, dtype=np.uint64)
    red = x.copy()
    for b in R:
        p = b.bit_length() - 1
        mask = ((red >> np.uint64(p)) & np.uint64(1)).astype(bool)
        red[mask] ^= np.uint64(b)
    idx = np.zeros(N, dtype=np.int64)
    for j, f in enumerate(free):
        idx |= (((red >> np.uint64(f)) & np.uint64(1)).astype(np.int64) << j)
    return vals_coset[idx]

def analyse(name, C, n, k, bs, do_full):
    print(f"=== {name}: n={n}, |C|=2^{len(rref(C))}, claimed order k={k}")
    t0 = time.time()
    reps, counts, free, piv, words = coset_distance_table(C, n)
    ncos = len(reps)
    assert ncos * len(words) == 1 << n
    print(f"  coset table: {ncos} cosets x {len(words)} words, {time.time() - t0:.1f}s; "
          f"covering radius = {int(np.max(np.argmax(counts > 0, axis=1)))}")
    dmin_coset = np.argmax(counts > 0, axis=1)             # d_H(x, C) on each coset
    for b in bs:
        sig = 1 / (1 + math.exp(-b)); tau = math.tanh(b / 2)
        pw = np.array([sig ** (n - w) * (1 - sig) ** w for w in range(n + 1)])
        nu_c = counts @ pw / len(words)                    # nu on a representative
        tot = nu_c.sum() * len(words)
        S = -len(words) * np.sum(nu_c * np.log(nu_c))
        lo, hi = n * h2(sig), n * h2(sig) + math.log(len(words))
        # variant: mu ~ exp(-b d(x,C))
        wv = np.exp(-b * dmin_coset); Zv = len(words) * wv.sum(); mu_c = wv / Zv
        Sv = -len(words) * np.sum(mu_c * np.log(mu_c))
        print(f"  b={b}: sum nu = {tot:.15f}; S(nu) = {S:.6f} in [{lo:.6f}, {hi:.6f}] -> "
              f"{lo - 1e-9 <= S <= hi + 1e-9};  S - n h = {S - lo:.4f} of ln|C| = {math.log(len(words)):.4f};"
              f"  n ln2 - S = {n * math.log(2) - S:.4f};  variant S = {Sv:.6f} (in range: {lo - 1e-9 <= Sv <= hi + 1e-9})")
        if do_full:
            for label, vc in (("nu_{C,b}", nu_c), ("exp(-b d(x,C))", mu_c)):
                full = full_cube_from_cosets(C, n, reps, vc, free, piv)
                # spot check against direct summation (mixture only)
                if label.startswith("nu"):
                    rng = np.random.default_rng(7)
                    xs = rng.integers(0, 1 << n, size=300, dtype=np.uint64)
                    d = np.bitwise_count(xs[:, None] ^ words[None, :]).astype(np.int64)
                    direct = pw[d].sum(axis=1) / len(words)
                    print(f"    [{label}] spot check vs direct summation at 300 random x: max rel err "
                          f"{np.max(np.abs(direct - full[xs.astype(np.int64)]) / direct):.2e}")
                # cone inequalities on all (x,i)
                a = full.reshape([2] * n)
                worst = 0.0
                for ax in range(n):
                    r = np.take(a, 1, axis=ax) / np.take(a, 0, axis=ax)
                    worst = max(worst, float(r.max()), float((1 / r).max()))
                # all Fourier coefficients
                F = fwht_inplace(full.copy())
                wt = np.bitwise_count(np.arange(1 << n, dtype=np.uint64)).astype(np.int64)
                mx = np.zeros(n + 1)
                np.maximum.at(mx, wt, np.abs(F))
                order = next((j for j in range(1, n + 1) if mx[j] > 1e-9), None)
                print(f"    [{label}] max single-flip ratio = {worst:.12f} vs e^b = {math.exp(b):.12f} "
                      f"(in class: {worst <= math.exp(b) * (1 + 1e-12)});")
                print(f"    [{label}] max |E chi_T| by order |T|=1..{min(n, k + 3)}: "
                      + " ".join(f"{mx[j]:.1e}" for j in range(1, min(n, k + 3) + 1))
                      + f"  -> first visible order = {order} (expected k+1 = {k + 1}; "
                      f"tau^(k+1) = {tau ** (k + 1):.3e})")
                del F, full
    # (e): the path b' in [0, b]
    b = bs[-1]
    grid = np.linspace(0, b, 41)
    Ss = []
    for bp in grid:
        sig = 1 / (1 + math.exp(-bp))
        pw = np.array([sig ** (n - w) * (1 - sig) ** w for w in range(n + 1)])
        nu_c = counts @ pw / len(words)
        Ss.append(-len(words) * np.sum(nu_c * np.log(nu_c)))
    Ss = np.array(Ss)
    print(f"  (e) path b' in [0,{b}]: S from {Ss[0]:.4f} (n ln 2 = {n * math.log(2):.4f}) down to {Ss[-1]:.4f}; "
          f"monotone decreasing: {bool(np.all(np.diff(Ss) < 1e-12))}")
    return counts

def random_class_member(n, b, rng):
    """A random function g on {0,1}^n with single-flip differences <= b: a random mixture of
    lower/upper envelopes of random anchor values (McShane), which are b-Lipschitz."""
    N = 1 << n
    x = np.arange(N, dtype=np.uint64)
    kind = rng.integers(0, 4)
    m = int(rng.integers(1, 6))
    anchors = rng.integers(0, N, size=m, dtype=np.uint64)
    d = np.bitwise_count(x[:, None] ^ anchors[None, :]).astype(float)
    vals = rng.normal(0, b * n / 3, size=m)
    if kind == 0:
        g = np.min(vals[None, :] + b * d, axis=1)
    elif kind == 1:
        g = np.max(vals[None, :] - b * d, axis=1)
    elif kind == 2:
        lam = rng.random()
        g = lam * np.min(vals[None, :] + b * d, axis=1) + (1 - lam) * np.max(vals[None, :] - b * d, axis=1)
    else:   # additive with extreme slopes plus a dip
        s = rng.choice([-1.0, 1.0], size=n) * b * rng.random(n) ** 0.2
        bits = ((x[:, None] >> np.arange(n, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(float)
        g = bits @ s
    return g

def check_d(rng):
    print("=== Theorem 2(d): S(mu_g) >= n h(sigma(b)) on random class members")
    worst = math.inf
    for n in (3, 5, 8, 10):
        for b in (0.5, 1.0, 2.0, 4.0):
            for _ in range(200):
                g = random_class_member(n, b, rng)
                # verify membership
                a = g.reshape([2] * n)
                assert all(np.max(np.abs(np.take(a, 1, axis=ax) - np.take(a, 0, axis=ax))) <= b + 1e-9 for ax in range(n))
                w = np.exp(-(g - g.min())); p = w / w.sum()
                S = -np.sum(p * np.log(p))
                worst = min(worst, S - n * h2(1 / (1 + math.exp(-b))))
    print(f"  3200 members, n in (3,5,8,10): min of S - n h(sigma(b)) = {worst:.3e} (>= 0 required)")
    # adversarial: n = 4, projected random search on log-weights to minimise S - n h
    n, b = 4, 1.5
    N = 1 << n
    best = math.inf
    nb = [[x ^ (1 << i) for i in range(n)] for x in range(N)]
    for trial in range(200):
        g = random_class_member(n, b, rng)
        def S_of(g):
            w = np.exp(-(g - g.min())); p = w / w.sum(); return -np.sum(p * np.log(p))
        cur = S_of(g)
        for it in range(3000):
            x = int(rng.integers(0, N)); delta = rng.normal(0, 0.3)
            lo = max(g[y] for y in nb[x]) - b; hi = min(g[y] for y in nb[x]) + b
            new = min(max(g[x] + delta, lo), hi)
            old = g[x]; g[x] = new
            s = S_of(g)
            if s <= cur:
                cur = s
            else:
                g[x] = old
        best = min(best, cur - n * h2(1 / (1 + math.exp(-b))))
    print(f"  adversarial descent, n=4, b=1.5, 200 starts: min of S - n h(sigma) = {best:.3e}")

if __name__ == "__main__":
    rng = np.random.default_rng(20261125)
    check_d(rng)
    C, n = bch_dual(4, 2)
    analyse("dual of BCH(15, t=2)  [15,8,4], dual distance 5", C, n, 4, [0.5, 1.0, 2.0, 4.0], True)
    G = golay24()
    analyse("extended Golay [24,12,8], dual distance 8", G, 24, 7, [1.0, 2.0, 4.0], True)
    if len(sys.argv) > 1 and sys.argv[1] == "big":
        C, n = bch_dual(5, 2)
        analyse("dual of BCH(31, t=2)  [31,10,12], dual distance 5", C, n, 4, [1.0, 2.0, 4.0], False)
