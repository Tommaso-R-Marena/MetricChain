#!/usr/bin/env python3
"""R13 / item 1 (iii): OWN implementation of the level recursion of the cube.

Written from the STATEMENTS only (theory report at 63e36f7, Theorem 11.52 display (11.18.2)/R[T],
Theorem 11.53(d), the setting of section 11.18) BEFORE opening anything in
experiments/coordinator_checks/nested_review_R6/ of the export.

    theta_na(x)   = min{ KL(rho||1/2) : KL(rho||p_u) <= x },   p_u = 1/(1+e^u),  (0 for x >= eps*)
    theta_hint(e) = KL((Lam1+e)/u || 1/2),   Lam1 = ln(2/(1+e^-u)),   eps* = ln cosh(u/2)
    a = KL(p_u||1/2),  h = KL(Lam1/u||1/2)
    R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma>=beta} [ min(gamma, phi*theta_na((g-beta)/phi)) + (1-phi)*T(gamma/(1-phi)) ]
    T_1 = theta_na,   T_{k+1} = min(T_k, R[T_k]).

WHAT IS COMPUTED: an UPPER bound of every T_k (one-sided discretisation), namely a nonincreasing
step function  Uhat_k >= T_k  on (0, infinity):

    Uhat_k(y) = B_k      on (0, x_1)          (B_k >= sup T_k = tau_k)
              = U_k[i]   on [x_i, x_{i+1})    (i = 1..N-1)
              = U_k[N]   on [x_N, inf)        (x_N = eps*, value 0)

Why it can only over-estimate (induction on k; the only uncontrolled thing is floating point, ~1e-15):
 (1) T_k is nonincreasing in the accuracy (Lean: exactRec_props), so T_k(y) <= T_k(x_i) <= U_k[i] on [x_i, x_{i+1}).
 (2) R is monotone in T (larger T, larger bracket), so R[T_k] <= R[Uhat_k].
 (3) the infimum over (phi, beta) is replaced by a minimum over finitely many admissible pairs: an over-estimate.
     The pairs are parametrised by (phi, rho): beta = g - phi*KL(rho||p_u), which gives
     phi*theta_na((g-beta)/phi) = phi*KL(rho||1/2) in closed form (rho in (p_u, 1/2]); admissible iff phi*KL(rho||p_u) < g.
 (4) the supremum over gamma is bounded from above cell by cell: for gamma >= mu := phi*theta_na(.) the bracket is
     mu + (1-phi)*Uhat(gamma/(1-phi)), nonincreasing in gamma; for beta <= gamma <= mu it is
     (1-phi)*(y + Uhat(y)), y = gamma/(1-phi), and on a cell [x_i, x_{i+1}) this is < (1-phi)*(x_{i+1} + U[i])
     (right end of the cell with the value of the left end); on the cell that contains y_hi = mu/(1-phi): y_hi + U[i].
 (5) B_{k+1}: for every g > 0 and every fixed phi (beta = g/2):  bracket <= sup_{0<gamma<=phi*a} [gamma + (1-phi)*Uhat_k(gamma/(1-phi))]
     (theta_na <= a; for gamma > phi*a use monotonicity of Uhat) -- bounded cell by cell as in (4), bottom cell included.
 (6) T_{k+1} nonincreasing => running minimum from the left is allowed; T_{k+1} <= sup T_{k+1} <= B_{k+1}.

The grid x_j = KL(rho_j||p_u) is chosen through radii rho_j, so theta_na(x_j) = KL(rho_j||1/2) needs no root finding.

Self-checks printed: U_k[j] >= theta_hint(x_j) at every level (the lower barrier of Thm 11.53(b); a bug that
under-estimates would show here), U nonincreasing, and one step from theta_hint returns ~theta_hint.

Usage: python3 r13_01_cube_recursion.py <u> <levels> <grid_ratio> <outfile.json>
"""
import sys, json, math, time
import numpy as np


def kl(r, q):
    r = np.asarray(r, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        t1 = np.where(r > 0, r * np.log(r / q), 0.0)
        t2 = np.where(r < 1, (1 - r) * np.log((1 - r) / (1 - q)), 0.0)
    return t1 + t2


class Cube:
    def __init__(self, u):
        self.u = float(u)
        self.p = 1.0 / (1.0 + math.exp(u))
        self.lam = math.log(2.0 / (1.0 + math.exp(-u)))
        self.estar = math.log(math.cosh(u / 2.0))
        self.a = float(kl(self.p, 0.5))
        self.h = float(kl(self.lam / u, 0.5))

    def D(self, rho):      # accuracy rate of the non-adaptive sample at radius rho:  KL(rho || p_u)
        return kl(rho, self.p)

    def K(self, rho):      # its exponent: KL(rho || 1/2)
        return kl(rho, 0.5)

    def theta_hint(self, e):
        e = np.asarray(e, dtype=float)
        r = np.minimum((self.lam + e) / self.u, 0.5)
        return np.where(e < self.estar, kl(r, 0.5), 0.0)


def constants(a, h):
    kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    c1 = h * (1 + kappa) / kappa
    c2 = (a + h) * (2 * a - h) / (h * a) - 2
    return kappa, c1, c2


class StepFn:
    """Nonincreasing step function on (0, inf): value Us[i] on [xs[i], xs[i+1]), xs[0] = 0, last cell unbounded."""

    def __init__(self, xpos, B, U):
        self.xs = np.concatenate(([0.0], xpos))
        self.Us = np.concatenate(([B], U))
        n = len(self.Us)
        self.n = n
        # cell suprema of y + Uhat(y): right end + value, for the bounded cells 0..n-2
        s = self.xs[1:] + self.Us[:-1]
        # sparse table for range maxima
        L = max(1, int(math.floor(math.log2(len(s)))) + 1)
        tab = np.full((L, len(s)), -np.inf)
        tab[0] = s
        for k in range(1, L):
            w = 1 << (k - 1)
            tab[k, :len(s) - w] = np.maximum(tab[k - 1, :len(s) - w], tab[k - 1, w:])
            tab[k, len(s) - w:] = tab[k - 1, len(s) - w:]
        self.tab = tab
        self.lg = np.zeros(len(s) + 2, dtype=np.int64)
        for i in range(2, len(s) + 2):
            self.lg[i] = self.lg[i // 2] + 1

    def idx(self, y):
        return np.searchsorted(self.xs, y, side='right') - 1

    def val(self, y):
        return self.Us[self.idx(y)]

    def sup_y_plus(self, ylo, yhi):
        """upper bound of sup_{ylo <= y <= yhi} (y + Uhat(y)); arrays, ylo <= yhi."""
        ilo = self.idx(ylo)
        ihi = self.idx(yhi)
        top = yhi + self.Us[ihi]
        length = ihi - ilo            # number of full cells ilo .. ihi-1
        has = length > 0
        lo = np.where(has, ilo, 0)
        ln = np.where(has, length, 1)
        k = self.lg[ln]
        hi2 = lo + ln - (1 << k)
        hi2 = np.minimum(hi2, self.tab.shape[1] - 1)
        lo = np.minimum(lo, self.tab.shape[1] - 1)
        rm = np.maximum(self.tab[k, lo], self.tab[k, hi2])
        return np.where(has, np.maximum(rm, top), top)


def bracket_sup(cube, F, g, phi, rho):
    """Upper bound of sup_{gamma>=beta}[min(gamma,mu)+(1-phi)*Uhat(gamma/(1-phi))] for the admissible pair
    (phi, beta = g - phi*D(rho)); returns +inf where the pair is not admissible."""
    Dr = cube.D(rho)
    Kr = cube.K(rho)
    beta = g - phi * Dr
    mu = phi * Kr
    ok = (beta > 0) & (phi > 0) & (phi < 1) & (beta < g)
    om = 1.0 - phi
    om = np.where(ok, om, 1.0)
    beta_s = np.where(ok, beta, 1.0)
    mu_s = np.where(ok, mu, 0.0)
    ylo = beta_s / om
    yhi = np.maximum(mu_s / om, ylo)
    v_a = mu_s + om * F.val(ylo)                 # case beta >= mu
    v_b = om * F.sup_y_plus(ylo, yhi)            # case beta <  mu
    v = np.where(beta_s >= mu_s, v_a, v_b)
    return np.where(ok, v, np.inf)


def macro_bound(cube, F, phis):
    yhi = phis * cube.a / (1.0 - phis)
    tiny = np.full_like(yhi, 1e-300)
    return (1.0 - phis) * F.sup_y_plus(tiny, yhi)


def run(u, levels, ratio, verbose=True):
    cube = Cube(u)
    a, h, estar, p = cube.a, cube.h, cube.estar, cube.p
    kappa, c1, c2 = constants(a, h)
    # grid in the accuracy through radii: rho_j = p + (1/2-p)*t_j, t geometric; x_j = D(rho_j) (ratio ~ ratio near 0)
    tr = math.sqrt(ratio)
    t1 = 1e-4
    nt = int(math.ceil(math.log(1.0 / t1) / math.log(tr)))
    t = np.exp(np.linspace(math.log(t1), 0.0, nt + 1))
    rho_g = p + (0.5 - p) * t
    rho_g[-1] = 0.5
    xpos = cube.D(rho_g)
    xpos[-1] = estar
    U = cube.K(rho_g)            # T_1 = theta_na at the grid points (closed form)
    U[-1] = 0.0
    B = a
    N = len(xpos)
    th = cube.theta_hint(xpos)
    A_g = np.maximum(c1 + xpos + th, (1 + c2) * (a - h + xpos))
    # candidates
    tc = np.unique(np.concatenate((np.exp(np.linspace(math.log(1e-4), 0.0, 44)), np.linspace(0.02, 1.0, 50))))
    rho_c = p + (0.5 - p) * tc
    rho_c[-1] = 0.5
    f_c = np.unique(np.concatenate((1.0 - np.exp(np.linspace(math.log(1e-9), math.log(0.5), 25)),
                                    np.linspace(0.04, 0.96, 24))))
    phis_macro = np.unique(np.concatenate((np.exp(np.linspace(math.log(1e-6), math.log(0.999), 4000)),
                                           np.linspace(0.001, 0.999, 999))))
    Dc = cube.D(rho_c)
    out = dict(u=u, a=a, h=h, estar=estar, p=p, lam=cube.lam, kappa=kappa, c1=c1, c2=c2, N=N, ratio=ratio,
               x1=float(xpos[0]), levels=[])
    best_t = None
    best_f = None
    t0 = time.time()
    for k in range(1, levels + 1):
        bound_a = c1 / (k + c2)
        m_b = float(np.max((U - th)[xpos < estar]))
        rb = (U - th) / (A_g / (k + c2))
        rb_max = float(np.max(rb[xpos < estar]))
        barrier = float(np.min((U - th)[xpos < estar]))
        sel = {}
        for frac in (0.1, 0.25, 0.5, 0.75):
            jj = int(np.searchsorted(xpos, frac * estar))
            sel[str(frac)] = dict(x=float(xpos[jj]), U=float(U[jj]), th=float(th[jj]), bound_b=float(A_g[jj] / (k + c2)))
        rec = dict(k=k, B=B, tau_minus_h=B - h, bound_a=bound_a, ratio_a=(B - h) / bound_a,
                   max_T_minus_hint=m_b, ratio_b_max=rb_max, barrier_min=barrier,
                   U_first=float(U[0]), k2_scaled=(B - h) / a * k * k, sel=sel)
        out['levels'].append(rec)
        if verbose:
            print(f"k={k:3d}  B_k-h={B-h:.6e}  c1/(k+c2)={bound_a:.6e}  ratio(a)={(B-h)/bound_a:.4f}  "
                  f"max_g(U-th)={m_b:.4e}  max ratio(b)={rb_max:.4f}  min(U-th)={barrier:+.2e}  "
                  f"(tau-h)k^2/a={(B-h)/a*k*k:.3f}  t={time.time()-t0:.0f}s", flush=True)
        if k == levels:
            break
        F = StepFn(xpos, B, U)
        g = xpos[:, None, None]
        # coarse candidates: rho_c x f_c, phi = f * min(1, g/D(rho))   (in chunks of g to bound memory)
        best = np.empty(N)
        bt = np.empty(N)
        bf = np.empty(N)
        CH = 400
        for c0 in range(0, N, CH):
            gc = g[c0:c0 + CH]
            phimax = np.minimum(1.0, gc / Dc[None, :, None])
            phi = f_c[None, None, :] * phimax
            V = bracket_sup(cube, F, gc, phi, rho_c[None, :, None])
            Vf = V.reshape(V.shape[0], -1)
            j = np.argmin(Vf, axis=1)
            best[c0:c0 + CH] = Vf[np.arange(Vf.shape[0]), j]
            jr, jf = np.unravel_index(j, (len(rho_c), len(f_c)))
            bt[c0:c0 + CH] = tc[jr]
            bf[c0:c0 + CH] = f_c[jf]
        # also try last level's optimum as a seed
        if best_t is not None:
            rho_s = np.minimum(p + (0.5 - p) * best_t, 0.5)
            phi_s = best_f * np.minimum(1.0, xpos / cube.D(rho_s))
            Vs = bracket_sup(cube, F, xpos, phi_s, rho_s)
            imp = Vs < best
            best = np.where(imp, Vs, best)
            bt = np.where(imp, best_t, bt)
            bf = np.where(imp, best_f, bf)
        # local refinement (pattern search in (log t, logit-ish f)); any admissible pair gives a valid bound
        wt, wf = 0.12, 0.06
        for it in range(6):
            dt = np.linspace(-wt, wt, 9)
            df = np.linspace(-wf, wf, 9)
            tt = np.clip(bt[:, None, None] * np.exp(dt[None, :, None]), 1e-6, 1.0)
            ff = np.clip(bf[:, None, None] + df[None, None, :] * np.minimum(bf, 1 - bf)[:, None, None] * 4, 1e-9, 1 - 1e-12)
            rr = np.minimum(p + (0.5 - p) * tt, 0.5)
            ph = ff * np.minimum(1.0, g / cube.D(rr))
            V2 = bracket_sup(cube, F, g, ph, rr).reshape(N, -1)
            j2 = np.argmin(V2, axis=1)
            b2 = V2[np.arange(N), j2]
            a1, a2 = np.unravel_index(j2, (9, 9))
            imp = b2 < best
            best = np.where(imp, b2, best)
            bt = np.where(imp, tt[np.arange(N), a1, 0], bt)
            bf = np.where(imp, ff[np.arange(N), 0, a2] if ff.shape[1] == 1 else ff[np.arange(N), a1, a2], bf)
            wt *= 0.5
            wf *= 0.5
        best_t, best_f = bt, bf
        Unew = np.minimum(U, best)
        Bnew = min(B, float(np.min(macro_bound(cube, F, phis_macro))))
        Unew = np.minimum(Unew, Bnew)
        Unew = np.minimum.accumulate(Unew)
        Unew[-1] = 0.0
        U, B = Unew, Bnew
    out['final_U'] = [float(v) for v in U]
    out['x'] = [float(v) for v in xpos]
    out['theta_hint'] = [float(v) for v in th]
    out['A_g'] = [float(v) for v in A_g]
    out['seconds'] = time.time() - t0
    return out


def selfcheck_fixed_point(u, ratio):
    """One step from Uhat = theta_hint (clipped): the result must stay >= theta_hint (my bound is an upper bound of
    R[theta_hint] = theta_hint) and should be close to it."""
    cube = Cube(u)
    p = cube.p
    tr = math.sqrt(ratio)
    nt = int(math.ceil(math.log(1e4) / math.log(tr)))
    t = np.exp(np.linspace(math.log(1e-4), 0.0, nt + 1))
    rho_g = p + (0.5 - p) * t
    rho_g[-1] = 0.5
    xpos = cube.D(rho_g)
    xpos[-1] = cube.estar
    th = cube.theta_hint(xpos)
    F = StepFn(xpos, cube.h, th)
    # the pair of Theorem 11.53(b): phi = g/(g+theta_hint(g)), beta -> 0, i.e. rho = (lam+g)/u, f -> 1
    res = []
    for f in (1 - 1e-3, 1 - 1e-6, 1 - 1e-9):
        rho = np.minimum((cube.lam + xpos) / cube.u, 0.5)
        phi = f * np.minimum(1.0, xpos / cube.D(rho))
        V = bracket_sup(cube, F, xpos, phi, rho)
        m = xpos < cube.estar
        dv = (V - th)[m]
        res.append((f, float(np.min(dv)), float(np.max(dv)), float(np.max((dv / th[m])[:-5]))))
    return res


if __name__ == '__main__':
    u = float(sys.argv[1])
    levels = int(sys.argv[2])
    ratio = float(sys.argv[3])
    outfile = sys.argv[4]
    cube = Cube(u)
    k_, c1_, c2_ = constants(cube.a, cube.h)
    print(f"# r13_01_cube_recursion.py u={u} levels={levels} grid ratio={ratio}")
    print(f"# p_u={cube.p:.12f} Lam1={cube.lam:.12f} eps*={cube.estar:.12f} a={cube.a:.12f} h={cube.h:.12f}")
    print(f"# kappa={k_:.12f} c1={c1_:.12f} c2={c2_:.12f} c1/a={c1_/cube.a:.6f}")
    for f, lo, hi, rel in selfcheck_fixed_point(u, ratio):
        print(f"# self-check one step from theta_hint, f={f}: min(V-th)={lo:+.3e} max(V-th)={hi:.3e} max rel (all but top 5 cells)={rel:.3e}")
    out = run(u, levels, ratio)
    viol_a = [r['k'] for r in out['levels'] if r['ratio_a'] > 1.0]
    viol_b = [r['k'] for r in out['levels'] if r['ratio_b_max'] > 1.0]
    low = [r['k'] for r in out['levels'] if r['barrier_min'] < -1e-12]
    print(f"# levels with B_k-h > c1/(k+c2): {viol_a}")
    print(f"# levels with some grid point above A(g)/(k+c2): {viol_b}")
    print(f"# levels where the upper bound dips below theta_hint (must be empty): {low}")
    print(f"# max ratio(a) = {max(r['ratio_a'] for r in out['levels']):.6f} at k={max(out['levels'], key=lambda r: r['ratio_a'])['k']}")
    print(f"# max ratio(b) = {max(r['ratio_b_max'] for r in out['levels']):.6f} at k={max(out['levels'], key=lambda r: r['ratio_b_max'])['k']}")
    with open(outfile, 'w') as fh:
        json.dump(out, fh)
    print(f"# wrote {outfile}; {out['seconds']:.0f} s")
    print("# END")
