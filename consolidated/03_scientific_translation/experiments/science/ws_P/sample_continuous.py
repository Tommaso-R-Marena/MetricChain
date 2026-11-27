"""
Off-grid ("continuous") ensemble for Ace-(Ala)_n-NMe and single-torsion scans.

Ensemble C: every residue's (phi, psi) drawn uniformly from the clash-free part of the
dipeptide map (5-degree cells with clash score > TAU at the cell centre, plus uniform jitter
inside the cell); conformations with a non-local clash (score <= TAU) are rejected.

usage:
  python3 sample_continuous.py ens  <n> <M>            -> data/cont_n<n>.npz
  python3 sample_continuous.py scan <n> <Nbase> [step] -> data/scan_n<n>.npz
       for Nbase conformations of ensemble C and every torsion i: g along a full rotation of
       torsion i (step degrees, default 10), the other torsions fixed.
"""
import sys, math, time, os
import numpy as np
from pepbuild import Peptide
from fastff import FastFF

TAU = 0.7


def allowed_cells():
    P1 = Peptide(1, extra_ffs=(), solvent=False, platform="Reference")
    ang = np.arange(-177.5, 180.0, 5.0)
    PH, PS = np.meshgrid(ang, ang, indexing="ij")
    X = P1.coords(np.deg2rad(PH.reshape(-1, 1)), np.deg2rad(PS.reshape(-1, 1)))
    cs = P1.clash_score(X)
    ok = cs > TAU
    return PH.reshape(-1)[ok], PS.reshape(-1)[ok], ok.mean()


def sample(P, n, M, rng, cells):
    cph, cps, _ = cells
    phis, psis = [], []
    tried = 0
    while sum(len(a) for a in phis) < M:
        B = 4096
        pick = rng.integers(0, len(cph), (B, n))
        phi = np.deg2rad(cph[pick] + rng.uniform(-2.5, 2.5, (B, n)))
        psi = np.deg2rad(cps[pick] + rng.uniform(-2.5, 2.5, (B, n)))
        X = P.coords(phi, psi)
        ok = P.clash_score(X) > TAU
        phis.append(phi[ok]); psis.append(psi[ok]); tried += B
    phi = np.concatenate(phis)[:M]; psi = np.concatenate(psis)[:M]
    return phi, psi, sum(len(a) for a in phis) / tried


def main():
    mode, n = sys.argv[1], int(sys.argv[2])
    rng = np.random.default_rng(2026 + n)
    P = Peptide(n, extra_ffs=("ff03", "ff15ipq"), platform="CPU")
    F = FastFF(P, threads=1)
    cells = allowed_cells()
    os.makedirs("data", exist_ok=True)
    t0 = time.time()
    if mode == "ens":
        M = int(sys.argv[3])
        phi, psi, acc = sample(P, n, M, rng, cells)
        X = P.coords(phi, psi)
        E = F.energies(X, gb=("gbn2", "obc2"))
        np.savez(f"data/cont_n{n}.npz", n=n, phi=phi, psi=psi, acceptance=acc,
                 local_allowed_fraction=cells[2], **E)
        g = E["gbn2"]
        print(f"ens n={n}: {M} conformations, non-local acceptance {acc:.3f}, locally allowed fraction of the "
              f"(phi,psi) map {cells[2]:.3f}; GB mean {g.mean():.2f} std {g.std():.2f} range {g.max()-g.min():.2f}; {time.time()-t0:.0f}s", flush=True)
    elif mode == "scan":
        Nb = int(sys.argv[3]); step = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0
        phi, psi, acc = sample(P, n, Nb, rng, cells)
        ang = np.deg2rad(np.arange(-180.0, 180.0, step)); K = len(ang)
        m = 2 * n
        keys = ("gbn2", "tors", "lj", "coul", "clash", "ff03_tors", "ff03_lj", "ff03_coul",
                "ff15ipq_tors", "ff15ipq_lj", "ff15ipq_coul")
        out = {k: np.empty((Nb, m, K)) for k in keys}
        for site in range(m):
            ph = np.repeat(phi, K, axis=0); ps = np.repeat(psi, K, axis=0)
            if site % 2 == 0:
                ph[:, site // 2] = np.tile(ang, Nb)
            else:
                ps[:, site // 2] = np.tile(ang, Nb)
            E = F.energies(P.coords(ph, ps), gb=("gbn2",))
            for k in keys:
                out[k][:, site, :] = E[k].reshape(Nb, K)
            print(f"  scan n={n} site {site + 1}/{m}  {time.time() - t0:.0f}s", flush=True)
        np.savez(f"data/scan_n{n}.npz", n=n, phi=phi, psi=psi, step=step, **out)
        print(f"scan n={n}: {Nb} base conformations x {m} torsions x {K} angles; {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
