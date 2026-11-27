"""A proof strategy for the randomised count of the Hamming ball at prescribed width (theory report Proposition
11.18e(b')(ii), a conjecture), tested in exact arithmetic on the cube at order two.

Setting.  h(s) = alpha + sum_i beta_i s_i on {-1, 1}^n with huge coefficients; ln Z is then -min h = -alpha + sum |beta_i|
up to a bounded term, attained at x* = -sign(beta).  An algorithm has evaluated h on a set Q of n affinely independent
points (one evaluation fewer than the ball has points).  Let nu span the kernel of the differences x^j - x^1.  The
minimum is a known linear combination of the observed values iff x* lies in the affine hull of Q, i.e. iff
nu . x* = nu . x^1 (the event S).

The pairing.  For beta with pairwise widely separated magnitudes let k be the coordinate of supp(nu) with the least
|beta_k / nu_k|, t = -2 beta_k / nu_k, beta' = beta + t nu, alpha' = alpha - t nu . x^1.  Claims tested here, exactly
(integers and fractions):
  (1) h' = h on Q (the two instances have the same transcript);
  (2) beta' has the signs of beta except at k, where the sign flips, and k(beta') = k(beta): the map is an involution;
  (3) the magnitudes of the other coordinates change by a relative amount that is tiny (the log-uniform prior density
      prod 1/|beta_i| is preserved up to a factor 1 + o(1));
  (4) S(beta) and S(beta') never both hold, so the pairing maps S into its complement: P(S | transcript) <= 1/2 + o(1);
  (5) whenever S(beta) holds, min h' differs from min h by an amount of the order of |t| - no single output is right
      for both;
  (6) under the prior (independent signs, log-uniform magnitudes) the frequency of S is at most 1/2 for every Q tried,
      and exactly 1/2 for coordinate directions.
Not tested, and not proved here: adaptive choice of Q (the pairing is transcript by transcript, so it covers adaptive
strategies, but the argument that the 'lucky' outputs off S have vanishing posterior probability is on paper only);
orders above two; alphabets with more than two states.

Run from the repository root:  python3 experiments/coordinator_checks/random_ball/pairing_check.py [output file]
"""
import itertools
import math
import random
import sys
from fractions import Fraction

OUT = open(sys.argv[1], "w") if len(sys.argv) > 1 else None


def out(s):
    print(s)
    if OUT:
        OUT.write(s + "\n")


def kernel_vector(rows, n):
    """a nonzero rational vector orthogonal to all rows, or None if the rows have rank n (or rank < n - 1)"""
    M = [[Fraction(v) for v in r] for r in rows]
    piv, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    if r != n - 1:
        return None
    free = next(c for c in range(n) if c not in piv)
    nu = [Fraction(0)] * n
    nu[free] = Fraction(1)
    for i, c in enumerate(piv):
        nu[c] = -M[i][free]
    den = math.lcm(*[v.denominator for v in nu])
    return [int(v * den) for v in nu]


def draw_instance(rng, n, logB0, Lam):
    beta = [rng.choice((-1, 1)) * int(math.exp(logB0 + rng.random() * Lam)) for _ in range(n)]
    alpha = rng.randrange(-10 ** 9, 10 ** 9) * int(math.exp(logB0 + Lam))        # much wider than every beta
    return alpha, beta


def main():
    rng = random.Random(20261126)
    out("pairing check for the randomised count of the Hamming ball (cube, order two); exact arithmetic")
    out(f"{'n':>2} {'sets Q':>7} {'draws':>7} {'separated':>10} {'(1) transcript':>15} {'(2) involution':>15} {'(3) max rel. change':>20}"
        f" {'(4) S and S′':>12} {'(5) same min on S':>18} {'freq S: least, largest':>24}")
    totals = dict(sep=0, draws=0, bad1=0, bad2=0, bad4=0, bad5=0)
    worst_freq = 0.0
    for n in range(2, 8):
        cube = list(itertools.product((-1, 1), repeat=n))
        nQ, per = 30, 400
        stats = dict(sep=0, bad1=0, bad2=0, bad4=0, bad5=0, rel=0.0)
        freqs = []
        for qi in range(nQ):
            while True:
                if qi == 0:      # a coordinate direction: the star without its last arm
                    Q = [tuple([1] * n)] + [tuple(-1 if j == i else 1 for j in range(n)) for i in range(n - 1)]
                else:
                    Q = rng.sample(cube, n)
                nu = kernel_vector([[(a - b) // 2 for a, b in zip(x, Q[0])] for x in Q[1:]], n)
                if nu is not None:
                    break
            supp = [i for i in range(n) if nu[i] != 0]
            cmax = max(abs(Fraction(nu[i], nu[j])) for i in supp for j in supp)
            nS = 0
            for _ in range(per):
                alpha, beta = draw_instance(rng, n, 12.0, 60.0 * n)
                mags = sorted(abs(b) for b in beta)
                separated = all(mags[i + 1] >= 10 ** 4 * cmax * mags[i] for i in range(n - 1))
                xs = [-1 if b > 0 else 1 for b in beta]
                S = sum(nu[i] * xs[i] for i in range(n)) == sum(nu[i] * Q[0][i] for i in range(n))
                nS += S
                if not separated:
                    continue
                stats["sep"] += 1
                k = min(supp, key=lambda i: abs(Fraction(beta[i], nu[i])))
                t = Fraction(-2 * beta[k], nu[k])
                beta2 = [Fraction(beta[i]) + t * nu[i] for i in range(n)]
                alpha2 = Fraction(alpha) - t * sum(nu[i] * Q[0][i] for i in range(n))
                h = lambda x: alpha + sum(b * s for b, s in zip(beta, x))
                h2 = lambda x: alpha2 + sum(b * s for b, s in zip(beta2, x))
                if any(h(x) != h2(x) for x in Q):
                    stats["bad1"] += 1
                signs_ok = all((beta2[i] > 0) == (beta[i] > 0) for i in range(n) if i != k) and beta2[k] == -beta[k]
                k2 = min(supp, key=lambda i: abs(beta2[i] / nu[i]))
                t2 = -2 * beta2[k2] / nu[k2]
                back = [beta2[i] + t2 * nu[i] for i in range(n)]
                if not (signs_ok and k2 == k and back == [Fraction(b) for b in beta]):
                    stats["bad2"] += 1
                stats["rel"] = max(stats["rel"], max(float(abs(beta2[i] - beta[i]) / abs(beta[i])) for i in range(n) if i != k))
                xs2 = [-1 if b > 0 else 1 for b in beta2]
                S2 = sum(nu[i] * xs2[i] for i in range(n)) == sum(nu[i] * Q[0][i] for i in range(n))
                if S and S2:
                    stats["bad4"] += 1
                if S:
                    m1, m2 = min(h(x) for x in cube), min(h2(x) for x in cube)
                    if abs(m1 - m2) < abs(t) / max(abs(v) for v in nu if v) / 4:
                        stats["bad5"] += 1
            freqs.append(nS / per)
        totals["draws"] += nQ * per
        for key in ("sep", "bad1", "bad2", "bad4", "bad5"):
            totals[key] += stats[key]
        worst_freq = max(worst_freq, max(freqs))
        out(f"{n:>2} {nQ:>7} {nQ * per:>7} {stats['sep'] / (nQ * per):>10.3f} {stats['bad1']:>15} {stats['bad2']:>15} {stats['rel']:>20.2e}"
            f" {stats['bad4']:>12} {stats['bad5']:>18} {min(freqs):>11.3f}, {max(freqs):.3f}")
    out(f"draws {totals['draws']}, of which with separated magnitudes {totals['sep']}; violations of (1), (2), (4), (5): "
        f"{totals['bad1']}, {totals['bad2']}, {totals['bad4']}, {totals['bad5']}; largest frequency of S for one set Q: {worst_freq:.3f}"
        f" (400 draws per set: one standard error is 0.025)")
    ok = totals["bad1"] == totals["bad2"] == totals["bad4"] == totals["bad5"] == 0 and worst_freq < 0.6
    out("ALL CLAIMS HELD" if ok else "A CLAIM FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
