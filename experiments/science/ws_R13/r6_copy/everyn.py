"""
everyn.py -- workstream R6: the cost bound of the two-level algorithm for EVERY n, with every constant explicit.

For given (u, n, phi) and a design (b, lam, eta, eta', theta, nu1, delta, ladder) this computes, from exact binomial tables
(r6lib.Tables; no asymptotics, no o(n)):

  C_max  = 1 + 2 Mbar + sum_l min{2 Mbar, (J+1) cnt(x_{l-1})} C_l      (Theorem K1 = 11.56), with
  C_l    = the cost of the base bracket of Proposition K0 = 11.57(a) in dimension n_i at accuracy x_l and failure
           probability delta' = delta/(4 L Mbar)   (two samples of size M_l, or enumeration when cheaper),
  x_out  = ln[(2p_u)^n + e^b(e^lam (1+eta)/(1-eta) + eta' + theta)]     (certified accuracy),
  plain  = cost of the base bracket alone in dimension n at accuracy x_out and failure probability delta,
  LB_hint = (1-2 delta) 2^n/|B(n, k*)|,  k* = least k with Delta_k > x_out            (Theorem 11.25(a), machine-checked),
  LB_na   = (1-2 delta) 2^n/|B(n, R-1)|, R  = least R with D_R > x_out                (Theorem 11.45(b), non-adaptive algorithms).

All of these are statements for the given n: the first two are upper bounds valid in every run on every member of L_u(Q_n)
(paper proofs K1, K0), the last two are lower bounds on expected numbers of evaluations.

usage: python3 everyn.py <u> <phi> <n1,n2,...> [design]
"""
import sys, math, time, json, os
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
from fractions import Fraction
import mpmath as mp
import r6lib as R

mp.mp.dps = 40
E = mp.e


def eta_for(x):
    """eta = min(1/2, tanh(x/4)), rounded DOWN to a rational with denominator 10^6 (a smaller eta keeps ln((1+eta)/(1-eta)) <= x/2)."""
    t = mp.tanh(mp.mpf(x) / 4)
    if t >= mp.mpf(1) / 2:
        return Fraction(1, 2)
    return Fraction(int(mp.floor(t * 10 ** 6)), 10 ** 6)


def k0_cost(d, u, x, deltap, tab):
    """Proposition K0: (ln cost, info) of the base family for (d, x, delta')."""
    eta = eta_for(x)
    two_d = mp.mpf(2) ** d
    if eta <= 0:
        return d * mp.log(2), dict(mode="enum")
    ef = mp.mpf(eta.numerator) / eta.denominator
    K = int(mp.ceil(3 * (1 + ef) / ef ** 2 * mp.log(4 / mp.mpf(deltap))))
    target = mp.mpf(x) - mp.log((1 + ef) / (1 - ef))
    thr = E ** target - 1                        # need Gamma''(r') <= thr for all r' <= r*
    rs = -1
    # kappa(r) is nondecreasing in r: advance a pointer instead of a binary search
    c_num, c_den = (1 - eta).numerator * (1 + eta).denominator, (1 - eta).denominator * (1 + eta).numerator   # c_eta = c_num/c_den
    k = 0
    for r in range(0, d):
        bm1 = tab.ballm1(r - 1)
        # largest k with |B(k)| * c_den <= max(c_den, c_num * bm1)
        bound = max(c_den, c_num * bm1)
        while k + 1 <= d and tab.ball[k + 1] * c_den <= bound:
            k += 1
        if tab.E[r] / tab.T[k] <= thr:
            rs = r
        else:
            break
    if rs < 0:
        return d * mp.log(2), dict(mode="enum", eta=str(eta), K=K)
    M = mp.ceil(K * two_d / ((1 - ef) * tab.ball[rs]))
    cost = 2 * M
    if cost >= two_d:
        return d * mp.log(2), dict(mode="enum", eta=str(eta), K=K, rstar=rs)
    return mp.log(cost), dict(mode="sample", eta=str(eta), K=K, rstar=rs, lnM=float(mp.log(M)))


def lower_bounds(n, u, eps, delta, tab_n):
    """hinted and non-adaptive lower bounds at accuracy eps (bracket ratio e^eps), from exact tables on Q_n."""
    two_n = mp.mpf(2) ** n
    # Delta_k = ln(1 + 2^-n E_k(n)); k* = least k with Delta_k > eps
    kstar = None
    thr = (E ** mp.mpf(eps) - 1) * two_n
    lo, hi = 0, n
    while lo < hi:                               # E_k is increasing in k
        mid = (lo + hi) // 2
        if tab_n.E[mid] > thr:
            hi = mid
        else:
            lo = mid + 1
    kstar = lo
    ln_hint = mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2) - mp.log(tab_n.ball[kstar])
    # D_R = n ln(1+e^-u) - ln sum_j C(n,j) e^{-u max(j,R)};  sum = e^{-uR}|B(R-1)|... precisely
    #   sum_j C(n,j) e^{-u max(j,R)} = e^{-uR} |B(n,R)| + sum_{j>R} C(n,j) e^{-uj} = e^{-uR} T_n(R)   (T_n(R) = |B(R)| + sum_{j>R} C e^{-u(j-R)})
    # so D_R = n ln(1+e^-u) + uR - ln T_n(R); D_R increasing in R.
    uu = mp.mpf(u)
    base = n * mp.log(1 + E ** (-uu))

    def D(Rr):
        return base + uu * Rr - mp.log(tab_n.T[Rr])
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if D(mid) > eps:
            hi = mid
        else:
            lo = mid + 1
    Rmin = lo
    if Rmin == 0:
        ln_na = mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2)     # |B(-1)| read as 1 -> full evaluation
    else:
        ln_na = mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2) - mp.log(tab_n.ball[Rmin - 1])
    return dict(kstar=kstar, ln_hint=ln_hint, Rmin=Rmin, ln_na=ln_na, D_Rmin=float(D(Rmin)))


DESIGNS = {
    # the design of K_REPORT 6.4 / ENG-RES-0008 (as far as their text specifies it): b = 0.5, lam = 0.2, eta = eta' = theta = 0.05,
    # nu1 = 2 e^u n_o/theta, delta = 0.05, inner rates eps* 0.85^i (i < 40), certified accuracy 0.872
    "K64": dict(b=0.5, lam=0.2, eta=Fraction(1, 20), etap=0.05, theta=0.05, delta=0.05, ratio=0.85, nr=40),
    # a coarser design with a larger certified accuracy (x_out about 2.9): smaller polynomial factors
    "coarse": dict(b=0.5, lam=1.0, eta=Fraction(1, 2), etap=1.0, theta=1.0, delta=0.05, ratio=0.85, nr=40),
}


def two_level(n, u, phi, design="K64", tabs=None, verbose=False):
    D = DESIGNS[design]
    uu = mp.mpf(u)
    n_o = int(math.floor(phi * n))
    n_i = n - n_o
    eps_star = mp.log(mp.cosh(uu / 2))
    b = D["b"]
    xs = [2 * uu * n_i]
    for i in range(D["nr"]):
        x = eps_star * mp.mpf(D["ratio"]) ** i * n_i
        if x > b * 1.0000001 and x < xs[-1]:
            xs.append(x)
    xs.append(mp.mpf(b))
    L = len(xs) - 1
    tabs = {} if tabs is None else tabs
    for m in (n_o, n_i, n):
        if m not in tabs:
            tabs[m] = R.Tables(m, u)
    P = R.Params2LP(n, n_o, u, D["lam"], D["eta"], D["etap"], D["theta"], 2 * float(E ** uu) * n_o / D["theta"], b, D["delta"],
                    xs, [1] * L, tables=tabs[n_o])
    lnC = [None]
    info = []
    for l in range(1, L + 1):
        c, inf = k0_cost(n_i, u, xs[l], P.deltap, tabs[n_i])
        lnC.append(c)
        info.append(inf)
    terms = [mp.log(2 * P.Mbar)]
    for l in range(1, L + 1):
        terms.append(mp.log(min(2 * P.Mbar, (P.J + 1) * P.cnt(xs[l - 1]))) + lnC[l])
    mx = max(terms)
    lnCmax = mx + mp.log(mp.fsum(E ** (t - mx) for t in terms) + E ** (-mx))
    # the same with the lowered cap of the remark of 40c5bd7: Mbar -> cap_new in C_max (m_max, delta' kept: they only matter through K and C_l)
    terms2 = [mp.log(2 * P.cap_new)]
    for l in range(1, L + 1):
        terms2.append(mp.log(min(2 * P.cap_new, (P.J + 1) * P.cnt(xs[l - 1]))) + lnC[l])
    mx2 = max(terms2)
    lnCmax2 = mx2 + mp.log(mp.fsum(E ** (t - mx2) for t in terms2) + E ** (-mx2))
    lnplain, pinfo = k0_cost(n, u, P.x_out, D["delta"], tabs[n])
    lb = lower_bounds(n, u, P.x_out, D["delta"], tabs[n])
    a = mp.log(2) - (-(1 / (1 + E ** uu)) * mp.log(1 / (1 + E ** uu)) - (1 - 1 / (1 + E ** uu)) * mp.log(1 - 1 / (1 + E ** uu)))
    out = dict(n=n, u=float(u), phi=phi, n_o=n_o, design=design, L=L, x_out=float(P.x_out), J=P.J, K=P.K, rdag=P.rdag,
               lnMdag=float(mp.log(P.Mdag)), lnMbar=float(mp.log(P.Mbar)), lncap=float(mp.log(P.cap_new)), lnCmax=float(lnCmax),
               lnCmax_cap=float(lnCmax2), lnplain=float(lnplain), ln_hint=float(lb["ln_hint"]), ln_na=float(lb["ln_na"]), kstar=lb["kstar"],
               Rmin=lb["Rmin"], a=float(a), argmax_term=int(max(range(len(terms)), key=lambda i: terms[i])),
               inner_modes=[i["mode"] for i in info])
    na = n * float(a)
    out.update(Cmax_na=out["lnCmax"] / na, Cmaxcap_na=out["lnCmax_cap"] / na, plain_na=out["lnplain"] / na, hint_na=out["ln_hint"] / na,
               na_na=out["ln_na"] / na)
    return out, P, xs, lnC


if __name__ == "__main__":
    u = float(sys.argv[1])
    phi = float(sys.argv[2])
    ns = [int(x) for x in sys.argv[3].split(",")]
    design = sys.argv[4] if len(sys.argv) > 4 else "K64"
    print("%7s %5s | %7s %7s %7s | %8s %8s %8s %8s %8s | %s" % ("n", "phi", "x_out", "lnMdag", "lnMbar", "Cmax/na", "cap/na", "plain/na", "LBna/na",
                                                               "LBhint/na", "ln: Cmax, Cmax(cap), plain, LB_na, LB_hint"))
    for n in ns:
        t0 = time.time()
        o, P, xs, lnC = two_level(n, u, phi, design)
        print("%7d %5.2f | %7.3f %7.1f %7.1f | %8.4f %8.4f %8.4f %8.4f %8.4f | %.1f %.1f %.1f %.1f %.1f  (%.0fs)" % (
            n, phi, o["x_out"], o["lnMdag"], o["lnMbar"], o["Cmax_na"], o["Cmaxcap_na"], o["plain_na"], o["na_na"], o["hint_na"],
            o["lnCmax"], o["lnCmax_cap"], o["lnplain"], o["ln_na"], o["ln_hint"], time.time() - t0))
        sys.stdout.flush()
        _os.makedirs(_os.path.join(HERE, "data"), exist_ok=True)
        with open(HERE + "/data/everyn_%s.jsonl" % design, "a") as f:
            f.write(json.dumps(o) + "\n")
