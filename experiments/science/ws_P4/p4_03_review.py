"""
P4 item 3: numerical checks that accompany the review of Theorem 11.18a and Propositions 11.18b,
11.18c (theory report at 24a3c27, section 11.7).  Everything here is my own code (no code of the
theory division is run); small random instances, brute force and small linear programmes.

Blocks (each prints its counts; an assertion failure would be a counterexample or a bug):
  A  Theorem 11.18a (a)-(d): I_2 g is exact on the ball; remainder bound; coverings (site thirds,
     pair thirds, random mixed shares); pointwise order site <= pair <= envelope; (d) attainment by
     a linear programme over the class; share-based coverings do not exhaust the coverings of (b).
  B  Proposition 11.18b (a), (b): criterion (enumeration)  <=>  no over-dense set  <=>  shares (flow),
     for every alphabet size, with ties (integer data) and single-state sites.
  C  Proposition 11.18b (c): triples -- shares among three sites <=> no set over-dense w.r.t. the
     triples <=> x0 minimises the three-body envelope when all pair terms vanish.
  D  Proposition 11.18b (d): sufficiency on random pairwise known parts; how often it is not
     necessary and by which mechanism; an explicit two-site example.
  E  Proposition 11.18c (a)-(c): D' is reset-closed and the largest such part; remainder bounds on
     D' with constants over the boxes inside D'; the counterexample {00, 01, 11}; values on D \\ D'
     are unconstrained (LP unbounded) even given ALL values on D';
     and a counterexample to "Proposition 11.18b(b) holds verbatim on a reset-closed domain".
  F  cross-check of my fast class constants (p4lib.c2_matrix, c3_dict) against brute force over boxes.
  G  state-dependent shares exist  <=>  the reference solves the local-polytope relaxation of min L.

usage: python3 -B p4_03_review.py     (about a minute; last line "DONE p4_03_review")
"""
import sys, math, itertools, time
import numpy as np
from scipy.optimize import linprog
import scipy.sparse as sp
import p4lib as L4
from p4lib import Fraction

t00 = time.time()
rng = np.random.default_rng(20261126)


def states(shape):
    return list(itertools.product(*[range(k) for k in shape]))


def boxes(shape, T, mask=None):
    """all boxes over the sites T: yields list of (index tuple, sign) for the 2^|T| corners;
    base = any assignment of the other sites, two distinct states a < a' at each site of T.
    If mask is given, only boxes with all corners inside the mask."""
    n = len(shape)
    others = [i for i in range(n) if i not in T]
    for base in itertools.product(*[range(shape[i]) for i in others]):
        for prs in itertools.product(*[list(itertools.combinations(range(shape[i]), 2)) for i in T]):
            corners = []
            ok = True
            for bits in itertools.product((0, 1), repeat=len(T)):
                x = [0] * n
                for i, v in zip(others, base):
                    x[i] = v
                for t, b in zip(range(len(T)), bits):
                    x[T[t]] = prs[t][b]
                x = tuple(x)
                if mask is not None and not mask[x]:
                    ok = False
                    break
                corners.append((x, (-1) ** (len(T) - sum(bits))))
            if ok:
                yield corners


def brute_const(g, T, mask=None):
    best = 0.0
    for corners in boxes(g.shape, T, mask):
        best = max(best, abs(sum(s * g[x] for x, s in corners)))
    return best


def hamming(x, x0):
    return sum(1 for a, b in zip(x, x0) if a != b)


def class_lp_min(g, x0, order, const, xstar, mask=None, fixed=None):
    """min of g'(xstar) over all g' on the domain (mask; default the whole product) whose mixed
    differences of the given order over every box inside the domain are bounded by const[T], and
    with g' = g on `fixed` (default: the Hamming ball of radius order-1 around x0, inside the domain).
    Returns (status, value)."""
    shape = g.shape
    S = [x for x in states(shape) if mask is None or mask[x]]
    idx = {x: k for k, x in enumerate(S)}
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for T in itertools.combinations(range(len(shape)), order):
        for corners in boxes(shape, T, mask):
            for sgn in (1.0, -1.0):
                for x, s in corners:
                    rows.append(r); cols.append(idx[x]); vals.append(sgn * s)
                rhs.append(const[T]); r += 1
    if fixed is None:
        fixed = [x for x in S if hamming(x, x0) <= order - 1]
    Aeq = sp.csr_matrix((np.ones(len(fixed)), (np.arange(len(fixed)), [idx[x] for x in fixed])), shape=(len(fixed), len(S)))
    beq = np.array([g[x] for x in fixed])
    c = np.zeros(len(S)); c[idx[xstar]] = 1.0
    Aub = sp.csr_matrix((vals, (rows, cols)), shape=(r, len(S))) if r else None
    res = linprog(c, A_ub=Aub, b_ub=(np.array(rhs) if r else None), A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * len(S), method="highs")
    return res.status, (float(res.fun) if res.status == 0 else None)


# =========================================================================================== A
print("A. Theorem 11.18a")
st = dict(inst=0, pts=0, ball_err=0.0, worst_rem_slack=math.inf, rem_tight=0, cover_checks=0, order_viol=0, mixed_viol=0, lp=0, lp_err=0.0)
for it in range(120):
    n = int(rng.integers(3, 6))
    ks = [int(k) for k in rng.integers(2, 4, size=n)]
    g = np.zeros(ks)
    for (i, j) in itertools.combinations(range(n), 2):
        sh = [1] * n; sh[i] = ks[i]; sh[j] = ks[j]
        g = g + rng.normal(size=(ks[i], ks[j])).reshape(sh)
    kind = it % 3
    if kind == 0:
        g = g + 0.2 * rng.normal(size=ks)
    elif kind == 1:
        for T in itertools.combinations(range(n), 3):
            if rng.random() < 0.6:
                sh = [1] * n
                for s in T:
                    sh[s] = ks[s]
                g = g + rng.normal(size=[ks[s] for s in T]).reshape(sh) * 0.3
    else:
        g = rng.normal(size=ks)
    x0 = tuple(int(rng.integers(0, k)) for k in ks)
    c3 = L4.c3_dict(g)
    I2 = L4.interp2(g, x0)
    pen = L4.triple_penalty(ks, x0, c3)
    gam = np.zeros(n); gam2 = np.zeros((n, n)); gs_m = np.zeros(n); g2_m = np.zeros((n, n))
    for T, v in c3.items():
        lam = rng.dirichlet(np.ones(6))                       # random mixed shares: 3 sites, 3 pairs
        prs = ((T[0], T[1]), (T[0], T[2]), (T[1], T[2]))
        for q, s in enumerate(T):
            gam[s] += v / 3; gs_m[s] += v * lam[q]
        for q, (u, w) in enumerate(prs):
            gam2[u, w] += v / 3; gam2[w, u] += v / 3
            g2_m[u, w] += v * lam[3 + q]; g2_m[w, u] += v * lam[3 + q]
    p_site = L4.site_penalty(ks, x0, gam); p_pair = L4.pair_penalty(ks, x0, gam2)
    p_mix = L4.site_penalty(ks, x0, gs_m) + L4.pair_penalty(ks, x0, g2_m)
    for x in states(ks):
        st["pts"] += 1
        if hamming(x, x0) <= 2:
            st["ball_err"] = max(st["ball_err"], abs(g[x] - I2[x]))
        sl = pen[x] - abs(g[x] - I2[x])
        st["worst_rem_slack"] = min(st["worst_rem_slack"], sl)
        if abs(sl) < 1e-9 and pen[x] > 1e-6:
            st["rem_tight"] += 1
        assert sl >= -1e-9, ("remainder bound violated", ks, x0, x)
        st["cover_checks"] += 3
        assert p_site[x] >= p_pair[x] - 1e-12 and p_pair[x] >= pen[x] - 1e-12, ("order site >= pair >= triples violated", ks, x)
        assert p_mix[x] >= pen[x] - 1e-12, ("mixed shares do not cover", ks, x)
    # (d) attainment: LP over the class for small instances
    if int(np.prod(ks)) <= 36 and st["lp"] < 25:
        cT = {T: v for T, v in c3.items()}
        xs = states(ks)
        for x in [xs[int(k)] for k in rng.choice(len(xs), size=min(4, len(xs)), replace=False)]:
            status, val = class_lp_min(g, x0, 3, cT, x)
            assert status == 0
            st["lp"] += 1
            st["lp_err"] = max(st["lp_err"], abs(val - (I2[x] - pen[x])))
    st["inst"] += 1
assert st["ball_err"] < 1e-9 and st["lp_err"] < 1e-7
print("   ", st)
# share-based coverings do not exhaust the coverings of 11.18a(b): n = 4, triples {0,1,2} and {0,1,3} with c = 1
cT = {(0, 1, 2): 1.0, (0, 1, 3): 1.0, (0, 2, 3): 0.0, (1, 2, 3): 0.0}
gpair = {(0, 1): 1.0, (2, 3): 1.0}
ok = True
for r in range(5):
    for S in itertools.combinations(range(4), r):
        need = sum(v for T, v in cT.items() if set(T) <= set(S))
        have = sum(v for p, v in gpair.items() if set(p) <= set(S))
        ok = ok and have >= need
five = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3)]
cover_sum = sum(sum(v for p, v in gpair.items() if set(p) <= set(S)) for S in five)
share_sums = []
for _ in range(200):                                            # random share allocations (pair shares of each triple, summing to one)
    a = rng.dirichlet(np.ones(3)); d = rng.dirichlet(np.ones(3))
    gsh = {(0, 1): a[0] + d[0], (0, 2): a[1], (1, 2): a[2], (0, 3): d[1], (1, 3): d[2]}
    share_sums.append(sum(sum(v for p, v in gsh.items() if set(p) <= set(S)) for S in five))
print(f"    n = 4, triples {{0,1,2}}, {{0,1,3}} with c = 1: the penalties gamma_01 = gamma_23 = 1 cover every set of sites: {ok}; "
      f"sum of the penalties of the five two-site sets other than {{2,3}}: {cover_sum:.0f} for this cover, "
      f"{min(share_sums):.6f}..{max(share_sums):.6f} for 200 random share allocations (identically 2: the shares of each triple add up to one) "
      f"-> the cover is not dominated by any share-based covering")
assert ok and cover_sum == 1 and abs(min(share_sums) - 2) < 1e-12

# with the best pair shares the margin of the pairwise model need not reach that of the three-body envelope:
# three sites, two changed states each; each pair of sites is cheap in one combination of states only, and the
# three combinations exclude one another; one triple with c = 1
ks = [3, 3, 3]; x0 = (0, 0, 0)
Bm = np.zeros(ks)
for i in range(3):
    sh = [1] * 3; sh[i] = 3
    Bm = Bm + np.array([0.0, 1.0, 1.0]).reshape(sh)
J01 = np.zeros((3, 3)); J01[1, 1] = -1.5
J12 = np.zeros((3, 3)); J12[2, 1] = -1.5
J02 = np.zeros((3, 3)); J02[2, 2] = -1.5
Bm = Bm + J01[:, :, None] + J12[None, :, :] + J02[:, None, :]
ch = L4.changed(ks, x0)
env = Bm - ch[0] * ch[1] * ch[2]
BS = {}
for x in states(ks):
    S = tuple(i for i in range(3) if x[i] != 0)
    BS[S] = min(BS.get(S, math.inf), Bm[x])
# LP over the pair shares mu_01, mu_02, mu_12 (sum 1): maximise t with B(pair) - mu_pair >= t, B(single) >= t, B(triple) - 1 >= t
res = linprog([0, 0, 0, -1.0], A_ub=[[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]], b_ub=[BS[(0, 1)], BS[(0, 2)], BS[(1, 2)]],
              A_eq=[[1, 1, 1, 0]], b_eq=[1.0], bounds=[(0, None)] * 3 + [(None, min(BS[(0,)], BS[(1,)], BS[(2,)], BS[(0, 1, 2)] - 1.0))], method="highs")
print(f"    three sites with two changed states: least unpenalised values B(single) = {BS[(0,)]:.1f}, B(pair) = {BS[(0, 1)]:.1f}, {BS[(0, 2)]:.1f}, {BS[(1, 2)]:.1f}, B(triple) = {BS[(0, 1, 2)]:.1f}; "
      f"margin of the three-body envelope {L4.margin_at(env, x0):.4f}; best margin over pair shares (LP) {res.x[-1]:.4f}")
assert abs(L4.margin_at(env, x0) - 0.5) < 1e-12 and abs(res.x[-1] - 1.0 / 6.0) < 1e-9

# =========================================================================================== B
print("B. Proposition 11.18b (a), (b): additive known part")
st = dict(inst=0, exact=0, dense_ok=0, flow_ok=0, rowsum=0, ties=0, single_state_sites=0, neg_delta=0)
for it in range(1500):
    n = int(rng.integers(2, 7))
    ks = [int(k) for k in rng.integers(1, 5, size=n)]
    if it % 2 == 0:                                            # integer data: ties occur
        c = rng.integers(0, 4, size=(n, n)).astype(float)
        A = [rng.integers(0 if it % 4 else -1, 6, size=k).astype(float) for k in ks]
    else:
        c = rng.random((n, n)) * rng.choice([0.3, 1.0, 2.0])
        A = [rng.random(k) * 3 for k in ks]
    c = np.triu(c, 1); c = c + c.T
    if it % 7 == 0:
        c[rng.random((n, n)) < 0.5] = 0.0; c = np.triu(c, 1); c = c + c.T
    x0 = tuple(int(rng.integers(0, k)) for k in ks)
    for i in range(n):
        A[i][x0[i]] = 0.0
    Delta = L4.min_excitation(A, x0)
    st["single_state_sites"] += sum(1 for k in ks if k == 1)
    st["neg_delta"] += any(d < 0 for d in Delta)
    # criterion by enumeration: L(x) - L(x0) = sum_{changed} A_i(x_i) - sum_{changed pairs} c_ij
    Lm = np.zeros(ks)
    for i in range(n):
        sh = [1] * n; sh[i] = ks[i]
        Lm = Lm + np.asarray(A[i]).reshape(sh)
    Lm = Lm - L4.pair_penalty(ks, x0, c)
    exact = bool(Lm.min() >= Lm[x0])                           # exact arithmetic for the integer half; floats otherwise
    bf, bfS = L4.densest_excess(c, Delta)
    dense_ok = bool(bf <= 0)
    cz = c.copy()
    for i in range(n):
        if ks[i] == 1:
            cz[i, :] = 0; cz[:, i] = 0                          # a single-state site is never changed
    fl = L4.share_flow(cz, Delta)
    if fl["ok"]:
        assert L4.verify_shares(cz, Delta, fl["s"])
    else:
        assert L4.verify_overdense(cz, Delta, fl["S"])
    bf2, _ = L4.densest_excess(cz, Delta)
    assert exact == (bf2 <= 0) == fl["ok"], ("11.18b(b) fails", ks, x0, c, A)
    if it % 2 == 0 and abs(bf2) == 0.0 and any(k > 1 for k in ks):
        st["ties"] += 1
    rs = L4.rowsum_ok(cz, Delta)
    assert (not rs) or fl["ok"]
    st["inst"] += 1; st["exact"] += exact; st["dense_ok"] += bool(bf2 <= 0); st["flow_ok"] += fl["ok"]; st["rowsum"] += rs
print("   ", st)

# =========================================================================================== C
print("C. Proposition 11.18b (c): triples")
st = dict(inst=0, exact=0, dense_ok=0, lp_ok=0, thirds=0)
for it in range(400):
    n = int(rng.integers(3, 7))
    ks = [int(k) for k in rng.integers(2, 4, size=n)]
    trip = list(itertools.combinations(range(n), 3))
    cT = {T: float(rng.integers(0, 4)) if rng.random() < 0.7 else 0.0 for T in trip}
    x0 = tuple(0 for _ in ks)
    A = [np.r_[0.0, rng.integers(0, 7, size=k - 1).astype(float)] for k in ks]
    Delta = L4.min_excitation(A, x0)
    Lm = np.zeros(ks)
    for i in range(n):
        sh = [1] * n; sh[i] = ks[i]
        Lm = Lm + np.asarray(A[i]).reshape(sh)
    Lm = Lm - L4.triple_penalty(ks, x0, cT)
    exact = bool(Lm.min() >= Lm[x0])
    dense_ok = True
    for r in range(1, n + 1):
        for S in itertools.combinations(range(n), r):
            if sum(v for T, v in cT.items() if set(T) <= set(S)) > sum(Delta[i] for i in S):
                dense_ok = False
    # LP: shares lam_{T,i} >= 0, sum_i lam_{T,i} >= c_T, loads <= Delta_i; maximise the least slack
    nv = 3 * len(trip)
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for q, T in enumerate(trip):
        for u in range(3):
            rows.append(r); cols.append(3 * q + u); vals.append(-1.0)
        rhs.append(-cT[T]); r += 1
    for i in range(n):
        for q, T in enumerate(trip):
            if i in T:
                rows.append(r); cols.append(3 * q + T.index(i)); vals.append(1.0)
        rows.append(r); cols.append(nv); vals.append(1.0)
        rhs.append(Delta[i]); r += 1
    res = linprog(np.r_[np.zeros(nv), -1.0], A_ub=sp.csr_matrix((vals, (rows, cols)), shape=(r, nv + 1)), b_ub=np.array(rhs),
                  bounds=[(0, None)] * nv + [(None, None)], method="highs")
    lp_ok = bool(res.status == 0 and res.x[-1] >= -1e-9)
    assert exact == dense_ok == lp_ok, ("11.18b(c) fails", ks, cT, A)
    thirds = all(sum(v for T, v in cT.items() if i in T) / 3 <= Delta[i] for i in range(n))
    assert (not thirds) or lp_ok
    st["inst"] += 1; st["exact"] += exact; st["dense_ok"] += dense_ok; st["lp_ok"] += lp_ok; st["thirds"] += thirds
print("   ", st)

# =========================================================================================== D
print("D. Proposition 11.18b (d): pairwise known part")
st = dict(inst=0, exact=0, rowsum=0, shares=0, exact_no_shares=0, of_which_state_shares=0, binary_inst=0, binary_exact=0, binary_shares=0)
for it in range(600):
    n = int(rng.integers(2, 6))
    binary = it % 3 == 0
    ks = [2] * n if binary else [int(k) for k in rng.integers(2, 5, size=n)]
    x0 = tuple(0 for _ in ks)
    A = [np.r_[0.0, rng.random(k - 1) * 2.0 + 0.05] for k in ks]
    c = rng.random((n, n)) * rng.choice([0.2, 0.6, 1.2]); c = np.triu(c, 1); c = c + c.T
    Tt = {}
    for (i, j) in itertools.combinations(range(n), 2):
        t = rng.normal(size=(ks[i], ks[j])) * rng.choice([0.0, 0.3, 1.0])
        t[0, :] = 0; t[:, 0] = 0
        Tt[(i, j)] = t
    Tpair = lambda i, j: Tt[(i, j)]
    Lm = np.zeros(ks)
    for i in range(n):
        sh = [1] * n; sh[i] = ks[i]
        Lm = Lm + A[i].reshape(sh)
    for (i, j), t in Tt.items():
        sh = [1] * n; sh[i] = ks[i]; sh[j] = ks[j]
        Lm = Lm + t.reshape(sh)
    Lm = Lm - L4.pair_penalty(ks, x0, c)
    exact = bool(Lm.min() >= Lm[x0] - 1e-12)
    Delta = L4.min_excitation(A, x0)
    w = L4.deficits(c, Tpair, x0, ks)
    fl = L4.share_flow(w, Delta)
    rs = L4.rowsum_ok(w, Delta)
    if fl["ok"]:
        assert L4.verify_shares(w, Delta, fl["s"])
        assert exact, ("11.18b(d): shares exist and x0 does not minimise L", ks, c, Tt, A)
    assert (not rs) or fl["ok"]
    st["inst"] += 1; st["exact"] += exact; st["rowsum"] += rs; st["shares"] += fl["ok"]
    if binary:
        st["binary_inst"] += 1; st["binary_exact"] += exact; st["binary_shares"] += fl["ok"]
    if exact and not fl["ok"]:
        st["exact_no_shares"] += 1
        t, ss = L4.state_shares_lp(c, Tpair, A, x0, ks)
        if ss is not None:
            sl = L4.verify_state_shares(c, Tpair, A, x0, ks, ss)
            if sl is not None and sl >= 0:
                st["of_which_state_shares"] += 1
print("   ", st)
# explicit two-site example: one pair; the states that realise the deficit are not the cheapest states
ks = [3, 3]; x0 = (0, 0)
A = [np.array([0.0, 1.0, 5.0]), np.array([0.0, 1.0, 5.0])]
Tm = np.zeros((3, 3)); Tm[2, 2] = -4.0
c = np.array([[0.0, 1.0], [1.0, 0.0]])
Lm = A[0][:, None] + A[1][None, :] + Tm - L4.pair_penalty(ks, x0, c)
w = L4.deficits(c, lambda i, j: Tm, x0, ks)
fl = L4.share_flow(w, L4.min_excitation(A, x0))
t, ss = L4.state_shares_lp(c, lambda i, j: Tm, A, x0, ks)
print(f"    two sites, three states: A = (0,1,5) twice, T(2,2) = -4, c = 1: min_(x != x0) L - L(x0) = {L4.margin_at(Lm, x0):.1f} (criterion holds); "
      f"deficit w_01 = {w[0,1]:.1f}, Delta = (1, 1): shares exist: {fl['ok']} (over-dense {fl['S']}, excess {float(fl['excess']):.1f}); "
      f"state-dependent shares: exact slack {float(L4.verify_state_shares(c, lambda i, j: Tm, A, x0, ks, ss)):.2f}")
assert L4.margin_at(Lm, x0) >= 0 and not fl["ok"]
# explicit three-site binary example: a pair term of the known part that helps is discarded by the clipping
ks = [2, 2, 2]; x0 = (0, 0, 0)
A = [np.array([0.0, 1.0])] * 3
c = np.zeros((3, 3))
Tt3 = {(0, 1): -1.8, (1, 2): -1.8, (0, 2): 10.0}
Tp = lambda i, j: np.array([[0.0, 0.0], [0.0, Tt3[(i, j)]]])
Lm = np.zeros(ks)
for i in range(3):
    sh = [1] * 3; sh[i] = 2
    Lm = Lm + A[i].reshape(sh)
for (i, j) in Tt3:
    sh = [1] * 3; sh[i] = 2; sh[j] = 2
    Lm = Lm + Tp(i, j).reshape(sh)
w = L4.deficits(c, Tp, x0, ks)
fl = L4.share_flow(w, L4.min_excitation(A, x0))
t3, ss3 = L4.state_shares_lp(c, Tp, A, x0, ks)
print(f"    three binary sites: A = 1 each, T_01 = T_12 = -1.8, T_02 = +10, c = 0: min L - L(x0) = {L4.margin_at(Lm, x0):.1f} (criterion holds); "
      f"deficits 1.8, 1.8, 0: shares exist: {fl['ok']} (over-dense {fl['S']}, excess {float(fl['excess']):.1f}); "
      f"state-dependent shares: LP value {t3:.2f} (fails as well: with two states they are the same certificate)")
assert L4.margin_at(Lm, x0) >= 0 and not fl["ok"] and t3 < 0

# =========================================================================================== E
print("E. Proposition 11.18c")


def dprime(mask, x0):
    """{x in D: every reset of x (changed sites K kept, the others reset) lies in D}  -- the largest
    reset-closed part by definition; for pairwise exclusions it should equal the D' of the proposition."""
    out = np.zeros(mask.shape, dtype=bool)
    n = mask.ndim
    for x in states(mask.shape):
        if not mask[x]:
            continue
        S = [i for i in range(n) if x[i] != x0[i]]
        ok = True
        for r in range(len(S) + 1):
            for K in itertools.combinations(S, r):
                y = tuple(x[i] if i in K else x0[i] for i in range(n))
                if not mask[y]:
                    ok = False
        out[x] = ok
    return out


st = dict(domains=0, D_not_reset_closed=0, Dprime_eq_formula=0, pts2=0, pts3=0, worst2=math.inf, worst3=math.inf, tight2=0, tight3=0,
          outside_pts=0, outside_unbounded=0, product_const_larger=0)
for it in range(60):
    n = int(rng.integers(3, 6))
    ks = [int(k) for k in rng.integers(2, 4, size=n)]
    x0 = tuple(int(rng.integers(0, k)) for k in ks)
    forb = set()
    for (i, j) in itertools.combinations(range(n), 2):
        for a in range(ks[i]):
            for b in range(ks[j]):
                if (a, b) != (x0[i], x0[j]) and rng.random() < 0.12:
                    forb.add((i, a, j, b))
    mask = np.ones(ks, dtype=bool)
    for x in states(ks):
        if any((i, x[i], j, x[j]) in forb for (i, j) in itertools.combinations(range(n), 2)):
            mask[x] = False
    assert mask[x0]
    # D' by the formula of the proposition: every changed state compatible with the reference state of every other site
    Df = np.zeros(ks, dtype=bool)
    for x in states(ks):
        if mask[x]:
            Df[x] = all(not ((min(i, j), (x[i] if i < j else x0[j]), max(i, j), (x0[j] if i < j else x[i])) in forb)
                        for i in range(n) if x[i] != x0[i] for j in range(n) if j != i)
    Dp = dprime(mask, x0)
    assert (Dp == Df).all(), "D' of the proposition is not the largest reset-closed part"
    st["Dprime_eq_formula"] += 1
    st["D_not_reset_closed"] += bool((Dp != mask).any())
    g = rng.normal(size=ks)
    # second order on D' with constants over the rectangles inside D'
    c2 = np.zeros((n, n))
    for (i, j) in itertools.combinations(range(n), 2):
        c2[i, j] = c2[j, i] = brute_const(g, (i, j), Dp)
    c2full = L4.c2_matrix(g)
    st["product_const_larger"] += bool((c2full > c2 + 1e-12).any())
    gs = L4.star_part(g, x0); W = L4.pair_penalty(ks, x0, c2)
    c3 = {T: brute_const(g, T, Dp) for T in itertools.combinations(range(n), 3)}
    I2 = L4.interp2(g, x0); W3 = L4.triple_penalty(ks, x0, c3)
    for x in states(ks):
        if Dp[x]:
            s2 = W[x] - abs(g[x] - gs[x]); s3 = W3[x] - abs(g[x] - I2[x])
            assert s2 >= -1e-9 and s3 >= -1e-9, ("remainder bound fails on D'", ks, x0, x)
            st["pts2"] += 1; st["pts3"] += 1
            st["worst2"] = min(st["worst2"], s2); st["worst3"] = min(st["worst3"], s3)
            st["tight2"] += bool(abs(s2) < 1e-9 and W[x] > 1e-9); st["tight3"] += bool(abs(s3) < 1e-9 and W3[x] > 1e-9)
    # values outside D' are unconstrained by the second-order class on D, even given every value on D'
    out = [x for x in states(ks) if mask[x] and not Dp[x]]
    if out and int(mask.sum()) <= 120 and st["outside_pts"] < 40:
        # constants: the exact maxima of g over the rectangles inside D (so that g itself is a member)
        cc = {T: brute_const(g, T, mask) + 1e-9 for T in itertools.combinations(range(n), 2)}
        for x in out[:3]:
            status, val = class_lp_min(g, x0, 2, cc, x, mask=mask, fixed=[y for y in states(ks) if Dp[y]])
            st["outside_pts"] += 1
            st["outside_unbounded"] += bool(status == 3)
    st["domains"] += 1
print("   ", st)
assert st["outside_pts"] == st["outside_unbounded"]
# the counterexample of (c)
mask = np.zeros((2, 2), dtype=bool); mask[0, 0] = mask[0, 1] = mask[1, 1] = True
print("    D = {00, 01, 11}: rectangles inside D:", sum(1 for _ in boxes((2, 2), (0, 1), mask)), "; D' =", [x for x in states((2, 2)) if dprime(mask, (0, 0))[x]])
# completeness of 11.18b(b) on a reset-closed domain that is not a product: two sites, three states, the pair (1,1) excluded
ks = [3, 3]; x0 = (0, 0)
mask = np.ones(ks, dtype=bool); mask[1, 1] = False
assert (dprime(mask, x0) == mask).all()                         # D is reset-closed
A = [np.array([0.0, 1.0, 10.0]), np.array([0.0, 1.0, 10.0])]
c = np.array([[0.0, 3.0], [3.0, 0.0]])
Lm = A[0][:, None] + A[1][None, :] - L4.pair_penalty(ks, x0, c)
Ld = np.where(mask, Lm, np.inf)
fl = L4.share_flow(c, L4.min_excitation(A, x0))
# the lower model on D is attained by a member of the class on D (LP over the class, constants over the rectangles inside D)
g = np.zeros(ks)                                                # star data of the residual: zero (put the excitations into the known part)
errs = []
for x in states(ks):
    if mask[x]:
        status, val = class_lp_min(g, x0, 2, {(0, 1): 3.0}, x, mask=mask)
        errs.append(abs(val - (-3.0 if (x[0] != 0 and x[1] != 0) else 0.0)))
Ld2 = Ld.copy(); Ld2[x0] = np.inf
print(f"    reset-closed non-product domain (3 x 3 minus the pair (1,1)); A = (0,1,10) twice, c_01 = 3: min over x in D, x != x0, of L(x) - L(x0) = {float(Ld2.min() - Ld[x0]):.1f} "
      f"(x0 minimises the exact envelope on D; LP over the class on D reproduces the envelope to {max(errs):.1e}); "
      f"shares exist: {fl['ok']} (over-dense set {fl['S']}, excess {float(fl['excess']):.1f})  ->  'iff' of 11.18b(b) fails on D")
assert Ld.min() >= Ld[x0] and not fl["ok"] and max(errs) < 1e-8

# =========================================================================================== F
print("F. fast class constants against brute force over boxes")
worst = 0.0
for it in range(40):
    n = int(rng.integers(3, 5))
    ks = [int(k) for k in rng.integers(2, 5, size=n)]
    g = rng.normal(size=ks)
    C = L4.c2_matrix(g); c3 = L4.c3_dict(g)
    for (i, j) in itertools.combinations(range(n), 2):
        worst = max(worst, abs(C[i, j] - brute_const(g, (i, j))))
    for T in itertools.combinations(range(n), 3):
        worst = max(worst, abs(c3[T] - brute_const(g, T)))
print(f"    40 random grids: largest difference {worst:.2e}")
assert worst < 1e-12
# =========================================================================================== G
print("G. state-dependent shares  <=>  the reference solves the pairwise (local-polytope) linear relaxation of min L")


def local_polytope_min(ks, A, Tt, c, x0):
    """min over the local polytope of  sum_i A_i(a) mu_i(a) + sum_{i<j} theta_ij(a,b) mu_ij(a,b),
    theta_ij(a,b) = T_ij(a,b) - c_ij if both states are changed, 0 otherwise.  (Value 0 at x0.)"""
    n = len(ks)
    off1 = np.cumsum([0] + ks)
    prs = list(itertools.combinations(range(n), 2))
    off2 = {}
    nv = off1[-1]
    for (i, j) in prs:
        off2[(i, j)] = nv; nv += ks[i] * ks[j]
    cost = np.zeros(nv)
    for i in range(n):
        cost[off1[i]:off1[i] + ks[i]] = A[i]
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for i in range(n):
        for a in range(ks[i]):
            rows.append(r); cols.append(off1[i] + a); vals.append(1.0)
        rhs.append(1.0); r += 1
    for (i, j) in prs:
        th = Tt[(i, j)] - c[i, j]
        th = th.copy(); th[x0[i], :] = 0.0; th[:, x0[j]] = 0.0
        cost[off2[(i, j)]:off2[(i, j)] + ks[i] * ks[j]] = th.ravel()
        for a in range(ks[i]):
            for b in range(ks[j]):
                rows.append(r); cols.append(off2[(i, j)] + a * ks[j] + b); vals.append(1.0)
            rows.append(r); cols.append(off1[i] + a); vals.append(-1.0)
            rhs.append(0.0); r += 1
        for b in range(ks[j]):
            for a in range(ks[i]):
                rows.append(r); cols.append(off2[(i, j)] + a * ks[j] + b); vals.append(1.0)
            rows.append(r); cols.append(off1[j] + b); vals.append(-1.0)
            rhs.append(0.0); r += 1
    res = linprog(cost, A_eq=sp.csr_matrix((vals, (rows, cols)), shape=(r, nv)), b_eq=np.array(rhs), bounds=[(0, None)] * nv, method="highs")
    return float(res.fun)


st = dict(inst=0, exact=0, lp_tight=0, state_shares=0, const_shares=0, disagree=0)
for it in range(300):
    n = int(rng.integers(2, 6))
    ks = [int(k) for k in rng.integers(2, 5, size=n)]
    x0 = tuple(0 for _ in ks)
    A = [np.r_[0.0, rng.random(k - 1) * 2.0 + 0.05] for k in ks]
    c = rng.random((n, n)) * rng.choice([0.2, 0.6, 1.2]); c = np.triu(c, 1); c = c + c.T
    Tt = {}
    for (i, j) in itertools.combinations(range(n), 2):
        t = rng.normal(size=(ks[i], ks[j])) * rng.choice([0.0, 0.3, 1.0])
        t[0, :] = 0; t[:, 0] = 0
        Tt[(i, j)] = t
    Tpair = lambda i, j: Tt[(i, j)]
    Lm = np.zeros(ks)
    for i in range(n):
        sh = [1] * n; sh[i] = ks[i]
        Lm = Lm + A[i].reshape(sh)
    for (i, j), t in Tt.items():
        sh = [1] * n; sh[i] = ks[i]; sh[j] = ks[j]
        Lm = Lm + t.reshape(sh)
    Lm = Lm - L4.pair_penalty(ks, x0, c)
    exact = bool(Lm.min() >= Lm[x0] - 1e-12)
    lpv = local_polytope_min(ks, A, Tt, c, x0)
    tss, ss = L4.state_shares_lp(c, Tpair, A, x0, ks)
    fl = L4.share_flow(L4.deficits(c, Tpair, x0, ks), L4.min_excitation(A, x0))
    lp_tight = lpv >= -1e-7
    ss_ok = tss >= -1e-7
    st["inst"] += 1; st["exact"] += exact; st["lp_tight"] += lp_tight; st["state_shares"] += ss_ok; st["const_shares"] += fl["ok"]
    if abs(abs(lpv) - 0.0) > 1e-6 and abs(tss) < 1e-6:
        pass
    st["disagree"] += (lp_tight != ss_ok) and min(abs(lpv), abs(tss)) > 1e-6
    assert (not ss_ok) or exact
    assert (not fl["ok"]) or ss_ok
print("   ", st)
assert st["disagree"] == 0
print(f"[{time.time() - t00:.0f}s] DONE p4_03_review")
