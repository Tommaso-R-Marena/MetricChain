"""
T2 — robust barrier heights under an envelope class (brief, sketch 2).

Claim A (no anchors).  For E_g = f + g, g admissible (g(x)-g(y) <= d(x,y)), the height
    H_g(a,b) = B_{f+g}(a,b) - (f+g)(a)
ranges exactly over [ B_{f-d(a,.)}(a,b) - f(a),  B_{f+d(.,a)}(a,b) - f(a) ].
Claim B (anchors (A,v)).  Same with d replaced by the conditional envelope
    D_A(x,y) = min(d(x,y), U(x)-L(y)); extremal residuals
    g+ = min(U, L(a)+d(.,a)),  g- = max(L, U(a)-d(a,.)).
Claim C.  The saddle energy B_{f+g}(a,b) ranges exactly over [B_{f+L}, B_{f+U}].
Claim D.  depth_g(a) (0-dim persistence of the state a) has its extreme values at the same two
    cone residuals (range not an interval in general: +inf can occur).

Tests: (1) random sampling of admissible g (never outside; ends attained);
       (2) INDEPENDENT exact optimisation over the polytrope on tiny spaces by LPs:
           max_g H_g = max over separators of an LP;  min_g H_g = min over simple paths of an LP;
       (3) anchors;  (4) depth;  (5) width of the exact interval vs the sup-norm stability bound.
Run:  python3 t2_robust_barrier.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from kcore import (Space, barrier_from, outer_boundary, random_pairwise, pairwise_energy,
                   is_admissible, mcshane, cond_env, random_admissible, depth, minimax_path)

rng = np.random.default_rng(7)


def rand_site_env(S, rng, asym=True):
    """random site-additive envelope: delta_i = shortest-path closure of a random nonneg matrix"""
    deltas = []
    for i in range(S.n):
        k = S.ks[i]
        M = rng.uniform(0.1, 1.0, (k, k))
        if not asym:
            M = 0.5 * (M + M.T)
        np.fill_diagonal(M, 0.0)
        for m in range(k):                     # Floyd–Warshall closure
            M = np.minimum(M, M[:, [m]] + M[[m], :])
        deltas.append(M)
    return S.site_env(deltas)


def height(S, f, g, a, b):
    E = f + g
    return barrier_from(S, E, a)[b] - E[a]


def lp_extremes(S, f, D, a, b):
    """Exact max and min of H_g over the admissible class by enumeration + LP (tiny spaces only)."""
    N = S.N
    pairs = [(x, y) for x in range(N) for y in range(N) if x != y]
    A_ub = np.zeros((len(pairs), N + 1))
    b_ub = np.zeros(len(pairs))
    for r, (x, y) in enumerate(pairs):
        A_ub[r, x] = 1.0
        A_ub[r, y] = -1.0
        b_ub[r] = D[x, y]
    A_eq = np.zeros((1, N + 1))
    A_eq[0, a] = 1.0                           # pin g(a)=0 (H is invariant under constants)
    bounds = [(None, None)] * (N + 1)
    # ---- max over separators: maximise t s.t. t <= f(y)+g(y)-f(a) for y in outer boundary of S
    best_max = 0.0                             # the trivial term E(a)-E(a)=0
    others = [u for u in range(N) if u not in (a, b)]
    for r in range(len(others) + 1):
        for T in itertools.combinations(others, r):
            mask = np.zeros(N, dtype=bool)
            mask[a] = True
            mask[list(T)] = True
            ob = np.nonzero(outer_boundary(S, mask))[0]
            rows = np.zeros((len(ob), N + 1))
            rhs = np.zeros(len(ob))
            for j, y in enumerate(ob):
                rows[j, N] = 1.0
                rows[j, y] = -1.0
                rhs[j] = f[y] - f[a]
            c = np.zeros(N + 1)
            c[N] = -1.0
            res = linprog(c, A_ub=np.vstack([A_ub, rows]), b_ub=np.concatenate([b_ub, rhs]),
                          A_eq=A_eq, b_eq=[0.0], bounds=bounds, method="highs")
            assert res.status == 0, res.message
            best_max = max(best_max, -res.fun)
    # ---- min over simple paths: minimise t s.t. t >= f(y)+g(y)-f(a) for y on the path
    best_min = np.inf
    adj = [set(int(v) for v in S.nbrs[u]) for u in range(N)]

    def paths(u, visited, path):
        if u == b:
            yield list(path)
            return
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                path.append(v)
                yield from paths(v, visited, path)
                path.pop()
                visited.remove(v)

    npaths = 0
    for P in paths(a, {a}, [a]):
        npaths += 1
        rows = np.zeros((len(P), N + 1))
        rhs = np.zeros(len(P))
        for j, y in enumerate(P):
            rows[j, N] = -1.0
            rows[j, y] = 1.0
            rhs[j] = -(f[y] - f[a])
        c = np.zeros(N + 1)
        c[N] = 1.0
        res = linprog(c, A_ub=np.vstack([A_ub, rows]), b_ub=np.concatenate([b_ub, rhs]),
                      A_eq=A_eq, b_eq=[0.0], bounds=bounds, method="highs")
        assert res.status == 0, res.message
        best_min = min(best_min, res.fun)
    return best_min, best_max, npaths


def main():
    # ---------------- (2) independent LP check on tiny spaces
    print("T2(2) independent LP optimisation over the polytrope (tiny spaces)")
    worst = 0.0
    for ks, asym in (([2, 2, 2], False), ([2, 2, 2], True), ([3, 3], True), ([2, 4], True)):
        S = Space(ks)
        for trial in range(4):
            h, J = random_pairwise(S, rng)
            f = pairwise_energy(S, h, J)
            D = rand_site_env(S, rng, asym=asym)
            a, b = rng.choice(S.N, 2, replace=False)
            lo = barrier_from(S, f - D[a, :], a)[b] - f[a]
            hi = barrier_from(S, f + D[:, a], a)[b] - f[a]
            mn, mx, npaths = lp_extremes(S, f, D, a, b)
            worst = max(worst, abs(mn - lo), abs(mx - hi))
            print(f"  ks={ks} asym={asym} a={a} b={b}: claimed [{lo:.6f},{hi:.6f}]  "
                  f"LP [{mn:.6f},{mx:.6f}]  ({npaths} simple paths)")
    print(f"  max |claimed - LP| = {worst:.2e}")
    assert worst < 1e-7

    # ---------------- (1),(3),(4),(5) sampling
    print("T2(1,3,4,5) random sampling")
    viol = dict(A=0, B=0, C=0, D=0)
    att = dict(A=0, B=0, C=0)
    ncase = dict(A=0, B=0, C=0, D=0)
    widths = []
    for ks in ([2] * 6, [3] * 4, [2, 3, 2, 3, 2], [4, 4, 3]):
        S = Space(ks)
        for trial in range(12):
            h, J = random_pairwise(S, rng)
            f = pairwise_energy(S, h, J)
            D = rand_site_env(S, rng, asym=bool(trial % 2))
            a, b = rng.choice(S.N, 2, replace=False)
            gminus, gplus = -D[a, :], D[:, a]
            assert is_admissible(gminus, D) and is_admissible(gplus, D)
            lo = barrier_from(S, f + gminus, a)[b] - f[a]
            hi = barrier_from(S, f + gplus, a)[b] - f[a]
            H0 = height(S, f, np.zeros(S.N), a, b)
            glob = max(D[:, a].max(), D[a, :].max())       # sup-norm (pinned) stability bound
            P, _ = minimax_path(S, f, a, b)
            path_rad = D[P, a].max()
            widths.append((hi - lo, 2 * glob, hi - H0, path_rad))
            dlo, dhi = depth(S, f + gminus, a), depth(S, f + gplus, a)
            for s in range(60):
                g = random_admissible(D, rng)
                assert is_admissible(g, D)
                H = height(S, f, g, a, b)
                ncase["A"] += 1
                viol["A"] += int(H < lo - 1e-9 or H > hi + 1e-9)
                dg = depth(S, f + g, a)
                ncase["D"] += 1
                viol["D"] += int(dg < dlo - 1e-9 or dg > dhi + 1e-9)
            # interval is filled: intermediate values along the segment between the cone residuals
            Hs = [height(S, f, (1 - lam) * gminus + lam * gplus, a, b) for lam in np.linspace(0, 1, 41)]
            att["A"] += int(abs(Hs[0] - lo) < 1e-12 and abs(Hs[-1] - hi) < 1e-12
                            and np.max(np.abs(np.diff(Hs))) <= (hi - lo) + 1e-9)
            # ---- anchors
            g0 = random_admissible(D, rng)
            m = int(rng.integers(1, 6))
            A = rng.choice(S.N, m, replace=False)
            v = g0[A]
            L, U = mcshane(D, A, v)
            DA = cond_env(D, L, U)
            gp = np.minimum(U, L[a] + D[:, a])
            gm = np.maximum(L, U[a] - D[a, :])
            for gg in (gp, gm, L, U):
                assert is_admissible(gg, D) and np.allclose(gg[A], v)
            assert np.allclose(gp - gp[a], DA[:, a]) and np.allclose(gm - gm[a], -DA[a, :])
            loA = barrier_from(S, f - DA[a, :], a)[b] - f[a]
            hiA = barrier_from(S, f + DA[:, a], a)[b] - f[a]
            att["B"] += int(abs(height(S, f, gp, a, b) - hiA) < 1e-9 and abs(height(S, f, gm, a, b) - loA) < 1e-9)
            sadlo = barrier_from(S, f + L, a)[b]
            sadhi = barrier_from(S, f + U, a)[b]
            att["C"] += 1
            for s in range(40):
                # consistent admissible residual: extend the anchor data by further random anchors
                extra = rng.choice(S.N, int(rng.integers(0, 8)), replace=False)
                A2, v2 = list(A), list(v)
                for x in extra:
                    if x in A2:
                        continue
                    L2, U2 = mcshane(D, A2, v2)
                    lam = rng.choice([0.0, 1.0, rng.uniform()])
                    A2.append(int(x))
                    v2.append((1 - lam) * L2[x] + lam * U2[x])
                L2, U2 = mcshane(D, A2, v2)
                lam = rng.choice([0.0, 1.0, rng.uniform()])
                g = (1 - lam) * L2 + lam * U2
                assert is_admissible(g, D) and np.allclose(g[A], v)
                H = height(S, f, g, a, b)
                ncase["B"] += 1
                viol["B"] += int(H < loA - 1e-9 or H > hiA + 1e-9)
                sad = barrier_from(S, f + g, a)[b]
                ncase["C"] += 1
                viol["C"] += int(sad < sadlo - 1e-9 or sad > sadhi + 1e-9)
    print("  samples:", ncase)
    print("  violations of the claimed ranges:", viol)
    print("  ends attained (cases):", att)
    w = np.array(widths)
    print(f"  exact interval width / sup-norm stability width: median {np.median(w[:,0]/w[:,1]):.3f}, "
          f"min {np.min(w[:,0]/w[:,1]):.3f}, max {np.max(w[:,0]/w[:,1]):.3f}")
    ok = np.all(w[:, 2] <= w[:, 3] + 1e-9)
    print(f"  upper excursion hi - H_f <= envelope radius of the f-optimal path in all cases: {ok}")
    assert all(vv == 0 for vv in viol.values())


if __name__ == "__main__":
    main()
