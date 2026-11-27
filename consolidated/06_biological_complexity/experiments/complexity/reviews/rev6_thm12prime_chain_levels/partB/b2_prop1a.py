# b2_prop1a.py -- REVIEW 6, referee's own numerical check of Proposition 1a (OPT_{k+1}(H') = 25 n L + 9 OPT_k(H),
# L >= 4.5 (k+1) Delta) on graphs NOT used by the authors, for which OPT_k(H) is known in closed form:
#   bipartite graphs: OPT_k = |E| for all k;   K_n: OPT_1 = 2*floor(n^2/4) - C(n,2), OPT_k = n/2 for k >= 2;
#   odd cycles C_n: OPT_1 = n - 2, OPT_k = n cos(pi/n) for k >= 2.
# (Petersen k=1: OPT_1 = 9 by enumeration.)
# Reduced objective (R-spins maximised out by the blow-up lemma and the triangle lemma):
#     -9 sum_E <u_v,u_w> + sum_{v,l} g(<u_v,z_l>),    g(t) = 5 sqrt(25+24t) - 12 t,
# maximised over unit vectors u_v, z_l in R^{k+1} from random and ADVERSARIAL starts; and the explicit unweighted
# graph H' maximised over all its vertices for two small cases.
import itertools, math, sys, time
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(707)
OPTS = {"maxiter": 30000, "ftol": 1e-15, "gtol": 1e-10}


def g(t):
    return 5.0 * np.sqrt(25.0 + 24.0 * t) - 12.0 * t


def dg(t):
    return 60.0 / np.sqrt(25.0 + 24.0 * t) - 12.0


def adj(n, E):
    A = np.zeros((n, n))
    for v, w in E:
        assert v != w and A[v, w] == 0
        A[v, w] = A[w, v] = 1
    return A


def sphere_wrap(fun_grad, shape):
    def f(y):
        Y = y.reshape(shape)
        nr = np.linalg.norm(Y, axis=1, keepdims=True)
        X = Y / nr
        val, G = fun_grad(X)
        G = (G - np.sum(G * X, axis=1, keepdims=True) * X) / nr
        return -val, -G.ravel()
    return f


def vec_opt(n, E, k, starts=80):
    """numerical OPT_k(H) and an optimiser (unit vectors in R^k)"""
    A = adj(n, E)
    if k == 1:
        best, arg = -1e9, None
        for s in itertools.product((1, -1), repeat=n):
            v = -sum(s[i] * s[j] for i, j in E)
            if v > best:
                best, arg = v, s
        return best, np.array(arg, float).reshape(n, 1)
    f = sphere_wrap(lambda X: (-0.5 * np.sum(X * (A @ X)), -(A @ X)), (n, k))
    best, bx = -1e18, None
    for _ in range(starts):
        r = minimize(f, rng.normal(size=n * k), jac=True, method="L-BFGS-B", options=OPTS)
        if -r.fun > best:
            Y = r.x.reshape(n, k)
            best, bx = -r.fun, Y / np.linalg.norm(Y, axis=1, keepdims=True)
    return best, bx


def lifted(n, E, L):
    A = adj(n, E)

    def fg(X):
        U, Z = X[:n], X[n:]
        T = np.clip(U @ Z.T, -1.0, 1.0)
        val = -4.5 * np.sum(U * (A @ U)) + np.sum(g(T))
        D = dg(T)
        return val, np.vstack([-9.0 * (A @ U) + D @ Z, D.T @ U])
    return fg


def closed_form(name, n, E, k):
    if name.startswith("bip:"):
        return float(len(E))
    if name.startswith("K_"):
        return float(2 * (n * n // 4) - n * (n - 1) // 2) if k == 1 else n / 2.0
    if name.startswith("C_"):
        return float(n - 2) if k == 1 else n * math.cos(math.pi / n)
    return None


def check(name, n, E, k, L=None, nrand=14):
    deg = [sum(1 for e in E if v in e) for v in range(n)]
    Delta = max(deg)
    Lmin = math.ceil(4.5 * (k + 1) * Delta)
    L = Lmin if L is None else L
    cf = closed_form(name, n, E, k)
    num, Xk = vec_opt(n, E, k)
    base = cf if cf is not None else num
    assert abs(num - base) < 1e-6, (name, k, num, base)
    target = 25 * n * L + 9 * base
    fg = lifted(n, E, L)
    f = sphere_wrap(fg, (n + L, k + 1))
    d = k + 1
    # explicit configuration of the lower bound
    X0 = np.zeros((n + L, d)); X0[:n, :k] = Xk; X0[n:, k] = 1.0
    explicit = fg(X0)[0]
    # optimum of H one dimension higher (may be better than OPT_k)
    num1, Xk1 = vec_opt(n, E, d)
    starts = []
    starts.append(("explicit + noise 0.05", X0 + 0.05 * rng.normal(size=X0.shape)))
    starts.append(("explicit + noise 0.5", X0 + 0.5 * rng.normal(size=X0.shape)))
    # B1: poles spread evenly over an orthonormal frame, u = optimum of H in R^{k+1}
    S = np.zeros((n + L, d)); S[:n] = Xk1
    for l in range(L):
        S[n + l, l % d] = 1.0
    starts.append(("poles on a frame (M = L/(k+1) I), u = OPT_{k+1} configuration", S + 1e-3 * rng.normal(size=S.shape)))
    # B2: all poles along the least principal axis of the (k+1)-dimensional optimum
    w, V = np.linalg.eigh(Xk1.T @ Xk1)
    S = np.zeros((n + L, d)); S[:n] = Xk1; S[n:] = V[:, 0]
    starts.append(("all poles on the least principal axis of the OPT_{k+1} configuration", S + 1e-3 * rng.normal(size=S.shape)))
    # B3: poles in two groups at a small angle
    S = X0.copy()
    S[n + L // 2:, 0] = 0.3
    starts.append(("two groups of poles at a small angle", S + 1e-3 * rng.normal(size=S.shape)))
    # B4: poles +-f (antipodal groups)
    S = X0.copy(); S[n + L // 2:, k] = -1.0
    starts.append(("antipodal groups of poles", S + 1e-2 * rng.normal(size=S.shape)))
    # B5: u all equal to a pole direction
    S = X0.copy(); S[:n] = 0; S[:n, k] = 1.0
    starts.append(("all u along the poles", S + 1e-2 * rng.normal(size=S.shape)))
    starts += [("random", rng.normal(size=(n + L, d))) for _ in range(nrand)]
    best, lab = -1e18, None
    for label, S0 in starts:
        r = minimize(f, S0.ravel(), jac=True, method="L-BFGS-B", options=OPTS)
        if -r.fun > best:
            best, lab = -r.fun, label
    ok_att = abs(explicit - target) < 1e-7
    ok_up = best <= target + 1e-5
    print(f"   {name:14s} k={k}->{k+1} n={n:2d} Delta={Delta} L={L:3d} (bound {Lmin:3d})  OPT_k={base:9.6f} OPT_k+1={num1:9.6f}  "
          f"target={target:13.6f} explicit={explicit:13.6f} best of {len(starts)}={best:13.6f} "
          f"{'attained' if ok_att else 'NOT ATTAINED'}; {'never exceeded' if ok_up else 'EXCEEDED by %.6f' % (best - target)}; reached {abs(best-target) < 1e-4}", flush=True)
    return ok_att, ok_up, best - target


def explicit_graph(n, E, L):
    idx, cl = 0, {}
    for v in range(n):
        cl[("U", v)] = list(range(idx, idx + 3)); idx += 3
    for l in range(L):
        cl[("Z", l)] = list(range(idx, idx + 4)); idx += 4
    for v in range(n):
        for l in range(L):
            cl[("R", v, l)] = list(range(idx, idx + 5)); idx += 5
    EE = []
    def join(a, b):
        EE.extend((i, j) for i in cl[a] for j in cl[b])
    for v, w in E:
        join(("U", v), ("U", w))
    for v in range(n):
        for l in range(L):
            join(("U", v), ("Z", l)); join(("R", v, l), ("U", v)); join(("R", v, l), ("Z", l))
    return idx, EE


def check_explicit(name, n, E, k, starts=6):
    deg = [sum(1 for e in E if v in e) for v in range(n)]
    L = math.ceil(4.5 * (k + 1) * max(deg))
    base = closed_form(name, n, E, k)
    N, EE = explicit_graph(n, E, L)
    assert N == 3 * n + 4 * L + 5 * n * L
    A = adj(N, EE)
    f = sphere_wrap(lambda X: (-0.5 * np.sum(X * (A @ X)), -(A @ X)), (N, k + 1))
    target = 25 * n * L + 9 * base
    best = -1e18
    for _ in range(starts):
        r = minimize(f, rng.normal(size=N * (k + 1)), jac=True, method="L-BFGS-B", options=OPTS)
        best = max(best, -r.fun)
    ok = best <= target + 1e-4
    print(f"   explicit H' of {name} k={k}->{k+1}: simple graph, {N} vertices, {len(EE)} edges, L={L}; target={target:.6f}  "
          f"best of {starts} maximisations over all vertices={best:.6f}  {'never exceeded' if ok else 'EXCEEDED'}; reached {abs(best-target) < 1e-3}", flush=True)
    return ok


GR = {
    "bip:claw": (4, [(0, 1), (0, 2), (0, 3)]),
    "bip:C_4": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    "bip:K_{3,3}": (6, [(i, 3 + j) for i in range(3) for j in range(3)]),
    "K_5": (5, list(itertools.combinations(range(5), 2))),
    "K_6": (6, list(itertools.combinations(range(6), 2))),
    "C_7": (7, [(i, (i + 1) % 7) for i in range(7)]),
    "C_9": (9, [(i, (i + 1) % 9) for i in range(9)]),
    "Petersen": (10, [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]),
}

if __name__ == "__main__":
    t0 = time.time()
    allok = True
    print("(A) lifting with L = ceil(4.5 (k+1) Delta):")
    for name, k in (("bip:claw", 1), ("bip:C_4", 1), ("K_5", 1), ("C_7", 1), ("C_9", 1), ("bip:K_{3,3}", 1), ("K_6", 1), ("Petersen", 1),
                    ("K_5", 2), ("C_7", 2), ("bip:claw", 2), ("K_5", 3), ("C_7", 3), ("K_6", 4)):
        a, b, _ = check(name, *GR[name], k)
        allok &= a and b
    print("(B) power of the test: too few poles (the identity should fail when OPT_{k+1}(H) > OPT_k(H)):")
    for name, k, L in (("K_5", 1, 1), ("C_7", 1, 2), ("K_5", 1, 4), ("C_7", 1, 9)):
        a, b, exc = check(name, *GR[name], k, L=L)
        print(f"        excess over the formula: {exc:.6f}  ({'violation detected' if exc > 1e-3 else 'no violation found'})")
    print("(C) the explicit unweighted graph H' (no assumption that copies are equal):")
    allok &= check_explicit("bip:C_4", *GR["bip:C_4"], 1)
    allok &= check_explicit("K_5", *GR["K_5"], 1, starts=4)
    print("ALL OK" if allok else "SOME CHECK FAILED", f"({time.time()-t0:.0f}s)")
