"""(i) Proposition 6.1: referee's own implementation of DEMIX from the description in section 6,
on ensembles built with the referee's chain builder (bond angle 97 deg; unequal bonds).
Also: behaviour below the threshold, on helical states, and the size of s* (the smallest
non-trivial singular value of the conic system) at n0 and above (authors' geometry 111 deg)."""
import itertools
import numpy as np
from mylib import build_chain, sqdist, stack, e0_pairs, conic_system, nullspace, unvech


def demix(M, pairs, lengths, d=3, rank_tol=1e-8, null_tol=1e-7, rng=None):
    rng = rng or np.random.default_rng(0)
    n = len(M)
    J = np.eye(n) - np.ones((n, n)) / n
    G = -0.5 * J @ M @ J
    ev, V = np.linalg.eigh(G)
    ev, V = ev[::-1], V[:, ::-1]
    r = int((ev > rank_tol * ev[0]).sum())
    if r % d:
        return dict(ok=False, why=f"rank {r} not a multiple of {d}")
    K = r // d
    Z = V[:, :r] * np.sqrt(ev[:r])
    dim = r * (r + 1) // 2
    A = conic_system(Z, pairs)
    N, s, rank = nullspace(A, dim, rtol=null_tol)
    if dim - rank != K - 1:
        return dict(ok=False, why=f"certificate fails: nullity {dim - rank}, expected {K - 1}", K=K, s=s)
    sstar = s[rank - 1] / s[0]
    if K == 1:
        return dict(ok=True, K=1, weights=np.array([1.0]), states=[Z], sstar=sstar)
    T = sum(c * unvech(v, r) for c, v in zip(rng.normal(size=K - 1), N))
    tv, Q = np.linalg.eigh(T)
    # eigenvalues must come in K groups of multiplicity d
    groups = tv.reshape(K, d)
    mult_err = np.abs(groups - groups.mean(1, keepdims=True)).max()
    states, weights = [], []
    i, j = pairs[0]
    for k in range(K):
        Qk = Q[:, d * k:d * k + d]
        Y = Z @ Qk
        wk = ((Y[j] - Y[i]) ** 2).sum() / lengths[0] ** 2
        weights.append(wk)
        states.append(Y / np.sqrt(wk))
    return dict(ok=True, K=K, weights=np.array(weights), states=states, sstar=sstar, mult_err=mult_err)


def compare(Xs, w, out):
    K = len(w)
    best = (np.inf, np.inf)
    for perm in itertools.permutations(range(K)):
        e = max(np.abs(sqdist(Xs[k]) - sqdist(out["states"][perm[k]])).max() for k in range(K))
        dw = max(abs(w[k] - out["weights"][perm[k]]) for k in range(K))
        best = min(best, (e, dw))
    return best


if __name__ == "__main__":
    rng = np.random.default_rng(77)
    print("DEMIX on exact data (own implementation):")
    for K, n, kind in ((1, 5, "unit"), (2, 12, "unit"), (2, 12, "unequal"), (2, 15, "unequal"), (3, 23, "unit"), (3, 26, "unequal"), (4, 39, "unit")):
        bonds = np.ones(n - 1) if kind == "unit" else rng.uniform(0.8, 1.7, n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(97.0))
        w = rng.dirichlet(np.ones(K) * 4)
        Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
        M = sum(wk * sqdist(X) for wk, X in zip(w, Xs))
        pairs = e0_pairs(n)
        D0 = sqdist(Xs[0])
        lengths = [np.sqrt(D0[i, j]) for (i, j) in pairs]
        out = demix(M, pairs, lengths)
        if not out["ok"]:
            print(f"   K={K} n={n} {kind}: REFUSED: {out['why']}")
            continue
        e, dw = compare(Xs, w, out)
        print(f"   K={K} n={n:2d} {kind:7s}: recovered K={out['K']}; max|D(state) - D(true)| = {e:.1e}; max weight error {dw:.1e}; s* = {out['sstar']:.1e}")
    print("below the threshold / degenerate inputs:")
    for K, n, mode in ((2, 11, "random"), (2, 8, "random"), (2, 14, "helices"), (2, 14, "one planar state"), (2, 14, "equal states")):
        bonds = np.ones(n - 1)
        alphas = np.full(n - 2, np.pi - np.deg2rad(97.0))
        w = rng.dirichlet(np.ones(K) * 4)
        if mode == "helices":
            Xs = [build_chain(np.full(n - 3, rng.uniform(-np.pi, np.pi)), bonds, alphas) for _ in range(K)]
        elif mode == "one planar state":
            Xs = [build_chain(rng.choice([0.0, np.pi], n - 3), bonds, alphas), build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas)]
        elif mode == "equal states":
            t = rng.uniform(-np.pi, np.pi, n - 3)
            Xs = [build_chain(t, bonds, alphas), build_chain(-t, bonds, alphas)]      # mirror images: congruent
        else:
            Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
        M = sum(wk * sqdist(X) for wk, X in zip(w, Xs))
        pairs = e0_pairs(n)
        D0 = sqdist(Xs[0])
        out = demix(M, pairs, [np.sqrt(D0[i, j]) for (i, j) in pairs])
        print(f"   K={K} n={n} {mode}: " + (f"REFUSED: {out['why']}" if not out["ok"] else f"returned K={out['K']}"))
    print("s* (smallest non-trivial singular value / largest) at bond angle 111 deg, K = 2, 20 instances each:")
    for n in (12, 13, 14, 16, 20):
        vals = []
        for rep in range(20):
            bonds = np.ones(n - 1)
            alphas = np.full(n - 2, np.pi - np.deg2rad(111.0))
            w = rng.dirichlet(np.ones(2) * 4)
            Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(2)]
            Z = stack(Xs, w)
            s = np.linalg.svd(conic_system(Z, e0_pairs(n)), compute_uv=False)
            sfull = np.concatenate([s, np.zeros(max(0, 21 - len(s)))])
            vals.append(sfull[19])                      # 20th singular value (index 19): last non-trivial
        vals = np.array(vals)
        print(f"   n={n}: s* (absolute) min {vals.min():.1e}, median {np.median(vals):.1e}, max {vals.max():.1e}")
