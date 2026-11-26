"""Referee's check of the numbers in the paragraph 'What "sharp" does and does not mean' (section 7 of the
NANUQ note): six-point tree-generated systems, which of them fail and how, and blow-ups.
Own code: split systems as sets of frozenset pairs; metric from nanuq_core.nanuq_metric (definition)."""
import itertools, sys, time
from fractions import Fraction
from collections import Counter, defaultdict
from nanuq_core import nanuq_metric, circ_splits, alpha, quartets_from_splits

N = 6
X = list(range(1, N + 1))
FULL = frozenset(X)


def interval_split(i, j, order):
    n = len(order)
    U = frozenset(order[k % n] for k in range(i, j))
    return frozenset([U, frozenset(order) - U])


def nontrivial_circular_splits(order):
    n = len(order)
    out = set()
    for i in range(n):
        for L in range(2, n - 1):
            out.add(interval_split(i, i + L, order))
    return out


def compatible(s, t):
    a, b = tuple(s)
    c, d = tuple(t)
    return not (a & c) or not (a & d) or not (b & c) or not (b & d)


def trivial(order):
    return {frozenset([frozenset([x]), frozenset(order) - {x}]) for x in order}


def circular_trees(order):
    NT = sorted(nontrivial_circular_splits(order), key=lambda s: sorted(map(sorted, s)))
    n = len(order)
    out = []
    for comb in itertools.combinations(NT, n - 3):
        if all(compatible(s, t) for s, t in itertools.combinations(comb, 2)):
            out.append(frozenset(comb) | frozenset(trivial(order)))
    return out


def weight_classes(S, order):
    """returns (kalmanson, exact_support, min alpha, list of (split, alpha, in S))"""
    d = nanuq_metric(S, order)
    rows = []
    for i, j, sp in circ_splits(order):
        a = alpha(d, order, i, j)
        rows.append((sp, a, sp in S))
    kal = all(a >= 0 for _, a, _ in rows)
    exact = all((a > 0) == ins for _, a, ins in rows)
    return kal, exact, min(a for _, a, _ in rows), rows


def wq(Q, a, b, c, d):
    """w(ab|cd) in {1, 1/2, 0}"""
    qs = Q[frozenset([a, b, c, d])]
    me = frozenset([frozenset([a, b]), frozenset([c, d])])
    if me in qs:
        return Fraction(1, len(qs))
    return Fraction(0)


def six_locally_good(S, order):
    """every dihedral labelling y1..y6 (u1,z,w,up,v1,vq): Phi6 >= 0 with equality if y1 y4 | y5 y6 not displayed"""
    Q = quartets_from_splits(S, order)
    n = len(order)
    assert n == 6
    vals = []
    ok = True
    for r in range(n):
        for refl in (1, -1):
            y = [order[(r + refl * k) % n] for k in range(n)]
            u1, z, w, up, v1, vq = y
            phi = wq(Q, z, w, v1, vq) + wq(Q, z, w, u1, up) - wq(Q, z, w, vq, up) - wq(Q, z, w, u1, v1)
            disp = wq(Q, u1, up, v1, vq) > 0
            vals.append((phi, disp))
            if phi < 0 or (not disp and phi != 0):
                ok = False
    return ok, vals


def all_restrictions_good(S, order):
    for sub in itertools.combinations(order, 6):
        subset = frozenset(sub)
        R = set()
        for sp in S:
            a, b = tuple(sp)
            a2, b2 = a & subset, b & subset
            if a2 and b2:
                R.add(frozenset([a2, b2]))
        if not six_locally_good(R, list(sub))[0]:
            return False
    return True


def blow_up(S, order, mult, shapes):
    """replace leaf x by a clade of mult[x] leaves; shapes[x] in {0,1} selects the caterpillar for mult 3:
    0 = ((a,b),c), 1 = (a,(b,c))."""
    groups = {}
    new_order = []
    extra = []
    for x in order:
        m = mult[x]
        names = [(x, i) for i in range(m)]
        groups[x] = frozenset(names)
        new_order += names
        if m == 3:
            inner = names[:2] if shapes[x] == 0 else names[1:]
            extra.append(frozenset(inner))
    full = frozenset(new_order)
    out = set()
    for sp in S:
        a, b = tuple(sp)
        A = frozenset().union(*[groups[x] for x in a])
        out.add(frozenset([A, full - A]))
    for x in new_order:
        out.add(frozenset([frozenset([x]), full - {x}]))
    for g in extra:
        out.add(frozenset([g, full - g]))
    return out, new_order


if __name__ == "__main__":
    t0 = time.time()
    trees = circular_trees(X)
    print("circular binary trees on 6 points:", len(trees))
    systems = set()
    for r in range(1, len(trees) + 1):
        pass
    # unions of non-empty sets of trees
    cur = {frozenset(t) for t in trees}
    frontier = set(cur)
    while frontier:
        new = set()
        for s in frontier:
            for t in trees:
                u = s | t
                if u not in cur:
                    cur.add(u)
                    new.add(u)
        frontier = new
    systems = sorted(cur, key=lambda s: (len(s), sorted(sorted(map(sorted, sp)) for sp in s)))
    print("tree-generated systems on 6 points:", len(systems))
    NT = nontrivial_circular_splits(X)
    two = lambda sp: min(len(a) for a in sp) == 2
    good = fail_neg = fail_supp = 0
    loc = 0
    failing = []
    excluded = []
    for S in systems:
        kal, exact, mn, rows = weight_classes(S, X)
        lg, _ = six_locally_good(S, X)
        loc += lg
        if kal and exact:
            good += 1
        else:
            failing.append((S, kal, exact))
            if not kal:
                fail_neg += 1
            else:
                fail_supp += 1
        if not lg:
            excluded.append((S, kal and exact, kal))
        if lg and not (kal and exact):
            print("  LOCALLY GOOD BUT FAILING ?!")
    print("Kalmanson with exact support: %d ; failing: %d (negative weight %d, Kalmanson with wrong support %d)"
          % (good, len(failing), fail_neg, fail_supp))
    print("6-locally good: %d ; excluded: %d (of which globally fine on six points: %d)"
          % (loc, len(excluded), sum(1 for _, g, _ in excluded if g)))
    desc = Counter()
    for S, g, kal in excluded:
        missing = sorted(NT - S, key=lambda sp: sorted(map(sorted, sp)))
        desc[(len([m for m in missing if two(m)]), len([m for m in missing if not two(m)]), g, kal)] += 1
    print("excluded systems by (missing 2-splits, missing 3-splits, fine on 6 points, Kalmanson on 6 points):", dict(desc))

    # ---- blow-ups (multiplicities <= 3, at most `maxleaves` leaves)
    maxleaves = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    summary = Counter()
    per_type = defaultdict(lambda: [0, 0, 0])
    for idx, (S, g, kal6) in enumerate(excluded):
        missing = sorted(NT - S, key=lambda sp: sorted(map(sorted, sp)))
        typ = (len([m for m in missing if two(m)]), len([m for m in missing if not two(m)]))
        best_fail = None       # smallest blow-up failing at all (wrong support or negative)
        best_neg = None        # smallest blow-up with a negative weight
        if not g:
            best_fail = (6, None, "kalmanson" if kal6 else "negative")
            if not kal6:
                best_neg = (6, None)
        for total in range(7, maxleaves + 1):
            if best_neg is not None:
                break
            for mult_t in itertools.product([1, 2, 3], repeat=6):
                if sum(mult_t) != total:
                    continue
                mult = dict(zip(X, mult_t))
                threes = [x for x in X if mult[x] == 3]
                for sh in itertools.product([0, 1], repeat=len(threes)):
                    shapes = dict(zip(threes, sh))
                    S2, o2 = blow_up(S, X, mult, shapes)
                    kal, exact, mn, rows = weight_classes(S2, o2)
                    if not (kal and exact) and best_fail is None:
                        best_fail = (total, mult_t, "kalmanson" if kal else "negative")
                    if not kal and best_neg is None:
                        best_neg = (total, mult_t)
                if best_neg is not None and best_fail is not None:
                    break
        summary[("minimal failing blow-up remains Kalmanson", best_fail[2] == "kalmanson" if best_fail else None)] += 1
        summary[("negative weight reached with <= %d leaves" % maxleaves, best_neg is not None)] += 1
        per_type[typ][0] += 1
        per_type[typ][1] += best_neg is not None
        per_type[typ][2] += (best_fail is not None)
        print("  excluded system %2d  missing(2-splits,3-splits)=%s fine_on_6=%s : minimal failing blow-up %s ; first negative weight %s  [%.0fs]"
              % (idx, typ, g, best_fail, best_neg, time.time() - t0), flush=True)
    print("summary:", dict(summary))
    print("by type (missing 2-splits, missing 3-splits): [systems, negative weight reached, some failure reached]:", dict(per_type))
