"""Independent check of two formulas of the Geometric Inference Division's GEOMETRY-RES-0002
(branch research/geometric-inference, commit e8e2582; Findings 1 and 3: rod model, small angles).

Finding 1: a straight uniform rod of length L, kinked by a small angle phi at position s, has
after optimal rigid superposition the squared distance
        D^2 = phi^2 s^3 (L-s)^3 / (3 L^3).
Finding 3: for several small kinks phi_k at s_k (all about the same perpendicular axis) the
squared distance is sum_{k,l} phi_k phi_l G(s_k, s_l) with
        G(s, s') = s^2 (L-s')^2 (3 L s' - L s - 2 s s') / (6 L^3)   (s <= s').

Written from the statements alone (own code: a discretised rod, Kabsch superposition by SVD).
Nothing here is a proof; the output is the ratio of the computed squared distance to the formula.
"""
import numpy as np

def kabsch_sq(X, Y):
    """min over proper rigid motions of sum |R x_i + t - y_i|^2 (uniform weights)."""
    Xc = X - X.mean(0); Yc = Y - Y.mean(0)
    H = Xc.T @ Yc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    S2 = S.copy(); S2[-1] *= d
    return (Xc**2).sum() + (Yc**2).sum() - 2 * S2.sum()

def rod(N, kinks):
    """N+1 points with spacing 1/N on [0,1]; kinks = [(s, phi)]: rotation of the part beyond s
    by phi about the z axis through the point at s (perpendicular to the rod)."""
    t = np.linspace(0.0, 1.0, N + 1)
    P = np.stack([t, 0 * t, 0 * t], 1)
    for s, phi in sorted(kinks):
        c, sn = np.cos(phi), np.sin(phi)
        R = np.array([[c, -sn, 0], [sn, c, 0], [0, 0, 1.0]])
        # the joint has been moved by earlier kinks: find its current position
        i0 = int(round(s * N))
        piv = P[i0].copy()
        P[i0 + 1:] = (P[i0 + 1:] - piv) @ R.T + piv
    return P

def G(s, sp, L=1.0):
    if s > sp:
        s, sp = sp, s
    return s**2 * (L - sp)**2 * (3 * L * sp - L * s - 2 * s * sp) / (6 * L**3)

ok = True
print("Finding 1: one kink; ratio of N * (Kabsch squared distance) / (phi^2 s^3 (1-s)^3 / 3)")
print("  (a rod of N + 1 points: the discretisation error is of order 1/N; the criterion is")
print("   that N * (ratio - 1) is the same at N = 1000 and N = 4000 to 10 per cent, i.e. limit 1)")
rows = {}
for N in (200, 1000, 4000):
    row = []
    for s in (0.1, 0.25, 0.5, 0.8):
        phi = 1e-4
        X = rod(N, []); Y = rod(N, [(s, phi)])
        d2 = kabsch_sq(X, Y) / N          # Riemann sum -> integral over the rod
        f = phi**2 * s**3 * (1 - s)**3 / 3
        row.append(d2 / f)
    rows[N] = row
    print(f"  N = {N:5d}: " + "  ".join(f"{r:.5f}" for r in row)
          + "    N*(ratio-1): " + "  ".join(f"{N * (r - 1):6.2f}" for r in row))
ok &= all(abs(r - 1) < 5e-3 for r in rows[4000])
ok &= all(abs(4000 * (b - 1) / (1000 * (a - 1)) - 1) < 0.1 for a, b in zip(rows[1000], rows[4000]))
print("  consistency with G: G(s,s) / (s^3 (1-s)^3 / 3) =",
      [round(G(s, s) / (s**3 * (1 - s)**3 / 3), 12) for s in (0.1, 0.25, 0.5, 0.8)])
ok &= all(abs(G(s, s) / (s**3 * (1 - s)**3 / 3) - 1) < 1e-12 for s in (0.1, 0.25, 0.5, 0.8))

print("Finding 3: several kinks; ratio of N * (Kabsch squared distance) / sum phi_k phi_l G(s_k, s_l)")
rng = np.random.default_rng(7)
N = 4000
worst = 0.0
for trial in range(12):
    m = int(rng.integers(2, 5))
    ss = np.sort(rng.choice(np.arange(1, 20), size=m, replace=False)) / 20.0
    ph = rng.uniform(-1, 1, size=m) * 1e-4
    X = rod(N, []); Y = rod(N, list(zip(ss, ph)))
    d2 = kabsch_sq(X, Y) / N
    q = sum(ph[k] * ph[l] * G(ss[k], ss[l]) for k in range(m) for l in range(m))
    worst = max(worst, abs(d2 / q - 1))
    if trial < 4:
        print(f"  kinks at {ss.tolist()}: ratio {d2 / q:.5f}")
print(f"  largest |ratio - 1| over 12 random sets of 2-4 kinks: {worst:.2e}")
ok &= worst < 5e-3
# the middle kink against the coaxial cost I_red phi^2 (their 'a quarter'):
s = 0.5; Ired = (s**3 / 3) * ((1 - s)**3 / 3) / (s**3 / 3 + (1 - s)**3 / 3)
print(f"at the middle: (s^3 (1-s)^3 / 3) / I_red = {(s**3 * (1 - s)**3 / 3) / Ired:.4f}   (their statement: a quarter)")
ok &= abs((s**3 * (1 - s)**3 / 3) / Ired - 0.25) < 1e-12
print("ALL CHECKS PASS" if ok else "A CHECK FAILED")
