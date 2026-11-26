#!/usr/bin/env python3
"""R12 item 4 — Corollary 11.114 (a ratio of two macrostate weights in a box class), written from the
statement in the theory report (export at 9408e33) and from the Lean statements of
proofs/Frontiers/BoxRatio.lean, before the harness block XXIV.8 was opened.

Setting.  X finite, weights pi >= 0, box lo <= r <= hi, macrostates A, B (disjoint).  For M in {A, B}:
W_M = sum_{x in M} pi e^{-r};  dip_M(x) = pi(x)(e^{-lo} - e^{-r}) on M, 0 elsewhere;  bump_M likewise;
U_M, V_M their totals;  a_M = U_M/W_M = W_M(lo)/W_M - 1,  b_M = V_M/W_M = 1 - W_M(hi)/W_M.
Sampler: q = 1/4 (dip_A/U_A + bump_A/V_A + dip_B/U_B + bump_B/V_B).

A member r' of the box changes the log-ratio ln(W_A/W_B) by more than eta iff it differs from r on a
set D that is *ratio-heavy*: (1 + dip_A(D)/W_A)/(1 - bump_B(D)/W_B) > e^eta  (lower D∩A, raise D∩B)
or the same with A and B exchanged.  All subsets D are enumerated.

Checked:
  (a) exact detection probability min_{D heavy} q(D)  >=  1/2 min(p_A, p_B),
      p_M = 1/2 min((e^eta - 1)/a_M, (1 - e^{-eta})/b_M)                 [ratio_detect_ge]
      and the arithmetic core [ratio_core] on random numbers;
  (b) exact worst-case failure of the spot check with N = ceil(ln(1/delta)/min(1, 1/2 min(p_A, p_B))) <= delta;
  (c) packings: sets inside one macrostate with dip weight > (e^eps - 1) W_M  (the alternatives of the
      Lean lower bound), exact by DP; all ratio-heavy sets, exact by DP; fractional hitting number by LP;
  (d) the display "cost ~ max_M a_M / eps": where it holds, and an instance at the floor of both
      macrostates where the dips give nothing and the bumps force ~ b/eps evaluations;
  (3) A, B a partition: packing and fractional hitting numbers of ln Z against those of the ratio;
      the example "weight 1e-6, floor 8 kT deep, 0.1 kT elsewhere".

One command:  python3 r12_06_ratio.py
"""
import math
import time

import numpy as np
from scipy.optimize import linprog

T0 = time.time()
rng = np.random.default_rng(2026112606)


def subset_sums(v):
    n = len(v)
    s = np.zeros(1 << n)
    for i in range(n):
        s[1 << i:1 << (i + 1)] = s[0:1 << i] + v[i]
    return s


def packing_number(heavy):
    size = len(heavy)
    f = np.zeros(size, dtype=np.int32)
    for S in range(1, size):
        low = S & (-S)
        rest = S ^ low
        best = f[rest]
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
    idx = np.nonzero(heavy)[0]
    if len(idx) == 0:
        return 0.0
    rows = []
    for D in idx:
        if not any((D >> i & 1) and heavy[D ^ (1 << i)] for i in range(n)):
            rows.append([-(D >> i & 1) for i in range(n)])
    A = np.array(rows, dtype=float)
    res = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(rows)), bounds=[(0, None)] * n, method="highs")
    assert res.status == 0
    return float(res.fun)


def analyse(pi, lo, hi, r, inA, eps, delta):
    """inA: boolean array, True for states of A, False for states of B (a partition of X)."""
    n = len(pi)
    inB = ~inA
    w = pi * np.exp(-r)
    dip = pi * (np.exp(-lo) - np.exp(-r))
    bump = pi * (np.exp(-r) - np.exp(-hi))
    out = {}
    WA, WB = w[inA].sum(), w[inB].sum()
    dA, dB = np.where(inA, dip, 0.0), np.where(inB, dip, 0.0)
    bA, bB = np.where(inA, bump, 0.0), np.where(inB, bump, 0.0)
    UA, UB, VA, VB = dA.sum(), dB.sum(), bA.sum(), bB.sum()
    aA, aB, bbA, bbB = UA / WA, UB / WB, VA / WA, VB / WB
    sdA, sdB, sbA, sbB = subset_sums(dA), subset_sums(dB), subset_sums(bA), subset_sums(bB)

    def heavy_ratio(e):
        up = (1 + sdA / WA) > math.exp(e) * (1 - sbB / WB)
        down = (1 + sdB / WB) > math.exp(e) * (1 - sbA / WA)
        return up | down

    def heavy_dips_inside(e):
        """the alternatives of ratio_expected_queries_ge: D inside one macrostate, heavy in dips there"""
        allS = np.arange(1 << n)
        maskA = sum(1 << i for i in range(n) if inA[i])
        maskB = sum(1 << i for i in range(n) if inB[i])
        insA = (allS & maskB) == 0
        insB = (allS & maskA) == 0
        return (insA & (sdA > (math.exp(e) - 1) * WA)) | (insB & (sdB > (math.exp(e) - 1) * WB))

    def heavy_Z(e):
        Z = WA + WB
        return ((sdA + sdB) > (math.exp(e) - 1) * Z) | ((sbA + sbB) > (1 - math.exp(-e)) * Z)

    eta = eps / 2
    L = math.log(1 / delta)
    out.update(aA=aA, aB=aB, bA=bbA, bB=bbB)
    if min(UA, UB, VA, VB) > 0:
        q = 0.25 * (dA / UA + bA / VA + dB / UB + bB / VB)
        sq = subset_sums(q)
        pA = 0.5 * min((math.exp(eta) - 1) / aA, (1 - math.exp(-eta)) / bbA)
        pB = 0.5 * min((math.exp(eta) - 1) / aB, (1 - math.exp(-eta)) / bbB)
        p_formula = 0.5 * min(pA, pB)
        h2 = heavy_ratio(eta)
        p_exact = float(sq[h2].min()) if h2.any() else 1.0
        N = math.ceil(L / min(1.0, p_formula) - 1e-12)
        out.update(p_formula=p_formula, p_exact=p_exact, N=N,
                   fail=(1 - min(1.0, p_exact)) ** N if h2.any() else 0.0)
        # ln Z spot check of Theorem 11.110(c) for comparison
        aZ, bZ = (UA + UB) / (WA + WB), (VA + VB) / (WA + WB)
        out["N_Z"] = math.ceil(L * max(1.0, 2 * aZ / (math.exp(eta) - 1), 2 * bZ / (1 - math.exp(-eta))) - 1e-12)
        out["aZ"], out["bZ"] = aZ, bZ
    hr = heavy_ratio(eps)
    hd = heavy_dips_inside(eps)
    hz = heavy_Z(eps)
    out["k_dips_inside"] = packing_number(hd)
    out["k_ratio"] = packing_number(hr)
    out["k_Z"] = packing_number(hz)
    out["tau_ratio"] = frac_hitting(hr, n)
    out["tau_Z"] = frac_hitting(hz, n)
    out["single_dip"] = bool(np.any(dA > (math.exp(eps) - 1) * WA) or np.any(dB > (math.exp(eps) - 1) * WB))
    out["floor_formula"] = max(math.floor(aA / (2 * (math.exp(eps) - 1))), math.floor(aB / (2 * (math.exp(eps) - 1))))
    return out


print("=" * 110)
print("PART 1 — the arithmetic core (ratio_core) on random numbers")
print("=" * 110)
bad = 0
tested = 0
for _ in range(200000):
    E = 1 + rng.exponential(1.0)
    ZA, ZB, UA, VB = rng.exponential(1.0, 4) + 1e-6
    dA, bB = rng.exponential(1.0) * rng.integers(0, 2), rng.exponential(1.0) * rng.integers(0, 2)
    if (E - 1) * ZA * ZB < dA * ZB + E * ZA * bB:
        tested += 1
        if min((E - 1) * ZA / UA, (1 - 1 / E) * ZB / VB) > dA / UA + bB / VB + 1e-12:
            bad += 1
print("random instances satisfying the hypothesis: %d; violations of the conclusion: %d" % (tested, bad))

print()
print("=" * 110)
print("PART 2 — random boxes with a partition into two macrostates (n = 8, 10), exhaustive over subsets")
print("=" * 110)
delta = 0.05
viol = []
cases = 0
worst_fail = 0.0
ratio_p = []
n_kz_gt = 0
n_tau_gt = 0
n_ratio_gt_inside = 0
n_floor_checked = 0
for n in (8, 10):
    for inst in range(20 if n == 8 else 8):
        pi = rng.dirichlet(np.ones(n))
        lo = -rng.exponential(1.5, n)
        hi = rng.exponential(1.5, n)
        inA = np.zeros(n, dtype=bool)
        inA[rng.choice(n, size=n // 2, replace=False)] = True
        for pl in range(3):
            if pl == 0:
                r = lo + rng.random(n) * (hi - lo)
            elif pl == 1:
                r = lo + 1e-3 * (hi - lo)
            else:
                r = hi - 1e-3 * (hi - lo)
            for eps in (0.05, 0.2, 1.0):
                o = analyse(pi, lo, hi, r, inA, eps, delta)
                cases += 1
                if "p_exact" in o:
                    if o["p_exact"] < o["p_formula"] - 1e-9:
                        viol.append(("ratio_detect_ge", o))
                    if o["fail"] > delta + 1e-9:
                        viol.append(("spot check failure", o))
                    worst_fail = max(worst_fail, o["fail"])
                    if o["p_formula"] < 1:
                        ratio_p.append(o["p_exact"] / o["p_formula"])
                if o["k_dips_inside"] > o["k_ratio"]:
                    viol.append(("inside-dip packing exceeds the ratio packing", o))
                if o["k_ratio"] > o["tau_ratio"] + 1e-6:
                    viol.append(("packing > fractional", o))
                if o["k_Z"] > o["k_ratio"]:
                    n_kz_gt += 1
                    viol.append(("k_Z > k_ratio on a partition", o))
                if o["tau_Z"] > o["tau_ratio"] + 1e-6:
                    n_tau_gt += 1
                    viol.append(("tau*_Z > tau*_ratio on a partition", o))
                if o["k_ratio"] > o["k_dips_inside"]:
                    n_ratio_gt_inside += 1
                if not o["single_dip"]:
                    n_floor_checked += 1
                    if o["k_dips_inside"] < o["floor_formula"]:
                        viol.append(("greedy floor max_M floor(a_M/(2(e^eps-1))) fails", o))
print("cases: %d; violations of any checked statement: %d" % (cases, len(viol)))
for name, o in viol[:5]:
    print("   VIOLATION", name, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in o.items()})
print("exact detection probability / (1/2 min(p_A, p_B)): min %.4f, median %.2f" % (min(ratio_p), float(np.median(ratio_p))))
print("worst exact failure of the spot check: %.5f (delta = %g)" % (worst_fail, delta))
print("cases with k_Z > k_ratio: %d; with tau*_Z > tau*_ratio: %d (claim (3): the ratio costs at least as much as ln Z)" % (
    n_kz_gt, n_tau_gt))
print("cases in which the packing of all ratio-heavy sets exceeds the packing of the Lean alternatives (dips inside one "
      "macrostate): %d of %d (the bumps and the mixed alternatives matter there)" % (n_ratio_gt_inside, cases))
print("cases with no single state heavy in dips inside its macrostate: %d (greedy floor checked there)" % n_floor_checked)

print()
print("=" * 110)
print("PART 3 — both macrostates at the floor: the dip display of (d) gives 0, the bumps carry the cost")
print("=" * 110)


def uniform_two_macro(nA, nB, rho_m, rho_p, vA, vB, eps, delta, weightA=0.5):
    """Identical points inside each macrostate; closed forms.  Constant box [-rho_m, rho_p], r = vA on A, vB on B."""
    res = {}
    L = math.log(1 / delta)
    ks = {}
    for name, nM, v in (("A", nA, vA), ("B", nB, vB)):
        a = math.exp(rho_m + v) - 1          # W_M(lo)/W_M - 1
        b = 1 - math.exp(-(rho_p - v))       # 1 - W_M(hi)/W_M
        # sets inside M: m points have relative dip weight m a / nM, relative bump weight m b / nM
        m_d = math.floor((math.exp(eps) - 1) * nM / a + 1e-12) + 1 if a > 0 else math.inf
        m_b = math.floor((1 - math.exp(-eps)) * nM / b + 1e-12) + 1 if b > 0 else math.inf
        ks[name] = (nM // m_d if m_d <= nM else 0, nM // m_b if m_b <= nM else 0, a, b)
    res["k_dip"] = ks["A"][0] + ks["B"][0]
    res["k_bump"] = ks["A"][1] + ks["B"][1]
    aS, bS = max(ks["A"][2], ks["B"][2]), max(ks["A"][3], ks["B"][3])
    eta = eps / 2
    A_ = aS / (math.exp(eta) - 1) if aS > 0 else 0.0
    B_ = bS / (1 - math.exp(-eta)) if bS > 0 else 0.0
    res["N"] = math.ceil(L * max(1.0, 4 * A_, 4 * B_) - 1e-12)
    res["a_max"], res["b_max"] = aS, bS
    return res


for eps in (0.2, 0.05, 0.01):
    u = uniform_two_macro(10 ** 6, 10 ** 6, 3.0, 3.0, -3.0, -3.0, eps, 0.05)
    print("eps = %-5g at the floor of both macrostates: max_M a_M = %.3g (display of (d): %.3g); dip packing %d; bump packing "
          "inside the macrostates %d  =>  cost >= (1 - 2 delta) x %d = %.1f;  spot check (with the bump half only where "
          "U_M = 0): N <= %d" % (eps, u["a_max"], u["a_max"] / eps, u["k_dip"], u["k_bump"], u["k_bump"],
                                 0.9 * u["k_bump"], u["N"]))
print("(the alternative 'raised to the ceiling on a set inside one macrostate' lowers that macrostate's weight by its bump "
      "weight and leaves the other unchanged: the log-ratio moves by -ln(1 - bump_M(D)/W_M) > eps as soon as "
      "bump_M(D) > (1 - e^-eps) W_M — the analogue of logZ_bumpAlt_gt; it is not in BoxRatio.lean)")

print()
print("=" * 110)
print("PART 4 — the example of consequence (3)")
print("=" * 110)
wA = 1e-6
aA = math.exp(8.0) - 1
aB = math.exp(0.1) - 1
aZ = wA * aA + (1 - wA) * aB
print("macrostate A: weight %.0e, floor 8 kT deep: W_A(lo)/W_A - 1 = %.2f (report: 2980);  elsewhere 0.1 kT: %.5f;" % (wA, aA, aB))
print("ln Z: Z(lo)/Z - 1 = %.5f (report: 0.11) = weighted mean of the two (weights W_M/Z)" % aZ)
for eps in (0.2,):
    eta = eps / 2
    L = math.log(20)
    N_ratio = math.ceil(L * max(1, 4 * aA / (math.exp(eta) - 1)))
    N_Z = math.ceil(L * max(1, 2 * aZ / (math.exp(eta) - 1), 2 * 1.0 / (1 - math.exp(-eta))))
    print("eps = %g, delta = 0.05, ceiling far away: spot-check sizes: ratio (dip term of A) %d;  ln Z: at most %d "
          "(dip term %.1f, bump term at most %.1f)" % (
              eps, N_ratio, N_Z, L * 2 * aZ / (math.exp(eta) - 1), L * 2 / (1 - math.exp(-eta))))
print()
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_06_DONE")
