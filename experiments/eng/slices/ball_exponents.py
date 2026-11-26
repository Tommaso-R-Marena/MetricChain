"""X-008: smallest sensitive balls on a type class of the cube (THY-REQ-0010, question 2).

Type class T_k = {x in {0,1}^n : |x| = k}, uniform measure, Hamming distance, slope u.  A *ball* is

    D(m, i0) = {x in T_k : |x AND c| >= i0}        for a centre c of type |c| = m, 0 <= m <= n,

i.e. the points of T_k at Hamming distance at most m + k - 2 i0 from c (the distance from c takes the
values m + k - 2i on T_k).  Balls "from the other side" (overlap at most j) are balls around the
complement of c, so every ball around every binary centre is of this form.

For x in D with overlap i the nearest point of T_k outside D is at Hamming distance 2 (i - i0 + 1): one
swap changes the overlap by at most one, and lowering it by one is possible as long as the overlap is
above its minimum max(0, m + k - n).  Hence, with w_i = C(m, i) C(n - m, k - i) / C(n, k),

    density  q(m, i0) = sum_{i >= i0} w_i,
    effect   Phi(m, i0) = sum_{i >= i0} w_i (e^{2u(i - i0 + 1)} - 1),

and D is eps-sensitive iff ln(1 + Phi) > eps (definitions of THY-REQ-0010).  The script computes

    q*_ball(eps) = min { q(m, i0) : 0 <= m <= n, i0 > max(0, m + k - n), ln(1 + Phi(m, i0)) > eps }

in floating point in the log domain (``ball_optimum``) and, for small n, with exact integer weights and
a 60-digit comparison (``ball_optimum_exact``); the two must select the same ball.

    python experiments/eng/slices/ball_exponents.py --out experiments/eng/slices/results/ball_exponents.json
"""
from __future__ import annotations

import argparse
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.special import gammaln

NS = (20, 40, 60, 100, 200, 400, 1000, 2000, 4000, 10000)
KAPPAS = (0.5, 0.4, 0.3)
LIMITS = {0.5: 0.029139, 0.4: 0.028005, 0.3: 0.024588}        # THY-REQ-0010, question 2 (u = 1, eps = 1); theirs


def ball_optimum(n: int, k: int, u: float, eps: float) -> dict:
    """Smallest eps-sensitive ball of T_k over all centre types; floating point, log domain."""
    lf = gammaln(np.arange(n + 2, dtype=float) + 1.0)           # lf[j] = ln j!
    m = np.arange(n + 1)
    i_lo = np.maximum(0, m + k - n)
    i_hi = np.minimum(m, k)
    lcnk = lf[n] - lf[k] - lf[n - k]
    lS = np.full(n + 1, -np.inf)                                # ln sum_{i >= i0} w_i e^{2u(i - i0 + 1)}
    lQ = np.full(n + 1, -np.inf)                                # ln sum_{i >= i0} w_i
    best_lq = np.full(n + 1, np.inf)
    best_i0 = np.full(n + 1, -1)
    lthr = math.log(math.expm1(eps))
    for i in range(k, -1, -1):
        act = (i <= i_hi) & (i >= i_lo)
        if not act.any():
            continue
        ma = m[act]
        lw = (lf[ma] - lf[i] - lf[ma - i]) + (lf[n - ma] - lf[k - i] - lf[n - ma - k + i]) - lcnk
        lS[act] = 2 * u + np.logaddexp(lw, lS[act])
        lQ[act] = np.logaddexp(lQ[act], lw)
        # a proper subset: the ball must leave out the lowest overlap
        cand = act & (i > i_lo) & (best_i0 < 0)
        if cand.any():
            lphi = lS[cand] + np.log1p(-np.exp(lQ[cand] - lS[cand]))
            hit = lphi > lthr
            idx = np.flatnonzero(cand)[hit]
            best_i0[idx] = i
            best_lq[idx] = lQ[idx]
    mstar = int(np.argmin(best_lq))
    # the best centre inside the class and the best centre of the "natural" other types, for comparison
    return dict(n=n, k=k, u=u, eps=eps, lq=float(best_lq[mstar]), m=mstar, i0=int(best_i0[mstar]),
                radius=mstar + k - 2 * int(best_i0[mstar]), lq_centre_in_class=float(best_lq[k]), i0_centre_in_class=int(best_i0[k]),
                lq_centre_ones=float(best_lq[n]) if best_i0[n] >= 0 else None,
                lq_by_m=None)


def ball_optimum_exact(n: int, k: int, u: float, eps: float) -> dict:
    """The same optimum with exact integer weights; the comparison with e^eps - 1 in 60-digit arithmetic."""
    import mpmath as mp
    mp.mp.dps = 60
    cnk = math.comb(n, k)
    thr = (mp.e ** mp.mpf(eps) - 1) * cnk
    e2u = mp.e ** (2 * mp.mpf(u))
    best = None
    for m in range(n + 1):
        i_lo, i_hi = max(0, m + k - n), min(m, k)
        S = mp.mpf(0)
        Q = 0
        for i in range(i_hi, i_lo, -1):                          # i0 = i > i_lo
            w = math.comb(m, i) * math.comb(n - m, k - i)
            S = e2u * (w + S)
            Q += w
            if S - Q > thr:
                if best is None or Q < best[0]:
                    best = (Q, m, i)
                break
    Q, m, i0 = best
    return dict(n=n, k=k, q=Fraction(Q, cnk), lq=float(mp.log(mp.mpf(Q) / cnk)), m=m, i0=i0)


def validation_target() -> dict:
    """THY-REQ-0010: n = 8, k = 4, u = 1, the ball {d(x, c) < 4} around c in T_4 has 17 points and
    Phi = ((e^4 - 1) + 16 (e^2 - 1)) / 70."""
    n, k, m, i0, u = 8, 4, 4, 3, 1.0
    w = {i: math.comb(m, i) * math.comb(n - m, k - i) for i in range(i0, 5)}
    size = sum(w.values())
    phi = sum(w[i] * math.expm1(2 * u * (i - i0 + 1)) for i in w) / math.comb(n, k)
    return dict(size=size, phi=phi, phi_target=((math.e ** 4 - 1) + 16 * (math.e ** 2 - 1)) / 70, ok=size == 17)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--u", type=float, default=1.0)
    ap.add_argument("--eps", type=float, default=1.0)
    args = ap.parse_args()
    t0 = time.time()
    res = dict(u=args.u, eps=args.eps, validation=validation_target(), limits=LIMITS, rows=[], exact=[])
    assert res["validation"]["ok"] and abs(res["validation"]["phi"] - res["validation"]["phi_target"]) < 1e-12
    for kappa in KAPPAS:
        for n in NS:
            k = round(kappa * n)
            assert abs(k - kappa * n) < 1e-9
            r = ball_optimum(n, k, args.u, args.eps)
            r.pop("lq_by_m")
            r.update(kappa=kappa, exponent=-r["lq"] / n)
            res["rows"].append(r)
            print(f"kappa={kappa} n={n}: -ln q*/n = {r['exponent']:.6f}  centre type m/n = {r['m'] / n:.4f}  radius/n = {r['radius'] / n:.4f}"
                  f"  centre in class: {-r['lq_centre_in_class'] / n:.6f}", flush=True)
            if n <= 400:
                e = ball_optimum_exact(n, k, args.u, args.eps)
                same = (e["m"], e["i0"]) == (r["m"], r["i0"]) or abs(e["lq"] - r["lq"]) < 1e-9
                res["exact"].append(dict(kappa=kappa, n=n, m=e["m"], i0=e["i0"], lq=e["lq"], q_num=str(e["q"].numerator), q_den=str(e["q"].denominator),
                                         float_agrees=bool(same), lq_difference=abs(e["lq"] - r["lq"])))
                assert same, (kappa, n, e, r)
    res["seconds"] = time.time() - t0
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
