"""Section 6.6 (iii) / Proposition 11.81(b), careful version of the scan: for each (u, e) the value
r_{mu*}(e) of the uniform cube's profile mu* = (1/2; p_u, p_u) on a grid of couplings
bJ = 1 + f (bJ*(e,u) - 1), f in (0, 1), against R_unif(e); inner solver S1 with fine settings,
relative tolerance 1e-6; the first f at which the relative deficit exceeds the tolerance.
Then, for the failing (u, e): details at that coupling (contact set, exit, S2, best binary profile)."""
import time, sys
import numpy as np
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
fine = dict(G=300, zooms=4, ncand=5, nz=31, rounds=8)

def consts(u, e):
    rho = (Lam1(u) + e) / u
    c2 = 1.0 / (2 * rho * (1 - rho)) - 2.0
    L = np.log((1 - rho) / rho)
    return rho, c2, L, 1.0 + u * c2 / (2 * L)

fs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
print("#  u    e-tag     e        bJ*      first f with relative deficit > 1e-6 (bJ there)   max relative excess of S1 over R_unif (precision)   barrier at bJ*   E_unif - e")
fails = []
for u in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
    Eu = float(np.log(np.cosh(u / 2)))
    ec = -float(kl(p_u(u), 0.5))
    for tag, e in (("0.9 e_c", 0.9 * ec), ("0.6 e_c", 0.6 * ec), ("0.3 e_c", 0.3 * ec), ("0", 0.0), ("0.3 E", 0.3 * Eu), ("0.6 E", 0.6 * Eu), ("0.9 E", 0.9 * Eu)):
        rho, c2, L, bJs = consts(u, e)
        Ru = R_unif(e, u)
        first = None
        exc = 0.0
        for f in fs:
            bJ = 1.0 + f * (bJs - 1.0)
            M = Model(bJ=bJ, bB=0.0, u=u, N=100001)
            lam, mu = binary(0.5, p_u(u), p_u(u))
            v = inner_clip(M, lam, mu, e + alpha(M, lam, mu), **fine)[0]
            rel = (Ru - v) / Ru
            exc = max(exc, -rel)
            if rel > 1e-6 and first is None:
                first = (f, bJ, v)
        Ms = Model(bJ=bJs, bB=0.0, u=u, N=100001)
        if first is None:
            print(f"  {u:4.1f}  {tag:8s} {e:+.5f}  {bJs:8.4f}   none up to f = 0.99                      {exc:.1e}   {float(Ms.I(0.5)):.4f}  {Eu - e:.4f}   t={time.time()-t0:.0f}", flush=True)
        else:
            fails.append((u, tag, e, bJs, first))
            print(f"  {u:4.1f}  {tag:8s} {e:+.5f}  {bJs:8.4f}   f = {first[0]:.2f} (bJ = {first[1]:.4f}): r_mu* = {first[2]:.6f} < R_unif = {Ru:.6f}   {exc:.1e}   {float(Ms.I(0.5)):.4f}  {Eu - e:.4f}   <-- (iii) fails   t={time.time()-t0:.0f}", flush=True)
print("# details at the first failing coupling of the grid")
for (u, tag, e, bJs, (f, bJ, v)) in fails:
    if time.time() - t0 > 480:
        print("  (time limit)"); break
    M = Model(bJ=bJ, bB=0.0, u=u)
    lam, mu = binary(0.5, p_u(u), p_u(u))
    B = e + alpha(M, lam, mu)
    s1, arg = inner_clip(M, lam, mu, B, **fine)
    s2, k2, loc = inner_dual(M, lam, mu, B, nk=801, refine=4)
    nu = np.minimum(np.maximum(mu, arg[0]), arg[1])
    lhs = u * float(lam @ np.abs(nu - mu)) + float(M.I(lam @ nu))
    Rb, lb, mb = R_binary(M, e, starts=[(0.5, p_u(u), p_u(u)), (0.5, min(p_u(u) * 1.5, 0.45), min(p_u(u) * 1.5, 0.45)), (0.5, 0.25, 0.25), (0.45, p_u(u) * 1.2, p_u(u))], kw=fine)
    print(f"  u={u} e={e:+.5f} ({tag}) bJ={bJ:.4f} (f={f}, bJ* = {bJs:.4f}): R_unif = {R_unif(e,u):.7f}; r_mu* = {s1:.7f} (S1), {s2:.7f} (S2: dual per exit type, I); cheapest exit nu = ({nu[0]:.4f}, {nu[1]:.4f}), type {float(lam@nu):.4f}, MI {MI(lam,nu):.7f}, u*dist + I(type) = {lhs:.6f} <= e + alpha = {B:.6f}: {lhs <= B + 1e-9}")
    print(f"       contact set {[(round(a,4), round(b,4)) for a,b in M.contact()]}; (I - v)(1/2) = {float(M.I(0.5)) - float(M.v(0.5)):.3e}; wells at {M.kmin:.4f}; best binary profile found: {Rb:.7f} [{fmt(lb, mb)}]; R_unif - best = {R_unif(e,u) - Rb:+.3e}   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
