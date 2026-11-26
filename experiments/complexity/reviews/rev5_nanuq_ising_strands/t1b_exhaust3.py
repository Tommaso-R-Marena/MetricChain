# t1b_exhaust3.py n [procs] -- REVIEWER'S OWN CODE.
# All networks with THREE hybrid nodes on n (unlabelled) leaves, by three hybrid-arc insertions into
# every tree shape; intermediate 2-hybrid networks are reduced up to isomorphism (the statements tested
# do not depend on leaf labels).  Kept: valid, level <= 2, outer-labeled planar.  Checked: blob structure,
# Lemma C, Theorem 12 (a),(b).   (Level <= 2 with three hybrids means at least two non-trivial blobs.)
import sys, itertools, collections, time
from multiprocessing import Pool
import networkx as nx
from mynet import Net
from mygen import tree_shapes, edge_list, insert_arc, Counter
from myblob import blob_report, check_theorem12


def digraph(ch, root):
    G = nx.MultiDiGraph()
    for u, vs in ch.items():
        for v in vs:
            G.add_edge(u, v)
    for v in G.nodes:
        G.nodes[v]['t'] = '%d%d' % (G.in_degree(v), G.out_degree(v))
    return G


def acyclic(ch):
    G = nx.DiGraph()
    for u, vs in ch.items():
        for v in vs:
            G.add_edge(u, v)
    return nx.is_directed_acyclic_graph(G)


def key(G):
    S = nx.DiGraph(G)
    for u, v in S.edges:
        S[u][v]['m'] = str(G.number_of_edges(u, v))
    return (nx.weisfeiler_lehman_graph_hash(S, node_attr='t', edge_attr='m', iterations=4),
            nx.weisfeiler_lehman_graph_hash(S.reverse(), node_attr='t', edge_attr='m', iterations=4),
            S.number_of_nodes())


def dedupe(items):
    buckets = collections.defaultdict(list)
    out = []
    nm = lambda a, b: a['t'] == b['t']
    for ch, root in items:
        G = digraph(ch, root)
        k = key(G)
        found = False
        for H in buckets[k]:
            if nx.is_isomorphic(G, H, node_match=nm):
                found = True
                break
        if not found:
            buckets[k].append(G)
            out.append((ch, root))
    return out


def final_stage(args):
    ch, root, n = args
    stats = collections.Counter(); examples = []; hist = collections.Counter()
    E = edge_list(ch, root)
    for e1 in E + [None]:
        for e2 in E:
            c = Counter(); c.c = 1000
            ch2, root2 = insert_arc(ch, root, e1, e2, c)
            net = Net(ch2, root2)
            stats['candidates'] += 1
            if not net.is_valid():
                continue
            stats['valid'] += 1
            if net.level() > 2:
                stats['level>2'] += 1
                continue
            stats['valid level<=2'] += 1
            try:
                reps = blob_report(net)
            except AssertionError as e:
                stats['STRUCTURE VIOLATION'] += 1
                if len(examples) < 3: examples.append(('structure', str(e), net.ch, net.root))
                continue
            gal = net.is_galled()
            has_nested = any(r['kind'] == 'nested' for r in reps)
            if gal == has_nested:
                stats['GALLED/NESTED MISMATCH'] += 1
            order = net.circular_order()
            if order is None:
                stats['nonplanar'] += 1
                continue
            stats['planar'] += 1
            stats['planar galled' if gal else 'planar nongalled'] += 1
            stats['planar with %d non-trivial blobs' % len(reps)] += 1
            info = check_theorem12(net, order=order, reps=reps)
            for v in info['crit_values']:
                hist[v] += 1
            if info['viol']:
                stats['THEOREM 12 VIOLATION'] += 1
                if len(examples) < 3: examples.append(('thm12', info['viol'], net.ch, net.root, info['order']))
    return stats, examples, hist


if __name__ == '__main__':
    n = int(sys.argv[1]); procs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    level0 = tree_shapes(n)
    cur = level0
    for depth in range(2):
        nxt = []
        for ch, root in cur:
            E = edge_list(ch, root)
            for e1 in E + [None]:
                for e2 in E:
                    c = Counter(); c.c = 100 * (depth + 1)
                    ch2, root2 = insert_arc(ch, root, e1, e2, c)
                    if acyclic(ch2):
                        nxt.append((ch2, root2))
        before = len(nxt)
        cur = dedupe(nxt)
        print("after %d insertion(s): %d acyclic candidates, %d up to isomorphism  (%.0fs)" % (depth + 1, before, len(cur), time.time() - t0), flush=True)
    tot = collections.Counter(); ex = []; hist = collections.Counter()
    with Pool(procs) as pool:
        for stats, examples, h in pool.imap_unordered(final_stage, [(ch, root, n) for ch, root in cur], chunksize=8):
            tot.update(stats); ex += examples; hist.update(h)
    print("n =", n, "three insertions; time %.0fs" % (time.time() - t0))
    for k in sorted(tot): print("  %-40s %d" % (k, tot[k]))
    print("  critical splits by value of 12(b):", dict(sorted(hist.items())))
    for e in ex[:10]: print("  EXAMPLE", e)
