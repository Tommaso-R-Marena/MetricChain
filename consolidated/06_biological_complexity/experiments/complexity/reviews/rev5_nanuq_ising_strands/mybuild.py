# mybuild.py -- REVIEWER'S OWN CODE: explicit rooted networks composed of blobs.
# A fragment is (children dict, top node, list of slots); a slot is a node that still needs one
# pendant child.  compose() hangs fragments below the slots.  The checker (myblob.py) does NOT use
# the specs: it reads the blob structure from the final graph.
import itertools, random
from mynet import Net


class Namer:
    def __init__(self):
        self.c = 0
    def new(self, pre):
        self.c += 1
        return '%s_%d' % (pre, self.c)


def chain(ch, start, names, end):
    """directed path start -> names[0] -> ... -> names[-1] -> end (adds edges to ch)"""
    prev = start
    for v in names:
        ch.setdefault(prev, []).append(v)
        prev = v
    ch.setdefault(prev, []).append(end)


def frag_nested(nm, kB, k1, k2, src):
    """nested blob.  src = ('A',) | ('B', j) with 0<=j<=kB | ('C', j) with 0<=j<=k2 : the place of the
    source node s (between b_j and b_{j+1}, b_0 = h1, b_{kB+1} = t ; between c_j and c_{j+1}, c_0 = h2,
    c_{k2+1} = t).  Returns (ch, s, slots, names) ; slots in the order b_1..b_kB, x_1..x_k1, y, c_1..c_k2."""
    ch = {}
    s = nm.new('s'); t = nm.new('t'); h1 = nm.new('h1'); h2 = nm.new('h2')
    b = [nm.new('b') for _ in range(kB)]       # b[0] = b_1 nearest h1
    x = [nm.new('x') for _ in range(k1)]
    c = [nm.new('c') for _ in range(k2)]       # c[0] = c_1 nearest h2
    # C from h1 to h2
    chain(ch, h1, x, h2)
    if src[0] == 'A':
        ch.setdefault(s, []).append(t)
        ch.setdefault(s, []).append(h1)
        chain(ch, t, list(reversed(b)), h1)
        chain(ch, t, list(reversed(c)), h2)
    elif src[0] == 'B':
        j = src[1]
        chain(ch, s, list(reversed(b[:j])), h1)       # s -> b_j -> ... -> b_1 -> h1
        chain(ch, s, b[j:], t)                        # s -> b_{j+1} -> ... -> b_kB -> t
        ch.setdefault(t, []).append(h1)               # A
        chain(ch, t, list(reversed(c)), h2)
    elif src[0] == 'C':
        j = src[1]
        chain(ch, s, list(reversed(c[:j])), h2)       # s -> c_j -> ... -> c_1 -> h2
        chain(ch, s, c[j:], t)                        # s -> c_{j+1} -> ... -> c_k2 -> t
        ch.setdefault(t, []).append(h1)               # A
        chain(ch, t, list(reversed(b)), h1)           # B
    else:
        raise ValueError(src)
    slots = b + x + [h2] + c
    return ch, s, slots, dict(s=s, t=t, h1=h1, h2=h2, b=b, x=x, c=c)


def frag_cycle(nm, a, bb):
    """level-1 cycle with source s on top, a nodes on one side, bb on the other, hybrid h"""
    ch = {}
    s = nm.new('s'); h = nm.new('g')
    l = [nm.new('l') for _ in range(a)]
    r = [nm.new('r') for _ in range(bb)]
    chain(ch, s, l, h)
    chain(ch, s, r, h)
    return ch, s, l + r + [h]


def frag_g2a(nm, q):
    """galled level-2 blob, source on the third path: s -> t1, s -> t2 ; t1 -q0-> g1 <-q1- t2 ;
    t1 -q2-> g2 <-q3- t2  (q = four chain lengths)"""
    ch = {}
    s = nm.new('s'); t1 = nm.new('t'); t2 = nm.new('t'); g1 = nm.new('g'); g2 = nm.new('g')
    cs = [[nm.new('p') for _ in range(k)] for k in q]
    ch[s] = [t1, t2]
    chain(ch, t1, cs[0], g1); chain(ch, t2, cs[1], g1)
    chain(ch, t1, cs[2], g2); chain(ch, t2, cs[3], g2)
    return ch, s, cs[0] + cs[1] + cs[2] + cs[3] + [g1, g2]


def frag_g2b(nm, q):
    """galled level-2 blob, source on the path of g1: s -q0-> g1 ; s -q1-> t2 ; t2 -> t1 ; t1 -q2-> g1 ;
    t1 -q3-> g2 ; t2 -q4-> g2"""
    ch = {}
    s = nm.new('s'); t1 = nm.new('t'); t2 = nm.new('t'); g1 = nm.new('g'); g2 = nm.new('g')
    cs = [[nm.new('p') for _ in range(k)] for k in q]
    chain(ch, s, cs[0], g1); chain(ch, s, cs[1], t2)
    ch.setdefault(t2, []).append(t1)
    chain(ch, t1, cs[2], g1); chain(ch, t1, cs[3], g2); chain(ch, t2, cs[4], g2)
    return ch, s, cs[0] + cs[1] + cs[2] + cs[3] + cs[4] + [g1, g2]


def compose(spec, nm, leafnames):
    """spec: ('leaf',) | ('tree', s1, s2) | ('nested', kB,k1,k2, src, [specs]) | ('cyc', a, b, [specs])
    | ('g2a', q, [specs]) | ('g2b', q, [specs]).  Returns (ch, top)."""
    kind = spec[0]
    if kind == 'leaf':
        x = leafnames.pop(0)
        return {}, x
    if kind == 'tree':
        v = nm.new('v')
        ch = {v: []}
        for sub in spec[1:]:
            c2, top = compose(sub, nm, leafnames)
            ch.update(c2)
            ch[v].append(top)
        return ch, v
    if kind == 'nested':
        ch, s, slots, _ = frag_nested(nm, spec[1], spec[2], spec[3], spec[4])
        subs = spec[5]
    elif kind == 'cyc':
        ch, s, slots = frag_cycle(nm, spec[1], spec[2])
        subs = spec[3]
    elif kind == 'g2a':
        ch, s, slots = frag_g2a(nm, spec[1])
        subs = spec[2]
    elif kind == 'g2b':
        ch, s, slots = frag_g2b(nm, spec[1])
        subs = spec[2]
    else:
        raise ValueError(kind)
    assert len(subs) == len(slots), (kind, len(subs), len(slots))
    for p, sub in zip(slots, subs):
        c2, top = compose(sub, nm, leafnames)
        for u, vs in c2.items():
            ch.setdefault(u, []).extend(vs)
        ch.setdefault(p, []).append(top)
    return ch, s


def build(spec):
    nm = Namer()
    nleaves = count_leaves(spec)
    names = ['L%02d' % i for i in range(nleaves)]
    ch, top = compose(spec, nm, names)
    return Net(ch, top)


def count_leaves(spec):
    if spec[0] == 'leaf':
        return 1
    if spec[0] == 'tree':
        return sum(count_leaves(s) for s in spec[1:])
    return sum(count_leaves(s) for s in spec[-1])


def bloblet_spec(kB, k1, k2, src=('A',), sizes=None):
    """N[kB,k1,k2] with a leaf (or a caterpillar clade of the given size) at every position.
    sizes: list in slot order b_1..b_kB, x_1..x_k1, y, c_1..c_k2"""
    P = kB + k1 + k2 + 1
    if sizes is None:
        sizes = [1] * P
    return ('nested', kB, k1, k2, src, [clade_spec(m) for m in sizes])


def clade_spec(m, shape='cat'):
    if m == 1:
        return ('leaf',)
    if shape == 'cat':
        s = ('leaf',)
        for _ in range(m - 1):
            s = ('tree', s, ('leaf',))
        return s
    # balanced
    a = m // 2
    return ('tree', clade_spec(a, shape), clade_spec(m - a, shape))


# ---------- random specs ----------
def composition(rng, total, parts):
    """random composition of total into `parts` positive integers"""
    assert total >= parts >= 1
    cuts = sorted(rng.sample(range(1, total), parts - 1))
    return [b - a for a, b in zip([0] + cuts, cuts + [total])]


def weak_composition(rng, total, parts):
    c = composition(rng, total + parts, parts)
    return [v - 1 for v in c]


def rand_spec(rng, nleaves, root=True, depth=0, pnest=0.45, maxpos=9):
    if nleaves == 1:
        return ('leaf',)
    r = rng.random()
    if depth >= 3:
        r = 2.0                       # only trees deep down
    if r < pnest:
        # nested blob with P pendant positions (below); if not root the source is one more position
        P = rng.randint(1, min(nleaves, maxpos))
        ks = weak_composition(rng, P - 1, 3)
        # bias: sort so that kB tends to be large
        if rng.random() < 0.6:
            ks.sort(reverse=True)
            if ks[1] == 0 and ks[0] >= 2 and rng.random() < 0.8:
                ks[0] -= 1; ks[1] += 1
            kB, k1, k2 = ks[0], ks[1], ks[2]
            if rng.random() < 0.5:
                k1, k2 = max(k1, k2), min(k1, k2)
        else:
            kB, k1, k2 = ks
        choices = [('B', j) for j in range(kB + 1)] + [('C', j) for j in range(k2 + 1)]
        if root:
            choices += [('A',)] * 3
        src = rng.choice(choices)
        sizes = composition(rng, nleaves, P)
        subs = [rand_spec(rng, m, False, depth + 1, pnest, maxpos) for m in sizes]
        return ('nested', kB, k1, k2, src, subs)
    if r < pnest + 0.15:
        P = rng.randint(1, min(nleaves, 6))
        a = rng.randint(0, P - 1)
        sizes = composition(rng, nleaves, P)
        return ('cyc', a, P - 1 - a, [rand_spec(rng, m, False, depth + 1, pnest, maxpos) for m in sizes])
    if r < pnest + 0.27 and nleaves >= 2:
        # galled level 2
        if root and rng.random() < 0.4:
            P = rng.randint(2, min(nleaves, 7))
            q = weak_composition(rng, P - 2, 4)
            sizes = composition(rng, nleaves, P)
            return ('g2a', q, [rand_spec(rng, m, False, depth + 1, pnest, maxpos) for m in sizes])
        P = rng.randint(2, min(nleaves, 7))
        q = weak_composition(rng, P - 2, 5)
        sizes = composition(rng, nleaves, P)
        return ('g2b', q, [rand_spec(rng, m, False, depth + 1, pnest, maxpos) for m in sizes])
    a = rng.randint(1, nleaves - 1)
    return ('tree', rand_spec(rng, a, False, depth + 1, pnest, maxpos), rand_spec(rng, nleaves - a, False, depth + 1, pnest, maxpos))
