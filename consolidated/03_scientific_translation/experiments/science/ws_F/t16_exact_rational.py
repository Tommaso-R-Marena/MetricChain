"""Lemma 3 / Theorem A in EXACT rational arithmetic (python Fractions) on the whole cube, n = 8, 10:
p, e^{-u}, e^{-gamma}, e^{r} rational  =>  every weight is rational; the compensated base and the cyclically symmetrised
alternative are checked to be in the class and to have IDENTICAL one-body marginals as fractions (no rounding at all)."""
from fractions import Fraction as Fr
import itertools, sys
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()

def run(n, p, z, g_, er, k):
    # z = e^{-u}, g_ = e^{-gamma}, er = e^{r}
    q = 1 - p
    pts = list(itertools.product((0, 1), repeat=n))
    wt = [sum(x) for x in pts]
    pi = [p ** w * q ** (n - w) for w in wt]
    Zg = (q + p * g_) ** n
    w1 = [g_ ** w / Zg for w in wt]                       # normalised additive weight
    pg = p * g_ / (q + p * g_)
    def cone(s):
        d = [sum(a != b for a, b in zip(x, s)) for x in pts]
        c = [z ** dd for dd in d]
        Z = sum(a * b for a, b in zip(pi, c))
        return [cc / Z for cc in c]
    s0 = tuple([1] * k + [0] * (n - k))
    shifts = sorted(set(tuple(s0[(i - j) % n] for i in range(n)) for j in range(n)))
    exc = [Fr(0)] * len(pts)
    for s in shifts:
        c = cone(s)
        for i in range(len(pts)):
            v = er * c[i] - w1[i]
            if v > 0: exc[i] += v / len(shifts)
    E = sum(a * b for a, b in zip(pi, exc))
    cE = sum(a * b * w for a, b, w in zip(pi, exc, wt)) / (n * E)
    pplus = p / (p + q * z); pminus = p * z / (q + p * z)
    p2, g2 = (pplus, 1 / z) if cE > pg else (pminus, z)       # e^{-gamma_2} = e^{u} or e^{-u}
    b = (cE - pg) / (p2 - cE)
    assert b >= 0
    Z2 = (q + p * g2) ** n
    w2 = [g2 ** w / Z2 for w in wt]
    w0 = [a + b * c for a, c in zip(w1, w2)]
    walt = [a + e for a, e in zip(w0, exc)]
    def in_class(w):
        idx = {x: i for i, x in enumerate(pts)}
        for i, x in enumerate(pts):
            for j in range(n):
                y = list(x); y[j] ^= 1
                ratio = w[idx[tuple(y)]] / w[i]
                if ratio > 1 / z or ratio < z: return False
        return True
    def marg(w):
        A = sum(a * b for a, b in zip(pi, w))
        return [sum(a * b for a, b, x in zip(pi, w, pts) if x[i]) / A for i in range(n)], A
    m0, A0 = marg(w0); m1, A1 = marg(walt)
    P(f"n={n} p={p} e^-u={z} e^-gamma={g_} e^r={er} k={k}: b = {b} (= {float(b):.6f}); c_E = {float(cE):.6f}; p_gamma = {float(pg):.6f}")
    P(f"   base in class: {in_class(w0)}; alternative in class: {in_class(walt)}")
    P(f"   one-body marginals identical as fractions at all {n} sites: {m0 == m1}; all equal to c_E: {all(v == cE for v in m0 + m1)}")
    P(f"   A(alt)/A(base) = {float(A1 / A0):.6f} = 1 + E/(1+b): {A1 / A0 == 1 + E / (1 + b)}")
    return m0 == m1

ok = []
ok.append(run(8, Fr(1, 4), Fr(1, 3), Fr(6, 5), Fr(2), 4))
ok.append(run(8, Fr(3, 10), Fr(2, 5), Fr(1), Fr(5, 2), 3))
ok.append(run(10, Fr(1, 10), Fr(1, 7), Fr(3, 2), Fr(3), 5))
P("ALL EXACT:", all(ok))
open('out/t16_exact_rational.txt', 'w').write('\n'.join(out) + '\n')
