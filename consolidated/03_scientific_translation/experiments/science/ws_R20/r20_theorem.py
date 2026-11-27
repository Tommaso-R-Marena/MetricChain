#!/usr/bin/env python3
"""r20_theorem.py -- workstream R20: replication of Theorems 1 and 3 of the note under review on small
synthetic packing instances, with my own enumerator (r20_enum.py), plus controls that must fail.

For an instance (a_1..a_n ; m ; B) with sum a_i = m B the system is
    template  G^B (A G^B)^(m-1)      items  C^(a_i),
and M = m B - n.  ALL connected unpseudoknotted structures are enumerated over ALL (n)! cyclic orders
(labelled strands), each is decomposed into faces, and for every loop-energy function in the list
below the following statements are tested (sigma = energy of the GG/CC stack, exterior loops 0):

  S1  packing solvable     =>  min energy = sigma*M                         (Theorem 1.1)
  S2  packing not solvable =>  min energy >= sigma*(M-1)                    (Theorem 1.2)
  S3  {structures of energy sigma*M} = {tiling structures}                  (Theorem 1, last statement)
  S4  number of labelled structures of energy sigma*M = Til(a,m,B)          (Theorem 3.1), Til by brute force
  S5  number of orbits under permutations of equal items = Til / prod mu_s! (Theorem 3.2), orbits by
      brute-force canonicalisation
and, independently of the energy function,
  U1  st(S) <= M for every structure; max st = M iff solvable               (step (c), (d))
  U2  R(S) = 1 for every structure                                          (step (b))
  U3  the cyclic order of S computed from S alone equals the order under which it was generated
      (uniqueness of the order; representation theorem)
  U4  every face of a connected structure has at most one nick and exactly c faces have one (Fact 1; the
      enumeration itself prunes on this, so U4 only confirms the bookkeeping; the equivalence with
      connectedness is tested in r20_validate.py and, with --crosscheck, here by union-find on the
      unpruned enumeration)
  U5  the group of permutations of equal items acts freely on ALL connected structures (so that the
      number of physical structures with k stacks is the labelled number / prod mu_s!)  [--orbits]

The association term (c-1)*dG_assoc and the symmetry term kT ln R(S) are the same for all structures of
one instance (U2), so they are left out of the comparison of energies.

Loop-energy functions.  Class "H": satisfy (H0)-(H2) of the note.  Class "GEN": outside (H0)-(H2) but
inside a weaker hypothesis proposed by this review; the prediction tested is the reviewer's, stated in
the model's entry.  Class "CTRL": controls for which the note's Theorem 1 (S1-S3, read literally with
E* = sigma*M) must FAIL on at least one instance.

Usage:  python3 -I -B r20_theorem.py <instance-set> [--crosscheck] [--orbits]
"""
import sys
import os
import time
import zlib
from itertools import permutations, product
from math import factorial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r20_enum as E  # noqa: E402


# ----------------------------------------------------------------------------------------------
# the packing side, by brute force (independent of the enumerator)
# ----------------------------------------------------------------------------------------------
def arrangements(a, m, B):
    """All ways to arrange the labelled items 0..n-1 into m ordered rows, each row an ordered sequence
    of items of total length exactly B.  Returned as a list of tuples of rows (each row a tuple)."""
    n = len(a)
    out = []
    rows = []

    def fill(t, used, row, room):
        if room == 0:
            rows.append(tuple(row))
            if t == m - 1:
                if all(used):
                    out.append(tuple(rows))
            else:
                fill(t + 1, used, [], B)
            rows.pop()
            return
        for i in range(n):
            if not used[i] and a[i] <= room:
                used[i] = True
                row.append(i)
                fill(t, used, row, room - a[i])
                row.pop()
                used[i] = False

    fill(0, [False] * n, [], B)
    return out


def solvable_bruteforce(a, m, B):
    """Exact bin packing by brute force over all maps beta: items -> bins (independent of `arrangements`)."""
    n = len(a)
    for beta in product(range(m), repeat=n):
        load = [0] * m
        for i, t in enumerate(beta):
            load[t] += a[i]
        if all(x == B for x in load):
            return True
    return False


def count_partitions(a, m, B):
    """L(a,m,B): the number of partitions of the index set into m classes of total size B each
    (unordered classes), by brute force over beta with a canonical-labelling filter."""
    n = len(a)
    cnt = 0
    for beta in product(range(m), repeat=n):
        # canonical: bins are numbered in order of first appearance
        seen = -1
        ok = True
        for t in beta:
            if t > seen + 1:
                ok = False
                break
            if t == seen + 1:
                seen = t
        if not ok:
            continue
        load = [0] * m
        for i, t in enumerate(beta):
            load[t] += a[i]
        if all(x == B for x in load):
            cnt += 1
    return cnt


def tiling_key(a, m, B, rows):
    """The labelled structure of an arrangement: in block t the items of rows[t] are laid along the
    template 5'->3' in the given order; item base j (0-based, 5'->3') of an item occupying template
    positions p..p+len-1 is paired with p+len-1-j (antiparallel)."""
    offs = [m * B + m - 1]
    for x in a[:-1]:
        offs.append(offs[-1] + x)
    key = []
    for t in range(m):
        p = t * (B + 1)
        for i in rows[t]:
            L = a[i]
            for j in range(L):
                key.append((p + L - 1 - j, offs[i] + j))
            p += L
    key.sort()
    return tuple(key)


# ----------------------------------------------------------------------------------------------
# face descriptors and loop-energy functions
# ----------------------------------------------------------------------------------------------
def descriptor(circ, face):
    """(kind, segments) with every segment written as letters joined by '|' (covalent bond) or '/' (nick),
    e.g. a stack is ('stack', ('C|C', 'G|G')); segments are rotated to the lexicographically least rotation."""
    nn, k, segs = face
    N = circ.N
    letter = circ.letter
    nick = circ.nick_after
    ss = []
    for (p, nl) in segs:
        parts = [letter[p]]
        q = p
        for _ in range(nl):
            parts.append("/" if nick[q] else "|")
            q = q + 1 if q + 1 < N else 0
            parts.append(letter[q])
        ss.append("".join(parts))
    r = len(ss)
    best = min(tuple(ss[i:] + ss[:i]) for i in range(r))
    return (E.kind_of(face), best)


def n_item_bonds(d):
    """b(f): the number of covalent bonds between two C's (= bonds of items) on the boundary of the face."""
    tot = 0
    for s in d[1]:
        for i in range(1, len(s) - 1, 2):
            if s[i] == "|" and s[i - 1] == "C" and s[i + 1] == "C":
                tot += 1
    return tot


def n_unpaired(seg):
    return (len(seg) - 1) // 2 - 1


def is_flush_nick(d):
    """exterior loop with two chords and no unpaired base: one covalent bond and one nick ('coaxial stack')."""
    return d[0] == "exterior" and len(d[1]) == 2 and all(len(s) == 3 for s in d[1])


def is_A_bulge(d):
    """the bulge loop in which an item crosses a separator: template side G|A|G, item side C|C."""
    return d[0] == "bulge" and sorted(d[1]) == ["C|C", "G|A|G"]


def n_dangles(d):
    """number of unpaired bases of an exterior loop that are covalently adjacent to a paired base of the
    loop (a base flanked by two pairs is counted once): the 'some dangles' convention with equal energies."""
    tot = 0
    for s in d[1]:
        r = (len(s) - 1) // 2          # number of links
        if r < 2:
            continue
        first_cov = s[1] == "|"
        last_cov = s[-2] == "|"
        if r == 2:
            tot += 1 if (first_cov or last_cov) else 0
        else:
            tot += (1 if first_cov else 0) + (1 if last_cov else 0)
    return tot


def hashval(d, seed, lo, hi):
    h = zlib.crc32((repr(d) + "#" + str(seed)).encode())
    return lo + h % (hi - lo + 1)


NONSTACK = ("bulge", "interior", "multi")


def make_models():
    """name -> dict(klass, sigma, f, estar(M,n,m,B), gap, text)."""
    md = {}

    def add(name, klass, sigma, f, estar, gap, text):
        md[name] = dict(klass=klass, sigma=sigma, f=f, estar=estar, gap=gap, text=text)

    std = lambda sigma: (lambda M, n, m, B: sigma * M)  # noqa: E731

    # ---- class H: inside (H0)-(H2) ----
    add("H1_stack_only", "H", -1,
        lambda d: -1 if d[0] == "stack" else 0, std(-1), 1,
        "stack -1, everything else 0")
    add("H2_penalties", "H", -3,
        lambda d: -3 if d[0] == "stack" else
        (2 + sum(n_unpaired(s) for s in d[1]) if d[0] == "bulge" else
         (3 + sum(n_unpaired(s) for s in d[1]) if d[0] == "interior" else
          (4 + len(d[1]) + sum(n_unpaired(s) for s in d[1]) if d[0] == "multi" else 0))),
        std(-3), 3, "stack -3; bulge 2+u; interior 3+u; multiloop 4+k+u; exterior 0")
    add("H3_hash_0to9", "H", -5,
        lambda d: -5 if d[0] == "stack" else (hashval(d, 1, 0, 9) if d[0] in NONSTACK else 0),
        std(-5), 5, "stack -5; bulge/interior/multi: pseudo-random integer in 0..9 (crc32 of the loop, seed 1)")
    add("H4_hash_0to3", "H", -2,
        lambda d: -2 if d[0] == "stack" else (hashval(d, 2, 0, 3) if d[0] in NONSTACK else 0),
        std(-2), 2, "stack -2; bulge/interior/multi: pseudo-random integer in 0..3 (seed 2)")
    add("H5_boundary_zero", "H", -7,
        lambda d: -7 if d[0] == "stack" else 0, std(-7), 7,
        "stack -7; bulge/interior/multi exactly 0 (boundary of H2)")

    # ---- class GEN: reviewer's weaker hypotheses ----
    add("GEN1_H2star_delta1", "GEN", -4,
        lambda d: -4 if d[0] == "stack" else (-4 * n_item_bonds(d) + 1 if d[0] in NONSTACK else 0),
        std(-4), 1,
        "(H2*) with delta=1: every bulge/interior/multiloop has energy sigma*b(f)+1 < 0 (b = item bonds on it); "
        "prediction: S1, S3-S5 unchanged, S2 with gap min(|sigma|,delta)=1")
    add("GEN2_H2star_mixed", "GEN", -6,
        lambda d: -6 if d[0] == "stack" else
        ((-6 * (n_item_bonds(d) - 1) if n_item_bonds(d) >= 2 else -1) if d[0] == "bulge" else
         (-6 * n_item_bonds(d) + 3 if d[0] in ("interior", "multi") else 0)),
        std(-6), 3,
        "bulge with b>=2 item bonds: sigma*(b-1); bulge with b=1: -1; interior/multi: sigma*b+3; prediction gap 3")
    add("GEN3_coax_weaker", "GEN", -2,
        lambda d: -2 if d[0] == "stack" else (-1 if is_flush_nick(d) else 0),
        lambda M, n, m, B: -2 * M - 1 * (n - m), 1,
        "stack -2; flush nick (coaxial stack) kappa=-1 with sigma<kappa<=0; other loops 0; prediction: "
        "E* = sigma*M + kappa*(n-m), gap kappa-sigma = 1, minimisers = tilings")
    add("GEN4_coax_equal_bulge_pos", "GEN", -2,
        lambda d: -2 if (d[0] == "stack" or is_flush_nick(d)) else (1 if d[0] in NONSTACK else 0),
        lambda M, n, m, B: -2 * m * (B - 1), 1,
        "stack -2; flush nick -2 (coaxial stack as strong as a stack); bulge/interior/multi +1; prediction "
        "(for B>=2): E* = sigma*m*(B-1), gap min(|sigma|,1) = 1, minimisers = tilings")
    add("GEN5_dangles_small", "GEN", -3,
        lambda d: -3 if d[0] == "stack" else (-1 * n_dangles(d) if d[0] == "exterior" else 0),
        lambda M, n, m, B: -3 * M - 1 * (m - 1), 1,
        "stack -3; exterior loops: -1 per unpaired base covalently next to a pair ('some dangles'); other 0; "
        "prediction (|sigma| > D_G + D_C = 2): E* = sigma*M + d*(m-1), gap |sigma|-2 = 1, minimisers = tilings")
    add("GEN6_exterior_constant", "GEN", -3,
        lambda d: -3 if d[0] == "stack" else (-2 if d[0] == "exterior" else 0),
        lambda M, n, m, B, : -3 * M - 2 * 0, 3,
        "stack -3; EVERY exterior loop -2 (a constant): energies shift by -2c for all structures; the entry "
        "E* omits the shift on purpose, see the special handling (shift = -2*(n+1))")

    add("GEN7_coax_equal_Abulge_only", "GEN", -2,
        lambda d: -2 if (d[0] == "stack" or is_flush_nick(d)) else (1 if is_A_bulge(d) else 0),
        lambda M, n, m, B: -2 * m * (B - 1), 1,
        "as GEN4 but ONLY the bulge 'G A G over C C' (an item crossing a separator) costs +1, every other "
        "bulge/interior/multiloop 0; same prediction as GEN4 (for B>=2)")

    # ---- class CTRL: the note's Theorem 1 must fail ----
    add("CTRL1_H0_coax_equal", "CTRL", -1,
        lambda d: -1 if (d[0] == "stack" or is_flush_nick(d)) else 0, std(-1), 1,
        "(H0) dropped: a flush nick ('stack across a nick') gets sigma=-1; bulge/interior/multi 0")
    add("CTRL2_H2_bulge_as_stack", "CTRL", -1,
        lambda d: -1 if d[0] in ("stack", "bulge") else 0, std(-1), 1,
        "(H2) dropped: every bulge gets sigma=-1")
    add("CTRL3_H1_sigma_zero", "CTRL", 0,
        lambda d: 0, std(0), 0,
        "(H1) dropped: sigma = 0 (all loops 0)")
    add("CTRL4_H2star_delta0", "CTRL", -4,
        lambda d: -4 if d[0] == "stack" else (-4 * n_item_bonds(d) if d[0] in NONSTACK else 0), std(-4), 4,
        "(H2*) at delta=0: bulge/interior/multi get sigma*b(f)")
    add("CTRL5_dangles_large", "CTRL", -3,
        lambda d: -3 if d[0] == "stack" else (-2 * n_dangles(d) if d[0] == "exterior" else 0),
        lambda M, n, m, B: -3 * M - 2 * (m - 1), 1,
        "(H0) dropped: 'dangles' of -2 per base with |sigma|=3 < D_G+D_C=4; tested against the GEN5 "
        "prediction E* = sigma*M + d*(m-1) (minimisers = tilings), which must fail")
    return md


# ----------------------------------------------------------------------------------------------
INSTANCE_SETS = {
    # (a, m, B)
    "tiny": [((2, 1), 1, 3), ((2, 2), 2, 2), ((1, 1, 2), 2, 2), ((3, 1), 2, 2), ((2, 2, 2), 2, 3),
             ((3, 2, 1), 2, 3), ((4, 2), 2, 3)],
    "small": [
        # m = 1 (always solvable)
        ((3,), 1, 3), ((2, 1), 1, 3), ((1, 1, 1), 1, 3), ((2, 2), 1, 4), ((2, 1, 1), 1, 4),
        # m = 2, B = 2
        ((2, 2), 2, 2), ((1, 1, 2), 2, 2), ((1, 1, 1, 1), 2, 2), ((3, 1), 2, 2), ((4,), 2, 2),
        # m = 2, B = 3
        ((3, 3), 2, 3), ((2, 2, 2), 2, 3), ((3, 2, 1), 2, 3), ((2, 2, 1, 1), 2, 3), ((4, 2), 2, 3),
        ((4, 1, 1), 2, 3), ((5, 1), 2, 3), ((3, 1, 1, 1), 2, 3), ((2, 1, 1, 1, 1), 2, 3), ((6,), 2, 3),
        # m = 2, B = 4
        ((4, 4), 2, 4), ((3, 3, 2), 2, 4), ((4, 2, 2), 2, 4), ((3, 3, 1, 1), 2, 4), ((2, 2, 2, 2), 2, 4),
        ((3, 2, 2, 1), 2, 4), ((4, 3, 1), 2, 4), ((5, 3), 2, 4), ((5, 2, 1), 2, 4), ((6, 1, 1), 2, 4),
        # m = 3, B = 2
        ((2, 2, 2), 3, 2), ((2, 2, 1, 1), 3, 2), ((3, 3), 3, 2), ((3, 2, 1), 3, 2), ((4, 1, 1), 3, 2),
        ((2, 1, 1, 1, 1), 3, 2),
        # m = 3, B = 3
        ((3, 3, 3), 3, 3), ((4, 4, 1), 3, 3), ((3, 2, 2, 2), 3, 3), ((3, 3, 2, 1), 3, 3), ((4, 3, 2), 3, 3),
        ((5, 2, 2), 3, 3), ((2, 2, 2, 2, 1), 3, 3),
    ],
    "medium": [
        ((3, 3, 2, 2), 2, 5), ((4, 4, 2), 2, 5), ((4, 3, 3), 2, 5), ((4, 4, 1, 1), 2, 5), ((5, 3, 2), 2, 5),
        ((3, 3, 3, 1), 2, 5), ((4, 2, 2, 2), 2, 5), ((2, 2, 2, 2, 2), 2, 5), ((3, 2, 2, 2, 1), 2, 5),
        ((2, 2, 2, 1, 1, 1), 3, 3), ((3, 3, 1, 1, 1), 3, 3), ((2, 2, 2, 2, 2, 2), 3, 4), ((3, 3, 3, 3), 3, 4),
        ((4, 4, 2, 2), 3, 4), ((3, 3, 2, 2, 2), 3, 4), ((3, 3, 3, 2, 1), 3, 4),
        ((2, 2, 2, 2, 2, 2), 2, 6), ((3, 3, 3, 3), 2, 6), ((4, 4, 4), 2, 6), ((5, 5, 2), 2, 6), ((4, 3, 3, 2), 2, 6),
    ],
    # batches of the feasible part of "medium" (each batch < 20 min; sizes from logs/count_medium_cap45.log)
    "medium_a": [((3, 3, 2, 2), 2, 5), ((4, 4, 2), 2, 5), ((4, 3, 3), 2, 5), ((4, 4, 1, 1), 2, 5), ((5, 3, 2), 2, 5)],
    "medium_b": [((3, 3, 3, 1), 2, 5), ((4, 2, 2, 2), 2, 5), ((2, 2, 2, 1, 1, 1), 3, 3), ((3, 3, 1, 1, 1), 3, 3)],
    "medium_c": [((2, 2, 2, 2, 2), 2, 5)],
    "medium_d": [((3, 2, 2, 2, 1), 2, 5)],
    # degenerate shapes: B = 1 (no G-G bond), a single item, all items of length 1, items longer than a block
    "edge": [((1,), 1, 1), ((2,), 1, 2), ((1, 1), 2, 1), ((2,), 2, 1), ((1, 1, 1), 3, 1), ((2, 1), 3, 1), ((3,), 3, 1),
             ((1, 1, 1, 1), 4, 1), ((2, 1, 1), 4, 1), ((5,), 1, 5), ((1, 1, 1, 1, 1), 1, 5), ((6,), 3, 2),
             ((1, 1, 1, 1, 1, 1), 3, 2), ((8,), 2, 4)],
    # a case of the reviewed division's big test that is not in my other sets
    "their_extra": [((3, 2, 2, 1, 1), 3, 3)],
    # larger instances, only with --reduce-orders
    "large_reduced_a": [((2, 2, 2, 2, 2, 2), 2, 6), ((2, 2, 2, 2, 2, 2), 3, 4), ((3, 3, 3, 3), 3, 4)],
    "large_reduced_b": [((3, 3, 3, 3), 2, 6), ((4, 4, 4), 2, 6)],
    # 3-PARTITION-shaped (B/4 < a_i < B/2, n = 3m) and 4-PARTITION-shaped (B/5 < a_i < B/3, n = 4m)
    "partition_shaped": [
        ((2, 2, 2, 2, 2, 2), 2, 6),          # 3-PARTITION shape, B=6
        ((3, 2, 2, 3, 2, 2), 2, 7),          # 3-PARTITION shape, B=7 (solvable)
        ((3, 3, 3, 2, 2, 1), 2, 7),          # not 3-PARTITION shaped (a=1), kept as a no/yes mix
        ((3, 3, 3, 3, 1, 1), 2, 7),
    ],
}


def canonical_orders(a):
    """One cyclic order per class under permutations of equal items: the orders in which items of equal
    length appear in increasing index order.  Every other order is the image of exactly one of these under a
    relabelling of equal items, and relabelling is a bijection on labelled structures that preserves all
    loop types; so labelled counts are prod(mu_s!) times the counts over these orders (the free action that
    makes this exact is checked directly by U5 in full enumerations)."""
    n = len(a)
    for order in E.cyclic_orders(n + 1):
        last = {}
        ok = True
        for t in order[1:]:
            x = a[t - 1]
            if x in last and last[x] > t:
                ok = False
                break
            last[x] = t
        if ok:
            yield order


def run_instance(a, m, B, models, crosscheck=False, orbits=False, reduce_orders=False, out=sys.stdout):
    n = len(a)
    assert sum(a) == m * B and all(x >= 1 for x in a)
    c = n + 1
    M = m * B - n
    template = "A".join(["G" * B] * m)
    strands = [template] + ["C" * x for x in a]
    t0 = time.time()
    arr = arrangements(a, m, B)
    Til = len(arr)
    solv = solvable_bruteforce(a, m, B)
    assert solv == (Til > 0)
    Lpart = count_partitions(a, m, B)
    tilings = set(tiling_key(a, m, B, rows) for rows in arr)
    assert len(tilings) == Til
    mu = {}
    for x in a:
        mu[x] = mu.get(x, 0) + 1
    prod_mu = 1
    for x in mu.values():
        prod_mu *= factorial(x)
    # group of permutations of equal items, as permutations of base identifiers
    offs = [m * B + m - 1]
    for x in a[:-1]:
        offs.append(offs[-1] + x)
    groups = {}
    for i, x in enumerate(a):
        groups.setdefault(x, []).append(i)
    glist = [list(permutations(g)) for g in groups.values()]
    gkeys = list(groups.values())
    perms = []
    for combo in product(*glist):
        pm = list(range(m * B + m - 1 + sum(a)))
        ident = True
        for g, img in zip(gkeys, combo):
            for i, j in zip(g, img):
                if i != j:
                    ident = False
                for q in range(a[i]):
                    pm[offs[i] + q] = offs[j] + q
        perms.append((ident, pm))
    assert len(perms) == prod_mu

    def canon(key):
        best = key
        for ident, pm in perms:
            if ident:
                continue
            k2 = tuple(sorted((pm[x] if pm[x] < pm[y] else pm[y], pm[y] if pm[x] < pm[y] else pm[x]) for x, y in key))
            if k2 < best:
                best = k2
        return best

    names = list(models)
    fl = [models[nm]["f"] for nm in names]
    cache = [dict() for _ in names]
    estar = []
    for nm in names:
        e = models[nm]["estar"](M, n, m, B)
        if nm == "GEN6_exterior_constant":
            e += -2 * c
        estar.append(e)
    nmod = len(names)
    emin = [None] * nmod
    nmin = [0] * nmod
    n_at_estar = [0] * nmod
    n_at_estar_nontiling = [0] * nmod
    n_tiling_off_estar = [0] * nmod
    orb_at_estar = [set() for _ in names]
    stat = dict(total=0, st_hist={}, u1=0, u2=0, u3=0, u4=0, u5=0, tilings_seen=0, max_st=-1)
    all_keys = set() if orbits else None
    dcache = {}
    want_cache = {}

    order_list = list(canonical_orders(a)) if reduce_orders else list(E.cyclic_orders(c))
    mult = prod_mu if reduce_orders else 1
    for order in order_list:
        circ = E.Circle(strands, order)
        want = [None] * c
        for j in range(c):
            want[order[j]] = order[(j + 1) % c]

        def visit(partner, circ=circ, want=want):
            stat["total"] += 1
            fs = E.faces(circ, partner)
            key = E.key_of(circ, partner)
            ds = []
            st = 0
            n_ext = 0
            bad = False
            for f in fs:
                if f[0] >= 2:
                    bad = True
                if f[0] == 1:
                    n_ext += 1
                d = descriptor(circ, f)
                ds.append(d)
                if d[0] == "stack":
                    st += 1
            if bad or n_ext != c or len(fs) != len(key) + 1:
                stat["u4"] += 1
            stat["st_hist"][st] = stat["st_hist"].get(st, 0) + 1
            if st > M:
                stat["u1"] += 1
            if st > stat["max_st"]:
                stat["max_st"] = st
            if E.symmetry_number(circ, partner) != 1:
                stat["u2"] += 1
            if E.successor_from_structure(strands, key) != want:
                stat["u3"] += 1
            is_til = key in tilings
            ck = None
            if is_til:
                stat["tilings_seen"] += 1
                ck = canon(key)
            if all_keys is not None:
                if key in all_keys:
                    stat["u3"] += 1       # the same labelled structure under two orders
                all_keys.add(key)
            for i in range(nmod):
                f_ = fl[i]
                ch = cache[i]
                e = 0
                for d in ds:
                    v = ch.get(d)
                    if v is None:
                        v = f_(d)
                        ch[d] = v
                    e += v
                if emin[i] is None or e < emin[i]:
                    emin[i] = e
                    nmin[i] = 1
                elif e == emin[i]:
                    nmin[i] += 1
                if e == estar[i]:
                    n_at_estar[i] += 1
                    if not is_til:
                        n_at_estar_nontiling[i] += 1
                    else:
                        orb_at_estar[i].add(ck)
                elif is_til:
                    n_tiling_off_estar[i] += 1

        E.enum_noncrossing(circ, E.WATSON_CRICK, visit, prune_two_nicks=True)

    cross = None
    if crosscheck:
        # unpruned enumeration + union-find: the number of connected structures must agree
        cnt = [0, 0]
        for order in E.cyclic_orders(c):
            circ = E.Circle(strands, order)

            def visit2(partner, circ=circ):
                cnt[1] += 1
                if E.connected_uf(circ, partner):
                    cnt[0] += 1

            E.enum_noncrossing(circ, E.WATSON_CRICK, visit2, prune_two_nicks=False)
        cross = (cnt[0], cnt[1])

    if all_keys is not None:
        # U5: free action on all connected structures: every orbit has prod_mu elements
        seen = set()
        norb = 0
        for key in all_keys:
            if key in seen:
                continue
            orb = set()
            for ident, pm in perms:
                k2 = tuple(sorted((pm[x] if pm[x] < pm[y] else pm[y], pm[y] if pm[x] < pm[y] else pm[x]) for x, y in key))
                orb.add(k2)
            if len(orb) != prod_mu or not orb <= all_keys:
                stat["u5"] += 1
            seen |= orb
            norb += 1
        stat["n_orbits"] = norb

    # ---- report ----
    w = out.write
    w("instance a=%s m=%d B=%d : n=%d c=%d N=%d M=%d  solvable=%s  Til=%d  L=%d  prod(mu_s!)=%d  Til/prod=%s\n" % (
        list(a), m, B, n, c, len(template) + sum(a), M, solv, Til, Lpart, prod_mu,
        (str(Til // prod_mu) if Til % prod_mu == 0 else "NOT AN INTEGER")))
    if reduce_orders:
        w("  [orders reduced by the symmetry of equal items: %d of %d orders enumerated (%d structures visited); "
          "labelled counts below = visited counts x %d]\n" % (len(order_list), factorial(n), stat["total"], mult))
    w("  connected unpseudoknotted labelled structures: %d   max st = %d   (orders: %d)   time %.1f s\n" % (
        stat["total"] * mult, stat["max_st"], factorial(n), time.time() - t0))
    hist = stat["st_hist"]
    w("  labelled count by number of stacks k: %s\n" % " ".join("%d:%d" % (k, hist[k] * mult) for k in sorted(hist)))
    u1 = stat["u1"] + (0 if (stat["max_st"] == M) == solv else 1)
    w("  U1 (st<=M, max st=M iff solvable) violations: %d   U2 (R=1): %d   U3 (unique order): %d   U4 (faces/nicks): %d"
      % (u1, stat["u2"], stat["u3"], stat["u4"]))
    if all_keys is not None:
        w("   U5 (free action; orbits=%d): %d" % (stat["n_orbits"], stat["u5"]))
        if stat["n_orbits"] * prod_mu != stat["total"]:
            w("   U5-count MISMATCH")
            stat["u5"] += 1
    w("\n")
    if stat["tilings_seen"] * mult != Til:
        w("  !! tilings seen in the enumeration: %d, expected %d\n" % (stat["tilings_seen"], Til))
    if cross is not None:
        ok = cross[0] == stat["total"]
        w("  crosscheck (unpruned enumeration %d structures, connected by union-find %d): %s\n" % (
            cross[1], cross[0], "agrees" if ok else "DISAGREES"))
        if not ok:
            stat["u4"] += 1
    res = {}
    for i, nm in enumerate(names):
        md = models[nm]
        sig = md["sigma"]
        v = dict(S1=0, S2=0, S3=0, S4=0, S5=0)
        if solv and emin[i] != estar[i]:
            v["S1"] = 1
        if (not solv) and not (emin[i] >= estar[i] + md["gap"]):
            v["S2"] = 1
        if n_at_estar_nontiling[i] or n_tiling_off_estar[i]:
            v["S3"] = 1
        if n_at_estar[i] * mult != Til:
            v["S4"] = 1
        if Til % prod_mu != 0 or len(orb_at_estar[i]) != Til // prod_mu:
            v["S5"] = 1
        # the decision the reduction makes: "min energy <= E*"  <=>  solvable ?
        decision_wrong = int((emin[i] <= estar[i]) != solv)
        if nm.startswith(("GEN4", "GEN7")) and B == 1:
            # the reviewer's statement for 'coaxial stack as strong as a stack' is made for B >= 2 only
            # (for B = 1 the template has no G-G bond, nothing is rewarded and the statement is void)
            v = dict(S1=0, S2=0, S3=0, S4=0, S5=0)
            decision_wrong = 0
            w("  %-28s [%s] not applicable for B = 1 (statement made for B >= 2)\n" % (nm, md["klass"]))
            res[nm] = (v, decision_wrong, emin[i], nmin[i] * mult, estar[i])
            continue
        res[nm] = (v, decision_wrong, emin[i], nmin[i] * mult, estar[i])
        w("  %-28s [%s] sigma=%3d  E*=%4d  min=%4d (#min=%d)  #at E*=%d (non-tiling %d; tilings off E* %d; orbits %d)"
          "  viol S1..S5 = %d %d %d %d %d  decision %s\n" % (
              nm, md["klass"], sig, estar[i], emin[i], nmin[i] * mult, n_at_estar[i] * mult,
              n_at_estar_nontiling[i] * mult,
              n_tiling_off_estar[i] * mult, len(orb_at_estar[i]), v["S1"], v["S2"], v["S3"], v["S4"], v["S5"],
              "WRONG" if decision_wrong else "right"))
    out.flush()
    ustat = dict(U1=u1, U2=stat["u2"], U3=stat["u3"], U4=stat["u4"], U5=stat["u5"])
    return res, ustat, stat["total"] * mult, solv


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    setname = args[0] if args else "tiny"
    crosscheck = "--crosscheck" in sys.argv
    orbits = "--orbits" in sys.argv
    reduce_orders = "--reduce-orders" in sys.argv
    assert not (reduce_orders and (orbits or crosscheck)), "--reduce-orders excludes --orbits and --crosscheck"
    models = make_models()
    print("r20_theorem.py  instance set '%s'  crosscheck=%s orbits=%s reduce_orders=%s" % (
        setname, crosscheck, orbits, reduce_orders))
    print("loop-energy functions:")
    for nm, md in models.items():
        print("  %-28s [%s] %s" % (nm, md["klass"], md["text"]))
    print()
    t0 = time.time()
    tot = {nm: dict(S1=0, S2=0, S3=0, S4=0, S5=0, dec=0) for nm in models}
    utot = dict(U1=0, U2=0, U3=0, U4=0, U5=0)
    n_inst = 0
    n_yes = 0
    n_struct = 0
    for (a, m, B) in INSTANCE_SETS[setname]:
        res, ustat, total, solv = run_instance(a, m, B, models, crosscheck, orbits, reduce_orders)
        n_inst += 1
        n_yes += int(solv)
        n_struct += total
        for k in utot:
            utot[k] += ustat[k]
        for nm in models:
            v, dw = res[nm][0], res[nm][1]
            for k in v:
                tot[nm][k] += v[k]
            tot[nm]["dec"] += dw
    print()
    print("SUMMARY  set '%s': %d instances (%d solvable, %d not), %d connected labelled structures enumerated, %.1f s"
          % (setname, n_inst, n_yes, n_inst - n_yes, n_struct, time.time() - t0))
    print("  model-independent checks, violations:  " + "  ".join("%s=%d" % (k, utot[k]) for k in sorted(utot)))
    print("  per loop-energy function: number of instances violating S1..S5 and number of wrong decisions")
    ok = not any(utot.values())
    for nm, md in models.items():
        t = tot[nm]
        nviol = t["S1"] + t["S2"] + t["S3"] + t["S4"] + t["S5"]
        if md["klass"] in ("H", "GEN"):
            verdict = "ok (0 violations)" if nviol == 0 and t["dec"] == 0 else "VIOLATED"
            ok = ok and nviol == 0 and t["dec"] == 0
        else:
            verdict = "control fails as it must" if nviol > 0 else "CONTROL DID NOT FAIL"
            ok = ok and nviol > 0
        print("  %-28s [%-4s] S1=%d S2=%d S3=%d S4=%d S5=%d wrong decisions=%d   -> %s" % (
            nm, md["klass"], t["S1"], t["S2"], t["S3"], t["S4"], t["S5"], t["dec"], verdict))
    print("RESULT:", "PASS (classes H and GEN: 0 violations; every control violated)" if ok else "FAIL")
    print("END r20_theorem.py")


if __name__ == "__main__":
    main()
