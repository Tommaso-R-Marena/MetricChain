#!/usr/bin/env python3
"""R22 Item 3(c), route A (decides the question by Theorem B'): two states of a chain that SHARE RIGID SEGMENTS
(they differ in 1, 2 or 3 torsions).  (CC) fails there (coordinator, hinge_pair.py).  Is the mixture identifiable?

Theorem B' (ENSEMBLE_RIGIDITY.md l.246-262): identifiable  <=>  I is the barycentre of exactly one probability measure
on P(z) = {P in I + N(z), P >= 0, rank P <= 3}.  P(z) = {A^T A : x = A z is a chain}, the linear images of z that
are chains.  So:  (1) enumerate P(z)  [multi-start Levenberg-Marquardt on |A e|^2 = |e|^2 over the E0-edges of z,
unknown A in R^{3x6}; no use of my paper derivation];  (2) compare with the list predicted on paper (R22 notes):
for two differing torsions exactly 8 points, (rho1, rho2) in
   (I,I)=X1, (R1,R2)=X2, (R1,s), (I,sR2), (s,R2), (R1s,I), (R1s,sR2), (s,s)
with R_j the rotation of state 2 about hinge j and s the reflection in the plane of the two hinge directions;
(3) a linear programme over the points found: minimise the mass on the two true states subject to
sum c_i P_i = I, c >= 0 (equivalently equal M).  Minimum 1 = identifiable (given the enumeration is complete).
Controls: one differing torsion (the programme MUST find competitors: a continuum of linear images);
the half-turn case theta1 = theta2 = pi (predicted on paper: D(X1)+D(X2) = D(Y_v)+D(Y_vi), NOT identifiable);
a generic pair at n = 12 (CC holds: only the two states may be found).
Run: OMP_NUM_THREADS=1 python3 -B t3c_linear_images.py > t3c_linear_images.log
"""
import time
import numpy as np
from scipy.optimize import least_squares, linprog
import r22lib as L

t0 = time.time()
COS = -1.0 / 3.0


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def enumerate_linear_images(z, nstart, rng, tol=1e-9):
    """all A (3 x m) found with |A e|^2 = |e|^2 on the E0-edges of z; returns list of (D(Az), P=A^T A, hits)"""
    n, m = z.shape
    Ed = np.array([z[j] - z[i] for i, j in L.E0(n)])
    l2 = (Ed ** 2).sum(1)

    def res(a):
        A = a.reshape(3, m)
        return ((Ed @ A.T) ** 2).sum(1) / l2 - 1.0

    def jac(a):
        A = a.reshape(3, m)
        AE = Ed @ A.T                                    # (edges, 3)
        return (2.0 * AE[:, :, None] * Ed[:, None, :] / l2[:, None, None]).reshape(len(Ed), 3 * m)

    found = []
    nconv = 0
    for s in range(nstart):
        a0 = rng.normal(size=3 * m) * rng.uniform(0.3, 2.5)
        try:
            sol = least_squares(res, a0, jac=jac, method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        except Exception:
            continue
        if np.abs(sol.fun).max() > tol:
            continue
        nconv += 1
        A = sol.x.reshape(3, m)
        Dx = L.sqdist(z @ A.T)
        for f in found:
            if np.abs(f[0] - Dx).max() < 1e-5:
                f[2] += 1
                break
        else:
            found.append([Dx, A.T @ A, 1])
    return found, nconv


def lp_min_true_mass(Ds, M, true_idx):
    """min mass on the true states s.t. sum c_i D_i = M, sum c = 1, c >= 0.  Ds: list of n x n matrices."""
    n = M.shape[0]
    iu = [(i, j) for i in range(n) for j in range(i + 3, n)]
    Aeq = np.array([[D[i, j] for D in Ds] for (i, j) in iu] + [[1.0] * len(Ds)])
    beq = np.array([M[i, j] for (i, j) in iu] + [1.0])
    c = np.zeros(len(Ds))
    c[list(true_idx)] = 1.0
    r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(Ds), method="highs",
                options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
    return r


def build(n, hinges, thetas, rng):
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    t2 = t1.copy()
    for h, th in zip(hinges, thetas):
        t2[h] += th
    return t1, t2, L.chain(t1, COS), L.chain(t2, COS)


def rehinge(X1, hinges, rhos):
    """conformation with segment maps B_1 = I, B_{j+1} = B_j rho_j (rho_j fixes hinge direction j in the frame of X1)"""
    X = X1.copy()
    B = np.eye(3)
    for h, rho in zip(hinges, rhos):
        p = h + 1                                         # hinge atoms h+1, h+2; torsion h moves atoms >= h+3
        B = B @ rho
        X[p:] = X[p] + (X1[p:] - X1[p]) @ B.T
    return X


def in_C(X, X1):
    D, D1 = L.sqdist(X), L.sqdist(X1)
    return max(abs(D[i, j] - D1[i, j]) for i, j in L.E0(len(X)))


print("=== R22 3(c) route A: linear images of the stacked pair that are chains, then a linear programme (Theorem B')")
print(f"unit bonds, cos(bond angle) = {COS:.4f}; weights (0.37, 0.63); seed 2203")
rng = np.random.default_rng(2203)
W = (0.37, 0.63)
summary = []

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (0) control: generic pair, n = 12 ((CC) holds): the enumeration may find only the two states")
n = 12
X1 = L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS)
X2 = L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS)
z = L.stack([X1, X2], W)
found, nconv = enumerate_linear_images(z, 300, rng)
dimN = L.conic_nullity(z)[0]
is_true = [min(np.abs(f[0] - L.sqdist(Xk)).max() for Xk in (X1, X2)) < 1e-5 for f in found]
print(f"    dim N(z) = {dimN}; {nconv} of 300 starts converged; distinct linear images found: {len(found)}; of these the two states: {sum(is_true)}")
ctrl0 = int(not (len(found) == 2 and sum(is_true) == 2 and dimN == 1))

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (1) control: ONE differing torsion (must be non-identifiable): linear images form a continuum")
n, hinges = 16, [6]
t1, t2, X1, X2 = build(n, hinges, [1.9], rng)
z = L.stack([X1, X2], W)
rk = np.linalg.matrix_rank(z - z.mean(0), tol=1e-9)
found, nconv = enumerate_linear_images(z, 300, rng)
Ds = [L.sqdist(X1), L.sqdist(X2)] + [f[0] for f in found]
M = W[0] * Ds[0] + W[1] * Ds[1]
r = lp_min_true_mass(Ds, M, (0, 1))
far = [i for i, D in enumerate(Ds[2:]) if min(np.abs(D - Ds[0]).max(), np.abs(D - Ds[1]).max()) > 1e-3]
print(f"    n = {n}, hinge torsion {hinges}: affine rank of z = {rk} (of 6); dim N(z) = {L.conic_nullity(z)[0]}; "
      f"{nconv} of 300 starts converged to {len(found)} distinct linear images ({len(far)} of them other shapes)")
print(f"    linear programme over the true states and the {len(found)} images: minimal mass on the two true states = {r.fun:.3e} "
      f"(status {r.status}); 0 = a competing ensemble of other conformations exists (expected)")
ctrl1 = int(not (r.status == 0 and r.fun < 1e-7 and len(far) > 20))
summary.append(("1 torsion (control)", n, len(found), r.fun))

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (2) TWO differing torsions, long segments")
print("| n | hinges | thetas | dim N | LM: converged/starts | distinct images | match the 8 predicted | predicted all found | "
      "max |e-length err| of predicted | max phi of predicted | alternating affine dependency residual | LP: min mass on true states |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
viol2 = 0
cases2 = [(16, [4, 9], None), (16, [3, 8], None), (20, [5, 12], None), (20, [6, 11], None), (26, [7, 16], None), (26, [9, 15], None),
          (14, [3, 7], None), (14, [4, 8], None)]
for (n, hinges, _) in cases2:
    th = rng.uniform(0.5, 2.6, 2) * rng.choice([-1, 1], 2)
    t1, t2, X1, X2 = build(n, hinges, th, rng)
    z = L.stack([X1, X2], W)
    Pperp, _ = L.perp_projector(z)
    b = [X1[h + 2] - X1[h + 1] for h in hinges]
    e = np.cross(b[0], b[1])
    e /= np.linalg.norm(e)
    s = np.eye(3) - 2.0 * np.outer(e, e)
    R1, R2 = rot(b[0], th[0]), rot(b[1], th[1])
    I3 = np.eye(3)
    pred = [(I3, I3), (R1, R2), (R1, s), (I3, s @ R2), (s, R2), (R1 @ s, I3), (R1 @ s, s @ R2), (s, s)]
    Y = [rehinge(X1, hinges, rr) for rr in pred]
    chk_state2 = np.abs(L.sqdist(Y[1]) - L.sqdist(X2)).max()
    lerr = max(in_C(y, X1) for y in Y)
    phis = max(float(((Pperp @ y) ** 2).sum()) for y in Y)
    DY = [L.sqdist(y) for y in Y]
    sep = min(np.abs(DY[a] - DY[c]).max() for a in range(8) for c in range(a + 1, 8))
    alt = np.abs(sum(((-1) ** k) * DY[k] for k in range(8))).max()
    found, nconv = enumerate_linear_images(z, 400, rng)
    match = sum(int(min(np.abs(f[0] - D).max() for D in DY) < 1e-5) for f in found)
    allfound = sum(int(min(np.abs(f[0] - D).max() for f in found) < 1e-5) for D in DY)
    # LP over the union of predicted and found
    Ds = DY + [f[0] for f in found if min(np.abs(f[0] - D).max() for D in DY) >= 1e-5]
    M = W[0] * DY[0] + W[1] * DY[1]
    r = lp_min_true_mass(Ds, M, (0, 1))
    ok = (len(found) == 8 and match == 8 and allfound == 8 and lerr < 1e-10 and phis < 1e-18 and alt < 1e-9
          and abs(r.fun - 1.0) < 1e-7 and chk_state2 < 1e-10 and sep > 1e-3)
    viol2 += int(not ok)
    print(f"| {n} | {hinges} | {th[0]:+.3f}, {th[1]:+.3f} | {L.conic_nullity(z)[0]} | {nconv}/400 | {len(found)} | {match} | {allfound} | "
          f"{lerr:.1e} | {phis:.1e} | {alt:.1e} | {r.fun:.9f} |" + ("" if ok else "  <-- differs from the prediction"))
    summary.append(("2 torsions", n, len(found), r.fun))
print(f"    two torsions: {viol2} of {len(cases2)} cases differ from the paper prediction (8 images = the predicted ones; "
      f"P1-P2+Pi-Pii+Piii-Piv+Pv-Pvi = 0; LP minimum 1)")

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (2h) the half-turn case theta1 = theta2 = pi (predicted NOT identifiable)")
print("| n | hinges | max |D(X1)+D(X2)-D(Yv)-D(Yvi)| | Procrustes d_P^2 of Yv, Yvi to the nearer true state | LP: min mass on true states | 1 - 2 min(w) |")
print("|---|---|---|---|---|---|")
violh = 0
for (n, hinges) in ((16, [4, 9]), (20, [5, 12]), (26, [8, 16])):
    th = np.array([np.pi, np.pi])
    t1, t2, X1, X2 = build(n, hinges, th, rng)
    b = [X1[h + 2] - X1[h + 1] for h in hinges]
    e = np.cross(b[0], b[1])
    e /= np.linalg.norm(e)
    s = np.eye(3) - 2.0 * np.outer(e, e)
    R1, R2 = rot(b[0], th[0]), rot(b[1], th[1])
    I3 = np.eye(3)
    pred = [(I3, I3), (R1, R2), (R1, s), (I3, s @ R2), (s, R2), (R1 @ s, I3), (R1 @ s, s @ R2), (s, s)]
    Y = [rehinge(X1, hinges, rr) for rr in pred]
    DY = [L.sqdist(y) for y in Y]
    idn = np.abs(DY[0] + DY[1] - DY[6] - DY[7]).max()
    dp = [min(L.procrustes2(Y[k], X1), L.procrustes2(Y[k], X2)) for k in (6, 7)]
    lerr = max(in_C(y, X1) for y in Y)
    M = W[0] * DY[0] + W[1] * DY[1]
    r = lp_min_true_mass(DY, M, (0, 1))
    ok = idn < 1e-10 and min(dp) > 1e-2 and abs(r.fun - (1 - 2 * min(W))) < 1e-6 and lerr < 1e-10
    violh += int(not ok)
    print(f"| {n} | {hinges} | {idn:.1e} | {dp[0]:.3f}, {dp[1]:.3f} | {r.fun:.9f} | {1 - 2 * min(W):.9f} |" + ("" if ok else "  <-- differs"))
    summary.append(("2 torsions, both half-turns", n, 8, r.fun))
# how close to a half turn does it matter?  (the LP minimum is 1 for every other angle; shown for information)
n, hinges = 20, [5, 12]
row = []
for d in (0.3, 0.1, 0.01, 0.0):
    th = np.array([np.pi - d, np.pi - d])
    t1, t2, X1, X2 = build(n, hinges, th, np.random.default_rng(77))
    b = [X1[h + 2] - X1[h + 1] for h in hinges]
    e = np.cross(b[0], b[1]); e /= np.linalg.norm(e)
    s = np.eye(3) - 2.0 * np.outer(e, e); R1, R2 = rot(b[0], th[0]), rot(b[1], th[1]); I3 = np.eye(3)
    pred = [(I3, I3), (R1, R2), (R1, s), (I3, s @ R2), (s, R2), (R1 @ s, I3), (R1 @ s, s @ R2), (s, s)]
    DY = [L.sqdist(rehinge(X1, hinges, rr)) for rr in pred]
    r = lp_min_true_mass(DY, W[0] * DY[0] + W[1] * DY[1], (0, 1))
    row.append(f"pi-{d}: {r.fun:.6f}")
print("    LP minimum of the mass on the true states for theta1 = theta2 = " + "; ".join(row))
print(f"    half-turn case: {violh} of 3 cases differ from the prediction (identity exact, competitor of other shapes, LP minimum 1 - 2 min w)")

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (3) THREE differing torsions, long segments")
print("| n | hinges | dim N | LM: converged/starts | distinct images | of these the two states | LP: min mass on true states |")
print("|---|---|---|---|---|---|---|")
viol3 = 0
for (n, hinges) in ((20, [4, 9, 14]), (20, [3, 8, 13]), (26, [5, 12, 19]), (26, [6, 11, 18]), (32, [7, 15, 23]), (18, [3, 7, 11])):
    th = rng.uniform(0.5, 2.6, 3) * rng.choice([-1, 1], 3)
    t1, t2, X1, X2 = build(n, hinges, th, rng)
    z = L.stack([X1, X2], W)
    found, nconv = enumerate_linear_images(z, 400, rng)
    D1, D2 = L.sqdist(X1), L.sqdist(X2)
    ntrue = sum(int(min(np.abs(f[0] - D1).max(), np.abs(f[0] - D2).max()) < 1e-5) for f in found)
    Ds = [D1, D2] + [f[0] for f in found if min(np.abs(f[0] - D1).max(), np.abs(f[0] - D2).max()) >= 1e-5]
    r = lp_min_true_mass(Ds, W[0] * D1 + W[1] * D2, (0, 1))
    ok = len(found) == 2 and ntrue == 2 and abs(r.fun - 1.0) < 1e-7
    viol3 += int(not ok)
    print(f"| {n} | {hinges} | {L.conic_nullity(z)[0]} | {nconv}/400 | {len(found)} | {ntrue} | {r.fun:.9f} |" + ("" if ok else "  <-- more than the two states"))
    summary.append(("3 torsions", n, len(found), r.fun))
print(f"    three torsions: {viol3} of 6 cases with a linear image other than the two states")

print("\n--- (3h) three differing torsions, all half-turns (information; no paper prediction)")
for (n, hinges) in ((20, [4, 9, 14]), (26, [5, 12, 19])):
    th = np.array([np.pi] * 3)
    t1, t2, X1, X2 = build(n, hinges, th, rng)
    z = L.stack([X1, X2], W)
    found, nconv = enumerate_linear_images(z, 400, rng)
    D1, D2 = L.sqdist(X1), L.sqdist(X2)
    Ds = [D1, D2] + [f[0] for f in found if min(np.abs(f[0] - D1).max(), np.abs(f[0] - D2).max()) >= 1e-5]
    r = lp_min_true_mass(Ds, W[0] * D1 + W[1] * D2, (0, 1))
    print(f"    n = {n}, hinges {hinges}, thetas pi: dim N = {L.conic_nullity(z)[0]}; {nconv}/400 converged; distinct images {len(found)}; LP minimum on true states {r.fun:.9f}")

# ---------------------------------------------------------------------------------------------------------------
print("\n--- (4) short segments (fewer than 5 atoms between hinges: the segment's edge directions lie on a conic)")
for (n, hinges) in ((16, [5, 6]), (16, [5, 7]), (16, [5, 8]), (16, [1, 8]), (16, [2, 8])):
    th = rng.uniform(0.5, 2.6, 2) * rng.choice([-1, 1], 2)
    t1, t2, X1, X2 = build(n, hinges, th, rng)
    z = L.stack([X1, X2], W)
    found, nconv = enumerate_linear_images(z, 400, rng)
    D1, D2 = L.sqdist(X1), L.sqdist(X2)
    Ds = [D1, D2] + [f[0] for f in found if min(np.abs(f[0] - D1).max(), np.abs(f[0] - D2).max()) >= 1e-5]
    r = lp_min_true_mass(Ds, W[0] * D1 + W[1] * D2, (0, 1))
    seg = [hinges[0] + 3, hinges[1] - hinges[0] + 2, n - 1 - hinges[1]]
    print(f"    n = {n}, hinges {hinges} (segment sizes {seg}): dim N = {L.conic_nullity(z)[0]}; {nconv}/400 converged; distinct images {len(found)}; "
          f"LP minimum on true states {r.fun:.6f} (status {r.status})")

print("\n--- summary")
for name, n, k, v in summary:
    print(f"    {name:30s} n = {n:2d}: {k:3d} linear images; LP minimum of the mass on the two true states {v:.6f}")
print(f"control violations: generic pair {ctrl0}, one torsion {ctrl1};  prediction violations: two torsions {viol2}, half-turn {violh}, three torsions {viol3}")
print(f"ALL DONE {time.time() - t0:.1f} s")
