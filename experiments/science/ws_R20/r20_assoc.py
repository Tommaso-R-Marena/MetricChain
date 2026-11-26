#!/usr/bin/env python3
"""r20_assoc.py -- workstream R20, item 2(f): what happens to the reduction if the problem is NOT posed for one
complex containing all strands, but (as in the base-pair model of Condon-Hajiaghayi-Thachuk, E = -p + (m-l)K_assoc)
strands may be left out of the complex, every strand that is bound costing an association energy A?

In the instances I(a,m,B) an item can only pair with the template, so a general unpseudoknotted structure is:
a set J of items forming ONE complex with the template (connected), and the other items free.  Its energy is
    [sum of loop energies of the complex] + |J| * A .
Hence   MFE_all(A) = min over J of ( MFE_conn(template + J) + |J| * A ),
where MFE_conn is the minimum over connected unpseudoknotted structures, computed here by exhaustive enumeration
with r20_enum.py for EVERY sub-multiset J of the items.

Reviewer's claim (extension of Theorem 1; [P], tested here):
    put Delta = min_i ( |sigma| (a_i - 1) - A ).  If Delta > 0 then
        solvable     =>  MFE_all(A) = sigma*M + n*A,
        not solvable =>  MFE_all(A) >= sigma*M + n*A + min(|sigma|, Delta).
Control that must fail: values of A with Delta <= 0 (an item that gains less by binding than it pays): the decision
"MFE_all(A) <= sigma*M + n*A  <=>  solvable" must be wrong for at least one instance.

Usage: python3 -I -B r20_assoc.py
"""
import sys
import os
import time
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r20_enum as E      # noqa: E402
import r20_theorem as T   # noqa: E402

INSTANCES = [
    ((2, 2), 2, 2), ((3, 1), 2, 2), ((1, 1, 2), 2, 2),
    ((3, 3), 2, 3), ((2, 2, 2), 2, 3), ((3, 2, 1), 2, 3), ((4, 2), 2, 3), ((2, 2, 1, 1), 2, 3),
    ((4, 4), 2, 4), ((3, 3, 2), 2, 4), ((4, 2, 2), 2, 4), ((2, 2, 2, 2), 2, 4), ((5, 3), 2, 4), ((3, 2, 2, 1), 2, 4),
    ((2, 2, 2), 3, 2), ((3, 3), 3, 2), ((3, 3, 3), 3, 3), ((3, 2, 2, 2), 3, 3), ((4, 3, 2), 3, 3),
    ((4, 4, 2), 2, 5), ((4, 3, 3), 2, 5), ((3, 3, 2, 2), 2, 5),
]
A_VALUES = [-2, 0, 1, 2, 3, 4, 7]
MODELS = ["H1_stack_only", "H2_penalties", "H3_hash_0to9"]


def mfe_conn(template, sizes, fl):
    """min over connected unpseudoknotted structures of [template] + [C^s for s in sizes], for each model in fl.
    sizes may be empty (template alone: energy 0)."""
    if not sizes:
        return [0] * len(fl), 1
    strands = [template] + ["C" * s for s in sizes]
    c = len(strands)
    best = [None] * len(fl)
    cache = [dict() for _ in fl]
    cnt = [0]
    # equal items are interchangeable: one order per class is enough for a minimum
    orders = list(T.canonical_orders(sizes))
    for order in orders:
        circ = E.Circle(strands, order)

        def visit(partner, circ=circ):
            cnt[0] += 1
            ds = [T.descriptor(circ, f) for f in E.faces(circ, partner)]
            for i, f_ in enumerate(fl):
                ch = cache[i]
                e = 0
                for d in ds:
                    v = ch.get(d)
                    if v is None:
                        v = f_(d)
                        ch[d] = v
                    e += v
                if best[i] is None or e < best[i]:
                    best[i] = e

        E.enum_noncrossing(circ, E.WATSON_CRICK, visit, prune_two_nicks=True)
    return best, cnt[0]


def main():
    t0 = time.time()
    models = T.make_models()
    fl = [models[nm]["f"] for nm in MODELS]
    sig = [models[nm]["sigma"] for nm in MODELS]
    print("r20_assoc.py: 'several complexes allowed' version of the problem; models", MODELS, "sigma", sig)
    print("A = association energy per bound strand;  Delta = min_i(|sigma|(a_i-1) - A)")
    viol_claim = 0
    n_claim = 0
    wrong_ctrl = 0
    n_ctrl = 0
    n_struct = 0
    for (a, m, B) in INSTANCES:
        n = len(a)
        M = m * B - n
        template = "A".join(["G" * B] * m)
        solv = T.solvable_bruteforce(a, m, B)
        memo = {}
        table = {}   # sorted sizes tuple -> best per model
        for r in range(n + 1):
            for J in combinations(range(n), r):
                key = tuple(sorted(a[i] for i in J))
                if key not in memo:
                    memo[key], k = mfe_conn(template, key, fl)
                    n_struct += k
                table[J] = memo[key]
        line = "a=%s m=%d B=%d M=%d solvable=%s:" % (list(a), m, B, M, solv)
        for mi, nm in enumerate(MODELS):
            s = sig[mi]
            for A in A_VALUES:
                mfe_all = min(table[J][mi] + len(J) * A for J in table)
                thr = s * M + n * A
                delta = min(abs(s) * (x - 1) - A for x in a)
                if delta > 0:
                    n_claim += 1
                    ok = (mfe_all == thr) if solv else (mfe_all >= thr + min(abs(s), delta))
                    if not ok:
                        viol_claim += 1
                        line += " [VIOLATION %s A=%d: MFE_all=%d thr=%d]" % (nm, A, mfe_all, thr)
                else:
                    n_ctrl += 1
                    if (mfe_all <= thr) != solv:
                        wrong_ctrl += 1
        # short per-instance summary for the stack-only model
        s = sig[0]
        line += "  stack-only: " + " ".join("A=%d:%d(thr %d)" % (A, min(table[J][0] + len(J) * A for J in table), s * M + n * A)
                                             for A in A_VALUES)
        print(line)
        sys.stdout.flush()
    print()
    print("SUMMARY: %d instances, %d connected structures enumerated over all sub-multisets, %.1f s" % (
        len(INSTANCES), n_struct, time.time() - t0))
    print("  claim (Delta > 0): %d (instance, model, A) cases, violations: %d" % (n_claim, viol_claim))
    print("  control (Delta <= 0): %d cases, wrong decisions of 'MFE_all <= sigma*M + n*A <=> solvable': %d   (must be > 0)" % (
        n_ctrl, wrong_ctrl))
    print("RESULT:", "PASS" if viol_claim == 0 and wrong_ctrl > 0 else "FAIL")
    print("END r20_assoc.py")


if __name__ == "__main__":
    main()
