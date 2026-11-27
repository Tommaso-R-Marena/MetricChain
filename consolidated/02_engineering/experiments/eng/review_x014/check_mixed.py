"""Review of ENG-RES-0016 §5.1 and of ``hetero.MixedTables`` (added to the module while the review ran): an outer block
that mixes site types, with the sorted-slope tail functions

    upper (Lemma N14 of the theory division):  E_r  = sum_{j=1}^{r+1} (e^{U_j} - e^{U_{j-1}}) |B(m, r+1-j)|,
    lower (the division's own):                T(k) = sum_j C(m, j) e^{-U_{(j-k)_+}},      U_j = the sum of the j largest slopes.

(a) Both inequalities at their extremal functions, by brute force: for a set D of outer points the largest
    E(V - s)_+ / s over the class with {V > s} = D is 2^-m sum_{x in D} (e^{dist_u(x, D^c)} - 1), and for a set S the smallest
    E min(V, t)/t with {V >= t} = S is 2^-m sum_x e^{-dist_u(x, S)}.  All proper subsets of Q_4 for eight slope patterns
    (two, three and four different slopes); for Q_5..Q_8 random subsets and structured ones (Hamming balls, weighted balls,
    sub-cubes, initial segments of simplicial orders with the steep sites first / last / at random).
(b) ``hetero.MixedTables`` against the definitions (the referee's ``OuterTables`` with the sorted depth cost), for random
    compositions with up to four types and up to 160 sites; r_dagger with it.
(c) ``hetero.constants`` with a mixed outer block against the referee's constants.
(d) Literal runs with a mixed outer block: the referee's simulator with every claim checked, and the division's
    ``hetero_literal.run_2l`` fed with ``hetero.constants(.., comp)`` and ``hetero.mixed_tables(comp)``; negative controls:
    tables with the slopes sorted the WRONG way along the depth (smallest first), and uniform tables for the smallest slope.

    python experiments/eng/review_x014/check_mixed.py [--minutes 8] [--procs 2]          # writes check_mixed.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))

import hetero_literal as hl  # noqa: E402
import review_sim as rs  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402

LID = math.log(20.0)
BIG = 1e6


# ---------------------------------------------------------------------------------------------
# (a) brute force
# ---------------------------------------------------------------------------------------------
def sorted_tables(us):
    """(ball sizes, E_r for r <= m-1, T(k)) of the sorted-slope bounds, straight from the formulas above."""
    m = len(us)
    U = [0.0]
    for s in sorted(us, reverse=True):
        U.append(U[-1] + s)
    binom = [math.comb(m, j) for j in range(m + 1)]
    ball = [sum(binom[: r + 1]) for r in range(m + 1)]
    E = [math.fsum((math.exp(U[j]) - math.exp(U[j - 1])) * ball[r + 1 - j] for j in range(1, r + 2)) for r in range(m)]
    T = [math.fsum(binom[j] * math.exp(-U[max(j - k, 0)]) for j in range(m + 1)) for k in range(m + 1)]
    return np.array(ball), np.array(E), np.array(T)


def tails_of_sets(member: np.ndarray, us) -> tuple[np.ndarray, np.ndarray]:
    """member: (number of sets, 2^m) booleans.  Returns (sum_{x in D}(e^{dist(x, D^c)} - 1), sum_x e^{-dist(x, D)}) per set."""
    P = member.shape[1]
    idx = np.arange(P)
    out_c = np.where(member, BIG, 0.0)                    # -> weighted distance to the complement
    to_s = np.where(member, 0.0, BIG)                     # -> weighted distance to the set
    for i, u in enumerate(us):
        out_c = np.minimum(out_c, out_c[:, idx ^ (1 << i)] + u)
        to_s = np.minimum(to_s, to_s[:, idx ^ (1 << i)] + u)
    return np.expm1(out_c).sum(axis=1), np.exp(-to_s).sum(axis=1)


def check_sets(member: np.ndarray, us, ball, E, T) -> dict:
    m = len(us)
    size = member.sum(axis=1)
    keep = (size > 0) & (size < member.shape[1])
    member, size = member[keep], size[keep]
    parts = [tails_of_sets(member[i: i + 8192], us) for i in range(0, len(member), 8192)]       # in chunks: bounded memory
    up, low = np.concatenate([p[0] for p in parts]), np.concatenate([p[1] for p in parts])
    r = np.searchsorted(ball, size, side="left")            # least r with |B(m, r)| >= |D|   (<= m - 1 for a proper subset)
    k = np.searchsorted(ball, size, side="right") - 1       # largest k with |B(m, k)| <= |S|
    ratio_up = up / E[r]                                    # claim: <= 1
    ratio_low = T[k] / low                                  # claim: <= 1
    return dict(sets=int(len(size)), upper_violations=int(np.sum(ratio_up > 1 + 1e-12)), lower_violations=int(np.sum(ratio_low > 1 + 1e-12)),
                max_upper_ratio=float(ratio_up.max()), min_upper_ratio=float(ratio_up.min()), max_lower_ratio=float(ratio_low.max()),
                min_lower_ratio=float(ratio_low.min()))


def structured_sets(m: int, us, rng, count: int) -> np.ndarray:
    P = 2 ** m
    X = ((np.arange(P)[:, None] >> np.arange(m)[None, :]) & 1)
    sets = []
    for _ in range(count):
        kind = rng.integers(6)
        c = X[rng.integers(P)]
        dH = np.abs(X - c[None, :]).sum(axis=1)
        dW = np.abs(X - c[None, :]) @ us
        if kind == 0:                                       # Hamming ball
            sets.append(dH <= rng.integers(0, m))
        elif kind == 1:                                     # weighted ball
            sets.append(dW < rng.uniform(0, dW.max() * 1.05))
        elif kind == 2:                                     # sub-cube (some coordinates fixed)
            fixed = rng.random(m) < 0.5
            sets.append(np.all((X == c[None, :]) | ~fixed[None, :], axis=1))
        elif kind in (3, 4):                                # initial segment of a simplicial order: by Hamming distance, ties by a coordinate priority
            order = np.argsort(us) if kind == 3 else np.argsort(-us)          # steep sites last / first in the tie-break
            if rng.random() < 0.3:
                order = rng.permutation(m)
            key = ((X ^ c[None, :])[:, order] @ (1 << np.arange(m)))
            rank = np.lexsort((key, dH))
            s = np.zeros(P, dtype=bool)
            s[rank[: rng.integers(1, P)]] = True
            sets.append(s)
        else:                                               # union of two balls
            c2 = X[rng.integers(P)]
            sets.append((dH <= rng.integers(0, m // 2 + 1)) | (np.abs(X - c2[None, :]).sum(axis=1) <= rng.integers(0, m // 2 + 1)))
    return np.array(sets)


def brute_force(rng) -> dict:
    out = dict(exhaustive=[], sampled=[])
    for us in ([1.7, 1.7, 0.4, 0.4], [2.0, 0.5, 0.5, 0.5], [0.3, 0.3, 0.3, 4.0], [3.0, 1.0, 0.3, 0.1], [5.0, 0.1, 0.1, 0.1], [1.0, 1.0, 1.0, 1.0],
               [0.05, 2.5, 0.05, 2.5], [8.0, 4.0, 2.0, 1.0]):
        us = np.array(us)
        ball, E, T = sorted_tables(us)
        masks = np.arange(1, 2 ** 16 - 1, dtype=np.int64)
        member = ((masks[:, None] >> np.arange(16)[None, :]) & 1).astype(bool)
        res = check_sets(member, us, ball, E, T)
        res["slopes"] = us.tolist()
        out["exhaustive"].append(res)
    for m, us in ((5, [2.0, 2.0, 0.5, 0.5, 0.5]), (5, [3.0, 1.0, 0.5, 0.2, 0.1]), (6, [2.0, 2.0, 2.0, 0.5, 0.5, 0.5]), (6, [4.0, 0.25, 0.25, 0.25, 0.25, 0.25]),
                  (7, [1.5, 1.5, 1.0, 1.0, 0.3, 0.3, 0.3]), (8, [2.0, 2.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5]), (8, [6.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])):
        us = np.array(us)
        ball, E, T = sorted_tables(us)
        P = 2 ** m
        dens = rng.random((40000, 1)) ** 2
        member = np.concatenate([rng.random((40000, P)) < dens, structured_sets(m, us, rng, 20000)])
        res = check_sets(member, us, ball, E, T)
        res["slopes"] = us.tolist()
        out["sampled"].append(res)
    return out


# ---------------------------------------------------------------------------------------------
# (b), (c) the module's tables and constants
# ---------------------------------------------------------------------------------------------
def tables_and_constants(rng, cases: int) -> dict:
    out = dict(table_cases=0, max_abs_diff_lE=0.0, max_abs_diff_lT=0.0, max_abs_diff_lGt=0.0, r_dagger_cases=0, r_dagger_mismatches=[],
               constants_cases=0, constants_mismatches=[], worst_table_case=None)
    slopes_pool = [0.01, 0.05, 0.2, 0.5, 0.7, 1.0, 1.3, 2.0, 3.0, 5.0, 8.0]
    for c in range(cases):
        ntypes = int(rng.integers(2, 5))
        slopes = rng.choice(slopes_pool, size=ntypes, replace=False)
        hi = (6, 30, 80)[c % 3]
        comp = H.make_block([(float(u), int(rng.integers(1, hi))) for u in slopes])
        m = H.dim(comp)
        if m > 160 or max(u for u, _ in comp) * m > 600:
            continue
        Tm = H.MixedTables(m=m, u=H.umax(comp), comp=comp)
        eta = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 20)][int(rng.integers(4))]
        us_outer = [u for u, k in comp for _ in range(k)]
        Tr = rs.OuterTables(m, H.umax(comp), eta, depth_cost=rs.sorted_depth_cost(us_outer))
        dE = float(np.max(np.abs(Tm.lE[:m] - np.array(Tr.lE[:m]))))
        dT = float(np.max(np.abs(Tm.lT - np.array(Tr.lT))))
        dG = float(np.max(np.abs(Tm.lGt[:m] - np.array(Tr.lGt[:m]))))
        out["table_cases"] += 1
        if max(dE, dT, dG) > max(out["max_abs_diff_lE"], out["max_abs_diff_lT"], out["max_abs_diff_lGt"]):
            out["worst_table_case"] = dict(comp=[list(t) for t in comp], dE=dE, dT=dT, dG=dG)
        out["max_abs_diff_lE"] = max(out["max_abs_diff_lE"], dE)
        out["max_abs_diff_lT"] = max(out["max_abs_diff_lT"], dT)
        out["max_abs_diff_lGt"] = max(out["max_abs_diff_lGt"], dG)
        # r_dagger
        for _ in range(3):
            lth = math.log(float(rng.choice([0.01, 0.05, 0.25, 1.0, 5.0, 40.0, 1e6])))
            nu0 = float(rng.choice([2.0, 30.0, 1e3, 1e5]))
            a, b = Tm.r_dagger(float(eta), None, nu0, lth=lth), Tr.r_dagger(lth, nu0)
            out["r_dagger_cases"] += 1
            if a != b and len(out["r_dagger_mismatches"]) < 10:
                out["r_dagger_mismatches"].append(dict(comp=[list(t) for t in comp], eta=str(eta), lth=lth, nu0=nu0, theirs=a, mine=b))
        # constants of a level with this outer block and an inner block of one to three types
        inner = [(float(u), int(rng.integers(1, 20))) for u in rng.choice(slopes_pool, size=int(rng.integers(1, 4)), replace=False)]
        B = H.make_block(list(comp) + inner)
        x0 = 2 * sum(u * k for u, k in inner)
        kw = dict(lam=float(rng.choice([1.0, 0.5, 0.2])), eta=float(eta), etap=float(rng.choice([1.0, 0.25, 0.05])), b=min(float(rng.choice([0.1, 0.5, 1.0])), 0.45 * x0),
                  Lr=int(rng.integers(1, 6)), theta=float(rng.choice([0.05, 0.25, 1.0, 40.0])), bounded=bool(rng.random() < 0.5))
        Ch = H.constants(B, H.HDesign(j=0, k=0, comp=comp, **kw), LID)
        if Ch is None:
            continue
        us = us_outer + [u for u, k in inner for _ in range(k)]
        nu1 = max(1.0, 2 * m * math.exp(H.umax(comp)) / kw["theta"]) if kw["bounded"] else 1.0
        Dr = rs.Design(us=tuple(us), n_o=m, lam=kw["lam"], eta=eta, etap=kw["etap"], lth=math.log(kw["theta"]), nu1=nu1, b=kw["b"],
                       xs=rs.geometric_ladder(x0, kw["b"], kw["Lr"]))
        Cr = rs.make_consts(Dr, T=Tr)
        out["constants_cases"] += 1
        bad = {}
        for name, (a, b) in dict(J=(Ch.J, Cr.J), K=(Ch.K, Cr.K), m_max=(Ch.m_max, Cr.m_max), r_dag=(Ch.r_dag, Cr.r_dag)).items():
            if a != b:
                bad[name] = (a, b)
        for name, (a, b) in dict(lM_bar=(Ch.lM_bar, Cr.lM_bar), x_out=(Ch.x_out, Cr.x_out), omega=(Ch.omega, Cr.Omega), l2p=(Ch.l2p, Cr.lPi),
                                 x0=(Ch.xs[0], 2 * Cr.Omega_Y), lCmax_unit=(hl.lcmax_unit(Ch), Cr.lCmax())).items():
            if abs(a - b) > 1e-8 * max(1.0, abs(b)):
                bad[name] = (a, b)
        if bad and len(out["constants_mismatches"]) < 10:
            out["constants_mismatches"].append(dict(comp=[list(t) for t in comp], inner=inner, design=kw, bad=bad))
    return out


def large_tables() -> dict:
    """The module's window sums at sizes where a loss of digits would show: against the definitions evaluated term by term
    (log-shifted ``math.fsum``), for blocks of 300-640 sites."""
    out = dict(cases=[])
    for comp in ([(2.0, 250), (0.5, 350)], [(4.0, 60), (1.0, 500)], [(3.0, 200), (1.0, 200), (0.2, 200)], [(8.0, 20), (0.05, 300)],
                 [(1.0, 300), (0.99, 300)], [(2.0, 1), (0.5, 400)], [(6.0, 100), (0.01, 540)]):
        comp = H.make_block(comp)
        m = H.dim(comp)
        t0 = time.time()
        Tm = H.MixedTables(m=m, u=H.umax(comp), comp=comp)
        Tr = rs.OuterTables(m, H.umax(comp), Fraction(1, 3), depth_cost=rs.sorted_depth_cost([u for u, k in comp for _ in range(k)]))
        out["cases"].append(dict(comp=[list(t) for t in comp], m=m, max_abs_diff_lE=float(np.max(np.abs(Tm.lE[:m] - np.array(Tr.lE[:m])))),
                                 max_abs_diff_lT=float(np.max(np.abs(Tm.lT - np.array(Tr.lT)))),
                                 max_abs_diff_lG2=float(np.max(np.abs(Tm.lG2(1 / 3)[:m] - np.array(Tr.lG2[:m])))),
                                 kappa_equal=bool(np.array_equal(Tm.kappa(1 / 3), np.array(Tr.kappa))), seconds=time.time() - t0))
    out["max_abs_diff"] = max(max(c["max_abs_diff_lE"], c["max_abs_diff_lT"]) for c in out["cases"])
    return out


# ---------------------------------------------------------------------------------------------
# (d) literal runs
# ---------------------------------------------------------------------------------------------
SHAPES = [  # (outer composition as (slope, count) pairs, inner slopes)
    ([(2.0, 2), (0.5, 3)], (1.0, 1.0, 1.0)),
    ([(3.0, 1), (0.2, 5)], (0.7, 2.0)),
    ([(1.5, 3), (1.0, 2), (0.3, 2)], (2.5,)),
    ([(4.0, 2), (0.25, 4)], (0.5, 0.5, 0.5)),
    ([(0.9, 1), (0.1, 4)], (3.0, 3.0)),
    ([(2.0, 4), (0.5, 4)], (1.3, 0.4)),
    ([(6.0, 1), (0.05, 6)], (1.0, 0.2)),
    ([(1.37, 2), (0.83, 2), (0.29, 2)], (2.11, 0.61)),
]
DESIGNS = [
    dict(name="EXT", lam=1.0, eta=Fraction(1, 2), etap=1.0, theta=1.0, bounded=False, b=1.0, L=4),
    dict(name="BND", lam=0.5, eta=Fraction(1, 4), etap=0.25, theta=0.25, bounded=True, b=0.5, L=4),
    dict(name="generic", lam=0.6180339887, eta=Fraction(1, 2), etap=1.0, theta=1.0, bounded=True, b=0.7310585786, L=3),
    dict(name="theta=e^6", lam=1.0, eta=Fraction(1, 2), etap=1.0, theta=math.exp(6.0), bounded=False, b=1.0, L=3),
    dict(name="theta=0.02", lam=0.3, eta=Fraction(1, 3), etap=0.1, theta=0.02, bounded=True, b=0.2, L=4),
]
TABLES = ("sorted (the claim)", "CONTROL: slopes sorted smallest first", "CONTROL: uniform tables for the smallest slope")


def literal_task(args):
    si, di, ti, seconds, seed = args
    comp, inner = SHAPES[si]
    design = DESIGNS[di]
    us_outer = [u for u, k in comp for _ in range(k)]
    rng = np.random.default_rng(seed)
    rng.shuffle(us_outer)                                     # the order of the sites inside the outer block is irrelevant to the claim
    us = np.array(us_outer + list(inner))
    n_o = len(us_outer)
    x0 = 2 * sum(inner)
    b = design["b"] if design["b"] < 0.9 * x0 else 0.45 * x0
    umax = max(us_outer)
    nu1 = max(1.0, 2 * n_o * math.exp(umax) / design["theta"]) if design["bounded"] else 1.0
    D = rs.Design(us=tuple(us), n_o=n_o, lam=design["lam"], eta=design["eta"], etap=design["etap"], lth=math.log(design["theta"]), nu1=nu1, b=b,
                  xs=rs.geometric_ladder(x0, b, design["L"]))
    if ti == 0:
        T = None                                              # make_consts builds the sorted-slope tables
    elif ti == 1:
        srt = sorted(us_outer)                                # WRONG: smallest slopes first along the depth
        cum = [0.0] + list(np.cumsum(srt))
        T = rs.OuterTables(n_o, srt[0], design["eta"], depth_cost=lambda i: cum[i] if i <= n_o else cum[n_o] + srt[-1] * (i - n_o))
    else:
        T = rs.OuterTables(n_o, min(us_outer), design["eta"])
    C = rs.make_consts(D, T=T)
    out = dict(outer=comp, inner=list(inner), design=design["name"], tables=TABLES[ti], K=C.K, J=C.J, r_dag=C.r_dag, x_out=C.x_out, seed=seed)
    if C.K * 2 ** (n_o + 1) / (1 - float(design["eta"])) > 3e6:
        out["skipped"] = "samples too large"
        return out
    # the division's objects for the same level (claim only)
    Ch = Th = None
    if ti == 0:
        compB = H.make_block(comp)
        B = H.make_block(list(comp) + [(u, 1) for u in inner])
        Ch = H.constants(B, H.HDesign(j=0, k=0, comp=compB, lam=design["lam"], eta=float(design["eta"]), etap=design["etap"], b=b, Lr=design["L"],
                                      theta=design["theta"], bounded=design["bounded"]), LID)
        Th = H.mixed_tables(compB)
        out["division_constants_agree"] = bool(Ch is not None and (Ch.K, Ch.J, Ch.r_dag) == (C.K, C.J, C.r_dag) and abs(Ch.x_out - C.x_out) < 1e-9)
    st = dict(runs=0, closed=0, aborted=0, tie_aborts=0, good=0, invalid_good=0, invalid_bad=0, viol_good={}, viol_bad={}, det_viol={}, max_width=0.0,
              class_violation=-math.inf, div_runs=0, div_invalid=0, div_too_wide=0, div_aborted=0, div_bad_certificates=0, div_over_budget=0, examples=[])
    combos = [(k, o) for k in rs.INSTANCE_KINDS for o in rs.ORACLES]
    rng.shuffle(combos)
    t0 = time.time()
    i = 0
    while time.time() - t0 < seconds:
        kind, orc = combos[i % len(combos)]
        i += 1
        psi = rs.instance(kind, us, n_o, rng)
        st["class_violation"] = max(st["class_violation"], rs.class_violation(psi, us))
        s = int(rng.integers(2 ** 31))
        R = rs.run(psi, C, orc, np.random.default_rng(s))
        st["runs"] += 1
        st["good"] += R.good
        if R.status == "closed":
            st["closed"] += 1
            st["max_width"] = max(st["max_width"], R.width)
        elif R.info_tie_abort:
            st["tie_aborts"] += 1
        else:
            st["aborted"] += 1
        if any(k in R.viol for k in ("(ii) L <= A", "(ii) A <= U")):
            st["invalid_good" if R.good else "invalid_bad"] += 1
        for claim in R.viol:
            if claim in rs.DETERMINISTIC:
                st["det_viol"][claim] = st["det_viol"].get(claim, 0) + 1
            tgt = st["viol_good"] if R.good else st["viol_bad"]
            tgt[claim] = tgt.get(claim, 0) + 1
        if R.viol and len(st["examples"]) < 4:
            st["examples"].append(dict(kind=kind, oracle=orc, run_seed=s, good=R.good, viol=R.viol, lA=R.lA, lL=R.lL, lU=R.lU))
        if Ch is not None and i % 3 == 0:                      # the division's simulator on the same table
            for o2 in hl.ORACLES:
                r = hl.run_2l(psi, n_o, Ch, Th, o2, np.random.default_rng(int(rng.integers(2 ** 31))))
                st["div_runs"] += 1
                if r["status"] != "closed":
                    st["div_aborted"] += 1
                else:
                    st["div_invalid"] += not r["valid"]
                    st["div_too_wide"] += r["width"] > Ch.x_out + 1e-9
                    st["div_bad_certificates"] += not r["certificates_ok"]
                st["div_over_budget"] += math.log(r["cost"]) > hl.lcmax_unit(Ch) + 1e-9
    out.update(st)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=8.0)
    ap.add_argument("--procs", type=int, default=2)
    args = ap.parse_args()
    rs.limit_memory(1.3)
    t0 = time.time()
    rng = np.random.default_rng(2718)
    res = dict(brute_force=brute_force(rng), module=tables_and_constants(rng, 240), large_tables=large_tables())
    print("brute force, all proper subsets of Q_4:")
    for r in res["brute_force"]["exhaustive"]:
        print("   ", r)
    print("brute force, sampled and structured subsets:")
    for r in res["brute_force"]["sampled"]:
        print("   ", r)
    mo = res["module"]
    print(f"module: {mo['table_cases']} compositions, max |d ln E| {mo['max_abs_diff_lE']:.2e}, |d ln T| {mo['max_abs_diff_lT']:.2e}, |d ln Gamma~| {mo['max_abs_diff_lGt']:.2e}; "
          f"r_dagger: {len(mo['r_dagger_mismatches'])} mismatches in {mo['r_dagger_cases']}; constants: {len(mo['constants_mismatches'])} mismatches in {mo['constants_cases']}")
    for x in mo["r_dagger_mismatches"][:5] + mo["constants_mismatches"][:5]:
        print("   ", x)
    print("large blocks:", json.dumps(res["large_tables"], default=float))
    jobs = [(si, di, ti) for ti in range(3) for si in range(len(SHAPES)) for di in range(len(DESIGNS))]
    per = args.minutes * 60 * args.procs / len(jobs)
    with Pool(args.procs) as pool:
        rows = pool.map(literal_task, [j + (per, 5000 + 17 * i) for i, j in enumerate(jobs)], chunksize=1)
    summ = {}
    for r in rows:
        if "skipped" in r:
            continue
        d = summ.setdefault(r["tables"], dict(configurations=0, runs=0, closed=0, aborted=0, tie_aborts=0, good=0, invalid_on_good_event=0, invalid_off_good_event=0,
                                              violations_on_good_event={}, deterministic_violations={}, configurations_with_a_violation=0,
                                              division_runs=0, division_invalid=0, division_too_wide=0, division_aborted=0, division_bad_certificates=0,
                                              division_over_budget=0, division_constants_disagree=0))
        d["configurations"] += 1
        for a, b in (("runs", "runs"), ("closed", "closed"), ("aborted", "aborted"), ("tie_aborts", "tie_aborts"), ("good", "good"), ("invalid_on_good_event", "invalid_good"),
                     ("invalid_off_good_event", "invalid_bad"), ("division_runs", "div_runs"), ("division_invalid", "div_invalid"), ("division_too_wide", "div_too_wide"),
                     ("division_aborted", "div_aborted"), ("division_bad_certificates", "div_bad_certificates"), ("division_over_budget", "div_over_budget")):
            d[a] += r[b]
        for a, b in (("violations_on_good_event", "viol_good"), ("deterministic_violations", "det_viol")):
            for k, v in r[b].items():
                d[a][k] = d[a].get(k, 0) + v
        d["configurations_with_a_violation"] += bool(r["viol_good"] or r["viol_bad"])
        d["division_constants_disagree"] += r.get("division_constants_agree") is False
    res["literal"] = dict(summary=summ, rows=rows)
    res["seconds"] = time.time() - t0
    (HERE / "check_mixed.json").write_text(json.dumps(res, indent=1, default=float))
    for k, d in summ.items():
        print(k, json.dumps(d, default=float))
    print(f"[{time.time() - t0:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
