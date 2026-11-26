"""
P8 step 1(iv) -- what every sign-blind bound must pay, for the charged instances (P5's Proposition 7 / Theorem 8).

The kernel matrix M(x) does not depend on the charges; for s in {+1,-1}^N the function
    g_s(x) = (PRE/2) sum_{p,q} s_p s_q |q_p q_q| M_pq(x)
is the GBn2 energy of the same atoms with the charges s_p |q_p|.  A bound that uses the charges only through |q_p|
must hold for every s (P5, Proposition 7).  Lower bounds computed here (all are EXACT EVALUATIONS of g_s):

  (A) per subset T:  LS_T = the largest |Delta_T g_s(z; y_T)| found, <= SB_T = max_s c_T(g_s) <= PP_T (best pair-by-pair);
  (B) one pattern for all subsets: sum_T c_T(g_s) for s = all-plus and for the patterns found for the remainder;
  (C) the remainder:  sup_x |g_s - I_{m-1} g_s|(x) for the patterns found.

HOW THE SEARCH IS DONE.  For a symmetric matrix A (the mixed-difference matrix of a subset at one (context, states), or
the remainder matrix at one state), maximise |s^T A s| over sign vectors by 1-flip ascent (both signs of the objective)
from: the true signs, all-plus, the signs of the 6 eigenvectors of A with the largest |eigenvalue| (and their
negatives are equivalent), and NRAND random sign vectors; then one round of best-improving 2-flips, then 1-flips again.
(A): A at the (z, y_T) where |Delta_T g| is largest for the true charges and where it is largest for all-plus charges.
(C): A at the states with the largest true / all-plus remainders (NCAND each) and at NRS random states with at least m
changed sites; the patterns found are then evaluated at ALL states.
HOW GOOD IT IS: the result is bracketed from above by the pair-by-pair optimum; the log prints both.

usage: python3 -B p8_02_signblind.py SEQ BB TAU [--nrand 24] [--ncand 4] [--nrs 4]
needs out/m1_<tag>.npz (p8_01_measure.py).  Writes logs/sb_<tag>.log, out/sb_<tag>.json
"""
import sys, os, json, time, itertools
from math import comb
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
NRAND = int(a[a.index("--nrand") + 1]) if "--nrand" in a else 24
NCAND = int(a[a.index("--ncand") + 1]) if "--ncand" in a else 4
NRS = int(a[a.index("--nrs") + 1]) if "--nrs" in a else 4
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"sb_{tag}.log"))
t0 = time.time()
rng = np.random.default_rng(20261126)
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
st = G.product_states()
S = len(st)
x0 = tuple(int(v) for v in Z["anchor"])
assert tuple(Z["shape"]) == shape
gt = Z["g"]; ga = Z["gabs"]
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
orders = np.array([len(T) for T in Tlist]); maxorder = int(orders.max())
q = G.q.copy(); aq = np.abs(q); sg = np.where(q >= 0, 1.0, -1.0)
QQ = 0.5 * PRE * np.outer(aq, aq)                     # g_s = s^T (QQ o M) s
allrows = np.arange(N)
log(f"=== p8_02_signblind: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, {S} states, anchor {x0}; {len(Tlist)} subsets; NRAND {NRAND}, NCAND {NCAND}, NRS {NRS}")


def kernel_at(states):
    return P5.kernel_rows(G, np.atleast_2d(np.array(states)), allrows)          # (k, N, N)


def ascent(A, s, sign):
    """1-flip ascent of sign * s^T A s; returns s (modified copy)."""
    s = s.copy()
    dA = np.diag(A)
    As = A @ s
    for _ in range(40 * len(s)):
        gain = -4.0 * sign * s * (As - dA * s)
        p = int(np.argmax(gain))
        if gain[p] <= 1e-15:
            break
        s[p] = -s[p]
        As += 2.0 * A[:, p] * s[p]
    return s


def two_flip(A, s, sign):
    """one best-improving 2-flip (p, r), if any: change of s^T A s when flipping p and r together."""
    dA = np.diag(A)
    As = A @ s
    g1 = -4.0 * s * (As - dA * s)                      # change of s^T A s for a single flip
    d2 = g1[:, None] + g1[None, :] + 8.0 * A * np.outer(s, s)
    np.fill_diagonal(d2, -np.inf if sign > 0 else np.inf)
    k = int(np.argmax(sign * d2))
    p, r = divmod(k, len(s))
    if sign * d2[p, r] > 1e-15:
        s = s.copy(); s[p] = -s[p]; s[r] = -s[r]
        return s, True
    return s, False


def search(A, nrand=None):
    """best (|s^T A s|, s) over the starts described in the module docstring."""
    starts = [sg, np.ones(N)]
    w, V = np.linalg.eigh(A)
    for k in np.argsort(-np.abs(w))[:6]:
        starts.append(np.where(V[:, k] >= 0, 1.0, -1.0))
    starts += [rng.choice([-1.0, 1.0], size=N) for _ in range(NRAND if nrand is None else nrand)]
    best = (-1.0, None)
    for s_ in starts:
        for sign in (1.0, -1.0):
            s = ascent(A, s_, sign)
            for _ in range(50):
                s, moved = two_flip(A, s, sign)
                if not moved:
                    break
                s = ascent(A, s, sign)
            v = abs(float(s @ A @ s))
            if v > best[0]:
                best = (v, s)
    return best


def state_of(T, flat, dshape):
    """state carrying y_T on T and the context elsewhere, from the flat index into P5's reduced difference array D_T."""
    idx = list(np.unravel_index(flat, dshape))
    z = list(x0)
    for i in range(n):
        if i in T:
            z[i] = (1 - x0[i]) if shape[i] == 2 else int(idx[i])
        else:
            z[i] = int(idx[i])
    return z


def mixed_matrix(T, zy):
    m = len(T)
    sts, sgn_ = [], []
    for r in range(m + 1):
        for U in itertools.combinations(T, r):
            x = list(zy)
            for i in T:
                if i not in U:
                    x[i] = x0[i]
            sts.append(x); sgn_.append((-1.0) ** (m - r))
    return np.tensordot(np.array(sgn_), kernel_at(sts), axes=1)


def remainder_matrix(xs, m):
    """M(x*) - I_{m-1} M(x*) as an (N, N) matrix (inclusion-exclusion over the subsets V of S(x*), |V| < m)."""
    Sx = [i for i in range(n) if xs[i] != x0[i]]
    s_ = len(Sx)
    sts, cf = [list(xs)], [1.0]
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
        out += np.tensordot(np.array(cf[s0_:s0_ + 64]), kernel_at(sts[s0_:s0_ + 64]), axes=1)
    return out


# ------------------------------------------------------------------ (A) per subset
ctrue, cplus, arg_t, arg_p = {}, {}, {}, {}


def cbf(store, argstore):
    def cb(T, D):
        A = np.abs(D)
        k = int(np.argmax(A))
        store[T] = float(A.reshape(-1)[k]); argstore[T] = (k, D.shape)
    return cb


anch_walk(gt.reshape(shape), x0, n, maxorder, cbf(ctrue, arg_t))
anch_walk(ga.reshape(shape), x0, n, maxorder, cbf(cplus, arg_p))
LS = {}
PPT = Z["C_PP"]; P3T = Z["C_P3"]
nchk = nviol = 0
for ti, T in enumerate(Tlist):
    assert abs(ctrue[T] - Z["C_total"][ti]) < 1e-9 and abs(cplus[T] - Z["C_allplus"][ti]) < 1e-9
    best = max(ctrue[T], cplus[T])
    for (k, dsh) in (arg_t[T], arg_p[T]):
        zy = state_of(T, k, dsh)
        A = QQ * mixed_matrix(T, zy)
        v, s = search(A)
        best = max(best, v)
    LS[T] = best
    for lo_, hi_, nm in ((ctrue[T], LS[T], "truth<=LS"), (LS[T], PPT[ti], "LS<=PP"), (PPT[ti], P3T[ti], "PP<=P3")):
        nchk += 1
        if hi_ < lo_ - 1e-9:
            nviol += 1; log(f"    VIOLATION {nm} at T = {T}: {lo_} > {hi_}")
log(f"    (A) per-subset searches done, {time.time() - t0:.0f} s; chain truth <= LS_T <= PP_T <= P3: {nchk} checks, {nviol} violations")

# ------------------------------------------------------------------ (C) remainder patterns
gtg = gt.reshape(shape); gag = ga.reshape(shape)
pats = {}; rem_true = {}; rem_plus = {}; local = {}
nchg = (st != np.array(x0)[None, :]).sum(axis=1)
for m in range(3, maxorder + 1):
    rt = (gtg - anchored_interp(gtg, x0, m - 1)).reshape(-1); rp = (gag - anchored_interp(gag, x0, m - 1)).reshape(-1)
    rem_true[m] = float(np.abs(rt).max()); rem_plus[m] = float(np.abs(rp).max())
    cands = set(int(v) for v in np.argsort(-np.abs(rt))[:NCAND]) | set(int(v) for v in np.argsort(-np.abs(rp))[:NCAND])
    elig = np.flatnonzero(nchg >= m)
    if len(elig):
        cands |= set(int(v) for v in rng.choice(elig, size=min(NRS, len(elig)), replace=False))
    best = (-1.0, None)
    for k in sorted(cands):
        xs = [int(v) for v in st[k]]
        if nchg[k] < m:
            continue
        A = QQ * remainder_matrix(xs, m)
        assert abs(float(sg @ A @ sg) - rt[k]) < 1e-8 and abs(float(np.ones(N) @ A @ np.ones(N)) - rp[k]) < 1e-8
        v, s = search(A)
        if v > best[0]:
            best = (v, s)
    pats[m] = best[1]; local[m] = best[0]
    log(f"    (C) order {m}: remainder search at {len(cands)} states done, {time.time() - t0:.0f} s; largest |remainder| found at a single state: {best[0]:.4e}")

# evaluate the patterns found at ALL states
mlist = list(range(3, maxorder + 1))
Cpat = np.stack([aq * pats[m] for m in mlist], axis=1)           # (N, K) charge vectors
B = 1.0 / G.invB(G.descreening(st))
gp = np.zeros((S, len(mlist)))
for p in range(N):
    cols = np.arange(p, N)
    M = kernel_row(G, st, p, B, cols)
    w = np.full(len(cols), PRE); w[0] = 0.5 * PRE
    gp += (M @ (w[:, None] * Cpat[cols])) * Cpat[p][None, :]
    del M
log(f"    patterns evaluated at all {S} states, {time.time() - t0:.0f} s")

# ------------------------------------------------------------------ report
Gam = {}
J = json.load(open(os.path.join(HERE, "out", f"m1_{tag}.json")))
res = dict(seq=seq, bb=bb, tau=tau, natoms=N, nstates=S, orders={})
nst = nstv = 0; minratio = np.inf
for mi, m in enumerate(mlist):
    sel = np.flatnonzero(orders == m)
    if not len(sel):
        continue
    Gm = sum(J["orders"][str(m)]["Gamma"])
    gpg = gp[:, mi].reshape(shape)
    rs = (gpg - anchored_interp(gpg, x0, m - 1)).reshape(-1)
    rem_pat = float(np.abs(rs).max())
    assert rem_pat >= local[m] - 1e-9
    for arr in (gtg - anchored_interp(gtg, x0, m - 1), gag - anchored_interp(gag, x0, m - 1), rs):
        nst += S; nstv += int((np.abs(arr) > Gm + 1e-9).sum())
        mx = float(np.abs(arr).max())
        if mx > 0:
            minratio = min(minratio, Gm / mx)
    cpat = {}
    anch_walk(gpg, x0, n, m, cbf(cpat, {}), minorder=m)
    for ti in sel:
        T = Tlist[ti]
        nchk += 2
        if cpat[T] > P3T[ti] + 1e-9 or cpat[T] > PPT[ti] + 1e-9:
            nviol += 1; log(f"    VIOLATION: pattern constant above PP or P3 at T = {T}")
        LS[T] = max(LS[T], cpat[T])
    truth = float(sum(ctrue[Tlist[ti]] for ti in sel)); plus = float(sum(cplus[Tlist[ti]] for ti in sel))
    onepat = float(sum(cpat[Tlist[ti]] for ti in sel)); lsA = float(sum(LS[Tlist[ti]] for ti in sel))
    pp = float(PPT[sel].sum()); p3 = float(P3T[sel].sum())
    remC = max(rem_pat, rem_plus[m])
    rat = np.array([LS[Tlist[ti]] / ctrue[Tlist[ti]] for ti in sel if ctrue[Tlist[ti]] > 0])
    row = dict(nsub=int(len(sel)), truth_sum=truth, allplus_sum=plus, onepattern_sum=onepat, B_sum=max(plus, onepat), A_sum=lsA, PP_sum=pp, P3_sum=p3,
               rem_true=rem_true[m], rem_allplus=rem_plus[m], rem_pattern=rem_pat, C_rem=remC, Gamma=Gm,
               pattern_minus_fraction=float((pats[m] < 0).mean()), pattern_agrees_with_true_signs=float((pats[m] == sg).mean()),
               A_ratio_min=float(rat.min()), A_ratio_median=float(np.median(rat)), A_ratio_max=float(rat.max()))
    res["orders"][str(m)] = row
    log(f"--- order {m}: {len(sel)} subsets (kcal/mol)")
    log(f"    sums over subsets: truth {truth:.4e} | all-plus {plus:.4e} | remainder pattern {onepat:.4e} | (A) best pattern per subset {lsA:.4e} | best pair-by-pair {pp:.4e} | P3 {p3:.4e}")
    log(f"    (A)/truth >= {lsA / truth:.2f} [per subset min/median/max {rat.min():.2f}/{np.median(rat):.2f}/{rat.max():.2f}];  (B)/truth >= {max(plus, onepat) / truth:.2f};  "
        f"pair-by-pair/(A) <= {pp / lsA:.2f};  P3/(A) <= {p3 / lsA:.2f};  P3/pair-by-pair = {p3 / pp:.2f}")
    log(f"    remainder sup_x|g - I_{m - 1}g|: truth {rem_true[m]:.4e} | all-plus {rem_plus[m]:.4e} | pattern found {rem_pat:.4e} "
        f"({100 * row['pattern_minus_fraction']:.0f} % of the charges negative; {100 * row['pattern_agrees_with_true_signs']:.0f} % as the true signs) | Gamma_{m} {Gm:.4e}")
    log(f"    (C) every sign-blind bound of the remainder / truth >= {remC / rem_true[m]:.2f};  Gamma_{m} / (C) = {Gm / remC:.1f};  Gamma_{m} / truth = {Gm / rem_true[m]:.0f}")
log(f"    chain checks in all: {nchk}, violations {nviol}")
log(f"    P3's Gamma_m against the remainders of the sign-flipped systems (true signs, all-plus, pattern found) at every state: {nst} state checks, {nstv} violations; "
    f"smallest Gamma_m / sup|remainder| = {minratio:.2f}")
res["checks"] = dict(chain=dict(n=nchk, violations=nviol), states=dict(n=nst, violations=nstv, min_ratio=float(minratio)))
np.savez_compressed(os.path.join(HERE, "out", f"sb_{tag}.npz"), patterns=np.stack([pats[m] for m in mlist]), orders=np.array(mlist), gp=gp)
with open(os.path.join(HERE, "out", f"sb_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
