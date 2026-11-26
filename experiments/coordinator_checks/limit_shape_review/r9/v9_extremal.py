#!/usr/bin/env python3
"""V9 -- Theorem R9.1(d): is beta = 60 attained, and the arithmetic of 108/(N+3).

1. Takes from the output of `v9_cobound single NMAX ...` the first (x1, c1) with A = (1,6,10;1) and the first x2 with
   B = (0,3,4;0) (my own exhaustive search), re-verifies both with the Python implementation, builds the REAL
   concatenation from coordinates and compares its (h,g) with the sum: error vector and norm.
2. Optionally (second argument) the same for an example given in a file of the reviewed division (their OUTPUT
   `out/extremal.txt`, coordinates only; read after part 1 was done).
3. The arithmetic of 108: exact, with the box [0,1]x[0,5]x[0,6]x[0,1] and the bounds A <= (1,6,10;1), B <= (0,3,4;0),
   and a brute-force maximisation of ||3 (h,g)/N - (A+B)|| over the vertices of the two boxes.
usage: v9_extremal.py OUT_SINGLE [THEIR_EXTREMAL]
"""
import sys, re, itertools
sys.dont_write_bytecode = True
from fractions import Fraction as Fr
from v9_lib import *


def parse_walk(s):
    return [tuple(int(t) for t in m.groups()) for m in re.finditer(r"\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", s)]


xa = ca = xb = None
for line in open(sys.argv[1]):
    if line.startswith("first (x, c1) with A = (1,6,10;1)"):
        m = re.search(r"N = (\d+), c1 = \((-?\d+),(-?\d+),(-?\d+)\): (.*)", line)
        ca = tuple(int(t) for t in m.groups()[1:4])
        xa = parse_walk(m.group(5))
        assert len(xa) == int(m.group(1))
    if line.startswith("first x with B = (0,3,4;0)"):
        m = re.search(r"N = (\d+): (.*)", line)
        xb = parse_walk(m.group(2))
        assert len(xb) == int(m.group(1))
assert xa and xb, "extremal examples not found in the output"


def verify(x1, c1, x2, label):
    check_bridge(x1)
    check_bridge(x2)
    assert c1 in admissible(x1)
    A1 = A_of(x1, c1)
    B2 = B_of(x2)
    y, g = concat(x1, c1, x2)
    check_bridge(y)
    hy = ML.profile_hash(y)
    assert hy == ML.profile_bruteforce(y) == ML.profile_kdtree(y)
    h1 = ML.profile_bruteforce(x1)
    h2 = ML.profile_bruteforce(x2)
    err = tuple(hy[k] - h1[k] - h2[k] for k in range(4))
    print(f"{label}: N1 = {len(x1)}, N2 = {len(x2)}, c1 = {c1}")
    print(f"   x1 = {x1}")
    print(f"   x2 = {x2}")
    print(f"   A(x1, c1) = {A1}, B(x2) = {B2}; (h,g)(x1) = {h1}, (h,g)(x2) = {h2}")
    print(f"   real concatenation: {len(y)} beads, self-avoiding bridge, (h,g) = {hy} (three counts agree)")
    print(f"   error vector = {err}, norm ||.||_c + |.| = {nrm(err)}   [A + B = {vadd(A1, B2)}]")
    assert err == vadd(A1, B2)
    return err


print("1. own extremal pair (from my exhaustive enumeration)")
e = verify(xa, ca, xb, "   own")
assert e == (1, 9, 14, 1) and nrm(e) == 60
print("   => the bound (1, 9, 14; 1), norm 60 = beta, of Lemma 11.68 is attained with N1 = 21, N2 = 14.")
# the structure of the top end of xa: which beads are seen by t1, t2, t3
idx = index_of(xa)
t = sites_above(xa, ca)
for j, s in enumerate(t):
    seen = []
    for d in (3, 8, 11):
        for v in DISP[d]:
            q = add(s, v)
            if q in idx and (len(xa) + j) - idx[q] >= 3:
                seen.append((idx[q], d))
    print(f"   t{j+1} = {s} sees beads (index, squared distance): {sorted(seen)}")

if len(sys.argv) > 2:
    print("\n2. the example of the reviewed division (coordinates read from their output file)")
    txt = open(sys.argv[2]).read()
    walks = []
    for line in txt.splitlines():
        w = parse_walk(line)
        if len(w) >= 3:
            walks.append(w)
    print(f"   coordinate lists found in the file: lengths {[len(w) for w in walks]}")
    cand1 = [w for w in walks if len(w) == 21]
    cand2 = [w for w in walks if len(w) == 14]
    done = False
    for w1 in cand1:
        for w2 in cand2:
            try:
                check_bridge(w1)
                check_bridge(w2)
            except AssertionError:
                continue
            for c in admissible(w1):
                if A_of(w1, c) == (1, 6, 10, 1) and B_of(w2) == (0, 3, 4, 0):
                    e2 = verify(w1, c, w2, "   theirs")
                    assert e2 == (1, 9, 14, 1)
                    done = True
    print("   their example verified from coordinates:", done)

print("\n3. the arithmetic of 108/(N+3)")
# (h,g)/N - qhat/(N+3) = [3 (h,g)/N - (A+B)] / (N+3)
N = Fr(1000)
hgx = (Fr(7), Fr(11), Fr(13), Fr(5))
AB = (Fr(1), Fr(2), Fr(3), Fr(1))
lhs = tuple(hgx[k] / N - (hgx[k] + AB[k]) / (N + 3) for k in range(4))
rhs = tuple((3 * hgx[k] / N - AB[k]) / (N + 3) for k in range(4))
assert lhs == rhs
print("   identity (h,g)/N - q-hat/(N+3) = [3 (h,g)/N - (A + B)]/(N+3): checked in rationals")
box = (1, 5, 6, 1)                 # (h,g)/N in [0,1]x[0,5]x[0,6]x[0,1]
ABmax = (1, 9, 14, 1)              # A + B <= (1,6,10;1) + (0,3,4;0)
best = 0
arg = None
for u in itertools.product(*[(0, 3 * b) for b in box]):
    for v in itertools.product(*[(0, m) for m in ABmax]):
        d = tuple(u[k] - v[k] for k in range(4))
        if nrm(d) > best:
            best, arg = nrm(d), (u, v)
print(f"   max of ||u - v|| over the vertices u of 3 x box and v of [0, A+B max] (the norm is convex, so this is the maximum over both boxes): {best} at {arg}")
print(f"   R9's count: cumulative coordinates a <= 3, b <= 18, c <= 36, g <= 3 against 1, 10, 24, 1: 5*3 + 3*18 + 36 + 3 = {5*3 + 3*18 + 36 + 3};  3R = 3*36 = {3*36}")
assert best == 108
print("   norm of the box corner: R = 9*1 + 4*5 + 6 + 1 =", 9 + 20 + 6 + 1, "; beta = norm of (1,9,14;1) =", nrm((1, 9, 14, 1)))
