#!/usr/bin/env python3
"""R19, item 4: Part A of docs/science/ASSUMPTION_AUDIT.md tested with my own code (no code of the division is imported).

 S1  Proposition AA.1 / Corollary AA.2 (obligation G-1) on synthetic energies that are NOT generalised Born,
     g(x) = sum_p phi_p(c_p + sum_i a_{p,i}(x_i)), every state enumerated: the bound M_m e_m(delta) at every state, for every
     term and for the sum; tightness; controls that must fail (M_m halved; M_m replaced by the supremum of the derivative
     of order m - 1; M_m replaced by |phi^(m)| at the anchor's value of u instead of its supremum over the hull).
 S2  Vector-valued statistics (r = 2): the bound with a consistent pair of norms; control: the norm of the increments and
     the operator norm of D^m phi taken with respect to different norms.
 S3  The remainder identity with its contexts z^{T,x} (A2), for random functions and random orders of the sites, and the
     bound of AA.1 for every single term Delta_T(phi o u)(z^{T,x}; x_T) with a context that is not the anchor.
 S4  G-1, second half: <e_m(delta)> under a band model by a transfer matrix with polynomial entries truncated at degree m,
     against enumeration.
 S5  Level H2' (obligation G-2): a band model plus phi(u(x)), u one site-additive statistic: a transfer matrix that
     carries the partial sum on a grid; floor and ceiling; the allowance; against enumeration; control: the allowance of
     ONE cell instead of the accumulated one.  Comparison with the envelope bracket of level H3 on the same instance.
 S6  A8: the growth comparison on an exchangeable instance: the "cost" of displacing s sites in the floor is a polynomial
     of degree m - 1 in s (not linear); where the floor leaves the anchor.
 S7  Classifications: A1 (a ceiling that is finite and wrong outside a region: the lower end is false; +infinity there:
     true); A6 (non-negative group slacks: counterexamples for (LP), (UP) and (UE), each with its control); A3 (m against
     the number of hosts: with two hosts and m = 2 the remainder does not vanish when no additive statistic moves).

Run: python3 -B r19_audit_tests.py [seed] > r19_audit_tests.log
"""
import sys, math, itertools, time, resource
import numpy as np
t00 = time.time(); SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 19


def all_states(k):
    return np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, len(k))


def lnz(e, beta=1.0):
    e = np.asarray(e, dtype=float); m = e.min(); return float(-beta * m + math.log(np.exp(-beta * (e - m)).sum()))


def interpolant(G, x0, M):
    """I_M G on the full grid (G: array over all states), by my own anchored differencing: sum over |U| <= M of d_U."""
    n = G.ndim; out = np.zeros_like(G, dtype=float)
    for s in range(M + 1):
        for U in itertools.combinations(range(n), s):
            idx = tuple(slice(None) if i in U else x0[i] for i in range(n)); dd = np.array(G[idx], dtype=float)
            for a, u in enumerate(U): dd = dd - np.take(dd, [x0[u]], axis=a)
            out = out + dd.reshape([G.shape[i] if i in U else 1 for i in range(n)])
    return out


def esym(delta, m):
    """e_0..e_m of (delta_1(x_1), ..., delta_n(x_n)) at every state: list of arrays over the full grid. delta: list of 1-d arrays."""
    n = len(delta); shape = [len(v) for v in delta]; E = [np.ones(shape)] + [np.zeros(shape) for _ in range(m)]
    for i in range(n):
        di = delta[i].reshape([shape[i] if j == i else 1 for j in range(n)])
        for j in range(m, 0, -1): E[j] = E[j] + di * E[j - 1]
    return E


# ------------------------------------------------------------------ families of scalar functions with exact derivative suprema on an interval
class Exp:
    def __init__(s, A, lam): s.A, s.lam = A, lam; s.name = f"{A:+.2f} exp({lam:+.2f} u)"
    def val(s, u): return s.A * np.exp(s.lam * u)
    def d(s, j, u): return s.A * s.lam ** j * np.exp(s.lam * u)
    def dsup(s, j, lo, hi): return abs(s.A) * abs(s.lam) ** j * math.exp(max(s.lam * lo, s.lam * hi))


class Sin:
    def __init__(s, A, om, th): s.A, s.om, s.th = A, om, th; s.name = f"{A:+.2f} sin({om:.2f} u {th:+.2f})"
    def val(s, u): return s.A * np.sin(s.om * u + s.th)
    def d(s, j, u): return s.A * s.om ** j * np.sin(s.om * u + s.th + j * math.pi / 2)
    def dsup(s, j, lo, hi):
        a, b = s.om * lo + s.th + j * math.pi / 2, s.om * hi + s.th + j * math.pi / 2
        kk = math.ceil((a - math.pi / 2) / math.pi)                                    # is there a point pi/2 + k pi in [a, b]?
        top = 1.0 if math.pi / 2 + kk * math.pi <= b else max(abs(math.sin(a)), abs(math.sin(b)))
        return abs(s.A) * s.om ** j * top


class Pow:                                                                             # A (c + u)^(-sg), c + u > 0 on the hull: "Born-like", but not a Born term
    def __init__(s, A, c, sg): s.A, s.c, s.sg = A, c, sg; s.name = f"{A:+.2f} ({c:.2f} + u)^(-{sg})"
    def _r(s, j): return math.prod(s.sg + i for i in range(j))
    def val(s, u): return s.A * (s.c + u) ** (-s.sg)
    def d(s, j, u): return s.A * (-1) ** j * s._r(j) * (s.c + u) ** (-s.sg - j)
    def dsup(s, j, lo, hi): assert s.c + lo > 0; return abs(s.A) * s._r(j) * (s.c + lo) ** (-s.sg - j)


class Mono:
    def __init__(s, A, q): s.A, s.q = A, q; s.name = f"{A:+.2f} u^{q}"
    def _f(s, j): return math.factorial(s.q) / math.factorial(s.q - j) if j <= s.q else 0.0
    def val(s, u): return s.A * u ** s.q
    def d(s, j, u): return s.A * s._f(j) * u ** (s.q - j) if j <= s.q else 0.0 * u
    def dsup(s, j, lo, hi): return abs(s.A) * s._f(j) * max(abs(lo), abs(hi)) ** (s.q - j) if j <= s.q else 0.0


def random_phi(rng, lo, hi):
    """a random member of the four families, valid on [lo, hi]."""
    t = int(rng.integers(4)); A = float(rng.choice([-1, 1]) * rng.uniform(0.3, 2.0))
    if t == 0: return Exp(A, float(rng.choice([-1, 1]) * rng.uniform(0.4, 2.5)))
    if t == 1: return Sin(A, float(rng.uniform(1.2, 4.0)), float(rng.uniform(0, 6.28)))
    if t == 2: return Pow(A, float(-lo + rng.uniform(0.3, 1.5)), int(rng.integers(1, 3)) * 0.5)
    return Mono(A, int(rng.integers(2, 7)))


def S1(rng, ninst=300):
    print("S1  Corollary AA.2 on synthetic energies g = sum_p phi_p(c_p + sum_i a_{p,i}(x_i)) (families: exp, sin, (c+u)^(-s), u^q); every state; anchor = a random state")
    res = {m: dict(inst=0, states=0, viol=0, viol_term=0, viol_crude=0, viol_T=0, nT=0, half=0, half_inst=0, lower=0, lower_inst=0, lower_live=0, anch=0, anch_inst=0,
                   tight_min=[], tight_med=[], attained=0.0) for m in (2, 3, 4, 5)}
    for it in range(ninst):
        n = int(rng.integers(4, 8)); k = [int(v) for v in rng.integers(2, 5, n)]
        while np.prod(k) > 6000: k[int(rng.integers(n))] = 2
        x0 = [int(rng.integers(v)) for v in k]; X = all_states(k); P = int(rng.integers(1, 6))
        terms = []
        for p in range(P):
            sc = float(rng.choice([0.05, 0.2, 0.6])); a = [rng.normal(0, sc, v) for v in k]; c = float(rng.normal())
            lo = c + sum(v.min() for v in a); hi = c + sum(v.max() for v in a)
            terms.append((random_phi(rng, lo, hi), c, a, lo, hi))
        gp = []
        for phi, c, a, lo, hi in terms:
            u = c + sum(a[i][X[:, i]] for i in range(n)); assert u.min() >= lo - 1e-12 and u.max() <= hi + 1e-12
            gp.append(phi.val(u).reshape(k))
        g = sum(gp)
        for m in (2, 3, 4, 5):
            if m > n: continue
            R = res[m]; R["inst"] += 1; R["states"] += len(X)
            rp = [G - interpolant(G, x0, m - 1) for G in gp]; r = g - interpolant(g, x0, m - 1)
            assert abs(float((sum(rp) - r).max())) < 1e-9
            B = np.zeros(k); Bh = np.zeros(k); Bl = np.zeros(k); Ba = np.zeros(k); Bc = np.zeros(k); scale = max(1.0, float(np.abs(g).max()))
            for (phi, c, a, lo, hi), rpp in zip(terms, rp):
                delta = [np.abs(a[i] - a[i][x0[i]]) for i in range(n)]; em = esym(delta, m)[m]
                Mm = phi.dsup(m, lo, hi); Ml = phi.dsup(m - 1, lo, hi); u0 = c + sum(a[i][x0[i]] for i in range(n)); Ma = abs(float(phi.d(m, u0)))
                bt = Mm * em; R["viol_term"] += int((np.abs(rpp) > bt * (1 + 1e-9) + 1e-11 * scale).sum())
                B += bt; Bh += 0.5 * bt; Bl += Ml * em; Ba += Ma * em
                Bc += Mm * esym(delta, 1)[1] ** m / math.factorial(m)
            tol = 1e-11 * scale
            R["viol"] += int((np.abs(r) > B * (1 + 1e-9) + tol).sum()); R["viol_crude"] += int((np.abs(r) > Bc * (1 + 1e-9) + tol).sum())
            vh = int((np.abs(r) > Bh * (1 + 1e-9) + tol).sum()); R["half"] += vh; R["half_inst"] += int(vh > 0)
            vl = int((np.abs(r) > Bl * (1 + 1e-9) + tol).sum()); R["lower"] += vl; R["lower_inst"] += int(vl > 0); R["lower_live"] += int(float((Bl - B).min()) < 0)
            va = int((np.abs(r) > Ba * (1 + 1e-9) + tol).sum()); R["anch"] += va; R["anch_inst"] += int(va > 0)
            off = (X != np.array(x0)[None]).sum(1).reshape(k)
            sel = (np.abs(r) > 1e-9 * scale) & (B > 0)
            if sel.any():
                q = (B[sel] / np.abs(r[sel])); R["tight_min"].append(float(q.min())); R["tight_med"].append(float(np.median(q))); R["attained"] = max(R["attained"], float(1 / q.min()))
            # the statement for one subset T: at states with exactly m sites off, r is Delta_T at the anchor's context
            sT = off == m; R["nT"] += int(sT.sum()); R["viol_T"] += int((np.abs(r[sT]) > B[sT] * (1 + 1e-9) + tol).sum())
    for m, R in res.items():
        print(f"    m = {m}: {R['inst']} instances, {R['states']} states: violations of |g - I_(m-1) g| <= sum_p M_m e_m(delta_p): {R['viol']}; term by term: {R['viol_term']}; of the cruder (sum delta)^m / m!: {R['viol_crude']}; "
              f"at the {R['nT']} states with exactly m sites off (one subset): {R['viol_T']}.  Tightness bound/|remainder|: smallest over all states and instances {min(R['tight_min']):.3f} "
              f"(the bound is attained to {100 * R['attained']:.1f} %), median of the per-instance minima {np.median(R['tight_min']):.2f}, median of the per-instance medians {np.median(R['tight_med']):.1f}")
        print(f"           controls: M_m halved: {R['half']} violations in {R['half_inst']} of {R['inst']} instances; M_m -> sup of the derivative of order m-1: {R['lower']} violations in {R['lower_inst']} instances "
              f"(the control is smaller than the bound somewhere in {R['lower_live']} instances); M_m -> |phi^(m)(u(x0))|: {R['anch']} violations in {R['anch_inst']} instances")
    # an instance built to be tight: one term, small increments, phi = exp: the bound is attained to first order
    n, k, x0 = 6, [3] * 6, [0] * 6; X = all_states(k); a = [np.array([0.0, 0.01 * (i + 1), 0.02]) for i in range(n)]; phi = Exp(1.0, 2.0)
    u = sum(a[i][X[:, i]] for i in range(n)); G = phi.val(u).reshape(k); lo, hi = 0.0, float(u.max())
    for m in (2, 3, 4):
        r = G - interpolant(G, x0, m - 1); em = esym([np.abs(v - v[0]) for v in a], m)[m]; B = phi.dsup(m, lo, hi) * em; sel = B > 0
        print(f"    tight instance (exp(2u), increments <= 0.06 in all): m = {m}: violations {int((np.abs(r) > B * (1 + 1e-9) + 1e-13).sum())}; bound/|remainder| between {float((B[sel] / np.abs(r[sel])).min()):.4f} and "
              f"{float((B[sel] / np.abs(r[sel])).max()):.4f}; with M_m halved: {int((np.abs(r) > 0.5 * B + 1e-13).sum())} violations of {int(sel.sum())} states with a non-zero bound; "
              f"with M_m -> M_(m-1): {int((np.abs(r) > phi.dsup(m - 1, lo, hi) * em + 1e-13).sum())}")


def S2(rng, ninst=200):
    print("S2  vector-valued statistics, r = 2: phi(u) = psi_1(u_1) psi_2(u_2); the l1 operator norm of D^m phi is max_j |psi_1^(j) psi_2^(m-j)| (suprema over the bounding rectangle of the hull)")
    for m in (2, 3, 4):
        v1 = v2 = v3 = st = 0; i3 = 0; inst = 0
        for it in range(ninst):
            n = int(rng.integers(max(4, m), 7)); k = [int(v) for v in rng.integers(2, 4, n)]; x0 = [int(rng.integers(v)) for v in k]; X = all_states(k)
            sc = float(rng.choice([0.1, 0.4])); a1 = [rng.normal(0, sc, v) for v in k]; a2 = [rng.normal(0, sc, v) for v in k]; c1, c2 = float(rng.normal()), float(rng.normal())
            lo1, hi1 = c1 + sum(v.min() for v in a1), c1 + sum(v.max() for v in a1); lo2, hi2 = c2 + sum(v.min() for v in a2), c2 + sum(v.max() for v in a2)
            p1, p2 = random_phi(rng, lo1, hi1), random_phi(rng, lo2, hi2)
            u1 = c1 + sum(a1[i][X[:, i]] for i in range(n)); u2 = c2 + sum(a2[i][X[:, i]] for i in range(n)); G = (p1.val(u1) * p2.val(u2)).reshape(k)
            r = G - interpolant(G, x0, m - 1); M1 = max(p1.dsup(j, lo1, hi1) * p2.dsup(m - j, lo2, hi2) for j in range(m + 1))
            d1 = [np.abs(a1[i] - a1[i][x0[i]]) + np.abs(a2[i] - a2[i][x0[i]]) for i in range(n)]; d2 = [np.hypot(a1[i] - a1[i][x0[i]], a2[i] - a2[i][x0[i]]) for i in range(n)]
            B11 = M1 * esym(d1, m)[m]; B12 = M1 * esym(d2, m)[m]; B22 = 2 ** (m / 2) * M1 * esym(d2, m)[m]; tol = 1e-11 * max(1.0, float(np.abs(G).max()))
            v1 += int((np.abs(r) > B11 * (1 + 1e-9) + tol).sum()); v2 += int((np.abs(r) > B22 * (1 + 1e-9) + tol).sum()); w3 = int((np.abs(r) > B12 * (1 + 1e-9) + tol).sum()); v3 += w3; i3 += int(w3 > 0); st += len(X); inst += 1
        print(f"    m = {m}: {inst} instances, {st} states: violations with (l1 increments, l1 operator norm): {v1}; with (Euclidean increments, 2^(m/2) x l1 operator norm >= Euclidean operator norm): {v2}; "
              f"CONTROL (Euclidean increments with the l1 operator norm, an inconsistent pair): {v3} violations in {i3} instances")
    # a deterministic instance for the inconsistent pair: phi = (u_1 + u_2)^2 / 2, Hessian [[1, 1], [1, 1]]: l1 operator norm 1 (largest entry), Euclidean operator norm 2
    k = [2, 2]; X = all_states(k); a1 = [np.array([0.0, 1.0]), np.array([0.0, 1.0])]; a2 = [np.array([0.0, 1.0]), np.array([0.0, 1.0])]
    u1 = sum(a1[i][X[:, i]] for i in range(2)); u2 = sum(a2[i][X[:, i]] for i in range(2)); G = (0.5 * (u1 + u2) ** 2).reshape(k); r = G - interpolant(G, [0, 0], 1)
    print(f"    phi = (u_1 + u_2)^2 / 2 (Hessian all ones: l1 operator norm 1, Euclidean operator norm 2), two sites with increments (1, 1): remainder at (1, 1) = {float(r[1, 1]):.3f}; "
          f"(l1 increments 2, 2; l1 norm 1): bound 4 -- attained; (Euclidean increments sqrt2, sqrt2; Euclidean norm 2): bound 4 -- attained; "
          f"CONTROL (Euclidean increments with the l1 norm): bound 2 < {float(r[1, 1]):.0f}: violated: {2.0 < abs(float(r[1, 1]))}")


def S3(rng):
    print("S3  the remainder identity with its contexts z^(T,x) (statement A2), random functions, random orders of the sites; and AA.1 term by term with non-anchor contexts")
    worst = 0.0; nchk = 0; viol = 0; nterms = 0; tight = 0.0
    for it in range(12):
        n = int(rng.integers(4, 7)); k = [int(v) for v in rng.integers(2, 4, n)]; x0 = [int(rng.integers(v)) for v in k]; X = all_states(k); m = int(rng.integers(2, min(4, n) + 1))
        additive = it % 2 == 1
        if additive:
            a = [rng.normal(0, 0.3, v) for v in k]; c = float(rng.normal()); lo = c + sum(v.min() for v in a); hi = c + sum(v.max() for v in a); phi = random_phi(rng, lo, hi)
            F = phi.val(c + sum(a[i][X[:, i]] for i in range(n))).reshape(k); Mm = phi.dsup(m, lo, hi)
        else:
            F = rng.normal(0, 1, k)
        order = [int(v) for v in rng.permutation(n)]; rank = {s: q for q, s in enumerate(order)}          # order[0] is the first site
        lhs = F - interpolant(F, x0, m - 1); rhs = np.zeros(k)
        for x in X:
            S = [i for i in range(n) if x[i] != x0[i]]; tot = 0.0
            for T in itertools.combinations(S, m):
                first = min(rank[i] for i in T); z = [int(x[i]) if rank[i] < first else x0[i] for i in range(n)]
                dT = 0.0
                for q in range(m + 1):
                    for V in itertools.combinations(T, q):
                        y = list(z)
                        for i in V: y[i] = int(x[i])
                        dT += (-1) ** (m - q) * F[tuple(y)]
                tot += dT
                if additive:
                    bT = Mm * math.prod(abs(a[i][x[i]] - a[i][x0[i]]) for i in T); nterms += 1; viol += int(abs(dT) > bT * (1 + 1e-9) + 1e-12)
                    if bT > 0: tight = max(tight, abs(dT) / bT)
            rhs[tuple(x)] = tot
        worst = max(worst, float(np.abs(lhs - rhs).max()) / max(1.0, float(np.abs(F).max()))); nchk += len(X)
    print(f"    12 instances, {nchk} states: largest relative difference between F - I_(m-1) F and the sum of the mixed differences in their contexts: {worst:.1e}; "
          f"AA.1 for every single term with its context ({nterms} terms): violations {viol}; largest |Delta_T| / (M_m prod delta) = {tight:.3f}")


# ------------------------------------------------------------------ a small band model of my own, with a polynomial / grid axis
class Band:
    """terms: list of (sites sorted tuple, table); all within a band w (max - min <= w)."""

    def __init__(s, rng, n, k, w, scale=1.0):
        s.n, s.k, s.w = n, k, w; s.terms = []
        for i in range(n): s.terms.append(((i,), rng.normal(0, scale, k[i])))
        for i in range(n):
            for j in range(i + 1, min(i + w, n - 1) + 1):
                if rng.random() < 0.8: s.terms.append(((i, j), rng.normal(0, scale, (k[i], k[j]))))
        if w >= 2:
            for i in range(n - 2):
                if rng.random() < 0.5: s.terms.append(((i, i + 1, i + 2), rng.normal(0, 0.5 * scale, (k[i], k[i + 1], k[i + 2]))))

    def energy(s, X):
        e = np.zeros(len(X))
        for U, t in s.terms: e += t[tuple(X[:, u] for u in U)]
        return e

    def poly_sum(s, beta, site_poly, deg):
        """sum over all states of exp(-beta energy) prod_i P_i(x_i; t), truncated at degree deg, as the array of coefficients.
        site_poly[i][b] = list of (power, coefficient).  Variable elimination site by site; scopes stay within w + 1 sites."""
        n, k = s.n, s.k; msg = np.zeros((deg + 1,)); msg[0] = 1.0; scope = []                         # msg axes: scope sites..., degree
        for t in range(n):
            new_scope = sorted(set(scope) | {t} | {u for U, _ in s.terms if min(U) == t for u in U})
            assert new_scope[0] == t and new_scope[-1] - t <= s.w
            A = msg.reshape([k[u] if u in scope else 1 for u in new_scope] + [deg + 1]) * np.ones([k[u] for u in new_scope] + [1])
            for U, tab in s.terms:
                if min(U) == t:
                    A = A * np.exp(-beta * tab).reshape([k[u] if u in U else 1 for u in new_scope] + [1])
            out = np.zeros(A.shape[1:])
            for b in range(k[t]):
                for pw_, cf in site_poly[t][b]:
                    if pw_ > deg: continue
                    if pw_ == 0: out += cf * A[b]
                    else: out[..., pw_:] += cf * A[b][..., :deg + 1 - pw_]
            msg = out; scope = new_scope[1:]
        assert msg.shape == (deg + 1,)
        return msg


def S4(rng, ninst=200):
    print("S4  <e_j(delta)> under a band model by a transfer matrix with polynomial entries truncated at degree m (G-1, second half), against enumeration")
    worst = 0.0; nst = 0
    for it in range(ninst):
        n = int(rng.integers(4, 9)); w = int(rng.integers(1, 4)); k = [int(v) for v in rng.integers(2, 4, n)]; beta = float(rng.choice([0.5, 1.0, 2.0])); mdl = Band(rng, n, k, w)
        X = all_states(k); e = mdl.energy(X); wg = np.exp(-beta * (e - e.min())); wg /= wg.sum(); m = int(rng.integers(2, 6))
        delta = [np.abs(rng.normal(0, 0.5, v)) * (np.arange(v) != int(rng.integers(v))) for v in k]
        coef = mdl.poly_sum(beta, [[[(0, 1.0), (1, float(delta[i][b]))] for b in range(k[i])] for i in range(n)], m)
        E = esym(delta, m)
        for j in range(m + 1):
            ex = float(wg @ E[j].reshape(-1)); got = coef[j] / coef[0]; worst = max(worst, abs(ex - got) / max(abs(ex), 1e-300)); nst += 1
        worst = max(worst, abs(math.log(coef[0]) - lnz(e, beta)))
    print(f"    {ninst} random band models (4-8 sites, band 1-3, pair and triple terms), degrees 0..m, m in 2..5: {nst} means, largest relative deviation from enumeration (and of ln Z): {worst:.1e}")
    # control: truncation one degree too low loses the top coefficient; a wrong recurrence (delta added, not multiplied) is not tested -- the comparison above is the test
    n, w, k = 6, 2, [3] * 6; mdl = Band(rng, n, k, w); X = all_states(k); e = mdl.energy(X); wg = np.exp(-(e - e.min())); wg /= wg.sum()
    delta = [np.array([0.0, 0.3, 0.7])] * n; E = esym(delta, 3); c3 = mdl.poly_sum(1.0, [[[(0, 1.0), (1, float(delta[i][b]))] for b in range(3)] for i in range(n)], 3)
    indep = [float(wg @ (delta[i][X[:, i]])) for i in range(n)]; prod_form = esym([np.array([v]) for v in indep], 3)[3].item()
    print(f"    control (must differ): <e_3(delta)> exact {float(wg @ E[3].reshape(-1)):.6f}, transfer matrix {c3[3] / c3[0]:.6f}; the product-measure formula e_3(<delta_i>) = {prod_form:.6f} (correlations ignored)")


def S5(rng, ninst=120):
    print("S5  level H2' (G-2): band model + phi(u(x)), u = c + sum_i a_i(x_i) one statistic; increments rounded to a grid of cell h; the transfer matrix carries the gridded partial sum (my code)")
    print("    floor/ceiling: phi(u~) -/+ Lip x rho, rho = sum_i max_b |a_i(b) - a~_i(b)| <= n h / 2 (the accumulated rounding); width = 2 beta Lip rho <= beta Lip n h.  Control: allowance of one cell, Lip x h / 2")
    rows = {}
    for it in range(ninst):
        n = int(rng.integers(5, 10)); w = int(rng.integers(1, 3)); k = [int(v) for v in rng.integers(2, 4, n)]; beta = float(rng.choice([1.0, 2.0])); mdl = Band(rng, n, k, w)
        while np.prod(k) > 40000: k[int(rng.integers(n))] = 2
        mdl = Band(rng, n, k, w); X = all_states(k); a = [rng.normal(0, 0.5, v) for v in k]; c = float(rng.normal()); lo = c + sum(v.min() for v in a); hi = c + sum(v.max() for v in a)
        phi = Sin(float(rng.uniform(0.5, 3.0)), float(rng.uniform(0.8, 3.0)), float(rng.uniform(0, 6.28))) if it % 2 == 0 else Exp(float(rng.uniform(0.3, 1.5)), float(rng.choice([-1, 1]) * rng.uniform(0.3, 1.2)))
        u = c + sum(a[i][X[:, i]] for i in range(n)); eb = mdl.energy(X); exact = lnz(eb + phi.val(u), beta)
        for nb in (8, 32, 128, 512):
            h = (hi - lo) / nb; q = [np.rint(a[i] / h).astype(int) for i in range(n)]; qmin = [int(v.min()) for v in q]
            rho = sum(float(np.abs(a[i] - h * q[i]).max()) for i in range(n)); B = sum(int(v.max() - v.min()) for v in q) + 1
            Zs = mdl.poly_sum(beta, [[[(int(q[i][b] - qmin[i]), 1.0)] for b in range(k[i])] for i in range(n)], B - 1)
            ugrid = c + h * (sum(qmin) + np.arange(B))
            Lip = phi.dsup(1, lo - rho, hi + rho)
            def lz(en):
                keep = Zs > 0; ee = -beta * en[keep] + np.log(Zs[keep]); mx = ee.max(); return float(mx + math.log(np.exp(ee - mx).sum()))
            lo_end, up_end = lz(phi.val(ugrid) + Lip * rho), lz(phi.val(ugrid) - Lip * rho)
            lo_c, up_c = lz(phi.val(ugrid) + Lip * h / 2), lz(phi.val(ugrid) - Lip * h / 2)
            # sharper: the extreme values of phi on the cell [u~ - rho, u~ + rho] (dense sampling of the cell plus the Lipschitz allowance of the sampling step)
            ss = np.linspace(-rho, rho, 41); vals = phi.val(ugrid[:, None] + ss[None, :]); step = 2 * rho / 40
            lo_x, up_x = lz(vals.max(1) + Lip * step / 2), lz(vals.min(1) - Lip * step / 2)
            R = rows.setdefault(nb, dict(n=0, bad=0, badx=0, ctrl=0, width=[], widthx=[], ratio=[], B=[], gridcheck=0.0))
            R["n"] += 1; R["bad"] += int(not (lo_end - 1e-10 <= exact <= up_end + 1e-10)); R["badx"] += int(not (lo_x - 1e-10 <= exact <= up_x + 1e-10)); R["ctrl"] += int(not (lo_c <= exact <= up_c))
            R["width"].append(up_end - lo_end); R["widthx"].append(up_x - lo_x); R["ratio"].append((up_end - lo_end) / (beta * Lip * n * h)); R["B"].append(B)
            # the gridded law itself against enumeration
            ut = np.rint((sum(h * q[i][X[:, i]] for i in range(n)) - h * sum(qmin)) / h).astype(int); hist = np.bincount(ut, weights=np.exp(-beta * eb), minlength=B)
            R["gridcheck"] = max(R["gridcheck"], float(np.abs(hist - Zs).max() / hist.max()))
    for nb, R in rows.items():
        print(f"    range/h = {nb}: {R['n']} instances; grid values B: median {int(np.median(R['B']))}, largest {max(R['B'])}; exact ln Z outside [ceiling, floor]: {R['bad']} (Lipschitz allowance), {R['badx']} (extreme values on the cell); "
              f"width: median {np.median(R['width']):.3g} (Lipschitz), {np.median(R['widthx']):.3g} (extremes); width / (beta Lip n h): median {np.median(R['ratio']):.3f}, largest {max(R['ratio']):.3f}; "
              f"CONTROL allowance of one cell: exact ln Z outside in {R['ctrl']} instances; gridded law against enumeration: {R['gridcheck']:.1e}")
    # ---- the allowance must accumulate: every increment 0.49 h above a grid point, phi linear (Lipschitz constant lam): u - u~ = 0.49 n h at EVERY state
    for n in (2, 4, 8):
        k = [2] * n; mdl = Band(rng, n, k, 1); X = all_states(k); h = 0.1; lam = 1.0; beta = 1.0; a = [h * (np.array([0.0, 3.0]) + 0.49) for _ in range(n)]
        u = sum(a[i][X[:, i]] for i in range(n)); exact = lnz(mdl.energy(X) + lam * u, beta); q = [np.rint(v / h).astype(int) for v in a]; ut = sum(h * q[i][X[:, i]] for i in range(n)); zt = lnz(mdl.energy(X) + lam * ut, beta)
        rho = sum(float(np.abs(a[i] - h * q[i]).max()) for i in range(n))
        print(f"    sharpness, n = {n}: exact ln Z = {exact:.6f}; gridded model {zt:.6f}; with the allowance of one cell [{zt - beta * lam * h / 2:.6f}, {zt + beta * lam * h / 2:.6f}] contains it: {zt - beta * lam * h / 2 <= exact <= zt + beta * lam * h / 2}; "
              f"with the accumulated allowance rho = {rho:.3f} = 0.49 n h: [{zt - beta * lam * rho:.6f}, {zt + beta * lam * rho:.6f}] contains it: {zt - beta * lam * rho - 1e-12 <= exact <= zt + beta * lam * rho + 1e-12} (attained at the lower end)")
    # ---- H2' against the envelope bracket of H3 on one instance: few statistics against many sites off the anchor
    n, w, k = 9, 2, [3] * 9; mdl = Band(rng, n, k, w, scale=0.3); X = all_states(k); a = [np.array([0.0, 0.25, -0.2]) * (1 + 0.1 * i) for i in range(n)]; c = 0.3; beta = 1.0
    phi = Sin(1.0, 1.5, 0.4); u = c + sum(a[i][X[:, i]] for i in range(n)); eb = mdl.energy(X); g = phi.val(u).reshape(k); E = eb + g.reshape(-1); exact = lnz(E, beta)
    wg = np.exp(-beta * (E - E.min())); wg /= wg.sum(); x0 = [0] * n; lo, hi = c + sum(v.min() for v in a), c + sum(v.max() for v in a)
    print(f"    one instance, 9 sites x 3 states ({len(X)} states), g = sin(1.5 u + 0.4), mean number of sites off the anchor in the true ensemble {float(wg @ (X != 0).sum(1)):.2f}, exact ln Z = {exact:.6f}")
    delta = [np.abs(v - v[0]) for v in a]
    for m in (2, 3, 4, 5, 6):
        I = interpolant(g, x0, m - 1); env = phi.dsup(m, lo, hi) * esym(delta, m)[m]; assert (np.abs(g - I) <= env * (1 + 1e-9) + 1e-12).all()
        wd = lnz(eb + (I - env).reshape(-1), beta) - lnz(eb + (I + env).reshape(-1), beta); nball = sum(math.comb(n, s) * 2 ** s for s in range(m))
        print(f"      H3 at order m = {m}: ball of {nball} evaluations; bracket of the envelope itself (floor and ceiling by enumeration, no band reduction, no allocation): {wd:.4g} nats")
    for nb in (16, 64, 256, 1024):
        h = (hi - lo) / nb; q = [np.rint(v / h).astype(int) for v in a]; qmin = [int(v.min()) for v in q]; rho = sum(float(np.abs(a[i] - h * q[i]).max()) for i in range(n)); B = sum(int(v.max() - v.min()) for v in q) + 1
        Zs = mdl.poly_sum(beta, [[[(int(q[i][b] - qmin[i]), 1.0)] for b in range(3)] for i in range(n)], B - 1); ug = c + h * (sum(qmin) + np.arange(B)); Lip = phi.dsup(1, lo - rho, hi + rho)
        keep = Zs > 0; f_ = lambda en: float(np.log((Zs[keep] * np.exp(-beta * en[keep])).sum()))
        lo_e, up_e = f_(phi.val(ug) + Lip * rho), f_(phi.val(ug) - Lip * rho)
        print(f"      H2' with range/h = {nb} ({B} grid values, no evaluation of g on a ball: phi is evaluated at {B} grid values): [{lo_e:.6f}, {up_e:.6f}], width {up_e - lo_e:.4g}; contains the exact value: {lo_e <= exact <= up_e}")


def S6():
    print("S6  A8, the growth comparison, on an exchangeable instance: n two-state sites, u = delta x (number of displaced sites s), g = phi(u), known part f = c s; envelope M_m delta^m C(s, m)")
    for name, phi, dl in (("sin(2u), delta = 0.5", Sin(1.0, 2.0, 0.0), 0.5), ("exp(-u), delta = 0.5", Exp(1.0, -1.0), 0.5)):
        for m in (2, 3, 4):
            # the interpolant as a function of s: I_(m-1) g (s) = sum_{j<m} C(s, j) Delta^j phi(0)   (Newton's forward formula for an exchangeable function)
            def Dj(j): return sum((-1) ** (j - i) * math.comb(j, i) * float(phi.val(np.array(dl * i))) for i in range(j + 1))
            S = np.arange(0, 400); I = np.array([sum(math.comb(int(s), j) * Dj(j) for j in range(m)) for s in S], dtype=float)
            # check Newton's formula against my interpolant on a small grid
            nn = 8; X = all_states([2] * nn); G = phi.val(dl * X.sum(1)).reshape([2] * nn); Ichk = interpolant(G, [0] * nn, m - 1).reshape(-1); dev = max(abs(Ichk[q] - I[int(X[q].sum())]) for q in range(len(X)))
            # growth exponent of |I(s) - I(0)| between s = 100 and s = 399
            gI = np.abs(I - I[0]); expo = math.log(gI[399] / gI[100]) / math.log(399 / 100) if gI[100] > 0 and gI[399] > 0 else float('nan')
            out = []
            for cst in (0.5, 2.0):
                beta = 1.0; nstar = None; nstar_true = None
                for n in range(m, 400):
                    s = np.arange(n + 1); lw = np.array([math.lgamma(n + 1) - math.lgamma(v + 1) - math.lgamma(n - v + 1) for v in s])
                    Mm = phi.dsup(m, 0.0, dl * n); pen = Mm * dl ** m * np.array([math.comb(int(v), m) for v in s], dtype=float)
                    fl = cst * s + I[:n + 1] - pen; tr = cst * s + phi.val(dl * s)
                    assert (np.abs(phi.val(dl * s) - I[:n + 1]) <= pen * (1 + 1e-9) + 1e-9).all()
                    pf = lw - beta * fl; pf -= pf.max(); pf = np.exp(pf); pf /= pf.sum(); pt = lw - beta * tr; pt -= pt.max(); pt = np.exp(pt); pt /= pt.sum()
                    if nstar is None and float(pf @ s) > float(pt @ s) + 0.25 * n: nstar = n
                    if nstar is not None: break
                out.append(f"cost c = {cst}: the floor's mean number of displaced sites exceeds the true one by n/4 from n = {nstar}")
            print(f"    {name}, m = {m}: Newton's formula for I_(m-1) g against my interpolant on 8 sites: {dev:.1e}; |I_(m-1) g(s) - g(0)| grows like s^{expo:.2f} (the audit says the cost grows 'at most linearly'; the degree is m - 1 = {m - 1}); " + "; ".join(out))


def S6b():
    print("S6b A8 with a known part whose cost is NOT linear: f = c2 x C(s, 2) (every pair of displaced sites repels by c2), g = sin(2u), delta = 0.5 (M_m delta^m = 1, 1, 1 for m = 2, 3, 4)")
    phi = Sin(1.0, 2.0, 0.0); dl = 0.5; beta = 1.0
    for m in (2, 3, 4):
        def Dj(j): return sum((-1) ** (j - i) * math.comb(j, i) * float(phi.val(np.array(dl * i))) for i in range(j + 1))
        for c2 in (0.5, 2.0):
            worst_gap = 0.0; nstar = None
            for n in range(m, 201):
                s = np.arange(n + 1); lw = np.array([math.lgamma(n + 1) - math.lgamma(v + 1) - math.lgamma(n - v + 1) for v in s])
                I = np.array([sum(math.comb(int(v), j) * Dj(j) for j in range(m)) for v in s], dtype=float); pen = phi.dsup(m, 0.0, dl * n) * dl ** m * np.array([math.comb(int(v), m) for v in s], dtype=float)
                pair = c2 * np.array([math.comb(int(v), 2) for v in s], dtype=float); fl = pair + I - pen; tr = pair + phi.val(dl * s)
                def lz(e): ee = lw - beta * e; mx = ee.max(); return float(mx + math.log(np.exp(ee - mx).sum()))
                gap = lz(fl) - lz(tr); worst_gap = max(worst_gap, gap)
                if nstar is None and gap > 1.0: nstar = n
            print(f"    m = {m}, c2 = {c2}: ln Z(floor) - ln Z(E) exceeds one nat first at n = {nstar} (largest gap for n <= 200: {worst_gap:.3g} nats)")


def S7():
    print("S7  classifications")
    # A1: the ceiling
    E = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 5.0, 5.0, 0.2]); A = np.arange(10) <= 4; z = lnz(E)
    ceil_inf = np.where(A, E, np.inf); fin = np.isfinite(ceil_inf); lz_inf = lnz(ceil_inf[fin])
    ceil_bad = np.where(A, E, -1.0)                                                      # a finite 'ceiling' that is valid on the region A only (below E outside)
    ceil_ok = np.where(A, E, 7.0)                                                        # a finite ceiling valid everywhere
    print(f"    A1 (the example of aa01_essential.py (3), ten states, two modes; exact ln Z = {z:.6f}): ceiling = E on the first mode and +infinity elsewhere: lower end {lz_inf:.6f} <= ln Z: {lz_inf <= z};  "
          f"a FINITE model that is a ceiling on the first mode only (-1 elsewhere, below E): 'lower end' {lnz(ceil_bad):.6f} <= ln Z: {lnz(ceil_bad) <= z}  [must be False];  control, a finite ceiling valid everywhere: {lnz(ceil_ok):.6f} <= ln Z: {lnz(ceil_ok) <= z}")
    # A6: (LP), (UP), (UE) with a group slack that is negative somewhere
    b = 1.0; mhi = np.zeros(2); E2 = np.zeros(2); S1 = np.array([0.0, math.log(2.0)]); S2 = -S1; w = np.array([0.5, 0.5])
    LP = lnz(mhi) + math.log(1 + float(w @ (np.exp(S1) - 1)) + float(w @ (np.exp(S2) - 1)))
    # (UP): floor = E = ceiling, minus-groups S1, S2 (sum zero), plus-groups zero: C' = <e^S1 - 1> + <e^S2 - 1> = 1/4
    Cp = float(w @ (np.exp(S1) - 1)) + float(w @ (np.exp(S2) - 1)); v = lnz(E2); its = []
    for _ in range(60): v = lnz(E2) - math.log1p(Cp * math.exp(lnz(mhi) - v)); its.append(v)
    print(f"    A6 (LP), the audit's example: (LP) = {LP:.6f} > ln Z = {lnz(E2):.6f}: {LP > lnz(E2) + 1e-12}.   (UP), the same two groups as minus-slacks with m- = E = m+ (sum zero, hypothesis holds): C' = {Cp:.4f}, first iterate {its[0]:.6f}, "
          f"limit {its[-1]:.6f} < ln Z = {lnz(E2):.6f}: {its[-1] < lnz(E2) - 1e-12}  [the formula is violated]")
    Cp1 = float(w @ (np.exp(np.maximum(S1 + S2, 0)) - 1)); print(f"         control: the same slack as one non-negative group (S = 0): C' = {Cp1:.1f}, (UP) = ln Z(m-) = {lnz(E2):.6f} (holds, attained)")
    # (UE): two states, E = (0, 0), ceiling m+ = (0, L), floor m- = (-a, 0); minus-groups S-_1 = (a, -bb), S-_2 = (0, +bb) (sum (a, 0) = E - m-); plus-groups S+_1 = 0, S+_2 = (0, sig), sig <= L
    a_, bb, sig, L = 0.1, 5.0, 1.0, 1.0; E3 = np.zeros(2); mp = np.array([0.0, L]); mm = np.array([-a_, 0.0]); wp = np.exp(-mp); wp /= wp.sum()
    Sm1, Sm2, Sp1, Sp2 = np.array([a_, -bb]), np.array([0.0, bb]), np.zeros(2), np.array([0.0, sig])
    assert (Sm1 + Sm2 <= E3 - mm + 1e-15).all() and (Sp1 + Sp2 <= mp - E3 + 1e-15).all()
    C = float(wp @ (Sm1 * np.exp(Sp1))) + float(wp @ (Sm2 * np.exp(Sp2))); u = lnz(mm); it2 = []
    for _ in range(60):
        u = lnz(mm) - C * math.exp(min(lnz(mp) - u, 700.0)); it2.append(u)
    Cc = float(wp @ ((Sm1 + Sm2) * np.exp(Sp1 + Sp2)))                                    # control: one group, both slacks non-negative
    uc = lnz(mm)
    for _ in range(60): uc = lnz(mm) - Cc * math.exp(lnz(mp) - uc)
    print(f"    A6 (UE): two states, E = (0, 0), m+ = (0, {L}), m- = (-{a_}, 0); minus-groups ({a_}, -{bb}), (0, +{bb}) [sum = E - m-], plus-groups 0, (0, {sig}) [sum <= m+ - E]: C = {C:.4f}, first iterate {it2[0]:.6f} < ln Z = {lnz(E3):.6f}: {it2[0] < lnz(E3) - 1e-12} "
          f"(the iteration then runs away: step 60 = {it2[-1]:.3g})  [violated: one minus-group is negative];  control, the same slacks as one group (non-negative): C = {Cc:.4f}, (UE) = {uc:.6f} >= ln Z: {uc >= lnz(E3) - 1e-12}")
    # negative plus-group in (UE)/(UP): S+_1 = (0, s), S+_2 = (0, -s) with m+ = E; S- = (0, t), m- = E - S-
    s_, t_ = 2.0, 0.5; E4 = np.zeros(2); mp4 = np.zeros(2); mm4 = np.array([0.0, -t_]); w4 = np.array([0.5, 0.5]); Sm = np.array([0.0, t_])
    C4 = float(w4 @ (Sm * np.exp(np.array([0.0, s_])))); u1 = lnz(mm4) - C4 * math.exp(lnz(mp4) - lnz(mm4))
    C4c = float(w4 @ Sm); u1c = lnz(mm4) - C4c * math.exp(lnz(mp4) - lnz(mm4))
    print(f"    A6 (UE) with a negative PLUS group: m+ = E, plus-groups (0, {s_}), (0, -{s_}) [sum 0 <= m+ - E], the minus-slack (0, {t_}) paired with the first: C = {C4:.4f}, first iterate of (UE) = {u1:.6f} < ln Z = {lnz(E4):.6f}: "
          f"{u1 < lnz(E4) - 1e-12}  [violated];  control, the plus-groups merged into one (zero): C = {C4c:.4f}, first iterate {u1c:.6f} >= ln Z: {u1c >= lnz(E4) - 1e-12}")
    # A3: m against the number of hosts.  tau(x) = psi(x_1, x_2) phi(c + sum_{i>=3} a_i(x_i)), hosts 1, 2; a_i CONSTANT for i >= 3 (no additive statistic moves)
    k = [3, 3, 2, 2]; X = all_states(k); rng = np.random.default_rng(5); psi = rng.normal(0, 1, (3, 3)); tau = (psi[X[:, 0], X[:, 1]] * math.sin(0.7)).reshape(k)
    r2 = tau - interpolant(tau, [0] * 4, 1); r3 = tau - interpolant(tau, [0] * 4, 2)
    print(f"    A3 (m and the number of hosts): a term with two hosts whose additive statistics do not move at all (all increments zero): every bound of the form M x prod delta is zero; "
          f"remainder at order m = 2: largest |g - I_1 g| = {float(np.abs(r2).max()):.4f} (NOT zero: the subset T = the two hosts has no non-host site); at order m = 3: {float(np.abs(r3).max()):.1e} (zero)")


def S8(rng, ninst=200):
    print("S8  the class WITH a host (A3' in words; not covered by Proposition AA.1 as stated): tau(x) = phi(c(x_h) + sum_{i != h} a_i^{x_h}(x_i)), h the host; the statistic is additive over the")
    print("    other sites only for a fixed host state.  Bound written from P9's Lemma T' / Theorem R in this class, for m >= 2 (one host, m > number of hosts):")
    print("    Theta_T(x_T) = M_m^{c0} prod_{i in T} delta_i^{c0}(x_i) if h not in T (c0 the host's anchor state);  = sum_{c in {c0, x_h}} M_{m-1}^{c} prod_{i in T, i != h} delta_i^{c}(x_i) if h in T")
    res = {m: dict(viol=0, st=0, c_one=0, c_one_i=0, c_aa=0, c_aa_i=0, inst=0, tmin=[]) for m in (2, 3, 4)}
    for it in range(ninst):
        n = int(rng.integers(4, 7)); k = [int(v) for v in rng.integers(2, 4, n)]; x0 = [int(rng.integers(v)) for v in k]; X = all_states(k); h = int(rng.integers(n)); oth = [i for i in range(n) if i != h]
        sc = float(rng.choice([0.1, 0.3, 0.6])); cc = rng.normal(0, 1.0, k[h]); a = [[rng.normal(0, sc, k[i]) for i in range(n)] for c in range(k[h])]
        lo = [float(cc[c] + sum(a[c][i].min() for i in oth)) for c in range(k[h])]; hi = [float(cc[c] + sum(a[c][i].max() for i in oth)) for c in range(k[h])]
        phi = random_phi(rng, min(lo), max(hi))
        u = np.array([cc[x[h]] + sum(a[x[h]][i][x[i]] for i in oth) for x in X]); G = phi.val(u).reshape(k); scale = max(1.0, float(np.abs(G).max()))
        offh = (X[:, h] != x0[h]).reshape(k)
        for m in (2, 3, 4):
            if m > n - 1: continue
            R = res[m]; R["inst"] += 1; r = G - interpolant(G, x0, m - 1)
            # e_j of the increments of the non-host sites, for every host state c used as the context, on the grid of the non-host sites
            def e_of(c, j):
                d = [np.abs(a[c][i] - a[c][i][x0[i]]) if i != h else np.zeros(k[h]) for i in range(n)]
                return esym(d, j)[j]                                           # the host's own increment is zero here: sums over subsets of the other sites
            B = np.zeros(k); B1 = np.zeros(k); Baa = np.zeros(k)
            c0 = x0[h]; B += phi.dsup(m, lo[c0], hi[c0]) * e_of(c0, m); B1 += phi.dsup(m, lo[c0], hi[c0]) * e_of(c0, m)
            for c in range(k[h]):                                              # states with x_h = c != c0: the subsets T that contain the host
                if c == c0: continue
                sl = [slice(None)] * n; sl[h] = c; sl = tuple(sl)
                t_c0 = phi.dsup(m - 1, lo[c0], hi[c0]) * e_of(c0, m - 1)[sl]; t_c = phi.dsup(m - 1, lo[c], hi[c]) * e_of(c, m - 1)[sl]
                B[sl] += t_c0 + t_c; B1[sl] += t_c                             # control: only the actual host state, the anchor's host state forgotten
            # control: Corollary AA.2 applied as if the host were an ordinary site with increment |c(x_h) - c(x0_h)| and the tables of the anchor's host state
            d_aa = [np.abs(a[c0][i] - a[c0][i][x0[i]]) if i != h else np.abs(cc - cc[c0]) for i in range(n)]
            Baa = phi.dsup(m, min(lo), max(hi)) * esym(d_aa, m)[m]
            tol = 1e-11 * scale; R["st"] += len(X); R["viol"] += int((np.abs(r) > B * (1 + 1e-9) + tol).sum())
            v1 = int((np.abs(r) > B1 * (1 + 1e-9) + tol).sum()); R["c_one"] += v1; R["c_one_i"] += int(v1 > 0)
            v2 = int((np.abs(r) > Baa * (1 + 1e-9) + tol).sum()); R["c_aa"] += v2; R["c_aa_i"] += int(v2 > 0)
            sel = (np.abs(r) > 1e-9 * scale) & (B > 0)
            if sel.any(): R["tmin"].append(float((B[sel] / np.abs(r[sel])).min()))
    for m, R in res.items():
        print(f"    m = {m}: {R['inst']} instances, {R['st']} states: violations of the bound with hosts: {R['viol']}; smallest bound/|remainder| {min(R['tmin']):.3f}, median of the per-instance minima {np.median(R['tmin']):.2f}; "
              f"controls: one host assignment only (the anchor's forgotten): {R['c_one']} violations in {R['c_one_i']} instances; Corollary AA.2 as stated, the host treated as an additive site: {R['c_aa']} violations in {R['c_aa_i']} instances")


def S9():
    print("S9  two small statements of the audit run: (i) A2, 'at most m hosts' is sharp (the theory division's example, term_orders_sharp); (ii) A4, which non-negativity Proposition P needs")
    k = [2, 2, 2]; X = all_states(k); F = (X[:, 0] * X[:, 1] * X[:, 2]).astype(float).reshape(k); r = F - interpolant(F, [0, 0, 0], 1)
    md = max(abs(F[tuple(1 if i in T else 0 for i in range(3))] - F[tuple(1 if i == T[0] else 0 for i in range(3))] - F[tuple(1 if i == T[1] else 0 for i in range(3))] + F[0, 0, 0]) for T in ((0, 1), (0, 2), (1, 2)))
    print(f"    (i) F = x1 x2 x3 on three binary sites, m = 2, all three sites hosts: every pair mixed difference with the third site at the anchor is {md:.0f}, the remainder at (1,1,1) is {float(r[1, 1, 1]):.0f}: the host-anchored constants 0 do not bound it (m + 1 hosts)")
    # (ii) two binary sites, m = 2, T = {1, 2}, U = {1} with weight 1; Phi_T = -1 at the one state of X*_T
    lhs = 0.0; gam = -1.0                                                     # at x = (1, 0): no T inside S(x); gamma_U(x_U) = w c_{T,U}(1) = max{Phi_T(y): y_1 = 1} = -1
    print(f"    (ii) Phi_T = -1 (signed), c_(T,U) = max Phi_T = -1 < 0: at x = (1, 0) the left side (no subset inside the changed set) is {lhs:.0f}, the right side gamma_U = {gam:.0f}: the allocation inequality FAILS; "
          f"with c_(T,U) := max(Phi_T, 0) = 0 it holds (0 <= 0) although Phi_T is negative: what is needed is c >= 0, not Phi >= 0 (as the theory division's resolved_allocation states)")


def main():
    rng = np.random.default_rng(SEED)
    S1(rng); S2(rng); S3(rng); S4(rng); S5(rng); S6(); S6b(); S7(); S8(np.random.default_rng(SEED + 8)); S9()
    print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
