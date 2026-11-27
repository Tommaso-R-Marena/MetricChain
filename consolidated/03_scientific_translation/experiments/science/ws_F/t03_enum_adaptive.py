"""N5a: exhaustive enumeration (n <= 16) of the compensated adaptive construction.

Base        w0   = w~_{g1} + b * w~_{g2}                     (two additive components, normalised weights)
Alternative w_s  = w0 + (1/n) sum_j ( e^r cone~_{sigma^j s} - w~_{g1} )_+     (cyclically symmetrised dip excess)
Checked exactly on the whole cube:
  (i)   both are in the class (all single-flip weight ratios within [e^-u, e^u]);
  (ii)  all n one-body marginals of mu_{w0} and of mu_{w_s} coincide (to rounding);
  (iii) ln A(w_s) - ln A(w0) = ln(1 + E/(1+b));
  (iv)  the set where they differ, and the exact packing bound |T_k| / max_x #{s in T_k : x in union of shifts of D_s}
        against the union bound n * max_x #{s : x in D_s} used in the proof;
  (v)   what the oracle would see WITHOUT compensation (b = 0): the marginal gap.
"""
import numpy as np, itertools, sys
from math import comb
from sl import *

out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()


def cube(n):
    X = np.arange(2 ** n, dtype=np.int64)
    bits = ((X[:, None] >> np.arange(n)) & 1).astype(np.int8)     # bits[x,i]
    wt = bits.sum(1)
    return X, bits, wt


def popcount(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


def in_class(w, n, u, tol=1e-11):
    X = np.arange(len(w))
    worst = 0.0
    for i in range(n):
        r = np.log(w[X ^ (1 << i)] / w)
        worst = max(worst, np.abs(r).max())
    return worst <= u * (1 + tol) + tol, worst


def marginals(pi, w, bits):
    mu = pi * w
    A = mu.sum()
    return (mu[:, None] * bits).sum(0) / A, A


def rot(s, j, n):
    return ((s << j) | (s >> (n - j))) & ((1 << n) - 1) if j else s


def run(n, p, u, g1, k, eps, label=''):
    q = 1 - p
    X, bits, wt = cube(n)
    pi = p ** wt * q ** (n - wt)
    w1 = np.exp(-g1 * wt); w1 /= (pi * w1).sum()
    s0 = (1 << k) - 1                         # centre: k ones (a block; its cyclic orbit has n elements if 0<k<n)
    dist = lambda s: popcount(X ^ s)
    def cone(s):
        c = np.exp(-u * dist(s)); return c / (pi * c).sum()
    p1g = pgam(p, g1)

    # choose the depth r by bisection so that the separation after compensation is eps (+1e-9)
    def build(r):
        c = cone(s0)
        D = np.exp(r) * c > w1
        exc = np.where(D, np.exp(r) * c - w1, 0.0)
        E = (pi * exc).sum()
        cE = (pi * exc * wt).sum() / (n * E)
        g2 = -u if cE > p1g else u
        p2 = pgam(p, g2)
        b = (cE - p1g) / (p2 - cE)
        sep = np.log1p(E / (1 + b))
        return D, exc, E, cE, g2, p2, b, sep
    lo, hi = 0.0, eps + 20
    for _ in range(200):
        mid = (lo + hi) / 2
        if build(mid)[-1] > eps + 1e-9: hi = mid
        else: lo = mid
    r = hi
    D, exc, E, cE, g2, p2, b, sep = build(r)
    assert b >= 0, b
    w2 = np.exp(-g2 * wt); w2 /= (pi * w2).sum()
    w0 = w1 + b * w2
    # symmetrised alternative
    orbit = sorted(set(rot(s0, j, n) for j in range(n)))
    excbar = np.zeros_like(w0); Dbar = np.zeros(len(w0), bool)
    for s in orbit:
        c = cone(s)
        Ds = np.exp(r) * c > w1
        excbar += np.where(Ds, np.exp(r) * c - w1, 0.0) / len(orbit)
        Dbar |= Ds
    walt = w0 + excbar
    ok0, worst0 = in_class(w0, n, u); ok1, worst1 = in_class(walt, n, u)
    m0, A0 = marginals(pi, w0, bits); m1, A1 = marginals(pi, walt, bits)
    # uncompensated: base w1, alternative w1 + excbar
    mu0, _ = marginals(pi, w1, bits); mu1, _ = marginals(pi, w1 + excbar, bits)
    # single unsymmetrised dip on the compensated base: the oracle reveals the centre
    ms, _ = marginals(pi, w0 + exc, bits)
    # exact packing numbers: for every centre s of type k, the difference set of its symmetrised alternative
    Tk = [sum(1 << i for i in c) for c in itertools.combinations(range(n), k)]
    cnt_single = np.zeros(len(w0), np.int32)
    for s in Tk:
        cnt_single += (np.exp(r) * cone(s) > w1)
    exact_union = None
    if n <= 12:
        cnt_union = np.zeros(len(w0), np.int32)
        Dsingle = {s: (np.exp(r) * cone(s) > w1) for s in Tk}
        for s in Tk:
            U = np.zeros(len(w0), bool)
            for j in range(n): U |= Dsingle[rot(s, j, n)]
            cnt_union += U
        exact_union = cnt_union.max()
    NT = len(Tk)
    LB_union_bound = NT / (n * cnt_single.max())
    P(f"--- n={n} p={p} u={u} gamma1={g1:+.4f} k={k} eps={eps} {label}")
    P(f"    depth r={r:.6f}  excess E={E:.6f}  excess density c_E={cE:.6f}  (cone density c_0={cone_density(p,u,k/n):.6f}; base comp. density p_g1={p1g:.6f})")
    P(f"    compensator gamma2={g2:+.2f} (p_2={p2:.6f}), b={b:.6f}  => base density (p_g1+b p_2)/(1+b)={(p1g+b*p2)/(1+b):.6f}")
    P(f"    (i)  in class: base {ok0} (max |ln ratio|={worst0:.6f}), alternative {ok1} ({worst1:.6f}); u={u}")
    P(f"    (ii) one-body marginals: base all = {m0.mean():.12f} (spread {np.ptp(m0):.1e}); alt all = {m1.mean():.12f} (spread {np.ptp(m1):.1e}); max |alt - base| = {np.abs(m1-m0).max():.2e}")
    P(f"    (iii) ln A(alt) - ln A(base) = {np.log(A1/A0):.9f}  (formula ln(1+E/(1+b)) = {sep:.9f}; required > eps = {eps})")
    P(f"    (iv) |difference set| = {int(Dbar.sum())} of {2**n} ; pi-mass of it under base Gibbs = {(pi*w0)[Dbar].sum()/A0:.3e}")
    P(f"         packing: |T_k|={NT}, max_x #{{s: x in D_s}} = {cnt_single.max()}, union bound LB = |T_k|/(n*max) = {LB_union_bound:.3f}" + (f", exact max_x #{{s: x in orbit-union}} = {exact_union} -> exact LB = {NT/exact_union:.3f}" if exact_union else ""))
    P(f"    (v)  WITHOUT compensation (base = additive gamma1): marginals base {mu0.mean():.9f}, alt {mu1.mean():.9f}: gap {mu1.mean()-mu0.mean():+.3e}  (the oracle separates them)")
    P(f"         single (unsymmetrised) dip: marginals range from {ms.min():.6f} to {ms.max():.6f} (reveals the centre)")
    return dict(n=n, r=r, E=E, cE=cE, b=b, sep=sep, dev=np.abs(m1 - m0).max(), ok=ok0 and ok1)


if __name__ == '__main__':
    res = []
    for (n, p, u, f) in ((8, 0.3, 1.0, 0.0), (12, 0.3, 1.0, 0.0), (12, 0.1, 2.0, 0.0), (12, 0.1, 2.0, 0.3), (14, 0.2, 1.5, 0.2), (16, 0.3, 1.0, 0.3), (16, 0.1, 2.0, 0.3)):
        E = E_threshold(p, u)
        R, t, m, Q, g = Rmax(p, u, f * E, return_all=True)
        eps = max(f * E * n, 0.5)             # extensive accuracy eps1*n, or the bounded accuracy 0.5 when f=0
        k = int(round(m * n))
        res.append(run(n, p, u, g, k, eps, label=f"[gamma*,m* of e={f}E: gamma*={g:+.4f}, m*={m:.4f}, R^max={R:.5f}]"))
    # a non-optimal instance for contrast: the zero residual with compensation (any base component can be compensated)
    res.append(run(12, 0.2, 1.0, 0.0, 6, 0.5, label="[base component = zero residual]"))
    P("\nSUMMARY: all in class:", all(r['ok'] for r in res), "; max |marginal(alt) - marginal(base)| over all runs:", max(r['dev'] for r in res))
    open('out/t03_enum_adaptive.txt', 'w').write('\n'.join(out) + '\n')
