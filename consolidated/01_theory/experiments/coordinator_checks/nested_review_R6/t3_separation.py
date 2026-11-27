"""R6-T3: recomputation of the science division's finite-n separation table (SCI-REV-0007, section 5).

Column 1  ln C_max:  Theorem 11.56 (cost of Algorithm 2L+, a bound that holds in every run on every member of
          L_u(Q_n)) with the base brackets of Proposition 11.57(a) (explicit family: K_REPORT.md, Proposition K0)
          as inner procedures, in the design of K_REPORT.md section 6.4:
              b = 0.5, lambda = 0.2, eta = eta' = theta = 0.05, delta = 0.05, nu_1 = 2 e^u n_o/theta,
              inner ladder x_0 = 2 u n_i > (eps* 0.85^i n_i, i < 40, those strictly between b and 2 u n_i) > x_L = b,
              n_o = floor(phi n), n_i = n - n_o.
Column 2  ln LB_na:  Theorem 11.45(b) at the accuracy eps = x_out (the certified log-ratio of the bracket) and the
          same delta:  (1 - 2 delta) 2^n/|B(n, R-1)|, R the least radius with D_R > eps.
Column 3  ln of the hinted lower bound of Theorem 11.25(a) at the same eps, delta.

Usage:  python3 t3_separation.py            (the five rows of the review, their neighbours, phi = 0.50)
        python3 t3_separation.py grid       (in addition: outer fractions 0.45, 0.55 and the lowered cap)
"""
import sys, time
import mpmath as mp
from fractions import Fraction
from r6lib_coord import Tab, consts, constants_2Lplus, base_bracket_cost, nonadaptive_lb, hinted_lb, frac, outfile

DESIGN = dict(b=0.5, lam=0.2, eta=0.05, etap=0.05, theta=0.05, delta=0.05)


def two_level(n, u, phi, tabs, cap=None, design=DESIGN):
    """ln C_max of Theorem 11.56 with base brackets inside.  cap = None: M_bar of the theorem;
    cap = 'A': M_bar replaced by 2 max{e^lam M_dag, M_ddag} in C_max only (K, m_max, delta' unchanged);
    cap = 'B': replaced in C_max, m_max and delta' as the remark after Theorem 11.56 states."""
    b, lam, eta, etap, theta, delta = (design[k] for k in ("b", "lam", "eta", "etap", "theta", "delta"))
    pu, lam1, estar, a, h = consts(u)
    n_o = max(1, min(n - 1, int(phi * n + 1e-12)))
    n_i = n - n_o
    tab_o = tabs.setdefault((n_o, u), Tab(n_o, u))
    tab_i = tabs.setdefault((n_i, u), Tab(n_i, u))
    rates = [estar * 0.85 ** i for i in range(40)]
    xs = [2 * u * n_i] + [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    nu1 = 2 * mp.exp(mp.mpf(u)) * n_o / mp.mpf(theta)
    C = constants_2Lplus(n, n_o, u, lam, eta, etap, theta, nu1, b, delta, xs, tab_o)
    L, J, K = C["L"], C["J"], C["K"]
    Mbar, deltap, cnt = C["Mbar"], C["deltap"], C["cnt"]
    etaf, lamf = mp.mpf(eta), mp.mpf(lam)
    if cap is not None:
        Delta = int(mp.ceil(lamf / mp.mpf(u) - mp.mpf(10) ** -40))
        rd = C["rdag"]
        two_no = mp.mpf(2) ** n_o
        if rd >= Delta:
            Mdd = K / ((1 - etaf) * (mp.mpf(tab_o.ball[rd - Delta]) / two_no))
        else:
            Mdd = K * two_no / (1 - etaf)
        Mcap_over_K = 2 * max(mp.exp(lamf) * C["Mdag"], Mdd) / K
        if cap == "B":
            m_max = int(mp.ceil(mp.log(Mcap_over_K, 2)))
            K = int(mp.ceil(3 * (1 + etaf) / etaf ** 2 * mp.log(2 * (J + 1) * (m_max + 1) * (L + 2) / mp.mpf(delta))))
            nu = K * C["nu0"]
            cnt = lambda x, K=K, nu=nu: max(mp.mpf(K), 2 * (1 + etaf) ** 2 / (1 - etaf) * mp.exp(lamf) * nu * mp.exp(mp.mpf(x)))
            Mbar = Mcap_over_K * K
            deltap = mp.mpf(delta) / (4 * L * Mbar)
        else:
            Mbar = Mcap_over_K * K
    total = 1 + 2 * Mbar
    worst = (None, mp.mpf(0))
    for l in range(1, L + 1):
        Cl, info = base_bracket_cost(tab_i, xs[l], deltap)
        term = min(2 * Mbar, (J + 1) * cnt(xs[l - 1])) * Cl
        total += term
        if term > worst[1]:
            worst = (l, term)
    return dict(lnC=mp.log(total), x_out=C["x_out"], n_o=n_o, n_i=n_i, L=L, J=J, K=K, rdag=C["rdag"], lnMbar=mp.log(Mbar),
                lnMdag=mp.log(C["Mdag"]), worst_rung=worst[0], ln_worst=mp.log(worst[1]), m_max=C["m_max"])


def main():
    grid = len(sys.argv) > 1 and sys.argv[1] == "grid"
    rows = [(1.0, 1000), (1.0, 1350), (1.0, 1380), (1.0, 1400), (2.0, 520), (2.0, 540), (0.5, 4500), (0.5, 4700)]
    review = {(1.0, 1000): (126.3, 110.9, 31.7), (1.0, 1350): (150.8, 149.0, 42.0), (1.0, 1400): (154.0, 155.0, 43.5),
              (2.0, 540): (173.9, 176.5, 55.1), (0.5, 4700): (139.6, 141.5, 39.0),
              (2.0, 520): (170.1, 169.1, 53.4), (0.5, 4500): (136.3, 135.7, 37.3)}
    out = []
    def pr(s=""):
        print(s); out.append(s); sys.stdout.flush()
    pr("R6-T3: ln C_max (Theorem 11.56 + Proposition 11.57(a), design of K_REPORT 6.4, phi = 0.50) against ln LB_na (Theorem 11.45(b))")
    pr("       and the hinted lower bound (Theorem 11.25(a)), all at the accuracy eps = x_out and delta = 0.05")
    pr(f"{'u':>4} {'n':>6} | {'x_out':>8} | {'ln C_max':>10} {'(review)':>9} | {'ln LB_na':>10} {'(review)':>9} | {'R':>5} {'D_R':>9} {'D_{R-1}':>9} | "
       f"{'ln hinted':>9} {'(review)':>9} {'k*':>5} | {'C_max<LB_na':>11} | details")
    tabs = {}
    for (u, n) in rows:
        t0 = time.time()
        res = two_level(n, u, 0.5, tabs)
        tn = Tab(n, u)
        eps = res["x_out"]
        lb, R, D, Dm = nonadaptive_lb(tn, eps, DESIGN["delta"])
        hl, kst = hinted_lb(tn, eps, DESIGN["delta"])
        rv = review.get((u, n), (float("nan"),) * 3)
        pr(f"{u:4.1f} {n:6d} | {float(eps):8.5f} | {float(res['lnC']):10.3f} {rv[0]:9.1f} | {float(lb):10.3f} {rv[1]:9.1f} | {R:5d} {float(D):9.5f} {float(Dm):9.5f} | "
           f"{float(hl):9.3f} {rv[2]:9.1f} {kst:5d} | {str(res['lnC'] < lb):>11} | n_o={res['n_o']} L={res['L']} J={res['J']} K={res['K']} r_dag={res['rdag']} "
           f"m_max={res['m_max']} lnMbar={float(res['lnMbar']):.2f} lnMdag={float(res['lnMdag']):.2f} dominant rung l={res['worst_rung']} ({float(res['ln_worst']):.2f})  [{time.time() - t0:.1f} s]")
        del tn
    if grid:
        pr()
        pr("Outer fractions next to 0.50 (theorem's cap), and the lowered cap of the remark after Theorem 11.56")
        pr("  cap A: M_bar -> 2 max{e^lam M_dag, M_ddag} in C_max only (the science division's variant);  cap B: also in m_max, K and delta'")
        pr(f"{'u':>4} {'n':>6} {'phi':>5} | {'ln C_max':>10} | {'cap A':>10} | {'cap B':>10} | {'ln LB_na':>10}")
        cells = [(1.0, 1400, (0.45, 0.50, 0.55)), (2.0, 540, (0.45, 0.50, 0.55)), (0.5, 4700, (0.45, 0.50, 0.55)),
                 (1.0, 1275, (0.55,)), (1.0, 1300, (0.50, 0.55)), (2.0, 475, (0.55,)), (2.0, 500, (0.50, 0.55)),
                 (0.5, 4000, (0.55,)), (0.5, 4150, (0.50, 0.55))]
        for (u, n, phis) in cells:
            tn = Tab(n, u)
            for phi in phis:
                tabs = {}
                r0 = two_level(n, u, phi, tabs)
                rA = two_level(n, u, phi, tabs, cap="A")
                rB = two_level(n, u, phi, tabs, cap="B")
                lb, R, D, Dm = nonadaptive_lb(tn, r0["x_out"], DESIGN["delta"])
                pr(f"{u:4.1f} {n:6d} {phi:5.2f} | {float(r0['lnC']):10.3f} | {float(rA['lnC']):10.3f} | {float(rB['lnC']):10.3f} | {float(lb):10.3f}")
            del tn
    open(outfile("t3_separation_grid.txt" if grid else "t3_separation.txt"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
