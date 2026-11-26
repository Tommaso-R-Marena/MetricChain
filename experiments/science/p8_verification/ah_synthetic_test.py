#!/usr/bin/env python3
"""Coordinator's check of workstream P8's Theorem AH ("anchored hosts") on RANDOM functions, with EXACT constants.

Statement tested (P8_REPORT section 3.3, in the form its proof gives; my re-derivation is in the coordinator's note of
that report).  X = prod_i X_i finite, anchor x0, S(x) = {i : x_i != x0_i}, I_{m-1} the anchored expansion of order
m - 1.  A term tau is ANY function on X together with a set H of "host" sites.  Define, for |T| = m,

    Theta_tau(T)  =  max over x_T in X_T and over contexts z in X_{-T} WITH z_l = x0_l FOR EVERY HOST l NOT IN T
                     of | Delta_T tau(z; x_T) |,     Delta_T tau(z; x_T) = sum_{V subset T} (-1)^{|T - V|} tau(x_V, x0_{T-V}, z).

Claim: if |H| <= m then for every x:   | tau(x) - I_{m-1} tau(x) |  <=  sum_{T subset S(x), |T| = m} Theta_tau(T).
(P8 states it for |H| <= m - 1; the proof needs only |H| <= m: with the hosts last in the order, a host l outside T
could precede min T only if T fitted among the hosts after l.)

The constants here are the EXACT restricted suprema -- the smallest numbers the theorem allows -- so nothing but the
theorem itself can make the inequality hold.  Two families of functions:
  "gauss"      i.i.d. Gaussian tables (generic; but a sum of many maxima against one number is a weak test: my first
               version of this script used only this family and NONE of its controls failed for m >= 3 -- kept in the
               log as a warning);
  "structured" F = sum of 1..3 products  c prod_{i in U} [x_i != x0_i]  with Gaussian c, the first U containing all
               hosts.  For these the restricted constants vanish wherever the theorem lets them, the inequality is
               attained with ratio exactly 1 when |H| = m, and every wrong version of the statement is violated.
Controls that MUST fail on the structured family (a test that cannot fail tests nothing):
  control A: all sites outside T at the anchor (the "anchor context" only) -- not what the theorem says;
  control B: |H| = m + 1 hosts -- one more host than the hypothesis allows (shows the hypothesis |H| <= m is sharp);
  control C: the roles exchanged (every NON-host outside T at the anchor, hosts free), one host.
Also tested: the unrestricted constants (workstream P3's Proposition 1), which must hold as well.

Run: python3 -B ah_synthetic_test.py > ah_synthetic_test.log
"""
import itertools, sys, time, resource
import numpy as np

rng = np.random.default_rng(20261126)
t0 = time.time()


def anchored_remainder(F, m):
    """F - I_{m-1} F on the whole grid (anchor = index 0 on every axis): sum over U, |U| >= m, of the anchored
    component d_U, d_U = prod_{i in U} (1 - P_i) prod_{i not in U} P_i F,  P_i = restriction to the anchor on axis i."""
    n = F.ndim
    R = np.zeros_like(F)
    for r in range(m, n + 1):
        for U in itertools.combinations(range(n), r):
            d = F
            for i in range(n):
                a = np.take(d, [0], axis=i)
                d = (d - a) if i in U else a + 0 * d[tuple(slice(0, 1) if j == i else slice(None) for j in range(n))]
            R = R + d                      # d has size 1 on the axes outside U: broadcasts; vanishes when x_i = x0_i, i in U
    return R


def mixed_difference(F, T):
    """Delta_T F(z; x_T) as an array over the whole grid (x_T on the axes of T, z on the others)."""
    d = F
    for i in T:
        d = d - np.take(d, [0], axis=i)
    return d


def theta(F, T, frozen):
    """max |Delta_T F| over x_T and the contexts z with z_l = x0_l for l in `frozen` (a set of sites outside T)."""
    d = np.abs(mixed_difference(F, T))
    for l in frozen:
        d = np.take(d, [0], axis=l)
    return float(d.max())


def make_function(shape, H, family):
    n = len(shape)
    if family == "gauss":
        return rng.standard_normal(shape)
    F = np.zeros(shape)
    for j in range(int(rng.integers(1, 4))):
        U = set(H) if j == 0 else set()
        U |= {i for i in range(n) if rng.random() < 0.5}
        if not U: U = {int(rng.integers(n))}
        term = np.array(rng.standard_normal())
        for i in range(n):
            ind = (np.arange(shape[i]) != 0).astype(float) if i in U else np.ones(shape[i])
            term = np.multiply.outer(term, ind)
        F = F + term
    return F


def run(shape, m, nhost, mode, ntrial, family):
    """returns (functions, (function, state) checks, violations, functions with a violation,
    smallest bound/|remainder| over the states with MORE than m sites off the anchor)."""
    n = len(shape); viol = 0; checks = 0; worst = np.inf; fviol = 0
    S = np.stack(np.meshgrid(*[np.arange(k) != 0 for k in shape], indexing="ij"), axis=-1)       # indicator of S(x)
    more = S.sum(axis=-1) > m
    for _ in range(ntrial):
        H = set(rng.choice(n, size=nhost, replace=False).tolist()) if nhost else set()
        F = make_function(shape, H, family)
        R = np.abs(anchored_remainder(F, m))
        B = np.zeros(shape)
        for T in itertools.combinations(range(n), m):
            out = [i for i in range(n) if i not in T]
            if mode == "AH": frozen = [l for l in out if l in H]
            elif mode == "all-contexts": frozen = []
            elif mode == "anchor-context": frozen = out
            elif mode == "roles-exchanged": frozen = [l for l in out if l not in H]
            B += theta(F, T, frozen) * S[..., list(T)].all(axis=-1)
        bad = R > B * (1 + 1e-10) + 1e-10
        viol += int(bad.sum()); checks += R.size; fviol += int(bad.any())
        nz = more & (R > 1e-10)
        if nz.any(): worst = min(worst, float((B[nz] / R[nz]).min()))
    return ntrial, checks, viol, fviol, worst


print("Theorem AH with exact restricted constants; anchor = state 0 of every site", flush=True)
print("| family | grid | m | hosts | constants | functions | (function, state) checks | violations (functions with one) | smallest bound / |remainder|, states with more than m sites off the anchor | expected | as expected |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
tot_ok = 0; fails = []; weak = []
for family in ("structured", "gauss"):
    for shape in ((3, 2, 3, 2, 3), (2, 3, 2, 2, 3, 2)):
        n = len(shape)
        for m in (2, 3, 4):
            cases = [(h, "AH", "holds") for h in range(0, m + 1)] + [(0, "all-contexts", "holds"), (2, "all-contexts", "holds")]
            cases += [(1, "anchor-context", "FAILS (control A)")]
            if m + 1 <= n: cases += [(m + 1, "AH", "FAILS (control B)")]
            if n - 1 >= m + 1: cases += [(1, "roles-exchanged", "FAILS (control C)")]
            for h, mode, exp in cases:
                nt = 400 if n == 5 else 150
                nf, ck, v, fv, w = run(shape, m, h, mode, nt, family)
                ok = (v == 0) if exp == "holds" else (v > 0)
                print(f"| {family} | {'x'.join(map(str, shape))} | {m} | {h} | {mode} | {nf} | {ck} | {v} ({fv}) | {w:.4f} | {exp} | {'yes' if ok else 'NO'} |", flush=True)
                if exp == "holds":
                    tot_ok += ck
                    if v: fails.append((family, shape, m, h, mode, v))
                elif v == 0:
                    (weak if family == "gauss" else fails).append((family, shape, m, h, mode, "control did not fail"))
print()
print(f"claims expected to hold: {tot_ok} (function, state) checks, violations: {sum(f[-1] for f in fails if isinstance(f[-1], int))}")
print(f"unexpected outcomes on the structured family: {[f for f in fails] if fails else 'none'}")
print(f"controls that did not fail on the Gaussian family (the weakness of that family, see the docstring): {len(weak)}")
print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
