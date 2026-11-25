"""R7 OWN enumerator of the generic ("gen") off-lattice chain.

Written from the MODEL DEFINITION ONLY (theory division, docs/workstreams/P_REPORT.md
sections 0, 2.1, 3.3) BEFORE reading any engineering code or engineering report on X-004.

Model "gen" (P_REPORT section 0):
  * beads 0..N-1, N = n+3, n torsions with states t, g+, g- (180, +60, -60 degrees);
  * bond length b = 1, bond angle theta = 111 degrees;
  * hard core: squared distance s_pq >= 3.0 for q-p >= 3;
  * pairs P = {(p,q): q-p >= 3}; cutoff S_c = 16; truncated s~ = min(s, S_c);
  * profile N^x(s) = #{pairs: s_pq(x) <= s}, 0 <= s < S_c  <=> sorted multiset of s~;
  * d_P(x,y) = L * || N^x - N^y ||_1 = L * sum |sort(s~^x) - sort(s~^y)|   (Prop. 2);
  * known part f = #gauche (e = 1); residual zero.

My own conventions (decided here, to be compared with engineering's afterwards):
  * coordinates by the standard internal->Cartesian recursion (float64);
  * the hard-core test is `s >= HC - tol_hc` with tol_hc = 1e-9; the smallest |s - HC|
    met is recorded so that the role of the tolerance can be judged;
  * profile classes are formed from GLOBAL clusters of the occurring truncated squared
    distances (two values are identified iff they lie in a chain of gaps < tol_tie); the
    spectrum of gaps between consecutive distinct values is recorded, so "tie or not" can
    be read off the data instead of being assumed.
"""
import math
import sys
import time

import numpy as np

THETA = math.radians(111.0)
PHIS = np.array([math.pi, math.pi / 3.0, -math.pi / 3.0])  # state 0 = t, 1 = g+, 2 = g-
HC = 3.0
SC = 16.0


def coords_from_words(words, theta=THETA, phis=PHIS):
    """words: (M, n) uint8 torsion states. Returns (M, n+3, 3) float64 coordinates."""
    words = np.asarray(words)
    M, n = words.shape
    N = n + 3
    X = np.zeros((M, N, 3))
    ct, st = math.cos(theta), math.sin(theta)
    X[:, 1, 0] = 1.0
    # bead 2: interior angle theta at bead 1
    X[:, 2, 0] = 1.0 - ct
    X[:, 2, 1] = st
    for i in range(3, N):
        a, b, c = X[:, i - 3], X[:, i - 2], X[:, i - 1]
        bc = c - b
        bc /= np.linalg.norm(bc, axis=1, keepdims=True)
        nrm = np.cross(b - a, bc)
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
        m = np.cross(nrm, bc)
        phi = phis[words[:, i - 3]]
        d = (-ct) * bc + (st * np.cos(phi))[:, None] * m + (st * np.sin(phi))[:, None] * nrm
        X[:, i] = c + d
    return X


def enumerate_words(n, hard_core=HC, tol_hc=1e-9, chunk=60000, record=None):
    """All torsion words of length n whose chain satisfies s_pq >= hard_core (q-p>=3).

    Level-by-level growth with prefix pruning (a violated pair stays violated).
    Returns (words (M,n) uint8).  If record is a dict, stores the smallest margin
    min |s - hard_core| seen over all tested pairs (accepted or rejected).
    """
    words = np.zeros((1, 0), dtype=np.uint8)
    min_margin = math.inf
    for level in range(1, n + 1):
        out = []
        for lo in range(0, len(words), chunk):
            w = words[lo:lo + chunk]
            ext = np.repeat(w, 3, axis=0)
            last = np.tile(np.arange(3, dtype=np.uint8), len(w))[:, None]
            ext = np.concatenate([ext, last], axis=1)
            X = coords_from_words(ext)
            newb = X[:, -1]                      # bead index level+2
            old = X[:, :level + 2 - 2]           # beads 0 .. (level+2)-3
            s = ((old - newb[:, None, :]) ** 2).sum(axis=2)
            if hard_core is None:
                ok = np.ones(len(ext), dtype=bool)
            else:
                ok = (s >= hard_core - tol_hc).all(axis=1)
                mm = np.abs(s - hard_core).min()
                if mm < min_margin:
                    min_margin = mm
            out.append(ext[ok])
        words = np.concatenate(out, axis=0)
    if record is not None:
        record["min_margin_to_hard_core"] = float(min_margin)
    return words


def pair_index(N):
    p, q = np.triu_indices(N, k=3)
    return p, q


def truncated_sorted_sq(words, sc=SC, chunk=20000):
    """(M, P) array: sorted truncated squared distances min(s, sc) over pairs q-p>=3."""
    M, n = words.shape
    N = n + 3
    p, q = pair_index(N)
    out = np.empty((M, len(p)))
    for lo in range(0, M, chunk):
        X = coords_from_words(words[lo:lo + chunk])
        s = ((X[:, p, :] - X[:, q, :]) ** 2).sum(axis=2)
        np.minimum(s, sc, out=s)
        s.sort(axis=1)
        out[lo:lo + chunk] = s
    return out


def cluster_values(vals, tol_tie=1e-9):
    """Global clustering of a 1-d array of values: chains of gaps < tol_tie are one cluster.

    Returns (sorted distinct representatives, gaps between consecutive sorted unique raw
    values) so that the gap spectrum can be inspected.
    """
    u = np.unique(vals)
    gaps = np.diff(u)
    brk = np.concatenate([[True], gaps >= tol_tie])
    reps = u[brk]
    return reps, gaps, u


def profile_classes(S, sc=SC, tol_tie=1e-9):
    """Classes of equal profile.  S: (M,P) sorted truncated squared distances.

    Returns (class_id per conformation, number of classes, info dict).
    """
    reps, gaps, u = cluster_values(S.ravel(), tol_tie)
    # cluster id of each value: index of the last representative <= value (+tol)
    ids = np.searchsorted(reps, S + tol_tie / 2, side="right") - 1
    # S rows are sorted, ids rows are then sorted as well (monotone map)
    _, inv = np.unique(ids, axis=0, return_inverse=True)
    inv = np.asarray(inv).ravel()
    info = {
        "n_raw_unique": int(len(u)),
        "n_clusters": int(len(reps)),
        "max_gap_inside_clusters": float(gaps[gaps < tol_tie].max()) if (gaps < tol_tie).any() else 0.0,
        "min_gap_between_clusters": float(gaps[gaps >= tol_tie].min()) if (gaps >= tol_tie).any() else math.inf,
    }
    return inv, int(inv.max()) + 1, info


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    # sanity: 1-4 squared distances
    w = np.array([[0], [1], [2]], dtype=np.uint8)
    X = coords_from_words(w)
    print("1-4 squared distances t,g+,g-:", ((X[:, 0] - X[:, 3]) ** 2).sum(axis=1))
    print("1-3 squared distance:", ((X[0, 0] - X[0, 2]) ** 2).sum())
    wgg = np.array([[1, 2], [1, 1], [0, 0]], dtype=np.uint8)
    X = coords_from_words(wgg)
    print("1-5 squared distances g+g-, g+g+, tt:", ((X[:, 0] - X[:, 4]) ** 2).sum(axis=1))
    for n in range(1, nmax + 1):
        t0 = time.time()
        rec = {}
        words = enumerate_words(n, record=rec)
        S = truncated_sorted_sq(words)
        cid, ncls, info = profile_classes(S)
        print(f"n={n:2d} N={n+3:2d} conf={len(words):8d} classes={ncls:7d} "
              f"hc_margin={rec['min_margin_to_hard_core']:.3e} "
              f"clusters={info['n_clusters']} raw_unique={info['n_raw_unique']} "
              f"max_in={info['max_gap_inside_clusters']:.2e} min_between={info['min_gap_between_clusters']:.3e} "
              f"t={time.time()-t0:.1f}s", flush=True)
