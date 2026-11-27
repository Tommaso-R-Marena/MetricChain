"""Labelled synthetic instances for testing software that claims to reconstruct conformations
or ensembles from distance-type data (docs/geometry/BENCHMARKS.md).

Every instance is an abstract chain (unit bonds, one bond angle; no sequence, no chemistry) with
  * the data a tool would receive,
  * the ground truth (states, weights),
  * a label saying what is TRUE of the instance -- uniquely determined / not determined /
    determined only locally / determined but with no efficient certificate known / ill-conditioned /
    outside the assumptions -- with the evidence level of the label (P, P-exact, N, C), and
  * where the label says "not determined": an explicit second solution with the same data.
The script re-derives every label it can with the division's own tools and fails if one does not
hold.  It is cheap (about a minute); nothing here is a benchmark RUN -- executing and judging
software on these instances is the Engineering division's task.

Usage:  benchmark_instances.py            self-check and summary table
        benchmark_instances.py --write    also (re)write benchmark_suite/*.json and MANIFEST.json
"""
import hashlib
import json
import os
import sys

import numpy as np
from scipy.optimize import linprog

import demix as DM
import demix4 as D4
import hinge_pairs as HP
import label_patterns as LP
from geomlib import chain, edm, kabsch_rmsd
from local_data_upper import band_pairs, sharp_constants, csig3

HERE = os.path.dirname(os.path.abspath(__file__))
THETA = np.deg2rad(111.0)


# ---------------------------------------------------------------------------------- helpers
def mixture_data(Xs, w):
    return sum(wk * edm(X) for wk, X in zip(w, Xs))


def chain_spec(theta):
    return {"bond_length": 1.0, "bond_angle_deg": float(np.rad2deg(theta)),
            "second_neighbour_distance": float(np.sqrt(2 - 2 * np.cos(theta))),
            "statewise_constraints": "every state has unit bonds |x_i - x_{i+1}| and the stated distance |x_i - x_{i+2}|"}


def constraints_ok(X, theta, tol=1e-8):
    n = len(X)
    b = max(abs(np.linalg.norm(X[i + 1] - X[i]) - 1) for i in range(n - 1))
    c = max(abs(np.linalg.norm(X[i + 2] - X[i]) - np.sqrt(2 - 2 * np.cos(theta))) for i in range(n - 2))
    return max(b, c) < tol


def dihedrals(X):
    out = []
    for i in range(len(X) - 3):
        b0, b1, b2 = X[i + 1] - X[i], X[i + 2] - X[i + 1], X[i + 3] - X[i + 2]
        n1, n2 = np.cross(b0, b1), np.cross(b1, b2)
        m1 = np.cross(n1, b1 / np.linalg.norm(b1))
        out.append(np.arctan2(m1 @ n2, n1 @ n2))
    return np.array(out)


def linear_certificate(M, theta):
    """The conic (linear) certificate of DEMIX in exact-data mode: (certified, K, nullity or reason)."""
    n = len(M)
    edges, lengths = DM.chain_edges(n, theta=theta)
    out = DM.demix(M, edges, lengths)
    return out


def jacobian_rank_two_states(Xs, w, theta, h=1e-6, tol=1e-6):
    """Rank of the derivative of (torsions of both states, weight) -> M: equal to the number of
    parameters iff the ensemble is locally identifiable within two-state ensembles."""
    n = len(Xs[0])
    t0 = np.concatenate([-dihedrals(Xs[0]), -dihedrals(Xs[1]), [w[0]]])

    def data(p):
        X1, X2 = chain(n, p[:n - 3], theta=theta), chain(n, p[n - 3:2 * (n - 3)], theta=theta)
        return (p[-1] * edm(X1) + (1 - p[-1]) * edm(X2))[np.triu_indices(n, 1)]
    base = data(t0)
    # the chain builder's sign convention for torsions: accept whichever sign reproduces the data
    ref = mixture_data(Xs, w)[np.triu_indices(n, 1)]
    if np.abs(base - ref).max() > 1e-8:
        t0 = np.concatenate([dihedrals(Xs[0]), dihedrals(Xs[1]), [w[0]]])
        base = data(t0)
    assert np.abs(base - ref).max() < 1e-8, "torsions do not rebuild the states"
    J = np.array([(data(t0 + h * e) - data(t0 - h * e)) / (2 * h) for e in np.eye(len(t0))]).T
    s = np.linalg.svd(J, compute_uv=False)
    return int((s > tol * s[0]).sum()), len(t0)


def inst(iid, category, title, theta, Xs, w, data, truth, expected, evidence, reference, extra=None):
    d = {"id": iid, "category": category, "title": title, "chain": chain_spec(theta),
         "n_points": int(len(Xs[0])), "n_states": int(len(Xs)),
         "truth": {"states": [np.asarray(X).tolist() for X in Xs], "weights": [float(x) for x in w]},
         "data": data, "label": truth, "expected_behaviour_of_a_correct_tool": expected,
         "evidence_for_label": evidence, "reference": reference}
    if extra:
        d.update(extra)
    return d


def averaged_data(Xs, w):
    return {"kind": "ensemble-averaged squared distances, all pairs, exact",
            "matrix": mixture_data(Xs, w).tolist()}


# ---------------------------------------------------------------------------------- instances
def build(quick=False):
    I, checks = [], []

    def check(name, cond, note=""):
        checks.append((name, bool(cond), note))

    # ---- A: uniquely determined, linear certificate -----------------------------------
    for iid, K, n, seed in (("A1", 2, 12, 11), ("A2", 2, 16, 12), ("A3", 3, 23, 13)):
        rng = np.random.default_rng(seed)
        w = rng.dirichlet(np.ones(K) * 4)
        Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(K)]
        M = mixture_data(Xs, w)
        out = linear_certificate(M, THETA)
        err = DM.match_error(Xs, w, out) if out["ok"] else (np.inf, np.inf)
        check(f"{iid}: linear certificate and recovery", out["ok"] and err[0] < 1e-6 and err[1] < 1e-6, f"RMSD {err[0]:.1e}")
        I.append(inst(iid, "A uniquely determined; linear certificate",
                      f"{K} generic states, {n} points (at or above the conic threshold)", THETA, Xs, w, averaged_data(Xs, w),
                      {"globally_identifiable": True, "linear_certificate": True, "recoverable_by_linear_algebra": True},
                      "report K, the states up to congruence (mirror images count as the same shape) and the weights; "
                      "report the certificate (nullity K - 1 of the linear system)",
                      "P for this instance (Theorem B with the certificate computed here in floating point: nullity "
                      f"{out['certificate']['nullity']}, smallest non-trivial singular value {out['certificate']['smallest_nontrivial_sv']:.2e})",
                      "ENSEMBLE_RIGIDITY.md Theorems B, C; Algorithm DEMIX; Lean mixture_identifiable_stacked"))

    # ---- B: uniquely determined, only the quartic certificate --------------------------
    cases = [("B1", 2, 11, 29, "h_4 = K"), ("B2", 2, 10, 3, "h_4 = K + dim L (structural point)")]
    if not quick:
        cases.append(("B3", 3, 17, 68, "h_4 = K"))
    for iid, K, n, seed, cert in cases:
        rng = np.random.default_rng(seed)
        w = rng.dirichlet(np.ones(K) * 4)
        Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(K)]
        M = mixture_data(Xs, w)
        lin = linear_certificate(M, THETA)
        out4, info = D4.demix4(M, theta=THETA, rng=np.random.default_rng(seed + 100))
        m = info["dim_L"]
        if iid == "B2":
            check(f"{iid}: linear certificate fails, quartic defect is K + dim L", (not lin["ok"]) and info["HF"] == K + m,
                  f"h_4 = {info['HF']}, dim L = {m}")
        else:
            rec = out4 is not None and max(min(kabsch_rmsd(X, Y) for Y in out4[0]) for X in Xs) < 1e-5
            check(f"{iid}: linear certificate fails, quartic certificate holds, states recovered", (not lin["ok"]) and info["HF"] == K and rec,
                  f"h_4 = {info['HF']}")
        I.append(inst(iid, "B uniquely determined; quartic certificate only",
                      f"{K} generic states, {n} points (below the conic threshold): {cert}", THETA, Xs, w, averaged_data(Xs, w),
                      {"globally_identifiable": True, "linear_certificate": False, "quartic_certificate": cert,
                       "recoverable_by_linear_algebra": iid != "B2"},
                      "a tool limited to the linear certificate must answer 'not certified' (not 'not unique'); a tool with the "
                      "quartic certificate may certify and, for h_4 = K, recover the states",
                      "P-exact for generic chains at two other bond angles (Theorem I'); for this instance N (floating point: "
                      f"h_4 = {info['HF']}) -- floating point is not reliable for this rank (DEAD_ENDS DG-23)",
                      "ENSEMBLE_RIGIDITY.md section 6.2, Proposition 6.2, Theorem I'; exact_demix4.py"))

    # ---- C: not determined (explicit second solutions) -------------------------------
    d = np.load(os.path.join(HERE, "review1", "alt_K2_n8_s2.npz"))
    Xs, w, S, v = list(d["Xs"]), d["w"], list(d["states"]), d["weights"]
    th8 = np.arccos(1 - np.mean([np.linalg.norm(Xs[0][i + 2] - Xs[0][i]) ** 2 for i in range(6)]) / 2)
    gap = np.abs(mixture_data(Xs, w) - mixture_data(S, v)).max()
    far = min(min(kabsch_rmsd(X, Y) for X in Xs) for Y in S)
    rank, npar = jacobian_rank_two_states(Xs, w, th8)
    check("C1/D1: nine other chains have the same averaged data", gap < 1e-10 and all(constraints_ok(Y, th8) for Y in S) and far > 1e-2 and v.min() > 0,
          f"max data difference {gap:.1e}; nearest competitor state at RMSD {far:.2f}")
    check("C1/D1: locally identifiable within two-state ensembles", rank == npar, f"Jacobian rank {rank} of {npar}")
    I.append(inst("C1", "C not determined; D determined only locally",
                  "2 states, 8 points: a 9-state ensemble of other chains has the same averaged data", th8, Xs, w, averaged_data(Xs, w),
                  {"globally_identifiable": False, "locally_identifiable_within_K_states": True, "linear_certificate": False},
                  "must NOT report the two states as the unique ensemble; acceptable: 'not certified', or a description of "
                  "the non-uniqueness; a search restricted to two-state ensembles will find the truth and must not present "
                  "that as identification among all ensembles",
                  f"exact for this instance up to rounding: the second solution is given (data agree to {gap:.0e}); local "
                  f"identifiability N (Jacobian rank {rank} = number of parameters), P-exact generically (Theorem H)",
                  "ENSEMBLE_RIGIDITY.md section 5.5, Theorem H; the competing ensemble is the internal referee's (review1/)",
                  {"second_solution": {"states": [np.asarray(Y).tolist() for Y in S], "weights": [float(x) for x in v]}}))

    # one differing torsion (one hinge): never determined
    rng = np.random.default_rng(21)
    n, h = 14, 5
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    phi = np.array([t1[h], t1[h] + 1.7])
    w = np.array([0.35, 0.65])
    mom = w[0] * np.exp(1j * phi[0]) + w[1] * np.exp(1j * phi[1])
    psi = np.angle(mom) + np.array([1, -1]) * np.arccos(abs(mom))

    def with_torsion(val):
        t = t1.copy()
        t[h] = val
        return chain(n, t, theta=THETA)
    Xs, S, v = [with_torsion(p) for p in phi], [with_torsion(p) for p in psi], np.array([0.5, 0.5])
    gap = np.abs(mixture_data(Xs, w) - mixture_data(S, v)).max()
    far = min(min(kabsch_rmsd(X, Y) for X in Xs) for Y in S)
    check("C2: two states that differ in one torsion are not determined", gap < 1e-10 and far > 1e-2, f"data difference {gap:.1e}, RMSD {far:.2f}")
    I.append(inst("C2", "C not determined", "2 states that differ in one torsion (one hinge)", THETA, Xs, w, averaged_data(Xs, w),
                  {"globally_identifiable": False, "linear_certificate": False,
                   "what_is_determined": "the two rigid parts and the mean of (cos, sin) of the hinge angle"},
                  "must NOT report two definite states; a correct output is the hinge position, the rigid parts and the first "
                  "circular moment of the hinge angle",
                  "P (the data are affine in the mean of (cos, sin) of the hinge angle; a second solution is given)",
                  "HINGE_ENSEMBLES.md Theorem M (a) (first shown by the Science division, SCI-RES-0029)",
                  {"second_solution": {"states": [Y.tolist() for Y in S], "weights": v.tolist()}}))

    # two half-turn hinges: not determined
    n, hinges, w = 14, [3, 7], np.array([0.37, 0.63])
    t1 = np.random.default_rng(41).uniform(-np.pi, np.pi, n - 3)
    t2 = t1.copy()
    t2[hinges[0]] += np.pi
    t2[hinges[1]] += np.pi
    X1, X2 = chain(n, t1, theta=THETA), chain(n, t2, theta=THETA)
    cand, _, _ = HP.cube_candidates(X1, X2, hinges)
    keys = list(cand)
    M = mixture_data([X1, X2], w)
    iu = np.triu_indices(n, 1)
    A = np.vstack([np.array([edm(cand[k])[iu] for k in keys]).T, np.ones(8)])
    cost = np.array([0.0 if k in ((0, 0, 0), (1, 1, 1)) else -1.0 for k in keys])
    r = linprog(cost, A_eq=A, b_eq=np.append(M[iu], 1.0), bounds=(0, None), method="highs")
    S = [cand[k] for k, x in zip(keys, r.x) if x > 1e-9]
    v = np.array([x for x in r.x if x > 1e-9])
    gap = np.abs(M - mixture_data(S, v)).max()
    check("C3: two half-turn hinges are not determined", r.status == 0 and -r.fun > 0.5 and gap < 1e-9 and all(constraints_ok(Y, THETA) for Y in S),
          f"weight {-r.fun:.2f} on other chains, data difference {gap:.1e}")
    I.append(inst("C3", "C not determined", "2 states that differ by half-turns at two hinges", THETA, [X1, X2], w, averaged_data([X1, X2], w),
                  {"globally_identifiable": False, "linear_certificate": False},
                  "must NOT report the two states as unique: an ensemble of mirrored assemblies has the same data",
                  "P (Science division, Proposition R22-1 (d); our Theorem M (b)); the second solution is given",
                  "HINGE_ENSEMBLES.md Theorem M; SCI-REV-0021",
                  {"second_solution": {"states": [Y.tolist() for Y in S], "weights": v.tolist()}}))

    # no statewise constraints: nothing is determined
    rng = np.random.default_rng(22)
    X = chain(8, rng.uniform(-np.pi, np.pi, 5), theta=THETA)
    Xc = X - X.mean(0)
    S = [np.column_stack([np.sqrt(3) * Xc[:, a], np.zeros(8), np.zeros(8)]) for a in range(3)]
    gap = np.abs(edm(X) - mixture_data(S, [1 / 3] * 3)).max()
    check("C4: without statewise constraints a single conformation has the data of three collinear ones", gap < 1e-10, f"data difference {gap:.1e}")
    I.append(inst("C4", "C not determined; G outside the assumptions (no statewise constraints supplied)",
                  "one conformation; the tool is NOT told the bond lengths", THETA, [X], [1.0],
                  {"kind": "ensemble-averaged squared distances, all pairs, exact; NO statewise constraints supplied",
                   "matrix": edm(X).tolist()},
                  {"globally_identifiable": False, "reason": "without statewise constraints averaged squared distances determine no ensemble"},
                  "must refuse to report a structure or an ensemble",
                  "P (Proposition 3.1); the second solution is given",
                  "ENSEMBLE_RIGIDITY.md section 3",
                  {"second_solution": {"states": [Y.tolist() for Y in S], "weights": [1 / 3] * 3}}))

    # single conformation, distances of separation <= 3: a reflected tail
    rng = np.random.default_rng(23)
    X = chain(20, rng.uniform(0.7, 2.4, 17) * rng.choice([-1, 1], 17), theta=THETA)
    i = 8
    nrm = np.cross(X[i + 1] - X[i], X[i + 2] - X[i])
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 3:] = X[i + 3:] - 2 * np.outer((X[i + 3:] - X[i]) @ nrm, nrm)
    d3 = max(abs(np.linalg.norm(X[j] - X[k]) - np.linalg.norm(Y[j] - Y[k])) for j, k in band_pairs(20, 3))
    d4 = max(abs(np.linalg.norm(X[j] - X[k]) - np.linalg.norm(Y[j] - Y[k])) for j, k in band_pairs(20, 4))
    check("C5: a reflected tail keeps all distances of separation <= 3", d3 < 1e-10 and d4 > 1e-2 and kabsch_rmsd(X, Y) > 0.1,
          f"separation <= 3: {d3:.1e}; separation 4 changes by {d4:.2f}; RMSD {kabsch_rmsd(X, Y):.2f}")
    I.append(inst("C5", "C not determined (separation <= 3); A determined (separation <= 4)",
                  "one conformation, 20 points; distances between points at sequence separation at most 3, or at most 4", THETA, [X], [1.0],
                  {"kind": "distances of one conformation for pairs of sequence separation <= 3 (variant a) or <= 4 (variant b), exact",
                   "pairs_a": band_pairs(20, 3), "distances_a": [float(np.linalg.norm(X[j] - X[k])) for j, k in band_pairs(20, 3)],
                   "pairs_b": band_pairs(20, 4), "distances_b": [float(np.linalg.norm(X[j] - X[k])) for j, k in band_pairs(20, 4)]},
                  {"variant_a_globally_identifiable": False, "variant_b_globally_identifiable": True,
                   "note": "2^17 configurations share the data of variant a (one mirror choice per window)"},
                  "variant a: must not report a unique conformation (up to congruence); variant b: unique",
                  "P (variant a: the second solution is given; variant b: Theorem L, exact data)",
                  "LOCAL_DATA_STABILITY.md Theorem L, Proposition L0",
                  {"second_solution_variant_a": {"states": [Y.tolist()], "weights": [1.0]}}))

    # ---- label patterns: only a subset of the points is observed -----------------------
    S = sorted(list(range(20, 32)) + [0, 7, 13, 40, 47, 55, 59])
    Xs, w = LP.random_mixture(2, 60, seed=71)
    nul, c = LP.conic_nullity(Xs, w, S)
    cert, rmsd = LP.demix_pattern(Xs, w, S)
    check("A4: an anchor stretch of 12 labelled points certifies all 19 labelled sites", cert and rmsd < 1e-6 and nul == 1 and c == 21, f"c = {c}, RMSD {rmsd:.1e}")
    I.append(inst("A4", "A uniquely determined; linear certificate (partial labelling)",
                  "2 generic states, 60 points of which 19 are observed: 12 consecutive ones and 7 scattered", THETA, Xs, w,
                  {"kind": "ensemble-averaged squared distances among the labelled sites only, exact", "labelled_sites": S,
                   "matrix": sum(wk * edm(X[S]) for wk, X in zip(w, Xs)).tolist()},
                  {"globally_identifiable": "the ensemble of configurations of the 19 labelled sites: yes; the unlabelled points: not determined",
                   "linear_certificate": True, "constrained_labelled_pairs": c, "needed": LP.needed(2)},
                  "report the two configurations of the labelled sites (all 19, including the 7 isolated ones) and the weights, with the "
                  "certificate; must not report positions of unlabelled points as determined",
                  "P for this instance (Theorem B for the labelled constraint graph, certificate computed in floating point)",
                  "LABEL_PATTERNS.md Theorems P1, P2"))
    r = LP.second_solution(n=41, gap=4, eps=0.03, seed=0)
    check("C6: with labels every fourth point two other chains have the same labelled data",
          r["fit_residual"] < 1e-9 and r["data_difference"] < 1e-9 and r["moved"] > 1e-2 and all(constraints_ok(Y, THETA) for Y in r["second"]),
          f"data difference {r['data_difference']:.1e}, labelled sites moved by RMSD {r['moved']:.2f}")
    I.append(inst("C6", "C not determined (sparse labels)", "2 states, 41 points of which every fourth is observed (11 labelled sites)", THETA,
                  r["truth"], r["weights"],
                  {"kind": "ensemble-averaged squared distances among the labelled sites only, exact", "labelled_sites": r["S"],
                   "matrix": sum(wk * edm(X[r["S"]]) for wk, X in zip(r["weights"], r["truth"])).tolist()},
                  {"globally_identifiable": False, "locally_identifiable_within_K_states": False, "constrained_labelled_pairs": 0,
                   "reason": "no two labelled sites are at chain separation 1 or 2: no statewise equality constraint among the observed "
                             "points; the two-state ensembles with these data form a family of dimension at least 9"},
                  "must not report two definite configurations of the labelled sites",
                  "P (Proposition P3); the second solution is given",
                  "LABEL_PATTERNS.md Proposition P3",
                  {"second_solution": {"states": [Y.tolist() for Y in r["second"]], "weights": [float(x) for x in r["weights"]]}}))

    # ---- E: determined, but no efficient certificate known ---------------------------
    for iid, K, n, seed in (("E1", 2, 9, 31), ("E2", 3, 15, 32)):
        rng = np.random.default_rng(seed)
        w = rng.dirichlet(np.ones(K) * 4)
        Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(K)]
        lin = linear_certificate(mixture_data(Xs, w), THETA)
        check(f"{iid}: the linear certificate fails", not lin["ok"], lin.get("reason", ""))
        I.append(inst(iid, "E determined (numerical evidence or conjecture); no efficient certificate known",
                      f"{K} generic states, {n} points", THETA, Xs, w, averaged_data(Xs, w),
                      {"globally_identifiable": "numerical evidence" if K == 2 else "numerical evidence and conjecture",
                       "linear_certificate": False, "quartic_certificate": False},
                      "'not certified' is the correct output of any tool we know how to build; a tool that claims a certificate "
                      "here must exhibit it; a tool that returns the truth without a certificate has not identified it",
                      "N (two states at 9 points: identified in 24 instances by exhaustive numerical search for other "
                      "solutions; three states at 14 and 15 points: no other solutions found) -- not a theorem",
                      "ENSEMBLE_RIGIDITY.md sections 5.2, 5.5, 6.2; PROOF_OBLIGATIONS O-2, O-15"))

    # ---- F: ill-conditioned ----------------------------------------------------------
    rng = np.random.default_rng(51)
    n = 12
    t = rng.uniform(-np.pi, np.pi, n - 3)
    for iid, eps in (("F1a", 1e-1), ("F1b", 1e-3)):
        Xs = [chain(n, t, theta=THETA), chain(n, t + eps * rng.normal(size=n - 3), theta=THETA)]
        w = np.array([0.4, 0.6])
        out = linear_certificate(mixture_data(Xs, w), THETA)
        sv = out["certificate"]["smallest_nontrivial_sv"] if "certificate" in out else None
        lam = out["certificate"]["lambda_min"] if "certificate" in out else None
        I.append(inst(iid, "F ill-conditioned", f"2 states that differ by torsion changes of size {eps:g}, 12 points", THETA, Xs, w, averaged_data(Xs, w),
                      {"globally_identifiable": True, "conditioning": {"smallest_eigenvalue_of_the_stack": lam, "smallest_non_trivial_singular_value": sv,
                                                                       "rmsd_between_states": float(kabsch_rmsd(*Xs))}},
                      "identification is true in exact arithmetic; a tool must report the conditioning (the sixth eigenvalue of "
                      "the centred Gram matrix is of the order of the squared difference of the states) and must not certify "
                      "when its rank decisions are not separated from its tolerance",
                      "P for exact data (generic position); the numbers are N",
                      "ENSEMBLE_RIGIDITY.md section 6.1 (noise), Theorem G"))
        if iid == "F1a":
            check("F1a: nearly equal states are still certified in floating point", out["ok"], f"lambda_min {lam:.1e}")
    # local distance data: thin window, long helix
    rng = np.random.default_rng(52)
    tors = rng.uniform(0.7, 2.4, 17) * rng.choice([-1, 1], 17)
    tors[9] = 0.02
    X = chain(20, tors, theta=THETA)
    mu, Lam, CL = sharp_constants(X)
    tau = min(csig3(X[i:i + 4]) for i in range(17))
    check("F2: a nearly planar window makes local distance data ill-conditioned", tau < 0.02 and 1 / (2 * mu) > 5, f"tau = {tau:.3f}, 1/(2 mu) = {1 / (2 * mu):.1f}")
    I.append(inst("F2", "F ill-conditioned", "one conformation, 20 points, one nearly planar window; distances of separation <= 4", THETA, [X], [1.0],
                  {"kind": "distances of one conformation for pairs of sequence separation <= 4, exact",
                   "pairs": band_pairs(20, 4), "distances": [float(np.linalg.norm(X[j] - X[k])) for j, k in band_pairs(20, 4)]},
                  {"globally_identifiable": True, "conditioning": {"thinnest_window": tau, "first_order_constant_1_over_2mu": 1 / (2 * mu), "C_L": CL}},
                  "unique for exact data; with errors the mirror image of the tail beyond the thin window fits almost as well: a tool "
                  "must report the first-order constant and must not claim the handedness of the tail without checking the residual gap",
                  "P for exact data (Theorem L); numbers N", "LOCAL_DATA_STABILITY.md Theorems L, L+"))
    Xh = chain(100, np.full(97, 1.0), theta=THETA)
    mu, Lam, CL = sharp_constants(Xh)
    X20 = chain(20, np.full(17, 1.0), theta=THETA)
    mu20 = sharp_constants(X20)[0]
    check("F3: on a helix the first-order constant grows like n^2", 15 < mu20 / mu < 40, f"ratio of constants between 100 and 20 points: {mu20 / mu:.1f} (25 = n^2 law)")
    I.append(inst("F3", "F ill-conditioned (by length)", "one helical conformation, 100 points; distances of separation <= 4", THETA, [Xh], [1.0],
                  {"kind": "distances of one conformation for pairs of sequence separation <= 4, exact",
                   "pairs": band_pairs(100, 4), "distances": [float(np.linalg.norm(Xh[j] - Xh[k])) for j, k in band_pairs(100, 4)]},
                  {"globally_identifiable": True, "conditioning": {"first_order_constant_1_over_2mu": 1 / (2 * mu), "C_L": CL}},
                  "unique for exact data; the error amplification grows like the square of the length (Theorem K (c)): accuracy "
                  "claims that do not degrade with length from local distances alone are wrong",
                  "P (Theorems K (c), L)", "LOCAL_DATA_STABILITY.md"))

    # ---- G: outside the assumptions -------------------------------------------------
    rng = np.random.default_rng(61)
    n = 12
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA), chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=np.deg2rad(104.0))]
    w = np.array([0.5, 0.5])
    out = linear_certificate(mixture_data(Xs, w), THETA)
    check("G1: states with different bond angles are refused by the linear certificate", not out["ok"], out.get("reason", ""))
    I.append(inst("G1", "G outside the assumptions", "2 states with different bond angles (111 and 104 degrees); the tool is told 111", THETA, Xs, w, averaged_data(Xs, w),
                  {"assumption_violated": "the statewise constraints supplied to the tool are false for one state"},
                  "must refuse (the supplied constraints are inconsistent with the data), not return two states",
                  "N (our linear certificate refuses: " + out.get("reason", "") + ")", "ENSEMBLE_RIGIDITY.md section 12"))
    t = rng.uniform(-np.pi, np.pi, n - 3)
    arc = np.linspace(-0.8, 0.8, 201)
    Xs = []
    for a in arc:
        tt = t.copy()
        tt[4] += a
        tt[7] += 0.5 * a * a
        Xs.append(chain(n, tt, theta=THETA))
    w = np.full(len(arc), 1 / len(arc))
    M = mixture_data(Xs, w)
    G = -0.5 * (np.eye(n) - 1 / n) @ M @ (np.eye(n) - 1 / n)
    ev = np.sort(np.linalg.eigvalsh(G))[::-1]
    rk = int((ev > 1e-8 * ev[0]).sum())
    out = linear_certificate(M, THETA)
    check("G2: a continuous ensemble is refused", not out["ok"], out.get("reason", "") + f"; rank of the stack {rk}")
    I.append(inst("G2", "G outside the assumptions; C not determined", "a continuous one-parameter family of conformations (201 quadrature states on an arc)", THETA,
                  Xs[::50], [0.2] * 5, {"kind": "ensemble-averaged squared distances, all pairs, exact (of the 201-state quadrature)", "matrix": M.tolist()},
                  {"globally_identifiable": False, "reason": "an ensemble with a continuous part is never determined by averaged squared distances",
                   "note": "truth.states lists 5 of the 201 quadrature states only"},
                  "must not return a finite list of states as 'the' ensemble",
                  "P (Science division, SCI-REV-0021 F7 (c); our Corollary 4.2 (c))", "ENSEMBLE_RIGIDITY.md Corollary 4.2"))
    Xs = [chain(n, rng.choice([0.0, np.pi], n - 3), theta=THETA) for _ in range(2)]
    w = np.array([0.5, 0.5])
    out = linear_certificate(mixture_data(Xs, w), THETA)
    check("G3: planar states are refused", not out["ok"], out.get("reason", ""))
    I.append(inst("G3", "G outside the assumptions", "2 planar states (all torsions 0 or 180 degrees)", THETA, Xs, w, averaged_data(Xs, w),
                  {"assumption_violated": "the states do not span space: the stack has rank 4, not 6"},
                  "must refuse or treat the problem as two-dimensional; must not pad the rank",
                  "N (our linear certificate refuses: " + out.get("reason", "") + ")", "ENSEMBLE_RIGIDITY.md Theorem A, section 12"))
    rng = np.random.default_rng(62)
    w = rng.dirichlet(np.ones(2) * 4)
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(2)]
    M = mixture_data(Xs, w)
    Nz = rng.normal(size=(n, n))
    Mn = M + 1e-2 * np.abs(M).mean() * (Nz + Nz.T) / 2
    np.fill_diagonal(Mn, 0.0)
    out = linear_certificate(Mn, THETA)
    check("G4: noisy data are not certified in exact-data mode", not out["ok"], out.get("reason", ""))
    I.append(inst("G4", "G outside the assumptions (noise)", "instance like A1 with symmetric noise of relative size 1e-2 on the averaged data", THETA, Xs, w,
                  {"kind": "ensemble-averaged squared distances, all pairs, with noise", "matrix": Mn.tolist(), "noise_relative_size": 1e-2},
                  {"globally_identifiable": "for the exact data: yes; for the noisy data no statement is proved at this noise level"},
                  "must not output a certificate of uniqueness; an estimate must come with the statement that the certificate was not established",
                  "N (our exact-data certificate refuses: " + out.get("reason", "") + "); the proved noise bound (Theorem G) has an uncomputed constant",
                  "ENSEMBLE_RIGIDITY.md section 6.1, Theorem G, PROOF_OBLIGATIONS O-5"))
    return I, checks


def main():
    write = "--write" in sys.argv
    quick = "--quick" in sys.argv
    I, checks = build(quick=quick)
    ok = True
    for name, cond, note in checks:
        ok &= cond
        print(f"{'ok  ' if cond else 'FAIL'}  {name}" + (f"   [{note}]" if note else ""))
    print(f"{len(I)} instances; {sum(c for _, c, _ in checks)} of {len(checks)} label checks hold")
    for d in I:
        print(f"  {d['id']:4s} {d['category'][:62]:62s} K = {d['n_states']}, n = {d['n_points']}")
    if write and ok and not quick:
        out = os.path.join(HERE, "benchmark_suite")
        os.makedirs(out, exist_ok=True)
        manifest = []
        for d in I:
            txt = json.dumps(d, indent=1, sort_keys=True)
            with open(os.path.join(out, d["id"] + ".json"), "w") as f:
                f.write(txt + "\n")
            manifest.append({"id": d["id"], "category": d["category"], "title": d["title"],
                             "sha256": hashlib.sha256((txt + "\n").encode()).hexdigest()})
        with open(os.path.join(out, "MANIFEST.json"), "w") as f:
            f.write(json.dumps(manifest, indent=1) + "\n")
        print(f"written: {len(I)} instances and MANIFEST.json to {out}")
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
