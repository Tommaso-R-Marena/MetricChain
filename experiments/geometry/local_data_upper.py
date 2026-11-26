"""Theorems L, L+ and K(c) of docs/geometry/LOCAL_DATA_STABILITY.md, checked on instances.

Theorem L (global upper bound, no threshold).  X: n points in R^3; for windows of K and K + 1
consecutive points (K = 4: tetrahedra W_i and five-point windows F_i) let tau_i, s_i be the
third singular values of the centred windows.  For EVERY configuration Y there is an isometry
g with, for each point k,

    |y_k - g x_k|  <=  delta_i(k) + sum_{j < i(k)} (delta_j + delta_{j+1}) ( |x_k - c_{j+1}| / tau_{j+1} + 1/sqrt(K) ),
    delta_j = kappa e_j / s_j,   kappa = 1 / (2 sqrt(sqrt 2 - 1)) < 0.777,

e_j the l2 norm of the errors of the squared distances inside F_j, c_{j+1} the centroid of the
K points shared by F_j and F_{j+1}.  For K = 4 this gives

    || Y - g X ||_F  <=  1.2 (b / (s_* tau_*)) (n + 2)^2 || eta ||_2,     eta over all pairs of separation <= 4.

Theorem L+ (sharp constant for small errors).  With A the matrix of rows (x_j - x_k)^T (e_j - e_k)
over the measured pairs, mu its smallest non-zero singular value, Lambda the largest Laplacian
eigenvalue of the band graph and C_L the constant of Theorem L: if ||eta||_2 <= mu / (Lambda C_L)
then  d_P(X, Y) <= ||eta||_2 / (mu + sqrt(mu^2 - Lambda ||eta||_2))   (-> ||eta||_2 / (2 mu), the
first-order constant).

Proposition L0 (the form of the eighth checkpoint, with the threshold (S)) is kept as
theorem_L0_sides.

Theorem K(c) (lower bound in a tube).  If the points lie within distance rho of the z-axis with
axial coordinates z_i = (i - 1/2) h, then for every set F of pairs
    s_7(R)^2 <= 196 pi^4 rho^2 sum_F |x_j - x_k|^2 / (n L^4),   L = n h.

Usage: python3 local_data_upper.py [seed]
"""
import sys
import numpy as np
from geomlib import chain
from local_data_bounds import rigidity_matrix


def windows(X):
    return [np.column_stack([X[i + 1] - X[i], X[i + 2] - X[i], X[i + 3] - X[i]]) for i in range(len(X) - 3)]


def thickness(X):
    sv = [np.linalg.svd(P, compute_uv=False) for P in windows(X)]
    return min(s[-1] for s in sv), max(s[0] for s in sv)


def sqd(X, sep):
    n = len(X)
    return {(j, k): float(((X[j] - X[k]) ** 2).sum()) for j in range(n) for k in range(j + 1, min(n, j + sep + 1))}


def d_procrustes(X, Y):
    """min over isometries (reflections allowed) of ||Y - gX||_F.  The residual is formed
    explicitly: the closed form ||A||^2 + ||B||^2 - 2 sum(sigma) cancels catastrophically for
    displacements below about 1e-7 of the size."""
    A, B = X - X.mean(0), Y - Y.mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    return float(np.linalg.norm(B - A @ (U @ Vt)))


def theorem_L0_sides(X, Y):
    n = len(X)
    tau, D = thickness(X)
    b = max(np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1))
    dX4, dY4 = sqd(X, 4), sqd(Y, 4)
    S = max(abs(dY4[p] - dX4[p]) for p in dX4) <= tau ** 4 / (73 * D ** 2)
    eta = np.sqrt(sum((dY4[p] - dX4[p]) ** 2 for p in dX4 if p[1] - p[0] <= 3))
    left = d_procrustes(X, Y)
    right = 6.9 * b / tau ** 2 * n * (n + 1) * eta
    return S, left, right, tau, D


KAPPA = 1.0 / (2.0 * np.sqrt(np.sqrt(2.0) - 1.0))          # constant of Lemma Q: 0.7769...


def csig3(P):
    """Third singular value of a centred point set (rows are points)."""
    return float(np.linalg.svd(P - P.mean(0), compute_uv=False)[-1])


def band_pairs(n, K=4):
    return [(j, k) for j in range(n) for k in range(j + 1, min(n, j + K + 1))]


def sq_errors(X, Y, pairs):
    return np.array([((Y[j] - Y[k]) ** 2).sum() - ((X[j] - X[k]) ** 2).sum() for j, k in pairs])


def best_fit(Xw, Yw):
    """R in O(3) and t minimising ||Yw - Xw R - t||_F (rows are points); returns R, t, residual."""
    A, B = Xw - Xw.mean(0), Yw - Yw.mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    R = U @ Vt
    t = Yw.mean(0) - Xw.mean(0) @ R
    return R, t, float(np.linalg.norm(Yw - Xw @ R - t))


def theorem_L_bounds(X, Y, K=4, kappa=KAPPA, sep_in_eta=None, check_steps=False):
    """Both sides of Theorem L for an arbitrary Y.  Returns a dict with
    left (Procrustes distance), right_local (the per-point bound of the proof, summed),
    right (the uniform bound, K = 4 only), viol (violated steps of the proof, if checked)."""
    n = len(X)
    sep_in_eta = K if sep_in_eta is None else sep_in_eta
    b = max(np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1))
    F = [list(range(i, i + K + 1)) for i in range(n - K)]
    s = np.array([csig3(X[f]) for f in F])
    tau = np.array([csig3(X[i:i + K]) for i in range(n - K + 1)])
    pair_err = {p: v for p, v in zip(band_pairs(n, K), sq_errors(X, Y, band_pairs(n, K)))}
    if sep_in_eta < K:                                   # planted error: forget the longest separation
        pair_err = {p: (v if p[1] - p[0] <= sep_in_eta else 0.0) for p, v in pair_err.items()}
    e = np.array([np.sqrt(sum(pair_err[(f[a], f[c])] ** 2 for a in range(K + 1) for c in range(a + 1, K + 1)))
                  for f in F])
    eta = float(np.sqrt(sum(v ** 2 for v in pair_err.values())))
    delta = kappa * e / s
    a = delta[:-1] + delta[1:]
    cents = [X[j + 1:j + 1 + K].mean(0) for j in range(n - K - 1)]
    tau_sh = tau[1:n - K]
    loc2 = 0.0
    for k in range(n):
        i = min(k, n - K - 1)
        tot = delta[i]
        for j in range(i):
            tot += a[j] * (np.linalg.norm(X[k] - cents[j]) / tau_sh[j] + 1.0 / np.sqrt(K))
        loc2 += tot ** 2
    out = {"left": d_procrustes(X, Y), "right_local": float(np.sqrt(loc2)), "eta": eta,
           "s": float(s.min()), "tau": float(tau.min()), "b": float(b), "viol": []}
    out["right"] = 1.2 * b / (s.min() * tau.min()) * (n + 2) ** 2 * eta if K == 4 else None
    if check_steps:
        fits = [best_fit(X[f], Y[f]) for f in F]
        tol = lambda x: x * (1 + 1e-9) + 1e-12
        for i, (_, _, res) in enumerate(fits):
            if res > tol(delta[i]):
                out["viol"].append(("window", i, res, float(delta[i])))
        for i in range(n - K - 1):
            rho = float(np.linalg.norm(fits[i][0] - fits[i + 1][0]))
            if rho > tol(a[i] / tau_sh[i]):
                out["viol"].append(("frames", i, rho, float(a[i] / tau_sh[i])))
        R1, t1, _ = fits[0]
        direct = float(np.linalg.norm(Y - X @ R1 - t1))
        if direct > tol(out["right_local"]):
            out["viol"].append(("telescope", direct, out["right_local"]))
    return out


def sq_rigidity(X, pairs):
    """Half the Jacobian of X -> (|x_j - x_k|^2): rows (x_j - x_k)^T (e_j - e_k)."""
    n = len(X)
    A = np.zeros((len(pairs), 3 * n))
    for r, (j, k) in enumerate(pairs):
        d = X[j] - X[k]
        A[r, 3 * j:3 * j + 3] = d
        A[r, 3 * k:3 * k + 3] = -d
    return A


def laplacian_max(n, pairs):
    L = np.zeros((n, n))
    for j, k in pairs:
        L[j, j] += 1
        L[k, k] += 1
        L[j, k] -= 1
        L[k, j] -= 1
    return float(np.linalg.eigvalsh(L)[-1])


def sharp_constants(X, K=4):
    """mu (smallest non-zero singular value of sq_rigidity), Lambda, and the constant C_L of
    Theorem L (uniform form, K = 4)."""
    n = len(X)
    pairs = band_pairs(n, K)
    mu = float(np.linalg.svd(sq_rigidity(X, pairs), compute_uv=False)[3 * n - 7])
    Lam = laplacian_max(n, pairs)
    b = max(np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1))
    s = min(csig3(X[i:i + K + 1]) for i in range(n - K))
    tau = min(csig3(X[i:i + K]) for i in range(n - K + 1))
    return mu, Lam, 1.2 * b * (n + 2) ** 2 / (s * tau)


def theorem_Lplus_bound(mu, Lam, CL, eta, quadratic=True):
    """The bound of Theorem L+ on d_P, or None outside its range ||eta|| <= mu / (Lam CL).
    quadratic=False is a planted error (the first-order constant used for finite errors)."""
    if eta > mu / (Lam * CL):
        return None
    if not quadratic:
        return eta / (2 * mu)
    if eta <= mu ** 2 / Lam:
        return eta / (mu + np.sqrt(mu ** 2 - Lam * eta))
    return eta / mu


def thick_chain(n, rng, theta=np.deg2rad(111.0), lo=0.7, hi=2.4):
    """Random torsions bounded away from 0 and pi, so that all windows are thick."""
    t = rng.uniform(lo, hi, n - 3) * rng.choice([-1, 1], n - 3)
    return chain(n, t, theta=theta), t


def helix(n, tors, theta=np.deg2rad(111.0)):
    return chain(n, np.full(n - 3, tors), theta=theta)


def softest_mode(X, K=4):
    n = len(X)
    edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
    R = rigidity_matrix(X, edges)
    _, s, Vt = np.linalg.svd(R)
    return Vt[-7].reshape(n, 3), s[-7]


def helix_axis_frame(X):
    """Axis direction, radius and rise of an exact helix (from three consecutive bonds)."""
    b = np.diff(X, axis=0)
    ax = np.cross(b[1] - b[0], b[2] - b[1])
    ax /= np.linalg.norm(ax)
    h = float(b[0] @ ax)
    if h < 0:
        ax, h = -ax, -h
    # centre of the axis: least squares on the projections orthogonal to ax
    Pp = X - np.outer(X @ ax, ax)
    A = np.column_stack([2 * Pp, np.ones(len(X))])
    sol = np.linalg.lstsq(A, (Pp ** 2).sum(1), rcond=None)[0]
    c = sol[:3] - (sol[:3] @ ax) * ax
    rho = float(np.sqrt(np.mean(((Pp - c) ** 2).sum(1))))
    spread = float(np.std(np.sqrt(((Pp - c) ** 2).sum(1))))
    return ax, h, rho, spread


def competitor(X, kind, rng):
    """An arbitrary configuration Y to be compared with X: 0 noise of any size, 1 softest mode,
    2 the tail reflected in the plane of three consecutive points, 3 an unrelated chain,
    4 random points, 5 the mirror image with noise, 6 a rotation of the head about an axis
    through two points of the chain."""
    n = len(X)
    if kind == 0:
        return X + rng.normal(size=X.shape) * 10 ** rng.uniform(-8, 0.5)
    if kind == 1:
        V, _ = softest_mode(X)
        return X + V / np.abs(V).max() * 10 ** rng.uniform(-6, 1)
    if kind == 2:
        i = int(rng.integers(1, n - 3))
        nrm = np.cross(X[i + 1] - X[i], X[i + 2] - X[i])
        nrm /= np.linalg.norm(nrm)
        Y = X.copy()
        Y[i + 3:] = X[i + 3:] - 2 * np.outer((X[i + 3:] - X[i]) @ nrm, nrm)
        return Y
    if kind == 3:
        return thick_chain(n, rng)[0]
    if kind == 4:
        return rng.normal(size=X.shape) * rng.uniform(0.1, 10)
    if kind == 5:
        return X * np.array([1, 1, -1]) + rng.normal(size=X.shape) * 1e-3
    i = int(rng.integers(1, n - 3))
    ax = X[i + 2] - X[i]
    ax /= np.linalg.norm(ax)
    th = rng.uniform(-3, 3)
    Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    Rm = np.eye(3) + np.sin(th) * Kx + (1 - np.cos(th)) * Kx @ Kx
    Y = X.copy()
    Y[:i] = (X[:i] - X[i]) @ Rm.T + X[i]
    return Y


def procrustes_gram_ratio(rng, trials=20000):
    """Lemma P: the largest ratio dist^2(U, X) / ( ||UU^T - XX^T||_F^2 / (2 (sqrt 2 - 1) sigma_r(X)^2) )."""
    worst = 0.0
    for _ in range(trials):
        r, m = 3, int(rng.integers(3, 9))
        X = rng.normal(size=(m, r)) * rng.uniform(0.1, 3, size=r)
        kind = rng.integers(0, 4)
        if kind == 0:
            U = rng.normal(size=(m, r)) * rng.uniform(0.01, 5)
        elif kind == 1:
            U = X @ np.linalg.qr(rng.normal(size=(r, r)))[0] + rng.normal(size=(m, r)) * 10 ** rng.uniform(-6, 0)
        elif kind == 2:
            U = X.copy()
            U[:, rng.integers(0, r)] *= rng.uniform(-2, 2)
        else:
            U = X * rng.uniform(0, 3)
        sig = np.linalg.svd(X, compute_uv=False)[-1]
        d2 = max(0.0, (X ** 2).sum() + (U ** 2).sum() - 2 * np.linalg.svd(X.T @ U, compute_uv=False).sum())
        rhs = np.linalg.norm(U @ U.T - X @ X.T) ** 2 / (2 * (np.sqrt(2) - 1) * sig ** 2)
        if rhs > 0:
            worst = max(worst, d2 / rhs)
    return worst


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    rng = np.random.default_rng(seed)
    ok = True

    w = procrustes_gram_ratio(rng)
    print(f"(0) Lemma P (Procrustes-Gram inequality) on 20000 pairs: largest dist^2 / bound = {w:.3f} (must be <= 1)")
    ok &= w <= 1.0

    print("(1) Theorem L for ARBITRARY Y (noise of any size, soft modes, reflected tails, unrelated chains, random points, mirror images, rotated heads):")
    for K, trials in ((4, 420), (5, 105), (6, 105), (7, 105)):
        nviol, wl, wg, tot = 0, 0.0, 0.0, 0
        for trial in range(trials):
            n = int(rng.integers(K + 2, 60))
            X = helix(n, rng.choice([1.0, 1.3, 2.0, -1.7])) if trial % 3 == 0 else thick_chain(n, rng)[0]
            Y = competitor(X, trial % 7, rng)
            r = theorem_L_bounds(X, Y, K=K, check_steps=True)
            tot += 1
            bad = bool(r["viol"]) or r["left"] > r["right_local"] * (1 + 1e-9) + 1e-12
            if K == 4:
                bad |= r["right_local"] > r["right"] * (1 + 1e-9) + 1e-12
                wg = max(wg, r["left"] / r["right"] if r["right"] > 0 else 0.0)
            nviol += bad
            wl = max(wl, r["left"] / r["right_local"] if r["right_local"] > 0 else 0.0)
        extra = f", left/uniform bound = {wg:.4f}" if K == 4 else ""
        print(f"    separation <= {K}: {tot} pairs, violated steps or bounds: {nviol}; largest left/local bound = {wl:.3f}{extra}")
        ok &= nviol == 0

    print("(2) Theorem L+ (sharp constant) inside its range ||eta|| <= mu / (Lambda C_L):")
    worst, closest, used = 0.0, 0.0, 0
    for trial in range(60):
        n = int(rng.integers(8, 40))
        X = helix(n, rng.choice([1.0, 1.3, 2.0])) if trial % 2 == 0 else thick_chain(n, rng)[0]
        mu, Lam, CL = sharp_constants(X)
        V = softest_mode(X)[0] if trial % 3 else rng.normal(size=X.shape)
        V = V / np.linalg.norm(V)
        for frac in (0.9, 0.3, 0.01):
            # amplitude chosen so that ||eta|| is the given fraction of the range
            amp = frac * mu / (Lam * CL) / (2 * np.linalg.norm(sq_rigidity(X, band_pairs(n)) @ V.ravel()))
            for sign in (1, -1):
                Y = X + sign * amp * V
                eta = float(np.linalg.norm(sq_errors(X, Y, band_pairs(n))))
                bound = theorem_Lplus_bound(mu, Lam, CL, eta)
                if bound is None:
                    continue
                used += 1
                dP = d_procrustes(X, Y)
                worst = max(worst, dP / bound)
                closest = max(closest, dP / (eta / (2 * mu)))
    print(f"    {used} pairs: largest d_P / bound = {worst:.6f} (must be <= 1); largest d_P / (||eta|| / 2 mu) = {closest:.6f} "
          f"(1 = the first-order constant is attained)")
    ok &= worst <= 1.0 and used > 100

    print("(3) Proposition L0 (the earlier form with the threshold (S)) on perturbations:")

    worst, used, skipped = 0.0, 0, 0
    best_tight = 0.0
    for trial in range(120):
        n = int(rng.integers(10, 90))
        if trial % 3 == 0:
            X = helix(n, rng.choice([1.0, 1.3, 2.0, -1.7]))
        else:
            X, _ = thick_chain(n, rng)
        tau, D = thickness(X)
        kind = trial % 4
        scale = tau ** 4 / (73 * D ** 2)
        if kind == 0:                                   # random displacement of every point
            V = rng.normal(size=X.shape)
        elif kind == 1:                                 # softest mode of the local rigidity matrix
            V, _ = softest_mode(X)
        elif kind == 2:                                 # smooth bending field
            z = np.linspace(0, 1, n)
            V = np.column_stack([np.cos(np.pi * z), np.sin(2 * np.pi * z), 0 * z]) @ np.linalg.qr(rng.normal(size=(3, 3)))[0]
        else:                                           # change of the torsions (stays a chain)
            V = None
        for amp in (1.0, 0.3, 0.05):
            if V is None:
                Xc, t = thick_chain(n, rng)
                X = Xc
                tau, D = thickness(X)
                scale = tau ** 4 / (73 * D ** 2)
                Y = chain(n, t + amp * scale * 0.2 * rng.normal(size=n - 3) / np.sqrt(n))
            else:
                Y = X + amp * scale * 0.05 * V / np.abs(V).max()
            S, left, right, tau, D = theorem_L0_sides(X, Y)
            if not S:
                skipped += 1
                continue
            used += 1
            worst = max(worst, left / right if right > 0 else 0.0)
            if kind == 1:
                best_tight = max(best_tight, left / right)
    print(f"    {used} pairs (X, Y) satisfying (S) ({skipped} skipped): largest left/right = {worst:.4f} (must be <= 1); "
          f"along softest modes the bound is attained up to the factor {1 / best_tight:.0f}")
    ok &= worst <= 1.0 and used > 100

    print("(4) why separation 4 is needed: reflecting the tail of a chain in the plane of three consecutive atoms")
    X, t = thick_chain(30, rng)
    i = 12
    p0, u, v = X[i + 1], X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]
    nrm = np.cross(u, v)
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * np.outer((X[i + 4:] - p0) @ nrm, nrm)
    S, left, right, tau, D = theorem_L0_sides(X, Y)
    dX3, dY3 = sqd(X, 3), sqd(Y, 3)
    e3 = max(abs(dY3[p] - dX3[p]) for p in dX3)
    dX4, dY4 = sqd(X, 4), sqd(Y, 4)
    e4 = max(abs(dY4[p] - dX4[p]) for p in dX4)
    print(f"    separation <= 3 data unchanged (max |d^2 difference| = {e3:.1e}), separation-4 data change by {e4:.3f} "
          f"> tau^4/(73 D^2) = {tau**4/(73*D**2):.1e}; (S) holds: {S}; d_P(X, Y) = {left:.2f}")
    r = theorem_L_bounds(X, Y, check_steps=True)
    print(f"    Theorem L for this Y: d_P = {r['left']:.2f} <= local bound {r['right_local']:.1f} <= uniform bound {r['right']:.0f} "
          f"(the one changed distance of separation 4 pays for the whole displacement)")
    ok &= (not S) and e3 < 1e-9 and left > 0.5 and not r["viol"] and r["left"] <= r["right_local"]

    print("(5) tube bound on helices (all pairs of sequence separation <= K):")
    for tors, K in ((np.deg2rad(60.0), 4), (np.deg2rad(150.0), 4), (np.deg2rad(60.0), 6)):
        rows = []
        for n in (40, 80, 160):
            X = helix(n, tors)
            ax, h, rho, spread = helix_axis_frame(X)
            edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
            R = rigidity_matrix(X, edges)
            s7 = np.sort(np.linalg.svd(R, compute_uv=False))[6]
            L = n * h
            sumsq = sum(((X[i] - X[j]) ** 2).sum() for i, j in edges)
            bound = np.sqrt(196 * np.pi ** 4 * rho ** 2 * sumsq / (n * L ** 4))
            rows.append((n, s7, bound, spread))
            ok &= s7 <= bound and spread < 1e-8
        tau, D = thickness(helix(40, tors))
        txt = ", ".join(f"n = {n}: s_7 = {s7:.2e} <= {bd:.2e}" for n, s7, bd, _ in rows)
        print(f"    torsion {np.rad2deg(tors):.0f} deg, K = {K}: rise h = {h:.3f}, radius rho = {rho:.3f}, tau = {tau:.3f}, D = {D:.3f}; {txt}; "
              f"n^2 s_7 = {rows[-1][1] * rows[-1][0] ** 2:.1f}, n^2 bound = {rows[-1][2] * rows[-1][0] ** 2:.0f}")
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
