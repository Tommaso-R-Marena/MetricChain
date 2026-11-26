# t1_exhaust.py n k [procs] -- REVIEWER'S OWN CODE.
# All rooted binary networks obtained from every rooted binary tree shape on n leaves by k hybrid-arc
# insertions (tail on any edge or above the root, head on any edge, same edge allowed -> parallel edges).
# Every valid (Def. 2.1, root = LSA) outer-labeled planar network of level <= 2 is checked against
# 'Blobs, positions, sizes', Lemma C and Theorem 12 (a),(b).  Non-planar ones: only the structural
# statements of Lemma C that do not need planarity.
import sys, itertools, collections, time
from multiprocessing import Pool
from mynet import Net
from mygen import tree_shapes, edge_list, insert_arc, Counter
from myblob import blob_report, check_theorem12


def expand(args):
    ch0, root0, k, n = args
    stats = collections.Counter()
    examples = []
    crit_hist = collections.Counter()
    kinds = collections.Counter()
    def rec(ch, root, depth, cnt):
        if depth == k:
            net = Net(ch, root)
            stats['candidates'] += 1
            if not net.is_valid():
                return
            stats['valid'] += 1
            lev = net.level()
            if lev > 2:
                stats['level>2'] += 1
                return
            order = net.circular_order()
            try:
                reps = blob_report(net)
            except AssertionError as e:
                stats['STRUCTURE VIOLATION'] += 1
                if len(examples) < 5:
                    examples.append(('structure', str(e), net.ch, net.root))
                return
            gal = net.is_galled()
            has_nested = any(r['kind'] == 'nested' for r in reps)
            if gal == has_nested:
                stats['GALLED/NESTED MISMATCH'] += 1
                if len(examples) < 5:
                    examples.append(('galled-vs-nested', gal, net.ch, net.root))
            for r in reps:
                if len(r['sources']) != 1:
                    stats['SOURCE COUNT VIOLATION'] += 1
            if order is None:
                stats['nonplanar'] += 1
                for r in reps:
                    if r['kind'] == 'nested' and r['AB_both_have_positions']:
                        stats['nonplanar nested with positions on A and B'] += 1
                return
            stats['planar'] += 1
            stats['planar galled' if gal else 'planar nongalled'] += 1
            if n < 4:
                return
            info = check_theorem12(net, order=order, reps=reps)
            for kk in info['nested']:
                kinds[kk] += 1
            for v in info['crit_values']:
                crit_hist[v] += 1
            if info['viol']:
                stats['THEOREM 12 VIOLATION'] += 1
                if len(examples) < 5:
                    examples.append(('thm12', info['viol'], net.ch, net.root, info['order']))
            # galled planar: Theorem 7 says everything is fine (no critical split)
            return
        E = edge_list(ch, root)
        for e1 in E + [None]:
            for e2 in E:
                c2 = Counter(); c2.c = cnt.c
                ch2, root2 = insert_arc(ch, root, e1, e2, c2)
                rec(ch2, root2, depth + 1, c2)
    rec(ch0, root0, 0, Counter())
    return stats, examples, crit_hist, kinds


if __name__ == '__main__':
    n = int(sys.argv[1]); k = int(sys.argv[2]); procs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    t0 = time.time()
    shapes = tree_shapes(n)
    # split the work: one task per (shape, first insertion)
    tasks = []
    for ch, root in shapes:
        if k == 0:
            tasks.append((ch, root, 0, n)); continue
        E = edge_list(ch, root)
        for e1 in E + [None]:
            for e2 in E:
                c = Counter()
                ch2, root2 = insert_arc(ch, root, e1, e2, c)
                # counters restart inside expand; rename-safe because names t/h are unique per insertion depth
                tasks.append((ch2, root2, k - 1, n))
    # in expand the counter restarts at 0 -> name clash with t1/h1 ; avoid by renaming first-level nodes
    def ren(task):
        ch, root, kk, nn = task
        m = {u: ('z' + u if isinstance(u, str) and (u.startswith('t') or u.startswith('h')) else u) for u in ch}
        ch2 = {m.get(u, u): [m.get(v, v) for v in vs] for u, vs in ch.items()}
        return (ch2, m.get(root, root), kk, nn)
    tasks = [ren(t) for t in tasks]
    tot = collections.Counter(); ex = []; hist = collections.Counter(); kinds = collections.Counter()
    with Pool(procs) as pool:
        for stats, examples, crit_hist, kd in pool.imap_unordered(expand, tasks, chunksize=4):
            tot.update(stats); ex += examples; hist.update(crit_hist); kinds.update(kd)
    print("n =", n, "insertions =", k, "tree shapes", len(shapes), "time %.0fs" % (time.time() - t0))
    for key in sorted(tot):
        print("  %-45s %d" % (key, tot[key]))
    print("  nested blobs by (kB,k1,k2):", dict(sorted(kinds.items())))
    print("  critical splits (k1>=1,kB>=2) by value of formula 12(b):", dict(sorted(hist.items())))
    for e in ex[:10]:
        print("  EXAMPLE", e)
