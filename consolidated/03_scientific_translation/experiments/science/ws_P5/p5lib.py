"""
Workstream P5 -- shared library.

Reads (never writes) workstream P3's and P2's modules: p3core.GBModel (evaluator, descreening
tables), encl.EnvelopeSup (interval enclosures; its cache directory is redirected to
ws_P5/cache so that nothing is written into ws_P3), gfbound.GFBound (P3's term-by-term bound).

The object.  For a fixed-backbone rotamer model G (P3's GBModel) with atoms p = 1..N, charges
q_p, and for every assignment x of the product domain X the symmetric KERNEL MATRIX

    M_pq(x) = h(ell_p(x) + ell_q(x); r_pq(x)) = 1/f_GB(r_pq, B_p B_q)   (p != q),
    M_pp(x) = 1/B_p(x),

the GBn2 polarisation energy is the quadratic form (kcal/mol)

    g(x) = sum_{p,q} W_pq(x),     W_pq(x) := -(KAPPA/2) q_p q_q M_pq(x) / KCAL

(ordered pairs, diagonal included: the diagonal is the self part, the off-diagonal the cross
part).  M does NOT depend on the charges.

Anchored constants.  For an anchor x0 and a set T of sites, and any array F over the states,
    c_T^anch(F) = sup { |Delta_T F(z; x0_T -> y_T)| : z in X, y_T in X_T }
(mixed difference between the anchor states and arbitrary states of the sites of T, in every
context z of the other sites).
"""
import sys, os, itertools, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
P3DIR = os.path.normpath(os.path.join(HERE, "..", "ws_P3"))
if P3DIR not in sys.path:
    sys.path.insert(0, P3DIR)
import numpy as np
import p3core
from p3core import GBModel, KAPPA, KCAL, KT300
import encl
encl.CACHE = os.path.join(HERE, "cache")          # never write into ws_P3
from encl import EnvelopeSup
from gfbound import GFBound


class Tee:
    """print to stdout and to a log file; the log is closed by .done(), which writes the last line."""
    def __init__(self, path):
        self.f = open(path, "w")
        self.t0 = time.time()

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n"); self.f.flush()

    def done(self):
        self(f"DONE in {time.time() - self.t0:.1f} s")
        self.f.close()


def build(seq, bb, tau):
    """model, all states, shape, known part f, total g (P3's evaluator), anchor = argmin E by enumeration."""
    G = GBModel(seq, bb, tau=tau)
    n = G.ns
    shape = tuple(G.k)
    st = G.product_states()
    g = G.energy(st)
    c0, h, J = G.fb.site_tables("ff14SB")
    f = np.full(shape, c0)
    for i in range(n):
        sh = [1] * n; sh[i] = shape[i]
        f = f + h[i][G.dom[i]].reshape(sh)
    for (i, j), tab in J.items():
        sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
        f = f + tab[np.ix_(G.dom[i], G.dom[j])].reshape(sh)
    E = f + g.reshape(shape)
    x0 = tuple(int(v) for v in np.unravel_index(np.argmin(E), shape))
    return G, st, shape, f, g.reshape(shape), E, x0


def kernel_rows(G, st, rows, B=None, X=None):
    """M[x, p, q] for p in rows, all q: (S, len(rows), N).  nm^-1."""
    if B is None:
        B = 1.0 / G.invB(G.descreening(st))
    if X is None:
        X = G.coords(st)
    d = X[:, rows][:, :, None, :] - X[:, None, :, :]
    r2 = (d * d).sum(-1)
    BB = B[:, rows][:, :, None] * B[:, None, :]
    return 1.0 / np.sqrt(r2 + BB * np.exp(-r2 / (4.0 * BB)))


def weights(G, M, rows, q=None):
    """W[x, p, q] = -(KAPPA/2) q_p q_q M_pq / KCAL (kcal/mol) for the row block."""
    q = G.q if q is None else q
    return (-0.5 * KAPPA / KCAL) * q[rows][None, :, None] * q[None, None, :] * M


# ----------------------------------------------------------------------------- groupings
def groupings(G):
    """dict name -> integer array (N,) of group labels.
    'residue'  : ACE, each residue, NME (every group has total charge 0 for neutral residues);
    'rigid'    : per residue its fixed (backbone + CB) atoms and its moving side-chain atoms; caps whole
                 (rigid bodies on the rotamer grid; not neutral individually);
    'peptide'  : planar peptide units {C, O of residue i, N, H of residue i+1}, {CA, HA, CB, ...fixed rest},
                 moving side chain, cap methyls;
    'united'   : every heavy atom with its hydrogens, carbonyl C and O merged."""
    P = G.P
    names = list(P.names); resid = np.asarray(P.resid); N = G.nat
    site = np.asarray(P.site_of_atom)
    out = {}
    out["residue"] = resid.copy()
    rig = np.zeros(N, dtype=int)
    lab = {}
    for p in range(N):
        key = (int(resid[p]), int(site[p] != 0))
        rig[p] = lab.setdefault(key, len(lab))
    out["rigid"] = rig
    pep = np.zeros(N, dtype=int); lab = {}
    for p in range(N):
        r = int(resid[p]); nm = names[p]
        if site[p] != 0:
            key = ("sc", r)
        elif nm in ("C", "O"):
            key = ("pep", r)
        elif nm in ("N", "H"):
            key = ("pep", r - 1)
        else:
            key = ("rest", r)
        pep[p] = lab.setdefault(key, len(lab))
    out["peptide"] = pep
    # united atoms from the topology bonds
    bonds = [(b[0].index, b[1].index) for b in P.top.bonds()]
    el = [str(e) for e in P.elements]
    parent = np.arange(N)
    for a, b in bonds:
        if el[a] == "H" and el[b] != "H":
            parent[a] = b
        elif el[b] == "H" and el[a] != "H":
            parent[b] = a
    for a, b in bonds:                       # carbonyl: merge O into its C
        na, nb = names[a], names[b]
        if na == "C" and nb == "O":
            parent[b] = a
        elif nb == "C" and na == "O":
            parent[a] = b
    for p in range(N):
        parent[p] = parent[parent[p]]
    _, uni = np.unique(parent, return_inverse=True)
    out["united"] = uni
    return out


def group_charges(G, lab):
    return np.array([G.q[lab == a].sum() for a in range(lab.max() + 1)])


# ----------------------------------------------------------------------------- anchored constants
def anch_diff(D, x0i, axis):
    """difference to the anchor state along `axis`.  Two states: the (zero) anchor slice is removed (the array
    halves); more states: the zero slice is kept (no copy for the removal; it does not change any maximum)."""
    ref = np.take(D, [x0i], axis=axis)
    if D.shape[axis] == 2:
        return np.take(D, [1 - x0i], axis=axis) - ref
    return D - ref


def anch_walk(F, x0, n, maxorder, callback, minorder=3):
    """Depth-first walk over all subsets T (|T| <= maxorder) of the n site axes (the first n axes of F);
    for every T with |T| >= minorder calls callback(T, D_T), D_T = anchored mixed difference array of shape
    (reduced state axes..., extra axes...).  Sites with a single state give empty arrays (constant zero)."""
    def rec(D, last, T):
        for i in range(last + 1, n):
            if F.shape[i] < 2:
                continue
            D2 = anch_diff(D, x0[i], i)
            T2 = T + (i,)
            if len(T2) >= minorder:
                callback(T2, D2)
            if len(T2) < maxorder:
                rec(D2, i, T2)
    rec(F, -1, ())


def anch_consts(F, x0, n, maxorder, minorder=3):
    """dict T -> array over the extra axes of sup over states of |D_T| (c_T^anch of every extra component)."""
    out = {}

    def cb(T, D):
        A = D.reshape((-1,) + D.shape[n:])
        out[T] = np.maximum(A.max(axis=0), -A.min(axis=0)) if A.shape[0] else np.zeros(D.shape[n:])
    anch_walk(F, x0, n, maxorder, cb, minorder)
    return out


def subsets(n, shape, lo, hi):
    return [T for m in range(lo, hi + 1) for T in itertools.combinations(range(n), m) if all(shape[i] >= 2 for i in T)]


def anchored_interp(g, x0, order):
    """anchored expansion of g at x0 truncated at `order` (sum of d_T, |T| <= order), by inclusion-exclusion."""
    n = g.ndim
    out = np.zeros(g.shape)
    for m in range(order + 1):
        for T in itertools.combinations(range(n), m):
            idx = list(x0)
            for i in T:
                idx[i] = slice(None)
            sub = g[tuple(idx)]
            dd = sub.copy()
            for a, i in enumerate(sorted(T)):
                dd = dd - np.take(dd, [x0[i]], axis=a)
            sh = [1] * n
            for a, i in enumerate(sorted(T)):
                sh[i] = g.shape[i]
            out = out + dd.reshape(sh)
    return out
