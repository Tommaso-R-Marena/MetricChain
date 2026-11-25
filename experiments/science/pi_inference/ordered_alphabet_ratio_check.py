"""Ordered alphabets: the stochastic sandwich of addendum A11 beyond binary sites (A11, remark 1; A13).

X = {0..q-1}^n with the product order.  Site-additive envelope d(x,y) = sum_i d_i(x_i, y_i), each d_i a
quasi-metric on {0..q-1}; g admissible iff g(x) - g(y) <= d(x,y).  Known part f submodular on the
product lattice (here: site terms + convex functions of differences of neighbouring sites).

Claim (A13).  With the step fields
    Gup(x) = sum_i sum_{r < x_i} d_i(r+1, r),      Gdn(x) = sum_i sum_{r < x_i} d_i(r, r+1),
for every admissible g:   mu_{f+Gup} <=_st mu_{f+g} <=_st mu_{f-Gdn}.
So for an up-set B, A its complement:   R(f-Gdn) <= Z_{f+g}(A)/Z_{f+g}(B) <= R(f+Gup).
The bounds are attained in the class iff the fields are admissible, which holds when every d_i is
additive along the order ("path envelope"); for the discrete envelope c_i [s != t] with q >= 3 they
are valid and not attained.

Checked by exact linear programming over the weight cone (scaled variables, tolerance 1e-10).
"""
import itertools, math
import numpy as np
from scipy.optimize import linprog

def lp_ratio(X, f, dsite, inA, sense):
    N, n = X.shape; q = dsite[0].shape[0]
    idx = {tuple(x): k for k, x in enumerate(X)}
    rows = []
    for k, x in enumerate(X):
        for i in range(n):
            for t in range(q):
                if t == x[i]: continue
                y = x.copy(); y[i] = t; l = idx[tuple(y)]
                # g(y) - g(x) <= d_i(y_i, x_i)  <=>  w(x) <= e^{d_i(y_i,x_i)} w(y);  scaled v = e^{-f} w
                r = np.zeros(N); r[k] = 1; r[l] = -math.exp(dsite[i][t, x[i]] + f[l] - f[k]); rows.append(r)
    A = np.array(rows)
    cA = inA.astype(float); cB = (~inA).astype(float)
    res = linprog(-sense*cA, A_ub=A, b_ub=np.zeros(len(rows)), A_eq=cB[None, :], b_eq=[1.0],
                  bounds=[(0, None)]*N, method="highs",
                  options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    assert res.status == 0, res.message
    assert float(np.max(A @ res.x)) < 1e-9
    return float(cA @ res.x)

def ratio(f, G, inA):
    w = np.exp(-f - G); return float(w[inA].sum()/w[~inA].sum())

def random_upset(X, rng):
    N = len(X)
    while True:
        gens = X[rng.choice(N, size=rng.integers(1, 4), replace=False)]
        inB = np.zeros(N, bool)
        for g in gens: inB |= np.all(X >= g, axis=1)
        if 0 < inB.sum() < N: return ~inB

def run(kind, n, q, trials, rng):
    X = np.array(list(itertools.product(range(q), repeat=n)), dtype=int); N = len(X)
    worst_valid = -1e9; gap_hi = gap_lo = 0.0; attained = 0
    for _ in range(trials):
        h = rng.normal(0, 0.7, (n, q))
        f = sum(h[i][X[:, i]] for i in range(n)).astype(float)
        for i in range(n-1):
            J = abs(rng.normal(0, 0.5)); p = rng.choice((1.0, 2.0))
            f = f + J*np.abs(X[:, i] - X[:, i+1])**p          # convex in the difference: submodular
        dsite = []
        for i in range(n):
            d = np.zeros((q, q))
            if kind == "path":
                up = rng.uniform(0.1, 1.0, q-1); dn = rng.uniform(0.1, 1.0, q-1)
                for s in range(q):
                    for t in range(q):
                        if s > t: d[s, t] = up[t:s].sum()      # raising t -> s
                        if s < t: d[s, t] = dn[s:t].sum()      # lowering t -> s
            else:                                               # discrete envelope c [s != t]
                c = rng.uniform(0.1, 1.0); d[:] = c; np.fill_diagonal(d, 0.0)
            dsite.append(d)
        Gup = sum(np.array([sum(dsite[i][r+1, r] for r in range(s)) for s in range(q)])[X[:, i]] for i in range(n))
        Gdn = sum(np.array([sum(dsite[i][r, r+1] for r in range(s)) for s in range(q)])[X[:, i]] for i in range(n))
        inA = random_upset(X, rng)
        hi = lp_ratio(X, f, dsite, inA, +1); lo = lp_ratio(X, f, dsite, inA, -1)
        bhi = ratio(f, Gup, inA); blo = ratio(f, -Gdn, inA)
        v = max(math.log(hi/bhi), math.log(blo/lo)); worst_valid = max(worst_valid, v)   # must be <= 0
        ghi = math.log(bhi/hi); glo = math.log(lo/blo)
        gap_hi = max(gap_hi, ghi); gap_lo = max(gap_lo, glo); attained += (ghi < 1e-8 and glo < 1e-8)
    print(f"{kind:8s} envelope, q={q}, n={n}: {trials} instances; largest violation of the sandwich (ln, must be <= 0) = {worst_valid:+.1e}; "
          f"bound attained in {attained}; largest slack ln(bound/LP): upper {gap_hi:.3f}, lower {gap_lo:.3f}")
    assert worst_valid < 1e-8
    return attained

if __name__ == "__main__":
    rng = np.random.default_rng(20261125)
    for (n, q) in ((3, 3), (4, 3), (3, 4)):
        a = run("path", n, q, 60, rng); assert a == 60
    for (n, q) in ((3, 3), (4, 3), (3, 4)):
        run("discrete", n, q, 60, rng)
    print("OK")
