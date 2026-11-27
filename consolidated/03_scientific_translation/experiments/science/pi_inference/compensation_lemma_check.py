"""Coordinator's own check of workstream F's Lemma 3 (compensation) and of the construction of its Theorem A.
Own code, nothing imported from experiments/science/ws_F.

Biased cube, pi = Bern(p)^n, class L_u.  Base: additive instance w_gamma (normalised).  Alternative: base plus the
cyclic average of the dips (e^r c_s - w_gamma)_+ around the shifts of a centre s.  Compensator: b * (normalised
extreme additive instance), added to BOTH, with b = A_w (c_D - c_w)/(p_2 - c_D).  Claims checked on the whole cube:
both are members of the class; all n one-body marginals of both are equal to c_D; ln A(alt) - ln A(base) =
ln(1 + E/(1 + b)); without the compensator the marginals differ.

Usage: python3 compensation_lemma_check.py     (seconds)
"""
import math, itertools
import numpy as np

def run(n, p, u, gamma, s, r):
    X = np.array(list(itertools.product([0, 1], repeat=n))); N = len(X); wt = X.sum(axis=1)
    pi = p**wt * (1 - p)**(n - wt)
    def additive(g):                                   # normalised: sum pi w = 1
        return np.exp(-g*wt) / ((1 - p) + p*math.exp(-g))**n
    def cone(c):
        w = np.exp(-u*(X != c[None, :]).sum(axis=1)); return w/(pi @ w)
    wg = additive(gamma)
    shifts = [np.roll(s, j) for j in range(n)]
    D = sum(np.maximum(math.exp(r)*cone(c) - wg, 0.0) for c in shifts)/n
    dens = lambda w: float((pi*w) @ wt)/(n*float(pi @ w))
    E = float(pi @ D); cD = dens(D); cw = dens(wg)
    g2 = -u if cD > cw else u
    p2 = p*math.exp(-g2)/((1 - p) + p*math.exp(-g2))
    b = 1.0*(cD - cw)/(p2 - cD)
    assert b > 0
    w0 = wg + b*additive(g2); w1 = w0 + D
    def in_class(w):
        worst = 0.0
        for i in range(n):
            flip = np.array([int("".join(map(str, np.where(np.arange(n) == i, 1 - x, x))), 2) for x in X])
            worst = max(worst, float(np.max(np.abs(np.log(w[flip]/w)))))
        return worst
    marg = lambda w: (pi*w) @ X / float(pi @ w)
    m0, m1 = marg(w0), marg(w1); mb, ma = marg(wg), marg(wg + D)
    sep = math.log(float(pi @ w1)/float(pi @ w0))
    return dict(b=b, cD=cD, cw=cw, lip0=in_class(w0)/u, lip1=in_class(w1)/u,
                marg_spread=float(max(np.max(np.abs(m0 - cD)), np.max(np.abs(m1 - cD)))),
                sep_err=abs(sep - math.log(1 + E/(1 + b))), uncompensated_diff=float(np.max(np.abs(mb - ma))), sep=sep)

if __name__ == "__main__":
    rng = np.random.default_rng(3)
    worst = 0.0
    for trial in range(12):
        n = int(rng.integers(6, 11)); p = float(rng.uniform(0.1, 0.45)); u = float(rng.uniform(0.8, 2.2))
        gamma = float(rng.uniform(-u, u)); k = int(rng.integers(2, n - 1)); r = float(rng.uniform(2.0, 4.0))
        s = np.zeros(n, int); s[rng.choice(n, k, replace=False)] = 1
        try:
            o = run(n, p, u, gamma, s, r)
        except AssertionError:
            print(f"n={n} p={p:.3f} u={u:.2f} gamma={gamma:+.2f} k={k} r={r:.2f}: excess density equals the base density or lies outside the reachable side; skipped"); continue
        assert o["lip0"] <= 1 + 1e-9 and o["lip1"] <= 1 + 1e-9 and o["marg_spread"] < 1e-10 and o["sep_err"] < 1e-9
        worst = max(worst, o["marg_spread"])
        print(f"n={n} p={p:.3f} u={u:.2f} gamma={gamma:+.2f} k={k} r={r:.2f}: b={o['b']:.4f}  class slopes/u: {o['lip0']:.4f}, {o['lip1']:.4f}  "
              f"all one-body marginals of base and alternative = c_D = {o['cD']:.5f} (max dev {o['marg_spread']:.1e})  "
              f"ln A gap {o['sep']:.3f} (formula error {o['sep_err']:.1e})  without compensator the marginals differ by {o['uncompensated_diff']:.3f}")
    print(f"largest deviation of any marginal from the common value: {worst:.1e}")
