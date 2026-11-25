"""R7 OWN covering numbers N^P_cov of the profile envelope on the generic chain.

Written from theory definitions only (THEORY_REPORT Thm 11.4; P_REPORT sections 0, 3.3),
BEFORE reading engineering code.

Instance: f = #gauche (e = 1), residual g = 0, envelope d_P(x,y) = L * ||N^x - N^y||_1.
Slack s(a,y) = d_P(a,y) (zero residual).  gap(y) = f(y) - min f.
N_cov(eps) = least number of centres such that every conformation y has a centre a with
             d_P(a,y) <= gap(y) + eps.
Conformations with equal profiles are at distance 0, so the problem lives on profile
classes with radius r(C) = min_{y in C} gap(y) + eps.

Exactness: the set-cover ILP is solved by HiGHS (scipy.optimize.milp).  The returned 0/1
vector is re-checked for feasibility against the boolean cover matrix (no tolerance); the
lower bound is HiGHS' branch-and-bound dual bound, plus an independent LP-duality bound
ceil(sum of a rational-rounded dual solution) which is checked WITHOUT solver tolerances
(see `certified_lp_lower_bound`).
"""
import math
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
from scipy.sparse import csr_matrix, csc_matrix

import own_gen as og


def class_data(n, sc=og.SC, tol_tie=1e-9):
    words = og.enumerate_words(n)
    S = og.truncated_sorted_sq(words, sc=sc)
    cid, ncls, info = og.profile_classes(S, sc=sc, tol_tie=tol_tie)
    gauche = (words != 0).sum(axis=1)
    # representative (first member) and minimal gap of each class
    order = np.argsort(cid, kind="stable")
    first = np.zeros(ncls, dtype=np.int64)
    first[cid[order][::-1]] = order[::-1]
    mingap = np.full(ncls, 10 ** 9, dtype=np.int64)
    np.minimum.at(mingap, cid, gauche)
    mingap -= gauche.min()
    size = np.bincount(cid, minlength=ncls)
    return dict(words=words, S=S, cid=cid, ncls=ncls, info=info, rep=first,
                mingap=mingap, size=size, Srep=S[first])


def dist_matrix(Srep, block=256):
    """D[a,y] = || N^a - N^y ||_1 = sum_k |sorted_a[k] - sorted_y[k]|."""
    C = len(Srep)
    D = np.empty((C, C))
    for lo in range(0, C, block):
        D[lo:lo + block] = np.abs(Srep[lo:lo + block, None, :] - Srep[None, :, :]).sum(axis=2)
    return D


def cover_matrix(D, mingap, L, eps, tol=1e-9, info=None):
    """cov[a,y] = True iff centre class a covers class y: L*D[a,y] <= mingap[y] + eps."""
    lhs = L * D
    rhs = (mingap + eps)[None, :]
    cov = lhs <= rhs + tol
    if info is not None:
        off = np.abs(lhs - rhs)
        np.fill_diagonal(off, np.inf)
        info["min_margin"] = float(off.min())
    return cov


def greedy_cover(cov):
    C = cov.shape[0]
    uncovered = np.ones(C, dtype=bool)
    chosen = []
    while uncovered.any():
        gain = cov[:, uncovered].sum(axis=1)
        a = int(gain.argmax())
        chosen.append(a)
        uncovered &= ~cov[a]
    return chosen


def reduce_instance(cov):
    """Standard exact reductions: forced centres (a point covered by one centre only)."""
    C = cov.shape[0]
    ncov = cov.sum(axis=0)          # number of centres covering y
    forced = np.unique(np.nonzero(cov[:, ncov == 1])[0])
    return forced


def exact_cover(cov, time_limit=600.0, verbose=False):
    """Exact minimum set cover by MILP.  Returns dict(primal, dual_bound, status, chosen)."""
    C = cov.shape[0]
    # constraints: for every y: sum_a cov[a,y] x_a >= 1
    A = csr_matrix(cov.T.astype(np.float64))
    res = milp(c=np.ones(C), constraints=LinearConstraint(A, lb=np.ones(C), ub=np.inf),
               integrality=np.ones(C), bounds=Bounds(0, 1),
               options=dict(time_limit=time_limit, disp=verbose, mip_rel_gap=0.0))
    out = dict(status=int(res.status), message=str(res.message))
    if res.x is not None:
        x = np.round(res.x).astype(int)
        assert np.abs(res.x - x).max() < 1e-6
        chosen = np.nonzero(x)[0]
        feas = cov[chosen].any(axis=0).all()
        out.update(primal=int(x.sum()), chosen=chosen, primal_feasible_checked=bool(feas))
    db = getattr(res, "mip_dual_bound", None)
    out["dual_bound"] = None if db is None else float(db)
    return out


def lp_fractional(cov):
    """Fractional covering number (LP) and a dual solution (weights on points)."""
    C = cov.shape[0]
    # dual: max sum w_y  s.t. for every centre a: sum_{y covered by a} w_y <= 1, w >= 0
    A = csr_matrix(cov.astype(np.float64))
    res = linprog(c=-np.ones(C), A_ub=A, b_ub=np.ones(C), bounds=(0, None), method="highs")
    return -res.fun, res.x


def certified_lp_lower_bound(cov, w, den=10 ** 6):
    """Tolerance-free lower bound from an approximate dual solution w.

    Round w down to multiples of 1/den, clip at 0, then rescale by the exact maximal
    centre load so that every centre constraint holds EXACTLY (integer arithmetic).
    Returns a Fraction lower bound on the (fractional, hence integral) covering number.
    """
    wi = np.floor(np.maximum(w, 0.0) * den).astype(np.int64)
    load = cov.astype(np.int64) @ wi          # exact integers
    mx = int(load.max())
    tot = int(wi.sum())
    if mx == 0:
        return Fraction(0)
    # w' = wi / mx is feasible exactly: every load <= 1
    return Fraction(tot, mx)


def run(n, L, eps, time_limit=600.0, verbose=False, cd=None, D=None):
    cd = cd or class_data(n)
    if D is None:
        D = dist_matrix(cd["Srep"])
    info = {}
    cov = cover_matrix(D, cd["mingap"], L, eps, info=info)
    g = greedy_cover(cov)
    lpval, w = lp_fractional(cov)
    lb = certified_lp_lower_bound(cov, w)
    ex = exact_cover(cov, time_limit=time_limit, verbose=verbose)
    return dict(n=n, L=L, eps=eps, classes=cd["ncls"], greedy=len(g), lp=lpval,
                lp_certified_lb=float(lb), lp_certified_ceil=math.ceil(lb),
                min_margin=info["min_margin"], **{k: v for k, v in ex.items() if k != "chosen"})


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    for n in range(5, nmax + 1):
        cd = class_data(n)
        D = dist_matrix(cd["Srep"])
        N = n + 3
        for (L, eps) in [(1.0, 0.0), (1.0, N / 2.0), (0.2, 0.0)]:
            t0 = time.time()
            r = run(n, L, eps, time_limit=tl, cd=cd, D=D)
            print(f"n={n} L={L} eps={eps}: classes={r['classes']} greedy={r['greedy']} LP={r['lp']:.6f} "
                  f"certLB={r['lp_certified_ceil']} MILP primal={r.get('primal')} dual={r['dual_bound']} "
                  f"feas={r.get('primal_feasible_checked')} margin={r['min_margin']:.3e} status={r['status']} "
                  f"t={time.time()-t0:.1f}s", flush=True)
