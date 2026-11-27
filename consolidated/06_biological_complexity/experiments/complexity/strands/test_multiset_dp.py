"""Validation of multiset_dp.magnified_pf against exhaustive enumeration (ref_enum.py), exact rationals.

Brute force: enumerate all labelled connected unpseudoknotted structures (all circular orderings), compute the
product of loop weights, group into orbits under permutations of identical strands; a physical structure with
stabiliser of order R contributes  w**alpha / R**alpha."""
import sys, time
from fractions import Fraction
from itertools import permutations, product
from ref_enum import concat, noncrossing_matchings, faces, classify, COMPLEMENT
from multiset_dp import Model, magnified_pf, G1, Gd

def hp(u):
    return Fraction(1, 2 + u)

def il(l1, l2):
    if l1 == 0 and l2 == 0:
        return Fraction(3)                    # stack
    return Fraction(2, 3 + l1 + l2 + abs(l1 - l2))

MODEL = Model(hp, il, Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))

def face_weight(kind, f, m):
    if kind == "exterior":
        return Fraction(1)
    if kind == "hairpin":
        return Fraction(m.hp(len(f["unpaired"])))
    if kind in ("stack", "bulge", "interior"):
        return Fraction(m.il(f["segs"][0], f["segs"][1]))
    if kind == "multi":
        return m.ma * m.mb ** len(f["pairs"]) * m.mc ** len(f["unpaired"])
    raise ValueError(kind)

def brute(species, counts, m, alphas):
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
            w = Fraction(1)
            for f, kd in zip(fs, kinds):
                w *= face_weight(kd, f, m)
            lab = frozenset(tuple(sorted(((owner[i], idx[i]), (owner[j], idx[j])))) for i, j in pairs)
            assert lab not in structs
            structs[lab] = w
    # group of permutations of identical strands
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
    seen = set()
    out = {a: Fraction(0) for a in alphas}
    nphys = 0
    Rhist = {}
    for lab, w in structs.items():
        if lab in seen:
            continue
        orbit = set()
        stab = 0
        for sg in perms:
            img = frozenset(tuple(sorted(((sg[a[0]], a[1]), (sg[b[0]], b[1])))) for a, b in lab)
            orbit.add(img)
            if img == lab:
                stab += 1
        seen |= orbit
        assert len(orbit) * stab == len(perms)
        nphys += 1
        Rhist[stab] = Rhist.get(stab, 0) + 1
        for a in alphas:
            out[a] += w ** a / Fraction(stab) ** a
    return out, len(structs), nphys, Rhist

def run(species, counts, alphas=(0, 1, 2, 3)):
    t0 = time.time()
    b, nlab, nphys, Rhist = brute(species, counts, MODEL, alphas)
    t1 = time.time()
    ok = True
    for a in alphas:
        dp = magnified_pf(species, counts, MODEL, a)
        if dp != b[a]:
            ok = False
            print("   MISMATCH alpha", a, "dp", dp, "brute", b[a])
    print(f"{list(zip(species, counts))}: labelled structures {nlab}, physical {nphys}, symmetry histogram {Rhist}: "
          f"{'OK' if ok else 'FAIL'} for alpha in {alphas}  [brute {t1-t0:.1f}s, dp {time.time()-t1:.1f}s]", flush=True)
    return ok

if __name__ == "__main__":
    cases = [
        (["GC"], [1]), (["GGACC"], [1]), (["GGAACCAGGTCC"], [1]),
        (["GC"], [2]), (["GC"], [3]), (["GC"], [4]),
        (["GGCC"], [2]), (["GCGC"], [2]), (["GAC", "GTC"], [1, 1]), (["GAC", "GTC"], [2, 2]),
        (["GG", "CC"], [2, 2]), (["GG", "CC"], [3, 3]), (["G", "C"], [3, 3]),
        (["GC", "AT"], [2, 2]), (["GGC", "GCC"], [2, 1]), (["GCA", "TGC"], [2, 2]),
        (["GC"], [5]), (["GC"], [6]), (["GGCC"], [3]), (["GCGC", "GC"], [2, 2]),
    ]
    allok = True
    for sp, ct in cases:
        allok &= run(sp, ct)
    print("ALL OK" if allok else "SOME FAILED")
