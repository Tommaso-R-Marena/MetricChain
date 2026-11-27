"""Validation controls of GEOMETRY-REQ-0006 (run by run_controls.py and by the tests).

NOT TRUSTED (orchestration).  The controls run the same trusted functions as the certificates on
inputs for which the expected outcome is known:

(Q-a)
  A1  instance A, the runner-up maximum claimed to be the global one: must NOT be certified
      (and a point with a larger value is exhibited);
  A2  instance A with the couplings of the wrong sign (the conformation is then a minimiser):
      must NOT be certified;
  A3  the control conformation with a positive semidefinite stress: (Q-a) MUST be certified
      (a universally rigid framework satisfying the conic condition is second-moment rigid).
  (The request's control "find the second local maximum of instance A" is the certificate
  `outside` of run_qa.py, recorded in results/qa_instance_A.json.)
(Q-b)
  B1  the control conformation with a positive semidefinite stress: no realisation of affine
      dimension 4 exists (universal rigidity); the search must find none and the Krawczyk test
      must fail, both at the flat realisation and with the fourth coordinates pinned away from 0;
  B2  instance A with the fourth coordinates pinned at 0 (the flat realisation X^ itself): must NOT
      be certified (singular Jacobian; sigma_4 = 0);
  B3  six atoms, F = {(0,3), (1,4), (2,5), (0,5)} (the graph of hierarchy_example.py), a conformation
      with a semidefinite stress: must NOT be certified;
  B4  the same graph at a conformation with an indefinite stress: MUST be certified.
"""
from __future__ import annotations

from fractions import Fraction as Fr

import numpy as np

import gr6_common as common
import gr6_kernel as kernel
import gr6_model as model
import gr6_qa_proof as QA
import gr6_records as records
import gr6_search as search
from gr6_common import box_json, dec_down, enclosure, fr

PAIRS_6 = [(0, 3), (1, 4), (2, 5), (0, 5)]
# conformations of the 6-atom chain (torsions / pi, exact rationals), from our own random search
SIX_SEMIDEFINITE = [Fr(2740, 10000), Fr(-3504, 10000), Fr(2869, 10000)]     # stress eigenvalues (0.85, 1) x scale
SIX_INDEFINITE = [Fr(3257, 10000), Fr(-4494, 10000), Fr(-7241, 10000)]      # stress eigenvalues (-0.87, 1) x scale
PINS = {(4, 3): Fr(9, 20), (5, 3): Fr(3, 4)}                                # the pins of instance A


def witness_above(form, boxes, value):
    """A point of the torus with H > value, sought at the centres of the given boxes of the
    (theta_1, theta_2)-plane with the end torsions at the polar angles of V and W (floating
    point), then evaluated rigorously.  Returns (torsions / pi, lower bound of H) or None."""
    red = QA.reduce_ends(form)
    for level, j1, j2 in boxes:
        (a1, b1), (a2, b2) = QA.grid_arc(level, j1), QA.grid_arc(level, j2)
        t1, t2 = (a1 + b1) / 2, (a2 + b2) / 2
        P = [None, kernel.point(t1), kernel.point(t2), None]
        v = [float(kernel.ma_eval(red[k], P).mid()) for k in ("V1", "V2", "W1", "W2")]
        t0 = Fr(int(round(np.arctan2(v[1], v[0]) / np.pi * 2 ** 40)), 2 ** 40)
        t3 = Fr(int(round(np.arctan2(v[3], v[2]) / np.pi * 2 ** 40)), 2 ** 40)
        tau = [t0, t1, t2, t3]
        h = kernel.ma_eval(form, [kernel.point(t) for t in tau])
        if h > value:
            return tau, h.lower()
    return None


def control_a1(log, start=None, starts=200):
    """Runner-up claimed as the global maximiser.  The runner-up is found by a multi-start search
    (or refined from the approximate torsions `start`, if given)."""
    _, form, centre, _ = records.build(common.INSTANCE_A)
    if start is None:
        start = search.local_maxima(form, starts=starts, seed=0)[1][1]
    other, _ = search.refine_critical(form, start)
    r = QA.certify(form, other, [6, 8], log=log)
    claimed = kernel.ma_eval(form, [kernel.point(t) for t in other])
    outsiders = [b for g in r["attempts"][-1]["groups"] if g["sign"] is None for b in g["members"]]
    w = witness_above(form, outsiders, claimed)
    return {
        "claim": "the runner-up critical point of instance A is the global maximiser",
        "claimed_centre_radians_float": [float(c) * np.pi for c in other],
        "claimed_value": enclosure(claimed, 30),
        "certified": r["certified"], "expected_certified": False,
        "unresolved_boxes_at_level_8": len(r["unresolved"]),
        "unresolved_boxes_away_from_the_claimed_maximiser": len(outsiders),
        "groups": [{"sign": g["sign"], "boxes": len(g["members"]), "group_box_tau": box_json(g["sides"])}
                   for g in r["attempts"][-1]["groups"]],
        "refutation": None if w is None else {"theta_over_pi": [fr(t) for t in w[0]], "H_lower_bound": dec_down(w[1], 30)},
        "passed": (not r["certified"]) and w is not None,
    }


def control_a2(log):
    """Couplings of the wrong sign."""
    inst = dict(common.INSTANCE_A, name="A-wrong-sign", couplings=[-c for c in common.INSTANCE_A["couplings"]])
    _, form, centre, _ = records.build(inst)
    r = QA.certify(form, centre, [5, 6], log=log)
    return {
        "claim": "the conformation of instance A maximises H_c for the couplings -c",
        "certified": r["certified"], "expected_certified": False,
        "unresolved_boxes_at_level_6": len(r["unresolved"]), "boxes_of_level_6": 4 ** 6,
        "groups": len(r["attempts"][-1]["groups"]),
        "passed": not r["certified"],
    }


def control_psd(log, trials=60):
    """A3 and B1: the control conformation with a semidefinite stress (same graph as instance A)."""
    inst = common.CONTROL_PSD
    n, edges = inst["n"], model.statewise_pairs(inst["n"]) + inst["pairs"]
    qa, obj = records.certificate_record(inst, log=log)
    a3 = {k: qa.get(k) for k in ("couplings", "theta_request", "centre_radians_float", "certified", "maximum",
                                 "maximiser_radians", "hessian_spectrum_at_maximiser", "float_at_theta_request",
                                 "float_at_maximiser")}
    a3["boxes_examined"] = qa["branch_and_bound"]["boxes_examined"]
    a3["expected_certified"] = True
    a3["passed"] = qa["certified"]
    if not qa["certified"]:
        return a3, {"certified": False, "expected_certified": False, "passed": False,
                    "failed": "no enclosure of the maximiser of the control"}
    K = records.plus_local(obj["result"])["K"]
    targets = records.length_targets(obj["chain"], edges, K)
    X = model.nerf_chain([float(k.mid()) * np.pi for k in K])
    lifted, ls_res = records.lifted_candidate(X, edges, PINS)
    b1 = records.realisation_pipeline(n, edges, targets, X,
                                      {"flat": records.flat_candidate(X, list(PINS)), "lifted": lifted}, log, trials)
    b1["lifted_least_squares_residual"] = ls_res
    b1["expected_certified"] = False
    b1["passed"] = (not b1["certified"]) and not any(c["certified"] for c in b1["forced_candidates"].values())
    return a3, b1


def control_b2(log):
    """Instance A with the fourth coordinates pinned at zero."""
    inst = common.INSTANCE_A
    n, edges = inst["n"], model.statewise_pairs(inst["n"]) + inst["pairs"]
    qa, obj = records.certificate_record(inst, log=lambda *a: None)
    K = records.plus_local(obj["result"])["K"]
    targets = records.length_targets(obj["chain"], edges, K)
    X = model.nerf_chain([float(k.mid()) * np.pi for k in K])
    cand = records.flat_candidate(X, list(PINS))
    cert, resid = records.certify_candidate(n, edges, targets, cand, log=log)
    rec = records.realisation_record(n, edges, targets, cert, cand)
    return dict(rec, claim="the flat realisation X^ of instance A, fourth coordinates of the atoms 4 and 5 pinned at 0",
                expected_certified=False, passed=not cert["ok"])


def control_six(taus, expected, log, trials=60):
    """B3 / B4: the 6-atom chain with F = PAIRS_6 at the conformation pi * taus."""
    n, edges = 6, model.statewise_pairs(6) + PAIRS_6
    chain = model.Chain(n)
    targets = records.length_targets(chain, edges, [kernel.ball(t) for t in taus])
    X = model.nerf_chain([float(t) * np.pi for t in taus])
    out = records.realisation_pipeline(n, edges, targets, X, None, log, trials)
    out["torsions_over_pi"] = [fr(t) for t in taus]
    out["expected_certified"] = expected
    out["passed"] = out["certified"] == expected
    return out


def run_all(log=print):
    rec = {"request": "GEOMETRY-REQ-0006 (validation controls)", "precision_bits": kernel.PREC}
    rec["A1_runner_up_claimed_global"] = control_a1(log)
    rec["A2_wrong_sign"] = control_a2(log)
    rec["A3_semidefinite_stress_Qa"], rec["B1_semidefinite_stress_Qb"] = control_psd(log)
    rec["B2_flat_instance_A"] = control_b2(log)
    rec["B3_six_atoms_semidefinite"] = control_six(SIX_SEMIDEFINITE, False, log)
    rec["B4_six_atoms_indefinite"] = control_six(SIX_INDEFINITE, True, log)
    rec["all_passed"] = all(v["passed"] for v in rec.values() if isinstance(v, dict))
    return rec
