#!/usr/bin/env python3
"""
Referee's independent brute-force enumerator (review3).  Written from the definitions in
docs/complexity/STRANDS_ALGORITHM.md section 1 and STRANDS_NN_HARDNESS.md section 1 BEFORE reading
the author's code.  Does not import anything of the author's.

Objects
-------
strands : list of words over ACGT (labelled 0..c-1)
circular ordering : a permutation of the labels with label 0 first
structure : set of pairs of complementary bases, each base at most once, non-crossing on the
            circle of the ordering, connected (checked both by "no face with >= 2 nicks" and,
            optionally, by union-find on the graph of covalent bonds and pairs)
faces : computed by walking the boundary (links and chords)
R(S) : number of slot rotations mapping each strand to a strand of equal sequence and S to S
physical ensemble : labelled structures modulo permutations of equal strands (orbits computed by
            brute force over the whole group, `physical_sum_by_orbits`), or - once that
            identification has been tested - orbits of the slot rotations on (species word,
            structure) pairs (`physical_sum_by_words`).
"""
import itertools
import math
from fractions import Fraction

PAIRS = {('A', 'T'), ('T', 'A'), ('C', 'G'), ('G', 'C')}


class Model:
    """Loop weights.  hp(u,a,b): hairpin with u unpaired, closing letters a (5' side) and b.
    il(l1,a1,b1,l2,a2,b2): nick-free two-pair face; going round the face one meets a segment
    with l1 unpaired bases from a paired base with letter a1 to a paired base with letter b1,
    then a chord, then a segment with l2 unpaired bases from letter a2 to letter b2, then a chord.
    The model must be invariant under exchanging the two segments (it is a function of the face);
    `sym_il` enforces this by canonicalising.  Multiloop: ma * mb^b * mc^u."""

    def __init__(self, hp, il, ma, mb, mc, name=''):
        self.hp = hp
        self._il = il
        self.ma = Fraction(ma)
        self.mb = Fraction(mb)
        self.mc = Fraction(mc)
        self.name = name

    def il(self, l1, a1, b1, l2, a2, b2):
        k1 = (l1, a1, b1, l2, a2, b2)
        k2 = (l2, a2, b2, l1, a1, b1)
        return self._il(*min(k1, k2))


def faces_of(partner, nick_after, N):
    """Walk all faces.  partner[p] = q or -1.  nick_after[p] True if the link p -> p+1 (mod N) is
    a nick.  Returns list of faces; a face is (nnicks, segments) with segments a list of
    (start_base, end_base, unpaired) in boundary order; for the face without chords start=end=-1."""
    seen = [False] * N
    faces = []
    for p0 in range(N):
        if seen[p0]:
            continue
        # walk the face containing link p0 -> p0+1
        segs = []
        nn = 0
        p = p0
        # find segment structure: we start in the middle of a segment possibly; collect raw walk
        walk = []  # sequence of ('L', p) links and ('C', a, b) chords
        while True:
            if seen[p]:
                break
            seen[p] = True
            walk.append(('L', p))
            if nick_after[p]:
                nn += 1
            q = (p + 1) % N
            if partner[q] >= 0:
                walk.append(('C', q, partner[q]))
                p = partner[q]
            else:
                p = q
        # rotate walk so that it starts right after a chord (if any chord)
        cidx = [k for k, x in enumerate(walk) if x[0] == 'C']
        if not cidx:
            faces.append((nn, [(-1, -1, len(walk))], 0))
            continue
        k0 = cidx[-1]
        walk = walk[k0 + 1:] + walk[:k0 + 1]
        cur_start = None
        cnt = 0
        for x in walk:
            if x[0] == 'L':
                if cur_start is None:
                    cur_start = x[1]
                    cnt = 0
                cnt += 1
            else:
                segs.append((cur_start, x[1], cnt - 1))
                cur_start = None
        faces.append((nn, segs, len(segs)))
    return faces


def structure_weight(partner, nick_after, N, letters, model, facecache=None):
    """Returns None if disconnected (a face with >= 2 nicks), else the weight w(S) (Fraction)."""
    w = Fraction(1)
    for nn, segs, b in faces_of(partner, nick_after, N):
        if nn >= 2:
            return None
        if nn == 1:
            continue  # exterior loop, weight 1
        if b == 0:
            raise AssertionError('face with no chord and no nick')
        if b == 1:
            (x, y, u), = segs
            w *= model.hp(u, letters[x], letters[y])
        elif b == 2:
            (x1, y1, u1), (x2, y2, u2) = segs
            w *= model.il(u1, letters[x1], letters[y1], u2, letters[x2], letters[y2])
        else:
            u = sum(s[2] for s in segs)
            w *= model.ma * model.mb ** b * model.mc ** u
    return w


def gen_structures(letters, N, visit, partner):
    """Enumerate all non-crossing sets of complementary pairs on positions 0..N-1 (linear order =
    circle cut anywhere).  Calls visit() with the global partner array filled."""
    can = [[(letters[i], letters[j]) in PAIRS for j in range(N)] for i in range(N)]

    def gen(i, j, cont):
        if i > j:
            cont()
            return
        gen(i + 1, j, cont)
        ci = can[i]
        for k in range(i + 1, j + 1):
            if ci[k]:
                partner[i] = k
                partner[k] = i
                gen(i + 1, k - 1, lambda: gen(k + 1, j, cont))
                partner[i] = -1
                partner[k] = -1

    gen(0, N - 1, visit)


def layout(strand_seq):
    """strand_seq: list of words in circular order.  Returns letters, nick_after, N, slot_of, idx_of,
    start positions."""
    letters = []
    slot_of = []
    idx_of = []
    starts = []
    for t, s in enumerate(strand_seq):
        starts.append(len(letters))
        for i, ch in enumerate(s):
            letters.append(ch)
            slot_of.append(t)
            idx_of.append(i)
    N = len(letters)
    nick_after = [False] * N
    for t, s in enumerate(strand_seq):
        nick_after[starts[t] + len(s) - 1] = True
    return letters, nick_after, N, slot_of, idx_of, starts


def connected_by_union_find(partner, nick_after, N):
    par = list(range(N))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for p in range(N):
        if not nick_after[p]:
            a, b = find(p), find((p + 1) % N)
            par[a] = b
        if partner[p] > p:
            a, b = find(p), find(partner[p])
            par[a] = b
    r = find(0)
    return all(find(x) == r for x in range(N))


def rot_symmetry(partner, strand_seq, starts, N):
    """R(S): number of slot shifts j (0 <= j < c) with seq(slot t) = seq(slot t+j) for all t and S
    mapped to itself."""
    c = len(strand_seq)
    R = 0
    for j in range(c):
        if any(strand_seq[t] != strand_seq[(t + j) % c] for t in range(c)):
            continue
        shift = starts[j] - starts[0]
        ok = True
        for p in range(N):
            q = partner[p]
            pp = (p + shift) % N
            if q < 0:
                if partner[pp] >= 0:
                    ok = False
                    break
            else:
                if partner[pp] != (q + shift) % N:
                    ok = False
                    break
        if ok:
            R += 1
    return R


def all_connected(strand_seq, model, check_uf=False):
    """Yield (partner tuple, weight, R) for all connected non-crossing structures of the circular
    arrangement strand_seq (a list of words)."""
    letters, nick_after, N, slot_of, idx_of, starts = layout(strand_seq)
    partner = [-1] * N
    out = []

    def visit():
        w = structure_weight(partner, nick_after, N, letters, model)
        if check_uf:
            assert (w is not None) == connected_by_union_find(partner, nick_after, N)
        if w is None:
            return
        R = rot_symmetry(partner, strand_seq, starts, N)
        out.append((tuple(partner), w, R))

    gen_structures(letters, N, visit, partner)
    return out, (letters, nick_after, N, slot_of, idx_of, starts)


def group_elements(strands):
    """All permutations g of the labels with strands[g[t]] == strands[t]."""
    c = len(strands)
    classes = {}
    for t, s in enumerate(strands):
        classes.setdefault(s, []).append(t)
    cls = list(classes.values())
    res = []
    for perms in itertools.product(*[itertools.permutations(cl) for cl in cls]):
        g = list(range(c))
        for cl, pm in zip(cls, perms):
            for a, b in zip(cl, pm):
                g[a] = b
        res.append(tuple(g))
    return res


def physical_sum_by_orbits(strands, model, alphas, check_uf=True, stats=None):
    """Definition-level reference.  Enumerate labelled connected unpseudoknotted structures over all
    (c-1)! circular orderings, form orbits under the full group of permutations of equal strands by
    brute force, compute R from the definition for one representative, and return
    {alpha: sum over orbits of w^alpha R^-alpha}.  Also checks: every labelled structure occurs under
    exactly one circular ordering; w and R are constant on orbits; |orbit| * R = |G|."""
    c = len(strands)
    G = group_elements(strands)
    labelled = {}  # frozenset of labelled pairs -> (w, R)
    nlab = 0
    for rest in itertools.permutations(range(1, c)):
        order = (0,) + rest
        seq = [strands[t] for t in order]
        structs, (letters, nick_after, N, slot_of, idx_of, starts) = all_connected(seq, model, check_uf)
        for partner, w, R in structs:
            key = frozenset(
                ((order[slot_of[p]], idx_of[p]), (order[slot_of[q]], idx_of[q])) if (order[slot_of[p]], idx_of[p]) < (order[slot_of[q]], idx_of[q])
                else ((order[slot_of[q]], idx_of[q]), (order[slot_of[p]], idx_of[p]))
                for p, q in enumerate(partner) if q > p)
            assert key not in labelled, 'labelled structure non-crossing under two circular orderings'
            labelled[key] = (w, R)
            nlab += 1
    # orbits
    seen = set()
    total = {a: Fraction(0) for a in alphas}
    norb = 0
    Rhist = {}
    for key, (w, R) in labelled.items():
        if key in seen:
            continue
        orbit = set()
        for g in G:
            img = frozenset(tuple(sorted(((g[a[0]], a[1]), (g[b[0]], b[1])))) for a, b in key)
            orbit.add(img)
        for img in orbit:
            assert img in labelled, 'image of a structure under a permutation of equal strands is missing'
            assert labelled[img] == (w, R), 'w or R not constant on an orbit'
        assert len(orbit) * R == len(G), ('orbit-stabiliser', len(orbit), R, len(G))
        seen |= orbit
        norb += 1
        Rhist[R] = Rhist.get(R, 0) + 1
        for a in alphas:
            total[a] += power(w, a) / power(Fraction(R), a)
    if stats is not None:
        stats['labelled'] = nlab
        stats['orbits'] = norb
        stats['Rhist'] = Rhist
    return total


def power(x, a):
    """x^a for Fraction x and integer a (exact).  0^0 = 1; 0^negative raises."""
    if isinstance(a, int):
        if a >= 0:
            return x ** a
        return Fraction(1) / (x ** (-a))
    raise TypeError('exact power needs integer exponent')


def distinct_words(strands):
    """All distinct sequences (arrangements) of the multiset of strand words."""
    return sorted(set(itertools.permutations(strands)))


def physical_sum_by_words(strands, model, alphas, stats=None, check_uf=False):
    """Second reference: (1/c) * sum over (word Y, structure S) of w^alpha R^(1-alpha), i.e. orbit
    counting for the cyclic group of slot shifts acting on pairs (arrangement, structure).  Uses
    only the orbit-stabiliser theorem, no Moebius inversion, no central loop."""
    c = len(strands)
    total = {a: Fraction(0) for a in alphas}
    Rhist = {}
    n = 0
    for Y in distinct_words(strands):
        structs, _ = all_connected(list(Y), model, check_uf)
        for partner, w, R in structs:
            n += 1
            Rhist[R] = Rhist.get(R, 0) + 1
            for a in alphas:
                total[a] += power(w, a) * power(Fraction(R), 1 - a)
    for a in alphas:
        total[a] /= c
    if stats is not None:
        stats['pairs'] = n
        stats['Rhist_pairs'] = Rhist
    return total


# ----------------------------------------------------------------------------------------------
# a few models
# ----------------------------------------------------------------------------------------------

def model_unit():
    return Model(lambda u, a, b: Fraction(1), lambda *k: Fraction(1), 1, 1, 1, 'unit (counting)')


def model_sizes():
    """size-dependent hairpin, interior, affine multiloop with all three parameters non-trivial"""
    def hp(u, a, b):
        return Fraction(u + 2, 7)

    def il(l1, a1, b1, l2, a2, b2):
        if l1 == 0 and l2 == 0:
            return Fraction(5, 2)
        return Fraction(3, 2 + 3 * (l1 + l2) + 5 * abs(l1 - l2))

    return Model(hp, il, Fraction(2, 3), Fraction(3, 5), Fraction(7, 11), 'sizes')


def model_letters(seed=1):
    """letter- and size-dependent weights, pseudo-random but face-invariant (Model.il canonicalises)"""
    import random

    cache = {}

    def val(key):
        if key not in cache:
            rnd = random.Random(repr((seed, key)))
            cache[key] = Fraction(rnd.randint(1, 9), rnd.randint(1, 9))
        return cache[key]

    def hp(u, a, b):
        return val(('hp', u, a, b))

    def il(*k):
        return val(('il',) + k)

    return Model(hp, il, val('ma'), val('mb'), val('mc'), 'letters%d' % seed)


def model_hp3():
    """hairpins need at least 3 unpaired bases (weight 0 below), stack-favouring"""
    def hp(u, a, b):
        return Fraction(0) if u < 3 else Fraction(1, u)

    def il(l1, a1, b1, l2, a2, b2):
        if l1 == 0 and l2 == 0:
            return Fraction(4)
        return Fraction(1, 1 + l1 + l2)

    return Model(hp, il, Fraction(1, 2), Fraction(2, 3), Fraction(5, 4), 'hp3')


if __name__ == '__main__':
    import sys
    strands = sys.argv[1:] or ['GC', 'GC']
    for mk in (model_unit, model_sizes, model_letters):
        m = mk()
        st = {}
        a = physical_sum_by_orbits(strands, m, [0, 1, 2, 3, -1], stats=st)
        st2 = {}
        b = physical_sum_by_words(strands, m, [0, 1, 2, 3, -1], stats=st2)
        print(m.name, st, st2)
        for al in a:
            print('  alpha', al, a[al], b[al], 'OK' if a[al] == b[al] else 'MISMATCH')
