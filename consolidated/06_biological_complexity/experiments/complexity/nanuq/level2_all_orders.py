"""Theorem 12' of docs/complexity/NANUQ_LOCAL_CRITERION.md: a negative critical weight excludes EVERY circular order.

For the nested bloblets N[kB, k1, k2] with clades of prescribed sizes at the positions (the systems of Theorem 12),
whenever the critical split S* has negative weight, the proof uses five leaves

    B1  the first leaf of position b_1,        Z   any leaf at a middle position b_j (j in M),
    Cc  the last leaf of position c_1 (or of b_kB when k2 = 0),   Y  any leaf at y,   X1  any leaf at x_1,

and three four-point facts about d = d_N (P(pq,rs) := d(p,q) + d(r,s)):
    (1)  P(B1 Cc, Y X1)  >  P(B1 Y, Cc X1)  and  >  P(B1 X1, Cc Y)      -- the pair {B1,Cc} must separate Y from X1,
    (2)  P(B1 Cc, Z Y)   >  the other two sums on {B1, Z, Cc, Y}         -- {B1,Cc} must separate Z from Y,
    (3)  P(B1 Cc, Z X1)  >  the other two sums on {B1, Z, Cc, X1}        -- {B1,Cc} must separate Z from X1,
which no circular order satisfies.  This script
    (a) checks (1)-(3) for every admissible choice of the five leaves, on all blow-ups with at most MAXN leaves and
        position sizes at most 3 that have a negative critical weight, and also that the difference in (1) is
        exactly -alpha(S*), i.e. minus twice the weight alpha/2 of S* (no other split separates {Y,X1} from {B1,Cc});
    (b) confirms by the independent backtracking search over all circular orders (kalmanson_only.kalmanson_for_some_order)
        that no order exists, for the instances with at most SEARCHN leaves;
    (c) control: for the blow-ups with critical weight >= 0 the metric is Kalmanson for the given order.
Exact integer arithmetic (the functions return 2d).

Usage:  python3 level2_all_orders.py [MAXN [SEARCHN]]      (defaults 13, 10)
"""
import itertools
import sys

from splitsys import nanuq_2d, alphas_2, canon, split_mask
from localcrit import blowup
from level2_nongalled import system
from level2_classification import formula
from kalmanson_only import kalmanson_for_some_order


def blown(kB, k1, k2, mult):
    """mult: list of sizes in circular order (b_1..b_kB, c_k2..c_1, y, x_k1..x_1).  Returns n2, sigma2, pos (leaf -> position name)."""
    n, names, sigma, _ = system(kB, k1, k2)
    n2, s2 = blowup(n, sigma, mult)
    pos = []
    for p in range(n):
        pos += [names[p]] * mult[p]
    return n2, s2, pos


def three_sums(D, p, q, r, s):
    return D[p][q] + D[r][s], D[p][r] + D[q][s], D[p][s] + D[q][r]


def kalmanson_given_order(n, D):
    for a, b, c, d in itertools.combinations(range(n), 4):
        s = D[a][c] + D[b][d]
        if s < D[a][b] + D[c][d] or s < D[a][d] + D[b][c]:
            return False
    return True


def main(maxn, searchn):
    ok = True
    neg = zero = pos_ = searched = quintuples = 0
    for kB in range(2, maxn):
        for k1 in range(1, maxn):
            for k2 in range(0, maxn):
                base = kB + k1 + k2 + 1
                if base > maxn:
                    break
                for mult in itertools.product((1, 2, 3), repeat=base):
                    if sum(mult) > maxn:
                        continue
                    n2, s2, pos = blown(kB, k1, k2, list(mult))
                    beta = list(mult[:kB])
                    gamma = list(mult[kB:kB + k2])[::-1]
                    eta = mult[kB + k2]
                    xi = list(mult[kB + k2 + 1:])[::-1]
                    pred = formula(beta, xi, eta, gamma)
                    D = nanuq_2d(n2, s2)
                    m = 0
                    for q in range(n2):
                        if pos[q][0] in "yx":
                            m |= 1 << q
                    star = canon(n2, m)
                    al = alphas_2(n2, D)
                    val = [v for (i, j), v in al.items() if canon(n2, split_mask(n2, i, j)) == star]
                    assert len(val) == 1
                    ok &= (val[0] == 2 * pred)                      # alphas_2 returns 2*alpha, D = 2d: val = 2*alpha
                    if pred > 0:
                        pos_ += 1
                        ok &= kalmanson_given_order(n2, D)
                        continue
                    if pred == 0:
                        zero += 1
                        ok &= kalmanson_given_order(n2, D)
                        continue
                    neg += 1
                    where = lambda nm: [q for q in range(n2) if pos[q] == nm]
                    B1 = where(("b", 1))[0]
                    Cc = where(("c", 1))[-1] if k2 >= 1 else where(("b", kB))[-1]
                    M = range(2, kB + 1) if k2 >= 1 else range(2, kB)
                    for Z in [q for j in M for q in where(("b", j))]:
                        for Y in where(("y", 0)):
                            for X1 in where(("x", 1)):
                                quintuples += 1
                                a1, a2, a3 = three_sums(D, B1, Cc, Y, X1)          # (B1Cc|YX1), (B1Y|CcX1), (B1X1|CcY)
                                ok &= a1 > a2 and a1 > a3
                                ok &= (a1 - a2) == -2 * pred                     # P1 - P2 = -alpha(S*) in d (the split weight is alpha/2), i.e. -2 alpha in 2d
                                b1, b2, b3 = three_sums(D, B1, Cc, Z, Y)
                                ok &= b1 > b2 and b1 > b3
                                c1, c2, c3 = three_sums(D, B1, Cc, Z, X1)
                                ok &= c1 > c2 and c1 > c3
                    if n2 <= searchn:
                        searched += 1
                        ok &= kalmanson_for_some_order(n2, D) is None
                    if not ok:
                        print("FAILURE at", (kB, k1, k2), mult)
                        return False
    print(f"blow-ups of N[kB,k1,k2] with position sizes <= 3 and at most {maxn} leaves: critical weight positive {pos_}, zero {zero}, negative {neg}")
    print(f"   formula of Theorem 12(b) for the critical weight in all of them; Kalmanson for the given order whenever the weight is >= 0: {ok}")
    print(f"   negative weight: the three four-point facts hold for all {quintuples} admissible choices of five leaves, and the first difference equals -alpha(S*): {ok}")
    print(f"   independent search over all circular orders on the {searched} negative instances with at most {searchn} leaves: no order found: {ok}")
    print("ALL OK" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    searchn = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    sys.exit(0 if main(maxn, searchn) else 1)
