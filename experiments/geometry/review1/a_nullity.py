"""(a) Nullity formula  dim N(z) = max(K-1, dim Sym(3K) - (2n-3))  near the thresholds
n0(K) = ceil((9K^2+K+8)/4), for bond geometries NOT used by the authors, including unequal
bond lengths and unequal bond angles.  Also: are the null vectors the trivial quadrics?
Also an adversarial scan over special bond angles (attempt to falsify conjecture C(d))."""
import sys
import numpy as np
from mylib import build_chain, stack, e0_pairs, conic_system, nullspace, unvech


def n0(K):
    return -(-(9 * K * K + K + 8) // 4)


def instance(K, n, rng, kind, angle_deg=97.0):
    if kind == "homog":
        bonds = np.ones(n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(angle_deg))
    elif kind == "unequal_bonds":
        bonds = rng.uniform(0.7, 1.9, n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(angle_deg))
    elif kind == "hetero":
        bonds = rng.uniform(0.7, 1.9, n - 1)
        alphas = np.pi - np.deg2rad(rng.uniform(75, 150, n - 2))
    w = rng.dirichlet(np.ones(K) * 3)
    Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
    return w, Xs


def nullity(K, n, rng, kind, angle_deg=97.0, check_trivial=False):
    w, Xs = instance(K, n, rng, kind, angle_deg)
    Z = stack(Xs, w)
    m = 3 * K
    dim = m * (m + 1) // 2
    A = conic_system(Z, e0_pairs(n))
    N, s, rank = nullspace(A, dim)
    out = dim - rank
    gap = None
    if rank < len(s) and rank > 0:
        gap = s[rank] / s[rank - 1] if rank < len(s) else 0.0
    dist = None
    if check_trivial and out == K - 1 and K > 1:
        dist = 0.0
        for v in N:
            S = unvech(v, m)
            sk = np.array([np.trace(S[3 * k:3 * k + 3, 3 * k:3 * k + 3]) / 3 for k in range(K)])
            T = np.kron(np.diag(sk), np.eye(3))
            dist = max(dist, np.abs(S - T).max(), abs(w @ sk))
    return out, s[rank - 1] / s[0], dist


if __name__ == "__main__":
    rng = np.random.default_rng(20261126)
    print("== nullity vs formula; bond angle 97 deg (unit bonds), unequal bonds, heterogeneous ==")
    bad = 0
    for kind in ("homog", "unequal_bonds", "hetero"):
        for K in (1, 2, 3):
            m = 3 * K
            dim = m * (m + 1) // 2
            for n in range(max(4, n0(K) - 3), n0(K) + 3):
                res = []
                for rep in range(3):
                    nul, cond, dist = nullity(K, n, rng, kind, check_trivial=True)
                    res.append((nul, cond, dist))
                want = max(K - 1, dim - (2 * n - 3))
                ok = all(r[0] == want for r in res)
                bad += (not ok)
                dmax = max([r[2] for r in res if r[2] is not None], default=None)
                print(f"{kind:14s} K={K} n={n:3d} (n0={n0(K)}): nullities {[r[0] for r in res]} predicted {want} "
                      f"{'OK' if ok else 'MISMATCH'}; smallest kept sv ratio {min(r[1] for r in res):.1e}"
                      + (f"; dist of null space from trivial quadrics {dmax:.1e}" if dmax is not None else ""))
    print("mismatches:", bad)

    print("\n== adversarial scan over bond angles at n = n0(K) (unit bonds): nullity should be K-1 ==")
    angles = [20, 30, 45, 60, 70.528779, 72, 90, 100, 108, 109.4712206, 120, 135, 144, 150, 160, 170]
    for K in (1, 2, 3):
        m = 3 * K
        dim = m * (m + 1) // 2
        row = []
        for ang in angles:
            vals = [nullity(K, n0(K), rng, "homog", ang) for _ in range(3)]
            row.append((ang, sorted(set(v[0] for v in vals)), min(v[1] for v in vals)))
        print(f"K={K} n0={n0(K)}: " + "; ".join(f"{a:g}deg->{nu} (sv {c:.0e})" for a, nu, c in row))
    print("\n== same one atom below threshold: nullity should be dim - (2n-3) ==")
    for K in (1, 2, 3):
        m = 3 * K
        dim = m * (m + 1) // 2
        n = n0(K) - 1
        row = []
        for ang in angles:
            vals = [nullity(K, n, rng, "homog", ang) for _ in range(2)]
            row.append((ang, sorted(set(v[0] for v in vals))))
        print(f"K={K} n={n}: predicted {max(K-1, dim-(2*n-3))}: " + "; ".join(f"{a:g}->{nu}" for a, nu in row))
