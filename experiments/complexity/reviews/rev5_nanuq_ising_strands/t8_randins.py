# t8_randins.py seed N -- REVIEWER'S OWN CODE.  Unstructured random networks: random tree, 2..6 hybrid-arc
# insertions (with a bias towards nearby edges so that blobs stay small), kept if valid, outer-labeled planar
# and of level <= 2.  Theorem 12 is checked for SEVERAL induced circular orders (different planar embeddings).
import sys, random, collections, time
import networkx as nx
from mynet import Net
from mygen import random_tree_children, edge_list, insert_arc, Counter
from myblob import blob_report, check_theorem12

def circular_orders(net, rng, tries=6):
    """distinct induced circular orders from planar embeddings of shuffled copies of the graph"""
    out = {}
    edges = [(u, v) for u in net.nodes for v in net.ch[u]]
    apex = ('*apex*',)
    for _ in range(tries):
        S = nx.Graph()
        nodes = list(net.nodes); rng.shuffle(nodes)
        S.add_nodes_from(nodes)
        ee = edges + [(apex, x) for x in net.leaves]
        rng.shuffle(ee)
        for u, v in ee:
            if rng.random() < 0.5: S.add_edge(u, v)
            else: S.add_edge(v, u)
        ok, emb = nx.check_planarity(S)
        if not ok:
            return []
        o = list(emb.neighbors_cw_order(apex))
        i = o.index(net.leaves[0]); o = o[i:] + o[:i]
        r = [o[0]] + o[:0:-1]
        key = min(tuple(o), tuple(r))
        out[key] = list(key)
    return list(out.values())

seed = int(sys.argv[1]); N = int(sys.argv[2])
maxleaves = int(sys.argv[3]) if len(sys.argv) > 3 else 11
rng = random.Random(seed)
st = collections.Counter(); hist = collections.Counter()
t0 = time.time(); examples = []
while st['checked'] < N:
    n = rng.randint(5, maxleaves)
    ch, root = random_tree_children(n, rng)
    cnt = Counter()
    k = rng.randint(2, 6)
    for _ in range(k):
        E = edge_list(ch, root)
        e1 = rng.choice(E + [None, None])
        if e1 is not None and rng.random() < 0.8:
            # nearby edges: within distance 3 of e1's lower end in the underlying graph
            G = nx.Graph()
            for u, vs in ch.items():
                for v in vs: G.add_edge(u, v)
            near = nx.single_source_shortest_path_length(G, ch[e1[0]][e1[1]], cutoff=3)
            cand = [e for e in E if e[0] in near and ch[e[0]][e[1]] in near]
            e2 = rng.choice(cand) if cand else rng.choice(E)
        else:
            e2 = rng.choice(E)
        ch, root = insert_arc(ch, root, e1, e2, cnt)
    net = Net(ch, root)
    st['built'] += 1
    if not net.is_valid(): st['invalid'] += 1; continue
    if net.level() > 2: st['level > 2'] += 1; continue
    orders = circular_orders(net, rng)
    if not orders: st['nonplanar'] += 1; continue
    try:
        reps = blob_report(net)
    except AssertionError as e:
        st['STRUCTURE VIOLATION'] += 1; examples.append(('structure', str(e), net.ch, net.root)); continue
    M6 = net.nanuq6()
    st['checked'] += 1
    st['orders checked'] += len(orders)
    st['networks with >1 distinct induced order found'] += len(orders) > 1
    first = True
    for o in orders:
        info = check_theorem12(net, order=o, reps=reps, M6=M6)
        if info['viol']:
            st['THEOREM 12 VIOLATION'] += 1
            if len(examples) < 5: examples.append((info['viol'], net.ch, net.root, o))
        if first:
            first = False
            st['critical splits'] += info['ncrit']
            st['critical splits with weight <= 0'] += sum(1 for v in info['crit_values'] if v <= 0)
            st['other splits (first order)'] += len(info['alpha']) - info['ncrit']
            for v in info['crit_values']: hist[v] += 1
    nh = len(net.hyb)
    st['hybrid nodes = %d' % nh] += 1
    st['galled'] += net.is_galled()
    st['with several non-trivial blobs'] += len(reps) >= 2
    st['with a nested blob'] += any(r['kind'] == 'nested' for r in reps)
print("seed", seed, "time %.0fs" % (time.time() - t0))
for k in sorted(st): print("  %-50s %d" % (k, st[k]))
print("  critical weights:", dict(sorted(hist.items())))
for e in examples: print("  EXAMPLE", e)
