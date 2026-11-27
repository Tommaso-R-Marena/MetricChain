"""Referee A, test 3 (item 5 of the brief): the exact dynamics of convex majorants of remark (1), section 5 --
own code, semi-analytic (no B-grid):

   S_0 = 0 on [0, a];   tau_{k+1} = root of S_k(B) = 1 - B/a;
   S_{k+1} = lower convex envelope of min(1, H_k) on [0, tau_{k+1}],  H_k(B) = Sigma(B, S_k(B)),  value 1 at tau_{k+1}
           = H_k on [0, Bc], then the tangent line of H_k through (tau_{k+1}, 1).

S_k is stored as a list of cuts (Bc, S(Bc), slope); S_k(B) and its derivative are evaluated by descending to the
level whose linear part contains B and applying the slope map (with its partial derivatives) on the way back.
The tangent point is found by bisection on  H(B) + H'(B)(tau - B) - 1  (nondecreasing in B, by convexity of H).
T_k <= M_{S_k, tau_k} for all k by Proposition U + Corollary U' (tau_k here is the UPPER bound for sup T_k).

Usage: python3 a3_dual_dynamics.py gauss|cube:u [K]
"""
import math, sys

pair = sys.argv[1] if len(sys.argv) > 1 else "gauss"
K = int(sys.argv[2]) if len(sys.argv) > 2 else 320
NBIS = 70

if pair == "gauss":
    a, h, L, vartheta = 1.0, 0.25, 0.5, 0.5

    def sig3(B, s):
        """(Sigma, dSigma/dB, dSigma/ds); inf if not regular."""
        y = 1.0 - s
        if y - B <= 0:
            return math.inf, math.inf, math.inf
        d = y - B
        return B * y / d, y * y / (d * d), B * B / (d * d)
else:
    u = float(pair.split(":")[1])
    pu = 1.0 / (1.0 + math.exp(u))
    kl = lambda x, p: x * math.log(x / p) + (1 - x) * math.log((1 - x) / (1 - p))
    a = kl(pu, 0.5)
    # theta in the parameter rho in [pu, 1/2]: e = KL(rho||pu), theta = KL(rho||1/2), dtheta/de = l/(l + u), l = ln(rho/(1-rho)) < 0
    # tangent of theta at e: intercept kappa = theta - e theta' ; slope theta' in (-inf, 0]
    def tangent(rho):
        l = math.log(rho / (1 - rho))
        e = kl(rho, pu); th = kl(rho, 0.5)
        dth = l / (l + u)                     # l + u > 0 for rho > pu ; dth <= 0
        return e, th, dth

    def sig3(B, s):
        y = 1.0 - s
        if B >= y * a:
            return math.inf, math.inf, math.inf
        if B <= 0:
            return 0.0, 0.0, 0.0              # (derivative at B = 0 not needed)
        # maximiser e*: theta(e) - e theta'(e) = B/y  (decreasing in e, i.e. in rho)
        target = B / y
        lo, hi = pu, 0.5
        for _ in range(NBIS):
            mid = 0.5 * (lo + hi)
            e, th, dth = tangent(mid)
            if th - e * dth > target:
                lo = mid
            else:
                hi = mid
        e, th, dth = tangent(0.5 * (lo + hi))
        return -y * dth, 1.0 / e, th / e

    # h, L, vartheta from J(t) = Lam(tu) - t Lam(u)
    Lam = lambda v: math.log(2 / (1 + math.exp(-v)))
    J = lambda t: Lam(t * u) - t * Lam(u)
    lo, hi = 0.0, 1.0
    for _ in range(NBIS):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if J(m1) < J(m2):
            lo = m1
        else:
            hi = m2
    L = 0.5 * (lo + hi); h = J(L)
    d = 1e-4
    vartheta = -1.0 / ((J(L + d) - 2 * J(L) + J(L - d)) / d ** 2)

const = 2 * math.pi ** 2 * h * h * vartheta
cuts = []          # cuts[k-1] = (Bc, Sc, m, tau) of S_k, k >= 1 ; S_k(B) = Sc + m (B - Bc) for B >= Bc


def S(k, B):
    """(S_k(B), S_k'(B)).  S_0 = 0."""
    i = k
    while i >= 1 and B < cuts[i - 1][0]:
        i -= 1
    if i == 0:
        val, der = 0.0, 0.0
    else:
        Bc, Sc, m, _ = cuts[i - 1]
        val, der = Sc + m * (B - Bc), m
    for _ in range(i, k):
        v, dB, ds = sig3(B, val)
        if not math.isfinite(v):
            return math.inf, math.inf
        val, der = v, dB + ds * der
    return val, der


def H(k, B):
    v, d = S(k, B)
    if not math.isfinite(v):
        return math.inf, math.inf
    w, dB, ds = sig3(B, v)
    if not math.isfinite(w):
        return math.inf, math.inf
    return w, dB + ds * d


tau = a
print("# %s: a = %.8f h = %.8f L = %.6f vartheta = %.6f const = %.8f" % (pair, a, h, L, vartheta, const))
print("#   k   tau_k (upper bound)      k^2 (tau_k - h)/const    Bc(k)          S_k(Bc)     slope m_k")
show = set([1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 55, 60, 80, 85, 100, 120, 160, 200, 240, 320, 400, 640])
for k in range(1, K + 1):
    # tau_k = root of S_{k-1}(B) = 1 - B/a on [0, tau_{k-1}]   (S_{k-1}(B) + B/a is increasing)
    lo, hi = 0.0, tau
    for _ in range(NBIS):
        mid = 0.5 * (lo + hi)
        if S(k - 1, mid)[0] + mid / a < 1.0:
            lo = mid
        else:
            hi = mid
    tau = 0.5 * (lo + hi)
    # tangent point of H_{k-1} from (tau, 1): G(B) = H + H'(tau - B) - 1 nondecreasing ; root, or Bc = 0 if G(0+) >= 0
    def Gf(B):
        v, d = H(k - 1, B)
        if not math.isfinite(v):
            return math.inf
        return v + d * (tau - B) - 1.0
    lo, hi = 0.0, tau
    eps0 = 1e-13 * tau
    if Gf(eps0) >= 0:
        Bc, Sc, m = 0.0, 0.0, 1.0 / tau
    else:
        lo = eps0
        for _ in range(NBIS):
            mid = 0.5 * (lo + hi)
            if Gf(mid) < 0:
                lo = mid
            else:
                hi = mid
        Bc = lo
        Sc, m = H(k - 1, Bc)
        m = (1.0 - Sc) / (tau - Bc)          # the chord to (tau, 1); equals H' at the tangent point up to rounding
    cuts.append((Bc, Sc, m, tau))
    if k in show:
        print("  %4d  %.12f       %.6f               %.9f   %.6f   %.5e" % (k, tau, k * k * (tau - h) / const, Bc, Sc, m))
        sys.stdout.flush()
