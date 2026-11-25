#!/usr/bin/env python3
"""R3 — adversarial test of Theorem 7 (stability of maximum-entropy refinement) of
INFERENCE_LIMITS.md, and of the referee's sharpening.

Setting (beta = 1; lambda can be absorbed into mu0 without changing nu):
    mu ~ mu0 exp(-r),  osc(r) = omega,   nu = I-projection of mu0 on {E Phi = E_mu Phi}.
Note's claims:   (i) J := KL(mu|nu)+KL(nu|mu) = E_nu r - E_mu r;  (ii) TV <= omega/4;
                 (iii) J <= omega^2/4;  (v) KL(mu|mu0) - KL(nu|mu0) = KL(mu|nu) >= 0.
Referee's sharpening (proved in the report): TV <= tanh(omega/4), J <= omega tanh(omega/4),
both attained for every omega (two points, no feature, mu0(A) = 1/(1+e^{omega/2})), because
J >= 2 TV ln((1+TV)/(1-TV)) for every pair of measures.

What is done: (a) the sharp Jeffreys-TV inequality on random pairs; (b) random instances;
(c) adversarial ascent (Nelder-Mead restarts on (mu0, Phi, r)) on TV / tanh(omega/4) and on
KL(mu|nu) / [omega tanh(omega/4)/2]; (d) the extremal two-point family.
"""
import math, sys
import numpy as np
from scipy.optimize import minimize

def iproj(mu0, Phi, m, tol=1e-13):
    """I-projection of mu0 on {E Phi = m}: nu ~ mu0 exp(theta.Phi).  Phi: (K, N)."""
    K, N = Phi.shape
    if K == 0:
        return mu0.copy(), np.zeros(0)
    C = Phi - m[:, None]
    theta = np.zeros(K)
    def F(th):
        a = th @ C + np.log(mu0)
        mx = a.max()
        return mx + math.log(np.exp(a - mx).sum())
    for it in range(200):
        a = theta @ C + np.log(mu0); a -= a.max()
        p = np.exp(a); p /= p.sum()
        g = C @ p
        if np.max(np.abs(g)) < tol:
            break
        H = (C * p) @ C.T - np.outer(g, g)
        try:
            step = np.linalg.lstsq(H + 1e-14 * np.eye(K), -g, rcond=None)[0]
        except np.linalg.LinAlgError:
            step = -g
        f0 = F(theta); tt = 1.0
        while F(theta + tt * step) > f0 - 1e-4 * tt * abs(g @ step) and tt > 1e-12:
            tt *= 0.5
        theta = theta + tt * step
    a = theta @ C + np.log(mu0); a -= a.max()
    p = np.exp(a); p /= p.sum()
    return p, theta

def kl(p, q):
    return float(np.sum(p * (np.log(p) - np.log(q))))

def instance(mu0, Phi, r):
    w = mu0 * np.exp(-(r - r.min()))
    mu = w / w.sum()
    m = Phi @ mu if Phi.shape[0] else np.zeros(0)
    nu, theta = iproj(mu0, Phi, m)
    res = float(np.max(np.abs(Phi @ nu - m))) if Phi.shape[0] else 0.0
    tv = 0.5 * float(np.abs(mu - nu).sum())
    J = kl(mu, nu) + kl(nu, mu)
    return dict(mu=mu, nu=nu, tv=tv, J=J, klmn=kl(mu, nu), klnm=kl(nu, mu), res=res,
                id_i=J - float(nu @ r - mu @ r),
                id_v=kl(mu, mu0) - kl(nu, mu0) - kl(mu, nu))

def jeffreys_tv(rng):
    worst = math.inf
    for _ in range(200000):
        N = int(rng.integers(2, 7))
        p = rng.dirichlet(np.ones(N) * rng.choice([0.2, 1.0, 5.0])) + 1e-12; p /= p.sum()
        q = rng.dirichlet(np.ones(N) * rng.choice([0.2, 1.0, 5.0])) + 1e-12; q /= q.sum()
        V = 0.5 * np.abs(p - q).sum()
        if V < 1e-6 or V > 1 - 1e-9:
            continue
        J = float(np.sum((p - q) * (np.log(p) - np.log(q))))
        worst = min(worst, J / (2 * V * math.log((1 + V) / (1 - V))))
    print(f"(a) J / [2 TV ln((1+TV)/(1-TV))] over 2e5 random pairs: min = {worst:.6f} (>= 1 claimed; = 1 on symmetric two-point pairs)")

def random_instances(rng, n_inst=4000):
    worst = dict(tv4=0, tvt=0, J4=0, Jt=0, idi=0, idv=0, res=0)
    for _ in range(n_inst):
        N = int(rng.integers(2, 40)); K = int(rng.integers(0, 7))
        mu0 = rng.dirichlet(np.ones(N) * rng.choice([0.3, 1.0, 3.0])) + 1e-9; mu0 /= mu0.sum()
        Phi = rng.normal(size=(K, N)) * rng.choice([0.3, 1.0, 3.0])
        om = float(rng.choice([0.05, 0.2, 0.5, 1, 2, 4, 8]))
        kind = rng.integers(0, 3)
        if kind == 0:
            r = rng.random(N)
        elif kind == 1:
            r = (rng.random(N) < rng.random()).astype(float)
        else:
            r = np.round(rng.random(N) * 3) / 3
        if r.max() == r.min():
            r[0] = r.min() + 1
        r = (r - r.min()) / (r.max() - r.min()) * om
        o = instance(mu0, Phi, r)
        if o["res"] > 1e-8:
            continue
        worst["tv4"] = max(worst["tv4"], o["tv"] / (om / 4))
        worst["tvt"] = max(worst["tvt"], o["tv"] / math.tanh(om / 4))
        worst["J4"] = max(worst["J4"], o["J"] / (om ** 2 / 4))
        worst["Jt"] = max(worst["Jt"], o["J"] / (om * math.tanh(om / 4)))
        worst["idi"] = max(worst["idi"], abs(o["id_i"]))
        worst["idv"] = max(worst["idv"], abs(o["id_v"]))
        worst["res"] = max(worst["res"], o["res"])
    print(f"(b) {n_inst} random instances (|X|<40, <=6 features): max TV/(w/4) = {worst['tv4']:.5f}, "
          f"max TV/tanh(w/4) = {worst['tvt']:.5f}, max J/(w^2/4) = {worst['J4']:.5f}, max J/(w tanh(w/4)) = {worst['Jt']:.5f};\n"
          f"    identity (i) residual {worst['idi']:.1e}, Pythagoras (v) residual {worst['idv']:.1e}, moment residual {worst['res']:.1e}")

def adversarial(rng):
    print("(c) adversarial ascent (Nelder-Mead, many restarts): can features make max-ent refinement worse than tanh(w/4)?")
    for om in (0.5, 2.0, 4.0, 8.0, 16.0):
        best_tv = 0.0; best_kl = 0.0; best_klnm = 0.0
        for N, K in ((2, 0), (3, 1), (4, 1), (4, 2), (5, 2), (6, 3)):
            for restart in range(12):
                def unpack(z):
                    a = z[:N]; mu0 = np.exp(a - a.max()); mu0 = mu0 / mu0.sum()
                    Phi = z[N:N + K * N].reshape(K, N)
                    rr = z[N + K * N:]
                    r = 1 / (1 + np.exp(-rr))            # in (0,1)
                    r = (r - r.min()) / max(r.max() - r.min(), 1e-12) * om
                    return mu0, Phi, r
                def neg(z, which):
                    mu0, Phi, r = unpack(z)
                    if mu0.min() < 1e-12:
                        return 0.0
                    try:
                        o = instance(mu0, Phi, r)
                    except Exception:
                        return 0.0
                    if o["res"] > 1e-7 or not np.isfinite(o["tv"]):
                        return 0.0
                    return -o[which]
                z0 = rng.normal(size=N + K * N + N) * 2
                for which in ("tv", "klmn", "klnm"):
                    res = minimize(neg, z0, args=(which,), method="Nelder-Mead",
                                   options=dict(maxiter=3000, xatol=1e-9, fatol=1e-12))
                    val = -res.fun
                    if which == "tv":
                        best_tv = max(best_tv, val)
                    elif which == "klmn":
                        best_kl = max(best_kl, val)
                    else:
                        best_klnm = max(best_klnm, val)
        t = math.tanh(om / 4)
        # no-feature suprema of the one-sided divergences (two points, optimise mu0(A))
        ps = np.linspace(1e-6, 1 - 1e-6, 200001)
        q = math.exp(-om)
        muA = ps / (ps + (1 - ps) * q)
        kl_mn = muA * np.log(muA / ps) + (1 - muA) * np.log((1 - muA) / (1 - ps))
        kl_nm = ps * np.log(ps / muA) + (1 - ps) * np.log((1 - ps) / (1 - muA))
        print(f"   w={om}: best TV found = {best_tv:.6f}; tanh(w/4) = {t:.6f}; note's w/4 = {om / 4:.4f}"
              f"{' (vacuous: > 1)' if om / 4 >= 1 else ''} | best KL(mu|nu) = {best_kl:.5f}, best KL(nu|mu) = {best_klnm:.5f}; "
              f"no-feature sup: {kl_mn.max():.5f}, {kl_nm.max():.5f}; J bound w tanh(w/4) = {om * t:.5f}; note's w^2/4 = {om * om / 4:.4f}")

def extremal():
    print("(d) the extremal family: two points, no feature, mu0(A) = 1/(1+e^{w/2}), r = 0 on A, w off A")
    for om in (0.1, 1.0, 4.0, 10.0):
        p = 1 / (1 + math.exp(om / 2))
        mu0 = np.array([p, 1 - p]); r = np.array([0.0, om])
        o = instance(mu0, np.zeros((0, 2)), r)
        print(f"   w={om}: TV = {o['tv']:.10f}, tanh(w/4) = {math.tanh(om / 4):.10f}; J = {o['J']:.10f}, w tanh(w/4) = {om * math.tanh(om / 4):.10f};"
              f" note's example (uniform mu0): TV = {0.5 * math.tanh(om / 2):.6f}")

if __name__ == "__main__":
    rng = np.random.default_rng(424242)
    jeffreys_tv(rng)
    random_instances(rng)
    extremal()
    adversarial(rng)
