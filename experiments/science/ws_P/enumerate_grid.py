"""
Exact enumeration of Ace-(Ala)_n-NMe on a product torsion grid.

usage: python3 enumerate_grid.py <n> <alphabet> [--no-obc2] [--part i/m]

Alphabets (states per torsion; sites ordered phi_1, psi_1, ..., phi_n, psi_n):
  A3 : phi in {-150, -70, +60},  psi in {-40, +60, +150}        (9 states per residue)
  A2 : phi in {-150, -70},       psi in {-40, +150}             (4 states per residue)
  U6 : phi, psi in {-150, -90, -30, 30, 90, 150}                (36 per residue)
  U12: phi, psi on a 30-degree grid from -165                   (144 per residue)

Output: data/grid_<alphabet>_n<n>.npz with one float64 array of length k^(2n) per energy
component (kcal/mol), C-ordered so that arr.reshape((k,)*(2n)) has axis i = torsion site i.
"""
import sys, time, math, os, itertools
import numpy as np
from pepbuild import Peptide, KCAL
from fastff import FastFF

ALPHABETS = {
    "A3": ([-150.0, -70.0, 60.0], [-40.0, 60.0, 150.0]),
    "A2": ([-150.0, -70.0], [-40.0, 150.0]),
    "U6": ([-150.0, -90.0, -30.0, 30.0, 90.0, 150.0],) * 2,
    "U12": (list(np.arange(-165.0, 180.0, 30.0)),) * 2,
}


def grid_angles(n, alphabet, idx):
    """idx: (M,) conformation indices -> phi, psi (M, n) in radians and states (M, 2n)."""
    ph, ps = ALPHABETS[alphabet]
    k = len(ph)
    m = 2 * n
    st = np.empty((len(idx), m), dtype=np.int8)
    rem = idx.copy()
    for site in range(m - 1, -1, -1):
        st[:, site] = rem % k
        rem //= k
    phi = np.deg2rad(np.array(ph))[st[:, 0::2]]
    psi = np.deg2rad(np.array(ps))[st[:, 1::2]]
    return phi, psi, st


def cmap_table(alphabet, name="ff19SB"):
    """CMAP energy (kcal/mol) of one residue for every (phi state, psi state), from OpenMM."""
    ph, ps = ALPHABETS[alphabet]
    P1 = Peptide(1, extra_ffs=(name,), solvent=False, platform="Reference")
    k = len(ph)
    tab = np.zeros((k, len(ps)))
    for a in range(k):
        X = P1.coords(np.full((len(ps), 1), math.radians(ph[a])), np.deg2rad(np.array(ps))[:, None])
        tab[a] = P1.cmap_energy(X, name)
    return tab


def main():
    n = int(sys.argv[1]); alphabet = sys.argv[2]
    obc2 = "--no-obc2" not in sys.argv
    part = None
    if "--part" in sys.argv:
        a, b = sys.argv[sys.argv.index("--part") + 1].split("/")
        part = (int(a), int(b))
    k = len(ALPHABETS[alphabet][0])
    total = k ** (2 * n)
    lo, hi = 0, total
    if part:
        lo = total * part[0] // part[1]; hi = total * (part[0] + 1) // part[1]
    t0 = time.time()
    P = Peptide(n, platform="CPU")
    F = FastFF(P, threads=1)
    tab = cmap_table(alphabet)
    gb = ("gbn2", "obc2") if obc2 else ("gbn2",)
    out = None
    step = 8192
    rng = np.random.default_rng(12345 + n)
    worst = 0.0
    for s in range(lo, hi, step):
        idx = np.arange(s, min(hi, s + step), dtype=np.int64)
        phi, psi, st = grid_angles(n, alphabet, idx)
        X = P.coords(phi, psi)
        E = F.energies(X, gb=gb)
        E["ff19SB_cmap"] = tab[st[:, 0::2], st[:, 1::2]].sum(axis=1)
        if out is None:
            out = {key: np.empty(hi - lo) for key in E}
        for key in E:
            out[key][s - lo:s - lo + len(idx)] = E[key]
        # spot check against OpenMM (CPU platform, single precision) on 2 conformations per block
        pick = rng.choice(len(idx), size=min(2, len(idx)), replace=False)
        Eo = P.energies(X[pick])
        for j, p in enumerate(pick):
            if E["clash"][p] > 0.6:
                dv = [abs(Eo["gbn2"][j] - E["gbn2"][p]), abs(Eo["tors"][j] - E["tors"][p]),
                      abs(Eo["nb"][j] - E["lj"][p] - E["coul"][p]),
                      abs(Eo["ff19SB_cmap"][j] - E["ff19SB_cmap"][p]),
                      abs(Eo["ff03"][j] - Eo["bond"][j] * 0 - (E["ff03_tors"][p] + E["ff03_lj"][p] + E["ff03_coul"][p])
                          - (Eo["ff03"][j] - Eo["ff03_tors"][j] - Eo["ff03_nb"][j]))]
                worst = max(worst, max(dv))
        if (s - lo) // step % 20 == 0:
            print(f"  {s - lo + len(idx)}/{hi - lo}  {time.time() - t0:.0f}s  worst spot-check dev {worst:.2e}", flush=True)
    os.makedirs("data", exist_ok=True)
    tag = f"grid_{alphabet}_n{n}" + (f"_part{part[0]}of{part[1]}" if part else "")
    np.savez(f"data/{tag}.npz", n=n, alphabet=alphabet, k=k, lo=lo, hi=hi,
             phi_states=np.array(ALPHABETS[alphabet][0]), psi_states=np.array(ALPHABETS[alphabet][1]),
             cmap_table=tab, **out)
    print(f"n={n} {alphabet}: {hi - lo} conformations in {time.time() - t0:.1f}s; "
          f"worst spot-check deviation fast vs OpenMM CPU platform: {worst:.2e} kcal/mol", flush=True)


if __name__ == "__main__":
    main()
