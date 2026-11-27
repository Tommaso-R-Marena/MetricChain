#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- Corollary 11.91: the inequalities, with ALL exits (also those that change the type).

For an exchangeable known part with rate function I (of the type), a landscape lam (u-Lipschitz, lam <= I, touching)
and a two-block profile mu = (m; a, b) of type kappa = m a + (1-m) b:
    r_mu(e) = min{ MI(nu) : u dist(nu, mu) + lam(nu-bar) <= e + MI(mu) + I(kappa) },    nu = (a', b') in [0,1]^2
(Lemma 11.77(b): for lam = v one may put I in place of v.)  Corollary 11.91 claims
    r_mu(e) <= r^kappa_mu(e + (I - lam)(kappa)) <= R^kappa(e + (I-lam)(kappa)) <= R_unif(e).
Checks (own code; the inner minimum is a dense 2-D grid followed by SLSQP polishing from the best grid points;
a grid alone is biased UPWARD, which can only produce false violations, never hide one):
 (C1) the chain on random profiles for four rate functions: a field p = 0.3; Curie-Weiss beta J = 1.5 (two phases);
      an antiferromagnet beta J = -2; Curie-Weiss beta J = 0.8 with a field beta B = 0.1 -- landscapes v (flat histogram) and 0;
 (C2) "what the corollary does not say", field p = 0.3, u = 1: the true sup over binary centres of r_mu(0) (flat-histogram
      landscape) is 0.025034 (claimed), the slice bound is 0.029139; the same number from the vertex-channel formula of
      Theorem 11.99 (new checkpoint), an independent route;
 (C3) two phases, beta J = 1.5: r_mu(0) at the barrier shell x = 0.29803 of a centre of type 1/2 is 0.0251012 (claimed);
 (C4) equality case (ii): symmetric convex rate function (beta J = -2 and beta J = 0.8, B = 0): r_mu(e) of the cube's optimal
      profile equals R_unif(e).
Run:  python3 corollary_1191_checks.py
"""
import math
import sys

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from thm_1190 import Ray, best_centre, R_unif, Psi_c

rng = np.random.default_rng(1191)
EPS = 1e-300


def hb(x):
    x = np.clip(x, 0.0, 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return -(np.where(x > 0, x * np.log(np.maximum(x, EPS)), 0.0) + np.where(x < 1, (1 - x) * np.log(np.maximum(1 - x, EPS)), 0.0))


class Rate:
    """rate function I = phi - h - min(phi - h) of the type, its largest u-Lipschitz minorant v"""

    def __init__(self, phi, u, n=20001):
        self.phi, self.u = phi, u
        self.grid = np.linspace(0.0, 1.0, n)
        raw = phi(self.grid) - hb(self.grid)
        r = minimize_scalar(lambda k: float(phi(np.array([k]))[0] - hb(np.array([k]))[0]), bounds=(1e-9, 1 - 1e-9), method="bounded",
                            options={"xatol": 1e-14})
        # global minimum: grid, then polish around the best grid point
        i = int(np.argmin(raw))
        lo, hi = self.grid[max(i - 1, 0)], self.grid[min(i + 1, n - 1)]
        r = minimize_scalar(lambda k: float(phi(np.array([k]))[0] - hb(np.array([k]))[0]), bounds=(lo, hi), method="bounded",
                            options={"xatol": 1e-15})
        self.minval = min(r.fun, raw[i])
        self.Igrid = raw - self.minval
        # v on the grid: v = min_k' [I(k') + u |k - k'|]  (two sweeps)
        v = self.Igrid.copy()
        step = self.u * (self.grid[1] - self.grid[0])
        for j in range(1, n):
            v[j] = min(v[j], v[j - 1] + step)
        for j in range(n - 2, -1, -1):
            v[j] = min(v[j], v[j + 1] + step)
        self.vgrid = v

    def I(self, k):
        k = np.asarray(k, float)
        return self.phi(k) - hb(k) - self.minval

    def v(self, k):
        return np.interp(k, self.grid, self.vgrid)


def MI2(m, a, b):
    k = m * a + (1 - m) * b
    return hb(k) - m * hb(a) - (1 - m) * hb(b)


def r_general(rate, lam, m, a, b, e, u, ngrid=601, polish=6):
    """min{MI(nu): u dist(nu,mu) + lam(nu-bar) <= e + MI(mu) + I(kappa)} over nu in [0,1]^2.
    lam = 'v' uses I in place of v (Lemma 11.77(b)); lam = '0' is the zero residual.
    Solver: dense grid; then, from the best feasible grid points AND from the profile itself, one smooth SLSQP problem per
    sign pattern of (a'-a, b'-b) (the constraint has kinks there); then successive zooms around the best point found.
    (First version: grid + plain SLSQP, and it returned MI(mu) whenever no grid point was feasible -- for profiles with a
    tiny budget this over-estimated the minimum and produced two false 'violations' of Corollary 11.91; see NOTES.)"""
    kappa = m * a + (1 - m) * b
    budget = e + float(MI2(m, a, b)) + float(rate.I(kappa))
    L = (lambda k: rate.I(k)) if lam == "v" else (lambda k: 0.0 * np.asarray(k))
    Ls = lambda k: float(L(np.array(k)))
    if Ls(kappa) > budget + 1e-15:
        self_feasible = False
    else:
        self_feasible = True
    g = np.linspace(0.0, 1.0, ngrid)
    A, B = np.meshgrid(g, g, indexing="ij")
    cons = u * (m * np.abs(A - a) + (1 - m) * np.abs(B - b)) + L(m * A + (1 - m) * B)
    feas = cons <= budget
    obj = np.where(feas, MI2(m, A, B), np.inf)
    starts = []
    best = math.inf
    bestz = None
    if feas.any():
        idx = np.argsort(obj, axis=None)[:polish]
        starts += [np.array([A.flat[i], B.flat[i]]) for i in idx if np.isfinite(obj.flat[i])]
        i = int(np.argmin(obj))
        best, bestz = float(obj.flat[i]), np.array([A.flat[i], B.flat[i]])
    if self_feasible:
        starts.append(np.array([a, b]))
        if float(MI2(m, a, b)) < best:
            best, bestz = float(MI2(m, a, b)), np.array([a, b])
    if not starts:
        return -math.inf

    def f(z):
        return float(MI2(m, z[0], z[1]))

    for sa in (+1, -1):
        for sb in (+1, -1):
            bnds = [((a, 1.0) if sa > 0 else (0.0, a)), ((b, 1.0) if sb > 0 else (0.0, b))]

            def c(z, sa=sa, sb=sb):
                return budget - (u * (m * sa * (z[0] - a) + (1 - m) * sb * (z[1] - b)) + Ls(m * z[0] + (1 - m) * z[1]))

            for z0 in starts:
                z0c = np.array([min(max(z0[0], bnds[0][0]), bnds[0][1]), min(max(z0[1], bnds[1][0]), bnds[1][1])])
                try:
                    res = minimize(f, z0c, method="SLSQP", bounds=bnds, constraints=[{"type": "ineq", "fun": c}],
                                   options={"ftol": 1e-16, "maxiter": 400})
                    if c(res.x) >= -1e-12 and f(res.x) < best:
                        best, bestz = f(res.x), np.array(res.x)
                except Exception:
                    pass
    # zooms (derivative free) around the best point found
    w = 2.0 / (ngrid - 1)
    for _ in range(8):
        ga = np.clip(np.linspace(bestz[0] - w, bestz[0] + w, 41), 0, 1)
        gb = np.clip(np.linspace(bestz[1] - w, bestz[1] + w, 41), 0, 1)
        AA, BB = np.meshgrid(ga, gb, indexing="ij")
        cz = u * (m * np.abs(AA - a) + (1 - m) * np.abs(BB - b)) + L(m * AA + (1 - m) * BB)
        oz = np.where(cz <= budget, MI2(m, AA, BB), np.inf)
        j = int(np.argmin(oz))
        if np.isfinite(oz.flat[j]) and float(oz.flat[j]) < best:
            best, bestz = float(oz.flat[j]), np.array([AA.flat[j], BB.flat[j]])
        w /= 4
    return max(best, 0.0)


def r_slice(m, a, b, e_eff, u):
    """r^kappa_mu(e_eff) for the two-block profile: exits on the ray of type kappa (one-dimensional, exact)"""
    kappa = m * a + (1 - m) * b
    ray = Ray(m, kappa)
    l = 2 * m * (a - kappa)
    return ray.r_shell(l, e_eff, u)


def cw(bJ, bB=0.0):
    return lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)


def field(p):
    # f = -sum x_i logit p ... : phi(k) = -k ln p - (1-k) ln(1-p)  =>  I(k) = KL(k || p)
    return lambda k: -k * math.log(p) - (1 - k) * math.log(1 - p)


ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    sys.stdout.flush()


def main():
    u = 1.0
    models = {"field p=0.3": field(0.3), "CW bJ=1.5 (two phases)": cw(1.5), "antiferro bJ=-2": cw(-2.0),
              "CW bJ=0.8, bB=0.1": cw(0.8, 0.1)}
    rates = {k: Rate(f, u) for k, f in models.items()}

    # ---------------- (C1) the chain of inequalities ----------------
    worst1 = worst2 = worst3 = -math.inf
    n = 0
    for name, rate in rates.items():
        for lam in ("v", "0"):
            for _ in range(18):
                m = float(rng.uniform(0.1, 0.9))
                a = float(rng.uniform(0.05, 0.95))
                b = float(rng.uniform(0.05, 0.95))
                if a < b:
                    a, b = b, a
                kappa = m * a + (1 - m) * b
                e = float(rng.choice([0.0, 0.0, 0.01, 0.03, -0.01]))
                lamk = float(rate.v(kappa)) if lam == "v" else 0.0
                gap = float(rate.I(kappa)) - lamk                 # (I - lam)(kappa) >= 0
                if lam == "0" and gap < 0:
                    continue
                rg = r_general(rate, lam, m, a, b, e, u, ngrid=401)
                if rg == -math.inf:
                    continue
                rs = r_slice(m, a, b, e + gap, u)
                e_eff = e + gap
                Rk = best_centre(kappa, u, e_eff, "V")[0] if e_eff >= 0 else max(
                    Ray(float(mm), kappa).V_game(e_eff, u) for mm in np.linspace(0.02, 0.98, 97))
                Ru = R_unif(e, u) if e >= -0.11 else None
                worst1 = max(worst1, rg - rs)
                worst2 = max(worst2, rs - Rk)
                if Ru is not None:
                    worst3 = max(worst3, Rk - Ru)
                n += 1
    report("(C1) chain", worst1 <= 1e-8 and worst2 <= 1e-9 and worst3 <= 1e-9,
           f"{n} random two-block profiles x 4 rate functions x landscapes (v, 0): max[r_mu(e) - r^kappa_mu(e+(I-lam)(kappa))] = {worst1:.2e}; "
           f"max[r^kappa_mu - R^kappa] = {worst2:.2e}; max[R^kappa(e+(I-lam)(kappa)) - R_unif(e)] = {worst3:.2e}  (all must be <= 0 up to solver tolerance)")

    # ---------------- (C2) the field p = 0.3 ----------------
    rate = rates["field p=0.3"]

    def neg(z):
        m, a, b = 1 / (1 + math.exp(-z[0])), 1 / (1 + math.exp(-z[1])), 1 / (1 + math.exp(-z[2]))
        v = r_general(rate, "v", m, a, b, 0.0, u, ngrid=201, polish=3)
        return -v if v > -math.inf else 1.0

    best = (-1, None)
    for s in range(6):
        z0 = rng.normal(0, 1.0, 3)
        res = minimize(neg, z0, method="Nelder-Mead", options={"maxiter": 220, "xatol": 1e-6, "fatol": 1e-10})
        if -res.fun > best[0]:
            best = (-res.fun, res.x)
    m, a, b = [1 / (1 + math.exp(-t)) for t in best[1]]
    val = r_general(rate, "v", m, a, b, 0.0, u, ngrid=801, polish=8)
    # the vertex-channel formula (Theorem 11.99): two letters, pi = (0.7, 0.3) or (0.3, 0.7), vertices u*1_{0}, u*1_{1}
    from remark_v2_sites import vertex_laws, h_value
    P, _ = vertex_laws([0.7, 0.3], u)
    h_renyi = h_value(P, ngrid=80)[0]
    slice_bound = max(best_centre(float(k), u, float(rate.I(k) - rate.v(k)), "V")[0] for k in np.linspace(0.05, 0.95, 91))
    report("(C2) field p=0.3, u=1", abs(val - 0.025034) < 3e-6 and abs(h_renyi - 0.025034) < 6e-7 and abs(slice_bound - 0.029139) < 1e-6,
           f"sup over binary centres of r_mu(0) with all exits (multistart search) = {val:.6f} at (m,a,b)=({m:.4f},{a:.4f},{b:.4f}), type "
           f"{m * a + (1 - m) * b:.4f}; vertex-channel formula h = {h_renyi:.6f}; claimed 0.025034; slice bound sup_kappa R^kappa((I-v)(kappa)) = {slice_bound:.6f} (claimed 0.029139)")

    # ---------------- (C3) two phases ----------------
    rate = rates["CW bJ=1.5 (two phases)"]
    x = 0.29803
    val = r_general(rate, "v", 0.5, 1 - x, x, 0.0, u, ngrid=1201, polish=12)
    # local maximality in x
    vals = [(xx, r_general(rate, "v", 0.5, 1 - xx, xx, 0.0, u, ngrid=801, polish=8)) for xx in (0.288, 0.293, 0.29803, 0.303, 0.308)]
    report("(C3) CW bJ=1.5, barrier shell", abs(val - 0.0251012) < 3e-6,
           f"r_mu(0) at (m; a, b) = (1/2; 1-x, x), x = 0.29803: {val:.7f} (claimed 0.0251012); neighbours: "
           + ", ".join(f"x={xx}: {vv:.7f}" for xx, vv in vals) + f"; I(1/2) = {float(rate.I(0.5)):.4f} (claimed barrier 0.1152)")

    # ---------------- (C4) equality for symmetric convex rate functions ----------------
    worst = 0.0
    for name in ("antiferro bJ=-2",):
        rate = rates[name]
        for e in (0.0, 0.01, 0.04):
            lstar = 0.5 * math.tanh(u / 2)
            val = r_general(rate, "v", 0.5, 0.5 + lstar, 0.5 - lstar, e, u, ngrid=801, polish=8)
            worst = max(worst, abs(val - R_unif(e, u)))
    rate08 = Rate(cw(0.8), u)
    for e in (0.0, 0.02):
        lstar = 0.5 * math.tanh(u / 2)
        val = r_general(rate08, "v", 0.5, 0.5 + lstar, 0.5 - lstar, e, u, ngrid=801, polish=8)
        worst = max(worst, abs(val - R_unif(e, u)))
    report("(C4) equality (ii)", worst < 3e-7,
           f"antiferromagnet bJ=-2 and ferromagnet bJ=0.8 (B=0): |r_mu(e) - R_unif(e)| <= {worst:.1e} at the cube's optimal profile "
           f"(m=1/2, shell l*), e in (0, .01, .04 / 0, .02), exits of every type allowed")
    # ---------------- (C5) case (iii): the junction of Proposition 11.81(b), also for a larger slope ----------------
    # beta J*(e,u) = 1 + u c2/(2L), rho = (Lambda_1 + e)/u, c2 = 1/(2 rho (1-rho)) - 2, L = ln((1-rho)/rho).
    # Corollary 11.91(iii) (5ed4072): R_H = R_unif "with two phases up to the junction beta J*" (local statement proved, global
    # numerical).  The new checkpoint reports from referee R10 that for larger slopes the junction comes earlier.
    # Test: r_mu(0) with ALL exits at the cube's optimal profile (the only profile at which a slice attains R_unif).
    print("      (C5) Curie-Weiss, B = 0: r_mu(0) at the cube's optimal profile against R_unif(0)")
    rows = []
    for uu in (1.0, 3.0):
        Lam1 = math.log(2 / (1 + math.exp(-uu)))
        rho = Lam1 / uu
        bJstar = 1 + uu * (1 / (2 * rho * (1 - rho)) - 2) / (2 * math.log((1 - rho) / rho))
        lstar = 0.5 * math.tanh(uu / 2)
        for frac in (0.5, 0.8, 0.95, 1.05):
            bJ = 1 + frac * (bJstar - 1)
            rt = Rate(cw(bJ), uu)
            contact = abs(float(rt.I(0.5)) - float(rt.v(0.5))) < 1e-9
            val = r_general(rt, "v", 0.5, 0.5 + lstar, 0.5 - lstar, 0.0, uu, ngrid=801, polish=10)
            rows.append((uu, bJstar, bJ, val, R_unif(0.0, uu), contact))
            print(f"        u={uu}: bJ* = {bJstar:.4f}; bJ = {bJ:.4f} ({frac:.2f} of the way): r_mu(0) = {val:.7f}, R_unif(0) = {R_unif(0.0, uu):.7f}, "
                  f"difference {val - R_unif(0.0, uu):+.2e}; 1/2 a contact type: {contact}")
    # expected at u = 1: equality below bJ*, strict inequality above (as the report says)
    u1 = [r for r in rows if r[0] == 1.0]
    ok5 = all(abs(r[3] - r[4]) < 1e-7 for r in u1[:3]) and (u1[3][3] < u1[3][4] - 1e-7)
    u3 = [r for r in rows if r[0] == 3.0]
    early = [r for r in u3[:3] if r[3] < r[4] - 1e-6]
    report("(C5) junction", ok5,
           "u = 1: equality for bJ < bJ* and strict inequality just above, as stated; u = 3: "
           + (f"the profile already loses the exponent BELOW bJ* (first at bJ = {early[0][2]:.4f} < bJ* = {early[0][1]:.4f}): the global half of "
              "Proposition 11.81(b), hence Corollary 11.91(iii) as worded at 5ed4072, fails for this slope (consistent with referee R10 as "
              "reported at 89ac710)" if early else "no early junction found on this grid"))
    print()
    print("SUMMARY:", "ALL PASS" if ok_all else "FAILURES")


if __name__ == "__main__":
    main()
