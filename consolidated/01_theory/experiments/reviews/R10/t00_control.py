"""controls: uniform cube; binary barrier shell at bJ=1.5; free-block profile; three inner solvers."""
import time, sys
import numpy as np
from r10lib import *
t0 = time.time()
u = 1.0
# 1. uniform cube
M0 = Model(bJ=0.0, bB=0.0, u=u)
lam, mu = binary(0.5, p_u(u), p_u(u))
for e in (0.0, 0.02, -0.03):
    B = e + alpha(M0, lam, mu)
    v1 = inner_clip(M0, lam, mu, B)[0]
    v2 = inner_dual(M0, lam, mu, B, nk=801)[0]
    v3 = inner_primal(M0, lam, mu, B, nstart=30)[0]
    print(f"unif cube e={e:+.3f}: S1 {v1:.10f}  S2 {v2:.10f}  S3 {v3:.10f}  closed form {R_unif(e,u):.10f}")
# 2. CW two phases
M = Model(bJ=1.5, bB=0.0, u=u)
print("c0 =", M.c0, " kmin =", M.kmin, " I(1/2) =", float(M.I(0.5)), " contact:", M.contact())
x = 0.29803
lam, mu = binary(0.5, x, x)
B = alpha(M, lam, mu)
v1, arg = inner_clip(M, lam, mu, B)
v2, k2, loc = inner_dual(M, lam, mu, B)
v3, nu3 = inner_primal(M, lam, mu, B, nstart=60)
print(f"bJ=1.5 binary x={x}: S1 {v1:.10f} {arg}  S2 {v2:.10f} at kp={k2:.5f} loc={loc}  S3 {v3:.10f} nu={nu3}")
# 3. free block
for (e, lf, xx, ref) in ((0.02, 0.141, 0.2774, 0.0161548), (0.0, 0.14, 0.2715, None)):
    lam = np.array([(1 - lf) / 2, lf, (1 - lf) / 2]); mu = np.array([1 - xx, 0.5, xx])
    B = e + alpha(M, lam, mu)
    v1, arg = inner_clip(M, lam, mu, B)
    v2, k2, loc = inner_dual(M, lam, mu, B)
    v3, nu3 = inner_primal(M, lam, mu, B, nstart=60)
    print(f"S3 profile e={e} lf={lf} x={xx}: S1 {v1:.10f}  S2 {v2:.10f} loc={loc}  S3 {v3:.10f}   (report: {ref})")
print("time", time.time() - t0)
