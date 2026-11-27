#!/usr/bin/env python3
"""Exact (rational) certificates for the facets of the bond-cluster LP outer bound.

Primal (see cluster_lp.py): maximise  c.(p3,p8,p11) = mu.obj_c - c3 - c8  over measures mu >= 0 on the allowed
cluster configurations with  mu(v=1) = 1,  mu invariant under the 12 cluster symmetries, star marginal symmetric.
Because the objective and the constraints are invariant under the cluster symmetries, we work with ORBITS of
configurations: variable nu(o) = total mass of orbit o; only the star constraints and the normalisation remain.

Certificate for  c.p <= b:  multipliers y (one per star constraint) and y0 (normalisation) with
     obj_c(o) - sum_k y_k R_k(o) - y0 * fv(o)  <=  0     for every allowed orbit o,        y0 - c3 - c8 <= b.
Then  mu.obj_c <= y0  for every feasible mu.  Everything is verified with exact rational arithmetic.

For finite sets: the orbits that violate "an occupied centre has >= 2 occupied neighbours" are listed with
their largest reduced cost M_c; a finite set S with N sites of which |E| have fewer than two occupied neighbours
satisfies  c.(e3/N - 1, e8/N - 1, e11/N) <= b + 2 M_c |E| / N.

usage: lp_exact.py LP_VERTICES.npy OUT.txt
"""
import sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull

CFG = list(itertools.product((0, 1), repeat=8))        # (v, w, u1, u2, u3, z1, z2, z3)

def C2(d):
    return d * (d - 1) // 2

ROWKEYS = []

def images(s):
    """the orbit of s under the 12 cluster symmetries"""
    out = set()
    v, w, u, z = s[0], s[1], s[2:5], s[5:8]
    for perm in itertools.permutations(range(3)):
        uu = tuple(u[i] for i in perm); zz = tuple(z[i] for i in perm)
        out.add((v, w) + uu + zz)
        out.add((w, v) + zz + uu)
    return out

def setup():
    seen = {}
    orbits = []
    for s in CFG:
        if s in seen: continue
        o = sorted(images(s))
        for t in o: seen[t] = len(orbits)
        orbits.append(o)
    def feats(s):
        v, w, u, z = s[0], s[1], s[2:5], s[5:8]
        dv = w + sum(u); dw = v + sum(z)
        f3 = Fr(v * w); f8 = Fr(C2(dv) + C2(dw), 2)
        f11 = Fr(sum(u[j] * z[k] for j in range(3) for k in range(3) if j != k))
        ok = not ((v and dv < 2) or (w and dw < 2))
        return f3, f8, f11, Fr(v), ok
    F = []
    for o in orbits:
        f = [feats(t) for t in o]
        # the functions are symmetric: averages over the orbit
        n = len(o)
        F.append((sum(x[0] for x in f) / n, sum(x[1] for x in f) / n, sum(x[2] for x in f) / n,
                  sum(x[3] for x in f) / n, all(x[4] for x in f), any(x[4] for x in f)))
    for f in F:
        assert f[4] == f[5]                # allowedness is constant on orbits
    # star constraints: for the symmetrised measure (mass nu(o) spread uniformly over the orbit),
    #   M(v, w=1, u1=0, u2, u3) - M(v, w=0, u1=1, u2, u3) = 0
    rows = []
    for (v, u2, u3) in itertools.product((0, 1), repeat=3):
        r = []
        for o in orbits:
            c = 0
            for t in o:
                if t[0] == v and t[3] == u2 and t[4] == u3:
                    if t[1] == 1 and t[2] == 0: c += 1
                    if t[1] == 0 and t[2] == 1: c -= 1
            r.append(Fr(c, len(o)))
        if any(x != 0 for x in r) and r not in rows and [-x for x in r] not in rows:
            rows.append(r); ROWKEYS.append((v, u2, u3))
    return orbits, F, rows

def certificate(c, orbits, F, rows):
    """c = integer triple.  returns (bound b_exact, y list, y0, M) verified exactly, or None"""
    allowed = [i for i in range(len(orbits)) if F[i][4]]
    m = len(rows)
    obj = [c[0] * 2 * F[i][0] + c[1] * F[i][1] + c[2] * F[i][2] for i in range(len(orbits))]
    # dual LP (floats): minimise y0  s.t.  sum_k y_k R_k(o) + y0 fv(o) >= obj(o) for allowed o
    A = np.array([[-float(rows[k][i]) for k in range(m)] + [-float(F[i][3])] for i in allowed])
    bvec = np.array([-float(obj[i]) for i in allowed])
    cost = np.zeros(m + 1); cost[-1] = 1
    res = linprog(cost, A_ub=A, b_ub=bvec, bounds=[(None, None)] * (m + 1), method="highs")
    if res.status != 0:
        return None
    for den in (1, 2, 3, 4, 6, 12, 24, 60, 120, 360, 2520, 10**6):
        y = [Fr(float(x)).limit_denominator(den) for x in res.x[:m]]
        # best y0 for this y: the smallest y0 with all reduced costs <= 0 (needs fv(o) > 0 where the rest is positive)
        need = Fr(-10**9); ok = True
        for i in allowed:
            rest = obj[i] - sum(y[k] * rows[k][i] for k in range(m))
            if F[i][3] > 0:
                need = max(need, rest / F[i][3])
            elif rest > 0:
                ok = False; break
        if not ok:
            continue
        y0 = need
        # exact verification
        for i in allowed:
            assert obj[i] - sum(y[k] * rows[k][i] for k in range(m)) - y0 * F[i][3] <= 0
        if abs(float(y0) - res.fun) < 1e-6:
            M = max([obj[i] - sum(y[k] * rows[k][i] for k in range(m)) - y0 * F[i][3]
                     for i in range(len(orbits)) if not F[i][4]] + [Fr(0)])
            return y0 - c[0] - c[1], y, y0, M
    return None

def main():
    V = np.load(sys.argv[1])
    orbits, F, rows = setup()
    out = open(sys.argv[2], "w")
    def P(*a):
        print(*a); print(*a, file=out)
    P(f"# {len(orbits)} orbits of cluster configurations, {sum(1 for f in F if f[4])} allowed; {len(rows)} star constraints")
    P(f"# star constraint k:  P(v, w=1, u1=0, u2, u3) - P(v, w=0, u1=1, u2, u3) = 0  for (v, u2, u3) = {ROWKEYS}")
    hull = ConvexHull(V)
    Vq = [[Fr(float(x)).limit_denominator(60) for x in v] for v in V]
    # exact facet planes through rational vertices
    facets = {}
    for simplex, eq in zip(hull.simplices, hull.equations):
        a, b_, c_ = (Vq[i] for i in simplex)
        e1 = [b_[k] - a[k] for k in range(3)]; e2 = [c_[k] - a[k] for k in range(3)]
        nrm = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]
        if sum(float(nrm[k]) * eq[k] for k in range(3)) < 0:
            nrm = [-x for x in nrm]
        # integer normal
        den = 1
        for x in nrm: den = den * x.denominator // np.gcd(den, x.denominator)
        ints = [int(x * den) for x in nrm]
        g = np.gcd.reduce([abs(x) for x in ints]); ints = [x // g for x in ints]
        rhs = sum(ints[k] * a[k] for k in range(3))
        facets[tuple(ints)] = rhs
    P(f"# LP polytope: {len(V)} vertices, {len(facets)} facets, volume {hull.volume:.6f}")
    P("# facet  c3*p3 + c8*p8 + c11*p11 <= b ;  certified bound (exact) ; equal? ; M (largest reduced cost of a forbidden orbit)")
    allok = True
    for c, b in sorted(facets.items()):
        # all vertices satisfy it
        assert all(sum(c[k] * v[k] for k in range(3)) <= b for v in Vq)
        cert = certificate(c, orbits, F, rows)
        if cert is None:
            P(f"  {c}  <= {b}   NO CERTIFICATE FOUND"); allok = False; continue
        bx, y, y0, M = cert
        c = tuple(int(x) for x in c)
        P(f"  {str(c):>16} . p <= {str(b):>6}    certified: <= {str(bx):>6}   {'EXACT' if bx == b else 'weaker'}   M = {M}   y = {[str(x) for x in y]}, y0 = {y0}")
        if bx != b: allok = False
    P(f"# all facets certified exactly: {allok}")
    # also certify the hand-proved inequalities and the box
    P("# other inequalities:")
    for c, name in (((-1, 0, 0), "p3 >= 0"), ((4, -1, 0), "p8 >= 4 p3"), ((6, -1, 0), "p8 >= 6 p3 - 1"),
                    ((-2, 1, 0), "p8 <= 3 + 2 p3"), ((0, 0, 1), "p11 <= ?"), ((1, 0, 0), "p3 <= ?"), ((0, 1, 0), "p8 <= ?"),
                    ((0, 0, -1), "p11 >= ?"), ((9, 4, 1), "9p3+4p8+p11 <= ?")):
        cert = certificate(c, orbits, F, rows)
        P(f"  {name:>18}:  {c} . p <= {cert[0]}   (M = {cert[3]})")
    out.close()

if __name__ == "__main__":
    main()
