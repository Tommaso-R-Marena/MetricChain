# t5_nestedfacts.py -- REVIEWER'S OWN CODE: the four trees, the circular order, and the finite fact of
# Step 1 of Theorem 12 (six-point restrictions of Sigma[kB,k1,k2]), all from explicit rooted networks.
import itertools, collections, sys
from mynet import Net
from mybuild import bloblet_spec, build, frag_nested, Namer
from myblob import blob_report
from mysplits import norm, six_locally_good_6, restrict, show, globally_good, compatible

def explicit(kB, k1, k2, src):
    """N[kB,k1,k2] with leaves named by their positions"""
    nm = Namer()
    ch, s, slots, names = frag_nested(nm, kB, k1, k2, src)
    lab = {}
    for j, v in enumerate(names['b']): lab[v] = 'b%d' % (j + 1)
    for j, v in enumerate(names['x']): lab[v] = 'x%d' % (j + 1)
    for j, v in enumerate(names['c']): lab[v] = 'c%d' % (j + 1)
    lab[names['h2']] = 'y'
    for p in slots:
        ch.setdefault(p, []).append(lab[p])
    return Net(ch, s)

def note_order(kB, k1, k2):
    return ['b%d' % j for j in range(1, kB + 1)] + ['c%d' % e for e in range(k2, 0, -1)] + ['y'] + ['x%d' % a for a in range(k1, 0, -1)]

def tree_from_arms(arms, leaves):
    """splits of the tree with a central node and the given arms (each listed from its far end);
    a caterpillar is one arm.  Returns frozenset of frozensets (one side), normalised by excluding leaves[0]"""
    allL = frozenset(leaves)
    sp = set()
    for arm in arms:
        for k in range(1, len(arm) + 1):
            side = frozenset(arm[:k])
            if 1 < len(side) < len(allL) - 1:
                if leaves[0] in side:
                    side = allL - side
                sp.add(side)
    return frozenset(sp)

def four_trees(kB, k1, k2):
    b = ['b%d' % j for j in range(1, kB + 1)]; x = ['x%d' % a for a in range(1, k1 + 1)]; c = ['c%d' % e for e in range(1, k2 + 1)]
    L = note_order(kB, k1, k2)
    T1 = tree_from_arms([c + b[::-1] + x + ['y']], L)
    T2 = tree_from_arms([b, c, ['y'] + x[::-1]], L)
    T3 = tree_from_arms([['y'] + c + b[::-1] + x], L)
    T4 = tree_from_arms([b, ['y'] + c, x[::-1]], L)
    return {T1, T2, T3, T4}

def net_trees(net, L):
    out = set()
    NL = net.leaves
    for t in net.displayed_trees():
        sp = set()
        for m in t:
            side = frozenset(NL[i] for i in range(len(NL)) if (m >> i) & 1)
            if len(side) in (1, len(NL) - 1):
                continue
            if L[0] in side:
                side = frozenset(NL) - side
            sp.add(side)
        out.add(frozenset(sp))
    return out

maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 10
cnt = collections.Counter()
exceptions = collections.Counter()
exc_detail = {}
for s in range(1, maxn):
    for kB in range(s + 1):
        for k1 in range(s - kB + 1):
            k2 = s - kB - k1
            n = s + 1
            L = note_order(kB, k1, k2)
            srcs = [('A',)] + [('B', j) for j in range(kB + 1)] + [('C', j) for j in range(k2 + 1)]
            trees0 = None
            for src in srcs:
                net = explicit(kB, k1, k2, src)
                cnt['networks built'] += 1
                if not net.is_valid(need_lsa=True):
                    cnt['root not LSA / invalid (skipped)'] += 1
                    # still a valid DAG? the semi-directed network is the same; check trees anyway
                    if not net.is_valid(need_lsa=False):
                        cnt['INVALID DAG'] += 1; continue
                tr = net_trees(net, L)
                if tr != four_trees(kB, k1, k2):
                    cnt['FOUR TREES MISMATCH'] += 1
                    print("four trees mismatch", (kB, k1, k2), src)
                if trees0 is None:
                    trees0 = tr
                # circular order: the note's order must be an induced circular order: all displayed splits
                # are intervals of it, and the embedding with apex yields it (bloblet: unique)
                if n >= 3:
                    o = net.circular_order()
                    assert o is not None
                    i0 = o.index(L[0]); rot = o[i0:] + o[:i0]
                    if not (rot == L or rot == [L[0]] + L[:0:-1]):
                        cnt['CIRCULAR ORDER MISMATCH'] += 1
                        print("order mismatch", (kB, k1, k2), src, o)
                # structure as read from the graph
                rep = [r for r in blob_report(net) if r['kind'] == 'nested']
                assert len(rep) == 1
                if rep[0]['B'] is None or tuple(rep[0]['k']) != (kB, k1, k2):
                    # when kB = 0 the two paths entering h1 are both free of positions: fine
                    cnt['parameters read from graph differ'] += 1
                    print("param mismatch", (kB, k1, k2), src, rep[0].get('k'))
            cnt['bloblets'] += 1
            if n < 6:
                continue
            # split system on points 0..n-1 in the note's circular order
            idx = {x: i for i, x in enumerate(L)}
            S = set()
            for t in trees0:
                for side in t:
                    S.add(norm(sum(1 << idx[x] for x in side), n))
            for i in range(n):
                S.add(norm(1 << i, n))
            S = frozenset(S)
            for Y in itertools.combinations(range(n), 6):
                cnt['six-point restrictions'] += 1
                if n <= 7:
                    cnt['six-point restrictions of systems with <= 7 positions'] += 1
                R = restrict(S, Y, n)
                if not six_locally_good_6(R):
                    names = tuple(L[i] for i in Y)
                    typ = (sum(1 for a in names if a[0] == 'b'), sum(1 for a in names if a[0] == 'x'),
                           sum(1 for a in names if a[0] == 'c'), 'y' in names)
                    exceptions[typ] += 1
                    # all nine splits minus the 2-split of the 2nd and 3rd b-leaf?
                    bs = [i for i, a in enumerate(names) if a[0] == 'b']
                    allnine = {norm(sum(1 << ((i + t) % 6) for t in range(k)), 6) for i in range(6) for k in (2, 3)}
                    miss = allnine - set(R)
                    expected = {norm((1 << bs[1]) | (1 << bs[2]), 6)} if len(bs) >= 3 else None
                    ok = (miss == expected) and globally_good(R, 6)
                    cnt['exceptional restrictions'] += 1
                    cnt['exceptional restrictions as described (nine minus {2nd,3rd b}; globally good)'] += ok
                    if not ok:
                        print("UNEXPECTED exceptional restriction", (kB, k1, k2), names, show(R, 6))
for k in sorted(cnt):
    print("%-85s %d" % (k, cnt[k]))
print("exceptional restrictions by (#b, #x, #c, y in Y):", dict(exceptions))
