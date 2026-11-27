#!/usr/bin/env python3
"""
Referee's tests of Theorems 1, 1c, 1d (and Theorem 3 counts, Remark 5) of STRANDS_NN_HARDNESS.md, with the
referee's own enumerator (bf.py).  Does not import the author's code.

For an instance I(a, m, B): template G^B A G^B ... G^B, items C^{a_i}.  All connected non-crossing structures
over all distinct circular arrangements (template first, items as a sequence of lengths) are enumerated with the
generic enumerator; faces come from the generic face walker; "tiling" is decided from the definition, not from
the energy.
"""
import itertools, sys, time
from fractions import Fraction as F
import bf


def instance(a, m, B):
    return 'A'.join(['G' * B] * m), ['C' * x for x in a]


def enumerate_instance(a, m, B, items_subset=None):
    """yield (word, partner, faces, layout) for every connected structure; word = template + item order"""
    templ, items = instance(a, m, B)
    if items_subset is not None:
        items = [items[i] for i in items_subset]
    for perm in sorted(set(itertools.permutations(items))):
        seq = [templ] + list(perm)
        letters, nick_after, N, slot_of, idx_of, starts = bf.layout(seq)
        partner = [-1] * N
        out = []

        def visit():
            fs = bf.faces_of(partner, nick_after, N)
            if any(f[0] >= 2 for f in fs):
                return
            out.append((tuple(partner), fs))

        bf.gen_structures(letters, N, visit, partner)
        for partner_t, fs in out:
            yield seq, partner_t, fs, (letters, nick_after, N, slot_of, idx_of, starts)


def is_tiling(seq, partner, lay, m, B):
    letters, nick_after, N, slot_of, idx_of, starts = lay
    T = len(seq[0])
    # every item base paired; partners of an item form a run of consecutive template positions inside one
    # block, antiparallel; (runs partition the G's automatically if all item bases are paired, sum a_i = mB)
    for t in range(1, len(seq)):
        L = len(seq[t])
        ps = []
        for i in range(L):
            q = partner[starts[t] + i]
            if q < 0:
                return False
            ps.append(q)
        for i in range(L - 1):
            if ps[i + 1] != ps[i] - 1:      # antiparallel: 5'->3' on the item goes 3'->5' on the template
                return False
        blocks = {p // (B + 1) for p in ps}
        if len(blocks) != 1:
            return False
    # all template G's paired?
    for p in range(T):
        if letters[p] == 'G' and partner[p] < 0:
            return False
    return True


def face_info(face, lay):
    """returns dict: nicks, nchords, unpaired positions, item_bonds (covalent bonds inside items), templ_GG_bonds,
    kind, flush flag, u_C (unpaired item bases), u_T (unpaired template bases), dangling list"""
    letters, nick_after, N, slot_of, idx_of, starts = lay
    nn, segs, b = face
    info = {'nn': nn, 'b': b}
    item_bonds = 0
    gg = 0
    unp = []
    dang = []   # (position, number of paired covalent neighbours on this face)
    nick_between_items = 0
    for (x, y, u) in segs:
        if x < 0:
            continue
        p = x
        for step in range(u + 1):
            q = (p + 1) % N
            if nick_after[p]:
                if slot_of[p] != 0 and slot_of[q] != 0:
                    nick_between_items += 1
            else:
                if slot_of[p] == 0:
                    if letters[p] == 'G' and letters[q] == 'G':
                        gg += 1
                else:
                    item_bonds += 1
            p = q
        for step in range(1, u + 1):
            pos = (x + step) % N
            unp.append(pos)
            cnt = 0
            if step == 1 and not nick_after[x]:
                cnt += 1
            if step == u and not nick_after[pos]:
                cnt += 1
            if cnt:
                dang.append((pos, cnt))
    info['item_bonds'] = item_bonds
    info['gg'] = gg
    info['unp'] = unp
    info['dang'] = dang
    info['uC'] = sum(1 for p in unp if letters[p] == 'C')
    info['uT'] = sum(1 for p in unp if letters[p] != 'C')
    if nn == 1:
        info['kind'] = 'ext'
        info['flush'] = (b == 2 and not unp and gg == 1 and nick_between_items == 1)
    elif b == 1:
        info['kind'] = 'hairpin'
    elif b == 2:
        info['kind'] = 'stack' if not unp else 'bulgeint'
    else:
        info['kind'] = 'multi'
    return info


def Til_bruteforce(a, m, B):
    """number of labelled tilings: assignments of items to blocks with exact fill, times orders within blocks"""
    n = len(a)
    tot = 0
    for beta in itertools.product(range(m), repeat=n):
        load = [0] * m
        cnt = [0] * m
        for i, t in enumerate(beta):
            load[t] += a[i]
            cnt[t] += 1
        if all(x == B for x in load):
            w = 1
            for x in cnt:
                for j in range(2, x + 1):
                    w *= j
            tot += w
    return tot


def mult_factor(a):
    r = 1
    for s in set(a):
        k = list(a).count(s)
        for j in range(2, k + 1):
            r *= j
    return r


def analyse(a, m, B, energy, lay_cache={}):
    """energy(info list, letters) -> Fraction.  Returns (min energy of tiling structures, max energy of tiling,
    number of tiling structures (physical), min energy of non-tiling structures, number of structures)."""
    tmin = tmax = None
    ntil = 0
    omin = None
    n = 0
    for seq, partner, fs, lay in enumerate_instance(a, m, B):
        infos = [face_info(f, lay) for f in fs]
        e = energy(infos, lay[0])
        n += 1
        if is_tiling(seq, partner, lay, m, B):
            ntil += 1
            tmin = e if tmin is None else min(tmin, e)
            tmax = e if tmax is None else max(tmax, e)
        else:
            omin = e if omin is None else min(omin, e)
    return tmin, tmax, ntil, omin, n


def cache_structures(a, m, B):
    """Counter of structure signatures.  signature = (is_tiling, n_stacks, sorted tuple of (uC,uT) of the
    bulge/interior loops, n_flush, dangling G, dangling C, A with two paired neighbours, A with one paired
    neighbour (all dangling counts in exterior loops only), sum over exterior loops of item bonds)"""
    from collections import Counter
    res = Counter()
    for seq, partner, fs, lay in enumerate_instance(a, m, B):
        letters = lay[0]
        nst = nfl = dG = dC = dA2 = dA1 = 0
        bul = []
        for f in fs:
            fi = face_info(f, lay)
            k = fi['kind']
            if k == 'stack':
                nst += 1
            elif k == 'bulgeint':
                bul.append((fi['uC'], fi['uT']))
            elif k == 'ext':
                if fi['flush']:
                    nfl += 1
                for pos, cnt in fi['dang']:
                    ch = letters[pos]
                    if ch == 'G':
                        dG += 1
                    elif ch == 'C':
                        dC += 1
                    elif cnt == 2:
                        dA2 += 1
                    else:
                        dA1 += 1
            else:
                raise AssertionError('hairpin or multiloop in an instance: ' + k)
        res[(is_tiling(seq, partner, lay, m, B), nst, tuple(sorted(bul)), nfl, dG, dC, dA2, dA1)] += 1
    return res


# ------------------------------------------------------------------ energy models on signatures
def E_T1(sig, sigma, bulge):
    til, nst, bul, nfl, dG, dC, dA2, dA1 = sig
    return sigma * nst + sum(bulge(uC, uT) for uC, uT in bul)


def E_T1c(sig, sigma, x, gamma_fn):
    til, nst, bul, nfl, dG, dC, dA2, dA1 = sig
    return sigma * nst + sum(gamma_fn(uC, uT) for uC, uT in bul) + x * nfl


def E_T1d(sig, sigma, DG, DC, eA, eA_one, bulge):
    til, nst, bul, nfl, dG, dC, dA2, dA1 = sig
    return sigma * nst + sum(bulge(uC, uT) for uC, uT in bul) - DG * dG - DC * dC + eA * dA2 + eA_one * dA1


INSTANCES = [
    ((1,), 1, 1), ((1, 1), 2, 1), ((2,), 2, 1), ((1, 1, 1), 3, 1), ((2, 1), 3, 1), ((3,), 3, 1), ((2, 2), 4, 1), ((1, 1, 2), 4, 1),
    ((2,), 1, 2), ((1, 1), 1, 2), ((3,), 1, 3), ((1, 2), 1, 3), ((1, 1, 1), 1, 3), ((2, 2), 1, 4), ((1, 3), 1, 4), ((1, 1, 2), 1, 4),
    ((2, 2), 2, 2), ((1, 1, 2), 2, 2), ((1, 3), 2, 2), ((4,), 2, 2), ((1, 1, 1, 1), 2, 2),
    ((3, 3), 2, 3), ((2, 2, 2), 2, 3), ((1, 2, 3), 2, 3), ((2, 4), 2, 3), ((1, 1, 4), 2, 3), ((1, 5), 2, 3), ((1, 1, 2, 2), 2, 3), ((6,), 2, 3),
    ((2, 2, 2), 3, 2), ((1, 1, 2, 2), 3, 2), ((3, 3), 3, 2), ((4, 2), 3, 2), ((1, 2, 3), 3, 2), ((1, 1, 4), 3, 2), ((1, 1, 1, 3), 3, 2),
    ((4, 4), 2, 4), ((3, 5), 2, 4), ((2, 2, 4), 2, 4), ((2, 3, 3), 2, 4), ((1, 3, 4), 2, 4), ((2, 2, 2, 2), 2, 4),
    ((3, 3, 3), 3, 3), ((2, 2, 5), 3, 3), ((1, 4, 4), 3, 3), ((2, 3, 4), 3, 3), ((1, 2, 3, 3), 3, 3),
    ((2, 2, 2, 2), 4, 2), ((1, 1, 2, 4), 4, 2), ((3, 3, 2), 4, 2),
    ((5, 5), 2, 5), ((4, 6), 2, 5), ((2, 3, 5), 2, 5), ((3, 3, 4), 2, 5),
]

if __name__ == '__main__':
    t0 = time.time()
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    import pickle
    cache = {}
    for inst in INSTANCES:
        a, m, B = inst
        cache[inst] = cache_structures(a, m, B)
        ntil = sum(v for s, v in cache[inst].items() if s[0])
        print('cached', inst, sum(cache[inst].values()), 'structures,', len(cache[inst]), 'signatures, tilings (physical)', ntil,
              'Til/prod mu!', F(Til_bruteforce(a, m, B), mult_factor(a)), '[%.0fs]' % (time.time() - t0), flush=True)
        assert ntil * mult_factor(a) == Til_bruteforce(a, m, B)
        pickle.dump(cache, open('hard_cache.pkl', 'wb'))
    print('total structures', sum(sum(v.values()) for v in cache.values()))
