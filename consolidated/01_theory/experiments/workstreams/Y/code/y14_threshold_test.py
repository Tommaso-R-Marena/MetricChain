"""Is the uniform field the maximiser of the Jensen functional J(phi) = ln E_pi e^{-phi} + E_pi phi = KL(pi || pi_phi) over the
u-Lipschitz functions on a chain of n = 8..12 sites?  (If some phi in C has J(phi) > ln Z_n(h)/Z_n(0), then E_n > ln Z_n(h)/Z_n(0):
equality E_n = ln z_n forces the optimal centre to be pi.)
J is convex, so successive linearisation (each step an LP over the Lipschitz polytope: maximise <pi - pi_phi_k, phi>) increases J
monotonically and stops at a vertex that is a local maximum.  Starts: the uniform field, random members, domain fields,
functions of the magnetisation, minus the distance to the two ground states."""
import sys, time, math, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

t0 = time.time(); u = 1.0; rng = np.random.default_rng(3)
def setup(n):
    N = 2 ** n
    S = 1.0 - 2.0 * ((np.arange(N)[:, None] >> np.arange(n)[None, :]) & 1)
    rows, cols, vals = [], [], []; r = 0
    for i in range(n):
        x = np.arange(N); y = x ^ (1 << i); m = x < y
        for a, b in ((x[m], y[m]), (y[m], x[m])):
            k = len(a); rr = np.arange(r, r + k)
            rows += [rr, rr]; cols += [a, b]; vals += [np.ones(k), -np.ones(k)]; r += k
    A = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(r, N)).tocsr()
    return S, A, np.full(r, u)
def J(pi, phi):
    m = (-phi).max(); return m + math.log(float((pi * np.exp(-phi - m)).sum())) + float(pi @ phi)
def climb(pi, phi, A, b, itmax=60):
    N = len(pi); val = J(pi, phi)
    for it in range(itmax):
        w = pi * np.exp(-(phi - phi.min())); w /= w.sum()
        res = linprog(-(pi - w), A_ub=A, b_ub=b, bounds=[(0, 0)] + [(None, None)] * (N - 1), method="highs")
        new = res.x; v2 = J(pi, new)
        if v2 <= val + 1e-12: break
        phi, val = new, v2
    return val, phi
for n in (8, 10, 12):
    S, A, b = setup(n); N = 2 ** n; m = S.sum(axis=1)
    for p in (0.3, 0.2, 0.1, 0.05):
        Kp = 0.5 * math.log((1 - p) / p)
        lw = Kp * (S[:, :-1] * S[:, 1:]).sum(axis=1); pi = np.exp(lw - lw.max()); pi /= pi.sum()
        lnz = math.log(float((pi * np.exp(0.5 * u * m)).sum()))
        starts = {"uniform field": -0.5 * u * m, "-|m| type": -0.5 * u * np.abs(m), "+|m| type": 0.5 * u * np.abs(m),
                  "-dist to ground states": -u * np.minimum((n - m) / 2, (n + m) / 2),
                  "one domain wall": -0.5 * u * (S[:, :n // 2].sum(axis=1) - S[:, n // 2:].sum(axis=1)),
                  "bond field": 0.25 * u * (S[:, :-1] * S[:, 1:]).sum(axis=1)}
        nrand = 6 if n <= 10 else 2
        for k in range(nrand):
            c = rng.uniform(0, 3 * n, N); c[rng.random(N) < 0.9] = np.inf; c[rng.integers(N)] = 0
            D = None
            # random member by inf-convolution with the Hamming distance (via bit tricks, O(N n) relaxation)
            f = c.copy()
            for sweep in range(n):
                for i in range(n):
                    f = np.minimum(f, f[np.arange(N) ^ (1 << i)] + u)
            starts["random %d" % k] = f * rng.choice([1.0, -1.0])
        best = (-1, None); line = []
        for name, phi in starts.items():
            assert np.abs(A @ phi).max() <= u + 1e-9
            v, ph = climb(pi, phi, A, b)
            line.append("%s: %.5f->%.5f" % (name, J(pi, phi), v))
            if v > best[0]: best = (v, name)
        print("n=%2d p=%.2f: ln z_n = %.6f;  best local maximum found: %.6f (from '%s');  excess over ln z_n: %+.2e   [%.0f s]" % (n, p, lnz, best[0], best[1], best[0] - lnz, time.time() - t0), flush=True)
        if n == 10: print("      " + " | ".join(line))
print("%.1f s" % (time.time() - t0))
