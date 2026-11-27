# t2_sixpoint.py -- REVIEWER'S OWN CODE: the six-point facts of Sections 3, 7, 7.1
import itertools, collections
from fractions import Fraction
from mysplits import *

n = 6
TG = {k: tree_generated(k) for k in (3, 4, 5, 6)}
print("tree-generated systems on 3,4,5,6 points:", [len(TG[k]) for k in (3, 4, 5, 6)], " planar trees:", [len(planar_trees(k)) for k in (4, 5, 6)])
gg = [S for S in TG[6] if globally_good(S, 6)]
lg = [S for S in TG[6] if six_locally_good_6(S)]
kal = [S for S in TG[6] if kalmanson_identity(S, 6)]
print("globally good (Kalmanson, exact support):", len(gg), " 6-locally good:", len(lg), " Kalmanson for the given order:", len(kal))
assert set(lg) <= set(gg)

# the nine non-trivial splits of six points
three = [norm(interval(i, i + 3, 6), 6) for i in range(3)]
three = sorted(set(three))
two = sorted({norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)})
assert len(three) == 3 and len(two) == 6
for a in three:
    for b in three:
        if a != b:
            assert not compatible(a, b, 6)
for t in two:
    inc = [a for a in three if not compatible(t, a, 6)]
    assert len(inc) == 1

# Corollary 5': Phi6 < 0 iff the three 3-splits are present and the 2-split {z,w} is absent
bad = 0; cnt = 0; neg = 0; vals = collections.Counter()
for S in TG[6]:
    for lab in dihedral_labellings(range(6)):
        u1, z, w, up, v1, vq = lab
        f = phi6_any(S, u1, z, w, up, v1, vq)
        vals[f] += 1
        zw = norm((1 << z) | (1 << w), 6)
        pred = all(a in S for a in three) and zw not in S
        cnt += 1
        neg += f < 0
        if (f < 0) != pred:
            bad += 1
print("Corollary 5': labellings checked", cnt, " with Phi6<0:", neg, " mismatches:", bad, " values of Phi6:", dict(vals))

# Theorem 10'(d): systems containing the three 3-splits and missing a 2-split
pat = [S for S in TG[6] if all(a in S for a in three) and any(t not in S for t in two)]
print("systems with the three 3-splits and a missing 2-split:", len(pat), " -> |K'_6| =", 150 - len(pat))
def missing_type(S):
    miss = [i for i in range(6) if norm((1 << i) | (1 << ((i + 1) % 6)), 6) not in S]
    if len(miss) == 1: return 'one 2-split'
    if len(miss) == 2:
        d = (miss[1] - miss[0]) % 6
        return {3: 'two antipodal', 2: 'two at distance two', 4: 'two at distance two'}.get(d, 'two adjacent?')
    if len(miss) == 3: return 'three alternate'
    return 'other %s' % miss
print("  by type:", dict(collections.Counter(missing_type(S) for S in pat)))
Kp = [S for S in TG[6] if S not in pat]
notlg = [S for S in Kp if not six_locally_good_6(S)]
print("  in K'_6 but not 6-locally good:", len(notlg))
def is_minus_2_and_crossing3(S):
    allnine = set(two) | set(three)
    miss = [s for s in allnine if s not in S]
    if len(miss) != 2: return False
    t = [s for s in miss if s in two]; a = [s for s in miss if s in three]
    return len(t) == 1 and len(a) == 1 and not compatible(t[0], a[0], 6)
print("  all of these are 'nine minus a 2-split and the 3-split incompatible with it':", all(is_minus_2_and_crossing3(S) for S in notlg))
print("  of the 17: Kalmanson (given order) on six points:", sum(kalmanson_identity(S, 6) for S in pat), " globally good:", sum(globally_good(S, 6) for S in pat))
print("  the 133 of K'_6 all Kalmanson for the given order:", all(kalmanson_identity(S, 6) for S in Kp), "; with alpha>0 on every split of the system:",
      all(all(a > 0 for (i, j), a in alpha2(nanuq2(S, 6)).items() if split_ij(i, j, 6) in S) for S in Kp))
# 9 global failures of Theorem 10(a)
fail = [S for S in TG[6] if S not in gg]
def describe(S):
    allnine = set(two) | set(three)
    miss = sorted(s for s in allnine if s not in S)
    return tuple(sorted(bin(s).count('1') for s in miss)), show(frozenset(miss) , 6)
print("global failures:", len(fail))
for S in fail:
    M = nanuq2(S, 6); al = alpha2(M)
    negs = [(i, j) for (i, j), a in al.items() if a < 0]
    wrong = [(i, j) for (i, j), a in al.items() if a > 0 and split_ij(i, j, 6) not in S]
    print("   missing:", describe(S), " negative:", len(negs), " positive on undisplayed:", len(wrong))

# Step 1 of Theorem 12: substitutions of tree-generated systems with 3+5, 4+4, 5+3 leaves on six points
subs = set(); nsub = 0; nbad = 0
for n1, n2 in ((3, 5), (4, 4), (5, 3)):
    for S1 in TG[n1]:
        for S2 in TG[n2]:
            for p in range(n1):
                for r in range(n2):
                    S, nn = substitute(S1, n1, p, S2, n2, r)
                    assert nn == 6
                    nsub += 1
                    subs.add(S)
                    if not six_locally_good_6(S):
                        nbad += 1
print("substitutions (S1,S2,p,r) with 3+5,4+4,5+3 leaves:", nsub, " distinct systems:", len(subs), " not 6-locally good:", nbad)
# count as the note may count: p fixed? report a few alternative counts
c2 = 0
for n1, n2 in ((3, 5), (4, 4), (5, 3)):
    c2 += len(TG[n1]) * len(TG[n2]) * 6
print("  (alternative count: |TG_n1|*|TG_n2|*6 rotations summed = %d)" % c2)
# are all tree-generated systems on <= 5 points in class A? (count only)
print("all subs tree-generated:", all(S in set(TG[6]) for S in subs))
