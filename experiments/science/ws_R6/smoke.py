import time, numpy as np, mpmath as mp
from fractions import Fraction
import r6lib as R, instances as I, checks as C

def one(n=24, n_o=12, u=1.0, seed=0, prof="flat", strat=(R.S_CENTER,), verbose=True, Kov=None):
    rng = np.random.default_rng(seed)
    n_i = n - n_o
    b = 0.5
    c0 = 0.2
    xs = [2*u*n_i, 12.0, 6.0, 3.0, 1.5, 0.5]
    costs = [10, 100, 1000, 10**4, 10**5]
    P = R.Params2LP(n, n_o, u, lam=c0, eta=Fraction(1,5), etap=c0, theta=c0, nu1=2*np.e**u*n_o/c0, b=b, delta=0.05,
                    xs=xs, costs=costs, K_override=Kov)
    if prof == "flat": F = I.prof_flat(n_o, u)
    elif prof == "cone": F = I.prof_cone(n_o, u)
    elif prof == "dip": F = I.prof_dip(n_o, u, 3)
    elif prof == "eq": F = I.prof_equal_mass(n_o, u)
    inst = I.radial(n, n_o, u, F, d0=0, s_in=0.0, strats=strat)
    orc = R.SimOracle(xs, rng)
    t0 = time.time()
    run = R.Run(P, inst, orc, rng).run()
    ck = C.check_2LP(run)
    if verbose:
        print(prof, "J", P.J, "K", P.K, "rdag", P.rdag, "m_max", P.m_max, "lnMbar", float(mp.log(P.Mbar)), "lnMdag", float(mp.log(P.Mdag)),
              "lncap", float(mp.log(P.cap_new)), "x_out", float(P.x_out), "lnCmax", float(mp.log(P.Cmax)))
        print(" status", run.status, run.abort_reason, "levels", len(run.levels), "units", len(run.cnt), "points", run.points_drawn,
              "lnq", float(mp.log(run.queries())), "time %.2f" % (time.time()-t0))
        if run.status == "closed":
            lo, up = run.result
            lnA = mp.log(inst.A)
            print(" bracket", float(lo - lnA), float(up - lnA), "width", float(up - lo))
        st = [r["status"] for r in run.levels]
        print(" populated", st.count("populated"), "negligible", st.count("negligible"), "calls", run.calls)
        print(" check: G", ck["G"], ck["Gfail"][:3], "det", ck["det"][:3], "good", ck["good"][:3])
        print(" ratios", {k: round(v, 4) for k, v in ck["ratios"].items()})
    return run, ck

if __name__ == "__main__":
    for prof in ["flat", "cone", "dip", "eq"]:
        one(prof=prof)
    one(prof="flat", strat=(R.S_ADV_HI,))
    one(prof="dip", strat=(R.S_ADV_LO, R.S_BOTTOM, R.S_TOP))
