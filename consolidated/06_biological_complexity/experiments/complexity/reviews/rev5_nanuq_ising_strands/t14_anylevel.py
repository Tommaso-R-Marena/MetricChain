# t14_anylevel.py -- REVIEWER'S OWN CODE: Remark 3 of 7.2 (Step 1 of Theorem 12 for ANY outer-labeled planar
# network): a six-leaf restriction that is not 6-locally good meets six different positions of one blob;
# and Theorem 10'(a) / Remark 2 of 7.1 on explicit networks of any level: if no six-leaf restriction has the
# pattern, the metric is Kalmanson for the induced order with alpha > 0 on every displayed split.
import sys, random, collections, itertools, time
import networkx as nx
from mynet import Net, alphas, split_mask_of
from mygen import random_tree_children, edge_list, insert_arc, Counter
from myblob import blob_report
from mysplits import norm, restrict, six_locally_good_6, interval

three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
lg = {}; pt = {}
def lg6(R):
    if R not in lg: lg[R] = six_locally_good_6(R)
    return lg[R]
def pat6(R):
    if R not in pt: pt[R] = all(a in R for a in three) and any(t not in R for t in two)
    return pt[R]

seed = int(sys.argv[1]); N = int(sys.argv[2])
rng = random.Random(seed)
st = collections.Counter(); t0 = time.time()
while st['networks'] < N:
    n = rng.randint(6, 10)
    ch, root = random_tree_children(n, rng)
    cnt = Counter()
    for _ in range(rng.randint(2, 6)):
        E = edge_list(ch, root)
        ch, root = insert_arc(ch, root, rng.choice(E + [None]), rng.choice(E), cnt)
    net = Net(ch, root)
    if not net.is_valid(): continue
    order = net.circular_order()
    if order is None: continue
    try:
        reps = blob_report(net)
    except AssertionError as e:
        st['STRUCTURE VIOLATION'] += 1; continue
    lev = net.level()
    st['networks'] += 1; st['level %d' % lev] += 1
    L = net.leaves
    idx = {x: i for i, x in enumerate(order)}
    lpos = [idx[x] for x in L]                     # matrix index -> position in the order
    S = frozenset(norm(sum(1 << lpos[i] for i in range(n) if (m >> i) & 1), n) for m in net.displayed_splits())
    # for every blob: which pendant set (as set of order positions) each leaf belongs to
    blobmaps = []
    for r in reps:
        mp = {}
        for k, (v, m) in enumerate(r['pos'].items()):
            for i in range(n):
                if (m >> i) & 1: mp[lpos[i]] = k
        blobmaps.append(mp)
    haspat = False; allgood = True
    for Y in itertools.combinations(range(n), 6):
        R = restrict(S, Y, n)
        if pat6(R): haspat = True
        if not lg6(R):
            allgood = False
            st['six-leaf restrictions not 6-locally good'] += 1
            ok = any(len({mp.get(y, ('none', y)) for y in Y}) == 6 and all(y in mp for y in Y) for mp in blobmaps)
            if not ok:
                st['REMARK 3 VIOLATED (not six positions of one blob)'] += 1
    M6 = net.nanuq6()
    P = [L.index(x) for x in order]
    al = alphas(M6, P)
    ds = net.displayed_splits()
    kal = all(a >= 0 for a in al.values())
    pos_on = all(a > 0 for (i, j), a in al.items() if split_mask_of(P, i, j, n) in ds)
    exact = kal and all((a > 0) == (split_mask_of(P, i, j, n) in ds) for (i, j), a in al.items())
    if not haspat:
        st["networks in K'"] += 1
        if not (kal and pos_on): st["THEOREM 10'(a) VIOLATED on a network"] += 1
    else:
        st["networks outside K'"] += 1
        st["   of which Kalmanson for the induced order"] += kal
    if allgood:
        st['networks in K'] += 1
        if not exact: st['THEOREM 4 VIOLATED on a network'] += 1
print("seed", seed, "time %.0fs" % (time.time() - t0))
for k in sorted(st): print("  %-58s %d" % (k, st[k]))
