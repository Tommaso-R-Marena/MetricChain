#!/usr/bin/env python3
"""t18 -- (i) antiferromagnets without a field: R_H(0) by the cone formula (and per centre type) and by the symmetric
sup-min, against the uniform cube;  (ii) the value u_top below which the top of the barrier leaves the contact set
(largest chord slope from the top) for bJ = 1.5.   usage: python3 t18_antiferro.py"""
import numpy as np
import tlib as T
u = 1.0
for bJ in (-1.0, -2.0, -8.0, -40.0):
    K = T.Known(T.phi_cw(bJ, 0.0), u)
    Rc, mc = T.R_cone(K, 0.0, K.v, full=True)
    vals = [(m, T.V_bin(K, m, 0.0, 0.0, T.Lam_m(K, m), K.v)) for m in (0.3, 0.4, 0.45, 0.5)]
    rs = T.R_sym(K, 0.0, K.v, kinds=("S2",))
    print(f"bJ={bJ}: contact set {[(round(a,3),round(b,3)) for a,b in K.contact_pieces()]}; cone formula R(0) = {Rc:.7f} at m = {mc:.4f};"
          f" by centre type {[(m, round(v, 7)) for m, v in vals]}; symmetric sup-min {rs['S2'][0]:.7f}")
K = T.Known(T.phi_cw(1.5, 0.0), 1.0)
k, I = K.grid, K.Ig
sel = (k > 0.001) & (k < 0.499)
ch = (float(K.I(0.5)) - I[sel]) / (0.5 - k[sel])
i = int(np.argmax(ch))
dI = np.gradient(I, k)
print(f"bJ=1.5: largest chord slope from the top of the barrier u_top = {ch[i]:.5f} (chord to kappa = {k[sel][i]:.4f});"
      f" largest slope of I on the barrier {dI[(k>0.0707)&(k<0.5)].max():.5f}; mean slope to the well {float(K.I(0.5))/(0.5-0.07072):.5f}")
for uu in (0.27, 0.28, 0.2843, 0.29, 0.30):
    Ku = T.Known(T.phi_cw(1.5, 0.0), uu, N=200001)
    print(f"   u = {uu}: contact set {[(round(a,4),round(b,4)) for a,b in Ku.contact_pieces()]}")
