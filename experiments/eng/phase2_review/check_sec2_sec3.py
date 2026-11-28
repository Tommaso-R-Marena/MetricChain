"""Review checks for sections 2 and 3 of CERTIFIED_INFERENCE.md.

Proposition 2.1 (support function), Theorems 2.2 and 3.1 (simulated Hausdorff deviations against both
bounds, exact d_H in dimension 2-4), Proposition 2.3 (adversarial search), Corollary 2.4 (non-convex
region), Proposition 2.5 and the sentence after it (excess width).

Run:  python check_sec2_sec3.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

import ref

rng = np.random.default_rng(20261128)


def random_instance(N, m, rng, gamma=None, zero_l=False, degenerate=0.0):
    u = rng.uniform(0.2, 1.0, N)
    if zero_l:
        l = np.zeros(N)
    elif gamma is not None:
        l = u / gamma
    else:
        l = u * rng.uniform(0.05, 1.0, N)
    if degenerate > 0:
        mask = rng.random(N) < degenerate
        l = np.where(mask, u, l)
    phi = rng.uniform(-1, 1, (N, m))
    f = rng.uniform(-1, 1, N)
    return l, u, phi, f


def check_prop21():
    worst = 0.0
    for _ in range(200):
        N = int(rng.integers(3, 9))
        m = int(rng.integers(0, 3))
        l, u, phi, f = random_instance(N, m, rng, degenerate=0.3)
        V = np.column_stack([np.ones(N), phi, f])
        lam = rng.normal(size=V.shape[1])
        proj = V @ lam
        formula = float(np.sum(u * np.maximum(proj, 0) - l * np.maximum(-proj, 0)))
        res = linprog(-proj, bounds=list(zip(l, u)), method="highs")
        worst = max(worst, abs(-res.fun - formula))
    print(f"[2.1] support function formula vs LP over weights: max abs diff = {worst:.2e}")


def check_concentration():
    print("[2.2/3.1] simulated d_H/G against the two bounds (exact d_H by arrangement vertices)")
    print("   d   N     L  delta   q95(or q80) sim   eps_S3(L)   eps_3.1(L)  max sim/eps_3.1  viol_S3 viol_3.1")
    for d, N, Ls in ((2, 10, (20, 200, 2000)), (3, 10, (20, 200, 2000)), (4, 8, (50, 500))):
        for kind in ("random", "signs"):
            m = d - 2
            if kind == "random":
                phi = rng.uniform(-1, 1, (N, m))
                f = rng.uniform(-1, 1, N)
                q = rng.dirichlet(np.ones(N))
            else:
                # generators at the corners of the cube: the hardest case for an l_inf deviation
                phi = rng.choice([-1.0, 1.0], size=(N, m))
                f = rng.choice([-1.0, 1.0], size=N)
                q = np.ones(N) / N
            V = np.column_stack([np.ones(N), phi, f])
            for L in Ls:
                for delta in (0.05,):
                    reps = 1500 if d < 4 else 400
                    devs = np.empty(reps)
                    for r in range(reps):
                        counts = rng.multinomial(L, q)
                        devs[r] = ref.hausdorff_linf_over_G(V, q, counts)
                    e_s3 = ref.s3_eps_from_L(L, d, delta)
                    e_31 = ref.thm31_eps_from_L(L, d, delta)
                    print(f"   {d}  {N:2d}  {L:5d}  {delta:.2f}  {kind:6s} {np.quantile(devs, 1 - delta):.4f}"
                          f"      {e_s3:.4f}      {e_31:.4f}      {devs.max() / e_31:.3f}"
                          f"          {np.mean(devs > e_s3):.4f}  {np.mean(devs > e_31):.4f}")


def compare_bounds():
    print("[3.1 vs 2.2] sample sizes required for d_H <= eps*G, delta = 0.05  (ratio = L_3.1 / L_S3)")
    print("   d      eps      L_S3        L_3.1     ratio")
    worse = []
    for d in (2, 3, 4, 6, 12, 52, 1002):
        for eps in (2.0, 1.0, 0.5, 0.3, 0.1, 0.01, 0.001):
            a = ref.s3_L(eps, d, 0.05)
            b = ref.thm31_L(eps, d, 0.05)
            if b > a:
                worse.append((d, eps, a, b))
            print(f"   {d:5d}  {eps:6.3f}  {a:12.1f}  {b:12.1f}  {b / a:6.3f}")
    print(f"   cases where Theorem 3.1 needs MORE draws than S3: {[(d, e) for d, e, _, _ in worse]}")
    # crossing point in eps for small d
    for d in (2, 3, 4, 5, 6):
        lo, hi = 1e-6, 10.0
        f = lambda e: ref.thm31_L(e, d, 0.05) - ref.s3_L(e, d, 0.05)
        if f(lo) * f(hi) > 0:
            print(f"   d={d}: no crossing in [1e-6, 10]  (sign {np.sign(f(lo))})")
            continue
        for _ in range(100):
            mid = np.sqrt(lo * hi)
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        print(f"   d={d}: Theorem 3.1 is better only for eps < {hi:.4f}")


def check_prop23():
    """Adversarial random search: max |M_i/M_0 - Mh_i/Mh_0| / kappa over pairs within eps*G in l_inf."""
    worst = 0.0
    for _ in range(300):
        N = int(rng.integers(3, 8))
        m = int(rng.integers(0, 3))
        l, u, phi, f = random_instance(N, m, rng, degenerate=0.2)
        V = np.column_stack([np.ones(N), phi, f])
        G = (u - l).sum()
        Zl = l.sum()
        if G <= 0 or Zl <= 0:
            continue
        q = (u - l) / G
        L = int(rng.integers(2, 12))
        counts = rng.multinomial(L, q)
        uh = l + G * counts / L
        eps = float(rng.uniform(0.01, 0.5))
        kappa = 2 * eps * G / Zl
        for _ in range(60):
            # extreme points are the adversarial choices
            w = np.where(rng.random(N) < 0.5, l, u)
            wh = np.where(rng.random(N) < 0.5, l, uh)
            M = V.T @ w
            Mh = V.T @ wh
            if np.max(np.abs(M - Mh)) <= eps * G:
                dev = np.max(np.abs(M[1:] / M[0] - Mh[1:] / Mh[0]))
                worst = max(worst, dev / kappa)
    print(f"[2.3] max over random extreme pairs of |ratio diff| / kappa = {worst:.3f}  (must be <= 1)")
    # tightness: l tiny mass on a state with v = (1, 1); gap mass on a state with v = (1, -1)
    # M = b + G t (1,-1), Mh = b + G th (1,-1): ratio diff ~ 2 G |t - th| / Zl for small G/Zl
    Zl, G, eps = 1.0, 1e-3, 0.5
    t, th = 0.0, eps
    M = np.array([Zl + G * t, Zl - G * t])
    Mh = np.array([Zl + G * th, Zl - G * th])
    dev = abs(M[1] / M[0] - Mh[1] / Mh[0])
    print(f"[2.3] tightness example: |ratio diff| / kappa = {dev / (2 * eps * G / Zl):.4f}  (-> 1: the constant 2 is sharp)")


def check_cor24_nonconvex():
    """Non-convex region R = R1 u R2 (m = 1).  K_hat is the moment body of the box class (l, l + G counts/L)."""
    viol = 0
    cases = 0
    empties = 0
    min_slack = np.inf
    for _ in range(400):
        N = int(rng.integers(4, 9))
        l, u, phi, f = random_instance(N, 1, rng, gamma=float(rng.uniform(1.5, 8)))
        V = np.column_stack([np.ones(N), phi, f])
        G = (u - l).sum()
        Zl = l.sum()
        q = (u - l) / G
        L = int(rng.integers(3, 40))
        counts = rng.multinomial(L, q)
        uh = l + G * counts / L
        dH = ref.hausdorff_linf_over_G(V, q, counts) * G
        kappa = 2 * dH / Zl
        # two pieces placed around the reachable range of E phi
        lo_y = ref.primal_extreme(l, u, phi, phi[:, 0], None, None, -1)
        hi_y = ref.primal_extreme(l, u, phi, phi[:, 0], None, None, +1)
        a = np.sort(rng.uniform(lo_y - 0.2, hi_y + 0.2, 4))
        pieces = [(a[0], a[1]), (a[2], a[3])]
        for (ya, yb) in pieces:
            A, c = ref.box_region([ya], [yb])
            I = ref.primal_interval(l, u, phi, f, A, c)
            A2, c2 = ref.box_region([ya - kappa], [yb + kappa])
            Ih = ref.primal_interval(l, uh, phi, f, A2, c2)
            cases += 1
            if Ih is None:
                empties += 1
                if I is not None:
                    viol += 1
                continue
            if I is None:
                continue
            slack = min(Ih[1] + kappa - I[1], I[0] - (Ih[0] - kappa))
            min_slack = min(min_slack, slack / kappa if kappa > 0 else np.inf)
            if slack < -1e-9:
                viol += 1
    print(f"[2.4] non-convex region, kappa from the realised d_H: {cases} pieces, "
          f"{empties} with empty sampled set, violations = {viol}, min slack/kappa = {min_slack:.3f}")


def check_prop25_and_excess():
    # (i) the inequality of Proposition 2.5
    worst = -np.inf
    for _ in range(200):
        N = int(rng.integers(4, 9))
        m = int(rng.integers(1, 3))
        l, u, phi, f = random_instance(N, m, rng)
        p0 = rng.uniform(l, u)
        y = (p0 @ phi) / p0.sum()
        half = rng.uniform(0.01, 0.1, m)
        ylo, yhi = y - half, y + half
        tau, eta = ref.dual_upper_lp_box(l, u, phi, f, ylo, yhi)
        kappa = float(rng.uniform(0.001, 0.2))
        A, c = ref.box_region(ylo - kappa, yhi + kappa)
        v = ref.primal_extreme(l, u, phi, f, A, c, +1)
        worst = max(worst, v - (tau + kappa * np.abs(eta).sum()))
    print(f"[2.5] max of sup I(R + kappa B) - (tau + kappa |eta|_1) over 200 instances = {worst:.2e} (must be <= 0)")

    # (ii) an explicit instance where the excess of the ENLARGED EXACT problem is >> kappa
    # X = {0,1,2}; f = (0, 1, 1); phi = eps' * f  ->  E f = E phi / eps'
    for epsp in (0.1, 0.01):
        l = np.array([1.0, 1.0, 1.0])
        u = 4 * l
        f = np.array([0.0, 1.0, 1.0])
        phi = (epsp * f).reshape(-1, 1)
        y_hi = 0.5 * epsp
        A, c = ref.box_region([-1.0], [y_hi])
        v0 = ref.primal_extreme(l, u, phi, f, A, c, +1)
        kappa = 1e-3
        A, c = ref.box_region([-1.0 - kappa], [y_hi + kappa])
        v1 = ref.primal_extreme(l, u, phi, f, A, c, +1)
        tau, eta = ref.dual_upper_lp_box(l, u, phi, f, [-1.0], [y_hi])
        print(f"[2.5] steep instance eps'={epsp}: V+ = {v0:.4f}, after enlarging R by kappa={kappa}: {v1:.4f};"
              f" increase/kappa = {(v1 - v0) / kappa:.1f}, |eta|_1 = {np.abs(eta).sum():.1f}")

    # (iii) the sentence 'total excess width of S3's interval is up to 2 kappa (1 + |eta+| v |eta-|)':
    # search for samples where the excess is larger (kappa from the realised d_H, the least valid kappa)
    best = 0.0
    best_case = None
    best_rep = 0.0          # against the repaired bound 2 kappa (2 + |eta+| + |eta-|)
    for _ in range(3000):
        N = int(rng.integers(3, 7))
        l, u, phi, f = random_instance(N, 1, rng, gamma=float(rng.uniform(1.5, 6)))
        V = np.column_stack([np.ones(N), phi, f])
        G = (u - l).sum()
        Zl = l.sum()
        q = (u - l) / G
        L = int(rng.integers(2, 30))
        counts = rng.multinomial(L, q)
        uh = l + G * counts / L
        dH = ref.hausdorff_linf_over_G(V, q, counts) * G
        kappa = 2 * dH / Zl
        if kappa <= 1e-9:
            continue
        p0 = rng.uniform(l, u)
        y = (p0 @ phi) / p0.sum()
        half = rng.uniform(0.0, 0.05, 1)
        ylo, yhi = y - half, y + half
        A, c = ref.box_region(ylo, yhi)
        I = ref.primal_interval(l, u, phi, f, A, c)
        A2, c2 = ref.box_region(ylo - kappa, yhi + kappa)
        Ih = ref.primal_interval(l, uh, phi, f, A2, c2)
        if I is None or Ih is None:
            continue
        tau_p, eta_p = ref.dual_upper_lp_box(l, u, phi, f, ylo, yhi)
        tau_m, eta_m = ref.dual_upper_lp_box(l, u, phi, -f, ylo, yhi)
        if eta_p is None or eta_m is None:
            continue
        excess = (Ih[1] - Ih[0] + 2 * kappa) - (I[1] - I[0])
        claim = 2 * kappa * (1 + max(np.abs(eta_p).sum(), np.abs(eta_m).sum()))
        repaired = 2 * kappa * (2 + np.abs(eta_p).sum() + np.abs(eta_m).sum())
        best_rep = max(best_rep, excess / repaired)
        if excess / claim > best:
            best = excess / claim
            best_case = (N, L, round(float(kappa), 5), round(float(excess), 5), round(float(claim), 5))
    print(f"[2.5] max over 3000 random samples of (excess width of S3) / (2 kappa (1 + max|eta|_1)) = {best:.3f}"
          f"   case (N, L, kappa, excess, claimed) = {best_case}")
    print(f"[2.5] the same against 2 kappa (2 + |eta+|_1 + |eta-|_1) (region enlarged by 2 kappa in the"
          f" coordinates of K, target by 2 kappa): max ratio = {best_rep:.3f} (must be <= 1)")


if __name__ == "__main__":
    check_prop21()
    compare_bounds()
    check_prop23()
    check_cor24_nonconvex()
    check_prop25_and_excess()
    check_concentration()
