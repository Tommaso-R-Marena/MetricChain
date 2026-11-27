# anchors: (1) Table 1(a) of arXiv:2507.17308v2 (level-1 6-cycle network), (2) N* of the note (Section 6)
import numpy as np
from mynet import Net, alphas, split_mask_of

# (1) 6-sunlet: cycle nodes c0..c5, hybrid at c0 (leaf 'a'), root placed on the cycle opposite to the hybrid
def sunlet(names):
    # names[0] is the hybrid leaf; cycle order names[0..5]
    ch = {}
    # root r above c3 : r -> c3 ... build: r has children c3 and c2?  Put the root on the edge c2-c3
    ch['r'] = ['c2', 'c3']
    ch['c2'] = ['L2', 'c1']; ch['c1'] = ['L1', 'c0']
    ch['c3'] = ['L3', 'c4']; ch['c4'] = ['L4', 'c5']; ch['c5'] = ['L5', 'c0']
    ch['c0'] = ['L0']
    ren = {'L%d' % i: names[i] for i in range(6)}
    ch2 = {ren.get(u, u): [ren.get(v, v) for v in vs] for u, vs in ch.items()}
    return Net(ch2, 'r')

N = sunlet(list('abcdef'))
assert N.is_valid()
M = N.nanuq6()
assert (M % 6 == 0).all()
D = M // 6
L = N.leaves
print("6-sunlet, hybrid leaf a, leaves", L)
print(D)
table1a = {('a','b'):14,('a','c'):17,('a','d'):18,('a','e'):17,('a','f'):14,('b','c'):11,('b','d'):16,('b','e'):19,('b','f'):20,
           ('c','d'):15,('c','e'):18,('c','f'):19,('d','e'):15,('d','f'):16,('e','f'):11}
ok = all(D[L.index(x), L.index(y)] == v for (x, y), v in table1a.items())
print("matches Table 1(a) of the paper with hybrid at a:", ok)
if not ok:
    import itertools
    for rot in range(6):
        names = list('abcdef')[rot:] + list('abcdef')[:rot]
        N2 = sunlet(names); D2 = N2.nanuq6() // 6; L2 = N2.leaves
        print(rot, names[0], all(D2[L2.index(x), L2.index(y)] == v for (x, y), v in table1a.items()))

# (2) N* of the note
ch = {'rho': ['w1', 'w3'], 'w1': ['a1', 'w2'], 'w2': ['a2', 'p1'], 'p1': ['b', 'h1'],
      'w3': ['d', 'q1'], 'q1': ['h1', 'q2'], 'q2': ['h2', 'c'], 'h1': ['u'], 'u': ['x', 'h2'], 'h2': ['y']}
Ns = Net(ch, 'rho')
assert Ns.is_valid()
order = ['a1', 'a2', 'b', 'x', 'y', 'c', 'd']
M = Ns.nanuq6(); assert (M % 6 == 0).all()
L = Ns.leaves
P = [L.index(x) for x in order]
D = (M // 6)[np.ix_(P, P)]
print("N*: NANUQ matrix in order", order); print(D)
note = np.array([[0,21,23,26,26,23,21],[21,0,17,24,26,27,25],[23,17,0,20,24,29,27],[26,24,20,0,20,24,26],
                 [26,26,24,20,0,20,24],[23,27,29,24,20,0,17],[21,25,27,26,24,17,0]])
print("matches the matrix printed in the note:", (D == note).all())
print("galled:", Ns.is_galled(), " level:", Ns.level(), " planar order found:", Ns.circular_order())
al = alphas(M, P)
n = 7
ds = Ns.displayed_splits()
for (i, j), a in sorted(al.items()):
    m = split_mask_of(P, i, j, n)
    side = [order[k] for k in range(i + 1, j + 1)]
    flag = 'displayed' if m in ds else ''
    if a != 0 or flag:
        print(i, j, side, a / 6, flag)
print("displayed trees:", len(Ns.displayed_trees()))
# multiplicity-weighted metric: Corollary 3.4 says circular decomposable with support displayed splits
Mw, mu = Ns.dqm_num()
alw = alphas(Mw, P)
bad = [(i, j) for (i, j), a in alw.items() if a < 0 or ((a > 0) != (split_mask_of(P, i, j, n) in ds))]
print("displayed-quartet metric (weighted): violations of Cor. 3.4:", bad,
      " weight of {x,y}|rest:", [alw[(i, j)] / mu for (i, j) in alw if set(order[i + 1:j + 1]) == {'x', 'y'}])
