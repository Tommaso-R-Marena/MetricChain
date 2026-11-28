"""Review checks for Theorem 4.1 of CERTIFIED_INFERENCE.md (exact dual, consistency).

(a) soundness, (b) completeness against a primal linear programme, on random and degenerate instances;
(c) extremal weights - a counterexample to the literal statement; (e) the inconsistency certificate -
its failure for l = 0; non-attainment of the infimum over eta for a region tangent to the reachable set.

Run:  python check_thm41.py
"""
from __future__ import annotations

import numpy as np

import ref

rng = np.random.default_rng(4141)


def reachable_point(l, u, phi, rng):
    w = rng.uniform(l, u)
    if w.sum() <= 0:
        w = u.copy()
    return (w @ phi) / w.sum()


def gen(N, m, kind, rng):
    u = rng.uniform(0.2, 1.0, N)
    if kind == "generic":
        l = u * rng.uniform(0.05, 0.9, N)
    elif kind == "l=u somewhere":
        l = np.where(rng.random(N) < 0.5, u, u * rng.uniform(0.05, 0.9, N))
    elif kind == "l=u everywhere":
        l = u.copy()
    elif kind == "l=0":
        l = np.zeros(N)
    elif kind == "l=0 somewhere":
        l = np.where(rng.random(N) < 0.5, 0.0, u * rng.uniform(0.05, 0.9, N))
        if l.sum() == 0:
            l[0] = 0.5 * u[0]
    elif kind == "u=0 somewhere":
        l = u * rng.uniform(0.05, 0.9, N)
        dead = rng.random(N) < 0.3
        dead[0] = False
        u = np.where(dead, 0.0, u)
        l = np.where(dead, 0.0, l)
    else:
        raise ValueError(kind)
    phi = rng.uniform(-1, 1, (N, m))
    f = rng.uniform(-1, 1, N)
    return l, u, phi, f


def check_completeness():
    print("[4.1 a,b] primal LP  vs  inf_eta tau*(eta) (direct minimisation)  vs  dual LP;  box regions")
    print("   kind                m   cases  empty   max|primal - dual_direct|   max|primal - dual_LP|   soundness viol.")
    for kind in ("generic", "l=u somewhere", "l=u everywhere", "l=0", "l=0 somewhere", "u=0 somewhere"):
        for m in (0, 1, 2):
            worst_direct = 0.0
            worst_lp = 0.0
            sound_viol = 0
            empty = 0
            cases = 0
            for _ in range(60):
                N = int(rng.integers(3, 9))
                l, u, phi, f = gen(N, m, kind, rng)
                if m > 0:
                    y = reachable_point(l, u, phi, rng)
                    mode = rng.integers(0, 4)
                    if mode == 0:        # generic box around a reachable point
                        half = rng.uniform(0.02, 0.3, m)
                    elif mode == 1:      # exact data: R a point
                        half = np.zeros(m)
                    elif mode == 2:      # displaced: possibly empty
                        y = y + rng.uniform(-1.0, 1.0, m)
                        half = rng.uniform(0.0, 0.1, m)
                    else:                # observables at the end of their range / uninformative
                        half = np.full(m, 3.0)
                    ylo, yhi = y - half, y + half
                    A, c = ref.box_region(ylo, yhi)
                    hR = lambda e, ylo=ylo, yhi=yhi: ref.h_box(e, ylo, yhi)
                else:
                    A = c = None
                    ylo = yhi = np.zeros(0)
                    hR = lambda e: 0.0
                cases += 1
                vp = ref.primal_extreme(l, u, phi, f, A, c, +1)
                if vp is None:
                    empty += 1
                    continue
                vd, eta = ref.dual_upper(l, u, phi, f, hR, m, seed=int(rng.integers(1 << 30)))
                worst_direct = max(worst_direct, abs(vp - vd))
                if vd < vp - 1e-9:
                    sound_viol += 1
                vlp, _ = ref.dual_upper_lp_box(l, u, phi, f, ylo, yhi)
                if vlp is not None:
                    worst_lp = max(worst_lp, abs(vp - vlp))
                else:
                    worst_lp = np.inf
                # soundness (a) at random certificates: any (tau, eta) with Psi <= 0 bounds the primal
                for _ in range(5):
                    e = rng.normal(size=m) * rng.choice([0.3, 3.0, 30.0])
                    t = ref.tau_star(e, l, u, phi, f, hR)
                    if t < vp - 1e-9:
                        sound_viol += 1
            print(f"   {kind:18s}  {m}   {cases:4d}   {empty:4d}        {worst_direct:.2e}"
                  f"                {worst_lp:.2e}              {sound_viol}")


def check_m0_threshold():
    worst = 0.0
    for _ in range(300):
        N = int(rng.integers(2, 9))
        l, u, phi, f = gen(N, 0, rng.choice(["generic", "l=0", "l=u somewhere", "l=u everywhere"]), rng)
        a = ref.threshold_max(l, u, f)
        b = ref.tau_star(np.zeros(0), l, u, phi, f, lambda e: 0.0)
        c = ref.primal_extreme(l, u, phi, f, None, None, +1)
        worst = max(worst, abs(a - b), abs(a - c))
    print(f"[4.1, m=0] threshold enumeration = root of Psi = LP: max abs diff = {worst:.2e}")


def counterexample_c():
    """4.1(c) read literally: 'at a pair (tau, eta) with Psi = 0 the threshold weights attain it'."""
    l = np.array([1.0, 1.0, 1.0])
    u = np.array([3.0, 3.0, 3.0])
    f = np.array([0.0, 0.5, 1.0])
    phi = np.array([[0.0], [0.0], [1.0]])
    ylo, yhi = np.array([0.0]), np.array([0.25])          # E_p phi = p(2) <= 0.25
    A, c = ref.box_region(ylo, yhi)
    hR = lambda e: ref.h_box(e, ylo, yhi)
    vplus = ref.primal_extreme(l, u, phi, f, A, c, +1)
    print("[4.1 c] instance: l=1, u=3 on 3 states, f=(0,.5,1), phi=1{x=2}, R=[0,0.25];"
          f" V+ = {vplus:.6f}")
    # (i) a non-optimal eta: Psi = 0 at tau*(0) but the threshold ensemble is infeasible
    eta = np.array([0.0])
    tau = ref.tau_star(eta, l, u, phi, f, hR)
    s = f - tau - phi @ eta + hR(eta)
    w = np.where(s > 0, u, l)
    p = w / w.sum()
    print(f"   eta = 0: tau*(0) = {tau:.6f} (Psi = {ref.Psi(tau, eta, l, u, phi, f, hR):.1e});"
          f" threshold ensemble has E f = {p @ f:.6f}, E phi = {(p @ phi)[0]:.4f} -> outside R: not in the identified set")
    # (ii) the optimal eta: the set {s = 0} carries weight and 'anything in between' is false
    tau_o, eta_o = ref.dual_upper_lp_box(l, u, phi, f, ylo, yhi)
    s = f - tau_o - phi @ eta_o + hR(eta_o)
    print(f"   optimal eta = {eta_o[0]:.6f}, tau = {tau_o:.6f}, scores s = {np.round(s, 9)}")
    zero = np.abs(s) < 1e-9
    for choice in ("l on {s=0}", "u on {s=0}"):
        w = np.where(s > 1e-9, u, l).astype(float)
        if choice.startswith("u"):
            w = np.where(zero, u, w)
        p = w / w.sum()
        feas = ylo[0] - 1e-12 <= (p @ phi)[0] <= yhi[0] + 1e-12
        print(f"   weights '{choice}': E f = {p @ f:.6f}, E phi = {(p @ phi)[0]:.6f}, feasible = {feas},"
              f" attains V+ = {abs(p @ f - vplus) < 1e-9}")


def counterexample_e():
    """4.1(e) 'I empty iff some eta has Phi(eta) > 0' fails for l = 0 (Phi <= 0 identically)."""
    u = np.array([1.0, 1.0])
    l = np.zeros(2)
    phi = np.array([[0.0], [1.0]])
    f = np.array([0.0, 1.0])
    ylo, yhi = np.array([2.0]), np.array([3.0])
    A, c = ref.box_region(ylo, yhi)
    print(f"[4.1 e] l = 0, phi = (0,1), R = [2,3]: primal = {ref.primal_extreme(l, u, phi, f, A, c, +1)} (None = empty set)")
    etas = np.concatenate([np.linspace(-50, 50, 2001), [1e3, -1e3, 1e6, -1e6]])
    best = -np.inf
    for e in etas:
        t = phi[:, 0] * e - ref.h_box([e], ylo, yhi)
        Phi = float(np.sum(l * np.maximum(t, 0) - u * np.maximum(-t, 0)))
        best = max(best, Phi)
    print(f"   sup over a wide grid of eta of Phi(eta) = {best:.3e}   (Phi = -sum u t_- <= 0 whenever l = 0:"
          " the certificate of (e) can never fire)")
    e = -1.0
    t = phi[:, 0] * e - ref.h_box([e], ylo, yhi)
    print(f"   the correct model-free certificate, min over supp u of t = eta.phi - h_R(eta), at eta = -1: {t.min():.3f} > 0")
    # with a small l > 0 the statement is right again
    l2 = np.full(2, 1e-3)
    best = max(float(np.sum(l2 * np.maximum(phi[:, 0] * e - ref.h_box([e], ylo, yhi), 0)
                            - u * np.maximum(-(phi[:, 0] * e - ref.h_box([e], ylo, yhi)), 0))) for e in etas)
    print(f"   same instance with l = 1e-3: sup Phi = {best:.3e} > 0")
    # random confirmation of (e) for Z_l > 0, both directions, m = 1
    agree = 0
    tot = 0
    for _ in range(300):
        N = int(rng.integers(3, 8))
        l, u, phi, f = gen(N, 1, rng.choice(["generic", "l=0 somewhere", "l=u somewhere"]), rng)
        y = reachable_point(l, u, phi, rng) + rng.uniform(-0.8, 0.8, 1)
        half = rng.uniform(0.0, 0.1, 1)
        ylo, yhi = y - half, y + half
        A, c = ref.box_region(ylo, yhi)
        empty = ref.primal_extreme(l, u, phi, f, A, c, +1) is None
        # Phi is positively homogeneous in eta: enough to test eta = +1 and eta = -1 for m = 1
        fires = False
        for e in (1.0, -1.0):
            t = phi[:, 0] * e - ref.h_box([e], ylo, yhi)
            if np.sum(l * np.maximum(t, 0) - u * np.maximum(-t, 0)) > 1e-12:
                fires = True
        tot += 1
        agree += int(fires == empty)
    print(f"   Z_l > 0, m = 1, random: certificate fires <=> primal empty in {agree}/{tot} instances")


def nonattainment():
    """A disc tangent to the reachable set: inf over eta of tau*(eta) is not attained (eta -> infinity)."""
    # States top, bottom, a, b with phi = (0,1), (0,-1), (1,0), (-1,0).  With u_top = l_bottom the maximum
    # of E phi_2 over the class is 0 for ANY weights of a, b: the reachable set Y of E phi has an edge on
    # the line y_2 = 0.  A disc above that line, tangent to it at an interior point y* of the edge, meets Y
    # only at y*, and f varies along the edge, so the multiplier needs a tangential part of finite size
    # and a normal part that must tend to infinity.  Z_l > 0 here.
    l = np.array([0.5, 1.0, 0.5, 0.5])
    u = np.array([1.0, 2.0, 2.0, 2.0])
    phi = np.array([[0.0, 1.0], [0.0, -1.0], [1.0, 0.0], [-1.0, 0.0]])
    f = np.array([0.0, 0.0, 1.0, 0.3])
    top = ref.primal_extreme(l, u, phi, phi[:, 1], None, None, +1)
    lo1 = ref.primal_extreme(l, u, phi, phi[:, 0], *ref.box_region([-9, top], [9, top]), -1)
    hi1 = ref.primal_extreme(l, u, phi, phi[:, 0], *ref.box_region([-9, top], [9, top]), +1)
    ystar = np.array([0.1, 0.0])
    rad = 0.5
    centre = ystar + np.array([0.0, rad])
    hR = lambda e: ref.h_ball(e, centre, rad)
    A, c = ref.box_region(ystar, ystar)
    vplus = ref.primal_extreme(l, u, phi, f, A, c, +1)
    print(f"[4.1 b] disc of radius {rad} tangent to the reachable set: max E phi_2 = {top:.2e}, edge"
          f" y_1 in [{lo1:.4f}, {hi1:.4f}], tangency at y* = {ystar}; Z_l = {l.sum()}")
    print(f"   primal V+ (the region meets the reachable set only at y*) = {vplus:.10f}")
    print("   tau*(eta) for eta = (a, -k), minimised over a:")
    from scipy.optimize import minimize_scalar
    for k in (1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6):
        res = minimize_scalar(lambda a: ref.tau_star(np.array([a, -k]), l, u, phi, f, hR),
                              bounds=(-20, 20), method="bounded", options={"xatol": 1e-12})
        print(f"      k = {k:9.0f}: best a = {res.x:8.5f}, tau* = {res.fun:.10f}, gap to V+ = {res.fun - vplus:.3e},"
              f" k*gap = {k * (res.fun - vplus):.4f}")
    vd, eta = ref.dual_upper(l, u, phi, f, hR, 2, seed=1)
    print(f"   multi-start minimiser over eta in R^2: value {vd:.10f} (gap {vd - vplus:.2e}) at eta = {np.round(eta, 3)}")
    print("   -> inf_eta tau*(eta) = V+ but it is not attained: at tau = V+ no eta has Psi <= 0; the statement"
          " 'V+ = inf{tau : exists eta, Psi <= 0}' is an infimum, not a minimum, and a dual optimiser sees |eta| -> infinity")


def check_b_at_every_tau():
    """4.1(b), first sentence, at arbitrary tau (not only at the root), box regions, including Z_l = 0:
    inf_eta Psi(tau, eta) = max{M_f - tau M_0 : M in K, M_phi in M_0 R}  (both sides are linear programmes)."""
    from scipy.optimize import linprog
    worst = 0.0
    cases = 0
    minus_inf_ok = 0
    for _ in range(300):
        N = int(rng.integers(3, 8))
        m = int(rng.integers(1, 3))
        kind = rng.choice(["generic", "l=0", "l=u somewhere", "l=0 somewhere"])
        l, u, phi, f = gen(N, m, kind, rng)
        y = reachable_point(l, u, phi, rng) + (rng.uniform(-0.8, 0.8, m) if rng.random() < 0.3 else 0.0)
        half = rng.uniform(0.0, 0.15, m)
        ylo, yhi = y - half, y + half
        tau = float(rng.uniform(-1.5, 1.5))
        # right-hand side: max over w in [l, u] of sum w (f - tau), s.t. ylo sum w <= sum w phi <= yhi sum w
        rows = np.vstack([(phi - yhi).T, (ylo - phi).T])
        res = linprog(-(f - tau), A_ub=rows, b_ub=np.zeros(2 * m), bounds=list(zip(l, u)), method="highs")
        rhs = -res.fun if res.status == 0 else -np.inf
        # left-hand side: inf over eta of Psi(tau, eta) as a linear programme in (eta+, eta-, a, b)
        nv = 2 * m + 2 * N
        obj = np.r_[np.zeros(2 * m), u, -l]
        A_eq = np.zeros((N, nv))
        for x in range(N):
            A_eq[x, :m] = phi[x] - yhi
            A_eq[x, m:2 * m] = -(phi[x] - ylo)
            A_eq[x, 2 * m + x] = 1.0
            A_eq[x, 2 * m + N + x] = -1.0
        res2 = linprog(obj, A_eq=A_eq, b_eq=f - tau, bounds=[(0, None)] * nv, method="highs")
        lhs = res2.fun if res2.status == 0 else (-np.inf if res2.status == 3 else np.nan)
        cases += 1
        if np.isinf(rhs) and np.isinf(lhs):
            minus_inf_ok += 1
            continue
        worst = max(worst, abs(lhs - rhs))
    print(f"[4.1 b] inf_eta Psi(tau, eta) = max over the feasible part of K, at random tau: {cases} instances"
          f" ({minus_inf_ok} with both sides -inf), max abs diff = {worst:.2e}")


def enlargement_at_tangency():
    """Proposition 2.5 says the cost of enlarging R by kappa is at most kappa * inf |eta|_1 over dual certificates,
    'which is finite'.  At a tangency no dual certificate exists at tau = V+ and the cost is of order sqrt(kappa)."""
    l = np.array([0.5, 1.0, 0.5, 0.5])
    u = np.array([1.0, 2.0, 2.0, 2.0])
    phi = np.array([[0.0, 1.0], [0.0, -1.0], [1.0, 0.0], [-1.0, 0.0]])
    f = np.array([0.0, 0.0, 1.0, 0.3])
    ystar = np.array([0.1, 0.0])
    rad = 0.5
    centre = ystar + np.array([0.0, rad])
    A, c = ref.box_region(ystar, ystar)
    v0 = ref.primal_extreme(l, u, phi, f, A, c, +1)
    print("[2.5 at a tangency] the disc instance above, region enlarged by kappa in l_inf:")
    for kappa in (1e-2, 1e-3, 1e-4, 1e-5):
        hR = lambda e, kappa=kappa: ref.h_ball(e, centre, rad) + kappa * float(np.abs(e).sum())
        starts = [np.array([0.13, -k]) for k in (1.0, 10.0, 100.0, 1000.0)] + [np.zeros(2)]
        v, eta = ref.dual_upper(l, u, phi, f, hR, 2, starts=starts)
        print(f"      kappa = {kappa:.0e}: V+(R + kappa B) - V+ = {v - v0:.3e}   ratio to kappa = {(v - v0) / kappa:8.1f}"
              f"   ratio to sqrt(kappa) = {(v - v0) / np.sqrt(kappa):.3f}   |eta|_1 at the optimum = {np.abs(eta).sum():.1f}")


if __name__ == "__main__":
    check_m0_threshold()
    check_b_at_every_tau()
    check_completeness()
    counterexample_c()
    counterexample_e()
    nonattainment()
    enlargement_at_tangency()
