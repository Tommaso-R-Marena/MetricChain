#!/usr/bin/env python3
"""Check 1 of workstream W: the Renyi form of the site function against the matrix game; the tables of the worked example."""
import math, numpy as np
from scipy.optimize import minimize
from wv_lib import *
rng = np.random.default_rng(5)
print("(a) vertices of the Lipschitz polytopes:", {k: len(vertices(d)) for k, (pi, d) in SITES.items()}, " (report: 2, 4, 6, 5)")
# (b) Renyi form = max over gamma of the game value (blind search over gamma by Nelder-Mead from several starts); dual bracket
print("(b) F*(t): Renyi form [primal, dual bound] against the best game value found by a blind search over gamma")
for name in ("bin", "path", "tri", "asym"):
    pi, d = SITES[name]; V = vertices(d); q = len(pi)
    for t in (0.2, 0.46, 0.8):
        val, M, upper, Q = renyi_form(pi, V, t)
        # the hardest instance according to the report: Gibbs law = Renyi centre  ->  gamma* = -ln(Q/pi)
        gstar = -np.log(Q/np.asarray(pi)); gstar -= gstar[0]
        in_class = all(gstar[a] - gstar[b] <= d[a][b] + 1e-9 for a in range(q) for b in range(q))
        at_star, _ = F_game(pi, V, gstar, t)
        def neg(z):
            g = np.concatenate([[0.0], z])
            if any(g[a] - g[b] > d[a][b] + 1e-12 for a in range(q) for b in range(q)): return 1.0
            return -F_game(pi, V, g, t)[0]
        blind = 0
        for s in range(6):
            z0 = gstar[1:] + rng.normal(0, 0.15, q - 1) if s < 3 else rng.uniform(-0.3, 0.3, q - 1)
            res = minimize(neg, z0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 3000})
            blind = max(blind, -res.fun)
        print(f"    {name:5s} t = {t:4.2f}: Renyi {val:.9f} (dual bound {upper:.9f});  game at gamma* {at_star:.9f} (in the class: {in_class});  blind search {blind:.9f}")
# (c) the table of the worked example
print("(c) chain: E, a, h = R^max(0) [t*], R^max(0.3E), theta_na(0.3E)   -- report in brackets")
REP = {"bin": (0.103131, 0.095301, 0.025034, None, None), "path": (0.400622, 0.294791, 0.089589, 0.043375, 0.066899),
       "tri": (0.284907, 0.247541, 0.066729, 0.032077, 0.051124), "asym": (0.191059, 0.166046, 0.045407, 0.022108, 0.035544),
       "mix": (0.251877, 0.195046, 0.057275, 0.027759, 0.043288), "mix2": (0.212197, 0.186645, 0.050050, 0.024122, 0.038641)}
chains = {k: Chain([SITES[k]], [1.0]) for k in ("bin", "path", "tri", "asym")}
chains["mix"] = Chain([SITES["bin"], SITES["path"]], [0.5, 0.5])
chains["mix2"] = Chain([SITES["bin"], SITES["tri"]], [0.4, 0.6])
worst = 0
for name, ch in chains.items():
    E, a = ch.E_a(); h, ts = ch.Rmax(0.0); r3, _ = ch.Rmax(0.3*E); th3 = ch.theta_na(0.3*E)
    rep = REP[name]
    got = (E, a, h, r3, th3)
    worst = max(worst, max(abs(g - r) for g, r in zip(got, rep) if r is not None))
    print(f"    {name:5s} E = {E:.6f} [{rep[0]}], a = {a:.6f} [{rep[1]}], h = {h:.6f} [{rep[2]}] (t* = {ts:.3f}), R(0.3E) = {r3:.6f} [{rep[3]}], theta_na(0.3E) = {th3:.6f} [{rep[4]}]")
print(f"    largest deviation from the report: {worst:.1e}")
# (d) exponents do not add: mix at 0.3E, 0.5E: R^max against the average at a common accuracy
E, _ = chains["mix"].E_a()
for f in (0.3, 0.5, 0.9):
    avg = 0.5*chains["bin"].Rmax(f*E)[0] + 0.5*chains["path"].Rmax(f*E)[0]
    print(f"(d) mix at {f}E: R^max = {chains['mix'].Rmax(f*E)[0]:.6f}, average at a common accuracy = {avg:.6f}  (report: 0.027759/0.030121, 0.014126/0.020800, 0.000568/0.008322)")
# (e) pair identity theta_na(e + R(e)) = R(e)
w = 0
for name in ("path", "tri", "mix"):
    ch = chains[name]; E, _ = ch.E_a()
    for f in (0.0, 0.2, 0.5):
        R, _ = ch.Rmax(f*E); w = max(w, abs(ch.theta_na(f*E + R) - R))
print(f"(e) pair identity theta_na(e + R(e)) = R(e): largest deviation {w:.1e}")
