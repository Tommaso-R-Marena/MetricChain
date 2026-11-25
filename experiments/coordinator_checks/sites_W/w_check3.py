#!/usr/bin/env python3
"""Check 3 (coordinator; q = 6 was dropped: 62 vertices are too slow for this implementation): uniform q-letter sites with the Hamming envelope, all vertices of the Lipschitz polytope (boxes) --
against the two families one can write in closed form: single dips on k equally weighted groups of letters (k divides q),
    R_k(0) = max_t [t Psi_k(u) - Psi_k(tu)],  Psi_k(s) = ln((e^s + k - 1)/k) - s/k,   a_k = I_k(u),   E_k = Psi_k(u).
Question: is h(uniform q letters) = max over divisors k of q of R_k(0)?  (q = 4: k = 2 or 4;  q = 6: k = 2, 3, 6.)"""
import math, numpy as np
from wv_lib import *
Psi = lambda k, s: math.log((math.exp(s) + k - 1)/k) - s/k
def R_k(k, u):
    ts = np.linspace(0, 1, 400001); return float((ts*Psi(k, u) - np.log((np.exp(ts*u) + k - 1)/k) + ts*u/k).max())
def I_k(k, s):
    p = math.exp(s)/(math.exp(s) + k - 1); return math.log(k) + p*math.log(p) + (1-p)*math.log((1-p)/(k-1))
for q, divs in ((3, (3,)), (4, (2, 4))):
    V = vertices(hamming(q, 1.0))
    print(f"q = {q}: {len(V)} vertices (2^q - 2 = {2**q - 2})")
    for u in ((0.5, 1.0, 2.0, 3.0) if q < 6 else (0.5, 1.0, 2.0)):
        ch = Chain([([1.0/q]*q, hamming(q, u))], [1.0])
        E, a = ch.E_a(); h, t = ch.Rmax(0.0, grid=60)
        print(f"   u = {u}: h = {h:.6f} [groups: " + ", ".join(f"k={k}: {R_k(k, u):.6f}" for k in divs) + f"];  a = {a:.6f} [" + ", ".join(f"{I_k(k, u):.6f}" for k in divs)
              + f"];  E = {E:.6f} [" + ", ".join(f"{Psi(k, u):.6f}" for k in divs) + "]")
