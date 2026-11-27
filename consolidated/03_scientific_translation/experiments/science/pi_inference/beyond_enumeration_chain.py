#!/usr/bin/env python3
"""Addendum A17 (10): a solvated side-chain free energy at a size beyond enumeration -- coordinator's script.

System: Ace-X_n-NMe on a fixed ideal backbone, one rotamer variable per residue (workstream P2's model, imported
read-only: experiments/science/ws_P2/fbmodel.py; ff14SB vacuum energy f, exactly pairwise in the residues, plus the
GBn2 polarisation energy gb, evaluated exactly as OpenMM does).  True energy g = f + gb, 300 K.

Tractable model (a chain with couplings up to W residues apart; built WITHOUT any enumeration):
    m(x) = c0 + gb(x0) + sum_i [h_i + a_i](x_i) + sum_{0<j-i<=W} [J_ij + a_ij](x_i, x_j)
  h_i, J_ij: exact tables of f;  a_i, a_ij: the anchored expansion of gb at a reference assignment x0
  (a_i(s) = gb(x0; x_i=s) - gb(x0);  a_ij(s,t) = gb(x0; x_i=s, x_j=t) - gb(x0) - a_i(s) - a_j(t)),
  which costs 1 + sum_i k_i + sum_{pairs in the window} k_i k_j evaluations of gb.
ln Z(m) and exact samples of pi_m by a transfer matrix over blocks of W consecutive sites.
Remainder r = beta (g - m): evaluated at N samples of pi_m.  Reported:
    first-order estimate   ln Z(g) ~ ln Z(m) - mean(r)                 (exact identity: ln Z(g) = ln Z(m) - E r + K, K >= 0)
    the sample statistics of r (mean, standard deviation, smallest value), the exponential-average estimate of K,
    and the Bennett bracket W(b, s2) evaluated at the SAMPLED floor and variance -- which is what a certificate would
    give if a floor and a variance of that size were PROVED.  Nothing here is a certificate.
Validation: at a size where everything can be enumerated the same pipeline is compared with the exact values.

usage: python3 beyond_enumeration_chain.py SEQLETTER BACKBONE W n_small n_large [n_large2 ...]
"""
import os, sys, math, json, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
from fbmodel import FBModel
KT = 0.0019872041 * 300.0; BETA = 1.0 / KT
TAU = 0.60

def W_sharp(b, s2):
    if b < 1e-12 or s2 < 1e-300: return 0.0
    if b > 700.0: return b + math.log(s2 / (b * b + s2))
    return math.log1p((b * b * math.expm1(-s2 / b) + s2 * math.expm1(b)) / (b * b + s2))

class Chain:
    """m(x) = const + sum_i u[i][x_i] + sum_{0<j-i<=W} v[(i,j)][x_i,x_j]  (energies in k_BT) on local alphabets of size k[i]."""
    def __init__(self, const, u, v, W):
        self.const, self.u, self.v, self.W = const, u, v, W
        self.n = len(u); self.k = [len(a) for a in u]
    def energy(self, x):                      # x: (M, n) local indices
        e = np.full(x.shape[0], self.const)
        for i in range(self.n): e += self.u[i][x[:, i]]
        for (i, j), t in self.v.items(): e += t[x[:, i], x[:, j]]
        return e
    def _blocks(self):
        # composite state at position i: (x_i, ..., x_{i+W-1});  i = 0 .. n-W
        n, W, k = self.n, self.W, self.k
        self.shapes = [tuple(k[i:i + W]) for i in range(n - W + 1)]
        # weight carried by block 0: all one-body terms and pairs inside it
        lw0 = np.zeros(self.shapes[0])
        idx = np.indices(self.shapes[0])
        for a in range(W):
            lw0 -= self.u[a][idx[a]]
            for b in range(a + 1, W):
                if (a, b) in self.v: lw0 -= self.v[(a, b)][idx[a], idx[b]]
        self.lw0 = lw0
        # transition i -> i+1 adds site j = i+W: its one-body term and its pairs with sites i+1 .. i+W-1 and with site i
        self.ltr = []
        for i in range(n - W):
            j = i + W
            sh = tuple(k[i:i + W + 1])                      # (x_i, ..., x_{i+W})
            ix = np.indices(sh)
            lt = -self.u[j][ix[W]]
            for a in range(W):
                if (i + a, j) in self.v: lt = lt - self.v[(i + a, j)][ix[a], ix[W]]
            self.ltr.append(lt)
    def solve(self):
        self._blocks()
        la = [self.lw0]                                      # log forward messages over blocks
        for lt in self.ltr:
            t = la[-1][..., None] + lt                       # axes (x_i, ..., x_{i+W})
            mx = t.max(axis=0)
            la.append(mx + np.log(np.exp(t - mx).sum(axis=0)))
        self.la = la
        mx = la[-1].max()
        self.lnZ = float(mx + np.log(np.exp(la[-1] - mx).sum())) - self.const
        return self.lnZ
    def sample(self, N, rng):
        n, W = self.n, self.W
        x = np.zeros((N, n), dtype=int)
        last = self.la[-1]; p = np.exp(last - last.max()).ravel(); p /= p.sum()
        flat = rng.choice(p.size, size=N, p=p)
        tail = np.array(np.unravel_index(flat, last.shape)).T          # (N, W): sites n-W .. n-1
        x[:, n - W:] = tail
        for i in range(n - W - 1, -1, -1):                              # sample x_i given x_{i+1..i+W}
            # log weight over x_i: la[i][x_i, x_{i+1..i+W-1}] + ltr[i][x_i, ..., x_{i+W}]
            if W == 1:
                sub_la = self.la[i][:, None]                                                        # (k_i, 1): no conditioning sites inside the block
            else:
                sub_la = self.la[i][(slice(None),) + tuple(x[:, i + 1 + a] for a in range(W - 1))]  # (k_i, N)
            sub_lt = self.ltr[i][(slice(None),) + tuple(x[:, i + 1 + a] for a in range(W))]         # (k_i, N)
            lw = (sub_la + sub_lt).T                                    # (N, k_i)
            pw = np.exp(lw - lw.max(axis=1, keepdims=True)); pw /= pw.sum(axis=1, keepdims=True)
            cum = pw.cumsum(axis=1); uu = rng.random(N)[:, None]
            x[:, i] = (uu > cum).sum(axis=1).clip(0, pw.shape[1] - 1)
        return x

def build(seq, bb, W, log):
    t0 = time.time()
    M = FBModel(seq, bb, grid="R3", extra_ffs=())
    dom = [np.flatnonzero(s > TAU) for s in M.s1]            # allowed states per site (one-site clash score)
    n = M.ns
    c0, h, J = M.site_tables()
    # reference assignment: per site the allowed state of lowest one-body vacuum energy
    x0 = np.array([dom[i][int(np.argmin(h[i][dom[i]]))] for i in range(n)])
    ev = 0
    def gb(st):
        nonlocal ev
        st = np.atleast_2d(st); ev += st.shape[0]
        return M.gb_energy(st)
    gb0 = float(gb(x0)[0])
    a1 = []
    for i in range(n):
        st = np.repeat(x0[None], len(dom[i]), 0); st[:, i] = dom[i]
        a1.append(gb(st) - gb0)
    v = {}
    for i in range(n):
        for j in range(i + 1, min(n, i + W + 1)):
            ki, kj = len(dom[i]), len(dom[j])
            st = np.repeat(x0[None], ki * kj, 0)
            gi, gj = np.meshgrid(np.arange(ki), np.arange(kj), indexing="ij")
            st[:, i] = dom[i][gi.ravel()]; st[:, j] = dom[j][gj.ravel()]
            a2 = (gb(st) - gb0).reshape(ki, kj) - a1[i][:, None] - a1[j][None, :]
            v[(i, j)] = BETA * (J[(i, j)][np.ix_(dom[i], dom[j])] + a2)
    u = [BETA * (h[i][dom[i]] + a1[i]) for i in range(n)]
    const = BETA * (c0 + gb0)
    ch = Chain(const, u, v, W)
    log(f"   built {seq[:1]}{n} on {bb}: {M.P.natoms} atoms, states per site {sorted(set(len(d) for d in dom))}, "
        f"window W={W}; {ev} GB evaluations for the model tables; {time.time() - t0:.0f} s")
    def g_of(xloc):                                           # true energy in k_BT at local-index assignments
        st = np.stack([dom[i][xloc[:, i]] for i in range(n)], axis=1)
        return BETA * (M.table_energy(st) + M.gb_energy(st))
    return ch, g_of, dom

def report(tag, ch, g_of, N, rng, log, exact=None):
    lnZm = ch.solve()
    x = ch.sample(N, rng)
    r = g_of(x) - ch.energy(x)
    mean, sd, lo = float(r.mean()), float(r.std(ddof=1)), float(r.min())
    Kexp = float(np.log(np.mean(np.exp(-(r - mean)))))
    b = mean - lo
    res = dict(tag=tag, n=ch.n, W=ch.W, N=N, lnZ_model=lnZm, r_mean=mean, r_sd=sd, r_min=lo, r_max=float(r.max()),
               first_order=lnZm - mean, se_mean=sd / math.sqrt(N), K_exp=Kexp, b_sampled=b, W_bennett_sampled=W_sharp(b, sd * sd))
    log(f"   {tag}: ln Z(m) = {lnZm:.4f};  remainder over {N} samples of pi_m: mean {mean:+.5f}, sd {sd:.5f}, min {lo:+.4f}, max {r.max():+.4f} (k_BT)")
    log(f"      first-order estimate ln Z(g) ~ ln Z(m) - mean r = {lnZm - mean:.4f} +- {sd / math.sqrt(N):.5f} (standard error);  "
        f"exponential-average estimate of K = {Kexp:.2e};  Bennett W at the sampled floor b = {b:.3f} and variance: {res['W_bennett_sampled']:.2e}")
    if exact is not None:
        res.update(exact)
        log(f"      EXACT (enumeration): ln Z(g) = {exact['lnZ_true']:.4f};  E r = {exact['Er']:+.5f}, sd {exact['sd']:.5f}, floor b = {exact['b']:.3f}, "
            f"K = {exact['K']:.2e}, Bennett W = {exact['W']:.2e};  first-order error = K;  sampled first-order - exact = {lnZm - mean - exact['lnZ_true']:+.5f}")
    return res

def exact_values(ch, g_of):
    k = ch.k
    grids = np.meshgrid(*[np.arange(a) for a in k], indexing="ij")
    X = np.stack([gx.reshape(-1) for gx in grids], axis=1)
    g = np.concatenate([g_of(X[s:s + 20000]) for s in range(0, len(X), 20000)])
    m = ch.energy(X)
    lnZg = float(-g.min() + np.log(np.exp(-(g - g.min())).sum()))
    pm = np.exp(-(m - m.min())); pm /= pm.sum()
    r = g - m; Er = float(pm @ r); rc = r - Er
    s2 = float(pm @ rc**2); b = float(-rc.min()); K = float(np.log1p(pm @ np.expm1(-rc)))
    lnZm_enum = float(-m.min() + np.log(np.exp(-(m - m.min())).sum())) - 0.0
    return dict(lnZ_true=lnZg, lnZ_model_enum=lnZm_enum, Er=Er, sd=math.sqrt(s2), b=b, K=K, W=W_sharp(b, s2), states=len(X))

if __name__ == "__main__":
    aa, bb, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
    n_small = int(sys.argv[4]); larges = [int(v) for v in sys.argv[5:]]
    out = []; lines = []
    def log(s): print(s, flush=True); lines.append(s)
    rng = np.random.default_rng(20261126)
    log(f"# {aa} homopeptide on backbone {bb}, chain model with window W = {W}; energies in k_BT at 300 K")
    ch, g_of, dom = build(aa * n_small, bb, W, log)
    ex = exact_values(ch, g_of)
    lnZm = ch.solve()
    log(f"   check of the transfer matrix at n = {n_small}: ln Z(m) = {lnZm:.6f} against enumeration {ex['lnZ_model_enum']:.6f} ({ex['states']} states)")
    assert abs(lnZm - ex['lnZ_model_enum']) < 1e-8 * max(1.0, abs(lnZm)), "transfer matrix disagrees with enumeration"
    out.append(report(f"{aa}{n_small}_{bb} (validation)", ch, g_of, 4000, rng, log, exact=ex))
    for nl in larges:
        ch, g_of, dom = build(aa * nl, bb, W, log)
        out.append(report(f"{aa}{nl}_{bb}", ch, g_of, 4000, rng, log))
        log(f"      (number of rotamer assignments: about 10^{sum(math.log10(len(d)) for d in dom):.1f})")
    json.dump(out, open(os.path.join(HERE, f"beyond_enumeration_chain_{aa}_{bb}_W{W}.json"), "w"), indent=1)
