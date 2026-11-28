"""
Phase II (adaptive hierarchy) -- Proposition C (a code of cells) at finite slope, exact binomial costs.

N = exp(n R) cells with the same profile, one special cell.  Three blocks P, Q, T.  Relative costs t_j.
Regions for the special cell (budget Theta = n theta, NR = n R):
   W1 = { t <= Theta }                                  F = G1(d_P)
   W2 = { min(t_P, NR) + t_Q + t_T <= Theta }           F = G2(d_P, d_Q)
   W3 = { min(t_P + t_Q, NR) + t_T <= Theta }           twins agree
Normalisation: visible mass exponent 0, i.e.  U = -F <= (t - NR)_+  on W3.
The script builds the pointwise largest admissible U with these properties (iterating the three
projections to a fixed point) and its deepest extension beyond W3, and reports
   gain = max over types outside W3 of [ U(y) - t(y) ]      (the special cell has multiplicity one).
Proposition C: gain <= O(log n) when theta >= h (no hidden mass).  For comparison the same quantity is
reported for theta < h, where a plain dip is hidden.
"""
import sys
import numpy as np
from scipy.special import gammaln
LN2 = np.log(2.0)
def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16); return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)
def consts(u):
    pu = 1 / (1 + np.exp(u)); L1 = np.log(2 / (1 + np.exp(-u))); return pu, L1, f(pu), f(L1 / u)
def relcost(n):
    k = np.arange(n + 1); lb = gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1); return lb.max() - lb
def lip_pass(U, u):
    for ax in range(U.ndim):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + u, out=U[i])
        for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + u, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def run(u, ns, R_over_h, theta_over_h, iters=400):
    pu, L1, a, h = consts(u); n = sum(ns)
    tP, tQ, tT = [relcost(nj) for nj in ns]
    TP, TQ, TT = tP[:, None, None], tQ[None, :, None], tT[None, None, :]
    t = TP + TQ + TT
    Theta = theta_over_h * n * h; NR = R_over_h * n * h
    W1 = t <= Theta
    W2 = (np.minimum(TP, NR) + TQ + TT) <= Theta
    W3 = (np.minimum(TP + TQ, NR) + TT) <= Theta
    INF = 1e18
    U = np.where(W3, np.maximum(t - NR, 0.0), INF)
    for it in range(iters):
        Uold = U.copy()
        U = lip_pass(U, u)
        m = np.where(W1, U, INF).min(axis=(1, 2), keepdims=True); U = np.where(W1, np.minimum(U, m), U)
        m = np.where(W2, U, INF).min(axis=2, keepdims=True); U = np.where(W2, np.minimum(U, m), U)
        U = np.where(W3, U, INF)                      # only W3 is constrained; the extension is recomputed
        if it > 2 and np.max(np.abs(np.where(W3, U - Uold, 0))) < 1e-10: break
    U = lip_pass(U, u)
    hidden = ~W3
    gain = float((U - t)[hidden].max()) if hidden.any() else float('-inf')
    j = np.unravel_index(np.argmax(np.where(hidden, U - t, -INF)), t.shape)
    return gain, tuple(int(x) for x in j), n * h, it

if __name__ == "__main__":
    print("gain = max over types outside W3 of [U - t], nats;  ln(n+1) is about 5.6")
    for u in (1.0, 2.0):
        pu, L1, a, h = consts(u)
        for ns in ((60, 120, 120), (120, 90, 90), (30, 60, 210)):
            for R in (0.0, 0.1, 0.3, 0.6, 1.2):
                row = []
                for th in (0.7, 1.0, 1.2, 1.5):
                    g, at, nh, it = run(u, ns, R, th)
                    row.append("theta=%.1fh: %+7.2f" % (th, g))
                print("u=%.0f blocks %-14s n h = %5.1f  R = %.1f h | %s" % (u, ns, sum(ns) * h, R, "  ".join(row)))
                sys.stdout.flush()
