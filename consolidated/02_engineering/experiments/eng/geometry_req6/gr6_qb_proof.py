"""(Q-b) of GEOMETRY-REQ-0006: a configuration of n points in R^4, of affine dimension 4, with
prescribed squared lengths on the pairs of a graph.

TRUSTED.  The statement certified by `certify_realisation`:

    for every choice of real targets t_e in the balls `targets[e]` there is a configuration
    y_0..y_{n-1} in R^4 with |y_i - y_j|^2 = t_e for every pair e = (i, j) of `edges`, in the gauge
    below, with the pinned coordinates at their rational values and the other unknown coordinates
    in the balls d["K"]; the singular values of its centred configuration matrix lie in the
    intervals d["sigma"] and are all >= d["sigma_min_lower"] > 0 (affine dimension 4).

Gauge (it removes the Euclidean motions of R^4; we only need existence, so no claim that every
solution can be brought to it):  y_0 = 0,  y_1 = (*, 0, 0, 0),  y_2 = (*, *, 0, 0),
y_3 = (*, *, *, 0), all other coordinates free: 4n - 10 unknowns.  With |edges| equations,
4n - 10 - |edges| unknowns are pinned at rational values; the square system is certified by the
Krawczyk test (kernel.krawczyk) with the targets as interval parameters: the residual at the
centre is evaluated with the balls t_e, so the computed operator contains the Krawczyk operator
of every system with targets in the balls, and its inclusion in the interior of the box proves
existence (and uniqueness in the box) for each of them.
"""
from __future__ import annotations

from flint import arb

from gr6_kernel import ball, krawczyk, pairwise_disjoint, sym_eig_enclosure

DIM = 4


def gauge_unknowns(n):
    """The coordinates (atom, axis) that are not fixed to zero by the gauge."""
    return [(i, a) for i in range(1, n) for a in range(DIM) if i >= 4 or a < i]


def configuration(n, values):
    """n x 4 table of balls: `values[(atom, axis)]` where given, exact zero elsewhere."""
    return [[values.get((i, a), arb(0)) for a in range(DIM)] for i in range(n)]


def sq_length(Y, i, j):
    s = arb(0)
    for a in range(DIM):
        d = Y[i][a] - Y[j][a]
        s += d * d
    return s


def length_system(n, edges, targets, pins):
    """(free, f, jac, config) of the gauged system: `free` the unknown coordinates in order,
    f(z)_e = |y_i - y_j|^2 - t_e, jac(z) its Jacobian, config(z) the n x 4 configuration, for z a
    list of balls (one per free unknown).  pins: {(atom, axis): Fraction}."""
    unknowns = gauge_unknowns(n)
    assert all(u in unknowns for u in pins)
    free = [u for u in unknowns if u not in pins]
    fixed = {u: ball(v) for u, v in pins.items()}
    col = {u: k for k, u in enumerate(free)}

    def config(z):
        vals = dict(fixed)
        vals.update(zip(free, z))
        return configuration(n, vals)

    def f(z):
        Y = config(z)
        return [sq_length(Y, i, j) - t for (i, j), t in zip(edges, targets)]

    def jac(z):
        Y = config(z)
        J = [[arb(0)] * len(free) for _ in edges]
        for e, (i, j) in enumerate(edges):
            for a in range(DIM):
                g = 2 * (Y[i][a] - Y[j][a])
                if (i, a) in col:
                    J[e][col[(i, a)]] = J[e][col[(i, a)]] + g
                if (j, a) in col:
                    J[e][col[(j, a)]] = J[e][col[(j, a)]] - g
        return J

    return free, f, jac, config


def singular_values(Y):
    """Enclosure of the singular values of the centred configuration matrix of Y (n x 4 balls):
    (intervals, disjoint, smallest), where every singular value of every configuration in Y lies
    in the union of the intervals (exactly one in each if `disjoint`) and is >= smallest (an
    exact number, possibly <= 0 when nothing is certified).  Raises ZeroDivisionError if the
    approximate eigenvector matrix is not certified invertible.

    Proof.  The squared singular values are the eigenvalues of the 4 x 4 Gram matrix of the centred
    configuration, enclosed by kernel.sym_eig_enclosure."""
    n = len(Y)
    mean = [sum((Y[i][a] for i in range(n)), arb(0)) / n for a in range(DIM)]
    Yc = [[Y[i][a] - mean[a] for a in range(DIM)] for i in range(n)]
    gram = [[sum((Yc[i][a] * Yc[i][b] for i in range(n)), arb(0)) for b in range(DIM)] for a in range(DIM)]
    import numpy as np                      # approximate eigenvectors only (any Q is admissible)
    Q = np.linalg.eigh(np.array([[float(gram[a][b].mid()) for b in range(DIM)] for a in range(DIM)]))[1]
    eig = sym_eig_enclosure(gram, Q)
    smallest = eig[0][0]
    for lo, _ in eig[1:]:
        if lo < smallest:                   # exact comparison of exact numbers
            smallest = lo
    if not smallest > 0:
        return None, False, smallest
    intervals = [(lo.sqrt().lower(), hi.sqrt().upper()) for lo, hi in eig]
    return intervals, pairwise_disjoint(eig), smallest.sqrt().lower()


def certify_realisation(n, edges, targets, pins, centre, radius=2.0 ** -70):
    """See the module docstring.  centre: {(atom, axis): exact ball} for the unknowns of the gauge
    that are not pinned.  Returns a dict d; the statement is certified iff d["ok"]."""
    d = {"ok": False}
    free, f, jac, config = length_system(n, edges, targets, pins)
    assert sorted(centre) == sorted(free)
    if len(free) != len(edges):
        d["failed"] = "the system is not square"
        return d
    ok, K = krawczyk(f, jac, [centre[u] for u in free], radius)
    if not ok:
        d["failed"] = "Krawczyk test failed (no certified zero in the box)"
        return d
    d["K"] = dict(zip(free, K))
    d["Y"] = config(K)
    try:
        d["sigma"], d["sigma_disjoint"], d["sigma_min_lower"] = singular_values(d["Y"])
    except ZeroDivisionError:
        d["failed"] = "eigenvector matrix not certified invertible"
        return d
    if d["sigma"] is None:
        d["failed"] = "smallest singular value not certified positive"
        return d
    d["ok"] = True
    return d
