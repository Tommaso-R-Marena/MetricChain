"""
t05_evaluation_lemma.py -- the single-letter step on which every upper bound of section 11.26 rests
(Theorem 11.98(a),(b) = W3(a),(b)), tested by a PRIMAL solver that knows nothing of games, vertices-as-labels,
Renyi capacities or the slope t:

   V(mu, B; v) := min { MI(nu) : dist(nu -> mu) + v(nubar) <= B }      (labelled profile mu; exit profile nu)
   claim:  V(mu, B; v) <= R^(B - alpha(mu))   for EVERY labelled profile mu and every B >= v(mubar),
           with equality (for B - alpha >= 0) at the generalised-dip profile (labels = optimal vertices, letter laws = Gibbs laws).

Here, for one or several site types j with fractions lambda_j:
   MI(nu)        = sum_j lambda_j sum_u P_j(u) KL(nu_ju || nubar_j)
   dist(nu->mu)  = sum_j lambda_j sum_u P_j(u) W_j(nu_ju, mu_ju),   W_j(P', P) = max_{phi in V_j} [E_P' phi - E_P phi]   (oriented)
   v(P)          = sum_j lambda_j min_{P''} [ KL(P''||pi_j) + W_j(P'', P_j) ]
   alpha(mu)     = sum_j lambda_j sum_u P_j(u) KL(mu_ju || pi_j)
The minimisation is one convex programme in (nu, P'', epigraph variables), solved by SLSQP (no duality used).
The claim for several site types tests "one common slope" (R^ uses F* = sum_j lambda_j F*_j at a COMMON t).
"""
import sys, time
import numpy as np
from scipy.optimize import minimize
from r5lib import *
from t01_identity import sites_example, random_site

np.set_printoptions(precision=5, suppress=True, linewidth=160)


def kl(p, q):
    p = np.maximum(p, 1e-300)
    return float(np.sum(p * (np.log(p) - np.log(q))))


class Profile:
    """labelled profile for a chain: for every site type j, label weights P_j (n_u) and letter laws mu_j (n_u x q_j)."""
    def __init__(self, chain, P, mu):
        self.chain, self.P, self.mu = chain, P, mu

    def alpha(self):
        return sum(l * sum(self.P[j][u] * kl(self.mu[j][u], s.pi) for u in range(len(self.P[j])))
                   for j, (l, s) in enumerate(self.chain.parts))

    def bar(self, j):
        return self.P[j] @ self.mu[j]


def W_cost(site, Pp, P):
    """oriented transport cost W(P', P) = max over vertices of E_P' phi - E_P phi  (Kantorovich dual; = primal LP value)."""
    return float(np.max(site.V @ (Pp - P)))


def v_site(site, P):
    """v_j(P) = min_{P''} [KL(P''||pi) + W(P'', P)]  (small convex programme, epigraph form)."""
    q = site.q
    x0 = np.concatenate([P * 0.999 + 0.001 / q, [0.0]])
    cons = [dict(type="eq", fun=lambda x: x[:q].sum() - 1.0),
            dict(type="ineq", fun=lambda x: x[q] - site.V @ (x[:q] - P))]
    res = minimize(lambda x: kl(x[:q], site.pi) + x[q], x0, method="SLSQP", bounds=[(1e-12, 1)] * q + [(0, None)],
                   constraints=cons, options=dict(ftol=1e-14, maxiter=500))
    return res.fun


def V_primal(prof, B, starts=3, seed=0):
    """min { MI(nu) : sum_j lambda_j [ sum_u P_j(u) d_ju + KL(P''_j||pi_j) + w_j ] <= B,
             d_ju >= E_{nu_ju} phi - E_{mu_ju} phi,  w_j >= E_{P''_j} phi - E_{nubar_j} phi   for all vertices phi }"""
    ch = prof.chain
    sizes = []
    off = 0
    layout = []
    for j, (l, s) in enumerate(ch.parts):
        nu_ = len(prof.P[j])
        layout.append(dict(nu=(off, nu_, s.q), Pp=off + nu_ * s.q, d=off + nu_ * s.q + s.q, w=off + nu_ * s.q + s.q + nu_))
        off += nu_ * s.q + s.q + nu_ + 1
    nvar = off

    def parts(x, j):
        L = layout[j]
        o, nu_, q = L["nu"]
        nu = x[o:o + nu_ * q].reshape(nu_, q)
        Pp = x[L["Pp"]:L["Pp"] + q]
        d = x[L["d"]:L["d"] + nu_]
        w = x[L["w"]]
        return nu, Pp, d, w

    def MI(x):
        tot = 0.0
        for j, (l, s) in enumerate(ch.parts):
            nu, Pp, d, w = parts(x, j)
            nu = np.maximum(nu, 1e-300)
            bar = prof.P[j] @ nu
            tot += l * float(np.sum(prof.P[j][:, None] * nu * (np.log(nu) - np.log(bar)[None, :])))
        return tot

    def budget(x):
        tot = 0.0
        for j, (l, s) in enumerate(ch.parts):
            nu, Pp, d, w = parts(x, j)
            tot += l * (float(prof.P[j] @ d) + kl(Pp, s.pi) + w)
        return B - tot

    def eqs(x):
        out = []
        for j, (l, s) in enumerate(ch.parts):
            nu, Pp, d, w = parts(x, j)
            out.extend(nu.sum(axis=1) - 1.0)
            out.append(Pp.sum() - 1.0)
        return np.array(out)

    def ineqs(x):
        out = [budget(x)]
        for j, (l, s) in enumerate(ch.parts):
            nu, Pp, d, w = parts(x, j)
            bar = prof.P[j] @ nu
            for u in range(len(d)):
                out.extend(d[u] - s.V @ (nu[u] - prof.mu[j][u]))
            out.extend(w - s.V @ (Pp - bar))
        return np.array(out)

    bounds = []
    for j, (l, s) in enumerate(ch.parts):
        nu_ = len(prof.P[j])
        bounds += [(1e-10, 1)] * (nu_ * s.q) + [(1e-10, 1)] * s.q + [(0, None)] * nu_ + [(0, None)]
    rng = np.random.default_rng(seed)
    best = np.inf
    for st in range(starts):
        x0 = np.zeros(nvar)
        for j, (l, s) in enumerate(ch.parts):
            L = layout[j]
            o, nu_, q = L["nu"]
            base = prof.mu[j].copy()
            if st > 0:
                base = 0.7 * base + 0.3 * rng.dirichlet(np.ones(q), size=nu_)
            x0[o:o + nu_ * q] = base.ravel()
            bar = prof.P[j] @ base
            x0[L["Pp"]:L["Pp"] + q] = bar
            x0[L["d"]:L["d"] + nu_] = [max(0.0, W_cost(s, base[u], prof.mu[j][u])) for u in range(nu_)]
            x0[L["w"]] = 0.0
        res = minimize(MI, x0, method="SLSQP", bounds=bounds,
                       constraints=[dict(type="eq", fun=eqs), dict(type="ineq", fun=ineqs)],
                       options=dict(ftol=1e-13, maxiter=3000))
        if res.success and np.min(ineqs(res.x)) > -1e-8 and np.max(np.abs(eqs(res.x))) < 1e-8:
            best = min(best, res.fun)
    return best


def gen_dip_profile(chain, t):
    P, mu = [], []
    for l, s in chain.parts:
        lo, M, hi = renyi_primal(s, t)
        idx = [k for k in range(len(M)) if M[k] > 1e-7]
        P.append(M[idx] / M[idx].sum())
        mu.append(s.W[idx].copy())
    return Profile(chain, P, mu)


def random_profile(chain, rng, nlab=(1, 2, 3)):
    P, mu = [], []
    for l, s in chain.parts:
        k = int(rng.choice(nlab))
        P.append(rng.dirichlet(np.ones(k) * 2))
        m = rng.dirichlet(np.ones(s.q) * rng.choice([0.5, 1.0, 3.0]), size=k)
        m = 0.97 * m + 0.03 / s.q
        mu.append(m)
    return Profile(chain, P, mu)


if __name__ == "__main__":
    t0 = time.time()
    nrand = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    S = sites_example()
    chains = {"asym": Chain([(1.0, S["asym"])], "asym"),
              "tri": Chain([(1.0, S["tri"])], "tri"),
              "mix": Chain([(0.5, S["bin"]), (0.5, S["path"])], "mix"),
              "asym+tri (0.3/0.7)": Chain([(0.3, S["asym"]), (0.7, S["tri"])], "asym+tri")}
    rng = np.random.default_rng(11)
    for nm, ch in chains.items():
        E = ch.E()
        print(f"== chain {nm}: E = {E:.6f} ==")
        # (1) equality at the generalised-dip profile
        for fr in (0.0, 0.3, 0.6):
            e = fr * E
            R, tstar = Rhat(ch.Fstar, e)
            prof = gen_dip_profile(ch, tstar)
            Vp = V_primal(prof, e + prof.alpha(), starts=3)
            print(f"   generalised-dip profile at e = {fr}E: R^(e) = {R:.9f}; primal V(mu*, e+alpha; v) = {Vp:.9f}; V - R^ = {Vp-R:+.2e}"
                  f"   (t* = {tstar:.4f}, labels per type {[len(p) for p in prof.P]})")
        # (2) random profiles never exceed R^
        worst = -np.inf
        nfail = 0
        ndone = 0
        for rep in range(nrand):
            prof = random_profile(ch, rng)
            al = prof.alpha()
            vbar = sum(l * v_site(s, prof.bar(j)) for j, (l, s) in enumerate(ch.parts))
            # budgets: B - alpha = e in a range of both signs, subject to B >= v(mubar)
            for e in (-0.5 * E, 0.0, 0.3 * E, 0.8 * E):
                B = e + al
                if B < vbar + 1e-9:
                    continue
                Vp = V_primal(prof, B, starts=2, seed=rep)
                if not np.isfinite(Vp):
                    nfail += 1
                    continue
                R = Rhat(ch.Fstar, e, ngrid=200)[0]
                worst = max(worst, Vp - R)
                ndone += 1
        print(f"   {ndone} (profile, budget) pairs from {nrand} random profiles (solver failures: {nfail}): max [V(mu,B;v) - R^(B-alpha)] = {worst:+.3e}"
              f"   (claim: <= 0)")
        # (3) perturbations of the optimal profile at e = 0.3E
        e = 0.3 * E
        R, tstar = Rhat(ch.Fstar, e)
        base = gen_dip_profile(ch, tstar)
        worst = -np.inf
        for rep in range(max(6, nrand // 3)):
            P = [np.maximum(p * np.exp(0.2 * rng.normal(size=len(p))), 1e-6) for p in base.P]
            P = [p / p.sum() for p in P]
            mu = [m * np.exp(0.15 * rng.normal(size=m.shape)) for m in base.mu]
            mu = [m / m.sum(axis=1, keepdims=True) for m in mu]
            prof = Profile(ch, P, mu)
            Vp = V_primal(prof, e + prof.alpha(), starts=2, seed=rep)
            if np.isfinite(Vp):
                worst = max(worst, Vp - R)
        print(f"   perturbed optimal profiles at e = 0.3E: max [V - R^] = {worst:+.3e}")
        print(f"   [{time.time()-t0:.0f} s]")
