#!/usr/bin/env python3
"""R25, Item 1 -- direct test of Theorem 1c, structure by structure, with explicit loop-energy functions
(own code; independent of the signature algebra of t1c_analysis.py).

Usage: python3 -B t1c_direct.py QMAX

For every composition of mB (mB <= QMAX) and every connected unpseudoknotted structure of I(a,m,B) (generic
enumerator: backtracking over non-crossing pair sets, union-find, faces as orbits of links) the energy
sum_f g(f) is computed face by face with exact rationals, for each model (sigma, x, gamma, table):
    stack -> sigma ;  flush face -> x ;  every other exterior loop -> 0 ;
    bulge / interior loop with uT unpaired template bases and uC unpaired item bases -> gamma + table(uT, uC).
table = 0 ("extremal": every such loop costs exactly gamma) or a fixed pseudo-random table of non-negative
rationals (seed 25), so that g satisfies (C0), (H1), (C2) in both cases.

Claim tested for the models in the regime |sigma| <= |x| < |sigma| + min(|sigma|, gamma), instances with B >= 2:
    tiling structure (definition of section 2)  =>  E  = E_0 := sigma*M + x*(n-m)
    any other connected structure               =>  E >= E_0 + eps_x,   eps_x = min(|sigma|,gamma) - (|x|-|sigma|)
Controls (must fail): the same claim on the instances with B = 1; models outside the hypothesis (a non-tiling
structure at or below E_0 must exist for the extremal table).
"""
import sys
import time
import random
from fractions import Fraction as F
from collections import Counter

import nn_model as nn

IN_REGIME = [
    ("x=sigma, gamma=1/2", F(-1), F(-1), F(1, 2)),
    ("x=sigma, gamma=3", F(-1), F(-1), F(3)),
    ("x=sigma, gamma=1/1000", F(-1), F(-1), F(1, 1000)),
    ("|x|=5/4, gamma=1/2", F(-1), F(-5, 4), F(1, 2)),
    ("|x|=149/100, gamma=1/2 (just below |sigma|+gamma)", F(-1), F(-149, 100), F(1, 2)),
    ("|x|=7/4, gamma=2", F(-1), F(-7, 4), F(2)),
    ("|x|=199/100, gamma=5 (just below 2|sigma|)", F(-1), F(-199, 100), F(5)),
    ("sigma=-3, x=-4, gamma=2", F(-3), F(-4), F(2)),
]
OUTSIDE = [
    ("(x,gamma)=(sigma,0)", F(-1), F(-1), F(0)),
    ("|x|=|sigma|+gamma=3/2", F(-1), F(-3, 2), F(1, 2)),
    ("|x|=2|sigma|, gamma=2", F(-1), F(-2), F(2)),
    ("|x|=9/4, gamma=3", F(-1), F(-9, 4), F(3)),
]


def profile(circ, partner, m, B):
    """(tiling by definition, #stacks, #flush, sorted tuple of (uT, uC) of the bulge/interior loops)"""
    st = fl = 0
    loops = []
    nfaces = 0
    for f in nn.faces(circ, partner):
        nfaces += 1
        typ, d = nn.classify_face(circ, partner, f)
        if typ == "stack":
            st += 1
        elif typ == "flush":
            fl += 1
        elif typ in ("bulge", "interior"):
            uT = uC = 0
            for i in f[0]:
                h = (i + 1) % circ.N
                if partner[h] == -1:
                    if circ.sid[h] == 0:
                        uT += 1
                    else:
                        uC += 1
            loops.append((uT, uC))
        elif typ != "ext":
            raise nn.StructureError("unexpected face type " + typ)
    til = 1 if nn.tiling_by_definition(circ, partner, m, B) else 0
    return (til, st, fl, tuple(sorted(loops)))


def main():
    t0 = time.time()
    qmax = int(sys.argv[1])
    rng = random.Random(25)
    table = {}

    def rnd(uT, uC):
        if (uT, uC) not in table:
            table[(uT, uC)] = F(rng.randint(0, 8), 4)        # 0, 1/4, ..., 2
        return table[(uT, uC)]

    fams = [(m, B) for m in range(1, qmax + 1) for B in range(1, qmax + 1) if m * B <= qmax]
    profs = []    # (m, B, order, Counter of profiles)
    nstruct = Counter()
    for (m, B) in fams:
        for order in nn.compositions(m * B):
            circ = nn.Circle([nn.template(m, B)] + ["C" * a for a in order])
            cnt = Counter()

            def leaf(partner, circ=circ, cnt=cnt, m=m, B=B):
                if nn.is_connected(circ, partner):
                    cnt[profile(circ, partner, m, B)] += 1

            nn.enumerate_noncrossing(circ, leaf)
            profs.append((m, B, order, cnt))
            nstruct["B1" if B == 1 else "B>=2"] += sum(cnt.values())
    print(f"enumerated {len(profs)} ordered instances in {len(fams)} families with mB <= {qmax}: "
          f"{nstruct['B>=2']} connected structures with B >= 2, {nstruct['B1']} with B = 1; "
          f"enumeration time {time.time() - t0:.1f} s", flush=True)
    # make the random table deterministic: fill it in sorted order of the keys that occur
    keys = sorted({lp for (_, _, _, cnt) in profs for (til, st, fl, loops) in cnt for lp in loops})
    for k in keys:
        rnd(*k)
    print(f"loop shapes (uT, uC) that occur: {len(keys)}; random table: "
          + ", ".join(f"{k}:{table[k]}" for k in keys[:12]) + (" ..." if len(keys) > 12 else ""))

    def energy(sig, x, gam, tab, st, fl, loops):
        e = sig * st + x * fl
        for lp in loops:
            e += gam + (table[lp] if tab == "random" else 0)
        return e

    for name, sig, x, gam in IN_REGIME:
        eps = min(-sig, gam) - (-x + sig)
        assert eps > 0 and -x >= -sig
        for tab in ("extremal", "random"):
            res = Counter()
            slack = None
            for (m, B, order, cnt) in profs:
                n = len(order)
                E0 = sig * (m * B - n) + x * (n - m)
                key = "B1" if B == 1 else "B2"
                for (til, st, fl, loops), w in cnt.items():
                    e = energy(sig, x, gam, tab, st, fl, loops)
                    res[key + "_checked"] += w
                    if til:
                        if e != E0:
                            res[key + "_viol_tiling"] += w
                    else:
                        if e < E0 + eps:
                            res[key + "_viol_gap"] += w
                        if key == "B2":
                            s = e - E0 - eps
                            if slack is None or s < slack:
                                slack = s
            print(f"IN  {name} [{tab} table] eps_x={eps}: B>=2: structures {res['B2_checked']}, violations: tiling energy "
                  f"{res['B2_viol_tiling']}, gap {res['B2_viol_gap']}, least (E-E_0-eps_x) over non-tiling {slack} | "
                  f"control B=1: structures {res['B1_checked']}, violations: tiling energy {res['B1_viol_tiling']}, "
                  f"gap {res['B1_viol_gap']}")
    for name, sig, x, gam in OUTSIDE:
        for tab in ("extremal", "random"):
            res = Counter()
            for (m, B, order, cnt) in profs:
                if B < 2:
                    continue
                n = len(order)
                E0 = sig * (m * B - n) + x * (n - m)
                for (til, st, fl, loops), w in cnt.items():
                    e = energy(sig, x, gam, tab, st, fl, loops)
                    if til:
                        if e != E0:
                            res["viol_tiling"] += w
                    elif e <= E0:
                        res["nontiling_at_or_below_E0"] += w
            print(f"OUT {name} [{tab} table], B>=2: non-tiling structures at or below E_0: {res['nontiling_at_or_below_E0']}; "
                  f"tiling structures off E_0: {res['viol_tiling']}")
    print(f"time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
