#!/usr/bin/env python3
"""R8 / script 03 -- Lemma A16.5 (isoperimetry with an energy constraint) by brute force over
GENERAL members of the class (not over the profile the proof says is optimal).  Own code.

Statement tested.  u > 0, U0 <= 0, D a subset of Q_n with |D| = N.  Among all u-Lipschitz g
that vanish outside D and have mean energy U_g >= U0,   Z_g <= Zpl(N, U0), where
   Zpl(N,U0) = partition function of  -min(c*, u dist(x, D*^c)),  D* = the LAST N points of the
   simplicial order (complement of an initial segment), c* the level with mean energy U0
   (the full cone if its mean energy is >= U0).

Parts
 A  Harper's theorem in the form used: for every subset D of Q_4 (all 65 534), of Q_3, and random
    subsets of Q_5, Q_6, the erosion numbers #{x : dist(x, D^c) >= k} are, for all k at once, at
    most those of D*.  Also: D* is isomorphic to an initial segment (same erosion numbers).
 B  the lemma as a CONVEX PROGRAMME in the weights t = e^{-g}:
       max sum_x t(x)   s.t.  t = 1 off D;  t(x) <= e^u t(y) for neighbours;
                              phi(t) = sum t ln t + U0 sum t <= 0,
    solved by Kelley's cutting planes with HiGHS (feasibility tolerances 1e-10): the LP values are
    upper bounds that decrease to the optimum; a feasible point on the segment to t = 1 gives a
    lower bound.  All supports of Q_3; all supports of Q_4 up to the 384 symmetries; random
    supports in Q_5, Q_6.  No assumption on the form of the optimiser.
 C  exhaustive grid: every u-Lipschitz function on Q_3 with values in (u/4)Z and on Q_4 with
    values in (u/2)Z that vanishes at one vertex (WLOG vertex 0), hills and dips alike:
       U_g <= 0  =>  Z_g <= Zpl(#{g != 0}, U_g);        U_g >= 0  =>  Z_g <= 2^n.
 D  random general members with dips and hills on random supports, n = 5..10.
 E  mutations (the test can fail): (1) the comparison set replaced by a subcube of the same size;
    (2) the energy constraint dropped.

Run:  python3 r8_03_isoperimetry.py [quick]       (full: about 10 minutes)
"""
import itertools, math, sys, time
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(8)
TOL = 1e-10
HOPT = {"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10}


# ---------------------------------------------------------------- cube utilities
class Cube:
    def __init__(self, n):
        self.n = n
        self.N = 1 << n
        x = np.arange(self.N)
        self.pc = np.array([bin(v).count("1") for v in range(self.N)])
        self.nb = np.stack([x ^ (1 << i) for i in range(n)], axis=1)
        self.dist = self.pc[x[:, None] ^ x[None, :]]
        # simplicial order: by weight, then lexicographic on the sorted list of elements
        key = lambda v: (self.pc[v], tuple(i for i in range(n) if (v >> i) & 1))
        self.simp = sorted(range(self.N), key=key)
        self.edges = [(a, a ^ (1 << i)) for a in range(self.N) for i in range(n) if a < a ^ (1 << i)]

    def final_segment(self, N):
        m = np.zeros(self.N, dtype=bool)
        if N > 0:
            m[self.simp[self.N - N:]] = True
        return m

    def initial_segment(self, N):
        m = np.zeros(self.N, dtype=bool)
        m[self.simp[:N]] = True
        return m

    def rho(self, D):
        """dist(x, complement of D); 0 off D.  D boolean mask, D != everything."""
        comp = np.where(~D)[0]
        r = self.dist[:, comp].min(axis=1)
        return r

    def erosion(self, D):
        r = self.rho(D)
        return np.array([(r >= k).sum() for k in range(1, self.n + 2)])


def plateau_Z(cube, D, U0, u):
    """Z and level of the plateau on D with mean energy U0 (full cone if feasible)."""
    r = cube.rho(D).astype(float)
    def stats(c):
        g = -np.minimum(c, u * r)
        w = np.exp(-g)
        Z = w.sum()
        return Z, float((w * g).sum() / Z)
    cmax = u * r.max()
    Zc, Uc = stats(cmax)
    if Uc >= U0:
        return Zc, cmax
    lo, hi = 0.0, cmax
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if stats(mid)[1] > U0:
            lo = mid
        else:
            hi = mid
    c = 0.5 * (lo + hi)
    return stats(c)[0], c


# ---------------------------------------------------------------- part A
def part_A(quick):
    print("== A: Harper's theorem in the form used (erosion numbers) ==")
    ok = True
    for n in (3, 4):
        cube = Cube(n)
        best = {N: cube.erosion(cube.final_segment(N)) for N in range(1, cube.N)}
        ini = {N: cube.erosion(cube.initial_segment(N)) for N in range(1, cube.N)}
        iso = all((best[N] == ini[N]).all() for N in best)
        # all subsets via vectorised bit tricks: rho >= k  <=>  ball of radius k-1 around x inside D
        masks = np.arange(1, (1 << cube.N) - 1, dtype=np.int64)
        ballmask = [[0] * cube.N for _ in range(n + 1)]
        for k in range(n + 1):
            for x in range(cube.N):
                m = 0
                for y in range(cube.N):
                    if cube.dist[x, y] <= k:
                        m |= 1 << y
                ballmask[k][x] = m
        sizes = np.zeros(len(masks), dtype=np.int64)
        for y in range(cube.N):
            sizes += (masks >> y) & 1
        viol = 0
        for k in range(1, n + 1):
            cnt = np.zeros(len(masks), dtype=np.int64)
            for x in range(cube.N):
                bm = ballmask[k - 1][x]
                cnt += ((masks & bm) == bm)
            bound = np.array([best[N][k - 1] for N in range(1, cube.N)])
            viol += int((cnt > bound[sizes - 1]).sum())
        print(f"  Q_{n}: all {len(masks)} proper non-empty subsets, all k: violations {viol};  final segment ~ initial segment: {iso}")
        ok &= viol == 0 and iso
    for n in (5, 6):
        cube = Cube(n)
        best = {N: cube.erosion(cube.final_segment(N)) for N in range(1, cube.N)}
        viol = 0; cnt = 0
        reps = 2000 if quick else 20000
        for _ in range(reps):
            N = int(rng.integers(1, cube.N))
            kind = rng.integers(0, 3)
            if kind == 0:
                D = np.zeros(cube.N, dtype=bool); D[rng.choice(cube.N, N, replace=False)] = True
            elif kind == 1:      # ball-like around a random centre with random tie-breaking
                c = int(rng.integers(0, cube.N))
                order = np.lexsort((rng.random(cube.N), cube.dist[c]))
                D = np.zeros(cube.N, dtype=bool); D[order[:N]] = True
            else:                # grown cluster
                D = np.zeros(cube.N, dtype=bool); D[int(rng.integers(0, cube.N))] = True
                while D.sum() < N:
                    fr = np.where(~D & (D[cube.nb].any(axis=1)))[0]
                    D[rng.choice(fr)] = True
            e = cube.erosion(D)
            viol += int((e > best[N]).any()); cnt += 1
        print(f"  Q_{n}: {cnt} random subsets (uniform, ball-like, grown): violations {viol}")
        ok &= viol == 0
    return ok


# ---------------------------------------------------------------- part B
def solve_convex(cube, D, U0, u, target=None, maxit=300, rtol=1e-8):
    """max sum t  s.t. t=1 off D, class cone, phi(t) <= 0.  Returns (UB, LB, iterations).
    UB: value of an outer (cutting-plane) LP relaxation -- a rigorous upper bound on the optimum
    up to the LP tolerance.  LB: value of a feasible member.  The cuts are gradient cuts of the
    convex constraint; the first ones are taken at clipped-level profiles on D (any point gives
    a valid cut, so this assumes nothing about the optimiser).
    If target is given, stops as soon as UB <= target (1 + rtol)."""
    idx = np.where(D)[0]
    pos = {int(v): k for k, v in enumerate(idx)}
    m = len(idx)
    r = cube.rho(D).astype(float)
    A = []; b = []
    for (x, y) in cube.edges:
        for (p, q) in ((x, y), (y, x)):          # t(p) - e^u t(q) <= 0
            row = np.zeros(m); rhs = 0.0
            if p in pos: row[pos[p]] += 1.0
            else: rhs -= 1.0
            if q in pos: row[pos[q]] -= math.exp(u)
            else: rhs += math.exp(u)
            if p in pos or q in pos:
                A.append(row); b.append(rhs)
    A = np.array(A); b = np.array(b)
    bounds = [(math.exp(-u * r[v]), math.exp(u * r[v])) for v in idx]
    noff = cube.N - m
    cuts_A = []; cuts_b = []
    def add_cut(t):
        phi = float((t * np.log(t)).sum() + U0 * (t.sum() + noff))
        grad = np.log(t) + 1.0 + U0
        cuts_A.append(grad[None, :]); cuts_b.append(float(grad @ t - phi))
        return phi
    rD = r[idx]
    for c in np.linspace(0.0, u * rD.max(), 9)[1:]:
        add_cut(np.exp(np.minimum(c, u * rD)))
    UB = np.inf; LB = cube.N * 1.0       # t = 1 is feasible since U0 <= 0
    for it in range(maxit):
        AA = np.vstack([A] + cuts_A)
        bb = np.concatenate([b, np.array(cuts_b)])
        res = linprog(-np.ones(m), A_ub=AA, b_ub=bb, bounds=bounds, method="highs", options=HOPT)
        if res.status != 0:
            raise RuntimeError(res.message)
        t = res.x
        UB = min(UB, -res.fun + noff)
        phi = add_cut(t)
        if phi <= 0:
            LB = max(LB, t.sum() + noff)
        else:
            lo, hi = 0.0, 1.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                tm = 1 + mid * (t - 1)
                if (tm * np.log(tm)).sum() + U0 * (tm.sum() + noff) <= 0: lo = mid
                else: hi = mid
            tf = 1 + lo * (t - 1)
            LB = max(LB, tf.sum() + noff)
            add_cut(tf)
        if target is not None and UB <= target * (1 + rtol):
            return UB, LB, it + 1
        if UB - LB <= rtol * max(1.0, UB) or phi <= 1e-11:
            return UB, LB, it + 1
    return UB, LB, maxit


def canon_supports(cube):
    """one representative per orbit of subsets under the automorphism group of the cube"""
    n, N = cube.n, cube.N
    perms = []
    for p in itertools.permutations(range(n)):
        for flip in range(N):
            img = np.zeros(N, dtype=np.int64)
            for x in range(N):
                y = 0
                for i in range(n):
                    if (x >> i) & 1: y |= 1 << p[i]
                img[x] = y ^ flip
            perms.append(img)
    perms = np.array(perms)                               # (|G|, N)
    pw = (1 << perms).astype(np.int64)
    seen = np.zeros(1 << N, dtype=bool)
    reps = []
    for m in range(1, (1 << N) - 1):
        if seen[m]: continue
        bits = np.array([(m >> x) & 1 for x in range(N)], dtype=np.int64)
        imgs = (pw * bits[None, :]).sum(axis=1)
        seen[imgs] = True
        reps.append((m, len(np.unique(imgs))))
    return reps


def part_B(quick):
    print("== B: the lemma as a convex programme over all members with a given support ==")
    ok = True
    worst_feas = -np.inf        # largest (feasible value - Zpl)/Zpl : > 0 would be a counterexample
    worst_cert = -np.inf        # largest (upper bound - Zpl)/Zpl at termination: certified slack
    for n in (3, 4):
        cube = Cube(n)
        reps = canon_supports(cube)
        tot_orbits = sum(sz for _, sz in reps)
        print(f"  Q_{n}: {len(reps)} orbits of supports ({tot_orbits} supports)")
        for u in ((1.0, 2.0) if not quick else (1.0,)):
            ncase = 0; nviol = 0; its = 0; nopen = 0
            zpl_cache = {}
            for (m, sz) in reps:
                D = np.array([(m >> x) & 1 for x in range(cube.N)], dtype=bool)
                N = int(D.sum())
                Dstar = cube.final_segment(N)
                r = cube.rho(Dstar).astype(float)
                gc = -u * r; wc = np.exp(-gc); Ucone = float((wc * gc).sum() / wc.sum())
                for frac in (0.15, 0.5, 0.85, 1.2):
                    U0 = frac * Ucone
                    key = (N, frac)
                    if key not in zpl_cache:
                        zpl_cache[key] = plateau_Z(cube, Dstar, U0, u)[0]
                    Zpl = zpl_cache[key]
                    UB, LB, k = solve_convex(cube, D, U0, u, target=Zpl)
                    its += k; ncase += 1
                    worst_feas = max(worst_feas, (LB - Zpl) / Zpl)
                    worst_cert = max(worst_cert, (UB - Zpl) / Zpl)
                    if LB > Zpl * (1 + 1e-9):
                        nviol += 1
                        print("   VIOLATION", n, u, bin(m), U0, LB, Zpl)
                    if UB > Zpl * (1 + 1e-6):
                        nopen += 1
            print(f"     u={u}: cases {ncase} (orbit x U0), LP solves {its}, violations {nviol}, not certified to 1e-6: {nopen}")
            ok &= nviol == 0 and nopen == 0
            # tightness: on D* itself the optimum over ALL members is the plateau
            dev = 0.0
            for N in range(1, cube.N):
                Dstar = cube.final_segment(N)
                r = cube.rho(Dstar).astype(float)
                gc = -u * r; wc = np.exp(-gc); Ucone = float((wc * gc).sum() / wc.sum())
                for frac in (0.15, 0.5, 0.85, 1.2):
                    U0 = frac * Ucone
                    Zpl = plateau_Z(cube, Dstar, U0, u)[0]
                    UB, LB, k = solve_convex(cube, Dstar, U0, u, target=None, rtol=1e-9)
                    dev = max(dev, abs(UB - Zpl) / Zpl, abs(LB - Zpl) / Zpl)
            print(f"     u={u}: on D* (every size) the optimum over all members equals the plateau value to {dev:.1e}")
            ok &= dev < 1e-6
    for n in (5, 6):
        cube = Cube(n)
        ncase = 0; nviol = 0; nopen = 0
        reps_n = (40 if n == 5 else 15) if quick else (500 if n == 5 else 150)
        for _ in range(reps_n):
            u = float(rng.choice([0.7, 1.5]))
            N = int(rng.integers(2, cube.N - 1))
            kind = rng.integers(0, 3)
            if kind == 0:
                D = np.zeros(cube.N, dtype=bool); D[rng.choice(cube.N, N, replace=False)] = True
            elif kind == 1:
                c = int(rng.integers(0, cube.N))
                order = np.lexsort((rng.random(cube.N), cube.dist[c]))
                D = np.zeros(cube.N, dtype=bool); D[order[:N]] = True
            else:
                D = np.zeros(cube.N, dtype=bool); D[int(rng.integers(0, cube.N))] = True
                while D.sum() < N:
                    fr = np.where(~D & (D[cube.nb].any(axis=1)))[0]
                    D[rng.choice(fr)] = True
            Dstar = cube.final_segment(N)
            r = cube.rho(Dstar).astype(float)
            gc = -u * r; wc = np.exp(-gc); Ucone = float((wc * gc).sum() / wc.sum())
            U0 = float(rng.uniform(0.05, 1.1)) * Ucone
            Zpl = plateau_Z(cube, Dstar, U0, u)[0]
            UB, LB, k = solve_convex(cube, D, U0, u, target=Zpl)
            ncase += 1
            worst_feas = max(worst_feas, (LB - Zpl) / Zpl)
            worst_cert = max(worst_cert, (UB - Zpl) / Zpl)
            if LB > Zpl * (1 + 1e-9):
                nviol += 1; print("   VIOLATION", n, u, N, U0, LB, Zpl)
            if UB > Zpl * (1 + 1e-6):
                nopen += 1
        print(f"  Q_{n}: {ncase} random supports (uniform, ball-like, grown): violations {nviol}, not certified to 1e-6: {nopen}")
        ok &= nviol == 0 and nopen == 0
    print(f"  largest (feasible value - Zpl)/Zpl over all cases: {worst_feas:+.2e};  largest (LP upper bound - Zpl)/Zpl: {worst_cert:+.2e}")
    return ok


# ---------------------------------------------------------------- part C
def grid_partial(cube, q, upto):
    """all integer functions on the first `upto` vertices (ordered by weight) with k(0) = 0 and
    |k(x)-k(y)| <= q on the edges among them.  Returns (order, array)."""
    N = cube.N
    order = sorted(range(N), key=lambda v: (cube.pc[v], v))
    posn = {v: i for i, v in enumerate(order)}
    F = np.zeros((1, 1), dtype=np.int8)
    return order, posn, extend(cube, q, order, posn, F, 1, upto)


def extend(cube, q, order, posn, F, start, stop):
    for step in range(start, stop):
        v = order[step]
        prev = [posn[int(w)] for w in cube.nb[v] if posn[int(w)] < step]
        lo = (F[:, prev].max(axis=1) - q).astype(np.int16)
        hi = (F[:, prev].min(axis=1) + q).astype(np.int16)
        cnt = np.maximum(hi - lo + 1, 0).astype(np.int64)
        tot = int(cnt.sum())
        rep = np.repeat(np.arange(len(F)), cnt)
        off = np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        newcol = (lo[rep] + off).astype(np.int8)
        F = np.concatenate([F[rep], newcol[:, None]], axis=1)
    return F


def zpl_batch(cube, N, U0s, u):
    """vectorised Zpl(N, U0) for an array of U0 <= 0 (bisection on the level; the returned value
    is the one at the upper end of the last bisection interval, i.e. an under-estimate of Zpl by
    less than 1e-12 relative -- conservative for a violation test)."""
    Dstar = cube.final_segment(N)
    r = cube.rho(Dstar).astype(float)[None, :]
    def stats(c):
        g = -np.minimum(c[:, None], u * r)
        w = np.exp(-g)
        Z = w.sum(axis=1)
        return Z, (w * g).sum(axis=1) / Z
    cmax = np.full(len(U0s), u * r.max())
    Zc, Uc = stats(cmax)
    lo = np.zeros(len(U0s)); hi = cmax.copy()
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        Um = stats(mid)[1]
        up = Um > U0s
        lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    Zlo = stats(lo)[0]           # level slightly too shallow: mean energy > U0, Z(lo) <= Zpl
    full = Uc >= U0s
    return np.where(full, Zc, Zlo)


def part_C(quick):
    print("== C: exhaustive grid of general members (dips and hills), vanishing at vertex 0 ==")
    ok = True
    for (n, q) in (((3, 4), (4, 2)) if not quick else ((3, 2), (4, 1))):
        cube = Cube(n)
        half = cube.N // 2 + (2 if n == 4 else 0)
        order, posn, P = grid_partial(cube, q, half)
        us = (0.6, 1.0, 2.5)
        stat = {u: dict(ntest=0, nviol=0, worst=-np.inf, att=0, pos=0) for u in us}
        total = 0
        chunk = 4000
        cols = [posn[v] for v in range(cube.N)]
        for a in range(0, len(P), chunk):
            F = extend(cube, q, order, posn, P[a:a + chunk], half, cube.N)[:, cols]
            total += len(F)
            Nsup = (F != 0).sum(axis=1)
            for u in us:
                g = F.astype(float) * (u / q)
                w = np.exp(-g)
                Z = w.sum(axis=1)
                U = (w * g).sum(axis=1) / Z
                st = stat[u]
                pos = U > 0
                st["pos"] += int(pos.sum())
                st["nviol"] += int((Z[pos] > cube.N * (1 + 1e-12)).sum()); st["ntest"] += int(pos.sum())
                for N in range(1, cube.N):
                    sel = (~pos) & (Nsup == N)
                    if not sel.any(): continue
                    Zpl = zpl_batch(cube, N, U[sel], u)
                    rel = (Z[sel] - Zpl) / Zpl
                    st["worst"] = max(st["worst"], float(rel.max()))
                    st["nviol"] += int((rel > 1e-9).sum()); st["ntest"] += int(sel.sum())
                    st["att"] += int((np.abs(rel) < 1e-9).sum())
        print(f"  Q_{n}, values in (u/{q})Z: {total} functions")
        for u in us:
            st = stat[u]
            print(f"     u={u}: tested {st['ntest']}; violations {st['nviol']}; largest (Z_g - Zpl)/Zpl = {st['worst']:+.2e}; "
                  f"members attaining the bound: {st['att']}; with U_g > 0: {st['pos']}")
            ok &= st["nviol"] == 0
    return ok


# ---------------------------------------------------------------- part D
def part_D(quick):
    print("== D: random general members with dips and hills on random supports ==")
    tot = 0; nviol = 0; worst = -np.inf; nhill = 0
    for n in ((5, 6, 7, 8, 9, 10) if not quick else (5, 7)):
        cube = Cube(n)
        x = np.arange(cube.N)
        for rep in range(150 if not quick else 30):
            u = float(rng.choice([0.5, 1.0, 2.0, 3.0]))
            N = int(rng.integers(1, max(2, cube.N // int(rng.choice([2, 4, 8])))))
            kind = rng.integers(0, 3)
            if kind == 0:
                D = np.zeros(cube.N, dtype=bool); D[rng.choice(cube.N, N, replace=False)] = True
            elif kind == 1:
                c = int(rng.integers(0, cube.N))
                order = np.lexsort((rng.random(cube.N), cube.dist[c]))
                D = np.zeros(cube.N, dtype=bool); D[order[:N]] = True
            else:
                c = int(rng.integers(0, cube.N)); c2 = int(rng.integers(0, cube.N))
                sc = cube.dist[c] + 0.7 * cube.dist[c2] + 0.3 * rng.random(cube.N)
                D = np.zeros(cube.N, dtype=bool); D[np.argsort(sc)[:N]] = True
            r = cube.rho(D).astype(float)
            # a random Lipschitz function clipped between -u rho and u rho  (median of three)
            psi = rng.normal(0, rng.choice([0.5, 2.0, 8.0]) * u, cube.N) - rng.uniform(0, 3) * u
            for i in range(n):
                psi = np.minimum(psi, psi[x ^ (1 << i)] + u)
            if rng.random() < 0.3:
                psi = -psi
            g = np.maximum(-u * r, np.minimum(psi, u * r))
            assert max(np.max(np.abs(g - g[x ^ (1 << i)])) for i in range(n)) <= u + 1e-12
            w = np.exp(-g); Z = w.sum(); U = float((w * g).sum() / Z)
            Nsup = int((g != 0).sum())
            tot += 1
            if Nsup == 0: continue
            nhill += int((g > 0).any())
            if U > 0:
                bad = Z > cube.N * (1 + 1e-12)
            else:
                Zpl = plateau_Z(cube, cube.final_segment(Nsup), U, u)[0]
                worst = max(worst, (Z - Zpl) / Zpl)
                bad = Z > Zpl * (1 + 1e-9)
            nviol += int(bad)
    print(f"  members {tot} ({nhill} with hills): violations {nviol}; largest (Z_g - Zpl)/Zpl = {worst:+.2e}")
    return nviol == 0


# ---------------------------------------------------------------- part E
def part_E():
    print("== E: mutations ==")
    cube = Cube(4)
    u = 1.0
    # (1) the bound taken from the plateau on a subcube of the same size instead of D*
    N = 8
    Dstar = cube.final_segment(N)
    sub = np.array([(x >> 3) & 1 == 1 for x in range(cube.N)])
    r = cube.rho(Dstar).astype(float); gc = -u * r; wc = np.exp(-gc); Ucone = float((wc * gc).sum() / wc.sum())
    U0 = 0.97 * Ucone
    Zsub = plateau_Z(cube, sub, U0, u)[0]
    UB, LB, _ = solve_convex(cube, Dstar, U0, u)
    m1 = LB > Zsub * (1 + 1e-9)
    print(f"  (1) bound taken from a subcube of 8 points: {Zsub:.6f}; best member on D*: {LB:.6f} -> violation detected: {m1}")
    # (2) drop the energy constraint: optimum is the full cone, larger than Zpl
    U0 = 0.5 * Ucone
    Zpl = plateau_Z(cube, Dstar, U0, u)[0]
    Zcone = wc.sum()
    m2 = Zcone > Zpl * (1 + 1e-9)
    print(f"  (2) without the energy constraint: full cone {Zcone:.6f} > Zpl {Zpl:.6f}: {m2}")
    # (3) the solver finds a violation when the comparison value is taken at a higher energy bound
    Zpl_wrong = plateau_Z(cube, Dstar, 0.3 * Ucone, u)[0]
    UB, LB, _ = solve_convex(cube, Dstar, 0.5 * Ucone, u)
    m3 = LB > Zpl_wrong * (1 + 1e-9)
    print(f"  (3) comparison value at the wrong energy: {Zpl_wrong:.6f} < best member {LB:.6f}: {m3}")
    return m1 and m2 and m3


if __name__ == "__main__":
    args = sys.argv[1:]
    quick = "quick" in args
    parts = [a for a in args if a in "ABCDE"] or list("ABCDE")
    t0 = time.time()
    res = {}
    fn = {"A": lambda: part_A(quick), "B": lambda: part_B(quick), "C": lambda: part_C(quick),
          "D": lambda: part_D(quick), "E": part_E}
    for p_ in parts:
        res[p_] = bool(fn[p_]()); print(f"   [{time.time()-t0:.0f}s]", flush=True)
    print("SUMMARY", res, f" time {time.time()-t0:.0f}s")
    sys.exit(0 if all(res.values()) else 1)
