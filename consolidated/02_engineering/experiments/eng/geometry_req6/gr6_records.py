"""Orchestration of the certificates of GEOMETRY-REQ-0006 and the records written to results/.

NOT TRUSTED (search heuristics, choice of inputs, bookkeeping).  The statements come from
gr6_qa_proof.certify / certify_direct / certify_outside, gr6_qb_proof.certify_realisation and the
kernel; the functions here choose what to feed them (approximate maximisers, grid levels,
approximate realisations and pins) and turn their results into JSON.
"""
from __future__ import annotations

import time
from fractions import Fraction as Fr

import numpy as np

import gr6_common as common
import gr6_kernel as kernel
import gr6_model as model
import gr6_qa_proof as QA
import gr6_qb_proof as QB
import gr6_search as search
from gr6_common import box_json, dec_down, enclosure, fr, interval, radians

LEVELS = [8, 10, 12, 14, 16, 18, 20, 22, 24]      # grid levels at which the local step is attempted
HILL_LEVEL = 8                                    # level at which the hill region N is defined

# The candidate realisation for instance A.  The realisations in R^4 with the 16 lengths form a
# two-parameter family; `find_candidate` (random starts on the isotropic cone of the stress matrix)
# finds members of it, and this one is the member with the fourth coordinates of the atoms 4 and 5
# pinned at 9/20 and 3/4 (reached from a member found by the search by continuation in the two
# pins; the largest fourth singular value on the family is about 0.278, where the length system
# is close to singular).  Stored so that the certificate does not depend on a random number
# generator.
CANDIDATE_A = dict(
    pins={(4, 3): Fr(9, 20), (5, 3): Fr(3, 4)},
    start=[[0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [1.35837, 0.93358, 0.0, 0.0], [1.35303, 1.31949, 0.92252, 0.0],
           [0.55151, 1.29721, 1.31567, 0.45], [0.73294, 1.23884, 2.25038, 0.75], [0.56604, 0.32094, 2.61034, 0.74537]],
)


# ------------------------------------------------------------------ (Q-a)
def build(inst):
    """The form H_c of an instance and its approximate maximiser (exact dyadic rationals / pi)."""
    chain = model.Chain(inst["n"])
    form = chain.energy(inst["pairs"], inst["couplings"])
    centre, last_step = search.refine_critical(form, inst["theta_request"])
    return chain, form, centre, last_step


def local_json(loc):
    """Record of a local certificate (concavity_certificate / local_certificate)."""
    if loc is None:
        return None
    out = {"ok": loc["ok"], "failed": loc.get("failed")}
    if loc.get("direction_halfwidths") and None not in loc["direction_halfwidths"]:
        out["direction_halfwidths_tau"] = [fr(x) for x in loc["direction_halfwidths"]]
    if "box" in loc:
        out["B_tau"] = box_json(loc["box"])
        out["B_radians_float"] = [[float(lo) * np.pi, float(hi) * np.pi] for lo, hi in loc["box"]]
    if "hessian_eig_enclosure" in loc:
        out["hessian_spectrum_on_B"] = [interval(lo, hi, 12) for lo, hi in loc["hessian_eig_enclosure"]]
    if loc["ok"]:
        out["critical_point_tau"] = [enclosure(k, 36) for k in loc["K"]]
        out["critical_point_radians"] = [enclosure(radians(k), 36) for k in loc["K"]]
        out["H"] = enclosure(loc["H"], 36)
    return out


def groups_json(groups):
    return [{"sign": g["sign"], "group_box_tau": box_json(g["sides"]),
             "group_box_radians_float": [[float(lo) * np.pi, float(hi) * np.pi] for lo, hi in g["sides"]],
             "boxes": len(g["members"]), "local": local_json(g["local"])} for g in groups]


def stats_json(stats):
    return {str(level): {"examined": st[0], "excluded": st[1]} for level, st in sorted(stats.items())}


def hessian_at(form, K):
    """Enclosure of the spectrum of the Hessian of the form at the point enclosed by K (tau)."""
    P = [kernel.point(t) for t in K]
    nv = len(K)
    hess = [[kernel.ma_eval(model.derivative(model.derivative(form, k), l), P) for l in range(nv)] for k in range(nv)]
    Q = np.linalg.eigh(np.array([[float(x.mid()) for x in row] for row in hess]))[1]
    return [interval(lo, hi, 20) for lo, hi in kernel.sym_eig_enclosure(hess, Q)]


def bnb_json(r, dim, full):
    """Record of a branch and bound: counts, tiling check, optionally the excluded boxes."""
    out = {
        "root_level": 3, "dimension": dim, "levels_attempted": [a["level"] for a in r["attempts"]],
        "per_level": stats_json(r["stats"]),
        "boxes_examined": sum(st[0] for st in r["stats"].values()),
        "boxes_excluded": len(r["excluded"]), "boxes_unresolved": len(r["unresolved"]),
        "tiling_checked": QA.is_partition(r["excluded"] + r["unresolved"]),
        "unresolved": [list(b) for b in sorted(r["unresolved"])],
    }
    if full:
        out["excluded"] = [list(b) for b in sorted(r["excluded"])]
    return out


def plus_local(r):
    """The local certificate around +centre of a certified result."""
    return next(g for g in r["groups"] if g["sign"] == 1)["local"]


def certificate_record(inst, levels=LEVELS, direct=False, log=print):
    """Run the certificate(s) of the global maximum for an instance; returns (record, objects).
    The record is that of certificate R; with direct=True certificate D is run as well and
    recorded under "direct"."""
    t0 = time.perf_counter()
    chain, form, centre, last_step = build(inst)
    t_build = time.perf_counter() - t0
    t0 = time.perf_counter()
    r = QA.certify(form, centre, levels, log=log)
    t_cert = time.perf_counter() - t0
    c_float, info = search.couplings(inst["theta_request"], inst["pairs"])
    rec = {
        "instance": inst["name"], "atoms": inst["n"], "pairs": [list(p) for p in inst["pairs"]],
        "couplings": [fr(c) for c in inst["couplings"]],
        "couplings_unrounded_float": None if c_float is None else [float(x) for x in c_float],
        "theta_request": inst["theta_request"],
        "float_at_theta_request": info | ({} if c_float is None else {
            "H_unrounded_couplings": search.energy_float(inst["theta_request"], inst["pairs"], c_float)}),
        "monomials": len(form), "odd_sine_monomials": len(model.odd_sine_monomials(form)),
        "centre_tau": [fr(c) for c in centre],
        "centre_radians_float": [float(c) * np.pi for c in centre],
        "newton_last_step": last_step,
        "certified": r["certified"], "distinct_maximisers": r.get("distinct"),
        "lower_bound_L": dec_down(r["lower_bound"], 40),
        "branch_and_bound": bnb_json(r, 2, True),
        "groups": groups_json(r["attempts"][-1]["groups"]),
        "seconds": {"build_and_newton": t_build, "certificate_R": t_cert},
    }
    if r["certified"]:
        plus = plus_local(r)
        rec["maximiser_tau"] = [enclosure(k, 36) for k in plus["K"]]
        rec["maximiser_radians"] = [enclosure(radians(k), 36) for k in plus["K"]]
        rec["maximum"] = enclosure(plus["H"], 36)
        rec["hessian_spectrum_at_maximiser"] = hessian_at(form, plus["K"])
        # floating-point cross-check: the couplings are the stress of the framework at the maximiser
        X = model.nerf_chain([float(k.mid()) * np.pi for k in plus["K"]])
        E0 = model.statewise_pairs(inst["n"])
        om, Om, sv = search.stress(X, E0 + list(inst["pairs"]))
        c = np.array([float(x) for x in inst["couplings"]])
        w = om[len(E0):]
        w = w * np.sign(w @ c)
        rec["float_at_maximiser"] = {
            "stress_singular_values_tail": sv[-2:].tolist(),
            "stress_matrix_eigenvalues": np.linalg.eigvalsh(Om * np.sign(om[len(E0):] @ c)).tolist(),
            "stress_on_F_vs_couplings_direction_error": float(np.abs(w / np.linalg.norm(w) - c / np.linalg.norm(c)).max()),
        }
    obj = dict(chain=chain, form=form, centre=centre, result=r)
    if direct:
        t0 = time.perf_counter()
        rd = QA.certify_direct(form, centre, levels, log=log)
        rec["seconds"]["certificate_D"] = time.perf_counter() - t0
        rec["direct"] = {
            "certified": rd["certified"], "distinct_maximisers": rd.get("distinct"),
            "lower_bound_L": dec_down(rd["lower_bound"], 40),
            "branch_and_bound": bnb_json(rd, 4, False),
            "groups": groups_json(rd["attempts"][-1]["groups"]),
        }
        if rd["certified"]:
            plus = plus_local(rd)
            rec["direct"]["maximiser_radians"] = [enclosure(radians(k), 36) for k in plus["K"]]
            rec["direct"]["maximum"] = enclosure(plus["H"], 36)
        obj["direct"] = rd
    return rec, obj


def outside_record(form, centre, other, hill_level=HILL_LEVEL, levels=LEVELS, log=print):
    """Record of gr6_qa_proof.certify_outside (the supremum away from the main maximisers)."""
    t0 = time.perf_counter()
    r = QA.certify_outside(form, centre, other, hill_level, [lv for lv in levels if lv > hill_level], log=log)
    rec = {
        "certified": r["certified"],
        "other_centre_tau": [fr(c) for c in other], "other_centre_radians_float": [float(c) * np.pi for c in other],
        "lower_bound_L2": dec_down(r["lower_bound"], 40),
        "hill_level": hill_level, "hill_boxes": len(r["hill"]),
        "hill_area_fraction": len(r["hill"]) / 4 ** hill_level,
        "hill_bounding_boxes_tau": [box_json(sides) for sides, _ in QA.clusters(r["hill"])],
        "hill": [list(b) for b in sorted(r["hill"])],
        "branch_and_bound": {
            "per_level": stats_json(r["stats"]), "boxes_examined": sum(st[0] for st in r["stats"].values()),
            "boxes_excluded": len(r["excluded"]), "boxes_unresolved": len(r["unresolved"]),
            "tiling_checked": QA.is_partition(r["excluded"] + r["hill"] + r["unresolved"]),
            "excluded": [list(b) for b in sorted(r["excluded"])],
            "unresolved": [list(b) for b in sorted(r["unresolved"])],
        },
        "groups": groups_json(r["attempts"][-1]["groups"]) if r["attempts"] else [],
        "seconds": time.perf_counter() - t0,
    }
    if r["certified"]:
        plus = plus_local(r)
        rec["second_maximiser_radians"] = [enclosure(radians(k), 36) for k in plus["K"]]
        rec["second_maximum"] = enclosure(plus["H"], 36)
        rec["hessian_spectrum_at_second_maximiser"] = hessian_at(form, plus["K"])
    return rec, r


# ------------------------------------------------------------------ (Q-b)
def length_targets(chain, edges, K):
    """Balls containing |x_i - x_j|^2 at every torsion vector in the box K (tau units)."""
    P = [kernel.point(t) for t in K]
    return [kernel.ma_eval(chain.sqdist(i, j), P) for i, j in edges]


def find_candidate(X, edges, Om, trials=300, seed=1, min_sigma4=1e-3, log=print):
    """Search heuristics: a non-flat approximate realisation, the coordinates to pin (the
    best-conditioned square system) and rational values for them (rounded to as few decimals
    as keep the floating-point Newton iteration convergent).  Returns (candidate or None, info)."""
    t0 = time.perf_counter()
    cands = search.realise_4d(X, edges, Om, trials=trials, seed=seed)
    info = {"trials": trials, "converged": len(cands), "sigma4_best": cands[0][0] if cands else None}
    log(f"4D search: {len(cands)} of {trials} starts converged; largest sigma_4 = {info['sigma4_best']}")
    cand = None
    if cands and cands[0][0] >= min_sigma4:
        Y = cands[0][1]
        target = np.array([((X[i] - X[j]) ** 2).sum() for (i, j) in edges])
        pins, info["condition_number"] = search.choose_pins(Y, edges)
        free = [u for u in QB.gauge_unknowns(X.shape[0]) if u not in pins]
        for digits in range(2, 10):
            Z = Y.copy()
            for u in pins:
                Z[u] = round(Y[u], digits)
            Z, res = search.newton_float(Z, edges, free, target)
            if res < 1e-12 and np.abs(Z - Y).max() < 0.05:
                cand = dict(pins={u: Fr(int(round(Y[u] * 10 ** digits)), 10 ** digits) for u in pins}, start=Z.tolist())
                break
    info["seconds"] = time.perf_counter() - t0
    return cand, info


def certify_candidate(n, edges, targets, cand, log=print):
    """Newton refinement of the candidate (approximation), then the trusted certificate.
    Returns (certificate dict, residual of the refinement)."""
    free, f, jac, _ = QB.length_system(n, edges, targets, cand["pins"])
    if len(free) != len(edges):
        return {"ok": False, "failed": "the system is not square"}, None
    z0 = [cand["start"][i][a] for (i, a) in free]
    centre, resid = search.refine_square(free, f, jac, z0)
    log(f"Newton refinement: max |f| at the centre = {resid:.3g}")
    cert = QB.certify_realisation(n, edges, targets, cand["pins"], dict(zip(free, centre)))
    return cert, resid


def realisation_record(n, edges, targets, cert, cand):
    rec = {"certified": cert["ok"], "failed": cert.get("failed"),
           "pins": {f"y_{i}[{a}]": fr(v) for (i, a), v in cand["pins"].items()}}
    if not cert["ok"]:
        return rec
    Y = cert["Y"]
    rec["configuration"] = [[enclosure(Y[i][a], 30) for a in range(4)] for i in range(n)]
    rec["configuration_float"] = [[float(Y[i][a].mid()) for a in range(4)] for i in range(n)]
    rec["max_coordinate_radius"] = float(max(Y[i][a].rad() for i in range(n) for a in range(4)))
    rec["singular_values"] = [interval(lo, hi, 20) for lo, hi in cert["sigma"]]
    rec["singular_value_intervals_disjoint"] = cert["sigma_disjoint"]
    rec["sigma_4_lower_bound"] = dec_down(cert["sigma_min_lower"], 20)
    rec["target_radius_max"] = float(max(t.rad() for t in targets))
    rec["squared_lengths"] = {f"{i}-{j}": enclosure(QB.sq_length(Y, i, j), 30) for i, j in edges}
    return rec


def realisation_pipeline(n, edges, targets, X, forced, log, trials=60):
    """The (Q-b) pipeline on an arbitrary framework: the search, then the certificate for the
    candidate it proposes (if any); the candidates in `forced` (name -> candidate) are submitted
    to the certificate as well."""
    _, Om, sv = search.stress(X, edges)
    out = {"stress_eigenvalues_float": np.linalg.eigvalsh(Om).tolist(),
           "stress_singular_values_tail": sv[-2:].tolist()}
    cand, info = find_candidate(X, edges, Om, trials=trials, log=log)
    out["search"] = info
    out["search_candidate"] = None
    out["certified"] = False
    if cand is not None:
        cert, resid = certify_candidate(n, edges, targets, cand, log=log)
        out["search_candidate"] = realisation_record(n, edges, targets, cert, cand)
        out["certified"] = cert["ok"]
    if forced:
        out["forced_candidates"] = {}
        for name, c in forced.items():
            cert, resid = certify_candidate(n, edges, targets, c, log=log)
            out["forced_candidates"][name] = dict(realisation_record(n, edges, targets, cert, c), newton_residual=resid)
    return out


def flat_candidate(X, pins):
    """The flat configuration [X, 0] as a candidate with the given coordinates pinned at their
    values in it (exact rationals of the floats)."""
    Y = np.hstack([X, np.zeros((X.shape[0], 1))])
    return dict(pins={u: Fr(float(Y[u])) for u in pins}, start=Y.tolist())


def lifted_candidate(X, edges, pins):
    """A candidate with coordinates pinned at prescribed values (fourth coordinates away from
    zero): a least-squares solution of the square system started at [X, 0].  Returns (candidate,
    max residual), the residual being positive when no realisation exists."""
    from scipy.optimize import least_squares

    n = X.shape[0]
    Y = np.hstack([X, np.zeros((n, 1))])
    for u, v in pins.items():
        Y[u] = float(v)
    free = [u for u in QB.gauge_unknowns(n) if u not in pins]
    target = np.array([((X[i] - X[j]) ** 2).sum() for (i, j) in edges])

    def res(z):
        Z = Y.copy()
        for k, u in enumerate(free):
            Z[u] = z[k]
        return search.residual_jacobian(Z, edges, free, target)[0]

    sol = least_squares(res, np.array([Y[u] for u in free]), xtol=1e-14, ftol=1e-14, gtol=1e-14)
    for k, u in enumerate(free):
        Y[u] = sol.x[k]
    return dict(pins=dict(pins), start=Y.tolist()), float(np.abs(sol.fun).max())
