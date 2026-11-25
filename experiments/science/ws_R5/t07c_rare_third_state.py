"""t07c_rare_third_state.py -- three letters, Hamming envelope, u = 0.5: site laws with a RARE third state against the
two-letter cube and the uniform three-letter site, for h, a and E (precise values; the grid of t07 found the grid maxima
of all three at (0.05, 0.5, 0.45))."""
import numpy as np
from r5lib import *
from t04_beyond_two_letters import hamming, h_k, a_k, E_k

u = 0.5
print(f"u = {u}: two-letter cube h_2 = {h_k(2,u):.9f}, a_2 = {a_k(2,u):.9f}, E_2 = {E_k(2,u):.9f};"
      f"  uniform three letters h_3 = {h_k(3,u):.9f}, a_3 = {a_k(3,u):.9f}, E_3 = {E_k(3,u):.9f}")
for pi in ([0.05, 0.5, 0.45], [0.05, 0.475, 0.475], [0.02, 0.49, 0.49], [0.1, 0.45, 0.45], [0.1, 0.5, 0.4], [0.15, 0.45, 0.40],
           [0.001, 0.4995, 0.4995]):
    s = Site(pi, hamming(3, u))
    h, t = Rhat(lambda x: Fstar_site(s, x), 0.0, ngrid=200)
    gap = Fstar_gap(s, t)
    a = capacity_a(s)
    E = threshold_E(s)
    print(f"  pi = {pi}: h = {h:.9f} (t* = {t:.4f}, duality gap {gap:.0e}; h - h_2 = {h - h_k(2,u):+.2e}),"
          f" a in [{a[0]:.9f}, {a[1]:.9f}] (a - a_2 = {a[0] - a_k(2,u):+.2e}), E in [{E[0]:.9f}, {E[1]:.9f}] (E - E_2 = {E[0] - E_k(2,u):+.2e})")
