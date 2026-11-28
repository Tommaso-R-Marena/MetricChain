"""
Phase II (adaptive hierarchy) -- open problem 2 probed at finite slope: energies of the distances to three
hidden centres s1, s2, s3 with prescribed overlaps (hidden information that is "distributed": every centre
is a point of the whole cube).

Fine classes: the sites are classified by (t2, t3) = (s1 xor s2, s1 xor s3); class weights w = (w00, w01, w10, w11).
Type of a point: z_c = density of sites of class c where the point differs from s1.  Uniform rate r = sum w_c f(z_c).
   round 1 (blind):              sees  V0 = { r(z) <= theta };                       there F = G1(zbar)        (zbar = d(x,s1)/n)
   round 2 (knows s1):           sees  V1 = { sum w_c KL(z_c || zbar) <= theta };    there F = G2(m_0, m_1)    (means over t2 = 0, 1)
   round 3 (knows s1, s2):       sees  V2 = { sum w_c KL(z_c || m_{t2(c)}) <= theta }
F is any function of the type with |dF| <= u sum w_c |dz_c|  (this contains all F(d1, d2, d3)).
The script builds the pointwise largest U = -F with U <= r on V0 and the two independence constraints, and
reports   gain = max over types outside V2 of [U - r]   in units of h  (generalised Lemma B would say <= 1 - theta/h).
A clearly positive gain at theta > h would be a candidate for a three-round separation; negative gains
support open problem 2 (the relaxation principle for overlapping centres at finite slope).
Continuous model on a grid of step d (no log n terms); region boundaries are rounded to the grid.
"""
import sys, itertools
import numpy as np
LN2 = np.log(2.0)
def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16); return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)
def kl(p, q):
    p = np.clip(p, 1e-300, 1 - 1e-16); q = np.clip(q, 1e-12, 1 - 1e-12)
    return p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))
def consts(u):
    pu = 1 / (1 + np.exp(u)); L1 = np.log(2 / (1 + np.exp(-u))); return pu, L1, f(pu), f(L1 / u)
def lip_pass(U, costs):
    for ax, c in enumerate(costs):
        U = np.moveaxis(U, ax, 0)
        for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + c, out=U[i])
        for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + c, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def group_min(U, mask, key):
    """replace U on mask by the minimum over points of mask with the same integer key"""
    k = key[mask]; v = U[mask]
    order = np.argsort(k, kind='stable'); ks = k[order]; vs = v[order]
    starts = np.r_[0, np.flatnonzero(np.diff(ks)) + 1]
    mins = np.minimum.reduceat(vs, starts)
    out = np.empty_like(vs); idx = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(ks)]))
    out[order] = mins[idx]
    U2 = U.copy(); U2[mask] = np.minimum(v, out)
    return U2
def run(u, wts, theta_over_h, N=20, iters=300):
    pu, L1, a, h = consts(u); theta = theta_over_h * h
    w = np.array(wts, float); w = w / w.sum()
    g = np.arange(N + 1) / N
    Z = np.meshgrid(g, g, g, g, indexing='ij')
    I = np.meshgrid(*[np.arange(N + 1)] * 4, indexing='ij')
    wi = np.round(w * 1000).astype(np.int64)                 # integer weights for exact keys
    r = sum(w[c] * f(Z[c]) for c in range(4))
    zbar = sum(w[c] * Z[c] for c in range(4))
    key1 = sum(wi[c] * I[c] for c in range(4))
    w0, w1 = w[0] + w[1], w[2] + w[3]                         # cells t2 = 0 (classes 00, 01) and t2 = 1 (10, 11)
    m0 = (w[0] * Z[0] + w[1] * Z[1]) / w0; m1 = (w[2] * Z[2] + w[3] * Z[3]) / w1
    k0 = wi[0] * I[0] + wi[1] * I[1]; k1 = wi[2] * I[2] + wi[3] * I[3]
    key2 = k0 * (int(k1.max()) + 1) + k1
    cost1 = sum(w[c] * kl(Z[c], zbar) for c in range(4))
    cost2 = w[0] * kl(Z[0], m0) + w[1] * kl(Z[1], m0) + w[2] * kl(Z[2], m1) + w[3] * kl(Z[3], m1)
    V0 = r <= theta + 1e-12; V1 = cost1 <= theta + 1e-12; V2 = cost2 <= theta + 1e-12
    costs = tuple(u * w[c] / N for c in range(4))
    INF = 1e9
    U = np.where(V0, r, INF)
    for it in range(iters):
        Uold = U.copy()
        U = lip_pass(U, costs)
        U = group_min(U, V0, key1)
        U = group_min(U, V1, key2)
        if it > 2 and np.max(np.abs(U - Uold)) < 1e-11: break
    hidden = ~V2
    gain = float((U - r)[hidden].max())
    j = np.unravel_index(np.argmax(np.where(hidden, U - r, -INF)), r.shape)
    vis2 = float((U - r)[V2].max())                          # largest log-mass on what round 3 sees
    return gain / h, vis2 / h, tuple(float(g[x]) for x in j), it

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    parts = [p for p in itertools.product(range(1, 8), repeat=4) if sum(p) == 10]
    print("gain/h = max over types hidden from round 3 of (U - r)/h, blind-visible maximum normalised to 0; grid N = %d" % N)
    for u in (1.0, 2.0, 4.0):
        pu, L1, a, h = consts(u)
        for th in (1.0, 1.3):
            res = []
            for p in parts:
                gn, v2, at, it = run(u, [x / 10 for x in p], th, N=N)
                res.append((gn, p, at, v2))
            res.sort(key=lambda t: -t[0])
            print("u=%.0f theta=%.1fh (1 - theta/h = %+.2f): %d weight vectors; five largest gains/h:" % (u, th, 1 - th, len(res)))
            for gn, p, at, v2 in res[:5]:
                print("     gain/h %+.3f   weights (w00,w01,w10,w11) = %s/10   hidden type %s   (largest round-3-visible log-mass/h %+.3f)" % (gn, p, at, v2))
            print("     smallest gain/h %+.3f" % res[-1][0])
            sys.stdout.flush()
