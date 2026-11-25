"""
T3 — query model: "barrier certificates are coverings of a separator and of a path".

Setting: f known, g true residual (admissible for d), E = f+g, anchors A with v = g|_A,
slack s(a',y) = d(a',y) - g(a') + g(y) >= 0, s(A,y) = min_a' s(a',y), s(y,A) = min_a' s(y,a').
McShane: L_A = g - s(A,.), U_A = g + s(.,A)   (theory report Thm 11.3).
Consistent saddle energies range over [LB(A), UB(A)] = [B_{f+L_A}(p,q), B_{f+U_A}(p,q)]  (T2, Claim C).

Claim (lower):  LB(A) >= B_E - eps  <=>  W_eps(A) = {y : s(A,y) <= E(y) - B_E + eps} separates p from q.
Claim (upper):  UB(A) <= B_E + eps  <=>  V_eps(A) = {y : s(y,A) <= B_E + eps - E(y)} connects p and q.

(i)  random test of both equivalences.
(ii) minimal numbers of evaluations (brute force over anchor sets, N=16):
       N_low(eps), N_up(eps) for the barrier  vs  N_point(eps) for the minimum (theory Thm 11.4).
(iii) mean-field barrier f = phi(|x|) on the n-cube, g = 0, uniform Hamming envelope c:
       for eps < min(c, phi(m)-max(phi(m±1))) the lower certificate must contain the whole
       transition layer: N_low = C(n,m).
Run:  python3 t3_cover.py
"""
import itertools
from math import comb
import numpy as np
from kcore import (Space, barrier_from, random_pairwise, pairwise_energy, mcshane, random_admissible,
                   separates, connects, is_admissible)

rng = np.random.default_rng(11)


def slack_sets(D, g, A):
    A = np.asarray(A, dtype=np.int64)
    s_from = (D[A, :] - g[A][:, None] + g[None, :]).min(axis=0)      # s(A,y)
    s_to = (D[:, A] - g[:, None] + g[A][None, :]).min(axis=1)        # s(y,A)
    return s_from, s_to


def main():
    # ---------------- (i) equivalences
    n_low = n_up = 0
    bad_low = bad_up = 0
    true_low = true_up = 0
    for ks in ([2] * 5, [3] * 3, [2, 3, 4], [2] * 7):
        S = Space(ks)
        for trial in range(40):
            h, J = random_pairwise(S, rng)
            f = pairwise_energy(S, h, J)
            c = rng.uniform(0.2, 1.5, S.n)
            D = S.hamming_env(c)
            kappa = rng.choice([0.0, 0.5, 1.0])
            g = kappa * random_admissible(D, rng)
            assert is_admissible(g, D)
            E = f + g
            p, q = rng.choice(S.N, 2, replace=False)
            BE = barrier_from(S, E, p)[q]
            m = int(rng.integers(1, max(2, S.N // 3)))
            A = rng.choice(S.N, m, replace=False)
            L, U = mcshane(D, A, g[A])
            s_from, s_to = slack_sets(D, g, A)
            assert np.allclose(L, g - s_from) and np.allclose(U, g + s_to)
            LB = barrier_from(S, f + L, p)[q]
            UB = barrier_from(S, f + U, p)[q]
            assert LB <= BE + 1e-9 <= UB + 2e-9
            for eps in (0.0, 0.1, 0.3, 1.0, BE - LB, UB - BE, 0.5 * (BE - LB), 0.5 * (UB - BE)):
                # a tolerance-free comparison: skip eps values within 1e-9 of a threshold
                if abs((BE - LB) - eps) < 1e-9 or abs((UB - BE) - eps) < 1e-9:
                    eps = eps + 1e-6
                W = s_from <= E - BE + eps
                V = s_to <= BE + eps - E
                lhs_low = LB >= BE - eps
                rhs_low = separates(S, W, p, q)
                lhs_up = UB <= BE + eps
                rhs_up = connects(S, V, p, q)
                n_low += 1
                n_up += 1
                bad_low += int(lhs_low != rhs_low)
                bad_up += int(lhs_up != rhs_up)
                true_low += int(lhs_low)
                true_up += int(lhs_up)
    print(f"T3(i) lower equivalence: {n_low} tests, {bad_low} mismatches ({true_low} true instances)")
    print(f"T3(i) upper equivalence: {n_up} tests, {bad_up} mismatches ({true_up} true instances)")
    assert bad_low == 0 and bad_up == 0

    # ---------------- (ii) minimal certificate sizes on N=16
    print("T3(ii) minimal numbers of evaluations, 4 binary sites (N=16), brute force over anchor sets")
    S = Space([2] * 4)
    rows = []
    for trial in range(12):
        h, J = random_pairwise(S, rng, scale_J=1.5)
        f = pairwise_energy(S, h, J)
        c = np.full(S.n, 0.6)
        D = S.hamming_env(c)
        g = 0.5 * random_admissible(D, rng, kind="mix")
        E = f + g
        # choose p = global min, q = the local minimum with the largest barrier from p
        p = int(np.argmin(E))
        Bp = barrier_from(S, E, p)
        cand = [u for u in range(S.N) if u != p and np.all(E[S.nbrs[u]] >= E[u])]
        if not cand:
            continue
        q = max(cand, key=lambda u: Bp[u] - E[u])
        BE = Bp[q]
        Emin = E.min()
        res = {}
        for eps in (0.05, 0.3):
            nl = nu = npnt = None
            for size in range(0, S.N + 1):
                for A in itertools.combinations(range(S.N), size):
                    if size == 0:
                        continue
                    A = np.array(A)
                    L, U = mcshane(D, A, g[A])
                    if nl is None and barrier_from(S, f + L, p)[q] >= BE - eps:
                        nl = size
                    if nu is None and barrier_from(S, f + U, p)[q] <= BE + eps:
                        nu = size
                    if npnt is None and E[A].min() - (f + L).min() <= eps:
                        npnt = size
                    if nl is not None and nu is not None and npnt is not None:
                        break
                if nl is not None and nu is not None and npnt is not None:
                    break
            res[eps] = (nl, nu, npnt)
        rows.append((trial, p, q, BE - E[p], res))
        print(f"  inst {trial}: height {BE - E[p]:.2f}; (N_low, N_up, N_point[min]) at eps=0.05: {res[0.05]}, "
              f"eps=0.3: {res[0.3]}")

    # ---------------- (iii) mean-field barrier: whole transition layer
    print("T3(iii) mean-field barrier on the n-cube, g=0, uniform envelope c=1")
    for n, phi in ((4, [0, 1, 2.5, 1, 0]), (5, [0, 1.2, 2.5, 4.0, 1.0, 0.3])):
        S = Space([2] * n)
        wt = S.cfg.sum(axis=1)
        f = np.array(phi)[wt]
        D = S.hamming_env(np.ones(n))
        g = np.zeros(S.N)
        p, q = 0, S.N - 1
        BE = barrier_from(S, f, p)[q]
        mtop = int(np.argmax(phi))
        layer = np.nonzero(wt == mtop)[0]
        eps = 0.5
        # (a) the layer itself is a certificate; (b) no anchor set of size C(n,m)-1 is; brute force
        L, U = mcshane(D, layer, g[layer])
        ok_layer = barrier_from(S, f + L, p)[q] >= BE - eps
        target = comb(n, mtop)
        found_smaller = False
        if S.N <= 16:
            for size in range(1, target):
                for A in itertools.combinations(range(S.N), size):
                    A = np.array(A)
                    L, U = mcshane(D, A, g[A])
                    if barrier_from(S, f + L, p)[q] >= BE - eps:
                        found_smaller = True
                        break
                if found_smaller:
                    break
            how = "exhaustive over all smaller anchor sets"
        else:
            # removing any single layer point breaks it, and random sets of size target-1 fail
            for drop in range(len(layer)):
                A = np.delete(layer, drop)
                L, U = mcshane(D, A, g[A])
                found_smaller |= bool(barrier_from(S, f + L, p)[q] >= BE - eps)
            for r in range(3000):
                A = rng.choice(S.N, target - 1, replace=False)
                L, U = mcshane(D, A, g[A])
                found_smaller |= bool(barrier_from(S, f + L, p)[q] >= BE - eps)
            how = "layer minus one point (all) + 3000 random sets of size C(n,m)-1"
        print(f"  n={n}, phi={phi}: B={BE}, top layer m={mtop}, C(n,m)={target}; layer certifies: {ok_layer}; "
              f"smaller certificate found: {found_smaller}  [{how}]")
        # upper certificate: one monotone path suffices (n+1 evaluations), fewer for eps>0
        path = [int(sum(2 ** (n - 1 - i) for i in range(j))) for j in range(n + 1)]
        L, U = mcshane(D, path, g[path])
        print(f"     upper certificate from one monotone path ({n+1} evaluations): "
              f"UB - B = {barrier_from(S, f + U, p)[q] - BE:.3f}")


if __name__ == "__main__":
    main()
