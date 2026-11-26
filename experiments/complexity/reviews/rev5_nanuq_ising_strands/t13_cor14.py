# t13_cor14.py -- REVIEWER'S OWN CODE: Corollary 14, (i) <=> (ii) <=> (iii), and (i) => conclusion for clade blow-ups
import itertools, random, collections
from mysplits import norm, restrict, six_locally_good_6, interval
from mybuild import rand_spec, build, clade_spec
from myblob import blob_report, check_theorem12

three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
lg = {}; pt = {}
def lg6(R):
    if R not in lg: lg[R] = six_locally_good_6(R)
    return lg[R]
def pat6(R):
    if R not in pt: pt[R] = all(a in R for a in three) and any(t not in R for t in two)
    return pt[R]

def cond_i(reps):
    for r in reps:
        if r['kind'] == 'nested':
            kB, k1, k2 = r['k']
            if k1 >= 1 and not (kB <= 2 or (kB == 3 and k2 == 0)):
                return False
    return True

def replace_leaves(spec, rng, p=0.5, maxm=3):
    """replace leaves of a spec by random clades"""
    if spec[0] == 'leaf':
        if rng.random() < p:
            return clade_spec(rng.randint(2, maxm), rng.choice(('cat', 'bal')))
        return spec
    if spec[0] == 'tree':
        return ('tree',) + tuple(replace_leaves(s, rng, p, maxm) for s in spec[1:])
    return spec[:-1] + ([replace_leaves(s, rng, p, maxm) for s in spec[-1]],)

rng = random.Random(41)
st = collections.Counter()
while st['networks'] < 1200:
    n = rng.randint(6, 10)
    spec = rand_spec(rng, n, True, pnest=0.55, maxpos=7)
    net = build(spec)
    if len(net.hyb) > 8 or not net.is_valid(): continue
    order = net.circular_order()
    if order is None: continue
    reps = blob_report(net)
    L = net.leaves
    idx = {x: i for i, x in enumerate(order)}
    S = frozenset(norm(sum(1 << idx[L[i]] for i in range(n) if (m >> i) & 1), n) for m in net.displayed_splits())
    rs = [restrict(S, Y, n) for Y in itertools.combinations(range(n), 6)]
    ii = all(lg6(R) for R in rs)
    iii = not any(pat6(R) for R in rs)
    i = cond_i(reps)
    st['networks'] += 1
    st['(i) holds'] += i
    if not (i == ii == iii):
        st['COROLLARY 14 (i)<=>(ii)<=>(iii) VIOLATED'] += 1
        print("violation", spec, i, ii, iii)
    if i and st['blow-ups checked'] < 250:
        # (iv): the conclusion for a network with leaves replaced by clades (at most 13 leaves)
        spec2 = replace_leaves(spec, rng)
        net2 = build(spec2)
        if len(net2.leaves) <= 13 and net2.is_valid():
            info = check_theorem12(net2)
            st['blow-ups checked'] += 1
            ok = all((a > 0) for a in info['crit_values']) and not info['viol']
            if not ok: st['(i)=>(iv) VIOLATED'] += 1
print(dict(st))
