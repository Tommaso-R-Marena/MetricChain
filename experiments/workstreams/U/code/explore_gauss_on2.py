#!/usr/bin/env python3
"""Exploration (not a proof): orthant-nest family ON in the small-slope limit, vectorised.

Units a = 1, h = 1/4.  Levels j = 1..k with opening thresholds tau_j >= 0 (or "no new
direction": the level is a truncation of the previous cone), plateau depths
0 = lam_0 <= lam_1 <= ... <= lam_{k-1}.  At depth lam >= lam_{j-1} the threshold of direction j
is y_j(lam) = tau_j + lam - lam_{j-1}.
  J(i->m) = sum_{i<j<=m, j has a direction} y_j(lam_{m-1})^2
  g_i(lam) = 2 lam - sum_{j<=i} y_j(lam)^2 ;  M_i = max_{[lam_{i-1}, lam_i]} g_i ;  M_0 = 0
  significance: M_k >= max_{i<k} M_i   (lam_k = +inf)
  V_r = min over paths with <= r jumps of the largest jump.
Random search (vectorised) followed by local improvement.
"""
import sys, itertools
import numpy as np

rng = np.random.default_rng(20261125)


def evaluate(tau, dlam, mask, rmax):
    """tau: (N,k) thresholds; dlam: (N,k-1) plateau increments; mask: tuple of 0/1 (has direction).
    Returns (viol (N,), V (N, rmax+1))."""
    N, k = tau.shape
    lam = np.concatenate([np.zeros((N, 1)), np.cumsum(dlam, axis=1)], axis=1)  # lam_0..lam_{k-1}
    msk = np.array(mask, dtype=float)[None, :]
    # y_j(l) = tau_j + l - lam_{j-1} for l >= lam_{j-1}
    def g(i, l):  # i directions open, l: (N,)
        y = tau[:, :i] + l[:, None] - lam[:, :i]
        return 2 * l - np.sum(msk[:, :i] * y ** 2, axis=1)
    def gprime(i, l):
        y = tau[:, :i] + l[:, None] - lam[:, :i]
        return 2 - 2 * np.sum(msk[:, :i] * y, axis=1)
    M = [np.zeros(N)]
    for i in range(1, k + 1):
        lo = lam[:, i - 1].copy()
        hi = lam[:, i].copy() if i < k else lo + 8.0
        # concave: maximise by bisection on g'
        a_, b_ = lo.copy(), hi.copy()
        for _ in range(60):
            mid = 0.5 * (a_ + b_)
            pos = gprime(i, mid) > 0
            a_ = np.where(pos, mid, a_)
            b_ = np.where(pos, b_, mid)
        M.append(g(i, 0.5 * (a_ + b_)))
    Mx = np.max(np.stack(M[:-1], axis=1), axis=1)
    viol = np.maximum(0.0, Mx - M[-1])
    # jumps
    J = np.zeros((N, k + 1, k + 1))
    for m in range(1, k + 1):
        y = tau[:, :m] + lam[:, m - 1][:, None] - lam[:, :m]
        sq = msk[:, :m] * y ** 2
        for i in range(0, m):
            J[:, i, m] = np.sum(sq[:, i:m], axis=1)
    INF = 1e18
    best = np.full((N, k + 1), INF)
    best[:, 0] = 0.0
    V = np.zeros((N, rmax + 1))
    for t in range(1, rmax + 1):
        new = best.copy()
        for m in range(1, k + 1):
            for i in range(0, m):
                c = np.maximum(best[:, i], J[:, i, m])
                new[:, m] = np.minimum(new[:, m], c)
        best = new
        V[:, t] = best[:, k]
    return viol, V


def search(k, mask, r, rounds=6, N=200000):
    tau = rng.uniform(0, 0.7, (N, k))
    dlam = rng.uniform(0, 0.6, (N, k - 1)) * (rng.uniform(size=(N, k - 1)) > 0.2)
    bestv, bestx = -1.0, None
    scale = 0.15
    for it in range(rounds):
        viol, V = evaluate(tau, dlam, mask, r)
        score = np.where(viol < 1e-9, V[:, r], -viol)
        idx = np.argsort(-score)[:200]
        if score[idx[0]] > bestv:
            bestv = score[idx[0]]
            bestx = (tau[idx[0]].copy(), dlam[idx[0]].copy())
        # resample around the elite
        pick = rng.choice(idx, size=N)
        tau = np.abs(tau[pick] + scale * rng.standard_normal((N, k)) * (rng.uniform(size=(N, k)) < 0.5))
        dlam = np.abs(dlam[pick] + scale * rng.standard_normal((N, k - 1)) * (rng.uniform(size=(N, k - 1)) < 0.5))
        tau[0], dlam[0] = bestx
        scale *= 0.55
    return bestv, bestx


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for k in range(1, kmax + 1):
        for mask in itertools.product([1, 0], repeat=k):
            if mask[0] == 0:
                continue
            if any(mask[i] == 0 and mask[i - 1] == 0 for i in range(1, k)):
                continue
            line = f"k={k} mask={mask}:"
            for r in range(1, k + 1):
                v, x = search(k, mask, r, rounds=10, N=120000 if k <= 4 else 60000)
                line += f"  V_{r}={v:.4f}"
                if r == 2 and x is not None:
                    line += " [tau=" + ",".join(f"{t:.3f}" for t in x[0]) + " dlam=" + ",".join(f"{t:.3f}" for t in x[1]) + "]"
            print(line, flush=True)
