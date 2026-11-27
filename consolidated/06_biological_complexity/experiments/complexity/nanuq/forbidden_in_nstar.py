"""Consistency test of Theorem 10'(a): a system whose NANUQ metric is not Kalmanson must have a six-point restriction
that contains its three 3-splits and misses a 2-split.  Here: the 7-leaf non-galled network N* of counterexample7.py,
and the non-galled family N(s, t) of nongalled_formula.py for small s, t (if importable)."""
from itertools import combinations
from counterexample7 import NET, ORDER
from netcalc import nanuq_metric


def restrictions_with_pattern(order, splits):
    """splits: iterable of frozenset({A, B}) on the leaves in `order` (a circular order).  Yields (Y, missing 2-splits)
    for the 6-subsets Y whose restriction contains the three 3-splits and misses at least one 2-split."""
    out = []
    for Y in combinations(order, 6):
        Yset = set(Y)
        rest = set()
        for s in splits:
            A, B = tuple(s)
            a, b = frozenset(A & Yset), frozenset(B & Yset)
            if a and b:
                rest.add(frozenset([a, b]))
        three = [frozenset([frozenset(Y[k:k + 3]), frozenset(Yset - set(Y[k:k + 3]))]) for k in range(3)]
        two = []
        for k in range(6):
            pair = frozenset([Y[k], Y[(k + 1) % 6]])
            two.append(frozenset([pair, frozenset(Yset - pair)]))
        if all(t in rest for t in three):
            missing = [sorted(next(iter(x for x in t if len(x) == 2))) for t in two if t not in rest]
            if missing:
                out.append((Y, missing))
    return out


if __name__ == "__main__":
    d, splits = nanuq_metric(NET)
    res = restrictions_with_pattern(ORDER, splits)
    print("N*: six-leaf restrictions containing the three 3-splits and missing a 2-split:", len(res))
    for Y, missing in res:
        print("    leaves", Y, " missing 2-splits:", missing)
