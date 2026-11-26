"""
P4 item 4: does the pair form at order m tighten workstream P3's certified sandwich?
P3 (P3_REPORT section 2.4-2.5): lower model  m_- = f + I_{m-1} g - sum_i gamma_i [x_i changed],
gamma_i = (1/m) sum_{T contains i, |T| = m} chat_T  with constants chat_T certified by analysis.
Pair form at order m (this script):  gamma_ij = (1 / C(m,2)) sum_{T contains i, j} chat_T ,
model  f + I_{m-1} g - sum_{i<j changed} gamma_ij ;  and the banded variant for band width w:
pairs with j - i <= w keep their pair penalty, the share of every other pair of T goes in halves
to its two sites (the model then has pair terms of separation at most w, as P3's banded models).

What is whose: the certified constants chat_T come from P3's code, RE-RUN here unchanged
(p3core.GBModel, encl.EnvelopeSup, gfbound.GFBound.total(m, T) in its "anchored" mode at my
anchor); the grids of f and g_GB are P2's enumeration; interpolants, penalties, soundness check
and partition sums are mine.  Only the penalty is compared: P3's band reductions of the pair
terms of f + I g are not applied (they are the same for all penalty forms).

usage: python3 -B p4_06_p3pair.py SEQ BB TAU M [W]     e.g.  V6 E 0.70 3 2
"""
import sys, os, time, math, itertools, json
import numpy as np
import p4lib as L4
P3 = os.path.normpath(os.path.join(L4.HERE, "..", "ws_P3"))
sys.path.insert(1, P3)
import glob, shutil
import encl
# P3's enclosure code caches tables in ws_P3/cache; that directory is read-only for me, so the
# cache is redirected to my own directory (pre-filled with copies of P3's cached tables).
MYCACHE = os.path.join(L4.HERE, "cache_p3")
os.makedirs(MYCACHE, exist_ok=True)
for fn in glob.glob(os.path.join(P3, "cache", "atom_*.npz")) + glob.glob(os.path.join(P3, "cache", "zeta_*.npz")):
    dst = os.path.join(MYCACHE, os.path.basename(fn))
    if not os.path.exists(dst):
        shutil.copy(fn, dst)
encl.CACHE = MYCACHE
from p3core import GBModel
from encl import EnvelopeSup
from gfbound import GFBound

seq, bb, tau, m = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
w = int(sys.argv[5]) if len(sys.argv) > 5 else 2
t0 = time.time()
tag = f"fb_{seq.replace(':', 'c')}_{bb}_R3_t0.60"
inst = L4.load_instance(tag, tau)
shape = inst["shape"]; n = len(shape)
f = inst["f"]; g = inst["R"]["GB"]; E = f + g
x0 = L4.argmin_index(E)
G = GBModel(seq, bb, tau=tau)
assert list(G.k) == list(shape), (G.k, shape)
# the same domain and state order: P3's table energy against P2's enumerated g_GB at 50 random states and at x0
rng = np.random.default_rng(1)
st = np.stack([rng.integers(0, k, 50) for k in shape], axis=1); st[0] = x0
eg = G.energy(st)
dg = float(np.abs(eg - g[tuple(st.T)]).max())
print(f"{seq}/{bb} tau {tau}: X' {list(shape)}; anchor x0 = argmin E = {x0}; |g_GB(P3 tables) - g_GB(P2 grid)| at 50 states: {dg:.1e} kcal/mol", flush=True)
assert dg < 1e-6
sup = EnvelopeSup(G)
GF = GFBound(G, np.array(x0), sup, K=m)
chat = {}
for T in itertools.combinations(range(n), m):
    s_, c_ = GF.total(m, T=list(T))
    chat[T] = float(s_ + c_)
tot = sum(GF.total(m))
print(f"   certified constants chat_T, |T| = {m}: {len(chat)} subsets, sum {sum(chat.values()):.6f} (P3's Gamma_{m} = {tot:.6f}), max {max(chat.values()):.6f} kcal/mol  [{time.time() - t0:.0f}s]", flush=True)


def anchored_term(h, x0, U):
    """mixed difference of h at x0 over the sites U as a table over the states of U (broadcastable)."""
    nn = h.ndim
    idx = list(x0)
    for u in U:
        idx[u] = slice(None)
    D = h[tuple(idx)]                                           # axes in increasing site order
    for pos, u in enumerate(sorted(U)):
        ref = np.take(D, [x0[u]], axis=pos)
        D = D - ref
    sh = [1] * nn
    for u in U:
        sh[u] = h.shape[u]
    return D.reshape(sh)


I = np.full(shape, g[x0])
for r in range(1, m):
    for U in itertools.combinations(range(n), r):
        I = I + anchored_term(g, x0, U)
rem = g - I
ch = L4.changed(shape, x0)
# exact measured anchored constants of the remainder at order m (for comparison: chat_T must dominate them)
pen_env = np.zeros(shape)
for T, v in chat.items():
    t = v
    for s in T:
        t = t * ch[s]
    pen_env = pen_env + t
assert (np.abs(rem) <= pen_env + 1e-9).all(), "P3's certified remainder bound violated on the grid"
c2m = math.comb(m, 2)
gam = np.zeros(n); gam2 = np.zeros((n, n)); gam_b = np.zeros(n); gam2_b = np.zeros((n, n))
for T, v in chat.items():
    for s in T:
        gam[s] += v / m
    for (i, j) in itertools.combinations(T, 2):
        gam2[i, j] += v / c2m; gam2[j, i] += v / c2m
        if j - i <= w:
            gam2_b[i, j] += v / c2m; gam2_b[j, i] += v / c2m
        else:
            gam_b[i] += v / (2 * c2m); gam_b[j] += v / (2 * c2m)
base = f + I
lnZE = L4.lnZ(E)
models = {"envelope (m-body)": base - pen_env, "site form (P3)": base - L4.site_penalty(shape, x0, gam),
          "pair form": base - L4.pair_penalty(shape, x0, gam2),
          f"banded pair form (w = {w})": base - L4.site_penalty(shape, x0, gam_b) - L4.pair_penalty(shape, x0, gam2_b)}
res = {}
print(f"   max |g - I_{m-1} g| = {float(np.abs(rem).max()):.5f}; max gamma_i = {gam.max():.5f}, max gamma_ij = {gam2.max():.5f} kcal/mol")
for nm, mod in models.items():
    gap = E - mod
    d = L4.lnZ(mod) - lnZE
    res[nm] = dict(sound=float(gap.min()), dlnZ=d, cost=float(math.expm1(d)), maxgap=float(gap.max()), margin=L4.margin_at(mod, x0))
    print(f"   {nm:28s}: min(E - m) = {gap.min():.2e}; ln Z(m) - ln Z(E) = {d:.6f} nats (cost number {math.expm1(d):.6f}); max(E - m) = {gap.max():.4f}; margin at x0 = {res[nm]['margin']:.4f}")
ps, pp, pb = L4.site_penalty(shape, x0, gam), L4.pair_penalty(shape, x0, gam2), L4.site_penalty(shape, x0, gam_b) + L4.pair_penalty(shape, x0, gam2_b)
print(f"   pointwise: envelope <= pair <= banded pair <= site penalties at every state: {bool((pen_env <= pp + 1e-12).all() and (pp <= pb + 1e-12).all() and (pb <= ps + 1e-12).all())}")
os.makedirs(os.path.join(L4.HERE, "out"), exist_ok=True)
json.dump(dict(seq=seq, bb=bb, tau=tau, m=m, w=w, shape=list(shape), x0=list(x0), chat={",".join(map(str, T)): v for T, v in chat.items()}, Gamma=float(tot), models=res),
          open(os.path.join(L4.HERE, "out", f"p4_06_{seq.replace(':', 'c')}_{bb}_{tau:.2f}_m{m}.json"), "w"), indent=0)
print(f"[{time.time() - t0:.0f}s] DONE p4_06_p3pair {seq} {bb} {tau} {m}")
