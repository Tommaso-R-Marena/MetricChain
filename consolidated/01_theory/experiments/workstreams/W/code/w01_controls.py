"""w01: binary controls of the brief, reproduced with the general code (game over Lipschitz vertices) before
anything else is believed.

  p = 0.1, u = 2 : R^max(0) = 0.048130, E = 0.212295, R^max(0.3E) = 0.023270, theta_na(0.3E) = 0.036246
  p = 1/2, u = 1 : R^max(0) = 0.029139
  two binary site types, u = 1, fields 0 and 3, half each, e = 0.3E : 0.008559 against the average 0.009791
and three controls for larger alphabets from the theory report (Theorems 11.27, 11.28):
  flat 4-state Hamming site, u = 1, zero residual: 0.02914 (boxes of pairs) against 0.02841 (dips)
  three-state site with energies (0,0,2), beta = c = 1, zero residual: 0.02903 (all vertices), 0.02467 (dips)
  the same site: thr(0) = 0.11969 < class threshold 0.11988
"""
import math
import sys
import time

import numpy as np

from wlib import *

t0 = time.time()
print("=== w01 controls ===")

# --- game value: enumeration against LP, random matrices -------------------------------------------------
rng = np.random.default_rng(1)
worst = 0.0
for q, nc in ((2, 2), (2, 5), (3, 4), (3, 6), (3, 3)):
    K = np.exp(rng.normal(size=(400, q, nc)))
    v1 = game_value_batch(K)
    v2 = np.array([game_lp(k)[0] for k in K])
    worst = max(worst, float(np.max(np.abs(v1 - v2))))
print(f"game value, enumeration against LP (2000 random matrices): max abs difference {worst:.2e}")

# --- closed binary form against the general game -----------------------------------------------------------
worst = 0.0
for p, u in ((0.1, 2.0), (0.3, 1.0), (0.5, 1.0), (0.05, 2.0), (0.2, 4.0)):
    s = binary_site(p, u)
    assert s.nv == 2
    for g in np.linspace(-u * 0.99, u * 0.99, 23):
        for t in (0.05, 0.3, 0.5, 0.8, 0.97):
            worst = max(worst, abs(s.F(np.array([0.0, g]), t) - F_binary_closed(p, u, g, t)))
print(f"binary site: general game against the cosh form of Theorem 11.59(b) (575 points): max abs difference {worst:.2e}")

# --- the brief's numbers -------------------------------------------------------------------------------------
ch = Chain([binary_site(0.1, 2.0)], [1.0])
E = ch.E()
R0, tR0 = ch.R(0.0, return_t=True)
R3, tR3 = ch.R(0.3 * E, return_t=True)
th, e_na = ch.theta_na(0.3 * E)
thd, tau = ch.theta_na_direct(0.3 * E)
print(f"p=0.1,u=2: E = {E:.6f} (brief 0.212295); R^max(0) = {R0:.6f} (0.048130) at t={tR0:.4f}, gamma*={ch.gammas(tR0)[0][1]:.4f};")
print(f"           R^max(0.3E) = {R3:.6f} (0.023270) at t={tR3:.4f}, gamma*={ch.gammas(tR3)[0][1]:.4f};"
      f" theta_na(0.3E) = {th:.6f} = {thd:.6f} (0.036246)")
# pair identity
for e in (0.0, 0.3 * E, 0.6 * E, -0.05):
    R = ch.R(e)
    print(f"           pair identity at e={e:+.5f}: R = {R:.8f}, theta_na(e + R) via max_tau = {ch.theta_na_direct(e + R)[0]:.8f}")
a, info = ch.a()
print(f"           a = theta_na(0+) = {a:.6f} (theory report table: 0.1841 at theta=2; p=0.1 is theta=2.197)")

ch = Chain([binary_site(0.5, 1.0)], [1.0])
print(f"p=1/2,u=1: R^max(0) = {ch.R(0.0):.6f} (0.029139); E = {ch.E():.6f} (ln cosh(1/2) = {math.log(math.cosh(0.5)):.6f});"
      f" a = {ch.a()[0]:.6f} (0.110944)")

p3 = 1 / (1 + math.exp(3.0))
s0, s3 = binary_site(0.5, 1.0), binary_site(p3, 1.0)
mix = Chain([s0, s3], [0.5, 0.5])
c0, c3 = Chain([s0], [1.0]), Chain([s3], [1.0])
E = mix.E()
Efd = mix.Fstar(2.5e-4) / 2.5e-4        # the reference control divides F* by the first step of a grid of 4001 values of t
for EE, lab in ((E, "E = limit"), (Efd, "E = F*(t)/t at t = 1/4000, as in the workstream-F control")):
    e = 0.3 * EE
    Rm, tm = mix.R(e, return_t=True)
    avg = 0.5 * c0.R(e) + 0.5 * c3.R(e)
    print(f"two binary types (fields 0, 3; u=1), {lab}: E = {EE:.6f}; R^max(0.3E) = {Rm:.6f} (0.008559) at t = {tm:.4f};"
          f" average of the two exponents at the same e = {avg:.6f} (0.009791)")
print(f"           thresholds: {c0.E():.6f}, {c3.E():.6f}; average {0.5*c0.E()+0.5*c3.E():.6f} = E of the mixture {E:.6f}")
print(f"           e = 0: mixture {mix.R(0.0):.6f}, average {0.5*c0.R(0.0)+0.5*c3.R(0.0):.6f}")

# --- larger alphabets: controls from Theorems 11.27 / 11.28 ---------------------------------------------------
ham = lambda q, c=1.0: c * (1 - np.eye(q))
flat4 = Site(np.ones(4) / 4, ham(4), "flat4")
print(f"flat 4-state Hamming site: {flat4.nv} vertices (expected 2^4 - 2 = 14), of which distance functions: {int(flat4.is_dist.sum())}")
zero4 = np.zeros(4)
ts = np.linspace(0, 1, 401)
Fall = np.array([flat4.F(zero4, t) for t in ts])
Fdip = np.array([flat4.F(zero4, t, cols=np.where(flat4.is_dist)[0]) for t in ts])
print(f"   zero residual, u=1, e=0: all vertices {Fall.max():.5f} (0.02914), dips only {Fdip.max():.5f} (0.02841)")
u = 1.0
D = lambda r, th_: klb(r, th_)
form = max(D(-math.log(m / 4 + (1 - m / 4) * math.exp(-u)) / u, 1 - m / 4) if -math.log(m / 4 + (1 - m / 4) * math.exp(-u)) / u < 1 - m / 4 else 0 for m in (1, 2, 3))
print(f"   closed form max_m D(rho_m || 1 - m/k): {form:.5f}")

w = np.exp(-np.array([0.0, 0.0, 2.0]))
s002 = Site(w / w.sum(), ham(3), "(0,0,2)")
zero3 = np.zeros(3)
Fall = np.array([s002.F(zero3, t) for t in ts])
Fdip = np.array([s002.F(zero3, t, cols=np.where(s002.is_dist)[0]) for t in ts])
print(f"three-state site (0,0,2), Hamming, beta=c=1: {s002.nv} vertices; zero residual, e=0: all {Fall.max():.5f} (0.02903), dips {Fdip.max():.5f} (0.02467)")
print(f"   thr(0) = {s002.thr(zero3):.5f} (0.11969); dips only {s002.thr(zero3, cols=np.where(s002.is_dist)[0]):.5f} (0.0947);"
      f" class threshold max_gamma thr = {s002.Estar():.5f} (0.11988)")
print(f"   F(0,t)/t at t=1e-4: {s002.F(zero3, 1e-4)/1e-4:.5f}")

# --- the maximised game function: variational (Renyi) form against the zoom search over gamma and against LP ---
print("F*(t) = max_gamma F(gamma,t): closed variational form [lower, upper certificate] against the zoom search and the LP at gamma*")
from wsites import path_site, tri_site, asym_site
worst_gap = worst_zoom = worst_lp = 0.0
for s in (binary_site(0.1, 2.0), binary_site(0.3, 1.0), s002, path_site(), tri_site(), asym_site()):
    for t in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95):
        r = s.renyi(t)
        vz = s.Fstar_game(t)
        vlp = -math.log(s.strategies(r["gamma"], t)[0])
        assert s.in_L(r["gamma"])
        worst_gap = max(worst_gap, r["upper"] - r["F"])
        worst_zoom = max(worst_zoom, vz - r["upper"])          # the zoom value must not exceed the upper certificate
        worst_lp = max(worst_lp, abs(vlp - r["F"]))
        if t in (0.2, 0.5, 0.8):
            print(f"   {s.name:14s} t={t:.2f}: [{r['F']:.10f}, {r['upper']:.10f}]  zoom {vz:.10f}  LP at gamma* {vlp:.10f}")
    Ed = s.Estar(full=True)
    cap = s.capacity(full=True)
    print(f"   {s.name:14s} E = [{Ed['E']:.8f}, {Ed['upper']:.8f}] (zoom over gamma: {s.Estar_game():.8f}; F*(t)/t at 1e-5: {s.Fstar(1e-5)/1e-5:.8f});"
          f" a = [{cap['a']:.8f}, {cap['upper']:.8f}] (F*(t)/(1-t) at 1-1e-5: {s.Fstar(1-1e-5)/1e-5:.8f})")
print(f"   42 points: largest certificate gap {worst_gap:.1e}; largest excess of the zoom value over the certificate {worst_zoom:.1e};"
      f" largest |LP at gamma* - value| {worst_lp:.1e}")
print(f"time {time.time()-t0:.1f} s")
