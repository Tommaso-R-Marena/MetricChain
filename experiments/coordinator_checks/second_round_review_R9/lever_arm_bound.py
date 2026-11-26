#!/usr/bin/env python3
"""V9 -- text point 5 (Theorem 11.36): is workstream G's bound I-bar(m) = sum_{p<=m} d-bar(p)^2 attained by the arm
'one gauche torsion next to the axis, then all-trans'?  Chain with unit bonds and bond angle theta, built by the usual
internal-coordinate construction; moment of inertia of the arm atoms about the line of the axis bond.
Prints I(m)/I-bar(m) for the one-kink arm and for the all-trans arm, and the angle between the zigzag axis of the arm
and the torsion axis."""
import numpy as np, math

def build(theta_deg, torsions_deg):
    """atoms 0,1,2 fixed; atom k+3 placed from atoms k, k+1, k+2 with bond 1, angle theta, torsion torsions[k]"""
    th = math.radians(theta_deg)
    X = [np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])]
    X.append(X[1] + np.array([-math.cos(th), math.sin(th), 0.0]))
    for phi in torsions_deg:
        a, b, c = X[-3], X[-2], X[-1]
        bc = (c - b) / np.linalg.norm(c - b)
        n = np.cross(b - a, bc); n /= np.linalg.norm(n)
        m = np.cross(n, bc)
        ph = math.radians(phi)
        d = np.array([-math.cos(th), math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph)])
        X.append(c + d[0] * bc + d[1] * m + d[2] * n)
    return np.array(X)

def inertia_about_axis(X, i, m):
    """axis = bond (i, i+1), axis atom i+1; arm = the m atoms at chain distance 1..m from the axis atom
    (atoms i+2 .. i+m+1), as in workstream G, section 2.1(c)"""
    u = X[i + 1] - X[i]; u /= np.linalg.norm(u)
    tot = 0.0
    for p in range(1, m + 1):
        r = X[i + 1 + p] - X[i + 1]
        tot += r @ r - (r @ u) ** 2
    return tot

def dbar(p, theta_deg):
    s = math.sin(math.radians(theta_deg) / 2)
    return 2 * (p // 2) * s + (p % 2)

for theta in (math.degrees(math.acos(-1 / 3)), 111.0):
    s2 = math.sin(math.radians(theta) / 2) ** 2
    print(f"theta = {theta:.4f} deg: sin^2(theta/2)/3 = {s2/3:.6f}")
    for m in (12, 50, 200, 1000, 4000):
        Ibar = sum(dbar(p, theta) ** 2 for p in range(1, m + 1))
        best = {}
        for name, first in (("one gauche (+60) then trans", 60.0), ("one gauche (-60) then trans", -60.0), ("all-trans", 180.0)):
            # axis bond = (1, 2), axis atom 2: the arm is atoms 3 .. m+2; the torsion about bond (2,3) is the first one listed after the axis torsion
            X = build(theta, [180.0, first] + [180.0] * (m + 2))
            I = inertia_about_axis(X, 1, m)
            best[name] = I
        zz = X = build(theta, [180.0, 60.0] + [180.0] * (m + 2))
        u = zz[2] - zz[1]; u /= np.linalg.norm(u)
        w = zz[m] - zz[m - 2]; w /= np.linalg.norm(w)
        ang = math.degrees(math.acos(abs(u @ w)))
        print(f"   m = {m:5d}: I-bar/m^3 = {Ibar/m**3:.6f};  I/m^3 of the one-kink arm = {best['one gauche (+60) then trans']/m**3:.6f};  I/I-bar: " + ", ".join(f"{k}: {v/Ibar:.6f}" for k, v in best.items()) + f";  angle(zigzag axis, torsion axis) = {ang:.4f} deg, sin^2 = {math.sin(math.radians(ang))**2:.6f}")

# ---- addendum: can a longer rotamer prefix (trans / gauche+ / gauche-) bring the all-trans arm closer to perpendicular
#      at theta = 111 deg?  For every prefix of k torsions after the axis bond, the angle between the zigzag axis of the
#      all-trans continuation and the torsion axis; sin^2 of it is the asymptotic ratio I / I-bar of that arm.
import itertools
print("\nprefix search at theta = 111 deg (torsions after the axis bond, then all-trans): best asymptotic ratio sin^2(angle)")
for k in range(1, 10):
    best = (0.0, None)
    for pre in itertools.product((180.0, 60.0, -60.0), repeat=k):
        X = build(111.0, [180.0] + list(pre) + [180.0] * 8)
        u = X[2] - X[1]; u /= np.linalg.norm(u)
        w = X[-1] - X[-3]; w /= np.linalg.norm(w)
        s2 = 1.0 - (u @ w) ** 2
        if s2 > best[0]:
            best = (s2, pre)
    print(f"   prefix length {k}: best sin^2 = {best[0]:.6f} (1 - {1-best[0]:.2e}), prefix {['t' if p == 180.0 else ('g+' if p > 0 else 'g-') for p in best[1]]}")
