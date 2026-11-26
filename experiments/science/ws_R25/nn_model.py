#!/usr/bin/env python3
"""R25 -- the formal nearest-neighbour loop model of STRANDS_NN_HARDNESS.md (sections 1-3),
re-implemented from the statements of the note (their code was not available to this workstream).

Everything here is combinatorics on words over {A, C, G}: strands on a circle, pair sets, faces.

Three enumerators of increasing speed and decreasing generality:

  L0  brute force: every set of complementary pairs with each base at most once (no ordering assumed),
      tested against every labelled cyclic ordering of the strands with a pairwise chord-crossing test;
      connectivity by union-find.  Tiny instances only.
  LA  for one cyclic ordering: backtracking over all pairwise non-crossing sets of complementary pairs
      (generic crossing predicate on circle positions), faces as orbits of the link successor map,
      loop types from the definitions of section 1, connectivity by union-find.
  LB  transfer-matrix dynamic programme over nested chords (uses step (a') of the note: every chord joins
      the template to an item, so chords are nested).  Validated against LA where both run.

Signature of a connected structure of I(a, m, B) (template = strand 0, items in the given circular order):
  (tiling, st, fl, nb, L, z, r)
    tiling  1 iff tiling structure BY THE DEFINITION of section 2 (LA) / iff st == M (LB)
    st      number of stacks (no nick, two chords, no unpaired base)
    fl      number of flush faces (two chords, one template bond, one nick between two items, no unpaired base)
    nb      number of bulges + interior loops
    L       template GG bonds lying on a face that is neither a stack nor flush ("loose")
    z       nicks between two items lying on faces that are not flush
    r       faces with a separator A, two chords and no nick (bulge/interior loops over a separator)
"""
import itertools
import resource
from collections import Counter


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def limit_memory(gb=2.0):
    """hard cap on the address space of this process (machine rule of the brief: no process above 2 GB);
    an over-allocation then raises MemoryError instead of growing"""
    lim = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))


COMPLEMENT = {("A", "T"), ("T", "A"), ("C", "G"), ("G", "C")}


def template(m, B):
    return "A".join(["G" * B] * m)


def compositions(q):
    """all tuples of positive integers with sum q (= all (multiset, order) pairs of item sizes)"""
    if q == 0:
        yield ()
        return
    for first in range(1, q + 1):
        for rest in compositions(q - first):
            yield (first,) + rest


class Circle:
    """Strands placed on a circle in the given order, each 5'->3'; link i joins position i and i+1 (mod N)."""

    def __init__(self, strands):
        self.strands = list(strands)
        self.letters = "".join(strands)
        self.N = len(self.letters)
        self.sid = []
        for s, w in enumerate(strands):
            self.sid.extend([s] * len(w))
        N = self.N
        c = len(strands)
        # nick: the two ends belong to different strands (or last/first base of the only strand)
        self.nick = [(self.sid[i] != self.sid[(i + 1) % N]) or (c == 1 and i == N - 1) for i in range(N)]
        assert sum(self.nick) == c


def chords_cross(a, b, c, d):
    """chords {a,b}, {c,d} between distinct points of a circle labelled 0..N-1; a<b, c<d"""
    return (a < c < b < d) or (c < a < d < b)


def enumerate_noncrossing(circ, leaf):
    """call leaf(partner) for every set of pairwise non-crossing complementary pairs (each base at most once)"""
    N = circ.N
    letters = circ.letters
    partner = [-1] * N
    chords = []

    def rec(i):
        while i < N and partner[i] != -1:
            i += 1
        if i == N:
            leaf(partner)
            return
        rec(i + 1)  # i unpaired
        li = letters[i]
        for j in range(i + 1, N):
            if partner[j] == -1 and (li, letters[j]) in COMPLEMENT:
                ok = True
                for (a, b) in chords:
                    if chords_cross(a, b, i, j):
                        ok = False
                        break
                if ok:
                    partner[i] = j
                    partner[j] = i
                    chords.append((i, j))
                    rec(i + 1)
                    chords.pop()
                    partner[i] = -1
                    partner[j] = -1

    rec(0)


def is_connected(circ, partner):
    """graph on the bases with covalent bonds and pairs as edges (section 1); union-find"""
    N = circ.N
    par = list(range(N))

    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    for i in range(N):
        if not circ.nick[i]:
            a, b = find(i), find((i + 1) % N)
            if a != b:
                par[a] = b
        p = partner[i]
        if p > i:
            a, b = find(i), find(p)
            if a != b:
                par[a] = b
    root = find(0)
    return all(find(u) == root for u in range(N))


def faces(circ, partner):
    """faces of the disc cut by the chords = orbits of the successor map on links.
    Returns a list of faces; a face is (links, sides) where links is the cyclic list of link indices and
    sides is the list of the numbers of links of the maximal chord-free runs (one run per chord of the face;
    a face without chord has one run)."""
    N = circ.N
    seen = [False] * N
    out = []
    for s in range(N):
        if seen[s]:
            continue
        links = []
        ends = []  # for each link: True if its head is paired (a chord is traversed after it)
        i = s
        while not seen[i]:
            seen[i] = True
            links.append(i)
            h = (i + 1) % N
            p = partner[h]
            if p == -1:
                ends.append(False)
                i = h
            else:
                ends.append(True)
                i = p
        # runs between chord traversals (cyclic)
        k = sum(ends)
        if k == 0:
            sides = [len(links)]
        else:
            first = ends.index(True)
            rot = ends[first + 1:] + ends[:first + 1]
            sides = []
            run = 0
            for e in rot:
                run += 1
                if e:
                    sides.append(run)
                    run = 0
            assert run == 0 and len(sides) == k
        out.append((links, sides, k))
    return out


def classify_face(circ, partner, face):
    """loop type by the definitions of section 1 and of 'flush' in section 3.  Template = strand 0.
    returns (type, data) with type in {'disc','ext','flush','hairpin','stack','bulge','interior','multi'}"""
    links, sides, k = face
    N = circ.N
    sid = circ.sid
    letters = circ.letters
    nnick = 0
    item_nicks = 0   # nicks between two items
    tGG = 0          # template bonds between two G's
    tbonds = 0       # template bonds
    ibonds = 0       # covalent bonds of items
    seps = 0         # unpaired A on the boundary
    unp = 0
    for i in links:
        h = (i + 1) % N
        if circ.nick[i]:
            nnick += 1
            if sid[i] != 0 and sid[h] != 0:
                item_nicks += 1
        elif sid[i] == 0:
            tbonds += 1
            if letters[i] == "G" and letters[h] == "G":
                tGG += 1
        else:
            ibonds += 1
        if partner[h] == -1:
            unp += 1
            if letters[h] == "A":
                seps += 1
    data = dict(nnick=nnick, item_nicks=item_nicks, tGG=tGG, tbonds=tbonds, ibonds=ibonds, seps=seps,
                unp=unp, k=k, nlinks=len(links))
    if nnick >= 2:
        return "disc", data
    if nnick == 1:
        if k == 2 and unp == 0 and len(links) == 2 and tbonds == 1 and item_nicks == 1:
            return "flush", data
        return "ext", data
    if k == 1:
        return "hairpin", data
    if k == 2:
        if unp == 0:
            return "stack", data
        if min(sides) == 1:
            return "bulge", data
        return "interior", data
    return "multi", data


def tiling_by_definition(circ, partner, m, B):
    """section 2: 'every item is paired, base by base and antiparallel, with a run of consecutive G's inside one
    block, and these runs partition the G's of the template'.  Template = strand 0 at positions 0..T-1."""
    T = len(circ.strands[0])
    covered = set()
    pos = T
    for w in circ.strands[1:]:
        ps = list(range(pos, pos + len(w)))
        pos += len(w)
        qs = [partner[p] for p in ps]
        if any(q == -1 for q in qs):
            return False
        if any(not (0 <= q < T) or circ.letters[q] != "G" for q in qs):
            return False
        for j in range(len(qs) - 1):
            if qs[j + 1] != qs[j] - 1:   # antiparallel: 5'->3' on the item runs 3'->5' on the template
                return False
        if len({q // (B + 1) for q in qs}) != 1:
            return False
        covered.update(qs)
    allG = {q for q in range(T) if circ.letters[q] == "G"}
    return covered == allG


class StructureError(Exception):
    pass


def signature(circ, partner, m, B):
    """signature (tiling, st, fl, nb, L, z, r) of a CONNECTED structure, from the generic face decomposition.
    Raises StructureError if a hairpin/multiloop occurs or the number of exterior loops is not c."""
    fs = faces(circ, partner)
    npairs = sum(1 for p in partner if p != -1) // 2
    if len(fs) != npairs + 1:
        raise StructureError("number of faces != |S|+1")
    st = fl = nb = L = z = r = 0
    next_ = 0
    for f in fs:
        typ, d = classify_face(circ, partner, f)
        if typ == "disc":
            raise StructureError("face with two nicks in a connected structure")
        if typ in ("hairpin", "multi"):
            raise StructureError("hairpin or multiloop")
        if typ == "stack":
            st += 1
            if not (d["tGG"] == 1 and d["ibonds"] == 1 and d["nlinks"] == 2):
                raise StructureError("stack that is not the GG/CC stack of (H1)")
        elif typ == "flush":
            fl += 1
            if d["tGG"] != 1:
                raise StructureError("flush face without a template GG bond")
        else:
            L += d["tGG"]
            z += d["item_nicks"]
            if typ in ("bulge", "interior"):
                nb += 1
                if d["seps"] >= 1:
                    r += 1
        if typ in ("ext", "flush"):
            next_ += 1
    if next_ != len(circ.strands):
        raise StructureError("number of exterior loops != c")
    til = 1 if tiling_by_definition(circ, partner, m, B) else 0
    return (til, st, fl, nb, L, z, r)


def level_A(m, B, order, check=True):
    """all connected unpseudoknotted structures of I(a,m,B) for the circular order (template, items in 'order').
    Returns (Counter of signatures, stats).  check=True also verifies Fact 1 on every non-crossing pair set."""
    circ = Circle([template(m, B)] + ["C" * a for a in order])
    cnt = Counter()
    stats = dict(noncrossing=0, connected=0, fact1_violations=0)

    def leaf(partner):
        stats["noncrossing"] += 1
        conn = is_connected(circ, partner)
        if check:
            fs = faces(circ, partner)
            two = any(sum(1 for i in f[0] if circ.nick[i]) >= 2 for f in fs)
            if conn == two:
                stats["fact1_violations"] += 1
        if conn:
            stats["connected"] += 1
            cnt[signature(circ, partner, m, B)] += 1

    enumerate_noncrossing(circ, leaf)
    return cnt, stats


def level_B(m, B, order):
    """transfer-matrix DP over nested chords (t_1<...<t_K on the template, c_1>...>c_K on the items).
    Returns Counter of signatures (tiling, st, fl, nb, L, z, r) with tiling := (st == M)."""
    T = m * B + m - 1
    tl = template(m, B)
    Gpos = [p for p in range(T) if tl[p] == "G"]
    # prefix count of separators: sepc[p] = number of A at positions < p
    sepc = [0] * (T + 1)
    for p in range(T):
        sepc[p + 1] = sepc[p] + (1 if tl[p] == "A" else 0)
    item_of = []
    for idx, a in enumerate(order):
        item_of.extend([idx] * a)
    q = len(item_of)
    n = len(order)
    M = q - n
    assert q == m * B
    # state[(t, c)] -> Counter{(st, fl, nb, L, z, r): count}
    state = {}
    # first chord (outermost): c in the last item; F_0 has template positions 0..t
    for t in Gpos:
        gg0 = t - 2 * sepc[t]
        for c in range(q - 1, -1, -1):
            if item_of[c] != n - 1:
                break
            state[(t, c)] = Counter({(0, 0, 0, gg0, 0, 0): 1})
    result = Counter()
    # process states in order of increasing t (transitions go to larger t)
    for t in Gpos:
        for c in range(q - 1, -1, -1):
            cur = state.get((t, c))
            if not cur:
                continue
            # close: (t, c) is the innermost chord iff c is in the first item; F_K has positions t..T-1
            if item_of[c] == 0:
                ggK = (T - 1 - t) - 2 * (sepc[T] - sepc[t])
                for (st, fl, nb, L, z, r), w in cur.items():
                    result[(1 if st == M else 0, st, fl, nb, L + ggK, z, r)] += w
            # extend to an inner chord (t2 > t, c2 < c) with at most one nick between c2 and c
            for t2 in Gpos:
                if t2 <= t:
                    continue
                dt = t2 - t
                sep = sepc[t2] - sepc[t]
                gg = dt - 2 * sep
                for c2 in range(c - 1, -1, -1):
                    nk = item_of[c] - item_of[c2]
                    if nk > 1:
                        break
                    dc = c - c2
                    tight = (dt == 1 and dc == 1)
                    if nk == 0:
                        if tight:
                            delta = (1, 0, 0, 0, 0, 0)
                        else:
                            delta = (0, 0, 1, gg, 0, 1 if sep >= 1 else 0)
                    else:
                        if tight:
                            delta = (0, 1, 0, 0, 0, 0)
                        else:
                            delta = (0, 0, 0, gg, 1, 0)
                    tgt = state.get((t2, c2))
                    if tgt is None:
                        tgt = state[(t2, c2)] = Counter()
                    d0, d1, d2, d3, d4, d5 = delta
                    for (st, fl, nb, L, z, r), w in cur.items():
                        tgt[(st + d0, fl + d1, nb + d2, L + d3, z + d4, r + d5)] += w
            del state[(t, c)]
    return result


def level_0(m, B, sizes):
    """Brute force on a labelled instance: every partial matching between the G's and the C's, every labelled
    cyclic order (template first, items permuted).  Returns dict: frozenset(pairs) -> list of orders (tuples of
    item labels) for which the pair set is non-crossing, restricted to CONNECTED pair sets; plus the number of
    all pair sets and of connected ones.  Bases are (strand, index) with strand 0 the template."""
    tl = template(m, B)
    n = len(sizes)
    Gs = [(0, i) for i in range(len(tl)) if tl[i] == "G"]
    Cs = [(s + 1, i) for s in range(n) for i in range(sizes[s])]
    # connectivity does not depend on the order: union-find on bases
    def connected(pairs):
        par = {}
        bases = [(0, i) for i in range(len(tl))] + Cs
        for b in bases:
            par[b] = b

        def find(u):
            while par[u] != u:
                par[u] = par[par[u]]
                u = par[u]
            return u
        for i in range(len(tl) - 1):
            par[find((0, i))] = find((0, i + 1))
        for s in range(n):
            for i in range(sizes[s] - 1):
                par[find((s + 1, i))] = find((s + 1, i + 1))
        for (g, c) in pairs:
            par[find(g)] = find(c)
        root = find((0, 0))
        return all(find(b) == root for b in bases)

    all_sets = 0
    res = {}
    orders = list(itertools.permutations(range(1, n + 1)))
    pos_maps = []
    for od in orders:
        pm = {}
        p = 0
        for i in range(len(tl)):
            pm[(0, i)] = p
            p += 1
        for s in od:
            for i in range(sizes[s - 1]):
                pm[(s, i)] = p
                p += 1
        pos_maps.append(pm)
    for k in range(0, min(len(Gs), len(Cs)) + 1):
        for gsub in itertools.combinations(Gs, k):
            for cperm in itertools.permutations(Cs, k):
                pairs = tuple(zip(gsub, cperm))
                all_sets += 1
                if not connected(pairs):
                    continue
                good = []
                for od, pm in zip(orders, pos_maps):
                    ch = [tuple(sorted((pm[g], pm[c]))) for (g, c) in pairs]
                    ok = True
                    for u in range(len(ch)):
                        for v in range(u + 1, len(ch)):
                            if chords_cross(ch[u][0], ch[u][1], ch[v][0], ch[v][1]):
                                ok = False
                                break
                        if not ok:
                            break
                    if ok:
                        good.append(od)
                res[frozenset(pairs)] = good
    return res, all_sets
