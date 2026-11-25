"""Section 6.6 (iii) / Proposition 11.81(b): "for 1 < bJ <= bJ*(e,u) the local minimum is global, so
R_H(e) = R_unif(e)".  Scan over (u, e): the largest coupling up to which r_{mu*}(e) = R_unif(e) for
the uniform cube's profile mu* = (1/2; p_u, p_u), against bJ*(e,u).  A far exit (towards a well) can
undercut the symmetric exit before the symmetric exit becomes locally unstable.
For the failing cases: the explicit exit, the best binary profile found, and the contact set."""
import time, sys
import numpy as np
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()

def consts(u, e):
    rho = (Lam1(u) + e) / u
    c2 = 1.0 / (2 * rho * (1 - rho)) - 2.0
    L = np.log((1 - rho) / rho)
    return rho, c2, L, 1.0 + u * c2 / (2 * L)

def value(bJ, u, e, N=100001):
    M = Model(bJ=bJ, bB=0.0, u=u, N=N)
    lam, mu = binary(0.5, p_u(u), p_u(u))
    return inner_clip(M, lam, mu, e + alpha(M, lam, mu))[0], M

print("#  u     e/e_c or e/E      e        bJ*     largest bJ with r_mu*(e) = R_unif(e)   ratio (bJ_eq - 1)/(bJ* - 1)   barrier there   E_unif - e")
fails = []
for u in (1.0, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0):
    Eu = float(np.log(np.cosh(u / 2)))
    ec = -float(kl(p_u(u), 0.5))
    for tag, e in (("0.9 e_c", 0.9 * ec), ("0.6 e_c", 0.6 * ec), ("0.3 e_c", 0.3 * ec), ("0", 0.0), ("0.3 E", 0.3 * Eu), ("0.6 E", 0.6 * Eu)):
        rho, c2, L, bJs = consts(u, e)
        Ru = R_unif(e, u)
        # bisection on f in (0, 1): equality holds at f -> 0 (bJ = 1)
        lo, hi = 0.0, 1.0
        v1, M1 = value(1.0 + 0.999 * (bJs - 1.0), u, e)
        if abs(v1 - Ru) < 1e-8:
            feq = 0.999
        else:
            for _ in range(12):
                mid = 0.5 * (lo + hi)
                v, _ = value(1.0 + mid * (bJs - 1.0), u, e)
                if abs(v - Ru) < 1e-8:
                    lo = mid
                else:
                    hi = mid
            feq = lo
        bJeq = 1.0 + feq * (bJs - 1.0)
        Mq = Model(bJ=bJeq, bB=0.0, u=u, N=100001)
        flag = "" if feq >= 0.999 else "   <-- (iii) fails: far exit"
        if feq < 0.999:
            fails.append((u, e, bJs, bJeq))
        print(f"  {u:4.1f}  {tag:8s}  {e:+.5f}  {bJs:.5f}  {bJeq:.5f}   {feq:.3f}   {float(Mq.I(0.5)):.4f}   {Eu - e:.4f}{flag}   t={time.time()-t0:.0f}", flush=True)
print("# failing cases in detail (coupling halfway between the last equality and bJ*)")
for (u, e, bJs, bJeq) in fails[:6]:
    bJ = 0.5 * (bJeq + bJs)
    M = Model(bJ=bJ, bB=0.0, u=u)
    lam, mu = binary(0.5, p_u(u), p_u(u))
    B = e + alpha(M, lam, mu)
    s1, arg = inner_clip(M, lam, mu, B, G=400, zooms=5, ncand=6, nz=41, rounds=8)
    s2, k2, loc = inner_dual(M, lam, mu, B, nk=801, refine=4)
    nu = np.minimum(np.maximum(mu, arg[0]), arg[1])
    lhs = u * float(lam @ np.abs(nu - mu)) + float(M.I(lam @ nu))
    Rb, lb, mb = R_binary(M, e, starts=[(0.5, p_u(u), p_u(u)), (0.5, p_u(u) * 1.3, p_u(u) * 1.3), (0.5, 0.2, 0.2), (0.45, p_u(u) * 1.2, p_u(u)), (0.5, 0.35, 0.35)])
    print(f"  u={u} e={e:+.5f} bJ={bJ:.5f} (bJ* = {bJs:.5f}): R_unif = {R_unif(e,u):.7f}; r_mu* = {s1:.7f} (S1), {s2:.7f} (S2, dual with I); cheapest exit nu = ({nu[0]:.4f}, {nu[1]:.4f}), type {float(lam@nu):.4f}, MI {MI(lam,nu):.7f}; check u*dist + I(type) = {lhs:.6f} <= e + alpha = {B:.6f}: {lhs <= B + 1e-12};")
    print(f"       contact set {[(round(a,3), round(b,3)) for a,b in M.contact()]}; (I - v)(1/2) = {float(M.I(0.5)) - float(M.v(0.5)):.2e};  best binary profile found: {Rb:.7f} [{fmt(lb, mb)}]  (R_unif - best = {R_unif(e,u) - Rb:+.2e})   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
