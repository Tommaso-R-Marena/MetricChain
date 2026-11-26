#!/usr/bin/env python3
"""R9, item 2(d): the lever-arm constant.  Own code (numpy only), written from the definitions:
chain with bond length b = 1, bond angle theta, torsions in {180, +60, -60} degrees; arm of m atoms beyond the
torsion axis (the bond between atoms 0 and 1; arm atoms 2..m+1); I = sum of squared distances from the axis.
(1) the formula (2/sqrt3) sin(delta/2) sin(theta/2) at the two parameter sets; 4/3 = sqrt2 * 2sqrt2/3.
(2) G_REPORT 2.1(c): Ibar(m) = sum_p dbar(p)^2, dbar(p) = 2 floor(p/2) sin(theta/2) + (p mod 2): ratio to m^3,
    monotone decrease to sin^2(theta/2)/3.
(3) the arm 'one gauche next to the axis, then all-trans': angle to the axis; I/m^3 for large m; and the exhaustive
    maximum of I over all 3^k settings of the first k arm torsions (rest all-trans).
"""
import itertools, math
import numpy as np

def build(theta_deg, torsions):
    """atoms 0..len(torsions)+2 with bond length 1; torsion j is the dihedral of atoms (j, j+1, j+2, j+3)"""
    th = math.radians(theta_deg)
    X = [np.array([0.0, 0, 0]), np.array([1.0, 0, 0]), np.array([1 - math.cos(th), math.sin(th), 0.0])]
    for phi in torsions:
        a, b, c = X[-3], X[-2], X[-1]
        bc = c - b; bc /= np.linalg.norm(bc)
        n = np.cross(b - a, bc); n /= np.linalg.norm(n)
        m = np.cross(n, bc)
        ph = math.radians(phi)
        d = np.array([-math.cos(th), math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph)])
        X.append(c + d[0] * bc + d[1] * m + d[2] * n)
    return np.array(X)

def inertia_about_first_bond(X, m):
    """sum over arm atoms 2..m+1 of the squared distance from the line through atoms 0, 1"""
    u = X[1] - X[0]; u /= np.linalg.norm(u)
    P = X[2:m + 2] - X[1]
    perp = P - np.outer(P @ u, u)
    return float((perp ** 2).sum())

for th, dl in ((111.0, 120.0), (math.degrees(math.acos(-1 / 3)), 180.0), (math.degrees(math.acos(-1 / 3)), 120.0)):
    s = math.sin(math.radians(th / 2))
    print(f"theta = {th:.4f}, delta = {dl}: (2/sqrt3) sin(delta/2) sin(theta/2) = {2 / math.sqrt(3) * math.sin(math.radians(dl / 2)) * s:.6f};"
          f"  sin^2(theta/2)/3 = {s * s / 3:.6f}")
print("2 sqrt2/3 =", 2 * math.sqrt(2) / 3, "; sqrt2 * 2sqrt2/3 =", 4 / 3)

for th in (111.0, math.degrees(math.acos(-1 / 3))):
    s = math.sin(math.radians(th / 2))
    print(f"\ntheta = {th:.4f}:  G's bound Ibar(m)/m^3 (limit {s*s/3:.6f}):")
    prev = None; mono = True
    row = []
    for m in range(1, 4001):
        I = sum((2 * (p // 2) * s + (p % 2)) ** 2 for p in range(1, m + 1)) if m < 60 else None
        if m < 60:
            r = I / m ** 3
            if prev is not None and r > prev + 1e-15: mono = False
            prev = r
            if m in (1, 2, 3, 5, 10, 20, 40): row.append((m, round(r, 5)))
    # closed evaluation for large m by cumulative sums
    p = np.arange(1, 200001)
    d = 2 * (p // 2) * s + (p % 2)
    cs = np.cumsum(d ** 2) / p.astype(float) ** 3
    mono_all = bool(np.all(np.diff(cs) <= 1e-15))
    print("   ", row, " m=200:", round(cs[199], 5), " m=2e5:", round(cs[-1], 6), "; nonincreasing for all m <= 2e5:", mono_all,
          "; 2 sin(60) sqrt(Ibar(m))/m^1.5 at m = 10, 100, 1000:", [round(2 * math.sin(math.radians(60)) * math.sqrt(cs[k - 1]), 4) for k in (10, 100, 1000)])
    # NOTE on indices: build(theta, tors) places atoms 0,1,2 and then uses tors[j] = dihedral of atoms (j, j+1, j+2, j+3),
    # i.e. tors[0] is the torsion about the FIRST ARM BOND (1-2), seen from the axis bond (0-1).  The torsion about the
    # axis itself only rotates the whole arm about the axis and does not change any distance from the axis.
    for first in (180.0, 60.0, -60.0):
        m = 2000
        X = build(th, [first] + [180.0] * (m - 1))
        u = X[1] - X[0]
        e = X[-1] - X[-3]; e /= np.linalg.norm(e)
        ang = math.degrees(math.acos(abs(float(e @ u))))
        print(f"    torsion about the first arm bond = {first:6.1f}, rest all-trans: angle(zigzag, axis) = {ang:7.3f} deg;"
              f"  I/m^3 at m = 200, 2000: {inertia_about_first_bond(X, 200)/200**3:.5f}, {inertia_about_first_bond(X, 2000)/2000**3:.5f};"
              f"  sin^2(theta/2) sin^2(angle)/3 = {s*s*math.sin(math.radians(ang))**2/3:.5f}")
    # asymptotic direction after an arbitrary prefix of k rotamer torsions (then all-trans): the leading term of I/m^3 is
    # sin^2(theta/2) sin^2(angle)/3; largest sin^2(angle) over all 3^k prefixes
    for k in range(1, 10):
        best = (0.0, None)
        for tors in itertools.product((180.0, 60.0, -60.0), repeat=k):
            X = build(th, list(tors) + [180.0] * 4)
            u = X[1] - X[0]
            e = X[-1] - X[-3]; e /= np.linalg.norm(e)
            s2 = 1 - float(e @ u) ** 2
            if s2 > best[0] + 1e-12: best = (s2, tors)
        print(f"    prefix of {k} torsions then all-trans: max sin^2(angle to the axis) = {best[0]:.6f} at {best[1]}")
    # exhaustive maximum of I at finite m
    for k, m in ((5, 40), (6, 100), (7, 200)):
        best = (0, None)
        for tors in itertools.product((180.0, 60.0, -60.0), repeat=k):
            X = build(th, list(tors) + [180.0] * (m - k))
            I = inertia_about_first_bond(X, m)
            if I > best[0]: best = (I, tors)
        print(f"    exhaustive over the first {k} arm torsions (rest all-trans), m = {m}: max I/m^3 = {best[0]/m**3:.5f} at {best[1]};"
              f"  bound Ibar(m)/m^3 = {cs[m-1]:.5f};  ratio = {best[0]/m**3/cs[m-1]:.5f}")
