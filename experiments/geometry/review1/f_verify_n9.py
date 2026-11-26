"""(f) Careful recount of the real PSD rank-3 points of P(z) for K = 2, n = 9 (finite set), with
more starts, a Newton polish, and an isolation check (Jacobian rank 15 modulo the O(3) gauge)."""
import sys
import numpy as np
from multiprocessing import Pool
from b_pz import make_problem, solve_one, unpackA

def run(seed, nstart, angle=97.0):
    pr = make_problem(2, 9, seed, angle)
    Z, E, L2, w = pr["Z"], pr["E"], pr["L2"], pr["w"]
    with Pool(4) as pool:
        out = pool.map(solve_one, [(E, L2, 6, 31 * seed + 104729 * s + 1) for s in range(nstart)], chunksize=32)
    good = [A for r, A in out if r < 1e-12]
    distinct = []
    for A in good:
        P = A.T @ A
        for d in distinct:
            if np.abs(P - d[0]).max() < 1e-7:
                d[2] += 1
                break
        else:
            distinct.append([P, A, 1])
    forced = [np.kron(np.diag([1.0 if j == k else 0.0 for j in range(2)]), np.eye(3)) / w[k] for k in range(2)]
    rows = []
    for P, A, hits in distinct:
        ev = np.linalg.eigvalsh(P)
        res = np.abs(((E @ A.T) ** 2).sum(1) - L2).max()
        # Jacobian of the 15 equations w.r.t. A (18 unknowns): rank 15 <=> isolated modulo O(3)
        Y = E @ A.T
        J = (2 * Y[:, :, None] * E[:, None, :]).reshape(len(E), -1)
        sv = np.linalg.svd(J, compute_uv=False)
        isf = any(np.abs(P - Fk).max() < 1e-6 for Fk in forced)
        rows.append((isf, hits, res, ev[2], ev[3], sv[14] / sv[0]))
    mind = min(np.abs(distinct[i][0] - distinct[j][0]).max() for i in range(len(distinct)) for j in range(i))
    nf = sum(r[0] for r in rows)
    print(f"seed {seed} (angle {angle}): {nstart} starts, {len(good)} converged; distinct points {len(distinct)} = {nf} forced + {len(distinct) - nf} others; "
          f"min pairwise distance {mind:.3f}; min hits {min(r[1] for r in rows)}; max residual {max(r[2] for r in rows):.1e}; "
          f"max |3rd smallest eig| {max(abs(r[3]) for r in rows):.1e}; min 4th eig {min(r[4] for r in rows):.3f}; min Jacobian sv15/sv1 {min(r[5] for r in rows):.1e}")
    return len(distinct) - nf

if __name__ == "__main__":
    ang = float(sys.argv[1]) if len(sys.argv) > 1 else 97.0
    counts = [run(s, 6000, ang) for s in range(0, 9)]
    print("numbers of further real PSD rank-3 points:", counts)
