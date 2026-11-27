# c6_missing36.py -- REVIEW 6: the tree-generated six-point systems NOT found by the (re-)enumeration with <= 3
# hybrid nodes: their number, dihedral classes, and status of the NANUQ metric d_Sigma at six leaves, all from own
# code (150 systems as unions of the split systems of the 14 planar trees; metric from the definition in section 1
# of NANUQ_LOCAL_CRITERION.md).  Compared with the table of NANUQ_HIGHER_LEVELS.md section 2.2.
# Also: for each class, the planar trees whose splits lie in the system, and whether the trees needed are connected
# under single subtree-prune-and-regraft moves (a necessary condition for being the tree set of any network).
import itertools, pickle
from fractions import Fraction

N = 6
FULL = 63


def norm(m):
    return min(m, FULL ^ m)


def interval(i, ln):
    m = 0
    for t in range(ln):
        m |= 1 << ((i + t) % N)
    return m


TWO = [norm(interval(i, 2)) for i in range(6)]
THREE = sorted({norm(interval(i, 3)) for i in range(6)})


def planar_trees():
    """the 14 unrooted binary trees on 6 leaves that are planar for the circular order: sets of 3 pairwise
    compatible non-trivial circular splits"""
    S = sorted(set(TWO + THREE))

    def compat(a, b):
        A, B = (a, FULL ^ a), (b, FULL ^ b)
        return any((x & y) == 0 for x in A for y in B)
    return [frozenset(c) for c in itertools.combinations(S, 3) if all(compat(a, b) for a, b in itertools.combinations(c, 2))]


TREES = planar_trees()
assert len(TREES) == 14
SYSTEMS = set()
for r in range(1, 15):
    for comb in itertools.combinations(TREES, r):
        SYSTEMS.add(frozenset().union(*comb))
print("planar binary trees:", len(TREES), " tree-generated systems on six points:", len(SYSTEMS))
found = pickle.load(open("systems_level_3.pkl", "rb"))
missing = SYSTEMS - found
print("found by the re-enumeration (<= 3 hybrid nodes):", len(found), " all tree-generated:", found <= SYSTEMS, " not found:", len(missing))


def displayed(S, a, b, c, d):
    """is the quartet ab|cd displayed by the split system S (non-trivial splits as masks)?"""
    A, B = (1 << a) | (1 << b), (1 << c) | (1 << d)
    for m in S:
        for side in (m, FULL ^ m):
            if side & A == A and side & B == 0:
                return True
    return False


def metric(S):
    d = [[Fraction(0)] * N for _ in range(N)]
    for x, y in itertools.combinations(range(N), 2):
        tot = Fraction(2 * N - 4)
        rest = [l for l in range(N) if l not in (x, y)]
        for z, w in itertools.combinations(rest, 2):
            tops = [((x, y), (z, w)), ((x, z), (y, w)), ((x, w), (y, z))]
            disp = [t for t in tops if displayed(S, *t[0], *t[1])]
            assert disp
            notcherry = sum(1 for t in disp if t[0] != (x, y))
            tot += 2 * Fraction(notcherry, len(disp))
        d[x][y] = d[y][x] = tot
    return d


def status(S):
    d = metric(S)
    neg = wrong = False
    for i in range(N):
        for j in range(i + 1, N):
            a = d[i][j] + d[(i + 1) % N][(j + 1) % N] - d[i][(j + 1) % N] - d[(i + 1) % N][j]
            m = norm(interval(i + 1, j - i))
            trivial = bin(m).count("1") in (1, 5)
            if a < 0:
                neg = True
            if not trivial and ((a > 0) != (m in S)):
                wrong = True
    pattern = all(t in S for t in THREE) and not all(t in S for t in TWO)
    return ("negative weight" if neg else "wrong support" if wrong else "good at six leaves") + ("; has the pattern" if pattern else "")


def image(S, r, refl):
    out = set()
    for m in S:
        mm = 0
        for q in range(N):
            if (m >> q) & 1:
                mm |= 1 << ((((-q) % N if refl else q) + r) % N)
        out.add(norm(mm))
    return frozenset(out)


def name(m):
    for side in (m, FULL ^ m):
        ls = [q + 1 for q in range(N) if (side >> q) & 1]
        if len(ls) <= 3 and (len(ls) < 3 or 1 in ls or True):
            pass
    side = m if bin(m).count("1") <= 3 else FULL ^ m
    ls = [q for q in range(N) if (side >> q) & 1]
    # print as consecutive run
    for s in range(N):
        if all(((s + t) % N) in ls for t in range(len(ls))):
            return "".join(str((s + t) % N + 1) for t in range(len(ls)))


def spr_adjacent(T1, T2):
    """unrooted trees as split sets: do they differ by pruning one pendant subtree (a common clade or leaf)?"""
    if T1 == T2:
        return True
    cands = [1 << q for q in range(N)] + [s for m in (T1 & T2) for s in (m, FULL ^ m)]
    for X in cands:
        rest = FULL ^ X
        def restr(T, keep):
            out = set()
            for m in T:
                a = m & keep
                b = keep ^ a
                if bin(a).count("1") >= 2 and bin(b).count("1") >= 2:
                    out.add(min(a, b))
            return out
        if restr(T1, rest) == restr(T2, rest) and restr(T1, X) == restr(T2, X):
            return True
    return False


classes = {}
for S in missing:
    rep = min(tuple(sorted(image(S, r, refl))) for r in range(N) for refl in (0, 1))
    classes.setdefault(rep, set()).add(S)
print("dihedral classes of the systems not found:", len(classes))
for rep, members in sorted(classes.items(), key=lambda kv: (status(frozenset(kv[0])), len(kv[1]))):
    S = frozenset(rep)
    inside = [T for T in TREES if T <= S]
    # minimal requirement: every split of S must be covered; check connectivity of ALL trees inside (if the full set
    # is disconnected a connected covering subfamily may still exist; report components)
    comp = []
    todo = list(inside)
    while todo:
        c = [todo.pop()]
        ch = True
        while ch:
            ch = False
            for T in list(todo):
                if any(spr_adjacent(T, U) for U in c):
                    c.append(T); todo.remove(T); ch = True
        comp.append(c)
    covering = [c for c in comp if frozenset().union(*c) == S]
    print(f"  class of size {len(members):2d}: {status(S):40s} 2-splits {' '.join(sorted(name(m) for m in S if m in TWO))} | "
          f"3-splits {' '.join(sorted(name(m) for m in S if m in THREE)) or 'none'} | planar trees inside: {len(inside)}, "
          f"SPR-components: {[len(c) for c in comp]}, a component covers the system: {bool(covering)}")
