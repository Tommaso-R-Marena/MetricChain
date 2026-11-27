"""
Reference (exhaustive) enumerator for multi-stranded unpseudoknotted secondary structures and their
nearest-neighbour loop decomposition.  Exact combinatorics; energies are integers or Fractions if the
supplied loop-energy function returns such.

Model (Dirks et al. 2007; Ducloz-Shalaby-Woods 2025 Def. 11; Shalaby-Woods 2026 Def. 7):
  * strands are words over {A,C,G,T}; allowed pairs A-T, C-G;
  * for a circular ordering pi of the strands the bases are placed on a circle; a structure is a set of
    pairwise non-crossing chords (polymer graph); links between circularly consecutive bases are either
    covalent bonds or nicks (between strands);
  * the faces ("loops") are: one face per base pair (i,j) (the region just inside the chord), and the outer face;
    a face with >= 2 nicks <=> the structure is disconnected; a face with exactly one nick is an exterior
    loop; a nick-free face with k pairs on its boundary is a hairpin (k=1), a stack / bulge / interior loop
    (k=2) or a multiloop (k>=3).

Everything here is deliberately naive: it is the ground truth against which reductions and dynamic
programmes are tested.
"""
from itertools import permutations
from fractions import Fraction

COMPLEMENT = {("A", "T"), ("T", "A"), ("C", "G"), ("G", "C")}


def concat(strands, order):
    """order: tuple of strand indices.  Returns (seq, owner, idx, nick_after) where nick_after[p] is True
    iff the link between position p and p+1 (mod N) is a nick."""
    seq, owner, idx, nick_after = [], [], [], []
    for s in order:
        w = strands[s]
        for t, ch in enumerate(w):
            seq.append(ch)
            owner.append(s)
            idx.append(t)
            nick_after.append(t == len(w) - 1)
    return seq, owner, idx, nick_after


def noncrossing_matchings(seq, lo, hi, can_pair):
    """all non-crossing matchings on positions lo..hi-1, as lists of (i,j)."""
    if hi - lo <= 1:
        yield []
        return
    # position lo unpaired
    for m in noncrossing_matchings(seq, lo + 1, hi, can_pair):
        yield m
    # position lo paired with j
    for j in range(lo + 1, hi):
        if can_pair(lo, j):
            for inner in noncrossing_matchings(seq, lo + 1, j, can_pair):
                for outer in noncrossing_matchings(seq, j + 1, hi, can_pair):
                    yield [(lo, j)] + inner + outer


def faces(N, pairs, nick_after):
    """Loop decomposition.  Returns list of faces; each face is a dict with
       closing: (i,j) or None (outer face), pairs: list of pairs on the boundary (closing first if any),
       unpaired: list of unpaired positions on the boundary, nicks: number of nick links on the boundary,
       segs: list of unpaired-run lengths between consecutive boundary pairs (in boundary order)."""
    partner = {}
    for i, j in pairs:
        partner[i] = j
        partner[j] = i
    out = []

    def walk(start, end, closing):
        # boundary from position start to position end inclusive (positions strictly inside the closing pair,
        # or 0..N-1 for the outer face), skipping over child pairs
        bp = [closing] if closing is not None else []
        unp = []
        nicks = 0
        segs = []
        run = 0
        p = start
        prev = closing[0] if closing is not None else None
        while p <= end:
            if prev is not None and nick_after[prev]:
                nicks += 1
            if p in partner and partner[p] > p:
                bp.append((p, partner[p]))
                segs.append(run)
                run = 0
                prev = partner[p]
                p = partner[p] + 1
            else:
                unp.append(p)
                run += 1
                prev = p
                p += 1
        # final link from prev to the closing j (or wrap-around for the outer face)
        if closing is not None:
            if nick_after[prev]:
                nicks += 1
        else:
            if prev is None:
                # no bases at all cannot happen
                pass
            # wrap link (N-1 -> 0) is always a nick; links inside were counted when stepping
            nicks += 1 if nick_after[N - 1] else 0
        segs.append(run)
        return {"closing": closing, "pairs": bp, "unpaired": unp, "nicks": nicks, "segs": segs}

    out.append(walk(0, N - 1, None))
    for i, j in pairs:
        out.append(walk(i + 1, j - 1, (i, j)))
    return out


def classify(face):
    """returns loop type string"""
    if face["nicks"] >= 2:
        return "disconnected"
    if face["nicks"] == 1:
        return "exterior"
    k = len(face["pairs"])
    if k == 1:
        return "hairpin"
    if k == 2:
        a, b = face["segs"]
        if a == 0 and b == 0:
            return "stack"
        if a == 0 or b == 0:
            return "bulge"
        return "interior"
    return "multi"


def connected_uf(N, pairs, owner):
    """union-find connectivity of strands via base pairs (independent check)."""
    strands = sorted(set(owner))
    parent = {s: s for s in strands}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, j in pairs:
        parent[find(owner[i])] = find(owner[j])
    return len({find(s) for s in strands}) == 1


def enumerate_structures(strands, loop_energy, connected_only=True, min_hairpin=0, check=False):
    """Enumerate all (labelled) unpseudoknotted structures, over all circular orderings with strand 0 first.
    Yields (order, pairs_as_labelled_frozenset, energy_without_symmetry, faces_summary).
    loop_energy(kind, face, seq) -> number.
    If connected_only is False, disconnected structures are yielded with the energies of their faces computed
    with kind 'disconnected' passed to loop_energy for faces having >= 2 nicks (BPM/BPS-type models)."""
    c = len(strands)
    for rest in permutations(range(1, c)):
        order = (0,) + rest
        seq, owner, idx, nick_after = concat(strands, order)
        N = len(seq)

        def can_pair(i, j):
            if (seq[i], seq[j]) not in COMPLEMENT:
                return False
            if owner[i] == owner[j] and j - i - 1 < min_hairpin:
                # same strand and no nick between: hairpin size constraint
                return False
            return True

        for pairs in noncrossing_matchings(seq, 0, N, can_pair):
            fs = faces(N, pairs, nick_after)
            kinds = [classify(f) for f in fs]
            conn = "disconnected" not in kinds
            if check:
                assert conn == connected_uf(N, pairs, owner), (order, pairs)
            if connected_only and not conn:
                continue
            e = 0
            for f, kd in zip(fs, kinds):
                e += loop_energy(kd, f, seq)
            lab = frozenset(((owner[i], idx[i]), (owner[j], idx[j])) for i, j in pairs)
            yield order, lab, e, kinds


def symmetry_orbits(strands, structures):
    """structures: iterable of (labelled frozenset, energy).  Groups them into orbits under permutations of
    identical strands.  Returns list of (representative, energy, orbit_size, stabiliser_size)."""
    from itertools import product
    c = len(strands)
    groups = {}
    for s, w in enumerate(strands):
        groups.setdefault(w, []).append(s)
    blocks = list(groups.values())
    perms = []
    for combo in product(*[list(permutations(b)) for b in blocks]):
        sigma = list(range(c))
        for b, img in zip(blocks, combo):
            for x, y in zip(b, img):
                sigma[x] = y
        perms.append(tuple(sigma))
    seen = {}
    allstructs = {}
    for lab, e in structures:
        allstructs[lab] = e
    out = []
    for lab, e in allstructs.items():
        if lab in seen:
            continue
        orbit = set()
        stab = 0
        for sg in perms:
            img = frozenset(tuple(sorted(((sg[a[0]], a[1]), (sg[b[0]], b[1])))) for a, b in lab)
            orbit.add(img)
            if img == norm(lab):
                stab += 1
        for o in orbit:
            seen[o] = True
        out.append((lab, e, len(orbit), stab))
    return out


def norm(lab):
    return frozenset(tuple(sorted(p)) for p in lab)
