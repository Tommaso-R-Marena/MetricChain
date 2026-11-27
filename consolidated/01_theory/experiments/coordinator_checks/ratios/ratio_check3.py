"""(3) One-coordinate macrostates on product spaces.  Sites with alphabets q_i, site-additive envelope d = sum_i d_i (each d_i
a quasi-metric), A = {x_i in A_i}, B = {x_i in B_i}.
 (a) additive known part: R+(A,B) = the single-site value for site i with its own weights;
 (b) pairwise known part: single-site value with MARGINAL weights  <=  R+  <=  max over the rest r of the single-site value
     with the CONDITIONAL weights given r; both inequalities can be strict.
(4) Three letters, type-defined macrostates, exponential scale: the LP on types against
     max_{P in A} min_{Q in B} [W_d(Q,P) + I(Q) - I(P)], bracketed at finite n by the best cone around a type class (below)
     and by the plan 'every class of A ships from its best class of B' (above)."""
import numpy as np, math, itertools
from ratio_lib import *
from scipy.optimize import linprog
from scipy.special import gammaln, logsumexp
rng = np.random.default_rng(11)

def rand_qm(q):
    D = rng.uniform(0.2, 2.0, size=(q, q))
    return closure(D)

# ---- (3) ----
stats = dict(additive=0.0, lower_gap=0.0, upper_gap=0.0, lower_viol=0.0, upper_viol=0.0, strict_lower=0, strict_upper=0, cases=0)
for rep in range(120):
    qs = [int(rng.integers(2, 4)) for _ in range(3)]
    Ds = [rand_qm(q) for q in qs]
    pts = list(itertools.product(*[range(q) for q in qs]))
    N = len(pts)
    D = np.zeros((N, N))
    for a, x in enumerate(pts):
        for b, y in enumerate(pts):
            D[a, b] = sum(Ds[i][x[i], y[i]] for i in range(3))
    site = int(rng.integers(3))
    q = qs[site]
    perm = rng.permutation(q)
    na = int(rng.integers(1, q)); Ai = perm[:na].tolist(); Bi = perm[na:].tolist()
    if q >= 3 and rng.random() < 0.5 and len(Bi) > 1:
        Bi = Bi[:-1]
    A = [k for k, x in enumerate(pts) if x[site] in Ai]; B = [k for k, x in enumerate(pts) if x[site] in Bi]
    f1 = [rng.normal(0, 1, size=qq) for qq in qs]
    pair = {(i, j): rng.normal(0, 1.0, size=(qs[i], qs[j])) for i in range(3) for j in range(i + 1, 3)}
    for kind in ("additive", "pairwise"):
        logw = np.array([sum(f1[i][x[i]] for i in range(3)) + (sum(pair[(i, j)][x[i], x[j]] for (i, j) in pair) if kind == "pairwise" else 0.0) for x in pts])
        w = np.exp(logw)
        v, _ = lp_bip(w, D, A, B)
        # single-site problems
        def single(ws):
            vv, _ = lp_bip(ws, Ds[site], Ai, Bi)
            return vv
        marg = np.array([sum(w[k] for k, x in enumerate(pts) if x[site] == a) for a in range(q)])
        rest = sorted({tuple(x[j] for j in range(3) if j != site) for x in pts})
        conds = []
        for r in rest:
            ws = np.zeros(q)
            for k, x in enumerate(pts):
                if tuple(x[j] for j in range(3) if j != site) == r:
                    ws[x[site]] = w[k]
            conds.append(single(ws))
        lo, hi = single(marg), max(conds)
        if kind == "additive":
            stats["additive"] = max(stats["additive"], abs(lo - v) / v, abs(hi - v) / v)
        else:
            stats["lower_viol"] = max(stats["lower_viol"], lo / v - 1); stats["upper_viol"] = max(stats["upper_viol"], v / hi - 1)
            stats["lower_gap"] = max(stats["lower_gap"], v / lo - 1); stats["upper_gap"] = max(stats["upper_gap"], hi / v - 1)
            stats["strict_lower"] += v > lo * (1 + 1e-9); stats["strict_upper"] += hi > v * (1 + 1e-9)
    stats["cases"] += 1
print("(3) one-coordinate macrostates:", {k: (f"{v:.2e}" if isinstance(v, float) else v) for k, v in stats.items()})

# ---- (4) three letters ----
def types(n, q=3):
    return [c for c in itertools.product(range(n + 1), repeat=q) if sum(c) == n]

def W_cost(P, Q, Dq):
    """min-cost transport from the count vector P to Q (cost Dq[a, b] for moving a letter a of the first to b of the second)"""
    q = len(P)
    c = Dq.reshape(-1)
    Aeq = np.zeros((2 * q, q * q)); beq = np.concatenate([P, Q]).astype(float)
    for a in range(q):
        for b in range(q):
            Aeq[a, a * q + b] = 1; Aeq[q + b, a * q + b] = 1
    res = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (q * q), method="highs")
    return res.fun

Dq = closure(np.array([[0, 1.0, 1.6], [0.7, 0, 1.2], [1.5, 0.9, 0]]))
pi = np.array([0.5, 0.3, 0.2])
hfun = np.array([0.0, 1.0, 2.0])                      # additive order parameter; A = {mean h >= 1.1}, B = {mean h <= 0.6} (off the lattice: see ratio_check4.py for lattice thresholds)
for n in (6, 9, 12, 15, 18):
    T = types(n)
    logW = np.array([gammaln(n + 1) - sum(gammaln(np.array(c) + 1)) + sum(c[a] * math.log(pi[a]) for a in range(3)) for c in T])
    hv = np.array([np.dot(c, hfun) / n for c in T])
    At = [k for k in range(len(T)) if hv[k] >= 1.1 - 1e-12]; Bt = [k for k in range(len(T)) if hv[k] <= 0.6 + 1e-12]
    D = np.zeros((len(T), len(T)))
    for z in Bt:
        for y in At:
            D[z, y] = W_cost(np.array(T[z]), np.array(T[y]), Dq)      # distance from the class of z to the class of y  (g(z) - g(y) <= d(z, y))
    w = np.exp(logW)
    v, _ = lp_bip(w, D, At, Bt)
    # lower: best cone around a type class of A:  g = d(., class y*)  i.e. g(x) = W(x, y*)  [admissible: g(x) - g(y) <= d(x,y)]
    best = -np.inf
    for ystar in At:
        gA = np.array([W_cost(np.array(T[y]), np.array(T[ystar]), Dq) for y in At])
        gB = np.array([D[z, ystar] for z in Bt])
        best = max(best, logsumexp(logW[At] - gA) - logsumexp(logW[Bt] - gB))
    # upper: the plan in which every class of A ships from its best class of B
    src = {y: min(Bt, key=lambda z: D[z, y] - logW[z]) for y in At}
    load = {}
    for y in At:
        z = src[y]
        load[z] = np.logaddexp(load.get(z, -np.inf), D[z, y] + logW[y] - logW[z])
    upper = max(load.values())
    # exponential-scale formula on the lattice of types of this n (max over P in A of min over Q in B)
    form = max(min(D[z, y] / n - (logW[z] - logW[y]) / n for z in Bt) for y in At)
    print(f"(4) n={n:3d} types={len(T):4d}  ln R+/n: cone {best / n:.5f} <= LP {math.log(v) / n:.5f} <= plan {upper / n:.5f};  max-min on types {form:.5f}")
