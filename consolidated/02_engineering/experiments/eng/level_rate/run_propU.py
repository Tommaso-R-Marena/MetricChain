"""An attempt to break Proposition U of R_REPORT (the one-level upper bound in dual form), and Lemma L with it.

Proposition U (their paper proof, not machine-checked): for b > 0, W : [0, b] -> [0, 1] convex, nondecreasing,
continuous, M_{W,b}(x) = max_{0<=B<=b} (B - W(B) x) and every nonincreasing T <= M_{W,b},

    R[T](g)  <=  U(g) := sup{ B - Sigma(B, W(B)) g : 0 <= B <= b, Sigma(B, W(B)) < infinity }.

Lemma L (machine-checked by them; re-derived by hand here) gives, for T = M_{W,b},

    R[T](g)  >=  Llow(g) := sup{ B - max(W(B), Sigma(B, W(B))) g : ... }.

The test takes T = M_{W,b} (the extreme case), random convex piecewise-linear W, and computes
r(g) = inf_phi H1(phi, beta; g) for the chords of T on a grid (H1 of lr_recursion.py: an upper bound of R[T],
and exactly the quantity that their proof bounds by U, because for slopes in [-1, 0] the choice beta -> 0 is
optimal in H1).  Reported: max of (r - U)/a (Proposition U wants <= 0; r is computed from the chords of T,
which lie above T, so r - U > 0 is discretisation error and is shown on two grids, N = 3000 and 12000) and
min of (r - Llow)/a (Lemma L wants >= 0), over all cases and accuracies.

    python experiments/eng/level_rate/run_propU.py [--cases 150]          # about 4 minutes
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_lines as LN  # noqa: E402
import lr_recursion as R  # noqa: E402
import numpy as np  # noqa: E402


def random_convex_W(rng, b: float, x_top: float, nb: int = 6001):
    """A convex nondecreasing piecewise-linear W on [0, b] with W(0) = 0, first slope >= 1/x_top (so that
    M_{W,b} vanishes from x_top on) and W(b) = wtop in (0.15, 1]."""
    Bs = np.linspace(0.0, b, nb)
    m = int(rng.integers(1, 6))
    br = np.sort(rng.uniform(0.0, b, size=m))
    inc = rng.exponential(1.0, size=m)
    W = np.zeros(nb)
    for p, s in zip(br, inc):
        W += s * np.maximum(Bs - p, 0.0)
    base = Bs / b
    W = rng.uniform(0.0, 1.0) * base + W / max(W[-1], 1e-300) * rng.uniform(0.0, 1.0)
    wtop = rng.uniform(0.15, 1.0)
    W = W / W[-1] * wtop
    W = np.maximum(W, Bs / x_top)                # keeps convexity (maximum of convex functions), W(0) = 0
    if W[-1] > 1.0:
        W = W / W[-1]
    return Bs, W


def prop_u_case(pair, theta, rng, N: int = 3000, ng: int = 9, N2: int | None = None):
    """One random case.  With ``N2`` the value r is computed on a second, finer grid as well (key ``r2``): the
    excess of r over U is discretisation error of r (chords of M_{W,b}) and must shrink with the grid."""
    a, h, E = float(pair.a), float(pair.h), float(pair.E)
    b = h + (a - h) * rng.uniform(0.02, 0.95)
    x_top = 40.0 * b
    Bs, W = random_convex_W(rng, b, x_top)
    g = E * rng.uniform(0.01, 0.9, size=ng)
    out = {}
    for key, n in (("r", N), ("r2", N2)):
        if n is None:
            continue
        out[key] = _r_on_grid(pair, theta, Bs, W, x_top, g, n)
    r = out["r"]
    sig, _ = LN.sigma_dual(pair, Bs[1:], W[1:])
    fin = np.isfinite(sig)
    Bf, sf, Wf = Bs[1:][fin], sig[fin], W[1:][fin]
    U = np.max(Bf[None, :] - sf[None, :] * g[:, None], axis=1)
    Llow = np.max(Bf[None, :] - np.maximum(sf, Wf)[None, :] * g[:, None], axis=1)
    U, Llow = np.maximum(U, 0.0), np.maximum(Llow, 0.0)        # the line B = 0
    sub = bool(np.all(sf >= Wf - 1e-12))          # W is a sub-solution on the regular range: then U = Llow
    res = dict(b=b, g=g, r=r, U=U, Llow=Llow, subsolution=sub, wtop=float(W[-1]))
    if "r2" in out:
        res["r2"] = out["r2"]
    return res


def _r_on_grid(pair, theta, Bs, W, x_top, g, N):
    ub = R.ConvexUpperBound(pair, N=N, theta=theta, x_top=x_top)
    x = ub.x
    M = np.empty(len(x))
    for i0 in range(0, len(x), 500):             # M_{W,b} at the nodes
        xs = x[i0:i0 + 500]
        M[i0:i0 + 500] = np.max(Bs[None, :] - W[None, :] * xs[:, None], axis=1)
    M[-1] = 0.0
    M, _ = R.lower_hull_values(x, M)
    ub.Mf.set(M)
    return ub.apply(g)[0]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261126)
    args = ap.parse_args(argv)
    out = dict(pinned_theory_commit=C.PINNED, cases_per_pair=args.cases, seed=args.seed, pairs={})
    for case in ("gauss", "cube_u1", "prod_4_1_l0.25"):
        t0 = time.time()
        pair = C.make(case)
        theta = R.build_theta(pair, 200_000)
        rng = np.random.default_rng(args.seed)
        worst_u, worst_u2, worst_l, nsub, gap = -np.inf, -np.inf, np.inf, 0, 0.0
        eq_sub = 0.0
        for _ in range(args.cases):
            res = prop_u_case(pair, theta, rng, N=3000, N2=12000)
            du = float(np.max(res["r"] - res["U"]) / pair.a)
            du2 = float(np.max(res["r2"] - res["U"]) / pair.a)
            dl = float(np.min(res["r2"] - res["Llow"]) / pair.a)
            worst_u, worst_u2, worst_l = max(worst_u, du), max(worst_u2, du2), min(worst_l, dl)
            gap = max(gap, float(np.max(res["U"] - res["Llow"]) / pair.a))
            if res["subsolution"]:
                nsub += 1
                eq_sub = max(eq_sub, float(np.max(np.abs(res["r2"] - res["U"])) / pair.a))
        out["pairs"][case] = dict(max_r_minus_U_over_a_N3000=worst_u, max_r_minus_U_over_a_N12000=worst_u2,
                                  min_r_minus_Llow_over_a=worst_l,
                                  n_subsolutions=nsub, max_abs_r_minus_U_over_a_on_subsolutions_N12000=eq_sub,
                                  max_U_minus_Llow_over_a=gap, seconds=time.time() - t0)
        print(case, out["pairs"][case], flush=True)
    C.dump("propU.json", out)


if __name__ == "__main__":
    main()
