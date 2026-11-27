"""Review of ENG-RES-0016 §3 (item 3 of the brief): the lower bound by weighted dips.

(a) The dip f_c(x) = -(rho - d_u(x, c))_+ on explicit small cubes: membership in the class, the set where it differs from
    0 (the OPEN ball), the factor 1 + Exc(rho), translation invariance, and the double count behind the bound (every
    point lies in exactly |D_rho| of the 2^n dips).
(b) ``hetero.hinted_lower_bound`` against an independent evaluation with exact distances (Fractions: ties between
    weighted distances are exact) and 50-digit arithmetic for the excess, on tie-rich and generic blocks, for
    accuracies from 1e-6 to 20; and against a scan over all points of explicit small cubes.
(c) Is "the smallest admissible dip" the best bound of this kind?  Dips of the semi-metric of a SUB-block (sites outside
    it ignored) are members of the class as well and the same argument applies; the bound of a sub-block is compared
    with the bound of the whole block.

    python experiments/eng/review_x014/check_lower_bound.py          # writes check_lower_bound.json   (about 12 minutes)
"""
from __future__ import annotations

import itertools
import json
import math
import sys
import time
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import hetero as H  # noqa: E402

mp.mp.dps = 50
LN2 = math.log(2.0)


# ---------------------------------------------------------------------------------------------
# (a) the dip on explicit cubes
# ---------------------------------------------------------------------------------------------
def dip_checks(rng, trials: int) -> dict:
    out = dict(trials=0, class_violations=0, support_errors=0, excess_errors=0, translation_errors=0, double_count_errors=0, max_excess_rel_err=0.0)
    for _ in range(trials):
        n = int(rng.integers(2, 9))
        us = rng.choice([0.25, 0.5, 1.0, 1.5, 2.0, 0.37, 1.93, 3.0], size=n)
        X = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
        idx = np.arange(2 ** n)
        d0 = X @ us
        dvals = np.unique(np.round(d0, 12))
        # radii: between distance values, AT distance values (the open/closed question), and beyond the diameter
        rhos = list(rng.uniform(0, d0.max() * 1.2, size=3)) + list(rng.choice(dvals[1:], size=min(3, len(dvals) - 1)))
        for rho in rhos:
            out["trials"] += 1
            c = int(rng.integers(2 ** n))
            dc = np.abs(X - X[c][None, :]) @ us
            f = -np.maximum(rho - dc, 0.0)
            # class: |f(x) - f(x + e_i)| <= u_i
            viol = max(float(np.max(np.abs(f - f[idx ^ (1 << i)])) - us[i]) for i in range(n))
            out["class_violations"] += viol > 1e-12
            # support: f != 0 exactly on the open ball {d < rho} (ties resolved with a tolerance far below the gaps)
            open_ball = dc < rho - 1e-12
            out["support_errors"] += not np.array_equal(f < -1e-12, open_ball)
            # factor 1 + Exc(rho), Exc computed from the distances FROM THE ORIGIN (translation invariance of d_u)
            exc0 = float(np.sum(np.expm1(np.maximum(rho - d0, 0.0))) / 2 ** n)
            A = float(np.mean(np.exp(-f)))
            rel = abs(A - (1 + exc0)) / (1 + exc0)
            out["max_excess_rel_err"] = max(out["max_excess_rel_err"], rel)
            out["excess_errors"] += rel > 1e-12
            # translation: f_c(x) = f_0(x xor c)
            f0 = -np.maximum(rho - d0, 0.0)
            out["translation_errors"] += not np.allclose(f, f0[idx ^ c], atol=1e-12)
            # double count: x in D(c) iff c in D(x); so every x lies in exactly |D| of the 2^n dips
            if n <= 6:
                D = (np.abs(X[:, None, :] - X[None, :, :]) @ us) < rho - 1e-12            # D[c, x]
                out["double_count_errors"] += not (np.array_equal(D, D.T) and len(set(D.sum(axis=0).tolist())) == 1)
    return out


# ---------------------------------------------------------------------------------------------
# (b) the smallest admissible dip, independently
# ---------------------------------------------------------------------------------------------
def exact_shells(block):
    """{distance (Fraction): number of points} of the weighted distance from a point; block = [(Fraction u, n), ...]."""
    cnt = {Fraction(0): 1}
    for u, n in block:
        new = defaultdict(int)
        for d, c in cnt.items():
            for j in range(n + 1):
                new[d + j * u] += c * math.comb(n, j)
        cnt = new
    return cnt


def independent_lower_bound(block, eps, delta):
    """ln[(1 - 2 delta) 2^n / |D|], D the smallest open ball {d_u < rho} with Exc(rho) > e^eps - 1 for some rho; plus the
    relative distance of the deciding comparison from equality (a near-tie in the THRESHOLD, not in the distances)."""
    cnt = exact_shells(block)
    n = sum(k for _, k in block)
    ds = sorted(cnt)
    target = mp.expm1(mp.mpf(eps)) * mp.mpf(2) ** n
    ball = 0
    S = mp.mpf(0)
    margin = None
    for k, d in enumerate(ds):
        ball += cnt[d]
        S += cnt[d] * mp.exp(-(mp.mpf(d.numerator) / d.denominator))
        if k + 1 == len(ds):
            return float(mp.log(1 - 2 * delta) + n * mp.log(2) - mp.log(ball)), margin, ball
        nxt = ds[k + 1]
        sup = mp.exp(mp.mpf(nxt.numerator) / nxt.denominator) * S - ball       # 2^n * sup of Exc over rho in (d_k, d_{k+1}]
        m = abs(sup / target - 1)
        margin = m if margin is None else min(margin, m)
        if sup > target:
            return float(mp.log(1 - 2 * delta) + n * mp.log(2) - mp.log(ball)), float(margin), ball


def scan_lower_bound(us, eps, delta):
    """All points of an explicit cube: for every candidate radius (each distance value and just above it) the dip and its excess."""
    n = len(us)
    d = np.array([sum(u for u, bit in zip(us, bits) if bit) for bits in itertools.product((0, 1), repeat=n)], dtype=object)   # Fractions
    vals = sorted(set(d.tolist()))
    df = np.array([float(v) for v in d])
    best = None
    for k, v in enumerate(vals):
        nxt = float(vals[k + 1]) if k + 1 < len(vals) else float(v) + 50.0
        inside = np.array([x <= v for x in d])                    # = open ball of every rho in (v, next value]
        exc_sup = float(np.sum(np.expm1(nxt - df[inside])) / 2 ** n)
        if exc_sup > math.expm1(eps):
            best = int(inside.sum())
            break
    return math.log(1 - 2 * delta) + n * LN2 - math.log(best)


def compare(rng, cases: int) -> dict:
    out = dict(cases=0, max_abs_diff=0.0, mismatches=[], near_threshold_cases=0, scan_cases=0, scan_max_abs_diff=0.0, scan_mismatches=[])
    slope_sets = [  # tie-rich (commensurable) and generic
        [Fraction(1), Fraction(1, 2)], [Fraction(3, 10), Fraction(1, 10)], [Fraction(2, 3), Fraction(1, 3)], [Fraction(3, 2), Fraction(1, 2), Fraction(1, 4)],
        [Fraction(2), Fraction(1, 2)], [Fraction(4), Fraction(1)], [Fraction(4), Fraction(1, 4)], [Fraction(13, 10), Fraction(2, 5)],
        [Fraction(7, 10), Fraction(3, 10), Fraction(1, 10)], [Fraction(1), Fraction(1, 3), Fraction(1, 7)], [Fraction(1234567, 1000000), Fraction(765432, 1000000)],
        [Fraction(5, 2)], [Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5)]]
    eps_list = [1e-6, 1e-3, 0.05, 0.5, 0.8715, 2.0, 5.0, 20.0]
    for c in range(cases):
        slopes = slope_sets[c % len(slope_sets)]
        big = (c // len(slope_sets)) % 3
        hi = (5, 40, 300)[big]
        block = [(u, int(rng.integers(1, hi))) for u in slopes]
        # ``hetero.weighted_shells`` enumerates prod (n_t + 1) shells whatever the slopes: keep that product small.  (The first
        # version of this script did not, called it on four types of up to 300 sites — 8e9 shells — and exhausted the machine.)
        while math.prod(k + 1 for _, k in block) > 2_000_000:
            block = [(u, max(1, k // 2)) for u, k in block]
        eps = eps_list[int(rng.integers(len(eps_list)))]
        B = H.make_block([(float(u), k) for u, k in block])
        try:
            mine, margin, ball = independent_lower_bound(block, eps, 0.05)
        except Exception as e:                                        # pragma: no cover
            out["mismatches"].append(dict(block=str(block), eps=eps, error=repr(e)))
            continue
        theirs = H.hinted_lower_bound(B, eps, 0.05)["lbound"]
        out["cases"] += 1
        diff = abs(mine - theirs)
        near = margin is not None and margin < 1e-9
        out["near_threshold_cases"] += bool(near)
        if diff > 1e-8 * max(1.0, abs(mine)) and not near:
            out["mismatches"].append(dict(block=[(str(u), k) for u, k in block], eps=eps, mine=mine, theirs=theirs, margin=margin))
        out["max_abs_diff"] = max(out["max_abs_diff"], diff if not near else 0.0)
        if sum(k for _, k in block) <= 13:
            us = [u for u, k in block for _ in range(k)]
            sc = scan_lower_bound(us, eps, 0.05)
            out["scan_cases"] += 1
            d2 = abs(sc - theirs)
            out["scan_max_abs_diff"] = max(out["scan_max_abs_diff"], d2)
            if d2 > 1e-9:
                out["scan_mismatches"].append(dict(block=[(str(u), k) for u, k in block], eps=eps, scan=sc, theirs=theirs))
    return out


# ---------------------------------------------------------------------------------------------
# (c) sub-blocks
# ---------------------------------------------------------------------------------------------
def sub_block_scan() -> dict:
    """For blocks of two types: the bound of the block against the bounds of its sub-blocks (dips that ignore some sites)."""
    out = dict(cells=[], any_sub_block_better=False, largest_gain_nats=0.0)
    eps, delta = 0.8715, 0.05
    for (uH, uL) in ((2.0, 0.5), (1.0, 0.5), (2.0, 1.0), (4.0, 1.0), (4.0, 0.25)):
        for frac in (0.1, 0.25, 0.5, 0.75, 0.9):
            for n in (40, 200, 1000):
                nH = int(round(frac * n))
                nL = n - nH
                full = H.hinted_lower_bound(H.make_block([(uH, nH), (uL, nL)]), eps, delta)["lbound"]
                best, arg = full, (nH, nL)
                cands = {(nH, 0), (0, nL)} | {(nH, nL - j) for j in range(1, min(nL, 12) + 1)} | {(nH - j, nL) for j in range(1, min(nH, 12) + 1)}
                if n <= 40:
                    cands |= {(a, b) for a in range(nH + 1) for b in range(nL + 1)}
                for a, b in cands:
                    if a + b == 0 or (a, b) == (nH, nL):
                        continue
                    v = H.hinted_lower_bound(H.make_block([(uH, a), (uL, b)]), eps, delta)["lbound"]
                    if v > best + 1e-9:
                        best, arg = v, (a, b)
                gain = best - full
                out["cells"].append(dict(uH=uH, uL=uL, n=n, nH=nH, nL=nL, lbound=full, best_sub_block=list(arg), best_sub_block_lbound=best, gain_nats=gain))
                out["any_sub_block_better"] |= gain > 1e-9
                out["largest_gain_nats"] = max(out["largest_gain_nats"], gain)
    return out


# ---------------------------------------------------------------------------------------------
# (d) what the argument gives at best, on a four-site cube
# ---------------------------------------------------------------------------------------------
def exact_small() -> dict:
    """The argument of §3 works for ANY member g of the class that vanishes outside a set D (its translates differ from 0
    on the translates of D, and every point lies in |D| of them): the bound is (1 - 2 delta) 2^n/|D| as soon as
    2^-n sum_D (e^{-g} - 1) > e^eps - 1, and the largest such sum for a given D is Phi(D) = 2^-n sum_{x in D} (e^{dist_u(x, D^c)} - 1).
    So the best bound of this kind is given by the smallest set D with Phi(D) > e^eps - 1 — the weighted cube's exact upper
    tail function — and "the smallest admissible dip" of the message is the smallest weighted BALL with the cone on it.
    On Q_4 all 65 534 proper subsets can be enumerated: three numbers per accuracy,
        balls_cone     the message's rule (``hetero.hinted_lower_bound``),
        balls_extremal the same balls with the largest member of the class on them,
        all_sets       the exact optimum of the argument."""
    out = dict(patterns=[])
    n, P = 4, 16
    idx = np.arange(P)
    masks = np.arange(1, 2 ** P - 1, dtype=np.int64)
    member = ((masks[:, None] >> idx[None, :]) & 1).astype(bool)
    size = member.sum(axis=1)
    X = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
    eps_grid = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8715, 1.0, 1.5, 2.0, 3.0]
    for us in ([1.0, 1.0, 1.0, 1.0], [1.7, 1.7, 0.4, 0.4], [2.0, 0.5, 0.5, 0.5], [1.0, 1.0, 0.3, 0.3], [3.0, 1.0, 0.3, 0.1], [2.0, 2.0, 2.0, 0.5], [4.0, 0.25, 0.25, 0.25]):
        us = np.array(us)
        v = np.where(member, 1e6, 0.0)
        for i, u in enumerate(us):
            v = np.minimum(v, v[:, idx ^ (1 << i)] + u)
        phi = np.expm1(v).sum(axis=1) / P                                  # Phi(D) for every proper subset
        best_by_size = np.array([phi[size == N].max() for N in range(1, P)])   # exact extremal function at every cardinality
        d0 = X @ us
        vals = np.unique(np.round(d0, 12))
        balls = []                                                        # (|ball|, sup of the cone's excess, Phi(ball)) for the balls around 0
        for k, dv in enumerate(vals[:-1]):
            inside = d0 <= dv + 1e-12
            mask = int(np.sum(inside.astype(np.int64) << idx))
            balls.append((int(inside.sum()), float(np.sum(np.expm1(vals[k + 1] - d0[inside])) / P), float(phi[mask - 1])))
        rows = []
        for eps in eps_grid:
            t = math.expm1(eps)
            cone = min((N for N, e, _ in balls if e > t), default=P)
            ext = min((N for N, _, f in balls if f > t), default=P)
            alls = min((N for N in range(1, P) if best_by_size[N - 1] > t), default=P)
            theirs = H.hinted_lower_bound(H.make_block([(float(u), 1) for u in us]), eps, 0.05)["ldip"]
            rows.append(dict(eps=eps, balls_cone=cone, balls_extremal=ext, all_sets=alls, module_dip=round(math.exp(theirs))))
        out["patterns"].append(dict(slopes=us.tolist(), rows=rows,
                                    module_agrees_with_balls_cone=all(r["balls_cone"] == r["module_dip"] for r in rows),
                                    accuracies_where_a_smaller_set_exists=[r["eps"] for r in rows if r["all_sets"] < r["balls_cone"]],
                                    largest_gain_factor=max(r["balls_cone"] / r["all_sets"] for r in rows)))
    out["any_improvement"] = any(p_["accuracies_where_a_smaller_set_exists"] for p_ in out["patterns"])
    return out


def main() -> int:
    sys.path.insert(0, str(HERE))
    from review_sim import limit_memory

    limit_memory(2.5)
    t0 = time.time()
    rng = np.random.default_rng(314159)
    res = dict(dip=dip_checks(rng, 400), compare=compare(rng, 234), sub_blocks=sub_block_scan(), exact_small=exact_small())
    res["seconds"] = time.time() - t0
    (HERE / "check_lower_bound.json").write_text(json.dumps(res, indent=1, default=float))
    print("dip:", res["dip"])
    c = res["compare"]
    print(f"compare: {c['cases']} cases, max |diff| {c['max_abs_diff']:.2e}, {len(c['mismatches'])} mismatches, {c['near_threshold_cases']} near-threshold; "
          f"scan: {c['scan_cases']} cases, max |diff| {c['scan_max_abs_diff']:.2e}, {len(c['scan_mismatches'])} mismatches")
    for m in c["mismatches"][:8] + c["scan_mismatches"][:8]:
        print("   ", m)
    s = res["sub_blocks"]
    print(f"sub-blocks: any better {s['any_sub_block_better']}, largest gain {s['largest_gain_nats']:.4f} nats")
    for cell in s["cells"]:
        if cell["gain_nats"] > 1e-9:
            print("   ", cell)
    for p_ in res["exact_small"]["patterns"]:
        print("Q_4, slopes", p_["slopes"], ": module = smallest ball with the cone:", p_["module_agrees_with_balls_cone"], "; a smaller admissible set exists at eps =",
              p_["accuracies_where_a_smaller_set_exists"], "; largest factor", p_["largest_gain_factor"])
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
