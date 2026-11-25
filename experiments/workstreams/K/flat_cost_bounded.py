"""Workstream K, numerical check (iv): what Algorithm 2L+ costs at the FLAT instance at a BOUNDED accuracy, for real n.

At the flat instance (psi = 0) every fibre average equals 1, so the outer loop is deterministic once the behaviour of
the inner procedure is fixed.  We take the inner bracket [W, W e^x] ("value at the bottom"), which is the worst valid
behaviour for the levels above the bulk (a point is classified LOW at level e^y only by an inner bracket of accuracy
<= y), and add the K points of the populated levels at the finest inner accuracy (the worst case there).  The inner
procedure is the base family of Proposition K0 (two-sample bracket with certified width), with the sample sizes of
its proof; all constants (K, nu, J, delta') are those of Theorem K1.  So the number computed is the exact number of
evaluations of the algorithm on this instance with this (valid) inner behaviour -- no expectations, no simulation.

Reported, for each n: ln(cost)/n for the best outer fraction phi of a grid, the certified accuracy, the cost of the
plain two-sample bracket at the same accuracy (exponent a), and the hinted lower bound (1-2 delta) 2^n/|B(n, k*(eps))|
at that accuracy (Theorem 11.25(a)); the necessary condition "no cost below the lower bound" is asserted.
Limits as n -> infinity:  a = KL(p_u||1/2) for the plain bracket,  tau_2 = min_phi max((1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi)))
for two levels,  h for the lower bound.
"""
import math, sys, time
import numpy as np
from klib import Cube, consts, theta_na, kl


def log_base_cost(cube, x, log_inv_delta, cache):
    """ln(#evaluations) of the base bracket (Proposition K0) of accuracy x on the cube `cube` with failure probability
    delta' (log_inv_delta = ln(1/delta')): 2 M, M = ceil(K 2^d / ((1-eta)|B(d, r*)|)), eta = min(1/2, tanh(x/4)),
    K = ceil(3(1+eta)/eta^2 ln(4/delta')), r* the largest radius with ln(1 + G2(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*;
    never more than full enumeration 2^d."""
    key = (round(x, 9), round(log_inv_delta, 6))
    if key in cache:
        return cache[key]
    d = cube.n
    eta = min(0.5, math.tanh(x / 4))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + log_inv_delta))
    budget = x - math.log((1 + eta) / (1 - eta))
    full = d * math.log(2)
    if budget <= 0:
        cache[key] = full
        return full
    rstar = -1
    lim = math.log(math.expm1(budget)) if budget < 30 else budget
    for r in range(0, d):
        if cube.lG2(r, eta) <= lim:
            rstar = r
        else:
            break
    if rstar < 0:
        cache[key] = full
        return full
    logM = math.log(K) + d * math.log(2) - math.log(1 - eta) - cube.lball_r(rstar)
    logM = max(logM, math.log(K / (1 - eta)))
    val = min(full, math.log(2) + logM)
    cache[key] = val
    return val


def flat_two_level(n, u, phi, b=0.5, lam=0.2, eta=0.05, etap=0.05, theta=0.05, delta=0.05, rates=None, tabs=None, nu1=None):
    """(ln cost, certified log-width, info) of Algorithm 2L+ at the flat instance, value-at-the-bottom inner brackets."""
    pu, lam1, estar, a, h = consts(u)
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    if tabs is None:
        tabs = {}
    outer = tabs.setdefault(("c", n_o), Cube(n_o, u))
    inner = tabs.setdefault(("c", n_i), Cube(n_i, u))
    icache = tabs.setdefault(("ic", n_i), {})
    if rates is None:
        rates = [estar * 0.85 ** i for i in range(40)]                  # geometric ladder of inner accuracy rates, ratio 0.85
    xs = [2 * u * n_i] + [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    L = len(xs) - 1
    J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
    if nu1 is None:
        nu1 = 2 * math.exp(u) * n_o / theta
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    # r_dagger and the constants of Theorem K1
    lth = math.log(theta)
    rdag = -1
    for r in range(0, n_o):
        okN = outer.lGt[r] <= lth + math.log((1 - eta) * nu0)
        okP = min(math.log((1 + eta) / (1 - eta)) + outer.lGt[r], outer.lG2(r, eta)) <= lth
        if okN and okP:
            rdag = r
        else:
            break
    lpidag = (outer.lball_r(rdag) if rdag >= 0 else math.log(0.5)) - n_o * math.log(2)
    mmax = math.ceil((math.log(2 * (1 + eta) * math.exp(lam) * nu0 / (1 - eta)) - lpidag) / math.log(2))
    Nev = (J + 1) * (mmax + 1) * (L + 2)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * Nev / delta))
    lnu = math.log(K * nu0)
    lMbar = math.log(2 * (1 + eta) * math.exp(lam) * nu0 * K / (1 - eta)) - lpidag
    log_inv_dp = math.log(4 * L / delta) + lMbar                         # delta' = delta / (4 L Mbar)
    lC = [0.0] + [log_base_cost(inner, x, log_inv_dp, icache) for x in xs[1:]]      # ln C(n_i, x_l, delta'); the trivial bracket costs 1
    lcum = np.logaddexp.accumulate(np.array(lC))                        # ln sum_{l' <= l} C(x_l')
    # the outer loop at the flat instance (psi = 0: s0 = e^{-un}, ell_ref = ((1+e^-u)/2)^n, W = 1)
    ls0 = -u * n
    lell = n * math.log((1 + math.exp(-u)) / 2)
    terms = [math.log(K) + lcum[L]]                                      # K points of the populated levels at the finest accuracy
    lMprev = math.log(K)
    closed = None
    # populated levels: all j with ln s_j < b (all points HIGH since L = 1 > s e^-b; M = N = K, q = 1, no closure as r = n_o);
    # ell is nondecreasing in j there, so only the last of them matters
    npop = min(J + 1, max(0, math.ceil((b - ls0) / lam)))                # number of j >= 0 with ls0 + j lam < b
    if npop > 0:
        ls = ls0 + (npop - 1) * lam
        lp = -math.log(1 + eta)
        k = outer.kball(n_o * math.log(2) + lp)
        lell = max(lell, ls - b + lp, ls - b - n_o * math.log(2) + outer.lT[k])
    nneg = 0
    lK = math.log(K)
    for j in range(npop, J + 1):
        ls = ls0 + j * lam
        y = ls                                                           # level e^y, y >= b: nothing HIGH; LOW needs accuracy <= y
        lidx = next(l for l in range(L + 1) if xs[l] <= y)
        lMneg = lnu + ls - lell - b
        # smallest M = K 2^m at which the level is left as negligible
        m_neg = max(0, math.ceil((lMneg - lK) / math.log(2) - 1e-12))
        # smallest M = K 2^m at which the closure test succeeds: tail(M) is nonincreasing in M
        #   (i) 2^{n_o} q < 1, q = K/((1-eta) M)                         <=>  M > K 2^{n_o}/(1-eta)
        m_close = max(0, math.floor((n_o * math.log(2) - math.log(1 - eta)) / math.log(2) + 1e-12) + 1)
        r_close = -1
        #   (ii) r(q) <= r_ok, r_ok the largest radius <= n_o - 1 with s_j 2^{-n_o} E_r <= theta e^b ell
        r_ok = int(np.searchsorted(outer.lE[:n_o], lth + b + lell - ls + n_o * math.log(2) + 1e-12, side="right")) - 1
        if r_ok >= 0:
            # need |B(r_ok)| >= 2^{n_o} q with q = min(1, K/((1-eta) M)) < 1 or r_ok such that the ball is not the whole cube
            need = n_o * math.log(2) - math.log(1 - eta) - outer.lball_r(r_ok)          # ln(M/K) >= need
            m2 = max(0, math.ceil(need / math.log(2) - 1e-12))
            if m2 < m_close:
                m_close = m2
                r_close = None
        m = min(m_neg, m_close)
        lM = lK + m * math.log(2)
        tail_ok = (m_close <= m_neg)
        if tail_ok:
            lq = min(0.0, math.log(K / (1 - eta)) - lM)
            r = -1 if n_o * math.log(2) + lq < 0 else outer.radius(lq)
        if lM > lMprev:                                                  # new points, each refined down to the accuracy x_lidx
            terms.append(lM + math.log1p(-math.exp(lMprev - lM)) + lcum[lidx])
            lMprev = lM
        if tail_ok:
            closed = dict(level=j, y=y, r=r, lM=lM, rdag=rdag, n_o=n_o)
            break
        nneg += 1
    if closed is None:
        return math.inf, None, None
    terms.append(lMprev)                                                 # one evaluation per sampled point (trivial bracket)
    mx = max(terms)
    lcost = mx + math.log(sum(math.exp(t - mx) for t in terms))
    width = math.log((2 * pu) ** n + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
    closed.update(K=K, lMbar=lMbar, lMdag=math.log(K / (1 - eta)) - lpidag, npop=npop, nneg=nneg, inner_finest=lC[L], Lx=L)
    return lcost, width, closed


def hinted_lower_bound(cube, eps, delta):
    """ln((1 - 2 delta) 2^n / |B(n, k*)|), k* the least k with Delta_k > eps, e^{Delta_k} - 1 = 2^{-n} E_k(n)   (Theorem 11.25(a))"""
    n = cube.n
    target = math.log(math.expm1(eps)) + n * math.log(2)
    k = int(np.searchsorted(cube.lE, target, side="right"))            # least k with ln E_k > target
    if k > n:
        return 0.0, None
    return math.log(1 - 2 * delta) + n * math.log(2) - cube.lball_r(k), k


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    ok = True
    delta = 0.05
    t0 = time.time()
    for u in ((1.0,) if quick else (1.0, 2.0)):
        pu, lam1, estar, a, h = consts(u)
        phis = np.linspace(0.02, 0.98, 97)
        tau2 = min(max((1 - p) * a, p * a + (1 - p) * theta_na(u, p * a / (1 - p))) for p in np.linspace(1e-3, 0.999, 2000))
        out(f"\n=== u = {u}: a = {a:.5f}, tau_2 = {tau2:.5f} = {tau2 / a:.4f} a, h = {h:.5f} = {h / a:.4f} a;  delta = {delta}")
        out(f"{'n':>7} | {'two-level ln(cost)/n':>20} | {'/a':>6} | {'phi':>5} | {'width':>6} | {'plain bracket /n':>16} | {'/a':>6} | {'hinted lower bound /n':>21} | {'/a':>6} | closes at r (r_dag), levels pop/neg, ln M_last/n")
        for n in ((500, 2000, 8000) if quick else (250, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000)):
            tabs = {}
            best = (math.inf, None, None, None)
            for phi in (0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85):
                c, w, info = flat_two_level(n, u, phi, delta=delta, tabs=tabs)
                if c < best[0]:
                    best = (c, w, info, phi)
            c, w, info, phi = best
            full = Cube(n, u)
            plain = log_base_cost(full, w, math.log(1 / delta), {})
            lb, kst = hinted_lower_bound(full, w, delta)
            out(f"{n:7d} | {c / n:20.5f} | {c / n / a:6.3f} | {phi:5.2f} | {w:6.3f} | {plain / n:16.5f} | {plain / n / a:6.3f} | {lb / n:21.5f} | {lb / n / a:6.3f} | r = {info['r']} ({info['rdag']}), {info['npop']}/{info['nneg']}, {info['lM'] / n:.5f}")
            if c < lb or plain < lb:
                ok = False; out("   A COST BELOW THE HINTED LOWER BOUND")
    out(f"\nno cost below the hinted lower bound: {ok}   ({time.time() - t0:.0f} s)")
    open("out_flat_cost_bounded.txt" if not quick else "out_flat_cost_bounded_quick.txt", "w").write("\n".join(lines) + "\n")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
