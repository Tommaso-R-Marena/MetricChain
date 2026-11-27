"""Referee B, check 6 (global test of Theorem R without the report's machinery): the recursion itself,

    T_1 = theta,   T_{k+1} = min(T_k, R[T_k]),
    R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma >= beta} [ min(gamma, mu) + (1 - phi) T(gamma/(1 - phi)) ],  mu = phi theta((g - beta)/phi),

iterated on a grid, own implementation (written without reference to iterate_exact.py's code path: different grid,
different parametrisation (logit of phi, logit of beta/g), local zoom refinement of the (phi, beta) minimisation).

For a nonincreasing T the supremum over gamma is evaluated exactly for the piecewise-linear interpolant of T:
    beta <= mu:  (1 - phi) max_{y in [beta/(1-phi), mu/(1-phi)]} S(y),   S(y) = y + T(y)     (range maximum over grid nodes + the two ends)
    beta >  mu:  mu + (1 - phi) T(beta/(1 - phi)).
Nothing is assumed about the location of the supremum (no "x + T(x) nondecreasing"), nothing about beta -> 0.
tau_{k+1} = T_{k+1}(0+) is obtained in two ways: (A) from the grid point g_min (the full two-parameter minimisation at a
tiny accuracy), (B) from the one-parameter formula at accuracy zero, inf_phi (1 - phi) sup_{0 < y <= phi a/(1 - phi)} S_k(y).
The grid minimisation over (phi, beta) can only OVER-estimate the infimum; interpolation errors have no sign.

Usage: python3 b6_recursion.py pair levels [q] [nz] [xmin] [chunk]
"""
import sys, math, time
import numpy as np

# ------------------------------------------------------------------------------------------------ pairs (numpy theta)
def make_pair(name):
    if name == "gauss":
        th = lambda e: np.where(e < 1.0, (1.0 - np.sqrt(np.clip(e, 0.0, 1.0))) ** 2, 0.0)
        return dict(theta=th, a=1.0, xmax=1.0, h=0.25, c2=math.pi ** 2 / 16, label="Gaussian (1 - sqrt e)^2")
    if name == "cubroot":
        th = lambda e: np.where(e < 1.0, (1.0 - np.sqrt(np.clip(e, 0.0, 1.0))) ** 3, 0.0)
        return dict(theta=th, a=1.0, xmax=1.0, h=0.18503737537, c2=0.5353075, label="(1 - sqrt e)_+^3")
    if name == "quad":
        th = lambda e: np.where(e < 1.0, (1.0 - np.clip(e, 0.0, 1.0)) ** 2, 0.0)
        return dict(theta=th, a=1.0, xmax=1.0, h=(3 - math.sqrt(5)) / 2, c2=0.5151744, label="(1 - e)_+^2")
    if name == "kink":
        th = lambda e: np.maximum(np.maximum(1.0 - 3.0 * e, 0.5 - e), 0.0)
        return dict(theta=th, a=1.0, xmax=0.5, h=0.25, c2=None, label="kinked max(1 - 3e, 1/2 - e, 0)")
    if name == "kinksmooth":
        th = lambda e: np.maximum(np.where(e < 1.0, (1.0 - np.sqrt(np.clip(e, 0.0, 1.0))) ** 2, 0.0), np.maximum(0.25 + 0.4 * (0.25 - e), 0.0))
        return dict(theta=th, a=1.0, xmax=1.0, h=0.25, c2=None, label="kink: max((1 - sqrt e)^2, 1/4 + 0.4 (1/4 - e))")
    if name == "chord":
        def th(e):
            g = np.where(e < 1.0, (1.0 - np.sqrt(np.clip(e, 0.0, 1.0))) ** 2, 0.0)
            return np.where((e >= 0.16) & (e <= 0.36), 0.52 - e, g)
        return dict(theta=th, a=1.0, xmax=1.0, h=0.26, c2=None, label="Gaussian with chord on [0.16, 0.36] (theta affine near h)")
    if name == "lin":
        th = lambda e: np.maximum(1.0 - 2.0 * e, 0.0)
        return dict(theta=th, a=1.0, xmax=0.5, h=1.0 / 3, c2=None, label="(1 - 2e)_+ (affine through the fixed point)")
    if name.startswith("cube"):
        # the cube from the KL definitions (theory report 11.18): theta_na(e) = KL(rho_e || 1/2), KL(rho_e || p_u) = e.
        # Tabulated in z = sqrt(e) (theta is smooth in z, also at zero) on 400001 nodes; linear interpolation in z.
        u = float(name[4:])
        pu = 1.0 / (1.0 + math.exp(u))
        kl = lambda xx, yy: xx * np.log(xx / yy) + (1 - xx) * np.log((1 - xx) / (1 - yy))
        estar = math.log(math.cosh(u / 2))
        zt = np.linspace(0.0, math.sqrt(estar), 400001)
        et = zt ** 2
        lo = np.full(et.shape, pu)
        hi = np.full(et.shape, 0.5)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            ok = kl(mid, pu) <= et
            lo = np.where(ok, mid, lo)
            hi = np.where(ok, hi, mid)
        tt = kl(0.5 * (lo + hi), 0.5)
        tt[0] = float(kl(pu, 0.5))
        tt[-1] = 0.0
        th = lambda e: np.interp(np.sqrt(np.clip(e, 0.0, None)), zt, tt)        # 0 beyond eps*
        lam1 = math.log(2 / (1 + math.exp(-u)))
        rho_h = lam1 / u
        hh = float(kl(rho_h, 0.5))
        c2 = 2 * math.pi ** 2 * hh ** 2 / (u * u * rho_h * (1 - rho_h))
        return dict(theta=th, a=float(kl(pu, 0.5)), xmax=estar, h=hh, c2=c2, label="cube u = %g (KL definitions)" % u)
    raise SystemExit("unknown pair")


class RMQ:
    """range maximum by a sparse table"""
    def __init__(self, v):
        n = len(v)
        K = max(1, n.bit_length())
        tab = np.full((K, n), -np.inf)
        tab[0] = v
        j = 1
        while (1 << j) <= n:
            half = 1 << (j - 1)
            m = n - (1 << j) + 1
            tab[j, :m] = np.maximum(tab[j - 1, :m], tab[j - 1, half:half + m])
            j += 1
        self.tab = tab

    def query(self, lo, hi):
        length = hi - lo + 1
        j = np.frexp(length.astype(np.float64))[1] - 1
        return np.maximum(self.tab[j, lo], self.tab[j, hi - np.left_shift(1, j) + 1])


def bracket(g, phi, beta, theta, x, T, rm):
    """sup_{gamma >= beta} [min(gamma, mu) + (1 - phi) T(gamma/(1 - phi))] for the interpolant of T (arrays broadcast)."""
    om = 1.0 - phi
    mu = phi * theta((g - beta) / phi)
    ylo = beta / om
    yhi = np.maximum(mu, beta) / om
    Tlo = np.interp(ylo, x, T)
    Thi = np.interp(yhi, x, T)
    best = np.maximum(ylo + Tlo, yhi + Thi)
    ilo = np.searchsorted(x, ylo, side="right")
    ihi = np.searchsorted(x, yhi, side="left") - 1
    ok = ihi >= ilo
    if ok.any():
        best_in = rm.query(np.where(ok, ilo, 0), np.where(ok, ihi, 0))
        best = np.where(ok, np.maximum(best, best_in), best)
    VA = om * best
    VB = mu + om * Tlo
    return np.where(beta <= mu, VA, VB)


def step(x, T, P, nz, bz, chunk):
    """one level: returns (R on the grid nodes x[1:], statistics)."""
    theta = P["theta"]
    S = x + T
    rm = RMQ(S)
    n = len(x)
    R = np.empty(n)
    R[0] = np.nan
    zb = np.asarray(bz)                    # logit of beta/g
    stat_b = []
    for s0 in range(1, n, chunk):
        g = x[s0:s0 + chunk]
        m = len(g)
        # logit(phi) from logit(g/(40 xmax)) to 14
        zlo = np.log(g / (40.0 * P["xmax"]))
        zhi = 14.0
        u = np.linspace(0.0, 1.0, nz)
        Z = zlo[:, None] + (zhi - zlo)[:, None] * u[None, :]                 # (m, nz)
        dz = (zhi - zlo) / (nz - 1)
        phi = 1.0 / (1.0 + np.exp(-Z))
        bfr = 1.0 / (1.0 + np.exp(-zb))                                      # (nb,)
        G = g[:, None, None]
        V = bracket(G, phi[:, :, None], G * bfr[None, None, :], theta, x, T, rm)   # (m, nz, nb)
        flat = V.reshape(m, -1)
        idx = np.argmin(flat, axis=1)
        best = flat[np.arange(m), idx]
        iz, ib = np.unravel_index(idx, (nz, len(zb)))
        zc = Z[np.arange(m), iz]
        bc = zb[ib]
        hz = dz.copy()
        hb = np.full(m, 3.0)
        off = np.linspace(-1.0, 1.0, 9)
        for _ in range(7):
            Zr = zc[:, None, None] + hz[:, None, None] * off[None, :, None]
            Br = bc[:, None, None] + hb[:, None, None] * off[None, None, :]
            Zr = np.minimum(Zr, 30.0)
            Br = np.clip(Br, -40.0, 30.0)
            ph = 1.0 / (1.0 + np.exp(-Zr))
            ph = np.clip(ph, 1e-300, 1.0 - 1e-15)
            bf = 1.0 / (1.0 + np.exp(-Br))
            bf = np.clip(bf, 1e-17, 1.0 - 1e-12)
            Vr = bracket(G, ph, G * bf, theta, x, T, rm)
            fl = Vr.reshape(m, -1)
            j = np.argmin(fl, axis=1)
            v = fl[np.arange(m), j]
            jz, jb = np.unravel_index(j, (9, 9))
            better = v < best
            best = np.where(better, v, best)
            zc = np.where(better, zc + hz * off[jz], zc)
            bc = np.where(better, bc + hb * off[jb], bc)
            hz *= 0.35
            hb *= 0.35
        R[s0:s0 + chunk] = best
        stat_b.append(1.0 / (1.0 + np.exp(-bc)))
    return R, np.concatenate(stat_b)


def tau_zero(x, T, a):
    """accuracy zero, one parameter: inf_phi (1 - phi) sup_{0 < y <= phi a/(1 - phi)} S(y)  (prefix maximum of the interpolant)."""
    S = x + T
    pm = np.maximum.accumulate(S)

    def f(phi):
        Y = phi * a / (1.0 - phi)
        i = np.searchsorted(x, Y, side="right") - 1
        i = np.clip(i, 0, len(x) - 1)
        return (1.0 - phi) * np.maximum(pm[i], Y + np.interp(Y, x, T))
    z = np.linspace(-30.0, 12.0, 20001)
    phi = 1.0 / (1.0 + np.exp(-z))
    v = f(phi)
    i = int(np.argmin(v))
    lo, hi = z[max(i - 1, 0)], z[min(i + 1, len(z) - 1)]
    for _ in range(6):
        zz = np.linspace(lo, hi, 2001)
        vv = f(1.0 / (1.0 + np.exp(-zz)))
        j = int(np.argmin(vv))
        lo, hi = zz[max(j - 1, 0)], zz[min(j + 1, len(zz) - 1)]
    return float(min(v[i], vv[j])), float(1.0 / (1.0 + math.exp(-zz[j])))


SAVE_LEVELS = set(int(v) for v in __import__("os").environ.get("SAVE_LEVELS", "").split(",") if v)


def main():
    name = sys.argv[1]
    levels = int(sys.argv[2])
    q = float(sys.argv[3]) if len(sys.argv) > 3 else 1.02
    nz = int(sys.argv[4]) if len(sys.argv) > 4 else 160
    xmin = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-9
    chunk = int(sys.argv[6]) if len(sys.argv) > 6 else 200
    P = make_pair(name)
    a, h = P["a"], P["h"]
    G = int(math.ceil(math.log(P["xmax"] / xmin) / math.log(q)))
    x = np.concatenate([[0.0], P["xmax"] * q ** np.arange(-G, 1.0)])
    T = P["theta"](x)
    T[0] = a
    bz = [-34.0, -20.0, -12.0, -8.0, -6.0, -4.5, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.5, 6.0]
    print("# pair %s: a = %.10g, h = %.10g, c_*^2 = %s" % (P["label"], a, h, P["c2"]))
    print("# grid: %d nodes on [%g, %g], ratio %g; logit(phi) grid %d, beta grid %d, 7 zoom rounds of 9 x 9" % (len(x) - 1, x[1], x[-1], q, nz, len(bz)))
    print("# k  tau_k(A: grid node g_min)  tau_k(B: accuracy-zero formula)  k^2(tau_k - h) [B]  k(tau_k - h) [B]  1/sqrt(tau_k-h) increment  optimal beta/g: median, max  secs")
    t0 = time.time()
    tauA = tauB = a
    prevQ = None
    for k in range(1, levels + 1):
        d = tauB - h
        Q = 1.0 / math.sqrt(d) if d > 0 else float("nan")
        inc = (Q - prevQ) if prevQ is not None else float("nan")
        prevQ = Q
        extra = "" if k == 1 else "%.2e %.2e" % (np.median(bstat), np.max(bstat))
        print("%3d %.10f %.10f %.6f %.6f %.5f  %s  %.0f" % (k, tauA, tauB, k * k * d, k * d, inc, extra, time.time() - t0), flush=True)
        if k == levels:
            break
        R, bstat = step(x, T, P, nz, bz, chunk)
        tz, phiz = tau_zero(x, T, a)
        newT = T.copy()
        newT[1:] = np.minimum(T[1:], R[1:])
        newT[1:] = np.minimum.accumulate(newT[1:])
        tauA = float(newT[1])
        tauB = min(tauB, tz)
        # the value at 0+ is the supremum; keep the grid consistent with the accuracy-zero formula
        newT[0] = max(tauB, newT[1])
        T = newT
        if (k + 1) in SAVE_LEVELS:
            np.save("T_%s_level%d.npy" % (name, k + 1), np.vstack([x, T]))
    np.save("T_%s_%d.npy" % (name, levels), np.vstack([x, T]))


if __name__ == "__main__":
    main()
