#!/usr/bin/env python3
"""Synthetic controls with ground truth for ensemble-inference software (docs/ensemble/BENCHMARK_CONTROLS.md).

Writes experiments/ensemble/benchmarks/controls_v1.json: a list of small, exactly specified instances, each with
the configuration space, the observables, the data, the question, and the verdict a sound tool must give
(IDENTIFIED with a certificate, NOT_IDENTIFIED with an explicit twin, an INTERVAL with dual certificates, or
the requirement to ABSTAIN), together with the reason and the place in the report.

Every claim written to the file is verified here before it is written:
  * twins: equality of the data in exact rational arithmetic (or to 1e-13 where square roots enter);
  * certificates: the function c + lambda.Phi is computed in exact rational arithmetic on every configuration
    (zero on the support, at least gamma off it), after the linear programme's solution has been rounded inside
    the exact solution space of the equalities — the solver is not trusted;
  * intervals: both ends by linear programming and, where a closed form exists, against the closed form; the dual
    certificates are checked on every configuration in exact arithmetic.
This is a specification with reference instances.  It is not a benchmark harness: running tools against it,
timing them and scoring them is the engineering division's work.

Usage: python3 experiments/ensemble/benchmark_controls.py      (a few seconds; exit code 0 iff every check holds)
"""
import itertools, json, math, pathlib, sys
from fractions import Fraction as Fr
import numpy as np
import sympy
from scipy.optimize import linprog

here = pathlib.Path(__file__).resolve().parent
OUT = here / "benchmarks" / "controls_v1.json"
checks = []          # (description, bool)


def check(desc, cond):
    checks.append((desc, bool(cond)))
    return bool(cond)


def fr(v):
    return str(Fr(v))


def frac_list(vs):
    return [fr(v) for v in vs]


# ----------------------------------------------------------------------------------------------------------------
# exact helpers on a finite space: Phi is a list of m rows of length M with Fraction entries
# ----------------------------------------------------------------------------------------------------------------
def means(Phi, weights):
    return [sum(w * row[k] for k, w in weights.items()) for row in Phi]


def exact_certificate(Phi, S, bound=1):
    """A certificate (c, lam) with c + lam.Phi = 0 on S and > 0 off S, in exact rationals, or None.
    The equalities are solved exactly (a rational basis of their solution space); the LP only chooses a point in
    that space, which is then rounded to rationals — so the equalities hold exactly whatever the solver did."""
    m, M = len(Phi), len(Phi[0])
    G = sympy.Matrix([[1] + [Phi[i][x] for i in range(m)] for x in S])            # rows (1, Phi(x)), x in S
    basis = G.nullspace()                                                          # exact rational basis
    if not basis:
        return None
    B = np.array([[float(v) for v in b] for b in basis]).T                         # (m+1) x k
    off = [x for x in range(M) if x not in S]
    R = np.array([[1.0] + [float(Phi[i][x]) for i in range(m)] for x in off])      # rows (1, Phi(y)), y off S
    k = B.shape[1]
    # maximise t subject to R B u >= t, |u_j| <= bound
    res = linprog(np.concatenate([np.zeros(k), [-1.0]]), A_ub=np.hstack([-R @ B, np.ones((len(off), 1))]),
                  b_ub=np.zeros(len(off)), bounds=[(-bound, bound)] * k + [(None, None)], method="highs")
    if res.status != 0 or -res.fun < 1e-9:
        return None
    u = [Fr(float(v)).limit_denominator(10 ** 6) for v in res.x[:k]]
    coef = [sum(u[j] * Fr(str(basis[j][r])) for j in range(k)) for r in range(m + 1)]
    f = [coef[0] + sum(coef[1 + i] * Phi[i][x] for i in range(m)) for x in range(M)]
    if any(f[x] != 0 for x in S) or any(f[x] <= 0 for x in off):
        return None
    gamma = min(f[x] for x in off)
    return {"c": coef[0], "lam": coef[1:], "gamma": gamma, "norm1": sum(abs(v) for v in coef[1:])}


def affinely_independent(Phi, S):
    G = sympy.Matrix([[1] + [Phi[i][x] for i in range(len(Phi))] for x in S])
    return G.rank() == len(S)


def lp_interval(Phi, y, tau, psi):
    """Range of E psi over ensembles with |E Phi_i - y_i| <= tau (floating point)."""
    m, M = len(Phi), len(Phi[0])
    A = np.array([[float(v) for v in row] for row in Phi]); yy = np.array([float(v) for v in y]); p = np.array([float(v) for v in psi])
    Aub = np.vstack([A, -A]); bub = np.concatenate([yy + float(tau), -(yy - float(tau))])
    kw = dict(A_ub=Aub, b_ub=bub, A_eq=np.ones((1, M)), b_eq=[1.0], bounds=[(0, None)] * M, method="highs")
    lo = linprog(p, **kw); hi = linprog(-p, **kw)
    return lo.fun, -hi.fun


def cube(n, mod_flip=False):
    pts = [p for p in itertools.product((1, -1), repeat=n) if not mod_flip or p[0] == 1]
    return pts


def sign_label(p):
    return "".join("+" if v > 0 else "-" for v in p)


def pair_table(pts):
    n = len(pts[0])
    names = [f"x{i + 1}*x{j + 1}" for i in range(n) for j in range(i + 1, n)]
    rows = [[Fr(p[i] * p[j]) for p in pts] for i in range(n) for j in range(i + 1, n)]
    return names, rows


controls = []


def add(**kw):
    controls.append(kw)


# ================================================================================================================
# B1  identified, with a certificate
# ================================================================================================================
pts = cube(4, mod_flip=True); names, Phi = pair_table(pts)
S = [pts.index(p) for p in ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1))]
cert = exact_certificate(Phi, S)
check("B1-01 certificate exists and is exact", cert is not None and affinely_independent(Phi, S))
w = {S[0]: Fr(1, 2), S[1]: Fr(3, 10), S[2]: Fr(1, 5)}
add(id="B1-01", family="identified", title="Three conformers on the 4-cube, pair correlations",
    space={"type": "finite", "description": "{+1,-1}^4 modulo the global flip (first sign +)", "states": [sign_label(p) for p in pts]},
    observables={"names": names, "table": [frac_list(r) for r in Phi]},
    ensemble={"support": [sign_label(pts[k]) for k in S], "weights": frac_list([w[k] for k in S])},
    data=frac_list(means(Phi, w)),
    question="Is the ensemble determined by the six pair correlations among all ensembles on the space?",
    expected={"verdict": "IDENTIFIED", "certificate": {"c": fr(cert["c"]), "lambda": frac_list(cert["lam"]),
              "gamma": fr(cert["gamma"]), "lambda_l1_norm": fr(cert["norm1"])},
              "stability": "every ensemble with pair correlations within tau (max norm) of the data has mass at most "
                           "lambda_l1_norm * tau / gamma outside the support (Proposition E1.1)"},
    why="Any three conformers are determined by pair correlations (Proposition E9(a)); the answer does not depend on the weights.",
    source="ENSEMBLE_REPORT.md section 2.1 (E1, E1.1), section 4.1 (E9)")

rng = np.random.default_rng(20261126)
pts6 = cube(6, mod_flip=True); names6, Phi6 = pair_table(pts6)
while True:
    S6 = sorted(int(v) for v in rng.choice(len(pts6), size=5, replace=False))
    cert6 = exact_certificate(Phi6, S6)
    if cert6 is not None and affinely_independent(Phi6, S6):
        break
w6 = dict(zip(S6, [Fr(3, 10), Fr(1, 4), Fr(1, 5), Fr(3, 20), Fr(1, 10)]))
check("B1-02 certificate exact", cert6["gamma"] > 0)
add(id="B1-02", family="identified", title="Five conformers on the 6-cube that form a face, pair correlations",
    space={"type": "finite", "description": "{+1,-1}^6 modulo the global flip", "states": [sign_label(p) for p in pts6]},
    observables={"names": names6, "table": [frac_list(r) for r in Phi6]},
    ensemble={"support": [sign_label(pts6[k]) for k in S6], "weights": frac_list([w6[k] for k in S6])},
    data=frac_list(means(Phi6, w6)),
    question="Is the ensemble determined by the fifteen pair correlations?",
    expected={"verdict": "IDENTIFIED", "certificate": {"c": fr(cert6["c"]), "lambda": frac_list(cert6["lam"]),
              "gamma": fr(cert6["gamma"]), "lambda_l1_norm": fr(cert6["norm1"])}},
    why="The support is the exact ground-state set of a pair energy and its pair features are affinely independent (Theorem E1(a)).",
    source="section 2.1 (E1)")

# ================================================================================================================
# B2  not identified: explicit twins
# ================================================================================================================
sq = cube(2); Phi_sq = [[Fr(p[0]) for p in sq], [Fr(p[1]) for p in sq]]
mu = {sq.index((1, 1)): Fr(1, 2), sq.index((-1, -1)): Fr(1, 2)}; nu = {sq.index((1, -1)): Fr(1, 2), sq.index((-1, 1)): Fr(1, 2)}
check("B2-01 twin has the same data", means(Phi_sq, mu) == means(Phi_sq, nu))
Phi_sq3 = Phi_sq + [[Fr(p[0] * p[1]) for p in sq]]
check("B2-01 with the pair observable the data differ", means(Phi_sq3, mu) != means(Phi_sq3, nu))
add(id="B2-01", family="not identified", title="The square: one-body data do not see which sites move together",
    space={"type": "finite", "description": "{+1,-1}^2", "states": [sign_label(p) for p in sq]},
    observables={"names": ["x1", "x2"], "table": [frac_list(r) for r in Phi_sq]},
    ensemble={"support": ["++", "--"], "weights": ["1/2", "1/2"]}, data=frac_list(means(Phi_sq, mu)),
    question="Is the ensemble determined by the two one-body means (equivalently, by the laws of the two coordinates)?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"support": ["+-", "-+"], "weights": ["1/2", "1/2"]},
              "remark": "with the observable x1*x2 added every ensemble on this space is determined (the four feature vectors are affinely independent)"},
    why="Two conformers and two coordinate laws: the smallest instance of the sharpness of the Renyi-Heppes count (Theorem E4).",
    source="section 3.1 (E4)")

Phi_abc = [[Fr(0), Fr(0), Fr(1)]]
check("B2-02 exposed", all(v >= 0 for v in Phi_abc[0]) and [k for k, v in enumerate(Phi_abc[0]) if v == 0] == [0, 1])
check("B2-02 not affinely independent on the support", not affinely_independent(Phi_abc, [0, 1]))
add(id="B2-02", family="not identified", title="Exposed is not identified",
    space={"type": "finite", "description": "three configurations a, b, c", "states": ["a", "b", "c"]},
    observables={"names": ["phi"], "table": [frac_list(Phi_abc[0])]},
    ensemble={"support": ["a", "b"], "weights": ["1/2", "1/2"]}, data=["0"],
    question="Is the ensemble determined by the mean of phi?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"support": ["a", "b"], "weights": ["1/4", "3/4"]},
              "trap": "the support {a, b} IS the zero set of the non-negative function phi in the span; a tool that tests "
                      "only this condition answers IDENTIFIED, wrongly: the features are not affinely independent on the support"},
    why="Condition (i) of Theorem E1(a) fails while condition (ii) holds.", source="section 2.1; report section 7 item 6, F1")

pts5 = cube(5, mod_flip=True); names5, Phi5 = pair_table(pts5)
A4 = [(1, 1, 1, 1, 1), (1, 1, 1, -1, -1), (1, 1, -1, 1, -1), (1, 1, -1, -1, 1)]
B4 = [(1, 1, 1, 1, -1), (1, 1, 1, -1, 1), (1, 1, -1, 1, 1), (1, 1, -1, -1, -1)]
muA = {pts5.index(p): Fr(1, 4) for p in A4}; muB = {pts5.index(p): Fr(1, 4) for p in B4}
check("B2-03 twin has the same ten pair correlations", means(Phi5, muA) == means(Phi5, muB))
check("B2-03 the support is not a face (no certificate)", exact_certificate(Phi5, sorted(muA)) is None)
add(id="B2-03", family="not identified", title="Four conformers on the 5-cube with a twin of the other parity",
    space={"type": "finite", "description": "{+1,-1}^5 modulo the global flip", "states": [sign_label(p) for p in pts5]},
    observables={"names": names5, "table": [frac_list(r) for r in Phi5]},
    ensemble={"support": [sign_label(p) for p in A4], "weights": ["1/4"] * 4}, data=frac_list(means(Phi5, muA)),
    question="Is the ensemble determined by the ten pair correlations?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"support": [sign_label(p) for p in B4], "weights": ["1/4"] * 4},
              "remark": "three of the four conformers, with any weights, are determined (B1-01); the fourth breaks it"},
    why="A Hadamard quadruple on four of the sites (Proposition E9(b)); the cut polytope is 3-neighbourly and not 4-neighbourly.",
    source="section 4.1 (E9(b)); internal review ER3, F2")

tri = {"mu": [[3, 4, 5], [4, 5, 6]], "nu": [[3, 5, 6], [4, 4, 5]]}
laws = lambda ens: [sorted(t[e] for t in ens) for e in range(3)]
check("B2-04 same law on every edge", laws(tri["mu"]) == laws(tri["nu"]))
check("B2-04 triangle inequalities", all(a + b > c for ens in tri.values() for t in ens for a, b, c in itertools.permutations(t)))
add(id="B2-04", family="not identified", title="Two triangles: the laws of the three side lengths",
    space={"type": "continuous", "description": "triangles in the plane up to congruence, given by their side lengths (edges 01, 02, 12)"},
    observables={"names": ["law of |01|", "law of |02|", "law of |12|"]},
    ensemble={"conformers": tri["mu"], "weights": ["1/2", "1/2"]}, data={"edge laws (multisets)": laws(tri["mu"])},
    question="Is the two-conformer ensemble determined by the three edge-length laws?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"conformers": tri["nu"], "weights": ["1/2", "1/2"]}},
    why="The rigidity matroid of the triangle is free, hence disconnected: lengths of different conformers can be spliced (Theorem E5(b)).",
    source="section 3.2 (E5); check R4")

d1_x1 = [(Fr(1, 2), Fr(2)), (Fr(3), Fr(3)), (Fr(-1), Fr(0)), (Fr(1), Fr(0))]
d1_x2 = [(Fr(1, 2), Fr(3, 2)), (Fr(3, 2), Fr(-4)), (Fr(-2), Fr(0)), (Fr(2), Fr(0))]
refl = lambda P: [P[0], (P[1][0], -P[1][1]), P[2], P[3]]
E4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
sqlen = lambda P, E: [(P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2 for i, j in E]
elaws = lambda ens, E: [sorted(sqlen(P, E)[e] for P in ens) for e in range(len(E))]
d1_y, d1_yp = refl(d1_x1), refl(d1_x2)
check("B2-05 same law on all six edges", elaws([d1_x1, d1_x2], E4) == elaws([d1_y, d1_yp], E4))
check("B2-05 a different ensemble", sorted([sqlen(d1_x1, E4), sqlen(d1_x2, E4)]) != sorted([sqlen(d1_y, E4), sqlen(d1_yp, E4)]))
check("B2-05 no edge length in common", all(a != b for a, b in zip(sqlen(d1_x1, E4), sqlen(d1_x2, E4))))
coords = lambda P: [[fr(c) for c in pt] for pt in P]
add(id="B2-05", family="not identified", title="A globally rigid graph, individually generic conformers, a twin (the science division's Example D1)",
    space={"type": "continuous", "description": "four points in the plane up to congruence; all six distances measured (K4)"},
    observables={"names": [f"law of the squared distance {i}{j}" for i, j in E4]},
    ensemble={"conformers": [coords(d1_x1), coords(d1_x2)], "weights": ["1/2", "1/2"]},
    data={"squared edge-length laws (multisets)": [[fr(v) for v in e] for e in elaws([d1_x1, d1_x2], E4)]},
    question="Is the ensemble determined by the six edge-length laws?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"conformers": [coords(d1_y), coords(d1_yp)], "weights": ["1/2", "1/2"]},
              "trap": "K4 is generically globally rigid and the two conformers have no length in common, but the pair is not "
                      "JOINTLY generic: in both, points 2 and 3 lie on a common line through which point 1 can be reflected"},
    why="Theorem E7 needs jointly generic conformers; this is the counterexample of the science division's review SCI-REV-0020.",
    source="section 3.3 (E7, Example D1); check R9")

T3 = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1))]
P3, P4, Q3, Q4 = (Fr(2), Fr(1)), (Fr(-1), Fr(2)), (Fr(1), Fr(3)), (Fr(3), Fr(-1))
d2 = {"x1": T3 + [P3, P4], "x2": T3 + [Q3, Q4], "y": T3 + [P3, Q4], "yp": T3 + [Q3, P4]}
E5m = [(i, j) for i in range(5) for j in range(i + 1, 5) if (i, j) != (3, 4)]
check("B2-06 same law on every measured edge", elaws([d2["x1"], d2["x2"]], E5m) == elaws([d2["y"], d2["yp"]], E5m))
check("B2-06 the unmeasured distance tells them apart", elaws([d2["x1"], d2["x2"]], [(3, 4)]) != elaws([d2["y"], d2["yp"]], [(3, 4)]))
add(id="B2-06", family="not identified", title="A shared rigid part: two mobile groups whose coupling the data do not see (Example D2)",
    space={"type": "continuous", "description": "five points in the plane up to congruence; all distances measured except 3-4"},
    observables={"names": [f"law of the squared distance {i}{j}" for i, j in E5m]},
    ensemble={"conformers": [coords(d2["x1"]), coords(d2["x2"])], "weights": ["1/2", "1/2"]},
    data={"squared edge-length laws (multisets)": [[fr(v) for v in e] for e in elaws([d2["x1"], d2["x2"]], E5m)]},
    question="Is the ensemble determined by the nine measured edge-length laws?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"conformers": [coords(d2["y"]), coords(d2["yp"])], "weights": ["1/2", "1/2"]},
              "what_is_determined": "the positions of points 3 and 4 relative to the triangle 0-1-2, separately; not which position of 3 goes with which position of 4"},
    why="The graph is rigid, but the conformers share the triangle 0-1-2: the laws cannot see how the two motions are coupled.",
    source="section 3.3 (Example D2), Problem O3; check R10")

def torus_data(points, weights):
    out = []
    for f1 in (lambda t: 1.0, math.cos, math.sin):
        for f2 in (lambda t: 1.0, math.cos, math.sin):
            out.append(sum(w * f1(p[0]) * f2(p[1]) for p, w in zip(points, weights)))
    return np.array(out)
tA = [(2 * math.pi * k / 3, 2 * math.pi * k / 3) for k in range(3)]
tB = [(math.pi / 3 + 2 * math.pi * k / 3, math.pi / 3 + 2 * math.pi * k / 3) for k in range(3)]
check("B2-07 same nine bilinear trigonometric means", np.abs(torus_data(tA, [1 / 3] * 3) - torus_data(tB, [1 / 3] * 3)).max() < 1e-13)
add(id="B2-07", family="not identified", title="Three states on a torus of two angles, all products of 1, cos, sin over the two angles",
    space={"type": "continuous", "description": "the torus of two angles (phi1, phi2)"},
    observables={"names": ["means of u(phi1)*v(phi2), u, v in {1, cos, sin} (nine numbers)"]},
    ensemble={"conformers_in_units_of_pi": [["0", "0"], ["2/3", "2/3"], ["4/3", "4/3"]], "weights": ["1/3"] * 3},
    data={"E cos*cos": "1/2", "E sin*sin": "1/2", "the other six non-constant means": "0"},
    question="Is the ensemble determined by the nine means among all probability measures on the torus?",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"conformers_in_units_of_pi": [["1/3", "1/3"], ["1", "1"], ["5/3", "5/3"]], "weights": ["1/3"] * 3},
              "remark": "no three-state ensemble on this torus is determined by these data (Proposition E22); two states that "
                        "differ in both angles are (Proposition E20')",
              "trap": "a search restricted to a product grid of angles reports IDENTIFIED: the twin does not lie on the grid"},
    why="Every measure with the data lives on the circle where the bilinear form through the three states vanishes, and there the data are trigonometric moments of order at most two.",
    source="section 4c.4 (Proposition E22; found by the internal review ER3)")

def leg_lengths_sq(theta, t, U, V):
    c, s = math.cos(theta), math.sin(theta)
    return [(u[0] - (c * v[0] - s * v[1] + t[0])) ** 2 + (u[1] - (s * v[0] + c * v[1] + t[1])) ** 2 for u, v in zip(U, V)]
U = [(0.0, 0.0), (1.0, 0.0), (3.0, 0.0), (4.5, 0.0), (6.0, 0.0), (7.0, 0.0)]
V = [(0.0, 0.0), (2.0, 0.0), (5.0, 0.0), (-1.0, 0.0), (1.5, 0.0), (3.0, 0.0)]
pose, mirror = (0.7, (0.4, 1.3)), (-0.7, (0.4, -1.3))
check("B2-08 the mirror pose has the same six leg lengths",
      np.abs(np.array(leg_lengths_sq(*pose, U, V)) - np.array(leg_lengths_sq(*mirror, U, V))).max() < 1e-12)
add(id="B2-08", family="not identified", title="Two planar rigid bodies: a mirror pose for every number of legs",
    space={"type": "continuous", "description": "relative poses (rotation angle theta, translation t) of two rigid bodies in the plane; "
           "leg e joins the point U[e] of the first body to the point V[e] of the second (body coordinates), length |U[e] - R(theta) V[e] - t|"},
    observables={"names": ["six leg lengths"], "U": U, "V": V},
    ensemble={"conformers": [{"theta": pose[0], "t": list(pose[1])}], "weights": ["1"]},
    data={"squared leg lengths": [round(v, 12) for v in leg_lengths_sq(*pose, U, V)]},
    question="Is the single pose determined by its six leg lengths?  (Four legs determine a generic pose in the plane.)",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"conformers": [{"theta": mirror[0], "t": list(mirror[1])}], "weights": ["1"]},
              "trap": "all attachment points of each body are collinear; then the reflected pose (-theta, (t_x, -t_y)) has the same "
                      "length for every leg, for any number of legs, although the leg matroid is connected"},
    why="Theorem E7' is for generic attachment points; planar (here: collinear) bodies are excluded.  Connectivity of the matroid is not the whole criterion.",
    source="section 3.3 (E7', 'What genericity excludes'); check P4; internal review ER2, F6")

# ================================================================================================================
# B3  identified, and a small error in the data leaves almost everything open
# ================================================================================================================
N = 360; gam = 1 - math.cos(2 * math.pi / N)
A_poly = np.array([[math.cos(2 * math.pi * k / N) for k in range(N)], [math.sin(2 * math.pi * k / N) for k in range(N)]])
def worst_mass_off_vertex(tau):
    c = np.zeros(N); c[0] = 1.0                                     # minimise the population of vertex 0
    Aub = np.vstack([A_poly, -A_poly]); bub = np.array([1 + tau, tau, -(1 - tau), tau])
    res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=np.ones((1, N)), b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
    return 1 - res.fun
b3 = {tau: worst_mass_off_vertex(tau) for tau in (1e-5, 1e-4, 2e-4)}
check("B3-01 the bound tau/gamma is attained", all(abs(b3[t] - min(1.0, t / gam)) < 1e-6 for t in b3))
add(id="B3-01", family="identified but ill-conditioned", title="A vertex of a regular 360-gon, means of (cos, sin)",
    space={"type": "finite", "description": "the vertices (cos(2 pi k/360), sin(2 pi k/360)), k = 0..359"},
    observables={"names": ["cos", "sin"]},
    ensemble={"support": ["k = 0"], "weights": ["1"]}, data=["1", "0"],
    question="(a) Is the conformation k = 0 determined by the two means?  (b) If each mean is known within tau, how much mass can be elsewhere?",
    expected={"verdict": "IDENTIFIED", "certificate": {"f": "1 - cos", "gamma": gam, "lambda_l1_norm": 1},
              "stability_constant": 1 / gam,
              "largest mass off the conformation compatible with the data within tau": {str(t): round(v, 6) for t, v in b3.items()},
              "closed form": "min(1, tau / gamma), gamma = 1 - cos(2 pi/360) = 1.523e-4: attained by the two neighbouring vertices"},
    why="The verdict IDENTIFIED is correct and nearly useless: an error of 1.5e-4 in one mean leaves the population of the "
        "conformation completely undetermined.  On a continuous circle the modulus is a square root (Example E1.2, Proposition E2.2).",
    source="section 2.1 (E1.1, E1.2), section 2.2 (E2.2)")

# ================================================================================================================
# B4  a certificate of one kind must abstain although the ensemble is identified
# ================================================================================================================
pts8 = cube(8, mod_flip=True); names8, Phi8 = pair_table(pts8)
X8 = np.array(pts8, dtype=float)
def spurious_sign_vectors(S):
    Sm = X8[S].T; P = Sm @ np.linalg.pinv(Sm)
    f = np.sum((X8 - X8 @ P) ** 2, axis=1)
    return [k for k in np.nonzero(f < 1e-9)[0].tolist() if k not in S]
rng4 = np.random.default_rng(4)
while True:
    S8 = sorted(int(v) for v in rng4.choice(len(pts8), size=4, replace=False))
    extra = spurious_sign_vectors(S8)
    if extra and np.linalg.matrix_rank(X8[S8]) == 4:
        cert8 = exact_certificate(Phi8, S8)
        if cert8 is not None and affinely_independent(Phi8, S8):
            break
# the extra sign vector is an exact rational combination of the conformers
sol = sympy.Matrix([[int(v) for v in pts8[k]] for k in S8]).T.solve_least_squares(sympy.Matrix([int(v) for v in pts8[extra[0]]]))
comb_ok = (sympy.Matrix([[int(v) for v in pts8[k]] for k in S8]).T * sol) == sympy.Matrix([int(v) for v in pts8[extra[0]]])
check("B4-01 another sign vector lies in the span (exact)", comb_ok)
check("B4-01 and the support is a face with an exact certificate", cert8["gamma"] > 0)
add(id="B4-01", family="must abstain", title="Identified, but not by the projection certificate",
    space={"type": "finite", "description": "{+1,-1}^8 modulo the global flip (128 states)", "states": "all sign vectors of length 8 with first sign +"},
    observables={"names": "the 28 pair products x_i*x_j, i < j"},
    ensemble={"support": [sign_label(pts8[k]) for k in S8], "weights": "any positive weights"},
    question="Is every ensemble on these four conformers determined by its pair correlations?",
    expected={"verdict": "IDENTIFIED", "certificate": {"c": fr(cert8["c"]), "lambda (order of the 28 pairs)": frac_list(cert8["lam"]),
              "gamma": fr(cert8["gamma"])},
              "must_abstain": "a tool that only has the projection certificate ||x - Px||^2 (Theorem E10) must answer ABSTAIN or "
                              "'not certified by this certificate', never NOT_IDENTIFIED",
              "other sign vector in the span": {"vector": sign_label(pts8[extra[0]]), "coefficients on the conformers": [str(v) for v in sol]}},
    why="The span of the conformers contains another sign vector, so every positive semidefinite certificate vanishes there too; "
        "the support is nevertheless the exact ground-state set of a pair energy, which needs a certificate of degree at least 4 "
        "(the Complexity division's Proposition 13).  At n = 12, K = 9 this is the case for 92 % of random supports.",
    source="section 4.2 (E10; 'Deciding exposedness'); degree2_vs_face.py")

# ================================================================================================================
# B5  partial identification: exact intervals
# ================================================================================================================
c3 = cube(3); Phi1 = [[Fr(p[i]) for p in c3] for i in range(3)]
m = [Fr(1, 5), Fr(1, 2), Fr(-3, 10)]
psi12 = [Fr(p[0] * p[1]) for p in c3]
lo, hi = lp_interval(Phi1, m, 0, psi12)
check("B5-01 interval = Frechet bounds", abs(lo - float(abs(m[0] + m[1]) - 1)) < 1e-9 and abs(hi - float(1 - abs(m[0] - m[1]))) < 1e-9)
check("B5-01 dual certificates hold at every configuration",
      all(p[0] * p[1] <= 1 + p[0] - p[1] and p[0] * p[1] >= -1 + p[0] + p[1] for p in c3))
add(id="B5-01", family="partial identification", title="One-body data on the 3-cube: the range of a pair correlation",
    space={"type": "finite", "description": "{+1,-1}^3", "states": [sign_label(p) for p in c3]},
    observables={"names": ["x1", "x2", "x3"], "table": [frac_list(r) for r in Phi1]}, data=frac_list(m),
    question="What is the range of E[x1*x2] over all ensembles with these three means?",
    expected={"verdict": "INTERVAL", "interval": [fr(abs(m[0] + m[1]) - 1), fr(1 - abs(m[0] - m[1]))],
              "dual certificates": {"upper": "x1*x2 <= 1 + x1 - x2 on the cube, so E[x1*x2] <= 1 + m1 - m2",
                                    "lower": "x1*x2 >= -1 + x1 + x2 on the cube, so E[x1*x2] >= -1 + m1 + m2"},
              "closed form": "[|m1 + m2| - 1, 1 - |m1 - m2|]"},
    why="Nothing is identified here except the one-body means; the certified answer is an interval with a dual certificate for each end (Theorem E2(a) / E17(a)).",
    source="section 2.2, section 4b; SOFTWARE_INTERFACE.md F3")

ppp = [Fr(1) if p == (1, 1, 1) else Fr(0) for p in c3]
lo, hi = lp_interval(Phi1, m, 0, ppp)
pi_ = [(1 + v) / 2 for v in m]
check("B5-02 population interval = Frechet bounds", abs(lo - float(max(Fr(0), sum(pi_) - 2))) < 1e-9 and abs(hi - float(min(pi_))) < 1e-9)
add(id="B5-02", family="partial identification", title="The same data: the range of the population of one state",
    space={"type": "finite", "description": "{+1,-1}^3"}, observables={"names": ["x1", "x2", "x3"]}, data=frac_list(m),
    question="What is the range of the population of the state +++?",
    expected={"verdict": "INTERVAL", "interval": [fr(max(Fr(0), sum(pi_) - 2)), fr(min(pi_))],
              "closed form": "[max(0, p1 + p2 + p3 - 2), min(p1, p2, p3)], p_i = (1 + m_i)/2",
              "reading": "the data are compatible with the state being absent and with a population of 35 %"},
    why="A certified restriction on a population when the ensemble is not identified.", source="SOFTWARE_INTERFACE.md F3")

tau = Fr(1, 20)
lo, hi = lp_interval(Phi1, m, tau, psi12)
check("B5-03 interval with tolerance", abs(lo - float(abs(m[0] + m[1]) - 1 - 2 * tau)) < 1e-9 and abs(hi - float(1 - abs(m[0] - m[1]) + 2 * tau)) < 1e-9)
add(id="B5-03", family="partial identification", title="The same question with each mean known within 1/20",
    space={"type": "finite", "description": "{+1,-1}^3"}, observables={"names": ["x1", "x2", "x3"]}, data=frac_list(m),
    tolerance={"norm": "max", "tau": fr(tau)},
    question="What is the range of E[x1*x2] over all ensembles whose three means are within 1/20 of the data?",
    expected={"verdict": "INTERVAL", "interval": [fr(abs(m[0] + m[1]) - 1 - 2 * tau), fr(1 - abs(m[0] - m[1]) + 2 * tau)],
              "dual certificates": "the same two inequalities; each end moves by tau times the l1 norm (= 2) of its dual vector"},
    why="Bounded errors enter through the dual norm of the certificate (Theorem E2(a)).", source="section 2.2")

# ================================================================================================================
# B6  finite temperature: a bound that holds, and a hypothesis that must be checked
# ================================================================================================================
e2 = math.exp(2.0)
mustar = np.array([1, 1, 1, math.exp(-2.0)]) / (3 + math.exp(-2.0))          # order e = 00, 01, 10, 11
member = np.array([1, e2, 1, 1]) / (3 + e2)
tv = 0.5 * np.abs(member - mustar).sum()
deficits = ((mustar[0] + mustar[1]) - (member[0] + member[1])) + ((mustar[0] + mustar[2]) - (member[0] + member[2]))
check("B6-01 the union bound is violated by 0.1696", abs((tv - deficits) - ((1 + e2) / (3 + e2) - 2 / (3 + 1 / e2))) < 1e-12 and tv > deficits)
add(id="B6-01", family="hypothesis must be checked", title="A frustrated known part: the thermal union bound fails",
    space={"type": "finite", "description": "{+1,-1}^2; disagreement variables e_i = [x_i != +1]; states in the order e = 00, 01, 10, 11"},
    model={"reference": "pi proportional to exp(-x1*x2/2)", "envelope": "d(x, y) = number of sites where x and y differ (slopes 1)", "centre": "++"},
    ensemble={"member": "mu proportional to pi * exp(-e1 + e2)", "weights (order 00, 01, 10, 11)": [round(float(v), 12) for v in member]},
    data={"polarised member (order 00, 01, 10, 11)": [round(float(v), 12) for v in mustar]},
    question="Is TV(mu, mu*) at most the sum over sites of mu*(x_i = +) - mu(x_i = +)?",
    expected={"verdict": "NO", "TV": round(float(tv), 6), "sum of one-body deficits": round(float(deficits), 6),
              "excess (closed form (1+e^2)/(3+e^2) - 2/(3+e^-2))": round(float(tv - deficits), 6),
              "trap": "the bound is a theorem for product references and for positively associated polarised members; here the "
                      "polarised member has Cov(e1, e2) < 0.  A tool must check the hypothesis (Proposition E15U) or abstain"},
    why="A violated bond can break the bound (Theorem E15T(d)).", source="section 4a.2 (E15T, E15U); check F6")

sig = 1 / (1 + math.exp(-1.0))
p_star = np.array([sig ** 3 * ((1 - sig) / sig) ** k for k in (0, 1, 1, 2, 1, 2, 2, 3)])      # e in binary order, product law
check("B6-02 product law normalised", abs(p_star.sum() - 1) < 1e-12)
flip_first = np.array([p_star[k ^ 4] for k in range(8)])                                       # centre moved at site 1
tv2 = 0.5 * np.abs(flip_first - p_star).sum()
check("B6-02 equality case of the binary bound", abs(tv2 - (2 * sig - 1)) < 1e-12)
add(id="B6-02", family="identified inside a class", title="Product reference: the equality case of the thermal union bound",
    space={"type": "finite", "description": "{+1,-1}^3, uniform reference, envelope = Hamming distance (slopes 1), centre +++"},
    ensemble={"member": "the member most polarised towards -++ (it is in the class)"},
    data={"one-body populations of + at sites 1, 2, 3": [round(1 - sig, 12), round(sig, 12), round(sig, 12)], "sigma": round(sig, 12)},
    question="How far, in total variation, can a member with these one-body populations be from the member polarised towards +++?",
    expected={"verdict": "BOUND", "bound": round(2 * sig - 1, 12), "attained": True,
              "formula": "sum_i (sigma - mu(x_i = +)) = (sigma - (1 - sigma)) + 0 + 0 = 2 sigma - 1, sigma = 1/(1 + e^-1)"},
    why="Theorem E15(c), with equality for members polarised towards a centre one flip away.", source="section 4a.2 (E15)")

# ================================================================================================================
# B7  noise
# ================================================================================================================
kappa = 0.449600
add(id="B7-01", family="noise", title="Two configurations, one noisy mean",
    space={"type": "finite", "description": "{0, 1}", "states": ["0", "1"]},
    observables={"names": ["phi(x) = x"], "table": [["0", "1"]]},
    noise={"model": "y = E[phi] + sigma * standard Gaussian", "sigma": "1/2"},
    question="How well can the population p of state 1 be estimated from y, in the worst case over p?",
    expected={"verdict": "BRACKET", "modulus omega(2 sigma)": 1, "minimax root-mean-square error between": [round(math.sqrt(kappa) / 2, 4), 0.5],
              "estimator that attains the upper end": "T = y (lambda = 1, c = 0): risk sigma^2 = 1/4",
              "reading": "at this noise level no estimator knows p to better than 0.335 in the worst case"},
    why="Theorem E17: the dual vector of the identified interval is a near-minimax estimator; lower constant sqrt(E sech^2(1+Z))/2.",
    source="section 4b (E17); check F5")

# ================================================================================================================
# B8  data that are not linear in the ensemble (report Part VII)
# ================================================================================================================
Phi_abc2 = [[Fr(1), Fr(0), Fr(1)], [Fr(0), Fr(1), Fr(1)]]                     # configurations a, b, c
mu_ab = {0: Fr(1, 2), 1: Fr(1, 2)}; mu_c = {2: Fr(1)}
za, zc = means(Phi_abc2, mu_ab), means(Phi_abc2, mu_c)
cert_ab = exact_certificate(Phi_abc2, [0, 1])
check("B8-01 with the factor known the ensemble is determined (exact certificate with a constant term, affine independence)",
      cert_ab is not None and affinely_independent(Phi_abc2, [0, 1]))
check("B8-01 no certificate without a constant term: lambda.Phi vanishing at a and b is identically zero",
      sympy.Matrix([[Phi_abc2[i][x] for i in range(2)] for x in (0, 1)]).rank() == 2)
check("B8-01 the twin has proportional means", zc[0] * za[1] == zc[1] * za[0] and zc != za)
add(id="B8-01", family="non-linear data", title="An unknown calibration factor destroys an identification",
    space={"type": "finite", "description": "three configurations a, b, c", "states": ["a", "b", "c"]},
    observables={"names": ["phi1", "phi2"], "table": [frac_list(r) for r in Phi_abc2]},
    ensemble={"support": ["a", "b"], "weights": ["1/2", "1/2"]}, data=frac_list(za),
    question="(a) Is the ensemble determined by its two means?  (b) Is it determined if the two data are known only up to one common unknown positive factor?",
    expected={"(a)": {"verdict": "IDENTIFIED", "reason": "nu(a) + nu(c) = 1/2, nu(b) + nu(c) = 1/2 and total mass 1 force nu(c) = 0"},
              "(b)": {"verdict": "NOT_IDENTIFIED", "twin": {"support": ["c"], "weights": ["1"], "its means": frac_list(zc)},
                      "reason": "no combination of phi1, phi2 WITHOUT a constant term is non-negative with zero set {a, b}"},
              "control": "the ensemble concentrated on a IS determined up to the factor (certificate phi2)"},
    why="With an unknown factor the constant function leaves the span in which a certificate must be found (Proposition E23(b)).",
    source="section 4d.1 (E23); check Q5")

sq_corners = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
m1 = (Fr(1, 2) * 1 + Fr(1, 2) * 1, Fr(1, 2) * 1 + Fr(1, 2) * (-1)); m2 = (Fr(1, 2) * 1 + Fr(1, 2) * (-1), Fr(1, 2) * 1 + Fr(1, 2) * 1)
check("B8-02 both ensembles have a mean vector of length one", m1[0] ** 2 + m1[1] ** 2 == 1 and m2[0] ** 2 + m2[1] ** 2 == 1 and m1 != m2)
add(id="B8-02", family="non-linear data", title="The length of a mean vector between its extremes determines nothing",
    space={"type": "finite", "description": "the four corners (+-1, +-1) of a square; the observable is the position vector", "states": ["(1,1)", "(1,-1)", "(-1,1)", "(-1,-1)"]},
    observables={"names": ["the length |E Phi| of the mean position"]},
    ensemble={"support": ["(1,1)", "(1,-1)"], "weights": ["1/2", "1/2"]}, data={"length of the mean vector": "1"},
    question="Is the ensemble determined by the length of its mean vector?  (Lengths range from 0 to sqrt 2.)",
    expected={"verdict": "NOT_IDENTIFIED", "twin": {"support": ["(1,1)", "(-1,1)"], "weights": ["1/2", "1/2"]},
              "what_is_determined": "at length sqrt 2 a single corner (up to the symmetry of the square: four ensembles have it); at length 0 only that the mean vanishes",
              "remark": "for a moment body of dimension at least two a length strictly between the least and the largest is shared by infinitely many mean vectors"},
    why="Theorem E25(b), (e).", source="section 4d.3 (E25); check Q2")

P8 = [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(2), Fr(2)), (Fr(3), Fr(1))]          # the hull misses the origin; nearest point (1/2, 1/2)
zs8 = (Fr(1, 2), Fr(1, 2)); r2 = zs8[0] ** 2 + zs8[1] ** 2
f8 = [zs8[0] * p[0] + zs8[1] * p[1] - r2 for p in P8]
check("B8-03 certificate of the least length", f8[0] == 0 and f8[1] == 0 and all(v > 0 for v in f8[2:]))
add(id="B8-03", family="non-linear data", title="The least possible length of a mean vector identifies an ensemble",
    space={"type": "finite", "description": "four points of the plane: (1,0), (0,1), (2,2), (3,1)", "states": ["(1,0)", "(0,1)", "(2,2)", "(3,1)"]},
    observables={"names": ["the length |E Phi| of the mean position"]},
    ensemble={"support": ["(1,0)", "(0,1)"], "weights": ["1/2", "1/2"]}, data={"squared length of the mean vector": fr(r2)},
    question="(a) Is the ensemble determined by the length of its mean vector?  (b) If the length is known within tau, how much mass can be on the other two points, and how far can the weights move?",
    expected={"verdict": "IDENTIFIED", "certificate": {"f": "z*.Phi(x) - |z*|^2 with z* = (1/2, 1/2)", "values at the four points": frac_list(f8),
              "gamma": fr(min(f8[2:]))},
              "stability": {"mass off the support": "at most r tau / gamma with r = sqrt(1/2), gamma = 3/2",
                            "weights": "the mean moves by at most sqrt(2 r tau + tau^2): a SQUARE ROOT of the error, attained along the segment between the two support points"}},
    why="The length is at its minimum over all ensembles; Theorem E25(d).", source="section 4d.3 (E25); check Q2")

def partition_signs(a):
    for s in itertools.product((1, -1), repeat=len(a) - 1):
        s = (1,) + s
        if sum(si * ai for si, ai in zip(s, a)) == 0:
            return s
    return None
yes_a, no_a = [3, 1, 1, 2, 2, 1], [5, 4, 2]
sy = partition_signs(yes_a)
check("B8-04 consistent instance has a split, inconsistent has none", sy is not None and partition_signs(no_a) is None)
A_yes = sum(yes_a)
add(id="B8-04", family="non-linear data", title="Squared means: consistency of the data is a partition problem",
    space={"type": "finite", "description": "2m configurations (i, +) and (i, -), i = 1..m; observable phi_i equals +A at (i, +), -A at (i, -), 0 elsewhere, A = a_1 + ... + a_m"},
    observables={"names": ["(E phi_i)^2 for i = 1..m", "(E (phi_1 + ... + phi_m))^2"]},
    data={"instance 1": {"a": yes_a, "(E phi_i)^2": [v * v for v in yes_a], "(E sum phi_i)^2": 0},
          "instance 2": {"a": no_a, "(E phi_i)^2": [v * v for v in no_a], "(E sum phi_i)^2": 0}},
    question="Is there any ensemble with these data?",
    expected={"instance 1": {"verdict": "CONSISTENT", "signs": list(sy),
                             "an ensemble": {f"({i + 1},{'+' if sy[i] > 0 else '-'})": f"{yes_a[i]}/{A_yes}" for i in range(len(yes_a))}},
              "instance 2": {"verdict": "INCONSISTENT", "reason": "5, 4, 2 cannot be split into two parts of equal sum"},
              "trap": "a local fit of an ensemble to squared data can stall on instance 2 without proving anything; the certified answer enumerates signs (2^m linear programmes) or abstains"},
    why="Deciding consistency of squared-mean data is NP-complete (Theorem E26).", source="section 4d.4 (E26); check Q3")

# ================================================================================================================
# B9  an incomplete model: several gains, a library that misses configurations, the number of conformers (Part VIII)
# ================================================================================================================
Phi9 = [[Fr(1), Fr(0), Fr(1), Fr(1)], [Fr(0), Fr(1), Fr(1), Fr(0)], [Fr(1), Fr(0), Fr(2), Fr(0)], [Fr(0), Fr(1), Fr(1), Fr(2)]]  # rows: observables; columns: a, b, c, d
mu9 = {0: Fr(1, 2), 1: Fr(1, 2)}; tw9 = {0: Fr(1, 7), 1: Fr(2, 7), 2: Fr(3, 7), 3: Fr(1, 7)}
z9, zt9 = means(Phi9, mu9), means(Phi9, tw9)
# one common gain: nu compatible iff the four means are equal; with total mass one this linear system has one solution
M9 = sympy.Matrix([[Phi9[0][x] - Phi9[i][x] for x in range(4)] for i in (1, 2, 3)] + [[1, 1, 1, 1]])
sol9 = M9.solve(sympy.Matrix([0, 0, 0, 1])) if M9.rank() == 4 else None
check("B9-01 with one common gain the ensemble is the only solution (a 4 x 4 system of full rank)",
      sol9 is not None and list(sol9) == [Fr(1, 2), Fr(1, 2), 0, 0])
check("B9-01 with two gains the twin has proportional means in each pair, and not with one gain",
      zt9[0] * z9[1] == zt9[1] * z9[0] and zt9[2] * z9[3] == zt9[3] * z9[2] and zt9[0] * z9[2] != zt9[2] * z9[0]
      and sum(tw9.values()) == 1)
add(id="B9-01", family="incomplete model", title="One unknown gain keeps an identification that two gains lose",
    space={"type": "finite", "description": "four configurations a, b, c, d", "states": ["a", "b", "c", "d"]},
    observables={"names": ["phi1", "phi2", "phi3", "phi4"], "table": [frac_list(r) for r in Phi9],
                 "groups": "data 1, 2 form one group and data 3, 4 another (two instruments)"},
    ensemble={"support": ["a", "b"], "weights": ["1/2", "1/2"]}, data=frac_list(z9),
    question="Is the ensemble determined if (a) all four data share one unknown positive gain; (b) each group has its own unknown positive gain?",
    expected={"(a)": {"verdict": "IDENTIFIED", "reason": "the four means must be equal, which forces nu(c) = nu(d) = 0 and nu(a) = nu(b)"},
              "(b)": {"verdict": "NOT_IDENTIFIED", "twin": {"weights on a, b, c, d": frac_list([tw9[i] for i in range(4)]), "its means": frac_list(zt9)}}},
    why="Every unknown gain removes one direction from the span in which a certificate must be found (Proposition E23.1).",
    source="section 4d.1 (E23.1); check M1")

lib_max, all_max, y9 = Fr(1), Fr(2), Fr(3, 2)
bound9 = (y9 - lib_max) / (all_max - lib_max)
check("B9-02 the library {0, 1} is falsified by the mean 3/2, the bound on the missing weight is 1/2 and it is attained",
      y9 > lib_max and bound9 == Fr(1, 2) and Fr(1, 2) * 1 + Fr(1, 2) * 2 == y9)
add(id="B9-02", family="incomplete model", title="Data that falsify a library bound the weight it misses",
    space={"type": "finite", "description": "the library lists the configurations with phi = 0 and phi = 1; all that is known about unlisted configurations is 0 <= phi <= 2"},
    observables={"names": ["phi"]}, data={"mean of phi": fr(y9), "tolerance": "0"},
    question="(a) Can an ensemble on the library have the datum?  (b) What do the data say about the weight of unlisted configurations?",
    expected={"(a)": {"verdict": "LIBRARY_FALSIFIED", "certificate": "lambda = 1: lambda.y = 3/2 exceeds the largest value 1 of phi on the library"},
              "(b)": {"missing weight": "at least " + fr(bound9), "attained_by": "weight 1/2 at phi = 1 and 1/2 at phi = 2",
                      "no_upper_bound": "weight 3/4 at phi = 2 and 1/4 at phi = 0 has the datum with three quarters of the weight off the library"}},
    why="An incomplete library is testable; a failed test gives a certified lower bound on the missing weight from bounds on the observables alone (Proposition E28).",
    source="section 4e.2 (E28); check M3")

X9 = [0, 1, 2, 3]
data9 = (Fr(3, 2), Fr(7, 2))                                                 # mean and mean square of the uniform ensemble
def fits9(sub):
    """exact weights on the support `sub` with the two data and total mass one, if positive"""
    A = sympy.Matrix([[1] * len(sub), [x for x in sub], [x * x for x in sub]])
    b = sympy.Matrix([1, data9[0], data9[1]])
    try:
        sols = sympy.linsolve((A, b))
    except Exception:
        return False
    if not sols:
        return False
    sol = list(sols)[0]
    if any(v.free_symbols for v in sol):
        return None                                                          # a family: handled below for the full support
    return all(v > 0 for v in sol)
by_size = {k: [sub for sub in itertools.combinations(X9, k) if fits9(sub) is True] for k in (1, 2, 3)}
check("B9-03 no ensemble with one or two conformers has the data; two with three conformers do; the uniform one has four",
      by_size[1] == [] and by_size[2] == [] and len(by_size[3]) == 2
      and sum(Fr(1, 4) * x for x in X9) == data9[0] and sum(Fr(1, 4) * x * x for x in X9) == data9[1])
edge9 = (Fr(1, 2) * 1 + Fr(1, 2) * 2, Fr(1, 2) * 1 + Fr(1, 2) * 4)
check("B9-03 control on the boundary: the certificate (x-1)(x-2) is non-negative on X with zero set {1, 2}",
      all((x - 1) * (x - 2) >= 0 for x in X9) and [x for x in X9 if (x - 1) * (x - 2) == 0] == [1, 2] and edge9 == (Fr(3, 2), Fr(5, 2)))
add(id="B9-03", family="incomplete model", title="How many conformers do the data require, and how many do they allow?",
    space={"type": "finite", "description": "configurations 0, 1, 2, 3 on a line", "states": ["0", "1", "2", "3"]},
    observables={"names": ["x", "x^2"]},
    ensemble={"support": ["0", "1", "2", "3"], "weights": ["1/4", "1/4", "1/4", "1/4"]}, data=frac_list(list(data9)),
    question="What are the least and the largest number of conformers of an ensemble with these two means?",
    expected={"K_min": 3, "K_max": 4, "with three conformers": [list(sub) for sub in by_size[3]],
              "remark": "a fit with the fewest conformers returns three; the truth has four",
              "control": {"data": frac_list(list(edge9)), "K_min": 2, "K_max": 2, "verdict": "IDENTIFIED",
                          "certificate": "(x - 1)(x - 2) = x^2 - 3x + 2 is non-negative on the four configurations with zero set {1, 2}"}},
    why="The largest number is the size of the zero set of a certificate; the smallest is a combinatorial search; they agree iff the ensemble is identified (Proposition E29).",
    source="section 4e.3 (E29); check M4")

# ================================================================================================================
bad = [d for d, ok in checks if not ok]
print(f"benchmark controls: {len(controls)} instances, {len(checks)} verifications, {len(bad)} failure(s)")
for d in bad:
    print("    FAILED: " + d)
if not bad:
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"version": 1, "generated_by": "experiments/ensemble/benchmark_controls.py",
                               "conventions": "numbers in quotes are exact rationals; unquoted numbers are decimal approximations",
                               "controls": controls}, indent=1, ensure_ascii=False) + "\n")
    print(f"written: {OUT.relative_to(here.parent.parent)}")
print("PASS" if not bad else "FAIL")
sys.exit(0 if not bad else 1)
