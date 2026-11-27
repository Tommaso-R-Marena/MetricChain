"""How far is the GBn2 polarisation energy from an EXACTLY pair-additive function of the atom
positions (every atom pair its own radial function)?  Constructive upper bound:
   S(x) = sum_{i<j} e_pair(r_ij; Bbar_i, Bbar_j)  -  (tau/2) sum_i q_i^2 (a_i + b_i I_i(x)),
where I_i(x) = sum_j H_ij(r_ij) is the (pair-additive) descreening sum of atom i, Bbar_i the
mean Born radius, and a_i + b_i I the least-squares line through 1/B_i(I_i).  S is exactly
pair-additive with pair-specific radial functions, so |g - S - const| bounds the distance of
g_GB to that class from above (RMS: for this particular S; max: sup-norm distance <= max).
Parameters (Bbar, a, b) are fitted on ensemble C and then applied to the grids unchanged.
usage: python3 an11_manybody.py n [n ...]"""
import sys, os, math, json
import numpy as np
import numexpr as ne
from pepbuild import Peptide, KT300, KCAL
from fastff import FastFF, ONE_4PI_EPS0
from analysis_lib import load, residuals, HERE
from enumerate_grid import grid_angles

def details(F, X, chunk=256):
    """Born radii B (nm), descreening sums I, and r^2 (upper triangle) for GBn2."""
    g = F.gb["gbn2"]; F._prepare() if not getattr(F, "_prepared", False) else None
    orr = g["or"]; sr = g["sr"]; or1 = orr[None, :, None]; sr2 = sr[None, None, :]
    off = F._offdiag; d0, m0, cut = g["_d0"], g["_m0"], g["_cut"]
    i, j = F.iu; eye = np.eye(F.nat)[None]
    Bs, Is, R2 = [], [], []
    for s in range(0, X.shape[0], chunk):
        x = X[s:s + chunk] * 0.1
        r2 = ((x[:, :, None, :] - x[:, None, :, :]) ** 2).sum(3)
        r = np.sqrt(r2 + eye)
        U = r + sr2; L = np.maximum(or1, np.abs(r - sr2))
        I = ne.evaluate("off * (where(r + sr2 - or1 >= 0.0, 0.5*(1.0/L - 1.0/U + 0.25*(r - sr2*sr2/r)*(1.0/(U*U) - 1.0/(L*L)) + 0.5*log(L/U)/r), 0.0)"
                        " + where(cut - r >= 0.0, 0.826836*m0/(1.0 + 100.0*(r-d0)**2 + 0.3e6*(r-d0)**6), 0.0))").sum(axis=2)
        psi = I * orr[None]; rad = (orr + 0.0195141)[None]
        th = np.tanh(g["alpha"][None] * psi - g["beta"][None] * psi ** 2 + g["gamma"][None] * psi ** 3)
        Bs.append(1.0 / (1.0 / orr[None] - th / rad)); Is.append(I); R2.append(r2[:, i, j])
    return np.concatenate(Bs), np.concatenate(Is), np.concatenate(R2)

def parts(F, B, r2u):
    q = F.gb["gbn2"]["charge"]; pref = ONE_4PI_EPS0 * (1.0 - 1.0 / 78.5); i, j = F.iu
    e_self = -0.5 * pref * (q[None] ** 2 / B).sum(1)
    BB = B[:, i] * B[:, j]; qq = (q[i] * q[j])[None]
    e_pair = -pref * ne.evaluate("qq / sqrt(r2u + BB * exp(-r2u / (4.0 * BB)))").sum(axis=1)
    return e_self / KCAL, e_pair / KCAL

out = {}
for n in [int(a) for a in sys.argv[1:]]:
    P = Peptide(n, extra_ffs=(), platform="Reference"); F = FastFF(P, threads=1)
    d = dict(np.load(os.path.join(HERE, "data", f"cont_n{n}.npz")))
    X = P.coords(d["phi"], d["psi"])
    B, I, r2u = details(F, X)
    e_self, e_pair = parts(F, B, r2u)
    assert np.abs(e_self + e_pair - d["gbn2"]).max() < 1e-8, np.abs(e_self + e_pair - d["gbn2"]).max()
    M = len(X); half = M // 2
    q = F.gb["gbn2"]["charge"]; pref = ONE_4PI_EPS0 * (1.0 - 1.0 / 78.5)
    Bbar = B[:half].mean(axis=0)
    # S(x) = sum_{i<j} e_pair(r_ij; Bbar_i, Bbar_j) + w0 + sum_i w_i I_i(x): the weights w are fitted by least
    # squares on the training half (first-order response of self AND cross terms to the descreening sums)
    def frozen_pair(Bx, r2x):
        _, s_pair = parts(F, np.broadcast_to(Bbar, Bx.shape).copy(), r2x)
        return s_pair
    t = d["gbn2"][:half] - frozen_pair(B[:half], r2u[:half])
    A = np.hstack([np.ones((half, 1)), I[:half]])
    w, *_ = np.linalg.lstsq(A, t, rcond=None)
    # for comparison: the naive version (self term linearised atom by atom, cross term frozen)
    Im = I[:half].mean(0); iB = 1.0 / B[:half]; iBm = iB.mean(0)
    b = ((I[:half] - Im) * (iB - iBm)).sum(0) / np.maximum(((I[:half] - Im) ** 2).sum(0), 1e-30)
    a = iBm - b * Im
    def report(label, g, Bx, Ix, r2x):
        sp = frozen_pair(Bx, r2x)
        S = sp + w[0] + Ix @ w[1:]
        r = g - S; r0 = r - r.mean()
        s_naive = sp - 0.5 * pref * (q[None] ** 2 * (a[None] + b[None] * Ix)).sum(1) / KCAL
        rn = g - s_naive; rn -= rn.mean()
        print(f"  {label:24s} std(g) {g.std():5.2f} | g - S (intercept as fitted): RMS {np.sqrt((r**2).mean()):.3f} max {np.abs(r).max():.2f} kcal/mol; "
              f"intercept refitted: RMS {np.sqrt((r0**2).mean()):.3f} max {np.abs(r0).max():.2f} = {np.sqrt((r0**2).mean())/KT300:.2f} / {np.abs(r0).max()/KT300:.1f} kT | "
              f"naive frozen-radii surrogate: RMS {np.sqrt((rn**2).mean()):.2f} max {np.abs(rn).max():.1f} | "
              f"Born radii rel. std: mean {np.mean(Bx.std(0)/Bx.mean(0)):.3f}, max {np.max(Bx.std(0)/Bx.mean(0)):.3f}")
        return dict(rms=float(np.sqrt((r0**2).mean())), max=float(np.abs(r0).max()), std=float(g.std()), rms_naive=float(np.sqrt((rn**2).mean())))
    print(f"=== n={n}: exactly pair-additive surrogate of g_GB fitted on {half} conformations of ensemble C")
    out[f"{n}|C-train"] = report("ensemble C (train)", d["gbn2"][:half], B[:half], I[:half], r2u[:half])
    out[f"{n}|C-test"] = report("ensemble C (held-out)", d["gbn2"][half:], B[half:], I[half:], r2u[half:])
    for alphabet in ("A3", "A2"):
        if not (os.path.exists(os.path.join(HERE, "data", f"grid_{alphabet}_n{n}.npz"))):
            continue
        dg = load(alphabet, n); mask = dg["clash"] > 0.7
        flat = np.flatnonzero(mask.reshape(-1))
        if len(flat) > 40000:
            flat = np.sort(np.random.default_rng(3).choice(flat, 40000, replace=False))
        phi, psi, _ = grid_angles(n, alphabet, flat.astype(np.int64))
        Xg = P.coords(phi, psi)
        Bg, Ig, r2g = details(F, Xg)
        out[f"{n}|{alphabet}"] = report(f"grid {alphabet} ({len(flat)} conf.)", dg["gbn2"].reshape(-1)[flat], Bg, Ig, r2g)
p = os.path.join(HERE, "out", "an11_manybody.json")
old = json.load(open(p)) if os.path.exists(p) else {}
old.update(out); json.dump(old, open(p, "w"), indent=0)
