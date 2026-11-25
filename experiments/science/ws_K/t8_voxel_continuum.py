"""
T8 — do discrete barrier certificates mean anything for the continuous potential-energy surface?

Claim (continuum bracket).  E continuous on the torus T^d, voxels = products of k arcs per torsion,
tables E_lo(V) <= min_V E, E_hi(V) >= max_V E.  On the FACE-ADJACENCY graph (one torsion moves to a
neighbouring arc):
        B_disc[E_lo](V(a), V(b))  <=  B_cont(a, b)  <=  B_disc[E_hi](V(a), V(b)).
With UNRESTRICTED single-site moves (any arc -> any arc of one torsion; the programme's default Hamming
graph) only the left inequality survives, and it degenerates: a torsion may "jump" over its own barrier.

Also: "certified relaxed scan" = coordinate cut on the cyclic site graph:
        B >= min over the two arcs of torsion i between the arc of a and the arc of b of
             max_{s in arc} m_i(s),      m_i(s) = min_{x : x_i = s} E_lo(x)   (k global minimisations).

Test potential (2 and 3 torsions):
   E = sum_i (1 + cos 3 theta_i) + 1.5 cos(theta_1 - theta_2) + 0.7 cos(theta_1 + 2 theta_2 + 0.4)
       [+ 1.2 cos(theta_2 - theta_3) + 0.5 cos(theta_3 - 2 theta_1 + 1.0)   for d = 3]
Enclosures from analytic gradient bounds G_i: |E(theta) - E(centre)| <= sum_i G_i * pi/k.

Run:  python3 t8_voxel_continuum.py
"""
import heapq
import itertools
import numpy as np


def energy(theta):
    th = np.asarray(theta)
    d = th.shape[-1]
    E = (1 + np.cos(3 * th)).sum(axis=-1)
    E = E + 1.5 * np.cos(th[..., 0] - th[..., 1]) + 0.7 * np.cos(th[..., 0] + 2 * th[..., 1] + 0.4)
    if d == 3:
        E = E + 1.2 * np.cos(th[..., 1] - th[..., 2]) + 0.5 * np.cos(th[..., 2] - 2 * th[..., 0] + 1.0)
    return E


def grad_bounds(d):
    G = np.array([3 + 1.5 + 0.7, 3 + 1.5 + 1.4])
    if d == 3:
        G = np.array([3 + 1.5 + 0.7 + 1.0, 3 + 1.5 + 1.4 + 1.2, 3 + 1.2 + 0.5])
    return G


def grid_tables(d, k):
    centres = (np.arange(k) + 0.5) * 2 * np.pi / k
    mesh = np.stack(np.meshgrid(*([centres] * d), indexing="ij"), axis=-1)
    Ec = energy(mesh)
    slack = grad_bounds(d).sum() * np.pi / k
    return Ec - slack, Ec + slack, Ec


def minimax(Etab, src, dst, mode="face"):
    """minimax barrier on the voxel grid; mode 'face' = +-1 moves (cyclic), 'complete' = any arc of one torsion."""
    shape = Etab.shape
    d = len(shape)
    k = shape[0]
    Ef = Etab.ravel()
    strides = [k ** (d - 1 - i) for i in range(d)]
    s = int(np.ravel_multi_index(src, shape))
    t = int(np.ravel_multi_index(dst, shape))
    B = np.full(Ef.size, np.inf)
    B[s] = Ef[s]
    done = np.zeros(Ef.size, dtype=bool)
    heap = [(Ef[s], s)]
    while heap:
        b, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        if u == t:
            return b
        for i in range(d):
            ci = (u // strides[i]) % k
            steps = (1, -1) if mode == "face" else range(1, k)
            for st in steps:
                v = u + (((ci + st) % k) - ci) * strides[i]
                if done[v]:
                    continue
                nb = b if b >= Ef[v] else Ef[v]
                if nb < B[v]:
                    B[v] = nb
                    heapq.heappush(heap, (nb, v))
    return B[t]


def scan_bound(Etab, src, dst, i):
    """certified relaxed scan along torsion i (coordinate cut on the cyclic site graph)."""
    k = Etab.shape[0]
    axes = tuple(j for j in range(Etab.ndim) if j != i)
    prof = Etab.min(axis=axes)
    sa, sb = src[i], dst[i]
    if sa == sb:
        return -np.inf
    arc1 = [(sa + j) % k for j in range(0, ((sb - sa) % k) + 1)]
    arc2 = [(sa - j) % k for j in range(0, ((sa - sb) % k) + 1)]
    return min(prof[arc1].max(), prof[arc2].max())


def local_min(theta0, d):
    from scipy.optimize import minimize
    res = minimize(lambda t: float(energy(t)), theta0, method="BFGS", options=dict(gtol=1e-10))
    return np.mod(res.x, 2 * np.pi), res.fun


def main():
    for d, ks, kref in ((2, (6, 12, 24, 48, 96, 192), 720), (3, (6, 12, 24, 48), 96)):
        # two distinct local minima: the global one and the best one that differs in torsion 1
        rng = np.random.default_rng(0)
        found = {}
        for trial in range(200):
            th, val = local_min(rng.uniform(0, 2 * np.pi, d), d)
            key = tuple(np.round(th, 3))
            found[key] = (val, th)
        mins = sorted(found.values(), key=lambda p: p[0])
        a_val, a_th = mins[0]
        b_val, b_th = None, None
        for val, th in mins[1:]:
            if abs(((th[0] - a_th[0] + np.pi) % (2 * np.pi)) - np.pi) > 1.0:
                b_val, b_th = val, th
                break
        print(f"T8 d={d}: {len(mins)} local minima found; a = {np.round(a_th, 3)} E={a_val:.4f};  "
              f"b = {np.round(b_th, 3)} E={b_val:.4f}")
        # reference: finest bracket
        lo, hi, Ec = grid_tables(d, kref)
        va = tuple((a_th / (2 * np.pi) * kref).astype(int) % kref)
        vb = tuple((b_th / (2 * np.pi) * kref).astype(int) % kref)
        ref_lo = minimax(lo, va, vb)
        ref_hi = minimax(hi, va, vb)
        print(f"   reference bracket of B_cont from k={kref}: [{ref_lo:.4f}, {ref_hi:.4f}]  "
              f"(height above a: [{ref_lo - a_val:.4f}, {ref_hi - a_val:.4f}])")
        print("   k     B_lo(face)  B_hi(face)  contains ref?  B_lo(complete)  trivial=max(E_lo(a),E_lo(b))  "
              "scan bounds per torsion (E_lo)")
        ok_all = True
        for k in ks:
            lo, hi, Ec = grid_tables(d, k)
            va = tuple((a_th / (2 * np.pi) * k).astype(int) % k)
            vb = tuple((b_th / (2 * np.pi) * k).astype(int) % k)
            blo = minimax(lo, va, vb)
            bhi = minimax(hi, va, vb)
            ok = blo <= ref_lo + 1e-9 and bhi >= ref_hi - 1e-9
            ok_all &= ok
            bcomp = minimax(lo, va, vb, mode="complete") if lo.size * k <= 3e6 else np.nan
            triv = max(lo[va], lo[vb])
            scans = [scan_bound(lo, va, vb, i) for i in range(d)]
            assert all(sc <= blo + 1e-9 for sc in scans)
            assert np.isnan(bcomp) or bcomp <= blo + 1e-9
            print(f"   {k:<5d} {blo:<11.4f} {bhi:<11.4f} {str(ok):<14s} {bcomp:<15.4f} {triv:<29.4f} "
                  + "  ".join(f"{sc:.4f}" for sc in scans))
        print(f"   all brackets nested around the reference: {ok_all}")


if __name__ == "__main__":
    main()
