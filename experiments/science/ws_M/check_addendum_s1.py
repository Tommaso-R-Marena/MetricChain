#!/usr/bin/env python3
"""Workstream M, addendum S1 — the coordinator's Theorem 7 (stability of maximum-entropy
refinement) against a derivation from two textbook facts.

Setting (INFERENCE_LIMITS.md, Theorem 7): X finite, mu0 full support,
  mu      ~ mu0 * exp(-beta*(lam.Phi + r)),            omega = osc(r),
  mu_lam  ~ mu0 * exp(-beta*lam.Phi)                   (the truth without the remainder),
  nu      = I-projection of mu0 on {E Phi = E_mu Phi}  (= member of the exponential family
            {mu0 exp(-theta.Phi)} with the Phi-means of mu).
Facts checked here:
  F1  nu minimises KL(mu || q) over the exponential family (moment matching = reverse
      I-projection), hence KL(mu||nu) <= KL(mu||mu_lam).
  F2  KL(mu||mu_lam) <= (beta*omega)^2/8  (mu is a bounded tilt of mu_lam; Hoeffding's lemma).
  =>  KL(mu||nu) <= (beta*omega)^2/8  and, by Pinsker, TV(mu,nu) <= beta*omega/4.
  Compared with Theorem 7:  (i) J = KL(mu||nu)+KL(nu||mu) = beta(E_nu r - E_mu r);
  (ii) TV <= beta*omega/4;  (iii) J <= (beta*omega)^2/4;  (v) Pythagoras.
  Also recorded: the sharp feature-free bound TV <= tanh(beta*omega/4) does NOT need to hold
  with features (we report the largest ratio TV/tanh(beta*omega/4) seen).
Run:  python3 experiments/science/ws_M/check_addendum_s1.py   (about 20 s)
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(7)


def kl(p, q):
    return float(np.sum(p * (np.log(p) - np.log(q))))


def gibbs(logw):
    a = logw - logw.max()
    p = np.exp(a)
    return p / p.sum()


def iproj(mu0, Phi, m):
    """member of {mu0 exp(-theta.Phi)} with E Phi = m (convex dual, BFGS + Newton polish)."""
    K = Phi.shape[1]

    def f(th):
        a = -Phi @ th + np.log(mu0)
        amax = a.max()
        return amax + np.log(np.exp(a - amax).sum()) + th @ m

    def g(th):
        p = gibbs(-Phi @ th + np.log(mu0))
        return m - p @ Phi

    r = minimize(f, np.zeros(K), jac=g, method="BFGS", options={"gtol": 1e-12, "maxiter": 10000})
    th = r.x
    for _ in range(50):                       # Newton polish
        p = gibbs(-Phi @ th + np.log(mu0))
        grad = m - p @ Phi
        cov = (Phi * p[:, None]).T @ Phi - np.outer(p @ Phi, p @ Phi)
        try:
            step = np.linalg.solve(cov + 1e-14 * np.eye(K), -grad)
        except np.linalg.LinAlgError:
            break
        th = th + step
        if np.max(np.abs(grad)) < 1e-13:
            break
    return gibbs(-Phi @ th + np.log(mu0)), th


rows = []
worst = dict(F1=-np.inf, F2=0.0, KL8=0.0, TV=0.0, J4=0.0, idJ=0.0, pyth=0.0, tanh=0.0)
n_inst = 0
for trial in range(4000):
    n = int(rng.integers(3, 40))
    K = int(rng.integers(0, 7))
    beta = 1.0
    mu0 = rng.dirichlet(np.ones(n) * rng.choice([0.3, 1.0, 3.0]))
    Phi = rng.normal(size=(n, K)) * rng.choice([0.3, 1.0, 3.0]) if K else np.zeros((n, 0))
    lam = rng.normal(size=K) * rng.choice([0.3, 1.0, 3.0])
    kind = rng.integers(0, 3)
    r = rng.normal(size=n) if kind == 0 else (rng.random(n) < 0.5).astype(float) if kind == 1 \
        else rng.exponential(size=n)
    if np.ptp(r) == 0:
        continue
    bw = float(rng.choice([0.05, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0]))
    r = r / np.ptp(r) * bw / beta
    mu = gibbs(np.log(mu0) - beta * (Phi @ lam + r))
    mul = gibbs(np.log(mu0) - beta * (Phi @ lam))
    if mu.min() < 1e-14:
        continue
    if K:
        nu, th = iproj(mu0, Phi, mu @ Phi)
        if np.max(np.abs(nu @ Phi - mu @ Phi)) > 1e-9 or nu.min() < 1e-300:
            continue
    else:
        nu = mu0.copy()
    n_inst += 1
    klmn, klnm = kl(mu, nu), kl(nu, mu)
    J = klmn + klnm
    tv = 0.5 * np.abs(mu - nu).sum()
    worst["F1"] = max(worst["F1"], klmn - kl(mu, mul))            # must be <= 0
    worst["F2"] = max(worst["F2"], kl(mu, mul) / (bw ** 2 / 8))   # must be <= 1
    worst["KL8"] = max(worst["KL8"], klmn / (bw ** 2 / 8))        # must be <= 1
    worst["TV"] = max(worst["TV"], tv / (bw / 4))                 # Thm 7(ii): <= 1
    worst["J4"] = max(worst["J4"], J / (bw ** 2 / 4))             # Thm 7(iii): <= 1
    worst["idJ"] = max(worst["idJ"], abs(J - beta * (nu @ r - mu @ r)))
    worst["pyth"] = max(worst["pyth"], abs(kl(mu, mu0) - kl(nu, mu0) - klmn))
    worst["tanh"] = max(worst["tanh"], tv / np.tanh(bw / 4))

lines = [f"instances used: {n_inst}",
         f"F1  max [KL(mu||nu) - KL(mu||mu_lam)]            = {worst['F1']:.3e}   (must be <= 0 up to solver tolerance)",
         f"F2  max KL(mu||mu_lam) / ((beta*omega)^2/8)       = {worst['F2']:.5f}   (must be <= 1)",
         f"    max KL(mu||nu)     / ((beta*omega)^2/8)       = {worst['KL8']:.5f}   (must be <= 1: the sharper bound)",
         f"T7(ii)  max TV(mu,nu) / (beta*omega/4)            = {worst['TV']:.5f}",
         f"T7(iii) max J(mu,nu)  / ((beta*omega)^2/4)        = {worst['J4']:.5f}",
         f"T7(i)   max |J - beta(E_nu r - E_mu r)|           = {worst['idJ']:.2e}",
         f"T7(v)   max |KL(mu||mu0) - KL(nu||mu0) - KL(mu||nu)| = {worst['pyth']:.2e}",
         f"        max TV(mu,nu) / tanh(beta*omega/4)        = {worst['tanh']:.5f}   (feature-free sharp form; > 1 would show it fails with features)"]
out = "\n".join(lines)
print(out)
open(__file__.replace(".py", ".out"), "w").write(out + "\n")
