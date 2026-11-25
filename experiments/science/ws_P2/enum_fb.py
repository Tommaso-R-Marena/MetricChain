"""
Exact enumeration of a fixed-backbone rotamer model.

usage: python3 -B enum_fb.py SEQ BB [--grid R3|R2|R3c] [--tau 0.60] [--maxconf 3e6] [--threads 1] [--ffs ff03,ff15ipq,ff99SB]

SEQ : one-letter sequence, or a homopolymer shorthand like S6, V12, K4 (letter + length), or
      LKSE*2 (pattern * repeats) / LKSE:6 (pattern repeated and truncated to 6 residues)
BB  : name in fbmodel.BACKBONES (H, E, P2, Hp, Ep, P2p)

Domain enumerated: the product over sites of the states whose ONE-SITE clash score exceeds
--tau (use the smallest threshold that will be analysed; larger thresholds and the pair-clash
filter are applied afterwards as masks, the scores are stored).

Output: data/fb_<SEQ>_<BB>_<grid>_t<tau>.npz with flat C-ordered arrays over the product
(axis i = site i): gb (GBn2 polarisation energy), tors, lj, coul (ff14SB vacuum components),
<ff> (total vacuum energy of each extra force field, same coordinates; bonds and angles are
constant and omitted), s1min, s2min (min one-site / two-site clash score of the assignment).
All energies in kcal/mol.
"""
import sys, os, time, math, re
import numpy as np
from fbmodel import FBModel, BACKBONES

HERE = os.path.dirname(os.path.abspath(__file__))


def expand_seq(s):
    m = re.fullmatch(r"([A-Z])(\d+)", s)
    if m:
        return m.group(1) * int(m.group(2))
    m = re.fullmatch(r"([A-Z]+)\*(\d+)", s)
    if m:
        return m.group(1) * int(m.group(2))
    m = re.fullmatch(r"([A-Z]+):(\d+)", s)
    if m:
        pat, n = m.group(1), int(m.group(2))
        return (pat * (n // len(pat) + 1))[:n]
    return s


def tagname(seqarg, bb, grid, tau):
    return f"fb_{seqarg.replace('*', 'x').replace(':', 'c')}_{bb}_{grid}_t{tau:.2f}"


def main():
    a = sys.argv[1:]
    seqarg, bb = a[0], a[1]
    opt = lambda k, d: (a[a.index(k) + 1] if k in a else d)
    grid = opt("--grid", "R3")
    tau = float(opt("--tau", "0.60"))
    maxconf = float(opt("--maxconf", "3e6"))
    threads = int(opt("--threads", "1"))
    ffs = tuple(x for x in opt("--ffs", "ff03,ff15ipq,ff99SB").split(",") if x)
    seq = expand_seq(seqarg)
    t0 = time.time()
    Mdl = FBModel(seq, bb, grid=grid, extra_ffs=ffs, threads=threads)
    P, F = Mdl.P, Mdl.F
    dom = Mdl.domain(tau)
    shape = [len(d) for d in dom]
    total = int(np.prod(shape, dtype=np.float64)) if min(shape) > 0 else 0
    print(f"{seqarg} = {seq} on {bb} {BACKBONES[bb]}, grid {grid}: atoms {P.natoms}, sites {Mdl.ns}, states/site {Mdl.k}; "
          f"fixed-atom clash score {Mdl.s_fixed:.3f}; one-site domain sizes at tau={tau}: {shape}; product {total}", flush=True)
    if total == 0:
        print("EMPTY domain: some site has no state with one-site clash score above the threshold.")
        return
    if total > maxconf:
        print(f"too large (> {maxconf:.0f}); not enumerated")
        return
    st = Mdl.product_states(dom)
    out = {}
    for c in ("tors", "lj", "coul"):
        out[c] = Mdl.table_energy(st, "ff14SB", (c,))
    for ff in ffs:
        out[ff] = Mdl.table_energy(st, ff)
    s1 = np.full(total, np.inf)
    for i in range(Mdl.ns):
        s1 = np.minimum(s1, Mdl.s1[i][st[:, i]])
    out["s1min"] = s1
    out["s2min"] = Mdl.pair_clash_of(st)
    t1 = time.time()
    gb = np.empty(total)
    step = 16384
    for s in range(0, total, step):
        gb[s:s + step] = Mdl.gb_energy(st[s:s + step])
        if (s // step) % 8 == 0:
            print(f"   GB {min(total, s + step)}/{total}  {time.time() - t1:.0f}s", flush=True)
    out["gb"] = gb
    t2 = time.time()
    # spot checks: 24 random assignments against P's FastFF (double), 4 against OpenMM (CPU platform, single precision)
    rng = np.random.default_rng(2026)
    pick = rng.choice(total, size=min(24, total), replace=False)
    X = Mdl.assemble(st[pick])
    with np.errstate(divide="ignore"):
        Ef = F.energies(X, gb=("gbn2",))
    dv = {"gb": np.abs(Ef["gbn2"] - gb[pick]).max(), "tors": np.abs(Ef["tors"] - out["tors"][pick]).max(),
          "lj_rel": (np.abs(Ef["lj"] - out["lj"][pick]) / np.maximum(1.0, np.abs(Ef["lj"]))).max(),
          "coul": np.abs(Ef["coul"] - out["coul"][pick]).max(),
          "clash": np.abs(Ef["clash"] - np.minimum(np.minimum(s1[pick], out["s2min"][pick]), Mdl.s_fixed)).max()}
    for ff in ffs:
        tot = Ef[ff + "_tors"] + Ef[ff + "_lj"] + Ef[ff + "_coul"]
        dv[ff + "_rel"] = (np.abs(tot - out[ff][pick]) / np.maximum(1.0, np.abs(tot))).max()
    Eo = P.energies(X[:4])
    dv["gb_vs_OpenMM_CPU"] = np.abs(Eo["gbn2"] - gb[pick[:4]]).max()
    print("   spot checks (max abs deviation, kcal/mol; _rel = relative): " + ", ".join(f"{k} {v:.1e}" for k, v in dv.items()), flush=True)
    assert dv["gb"] < 1e-8 and dv["coul"] < 1e-8 and dv["clash"] < 1e-9
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    tag = tagname(seqarg, bb, grid, tau)
    ca = np.array([Mdl.X0[P.idx[(k, "CA")]] for k in Mdl.sites])
    cb = np.array([Mdl.X0[P.idx[(k, "CB")]] for k in Mdl.sites])
    chi_tab = np.full((Mdl.ns, max(Mdl.k), 4), np.nan)
    for i in range(Mdl.ns):
        arr = np.array(Mdl.states[i], dtype=float).reshape(Mdl.k[i], -1)
        chi_tab[i, :Mdl.k[i], :arr.shape[1]] = arr
    np.savez(os.path.join(HERE, "data", tag + ".npz"), seq=seq, bb=bb, grid=grid, tau_enum=tau, shape=np.array(shape),
             dom_flat=np.concatenate(dom), dom_off=np.cumsum([0] + shape), s_fixed=Mdl.s_fixed, sites=np.array(Mdl.sites),
             CA=ca, CB=cb, chi_tab=chi_tab, natoms=P.natoms, ffs=np.array(ffs),
             s1_flat=np.concatenate([Mdl.s1[i][dom[i]] for i in range(Mdl.ns)]), **out)
    print(f"   done: {total} assignments; setup+tables {t1 - t0:.1f}s, GB {t2 - t1:.1f}s ({1e6 * (t2 - t1) / total:.0f} us/conf); "
          f"pair-clash-free at 0.70: {int((out['s2min'] > 0.70).sum())}, at {tau}: {int((out['s2min'] > tau).sum())}; -> data/{tag}.npz", flush=True)


if __name__ == "__main__":
    main()
