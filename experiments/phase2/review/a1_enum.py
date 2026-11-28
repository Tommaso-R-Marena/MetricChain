#!/usr/bin/env python3
"""a1_enum.py -- referee A1, exact enumeration for Lemma 2.5 (iv) and the new Theorem A'.

Written from the definitions of docs/phase2/PHASE2_REPORT.md (sections 1 and 2.3) only; nothing is
imported from the repository.  For a cube {0,1}^n (n <= 6), a radius r, a slope u and L <= 4 the
script enumerates ALL (2^n)^L tuples of centres c = (c_1..c_L) (equal and overlapping centres
included) and computes, for every tuple,

    w_c = 1 + max_j e_r(. xor c_j),   e_r(x) = (exp(u (r - |x|)) - 1)_+ ,
    A(w_c) - 1,   O_c = sum_{j<j'} E_pi min(e_j, e_j'),   G_psi(c) = E_pi[(w_c - 1) psi],  psi = phi - E_pi phi,

for a fixed list of observables phi with values in [-1, 1].  Checked:

  (a) Lemma 2.5 (ii):  R - O_c <= A(w_c) - 1 <= R  (R = L m_r) for every tuple;  E O_c <= C(L,2) m_r V / 2^n.
  (b) Lemma 2.5 (iv):  the mean of G_psi over all tuples is 0 (exactly, in integers, when u = ln 2);
      the one-centre oscillation  max |G_psi(c) - G_psi(c')|  (c, c' differ in one centre)  against
      2 ||psi||_inf m_r (lemma), 4 m_r (theorem) and against the sharper  osc(phi) m_r <= 2 m_r.
  (c) the identity  E_{mu_{w_c}} phi - E_pi phi = G_psi(c) / A(w_c)  for every tuple.
  (d) exact tails:  sup_t P(|G_psi| >= t) / [2 exp(-2 t^2 / (L d^2))]  for d = 4 m_r (the report),
      d = 2 m_r (referee's sharper constant) and d = the exact one-centre oscillation (McDiarmid's
      own hypothesis; a ratio > 1 there would mean a bug in this script).
  (e) Markov step:  P(O_c >= R/2) <= (L-1) V / 2^n <= eta'' ;  O_c < R/2  =>  A(w_c) - 1 > R/2.
  (f) the good event of Theorem A' where its hypotheses can be met on a small cube:
      M = number of observables, tau = sqrt(C R m_r ln(2M/eta)) (the least tolerance allowed),
      eps = ln(1 + R/2) (the largest accuracy allowed):  exact P(not good) against eta + eta''.
      C = 8 is the text that was reviewed (commit 67956b7); C = 2 is the text as revised on
      2026-11-28 03:17 UTC after this review (d = 2 m_r in McDiarmid's inequality).

Two modes: floating point (any u) and exact integers (u = ln 2, where e_r is integer valued and all
sums are integers; the float64 matrix products used there are exact because all partial sums are
integers below 2^53).

Usage:  python3 a1_enum.py [quick]      (output: stdout; redirected to a1_out_enum.txt)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import sys
import math
import time
import itertools
import numpy as np

LN2 = math.log(2.0)
KT = 2000          # number of grid thresholds for the conservative tail ratio


def popcounts(n):
    x = np.arange(1 << n)
    pc = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        pc += (x >> i) & 1
    return pc


def excess(n, u, r, exact):
    """e_r(x) for all x; exact=True means u = ln 2 and integer values 2^(r-|x|) - 1."""
    pc = popcounts(n)
    if exact:
        return np.where(pc < r, (1 << np.clip(r - pc, 0, 60)) - 1, 0).astype(np.int64)
    return np.where(pc < r, np.expm1(u * (r - pc)), 0.0)


def observables(n, r, seed, exact):
    """fixed observables with values in [-1, 1] (integer valued except the last one)."""
    N = 1 << n
    x = np.arange(N)
    pc = popcounts(n)
    rng = np.random.default_rng(seed)
    obs = [
        ("chi_1", 1 - 2 * (x & 1)),                                  # first coordinate
        ("parity", 1 - 2 * (pc & 1)),                                # Walsh character of full weight
        ("majority", np.sign(n - 2 * pc)),                           # 0 at ties
        ("point", (x == 0).astype(np.int64)),                        # indicator of one point
        ("1-2*B(0,1)", 1 - 2 * (pc <= 1).astype(np.int64)),          # psi close to -2 on a small ball
        ("two_balls", (pc < r).astype(np.int64) - ((n - pc) < r).astype(np.int64)),  # +1/-1 on antipodal dips
        ("halfcube", ((x & 1) == 0).astype(np.int64)),               # (1 + chi_1)/2
        ("rand_pm1", rng.choice(np.array([-1, 1]), size=N)),
        ("rand_tern", rng.choice(np.array([-1, 0, 1]), size=N)),
    ]
    if not exact:
        obs.append(("rand_unif", rng.uniform(-1.0, 1.0, size=N)))
    return obs


def brute_force(n, u, r, L, phis):
    """pure-Python reference (no tables shared with the vectorised code): for every tuple returns
    (A-1, O_c, [G_psi]) from the definitions.  Only for tiny cases."""
    N = 1 << n

    def dist(a, b):
        return bin(a ^ b).count("1")

    def e(x, c):
        d = dist(x, c)
        return math.exp(u * (r - d)) - 1.0 if d < r else 0.0

    means = [sum(float(v) for v in phi) / N for phi in phis]
    res = {}
    for c in itertools.product(range(N), repeat=L):
        wm1 = [max(e(x, cj) for cj in c) for x in range(N)]
        a1 = sum(wm1) / N
        o = 0.0
        for j in range(L):
            for k in range(j + 1, L):
                o += sum(min(e(x, c[j]), e(x, c[k])) for x in range(N)) / N
        g = [sum(wm1[x] * (float(phi[x]) - mu) for x in range(N)) / N for phi, mu in zip(phis, means)]
        res[c] = (a1, o, g)
    return res


def run_config(n, u, r, L, exact, seed=20261128, verbose=False, etas=(0.5, 0.9), cross_check=False):
    t0 = time.time()
    N = 1 << n
    u_eff = LN2 if exact else u
    e = excess(n, u, r, exact)
    idx = np.arange(N)
    E = e[idx[:, None] ^ idx[None, :]]                 # E[c, x] = e_r(x xor c)
    Ef = E.astype(np.float64)
    V = int((e > 0).sum())
    sum_e = float(e.sum())
    m_r = sum_e / N
    R = L * m_r
    # closed forms of section 1
    V_cf = sum(math.comb(n, j) for j in range(min(r, n + 1)))
    m_cf = sum(math.comb(n, j) * math.expm1(u_eff * (r - j)) for j in range(min(r, n + 1))) / N
    assert V == V_cf, (V, V_cf)
    assert abs(m_r - m_cf) <= 1e-12 * max(1.0, m_cf), (m_r, m_cf)
    eta2 = L * V / N

    obs = observables(n, r, seed, exact)
    names = [nm for nm, _ in obs]
    K = len(obs)
    Phi = np.stack([np.asarray(p, dtype=np.float64) for _, p in obs], axis=1)     # N x K
    assert np.all(np.abs(Phi) <= 1.0)
    phibar = Phi.mean(axis=0)
    Psi = Phi - phibar[None, :]
    psi_inf = np.abs(Psi).max(axis=0)
    psi_osc = Psi.max(axis=0) - Psi.min(axis=0)
    assert np.all(psi_inf <= 2.0 + 1e-12)
    if exact:
        PsiI = N * Phi - Phi.sum(axis=0)[None, :]      # integers: N * psi
        assert np.all(PsiI == np.rint(PsiI))
        Smax = int(round(L * sum_e * 2 * N)) + 1      # |S| <= sum_x maxE * |N psi| <= L sum_e * 2N
        hist = np.zeros((K, 2 * Smax + 1), dtype=np.int64)

    # pair overlaps  Pm[c,c'] = E_pi min(e(.+c), e(.+c'))
    Pm = np.minimum(Ef[:, None, :], Ef[None, :, :]).sum(axis=2) / N
    M2 = np.maximum(Ef[:, None, :], Ef[None, :, :]).reshape(N * N, N) if L >= 2 else None

    def blocks():
        if L == 1:
            yield (), Ef
        elif L == 2:
            yield (), M2
        elif L == 3:
            for c1 in range(N):
                yield (c1,), np.maximum(Ef[c1][None, :], M2)
        elif L == 4:
            for c1 in range(N):
                for c2 in range(N):
                    yield (c1, c2), np.maximum(M2[c1 * N + c2][None, :], M2)
        else:
            raise ValueError

    tail_len = 1 if L == 1 else 2
    O_tail = np.zeros(N) if L == 1 else Pm.reshape(N * N).copy()

    ntot = N ** L
    store = (ntot <= (1 << 20)) and not exact
    if store:
        Gall = np.empty((ntot, K))
        pos = 0
    gmax_bound = 2.0 * R                     # |G| <= ||psi||_inf (A-1) <= 2 R
    edges = np.linspace(0.0, gmax_bound * (1 + 1e-9), KT + 1)
    counts = np.zeros((K, KT), dtype=np.int64)

    sumG = np.zeros(K)
    sumG2 = np.zeros(K)
    maxabsG = np.zeros(K)
    osc1 = np.zeros(K)
    sumO = 0.0
    n_O_ge = 0
    n_A_le = 0
    n_implication_viol = 0
    n_hit0 = 0                   # tuples with w_c(0) != 1
    max_lower_viol = -np.inf     # max of (R - O_c) - (A-1): must be <= 0
    max_upper_viol = -np.inf     # max of (A-1) - R: must be <= 0
    max_ident = 0.0
    cases = [(cst, eta) for cst in (8.0, 2.0) for eta in etas]          # constant in the hypothesis, eta
    taus = [math.sqrt(cst * R * m_r * math.log(2.0 * K / eta)) for cst, eta in cases]
    n_badG = [0] * len(cases)     # exists i: |G_i| > tau
    n_badD = [0] * len(cases)     # exists i: |D_i| > tau   (D = G / A: the actual bias)
    n_bad = [0] * len(cases)      # not good: (exists i: |D_i| > tau) or A - 1 <= R/2
    sumS_exact = [0] * K
    probe = {}

    for prefix, blk in blocks():
        Am1 = blk.mean(axis=1)
        n_hit0 += int((blk[:, 0] > 0).sum())
        if exact:
            S = blk @ PsiI                         # exact integers in float64
            Sr = np.rint(S)
            assert np.all(S == Sr)
            G = Sr / (N * N)
            Si = Sr.astype(np.int64)
            for k in range(K):
                np.add.at(hist[k], Si[:, k] + Smax, 1)
                sumS_exact[k] += int(Si[:, k].sum())
        else:
            G = (blk @ Psi) / N
        # overlaps
        O = O_tail.copy()
        for i, p in enumerate(prefix):
            for q in prefix[i + 1:]:
                O += Pm[p, q]
            if tail_len == 2:
                O += (Pm[p][:, None] + Pm[p][None, :]).ravel()
            else:
                O += Pm[p]
        # (a)
        max_lower_viol = max(max_lower_viol, float(((R - O) - Am1).max()))
        max_upper_viol = max(max_upper_viol, float((Am1 - R).max()))
        sumO += float(O.sum())
        o_ge = O >= R / 2 - 1e-13 * max(R, 1.0)     # counted generously
        n_O_ge += int(o_ge.sum())
        a_le = Am1 <= R / 2 + 1e-13 * max(R, 1.0)   # counted generously
        n_A_le += int(a_le.sum())
        n_implication_viol += int((a_le & ~o_ge).sum())
        # (c) identity
        D_direct = ((1.0 + blk) @ Phi / N) / (1.0 + Am1)[:, None] - phibar[None, :]
        D = G / (1.0 + Am1)[:, None]
        max_ident = max(max_ident, float(np.abs(D_direct - D).max()))
        # (b)
        sumG += G.sum(axis=0)
        sumG2 += (G * G).sum(axis=0)
        absG = np.abs(G)
        maxabsG = np.maximum(maxabsG, absG.max(axis=0))
        if tail_len == 2:
            G3 = G.reshape(N, N, K)
            osc1 = np.maximum(osc1, (G3.max(axis=1) - G3.min(axis=1)).max(axis=0))
        else:
            osc1 = np.maximum(osc1, G.max(axis=0) - G.min(axis=0))
        # (d)
        for k in range(K):
            counts[k] += np.histogram(absG[:, k], bins=edges)[0]
        if store:
            Gall[pos:pos + G.shape[0]] = G
            pos += G.shape[0]
        # (f)
        mG = absG.max(axis=1)
        mD = np.abs(D).max(axis=1)
        for i, tau in enumerate(taus):
            n_badG[i] += int((mG > tau).sum())
            n_badD[i] += int((mD > tau).sum())
            n_bad[i] += int(((mD > tau) | a_le).sum())
        if cross_check:
            tails = itertools.product(range(N), repeat=tail_len)
            for t, tl in enumerate(tails):
                probe[tuple(prefix) + tuple(tl)] = (Am1[t], O[t], G[t].copy())

    meanG = sumG / ntot
    sdG = np.sqrt(np.maximum(sumG2 / ntot - meanG ** 2, 0.0))
    EO = sumO / ntot
    EO_bound = math.comb(L, 2) * m_r * V / N

    def b_mcd(t, d):
        return 2.0 * np.exp(-2.0 * t * t / (L * d * d))

    # conservative grid ratio:  sup_t P(|G|>=t)/b(t) <= max_k P(|G| >= t_k) / b(t_{k+1});
    # "nt" = the same sup restricted to the non-trivial range of the bound, b(t) < 1.
    tailP = counts[:, ::-1].cumsum(axis=1)[:, ::-1] / ntot           # P(|G| >= t_k), k = 0..KT-1

    def sup_ratio(p_ge, tvals, bvals_at):
        """(sup of p/b over all atoms, sup over atoms with b < 1); bvals_at = thresholds where b is evaluated"""
        b = b_mcd(bvals_at, d)
        pos = p_ge > 0
        if not pos.any():
            return 0.0, 0.0
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.where(pos, p_ge / b, 0.0)
        nt = pos & (b < 1.0)
        return float(q.max()), (float(q[nt].max()) if nt.any() else 0.0)

    ratios = {}
    for label, dvec in (("4m", np.full(K, 4 * m_r)), ("2m", np.full(K, 2 * m_r)), ("osc", osc1)):
        rr = np.zeros((K, 2))
        for k in range(K):
            d = max(dvec[k], 1e-300)
            rr[k] = sup_ratio(tailP[k], edges[:-1], edges[1:])
        ratios[label + "_grid"] = rr
        if store:
            rr2 = np.zeros((K, 2))
            for k in range(K):
                d = max(dvec[k], 1e-300)
                sv = np.sort(np.abs(Gall[:, k]))
                p_ge = (ntot - np.arange(ntot)) / ntot              # P(|G| >= sv[i]) (first index of a tie is the max)
                rr2[k] = sup_ratio(p_ge, sv, sv)
            ratios[label + "_exact"] = rr2
        if exact:
            rr3 = np.zeros((K, 2))
            svals = np.arange(-Smax, Smax + 1)
            for k in range(K):
                d = max(dvec[k], 1e-300)
                habs = np.bincount(np.abs(svals), weights=hist[k].astype(np.float64), minlength=Smax + 1)   # counts by |S|
                p_ge = habs[::-1].cumsum()[::-1] / ntot
                tgrid = np.arange(Smax + 1) / (N * N)
                nz = habs > 0
                rr3[k] = sup_ratio(p_ge[nz], tgrid[nz], tgrid[nz])
            ratios[label + "_exact"] = rr3

    key = "exact" if (store or exact) else "grid"
    res = dict(n=n, u=u_eff, r=r, L=L, exact=exact, ntot=ntot, m_r=m_r, R=R, V=V, eta2=eta2,
               names=names, meanG=meanG, sdG=sdG, maxabsG=maxabsG, osc1=osc1, psi_inf=psi_inf, psi_osc=psi_osc,
               EO=EO, EO_bound=EO_bound, P_O_ge=n_O_ge / ntot, P_A_le=n_A_le / ntot,
               n_implication_viol=n_implication_viol, P_hit0=n_hit0 / ntot,
               max_lower_viol=max_lower_viol, max_upper_viol=max_upper_viol, max_ident=max_ident,
               ratios=ratios, key=key, taus=taus, etas=etas, cases=cases,
               P_badG=[x / ntot for x in n_badG], P_badD=[x / ntot for x in n_badD], P_bad=[x / ntot for x in n_bad],
               sumS_exact=sumS_exact if exact else None, secs=time.time() - t0, probe=probe, K=K)
    return res


FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
    return "ok" if cond else "FAIL"


def report(res, verbose):
    n, u, r, L = res["n"], res["u"], res["r"], res["L"]
    m_r, R, V, K = res["m_r"], res["R"], res["V"], res["K"]
    tag = "n=%d u=%s r=%d L=%d" % (n, "ln2(exact)" if res["exact"] else "%g" % u, r, L)
    scale = max(R, 1e-300)
    key = res["key"]
    # (b) mean
    if res["exact"]:
        mean_ok = all(s == 0 for s in res["sumS_exact"])
        mean_str = "sum over all tuples of N^2*G_psi = %s (integers)" % (
            "0 for all psi" if mean_ok else str(res["sumS_exact"]))
    else:
        worst = float(np.abs(res["meanG"]).max())
        mean_ok = worst <= 1e-12 * scale
        mean_str = "max_psi |mean G_psi| = %.2e (R = %.3g)" % (worst, R)
    c_mean = check(mean_ok, tag + ": mean of G_psi not zero")
    # (b) oscillation
    osc = res["osc1"]
    c_o_lem = check(bool(np.all(osc <= 2 * res["psi_inf"] * m_r * (1 + 1e-12))), tag + ": osc > 2||psi|| m_r")
    c_o_thm = check(bool(np.all(osc <= 4 * m_r * (1 + 1e-12))), tag + ": osc > 4 m_r")
    c_o_ref = check(bool(np.all(osc <= res["psi_osc"] * m_r * (1 + 1e-12))), tag + ": osc > osc(psi) m_r (referee)")
    # (a)
    tol = 1e-12 * max(1.0, R)
    c_a1 = check(res["max_lower_viol"] <= tol, tag + ": A-1 < R - O_c")
    c_a2 = check(res["max_upper_viol"] <= tol, tag + ": A-1 > R")
    c_a3 = check(res["EO"] <= res["EO_bound"] * (1 + 1e-12) + 1e-300, tag + ": E O_c > bound")
    # (c)
    c_id = check(res["max_ident"] <= 1e-12, tag + ": identity bias = G/A")
    # (d)
    rat = res["ratios"]
    c_t4 = check(float(rat["4m_" + key][:, 0].max()) <= 1.0, tag + ": tail > McDiarmid with d = 4 m_r")
    c_t2 = check(float(rat["2m_" + key][:, 0].max()) <= 1.0, tag + ": tail > McDiarmid with d = 2 m_r (referee)")
    c_to = check(float(rat["osc_" + key][:, 0].max()) <= 1.0, tag + ": tail > McDiarmid with the exact oscillation")
    # (e)
    c_e1 = check(res["P_O_ge"] <= (L - 1) * V / (1 << n) + 1e-15, tag + ": P(O>=R/2) > (L-1)V/2^n")
    c_e2 = check(res["n_implication_viol"] == 0, tag + ": O<R/2 but A-1<=R/2")
    print("%-28s tuples=%-9d m_r=%.5g R=%.5g V=%d eta''=%.4g  [%.1fs]" % (tag, res["ntot"], m_r, R, V, res["eta2"], res["secs"]))
    print("   (a) max[(R-O_c)-(A-1)] = %+.2e %s; max[(A-1)-R] = %+.2e %s; E O_c = %.5g <= %.5g %s (ratio %.3f)" % (
        res["max_lower_viol"], c_a1, res["max_upper_viol"], c_a2, res["EO"], res["EO_bound"], c_a3,
        res["EO"] / res["EO_bound"] if res["EO_bound"] > 0 else float("nan")))
    print("   (b) %s %s; one-centre oscillation / m_r: max over psi = %.4f  [<= 2||psi|| %s, <= 4 %s, <= osc(phi) (referee) %s]" % (
        mean_str, c_mean, float((osc / m_r).max()), c_o_lem, c_o_thm, c_o_ref))
    print("   (c) max |bias - G/A| = %.1e %s" % (res["max_ident"], c_id))
    print("   (d) sup_t P(|G|>=t)/McDiarmid (%s; all t | only t where the bound is < 1): d=4m_r: %.4f | %.4f %s; d=2m_r: %.4f | %.4f %s; d=exact osc: %.4f | %.4f %s" % (
        key, float(rat["4m_" + key][:, 0].max()), float(rat["4m_" + key][:, 1].max()), c_t4,
        float(rat["2m_" + key][:, 0].max()), float(rat["2m_" + key][:, 1].max()), c_t2,
        float(rat["osc_" + key][:, 0].max()), float(rat["osc_" + key][:, 1].max()), c_to))
    hit_exact = 1.0 - (1.0 - V / (1 << n)) ** L
    c_e3 = check(abs(res["P_hit0"] - hit_exact) < 1e-12 and res["P_hit0"] <= res["eta2"] + 1e-15, tag + ": hitting probability")
    print("   (e) P(O_c>=R/2) = %.5g <= (L-1)V/2^n = %.5g %s; P(A-1<=R/2) = %.5g; [O_c<R/2 => A-1>R/2] %s; P(w_c(x0)!=1) = %.5g = 1-(1-V/2^n)^L <= eta'' %s" % (
        res["P_O_ge"], (L - 1) * V / (1 << n), c_e1, res["P_A_le"], c_e2, res["P_hit0"], c_e3))
    for (cst, eta), tau, pg, pd, pb in zip(res["cases"], res["taus"], res["P_badG"], res["P_badD"], res["P_bad"]):
        if tau <= 1.0:
            c_f1 = check(pg <= eta + 1e-15, tag + ": P(exists |G|>tau) > eta (C=%g)" % cst)
            c_f2 = check(pb <= eta + res["eta2"] + 1e-15, tag + ": P(not good) > eta + eta'' (C=%g)" % cst)
            print("   (f) C=%g M=%d eta=%.2f tau=%.4f eps=%.4f: P(exists i |G_i|>tau) = %.3g <= eta %s; P(exists i |bias_i|>tau) = %.3g; "
                  "P(not good) = %.5g <= eta+eta'' = %.4g %s" % (cst, K, eta, tau, math.log1p(R / 2), pg, c_f1, pd, pb, eta + res["eta2"], c_f2))
        else:
            print("   (f) C=%g M=%d eta=%.2f: least tau allowed = %.3f > 1 -- hypotheses of Theorem A' cannot be met here" % (cst, K, eta, tau))
    if verbose:
        print("       %-11s %10s %10s %10s %9s %9s %19s %19s" % (
            "phi", "mean G", "sd G/m_r", "max|G|/R", "osc/m_r", "osc(phi)", "ratio d=4m (all|nt)", "ratio d=2m (all|nt)"))
        for k, nm in enumerate(res["names"]):
            print("       %-11s %+10.1e %10.4f %10.4f %9.4f %9.4f %9.4f | %7.4f %9.4f | %7.4f" % (
                nm, res["meanG"][k], res["sdG"][k] / m_r, res["maxabsG"][k] / scale, osc[k] / m_r, res["psi_osc"][k],
                rat["4m_" + key][k, 0], rat["4m_" + key][k, 1], rat["2m_" + key][k, 0], rat["2m_" + key][k, 1]))


def cross_check_bruteforce():
    """the vectorised block enumeration against a pure-Python brute force (independent indexing)."""
    print("== cross-check of the vectorised enumeration against a pure-Python brute force ==")
    for (n, u, r, L) in ((3, 1.0, 2, 3), (3, 0.7, 1, 4), (4, 1.3, 2, 2), (3, 2.0, 3, 2), (4, 1.0, 3, 1)):
        res = run_config(n, u, r, L, exact=False, cross_check=True)
        obs = observables(n, r, 20261128, False)
        bf = brute_force(n, u, r, L, [p for _, p in obs])
        worst = 0.0
        for c, (a1, o, g) in bf.items():
            pa, po, pg = res["probe"][c]
            worst = max(worst, abs(pa - a1), abs(po - o), float(np.abs(pg - np.array(g)).max()))
        st = check(worst < 1e-12 and len(bf) == res["ntot"], "cross-check n=%d r=%d L=%d" % (n, r, L))
        print("   n=%d u=%g r=%d L=%d: %d tuples, max |vectorised - brute force| over (A-1, O_c, all G_psi) = %.1e %s" % (
            n, u, r, L, len(bf), worst, st))


def main():
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    print("a1_enum.py -- referee A1 -- exact enumeration over all tuples of centres")
    print("numpy %s; grid thresholds %d; 'exact' ratio = sup over the atoms of |G|; 'grid' ratio = conservative upper bound" % (np.__version__, KT))
    print()
    cross_check_bruteforce()
    print()
    cfgs = []
    # floating point, several slopes
    for n in (4,):
        for u in (0.25, 1.0, 2.0):
            for r in (1, 2, 3):
                for L in (1, 2, 3, 4):
                    cfgs.append((n, u, r, L, False))
    for n in (5,):
        for u in (0.25, 1.0):
            for r in (1, 2, 3):
                for L in (1, 2, 3, 4):
                    cfgs.append((n, u, r, L, False))
    for u in (0.25, 1.0):
        for r in (1, 2, 3):
            for L in (1, 2, 3):
                cfgs.append((6, u, r, L, False))
    # exact integers, u = ln 2
    for n in (4, 5):
        for r in (1, 2, 3):
            for L in (1, 2, 3, 4):
                cfgs.append((n, LN2, r, L, True))
    for r in (1, 2, 3):
        for L in (1, 2, 3):
            cfgs.append((6, LN2, r, L, True))
    big = [(6, 1.0, 2, 4, False), (6, 0.25, 2, 4, False), (6, 1.0, 1, 4, False), (6, 0.25, 3, 4, False),
           (6, LN2, 2, 4, True), (6, LN2, 3, 4, True), (6, LN2, 1, 4, True)]
    if quick:
        cfgs = [c for c in cfgs if c[0] <= 4]
        big = []
    print("== all tuples, n <= 6, L <= 4 ==")
    for (n, u, r, L, exact) in cfgs + big:
        res = run_config(n, u, r, L, exact)
        report(res, verbose=(n == 6 and L >= 3) or (n == 5 and L == 4 and r == 2))
        sys.stdout.flush()
    print()
    print("configurations: %d;  failed checks: %d" % (len(cfgs) + len(big), len(FAILS)))
    for f in FAILS:
        print("   FAIL: " + f)


if __name__ == "__main__":
    main()
