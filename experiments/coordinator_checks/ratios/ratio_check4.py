"""(4') Three letters at larger n (macrostates {mean h >= 1.25}, {mean h <= 0.5}: thresholds on the lattice of types for n divisible by 4): W_d through the vertices of the Lipschitz polytope; bracket of ln R+/n by the best cone
around a type class (lower) and by the plan 'each class of A ships from its best class of B' (upper); the continuum formula
max_{P in A} min_{Q in B} [W_d(Q,P) + KL(Q||pi) - KL(P||pi)]."""
import numpy as np, math, itertools
from ratio_lib import closure
from scipy.special import gammaln, logsumexp

def lip_vertices(Dq):
    """vertices of {phi : phi(b) - phi(a) <= Dq[a,b], phi(0) = 0}; W(P -> Q) = max_phi phi . (Q - P)"""
    q = len(Dq)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    V = []
    for S in itertools.combinations(cons, q - 1):
        M = np.zeros((q, q)); rhs = np.zeros(q)
        for r, (a, b) in enumerate(S):
            M[r, b] += 1; M[r, a] -= 1; rhs[r] = Dq[a, b]
        M[q - 1, 0] = 1
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        phi = np.linalg.solve(M, rhs)
        if all(phi[b] - phi[a] <= Dq[a, b] + 1e-9 for a, b in cons) and not any(np.allclose(phi, v) for v in V):
            V.append(phi)
    return np.array(V)

Dq = closure(np.array([[0, 1.0, 1.6], [0.7, 0, 1.2], [1.5, 0.9, 0]]))
V = lip_vertices(Dq)
pi = np.array([0.5, 0.3, 0.2]); hfun = np.array([0.0, 1.0, 2.0])
print("vertices of the Lipschitz polytope:", len(V))
# check W by vertices against the transport LP on a few random pairs
from scipy.optimize import linprog
rng = np.random.default_rng(1)
for _ in range(200):
    P = rng.dirichlet(np.ones(3)); Q = rng.dirichlet(np.ones(3))
    c = Dq.reshape(-1); Aeq = np.zeros((6, 9))
    for a in range(3):
        for b in range(3):
            Aeq[a, a * 3 + b] = 1; Aeq[3 + b, a * 3 + b] = 1
    res = linprog(c, A_eq=Aeq, b_eq=np.concatenate([P, Q]), bounds=[(0, None)] * 9, method="highs")
    assert abs(res.fun - float((V @ (Q - P)).max())) < 1e-9
print("W by vertices = W by transport: ok")

def continuum(m=240):
    g = np.array([(i / m, j / m, 1 - (i + j) / m) for i in range(m + 1) for j in range(m + 1 - i)])
    I = np.where(g > 0, g * np.log(np.maximum(g, 1e-300) / pi), 0.0).sum(axis=1)
    hv = g @ hfun
    PA = g[hv >= 1.25 - 1e-12]; IA = I[hv >= 1.25 - 1e-12]
    QB = g[hv <= 0.5 + 1e-12]; IB = I[hv <= 0.5 + 1e-12]
    best = -np.inf
    for P, iP in zip(PA, IA):
        W = (V[None, :, :] * (P[None, None, :] - QB[:, None, :])).sum(axis=2).max(axis=1)      # W(Q -> P)
        best = max(best, float((W + IB).min() - iP))
    return best
form = continuum()
print(f"continuum formula: {form:.5f}")
for n in (12, 24, 48, 96, 144):
    T = np.array([c for c in itertools.product(range(n + 1), repeat=3) if sum(c) == n])
    logW = gammaln(n + 1) - gammaln(T + 1).sum(axis=1) + (T * np.log(pi)).sum(axis=1)
    hv = T @ hfun / n
    At = np.nonzero(hv >= 1.25 - 1e-12)[0]; Bt = np.nonzero(hv <= 0.5 + 1e-12)[0]
    TA, TB = T[At].astype(float), T[Bt].astype(float)
    # D[z, y] = W(class z -> class y) for z in B, y in A, by blocks
    def Wmat(X, Y):       # W(x -> y) for rows of X and Y (counts)
        out = np.empty((len(X), len(Y)))
        for i in range(0, len(X), 200):
            diff = Y[None, :, :] - X[i:i + 200, None, :]
            out[i:i + 200] = np.max(np.einsum("vk,xyk->xyv", V, diff), axis=2)
        return out
    DBA = Wmat(TB, TA)
    DAA = Wmat(TA, TA)
    # lower: cone around the class y*: g = W(., y*)
    lowers = logsumexp(logW[At][:, None] - DAA, axis=0) - logsumexp(logW[Bt][:, None] - DBA, axis=0)
    lower = float(lowers.max())
    # upper: plan from the best source
    score = DBA - logW[Bt][:, None]
    src = score.argmin(axis=0)
    load = np.full(len(Bt), -np.inf)
    contrib = DBA[src, np.arange(len(At))] + logW[At] - logW[Bt][src]
    for z, c in zip(src, contrib):
        load[z] = np.logaddexp(load[z], c)
    upper = float(load.max())
    lattice = float((score + logW[At][None, :] * 0).min(axis=0).__add__(logW[At]).max()) if False else float((score.min(axis=0) + logW[At]).max())
    print(f"n={n:4d} types={len(T):6d}  ln R+/n in [{lower / n:.5f}, {upper / n:.5f}]  width*n/ln n = {(upper - lower) / math.log(n):.2f}   max-min on the lattice {lattice / n:.5f}   continuum {form:.5f}")
