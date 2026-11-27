"""Coordinator's check of the weak-coupling coefficient of SCI-RES-0033 section 4a (science division).

Their statement (a derivation at fixed block length, not a proof): for the symmetric binary chain
with flip probability p as known part, K = ln((1-p)/p), t = tanh(u/2), the increment of the
site-wise optimum of the block quantity is  a_cube(u) + (K^2/4) F*(u) + O(K^4),
    F*(u) = t^4 (1 - t^4)/2 - u t^3 (1 - t^2) + (1 - t^2)^2 (u - t (1 + t^2))^2 / (2 t^2),
with one sign change at u0 = 1.505534.

Checked here: (1) the root of F* by bisection, and that it is the only sign change on a grid;
(2) the second-order coefficient by a brute-force computation of our own: the capacity of the
channel W(s | tau) ~ exp(J sum s_{i-1} s_i + h sum tau_i s_i) over the 2^L site-wise labels
(Blahut-Arimoto), increments in L, second difference in K -- written from the statement, not from
their script; (3) the value at (p, u) = (0.4, 1) against the bracket [0.1168, 0.1215] for a_infinity
in the theory report, Proposition 11.117(a).
"""
import itertools, math
import numpy as np

def Fstar(u):
    t = math.tanh(u / 2)
    return t**4 * (1 - t**4) / 2 - u * t**3 * (1 - t * t) + (1 - t * t)**2 * (u - t * (1 + t * t))**2 / (2 * t * t)

def a_cube(u):
    # non-adaptive exponent at accuracy zero of the cube: capacity of a binary symmetric channel
    # with flip probability p_u = 1/(1 + e^u):  ln 2 - H(p_u)   (theory report: a = KL(p_u || 1/2))
    q = 1 / (1 + math.exp(u))
    return math.log(2) + q * math.log(q) + (1 - q) * math.log(1 - q)

def capacity_sitewise(L, K, u, iters=400000):
    """Capacity (nats) of the channel with inputs tau in {+-1}^L and outputs s in {+-1}^L,
    W(s | tau) proportional to exp(J sum_{i} s_{i-1} s_i + h sum_i tau_i s_i), J = K/2, h = u/2,
    free boundary.  Blahut-Arimoto with a duality check."""
    J, h = K / 2, u / 2
    S = np.array(list(itertools.product((-1, 1), repeat=L)), dtype=float)
    bond = (S[:, :-1] * S[:, 1:]).sum(axis=1)                     # sum s_{i-1} s_i
    logW = J * bond[None, :] + h * (S @ S.T)                      # rows: tau, columns: s
    logW -= np.log(np.exp(logW).sum(axis=1, keepdims=True))
    W = np.exp(logW)
    M = np.full(len(S), 1.0 / len(S))
    for _ in range(iters):
        Q = M @ W
        D = (W * (logW - np.log(Q)[None, :])).sum(axis=1)         # KL(W_tau || Q)
        Mn = M * np.exp(D); Mn /= Mn.sum()
        M = Mn
        if _ % 200 == 0:
            Q = M @ W
            D = (W * (logW - np.log(Q)[None, :])).sum(axis=1)
            if D.max() - M @ D < 2e-12: break
    Q = M @ W
    D = (W * (logW - np.log(Q)[None, :])).sum(axis=1)
    lo, hi = float(M @ D), float(D.max())
    return lo, hi

ok = True
# (1) root and sign pattern
a, b = 1.0, 2.0
for _ in range(80):
    m = (a + b) / 2
    if Fstar(a) * Fstar(m) <= 0: b = m
    else: a = m
u0 = (a + b) / 2
grid = np.arange(0.02, 40.0, 0.001)
vals = np.array([Fstar(x) for x in grid]); signs = np.sign(vals)
where = [float(grid[i]) for i in range(len(grid) - 1) if signs[i] != signs[i + 1]]
print("root of F*: u0 = %.6f (quoted 1.505534);  sign changes of F* on [0.02, 40), step 0.001, in floating point: at %s;  F*(1) = %.5f, F*(2) = %.5f" % (u0, ["%.3f" % w for w in where], Fstar(1.0), Fstar(2.0)))
# beyond u ~ 36 the three terms cancel below rounding (1 - t^2 ~ 4 e^{-u} < 1e-15); check the sign there
# from the normalised form F*/(1 - t^2), whose limit is 1 - u:
def Fnorm(u):
    t = math.tanh(u / 2); w = 4 * math.exp(-u) / (1 + math.exp(-u))**2      # 1 - t^2, computed stably
    return t**4 * (1 + t * t) / 2 - u * t**3 + w * (u - t * (1 + t * t))**2 / (2 * t * t)
nsigns = np.sign([Fnorm(x) for x in grid])
nwhere = [float(grid[i]) for i in range(len(grid) - 1) if nsigns[i] != nsigns[i + 1]]
print("   the same with F*/(1 - t^2) computed stably: sign changes at %s;  value at u = 40: %.3f (limit 1 - u)" % (["%.3f" % w for w in nwhere], Fnorm(40.0)))
ok &= abs(u0 - 1.505534) < 2e-6 and len(nwhere) == 1 and Fstar(1.0) > 0 > Fstar(2.0)

# (2) brute force: increment of the site-wise capacity in L, coefficient of K^2
print("brute force (own Blahut-Arimoto over the 2^L site-wise labels): [cap_{L+1} - cap_L - a_cube] / (K^2/4)  against F*(u)")
for u in (0.8, 1.2, 1.505534, 1.8, 2.5):
    row = []
    for p in (0.49, 0.495):
        K = math.log((1 - p) / p)
        c = {}
        for L in (4, 5):
            lo, hi = capacity_sitewise(L, K, u)
            assert hi - lo < 1e-10, (hi - lo)   # duality gap of the capacity
            c[L] = lo
        row.append((c[5] - c[4] - a_cube(u)) / (K * K / 4))
    print("   u = %.4f:  p = 0.49: %+.6f   p = 0.495: %+.6f   F*(u) = %+.6f" % (u, row[0], row[1], Fstar(u)))
    ok &= abs(row[1] - Fstar(u)) < 2e-4
# control: K = 0 gives the cube
lo, hi = capacity_sitewise(4, 0.0, 1.0)
print("control K = 0, L = 4, u = 1: capacity per site %.9f, a_cube %.9f" % (lo / 4, a_cube(1.0)))
ok &= abs(lo / 4 - a_cube(1.0)) < 1e-9

# (3) against the bracket of Proposition 11.117(a)
K = math.log(0.6 / 0.4)
val = a_cube(1.0) + K * K / 4 * Fstar(1.0)
print("second-order value at (p, u) = (0.4, 1): %.4f;  theory report bracket for a_infinity: [0.1168, 0.1215]  -> %s" % (val, "inside" if 0.1168 <= val <= 0.1215 else "OUTSIDE"))
ok &= 0.1168 <= val <= 0.1215
K = math.log(0.7 / 0.3)
print("for comparison (p, u) = (0.3, 1): %.4f against the bracket [0.1264, 0.1409] (K = %.2f: outside the range of the expansion)" % (a_cube(1.0) + K * K / 4 * Fstar(1.0), K))
print("RESULT:", "ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
