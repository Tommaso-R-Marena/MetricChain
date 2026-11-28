"""Review item 3: Lemma A2 and Theorem H2 (two rounds on two blocks).

Part A  Xi(theta, phi1) = min{ phi1 k(z) + phi2 (u rho - Lambda1) : z in [p_u, 1/2], phi1 f(z) + phi2 f(rho) <= theta }:
        own minimisation; monotonicity in theta; sign at theta = h; root; vartheta(phi1) = min{phi2 a, root};
        theta_2^*(u) = max_phi1 vartheta(phi1); compared with the numbers printed in the report (sections 2 and 6).
Part B  Lemma A2 at finite n with exact binomial costs.  The pointwise largest G = -F on two blocks subject to
          (adm) u-Lipschitz on the grid, (hyp) F sees only block 1 on V_0(Theta) [parity version],
          (norm) nu <= 0 on V_{1}(Theta) = {t_2(d_2) <= Theta}   (nu_1 = 0, attained)
        is computed as a shortest-path distance (same method as r2_lemmaB.py), and
          H := max{ nu*(y) : t_2(y_2) > Theta }
        is compared with (A1): n Xi(theta^-, phi1) + 2u + 4L and, when (Theta - L)/n_2 >= a, with
        (A2): -n_2 k(y^1) + u + 2L.  Also printed: n * min{Xi(theta, phi1), phi2 k(y^1)}, the gap formula of
        the archive's twins (Theorem 11.86), which H should approach from above up to O(log n) if "the twins
        are extremal".
usage: python3 r4_lemmaA2_H2.py A | B
"""
import math
import sys
import time
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from rv_common import consts, fKL, kKL, finv, tcost

LN2 = math.log(2.0)


def f_np(r):
    r = np.asarray(r, dtype=float)
    out = np.full(r.shape, LN2)
    ok = (r > 0) & (r < 1)
    rr = r[ok]
    out[ok] = rr * np.log(2 * rr) + (1 - rr) * np.log(2 * (1 - rr))
    return out


def finv_np(theta):
    """vectorised inverse of f on [0, 1/2]; theta in [0, ln 2]."""
    theta = np.asarray(theta, dtype=float)
    lo = np.zeros(theta.shape)
    hi = np.full(theta.shape, 0.5)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        up = f_np(mid) > theta
        lo = np.where(up, mid, lo)
        hi = np.where(up, hi, mid)
    return 0.5 * (lo + hi)


def Xi(theta, phi1, u, grid=2001):
    """own evaluation of Xi (grid in z, three zooms); +inf if the feasible set is empty."""
    c = consts(u)
    pu, Lam = c['pu'], c['Lam']
    phi2 = 1.0 - phi1

    def E(zs):
        fz = f_np(zs)
        rem = theta - phi1 * fz
        feas = rem >= 0
        rho = np.where(rem >= phi2 * LN2, 0.0, finv_np(np.clip(rem / phi2, 0.0, LN2)))
        val = phi1 * (fz + u * zs - Lam) + phi2 * (u * rho - Lam)
        return np.where(feas, val, np.inf)

    lo, hi = pu, 0.5
    best, zbest = float('inf'), None
    for _ in range(4):
        zs = np.linspace(lo, hi, grid)
        vals = E(zs)
        i = int(np.argmin(vals))
        if not np.isfinite(vals[i]):
            return float('inf'), None
        if vals[i] < best:
            best, zbest = float(vals[i]), float(zs[i])
        lo, hi = zs[max(i - 1, 0)], zs[min(i + 1, grid - 1)]
    return best, zbest


def Xi_root(phi1, u):
    c = consts(u)
    lo = c['h']
    hi = phi1 * c['a'] + (1 - phi1) * LN2 + 1e-9
    assert Xi(lo, phi1, u)[0] > 0 and Xi(hi, phi1, u)[0] < 0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if Xi(mid, phi1, u)[0] > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def vartheta(phi1, u):
    c = consts(u)
    return min((1 - phi1) * c['a'], Xi_root(phi1, u))


def partA():
    print('# Part A: Xi, its root, vartheta and theta_2^*')
    print('# claims of the report: theta2*/a = 0.3460, 0.3469, 0.3495, 0.3594, 0.3940, 0.4396, 0.4878, 0.5749 and best phi1 = 0.654, 0.653,')
    print('#   0.651, 0.641, 0.606, 0.560, 0.512, 0.425 at u = 0.05, 0.25, 0.5, 1, 2, 3, 4, 6; table of section 6: theta2* = 0.01059, 0.03987, 0.12916, 0.29417 at u = 0.5, 1, 2, 4')
    for u in (0.05, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0):
        c = consts(u)
        # monotonicity and sign of Xi
        worst_incr = -1e300
        min_at_h = 1e300
        for phi1 in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95):
            th = np.linspace(c['h'], phi1 * c['a'] + (1 - phi1) * LN2, 60)
            xs = np.array([Xi(t, phi1, u)[0] for t in th])
            worst_incr = max(worst_incr, float(np.max(np.diff(xs))))
            min_at_h = min(min_at_h, xs[0])
        # theta_2^* = max over phi1 of min{phi2 a, root}: the root increases and phi2 a decreases in phi1
        lo, hi = 0.02, 0.98
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if Xi_root(mid, u) < (1 - mid) * c['a']:
                lo = mid
            else:
                hi = mid
        phibest = 0.5 * (lo + hi)
        th2 = vartheta(phibest, u)
        # is the crossing really the maximum of vartheta?  scan
        scan = max(vartheta(p, u) for p in np.linspace(0.03, 0.97, 95))
        print('u=%5.2f a=%.5f h=%.5f | theta2*=%.5f theta2*/a=%.4f theta2*/h=%.3f best phi1=%.3f (scan max %.5f) | '
              'largest increase of Xi along theta: %.1e | min over phi1 of Xi(h, phi1) = %.2e'
              % (u, c['a'], c['h'], th2, th2 / c['a'], th2 / c['h'], phibest, scan, worst_incr, min_at_h), flush=True)
    # Corollary H3: which splits have c_2 > h ?
    print('# Corollary H3: c_2 = max{h, vartheta(phi1), vartheta(phi2)} for a few splits (units of h); threshold 1 - h/a')
    for u in (1.0, 4.0, 8.0, 12.0):
        c = consts(u)
        row = []
        for phi1 in (0.1, 0.3, 0.5, 0.7, 0.9):
            v1 = vartheta(phi1, u)
            v2 = vartheta(1 - phi1, u)
            row.append('phi1=%.1f: %.3f' % (phi1, max(c['h'], v1, v2) / c['h']))
        print('u=%5.2f h/a=%.3f 1-h/a=%.3f | c_2/h: %s' % (u, c['h'] / c['a'], 1 - c['h'] / c['a'], ', '.join(row)), flush=True)


def extremal_A2(n1, n2, u, Theta, parity=True):
    ns = (n1, n2)
    shape = (n1 + 1, n2 + 1)
    N = shape[0] * shape[1]
    t1 = tcost(n1)
    t2 = tcost(n2)
    tall = t1[:, None] + t2[None, :]
    V0 = tall <= Theta
    V1 = np.broadcast_to(t2[None, :] <= Theta, shape)
    idx = np.arange(N, dtype=np.int64).reshape(shape)
    d2 = np.broadcast_to(np.arange(n2 + 1)[None, :], shape)
    d1 = np.broadcast_to(np.arange(n1 + 1)[:, None], shape)
    key = d1 * 2 + ((d2 % 2) if parity else 0)
    nodes = idx[V0]
    keys = key[V0]
    uniq, inv = np.unique(keys, return_inverse=True)
    rep = np.empty(len(uniq), dtype=np.int64)
    rep[inv[::-1]] = nodes[::-1]
    A = coo_matrix((np.ones(len(nodes), dtype=np.int8), (nodes, rep[inv])), shape=(N, N)).tocsr()
    ncomp, lab = connected_components(A, directed=False)
    lab = lab.astype(np.int64)
    labg = lab.reshape(shape)
    pairs = []
    for a, b in ((labg[:-1, :].ravel(), labg[1:, :].ravel()), (labg[:, :-1].ravel(), labg[:, 1:].ravel())):
        keep = a != b
        lo = np.minimum(a[keep], b[keep])
        hi = np.maximum(a[keep], b[keep])
        pairs.append(np.unique(lo * ncomp + hi))
    pairs = np.unique(np.concatenate(pairs))
    ea = pairs // ncomp
    eb = pairs % ncomp
    cap = np.full(ncomp, np.inf)
    np.minimum.at(cap, lab[V1.ravel()], tall.ravel()[V1.ravel()])
    fin = np.isfinite(cap)
    src = ncomp
    OFF = 1.0
    r = np.concatenate([ea, np.full(int(fin.sum()), src, dtype=np.int64)])
    c = np.concatenate([eb, np.nonzero(fin)[0]])
    w = np.concatenate([np.full(len(ea), float(u)), cap[fin] + OFF])
    dist = dijkstra(csr_matrix((w, (r, c)), shape=(ncomp + 1, ncomp + 1)), directed=False, indices=src)
    G = (dist[:ncomp] - OFF)[lab].reshape(shape)
    nu = G - tall
    nu1 = float(nu[V1].max())
    hidden = ~V1
    H = float(nu[hidden].max()) - nu1 if hidden.any() else float('nan')
    arg = np.unravel_index(int(np.argmax(np.where(hidden, nu, -np.inf))), shape) if hidden.any() else None
    lip = max(float(np.abs(np.diff(G, axis=0)).max()), float(np.abs(np.diff(G, axis=1)).max()))
    return H, arg, nu1, lip


def partB():
    print('# Part B: Lemma A2, exact extremal functions (parity version).  H = max hidden nu - nu_1.')
    print('# columns: u phi1 n (n1,n2) Theta/(n h) | H | (A1) bound | (A2) bound (if applicable) | n*min{Xi,phi2 k(y1)} (archive gap formula) | violations')
    viol = 0
    for u in (1.0, 2.0, 4.0):
        c = consts(u)
        for phi1 in (0.3, 0.5, 0.641, 0.8):
            th2 = vartheta(phi1, u)
            ratios = sorted(set([1.0, 1.2, round(th2 / c['h'], 4), round(th2 / c['h'] + 0.1, 4), 2.0, 3.0,
                                 round((1 - phi1) * c['a'] / c['h'] + 0.3, 4)]))
            for n in (800, 3200):
                n1 = int(round(phi1 * n))
                n2 = n - n1
                p1 = n1 / n
                p2 = n2 / n
                L = math.log(n + 1.0)
                for ratio in ratios:
                    Theta = ratio * n * c['h']
                    H, arg, nu1, lip = extremal_A2(n1, n2, u, Theta, parity=True)
                    assert lip <= u + 1e-9 and abs(nu1) < 1e-9
                    thm = (Theta - 2 * L) / n
                    xi_m = Xi(thm, p1, u)[0]
                    b1 = n * xi_m + 2 * u + 4 * L
                    b2 = float('nan')
                    if (Theta - L) / n2 >= c['a']:
                        y1 = finv((Theta - L) / n2)
                        b2 = -n2 * kKL(y1, u) + u + 2 * L
                    # archive formula at theta = Theta/n
                    th = Theta / n
                    xi0 = Xi(th, p1, u)[0]
                    if th < p2 * c['a']:
                        y1a = finv(th / p2)
                        form = n * min(xi0, p2 * kKL(y1a, u))
                    else:
                        form = float('nan')
                    bad = (H == H) and ((H > b1 + 1e-9) or (b2 == b2 and H > b2 + 1e-9))
                    viol += bad
                    print('u=%g phi1=%.3f n=%d (%d,%d) Theta=%.4f n h (theta/vartheta=%.3f) | H=%+9.3f at %s | A1: %+9.3f | A2: %+9.3f | formula: %+9.3f | %s'
                          % (u, phi1, n, n1, n2, ratio, th / th2, H, str(tuple(int(v) for v in arg)) if arg is not None else '-',
                             b1, b2, form, 'VIOLATION' if bad else 'ok'), flush=True)
    print('violations of (A1)/(A2): %d' % viol)


if __name__ == '__main__':
    t0 = time.time()
    what = sys.argv[1] if len(sys.argv) > 1 else 'A'
    if what == 'A':
        partA()
    else:
        partB()
    print('part %s finished in %.0f s' % (what, time.time() - t0))
