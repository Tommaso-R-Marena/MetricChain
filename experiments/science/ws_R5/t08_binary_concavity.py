"""t08_binary_concavity.py -- is the site function concave for EVERY two-letter site?  (Proposition 11.100: "concave in 100
cases computed (no proof)").  Every pair of Bernoulli laws with full support is the pair of vertex Gibbs laws of some
two-letter site (pi, (u1,u2)), so the question is: is
     F*(t) = max_{0<=M<=1}  -t ln sum_a ( M P1(a)^t + (1-M) P2(a)^t )^(1/t)
concave on [0,1] for every binary-input binary-output channel (P1, P2)?   Wider and more extreme scan than the report's.
Method: for every t on a grid, 1-D bounded maximisation over M (the function is quasi-concave in M), then second differences."""
import sys, time
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp

def G(M, t, lP1, lP2):
    ls = np.logaddexp(np.log(M) + t * lP1, np.log1p(-M) + t * lP2)
    return -t * logsumexp(ls / t)

def Fstar(t, lP1, lP2):
    r = minimize_scalar(lambda M: -G(M, t, lP1, lP2), bounds=(1e-13, 1 - 1e-13), method="bounded", options=dict(xatol=1e-14))
    return -r.fun

if __name__ == "__main__":
    t0 = time.time()
    nch = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    rng = np.random.default_rng(5)
    ts = np.linspace(0.02, 0.98, 97)
    worst = (-np.inf, None)
    nviol = 0
    for k in range(nch):
        # logits spread over many scales: |logit| up to ~14, including nearly noiseless and very skewed channels
        l1, l2 = rng.normal(scale=rng.choice([0.5, 2.0, 5.0]), size=2) + rng.normal(scale=rng.choice([0.0, 3.0]))
        if abs(l1 - l2) < 1e-3:
            continue
        a1, a2 = 1 / (1 + np.exp(-l1)), 1 / (1 + np.exp(-l2))
        lP1 = np.array([np.log(a1), np.log1p(-a1)]); lP2 = np.array([np.log(a2), np.log1p(-a2)])
        F = np.array([Fstar(t, lP1, lP2) for t in ts])
        d2 = F[2:] - 2 * F[1:-1] + F[:-2]
        rel = d2.max() / max(F.max(), 1e-300)
        if rel > worst[0]:
            worst = (rel, (a1, a2, ts[1 + int(d2.argmax())], d2.max(), F.max()))
        nviol += (d2.max() > 1e-11 * max(F.max(), 1e-12))
    print(f"{nch} random two-letter sites (logits of the two vertex laws up to |14|), grid step 0.01 in t:")
    print(f"   sites with a positive second difference of F* (beyond 1e-11 relative): {nviol}")
    print(f"   largest (second difference)/max F*: {worst[0]:+.3e} at (P1(0), P2(0), t, d2, maxF) = {worst[1]}")
    print(f"[{time.time()-t0:.0f} s]")
