#!/usr/bin/env python3
"""r26_n12.py -- workstream R26, Item 2: Proposition N12 (the false certificate under unbounded influence).

Usage:  python3 -B r26_n12.py <block> [runs]
   abc      the statements (a)-(c): closed forms against enumeration, the numbers of the text
   assumed  Algorithm A with the tail function of the ASSUMED class (Harper, slope u), theta in {20, 1}, several
            parameter sets; counts invalid brackets and locates the false inference
   scan     the same over a range of thresholds theta (where does the false certificate stop?)
   true     Algorithm A with the tail function of the TRUE class of V (Harper, slope = largest edge ratio)
   control  the same algorithm, the same tail function of the assumed class, on a PRODUCT known part with
            integrands that are in the class; and two mutations that must make this control fail

The instance (N_REPORT 5.2): outer cube Q_m with uniform marginal, inner cube Q_k with the conditional law
Bernoulli(p(a))^k, p(a) = sigma(J (tau - |a|)); residual psi(a,b) = u |b|.  m=12, k=16, u=1, J=4, tau=10.5.
The inner procedures are a simulated oracle (valid brackets of the promised ratio around the exact V(a)); this is
the same restriction as in N_REPORT 7.3 -- not an end-to-end run.
"""
import math
import sys
import time

import numpy as np

import r26_alg as A

M_, K_, U_, J_, TAU_ = 12, 16, 1.0, 4.0, 10.5


def sigma(x):
    return 1.0 / (1.0 + np.exp(-x))


def instance(m=M_, k=K_, u=U_, J=J_, tau=TAU_):
    pts = np.arange(1 << m)
    wt = np.array([bin(int(a)).count("1") for a in pts])
    p = sigma(J * (tau - wt))
    V = (1 - p + p * math.exp(-u)) ** k
    mu = np.full(1 << m, 1.0 / (1 << m))
    return wt, p, V, mu


def reference_data(wt, p, V, mu, m=M_, k=K_, u=U_):
    """Valid reference data for the class L_u(Q_{m+k}) under the TRUE (dependent) measure, reference point 0:
    ell0 = e^{-psi(0)} E e^{-u d(x,0)} = sum_a mu(a) e^{-u|a|} E[e^{-u|b|} | a];
    Vmax = max_a e^{u|a|} E[e^{u|b|} | a]   (psi(a,b) >= psi(0) - u|a| - u|b| and psi(0) = 0)."""
    ell0 = float((mu * np.exp(-u * wt) * V).sum())
    Vmax = float((np.exp(u * wt) * (1 - p + p * math.exp(u)) ** k).max())
    return ell0, Vmax


def block_abc():
    m, k, u, J, tau = M_, K_, U_, J_, TAU_
    wt, p, V, mu = instance()
    viol = 0
    # (b) closed form of V against enumeration of the 65536 inner points under Bernoulli(p)^k
    binner = np.arange(1 << k)
    wb = np.array([bin(int(b)).count("1") for b in binner])
    worst = 0.0
    for w in range(m + 1):
        pw = sigma(J * (tau - w))
        prob = pw ** wb * (1 - pw) ** (k - wb)
        Vb = float((prob * np.exp(-u * wb)).sum())
        Vc = (1 - pw + pw * math.exp(-u)) ** k
        worst = max(worst, abs(Vb - Vc) / Vc)
    print(f"(b) V(a) = (1 - p + p e^-u)^k against enumeration of Q_{k}: largest relative difference {worst:.2e}")
    viol += worst > 1e-10
    c = math.log((1 - sigma(-J / 2) * (1 - math.exp(-u))) / (1 - sigma(J / 2) * (1 - math.exp(-u))))
    lnV = np.log(V)
    # largest edge ratio on the outer cube (V depends on |a| only: edges join weights w and w+1)
    Vw = np.array([(1 - sigma(J * (tau - w)) + sigma(J * (tau - w)) * math.exp(-u)) ** k for w in range(m + 1)])
    edge = np.abs(np.diff(np.log(Vw)))
    print(f"    c(J,u) = {c:.6f};  k c = {k * c:.4f};  largest edge ratio ln = {edge.max():.4f} "
          f"(between |a| = {int(edge.argmax())} and {int(edge.argmax()) + 1});  text: e^11.77")
    viol += abs(edge.max() - k * c) > 1e-9
    print("    V by weight |a| = 8..12: " + "  ".join(f"{Vw[w]:.4e}" for w in range(8, 13)))
    Atot = float((mu * V).sum())
    spike = float((mu * V)[wt >= 11].sum())
    print(f"    A = {Atot:.6e} (text 1.0747e-3);  share of the 13 points with |a| >= 11: {100 * spike / Atot:.4f} %;  "
          f"bulk max (|a| <= 9) = {Vw[:10].max():.3e} (text 1.2e-7)")
    viol += abs(Atot - 1.0747e-3) > 1e-7
    # influences per outer flip
    pt_thr = k * max(math.log(sigma(J / 2) / sigma(-J / 2)), math.log((1 - sigma(-J / 2)) / (1 - sigma(J / 2))))
    p1, p2 = sigma(J * (tau - 3)), sigma(J * (tau - 4))
    q1, q2 = sigma(J * (tau - 12)), sigma(J * (tau - 11))
    pt_away = k * max(abs(math.log(q1 / q2)), abs(math.log((1 - q1) / (1 - q2))))
    print(f"    pointwise influence per outer flip: at the threshold {pt_thr:.3f} (= kJ/2 = {k * J / 2:.1f}); between "
          f"|a| = 11 and 12: {pt_away:.3f} (kJ = {k * J:.1f});  class-relative (u-Lipschitz): k c = {k * c:.3f}")
    # (c) (TU) with Harper's function of the assumed class: worst ratio over all levels
    H = A.HarperCube(m, u)
    S = A.SharpestTails(mu, V)
    worst_tu, where = 0.0, None
    for i, v in enumerate(S.vals[:-1]):
        q = S.above[i]
        if q <= 0 or q >= 1:
            continue
        ratio = S.excess[i] / (v * H.Xi(q))
        if ratio > worst_tu:
            worst_tu, where = ratio, (v, q)
    print(f"(c) (TU) for the slope u: largest E(V-s)_+ / (s Xi_u(p(s))) = {worst_tu:.4e} at s = {where[0]:.3e}, "
          f"p(s) = {where[1] * 4096:.0f}/4096   (text: 1.7e5)")
    viol += not (1.6e5 < worst_tu < 1.8e5)
    suff = k * c > u * (m - tau + 0.5)
    print(f"    sufficient condition k c > u (m - tau + 1/2): {k * c:.3f} > {u * (m - tau + 0.5):.3f}: {suff}")
    # the same for the Harper function of the true slope: must hold
    Ht = A.HarperCube(m, edge.max())
    worst_true = max(S.excess[i] / (v * Ht.Xi(S.above[i])) for i, v in enumerate(S.vals[:-1])
                     if 0 < S.above[i] < 1)
    print(f"    with Harper's function of the slope {edge.max():.3f}: largest ratio {worst_true:.4f} (must be <= 1)")
    viol += worst_true > 1 + 1e-9
    # (a) psi(a,b) = u|b| is in L_u(Q_{m+k}): one flip changes it by u or 0 -- nothing to compute.
    print(f"abc violations: {viol}")
    return viol


PARAM_SETS = {
    "P0 (lam=1, eta=1/2, b=0.5, delta=0.05)": dict(),
    "P1 (b=1)": dict(b=1.0, x=(32.0, 4.0, 1.0)),
    "P2 (b=0.25)": dict(b=0.25, x=(32.0, 2.0, 0.25)),
    "P3 (lam=0.5)": dict(lam=0.5),
    "P4 (eta=0.3)": dict(eta=0.3),
    "P5 (delta=0.001)": dict(delta=0.001),
    "P6 (kappa0=0.05)": dict(kappa0=0.05),
}


def make_params(theta, **kw):
    base = dict(lam=1.0, eta=0.5, etap=1.0, theta=theta, nu1=1.0, b=0.5, delta=0.05, kappa0=1.0,
                x=(32.0, 2.0, 0.5), C=(1.0, 1.0, 1.0), c_ref=1.0)
    base.update(kw)
    return A.Params(**base)


class ThetaId:
    """Harper's upper tail function with the Markov lower tail function Theta = id (no "Harper term")."""

    def __init__(self, H):
        self.H = H

    def Xi(self, q):
        return self.H.Xi(q)

    def Theta(self, p):
        return p


def closing_level_steps(H, Theta, theta, eta, nu0):
    """Closing level for Harper's Xi (a step function) and an arbitrary nondecreasing right-continuous Theta."""
    c = (1 - eta) / (1 + eta)
    best = 1.0 / H.size
    for r in range(0, H.m):
        qleft = (H.ball[r - 1] if r >= 1 else 1.0) / H.size
        xi = H.E[r] / H.size
        if xi <= theta * (1 - eta) * nu0 * qleft and xi <= theta * max(c * qleft, Theta(c * qleft)):
            best = H.ball[r] / H.size
        else:
            break
    return best


def run_many(P, V, mu, tails, ell0, Vmax, runs, seed0, placement="random", pi_star=None, Hc=None):
    cst0 = A.constants(P, ell0, 1.0, Vmax=Vmax)             # J and nu0 do not depend on pi_star
    if pi_star is None:
        pi_star = closing_level_steps(Hc, tails.Theta, P.theta, P.eta, cst0["nu0"])
    n = len(V)
    out = []
    for r in range(runs):
        rng = np.random.default_rng(seed0 + r)
        rec = A.run_A(P, V, lambda k_: rng.integers(0, n, k_), tails.Xi, tails.Theta, ell0, pi_star, rng,
                      Vmax=Vmax, placement=placement)
        chk = A.check_run(rec, P, mu, V)
        chk["close"] = rec["close"]
        chk["nspike"] = None
        out.append(chk)
    return out, pi_star, A.constants(P, ell0, pi_star, Vmax=Vmax)


def summarise(res, label, A_true, wt=None):
    n = len(res)
    inval = sum(not r["valid"] for r in res)
    aborts = sum(r["stop"] == "abort" for r in res)
    below = [A_true / r["U"] for r in res if r["U"] < A_true]
    med_pts = int(np.median([r["points"] for r in res]))
    f = lambda key: sum(not r[key] for r in res)
    line = (f"  {label}: runs {n}; INVALID {inval}; aborts {aborts}; median outer points {med_pts}; "
            f"false certificates: q {f('cert_q')}, plow {f('cert_p')}, ell {f('cert_ell')}, TAIL {f('cert_tail')}; "
            f"Chernoff events failed {f('chernoff')}; width violated {f('width')}")
    if below:
        line += f"; A/U among runs with U < A: median {np.median(below):.0f} (min {min(below):.0f}, max {max(below):.0f})"
    reasons = {}
    for r in res:
        if r["stop"] == "abort":
            reasons[r["abort"]] = reasons.get(r["abort"], 0) + 1
    if reasons:
        line += f"; abort reasons {reasons}"
    above = [r["L"] / A_true for r in res if r["L"] > A_true]
    if above:
        line += (f"; L/A among the {len(above)} runs with L > A: median {np.median(above):.2f} "
                 f"(min {min(above):.2f}, max {max(above):.2f})")
    print(line)
    return inval


def block_assumed(runs):
    wt, p, V, mu = instance()
    ell0, Vmax = reference_data(wt, p, V, mu)
    H = A.HarperCube(M_, U_)
    Atot = float((mu * V).sum())
    print(f"assumed class: Harper's tail functions for slope u = {U_} on Q_{M_}; ell0 = {ell0:.3e}, Vmax = {Vmax:.3e}, "
          f"A = {Atot:.6e}")
    print(f"seeds: run r of a cell uses numpy default_rng(100000*cell + r), r = 0..{runs - 1}; cells numbered in order")
    cell = 0
    total_valid_runs = 0
    for theta in (20.0, 1.0):
        print(f" theta = {theta}")
        for name, kw in PARAM_SETS.items():
            P = make_params(theta, **kw)
            res, pi_star, cst = run_many(P, V, mu, H, ell0, Vmax, runs, 100000 * cell, Hc=H)
            cell += 1
            inval = summarise(res, f"{name:40s} K={cst['K']} J={cst['J']} x_out={cst['x_out']:.2f} "
                                   f"pi*={pi_star:.2e}", Atot)
            total_valid_runs += len(res) - inval
            # where the runs closed
            js = [r["close"]["j"] for r in res if r["close"]]
            ss = [r["close"]["s"] for r in res if r["close"]]
            Ms = [r["close"]["M"] for r in res if r["close"] and r["close"]["M"]]
            Ns = [r["close"]["N"] for r in res if r["close"] and r["close"]["N"] is not None]
            pops = sum(bool(r["close"].get("populated")) for r in res if r["close"])
            print(f"      closing level s_j: median {np.median(ss):.3e} (bulk max 1.2e-7, layer |a|=10: 2.2e-6, spike "
                  f">= 0.2855); closing pass M: median {int(np.median(Ms)) if Ms else None}, N high: median "
                  f"{int(np.median(Ns)) if Ns else None}; closing pass populated in {pops} runs")
    print(f"assumed: number of VALID runs over all cells: {total_valid_runs}")
    return 0


def block_scan(runs):
    wt, p, V, mu = instance()
    ell0, Vmax = reference_data(wt, p, V, mu)
    H = A.HarperCube(M_, U_)
    Atot = float((mu * V).sum())
    thetas = (100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.5, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02)
    print("scan over theta, parameter set P0, assumed class: Harper's UPPER tail function of slope 1, with")
    print(" (i) Harper's LOWER tail function of slope 1 (the 'Harper term' of Theorem 11.56 / Algorithm A)")
    print(f" seeds: default_rng(700000 + 1000*i + r), i = index of theta, r = 0..{runs - 1}")
    for i, theta in enumerate(thetas):
        P = make_params(theta)
        res, pi_star, cst = run_many(P, V, mu, H, ell0, Vmax, runs, 700000 + 1000 * i, Hc=H)
        summarise(res, f"theta={theta:6.2f} K={cst['K']} x_out={cst['x_out']:.2f} pi*={pi_star:.2e}", Atot)
    print(" (ii) the Markov lower tail function Theta = id (always valid; the lower end of Theorem 11.52)")
    print(f" seeds: default_rng(800000 + 1000*i + r)")
    Hid = ThetaId(H)
    nvalid = 0
    for i, theta in enumerate(thetas):
        P = make_params(theta)
        res, pi_star, cst = run_many(P, V, mu, Hid, ell0, Vmax, runs, 800000 + 1000 * i, Hc=H)
        inval = summarise(res, f"theta={theta:6.2f} K={cst['K']} x_out={cst['x_out']:.2f} pi*={pi_star:.2e}", Atot)
        nvalid += len(res) - inval
    print(f"scan: valid runs with Theta = id: {nvalid}")
    return 0


def block_true(runs):
    wt, p, V, mu = instance()
    ell0, Vmax = reference_data(wt, p, V, mu)
    Vw = np.unique(V)
    slope = float(np.abs(np.diff(np.log(np.array([V[wt == w][0] for w in range(M_ + 1)])))).max())
    Ht = A.HarperCube(M_, slope)
    Atot = float((mu * V).sum())
    print(f"true class: Harper's tail functions for the slope {slope:.4f} (largest edge ratio of -ln V)")
    print(f"seeds: default_rng(300000 + 1000*cell + r), r = 0..{runs - 1}")
    v = 0
    for cell, theta in enumerate((20.0, 1.0)):
        P = make_params(theta)
        res, pi_star, cst = run_many(P, V, mu, Ht, ell0, Vmax, runs, 300000 + 1000 * cell, Hc=Ht)
        inval = summarise(res, f"theta={theta} K={cst['K']} pi*={pi_star:.2e} Mbar={cst['Mbar']:.2e}", Atot)
        pts = np.array([r["points"] for r in res])
        print(f"      outer points: median {np.median(pts):.3g}, min {pts.min()}, max {pts.max()}  "
              f"(= {np.median(pts) / 4096:.0f} x the 4096 points of the outer cube);  U/L median "
              f"{np.median([r['U'] / r['L'] for r in res]):.2f}")
        v += inval
    print(f"true-class invalid runs: {v}")
    return v


def lipschitz_majorant(V, u, m):
    """Smallest log-u-Lipschitz majorant on Q_m: max_{a'} V(a') e^{-u d(a,a')}, by m sweeps over coordinates."""
    lnV = np.log(V).copy()
    for _ in range(m):
        for i in range(m):
            flipped = lnV[np.arange(len(V)) ^ (1 << i)]
            lnV = np.maximum(lnV, flipped - u)
    return np.exp(lnV)


def control_instances(rng, m=M_, u=U_):
    pts = np.arange(1 << m)
    pop = np.array([bin(int(a)).count("1") for a in pts])

    def dist(center):
        return np.array([bin(int(a) ^ int(center)).count("1") for a in pts])
    inst = {}
    wt, p, V, mu = instance()
    inst["majorant of the N12 landscape"] = lipschitz_majorant(V, u, m)
    inst["flat (product N12: J = 0, psi = u|b|)"] = np.full(1 << m, ((1 + math.exp(-u)) / 2) ** K_)
    inst["cone e^{-u d(a,1)} x 1e-3"] = 1e-3 * np.exp(-u * dist((1 << m) - 1))
    for R in (1, 2, 4):
        inst[f"Harper-extremal dip, radius {R}"] = np.exp(u * np.maximum(R + 1 - dist(int(rng.integers(1 << m))), 0))
    centers = rng.integers(0, 1 << m, 5)
    inst["mixture of 5 cones"] = sum(math.exp(rng.normal(0, 3)) * np.exp(-u * dist(c)) for c in centers)
    cfield = rng.uniform(-u, u, m)
    bits = ((pts[:, None] >> np.arange(m)[None, :]) & 1)
    inst["random field e^{-c.a}, |c_i| <= u"] = np.exp(-(bits * cfield[None, :]).sum(axis=1))
    noise = np.exp(rng.normal(0, 6, 1 << m))
    inst["majorant of lognormal noise (sd 6)"] = lipschitz_majorant(noise, u, m)
    return inst


def block_control(runs):
    m, u = M_, U_
    H = A.HarperCube(m, u)
    mu = np.full(1 << m, 1.0 / (1 << m))
    rng0 = np.random.default_rng(4242)
    inst = control_instances(rng0)
    print("control: product known part (uniform outer cube), integrands with -ln V u-Lipschitz, the SAME algorithm "
          "and the SAME tail functions (Harper, slope 1) as in the 'assumed' block")
    print(f"seeds: instances from default_rng(4242); run r of cell c uses default_rng(500000 + 1000*c + r), "
          f"r = 0..{runs - 1}")
    viol, cell, nruns = 0, 0, 0
    pts = np.arange(1 << m)
    for name, V in inst.items():
        # membership check (a control of the control): every edge ratio <= e^u
        worst_edge = max(np.abs(np.log(V) - np.log(V[pts ^ (1 << i)])).max() for i in range(m))
        S = A.SharpestTails(mu, V)
        tu = max((S.excess[i] / (v * H.Xi(S.above[i])) for i, v in enumerate(S.vals[:-1]) if 0 < S.above[i] < 1),
                 default=0.0)
        ell0 = float(V[0] * ((1 + math.exp(-u)) / 2) ** m)
        Vmax = float(V[0] * math.exp(u * m))
        Atot = float((mu * V).sum())
        print(f" instance '{name}': largest edge ratio {worst_edge:.4f} (<= u = {u}); largest (TU) ratio {tu:.4f}; "
              f"A = {Atot:.3e}")
        if worst_edge > u + 1e-9 or tu > 1 + 1e-9:
            viol += 1
        for theta in (20.0, 1.0):
            for placement in ("random", "top", "bottom"):
                P = make_params(theta)
                res, pi_star, cst = run_many(P, V, mu, H, ell0, Vmax, runs, 500000 + 1000 * cell,
                                             placement=placement, Hc=H)
                cell += 1
                nruns += len(res)
                inval = sum(not r["valid"] for r in res)
                other = sum((not r["cert_q"]) or (not r["cert_p"]) or (not r["cert_ell"]) or (not r["cert_tail"])
                            or (not r["width"]) or (not r["closing"]) or (not r["sizes"]) or r["stop"] == "abort"
                            for r in res)
                viol += inval + other
                if inval or other:
                    print(f"   theta={theta} placement={placement}: INVALID {inval}, other claim violated {other}")
        print(f"   6 cells x {runs} runs: done")
    print(f"control: {nruns} runs; violations (invalid bracket or any other claim of Theorem N1): {viol}")
    # mutations: the control must be able to fail
    print("mutations on the instance 'Harper-extremal dip, radius 2' and 'cone', theta = 20 and 1:")
    mfail = 0
    for name in ("Harper-extremal dip, radius 2", "cone e^{-u d(a,1)} x 1e-3", "majorant of the N12 landscape"):
        V = inst[name]
        ell0 = float(V[0] * ((1 + math.exp(-u)) / 2) ** m)
        Vmax = float(V[0] * math.exp(u * m))
        Atot = float((mu * V).sum())

        class Mut:
            def __init__(self, f):
                self.f = f

            def Xi(self, q):
                return H.Xi(q) / self.f

            def Theta(self, p):
                return H.Theta(p)
        for theta in (20.0, 1.0):
            for fdiv in (50.0, 1000.0):
                P = make_params(theta)
                res, pi_star, cst = run_many(P, V, mu, Mut(fdiv), ell0, Vmax, runs, 900000 + 1000 * cell, Hc=H)
                cell += 1
                inval = sum(not r["valid"] for r in res)
                mfail += inval
                print(f"   '{name}', theta={theta}, Xi/{fdiv:g}: invalid {inval} of {len(res)}")
            P = make_params(theta, K_override=3)
            res, pi_star, cst = run_many(P, V, mu, H, ell0, Vmax, runs, 900000 + 1000 * cell, Hc=H)
            cell += 1
            inval = sum(not r["valid"] for r in res)
            cq = sum(not r["cert_q"] or not r["cert_p"] for r in res)
            mfail += inval + cq
            print(f"   '{name}', theta={theta}, K = 3 instead of {cst['K_theorem']}: invalid {inval}, false sampling "
                  f"certificates in {cq} of {len(res)} runs")
    print(f"mutations: failures detected {mfail} (the control can fail iff this is > 0)")
    return viol + (0 if mfail > 0 else 1)


def block_hubcube(runs):
    """The remark at the end of N_REPORT 5.2 in ITS OWN setting: the uniform outer cube Q_12 with Harper's functions
    of slope 1, the influence confined to a hub of k0 outer sites: p(a) = sigma(-6) if a_1 = .. = a_k0 = 1, and
    sigma(+6) otherwise (inner cube Q_16, residual u|b| as in Proposition N12)."""
    m, k, u = M_, K_, U_
    pts = np.arange(1 << m)
    wt = np.array([bin(int(a)).count("1") for a in pts])
    mu = np.full(1 << m, 1.0 / (1 << m))
    H = A.HarperCube(m, u)
    Hid = ThetaId(H)
    print("uniform outer cube Q_12, Harper's tail functions of slope 1; influence confined to the first k0 outer "
          "sites (a hub); inner cube Q_16, residual u|b|, u = 1")
    print(f"seeds: default_rng(1100000 + 1000*cell + r), r = 0..{runs - 1}")
    cell = 0
    for k0 in (1, 2, 3, 4, 6):
        hub = (pts & ((1 << k0) - 1)) == ((1 << k0) - 1)
        p = np.where(hub, sigma(-6.0), sigma(6.0))
        V = (1 - p + p * math.exp(-u)) ** k
        ell0, Vmax = reference_data(wt, p, V, mu)
        Atot = float((mu * V).sum())
        S = A.SharpestTails(mu, V)
        tu = max(S.excess[i] / (v * H.Xi(S.above[i])) for i, v in enumerate(S.vals[:-1]) if 0 < S.above[i] < 1)
        tl = max(v * max(S.atleast[i], H.Theta(S.atleast[i])) / S.trunc[i] for i, v in enumerate(S.vals))
        print(f" hub of k0 = {k0} sites: P(hub state) = 2^-{k0} = {2.0 ** -k0:.4f}; ln(V_hub/V_rest) = "
              f"{math.log(V[hub][0] / V[~hub][0]):.2f}; A = {Atot:.3e}; (TU) worst ratio {tu:.3g}, (TL) worst ratio "
              f"{tl:.3g}")
        for theta in (50.0, 20.0, 5.0, 1.0):
            for name, tails in (("Harper upper + Harper lower", H), ("Harper upper + Markov lower", Hid)):
                P = make_params(theta)
                res, pi_star, cst = run_many(P, V, mu, tails, ell0, Vmax, runs, 1100000 + 1000 * cell, Hc=H)
                cell += 1
                summarise(res, f"   theta={theta:5.1f} {name}", Atot)
    return 0


if __name__ == "__main__":
    t0 = time.time()
    block = sys.argv[1] if len(sys.argv) > 1 else "abc"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(f"r26_n12.py block {block} runs {runs}; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    v = dict(abc=block_abc, assumed=lambda: block_assumed(runs), scan=lambda: block_scan(runs),
             true=lambda: block_true(runs), control=lambda: block_control(runs),
             hubcube=lambda: block_hubcube(runs))[block]()
    print(f"exit violations: {v}")
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {A.peak_mb():.0f} MB")
    sys.exit(1 if v else 0)
