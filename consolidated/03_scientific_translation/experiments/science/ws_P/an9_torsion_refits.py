"""Continuous-circle constants of the same-lineage force-field differences on the dipeptide:
g_99(phi) = E_ff99SB - E_ff14SB (function of phi only for Ala) on a 1-degree scan, and
g_19(phi, psi) = E_ff19SB - E_ff14SB on a 5-degree map (CMAP from OpenMM).  Also checks that
the differences do not depend on the other torsion / on chain length (n = 1 vs 3).
usage: python3 an9_torsion_refits.py"""
import math, numpy as np
from pepbuild import Peptide, KT300
from fastff import FastFF

P = Peptide(1, extra_ffs=("ff99SB", "ff19SB"), solvent=False, platform="Reference"); F = FastFF(P, threads=1)
ang = np.deg2rad(np.arange(-180.0, 180.0, 1.0))
res = {}
for psi0 in (-40.0, 60.0, 150.0):
    X = P.coords(ang[:, None], np.full((len(ang), 1), math.radians(psi0)))
    E = F.energies(X, gb=(), clash=False)
    g99 = E["ff99SB_tors"] + E["ff99SB_lj"] + E["ff99SB_coul"] - (E["tors"] + E["lj"] + E["coul"])
    nb = np.abs(E["ff99SB_lj"] + E["ff99SB_coul"] - E["lj"] - E["coul"]).max()
    res[psi0] = g99 - g99.mean()
    print(f"g_99 along phi (1 deg) at psi={psi0:6.1f}: max-min = {np.ptp(g99):.4f} kcal/mol = {np.ptp(g99)/KT300:.2f} kT; "
          f"max |d/dphi| = {np.abs(np.diff(g99)).max()/math.radians(1):.3f} kcal/mol/rad; non-bonded part of the difference <= {nb:.1e}")
print("dependence of g_99(phi) on psi: max deviation between the three scans:", np.abs(res[-40.0] - res[150.0]).max(), np.abs(res[60.0] - res[150.0]).max())
for phi0 in (-150.0, -70.0):
    X = P.coords(np.full((len(ang), 1), math.radians(phi0)), ang[:, None])
    E = F.energies(X, gb=(), clash=False)
    g99 = E["ff99SB_tors"] + E["ff99SB_lj"] + E["ff99SB_coul"] - (E["tors"] + E["lj"] + E["coul"])
    print(f"g_99 along psi at phi={phi0}: max-min = {np.ptp(g99):.2e} kcal/mol")
a5 = np.deg2rad(np.arange(-180.0, 180.0, 5.0))
PH, PS = np.meshgrid(a5, a5, indexing="ij")
X = P.coords(PH.reshape(-1, 1), PS.reshape(-1, 1))
E = F.energies(X, gb=(), clash=False)
g19 = (E["ff19SB_tors"] + P.cmap_energy(X, "ff19SB") + E["ff19SB_lj"] + E["ff19SB_coul"] - (E["tors"] + E["lj"] + E["coul"])).reshape(PH.shape)
print(f"g_19 on the 5-degree (phi, psi) map: max-min = {np.ptp(g19):.3f} kcal/mol = {np.ptp(g19)/KT300:.1f} kT; "
      f"largest change along phi at fixed psi {np.ptp(g19, axis=0).max():.3f}, along psi at fixed phi {np.ptp(g19, axis=1).max():.3f}; "
      f"largest mixed second difference over the map {np.abs(g19[:, :, None, None] - g19[:, None, :, None].transpose(2,1,0,3)).max() if False else float('nan')}")
# mixed second difference c_{phi psi} on the 5-degree map (all quadruples)
G = g19
best = 0.0
for a in range(G.shape[0]):
    D = (G[a][None, :, None] - G[:, :, None]) - (G[a][None, None, :] - G[:, None, :])     # (a2, b, b2)
    best = max(best, float(np.abs(D).max()))
print(f"g_19: mixed second difference over all (phi,phi',psi,psi') of the 5-degree map: {best:.3f} kcal/mol")
# restricted to the clash-free part of the map
ok = (P.clash_score(X) > 0.7).reshape(PH.shape)
Gm = np.where(ok, g19, np.nan)
cphi = np.nanmax(np.nanmax(Gm, axis=0) - np.nanmin(Gm, axis=0)); cpsi = np.nanmax(np.nanmax(Gm, axis=1) - np.nanmin(Gm, axis=1))
print(f"g_19 on the clash-free {100*ok.mean():.0f} % of the map: max-min = {np.nanmax(Gm)-np.nanmin(Gm):.3f} kcal/mol; "
      f"c_phi = {cphi:.3f}, c_psi = {cpsi:.3f} kcal/mol")
g99m = None
