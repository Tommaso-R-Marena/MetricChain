"""Independent replication of theory report Theorem 11.105 (commit dcdfea6, section 11.28): the robust range of a
ratio of macrostate weights.  Own code; nothing imported from the theory division.

For random finite spaces X, weights w > 0, an asymmetric envelope d with the triangle inequality (shortest-path
closure of random arc lengths), and random disjoint A, B (not covering X):
  P_full : sup Z_g(A)/Z_g(B) over all admissible g on X          (linear programme in t = e^{-g}, Charnes-Cooper)
  P_rel  : the same with ONLY the constraints from B to A         (Theorem 11.105(a) says: equal to P_full)
  D_bip  : the bipartite transport programme with gains           (Theorem 11.105(c) says: equal)
and the closed forms (d) (one state) and the sandwich (e).  Controls:
  * an envelope WITHOUT the triangle inequality: (a) must be able to fail (P_full < P_rel);
  * the threshold case of Theorem 11.106 on the cube against our own addendum A11 (maximal field).

Solver: HiGHS with tolerances 1e-10 and scaled variables (default tolerances fake violations of exact
statements: DEAD_ENDS.md SD17).

Usage: python3 ratio_duality_replication.py        (about 20 s)
"""
from __future__ import annotations
import math, itertools
import numpy as np
from scipy.optimize import linprog

OPT = {"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10}

def closure(L):
    """shortest-path closure (Floyd-Warshall): a quasi-metric"""
    d = L.copy(); n = len(d)
    for k in range(n):
        d = np.minimum(d, d[:, k][:, None] + d[k, :][None, :])
    np.fill_diagonal(d, 0.0)
    return d

def primal(w, d, A, B, pairs):
    """max sum_A w t  s.t. sum_B w t = 1, t(y) <= e^{d(x,y)} t(x) for (x,y) in pairs, t >= 0.
    Variables scaled: v = w t."""
    N = len(w); rows = []; 
    for (x, y) in pairs:
        r = np.zeros(N); r[y] = 1.0/w[y]; r[x] = -math.exp(d[x, y])/w[x]; rows.append(r)
    c = np.zeros(N); c[A] = -1.0
    aeq = np.zeros((1, N)); aeq[0, B] = 1.0
    res = linprog(c, A_ub=np.array(rows) if rows else None, b_ub=np.zeros(len(rows)) if rows else None,
                  A_eq=aeq, b_eq=[1.0], bounds=[(0, None)]*N, method="highs", options=OPT)
    assert res.status == 0, res.message
    return -res.fun

def dual_bipartite(w, d, A, B):
    """min lam s.t. sum_y e^{d(z,y)} psi(z,y) <= lam w(z) (z in B), sum_z psi(z,y) >= w(y) (y in A), psi >= 0.
    Variables scaled: phi(z,y) = psi(z,y)/w(y)."""
    nb, na = len(B), len(A); nv = nb*na + 1
    c = np.zeros(nv); c[-1] = 1.0
    rows = []; rhs = []
    for i, z in enumerate(B):
        r = np.zeros(nv)
        for j, y in enumerate(A): r[i*na + j] = math.exp(d[z, y])*w[y]/w[z]
        r[-1] = -1.0; rows.append(r); rhs.append(0.0)
    for j, y in enumerate(A):
        r = np.zeros(nv)
        for i in range(nb): r[i*na + j] = -1.0
        rows.append(r); rhs.append(-1.0)
    res = linprog(c, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(0, None)]*nv, method="highs", options=OPT)
    assert res.status == 0, res.message
    return res.fun

def instance(rng, N, tri=True):
    w = np.exp(rng.normal(0, 1.5, N))
    L = rng.uniform(0.1, 3.0, (N, N))
    d = closure(L) if tri else L - np.diag(np.diag(L))
    idx = rng.permutation(N); na = int(rng.integers(1, max(2, N//2))); nb = int(rng.integers(1, max(2, N//2)))
    A = list(idx[:na]); B = list(idx[na:na + nb])
    return w, d, A, B

def main():
    rng = np.random.default_rng(20261125)
    worst = 0.0; nfull = 0; sand = 0; one = 0
    for trial in range(400):
        N = int(rng.integers(4, 13)); w, d, A, B = instance(rng, N)
        allpairs = [(x, y) for x in range(N) for y in range(N) if x != y]
        ba = [(z, y) for z in B for y in A]
        pf = primal(w, d, A, B, allpairs); pr = primal(w, d, A, B, ba); db = dual_bipartite(w, d, A, B)
        dev = max(abs(math.log(pf/pr)), abs(math.log(pf/db))); worst = max(worst, dev); nfull += 1
        assert dev < 1e-7, (trial, pf, pr, db)
        M = max(min(math.exp(d[z, y])*w[y]/w[z] for z in B) for y in A)
        assert M/len(B) <= pf*(1 + 1e-9) and pf <= len(A)*M*(1 + 1e-9); sand += 1
        if len(A) == 1:
            y = A[0]; cf = w[y]/sum(w[z]*math.exp(-d[z, y]) for z in B)
            assert abs(math.log(pf/cf)) < 1e-7; one += 1
        if len(B) == 1:
            z = B[0]; cf = sum(w[y]*math.exp(d[z, y]) for y in A)/w[z]
            assert abs(math.log(pf/cf)) < 1e-7; one += 1
    print(f"Theorem 11.105 (a), (c): {nfull} random instances (4..12 states, asymmetric envelopes, A and B not covering X): "
          f"full programme = B->A programme = bipartite dual, largest |ln ratio| = {worst:.1e}")
    print(f"Theorem 11.105 (e) sandwich: {sand} instances, no violation;  (d) one-state closed forms: {one} instances, agree to 1e-7")
    # control: without the triangle inequality (a) can fail
    fail = 0; tot = 0; big = 0.0
    for trial in range(400):
        N = int(rng.integers(4, 10)); w, d, A, B = instance(rng, N, tri=False)
        allpairs = [(x, y) for x in range(N) for y in range(N) if x != y]
        ba = [(z, y) for z in B for y in A]
        pf = primal(w, d, A, B, allpairs); pr = primal(w, d, A, B, ba); tot += 1
        assert pf <= pr*(1 + 1e-9)
        if pf < pr*(1 - 1e-6): fail += 1; big = max(big, math.log(pr/pf))
    print(f"control, envelopes without the triangle inequality: B->A programme strictly larger than the full one in {fail} of {tot} "
          f"instances (largest ln ratio {big:.2f}) -- the triangle inequality is used")
    # threshold case on the cube: Theorem 11.106 against addendum A11 (maximal field), uniform and exchangeable weights
    devs = []
    for n in (4, 6, 8):
        X = np.array(list(itertools.product([0, 1], repeat=n))); N = len(X); wt = X.sum(axis=1)
        for u in (0.5, 1.3):
            for kind in ("uniform", "exchangeable, non-monotone"):
                Wj = np.ones(n + 1) if kind == "uniform" else np.exp(rng.normal(0, 1.0, n + 1))
                w = Wj[wt]
                d = u*(X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float)
                for (lo, hi) in ((n//2, n//2 + 1), (1, n - 1)):          # B = {|x| <= lo}, A = {|x| >= hi}
                    A = [k for k in range(N) if wt[k] >= hi]; B = [k for k in range(N) if wt[k] <= lo]
                    edges = [(k, k ^ (1 << i)) for k in range(N) for i in range(n)]
                    # states as integers: rebuild index -> product order
                    code = (X*(1 << np.arange(n))[None, :]).sum(axis=1); pos = {int(c): k for k, c in enumerate(code)}
                    pairs = [(k, pos[int(code[k]) ^ (1 << i)]) for k in range(N) for i in range(n)]
                    pf = primal(w, d, A, B, pairs)                  # single-flip constraints generate the class
                    cf = sum(w[k]*math.exp(u*wt[k]) for k in A)/sum(w[k]*math.exp(u*wt[k]) for k in B)
                    devs.append(abs(math.log(pf/cf)))
    print(f"Theorem 11.106, two sides of a threshold on the cube (n = 4, 6, 8; uniform and random exchangeable weights; "
          f"with and without a gap): full programme = maximal-field formula, largest |ln ratio| = {max(devs):.1e} over {len(devs)} cases")
    assert max(devs) < 1e-7

if __name__ == "__main__":
    main()
