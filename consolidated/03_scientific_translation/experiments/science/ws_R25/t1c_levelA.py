#!/usr/bin/env python3
"""R25, Item 1 -- first-principles enumeration for Theorem 1c (own code; replication from the statements).

Usage:  python3 -B t1c_levelA.py part1                 (L0 brute force vs LA, labelled, tiny instances)
        python3 -B t1c_levelA.py part2 QMAX OUT.json   (LA on every composition of mB <= QMAX; structural
                                                        checks of the proof; cross-check with the DP LB;
                                                        signatures dumped to OUT.json)
        python3 -B t1c_levelA.py part2f "m,B;m,B" OUT.json   (the same for explicit families)

Controls (each must be able to fail and is reported with its number of violations):
  part1: 'mutant' enumerator that forgets one admissible partner  -> must differ from L0
  part2: the separator inequality with one term dropped (m-1 <= L+z, m-1 <= r+z, m-1 <= L+r) -> must fail
         a mutant DP (flush test without the 'one template bond' condition)                  -> must differ from LA
"""
import sys
import json
import time
import itertools
from collections import Counter

import nn_model as nn


def la_pairsets(m, B, sizes, od, drop_last_partner=False):
    strands = [nn.template(m, B)] + ["C" * sizes[s - 1] for s in od]
    circ = nn.Circle(strands)
    lab = [(0, i) for i in range(len(strands[0]))]
    for s in od:
        lab.extend((s, i) for i in range(sizes[s - 1]))
    out = set()

    def leaf(partner):
        if nn.is_connected(circ, partner):
            out.add(frozenset((lab[i], lab[p]) for i, p in enumerate(partner) if p > i))

    if drop_last_partner:
        # mutant: the last base of the circle is never used as a partner
        save = circ.letters
        circ.letters = circ.letters[:-1] + "A"
        nn.enumerate_noncrossing(circ, leaf)
        circ.letters = save
    else:
        nn.enumerate_noncrossing(circ, leaf)
    return out


def part1():
    t0 = time.time()
    tiny = [(1, 1, (1,)), (1, 2, (1, 1)), (1, 2, (2,)), (2, 1, (1, 1)), (3, 1, (1, 1, 1)), (4, 1, (1, 1, 1, 1)),
            (1, 3, (1, 2)), (1, 3, (1, 1, 1)), (1, 3, (3,)),
            (2, 2, (2, 2)), (2, 2, (1, 1, 2)), (2, 2, (3, 1)), (2, 2, (4,)), (2, 2, (1, 1, 1, 1)),
            (1, 4, (2, 2)), (1, 4, (1, 3)), (1, 4, (1, 1, 2)),
            (1, 5, (2, 3)), (1, 5, (1, 2, 2)), (5, 1, (1, 1, 1, 1, 1)),
            (2, 3, (2, 2, 2)), (2, 3, (3, 3)), (2, 3, (1, 2, 3)), (2, 3, (4, 2)), (2, 3, (1, 1, 4)),
            (3, 2, (2, 2, 2)), (3, 2, (3, 1, 1, 1)), (3, 2, (4, 2)), (3, 2, (1, 1, 2, 2))]
    tot_sets = tot_conn = tot_conn_unpk = 0
    viol_unique = 0      # connected pair set non-crossing for two or more labelled orders
    viol_enum = 0        # LA set of an order != L0 set of that order
    mutant_differs = 0   # control
    for (m, B, sizes) in tiny:
        res, all_sets = nn.level_0(m, B, sizes)
        tot_sets += all_sets
        tot_conn += len(res)
        byorder = {}
        for S, good in res.items():
            if len(good) >= 2:
                viol_unique += 1
            if good:
                tot_conn_unpk += 1
            for od in good:
                byorder.setdefault(od, set()).add(S)
        n = len(sizes)
        inst_mut = 0
        for od in itertools.permutations(range(1, n + 1)):
            a = la_pairsets(m, B, sizes, od)
            if a != byorder.get(od, set()):
                viol_enum += 1
            b = la_pairsets(m, B, sizes, od, drop_last_partner=True)
            if b != byorder.get(od, set()):
                inst_mut += 1
        mutant_differs += 1 if inst_mut else 0
        print(f"  m={m} B={B} a={sizes}: pair sets {all_sets}, connected {len(res)}, "
              f"connected+unpseudoknotted {sum(1 for g in res.values() if g)}, orders {len(byorder)}", flush=True)
    print(f"PART1 instances {len(tiny)}; pair sets {tot_sets}; connected {tot_conn}; "
          f"connected and unpseudoknotted {tot_conn_unpk}")
    print(f"PART1 violations: uniqueness of the ordering {viol_unique}; LA != L0 on some order {viol_enum}")
    print(f"PART1 control (mutant enumerator differs from L0): detected on {mutant_differs} of {len(tiny)} instances")
    print(f"PART1 time {time.time() - t0:.1f} s")


def structural_checks(m, B, order, cnt, tally):
    n = len(order)
    q = m * B
    M = q - n
    for (til, st, fl, nb, L, z, r), w in cnt.items():
        tally["structures"] += w
        if st + fl + L != m * (B - 1):
            tally["viol_bond_count"] += w
        if fl != n - 1 - z:
            tally["viol_nick_count"] += w
        key = "B1" if B == 1 else "B>=2"
        if m - 1 > L + r + z:
            tally["viol_sep_ineq_" + key] += w
        if B >= 2:
            tally["structures_B>=2"] += w
            if m - 1 > L + z:
                tally["ctrl_B>=2_sep_ineq_without_r"] += w
            if m - 1 > r + z:
                tally["ctrl_B>=2_sep_ineq_without_L"] += w
            if m - 1 > L + r:
                tally["ctrl_B>=2_sep_ineq_without_z"] += w
        if (til == 1) != (st == M):
            tally["viol_tiling_iff_all_item_bonds_stacked"] += w
        if til == 1:
            tally["tilings"] += w
            if (st, fl, nb, L, z, r) != (M, n - m, 0, 0, m - 1, 0):
                tally["viol_tiling_signature"] += w
        if B >= 2 and (til == 1) != (L == 0 and nb == 0):
            tally["viol_tiling_iff_L0_nobulge"] += w
        if B == 1 and til != 1:
            tally["B1_nontiling_structures"] += w


def mutant_level_B(m, B, order):
    """control: a DP whose flush test ignores the template side (any face with a nick and adjacent item ends)"""
    T = m * B + m - 1
    tl = nn.template(m, B)
    Gpos = [p for p in range(T) if tl[p] == "G"]
    item_of = []
    for idx, a in enumerate(order):
        item_of.extend([idx] * a)
    q = len(item_of)
    n = len(order)
    state = {}
    for t in Gpos:
        for c in range(q - 1, -1, -1):
            if item_of[c] != n - 1:
                break
            state[(t, c)] = Counter({(0, 0, 0): 1})
    result = Counter()
    for t in Gpos:
        for c in range(q - 1, -1, -1):
            cur = state.get((t, c))
            if not cur:
                continue
            if item_of[c] == 0:
                for k, w in cur.items():
                    result[k] += w
            for t2 in Gpos:
                if t2 <= t:
                    continue
                for c2 in range(c - 1, -1, -1):
                    nk = item_of[c] - item_of[c2]
                    if nk > 1:
                        break
                    tight = (t2 - t == 1 and c - c2 == 1)
                    if nk == 0:
                        delta = (1, 0, 0) if tight else (0, 0, 1)
                    else:
                        delta = (0, 1, 0) if (c - c2 == 1) else (0, 0, 0)   # MUTANT: template side ignored
                    tgt = state.setdefault((t2, c2), Counter())
                    for (st, fl, nb), w in cur.items():
                        tgt[(st + delta[0], fl + delta[1], nb + delta[2])] += w
            del state[(t, c)]
    return result


def part2(qmax, outname, fams=None):
    t0 = time.time()
    tally = Counter()
    for k in ("structures", "structures_B>=2", "tilings", "noncrossing_pair_sets", "viol_bond_count",
              "viol_nick_count", "viol_sep_ineq_B1", "viol_sep_ineq_B>=2", "ctrl_B>=2_sep_ineq_without_r",
              "ctrl_B>=2_sep_ineq_without_L", "ctrl_B>=2_sep_ineq_without_z",
              "viol_tiling_iff_all_item_bonds_stacked", "viol_tiling_signature", "viol_tiling_iff_L0_nobulge",
              "B1_nontiling_structures"):
        tally[k] = 0
    dump = {}
    if fams is None:
        fam = [(m, B) for m in range(1, qmax + 1) for B in range(1, qmax + 1) if m * B <= qmax]
    else:
        fam = fams
    viol_fact1 = 0
    viol_AB = 0
    mutant_detected = 0
    ncomp = 0
    for (m, B) in fam:
        fam_structs = 0
        for order in nn.compositions(m * B):
            ncomp += 1
            cntA, stats = nn.level_A(m, B, order, check=True)
            viol_fact1 += stats["fact1_violations"]
            tally["noncrossing_pair_sets"] += stats["noncrossing"]
            structural_checks(m, B, order, cntA, tally)
            cntB = nn.level_B(m, B, order)
            if cntA != cntB:
                viol_AB += 1
            projA = Counter()
            for (til, st, fl, nb, L, z, r), w in cntA.items():
                projA[(st, fl, nb)] += w
            if mutant_level_B(m, B, order) != projA:
                mutant_detected += 1
            fam_structs += sum(cntA.values())
            dump[f"{m},{B}|" + ",".join(map(str, order))] = [list(k) + [w] for k, w in sorted(cntA.items())]
        print(f"  family m={m} B={B}: compositions {2 ** (m * B - 1)}, connected structures {fam_structs}, "
              f"elapsed {time.time() - t0:.1f} s", flush=True)
    with open(outname, "w") as fh:
        json.dump(dump, fh)
    print(f"PART2 families (m,B): {fam}")
    print(f"PART2 number of families {len(fam)}; compositions (ordered instances) {ncomp}")
    for k in sorted(tally):
        print(f"PART2 {k}: {tally[k]}")
    print(f"PART2 violations: Fact 1 (connected iff no face with >= 2 nicks) {viol_fact1}; "
          f"DP LB != LA on a composition {viol_AB}")
    print(f"PART2 control (mutant DP differs from LA): detected on {mutant_detected} of {ncomp} compositions")
    print(f"PART2 wrote {outname}; time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    if sys.argv[1] == "part1":
        part1()
    elif sys.argv[1] == "part2":
        part2(int(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == "part2f":       # explicit families "m,B;m,B;..."
        fams = [tuple(int(v) for v in f.split(",")) for f in sys.argv[2].split(";")]
        part2(None, sys.argv[3], fams)
    else:
        raise SystemExit("unknown mode")
    print(f"peak memory {nn.peak_mb():.1f} MB")
