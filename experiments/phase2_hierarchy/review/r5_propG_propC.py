"""Review item 4: Propositions G (flags, small-slope limit) and C (cells), sections 7.1-7.2.

Part G   the algebra of the proof of Proposition G:
         (1) symbolic: c0 = (rho-1)^2 (rho^2+2 rho-1); 16 rho^4 (4 c0 - c2^2) = -(2 rho-1)^3 (16 rho^3-8 rho^2-6 rho-1);
             the expansion of (D^2 + rho^2 + D/(2 rho))^2;
         (2) numeric: the anchor is in the set D; the displayed bound; G0 >= 0 on a grid;
             the monotonicity in theta; the reviewer's scaling identity  B(theta) = s^2 G0 + 2 s (s-1) R
             (theta = s^2/4), which gives the STRICT inequality for theta > 1/4 that the report does not prove;
             the minimum of the bracket for theta > 1/4 (the report claims 2 sqrt(theta) - 1 numerically).
Part C1  the two cases of the proof of Proposition C on random instances (exponent level, continuum):
         anchor in the required regions; the sum of the terms is <= 0; and how close to 0 the proof's bound
         comes for theta > h (the proof gives no strict margin in the sub-case "x <= R, T not relaxed").
Part C2  the statement of Proposition C itself at finite slope on a grid (own code, not the small-slope limit):
         the pointwise largest U = -F with the stated hypotheses and m_vis = 0, its deepest twin U_D
         (largest admissible function equal to U on W_3), and the hidden gain  max_{y not in W_3} [U_D(y) - r(y)].
usage: python3 r5_propG_propC.py G | C1 | C2
"""
import math
import sys
import time
import numpy as np
from rv_common import consts, fKL, kKL, finv


# ------------------------------------------------------------------ Part G
def partG():
    import sympy as sp
    rho, D = sp.symbols('rho Delta', positive=True)
    c2 = 2 * rho ** 2 - 2 + 1 / (4 * rho ** 2)
    c0 = (rho - 1) ** 2 * (rho ** 2 + 2 * rho - 1)
    print('c0 == rho^4 - 4 (rho - 1/2)^2 :', sp.simplify(c0 - (rho ** 4 - 4 * (rho - sp.Rational(1, 2)) ** 2)) == 0)
    lhs = 16 * rho ** 4 * (4 * c0 - c2 ** 2)
    rhs = -(2 * rho - 1) ** 3 * (16 * rho ** 3 - 8 * rho ** 2 - 6 * rho - 1)
    print('16 rho^4 (4 c0 - c2^2) == -(2 rho - 1)^3 (16 rho^3 - 8 rho^2 - 6 rho - 1) :', sp.expand(lhs - rhs) == 0)
    ex = sp.expand((D ** 2 + rho ** 2 + D / (2 * rho)) ** 2 - (D ** 4 + 2 * D ** 2 * rho ** 2 + rho ** 4 + D ** 3 / rho + D * rho + D ** 2 / (4 * rho ** 2)))
    print('expansion of (D^2 + rho^2 + D/(2 rho))^2 :', ex == 0)
    red = sp.expand((D ** 4 + 2 * D ** 2 * rho ** 2 + rho ** 4 + 2 * D ** 2 + D ** 2 / (4 * rho ** 2)) - 4 * D ** 2 - 4 * (rho - sp.Rational(1, 2)) ** 2
                    - (D ** 4 + c2 * D ** 2 + c0))
    print('reduction to D^4 + c2 D^2 + c0 :', sp.simplify(red) == 0)
    cubic = 16 * rho ** 3 - 8 * rho ** 2 - 6 * rho - 1
    roots = [complex(r) for r in sp.Poly(cubic, rho).nroots()]
    print('roots of the cubic:', [('%.6f%+.6fi' % (r.real, r.imag)) for r in roots], ' cos(pi/8) = %.6f' % math.cos(math.pi / 8))
    cmax = max(float(cubic.subs(rho, v)) for v in np.linspace(0.5, math.cos(math.pi / 8), 2001))
    print('max of the cubic on [1/2, cos(pi/8)] = %.4f (must be < 0)' % cmax)
    print('c2 at cos(pi/8): %.2e (must be 0);  c2 >= 0 for rho >= cos(pi/8):' % float(c2.subs(rho, math.cos(math.pi / 8))),
          all(float(c2.subs(rho, v)) >= -1e-12 for v in np.linspace(math.cos(math.pi / 8), 30, 3000)))

    # numeric part
    Dg = np.concatenate([np.linspace(1e-6, 3, 1500), np.linspace(3, 40, 500)])[:, None]
    rg = np.concatenate([np.linspace(0.5, 3, 1500), np.linspace(3, 40, 500)])[None, :]
    G0 = Dg ** 2 + Dg / (2 * rg) + rg ** 2 - 2 * np.sqrt(Dg ** 2 + (rg - 0.5) ** 2)
    i = np.unravel_index(int(np.argmin(G0)), G0.shape)
    print('G0 on a grid (Delta in (0,40], rho in [1/2,40]): min = %.3e at Delta = %.4f, rho = %.4f' % (G0.min(), Dg[i[0], 0], rg[0, i[1]]))

    rng = np.random.default_rng(7)
    nrand = 400000
    theta = 0.25 + rng.exponential(0.5, nrand) * (rng.random(nrand) < 0.8)
    st = np.sqrt(theta)
    ystar = rng.exponential(0.7, nrand)
    wstar = st * (1 + rng.exponential(0.5, nrand))
    qstar = rng.normal(0, 1.0, nrand) * (rng.random(nrand) < 0.8)
    rho_ = np.sqrt(qstar ** 2 + wstar ** 2)
    b = st * np.abs(wstar) / rho_
    ey = np.minimum(ystar, b)
    eq = st * qstar / rho_
    ew = st * wstar / rho_
    inD = (ey ** 2 + eq ** 2 <= theta + 1e-12) & (eq ** 2 + ew ** 2 <= theta + 1e-12)
    dist = np.sqrt((ystar - ey) ** 2 + (qstar - eq) ** 2 + (wstar - ew) ** 2)
    dist2 = np.sqrt((ystar - ey) ** 2 + (rho_ - st) ** 2)
    bound = ey ** 2 + 2 * dist - ystar ** 2 - rho_ ** 2
    print('random instances (%d): anchor in D: %s; |Y*-e| formula max error %.1e; b >= theta/rho: %s; max of the bound = %.3e (must be <= 0)'
          % (nrand, bool(inD.all()), float(np.abs(dist - dist2).max()), bool((b >= theta / rho_ - 1e-12).all()), float(bound.max())))
    # margin for theta > 1/4
    print('margin: max over (y*, q*, w*) of the bound, against 1 - 2 sqrt(theta)')
    for th in (0.25, 0.26, 0.3, 0.5, 1.0, 2.0):
        s_ = math.sqrt(th)
        ys = np.linspace(0, 4, 801)[:, None, None]
        ws = (s_ * (1 + np.linspace(0, 3, 301) ** 2))[None, :, None]
        qs = np.linspace(0, 4, 201)[None, None, :]
        r_ = np.sqrt(qs ** 2 + ws ** 2)
        b_ = s_ * ws / r_
        ey_ = np.minimum(ys, b_)
        bd = ey_ ** 2 + 2 * np.sqrt((ys - ey_) ** 2 + (r_ - s_) ** 2) - ys ** 2 - r_ ** 2
        print('   theta = %.2f: max bound = %+.5f   1 - 2 sqrt(theta) = %+.5f' % (th, float(bd.max()), 1 - 2 * s_))
    # monotonicity in theta of B(theta) = D^2 + 2 theta D / rho + rho^2 - 2 sqrt(D^2 + (rho - sqrt(theta))^2), theta in [1/4, rho^2]
    worst = 0.0
    wid = 0.0
    for _ in range(200000):
        r1 = 0.5 + rng.exponential(1.0)
        d1 = rng.exponential(1.0)
        t1, t2 = sorted(rng.uniform(0.25, r1 * r1, 2))
        B = lambda t: d1 ** 2 + 2 * t * d1 / r1 + r1 ** 2 - 2 * math.sqrt(d1 ** 2 + (r1 - math.sqrt(t)) ** 2)
        worst = min(worst, B(t2) - B(t1))
        # scaling identity
        s_ = 2 * math.sqrt(t1)
        dp, rp = d1 / s_, r1 / s_
        G0p = dp ** 2 + dp / (2 * rp) + rp ** 2 - 2 * math.sqrt(dp ** 2 + (rp - 0.5) ** 2)
        Rp = math.sqrt(dp ** 2 + (rp - 0.5) ** 2)
        wid = max(wid, abs(B(t1) - (s_ * s_ * G0p + 2 * s_ * (s_ - 1) * Rp)))
    print('monotonicity of the bracket in theta: most negative increment %.2e (must be >= 0)' % worst)
    print('scaling identity B(theta; D, rho) = s^2 G0(D/s, rho/s) + 2 s (s-1) R(D/s, rho/s), s = 2 sqrt(theta): max error %.1e' % wid)


# ------------------------------------------------------------------ Part C1
def relax_T(yT, phiT, target, kap):
    """tau in [0, kappa] with sum_T phi_j f(max(y_j, tau)) = target (rate nonincreasing in tau)."""
    rate = lambda tau: sum(p * fKL(max(y, tau)) for y, p in zip(yT, phiT))
    if rate(0.0) <= target:
        return 0.0
    lo, hi = 0.0, kap
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if rate(mid) > target:
            lo = mid
        else:
            hi = mid
    return hi


def partC1():
    rng = np.random.default_rng(11)
    stats = dict(n=0, hidden=0, region_fail=0, bound_pos=0)
    sup_by_case = {}
    closest = []
    for trial in range(400000):
        u = float(rng.choice([0.5, 1.0, 2.0, 4.0]))
        c = consts(u)
        h, kap, a, pu, Lam = c['h'], c['kap'], c['a'], c['pu'], c['Lam']
        nP, nQ, nT = int(rng.integers(0, 3)), int(rng.integers(0, 3)), int(rng.integers(0, 3))
        m = nP + nQ + nT
        if m == 0:
            continue
        phi = rng.dirichlet(np.ones(m))
        roles = ['P'] * nP + ['Q'] * nQ + ['T'] * nT
        ratio = float(rng.choice([1.0, 1.05, 1.2, 1.5, 2.5]))
        theta = ratio * h
        R = float(rng.choice([0.0, 0.3, 0.7, 0.95, 1.0, 1.05, 1.5, 3.0, 10.0])) * theta * rng.uniform(0.9, 1.1)
        mode = rng.integers(0, 4)
        if mode == 0:
            y = rng.uniform(0, 0.5, m)
        elif mode == 1:
            y = np.where(rng.random(m) < 0.5, pu, 0.5) + 0.0
        elif mode == 2:
            y = np.clip(pu + rng.normal(0, 0.03, m), 0, 0.5)
        else:
            y = np.clip(np.where(rng.random(m) < 0.5, rng.uniform(0, kap, m), rng.uniform(kap, 0.5, m)), 0, 0.5)
        rj = np.array([phi[j] * fKL(y[j]) for j in range(m)])
        iP = [j for j in range(m) if roles[j] == 'P']
        iQ = [j for j in range(m) if roles[j] == 'Q']
        iT = [j for j in range(m) if roles[j] == 'T']
        rP, rQ, rT = rj[iP].sum(), rj[iQ].sum(), rj[iT].sum()
        stats['n'] += 1
        if min(rP + rQ, R) + rT <= theta:
            continue                                   # y in W_3: nothing to prove
        stats['hidden'] += 1
        e = y.copy()
        for j in iP + iQ:
            e[j] = max(y[j], kap)
        x = sum(phi[j] * fKL(e[j]) for j in iP)
        rQe = sum(phi[j] * fKL(e[j]) for j in iQ)
        if x <= R:
            target = min(rT, theta - x - rQe)
            case = 'x<=R'
        else:
            target = min(rT, theta - R - rQe)
            case = 'x>R'
        relaxed = target < rT - 1e-15
        tau = relax_T([y[j] for j in iT], [phi[j] for j in iT], target, kap) if relaxed else 0.0
        for j in iT:
            e[j] = max(y[j], tau)
        rTe = sum(phi[j] * fKL(e[j]) for j in iT)
        # region checks
        tol = 1e-9
        ok = True
        ok &= (min(x + rQe, R) + rTe <= theta + tol)                       # anchor in W_3
        if case == 'x<=R':
            ok &= (x + rQe + rTe <= theta + tol)                           # anchor in W_1
            cap = 0.0
        else:
            ok &= (min(x, R) + rQe + rTe <= theta + tol)                   # anchor in W_2
            ok &= (min(x, R) + rQe <= theta + tol)                         # (e_P, e_Q, 1/2) in W_2
            ok &= (x + rQe <= theta + tol)                                 # (e_P, e_Q, 1/2) in W_1
            cap = x - R
        if relaxed and tau > kap + 1e-12:
            ok = False
        stats['region_fail'] += (not ok)
        total = cap + sum(phi[j] * (u * (e[j] - y[j]) - fKL(y[j])) for j in range(m))      # U_D(y) - r(y) - m_vis <= total
        key = (case, 'T relaxed' if relaxed else 'T not relaxed', 'theta=h' if ratio == 1.0 else 'theta>h')
        sup_by_case[key] = max(sup_by_case.get(key, -1e300), total / (theta - h) if ratio > 1.0 else total / h)
        if total > 1e-9:
            stats['bound_pos'] += 1
        if ratio > 1.0 and total > -1e-3 * h:
            closest.append((total, u, ratio, R / theta, roles, np.round(phi, 3).tolist(), np.round(y, 4).tolist()))
    print('C1: %d instances, %d with y outside W_3; region checks failed: %d; proof bound > 0: %d'
          % (stats['n'], stats['hidden'], stats['region_fail'], stats['bound_pos']))
    print('C1: largest value of the proof bound on U_D(y) - r(y) - m_vis, in units of (theta - h) [theta > h] or of h [theta = h]:')
    for k in sorted(sup_by_case):
        print('     %-40s %+.4f' % (str(k), sup_by_case[k]))
    print('C1: instances with theta > h where the proof bound is within 1e-3 h of 0 (no margin): %d; examples:' % len(closest))
    for row in closest[:4]:
        print('     bound=%+.2e u=%g theta/h=%g R/theta=%.2f roles=%s phi=%s y=%s' % row)


# ------------------------------------------------------------------ Part C2
def cells_gain(ns, roles, u, theta, R):
    from scipy.sparse import coo_matrix, csr_matrix
    from scipy.sparse.csgraph import connected_components, dijkstra
    m = len(ns)
    n = sum(ns)
    shape = tuple(x + 1 for x in ns)
    N = int(np.prod(shape))
    grids = np.meshgrid(*[np.arange(x + 1) for x in ns], indexing='ij', sparse=True)
    rate = [np.array([ns[j] / n * fKL(d / ns[j]) for d in range(ns[j] + 1)]) for j in range(m)]
    P = [j for j in range(m) if roles[j] == 'P']
    Q = [j for j in range(m) if roles[j] == 'Q']
    T = [j for j in range(m) if roles[j] == 'T']
    zero = np.zeros(shape)
    part = lambda idx: zero + sum(rate[j][grids[j]] for j in idx) if idx else zero.copy()
    rP, rQ, rT = part(P), part(Q), part(T)
    r = rP + rQ + rT
    eps = 1e-12
    W1 = r <= theta + eps
    W2 = np.minimum(rP, R) + rQ + rT <= theta + eps
    W3 = np.minimum(rP + rQ, R) + rT <= theta + eps
    idx = np.arange(N, dtype=np.int64).reshape(shape)

    def key_array(fixed):
        key = np.zeros(shape, dtype=np.int64)
        for j in range(m):
            key = key * (ns[j] + 1) + (grids[j] if j in fixed else 0)
        return key

    rows, cols = [], []
    for region, fixed in ((W1, P), (W2, P + Q)):
        nodes = idx[region]
        keys = key_array(fixed)[region]
        uniq, inv = np.unique(keys, return_inverse=True)
        rep = np.empty(len(uniq), dtype=np.int64)
        rep[inv[::-1]] = nodes[::-1]
        rows.append(nodes)
        cols.append(rep[inv])
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    ncomp, lab = connected_components(coo_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(N, N)).tocsr(), directed=False)
    lab = lab.astype(np.int64)
    labg = lab.reshape(shape)
    w_edge = u / n                                       # one grid step in any block costs u * phi_j * (1/n_j) = u/n
    pairs = []
    plain_a, plain_b = [], []
    for j in range(m):
        sa = [slice(None)] * m
        sb = [slice(None)] * m
        sa[j] = slice(0, ns[j])
        sb[j] = slice(1, ns[j] + 1)
        a = labg[tuple(sa)].ravel()
        b = labg[tuple(sb)].ravel()
        plain_a.append(idx[tuple(sa)].ravel())
        plain_b.append(idx[tuple(sb)].ravel())
        keep = a != b
        lo = np.minimum(a[keep], b[keep])
        hi = np.maximum(a[keep], b[keep])
        pairs.append(np.unique(lo * ncomp + hi))
    pairs = np.unique(np.concatenate(pairs))
    ea, eb = pairs // ncomp, pairs % ncomp
    cap = np.full(ncomp, np.inf)
    np.minimum.at(cap, lab, np.maximum(r - R, 0.0).ravel())           # m_vis <= 0: U(z) <= (r(z) - R)_+ everywhere
    OFF = 1.0
    src = ncomp
    rr = np.concatenate([ea, np.full(ncomp, src, dtype=np.int64)])
    cc = np.concatenate([eb, np.arange(ncomp)])
    ww = np.concatenate([np.full(len(ea), w_edge), cap + OFF])
    dist = dijkstra(csr_matrix((ww, (rr, cc)), shape=(ncomp + 1, ncomp + 1)), directed=False, indices=src)
    U = (dist[:ncomp] - OFF)[lab].reshape(shape)
    mvis = float((U - np.maximum(r - R, 0.0)).max())
    # deepest twin: largest admissible function equal to U on W_3
    pa = np.concatenate(plain_a)
    pb = np.concatenate(plain_b)
    w3 = np.nonzero(W3.ravel())[0]
    rr = np.concatenate([pa, np.full(len(w3), N, dtype=np.int64)])
    cc = np.concatenate([pb, w3])
    ww = np.concatenate([np.full(len(pa), w_edge), U.ravel()[w3] + OFF])
    dist2 = dijkstra(csr_matrix((ww, (rr, cc)), shape=(N + 1, N + 1)), directed=False, indices=N)
    UD = (dist2[:N] - OFF).reshape(shape)
    hidden = ~W3
    if not hidden.any():
        return float('nan'), mvis, None, 0
    val = np.where(hidden, UD - r, -np.inf)
    am = int(np.argmax(val))
    return float(val.ravel()[am]) - mvis, mvis, np.unravel_index(am, shape), int(hidden.sum())


def partC2():
    print('# C2: hidden gain of the cell model at finite slope, on a grid (units: exponent per coordinate).  Proposition C claims gain <= 0.')
    print('# For comparison: D(theta) = u f^{-1}(theta) - Lambda_1 (plain dip) and h - theta.  Grid step: one unit of the type grid costs u/n.')
    worst = -1e300
    worst_strict = -1e300
    for u in (1.0, 4.0):
        c = consts(u)
        h = c['h']
        for roles, ns in (('PQT', (40, 40, 40)), ('PQT', (20, 40, 60)), ('PT', (150, 150)), ('PT', (80, 220)), ('QT', (150, 150)),
                          ('PQ', (150, 150)), ('PP', (150, 150)), ('PTT', (40, 40, 40)), ('P', (600,))):
            n = sum(ns)
            for ratio in (1.0, 1.2, 1.6):
                theta = ratio * h
                row = []
                for Rm in (0.0, 0.5, 0.9, 1.0, 1.1, 2.0, 5.0, 50.0):
                    R = Rm * theta
                    g, mvis, arg, nh = cells_gain(list(ns), roles, u, theta, R)
                    assert abs(mvis) < 1e-9
                    row.append((Rm, g))
                    if g == g:
                        worst = max(worst, g)
                        if ratio > 1.0:
                            worst_strict = max(worst_strict, g / (theta - h))
                Dth = u * finv(theta) - c['Lam']
                print('u=%g %-3s %-13s theta=%.1f h: D(theta)=%+.5f h-theta=%+.5f grid u/n=%.5f | gain at R/theta = %s'
                      % (u, roles, str(ns), ratio, Dth, h - theta, u / n,
                         ', '.join('%g: %s' % (rm, ('%+.5f' % g) if g == g else 'none hidden') for rm, g in row)), flush=True)
    print('largest hidden gain over all cases: %+.5f (Proposition C: <= 0 up to the grid step u/n)' % worst)
    print('largest hidden gain / (theta - h) over the cases with theta > h: %+.4f (a strict margin needs this to be negative)' % worst_strict)


if __name__ == '__main__':
    t0 = time.time()
    what = sys.argv[1] if len(sys.argv) > 1 else 'G'
    {'G': partG, 'C1': partC1, 'C2': partC2}[what]()
    print('part %s finished in %.0f s' % (what, time.time() - t0))
