#!/usr/bin/env python3
"""Coordinator's own check of Proposition R22-1 of workstream R22 (review of the Geometry division's Theorem B):
two states of a chain that differ in TWO torsions, seen through the mean squared distances M of all pairs.

Claim checked (R22_REPORT.md section 3.3).  Hinge bonds b1, b2 (not parallel), rotations R_j = rot(b_j, theta_j),
e = b1 x b2 / |b1 x b2|, sigma = I - 2 e e^T.  A re-hinged conformation (rho1, rho2): the middle segment is moved by
rho1 about hinge 1, the last segment by rho1 rho2.
 (a) the conformations that are affine images of the stacked pair are exactly the eight
       X1 = (I, I), X2 = (R1, R2), Yi = (R1, sigma), Yii = (I, sigma R2), Yiii = (sigma, R2), Yiv = (R1 sigma, I),
       Yv = (R1 sigma, sigma R2), Yvi = (sigma, sigma);
 (b) D(X1) - D(X2) + D(Yi) - D(Yii) + D(Yiii) - D(Yiv) + D(Yv) - D(Yvi) = 0;
 (c) for angles in general position the mixture of X1 and X2 is the only ensemble with its M;
 (d) for two half-turns D(X1) + D(X2) = D(Yv) + D(Yvi): NOT identified.
Written with the chain builder of hinge_pair.py (the coordinator's), without the referee's code.  Per instance:
 (1) X2 built by the chain builder equals the re-hinging (R1, R2) (fixes the sign convention);
 (2) the eight are chains (bonded distances) and affine images (residual of the projection on span(1, X1, X2));
 (3) identity (b); control: the same sum with all signs + (must not vanish);
 (4) all re-hingings in the four components (rotation or reflection at each hinge): the residual on a 4-degree grid,
     every local minimum refined to convergence; the zeros found must be exactly the eight (by Lemma 2.2 of the Geometry
     division a competing state keeps every shared segment rigid, so it is a re-hinging).  A search, not a proof;
 (5) a linear programme over the eight classes: least mass on {X1, X2} among ensembles with the same M -- 1 in
     general position, 1 - 2 min(w) for two half-turns; control: half-turns moved by 0.3 rad give 1 again.
Run: python3 -B two_hinges.py > two_hinges.log
"""
import itertools, time
import numpy as np
from scipy.optimize import linprog
from scipy.optimize import minimize

t0 = time.time(); COS_ANGLE = -1.0 / 3.0


class HP:                        # the two functions of hinge_pair.py that are used (copied: importing that script would run it)
    @staticmethod
    def chain(torsions):
        th = np.arccos(COS_ANGLE); x = [np.zeros(3), np.array([1.0, 0, 0]), np.array([1.0 - np.cos(th), np.sin(th), 0.0])]
        for phi in torsions:
            a, b, c = x[-3], x[-2], x[-1]; bc = (c - b) / np.linalg.norm(c - b); nrm = np.cross(b - a, bc); nrm /= np.linalg.norm(nrm)
            m = np.cross(nrm, bc); d = np.array([-np.cos(th), np.sin(th) * np.cos(phi), np.sin(th) * np.sin(phi)])
            x.append(c + d[0] * bc + d[1] * m + d[2] * nrm)
        return np.array(x)

    @staticmethod
    def D(X): return ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)


def rot(axis, ang):
    k = axis / np.linalg.norm(axis); K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def rehinge(X1, j1, j2, rho1, rho2):
    """S1 = atoms 0..j1+2 fixed; S2 = atoms j1+3..j2+2 moved by rho1 about atom j1+1; S3 = atoms j2+3.. moved by rho1 rho2"""
    Y = X1.copy(); h1, h2 = X1[j1 + 1], X1[j2 + 1]
    Y[j1 + 3:j2 + 3] = h1 + (X1[j1 + 3:j2 + 3] - h1) @ rho1.T
    Y[j2 + 3:] = h1 + (h2 + (X1[j2 + 3:] - h2) @ rho2.T - h1) @ rho1.T
    return Y


def bonded(X): return np.array([np.linalg.norm(X[i] - X[i + s]) for s in (1, 2) for i in range(len(X) - s)])


def residual(Y, basis):          # squared distance of the centred Y from the column space of the centred stacked pair
    Yc = Y - Y.mean(axis=0); return float(np.linalg.norm(Yc - basis @ (basis.T @ Yc)) ** 2)


def eight(X1, j1, j2, th1, th2):
    b1 = X1[j1 + 2] - X1[j1 + 1]; b2 = X1[j2 + 2] - X1[j2 + 1]; e = np.cross(b1, b2); e /= np.linalg.norm(e); sg = np.eye(3) - 2 * np.outer(e, e)
    R1, R2 = rot(b1, th1), rot(b2, th2); I = np.eye(3)
    pairs = [(I, I), (R1, R2), (R1, sg), (I, sg @ R2), (sg, R2), (R1 @ sg, I), (R1 @ sg, sg @ R2), (sg, sg)]
    return [rehinge(X1, j1, j2, a, b) for a, b in pairs], (b1, b2, e, sg)


rng = np.random.default_rng(20261126); worst = dict(chain=0.0, image=0.0, ident=0.0, conv=0.0); ctrl_plus = []; lp_vals = []; clusters = []
for inst in range(6):
    n = int(rng.integers(22, 30)); tors = rng.uniform(-np.pi, np.pi, n - 3); j1 = int(rng.integers(3, 6)); j2 = int(rng.integers(j1 + 6, n - 8))
    th1, th2 = rng.uniform(0.5, 2.6, 2) * rng.choice([-1, 1], 2); w = np.array([0.37, 0.63])
    X1 = HP.chain(tors); t2 = tors.copy(); t2[j1] += th1; t2[j2] += th2; X2 = HP.chain(t2)
    # (1) sign convention: the chain builder's X2 against the re-hinging (R1, R2) with either sign of the angles
    best = None
    for s1, s2 in itertools.product((1, -1), repeat=2):
        Ys, _ = eight(X1, j1, j2, s1 * th1, s2 * th2); dev = np.abs(HP.D(Ys[1]) - HP.D(X2)).max()
        if best is None or dev < best[0]: best = (dev, s1, s2)
    assert best[0] < 1e-10, best; worst["conv"] = max(worst["conv"], best[0]); Ys, (b1, b2, e, sg) = eight(X1, j1, j2, best[1] * th1, best[2] * th2)
    # (2) chains and affine images
    Z = np.hstack([X1 - X1.mean(axis=0), Ys[1] - Ys[1].mean(axis=0)]); U, s, _ = np.linalg.svd(Z, full_matrices=False); basis = U[:, s > 1e-9 * s[0]]
    assert basis.shape[1] == 6, "the stacked pair must span six dimensions"
    for Y in Ys:
        worst["chain"] = max(worst["chain"], float(np.abs(bonded(Y) - bonded(X1)).max())); worst["image"] = max(worst["image"], residual(Y, basis))
    # (3) identity (b) and its control
    sgn = [1, -1, 1, -1, 1, -1, 1, -1]; Ds = [HP.D(Y) for Y in Ys]
    worst["ident"] = max(worst["ident"], float(np.abs(sum(a * d for a, d in zip(sgn, Ds))).max())); ctrl_plus.append(float(np.abs(sum(Ds) - 8 * Ds[0]).max()))
    # (4) all re-hingings in the four components: a 4-degree grid, every local minimum of the residual refined to convergence
    grid = np.deg2rad(np.arange(0, 360, 4.0)); G = len(grid); zeros = []
    c1 = np.cross(b1, e); c1 /= np.linalg.norm(c1); c2 = np.cross(b2, e); c2 /= np.linalg.norm(c2)

    def member(kind, bvec, cvec, ang):          # rotation about the hinge by ang, or reflection in a plane containing the hinge (normal at angle ang / 2 from e)
        if kind == "rot": return rot(bvec, ang)
        nrm = np.cos(ang / 2) * e + np.sin(ang / 2) * cvec
        return np.eye(3) - 2 * np.outer(nrm, nrm)
    nloc = 0
    for k1, k2 in itertools.product(("rot", "ref"), repeat=2):
        f = lambda a: residual(rehinge(X1, j1, j2, member(k1, b1, c1, a[0]), member(k2, b2, c2, a[1])), basis)
        R = np.array([[f((a1, a2)) for a2 in grid] for a1 in grid])
        for p_ in range(G):
            for q_ in range(G):
                nb = [R[(p_ + dp) % G, (q_ + dq) % G] for dp in (-1, 0, 1) for dq in (-1, 0, 1) if (dp, dq) != (0, 0)]
                if R[p_, q_] <= min(nb):
                    nloc += 1; o = minimize(f, (grid[p_], grid[q_]), method="Nelder-Mead", options=dict(xatol=1e-11, fatol=1e-22, maxiter=4000))
                    if o.fun < 1e-12: zeros.append(rehinge(X1, j1, j2, member(k1, b1, c1, o.x[0]), member(k2, b2, c2, o.x[1])))
    hit = [0] * 8; orphan = 0
    for Y in zeros:
        dd = [np.abs(HP.D(Y) - d).max() for d in Ds]; q = int(np.argmin(dd))
        if dd[q] < 1e-5: hit[q] += 1
        else: orphan += 1
    clusters.append((sum(1 for v in hit if v > 0), orphan, nloc)); found = zeros
    # (5) linear programme over the eight classes
    iu = np.triu_indices(n, 1); A = np.array([d[iu] for d in Ds]).T; target = w[0] * Ds[0][iu] + w[1] * Ds[1][iu]
    res = linprog(np.array([1, 1, 0, 0, 0, 0, 0, 0.0]), A_eq=np.vstack([A, np.ones((1, 8))]), b_eq=np.concatenate([target, [1.0]]), bounds=[(0, None)] * 8, method="highs")
    assert res.status == 0; lp_vals.append(float(res.fun))
    print(f"  instance {inst}: n = {n}, hinges at torsions {j1} and {j2}, angles {th1:+.2f}, {th2:+.2f}: the eight are chains and affine images; {nloc} local minima of the residual on the grid, {len(found)} of them refine to a zero: "
          f"{clusters[-1][0]} of the eight are reached, {orphan} zeros elsewhere; least mass on the two states among ensembles of the eight with the same M: {res.fun:.9f} [{time.time() - t0:.0f}s]", flush=True)
print(f"(1) the chain builder's second state equals the re-hinging (R1, R2): largest deviation of a squared distance {worst['conv']:.1e}")
print(f"(2) the eight conformations: largest deviation of a bonded distance from the chain's {worst['chain']:.1e}; largest residual as an affine image of the stacked pair {worst['image']:.1e} (both must be < 1e-10)")
print(f"(3) the alternating identity (b): largest entry {worst['ident']:.1e} (must be < 1e-10); control, the same eight with all signs +, minus 8 D(X1): {min(ctrl_plus):.2f} to {max(ctrl_plus):.2f} (must not vanish)")
print(f"(4) all re-hingings (4 components, 4-degree grid, every local minimum of the residual refined): (how many of the eight are reached, zeros that are none of them) per instance: {[(c, o) for c, o, _ in clusters]} (must be (8, 0) in every instance)")
print(f"(5) programme over the eight classes, angles in general position: {min(lp_vals):.9f} to {max(lp_vals):.9f} (must be 1: identified)")
assert worst["chain"] < 1e-10 and worst["image"] < 1e-10 and worst["ident"] < 1e-10 and min(ctrl_plus) > 1e-3 and all(c == 8 and o == 0 for c, o, _ in clusters) and min(lp_vals) > 1 - 1e-7
# ---- two half-turns, and the control
hv = []; hid = []; back = []; sep = []
for inst in range(4):
    n = int(rng.integers(22, 30)); tors = rng.uniform(-np.pi, np.pi, n - 3); j1 = int(rng.integers(3, 6)); j2 = int(rng.integers(j1 + 6, n - 8)); w = np.array([0.37, 0.63]); X1 = HP.chain(tors)
    for th, store in ((np.pi, hv), (np.pi - 0.3, back)):
        Ys, _ = eight(X1, j1, j2, th, th); Ds = [HP.D(Y) for Y in Ys]; iu = np.triu_indices(n, 1); A = np.array([d[iu] for d in Ds]).T; target = w[0] * Ds[0][iu] + w[1] * Ds[1][iu]
        res = linprog(np.array([1, 1, 0, 0, 0, 0, 0, 0.0]), A_eq=np.vstack([A, np.ones((1, 8))]), b_eq=np.concatenate([target, [1.0]]), bounds=[(0, None)] * 8, method="highs"); assert res.status == 0
        store.append(float(res.fun))
        if th == np.pi:
            hid.append(float(np.abs(Ds[0] + Ds[1] - Ds[6] - Ds[7]).max())); sep.append(min(float(np.abs(Ds[q] - Ds[r]).max()) for q in (6, 7) for r in (0, 1)))
print(f"(6) two half-turns (4 instances): D(X1) + D(X2) - D(Yv) - D(Yvi): largest entry {max(hid):.1e} (must be < 1e-10); Yv, Yvi differ from both states by at least {min(sep):.2f} in a squared distance; "
      f"least mass on the two states: {min(hv):.6f} to {max(hv):.6f} (must be 1 - 2 min w = 0.26: NOT identified); control, both angles pi - 0.3: {min(back):.6f} to {max(back):.6f} (must be 1)")
assert max(hid) < 1e-10 and min(sep) > 0.1 and max(hv) < 0.26 + 1e-6 and min(hv) > 0.26 - 1e-6 and min(back) > 1 - 1e-7
print(f"ALL DONE {time.time() - t0:.0f} s")
