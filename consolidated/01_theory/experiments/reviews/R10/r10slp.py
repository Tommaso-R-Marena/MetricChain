"""Sequential-linear-programming ascent over the LAW rho of the block types (own method).

For an exit type kp and multipliers (eta, tau >= 0), weak duality gives, for EVERY profile law rho
(atoms M with weights rho), with m = E_rho M:

  g(rho; kp) := min{ MI(nu) : nubar = kp, u*dist(nu,mu) <= e + alpha(mu) - v(kp) }
     >=  h(kp) - eta*kp + (tau/u) * ( v(kp) - e + c0 - phi(m) ) + E_rho[ (tau/u) h(M) - Gamma_{tau,eta}(M) ].

If phi is concave (ferromagnet), -phi(m) >= -phi(m0) - phi'(m0)(m - m0) for any reference mean m0,
so the right side is bounded below by a function L_kp(rho) that is LINEAR in rho; otherwise the
mean is kept fixed (then the bound is linear in rho as it stands).  With (eta, tau) optimal for a
reference law rho0, L_kp(rho0) = g(rho0; kp).  Hence r_rho(e) = min_kp g >= min_kp L_kp(rho), and
maximising min_kp L_kp over rho is a linear programme whose optimum is >= r_{rho0}(e): a monotone
ascent (up to the grid of exit types) which moves finite mass in one step.
"""
import numpy as np
from scipy import optimize
from r10lib import *
from r10lib import _gamma, _h


def hp(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return np.log((1 - x) / x)


def fixed_type_solve(lam, mu, kp, r, nb=44):
    """vectorised over exit types kp (array) with distance budgets r (array):
    the clipping (clo, chi) with type kp that uses the largest distance <= r.
    returns clo, chi, MI, status  (0 = regular, 1 = constant profile reachable (MI = 0),
    2 = infeasible (r < |kp - mubar|))."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    kp = np.asarray(kp, float)
    r = np.asarray(r, float)
    mb = float(lam @ mu)

    def T(clo, chi):
        nu = np.minimum(np.maximum(mu, clo[:, None]), chi[:, None])
        return nu @ lam

    def Dd(clo, chi):
        nu = np.minimum(np.maximum(mu, clo[:, None]), chi[:, None])
        return np.abs(nu - mu) @ lam

    def chi_of(clo):
        # smallest chi >= clo with T(clo, chi) >= kp
        lo = clo.copy()
        hi = np.ones_like(clo)
        for _ in range(nb):
            mid = 0.5 * (lo + hi)
            ok = T(clo, mid) >= kp
            hi = np.where(ok, mid, hi)
            lo = np.where(ok, lo, mid)
        return hi

    cmax = np.abs(kp[:, None] - mu[None, :]) @ lam
    status = np.zeros(len(kp), dtype=int)
    status[r >= cmax] = 1
    status[r < np.abs(kp - mb) - 1e-14] = 2
    # range of clo: [a0, kp]; a0 = 0 if kp <= mb else solution of T(a0, 1) = kp
    one = np.ones_like(kp)
    lo = np.zeros_like(kp)
    hi = kp.copy()
    # for kp > mb find a0 by bisection on T(clo, 1) >= kp
    a_lo = np.zeros_like(kp)
    a_hi = kp.copy()
    for _ in range(nb):
        mid = 0.5 * (a_lo + a_hi)
        ok = T(mid, one) >= kp
        a_hi = np.where(ok, mid, a_hi)
        a_lo = np.where(ok, a_lo, mid)
    a0 = np.where(kp > mb, a_hi, 0.0)
    lo = a0.copy()
    hi = np.maximum(kp, a0)
    # largest clo in [a0, kp] with dist(clo, chi_of(clo)) <= r
    for _ in range(nb):
        mid = 0.5 * (lo + hi)
        ch = chi_of(mid)
        ok = Dd(mid, ch) <= r
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    clo = lo
    chi = chi_of(clo)
    nu = np.minimum(np.maximum(mu, clo[:, None]), chi[:, None])
    mi = _h(nu @ lam) - _h(nu) @ lam
    mi = np.where(status == 1, 0.0, mi)
    mi = np.where(status == 2, np.inf, mi)
    return clo, chi, mi, status


def exit_minorants(model, lam, mu, e, K, cur=None):
    """for each exit type in K: multipliers (eta, tau), exact at the profile (lam, mu) for the
    feasible exits; returns arrays kp, eta, tau, val and (m0, B)."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    u = model.u
    m0 = float(lam @ mu)
    B = e + alpha(model, lam, mu)
    r = (B - model.v(K)) / u
    clo, chi, mi, status = fixed_type_solve(lam, mu, K, r)
    a = hp(np.maximum(clo, 1e-12))
    b = hp(np.minimum(chi, 1 - 1e-12))
    eta = 0.5 * (a + b)
    tau = np.maximum(0.5 * (a - b), 0.0)
    # status 1: tau = 0, eta = h'(kp)
    eta = np.where(status == 1, hp(K), eta)
    tau = np.where(status == 1, 0.0, tau)
    # status 2 (infeasible at the reference): a valid minorant with a large multiplier
    if (status == 2).any():
        idx = np.where(status == 2)[0]
        for i in idx:
            kp = K[i]
            # one-sided move to type kp
            if kp < m0:
                # lowering only: chi with T(0, chi) = kp
                lo_, hi_ = 0.0, 1.0
                for _ in range(60):
                    mid = 0.5 * (lo_ + hi_)
                    if float(np.minimum(mu, mid) @ lam) >= kp:
                        hi_ = mid
                    else:
                        lo_ = mid
                bb = float(hp(hi_))
                tt = 30.0
                eta[i], tau[i] = bb + tt, tt
            else:
                lo_, hi_ = 0.0, 1.0
                for _ in range(60):
                    mid = 0.5 * (lo_ + hi_)
                    if float(np.maximum(mu, mid) @ lam) >= kp:
                        hi_ = mid
                    else:
                        lo_ = mid
                aa = float(hp(hi_))
                tt = 30.0
                eta[i], tau[i] = aa - tt, tt
    # value of the minorant at the reference
    val = np.empty(len(K))
    for i, kp in enumerate(K):
        gam, _ = _gamma(eta[i], tau[i], mu)
        val[i] = float(h(kp)) - eta[i] * kp - tau[i] * r[i] - float(lam @ gam)
    return K, eta, tau, val, mi, status, m0, B


def slp_step(model, lam, mu, e, K, Mgrid, phi_prime=None):
    """one LP step.  phi_prime given => mean free (concave phi); None => mean fixed."""
    u = model.u
    K, eta, tau, val, mi, status, m0, B = exit_minorants(model, lam, mu, e, K)
    atoms = np.unique(np.concatenate((Mgrid, mu)))
    nA = len(atoms)
    hA = h(atoms)
    phi0 = float(model.phi(m0))
    fp = phi_prime(m0) if phi_prime is not None else 0.0
    A = np.zeros((len(K), nA + 1))
    b = np.zeros(len(K))
    vK = model.v(K)
    for i, kp in enumerate(K):
        gam, _ = _gamma(eta[i], tau[i], atoms)
        psi = (tau[i] / u) * hA - gam - (tau[i] / u) * fp * atoms
        c = float(h(kp)) - eta[i] * kp + (tau[i] / u) * (vK[i] - e + model.c0 - phi0 + fp * m0)
        A[i, :nA] = -psi
        A[i, nA] = 1.0
        b[i] = c
    cost = np.zeros(nA + 1)
    cost[nA] = -1.0
    Aeq = [np.concatenate((np.ones(nA), [0.0]))]
    beq = [1.0]
    if phi_prime is None:
        Aeq.append(np.concatenate((atoms, [0.0])))
        beq.append(m0)
    res = optimize.linprog(cost, A_ub=A, b_ub=b, A_eq=np.array(Aeq), b_eq=beq,
                           bounds=[(0, None)] * nA + [(None, None)], method='highs')
    if res.status != 0:
        return None
    rho = res.x[:nA]
    keep = rho > 1e-9
    lam_new = rho[keep] / rho[keep].sum()
    mu_new = atoms[keep]
    return float(res.x[nA]), lam_new, mu_new, float(val.min()), float(mi.min())


def merge(lam, mu, tol=1e-7, wmin=1e-7):
    """merge atoms closer than tol, drop tiny weights"""
    o = np.argsort(mu)
    lam, mu = np.asarray(lam)[o], np.asarray(mu)[o]
    L, Mv = [], []
    for l, m in zip(lam, mu):
        if l < wmin:
            continue
        if Mv and abs(m - Mv[-1]) < tol:
            tot = L[-1] + l
            Mv[-1] = (Mv[-1] * L[-1] + m * l) / tot
            L[-1] = tot
        else:
            L.append(l)
            Mv.append(m)
    L = np.array(L)
    return L / L.sum(), np.array(Mv)


def exit_grid(model, lam, mu, e, nK=161, nloc=31, levels=4, ntop=6):
    """base grid of exit types plus zoomed grids around the exits that are (nearly) active for
    the profile; the zoom points are kept, so that the active exit types are in the grid to
    about 1e-7."""
    K = np.linspace(0.004, 0.996, nK)
    B = e + alpha(model, lam, mu)

    def val(kk):
        r = (B - model.v(kk)) / model.u
        return fixed_type_solve(lam, mu, kk, r)[2]
    mi = val(K)
    fin = np.isfinite(mi)
    loc = [i for i in range(nK) if fin[i] and mi[i] <= (mi[i - 1] if i > 0 else np.inf)
           and mi[i] <= (mi[i + 1] if i < nK - 1 else np.inf)]
    loc = sorted(loc, key=lambda i: mi[i])[:ntop]
    extra = []
    if loc:
        a = np.array([K[max(i - 1, 0)] for i in loc])
        b = np.array([K[min(i + 1, nK - 1)] for i in loc])
        w = np.linspace(0.0, 1.0, nloc)
        for _ in range(levels):
            gg = a[:, None] + (b - a)[:, None] * w[None, :]
            vv = val(gg.ravel()).reshape(gg.shape)
            extra.append(gg.ravel())
            j = np.argmin(vv, axis=1)
            rows = np.arange(len(loc))
            a = gg[rows, np.maximum(j - 1, 0)]
            b = gg[rows, np.minimum(j + 1, nloc - 1)]
    return np.unique(np.concatenate([K] + extra))


def slp(model, lam, mu, e, phi_prime=None, nK=161, nM=401, iters=25, verbose=False, kw=None,
        steps=(1.0, 0.5, 0.25, 0.1, 0.03)):
    """SLP ascent from the profile (lam, mu).  Returns (value by S1, lam, mu, history)."""
    kw = kw or {}
    Mgrid = np.linspace(0.0, 1.0, nM)
    lam, mu = merge(lam, mu)
    cur = r_mu(model, lam, mu, e, **kw)
    hist = [cur]
    for it in range(iters):
        K = exit_grid(model, lam, mu, e, nK=nK)
        st = slp_step(model, lam, mu, e, K, Mgrid, phi_prime)
        if st is None:
            break
        t_lp, l1, m1, ref, refmi = st
        best = (cur, lam, mu)
        for s in steps:
            l2 = np.concatenate(((1 - s) * lam, s * l1))
            m2 = np.concatenate((mu, m1))
            l2, m2 = merge(l2, m2)
            val = r_mu(model, l2, m2, e, **kw)
            if np.isfinite(val) and val > best[0] + 1e-12:
                best = (val, l2, m2)
                if s == 1.0:
                    break
        if verbose:
            print(f"   it {it}: model at ref {ref:.8f} (grid exits {refmi:.8f}) cur {cur:.8f} LP {t_lp:.8f} -> {best[0]:.8f} atoms {len(best[2])}", flush=True)
        if best[0] <= cur + 1e-10:
            break
        cur, lam, mu = best
        hist.append(cur)
    return cur, lam, mu, hist


def coarsen(lam, mu, tol=0.004):
    """merge atoms that are within tol of each other (LP solutions on a grid come in adjacent pairs)"""
    return merge(lam, mu, tol=tol, wmin=1e-6)
