"""r10_09: the negative result of Y_REPORT 8.3 -- class-wise quantiles of an admissible residual
are not admissible for Markov-type classes (first letter + pair counts).  Own code.

Definitions (theory report, remark after Theorem 11.76): for a partition into classes and
0 < q < 1, the class-wise level  t(x) = max{ c : dens_x{psi < c} <= q }  (= the
(floor(q m)+1)-th smallest value of psi in the class of x, m = class size), the truncated
residual  psi^tr = max(psi, t).  For orbits of a group of isometries, t is admissible
(`lowDens_shift`), hence so is psi^tr.

 1. the explicit example of Y 8.3, verified literally for n = 5..9;
 2. brute force, n = 9: random admissible residuals x quantiles; violations of
    (i) t(a) - t(b) <= d(a,b)  and  (ii) psi^tr(a) - psi^tr(b) <= d(a,b)
    for Markov-type classes and, as a control, for the type classes of the cube.
"""
import time
import numpy as np

t0 = time.time()
u = 1.0
rng = np.random.default_rng(8)


def bits(n):
    k = np.arange(1 << n)
    return ((k[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)


def markov_classes(n):
    x = bits(n)                      # x[:,0] = first letter
    a, b = x[:, :-1].astype(int), x[:, 1:].astype(int)
    key = x[:, 0].astype(int)
    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        key = key * (n + 1) + ((a == i) & (b == j)).sum(axis=1)
    _, inv = np.unique(key, return_inverse=True)
    return inv


def type_classes(n):
    return bits(n).sum(axis=1)


def levels(psi, cls, q):
    t = np.empty_like(psi)
    for c in np.unique(cls):
        idx = np.nonzero(cls == c)[0]
        v = np.sort(psi[idx])
        t[idx] = v[int(np.floor(q * len(idx) + 1e-12))] if q * len(idx) < len(idx) else v[-1]
    return t


def worst_edge_violation(f, n):
    """max over Hamming neighbours (a,b) of f(a) - f(b) - u  (in units of flips: divide by u)."""
    N = 1 << n
    k = np.arange(N)
    w = -np.inf
    for i in range(n):
        nb = k ^ (1 << i)
        w = max(w, float((f - f[nb]).max()) - u)
    return w


# ---------------------------------------------------------------- 1. the explicit example
print("1. explicit example of Y 8.3:  psi = u*d_H(., 0...010),  x = 110...0,  y = 010...0,  q < 1/(n-2)")
for n in range(5, 10):
    X = bits(n)
    cls = markov_classes(n)
    y0 = np.zeros(n, dtype=int); y0[n - 2] = 1          # 0...010 (sites 1..n, the one at site n-1)
    psi = u * (X != y0[None, :]).sum(axis=1).astype(float)
    xv = np.zeros(n, dtype=int); xv[0] = 1; xv[1] = 1   # 110...0
    yv = np.zeros(n, dtype=int); yv[1] = 1              # 010...0
    ix = int((xv * (1 << np.arange(n))).sum()); iy = int((yv * (1 << np.arange(n))).sum()); iy0 = int((y0 * (1 << np.arange(n))).sum())
    q = 0.9 / (n - 2)
    t = levels(psi, cls, q)
    szx = int((cls == cls[ix]).sum()); szy = int((cls == cls[iy]).sum())
    print("   n=%d: |class(x)|=%d, |class(y)|=%d (y0 in class(y): %s); psi(x)=%g, t(x)=%g (weight level e^-%g); psi over class(y): %s, t(y)=%g; d(x,y)=%g;  t(x)-t(y) = %g > d(x,y) = %g : level function NOT admissible; psi^tr(x)-psi^tr(y) = %g"
          % (n, szx, szy, cls[iy0] == cls[iy], psi[ix], t[ix], t[ix], sorted(set(psi[cls == cls[iy]].tolist())), t[iy],
             u * (xv != yv).sum(), t[ix] - t[iy], u * (xv != yv).sum(), max(psi[ix], t[ix]) - max(psi[iy], t[iy])))

# ---------------------------------------------------------------- 2. brute force
n = 9
N = 1 << n
X = bits(n)
D = (X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float) * u
clsM = markov_classes(n)
clsT = type_classes(n)
print("\n2. brute force n=%d: %d Markov-type classes (sizes %d..%d), %d type classes" % (
    n, len(np.unique(clsM)), np.bincount(clsM).min(), np.bincount(clsM).max(), len(np.unique(clsT))))


def random_member(kind):
    if kind == 0:
        r = rng.normal(size=N) * rng.uniform(1.0, 4.0)
        return (r[None, :] + D).min(axis=1)
    if kind == 1:
        return D[:, rng.integers(N)].copy()
    if kind == 2:
        ys = rng.integers(N, size=rng.integers(2, 6))
        return (D[:, ys] + rng.uniform(0, 2, size=len(ys))[None, :]).min(axis=1)
    r1 = rng.normal(size=N) * 3; r2 = rng.normal(size=N) * 3
    return np.maximum((r1[None, :] + D).min(axis=1), (r2[None, :] + D).min(axis=1))


res = {("M", "level"): 0, ("M", "trunc"): 0, ("T", "level"): 0, ("T", "trunc"): 0}
worst = {k: 0.0 for k in res}
cases = 0
first_example = None
for j in range(200):
    psi = random_member(j % 4)
    assert worst_edge_violation(psi, n) < 1e-9
    for q in (0.05, 0.2, 0.5):
        cases += 1
        for name, cls in (("M", clsM), ("T", clsT)):
            t = levels(psi, cls, q)
            v1 = worst_edge_violation(t, n)
            v2 = worst_edge_violation(np.maximum(psi, t), n)
            if v1 > 1e-9:
                res[(name, "level")] += 1
            if v2 > 1e-9:
                res[(name, "trunc")] += 1
            worst[(name, "level")] = max(worst[(name, "level")], v1)
            worst[(name, "trunc")] = max(worst[(name, "trunc")], v2)
print("   %d cases (200 residuals x 3 quantiles)" % cases)
for name, lab in (("M", "Markov types"), ("T", "type classes of the cube")):
    print("   %-26s level function t inadmissible in %d cases (largest excess %.2f flips);  truncated residual max(psi,t) inadmissible in %d cases (largest excess %.2f flips)"
          % (lab, res[(name, "level")], worst[(name, "level")] / u, res[(name, "trunc")], worst[(name, "trunc")] / u))
print("time %.1fs" % (time.time() - t0))
