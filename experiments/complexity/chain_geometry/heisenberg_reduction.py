"""Checks for docs/complexity/CHAIN_GEOMETRY_HARDNESS.md.

(1) [X] The gadget inequality  h(t) = sqrt(25+24t) + sqrt(25-24t) <= 10 - t^2  on [-1,1], with equality only at 0:
    verified exactly as the polynomial inequality  76 t^2 + 125 t^4 - 10 t^6 + t^8/4 >= 0  (and the squaring steps)
    on a rational grid, in addition to the two-line proof in the note.
(2) [N] The reduction from MAX-CUT to the Heisenberg ground-state problem in R^3: for small graphs the value
        max F = 10*Lam*(2n+1) + 2*maxcut - |E|,   Lam = 4|E|,
    is compared with a numerical maximisation of F over unit vectors (many random starts; the formula value is
    always attained by the explicit configuration, and no start exceeds it).
(3) [X-numerical identity] sum_{i<j} c_ij |x_i - x_j|^2 = sum_{k,l} Q_kl <b_k, b_l> for the map c <-> Q of the note,
    on random chains (floating point, tolerance 1e-9), and the inverse map.
(4) Fixed bond angle: for random target unit vectors t_1..t_N and several bond-vector angles theta', intermediate
    bonds are constructed so that b_{1+(i-1)m} = t_i and all consecutive angles equal theta' (m as in the note).
(5) End to end on a small graph: the chain instance (integer data c) of the reduction, evaluated on the explicit
    optimal fixed-angle chain, gives the threshold value.

Usage: python3 heisenberg_reduction.py
"""
import itertools
import math
import random
from fractions import Fraction

import numpy as np
from scipy.optimize import minimize


# ------------------------------------------------------------------------------------------------ (1)
def check_gadget_inequality():
    ok = True
    for num in range(-2000, 2001):
        t = Fraction(num, 2000)
        t2 = t * t
        poly = 76 * t2 + 125 * t2 ** 2 - 10 * t2 ** 3 + t2 ** 4 / 4
        ok &= poly >= 0 and (poly == 0) == (t == 0)
        # the two squaring steps are legitimate: both sides non-negative
        ok &= 25 - 10 * t2 + t2 ** 2 / 2 >= 0 and 625 - 576 * t2 >= 0 and 10 - t2 >= 0
        # numerical cross-check of the original inequality
        h = math.sqrt(25 + 24 * float(t)) + math.sqrt(25 - 24 * float(t))
        ok &= h <= 10 - float(t2) + 1e-12
    return ok


# ------------------------------------------------------------------------------------------------ (2)
def maxcut(n, edges):
    best = 0
    for s in itertools.product((1, -1), repeat=n - 1):
        s = (1,) + s
        best = max(best, sum(1 for (v, w) in edges if s[v] != s[w]))
    return best


def reduction_matrix(n, edges):
    """spins: u_0..u_{n-1}, z1, z2, then two gadget spins per orthogonality gadget.  Returns Q (symmetric, zero
    diagonal, integer) and the index layout."""
    lam = 4 * len(edges)
    pairs = [(v, n) for v in range(n)] + [(v, n + 1) for v in range(n)] + [(n, n + 1)]     # orthogonality gadgets
    N = n + 2 + 2 * len(pairs)
    Q = np.zeros((N, N))
    for (v, w) in edges:
        Q[v, w] = Q[w, v] = -1
    for g, (p, q) in enumerate(pairs):
        a, a2 = n + 2 + 2 * g, n + 3 + 2 * g
        for (x, y, val) in ((a, p, 3 * lam), (a, q, 4 * lam), (a2, p, 3 * lam), (a2, q, -4 * lam)):
            Q[x, y] = Q[y, x] = val
    return Q, lam, pairs


def F(Q, B):
    G = B @ B.T
    return float(np.sum(np.triu(Q, 1) * G))


def explicit_optimum(n, edges, Q, lam, pairs):
    """z1 = e1, z2 = e2, u_v = +-e3 for a maximum cut, gadget spins aligned with 3p +- 4q."""
    best, bs = -1, None
    for s in itertools.product((1, -1), repeat=n - 1):
        s = (1,) + s
        c = sum(1 for (v, w) in edges if s[v] != s[w])
        if c > best:
            best, bs = c, s
    N = Q.shape[0]
    B = np.zeros((N, 3))
    for v in range(n):
        B[v] = [0, 0, bs[v]]
    B[n] = [1, 0, 0]
    B[n + 1] = [0, 1, 0]
    for g, (p, q) in enumerate(pairs):
        a, a2 = n + 2 + 2 * g, n + 3 + 2 * g
        x = 3 * B[p] + 4 * B[q]
        y = 3 * B[p] - 4 * B[q]
        B[a], B[a2] = x / np.linalg.norm(x), y / np.linalg.norm(y)
    return B


def numerical_max(Q, starts, rng):
    N = Q.shape[0]
    U = np.triu(Q, 1)
    S = U + U.T

    def neg(x):
        B = x.reshape(N, 3)
        nrm = np.linalg.norm(B, axis=1, keepdims=True)
        Bn = B / nrm
        G = Bn @ Bn.T
        val = np.sum(U * G)
        grad_Bn = S @ Bn
        grad = (grad_Bn - np.sum(grad_Bn * Bn, axis=1, keepdims=True) * Bn) / nrm
        return -val, -grad.ravel()

    best = -1e18
    for _ in range(starts):
        x0 = rng.normal(size=3 * N)
        res = minimize(neg, x0, jac=True, method="L-BFGS-B", options={"maxiter": 4000, "ftol": 1e-15, "gtol": 1e-10})
        best = max(best, -res.fun)
    return best


def check_reduction(rng):
    graphs = {
        "triangle": (3, [(0, 1), (1, 2), (0, 2)]),
        "path P3": (3, [(0, 1), (1, 2)]),
        "C4": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        "K4": (4, list(itertools.combinations(range(4), 2))),
        "C5": (5, [(i, (i + 1) % 5) for i in range(5)]),
        "K4 minus an edge": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]),
    }
    ok = True
    for name, (n, edges) in graphs.items():
        Q, lam, pairs = reduction_matrix(n, edges)
        mc = maxcut(n, edges)
        formula = 10 * lam * (2 * n + 1) + 2 * mc - len(edges)
        attained = F(Q, explicit_optimum(n, edges, Q, lam, pairs))
        found = numerical_max(Q, 60, rng)
        good = abs(attained - formula) < 1e-9 and found <= formula + 1e-6
        ok &= good
        print(f"    {name}: {Q.shape[0]} spins, Lam = {lam}, maxcut = {mc}; formula {formula}; explicit configuration "
              f"{attained:.9f}; best of 60 numerical maximisations {found:.6f} (never above the formula: "
              f"{found <= formula + 1e-6}; reaches it: {abs(found - formula) < 1e-4})")
    return ok


# ------------------------------------------------------------------------------------------------ (3)
def q_from_c(c):
    """Q_kl = sum_{i <= min(k,l)} sum_{j > max(k,l)} c_ij  for bonds k, l = 1..n-1 (atoms 1..n)."""
    n = c.shape[0]
    Q = np.zeros((n - 1, n - 1))
    for k in range(1, n):
        for l in range(1, n):
            lo, hi = min(k, l), max(k, l)
            Q[k - 1, l - 1] = sum(c[i - 1, j - 1] for i in range(1, lo + 1) for j in range(hi + 1, n + 1))
    return Q


def c_from_q(Q):
    """inverse: c_ij = Q_{i,j-1} - Q_{i-1,j-1} - Q_{i,j} + Q_{i-1,j}  (Q with index 0 or n is 0), i < j."""
    m = Q.shape[0]
    n = m + 1
    Qe = np.zeros((n + 1, n + 1))
    Qe[1:n, 1:n] = Q
    c = np.zeros((n, n))
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            c[i - 1, j - 1] = c[j - 1, i - 1] = Qe[i, j - 1] - Qe[i - 1, j - 1] - Qe[i, j] + Qe[i - 1, j]
    return c


def check_bijection(rng):
    ok = True
    for _ in range(30):
        n = rng.integers(3, 9)
        c = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                c[i, j] = c[j, i] = rng.integers(-5, 6)
        Q = q_from_c(c)
        ok &= np.allclose(c_from_q(Q), c)
        b = rng.normal(size=(n - 1, 3))
        b /= np.linalg.norm(b, axis=1, keepdims=True)
        x = np.vstack([np.zeros(3), np.cumsum(b, axis=0)])
        lhs = sum(c[i, j] * np.sum((x[i] - x[j]) ** 2) for i in range(n) for j in range(i + 1, n))
        rhs = np.sum(Q * (b @ b.T))
        ok &= abs(lhs - rhs) < 1e-9
    return ok


# ------------------------------------------------------------------------------------------------ (4)
def steps_needed(theta):
    psi = min(theta, math.pi - theta)
    return max(2, math.ceil(math.pi / psi - 1e-12))


def rot(axis, ang):
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * (K @ K)


def any_perp(p):
    a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
    v = np.cross(p, a)
    return v / np.linalg.norm(v)


def _dist(a, b):
    return math.acos(max(-1.0, min(1.0, float(np.dot(a, b)))))


def _towards(c, q, ang):
    """the point at spherical distance ang from c on the great circle through c and q, on the side of q"""
    d = _dist(c, q)
    if d < 1e-12 or abs(d - math.pi) < 1e-12:
        e = any_perp(c)
    else:
        e = q - math.cos(d) * c
        e /= np.linalg.norm(e)
    return math.cos(ang) * c + math.sin(ang) * e


def _link_small(p, q, psi, m):
    """w_0 = p, ..., w_m = q with consecutive spherical distances psi <= pi/2, for m >= max(2, ceil(pi/psi)).
    Walk towards q while more than two steps remain and either their number is odd or q is farther than 2 psi;
    spend pairs of steps going to a neighbour and back; finish with an isosceles elbow (construction of the note)."""
    w, c, r = [p], p, m
    while r > 2:
        d = _dist(c, q)
        if r % 2 == 1 or d > 2 * psi + 1e-12:
            c = _towards(c, q, psi)
            c /= np.linalg.norm(c)
            w.append(c)
            r -= 1
        else:
            nb = math.cos(psi) * c + math.sin(psi) * any_perp(c)
            w += [nb / np.linalg.norm(nb), c]
            r -= 2
    d = _dist(c, q)
    assert d <= 2 * psi + 1e-9
    if d < 1e-12:
        mid, nrm = c, any_perp(c)
    elif abs(d - math.pi) < 1e-9:
        mid, nrm = any_perp(c), None           # psi = pi/2: any point perpendicular to c (and to q = -c)
    else:
        mid = (c + q) / np.linalg.norm(c + q)
        nrm = np.cross(c, q)
        nrm /= np.linalg.norm(nrm)
    if nrm is None:
        elbow = mid
    else:
        cosphi = max(-1.0, min(1.0, math.cos(psi) / math.cos(d / 2)))
        phi = math.acos(cosphi)
        elbow = math.cos(phi) * mid + math.sin(phi) * nrm
    w += [elbow / np.linalg.norm(elbow), q]
    return w


def link(p, q, theta, m, rng=None):
    """unit vectors w_0 = p, ..., w_m = q with all consecutive angles equal to theta in (0, pi)."""
    if theta <= math.pi / 2:
        return _link_small(p, q, theta, m)
    psi = math.pi - theta
    w = _link_small(p, q if m % 2 == 0 else -q, psi, m)
    return [x if i % 2 == 0 else -x for i, x in enumerate(w)]


def check_fixed_angle(rng):
    ok = True
    for deg in (70.528779, 60.0, 90.0, 109.471221, 35.0, 150.0):
        theta = math.radians(deg)
        m = steps_needed(theta)
        worst = 0.0
        for _ in range(40):
            N = 4
            t = rng.normal(size=(N, 3))
            t /= np.linalg.norm(t, axis=1, keepdims=True)
            bonds = [t[0]]
            for i in range(1, N):
                bonds += link(t[i - 1], t[i], theta, m, rng)[1:]
            bonds = np.array(bonds)
            angs = [math.acos(max(-1, min(1, float(np.dot(bonds[k], bonds[k + 1]))))) for k in range(len(bonds) - 1)]
            worst = max(worst, max(abs(a - theta) for a in angs))
            ok &= np.allclose(bonds[::m], t)
        ok &= worst < 1e-7
        print(f"    angle between consecutive bond vectors {deg:.3f} deg: m = {m}; largest deviation of a constructed "
              f"angle: {worst:.1e}")
    return ok


# ------------------------------------------------------------------------------------------------ (5)
def check_end_to_end(rng):
    n, edges = 3, [(0, 1), (1, 2), (0, 2)]
    Q, lam, pairs = reduction_matrix(n, edges)
    B = explicit_optimum(n, edges, Q, lam, pairs)
    formula = 10 * lam * (2 * n + 1) + 2 * maxcut(n, edges) - len(edges)
    theta = math.radians(70.528779)
    m = steps_needed(theta)
    N = Q.shape[0]
    # designated bonds 1, 1+m, ...; couplings on them only
    nb = (N - 1) * m + 1
    Qbig = np.zeros((nb, nb))
    idx = [i * m for i in range(N)]
    for a in range(N):
        for b in range(N):
            Qbig[idx[a], idx[b]] = Q[a, b] / 2          # sum over ordered pairs k,l of Qbig <b_k,b_l> = sum_{a<b} Q_ab <.,.>
    c = c_from_q(Qbig)
    integer = np.allclose(2 * c, np.round(2 * c))
    bonds = [B[0]]
    for i in range(1, N):
        bonds += link(B[i - 1], B[i], theta, m, rng)[1:]
    bonds = np.array(bonds)
    x = np.vstack([np.zeros(3), np.cumsum(bonds, axis=0)])
    natoms = x.shape[0]
    val = sum(c[i, j] * np.sum((x[i] - x[j]) ** 2) for i in range(natoms) for j in range(i + 1, natoms))
    print(f"    triangle graph -> {N} spins -> fixed-angle chain with {natoms} atoms (m = {m}); data 2c integral: {integer};"
          f" objective on the explicit chain {val:.6f}, threshold {formula}")
    return integer and abs(val - formula) < 1e-6


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    r1 = check_gadget_inequality()
    print("(1) gadget inequality h(t) <= 10 - t^2 on [-1,1], equality only at t = 0:", r1)
    print("(2) reduction MAX-CUT -> Heisenberg ground state in R^3:")
    r2 = check_reduction(rng)
    r3 = check_bijection(rng)
    print("(3) identity sum c_ij |x_i - x_j|^2 = sum Q_kl <b_k, b_l> and the inverse map on 30 random chains:", r3)
    print("(4) fixed bond angle: every m-th bond is free")
    r4 = check_fixed_angle(rng)
    print("(5) end to end:")
    r5 = check_end_to_end(rng)
    print("ALL OK" if all((r1, r2, r3, r4, r5)) else "FAILURE")
