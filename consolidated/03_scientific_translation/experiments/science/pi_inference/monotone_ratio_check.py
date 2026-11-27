"""Check of the stochastic-domination theorem for robust macrostate ratios
(INFERENCE_LIMITS_ADDENDA.md A11).

Cube {0,1}^n, known part f, envelope d(x,y) = sum_{i: x_i=1,y_i=0} cup_i + sum_{i: x_i=0,y_i=1} cdn_i
(convention g(x) - g(y) <= d(x,y); cup_i = cost bound for raising site i, cdn_i for lowering it).
Claim: if f is submodular and B is an up-set, A its complement, then over all admissible g

    max_g Z_{f+g}(A)/Z_{f+g}(B)  is attained at the field  g = +sum_i cup_i x_i ,
    min_g Z_{f+g}(A)/Z_{f+g}(B)  is attained at the field  g = -sum_i cdn_i x_i ,

and more generally mu_{f + cup.x} <=_st mu_{f+g} <=_st mu_{f - cdn.x}.
The exact extremes are computed by linear programming over the weight cone (Charnes-Cooper).
Also: controls where a hypothesis is dropped (frustrated f; non-monotone B), to see whether the
field is still optimal, and the thermodynamic-integration formula for the width.
beta = 1 throughout.
"""
import itertools, math, sys
import numpy as np
from scipy.optimize import linprog

def cube(n):
    return np.array(list(itertools.product((0, 1), repeat=n)), dtype=int)

def lp_ratio(X, f, cup, cdn, inA, sense):
    """max (sense=+1) or min (sense=-1) of sum_A e^{-f}w / sum_B e^{-f}w over the weight cone
    {w >= 0 : w(x) <= e^{d(y,x)} w(y)}, by the Charnes-Cooper transformation.  Written in the scaled
    variables v(x) = e^{-f(x)} w(x) and solved with tight tolerances: with HiGHS defaults and unscaled
    variables three of 900 instances showed spurious deviations of 1e-6 .. 1e-5 (energy range 14-17)."""
    N, n = X.shape
    idx = {tuple(x): k for k, x in enumerate(X)}
    rows, rhs = [], []
    for k, x in enumerate(X):
        for i in range(n):
            if x[i] == 0:
                y = x.copy(); y[i] = 1; l = idx[tuple(y)]
                # g(y) - g(x) <= cup_i  <=>  w(x) <= e^{cup_i} w(y)
                r = np.zeros(N); r[k] = 1; r[l] = -math.exp(cup[i] + f[l] - f[k]); rows.append(r); rhs.append(0.0)
                # g(x) - g(y) <= cdn_i  <=>  w(y) <= e^{cdn_i} w(x)
                r = np.zeros(N); r[l] = 1; r[k] = -math.exp(cdn[i] + f[k] - f[l]); rows.append(r); rhs.append(0.0)
    cA = inA.astype(float); cB = (~inA).astype(float)
    res = linprog(-sense*cA, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=cB[None, :], b_eq=[1.0],
                  bounds=[(0, None)]*N, method="highs",
                  options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    assert res.status == 0, res.message
    assert float(np.max(np.array(rows) @ res.x)) < 1e-9
    return float(cA @ res.x)

def field_ratio(X, f, h, inA):
    w = np.exp(-f - X @ h)
    return float(w[inA].sum()/w[~inA].sum())

def random_upset(X, rng):
    """complement of the down-closure of a few random points, made non-trivial."""
    N, n = X.shape
    while True:
        gens = X[rng.choice(N, size=rng.integers(1, 4), replace=False)]
        inB = np.zeros(N, bool)
        for gpt in gens:
            inB |= np.all(X >= gpt, axis=1)
        if 0 < inB.sum() < N:
            return ~inB           # inA

def is_submodular(X, f):
    idx = {tuple(x): k for k, x in enumerate(X)}
    worst = 0.0
    for a in range(len(X)):
        for b in range(len(X)):
            j = idx[tuple(np.maximum(X[a], X[b]))]; m = idx[tuple(np.minimum(X[a], X[b]))]
            worst = max(worst, f[j] + f[m] - f[a] - f[b])
    return worst <= 1e-12

def pair_energy(X, J, h):
    s = X.astype(float)
    return s @ h + 0.5*np.einsum("ki,ij,kj->k", s, J, s)

def run(kind, n, trials, rng, monotone=True):
    X = cube(n); N = len(X)
    worst_hi = worst_lo = 0.0; strict = 0; tested = 0
    for _ in range(trials):
        h = rng.normal(0, 1, n)
        J = np.zeros((n, n))
        if kind != "additive":
            for i in range(n):
                for j in range(i+1, n):
                    if rng.random() < 0.7:
                        v = abs(rng.normal(0, 1))
                        if kind == "ferro": v = -v            # energy -|J| x_i x_j : submodular
                        elif kind == "frustrated": v = rng.choice((-1, 1))*v
                        J[i, j] = J[j, i] = v
        f = pair_energy(X, J, h)
        if kind in ("additive", "ferro"): assert is_submodular(X, f)
        cup = rng.uniform(0.1, 1.5, n); cdn = rng.uniform(0.1, 1.5, n)
        if monotone: inA = random_upset(X, rng)
        else:
            inA = rng.random(N) < 0.5
            if inA.all() or not inA.any(): continue
        hi = lp_ratio(X, f, cup, cdn, inA, +1); lo = lp_ratio(X, f, cup, cdn, inA, -1)
        fhi = field_ratio(X, f, +cup, inA); flo = field_ratio(X, f, -cdn, inA)
        assert hi >= fhi*(1 - 1e-7) and lo <= flo*(1 + 1e-7)       # fields are admissible
        dhi = math.log(hi/fhi); dlo = math.log(flo/lo)
        worst_hi = max(worst_hi, dhi); worst_lo = max(worst_lo, dlo)
        strict += (dhi > 1e-8) or (dlo > 1e-8); tested += 1
    print(f"{kind:10s} n={n} {'up-set B' if monotone else 'random B':9s}: {tested:4d} instances; "
          f"largest ln(LP max / field) = {worst_hi:.2e}, largest ln(field / LP min) = {worst_lo:.2e}; "
          f"field not optimal in {strict} instances")
    return strict

def integration_check(n, rng):
    """width = int_{-1}^{1} sum_i c_i ( <x_i>_{B,t} - <x_i>_{A,t} ) dt   (symmetric envelope cup = cdn = c)."""
    X = cube(n); h = rng.normal(0, 1, n); J = np.zeros((n, n))
    for i in range(n-1): J[i, i+1] = J[i+1, i] = -abs(rng.normal(0, 1))
    f = pair_energy(X, J, h); c = rng.uniform(0.1, 1.0, n); inA = X[:, 0] == 0   # A = {x_1 = 0}
    width = math.log(field_ratio(X, f, +c, inA)/field_ratio(X, f, -c, inA))
    ts = np.linspace(-1, 1, 4001); vals = []
    for t in ts:
        w = np.exp(-f - t*(X @ c)); mA = (w[inA] @ X[inA])/w[inA].sum(); mB = (w[~inA] @ X[~inA])/w[~inA].sum()
        vals.append(float(c @ (mB - mA)))
    integral = float(np.sum((np.array(vals[1:]) + np.array(vals[:-1]))/2*np.diff(ts)))
    w0 = np.exp(-f); mA = (w0[inA] @ X[inA])/w0[inA].sum(); mB = (w0[~inA] @ X[~inA])/w0[~inA].sum()
    print(f"  chain n={n}, A = {{x_1 = 0}}: width of ln R = {width:.6f}; thermodynamic integration = {integral:.6f}; "
          f"2 c_1 = {2*c[0]:.4f}; 2 sum_i c_i = {2*c.sum():.4f}; site contributions c_i*(<x_i>_B - <x_i>_A) at t=0: "
          + " ".join(f"{v:.3f}" for v in c*(mB - mA)))
    assert abs(width - integral) < 1e-5

if __name__ == "__main__":
    rng = np.random.default_rng(20261125)
    print("# hypotheses satisfied (theorem): the field must be optimal")
    bad = 0
    for n in (3, 4, 5):
        bad += run("additive", n, 150, rng); bad += run("ferro", n, 150, rng)
    assert bad == 0
    print("# controls: one hypothesis dropped")
    for n in (3, 4, 5):
        run("frustrated", n, 150, rng)
    for n in (3, 4):
        run("ferro", n, 150, rng, monotone=False)
    print("# locality of the width (ferromagnetic chain, macrostate defined by one site)")
    for n in (6, 10, 14):
        integration_check(n, rng)
    print("OK")
