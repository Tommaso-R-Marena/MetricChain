"""GEOMETRY-REQ-0001, item 1, validation at n = 9: a computer-assisted PROOF that, for a given
rational witness with K = 2, n = 9, the affine system

    rank P <= 3,   e^T P e = |e|^2 on the 15 constrained edge vectors

has exactly 48 solutions over C (the two forced ones and 46 others), all reduced, together with
the exact number of real ones and of real positive semidefinite ones.

Run from the repository root:

    python experiments/eng/geometry_req1/item1_n9_exact_count.py           # three witnesses: 10 min
    python experiments/eng/geometry_req1/item1_n9_exact_count.py --quick   # one witness: 3 min

One of the three witnesses is the n = 10 witness of item 1 without its last atom: for it the script
also evaluates the two equations of the tenth atom on the 46 certified boxes.  If every non-forced
solution violates one of them (the ball of the residual excludes 0), this is a second,
independent proof that the n = 10 system has no affine solution besides E_1 and E_2.

Output: experiments/eng/geometry_req1/results/item1_n9_exact_count.json

Notation: x = (x_0..x_6) homogeneous coordinates on the pencil L = Q E_1 + N(z) (P = sum x_i B_i),
h = x_0 + x_1, S = Q[x], J the ideal of the 120 minors of order 4, W = (S_7 / J_7)^* the space of
linear functionals on septics vanishing on J_7 (over C).

The proof has four computed ingredients and one paper argument.

 (1) [modular rank, rigorous as an inequality]  The Macaulay matrix of degree 7 (all products of
     a cubic monomial and a minor) has rank 1574 modulo a prime, hence rank >= 1574 over Q, hence
     dim W <= 1716 - 1574 = 142.

 (2) [exact / modular rank, rigorous]  Functionals at infinity.  All minors of order 4 vanish to
     order >= 2 at every matrix of rank <= 2 (their first partial derivatives are combinations of
     minors of order 3).  The rank-2 locus of P(N(z)) consists of two lines l_1, l_2 and two
     isolated points q_1, q_2 (enslib.rank2_families_at_infinity, exact).  Hence the following
     functionals on S_7 vanish on J_7:
       - for each line (spanned by integer points a, b): the 8 coefficients of g(s a + t b) and
         the 7 x 7 coefficients of (d_i g)(s a + t b), i = 0..6;
       - for each isolated point q: g -> sum_{i<=j} c_ij (d_i d_j g)(q) for every c with
         sum_{i<=j} c_ij (d_i d_j f)(q) = 0 for all 120 minors f  (then for a multiple m f:
         d_i d_j (m f)(q) = m(q) d_i d_j f(q), because f and its first derivatives vanish at q).
         The vectors c are computed exactly over Q and H c = 0 is verified in integers.
     All of them vanish on h^3 S_4 as well (h vanishes at infinity, these are differential
     conditions of order <= 2 at points at infinity).  Their matrix is an integer matrix; its rank
     modulo a prime is 94, so at least 94 of them are linearly independent over Q.
     [As a guard against implementation errors the script also checks modulo p that every one of
     these rows annihilates J_7 and h^3 S_4.]

 (3) [ball arithmetic, rigorous]  46 pairwise disjoint boxes, disjoint from E_1 and E_2, each
     containing exactly one solution of the square system (Krawczyk test, exact rational data, see
     item1_affine_solutions.py), all of rank 3; with E_1 and E_2: 48 distinct affine solutions.
     Their evaluations are linearly independent on cubic forms: a 48 x 48 minor of the matrix
     (monomial of degree 3)(point) has a determinant whose ball does not contain 0.

 (4) [paper]  Each affine solution p gives ev_p in W.  The 94 functionals of (2) vanish on h^4 S_3
     while the 48 evaluations are independent there (ev_p(h^4 g) = g(p)); so the 142 functionals
     are independent, and by (1) they span W.  Let q be ANY affine solution (h(q) = 1).  Then
     ev_q = sum_p c_p ev_p + (a combination of the functionals at infinity).  Restricting to
     h^3 S_4:  f(q) = sum_p c_p f(p) for all quartic forms f.  With f = h g:  g(q) = sum_p c_p g(p)
     for all cubics g;  with f = l g, l linear:  sum_p c_p (l(p) - l(q)) g(p) = 0 for all cubics g,
     so c_p (l(p) - l(q)) = 0 for every p and every l by (3).  If q were none of the 48 points,
     all c_p would vanish and g(q) = 0 for every cubic g, contradicting h(q)^3 = 1.  Hence the
     affine solutions over C are exactly the 48 points.  Each of the 46 is a non-singular zero of
     the square system at a point of rank 3, i.e. a reduced point of the scheme; E_1 and E_2 are
     reduced by the tangent-space criterion (enslib.forced_point_tangent_ranks).

Real and semidefinite solutions: decided box by box in ball arithmetic (item1_affine_solutions).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import scipy.linalg as sla  # noqa: E402

import enslib as el  # noqa: E402
import item1_affine_solutions as aff  # noqa: E402

flint = aff.flint
P = 2305843009213693951
PIN = "d84a43b"
V = 7
D = 7


# ------------------------------------------------------------------------------ exact helpers
def pencil_coordinates(S, mats):
    """Exact coordinates x with S = sum_k x_k B_k (S must lie in the span)."""
    idx = el.sym_index(6)
    rows = [[Fr(mats[k][i][j]) for k in range(len(mats))] + [Fr(S[i][j])] for (i, j) in idx]
    R, piv = el.rref_fraction(rows)
    assert piv == list(range(len(mats))), "not in the span of the pencil"
    return [R[k][len(mats)] for k in range(len(mats))]


def second_derivatives(alpha, pw, mod=None):
    """[(d_a d_b x^alpha)(q) for a <= b], q given through its table of powers pw[i][k] = q_i^k."""
    out = []
    v = len(alpha)
    for a in range(v):
        for b in range(a, v):
            if a == b:
                if alpha[a] < 2:
                    out.append(0)
                    continue
                coef = alpha[a] * (alpha[a] - 1)
                ex = [alpha[i] - (2 if i == a else 0) for i in range(v)]
            else:
                if alpha[a] < 1 or alpha[b] < 1:
                    out.append(0)
                    continue
                coef = alpha[a] * alpha[b]
                ex = [alpha[i] - (1 if i in (a, b) else 0) for i in range(v)]
            val = coef
            for i in range(v):
                if ex[i]:
                    val = val * pw[i][ex[i]]
                    if mod:
                        val %= mod
            out.append(val % mod if mod else val)
    return out


def hessian_kernel(polys, q):
    """Integer vectors c (28 entries, pairs a <= b) with sum c_ab (d_a d_b f)(q) = 0 for every
    minor f; exact (the kernel is computed by FLINT and verified here in integers)."""
    pw = [[q[i] ** k for k in range(5)] for i in range(V)]
    cache = {}
    H = []
    for f in polys:
        row = [0] * 28
        for beta, coef in f.items():
            if beta not in cache:
                cache[beta] = second_derivatives(beta, pw)
            sd = cache[beta]
            for t in range(28):
                if sd[t]:
                    row[t] += coef * sd[t]
        H.append(row)
    X, nullity = flint.fmpz_mat(H).nullspace()
    Xl = X.tolist()
    ker = []
    for col in range(int(nullity)):
        c = el.primitive_integer_vector([int(Xl[r][col]) for r in range(28)])
        assert all(sum(h * x for h, x in zip(row, c)) == 0 for row in H)      # exact check
        ker.append(c)
    return ker, el.rank_mod_p(H, P)


def conv(f, g, p):
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % p
    return out


def binary_forms(a, b, degree, p):
    """{alpha: coefficients (in powers of t) of prod_i (a_i s + b_i t)^alpha_i mod p}."""
    lin = []
    for i in range(V):
        table = [[1]]
        for _ in range(degree):
            table.append(conv(table[-1], [a[i] % p, b[i] % p], p))
        lin.append(table)
    out = {}
    for alpha in el.monomials(V, degree):
        f = [1]
        for i in range(V):
            if alpha[i]:
                f = conv(f, lin[i][alpha[i]], p)
        out[alpha] = f
    return out


def functionals_at_infinity(z, mats, polys, p):
    """Rows (over the 1716 septic monomials, modulo p) of the functionals of ingredient (2)."""
    mons = el.monomials(V, D)
    fams = el.rank2_families_at_infinity(z)
    rows, info = [], {"lines": 0, "isolated_points": 0, "hessian_kernel_dimensions": [],
                      "hessian_ranks_mod_p": []}
    for fam in fams:
        if fam["dimension"] == 1:
            pts = [el.primitive_integer_vector(pencil_coordinates(el.sym_outer(la, mu), mats))
                   for la in fam["ann_lambda"] for mu in fam["ann_mu"]]
            assert len(pts) == 2 and all(q[0] + q[1] == 0 for q in pts)
            a, b = pts
            f7 = binary_forms(a, b, 7, p)
            f6 = binary_forms(a, b, 6, p)
            for k in range(8):
                rows.append([f7[al][k] for al in mons])
            for i in range(V):
                for k in range(7):
                    row = []
                    for al in mons:
                        if al[i]:
                            lower = tuple(x - (1 if j == i else 0) for j, x in enumerate(al))
                            row.append(al[i] * f6[lower][k] % p)
                        else:
                            row.append(0)
                    rows.append(row)
            info["lines"] += 1
        elif fam["dimension"] == 0:
            S = el.sym_outer(fam["ann_lambda"][0], fam["ann_mu"][0])
            q = el.primitive_integer_vector(pencil_coordinates(S, mats))
            assert q[0] + q[1] == 0
            ker, hrank = hessian_kernel(polys, q)
            info["hessian_kernel_dimensions"].append(len(ker))
            info["hessian_ranks_mod_p"].append(hrank)
            pw = [[pow(q[i] % p, k, p) for k in range(8)] for i in range(V)]
            sd = [second_derivatives(al, pw, mod=p) for al in mons]
            for c in ker:
                cm = [x % p for x in c]
                rows.append([sum(cm[t] * s[t] for t in range(28)) % p for s in sd])
            info["isolated_points"] += 1
        else:
            raise AssertionError("unexpected family of rank-2 quadrics")
    return rows, info


def macaulay_rref_mod_p(polys, p):
    red = [{e: c % p for e, c in f.items()} for f in polys]
    mons4 = el.monomials(V, 4)
    R4, r4 = flint.nmod_mat(el.dense_rows(red, V, 4), p).rref()
    R4l = R4.tolist()
    basis4 = [{mons4[j]: int(c) for j, c in enumerate(R4l[i]) if int(c)} for i in range(r4)]
    rows = el.dense_rows(el.macaulay_rows(basis4, V, 4, D), V, D)
    R, r = flint.nmod_mat(rows, p).rref()
    return flint.nmod_mat([[int(c) for c in row] for row in R.tolist()[:r]], p), int(r)


# ------------------------------------------------------------------------------ driver
def prove(name, tangents, prec=400, rad_exp=-200, extension=None):
    t0 = time.time()
    res = {"witness": name, "n": 9, "tangents": [[str(t) for t in row] for row in tangents]}
    chains, z = el.ensemble(tangents)
    mats, rank, dimN = el.pencil_basis(z)
    assert rank == 15 and len(mats) == V
    polys = [f for _, f in el.all_4x4_minors(mats)]
    mons = el.monomials(V, D)
    pos = {e: i for i, e in enumerate(mons)}

    timing = {}
    # (1) modular rank of the Macaulay matrix
    t1 = time.time()
    RD, r7 = macaulay_rref_mod_p(polys, P)
    timing["step1_macaulay"] = round(time.time() - t1, 1)
    res["step1_macaulay_rank_mod_p"] = r7
    res["step1_dim_W_at_most"] = len(mons) - r7

    # (2) functionals at infinity
    t1 = time.time()
    rows, info = functionals_at_infinity(z, mats, polys, P)
    Fm = flint.nmod_mat(rows, P)
    res["step2"] = dict(info, functionals=len(rows), rank_mod_p=int(Fm.rank()))
    zero = flint.nmod_mat(r7, len(rows), P)
    res["step2"]["guard_all_annihilate_J7_mod_p"] = (RD * Fm.transpose()).tolist() == zero.tolist()
    hform = {aff.unit(V, 0): 1, aff.unit(V, 1): 1}
    h3 = el.pmul(el.pmul(hform, hform), hform)
    h3S4 = []
    for m4 in el.monomials(V, 4):
        row = [0] * len(mons)
        for e, c in el.pmul(h3, {m4: 1}).items():
            row[pos[e]] = c % P
        h3S4.append(row)
    Hm = flint.nmod_mat(h3S4, P)
    res["step2"]["guard_all_annihilate_h3_S4_mod_p"] = \
        (Hm * Fm.transpose()).tolist() == flint.nmod_mat(len(h3S4), len(rows), P).tolist()

    timing["step2_functionals_and_guards"] = round(time.time() - t1, 1)

    # (3) the affine solutions, certified
    t1 = time.time()
    cands = aff.numeric_candidates(z, 48)
    timing["step3_float_candidates"] = round(time.time() - t1, 1)
    t1 = time.time()
    sols = aff.certify_all(z, cands, prec=prec, rad_exp=rad_exp)
    timing["step3_polish_and_krawczyk"] = round(time.time() - t1, 1)
    t1 = time.time()
    cert = [s for s in sols if s["certified"]]
    nonforced = [s for s in cert if s["forced_point"] is None]
    res["step3"] = {
        "certified_boxes": len(cert),
        "forced_points_recovered": sorted(s["forced_point"] for s in cert if s["forced_point"]),
        "non_forced": len(nonforced),
        "boxes_pairwise_disjoint": aff.pairwise_disjoint(sols),
        "all_non_forced_of_rank_3": all(s["rank_3_certified"] for s in nonforced),
        "box_radius_log2_relative": rad_exp,
        "real": sum(1 for s in nonforced if s["real"]),
        "non_real": sum(1 for s in nonforced if s["non_real_certified"]),
        "real_positive_semidefinite": sum(1 for s in nonforced if s["real"]
                                          and s.get("definiteness", "").startswith("positive")),
        "real_not_semidefinite": sum(1 for s in nonforced if s["real"]
                                     and s.get("definiteness", "").startswith("not")),
        "real_undecided": sum(1 for s in nonforced if s["real"] and s.get("definiteness") == "undecided"),
    }
    # pencil coordinates of the points as balls: x = T^{-1} (seven entries of P)
    flint.ctx.prec = prec
    idx = el.sym_index(6)
    M = [[Fr(mats[k][i][j]) for (i, j) in idx] for k in range(V)]          # 7 x 21
    _, sel = el.rref_fraction(M)
    assert len(sel) == V
    Tinv = flint.fmpq_mat([[flint.fmpq(mats[k][idx[c][0]][idx[c][1]]) for k in range(V)] for c in sel]).inv()
    Tl = [[flint.acb(flint.arb(Tinv[i, j])) for j in range(V)] for i in range(V)]
    scale = [float(max(abs(x) for row in mats[k] for x in row)) for k in range(V)]
    points = [[flint.acb(1 if i == k else 0) for i in range(V)] for k in (0, 1)]      # E_1, E_2
    hsum_ok = True
    for s in nonforced:
        Pb = s["_balls"]
        vec = [Pb[idx[c][0]][idx[c][1]] for c in sel]
        x = [sum(Tl[i][j] * vec[j] for j in range(V)) for i in range(V)]
        hsum_ok = hsum_ok and (x[0] + x[1]).contains(flint.acb(1))
        points.append(x)
    res["step3"]["h_equals_1_on_all_boxes"] = bool(hsum_ok)
    # scaled coordinates (a diagonal change of coordinates; independence is unaffected)
    pts = [[x[i] * flint.arb(scale[i]) for i in range(V)] for x in points]
    mons3 = el.monomials(V, 3)

    def mono(x, e):
        val = flint.acb(1)
        for i in range(V):
            for _ in range(e[i]):
                val = val * x[i]
        return val

    E = [[mono(x, e) for e in mons3] for x in pts]                                 # 48 x 84 balls
    Emid = np.array([[complex(float(c.real.mid()), float(c.imag.mid())) for c in row] for row in E])
    if len(pts) <= len(mons3):
        _, _, piv = sla.qr(Emid, pivoting=True, mode="economic")
        cols = sorted(int(c) for c in piv[:len(pts)])
        det = flint.acb_mat([[row[c] for c in cols] for row in E]).det()
        nonzero = not det.contains(flint.acb(0))
    else:
        cols, nonzero = [], False
    res["step3"]["points"] = len(pts)
    res["step3"]["evaluations_independent_on_cubics"] = bool(nonzero)
    res["step3"]["cubic_monomials_used"] = len(cols)

    # optional: the nine-atom ensemble is the ten-atom ensemble `extension` without its last atom;
    # evaluate the two extra equations (bond 8-9, one-three vector 7-9) on every box
    if extension is not None:
        z10 = el.ensemble(extension)[1]
        assert [tuple(p) for p in z10[:9]] == [tuple(p) for p in z]
        extra = [el.edge_vectors(z10)[8], el.edge_vectors(z10)[16]]       # (e, l^2): last bond, last 1-3
        assert extra[0][1] == 1 and extra[1][1] == el.ONE3_2
        violating = 0
        smallest = None
        for s in nonforced:
            Pb = s["_balls"]
            bad = False
            best = flint.arb(0)
            for e, l2 in extra:
                ev = [flint.acb(aff.arb_q(x)) for x in e]
                val = sum(ev[i] * Pb[i][j] * ev[j] for i in range(6) for j in range(6)) - flint.acb(aff.arb_q(l2))
                if not val.contains(flint.acb(0)):
                    bad = True
                low = val.abs_lower()
                if low > best:
                    best = low
            violating += bad
            if smallest is None or best < smallest:
                smallest = best
        res["solutions"] = sorted(
            [{k: v for k, v in s.items() if k != "_balls"} for s in nonforced],
            key=lambda s: s["max_abs_entry"])
        res["extension_to_n10"] = {
            "smallest_certified_residual_of_the_extra_equations": smallest.str(8, radius=False),
            "description": "this ensemble is the n = 10 witness without its last atom; a solution "
                           "of the n = 10 system is a solution of this one that also satisfies the "
                           "two equations of the last atom",
            "non_forced_solutions_violating_an_extra_equation": violating,
            "non_forced_solutions": len(nonforced),
            "only_forced_points_survive": violating == len(nonforced)}

    timing["step3_independence_and_extension"] = round(time.time() - t1, 1)
    res["timing_seconds"] = timing

    # (4) conclusion
    ok = (res["step1_dim_W_at_most"] == 142 and res["step2"]["rank_mod_p"] == 94
          and res["step2"]["guard_all_annihilate_J7_mod_p"] and res["step2"]["guard_all_annihilate_h3_S4_mod_p"]
          and res["step3"]["points"] == 48 and res["step3"]["non_forced"] == 46
          and res["step3"]["forced_points_recovered"] == ["E_1", "E_2"]
          and res["step3"]["boxes_pairwise_disjoint"] and res["step3"]["all_non_forced_of_rank_3"]
          and res["step3"]["evaluations_independent_on_cubics"] and res["step3"]["h_equals_1_on_all_boxes"]
          and res["step3"]["real"] + res["step3"]["non_real"] == 46
          and res["step3"]["real_undecided"] == 0)
    dN, r22, r11 = el.forced_point_tangent_ranks(z)
    res["forced_points_reduced"] = (r22 == dN and r11 == dN)
    res["proved"] = bool(ok and res["forced_points_reduced"])
    res["statement"] = (
        "the affine system at n = 9 has exactly 48 solutions over C, all reduced: E_1, E_2 and 46 "
        "others of rank 3, of which %d are real (%d positive semidefinite, %d with a negative "
        "eigenvalue) and %d are not real" % (res["step3"]["real"], res["step3"]["real_positive_semidefinite"],
                                              res["step3"]["real_not_semidefinite"], res["step3"]["non_real"])
        if res["proved"] else "NOT PROVED: see the individual checks")
    res["seconds"] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    t10 = el.geometry_witness_tangents(2, 10, 0)
    jobs = [("geometry_seed_0", el.geometry_witness_tangents(2, 9, 0), None)]
    if not args.quick:
        jobs.append(("geometry_seed_0_n10_without_last_atom", [row[:6] for row in t10], t10))
        jobs.append(("geometry_seed_1", el.geometry_witness_tangents(2, 9, 1), None))
    out = {"request": "GEOMETRY-REQ-0001 item 1 (validation at n = 9: exact count of affine solutions)",
           "geometry_commit": PIN, "prime": str(P), "ball_precision_bits": 400,
           "python_flint": flint.__version__, "results": []}
    for name, tans, ext in jobs:
        r = prove(name, tans, extension=ext)
        out["results"].append(r)
        print(f"{name}: dim W <= {r['step1_dim_W_at_most']}; functionals at infinity: rank "
              f"{r['step2']['rank_mod_p']} of {r['step2']['functionals']} (guards "
              f"{r['step2']['guard_all_annihilate_J7_mod_p']}, {r['step2']['guard_all_annihilate_h3_S4_mod_p']}); "
              f"points {r['step3']['points']} (independent on cubics: "
              f"{r['step3']['evaluations_independent_on_cubics']}); proved: {r['proved']} [{r['seconds']}s]")
        print("   ", r["statement"], flush=True)
        if "extension_to_n10" in r:
            x = r["extension_to_n10"]
            print(f"    extension to n = 10: {x['non_forced_solutions_violating_an_extra_equation']} of "
                  f"{x['non_forced_solutions']} non-forced solutions violate an equation of the tenth atom",
                  flush=True)
    path = HERE / "results" / ("item1_n9_exact_count_quick.json" if args.quick else "item1_n9_exact_count.json")
    path.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
