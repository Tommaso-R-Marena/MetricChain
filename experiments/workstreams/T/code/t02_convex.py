#!/usr/bin/env python3
"""t02 -- convex rate function I (one phase): Curie-Weiss with bJ <= 1 (and antiferromagnetic bJ < 0), with and without a field.
Part 1 (checks, a few parameter sets):
   (i)   the brief's cone formula R_cone(e) against the single-letter sup-min R_H(e) over binary centres;
   (ii)  the collapse  R_H(e) = max_{|gamma|<=u} R_gamma(e)  (hardest additive instance = flat-histogram instance);
   (iii) the pair identity  n_mu*(e + R_H(e)) = R_H(e)  and the truncated cone at the same accuracy.
Part 2 (table): R_H(0+), gamma*, R_0(0+), the class threshold E, a = theta_na(0+), for a grid of (bJ, bB) -- cone formulas.
usage: python3 t02_convex.py check | table u [bJ1,bJ2,...]
"""
import sys, time, math
import numpy as np
from scipy.optimize import minimize_scalar
import tlib as T

mode = sys.argv[1]
t0 = time.time()


def R_add_max(K, e, n0=9):
    """max over additive instances gamma|x|, |gamma| <= u, of the cone formula"""
    u = K.u
    f = lambda g: -T.R_cone(K, e, K.lam_additive(g))
    gs = np.linspace(-u, u, n0)
    vals = np.array([-f(g) for g in gs])
    i = int(np.argmax(vals))
    r = minimize_scalar(f, bounds=(gs[max(i - 1, 0)], gs[min(i + 1, n0 - 1)]), method="bounded", options={"xatol": 1e-7})
    if -r.fun >= vals[i]:
        return -float(r.fun), float(r.x)
    return float(vals[i]), float(gs[i])


def threshold(K, lam):
    """E = max_m { min_kappa' [ u (m(1-kappa') + (1-m)kappa') + lam(kappa') ] - Lam_m }   (cone formula: R vanishes from E on)"""
    kg = np.linspace(0.0, 1.0, 20001)
    lk = lam(kg)

    def f(m):
        val = K.u * (m * (1 - kg) + (1 - m) * kg) + lk
        return -(float(val.min()) - T.Lam_m(K, m))
    ms = np.linspace(0.03, 0.97, 32)
    vals = np.array([-f(m) for m in ms])
    i = int(np.argmax(vals))
    r = minimize_scalar(f, bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 31)]), method="bounded", options={"xatol": 1e-9})
    return max(-float(r.fun), float(vals[i]))


def a_cone(K):
    """a = theta_na(0+) = max_m MI(Gibbs shell of the cone around a centre of type m)"""
    def f(m):
        _, (n0, n1) = T.Lam_m(K, m, full=True)
        return -float(T.MI_blocks(np.array([m, 1 - m]), np.array([n0, n1])))
    ms = np.linspace(0.03, 0.97, 32)
    vals = np.array([-f(m) for m in ms])
    i = int(np.argmax(vals))
    r = minimize_scalar(f, bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 31)]), method="bounded", options={"xatol": 1e-9})
    return max(-float(r.fun), float(vals[i]))


if mode == "check":
    print("== convex I: cone formula vs single-letter sup-min; collapse to the hardest additive instance; pair identity")
    for (bJ, bB, u) in ((0.5, 0.0, 1.0), (0.5, 0.3, 1.0), (0.9, 0.2, 2.0), (-1.0, 0.3, 1.0), (1.0, 0.1, 1.0)):
        K = T.Known(T.phi_cw(bJ, bB), u)
        E = threshold(K, K.v)
        print(f"\nbJ={bJ} bB={bB} u={u}: minimum of I at {K.minima[0][0]:.5f}; contact set {[(round(a,4),round(b,4)) for a,b in K.contact_pieces()]}; E = {E:.6f}")
        for e in (0.0, 0.3 * E):
            Rc, mc = T.R_cone(K, e, K.v, full=True)
            Rs, arg = T.R_bin(K, e, K.v, nrand=2)
            Ra, gs = R_add_max(K, e)
            # the same additive instance through the sup-min
            Rgs, _ = T.R_bin(K, e, K.lam_additive(gs), nrand=2)
            R0 = T.R_cone(K, e, K.lam_zero())
            X = e + Rs
            lams, mus = T.bin_blocks(*arg)
            nmu = T.n_mu(K, lams, mus, X, K.v)
            co = T.theta_shell(K, np.array([mc, 1 - mc]), np.array([1.0, 0.0]), X)
            co0 = T.theta_shell(K, np.array([mc, 1 - mc]), np.array([1.0, 0.0]), e + R0) if e + R0 > 0 else float("nan")
            print(f"  e={e:.6f}: R_H sup-min {Rs:.8f} at (m,a,b)=({arg[0]:.4f},{arg[1]:.4f},{arg[2]:.4f}) | cone formula {Rc:.8f} (m={mc:.4f}) [diff {Rs-Rc:+.1e}]"
                  f" | max_gamma R_gamma {Ra:.8f} at gamma*={gs:+.4f} [diff {Ra-Rs:+.1e}; sup-min at gamma*: {Rgs:.8f}] | R_0 {R0:.8f}")
            print(f"        pair identity at X = e + R_H = {X:.6f}: n_mu* = {nmu:.8f} [diff {nmu-Rs:+.1e}], truncated cone (m={mc:.3f}) = {co:.8f} [diff {co-Rs:+.1e}];"
                  f"  with R_0 in its place: theta_na(e + R_0) = {co0:.8f} against R_0 = {R0:.8f}   [{time.time()-t0:.0f}s]", flush=True)
else:
    u = float(sys.argv[2])
    pu = 1 / (1 + math.exp(u))
    Lam1 = math.log(2 / (1 + math.exp(-u)))
    print(f"== Curie-Weiss, one phase, u = {u}.  Uniform cube: R(0+) = {T.kl1(Lam1/u, 0.5):.6f}, a = {T.kl1(pu, 0.5):.6f}, E = {math.log(math.cosh(u/2)):.6f}")
    print("   bJ     bB    kappa_0   R_H(0+)    gamma*    R_0(0+)    E_H       E_0       a=theta_na(0+)   [s]")
    bJs = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else (-2.0, -1.0, 0.0, 0.5, 0.9, 1.0)
    for bJ in bJs:
        for bB in (0.0, 0.1, 0.3, 0.6):
            K = T.Known(T.phi_cw(bJ, bB), u)
            Ra, gs = R_add_max(K, 0.0)
            RH = T.R_cone(K, 0.0, K.v)
            R0 = T.R_cone(K, 0.0, K.lam_zero())
            EH = threshold(K, K.v)
            E0 = threshold(K, K.lam_zero())
            a = a_cone(K)
            print(f"  {bJ:+.2f}  {bB:.2f}   {K.minima[0][0]:.4f}   {RH:.6f}   {gs:+.4f}   {R0:.6f}   {EH:.6f}  {E0:.6f}  {a:.6f}     [{time.time()-t0:.0f}s]  (max_gamma R_gamma - R_H = {Ra-RH:+.1e})", flush=True)
print(f"time {time.time()-t0:.0f}s")
