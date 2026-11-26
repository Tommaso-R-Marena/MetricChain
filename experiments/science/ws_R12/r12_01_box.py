#!/usr/bin/env python3
"""R12 item 1 — replication of the corrected Theorem 11.110(c)-(e) (box classes), written from the
statement in docs/THEORY_REPORT.md (export of the theory branch at 9408e33) and from the Lean
statements in proofs/Frontiers/BoxClass.lean, BEFORE the theory division's harness was opened.

Setting.  X finite, pi a probability vector, lo <= r <= hi pointwise.  z = sum pi e^{-r} (= Z(r)/Z0),
dip(x) = pi(x)(e^{-lo} - e^{-r}), bump(x) = pi(x)(e^{-r} - e^{-hi}), U = sum dip, V = sum bump,
a = U/z = Z(lo)/Z - 1, b = V/z = 1 - Z(hi)/Z.

A set D is *dip-heavy at level e* if dip(D) > (e^e - 1) z, *bump-heavy* if bump(D) > (1 - e^{-e}) z.
The members of the box whose ln Z differs from that of r by more than e differ from r on exactly
the supersets of heavy sets (lowering all of D to the floor / raising all of D to the ceiling is
the extreme change supported on D).  So everything is a statement about the family of heavy sets:

  k_dip, k_bump, k_mix   exact packing numbers (max number of pairwise disjoint heavy sets), by a
                         dynamic programme over all subsets (exhaustive, no heuristic);
  tau*(e)                fractional hitting = fractional packing number of the heavy sets (an LP);
                         (1 - 2 delta) tau*(e) is a valid lower bound on the cost (the generic
                         packing lemma with fractional weights), and ceil(ln(1/delta) tau*(e/2)) is
                         the cost of the best possible spot check;
  p_exact(eta)           min over heavy sets at level eta of q(D): the exact detection probability
                         of a sampler q; (1 - p_exact)^N is the exact worst-case failure probability
                         of the spot check with N samples.

One command, no arguments:  python3 r12_01_box.py
"""
import math
import sys
import time

import numpy as np
from scipy.optimize import linprog

T0 = time.time()
rng = np.random.default_rng(20261126)


def subset_sums(v):
    """s[S] = sum of v over the bits of S, for all 2^n subsets."""
    n = len(v)
    s = np.zeros(1 << n)
    for i in range(n):
        s[1 << i:1 << (i + 1)] = s[0:1 << i] + v[i]
    return s


def packing_number(heavy):
    """Exact maximum number of pairwise disjoint subsets T with heavy[T] True (heavy is a boolean
    array over all 2^n subsets).  f[S] = best packing inside S; either the lowest element of S is
    unused, or it lies in a heavy set T subset of S."""
    size = len(heavy)
    f = np.zeros(size, dtype=np.int32)
    for S in range(1, size):
        low = S & (-S)
        rest = S ^ low
        best = f[rest]
        # enumerate T = low | sub, sub a subset of rest
        sub = rest
        while True:
            T = sub | low
            if heavy[T]:
                c = 1 + f[S ^ T]
                if c > best:
                    best = c
            if sub == 0:
                break
            sub = (sub - 1) & rest
        f[S] = best
    return int(f[size - 1])


def frac_hitting(heavy, n):
    """min sum m_x  s.t.  sum_{x in D} m_x >= 1 for every heavy D, m >= 0  (0 if no heavy set).
    Only minimal heavy sets are needed; we keep every heavy set none of whose one-point deletions
    is heavy."""
    idx = np.nonzero(heavy)[0]
    if len(idx) == 0:
        return 0.0
    rows = []
    for D in idx:
        minimal = True
        for i in range(n):
            if D >> i & 1 and heavy[D ^ (1 << i)]:
                minimal = False
                break
        if minimal:
            rows.append([-(D >> i & 1) for i in range(n)])
    A = np.array(rows, dtype=float)
    res = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(rows)), bounds=[(0, None)] * n, method="highs")
    assert res.status == 0, res.message
    return float(res.fun)


def analyse(pi, lo, hi, r, eps, delta, label, verbose=False):
    n = len(pi)
    z = float(np.sum(pi * np.exp(-r)))
    dip = pi * (np.exp(-lo) - np.exp(-r))
    bump = pi * (np.exp(-r) - np.exp(-hi))
    dip = np.maximum(dip, 0.0)
    bump = np.maximum(bump, 0.0)
    U, V = float(dip.sum()), float(bump.sum())
    a, b = U / z, V / z
    sd, sb = subset_sums(dip), subset_sums(bump)

    def heavy_at(e):
        return (sd > (math.exp(e) - 1) * z), (sb > (1 - math.exp(-e)) * z)

    hd, hb = heavy_at(eps)
    hm = hd | hb
    single = bool(np.any(dip >= (math.exp(eps) - 1) * z) or np.any(bump >= (1 - math.exp(-eps)) * z))
    k_dip, k_bump, k_mix = packing_number(hd), packing_number(hb), packing_number(hm)
    fl_dip = math.floor(a / (2 * (math.exp(eps) - 1)))
    fl_bump = math.floor(b / (2 * (1 - math.exp(-eps))))
    tau = frac_hitting(hm, n)
    hd2, hb2 = heavy_at(eps / 2)
    hm2 = hd2 | hb2
    tau2 = frac_hitting(hm2, n)
    eta = eps / 2
    A_ = a / (math.exp(eta) - 1)
    B_ = b / (1 - math.exp(-eta))
    out = dict(label=label, n=n, eps=eps, delta=delta, a=a, b=b, single=single, k_dip=k_dip,
               k_bump=k_bump, k_mix=k_mix, fl_dip=fl_dip, fl_bump=fl_bump, tau=tau, tau2=tau2,
               U=U, V=V)
    L = math.log(1 / delta)
    out["lower_k"] = (1 - 2 * delta) * k_mix
    out["lower_tau"] = (1 - 2 * delta) * tau
    out["upper_e"] = 4 * L * (math.exp(eps / 2) + 1) * (k_mix + 1) + 1
    out["upper_e_dips_only"] = 4 * L * (math.exp(eps / 2) + 1) * (k_dip + 1) + 1
    out["best_spot"] = math.ceil(L * max(1.0, tau2) - 1e-12)
    if U > 0 and V > 0:
        q = 0.5 * dip / U + 0.5 * bump / V
        sq = subset_sums(q)
        p_formula = min(1.0, 0.5 * min((math.exp(eta) - 1) / a, (1 - math.exp(-eta)) / b))
        N = math.ceil(L / p_formula - 1e-12)
        p_exact = float(sq[hm2].min()) if hm2.any() else 1.0
        out.update(N=N, p_formula=p_formula, p_exact=min(1.0, p_exact),
                   fail_exact=(1 - min(1.0, p_exact)) ** N if hm2.any() else 0.0)
        # the optimised mixture (my observation): lambda proportional to A_, 1-lambda to B_
        lam = A_ / (A_ + B_)
        qo = lam * dip / U + (1 - lam) * bump / V
        sqo = subset_sums(qo)
        p_opt_formula = min(1.0, 1.0 / (A_ + B_))
        N_opt = math.ceil(L / p_opt_formula - 1e-12)
        p_opt_exact = float(sqo[hm2].min()) if hm2.any() else 1.0
        out.update(N_opt=N_opt, p_opt_formula=p_opt_formula, p_opt_exact=min(1.0, p_opt_exact),
                   fail_opt_exact=(1 - min(1.0, p_opt_exact)) ** N_opt if hm2.any() else 0.0)
        # proportionality test
        prop = np.allclose(bump * U, dip * V, rtol=1e-12, atol=1e-15)
        out["proportional"] = bool(prop)
        if prop:
            p_prop = min(1.0, min((math.exp(eta) - 1) / a, (1 - math.exp(-eta)) / b))
            out["p_prop"] = p_prop
            out["N_prop"] = math.ceil(L / p_prop - 1e-12)
            out["fail_prop_exact"] = (1 - min(1.0, p_exact)) ** out["N_prop"] if hm2.any() else 0.0
    else:
        out.update(N=None)
    return out


def check(o, viol):
    """The chain of statements.  Returns nothing; appends violations."""
    tol = 1e-9
    # (i) packing <= fractional packing; mixed >= max, <= sum
    if o["k_mix"] > o["tau"] + 1e-6:
        viol.append(("k_mix > tau*", o))
    if not (max(o["k_dip"], o["k_bump"]) <= o["k_mix"] <= o["k_dip"] + o["k_bump"]):
        viol.append(("k_mix outside [max, sum]", o))
    # (ii) greedy floor under the single-state condition
    if not o["single"]:
        if o["k_dip"] < o["fl_dip"] or o["k_bump"] < o["fl_bump"]:
            viol.append(("greedy floor fails under the single-state condition", o))
    # (iii) the spot check of (c)
    if o["N"] is not None:
        if o["p_exact"] < o["p_formula"] - tol:
            viol.append(("detect_ge violated", o))
        if o["fail_exact"] > o["delta"] + tol:
            viol.append(("spot check failure > delta", o))
        if o["p_opt_exact"] < o["p_opt_formula"] - tol:
            viol.append(("optimised mixture: detection below 1/(A+B)", o))
        if o["fail_opt_exact"] > o["delta"] + tol:
            viol.append(("optimised mixture: failure > delta", o))
        if o["N_opt"] > o["N"]:
            viol.append(("optimised mixture needs more samples than the 1/2-1/2 one", o))
        if o["best_spot"] > o["N_opt"]:
            viol.append(("LP-optimal spot check worse than a concrete one", o))
        if o.get("proportional"):
            if o["p_exact"] < o["p_prop"] - tol:
                viol.append(("detect_ge_of_proportional violated", o))
            if o["fail_prop_exact"] > o["delta"] + tol:
                viol.append(("proportional spot check failure > delta", o))
        # (iv) part (e): N <= 4 ln(1/delta)(e^{eps/2}+1)(k+1)+1 under the single-state condition
        if not o["single"] and o["N"] > o["upper_e"] + tol:
            viol.append(("(e) upper end fails under the single-state condition", o))
    # (v) lower bounds do not exceed the trivial cost n nor the spot-check cost
    if o["lower_tau"] > o["n"] + tol:
        viol.append(("lower bound exceeds the number of states", o))
    if o["N"] is not None and o["lower_tau"] > o["N"] + tol:
        viol.append(("lower bound exceeds the spot check", o))


def fmt(o):
    s = (f"{o['label']:<28s} n={o['n']:>2d} eps={o['eps']:<5g} a={o['a']:<9.4g} b={o['b']:<8.4g} "
         f"single={int(o['single'])} k_dip={o['k_dip']} (floor {o['fl_dip']}) k_bump={o['k_bump']} "
         f"(floor {o['fl_bump']}) k_mix={o['k_mix']} tau*={o['tau']:.3f} tau*(e/2)={o['tau2']:.3f}")
    if o["N"] is not None:
        s += (f" | N={o['N']} N_opt={o['N_opt']} best_spot={o['best_spot']} p={o['p_formula']:.4g} "
              f"p_exact={o['p_exact']:.4g} fail={o['fail_exact']:.3g}")
    s += f" | (1-2d)k={o['lower_k']:.2f} (1-2d)tau={o['lower_tau']:.2f} upper(e)={o['upper_e']:.1f}"
    return s


print("=" * 110)
print("PART A — random boxes, exhaustive packings (n = 6, 8, 10; 4 placements of r; 6 values of eps)")
print("=" * 110)
viol = []
stats = dict(cases=0, single_ok=0, e_upper_checked=0, old_claim_fails=0, e_upper_fails_when_single=0,
             prop=0, kmix_gt_max=0, floor_case=0, ceil_case=0, greedy_tight=0)
delta = 0.05
examples = []
worst_fail = 0.0
min_ratio_p = math.inf
max_ratio_p = 0.0
for n in (6, 8, 10):
    for inst in range(12 if n < 10 else 6):
        pi = rng.dirichlet(np.ones(n) * rng.choice([0.3, 1.0, 5.0]))
        lo = -rng.exponential(1.5, n)
        hi = rng.exponential(1.5, n)
        placements = {
            "interior": lo + rng.random(n) * (hi - lo),
            "near floor": lo + 1e-3 * (hi - lo),
            "near ceiling": hi - 1e-3 * (hi - lo),
            "half floor/half ceil": np.where(rng.random(n) < 0.5, lo + 1e-9, hi - 1e-9),
        }
        for pl, r in placements.items():
            for eps in (0.02, 0.1, 0.2, 0.5, 1.0, 3.0):
                o = analyse(pi, lo, hi, r, eps, delta, f"rand n={n} #{inst} {pl}")
                check(o, viol)
                stats["cases"] += 1
                if not o["single"]:
                    stats["single_ok"] += 1
                    stats["e_upper_checked"] += 1
                    if o["N"] is not None and o["N"] > o["upper_e_dips_only"]:
                        stats["old_claim_fails"] += 1
                else:
                    if o["N"] is not None and o["N"] > o["upper_e"]:
                        stats["e_upper_fails_when_single"] += 1
                if o["k_mix"] > max(o["k_dip"], o["k_bump"]):
                    stats["kmix_gt_max"] += 1
                if o["N"] is not None:
                    worst_fail = max(worst_fail, o["fail_exact"])
                    if o["p_formula"] < 1:
                        min_ratio_p = min(min_ratio_p, o["p_exact"] / o["p_formula"])
                        max_ratio_p = max(max_ratio_p, o["p_exact"] / o["p_formula"])
                if inst == 0 and eps in (0.1, 1.0):
                    examples.append(fmt(o))
for e in examples:
    print(e)
print()
print("cases:", stats["cases"], "| with the single-state condition satisfied:", stats["single_ok"])
print("violations of any checked statement:", len(viol))
for name, o in viol[:10]:
    print("  VIOLATION:", name, "::", fmt(o))
print("worst exact failure probability of the spot check of (c) over all cases: %.4g (delta = %g)" % (worst_fail, delta))
print("exact detection probability / formula p(eta): min %.4f, max %.4f  (statement: >= 1; 'between p and 2p' "
      "holds for the linear relaxation only)" % (min_ratio_p, max_ratio_p))
print("cases with k_mix > max(k_dip, k_bump):", stats["kmix_gt_max"])
print("cases (single-state condition holding) in which N exceeds the bound of (e) computed with k_dip alone:",
      stats["old_claim_fails"])
print("cases in which the single-state condition FAILS and N exceeds the bound of (e):",
      stats["e_upper_fails_when_single"], "(the condition is needed for the display)")
print("elapsed %.1f s" % (time.time() - T0))

print()
print("=" * 110)
print("PART B — uniform pi on n points, constant box [-rho_m, rho_p]: packings in closed form (identical points)")
print("=" * 110)


def uniform_case(n, rho_m, rho_p, v, eps, delta):
    """All states have r = v.  Identical points: a set is heavy iff it has >= m_d (m_b) points."""
    z = math.exp(-v)
    dip1 = (math.exp(rho_m) - math.exp(-v)) / n
    bump1 = (math.exp(-v) - math.exp(-rho_p)) / n
    a, b = n * dip1 / z, n * bump1 / z
    td, tb = (math.exp(eps) - 1) * z, (1 - math.exp(-eps)) * z
    m_d = math.floor(td / dip1 + 1e-12) + 1 if dip1 > 0 else math.inf
    m_b = math.floor(tb / bump1 + 1e-12) + 1 if bump1 > 0 else math.inf
    k_dip = n // m_d if m_d <= n else 0
    k_bump = n // m_b if m_b <= n else 0
    m = min(m_d, m_b)
    k_mix = n // m if m <= n else 0
    single = (dip1 >= td) or (bump1 >= tb)
    eta = eps / 2
    A_ = a / (math.exp(eta) - 1)
    B_ = b / (1 - math.exp(-eta))
    L = math.log(1 / delta)
    N_general = math.ceil(L * max(1, 2 * A_, 2 * B_) - 1e-12)
    N_prop = math.ceil(L * max(1, A_, B_) - 1e-12)
    # exact: the sampler is uniform; a far member (level eta) differs on >= m2 points
    td2, tb2 = (math.exp(eta) - 1) * z, (1 - math.exp(-eta)) * z
    m2 = min(math.floor(td2 / dip1 + 1e-12) + 1 if dip1 > 0 else math.inf,
             math.floor(tb2 / bump1 + 1e-12) + 1 if bump1 > 0 else math.inf)
    p_exact = min(1.0, m2 / n) if m2 <= n else None
    return dict(n=n, a=a, b=b, k_dip=k_dip, k_bump=k_bump, k_mix=k_mix, single=single,
                fl_dip=math.floor(a / (2 * (math.exp(eps) - 1))), fl_bump=math.floor(b / (2 * (1 - math.exp(-eps)))),
                N_general=N_general, N_prop=N_prop, p_exact=p_exact,
                fail_prop=(1 - p_exact) ** N_prop if p_exact is not None else 0.0,
                lower=(1 - 2 * delta) * k_mix, upper_e=4 * L * (math.exp(eps / 2) + 1) * (k_mix + 1) + 1,
                upper_old=4 * L * (math.exp(eps / 2) + 1) * (k_dip + 1) + 1,
                lower_old=(1 - 2 * delta) * k_dip)


print("B1. the centre (v = 0), rho_m = 3, rho_p = 3, eps = 0.2 (eta = 0.1), delta = 0.05 — the report's 544 / 1088:")
for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
    u = uniform_case(n, 3.0, 3.0, 0.0, 0.2, 0.05)
    print(f"  n={n:>8d} a={u['a']:.4f} b={u['b']:.4f} k_dip={u['k_dip']} (floor {u['fl_dip']}) k_bump={u['k_bump']} "
          f"(floor {u['fl_bump']}) k_mix={u['k_mix']} | N_prop={u['N_prop']} N_general={u['N_general']} "
          f"exact failure of N_prop samples={u['fail_prop']:.5f} | (1-2d)k={u['lower']:.1f} <= cost <= "
          f"N_prop <= upper(e)={u['upper_e']:.1f}  single-state cond. violated: {u['single']}")
print("B2. the constant box, r at the floor (v = -rho_m): no dips at all; old statement vs new")
print("    old upper end with k_dip:  4 ln(1/delta)(e^{eps/2}+1)(k_dip+1)+1 ;  new lower end (1-2 delta) k_bump")
for eps in (0.2, 0.05, 0.02, 0.01, 0.005):
    u = uniform_case(10 ** 6, 3.0, 3.0, -3.0, eps, 0.05)
    flag = "OLD TWO-SIDED CLAIM REFUTED (lower bound from bumps exceeds the upper end written with k_dip)" \
        if u["lower"] > u["upper_old"] else ""
    print(f"  eps={eps:<6g} a={u['a']:.3g} b={u['b']:.5f} k_dip={u['k_dip']} k_bump={u['k_bump']} (floor {u['fl_bump']}) "
          f"(1-2d)k_bump={u['lower']:.1f}  upper(k_dip)={u['upper_old']:.1f}  upper(k_mix)={u['upper_e']:.1f}  {flag}")
print("B3. Theta-reading: ratio of the two ends of (e) as eps grows, centre of the constant box rho_m = 12, rho_p = 3, n = 10^7")
for eps in (0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0):
    u = uniform_case(10 ** 7, 12.0, 3.0, 0.0, eps, 0.05)
    quantity = u["a"] / eps + u["b"] / eps
    print(f"  eps={eps:<4g} (a+b)/eps={quantity:10.1f}  k={u['k_mix']:>7d}  lower=(1-2d)k={u['lower']:10.1f}  "
          f"N_prop={u['N_prop']:>8d}  upper(e)={u['upper_e']:12.1f}  N_prop/lower={u['N_prop'] / max(u['lower'], 1e-9):8.1f}  "
          f"lower/((a+b)/eps)={u['lower'] / quantity:.4f}  N_prop/((a+b)/eps)={u['N_prop'] / quantity:.4f}")

print()
print("=" * 110)
print("PART C — the rule without a hint ('what the hint buys'): exact failure probability")
print("=" * 110)


def q_of(v, rho_m, eta):
    up = (math.exp(eta) - 1) / (math.exp(rho_m + v) - 1) if rho_m + v > 0 else math.inf
    return min(up, 1 - math.exp(-eta))


def N_of(v, rho_m, eta, delta):
    return math.ceil(math.log(1 / delta) / q_of(v, rho_m, eta) - 1e-12) + 1


def failure(levels, masses, rho_m, eta, delta):
    """Exact probability that the rule stops with an output off by more than eta, on the member
    with the given levels and masses: sum over wrong levels v of s_v^{N(v)}."""
    zz = sum(s * math.exp(-v) for v, s in zip(levels, masses))
    tot = 0.0
    for v, s in zip(levels, masses):
        if abs(math.log(zz) + v) > eta:
            tot += s ** N_of(v, rho_m, eta, delta)
    return tot


rho_m, rho_p, eta, delta = 3.0, 3.0, 0.1, 0.05
print("N(0) = %d (report: 545);  hinted, proportional: %d (report: 544);  general bound of (c): %d (report: 1088)" % (
    N_of(0.0, rho_m, eta, delta),
    math.ceil(math.log(1 / delta) * max(1, (math.exp(rho_m) - 1) / (math.exp(eta) - 1),
                                        (1 - math.exp(-rho_p)) / (1 - math.exp(-eta))) - 1e-12),
    math.ceil(math.log(1 / delta) * max(1, 2 * (math.exp(rho_m) - 1) / (math.exp(eta) - 1),
                                        2 * (1 - math.exp(-rho_p)) / (1 - math.exp(-eta))) - 1e-12)))
# two-level members: level v (mass s) and level u (mass 1 - s); worst case approached at u = floor,
# s just below 1 - q(v)
worst2 = (0.0, None)
grid_v = np.linspace(-rho_m, rho_p, 241)
for v in grid_v:
    for u in (-rho_m, rho_p, 0.0, -1.5, 1.5):
        if u == v:
            continue
        qv = q_of(v, rho_m, eta)
        cand = [1 - qv - 1e-12, 1 - qv + 1e-12, 1 - qv * 1.01, 1 - qv * 1.1, 1 - qv * 2, 0.5, 0.9, 0.99, 0.999]
        # also the exact thresholds at which the output at v becomes wrong
        for s in cand:
            if 0 < s < 1:
                f = failure([v, u], [s, 1 - s], rho_m, eta, delta)
                if f > worst2[0]:
                    worst2 = (f, (float(v), float(u), float(s)))
# exact supremum over two-level members with the second level at the floor: s -> (1-s*)^- where
# s* is the exact threshold mass at which the up-error starts: (1-s)(e^{rho_m} - e^{-v}) = e^{-v}(e^eta - 1)
sup2 = (0.0, None)
for v in np.linspace(-rho_m + 1e-6, rho_p, 6001):
    thr = (math.exp(eta) - 1) / (math.exp(rho_m + v) - 1)
    if thr < 1:
        s = 1 - thr * (1 + 1e-12)
        f = s ** N_of(v, rho_m, eta, delta)
        if f > sup2[0]:
            sup2 = (f, float(v))
# and with the second level at the ceiling (down-error): (1-s)(e^{-v} - e^{-rho_p}) = e^{-v}(1 - e^{-eta})
sup2d = (0.0, None)
for v in np.linspace(-rho_m, rho_p - 1e-6, 6001):
    thr = (1 - math.exp(-eta)) / (1 - math.exp(-(rho_p - v)))
    if thr < 1:
        s = 1 - thr * (1 + 1e-12)
        f = s ** N_of(v, rho_m, eta, delta)
        if f > sup2d[0]:
            sup2d = (f, float(v))
print("two-level members, coarse search: worst failure %.6f = %.4f * delta at (v, u, s) = %s" % (
    worst2[0], worst2[0] / delta, worst2[1]))
print("two-level members, second level at the floor, mass at the exact threshold, v on a grid of 6001: "
      "sup failure %.6f = %.4f * delta at v = %.4f" % (sup2[0], sup2[0] / delta, sup2[1]))
print("two-level members, second level at the ceiling: sup failure %.6f = %.4f * delta at v = %.4f" % (
    sup2d[0], sup2d[0] / delta, sup2d[1]))
worst3 = 0.0
for _ in range(200000):
    lv = np.sort(rng.uniform(-rho_m, rho_p, 3))
    kind = rng.integers(3)
    if kind == 0:
        ms = rng.dirichlet(np.ones(3))
    elif kind == 1:
        s = 1 - q_of(lv[1], rho_m, eta) * rng.uniform(1.0, 1.5)
        t = rng.random()
        ms = np.array([(1 - s) * t, s, (1 - s) * (1 - t)])
    else:
        lv[0] = -rho_m
        s = 1 - q_of(lv[2], rho_m, eta) * rng.uniform(1.0, 1.2)
        t = rng.random()
        ms = np.array([(1 - s) * t, (1 - s) * (1 - t), s])
    if np.all(ms > 0):
        worst3 = max(worst3, failure(list(lv), list(ms), rho_m, eta, delta))
print("three-level members, 200000 random: worst failure %.6f = %.4f * delta" % (worst3, worst3 / delta))
print("all failures <= delta: %s" % (max(worst2[0], sup2[0], sup2d[0], worst3) <= delta))

print()
print("=" * 110)
print("PART D — Monte Carlo of the spot check on one random instance (sanity of 'exact failure probability')")
print("=" * 110)
n = 10
pi = rng.dirichlet(np.ones(n))
lo = -rng.exponential(1.5, n)
hi = rng.exponential(1.5, n)
r = lo + rng.random(n) * (hi - lo)
eps = 0.5
o = analyse(pi, lo, hi, r, eps, delta, "MC instance")
print(fmt(o))
z = float(np.sum(pi * np.exp(-r)))
dip = pi * (np.exp(-lo) - np.exp(-r))
bump = pi * (np.exp(-r) - np.exp(-hi))
q = 0.5 * dip / dip.sum() + 0.5 * bump / bump.sum()
sd, sb, sq = subset_sums(dip), subset_sums(bump), subset_sums(q)
heavy2 = (sd > (math.exp(eps / 2) - 1) * z) | (sb > (1 - math.exp(-eps / 2)) * z)
if heavy2.any():
    cand = np.nonzero(heavy2)[0]
    Dstar = int(cand[np.argmin(sq[cand])])
    members = [i for i in range(n) if Dstar >> i & 1]
    N = o["N"]
    trials = 200000
    draws = rng.choice(n, size=(trials, N), p=q)
    miss = np.mean(~np.isin(draws, members).any(axis=1))
    print("worst alternative differs from r on %s (q-mass %.4f); N = %d; simulated miss frequency %.5f "
          "(exact (1-q(D))^N = %.5f; delta = %g)" % (members, sq[Dstar], N, miss, (1 - sq[Dstar]) ** N, delta))
print()
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_01_DONE")
