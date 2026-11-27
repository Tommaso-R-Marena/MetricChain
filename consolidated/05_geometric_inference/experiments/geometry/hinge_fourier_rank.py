"""What the squared distances see of the differing torsions (HINGE_ENSEMBLES.md, Lemma M1; asked
by the Ensemble division, ENSEMBLE-RES-0003 "Requested response" (2)).

For a chain with s = 3 hinges (proper rotations only) the squared distances are functions of
(phi_1, phi_2, phi_3) in the 27-dimensional space of products of 1, cos phi_k, sin phi_k.
This script computes, from random samples of the hinge angles,
  * the dimension of the span of the squared distances (expected 2 s^2 + 1 = 19);
  * which products lie in that span: every product of two ADJACENT hinges does, no product of
    the non-adjacent pair (1, 3) does;
  * the same for s = 2 (rank 9: everything) and, with mirrored components, 5, 13, 25.
Floating point; residuals are relative least-squares residuals.
"""
import itertools
import sys
import numpy as np
from geomlib import chain, edm
from hinge_pairs import THETA


def data(n, hinges, rng, nsamp):
    t0 = rng.uniform(-np.pi, np.pi, n - 3)
    iu = np.triu_indices(n, 1)
    Phi, Ds = [], []
    for _ in range(nsamp):
        phi = rng.uniform(-np.pi, np.pi, len(hinges))
        t = t0.copy()
        t[hinges] = phi
        Phi.append(phi)
        Ds.append(edm(chain(n, t, theta=THETA))[iu])
    return np.array(Phi), np.array(Ds)


def monomials(Phi):
    s = Phi.shape[1]
    basis = [np.ones(len(Phi)), ]
    names = ["1"]
    one = [(np.ones(len(Phi)), "1"), ]
    per = [[(np.ones(len(Phi)), ""), (np.cos(Phi[:, k]), f"c{k+1}"), (np.sin(Phi[:, k]), f"s{k+1}")] for k in range(s)]
    cols, names = [], []
    for combo in itertools.product(range(3), repeat=s):
        v = np.ones(len(Phi))
        nm = ""
        for k, c in enumerate(combo):
            v = v * per[k][c][0]
            nm += per[k][c][1]
        cols.append(v)
        names.append(nm or "1")
    return np.array(cols).T, names


def in_span(target, A):
    coef, *_ = np.linalg.lstsq(A, target, rcond=None)
    return float(np.linalg.norm(A @ coef - target) / np.linalg.norm(target))


def main():
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    ok = True
    for s, hinges, n in ((2, [3, 8], 15), (3, [3, 8, 13], 20)):
        Phi, Ds = data(n, np.array(hinges), rng, 400)
        Mono, names = monomials(Phi)
        rank = np.linalg.matrix_rank(np.hstack([np.ones((len(Ds), 1)), Ds]), tol=1e-8)
        res_all = max(in_span(Ds[:, j], Mono) for j in range(0, Ds.shape[1], 7))
        A = np.hstack([np.ones((len(Ds), 1)), Ds])
        adj, non = [], []
        for nm, col in zip(names, Mono.T):
            idx = sorted({int(ch) for ch in nm if ch.isdigit()})
            if len(idx) == 2:
                (adj if idx[1] - idx[0] == 1 else non).append((nm, in_span(col, A)))
        print(f"s = {s} hinges (n = {n}): the squared distances lie in the span of the {3**s} products "
              f"(residual {res_all:.0e}); dimension of their span (with constants) = {rank} (expected {2*s*s+1})")
        print(f"   products of two adjacent hinges, residual of the fit by squared distances: max {max(r for _, r in adj):.1e}")
        if non:
            print(f"   products of the non-adjacent hinges 1 and 3: min residual {min(r for _, r in non):.2f} "
                  f"({', '.join(f'{nm}: {r:.2f}' for nm, r in non)})")
        ok &= rank == 2 * s * s + 1 and max(r for _, r in adj) < 1e-6 and (not non or min(r for _, r in non) > 1e-2)
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
