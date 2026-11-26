#!/usr/bin/env python3
"""AA1 audit, script 6: four small facts used in the audit report.

(a) Theorem 11.29 (normal form): the regularisation f -> f^d keeps every minimum but not ln Z.
(b) Theorem 2.5 / section 3.3: with one evaluated anchor the exact robust interval of ln Z on the
    uniform cube has the a-priori width beta * sum c_i  (exact, and useless).
(c) Theorem 11.36/11.37, role of "domains that contain extended arms": for a chain with fixed bond
    length b and bond angle theta (not 180 degrees) the moment of inertia of ANY arm of m atoms
    about ANY line is at least (m/3) * (w/2)^2, w = b cos(theta/2) the width of the triangle of
    three consecutive atoms (m a multiple of 3).  So the verified per-torsion constants of
    Theorem 4.6(d) grow at least like m^(1/2) on every torsion domain (compact ones included),
    and the hypothesis "c_i >= c0 m_i^gamma with gamma > 0" of Theorem 11.37 holds with
    gamma = 1/2 without any assumption on the domain.  Checked on random rotamer chains and on regular
    (all-trans, all-gauche, helical) ones, with the best line computed exactly (principal axis).

(d) Theorem 11.25(a) at finite sizes: the value of the machine-checked lower bound
    (1 - 2 delta) 2^n / |B(k*(eps))| at eps = 1, to see from which n it is large.

Run:  python3 experiments/audit/AA1/aa1_06_misc.py > experiments/audit/AA1/out_06_misc.txt
"""
import math

import numpy as np
from scipy.optimize import minimize

OK = True


def check(name, cond):
    global OK
    print(("PASS  " if cond else "FAIL  ") + name)
    OK = OK and bool(cond)


# ----------------------------------------------------------------------------- (a)
print("(a) normal form and free energies: X = {0,1}, d = 1 * [x != y], f = (0, 5), g = 0")
f = np.array([0.0, 5.0])
d = np.array([[0.0, 1.0], [1.0, 0.0]])
fd = np.array([min(f[x] + d[x, y] for x in range(2)) for y in range(2)])      # Pasch-Hausdorff envelope
print(f"    f^d = {fd.tolist()}")
adm = [np.array([0.0, t]) for t in np.linspace(-1, 1, 41)]                      # all admissible g up to constants
same_min = all(abs(min(f + g) - min(fd + g)) < 1e-12 for g in adm)
beta = 1.0
lz = [(math.log(np.exp(-beta * (f + g)).sum()), math.log(np.exp(-beta * (fd + g)).sum())) for g in adm]
maxdiff = max(abs(a - b) for a, b in lz)
print(f"    min(f+g) = min(f^d+g) for all admissible g: {same_min};  max |ln Z(f+g) - ln Z(f^d+g)| = {maxdiff:.4f}")
check("(a) minima agree for every admissible residual, free energies do not", same_min and maxdiff > 0.1)

# ----------------------------------------------------------------------------- (b)
print("(b) exact robust interval of ln Z with one anchor on the uniform cube (f = 0, d = c * Hamming, anchor 0...0, value 0)")
for n, u in ((10, 1.0), (100, 1.0), (100, 0.5)):
    width = n * math.log((1 + math.exp(u)) / (1 + math.exp(-u)))
    # brute force for n = 10
    if n == 10:
        pop = np.array([bin(i).count("1") for i in range(1 << n)])
        wb = math.log(np.exp(u * pop).sum()) - math.log(np.exp(-u * pop).sum())
        check(f"    n = 10: closed form {width:.6f} = brute force {wb:.6f} = n*u", abs(width - wb) < 1e-9 and abs(width - n * u) < 1e-9)
    print(f"    n = {n}, u = beta c = {u}: ln Z(f+L) - ln Z(f+U) = {width:.3f}  (a-priori width beta * sum c_i = {n*u:.3f})")

# ----------------------------------------------------------------------------- (c)
print("(c) inertia of an arm about an arbitrary line: lower bound (m/3) (w/2)^2 with w = b cos(theta/2)")
b = 1.0
theta = math.radians(111.0)
w = b * math.cos(theta / 2)
lb_per_atom = (1.0 / 3.0) * (w / 2) ** 2
print(f"    w = {w:.4f} b, bound per atom = {lb_per_atom:.5f} b^2   (constants: c_i^ver >= 2 Lambda sin(delta/2) sqrt({lb_per_atom:.5f} m) b = "
      f"{2*math.sqrt(lb_per_atom):.3f} Lambda b sin(delta/2) m^(1/2))")


def chain(torsions):
    """Atoms of a chain with bond length b, bond angle theta and the given torsions (NeRF)."""
    pts = [np.array([0.0, 0.0, 0.0]), np.array([b, 0.0, 0.0]),
           np.array([b - b * math.cos(theta), b * math.sin(theta), 0.0])]
    for phi in torsions:
        a, bb, c = pts[-3], pts[-2], pts[-1]
        bc = (c - bb) / np.linalg.norm(c - bb)
        nrm = np.cross(bb - a, bc)
        nrm /= np.linalg.norm(nrm)
        m_ = np.cross(nrm, bc)
        d2 = np.array([-b * math.cos(theta), b * math.sin(theta) * math.cos(phi), b * math.sin(theta) * math.sin(phi)])
        pts.append(c + d2[0] * bc + d2[1] * m_ + d2[2] * nrm)
    return np.array(pts)


def inertia_about_line(P, p0, dirv):
    dirv = dirv / np.linalg.norm(dirv)
    r = P - p0
    perp = r - np.outer(r @ dirv, dirv)
    return float((perp ** 2).sum())


def min_inertia_any_line(P):
    """Least moment of inertia about any line = smallest principal moment about the centroid."""
    Q = P - P.mean(axis=0)
    ev = np.linalg.eigvalsh(Q.T @ Q)             # ascending; inertia about principal axis k = sum of the other two
    return float(ev[0] + ev[1])


rng = np.random.default_rng(7)
worst = float("inf")
for m in (9, 30, 90, 300):
    for kind in ("random", "trans", "helix", "gauche"):
        for rep in range(40 if kind == "random" else 1):
            if kind == "random":
                tors = rng.choice([math.pi, math.pi / 3, -math.pi / 3], size=m - 3)
            elif kind == "trans":
                tors = np.full(m - 3, math.pi)
            elif kind == "helix":
                tors = np.full(m - 3, math.radians(50.0))
            else:
                tors = np.full(m - 3, math.pi / 3)
            P = chain(tors)
            ratio = min_inertia_any_line(P) / (m * b * b)
            worst = min(worst, ratio)
            # also the torsion axis proper: the line through the first two atoms
            ax = inertia_about_line(P, P[0], P[1] - P[0]) / (m * b * b)
            worst = min(worst, ax)
print(f"    least (inertia about the best line)/(m b^2) over all conformations tried: {worst:.5f}   (bound {lb_per_atom:.5f})")
check("(c) every arm tried has inertia >= (m/3)(w/2)^2 about every line, hence about its torsion axis", worst >= lb_per_atom - 1e-12)
# the two extremes for an all-trans arm: about its own long axis the inertia is linear in m (the bound is of
# the right order), about the first bond line (a torsion axis at its end) it grows like m^3 (the lever arm).
for m in (30, 300):
    P = chain(np.full(m - 3, math.pi))
    print(f"    all-trans arm, m = {m}: inertia about the best line = {min_inertia_any_line(P)/m:.4f} m b^2;  "
          f"about the first bond line = {inertia_about_line(P, P[0], P[1] - P[0]):.1f} b^2")

# ----------------------------------------------------------------------------- (d)
print("(d) Theorem 11.25(a) at finite size: the machine-checked lower bound (1 - 2 delta) 2^n / |B(k*(eps))| at the zero residual")
print("    (k*(eps) = least k with Delta_k > eps, Delta_k = ln(1 + 2^-n sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1)); exact integer binomials)")
from fractions import Fraction
from math import comb


def cube_lower_bound(n, u, eps):
    # log of sum_{j<=k} C(n,j)(e^{u(k+1-j)}-1) via floats on logs (n <= 2000 is fine with Python ints for the ball)
    ball = 0
    for k in range(0, n + 1):
        ball += comb(n, k)
        # Delta_k
        terms = [math.log(comb(n, j)) + math.log(math.expm1(u * (k + 1 - j))) for j in range(0, k + 1)]
        mx = max(terms)
        logsum = mx + math.log(sum(math.exp(t - mx) for t in terms))
        delta_k = math.log1p(math.exp(logsum - n * math.log(2))) if logsum - n * math.log(2) < 700 else logsum - n * math.log(2)
        if delta_k > eps:
            return k, n * math.log(2) - math.log(ball)
    return n, 0.0


print("      n      u    eps    k*    ln(2^n/|B(k*)|)    asymptotic n(ln2 - h(Lambda1/u))")
rows = []
for u in (0.5, 1.0, 2.0):
    lam1 = math.log(2 / (1 + math.exp(-u)))
    hh = lambda x: -x * math.log(x) - (1 - x) * math.log(1 - x)
    for n in (50, 100, 200, 500, 1000):
        k, lnb = cube_lower_bound(n, u, 1.0)
        rows.append((n, u, lnb))
        print(f"    {n:5d}   {u:4.1f}   1.0   {k:4d}    {lnb:10.2f}          {n * (math.log(2) - hh(lam1 / u)):10.2f}")
r100 = [r for r in rows if r[0] == 100 and r[1] == 1.0][0][2]
check("(d) at n = 100, u = 1, eps = 1 the bound is below e^7 (about a thousand evaluations): exponential only asymptotically", r100 < 7.0)

print()
print("ALL CHECKS PASSED" if OK else "SOME CHECK FAILED")
