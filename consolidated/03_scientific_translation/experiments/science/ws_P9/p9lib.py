"""
Workstream P9 -- shared library: penalties RESOLVED BY ROTAMER STATE.

What is whose
-------------
* Workstream P8's code path for the block bounds is used unchanged: `ResBound` subclasses p8sr.AHBound and only
  RECORDS the arrays `v` (one host) / `W` (two hosts) of block bounds per host state that
  BlockBound.total_T_blocks hands to `_c1` / `_c2`; the maximisation in `_c1` / `_c2` still runs (its results are P8's
  constants 'Sb' / 'SAb' and are compared with P8's stored files by the drivers).
* P3's ingredients (GFBound per-state data, enclosures, PAD_TAB, RND), P6's allowances (p6lib.fp_tables), the
  coordinator's window models (pi_inference/window_model.py, window_model_occ.py) are imported READ-ONLY.
* Mine: theta_parts / theta_table (the bound of a subset as a function of the states of its sites), the tables
  (site, pair, triple) and their chains, the drivers.

Nothing is written outside ws_P9:
  * sys.dont_write_bytecode before any foreign import (run with python3 -B as well);
  * the foreign libraries copy enclosure tables into THEIR cache directories at import time when a table is missing
    there (p6lib, p8lib) -- during their import shutil.copy / os.makedirs are replaced by guards that refuse any
    target inside experiments/science but outside ws_P9 and record the attempt in FOREIGN_WRITES (expected: empty);
  * afterwards encl.CACHE, p6lib.MYCACHE and p8lib.MYCACHE point to ws_P9/cache, which is pre-filled with my own
    copies of the tables.
  * pi_inference/nested_sampler.py is NOT imported (it creates and fills pi_inference/serine_helix_reach_cache).

Units: kcal/mol; beta = 1/kT at 300 K (p3core.BETA).
"""
import sys, os, time, glob, shutil, itertools, math, json, gc, resource, importlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
MYCACHE = os.path.join(HERE, "cache"); OUT = os.path.join(HERE, "out"); LOGS = os.path.join(HERE, "logs")
for _d in (MYCACHE, OUT, LOGS):
    os.makedirs(_d, exist_ok=True)
import numpy as np

# ---- (1) my own copies of the enclosure tables (the sources are only read)
for _src in ("ws_P8", "ws_P3"):
    for _fn in sorted(glob.glob(os.path.join(SCI, _src, "cache", "atom_*.npz")) + glob.glob(os.path.join(SCI, _src, "cache", "zeta_*.npz"))):
        _dst = os.path.join(MYCACHE, os.path.basename(_fn))
        if not os.path.exists(_dst):
            shutil.copy(_fn, _dst)

# ---- (2) guarded import of the foreign modules
FOREIGN_WRITES = []
_real_copy, _real_makedirs = shutil.copy, os.makedirs


def _foreign(p):
    p = os.path.abspath(str(p))
    return p.startswith(SCI + os.sep) and not (p == HERE or p.startswith(HERE + os.sep))


def _guard_copy(src, dst, *a, **k):
    if _foreign(dst):
        FOREIGN_WRITES.append(("copy", str(src), str(dst)))
        return dst
    return _real_copy(src, dst, *a, **k)


def _guard_makedirs(p, *a, **k):
    if _foreign(p) and not os.path.isdir(p):
        FOREIGN_WRITES.append(("makedirs", str(p)))
        return None
    return _real_makedirs(p, *a, **k)


shutil.copy = _guard_copy; os.makedirs = _guard_makedirs
try:
    for _d in ("ws_P6", "ws_P5", "ws_P3", "ws_P8"):
        _p = os.path.join(SCI, _d)
        if _p not in sys.path:
            sys.path.insert(0, _p)
    sys.path.append(os.path.join(SCI, "pi_inference"))
    import p8lib as P8L                                   # P8 (read-only); imports p5lib, encl, p3core, gfbound, termwise
    import p8sr                                           # P8 (read-only)
    import p6lib as L                                     # P6 (read-only)
    T9 = importlib.import_module("p6_09_triple")          # P6 (read-only)
    import window_model, window_model_occ                 # coordinator (read-only)
finally:
    shutil.copy = _real_copy; os.makedirs = _real_makedirs
import encl
encl.CACHE = MYCACHE; L.MYCACHE = MYCACHE; P8L.MYCACHE = MYCACHE
from p3core import GBModel, KAPPA, KCAL, KT300, BETA
from encl import EnvelopeSup
from gfbound import RND, PAD_TAB
pw = L.pw
EPS_G = L.EPS_G
WindowModel, build_window_models, diff_window = window_model.make(pw)
build_window_models_occ = window_model_occ.build_window_models_occ
gibbs_sample = window_model_occ.gibbs_sample
P8DIR = os.path.join(SCI, "ws_P8")
SC = RND / KCAL                                           # P8's scale: block sums (kJ/mol) -> kcal/mol, rounded up


class Log:
    """print to stdout and to a log file; .done() writes the LAST line, with the peak resident memory."""
    def __init__(self, path):
        self.path = path
        self.f = open(path, "w")
        self.t0 = time.time()

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n"); self.f.flush()

    def done(self):
        self(f"foreign writes attempted during import (refused): {len(FOREIGN_WRITES)}")
        self(f"ALL DONE {time.time() - self.t0:.0f} s; peak RSS {peak_rss():.0f} MB")
        self.f.close()


def peak_rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())


def tau_of(seq):
    return 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]


def tagname(seq, bb, tau):
    return f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"


def setup(seq, bb, tau):
    """as p6lib.setup: model, known tables, P3's coordinate-descent anchor."""
    G = GBModel(seq, bb, tau=tau)
    c0, h, J = pw.known_tables(G)
    x0, E0, nev = pw.icm_anchor(G, c0, h, J)
    return G, c0, h, J, [int(v) for v in x0], E0


# ============================================================================= the resolved bound of a subset
class ResBound(p8sr.AHBound):
    """p8sr.BlockBound (through AHBound) with the per-host-state block sums recorded before `_c1` / `_c2` maximise
    them.  Nothing of P8's arithmetic is changed: the recorded arrays are the arguments P8's code passes."""
    _cap = None

    def _c1(self, v, host, inT, anchored):
        if anchored and self._cap is not None:
            self._cap.append((host, None, np.array(v, dtype=float, copy=True)))
        return super()._c1(v, host, inT, anchored)

    def _c2(self, W, l, l2, in1, in2, anchored):
        if anchored and self._cap is not None:
            self._cap.append((l, l2, np.array(W, dtype=float, copy=True)))
        return super()._c2(W, l, l2, in1, in2, anchored)

    def blocks_T(self, m, T):
        """(P8's dict {'Sb': {key: const}, 'SAb': {...}}, list of (key, host1, host2, array over the host states)).
        Arrays in kJ/mol WITHOUT P8's factor SC (as P8's code passes them)."""
        self._cap = []
        out = self.total_T_blocks(m, T)
        cap, self._cap = self._cap, None
        keys = list(out["SAb"].keys())
        assert len(keys) == len(cap)
        res = []
        for key, (h1, h2, arr) in zip(keys, cap):
            if key[0] == "cross2":
                assert (h1, h2) == (key[1], key[2])
            else:
                assert h2 is None and (h1 == key[1] or (h1 is None and key[1] == -1))
            res.append((key, h1, h2, arr))
        return out, res


def theta_parts(SR, m, T, blocks=None):
    """The bound of the subset T with the ACTUAL states of the hosts in T (Theorem AH before the maximum over u),
    hosts outside T at the anchor, non-host sites through P3's maximal increments (first stage):

        Theta_T(x_T) = SC * ( C + sum_{l in T} A[l][x_l] + sum_{l < l2 in T} P[(l, l2)][x_l, x_l2] ),   x_l != x0_l,

    from P8's block arrays:  block without host: v[0] -> C;  host l: v[a_l] -> C, and v[x_l] -> A[l] if l in T;
    hosts l, l2: W[a, a2] -> C;  W[x_l, a2] -> A[l] if l in T;  W[a, x_l2] -> A[l2] if l2 in T;  W[x_l, x_l2] -> P if both.
    Returns dict(C, A, P, sab, sb): sab / sb = P8's constants of T (sum over blocks of its 'SAb' / 'Sb' values, kcal/mol).
    C, A, P are in kJ/mol without SC."""
    T = tuple(int(i) for i in T)
    out, blk = SR.blocks_T(m, T) if blocks is None else blocks
    a = SR.anchor; Tset = set(T); k = SR.G.k
    C = 0.0; A = {l: np.zeros(k[l]) for l in T}; P = {}
    for key, h1, h2, arr in blk:
        if h1 is None:
            C += float(arr[0])
        elif h2 is None:
            C += float(arr[a[h1]])
            if h1 in Tset:
                A[h1] += arr
        else:
            C += float(arr[a[h1], a[h2]])
            if h1 in Tset:
                A[h1] += arr[:, a[h2]]
            if h2 in Tset:
                A[h2] += arr[a[h1], :]
            if h1 in Tset and h2 in Tset:
                P[(h1, h2)] = arr
    return dict(T=T, C=C, A=A, P=P, sab=float(sum(out["SAb"].values())), sb=float(sum(out["Sb"].values())))


def nonanchor(k, x0, sites):
    return [np.array([b for b in range(k[l]) if b != x0[l]], dtype=int) for l in sites]


def theta_table(parts, k, x0):
    """Theta_T on the product of the NON-ANCHOR states of the sites of T (kcal/mol, P8's factor SC included):
    array of shape (k_l - 1 for l in T), and the lists of state indices."""
    T = parts["T"]; m = len(T)
    non = nonanchor(k, x0, T)
    tab = np.full([len(v) for v in non], parts["C"])
    for p, l in enumerate(T):
        sh = [1] * m; sh[p] = len(non[p])
        tab = tab + parts["A"][l][non[p]].reshape(sh)
    for (l, l2), W in parts["P"].items():
        p, p2 = T.index(l), T.index(l2)
        assert p < p2
        sh = [1] * m; sh[p] = len(non[p]); sh[p2] = len(non[p2])
        tab = tab + W[np.ix_(non[p], non[p2])].reshape(sh)
    return tab * SC, non


def theta_at(parts, X, x0):
    """Theta_T(x_T) at the rows of X (N, n) for which all sites of T are off the anchor; 0 elsewhere."""
    T = parts["T"]; X = np.atleast_2d(X)
    inS = np.ones(len(X), dtype=bool)
    for l in T:
        inS &= X[:, l] != x0[l]
    out = np.zeros(len(X))
    if inS.any():
        Y = X[inS]
        v = np.full(len(Y), parts["C"])
        for l in T:
            v += parts["A"][l][Y[:, l]]
        for (l, l2), W in parts["P"].items():
            v += W[Y[:, l], Y[:, l2]]
        out[inS] = v * SC
    return out


# ============================================================================= block tables of a subset, both stages
def _prodt(Ds, nc, na):
    """Ds: list of arrays (nc, r_i, na) -> (nc, prod r_i, na): products over the listed sites (C order)."""
    out = np.ones((nc, 1, na))
    for D in Ds:
        out = (out[:, :, None, :] * D[:, None, :, :]).reshape(nc, -1, na)
    return out


class Resolver:
    """Block bounds of a subset T as tables over the NON-ANCHOR states of the sites of T (axes in the order of T; an
    axis of length 1 where a block does not depend on a site).  kcal/mol, P8's factor SC included.

      stage 1: the hosts in T at their ACTUAL states (the arrays recorded in P8's own code path), hosts outside T at
               the anchor; non-host sites of T through P3's maximal increments.  A block depends on the axes of its
               hosts in T only.
      stage 2: hosts AND non-host sites of T at their actual states: P3's Corollary L2 with the actual increments
               delta^{p,c}_i(x_i) = |C^{p,c}_i(x_i) - C^{p,c}_i(x0_i)| (+ PAD_TAB wherever P3's maximal increment is
               non-zero).  Every other ingredient is the one P8 uses: per-host-state sup|ell^(k)|, sup|b^(k)|,
               sup|d^k h/dw^k| through p8sr.SRBound._stack / _M (suprema over ALL contexts).
               sum over set partitions of the free set B = sum over the splittings sigma of B into "sites taken with
               atom p" and "sites taken with atom q" of M_{|sigma|}[p, q] prod_{i in sigma} delta^p_i prod_{i not in sigma} delta^q_i
               (P8's identity, p8sr.hom2 / _M, with the products kept as functions of the states).
      maxmode=True replaces the actual increments by P3's maxima: stage 2 must then reproduce stage 1 (a check of
      this code against P8's).
      lite=True (stage 2 only): the blocks whose hosts are all OUTSIDE T (and that have a host) are taken at stage 1
      (constants); valid (each block is bounded separately), cheaper, slightly larger.
    """

    def __init__(self, SR, maxmode=False, lite=False):
        self.SR = SR; self.G = SR.G; self.n = SR.G.ns; self.k = list(SR.G.k); self.x0 = [int(v) for v in SR.anchor]
        self.non = nonanchor(self.k, self.x0, range(self.n))
        self.maxmode = maxmode; self.lite = lite; self._D = {}

    # ---- actual increments
    def D(self, o, i):
        """(number of host states of o, k_i - 1, atoms of o): the increment of the contribution of site i, in each of its
        non-anchor states, to the descreening integral of the atoms of o in each host state (nm^-1; PAD_TAB added
        wherever P3's maximal increment is non-zero, so that the maximum over the states IS P3's value -- asserted)."""
        key = (o.host, i)
        if key not in self._D:
            G = self.G
            dmax = self.SR._stack(o)["d"][:, i, :]
            C = np.asarray(G.A[i])[None] if o.host is None else np.asarray(G.T[(o.host, i)])
            assert C.shape == (dmax.shape[0], self.k[i], dmax.shape[1])
            d = np.abs(C - C[:, [self.x0[i]], :])
            d = np.where(dmax[:, None, :] > 0.0, d + PAD_TAB, 0.0)
            assert np.array_equal(d.max(axis=1), dmax), "per-state increments do not reproduce P3's maximal increments"
            if self.maxmode:
                d = np.broadcast_to(dmax[:, None, :], d.shape)
            self._D[key] = np.ascontiguousarray(d[:, self.non[i], :])
        return self._D[key]

    def _self(self, o, B, cs):
        """(len(cs), r_i for i in B): sum_p (KAPPA/2) q_p^2 sup|b_p^(|B|)| prod_{i in B} delta^p_i(x_i), kJ/mol."""
        st = self.SR._stack(o); nc = len(cs); na = len(o.atoms)
        w = 0.5 * KAPPA * (o.q ** 2)[None, :] * st["supB"][cs, len(B), :]
        Ds = [self.D(o, i)[cs] for i in B]
        h = len(Ds) // 2
        U = _prodt(Ds[:h], nc, na) * w[:, None, :]; V = _prodt(Ds[h:], nc, na)
        return np.matmul(U, V.transpose(0, 2, 1)).reshape([nc] + [D.shape[1] for D in Ds])

    def _prod(self, o, cs, sites):
        """cached (within one call of `blocks`): (len(cs), prod_{i in sites} r_i, atoms of o) = prod_i delta_i(x_i)."""
        key = (o.host, tuple(cs), tuple(sites))
        v = self._pc.get(key)
        if v is None:
            v = _prodt([self.D(o, i)[list(cs)] for i in sites], len(cs), len(o.atoms))
            self._pc[key] = v
        return v

    def _cross(self, o1, o2, B, cs1, cs2, coef):
        """(len(cs1), len(cs2), r_i for i in B)  [same host: (len(cs1), r_i ...)], kJ/mol:
        sum_{p, q} coef[p, q] sum_{sigma subset B} M_{|sigma|}[c1, c2, p, q] prod_{i in sigma} delta^{p,c1}_i(x_i) prod_{i not in sigma} delta^{q,c2}_i(x_i).
        Each splitting is contracted over the atoms without ever forming an array (all states of B) x (atoms): the
        larger of the two sides is itself split in two parts that are multiplied last."""
        s = len(B); M = self.SR._M(o1, o2, s, False)
        same = o1.host is not None and o1.host == o2.host
        n1, n2 = len(o1.atoms), len(o2.atoms)
        r = {i: len(self.non[i]) for i in B}
        size = lambda sites: int(np.prod([r[i] for i in sites])) if sites else 1
        lu = lambda A: A[:, None]                                   # atoms of o1: batch (b1, 1)
        lv = (lambda A: A[:, None]) if same else (lambda A: A[None])  # atoms of o2: batch (b, 1) for a shared host, else (1, b2)

        def split(sites, other):
            """(part 1, part 2) of `sites` minimising max(size(part 1) * other, size(part 2))."""
            best = None
            for mk in range(1 << len(sites)):
                p1 = [sites[j] for j in range(len(sites)) if (mk >> j) & 1]; p2 = [sites[j] for j in range(len(sites)) if not (mk >> j) & 1]
                c = max(size(p1) * other, size(p2))
                if best is None or c < best[0]:
                    best = (c, p1, p2)
            return best[1], best[2]

        out = None
        for mask in range(1 << s):
            sig = [B[j] for j in range(s) if (mask >> j) & 1]; rest = [B[j] for j in range(s) if not (mask >> j) & 1]
            a = len(sig)
            CM = (coef[None] * M[a][list(cs1)])[:, None] if same else coef[None, None] * M[a][np.ix_(cs1, cs2)]
            Rs, Rr = size(sig), size(rest)
            if Rs >= Rr:
                Wt = np.matmul(CM, lv(self._prod(o2, cs2, rest)).swapaxes(-1, -2))            # (b1, b2, n1, Rr)
                s1, s2 = split(sig, Rr)
                U1 = lu(self._prod(o1, cs1, s1)); U2 = lu(self._prod(o1, cs1, s2))
                Z = U1[:, :, :, None, :] * Wt.swapaxes(-1, -2)[:, :, None, :, :]             # (b1, b2, R1, Rr, n1)
                R = np.matmul(Z.reshape(Z.shape[0], Z.shape[1], -1, n1), U2.swapaxes(-1, -2))
                order = s1 + rest + s2
            else:
                Wt = np.matmul(lu(self._prod(o1, cs1, sig)), CM)                              # (b1, b2, Rs, n2)
                p1, p2 = split(rest, Rs)
                V1 = lv(self._prod(o2, cs2, p1)); V2 = lv(self._prod(o2, cs2, p2))
                Z = Wt[:, :, :, None, :] * V1[:, :, None, :, :]                               # (b1, b2, Rs, R1, n2)
                R = np.matmul(Z.reshape(Z.shape[0], Z.shape[1], -1, n2), V2.swapaxes(-1, -2))
                order = sig + p1 + p2
            R = R.reshape(list(R.shape[:2]) + [r[i] for i in order]).transpose([0, 1] + [2 + order.index(i) for i in B])
            if out is None:
                out = np.array(R, dtype=float, order="C")
            else:
                out += R
        return out[:, 0] if same else out

    def blocks(self, m, T, stage):
        """(P8's dict of block constants 'Sb' / 'SAb', list of (key, table)); the tables broadcast against the shape
        (k_t - 1 for t in T) and are in kcal/mol (factor SC included).  Keys in P8's order."""
        T = tuple(int(i) for i in T); Tl = list(T); pos = {l: p for p, l in enumerate(T)}
        a, non, k, n, SR = self.x0, self.non, self.k, self.n, self.SR
        out, blk = SR.blocks_T(m, T)
        self._pc = {}

        def place(arr, sites):
            arr = np.asarray(arr, dtype=float)
            assert arr.ndim == len(sites)
            sh = [1] * m
            if len(sites):
                order = sorted(range(len(sites)), key=lambda j: pos[sites[j]])
                arr = arr.transpose(order)
                for j, jj in enumerate(order):
                    sh[pos[sites[jj]]] = arr.shape[j]
            return arr.reshape(sh)

        def stage1(key, h1, h2, arr):
            if h1 is None:
                return place(arr[0], [])
            if h2 is None:
                return place(arr[a[h1]] + arr[non[h1]], [h1]) if h1 in pos else place(arr[a[h1]], [])
            in1, in2 = h1 in pos, h2 in pos
            if in1 and in2:
                return place(arr[a[h1], a[h2]] + arr[a[h1]][non[h2]][None, :] + arr[non[h1], a[h2]][:, None] + arr[np.ix_(non[h1], non[h2])], [h1, h2])
            if in1:
                return place(arr[a[h1], a[h2]] + arr[non[h1], a[h2]], [h1])
            if in2:
                return place(arr[a[h1], a[h2]] + arr[a[h1], non[h2]], [h2])
            return place(arr[a[h1], a[h2]], [])

        s1 = [(key, stage1(key, h1, h2, arr) * SC) for key, h1, h2, arr in blk]
        self._last_s1 = s1
        if stage == 1:
            return out, s1
        assert stage == 2
        s1d = dict(s1); res = []
        F = SR.F
        res.append((("self", -1), place(self._self(F, Tl, [0])[0], Tl) * SC))
        cFF = np.triu(KAPPA * np.abs(F.q[:, None] * F.q[None, :]), 1)
        res.append((("cross1", -1), place(self._cross(F, F, Tl, [0], [0], cFF)[0, 0], Tl) * SC))
        for l in range(n):
            o = SR.site[l]; inl = l in pos; B = [i for i in Tl if i != l]; allc = list(range(k[l]))
            if inl:
                cFo = KAPPA * np.abs(F.q[:, None] * o.q[None, :]); coo = np.triu(KAPPA * np.abs(o.q[:, None] * o.q[None, :]), 1)
                V = self._self(o, B, allc)
                res.append((("self", l), place(V[a[l]][None] + V[non[l]], [l] + B) * SC))
                V = self._cross(F, o, B, [0], allc, cFo)[0] + self._cross(o, o, B, allc, allc, coo)
                res.append((("cross1", l), place(V[a[l]][None] + V[non[l]], [l] + B) * SC))
            elif self.lite:
                res.append((("self", l), s1d[("self", l)])); res.append((("cross1", l), s1d[("cross1", l)]))
            else:
                cFo = KAPPA * np.abs(F.q[:, None] * o.q[None, :]); coo = np.triu(KAPPA * np.abs(o.q[:, None] * o.q[None, :]), 1)
                res.append((("self", l), place(self._self(o, B, [a[l]])[0], B) * SC))
                V = self._cross(F, o, B, [0], [a[l]], cFo)[0, 0] + self._cross(o, o, B, [a[l]], [a[l]], coo)[0]
                res.append((("cross1", l), place(V, B) * SC))
            for l2 in range(l + 1, n):
                o2 = SR.site[l2]; in2 = l2 in pos; B2 = [i for i in Tl if i != l and i != l2]; key = ("cross2", l, l2)
                if not inl and not in2 and self.lite:
                    res.append((key, s1d[key])); continue
                c12 = KAPPA * np.abs(o.q[:, None] * o2.q[None, :])
                if inl and in2:
                    W = self._cross(o, o2, B2, allc, list(range(k[l2])), c12)
                    tab = W[a[l], a[l2]][None, None] + W[a[l]][non[l2]][None, :] + W[non[l], a[l2]][:, None] + W[non[l]][:, non[l2]]
                    res.append((key, place(tab, [l, l2] + B2) * SC))
                elif inl:
                    W = self._cross(o, o2, B2, allc, [a[l2]], c12)[:, 0]
                    res.append((key, place(W[a[l]][None] + W[non[l]], [l] + B2) * SC))
                elif in2:
                    W = self._cross(o, o2, B2, [a[l]], list(range(k[l2])), c12)[0]
                    res.append((key, place(W[a[l2]][None] + W[non[l2]], [l2] + B2) * SC))
                else:
                    res.append((key, place(self._cross(o, o2, B2, [a[l]], [a[l2]], c12)[0, 0], B2) * SC))
        assert [key for key, _ in res] == [key for key, _ in s1]
        self._pc = {}
        return out, res

    def theta(self, m, T, stage):
        """(Theta_T on the non-anchor states of T, full shape; P8's 'SAb' constant of T; P8's 'Sb' constant)."""
        out, blk = self.blocks(m, T, stage)
        shape = [len(self.non[t]) for t in T]
        tab = np.zeros(shape)
        for key, t in blk:
            tab += t
        return tab, float(sum(out["SAb"].values())), float(sum(out["Sb"].values()))

    def theta_both(self, m, T):
        """(Theta^1_T, Theta^2_T, P8's 'SAb', P8's 'Sb') from one pass (stage 2 computes the stage-1 tables on its way)."""
        out, blk2 = self.blocks(m, T, 2)
        shape = [len(self.non[t]) for t in T]
        t1 = np.zeros(shape); t2 = np.zeros(shape)
        for key, t in self._last_s1:
            t1 += t
        for key, t in blk2:
            t2 += t
        return t1, t2, float(sum(out["SAb"].values())), float(sum(out["Sb"].values()))


# ============================================================================= tables
class Tables:
    """Top-level sums of the reduced bounds over the subsets (kcal/mol), on FULL state axes (anchor rows are zero):
        S1[i][b]              = sum_{T ni i}          max{ Theta_T(y_T) : y_i = b }                     (n arrays (k_i,))
        S2[(i,j)][b_i, b_j]   = sum_{T contains i,j}  max{ Theta_T(y_T) : y_i = b_i, y_j = b_j }        (all pairs i < j)
        S3[(i,j,l)][...]      = sum_{T contains i,j,l} max{ Theta_T(y_T) : y fixed on the triple }      (all triples)
    the per-subset constants cJ = max over y_T (joint maximum), cmin = min over y_T, sab / sb (P8's), and -- if
    keep=True -- the tables Theta_T themselves (for the envelope sum_{T subset S(x)} Theta_T(x_T))."""

    def __init__(self, n, k, x0, m, keep=True):
        self.n, self.k, self.x0, self.m, self.keep = n, list(k), list(x0), m, keep
        self.non = nonanchor(self.k, self.x0, range(n))
        self.S1 = [np.zeros(k[i]) for i in range(n)]
        self.S2 = {(i, j): np.zeros((k[i], k[j])) for i in range(n) for j in range(i + 1, n)}
        self.S3 = {(i, j, l): np.zeros((k[i], k[j], k[l])) for i in range(n) for j in range(i + 1, n) for l in range(j + 1, n)}
        self.subs = []; self.cJ = []; self.sab = []; self.sb = []; self.cmin = []; self.tabs = []

    def add(self, T, tab, sab, sb):
        T = tuple(int(i) for i in T); m = self.m; non = [self.non[t] for t in T]
        assert tab.shape == tuple(len(v) for v in non)
        self.subs.append(T); self.cJ.append(float(tab.max())); self.cmin.append(float(tab.min()))
        self.sab.append(sab); self.sb.append(sb)
        if self.keep:
            self.tabs.append(tab)
        for p in range(m):
            ax = tuple(q for q in range(m) if q != p)
            self.S1[T[p]][non[p]] += tab.max(axis=ax)
        for p, p2 in itertools.combinations(range(m), 2):
            ax = tuple(q for q in range(m) if q not in (p, p2))
            self.S2[(T[p], T[p2])][np.ix_(non[p], non[p2])] += tab.max(axis=ax)
        for p, p2, p3 in itertools.combinations(range(m), 3):
            ax = tuple(q for q in range(m) if q not in (p, p2, p3))
            self.S3[(T[p], T[p2], T[p3])][np.ix_(non[p], non[p2], non[p3])] += (tab.max(axis=ax) if ax else tab)

    def finish(self):
        for name in ("cJ", "sab", "sb", "cmin"):
            setattr(self, name, np.array(getattr(self, name)))
        return self

    def envelope(self, X):
        """sum_{T subset S(x)} Theta_T(x_T) at the rows of X (needs keep=True)."""
        X = np.atleast_2d(X); out = np.zeros(len(X))
        pos = [np.full(self.k[i], -1) for i in range(self.n)]
        for i in range(self.n):
            pos[i][self.non[i]] = np.arange(len(self.non[i]))
        P = np.stack([pos[i][X[:, i]] for i in range(self.n)], axis=1)
        for T, tab in zip(self.subs, self.tabs):
            idx = P[:, list(T)]; inS = (idx >= 0).all(axis=1)
            if inS.any():
                out[inS] += tab[tuple(idx[inS].T)]
        return out

    def save(self, fn, with_tabs=False):
        d = dict(n=self.n, k=np.array(self.k), x0=np.array(self.x0), m=self.m, subs=np.array(self.subs), cJ=self.cJ, sab=self.sab, sb=self.sb, cmin=self.cmin)
        for i in range(self.n):
            d[f"S1_{i}"] = self.S1[i]
        for key, v in self.S2.items():
            d["S2_" + "_".join(map(str, key))] = v
        for key, v in self.S3.items():
            d["S3_" + "_".join(map(str, key))] = v
        if with_tabs:
            for j, t in enumerate(self.tabs):
                d[f"tab_{j}"] = t
        np.savez(fn, **d)

    @staticmethod
    def load(fn, with_tabs=False):
        z = np.load(fn)
        TB = Tables(int(z["n"]), [int(v) for v in z["k"]], [int(v) for v in z["x0"]], int(z["m"]), keep=with_tabs)
        TB.subs = [tuple(int(v) for v in T) for T in z["subs"]]
        for name in ("cJ", "sab", "sb", "cmin"):
            setattr(TB, name, np.array(z[name]))
        for i in range(TB.n):
            TB.S1[i] = np.array(z[f"S1_{i}"])
        for key in TB.S2:
            TB.S2[key] = np.array(z["S2_" + "_".join(map(str, key))])
        for key in TB.S3:
            TB.S3[key] = np.array(z["S3_" + "_".join(map(str, key))])
        if with_tabs:
            TB.tabs = [np.array(z[f"tab_{j}"]) for j in range(len(TB.subs))]
        return TB


def off_mask(k, x0):
    off = [np.ones(k[i]) for i in range(len(k))]
    for i in range(len(k)):
        off[i][x0[i]] = 0.0
    return off


def form_tables(TB, form, w, resolved=True, const=None):
    """Penalty tables of the three share forms, as (g1: list of (k_i,), g2: dict in-band pair -> (k_i, k_j),
    g3: dict in-window triple -> (k_i, k_j, k_l)), kcal/mol, every entry rounded up by RND, anchor rows zero.

    resolved=True: from the state-resolved sums TB.S1 / S2 / S3.
        'S'  gamma_i(b) = S1_i(b) / m.
        'B'  gamma_ij = S2_ij / C(m,2);  in band (j - i <= w): kept;  beyond the band: one half of
             max_{b_j} gamma_ij(b_i, b_j) to site i and one half of max_{b_i} gamma_ij(b_i, b_j) to site j.
        'T'  gamma_ijl = S3_ijl / C(m,3);  in window (l - i <= w): kept;  else one third of its maximum over each of
             its sites to the pair of the two others; the pair tables so collected: in band kept, beyond the band
             in halves to the sites as in 'B'.
    resolved=False: the same chains with the state-independent constants `const` (array over TB.subs; e.g. TB.sab or
        TB.cJ): every table is constant on the non-anchor states.  This is P6's Lemma A / A' (without the
        floating-point allowances, which the drivers add separately through p6lib.fp_tables)."""
    n, k, x0, m = TB.n, TB.k, TB.x0, TB.m
    off = off_mask(k, x0)
    if resolved:
        S1, S2, S3 = TB.S1, TB.S2, TB.S3
    else:
        s1 = np.zeros(n); s2 = {key: 0.0 for key in TB.S2}; s3 = {key: 0.0 for key in TB.S3}
        for T, v in zip(TB.subs, const):
            for i in T:
                s1[i] += v
            for pr in itertools.combinations(T, 2):
                s2[pr] += v
            for tr in itertools.combinations(T, 3):
                s3[tr] += v
        S1 = [s1[i] * off[i] for i in range(n)]
        S2 = {(i, j): v * np.outer(off[i], off[j]) for (i, j), v in s2.items()}
        S3 = {(i, j, l): v * off[i][:, None, None] * off[j][None, :, None] * off[l][None, None, :] for (i, j, l), v in s3.items()}
    g1 = [np.zeros(k[i]) for i in range(n)]; g2 = {}; g3 = {}
    if form == "S":
        g1 = [S1[i] / m for i in range(n)]
    else:
        pair = {key: np.zeros((k[key[0]], k[key[1]])) for key in TB.S2}
        if form == "B":
            c2 = math.comb(m, 2)
            for key in pair:
                pair[key] = S2[key] / c2
        elif form == "T":
            c3 = math.comb(m, 3)
            for (i, j, l), tab in S3.items():
                t = tab / c3
                if l - i <= w:
                    g3[(i, j, l)] = t
                else:
                    pair[(i, j)] += t.max(axis=2) / 3.0
                    pair[(i, l)] += t.max(axis=1) / 3.0
                    pair[(j, l)] += t.max(axis=0) / 3.0
        else:
            raise ValueError(form)
        for (i, j), tab in pair.items():
            if j - i <= w:
                g2[(i, j)] = tab
            else:
                g1[i] = g1[i] + 0.5 * tab.max(axis=1)
                g1[j] = g1[j] + 0.5 * tab.max(axis=0)
    g1 = [v * RND for v in g1]
    g2 = {key: v * RND for key, v in g2.items() if np.any(v != 0.0)}
    g3 = {key: v * RND for key, v in g3.items() if np.any(v != 0.0)}
    return g1, g2, g3


def pen_value(X, g1, g2, g3):
    """sum_i g1_i(x_i) + sum g2_ij(x_i, x_j) + sum g3_ijl(x_i, x_j, x_l) at the rows of X."""
    X = np.atleast_2d(X)
    out = np.zeros(len(X))
    for i, v in enumerate(g1):
        out += v[X[:, i]]
    for (i, j), v in g2.items():
        out += v[X[:, i], X[:, j]]
    for (i, j, l), v in g3.items():
        out += v[X[:, i], X[:, j], X[:, l]]
    return out


def envelope_value(parts_list, X, x0):
    """the fully resolved envelope sum_{T subset S(x)} Theta_T(x_T) at the rows of X."""
    X = np.atleast_2d(X)
    out = np.zeros(len(X))
    for parts in parts_list:
        out += theta_at(parts, X, x0)
    return out


def const_envelope(subs, const, X, x0):
    """sum_{T subset S(x)} chat_T (state-independent constants)."""
    X = np.atleast_2d(X); s = X != np.asarray(x0)[None]
    out = np.zeros(len(X))
    for T, v in zip(subs, const):
        out += v * s[:, list(T)].all(axis=1)
    return out


# ============================================================================= left side: remainders by enumeration
def remainder_grid(F, x0, m):
    """F - I_{m-1} F on the whole grid (F: array over the n site axes, optional trailing axes): the sum of the anchored
    components d_U over |U| >= m, computed as F minus the components of order < m (my own code: successive anchored
    differences along the site axes; pattern of p8_verification/lys_enum_check.remainder, written for trailing axes)."""
    n = len(x0)
    acc = np.zeros_like(F)
    for r in range(0, m):
        for U in itertools.combinations(range(n), r):
            d = F
            for i in range(n):
                a = np.take(d, [x0[i]], axis=i)
                d = (d - a) if i in U else a
            acc = acc + d
    return F - acc


def enumerate_g(G, tag, log=None):
    """g at every state with P3's bulk evaluator (my own evaluation, cached in ws_P9/cache)."""
    fn = os.path.join(MYCACHE, f"enum_{tag}.npy")
    st = G.product_states()
    if os.path.exists(fn):
        g = np.load(fn)
        if len(g) == len(st):
            return st, g, "ws_P9 cache (my earlier evaluation)"
    g = np.empty(len(st)); t0 = time.time()
    for s in range(0, len(st), 256):
        g[s:s + 256] = G.bulk_energy(st[s:s + 256])
    np.save(fn, g)
    return st, g, f"evaluated now with P3's bulk evaluator ({time.time() - t0:.0f} s)"


# ============================================================================= full-size tables: accumulation, parts, files
def maximal_windows(U, w):
    """the maximal sub-tuples (as tuples of POSITIONS in U) of the sorted tuple U whose sites fit a window of w + 1
    consecutive sites (the coordinator's rule in window_model_occ.py)."""
    sets = []
    for a in range(len(U)):
        V = tuple(p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w)
        if not any(set(V) <= set(V2) for V2 in sets):
            sets = [V2 for V2 in sets if not set(V2) <= set(V)] + [V]
    return sets


class Acc:
    """Everything that is accumulated over the subsets T, for both stages, without keeping the tables Theta_T:
       TB[s]            top-level sums S1, S2, S3 (class Tables), per-subset maxima / minima;
       env[s][seed]     the fully resolved envelope sum_{T subset S(x)} Theta_T(x_T) at the states of the Gibbs samples;
       W[s][K]          the WINDOW form: every subset T is charged in full to ONE sub-tuple K of its sites that fits a
                        window (T itself if it fits), through max over the given-up sites; K = the maximal in-window
                        sub-tuple with the least expected value of the reduced table under the product of the
                        one-site marginals of the guiding sample (ties: least maximum).  Valid for every choice;
       typ[s]           per subset: sum over the non-anchor states of Theta_T(x_T) prod_i p_i(x_i) (p_i: one-site
                        marginals of the guiding sample with pseudo-count 1/2) -- an estimate of E[Theta_T; T off].
    """

    def __init__(self, n, k, x0, m, w, samples):
        self.n, self.k, self.x0, self.m, self.w = n, list(k), list(x0), m, w
        self.TB = {s: Tables(n, k, x0, m, keep=False) for s in (1, 2)}
        self.non = self.TB[1].non
        self.pos = [np.full(k[i], -1) for i in range(n)]
        for i in range(n):
            self.pos[i][self.non[i]] = np.arange(len(self.non[i]))
        self.samples = samples                                             # dict seed -> X (N, n)
        self.P = {sd: np.stack([self.pos[i][X[:, i]] for i in range(n)], axis=1) for sd, X in samples.items()}
        self.env = {s: {sd: np.zeros(len(X)) for sd, X in samples.items()} for s in (1, 2)}
        self.W = {1: {}, 2: {}}
        self.idx = []; self.typ = {1: [], 2: []}; self.med = {1: [], 2: []}; self.keep = {1: [], 2: []}; self.tabs2 = []
        guide = samples[min(samples)] if 4242 not in samples else samples[4242]
        self.pm = []
        for i in range(n):
            cnt = np.bincount(guide[:, i], minlength=k[i]).astype(float)
            self.pm.append(((cnt + 0.5) / (len(guide) + 0.5 * k[i]))[self.non[i]])

    def add(self, index, T, th1, th2, sab, sb, keeptabs=False):
        m, w = self.m, self.w
        self.idx.append(index)
        for s, tab in ((1, th1), (2, th2)):
            self.TB[s].add(T, tab, sab, sb)
            for sd, P in self.P.items():
                I = P[:, list(T)]; inS = (I >= 0).all(axis=1)
                if inS.any():
                    self.env[s][sd][inS] += tab[tuple(I[inS].T)]
            t = tab
            for p in range(m - 1, -1, -1):
                t = t @ self.pm[T[p]]
            self.typ[s].append(float(t)); self.med[s].append(float(np.median(tab)))
            best = None
            for keep in ([tuple(range(m))] if T[-1] - T[0] <= w else maximal_windows(T, w)):
                other = tuple(p for p in range(m) if p not in keep)
                red = tab.max(axis=other) if other else tab
                sc = red
                for p in reversed(keep):
                    sc = sc @ self.pm[T[p]]
                key = (float(sc), float(red.max()))
                if best is None or key < best[0]:
                    best = (key, keep, red)
            _, keep, red = best
            K = tuple(T[p] for p in keep)
            if K not in self.W[s]:
                self.W[s][K] = np.zeros([self.k[i] for i in K])
            self.W[s][K][np.ix_(*[self.non[i] for i in K])] += red
            self.keep[s].append(K)
        if keeptabs:
            self.tabs2.append(th2)

    def to_dict(self):
        d = dict(n=self.n, k=np.array(self.k), x0=np.array(self.x0), m=self.m, w=self.w, idx=np.array(self.idx, dtype=int))
        for s in (1, 2):
            TB = self.TB[s]
            d[f"s{s}_subs"] = np.array(TB.subs, dtype=int).reshape(-1, self.m)
            for name in ("cJ", "sab", "sb", "cmin"):
                d[f"s{s}_{name}"] = np.array(getattr(TB, name))
            d[f"s{s}_typ"] = np.array(self.typ[s]); d[f"s{s}_med"] = np.array(self.med[s])
            d[f"s{s}_keep"] = np.array(["_".join(map(str, K)) for K in self.keep[s]])
            for i in range(self.n):
                d[f"s{s}_S1_{i}"] = TB.S1[i]
            for key, v in TB.S2.items():
                d[f"s{s}_S2_" + "_".join(map(str, key))] = v
            for key, v in TB.S3.items():
                d[f"s{s}_S3_" + "_".join(map(str, key))] = v
            for key, v in self.W[s].items():
                d[f"s{s}_W_" + "_".join(map(str, key))] = v
            for sd, v in self.env[s].items():
                d[f"s{s}_env_{sd}"] = v
        return d


def merge_parts(files):
    """sum the additive accumulators of several part files (dicts as written by Acc.to_dict) into one dict."""
    out = None
    for fn in files:
        z = dict(np.load(fn))
        if out is None:
            out = z; continue
        for key, v in z.items():
            if key in ("n", "k", "x0", "m", "w"):
                assert np.array_equal(out[key], v)
            elif key == "idx" or key.endswith(("_subs", "_cJ", "_sab", "_sb", "_cmin", "_typ", "_med", "_keep")):
                out[key] = np.concatenate([out[key], v], axis=0)
            elif key in out:
                out[key] = out[key] + v
            else:
                out[key] = v
    order = np.argsort(out["idx"])
    for key in list(out):
        if key == "idx" or key.endswith(("_subs", "_cJ", "_sab", "_sb", "_cmin", "_typ", "_med", "_keep")):
            out[key] = out[key][order]
    return out


class Loaded:
    """the merged tables of one instance and order, as read from out/tables_<tag>_m<m>_w<w>.npz."""

    def __init__(self, fn):
        z = np.load(fn)
        self.n = int(z["n"]); self.k = [int(v) for v in z["k"]]; self.x0 = [int(v) for v in z["x0"]]; self.m = int(z["m"]); self.w = int(z["w"])
        self.TB = {}; self.W = {}; self.env = {}; self.typ = {}; self.med = {}; self.keep = {}
        for s in (1, 2):
            TB = Tables(self.n, self.k, self.x0, self.m, keep=False)
            TB.subs = [tuple(int(v) for v in T) for T in z[f"s{s}_subs"]]
            for name in ("cJ", "sab", "sb", "cmin"):
                setattr(TB, name, np.array(z[f"s{s}_{name}"]))
            for i in range(self.n):
                TB.S1[i] = np.array(z[f"s{s}_S1_{i}"])
            for key in TB.S2:
                TB.S2[key] = np.array(z[f"s{s}_S2_" + "_".join(map(str, key))])
            for key in TB.S3:
                TB.S3[key] = np.array(z[f"s{s}_S3_" + "_".join(map(str, key))])
            self.TB[s] = TB
            pre = f"s{s}_W_"
            self.W[s] = {tuple(int(v) for v in f[len(pre):].split("_")): np.array(z[f]) for f in z.files if f.startswith(pre)}
            pre = f"s{s}_env_"
            self.env[s] = {int(f[len(pre):]): np.array(z[f]) for f in z.files if f.startswith(pre)}
            self.typ[s] = np.array(z[f"s{s}_typ"]); self.med[s] = np.array(z[f"s{s}_med"]); self.keep[s] = [str(v) for v in z[f"s{s}_keep"]]


def window_form(W):
    """the window-form tables as (g1, g2, g3) for the band models: sub-tuples of one site -> site tables, of two
    sites -> pair tables, of three and more -> window tables; every entry rounded up by RND."""
    g1 = {}; g2 = {}; g3 = {}
    for K, tab in W.items():
        (g1 if len(K) == 1 else g2 if len(K) == 2 else g3)[K] = tab * RND
    return g1, g2, g3


def load_gibbs(tag, seed):
    z = np.load(os.path.join(MYCACHE, f"gibbs_{tag}_seed{seed}.npz"))
    return np.array(z["X"], dtype=int), np.array(z["g"]), np.array(z["f"])


def off_frequencies(X, k, x0):
    """off-anchor frequency of every site in the sample X, with the pseudo-count 1/2 per state used by Acc."""
    X = np.atleast_2d(X); out = []
    for i in range(len(k)):
        cnt = np.bincount(X[:, i], minlength=k[i]).astype(float)
        p = (cnt + 0.5) / (len(X) + 0.5 * k[i])
        out.append(float(p.sum() - p[x0[i]]))
    return out


def window_form_const(subs, const, k, x0, w, poff):
    """The window form with STATE-INDEPENDENT constants: every subset T is charged in full to the maximal in-window
    sub-tuple K of its sites with the least product of off-anchor frequencies (T itself if it fits a window):
    chat_T [T subset S(x)] <= chat_T prod_{i in K} [x_i != x0_i].  An allocation in the sense of the theory division's
    Proposition 11.18f (any sub-tuple is valid); workstream P8 estimated it to first order (its column "least-occupied
    in-window sub-tuple").  Returns (g1, g2, g3) as window_form."""
    import functools
    off = off_mask(k, x0); acc = {}
    for T, v in zip(subs, const):
        cands = [tuple(range(len(T)))] if T[-1] - T[0] <= w else maximal_windows(T, w)
        keep = min(cands, key=lambda K: (float(np.prod([poff[T[p]] for p in K])), -len(K)))
        K = tuple(T[p] for p in keep)
        acc[K] = acc.get(K, 0.0) + float(v)
    return window_form({K: v * functools.reduce(np.multiply.outer, [off[i] for i in K]) for K, v in acc.items()})
