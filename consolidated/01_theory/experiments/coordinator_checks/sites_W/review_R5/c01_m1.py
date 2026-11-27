"""M1 numerical checks (own code): (i) v = min_{P'}[I(P') + W(P',P)] = max_gamma v_gamma = I - min_gamma KL(P || pi_gamma);
(ii) the window step; (iii) the evaluation lemma V(mu, B; v) <= Rhat(B - alpha(mu)), with equality at the generalised-dip profile."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize, linprog
import dlib

rng = np.random.default_rng(20261125)
t0 = time.time()
EPS = 1e-300


def kl(p, q):
    p = np.asarray(p, float); q = np.asarray(q, float)
    m = p > 1e-300
    return float((p[m] * np.log(p[m] / q[m])).sum())


def transport(site, Pfirst, Psecond):
    """W(P', P) = min sum kappa(a,b) d(a,b), first marginal P', second marginal P (oriented)."""
    q = site.q
    A = []; b = []
    for a in range(q):
        row = np.zeros((q, q)); row[a, :] = 1; A.append(row.ravel()); b.append(Pfirst[a])
    for c in range(q):
        row = np.zeros((q, q)); row[:, c] = 1; A.append(row.ravel()); b.append(Psecond[c])
    res = linprog(site.d.ravel(), A_eq=np.array(A), b_eq=np.array(b), bounds=[(0, None)] * (q * q), method="highs")
    return res.fun, res.x.reshape(q, q)


def v_primal(site, P):
    """min over couplings kappa with second marginal P of KL(rowsum || pi) + <kappa, d>; returns (value, P'', kappa)."""
    q = site.q

    def f(z):
        k = z.reshape(q, q); r = k.sum(axis=1)
        return float((r * np.log(np.maximum(r, EPS) / site.pi)).sum() + (k * site.d).sum())
    cons = [{"type": "eq", "fun": lambda z: z.reshape(q, q).sum(axis=0) - P}]
    best = None
    for s in range(3):
        z0 = (np.diag(P) if s == 0 else np.outer(rng.dirichlet(np.ones(q)), P)).ravel()
        res = minimize(f, z0, method="SLSQP", bounds=[(0, 1)] * (q * q), constraints=cons, options={"ftol": 1e-15, "maxiter": 2000})
        if best is None or res.fun < best[0]:
            k = res.x.reshape(q, q); best = (float(res.fun), k.sum(axis=1), k)
    return best


def v_dual(site, P):
    """max over gamma in L of -E_P gamma - ln Z_gamma (concave, linear constraints); gamma[0] = 0."""
    q = site.q
    pairs = [(a, b) for a in range(q) for b in range(q) if a != b]

    def f(g):
        g = np.concatenate([[0.0], g])
        return float(P @ g + math.log(float((site.pi * np.exp(-g)).sum())))
    cons = [{"type": "ineq", "fun": (lambda g, a=a, b=b: site.d[a, b] - (np.concatenate([[0.0], g])[a] - np.concatenate([[0.0], g])[b]))} for a, b in pairs]
    res = minimize(f, np.zeros(q - 1), method="SLSQP", constraints=cons, options={"ftol": 1e-15, "maxiter": 2000})
    g = np.concatenate([[0.0], res.x])
    return -float(res.fun), g


print("(i),(ii)  v by two programmes, the distance-to-the-window formula, and the window step")
worst = dict(pd=0.0, formula=0.0, window=0.0, vdrop=0.0, chi2=-1.0)
ncase = 0
for name in ("path", "tri", "asym"):
    site = dlib.Site(*dlib.SITES[name])
    for _ in range(40):
        P = rng.dirichlet(np.ones(site.q) * rng.choice([0.5, 1.0, 3.0]))
        vp, P2, kap = v_primal(site, P)
        vd, g = v_dual(site, P)
        worst["pd"] = max(worst["pd"], abs(vp - vd))
        # formula: I - v = min_gamma KL(P || pi_gamma) = KL(P || pi_g) at the dual optimum
        worst["formula"] = max(worst["formula"], abs((kl(P, site.pi) - vd) - kl(P, dlib.gibbs(site.pi, g))))
        # window step: P'' = first marginal of the optimal coupling is in the window, and v(P'') = I(P'') = v(P) - W(P'',P)
        g2 = -np.log(np.maximum(P2, EPS) / site.pi)
        viol = max(g2[a] - g2[b] - site.d[a, b] for a in range(site.q) for b in range(site.q))
        worst["window"] = max(worst["window"], viol)
        W2 = transport(site, P2, P)[0]
        v2 = v_dual(site, P2)[0]
        worst["vdrop"] = max(worst["vdrop"], abs(v2 - (vp - W2)), abs(v2 - kl(P2, site.pi)))
        # quadratic bound: (I - v)(P) <= chi^2(P || Q) for every Q in the window  (random window members)
        for _ in range(5):
            w = rng.dirichlet(np.ones(len(site.V)))
            Q = dlib.gibbs(site.pi, w @ site.V)
            chi2 = float(((P - Q) ** 2 / Q).sum())
            worst["chi2"] = max(worst["chi2"], (kl(P, site.pi) - vd) - chi2)
            assert Q.min() >= site.pi.min() * math.exp(-site.d.max()) - 1e-12
        ncase += 1
print("   cases", ncase, " |primal - dual| <= %.1e;  |(I - v) - KL(P || pi_gamma*)| <= %.1e;  window violation of P'' <= %.1e;"
      "  |v(P'') - (v(P) - W(P'',P))|, |v(P'') - I(P'')| <= %.1e;  max[(I - v) - chi2(P||Q)] = %.1e (must be <= 0)" %
      (worst["pd"], worst["formula"], worst["window"], worst["vdrop"], worst["chi2"]))
print("   time %.1f s" % (time.time() - t0))


# ---------------------------------------------------------------- (iii) the evaluation lemma, chains with one or two site types
def solve_V(chain, prof, B, starts=3):
    """V(mu, B; v) = min MI(nu) s.t. dist(nu -> mu) + v(nubar) <= B.  chain = [(lam_j, site_j)], prof = [(Pu_j, mu_j)] with
    Pu_j the label weights and mu_j[u] the letter laws.  Variables: couplings kappa_ju (first marginal nu_ju, second mu_ju) and,
    for v(nubar_j) = min[KL(P''||pi) + W(P'', nubar)], couplings kappa''_j (first marginal P''_j, second nubar_j)."""
    shapes = []
    for (lam, site), (Pu, mu) in zip(chain, prof):
        shapes.append((site.q, len(Pu)))
    nvar = sum(q * q * (nu + 1) for q, nu in shapes)

    def unpack(z):
        out = []; pos = 0
        for q, nu in shapes:
            ks = z[pos:pos + q * q * nu].reshape(nu, q, q); pos += q * q * nu
            k2 = z[pos:pos + q * q].reshape(q, q); pos += q * q
            out.append((ks, k2))
        return out

    def MI(z):
        tot = 0.0
        for (lam, site), (Pu, mu), (ks, k2) in zip(chain, prof, unpack(z)):
            nus = ks.sum(axis=2) / Pu[:, None]            # nu_ju = first marginal of kappa_ju (kappa stored with weight P_j(u))
            nbar = (Pu[:, None] * nus).sum(axis=0)
            for u in range(len(Pu)):
                m = nus[u] > 1e-300
                tot += lam * Pu[u] * float((nus[u][m] * np.log(nus[u][m] / np.maximum(nbar[m], EPS))).sum())
        return tot

    def g(z):                                           # B - [dist + v-bound] >= 0
        tot = 0.0
        for (lam, site), (Pu, mu), (ks, k2) in zip(chain, prof, unpack(z)):
            tot += lam * float((ks * site.d[None]).sum())
            r = k2.sum(axis=1)
            tot += lam * (float((r * np.log(np.maximum(r, EPS) / site.pi)).sum()) + float((k2 * site.d).sum()))
        return B - tot

    def eqs(z):
        res = []
        for (lam, site), (Pu, mu), (ks, k2) in zip(chain, prof, unpack(z)):
            for u in range(len(Pu)):
                res.extend(ks[u].sum(axis=0) - Pu[u] * mu[u])          # second marginal of kappa_ju is mu_ju (weighted)
            nbar = ks.sum(axis=(0, 2))
            res.extend(k2.sum(axis=0) - nbar)                           # second marginal of kappa''_j is nubar_j
        return np.array(res)

    best = None
    for s in range(starts):
        z0 = []
        for (lam, site), (Pu, mu) in zip(chain, prof):
            q = site.q
            for u in range(len(Pu)):
                z0.append((np.diag(Pu[u] * mu[u]) if s == 0 else np.outer(rng.dirichlet(np.ones(q)), Pu[u] * mu[u])).ravel())
            nbar = (Pu[:, None] * mu).sum(axis=0)
            vp, P2, kap = v_primal(site, nbar) if s == 0 else (None, None, np.outer(rng.dirichlet(np.ones(q)), nbar))
            z0.append(kap.ravel())
        z0 = np.concatenate(z0)
        res = minimize(MI, z0, method="SLSQP", bounds=[(0, 1)] * nvar,
                       constraints=[{"type": "ineq", "fun": g}, {"type": "eq", "fun": eqs}], options={"ftol": 1e-14, "maxiter": 3000})
        feas = g(res.x) >= -1e-9 and np.abs(eqs(res.x)).max() <= 1e-9
        if feas and (best is None or res.fun < best):
            best = float(res.fun)
    return best


def alpha(chain, prof):
    return sum(lam * sum(Pu[u] * kl(mu[u], site.pi) for u in range(len(Pu))) for (lam, site), (Pu, mu) in zip(chain, prof))


def vbar(chain, prof):
    return sum(lam * v_dual(site, (Pu[:, None] * mu).sum(axis=0))[0] for (lam, site), (Pu, mu) in zip(chain, prof))


print("(iii) evaluation lemma  V(mu, B; v) <= Rhat(B - alpha(mu))  [a pass means: a feasible exit profile with MI <= Rhat + 1e-7 was found]")
chains = {
    "asym": [(1.0, dlib.Site(*dlib.SITES["asym"]))],
    "tri": [(1.0, dlib.Site(*dlib.SITES["tri"]))],
    "mix(bin,path)": [(0.5, dlib.Site(*dlib.SITES["bin"])), (0.5, dlib.Site(*dlib.SITES["path"]))],
    "asym/tri 0.3/0.7": [(0.3, dlib.Site(*dlib.SITES["asym"])), (0.7, dlib.Site(*dlib.SITES["tri"]))],
}
tot = viol = 0; worst_excess = -1.0; closest = -1.0; nontriv = 0; gaps = []; negacc = 0
for cname, chain in chains.items():
    E = sum(l * dlib.E_site(s) for l, s in chain)
    # (A) tightness at the generalised-dip profile for e = 0.3 E
    e = 0.3 * E
    R, tstar = dlib.Rhat(chain, e)
    prof = []
    for lam, site in chain:
        val, up, M, Q = dlib.renyi(site, tstar)
        keep = M > 1e-9
        prof.append((M[keep] / M[keep].sum(), site.P[keep]))
    Vstar = solve_V(chain, prof, e + alpha(chain, prof))
    print("   %-18s e = 0.3E: Rhat = %.9f (t* = %.4f);  V at the generalised-dip profile = %s  (diff %s)" %
          (cname, R, tstar, "%.9f" % Vstar if Vstar is not None else "solver failed", "%.1e" % (Vstar - R) if Vstar is not None else "-"))
    # (B) random profiles and budgets
    nrand = 0
    while nrand < 12 and time.time() - t0 < 420:
        prof = []
        for lam, site in chain:
            nu = int(rng.integers(1, 4))
            prof.append((rng.dirichlet(np.ones(nu) * 2), rng.dirichlet(np.ones(site.q) * rng.choice([0.7, 2.0]), size=nu)))
        al = alpha(chain, prof); vb = vbar(chain, prof)
        B = vb + float(rng.uniform(0.0, 1.2)) * E            # B >= v(mubar); the accuracy B - alpha may be negative
        V = solve_V(chain, prof, B)
        if V is None:
            continue
        Rb = dlib.Rhat(chain, B - al)[0]
        tot += 1; nrand += 1
        worst_excess = max(worst_excess, V - Rb)
        if Rb > 1e-6:
            nontriv += 1; gaps.append(V - Rb)
        if B - al < 0:
            negacc += 1
        if V > Rb + 1e-7:
            viol += 1
            print("      VIOLATION?", cname, "V", V, "Rhat", Rb, "B - alpha", B - al)
print("   random (profile, budget) pairs: %d, with V > Rhat + 1e-7: %d;  max(V - Rhat) = %.2e" % (tot, viol, worst_excess))
print("time %.1f s" % (time.time() - t0))

print("   of these with Rhat > 1e-6: %d (negative accuracy B - alpha < 0 in %d); there V - Rhat ranges in [%.2e, %.2e]" % (nontriv, negacc, min(gaps), max(gaps)))
