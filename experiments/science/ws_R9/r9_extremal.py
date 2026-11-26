#!/usr/bin/env python3
"""R9: the constants of Lemma 11.68 are attained.  Input: out/extremal_raw.txt (bin/r9_extremal 21 14: the first 21-bead
bridge with A-part (1,6,10;1) and the first 14-bead bridge with B-part (0,3,4) found by the enumeration).
Here, from coordinates (r9_lat.py): both are bridges, their end corrections are as stated, and their REAL concatenation
has (h,g) = (h,g)(x1) + (h,g)(x2) + (1, 9, 14, 1) — the bound of Lemma 11.68, of norm beta = 60."""
import sys
sys.dont_write_bytecode = True
import r9_lat as L
rows = {}
for line in open("out/extremal_raw.txt"):
    a = line.split()
    n = int(a[1]); c1 = tuple(int(t) for t in a[2:5]); co = [int(t) for t in a[5:]]
    rows[a[0]] = (c1, [tuple(co[3 * i:3 * i + 3]) for i in range(n)])
c1, x1 = rows["A"]; _, x2 = rows["B"]
for nm, x in (("x1", x1), ("x2", x2)):
    assert L.check_walk(x) is None and L.is_bridge(x)
    assert L.profile(x) == L.profile_brute(x)
print("x1:", len(x1), "beads, (h,g) =", L.profile(x1), " admissible c1:", L.admissible_c1(x1), " A(x1, c1) =", L.A_part(x1, c1))
print("x2:", len(x2), "beads, (h,g) =", L.profile(x2), " B(x2) =", L.B_part(x2))
y, g = L.concat(x1, x2, c1)
assert L.check_walk(y) is None and L.is_bridge(y) and len(y) == len(x1) + len(x2) + 3
hy, h1, h2 = L.profile_brute(y), L.profile(x1), L.profile(x2)
err = tuple(hy[i] - h1[i] - h2[i] for i in range(4))
print("concatenation:", len(y), "beads, a self-avoiding bridge; error vector (O(n^2) count) =", err, " norm 9*d3 + 4*d8 + d11 + dg =", 9 * err[0] + 4 * err[1] + err[2] + err[3])
print("x1 =", x1)
print("x2 =", x2)
