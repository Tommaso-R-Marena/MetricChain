"""Illustration of addenda A11/A13 on a classical synthetic model: the Zimm-Bragg helix-coil chain.

Sites x_i in {0 (coil), 1 (helix)}, i = 1..n.  Statistical weight  prod_i s^{x_i} * sigma^{#helix starts},
i.e. energy (beta = 1)   f(x) = -ln(sigma s) * sum_i x_i + ln(sigma) * sum_i x_{i-1} x_i ,   sigma < 1:
a ferromagnetic nearest-neighbour model in lattice-gas variables, hence submodular.
Uncertainty class: every residual g whose change under the flip of one residue is at most c (in k_B T),
whatever its form (errors of the cooperativity, capping, i/i+4 terms, sequence effects ...).
A11: for every increasing observable and every monotone macrostate the extremes over the whole class
are attained at the two uniform fields  g = +c sum x_i  and  g = -c sum x_i ,  i.e. at  s e^{-c}  and  s e^{+c}.

Computed exactly by transfer matrices (with a counter for threshold macrostates):
 (1) robust interval of the mean helix fraction;
 (2) robust interval of ln[ P(helix fraction >= 1/2) / P(< 1/2) ];
 (3) robust interval of ln[ P(residue k helical)/P(residue k coil) ] and its decomposition over sites
     (thermodynamic-integration formula of Corollary A11.2), showing cancellation and its range;
 (4) a brute-force confirmation of (3) against the exact linear programme at n = 10.
"""
import math, itertools, sys
import numpy as np

def chain_counts(n, s, sigma):
    """Z[m] = total weight of configurations with m helical residues (free ends)."""
    # state: (last residue helical?, count)
    A = np.zeros((2, n+1)); A[0, 0] = 1.0
    for _ in range(n):
        B = np.zeros_like(A)
        B[0, :] = A[0, :] + A[1, :]                       # coil
        B[1, 1:] = sigma*s*A[0, :-1] + s*A[1, :-1]        # helix: start (sigma s) or continue (s)
        A = B
    return A.sum(axis=0)

def site_marginals(n, s, sigma, pin=None):
    """P(x_i = 1) for all i, optionally conditioned on x_k = v with pin = (k, v) (0-based k)."""
    T = np.array([[1.0, sigma*s], [1.0, s]])              # T[a, b]: weight of residue with state b after a
    def allowed(i):
        if pin is not None and pin[0] == i: return [pin[1]]
        return [0, 1]
    fwd = [None]*n; v = np.zeros(2)
    for b in allowed(0): v[b] = T[0, b]                   # before residue 0: "coil"
    fwd[0] = v
    for i in range(1, n):
        w = np.zeros(2)
        for b in allowed(i): w[b] = fwd[i-1] @ T[:, b]
        fwd[i] = w
    bwd = [None]*n; bwd[n-1] = np.ones(2)
    for i in range(n-2, -1, -1):
        w = np.zeros(2)
        for a in (0, 1):
            w[a] = sum(T[a, b]*bwd[i+1][b] for b in allowed(i+1))
        bwd[i] = w
    Z = fwd[n-1].sum()
    return np.array([fwd[i][1]*bwd[i][1]/Z for i in range(n)]), Z

def helix_fraction(n, s, sigma):
    Zm = chain_counts(n, s, sigma); return float((np.arange(n+1) @ Zm)/(n*Zm.sum()))

def log_odds_threshold(n, s, sigma, m):
    Zm = chain_counts(n, s, sigma); return math.log(Zm[m:].sum()/Zm[:m].sum())

def log_odds_site(n, s, sigma, k):
    _, Z1 = site_marginals(n, s, sigma, (k, 1)); _, Z0 = site_marginals(n, s, sigma, (k, 0))
    return math.log(Z1/Z0)

def brute_check(n, s, sigma, c, k):
    """exact LP over the weight cone for max/min of Z(x_k=0)/Z(x_k=1); compare with the fields."""
    from scipy.optimize import linprog
    X = np.array(list(itertools.product((0, 1), repeat=n))); N = len(X)
    starts = X[:, 0] + ((X[:, 1:] == 1) & (X[:, :-1] == 0)).sum(axis=1)
    f = -(np.log(s)*X.sum(axis=1) + np.log(sigma)*starts)
    idx = {tuple(x): i for i, x in enumerate(X)}
    rows = []
    for a, x in enumerate(X):
        for i in range(n):
            if x[i] == 0:
                y = x.copy(); y[i] = 1; b = idx[tuple(y)]
                r = np.zeros(N); r[a] = 1; r[b] = -math.exp(c + f[b] - f[a]); rows.append(r)
                r = np.zeros(N); r[b] = 1; r[a] = -math.exp(c + f[a] - f[b]); rows.append(r)
    A = np.array(rows); inA = X[:, k] == 0
    out = []
    for sense in (+1, -1):
        res = linprog(-sense*inA.astype(float), A_ub=A, b_ub=np.zeros(len(rows)), A_eq=(~inA).astype(float)[None, :],
                      b_eq=[1.0], bounds=[(0, None)]*N, method="highs",
                      options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
        assert res.status == 0
        out.append(math.log(float(inA.astype(float) @ res.x)))
    return out   # ln max Z(A)/Z(B), ln min

if __name__ == "__main__":
    sigma = 1e-3
    print(f"# Zimm-Bragg chain, sigma = {sigma}; class: single-residue changes of the residual at most c k_BT")
    print("# (1) mean helix fraction: value at s, and its exact robust interval [at s e^-c, at s e^+c]")
    for n in (20, 50, 100):
        for s in (1.0, 1.2, 1.5):
            row = f"n={n:4d} s={s:.1f}: theta = {helix_fraction(n, s, sigma):.3f};"
            for c in (0.05, 0.1, 0.3):
                lo = helix_fraction(n, s*math.exp(-c), sigma); hi = helix_fraction(n, s*math.exp(c), sigma)
                row += f"  c={c}: [{lo:.3f}, {hi:.3f}]"
            print(row)
    print("# (2) ln odds of 'at least half helical': value and robust interval")
    for n in (20, 50, 100):
        for s in (1.2,):
            m = n//2; row = f"n={n:4d} s={s:.1f}: ln odds = {log_odds_threshold(n, s, sigma, m):+.2f};"
            for c in (0.05, 0.1, 0.3):
                row += f"  c={c}: [{log_odds_threshold(n, s*math.exp(-c), sigma, m):+.2f}, {log_odds_threshold(n, s*math.exp(c), sigma, m):+.2f}]"
            print(row)
    print("# (3) one residue (the middle one) helical against coil: width of the robust interval of the ln odds,")
    print("#     against 2c (no cooperativity) and 2cn (no cancellation); site contributions by thermodynamic integration")
    for n in (20, 50, 100):
        for s in (1.0, 1.2, 1.5):
            k = n//2; c = 0.1
            width = log_odds_site(n, s*math.exp(c), sigma, k) - log_odds_site(n, s*math.exp(-c), sigma, k)
            ts = np.linspace(-1, 1, 801); contrib = np.zeros(n)
            vals = []
            for t in ts:
                m1, _ = site_marginals(n, s*math.exp(c*t), sigma, (k, 1)); m0, _ = site_marginals(n, s*math.exp(c*t), sigma, (k, 0))
                vals.append(c*(m1 - m0))
            vals = np.array(vals); contrib = ((vals[1:] + vals[:-1])/2*np.diff(ts)[:, None]).sum(axis=0)
            assert abs(contrib.sum() - width) < 1e-4, (contrib.sum(), width)
            order = np.argsort(-contrib); eff = int((np.cumsum(contrib[order]) < 0.9*width).sum()) + 1
            print(f"n={n:4d} s={s:.1f} c={c}: width = {width:.3f}   2c = {2*c:.2f}   2cn = {2*c*n:.1f}   "
                  f"width/2c = {width/(2*c):.1f} residues;  90 % of it from {eff} residues around k")
    print("# (4) brute force: exact LP over the whole class against the two fields, n = 10")
    for (s, c, k) in ((1.2, 0.3, 5), (1.0, 0.5, 2), (1.5, 0.2, 9)):
        n = 10; hi, lo = brute_check(n, s, sigma, c, k)
        fhi = -log_odds_site(n, s*math.exp(-c), sigma, k); flo = -log_odds_site(n, s*math.exp(c), sigma, k)
        print(f"n=10 s={s} c={c} k={k}: LP ln max = {hi:+.6f}, field = {fhi:+.6f};  LP ln min = {lo:+.6f}, field = {flo:+.6f}")
        assert abs(hi - fhi) < 1e-6 and abs(lo - flo) < 1e-6
    print("OK")
