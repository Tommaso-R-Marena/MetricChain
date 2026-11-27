"""Extra referee checks.
 (A) N(s,t): which 6-point terms of the split {x,y}|rest are negative (the 'Why' paragraph of Section 6).
 (B) Chepoi-Fichet identity d = 1/2 sum alpha_ij delta_{S_ij} and Lemma 1 (d_N = d_Sigma) on explicit networks.
 (C) random iterated substitutions of systems of C_4, C_5, C_6: conclusion of Theorem 6' and 6-restrictions in C_6.
 (D) 'sharpness' for negativity alone: does each of the 23 excluded six-point systems have a blow-up with a
     NEGATIVE split weight (not merely a support mismatch)?
"""
import random, sys
from itertools import combinations, product
from collections import Counter
from fractions import Fraction
import rnet, gen, css
from t9c_family import build
from t3d_blowups import blowup

# ---------------------------------------------------------------- (A)
print("(A) local terms of alpha({x,y}|rest) in N(s,t)")
for bloblet in (True, False):
    for s, t in [(1, 2), (2, 2), (3, 3), (2, 4)]:
        net, order = build(s, t, bloblet)
        st, det, sigma, n = gen.check_fast(net, order)
        pos = {l: i for i, l in enumerate(order)}
        i, j = pos["b"], pos["y"]          # U = {x,y} = positions i+1..j
        half, six = css.alpha_from_local_terms(n, sigma, i, j)
        U = [(i + 1 + k) % n for k in range((j - i) % n)]
        V = [(j + 1 + k) % n for k in range(n - len(U))]
        v1, vq, u1, up = V[0], V[-1], U[0], U[-1]
        kinds = Counter()
        for z, w in combinations(V[1:-1], 2):
            val = css.Phi6(sigma, v1, z, w, vq, u1, up)
            kind = "".join(sorted(order[z][0] + order[w][0]))
            kinds[(kind, str(val))] += 1
        phi4 = css.Phi4(sigma, u1, up, v1, vq)
        phi5 = [str(css.Phi5(sigma, v1, z, vq, u1, up)) for z in V[1:-1]]
        print(f"   {'bloblet' if bloblet else 'clade  '} N({s},{t}): alpha/2={half}  Phi4={phi4}  Phi5 terms={phi5}  "
              f"Phi6 terms by leaf types (a/d): {dict(sorted(kinds.items()))}")

# ---------------------------------------------------------------- (B)
print("(B) Chepoi-Fichet identity and Lemma 1 on random outer-labeled planar networks")
rng = random.Random(4)
cnt = 0
for trial in range(600):
    n = rng.choice([5, 6, 7, 8]); k = rng.choice([1, 2, 3, 4])
    net = gen.grow(n, k, rng)
    if net is None:
        continue
    order = rnet.planar_circular_order(net)
    if order is None:
        continue
    L, per_tree, quads, Qsets = gen.displayed_fast(net)
    D = gen.nanuq_fast(len(L), quads, Qsets)
    st, det, sigma, nn = gen.check_fast(net, order)
    li = [L.index(l) for l in order]
    DN = [[D[li[a]][li[b]] for b in range(nn)] for a in range(nn)]
    DS = css.nanuq(nn, sigma)
    assert DS == DN, "Lemma 1 fails"
    al = css.alphas(nn, DN)
    for x in range(nn):
        for y in range(x + 1, nn):
            tot = Fraction(0)
            for (i, j), (a, m) in al.items():
                if ((m >> x) & 1) != ((m >> y) & 1):
                    tot += a
            assert tot / 2 == DN[x][y], "Chepoi-Fichet identity fails"
    cnt += 1
print("   networks (galled or not) on which d_N = d_Sigma and d = 1/2 sum alpha delta:", cnt)

# ---------------------------------------------------------------- (C)
print("(C) random iterated substitutions")
C = {m: sorted(css.C_class(m), key=sorted) for m in (3, 4, 5, 6)}
C6 = css.C_class(6)
rng = random.Random(9)
res = Counter()
for trial in range(1500):
    m = rng.choice([4, 5, 6])
    n, s = m, rng.choice(C[m])
    while n < rng.choice([7, 8, 9, 10]):
        m2 = rng.choice([3, 4, 5, 6])
        s2 = rng.choice(C[m2])
        if rng.random() < 0.5:
            s = css.substitute(n, s, rng.randrange(n), m2, s2, rng.randrange(m2))
        else:
            s = css.substitute(m2, s2, rng.randrange(m2), n, s, rng.randrange(n))
        n = n + m2 - 2
    stt = css.check(n, s)[0]
    res[(n, stt)] += 1
    subs = list(combinations(range(n), 6))
    if len(subs) > 30:
        subs = rng.sample(subs, 30)
    if not all(css.restrict(n, s, Y) in C6 for Y in subs):
        res["RESTRICTION NOT IN C6"] += 1
print("   ", dict(sorted(res.items(), key=str)))

# ---------------------------------------------------------------- (D)
print("(D) blow-ups with a NEGATIVE weight for the 23 excluded six-point systems (mult in {1,2,3}^6, total <= 11)")
tg6 = [css.with_trivial(6, nt) for nt in css.tree_generated_systems(6)]
allnt = set(css.nontrivial_circular_splits(6))
for s in tg6:
    if css.six_locally_good(6, s):
        continue
    base = css.check(6, s)[0]
    best = None
    if base == "neg":
        best = ((1,) * 6, "neg")
    else:
        for mult in sorted(product((1, 2, 3), repeat=6), key=sum):
            if sum(mult) == 6 or sum(mult) > 11:
                continue
            n2, s2 = blowup(6, s, mult)
            if css.check(n2, s2)[0] == "neg":
                best = (mult, "neg")
                break
    miss = sorted(tuple(p for p in range(6) if (m >> p) & 1) for m in allnt - s)
    print("    missing", miss, "| six-point status:", base, "| smallest blow-up with a negative weight:", best, flush=True)
