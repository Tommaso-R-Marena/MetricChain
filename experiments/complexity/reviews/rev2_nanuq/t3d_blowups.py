"""Task 3(d): Theorem 10(b) -- blow-ups of the 14 six-point systems that are globally good but not
6-locally good.  Blow-up implemented with the referee's own substitution routine (css.substitute):
multiplicity 2 = cherry, multiplicity 3 = caterpillar ((y1,y2),y3) in circular order."""
from itertools import product
from css import *

STAR3 = trivial_splits(3)
CAT4 = with_trivial(4, [canon(4, (1 << 1) | (1 << 2))])       # points r=0,y1,y2,y3 ; split {y1,y2}|{y3,r}

def blowup(n, sigma, mult):
    """replace leaves by clades, from the last leaf to the first so that earlier indices stay valid"""
    s, cur = frozenset(sigma), n
    for p in range(n - 1, -1, -1):
        if mult[p] == 2:
            s = substitute(cur, s, p, 3, STAR3, 0); cur += 1
        elif mult[p] == 3:
            s = substitute(cur, s, p, 4, CAT4, 0); cur += 2
    return cur, s

def system_missing(missing_sets):
    allnt = set(nontrivial_circular_splits(6))
    miss = set()
    for st in missing_sets:
        m = 0
        for p in st:
            m |= 1 << p
        miss.add(canon(6, m))
    assert miss <= allnt
    return with_trivial(6, allnt - miss)

listed = [
    ([(4, 5)], (1, 1, 1, 1, 1, 2)),
    ([(1, 2)], (1, 1, 2, 1, 1, 1)),
    ([(2, 3), (4, 5)], (1, 1, 1, 1, 1, 3)),
    ([(2, 3, 4, 5), (4, 5)], (1, 1, 1, 1, 2, 2)),
    ([(2, 3), (2, 3, 4, 5), (4, 5)], (1, 1, 1, 1, 3, 3)),
    ([(1, 2), (1, 2, 3, 4), (3, 4)], (1, 1, 1, 3, 3, 1)),
]
print("listed blow-ups (from the author's characterize6.py output), recomputed:")
for miss, mult in listed:
    s = system_missing(miss)
    assert is_tree_generated(6, [m for m in s if not is_trivial(6, m)])
    base = check(6, s)[0]
    n2, s2 = blowup(6, s, mult)
    assert is_tree_generated(n2, [m for m in s2 if not is_trivial(n2, m)])
    st, det = check(n2, s2)
    print(f"   missing {miss}: 6-point system '{base}', 6-locally good: {six_locally_good(6, s)}; blow-up {mult} "
          f"(n={n2}) -> '{st}' {dict((k, str(v)) for k, v in det.items()) if det else ''}")

print("own search: smallest failing blow-up (mult in {1,2,3}^6, total <= 10) for each of the 14 systems:")
tg6 = [with_trivial(6, nt) for nt in tree_generated_systems(6)]
cnt = 0
for s in tg6:
    if check(6, s)[0] != "ok" or six_locally_good(6, s):
        continue
    cnt += 1
    best = None
    for mult in product((1, 2, 3), repeat=6):
        tot = sum(mult)
        if tot == 6 or tot > 10 or (best and tot >= sum(best[0])):
            continue
        n2, s2 = blowup(6, s, mult)
        st, det = check(n2, s2)
        if st != "ok":
            best = (mult, st)
    allnt = set(nontrivial_circular_splits(6))
    miss = sorted(tuple(p for p in range(6) if (m >> p) & 1) for m in allnt - s)
    print("   missing", miss, "->", best)
print("systems treated:", cnt)
