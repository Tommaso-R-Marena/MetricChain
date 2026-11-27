"""X-015: an independent reproduction of the theory division's Proposition 11.121 (workstream N, Proposition N12) --
with a dependent known part of unbounded influence, Algorithm 2L+ run with the tail function of the *assumed* class
returns a false certificate; with the tail function of the true class it is valid and costs more than enumerating
the outer cube.

The instance, from the statement alone (theory report at eb88823, §11.33):

    outer block Q_m with the uniform marginal;  inner block Q_k with the conditional law Bernoulli(p(a))^k,
    p(a) = sigma(J (tau - |a|));  residual psi(a, b) = u |b|;   m = 12, k = 16, u = 1, J = 4, tau = 10.5,

so that V(a) = (1 - p(a) + p(a) e^-u)^k.  The simulator is ``hetero_literal.run_2l_fibres`` -- a transcription of
K_REPORT §2.2 written for experiment X-014 (cubes with site-dependent slopes), independent of the workstream's
``n3_sim_abstract.py`` and of its referee's code, neither of which was read.  The algorithm's parameters are ours
(the workstream's are not in its report): the two parameter sets of X-014 and the two thresholds theta = 20, 1 that
the proposition names.  Inner procedures are oracles that return a valid bracket of the promised ratio around the
exact V(a), at the bottom, at the top or at a random place.

    python experiments/eng/twolevel/false_certificate.py            # about a minute
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hetero_literal as HL  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.certified import tables  # noqa: E402
from metricchain_eng.twolevel.tables import LN2  # noqa: E402

OUT = Path(__file__).resolve().parent / "results" / "x015_false_certificate.json"
M, K_IN, U, J_C, TAU = 12, 16, 1.0, 4.0, 10.5


def sigma(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def instance() -> dict:
    """ln V on the outer cube (indexed by the integer whose bits are the outer coordinates) and the facts (a)-(c)."""
    weight = np.array([bin(a).count("1") for a in range(2 ** M)])
    lV_w = np.array([K_IN * math.log(1 - sigma(J_C * (TAU - w)) * (1 - math.exp(-U))) for w in range(M + 1)])
    lV = lV_w[weight]
    lA = float(np.logaddexp.reduce(lV) - M * LN2)
    c = math.log((1 - sigma(-J_C / 2) * (1 - math.exp(-U))) / (1 - sigma(J_C / 2) * (1 - math.exp(-U))))
    edge = float(np.max(np.abs(np.diff(lV_w))))
    spike = float(np.logaddexp.reduce(lV[weight >= 11]) - M * LN2)
    # (TU) for the assumed slope u: V increases with |a|, so the sets {V > s} are the balls D_t = {|a| >= t} around the
    # all-ones point; at each t, E(V - s)_+ with s the largest value outside D_t against s * Xi_u(mu(D_t)), Xi_u from
    # Harper's table (2^-m E_r for the ball of radius r = m - t).  The violation factor is the largest ratio.
    T = tables(M, U)
    tu = {}
    for t in range(1, M + 1):
        s = math.exp(float(np.max(lV[weight < t])))
        excess = float(np.sum(np.exp(lV[weight >= t]) - s) / 2 ** M)
        tu[t] = excess / (s * math.exp(float(T.lE[M - t]) - M * LN2))
    t_star = max(tu, key=tu.get)
    return dict(lV=lV, weight=weight, lA=lA, A=math.exp(lA), jump=K_IN * c, c=c, largest_edge=edge,
                spike_share=math.exp(spike - lA), V_by_weight={w_: math.exp(float(lV_w[w_])) for w_ in (9, 10, 11, 12)},
                tu_violation=tu[t_star], tu_violation_at_weight=t_star, tu_violation_at_tau=tu[math.ceil(TAU)],
                condition_c=dict(kc=K_IN * c, bound=U * (M - TAU + 0.5)))


def run_class(inst: dict, outer_slope: float, design: dict, runs: int, seed: int) -> dict:
    """Runs with the constants and the outer tables of the class in which -ln V is ``outer_slope``-Lipschitz."""
    B = H.make_block([(outer_slope, M), (U, K_IN)]) if outer_slope != U else H.make_block([(U, M + K_IN)])
    j = [i for i, (u, _) in enumerate(B) if u == outer_slope][0]
    C = H.constants(B, H.HDesign(j=j, k=M, **design), math.log(20.0))
    T = tables(M, outer_slope)
    rng = np.random.default_rng(seed)
    psi_ref = np.zeros(2 ** M)                   # psi(a, 0) = 0 for every fibre
    res = dict(outer_slope=outer_slope, x_out=C.x_out, K=C.K, J=C.J, m_max=C.m_max, r_dag=C.r_dag, runs=0, closed=0, invalid=0,
               upper_below_A=0, lower_above_A=0, aborted=0, bad_sampling_certificates=0, too_wide=0)
    factors, points, costs = [], [], []
    t0 = time.time()
    for _ in range(runs):
        for orc in HL.ORACLES:
            r = HL.run_2l_fibres(inst["lV"], psi_ref, 0.0, M, C, T, orc, rng)
            res["runs"] += 1
            costs.append(r["cost"])
            if r["status"] != "closed":
                res["aborted"] += 1
                continue
            res["closed"] += 1
            points.append(r["M"])
            if not r["valid"]:
                res["invalid"] += 1
            if r["lU"] < inst["lA"] - 1e-9:
                res["upper_below_A"] += 1
                factors.append(math.exp(inst["lA"] - r["lU"]))
            if r["lL"] > inst["lA"] + 1e-9:
                res["lower_above_A"] += 1
            if not r["certificates_ok"]:
                res["bad_sampling_certificates"] += 1
            if r["width"] > C.x_out + 1e-9:
                res["too_wide"] += 1
    res.update(seconds=time.time() - t0,
               factor_A_over_upper=dict(median=float(np.median(factors)), min=float(np.min(factors)), max=float(np.max(factors))) if factors else None,
               outer_points=dict(median=float(np.median(points)), min=int(np.min(points)), max=int(np.max(points))) if points else None,
               queries_median=float(np.median(costs)), outer_cube=2 ** M)
    return res


def main() -> int:
    inst = instance()
    facts = {k: v for k, v in inst.items() if k not in ("lV", "weight")}
    print("instance:", json.dumps(facts))
    designs = []
    for theta in (20.0, 1.0):
        d = {k: v for k, v in HL.EXT.items() if k != "name"}
        d["theta"] = theta
        designs.append((f"lam=1, eta=1/2, eta'=1, b=1, theta={theta:g}", d))
    designs.append((HL.BND["name"], {k: v for k, v in HL.BND.items() if k != "name"}))
    rows = []
    for name, d in designs:
        for label, slope, runs in (("assumed class (slope u on every site)", U, 40), ("true class of V (slope k c on the outer sites)", inst["largest_edge"], 8)):
            r = run_class(inst, slope, d, runs, seed=20261126)
            r.update(design=name, tail_function=label)
            rows.append(r)
            f = r["factor_A_over_upper"]
            print(f"{name}; {label}: runs {r['runs']}, closed {r['closed']}, invalid {r['invalid']}, upper end below A in {r['upper_below_A']}"
                  + (f" (A/U median {f['median']:.0f}, {f['min']:.0f} to {f['max']:.0f})" if f else "")
                  + f", sampling certificates false in {r['bad_sampling_certificates']}, aborted {r['aborted']}"
                  + (f", outer points median {r['outer_points']['median']:.0f} ({r['outer_points']['median'] / 2 ** M:.1f} x the outer cube)" if r["outer_points"] else "")
                  + f"  [{r['seconds']:.0f} s]", flush=True)
    OUT.write_text(json.dumps(dict(instance=facts, parameters=dict(m=M, k=K_IN, u=U, J=J_C, tau=TAU), rows=rows), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
