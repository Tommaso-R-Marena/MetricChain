#!/usr/bin/env python3
"""R3 — own enumerator for the diamond-lattice chain of theory report §11.22 and independent
linear programmes for §9 and §11 of INFERENCE_LIMITS.md.  Written before opening the author's
scripts in experiments/science/pi_chain/.

Conventions (theory report §11.22): bond vectors +-a_i, a0=(1,1,1), a1=(1,-1,-1), a2=(-1,1,-1),
a3=(-1,-1,1); a walk is a sequence of bond indices with consecutive indices different (sign
alternates with the sublattice); N beads, n = N-3 torsions; torsion k (bonds k,k+1,k+2) is
trans iff index(k+2) = index(k); profile h = (h3,h8,h11) counts pairs p<q, q-p>=3, at squared
distance 3, 8, 11; g = number of gauche torsions.  First two bonds fixed to (0,1): 3^n torsion
patterns, of which the self-avoiding ones are the conformations (the engineering tables count
the same set: 27 for n=3, 683 for n=6).

Usage:  python3 r3_chain.py tables      # compare class tables with the engineering data, n<=10
        python3 r3_chain.py sec112      # §11.2 intervals from the engineering tables (dual LP)
        python3 r3_chain.py sec111      # §11.1 (13 beads) model-free intervals, own enumeration
        python3 r3_chain.py sec9        # §9 falsification thresholds b_min (8 and 9 beads)
        python3 r3_chain.py sec114      # §11.4 envelope + data intervals (9 beads)
"""
import sys, os, math, itertools
import numpy as np
from scipy.optimize import linprog
import scipy.sparse as sp

A = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], dtype=np.int64)
CHIRAL = True      # torsion states as internal coordinates (t, g+, g-)
ENG = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro/experiments/eng/chain_cover/data"

def enumerate_chain(n):
    """All 3^n torsion patterns (first two bonds 0,1).  Returns dict of arrays over ALL patterns:
    code (base-3 torsion pattern; digit 0 = trans, 1/2 = the two gauche states), sa (bool),
    and for self-avoiding ones h (3 cols), g, rg2, r2, plus coordinates for further features."""
    N = n + 3
    codes, sa, H, G, RG2, R2, XS = [], [], [], [], [], [], []
    for pat in itertools.product(range(3), repeat=n):
        idx = [0, 1]
        vec = [A[0], -A[1]]
        for k, s in enumerate(pat):
            prev2, prev1 = idx[-2], idx[-1]
            sgn = 1 if len(idx) % 2 == 0 else -1
            if s == 0:
                nxt = prev2
            else:
                others = [i for i in range(4) if i != prev2 and i != prev1]
                if CHIRAL:
                    # internal coordinate: the two gauche states are distinguished by the sign of
                    # the triple product (v_k x v_{k+1}) . v_{k+2}  (state 1: positive, 2: negative)
                    ch = [int(np.dot(np.cross(vec[-2], vec[-1]), sgn * A[i])) for i in others]
                    assert ch[0] * ch[1] < 0
                    pos_i = others[0] if ch[0] > 0 else others[1]
                    neg_i = others[1] if ch[0] > 0 else others[0]
                    nxt = pos_i if s == 1 else neg_i
                else:
                    nxt = others[s - 1]     # labelling by absolute bond index (NOT a torsion angle)
            idx.append(nxt); vec.append(sgn * A[nxt])
        x = np.zeros((N, 3), dtype=np.int64)
        for k in range(N - 1):
            x[k + 1] = x[k] + vec[k]
        code = 0
        for s in pat:
            code = code * 3 + s
        codes.append(code)
        ok = len({tuple(v) for v in x}) == N
        sa.append(ok)
        if ok:
            d2 = ((x[:, None, :] - x[None, :, :]) ** 2).sum(-1)
            iu = np.triu_indices(N, 3)
            dd = d2[iu]
            H.append((int((dd == 3).sum()), int((dd == 8).sum()), int((dd == 11).sum())))
            G.append(sum(1 for s in pat if s))
            xc = x - x.mean(0)
            RG2.append(float((xc ** 2).sum() / N))
            R2.append(int(d2[0, N - 1]))
            XS.append(x)
        else:
            H.append((-1, -1, -1)); G.append(-1); RG2.append(np.nan); R2.append(-1); XS.append(x)
    return dict(n=n, N=N, code=np.array(codes), sa=np.array(sa), h=np.array(H), g=np.array(G),
                rg2=np.array(RG2), r2=np.array(R2), x=np.array(XS))

def load_eng(n):
    rows = []
    with open(os.path.join(ENG, f"dia_Sc12_n{n}.txt")) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            rows.append([int(v) for v in line.split()])
    return np.array(rows, dtype=object)     # h3 h8 h11 count gmin count_gmin gmax

# ---------------------------------------------------------------- tables
def cmd_tables(nmax=10):
    for n in range(1, nmax + 1):
        ch = enumerate_chain(n)
        m = ch["sa"]
        mine = {}
        for h, g in zip(map(tuple, ch["h"][m]), ch["g"][m]):
            e = mine.setdefault(h, [0, 10 ** 9, 0, -1])
            e[0] += 1
            if g < e[1]:
                e[1], e[2] = g, 1
            elif g == e[1]:
                e[2] += 1
            e[3] = max(e[3], g)
        eng = {tuple(r[:3]): list(r[3:]) for r in load_eng(n)}
        same = (mine == eng)
        print(f"n={n:2d} (N={n + 3:2d} beads): self-avoiding {int(m.sum())} of {3 ** n}; classes {len(mine)}; "
              f"identical to the engineering table (classes, counts, gmin, #gmin, gmax): {same}")

# ---------------------------------------------------------------- generic model-free interval
def interval_dual(feat, m, target):
    """Identified interval of E target given E feat = m, over ALL probability measures on the
    rows: solved in DUAL form (variables: multipliers), independent of a primal formulation.
        upper = min_{lam,l0} lam.m + l0  s.t. lam.feat_x + l0 >= target_x  for all x
        lower = max_{lam,l0} lam.m + l0  s.t. lam.feat_x + l0 <= target_x  for all x"""
    X, K = feat.shape
    scale = np.maximum(np.abs(feat).max(0), 1.0)
    Fs = feat / scale; ms = m / scale
    Aub = np.hstack([Fs, np.ones((X, 1))])
    c = np.concatenate([ms, [1.0]])
    up = linprog(c, A_ub=-Aub, b_ub=-target, bounds=[(None, None)] * (K + 1), method="highs")
    lo = linprog(-c, A_ub=Aub, b_ub=target, bounds=[(None, None)] * (K + 1), method="highs")
    assert up.status == 0 and lo.status == 0, (up.message, lo.message)
    return -lo.fun, up.fun

def interval_primal(feat, m, target, weights=None):
    X, K = feat.shape
    scale = np.maximum(np.abs(feat).max(0), 1.0)
    Aeq = np.vstack([(feat / scale).T, np.ones(X)]); beq = np.concatenate([m / scale, [1.0]])
    lo = linprog(target, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * X, method="highs")
    up = linprog(-target, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * X, method="highs")
    assert up.status == 0 and lo.status == 0
    return lo.fun, -up.fun

def cmd_sec112():
    print("§11.2: identified interval of the mean gauche fraction given the exact athermal mean profile")
    print("       (engineering class tables; own DUAL LP; note's table in brackets)")
    note = {7: (0.595, 0.734), 9: (0.492, 0.787), 11: (0.407, 0.822), 13: (0.359, 0.834), 15: (0.324, 0.850),
            17: (0.294, 0.850), 19: (0.270, 0.850), 21: (0.247, 0.853), 23: (0.230, 0.851), 25: (0.211, 0.854),
            27: (0.201, 0.855)}
    for N in range(7, 28, 2):
        n = N - 3
        T = load_eng(n)
        h = np.array(T[:, :3], dtype=float); cnt = np.array(T[:, 3], dtype=float)
        gmin = np.array(T[:, 4], dtype=float); gmax = np.array(T[:, 6], dtype=float)
        m = (cnt[:, None] * h).sum(0) / cnt.sum()
        lo, _ = interval_dual(h, m, gmin)
        _, up = interval_dual(h, m, gmax)
        # athermal mean gauche count is not in the table (only gmin/gmax per class): bracket it
        print(f"  N={N:2d}: lower {lo / n:.3f} [{note[N][0]:.3f}]  upper {up / n:.3f} [{note[N][1]:.3f}]  "
              f"width {(up - lo) / n:.3f} [{note[N][1] - note[N][0]:.3f}]   classes {len(T)}; "
              f"ok: {abs(lo / n - note[N][0]) < 6e-4 and abs(up / n - note[N][1]) < 6e-4}")

def truth_weights(ch, kind, eps=1.0):
    m = ch["sa"]
    if kind == "athermal":
        w = np.ones(int(m.sum()))
    elif kind == "stiff":
        w = np.exp(-ch["g"][m].astype(float))
    elif kind == "attractive":
        w = np.exp(eps * ch["h"][m][:, 0].astype(float))
    return w / w.sum()

def cmd_sec111(n=10):
    ch = enumerate_chain(n)
    m = ch["sa"]; N = ch["N"]
    h = ch["h"][m].astype(float); g = ch["g"][m].astype(float); rg2 = ch["rg2"][m]; r2 = ch["r2"][m].astype(float)
    print(f"§11.1 ({N} beads, n={n}, {int(m.sum())} conformations): width of the model-free identified interval / a-priori range")
    print("   own enumeration; dual LP on un-aggregated conformations; note's values in brackets")
    note = {("rg2", "gauche"): (0.76, 0.73, 0.72), ("rg2", "r2"): (0.41, 0.45, 0.37), ("rg2", "decile"): (0.79, 0.57, 0.89),
            ("profile", "gauche"): (0.47, 0.26, 0.49), ("profile", "r2"): (0.59, 0.73, 0.50), ("profile", "decile"): (0.70, 0.29, 1.00),
            ("fullhist", "gauche"): (0.31, 0.14, 0.35), ("fullhist", "r2"): (0.22, 0.18, 0.21), ("fullhist", "decile"): (0.50, 0.20, 0.75)}
    # full pair-distance histogram over pairs with q - p >= 3 (definition read from the author's
    # dia_chain.py AFTER my own enumerator was written), and the compact decile by R_g^2
    X = ch["x"][m]
    iu = np.triu_indices(N, 3)
    d2all = ((X[:, iu[0], :] - X[:, iu[1], :]) ** 2).sum(-1)
    svals = np.unique(d2all)
    full = np.stack([(d2all == s).sum(1) for s in svals], axis=1).astype(float)
    thr = np.quantile(rg2, 0.10)
    decile = (rg2 <= thr).astype(float)
    print(f"   full histogram: {len(svals)} distinct squared distances; compact decile: R_g^2 <= {thr:.4f}, athermal population {decile.mean():.4f}")
    feats = {"rg2": rg2[:, None], "profile": h, "fullhist": full}
    targets = {"gauche": g / n, "r2": r2, "decile": decile}
    for fn, F in feats.items():
        for tn, tgt in targets.items():
            out = []
            for kind in ("athermal", "stiff", "attractive"):
                p = truth_weights(ch, kind)
                mm = p @ F
                lo, up = interval_dual(F, mm, tgt)
                out.append((up - lo) / (tgt.max() - tgt.min()))
            ref = note[(fn, tn)]
            print(f"   data {fn:8s} target {tn:7s}: " + " / ".join(f"{v:.2f}" for v in out)
                  + "   [" + " / ".join(f"{v:.2f}" for v in ref) + "]   "
                  f"match to 0.006: {all(abs(a - b) < 6e-3 for a, b in zip(out, ref))}")
    return ch

# ---------------------------------------------------------------- envelope class LPs
def neighbour_pairs(n):
    """Ordered pairs (x, y) of base-3 codes differing in exactly one digit."""
    P = 3 ** n
    xs, ys = [], []
    codes = np.arange(P)
    for pos in range(n):
        base = 3 ** pos
        dig = (codes // base) % 3
        for delta in (1, 2):
            y = codes + ((dig + delta) % 3 - dig) * base
            xs.append(codes); ys.append(y)
    return np.concatenate(xs), np.concatenate(ys)

def envelope_lp(ch, b, feat=None, m=None, target=None, sense=+1, allpairs=False):
    """Variables w >= 0 on torsion patterns.  Cone: w(y) <= e^{b d_H(x,y)} w(x).
    Normalisation: mean of w over conformations = 1 (so mu = w/|SA| on conformations for an
    athermal model).  Optional data: sum_SA w (feat - m) = 0.  Objective: sense * mean_SA(w target).
    Returns (status, value).  allpairs=True: variables only on conformations, constraints for
    ALL ordered pairs with the Hamming distance of the torsion patterns (independent formulation)."""
    n = ch["n"]; P = 3 ** n
    order = np.argsort(ch["code"])                      # position of code c in arrays
    sa_by_code = ch["sa"][order]
    nSA = int(sa_by_code.sum())
    if not allpairs:
        xs, ys = neighbour_pairs(n)
        rows = np.arange(len(xs))
        Aub = sp.csr_matrix((np.concatenate([np.ones(len(xs)), -math.exp(b) * np.ones(len(xs))]),
                             (np.concatenate([rows, rows]), np.concatenate([ys, xs]))), shape=(len(xs), P))
        nv = P
        sa_idx = np.nonzero(sa_by_code)[0]
    else:
        sa_idx_codes = np.nonzero(sa_by_code)[0]
        digs = np.array([[(c // 3 ** pos) % 3 for pos in range(n)] for c in sa_idx_codes])
        dH = (digs[:, None, :] != digs[None, :, :]).sum(-1)
        I, Jx = np.nonzero(dH > 0)
        rows = np.arange(len(I))
        Aub = sp.csr_matrix((np.concatenate([np.ones(len(I)), -np.exp(b * dH[I, Jx])]),
                             (np.concatenate([rows, rows]), np.concatenate([Jx, I]))), shape=(len(I), nSA))
        nv = nSA
        sa_idx = np.arange(nSA)
    bub = np.zeros(Aub.shape[0])
    # equality rows
    eq_rows = [np.zeros(nv)]
    eq_rows[0][sa_idx] = 1.0 / nSA
    beq = [1.0]
    def on_sa(vec_sa_order_code):
        r = np.zeros(nv); r[sa_idx] = vec_sa_order_code / nSA; return r
    if feat is not None:
        Fc = feat[order][sa_by_code]                    # features in code order, conformations only
        sc = np.maximum(np.abs(Fc - m).max(0), 1e-12)
        for k in range(Fc.shape[1]):
            eq_rows.append(on_sa((Fc[:, k] - m[k]) / sc[k])); beq.append(0.0)
    c = np.zeros(nv)
    if target is not None:
        c = -sense * on_sa(target[order][sa_by_code])
    res = None
    for method in ("highs", "highs-ds", "highs-ipm"):
        res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=np.array(eq_rows), b_eq=np.array(beq),
                      bounds=[(0, None)] * nv, method=method)
        if res.status in (0, 2):
            break
    if res.status == 2:
        return "infeasible", None
    assert res.status == 0, res.message
    return "ok", (-res.fun * sense if target is not None else 0.0)

def full(ch, key):
    """Feature arrays indexed like ch arrays (all patterns; garbage on non-SA rows is unused)."""
    return ch[key].astype(float)

def bmin(ch, feat, m, lo=0.0, hi=8.0, tol=2e-4, allpairs=False):
    st, _ = envelope_lp(ch, hi, feat, m, allpairs=allpairs)
    assert st == "ok", "data infeasible even at large b"
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        st, _ = envelope_lp(ch, mid, feat, m, allpairs=allpairs)
        if st == "ok":
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def single_flip_constant(ch, values):
    """Largest |values(x) - values(y)| over conformations x, y differing in one torsion."""
    n = ch["n"]
    order = np.argsort(ch["code"]); sa = ch["sa"][order]; v = values[order]
    xs, ys = neighbour_pairs(n)
    ok = sa[xs] & sa[ys]
    return float(np.max(np.abs(v[xs[ok]] - v[ys[ok]])))

def cmd_sec9():
    print("§9: falsification thresholds.  Model athermal; data = exact averages under truth ~ exp(+eps c3)")
    note = {8: {"rg2": (0.068, 0.150, 0.360), "profile": (0.220, 0.438, 0.866), "const": (0.25, 0.5, 1.0)},
            9: {"rg2": (0.079, 0.176, 0.436), "profile": (0.240, 0.482, 0.952), "const": (0.5, 1.0, 2.0)}}
    for N in (8, 9):
        n = N - 3
        ch = enumerate_chain(n)
        msk = ch["sa"]
        c3 = ch["h"][:, 0].astype(float)
        feats = {"rg2": np.where(msk, ch["rg2"], 0.0)[:, None], "profile": np.where(msk[:, None], ch["h"], 0).astype(float)}
        for name, F in feats.items():
            vals = []
            for eps in (0.25, 0.5, 1.0):
                p = truth_weights(ch, "attractive", eps)
                m = p @ F[msk]
                vals.append(bmin(ch, F, m))
            sf = single_flip_constant(ch, c3)
            print(f"  N={N} data={name:8s}: b_min = " + " / ".join(f"{v:.3f}" for v in vals)
                  + "   [note: " + " / ".join(f"{v:.3f}" for v in note[N][name]) + "]"
                  + f"   match to 0.002: {all(abs(a - b) < 2e-3 for a, b in zip(vals, note[N][name]))}"
                  + f";  truth's single-flip constant = eps x {sf:.0f}")
        if N == 8:
            # independent formulation: all ordered pairs of conformations, Hamming distance
            F = feats["profile"]
            p = truth_weights(ch, "attractive", 0.5); m = p @ F[msk]
            v2 = bmin(ch, F, m, hi=2.0, allpairs=True)
            print(f"  N=8 profile, eps=0.5, ALL-PAIRS formulation on conformations only: b_min = {v2:.3f}")

def cmd_sec114():
    print("§11.4 (9 beads): model = truth = athermal; envelope b per torsion; own LP (Charnes-Cooper form)")
    ch = enumerate_chain(6)
    msk = ch["sa"]; n = 6
    g = np.where(msk, ch["g"], 0).astype(float) / n
    r2 = np.where(msk, ch["r2"], 0).astype(float)
    H = np.where(msk[:, None], ch["h"], 0).astype(float)
    p = truth_weights(ch, "athermal"); m = p @ H[msk]
    note = {"gauche": ((0.420, 0.825), (0.492, 0.787), (0.607, 0.701), (0.629, 0.677)),
            "r2": ((31.0, 69.4), (16.5, 77.6), (38.2, 53.9), (42.1, 49.9))}
    for name, tgt in (("gauche", g), ("r2", r2)):
        true = float(p @ tgt[msk])
        res = []
        for label, b, F in (("envelope b=1 only", 1.0, None), ("profile only", None, H), ("both b=1", 1.0, H), ("both b=0.5", 0.5, H)):
            if b is None:
                lo, up = interval_dual(H[msk], m, tgt[msk])
            else:
                lo = envelope_lp(ch, b, F, m if F is not None else None, tgt, sense=-1)[1]
                up = envelope_lp(ch, b, F, m if F is not None else None, tgt, sense=+1)[1]
            res.append((lo, up))
        print(f"  target {name} (true {true:.3f}): " + "  ".join(f"[{a:.3f}, {b_:.3f}]" for a, b_ in res))
        print(f"  {'':8s} note:          " + "  ".join(f"[{a:.3f}, {b_:.3f}]" for a, b_ in note[name]))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tables"
    if cmd == "tables":
        cmd_tables(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    elif cmd == "sec112":
        cmd_sec112()
    elif cmd == "sec111":
        cmd_sec111(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    elif cmd == "sec9":
        cmd_sec9()
    elif cmd == "sec114":
        cmd_sec114()
