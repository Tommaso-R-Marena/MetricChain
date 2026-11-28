"""
Phase II (adaptive hierarchy) -- two rounds, more than two blocks (report section 5, last paragraph).

Small-slope limit, box body.  Block P is revealed in round one; the hidden group T consists of one block
(the two-block game of Theorem H2) or of two blocks.  The script computes the largest hidden gain by exact
min-plus envelopes on a grid of step d (region boundaries rounded to the grid) and compares.
Conjecture (report): splitting the hidden group does not raise the two-round threshold above the
two-block value 0.346 a.  A positive gain at theta > 0.346 for some split would refute it.
"""
import numpy as np, sys
def lip_pass(U, costs):
    for ax, c in enumerate(costs):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i-1] + c, out=U[i])
        for i in range(U.shape[0]-2, -1, -1): np.minimum(U[i], U[i+1] + c, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def gain(phiP, phi1, theta, d=0.01, lim=1.1):
    phi2 = 1 - phiP - phi1
    sig = (np.sqrt(phiP), np.sqrt(phi1), np.sqrt(max(phi2, 0)))
    g = np.arange(0, lim + 1e-9, d)
    if phi2 <= 1e-12:
        Y, W1 = np.meshgrid(g, g, indexing='ij'); W2 = np.zeros_like(Y)
        costs = (2*sig[0]*d, 2*sig[1]*d)
    else:
        Y, W1, W2 = np.meshgrid(g, g, g, indexing='ij')
        costs = (2*sig[0]*d, 2*sig[1]*d, 2*sig[2]*d)
    rate = Y**2 + W1**2 + W2**2
    A1 = rate <= theta + 1e-12
    A2 = (W1**2 + W2**2) <= theta + 1e-12
    INF = 1e9
    U = np.where(A2, rate, INF)
    axes = tuple(range(1, U.ndim))
    for it in range(200):
        Uold = U.copy()
        U = lip_pass(U, costs)
        m = np.where(A1, U, INF).min(axis=axes, keepdims=True)
        U = np.where(A1, np.minimum(U, m), U)
        U = np.where(A2, U, INF)
        if it > 2 and np.max(np.abs(np.where(A2, U - Uold, 0))) < 1e-12: break
    U = lip_pass(U, costs)
    gm = np.where(~A2, U - rate, -INF)
    j = np.unravel_index(np.argmax(gm), gm.shape)
    return float(gm[j]), tuple(float(g[k]) for k in j)
if __name__ == "__main__":
    for theta in (0.346, 0.36, 0.38):
        print("theta =", theta)
        for phiP in (0.60, 0.654, 0.70, 0.75):
            row = ["2 blocks: %+.4f" % gain(phiP, 1 - phiP, theta)[0]]
            for frac in (0.5, 0.85):
                phi1 = frac * (1 - phiP)
                gg, at = gain(phiP, phi1, theta)
                row.append("T split %.2f: %+.4f at (%.2f,%.2f,%.2f)" % (frac, gg, *at))
            print("  phiP=%.3f  " % phiP + " | ".join(row)); sys.stdout.flush()
