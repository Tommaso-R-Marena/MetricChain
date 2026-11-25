#!/usr/bin/env python3
"""Finite checks of the lattice facts F1-F3 of section 3.1 and of the uniqueness statements of Lemma 2.3."""
import itertools
from collections import Counter
from lat import *

for name, o in (("A", (0, 0, 0)), ("B", (1, 1, 1))):
    nb = {d: [v for v in DISP[d] if is_site(add(o, v))] for d in (3, 8, 11)}
    print(f"site of type {name}: neighbours at squared distance 3, 8, 11: {[len(nb[d]) for d in (3, 8, 11)]};",
          "height differences:", {d: dict(sorted(Counter(v[1] for v in nb[d]).items())) for d in (3, 8, 11)})
    # common neighbours of second neighbours; three-bond paths to third neighbours
    N1 = set(nbrs(o))
    for d, want in ((8, 1), (11, 2)):
        cnt = Counter()
        for v in nb[d]:
            t = add(o, v)
            if d == 8:
                cnt[len(N1 & set(nbrs(t)))] += 1
            else:
                cnt[sum(1 for a in nbrs(o) for b in nbrs(a) if b != o and t in nbrs(b))] += 1
        print(f"   squared distance {d}: number of {'common neighbours' if d == 8 else 'three-bond paths'} -> {dict(cnt)} (expected all {want})")
    # third neighbours at graph distance 3 but squared distance 19 (trans)
    far = Counter(d2(o, c) for a in nbrs(o) for b in nbrs(a) if b != o for c in nbrs(b) if c != a)
    print("   squared distances of the end points of three-bond paths:", dict(far))
# F3: the eight maps act freely on ordered pairs (up-bond from A, up-bond from B)
UA = [a for a in A if a[1] == 1]; UB = [tuple(-c for c in a) for a in A if a[1] == -1]
star = {"A": set(A), "B": {tuple(-c for c in a) for a in A}}
ok = True
for M in YMAPS:
    img = {M(a) for a in A}
    ok &= (img == star["A"] or img == star["B"])
pairs = [(c, b) for c in UA for b in UB] + [(c, b) for c in UB for b in UA]
orbit = {(M(pairs[0][0]), M(pairs[0][1])) for M in YMAPS}
print("F3: every map sends the bond star of A to a bond star:", ok, "; orbit of one ordered pair of up-bonds has", len(orbit),
      "elements =", len(pairs), "ordered pairs:", orbit == set(pairs))
