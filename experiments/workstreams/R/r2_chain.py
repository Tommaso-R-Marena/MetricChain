"""R2: the restarted sub-solution chain of the upper bound (R_REPORT.md, section 6-8), followed numerically.

Restart at a level k1 with tau_{k1} <= b_0 = h + eps1  (T_{k1} <= b_0, the flat majorant: W_0 = 0 on [0, b_0]).
W_j = p_j (pure orbit curve) up to the point B_t(j) where it reaches the level s_t, continued by its tangent line
(slope m_j).  b_{j+1} = min(b_j, E_j), E_j the root of W_j(B) = 1 - B/a.  RANGE CONDITION: W_{j+1}(b_{j+1}) <= 1.
If it holds for all j, then tau_{k1 + j} <= b_j for all j  (Proposition U + Lemma T + Lemma RC of the report).

Prints, for each j in a list: case (A: p_j(b_0) <= s_t; B otherwise), B_t(j) - h, m_j, E_j - h, b_j - h, the value
W_{j+1}(b_{j+1}) (must be <= 1), j^2 (b_j - h)/const, and the ratio m_{j+1}/m_j against the bound used in the proof.
Usage: python3 r2_chain.py pair s_t-L eps1 [J]
"""
import math, sys
from rlib import Gauss, Cube

pair = sys.argv[1] if len(sys.argv) > 1 else "gauss"
dst = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
eps1 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
Jmax = int(sys.argv[4]) if len(sys.argv) > 4 else 400
P = (Gauss() if pair == "gauss" else Cube(float(pair.split(":")[1]))).setup()
h, L, a = P.h, P.L, P.a
s_t = L + dst
b0 = h + eps1
assert s_t < 1 - h / a and b0 < (1 - s_t) * a

# (C1), (C2) of Lemma RC
S_h = P.sigma(h, s_t)
lo, hi = L, s_t
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if P.sigma(h, mid) < s_t:
        lo = mid
    else:
        hi = mid
sig_star = 0.5 * (lo + hi)
lam = P.sigma_grad(h, sig_star)[2]
c2 = (S_h - s_t) + lam * (1 - s_t - h / a)
print("# %s: h = %.8f L = %.6f a = %.6f const = %.8f;  s_t = L + %.3f, b_0 = h + %.4g" % (P.name, h, L, a, P.const, dst, eps1))
print("# (C1) Sigma(h, s_t) = %.5f < 1 : %s;   (C2) D(h, s_t) + lambda (1 - s_t - h/a) = %.5f < 1 - s_t = %.5f : %s   (sigma_* = %.5f, lambda = %.4f)"
      % (S_h, S_h < 1, c2, 1 - s_t, c2 < 1 - s_t, sig_star, lam))


def Bt_and_slope(j):
    """B_t(j) (p_j = s_t) by bisection on [h, b0] and dp_j/dB there; None if p_j(b0) <= s_t (case A)."""
    if P.orbit_with_slope(b0, j)[0] <= s_t:
        return None
    lo, hi = h, b0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if P.orbit_with_slope(mid, j)[0] <= s_t:
            lo = mid
        else:
            hi = mid
    return lo, P.orbit_with_slope(lo, j)[1]


print("#    j case   B_t(j)-h       m_j          E_j-h        b_j-h        W_{j+1}(b_{j+1})  j^2(b_j-h)/const   m_{j+1}/m_j  bound")
b = b0
info = {}
ok = True
worst = 0.0
show = set([1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 400, 600, 800, 1000])
cur = Bt_and_slope(1)
for j in range(1, Jmax + 1):
    nxt = Bt_and_slope(j + 1)
    if cur is None:
        E = math.inf
        b_next = b
    else:
        Bt, m = cur
        E = Bt + (1 - s_t - Bt / a) / (m + 1 / a)
        b_next = min(b, E)
    # W_{j+1}(b_next)
    if nxt is None:
        Wn = P.orbit_with_slope(b_next, j + 1)[0]
        ratio = bound = float("nan")
    else:
        Bt1, m1 = nxt
        Wn = P.orbit_with_slope(b_next, j + 1)[0] if b_next <= Bt1 else s_t + m1 * (b_next - Bt1)
        if cur is not None:
            sig1 = P.orbit_with_slope(Bt1, j)[0]
            _, gB, gs = P.sigma_grad(Bt1, sig1)
            ratio, bound = m1 / cur[1], gs + gB / cur[1]
        else:
            ratio = bound = float("nan")
    worst = max(worst, Wn)
    if Wn > 1 + 1e-12:
        ok = False
    if j in show or Wn > 1 + 1e-12:
        print("  %5d  %s   %.6e  %.5e  %.6e  %.6e   %.6f         %.5f           %.4f     %.4f" % (
            j, "A" if cur is None else "B", (cur[0] - h) if cur else float("nan"), cur[1] if cur else float("nan"),
            E - h, b - h, Wn, j * j * (b - h) / P.const, ratio, bound))
    b = b_next
    cur = nxt
print("# range condition W_{j+1}(b_{j+1}) <= 1 for all j <= %d: %s  (largest value %.6f)" % (Jmax, ok, worst))
