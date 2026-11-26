"""The upper-bound dynamics in dual variables for the cube (coordinator's check; a grid approximation, NOT one-sided).
Same dynamics as dual_ub_gauss.py:  tau' = root of S(B) = 1 - B/a;  S~(B) = min(1, Sigma_B(S(B))) for B < tau',
S~(tau') = 1;  S' = lower convex envelope of S~ on [h, tau'].  The slope map through the dual function
J(t) = Lambda(t u) - t Lambda(u):  t' = Q^{-1}(B/(1 - s)),  s' = t' (1 - s)/(1 - t'),  Q = J/(1 - t).
Start: M_1 = hull(theta_na) = max(theta_na(x), a - x): for intercepts below that of the tangent at the kink the
slope of the tangent line of theta_na (= Sigma_B(0)), above it the pencil through the kink (x_c, a - x_c).
Usage: python3 dual_ub_cube.py [u=1] > out_dual_ub_cube_u1.txt
"""
import math, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0


def kl(x, y):
    return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))


pu = 1 / (1 + math.exp(u))
lam1 = math.log(2 / (1 + math.exp(-u)))
rho_h = lam1 / u
a, h = float(kl(pu, 0.5)), float(kl(rho_h, 0.5))
H2 = 1 / (u * u * rho_h * (1 - rho_h))
CONST = 2 * math.pi ** 2 * h * h * H2
Lam = lambda v: np.log(2 / (1 + np.exp(-v)))
tgrid = np.linspace(0.0, 1.0, 2000001)[1:-1]
Jg = Lam(tgrid * u) - tgrid * Lam(u)
Qg = Jg / (1 - tgrid)                                  # increasing from 0 to a


def sigma(B, s):
    """slope map, vectorised; +inf where the line is not regular (B >= (1 - s) a)."""
    target = B / np.maximum(1 - s, 1e-300)
    reg = (s < 1) & (target < Qg[-1])
    tp = np.interp(np.where(reg, target, Qg[0]), Qg, tgrid)
    out = tp * (1 - s) / (1 - tp)
    return np.where(reg, out, np.inf)


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


# the kink of hull(theta_na): kappa(rho_c) = a - e(rho_c)
# (x + theta_na(x) starts at a, decreases until the slope of theta_na is -1, i.e. rho = 1/(1 + e^{u/2}), and returns
#  to a at x_c; for the slopes used here eps* > a, so the return happens before eps*)
lo, hi = 1 / (1 + math.exp(u / 2)), 0.5
assert float(kl(hi, 0.5)) + float(kl(hi, pu)) > a, "eps* <= a: the hull of theta_na is (a - x)_+ and this start is not coded"
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if float(kl(mid, 0.5)) + float(kl(mid, pu)) > a else (mid, hi)
rho_c = hi
x_c = float(kl(rho_c, pu))
lam_c = math.log((1 - rho_c) / rho_c)
s_c = lam_c / (u - lam_c)
B_c = float(kl(rho_c, 0.5)) + s_c * x_c


def run(K, npts=40001):
    d = np.concatenate([[0.0], np.exp(np.linspace(math.log(1e-11 * a), math.log(a - h), npts))])
    B = h + d
    S = np.where(B <= B_c, sigma(B, np.zeros_like(B)), (B - a + x_c) / x_c)
    S = np.minimum(S, 1.0)
    tau = a
    out = {1: tau}
    for k in range(2, K + 1):
        f = S - (1 - B / a)
        idx = np.where((B <= tau + 1e-15) & (f >= 0))[0]
        if len(idx) == 0:
            tau_new = tau
        else:
            j = idx[0]
            tau_new = B[0] if j == 0 else B[j - 1] + f[j - 1] / (f[j - 1] - f[j]) * (B[j] - B[j - 1])
        out[k] = tau_new
        reg = B < tau_new
        Sn = np.minimum(1.0, np.maximum(sigma(B[reg], S[reg]), S[reg]))
        Bn = np.concatenate([B[reg], [tau_new]])
        Sn = np.concatenate([Sn, [1.0]])
        S = np.interp(B, Bn, lower_convex_envelope(Bn, Sn), right=1.0)
        tau = tau_new
    return out


def table(fname, col):
    o = {}
    p = os.path.join(HERE, fname)
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r"^\s*(\d+)\s+(\d\.\d+)", line)
            if m:
                o.setdefault(int(m.group(1)), float(m.group(2)))
    return o


ub = run(160)
grid = table("out_iterate_cube1_120.txt", 1) if abs(u - 1) < 1e-12 else {}
print("# cube u = %g: a = %.8f h = %.8f; kink of hull(theta_na) at x_c = %.6f (B_c = %.6f); constant %.8f" % (u, a, h, x_c, B_c, CONST))
print("#   k   tau (grid recursion)   tau^UB (dual dynamics)   k^2(tau-h)/const: grid     UB")
for k in list(range(2, 13)) + [15, 20, 30, 40, 55, 80, 100, 120, 160]:
    g = grid.get(k)
    print("  %4d   %s   %.10f     %s  %.5f" % (k, ("%.10f" % g) if g else "     -      ", ub[k],
          ("%.5f" % (k * k * (g - h) / CONST)) if g else "   -   ", k * k * (ub[k] - h) / CONST))
