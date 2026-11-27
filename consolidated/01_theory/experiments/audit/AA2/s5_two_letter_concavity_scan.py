#!/usr/bin/env python3
"""AA2 audit, script S5 -- an adversarial scan of the one conjecture on which the "exponents after the best
split add" statement of theory report Proposition 11.100 rests for two-letter sites:

    [C]  for every binary-input binary-output channel, rho -> max_p E_0(rho, p) is concave;
         equivalently the site function F*(t) = (1 - t) C_t of every two-letter site is concave on [0, 1].

The report: "concave in every case computed -- 100 sites of the workstream, 500 random sites of the
reviewer, 500 random sites with asymmetric envelopes of ours; slopes 0.02 ... 0.98 -- and there is no proof".

Every two-letter site (law pi, envelope slopes u1, u2) is a channel with rows W_0 = Bernoulli(x),
W_1 = Bernoulli(y), 0 < x < y < 1 (the Gibbs laws of its two vertices), and
    F*(t) = max_m  -t ln sum_a ( m W_0(a)^t + (1 - m) W_1(a)^t )^{1/t}          (Theorem 11.99).
This script scans a grid of channels that includes extreme ones (logit x, logit y in [-14, 14]: sites with
slopes up to u = 14 and fields up to 14) and tests the second differences of t -> F*(t) on a grid of 399
slopes.  Own code; float64 (the maximum over m is refined on a local grid of step 5e-6, so each value of F*
is accurate to about 1e-11, and violations are counted above 2e-10).

Run:  python3 experiments/audit/AA2/s5_two_letter_concavity_scan.py > experiments/audit/AA2/out_s5.txt
"""
import math
import numpy as np

ts = np.linspace(0.0025, 0.9975, 399)
h = ts[1] - ts[0]
mgrid = np.linspace(0.0, 1.0, 2001)


def G(t, m, x, y):
    """-t ln [ (m (1-x)^t + (1-m)(1-y)^t)^{1/t} + (m x^t + (1-m) y^t)^{1/t} ], broadcast over t (column) and m (row)."""
    a0 = m * (1 - x) ** t + (1 - m) * (1 - y) ** t
    a1 = m * x ** t + (1 - m) * y ** t
    return -t * np.log(a0 ** (1 / t) + a1 ** (1 / t))


def Fstar(x, y):
    T = ts[:, None]
    vals = G(T, mgrid[None, :], x, y)                     # 399 x 2001
    k = vals.argmax(axis=1)
    centre = mgrid[k]
    step = mgrid[1] - mgrid[0]
    loc = np.clip(centre[:, None] + np.linspace(-step, step, 401)[None, :], 0.0, 1.0)
    vals2 = G(T, loc, x, y)
    return vals2.max(axis=1), loc[np.arange(len(ts)), vals2.argmax(axis=1)]


sig = lambda z: 1.0 / (1.0 + math.exp(-z))
logits = np.arange(-14.0, 14.0001, 0.5)
tol = 2e-10
n_ch, n_viol = 0, 0
worst = (0.0, None)
largest_rel = (0.0, None)
min_curv = (0.0, None)
for i, lx in enumerate(logits):
    for ly in logits[i + 1:]:
        x, y = sig(lx), sig(ly)
        F, marg = Fstar(x, y)
        d2 = F[:-2] - 2 * F[1:-1] + F[2:]                 # must be <= 0 for a concave function
        n_ch += 1
        v = float(d2.max())
        if v > tol:
            n_viol += 1
        if v > worst[0]:
            worst = (v, (lx, ly, float(ts[1 + int(d2.argmax())])))
        # how close to linear does F* get (least curvature relative to its size)?
        rel = float((d2 / (h * h)).max())
        if min_curv[1] is None or rel > min_curv[0]:
            min_curv = (rel, (lx, ly, float(ts[1 + int(d2.argmax())]), float(F.max())))
print("AA2 / S5: concavity of the two-letter site function F*(t) = (1 - t) C_t")
print(f"channels scanned: {n_ch}  (logit x < logit y on the grid -14, -13.5, ..., 14: slopes u = (logit y - logit x)/2 up to 14, fields up to 14)")
print(f"slopes t: {len(ts)} values in (0, 1), step {h:.4f}")
print(f"channels with a second difference above {tol:g}: {n_viol}")
print(f"largest second difference found: {worst[0]:.3e} at (logit x, logit y, t) = {worst[1]}")
print(f"largest second derivative estimate (least concave point): {min_curv[0]:.3e} at (logit x, logit y, t, max F*) = {min_curv[1]}")
print()

# a finer look at the family where concavity is weakest: strongly asymmetric (Z-like) channels, fine grid in t
print("fine scan of strongly asymmetric channels (x -> 0: one vertex law nearly deterministic), t-step 0.0005:")
ts_f = np.linspace(0.0005, 0.9995, 1999)
hf = ts_f[1] - ts_f[0]


def Fstar_fine(x, y):
    T = ts_f[:, None]
    vals = G(T, mgrid[None, :], x, y)
    k = vals.argmax(axis=1)
    step = mgrid[1] - mgrid[0]
    loc = np.clip(mgrid[k][:, None] + np.linspace(-step, step, 401)[None, :], 0.0, 1.0)
    return G(T, loc, x, y).max(axis=1)


worst_f = (-1.0, None)
for lx in (-30.0, -20.0, -12.0, -8.0, -5.0, -3.0):
    for ly in (-6.0, -4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0, 8.0):
        if ly <= lx:
            continue
        x, y = sig(lx), sig(ly)
        F = Fstar_fine(x, y)
        d2 = F[:-2] - 2 * F[1:-1] + F[2:]
        v = float(d2.max())
        if v > worst_f[0]:
            worst_f = (v, (lx, ly, float(ts_f[1 + int(d2.argmax())])))
print(f"  largest second difference: {worst_f[0]:.3e} at (logit x, logit y, t) = {worst_f[1]}   (a positive value above 1e-10 would refute [C])")
print()
print("RESULT: no violation of concavity found" if n_viol == 0 and worst_f[0] <= 1e-10 else "RESULT: VIOLATION FOUND -- see above")
