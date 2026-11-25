"""
Analysis 4: sharpness of sites and certificate sizes on the real instance, and the theory's
formulas evaluated with measured numbers.

Instance: X = clash-free grid conformations, known part f = vacuum ff14SB energy, residual g,
E = f + g, envelope d(x,y) = sum_i c_i [x_i != y_i] with the measured constants (rescaled by
kappa_max if the single-flip constants do not dominate multi-site differences on the
non-product domain).

usage: python3 an7_sharpness.py alphabet n residual [--nocover]
"""
import sys, os, json, math, time
import numpy as np
import scipy.sparse as sp
from analysis_lib import *

alphabet, n, rname = sys.argv[1], int(sys.argv[2]), sys.argv[3]
do_cover = "--nocover" not in sys.argv
TAU = 0.7
beta = 1.0 / KT300
d = load(alphabet, n); R = residuals(d); m = d["m"]; k = d["k"]
mask = d["clash"] > TAU
st = states_of(mask).astype(np.int64)
M = len(st)
f = R["f"][mask]; g = R[rname][mask]; E = f + g
names = site_names(n)
c, rms, _ = first_order(R[rname], mask)
out = dict(alphabet=alphabet, n=n, residual=rname, M=int(M), c=c.tolist())
print(f"=== {alphabet} n={n} residual {rname}: {M} clash-free conformations; kT = {KT300:.4f} kcal/mol")
print(f"c_i (single-flip, kcal/mol): {np.round(c, 2)}")

# index lookup for neighbours
code = np.zeros(M, dtype=np.int64)
for i in range(m):
    code = code * k + st[:, i]
lookup = -np.ones(k ** m, dtype=np.int64); lookup[code] = np.arange(M)
pw = k ** (m - 1 - np.arange(m))

def neighbours(x):
    """list over sites of [(state, index in domain or -1)]"""
    res = []
    for i in range(m):
        row = []
        for s in range(k):
            if s != st[x, i]:
                cc = code[x] + (s - st[x, i]) * pw[i]
                row.append((s, int(lookup[cc])))
        res.append(row)
    return res

x0 = int(np.argmin(f)); xs = int(np.argmin(E))
print(f"argmin f: states {st[x0]}, f = min;  argmin E: states {st[xs]};  same conformation: {x0 == xs};  "
      f"E(argmin f) - min E = {E[x0] - E[xs]:.3f} kcal/mol = {(E[x0] - E[xs]) * beta:.2f} kT")
out.update(same_min=bool(x0 == xs), regret=float(E[x0] - E[xs]))

def site_gaps(x, h):
    gaps = np.full(m, np.inf); tables = []
    for i, row in enumerate(neighbours(x)):
        tab = [0.0]
        for s, j in row:
            if j >= 0:
                gaps[i] = min(gaps[i], h[j] - h[x]); tab.append(h[j] - h[x])
        tables.append(tab)
    return gaps, tables

e_f0, tab_f0 = site_gaps(x0, f)        # known-part excitation energies at the known-part minimiser
e_fs, tab_fs = site_gaps(xs, f)        # ... at the true minimiser
e_E, tab_E = site_gaps(xs, E)          # true excitation energies at the true minimiser
print(f"site gaps of the KNOWN part at argmin f (kcal/mol):   {np.round(e_f0, 2)}")
print(f"site gaps of the TRUE energy at argmin E (kcal/mol):  {np.round(e_E, 2)}")
has_nb = np.isfinite(e_f0)
sharp0 = int(((e_f0 >= c) & has_nb).sum())
print(f"single-flip sharpness at argmin f: {int(has_nb.sum())} of {m} sites have a clash-free single-flip neighbour; "
      f"of these {sharp0} are sharp (gap of f >= c_i);   ratios e_i/c_i: {np.round(e_f0 / c, 3)}")
has_nb_s = np.isfinite(e_fs)
sharp_s = int(((e_fs >= c) & has_nb_s).sum())
print(f"single-flip sharpness at argmin E (gaps of the known part f there: {np.round(e_fs, 2)}): "
      f"{int(has_nb_s.sum())} sites with a neighbour, {sharp_s} sharp")
out.update(e_f0=[float(v) if np.isfinite(v) else None for v in e_f0], e_E=[float(v) if np.isfinite(v) else None for v in e_E],
           e_fs=[float(v) if np.isfinite(v) else None for v in e_fs], sharp=sharp0, sites_with_neighbour=int(has_nb.sum()),
           sharp_at_minE=sharp_s, sites_with_neighbour_minE=int(has_nb_s.sum()))

# --- validity of the weighted-Hamming envelope on the (non-product) domain, O(M^2) chunked
H = np.zeros((M, m * k)); H[np.arange(M)[:, None], np.arange(m)[None, :] * k + st] = 1.0
Hc = H * np.repeat(c, k)[None, :]
csum = c.sum()

def dist_rows(rows):
    return csum - Hc[rows] @ H.T          # (len(rows), M) weighted Hamming distances

if M <= 40000:
    kap = 0.0
    for s0 in range(0, M, 512):
        rows = np.arange(s0, min(M, s0 + 512))
        D = dist_rows(rows)
        num = np.abs(g[rows][:, None] - g[None, :])
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(D > 1e-12, num / D, 0.0)
        kap = max(kap, float(ratio.max()))
    print(f"validity of d = sum c_i[x_i != y_i] on the clash-free domain: max |g(x)-g(y)|/d(x,y) = {kap:.4f}"
          + ("  (envelope valid as measured)" if kap <= 1 + 1e-9 else "  -> constants rescaled by this factor"))
    scale = max(1.0, kap)
    out.update(kappa_max=kap)
else:
    scale = 1.0
    print("domain too large for the O(M^2) validity check; constants used as measured")
cv = c * scale

# --- Theorem 11.7: is the single evaluation at argmin f an exact certificate?
D0 = (csum - Hc[[x0]] @ H.T)[0] * scale
margin = f - f[x0] - D0
margin[x0] = np.inf
print(f"Theorem 11.7 (one evaluation certifies iff d(x0,y) <= f(y)-f(x0) for all y): min margin = {margin.min():.2f} kcal/mol "
      f"-> {'YES' if margin.min() >= 0 else 'NO'};  conformations violating: {int((margin < 0).sum())} of {M - 1}")
out.update(thm117_margin=float(margin.min()), thm117_viol=int((margin < 0).sum()))
ham0 = (st != st[x0]).sum(axis=1)
ratio = np.where(ham0 > 0, (f - f[x0]) / np.where(ham0 > 0, D0, 1.0), np.inf)
ystar = int(np.argmin(ratio))
print(f"cost-to-distance ratio lambda* = min_y (f(y)-f(x0))/d(x0,y) = {ratio[ystar]:.4f}  (the constants would have to be "
      f"{1/max(ratio[ystar],1e-12):.0f} times smaller for one evaluation to certify); attained at Hamming distance {int((st[ystar] != st[x0]).sum())}, "
      f"f(y)-f(x0) = {f[ystar]-f[x0]:.2f} kcal/mol")
out.update(lambda_star=float(ratio[ystar]), lambda_star_hamming=int((st[ystar] != st[x0]).sum()))

# --- thresholds of the free-energy theory with the measured constants
u = beta * cv
thr = float(np.log(np.cosh(u / 2)).sum())
print(f"beta*c_i: {np.round(u, 1)}")
print(f"sum_i ln cosh(beta c_i/2) = {thr:.1f} nats = {thr * KT300:.1f} kcal/mol;   beta^2 sum c_i^2/8 = {float((u**2).sum()/8):.0f} nats;   "
      f"range of g on the domain = {g.max()-g.min():.1f} kcal/mol = {(g.max()-g.min())*beta:.0f} kT")
out.update(lncosh=thr, sandwich=float((u ** 2).sum() / 8))
lnZf = float(np.log(np.exp(-beta * (f - f.min())).sum())); lnZE = float(np.log(np.exp(-beta * (E - E.min())).sum()))
dF = -(lnZE - beta * E.min()) + (lnZf - beta * f.min())
pi_f = np.exp(-beta * (f - f.min())); pi_f /= pi_f.sum()
pi_E = np.exp(-beta * (E - E.min())); pi_E /= pi_E.sum()
mean_g = float((pi_f * g).sum())
print(f"exact on the grid: ln Z(f+g) - ln Z(f) = {-dF:.2f} nats; -beta <g>_f = {-beta*mean_g:.2f}; Jensen gap = {(-dF) + beta*mean_g:.3f} nats "
      f"(the class bound above is {thr:.0f}); Gibbs weight of argmin E: {pi_E[xs]:.3f}; entropy H(pi_E) = {float(-(pi_E*np.log(pi_E+1e-300)).sum()):.2f} nats")
out.update(dlnZ=float(-dF), jensen=float((-dF) + beta * mean_g), H_E=float(-(pi_E * np.log(pi_E + 1e-300)).sum()))

# --- product-landscape bound (Theorem 11.8 with Boltzmann weights, zero-residual form) from the star of f
def product_bound(tabs, cc, eps=0.0):
    best = (0.0, 0.0)
    for t in np.concatenate([[0.0], np.logspace(-3, 2, 400)]):
        val = -t * eps
        for tab, ci in zip(tabs, cc):
            kk = len(tab)
            if kk < 2:
                continue
            val += math.log(sum(math.exp(-t * e) for e in tab)) - math.log(1 + (kk - 1) * math.exp(-t * ci))
        if val > best[0]:
            best = (val, t)
    return best
pb, tb = product_bound(tab_f0, cv)
lnsize = sum(math.log(len(tab)) for tab in tab_f0)
print(f"product-landscape formula (Thm 11.8, Boltzmann weights) with the measured star of f at argmin f and measured c_i: "
      f"ln N >= {pb:.2f} (t = {tb:.3g}) of ln(prod k_i) = {lnsize:.2f}; i.e. N >= {math.exp(pb):.3g}   [heuristic for a non-additive f]")
out.update(product_bound=pb, lnsize=lnsize)

# --- the real covering problem (memory-safe: two chunked passes; sparse storage only if the cover is sparse)
if do_cover and M <= 40000:
    gap = E - E.min()
    def slack_rows(rows):
        return dist_rows(rows) * scale - g[rows][:, None] + g[None, :]       # slack s(a, y)
    for eps in (0.0, KT300, 2.0):
        t0 = time.time()
        ncover_of_y = np.zeros(M); size_of_a = np.zeros(M)
        for s0 in range(0, M, 512):
            rows = np.arange(s0, min(M, s0 + 512))
            cov = slack_rows(rows) <= gap[None, :] + eps + 1e-9
            ncover_of_y += cov.sum(axis=0); size_of_a[rows] = cov.sum(axis=1)
        forced = ncover_of_y == 1                              # covered only by itself
        sparse_case = size_of_a.sum() < 3e7
        vol = float("nan"); best_pf = float("nan")
        if sparse_case:
            rows_l, cols_l = [], []
            for s0 in range(0, M, 512):
                rows = np.arange(s0, min(M, s0 + 512))
                r_, c_ = np.nonzero(slack_rows(rows) <= gap[None, :] + eps + 1e-9)
                rows_l.append(rows[r_]); cols_l.append(c_)
            rr = np.concatenate(rows_l); cc_ = np.concatenate(cols_l)
            C = sp.csr_matrix((np.ones(len(rr), dtype=np.float32), (rr, cc_)), shape=(M, M))
            Ccsc = C.tocsc()
            My = np.array([size_of_a[Ccsc.indices[Ccsc.indptr[y]:Ccsc.indptr[y + 1]]].max() for y in range(M)])
            vol = float((1.0 / My).sum())
            best_pf = 0.0
            for t in (0.1, 0.4, 1.6):
                numer = np.exp(-t * gap).sum(); den = 0.0
                for s0 in range(0, M, 512):
                    rows = np.arange(s0, min(M, s0 + 512))
                    den = max(den, float(np.exp(-t * slack_rows(rows)).sum(axis=1).max()))
                best_pf = max(best_pf, math.exp(-t * eps) * numer / den)
            chosen = np.flatnonzero(forced).tolist()
            covered = np.zeros(M, dtype=bool)
            if chosen:
                covered |= np.asarray(C[chosen].sum(axis=0)).ravel() > 0
            while not covered.all():
                gain = C @ (~covered).astype(np.float32)
                a_ = int(np.argmax(gain)); chosen.append(a_)
                covered[C.indices[C.indptr[a_]:C.indptr[a_ + 1]]] = True
        else:
            # dense cover: greedy over a candidate pool (forced points + the 1500 largest sets); any point left
            # uncovered is added itself, so the result is a valid cover (an upper bound on N_cov)
            cand = np.unique(np.concatenate([np.flatnonzero(forced), np.argsort(-size_of_a)[:1500]]))
            Cd = np.zeros((len(cand), M), dtype=bool)
            for s0 in range(0, len(cand), 512):
                rows = cand[s0:s0 + 512]
                Cd[s0:s0 + 512] = slack_rows(rows) <= gap[None, :] + eps + 1e-9
            fidx = np.flatnonzero(np.isin(cand, np.flatnonzero(forced)))
            chosen = cand[fidx].tolist()
            covered = Cd[fidx].any(axis=0) if len(fidx) else np.zeros(M, dtype=bool)
            while not covered.all():
                gain = (Cd & ~covered[None, :]).sum(axis=1)
                a_ = int(np.argmax(gain))
                if gain[a_] == 0:
                    chosen += np.flatnonzero(~covered).tolist(); break
                chosen.append(int(cand[a_])); covered |= Cd[a_]
        lbs = [int(forced.sum()), 1]
        if vol == vol: lbs.append(math.ceil(vol - 1e-9))
        if best_pf == best_pf: lbs.append(math.ceil(best_pf - 1e-9))
        lb = max(lbs)
        if lb == 1 and len(chosen) > 1 and size_of_a.max() < M:
            lb = 2                                   # no single centre covers everything
        print(f"cover at eps = {eps:.3f} kcal/mol: forced points {int(forced.sum())}, volume bound {vol:.1f}, partition bound {best_pf:.1f} "
              f"=> N_cov >= {lb};  greedy cover {len(chosen)}  (of M = {M};  mean set size {size_of_a.mean():.1f}, max {int(size_of_a.max())}; "
              f"{'sparse' if sparse_case else 'dense'} path)  [{time.time()-t0:.0f}s]", flush=True)
        out[f"cover_eps{eps:.3f}"] = dict(forced=int(forced.sum()), volume=vol, partition=best_pf, lower=lb, greedy=len(chosen))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "out", f"an7_{alphabet}_n{n}_{rname}.json"), "w"), indent=0)
