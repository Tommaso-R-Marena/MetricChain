#!/usr/bin/env python3
"""R3 — checks of Theorem 4 on small codes and of three statements the referee proposes:

 (A) theta_na with a k-body marginal oracle: the C-symmetrised cone  c d_H(x, a+C)  and its
     flattening  max(c d_H(x, a+C), cR)  are C-invariant members of the class that differ exactly
     on U_a = {d(x, a+C) < R}; if the balls B(a', R-1), a' in a+C, are pairwise disjoint, then
         ln Z(cone_C) - ln Z(flat_C)  >=  D_R  (the drop for a single cone);
     in general  1 - e^{-drop_C} >= (1 - e^{-D_R}) - (|C|/2) cosh(u/2)^{-d_min(C)}.
 (B) sharpness of Theorem 2 within mixtures: for nu_pi = sum_a pi(a) P_a,
         S(nu_pi) - n h(sigma) = I(Z;X) >= -ln E kappa^{d(Z,Z')},   kappa = 1/cosh(b/2),
     and for k-wise uniform pi,  E kappa^{d(a,Z')} <= min_r [ M_t/min_{d<=r} F_t(d)^2 + kappa^{r+1} ].
 (C) Theorem 4 itself: g_a^C in the class, uniform k-body marginals, |U_a| <= |C| V(n,r),
     ln Z(g_a^C) >= ln Z(g_a).
"""
import math, sys
import numpy as np
from r3_codes import golay24, bch_dual, bch_ext_dual, rref, span, weight_distribution, dual_basis, min_weight
from r3_thm2 import coset_distance_table, full_cube_from_cosets, fwht_inplace, h2
from r3_thm3 import F, M, K

def lbinom(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

def single_cone_drop(n, u, R):
    Zc = n * math.log(1 + math.exp(-u))
    terms = [lbinom(n, j) - u * max(j, R) for j in range(n + 1)]
    mx = max(terms)
    return Zc - (mx + math.log(sum(math.exp(t - mx) for t in terms)))

def part_A(name, C, n, us=(0.5, 1.0, 2.0)):
    R_ = rref(C)
    size = 1 << len(R_)
    reps, counts, free, piv, words = coset_distance_table(C, n)
    dC = np.argmax(counts > 0, axis=1)                    # d(x, C) on each coset
    dmin = next(w for w in range(1, n + 1) if counts[0, w] > 0) if size > 1 else n + 1
    print(f"(A) {name}: n={n}, |C|={size}, d_min={dmin}, covering radius {int(dC.max())}")
    for u in us:
        Zc = size * np.sum(np.exp(-u * dC))
        rows = []
        for R in range(1, int(dC.max()) + 2):
            Zf = size * np.sum(np.exp(-u * np.maximum(dC, R)))
            dropC = math.log(Zc / Zf)
            DR = single_cone_drop(n, u, R)
            disjoint = 2 * (R - 1) < dmin
            lower_general = (1 - math.exp(-DR)) - (size / 2) * math.cosh(u / 2) ** (-dmin)
            okg = (1 - math.exp(-dropC)) >= lower_general - 1e-12
            Usize = size * int(np.sum(dC < R))
            VR = sum(math.comb(n, j) for j in range(R))
            rows.append((R, dropC, DR, disjoint, okg, Usize / (size * VR)))
            if disjoint:
                assert dropC >= DR - 1e-12, (name, u, R, dropC, DR)
            assert okg
        print(f"    u={u}: " + "; ".join(f"R={R}: drop_C={a:.4f} vs D_R={b:.4f}{' (disjoint, >= holds)' if dj else ''}"
                                         f" |U|/(|C|V)={fr:.3f}" for R, a, b, dj, og, fr in rows))

def part_B(name, C, n, k, bs=(1.0, 2.0, 4.0)):
    t = k // 2
    R_ = rref(C)
    size = 1 << len(R_)
    A = weight_distribution(R_, n)
    reps, counts, free, piv, words = coset_distance_table(C, n)
    print(f"(B) {name}: n={n}, |C|={size}, k={k}, t={t}")
    for b in bs:
        sig = 1 / (1 + math.exp(-b)); kap = 1 / math.cosh(b / 2)
        pw = np.array([sig ** (n - w) * (1 - sig) ** w for w in range(n + 1)])
        nu_c = counts @ pw / size
        S = -size * np.sum(nu_c * np.log(nu_c))
        Delta = S - n * h2(sig)
        L_code = math.log(size) - math.log(sum(A[w] * kap ** w for w in range(n + 1)))
        gen = min(M(n, t) / min(F(n, t, d) ** 2 for d in range(r + 1)) + kap ** (r + 1)
                  for r in range(0, n // 2) if all(F(n, t, d) > 0 for d in range(r + 1)))
        L_gen = -math.log(gen)
        print(f"    b={b}: Delta = S - n h(sigma) = {Delta:.4f};  -ln E kappa^d(Z,Z') = {L_code:.4f};  "
              f"k-wise-uniform-only bound = {L_gen:.4f};  ln|C| = {math.log(size):.4f};  ln M_t = {math.log(M(n, t)):.4f};  "
              f"chain Delta >= code bound >= generic bound: {Delta >= L_code - 1e-9 >= 0 and L_code >= L_gen - 1e-9}")
        assert Delta >= L_code - 1e-9 and L_code >= L_gen - 1e-9

def part_B_noncode(rng):
    """A k-wise uniform mixing law that is not uniform on a code: random convex combination of
    uniform laws on cosets of a few permuted copies of the [15,8] code (4-wise uniform)."""
    n = 15; k = 4; t = 2
    C, _ = bch_dual(4, 2)
    N = 1 << n
    x = np.arange(N, dtype=np.uint64)
    wt = np.bitwise_count(x).astype(np.int64)
    print("(B') non-code mixing laws (n=15, 4-wise uniform): S(nu_pi) - n h(sigma) vs -ln E kappa^d(Z,Z') vs generic bound")
    for trial in range(4):
        pi = np.zeros(N)
        ncomp = int(rng.integers(2, 6))
        wts = rng.dirichlet(np.ones(ncomp))
        for c in range(ncomp):
            perm = rng.permutation(n)
            Cp = []
            for cw in C:
                v = 0
                for i in range(n):
                    if cw >> i & 1:
                        v |= 1 << int(perm[i])
                Cp.append(v)
            words = np.array(span(rref(Cp)), dtype=np.int64)
            pi[words ^ int(rng.integers(0, N))] += wts[c] / len(words)
        # check 4-wise uniformity of pi
        Fp = fwht_inplace(pi.copy())
        assert np.max(np.abs(Fp[(wt >= 1) & (wt <= k)])) < 1e-12
        for b in (2.0, 4.0):
            sig = 1 / (1 + math.exp(-b)); kap = 1 / math.cosh(b / 2); tau = math.tanh(b / 2)
            # nu = T_tau pi  (Fourier multiplier tau^|T|)
            nu = fwht_inplace(Fp * tau ** wt) / N
            assert nu.min() > 0 and abs(nu.sum() - 1) < 1e-12
            Delta = -np.sum(nu * np.log(nu)) - n * h2(sig)
            # E kappa^{d(Z,Z')} = sum_y (pi * pi)(y) kappa^{|y|} ; autocorrelation via FWHT
            auto = fwht_inplace(Fp * Fp) / N
            Ek = float(np.sum(auto * kap ** wt))
            gen = min(M(n, t) / min(F(n, t, d) ** 2 for d in range(r + 1)) + kap ** (r + 1)
                      for r in range(0, n // 2) if all(F(n, t, d) > 0 for d in range(r + 1)))
            print(f"    trial {trial} ({ncomp} components) b={b}: Delta = {Delta:.4f} >= {-math.log(Ek):.4f} >= {-math.log(gen):.4f}: "
                  f"{Delta >= -math.log(Ek) - 1e-9 >= -math.log(gen) - 2e-9}")
            assert Delta >= -math.log(Ek) - 1e-9 and -math.log(Ek) >= -math.log(gen) - 1e-9

def part_B_asymptotic():
    print("(B'') the generic lower bound  -ln min_r [M_t/min F_t^2 + kappa^(r+1)]  against  t ln n - ln t!  and ceil(k/2) ln(2n):")
    for b in (1.0, 2.0, 4.0):
        kap = 1 / math.cosh(b / 2)
        for t in (1, 2, 3):
            row = []
            for n in (100, 1000, 10000, 100000):
                best = math.inf
                # F_t decreasing on [0, first root): scan r on a geometric grid
                for r in sorted(set(int(v) for v in np.unique(np.round(np.geomspace(1, n // 4, 60))))):
                    Fr = F(n, t, r)
                    if Fr <= 0:
                        break
                    val = M(n, t) / Fr ** 2 + kap ** (r + 1)
                    best = min(best, val)
                row.append((-math.log(best), t * math.log(n) - math.lgamma(t + 1), t * math.log(2 * n)))
            print(f"    b={b} t={t}: " + "  ".join(f"n=1e{int(round(math.log10(nn)))}: {a:.2f} / {bb:.2f} / {c:.2f}"
                                                   for nn, (a, bb, c) in zip((100, 1000, 10000, 100000), row)))

def part_C():
    print("(C) Theorem 4 on small codes (exact)")
    for name, C, n, k in (("simplex [15,4,8]", bch_dual(4, 1)[0], 15, 2), ("dual BCH(15,2) [15,8,4]", bch_dual(4, 2)[0], 15, 4),
                          ("Golay [24,12,8]", golay24(), 24, 7)):
        R_ = rref(C); size = 1 << len(R_)
        reps, counts, free, piv, words = coset_distance_table(C, n)
        dC = np.argmax(counts > 0, axis=1)
        u = 1.5
        for r in (2, 3, 4):
            gC = -u * np.maximum(r - dC, 0.0)                   # beta g_0^C on cosets
            ZC = size * np.sum(np.exp(-gC))
            Zdip = 2 ** n + sum(math.comb(n, j) * (math.exp(u * (r - j)) - 1) for j in range(r))
            Usize = size * int(np.sum(dC < r)); V = sum(math.comb(n, j) for j in range(r))
            line = (f"    {name} r={r}: |U_0| = {Usize} <= |C| V = {size * V}: {Usize <= size * V};  "
                    f"ln Z(g^C) - ln Z(dip) = {math.log(ZC / Zdip):+.4f} (>= 0);  ln Z(dip) - ln Z_0 = {math.log(Zdip / 2 ** n):.4f}")
            assert Usize <= size * V and ZC >= Zdip * (1 - 1e-12)
            if n <= 24:
                full = full_cube_from_cosets(C, n, reps, np.exp(-gC) / ZC, free, piv)
                a = full.reshape([2] * n)
                worst = max(max(float((np.take(a, 1, axis=ax) / np.take(a, 0, axis=ax)).max()),
                                float((np.take(a, 0, axis=ax) / np.take(a, 1, axis=ax)).max())) for ax in range(n))
                Fz = fwht_inplace(full.copy())
                wt = np.bitwise_count(np.arange(1 << n, dtype=np.uint64)).astype(np.int64)
                low = float(np.max(np.abs(Fz[(wt >= 1) & (wt <= k)])))
                hi = float(np.max(np.abs(Fz[wt == k + 1])))
                line += f";  max flip ratio {worst:.4f} <= e^u = {math.exp(u):.4f};  max |E chi_T|, 1<=|T|<={k}: {low:.1e}; |T|={k + 1}: {hi:.2e}"
                assert worst <= math.exp(u) * (1 + 1e-12) and low < 1e-12
            print(line)

if __name__ == "__main__":
    rng = np.random.default_rng(99)
    part_C()
    for name, C, n in (("simplex [15,4,8]", bch_dual(4, 1)[0], 15), ("RM(1,4) [16,5,8]", bch_ext_dual(4, 1)[0], 16),
                       ("dual BCH(15,2) [15,8,4]", bch_dual(4, 2)[0], 15), ("Golay [24,12,8]", golay24(), 24)):
        part_A(name, C, n)
    part_B("dual BCH(15,2) [15,8,4]", bch_dual(4, 2)[0], 15, 4)
    part_B("Golay [24,12,8]", golay24(), 24, 7)
    part_B("simplex [15,4,8]", bch_dual(4, 1)[0], 15, 2)
    part_B_noncode(rng)
    part_B_asymptotic()
    if len(sys.argv) > 1 and sys.argv[1] == "big":
        C, n = bch_dual(5, 2)
        part_A("dual BCH(31,2) [31,10,12]", C, n)
        part_B("dual BCH(31,2) [31,10,12]", C, n, 4)
