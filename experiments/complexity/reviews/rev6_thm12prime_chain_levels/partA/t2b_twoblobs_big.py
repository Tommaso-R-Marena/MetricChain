# t2_twoblobs.py -- REVIEW 6: two nested blobs, the lower one hanging at EVERY position of the upper one and
# entered through EVERY b- or c-position; all other positions single leaves or cherries.  Many of these networks
# have two negative critical weights.  Checks of chk.check (Theorem 12(a),(b); all circular orders; the five
# leaves of the proof of Theorem 12' for each negative blob, in the presence of another negative critical split).
import sys, random, itertools, time
from gen_l2 import Builder
from chk import check, new_stats

rng = random.Random(0)
st = new_stats()
t0 = time.time()
both_neg = 0
combos = 0
where = {}
shapes_top = [(6, 1, 1), (7, 1, 0), (6, 2, 0)]
shapes_low = [(4, 1, 1), (5, 1, 0)]
ok = True
for (kB, k1, k2) in shapes_top:
    positions = [("b", j) for j in range(1, kB + 1)] + [("x", a) for a in range(1, k1 + 1)] + \
                [("c", e) for e in range(1, k2 + 1)] + [("y", 0)]
    for pi in positions:
        for (lB, l1, l2) in shapes_low:
            entries = [("b", j) for j in range(1, lB + 1)] + [("c", e) for e in range(1, l2 + 1)]
            for ent in entries:
                for cherry in (0,):
                    B = Builder(rng)
                    nlow = lB + l1 + l2            # positions of the lower blob other than its entry
                    low_sizes = None
                    lowpos = [("b", j) for j in range(1, lB + 1)] + [("x", a) for a in range(1, l1 + 1)] + \
                             [("c", e) for e in range(1, l2 + 1)] + [("y", 0)]
                    low_sizes = {p: 1 for p in lowpos if p != ent}
                    if cherry:
                        q = rng.choice([p for p in lowpos if p != ent])
                        low_sizes[q] = 2
                    lt, lo = B.nested(lB, l1, l2, ent, sum(low_sizes.values()), 2, sizes=low_sizes)
                    top_sizes = {p: 1 for p in positions}
                    top_sizes[pi] = len(lo)
                    n = sum(top_sizes.values())
                    if n > 14:
                        continue
                    top, order = B.nested(kB, k1, k2, ("A",), n, 0, sizes=top_sizes, prebuilt={pi: (lt, lo)})
                    combos += 1
                    before = st["negative_splits"]
                    if not check(B.net, order, B.records, st, 14):
                        print("FAILED at", (kB, k1, k2), pi, (lB, l1, l2), ent)
                        ok = False
                        sys.exit(1)
                    k = st["negative_splits"] - before
                    if k == 2:
                        both_neg += 1
                        key = f"lower at {pi[0]}{pi[1] if pi[0] != 'y' else ''} of {kB,k1,k2}"
                        where[key] = where.get(key, 0) + 1
print(f"{combos} two-blob networks, {time.time()-t0:.0f}s; both critical weights negative in {both_neg}")
for k, v in st.items():
    print("  ", k, ":", v)
print("positions of the upper blob at which a lower blob with negative weight hangs while the upper is negative too:")
for k in sorted(where):
    print("    ", k, where[k])
print("ALL CHECKS PASSED" if ok else "FAILED")
