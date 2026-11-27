#!/usr/bin/env python3
"""R13 / item 2, Proposition 11.69b as replaced: the finite arithmetic of the statement, re-done (exact integers).
(1) determinants of the three five-vector sets (h3,h8,h11,g; N+3): ours (R9.1(e)), theirs (4,5,7,8,10 beads), ours of SCI-REV-0011 sec. 4;
(2) the norm  ||(h3,h8,h11;g)|| = 5|a| + 3|b| + |c| + |g|,  (a,b,c) = (h3, h3+h8, h3+h8+h11), of the bounds A <= (1,6,10;1), B <= (0,3,4;0),
    their sum, and the constant 108 of (d);
(3) the two bridges of out/certificate.txt (4 and 5 beads) from their coordinates: profile (pairs at chain separation >= 3 with squared
    distance 3, 8, 11) and number of gauche torsions, by the definition.
"""
from fractions import Fraction as Fr
from sympy import Matrix

sets = {
 "R9.1(e), bridges with 4,5,9,9,11 beads": [(0,0,1,1,7),(0,0,1,1,8),(0,2,6,5,12),(0,3,6,4,12),(1,6,11,7,14)],
 "theory report 11.69b(e), 4,5,7,8,10 beads": [(0,0,1,1,7),(0,0,1,1,8),(0,1,3,3,10),(0,1,5,4,11),(1,4,6,5,13)],
 "SCI-REV-0011 sec. 4, 10,10,8,10,10 beads": [(0,0,6,6,13),(1,4,6,5,13),(0,3,6,4,11),(0,1,6,5,13),(0,2,7,6,13)],
}
print("# r13_08_r9_arith.py")
for name, rows in sets.items():
    print(f"  det [{name}] = {Matrix(rows).det()};  projection to (h3,h8,h11;M): rank {Matrix([r[:3]+r[4:] for r in rows]).rank()}, "
          f"gcd of 4x4 minors = {__import__('math').gcd(*[int(Matrix([ (r[:3]+r[4:]) for i,r in enumerate(rows) if i != k]).det()) for k in range(5)])}")
def norm(v):
    a, b, c, g = v[0], v[0]+v[1], v[0]+v[1]+v[2], v[3]
    return 5*abs(a) + 3*abs(b) + abs(c) + abs(g)
A, B = (1,6,10,1), (0,3,4,0)
print(f"  norm A_max = {norm(A)}, norm B_max = {norm(B)}, norm (A+B)_max = {norm(tuple(x+y for x,y in zip(A,B)))}  [(1,9,14;1)]")
print(f"  108 = 5*3 + 3*18 + 36 + 3 = {5*3 + 3*18 + 36 + 3};  cumulative bound of A+B: (1, 10, 24; 1) -> {(A[0]+B[0], A[0]+B[0]+A[1]+B[1], sum(A[:3])+sum(B[:3]), 1)};  168 = 60 + 108: {60 + 108}")
def stats(w):
    n = len(w)
    bonds = [tuple(w[i+1][k]-w[i][k] for k in range(3)) for i in range(n-1)]
    assert all(sum(c*c for c in b) == 3 for b in bonds)
    h = {3: 0, 8: 0, 11: 0}
    for i in range(n):
        for j in range(i+3, n):
            d2 = sum((w[i][k]-w[j][k])**2 for k in range(3))
            if d2 in h: h[d2] += 1
    g = sum(1 for i in range(n-3) if bonds[i+2] != bonds[i])
    return (h[3], h[8], h[11], g, n+3)
for w in ([(0,0,0),(1,1,1),(0,2,2),(-1,3,1)], [(0,0,0),(1,1,1),(0,2,2),(1,3,3),(2,4,2)],
          [(0,0,0),(1,1,1),(0,2,2),(-1,3,1),(-2,2,0),(-3,3,-1),(-4,4,0)],
          [(0,0,0),(1,1,1),(0,2,2),(1,3,3),(0,4,4),(-1,5,3),(-2,4,2),(-1,3,1),(0,4,0),(1,5,1)]):
    print(f"  bridge of out/certificate.txt with {len(w)} beads: (h3,h8,h11,g; N+3) = {stats(w)}")
print("# END")
