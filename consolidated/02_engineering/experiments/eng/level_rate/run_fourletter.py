"""Where hypothesis (H1) of Theorem R fails for a product landscape: the uniform four-letter Hamming site at the
slope u* at which dips on single letters and dips on pairs are equally hard (see lr_multiletter.py).

1. checks of F* = max_s Phi_s: against the numbers of THEORY_REPORT 11.26 (Proposition 11.103(b), (d), (e)) and
   against a direct numerical solution of the Renyi programme of Theorem 11.99 over all vertices;
2. u*: the root of max Phi_1 = max Phi_2 (q = 4) -- it is u* = ln 3, where Phi_1(t) = Phi_2(1 - t) identically
   (algebra); the dual function J is then constant on [L_a, L_b] = [1 - L, L], theta_na has a kink at h, and
   Proposition K of R_REPORT gives tau_k - h >= (L_b - L_a) h/(k + 2);
3. the lower bound from the line dynamics at u* and at neighbouring slopes, for k up to 1280, and the convex
   upper bound at u* -- to see the rate 1/k at u* and the long pre-asymptotic range next to it.

    python experiments/eng/level_rate/run_fourletter.py           # about 10 minutes
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lr_cases as C  # noqa: E402
import lr_lines as LN  # noqa: E402
import lr_multiletter as ML  # noqa: E402
import lr_recursion as R  # noqa: E402
import numpy as np  # noqa: E402

KS = [2, 5, 10, 20, 40, 80, 160, 320, 640, 1280]


def main():
    t0 = time.time()
    out = dict(pinned_theory_commit=C.PINNED)
    # 1. checks
    s3 = ML.UniformHammingSite(3, 1.0)
    s4 = ML.UniformHammingSite(4, 1.0)
    out["report_numbers"] = dict(
        q3_u1_h=dict(ours=s3.h, theirs=0.03065363), q3_u1_E=dict(ours=s3.E, theirs=0.119499),
        q4_u1_h=dict(ours=s4.h, theirs=0.029139), q4_u1_a=dict(ours=s4.a, theirs=0.117993),
        q4_u1_E=dict(ours=s4.E, theirs=0.120115))
    direct = []
    for q, u, t in ((4, 1.0, 0.3), (4, 1.0, 0.7), (4, 1.5, 0.45), (4, 2.0, 0.5), (4, 1.2, 0.9), (3, 1.0, 0.5)):
        site = ML.UniformHammingSite(q, u, n_grid=2001)
        direct.append(dict(q=q, u=u, t=t, max_s_Phi=float(site.Fstar(np.array(t))), direct=ML.renyi_direct(q, u, t)))
    out["direct_programme"] = direct
    out["direct_max_abs_diff"] = max(abs(d["max_s_Phi"] - d["direct"]) for d in direct)
    # 2. the critical slope
    def gap(u):
        return ML.SubsetDip(4, 1, u).h - ML.SubsetDip(4, 2, u).h
    lo, hi = 1.0, 2.0
    assert gap(lo) < 0 < gap(hi)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if gap(mid) < 0:
            lo = mid
        else:
            hi = mid
    ustar = 0.5 * (lo + hi)
    site = ML.UniformHammingSite(4, ustar)
    La, Lb = site.flat_top(1e-9)
    p1, p2 = ML.SubsetDip(4, 1, ustar), ML.SubsetDip(4, 2, ustar)
    tt = np.linspace(0.0, 1.0, 1001)
    u3 = math.log(3.0)
    mirror = float(np.max(np.abs(ML.SubsetDip(4, 1, u3).F(tt) - ML.SubsetDip(4, 2, u3).F(1 - tt))))
    out["critical"] = dict(u_star=ustar, exp_u_star=math.exp(ustar), u_star_minus_ln3=ustar - u3,
                           max_abs_Phi1_t_minus_Phi2_1_minus_t_at_ln3=mirror,
                           h=site.h, a=site.a, E=site.E,
                           L_pairs=p2.L, L_singletons=p1.L, flat_top=[La, Lb],
                           vartheta_pairs=p2.vartheta, vartheta_singletons=p1.vartheta,
                           constant_pairs=p2.constant, constant_singletons=p1.constant,
                           kink_of_theta_na_at_h=dict(left_slope=-Lb / (1 - Lb), right_slope=-La / (1 - La)),
                           proposition_K_coefficient=(Lb - La) * site.h)
    # 3. sequences
    seqs = {}
    for du in (0.0, -0.02, 0.02, -0.1, 0.1, -0.3, 0.3):
        u = ustar + du
        st = ML.UniformHammingSite(4, u)
        act = max(st.parts, key=lambda p: p.h)              # the branch that carries the maximum
        const = act.constant
        rows = {}
        for k in KS + ([2560] if du == 0.0 else []):
            b = float(LN.b_inf(st, k))
            rows[str(k)] = dict(B=repr(b), k_excess_over_h=k * (b - st.h) / st.h, k2_excess=k * k * (b - st.h),
                                ratio_to_constant_of_active_branch=k * k * (b - st.h) / const)
        seqs[f"{du:+.2f}"] = dict(u=u, h=st.h, active_subset_size=act.s, L=act.L, vartheta=act.vartheta,
                                  constant=const, other_branch_h=min(p.h for p in st.parts[:2]),
                                  flat_top=list(st.flat_top(1e-9)), lines=rows)
        print(f"u = u* {du:+.2f}: k (B-h)/h at k=160, 640: {rows['160']['k_excess_over_h']:.4f} {rows['640']['k_excess_over_h']:.4f};"
              f" k^2 (B-h)/C: {rows['160']['ratio_to_constant_of_active_branch']:.3f} {rows['640']['ratio_to_constant_of_active_branch']:.3f}",
              flush=True)
    out["sequences"] = seqs
    # the upper bound at u*
    ub = R.ConvexUpperBound(site, N=4000, n_theta=200_000)
    ub.run(80)
    taus = ub.taus()
    out["upper_at_u_star"] = {str(k): dict(tau_upper=repr(taus[k]), k_excess_over_h=k * (taus[k] - site.h) / site.h)
                              for k in (2, 5, 10, 20, 40, 80)}
    out["upper_at_u_star_n_above"] = int(sum(r.get("n_above", 0) for r in ub.history))
    out["seconds"] = time.time() - t0
    C.dump("fourletter.json", out)
    print({k: v for k, v in out["critical"].items()})
    print("upper at u*:", out["upper_at_u_star"])


if __name__ == "__main__":
    main()
