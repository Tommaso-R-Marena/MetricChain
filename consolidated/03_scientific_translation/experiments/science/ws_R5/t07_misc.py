"""t07_misc.py -- (i) which site law is hardest: grid of 171 laws (multiples of 1/20), three letters, Hamming, u = 1 and 0.5;
(ii) two-letter asymmetric envelope = symmetric + tilted law (Proposition 11.102); (iii) zero residual against the hardest
instance for the asymmetric three-state site; (iv) the every-n bound of Theorem 11.101(a) at n = 480 on 'mix'."""
import time, sys
import numpy as np
from r5lib import *
from t01_identity import sites_example
from t02_reference_numbers import F0_chain
from t04_beyond_two_letters import hamming, h_k, a_k, E_k

t0 = time.time()
S = sites_example()
print("== (ii) two letters: asymmetric envelope (u1,u2) = symmetric u=(u1+u2)/2 with the site law tilted by kappa=(u2-u1)/2 ==")
worst = 0
rng = np.random.default_rng(3)
for rep in range(6):
    p = rng.uniform(0.1, 0.9); u1, u2 = rng.uniform(0.0, 2.5, size=2)
    if rep == 0: u2 = 0.0                  # one-sided information
    s_as = Site([1 - p, p], [[0, u1], [u2, 0]])
    u, kap = (u1 + u2) / 2, (u2 - u1) / 2
    w = np.array([1 - p, p * np.exp(-kap)]); w /= w.sum()
    s_sy = Site(w, [[0, u], [u, 0]])
    worst = max(worst, max(abs(Fstar_site(s_as, t) - Fstar_site(s_sy, t)) for t in np.linspace(0.05, 0.95, 19)))
    worst = max(worst, abs(threshold_E(s_as)[0] - threshold_E(s_sy)[0]), abs(capacity_a(s_as)[0] - capacity_a(s_sy)[0]))
print(f"   6 random sites (one with u2 = 0): max |F*, E, a (asymmetric) - (symmetric, tilted)| = {worst:.1e}")
print()
print("== (iii) asymmetric three-state site: zero residual against the hardest instance ==")
ch = Chain([(1.0, S["asym"])])
E = ch.E()
for fr in (0.0, 0.3, 0.7, 0.9):
    R = Rhat(ch.Fstar, fr * E)[0]
    R0 = Rhat(lambda t: F0_chain(ch, t), fr * E, ngrid=300)[0]
    print(f"   e = {fr}E: R^ = {R:.6f}, R_0 = {R0:.6f}, ratio {R0/R:.3f}")
ts = np.linspace(1e-4, 1e-2, 5)
print(f"   threshold of the zero residual: F(0,t)/t at t = 1e-4: {F0_chain(ch, 1e-4)/1e-4:.6f}   [theirs 0.155521; E = {E:.6f}]")
print()
print("== (iv) Theorem 11.101(a) at n = 480 on 'mix', accuracy eps = 0.3 E n + 1 ==")
mix = Chain([(0.5, S["bin"]), (0.5, S["path"])])
E = mix.E(); n = 480; eps = 0.3 * E * n + 1
val, t = Rhat(mix.Fstar, eps / n)
print(f"   eps = {eps:.2f}; max_t [n F*(t) - t eps] = {n*val:.4f} at t = {t:.4f}: every algorithm needs >= (1-2delta) * {np.exp(n*val):.3e}"
      f" evaluations at the hardest additive instance  [theirs, from exact joint-type sums, NOT replicated: (1-2delta) * 1.9e6]")
print()
print("== (i) three letters, Hamming: grid of 171 site laws (multiples of 1/20) ==")
for u in (1.0, 0.5):
    uni = Site([1/3, 1/3, 1/3], hamming(3, u))
    hu = Rhat(lambda t: Fstar_site(uni, t), 0.0, ngrid=120)[0]
    au = capacity_a(uni)[0]; Eu = threshold_E(uni)[0]
    best = dict(h=(-1, None), a=(-1, None), E=(-1, None))
    cnt = 0
    for i in range(1, 19):
        for j in range(1, 20 - i):
            k = 20 - i - j
            pi = np.array([i, j, k]) / 20.0
            s = Site(pi, hamming(3, u))
            hh = Rhat(lambda t: Fstar_site(s, t), 0.0, ngrid=40)[0]
            aa = capacity_a(s)[0]; EE = threshold_E(s)[0]
            cnt += 1
            if hh > best["h"][0]: best["h"] = (hh, pi)
            if aa > best["a"][0]: best["a"] = (aa, pi)
            if EE > best["E"][0]: best["E"] = (EE, pi)
    print(f"   u = {u}: {cnt} laws.  uniform: h = {hu:.6f}, a = {au:.6f}, E = {Eu:.6f};  two-letter cube: h_2 = {h_k(2,u):.6f}, a_2 = {a_k(2,u):.6f}, E_2 = {E_k(2,u):.6f}")
    for key, uv in (("h", hu), ("a", au), ("E", Eu)):
        print(f"        grid maximum of {key}: {best[key][0]:.6f} at pi = {best[key][1]}  ->  {'uniform law is harder' if uv >= best[key][0] else 'a grid law is HARDER than the uniform law'}")
    print(f"   [{time.time()-t0:.0f} s]")
