"""A sub-solution for the upper-bound dynamics (coordinator's exploration; grid numerics, not certified).

Dual upper-bound dynamics: S_{k+1} = lower convex envelope of min(1, Sigma_B(S_k(B))) on [0, tau_{k+1}],
tau_{k+1} = root of S_k(B) = 1 - B/a.  COMPARISON: if S_k >= W on [0, tau_k] with W convex nondecreasing, then
tau_{k+1} <= E(W) := root of W(B) = 1 - B/a, and S_{k+1} >= conv(min(1, Sigma_B(W(B)))) there.  So a family of convex
W_k with
   (S1)  W_{k+1}(B) <= min(1, Sigma_B(W_k(B)))   for B < E(W_k),
   (S2)  W_k convex, nondecreasing, <= 1 on [0, E(W_{k-1})],
   (S0)  S_{k1} >= W_{k1} on [0, tau_{k1}] and tau_{k1} <= E(W_{k1 - 1})
gives tau_{k+1} <= E(W_k) for all k >= k1.  Candidate: W_k = pure_{k - kappa0} (the orbit of the flat line) up to the
point B_t(k) where it reaches a fixed slope level s_t, continued by its tangent line.  Checked here on grids:
convexity of the orbit curve below s_t, (S1), the top condition E(W_k) <= T(W_{k+1}) (T = where the tangent line
reaches slope 1, so that W_{k+1} <= 1 on [0, E(W_k)]), and S_k >= W_k for the grid version of the dynamics.
Usage: python3 ub_subsolution.py pair [s_t - L_h = 0.1] [kappa0 = 0]     pair: gauss | cube:<u>
"""
import math, sys
import numpy as np

pair = sys.argv[1] if len(sys.argv) > 1 else "gauss"
ds = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
kappa0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0

tg = np.linspace(0.0, 1.0, 2000001)[1:-1]
if pair == "gauss":
    Jg = tg - tg * tg
    name = "Gaussian pair"
else:
    u = float(pair.split(":")[1])
    Lam = lambda v: np.log(2 / (1 + np.exp(-v)))
    Jg = Lam(tg * u) - tg * Lam(u)
    name = "cube u = %g" % u
i0 = int(np.argmax(Jg))
h, Lh = float(Jg[i0]), float(tg[i0])
J2 = float((Jg[i0 + 500] - 2 * Jg[i0] + Jg[i0 - 500]) / (tg[i0 + 500] - tg[i0]) ** 2)
Qg = Jg / (1 - tg)
a = float(Qg[-1])
CONST = 2 * math.pi ** 2 * h * h / (-J2)
s_t = Lh + ds


def sigma(B, s):
    target = B / np.maximum(1 - s, 1e-300)
    reg = (s < 1) & (target < Qg[-1])
    tp = np.interp(np.where(reg, target, Qg[0]), Qg, tg)
    return np.where(reg, tp * (1 - s) / (1 - tp), np.inf)


def lower_convex_envelope(x, y):
    hull = []
    for i in range(len(x)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            if (y[i2] - y[i1]) * (x[i] - x[i1]) >= (y[i] - y[i1]) * (x[i2] - x[i1]):
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(x, x[hull], y[hull])


K = 120
d = np.exp(np.linspace(math.log(1e-9 * a), math.log(0.999 * (a - h)), 60001))
B = h + d
# pure orbits from the flat line: pure[j] = slope after j steps (inf once not regular)
pure = [np.zeros_like(B)]
for j in range(1, K + 2):
    pure.append(sigma(B, pure[-1]))


def W_of(k):
    """(B_t, s at B_t, tangent slope m, E, T, array W on the grid) for W_k, or None."""
    j = k - kappa0
    if j < 1:
        return None
    p = pure[j]
    idx = np.where(p >= s_t)[0]
    if len(idx) == 0 or idx[0] < 3:
        return None
    it = idx[0]
    # tangent point: interpolate B_t with p = s_t; slope by a difference just below
    Bt = B[it - 1] + (s_t - p[it - 1]) / (p[it] - p[it - 1]) * (B[it] - B[it - 1])
    m = (p[it - 1] - p[it - 2]) / (B[it - 1] - B[it - 2])
    E = (1 - s_t + m * Bt) / (m + 1 / a)
    T = Bt + (1 - s_t) / m
    W = np.where(B <= Bt, np.where(np.isfinite(p), p, 2.0), s_t + m * (B - Bt))
    conv_ok = bool(np.all(np.diff(p[:it], 2) >= -1e-9 * np.abs(p[1:it - 1]).max()))
    return Bt, m, E, T, W, conv_ok


# the grid version of the true upper-bound dynamics, started from the constant a (S = 0): M_1 = a, M_2 = hull(theta_na)
S = np.zeros_like(B)
tau = a
taus = {1: a}
Ss = {1: S.copy()}
for k in range(2, K + 1):
    f = S - (1 - B / a)
    idx = np.where((B <= tau * (1 + 1e-15)) & (f >= 0))[0]
    tau_new = tau if len(idx) == 0 else (B[idx[0] - 1] + f[idx[0] - 1] / (f[idx[0] - 1] - f[idx[0]]) * (B[idx[0]] - B[idx[0] - 1]) if idx[0] > 0 else B[0])
    reg = B < tau_new
    Sn = np.minimum(1.0, np.maximum(sigma(B[reg], S[reg]), S[reg]))
    Bn = np.concatenate([B[reg], [tau_new]])
    Sn = np.concatenate([Sn, [1.0]])
    S = np.interp(B, Bn, lower_convex_envelope(Bn, Sn), right=1.0)
    tau = tau_new
    taus[k], Ss[k] = tau, S.copy()

print("# %s: h = %.8f a = %.6f L_h = %.5f; s_t = L_h + %.3f, kappa0 = %d; constant %.8f" % (name, h, a, Lh, ds, kappa0, CONST))
print("# (the dynamics here starts from the constant a at level 1, so level k here is level k - 1 of dual_ub_*.py)")
print("#   k   tau_k (dynamics)   E(W_{k-1}) (bound)   k^2(.-h)/const: tau    E      (S1) worst   top: E_k<=T_{k+1}   S_k>=W_k worst   convex")
for k in [3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 60, 80, 100, 120]:
    w0, w1, w2 = W_of(k - 1), W_of(k), W_of(k + 1)
    if w0 is None or w1 is None or w2 is None:
        print("  %4d   (W not defined at this level for these parameters)" % k)
        continue
    Bt, m, E, T, W, cv = w1
    # (S1): W_{k+1} <= min(1, Sigma(W_k)) on B < E_k
    msk = B < E
    img = np.minimum(1.0, sigma(B[msk], np.minimum(W[msk], 1.0)))
    s1 = float(np.min(img - np.minimum(w2[4][msk], 1.0)))
    top_ok = E <= w2[3] * (1 + 1e-12)
    # S_k >= W_k on [h, tau_k]
    dom = B <= taus[k]
    cmp_ = float(np.min(Ss[k][dom] - np.minimum(W[dom], 1.0)))
    print("  %4d   %.10f   %.10f      %.5f  %.5f   %+.2e    %s             %+.2e     %s" % (
        k, taus[k], w0[2], k * k * (taus[k] - h) / CONST, k * k * (w0[2] - h) / CONST, s1, top_ok, cmp_, cv))
