"""Selected self-similar profile of the level recursion (coordinator's heuristic).
ODE  zeta f'^2/2 + zeta f' + (zeta - 2) f = 0;  folded saddle at (3, 3/2), slope -1.
Minus branch for zeta < 3 (f' = -1 - sqrt(Delta)), plus branch for zeta > 3.  f0 = f(0)."""
import math
from mpmath import mp, mpf, sqrt, odefun

mp.dps = 30

def disc(z, f):
    return 1 - 2 * (z - 2) * f / z

def rhs_minus(z, f):
    d = disc(z, f)
    if d < 0:
        d = mpf(0)
    return -1 - sqrt(d)

def rhs_plus(z, f):
    d = disc(z, f)
    if d < 0:
        d = mpf(0)
    return -1 + sqrt(d)

def rk4(rhs, z0, f0, z1, n):
    hstep = (z1 - z0) / n
    z, f = z0, f0
    out = [(z, f)]
    for _ in range(n):
        k1 = rhs(z, f)
        k2 = rhs(z + hstep / 2, f + hstep * k1 / 2)
        k3 = rhs(z + hstep / 2, f + hstep * k2 / 2)
        k4 = rhs(z + hstep, f + hstep * k3)
        f = f + hstep * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        z = z + hstep
        out.append((z, f))
    return out

for eps in [mpf('1e-2'), mpf('1e-3'), mpf('1e-4')]:
    # local expansion at the folded saddle: y = -s + s^2/3 + O(s^3)
    s = -eps
    zstart = 3 + s
    fstart = mpf(3) / 2 - s + s * s / 3
    # backward on the minus branch to zeta = tiny; use variable zeta = x^2 near zero to tame the sqrt singularity
    # integrate in x = sqrt(zeta): df/dx = 2 x f'(zeta)
    def rhs_x(x, f):
        z = x * x
        # 2x * (-1 - sqrt(1 - 2 (z-2) f / z)) = -2x - 2 sqrt(x^2 - 2 (z - 2) f)
        d = x * x - 2 * (z - 2) * f
        if d < 0:
            d = mpf(0)
        return -2 * x - 2 * sqrt(d)
    traj = rk4(rhs_x, sqrt(zstart), fstart, mpf(0), 20000)
    f0 = traj[-1][1]
    # forward on the plus branch
    s = eps
    trajp = rk4(rhs_plus, 3 + s, mpf(3) / 2 - s + s * s / 3, mpf(60), 60000)
    mind = min(disc(z, f) for z, f in trajp)
    print("eps", eps, "f0 =", mp.nstr(f0, 12), " f(60) =", mp.nstr(trajp[-1][1], 6), " min disc on plus branch", mp.nstr(mind, 6),
          " f(2)=", mp.nstr([f for z, f in traj if abs(z*z - 2) < 2e-3][0], 8))
