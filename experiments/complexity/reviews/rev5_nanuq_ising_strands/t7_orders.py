# t7_orders.py -- REVIEWER'S OWN CODE: Corollary 13 (bloblet formula, the failing bloblets, no circular
# order), and: do non-bloblet networks with a negative critical weight have a Kalmanson order at all?
import itertools, collections, sys, random, time
import numpy as np
from mynet import Net, alphas
from mybuild import bloblet_spec, build, rand_spec
from myblob import blob_report, check_theorem12, formula12b
from mysplits import kalmanson_some_order
from math import comb

maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 9
t0 = time.time()
neg = []; zero = []; nblob = 0; bad = 0
for n in range(4, maxn + 1):
    s = n - 1
    for kB in range(s + 1):
        for k1 in range(s - kB + 1):
            k2 = s - kB - k1
            net = build(bloblet_spec(kB, k1, k2))
            assert net.is_valid()
            nblob += 1
            info = check_theorem12(net)
            if info['viol']:
                bad += 1; print("VIOLATION", (kB, k1, k2), info['viol'])
            if k1 >= 1 and kB >= 2:
                pred = k1 + k2 - comb(kB - 1, 2) if k2 >= 1 else k1 + 1 - comb(kB - 2, 2)
                assert info['crit_values'] == [pred], ((kB, k1, k2), info['crit_values'], pred)
                if pred < 0: neg.append((kB, k1, k2, pred))
                if pred == 0: zero.append((kB, k1, k2))
            else:
                assert info['ncrit'] == 0
print("bloblets N[kB,k1,k2] with 4..%d leaves:" % maxn, nblob, " violations of Theorem 12 / Corollary 13:", bad)
print("negative critical weight:", neg)
print("zero critical weight:", zero)
cnt_none = 0
for kB, k1, k2, pred in neg:
    net = build(bloblet_spec(kB, k1, k2))
    M = net.nanuq6()
    o = kalmanson_some_order(M.tolist(), nontrivial_only=True)
    print("   N[%d,%d,%d] (%d leaves, weight %d): Kalmanson order:" % (kB, k1, k2, kB + k1 + k2 + 1, pred), o)
    cnt_none += o is None
print("failing bloblets Kalmanson for no circular order:", cnt_none, "of", len(neg), " time %.0fs" % (time.time() - t0))
# zero-weight bloblets: Kalmanson for the planar order, S* missing from the support
for kB, k1, k2 in zero:
    net = build(bloblet_spec(kB, k1, k2))
    info = check_theorem12(net)
    print("   zero weight N[%d,%d,%d]: all alpha >= 0 for the planar order:" % (kB, k1, k2), all(a >= 0 for a in info['alpha'].values()))

# non-bloblets with a negative critical weight and at most 10 leaves
rng = random.Random(77)
tested = 0; with_order = 0; ex = []
t0 = time.time()
while tested < 150 and time.time() - t0 < 600:
    n = rng.randint(7, 10)
    spec = rand_spec(rng, n, True)
    net = build(spec)
    if len(net.hyb) > 8 or not net.is_valid(): continue
    order = net.circular_order()
    if order is None: continue
    reps = blob_report(net)
    info = check_theorem12(net, order=order, reps=reps)
    assert not info['viol']
    if not any(v < 0 for v in info['crit_values']): continue
    if len(reps) < 2 and all(bin(m).count('1') == 1 for r in reps for m in r['pos'].values()):
        continue    # a bloblet
    tested += 1
    o = kalmanson_some_order(net.nanuq6().tolist(), nontrivial_only=True)
    if o is not None:
        with_order += 1
        if len(ex) < 5: ex.append((spec, [net.leaves[i] for i in o], info['crit_values']))
print("non-bloblet networks (7-10 leaves) with a negative critical weight:", tested, "; Kalmanson for some OTHER circular order:", with_order,
      " time %.0fs" % (time.time() - t0))
for e in ex: print("   EXAMPLE", e)
