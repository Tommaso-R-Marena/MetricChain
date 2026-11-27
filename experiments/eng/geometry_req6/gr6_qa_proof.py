"""(Q-a) of GEOMETRY-REQ-0006: the global maximisers of H = H_c on the torus T^4 of torsions.

TRUSTED: every function of this file except `clusters` (a grouping heuristic whose output is
re-checked by `inside`).  Angles in units of pi (tau = theta / pi), as in gr6_kernel.py.

Two certificates of the same statement are implemented; they share the local step (L) and the
branch-and-bound loop, and differ in the function that bounds H on a box.

Certificate D (direct, on the 4-torus; `certify_direct`)
--------------------------------------------------------
(D-X) Exclusion.  Let L <= max H (L = a lower bound of H at one point).  `branch_and_bound`
      splits [-pi, pi]^4 into grid boxes and returns those on which sup H < L is NOT established
      by `H_upper`; on every other box of the tiling H < L <= max H.
(L)   Local step, `concavity_certificate`, for a box B of R^4: the Hessian of H is negative
      definite at every point of B, and H has a critical point theta^ in a tiny box inside B
      (Krawczyk).  Then H is strictly concave on the convex set B, theta^ is its only critical
      point in B, and H < H(theta^) on B minus {theta^}.                                   (L0)
(D-C) Conclusion.  If every unresolved box lies in one of two boxes B_+ and B_- with local
      certificates around +tau~ and -tau~, then H < L <= max H off B_+ u B_- and (L0) holds on
      each: the global maximisers form a non-empty subset of {theta^_+, theta^_-}.  H is even
      (no monomial with an odd number of sines: asserted), so -theta^_+ is a critical point; it
      is certified to lie in B_-, which contains only one: theta^_- = -theta^_+ and
      H(theta^_-) = H(theta^_+).  Hence both are global maximisers and every other theta is
      strictly below.

Certificate R (reduced to the 2-torus of the two middle torsions; `certify`)
----------------------------------------------------------------------------
(R)   No pair of F spans both the first and the last torsion, so no monomial of H contains both
      theta_0 and theta_3 (checked on the support of the form in `reduce_ends`), hence

          H(theta) = A + V1 cos theta_0 + V2 sin theta_0 + W1 cos theta_3 + W2 sin theta_3,

      with A, V = (V1, V2), W = (W1, W2) forms in (theta_1, theta_2) only.  By Cauchy-Schwarz

          H(theta) <= G(theta_1, theta_2) := A + |V| + |W|      for every theta in T^4,   (R1)

      with equality iff (cos theta_0, sin theta_0) = V/|V| and (cos theta_3, sin theta_3) = W/|W|
      (where V != 0 and W != 0).                                                          (R2)
(R-X) Exclusion.  `branch_and_bound` with `G_upper` on [-pi, pi]^2: on every box that is not
      returned, G < L, so by (R1) H < L on the cylinder T x box x T over it.
(R-L) Local step, `local_certificate`, for a box B' of the (theta_1, theta_2)-plane: V != 0 and
      W != 0 on B', with polar angles in arcs B_0, B_3, and (L) holds for B = B_0 x B' x B_3.
      For theta in the cylinder T x B' x T the point theta+ = (arg V, theta_1, theta_2, arg W)
      lies in B (mod 2 pi), and by (R1), (R2), (L0):
      H(theta) <= G(theta_1, theta_2) = H(theta+) <= H(theta^), with equality iff
      theta = theta+ = theta^ (mod 2 pi).  So

          H <= H(theta^) on the cylinder over B', with equality only at theta^.            (L1)
(R-C) Conclusion: as (D-C), with the cylinders over B'_+ and B'_- in place of B_+ and B_-.
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr
from itertools import product

from flint import arb

from gr6_kernel import (arc_hull, ball, krawczyk, ma_eval, ma_range, point, sym_eig_enclosure, to_fraction)
from gr6_model import derivative, f_add, f_scale, odd_sine_monomials


# ------------------------------------------------------------------ grids and branch and bound
def grid_arc(level, j):
    """Arc number j (0 <= j < 2^level) of the uniform partition of [-1, 1] into 2^level arcs."""
    return Fr(2 * j, 2 ** level) - 1, Fr(2 * (j + 1), 2 ** level) - 1


class Grid:
    """Cache of the hulls (kernel.arc_hull) of the grid arcs."""

    def __init__(self):
        self._hull = {}

    def hull(self, level, j):
        key = (level, j)
        if key not in self._hull:
            self._hull[key] = arc_hull(*grid_arc(level, j))
        return self._hull[key]


def root_boxes(level, dim):
    """All boxes (level, j_1, .., j_dim) of the level-`level` grid: they tile [-1, 1]^dim."""
    assert level >= 2                           # arcs of at most a quarter turn
    return [(level,) + js for js in product(range(2 ** level), repeat=dim)]


def children(box):
    """The 2^dim boxes of the next level that tile `box`."""
    return [(box[0] + 1,) + tuple(2 * j + b for j, b in zip(box[1:], bits))
            for bits in product((0, 1), repeat=len(box) - 1)]


def branch_and_bound(upper, threshold, start, max_level, stats=None, excluded=None):
    """Boxes descending from `start` on which upper(box) < threshold does not hold.

    upper(box) must be an exact number >= the supremum over the box of the function to exclude.
    Invariant: the union of the boxes in `start` is the union of the boxes excluded so far, the
    returned boxes, and the boxes on the stack (a box is replaced by its `children`).
    `stats[level] = [boxes examined, boxes excluded]`; the excluded boxes are appended to
    `excluded` if given."""
    stats = {} if stats is None else stats
    unresolved, stack = [], list(start)
    while stack:
        box = stack.pop()
        st = stats.setdefault(box[0], [0, 0])
        st[0] += 1
        if upper(box) < threshold:
            st[1] += 1
            if excluded is not None:
                excluded.append(box)
        elif box[0] >= max_level:
            unresolved.append(box)
        else:
            stack += children(box)
    return unresolved


def is_partition(leaves):
    """Exact test that the grid boxes `leaves` (of any levels) tile [-1, 1]^dim: no box is
    repeated or contained in another one, and the volumes add up to the volume of the cube."""
    seen = set(leaves)
    if len(seen) != len(leaves):
        return False
    dim = len(leaves[0]) - 1
    for box in leaves:
        for up in range(1, box[0] + 1):
            if (box[0] - up,) + tuple(j >> up for j in box[1:]) in seen:
                return False
    return sum(Fr(1, 2 ** (dim * box[0])) for box in leaves) == 1


def clusters(boxes):
    """Heuristic (not trusted): group grid boxes of one level into classes of boxes that touch
    (also across the seam theta = +-pi) and return for each class (sides, members), `sides` a
    bounding box [(lo, hi)] * dim in unwrapped tau coordinates."""
    if not boxes:
        return []
    level, dim = boxes[0][0], len(boxes[0]) - 1
    assert all(b[0] == level for b in boxes)
    n = 2 ** level
    todo = {b[1:] for b in boxes}
    steps = list(product((-1, 0, 1), repeat=dim))
    out = []
    while todo:
        seed = min(todo)
        todo.discard(seed)
        comp = {seed: seed}                       # box -> unwrapped index
        front = [seed]
        while front:
            b = front.pop()
            u = comp[b]
            for step in steps:
                nb = tuple((j + s) % n for j, s in zip(b, step))
                if nb in todo:
                    todo.discard(nb)
                    comp[nb] = tuple(x + s for x, s in zip(u, step))
                    front.append(nb)
        sides = tuple((Fr(2 * min(u[k] for u in comp.values()), n) - 1,
                       Fr(2 * (max(u[k] for u in comp.values()) + 1), n) - 1) for k in range(dim))
        out.append((sides, sorted((level,) + b for b in comp)))
    return out


def inside(box, sides):
    """Exact test: the grid box lies in the box `sides` modulo 2 (tau units)."""
    return all(any(lo <= a + 2 * s and b + 2 * s <= hi for s in (-1, 0, 1))
               for (a, b), (lo, hi) in zip((grid_arc(box[0], j) for j in box[1:]), sides))


def interiors_meet(box, sides):
    """Exact test: the interior of the grid box meets the interior of the box `sides` modulo 2."""
    return all(any(a + 2 * s < hi and lo < b + 2 * s for s in (-2, -1, 0, 1, 2))
               for (a, b), (lo, hi) in zip((grid_arc(box[0], j) for j in box[1:]), sides))


def point_inside(taus, sides):
    """Exact test: the point `taus` lies in the box `sides` modulo 2."""
    return all(any(lo <= t + 2 * s <= hi for s in (-1, 0, 1)) for t, (lo, hi) in zip(taus, sides))


# ------------------------------------------------------------------ bounds of H and G on boxes
def dense(form):
    """The coefficients of a form in four variables as a 3 x 3 x 3 x 3 table (zero where absent)."""
    return [[[[form.get((a, b, c, d), arb(0)) for d in range(3)] for c in range(3)] for b in range(3)]
            for a in range(3)]


def H_upper(T, hulls):
    """An exact number >= sup H over the box of T^4 whose sides are the arcs with hulls
    `hulls[0..3]`; T = dense(form).

    Proof.  As kernel.ma_range: H^ is affine in each (x_m, y_m), the arcs lie in the triangles,
    and the maximum over the product of the triangles is attained at a 4-tuple of vertices.
    The nested loops contract the table with one vertex at a time."""
    best = None
    for (_, x0, y0) in hulls[0]:
        T1 = [[[T[0][b][c][d] + T[1][b][c][d] * x0 + T[2][b][c][d] * y0 for d in range(3)]
               for c in range(3)] for b in range(3)]
        for (_, x1, y1) in hulls[1]:
            T2 = [[T1[0][c][d] + T1[1][c][d] * x1 + T1[2][c][d] * y1 for d in range(3)] for c in range(3)]
            for (_, x2, y2) in hulls[2]:
                T3 = [T2[0][d] + T2[1][d] * x2 + T2[2][d] * y2 for d in range(3)]
                for (_, x3, y3) in hulls[3]:
                    u = (T3[0] + T3[1] * x3 + T3[2] * y3).upper()
                    if best is None or best < u:
                        best = u
    return best


def reduce_ends(form):
    """The forms A, V1, V2, W1, W2 in (theta_1, theta_2) of the decomposition (R) of a form in four
    variables; raises ValueError if a monomial contains both theta_0 and theta_3."""
    red = {name: {} for name in ("A", "V1", "V2", "W1", "W2")}
    for (a, b, c, d), coef in form.items():
        if a and d:
            raise ValueError("a monomial contains both end torsions: the reduction (R) does not apply")
        name = "A" if not (a or d) else ("V%d" % a if a else "W%d" % d)
        red[name][(0, b, c, 0)] = coef
    return red


def tables(red):
    """The five reduced forms as 3 x 3 tables t[b][c] of coefficients (zero where absent)."""
    return [[[red[name].get((0, b, c, 0), arb(0)) for c in range(3)] for b in range(3)]
            for name in ("A", "V1", "V2", "W1", "W2")]


def G_upper(tabs, hull1, hull2):
    """An exact number >= sup G over the box whose sides are the arcs with hulls hull1, hull2.

    Proof.  G^(P1, P2) = A^ + |V^| + |W^| with A^, V^, W^ bi-affine in (P1, P2); a norm of an
    affine map is convex, so G^ is convex in P1 for fixed P2 and in P2 for fixed P1; the arcs lie
    in the triangles; a separately convex function on a product of polytopes is maximal at a pair
    of vertices.  The square root is taken of an upper bound of V1^2 + V2^2 (>= 0)."""
    best = None
    for (_, x1, y1) in hull1:
        rows = [[t[0][c] + t[1][c] * x1 + t[2][c] * y1 for c in range(3)] for t in tabs]
        for (_, x2, y2) in hull2:
            a, v1, v2, w1, w2 = [r[0] + r[1] * x2 + r[2] * y2 for r in rows]
            val = a + (v1 * v1 + v2 * v2).upper().sqrt() + (w1 * w1 + w2 * w2).upper().sqrt()
            u = val.upper()
            if best is None or best < u:
                best = u
    return best


# ------------------------------------------------------------------ (L) local step
def concavity_certificate(form, box, centre, kr_radius=2.0 ** -80):
    """Step (L) for the box B = `box` (four tau-intervals with rational end points, each of width
    at most 1/2) and the approximate critical point pi * centre (four exact dyadic rationals).
    Returns a dict d; (L0) holds iff d["ok"].  Then d["K"] encloses the unique critical point
    theta^/pi of H in B (balls), d["H"] contains H(theta^), and d["hessian_eig_enclosure"] are
    intervals containing the spectrum of the Hessian of H at every point of B."""
    d = {"ok": False, "box": box}
    if any(hi - lo > Fr(1, 2) for lo, hi in box):
        d["failed"] = "the box is wider than a quarter turn"
        return d
    hulls = [arc_hull(lo, hi) for lo, hi in box]
    grad = [derivative(form, k) for k in range(4)]
    hess = [[derivative(grad[k], l) for l in range(4)] for k in range(4)]
    M = [[None] * 4 for _ in range(4)]
    for k in range(4):
        for l in range(k, 4):
            lo, hi = ma_range(hess[k][l], hulls)
            M[k][l] = M[l][k] = lo.union(hi)        # a ball containing [lo, hi]
    import numpy as np                      # approximate eigenvectors only (any Q is admissible)
    Q = np.linalg.eigh(np.array([[float(M[k][l].mid()) for l in range(4)] for k in range(4)]))[1]
    try:
        eig = sym_eig_enclosure(M, Q)
    except ZeroDivisionError:
        d["failed"] = "eigenvector matrix not certified invertible"
        return d
    d["hessian_eig_enclosure"] = eig
    if not all(hi < 0 for _, hi in eig):
        d["failed"] = "Hessian not certified negative definite on B"
        return d

    # a critical point in a tiny box around the centre: Krawczyk in tau coordinates for
    # f(tau) = grad_theta H(pi tau), whose Jacobian is pi * Hess_theta H(pi tau)
    def f(taus):
        P = [point(t) for t in taus]
        return [ma_eval(g, P) for g in grad]

    def jac(taus):
        P = [point(t) for t in taus]
        return [[ma_eval(hess[k][l], P) * arb.pi() for l in range(4)] for k in range(4)]

    ok, K = krawczyk(f, jac, [ball(c) for c in centre], kr_radius)
    if not ok:
        d["failed"] = "Krawczyk test failed"
        return d
    if not all(ball(lo) <= K[k].lower() and K[k].upper() <= ball(hi) for k, (lo, hi) in enumerate(box)):
        d["failed"] = "the Krawczyk box is not inside B"
        return d
    d["K"] = K
    d["H"] = ma_eval(form, [point(t) for t in K])
    d["ok"] = True
    return d


def direction_halfwidth(F1, F2, tau0, hulls):
    """A rational rho such that on the box with hulls `hulls` the vector (F1, F2) does not vanish
    and its polar angle is within pi * rho of pi * tau0 (mod 2 pi); None if not certified.

    Proof.  (F1, F2) = par u + perp u', u = (cos, sin)(pi tau0), u' = (-sin, cos)(pi tau0); par and
    perp are forms; if par >= lo > 0 and |perp| <= m on the box, the polar angle relative to u is
    atan(perp / par), of absolute value at most atan(m / lo)."""
    _, c0, s0 = point(tau0)
    par = f_add(f_scale(F1, c0), f_scale(F2, s0))
    perp = f_add(f_scale(F2, c0), f_scale(F1, -s0))
    lo_par, _ = ma_range(par, hulls)
    lo_perp, hi_perp = ma_range(perp, hulls)
    if not lo_par > 0:
        return None
    m = abs(lo_perp)
    if m < abs(hi_perp):
        m = abs(hi_perp)
    rho = to_fraction(((m / lo_par).upper().atan() / arb.pi()).upper())
    return Fr(math.ceil(rho * 2 ** 64), 2 ** 64)


def local_certificate(form, sides, centre, kr_radius=2.0 ** -80):
    """Step (R-L) for the box B' = `sides` of the (tau_1, tau_2)-plane and the approximate
    critical point pi * centre.  Returns the dict of `concavity_certificate` for
    B = B_0 x B' x B_3 (plus d["direction_halfwidths"]); (L1) holds iff d["ok"]."""
    d = {"ok": False}
    red = reduce_ends(form)
    if any(hi - lo > Fr(1, 2) for lo, hi in sides):
        d["failed"] = "B' is wider than a quarter turn"
        return d
    hulls2 = [[None], arc_hull(*sides[0]), arc_hull(*sides[1]), [None]]
    rho0 = direction_halfwidth(red["V1"], red["V2"], centre[0], hulls2)
    rho3 = direction_halfwidth(red["W1"], red["W2"], centre[3], hulls2)
    d["direction_halfwidths"] = (rho0, rho3)
    if rho0 is None or rho3 is None or rho0 > Fr(1, 4) or rho3 > Fr(1, 4):
        d["failed"] = "V or W not certified to stay in a quarter-turn sector over B'"
        return d
    box = [(centre[0] - rho0, centre[0] + rho0), sides[0], sides[1], (centre[3] - rho3, centre[3] + rho3)]
    d.update(concavity_certificate(form, box, centre, kr_radius))
    return d


def _local_step(local, boxes, centre, select):
    """Group the unresolved boxes and attempt the local step around +centre and -centre.

    local(sides, c) -> certificate dict for the box `sides` of the grid space and the approximate
    critical point c; select(c) -> the coordinates of c in the grid space.
    Returns (groups, ok): ok iff there are exactly two groups, every box lies in the box of its
    group (re-checked with `inside`), the two local certificates hold, one around +centre
    (critical point theta^_+ in B_+) and one around -centre (theta^_- in B_-), and -theta^_+ lies
    in B_-.  In that case theta^_- = -theta^_+ (H is even, so -theta^_+ is a critical point, and
    B_- contains only one) and H(theta^_-) = H(theta^_+)."""
    groups = []
    for sides, members in clusters(boxes):
        g = {"sides": sides, "members": members, "sign": None, "local": None}
        for sign in (1, -1):
            c = [sign * x for x in centre]
            if point_inside(select(c), sides):
                g["sign"] = sign
                g["local"] = local(sides, c)
        groups.append(g)
    covered = all(any(inside(b, g["sides"]) for g in groups) for b in boxes)
    good = sorted(g["sign"] for g in groups if g["local"] is not None and g["local"]["ok"])
    if not (covered and len(groups) == 2 and good == [-1, 1]):
        return groups, False
    plus = next(g["local"] for g in groups if g["sign"] == 1)
    minus = next(g["local"] for g in groups if g["sign"] == -1)
    mirror = all(ball(lo) <= (-K).lower() and (-K).upper() <= ball(hi) for K, (lo, hi) in zip(plus["K"], minus["box"]))
    return groups, mirror


# ------------------------------------------------------------------ the certificates
def _certify(form, centre, levels, root_level, dim, upper, local, select, log):
    assert not odd_sine_monomials(form), "H is not even"                # H(-theta) = H(theta)
    lower = ma_eval(form, [point(c) for c in centre]).lower()            # L <= H(pi centre) <= max H
    r = {"certified": False, "lower_bound": lower, "stats": {}, "excluded": [], "attempts": []}
    boxes = root_boxes(root_level, dim)
    for level in levels:
        boxes = branch_and_bound(upper, lower, boxes, level, r["stats"], r["excluded"])
        groups, ok = _local_step(local, boxes, centre, select)
        r["attempts"].append({"level": level, "unresolved": len(boxes), "groups": groups})
        r["unresolved"] = boxes
        log(f"level {level}: {len(boxes)} unresolved boxes in {len(groups)} groups; local step {'ok' if ok else 'not ok'}")
        if ok:
            plus = next(g for g in groups if g["sign"] == 1)
            # theta^ != -theta^ mod 2 pi: two distinct maximisers (reported; not needed for (C))
            r["distinct"] = any(not K.contains_integer() for K in plus["local"]["K"])
            r["certified"] = True
            r["groups"] = groups
            return r
    return r


def certify(form, centre, levels, root_level=3, kr_radius=2.0 ** -80, log=None):
    """Certificate R: the global maximisers of the form H (four variables) on the torus are
    exactly +-theta^, where theta^ is the critical point enclosed near pi * centre.

    centre: four exact dyadic rationals (an approximate maximiser, tau units); levels: increasing
    grid levels (>= root_level) at which the local step is attempted.  Returns a dict r; the
    statement is certified iff r["certified"].  r["excluded"] and r["unresolved"] together tile
    [-1, 1]^2 (tau units, the (theta_1, theta_2)-plane)."""
    tabs, grid = tables(reduce_ends(form)), Grid()                       # (R); raises if not applicable
    return _certify(form, centre, levels, root_level, 2,
                    lambda b: G_upper(tabs, grid.hull(b[0], b[1]), grid.hull(b[0], b[2])),
                    lambda sides, c: local_certificate(form, sides, c, kr_radius),
                    lambda c: c[1:3], log or (lambda *a: None))


def certify_direct(form, centre, levels, root_level=3, kr_radius=2.0 ** -80, log=None):
    """Certificate D: the same statement as `certify`, by branch and bound on the 4-torus, without
    the reduction (R).  r["excluded"] and r["unresolved"] together tile [-1, 1]^4."""
    T, grid = dense(form), Grid()
    return _certify(form, centre, levels, root_level, 4,
                    lambda b: H_upper(T, [grid.hull(b[0], j) for j in b[1:]]),
                    lambda sides, c: concavity_certificate(form, list(sides), c, kr_radius),
                    lambda c: c, log or (lambda *a: None))


def certify_outside(form, centre, other, hill_level, levels, root_level=3, kr_radius=2.0 ** -80, log=None):
    """The supremum of H away from the main maximisers ("second maximum"), in the reduced setting.

    centre: approximate main maximiser; other: approximate critical point with a smaller value
    (both: exact dyadic rationals, tau units).  With L2 <= H(pi other): the boxes of the level
    `hill_level` of the (theta_1, theta_2)-plane on which sup G < L2 is not certified are
    grouped; N := the union of the groups that contain +-(centre_1, centre_2) (r["hill"]); the
    other boxes are refined at `levels` until the local step holds for them around +-other.
    If r["certified"]:

        H(theta) <= H(theta2^) for every theta in T^4 with (theta_1, theta_2) not in the interior
        of N, with equality exactly at +-theta2^,

    theta2^ being the unique critical point of H in the box B of the local certificate
    [off N and the two boxes B'_2 the bound G < L2 <= H(theta2^) holds; on the cylinders over the
    boxes B'_2, (L1); and +-theta2^ are not interior to N]."""
    log = log or (lambda *a: None)
    assert not odd_sine_monomials(form), "H is not even"
    tabs, grid = tables(reduce_ends(form)), Grid()

    def upper(b):
        return G_upper(tabs, grid.hull(b[0], b[1]), grid.hull(b[0], b[2]))

    lower = ma_eval(form, [point(c) for c in other]).lower()             # L2 <= H(pi other)
    r = {"certified": False, "lower_bound": lower, "stats": {}, "excluded": [], "attempts": []}
    boxes = branch_and_bound(upper, lower, root_boxes(root_level, 2), hill_level, r["stats"], r["excluded"])
    mains = [[s * x for x in centre[1:3]] for s in (1, -1)]
    hill = [b for sides, members in clusters(boxes) if any(point_inside(m, sides) for m in mains) for b in members]
    r["hill"] = hill
    in_hill = set(hill)
    boxes = [b for b in boxes if b not in in_hill]
    log(f"level {hill_level}: {len(hill)} boxes in the hill region N, {len(boxes)} other unresolved boxes")
    for level in levels:
        boxes = branch_and_bound(upper, lower, boxes, level, r["stats"], r["excluded"])
        groups, ok = _local_step(lambda sides, c: local_certificate(form, sides, c, kr_radius), boxes, other,
                                 lambda c: c[1:3])
        r["attempts"].append({"level": level, "unresolved": len(boxes), "groups": groups})
        r["unresolved"] = boxes
        log(f"level {level}: {len(boxes)} unresolved boxes in {len(groups)} groups; local step {'ok' if ok else 'not ok'}")
        if ok:
            # the boxes B'_2 do not meet the interior of N, so +-theta2^ are not interior to N
            if not any(interiors_meet(b, g["sides"]) for b in hill for g in groups):
                r["certified"] = True
                r["groups"] = groups
            return r
    return r
