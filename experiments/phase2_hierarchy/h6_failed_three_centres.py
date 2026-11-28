"""
Three-round type game in the small-slope (Gaussian) limit for functions of the
distances to three hidden centres s, s'', s' with prescribed overlaps.

Units: a = 1, h = 1/4.  Types Y in R^3 (orthonormal frame e1 = s, e2, e3 by
Gram-Schmidt), rate |Y|^2.  Lipschitz body K = {g : |<g, a_c>| <= 2, c = 4 classes}.

Round 1 (blind) sees the ball |Y|^2 <= theta; there F = G1(Y1).
Round 2 (knows s) sees the cylinder Y2^2 + Y3^2 <= theta; there F = G2(Y1, Y2).
Round 3 (knows s, s'') sees the slab |Y3| <= sqrt(theta).
Hidden: cone at the vertex X = s'.

Feasibility (derived in the notes): exists G2 on the strip |e2| <= sqrt(theta),
K12-Lipschitz, constant on chords of the disc, with
      T2 + gamma <= -G2 <= cap2,
T2(e1,e2) = 2 X1 e1 + 2 X2 e2 + 2 X3 sqrt(theta - e2^2) - 1,
cap2(e1,e2) = min_{|e3| <= sqrt(theta - e2^2)} ( |e|^2 - dist(e, K/2)^2 ).
We compute U = the largest admissible -G2 and report min (U - T2).
"""
import numpy as np, sys

def frame(pi):
    pi = np.asarray(pi, float); pi = pi / pi.sum()
    s  = np.array([1., 1., 1., 1.])
    s2 = np.array([1., 1., -1., -1.])
    s3 = np.array([1., -1., 1., -1.])
    ip = lambda v, w: float(np.sum(pi * v * w))
    e1 = s / np.sqrt(ip(s, s))
    v = s2 - ip(s2, e1) * e1; e2 = v / np.sqrt(ip(v, v))
    v = s3 - ip(s3, e1) * e1 - ip(s3, e2) * e2; e3 = v / np.sqrt(ip(v, v))
    A = np.stack([e1, e2, e3], axis=1)          # A[c] = a_c  (4 x 3)
    X = np.array([ip(s3, e1), ip(s3, e2), ip(s3, e3)])
    return pi, A, X

def proj_polytope(P, A, iters=400):
    """Dykstra projection of points P (m x 3) onto {g : |<g,a_c>| <= 1}."""
    x = P.copy()
    incr = [np.zeros_like(P) for _ in range(len(A))]
    nrm2 = np.sum(A * A, axis=1)
    for _ in range(iters):
        for c in range(len(A)):
            y = x + incr[c]
            t = y @ A[c]
            excess = np.clip(t, -1, 1) - t
            xn = y + np.outer(excess / nrm2[c], A[c])
            incr[c] = y - xn
            x = xn
    return x

def solve(pi, theta, d=0.02, E1=2.2, verbose=False, sweeps=60):
    pi, A, X = frame(pi)
    rt = np.sqrt(theta)
    if abs(X[2]) <= rt:
        return None
    n2 = int(np.floor(rt / d))
    e2 = np.arange(-n2, n2 + 1) * d
    # make the strip edge exact
    e2 = np.concatenate([[-rt], e2[(e2 > -rt + 1e-12) & (e2 < rt - 1e-12)], [rt]])
    e1 = np.arange(-int(E1 / d), int(E1 / d) + 1) * d
    G1, G2 = np.meshgrid(e1, e2, indexing='ij')
    pts = np.stack([G1.ravel(), G2.ravel()], axis=1)
    N = len(pts)
    # cap2: min over e3 in the cylinder fibre of |e|^2 - dist^2(e, K/2)
    cap = np.full(N, np.inf)
    for frac in np.linspace(-1, 1, 21):
        e3 = frac * np.sqrt(np.maximum(theta - pts[:, 1] ** 2, 0))
        P = np.column_stack([pts, e3])
        Q = proj_polytope(P, A)
        val = np.sum(P * P, axis=1) - np.sum((P - Q) ** 2, axis=1)
        cap = np.minimum(cap, val)
    T2 = 2 * X[0] * pts[:, 0] + 2 * X[1] * pts[:, 1] + 2 * abs(X[2]) * np.sqrt(np.maximum(theta - pts[:, 1] ** 2, 0)) - 1
    # K12 = {(g1,g2): |g1 a_c1 + g2 a_c2| <= 2}; two distinct constraint pairs (class A and class B)
    B = np.unique(np.round(A[:, :2], 12), axis=0)
    assert len(B) == 2, B
    # vertices of K12: solve <g,b1> = +-2, <g,b2> = +-2
    Minv = np.linalg.inv(B)
    W = np.array([Minv @ np.array([2., 2.]), Minv @ np.array([2., -2.])])   # two vertices (others are negatives)
    def h12(v):
        return np.max(np.abs(v @ W.T), axis=-1)
    indisc = (pts[:, 0] ** 2 + pts[:, 1] ** 2 <= theta + 1e-12)
    i1 = np.round(pts[:, 0] / d).astype(int)
    U = cap.copy()
    # precompute pairwise costs in chunks is too large; do sweeps with chunked min-plus
    def lipschitz_reg(U):
        out = U.copy()
        ch = 400
        for a in range(0, N, ch):
            diff = pts[a:a + ch, None, :] - pts[None, :, :]
            cost = np.max(np.abs(diff @ W.T), axis=-1)
            out[a:a + ch] = np.min(U[None, :] + cost, axis=1)
        return out
    for it in range(sweeps):
        Uold = U.copy()
        # chord constraint: on the disc, U depends on e1 only
        for k in np.unique(i1[indisc]):
            m = indisc & (i1 == k)
            U[m] = U[m].min()
        U = lipschitz_reg(U)
        if np.max(np.abs(U - Uold)) < 1e-10:
            break
    marg = U - T2
    j = np.argmin(marg)
    res = dict(margin=float(marg[j]), at=pts[j].tolist(), X=X.tolist(), W=W.tolist(), iters=it,
               margin_cap=float(np.min(cap - T2)))
    if verbose:
        print(res)
    return res

if __name__ == "__main__":
    pi = [float(x) for x in sys.argv[1:5]]
    theta = float(sys.argv[5])
    d = float(sys.argv[6]) if len(sys.argv) > 6 else 0.03
    print(solve(pi, theta, d=d, verbose=False))
