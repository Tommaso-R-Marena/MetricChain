import time, sys, numpy as np, mpmath as mp
from fractions import Fraction
import r6lib as R, instances as I, checks as C

def setup(n, n_o, u, x, L_ext=6, eta=None, c0=None, delta=0.05, Kov=None, costs=None):
    """bounded regime as in the proof of Theorem K2: b = x/2, lam = eta = eta' = theta = c0 = min(x/12, 1/3), nu1 = 2e^u n_o/theta;
    ladder: x_0 = 2u n_i, geometric rungs down to x_{L-1}, x_L = b."""
    n_i = n - n_o
    b = x / 2
    if c0 is None: c0 = min(x / 12, 1 / 3)
    if eta is None: eta = Fraction(c0).limit_denominator(1000)
    x0 = 2 * u * n_i
    xs = [x0]
    ratio = (b * 1.5 / x0) ** (1.0 / L_ext)
    for l in range(1, L_ext + 1):
        xs.append(x0 * ratio ** l)
    xs.append(b)
    if costs is None:
        costs = [float(np.exp(min(50.0, 0.5 * (x0 - xl) / u ** 0 * 0.02))) for xl in xs[1:]]
    P = R.Params2LP(n, n_o, u, lam=c0, eta=eta, etap=c0, theta=c0, nu1=2 * np.e ** u * n_o / c0, b=b, delta=delta,
                    xs=xs, costs=costs, K_override=Kov)
    return P

if __name__ == "__main__":
    n, n_o, u, x = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    t0 = time.time()
    P = setup(n, n_o, u, x)
    print("setup %.1fs" % (time.time() - t0), "J", P.J, "K", P.K, "rdag", P.rdag, "p_u n_o", n_o / (1 + np.e ** u), "m_max", P.m_max,
          "lnMdag", float(mp.log(P.Mdag)), "lnMbar", float(mp.log(P.Mbar)), "lncap", float(mp.log(P.cap_new)), "x_out", float(P.x_out),
          "lnCmax", float(mp.log(P.Cmax)), "ln 2^62", 62 * np.log(2))
    for prof in ["flat", "cone", "dip", "eq"]:
        rng = np.random.default_rng(1)
        F = {"flat": I.prof_flat(n_o, u), "cone": I.prof_cone(n_o, u), "dip": I.prof_dip(n_o, u, int(0.3 * n_o)), "eq": I.prof_equal_mass(n_o, u)}[prof]
        inst = I.radial(n, n_o, u, F, d0=0, s_in=0.0, strats=(R.S_CENTER,))
        t0 = time.time()
        run = R.Run(P, inst, R.SimOracle(P.xs, rng), rng).run()
        t1 = time.time()
        ck = C.check_2LP(run)
        st = [r["status"] for r in run.levels]
        print(prof, run.status, run.abort_reason, "levels", len(run.levels), "pop", st.count("populated"), "neg", st.count("negligible"),
              "units", len(run.cnt), "lnM", float(mp.log(run.points_drawn)), "run %.1fs check %.1fs" % (t1 - t0, time.time() - t1))
        print("   G", ck["G"], ck["Gfail"][:2], "det", ck["det"][:2], "good", ck["good"][:2], {k: round(v, 4) for k, v in ck["ratios"].items()})
        if run.status == "closed":
            lo, up = run.result; lnA = mp.log(inst.A)
            print("   bracket", float(lo - lnA), float(up - lnA), "width", float(up - lo), "closed at level", run.final["j"], "tail>0", run.final["tail"] > 0)
