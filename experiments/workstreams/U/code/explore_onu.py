#!/usr/bin/env python3
"""Exploration (not a proof): nests of cones with independent centres on the cube at finite u
(family ON_u).  Level j opens at depth l_{j-1} (per coordinate, i.e. psi = -n*l) as a ball of radius
kappa_j*n around an independent uniformly random centre; at depth l >= l_{j-1} its radius is
rho_j(l) = kappa_j - (l - l_{j-1})/u.  With f(rho) = KL(rho||1/2) (0 for rho >= 1/2, +inf for rho < 0):
  J(i->m) = sum_{i<j<=m} f(rho_j(l_{m-1}))            (independent centres: probabilities multiply)
  g_i(l)  = l - sum_{j<=i} f(rho_j(l)),  M_i = max over [l_{i-1}, l_i],  M_0 = 0
  significance: M_k >= max_{i<k} M_i
  V_r = min over paths with <= r jumps of the largest jump.
Necessary conditions tested: sup V_1 <= a = KL(p_u||1/2), sup V_inf <= h = KL(Lambda_1/u||1/2).
usage: explore_onu.py u kmax
"""
import sys, itertools
import numpy as np

rng = np.random.default_rng(20261125)
BIG = 50.0


def f(rho):
    r = np.clip(rho, 1e-300, 0.5)
    val = np.log(2.0) + r * np.log(r) + (1 - r) * np.log1p(-r)
    val = np.where(rho >= 0.5, 0.0, val)
    val = np.where(rho <= 0.0, np.log(2.0) + BIG * (-rho), val)  # penalise negative radii
    return val


def evaluate(kap, dl, mask, rmax, u):
    N, k = kap.shape
    lam = np.concatenate([np.zeros((N, 1)), np.cumsum(dl, axis=1)], axis=1)
    msk = np.array(mask, dtype=float)[None, :]

    def rho(i, l):
        return kap[:, :i] - (l[:, None] - lam[:, :i]) / u

    def g(i, l):
        return l - np.sum(msk[:, :i] * f(rho(i, l)), axis=1)

    M = [np.zeros(N)]
    for i in range(1, k + 1):
        lo = lam[:, i - 1].copy()
        if i < k:
            hi = lam[:, i].copy()
        else:
            # radii must stay nonnegative: l <= lam_{j-1} + u*kap_j for directions j
            lim = lam[:, :k] + u * kap[:, :k]
            lim = np.where(msk > 0, lim, np.inf)
            hi = np.maximum(lo, np.min(lim, axis=1))
        # g_i concave on the range where all radii are in [0, 1/2]; golden-section-free: grid + refine
        best = np.full(N, -np.inf)
        a_, b_ = lo.copy(), hi.copy()
        for _ in range(4):
            ts = np.linspace(0, 1, 41)
            vals = np.stack([g(i, a_ + t * (b_ - a_)) for t in ts], axis=1)
            j = np.argmax(vals, axis=1)
            best = np.maximum(best, vals[np.arange(N), j])
            w = (b_ - a_) / 40
            c = a_ + ts[j] * (b_ - a_)
            a_, b_ = np.maximum(a_, c - w), np.minimum(b_, c + w)
        M.append(best)
    Mx = np.max(np.stack(M[:-1], axis=1), axis=1)
    viol = np.maximum(0.0, Mx - M[-1])
    J = np.zeros((N, k + 1, k + 1))
    for m in range(1, k + 1):
        fr = msk[:, :m] * f(rho(m, lam[:, m - 1]))
        for i in range(0, m):
            J[:, i, m] = np.sum(fr[:, i:m], axis=1)
    INF = 1e18
    best = np.full((N, k + 1), INF)
    best[:, 0] = 0.0
    V = np.zeros((N, rmax + 1))
    for t in range(1, rmax + 1):
        new = best.copy()
        for m in range(1, k + 1):
            for i in range(0, m):
                new[:, m] = np.minimum(new[:, m], np.maximum(best[:, i], J[:, i, m]))
        best = new
        V[:, t] = best[:, k]
    return viol, V


def search(k, mask, r, u, rounds=10, N=100000):
    kap = rng.uniform(0, 0.6, (N, k))
    dl = rng.uniform(0, 0.5 * u, (N, k - 1)) * (rng.uniform(size=(N, k - 1)) > 0.2)
    bestv, bestx = -1.0, None
    scale = 0.12
    for it in range(rounds):
        viol, V = evaluate(kap, dl, mask, r, u)
        score = np.where(viol < 1e-9, V[:, r], -viol)
        idx = np.argsort(-score)[:200]
        if score[idx[0]] > bestv:
            bestv = score[idx[0]]
            bestx = (kap[idx[0]].copy(), dl[idx[0]].copy())
        pick = rng.choice(idx, size=N)
        kap = np.abs(kap[pick] + scale * rng.standard_normal((N, k)) * (rng.uniform(size=(N, k)) < 0.5))
        dl = np.abs(dl[pick] + scale * u * rng.standard_normal((N, k - 1)) * (rng.uniform(size=(N, k - 1)) < 0.5))
        kap[0], dl[0] = bestx
        scale *= 0.55
    return bestv, bestx


if __name__ == "__main__":
    u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    pu = 1 / (1 + np.exp(u))
    Lam1 = np.log(2 / (1 + np.exp(-u)))
    a = float(f(np.array(pu)))
    h = float(f(np.array(Lam1 / u)))
    print(f"u={u}: p_u={pu:.5f} rho_h={Lam1/u:.5f} a={a:.6f} h={h:.6f} h/a={h/a:.4f}", flush=True)
    for k in range(1, kmax + 1):
        for mask in itertools.product([1, 0], repeat=k):
            if mask[0] == 0:
                continue
            if any(mask[i] == 0 and mask[i - 1] == 0 for i in range(1, k)):
                continue
            line = f"k={k} mask={mask}:"
            for r in range(1, k + 1):
                v, x = search(k, mask, r, u)
                line += f"  V_{r}/a={v/a:.4f} (V_{r}/h={v/h:.4f})"
                if r == 2 and x is not None:
                    line += " [kap=" + ",".join(f"{t:.3f}" for t in x[0]) + " dl=" + ",".join(f"{t:.3f}" for t in x[1]) + "]"
            print(line, flush=True)
