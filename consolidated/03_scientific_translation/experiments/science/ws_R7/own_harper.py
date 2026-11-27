"""R7 OWN: fractional hitting number FC_n(eps) over ALL sensitive sets on the uniform cube.

Written from the theory definition only (docs/workstreams/A_REPORT.md section 2.0), BEFORE reading
ENG-RES-0006 or experiments/eng/fc_uniform_cube/harper_fc.py.

Definition (A_REPORT 2.0, uniform cube: S={0,1}, pi uniform, slack s_n(x,y) = u * d_H(x,y), beta = 1):
  for D a proper nonempty subset of {0,1}^n:  h_D(y) = min_{x not in D} s_n(x,y) = u * d_H(y, D^c)
  D is sensitive at level eps  iff  ln E_pi exp(h_D) > eps
  FC_n(eps) = 1 / max_q min_{D sensitive} q(D)          (q a probability vector on the cube)

My derivation (see R7_REPORT section 2, statement H1-H3):
  (H1) the family of sensitive sets is invariant under the automorphism group of the cube, which is
       transitive, and q -> min_D q(D) is concave, so the uniform q is optimal:
       FC_n(eps) = 2^n / m*,  m* = least size of a sensitive set.
  (H2) for |D| = m fixed, sum_y exp(u d(y, D^c)) = (2^n - m) + sum_{j>=1} (|D_j| - |D_{j+1}|) e^{uj},
       D_j = {d(., D^c) >= j} = complement of Gamma^{j-1}(D^c); by Harper's vertex-isoperimetric theorem
       all |Gamma^t(D^c)| are minimised simultaneously when D^c is an initial segment of the simplicial
       order; hence the maximum over |D| = m is attained at the complement of that initial segment.
  (H3) these optimal sets are nested, so F(m) = max_{|D|=m} E exp(h_D) is nondecreasing and
       m* = min{m : ln F(m) > eps}  (binary search).

This file computes
  * brute force over all 2^(2^n) - 2 proper nonempty subsets, n <= 4: least sensitive size, AND the LP
    max_q min_D q(D) WITHOUT the symmetry assumption (checks H1), AND for every size m the true maximum
    of the sum against the simplicial-order value (checks H2);
  * the Harper value for n <= 14 from explicit simplicial-order sets (no closed-form shortcut);
  * the single-dip (ball) value.
"""
import itertools
import json
import math
import sys

import numpy as np


def popcount(x):
    return bin(x).count("1")


def simplicial_order(n):
    """Points of {0,1}^n (as ints; bit i <-> coordinate i+1) in simplicial order:
    by weight, then lexicographically as sets (the set containing the smallest element of the
    symmetric difference comes first)."""
    pts = list(range(1 << n))
    key = lambda x: (popcount(x), tuple(-((x >> i) & 1) for i in range(n)))
    return sorted(pts, key=key)


def dist_to_complement(n, inD):
    """inD: boolean array over the 2^n points.  Returns d(y, D^c) (0 off D) by multi-source BFS."""
    N = 1 << n
    d = np.where(inD, -1, 0).astype(np.int64)
    frontier = np.nonzero(~inD)[0]
    step = 0
    idx = np.arange(N)
    while len(frontier):
        step += 1
        nxt = []
        for i in range(n):
            nb = frontier ^ (1 << i)
            new = nb[d[nb] == -1]
            d[new] = step
            nxt.append(new)
        frontier = np.unique(np.concatenate(nxt)) if nxt else np.empty(0, dtype=np.int64)
    return d


def log_mean_exp_h(n, inD, u):
    d = dist_to_complement(n, inD)
    return math.log(np.exp(u * d).sum() / (1 << n))


def harper_set(n, m, order=None):
    """Complement of the initial segment of size 2^n - m of the simplicial order (|D| = m)."""
    order = order or simplicial_order(n)
    inD = np.zeros(1 << n, dtype=bool)
    inD[order[(1 << n) - m:]] = True
    return inD


def harper_mstar(n, u, eps, order=None):
    """Least m (1 <= m <= 2^n - 1) such that the Harper set of size m is sensitive; None if none."""
    order = order or simplicial_order(n)
    N = 1 << n
    f = lambda m: log_mean_exp_h(n, harper_set(n, m, order), u)
    if not f(N - 1) > eps:
        return None
    lo, hi = 1, N - 1            # invariant: f(hi) > eps
    if f(lo) > eps:
        return 1
    while hi - lo > 1:           # f(lo) <= eps < f(hi)
        mid = (lo + hi) // 2
        if f(mid) > eps:
            hi = mid
        else:
            lo = mid
    return hi


def ball_mstar(n, u, eps):
    """Single dips: D = closed Hamming ball of radius R (R = 0..n-1).  Least |D| that is sensitive."""
    for R in range(0, n):
        tot = sum(math.comb(n, j) * math.exp(u * (R + 1 - j)) for j in range(0, R + 1)) + sum(math.comb(n, j) for j in range(R + 1, n + 1))
        if math.log(tot / (1 << n)) > eps:
            return sum(math.comb(n, j) for j in range(0, R + 1)), R
    return None, None


# ---------------------------------------------------------------- brute force, n <= 4

def brute(n, params):
    """All proper nonempty subsets.  For each (u, eps): least sensitive size, number of minimal sensitive sets,
    LP value max_q min_D q(D); and for each size m the max of sum exp(u d) against the Harper set."""
    N = 1 << n
    lo_masks = [sum(1 << p for p in range(N) if not (p >> i) & 1) for i in range(n)]
    full = (1 << N) - 1

    def gamma(A):                      # closed neighbourhood of a set of points (bitmask over points)
        out = A
        for i in range(n):
            sh = 1 << i
            out |= ((A & lo_masks[i]) << sh) | ((A & ~lo_masks[i] & full) >> sh)
        return out

    # layer counts: cnt[D] = tuple (#{d=1}, #{d=2}, ...) ; computed once per subset
    layers = {}
    for D in range(1, full):
        comp = full & ~D
        counts = []
        cur = comp
        while cur != full:
            nxt = gamma(cur)
            counts.append(popcount(nxt & ~cur))
            cur = nxt
        layers[D] = tuple(counts)
    order = simplicial_order(n)
    out = []
    for (u, eps) in params:
        val = {}
        for D, c in layers.items():
            val[D] = (N - popcount(D)) + sum(cj * math.exp(u * (j + 1)) for j, cj in enumerate(c))
        thr = N * math.exp(eps)
        sens = [D for D in val if val[D] > thr]
        margin = min(abs(math.log(v / N) - eps) for v in val.values())
        # check H2: for each size m, max over |D| = m equals the Harper set's value
        best = {}
        for D, v in val.items():
            m = popcount(D)
            if v > best.get(m, -1):
                best[m] = v
        h2_dev = 0.0
        for m in range(1, N):
            hv = N * math.exp(log_mean_exp_h(n, harper_set(n, m, order), u))
            h2_dev = max(h2_dev, abs(hv - best[m]) / best[m])
        rec = dict(n=n, u=u, eps=eps, n_sensitive=len(sens), margin=margin, H2_max_rel_dev=h2_dev)
        if sens:
            mstar = min(popcount(D) for D in sens)
            sset = set(sens)
            # minimal sensitive sets: no sensitive proper subset obtained by deleting one point
            minimal = [D for D in sens if all(((D & ~(1 << p)) not in sset) for p in range(N) if (D >> p) & 1 and D & ~(1 << p))]
            rec.update(mstar_brute=mstar, n_minimal=len(minimal))
            # LP without symmetry: max t  s.t.  q(D) >= t for all minimal sensitive D, sum q = 1, q >= 0
            from scipy.optimize import linprog
            A = np.zeros((len(minimal), N + 1))
            for r, D in enumerate(minimal):
                for p in range(N):
                    if (D >> p) & 1:
                        A[r, p] = -1.0
                A[r, N] = 1.0
            c = np.zeros(N + 1); c[N] = -1.0
            res = linprog(c, A_ub=A, b_ub=np.zeros(len(minimal)), A_eq=np.array([[1.0] * N + [0.0]]), b_eq=[1.0],
                          bounds=[(0, None)] * N + [(None, None)], method="highs")
            rec.update(lp_value=float(-res.fun), uniform_value=mstar / N, FC_brute=N / mstar,
                       lp_minus_uniform=float(-res.fun - mstar / N))
            hm = harper_mstar(n, u, eps, order)
            rec.update(mstar_harper=hm, agree=(hm == mstar))
        else:
            rec.update(mstar_brute=None, mstar_harper=harper_mstar(n, u, eps, order))
            rec["agree"] = rec["mstar_harper"] is None
        out.append(rec)
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "brute":
        us = [0.25, 0.5, 1.0, 2.0, 3.0]
        epss = [0.05, 0.1, 0.3, 0.5, 1.0, 2.0]
        res = []
        for n in (2, 3, 4):
            r = brute(n, [(u, e) for u in us for e in epss])
            res += r
            for x in r:
                print(x, flush=True)
        json.dump(res, open("out_own_harper_brute.json", "w"), indent=1)
        bad = [x for x in res if not x["agree"]]
        print("cases", len(res), "disagreements", len(bad), "max |LP - uniform|",
              max(abs(x.get("lp_minus_uniform", 0.0)) for x in res), "max H2 dev", max(x["H2_max_rel_dev"] for x in res),
              "min margin", min(x["margin"] for x in res))
    elif mode == "table":
        nmax = int(sys.argv[2])
        res = []
        for (u, eps) in [(1.0, 0.3), (1.0, 1.0), (2.0, 0.3), (0.5, 0.3)]:
            for n in range(1, nmax + 1):
                order = simplicial_order(n)
                m = harper_mstar(n, u, eps, order)
                mb, R = ball_mstar(n, u, eps)
                rec = dict(u=u, eps=eps, n=n, mstar=m, FC=(None if m is None else (1 << n) / m), ball_size=mb, ball_radius=R,
                           FC_dip=(None if mb is None else (1 << n) / mb))
                if m is not None and mb is not None:
                    rec["ratio"] = mb / m
                res.append(rec)
                print(rec, flush=True)
        json.dump(res, open("out_own_harper_table.json", "w"), indent=1)
