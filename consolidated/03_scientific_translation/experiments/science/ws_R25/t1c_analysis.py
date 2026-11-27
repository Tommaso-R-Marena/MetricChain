#!/usr/bin/env python3
"""R25, Item 1 -- analysis of the enumerated signatures against Theorem 1c (own code).

Usage: python3 -B t1c_analysis.py SIG1.json [SIG2.json ...]

Normalisation sigma = -1.  X = |x| >= 0, g = gamma >= 0.  In the extremal model of (C0),(H1),(C2) (every bulge
and interior loop costs exactly gamma; any other admissible g only raises the energy of structures that have
such loops, and tiling structures have none) a connected structure with st stacks, fl flush faces and nb
bulge/interior loops has
      E - E_0 = (M - st) - X*(fl - (n - m)) + g*nb  =:  A - X*Fd + g*nb ,      E_0 = sigma*M + x*(n-m).
Theorem 1c (regime X >= 1): if B >= 2 and X < 1 + min(1, g) then E - E_0 = 0 for tiling structures and
      E - E_0 >= eps = min(1, g) - (X - 1) for all others.

Checks (each printed with its number of violations) and controls (each must be able to fail):
  C1  tiling structures have (A, Fd, nb) = (0, 0, 0)                                   [parameter-free]
  C2  Theorem 1c as stated, regime X >= 1, on a rational grid, all instances with B >= 2
  C3  the same statement for B = 1                      (control: excluded by the theorem; must fail)
  C4  the conclusion outside the hypothesis at B = 2    (control: must fail at every grid point outside)
  C5  the three control models named in the note (x,gamma) = (sigma,0), |x| = |sigma|+gamma < 2|sigma|,
      |x| = 2|sigma| < |sigma|+gamma                    (control: must fail)
  C6  exact validity region per family: non-tiling > E_0 on {X < min(B, 1+g)}  (vertex test, integers)
  C7  conjectured exact gap min(1, 1+g-X, B-X) on a grid, per B
  C8  smallest counterexamples beyond the stated range
"""
import sys
import json
import time
import itertools
from fractions import Fraction as F
from math import factorial
from collections import defaultdict

import nn_model as nn


def load(files):
    data = {}
    for fn in files:
        with open(fn) as fh:
            d = json.load(fh)
        for key, rows in d.items():
            mb, od = key.split("|")
            m, B = (int(v) for v in mb.split(","))
            order = tuple(int(v) for v in od.split(","))
            sig = defaultdict(int)
            for row in rows:
                til, st, fl, nb = row[0], row[1], row[2], row[3]
                sig[(til, st, fl, nb)] += row[-1]
            k = (m, B, order)
            if k in data:
                if data[k] != dict(sig):
                    raise SystemExit(f"two files disagree on {k}")
            data[k] = dict(sig)
    return data


def pareto(triples):
    """minimal elements for the order: smaller A, larger Fd, smaller nb is worse for the theorem"""
    ts = sorted(set(triples))
    out = []
    for t in ts:
        dominated = False
        for u in ts:
            if u != t and u[0] <= t[0] and u[1] >= t[1] and u[2] <= t[2]:
                dominated = True
                break
        if not dominated:
            out.append(t)
    return out


def solvable(a, m, B):
    """exact bin packing by brute force: can the multiset a be split into m groups of sum B?"""
    a = sorted(a, reverse=True)
    if sum(a) != m * B or (a and a[0] > B):
        return False
    bins = [0] * m

    def rec(i):
        if i == len(a):
            return True
        tried = set()
        for b in range(m):
            if bins[b] + a[i] <= B and bins[b] not in tried:
                tried.add(bins[b])
                bins[b] += a[i]
                if rec(i + 1):
                    bins[b] -= a[i]
                    return True
                bins[b] -= a[i]
        return False

    return rec(0)


def ell(t, X, g):
    return t[0] - X * t[1] + g * t[2]


def find_structure(m, B, order, target):
    """explicit structure with (st, fl, nb) = target for the circular order, by the generic enumerator LA"""
    circ = nn.Circle([nn.template(m, B)] + ["C" * a for a in order])
    found = []

    def leaf(partner):
        if found:
            return
        if nn.is_connected(circ, partner):
            s = nn.signature(circ, partner, m, B)
            if (s[1], s[2], s[3]) == target and s[0] == 0:
                found.append(list(partner))

    nn.enumerate_noncrossing(circ, leaf)
    if not found:
        return None
    partner = found[0]
    T = len(circ.strands[0])
    pairs = [(i, partner[i]) for i in range(T) if partner[i] != -1]
    # human-readable: template positions 1..T; item k (in circular order), base j (5'->3')
    starts = []
    p = T
    for a in order:
        starts.append(p)
        p += a
    desc = []
    for (i, j) in pairs:
        k = max(u for u in range(len(order)) if starts[u] <= j)
        desc.append(f"G{i + 1}-item{k + 1}.{j - starts[k] + 1}")
    return " ".join(desc)


def main():
    t0 = time.time()
    data = load(sys.argv[1:])
    print(f"loaded {len(data)} ordered instances (m, B, order of item sizes) from {len(sys.argv) - 1} file(s)")
    # per ordered instance: normalised triples
    fam_front = defaultdict(set)          # (m,B) -> set of non-tiling triples (pareto per ordered instance, united)
    inst_front = defaultdict(set)         # (m,B,multiset) -> pareto set of non-tiling triples
    n_struct = 0
    n_struct_B2 = 0
    n_struct_lab = 0
    n_til = 0
    viol_c1 = 0
    fam_stats = defaultdict(lambda: [0, 0, 0])
    for (m, B, order), sig in data.items():
        n = len(order)
        M = m * B - n
        trip = set()
        mult = 1                               # labelled orders per order of sizes: prod over sizes of mu_s!
        for s_ in set(order):
            mult *= factorial(order.count(s_))
        for (til, st, fl, nb), w in sig.items():
            n_struct += w
            n_struct_lab += w * mult
            if B >= 2:
                n_struct_B2 += w
            fam_stats[(m, B)][1] += w
            t = (M - st, fl - (n - m), nb)
            if til:
                n_til += w
                fam_stats[(m, B)][2] += w
                if t != (0, 0, 0):
                    viol_c1 += w
            else:
                trip.add(t)
        fam_stats[(m, B)][0] += 1
        pf = pareto(trip)
        fam_front[(m, B)].update(pf)
        inst_front[(m, B, tuple(sorted(order)))].update(pf)
    for k in list(fam_front):
        fam_front[k] = set(pareto(fam_front[k]))
    for k in list(inst_front):
        inst_front[k] = set(pareto(inst_front[k]))
    fams = sorted(fam_front, key=lambda mb: (mb[0] * mb[1], mb[0]))
    print(f"families (m,B): {len(fams)}; instances (multisets a): {len(inst_front)}; "
          f"connected structures (equal items not distinguished): {n_struct}, of which B >= 2: {n_struct_B2}; "
          f"with all strands labelled: {n_struct_lab}; tiling structures: {n_til}")
    ninst_fam = defaultdict(int)
    for (m_, B_, a_) in inst_front:
        ninst_fam[(m_, B_)] += 1
    print("instances (multisets) per family: " + ", ".join(f"({m_},{B_}):{ninst_fam[(m_, B_)]}" for (m_, B_) in fams))
    print("family: ordered instances, structures, tilings, Pareto front of non-tiling (A, Fd, nb)")
    for mb in fams:
        st = fam_stats[mb]
        print(f"  m={mb[0]} B={mb[1]}: {st[0]}, {st[1]}, {st[2]}, {sorted(fam_front[mb])}")
    print(f"C1 tiling structures with (A,Fd,nb) != (0,0,0): {viol_c1} violations of {n_til}")

    # grids
    quarter = [F(k, 4) for k in range(0, 25)]            # 0 .. 6
    fine = [F(k, 20) for k in range(0, 61)]              # 0 .. 3 step 1/20
    def eps_stated(X, g):
        return min(F(1), g) - (X - 1)

    # C2: Theorem 1c as stated, regime X >= 1, B >= 2, X < 1 + min(1,g)
    gs = fine + [F(5), F(50)]
    pts = [(X, g) for X in fine for g in gs if X >= 1 and X < 1 + min(F(1), g)]
    tiny_ = F(1, 10 ** 6)
    edge = [(1 + min(F(1), g) - tiny_, g) for g in (F(1, 20), F(1, 4), F(1, 2), F(1), F(2), F(50))]   # just below the bound
    edge += [(F(1), g) for g in (F(1, 10 ** 6), F(1, 20), F(1), F(50))]                                # |x| = |sigma|
    for label, plist in (("grid X,g in (1/20)Z, g also 5 and 50", pts),
                         ("boundary points X = 1+min(1,g)-1e-6 and X = 1", edge)):
        checked = viol = 0
        slack_min = None
        attained_fams = set()
        for mb in fams:
            if mb[1] < 2:
                continue
            front = fam_front[mb]
            for (X, g) in plist:
                e = eps_stated(X, g)
                for t in front:
                    checked += 1
                    v = ell(t, X, g)
                    if v < e:
                        viol += 1
                    s = v - e
                    if slack_min is None or s < slack_min:
                        slack_min = s
                    if s == 0:
                        attained_fams.add(mb)
        print(f"C2 Theorem 1c as stated (X>=1, B>=2, X<1+min(1,g)); {label}: {len(plist)} parameter points, "
              f"{checked} (front triple, point) pairs, violations {viol}, least value of gap - eps_x: {slack_min}; "
              f"eps_x attained in families {sorted(attained_fams)}")
    # C2c: control for C2 -- the same test with a gap claimed too large by 1/20 must fail
    viol_ctrl = 0
    for mb in fams:
        if mb[1] < 2:
            continue
        for (X, g) in pts:
            e = eps_stated(X, g) + F(1, 20)
            if any(ell(t, X, g) < e for t in fam_front[mb]):
                viol_ctrl += 1
    print(f"C2c control (claimed gap eps_x + 1/20): fails at {viol_ctrl} (family, grid point) pairs")
    # C2d: the regime X < 1 (case 1 of the theorem; all B >= 1), gap 1 - X, for completeness
    checked = viol = 0
    for mb in fams:
        for X in fine:
            if X >= 1:
                continue
            for g in gs:
                for t in fam_front[mb]:
                    checked += 1
                    if ell(t, X, g) < 1 - X:
                        viol += 1
    print(f"C2d regime X < 1 (not the object of this review), all B >= 1, gap 1 - X: {checked} pairs, violations {viol}")

    # C3: control B = 1 in the excluded regime
    for mb in fams:
        if mb[1] != 1:
            continue
        front = fam_front[mb]
        pts = bad = bad0 = 0
        for X in fine:
            if X < 1:
                continue
            for g in fine:
                if not (X < 1 + min(F(1), g)):
                    continue
                pts += 1
                vals = [ell(t, X, g) for t in front]
                if vals and min(vals) < eps_stated(X, g):
                    bad += 1
                if vals and min(vals) <= 0:
                    bad0 += 1
        print(f"C3 control B=1, m={mb[0]}: grid points in the regime {pts}; conclusion 'gap >= eps_x' fails at {bad}; "
              f"'non-tiling above E_0' fails at {bad0}; front {sorted(front)}")

    # C4: control at B = 2 outside the hypothesis (X >= 1 + min(1,g)), quarter grid
    for mb in fams:
        if mb[1] != 2 or mb[0] < 2:
            continue
        front = fam_front[mb]
        pts = fail = 0
        for X in quarter:
            for g in quarter:
                if X < 1 + min(F(1), g):
                    continue
                pts += 1
                if min(ell(t, X, g) for t in front) <= 0:
                    fail += 1
        print(f"C4 control B=2, m={mb[0]}: grid points with X >= 1+min(1,g): {pts}; "
              f"a non-tiling structure at or below E_0 exists at {fail} of them")

    # C5: the three control models of the note
    ctrl = [("(x,gamma)=(sigma,0)", F(1), F(0)), ("|x|=|sigma|+gamma<2|sigma|", F(3, 2), F(1, 2)),
            ("|x|=2|sigma|<|sigma|+gamma", F(2), F(2))]
    for name, X, g in ctrl:
        bad_inst = [k for k, fr in inst_front.items() if k[1] >= 2 and fr and min(ell(t, X, g) for t in fr) <= 0]
        print(f"C5 control model {name}: instances with B >= 2 having a non-tiling structure at or below E_0: "
              f"{len(bad_inst)} of {sum(1 for k in inst_front if k[1] >= 2)}")

    # C6: exact validity region per family (vertex test), predicted region X < min(B, 1+g)
    print("C6 exact region: for each family, (i) every non-tiling triple is > 0 on {0<=X<min(B,1+g), g>=0} "
          "[A>0, A-Fd>=0, A-B*Fd+(B-1)*nb>=0];  (ii) triples (1,1,1) [straddle] and (B,1,0) [unpaired block] present")
    c6_viol = 0
    for mb in fams:
        m, B = mb
        front = fam_front[mb]
        bad = [t for t in front if not (t[0] > 0 and t[0] - t[1] >= 0 and t[0] - B * t[1] + (B - 1) * t[2] >= 0
                                        and t[2] >= 0)]
        c6_viol += len(bad)
        has_str = (1, 1, 1) in front
        has_blk = any(t[2] == 0 and t[1] > 0 and t[0] == B * t[1] for t in front)
        has_one = (1, 0, 0) in front
        print(f"  m={m} B={B}: (i) violations {len(bad)} {bad if bad else ''}; (ii) straddle {has_str}, "
              f"unpaired block {has_blk}; triple (1,0,0) present {has_one}")
    print(f"C6 total violations of (i): {c6_viol}")

    # C6b: the stated region {X < 1+min(1,g)} versus the exact one for B >= 3: grid points with
    #      1+min(1,g) <= X < min(B,1+g) where the conclusion nevertheless holds
    for mb in fams:
        m, B = mb
        if B < 3 or m < 2:
            continue
        front = fam_front[mb]
        pts = holds = 0
        for X in quarter:
            for g in quarter:
                if X >= 1 + min(F(1), g) and X < min(F(B), 1 + g):
                    pts += 1
                    if min(ell(t, X, g) for t in front) > 0:
                        holds += 1
        print(f"C6b m={m} B={B}: grid points outside the stated hypothesis but with X < min(B,1+g): {pts}; "
              f"conclusion still holds at {holds}")

    # C7: conjectured exact gap min(1, 1+g-X, B-X) for X < min(B,1+g)
    c7_viol = 0
    for mb in fams:
        m, B = mb
        front = fam_front[mb]
        if not front:
            print(f"C7 m={m} B={B}: no non-tiling structure at all")
            continue
        pts = below = equal = 0
        for X in quarter:
            for g in quarter:
                if not (X < min(F(B), 1 + g)):
                    continue
                pts += 1
                pred = min(F(1), 1 + g - X, B - X)
                val = min(ell(t, X, g) for t in front)
                if val < pred:
                    below += 1
                if val == pred:
                    equal += 1
        c7_viol += below
        print(f"C7 m={m} B={B}: grid points {pts}; least gap below min(1,1+g-X,B-X): {below}; equal: {equal}")
    print(f"C7 total grid points with a gap below the conjectured formula: {c7_viol}")

    # C8: smallest counterexamples beyond the stated range
    def size_key(k):
        m, B, a = k
        return (2 * m * B + m - 1, len(a) + 1, m, B, a)
    cases = [("B=1, x=sigma (X=1), gamma=1", lambda k: k[1] == 1, F(1), F(1)),
             ("B=1, X=3/2, gamma=1", lambda k: k[1] == 1, F(3, 2), F(1)),
             ("B>=2, (X,gamma)=(1,0)", lambda k: k[1] >= 2, F(1), F(0)),
             ("B>=2, X=1+gamma=3/2 (gamma=1/2)", lambda k: k[1] >= 2, F(3, 2), F(1, 2)),
             ("B>=2, X=2, gamma=2", lambda k: k[1] >= 2, F(2), F(2)),
             ("B>=3, X=2, gamma=2 (outside the stated range, inside X<min(B,1+g))", lambda k: k[1] >= 3, F(2), F(2)),
             ("B>=3, X=3, gamma=3", lambda k: k[1] >= 3, F(3), F(3))]
    for name, pred, X, g in cases:
        for want in (False, True):
            best = None
            for k in sorted(inst_front, key=size_key):
                if not pred(k):
                    continue
                fr = inst_front[k]
                if not fr:
                    continue
                if solvable(k[2], k[0], k[1]) != want:
                    continue
                tmin = min(fr, key=lambda t: ell(t, X, g))
                if ell(tmin, X, g) <= 0:
                    best = (k, tmin)
                    break
            lab = "yes-instance" if want else "no-instance "
            if best is None:
                print(f"C8 {name}; {lab}: none found")
                continue
            (m, B, a), t = best
            # find an order and an explicit structure
            expl = None
            for order in sorted(set(itertools.permutations(a))):
                sig = data.get((m, B, order))
                if sig is None:
                    continue
                n = len(a)
                M = m * B - n
                tgt = (M - t[0], t[1] + (n - m), t[2])
                if any((til == 0 and (st, fl, nb) == tgt) for (til, st, fl, nb) in sig):
                    if 2 * m * B <= 20:
                        expl = (order, find_structure(m, B, order, tgt))
                    else:
                        expl = (order, "(not searched)")
                    break
            print(f"C8 {name}; {lab}: smallest a={a}, m={m}, B={B} (N={2*m*B+m-1}, c={len(a)+1}); "
                  f"(A,Fd,nb)={t}, E-E_0={ell(t, X, g)}; circular order of item sizes {expl[0]}; pairs: {expl[1]}")
    # C9: full signature tables of the smallest instances (hand-checkable)
    for (m, B, a) in [(2, 1, (2,)), (2, 2, (4,)), (2, 2, (3, 1)), (2, 2, (2, 2)), (2, 2, (1, 1, 2))]:
        n = len(a)
        M = m * B - n
        for order in sorted(set(itertools.permutations(a))):
            sig = data.get((m, B, order))
            if sig is None:
                continue
            rows = []
            for (til, st, fl, nb), w in sorted(sig.items()):
                rows.append(f"[{'T' if til else '-'} st={st} fl={fl} nb={nb} x{w} -> (A,Fd,nb)=({M - st},{fl - (n - m)},{nb})]")
            print(f"C9 a={a} m={m} B={B} order {order} (M={M}, n-m={n - m}): " + " ".join(rows))
    print(f"analysis time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
