#!/usr/bin/env python3
"""R15, Item 4 -- Corollary 11.114(c), (d) of the theory report at f7df44f: a numerical companion to the READING of the
Lean theorem `ratio_expected_queries_ge_mixed` (nothing is compiled here, and this is no substitute for the kernel).

On random boxes with two disjoint macrostates A, B (weights pi, floor lo, ceiling hi, instance r):
 (1) the four alternatives of the theorem: a set D that avoids the other macrostate and whose dip (bump) weight inside
     M exceeds (e^eps - 1) W_M(r) (resp. (1 - e^-eps) W_M(r)) changes the log-ratio by more than eps when lowered to
     the floor (raised to the ceiling) -- also when D contains points outside both macrostates, and also when A and B
     overlap (the Lean statement assumes neither D inside M nor A, B disjoint);
 (2) greedy packings: if no single state of M has that much dip (bump) weight, the number of pairwise disjoint heavy
     sets inside M is at least floor(a_M / (2 (e^eps - 1))) for dips, floor(b_M / (2 (1 - e^-eps))) for bumps,
     a_M = W_M(lo)/W_M - 1, b_M = 1 - W_M(hi)/W_M; dip sets and bump sets of one macrostate share its states, sets of
     different macrostates do not: the theorem counts k_A + k_B with k_M >= max(dips, bumps);
 (3) the two-sided bound for eps <= 1 used in the report of this workstream:
        (1 - 2 delta) (max_M (a_M + b_M)/(6.9 eps) - 1)  <=  (1 - 2 delta)(k_A + k_B)
        N := ceil( ln(1/delta) / min(1, (1/4) min_M min((e^{eps/2} - 1)/a_M, (1 - e^{-eps/2})/b_M)) )
           <=  10.7 ln(1/delta) max_M (a_M + b_M)/eps + 1 + ln(1/delta)
     (N is the sample size of Corollary 11.114(b)); and lower <= N.

Run:  OMP_NUM_THREADS=1 python3 r15_item4_packing.py > logs/item4_packing.log
"""
import math, resource, time
import numpy as np

t0 = time.time()
ok_all = True


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


def W(pi, r, mask):
    return float((pi[mask] * np.exp(-r[mask])).sum())


def greedy(weights, thr):
    """number of disjoint sets, each of total weight > thr, by filling in decreasing order; and the sets"""
    order = np.argsort(-weights)
    sets, cur, tot = [], [], 0.0
    for i in order:
        if weights[i] <= 0:
            break
        cur.append(int(i)); tot += float(weights[i])
        if tot > thr:
            sets.append(cur); cur, tot = [], 0.0
    return sets


rng = np.random.default_rng(404)
stats = dict(boxes=0, alts=0, packs=0, overlap_alts=0, min_slack_low=math.inf, max_ratio_up=0.0, sum_gt_max=0)
for trial in range(400):
    n = int(rng.integers(200, 1200))
    pi = rng.dirichlet(np.ones(n) * float(rng.choice([0.3, 1.0, 5.0])))
    lab = rng.choice(3, size=n, p=[0.4, 0.4, 0.2])          # 0: A, 1: B, 2: neither
    A, B, O = lab == 0, lab == 1, lab == 2
    depth = float(rng.choice([0.3, 1.0, 3.0, 6.0])); height = float(rng.choice([0.3, 1.0, 3.0]))
    lo = -depth * rng.random(n); hi = height * rng.random(n)
    kind = trial % 4
    if kind == 0:
        r = lo + (hi - lo) * rng.random(n)
    elif kind == 1:
        r = lo.copy(); r[B] = (lo + (hi - lo) * rng.random(n))[B]      # A at its floor
    elif kind == 2:
        r = hi.copy(); r[A] = (lo + (hi - lo) * rng.random(n))[A]      # B at its ceiling
    else:
        r = np.zeros(n)
    eps = float(rng.choice([0.05, 0.2, 0.5, 1.0])); delta = float(rng.choice([0.05, 0.2]))
    logratio = lambda rr: math.log(W(pi, rr, A)) - math.log(W(pi, rr, B))
    L0 = logratio(r)
    ks = {}
    ab = {}
    heavy_single = False
    for M, name in ((A, "A"), (B, "B")):
        WM = W(pi, r, M)
        dip = np.where(M, pi * (np.exp(-lo) - np.exp(-r)), 0.0)
        bump = np.where(M, pi * (np.exp(-r) - np.exp(-hi)), 0.0)
        aM, bM = float(dip.sum()) / WM, float(bump.sum()) / WM
        check(abs(aM - (W(pi, lo, M) / WM - 1)) < 1e-9 and abs(bM - (1 - W(pi, hi, M) / WM)) < 1e-9, "a_M, b_M")
        ab[name] = (aM, bM)
        td, tb = math.expm1(eps) * WM, -math.expm1(-eps) * WM
        if dip.max() > td or bump.max() > tb:
            heavy_single = True
        sd, sb = greedy(dip, td), greedy(bump, tb)
        # (1) every packed set changes the log-ratio by more than eps; add some points outside both macrostates to it
        extra = np.flatnonzero(O)[:3].tolist()
        for D in sd[:5]:
            alt = r.copy(); idx = D + extra; alt[idx] = lo[idx]
            check(abs(logratio(alt) - L0) > eps, "a heavy dip set does not change the log-ratio by more than eps")
            stats["alts"] += 1
        for D in sb[:5]:
            alt = r.copy(); idx = D + extra; alt[idx] = hi[idx]
            check(abs(logratio(alt) - L0) > eps, "a heavy bump set does not change the log-ratio by more than eps")
            stats["alts"] += 1
        # (2) the floors
        if dip.max() <= td:
            check(len(sd) >= math.floor(aM / (2 * math.expm1(eps))), f"dip packing below the floor ({len(sd)})")
        if bump.max() <= tb:
            check(len(sb) >= math.floor(bM / (2 * -math.expm1(-eps))), "bump packing below the floor")
        ks[name] = max(len(sd), len(sb))
        stats["packs"] += 1
    # overlapping macrostates: a set that avoids B and is heavy inside A (weights restricted to A)
    A2 = A | (rng.random(n) < 0.05) & B                       # A2 overlaps B
    WA2 = W(pi, r, A2)
    dipA2 = np.where(A2 & ~B, pi * (np.exp(-lo) - np.exp(-r)), 0.0)        # only points of A2 outside B may be used
    for D in greedy(dipA2, math.expm1(eps) * WA2)[:3]:
        alt = r.copy(); alt[D] = lo[D]
        lr2 = lambda rr: math.log(W(pi, rr, A2)) - math.log(W(pi, rr, B))
        check(lr2(alt) - lr2(r) > eps, "overlapping macrostates: heavy dip set avoiding B")
        stats["overlap_alts"] += 1
    stats["boxes"] += 1
    if heavy_single or eps > 1:
        continue
    # (3) the two-sided bound
    mx = max(ab["A"][0] + ab["A"][1], ab["B"][0] + ab["B"][1])
    lower_closed = (1 - 2 * delta) * (mx / (6.9 * eps) - 1)
    lower = (1 - 2 * delta) * (ks["A"] + ks["B"])
    terms = []
    for name in ("A", "B"):
        aM, bM = ab[name]
        if aM > 0:
            terms.append(math.expm1(eps / 2) / aM)
        if bM > 0:
            terms.append(-math.expm1(-eps / 2) / bM)
    p = min(1.0, 0.25 * min(terms))
    N = math.ceil(math.log(1 / delta) / p)
    upper_closed = 10.7 * math.log(1 / delta) * mx / eps + 1 + math.log(1 / delta)
    check(lower_closed <= lower + 1e-9, f"closed-form lower bound above the packing bound: {lower_closed} > {lower}")
    check(N <= upper_closed + 1e-9, f"sample size above the closed-form upper bound: {N} > {upper_closed}")
    check(lower <= N + 1e-9, "lower bound above the upper bound")
    stats["min_slack_low"] = min(stats["min_slack_low"], lower - lower_closed)
    stats["max_ratio_up"] = max(stats["max_ratio_up"], N / upper_closed)
    stats["sum_gt_max"] += int(min(ks["A"], ks["B"]) > 0)
print(f"{stats['boxes']} random boxes (200 to 1200 states; macrostates A, B and a rest; instances generic, at the floor of A, at the ceiling of B, at r = 0):")
print(f"   (1) {stats['alts']} heavy sets (dips and bumps, in either macrostate, each with three points outside both macrostates added): the log-ratio always"
      f" changes by more than eps; {stats['overlap_alts']} sets with OVERLAPPING macrostates (set avoiding B, weight restricted to A): the same")
print(f"   (2) {stats['packs']} greedy packings: never below floor(a_M/(2(e^eps - 1))), floor(b_M/(2(1 - e^-eps))) where no single state is heavy")
print(f"   (3) two-sided bound for eps <= 1: closed-form lower bound <= (1 - 2 delta)(k_A + k_B) <= N <= closed-form upper bound in every box without a heavy"
      f" single state; least slack of the lower bound {stats['min_slack_low']:.2f}; largest N/upper {stats['max_ratio_up']:.3f};"
      f" boxes in which BOTH macrostates contribute sets (the sum exceeds the max): {stats['sum_gt_max']}")
print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
