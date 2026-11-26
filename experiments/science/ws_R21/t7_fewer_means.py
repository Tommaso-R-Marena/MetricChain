"""T7 — Proposition C of the R21 report (own code): one conformation is identified, among all ensembles,
by |E| + d(d+1)/2 means instead of the 2|E| of Corollary E8 (K = 1), when the framework has a positive
semidefinite equilibrium stress matrix Omega of rank N - d - 1 (complete graphs K_N, N >= d + 2):
      f(p) = tr(p^T Omega p) + sum_{e in E2} ( t_e(p) - t_e(x) )^2 ,
E2 = d(d+1)/2 = 3 edges (plane) whose directions are not on a conic at infinity.
Checked for K4 and K5 in the plane, 10 random frameworks each:
  * Omega is psd, of rank N - 3, in equilibrium;  tr(p^T Omega p) = sum_e omega_e t_e(p) (so f is in the
    span of 1, l_e^2 (e in E), l_e^4 (e in E2));
  * zeros of f found by minimisation from 2000 random starts are all congruent to x
    (control: such zeros ARE reached);
  * negative control: with only two edges in E2 (directions on a conic) non-congruent zeros appear.
"""
import itertools
import numpy as np
from r21_common import *

rng = np.random.default_rng(2107)
print("T7 fewer means for one conformation  start", now())


def psd_stress(x):
    """sum over (d+2)-subsets S of a_S a_S^T, a_S the affine dependency of the points of S (plane: 4-subsets)."""
    N = x.shape[0]
    Om = np.zeros((N, N))
    for S in itertools.combinations(range(N), 4):
        M = np.vstack([x[list(S)].T, np.ones(4)])           # 3 x 4
        a = np.linalg.svd(M)[2][-1]
        v = np.zeros(N)
        v[list(S)] = a
        Om += np.outer(v, v)
    return Om


def lm_fd(resfun, Z0, iters=300):
    def fun(Z, want_jac):
        r = resfun(Z)
        if not want_jac:
            return r, None
        h = 1e-6
        J = np.zeros((Z.shape[0], r.shape[1], Z.shape[1]))
        for k in range(Z.shape[1]):
            Zp = Z.copy(); Zp[:, k] += h
            Zm = Z.copy(); Zm[:, k] -= h
            J[:, :, k] = (resfun(Zp) - resfun(Zm)) / (2 * h)
        return r, J
    return batched_lm(fun, Z0, iters=iters)


tot_viol = 0
for name in ("K4", "K5"):
    N, E = graph_table()[name]
    EF = complete(N)
    n_inst = 10
    stats = dict(psd=0, rank=0, eq=0.0, span=0.0, zero_cong=0, zero_non=0, zero_non_neg=0, zero_cong_neg=0, conic=0)
    for inst in range(n_inst):
        x = rng.standard_normal((N, 2))
        Om = psd_stress(x)
        ev = np.linalg.eigvalsh(Om)
        stats['psd'] += int(ev.min() > -1e-10)
        stats['rank'] += int(np.sum(ev > 1e-9 * ev.max()) == N - 3)
        stats['eq'] = max(stats['eq'], np.max(np.abs(Om @ x)), np.max(np.abs(Om @ np.ones(N))))
        # tr(p^T Om p) = sum_e omega_e t_e(p), omega_e = -Om[u,v]
        Pr = rng.standard_normal((50, N, 2))
        lhs = np.einsum('bud,uv,bvd->b', Pr, Om, Pr)
        rhs = sqlen(Pr, E) @ np.array([-Om[u, v] for (u, v) in E])
        stats['span'] = max(stats['span'], np.max(np.abs(lhs - rhs)))
        w, U = np.linalg.eigh(Om)
        L = U[:, w > 1e-9 * w.max()] * np.sqrt(w[w > 1e-9 * w.max()])     # Om = L L^T
        for which, E2 in (("pos", [(0, 1), (0, 2), (1, 2)]), ("neg", [(0, 1), (0, 2)])):
            dirs = np.array([x[u] - x[v] for (u, v) in E2])
            conic_rank = num_rank(np.array([[dv[0] ** 2, 2 * dv[0] * dv[1], dv[1] ** 2] for dv in dirs]))
            if which == "pos":
                stats['conic'] += int(conic_rank == 3)
            t2 = sqlen(x, E2)

            def resfun(Z):
                P = Z.reshape(-1, N, 2)
                a = np.einsum('uk,bud->bkd', L, P).reshape(Z.shape[0], -1)
                b = sqlen(P, E2) - t2
                return np.hstack([a, b])

            Z0 = 1.5 * rng.standard_normal((2000, 2 * N))
            Z, cost, gn = lm_fd(resfun, Z0)
            zero = cost < 1e-18
            dT = np.max(np.abs(sqlen(Z.reshape(-1, N, 2), EF) - sqlen(x, EF)), axis=1)
            if which == "pos":
                stats['zero_cong'] += int(np.sum(zero & (dT <= 1e-6)))
                stats['zero_non'] += int(np.sum(zero & (dT > 1e-6)))
            else:
                stats['zero_cong_neg'] += int(np.sum(zero & (dT <= 1e-6)))
                stats['zero_non_neg'] += int(np.sum(zero & (dT > 1e-6)))
    print(f"{name}: |E| = {len(E)}; means used: |E| + 3 = {len(E) + 3} (Corollary E8 with K = 1: {2*len(E)}). {n_inst} random frameworks:")
    print(f"    Omega psd {stats['psd']}/{n_inst}; rank N-3 {stats['rank']}/{n_inst}; max |Omega x|, |Omega 1| = {stats['eq']:.1e}; "
          f"max |tr(p^T Omega p) - sum_e omega_e t_e(p)| on random p = {stats['span']:.1e}; E2 directions not on a conic {stats['conic']}/{n_inst}")
    print(f"    zeros of f from {2000*n_inst} minimisations: congruent to x {stats['zero_cong']} (control: must be > 0), "
          f"NOT congruent to x {stats['zero_non']} (Proposition C: must be 0)")
    print(f"    negative control, E2 = two edges (on a conic): zeros congruent to x {stats['zero_cong_neg']}, NOT congruent {stats['zero_non_neg']} (must be > 0)")
    tot_viol += (n_inst - stats['psd']) + (n_inst - stats['rank']) + stats['zero_non'] + int(stats['zero_cong'] == 0) + int(stats['zero_non_neg'] == 0)
print("violations:", tot_viol)
print("DONE t7_fewer_means", now())
