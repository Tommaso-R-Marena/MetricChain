"""R6-T4: a rate for the level recursion T_k -> theta_hint, and its numerical check on the functions of the cube.

STATEMENT [P: paper proof by the coordinator's check of SCI-REV-0007, not refereed; it uses only three machine-checked
consequences of the step inequality in proofs/Frontiers/HintRecursion.lean].  Let (theta_na, theta_h, a, h, E) be a
HintPair with the constant L >= 0 of `hint_lower` (theta_h(e) >= h - L e; L = 1 for the cube, `cubePair`), a > h, and let
T_1, T_2, ... : (0, oo) -> [0, oo) be nonincreasing with T_1 <= a, T_{k+1} <= T_k and StepLE theta_na T_k T_{k+1}
(for the exact recursion `exactRec` of the cube all of this is machine-checked: `exactRec_props`, `stepLE_exact`).
Put B_k := sup T_k (the value "at accuracy zero", tau_k in the report).

 (a) The top.  With d_0 = h/(a-h), k_0 = 1, J_m = ceil(d_m),
         d_{m+1} = d_m (J_m a + h)/(J_m a - h d_m),      k_{m+1} = k_m + J_m + 1,
     B_k <= h (1 + 1/d_m) for all k >= k_m.  In closed form, for all k >= 1,
         B_k - h <= c1/(k + c2),   kappa = h^2 a/((a-h)(a+h)(2a-h)),  c1 = h (1 + kappa)/kappa,  c2 = (a+h)(2a-h)/(h a) - 2,
     and limsup k (B_k - h) <= a.
 (b) Every accuracy.  For 0 < g < E, m_k := sup_{0<y<=g} (T_k(y) - theta_h(y))_+ and s := g + theta_h(g):
         m_{k+1} <= max{ B_{k+1} - h ,  m_k (B_{k+1} - h + L s)/(m_k + L s) },
     hence, for all k >= 1,
         T_k(g) - theta_h(g) <= A(g)/(k + c2),      A(g) = max{ c1 + L s , (1 + c2)(a - h + L g) }.

PROOF.  Three machine-checked facts, for T = T_k (nonincreasing) and T' = T_{k+1}:
 (L1) `StepLE.of_limit` with phi = g/h (then phi theta_na(g/phi) = g because theta_na(h) = h, and theta_na is
      continuous at h):  for 0 < g < h, if gamma + (1 - g/h) T(gamma/(1 - g/h)) <= B' for all 0 < gamma <= g, then T'(g) <= B'.
 (L2) `StepLE.of_macro`:  for g > 0, 0 < phi < 1, if gamma + (1-phi) T(gamma/(1-phi)) <= B' for all 0 < gamma <= phi a, then T'(g) <= B'.
 (L3) `StepLE.at_hint_fraction`:  for 0 < x < E, if y + T(y) <= C for all 0 < y <= x, then T'(x) <= theta_h(x)/(x + theta_h(x)) C.
 Lemma 1 (the slope grows, the range shrinks harmonically).  Let 0 <= sigma <= 1, 0 < x0 <= oo and T_k(x) <= B - sigma x for
 0 < x < x0.  Then T_{k+1}(g) <= B - (sigma + B/h - 1) g for 0 < g < x0 h/(h + x0) (for x0 = oo: 0 < g < h).
   Proof: such g has g < h and gamma/(1 - g/h) <= g h/(h - g) < x0 for gamma <= g, so
   gamma + (1 - g/h) T_k(gamma/(1 - g/h)) <= (1 - g/h) B + (1 - sigma) gamma <= (1 - g/h) B + (1 - sigma) g, and (L1) applies.
 Lemma 2 (the drop).  If T_k(x) <= B - x for 0 < x < x0, then T_{k+1} <= B a/(a + x0) everywhere.
   Proof: for phi with phi a/(1-phi) < x0 and gamma <= phi a:  gamma + (1-phi)(B - gamma/(1-phi)) = (1-phi) B; (L2); let phi increase to x0/(a + x0).
 Epoch.  Let T_k <= B everywhere, B > h, c = B/h - 1, J = ceil(1/c).  Lemma 1 applied J times (slopes c, 2c, ..., the last
 one >= 1 and then read as 1; ranges (0, h), (0, h/2), ..., (0, h/J)) gives T_{k+J}(x) <= B - x on (0, h/J), and Lemma 2 gives
 T_{k+J+1} <= B J a/(J a + h).  In terms of d = h/(B - h) = 1/c this is the recursion of (a); it starts from B = a (T_1 <= a).
 Closed form.  d' - d = d h (1 + d)/(J a - h d) and J < d + 1, so one epoch of J + 1 < d + 2 levels raises d by more than
 (J + 1) h f(d), f(d) = d (1 + d)/((d (a-h) + a)(d + 2)); f is increasing and d >= d_0, so the gain per level is at least
 kappa = h f(d_0).  Hence d_m >= d_0 + kappa (k_m - 1), and for k_m <= k < k_{m+1} (so k <= k_m + d_m + 1):
 d_m >= (d_0 + kappa (k - 2))/(1 + kappa), i.e. B_k - h <= h/d_m <= c1/(k + c2).  As d -> oo, h f(d) -> h/(a-h), which gives the limsup.
 (b).  For 0 < y <= g: z + T_k(z) <= z + theta_h(z) + m_k <= y + theta_h(y) + m_k for z <= y (`hint_mono`), so by (L3)
 T_{k+1}(y) - theta_h(y) <= theta_h(y)/(y + theta_h(y)) m_k <= (1 - y/s) m_k; and T_{k+1}(y) - theta_h(y) <= B_{k+1} - h + L y.
 The minimum of the two lines is largest where they cross, which is the recursion (if m_k <= B_{k+1} - h it gives
 m_{k+1} <= m_k).  With eps_k := B_k - h <= c1/(k + c2):  if m_k <= A/(k + c2) and A >= c1 + L s, then
 m_k (eps_{k+1} + L s)/(m_k + L s) <= A/(k + 1 + c2)  (equivalent to c1 + L s <= A), and m_1 <= a - h + L g <= A/(1 + c2).  QED

WHAT THE RATE GIVES AND WHAT IT DOES NOT.  The number of levels needed for the exponent theta_h(g) + eta is at most
A(g)/eta: explicit.  The o(n) of Theorems 11.54 and 11.58 is NOT made explicit by this: the sub-exponential factors of a
family with k nested levels are not quantified uniformly in k.  The true convergence is faster than the bound
(numerically (tau_k - h)/a ~ 0.65/k^2, K_REPORT.md, Proposition K5(d)): the bound is a rate, not the rate.

NUMERICAL CHECK (this script).  The recursion of the cube, T_1 = theta_na, T_{k+1} = min(T_k, R[T_k]), is iterated on a
grid in a ONE-SIDED mode: T is replaced by the step function that takes the value at the grid point to the left
(an upper bound, T being nonincreasing), the value near zero by a separate upper bound B_k of sup T_k (the bracket
at accuracy zero, (L2)), the infimum over (phi, beta) by a minimum over a grid.  Every computed number is therefore an
upper bound of the exact recursion up to rounding, and "computed <= proved bound" is checked for all levels (the
one-sided mode stalls a few per cent above h -- a known artefact of the discretisation, K_REPORT.md 6.1).
Also checked: the hypotheses of the HintPair for the cube on a grid, and that the computed values never fall below
theta_hint (the lower barrier `exactRec_ge_hint`).

Usage: python3 t4_rate.py [levels=40]
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


def kl(x, y):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(x > 0, x * np.log(x / y), 0.0)
        t2 = np.where(x < 1, (1 - x) * np.log((1 - x) / (1 - y)), 0.0)
    return t1 + t2


class CubeFunctions:
    def __init__(self, u):
        self.u = u
        self.pu = 1 / (1 + math.exp(u))
        self.lam1 = math.log(2 / (1 + math.exp(-u)))
        self.estar = math.log(math.cosh(u / 2))
        self.a = float(kl(self.pu, 0.5))
        self.h = float(kl(self.lam1 / u, 0.5))

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        rho = (self.lam1 + e) / self.u
        return np.where(rho < 0.5, kl(np.minimum(rho, 0.5), 0.5), 0.0)

    def theta_na(self, x):
        """min{KL(rho||1/2) : KL(rho||p_u) <= x}: the root rho in [p_u, 1/2] of KL(rho||p_u) = x, by bisection."""
        x = np.asarray(x, dtype=float)
        lo = np.full(x.shape, self.pu)
        hi = np.full(x.shape, 0.5)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            ok = kl(mid, self.pu) <= x
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        out = kl(lo, 0.5)
        return np.where(x >= self.estar, 0.0, np.where(x <= 0, self.a, out))


def proved_bounds(a, h, kmax):
    """(epoch bound on B_k for k = 1..kmax, closed-form constants kappa, c1, c2)."""
    d, k = h / (a - h), 1
    bound = np.full(kmax + 2, np.nan)
    while k <= kmax:
        J = math.ceil(d - 1e-15)
        k_next = k + J + 1
        bound[k:min(k_next, kmax + 1)] = h * (1 + 1 / d)
        d = d * (J * a + h) / (J * a - h * d)
        k = k_next
    kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    c1 = h * (1 + kappa) / kappa
    c2 = (a + h) * (2 * a - h) / (h * a) - 2
    return bound, kappa, c1, c2


def iterate(C, levels, G=160, nphi=99):
    """One-sided (upper-bound) iteration.  Returns grid g[1..G], T[k][i] (k = 1..levels), B[k]."""
    a, h, estar = C.a, C.h, C.estar
    g = estar * (np.arange(1, G + 1) / G) ** 1.5              # g_1 < ... < g_G = eps*
    T = C.theta_na(g)                                          # T_1 = theta_na on the grid; zero from eps* on
    T[-1] = 0.0
    B = a                                                      # sup T_1 = theta_na(0+) = a
    Ts, Bs = [None, T.copy()], [None, B]
    phis0 = np.linspace(0.01, 0.99, nphi)
    bfr = np.array([1e-4, 1e-3, 3e-3, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97])
    hi_edges = np.concatenate([g, [np.inf]])                   # interval i: [g_i, g_{i+1}), g_0 = 0, g_{G+1} = infinity
    for k in range(1, levels):
        Tval = np.concatenate([[B], T])                        # value of the step function on interval i = 0..G
        Tval[-1] = 0.0
        # the top: B_{k+1} <= min_phi sup_{0 < gamma <= phi a} [gamma + (1-phi) T(gamma/(1-phi))]     (StepLE.of_macro)
        ph = np.concatenate([phis0, np.linspace(0.001, 0.2, 200)])[:, None]
        hi = (1 - ph) * hi_edges[None, :]
        lo = (1 - ph) * np.concatenate([[0.0], g])[None, :]
        val = np.minimum(hi, ph * a) + (1 - ph) * Tval[None, :]
        val = np.where(lo < ph * a, val, -np.inf)
        Bn = min(B, float(val.max(axis=1).min()))
        Tn = np.empty_like(T)
        th = C.theta_hint(g)
        for j in range(G):
            gj = g[j]
            special = [gj / (gj + th[j])] if th[j] > 0 else []
            if gj < h:
                special.append(gj / h)
            ph = np.concatenate([phis0, np.clip(np.array(special), 1e-4, 1 - 1e-4)])[:, None]
            be = (bfr * gj)[None, :]
            mu = ph * C.theta_na((gj - be) / ph)                # shape (nphi, nbeta)
            hi3 = (1 - ph)[:, :, None] * hi_edges[None, None, :]
            val = np.minimum(hi3, mu[:, :, None]) + (1 - ph)[:, :, None] * Tval[None, None, :]
            val = np.where(hi3 > be[:, :, None], val, -np.inf)
            Tn[j] = min(T[j], float(val.max(axis=2).min()), Bn)
        Tn = np.minimum.accumulate(Tn)                          # nonincreasing in g (the exact T_{k+1} is)
        T, B = Tn, Bn
        Ts.append(T.copy()); Bs.append(B)
    return g, Ts, Bs


def main():
    levels = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    allok = True
    t0 = time.time()
    for u in (0.5, 1.0, 2.0):
        C = CubeFunctions(u)
        a, h, E = C.a, C.h, C.estar
        out(f"=== u = {u}: a = {a:.6f}, h = {h:.6f} (h/a = {h / a:.4f}), eps* = {E:.6f}")
        # the hypotheses of the HintPair on a grid
        e = np.linspace(1e-6, E * (1 - 1e-6), 4001)
        th = C.theta_hint(e)
        ident = float(np.abs(C.theta_na(e + th) - th).max())
        mono = float(np.diff(e + th).min())
        lower = float((th - (h - e)).min())
        nah = float(abs(C.theta_na(np.array([h]))[0] - h))
        okh = ident < 1e-9 and mono > 0 and lower > -1e-12 and nah < 1e-9
        allok = allok and okh
        out(f"  HintPair on a grid of 4001 accuracies: |theta_na(e + theta_h(e)) - theta_h(e)| <= {ident:.1e}; e + theta_h(e) increasing (smallest step {mono:.2e});"
            f" theta_h(e) - (h - e) >= {lower:.2e} (L = 1); |theta_na(h) - h| = {nah:.1e}: {okh}")
        bound, kappa, c1, c2 = proved_bounds(a, h, levels)
        out(f"  constants of the closed form: kappa = {kappa:.5f}, c1 = {c1:.5f} (c1/a = {c1 / a:.3f}), c2 = {c2:.3f};  asymptotically k (B_k - h) <= a")
        g, Ts, Bs = iterate(C, levels)
        tau2 = min(max((1 - p) * a, p * a + (1 - p) * float(C.theta_na(np.array([p * a / (1 - p)]))[0])) for p in np.linspace(1e-3, 0.999, 4000))
        out(f"  check of the implementation: closed form tau_2/a = {tau2 / a:.4f}; one-sided value B_2/a = {Bs[2] / a:.4f} (an upper bound of it)")
        allok = allok and Bs[2] >= tau2 - 1e-9
        th = C.theta_hint(g)
        # (a) the top
        worst_a = 0.0
        out("  (a) top:  k | B_k/a (one-sided upper bound of sup T_k) | epoch bound/a | closed form (h + c1/(k+c2))/a | (B_k - h) k^2/a")
        for k in range(1, levels + 1):
            closed = h + c1 / (k + c2) if k >= 2 else a
            ok = Bs[k] <= bound[k] + 1e-12 and Bs[k] <= closed + 1e-12 and Bs[k] >= h - 1e-9
            allok = allok and ok
            worst_a = max(worst_a, (Bs[k] - h) / (bound[k] - h))
            if k <= 8 or k % 8 == 0 or k == levels:
                out(f"      {k:3d} | {Bs[k] / a:8.4f} | {bound[k] / a:8.4f} | {closed / a:8.4f} | {(Bs[k] - h) * k * k / a:6.3f}   {'ok' if ok else 'VIOLATION'}")
        out(f"      largest (B_k - h)/(epoch bound - h) over the levels: {worst_a:.3f}")
        # (b) every accuracy
        s_all = g + th
        A = np.maximum(c1 + s_all, (1 + c2) * (a - h + g))     # A(g) with L = 1 and the bound m_1(g) <= a - h + g
        worst_b, worst_rec, barrier = 0.0, -np.inf, np.inf
        mprev = None
        for k in range(1, levels + 1):
            D = Ts[k] - th
            barrier = min(barrier, float(D.min()))
            m = np.maximum(np.maximum.accumulate(D), Bs[k] - h)  # sup over 0 < y <= g_j, including y -> 0
            ratio = float((D / (A / (k + c2))).max())
            worst_b = max(worst_b, ratio)
            if D.max() > 0 and not np.all(D <= A / (k + c2) + 1e-12):
                allok = False
            if mprev is not None:
                eps = Bs[k] - h
                rhs = np.maximum(eps, mprev * (eps + s_all) / (mprev + s_all))
                worst_rec = max(worst_rec, float((m - rhs).max()))
            mprev = m
        okb = worst_b <= 1 + 1e-12 and barrier >= -1e-9
        allok = allok and okb
        out(f"  (b) all {len(g)} grid accuracies, all levels: largest (T_k(g) - theta_h(g))/(A(g)/(k + c2)) = {worst_b:.3f};"
            f" smallest T_k(g) - theta_h(g) = {barrier:.2e} (never below the hinted exponent): {okb}")
        out(f"      the scalar recursion on the computed values: largest m_(k+1) - max(eps_(k+1), m_k (eps_(k+1) + s)/(m_k + s)) = {worst_rec:.2e}"
            f"   (<= 0 up to the one-sided discretisation: {worst_rec <= 2e-3 * a})")
        for frac in (0.1, 0.3, 0.6):
            j = int(np.searchsorted(g, frac * E))
            row = ", ".join(f"k={k}: {(Ts[k][j] - th[j]) / a:.4f} <= {A[j] / (k + c2) / a:.3f}" for k in (2, 4, 8, 16, levels))
            out(f"      g = {g[j] / E:.2f} eps*:  (T_k - theta_h)/a against the bound/a:  {row}")
    out(f"all checks passed: {allok}   ({time.time() - t0:.0f} s)")
    open(outfile("t4_rate.txt"), "w").write("\n".join(lines) + "\n")
    return allok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
