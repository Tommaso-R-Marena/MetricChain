"""
P6 step 5: the certified sandwich for a LONG chain (no enumeration possible): site form (P3) and banded pair form
at band w, from the ball of radius m-1 (cache written by p6_03a_ball.py or evaluated here if small) and the
in-band pair sums (closed form; out-of-band shares through the double-counting identity).  Then N exact samples of
pi_{m_-} (banded pair form), E evaluated at each: m_- <= E <= m_+ checked at every sampled state.

usage: python3 -B p6_03_reach.py SEQ BB TAU m [--w 8] [--bands 8,4,2] [--ref VALUE] [--N 1000] [--seed S]
"""
import sys, os, time, math, json
import numpy as np
import p6lib as L
pw = L.pw
BETA = L.BETA


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


a = sys.argv[1:]
seq, bb, tau, m = a[0], a[1], float(a[2]), int(a[3])
W = opt(a, "--w", 8, int)
bands = [int(v) for v in opt(a, "--bands", str(W)).split(",")]
ref = opt(a, "--ref", None, float)
N = opt(a, "--N", 1000, int)
seed = opt(a, "--seed", 20261126, int)
M = m - 1
t0 = time.time()
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
n, k = G.ns, G.k
size_log10 = float(sum(math.log10(v) for v in k))
print(f"=== reach: {seq} on {bb}, tau {tau}, order m = {m}: atoms {G.nat}, sites {n}, states/site {min(k)}..{max(k)}, |X| = 10^{size_log10:.2f}; "
      f"anchor {''.join(map(str, x0))} E = {E0:.6f} kcal/mol; bands {bands} [{time.time() - t0:.1f}s]", flush=True)
res = dict(seq=seq, bb=bb, tau=tau, m=m, n=n, natoms=int(G.nat), log10_size=size_log10, anchor=list(x0), E_anchor=E0, bands={}, ref=ref)
t1 = time.time()
sup = L.EnvelopeSup(G)
GF = L.GFBound2(G, x0, sup, K=m)
Gam, S, Gp, srcp = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, "gbn2", m, verbose=True, w=W)
ninband = int(np.isfinite(Gp).sum() - 0) // 2
print(f"    Gamma_{m} = {Gam:.6e} kcal/mol = {Gam * BETA:.4f} kT; pair sums: {srcp}; pair sums available for {ninband} pairs; "
      f"max S_i/m = {S.max() / m:.4e}, max G_ij/C(m,2) = {np.nanmax(Gp) / math.comb(m, 2):.4e} [{time.time() - t1:.1f}s]", flush=True)
res.update(Gamma=Gam, t_pairsums=time.time() - t1, pairsums=srcp)
t1 = time.time()
d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau)
print(f"    ball of radius {M}: {nball} values of g ({srcb if 'evaluated' in srcb else 'read from ' + os.path.basename(srcb)}) [{time.time() - t1:.1f}s]", flush=True)
res.update(nball=int(nball), t_ball=time.time() - t1, ball_src=os.path.basename(srcb))
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
keep = None
for w in bands:
    RW = {}
    for form in ("S", "B"):
        t1 = time.time()
        if form == "S":
            gs, g2 = L.site_form(n, m, S, phi1), np.zeros((n, n))
        else:
            gs, g2 = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
        lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)
        lnZlo, lnZup = lo.lnZ(), up.lnZ()
        diff = L.diff_model(lo, up)
        rho = diff.maximum()
        Eu, Eu2 = lo.moments(diff)
        RW[form] = dict(lnZ_lo=lnZlo, lnZ_up=lnZup, width=lnZlo - lnZup, rho_cert=rho, mean_u=BETA * Eu, min_lo=lo.minimum(), min_up=up.minimum())
        inside = "" if ref is None else f"; independent estimate {ref:.4f} inside: {lnZup <= ref <= lnZlo}"
        print(f"    w = {w:2d} form {form}: CERTIFIED ln Z(E) in [{lnZup:.6f}, {lnZlo:.6f}], width {lnZlo - lnZup:.6f} nats; rho_cert = {rho * BETA:.4f} kT; "
              f"E_(pi-) u = {BETA * Eu:.4e}; min m_- = {RW[form]['min_lo']:.6f}, min m_+ = {RW[form]['min_up']:.6f}{inside} [{time.time() - t1:.1f}s]", flush=True)
        if form == "B" and keep is None:
            keep = (lo, up, w)
    res["bands"][str(w)] = RW
if N > 0:
    lo, up, w = keep
    t1 = time.time()
    rng = np.random.default_rng(seed)
    Ssam = lo.sample(N, rng)
    uniq, inv = np.unique(Ssam, axis=0, return_inverse=True)
    inv = np.asarray(inv).reshape(-1)
    gU = np.empty(len(uniq))
    for s in range(0, len(uniq), 2048):
        gU[s:s + 2048] = G.bulk_energy(uniq[s:s + 2048])
    ES = (pw.f_energy(uniq, c0, h, J) + gU)[inv]
    ml, mu = lo.energy(Ssam), up.energy(Ssam)
    vl, vu = int((ES < ml - 1e-9).sum()), int((ES > mu + 1e-9).sum())
    r = BETA * (ES - ml)
    res.update(sample=dict(N=N, seed=seed, distinct=int(len(uniq)), viol_lower=vl, viol_upper=vu, r_mean=float(r.mean()), r_max=float(r.max()),
                           u_mean=float((BETA * (mu - ml)).mean()), mean_changed=float((Ssam != np.array(x0)[None]).sum(1).mean()), band=w))
    print(f"    SAMPLED CHECK (band {w}, form B): {N} exact samples of pi_(m_-) (seed {seed}; {len(uniq)} distinct; mean number of sites off the anchor "
          f"{res['sample']['mean_changed']:.2f}), E evaluated at each [{time.time() - t1:.1f}s]: m_- > E: {vl}, m_+ < E: {vu}; "
          f"beta(E - m_-): mean {r.mean():.3e}, max {r.max():.3e}; mean beta(m_+ - m_-) = {res['sample']['u_mean']:.3e}", flush=True)
res["seconds"] = time.time() - t0
fn = os.path.join(L.HERE, "out", f"reach_{L.tagname(seq, bb, tau)}_m{m}.json")
json.dump(res, open(fn, "w"), indent=1)
print(f"    -> {os.path.relpath(fn, L.HERE)}")
print(f"DONE p6_03_reach {seq} {bb} {tau} m={m} [{time.time() - t0:.0f}s]", flush=True)
