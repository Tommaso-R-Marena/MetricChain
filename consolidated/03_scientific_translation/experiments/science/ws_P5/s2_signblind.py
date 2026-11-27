"""
P5 step 2 (real instances) -- what EVERY sign-blind bound must pay.

The kernel matrix M(x) of the GB energy does not depend on the charges, so for a sign pattern
s in {+1,-1}^N the function  g_s(x) = -(KAPPA/2) (s o q)^T M(x) (s o q)  is the GB energy of the
same geometry with the charges s_p q_p.  A bound that depends on the charges only through |q_p|
(every term-by-term bound does; P3's Gamma_m does) is the same number for all s and must be valid
for all s.  Hence, for every s, every subset T and every state:

    (per subset)   beta_T    >=  c_T^anch(g_s)            and so  >=  max_s c_T^anch(g_s)  =: SB_T
    (remainder)    beta_rem  >=  sup_x |g_s - I_{m-1} g_s|(x)

This script computes, by exact enumeration,
  * the truth (s = sign of the real charges) and the all-plus pattern (charges |q_p|);
  * per subset T: a 1-flip local search over s at the state where the true (and where the all-plus)
    mixed difference is largest -> LS_T <= SB_T  (a certified lower bound: it is an exact evaluation);
  * per order m: a local search over s for the remainder at a few states, the patterns found are then
    evaluated at ALL states;
  * CHECKS of P3's bound on the sign-flipped systems (it must hold there, being sign-blind):
    c_T^anch(g_s) <= chat_T for all T, and |g_s - I_{m-1} g_s|(x) <= Gamma_m at every state x,
    for s = all-plus and for the patterns found.

usage: python3 -B s2_signblind.py SEQ BB TAU [maxorder=5] [--blk DOUBLES] [--nrand R] [--lsmax K] [--ncand C] [--nrandrem R2]
       (--ncand C: the remainder search also starts from the C states with the largest true and the C with the largest
        all-plus remainder; --nrandrem R2: random starts of the remainder search, default R)
       (--lsmax K: the per-subset search (A) only for subsets of order <= K; above K the per-subset lower bound is the
        larger of the all-plus pattern and the pattern found for the remainder, and the log says so)
needs out/s1_<tag>.json (pair-level optimum and P3's per-subset bounds).
"""
import sys, os, json, time, itertools
import numpy as np
from p5lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
maxorder = int(a[3]) if len(a) > 3 and not a[3].startswith("--") else 5
BLK = float(a[a.index("--blk") + 1]) if "--blk" in a else 6e7
NRAND = int(a[a.index("--nrand") + 1]) if "--nrand" in a else 30
LSMAX = int(a[a.index("--lsmax") + 1]) if "--lsmax" in a else 99      # per-subset local search only up to this order
NCAND = int(a[a.index("--ncand") + 1]) if "--ncand" in a else 0        # extra candidate states for the remainder search
NRANDREM = int(a[a.index("--nrandrem") + 1]) if "--nrandrem" in a else NRAND
tag = f"{seq}_{bb}_{tau:.2f}"
log = Tee(os.path.join(HERE, "logs", f"s2_{tag}.log"))
t0 = time.time()
rng = np.random.default_rng(20261126)
G, st, shape, f, g, E, x0 = build(seq, bb, tau)
n, N, S = G.ns, G.nat, len(st)
maxorder = min(maxorder, n)
s1 = json.load(open(os.path.join(HERE, "out", f"s1_{tag}.json")))
log(f"=== s2_signblind: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, domain {list(shape)} = {S} states; anchor {x0}")
q = G.q.copy()
aq = np.abs(q)
sg = np.where(q >= 0, 1.0, -1.0)
Tlist = subsets(n, shape, 3, maxorder)
Bfull = 1.0 / G.invB(G.descreening(st))
Xfull = G.coords(st)
PRE = -0.5 * KAPPA / KCAL
allrows = np.arange(N)


def energies(patterns):
    """g_c(x) at all states for charge vectors c (K, N): (K, S)."""
    patterns = np.atleast_2d(patterns)
    out = np.zeros((patterns.shape[0], S))
    R = max(1, min(N, int(BLK // (S * N))))
    for s_ in range(0, N, R):
        rows = np.arange(s_, min(N, s_ + R))
        M = kernel_rows(G, st, rows, Bfull, Xfull)
        out += PRE * np.einsum("kp,spq,kq->ks", patterns[:, rows], M, patterns, optimize=True)
    return out


def kernel_at(states):
    states = np.atleast_2d(states)
    return kernel_rows(G, states, allrows)                       # (m, N, N), own Born radii from the tables


def local_search(A, s_start):
    """1-flip ascent for |s^T A s| (A symmetric), both signs of the objective; returns (best |value|, s)."""
    best = (-1.0, None)
    dA = np.diag(A).copy()
    for sign in (1.0, -1.0):
        s = s_start.copy()
        As = A @ s
        for _ in range(20 * len(s)):
            gain = -4.0 * sign * s * (As - dA * s)
            p = int(np.argmax(gain))
            if gain[p] <= 1e-14:
                break
            s[p] = -s[p]
            As += 2.0 * A[:, p] * s[p]
        v = abs(float(s @ A @ s))
        if v > best[0]:
            best = (v, s.copy())
    return best


def search(A, nrand=None):
    best = (-1.0, None)
    starts = [sg, np.ones(N)] + [rng.choice([-1.0, 1.0], size=N) for _ in range(NRAND if nrand is None else nrand)]
    for s_ in starts:
        v, s = local_search(A, s_)
        if v > best[0]:
            best = (v, s)
    return best


def unravel_T(T, flat, dshape):
    """(z, y_T) of the flat index into the reduced array D_T (axes of two-state sites in T have length 1)."""
    idx = list(np.unravel_index(flat, dshape))
    z = list(x0)
    for i in range(n):
        if i in T:
            z[i] = (1 - x0[i]) if shape[i] == 2 else int(idx[i])
        else:
            z[i] = int(idx[i])
    return z                                                       # state with y_T at T and the context elsewhere


def mixed_matrix(T, zy):
    """A = Delta_T M (z; x0_T -> y_T) as an (N, N) matrix; zy = the state carrying y_T on T."""
    m = len(T)
    sts, sgn_ = [], []
    for r in range(m + 1):
        for U in itertools.combinations(T, r):
            x = list(zy)
            for i in T:
                if i not in U:
                    x[i] = x0[i]
            sts.append(x); sgn_.append((-1.0) ** (m - r))
    K = kernel_at(np.array(sts))
    return np.tensordot(np.array(sgn_), K, axes=1)


gt, ga = energies(np.stack([q, aq]))
err = float(np.abs(gt - g.reshape(-1)).max())
log(f"    check: quadratic form with the real charges = P3's evaluator at all {S} states to {err:.2e} kcal/mol")
assert err < 1e-8
res = dict(seq=seq, bb=bb, tau=tau, natoms=N, n=n, nstates=S)

# ------------------------------------------------------------------ per subset
ctrue, cplus, arg_t, arg_p = {}, {}, {}, {}


def cb_factory(store, argstore):
    def cb(T, D):
        A = np.abs(D)
        k = int(np.argmax(A))
        store[T] = float(A.reshape(-1)[k]); argstore[T] = (k, D.shape)
    return cb


anch_walk(gt.reshape(shape), x0, n, maxorder, cb_factory(ctrue, arg_t))
anch_walk(ga.reshape(shape), x0, n, maxorder, cb_factory(cplus, arg_p))
LS, LSpat = {}, {}
qq = np.outer(aq, aq)
nchk = nviol = 0
for T in Tlist:
    best = (-1.0, None)
    for (k, dsh) in ((arg_t[T], arg_p[T]) if len(T) <= LSMAX else ()):
        zy = unravel_T(T, k, dsh)
        A = PRE * qq * mixed_matrix(T, zy)
        vt = abs(float(sg @ A @ sg))
        v, s = search(A)
        if v > best[0]:
            best = (v, s)
    LS[T] = max(best[0], cplus[T], ctrue[T]); LSpat[T] = best[1]
    key = "-".join(map(str, T))
    # consistency with step 1 and the chain  truth <= LS <= SB <= pair-level optimum <= P3
    p3T = s1["per_subset"]["P3"].get(key, np.inf)                 # absent above --p3max of s1_cancel.py
    for lo_, hi_, nm in ((ctrue[T], LS[T], "truth<=LS"), (LS[T], s1["per_subset"]["pair"][key], "LS<=pair"),
                         (s1["per_subset"]["pair"][key], p3T, "pair<=P3"),
                         (cplus[T], p3T, "allplus<=P3")):
        nchk += 1
        if hi_ < lo_ - 1e-9:
            nviol += 1; log(f"    VIOLATION {nm} at T={T}: {lo_} > {hi_}")
    assert abs(ctrue[T] - s1["per_subset"]["total"][key]) < 1e-9
log(f"    per-subset searches done, {time.time() - t0:.0f} s; chain checks (truth <= LS <= pair optimum <= P3; all-plus <= P3): {nchk} checks, {nviol} violations")

# ------------------------------------------------------------------ remainder level
def interp(garr, m):
    return anchored_interp(garr.reshape(shape), x0, m - 1).reshape(-1)


def remainder_matrix(xs, m):
    """Rmat = M(x*) - I_{m-1} M (x*) (N, N): sum over V subset S(x*), |V| < m, of coef_V * M(x*_V, x0)."""
    Sx = [i for i in range(n) if xs[i] != x0[i]]
    s_ = len(Sx)
    sts, cf = [list(xs)], [1.0]
    from math import comb
    for r in range(0, min(m - 1, s_) + 1):
        c = sum((-1) ** j * comb(s_ - r, j) for j in range(0, m - 1 - r + 1))
        if c == 0:
            continue
        for V in itertools.combinations(Sx, r):
            x = list(x0)
            for i in V:
                x[i] = xs[i]
            sts.append(x); cf.append(-float(c))
    out = np.zeros((N, N))
    for s0_ in range(0, len(sts), 64):
        K = kernel_at(np.array(sts[s0_:s0_ + 64]))
        out += np.tensordot(np.array(cf[s0_:s0_ + 64]), K, axes=1)
    return out


pats = {}
rem_true, rem_plus = {}, {}
for m in range(3, maxorder + 1):
    rt = gt - interp(gt, m); rp = ga - interp(ga, m)
    rem_true[m] = float(np.abs(rt).max()); rem_plus[m] = float(np.abs(rp).max())
    cands = {int(np.argmax(np.abs(rt))), int(np.argmax(np.abs(rp))), int(np.ravel_multi_index([sh - 1 - x for sh, x in zip(shape, x0)] if all(sh == 2 for sh in shape) else [0 if x != 0 else 1 for x in x0], shape))}
    if NCAND:
        cands |= set(int(v) for v in np.argsort(-np.abs(rt))[:NCAND]) | set(int(v) for v in np.argsort(-np.abs(rp))[:NCAND])
    best = (-1.0, None)
    for k in sorted(cands):
        xs = [int(v) for v in st[k]]
        if sum(1 for i in range(n) if xs[i] != x0[i]) < m:
            continue
        A = PRE * qq * remainder_matrix(xs, m)
        chk = abs(float(sg @ A @ sg) - rt[k])
        assert chk < 1e-8, chk                                 # the matrix reproduces the true remainder at x*
        v, s = search(A, NRANDREM)
        if v > best[0]:
            best = (v, s)
    pats[m] = best[1]
gp = energies(np.stack([aq * pats[m] for m in range(3, maxorder + 1)]))
log(f"    remainder searches done, {time.time() - t0:.0f} s")

# ------------------------------------------------------------------ report + checks of P3's bound on sign-flipped systems
Gam = {int(m): sum(v) for m, v in s1["Gamma"].items()}
nst = nstv = 0; minratio = np.inf
out_rows = {}
for mi, m in enumerate(range(3, maxorder + 1)):
    Tm = [T for T in Tlist if len(T) == m]
    if not Tm:
        continue
    rs = gp[mi] - interp(gp[mi], m)
    rem_ls = float(np.abs(rs).max())
    # P3's Gamma_m must bound the remainder of every sign pattern at every state
    for arr in (gt - interp(gt, m), ga - interp(ga, m), rs):
        nst += S
        bad = int((np.abs(arr) > Gam[m] + 1e-9).sum())
        nstv += bad
        mx = float(np.abs(arr).max())
        if mx > 0:
            minratio = min(minratio, Gam[m] / mx)
    # per-subset constants of the pattern found for the remainder (one pattern for all T)
    cpat = {}
    anch_walk(gp[mi].reshape(shape), x0, n, m, cb_factory(cpat, {}), minorder=m)
    nsub = nsubv = 0
    for T in Tm:
        key = "-".join(map(str, T))
        nsub += 1
        if cpat[T] > s1["per_subset"]["P3"].get(key, np.inf) + 1e-9:
            nsubv += 1
        if cpat[T] > LS[T]:
            LS[T] = cpat[T]                                    # the remainder pattern is one more admissible sign pattern
        nsub += 1
        if LS[T] > s1["per_subset"]["pair"][key] + 1e-9:
            nsubv += 1
    k = lambda name: s1["sums"][str(m)][name]
    row = dict(n_subsets=len(Tm), truth_sum=sum(ctrue[T] for T in Tm), allplus_sum=sum(cplus[T] for T in Tm),
               onepattern_sum=sum(cpat[T] for T in Tm), LS_sum=sum(LS[T] for T in Tm), pair_sum=k("pair"), P3_sum=k("P3"),
               rem_true=rem_true[m], rem_allplus=rem_plus[m], rem_LS=max(rem_ls, rem_plus[m]), Gamma=Gam[m],
               pattern_minus_fraction=float((pats[m] < 0).mean()), per_subset_search=bool(m <= LSMAX))
    rat = np.array([LS[T] / ctrue[T] for T in Tm if ctrue[T] > 0])
    row.update(LS_ratio_min=float(rat.min()), LS_ratio_median=float(np.median(rat)), LS_ratio_max=float(rat.max()))
    out_rows[str(m)] = row
    log(f"--- order {m}: {len(Tm)} subsets (kcal/mol)")
    if m > LSMAX:
        log(f"    (order {m} > --lsmax {LSMAX}: no per-subset search; 'best pattern per T' = max(all-plus, remainder pattern) only)")
    log(f"    sum over subsets:  truth {row['truth_sum']:.4e} | all-plus charges {row['allplus_sum']:.4e} | one pattern for all T {row['onepattern_sum']:.4e} | "
        f"best pattern per T (local search), a lower bound of the sign-blind optimum {row['LS_sum']:.4e} | pair-level optimum {row['pair_sum']:.4e} | P3 {row['P3_sum']:.4e}")
    log(f"    every sign-blind per-subset bound / truth >= {row['LS_sum'] / row['truth_sum']:.1f} (sums); per subset min/median/max {rat.min():.1f} / {np.median(rat):.1f} / {rat.max():.1f};"
        f"  P3 / lower bound of the sign-blind optimum <= {row['P3_sum'] / row['LS_sum']:.1f}")
    log(f"    remainder sup_x |g - I_{m - 1} g|:  truth {row['rem_true']:.4e} | all-plus {row['rem_allplus']:.4e} | pattern found {rem_ls:.4e} "
        f"({100 * row['pattern_minus_fraction']:.0f}% of the charges negative) | P3's Gamma_{m} {Gam[m]:.4e}")
    log(f"    every sign-blind bound of the remainder / truth >= {row['rem_LS'] / row['rem_true']:.1f};  Gamma_{m} / that lower bound = {Gam[m] / row['rem_LS']:.1f}")
    log(f"    checks c_T(g_s) <= chat_T for the remainder pattern, and lower bound <= pair-level optimum: {nsub} checks, {nsubv} violations")
    nchk += nsub; nviol += nsubv
log(f"    P3's Gamma_m against the remainders of sign-flipped systems (true signs, all-plus, pattern found) at every state: "
    f"{nst} state checks, {nstv} violations; smallest ratio Gamma_m / sup|remainder| = {minratio:.2f}")
res.update(orders=out_rows, chain_checks=dict(n=nchk, violations=nviol), state_checks=dict(n=nst, violations=nstv, min_ratio=minratio))
with open(os.path.join(HERE, "out", f"s2_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
