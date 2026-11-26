#!/usr/bin/env python3
"""R25, Item 1 -- controls for the checks of t1c_levelA.py that had none of their own (own code).

Usage: python3 -B t1c_controls_extra.py QMAX

The checks concerned (all with 0 violations in runs 21-23):
  U  uniqueness of the circular ordering of a CONNECTED unpseudoknotted pair set          (part1)
  F  Fact 1: connected  <=>  no face with two or more nicks                               (part2)
  T  tiling structure (definition of section 2)  <=>  every item bond lies on a stack     (part2)
Controls, each of which must produce violations:
  U' the same uniqueness claim for ALL pair sets (connectivity dropped)
  F' Fact 1 with 'three or more nicks' in place of 'two or more'
  T' 'tiling  <=>  every base is paired'  (false: an item may straddle a separator)
  T'' 'tiling <=>  no bulge and no interior loop'  (false for structures with unpaired G's)
"""
import sys
import time
import itertools

import nn_model as nn


def all_pair_sets_orders(m, B, sizes):
    """every partial G-C matching of the labelled instance with the list of labelled orders for which it is
    non-crossing (as nn.level_0, but without the restriction to connected pair sets)"""
    tl = nn.template(m, B)
    n = len(sizes)
    Gs = [(0, i) for i in range(len(tl)) if tl[i] == "G"]
    Cs = [(s + 1, i) for s in range(n) for i in range(sizes[s])]
    orders = list(itertools.permutations(range(1, n + 1)))
    pos_maps = []
    for od in orders:
        pm = {}
        p = 0
        for i in range(len(tl)):
            pm[(0, i)] = p
            p += 1
        for s in od:
            for i in range(sizes[s - 1]):
                pm[(s, i)] = p
                p += 1
        pos_maps.append(pm)
    multi = total = 0
    for k in range(0, min(len(Gs), len(Cs)) + 1):
        for gsub in itertools.combinations(Gs, k):
            for cperm in itertools.permutations(Cs, k):
                pairs = tuple(zip(gsub, cperm))
                total += 1
                good = 0
                for pm in pos_maps:
                    ch = [tuple(sorted((pm[g], pm[c]))) for (g, c) in pairs]
                    ok = True
                    for u in range(len(ch)):
                        for v in range(u + 1, len(ch)):
                            if nn.chords_cross(ch[u][0], ch[u][1], ch[v][0], ch[v][1]):
                                ok = False
                                break
                        if not ok:
                            break
                    good += ok
                if good >= 2:
                    multi += 1
    return total, multi


def main():
    t0 = time.time()
    qmax = int(sys.argv[1])
    tiny = [(1, 2, (1, 1)), (2, 1, (1, 1)), (1, 3, (1, 2)), (2, 2, (2, 2)), (2, 2, (1, 1, 2)), (2, 2, (3, 1)),
            (1, 4, (1, 1, 2)), (2, 3, (2, 2, 2)), (3, 2, (1, 1, 2, 2))]
    tot = mul = 0
    for (m, B, sizes) in tiny:
        a, b = all_pair_sets_orders(m, B, sizes)
        tot += a
        mul += b
    print(f"U' control (uniqueness of the ordering without connectivity): {mul} of {tot} pair sets of {len(tiny)} "
          f"labelled instances with two or more items are non-crossing for two or more orders")
    f3 = t1 = t2 = nstruct = nnc = 0
    for m in range(1, qmax + 1):
        for B in range(1, qmax + 1):
            if m * B > qmax:
                continue
            for order in nn.compositions(m * B):
                circ = nn.Circle([nn.template(m, B)] + ["C" * a for a in order])
                box = [0, 0, 0, 0, 0]

                def leaf(partner, circ=circ, box=box, m=m, B=B):
                    box[4] += 1
                    conn = nn.is_connected(circ, partner)
                    fs = nn.faces(circ, partner)
                    three = any(sum(1 for i in f[0] if circ.nick[i]) >= 3 for f in fs)
                    if conn == three:
                        box[0] += 1
                    if conn:
                        box[3] += 1
                        til = nn.tiling_by_definition(circ, partner, m, B)
                        allpaired = all(partner[p] != -1 for p in range(circ.N) if circ.letters[p] != "A")
                        if til != allpaired:
                            box[1] += 1
                        s = nn.signature(circ, partner, m, B)
                        if til != (s[3] == 0):
                            box[2] += 1

                nn.enumerate_noncrossing(circ, leaf)
                f3 += box[0]
                t1 += box[1]
                t2 += box[2]
                nstruct += box[3]
                nnc += box[4]
    print(f"families with mB <= {qmax}: {nnc} non-crossing pair sets, {nstruct} connected structures")
    print(f"F' control (Fact 1 with 'three or more nicks'): {f3} violations")
    print(f"T' control ('tiling iff every base paired'): {t1} violations")
    print(f"T'' control ('tiling iff no bulge and no interior loop'): {t2} violations")
    print(f"time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
