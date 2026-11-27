"""
Workstream P8 -- shared library.

Reads (never writes) the modules of workstreams P3 (p3core.GBModel, encl.EnvelopeSup,
gfbound.GFBound, termwise.set_partitions), P5 (p5lib: build, kernel, anchored constants) and,
through them, P2.  Nothing is written outside ws_P8:
  * sys.dont_write_bytecode is set before any foreign import (run with python3 -B as well);
  * P3's enclosure cache directory (encl.CACHE) is redirected to ws_P8/cache, which is
    pre-filled with COPIES of the tables already built by P3 / P5 / P6 (read from their cache
    directories, written into mine).

Objects (notation of P5's report).  Atoms p = 1..N, charges q_p; kernel matrix
    M_pq(x) = h(ell_p(x) + ell_q(x); r_pq(x)) (p != q),   M_pp(x) = 1/B_p(x);
PAIR TERMS (unordered pairs p <= q; kcal/mol):
    t_pq(x) = -KAPPA q_p q_q M_pq(x) / KCAL  (p < q),      t_pp(x) = -(KAPPA/2) q_p^2 M_pp(x) / KCAL,
    g(x) = sum_{p <= q} t_pq(x).
Anchored constant of a function F for a set T of sites:  c_T(F) = sup |Delta_T F(z; x0_T -> y_T)|
over all contexts z and all states y_T (P5's `anch_consts`).
"""
import sys, os, time, glob, shutil, itertools, math, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
for _d in ("ws_P3", "ws_P5"):
    _p = os.path.join(SCI, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
import numpy as np
import p5lib as P5                                   # P5 (read-only); it redirects encl.CACHE to ws_P5/cache ...
import encl                                          # P3 (read-only)
MYCACHE = os.path.join(HERE, "cache")
os.makedirs(MYCACHE, exist_ok=True)
for _src in ("ws_P3", "ws_P5", "ws_P6"):             # copies INTO my cache; the sources are only read
    for _fn in glob.glob(os.path.join(SCI, _src, "cache", "atom_*.npz")) + glob.glob(os.path.join(SCI, _src, "cache", "zeta_*.npz")):
        _dst = os.path.join(MYCACHE, os.path.basename(_fn))
        if not os.path.exists(_dst):
            shutil.copy(_fn, _dst)
encl.CACHE = MYCACHE                                 # ... and here it is redirected to ws_P8/cache
from p3core import GBModel, KAPPA, KCAL, KT300, BETA
from encl import EnvelopeSup
from gfbound import GFBound, RND, bell_arrays, esym2, esym1, PAD_TAB
from termwise import set_partitions
from p5lib import Tee, build, subsets, anchored_interp
import gc


def anch_walk(*args, **kw):
    """p5lib.anch_walk followed by gc.collect().  P5's walk defines a recursive closure that keeps its base array F
    in a reference cycle; without a collection every call leaks one full array until Python's cyclic collector happens
    to run (memory incident of 06:46 in NOTES.md: 11.7 GB)."""
    try:
        return P5.anch_walk(*args, **kw)
    finally:
        gc.collect()


def anch_consts(*args, **kw):
    """p5lib.anch_consts followed by gc.collect() (see anch_walk)."""
    try:
        return P5.anch_consts(*args, **kw)
    finally:
        gc.collect()

PRE = -KAPPA / KCAL                                  # t_pq = PRE q_p q_q M_pq (p < q); t_pp = (PRE/2) q_p^2 M_pp
CLASSES = ["bb", "nsc", "chain", "head"]            # backbone (all fixed atoms), neutral side chain, aliphatic chain of a
                                                     # charged side chain, charged head group (NZ, HZ* / CD, OE*)
HEAD = {"K": ("NZ", "HZ1", "HZ2", "HZ3"), "E": ("CD", "OE1", "OE2"), "D": ("CG", "OD1", "OD2"), "R": ("NE", "HE", "CZ", "NH1", "HH11", "HH12", "NH2", "HH21", "HH22")}


class Log:
    """print to stdout and to a log file (append=True continues an interrupted run's log); .done() writes the last line."""
    def __init__(self, path, append=False):
        self.f = open(path, "a" if append else "w")
        self.t0 = time.time()

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n"); self.f.flush()

    def done(self):
        import resource
        self(f"DONE in {time.time() - self.t0:.1f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0:.0f} MB")
        self.f.close()


def rss_mb():
    """current resident set size of this process in MB (Linux /proc)."""
    with open("/proc/self/statm") as fh:
        return int(fh.read().split()[1]) * os.sysconf("SC_PAGE_SIZE") / 1e6


THREE = dict(LYS="K", GLU="E", ASP="D", ARG="R", LEU="L", SER="S", VAL="V", PHE="F", ALA="A", GLY="G", ILE="I", THR="T", ASN="N", GLN="Q",
             MET="M", CYS="C", TRP="W", TYR="Y", HIS="H", PRO="P")


def anchored_remainders(F, x0, n, orders):
    """For F of shape (k_1, ..., k_n) + extra: dict m -> array over `extra` of sup over all states of |F - I_{m-1} F|,
    I_M F = sum_{|U| <= M} d_U the anchored expansion at x0 (inclusion-exclusion as in P5's anchored_interp, with trailing axes)."""
    shape = F.shape[:n]; extra = F.shape[n:]
    acc = np.zeros_like(F)
    out = {}
    for r in range(0, max(orders)):
        for U in itertools.combinations(range(n), r):
            if any(shape[i] < 2 for i in U):
                continue
            idx = tuple(slice(None) if i in U else x0[i] for i in range(n))
            dd = F[idx].copy()
            for a_, i in enumerate(U):
                dd = dd - np.take(dd, [x0[i]], axis=a_)
            acc += dd.reshape([shape[i] if i in U else 1 for i in range(n)] + list(extra))
        if (r + 1) in orders:
            R = np.abs(F - acc)
            out[r + 1] = R.reshape((-1,) + tuple(extra)).max(axis=0)
            del R
    return out


def tagname(seq, bb, tau):
    return f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"


def atom_classes(G):
    """integer array (N,) with the index into CLASSES of every atom, and the residue letter of every atom ('-' for caps)."""
    P = G.P
    seq = list(P.seq)
    names = list(P.names); resid = np.asarray(P.resid); site = np.asarray(P.site_of_atom)
    cls = np.zeros(G.nat, dtype=int)
    letter = []
    for p in range(G.nat):
        r = int(resid[p])
        aa = seq[r - 1] if 1 <= r <= len(seq) else "-"
        aa = THREE.get(aa, aa)                       # P2's builder stores three-letter residue names
        letter.append(aa)
        if site[p] == 0:
            cls[p] = 0
        elif aa in HEAD:
            cls[p] = 3 if names[p] in HEAD[aa] else 2
        else:
            cls[p] = 1
    return cls, letter


def fine_groups(G):
    """labels (N,) of the groups 'per residue: fixed part / moving neutral side chain / chain / head' (caps whole), and names."""
    P = G.P
    cls, letter = atom_classes(G)
    resid = np.asarray(P.resid)
    lab = {}; out = np.zeros(G.nat, dtype=int); names = []
    for p in range(G.nat):
        key = (int(resid[p]), int(cls[p]))
        if key not in lab:
            lab[key] = len(lab); names.append(f"{letter[p]}{key[0]}:{CLASSES[key[1]]}")
        out[p] = lab[key]
    return out, names


def pair_index(nc):
    """index of the unordered pair (a <= b) of nc classes in a flat list, and the list of pairs."""
    pairs = [(a, b) for a in range(nc) for b in range(a, nc)]
    idx = -np.ones((nc, nc), dtype=int)
    for k, (a, b) in enumerate(pairs):
        idx[a, b] = idx[b, a] = k
    return idx, pairs


def kernel_row(G, st, p, B, cols, chunk=20000):
    """M[x, p, q] for q in cols, all states: (S, len(cols)), nm^-1 (diagonal q = p: 1/B_p)."""
    S = st.shape[0]
    out = np.empty((S, len(cols)))
    for s0 in range(0, S, chunk):
        sub = st[s0:s0 + chunk]
        X = G.coords(sub)
        d = X[:, p, None, :] - X[:, cols, :]
        r2 = (d * d).sum(-1)
        BB = B[s0:s0 + chunk, p, None] * B[s0:s0 + chunk][:, cols]
        out[s0:s0 + chunk] = 1.0 / np.sqrt(r2 + BB * np.exp(-r2 / (4.0 * BB)))
    return out


def pair_coef(G, p, cols, q=None):
    """coefficients c with t_pq = c * M_pq for q in cols (cols >= p): PRE q_p q_q, halved on the diagonal."""
    q = G.q if q is None else q
    c = PRE * q[p] * q[cols]
    c = np.where(np.asarray(cols) == p, 0.5 * c, c)
    return c


# ----------------------------------------------------------------------------- P3's bound, pair by pair
class GFDecomp(GFBound):
    """P3's GFBound with the per-atom and per-atom-pair summands of the bound exposed.

    `theta` and `self_sum` below are P3's bodies (gfbound.GFBound.theta / self_sum, read at the commit of this
    workstream) with ONE addition: before the matrix `coef * tot` (resp. the vector of self summands) is summed, it
    is added to the accumulators self.acc_cross[(p, q)] / self.acc_self[p] (kcal/mol, factor RND as in P3's
    `total`).  The returned floats are the same expressions as P3's; `check_against_base` compares both."""
    acc_cross = None
    acc_self = None

    def start(self):
        N = self.G.nat
        self.acc_cross = np.zeros((N, N)); self.acc_self = np.zeros(N)

    def stop(self):
        """returns (self vector (N,), symmetric pair matrix with zero diagonal: entry [p, q] = bound of the unordered pair)."""
        c = self.acc_cross; s = self.acc_self
        self.acc_cross = None; self.acc_self = None
        sym = c + c.T
        return s, sym

    def theta(self, o1, t1, o2, t2, s, subset=None):
        if s < 1:
            raise ValueError("order of the free set must be >= 1")
        if t1 not in o1.merged or t2 not in o2.merged:
            return 0.0
        m1, m2 = o1.merged[t1], o2.merged[t2]
        d1, d2 = m1["d"].copy(), m2["d"].copy()
        if self._excl is not None:
            d1[self._excl] = 0.0; d2[self._excl] = 0.0
        for h in (o1.host, o2.host):
            if h is not None:
                d1[h] = 0.0; d2[h] = 0.0
        sH = self.supH(o1, t1, o2, t2)
        if sH is None:
            return 0.0
        coef = self._coef(o1, o2)
        if subset is not None:
            B = tuple(subset)
            assert len(B) == s
            tot = np.zeros(coef.shape)
            for part in set_partitions(B):
                term = sH[len(part)].copy()
                for block in part:
                    k = len(block)
                    term = term * ((m1["supL"][k] * np.prod(d1[list(block)], axis=0))[:, None]
                                   + (m2["supL"][k] * np.prod(d2[list(block)], axis=0))[None, :])
                tot += term
        else:
            e = esym2(d1, d2, s)
            B1 = bell_arrays(m1["supL"], s); B2 = bell_arrays(m2["supL"], s)
            tot = np.zeros(coef.shape)
            for a in range(s + 1):
                b = s - a
                M = np.zeros(coef.shape)
                for r1 in range(0, a + 1):
                    if a > 0 and r1 == 0:
                        continue
                    for r2 in range(0, b + 1):
                        if b > 0 and r2 == 0:
                            continue
                        M += sH[r1 + r2] * B1[a][r1][:, None] * B2[b][r2][None, :]
                tot += e[a][b] * M
        mat = coef * tot
        if self.acc_cross is not None:
            self.acc_cross[np.ix_(o1.atoms, o2.atoms)] += mat / KCAL * RND
        return float(mat.sum())

    def self_sum(self, o, t, s, subset=None):
        if s < 1:
            raise ValueError
        if t not in o.merged:
            return 0.0
        m = o.merged[t]
        dd = m["d"]
        if self._excl is not None:
            dd = dd.copy(); dd[self._excl] = 0.0
        if subset is not None:
            prod = np.prod(dd[list(subset)], axis=0)
        else:
            prod = esym1(dd, s)[s]
        vec = 0.5 * KAPPA * (o.q ** 2 * m["supB"][s] * prod)
        if self.acc_self is not None:
            self.acc_self[o.atoms] += vec / KCAL * RND
        return float(vec.sum())

    def decomp(self, m, T=None):
        """(self part, cross part) as P3's total(m, T), plus (self vector, symmetric pair matrix) of the summands."""
        self.start()
        se, cr = self.total(m, T)
        sv, pm = self.stop()
        return se, cr, sv, pm


def check_against_base(G, x0, sup, K, orders, Tlist=None):
    """max relative deviation between GFDecomp (my copy of theta / self_sum) and P3's GFBound, for the closed-form sums
    of the given orders and for the subsets of Tlist; and between the summed decomposition and the returned totals."""
    GF0 = GFBound(G, x0, sup, K=K); GF1 = GFDecomp(G, x0, sup, K=K)
    worst = 0.0; worst_sum = 0.0; n = 0
    cases = [(m, None) for m in orders] + [(len(T), list(T)) for T in (Tlist or [])]
    for m, T in cases:
        a = GF0.total(m, T)
        se, cr, sv, pm = GF1.decomp(m, T)
        for u, v in zip(a, (se, cr)):
            worst = max(worst, abs(u - v) / max(abs(u), 1e-300)); n += 1
        worst_sum = max(worst_sum, abs(sv.sum() - se) / max(se, 1e-300), abs(np.triu(pm, 1).sum() - cr) / max(cr, 1e-300))
    return worst, worst_sum, n


def ball_size(ks, r):
    e = [1] + [0] * r
    for kk in ks:
        for j in range(r, 0, -1):
            e[j] += e[j - 1] * (kk - 1)
    return sum(e)
