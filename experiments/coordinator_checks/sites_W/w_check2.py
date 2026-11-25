#!/usr/bin/env python3
"""Check 2 of workstream W: the negative results, and the small-slope regime the workstream did not scan.

(a) "a field always helps" fails for three states near the threshold (Hamming, u = 1): E(uniform) = 0.119499 < E(0.05, 0.5, 0.45) = 0.120196;
    two-state cube: ln cosh(1/2) = 0.120115.
(b) F* of the triangle site is not concave: second differences near the label switch t_c = 0.378; corner of R^max at 0.1996 E.
(c) small slopes (coordinator; theory report 11.25, remark): for the Hamming envelope on three letters the uniform law is NOT the hardest
    for h = R^max(0) when u < ln 2, nor for a when u < 0.5194: site laws close to (1/2, 1/2, 0) are harder.
(d) the uniform k-ary Hamming site in closed form: F*(t) = t Psi_k(u) - Psi_k(tu), E = Psi_k(u), a = I_k(u)."""
import math, numpy as np
from wv_lib import *
def site_numbers(pi, u, q=3):
    ch = Chain([(list(pi), hamming(q, u))], [1.0])
    E, a = ch.E_a(); h, t = ch.Rmax(0.0)
    return E, a, h, ch
print("(a) Hamming, u = 1:  E, a, h")
for pi in ([1/3, 1/3, 1/3], [0.05, 0.5, 0.45], [0.02, 0.49, 0.49], [0.001, 0.4995, 0.4995]):
    E, a, h, _ = site_numbers(pi, 1.0)
    print(f"    pi = {np.round(pi, 4)}:  E = {E:.6f}, a = {a:.6f}, h = {h:.6f}")
print(f"    two-state cube: E = ln cosh(1/2) = {math.log(math.cosh(0.5)):.6f}, a = {math.log(2) + (lambda p: p*math.log(p) + (1-p)*math.log(1-p))(1/(1+math.e)):.6f}, h = 0.029139")
print("(b) triangle site: second differences of F* (grid 0.002) near the label switch, and the slope of R^max")
tri = Chain([SITES["tri"]], [1.0]); E, a = tri.E_a()
ts = np.arange(0.36, 0.3961, 0.002); F = np.array([tri.Fstar(t) for t in ts])
d2 = np.diff(F, 2)/0.002**2
print("    t:", " ".join(f"{t:.3f}" for t in ts[1:-1])); print("    F'':", " ".join(f"{x:+.3f}" for x in d2))
print(f"    largest second difference {d2.max():+.4f} (positive = not concave);  elsewhere (t = 0.2, 0.6): {np.diff([tri.Fstar(t) for t in (0.198, 0.2, 0.202)], 2)[0]/4e-6:+.3f}, {np.diff([tri.Fstar(t) for t in (0.598, 0.6, 0.602)], 2)[0]/4e-6:+.3f}")
for f in (0.19, 0.1996, 0.21):
    t1 = tri.Rmax(f*E)[1]
    print(f"    e = {f} E: maximiser t* = {t1:.4f} (the slope of R^max is -t*)")
print("(c) small slopes, three letters, Hamming:  u;  h and a for the uniform law, for (0.02, 0.49, 0.49), and the exact two-letter values")
Psi = lambda k, s: math.log((math.exp(s) + k - 1)/k) - s/k
def R_k(k, u):
    ts = np.linspace(0, 1, 200001); return float((ts*Psi(k, u) - np.log((np.exp(ts*u) + k - 1)/k) + ts*u/k).max())
def I_k(k, s):
    p = math.exp(s)/(math.exp(s) + k - 1); return math.log(k) + p*math.log(p) + (1-p)*math.log((1-p)/(k-1))
for u in (0.3, 0.5, 0.6, 0.8, 1.0):
    Eu, au, hu, _ = site_numbers([1/3, 1/3, 1/3], u)
    En, an, hn, _ = site_numbers([0.02, 0.49, 0.49], u)
    print(f"    u = {u}: uniform h = {hu:.6f} (closed form {R_k(3, u):.6f}), a = {au:.6f} ({I_k(3, u):.6f});  near two letters h = {hn:.6f}, a = {an:.6f};  two letters exactly h = {R_k(2, u):.6f}, a = {I_k(2, u):.6f}")
print("(d) uniform k-ary Hamming site, u = 1: E = Psi_k(u):", ", ".join(f"k={k}: {Psi(k, 1.0):.6f}" for k in (2, 3, 4)), ";  report: 0.120115 (k = 2), 0.119499 (k = 3), 0.11969 (k = 4)")
