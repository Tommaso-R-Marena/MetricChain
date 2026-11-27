"""Label patterns (docs/geometry/LABEL_PATTERNS.md): only a subset S of the points of a chain is
observed, through all ensemble-averaged squared distances among S.

The statewise equality constraints that survive are the labelled pairs at chain separation 1 or 2
(a bond, or the fixed 1-3 distance); c(S) is their number.  This script checks, in floating point:

 (1) the conic (linear) certificate holds, and DEMIX recovers the labelled-site states, exactly
     when c(S) >= D_K - K + 1 = (9K^2 + K + 2)/2 -- for an anchor stretch with sparse labels,
     scattered triples, scattered adjacent pairs, every second point, mixed runs;
 (2) with sparse labels (no two labelled points at separation 1 or 2) the data do not determine
     the ensemble: rotating the stacked configuration of the labelled sites gives labelled-site
     configurations of OTHER chains (fitted here, to rounding) with the same data;
 (3) regularity: the map torsions -> shape of the labelled sites has full rank 3|S| - 6 when all
     gaps are >= 3 (so nearby labelled-site configurations are realised by chains).

Usage: python3 label_patterns.py
"""
import itertools
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares

import demix as DM
from geomlib import chain, edm, kabsch_rmsd, quad_row, stack, sym_index

THETA = np.deg2rad(111.0)


def constrained_pairs(S, theta=THETA):
    """Pairs of positions in the sorted list S whose chain separation is 1 or 2, with their lengths."""
    S = sorted(S)
    c13 = float(np.sqrt(2 - 2 * np.cos(theta)))
    edges, lengths = [], []
    for a in range(len(S)):
        for b in range(a + 1, len(S)):
            sep = S[b] - S[a]
            if sep > 2:
                break
            edges.append((a, b))
            lengths.append(1.0 if sep == 1 else c13)
    return edges, lengths


def needed(K):
    return 3 * K * (3 * K + 1) // 2 - (K - 1)


def conic_nullity(Xs, w, S, tol=1e-9):
    S = sorted(S)
    Z = stack([X[S] for X in Xs], w)
    edges, _ = constrained_pairs(S)
    idx = sym_index(Z.shape[1])
    if not edges:
        return len(idx), 0
    A = np.array([quad_row(Z[j] - Z[i], idx) for (i, j) in edges])
    sv = np.linalg.svd(A, compute_uv=False)
    return len(idx) - int((sv > tol * sv[0]).sum()), len(edges)


def demix_pattern(Xs, w, S):
    """DEMIX on the labelled data.  Returns (certified, RMSD of the recovered labelled-site states)."""
    S = sorted(S)
    M = sum(wk * edm(X[S]) for wk, X in zip(w, Xs))
    edges, lengths = constrained_pairs(S)
    if not edges:
        return False, None
    out = DM.demix(M, edges, lengths)
    if not out["ok"]:
        return False, None
    return True, DM.match_error([X[S] for X in Xs], w, out)[0]


def random_mixture(K, n, seed):
    rng = np.random.default_rng(seed)
    w = rng.dirichlet(np.ones(K) * 4)
    return [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(K)], w


def triples(T, gap):
    return sorted(set(itertools.chain.from_iterable((s, s + 1, s + 2) for s in range(0, T * gap, gap))))


def pairs(T, gap):
    return sorted(set(itertools.chain.from_iterable((s, s + 1) for s in range(0, T * gap, gap))))


def runs(lengths, gap):
    out, pos = [], 0
    for r in lengths:
        out += list(range(pos, pos + r))
        pos += r + gap
    return out


PATTERNS = (
    # name, K, n, labelled set
    ("anchor of 12 consecutive points + 7 sparse labels", 2, 60, sorted(list(range(20, 32)) + [0, 7, 13, 40, 47, 55, 59])),
    ("anchor of 11 (one short) + 7 sparse labels", 2, 60, sorted(list(range(20, 31)) + [0, 7, 13, 40, 47, 55, 59])),
    ("7 scattered triples", 2, 60, triples(7, 8)),
    ("6 scattered triples", 2, 60, triples(6, 8)),
    ("20 scattered adjacent pairs", 2, 102, pairs(20, 5)),
    ("19 scattered adjacent pairs", 2, 102, pairs(19, 5)),
    ("every second point, 21 labels", 2, 45, list(range(0, 42, 2))),
    ("every second point, 20 labels", 2, 45, list(range(0, 40, 2))),
    ("four runs of 4", 2, 40, runs([4, 4, 4, 4], 5)),
    ("three runs of 4 and a pair", 2, 40, runs([4, 4, 4, 2], 5)),
    ("every third point (no constrained pair)", 2, 60, list(range(0, 60, 3))),
    ("three states: anchor of 23 + 6 sparse labels", 3, 80, sorted(list(range(30, 53)) + [0, 9, 17, 60, 70, 79])),
    ("three states: 15 scattered triples", 3, 95, triples(15, 6)),
    ("three states: 14 scattered triples", 3, 95, triples(14, 6)),
)


def fit_chain(n, S, target, t0):
    """Torsions t such that the labelled sites of chain(n, t) are congruent to `target`."""
    def resid(t):
        X = chain(n, t, theta=THETA)[S]
        A, B = X - X.mean(0), target - target.mean(0)
        U, _, Vt = np.linalg.svd(A.T @ B)
        R = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Vt))]) @ Vt
        return (A @ R - B).ravel()
    r = least_squares(resid, t0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
    return r.x, float(np.linalg.norm(resid(r.x)))


def second_solution(n=41, gap=4, eps=0.05, seed=0, orthogonal=True):
    """Two states, labels every `gap`-th point: another two-state ensemble of chains with the same
    averaged squared distances among the labelled sites.  Returns a dict with the truth, the second
    solution and the checks.  orthogonal=False is a planted error (the stack is sheared)."""
    rng = np.random.default_rng(seed)
    S = list(range(0, n, gap))
    w = np.array([0.4, 0.6])
    ts = [rng.uniform(-np.pi, np.pi, n - 3) for _ in range(2)]
    Xs = [chain(n, t, theta=THETA) for t in ts]
    Ys = [X[S] - X[S].mean(0) for X in Xs]
    Z = np.hstack([np.sqrt(wk) * Y for wk, Y in zip(w, Ys)])
    G = rng.normal(size=(6, 6))
    Q = expm(eps * (G - G.T)) if orthogonal else np.eye(6) + eps * G
    Z2 = Z @ Q
    new = [Z2[:, :3] / np.sqrt(w[0]), Z2[:, 3:] / np.sqrt(w[1])]
    fits = [fit_chain(n, S, Y, t) for Y, t in zip(new, ts)]
    chains = [chain(n, f[0], theta=THETA) for f in fits]
    M_true = sum(wk * edm(X[S]) for wk, X in zip(w, Xs))
    M_new = sum(wk * edm(X[S]) for wk, X in zip(w, chains))
    return {"S": S, "weights": w, "truth": Xs, "second": chains,
            "fit_residual": max(f[1] for f in fits), "data_difference": float(np.abs(M_true - M_new).max()),
            "moved": min(min(kabsch_rmsd(X[S], Y[S]) for X in Xs) for Y in chains)}


def labelled_shape_rank(n, S, seed=0, h=1e-6):
    """Rank of the derivative of torsions -> squared distances among the labelled sites."""
    rng = np.random.default_rng(seed)
    t0 = rng.uniform(-np.pi, np.pi, n - 3)
    pr = [(a, b) for i, a in enumerate(S) for b in S[i + 1:]]

    def f(t):
        X = chain(n, t, theta=THETA)
        return np.array([np.sum((X[a] - X[b]) ** 2) for a, b in pr])
    J = np.array([(f(t0 + h * e) - f(t0 - h * e)) / (2 * h) for e in np.eye(n - 3)]).T
    s = np.linalg.svd(J, compute_uv=False)
    return int((s > 1e-7 * s[0]).sum())


def main():
    ok = True
    print("(1) linear certificate and DEMIX on label patterns: certified iff c(S) >= (9K^2 + K + 2)/2")
    for name, K, n, S in PATTERNS:
        Xs, w = random_mixture(K, n, seed=K * 100 + len(S))
        nul, c = conic_nullity(Xs, w, S)
        cert, rmsd = demix_pattern(Xs, w, S)
        want = c >= needed(K)
        D = 3 * K * (3 * K + 1) // 2
        good = (cert == want) and nul == max(K - 1, D - c) and (not cert or rmsd < 1e-5)
        ok &= good
        print(f"    K = {K}: {name:48s} |S| = {len(S):3d}, c = {c:3d} (needed {needed(K)}), nullity {nul:2d}: "
              f"{'certified, states recovered to RMSD %.0e' % rmsd if cert else 'refused'}   {'OK' if good else 'FAIL'}")
    print("(2) sparse labels: a second two-state ensemble of chains with the same labelled data")
    for gap, eps in ((4, 0.03), (6, 0.1)):
        r = second_solution(gap=gap, eps=eps)
        good = r["fit_residual"] < 1e-9 and r["data_difference"] < 1e-9 and r["moved"] > 1e-2
        ok &= good
        print(f"    labels every {gap}th point ({len(r['S'])} labels): chains fitted to {r['fit_residual']:.0e}; data differ by "
              f"{r['data_difference']:.0e}; labelled sites moved by RMSD {r['moved']:.2f}   {'OK' if good else 'FAIL'}")
    print("(3) regularity: rank of torsions -> labelled shape, against 3|S| - 6")
    for gap in (3, 4, 6):
        S = list(range(0, 41, gap))
        rk = labelled_shape_rank(41, S)
        good = rk == 3 * len(S) - 6
        ok &= good
        print(f"    labels every {gap}th point: rank {rk} of {3 * len(S) - 6}   {'OK' if good else 'FAIL'}")
    S = list(range(0, 41, 2))
    rk = labelled_shape_rank(41, S)
    c = len(constrained_pairs(S)[0])
    good = rk == min(38, 3 * len(S) - 6 - c)
    ok &= good
    print(f"    labels every 2nd point: rank {rk} = min(number of torsions 38, 3|S| - 6 - c = {3 * len(S) - 6 - c})   {'OK' if good else 'FAIL'}")
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
