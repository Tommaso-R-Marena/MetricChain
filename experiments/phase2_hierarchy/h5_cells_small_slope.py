"""
Three-round type game with level-1 cells, CORRECT cap (shifted normalisation: total visible mass = 0):
   cap(y,q,w) = max_j [ partial sums of (Y_i^2 - R_i) ]_+   with R = (R1, R2, 0)
   hidden gain = U_ext(Y) - |Y|^2  (the special leaf has multiplicity one),  need > 0.
Visible regions (budget theta):
   W1 = { y^2+q^2+w^2 <= theta }                              F = G1(y)
   W2 = { min(y^2,R1) + q^2 + w^2 <= theta }                  F = G2(y,q)
   W3 = { min(y^2,R1) + min(q^2,R2) + w^2 <= theta }          twins agree
"""
import numpy as np, sys
def lip_pass(U, costs):
    for ax, c in enumerate(costs):
        U = np.moveaxis(U, ax, 0)
        n = U.shape[0]
        for i in range(1, n):
            np.minimum(U[i], U[i - 1] + c, out=U[i])
        for i in range(n - 2, -1, -1):
            np.minimum(U[i], U[i + 1] + c, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def solve(sig, R1, R2, theta, d=0.01, lim=1.25, iters=300):
    g = np.arange(0, lim + 1e-9, d)
    Y, Q, W = np.meshgrid(g, g, g, indexing='ij')
    rate = Y**2 + Q**2 + W**2
    p1 = Y**2 - R1; p2 = p1 + Q**2 - R2; p3 = p2 + W**2
    cap = np.maximum(np.maximum(np.maximum(p1, p2), p3), 0)
    W1 = rate <= theta + 1e-12
    W2 = (np.minimum(Y**2, R1) + Q**2 + W**2 <= theta + 1e-12)
    W3 = (np.minimum(Y**2, R1) + np.minimum(Q**2, R2) + W**2 <= theta + 1e-12)
    costs = tuple(2 * s * d for s in sig)
    INF = 1e9
    U = np.where(W3, cap, INF)
    for it in range(iters):
        Uold = U.copy()
        U = lip_pass(U, costs)
        m = np.where(W1, U, INF).min(axis=(1, 2), keepdims=True)
        U = np.where(W1, np.minimum(U, m), U)
        m = np.where(W2, U, INF).min(axis=2, keepdims=True)
        U = np.where(W2, np.minimum(U, m), U)
        if np.max(np.abs(np.where(Uold < INF / 2, Uold - U, 0))) < 1e-12 and it > 2:
            break
    U = lip_pass(U, costs)
    gainmap = np.where(~W3, U - rate, -INF)
    j = np.unravel_index(np.argmax(gainmap), gainmap.shape)
    return dict(gain=float(gainmap[j]), at=(float(g[j[0]]), float(g[j[1]]), float(g[j[2]])), iters=it)
if __name__ == "__main__":
    a = [float(x) for x in sys.argv[1:]]
    phi1, phi2, R1, R2, theta = a[:5]
    d = a[5] if len(a) > 5 else 0.01
    print(solve((np.sqrt(phi1), np.sqrt(phi2), np.sqrt(1 - phi1 - phi2)), R1, R2, theta, d=d))
