"""k = 2, exact, n prime: all one- AND two-body marginals of base and alternative coincide.

G = AGL(1,n) (x -> a x + b on F_n, n prime), sharply 2-transitive, |G| = n(n-1).
Alternative = base + theta * G-average of the excess of a dip of centre type k1 + (1-theta) * same for k2.
A G-invariant measure has all one-body marginals equal to c1 = E|x|/n and all pair marginals determined by
c2 = E|x|(|x|-1)/(n(n-1)).  Base = a * pi_gamma^n + (1-a) * pi_gamma2^n has (c1,c2) = a (p_g, p_g^2) + (1-a)(p_2, p_2^2).
Matching (c1,c2) of the excess X = (x, y), h = y - x^2 > 0, g = x - p_g:
      a = h/(h+g^2),   p_2 = x + h/g      (exact; two-component base again).
A single centre type has h < 0 (sampling without replacement): no mixture of product measures can match it.
"""
import numpy as np, sys, itertools
from sl import *
from t03_enum_adaptive import cube, popcount, in_class
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()


def run(n, p, u, g1, k1, k2, r, theta):
    q = 1 - p
    X, bits, wt = cube(n)
    pi = p ** wt * q ** (n - wt)
    w1 = np.exp(-g1 * wt); w1 /= (pi * w1).sum()
    pg = pgam(p, g1)
    G = [(a, b) for a in range(1, n) for b in range(n)]
    def perm_mask(s, a, b):
        m = 0
        for i in range(n):
            if (s >> i) & 1: m |= 1 << ((a * i + b) % n)
        return m
    def sym_excess(k):
        s0 = (1 << k) - 1
        centres = {}
        for (a, b) in G:
            s = perm_mask(s0, a, b); centres[s] = centres.get(s, 0) + 1
        exc = np.zeros(2 ** n); D = np.zeros(2 ** n, bool)
        for s, mult in centres.items():
            c = np.exp(-u * popcount(X ^ s)); c /= (pi * c).sum()
            Ds = np.exp(r) * c > w1
            exc += mult * np.where(Ds, np.exp(r) * c - w1, 0.0) / len(G); D |= Ds
        return exc, D, len(centres)
    def stats(v):          # mass, c1, c2 of the measure pi*v
        A = (pi * v).sum()
        return A, (pi * v * wt).sum() / (n * A), (pi * v * wt * (wt - 1)).sum() / (n * (n - 1) * A)
    e1, D1, n1 = sym_excess(k1); e2, D2, n2 = sym_excess(k2)
    E1, x1, y1 = stats(e1); E2, x2, y2 = stats(e2)
    exc = theta * e1 + (1 - theta) * e2
    Ex, x, y = stats(exc)
    h = y - x * x; g = x - pg
    P(f"--- n={n} p={p} u={u} gamma={g1:+.4f} (p_gamma={pg:.5f}); centre types {k1},{k2}; depth r={r}; theta={theta}; |G|={len(G)}, orbit sizes {n1},{n2}")
    P(f"    single types: (c1,c2-c1^2) = ({x1:.5f},{y1-x1*x1:+.6f}) and ({x2:.5f},{y2-x2*x2:+.6f})   [negative: below the parabola, no mixture of product measures matches]")
    P(f"    mixed excess: x={x:.6f}, h=y-x^2={h:+.6f}, self-consistency gap g=x-p_gamma={g:+.6f}")
    if h <= 0:
        P("    h <= 0: no exact two-body compensation with these two types"); return None
    a = h / (h + g * g); p2 = x + h / g
    _, p0, p1 = site_laws(p, u, 0.0)
    P(f"    compensation: a={a:.6f} (weight of the hard component), p_2={p2:.6f} (window [{p0[1]:.5f},{p1[1]:.5f}])")
    if not (p0[1] <= p2 <= p1[1]):
        P("    p_2 outside the window"); return None
    g2 = gamma_of_density(p, p2)
    w2 = np.exp(-g2 * wt); w2 /= (pi * w2).sum()
    b = (1 - a) / a
    w0 = w1 + b * w2
    walt = w0 + exc
    ok0, _ = in_class(w0, n, u); ok1, _ = in_class(walt, n, u)
    def margs(w):
        mu = pi * w; A = mu.sum()
        one = (mu[:, None] * bits).sum(0) / A
        two = (bits.T * mu) @ bits / A          # two[i,j] = P(x_i = x_j = 1)
        return one, two, A
    o0, t0, A0 = margs(w0); o1, t1, A1 = margs(walt)
    off = ~np.eye(n, dtype=bool)
    P(f"    in class: base {ok0}, alternative {ok1}")
    P(f"    one-body: base {o0.mean():.12f} (spread {np.ptp(o0):.1e}), alt spread {np.ptp(o1):.1e}, max|alt-base| = {np.abs(o1-o0).max():.2e}")
    P(f"    two-body P(x_i=x_j=1): base {t0[off].mean():.12f} (spread {np.ptp(t0[off]):.1e}), alt spread {np.ptp(t1[off]):.1e}, max|alt-base| over all {n*(n-1)//2} pairs = {np.abs(t1-t0)[off].max():.2e}")
    P(f"    separation ln A(alt)/A(base) = {np.log(A1/A0):.6f};  |difference set| = {int((D1|D2).sum())} of {2**n}")
    # control: three-body marginals differ (the oracle of order 3 would separate)
    mu0 = pi * w0 / A0; mu1 = pi * walt / A1
    d3 = max(abs((mu1 * bits[:, i] * bits[:, j] * bits[:, l]).sum() - (mu0 * bits[:, i] * bits[:, j] * bits[:, l]).sum())
             for i, j, l in itertools.combinations(range(n), 3))
    P(f"    control: max difference of three-body marginals P(x_i=x_j=x_l=1): {d3:.2e} (not matched, as expected)")
    return np.abs(o1 - o0).max(), np.abs(t1 - t0)[off].max()

res = []
for (n, p, u, f, k1, k2, r, th) in ((11, 0.3, 1.0, 0.0, 3, 8, 1.0, 0.5), (13, 0.3, 1.0, 0.0, 4, 9, 1.0, 0.5), (13, 0.1, 2.0, 0.3, 4, 10, 1.5, 0.5), (13, 0.2, 1.5, 0.2, 5, 9, 1.2, 0.4)):
    E = E_threshold(p, u)
    R, t, m, Q, g = Rmax(p, u, f * E, return_all=True)
    res.append(run(n, p, u, g, k1, k2, r, th))
P("\nSUMMARY: max one-body deviation:", max(r[0] for r in res if r), " max two-body deviation:", max(r[1] for r in res if r))
open('out/t08_k2_exact.txt', 'w').write('\n'.join(out) + '\n')
