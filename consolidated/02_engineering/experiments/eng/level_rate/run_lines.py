"""Method (b): the lower bound tau_k >= B_inf(k) from the line dynamics, the constants of Theorem R, and the
numerical check of hypothesis (H1), for one or several cases.

For every case, results/lines_<case>.json contains
* the constants a, E, L, h, vartheta = -1/F''(L), the predicted limit 2 pi^2 h^2 vartheta (mpmath, 40 digits);
* B_inf(k) for k = 1..K and a few larger k (double precision; multisection), with k^2 (B_inf - h) and its ratio
  to the predicted constant -- a floating-point evaluation of a proved lower bound of tau_k;
* cross-checks of selected values in mpmath (30 digits);
* for products of symmetric sites: decimal strings B for which "p_k(B) < infinity" is proved in interval
  arithmetic (rigorous lower bounds of tau_k, given Proposition A of R_REPORT);
* for the Gaussian pair: the exact lower bounds in rational arithmetic and the closed form of R_REPORT section 10;
* (H1): the dual function J evaluated from theta_na itself against F, its second difference at L, concavity of F.

Usage (repository root):
    python experiments/eng/level_rate/run_lines.py gauss cube_u1            # 2 to 8 minutes per case
    python experiments/eng/level_rate/run_lines.py --group new
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_lines as LN  # noqa: E402
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402

LARGE_K = [240, 320, 480, 640, 960, 1280, 2560, 5120]


def h1_check(pair) -> dict:
    """Numerical check of (H0)/(H1) for a smooth pair: F concave on a grid; a unique maximiser; the dual
    function computed from theta_na (an infimum over e) equals F; its second difference at L against F''(L)."""
    out = {}
    ts = np.linspace(1e-4, 1 - 1e-4, 20001)
    f = pair.F(ts)
    d2 = np.diff(f, 2) / (ts[1] - ts[0]) ** 2
    out["max_second_difference_of_F"] = float(d2.max())                 # < 0: strictly concave on the grid
    out["F_concave_on_grid"] = bool(d2.max() < 0)
    k = int(np.argmax(f))
    out["argmax_F_on_grid"] = float(ts[k])
    cst = pair.constants()
    L, h = float(cst["L"]), float(cst["h"])
    # J from theta_na against F (steps scaled down when the maximiser is close to an end of [0, 1])
    sc = min(1.0, min(L, 1 - L) / 0.25)
    out["step_scale"] = sc
    tt = [0.05 * sc, 0.2 * sc, L - 0.05 * sc, L, L + 0.05 * sc, 0.8, 0.95]
    out["J_from_theta_minus_F"] = [float(pair.dual_J_from_theta(t) - float(pair.F(np.array(t)))) for t in tt]
    out["J_from_theta_at_L_minus_h"] = float(pair.dual_J_from_theta(L) - h)
    sec = {}
    for eta0 in (2e-2, 1e-2, 5e-3):
        eta = eta0 * sc
        j0, jp, jm = (pair.dual_J_from_theta(L), pair.dual_J_from_theta(L + eta), pair.dual_J_from_theta(L - eta))
        sec[str(eta0)] = float((jp - 2 * j0 + jm) / eta**2)
    out["second_difference_of_J_from_theta_at_L"] = sec
    out["F2_at_L_mpmath"] = float(cst["d2"])
    # vartheta from theta_na itself: theta''(h)/(1 + |theta'(h)|)^3 by central differences of theta_na
    e = 1e-4 * h
    th = pair.theta_na(np.array([h - 2 * e, h - e, h, h + e, h + 2 * e]))
    d1 = (th[3] - th[1]) / (2 * e)
    d2h = (-th[4] + 16 * th[3] - 30 * th[2] + 16 * th[1] - th[0]) / (12 * e * e)
    out["theta_at_h_minus_h"] = float(th[2] - h)
    out["theta_prime_at_h"] = float(d1)
    out["minus_L_over_1_minus_L"] = float(-L / (1 - L))
    out["vartheta_from_theta_na"] = float(d2h / (1 + abs(d1)) ** 3)
    out["vartheta_from_F"] = float(cst["vartheta"])
    out["L_less_than_1_minus_h_over_a"] = bool(L < 1 - h / float(cst["a"]))
    return out


def run(case: str, K: int, large: bool, mp_ks, cert_ks) -> dict:
    t0 = time.time()
    pair = C.make(case)
    smooth = getattr(pair, "smooth", True)
    out = dict(case=case, name=pair.name, pinned_theory_commit=C.PINNED)
    if smooth:
        cst = pair.constants()
        out["constants"] = {k: mp.nstr(cst[k], 20) for k in ("a", "E", "L", "h", "vartheta", "constant", "d2", "d3")}
        finite = mp.isfinite(cst["constant"])
        const = float(cst["constant"]) if finite else None
    else:
        out["constants"] = dict(a=repr(pair.a), E=repr(pair.E), h=repr(pair.h))
        const = None
    h = float(pair.h)
    ks = list(range(1, K + 1)) + (LARGE_K if large else [])
    rows = {}
    for k in ks:
        b = float(LN.b_inf(pair, k))
        row = dict(B=repr(b), k2_excess=k * k * (b - h))
        if const:
            row["ratio"] = k * k * (b - h) / const
        rows[str(k)] = row
    out["lines"] = rows
    out["lines_note"] = "double precision evaluation of the proved lower bound tau_k >= B_inf(k); not certified"
    # mpmath cross-check
    if smooth and mp_ks:
        chk = {}
        for k in mp_ks:
            try:
                bm = LN.b_inf_mp(pair, k, dps=30, digits=16)
            except Exception as exc:                                    # recorded, not hidden
                chk[str(k)] = dict(error=repr(exc))
                continue
            bf = float(rows[str(k)]["B"])
            chk[str(k)] = dict(B_mp=mp.nstr(bm, 22), rel_diff_of_excess=float((mp.mpf(bf) - bm) / (bm - pair.constants(30)["h"])))
        out["mpmath_check"] = chk
    # interval arithmetic
    if smooth and hasattr(pair, "sites") and pair._symmetric() and cert_ks:
        cert = {}
        for k in cert_ks:
            b = float(rows[str(k)]["B"])
            lo = math.floor(b * 1e12 - 1) / 1e12                        # 12 decimals, rounded down
            s_lo = f"{lo:.12f}"
            s_hi = f"{lo + 3e-12:.12f}"
            cert[str(k)] = dict(B_certified=s_lo, proved=bool(LN.certify_lower(pair, s_lo, k)),
                                B_next=s_hi, next_proved=bool(LN.certify_lower(pair, s_hi, k)))
        out["certified_lower_bounds"] = cert
    if case == "gauss":
        ex = {}
        for k in (2, 3, 4, 5, 10, 20, 40, 80, 160):
            n9 = LN.gauss_exact(k, 9)
            b = Fraction(n9, 10**9)
            ex[str(k)] = dict(N=n9, k2_excess=float(k * k * (b - Fraction(1, 4))),
                              ratio=float(k * k * (b - Fraction(1, 4))) / (math.pi**2 / 16),
                              shifted_ratio=float((k + 0.5) ** 2 * (b - Fraction(1, 4))) / (math.pi**2 / 16),
                              closed_form_root=mp.nstr(LN.gauss_closed_form_root(k), 20))
        out["gauss_exact_1e9"] = ex
        pt = {}
        cstar = math.pi * 0.25 * math.sqrt(2 * 0.5)
        for e in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            n = LN.passage_time(pair, e * 0.25, 0.55)
            pt[str(e)] = dict(N_t=n, scaled=math.sqrt(e * 0.25) * n / cstar)
        out["passage_time_s_t_0.55"] = pt
    if smooth and const:
        out["H1_check"] = h1_check(pair)
    out["seconds"] = time.time() - t0
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*")
    ap.add_argument("--group", choices=["validation", "new", "stress", "negative"])
    ap.add_argument("--K", type=int, default=160)
    ap.add_argument("--no-large", action="store_true")
    args = ap.parse_args(argv)
    cases = list(args.cases)
    if args.group:
        cases += {"validation": C.VALIDATION, "new": C.NEW, "stress": C.STRESS, "negative": C.NEGATIVE}[args.group]
    for case in cases:
        biased = case.startswith("biased")
        res = run(case, args.K, not args.no_large, mp_ks=(2, 10, 40) if biased else (2, 3, 10, 40, 160),
                  cert_ks=(2, 3, 10, 40, 160))
        path = C.dump(f"lines_{case}.json", res)
        last = res["lines"][str(args.K)]
        print(f"{case}: h={res['constants'].get('h')} constant={res['constants'].get('constant')} "
              f"ratio at k={args.K}: {last.get('ratio')}  ({res['seconds']:.0f} s) -> {path.name}", flush=True)


if __name__ == "__main__":
    main()
