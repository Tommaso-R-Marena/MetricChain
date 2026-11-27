"""(2) Cube Q_n, exchangeable reference pi (Curie-Weiss weights), envelope u * Hamming; macrostates that are unions of type
classes.  (a) full LP on Q_n = LP on types with distances u|j-k|; (b) threshold macrostates A = {|x| >= j1}, B = {|x| <= j0}
(j0 < j1): the optimum is the maximal tilt g = -u|x|, R+ = sum_A W_j e^{uj} / sum_B W_k e^{uk}; (c) a band macrostate
(A between two parts of B): not a tilt; the type LP, its optimal residual, and the exponential-scale formula
max_{P in A} min_{Q in B} [u|P-Q| + I(Q) - I(P)] at larger n."""
import numpy as np, math, itertools
from ratio_lib import *
from scipy.special import gammaln, logsumexp

def cw_weights(n, bJ, bB):
    j = np.arange(n + 1)
    m = (2 * j - n) / n
    logW = gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1) + n * (bJ / 2 * m ** 2 + bB * m)
    return logW - logsumexp(logW)

def type_lp(logW, u, At, Bt):
    n = len(logW) - 1
    D = u * np.abs(np.subtract.outer(np.arange(n + 1), np.arange(n + 1))).astype(float)
    w = np.exp(logW - logW.max())
    v, t = lp_bip(w, D, At, Bt)
    return v, t

rng = np.random.default_rng(5)
worst = dict(full_vs_type=0.0, tilt=0.0)
for n in (5, 6, 7):
    pts = np.array(list(itertools.product((0, 1), repeat=n)))
    wt = pts.sum(axis=1)
    Dfull = None
    for (bJ, bB, u) in ((0.0, 0.0, 1.0), (1.5, 0.0, 0.7), (0.8, 0.3, 1.3), (-1.0, 0.2, 0.5)):
        logW = cw_weights(n, bJ, bB)
        wfull = np.exp(logW[wt]) / np.array([math.comb(n, k) for k in wt])
        if Dfull is None:
            H = (pts[:, None, :] != pts[None, :, :]).sum(axis=2).astype(float)
        D = u * H
        for (At, Bt) in (([k for k in range(n + 1) if k >= n // 2 + 1], [k for k in range(n + 1) if k <= n // 2]),
                         ([n - 1, n], [0, 1]), ([n // 2, n // 2 + 1], [0, n]), ([2, 3], [0, 1, n - 1, n]), ([0, n], [n // 2])):
            if set(At) & set(Bt):
                continue
            A = [i for i in range(len(pts)) if wt[i] in At]; B = [i for i in range(len(pts)) if wt[i] in Bt]
            vfull, _ = lp_bip(wfull, D, A, B)
            vtype, t = type_lp(logW, u, At, Bt)
            worst["full_vs_type"] = max(worst["full_vs_type"], abs(vfull - vtype) / vtype)
            if max(Bt) < min(At):                         # threshold / gap macrostates: the tilt
                tilt = sum(math.exp(logW[j] + u * j) for j in At) / sum(math.exp(logW[k] + u * k) for k in Bt)
                worst["tilt"] = max(worst["tilt"], abs(tilt - vtype) / vtype)
print("full LP on Q_n against the LP on types, and the tilt formula:", {k: f"{v:.2e}" for k, v in worst.items()})

# (c) band macrostate at larger n: type LP against the exponential-scale formula
def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16); return -(x * np.log(x) + (1 - x) * np.log1p(-x))
for (bJ, bB, u, band, outer) in ((0.0, 0.0, 1.0, (0.45, 0.55), (0.3, 0.7)), (1.5, 0.0, 0.6, (0.4, 0.6), (0.2, 0.8)), (0.5, 0.2, 2.0, (0.6, 0.7), (0.5, 0.9))):
    print(f"band A = types in [{band[0]}, {band[1]}], B = types <= {outer[0]} or >= {outer[1]}; bJ={bJ} bB={bB} u={u}")
    kap = np.linspace(0, 1, 200001)
    phi = -(bJ / 2) * (2 * kap - 1) ** 2 - bB * (2 * kap - 1)
    I = phi - hb(kap); I -= I.min()
    inA = (kap >= band[0]) & (kap <= band[1]); inB = (kap <= outer[0]) | (kap >= outer[1])
    # max_P min_Q [u|P-Q| + I(Q) - I(P)]: for P in A the nearest parts of B are the two edges and beyond
    vB_left = np.min(np.where(kap <= outer[0], I - u * kap, np.inf))      # min_Q<=o0 [I(Q) - uQ]  (+ uP)
    vB_right = np.min(np.where(kap >= outer[1], I + u * kap, np.inf))     # min_Q>=o1 [I(Q) + uQ]  (- uP)
    val = np.where(inA, np.minimum(u * kap + vB_left, -u * kap + vB_right) - I, -np.inf)
    pred = float(val.max()); Pstar = float(kap[val.argmax()])
    for n in (50, 100, 200, 400, 800):
        logW = cw_weights(n, bJ, bB)
        At = [k for k in range(n + 1) if band[0] * n <= k <= band[1] * n]
        Bt = [k for k in range(n + 1) if k <= outer[0] * n or k >= outer[1] * n]
        # LP in log-domain is ill-conditioned for large n: rescale weights by the predicted optimal cone t = e^{-u|k - P* n|}
        w = np.exp(logW - logW.max())
        D = u * np.abs(np.subtract.outer(np.arange(n + 1), np.arange(n + 1))).astype(float)
        # exact value by the closed-pair iteration started from the cone around P* (monotone improvement), cross-checked by the LP when it is solvable
        best = -np.inf
        for jstar in At:
            g = u * np.abs(np.arange(n + 1) - jstar).astype(float)
            lr = logsumexp(logW[At] - g[At]) - logsumexp(logW[Bt] - g[Bt])
            best = max(best, lr)
        lpv = float("nan")
        if u * n <= 50:                   # beyond that the coefficients e^{u|j-k|} leave the range of the LP solver
            v, _ = lp_bip(w, D, At, Bt); lpv = math.log(v) / n
        print(f"   n={n:4d}  ln R+/n: LP {lpv:.6f}   best cone around a type class {best / n:.6f}   formula {pred:.6f} (P* = {Pstar:.4f})")
