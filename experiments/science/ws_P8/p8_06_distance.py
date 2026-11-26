"""
P8 step 2 -- monopoles: how the many-body terms of a peptide too large to enumerate depend on distance and on charge.

For a 12-residue peptide (anchor: P3's ICM anchor), everything EXACT evaluations of the model at named states:

(B) third-order anchored terms in the ANCHOR CONTEXT, for every triple T of sites:
        M_T = max over y_T of |d_T(y_T)|,   d_T(y_T) = Delta_T g(x0; y_T)
    (a lower bound of the anchored constant c_T^anch, which also takes the supremum over the contexts), from the
    energies on the full grid of the three sites with all other sites at the anchor;
(C) the response of ONE GROUP's own solvation energy to changes at OTHER sites.  For a group A of atoms (per residue:
    its fixed backbone part, its charged head group, its aliphatic chain, or its neutral side chain; the group's own
    site stays at the anchor, so the group is rigid and only its Born radii change),
        E_A(x) = sum_{p <= q in A} t_pq(x)                        (self terms and the pairs inside the group),
        R1[A, j]    = max over y_j        of |E_A(x0; j -> y_j) - E_A(x0)|              (first-order response to site j)
        R2[A, j, k] = max over y_j, y_k   of |Delta_{jk} E_A(x0; y_j, y_k)|             (second-order: a 3-body term)
    with the distance between the centroid of A and the centroid of the moving atoms of site j at the maximising state.

usage: python3 -B p8_06_distance.py SEQ BB TAU [--budget SECONDS]
writes logs/dist_<tag>.log, out/dist_<tag>.npz
"""
import sys, os, time, itertools
import numpy as np
from p8lib import *
import pwmodel as pw

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"dist_{tag}.npz")) and "--force" not in a:
    print(f"out/dist_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"dist_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"dist_{tag}.log"), append=resume)
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat; k = list(G.k)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = np.array([int(v) for v in x0])
cls, letter = atom_classes(G)
fg, fgnames = fine_groups(G)
site_of = -np.ones(N, dtype=int)
for i in range(n):
    site_of[G.mov[i]] = i
names = list(G.P.names); resid = np.asarray(G.P.resid)
Xa = G.coords(x0[None])[0]
CA = np.array([Xa[[p for p in range(N) if names[p] == "CA" and resid[p] == G.fb.sites[i]][0]] for i in range(n)])
restype = [THREE.get(G.P.seq[G.fb.sites[i] - 1], G.P.seq[G.fb.sites[i] - 1]) for i in range(n)]
log(f"=== p8_06_distance: {seq} on {bb}, tau {tau}: {N} atoms, {n} sites ({''.join(restype)}), states per site {k}; anchor (ICM) {tuple(int(v) for v in x0)}" + ("; RESUMING" if resume else ""))

# ------------------------------------------------------------------ (C) group responses (cheap: Born radii only)
t1 = time.time()
nG = fg.max() + 1
gatoms = [np.flatnonzero(fg == a_) for a_ in range(nG)]
ghost = np.array([site_of[ga[0]] for ga in gatoms])
gq = np.array([G.q[ga].sum() for ga in gatoms]); gabsq = np.array([np.abs(G.q[ga]).sum() for ga in gatoms])
gcls = np.array([cls[ga[0]] for ga in gatoms])
gcen = np.array([Xa[ga].mean(axis=0) for ga in gatoms])


def group_energies(st):
    """E_A at the states st (M, n) for every group A, with the intra-group distances of the ANCHOR state: (M, nG).
    Only meaningful where the host of A is at its anchor state."""
    B = 1.0 / G.invB(G.descreening(st))
    out = np.zeros((st.shape[0], nG))
    for a_, ga in enumerate(gatoms):
        d = Xa[ga][:, None, :] - Xa[ga][None, :, :]
        r2 = (d * d).sum(-1)
        BB = B[:, ga][:, :, None] * B[:, ga][:, None, :]
        Mk = 1.0 / np.sqrt(r2[None] + BB * np.exp(-r2[None] / (4.0 * BB)))
        qq = G.q[ga][:, None] * G.q[ga][None, :]
        out[:, a_] = 0.5 * PRE * (qq[None] * Mk).sum(axis=(1, 2))
    return out


EA0 = group_energies(x0[None])[0]
R1 = np.zeros((nG, n)); D1 = np.full((nG, n), np.nan); S1 = np.zeros((nG, n))
single = {}
for j in range(n):
    st = np.tile(x0, (k[j], 1)); st[:, j] = np.arange(k[j])
    EA = group_energies(st) - EA0[None]                    # (k_j, nG)
    single[j] = EA
    Xj = G.Xm[j]                                           # (k_j, n_j, 3)
    cen_j = Xj.mean(axis=1)
    for a_ in range(nG):
        if ghost[a_] == j:
            continue
        y = int(np.argmax(np.abs(EA[:, a_])))
        R1[a_, j] = abs(EA[y, a_]); S1[a_, j] = EA[y, a_]
        D1[a_, j] = float(np.linalg.norm(gcen[a_] - cen_j[y]))
R2 = np.zeros((nG, n, n))
for j in range(n):
    for l in range(j + 1, n):
        grid = np.stack(np.meshgrid(np.arange(k[j]), np.arange(k[l]), indexing="ij"), axis=-1).reshape(-1, 2)
        st = np.tile(x0, (len(grid), 1)); st[:, j] = grid[:, 0]; st[:, l] = grid[:, 1]
        EA = (group_energies(st) - EA0[None]).reshape(k[j], k[l], nG)
        D2 = EA - single[j][:, None, :] - single[l][None, :, :]
        v = np.abs(D2).reshape(-1, nG).max(axis=0)
        for a_ in range(nG):
            if ghost[a_] not in (j, l):
                R2[a_, j, l] = R2[a_, l, j] = v[a_]
log(f"(C) group responses done: {nG} groups, {time.time() - t1:.0f} s")
log("    group | net charge | sum|q| | first-order response R1 to the nearest other site and to the farthest (kcal/mol; centroid distance nm)")
for a_ in range(nG):
    ok = np.flatnonzero(~np.isnan(D1[a_]))
    if not len(ok):
        continue
    jn = ok[np.argmin(D1[a_][ok])]; jf = ok[np.argmax(D1[a_][ok])]
    log(f"    {fgnames[a_]:10s} {gq[a_]:+.3f} {gabsq[a_]:.3f} | nearest: site {jn} at {D1[a_, jn]:.2f} nm, R1 = {R1[a_, jn]:.3e} | farthest: site {jf} at {D1[a_, jf]:.2f} nm, R1 = {R1[a_, jf]:.3e}")

# ------------------------------------------------------------------ (B) all triples in the anchor context
triples = [T for T in itertools.combinations(range(n), 3) if all(k[i] >= 2 for i in T)]
nT = len(triples)
if resume:
    z = np.load(ckpt); i_next = int(z["i_next"]); MT = z["MT"]; YT = z["YT"]; SG = z["SG"]
    log(f"    checkpoint read: triples 0..{i_next - 1} done")
else:
    i_next = 0; MT = np.zeros(nT); YT = np.zeros((nT, 3), dtype=int); SG = np.zeros(nT)
tlast = time.time(); stopped = False; nev_ = 0
for i in range(i_next, nT):
    T = triples[i]
    grid = np.stack(np.meshgrid(*[np.arange(k[s]) for s in T], indexing="ij"), axis=-1).reshape(-1, 3)
    st = np.tile(x0, (len(grid), 1))
    for c_, s in enumerate(T):
        st[:, s] = grid[:, c_]
    g = np.concatenate([G.bulk_energy(st[s0:s0 + 2048]) for s0 in range(0, len(st), 2048)]).reshape([k[s] for s in T])
    nev_ += len(st)
    D = g
    for ax, s in enumerate(T):
        D = D - np.take(D, [x0[s]], axis=ax)
    idx = int(np.argmax(np.abs(D)))
    MT[i] = float(np.abs(D).reshape(-1)[idx]); SG[i] = float(D.reshape(-1)[idx]); YT[i] = np.unravel_index(idx, D.shape)
    now = time.time()
    if now - tlast > 60 or i == nT - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, i_next=i + 1, MT=MT, YT=YT, SG=SG); os.replace(tmp, ckpt); tlast = now
        log(f"    triple {i + 1}/{nT} done ({nev_} evaluations in this run), checkpoint written, {now - t0:.0f} s")
    if now - t0 > BUDGET and i < nT - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at triple {i + 1}/{nT}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
dCA = np.linalg.norm(CA[:, None, :] - CA[None, :, :], axis=-1)
span = np.array([T[2] - T[0] for T in triples])
diam = np.array([max(dCA[T[0], T[1]], dCA[T[0], T[2]], dCA[T[1], T[2]]) for T in triples])
chargedT = np.array([sum(1 for s in T if restype[s] in HEAD) for T in triples])
log(f"(B) {nT} triples done; sum of M_T = {MT.sum():.4f} kcal/mol; largest {MT.max():.4f} at T = {triples[int(np.argmax(MT))]}")
log("    by sequence span (last - first site): number | sum of M_T | mean | max   (kcal/mol)")
for s_ in sorted(set(span.tolist())):
    mk = span == s_
    log(f"      span {s_:2d}: {int(mk.sum()):3d} | {MT[mk].sum():.4e} | {MT[mk].mean():.4e} | {MT[mk].max():.4e}")
if len(set(chargedT.tolist())) > 1:
    log("    by the number of charged side chains in T: number | sum | mean | median")
    for c_ in sorted(set(chargedT.tolist())):
        mk = chargedT == c_
        log(f"      {c_} charged: {int(mk.sum()):3d} | {MT[mk].sum():.4e} | {MT[mk].mean():.4e} | {np.median(MT[mk]):.4e}")
np.savez_compressed(os.path.join(HERE, "out", f"dist_{tag}.npz"), triples=np.array(triples), MT=MT, YT=YT, SG=SG, dCA=dCA, span=span, diam=diam, chargedT=chargedT,
                    restype=np.array(restype), anchor=x0, k=np.array(k), R1=R1, S1=S1, D1=D1, R2=R2, gq=gq, gabsq=gabsq, gcls=gcls, ghost=ghost, gcen=gcen,
                    gnames=np.array(fgnames), CA=CA)
log.done()
