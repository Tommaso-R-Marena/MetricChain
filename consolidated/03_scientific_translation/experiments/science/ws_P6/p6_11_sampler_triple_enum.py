"""
P6: the sandwich sampler on the TRIPLE-share sandwich, checked on an ENUMERATED instance: range of W at every state,
the identity Z(E) = Z(m_+) + (Z(m_-) - Z(m_+)) E_q W, and coverage of the Hoeffding bracket over repetitions of the
actual algorithm (rejection from the transfer-matrix sampler of the model with three-site terms).
usage: python3 -B p6_11_sampler_triple_enum.py SEQ BB TAU m w [--reps 200] [--N 1200]
"""
import sys, os, time, math, json
import numpy as np
import p6lib as L
import p6_04_sampler as SMP
import p6_09_triple as TR
pw = L.pw; BETA = L.BETA

a = sys.argv[1:]
seq, bb, tau, m, w = a[0], a[1], float(a[2]), int(a[3]), int(a[4])
reps = SMP.opt(a, "--reps", 200, int); N = SMP.opt(a, "--N", 1200, int); delta = 0.05
seed = 2026112600 + 10 * m + 3
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
lnZlo, lnZup = lo.lnZ(), up.lnZ(); D = lnZlo - lnZup; acc = -math.expm1(-D)
st, g, src = L.enumerate_g(G, seq, bb, tau)
E = pw.f_energy(st, c0, h, J) + g
ml, mu = lo.energy(st), up.energy(st)
lnZE = float(np.log(np.exp(-BETA * (E - E.min())).sum()) - BETA * E.min())
r = BETA * (E - ml); U = BETA * (mu - ml); pos = U > 0
W, dW = SMP.w_values(r[pos], U[pos])
qw = np.exp(-BETA * (ml[pos] - E.min())) * (-np.expm1(-U[pos])); q = qw / qw.sum()
EqW = float((q * W).sum()); lnZ_id = lnZup + math.log1p(math.expm1(D) * EqW)
print(f"=== sampler on the triple-share sandwich, enumerated: {seq} on {bb}, tau {tau}, m = {m}, window {w}; {len(st)} states; D = {D:.6f}; acceptance {acc:.5f}; seed {seed}")
print(f"    ENUMERATION: W in [{W.min():.6g}, {W.max():.6g}], states with W outside [0, 1]: {int(((W < 0) | (W > 1)).sum())}; exact E_q W = {EqW:.8f}; "
      f"identity: {lnZ_id:.10f} against ln Z(E) = {lnZE:.10f}, difference {abs(lnZ_id - lnZE):.1e}", flush=True)
rng = np.random.default_rng(seed)
batch = int(min(400000, max(20000, 2000 / max(acc, 1e-6))))
inside = 0; widths = []; errs = []; props = []
t1 = time.time()
for rep in range(reps):
    Sacc, Us, nprop = SMP.propose_accept(lo, diff, N, rng, batch)
    ii = np.ravel_multi_index(tuple(Sacc.T), k)
    Wi, dWi = SMP.w_values(BETA * (E[ii] - ml[ii]), BETA * (mu[ii] - ml[ii]))
    b0, b1, t, pt = SMP.bracket(Wi, dWi, lnZlo, lnZup, delta)
    inside += int(b0 <= lnZE <= b1); widths.append(b1 - b0); errs.append(pt - lnZE); props.append(nprop)
errs = np.array(errs)
print(f"    COVERAGE: {reps} repetitions with N = {N}: truth inside the bracket in {inside} of {reps}; mean width {np.mean(widths):.3e} (deterministic {D:.3e}); "
      f"rms error of the point estimate {np.sqrt((errs ** 2).mean()):.2e}; observed acceptance {N / np.mean(props):.5f} [{time.time() - t1:.1f}s]")
json.dump(dict(seq=seq, bb=bb, tau=tau, m=m, w=w, D=D, EqW=EqW, identity_dev=abs(lnZ_id - lnZE), W_min=float(W.min()), W_max=float(W.max()),
               reps=reps, N=N, inside=inside, mean_width=float(np.mean(widths)), rms_err=float(np.sqrt((errs ** 2).mean())), seed=seed),
          open(os.path.join(L.HERE, "out", f"sampler_triple_enum_{L.tagname(seq, bb, tau)}_m{m}_w{w}.json"), "w"), indent=1)
print(f"DONE p6_11_sampler_triple_enum {seq} {bb} {tau} m={m} w={w} [{time.time() - t0:.0f}s]", flush=True)
