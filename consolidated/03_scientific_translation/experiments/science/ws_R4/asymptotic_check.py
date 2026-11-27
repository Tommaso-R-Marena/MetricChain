#!/usr/bin/env python3
"""R4 (SCI-REV-0003) -- does the asymptotic formula of Theorem 11.86 describe the exact twins?

For u, phi1 and budgets theta: exact n^{-1}[ln A(F_D) - ln A(F_S)] at several n against the
claimed lower bound gamma = min{Xi(theta,phi1), phi2 k(y1)} (phi2 f(y1) = theta), and the
location of the heaviest type of F_D (claimed: (p_u, p_u) up to the symmetry d <-> n_j - d).
Also the single-type bound actually used in the proof: ln mass_D(x0, y0),
(x0, y0) = (ceil(p_u n1)+1, ceil(p_u n2)+1).

Own code (twins_exact.Twins, exponents.Cube); written before reading the authors' code.
"""
import math
import sys
import numpy as np
from twins_exact import Twins
from exponents import Cube, f, finv


def main():
    u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    phi1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
    ns = [int(x) for x in sys.argv[3:]] if len(sys.argv) > 3 else [800, 3200]
    C = Cube(u)
    phi2 = 1 - phi1
    print(f"# u={u} phi1={phi1}  a={C.a:.6f} h={C.h:.6f}  phi2*a={phi2*C.a:.6f}  p_u={C.pu:.5f}")
    thetas = [0.75 * C.h, C.h, 1.15 * C.h, 1.25 * C.h, 1.33 * C.h, 1.40 * C.h]
    print("# theta   theta/h  Xi        phi2*k(y1)  gamma+    | n: exact gap/n, lnA_S/n, lnA_D/n, "
          "single-type bound/n, argmax type of F_D as (d1/n1, d2/n2)")
    for th in thetas:
        if th >= phi2 * C.a:
            continue
        Xi = C.Xi(th, phi1)[0]
        y1 = float(finv(th / phi2))
        ky1 = float(C.k(y1))
        gam = max(min(Xi, phi2 * ky1), 0.0)
        row = f"{th:.5f}  {th/C.h:.3f}   {Xi:+.5f}  {phi2*ky1:.5f}    {gam:.5f}   |"
        for n in ns:
            n1 = int(math.floor(phi1 * n))
            n2 = n - n1
            tw = Twins(n1, n2, u, n * th)
            if not tw.ok:
                row += f" n={n}: W empty |"
                continue
            mass = tw.lp - tw.FD
            i, j = np.unravel_index(int(np.argmax(mass)), mass.shape)
            x0 = int(math.ceil(C.pu * n1)) + 1
            y0 = int(math.ceil(C.pu * n2)) + 1
            single = float(mass[x0, y0])
            row += (f" n={n}: {tw.gap/n:+.5f}, {tw.lnA_S/n:.5f}, {tw.lnA_D/n:.5f}, {single/n:+.5f}, "
                    f"({min(i, n1-i)/n1:.3f},{min(j, n2-j)/n2:.3f}) |")
        print(row)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
