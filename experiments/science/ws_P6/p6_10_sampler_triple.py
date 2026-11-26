"""
P6: the sandwich sampler (theory division, Proposition 11.113; see p6_04_sampler.py) on the TRIPLE-share sandwich
of p6_09_triple.py.  Same algorithm, same rounding treatment, same output as p6_04_sampler.py (functions imported).
usage: python3 -B p6_10_sampler_triple.py SEQ BB TAU m w [--N 50000] [--N1 1200] [--seed S]
"""
import sys, os, time, math, json, glob
import numpy as np
import p6lib as L
import p6_04_sampler as SMP
import p6_09_triple as TR
pw = L.pw; BETA = L.BETA

a = sys.argv[1:]
seq, bb, tau, m, w = a[0], a[1], float(a[2]), int(a[3]), int(a[4])
N = SMP.opt(a, "--N", 50000, int); N1 = SMP.opt(a, "--N1", 1200, int)
delta = 0.05
seed = SMP.opt(a, "--seed", 2026112600 + 10 * m + 2, int)
t0 = time.time()
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
n, k = G.ns, G.k
sup = L.EnvelopeSup(G); GF = L.GFBound2(G, x0, sup, K=m)
Gam, S, Gp, srcp = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, "gbn2", m)
z = np.load(os.path.join(L.HERE, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz"))
val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
tris = TR.window_triples(n, w)
se, cr = L.GFBatch(GF).totals(m, tris)
H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(t3)
     for tr, t3 in zip(tris, se + cr)}
M = m - 1
d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
gsT, g2T, eta = TR.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
lo, up = TR.build_triple_models(k, x0, c0, h, J, d, w, M, gsT, g2T, eta)
diff = TR.diff_triple(lo, up)
lnZlo, lnZup = lo.lnZ(), up.lnZ()
D = lnZlo - lnZup
acc_rate = -math.expm1(-D)
print(f"=== sandwich sampler on the TRIPLE-share sandwich: {seq} on {bb}, tau {tau}, m = {m}, window {w}; ball {nball} values; ln Z(m_-) = {lnZlo:.6f}, "
      f"ln Z(m_+) = {lnZup:.6f}, D = {D:.6f} nats; exact acceptance rate {acc_rate:.5f}; seed {seed}; delta {delta} [{time.time() - t0:.1f}s]", flush=True)
rng = np.random.default_rng(seed)
batch = int(min(400000, max(20000, 2000 / max(acc_rate, 1e-6))))
t1 = time.time()
Sacc, U, nprop = SMP.propose_accept(lo, diff, N, rng, batch)
uniq, inv = np.unique(Sacc, axis=0, return_inverse=True); inv = np.asarray(inv).reshape(-1)
print(f"    {N} accepted of {nprop} proposals (observed acceptance {N / nprop:.5f}) [{time.time() - t1:.1f}s]; {len(uniq)} distinct states; "
      f"mean number of sites off the anchor among accepted points {float((Sacc != np.array(x0)[None]).sum(1).mean()):.2f}", flush=True)
t1 = time.time()
known = {}
tg = L.tagname(seq, bb, tau)
for cf in sorted(glob.glob(os.path.join(L.P3, "cache", f"ball_{tg}_M*.npz")) + glob.glob(os.path.join(L.MYCACHE, f"ball_{tg}_M*.npz"))
                 + glob.glob(os.path.join(L.MYCACHE, f"evalcache_{tg}_*.npz"))):
    zz = np.load(cf)
    for row, v in zip(zz["states"].astype(np.int8), zz["vals"]):
        known[row.tobytes()] = float(v)
u8 = uniq.astype(np.int8)
gU = np.array([known.get(row.tobytes(), np.nan) for row in u8])
todo = np.flatnonzero(np.isnan(gU))
print(f"      {len(uniq) - len(todo)} of the {len(uniq)} distinct states already have a value of g on disk; {len(todo)} new evaluations", flush=True)
for s in range(0, len(todo), 4096):
    ii = todo[s:s + 4096]
    gU[ii] = G.bulk_energy(uniq[ii])
if len(todo):
    np.savez(os.path.join(L.MYCACHE, f"evalcache_{tg}_m{m}_T_w{w}_seed{seed}.npz"), states=u8[todo], vals=gU[todo])
chk = np.random.default_rng(seed + 7).integers(0, len(uniq), 24)
dev = float(np.abs(gU[chk] - G.energy(uniq[chk])).max()); assert dev < 1e-8, dev
ES = (pw.f_energy(uniq, c0, h, J) + gU)[inv]
mlS, muS = lo.energy(Sacc), up.energy(Sacc)
r = BETA * (ES - mlS); Us = BETA * (muS - mlS)
vl, vu = int((ES < mlS - 1e-9).sum()), int((ES > muS + 1e-9).sum())
W, dW = SMP.w_values(r, Us)
res = dict(seq=seq, bb=bb, tau=tau, m=m, form="T", w=w, seed=seed, delta=delta, lnZ_lo=lnZlo, lnZ_up=lnZup, D=D, acc_rate_exact=acc_rate, nball=int(nball),
           N=N, proposals=nprop, emp_acc=N / nprop, distinct=int(len(uniq)), new_evals=int(len(todo)), viol_lower=vl, viol_upper=vu,
           W_min=float(W.min()), W_max=float(W.max()), W_outside=int(((W < 0) | (W > 1)).sum()), dW_mean=float(dW.mean()), brackets={})
print(f"    E evaluated at the accepted points [{time.time() - t1:.1f}s]; m_- <= E <= m_+ at all {N} accepted points: violations below {vl}, above {vu}; "
      f"W in [{W.min():.6f}, {W.max():.6f}] (outside [0,1]: {res['W_outside']}); mean rounding half-width of W {dW.mean():.1e}", flush=True)
for NN in sorted({min(N1, N), N}):
    b0, b1, t, pt = SMP.bracket(W[:NN], dW[:NN], lnZlo, lnZup, delta)
    res["brackets"][str(NN)] = dict(lo=b0, hi=b1, width=b1 - b0, t=t, point=pt, Wmean=float(W[:NN].mean()), Wstd=float(W[:NN].std(ddof=1)),
                                    predicted_width_bound=math.expm1(D) * 2 * t)
    print(f"    N = {NN:6d} (the first {NN} accepted points): mean W = {W[:NN].mean():.6f} (std {W[:NN].std(ddof=1):.4f}); t = {t:.6f}; "
          f"CERTIFIED (prob. >= {1 - delta}): ln Z(E) in [{b0:.6f}, {b1:.6f}], width {b1 - b0:.3e} nats (bound (e^D - 1) 2t = {math.expm1(D) * 2 * t:.3e}); point estimate {pt:.6f}", flush=True)
res["seconds"] = time.time() - t0
json.dump(res, open(os.path.join(L.HERE, "out", f"sampler_{tg}_m{m}_T_w{w}.json"), "w"), indent=1)
print(f"DONE p6_10_sampler_triple {seq} {bb} {tau} m={m} w={w} [{time.time() - t0:.0f}s]", flush=True)
