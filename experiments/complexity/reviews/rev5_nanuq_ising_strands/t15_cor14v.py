# t15_cor14v.py -- REVIEWER'S OWN CODE: Corollary 14, (v) => (i) under the reading "Kalmanson for SOME circular
# order".  For networks violating (i), replace one leaf at b_j and one at b_l (j,l in M) by clades of m leaves
# (the construction of the note's proof) and search ALL circular orders (networks with at most 10 leaves).
import random, itertools, collections, time
from mynet import Net
from mybuild import rand_spec, build
from myblob import blob_report, check_theorem12
from mysplits import kalmanson_some_order

def blow(net, leaf, m, tag):
    ch = {u: list(vs) for u, vs in net.ch.items() if vs}
    p = net.par[leaf][0]
    top = leaf
    for i in range(1, m):
        v = 'q%s%d' % (tag, i)
        ch[v] = [top, 'L%s%d' % (tag, i)]
        top = v
    k = ch[p].index(leaf)
    ch[p][k] = top
    return Net(ch, net.root)

rng = random.Random(99)
st = collections.Counter(); t0 = time.time()
while st['tested'] < 120 and time.time() - t0 < 900:
    n = rng.randint(6, 8)
    spec = rand_spec(rng, n, True, pnest=0.7, maxpos=7)
    net = build(spec)
    if len(net.hyb) > 6 or not net.is_valid(): continue
    if net.circular_order() is None: continue
    reps = blob_report(net)
    cand = []
    for r in reps:
        if r['kind'] == 'nested' and r.get('B') is not None:
            kB, k1, k2 = r['k']
            if k1 >= 1:
                M = r['B'][1:] if k2 >= 1 else r['B'][1:-1]
                if len(M) >= 2:
                    cand.append((r, M))
    if not cand: continue
    r, M = rng.choice(cand)
    vj, vl = rng.sample(M, 2)
    L = net.leaves
    lj = [L[i] for i in range(len(L)) if (r['pos'][vj] >> i) & 1][0]
    ll = [L[i] for i in range(len(L)) if (r['pos'][vl] >> i) & 1][0]
    for m in (2, 3):
        if n + 2 * (m - 1) > 10: break
        net2 = blow(blow(net, lj, m, 'a'), ll, m, 'b')
        assert net2.is_valid()
        info = check_theorem12(net2)
        assert not info['viol']
        if min(info['crit_values']) >= 0:
            st['blow-up still Kalmanson for the planar order (m=%d)' % m] += 1
            continue
        o = kalmanson_some_order(net2.nanuq6().tolist(), nontrivial_only=True)
        st['tested'] += 1
        st['bloblet' if (len(reps) == 1 and all(bin(x).count('1') == 1 for x in r['pos'].values())) else 'not a bloblet'] += 1
        if o is not None:
            st['KALMANSON FOR ANOTHER ORDER'] += 1
            print("found order", spec, lj, ll, m, [net2.leaves[i] for i in o])
        break
print(dict(st), "time %.0fs" % (time.time() - t0))
