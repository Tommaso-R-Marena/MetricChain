#!/usr/bin/env python3
"""Check of the facts used in Proposition 5.5 about the two-rod strip R_{0,0} u R_{1,0}:
degrees inside the strip, the bonds between consecutive levels, and (brute force) that a strip of ell periods with
arbitrary short tails has no Hamiltonian path from a lowest to a highest site (small ell)."""
from lat import *
import lamella as lam
T = range(-40, 41)
strip = {lam.site(0, 0, t): ('rod0', t) for t in T} | {lam.site(1, 0, t): ('rod1', t) for t in T}
deg = {}
for p, (r, t) in strip.items():
    if abs(t) > 30: continue
    kind = (r, 'A' if t % 2 == 0 else 'B')
    d = sum(1 for q in nbrs(p) if q in strip)
    deg.setdefault(kind, set()).add(d)
print("degrees inside the strip:", deg)
# bonds between level y and y+1
for y in (10, 11, 12, 13):
    b = [(strip[p], strip[q]) for p in strip if p[1] == y for q in nbrs(p) if q in strip and q[1] == y + 1]
    print(f"bonds between levels {y} and {y+1}:", b)
# brute force: Hamiltonian paths of a finite strip (heights 2..2*ell-1 of both rods) from its lowest to its highest level
def ham_paths_bottom_to_top(S):
    S = set(S); ymin = min(p[1] for p in S); ymax = max(p[1] for p in S)
    cnt = 0
    def rec(p, seen):
        nonlocal cnt
        if len(seen) == len(S):
            if p[1] == ymax: cnt += 1
            return
        for q in nbrs(p):
            if q in S and q not in seen:
                seen.add(q); rec(q, seen); seen.discard(q)
    for s in S:
        if s[1] == ymin:
            rec(s, {s})
    return cnt
for ell in (3, 4, 5, 6):
    S = [p for p in strip if 2 <= p[1] <= 2 * ell - 1]
    print(f"ell = {ell}: {len(S)} sites; Hamiltonian paths from a lowest to a highest site: {ham_paths_bottom_to_top(S)}")
