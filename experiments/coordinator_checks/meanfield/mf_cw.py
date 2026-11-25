#!/usr/bin/env python3
"""Curie-Weiss known part: phi(kappa) = -(bJ/2) mu^2 - bB mu, mu = 2 kappa - 1.  Type-level exponents and the pair
identity theta_na(e + R(e)) = R(e) for R = R_H (flat-histogram reference, formula version)."""
import numpy as np, sys, time
from mf_lib import Model, hb

def run(bJ, bB, u, G=501):
    phi = lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - bB * (2 * k - 1)
    M = Model(phi, u, G=G)
    flat = np.abs(M.vk - M.Ik) < 1e-12
    win = M.kap[flat]
    # connected pieces of the flat window
    idx = np.nonzero(flat)[0]
    pieces = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
    desc = ", ".join(f"[{M.kap[q[0]]:.3f}, {M.kap[q[-1]]:.3f}]" for q in pieces)
    minima = M.kap[np.nonzero((M.Ik[1:-1] < M.Ik[:-2]) & (M.Ik[1:-1] <= M.Ik[2:]))[0] + 1]
    print(f"\n== bJ = {bJ}, bB = {bB}, u = {u}:  minima of I at kappa = {np.round(minima, 3)};  I(1/2) = {M.I(0.5):.4f};  flat window (v = I): {desc}")
    ms = np.linspace(0.02, 0.98, 49)
    # thresholds: E = accuracy at which R_H vanishes; a = theta_na(0+)
    a_na, m_a = M.theta_na(1e-6, ms)
    es = np.linspace(-0.6 * a_na, 0.4, 60)
    RH0, _ = M.R_formula(0.0, ms, "v")
    print(f"   a = theta_na(0+) = {a_na:.5f} (m = {m_a:.2f});  h = R_H(0) = {RH0:.5f};  R_0(0) = {M.R_formula(0.0, ms, '0')[0]:.5f}")
    print("        e       R_H(e)    R_0(e)   theta_na(e+R_H)   identity gap   theta_na(e + R_0) - R_0")
    for e in (-0.5 * RH0, -0.2 * RH0, 0.0, 0.01, 0.03, 0.06):
        RH, mH = M.R_formula(e, ms, "v")
        R0, m0 = M.R_formula(e, ms, "0")
        if not np.isfinite(RH) or RH <= 0:
            continue
        na, mn = M.theta_na(e + RH, ms)
        na0, _ = M.theta_na(e + R0, ms) if e + R0 > 0 else (np.nan, None)
        print(f"   {e:+.5f}   {RH:.5f}   {R0:.5f}      {na:.5f}        {na - RH:+.5f}        {na0 - R0:+.5f}    (m_H = {mH:.2f}, m_na = {mn:.2f})")
    return M

t0 = time.time()
G = int(sys.argv[1]) if len(sys.argv) > 1 else 501
run(0.0, 0.0, 1.0, G)        # uniform cube (control)
run(0.5, 0.0, 1.0, G)        # single phase
run(0.5, 0.3, 1.0, G)        # single phase with a field
run(1.5, 0.0, 1.0, G)        # two phases
run(1.5, 0.0, 0.3, G)        # two phases, small Lipschitz constant (barrier not flattened completely?)
run(1.5, 0.05, 1.0, G)       # two phases, metastable
print("time", round(time.time() - t0, 1))
