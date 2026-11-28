#!/usr/bin/env python3
"""Referee replication 2: exact enumeration on small cubes (n = 8..12), independent code.

Checks, each by brute force over all 2^n points (float64; tolerances 1e-9 unless said):
  A  Lemma 2.2 (averaging), identity (2.1)
  B  Theorem A: range of Y_j, admissibility of the uniform answer on the good event (simulation of P(G))
  C  Lemma 2.5 (i)-(iii); the degenerate case of (iii); exact expected overlap of two uniform centres
  D  Theorem A': on the good event the uniform answers are admissible
  E  Lemma 2.6 / Theorem A'' / Corollary A'': flat mixture for random pi; invertibility of the kernel;
     the product weights of exp(-gamma|x|) (report's formula versus the referee's)
  F  Lemma 3.1 / 3.2 / Theorem B / Theorem B': invariance kills characters; generators; random multiset
  G  Theorem C: zoom identity, the sampling bound
  H  Proposition C'(c): the wells
Nothing is imported from the coordinator's scripts.  Run: python3 -B r2_enum.py
"""
import math
import itertools
import numpy as np

rng = np.random.default_rng(20261128)
FAIL = []


def check(name, ok, info=""):
    print(("PASS  " if ok else "FAIL  ") + name + ("   " + info if info else ""))
    if not ok:
        FAIL.append(name)


def popcount_table(n):
    t = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        t += (np.arange(1 << n) >> i) & 1
    return t


def is_admissible(w, n, u, tol=1e-12):
    """w(x) <= e^u w(y) for all neighbours (equivalent to the full condition on the cube)."""
    x = np.arange(1 << n)
    for i in range(n):
        y = x ^ (1 << i)
        if np.any(w > math.exp(u) * w[y] * (1 + tol)):
            return False
    return bool(np.all(w > 0))


def random_admissible(n, u, PC, ncones=6):
    """A random member of the class: a positive combination / maximum of random cones and a floor."""
    N = 1 << n
    x = np.arange(N)
    w = np.full(N, rng.uniform(0.2, 2.0))
    for _ in range(ncones):
        c = int(rng.integers(N))
        cone = rng.uniform(0.5, 30.0) * np.exp(-u * PC[x ^ c])
        if rng.random() < 0.5:
            w = np.maximum(w, cone)
        else:
            w = w + cone
    return w


def e_r(n, u, r, PC):
    return np.maximum(np.exp(u * (r - PC)) - 1.0, 0.0)


def Vol(n, r):
    return sum(math.comb(n, j) for j in range(0, r + 1)) if r >= 0 else 0


# ----------------------------------------------------------------------------------------------
print("== A. Lemma 2.2 and identity (2.1) ==")
for (n, u) in [(8, 1.0), (10, 0.5), (10, 2.0)]:
    N = 1 << n
    PC = popcount_table(n)
    x = np.arange(N)
    w = random_admissible(n, u, PC)
    check(f"A0 n={n} u={u}: the random weight is admissible", is_admissible(w, n, u))
    L = 5
    cs = rng.integers(N, size=L)
    lam = rng.dirichlet(np.ones(L))
    wbar = sum(lam[j] * w[x ^ cs[j]] for j in range(L))
    check(f"A1 n={n}: wbar admissible", is_admissible(wbar, n, u))
    check(f"A2 n={n}: A(wbar)=A(w)", abs(wbar.mean() - w.mean()) < 1e-12 * w.mean())
    phi = rng.uniform(-1, 1, size=N)
    lhs = (wbar * phi).mean() / wbar.mean()
    rhs = sum(lam[j] * (w[x ^ cs[j]] * phi).mean() / w.mean() for j in range(L))
    check(f"A3 n={n}: mu_wbar = sum lam_j mu_(w(.+c_j))", abs(lhs - rhs) < 1e-12)
    c = int(cs[0])
    check(f"A4 n={n}: E_mu_(w(.+c)) phi = E_mu_w phi(.+c)",
          abs((w[x ^ c] * phi).mean() / w.mean() - (w * phi[x ^ c]).mean() / w.mean()) < 1e-12)
    # (2.1): average over ALL c of E_{mu_{w(.+c)}} phi equals E_pi phi  (use convolution identity)
    # sum_c sum_x w(x^c) phi(x) = (sum w)(sum phi)
    tot = 0.0
    for cc in range(N):
        tot += (w[x ^ cc] * phi).mean() / w.mean()
    check(f"A5 n={n}: (2.1) E_c E_mu_(w(.+c)) phi = E_pi phi", abs(tot / N - phi.mean()) < 1e-10)

# ----------------------------------------------------------------------------------------------
print("== B. Theorem A: the range of Y_j and the good event ==")
n, u = 10, 1.0
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)
for k in [1, 2, 3]:
    dip = np.maximum(1.0, np.exp(u * (k + 1 - PC)))        # w_{0,k+1}
    A = dip.mean()
    Delta = math.log(A)
    m_r = e_r(n, u, k + 1, PC).mean()
    check(f"B1 k={k}: ln A(dip) = ln(1+m_(k+1))", abs(A - (1 + m_r)) < 1e-12)
    check(f"B2 k={k}: dip = 1 off B(0,k), |B|=V(n,k)", int(np.sum(dip != 1.0)) == Vol(n, k))
    # extreme values of Y(phi) over phi in [-1,1]^X: Y = E_mu phi(.+c); sup - inf over c for the worst phi
    # Y_c - A^-1 E_pi phi = (1-A^-1) E_nu phi(.+c) in [-(1-1/A), 1-1/A]
    worst = 0.0
    for _ in range(20):
        phi = rng.choice([-1.0, 1.0], size=N)
        ys = np.array([(dip * phi[x ^ c]).mean() / A for c in rng.integers(N, size=200)])
        worst = max(worst, ys.max() - ys.min())
    # adversarial phi: +1 on the ball around 0, -1 elsewhere
    phi = np.where(PC <= k, 1.0, -1.0)
    ys = np.array([(dip * phi[x ^ c]).mean() / A for c in range(N)])
    worst = max(worst, ys.max() - ys.min())
    check(f"B3 k={k}: range of Y_j <= 2(1-e^-Delta)", worst <= 2 * (1 - math.exp(-Delta)) + 1e-12,
          f"observed {worst:.5f} <= {2*(1-math.exp(-Delta)):.5f}")
# simulation of the good event: M observables, tolerance tau, L from the theorem
k = 2
dip = np.maximum(1.0, np.exp(u * (k + 1 - PC)))
A = dip.mean()
Delta = math.log(A)
tau, eta, M = 0.05, 0.2, 40
L = math.ceil(2 * tau ** -2 * (1 - math.exp(-Delta)) ** 2 * math.log(2 * M / eta))
phis = [rng.choice([-1.0, 1.0], size=N) for _ in range(M - 12)]
phis += [1.0 - 2.0 * ((x >> i) & 1) for i in range(10)]            # dictators
phis += [np.where(PC <= n // 2, 1.0, -1.0), np.where(PC <= k, 1.0, -1.0)]
phis = np.array(phis)
trials, bad, maxdev = 300, 0, 0.0
for _ in range(trials):
    cs = rng.integers(N, size=L)
    wc = np.zeros(N)
    for c in cs:
        wc += dip[x ^ c]
    wc /= L
    dev = np.abs((phis * wc).mean(axis=1) / wc.mean() - phis.mean(axis=1)).max()
    maxdev = max(maxdev, dev)
    bad += dev > tau
check(f"B4 Theorem A(a) good event: L={L}, fraction of bad c = {bad/trials:.3f} <= eta={eta}", bad / trials <= eta,
      f"(largest deviation seen {maxdev:.4f}, tau={tau}; Delta_k={Delta:.4f})")

# ----------------------------------------------------------------------------------------------
print("== C. Lemma 2.5 ==")
for (n, u, r) in [(10, 1.0, 2), (10, 1.0, 3), (12, 0.5, 3), (12, 2.0, 2)]:
    N = 1 << n
    PC = popcount_table(n)
    x = np.arange(N)
    er = e_r(n, u, r, PC)
    m_r = er.mean()
    V = Vol(n, r - 1)
    worst_ii_lo, worst_ii_hi, worst_iii = 1e9, 1e9, 1e9
    for trial in range(200):
        L = int(rng.integers(2, 9))
        if trial % 4 == 0:      # clustered centres (overlaps)
            base = int(rng.integers(N))
            cs = [base ^ int(sum(1 << int(b) for b in rng.choice(n, size=int(rng.integers(0, 3)), replace=False))) for _ in range(L)]
        else:
            cs = [int(c) for c in rng.integers(N, size=L)]
        es = np.array([er[x ^ c] for c in cs])
        wc = 1.0 + es.max(axis=0)
        if trial < 3:
            check(f"C1 n={n} r={r}: w_c admissible", is_admissible(wc, n, u))
            check(f"C2 n={n} r={r}: w_c = 1 off the union of balls",
                  bool(np.all((wc == 1.0) | (np.min([PC[x ^ c] for c in cs], axis=0) <= r - 1))))
        Oc = 0.0
        for j in range(L):
            for jp in range(j + 1, L):
                Oc += np.minimum(es[j], es[jp]).mean()
        Aex = wc.mean() - 1.0
        worst_ii_lo = min(worst_ii_lo, Aex - (L * m_r - Oc))
        worst_ii_hi = min(worst_ii_hi, L * m_r - Aex)
        mu = wc / wc.sum()
        mut = (1.0 + es.sum(axis=0)) / (N * (1 + L * m_r))
        tv = 0.5 * np.abs(mu - mut).sum()
        Otil = (es.sum(axis=0) - es.max(axis=0)).mean()
        assert Otil <= Oc + 1e-12
        if Oc < 1 + L * m_r:
            worst_iii = min(worst_iii, Oc / (1 + L * m_r - Oc) - tv)
    check(f"C3 n={n} u={u} r={r}: (ii) lower  L m_r - O_c <= A-1", worst_ii_lo >= -1e-12, f"min slack {worst_ii_lo:.3e}")
    check(f"C4 n={n} u={u} r={r}: (ii) upper  A-1 <= L m_r", worst_ii_hi >= -1e-12, f"min slack {worst_ii_hi:.3e}")
    check(f"C5 n={n} u={u} r={r}: (iii) TV <= O_c/(1+L m_r-O_c) when O_c < 1+L m_r", worst_iii >= -1e-12, f"min slack {worst_iii:.3e}")
    # exact expected overlap of two independent uniform centres: average over z of E_pi min(e_r, e_r(.+z))
    exact = np.mean([np.minimum(er, er[x ^ z]).mean() for z in range(N)])
    check(f"C6 n={n} u={u} r={r}: E min(e,e') <= m_r V(n,r-1)/2^n", exact <= m_r * V / N + 1e-15,
          f"exact {exact:.4e} <= bound {m_r*V/N:.4e} (ratio {exact/(m_r*V/N):.3f})")
# degenerate case of (iii): all centres equal, large L  ->  O_c > 1 + L m_r, right-hand side negative
n, u, r = 10, 2.0, 4
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)
er = e_r(n, u, r, PC)
m_r = er.mean()
L = 40
Oc = math.comb(L, 2) * m_r
wc = 1.0 + er
mu = wc / wc.sum()
mut = (1.0 + L * er) / (N * (1 + L * m_r))
tv = 0.5 * np.abs(mu - mut).sum()
print(f"      C7 degenerate case of Lemma 2.5(iii) (L={L} equal centres, n={n}, u={u}, r={r}): O_c={Oc:.3f}, 1+L m_r={1+L*m_r:.3f}, "
      f"stated bound O_c/(1+L m_r-O_c)={Oc/(1+L*m_r-Oc):.3f}, true TV={tv:.3f}")
check("C7 Lemma 2.5(iii) as stated FAILS without the proviso O_c < 1 + L m_r (expected: a counterexample)",
      tv > Oc / (1 + L * m_r - Oc), "the lemma needs the proviso; with O~ in place of O_c it is always true")
Otil = (L * er - er).mean()
check("C8 the version with O~ = E(sum-max): TV <= O~/(1+L m_r-O~)", tv <= Otil / (1 + L * m_r - Otil) + 1e-12)

# ----------------------------------------------------------------------------------------------
print("== D. Theorem A': on the good event the uniform answers are admissible ==")
for (n, u, r, tau, eta, M) in [(12, 2.0, 1, 0.3, 0.5, 5), (12, 1.0, 2, 0.6, 0.5, 5), (12, 1.0, 2, 1.0, 0.5, 3)]:
    N = 1 << n
    PC = popcount_table(n)
    x = np.arange(N)
    er = e_r(n, u, r, PC)
    m_r = er.mean()
    V = Vol(n, r - 1)
    L = math.ceil(8 * tau ** -2 * math.log(2 * M / eta))
    etap = (5 * L * m_r / (2 * tau)) * L * V / N
    phis = [rng.choice([-1.0, 1.0], size=N) for _ in range(M - 2)]
    phis += [1.0 - 2.0 * (x & 1), np.where(PC <= n // 2, 1.0, -1.0)]
    phis = np.array(phis)
    viol, inG, trials = 0, 0, 300
    maxdev_G = 0.0
    for _ in range(trials):
        cs = rng.integers(N, size=L)
        es = np.array([er[x ^ c] for c in cs])
        wc = 1.0 + es.max(axis=0)
        srt = -np.sort(-es, axis=0)                      # sum_{j<j'} min(a_j,a_j') = sum_k (k-1) a_(k)
        Oc = float((srt * np.arange(L)[:, None]).sum(axis=0).mean())
        Z = np.array([[(er * ph[x ^ c]).mean() / m_r for c in cs] for ph in phis])        # Z_j(phi_i)
        devZ = np.abs(Z.mean(axis=1) - phis.mean(axis=1)).max()
        good = (devZ <= tau / 2) and (Oc <= tau / 5)
        dev = np.abs((phis * wc).mean(axis=1) / wc.mean() - phis.mean(axis=1)).max()
        if good:
            inG += 1
            maxdev_G = max(maxdev_G, dev)
            if dev > tau + 1e-12 or wc.mean() < 1 + L * m_r - tau / 5 - 1e-12:
                viol += 1
    check(f"D1 n={n} u={u} r={r} tau={tau} M={M} L={L} (L m_r={L*m_r:.3f}, eta'={etap:.3f}): on G answers within tau, A >= 1+L m_r-tau/5",
          viol == 0 and inG > 0, f"G in {inG}/{trials} trials; largest deviation on G {maxdev_G:.4f} <= tau")
    check(f"D2 P(G) = {inG/trials:.3f} >= 1 - eta - eta' = {1-eta-etap:.3f} (simulation)", inG / trials >= 1 - eta - etap - 0.05)

# ----------------------------------------------------------------------------------------------
print("== E. Lemma 2.6, Theorem A'', Corollary A'' ==")
n, u = 8, 1.0
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)
D = PC[x[:, None] ^ x[None, :]]
Kmat = np.exp(-u * D)                                   # K[x,c]
S0 = Kmat.sum(axis=1)
check("E1 row sums of exp(-u d) constant", np.ptp(S0) < 1e-9 * S0[0])
ev = np.linalg.eigvalsh(Kmat)
check("E2 the kernel is invertible (all eigenvalues > 0)", ev.min() > 0,
      f"min eigenvalue {ev.min():.4e} = (1-e^-u)^n = {(1-math.exp(-u))**n:.4e}")
for trial in range(3):
    pi = rng.dirichlet(np.ones(N) * 0.3)                # an arbitrary reference measure
    eps0 = 0.7
    m = pi @ Kmat
    q = m / S0[0]
    H = eps0 / m
    check(f"E3.{trial} q is a probability vector", abs(q.sum() - 1) < 1e-12)
    flat = Kmat @ (q * H)
    check(f"E4.{trial} sum_c q(c) H(c) e^(-u d(x,c)) = eps0 for every x", np.abs(flat - eps0).max() < 1e-12)
    dips = np.maximum(1.0, H[None, :] * Kmat)
    dtr = np.minimum(1.0, H[None, :] * Kmat) @ q
    check(f"E5.{trial} sum_c q(c) w_c(x) = 1 + eps0 - delta_tr(x)", np.abs(dips @ q - (1 + eps0 - dtr)).max() < 1e-12)
    # the expectations used in Theorem A'': E Y = eps0 E_pi phi - E_pi[phi delta_tr], E e = eps0 - xibar
    phi = rng.uniform(-1, 1, size=N)
    Y = ((dips - 1.0) * (pi * phi)[:, None]).sum(axis=0)
    e = ((dips - 1.0) * pi[:, None]).sum(axis=0)
    xibar = pi @ dtr
    check(f"E6.{trial} E_q Y = eps0 E_pi phi - E_pi[phi delta_tr];  E_q e = eps0 - xibar;  |Y|<=eps0, 0<=e<=eps0",
          abs(q @ Y - (eps0 * (pi @ phi) - pi @ (phi * dtr))) < 1e-12 and abs(q @ e - (eps0 - xibar)) < 1e-12
          and np.abs(Y).max() <= eps0 + 1e-12 and e.min() >= -1e-15 and e.max() <= eps0 + 1e-12)
# uniqueness: only the product q*H is forced.  Another hiding law with the same flat superposition:
q2 = rng.dirichlet(np.ones(N))
H2 = (eps0 / S0[0]) / q2
check("E7 any law q~ with heights H~ = eps0/(S0 q~) is also 'flat' (so only q*H is unique, not q)",
      np.abs(Kmat @ (q2 * H2) - eps0).max() < 1e-10,
      f"member masses then range over [{(H2*m).min():.3g}, {(H2*m).max():.3g}] instead of all = eps0")
# Corollary A'': is exp(-gamma|x|) a mixture of cones with product weights, and which ratio?
print("   Corollary A'': product weights for w0 = exp(-gamma|x|)")
for gam in [0.5, -0.3, 0.9]:
    w0 = np.exp(-gam * PC)
    lam_rep = (1 - math.exp(-(u + gam))) / (1 - math.exp(-(u - gam)))                      # report, line 286
    lam_ref = (math.exp(-gam) - math.exp(-u)) / (1 - math.exp(-(u + gam)))                 # referee
    for name, ratio in [("report ", lam_rep), ("referee", lam_ref)]:
        lam = ratio ** PC                                                                  # lambda(c) prop. ratio^{|c|}
        mix = Kmat @ lam
        rel = mix / w0
        ok = np.ptp(rel) < 1e-9 * rel.mean()
        print(f"      gamma={gam:+.1f} {name} lambda1/lambda0={ratio:.5f}: sum_c lambda(c) e^(-u d(x,c)) / w0(x) "
              f"ranges over [{rel.min()/rel.max():.4f}, 1] (x max)   -> {'proportional to w0' if ok else 'NOT proportional to w0'}")
        if name == "referee":
            check(f"E8 gamma={gam}: referee's ratio (e^-g - e^-u)/(1 - e^-(u+g)) reproduces w0", ok)
        else:
            check(f"E9 gamma={gam}: the report's ratio (1-e^-(u+g))/(1-e^-(u-g)) does NOT reproduce w0 (expected: an error in line 286)", not ok)
    # Corollary A'' with the correct weights: flat relative mixture
    lam = lam_ref ** PC
    lam = lam / (Kmat @ lam)[0] * w0[0]                 # normalise: sum_c lam(c) e^{-u d} = w0
    pi = rng.dirichlet(np.ones(N))                      # arbitrary reference again
    A0 = pi @ w0
    mcol = (pi @ Kmat) / A0
    q = lam * mcol
    H = eps0 / mcol
    members = np.maximum(w0[:, None], H[None, :] * Kmat)
    rel = (members @ q) / w0
    dtr = np.minimum(1.0, H[None, :] * Kmat / w0[:, None]) @ q
    check(f"E10 gamma={gam}: Corollary A'': q=lambda*m is a law and sum_c q(c) max(w0, H e^(-u d))/w0 = 1+eps0-delta_tr",
          abs(q.sum() - 1) < 1e-10 and np.abs(rel - (1 + eps0 - dtr)).max() < 1e-10)
    check(f"E11 gamma={gam}: members max(w0, H(c) e^(-u d(.,c))) are admissible", all(is_admissible(members[:, c], n, u) for c in range(0, N, 37)))

# ----------------------------------------------------------------------------------------------
print("== F. Lemmas 3.1, 3.2, Theorems B, B' ==")
n, u = 10, 1.0
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)


def chi(s):
    return 1.0 - 2.0 * (PC[x & s] & 1)


def span(gens):
    S = {0}
    for g in gens:
        S |= {a ^ g for a in S}
    return sorted(S)


def multiset_span(gens):
    out = [0]
    for g in gens:
        out = out + [a ^ g for a in out]
    return out


for trial in range(6):
    M = int(rng.integers(1, 60))
    S = [int(s) for s in rng.choice(np.arange(1, N), size=M, replace=False)]
    r = math.ceil(math.log2(M + 1))
    # Lemma 3.2: a tuple exists; find one by random search and count the success frequency
    succ, found = 0, None
    for _ in range(400):
        g = [int(v) for v in rng.integers(N, size=r)]
        if all(any(PC[s & gi] & 1 for gi in g) for s in S):
            succ += 1
            found = g
    check(f"F1.{trial} M={M}, r={r}: a separating r-tuple exists (random success rate {succ/400:.2f} >= 1 - M/2^r = {1-M/2**r:.2f} - noise)",
          found is not None and succ / 400 >= 1 - M / 2 ** r - 0.08)
    C = span(found)
    check(f"F2.{trial} |C|={len(C)} <= 2^r < 2(M+1)", len(C) <= 2 ** r < 2 * (M + 1))
    k = 2
    dip = np.maximum(1.0, np.exp(u * (k + 1 - PC)))
    a = int(rng.integers(N))
    wC = sum(dip[x ^ a ^ c] for c in C) / len(C)
    check(f"F3.{trial} w_a^C admissible, A preserved, C-invariant",
          is_admissible(wC, n, u) and abs(wC.mean() - dip.mean()) < 1e-12 and all(np.allclose(wC[x ^ c], wC) for c in C))
    coeff = max(abs((wC * chi(s)).mean()) for s in S)
    check(f"F4.{trial} E_pi[w chi_s] = 0 for all s in S", coeff < 1e-12, f"max |coefficient| {coeff:.2e}")
    # an arbitrary (unbounded) real observable with spectrum in S
    phi = 3.7 + sum(rng.normal(scale=50.0) * chi(s) for s in S)
    check(f"F5.{trial} exact mean of an unbounded observable with spectrum in S equals its uniform mean",
          abs((wC * phi).mean() / wC.mean() - phi.mean()) < 1e-9)
    check(f"F6.{trial} w_a^C = 1 off the union of |C| balls", int(np.sum(np.abs(wC - 1.0) > 1e-15)) <= len(C) * Vol(n, k))
# (c): S = W \ {0}, W spanned by the first d coordinate characters: every C with C^perp cap S empty has |C| >= 2^d
n = 6
N = 1 << n
PCs = popcount_table(n)
d = 3
W = [s for s in range(1, 1 << d)]
best = None
# all subgroups of F_2^6 generated by at most 3 elements (enough: we look for |C| < 2^d = 8, i.e. dim <= 2)
small_ok = False
for g1 in range(N):
    for g2 in range(g1, N):
        C = span([g1, g2])
        if all(any(PCs[s & c] & 1 for c in C) for s in W):
            small_ok = True
check("F7 Theorem B(c): for S = W\\{0}, dim W = 3 (n=6), no subgroup of dimension <= 2 has C^perp cap S empty", not small_ok)
# Theorem B': random multiset of combinations
n, u, r = 12, 1.0, 2
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)
er = e_r(n, u, r, PC)
m_r = er.mean()
V = Vol(n, r - 1)
M = 6
S = [int(s) for s in rng.choice(np.arange(1, N), size=M, replace=False)]
K = 2 ** math.ceil(math.log2(4 * M))
kk = int(math.log2(K))
check(f"F8 Theorem B' side condition 4 K V <= 2^n (K={K}, V={V})", 4 * K * V <= N)
bad_i = bad_ii = both_ok = 0
trials = 300
ok_claims = True
for _ in range(trials):
    gens = [int(v) for v in rng.integers(N, size=kk)]
    Ct = multiset_span(gens)
    fail_i = any(all((PC[s & g] & 1) == 0 for g in gens) for s in S)
    es = np.array([er[x ^ c] for c in Ct])
    srt = -np.sort(-es, axis=0)
    O = float((srt * np.arange(K)[:, None]).sum(axis=0).mean())
    fail_ii = O > 0.5 * K * m_r
    bad_i += fail_i
    bad_ii += fail_ii
    if not fail_i and not fail_ii:
        both_ok += 1
        a = int(rng.integers(N))
        wa = 1.0 + np.array([er[x ^ a ^ c] for c in Ct]).max(axis=0)
        inv = all(np.allclose(wa[x ^ g], wa) for g in gens)
        zero = max(abs((wa * chi(s)).mean()) for s in S) < 1e-12
        mass = wa.mean() - 1 >= K * m_r - O - 1e-12 and wa.mean() - 1 >= 0.5 * K * m_r - 1e-12
        ok_claims = ok_claims and inv and zero and mass and is_admissible(wa, n, u)
check(f"F9 Theorem B': P(C^perp meets S) = {bad_i/trials:.3f} <= M/K = {M/K:.3f};  P(O > K m_r/2) = {bad_ii/trials:.3f} <= 1/4",
      bad_i / trials <= M / K + 0.06 and bad_ii / trials <= 0.25)
check(f"F10 Theorem B': for good generators ({both_ok}/{trials}) w_a is admissible, C-invariant, kills S, A-1 >= K m_r - O >= K m_r/2", ok_claims)

# ----------------------------------------------------------------------------------------------
print("== G. Theorem C: the zoom identity and the sampling bound ==")
n, u, b = 10, 1.0, 3
N = 1 << n
PC = popcount_table(n)
w = random_admissible(n, u, PC)
A = w.mean()
cells = w.reshape(1 << b, 1 << (n - b)) if False else None
# first b coordinates = the high bits here
wm = w.reshape(1 << b, 1 << (n - b))
nu = wm.sum(axis=1) / w.sum()
As = wm.mean(axis=1)
check("G1 A(w) = 2^-b E_y w(s,y) / nu_w(s) for every cell s", np.abs(2.0 ** -b * As / nu - A).max() < 1e-12 * A)
for s in range(1 << b):
    sub = wm[s]
    assert is_admissible(sub, n - b, u)
check("G2 every restriction y -> w(s,y) is admissible on n-b sites", True)
eps = 0.4
kappa = 1 - math.exp(-eps / 4)
worst = 0.0
for _ in range(2000):
    tau = rng.uniform(0.001, 0.2)
    pert = rng.normal(size=1 << b)
    pert -= pert.mean()
    nuh = nu + pert * (tau / np.abs(pert).sum()) * rng.uniform(0, 1)
    if nuh.min() <= 0:
        continue
    l1 = np.abs(nuh - nu).sum()
    pbad = nuh[np.abs(nu / nuh - 1) > kappa].sum()
    worst = max(worst, pbad - l1 / kappa)
    # outside the bad event the error of ln nu^(s) is at most eps/4
    okc = np.abs(nu / nuh - 1) <= kappa
    assert np.all(np.abs(np.log(nu[okc] / nuh[okc])) <= eps / 4 + 1e-12)
check("G3 P_{s~nu^}(|nu_w(s)/nu^(s)-1|>kappa) <= ||nu^-nu_w||_1/kappa, and |ln ratio| <= eps/4 otherwise", worst <= 1e-12)
# cylinders: A(w)=A(v), nu_w uniform
v = random_admissible(n - b, u, popcount_table(n - b))
cyl = np.tile(v, 1 << b)
check("G4 a cylinder is admissible on X, has A(w)=A(v) and a uniform block law",
      is_admissible(cyl, n, u) and abs(cyl.mean() - v.mean()) < 1e-12 and np.ptp(cyl.reshape(1 << b, -1).sum(axis=1)) < 1e-9)

# ----------------------------------------------------------------------------------------------
print("== H. Proposition C'(c): the wells ==")
n, u = 10, 1.0
N = 1 << n
PC = popcount_table(n)
x = np.arange(N)
okH = True
worst_tv = 0.0
for trial in range(40):
    eps = rng.uniform(0.05, 2.5)
    Delta = eps + math.log(2)
    rho = math.ceil(Delta / u) - 1
    Q = rng.choice(N, size=int(rng.integers(1, 12)), replace=False)
    dQ = np.min([PC[x ^ int(c)] for c in Q], axis=0)
    w = np.minimum(math.exp(Delta), np.exp(u * dQ))
    p = np.mean(dQ <= rho)
    A = w.mean()
    tv = 0.5 * np.abs(w / w.sum() - 1.0 / N).sum()
    okH = okH and is_admissible(w, n, u) and bool(np.all(w[Q] == 1.0)) and A > math.exp(Delta) * (1 - p) \
        and tv <= p / (1 - p) + 1e-12 and tv <= p + 1e-12 and bool(np.all((w == math.exp(Delta)) == (dQ > rho)))
    worst_tv = max(worst_tv, tv / p)
check("H1 wells: admissible, =1 on Q, =e^Delta exactly off the balls B(x,rho), A > e^Delta(1-p), TV <= p (<= p/(1-p))", okH,
      f"largest TV/p seen {worst_tv:.3f}")

print()
print("FAILED CHECKS:", FAIL if FAIL else "none")
