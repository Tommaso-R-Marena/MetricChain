"""
campaign.py -- workstream R6: run Algorithm 2L+ (Theorem K1 = 11.56) and Algorithm 2L (Theorem 11.52) with a simulated
inner oracle on radial outer landscapes, with the constants of the theorems, and check every claim run by run.

usage:  python3 campaign.py <campaign-name> <nruns> <seed> [nproc]
writes data/<campaign-name>_<seed>.jsonl (one line per run) and prints a summary.
"""
import sys, json, time, os
import numpy as np
import mpmath as mp
from fractions import Fraction
from multiprocessing import Pool
import r6lib as R, instances as I, checks as C

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------------------------------------ cells
def cell_bounded(n, n_o, u, x, L_ext=5, delta=0.05, Kov=None, eta=None):
    """parameters of the proof of Theorem K2: b = x/2, lam = eta = eta' = theta = c0 = min(x/12, 1/3), nu1 = 2e^u n_o/theta."""
    n_i = n - n_o
    b = x / 2
    c0 = min(x / 12, 1 / 3)
    eta = Fraction(c0).limit_denominator(1000) if eta is None else eta
    return dict(kind="2L+", n=n, n_o=n_o, u=u, lam=c0, eta=eta, etap=c0, theta=c0, nu1=2 * float(np.e) ** u * n_o / c0, b=b,
                delta=delta, L_ext=L_ext, Kov=Kov)


def cell_general(n, n_o, u, b, lam, eta, etap, theta, nu1=None, L_ext=5, delta=0.05, Kov=None):
    if nu1 is None:
        nu1 = 2 * float(np.e) ** u * n_o / theta
    return dict(kind="2L+", n=n, n_o=n_o, u=u, lam=lam, eta=eta, etap=etap, theta=theta, nu1=nu1, b=b, delta=delta, L_ext=L_ext, Kov=Kov)


def cell_extensive(n, n_o, u, g, xi_last, L_ext=5, delta=0.05, Kov=None):
    """Corollary K1.b: b = x_L = xi_last n_i, lam = 1, eta = 1/2, eta' = 1, nu1 = 1, theta = e^{gn-b} - (3e+1) - (2p_u)^n e^{-b}."""
    n_i = n - n_o
    b = xi_last * n_i
    theta = mp.e ** (g * n - b) - (3 * mp.e + 1) - (2 / (1 + mp.e ** u)) ** n * mp.e ** (-b)
    assert theta > 0
    return dict(kind="2L+", n=n, n_o=n_o, u=u, lam=1.0, eta=Fraction(1, 2), etap=1.0, theta=theta, nu1=1.0, b=b, delta=delta,
                L_ext=L_ext, Kov=Kov, ext=True)


def cell_2L(n, n_o, u, g, xi_last, L_ext=5, delta=0.05, Kov=None):
    """Theorem 11.52: G = g n, tolerance b = x_last = xi_last n_i (so beta = (1-phi) xi_last)."""
    return dict(kind="2L", n=n, n_o=n_o, u=u, G=g * n, b=xi_last * (n - n_o), delta=delta, L_ext=L_ext, Kov=Kov)


_TABLES = {}


def tables(n_o, u):
    key = (n_o, float(u))
    if key not in _TABLES:
        _TABLES[key] = R.Tables(n_o, u)
    return _TABLES[key]


def ladder(cell, rng=None):
    """x_0 = 2 u n_i > ... > x_L with x_L slightly below b (a generic last rung avoids the floating-point tie of erratum m10)."""
    n_i = cell["n"] - cell["n_o"]
    x0 = 2 * cell["u"] * n_i
    b = float(cell["b"])
    xl = b * (1 - 1e-9)
    Lx = cell["L_ext"]
    xs = [x0]
    if Lx > 0 and x0 > 1.2 * b:
        top = x0 * 0.6
        lo = max(b * 1.5, xl * 1.01)
        if top > lo:
            for i in range(Lx):
                xs.append(top * (lo / top) ** (i / max(Lx - 1, 1)))
        xs = sorted(set(xs), reverse=True)
    xs.append(xl)
    costs = [10.0 ** l for l in range(1, len(xs))]
    return xs, costs


def make_params(cell):
    xs, costs = ladder(cell)
    tab = tables(cell["n_o"], cell["u"])
    if cell["kind"] == "2L+":
        return R.Params2LP(cell["n"], cell["n_o"], cell["u"], cell["lam"], cell["eta"], cell["etap"], cell["theta"], cell["nu1"],
                           cell["b"], cell["delta"], xs, costs, K_override=cell.get("Kov"), tables=tab)
    return R.Params2L(cell["n"], cell["n_o"], cell["u"], cell["G"], cell["delta"], xs, costs, K_override=cell.get("Kov"), tables=tab)


# ------------------------------------------------------------------------------------------------ instances
PROFILES = ["flat", "cone", "cone_half", "cone_quarter", "dip", "dip_crit", "flatcone", "platcone", "eqmass", "rw_uniform", "rw_pm",
            "rw_down", "rw_lazy", "alternating", "staircase", "grid_rw", "two_plateaus"]


def make_profile(name, cell, P, rng):
    n_o, u = cell["n_o"], cell["u"]
    lam = float(P.lam)
    if name == "flat":
        return I.prof_flat(n_o, u)
    if name == "cone":
        return I.prof_cone(n_o, u)
    if name == "cone_half":
        return I.prof_cone(n_o, u, u / 2)
    if name == "cone_quarter":
        return I.prof_cone(n_o, u, u / 4)
    if name == "dip":
        return I.prof_dip(n_o, u, int(rng.integers(1, max(2, n_o // 2))))
    if name == "dip_crit":
        # radius near the closing radius / near Lambda_1 n_o / u (the critical dip of the hinted problem)
        lam1 = np.log(2 / (1 + np.exp(-u)))
        centre = rng.choice([max(P.rdag, 1), int(lam1 * n_o / u), int(n_o / (1 + np.exp(u)))])
        return I.prof_dip(n_o, u, int(max(1, centre + rng.integers(-3, 4))))
    if name == "flatcone":
        return I.prof_flattened_cone(n_o, u, int(rng.integers(1, max(2, n_o // 2))))
    if name == "platcone":
        return I.prof_plateau_cone(n_o, u, int(rng.integers(1, max(2, n_o // 2))))
    if name == "eqmass":
        return I.prof_equal_mass(n_o, u)
    if name.startswith("rw_"):
        return I.prof_random_walk(n_o, u, rng, name[3:])
    if name == "alternating":
        return I.prof_alternating(n_o, u)
    if name == "staircase":
        return I.prof_staircase(n_o, u, int(rng.integers(1, 6)), float(rng.uniform(0.2, 1.0)) * u)
    if name == "grid_rw":
        # steps are integer multiples of lam (ties with the level grid when u n / lam is an integer and the fibre is flat)
        kmax = int(np.floor(u / lam + 1e-12))
        if kmax == 0:
            return I.prof_flat(n_o, u)
        steps = rng.integers(-kmax, kmax + 1, size=n_o) * lam
        return np.concatenate([[0.0], np.cumsum(steps)])
    if name == "two_plateaus":
        # bulk, then a plateau higher by H on the ball of radius R (ramps of slope u between them)
        Rr = int(rng.integers(1, max(2, n_o // 3)))
        H = float(rng.uniform(0.5, 12.0))
        d = np.arange(n_o + 1, dtype=float)
        return np.clip(u * (Rr - d) + H, 0.0, H)
    raise ValueError(name)


STRAT_SETS = {
    "center": (R.S_CENTER,), "top": (R.S_TOP,), "bottom": (R.S_BOTTOM,), "adv_hi": (R.S_ADV_HI,), "adv_lo": (R.S_ADV_LO,),
    "exact": (R.S_EXACT,), "random": (R.S_RANDOM,), "narrow": (R.S_NARROW,),
    "mix3": (R.S_ADV_HI, R.S_ADV_LO, R.S_CENTER), "mix_tb": (R.S_TOP, R.S_BOTTOM),
}
INVALID_SETS = {
    "inv_above": (R.S_INV_ABOVE, R.S_CENTER), "inv_below": (R.S_INV_BELOW, R.S_CENTER), "too_wide": (R.S_TOO_WIDE,),
    "trivial": (R.S_TRIVIAL,), "inv_mix": (R.S_INV_ABOVE, R.S_INV_BELOW, R.S_TOO_WIDE, R.S_ADV_HI),
    "inv_above_all": (R.S_INV_ABOVE,), "inv_below_all": (R.S_INV_BELOW,), "lazy": (R.S_LAZY,), "lazy_mix": (R.S_LAZY, R.S_BOTTOM),
}


def one_run(args):
    cell, prof, sname, seed, opts = args
    rng = np.random.default_rng(seed)
    P = make_params(cell)
    n, n_o, u = cell["n"], cell["n_o"], cell["u"]
    F = make_profile(prof, cell, P, rng)
    d0 = int(rng.choice([0, n_o // 2, n_o, int(rng.integers(0, n_o + 1))]))
    s_in = float(rng.choice([0.0, 0.0, u, -u, u / 2, -u / 2]))
    if prof == "grid_rw" or opts.get("flat_fibre"):
        s_in = 0.0
    strats = dict(STRAT_SETS, **INVALID_SETS)[sname]
    w = rng.dirichlet(np.ones(len(strats)))
    w = [mp.mpf(float(x)) for x in w]
    tot = mp.fsum(w)
    w = [x / tot for x in w]
    inst = I.radial(n, n_o, u, F, d0=d0, s_in=s_in, strats=strats, weights=w, name=prof)
    orc = R.SimOracle(P.xs, rng)
    t0 = time.time()
    try:
        run = R.Run(P, inst, orc, rng, variant=cell["kind"], mutation=opts.get("mutation")).run()
    except AssertionError as ex:
        return dict(cell=cell_tag(cell), prof=prof, strat=sname, seed=seed, harness_limit=str(ex))
    ck = C.check_2LP(run) if cell["kind"] == "2L+" else C.check_2L(run)
    st = [r["status"] for r in run.levels]
    rec = dict(cell=cell_tag(cell), prof=prof, strat=sname, seed=seed, d0=d0, s_in=s_in, status=run.status, abort=run.abort_reason,
               levels=len(run.levels), pop=st.count("populated"), neg=st.count("negligible"),
               lnM=float(mp.log(run.points_drawn)), lnq=float(mp.log(run.queries())), calls=[int(c) if c < 2 ** 62 else float(c) for c in run.calls],
               G=ck["G"], Gfail=[str(x) for x in ck["Gfail"][:4]], det=[str(x) for x in ck["det"][:6]], good=[str(x) for x in ck["good"][:6]],
               ratios=ck["ratios"], secs=round(time.time() - t0, 2), K=P.K, J=P.J, rdag=P.rdag, lnMdag=float(mp.log(P.Mdag)) if P.Mdag != mp.inf else None,
               lnCmax=float(mp.log(P.Cmax)) if P.Cmax != mp.inf else None, q_le_Cmax=bool(run.queries() <= P.Cmax))
    if run.status == "closed":
        lo, up = run.result
        lnA = mp.log(inst.A)
        last = run.levels[-1]["passes"][-1]
        rec.update(lo=float(lo - lnA), up=float(up - lnA), width=float(up - lo), close_pop=bool(last["populated"]),
                   close_tail0=bool(last["tail"] == 0), close_r=int(last["r"]), close_level=run.final["j"])
    return rec


def cell_tag(cell):
    c = dict(cell)
    for k, v in c.items():
        if isinstance(v, Fraction):
            c[k] = str(v)
        elif isinstance(v, mp.mpf):
            c[k] = "e^%.3f" % float(mp.log(v))
    return json.dumps(c, sort_keys=True)


CAMPAIGNS = {}


def campaign(name):
    def deco(f):
        CAMPAIGNS[name] = f
        return f
    return deco


@campaign("A_small")          # theorem constants, valid oracle, small cubes
def _a_small():
    cells = [cell_bounded(24, 12, 1.0, 1.0), cell_bounded(24, 12, 1.0, 4.0), cell_bounded(48, 24, 0.5, 4.0), cell_bounded(80, 40, 1.0, 4.0),
             cell_bounded(40, 10, 2.0, 2.0), cell_general(64, 32, 1.0, 0.5, 0.5, Fraction(1, 2), 1.0, 1.0),
             cell_general(64, 32, 2.0, 1.0, 1.0, Fraction(1, 4), 0.5, 0.25, nu1=1.0), cell_extensive(60, 30, 1.0, 0.25, 0.1)]
    return cells, PROFILES, list(STRAT_SETS), {}


@campaign("A_medium")         # theorem constants, valid oracle, n_o = 100..250
def _a_medium():
    cells = [cell_bounded(300, 120, 1.0, 4.0), cell_bounded(200, 100, 2.0, 4.0), cell_bounded(500, 250, 1.0, 4.0),
             cell_bounded(1000, 500, 0.5, 4.0), cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0),
             cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0), cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5),
             cell_general(500, 250, 1.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0), cell_extensive(2000, 1000, 1.0, 0.03, 0.02),
             cell_extensive(1200, 400, 1.0, 0.025, 0.015), cell_extensive(600, 300, 2.0, 0.08, 0.04), cell_extensive(1000, 500, 1.0, 0.045, 0.03)]
    return cells, PROFILES, list(STRAT_SETS), {}


@campaign("A_ties")           # dyadic lam, u n/lam integer, flat fibres, grid profiles: W exactly on levels and on s_j e^{-b}
def _a_ties():
    cells = [cell_general(48, 24, 1.0, 0.5, 0.5, Fraction(1, 2), 1.0, 1.0), cell_general(64, 32, 1.0, 1.0, 0.25, Fraction(1, 4), 0.5, 0.5),
             cell_general(200, 100, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 1.0), cell_general(300, 120, 1.0, 1.0, 1.0, Fraction(1, 2), 1.0, 1.0),
             cell_general(200, 100, 2.0, 1.0, 1.0, Fraction(1, 2), 1.0, 1.0, nu1=1.0)]
    return cells, ["grid_rw", "flat", "cone", "staircase", "two_plateaus", "dip_crit"], ["top", "bottom", "mix_tb", "exact", "adv_hi", "adv_lo"], dict(flat_fibre=True)


@campaign("B_reducedK")       # K reduced: the events of the proof fail often; claims must hold whenever they hold
def _b_reduced():
    cells = []
    for Kov in (8, 20, 50):
        cells += [cell_bounded(80, 40, 1.0, 4.0, Kov=Kov), cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, Kov=Kov),
                  cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5, Kov=Kov), cell_extensive(1200, 400, 1.0, 0.025, 0.015, Kov=Kov),
                  cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0, Kov=Kov)]
    return cells, PROFILES, list(STRAT_SETS), {}


@campaign("B_invalid")        # invalid inner answers: the statements "for every run" must survive
def _b_invalid():
    cells = [cell_bounded(80, 40, 1.0, 4.0), cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0),
             cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0), cell_extensive(1200, 400, 1.0, 0.025, 0.015),
             cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5), cell_bounded(24, 12, 1.0, 1.0),
             cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, Kov=20)]
    return cells, PROFILES, list(INVALID_SETS), {}


@campaign("B_lazy")           # invalid answers designed to make the cost abort fire: "the cost bound holds always"
def _b_lazy():
    cells = [cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0), cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0),
             cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5), cell_bounded(300, 120, 1.0, 4.0), cell_bounded(80, 40, 1.0, 4.0),
             cell_extensive(1200, 400, 1.0, 0.025, 0.015)]
    return cells, ["cone", "cone_half", "platcone", "flatcone", "eqmass", "dip_crit", "rw_down", "flat", "two_plateaus"], ["lazy", "lazy_mix"], {}


@campaign("D_2L")             # Algorithm 2L of Theorem 11.52, constants of the theorem
def _d_2l():
    cells = [cell_2L(60, 30, 1.0, 0.25, 0.1), cell_2L(2000, 1000, 1.0, 0.03, 0.02), cell_2L(1200, 400, 1.0, 0.025, 0.015), cell_2L(600, 300, 2.0, 0.08, 0.04),
             cell_2L(1000, 500, 1.0, 0.045, 0.03), cell_2L(40, 12, 1.0, 0.9, 0.2), cell_2L(600, 300, 2.0, 0.06, 0.03), cell_2L(3000, 1500, 0.5, 0.008, 0.005)]
    return cells, PROFILES, list(STRAT_SETS), {}


@campaign("D_2L_off")         # Algorithm 2L off the good event (reduced K, invalid answers)
def _d_2l_off():
    cells = [cell_2L(60, 30, 1.0, 0.25, 0.1, Kov=10), cell_2L(1200, 400, 1.0, 0.025, 0.015, Kov=10), cell_2L(600, 300, 2.0, 0.08, 0.04, Kov=30),
             cell_2L(1200, 400, 1.0, 0.025, 0.015), cell_2L(600, 300, 2.0, 0.08, 0.04)]
    return cells, PROFILES, list(STRAT_SETS) + list(INVALID_SETS), {}


def _mut(name):
    def f():
        cells = [cell_bounded(80, 40, 1.0, 4.0), cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0),
                 cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0), cell_bounded(300, 120, 1.0, 4.0),
                 cell_general(40, 8, 1.0, 3.0, 1.0, Fraction(1, 2), 1.0, 30.0, nu1=1.0), cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5)]
        return cells, PROFILES, list(STRAT_SETS), dict(mutation=name)
    return f


for _m in ("neg_tol", "noharper", "maxform", "close_at_no", "q_no_eta"):
    CAMPAIGNS["MUT_" + _m] = _mut(_m)


def summarise(recs):
    S = dict(runs=len(recs), harness_limit=0, closed=0, abort=0, Gfail=0, det_viol=0, good_viol=0, pop=0, neg=0, runs_with_neg=0,
             close_pop=0, close_unpop=0, close_tail0=0, invalid_bracket_any=0, maxratio={})
    for r in recs:
        if "harness_limit" in r:
            S["harness_limit"] += 1
            continue
        S["closed"] += r["status"] == "closed"
        S["abort"] += r["status"] == "abort"
        S["Gfail"] += (not r["G"])
        S["det_viol"] += bool(r["det"])
        S["good_viol"] += bool(r["good"])
        S["pop"] += r["pop"]
        S["neg"] += r["neg"]
        S["runs_with_neg"] += r["neg"] > 0
        if r["status"] == "closed":
            S["close_pop"] += r["close_pop"]
            S["close_unpop"] += (not r["close_pop"])
            S["close_tail0"] += r["close_tail0"]
            S["invalid_bracket_any"] += (r["lo"] > 1e-9 or r["up"] < -1e-9)
        for k, v in r["ratios"].items():
            S["maxratio"][k] = max(S["maxratio"].get(k, 0.0), v)
    return S


if __name__ == "__main__":
    name, nruns, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    nproc = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    cells, profs, strats, opts = CAMPAIGNS[name]()
    rng = np.random.default_rng(seed)
    jobs = []
    for i in range(nruns):
        cell = cells[i % len(cells)]
        jobs.append((cell, str(rng.choice(profs)), str(rng.choice(strats)), int(rng.integers(0, 2 ** 31)), opts))
    t0 = time.time()
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    out = os.path.join(HERE, "data", "%s_%d.jsonl" % (name, seed))
    recs = []
    with Pool(nproc) as pool, open(out, "w") as f:
        for rec in pool.imap_unordered(one_run, jobs, chunksize=1):
            recs.append(rec)
            f.write(json.dumps(rec) + "\n")
            f.flush()
    S = summarise(recs)
    print(name, "seed", seed, "time %.0fs" % (time.time() - t0))
    print(json.dumps(S, indent=1))
    bad = [r for r in recs if "harness_limit" not in r and (r["det"] or r["good"])]
    for r in bad[:10]:
        print("VIOLATION", r["cell"], r["prof"], r["strat"], r["seed"], r["det"], r["good"])
