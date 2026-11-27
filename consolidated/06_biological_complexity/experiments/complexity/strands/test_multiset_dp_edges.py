"""Edge cases of multiset_dp added after COMPLEXITY-REV-0003 (finding 5):
  (a) identical sequences given as two species are refused;
  (b) a minimum hairpin size as a pairing constraint: dynamic programme against exhaustive enumeration for
      alpha = 0, 1, 2, -1 (the encoding by weight 0 is wrong at alpha = 0 and impossible at alpha < 0);
  (c) weight 0 at magnification <= 0 raises."""
from fractions import Fraction
from itertools import permutations, product
from ref_enum import concat, noncrossing_matchings, faces, classify, COMPLEMENT
from multiset_dp import Model, magnified_pf

MINHP = 3
hp = lambda u: Fraction(1, 2 + u)
def il(l1, l2):
    return Fraction(3) if (l1 == 0 and l2 == 0) else Fraction(2, 3 + l1 + l2 + abs(l1 - l2))
MODEL = Model(hp, il, Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), min_hairpin=MINHP)


def face_weight(kind, f, m):
    if kind == "exterior":
        return Fraction(1)
    if kind == "hairpin":
        return Fraction(m.hp(len(f["unpaired"])))
    if kind in ("stack", "bulge", "interior"):
        return Fraction(m.il(f["segs"][0], f["segs"][1]))
    return m.ma * m.mb ** len(f["pairs"]) * m.mc ** len(f["unpaired"])


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
            if any(kd == "hairpin" and len(f["unpaired"]) < m.min_hairpin for f, kd in zip(fs, kinds)):
                continue
            w = Fraction(1)
            for f, kd in zip(fs, kinds):
                w *= face_weight(kd, f, m)
            lab = frozenset(tuple(sorted(((owner[i], idx[i]), (owner[j], idx[j])))) for i, j in pairs)
            structs[lab] = w
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
    for lab, w in structs.items():
        if lab in seen:
            continue
        orbit, stab = set(), 0
        for sg in perms:
            img = frozenset(tuple(sorted(((sg[a[0]], a[1]), (sg[b[0]], b[1])))) for a, b in lab)
            orbit.add(img)
            stab += img == lab
        seen |= orbit
        for a in alphas:
            out[a] += w ** a / Fraction(stab) ** a
    return out


if __name__ == "__main__":
    ok = True
    # (a)
    try:
        magnified_pf(["GC", "GC"], [1, 1], MODEL, 1)
        ok = False
        print("(a) FAIL: duplicate species accepted")
    except ValueError:
        print("(a) duplicate species are refused: True")
    # (b)
    alphas = (0, 1, 2, -1)
    cases = [(["GGAAACC"], [1]), (["GGAAACC"], [2]), (["GCAAAGC"], [2]), (["GGAAACC", "GG"], [1, 2]),
             (["GAAAC", "G", "C"], [1, 1, 1]), (["GCAAAAGC"], [2]), (["GGAAACC", "CC"], [2, 2]), (["GAAAC"], [3])]
    for species, counts in cases:
        b = brute(species, counts, MODEL, alphas)
        good = all(magnified_pf(species, counts, MODEL, a) == b[a] for a in alphas)
        ok &= good
        print(f"(b) {list(zip(species, counts))}: min_hairpin = {MINHP}, alpha in {alphas}: {'OK' if good else 'FAIL'}")
    # (c)
    zero = Model(lambda u: Fraction(0) if u < 3 else Fraction(1), il, 1, 1, 1)
    for a in (0, -1):
        try:
            magnified_pf(["GCGC"], [1], zero, a)
            ok = False
            print(f"(c) FAIL: weight 0 accepted at alpha = {a}")
        except ValueError:
            print(f"(c) weight 0 at alpha = {a} raises: True")
    print("ALL OK" if ok else "FAILURE")
