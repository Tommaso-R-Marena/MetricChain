#!/usr/bin/env python3
"""R3 — check of the two intermediate inequalities of R5(2) in a regime where gamma < 1:
   Z(flat^C) <= |C| Z(flat),   Z(cone^C) >= |C| Z(cone) (1 - gamma),
   gamma = (|C|-1)/2 * cosh(u/2)^(-d_min),   hence drop_C >= D_R + ln(1 - gamma).
Extended Golay code (n = 24, |C| = 4096, d_min = 8), exact on cosets."""
import math
import numpy as np
from r3_codes import golay24
from r3_thm2 import coset_distance_table
from r3_extensions import single_cone_drop

G = golay24(); n = 24
reps, counts, free, piv, words = coset_distance_table(G, n)
dC = np.argmax(counts > 0, axis=1); size = len(words); dmin = 8
for u in (3.0, 4.0, 5.0, 6.0):
    gamma = 0.5 * (size - 1) * math.cosh(u / 2) ** (-dmin)
    Zc1 = (1 + math.exp(-u)) ** n
    ZcC = size * float(np.sum(np.exp(-u * dC)))
    line = f"u={u}: gamma = {gamma:.4f}; Z(cone^C)/(|C| Z(cone)) = {ZcC / (size * Zc1):.6f} >= 1-gamma = {1 - gamma:.6f}: {ZcC >= size * Zc1 * (1 - gamma)}"
    ok = True
    for R in range(1, 6):
        ZfC = size * float(np.sum(np.exp(-u * np.maximum(dC, R))))
        Zf1 = sum(math.comb(n, j) * math.exp(-u * max(j, R)) for j in range(n + 1))
        DR = single_cone_drop(n, u, R)
        drop = math.log(ZcC / ZfC)
        a = ZfC <= size * Zf1 * (1 + 1e-12)
        b = (gamma >= 1) or (drop >= DR + math.log(1 - gamma) - 1e-12)
        ok &= a and b
        line += f"; R={R}: drop_C - D_R = {drop - DR:+.4f}"
    print(line + f"; ln(1-gamma) = {math.log(1 - gamma) if gamma < 1 else float('nan'):+.4f}; all inequalities: {ok}")
