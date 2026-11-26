#!/usr/bin/env python3
"""r20_packing_identities.py -- workstream R20: the purely combinatorial identities used in Theorem 3 and
Corollary 4 of the note, checked by brute force on the packing side (no structures):
    for 3-PARTITION-shaped instances (n = 3m, B/4 < a_i < B/2):  Til = L * m! * 6^m
    for 4-PARTITION-shaped instances (n = 4m, B/5 < a_i < B/3):  Til = L * m! * 24^m
    always: prod_s mu_s! divides Til
with Til = number of arrangements of the labelled items into m ordered rows of total length B (brute force,
r20_theorem.arrangements) and L = number of partitions of the index set into m classes of total size B
(brute force over all maps to bins, r20_theorem.count_partitions).
Control that must fail: the same identity with the wrong per-class factor (6 <-> 24).
Usage: python3 -I -B r20_packing_identities.py"""
import sys
import os
from math import factorial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r20_theorem as T  # noqa: E402

CASES3 = [((2, 2, 2, 2, 2, 2), 2, 6), ((3, 2, 2, 3, 2, 2), 2, 7), ((3, 3, 3, 3, 3, 3), 2, 9),
          ((4, 4, 3, 3, 3, 3), 2, 10), ((5, 3, 3, 5, 3, 3), 2, 11), ((5, 4, 3, 3, 4, 3), 2, 11),
          ((4, 4, 4, 4, 5, 5), 2, 13), ((4, 4, 4, 4, 4, 6), 2, 13), ((6, 5, 5, 4, 4, 4), 2, 14),
          ((6, 6, 6, 4, 4, 4), 2, 15), ((7, 5, 4, 4, 5, 5), 2, 15),
          ((2,) * 9, 3, 6), ((3, 2, 2, 3, 2, 2, 3, 2, 2), 3, 7), ((4, 3, 3, 4, 3, 3, 3, 4, 3), 3, 10)]
CASES4 = [((4,) * 8, 2, 16), ((5, 4, 4, 4, 5, 4, 4, 4), 2, 17), ((5, 5, 5, 5, 4, 4, 4, 4), 2, 18),
          ((6, 5, 4, 4, 5, 5, 5, 4), 2, 19), ((6, 6, 4, 4, 4, 4, 5, 5), 2, 19), ((6, 6, 6, 4, 4, 4, 4, 4), 2, 19)]


def main():
    viol = 0
    ctrl = 0
    n = 0
    for cases, k, lo, hi in ((CASES3, 3, 4, 2), (CASES4, 4, 5, 3)):
        for (a, m, B) in cases:
            assert len(a) == k * m and sum(a) == m * B and all(B < lo * x and hi * x < B for x in a), (a, m, B)
            Til = len(T.arrangements(a, m, B))
            L = T.count_partitions(a, m, B)
            mu = {}
            for x in a:
                mu[x] = mu.get(x, 0) + 1
            pm = 1
            for v in mu.values():
                pm *= factorial(v)
            ok = (Til == L * factorial(m) * factorial(k) ** m) and Til % pm == 0
            wrong_factor = factorial(7 - k)  # 24 for k = 3, 6 for k = 4
            bad = (Til == L * factorial(m) * wrong_factor ** m)
            n += 1
            viol += 0 if ok else 1
            ctrl += 0 if bad else 1
            print("%d-PARTITION shape a=%s m=%d B=%d: L=%d Til=%d  L*m!*(%d!)^m=%d  prod mu!=%d  Til/prod=%d  %s" % (
                k, list(a), m, B, L, Til, k, L * factorial(m) * factorial(k) ** m, pm, Til // pm, "ok" if ok else "VIOLATION"))
    print("SUMMARY: %d instances; identity violations: %d; control (wrong factor) fails on %d instances (must be > 0; "
          "it cannot fail where L = 0)" % (n, viol, ctrl))
    print("RESULT:", "PASS" if viol == 0 and ctrl > 0 else "FAIL")
    print("END r20_packing_identities.py")


if __name__ == "__main__":
    main()
