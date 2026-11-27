"""Small extra checks (a few minutes in total):

1. the four biased cubes of the theory division's out_lines_lb_general.txt: our constants (two closed forms of
   F*, mpmath derivatives) and our B_inf(k) against the numbers printed there;
2. the passage time of Lemma PT (R_REPORT section 7), sqrt(delta) N_t(delta) -> pi h sqrt(2 vartheta), for the
   validation pairs and the new instances;
3. the bottleneck (Sigma-6): D(h + delta, L + v) h / (delta + v^2/(2 vartheta)) -> 1;
4. tau_3 of the two validation pairs with no grid for T_2 (an independent check of the grid computations);
5. the two sides of condition (C2) of Lemma RC for the validation pairs (R_REPORT quotes 0.3005 against 0.45
   and 0.48 against 0.35 for the Gaussian pair).

    python experiments/eng/level_rate/run_extras.py
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_lines as LN  # noqa: E402
import lr_pairs as P  # noqa: E402
import lr_recursion as R  # noqa: E402
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402


def biased_table() -> dict:
    out = {}
    for case in ("biased_p0.3_u1", "biased_p0.1_u1", "biased_p0.1_u2", "biased_p0.02_u2"):
        pair = C.make(case)
        th = C.THEIRS[case]
        cst = pair.constants()
        p, u = pair.sites[0][2], pair.sites[0][1]
        old = mp.mp.dps
        mp.mp.dps = 30
        try:   # the cosh form of Theorem 11.59(b), independent of the Renyi form used by the pair
            L = cst["L"]
            h_cosh = P.biased_F_cosh(p, u, L, dps=30)
            d2_cosh = mp.diff(lambda s: P.biased_F_cosh(p, u, s, dps=30), L, 2, h=mp.mpf("1e-5"))
        finally:
            mp.mp.dps = old
        row = dict(ours={k: float(cst[k]) for k in ("a", "h", "L", "vartheta", "constant")},
                   ours_cosh_form=dict(h=float(h_cosh), vartheta=float(-1 / d2_cosh)),
                   theirs={k: th[k] for k in ("a", "h", "L", "vartheta", "constant")},
                   rel_diff_vartheta=th["vartheta"] / float(cst["vartheta"]) - 1,
                   rel_diff_constant=th["constant"] / float(cst["constant"]) - 1,
                   h_theirs_minus_ours=th["h"] - float(cst["h"]), lines={})
        for k, b_th in sorted(th["lines_lb"].items()):
            b = float(LN.b_inf(pair, k))
            row["lines"][str(k)] = dict(
                B_ours=repr(b), B_theirs=b_th, diff=b_th - b,
                ratio_ours=k * k * (b - float(cst["h"])) / float(cst["constant"]),
                ratio_theirs_printed=th.get("lines_ratio", {}).get(k),
                ratio_theirs_B_with_our_constants=k * k * (b_th - float(cst["h"])) / float(cst["constant"]))
        out[case] = row
        print(case, {k: (v if not isinstance(v, dict) else "...") for k, v in row.items() if k != "lines"},
              row["lines"].get("160"), flush=True)
    return out


def passage_table(cases) -> dict:
    out = {}
    for case in cases:
        pair = C.make(case)
        h, L, vth, a = pair.h, pair.L, pair.vartheta, pair.a
        s_t = L + 0.5 * min(0.1, 1 - h / a - L)          # a level in (L, 1 - h/a)
        cstar = math.pi * h * math.sqrt(2 * vth)
        rows = {}
        for e in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            n = LN.passage_time(pair, e * h, s_t)
            rows[str(e)] = dict(N_t=n, scaled=math.sqrt(e * h) * n / cstar)
        # (Sigma-6): D(h + delta, L + v) h/(delta + v^2/(2 vartheta)) for small delta, v
        bott = {}
        for delta_rel, v in ((1e-4, 0.0), (1e-4, 0.01), (1e-4, -0.01), (1e-6, 0.001), (1e-6, -0.001), (1e-3, 0.03)):
            delta = delta_rel * h
            sig = float(LN.sigma_dual(pair, h + delta, L + v)[0])
            bott[f"{delta_rel:g},{v:g}"] = (sig - (L + v)) * h / (delta + v * v / (2 * vth))
        out[case] = dict(s_t=s_t, one_minus_h_over_a=1 - h / a, passage=rows, bottleneck_ratio=bott)
        print(case, "passage:", {k: round(v["scaled"], 4) for k, v in rows.items()},
              "bottleneck:", {k: round(v, 4) for k, v in bott.items()}, flush=True)
    return out


def tau3_gridless(pair) -> dict:
    """tau_3 with the step from level 1 to level 2 done without any grid for T: T_2(x) = inf_{phi, beta} H1 with
    the closed-form T_1 = theta_na (convex, so H1 is exact: see lr_recursion.py), then tau_3 from the balance
    T_2(x_b) = tau_2 - x_b, tau_3 = tau_2 a/(a + x_b) -- the minimum over phi of
    max((1 - phi) tau_2, phi a + (1 - phi) T_2(phi a/(1 - phi))) when S_2 = x + T_2 increases at x_b (checked).
    An independent check of the grid computations at k = 3."""
    a = float(pair.a)
    xm = float(pair.curve(np.array(0.5))[0])                 # S_1 = x + theta has slope 0 where theta' = -1: t = 1/2
    smin = xm + float(pair.theta_na(np.array(xm)))

    def t12(phi, c, beta, g):
        t1 = beta + c * pair.theta_na(beta / c)
        mu = phi * pair.theta_na((g - beta) / phi)
        xh = mu / c
        t2 = np.where(xh >= xm, mu + c * pair.theta_na(xh), c * smin)
        return t1, t2

    def T2(x):
        x = np.asarray(x, dtype=float)
        f = lambda p: R.balance_min(t12, R._expit(p), R._expit(-p), x, xm, 60, 1e-16 * a)[0]
        return R.golden_min(f, np.full(x.shape, -34.0), np.full(x.shape, 34.0), 41, 60)[1]

    tau2 = R.tau2_closed(pair)
    lo, hi = 1e-3 * a, 0.99 * float(pair.E)
    for _ in range(9):                                        # multisection for T_2(x) = tau_2 - x
        xs = np.linspace(lo, hi, 17)
        d = T2(xs) - (tau2 - xs)                              # negative near 0 (T_2 falls steeply), positive later
        j = int(np.argmax(d > 0))
        lo, hi = xs[j - 1], xs[j]
    xb = 0.5 * (lo + hi)
    eps = 1e-3 * xb
    v = T2(np.array([xb - eps, xb, xb + eps]))
    return dict(tau2_closed=tau2, x_b=xb, tau3=tau2 * a / (a + xb), tau3_over_a=tau2 / (a + xb),
                S2_increasing_at_xb=bool(v[2] + eps > v[1] > v[0] - eps), bracket_width=hi - lo)


def c2_check(pair, ds: float) -> dict:
    """The two sides of condition (C2) of Lemma RC (R_REPORT section 6) at the level s_t = L + ds:
    D(h, s_t) + lambda_bar (1 - s_t - h/a) < 1 - s_t, lambda_bar = theta(e)/e at the point e where the line of
    intercept h and slope -s_t touches (1 - sigma_*) theta, Sigma(h, sigma_*) = s_t."""
    h, L, a = float(pair.h), float(pair.L), float(pair.a)
    s_t = L + ds
    D = float(LN.sigma_dual(pair, h, s_t)[0]) - s_t
    lo, hi = L, s_t                                           # Sigma(h, .) increases on [L, s_t]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if float(LN.sigma_dual(pair, h, mid)[0]) < s_t:
            lo = mid
        else:
            hi = mid
    sig = 0.5 * (lo + hi)
    _, tp = LN.sigma_dual(pair, h, sig)                       # the touching point has curve parameter t'
    e, th = pair.curve(np.array(float(tp)))
    lam = float(th / e)
    return dict(s_t=s_t, D=D, sigma_star=sig, e=float(e), lambda_bar=lam,
                left=D + lam * (1 - s_t - h / a), right=1 - s_t)


def main():
    t0 = time.time()
    out = dict(pinned_theory_commit=C.PINNED)
    out["C2_of_lemma_RC"] = {case: {str(ds): c2_check(C.make(case), ds) for ds in (0.05, 0.15)}
                             for case in C.VALIDATION}
    print("(C2):", {c: {k: (round(v["left"], 4), round(v["right"], 4)) for k, v in d.items()}
                    for c, d in out["C2_of_lemma_RC"].items()}, flush=True)
    out["tau3_gridless"] = {}
    for case in C.VALIDATION:
        out["tau3_gridless"][case] = tau3_gridless(C.make(case))
        print(case, "tau_3 without a grid for T_2:", out["tau3_gridless"][case], flush=True)
    out["biased_cubes"] = biased_table()
    out["passage_and_bottleneck"] = passage_table(C.VALIDATION + C.NEW)
    out["seconds"] = time.time() - t0
    C.dump("extras.json", out)
    _ = np


if __name__ == "__main__":
    main()
