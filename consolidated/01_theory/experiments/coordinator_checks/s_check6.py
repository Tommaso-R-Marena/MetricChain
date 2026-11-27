#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 6: the explicit bridge behind "gamma is not identically zero".

The walk is produced by the workstream's builder (experiments/workstreams/S/code/build.py: a box cut of a periodic
chain system, greedy linking, two tails); here it is only *checked*, with the coordinator's own code (s_lat.py):
valid self-avoiding lattice walk, bridge, and the profile (h3, h8, h11, gauche) from the definition.  Then
   2 h11 - 5 h3 - 8 N > 0,
which by Theorem 3.4 (distance <= 168/(N+3) to the limit set) and Theorem 4.2'(ii) (gauche density >= 2 p11 - 5 p3 - 8
for all limit points of walks) gives a point of the limit body where the gauche function is positive.

usage: s_check6.py PATH_TO_S_CODE "WITNESS" W   (W = box side; 128 reproduces the report, about 1-2 minutes)"""
import sys, os
from s_lat import valid_walk, is_bridge, profile


def main():
    code, wit, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
    sys.path.insert(0, code)
    import build
    hnf, ch = build.parse(wit)
    strands = build.strands_in_box(hnf, ch, (W, W, W))
    walk, nlink, dropped, ns = build.link(strands)
    b = build.make_bridge(walk)
    assert b is not None
    b = [tuple(int(c) for c in p) for p in b]
    assert valid_walk(b) and is_bridge(b)
    N = len(b)
    h3, h8, h11, g = profile(b)
    exc = 2 * h11 - 5 * h3 - 8 * N
    print(f"box {W}: bridge with N = {N} beads (own check: valid walk, bridge); (h3, h8, h11, g) = ({h3}, {h8}, {h11}, {g})")
    print(f"  2 h11 - 5 h3 - 8 N = {exc} = {exc / N:.4f} N;  g/N = {g / N:.4f};  168/(N+3) = {168 / (N + 3):.5f}")
    print(f"  => a point (p*, g*) of the limit set with 2 p11* - 5 p3* - 8 >= {exc / N - 2 * 168 / (N + 3):.4f}, hence gamma(p*) >= that")
    assert exc / N - 2 * 168 / (N + 3) > 0
    print("PART 6 OK")


if __name__ == "__main__":
    main()
