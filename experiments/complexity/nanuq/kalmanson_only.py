"""Sharpness for 'Kalmanson' alone (Theorem 10' of docs/complexity/NANUQ_LOCAL_CRITERION.md).

K' = tree-generated circular split systems all of whose six-point restrictions have Phi6 >= 0 in every dihedral
placement (no condition on undisplayed splits).  This script
  (1) counts the six-point systems in K' and lists those outside the 127 six-locally good ones;
  (2) checks that every five-point tree-generated system with one leaf doubled has Phi6 >= 0 everywhere
      (closure of K' under replacing a leaf by a cherry; the note also proves this from Lemma 5);
  (3) for every six-point system with a negative Phi6 in some placement (u1; z, w; up; v1, vq), replaces z and w
      by caterpillar clades of m leaves and compares the exact weight of the split {u1, Z, W, up} | {v1, vq}
      with the closed formula   alpha(m) = 2*Phi4 + 2*m*(Phi5(z) + Phi5(w)) + 2*m^2*Phi6   (Phi6 = -1/2),
      for m = 1..6, and records the least m with a negative weight;
  (4) for the six systems of K' outside the 127, checks that all blow-ups by clades of up to 3 leaves at up to
      three positions (at most 10 leaves) have a Kalmanson metric (as Theorem 10'(a),(b) predicts).
The helper functions phi4, phi5, phi6 of local_terms.py return twice the quantities of the note.
"""
import itertools
import sys
from splitsys import *
from local_terms import phi4, phi5, phi6, displayed
from localcrit import dihedral_images, tree_generated_systems, local_ok, blowup


def min_phi6(n, sigma):
    best = None
    for img in dihedral_images(n, sigma):
        v = phi6(set(img), n, 0, 1, 2, 3, 4, 5)
        best = v if best is None else min(best, v)
    return best


def phi6_ok_all_restrictions(n, sigma):
    """Phi6 >= 0 on every six-point restriction, every placement."""
    for Y in itertools.combinations(range(n), 6):
        idx = {y: k for k, y in enumerate(Y)}
        rest = set()
        for m in sigma:
            mm = 0
            for y in Y:
                if (m >> y) & 1:
                    mm |= 1 << idx[y]
            if mm != 0 and mm != 63:
                rest.add(canon(6, mm))
        if min_phi6(6, frozenset(rest)) < 0:
            return False
    return True


if __name__ == "__main__" and len(sys.argv) == 1:
    T6 = sorted(tree_generated_systems(6), key=lambda s: (len(s), sorted(s)))
    good = [s for s in T6 if local_ok(6, s)[0]]
    kprime = [s for s in T6 if min_phi6(6, s) >= 0]
    extra = [s for s in kprime if s not in set(good)]
    print(f"(1) six-point tree-generated systems: {len(T6)}; locally good: {len(good)}; with all Phi6 >= 0 (K'): {len(kprime)}; "
          f"in K' but not locally good: {len(extra)}")
    for s in extra:
        missing = sorted(set(all_circular_splits(6)) - set(s))
        print("     missing splits:", [bin(m)[2:].zfill(6) for m in missing if not is_trivial(6, m)])
    # (2) doubled five-point systems
    ok = True
    for s in tree_generated_systems(5):
        for k in range(5):
            n2, s2 = blowup(5, s, [2 if p == k else 1 for p in range(5)])
            ok &= min_phi6(6, frozenset(s2)) >= 0
    print("(2) every five-point tree-generated system with a doubled leaf has Phi6 >= 0 in all placements:", ok)
    # (3) blow-ups of the systems with a negative Phi6
    neg = [s for s in T6 if min_phi6(6, s) < 0]
    print(f"(3) systems with some Phi6 < 0: {len(neg)}")
    formula_ok, least = True, []
    for s in neg:
        # a dihedral image with phi6(0; 1, 2; 3; 4, 5) < 0; blow up the points 1 (z) and 2 (w)
        img = next(i for i in sorted(dihedral_images(6, s), key=sorted) if phi6(set(i), 6, 0, 1, 2, 3, 4, 5) < 0)
        si = set(img)
        p4 = phi4(si, 6, 0, 3, 4, 5)
        p5z, p5w = phi5(si, 6, 0, 1, 3, 4, 5), phi5(si, 6, 0, 2, 3, 4, 5)
        p6 = phi6(si, 6, 0, 1, 2, 3, 4, 5)
        vals = []
        for m in range(1, 7):
            n2, s2 = blowup(6, img, [m if p in (1, 2) else 1 for p in range(6)])
            D = nanuq_2d(n2, s2)
            al = alphas_2(n2, D)
            # gap i lies between point i and point i+1; the split with gaps (2m+1, n2-1) is {v1, vq} | the rest
            i, j = 2 * m + 1, n2 - 1
            assert al[(i, j)] % 2 == 0
            vals.append(al[(i, j)] // 2)
            formula_ok &= vals[-1] == p4 + m * (p5z + p5w) + m * m * p6
        least.append(next(m for m, v in enumerate(vals, 1) if v < 0))
        print(f"     2Phi4 = {p4}, 2Phi5(z), 2Phi5(w) = {p5z}, {p5w}, 2Phi6 = {p6};  weights for m = 1..6: {vals};  least m with a negative weight: {least[-1]}")
    print("    closed formula alpha(m) = 2Phi4 + 2m(Phi5(z)+Phi5(w)) + 2m^2 Phi6 agrees in all cases:", formula_ok)
    print("    largest 'least m':", max(least), "(so at most", 2 * max(least) + 4, "leaves)")
    # (4) the extra systems: Kalmanson in all blow-ups tried
    okk = True
    cnt = 0
    for s in extra:
        for pos in itertools.combinations(range(6), 3):
            for sizes in itertools.product((1, 2, 3), repeat=3):
                if sum(sizes) - 3 + 6 > 10:
                    continue
                mult = [1] * 6
                for pp, zz in zip(pos, sizes):
                    mult[pp] = zz
                n2, s2 = blowup(6, s, mult)
                D = nanuq_2d(n2, s2)
                al = alphas_2(n2, D)
                cnt += 1
                okk &= min(al.values()) >= 0
    print(f"(4) the {len(extra)} systems of K' outside the 127: {cnt} blow-ups (clades of up to 3 leaves at three positions, at most 10 leaves), all Kalmanson:", okk)


# ----------------------------------------------------------------------------------------------------------------
# (5), (6): added checks.  Run with  python3 kalmanson_only.py extra
# ----------------------------------------------------------------------------------------------------------------

def three_splits(n=6):
    return {canon(6, 0b000111), canon(6, 0b001110), canon(6, 0b011100)}


def kalmanson_for_some_order(n, D):
    """Is the symmetric matrix D Kalmanson for SOME circular order?  Backtracking over orders x_0 = 0, ..., with
    the four-point Kalmanson conditions on every 4-subset of the prefix (they are hereditary).  Returns an order
    or None."""
    def ok4(a, b, c, d):               # a, b, c, d in circular order
        s = D[a][c] + D[b][d]
        return s >= D[a][b] + D[c][d] and s >= D[a][d] + D[b][c]

    order = [0]
    used = [False] * n
    used[0] = True

    def rec():
        k = len(order)
        if k == n:
            return order[1] < order[-1]        # one of the two reflections
        for x in range(1, n):
            if used[x]:
                continue
            good = True
            for i in range(k):
                for j in range(i + 1, k):
                    for l in range(j + 1, k):
                        if not ok4(order[i], order[j], order[l], x):
                            good = False
                            break
                    if not good:
                        break
                if not good:
                    break
            if good:
                order.append(x)
                used[x] = True
                if rec():
                    return True
                order.pop()
                used[x] = False
        return False

    return list(order) if rec() else None


def extra():
    T6 = sorted(tree_generated_systems(6), key=lambda s: (len(s), sorted(s)))
    three = three_splits()
    two = [canon(6, 0b000011 << k if k < 5 else 0b100001) for k in range(6)]
    # (5) Lemma 5': Phi6 < 0 at (u1; z, w; up; v1, vq) iff the three 3-splits are present and the 2-split {z, w} is not
    ok5 = True
    for s in T6:
        for img in dihedral_images(6, s):
            si = set(img)
            neg = phi6(si, 6, 0, 1, 2, 3, 4, 5) < 0
            pred = three <= si and canon(6, 0b000110) not in si
            ok5 &= (neg == pred)
    cnt = sum(1 for s in T6 if three <= set(s) and not all(t in s for t in two))
    print("(5) Phi6 < 0 at (u1; z, w; up; v1, vq)  <=>  all three 3-splits present and the 2-split {z, w} absent:", ok5)
    print("    six-point tree-generated systems with the three 3-splits and a missing 2-split:", cnt)
    # sanity test of the order search: it finds an order for metrics that are Kalmanson (all 133 systems of K',
    # relabelled by a fixed scrambling permutation so that the natural order is not the first one tried)
    perm = [3, 0, 5, 1, 4, 2]
    sane = True
    for s in T6:
        if min_phi6(6, s) < 0:
            continue
        D = nanuq_2d(6, set(s))
        D2 = [[D[perm[a]][perm[b]] for b in range(6)] for a in range(6)]
        o = kalmanson_for_some_order(6, D2)
        sane &= o is not None
        if o is not None:
            Do = [[D2[o[a]][o[b]] for b in range(6)] for a in range(6)]
            sane &= min(alphas_2(6, Do).values()) >= 0
    print("    sanity: the order search finds a Kalmanson order for all 133 scrambled metrics of K'_6:", sane)
    # (6) the blow-ups of (3) are not Kalmanson for ANY circular order
    neg = [s for s in T6 if min_phi6(6, s) < 0]
    none_any = True
    for s in neg:
        img = next(i for i in sorted(dihedral_images(6, s), key=sorted) if phi6(set(i), 6, 0, 1, 2, 3, 4, 5) < 0)
        for m in (1, 2, 3):
            n2, s2 = blowup(6, img, [m if p in (1, 2) else 1 for p in range(6)])
            D = nanuq_2d(n2, s2)
            al = alphas_2(n2, D)
            if min(al.values()) < 0:
                break
        order = kalmanson_for_some_order(n2, D)
        print(f"     least failing blow-up m = {m} ({n2} leaves): Kalmanson for some other circular order: {order}")
        none_any &= order is None
    print("(6) none of the 17 least failing blow-ups is Kalmanson for any circular order:", none_any)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "extra":
    extra()
