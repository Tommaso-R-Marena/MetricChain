"""t16: the single-letter optimisation behind the converse tail lemma (Theorem F6 of REPORT.md), by a PRIMAL
minimisation that is independent of the game formula.

For a law P_UX on U x {0,1} (|U| <= 4), alpha = D(P_{X|U} || pi | P_U), and a budget B = alpha + e >= v(P_X):
    V_H(P_UX; B) = min { I(X';U) : u E d(X',X) + v(P_X') <= B }       (kernel X' | X, U)
               = min over nu in [0,1]^U of I(nu) s.t. u sum_u P(u)|mu_u - nu_u| + v(sum_u P(u) nu_u) <= B
(binary alphabet: the cheapest coupling of mu_u and nu_u costs |mu_u - nu_u|).
Claims tested:  (i) V_H(P_UX; alpha + e) <= R^max(e) for every P_UX (random laws, |U| = 2, 3, 4; e of both signs);
(ii) equality for U = centre letter with law Bernoulli(m*) and X | U = cone law (the generalised dip);
(iii) random local ascent from that law with |U| up to 4 does not exceed R^max(e)."""
import math, sys, time
import numpy as np
from scipy.optimize import minimize
from flib import *

rng = np.random.default_rng(16)

def Hb(x):
    x = min(max(x, 1e-300), 1 - 1e-16)
    return -x * math.log(x) - (1 - x) * math.log(1 - x)

def VH(st, PU, mu, B):
    """min I(nu) s.t. u sum P(u) d_u + v(nubar) <= B, d_u >= |mu_u - nu_u|; variables z = (nu, d)"""
    K = len(PU)
    u = st.u
    def I(z):
        nu = z[:K]
        return Hb(float(PU @ nu)) - float(sum(PU[k] * Hb(nu[k]) for k in range(K)))
    cons = [{"type": "ineq", "fun": lambda z: B - u * float(PU @ z[K:]) - float(st.v(float(PU @ z[:K])))}]
    for k in range(K):
        cons.append({"type": "ineq", "fun": lambda z, k=k: z[K + k] - (z[k] - mu[k])})
        cons.append({"type": "ineq", "fun": lambda z, k=k: z[K + k] - (mu[k] - z[k])})
    best = math.inf
    xbar = float(PU @ mu)
    starts = [np.concatenate([mu, np.zeros(K)])]
    # feasible interior starts: move a fraction lam towards a common value c
    for c in (xbar, st.p, min(max(xbar, st.kmin), st.kmax)):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            lam = (lo + hi) / 2
            nu = mu + lam * (c - mu)
            if u * float(PU @ np.abs(mu - nu)) + float(st.v(float(PU @ nu))) <= B:
                lo = lam
            else:
                hi = lam
        nu = mu + lo * (c - mu)
        starts.append(np.concatenate([nu, np.abs(mu - nu)]))
    for z0 in starts:
        res = minimize(I, z0, method="SLSQP", constraints=cons, bounds=[(1e-9, 1 - 1e-9)] * K + [(0, 1)] * K,
                       options=dict(ftol=1e-14, maxiter=400))
        z = res.x
        feas = all(c["fun"](z) >= -1e-9 for c in cons)
        if feas:
            best = min(best, I(z))
        if all(c["fun"](z0) >= -1e-9 for c in cons):
            best = min(best, I(z0))
    return best

def alpha_of(st, PU, mu):
    return float(sum(PU[k] * kls(mu[k], st.p) for k in range(len(PU))))

t0 = time.time()
worst = -math.inf; eqerr = 0.0; nrand = 0; nasc = 0
for p, u in ((0.3, 1.0), (0.1, 2.0), (0.2, 4.0), (0.5, 1.0)):
    st = Site(p, u)
    wp = WorstPair(p, u)
    for e in (-0.5 * wp.a, -0.2 * wp.h, 0.0, 0.3 * wp.E, 0.7 * wp.E):
        Rm = float(wp.R(e))
        # (ii) the generalised dip (only for e in the depth regime e > e_c)
        if e > wp.ec:
            aH = maxmin_precise(st, "na", float(wp.S(e)))        # the same centre type m* as for H at e (also for e < 0)
            PU = np.array([1 - aH[1], aH[1]]); mu = np.array([st.eta0, 1 - st.eta1])
            al = alpha_of(st, PU, mu)
            val = VH(st, PU, mu, al + e)
            eqerr = max(eqerr, abs(val - Rm))
            base = (PU, mu)
        else:
            base = None
        # (i) random laws
        for _ in range(40):
            K = int(rng.integers(2, 5))
            PU = rng.dirichlet(np.ones(K)); mu = rng.uniform(0.01, 0.99, size=K)
            al = alpha_of(st, PU, mu)
            if al + e < float(st.v(float(PU @ mu))) + 1e-9:
                continue
            val = VH(st, PU, mu, al + e)
            worst = max(worst, val - Rm); nrand += 1
        # (iii) local ascent from the generalised dip, with one or two extra labels
        if base is not None:
            PU0 = np.concatenate([base[0] * 0.98, [0.01, 0.01]]); mu0 = np.concatenate([base[1], [0.5, 0.5]])
            cur = -math.inf
            for it in range(60):
                PU = np.abs(PU0 + rng.normal(0, 0.03, size=4)); PU /= PU.sum()
                mu = np.clip(mu0 + rng.normal(0, 0.03, size=4), 0.005, 0.995)
                al = alpha_of(st, PU, mu)
                if al + e < float(st.v(float(PU @ mu))) + 1e-9:
                    continue
                val = VH(st, PU, mu, al + e)
                nasc += 1
                worst = max(worst, val - Rm)
                if val > cur:
                    cur, PU0, mu0 = val, PU, mu
    print(f"p={p} u={u}: so far  max over laws of [V_H - R^max] = {worst:.3e};  |V_H(generalised dip) - R^max| <= {eqerr:.3e};  laws tested {nrand} + {nasc}  [{time.time()-t0:.0f}s]", flush=True)
print("RESULT: no law with V_H > R^max:", worst <= 1e-6, " equality at the generalised dip:", eqerr <= 1e-6)
