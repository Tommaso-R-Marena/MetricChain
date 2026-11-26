#!/usr/bin/env python3
"""Science division — the discretisation term on a real force field (addendum A17 (25), item 100).

Model (workstream P2's builder, imported, not modified): Ace-X_1..X_r-NMe with residues from {Val, Leu, Ser, Ala},
ff14SB vacuum energy plus the GBn2 polarisation energy (OpenMM), ideal backbone (helix H = (-57, -47) or strand
E = (-139, 135) degrees), all bond lengths, bond angles and the backbone rigid; the only degrees of freedom are the
side-chain torsions (Val: chi_1; Leu: chi_1, chi_2; Ser: chi_1 and the hydroxyl torsion; Ala: none) — n in all, each
a "site".  Temperature 300 K (kT = 0.596 kcal/mol).  Reference measure: uniform on the torus of the n torsions.

"Continuum" = the rectangle rule on Nf points per angle (periodic), written cell by cell as a trapezoid rule on
closed cells, as in continuous_cells.py; every inequality of Proposition A17.24 is exact for this grid model and
is asserted.  The whole energy is ONE term on all sites (no pairwise decomposition is used), so the discrete
models are full tables over the k^n cell states.

Computed:
 (a) ln Z of the grid model;
 (b) the three-rotamer model: chi_1 in {60, 180, 300} degrees, each rotamer standing for a third of the circle
     (the model whose free energy the certificates of this branch are about), and the "minimised rotamer" model
     (cell minimum in place of the rotamer's energy) — their ln Z against (a), and their state populations;
 (c) the brackets of Proposition A17.24 from k cells per angle: cell minima/maxima; Jensen / bounded differences
     (mode H everywhere); the best assignment of modes by a threshold on c_i.
 (d) the same with a TILTED reference (remark 2 of item 97): e_i = the one-body slice of the energy through the
     grid minimum, nu_i ~ exp(-e_i); only the remainder V = E - E_min - sum_i e_i is discretised.  The lower end is
     then a discrete model with exact one-site cell free energies and cell-averaged remainder.
Controls that can fail: all coordinates in mode M must reproduce the bound by cell minima; the Jensen value used
as an upper end must be violated; a grid of twice the spacing (every second point) must give a nearby ln Z.
Run:  python3 -B continuous_cells_real.py VV H 144 ; ... VVV E 72     (energies are cached in --cache DIR)
"""
import sys, os, time, itertools, resource, argparse
import numpy as np
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
KT = 0.596                       # kcal/mol at 300 K, as in docs/science/PHYSICAL_APPLICABILITY.md
BACKBONE = {"H": (-57.0, -47.0), "E": (-139.0, 135.0)}
TOL = 1e-9

ap = argparse.ArgumentParser()
ap.add_argument("seq"); ap.add_argument("bb"); ap.add_argument("Nf", type=int)
ap.add_argument("--cache", default=os.environ.get("CC_CACHE", os.path.join(HERE, "cc_cache")))
args = ap.parse_args()
t0 = time.time()
seq, bb, Nf = args.seq, args.bb, args.Nf
NCHI1 = {"V": 1, "L": 2, "S": 2, "A": 0}
assert set(seq) <= set(NCHI1), "residues: V, L, S, A (alanine: no torsion, a spacer)"
nres = len(seq); n = sum(NCHI1[c] for c in seq); assert n <= 3, "at most three torsions (the grid is Nf^n)"
os.makedirs(args.cache, exist_ok=True)
cache = os.path.join(args.cache, f"E_{seq}_{bb}_{Nf}.npy")


def energy_grid():
    import scbuild
    import openmm.unit as unit
    pep = scbuild.SCPeptide(seq, solvent=True)
    assert pep.nchi == n
    kj = unit.kilojoule_per_mole
    phi0, psi0 = np.deg2rad(BACKBONE[bb])
    ang = np.arange(Nf) * 2 * np.pi / Nf
    out = np.empty((Nf,) * n + (2,))
    flat = out.reshape(-1, 2)
    idx = np.array(list(itertools.product(range(Nf), repeat=n)))
    CH = 20000
    for a in range(0, len(idx), CH):
        chi = ang[idx[a:a + CH]]
        X = pep.coords(np.full((len(chi), nres), phi0), np.full((len(chi), nres), psi0), chi)
        for m in range(len(chi)):
            pep.ctx.setPositions(X[m] * 0.1)
            flat[a + m, 0] = pep.ctx.getState(getEnergy=True, groups=0b1111).getPotentialEnergy().value_in_unit(kj)
            flat[a + m, 1] = pep.ctx.getState(getEnergy=True, groups=1 << 5).getPotentialEnergy().value_in_unit(kj)
    return out / scbuild.KCAL, pep.natoms


if os.path.exists(cache):
    EE = np.load(cache); natoms = -1; src = "cache"
else:
    EE, natoms = energy_grid(); np.save(cache, EE); src = f"computed in {time.time()-t0:.0f} s"
E = (EE[..., 0] + EE[..., 1]) / KT            # total energy in kT: vacuum ff14SB + GBn2
E = E - E.min()
lnZ = float(logsumexp(-E) - n * np.log(Nf))
sub = E[(slice(None, None, 2),) * n]
lnZ2 = float(logsumexp(-sub) - n * np.log(Nf // 2))
print(f"=== Ace-{seq}-NMe ({nres} residues, {n} side-chain torsions), backbone {bb} {BACKBONE[bb]}, ff14SB + GBn2, 300 K; every torsion on {Nf} points ({360/Nf:g} deg), {Nf**n} conformations ({src})")
print(f"energy range over the grid: vacuum {EE[...,0].min():.2f} .. {EE[...,0].max():.4g} kcal/mol; GBn2 {EE[...,1].min():.2f} .. {EE[...,1].max():.2f}; total range {E.max():.4g} kT")
print(f"(a) ln Z of the grid model (energy zero at the grid minimum; uniform reference): {lnZ:.6f}; with every second grid point: {lnZ2:.6f} (difference {lnZ2-lnZ:+.2e})")

# ------------------------------------------------------------------ (b) rotamer models
rot = [int(round(d / 360 * Nf)) for d in (60, 180, 300)]
assert all(abs(r * 360 / Nf - d) < 1e-9 for r, d in zip(rot, (60, 180, 300))), "the rotamer angles must be grid points"
Erot = E[np.ix_(*([rot] * n))]
lnZ_rot = float(logsumexp(-Erot) - n * np.log(3))


def cell_blocks(k):
    m = Nf // k; assert Nf % k == 0
    idx = (np.arange(k)[:, None] * m + np.arange(m + 1)[None, :]) % Nf
    trap = np.full(m + 1, 1.0 / m); trap[0] = trap[-1] = 0.5 / m
    ix = []
    for d in range(n):
        shape = [1] * (2 * n); shape[2 * d] = k; shape[2 * d + 1] = m + 1
        ix.append(idx.reshape(shape))
    B = E[tuple(ix)]                      # axes: (s_1, a_1, s_2, a_2, ...)
    return B, trap, m


def reduce_blocks(B, trap, A, P=None):
    """minimum over the inner axes of the sites in A, then the mean over the other inner axes (trapezoid weights, or the
    conditional weights P[d] of shape (k, m+1) of a tilted reference); also, for every site i not in A, the oscillation
    of the min-reduced block in its inner axis (sup over the others)"""
    R = B
    for d in sorted(A, reverse=True):
        R = R.min(axis=2 * d + 1, keepdims=True)
    osc = {}
    for i in range(n):
        if i in A: continue
        o = R.max(axis=2 * i + 1, keepdims=True) - R.min(axis=2 * i + 1, keepdims=True)
        for d in range(n):
            if d != i: o = o.max(axis=2 * d + 1, keepdims=True)
        osc[i] = o.reshape([B.shape[2 * d] for d in range(n)])
    Rm = R
    for d in range(n):
        if d in A:
            continue
        if P is None:
            w = trap.reshape([-1 if ax == 2 * d + 1 else 1 for ax in range(2 * n)])
        else:
            shape = [1] * (2 * n); shape[2 * d] = P[d].shape[0]; shape[2 * d + 1] = P[d].shape[1]
            w = P[d].reshape(shape)
        Rm = (Rm * w).sum(axis=2 * d + 1, keepdims=True)
    return Rm.reshape([B.shape[2 * d] for d in range(n)]), osc


B3, trap3, _ = cell_blocks(3)
Emin3, _ = reduce_blocks(B3, trap3, set(range(n)))
lnZ_min3 = float(logsumexp(-Emin3) - n * np.log(3))
# populations of the 3^n cells: grid model, rigid rotamers, minimised rotamers
Pg = np.zeros((3,) * n)
w = trap3
for d in range(n):
    pass
Wfull = np.exp(-B3)
for d in range(n):
    shape = [-1 if ax == 2 * d + 1 else 1 for ax in range(2 * n)]
    Wfull = (Wfull * trap3.reshape(shape)).sum(axis=2 * d + 1, keepdims=True)
Pg = Wfull.reshape((3,) * n); Pg = Pg / Pg.sum()
Pr = np.exp(-Erot); Pr /= Pr.sum()
Pm = np.exp(-Emin3); Pm /= Pm.sum()
print(f"(b) three-rotamer model (every torsion at 60, 180, 300 deg; each rotamer weighs a third of the circle): ln Z = {lnZ_rot:.4f}; minus the grid: {lnZ_rot-lnZ:+.4f} nats = {(lnZ_rot-lnZ)/n:+.4f} per torsion")
print(f"    minimised-rotamer model (cell minimum over 120-degree cells): ln Z = {lnZ_min3:.4f}; minus the grid: {lnZ_min3-lnZ:+.4f} nats = {(lnZ_min3-lnZ)/n:+.4f} per torsion")
print(f"    populations of the {3**n} rotamer cells: grid against rigid rotamers: largest difference {np.abs(Pg-Pr).max():.4f}, total variation {0.5*np.abs(Pg-Pr).sum():.4f}; grid against minimised rotamers: largest {np.abs(Pg-Pm).max():.4f}, total variation {0.5*np.abs(Pg-Pm).sum():.4f}")
print(f"    most populated cell: grid {Pg.max():.4f} (cell {np.unravel_index(Pg.argmax(), Pg.shape)}), rigid rotamers {Pr.max():.4f} (cell {np.unravel_index(Pr.argmax(), Pr.shape)}), minimised {Pm.max():.4f} (cell {np.unravel_index(Pm.argmax(), Pm.shape)})")

# the minimum-energy state: where the rigid-rotamer model has it and where the continuous energy has it
c_rot = tuple(int(x) for x in np.unravel_index(Erot.argmin(), Erot.shape))
c_min = tuple(int(x) for x in np.unravel_index(Emin3.argmin(), Emin3.shape))
second = np.partition(Erot.ravel(), 1)[1] - Erot.min() if Erot.size > 1 else float("nan")
print(f"    minimum-energy state: rigid rotamers — cell {c_rot} (gap to the next rotamer state {second:.3f} kT); continuous energy — cell {c_min} (at torsions "
      + ", ".join(f"{x*360/Nf:g}" for x in np.unravel_index(E.argmin(), E.shape)) + f" deg); the same cell: {c_rot == c_min}"
      + ("" if c_rot == c_min else f"; the continuous minimum of the rigid model's cell lies {Emin3[c_rot]-Emin3.min():.3f} kT above the global minimum"))
# per-cell anatomy: population in the grid model and in the two rotamer models; strain of the ideal rotamer above the cell
# minimum; and the cell's width term  -ln <exp(-(E - E_min))>_cell  (what a rotamer model ignores)
Fcell = -np.log(Wfull.reshape((3,) * n)) - Emin3
order = np.argsort(-Pg.ravel())[: (9 if n <= 2 else 6)]
print("    cell (index of the 120-degree cell of each torsion; 0, 1, 2 = centred at 60, 180, 300 deg): population grid / rigid rotamer / minimised;  E_rot - E_min [kT];  width term [nats]")
for f in order:
    c = np.unravel_index(f, Pg.shape)
    print(f"      {tuple(int(x) for x in c)}:  {Pg[c]:.4f} / {Pr[c]:.4f} / {Pm[c]:.4f};   {Erot[c]-Emin3[c]:8.3f};   {Fcell[c]:6.3f}")
wt = np.sum(Pg * Fcell)
print(f"    population-weighted width term: {wt:.4f} nats = {wt/n:.4f} per torsion; spread of the width term over cells with population above 1 %: {Fcell[Pg > 0.01].min():.3f} .. {Fcell[Pg > 0.01].max():.3f}")

# ------------------------------------------------------------------ (c) brackets of Proposition A17.24
print("(c) brackets for ln Z from k cells per angle [nats; widths per torsion in the last three columns]")
print("    k   cell   minima/maxima bracket             width    Jensen end    bounded-differences end (all H)   best modes: upper end    width    threshold   | per torsion: first-order   all-H     best")
rows = []
ks = [k for k in (3, 6, 12, 18, 24, 36, 48, 72, 144) if Nf % k == 0 and (n <= 2 or k <= 72)]
subsets = [set(c) for r in range(n + 1) for c in itertools.combinations(range(n), r)]
for k in ks:
    Bk, trap, m = cell_blocks(k)
    red = {frozenset(A): reduce_blocks(Bk, trap, A) for A in subsets}
    mean, osc0 = red[frozenset()]
    mn = red[frozenset(range(n))][0]
    mx = Bk
    for d in range(n): mx = mx.max(axis=2 * d + 1, keepdims=True)
    mx = mx.reshape((k,) * n)
    lw = -n * np.log(k)
    lo1 = float(logsumexp(-mx) + lw); hi1 = float(logsumexp(-mn) + lw); jl = float(logsumexp(-mean) + lw)
    with np.errstate(over="ignore"):
        hH = float(logsumexp(-mean + sum(osc0[i] ** 2 for i in range(n)) / 8) + lw)
    # modes by a threshold on the largest c_i a (site, cell) can meet
    cmax = [osc0[i].max(axis=tuple(d for d in range(n) if d != i)) for i in range(n)]
    best, best_thr = np.inf, None
    for thr in (np.inf, 12, 8, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0):
        M = [cmax[i] > thr for i in range(n)]
        expo = np.full((k,) * n, np.nan)
        for A in subsets:
            sel = np.ones((k,) * n, dtype=bool)
            for i in range(n):
                mi = M[i].reshape([-1 if d == i else 1 for d in range(n)])
                sel = sel & (mi if i in A else ~mi)
            if not sel.any(): continue
            R, osc = red[frozenset(A)]
            with np.errstate(over="ignore"):
                val = -R + sum(osc[i] ** 2 for i in osc) / 8
            expo[sel] = val[sel]
        assert not np.isnan(expo).any()
        up = float(logsumexp(expo) + lw)
        assert lnZ <= up + TOL, ("upper end violated", k, thr, up, lnZ)
        if thr == -1.0:
            assert abs(up - hi1) < 1e-9 * max(1.0, abs(hi1)), "control: all coordinates in mode M must give the bound by cell minima"
        if up < best: best, best_thr = up, thr
    assert lo1 <= lnZ + TOL and lnZ <= hi1 + TOL and jl <= lnZ + TOL and lnZ <= hH + TOL and lo1 <= jl + TOL
    viol = lnZ > jl + 1e-12
    ts = "all H" if best_thr == np.inf else ("all M" if best_thr == -1.0 else f"{best_thr:g}")
    rows.append(dict(k=k, w1=hi1 - lo1, wH=hH - jl, wb=best - jl, viol=viol, jl=jl))
    print(f"  {k:4d} {360/k:6.2f}  [{lo1:11.4f}, {hi1:11.4f}] {hi1-lo1:9.3e}   {jl:11.4f}   {hH:14.6g} ({hH-jl:9.3e})        {best:11.4f}    {best-jl:9.3e}   {ts:>6s}     |   {(hi1-lo1)/n:9.3e}  {(hH-jl)/n:9.3e}  {(best-jl)/n:9.3e}" + ("" if viol else "  [control NOT violated]"))
# ------------------------------------------------------------------ (d) tilted reference: one-body slices through the minimum
xs = np.unravel_index(E.argmin(), E.shape)
e1 = []
for i in range(n):
    sl = tuple(slice(None) if d == i else xs[d] for d in range(n))
    e1.append(E[sl].copy())                                   # E is zero at the grid minimum
V = E.copy()
for i in range(n):
    V = V - e1[i].reshape([-1 if d == i else 1 for d in range(n)])
lz1 = [float(logsumexp(-e1[i]) - np.log(Nf)) for i in range(n)]
lw_full = sum((-e1[i]).reshape([-1 if d == i else 1 for d in range(n)]) for i in range(n))
chk = float(logsumexp(lw_full - V) - n * np.log(Nf))
assert abs(chk - lnZ) < 1e-9, "the decomposition into one-body slices and a remainder must reproduce ln Z"
print(f"(d) tilted reference: one-body slices through the grid minimum (torsions at {', '.join(f'{x*360/Nf:g}' for x in xs)} deg); sum of the one-site ln z_i = {sum(lz1):.4f}; ln <exp(-V)> = {lnZ-sum(lz1):+.4f}; remainder V over the grid: {V.min():.4g} .. {V.max():.4g} kT")
print("    k   cell    Jensen end (one-site cell free energies, cell-averaged remainder): gap to the grid, per torsion     best certified upper end: gap, per torsion    threshold")
rows_t = []
for k in ks:
    m = Nf // k
    idx = (np.arange(k)[:, None] * m + np.arange(m + 1)[None, :]) % Nf
    trap = np.full(m + 1, 1.0 / m); trap[0] = trap[-1] = 0.5 / m
    ix = []
    for d in range(n):
        shape = [1] * (2 * n); shape[2 * d] = k; shape[2 * d + 1] = m + 1
        ix.append(idx.reshape(shape))
    Vb = V[tuple(ix)]
    P, lv = [], []
    for i in range(n):
        lwc = -e1[i][idx] + np.log(trap)[None, :] - np.log(k) - lz1[i]
        lvi = logsumexp(lwc, axis=1); lv.append(lvi); P.append(np.exp(lwc - lvi[:, None]))
    lvs = sum(lv[i].reshape([-1 if d == i else 1 for d in range(n)]) for i in range(n))
    redt = {frozenset(A): reduce_blocks(Vb, trap, A, P) for A in subsets}
    meanV, osc0 = redt[frozenset()]
    jt = float(logsumexp(lvs - meanV) + sum(lz1))
    assert jt <= lnZ + TOL, ("tilted Jensen end violated", jt, lnZ)
    cmax = [osc0[i].max(axis=tuple(d for d in range(n) if d != i)) for i in range(n)]
    best, best_thr = np.inf, None
    for thr in (np.inf, 12, 8, 6, 4, 3, 2, 1.5, 1, 0.5, -1.0):
        M = [cmax[i] > thr for i in range(n)]
        expo = np.full((k,) * n, np.nan)
        for A in subsets:
            sel = np.ones((k,) * n, dtype=bool)
            for i in range(n):
                mi = M[i].reshape([-1 if d == i else 1 for d in range(n)])
                sel = sel & (mi if i in A else ~mi)
            if not sel.any(): continue
            R, osc = redt[frozenset(A)]
            with np.errstate(over="ignore"):
                val = -R + sum(osc[i] ** 2 for i in osc) / 8
            expo[sel] = val[sel]
        up = float(logsumexp(lvs + expo) + sum(lz1))
        assert lnZ <= up + TOL, ("tilted upper end violated", k, thr, up, lnZ)
        if up < best: best, best_thr = up, thr
    ts = "all H" if best_thr == np.inf else ("all M" if best_thr == -1.0 else f"{best_thr:g}")
    rows_t.append(dict(k=k, gj=lnZ - jt, gu=best - lnZ))
    print(f"  {k:4d} {360/k:6.2f}    {jt:11.4f}    {lnZ-jt:9.3e}  {(lnZ-jt)/n:9.3e}                                    {best:11.4f}    {best-lnZ:9.3e}  {(best-lnZ)/n:9.3e}     {ts:>6s}")
rt3 = rows_t[0]
print(f"summary {seq} {bb}, tilted reference: at three cells per torsion the Jensen model is {rt3['gj']/n:.4f} nats per torsion below the grid (uniform reference: {(lnZ - rows[0]['jl'])/n:.3f}); the certified upper end is {rt3['gu']/n:.3g} per torsion above")

nv = sum(1 for r in rows if r["viol"])
r3 = rows[0]
print(f"summary {seq} {bb}: rotamer model minus grid {(lnZ_rot-lnZ)/n:+.4f} nats per torsion; minimised rotamers minus grid {(lnZ_min3-lnZ)/n:+.4f}; best certified bracket per torsion: "
      + ", ".join(f"k={r['k']}: {r['wb']/n:.3g}" for r in rows))
print(f"controls: the Jensen value as an upper end is violated in {nv} of {len(rows)} partitions; all-M reproduces the bound by minima (asserted); every bracket contains the grid value (asserted)")
print(f"ALL DONE  {time.time()-t0:.1f} s  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")
