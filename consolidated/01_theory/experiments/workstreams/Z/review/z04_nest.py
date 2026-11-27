#!/usr/bin/env python3
"""z04: (iv) of the brief -- a small nest of Z_REPORT.md sections 4-6 evaluated exactly, against the types of Propositions
Z3 and Z4 at every node and against the unrolled bound of section 6 at the top.

    F_0      a base that SATURATES the flat type b_0 with least accuracy 1:  ln cost = d b_0 + E_0(d, x; ln(1/delta) + d ln 2)
    Z_j      = Z[F_j]  (Proposition Z3): for x >= X = X_0(N) + 1 the level L(d; n_o, y/n_o) of Lemma Z2 over F_j at the n_o that
               minimises the proxy Pi_j (lines: the grid family of W_j at horizon N); enumeration for d <= d_min
    F_{j+1}  = Zhat[F_j; alpha] (Proposition Z4): the chain T[Z_j; alpha, m_{j+1}] of Q2_REPORT section 4 for alpha <= x < X
               (two-rung levels with outer block m, coarse rung served by Z_j at X, fine rung by the chain itself in dimension
               d - m; the real base bracket of Q below d_0), and Z_j for x >= X.
    output   F_k(n, eps^, delta);   alpha = 1 for j + 1 < k, eps^ for the top.

Every level is evaluated EXACTLY with the constants of Theorem 11.56 (evaluator of the referee of Q2, Q2/review/rlib.py),
each with its own failure probability delta' = delta/(4 L Mbar) handed down; nothing is cached across failure probabilities.
The chain (W_j, b_j) is this review's (zrev.py).  Blocks m_j: "design" = the least block with (4.1) of Q2 at the entry value of
Lambda in the unrolling of section 6 (then Delta_T = 0 at the top); or "design/f" = that block divided by f (then Delta_T > 0
and the term j(d) Delta_T of Proposition Z4 is exercised).

Checked at EVERY node (each at its own (d, x, delta), with Lambda = ln(1/delta) + d ln 2):
  Z-nodes:     accuracy <= x;  (U-inf) with the inner error function;  delta' bookkeeping of Lemma Z2;
               the type of Proposition Z3:  ln cost <= max_{grid W_{j+1}} [d B - sigma x] + E^+(d, x; Lambda)
  chain nodes: accuracy <= a_d <= alpha;  delta' bookkeeping of Proposition T(ii);
               Proposition T(iii):  ln cost <= d b_{j+1} + E^+(d, X; Lam*) + A_T(d, Lam*) + j(d) Delta_T(d, Lam*);
               the type of Proposition Z4 at x = alpha and at x just below X
  top:         ln cost <= n b_k + Ehat_k(n, eps^; Lambda_0)  (the composed error functions)  <= the unrolled bound of section 6.
A base level J0 > 0 (last argument) replaces the flat base by a base that saturates the type H^infty(grid of W_{J0}; E_0): then
the levels above work with sloped lines and extensive outer blocks, and inner calls at accuracies >= X go to the levels Z_j
(for a flat base and few levels every inner call is at an accuracy below X and goes to a chain).
Usage: python3 z04_nest.py u n k [blockdiv] [Ename] [eps] [ln delta] [seconds] [J0]
"""
import math
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
import zrev
import zlev

RL = zlev.RL
LN2 = math.log(2.0)
u = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
k = int(sys.argv[3]) if len(sys.argv) > 3 else 2
BDIV = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
ENAME = sys.argv[5] if len(sys.argv) > 5 else "0"
eps = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
ld_top = float(sys.argv[7]) if len(sys.argv) > 7 else math.log(0.05)
TMAX = float(sys.argv[8]) if len(sys.argv) > 8 else 270.0
J0 = int(sys.argv[9]) if len(sys.argv) > 9 else 0        # the base saturates the type H^infty(grid of W_{J0}; E_0); J0 = 0: flat type b_0
PAR = {0.5: (0.05, 0.0008), 1.0: (0.05, 0.003), 2.0: (0.05, 0.01), 4.0: (0.04, 0.02)}
dst, eps1 = PAR[u]
cu = zrev.Cube(u)
rc = RL.Cube(u)
C = zrev.Chain(cu, dst, eps1, J0 + k + 2)
assert C.range_ok
N = n
dm = zlev.dmin(u)
calX = zlev.X0(u, N) + 1
eh = min(eps, 1.0)
EFUNS = {"0": lambda d, x, Lam: 0.0, "lnLam": lambda d, x, Lam: math.log(Lam), "Lam/7": lambda d, x, Lam: Lam / 7.0,
         "3sqrt(d)": lambda d, x, Lam: 3 * math.sqrt(d), "5/x+lnLam": lambda d, x, Lam: 5.0 / x + math.log(Lam)}
E0 = EFUNS[ENAME]
t_start = time.time()


class Stat:
    def __init__(self):
        self.n, self.least, self.viol = {}, {}, {}

    def add(self, name, exact, bound, tag=None):
        self.n[name] = self.n.get(name, 0) + 1
        sl = bound - exact
        if sl < self.least.get(name, (1e300, None))[0]:
            self.least[name] = (sl, tag)
        if sl < -1e-9:
            self.viol[name] = self.viol.get(name, 0) + 1


ST = Stat()


class TimeUp(Exception):
    pass


class Base:
    """saturates the type H^infty(grid of W_{J0} at horizon N; E_0) (for J0 = 0: the flat type b_0), least accuracy 1"""

    def __init__(self, J0):
        Bs, Ws = C.grid(J0, N)
        self.lines = zlev.Lines(Bs, np.minimum(Ws, 1.0))
        self.level = J0

    def Ehat(self, d, x, Lam):
        return E0(d, x, Lam)

    def cost(self, d, xs, ld):
        Lam = -ld + d * LN2
        xs = np.atleast_1d(np.asarray(xs, dtype=np.float64))
        return self.lines.major(d, xs) + np.array([E0(d, x, Lam) for x in xs])


class ZFam:
    """F_{j+1} = Zhat[F_j; alpha]: chain T[Z_j; alpha, m] for alpha <= x < X, Z_j = Z[F_j] for x >= X."""

    def __init__(self, inner, j, alpha, m):
        self.inner, self.j, self.alpha, self.m = inner, j, alpha, m
        self.level = j + 1
        Bs, Ws = C.grid(j, N)
        self.lines = zlev.Lines(Bs, np.minimum(Ws, 1.0))             # the lines of F_j (proxy)
        Bn, Wn = C.grid(j + 1, N)
        self.nxt = zlev.Lines(Bn, np.minimum(Wn, 1.0))               # the lines of the type of Z_j and of F_{j+1}
        self.Bp = C.b[j + 1]
        self.ch = RL.Chain(rc, N, self.Bp, calX, alpha, m)
        self.tab = RL.Tables(u, m, self.ch.c) if self.ch.d0 <= N else None
        self.nZ = self.nT = 0

    # ---- error functions (Propositions Z3, Z4)
    def Eplus(self, d, x, Lam):
        return self.inner.Ehat(d, 1.0, Lam + zlev.q(u, d, Lam)) + zlev.ell0(u, d, Lam) + zlev.X0(u, d) + dm * LN2 + 2

    def ET(self, d, Lam):
        Ls = self.ch.Lam_star(d, Lam)
        return self.Eplus(d, calX, Ls) + self.ch.A_T(d, Ls) + self.ch.j(d) * self.ch.Delta_T(d, Ls)

    def Ehat(self, d, x, Lam):
        return self.ET(d, Lam) + calX + 1

    # ---- exact costs
    def Z_cost(self, d, xh, ld):
        if time.time() - t_start > TMAX:
            raise TimeUp()
        self.nZ += 1
        Lam = -ld + d * LN2
        typ = float(self.nxt.major(d, [xh])[0])
        if d <= dm:
            lC = d * LN2
            ST.add("Z%d type (enumeration)" % self.j, lC, typ + self.Eplus(d, xh, Lam), (d, xh))
            return lC
        y = xh - zlev.X0(u, d)
        assert y >= 1 - 1e-12
        nos, Pi = zlev.proxy_all(cu, d, y, self.lines)
        kb = int(np.argmin(Pi))
        n_o = int(nos[kb])
        res = zlev.level_Z2(cu, d, n_o, y, ld, self.inner.cost)
        qq = zlev.q(u, d, Lam)
        ST.add("Z%d accuracy" % self.j, res['xout'], xh, (d, xh))
        ST.add("Z%d (U-inf)" % self.j, res['lC'], float(Pi[kb]) + zlev.ell0(u, d, Lam) + self.inner.Ehat(d, 1.0, Lam + qq), (d, xh, n_o))
        ST.add("Z%d delta' (Lemma Z2)" % self.j, -res['ldp'] + (d - n_o) * LN2, Lam + qq, (d, xh, n_o))
        ST.add("Z%d type (Prop. Z3)" % self.j, res['lC'], typ + self.Eplus(d, xh, Lam), (d, xh, n_o))
        return res['lC']

    def chain_cost(self, d, ld):
        """exact ln cost of T[Z_j; alpha, m](d, delta), by the recursion over the chain (dimension d, d - m, ...)."""
        ch = self.ch
        stack = []
        dd, l = d, ld
        while dd >= ch.d0:
            jd = ch.j(dd)
            a_d = ch.alow + jd * ch.w
            b_d = a_d - ch.w
            assert 2 * u * (dd - self.m) > calX and calX > 1 >= self.alpha > b_d > 0
            lev = RL.Level(u, dd, self.m, ch.c, ch.c, ch.c, math.log(ch.c), 2 * math.exp(u) * self.m / ch.c, b_d, l, 2, tab=self.tab)
            Lam = -l + dd * LN2
            ST.add("T%d accuracy" % self.level, float(lev.x_out), a_d, (dd,))
            ST.add("T%d delta' (Prop. T(ii))" % self.level, -lev.ldp + (dd - self.m) * LN2, Lam + ch.qT(dd, Lam), (dd,))
            stack.append((dd, l, lev, b_d))
            dd, l = dd - self.m, lev.ldp
        # bottom: the base family of Q at the accuracy alow
        t = RL.base_lcost(rc, dd, ch.alow, l)[0]
        Lam = -l + dd * LN2
        ST.add("T%d claim (bottom)" % self.level, t, dd * self.Bp + self.ET(dd, Lam), (dd,))
        while stack:
            dd, l, lev, b_d = stack.pop()
            c1 = self.Z_cost(dd - self.m, calX, lev.ldp)
            t = lev.lcmax([calX, b_d], [c1, t])
            self.nT += 1
            Lam = -l + dd * LN2
            bound = dd * self.Bp + self.ET(dd, Lam)
            ST.add("T%d claim (Prop. T(iii))" % self.level, t, bound, (dd,))
            # the type of Proposition Z4 on [alpha, X): at x = alpha and just below X
            for x in (self.alpha, calX - 1e-9):
                ST.add("F%d type (Prop. Z4)" % self.level, t, float(self.nxt.major(dd, [x])[0]) + self.Ehat(dd, x, Lam), (dd, x))
        return t

    def cost(self, d, xs, ld):
        xs = np.atleast_1d(np.asarray(xs, dtype=np.float64))
        out = np.empty(xs.shape)
        low = xs < calX
        if low.any():
            assert xs[low].min() >= self.alpha - 1e-12
            out[low] = self.chain_cost(d, ld)
        for i in np.nonzero(~low)[0]:
            out[i] = self.Z_cost(d, float(xs[i]), ld)
        return out


# ---- the design: blocks from the unrolling of section 6 at (n, delta)
Lam0 = -ld_top + n * LN2
Lam = Lam0
blocks = {}
unrolled = 0.0
terms = []
for j in range(J0 + k, J0, -1):
    alpha = eh if j == J0 + k else 1.0
    m_des = RL.Chain.design_m(rc, n, C.b[j], calX, alpha, Lam)
    m = max(1, int(round(m_des / BDIV)))
    blocks[j] = (m, m_des, alpha)
    ch = RL.Chain(rc, n, C.b[j], calX, alpha, m)
    if BDIV == 1.0:
        Lam = Lam + ch.j(n) * ch.qT(n, Lam + n * C.b[j])           # the closed update of section 6 (Proposition T(iv))
        tchain = ch.A_T(n, Lam) + calX + 1
    else:
        Lam = ch.Lam_star(n, Lam)
        tchain = ch.A_T(n, Lam) + ch.j(n) * ch.Delta_T(n, Lam) + calX + 1
    tlev = zlev.ell0(u, n, Lam) + zlev.X0(u, n) + dm * LN2 + 2
    unrolled += tchain + tlev
    terms.append((j, m, ch.j(n), ch.d0, tchain, tlev))
    Lam = Lam + zlev.q(u, n, Lam)
unrolled += E0(n, 1.0, Lam)

print("# u = %g (h = %.5f, a = %.5f, d_min = %d), n = N = %d, k = %d levels above the base, eps^ = %g, ln delta = %.3f, base error E_0 = %s, blocks = design/%g"
      % (u, cu.h, cu.a, dm, n, k, eh, ld_top, ENAME, BDIV))
print("# chain: s_t = L + %g, b_0 = h + %g; base level J0 = %d; (b_j - h)/h, j = %d..%d: %s;  W_j(b_j): %s;  X = X_0(N) + 1 = %.3f"
      % (dst, eps1, J0, J0, J0 + k, " ".join("%.4f" % ((C.b[j] - cu.h) / cu.h) for j in range(J0, J0 + k + 1)), " ".join("%.3f" % C.Wtop[j] for j in range(J0, J0 + k + 1)), calX))
for (j, m, jn, d0, tc, tl) in terms:
    print("#   level %d: block m = %d (design %d), chain levels at d = n: %d, d_0 = %d; unrolled terms: chain %.2f, level %.2f" % (j, m, blocks[j][1], jn, d0, tc, tl))

fam = Base(J0)
for j in range(J0, J0 + k):
    m, _, alpha = blocks[j + 1]
    fam = ZFam(fam, j, alpha, m)
top = fam
done = True
try:
    lC = float(top.cost(n, [eh], ld_top)[0])
except TimeUp:
    done = False
    lC = float('nan')
el = time.time() - t_start
if done:
    Ek = top.Ehat(n, eh, Lam0)
    KK = J0 + k
    bound_types = n * C.b[KK] + Ek
    bound_unrolled = n * C.b[KK] + unrolled
    print("exact ln cost of F_%d(n, eps^, delta): %.3f = n b_k + %.3f   (n b_k = %.3f, n b_base = %.3f, n h = %.3f, n a = %.3f)" % (KK, lC, lC - n * C.b[KK], n * C.b[KK], n * C.b[J0], n * cu.h, n * cu.a))
    print("bound by the composed error functions: n b_k + %.3f;   unrolled bound of section 6: n b_k + %.3f" % (Ek, unrolled))
    ST.add("TOP: exact <= n b_k + Ehat_k(n, eps^; Lam_0)", lC, bound_types)
    ST.add("TOP: Ehat_k <= unrolled error of section 6", Ek, unrolled)
else:
    print("NOT FINISHED within %.0f s (the node checks below are those made so far)" % TMAX)
f = top
cnt = []
while isinstance(f, ZFam):
    cnt.append("F_%d: %d Z-levels, %d chain levels" % (f.level, f.nZ, f.nT))
    f = f.inner
print("nodes evaluated exactly: " + "; ".join(cnt) + "   [%.0f s]" % el)
print("%-48s %9s %12s %6s   %s" % ("check", "number", "least slack", "viol.", "at"))
for name in sorted(ST.n):
    sl, tag = ST.least[name]
    print("%-48s %9d %12.3f %6d   %s" % (name, ST.n[name], sl, ST.viol.get(name, 0), tag))
nviol = sum(ST.viol.values())
print("TOTAL: %d checks, %d violations   %s" % (sum(ST.n.values()), nviol, "ALL CHECKS PASS" if (nviol == 0 and done) else ("VIOLATION" if nviol else "(unfinished)")))
