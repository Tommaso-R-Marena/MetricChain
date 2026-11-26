"""(e) Theorem H: rank of the Jacobian of
      Phi_F : (torsions of K chains, K-1 weights) -> (mean squared distances on F)
by central finite differences in 60-digit arithmetic (mpmath), singular values in 60 digits.
Independent of the authors' modular computation (different method, different witness)."""
import sys
import mpmath as mp

mp.mp.dps = 60


def rot_x(t):
    c, s = mp.cos(t), mp.sin(t)
    return mp.matrix([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(t):
    c, s = mp.cos(t), mp.sin(t)
    return mp.matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def chain(tors, bonds, alphas):
    n = len(bonds) + 1
    X = [mp.matrix(3, 1) for _ in range(n)]
    F = mp.eye(3)
    X[1] = X[0] + bonds[0] * F[:, 0]
    for a in range(1, n - 1):
        tau = tors[a - 2] if a >= 2 else mp.mpf(0)
        F = F * rot_x(tau) * rot_z(alphas[a - 1])
        X[a + 1] = X[a] + bonds[a] * F[:, 0]
    return X


def d2(X, i, j):
    v = X[i] - X[j]
    return v[0] ** 2 + v[1] ** 2 + v[2] ** 2


def phi(params, K, n, pairs, bonds, alphas):
    tors = [params[k * (n - 3):(k + 1) * (n - 3)] for k in range(K)]
    w = list(params[K * (n - 3):])
    w.append(1 - sum(w))
    Xs = [chain(t, bonds, alphas) for t in tors]
    return [sum(w[k] * d2(Xs[k], i, j) for k in range(K)) for (i, j) in pairs]


def jac_rank(K, n, pairs, cosb, seed=1, bonds=None):
    mp.mp.dps = 60
    rnd = __import__("random").Random(seed)
    alpha = mp.pi - mp.acos(cosb)
    alphas = [alpha] * (n - 2)
    bonds = bonds or [mp.mpf(1)] * (n - 1)
    params = [mp.mpf(rnd.uniform(-3.1, 3.1)) for _ in range(K * (n - 3))]
    raw = [rnd.uniform(1, 3) for _ in range(K)]
    params += [mp.mpf(r / sum(raw)) for r in raw[:-1]]
    h = mp.mpf(10) ** (-20)
    cols = []
    for a in range(len(params)):
        pp = list(params); pm = list(params)
        pp[a] += h; pm[a] -= h
        fp = phi(pp, K, n, pairs, bonds, alphas)
        fm = phi(pm, K, n, pairs, bonds, alphas)
        cols.append([(x - y) / (2 * h) for x, y in zip(fp, fm)])
    J = mp.matrix(len(pairs), len(params))
    for a, col in enumerate(cols):
        for r, v in enumerate(col):
            J[r, a] = v
    S = mp.svd_r(J, compute_uv=False)
    sv = sorted([S[i] for i in range(len(S))], reverse=True)
    rank = sum(1 for s in sv if s > sv[0] * mp.mpf(10) ** (-25))
    return len(params), len(pairs), rank, sv


def band(n, w):
    return [(i, j) for i in range(n) for j in range(i + 3, min(n, i + w + 1))]


def report(label, K, n, pairs, cosb, **kw):
    P, D, r, sv = jac_rank(K, n, pairs, cosb, **kw)
    full = (r == P)
    smallest_kept = sv[r - 1]
    nxt = sv[r] if r < len(sv) else None
    print(f"  {label:40s} K={K} n={n:2d}: params {P:2d}, data {D:2d}, rank {r:2d} -> "
          f"{'FULL column rank' if full else 'DEFICIENT (column rank < params)'}; "
          f"smallest kept sv {mp.nstr(smallest_kept, 5)}" + (f", next sv {mp.nstr(nxt, 3)}" if nxt is not None else ""))
    return full


if __name__ == "__main__":
    for name, cosb in (("cos(bond angle) = -1/3", mp.mpf(-1) / 3), ("bond angle 97 deg", mp.cos(mp.pi * 97 / 180))):
        print(f"== {name}, unit bonds ==")
        report("complete data", 2, 7, band(7, 7), cosb)
        report("complete data", 2, 6, band(6, 6), cosb)
        report("complete data", 2, 8, band(8, 8), cosb)
        report("band w=5 (=K+3), square", 2, 7, band(7, 5), cosb)
        report("band w=5", 2, 8, band(8, 5), cosb)
        report("band w=5", 2, 10, band(10, 5), cosb)
        for n in (7, 8, 9, 10, 12):
            report("band w=4 (=K+2)", 2, n, band(n, 4), cosb)
        report("complete data", 3, 9, band(9, 9), cosb)
        report("complete data", 3, 8, band(8, 8), cosb)
        report("band w=6 (=K+3), square", 3, 11, band(11, 6), cosb)
        report("band w=5 (=K+2)", 3, 11, band(11, 5), cosb)
        report("K=1: band w=3 (=K+2)", 1, 8, band(8, 3), cosb)
        report("K=1: band w=4 (=K+3)", 1, 8, band(8, 4), cosb)
    print("== unequal bond lengths (0.9..1.7), bond angle 97 deg ==")
    rnd = __import__("random").Random(5)
    cosb = mp.cos(mp.pi * 97 / 180)
    for (K, n, w, lab) in ((2, 7, 7, "complete data"), (2, 7, 5, "band w=5, square"), (3, 9, 9, "complete data"), (3, 11, 6, "band w=6, square")):
        bonds = [mp.mpf(rnd.uniform(0.9, 1.7)) for _ in range(n - 1)]
        report(lab, K, n, band(n, w), cosb, bonds=bonds)
