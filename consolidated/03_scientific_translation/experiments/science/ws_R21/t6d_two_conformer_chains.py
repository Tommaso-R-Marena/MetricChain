"""T6d — two generic planar unit-bond chain conformers x1, x2 (own code; part (d) of T6, split off so that every
run stays far below the 20-minute limit).  For a given number of bonds: all chains of the form x1*A1 + x2*A2
(A_i 2x2) — the only chains that an ensemble with the mean squared distances (all pairs) of w1*x1 + w2*x2 can
charge — found by batched LM from random starts on the bond-length equations, and the identification test:
the largest mass that an ensemble with the same mean squared distances can put on the other chains found
(linear programme over the solutions; 0 <=> identified among the chains found).
Control: x1 and x2 themselves must be among the solutions reached.
usage: python3 -B t6d_two_conformer_chains.py <n_bonds> [n_inst] [starts]
"""
import sys
import numpy as np
from r21_common import *

NB = int(sys.argv[1])
N_INST = int(sys.argv[2]) if len(sys.argv) > 2 else 20
STARTS = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
rng = np.random.default_rng(2106 + NB)
print(f"T6d two-conformer chains  bonds={NB} instances={N_INST} starts={STARTS}  start", now())


def chain(phi):
    return np.stack([np.cos(phi), np.sin(phi)], axis=-1)


def lm_free(resfun, Z0, iters=300):
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


for nb in (NB,):
    n_inst = N_INST
    extra = []
    kerdim = []
    for inst in range(n_inst):
        ph1 = rng.uniform(0, 2 * np.pi, nb)
        ph2 = rng.uniform(0, 2 * np.pi, nb)
        C = np.hstack([chain(ph1[None])[0], chain(ph2[None])[0]])      # (nb, 4) rows c_u
        # dimension of {T symmetric 4x4 : c_u T c_u^T = 0 for all u}
        iu = np.triu_indices(4)
        Mq = np.array([[(c[i] * c[j] * (1 if i == j else 2)) for i, j in zip(*iu)] for c in C])   # (nb, 10)
        kerdim.append(10 - num_rank(Mq, 1e-10))

        def resfun(Z):
            M = Z.reshape(-1, 4, 2)
            v = np.einsum('uk,bkd->bud', C, M)                            # bond vectors of x1*A1 + x2*A2
            return np.sum(v * v, axis=2) - 1.0                            # (B, nb)

        Z0 = rng.standard_normal((STARTS, 8))
        Z, cost, gn = lm_free(resfun, Z0, iters=200)
        sol = cost < 1e-20
        Ms = Z[sol].reshape(-1, 4, 2)
        Ss = np.einsum('bkd,bld->bkl', Ms, Ms)                           # S = M M^T, invariant under O(2)
        S1 = np.zeros((4, 4)); S1[:2, :2] = np.eye(2)
        S2 = np.zeros((4, 4)); S2[2:, 2:] = np.eye(2)
        d1 = np.max(np.abs(Ss - S1), axis=(1, 2))
        d2 = np.max(np.abs(Ss - S2), axis=(1, 2))
        other = Ss[(d1 > 1e-6) & (d2 > 1e-6)]
        # distinct other solutions: round, unique, then merge rows closer than 1e-6 (max norm)
        if len(other):
            flat = np.unique(np.round(other.reshape(-1, 16), 5), axis=0)
            if len(flat) > 600:
                flat = flat[rng.choice(len(flat), 600, replace=False)]
            keep = np.ones(len(flat), dtype=bool)
            for a in range(len(flat)):
                if keep[a]:
                    dd = np.max(np.abs(flat[a + 1:] - flat[a]), axis=1) < 1e-6
                    keep[a + 1:][dd] = False
            uniq = [u.reshape(4, 4) for u in flat[keep]]
        else:
            uniq = []
        # identification test on the solutions found: an ensemble nu on chains x1*A1 + x2*A2 has the mean squared
        # distances of w1*x1 + w2*x2 iff sum_k nu_k S_k = w1*S1 + w2*S2 (the 4 columns of [x1c x2c] are independent).
        # LP: largest mass that such a nu can put on chains other than x1, x2 (0 <=> identified among the chains found).
        wts = np.array([0.4, 0.6])
        allS = [S1, S2] + uniq
        Amat = np.array([Sm[iu] for Sm in allS]).T                      # (10, n_sol)
        Amat = np.vstack([Amat, np.ones(len(allS))])
        rhs = np.concatenate([wts[0] * S1[iu] + wts[1] * S2[iu], [1.0]])
        cobj = -np.ones(len(allS)); cobj[:2] = 0.0
        from scipy.optimize import linprog
        lp = linprog(cobj, A_eq=Amat, b_eq=rhs, bounds=(0, None), method='highs')
        off = -lp.fun if lp.status == 0 else np.nan
        aff_indep = int(num_rank(Amat, 1e-9) == len(allS))
        extra.append((len(uniq), int(sol.sum()), int(np.sum(d1 <= 1e-6)), int(np.sum(d2 <= 1e-6)), off, aff_indep))
    ex = np.array(extra, dtype=float)
    print(f"    {nb:2d} bonds: dim of the space of quadrics through the bond vectors c_u = {sorted(set(kerdim))}; "
          f"instances with a chain other than x1, x2 (mod congruence) among the solutions: {int(np.sum(ex[:, 0] > 0))}/{n_inst}; "
          f"distinct extra solutions per instance (median, max; capped at 600) = {int(np.median(ex[:, 0]))}, {int(ex[:, 0].max())}; "
          f"runs reaching a solution: {int(ex[:, 1].sum())}/{STARTS*n_inst} (x1: {int(ex[:, 2].sum())}, x2: {int(ex[:, 3].sum())}); "
          f"IDENTIFICATION (weights 0.4/0.6): largest mass an ensemble with the same mean squared distances can put on the other chains found: "
          f"median {np.nanmedian(ex[:, 4]):.3f}, max {np.nanmax(ex[:, 4]):.3f}; instances where it is > 1e-6: {int(np.sum(ex[:, 4] > 1e-6))}/{n_inst}; "
          f"solutions affinely independent in {int(ex[:, 5].sum())}/{n_inst}")
    viol = int(np.sum((ex[:, 2] == 0) | (ex[:, 3] == 0)))
    print(f"    control: instances in which x1 or x2 was NOT reached by any start: {viol}/{n_inst}")
print("DONE t6d_two_conformer_chains", NB, now())
