"""Review of ENG-RES-0016 §2, item 2 of the brief: the code against the statement.

(a) ``hetero.constants`` against the referee's own evaluation of the formulas of K_REPORT §2.2 with the substitutions of
    the draft's table (``review_sim.make_consts``: exact integer balls, tables from the definitions), on random blocks
    and parameter sets, including outer blocks that are only part of a type.
(b) ``hetero_literal.run_2l`` against the referee's simulator, run by run: with a deterministic inner oracle ("bottom",
    "top") both draw the outer sample with the same calls of the generator, so the two runs see the same sample and
    must agree in the stopping level, the sample size and both ends of the bracket.

    python experiments/eng/review_x014/check_code.py            # writes check_code.json   (about 8 minutes)
"""
from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
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
from metricchain_eng.twolevel.certified import tables  # noqa: E402

LID = math.log(20.0)
ETAS = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 10), Fraction(1, 20)]


def random_case(rng, small: bool):
    n_o = int(rng.integers(1, 13 if small else 90))
    u_o = float(rng.choice([0.05, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]))
    m = int(rng.integers(1, 4))
    inner = []
    for _ in range(m):
        inner.append((float(rng.choice([0.01, 0.2, 0.5, 0.7, 1.0, 2.0, 2.5, 4.0, 8.0])), int(rng.integers(1, 5 if small else 60))))
    if rng.random() < 0.3:
        inner.append((u_o, int(rng.integers(1, 4))))                # outer block = part of a type
    eta = ETAS[int(rng.integers(len(ETAS)))]
    lam = float(rng.choice([1.0, 0.5, 0.2, 0.05, 0.6180339887]))
    etap = float(rng.choice([1.0, 0.5, 0.25, 0.05]))
    theta = float(rng.choice([0.01, 0.05, 0.25, 1.0, 5.0, 40.0, 1e6]))
    bounded = bool(rng.random() < 0.5)
    Lr = int(rng.integers(1, 9))
    omega_y = sum(u * k for u, k in inner)
    b = float(rng.choice([0.02, 0.1, 0.5, 1.0, 2.5])) if rng.random() < 0.8 else 0.9 * 2 * omega_y
    if b >= 2 * omega_y:
        b = 0.5 * 2 * omega_y
    return n_o, u_o, inner, dict(lam=lam, eta=eta, etap=etap, b=b, Lr=Lr, theta=theta, bounded=bounded)


def both_constants(n_o, u_o, inner, kw, same_floats: bool = False):
    B = H.make_block([(u_o, n_o)] + list(inner))
    j = [i for i, (u, _) in enumerate(B) if u == u_o][0]
    Dh = H.HDesign(j=j, k=n_o, lam=kw["lam"], eta=float(kw["eta"]), etap=kw["etap"], b=kw["b"], Lr=kw["Lr"], theta=kw["theta"], bounded=kw["bounded"])
    Ch = H.constants(B, Dh, LID)
    us = [u_o] * n_o + [u for u, k in sorted(inner, reverse=True) for _ in range(k)]
    x0 = 2 * sum(us[n_o:])
    lth = math.log(kw["theta"])
    nu1 = max(1.0, 2 * n_o * math.exp(u_o) / kw["theta"]) if kw["bounded"] else 1.0
    Dr = rs.Design(us=tuple(us), n_o=n_o, lam=kw["lam"], eta=kw["eta"], etap=kw["etap"], lth=lth, nu1=nu1, b=kw["b"],
                   xs=rs.geometric_ladder(x0, kw["b"], kw["Lr"]), l_inv_delta=LID)
    Cr = rs.make_consts(Dr)
    if same_floats and Ch is not None:
        # same floats for Omega, Omega_Y, ln Pi and the ladder in both simulators: exact ties are then resolved alike
        Dr.xs = tuple(Ch.xs)
        Cr = rs.make_consts(Dr, override=dict(Omega=Ch.omega, Omega_Y=Ch.xs[0] / 2, lPi=Ch.l2p))
    return Ch, Cr, us


def compare_constants(n_cases: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    out = dict(cases=0, mismatches=[], max_abs_diff=dict(lM_bar=0.0, x_out=0.0, l_inv_delta_p=0.0, lCmax_unit=0.0, lnu=0.0, xs=0.0, lmult=0.0))
    for c in range(n_cases):
        n_o, u_o, inner, kw = random_case(rng, small=(c % 2 == 0))
        Ch, Cr, us = both_constants(n_o, u_o, inner, kw)
        if Ch is None:
            continue
        out["cases"] += 1
        ints = dict(J=(Ch.J, Cr.J), K=(Ch.K, Cr.K), m_max=(Ch.m_max, Cr.m_max), r_dag=(Ch.r_dag, Cr.r_dag))
        bad = {k: v for k, v in ints.items() if v[0] != v[1]}
        floats = dict(lM_bar=(Ch.lM_bar, Cr.lM_bar), x_out=(Ch.x_out, Cr.x_out), l_inv_delta_p=(Ch.l_inv_delta_p, Cr.l_inv_delta_p),
                      lCmax_unit=(hl.lcmax_unit(Ch), Cr.lCmax()), lnu=(Ch.lnu, Cr.lnu),
                      xs=(max(abs(a - b) for a, b in zip(Ch.xs, Cr.D.xs)), 0.0),
                      lmult=(max(abs(float(a) - min(rs.LN2 + Cr.lM_bar, math.log(Cr.J + 1) + Cr.lcnt(Cr.D.xs[l])))
                                 for l, a in enumerate(Ch.lmult())), 0.0))
        for k, (a, b) in floats.items():
            d = abs(a - b)
            out["max_abs_diff"][k] = max(out["max_abs_diff"][k], d)
            if d > 1e-8 * max(1.0, abs(b)):
                bad[k] = (a, b)
        # the scalars of the substitution table
        if abs(Ch.omega - sum(us)) > 1e-9 or abs(Ch.l2p - Cr.lPi) > 1e-9 or abs(Ch.xs[0] - 2 * Cr.Omega_Y) > 1e-9:
            bad["scalars"] = (Ch.omega, sum(us), Ch.l2p, Cr.lPi, Ch.xs[0], 2 * Cr.Omega_Y)
        if bad:
            out["mismatches"].append(dict(n_o=n_o, u_o=u_o, inner=inner, design={k: (str(v) if isinstance(v, Fraction) else v) for k, v in kw.items()}, bad=bad))
    return out


def crosscheck_runs(seed: int, budget_s: float) -> dict:
    """Run by run: the division's simulator and the referee's on the same sample."""
    rng = np.random.default_rng(seed)
    t0 = time.time()
    out = dict(runs=0, agree=0, disagreements=[], max_abs_diff_L=0.0, max_abs_diff_U=0.0, statuses={}, class_violation=-math.inf)
    shapes = [(6, 0.5, [(2.0, 3)]), (5, 2.0, [(0.4, 4)]), (7, 1.0, [(0.3, 2), (2.5, 1)]), (4, 0.2, [(3.0, 2), (1.1, 2)]), (8, 1.3, [(0.7, 3)]),
              (3, 3.0, [(0.5, 5)]), (6, 0.7, [(6.0, 1)]), (2, 1.0, [(1.7, 4), (0.4, 3)])]
    designs = [dict(lam=1.0, eta=Fraction(1, 2), etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False),
               dict(lam=0.5, eta=Fraction(1, 4), etap=0.25, b=0.5, Lr=4, theta=0.25, bounded=True),
               dict(lam=0.6180339887, eta=Fraction(1, 2), etap=0.5, b=0.37, Lr=2, theta=3.0, bounded=True),
               dict(lam=0.2, eta=Fraction(1, 3), etap=1.0, b=1.3, Lr=1, theta=0.1, bounded=False)]
    kinds = rs.INSTANCE_KINDS
    it = 0
    while time.time() - t0 < budget_s:
        n_o, u_o, inner = shapes[it % len(shapes)]
        kw = designs[(it // len(shapes)) % len(designs)]
        it += 1
        Ch, Cr, us = both_constants(n_o, u_o, inner, kw, same_floats=True)
        if Ch is None or Ch.K != Cr.K or Ch.J != Cr.J:
            continue
        us = np.asarray(us)
        T = tables(n_o, u_o)
        for kind in kinds:
            psi = rs.instance(kind, us, n_o, rng)
            out["class_violation"] = max(out["class_violation"], rs.class_violation(psi, us))
            for orc in ("bottom", "top"):
                s = int(rng.integers(2 ** 31))
                a = hl.run_2l(psi, n_o, Ch, T, orc, np.random.default_rng(s))
                r = rs.run(psi, Cr, orc, np.random.default_rng(s))
                out["runs"] += 1
                out["statuses"][a["status"]] = out["statuses"].get(a["status"], 0) + 1
                # the referee's simulator labels an abort that is an exact floating-point tie (K_REPORT erratum m10) separately
                mine_status = "abort: unclassified at the last rung" if r.info_tie_abort else r.status
                out["tie_aborts_m10"] = out.get("tie_aborts_m10", 0) + bool(r.info_tie_abort)
                same = (a["status"] == mine_status and a["level"] == r.level)
                if same and a["status"] == "closed":
                    dL, dU = abs(a["lL"] - r.lL), abs(a["lU"] - r.lU)
                    out["max_abs_diff_L"] = max(out["max_abs_diff_L"], dL)
                    out["max_abs_diff_U"] = max(out["max_abs_diff_U"], dU)
                    same = a["M"] == r.M and dL < 1e-8 and dU < 1e-8 and a["cost"] == r.queries
                if same:
                    out["agree"] += 1
                elif len(out["disagreements"]) < 20:
                    out["disagreements"].append(dict(shape=[n_o, u_o, inner], design={k: str(v) for k, v in kw.items()}, kind=kind, oracle=orc, seed=s,
                                                     theirs={k: a.get(k) for k in ("status", "level", "M", "lL", "lU", "cost")},
                                                     mine=dict(status=r.status, level=r.level, M=r.M, lL=r.lL, lU=r.lU, cost=r.queries, ties=r.ties)))
    out["seconds"] = time.time() - t0
    return out


def main() -> int:
    rs.limit_memory(2.5)
    t0 = time.time()
    res = dict(constants=compare_constants(600, 11), runs=crosscheck_runs(12, 420.0))
    res["seconds"] = time.time() - t0
    (HERE / "check_code.json").write_text(json.dumps(res, indent=1, default=str))
    c, r = res["constants"], res["runs"]
    print(f"constants: {c['cases']} cases, {len(c['mismatches'])} mismatches; max abs differences {c['max_abs_diff']}")
    for m in c["mismatches"][:10]:
        print("   ", m)
    print(f"runs: {r['runs']} compared, {r['agree']} agree; statuses {r['statuses']} (of the aborts, {r.get('tie_aborts_m10', 0)} are exact floating-point ties); "
          f"max |dL| {r['max_abs_diff_L']:.2e}, max |dU| {r['max_abs_diff_U']:.2e}; "
          f"class violation {r['class_violation']:.1e}")
    for d in r["disagreements"][:10]:
        print("   ", d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
