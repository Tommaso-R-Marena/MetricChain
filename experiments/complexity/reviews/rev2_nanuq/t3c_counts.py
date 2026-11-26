"""Task 3(c): independent recomputation of the finite facts (Lemma 4, Lemma 8, the numbers of Section 7)."""
import sys, time, random
from itertools import combinations
from collections import Counter
from fractions import Fraction
from css import *

t0 = time.time()

def describe_missing(n, nontriv):
    allnt = set(nontrivial_circular_splits(n))
    return sorted(tuple(p for p in range(n) if (m >> p) & 1) for m in allnt - set(nontriv))

# ---------------------------------------------------------------- binary trees / tree-generated systems
for n in (4, 5, 6, 7):
    tg = tree_generated_systems(n)
    # independent characterisation over ALL subsets of non-trivial circular splits
    S = nontrivial_circular_splits(n)
    cnt2 = 0
    for r in range(0, len(S) + 1):
        for sub in combinations(S, r):
            if is_tree_generated(n, sub):
                cnt2 += 1
                assert frozenset(sub) in tg
    print(f"n={n}: binary circular trees {len(binary_trees(n))}; tree-generated systems {len(tg)} "
          f"(second characterisation: {cnt2})", flush=True)

# ---------------------------------------------------------------- Lemma 4: 5-point facts
n = 5
vals5, valsPsi = Counter(), Counter()
ok5 = True
for nt in tree_generated_systems(5):
    sigma = with_trivial(5, nt)
    for lab in dihedral_labellings(list(range(5))):
        u1, z, up, v1, vq = lab
        v = Phi5(sigma, u1, z, up, v1, vq)
        vals5[v] += 1
        if v < 0 or (v != 0 and not displays(sigma, u1, up, v1, vq)):
            ok5 = False
        a, u, b, zz, w = lab
        p = Psi(sigma, a, u, b, zz, w)
        valsPsi[p] += 1
        if p < 0:
            ok5 = False
print("Lemma 4: 5-point systems:", len(tree_generated_systems(5)), "| values of Phi5:", dict(vals5),
      "| values of Psi:", dict(valsPsi), "| all 5-point facts hold:", ok5)
# is the converse true (Phi5 > 0 whenever displayed)?  (not claimed; informative)
conv = all(Phi5(with_trivial(5, nt), *lab) > 0 or not displays(with_trivial(5, nt), lab[0], lab[2], lab[3], lab[4])
           for nt in tree_generated_systems(5) for lab in dihedral_labellings(list(range(5))))
print("   (Phi5 > 0 whenever u1up|v1vq is displayed: %s)" % conv)

# ---------------------------------------------------------------- validation of the fast A-system routine
cntv = 0
for N in range(4, 10):
    for k in range(0, N // 2 + 1):
        for tree in binary_trees(N):
            for pairs in adjacent_pair_sets(N, k):
                a, na = A_system(N, tree, pairs)
                b, nb = A_system_bruteforce(N, tree, pairs)
                assert a == b and na == nb
                cntv += 1
print("A-structures (N<=9 positions) on which the fast routine equals the brute-force definition:", cntv, flush=True)

# ---------------------------------------------------------------- classes A and C
for n in (3, 4, 5, 6):
    A = A_class(n)
    C = C_class(n)
    closedA = all(img in A for s in A for img in dihedral_images(n, s))
    closedC = all(img in C for s in C for img in dihedral_images(n, s))
    tgn = {with_trivial(n, nt) for nt in tree_generated_systems(n)} if n >= 4 else None
    print(f"n={n}: |A_n|={len(A)} |C_n|={len(C)}  A subset C: {A <= C}  dihedrally closed: A {closedA}, C {closedC}"
          + (f"  C subset of tree-generated: {C <= tgn}" if tgn else "") + f"  [{time.time()-t0:.0f}s]", flush=True)

# ---------------------------------------------------------------- six points
n = 6
tg6 = [with_trivial(6, nt) for nt in tree_generated_systems(6)]
status = {s: check(6, s)[0] for s in tg6}
good = [s for s in tg6 if status[s] == "ok"]
loc = [s for s in tg6 if six_locally_good(6, s)]
C6 = C_class(6)
A6 = A_class(6)
print(f"six points: tree-generated {len(tg6)} | Kalmanson with exact support {len(good)} "
      f"(status counts {dict(Counter(status.values()))}) | 6-locally good {len(loc)} | in C_6 {len(C6)} | in A_6 {len(A6)}")
print("   6-locally good subset of globally good:", set(loc) <= set(good), "| C_6 subset of 6-locally good:", C6 <= set(loc),
      "| A_6 subset of 6-locally good:", A6 <= set(loc))
print("   Theorem-4 hypothesis (locally NANUQ-positive, literal) holds for:",
      sum(1 for s in tg6 if locally_nanuq_positive(6, s)), "systems; coincides with 6-locally good:",
      {s for s in tg6 if locally_nanuq_positive(6, s)} == set(loc))
print("   by number of non-trivial splits (tree-generated / good / 6-loc. good / C_6 / A_6):")
for k in range(3, 10):
    f = lambda fam: sum(1 for s in fam if len(s) - 6 == k)
    print("      ", k, f(tg6), f(good), f(loc), f(C6), f(A6))
print("   globally bad systems (missing non-trivial splits):")
for s in tg6:
    if status[s] != "ok":
        print("      ", status[s], describe_missing(6, [m for m in s if not is_trivial(6, m)]), check(6, s)[1])
print("   6-locally bad but globally good (missing non-trivial splits):")
for s in good:
    if s not in set(loc):
        print("      ", describe_missing(6, [m for m in s if not is_trivial(6, m)]))
print("   systems that are 6-locally good but not in C_6:", len(set(loc) - C6),
      "| dihedral classes:", len({dihedral_canon(6, s) for s in set(loc) - C6}))
print("   dihedral classes: tree-generated", len({dihedral_canon(6, s) for s in tg6}),
      "good", len({dihedral_canon(6, s) for s in good}), "loc", len({dihedral_canon(6, s) for s in loc}),
      "C_6", len({dihedral_canon(6, s) for s in C6}))

# (c) cherry doubling of 5-point systems
okc = True
star3 = trivial_splits(3)
for nt in tree_generated_systems(5):
    s5 = with_trivial(5, nt)
    for p in range(5):
        s6 = substitute(5, s5, p, 3, star3, 0)
        okc &= six_locally_good(6, s6)
print("   every 5-point tree-generated system with one leaf doubled is 6-locally good:", okc)

# ---------------------------------------------------------------- Proposition 2 (identity)
def check_identity(n, sigma):
    D = nanuq(n, sigma)
    if D is None:
        return None
    al = alphas(n, D)
    for (i, j), (a, m) in al.items():
        loc_half, six = alpha_from_local_terms(n, sigma, i, j)
        assert a == 2 * loc_half, (n, sorted(sigma), i, j, a, loc_half)
    return True

cnt = 0
for n in (4, 5, 6, 7):
    for nt in tree_generated_systems(n):
        check_identity(n, with_trivial(n, nt)); cnt += 1
print("Proposition 2 identity verified on all tree-generated systems, n<=7:", cnt, flush=True)
rng = random.Random(2026)
cnt = 0
for n in (5, 6, 7, 8, 9):
    S = nontrivial_circular_splits(n)
    for _ in range(250):
        sub = [m for m in S if rng.random() < rng.choice([0.4, 0.6, 0.8])]
        if check_identity(n, with_trivial(n, sub)):
            cnt += 1
print("Proposition 2 identity verified on random arbitrary circular split systems (n=5..9) with all 4-sets resolved:", cnt)
print(f"[total {time.time()-t0:.0f}s]")
