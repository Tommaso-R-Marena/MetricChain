#!/usr/bin/env python3
"""R4 (SCI-REV-0003) -- the twins of Theorem 11.86, built from the STATEMENT in
THEORY_REPORT.md section 11.24 ("The twins."), exact binomial arithmetic in log space.

Own implementation; none of the authors' code was read before this file was written.

Conventions (sections 11.16-11.19):  w = e^{-psi},  A(F) = sum_d P1(d1) P2(d2) e^{-F(d1,d2)},
P_j = Bin(n_j, 1/2),  c_j = -ln P_j,  budget T = n*theta.
  W1 = {c1(d1)+c2(d2) <= T}            (what a blind batch of e^T points sees)
  W2 = {d2 : c2(d2) <= T},  V2 = {(d1,d2) : d2 in W2}
  g_j = -(largest u-Lipschitz minorant of  ln P_j(mode) - ln P_j)
  F_deep = lower McShane envelope of g1(d1) from W1 (metric u*(|dd1|+|dd2|))
  F_cap  = max(F_deep, g1+g2)
  F_D, F_S = F_cap on V2, continued outside V2 in d2 at slope -u / +u.

Everything asserted in the theorem about the pair is CHECKED here, not assumed:
  (L)  both are u-Lipschitz in each argument;
  (C1) F_D = F_S = g1(d1) on W1;      (C2) F_D = F_S on V2;     (C3) W1 subset V2;
  (S)  A(F_S) <= (n1+1)(n2+1);
  (P)  p1 = P((D1,D2) not in W1) <= (n1+1)(n2+1) e^{-T},  p2 = P(D2 not in W2) <= (n2+1) e^{-T};
and the gap ln A(F_D) - ln A(F_S) is returned.
"""
import math
import sys
import numpy as np
from scipy.special import gammaln, logsumexp

NEG = -np.inf


def ln_binom_pmf(n):
    d = np.arange(n + 1, dtype=float)
    return gammaln(n + 1) - gammaln(d + 1) - gammaln(n - d + 1) - n * math.log(2.0)


def lip_minorant(t, u):
    """Largest u-Lipschitz minorant of the 1-d array t: m(d) = min_e t(e) + u|d-e|."""
    m = t.copy()
    for d in range(1, len(m)):
        if m[d] > m[d - 1] + u:
            m[d] = m[d - 1] + u
    for d in range(len(m) - 2, -1, -1):
        if m[d] > m[d + 1] + u:
            m[d] = m[d + 1] + u
    return m


def upper_envelope_l1(F, u):
    """In place: F(d) <- max_e F(e) - u*(|d1-e1|+|d2-e2|)  (max-plus transform with the separable
    l1 kernel: one forward and one backward sweep along each axis)."""
    n1, n2 = F.shape
    for j in range(1, n2):
        np.maximum(F[:, j], F[:, j - 1] - u, out=F[:, j])
    for j in range(n2 - 2, -1, -1):
        np.maximum(F[:, j], F[:, j + 1] - u, out=F[:, j])
    for i in range(1, n1):
        np.maximum(F[i, :], F[i - 1, :] - u, out=F[i, :])
    for i in range(n1 - 2, -1, -1):
        np.maximum(F[i, :], F[i + 1, :] - u, out=F[i, :])
    return F


class Twins:
    def __init__(self, n1, n2, u, T, cap=True, W2_T=None):
        """cap=False builds the first (refuted, DEAD_ENDS D50 item 3) version without the cap g1+g2.
        W2_T: budget used for W2 (default T, as in the theorem)."""
        self.n1, self.n2, self.u, self.T = n1, n2, u, T
        lp1, lp2 = ln_binom_pmf(n1), ln_binom_pmf(n2)
        self.lp1, self.lp2 = lp1, lp2
        c1, c2 = -lp1, -lp2
        g1 = -lip_minorant(lp1.max() - lp1, u)
        g2 = -lip_minorant(lp2.max() - lp2, u)
        self.g1, self.g2 = g1, g2
        W1 = (c1[:, None] + c2[None, :]) <= T
        W2 = c2 <= (T if W2_T is None else W2_T)
        self.W1, self.W2 = W1, W2
        self.ok = bool(W1.any() and W2.any())
        if not self.ok:
            return
        idx = np.nonzero(W2)[0]
        lo2, hi2 = int(idx[0]), int(idx[-1])
        assert np.all(W2[lo2:hi2 + 1]), "W2 is not an interval"
        self.lo2, self.hi2 = lo2, hi2
        F = np.where(W1, g1[:, None], NEG) + np.zeros((n1 + 1, n2 + 1))
        upper_envelope_l1(F, u)
        self.Fdeep = F
        Fcap = np.maximum(F, g1[:, None] + g2[None, :]) if cap else F.copy()
        self.Fcap = Fcap
        FD, FS = Fcap.copy(), Fcap.copy()
        j = np.arange(n2 + 1)
        left, right = j < lo2, j > hi2
        if left.any():
            FD[:, left] = Fcap[:, [lo2]] - u * (lo2 - j[left])[None, :]
            FS[:, left] = Fcap[:, [lo2]] + u * (lo2 - j[left])[None, :]
        if right.any():
            FD[:, right] = Fcap[:, [hi2]] - u * (j[right] - hi2)[None, :]
            FS[:, right] = Fcap[:, [hi2]] + u * (j[right] - hi2)[None, :]
        self.FD, self.FS = FD, FS
        lp = lp1[:, None] + lp2[None, :]
        self.lp = lp
        self.lnA_D = float(logsumexp(lp - FD))
        self.lnA_S = float(logsumexp(lp - FS))
        self.gap = self.lnA_D - self.lnA_S
        # tail probabilities, summed in log space over the complements
        out1 = ~W1
        self.lnp1 = float(logsumexp(lp[out1])) if out1.any() else NEG
        self.lnp2 = float(logsumexp(lp2[~W2])) if (~W2).any() else NEG
        self.V2 = np.broadcast_to(W2[None, :], W1.shape)

    def lnp_sum(self):
        return float(np.logaddexp(self.lnp1, self.lnp2))

    def E(self):
        return -self.lnp_sum() / (self.n1 + self.n2)

    def checks(self, tol=1e-9):
        """Returns a dict of booleans / numbers; every item must be True for the theorem's pair."""
        u = self.u
        res = {}
        for name, F in (("FD", self.FD), ("FS", self.FS), ("Fcap", self.Fcap)):
            d1 = np.abs(np.diff(F, axis=0)).max() if F.shape[0] > 1 else 0.0
            d2 = np.abs(np.diff(F, axis=1)).max() if F.shape[1] > 1 else 0.0
            res[f"lip_{name}"] = bool(max(d1, d2) <= u * (1 + tol) + tol)
            res[f"maxstep_{name}"] = float(max(d1, d2))
        g1b = np.broadcast_to(self.g1[:, None], self.W1.shape)
        res["C1_FD_eq_g1_on_W1"] = bool(np.all(np.abs(self.FD[self.W1] - g1b[self.W1]) <= tol))
        res["C1_FS_eq_g1_on_W1"] = bool(np.all(np.abs(self.FS[self.W1] - g1b[self.W1]) <= tol))
        res["C2_FD_eq_FS_on_V2"] = bool(np.all(self.FD[self.V2] == self.FS[self.V2]))
        res["C3_W1_subset_V2"] = bool(np.all(self.V2[self.W1]))
        res["FS_ge_FD"] = bool(np.all(self.FS >= self.FD - tol))
        res["S_A_FS_le_types"] = bool(self.lnA_S <= math.log((self.n1 + 1) * (self.n2 + 1)) + tol)
        res["S_every_type_mass_le_1"] = bool((self.lp - self.FS).max() <= tol)
        res["P1_bound"] = bool(self.lnp1 <= math.log((self.n1 + 1) * (self.n2 + 1)) - self.T + tol)
        res["P2_bound"] = bool(self.lnp2 <= math.log(self.n2 + 1) - self.T + tol)
        # where do the twins actually differ?  (must be inside the complement of V2)
        diff = self.FD != self.FS
        res["differ_only_outside_V2"] = bool(not np.any(diff & self.V2))
        res["ln_P_differ"] = float(logsumexp(self.lp[diff])) if diff.any() else NEG
        return res


def all_algorithms_exponent(n, u, eps):
    """n^{-1} ln(2^n/|B(n,k*(eps))|), k* the least k with Delta_k > eps (Theorem 11.25(a));
    Delta_k = ln(1 + 2^{-n} sum_{j<=k} C(n,j)(e^{u(k+1-j)} - 1)), everything in log space."""
    lp = ln_binom_pmf(n)
    j = np.arange(n + 1, dtype=float)
    for k in range(0, n + 1):
        x = u * (k + 1 - j[:k + 1])
        term = lp[:k + 1] + x + np.log1p(-np.exp(-x))
        s = float(logsumexp(term))
        delta = s if s > 50 else math.log1p(math.exp(s))
        if delta > eps:
            return -float(logsumexp(lp[:k + 1])) / n, k, delta
    return 0.0, n, float("inf")


def largest_budget(n1, n2, u, gapmin, cap=True, verbose=False):
    """Largest T (bisection; the gap is checked to be decreasing on a grid by scan_gap) at which
    the gap of the twins exceeds gapmin, under the constraint of the theorem (W2 at the same T)."""
    n = n1 + n2
    lo, hi = 1.0, 0.25 * n      # gap > gapmin at lo expected, not at hi
    tlo = Twins(n1, n2, u, lo, cap)
    if not tlo.ok or tlo.gap <= gapmin:
        # find some budget with a gap
        found = False
        for T in np.linspace(1.0, 0.25 * n, 200):
            t = Twins(n1, n2, u, T, cap)
            if t.ok and t.gap > gapmin:
                lo, found = T, True
                break
        if not found:
            return None
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        t = Twins(n1, n2, u, mid, cap)
        if t.ok and t.gap > gapmin:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-7 * n:
            break
    return Twins(n1, n2, u, lo, cap)


def main():
    u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    gapmin = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    ns = [int(x) for x in sys.argv[3:]] if len(sys.argv) > 3 else [400, 800, 1600, 3200]
    splits = [0.45, 0.50, 0.55, 0.60, 0.65]
    print(f"# R4 own computation: exact twins of Theorem 11.86, u = {u}, accuracy (gap >) {gapmin}")
    print("# for each n and split: the largest budget T at which ln A(F_D) - ln A(F_S) > gap;")
    print("# E = -ln(p1+p2)/n;  'all' = n^-1 ln(2^n/|B(n,k*)|) (Theorem 11.25(a), same accuracy)")
    for n in ns:
        Eall, kstar, delta = all_algorithms_exponent(n, u, gapmin)
        best = None
        for s in splits:
            n1 = int(round(s * n))
            n2 = n - n1
            t = largest_budget(n1, n2, u, gapmin)
            if t is None:
                print(f"n={n} n1={n1}: no budget with gap > {gapmin}")
                continue
            ch = t.checks()
            allok = all(v for k_, v in ch.items() if isinstance(v, bool))
            print(f"n={n:6d} n1={n1:5d} n2={n2:5d} T={t.T:10.4f} T/n={t.T/n:.5f} gap={t.gap:.4f} "
                  f"lnA_S={t.lnA_S:.3f} lnA_D={t.lnA_D:.3f} lnp1={t.lnp1:.3f} lnp2={t.lnp2:.3f} "
                  f"E={t.E():.5f} lo2/n2={t.lo2/n2:.4f} checks_all_ok={allok}")
            if not allok:
                print("   FAILED CHECKS:", {k_: v for k_, v in ch.items() if v is False})
            sys.stdout.flush()
            if best is None or t.E() > best[0]:
                best = (t.E(), n1, t)
        if best:
            print(f"==> n={n}: best E (two rounds) = {best[0]:.5f} at n1={best[1]};  all algorithms: "
                  f"{Eall:.5f} (k*={kstar}, Delta_k*={delta:.4f})")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
