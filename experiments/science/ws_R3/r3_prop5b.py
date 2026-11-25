#!/usr/bin/env python3
"""R3 — independent check of Proposition 5b ("hidden twins") of INFERENCE_LIMITS.md, and of
the referee's own statements about it.  Own code; beta = 1, c = u.

Exact sums over the joint law of the two distances.  For centres a0, a' at Hamming distance D
a point x is described by (i, j): i = #coordinates among the D differing ones where x != a0,
j = #coordinates among the n-D agreeing ones where x differs from both;
    d(x,a0) = i + j,   d(x,a') = D - i + j,   multiplicity binom(D,i) binom(n-D,j).

Referee's identity (exact, any overlap):  with T_s = -u (r1 + s - d')_+ , g' = min(g0, T_s),
    Z' = Z0 + E_s,   N' = N0 + D_s,
    E_s = sum (e^{-T_s} - e^{-g0})_+ ,   D_s = sum [T_s e^{-T_s} - g0 e^{-g0}] 1[T_s < g0],
    U' - U0 = (E_s/(Z0 + E_s)) * (D_s/E_s - U0).
So the twin has the same mean energy iff the mean energy of its EXCESS mass equals U0.
All sums are evaluated relative to Z0 in the log domain (no cancellation in U' - U0).
"""
import math, sys
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def lbinom(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)

def h2(p):
    return -p * math.log(p) - (1 - p) * math.log(1 - p)

class Twin:
    def __init__(self, n, u, r1, D):
        self.n, self.u, self.r1, self.D = n, u, r1, D
        i = np.arange(D + 1)[:, None]; j = np.arange(n - D + 1)[None, :]
        self.lc = lbinom(D, i) + lbinom(n - D, j)          # log multiplicity
        self.d0 = (i + j).astype(float); self.d1 = (D - i + j).astype(float)
        self.g0 = -u * np.maximum(r1 - self.d0, 0.0)
        self.lZ0 = logsumexp(self.lc - self.g0)
        self.U0 = float(np.sum(self.g0 * np.exp(self.lc - self.g0 - self.lZ0)))
        # excess of the visible basin, B0 = Z0/2^n - 1
        self.lnB0 = logsumexp((self.lc + np.log(np.maximum(np.expm1(-self.g0), 1e-300)))[self.g0 < 0]) - n * math.log(2)

    def excess(self, s):
        """E_s/Z0 and D_s/Z0."""
        T = -self.u * np.maximum(self.r1 + s - self.d1, 0.0)
        m = T < self.g0
        lc, g0, T = self.lc[m], self.g0[m], T[m]
        # e^{-T} - e^{-g0} = e^{-T} (1 - e^{T - g0})
        fac = -np.expm1(T - g0)
        E = np.exp(lc - T - self.lZ0) * fac
        Dn = np.exp(lc - T - self.lZ0) * (T - g0 * np.exp(T - g0))
        return float(E.sum()), float(Dn.sum())

    def dU(self, s):
        E, Dn = self.excess(s)
        if E == 0.0:
            return 0.0
        return (E / (1 + E)) * (Dn / E - self.U0)

    def root(self, lo=-1.0, hi=1.0):
        f = lambda s: self.excess(s)[1] - self.U0 * self.excess(s)[0]     # sign of U'-U0
        flo, fhi = f(lo + 1e-12), f(hi - 1e-12)
        if flo * fhi > 0:
            return None, flo, fhi
        s = brentq(f, lo + 1e-12, hi - 1e-12, xtol=1e-15, rtol=1e-15, maxiter=500)
        return s, flo, fhi

def author_cases():
    print("== 1. the note's numbers (u = 1)")
    u = 1.0
    rho0 = math.log(2 / (1 + math.exp(-u))) / u
    print(f"   rho0 = {rho0:.6f}; hinted exponent ln2 - h(rho0) = {math.log(2) - h2(rho0):.6f}")
    for n, dr in ((1000, 0.01), (5000, 0.002)):
        r1 = (rho0 + dr) * n
        for frac in (0.3, 0.45, 0.5):
            D = int(round(frac * n))
            tw = Twin(n, u, r1, D)
            s, flo, fhi = tw.root()
            if s is None:
                print(f"   n={n} rho1=rho0+{dr} D={D}: NO sign change on (-1,1): f(-1)={flo:.3e}, f(1)={fhi:.3e}")
                continue
            E, Dn = tw.excess(s)
            dlnZ = math.log1p(E)
            relU = abs(tw.dU(s)) / abs(tw.U0)
            # cost exponent: ln 2 - (1/n) ln V(n, r1 + 1),  V = #points with d < r1 + 1
            R = math.ceil(r1 + 1) - 1
            lV = logsumexp(lbinom(n, np.arange(R + 1)))
            print(f"   n={n} rho1=rho0+{dr} (r1={r1:.2f}) D={D}: ln B0 = {tw.lnB0:.3f}, U0 = {tw.U0:.4f}; "
                  f"s* = {s:.6f}; |U'-U0|/|U0| = {relU:.1e}; ln Z' - ln Z0 = {dlnZ:.4f}; "
                  f"exponent ln2 - ln V(n,r1+1)/n = {math.log(2) - lV / n:.5f}, ln2 - h(rho1) = {math.log(2) - h2(rho0 + dr):.5f}")

def root_structure():
    print("== 2. when does the root exist?  (u = 1, rho1 = rho0 + 0.01, D = n/2; real r1 as in the note)")
    u = 1.0
    rho0 = math.log(2 / (1 + math.exp(-u))) / u
    for n in (100, 200, 300, 400, 500, 600, 700, 800, 1000):
        r1 = (rho0 + 0.01) * n
        tw = Twin(n, u, r1, n // 2)
        s, flo, fhi = tw.root()
        # scan for monotonicity of s -> U'(s) - U0 on (-1, 1)
        grid = np.linspace(-0.999, 0.999, 81)
        vals = np.array([tw.dU(x) for x in grid])
        nsign = int(np.sum(np.diff(np.sign(vals)) != 0))
        mono = bool(np.all(np.diff(vals) <= 1e-18))
        print(f"   n={n}: ln B0 = {tw.lnB0:7.3f}, |U0| = {abs(tw.U0):8.3f}, B0/|U0| = {math.exp(tw.lnB0) / abs(tw.U0):9.3f}; "
              f"root in (-1,1): {s if s is None else round(s, 5)}; sign changes on grid: {nsign}; "
              f"U'(s)-U0 nonincreasing in s: {mono}")

def disjoint_case():
    print("== 3. referee's disjoint-support statement (u large so that rho0 < 1/4):")
    print("      supports disjoint => U'(0) < U0 always, and U'(-1) > U0 as soon as W/2^n > e^u r1")
    for u in (2.6, 3.0, 4.0):
        rho0 = math.log(2 / (1 + math.exp(-u))) / u
        for n in (60, 120, 240, 480):
            r1 = int(math.floor((rho0 + 0.02) * n)) + 1         # integer radius
            D = 2 * r1 + 2
            if D > n:
                continue
            tw = Twin(n, u, float(r1), D)
            # W/2^n = sum_{d<r1} binom(n,d) e^{u(r1-d)} / 2^n
            d = np.arange(r1)
            lW = logsumexp(lbinom(n, d) + u * (r1 - d)) - n * math.log(2)
            cond = lW > math.log(math.exp(u) * r1)
            f0 = tw.dU(0.0); fm1 = tw.dU(-1.0 + 1e-12)
            s, flo, fhi = tw.root(-1.0, 0.0)
            E, Dn = tw.excess(s) if s is not None else (float('nan'),) * 2
            print(f"   u={u} rho0={rho0:.4f} n={n} r1={r1} D={D}: ln(W/2^n) = {lW:8.3f} vs ln(e^u r1) = {math.log(math.exp(u) * r1):6.3f} "
                  f"(condition {cond}); U'(0)-U0 = {f0:+.3e} (<0), U'(-1)-U0 = {fm1:+.3e}; root s* = "
                  f"{'none' if s is None else f'{s:.6f}'}; ln Z'-ln Z0 = {math.log1p(E) if s is not None else float('nan'):.4f} "
                  f"(>= ln(1+e^-u) - o(1) = {math.log(1 + math.exp(-u)):.4f})")
            if cond:
                assert f0 < 0 and fm1 > 0 and s is not None

def joint_oracle_golay():
    print("== 4. joint oracle (k-body marginals + mean energy) on the extended Golay code, exact on cosets:")
    print("      visible instance g0 = -u (r1 - d(x,C))_+ , twin = -u (r1 + s - d(x, a'+C))_+ ; both C-invariant,")
    print("      so every marginal of order <= 7 is uniform for g0 and for g' (Lemma 1); tune s for equal U.")
    from r3_codes import golay24, rref, span
    from r3_thm2 import coset_distance_table
    G = golay24(); n = 24
    reps, counts, free, piv, words = coset_distance_table(G, n)
    dC = np.argmax(counts > 0, axis=1).astype(float)          # d(x, C) per coset
    size = len(words)
    # index of coset of (rep ^ a'): reduce rep ^ a' to its representative
    R = rref(G)
    def coset_index(v):
        v = v.copy()
        for b in R:
            p = b.bit_length() - 1
            m = ((v >> np.uint64(p)) & np.uint64(1)).astype(bool)
            v[m] ^= np.uint64(b)
        idx = np.zeros(len(v), dtype=np.int64)
        for jj, f in enumerate(free):
            idx |= (((v >> np.uint64(f)) & np.uint64(1)).astype(np.int64) << jj)
        return idx
    for u, r1 in ((5.0, 3.0), (6.0, 3.0), (5.0, 4.0)):
        # choose a' at distance 4 from C (a deep hole)
        deep = int(np.argmax(dC == 4))
        ap = reps[deep]
        dT = dC[coset_index(reps ^ ap)]                         # d(x, a' + C) per coset
        g0 = -u * np.maximum(r1 - dC, 0.0)
        Z0 = size * np.sum(np.exp(-g0)); U0 = size * np.sum(g0 * np.exp(-g0)) / Z0
        def UZ(s):
            g = np.minimum(g0, -u * np.maximum(r1 + s - dT, 0.0))
            Z = size * np.sum(np.exp(-g)); return size * np.sum(g * np.exp(-g)) / Z, Z
        f = lambda s: UZ(s)[0] - U0
        lo, hi = -1.0 + 1e-9, 1.0 - 1e-9
        if f(lo) * f(hi) > 0:
            print(f"   u={u} r1={r1}: no sign change on (-1,1): U'(-1)-U0={f(lo):+.3e}, U'(1)-U0={f(hi):+.3e}; "
                  f"|C| W/2^n = {(Z0 - 2 ** n) / 2 ** n + np.sum(dC < r1) * size / 2 ** n:.2f}")
            continue
        s = brentq(f, lo, hi, xtol=1e-15)
        Us, Zs = UZ(s)
        print(f"   u={u} r1={r1}: Z0/2^n = {Z0 / 2 ** n:.3f}, U0 = {U0:.6f}; s* = {s:.6f}; U' - U0 = {Us - U0:+.1e}; "
              f"ln Z' - ln Z0 = {math.log(Zs / Z0):.4f}; g' differs from g0 on a fraction "
              f"{np.sum(np.minimum(g0, -u * np.maximum(r1 + s - dT, 0.0)) != g0) * size / 2 ** n:.4f} of the cube")

if __name__ == "__main__":
    author_cases()
    root_structure()
    disjoint_case()
    joint_oracle_golay()
