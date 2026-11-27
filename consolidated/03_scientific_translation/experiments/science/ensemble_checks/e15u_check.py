#!/usr/bin/env python3
"""Science division, coordinator's check of the Ensemble division's Proposition E15U as stated in ENSEMBLE-MSG-0005 §2
(their commit 7eb9cae; their report and proof NOT read).  The statement, quoted with every clause:

  "Binary sites, any positive known part, any slopes, centre a; nu = mu*_a; N the number of sites that disagree
   with the centre; an up-set is a set of configurations closed under switching further sites away from the centre.
   The bound TV(mu, mu*_a) <= sum_i [mu*_a(x_i = a_i) - mu(x_i = a_i)] holds for every member of the class if and
   only if E_nu[N | U] - E_nu[N | U^c] >= 1 for every up-set U."

In disagreement variables e in {0,1}^n (centre = 0): nu is an arbitrary positive measure; a member is mu = h nu /
E_nu h with ln h(e + i) - ln h(e) in [0, 2 delta_i] (the member's energy has differences at most delta_i; the
polarised member has them equal to delta_i towards the centre); the right-hand side of the bound is E_mu N - E_nu N.

REVIEW (my own derivation, in the message SCI-RES-0038): layer cake.  For a monotone density h with E_nu h = 1 let
p(s) = nu(h > s); the sets {h > s} are up-sets; TV = int_1^inf p;  E_nu[(h-1)N] = int_0^inf Cov(1_{h>s}, N) ds
>= int_0^inf p(1-p) under the condition; and int_1^inf p^2 <= p(1) int_0^1 (1-p) <= int_0^1 p(1-p).  Necessity: the
member h = 1 + t 1_U (t <= exp(2 min delta) - 1) has TV - RHS = t q (1-q) (1 - m_U) / (1 + t q),  q = nu(U).

REPLICATION (this script):
 (A) random nu on 2, 3, 4 sites: m(nu) = min over up-sets of E[N|U] - E[N|U^c].  If m >= 1: no member violates the
     bound — tested on random members (max and min of additive log-densities; random admissible log-densities) and
     on all two-level members.  If m < 1: the two-level member of the minimising up-set violates it by exactly the
     closed form above.
 (C) a frozen site: with slope 0 at one site the bound can hold for every member while the stated condition fails
     at an up-set that cuts through that site — so "any slopes" must be "any positive slopes" for the "only if".
 (B) their examples: two sites, pi ~ exp(-x1 x2 / 2), slopes 1, centre all-plus: the largest excess of TV over the
     bound, by search over all members, against their closed form (1+e^2)/(3+e^2) - 2/(3+e^-2) = 0.1696;
     three sites, nu = (1 - lam (-1)^N)/8: the bound holds iff lam <= 1/2.
Controls that can fail: a condition with threshold 0.9 instead of 1 must be contradicted by some instance (a nu with
0.9 <= m < 1 and a violating member); the closed form of the violation is asserted to 1e-12.
Run:  python3 -B e15u_check.py > e15u_check.log
"""
import itertools, time, resource
import numpy as np
t0 = time.time()
rng = np.random.default_rng(20261126)


def cube(n):
    return np.array(list(itertools.product((0, 1), repeat=n)))


def upsets(n):
    """all up-sets of {0,1}^n except the empty set and the whole cube, as boolean vectors over the 2^n states"""
    X = cube(n); idx = {tuple(x): k for k, x in enumerate(X)}
    out = set()
    # an up-set is determined by its antichain of minimal elements; enumerate by closure of all subsets of states (n <= 4: 2^16)
    N = len(X)
    above = np.zeros((N, N), dtype=bool)
    for a in range(N):
        for b in range(N):
            above[a, b] = np.all(X[b] >= X[a])
    if n <= 3:
        for mask in range(1, 2 ** N):
            gens = [k for k in range(N) if mask >> k & 1]
            U = above[gens].any(axis=0)
            out.add(U.tobytes())
    else:
        # antichains via recursive closure: grow up-sets by adding one maximal missing state whose all successors are inside
        start = np.zeros(N, dtype=bool); start[idx[tuple([1] * n)]] = True
        seen = {start.tobytes()}; stack = [start]
        while stack:
            U = stack.pop()
            for k in range(N):
                if not U[k] and all(U[j] for j in range(N) if j != k and above[k, j]):
                    V = U.copy(); V[k] = True; key = V.tobytes()
                    if key not in seen: seen.add(key); stack.append(V)
        out = seen
    res = [np.frombuffer(b, dtype=bool) for b in out]
    return [U for U in res if 0 < U.sum() < N]


def m_of(nu, Nn, ups):
    best, arg = np.inf, None
    for U in ups:
        q = nu[U].sum()
        d = (nu[U] @ Nn[U]) / q - (nu[~U] @ Nn[~U]) / (1 - q)
        if d < best: best, arg = d, U
    return best, arg


def excess(h, nu, Nn):
    """TV(mu, nu) - (E_mu N - E_nu N) for mu = h nu / E_nu h"""
    mu = h * nu; mu = mu / mu.sum()
    return 0.5 * np.abs(mu - nu).sum() - (mu @ Nn - nu @ Nn)


def random_members(n, X, delta, k):
    """admissible log-densities: increments in [0, 2 delta_i]"""
    out = []
    for _ in range(k):
        kind = rng.integers(3)
        W = rng.uniform(0, 2 * delta, size=(rng.integers(1, 5), n)); b = rng.normal(size=len(W))
        vals = W @ X.T + b[:, None]
        if kind == 0: lh = vals.max(axis=0)
        elif kind == 1: lh = vals.min(axis=0)
        else:
            # a random admissible log-density built state by state in order of N: any value between the constraints
            lh = np.zeros(len(X)); order = np.argsort(X.sum(axis=1), kind="stable")
            pos = {tuple(x): j for j, x in enumerate(X)}
            for j in order:
                x = X[j]
                if x.sum() == 0: continue
                lo, hi = -np.inf, np.inf
                for i in range(n):
                    if x[i]:
                        y = x.copy(); y[i] = 0; v = lh[pos[tuple(y)]]
                        lo = max(lo, v); hi = min(hi, v + 2 * delta[i])
                lh[j] = rng.uniform(lo, hi) if hi > lo else lo
        out.append(np.exp(lh - lh.max()))
    return out


print("Proposition E15U (Ensemble division, 7eb9cae; statement as in ENSEMBLE-MSG-0005 §2) — replication on 2, 3 and 4 binary sites\n")
tot = dict(inst=0, hold=0, fail=0, viol_when_hold=0, members=0, two_level=0, control=0)
for n in (2, 3, 4):
    X = cube(n); Nn = X.sum(axis=1).astype(float); ups = upsets(n)
    ninst = {2: 400, 3: 400, 4: 150}[n]; nh = nf = 0; worst_hold = -np.inf; ctrl = 0; least_viol = np.inf
    for _ in range(ninst):
        # positive measures of several kinds: random pair interactions of either sign plus fields, in disagreement variables
        J = rng.normal(scale=rng.choice([0.3, 1.0, 2.0]), size=(n, n)); J = np.triu(J, 1); hf = rng.normal(scale=1.0, size=n)
        s = 2 * X - 1
        nu = np.exp(np.einsum("ki,ij,kj->k", s, J, s) + s @ hf); nu /= nu.sum()
        delta = rng.uniform(0.2, 1.5, size=n)
        m, U = m_of(nu, Nn, ups)
        tot["inst"] += 1
        if m >= 1:
            nh += 1
            for h in random_members(n, X, delta, 60):
                e = excess(h, nu, Nn); worst_hold = max(worst_hold, e); tot["members"] += 1
                assert e <= 1e-12, ("the bound is violated although the condition holds", n, m, e)
            tcap = np.exp(2 * delta.min()) - 1
            for V in ups:
                for t in (1e-3, 0.5 * tcap, tcap):
                    e = excess(1 + t * V, nu, Nn); worst_hold = max(worst_hold, e); tot["two_level"] += 1
                    assert e <= 1e-12, ("a two-level member violates the bound although the condition holds", n, m, e)
        else:
            nf += 1
            t = np.exp(2 * delta.min()) - 1; q = nu[U].sum()
            e = excess(1 + t * U, nu, Nn); closed = t * q * (1 - q) * (1 - m) / (1 + t * q)
            assert abs(e - closed) < 1e-12 and e > 0, ("closed form of the violation", e, closed)
            # the member is admissible: increments of ln(1 + t 1_U) are 0 or ln(1+t) <= 2 min delta
            least_viol = min(least_viol, e)
            if m >= 0.9: ctrl += 1
    tot["hold"] += nh; tot["fail"] += nf; tot["control"] += ctrl
    print(f"n = {n}: {len(ups):4d} up-sets; {ninst} random measures: condition holds for {nh}, fails for {nf}; "
          f"when it holds the largest excess TV - bound over members is {worst_hold:.2e} (<= 0: no violation); when it fails the two-level member of the minimising up-set violates the bound, "
          f"smallest violation {least_viol:.2e}, equal to t q (1-q)(1-m)/(1+tq) to 1e-12; control: {ctrl} measures have 0.9 <= m < 1 and a violating member (a threshold of 0.9 would be wrong)")

print("\n(B1) two sites, pi ~ exp(-x1 x2 / 2), centre (+,+), slopes 1")
X = cube(2); Nn = X.sum(axis=1).astype(float); s = 1 - 2 * X            # disagreement 1 <-> spin -1
pi = np.exp(-0.5 * s[:, 0] * s[:, 1]); nu = pi * np.exp(-Nn); nu /= nu.sum()
m, U = m_of(nu, Nn, upsets(2))
best = -np.inf; arg = None
g = np.linspace(0, 2, 201)
for l10 in g:
    for l01 in g:
        lo, hi = max(l10, l01), min(l10, l01) + 2
        for l11 in np.linspace(lo, hi, 201):
            lh = np.zeros(4)
            for k, x in enumerate(X):
                lh[k] = (0.0, l01, l10, l11)[2 * x[0] + x[1]]
            e = excess(np.exp(lh), nu, Nn)
            if e > best: best, arg = e, (l10, l01, l11)
closed = (1 + np.e ** 2) / (3 + np.e ** 2) - 2 / (3 + np.e ** -2)
print(f"   m = {m:.4f} < 1 (the condition fails); largest excess of TV over the bound, grid search over all members: {best:.6f} at log-density (site 1, site 2, both) = {arg}; their closed form (1+e^2)/(3+e^2) - 2/(3+e^-2) = {closed:.6f}")
b1 = abs(best - closed) < 2e-4

print("\n(B2) three sites, nu = (1 - lam (-1)^N)/8: the least lam at which the condition fails")
X = cube(3); Nn = X.sum(axis=1).astype(float); ups3 = upsets(3)
def m3(lam):
    nu = (1 - lam * (-1) ** Nn) / 8
    return m_of(nu, Nn, ups3)[0]
lo, hi = 0.0, 0.999
assert m3(lo) >= 1 and m3(hi) < 1
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if m3(mid) >= 1 - 1e-13: lo = mid
    else: hi = mid
pc = [np.cov(X[:, i], X[:, j], aweights=(1 - 0.4 * (-1) ** Nn) / 8, bias=True)[0, 1] for i in range(3) for j in range(i + 1, 3)]
print(f"   threshold lam = {lo:.9f} (their statement: the bound holds iff lam <= 1/2); pair covariances at lam = 0.4: {max(abs(c) for c in pc):.1e} (their statement: all zero)")
b2 = abs(lo - 0.5) < 1e-8

print("\n(C) a frozen site (slope 0 at site 1), three sites: the bound can hold for every member although the condition fails at an up-set that cuts through the frozen site")
X = cube(3); Nn = X.sum(axis=1).astype(float); ups3 = upsets(3)
found = None
for trial in range(4000):
    w = rng.dirichlet(np.ones(8) * 0.7)
    inv = [U for U in ups3 if all(U[k] == U[k ^ 4] for k in range(8))]        # invariant under switching site 1 (the first coordinate = bit 4)
    m_inv = min((w[U] @ Nn[U]) / w[U].sum() - (w[~U] @ Nn[~U]) / w[~U].sum() for U in inv)
    m_all, Umin = m_of(w, Nn, ups3)
    if m_inv >= 1.02 and m_all <= 0.9:
        found = (w, m_inv, m_all, Umin); break
assert found is not None, "no instance found"
w, m_inv, m_all, Umin = found
delta = np.array([0.0, 1.0, 1.0]); worst = -np.inf; cnt = 0
for h in random_members(3, X, delta, 4000):
    assert all(abs(h[k] - h[k ^ 4]) < 1e-12 for k in range(8))                 # members do not vary along the frozen site
    worst = max(worst, excess(h, w, Nn)); cnt += 1
for U in inv:
    for t in (1e-3, 1.0, np.e ** 2 - 1):
        worst = max(worst, excess(1 + t * U, w, Nn)); cnt += 1
assert worst <= 1e-12, ("a member violates the bound in the frozen-site instance", worst)
print(f"   an instance: least m over the {len(inv)} up-sets invariant under site 1: {m_inv:.4f} >= 1; least m over all 18 up-sets: {m_all:.4f} < 1 (at an up-set that is not invariant: {not all(Umin[k] == Umin[k ^ 4] for k in range(8))}); "
      f"largest excess over {cnt} members with slopes (0, 1, 1): {worst:.2e} (<= 0: the bound holds for every member tested, the condition over all up-sets fails)")
frozen_ok = True

print(f"\nsummary: {tot['inst']} random measures on 2-4 sites: condition holds for {tot['hold']} (no violation among {tot['members']} random members and {tot['two_level']} two-level members), fails for {tot['fail']} "
      f"(an explicit admissible member violates the bound each time, by the closed form); control instances with 0.9 <= m < 1: {tot['control']}")
print(f"         their two-site excess reproduced: {b1}; their three-site threshold 1/2 reproduced: {b2}")
assert tot["control"] > 0 and b1 and b2 and frozen_ok
print(f"ALL DONE  {time.time()-t0:.1f} s  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")
