#!/usr/bin/env python3
"""R19, item 1: the accounting of the recovery as an IDENTITY at every state, with controls the coordinator did not run.

What is run.  The coordinator's driver experiments/science/pi_inference/first_order_recovery.py, the committed file,
UNMODIFIED, in-process (a RE-RUN); a profile hook copies the local objects of its main() at return (models lo/up, items,
routes, tables, choices, the enumerated states and energies).  Nothing of the driver is edited or copied.  All checks below
are MY code, written from the statements (addendum A17 (19)-(20), items 69-72, and the driver's docstring):

 (a) structure: every anchored term of the driver is exactly zero where a site is at the anchor; the allowance tables differ
     from it by exactly 2^|U| eps_g on the all-off entries; every routed item has all its sites but the held one in its window.
 (b) THE IDENTITY.  With my own evaluation of the two models from their tables, my own interpolant (from the enumerated values
     of g, not from the ball cache), my own envelope env(x) = sum_{T subset S(x)} Theta_T(x_T) and penalty pen(x) from P9's raw
     tables and the kept sub-tuples:
         R+(x) := m_+(x) - E(x) - s_+(x)   should equal   P+(x) := A(x) + (RND-1) pen(x) + env(x) - r(x),
         R-(x) := E(x) - m_-(x) - s_-(x)   should equal   P-(x) := A(x) + (RND-1) pen(x) + env(x) + r(x),
     A(x) = eps_g (1 + sum_{j=1}^{m-1} C(t, j) 2^j), t = number of sites off the anchor, r = g - I_{m-1} g,
     up to the 1e-9 by which the driver lowers every item (so 0 <= R - P <= (number of items of that side) * 1e-9).
     A slack counted twice ANYWHERE (not only where the margin is tight) makes R - P negative by that slack.
     Also separately: (b1) m_+ - m_+^src = far+ + term+ items, m_+^src the ceiling with nothing reduced (a "reduction minus
     source" identity that needs no energy); (b2) pen - env = alloc items; (b3) env >= |r| - A (Theorem R at every state).
 (c) controls.  K1: each single item doubled, in turn -- violations of the identity (must be > 0 for every item) and of the
     driver's hypothesis check (how many items the driver's check can see).  K2: the allocation slack of the floor moved to
     the ceiling (the sum s_+ + s_- unchanged): must violate the ceiling's hypothesis.  K3: the whole penalty claimed as
     slack on both sides (the envelope "counted twice"): must violate.  K4: Theta halved inside the alloc items: the
     identity must break; the hypothesis check is reported (it need not see it).  K5: each class doubled alone.
 (d) the five group statistics and the four bounds recomputed by my enumeration from the routes; the exact ln Z.

Run: python3 -B r19_item1_identity.py K5 4 2 --enum > r19_item1_identity_K5_m4_w2.log
"""
import os, sys, math, time, itertools, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
PI = "/home/user/MetricChain/experiments/science/pi_inference"
sys.path.insert(0, PI)
import numpy as np

t00 = time.time()
args = sys.argv[1:]
assert "--enum" in args
import first_order_recovery as FOR                                   # the coordinator's driver, as committed

cap = {}


def _prof(frame, event, arg):
    if event == "return" and frame.f_code is FOR.main.__code__:
        cap.update(frame.f_locals)


sys.argv = [os.path.join(PI, "first_order_recovery.py")] + args
print("##### R19: output of the coordinator's driver (re-run, unmodified) #####", flush=True)
sys.setprofile(_prof)
try:
    FOR.main()
finally:
    sys.setprofile(None)
print("##### R19: my checks on the captured objects #####", flush=True)

n, k, x0, m, M, w = cap["n"], list(cap["k"]), list(cap["x0"]), cap["m"], cap["M"], cap["w"]
lo, up, items, kind, rts = cap["lo"], cap["up"], cap["items"], cap["kind"], cap["rts"]
d, d_lo, d_up, tabs, subs, keepK = cap["d"], cap["d_lo"], cap["d_up"], cap["tabs"], cap["subs"], cap["keepK"]
st, EE, c0, h, J, GS, res = cap["st"], cap["EE"], cap["c0"], cap["h"], cap["J"], cap["GS"], cap["res"]
BETA, RND, SAFE, EPS = FOR.BETA, FOR.RND, FOR.SAFE, FOR.L.EPS_G
lnZlo_drv, lnZup_drv = cap["lnZlo"], cap["lnZup"]
N = len(st); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
X0 = np.array(x0); t_off = (st != X0[None]).sum(1)
cols = [st[:, i] for i in range(n)]
print(f"instance: n = {n}, k = {k}, anchor {x0}, order m = {m}, band w = {w}, {N} states, {len(items)} items "
      f"({sum(1 for q in kind if q[0] == 'far')} far, {sum(1 for q in kind if q[0] == 'term')} term, {sum(1 for q in kind if q[0] == 'alloc')} alloc); eps_g = {EPS}, RND - 1 = {RND - 1:.1e}")


def tab_at(U, tab):
    return np.asarray(tab)[tuple(cols[u] for u in U)]


def model_energy(mdl):
    """my own evaluation of a window model from its tables."""
    e = np.full(N, float(mdl.const))
    for i in range(n): e += np.asarray(mdl.one[i])[cols[i]]
    for (i, j), tab in mdl.pair.items(): e += np.asarray(tab)[cols[i], cols[j]]
    for U, tab in mdl.multi.items(): e += tab_at(U, tab)
    return e


# ---------------------------------------------------------------------------------------------- (a) structure
bad0 = 0; badallow = 0.0
for U, arr in d.items():
    if len(U) == 0: continue
    for a, u in enumerate(U):
        bad0 += int(np.count_nonzero(np.take(arr, x0[u], axis=a)))
    offm = np.ones(arr.shape, dtype=bool)
    for a, u in enumerate(U):
        sl = [slice(None)] * len(U); sl[a] = x0[u]; offm[tuple(sl)] = False
    exp_ = np.where(offm, (2 ** len(U)) * EPS, 0.0)
    badallow = max(badallow, float(np.abs((d_up[U] - arr) - exp_).max()), float(np.abs((arr - d_lo[U]) - exp_).max()))
badroute = 0
for it, r in zip(items, rts):
    if r is None: continue
    U = it[0]; dr, held, s = r
    V = U if dr == "fwd" else tuple(n - 1 - u for u in reversed(U)); hv = held if dr == "fwd" else n - 1 - held
    ok = (V[0] == hv) and all(s <= v <= s + w - 1 for v in V[1:]) and s >= hv + 1 and s + w - 1 <= n - 1
    badroute += int(not ok)
nofit = sum(1 for it in items if it[0][-1] - it[0][0] <= w)
print(f"(a) anchored terms of the driver: non-zero entries where a site of the term is at the anchor: {bad0} (must be 0); allowance tables d_up - d and d - d_lo against 2^|U| eps_g [all sites off]: "
      f"largest deviation {badallow:.1e}; routed items whose window does not hold all sites but the held one: {badroute}; items that would fit a window: {nofit}; "
      f"smallest entry of any item {min(float(it[1].min()) for it in items):.1e} (items must be >= 0)")

# ---------------------------------------------------------------------------------------------- (b) the identity
f_en = np.full(N, float(c0))
for i in range(n): f_en += np.asarray(h[i])[cols[i]]
for (i, j), tab in J.items(): f_en += np.asarray(tab)[cols[i], cols[j]]
ghat = EE - f_en                                                    # the evaluated solvent term at every state
Gfull = ghat.reshape(k)
# my own anchored terms from the ENUMERATED values (not the ball cache)
I_mine = np.zeros(N); nterm = 0
for s_ in range(0, M + 1):
    for U in itertools.combinations(range(n), s_):
        idx = tuple(slice(None) if i in U else x0[i] for i in range(n))
        dd = np.array(Gfull[idx], dtype=float)
        for a, u in enumerate(U):
            dd = dd - np.take(dd, [x0[u]], axis=a)
        I_mine += float(dd) if s_ == 0 else dd[tuple(cols[u] for u in U)]; nterm += 1
I_drv = np.zeros(N)
for U, arr in d.items():
    I_drv += float(arr) if len(U) == 0 else tab_at(U, arr)
r_mine = ghat - I_mine; r_drv = ghat - I_drv
# envelope and penalty from P9's raw tables (my code)
env = np.zeros(N); pen = np.zeros(N); alloc_raw_sum = np.zeros(N)
posn = [np.full(k[i], -1) for i in range(n)]
for i in range(n): posn[i][non[i]] = np.arange(len(non[i]))
for T, tab, K in zip(subs, tabs, keepK):
    offT = np.all([cols[i] != x0[i] for i in T], axis=0)
    th = np.zeros(N); th[offT] = tab[tuple(posn[i][cols[i][offT]] for i in T)]
    env += th
    other = tuple(p for p in range(m) if T[p] not in K)
    red = tab.max(axis=other) if other else tab
    offK = np.all([cols[i] != x0[i] for i in K], axis=0)
    pk = np.zeros(N); pk[offK] = red[tuple(posn[i][cols[i][offK]] for i in K)]
    pen += pk
    assert (pk - th >= -1e-15).all()
A = EPS * np.array([1.0 + sum(math.comb(int(t), j) * 2 ** j for j in range(1, M + 1)) for t in range(n + 1)])[t_off]
mp, mm = model_energy(up), model_energy(lo)
dev_en = max(float(np.abs(mp - up.energy(st)).max()), float(np.abs(mm - lo.energy(st)).max()))


def side_items(side, classes=("far", "term", "alloc")):
    return [j for j in range(len(items)) if kind[j][0] in classes and kind[j][1] in (side, 0)]


val = [tab_at(it[0], it[1]) for it in items]                         # every (cleaned) item at every state
sp = sum(val[j] for j in side_items(+1)); sm = sum(val[j] for j in side_items(-1))
Rp, Rm = mp - EE - sp, EE - mm - sm
Pp, Pm = A + (RND - 1.0) * pen + env - r_mine, A + (RND - 1.0) * pen + env + r_mine
np_, nm_ = len(side_items(+1)), len(side_items(-1))
tol = 2e-10
idp = int(((Rp - Pp < -tol) | (Rp - Pp > np_ * SAFE + tol)).sum()); idm = int(((Rm - Pm < -tol) | (Rm - Pm > nm_ * SAFE + tol)).sum())
print(f"(b) my interpolant ({nterm} terms from the enumerated g) against the driver's (ball cache): largest difference {float(np.abs(I_mine - I_drv).max()):.2e} kcal/mol; "
      f"my evaluation of the models against the driver's: {dev_en:.1e}")
print(f"    THE IDENTITY at every state: R+ - P+ in [{float((Rp - Pp).min()):.3e}, {float((Rp - Pp).max()):.3e}] (allowed [0, {np_} x 1e-9]), outside at {idp} states; "
      f"R- - P- in [{float((Rm - Pm).min()):.3e}, {float((Rm - Pm).max()):.3e}] (allowed [0, {nm_} x 1e-9]), outside at {idm} states (tolerance {tol:.0e})")
# (b1) reduction minus source, without the energy
for nm, mdl, dd, sgn, side in (("ceiling", up, d_up, +1, +1), ("floor", lo, d_lo, -1, -1)):
    src = f_en + float(dd[()]) + sgn * EPS + sgn * RND * pen
    for U, arr in dd.items():
        if len(U) >= 1: src += tab_at(U, arr)
    red_minus_src = sgn * (model_energy(mdl) - src)
    its = sum(val[j] for j in side_items(side, ("far", "term")))
    dif = red_minus_src - its; ni = len(side_items(side, ("far", "term")))
    print(f"    (b1) {nm}: |model - source model| - (far + term items): in [{float(dif.min()):.3e}, {float(dif.max()):.3e}] (allowed [0, {ni} x 1e-9]); outside at {int(((dif < -tol) | (dif > ni * SAFE + tol)).sum())} states; "
          f"largest reduction {float(red_minus_src.max()):.4g} kcal/mol")
al = sum(val[j] for j in side_items(+1, ("alloc",))) if side_items(+1, ("alloc",)) else np.zeros(N)
dif = (pen - env) - al; na = len(side_items(+1, ("alloc",)))
print(f"    (b2) pen - env - (alloc items): in [{float(dif.min()):.3e}, {float(dif.max()):.3e}] (allowed [0, {na} x 1e-9]); outside at {int(((dif < -tol) | (dif > na * SAFE + tol)).sum())} states; "
      f"largest pen {float(pen.max()):.4g}, largest env {float(env.max()):.4g} kcal/mol")
out = t_off >= m
ratio = env[out] / np.maximum(np.abs(r_mine[out]), 1e-300)
print(f"    (b3) Theorem R with the stored tables at every state: violations of |r| <= env + A: {int((np.abs(r_mine) > env + A).sum())}; inside the ball ({int((~out).sum())} states) largest |r| {float(np.abs(r_mine[~out]).max()):.2e}; "
      f"outside ({int(out.sum())} states): largest |r| {float(np.abs(r_mine[out]).max()):.4g}, smallest env/|r| {float(ratio.min()):.2f}, median {float(np.median(ratio)):.1f}; "
      f"states with r > 0: {int((r_mine[out] > 1e-9).sum())}, with r < 0: {int((r_mine[out] < -1e-9).sum())}")

# ---------------------------------------------------------------------------------------------- (c) controls


def hyp_viol(sp_, sm_):
    """the driver's test: violations of m+ - E >= s+ and of E - m- >= s- (its tolerance 1e-9)."""
    return int((mp - EE < sp_ - 1e-9).sum()), int((EE - mm < sm_ - 1e-9).sum())


def id_viol(sp_, sm_):
    a = mp - EE - sp_ - Pp; b = EE - mm - sm_ - Pm
    return int((a < -tol).sum()), int((b < -tol).sum())


v0 = hyp_viol(sp, sm); i0 = id_viol(sp, sm)
print(f"(c) no change: hypothesis violations (ceiling, floor) = {v0}; identity violations (R - P < -{tol:.0e}) = {i0}   [both must be (0, 0)]")
seen_h = {"far": [0, 0], "term": [0, 0], "alloc": [0, 0]}; seen_i = {"far": [0, 0], "term": [0, 0], "alloc": [0, 0]}; zero = 0; lines = []
for j in range(len(items)):
    c, side = kind[j]
    if float(val[j].max()) <= 0.0:
        zero += 1; continue
    hv = [0, 0]; iv = [0, 0]
    if side in (+1, 0):
        hv[0] = hyp_viol(sp + val[j], sm)[0]; iv[0] = id_viol(sp + val[j], sm)[0]
    if side in (-1, 0):
        hv[1] = hyp_viol(sp, sm + val[j])[1]; iv[1] = id_viol(sp, sm + val[j])[1]
    seen_h[c][0] += int(sum(hv) > 0); seen_h[c][1] += 1; seen_i[c][0] += int(sum(iv) > 0); seen_i[c][1] += 1
    lines.append((c, side, items[j][0], float(val[j].max()), sum(hv), sum(iv)))
print(f"    K1 each single item doubled in turn ({len(lines)} items with a non-zero table; {zero} identically zero): the driver's hypothesis check fails for "
      + ", ".join(f"{seen_h[c][0]} of {seen_h[c][1]} {c}" for c in seen_h) + "; my identity check fails for " + ", ".join(f"{seen_i[c][0]} of {seen_i[c][1]} {c}" for c in seen_i))
for c, side, U, mx, hv, iv in lines:
    if hv == 0:
        print(f"        not seen by the hypothesis check: {c} item on {U}, side {side:+d}, largest entry {mx:.3e} kcal/mol; identity violations {iv}")
if na:
    k2 = hyp_viol(sp + al, sm - al); print(f"    K2 allocation slack of the floor moved to the ceiling (s_+ + s_- unchanged): hypothesis violations (ceiling, floor) = {k2}; identity {id_viol(sp + al, sm - al)}")
    k3 = hyp_viol(sp - al + pen, sm - al + pen); print(f"    K3 the whole penalty claimed as slack on both sides (envelope counted as recoverable): hypothesis violations = {k3}; identity {id_viol(sp - al + pen, sm - al + pen)}")
    k4 = hyp_viol(sp + 0.5 * env, sm + 0.5 * env); print(f"    K4 Theta halved inside the alloc items (s + env/2 on both sides): hypothesis violations = {k4}; identity {id_viol(sp + 0.5 * env, sm + 0.5 * env)}")
    k4b = hyp_viol(sp + 0.9 * env, sm + 0.9 * env); print(f"    K4b Theta divided by ten inside the alloc items (s + 0.9 env): hypothesis violations = {k4b}; identity {id_viol(sp + 0.9 * env, sm + 0.9 * env)}")
for c in ("far", "term", "alloc"):
    a_ = sum(val[j] for j in side_items(+1, (c,))) if side_items(+1, (c,)) else np.zeros(N); b_ = sum(val[j] for j in side_items(-1, (c,))) if side_items(-1, (c,)) else np.zeros(N)
    print(f"    K5 class '{c}' doubled alone: hypothesis violations = {hyp_viol(sp + a_, sm + b_)}; identity {id_viol(sp + a_, sm + b_)}")
vd = hyp_viol(2 * sp, 2 * sm); print(f"    (the driver's own control, every item doubled: {vd[0] + vd[1]} violations — the driver printed its count above)")

# ---------------------------------------------------------------------------------------------- (d) group statistics and bounds, my enumeration
wu = np.exp(-BETA * (mp - mp.min())); Zs = wu.sum(); wu /= Zs
lnZup_mine = float(-BETA * mp.min() + math.log(Zs)); lnZlo_mine = float(-BETA * mm.min() + math.log(np.exp(-BETA * (mm - mm.min())).sum()))
lnZE = float(-BETA * EE.min() + math.log(np.exp(-BETA * (EE - EE.min())).sum()))
name = list(GS.keys())[-1]; groups = {}
for j in range(len(items)):
    if rts[j] is None: continue
    g = groups.setdefault(rts[j], [np.zeros(N), np.zeros(N)])
    if kind[j][1] in (+1, 0): g[0] += val[j]
    if kind[j][1] in (-1, 0): g[1] += val[j]
dev = 0.0; mine = {}
for gk, (Sp, Sm) in groups.items():
    ex = dict(a=float(wu @ Sp), e=float(wu @ np.expm1(BETA * Sp)), b=float(wu @ Sm), c=float(wu @ (Sm * np.exp(BETA * Sp))), cp=float(wu @ (np.expm1(BETA * Sm) * np.exp(BETA * Sp))))
    mine[gk] = ex
    for q in ex:
        if abs(ex[q]) > 1e-14: dev = max(dev, abs(ex[q] - GS[name][gk][q]) / abs(ex[q]))
same_keys = set(groups) == set(GS[name])
a_, e_, c_, cp_ = (sum(v[q] for v in mine.values()) for q in ("a", "e", "c", "cp"))
LJ = lnZup_mine + BETA * a_; LP = lnZup_mine + math.log1p(e_)
u = lnZlo_mine; v = lnZlo_mine
for _ in range(200):
    u = lnZlo_mine - BETA * c_ * math.exp(lnZup_mine - u); v = lnZlo_mine - math.log1p(cp_ * math.exp(lnZup_mine - v))
lo_m, up_m = max(LJ, LP), min(u, v); lo_d, up_d = res[name]
print(f"(d) ln Z of the two models, mine (enumeration) against the driver's (transfer matrix): {lnZup_mine - lnZup_drv:+.2e}, {lnZlo_mine - lnZlo_drv:+.2e}; groups: same keys {same_keys} ({len(groups)}); "
      f"five statistics per group, largest relative deviation {dev:.1e}")
print(f"    the four bounds from my statistics (no safety factor, 200 iterations): [{lo_m:.9f}, {up_m:.9f}] against the driver's [{lo_d:.9f}, {up_d:.9f}]: differences {lo_m - lo_d:+.2e}, {up_m - up_d:+.2e}; "
      f"exact ln Z = {lnZE:.9f}, inside mine: {lo_m <= lnZE <= up_m}, inside the driver's: {lo_d <= lnZE <= up_d}")
# what the hypotheses allow at most: the sandwich of the 'source' models (everything known put back): ln Z(E - (env - r)) etc. is not computable in general; report the truth's position
D = lnZlo_drv - lnZup_drv
print(f"    D = {D:.6g}; corrected width {up_d - lo_d:.4g}; D+ = ln Z(E) - ln Z(m+) = {lnZE - lnZup_drv:.6g}, D- = {lnZlo_drv - lnZE:.6g}; first-order slack recovered: beta sum<S+> = {BETA * a_:.6g}, beta sum <S->(ceiling) = {BETA * sum(v['b'] for v in mine.values()):.6g}")
print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
