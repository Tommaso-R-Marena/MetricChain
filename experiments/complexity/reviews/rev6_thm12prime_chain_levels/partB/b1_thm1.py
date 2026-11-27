# b1_thm1.py -- REVIEW 6, referee's own numerical check of Theorem 1 of CHAIN_GEOMETRY_HARDNESS.md
# (max F = 10*Lam*(2n+1) + 2*maxcut - |E| for the Heisenberg instance built from a graph), on graphs NOT used by
# the authors, with random and ADVERSARIAL starts.  Two objectives:
#   full:    F(b) = sum_{k<l} Q_kl <b_k,b_l>  over all 5n+4 spins (Q built here from the statement of the theorem)
#   reduced: Lam*[sum_v h(t_v1)+h(t_v2) + h(s)] - sum_E <u_v,u_w>   (gadget spins maximised out analytically)
# Numerical maximisation can only fail to find a violation; it is evidence, not proof.
import itertools, math, sys, time
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(606)


def maxcut(n, E):
    best, arg = -1, None
    for s in itertools.product((1, -1), repeat=n - 1):
        s = (1,) + s
        c = sum(1 for v, w in E if s[v] != s[w])
        if c > best:
            best, arg = c, s
    return best, arg


def build_Q(n, E, lam):
    # spins: u_0..u_{n-1}, z1 = n, z2 = n+1, then gadget spins (a, a') for the pairs (u_v,z1), (u_v,z2), (z1,z2)
    pairs = [(v, n) for v in range(n)] + [(v, n + 1) for v in range(n)] + [(n, n + 1)]
    N = n + 2 + 2 * len(pairs)
    assert N == 5 * n + 4
    Q = np.zeros((N, N))
    for v, w in E:
        Q[v, w] = Q[w, v] = -1
    for g, (p, q) in enumerate(pairs):
        a, a2 = n + 2 + 2 * g, n + 2 + 2 * g + 1
        Q[a, p] = Q[p, a] = 3 * lam
        Q[a, q] = Q[q, a] = 4 * lam
        Q[a2, p] = Q[p, a2] = 3 * lam
        Q[a2, q] = Q[q, a2] = -4 * lam
    return Q, pairs


def full_obj(Q):
    def f(y):
        B = y.reshape(-1, 3)
        nr = np.linalg.norm(B, axis=1, keepdims=True)
        X = B / nr
        val = 0.5 * np.sum(X * (Q @ X))
        G = Q @ X
        G = (G - np.sum(G * X, axis=1, keepdims=True) * X) / nr
        return -val, -G.ravel()
    return f


def h(t):
    return np.sqrt(25 + 24 * t) + np.sqrt(25 - 24 * t)


def dh(t):
    return 12 / np.sqrt(25 + 24 * t) - 12 / np.sqrt(25 - 24 * t)


def reduced_obj(n, E, lam):
    A = np.zeros((n, n))
    for v, w in E:
        A[v, w] = A[w, v] = 1

    def f(y):
        B = y.reshape(-1, 3)
        nr = np.linalg.norm(B, axis=1, keepdims=True)
        X = B / nr
        U, Z = X[:n], X[n:]
        T = U @ Z.T                      # n x 2
        s = float(Z[0] @ Z[1])
        val = lam * (np.sum(h(T)) + h(s)) - 0.5 * np.sum(U * (A @ U))
        GU = lam * dh(T) @ Z - A @ U
        GZ = lam * dh(T).T @ U
        GZ[0] += lam * dh(s) * Z[1]
        GZ[1] += lam * dh(s) * Z[0]
        G = np.vstack([GU, GZ])
        G = (G - np.sum(G * X, axis=1, keepdims=True) * X) / nr
        return -val, -G.ravel()
    return f


def gadget_spins(B, n, pairs):
    N = n + 2 + 2 * len(pairs)
    out = np.zeros((N, 3))
    out[:n + 2] = B[:n + 2]
    for g, (p, q) in enumerate(pairs):
        x = 3 * B[p] + 4 * B[q]
        y = 3 * B[p] - 4 * B[q]
        out[n + 2 + 2 * g] = x / max(np.linalg.norm(x), 1e-300) if np.linalg.norm(x) > 0 else np.array([1.0, 0, 0])
        out[n + 3 + 2 * g] = y / max(np.linalg.norm(y), 1e-300) if np.linalg.norm(y) > 0 else np.array([1.0, 0, 0])
    return out


def opt3(n, E, starts=60):
    """numerical optimum of -sum_E <x_v,x_w> over unit vectors in R^3 (the unconstrained vector optimum of G)"""
    A = np.zeros((n, n))
    for v, w in E:
        A[v, w] = A[w, v] = 1
    best, bx = -1e18, None

    def f(y):
        B = y.reshape(-1, 3)
        nr = np.linalg.norm(B, axis=1, keepdims=True)
        X = B / nr
        G = -(A @ X)
        G = (G - np.sum(G * X, axis=1, keepdims=True) * X) / nr
        return 0.5 * np.sum(X * (A @ X)), -G.ravel()
    for _ in range(starts):
        r = minimize(f, rng.normal(size=3 * n), jac=True, method="L-BFGS-B", options={"maxiter": 5000, "ftol": 1e-15, "gtol": 1e-11})
        if -r.fun > best:
            X = r.x.reshape(-1, 3)
            best, bx = -r.fun, X / np.linalg.norm(X, axis=1, keepdims=True)
    return best, bx


def rand_rot():
    M = rng.normal(size=(3, 3))
    Qm, R = np.linalg.qr(M)
    return Qm * np.sign(np.diag(R))


def adversarial_starts(n, E, sigma, X3):
    e1, e2, e3 = np.eye(3)
    S = []
    # A1: both poles equal, u in the optimal R^3 configuration of G
    S.append(("poles equal, u = vector optimum of G", np.vstack([X3 @ rand_rot().T, e1, e1 + 1e-3 * rng.normal(size=3)])))
    # A2: poles orthogonal, u = vector optimum of G in general position
    S.append(("poles orthogonal, u = vector optimum of G (general position)", np.vstack([X3 @ rand_rot().T, e1, e2])))
    # A3: u in the plane spanned by z2 and e3 (orthogonal to z1 only)
    P = X3.copy()
    S.append(("u = vector optimum of G as given, poles e1,e2", np.vstack([P, e1, e2])))
    # A4: near the intended optimum, small tilts
    for eps in (1e-3, 1e-2, 1e-1, 0.3):
        U = np.array([[0, 0, s] for s in sigma], float) + eps * rng.normal(size=(n, 3))
        S.append((f"intended optimum + tilt {eps}", np.vstack([U, e1, e2])))
    # A5: antipodal poles
    S.append(("poles antipodal", np.vstack([X3 @ rand_rot().T, e1, -e1 + 1e-3 * rng.normal(size=3)])))
    # A6: s = 1/2, u orthogonal to both poles
    z2 = 0.5 * e1 + math.sqrt(0.75) * e2
    S.append(("s = 1/2, u = +-e3", np.vstack([np.array([[0, 0, s] for s in sigma], float), e1, z2])))
    # A7: all u in the plane of the poles, 2D-like optimum
    U = X3.copy(); U[:, 2] = 1e-3 * rng.normal(size=n)
    S.append(("u flattened into the plane of the poles", np.vstack([U, e1, e2])))
    # A8: u = vector optimum, poles chosen to minimise sum of squared projections (two smallest principal axes)
    w, V = np.linalg.eigh(X3.T @ X3)
    S.append(("u = vector optimum, poles along its two least principal axes", np.vstack([X3, V[:, 0], V[:, 1]])))
    return S


GRAPHS = {
    "claw K_{1,3}": (4, [(0, 1), (0, 2), (0, 3)]),
    "paw": (4, [(0, 1), (1, 2), (0, 2), (2, 3)]),
    "bull": (5, [(0, 1), (1, 2), (0, 2), (1, 3), (2, 4)]),
    "K_{2,3}": (5, [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]),
    "K_5": (5, list(itertools.combinations(range(5), 2))),
    "C_7": (7, [(i, (i + 1) % 7) for i in range(7)]),
    "prism": (6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]),
    "K_3 + K_2 (disconnected)": (5, [(0, 1), (1, 2), (0, 2), (3, 4)]),
    "edge + isolated vertex": (3, [(0, 1)]),
    "W_5 (wheel, 6 vertices)": (6, [(i, (i + 1) % 5) for i in range(5)] + [(i, 5) for i in range(5)]),
    "Petersen": (10, [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]),
}


def run(name, n, E, lam=None, nrand=40, verbose=True):
    lam_std = 4 * len(E)
    lam = lam_std if lam is None else lam
    mc, sigma = maxcut(n, E)
    target = 10 * lam * (2 * n + 1) + 2 * mc - len(E)
    Q, pairs = build_Q(n, E, lam)
    fr, ff = reduced_obj(n, E, lam), full_obj(Q)
    o3, X3 = opt3(n, E)
    # explicit configuration
    e1, e2, e3 = np.eye(3)
    B0 = np.vstack([np.array([[0, 0, s] for s in sigma], float), e1, e2])
    v_red = -fr(B0.ravel())[0]
    v_full = -ff(gadget_spins(B0, n, pairs).ravel())[0]
    best_red = best_full = -1e18
    worst_start = None
    opts = {"maxiter": 20000, "ftol": 1e-15, "gtol": 1e-10}
    starts = adversarial_starts(n, E, sigma, X3) + [("random", rng.normal(size=(n + 2, 3))) for _ in range(nrand)]
    for label, S0 in starts:
        r = minimize(fr, S0.ravel(), jac=True, method="L-BFGS-B", options=opts)
        if -r.fun > best_red:
            best_red, worst_start = -r.fun, label
        # full objective from the same (u,z) with optimal gadget spins + noise, and from the reduced optimum
        F0 = gadget_spins(S0 / np.linalg.norm(S0, axis=1, keepdims=True), n, pairs) + 0.05 * rng.normal(size=(5 * n + 4, 3))
        r2 = minimize(ff, F0.ravel(), jac=True, method="L-BFGS-B", options=opts)
        best_full = max(best_full, -r2.fun)
    for _ in range(nrand // 2):
        r2 = minimize(ff, rng.normal(size=3 * (5 * n + 4)), jac=True, method="L-BFGS-B", options=opts)
        best_full = max(best_full, -r2.fun)
    ok_att = abs(v_red - target) < 1e-8 and abs(v_full - target) < 1e-8
    ok_up = best_red <= target + 1e-6 and best_full <= target + 1e-6
    if verbose:
        print(f"{name:28s} n={n:2d} |E|={len(E):2d} Lam={lam:6.2f} maxcut={mc:2d} OPT_3(G)={o3:8.5f} (2mc-|E|={2*mc-len(E)})  "
              f"target={target:11.4f}  explicit(red/full)={v_red:11.4f}/{v_full:11.4f}  "
              f"best reduced={best_red:13.6f}  best full={best_full:13.6f}  "
              f"{'attained' if ok_att else 'NOT ATTAINED'}; {'never exceeded' if ok_up else 'EXCEEDED by %.6f' % (max(best_red, best_full) - target)}"
              f"; reached: {abs(max(best_red, best_full) - target) < 1e-4}", flush=True)
    return ok_att, ok_up, max(best_red, best_full) - target


if __name__ == "__main__":
    t0 = time.time()
    allok = True
    print("Theorem 1 with Lam = 4|E| (the note's choice):")
    for name, (n, E) in GRAPHS.items():
        a, b, _ = run(name, n, E, nrand=(40 if n <= 7 else 16))
        allok &= a and b
    print("Power of the test: the same with a much smaller Lam (the formula should then FAIL when OPT_3(G) > 2maxcut-|E|):")
    for name in ("paw", "K_5", "C_7"):
        n, E = GRAPHS[name]
        for lam in (0.05, 0.5):
            a, b, exc = run(name, n, E, lam=lam, nrand=20)
            print(f"      -> excess over the formula {exc:.5f} ({'violation detected' if exc > 1e-4 else 'no violation'})")
    print("ALL OK" if allok else "SOME CHECK FAILED", f"({time.time()-t0:.0f}s)")
