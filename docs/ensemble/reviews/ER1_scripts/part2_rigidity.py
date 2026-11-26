#!/usr/bin/env python3
"""Referee checks for E5-E8: rigidity matroids (exact rank mod p), connectivity (brute force AND fundamental
circuits), realisability of splices (Cayley-Menger / multi-start least squares / exact sign enumeration in d = 1)."""
import itertools, sys
import numpy as np
from scipy.optimize import least_squares

rng = np.random.default_rng(13579)
P = 2_147_483_629   # prime < 2^31


def rank_mod_p(M):
    M = [[int(v) % P for v in row] for row in M]
    rk = 0; rows = len(M); cols = len(M[0]) if rows else 0
    for c in range(cols):
        piv = next((i for i in range(rk, rows) if M[i][c]), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], P - 2, P)
        M[rk] = [(v * inv) % P for v in M[rk]]
        for i in range(rows):
            if i != rk and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[rk])]
        rk += 1
        if rk == rows:
            break
    return rk


def rigidity_rows(E, n, d):
    p = [[int(v) for v in rng.integers(1, 10 ** 6, size=d)] for _ in range(n)]
    R = []
    for (i, j) in E:
        row = [0] * (n * d)
        for k in range(d):
            row[i * d + k] = p[i][k] - p[j][k]; row[j * d + k] = p[j][k] - p[i][k]
        R.append(row)
    return R


class Matroid:
    def __init__(self, E, n, d):
        self.R = rigidity_rows(E, n, d); self.m = len(E); self.cache = {}

    def r(self, J):
        J = tuple(sorted(J))
        if J not in self.cache:
            self.cache[J] = rank_mod_p([self.R[k] for k in J]) if J else 0
        return self.cache[J]

    def connected_bruteforce(self):
        m = self.m; full = self.r(range(m))
        for mask in range(1, 2 ** (m - 1)):
            J = [k for k in range(m) if mask >> k & 1]; Jc = [k for k in range(m) if not mask >> k & 1]
            if self.r(J) + self.r(Jc) == full:
                return False
        return True

    def components(self):
        """components via fundamental circuits w.r.t. a basis B: e (not in B) ~ b iff b in C(e, B)."""
        m = self.m; B = []
        for e in range(m):
            if self.r(B + [e]) == len(B) + 1:
                B.append(e)
        parent = list(range(m))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for e in range(m):
            if e in B:
                continue
            for b in B:
                Bb = [x for x in B if x != b] + [e]
                if self.r(Bb) == len(B):          # b is in the fundamental circuit of e
                    parent[find(b)] = find(e)
        comps = {}
        for e in range(m):
            comps.setdefault(find(e), []).append(e)
        return list(comps.values()), len(B)


def complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def wheel(k):
    return [(0, i) for i in range(1, k + 1)] + [(i, i % k + 1) for i in range(1, k + 1)]


def bipartite(a, b):
    return [(i, a + j) for i in range(a) for j in range(b)]


GRAPHS = {
    # name: (edges, n, d, generically globally rigid?)
    "K4, d=2": (complete(4), 4, 2, True),
    "K5, d=2": (complete(5), 5, 2, True),
    "wheel W4, d=2": (wheel(4), 5, 2, True),
    "wheel W6, d=2": (wheel(6), 7, 2, True),
    "K3 (triangle), d=2 [N < d+2]": (complete(3), 3, 2, True),
    "K_{3,3}, d=2 (Laman)": (bipartite(3, 3), 6, 2, False),
    "prism, d=2 (Laman)": ([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)], 6, 2, False),
    "two K4 glued along an edge, d=2": (complete(4) + [(0, 4), (0, 5), (1, 4), (1, 5), (4, 5)], 6, 2, False),
    "K4 + degree-2 vertex, d=2": (complete(4) + [(4, 0), (4, 1)], 5, 2, False),
    "K_{4,4}, d=2": (bipartite(4, 4), 8, 2, True),
    "K5, d=3": (complete(5), 5, 3, True),
    "K6 minus an edge, d=3": ([e for e in complete(6) if e != (0, 1)], 6, 3, True),   # two vertices trilaterated from a tetrahedron
    "octahedron K_{2,2,2}, d=3": ([e for e in complete(6) if e not in ((0, 1), (2, 3), (4, 5))], 6, 3, False),
    "K_{5,5}, d=3 (Connelly: not globally rigid)": (bipartite(5, 5), 10, 3, False),
    "double banana, d=3 (flexible circuit)": ([(a, b) for a in (0, 1) for b in (2, 3, 4)] + [(2, 3), (3, 4), (2, 4)]
                                              + [(a, b) for a in (0, 1) for b in (5, 6, 7)] + [(5, 6), (6, 7), (5, 7)],
                                              8, 3, False),
    "cycle C4, d=1": ([(0, 1), (1, 2), (2, 3), (3, 0)], 4, 1, True),
    "cycle C3, d=1": (complete(3), 3, 1, True),
    "path P4, d=1": ([(0, 1), (1, 2), (2, 3)], 4, 1, False),
    "two triangles sharing a vertex, d=1": ([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)], 5, 1, False),
    "K2, d=1 [N < d+2]": ([(0, 1)], 2, 1, True),
}


def sqlen(p, E):
    return np.array([np.sum((p[i] - p[j]) ** 2) for i, j in E])


def realise(E, n, d, q, starts=30, seeds=()):
    best = np.inf
    for s in range(starts):
        x0 = seeds[s].ravel().copy() if s < len(seeds) else rng.normal(size=n * d) * 1.5
        res = least_squares(lambda x: sqlen(x.reshape(n, d), E) - q, x0, xtol=1e-14, ftol=1e-14, gtol=1e-14)
        best = min(best, np.linalg.norm(res.fun))
        if best < 1e-10:
            break
    return best


def splice_test(name, pairs=3, splices=25, near=None):
    """smallest least-squares residual over non-constant splices of two conformers (and at a true conformer)."""
    E, n, d, _ = GRAPHS[name]; m = len(E)
    worst = np.inf; base = 0.0; realised = 0; tot = 0
    for _ in range(pairs):
        x1 = rng.normal(size=(n, d)); x2 = rng.normal(size=(n, d)) if near is None else x1 + near * rng.normal(size=(n, d))
        L = np.array([sqlen(x1, E), sqlen(x2, E)])
        base = max(base, realise(E, n, d, L[0], seeds=(x1 + 0.1 * rng.normal(size=(n, d)),)))
        for _ in range(splices):
            a = rng.integers(2, size=m)
            if a.min() == a.max():
                continue
            res = realise(E, n, d, L[a, range(m)], seeds=(x1, x2))
            worst = min(worst, res); tot += 1; realised += (res < 1e-9)
    return worst, base, realised, tot


def splice_along_separator(name, J, pairs=40, near=0.02):
    """E5(b): for x' near x, are BOTH splices along (J, J^c) realised?"""
    E, n, d, _ = GRAPHS[name]; m = len(E)
    both = 0
    for _ in range(pairs):
        x1 = rng.normal(size=(n, d)); x2 = x1 + near * rng.normal(size=(n, d))
        L = np.array([sqlen(x1, E), sqlen(x2, E)])
        a = np.array([0 if e in J else 1 for e in range(m)])
        r1 = realise(E, n, d, L[a, range(m)], seeds=(x1, x2)); r2 = realise(E, n, d, L[1 - a, range(m)], seeds=(x1, x2))
        both += (r1 < 1e-9 and r2 < 1e-9)
    return both, pairs


def cycle_on_line(n, trials=2000, integer=False):
    """C_n in R^1.  A vector q of lengths is realisable iff some signs give sum +-q_e = 0.
    Returns (#tuples with a realisable non-constant splice, #tuples with a second ensemble having the same laws)."""
    chim = 0; twin = 0; example = None
    for _ in range(trials):
        if integer:
            x = rng.integers(0, 9, size=(2, n)).astype(float)
        else:
            x = rng.normal(size=(2, n))
        L = np.abs(x - np.roll(x, -1, axis=1))                       # 2 x n lengths
        if integer and (np.any(L == 0) or np.any(L[0] == L[1])):
            continue
        real = set()
        for a in itertools.product((0, 1), repeat=n):
            if len(set(a)) == 1:
                continue
            q = L[list(a), range(n)]
            if any(abs(np.dot(s, q)) < 1e-9 for s in itertools.product((1, -1), repeat=n)):
                real.add(a)
        chim += bool(real)
        # equal weights: a second ensemble needs a realisable colouring a AND its complement
        for a in real:
            if tuple(1 - v for v in a) in real:
                twin += 1
                if example is None:
                    example = (x.copy(), a)
                break
    return chim, twin, example


def main():
    print("== rigidity matroids: rank, components, connectivity; consistency with [GGJ22 Thm 3.5]")
    viol = 0
    for name, (E, n, d, ggr) in GRAPHS.items():
        M = Matroid(E, n, d)
        comps, rk = M.components()
        conn = len(comps) == 1
        bf = M.connected_bruteforce() if len(E) <= 16 else None
        flag = ""
        if bf is not None and bf != conn:
            flag = "  !!! brute force disagrees"
        if ggr and n >= d + 2 and not conn:
            flag += "  !!! globally rigid on >= d+2 vertices but matroid not connected"; viol += 1
        print(f"   {name}: |E|={len(E)}, rank={rk}, components={sorted(len(c) for c in comps)}, connected={conn}"
              f"{'' if bf is None else ' (brute force: ' + str(bf) + ')'}; globally rigid: {ggr}{flag}")
    print(f"   violations of 'globally rigid on >= d+2 vertices => connected': {viol}")

    print("== E5(a)/E6: splices of two random conformers, connected matroids (should NOT be realisable)")
    for name in ("wheel W4, d=2", "two K4 glued along an edge, d=2", "K_{4,4}, d=2", "K6 minus an edge, d=3",
                 "double banana, d=3 (flexible circuit)"):
        w, b, rz, tot = splice_test(name)
        print(f"   {name}: smallest residual over {tot} random splices = {w:.2e} (true conformer: {b:.1e}); realised: {rz}")

    print("== E5(b): splices along a separator for nearby conformers (should be realisable: both splices)")
    for name, J in (("K_{3,3}, d=2 (Laman)", {0, 1, 2, 3}), ("prism, d=2 (Laman)", {0, 1, 2}),
                    ("K4 + degree-2 vertex, d=2", {6, 7}), ("octahedron K_{2,2,2}, d=3", {0, 1, 2, 3, 4})):
        both, pairs = splice_along_separator(name, J)
        print(f"   {name}, J = {sorted(J)}: both splices realised for {both}/{pairs} nearby pairs")

    print("== d = 1: cycles on a line (lengths |p_u - p_v|); exact sign enumeration")
    for n in (3, 4, 5):
        c, t, _ = cycle_on_line(n)
        print(f"   C_{n}, generic (Gaussian) conformers: tuples with a realisable non-constant splice: {c}/2000; "
              f"with a second two-conformer ensemble having the same laws: {t}")
    c, t, ex = cycle_on_line(4, integer=True)
    print(f"   C_4, INTEGER conformers (non-generic): realisable splice in {c}, same-law twin ensemble in {t}")
    if ex is not None:
        x, a = ex
        print(f"      example: x = {x[0].tolist()}, x' = {x[1].tolist()}, colouring {a} and its complement are both realisable")


if __name__ == "__main__":
    main()
