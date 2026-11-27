#!/usr/bin/env python3
"""Addendum A17 (7): a floor and a variance bracket ln Z without any exponential cost (Bennett) -- coordinator's script.

For a model m with tractable Gibbs measure pi_m and the true energy g = m + r (units k_BT):
    ln Z(g) - ln Z(m) = -E r + K,     K = ln E exp(-(r - E r))   (expectations under pi_m; K >= 0 is the Jensen gap).
If  r >= E r - b  (a one-sided floor, b > 0)  and  Var r <= s2,  then (Bennett's inequality, sharp two-point form)
    K  <=  W(b, s2) := ln[ (b^2 exp(-s2/b) + s2 exp(b)) / (b^2 + s2) ]  <=  (s2/b^2) (e^b - 1 - b).
Compare, on the 74 enumerated rotamer instances of workstream P2 (both batches), for the surrogates m0, m1, m2:
    the true K;  W with the exact b and s2 of the instance;  the range-only bound L(w) of the theory division's
    Theorem 11.110(a), w = max r - min r.
Everything by exact sums.  b and s2 are computed by enumeration here: this tests how sharp the bracket is, it is not a
certificate (a certificate needs b and s2 a priori)."""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib
BETA = anlib.BETA; TAU = 0.6

def W_sharp(b, s2):
    # log of the two-point extremal moment generating function at s = 1
    if b > 700.0:
        return b + math.log(s2 / (b * b + s2))
    # ln(1 + [b^2 (e^{-s2/b} - 1) + s2 (e^b - 1)] / (b^2 + s2)), with expm1/log1p so that tiny values are accurate
    return math.log1p((b * b * math.expm1(-s2 / b) + s2 * math.expm1(b)) / (b * b + s2))
def W_relaxed(b, s2):
    return (s2 / (b * b)) * (math.expm1(min(b, 700.0)) - b)
def L_range(w):
    if w < 1e-12: return 0.0
    if w > 700: return w - math.log(w) - 1.0
    return math.log(math.expm1(w) / w) - 1 + w / math.expm1(w)

def rows_for(tag):
    d = anlib.load_fb(tag)
    mask = d["s2min"] > TAU
    full = bool(mask.all())
    st = np.argwhere(mask)
    f = (d["tors"] + d["lj"] + d["coul"])[mask]; gb = d["gb"][mask]
    out = []
    fits = [("m0", np.zeros_like(gb))]
    for order in (1, 2):
        if order == 2 and d["n"] < 2: continue
        if full:
            fit = anlib.anova_fit(d["gb"], order)[mask]
        else:
            fit = anlib.fit_ls(anlib.design(st, d["shape"], anlib.subsets_of_order(d["n"], order)), gb)
        fits.append((f"m{order}", fit))
    for name, fit in fits:
        m = f + fit
        pm = np.exp(-BETA * (m - m.min())); pm /= pm.sum()
        r = BETA * (gb - fit)
        Er = float(pm @ r); rc = r - Er
        s2 = float(pm @ (rc * rc)); b = float(-rc.min()); w = float(r.max() - r.min())
        K = float(np.log1p(pm @ np.expm1(-rc)))
        if b < 1e-9 or s2 < 1e-18:
            Ws, Wr = 0.0, 0.0
        else:
            Ws, Wr = W_sharp(b, s2), W_relaxed(b, s2)
        out.append(dict(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], states=int(mask.sum()), surrogate=name, b=b, sigma=math.sqrt(s2),
                        width=w, K=K, W_sharp=Ws, W_relaxed=Wr, L_range=L_range(w)))
    return out

def self_test(trials=20000, seed=7):
    """the sharp two-point bound on random laws: X <= b, E X = 0, Var X = s2  =>  ln E e^X <= W_sharp(b, s2) <= W_relaxed;
    equality at the two-point law {b with prob s2/(b^2+s2), -s2/b}."""
    rng = np.random.default_rng(seed); worst = 0.0
    for _ in range(trials):
        k = int(rng.integers(2, 9))
        x = rng.normal(0, rng.choice([0.05, 0.5, 2.0, 6.0]), k); p = rng.dirichlet(np.full(k, rng.choice([0.2, 1.0])))
        x = x - p @ x
        b = float(x.max()); s2 = float(p @ (x * x))
        if b < 1e-9 or s2 < 1e-14: continue
        K = math.log1p(float(p @ np.expm1(x))) - float(p @ x)     # subtract the residual mean left by rounding
        W = W_sharp(b, s2)
        assert K <= W * (1 + 1e-9) + 1e-15, (K, W)                 # 1e-15: rounding of the centring, at x of order one
        assert W <= W_relaxed(b, s2) * (1 + 1e-9) + 1e-13
        if W > 1e-9: worst = max(worst, K / W)                     # ratios of numbers at rounding level are not informative
    for b, s2 in ((0.5, 0.01), (3.0, 0.2), (8.0, 1.0)):
        q = s2 / (b * b + s2)
        K = math.log1p(q * math.expm1(b) + (1 - q) * math.expm1(-s2 / b))
        assert abs(K - W_sharp(b, s2)) < 1e-12 * max(1.0, K)
    return worst

if __name__ == "__main__":
    print(f"# self-test of the sharp bound on 20 000 random laws: largest K/W (cases with W > 1e-9) = {self_test():.9f} (1 up to rounding: the law drawn most often is itself two-point); equality at the two-point law")
    tags = []
    for aa, ns in (("V", (4, 8, 12)), ("L", (4, 8)), ("S", (2, 4, 6)), ("K", (2, 3, 4)), ("F", (4, 6, 8)), ("LKSEc", (3, 4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for n in ns:
                t = f"fb_{aa}{n}_{bb}_R3_t0.60"
                if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): tags.append(t)
    out = []
    print(f"{'instance':<12}{'sur':>4}{'floor b':>9}{'sigma':>8}{'width w':>9} | {'true K':>10}{'Bennett W':>11}{'W/K':>8}{'range L(w)':>12}")
    viol = 0
    for t in tags:
        for r in rows_for(t):
            ratio = (r['W_sharp'] / r['K']) if r['K'] > 1e-12 else float('nan')
            if r['K'] > r['W_sharp'] * (1 + 1e-9) + 1e-12: viol += 1
            print(f"{(r['seq'] if len(set(r['seq']))>1 else r['seq'][0]+str(r['n'])) + '_' + r['bb']:<12}{r['surrogate']:>4}{r['b']:>9.3f}{r['sigma']:>8.4f}{r['width']:>9.2f} | "
                  f"{r['K']:>10.3e}{r['W_sharp']:>11.3e}{ratio:>8.1f}{r['L_range']:>12.3e}", flush=True)
            out.append(r)
    json.dump(out, open(os.path.join(HERE, "bennett_bracket_real.json"), "w"), indent=1)
    print(f"# {len(out)} rows; violations of K <= W: {viol}")
