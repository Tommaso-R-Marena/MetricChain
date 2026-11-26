# t6_table.py -- REVIEWER'S OWN CODE: the table of local terms in Step 4 of Theorem 12, computed from
# explicit rooted networks (nested blob, a clade of 3 leaves at every position), and Proposition 2
# (alpha/2 = Phi4 + sum Phi5 + sum Phi6) for the critical split on the same networks.
import itertools, collections, sys
from fractions import Fraction
from mynet import Net, alphas
from mybuild import frag_nested, Namer
from mysplits import norm, wq, phi4_any, phi5_any, phi6_any

def explicit_sizes(kB, k1, k2, src, size):
    nm = Namer()
    ch, s, slots, names = frag_nested(nm, kB, k1, k2, src)
    lab = {}
    for j, v in enumerate(names['b']): lab[v] = 'b%d' % (j + 1)
    for j, v in enumerate(names['x']): lab[v] = 'x%d' % (j + 1)
    for j, v in enumerate(names['c']): lab[v] = 'c%d' % (j + 1)
    lab[names['h2']] = 'y'
    posof = {}
    for p in slots:
        # caterpillar clade of `size` leaves
        leaves = ['%s.%d' % (lab[p], i) for i in range(size)]
        for x in leaves: posof[x] = lab[p]
        top = leaves[0]
        for i in range(1, size):
            v = nm.new('v'); ch[v] = [top, leaves[i]]; top = v
        ch.setdefault(p, []).append(top)
    return Net(ch, s), posof

maxpos = int(sys.argv[1]) if len(sys.argv) > 1 else 7
size = 3
T4 = collections.Counter(); T5 = collections.defaultdict(collections.Counter); T6 = collections.defaultdict(collections.Counter)
nets = 0; prop2_bad = 0
for P in range(4, maxpos + 1):
    for kB in range(2, P):
        for k1 in range(1, P - kB):
            k2 = P - 1 - kB - k1
            if k2 < 0: continue
            src = ('A',)
            net, posof = explicit_sizes(kB, k1, k2, src, size)
            assert net.is_valid()
            nets += 1
            n = len(net.leaves)
            order = net.circular_order()
            # rotate / reflect so that the order starts with the block of b1 and continues with b2 (or c / y)
            def blocks(o):
                out = []
                for x in o:
                    if not out or out[-1] != posof[x]: out.append(posof[x])
                if len(out) > 1 and out[0] == out[-1]: out.pop()
                return out
            expect = ['b%d' % j for j in range(1, kB + 1)] + ['c%d' % e for e in range(k2, 0, -1)] + ['y'] + ['x%d' % a for a in range(k1, 0, -1)]
            ok = False
            for o in (order, order[::-1]):
                for r in range(n):
                    oo = o[r:] + o[:r]
                    if posof[oo[0]] == 'b1' and posof[oo[-1]] != 'b1' and blocks(oo) == expect:
                        order2 = oo; ok = True; break
                if ok: break
            assert ok, (kB, k1, k2, blocks(order))
            idx = {x: i for i, x in enumerate(order2)}
            NL = net.leaves
            S = set()
            for m in net.displayed_splits():
                S.add(norm(sum(1 << idx[NL[i]] for i in range(n) if (m >> i) & 1), n))
            S = frozenset(S)
            # U = leaves at b- and c-positions = points 0..p-1 ; V = the rest
            p = sum(1 for x in order2 if posof[x][0] in 'bc')
            u1, up, v1, vq = 0, p - 1, p, n - 1
            assert posof[order2[u1]] == 'b1' and posof[order2[up]] == ('c1' if k2 >= 1 else 'b%d' % kB)
            assert posof[order2[v1]] == 'y' and posof[order2[vq]] == 'x1'
            def typ(i):
                a = posof[order2[i]]
                if a == 'b1': return 'b1'
                if a[0] == 'b':
                    j = int(a[1:])
                    if k2 == 0 and j == kB: return 'b_kB(k2=0)'
                    return 'b_M'
                if a == 'c1': return 'c1'
                if a[0] == 'c': return 'c_e>=2'
                if a == 'y': return 'y'
                if a == 'x1': return 'x1'
                return 'x_a>=2'
            f4 = phi4_any(S, u1, up, v1, vq); T4[f4] += 1
            total = f4
            for z in range(u1 + 1, up):
                f = phi5_any(S, u1, z, up, v1, vq); T5[typ(z)][f] += 1; total += f
            for z in range(v1 + 1, vq):
                f = phi5_any(S, v1, z, vq, u1, up); T5[typ(z)][f] += 1; total += f     # mirror image
            for z, w in itertools.combinations(range(u1 + 1, up), 2):
                f = phi6_any(S, u1, z, w, up, v1, vq); total += f
                same = posof[order2[z]] == posof[order2[w]]
                key = tuple(sorted((typ(z), typ(w)))) + (('same position',) if same else ())
                T6[key][f] += 1
            for z, w in itertools.combinations(range(v1 + 1, vq), 2):
                f = phi6_any(S, v1, z, w, vq, u1, up); total += f
                same = posof[order2[z]] == posof[order2[w]]
                key = tuple(sorted((typ(z), typ(w)))) + (('same position',) if same else ())
                T6[key][f] += 1
            # Proposition 2 against the metric
            M6 = net.nanuq6()
            Pm = [NL.index(x) for x in order2]
            al = alphas(M6, Pm)
            # S_ij with {x_{i+1..j}} = V = points p..n-1 -> i = p-1, j = n-1
            a = Fraction(al[(p - 1, n - 1)], 6)
            if a != 2 * total:
                prop2_bad += 1
            # formula of Theorem 12(b) with all sizes = size
            G = k2 * size if k2 >= 1 else size
            Mn = (kB - 1) if k2 >= 1 else (kB - 2)
            pred = size * G + size * (size * k1) - (Mn * (Mn - 1) // 2) * size * size
            if a != pred:
                print("FORMULA MISMATCH", (kB, k1, k2), a, pred)
print("networks:", nets, "(nested blob, clade of %d leaves at every position, up to %d positions)" % (size, maxpos))
print("Proposition 2 for the critical split: mismatches", prop2_bad)
print("Phi4 values:", dict(T4))
print("Phi5 by type:")
for k in sorted(T5): print("   %-14s %s" % (k, {str(a): b for a, b in T5[k].items()}))
print("Phi6 by pair of types:")
for k in sorted(T6): print("   %-45s %s" % (' + '.join(k), {str(a): b for a, b in T6[k].items()}))
