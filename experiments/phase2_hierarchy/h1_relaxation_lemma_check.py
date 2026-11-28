"""
Phase II (adaptive hierarchy) -- exact finite-n check of the relaxation lemma (Lemma B of
docs/phase2_hierarchy/HIERARCHY_REPORT.md) on its extremal functions.

Blocks 1..m with a role in {P, Q, T}.  Relative costs t_j(d) = ln P_j(mode) - ln P_j(d) (exact binomials).
For a budget Theta the extremal function is the pointwise deepest admissible F (largest U = -F) with
   (H1)  on V_0 = { t(d) <= Theta }:             U depends on d_P only, and nu(d) = U(d) - t(d) <= 0 there;
   (H2)  on V_P = { t_Q(d) + t_T(d) <= Theta }:  U depends on (d_P, d_Q) only;
no other constraint.  Because it is the pointwise largest such U, a bound that holds for it holds for
every F satisfying (H1), (H2) with nu_0 = max_{V_0} nu  (nu_0 = 0 here).

Lemma B:   nu(y) <= nu_0 + n phi_P h - min{ t_T(y), Theta - n (1 - phi_P) h } + m (u + 5 ln(n+1))   for all y.
Reported:  viol = max_y [ nu(y) - n phi_P h + min{...} ]  (to be compared with 0 and with the allowance
           m (u + 5 ln(n+1))),  and  hid = max over { t_T(y) > Theta } of nu(y)  against  n h - Theta.

Notes added after two independent replications (ENG-RES-0020 of the engineering division; the review
HIERARCHY_REVIEW.md), both with their own code:
 * (H1), (H2) are imposed here as plain independence of the other coordinates.  The report states them up to
   parities, which is weaker; under the report's hypotheses the values are higher by up to 0.16 nats.
 * All cases below use Theta = (theta/h) n h with theta/h <= 1.3, which is BELOW the lemma's own hypothesis
   Theta >= n h + 2 m ln(n+1) at these sizes, and some blocks are smaller than N_u.  The script therefore
   tests a statement somewhat stronger than the lemma, at small sizes; at n <= 400 the allowance does not
   separate valid from invalid profiles.
 * The extremal function is built by a fixed sequence of passes, not iterated to a fixed point; on these
   124 cases it equals the exact maximum to print rounding (both replications).
 * "hid <= n h - Theta + 0.002 for theta >= 1.1 h" is a property of these 124 cases only (other splits: up to
   +0.62 nats).
"""
import sys, itertools
import numpy as np
from scipy.special import gammaln
LN2 = np.log(2.0)
def f(r):
    r = np.clip(r, 1e-300, 1 - 1e-16); return LN2 + r * np.log(r) + (1 - r) * np.log1p(-r)
def consts(u):
    pu = 1 / (1 + np.exp(u)); L1 = np.log(2 / (1 + np.exp(-u))); return pu, L1, f(pu), f(L1 / u)
def relcost(n):
    k = np.arange(n + 1); lb = gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    return lb.max() - lb
def lip_pass(U, u):
    for ax in range(U.ndim):
        U = np.moveaxis(U, ax, 0)
        if U.ndim == 1:
            for i in range(1, len(U)): U[i] = min(U[i], U[i - 1] + u)
            for i in range(len(U) - 2, -1, -1): U[i] = min(U[i], U[i + 1] + u)
        else:
            for i in range(1, U.shape[0]): np.minimum(U[i], U[i - 1] + u, out=U[i])
            for i in range(U.shape[0] - 2, -1, -1): np.minimum(U[i], U[i + 1] + u, out=U[i])
        U = np.moveaxis(U, 0, ax)
    return U
def bcast(vec, j, m):
    sh = [1] * m; sh[j] = len(vec); return vec.reshape(sh)

def extremal(u, ns, roles, Theta):
    m = len(ns); t = [relcost(nj) for nj in ns]
    shape = tuple(nj + 1 for nj in ns)
    P = [j for j in range(m) if roles[j] == 'P']; Q = [j for j in range(m) if roles[j] == 'Q']; T = [j for j in range(m) if roles[j] == 'T']
    def tsum(blocks):
        out = np.zeros(shape)
        for j in blocks: out = out + bcast(t[j], j, m)
        return out
    tP, tQ, tT = tsum(P), tsum(Q), tsum(T)
    INF = 1e18
    # the largest admissible function of d_P alone with U <= t_P (flat histogram of the P-blocks)
    cap = lip_pass(tP.copy(), u)
    # (H1): on V0, U = G1(d_P) <= t_P;  G1 defined where (d_P, modes) is in V0, i.e. t_P <= Theta
    U = np.where((tP + tQ + tT) <= Theta, cap, INF)
    # deepest extension within functions of (d_P, d_Q): anchors are the points of V0 with typical T-part
    U = np.where(tT == 0, U, INF)                       # work on the slice of typical T-types
    U = lip_pass(U, u)                                  # (moves in the T-direction are harmless: all slices equal below)
    UPQ = np.min(np.where(tT == 0, U, INF), axis=tuple(T), keepdims=True) if T else U
    UPQ = np.broadcast_to(UPQ, shape).copy()
    # (H1) again: on V0 the value must be the function of d_P alone
    UPQ = np.where((tP + tQ) <= Theta, np.minimum(UPQ, cap), UPQ)
    UPQ = lip_pass(np.where(tT == 0, UPQ, INF), u)
    UPQ = np.broadcast_to(np.min(np.where(tT == 0, UPQ, INF), axis=tuple(T), keepdims=True), shape).copy() if T else UPQ
    # (H2): on V_P the function equals UPQ(d_P, d_Q); beyond, deepest admissible extension
    U = np.where((tQ + tT) <= Theta, UPQ, INF)
    U = lip_pass(U, u)
    return U, (tP, tQ, tT)

def check(u, ns, roles, theta_over_h, verbose=True):
    pu, L1, a, h = consts(u); n = sum(ns); m = len(ns)
    Theta = theta_over_h * n * h
    U, (tP, tQ, tT) = extremal(u, ns, roles, Theta)
    nu = U - (tP + tQ + tT)
    V0 = (tP + tQ + tT) <= Theta
    nu0 = nu[V0].max()
    # hypotheses actually hold for the constructed function?
    T = [j for j in range(m) if roles[j] == 'T']; Q = [j for j in range(m) if roles[j] == 'Q']
    def const_along(arr, mask, axes):
        if not axes: return True
        lo = np.min(np.where(mask, arr, np.inf), axis=tuple(axes), keepdims=True)
        hi = np.max(np.where(mask, arr, -np.inf), axis=tuple(axes), keepdims=True)
        return bool(np.all((hi - lo <= 1e-9) | ~np.isfinite(hi - lo)))
    h1 = const_along(U, V0, Q + T); h2 = const_along(U, (tQ + tT) <= Theta, T)
    step = max(np.abs(np.diff(U, axis=ax)).max() for ax in range(m))
    phiP = sum(nj for nj, r in zip(ns, roles) if r == 'P') / n
    rhs = n * phiP * h - np.minimum(tT, Theta - n * (1 - phiP) * h)
    viol = float((nu - nu0 - rhs).max())
    hidden = tT > Theta
    hid = float((nu - nu0)[hidden].max()) if hidden.any() else float('-inf')
    allow = m * (u + 5 * np.log(n + 1))
    if verbose:
        print("u=%.1f ns=%s roles=%s theta/h=%.2f | H1 %s H2 %s step<=u %s | viol=%+8.3f (allowance %.1f) | hidden max=%+8.3f vs n h - Theta=%+8.3f" % (
            u, ns, ''.join(roles), theta_over_h, h1, h2, step <= u + 1e-9, viol, allow, hid, n * h - Theta))
        sys.stdout.flush()
    return viol, allow, hid, n * h - Theta, (h1 and h2 and step <= u + 1e-9)

if __name__ == "__main__":
    worst = -1e9; okall = True
    cases3 = [((36, 162, 162), 'PQT'), ((72, 144, 144), 'PQT'), ((144, 108, 108), 'PQT'), ((216, 36, 108), 'PQT'),
              ((108, 18, 234), 'PQT'), ((120, 120, 120), 'PTT'), ((120, 120, 120), 'PPT'), ((120, 120, 120), 'QQT'), ((120, 120, 120), 'QTT')]
    for u in (0.5, 1.0, 2.0, 4.0):
        for ns, roles in cases3:
            for th in (1.0, 1.1, 1.3):
                v, al, hid, ref, ok = check(u, ns, list(roles), th)
                worst = max(worst, v); okall &= ok
    cases4 = [((40, 40, 60, 60), 'PPQT'), ((30, 50, 50, 70), 'PQTT'), ((50, 50, 50, 50), 'PQQT'), ((40, 60, 40, 60), 'PTQT')]
    for u in (1.0, 2.0):
        for ns, roles in cases4:
            for th in (1.0, 1.2):
                v, al, hid, ref, ok = check(u, ns, list(roles), th)
                worst = max(worst, v); okall &= ok
    print("worst value of viol over all cases: %+.3f nats;  all constructed functions admissible and satisfying (H1),(H2): %s" % (worst, okall))
