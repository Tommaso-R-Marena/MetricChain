"""Cross-check of flat_cost_bounded.flat_two_level (closed-form trajectory at the flat instance) against the simulated
outer loop of sim_outer_loop (mode 2 = value at the bottom) with identical parameters: closing level, radius, sample size."""
import math, numpy as np
import flat_cost_bounded as fc
import sim_outer_loop as so
from klib import consts

ok = True
for (u, n_o, n_i, b, lam, eta, etap, theta) in ((2.0, 24, 6, 0.5, 0.2, 0.25, 0.05, 0.05), (1.0, 30, 10, 0.5, 0.25, 0.25, 0.1, 0.1),
                                              (2.0, 36, 4, 1.0, 0.5, 0.5, 0.5, 0.5), (0.5, 40, 8, 0.27, 0.23, 0.25, 0.1, 0.02), (1.0, 34, 6, 0.31, 0.17, 0.1, 0.05, 0.03)):
    n = n_o + n_i
    pu, lam1, estar, a, h = consts(u)
    rates = [estar * f for f in (1.0, 0.5, 0.2, 0.1)]
    xs = [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    phi = (n_o + 0.5) / n
    lcost, width, info = fc.flat_two_level(n, u, phi, b=b, lam=lam, eta=eta, etap=etap, theta=theta, rates=rates)
    assert info["n_o"] == n_o
    P = so.Params(n, n_o, u, lam, eta, etap, theta, b, xs, delta=0.05)
    vals = np.array([1.0]); probs = np.array([1.0])
    s0 = math.exp(-u * n); ell_ref = ((1 + math.exp(-u)) / 2) ** n
    rng = np.random.default_rng(0)
    run = so.run_2L(rng, vals, probs, s0, ell_ref, P, mode=2)
    if "error" in run:
        print("simulation:", run); ok = False; continue
    last = run["last"]
    j_sim = len(run["levels"])
    same = (P.K == info["K"] and j_sim == info["level"] and last["r"] == info["r"] and abs(math.log(last["M"]) - info["lM"]) < 1e-9
            and abs(math.log(run["upper"] / run["lower"]) - 0) < width + 1e-9 and P.rdag == info["rdag"])
    npop = sum(1 for lv in run["levels"] if lv["populated"]); nneg = j_sim - npop
    print(f"u={u} n_o={n_o} n_i={n_i}: K {P.K}/{info['K']}  closing level {j_sim}/{info['level']}  r {last['r']}/{info['r']}  M {last['M']}/{math.exp(info['lM']):.0f}"
          f"  r_dag {P.rdag}/{info['rdag']}  pop/neg {npop}/{nneg} vs {info['npop']}/{info['nneg']}  width {math.log(run['upper']/run['lower']):.3f} <= {width:.3f}   same: {same}")
    ok = ok and same and npop == info["npop"] and nneg == info["nneg"]
# cases in which levels are left as NEGLIGIBLE (nu1 = 1, eta' = 1, theta between Gt(r1 - 1) and Gt(r1), as in part (iii) of the suite)
for (u, n_o, n_i, b, lam, eta, shift) in ((2.0, 40, 2, 0.5, 0.47, 0.5, 0), (2.0, 36, 6, 0.27, 0.9, 0.5, 0), (1.5, 44, 2, 0.9, 0.31, 0.5, 0),
                                             (2.0, 40, 2, 0.5, 0.31, 0.5, 2), (1.5, 44, 2, 0.4, 0.23, 0.5, 2), (2.0, 36, 2, 0.3, 0.17, 0.5, 2)):
    n = n_o + n_i
    pu, lam1, estar, a, h = consts(u)
    etap = 1.0
    J_ = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
    nu0_ = (J_ + 1) * math.expm1(lam) / (1 - eta)
    tab_ = so.Tables(n_o, u, eta)
    r1 = tab_.radius(1 / ((1 - eta) * nu0_ * 3.0))
    target = math.sqrt(tab_.Gt[r1 - 1 - shift] * tab_.Gt[r1 - shift])
    theta = target / ((J_ + 1) * math.expm1(lam) / etap)
    rates = [estar * f for f in (1.0, 0.5)]
    xs = [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    phi = (n_o + 0.5) / n
    lcost, width, info = fc.flat_two_level(n, u, phi, b=b, lam=lam, eta=eta, etap=etap, theta=theta, rates=rates, nu1=1.0)
    P = so.Params(n, n_o, u, lam, eta, etap, theta, b, xs, delta=0.05, nu1=1.0)
    vals = np.array([1.0]); probs = np.array([1.0])
    s0 = math.exp(-u * n); ell_ref = ((1 + math.exp(-u)) / 2) ** n
    run = so.run_2L(np.random.default_rng(0), vals, probs, s0, ell_ref, P, mode=2)
    if "error" in run:
        print("simulation:", run); ok = False; continue
    last = run["last"]; j_sim = len(run["levels"])
    npop = sum(1 for lv in run["levels"] if lv["populated"]); nneg = j_sim - npop
    same = (P.K == info["K"] and j_sim == info["level"] and last["r"] == info["r"] and abs(math.log(last["M"]) - info["lM"]) < 1e-9
            and P.rdag == info["rdag"] and npop == info["npop"] and nneg == info["nneg"])
    print(f"u={u} n_o={n_o} n_i={n_i} (nu1 = 1): K {P.K}/{info['K']}  closing level {j_sim}/{info['level']}  r {last['r']}/{info['r']}  M {last['M']}/{math.exp(info['lM']):.0f}"
          f"  r_dag {P.rdag}/{info['rdag']}  pop/neg {npop}/{nneg} vs {info['npop']}/{info['nneg']}   same: {same}")
    ok = ok and same
print("closed-form flat trajectory agrees with the simulated outer loop:", ok)
