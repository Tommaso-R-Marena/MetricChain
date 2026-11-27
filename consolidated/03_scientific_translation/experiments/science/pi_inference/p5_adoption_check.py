#!/usr/bin/env python3
"""Coordinator's checks before adopting workstream P5 (the compact case), 2026-11-26.

1. THE SIGN-REVERSAL NUMBERS OF P5'S THEOREM 8, WITH OWN CODE.  Ace-Leu6-NMe on the helix (64 assignments).  The kernel
   matrix M(x) (inverse Still function, diagonal 1/B) is computed here from workstream P3's TABLE-FREE reference path
   (descreening integrals summed over all ordered atom pairs -- the path of p3core.GBModel.energy_direct, not the tables
   P5 used); g_c(x) = -(kappa/2) c^T M(x) c for any charge vector c; the anchored interpolation I_{m-1} g is my own
   inclusion-exclusion.  Compared with P5's stored values: the true remainder sup |g - I_{m-1} g| for m = 3, 4, 5, and the
   same with all charges made positive.  Then my own search over random sign patterns (P5's pattern is not stored): any
   pattern found is a lower bound for every bound that uses the charges only through their magnitudes.
2. P5'S CERTIFICATE FOR Leu12 ON THE HELIX (order 6, site penalties) REBUILT THROUGH A DIFFERENT DRIVER: workstream P6's
   make_models (which calls P3's pwmodel.build_band_models with P6's own pair sums and site allocation code path 'S'),
   against the numbers stored by P5's run of P3's pipeline; the sandwich at all 4 096 states; exact ln Z by enumeration.
Run:  python3 -B p5_adoption_check.py > p5_adoption_check.log     (one core, about a minute)
"""
import os, sys, math, json, time, itertools
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "ws_P6")))
import p6lib as L                                  # also puts ws_P3 on the path
from p3core import GBModel, KAPPA, KCAL
pw = L.pw; BETA = L.BETA
P5OUT = os.path.normpath(os.path.join(HERE, "..", "ws_P5", "out"))


def log(s): print(s, flush=True)


def kernel(G, st):
    """M[x, p, q] by the table-free path of GBModel.energy_direct (my transcription of its formulas)."""
    out = np.empty((len(st), G.nat, G.nat)); allat = np.arange(G.nat); eye = np.eye(G.nat)
    for m in range(len(st)):
        X = G.coords(st[m:m + 1])[0]
        r = G._dist(X, X) + eye
        I = (G._H(r, allat, allat) * (1.0 - eye)).sum(-1)
        B = 1.0 / G.invB(I[None])[0]
        r2 = (r - eye) ** 2; BB = B[:, None] * B[None, :]
        out[m] = 1.0 / np.sqrt(r2 + BB * np.exp(-r2 / (4.0 * BB)))
    return out


def remainder_sup(gt, x0, order):
    """sup_x |g - I_{order-1} g|(x) for g given as an array over the product grid; anchored at x0 (own inclusion-exclusion)."""
    shape = gt.shape; n = len(shape); worst = 0.0
    for x in itertools.product(*[range(k) for k in shape]):
        S = [i for i in range(n) if x[i] != x0[i]]
        if len(S) < order: continue                       # the interpolation is exact when fewer than `order` sites differ
        val = 0.0
        for r in range(order):
            for U in itertools.combinations(S, r):
                # d_U(x_U) = sum over V subset of U of (-1)^{|U|-|V|} g(x0 with x on V)
                for rv in range(r + 1):
                    for V in itertools.combinations(U, rv):
                        y = list(x0)
                        for i in V: y[i] = x[i]
                        val += (-1) ** (r - rv) * gt[tuple(y)]
        worst = max(worst, abs(gt[x] - val))
    return worst


t0 = time.time()
log("=== 1. Leu6 on the helix: the remainder of the anchored expansion for the true charges and for reversed signs")
G = GBModel("L6", "H", tau=0.60); st = G.product_states(); shape = tuple(G.k); n = G.ns
sd = L.setup("L6", "H", 0.60); c0, h, J = sd[1], sd[2], sd[3]
M = kernel(G, st)
gq = lambda c: ((-0.5 * KAPPA / KCAL) * np.einsum("p,xpq,q->x", c, M, c)).reshape(shape)
g_true = gq(G.q)
dev = float(np.abs(g_true.ravel() - G.energy(st)).max())
E = (pw.f_energy(st, c0, h, J) + g_true.ravel()).reshape(shape)
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(E), shape))
ref = json.load(open(os.path.join(P5OUT, "s2_L6_H_0.60.json")))["orders"]
log(f"  {len(st)} states, {G.nat} atoms; my kernel sum against P3's table evaluator: largest difference {dev:.1e} kcal/mol; anchor (argmin E) {x0}")
rng = np.random.default_rng(20261126); pats = [np.ones(G.nat)] + [rng.choice([-1.0, 1.0], G.nat) for _ in range(400)]
out = {}
for m in (3, 4, 5):
    r_true = remainder_sup(g_true, x0, m); r_plus = remainder_sup(gq(np.abs(G.q)), x0, m)
    best = max(remainder_sup(gq(s * G.q), x0, m) for s in pats[1:])
    R = ref[str(m)]
    log(f"  m = {m}: true remainder sup = {r_true:.6f} (P5: {R['rem_true']:.6f});  all charges positive: {r_plus:.6f} (P5: {R['rem_allplus']:.6f});  "
        f"best of 400 random sign patterns here: {best:.4f} (P5's local search: {R['rem_LS']:.4f});  P3's Gamma_m = {R['Gamma']:.3f};  "
        f"so every sign-blind bound / truth >= {max(r_plus, best) / r_true:.1f} by my patterns ({R['rem_LS'] / R['rem_true']:.1f} by P5's)")
    assert abs(r_true - R["rem_true"]) < 1e-9 and abs(r_plus - R["rem_allplus"]) < 1e-9
    assert max(r_plus, best) <= R["Gamma"]
    out[m] = dict(rem_true=r_true, rem_allplus=r_plus, best_random=best, p5_rem_LS=R["rem_LS"], Gamma=R["Gamma"])

log("--- 1b. my own local search (1-flip ascent on the quadratic form of the remainder at one state, then exact evaluation at all states)")


def remainder_matrix(x, order):
    """A with  (g_c - I_{order-1} g_c)(x) = -(kappa/2) c^T A c : the same inclusion-exclusion applied to the kernel matrices."""
    idx = lambda y: int(np.ravel_multi_index(tuple(y), shape))
    S = [i for i in range(n) if x[i] != x0[i]]
    A = M[idx(x)].copy()
    for r in range(order):
        for U in itertools.combinations(S, r):
            for rv in range(r + 1):
                for V in itertools.combinations(U, rv):
                    y = list(x0)
                    for i in V: y[i] = x[i]
                    A -= (-1) ** (r - rv) * M[idx(y)]
    return A


def ascent(Bm, s):
    """1-flip local ascent of s^T Bm s over sign vectors (Bm symmetric)."""
    s = s.copy(); Bs = Bm @ s; d = np.diag(Bm)
    while True:
        gain = -4.0 * s * Bs + 4.0 * d                     # change of s^T Bm s when s_p is flipped
        p = int(np.argmax(gain))
        if gain[p] <= 1e-15: return s
        s[p] = -s[p]; Bs += 2.0 * s[p] * Bm[:, p]


aq = np.abs(G.q)
for m in (3, 4, 5):
    cands = []
    for x in itertools.product(*[range(k) for k in shape]):
        if sum(1 for i in range(n) if x[i] != x0[i]) < m: continue
        Bm = (-0.5 * KAPPA / KCAL) * aq[:, None] * remainder_matrix(x, m) * aq[None, :]
        for sign in (1.0, -1.0):
            for t in range(6):
                s = ascent(sign * Bm, np.ones(G.nat) if t == 0 else rng.choice([-1.0, 1.0], G.nat))
                cands.append((abs(float(s @ Bm @ s)), tuple(s)))
    cands.sort(reverse=True)
    best = 0.0
    for val, s in cands[:12]:                                # exact evaluation of the best candidates at all states
        best = max(best, remainder_sup(gq(np.array(s) * aq), x0, m))
    R = ref[str(m)]
    log(f"  m = {m}: pattern found by my search: remainder sup = {best:.4f} kcal/mol (P5's search: {R['rem_LS']:.4f});  truth {out[m]['rem_true']:.6f};  "
        f"every sign-blind bound of the remainder / truth >= {best / out[m]['rem_true']:.1f} (P5: {R['rem_LS'] / R['rem_true']:.1f});  P3's Gamma_m / pattern = {R['Gamma'] / best:.1f}")
    assert best <= R["Gamma"]
    out[m]["own_search"] = best

log("=== 2. Leu12 on the helix, order 6, site penalties: P5's run of P3's pipeline against a rebuild through P6's driver")
ref = json.load(open(os.path.join(P5OUT, "floor_L12_H_t0.60_gbn2_m6_siteres.json")))
sd = L.setup("L12", "H", 0.60); G12, c0, h, J, x012, E0 = sd
lo, up, info = L.make_models("L12", "H", 0.60, 6, 11, "S", setup_data=sd)
st, g, src = L.enumerate_g(G12, "L12", "H", 0.60, verbose=False)
E = pw.f_energy(st, c0, h, J) + g
ml, mu = lo.energy(st), up.energy(st)
lnZE = float(logsumexp(-BETA * E))
log(f"  anchor here {tuple(int(v) for v in x012)}, P5's {tuple(ref['anchor'])};  ln Z(m_-) = {lo.lnZ():.10f} (P5: {ref['lnZ_lower_model']:.10f});  "
    f"ln Z(m_+) = {up.lnZ():.10f} (P5: {ref['lnZ_upper_model']:.10f});  exact ln Z(E) = {lnZE:.9f} (P5: {ref['lnZ_E']:.9f})")
log(f"  sandwich at all {len(st)} states: m_- > E at {int((ml > E).sum())}, m_+ < E at {int((mu < E).sum())};  largest E - m_- = {float((E - ml).max()):.4f} "
    f"(P5: {ref['rho_exact']:.4f}), largest m_+ - E = {float((mu - E).max()):.4f} (P5: {ref['rho_up_exact']:.4f}) kcal/mol;  "
    f"cost number Z(m_-)/Z(E) - 1 = {math.expm1(lo.lnZ() - lnZE):.6f} (P5: {ref['cost']:.6f})")
assert int((ml > E).sum()) == 0 and int((mu < E).sum()) == 0
out["L12"] = dict(lnZ_lo=up.lnZ(), lnZ_hi=lo.lnZ(), lnZE=lnZE, p5_lo=ref["lnZ_upper_model"], p5_hi=ref["lnZ_lower_model"])
json.dump(out, open(os.path.join(HERE, "p5_adoption_check.json"), "w"), indent=1)
log(f"ALL DONE {time.time() - t0:.0f} s")
