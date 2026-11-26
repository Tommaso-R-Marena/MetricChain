# t4_struct.py seed N maxleaves -- REVIEWER'S OWN CODE.
# Random explicit rooted networks composed of trees, level-1 cycles, galled level-2 blobs and nested
# blobs (any source position; nested blobs inside pendant subnetworks; blobs entered through a cut edge
# at a b- or c-position).  Theorem 12 (a),(b) is checked with the blob structure read from the graph.
import sys, random, collections, time
from mynet import Net
from mybuild import rand_spec, build
from myblob import blob_report, check_theorem12

seed = int(sys.argv[1]); N = int(sys.argv[2]); maxleaves = int(sys.argv[3])
minleaves = int(sys.argv[4]) if len(sys.argv) > 4 else 5
rng = random.Random(seed)
st = collections.Counter(); hist = collections.Counter(); kinds = collections.Counter()
t0 = time.time()
examples = []
seen = set()
while st['checked'] < N:
    n = rng.randint(minleaves, maxleaves)
    spec = rand_spec(rng, n, True)
    net = build(spec)
    st['built'] += 1
    if len(net.hyb) > 9:
        st['skipped (more than 9 hybrid nodes)'] += 1; continue
    if not net.is_valid():
        st['invalid (not a network of Def. 2.1 / root not LSA)'] += 1; continue
    order = net.circular_order()
    if order is None:
        st['nonplanar'] += 1; continue
    lev = net.level()
    assert lev <= 2
    try:
        reps = blob_report(net)
    except AssertionError as e:
        st['STRUCTURE VIOLATION'] += 1
        examples.append(('structure', str(e), spec)); continue
    info = check_theorem12(net, order=order, reps=reps)
    st['checked'] += 1
    nb = len(reps)
    st['with several non-trivial blobs'] += nb >= 2
    nn = sum(1 for r in reps if r['kind'] == 'nested')
    st['with a nested blob'] += nn >= 1
    st['with >=2 nested blobs'] += nn >= 2
    st['with a nested blob entered through a cut edge'] += any(r['kind'] == 'nested' and r['source'] in r['pos'] for r in reps)
    st['with a nested blob having a non-leaf pendant subnetwork'] += any(
        r['kind'] == 'nested' and any(bin(m).count('1') > 1 for m in r['pos'].values()) for r in reps)
    st['critical splits'] += info['ncrit']
    st['critical splits with weight <= 0'] += sum(1 for v in info['crit_values'] if v <= 0)
    st['critical splits with weight < 0'] += sum(1 for v in info['crit_values'] if v < 0)
    st['other splits checked'] += len(info['alpha']) - info['ncrit']
    st['hybrid nodes max'] = max(st['hybrid nodes max'], len(net.hyb))
    for v in info['crit_values']:
        hist[v] += 1
    for kk in info['nested']:
        kinds[kk] += 1
    if info['viol']:
        st['THEOREM 12 VIOLATION'] += 1
        if len(examples) < 5:
            examples.append((info['viol'], spec, order))
print("seed", seed, "max leaves", maxleaves, "time %.0fs" % (time.time() - t0))
for k in sorted(st):
    print("  %-60s %d" % (k, st[k]))
print("  critical weights:", dict(sorted(hist.items())))
print("  distinct (kB,k1,k2) of nested blobs:", len(kinds))
for e in examples:
    print("  EXAMPLE", e)
