#!/usr/bin/env python3
"""Two states of a chain that differ in one torsion angle are never identified by mean squared distances.

Object: the Geometry division's first checkpoint (branch research/geometric-inference, commit d84a43b,
docs/geometry/ENSEMBLE_RIGIDITY.md): an ensemble of conformations of a chain with fixed bond lengths and bond
angles, seen through M_ij = <|x_i - x_j|^2>.  Their Theorem B: if the quadrics through the constrained edge
directions of the stacked configuration are only the K - 1 trivial ones (their condition (CC)), the mixture is the
only probability measure on conformations with its M; (CC) holds for generic conformations from a threshold in n.

This script, written from their definitions without their code, checks a remark of the coordinator (SCI-RES-0029):
  (1) if X(phi) is the chain with one torsion set to phi and all others fixed, every |x_i - x_j|^2 is of the form
      a_ij + b_ij cos(phi) + c_ij sin(phi)  (a point rotating about an axis);
  (2) hence a mixture of X(0) and X(theta) with weights 1 - w, w has the same M as ANY measure on the circle of
      phi with the same mean of exp(i phi) -- for instance the two-point mixtures on the other chords through
      m = (1 - w) + w exp(i theta); its states are not congruent to X(0), X(theta);
  (3) accordingly (CC) fails for such a pair at every chain length, and more generally whenever the two states
      differ in at most three torsions: with s rigid segments shared by the two states the space of quadrics has
      dimension at least 21 - 6 s + s (s - 1) / 2 = 10, 6, 3 for s = 2, 3, 4 (the stacked edge vectors of a shared
      segment lie in a three-dimensional subspace, and two such subspaces meet in a line); it holds for a pair
      with all torsions different once n >= 12 (their threshold for K = 2);
  (4) the same count with the differing torsions spread evenly along a chain of 80 atoms;
  (5) in general every squared distance is multilinear in (1, cos, sin) of the torsions between the two atoms, so
      M sees a distribution of torsion angles only through Fourier coefficients with all indices in {-1, 0, 1}.
Controls: a two-point mixture on a chord that misses m (must give a different M); the fit of (1) with the second
harmonic and the fit of (5) without the product functions (must fail); the dimension count on a generic pair (must
be exactly 1 at n >= 12 and larger below).
Run: python3 -B hinge_pair.py > hinge_pair.log
"""
import numpy as np, itertools, time

t0 = time.time()
COS_ANGLE = -1.0 / 3.0   # bond angle, tetrahedral; unit bonds


def chain(torsions):
    """n = len(torsions) + 3 atoms, unit bonds, fixed bond angle, given torsions (NeRF construction)."""
    th = np.arccos(COS_ANGLE); x = [np.zeros(3), np.array([1.0, 0, 0]), np.array([1.0 - np.cos(th), np.sin(th), 0.0])]
    for phi in torsions:
        a, b, c = x[-3], x[-2], x[-1]; bc = (c - b) / np.linalg.norm(c - b); nrm = np.cross(b - a, bc); nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc); d = np.array([-np.cos(th), np.sin(th) * np.cos(phi), np.sin(th) * np.sin(phi)])
        x.append(c + d[0] * bc + d[1] * m + d[2] * nrm)
    return np.array(x)


def D(X): return ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)


def edges(n): return [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]


def conic_dim(states, weights):
    """dimension of the space of quadrics through the constrained edge vectors of the stacked configuration"""
    z = np.concatenate([np.sqrt(w) * X for X, w in zip(states, weights)], axis=1); m = z.shape[1]
    idx = [(a, b) for a in range(m) for b in range(a, m)]; rows = []
    for i, j in edges(len(z)):
        e = z[j] - z[i]; rows.append([e[a] * e[b] * (1 if a == b else 2) for a, b in idx])
    s = np.linalg.svd(np.array(rows), compute_uv=False); rank = int((s > 1e-9 * s[0]).sum())
    return len(idx) - rank, float(s[rank - 1] / s[0]), (float(s[rank] / s[0]) if rank < len(s) else 0.0)


rng = np.random.default_rng(20261126)
print("=== hinge pairs: two states that differ in one torsion (unit bonds, cos(bond angle) = -1/3); seed 20261126")
print("(1) every squared distance of X(phi) is a + b cos(phi) + c sin(phi): largest residual of a least-squares fit on 64 angles")
for n in (8, 14, 20):
    tors = rng.uniform(-np.pi, np.pi, n - 3); h = (n - 3) // 2; phis = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    Ds = []
    for p in phis:
        t = tors.copy(); t[h] = p; Ds.append(D(chain(t)))
    Ds = np.array(Ds); B = np.stack([np.ones_like(phis), np.cos(phis), np.sin(phis)], 1)
    coef, *_ = np.linalg.lstsq(B, Ds.reshape(64, -1), rcond=None); res = np.abs(B @ coef - Ds.reshape(64, -1)).max()
    B2 = np.stack([np.ones_like(phis), np.cos(2 * phis), np.sin(2 * phis)], 1)
    coef2, *_ = np.linalg.lstsq(B2, Ds.reshape(64, -1), rcond=None); res2 = np.abs(B2 @ coef2 - Ds.reshape(64, -1)).max()
    print(f"    n = {n}, torsion {h}: residual {res:.2e}; control, the same fit with cos(2 phi), sin(2 phi) instead: {res2:.2e} (must be large)")

print("(2) competitors on other chords through m = (1 - w) + w exp(i theta)")
viol = 0; ctrl_viol = 0; ctrl_n = 0; tests = 0
for n in (8, 14, 20):
    for trial in range(5):
        tors = rng.uniform(-np.pi, np.pi, n - 3); h = int(rng.integers(0, n - 3)); theta = rng.uniform(0.4, 2 * np.pi - 0.4); w = rng.uniform(0.2, 0.8)

        def X(p):
            t = tors.copy(); t[h] = tors[h] + p; return chain(t)
        M = (1 - w) * D(X(0.0)) + w * D(X(theta)); m = (1 - w) + w * np.exp(1j * theta)
        for k in range(4):
            psi = rng.uniform(0, 2 * np.pi); u = np.exp(1j * psi)                       # chord through m in direction u
            # points m + s u on the unit circle: s^2 + 2 s Re(conj(m) u) + |m|^2 - 1 = 0
            bq = (np.conj(m) * u).real; disc = bq * bq - (abs(m) ** 2 - 1); s1, s2 = -bq - np.sqrt(disc), -bq + np.sqrt(disc)
            p, q = m + s1 * u, m + s2 * u; wq = -s1 / (s2 - s1); a1, a2 = np.angle(p), np.angle(q)
            Mnu = (1 - wq) * D(X(a1)) + wq * D(X(a2)); diff = np.abs(Mnu - M).max()
            # the competitor's states are other shapes: compare distance matrices with those of the two true states
            other = min(np.abs(D(X(a)) - D(X(b))).max() for a in (a1, a2) for b in (0.0, theta))
            tests += 1; viol += int(diff > 1e-10 or other < 1e-3 or not (0 < wq < 1))
            # control: a chord that misses m (shift m by 0.1 along the normal of the chord)
            m2 = m + 0.1j * u; bq2 = (np.conj(m2) * u).real; disc2 = bq2 * bq2 - (abs(m2) ** 2 - 1)
            if disc2 > 0:
                t1, t2 = -bq2 - np.sqrt(disc2), -bq2 + np.sqrt(disc2); p2, q2 = m2 + t1 * u, m2 + t2 * u; wq2 = -t1 / (t2 - t1)
                Mc = (1 - wq2) * D(X(np.angle(p2))) + wq2 * D(X(np.angle(q2))); ctrl_n += 1; ctrl_viol += int(np.abs(Mc - M).max() > 1e-10)
            if trial == 0 and k == 0:
                print(f"    n = {n}: states at 0 and {theta:.4f} with weights {1 - w:.4f}, {w:.4f}; competitor at {a1:.4f} and {a2:.4f} with weights {1 - wq:.4f}, {wq:.4f}: "
                      f"largest difference of the two matrices M {diff:.2e}; its states differ from the true ones by at least {other:.3f} in a squared distance")
print(f"    {tests} competitors on 15 chains: {viol} violations of 'same M, other shapes, weights in (0,1)'; control (the chord shifted off m by 0.1, where the shifted chord still meets the circle: {ctrl_n} cases): {ctrl_viol} give a different M (must be all)")

print("(3) dimension of the space of quadrics through the constrained edge directions of the stacked pair (K = 2; the trivial ones: 1; (CC) holds iff the entry is 1)")
print("    three random pairs per cell (weights 0.37, 0.63); 'all' = every torsion different (their generic case)")
kinds = (1, 2, 3, 4, 5, 6, 8, None)
print("| n | " + " | ".join(("all" if k is None else f"{k} torsion{'s' if k > 1 else ''} differ{'' if k and k > 1 else 's'}") for k in kinds) + " |")
print("|---|" + "---|" * len(kinds))
for n in (8, 10, 11, 12, 14, 20, 40, 80):
    out = []
    for kind in kinds:
        if kind is not None and kind > n - 3: out.append("-"); continue
        dims = []
        for trial in range(3):
            t1 = rng.uniform(-np.pi, np.pi, n - 3); t2 = t1.copy()
            where = range(n - 3) if kind is None else rng.choice(n - 3, size=kind, replace=False)
            for h in where: t2[h] = rng.uniform(-np.pi, np.pi)
            dims.append(conic_dim([chain(t1), chain(t2)], [0.37, 0.63])[0])
        out.append("/".join(str(d) for d in dims))
    print(f"| {n} | " + " | ".join(out) + " |")
print("(4) the same at n = 80 with the differing torsions spread evenly along the chain (segments of equal length), 5 random pairs per row: smallest and largest dimension")
for kind in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12):
    dims = []
    for trial in range(5):
        t1 = rng.uniform(-np.pi, np.pi, 77); t2 = t1.copy()
        for h in np.linspace(0, 76, kind + 2)[1:-1].round().astype(int): t2[h] = rng.uniform(-np.pi, np.pi)
        dims.append(conic_dim([chain(t1), chain(t2)], [0.37, 0.63])[0])
    print(f"    {kind} torsion{'s' if kind > 1 else ''} different ({kind + 1} rigid segments): dimension {min(dims)} to {max(dims)}")
print("(5) two torsions varied on a 12 x 12 grid, all others fixed: every squared distance lies in the span of {1, cos, sin} x {1, cos, sin} (nine functions)")
for n in (10, 16):
    tors = rng.uniform(-np.pi, np.pi, n - 3); h1, h2 = 1, n - 5; g = np.linspace(0, 2 * np.pi, 12, endpoint=False); rowsD = []; B9 = []; B5 = []
    for p in g:
        for q in g:
            t = tors.copy(); t[h1] = p; t[h2] = q; rowsD.append(D(chain(t)).ravel())
            b1 = [1.0, np.cos(p), np.sin(p)]; b2 = [1.0, np.cos(q), np.sin(q)]
            B9.append([u * v for u in b1 for v in b2]); B5.append([1.0, np.cos(p), np.sin(p), np.cos(q), np.sin(q)])
    rowsD = np.array(rowsD); B9 = np.array(B9); B5 = np.array(B5)
    r9 = np.abs(B9 @ np.linalg.lstsq(B9, rowsD, rcond=None)[0] - rowsD).max(); r5 = np.abs(B5 @ np.linalg.lstsq(B5, rowsD, rcond=None)[0] - rowsD).max()
    rank = np.linalg.matrix_rank(np.linalg.lstsq(B9, rowsD, rcond=None)[0], tol=1e-9)
    print(f"    n = {n}, torsions {h1} and {h2}: residual {r9:.2e}; control without the four product functions: {r5:.2e} (must be large); "
          f"rank of the map from the nine coefficients to M: {rank} (9 = M sees every Fourier coefficient of the pair with both indices in -1, 0, 1)")
print(f"ALL DONE {time.time() - t0:.1f} s")
