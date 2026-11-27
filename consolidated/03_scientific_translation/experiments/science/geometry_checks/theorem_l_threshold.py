#!/usr/bin/env python3
"""Science division, coordinator's check for SCI-REV-0023 (26 Nov 2026).

The Geometry division's Theorem L (their LOCAL_DATA_STABILITY.md at 288b2de, section 3) is quoted here with every clause:

  X: n >= 5 points in R^3;  P_i = [x_{i+1}-x_i, x_{i+2}-x_i, x_{i+3}-x_i]  (1 <= i <= n-3);
  tau = min_i sigma_min(P_i),  D = max_i sigma_max(P_i),  b = max_i |x_{i+1}-x_i|;  eta_jk = |y_j-y_k|^2 - |x_j-x_k|^2.
  "Let tau > 0 and let Y be any configuration of n points in R^3 such that
       (S)  |eta_jk| <= tau^4/(73 D^2)  for all pairs with |j-k| <= 4.
   Then there is an isometry g of R^3 (possibly improper) with
       ||Y - gX||_F <= 6.9 (b/tau^2) n(n+1) ||eta||_2,   ||eta||_2^2 = sum_{|j-k|<=3} eta_jk^2."

Nothing of their proof is checked here.  What is computed (their statement taken as given):

 (1) the necessary limit of ANY threshold in a statement of this form.  Reflect the points beyond x_{i+3} in the plane of
     x_{i+1}, x_{i+2}, x_{i+3}: no distance of separation <= 3 changes (their own remark), exactly one of separation 4
     does, and by a two-line computation
         |x'_{i+4} - x_i|^2 - |x_{i+4} - x_i|^2 = 4 h_i^- h_i^+ ,
     h_i^-, h_i^+ the signed heights of x_i and x_{i+4} over that plane.  For that Y the right-hand side of the theorem
     is 0 and Y is not congruent to X, so a correct pointwise threshold is below  gap = min_i 4|h_i^- h_i^+|,
     and gap >= 4 tau^2/sqrt(3)  (|h^-| >= tau/sqrt(3), |h^+| >= tau).   Both asserted below on every instance.
 (2) the numbers on three geometries in Angstrom: an ideal alpha-helix C-alpha trace, twisted strands, random chains.

Controls that can fail: the flipped configuration must reproduce every distance of separation <= 3 to rounding and must
differ at separation 4 by exactly 4 h^- h^+; its superposition distance to X (over proper AND improper isometries) must
be positive; at twist 180 degrees the strand is planar and tau must vanish.
Run:  python3 -B theorem_l_threshold.py > theorem_l_threshold.log
"""
import numpy as np, resource, sys, time
t0 = time.time()

def helix(n, radius, rise, turn_deg):
    t = np.arange(n) * np.deg2rad(turn_deg)
    return np.c_[radius * np.cos(t), radius * np.sin(t), rise * np.arange(n)]

def windows(X):
    n = len(X); sm, sM = [], []
    for i in range(n - 3):
        P = np.c_[X[i + 1] - X[i], X[i + 2] - X[i], X[i + 3] - X[i]]
        s = np.linalg.svd(P, compute_uv=False); sm.append(s[-1]); sM.append(s[0])
    return np.array(sm), np.array(sM)

def heights(X, i):
    """signed heights of x_i and x_{i+4} over the plane of x_{i+1}, x_{i+2}, x_{i+3}; and the unit normal"""
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm = nrm / np.linalg.norm(nrm)
    return nrm @ (X[i] - X[i + 1]), nrm @ (X[i + 4] - X[i + 1]), nrm

def flip(X, i):
    """reflect the points beyond x_{i+3} in the plane of x_{i+1}, x_{i+2}, x_{i+3}"""
    _, _, nrm = heights(X, i); Y = X.copy()
    for j in range(i + 4, len(X)):
        Y[j] = X[j] - 2 * (nrm @ (X[j] - X[i + 1])) * nrm
    return Y

def dP(X, Y):
    """min over all isometries (proper and improper) of ||Y - gX||_F  (orthogonal Procrustes)"""
    A = X - X.mean(0); B = Y - Y.mean(0)
    s = np.linalg.svd(A.T @ B, compute_uv=False)
    return np.sqrt(max((A * A).sum() + (B * B).sum() - 2 * s.sum(), 0.0))

def eta(X, Y, sep):
    n = len(X); out = []
    for j in range(n):
        for k in range(j + 1, min(n, j + sep + 1)):
            out.append(((Y[j] - Y[k]) ** 2).sum() - ((X[j] - X[k]) ** 2).sum())
    return np.array(out)

def report(name, X, unit="A"):
    n = len(X); sm, sM = windows(X); tau, D = sm.min(), sM.max()
    b = max(np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1))
    d4 = max(np.linalg.norm(X[i + s] - X[i]) for s in (1, 2, 3, 4) for i in range(n - s))
    if tau < 1e-9:
        print(f"{name:34s} n={n:3d}  tau = {tau:.1e}: four consecutive points coplanar -- Theorem L does not apply (control: expected at twist 180)")
        return None
    S = tau ** 4 / (73 * D ** 2)
    gaps = []
    for i in range(n - 4):
        hm, hp, _ = heights(X, i); g = 4 * hm * hp
        Y = flip(X, i)
        e3 = eta(X, Y, 3); e4 = eta(X, Y, 4)
        chg = e4[np.abs(e4) > 1e-9 * D * D]
        assert np.abs(e3).max() < 1e-9 * D * D, "flip changed a distance of separation <= 3"
        assert len(chg) == 1 and abs(chg[0] - g) < 1e-9 * D * D, ("separation-4 change is not 4 h- h+", chg, g)
        assert dP(X, Y) > 1e-6 * tau, "flipped configuration is congruent to X"
        assert abs(hm) >= tau / np.sqrt(3) - 1e-12 and abs(hp) >= tau - 1e-12, "height bounds violated"
        gaps.append(abs(g))
    gap = min(gaps)
    assert gap >= 4 * tau ** 2 / np.sqrt(3) - 1e-12
    c = 6.9 * b / tau ** 2
    # the bound of the theorem when every admitted pair error sits at the threshold: ||eta||_2 = (S) sqrt(#pairs of separation <= 3)
    npairs = sum(1 for j in range(n) for k in range(j + 1, min(n, j + 4)))
    assert npairs == 3 * n - 6
    rmsd_at_S = c * n * (n + 1) * S * np.sqrt(npairs) / np.sqrt(n)
    closed = 6.9 * b * tau ** 2 / (73 * D ** 2) * (n + 1) * np.sqrt(n * (3 * n - 6))
    assert abs(rmsd_at_S - closed) < 1e-9 * closed          # the same number in closed form: 6.9 b tau^2/(73 D^2) (n+1) sqrt(n(3n-6))
    rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)
    print(f"{name:34s} n={n:3d}  b={b:5.2f}  tau={tau:6.3f}  D={D:6.2f}  (S)={S:9.2e} {unit}^2  as a distance error at d={d4:5.2f}: {S/(2*d4):8.1e} {unit} | "
          f"flip gap={gap:7.3f} {unit}^2 (= {gap/(2*d4):6.3f} {unit}), >= 4tau^2/sqrt3={4*tau**2/np.sqrt(3):6.3f} | gap/(S)={gap/S:9.2e}  169(D/tau)^2={169*(D/tau)**2:9.2e} | "
          f"6.9 b/tau^2={c:8.2f}/{unit}; x n(n+1)={c*n*(n+1):9.3e} | RMSD guaranteed when all errors are at (S): {rmsd_at_S:8.2f} {unit} (radius of gyration {rg:6.2f} {unit}); "
          f"fraction of (S) at which the guarantee is 1 {unit}: {min(1.0, 1.0/rmsd_at_S):8.2e}")
    return dict(tau=tau, D=D, S=S, gap=gap, rmsd_at_S=rmsd_at_S, rg=rg, b=b)

print("Theorem L (Geometry division, 288b2de) -- threshold (S), the flip gap that bounds any threshold, and the constant, on physical geometries")
print("lengths in Angstrom for the helices and strands; unit bonds for the random chains\n")
res = {}
for n in (12, 15, 16, 20, 100):
    res[("alpha", n)] = report("alpha-helix CA (r 2.3, rise 1.5, 100 deg)", helix(n, 2.3, 1.5, 100.0))
print()
for tw in (180.0, 175.0, 170.0, 160.0, 150.0):
    res[("strand", tw)] = report(f"strand CA (r 0.94, rise 3.3, {tw:.0f} deg)", helix(20, 0.94, 3.3, tw))
print()
rng = np.random.default_rng(20261126)
worst = []
for trial in range(20):
    # freely jointed chain, unit bonds, bond angles and torsions uniform in a range that avoids near-coplanar windows
    X = [np.zeros(3), np.array([1.0, 0, 0])]
    X.append(X[1] + np.array([np.cos(1.2), np.sin(1.2), 0]))
    for i in range(3, 20):
        a, b_, c_ = X[-3], X[-2], X[-1]
        th = rng.uniform(np.deg2rad(95), np.deg2rad(125)); ph = rng.uniform(np.deg2rad(40), np.deg2rad(140)) * rng.choice([-1, 1])
        bc = (c_ - b_) / np.linalg.norm(c_ - b_); nn = np.cross(b_ - a, bc); nn /= np.linalg.norm(nn); m = np.cross(nn, bc)
        d = np.array([-np.cos(th), np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph)])
        X.append(c_ + d[0] * bc + d[1] * m + d[2] * nn)
    X = np.array(X)
    sm, sM = windows(X)
    worst.append((sm.min() ** 4 / (73 * sM.max() ** 2), trial, X))
worst.sort(key=lambda z: z[0])
for lab, (S, trial, X) in (("random chain, smallest (S) of 20", worst[0]), ("random chain, median (S) of 20", worst[10]), ("random chain, largest (S) of 20", worst[-1])):
    report(lab, X, unit="b")
print()
a = res[("alpha", 20)]
print(f"summary: alpha-helix: (S) = {a['S']:.2e} A^2 against a flip gap of {a['gap']:.2f} A^2: the threshold of the theorem is {a['gap']/a['S']:.1e} times below the limit that the reflections set;")
for n in (12, 15, 16, 20, 100):
    r = res[("alpha", n)]
    print(f"         alpha-helix, n = {n:3d}: with every pair error at the threshold the theorem guarantees an RMSD of {r['rmsd_at_S']:7.2f} A (radius of gyration {r['rg']:5.2f} A); a guarantee of 1 A needs errors of {min(1.0, 1/r['rmsd_at_S']):.1e} of the threshold")
assert res[("alpha", 15)]["rmsd_at_S"] < res[("alpha", 15)]["rg"] and res[("alpha", 16)]["rmsd_at_S"] > res[("alpha", 16)]["rg"]
print("         crossover: the guarantee at the threshold is below the radius of gyration at n = 15 and above it at n = 16 (asserted)")
print("         every assertion (flip leaves separations <= 3 unchanged; changes separation 4 by exactly 4 h- h+; is not congruent; height bounds) held on every window of every instance")
print(f"ALL DONE  {time.time()-t0:.1f} s  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")
