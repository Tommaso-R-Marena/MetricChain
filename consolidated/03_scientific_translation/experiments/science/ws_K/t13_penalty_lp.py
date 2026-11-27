"""
T13 — can a penalty replace the counter?  (report, Prop. K3 and the remark after it)

For a trap a with exit target b, I = all sites, q = Hamming distance from a, level r in 1..q(b):
   exact level minimum          m_r      = min_{q=r} E
   trivial barrier bound        max(E(a),E(b))
   linear multiplier            sup_lambda min_x [E + lambda (q - r)]              (integer programme, by enumeration)
   quadratic penalty, integer   min_x [E + mu (q - r)^2]                           (-> m_r as mu grows)
   quadratic penalty, LP leaf   pairwise LP relaxation (local polytope) of the same instance
                                = the best bound ONE leaf of the min-kernel can certify.
Binary sites, random pairwise "chain+" models, n = 10.

Run:  python3 t13_penalty_lp.py
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from kcore import Space, random_pairwise, pairwise_energy, local_minima, barrier_from

rng = np.random.default_rng(5)


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])])


def lp_relaxation(n, h, Jfull):
    """local-polytope LP for a binary pairwise model: h[i][a], Jfull[(i,j)][a,b] for all i<j."""
    pairs = list(itertools.combinations(range(n), 2))
    nv = 2 * n + 4 * len(pairs)
    c = np.zeros(nv)
    for i in range(n):
        c[2 * i:2 * i + 2] = h[i]
    A, bvec = [], []
    for i in range(n):
        row = np.zeros(nv); row[2 * i] = 1; row[2 * i + 1] = 1
        A.append(row); bvec.append(1.0)
    for pidx, (i, j) in enumerate(pairs):
        off = 2 * n + 4 * pidx
        c[off:off + 4] = np.asarray(Jfull[(i, j)]).ravel()          # order (a,b) = 00,01,10,11
        for a in (0, 1):
            row = np.zeros(nv); row[off + 2 * a] = 1; row[off + 2 * a + 1] = 1; row[2 * i + a] = -1
            A.append(row); bvec.append(0.0)
        for b in (0, 1):
            row = np.zeros(nv); row[off + b] = 1; row[off + 2 + b] = 1; row[2 * j + b] = -1
            A.append(row); bvec.append(0.0)
    res = linprog(c, A_eq=np.array(A), b_eq=np.array(bvec), bounds=[(0, None)] * nv, method="highs")
    assert res.status == 0
    return res.fun


def main():
    n = 10
    S = Space([2] * n)
    print("T13: level r of q = Hamming distance from the trap a; all values relative to E(a)")
    print("   inst trap   r   level-min  trivial  linear-mult | mu:  integer-penalty / LP-leaf-penalty")
    shown = 0
    for inst in range(8):
        h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
        E = pairwise_energy(S, h, J)
        for a in local_minima(S, E, strict=True):
            b = exit_target(S, E, a)
            if b is None:
                continue
            q = (S.cfg != S.cfg[a][None, :]).sum(axis=1)
            qb = int(q[b])
            prof = np.array([E[q == j].min() for j in range(n + 1)])
            r = int(np.argmax(prof[1:qb + 1]) + 1)
            if prof[r] - E[a] < 0.3:
                continue
            triv = max(E[a], E[b])
            # linear multiplier (integer programme): convex envelope of the profile at r
            lam = np.linspace(-20, 20, 4001)
            lin = max(np.min(prof + l * (np.arange(n + 1) - r)) for l in lam)
            line = (f"   {inst:<4d} {a:<6d} {r:<3d} {prof[r] - E[a]:<10.3f} {triv - E[a]:<8.3f} {lin - E[a]:<11.3f} |")
            ok = lin <= triv + 1e-9
            for mu in (0.0, 0.5, 2.0, 8.0, 32.0):
                ip = np.min(E + mu * (q - r) ** 2)
                # pairwise form of the penalty: z_i = [x_i != a_i]
                hh = [np.array(h[i], dtype=float).copy() for i in range(n)]
                Jf = {}
                for i in range(n):
                    flipped = 1 - S.cfg[a, i]
                    hh[i][flipped] += mu * (1 - 2 * r)
                for (i, j) in itertools.combinations(range(n), 2):
                    M = np.array(J[(i, j)], dtype=float).copy() if (i, j) in J else np.zeros((2, 2))
                    M[1 - S.cfg[a, i], 1 - S.cfg[a, j]] += 2 * mu
                    Jf[(i, j)] = M
                lp = lp_relaxation(n, hh, Jf) + mu * r * r
                assert lp <= ip + 1e-7 and ip <= prof[r] + 1e-9
                line += f"  {mu:g}: {ip - E[a]:.2f} / {lp - E[a]:.2f}"
                ok &= True
            print(line)
            shown += 1
            if shown >= 8:
                break
        if shown >= 8:
            break
    print("   (integer penalty -> level-min as mu grows; the LP-leaf value collapses for large mu)")
    # ---- systematic: best LP-leaf value over a grid of mu, for the top level of every trap
    print("T13(b): best single-leaf value over mu in {0.25, 0.5, ..., 6}, top level r of each trap")
    grid = np.arange(0.25, 6.01, 0.25)
    fr = []
    for inst in range(12):
        h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
        E = pairwise_energy(S, h, J)
        for a in local_minima(S, E, strict=True):
            b = exit_target(S, E, a)
            if b is None:
                continue
            q = (S.cfg != S.cfg[a][None, :]).sum(axis=1)
            qb = int(q[b])
            prof = np.array([E[q == j].min() for j in range(n + 1)])
            r = int(np.argmax(prof[1:qb + 1]) + 1)
            Hlev = prof[r] - E[a]
            if Hlev <= 1e-9:
                continue
            best = -np.inf
            for mu in grid:
                hh = [np.array(h[i], dtype=float).copy() for i in range(n)]
                Jf = {}
                for i in range(n):
                    hh[i][1 - S.cfg[a, i]] += mu * (1 - 2 * r)
                for (i, j) in itertools.combinations(range(n), 2):
                    M = np.array(J[(i, j)], dtype=float).copy() if (i, j) in J else np.zeros((2, 2))
                    M[1 - S.cfg[a, i], 1 - S.cfg[a, j]] += 2 * mu
                    Jf[(i, j)] = M
                lp = lp_relaxation(n, hh, Jf) + mu * r * r
                assert lp <= prof[r] + 1e-7
                best = max(best, lp)
            fr.append((max(best - E[a], 0.0) / Hlev, r))
    fr = np.array(fr)
    print(f"   {len(fr)} traps: mean certified fraction of the level height {fr[:,0].mean():.2f}; "
          f"exact (>= 0.999) in {np.mean(fr[:,0] > 0.999):.0%}; nothing (0) in {np.mean(fr[:,0] <= 1e-9):.0%}; "
          f"levels r: {sorted(set(int(x) for x in fr[:,1]))}")


if __name__ == "__main__":
    main()
