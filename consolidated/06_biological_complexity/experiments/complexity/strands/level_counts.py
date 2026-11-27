"""Minimum free energy and level counts per symmetry class from the fixed-point sums F_d
(Proposition 5 of docs/complexity/STRANDS_ALGORITHM.md; the argument is the one given by the referee of
COMPLEXITY-REV-0003, finding 2).

Loop energies are integers (units of eps).  For q = 2^(-K), K = ceil(N log2 24) + 1:
    F_d(q)  = sum over pairs (Y,S) fixed by the rotation of order d of q^E(S)            (multiset_dp.G1 / Gd)
    T_R(q)  = sum_{R | d | gcd} mu(d/R) F_d(q)   = sum over pairs with symmetry EXACTLY R of q^E(S)
            = sum_m N_R(m) q^m ,   0 <= N_R(m) <= 24^N < 2^K ,
so the integers N_R(m) are the base-2^K digits of T_R(q) * 2^(K*M) (M an upper bound for the energies), and the
number of PHYSICAL structures with symmetry R and loop energy m is N_R(m) * R / c.  Then
    MFE = min over (R, m) with N_R(m) > 0 of  m*eps + kT ln R      (+ (c-1) dG_assoc).
The symmetry-naive (min,+) recursion would instead return min_d (m_d + kT ln d) with m_d the least energy of a
structure whose symmetry is a MULTIPLE of d, which can lie below the true MFE; the test prints both.

Test: against exhaustive enumeration of the physical ensemble (all orderings, orbits under permutations of equal
strands), exact integers.
Usage: python3 level_counts.py
"""
import math
import sys
import time
from fractions import Fraction
from itertools import permutations, product

from ref_enum import concat, noncrossing_matchings, faces, classify, COMPLEMENT
from multiset_dp import Model, G1, Gd, divisors, mobius

# integer loop energies (units of eps); deliberately of mixed sign
def e_hp(u):
    return 2 + (u % 3)

def e_il(l1, l2):
    if l1 == 0 and l2 == 0:
        return -3                       # stack
    return 1 + (abs(l1 - l2) % 2) + (l1 + l2) // 3

E_MA, E_MB, E_MC = 2, -1, 1
KT_LN = lambda R: math.log(R)           # kT = 1 in units of eps for the comparison of free energies


def face_energy(kind, f):
    if kind == "exterior":
        return 0
    if kind == "hairpin":
        return e_hp(len(f["unpaired"]))
    if kind in ("stack", "bulge", "interior"):
        return e_il(f["segs"][0], f["segs"][1])
    if kind == "multi":
        return E_MA + E_MB * len(f["pairs"]) + E_MC * len(f["unpaired"])
    raise ValueError(kind)


def brute_levels(species, counts):
    """{(R, m): number of physical structures with symmetry R and loop energy m}"""
    strands = []
    for w, n in zip(species, counts):
        strands += [w] * n
    c = len(strands)
    structs = {}
    for rest in permutations(range(1, c)):
        order = (0,) + rest
        seq, owner, idx, nick_after = concat(strands, order)
        N = len(seq)
        can = lambda i, j: (seq[i], seq[j]) in COMPLEMENT
        for pairs in noncrossing_matchings(seq, 0, N, can):
            fs = faces(N, pairs, nick_after)
            kinds = [classify(f) for f in fs]
            if "disconnected" in kinds:
                continue
            en = sum(face_energy(kd, f) for f, kd in zip(fs, kinds))
            lab = frozenset(tuple(sorted(((owner[i], idx[i]), (owner[j], idx[j])))) for i, j in pairs)
            structs[lab] = en
    groups = {}
    for s, w in enumerate(strands):
        groups.setdefault(w, []).append(s)
    blocks = list(groups.values())
    perms = []
    for combo in product(*[list(permutations(b)) for b in blocks]):
        sg = list(range(c))
        for b, img in zip(blocks, combo):
            for x, y in zip(b, img):
                sg[x] = y
        perms.append(sg)
    seen, out = set(), {}
    for lab, en in structs.items():
        if lab in seen:
            continue
        orbit, stab = set(), 0
        for sg in perms:
            img = frozenset(tuple(sorted(((sg[a[0]], a[1]), (sg[b[0]], b[1])))) for a, b in lab)
            orbit.add(img)
            stab += img == lab
        seen |= orbit
        out[(stab, en)] = out.get((stab, en), 0) + 1
    return out


def dp_levels(species, counts):
    """the same table from the fixed-point sums, by Moebius inversion and digit extraction"""
    c = sum(counts)
    N = sum(len(w) * n for w, n in zip(species, counts))
    K = math.ceil(N * math.log2(24)) + 1
    q = Fraction(1, 2 ** K)
    model = Model(lambda u: q ** e_hp(u), lambda l1, l2: q ** e_il(l1, l2), q ** E_MA, q ** E_MB, q ** E_MC)
    g = 0
    for n in counts:
        if n:
            g = math.gcd(g, n)
    F = {d: (G1(species, counts, model, 1) if d == 1 else Gd(species, counts, model, 1, d)) for d in divisors(g)}
    M = 6 * N + 10                                  # |energy| <= 3 per base pair + small terms: generous bound
    out = {}
    bits = 0
    for R in divisors(g):
        T = sum(mobius(d // R) * F[d] for d in divisors(g) if d % R == 0)
        X = T * 2 ** (K * M)
        assert X.denominator == 1 and X >= 0
        X = X.numerator
        bits = max(bits, X.bit_length())
        p = 0
        while X:
            digit = X & ((1 << K) - 1)
            if digit:
                m = M - p
                assert (digit * R) % c == 0
                out[(R, m)] = digit * R // c
            X >>= K
            p += 1
    # what a symmetry-naive (min,+) recursion returns: min over d of (least energy with symmetry a multiple of d) + ln d
    naive = None
    for d in divisors(g):
        ms = [m for (R, m) in out if R % d == 0]
        if ms:
            v = min(ms) + KT_LN(d)
            naive = v if naive is None else min(naive, v)
    return out, K, bits, naive


if __name__ == "__main__":
    cases = [
        (["GC"], [2]), (["GC"], [3]), (["GC"], [4]), (["GGCC"], [2]), (["GCGC"], [2]),
        (["GAC", "GTC"], [1, 1]), (["GAC", "GTC"], [2, 2]), (["GG", "CC"], [2, 2]), (["G", "C"], [3, 3]),
        (["GC", "AT"], [2, 2]), (["GGC", "GCC"], [2, 1]), (["GC"], [5]), (["GC"], [6]), (["GGCC"], [3]),
        (["GCGC", "GC"], [2, 2]), (["GG", "CC"], [3, 3]), (["GGACC"], [2]),
    ]
    ok = True
    differs = 0
    for species, counts in cases:
        t0 = time.time()
        b = brute_levels(species, counts)
        d, K, bits, naive = dp_levels(species, counts)
        good = b == d
        ok &= good
        mfe = min(m + KT_LN(R) for (R, m) in d) if d else None
        sym = sorted({R for (R, m) in d})
        flag = ""
        if naive is not None and mfe is not None and naive < mfe - 1e-12:
            differs += 1
            flag = f"   <-- the symmetry-naive value {naive:.3f} is below the true minimum"
        print(f"{list(zip(species, counts))}: {sum(d.values())} physical structures, symmetries {sym}, levels agree: {good};"
              f" K = {K}, largest number {bits} bits; MFE (loop energy + ln R) = "
              f"{'none (no connected structure)' if mfe is None else format(mfe, '.3f')}{flag}  [{time.time()-t0:.1f}s]",
              flush=True)
    print("ALL OK" if ok else "FAILURE", "| systems where the symmetry-naive (min,+) value is too low:", differs)
