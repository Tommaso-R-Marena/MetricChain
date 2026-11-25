#!/usr/bin/env python3
"""Coordinator spot checks of workstream S, part 5: the eleven dual certificates of Theorem 4.2 verified in exact
rational arithmetic with own code (the multipliers are the workstream's, read from its output lp_exact.txt; the
functions, the symmetry group and the notion "allowed" are re-implemented here).

For a row (c, b, M) with multipliers y_1..y_6 (star relations) and y_0 the function
    g(s) = c3*2[v][w] + c8*(C(d_v,2)+C(d_w,2))/2 + c11*sum_{j!=k} u_j z_k - sum_k y_k r_k(s) - y0*[v]
averaged over the 12 symmetries of the cluster must be <= 0 on every allowed pattern and <= M on the forbidden ones,
and y0 = b + c3 + c8.  (mu(v) = 1; mu is invariant under the 12 symmetries, so averaging changes no integral;
star relation k: P(v, w=1, u1=0, u2, u3) = P(v, w=0, u1=1, u2, u3).)"""
import sys, re, itertools
from fractions import Fraction as Fr
from math import comb

V, W, U, Z = 0, 1, (2, 3, 4), (5, 6, 7)
ROWKEYS = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 1)]


def syms():
    out = []
    ex = {V: W, W: V}
    for j in range(3):
        ex[U[j]] = Z[j]; ex[Z[j]] = U[j]
    for pj in itertools.permutations(range(3)):
        m = list(range(8))
        for j in range(3):
            m[U[j]] = U[pj[j]]; m[Z[j]] = Z[pj[j]]
        out.append(m)
        out.append([ex[m[s]] for s in range(8)])
    return out


SYMS = syms()


def dv(s): return s[W] + sum(s[u] for u in U)
def dw(s): return s[V] + sum(s[z] for z in Z)


def star_rel(k, s):
    v, u2, u3 = ROWKEYS[k]
    a = (s[V] == v and s[W] == 1 and s[U[0]] == 0 and s[U[1]] == u2 and s[U[2]] == u3)
    b = (s[V] == v and s[W] == 0 and s[U[0]] == 1 and s[U[1]] == u2 and s[U[2]] == u3)
    return int(a) - int(b)


def g(s, c, y, y0):
    val = Fr(c[0] * 2 * s[V] * s[W]) + Fr(c[1] * (comb(dv(s), 2) + comb(dw(s), 2)), 2)
    val += c[2] * sum(s[U[j]] * s[Z[k]] for j in range(3) for k in range(3) if j != k)
    val -= sum(y[k] * star_rel(k, s) for k in range(6))
    val -= y0 * s[V]
    return val


def main(path):
    rows = []
    for line in open(path):
        m = re.match(r"\s*\((-?\d+), (-?\d+), (-?\d+)\) \. p <=\s+(\S+)\s+certified: <=\s+(\S+)\s+EXACT\s+M = (\S+)\s+y = \[(.*)\], y0 = (\S+)", line)
        if m:
            c = tuple(int(m.group(i)) for i in (1, 2, 3))
            b = Fr(m.group(4)); M = Fr(m.group(6))
            y = [Fr(t.strip().strip("'")) for t in m.group(7).split(",")]
            rows.append((c, b, M, y, Fr(m.group(8))))
    assert len(rows) == 11
    pats = list(itertools.product((0, 1), repeat=8))
    for (c, b, M, y, y0) in rows:
        assert y0 == b + c[0] + c[1]
        worst_allowed, worst_forb = Fr(-10 ** 9), Fr(-10 ** 9)
        for s in pats:
            if not any(s):
                continue
            avg = sum(g(tuple(s[m[i]] for i in range(8)), c, y, y0) for m in SYMS) / 12
            forbidden = (s[V] and dv(s) < 2) or (s[W] and dw(s) < 2)
            if forbidden:
                worst_forb = max(worst_forb, avg)
            else:
                worst_allowed = max(worst_allowed, avg)
        assert worst_allowed <= 0 and worst_forb <= M, (c, worst_allowed, worst_forb)
        print(f"  {str(c):>14} . p <= {str(b):>2}: symmetrised reduced cost <= {worst_allowed} on allowed patterns, <= {worst_forb} on forbidden ones (M = {M}): exact")
    print("PART 5 OK: the eleven certificates of Theorem 4.2 hold in exact arithmetic")


if __name__ == "__main__":
    main(sys.argv[1])
