#!/usr/bin/env python3
"""r20_enum.py -- workstream R20: an independent exhaustive enumerator of secondary structures of
several strands, written from the definitions of section 1 of the note under review
(STRANDS_NN_HARDNESS.md), without reading the reviewed division's code.

Model implemented (exactly as in the note, section 1):
  * strands are words, written 5'->3'; a base is (strand index, position);
  * a secondary structure S is a set of disjoint pairs of complementary bases;
  * for a cyclic order pi of the strands the bases are put on a circle, strand after strand, each
    5'->3'; two consecutive bases are joined by a LINK: a covalent bond, or a NICK when they belong
    to different strands (or are the last and first base of the only strand);
  * S is unpseudoknotted if for some pi its chords do not cross;
  * the chords cut the disc into |S|+1 faces; a face with exactly one nick is an exterior loop; a
    nick-free face with k chords is a hairpin (k=1), a stack / bulge / interior loop (k=2), or a
    multiloop (k>=3);
  * S is connected if the graph (bases; covalent bonds and pairs) is connected.

Nothing here designs, optimises or evaluates a sequence for any purpose: the inputs are the synthetic
strings of a reduction from a packing problem, and the outputs are counts.

Only the Python standard library is used.  All energies are integers (exact arithmetic).
"""
from itertools import permutations

WATSON_CRICK = frozenset([("A", "T"), ("T", "A"), ("C", "G"), ("G", "C"), ("A", "U"), ("U", "A")])
WC_PLUS_WOBBLE = WATSON_CRICK | frozenset([("G", "T"), ("T", "G"), ("G", "U"), ("U", "G")])


# ----------------------------------------------------------------------------------------------
# circle of a cyclic order
# ----------------------------------------------------------------------------------------------
class Circle:
    """The bases of `strands` on a circle in the cyclic order `order` (a tuple of strand indices)."""

    __slots__ = ("strands", "order", "N", "letter", "slot", "strand", "idx", "nick_after", "base_id", "c")

    def __init__(self, strands, order):
        self.strands = strands
        self.order = tuple(order)
        self.c = len(strands)
        offs = []
        tot = 0
        for s in strands:
            offs.append(tot)
            tot += len(s)
        self.N = tot
        self.letter = []      # letter at circle position p
        self.slot = []        # slot (index in `order`) of the strand at p
        self.strand = []      # strand index (in `strands`) at p
        self.idx = []         # index inside the strand (0-based, 5'->3')
        self.nick_after = []  # is the link p -> p+1 (mod N) a nick?
        self.base_id = []     # order-independent identifier of the base at p
        for sl, t in enumerate(self.order):
            s = strands[t]
            for i, ch in enumerate(s):
                self.letter.append(ch)
                self.slot.append(sl)
                self.strand.append(t)
                self.idx.append(i)
                self.nick_after.append(i == len(s) - 1)
                self.base_id.append(offs[t] + i)


def cyclic_orders(c):
    """All (c-1)! cyclic orders of 0..c-1, each written with strand 0 first."""
    for rest in permutations(range(1, c)):
        yield (0,) + rest


# ----------------------------------------------------------------------------------------------
# enumeration of the non-crossing matchings of one circle
# ----------------------------------------------------------------------------------------------
def enum_noncrossing(circ, pairing, visit, prune_two_nicks=False):
    """Call visit(partner) once for every non-crossing matching of the circle `circ` (partner[p] is the
    circle position paired with p, or -1; the list is reused: copy it if you keep it).

    The matching is generated as a word over {unpaired, open, close}: position p is unpaired, or the
    first end of a chord (pushed on a stack), or the second end of the chord whose first end is on top
    of the stack.  This is a bijection with non-crossing matchings on a line, and a matching on a
    circle is non-crossing iff it is non-crossing on the line obtained by cutting the circle anywhere.

    prune_two_nicks=True abandons a partial structure as soon as some face has two nicks.  (By Fact 1
    of the note these are exactly the disconnected structures; this option is validated against the
    unpruned enumeration + union-find in r20_validate.py before it is relied upon.)
    """
    N = circ.N
    letter = circ.letter
    nick_after = circ.nick_after
    partner = [-1] * N
    stack = []          # open positions
    cnt = []            # cnt[d] = nicks seen so far on the face directly under the chord opened by stack[d]
    outer = [1 if nick_after[N - 1] else 0]   # the wrap-around link N-1 -> 0 lies on the outer face
    letters = sorted(set(letter))
    comp = {a: [b for b in letters if (a, b) in pairing] for a in letters}
    # suffix counts: rem[a][p] = number of positions >= p with letter a
    rem = {a: [0] * (N + 2) for a in letters}
    for p in range(N - 1, -1, -1):
        for a in letters:
            rem[a][p] = rem[a][p + 1] + (1 if letter[p] == a else 0)
    can_open = {a: bool(comp[a]) for a in letters}
    nopen = {a: 0 for a in letters}

    if prune_two_nicks and outer[0] >= 2:   # cannot happen (one link), kept for symmetry
        return

    def feasible(p_next):
        # necessary condition: every open base can still be closed by a later complementary base
        for a in letters:
            if nopen[a]:
                tot = 0
                for b in comp[a]:
                    tot += rem[b][p_next]
                if nopen[a] > tot:
                    return False
        return True

    def rec(p):
        # the link p-1 -> p lies on the face of the current top of the stack
        # (the wrap-around link N-1 -> 0 is already counted in `outer`, so p = N is excluded here)
        bumped = None
        if 0 < p < N and nick_after[p - 1]:
            if stack:
                cnt[-1] += 1
                bumped = len(cnt) - 1
                if prune_two_nicks and cnt[-1] >= 2:
                    cnt[-1] -= 1
                    return
            else:
                outer[0] += 1
                bumped = -1
                if prune_two_nicks and outer[0] >= 2:
                    outer[0] -= 1
                    return
        if p == N:
            if not stack:
                visit(partner)
        else:
            a = letter[p]
            # (1) unpaired
            if feasible(p + 1):
                rec(p + 1)
            # (2) open
            if can_open[a]:
                stack.append(p)
                cnt.append(0)
                nopen[a] += 1
                if feasible(p + 1):
                    rec(p + 1)
                nopen[a] -= 1
                cnt.pop()
                stack.pop()
            # (3) close
            if stack:
                q = stack[-1]
                b = letter[q]
                if (b, a) in pairing:
                    stack.pop()
                    saved = cnt.pop()
                    nopen[b] -= 1
                    partner[q] = p
                    partner[p] = q
                    if feasible(p + 1):
                        rec(p + 1)
                    partner[q] = -1
                    partner[p] = -1
                    nopen[b] += 1
                    cnt.append(saved)
                    stack.append(q)
        if bumped is not None:
            if bumped == -1:
                outer[0] -= 1
            else:
                cnt[bumped] -= 1

    rec(0)


# ----------------------------------------------------------------------------------------------
# faces
# ----------------------------------------------------------------------------------------------
def faces(circ, partner):
    """The faces of the disc cut by the chords of `partner`.

    A face is traced as a cycle of links: after the link p -> p+1 comes the link that starts at
    partner[p+1] if p+1 is paired (follow the chord), and at p+1 otherwise.
    Returns a list of faces; a face is (nn, k, segs):
        nn   = number of nicks on its boundary,
        k    = number of chords on its boundary,
        segs = list of (first_position, number_of_links): maximal runs of links between two chords,
               i.e. the bases first, first+1, ..., first+number_of_links (mod N), of which the first
               and the last are paired and the others unpaired (if k = 0 there is one "segment" that
               is the whole circle).
    For a non-crossing matching the number of faces is |S| + 1 (Euler); a crossing matching gives fewer.
    """
    N = circ.N
    nick_after = circ.nick_after
    seen = [False] * N
    out = []
    for p0 in range(N):
        if seen[p0]:
            continue
        links = []
        jumps = []
        p = p0
        while True:
            seen[p] = True
            links.append(p)
            q = p + 1
            if q == N:
                q = 0
            r = partner[q]
            if r >= 0:
                jumps.append(True)
                p = r
            else:
                jumps.append(False)
                p = q
            if p == p0:
                break
        nn = 0
        for l in links:
            if nick_after[l]:
                nn += 1
        k = sum(jumps)
        L = len(links)
        if k == 0:
            segs = [(links[0], L)]
        else:
            # rotate so that the list ends with a jump
            last = max(i for i in range(L) if jumps[i])
            rot = links[last + 1:] + links[:last + 1]
            rj = jumps[last + 1:] + jumps[:last + 1]
            segs = []
            start = rot[0]
            n = 0
            for l, j in zip(rot, rj):
                if n == 0:
                    start = l
                n += 1
                if j:
                    segs.append((start, n))
                    n = 0
        out.append((nn, k, segs))
    return out


def kind_of(face):
    """Loop type of a face, exactly as in section 1 of the note."""
    nn, k, segs = face
    if nn >= 2:
        return "multinick"       # only in disconnected structures
    if nn == 1:
        return "exterior"
    if k == 0:
        return "empty"           # cannot occur: a face without chords contains all c >= 1 nicks
    if k == 1:
        return "hairpin"
    if k == 2:
        u1 = segs[0][1] - 1
        u2 = segs[1][1] - 1
        if u1 == 0 and u2 == 0:
            return "stack"
        if u1 == 0 or u2 == 0:
            return "bulge"
        return "interior"
    return "multi"


# ----------------------------------------------------------------------------------------------
# connectivity (union-find; independent of the faces)
# ----------------------------------------------------------------------------------------------
def connected_uf(circ, partner):
    N = circ.N
    par = list(range(N))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    comps = N
    for p in range(N):
        if not circ.nick_after[p]:
            q = p + 1 if p + 1 < N else 0
            a, b = find(p), find(q)
            if a != b:
                par[a] = b
                comps -= 1
        r = partner[p]
        if r > p:
            a, b = find(p), find(r)
            if a != b:
                par[a] = b
                comps -= 1
    return comps == 1


# ----------------------------------------------------------------------------------------------
# order-independent descriptions
# ----------------------------------------------------------------------------------------------
def key_of(circ, partner):
    """The labelled structure as a sorted tuple of pairs of order-independent base identifiers."""
    bid = circ.base_id
    out = []
    for p, r in enumerate(partner):
        if r > p:
            a, b = bid[p], bid[r]
            out.append((a, b) if a < b else (b, a))
    out.sort()
    return tuple(out)


def successor_from_structure(strands, key):
    """succ(t) for every strand t, computed from the labelled structure alone (no circle): walk the
    boundary of the face of the nick after the 3'-end of t backwards.  For a connected unpseudoknotted
    structure this is the successor of t in THE cyclic order for which the chords do not cross; the
    function returns None if the walk does not terminate within N steps (structure not of that kind)."""
    offs = []
    tot = 0
    for s in strands:
        offs.append(tot)
        tot += len(s)
    N = tot
    owner = [0] * N
    first = [False] * N
    for t, s in enumerate(strands):
        for i in range(len(s)):
            owner[offs[t] + i] = t
        first[offs[t]] = True
    partner = [-1] * N
    for a, b in key:
        partner[a] = b
        partner[b] = a
    succ = []
    for t, s in enumerate(strands):
        x = offs[t] + len(s) - 1
        steps = 0
        while True:
            e = partner[x] if partner[x] >= 0 else x
            if first[e]:
                succ.append(owner[e])
                break
            x = e - 1
            steps += 1
            if steps > N + 1:
                return None
    return succ


def symmetry_number(circ, partner):
    """R(S): the number of rotations of the circle by whole strands that map every strand to a strand
    with the same sequence and the set of chords to itself (the identity is counted)."""
    c = circ.c
    order = circ.order
    strands = circ.strands
    seqs = [strands[t] for t in order]
    start = []
    tot = 0
    for s in seqs:
        start.append(tot)
        tot += len(s)
    N = circ.N
    pairs = set()
    for p, r in enumerate(partner):
        if r > p:
            pairs.add((p, r))
    R = 0
    for sh in range(c):
        if any(seqs[j] != seqs[(j + sh) % c] for j in range(c)):
            continue
        # position map
        pm = [0] * N
        for j in range(c):
            j2 = (j + sh) % c
            for i in range(len(seqs[j])):
                pm[start[j] + i] = start[j2] + i
        ok = True
        for (p, r) in pairs:
            a, b = pm[p], pm[r]
            if a > b:
                a, b = b, a
            if (a, b) not in pairs:
                ok = False
                break
        if ok:
            R += 1
    return R


# ----------------------------------------------------------------------------------------------
# brute force over ALL matchings (for validation on tiny systems only)
# ----------------------------------------------------------------------------------------------
def all_matchings(strands, pairing):
    """All sets of disjoint complementary pairs of bases (labelled structures), crossing or not."""
    letters = "".join(strands)
    N = len(letters)
    out = []
    cur = []
    used = [False] * N

    def rec(i):
        while i < N and used[i]:
            i += 1
        if i == N:
            out.append(tuple(sorted(cur)))
            return
        used[i] = True
        rec(i + 1)                       # i unpaired
        for j in range(i + 1, N):
            if not used[j] and (letters[i], letters[j]) in pairing:
                used[j] = True
                cur.append((i, j))
                rec(i + 1)
                cur.pop()
                used[j] = False
        used[i] = False

    rec(0)
    return out


def noncrossing_on(circ, key):
    """Direct test: are the chords of the labelled structure `key` pairwise non-crossing on `circ`?"""
    pos = {b: p for p, b in enumerate(circ.base_id)}
    ch = []
    for a, b in key:
        p, q = pos[a], pos[b]
        if p > q:
            p, q = q, p
        ch.append((p, q))
    for i in range(len(ch)):
        p, q = ch[i]
        for j in range(i + 1, len(ch)):
            r, s = ch[j]
            if (p < r < q) != (p < s < q):
                return False
    return True


def connected_graph(strands, key):
    """Connectivity of (bases; covalent bonds, pairs) by depth-first search (third implementation)."""
    N = sum(len(s) for s in strands)
    adj = [[] for _ in range(N)]
    o = 0
    for s in strands:
        for i in range(len(s) - 1):
            adj[o + i].append(o + i + 1)
            adj[o + i + 1].append(o + i)
        o += len(s)
    for a, b in key:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * N
    st = [0]
    seen[0] = True
    n = 1
    while st:
        x = st.pop()
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True
                n += 1
                st.append(y)
    return n == N
