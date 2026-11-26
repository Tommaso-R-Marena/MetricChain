#!/usr/bin/env python3
"""R19, items 1 and 2 at PRODUCTION SIZE: what the driver's check at 5 380 states can see, and the exact group means against a
large exact sample.

What is run.  The coordinator's first_order_recovery.py, the committed file, UNMODIFIED, in-process (a RE-RUN; its output is
the first part of my log and is compared with the committed log afterwards); a profile hook copies the locals of main().
Then, with MY code:
 (b) the accounting as an IDENTITY at the driver's own 5 380 states (new evaluations of the energy through the driver's
     evaluator):  R+ := m_+ - E - s_+ = A + (RND-1) pen + env - r + 1e-9 x (number of ceiling items that are non-zero at the state),
     the same for the floor with + r;  A = eps_g (1 + sum_{j<m} C(t, j) 2^j), env and pen from P9's raw tables, r = g - I_{m-1} g
     with the driver's anchored terms.  (At every state of the five-residue instances this identity holds: r19_item1_identity.)
 (c) K1: each single item doubled, in turn: how many of the items the driver's hypothesis check sees at these states, and how
     many are non-zero at any of them (what the identity can see).  K2-K4 as in r19_item1_identity.py.
 (e) THE EXACT MEANS at this size: NBIG exact samples of the ceiling (the model's own backward sampler, seed of mine, not the
     driver's), the five statistics of every group and their sums against the held-site passes, in standard errors; and
     ln Z(m_-) - ln Z(m_+) against ln < e^{beta (m_+ - m_-)} > over the same samples.
     What it is compared with: the driver's comparison uses 20 000 samples (seed 4) and found the lysine cases 1.4-1.6 standard
     errors low in sum <S->; if that were a bias of the exact means (2 % of the mean) it would show here as -6 standard errors.

Run: python3 -B r19_item1_sampled.py K12 4 4 [NBIG] > r19_item1_sampled_K12_m4_w4.log
"""
import os, sys, math, time, itertools, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
PI = "/home/user/MetricChain/experiments/science/pi_inference"
sys.path.insert(0, PI)
import numpy as np

t00 = time.time()
args = [a for a in sys.argv[1:4]]
NBIG = int(sys.argv[4]) if len(sys.argv) > 4 else 400000
assert "--enum" not in sys.argv
import first_order_recovery as FOR                                   # the coordinator's driver, as committed

cap = {}


def _prof(frame, event, arg):
    if event == "return" and frame.f_code is FOR.main.__code__:
        cap.update(frame.f_locals)


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


sys.argv = [os.path.join(PI, "first_order_recovery.py")] + args
print("##### R19: output of the coordinator's driver (re-run, unmodified) #####", flush=True)
sys.setprofile(_prof)
try:
    FOR.main()
finally:
    sys.setprofile(None)
print(f"##### R19: my checks on the captured objects [{time.time() - t00:.0f}s, peak RSS {rss():.0f} MB] #####", flush=True)

n, k, x0, m, M, w = cap["n"], list(cap["k"]), list(cap["x0"]), cap["m"], cap["M"], cap["w"]
lo, up, items, kind, rts = cap["lo"], cap["up"], cap["items"], cap["kind"], cap["rts"]
d, tabs, subs, keepK = cap["d"], cap["tabs"], cap["subs"], cap["keepK"]
c0, h, J, GS, res, sets, energy = cap["c0"], cap["h"], cap["J"], cap["GS"], cap["res"], cap["sets"], cap["energy"]
BETA, RND, SAFE, EPS = FOR.BETA, FOR.RND, FOR.SAFE, FOR.L.EPS_G
lnZlo, lnZup = cap["lnZlo"], cap["lnZup"]; D = lnZlo - lnZup
non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]; X0 = np.array(x0)
posn = [np.full(k[i], -1) for i in range(n)]
for i in range(n): posn[i][non[i]] = np.arange(len(non[i]))
for key in ("XS", "XM", "gX", "I", "rem", "th", "thmin", "XGo"):       # large locals of the driver that I do not use
    cap.pop(key, None)


def tab_at(U, tab, X):
    return np.asarray(tab)[tuple(X[:, u] for u in U)]


def model_energy(mdl, X):
    e = np.full(len(X), float(mdl.const))
    for i in range(n): e += np.asarray(mdl.one[i])[X[:, i]]
    for (i, j), tab in mdl.pair.items(): e += np.asarray(tab)[X[:, i], X[:, j]]
    for U, tab in mdl.multi.items(): e += tab_at(U, tab, X)
    return e


def side_items(side, classes=("far", "term", "alloc")):
    return [j for j in range(len(items)) if kind[j][0] in classes and kind[j][1] in (side, 0)]


name = list(GS.keys())[-1]
print(f"instance: n = {n}, k = {k}, order m = {m}, band w = {w}; {len(items)} items ({sum(1 for q in kind if q[0] == 'far')} far, {sum(1 for q in kind if q[0] == 'term')} term, {sum(1 for q in kind if q[0] == 'alloc')} alloc), "
      f"{sum(r is not None for r in rts)} with a route, {len(GS[name])} groups; D = {D:.6g}; corrected bracket of the driver [{res[name][0]:.7f}, {res[name][1]:.7f}]")
badroute = 0
for it, r in zip(items, rts):
    if r is None: continue
    U = it[0]; dr, held, s = r
    V = U if dr == "fwd" else tuple(n - 1 - u for u in reversed(U)); hv = held if dr == "fwd" else n - 1 - held
    badroute += int(not ((V[0] == hv) and all(s <= v <= s + w - 1 for v in V[1:]) and s >= hv + 1 and s + w - 1 <= n - 1))
print(f"(a) routed items whose window does not hold all sites but the held one: {badroute}; items that would fit a window: {sum(1 for it in items if it[0][-1] - it[0][0] <= w)}; smallest entry of any item: {min(float(it[1].min()) for it in items):.1e}")

# ---------------------------------------------------------------------------------------------- (b) the identity at the driver's states
t1 = time.time(); names = list(sets); X = np.concatenate([np.asarray(sets[nm]) for nm in names]).astype(np.int64); lab = np.concatenate([np.full(len(sets[nm]), q) for q, nm in enumerate(names)])
N = len(X); EE = energy(X); t_off = (X != X0[None]).sum(1)
f_en = np.full(N, float(c0))
for i in range(n): f_en += np.asarray(h[i])[X[:, i]]
for (i, j), tab in J.items(): f_en += np.asarray(tab)[X[:, i], X[:, j]]
ghat = EE - f_en; I_drv = np.zeros(N)
for U, arr in d.items(): I_drv += float(arr) if len(U) == 0 else tab_at(U, arr, X)
r_ = ghat - I_drv
env = np.zeros(N); pen = np.zeros(N)
for T, tab, K in zip(subs, tabs, keepK):
    offT = np.all([X[:, i] != x0[i] for i in T], axis=0)
    if offT.any(): env[offT] += tab[tuple(posn[i][X[offT, i]] for i in T)]
    other = tuple(p for p in range(m) if T[p] not in K); red = tab.max(axis=other) if other else tab
    offK = np.all([X[:, i] != x0[i] for i in K], axis=0)
    if offK.any(): pen[offK] += red[tuple(posn[i][X[offK, i]] for i in K)]
A = EPS * np.array([1.0 + sum(math.comb(int(t), j) * 2 ** j for j in range(1, M + 1)) for t in range(n + 1)])[t_off]
mp, mm = model_energy(up, X), model_energy(lo, X)
val = [tab_at(it[0], it[1], X) for it in items]
ip, im = side_items(+1), side_items(-1)
sp = sum(val[j] for j in ip); sm = sum(val[j] for j in im)
nzp = sum((val[j] > 0).astype(int) for j in ip); nzm = sum((val[j] > 0).astype(int) for j in im)
Rp, Rm = mp - EE - sp, EE - mm - sm
Pp, Pm = A + (RND - 1.0) * pen + env - r_, A + (RND - 1.0) * pen + env + r_
dp_, dm_ = Rp - Pp - SAFE * nzp, Rm - Pm - SAFE * nzm
tol = 5e-10
print(f"(b) {N} states of the driver ({', '.join(f'{nm}: {int((lab == q).sum())}' for q, nm in enumerate(names))}), energies evaluated anew [{time.time() - t1:.0f}s]; sites off the anchor: "
      f"{dict(zip(*[v.tolist() for v in np.unique(t_off, return_counts=True)]))}")
print(f"    THE IDENTITY: R+ - P+ - 1e-9 x (non-zero ceiling items) in [{float(dp_.min()):.3e}, {float(dp_.max()):.3e}], outside +-{tol:.0e} at {int((np.abs(dp_) > tol).sum())} states; "
      f"the same for the floor: [{float(dm_.min()):.3e}, {float(dm_.max()):.3e}], outside at {int((np.abs(dm_) > tol).sum())} states; largest number of non-zero items at a state: {int(nzp.max())}, {int(nzm.max())}")
out = t_off >= m
if out.any():
    ratio = env[out] / np.maximum(np.abs(r_[out]), 1e-300)
    print(f"    Theorem R at these states: violations of |r| <= env + A: {int((np.abs(r_) > env + A).sum())}; inside the ball ({int((~out).sum())} states) largest |r| {float(np.abs(r_[~out]).max()):.2e}; outside ({int(out.sum())}): "
          f"largest |r| {float(np.abs(r_[out]).max()):.4g}, smallest env/|r| {float(ratio.min()):.2f}, median {float(np.median(ratio)):.1f}")
for q, nm in enumerate(names):
    s_ = lab == q
    print(f"      {nm}: smallest margins m+ - E - s+ = {float(Rp[s_].min()):.2e}, E - m- - s- = {float(Rm[s_].min()):.2e}; of which env - |r| at that state: {float((env - np.abs(r_))[s_][np.argmin(np.minimum(Rp, Rm)[s_])]):.2e}")

# ---------------------------------------------------------------------------------------------- (c) controls


def hyp_viol(sp_, sm_):
    return int((mp - EE < sp_ - 1e-9).sum()), int((EE - mm < sm_ - 1e-9).sum())


print(f"(c) no change: hypothesis violations (ceiling, floor) = {hyp_viol(sp, sm)}  [must be (0, 0)]; the driver's control (every item doubled): {sum(hyp_viol(2 * sp, 2 * sm))}")
cnt = {c: dict(n=0, nonzero=0, seen=0, routed=0, routed_seen=0, routed_nonzero=0) for c in ("far", "term", "alloc")}; unseen_slack = {c: 0.0 for c in cnt}
for j in range(len(items)):
    c, side = kind[j]; rr = cnt[c]; rr["n"] += 1; nzj = bool((val[j] > 0).any()); rr["nonzero"] += int(nzj)
    hv = 0
    if side in (+1, 0): hv += hyp_viol(sp + val[j], sm)[0]
    if side in (-1, 0): hv += hyp_viol(sp, sm + val[j])[1]
    rr["seen"] += int(hv > 0)
    if rts[j] is not None:
        rr["routed"] += 1; rr["routed_seen"] += int(hv > 0); rr["routed_nonzero"] += int(nzj)
for c, rr in cnt.items():
    print(f"    K1 '{c}': {rr['n']} items; non-zero at one of the states at least: {rr['nonzero']}; a doubling of the single item is seen by the driver's hypothesis check for {rr['seen']} "
          f"(of the {rr['routed']} with a route: non-zero {rr['routed_nonzero']}, seen {rr['routed_seen']})")
al = sum(val[j] for j in side_items(+1, ("alloc",))) if side_items(+1, ("alloc",)) else np.zeros(N)
print(f"    K2 allocation slack of the floor moved to the ceiling: hypothesis violations (ceiling, floor) = {hyp_viol(sp + al, sm - al)}")
print(f"    K3 the whole penalty claimed as slack on both sides (s + env): {hyp_viol(sp + env, sm + env)}")
print(f"    K4 Theta halved inside the alloc items (s + env/2): {hyp_viol(sp + 0.5 * env, sm + 0.5 * env)};  K4b Theta divided by ten (s + 0.9 env): {hyp_viol(sp + 0.9 * env, sm + 0.9 * env)}")
for c in ("far", "term", "alloc"):
    a_ = sum(val[j] for j in side_items(+1, (c,))) if side_items(+1, (c,)) else np.zeros(N); b_ = sum(val[j] for j in side_items(-1, (c,))) if side_items(-1, (c,)) else np.zeros(N)
    print(f"    K5 class '{c}' doubled alone: hypothesis violations = {hyp_viol(sp + a_, sm + b_)}")
del val

# ---------------------------------------------------------------------------------------------- (e) the exact means against a large exact sample
t1 = time.time(); rng = np.random.default_rng(1911 + 100 * m + w)
XS = up.sample(NBIG, rng).astype(np.int64)
print(f"(e) {NBIG} exact samples of the ceiling (seed {1911 + 100 * m + w}) [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]; sites off the anchor on average {float((XS != X0[None]).sum(1).mean()):.3f}")
groups = {}
for j in range(len(items)):
    if rts[j] is None: continue
    g = groups.setdefault(rts[j], [np.zeros(NBIG), np.zeros(NBIG)]); v = tab_at(items[j][0], items[j][1], XS)
    if kind[j][1] in (+1, 0): g[0] += v
    if kind[j][1] in (-1, 0): g[1] += v
assert set(groups) == set(GS[name])
tot = {q: np.zeros(NBIG) for q in ("a", "e", "b", "c", "cp")}; zs = []; worst = (0.0, None)
for gk, (Sp, Sm) in groups.items():
    Ep = np.exp(BETA * Sp); smp = dict(a=Sp, e=Ep - 1.0, b=Sm, c=Sm * Ep, cp=np.expm1(BETA * Sm) * Ep)
    for q, v in smp.items():
        tot[q] += v; se = float(v.std(ddof=1)) / math.sqrt(NBIG); ex = GS[name][gk][q]
        if se > 0:
            z = (float(v.mean()) - ex) / se; zs.append(z)
            if abs(z) > abs(worst[0]): worst = (z, (gk, q, ex, float(v.mean()), se))
zs = np.array(zs)
print(f"    per group and statistic ({len(zs)} comparisons with a non-zero standard error): z-scores: mean {zs.mean():+.3f}, standard deviation {zs.std():.3f}, largest |z| {np.abs(zs).max():.2f} "
      f"(group {worst[1][0]}, statistic {worst[1][1]}: exact {worst[1][2]:.6g}, sampled {worst[1][3]:.6g} +- {worst[1][4]:.2g}); |z| > 3: {int((np.abs(zs) > 3).sum())}, |z| > 2: {int((np.abs(zs) > 2).sum())} "
      f"(expected for independent standard normal values: {0.0027 * len(zs):.1f}, {0.0455 * len(zs):.1f})")
for q, lbl, fac in (("a", "sum <S+>", BETA), ("e", "sum <e^(beta S+) - 1>", 1.0), ("b", "sum <S->", BETA), ("c", "sum <S- e^(beta S+)>", BETA), ("cp", "sum <(e^(beta S-) - 1) e^(beta S+)>", 1.0)):
    ex = sum(g[q] for g in GS[name].values()); v = tot[q]; se = float(v.std(ddof=1)) / math.sqrt(NBIG)
    print(f"    {lbl}: exact (held-site passes) {fac * ex:.8g}, sampled {fac * float(v.mean()):.8g} +- {fac * se:.2g} ({(float(v.mean()) - ex) / se:+.2f} standard errors); "
          f"skewness of the summand {float(((v - v.mean()) ** 3).mean() / v.std() ** 3):.1f}")
dm = BETA * (model_energy(up, XS) - model_energy(lo, XS)); ed = np.exp(dm); Dhat = math.log(float(ed.mean())); seD = float(ed.std(ddof=1)) / math.sqrt(NBIG) / float(ed.mean())
print(f"    ln Z(m-) - ln Z(m+): transfer matrices {D:.8g}; ln < e^(beta (m+ - m-)) > over the samples {Dhat:.8g} +- {seD:.2g} ({(Dhat - D) / seD:+.2f} standard errors)")
# what the corrected bracket would be with every mean moved by three standard errors against it (sensitivity, not a certificate)
print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {rss():.0f} MB")
