#!/usr/bin/env python3
"""r20_validate.py -- validation of the enumerator r20_enum.py against a brute force over ALL
matchings, on tiny systems of synthetic strands (random words and small packing instances).

For every system:
  V1  the set {(order, S)} produced by enum_noncrossing equals the set obtained by listing all matchings
      S and testing, for every cyclic order, that no two chords cross (direct pairwise test);
  V2  the number of faces of every (order, S) is |S| + 1, and the links of the faces partition the links;
  V3  Fact 1 of the note: S connected (union-find; and, separately, depth-first search on the labelled
      graph) iff no face has two or more nicks; then exactly c faces have exactly one nick;
  V4  a connected S is non-crossing for exactly one cyclic order (the "representation theorem"), and
      that order is the one computed from S alone by successor_from_structure;
  V5  enum_noncrossing(prune_two_nicks=True) produces exactly the connected (order, S).
Every check is reported with its number of violations AND with the violations of a control that must fail:
  C1  V1 with the crossing test removed (reference = all matchings x all orders): fails on every system
      that has a crossing matching;
  C2  the face count |S|+1 applied to CROSSING matchings (Euler: a crossing matching has fewer faces);
  C3  Fact 1 with the threshold "no face has three or more nicks";
  C4  uniqueness of the cyclic order demanded of DISCONNECTED structures;
  C5  the pruned enumeration compared with ALL non-crossing structures instead of the connected ones.
Usage: python3 -I -B r20_validate.py [seed]
"""
import random
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import r20_enum as E  # noqa: E402


def check_system(strands, pairing):
    c = len(strands)
    v = {"V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0, "C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0}
    n_pairs_checked = 0
    brute = E.all_matchings(strands, pairing)
    orders = list(E.cyclic_orders(c))
    circles = {o: E.Circle(strands, o) for o in orders}
    # brute force: set of (order, key)
    ref = set()
    ref_nocrosstest = set()
    for key in brute:
        for o in orders:
            ref_nocrosstest.add((o, key))
            if E.noncrossing_on(circles[o], key):
                ref.add((o, key))
            else:
                # C2: faces of a crossing matching (partner list built by hand)
                circ = circles[o]
                pos = {b: p for p, b in enumerate(circ.base_id)}
                partner = [-1] * circ.N
                for a, b in key:
                    partner[pos[a]] = pos[b]
                    partner[pos[b]] = pos[a]
                if len(E.faces(circ, partner)) != len(key) + 1:
                    v["C2"] += 1
    got = []
    got_pruned = []
    info = {}
    for o in orders:
        circ = circles[o]

        def visit(partner, circ=circ, o=o):
            key = E.key_of(circ, partner)
            got.append((o, key))
            fs = E.faces(circ, partner)
            npairs = len(key)
            # V2
            if len(fs) != npairs + 1 or sum(sum(n for (_, n) in f[2]) for f in fs) != circ.N:
                v["V2"] += 1
            con = E.connected_uf(circ, partner)
            con2 = E.connected_graph(strands, key)
            maxnick = max(f[0] for f in fs)
            n_ext = sum(1 for f in fs if f[0] == 1)
            # V3
            if con != con2 or con != (maxnick <= 1) or (con and n_ext != c):
                v["V3"] += 1
            if con != (maxnick <= 2):
                v["C3"] += 1
            info[(o, key)] = con

        E.enum_noncrossing(circ, pairing, visit, prune_two_nicks=False)

        def visit2(partner, circ=circ, o=o):
            got_pruned.append((o, E.key_of(circ, partner)))

        E.enum_noncrossing(circ, pairing, visit2, prune_two_nicks=True)
    if len(got) != len(set(got)) or set(got) != ref:
        v["V1"] += 1
    if set(got) != ref_nocrosstest:
        v["C1"] += 1
    n_pairs_checked = len(ref)
    # V4
    by_key = {}
    for (o, key) in got:
        by_key.setdefault(key, []).append(o)
    n_conn = 0
    for key, os_ in by_key.items():
        if info[(os_[0], key)]:
            n_conn += 1
            if len(os_) != 1:
                v["V4"] += 1
                continue
            succ = E.successor_from_structure(strands, key)
            o = os_[0]
            want = [None] * c
            for j in range(c):
                want[o[j]] = o[(j + 1) % c]
            if succ != want:
                v["V4"] += 1
        else:
            if len(os_) != 1:
                v["C4"] += 1
    # V5
    conn_ref = set(x for x in got if info[x])
    if len(got_pruned) != len(set(got_pruned)) or set(got_pruned) != conn_ref:
        v["V5"] += 1
    if set(got_pruned) != set(got):
        v["C5"] += 1
    return v, len(brute), n_pairs_checked, n_conn


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261126
    rng = random.Random(seed)
    t0 = time.time()
    systems = []
    # random words over {A,C,G,T}: 2..4 strands, total length <= 9
    for _ in range(140):
        c = rng.randint(1, 4)
        lens = [rng.randint(1, 4) for _ in range(c)]
        while sum(lens) > 9:
            lens[rng.randrange(c)] = max(1, lens[rng.randrange(c)] - 1)
            if sum(lens) > 9 and all(x == 1 for x in lens):
                break
        alphabet = rng.choice(["ACGT", "CG", "CGA", "AT", "ACGT"])
        strands = ["".join(rng.choice(alphabet) for _ in range(L)) for L in lens]
        systems.append((strands, "WC"))
    # a few with wobble pairs allowed
    for _ in range(30):
        c = rng.randint(2, 3)
        strands = ["".join(rng.choice("GTCA") for _ in range(rng.randint(1, 3))) for _ in range(c)]
        systems.append((strands, "WC+wobble"))
    # small packing instances of the note:  template G^B (A G^B)^(m-1), items C^a
    for (a, m, B) in [((1, 1), 1, 2), ((2,), 1, 2), ((1, 1), 2, 1), ((2, 1), 1, 3), ((1, 1, 1), 1, 3),
                      ((2, 2), 2, 2), ((1, 1, 2), 2, 2), ((3, 1), 2, 2), ((1, 1, 1, 1), 2, 2)]:
        tmpl = "A".join(["G" * B] * m)
        systems.append(([tmpl] + ["C" * x for x in a], "WC"))
    # a few larger ones (total length 10..12)
    for (a, m, B) in [((2, 1, 1), 2, 2), ((2, 2, 1, 1), 2, 3), ((2, 2, 2), 2, 3), ((3, 2, 1), 2, 3)]:
        tmpl = "A".join(["G" * B] * m)
        systems.append(([tmpl] + ["C" * x for x in a], "WC"))
    for _ in range(6):
        c = rng.randint(2, 4)
        strands = ["".join(rng.choice("GCGCAT") for _ in range(rng.randint(2, 3))) for _ in range(c)]
        systems.append((strands, "WC"))
    tot = {"V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0, "C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0}
    n_sys = 0
    n_match = 0
    n_os = 0
    n_conn = 0
    for strands, rule in systems:
        pairing = E.WATSON_CRICK if rule == "WC" else E.WC_PLUS_WOBBLE
        v, nb, npc, nc = check_system(strands, pairing)
        for k in tot:
            tot[k] += v[k]
        n_sys += 1
        n_match += nb
        n_os += npc
        n_conn += nc
    print("r20_validate.py  seed", seed)
    print("systems checked:", n_sys, " matchings (all, crossing or not):", n_match,
          " non-crossing (order, structure) pairs:", n_os, " connected labelled structures:", n_conn)
    for k in ("V1", "V2", "V3", "V4", "V5"):
        print("  check   %s violations: %d" % (k, tot[k]))
    for k in ("C1", "C2", "C3", "C4", "C5"):
        print("  control %s violations: %d   (must be > 0)" % (k, tot[k]))
    print("elapsed %.1f s" % (time.time() - t0))
    ok = not any(tot[k] for k in ("V1", "V2", "V3", "V4", "V5")) and all(tot[k] > 0 for k in ("C1", "C2", "C3", "C4", "C5"))
    print("RESULT:", "PASS (all checks 0 violations, all controls fail as they must)" if ok else "FAIL")
    print("END r20_validate.py")


if __name__ == "__main__":
    main()
