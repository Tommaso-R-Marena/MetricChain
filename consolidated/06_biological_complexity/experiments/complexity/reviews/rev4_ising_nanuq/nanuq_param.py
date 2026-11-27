"""Referee's tests of Theorem 11 (parametric family rho = (rho_c, rho_s, rho_a, rho_o), author's reading for
outer-labeled planar networks: one planar quartet displayed = 'tree', both = '4-cycle').
All from explicit rooted networks; alpha_ij are computed as exact linear forms in rho."""
import itertools, random, sys, time
from fractions import Fraction as Fr
from collections import Counter, defaultdict
from nanuq_core import *

rng = random.Random(1111)
NAMES = ("c", "s", "a", "o")

# extreme rays of the closures of the stated domains (order c, s, a, o)
R_NANUQ = (0, 1, Fr(1, 2), 1)
R2 = (0, 1, 1, 1)
R3 = (1, 1, 1, 1)
R_MOD = (Fr(1, 2), 1, Fr(1, 2), 1)


def in_a(r):
    c, s, a, o = r
    return o == s and c + s <= 2 * a < 2 * s


def in_b(r):
    c, s, a, o = r
    return o == s and c <= a and s <= 2 * a < 2 * s


def fmt(f):
    """pretty linear form (const, c, s, a, o)"""
    out = []
    if f[0]:
        out.append(str(f[0]))
    for v, nme in zip(f[1:], NAMES):
        if v:
            out.append("%+g*%s" % (float(v), nme))
    return " ".join(out) if out else "0"


# ---------------------------------------------------------------- local terms of the parametric decomposition
def rho_forms(splits, order):
    """dict (frozenset 4-set, frozenset pair) -> form (c,s,a,o) with a single 1"""
    pos = {x: i for i, x in enumerate(order)}
    Q = quartets_from_splits(splits, order)
    out = {}
    for four in itertools.combinations(order, 4):
        key = frozenset(four)
        qs = Q[key]
        srt = sorted(four, key=lambda t: pos[t])
        for x, y in itertools.combinations(four, 2):
            pxy = frozenset([x, y])
            if len(qs) == 1:
                (q,) = tuple(qs)
                e = 0 if pxy in q else 1
            else:
                i, j = srt.index(x), srt.index(y)
                e = 2 if abs(i - j) in (1, 3) else 3
            v = [0, 0, 0, 0]
            v[e] = 1
            out[(key, pxy)] = tuple(v)
    return out


def add(a, b, sg=1):
    return tuple(p + sg * q for p, q in zip(a, b))


def local_terms(splits, order):
    """for every circular split: the local terms T4, T5(z), T6(z,w), TM(z,w) (non-trivial) or TQ(z), TP(z,w)
    (trivial), as forms (c,s,a,o); also checks that they add up to alpha/2 computed from the metric."""
    n = len(order)
    R = rho_forms(splits, order)
    forms = alpha_forms(splits, order)
    res = []
    Z = (0, 0, 0, 0)
    for i, j, sp in circ_splits(order):
        U = [order[k % n] for k in range(i + 1, i + 1 + ((j - i) % n))]
        V = [order[k % n] for k in range(j + 1, j + 1 + ((i - j) % n))]
        displayed = sp in splits
        if len(U) == 1 or len(V) == 1:
            if len(U) != 1:
                U, V = V, U
            u = U[0]
            a, b = V[-1], V[0]                # leaf before u and leaf after u
            others = [z for z in order if z not in (a, u, b)]
            terms = []
            tot = Z
            for z in others:
                q = frozenset([a, u, b, z])
                t = add(add(R[(q, frozenset([a, u]))], R[(q, frozenset([u, b]))]), R[(q, frozenset([a, b]))], -1)
                terms.append(("TQ", t, (z,)))
                tot = add(tot, t)
            for z, w in itertools.combinations(others, 2):
                t = add(add(R[(frozenset([a, u, z, w]), frozenset([a, u]))], R[(frozenset([u, b, z, w]), frozenset([u, b]))]),
                        R[(frozenset([a, b, z, w]), frozenset([a, b]))], -1)
                terms.append(("TP", t, (z, w)))
                tot = add(tot, t)
            f = forms[sp]
            assert f[0] == 2 * (n - 2) and tuple(Fr(v, 2) for v in f[1:]) == tuple(Fr(v) for v in tot), "trivial decomposition"
            res.append(dict(split=sp, trivial=True, displayed=True, terms=terms, alpha=f, u=u))
            continue
        u1, up, v1, vq = U[0], U[-1], V[0], V[-1]
        Y = [u1, up, v1, vq]
        pairs4 = [((vq, up), 1), ((u1, v1), 1), ((vq, v1), -1), ((u1, up), -1)]

        def c_of(q):
            t = Z
            for (s_, t_), sg in pairs4:
                if s_ in q and t_ in q:
                    t = add(t, R[(q, frozenset([s_, t_]))], sg)
            return t

        terms = [("T4", c_of(frozenset(Y)), ())]
        tot = terms[0][1]
        rest = [z for z in order if z not in Y]
        for z in rest:
            t = Z
            for y in Y:
                t = add(t, c_of(frozenset([w for w in Y if w != y] + [z])))
            terms.append(("T5", t, (z,)))
            tot = add(tot, t)
        for z, w in itertools.combinations(rest, 2):
            t = Z
            for (s_, t_), sg in pairs4:
                t = add(t, R[(frozenset([s_, t_, z, w]), frozenset([s_, t_]))], sg)
            kind = "T6" if ((z in U) == (w in U)) else "TM"
            terms.append((kind, t, (z, w)))
            tot = add(tot, t)
        f = forms[sp]
        assert f[0] == 0 and tuple(Fr(v, 2) for v in f[1:]) == tuple(Fr(v) for v in tot), "decomposition"
        res.append(dict(split=sp, trivial=False, displayed=displayed, terms=terms, alpha=f))
    return res


# ---------------------------------------------------------------- 1. sufficiency on explicit networks
def test_sufficiency(trials=3000, nmax=10, kmax=5):
    st = Counter()
    forms_seen = defaultdict(set)      # (kind, displayed, classA) -> forms
    seen = set()
    t0 = time.time()
    fails_mod = []
    smallest_mod_fail = None
    for it in range(trials):
        n = rng.randint(4, nmax)
        k = rng.randint(1, kmax)
        leaf_only = rng.random() < 0.35
        net = random_network(n, k, rng, galled=True, planar=True, tries=60, leaf_child_only=leaf_only)
        if not net.hybrids():
            continue
        key = canonical_key(net)
        if key in seen:
            continue
        seen.add(key)
        order = net.planar_order()
        S = net.split_system()
        classA = (net.mu() == 0)
        st["networks"] += 1
        st["class A (all hybrids with leaf child)"] += classA
        lev, nb = net.level()
        st["level-1"] += lev == 1
        LT = local_terms(S, order)
        for rec in LT:
            f = rec["alpha"]
            for kind, t, _ in rec["terms"]:
                forms_seen[(kind, rec["displayed"], classA)].add(t)
            if not rec["displayed"]:
                if any(f):
                    st["FAIL: alpha of an undisplayed split not identically 0"] += 1
                continue
            # domain (a): closure = cone(R_NANUQ, R2, R3), open towards R_NANUQ
            vals = [ev(f, r) for r in (R_NANUQ, R2, R3)]
            if not (vals[0] > 0 and vals[1] >= 0 and vals[2] >= 0):
                st["FAIL (a): displayed split not positive on the domain"] += 1
                print("   FAIL (a)", net.ch, rec["split"], fmt(f))
            if rec["trivial"]:
                n_ = len(order)
                if any(v < 2 * (n_ - 2) for v in vals):
                    st["trivial split below 2(n-2) on domain (a)"] += 1
            vm = ev(f, R_MOD)
            if classA:
                if not vm > 0:
                    st["FAIL (b): displayed split not positive at Modified NANUQ in class A"] += 1
                    print("   FAIL (b)", net.ch, rec["split"], fmt(f))
            else:
                if vm <= 0:
                    st["Modified NANUQ: displayed split with alpha <= 0 (outside class A)"] += 1
                    if vm < 0:
                        st["Modified NANUQ: negative weight"] += 1
                        if smallest_mod_fail is None or (len(order), lev) < smallest_mod_fail[0]:
                            smallest_mod_fail = ((len(order), lev), net.ch, net.root, order, rec["split"], vm)
    print("[1] sufficiency on %d distinct galled outer-labeled planar networks (4..%d leaves):" % (st["networks"], nmax))
    for k_, v in sorted(st.items()):
        print("    %-70s %d" % (k_, v))
    print("    smallest network with a negative Modified-NANUQ weight found:", smallest_mod_fail)
    print("    local forms that occur (kind, split displayed, class A):")
    for key in sorted(forms_seen):
        print("     ", key, sorted(fmt((0,) + t) for t in forms_seen[key]))
    print("    time %.0f s" % (time.time() - t0))
    return forms_seen


# ---------------------------------------------------------------- 2. the eight-leaf level-1 witness
def cycle_network(groups, hybrid_index=0):
    """level-1 network: a cycle with len(groups) positions; position `hybrid_index` is the hybrid.
    groups[i] = list of leaf names hanging (as a caterpillar clade) at position i.
    Rooted partner: root on the cycle edge opposite... we simply root at a new node on the cycle edge between
    positions 1 and 2 (any root on the cycle away from the hybrid gives the same semi-directed network)."""
    m = len(groups)
    assert hybrid_index == 0 and m >= 3
    ch = {}

    def clade(names, tag):
        if len(names) == 1:
            return names[0]
        top = names[0]
        for i, x in enumerate(names[1:]):
            node = "%s_c%d" % (tag, i)
            ch[node] = [top, x]
            top = node
        return top

    # cycle nodes c_0 (hybrid), c_1 .. c_{m-1}.  Root r is placed on the edge c_j - c_{j+1}, j = m//2
    j = max(1, m // 2)
    if j == m - 1:
        j = m - 2 if m > 3 else 1
    # path 1: r -> c_j -> c_{j-1} -> ... -> c_1 -> c_0 ;  path 2: r -> c_{j+1} -> ... -> c_{m-1} -> c_0
    for i in range(1, m):
        ch["c%d" % i] = [clade(groups[i], "g%d" % i)]
    ch["c0"] = [clade(groups[0], "g0")]
    for i in range(j, 0, -1):
        ch["c%d" % i].append("c%d" % (i - 1))
    for i in range(j + 1, m):
        ch["c%d" % i].append("c%d" % ((i + 1) % m))
    if j + 1 <= m - 1:
        ch["r"] = ["c%d" % j, "c%d" % (j + 1)]
    else:
        ch["r"] = ["c%d" % j, "c0"]
    return RNet(ch, "r")


def all_circular_orders(L):
    first = L[0]
    seen = set()
    for perm in itertools.permutations(L[1:]):
        if perm[0] > perm[-1]:
            continue
        yield [first] + list(perm)


def kalmanson_some_order(d, L):
    """number of circular orders for which all alpha_ij >= 0"""
    good = 0
    tot = 0
    n = len(L)
    for o in all_circular_orders(L):
        tot += 1
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if d[(o[i], o[j])] + d[(o[(i + 1) % n], o[(j + 1) % n])] - d[(o[i], o[(j + 1) % n])] - d[(o[(i + 1) % n], o[j])] < 0:
                    ok = False
                    break
            if not ok:
                break
        good += ok
    return good, tot


def test_witness8():
    print("[2] Modified NANUQ on level-1 networks: a 5-cycle, cherry below the hybrid, cherries at two other positions")
    for pos in itertools.combinations(range(1, 5), 2):
        groups = [["h1", "h2"]] + [[("p%d_1" % i), ("p%d_2" % i)] if i in pos else ["p%d" % i] for i in range(1, 5)]
        net = cycle_network(groups)
        assert net.is_valid() and net.is_galled(), net.ch
        lev, nb = net.level()
        order = net.planar_order()
        S = net.split_system()
        forms = alpha_forms(S, order)
        L = net.leaves()
        hsp = frozenset([frozenset(["h1", "h2"]), frozenset(L) - {"h1", "h2"}])
        f = forms[hsp]
        dm = {k: ev(v, R_MOD) for k, v in param_metric(S, order).items()}
        good, tot = kalmanson_some_order(dm, L)
        okN = check_conclusion(S, order, R_NANUQ)[:2]
        print("    cherries at cycle positions %s: n=%d level=%d  alpha(hybrid cherry|rest) = %s -> Modified NANUQ %s, NANUQ %s ;"
              " min alpha (Modified) = %s ; circular orders with all alpha>=0: %d of %d ; NANUQ conclusion %s"
              % (pos, len(L), lev, fmt(f), ev(f, R_MOD), ev(f, R_NANUQ),
                 min(ev(v, R_MOD) for v in forms.values()), good, tot, okN))


def test_small_level1(nmax=8):
    """smallest level-1 networks (one cycle with pendant clades) on which Modified NANUQ fails"""
    print("[2'] exhaustive over single-cycle level-1 networks with caterpillar-free group sizes (cycle length 3..6):")
    found = Counter()
    first = {}
    for n in range(4, nmax + 1):
        for m in range(3, 7):
            # compositions of n into m positive parts
            for comp in itertools.combinations(range(1, n), m - 1):
                sizes = [b - a for a, b in zip((0,) + comp, comp + (n,))]
                groups = [["g%d_%d" % (i, t) for t in range(sz)] for i, sz in enumerate(sizes)]
                net = cycle_network(groups)
                if not net.is_valid():
                    continue
                order = net.planar_order()
                S = net.split_system()
                nonneg, supp, mn, bad = check_conclusion(S, order, R_MOD)
                okN = check_conclusion(S, order, R_NANUQ)
                assert okN[0] and okN[1]
                if not nonneg:
                    found[(n, "negative")] += 1
                    first.setdefault((n, "negative"), (m, sizes, mn))
                elif not supp:
                    found[(n, "wrong support")] += 1
                    first.setdefault((n, "wrong support"), (m, sizes, mn))
                else:
                    found[(n, "ok")] += 1
    for k_ in sorted(found):
        print("    n=%d %-14s %d   first: %s" % (k_[0], k_[1], found[k_], first.get(k_)))


# ---------------------------------------------------------------- 3. necessity witnesses and blow-up
def blow_up(net, order, z, m, tag):
    """replace the leaf z by a caterpillar clade of m leaves; returns new net and order"""
    if m == 1:
        return net, order
    ch = {u: list(vs) for u, vs in net.ch.items()}
    names = ["%s%s%d" % (z, tag, i) for i in range(m)]
    top = names[0]
    for i, x in enumerate(names[1:]):
        node = "%s%s_cl%d" % (z, tag, i)
        ch[node] = [top, x]
        top = node
    (p,) = net.par[z]
    ch[p][ch[p].index(z)] = top
    del ch[z]
    new = RNet(ch, net.root)
    i = order.index(z)
    return new, order[:i] + names + order[i + 1:]


def find_witnesses(targets, trials=4000):
    """six-leaf networks of the class with a displayed non-trivial split and a pair z,w of NON-hybrid leaves
    whose pair term (T6 or TM) equals the target form.  Returns dict target -> (net, order, split, z, w, kind, classA)"""
    found = {}
    seen = set()
    for it in range(trials):
        k = rng.randint(1, 3)
        leaf_only = rng.random() < 0.6
        net = random_network(6, k, rng, galled=True, planar=True, tries=60, leaf_child_only=leaf_only)
        if not net.hybrids():
            continue
        key = canonical_key(net)
        if key in seen:
            continue
        seen.add(key)
        order = net.planar_order()
        S = net.split_system()
        classA = net.mu() == 0
        hyb_leaves = {net.ch[h][0] for h in net.hybrids()}
        for rec in local_terms(S, order):
            if rec["trivial"] or not rec["displayed"]:
                continue
            for kind, t, zw in rec["terms"]:
                if kind in ("T6", "TM") and t in targets and not (set(zw) & hyb_leaves):
                    k2 = (t, classA)
                    if k2 not in found:
                        found[k2] = (net, order, rec["split"], zw[0], zw[1], kind)
    return found


def test_necessity():
    # forms as (c, s, a, o)
    F = {"s-o": (0, 1, 0, -1), "o-s": (0, -1, 0, 1), "a-c": (-1, 0, 1, 0), "2a-c-s": (-1, -1, 2, 0)}
    found = find_witnesses(set(F.values()))
    print("[3] necessity witnesses on six leaves (pair of non-hybrid leaves, displayed split):")
    for name, f in F.items():
        for classA in (True, False):
            w = found.get((f, classA))
            print("    form %-7s in class %s: %s" % (name, "A (leaf children)" if classA else "general galled",
                                                    "FOUND (%s term)" % w[5] if w else "not found"))
    # blow-up: alpha(m) = 2 m^2 F + O(m)
    for name, f in F.items():
        for classA in (True, False):
            w = found.get((f, classA))
            if not w:
                continue
            net, order, sp, z, w_, kind = w
            vals = []
            for m in range(1, 7):
                n2, o2 = blow_up(net, order, z, m, "Z")
                n2, o2 = blow_up(n2, o2, w_, m, "W")
                assert n2.is_valid() and n2.is_galled() and n2.admits_order(o2)
                assert (n2.mu() == 0) == classA
                S2 = n2.split_system()
                # image of the split
                A, B = tuple(sp)
                def img(side):
                    out = set()
                    for x in side:
                        if x == z:
                            out |= {t for t in o2 if t.startswith(z + "Z")} if m > 1 else {z}
                        elif x == w_:
                            out |= {t for t in o2 if t.startswith(w_ + "W")} if m > 1 else {w_}
                        else:
                            out.add(x)
                    return frozenset(out)
                sp2 = frozenset([img(A), img(B)])
                assert sp2 in S2
                fm = alpha_forms(S2, o2)[sp2]
                vals.append(fm)
            # second differences of alpha(m) must equal 4F (alpha = 2 m^2 F + b m + c)
            dd = [tuple(vals[i + 2][t] - 2 * vals[i + 1][t] + vals[i][t] for t in range(5)) for i in range(len(vals) - 2)]
            ok = all(d == (0,) + tuple(4 * v for v in f) for d in dd)
            print("    blow-up of the %-7s witness (class %s): alpha(m), m=1..6 = %s ; second difference = 4F for all m: %s"
                  % (name, "A" if classA else "general", [fmt(v) for v in vals], ok))
            # explicit failure just outside the domain
            eps = Fr(1, 10)
            pts = {"s-o": (0, 1, Fr(3, 4), 1 + eps), "o-s": (0, 1, Fr(3, 4), 1 - eps),
                   "a-c": (Fr(1, 2) + eps, 1, Fr(1, 2), 1) if classA else (Fr(3, 4) + eps, 1, Fr(3, 4), 1),
                   "2a-c-s": (Fr(1, 2) + eps, 1, Fr(3, 4), 1)}
            r = pts[name]
            firstneg = next((m for m, v in zip(range(1, 7), vals) if ev(v, r) < 0), None)
            print("        at rho = %s (in (a): %s, in (b): %s): alpha(m) = %s ; first m with alpha < 0: %s"
                  % (tuple(str(v) for v in r), in_a(r), in_b(r), [str(ev(v, r)) for v in vals], firstneg))
    # 4-cycle and sunlets
    net = cycle_network([["h"], ["p1"], ["p2"], ["p3"]])
    order = net.planar_order()
    fs = alpha_forms(net.split_system(), order)
    print("    4-cycle network: alpha of the non-trivial splits:", sorted(fmt(f) for sp, f in fs.items() if all(len(s) > 1 for s in sp)))
    okall = True
    for n in range(4, 12):
        net = cycle_network([["h"]] + [["p%d" % i] for i in range(1, n)])
        order = net.planar_order()
        fs = alpha_forms(net.split_system(), order)
        f = fs[frozenset([frozenset(["h"]), frozenset(order) - {"h"}])]
        # alpha/2 = n-2 + ((n-3) + C(n-3,2)) (2 rho_a - rho_s)   given rho_o = rho_s
        cc, ss, aa, oo = f[1:]
        half = (Fr(f[0], 2), Fr(cc, 2), Fr(ss + oo, 2), Fr(aa, 2))
        mult = (n - 3) + (n - 3) * (n - 4) // 2
        want = (n - 2, 0, -mult, 2 * mult)
        okall &= (half == want)
    print("    n-sunlet, n=4..11: alpha/2 of the hybrid leaf's trivial split equals n-2+((n-3)+C(n-3,2))(2a-s) when o=s:", okall)


# ---------------------------------------------------------------- 4. how much of parameter space survives
def test_region(trials=1500):
    """collect all alpha forms of displayed splits over generated networks (plus blow-ups) and evaluate at
    test points inside / on the boundary / just outside the stated domains"""
    pts = {
        "inside (a): (0.1,1,0.7,1)": (Fr(1, 10), 1, Fr(7, 10), 1),
        "inside (a): (0,1,0.9,1)": (0, 1, Fr(9, 10), 1),
        "boundary (a): NANUQ (0,1,1/2,1)": R_NANUQ,
        "boundary (a): (0.4,1,0.7,1)  c+s=2a": (Fr(2, 5), 1, Fr(7, 10), 1),
        "outside (a), inside (b): Modified (1/2,1,1/2,1)": R_MOD,
        "outside (a), inside (b): (0.5,1,0.7,1)": (Fr(1, 2), 1, Fr(7, 10), 1),
        "outside (a): c+s = 2a + 0.02: (0.42,1,0.7,1)": (Fr(21, 50), 1, Fr(7, 10), 1),
        "outside: o = s + 0.02: (0.1,1,0.7,1.02)": (Fr(1, 10), 1, Fr(7, 10), Fr(51, 50)),
        "outside: o = s - 0.02: (0.1,1,0.7,0.98)": (Fr(1, 10), 1, Fr(7, 10), Fr(49, 50)),
        "outside: a = s: (0,1,1,1)": R2,
        "outside (b): c = a + 0.02: (0.72,1,0.7,1)": (Fr(18, 25), 1, Fr(7, 10), 1),
        "outside (b): s = 2a + 0.02: (0,1,0.49,1)": (0, 1, Fr(49, 100), 1),
    }
    res = {k: Counter() for k in pts}
    seen = set()
    nets = 0
    for it in range(trials):
        n = rng.randint(4, 12)
        k = rng.randint(1, 5)
        leaf_only = rng.random() < 0.4
        net = random_network(n, k, rng, galled=True, planar=True, tries=60, leaf_child_only=leaf_only)
        if not net.hybrids():
            continue
        key = canonical_key(net)
        if key in seen:
            continue
        seen.add(key)
        nets += 1
        order = net.planar_order()
        S = net.split_system()
        classA = net.mu() == 0
        forms = alpha_forms(S, order)
        for name, r in pts.items():
            ok = True
            for sp, f in forms.items():
                a = ev(f, r)
                if a < 0 or ((a > 0) != (sp in S)):
                    ok = False
                    break
            res[name][("A" if classA else "general", ok)] += 1
    print("[4] conclusion (circular decomposable with exact support) at test points, %d random networks (4..12 leaves):" % nets)
    for name in pts:
        c = res[name]
        print("    %-52s in(a)=%-5s in(b)=%-5s | class A: ok %d fail %d | general: ok %d fail %d"
              % (name, in_a(pts[name]), in_b(pts[name]), c[("A", True)], c[("A", False)], c[("general", True)], c[("general", False)]))


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3", "4"]
    if "2" in which:
        test_witness8()
        test_small_level1()
    if "3" in which: test_necessity()
    if "1" in which: test_sufficiency()
    if "4" in which: test_region()
