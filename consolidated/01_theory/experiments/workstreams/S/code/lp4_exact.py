#!/usr/bin/env python3
"""Exact (rational) certificates for inequalities of the path-cluster LP (profile densities AND gauche density).

Variables: orbits of the 340 marked cluster configurations (code/cluster_lp4.py) under the 12 cluster symmetries.
Constraints left after the reduction: the star relations (swap of the distinguished neighbour with u1, marks
included) and the normalisation mu(v occupied) = 1.
Certificate of   c3 p3 + c8 p8 + c11 p11 + cq q <= b :   multipliers y_k, y0 (rationals) with
     c3*2[v][w] + c8*(C(dv,2)+C(dw,2))/2 + c11*sum_{j!=k} u_j z_k + cq*2*[gauche at vw] - sum_k y_k r_k - y0 ([v]+[w])/2 <= 0
on every orbit (verified with fractions), and b = y0 - c3 - c8.
The configurations already encode "an occupied centre has exactly two marked bonds", which holds for all beads of a
walk except its two ends; a walk with N beads therefore satisfies the inequality up to O(1/N).

usage: lp4_exact.py OUT.txt [LP4_VERTICES3.npy]
"""
import sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
from cluster_lp4 import configs, perm_cfg, inv_cfg

def C2(d): return d * (d - 1) // 2

def setup():
    CF = configs()
    index = {}
    orbits = []
    for c in CF:
        if c in index: continue
        o = set()
        for perm in itertools.permutations(range(3)):
            t = perm_cfg(c, perm)
            o.add(t); o.add(inv_cfg(t))
        o = sorted(o)
        for t in o: index[t] = len(orbits)
        orbits.append(o)
    def feats(c):
        v, w, u, z, mv, mw = c
        dv = w + sum(u); dw = v + sum(z)
        f3 = Fr(v * w); f8 = Fr(C2(dv) + C2(dw), 2)
        f11 = Fr(sum(u[j] * z[k] for j in range(3) for k in range(3) if j != k))
        fg = Fr(0)
        if 0 in mv:
            j = [s for s in mv if s != 0][0]; k = [s for s in mw if s != 0][0]
            fg = Fr(1 if j != k else 0)
        return f3, f8, f11, fg, Fr(v)
    F = []
    for o in orbits:
        f = [feats(t) for t in o]
        F.append(tuple(sum(x[i] for x in f) / len(o) for i in range(5)))
    # star relations
    def star(c):
        v, w, u, z, mv, mw = c
        return (v, w, u, mv)
    def swap(key):
        v, w, u, mv = key
        sw = {0: 1, 1: 0, 2: 2, 3: 3}
        return (v, u[0], (w, u[1], u[2]), tuple(sorted(sw[s] for s in mv)))
    keys = sorted({star(c) for c in CF} | {swap(star(c)) for c in CF})
    rows = []; seen = set()
    for key in keys:
        k2 = swap(key)
        if k2 == key or (k2, key) in seen: continue
        seen.add((key, k2))
        r = []
        for o in orbits:
            cnt = sum((1 if star(t) == key else 0) - (1 if star(t) == k2 else 0) for t in o)
            r.append(Fr(cnt, len(o)))
        if any(x != 0 for x in r): rows.append(r)
    # keep a maximal independent subset of rows (exact Gaussian elimination)
    basis = []; kept = []
    for r in rows:
        v = list(r)
        for b, piv in basis:
            if v[piv] != 0:
                f = v[piv] / b[piv]
                v = [x - f * y for x, y in zip(v, b)]
        piv = next((i for i, x in enumerate(v) if x != 0), None)
        if piv is not None:
            basis.append((v, piv)); kept.append(r)
    return orbits, F, kept

def certify(c, orbits, F, rows):
    """c = (c3, c8, c11, cq) rationals.  returns (b_exact, ok) with exact verification."""
    m = len(rows); n = len(orbits)
    obj = [c[0] * 2 * F[i][0] + c[1] * F[i][1] + c[2] * F[i][2] + c[3] * 2 * F[i][3] for i in range(n)]
    A = np.array([[-float(rows[k][i]) for k in range(m)] + [-float(F[i][4])] for i in range(n)])
    bvec = np.array([-float(x) for x in obj])
    cost = np.zeros(m + 1); cost[-1] = 1
    res = linprog(cost, A_ub=A, b_ub=bvec, bounds=[(None, None)] * (m + 1), method="highs")
    if res.status != 0: return None
    for den in (1, 2, 3, 4, 6, 8, 12, 24, 48, 120, 720, 5040, 10**6, 10**9):
        y = [Fr(float(x)).limit_denominator(den) for x in res.x[:m]]
        need = None; ok = True
        for i in range(n):
            rest = obj[i] - sum(y[k] * rows[k][i] for k in range(m) if rows[k][i] != 0)
            if F[i][4] > 0:
                q = rest / F[i][4]
                need = q if need is None or q > need else need
            elif rest > 0:
                ok = False; break
        if not ok: continue
        y0 = need
        assert all(obj[i] - sum(y[k] * rows[k][i] for k in range(m) if rows[k][i] != 0) - y0 * F[i][4] <= 0 for i in range(n))
        if abs(float(y0) - res.fun) < 1e-6:
            return y0 - c[0] - c[1], den
    return None

def main():
    out = open(sys.argv[1], "w")
    def P(*a):
        print(*a); print(*a, file=out)
    orbits, F, rows = setup()
    P(f"# path-cluster LP: {sum(len(o) for o in orbits)} configurations in {len(orbits)} orbits; {len(rows)} independent star relations")
    P("# gauche inequalities  c3 p3 + c8 p8 + c11 p11 + cq q <= b  (exact certificates):")
    for c in [(0, 0, 0, 1), (0, 0, 0, -1), (-4, 0, 2, -1), (-3, 0, 2, -1), (-2, 0, 2, -1), (0, 0, 2, -1), (0, -1, 2, -1), (-4, 1, 1, -1),
              (0, 0, 1, -1), (0, 0, 1, 0), (-2, 1, 0, 0), (6, -1, 0, 0), (4, -1, 0, 0)]:
        r = certify(tuple(Fr(x) for x in c), orbits, F, rows)
        P(f"  {str(c):>18} . (p,q) <= {r[0] if r else 'NO CERTIFICATE'}" + (f"    (multipliers with denominators <= {r[1]})" if r else ""))
    if len(sys.argv) > 2:
        V = np.load(sys.argv[2])
        Vq = [[Fr(float(x)).limit_denominator(120) for x in v] for v in V]
        hull = ConvexHull(V)
        facets = {}
        for simplex, eq in zip(hull.simplices, hull.equations):
            a, b_, c_ = (Vq[i] for i in simplex)
            e1 = [b_[k] - a[k] for k in range(3)]; e2 = [c_[k] - a[k] for k in range(3)]
            nrm = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]
            if sum(float(nrm[k]) * eq[k] for k in range(3)) < 0: nrm = [-x for x in nrm]
            den = 1
            for x in nrm: den = den * x.denominator // int(np.gcd(den, x.denominator))
            ints = [int(x * den) for x in nrm]
            g = int(np.gcd.reduce([abs(x) for x in ints])); ints = tuple(x // g for x in ints)
            facets[ints] = sum(ints[k] * a[k] for k in range(3))
        P(f"# facets of the profile polytope of the path-cluster LP ({len(V)} vertices, volume {hull.volume:.6f}): exact certificates")
        allok = True
        for c, b in sorted(facets.items()):
            r = certify((Fr(c[0]), Fr(c[1]), Fr(c[2]), Fr(0)), orbits, F, rows)
            ok = r is not None and r[0] == b
            allok &= ok
            P(f"  {str(c):>16} . p <= {str(b):>5}    certified: {r[0] if r else 'NONE'}   {'EXACT' if ok else 'NOT EQUAL'}")
        P(f"# all facets certified exactly: {allok}")
    out.close()

if __name__ == "__main__":
    main()
