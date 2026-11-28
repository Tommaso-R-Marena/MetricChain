#!/usr/bin/env python3
"""Referee replication 4: the sampling part of Theorem E on a small cube (independent code).

Instances: w_K = 1 + max_{j<=K} e_r(. + c_j), centres independent and uniform.  Monte Carlo over instances,
everything else exact (sums over all 2^n points; Walsh-Hadamard transforms for convolutions).

Part A  E[TV(mu_w, ideal mixture)] <= 2 K V/2^n  (the claim after Lemma 2.5(iii) in the proof of Theorem E);
        P(O_1 > R/4) <= 8 K V/2^n for 2K centres;  A(w_0) <= 1 + R,  A(w_1) >= 1 + 2R - O_1.
Part B  two samples (m = 2), with the algorithm also seeing whether each sample is on the floor (w = 1):
        the law of (x_1 + x_2, floor flags) averaged over instances, for K and for 2K dips.  Its total-variation
        distance (a coarsening of what an algorithm sees from the samples and their values) must be at most
        the 'bad sampling' probabilities of the proof:
        [m/(1+R) + C(m,2)/K + m E TV_0] + [m/(1+2R) + C(m,2)/(2K) + m E TV_1] + (values at the samples) m K V/2^n.
Part C  the same quantities in the IDEAL model computed in closed form (floor / same dip / different dips),
        to see which term the difference comes from.
Run: python3 -B r4_samples.py
"""
import math
import numpy as np

rng = np.random.default_rng(7)


def wht(a):
    """unnormalised Walsh-Hadamard transform along axis 0 (length 2^n)."""
    a = a.copy()
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(N // (2 * h), 2, h)
        a = np.stack([a[:, 0, :] + a[:, 1, :], a[:, 0, :] - a[:, 1, :]], axis=1).reshape(N)
        h *= 2
    return a


def conv(f, g):
    """(f*g)(z) = sum_x f(x) g(x+z) on Z_2^n."""
    return wht(wht(f) * wht(g)) / f.shape[0]


def run(n, u, r, K, ninst):
    N = 1 << n
    x = np.arange(N)
    PC = np.zeros(N, dtype=np.int64)
    for i in range(n):
        PC += (x >> i) & 1
    er = np.maximum(np.exp(u * (r - PC)) - 1.0, 0.0)
    m_r = er.mean()
    V = sum(math.comb(n, j) for j in range(r))
    # exact expected overlap of one pair of independent uniform centres: E_z E_pi min(e_r, e_r(.+z))
    # = 2^-n sum_z 2^-n sum_x min(e(x), e(x+z)); only x, x+z in the ball matter
    ball = np.nonzero(er > 0)[0]
    pair_exact = 0.0
    for b1 in ball:
        pair_exact += np.minimum(er[b1], er[ball]).sum()
    pair_exact /= N * N
    shell = [PC == d for d in range(n + 1)]
    cnt = np.array([math.comb(n, d) for d in range(n + 1)], dtype=float)
    out = {}
    for label, KK in (("K", K), ("2K", 2 * K)):
        R = KK * m_r
        tvs, Os, Aex = [], [], []
        acc = np.zeros((3, n + 1))            # shell sums of the pair law, by floor flags (FF, FD+DF, DD)
        half = [np.zeros((3, n + 1)), np.zeros((3, n + 1))]
        for it in range(ninst):
            cs = rng.integers(N, size=KK)
            mx = np.zeros(N)
            sm = np.zeros(N)
            srt_sum = np.zeros(N)
            # O_c = sum_{j<j'} E min(e_j, e_j') ; computed from sorted values would need all K arrays;
            # use the identity sum_{j<j'} min(a_j,a_j') = sum_k (k-1) a_(k) through a running top-2 trick is not exact,
            # so keep all arrays (K <= 64 here, 2^14 points: fine).
            es = np.empty((KK, N))
            for j, c in enumerate(cs):
                es[j] = er[x ^ c]
            mx = es.max(axis=0)
            sm = es.sum(axis=0)
            nzcols = np.nonzero((es > 0).sum(axis=0) >= 2)[0]          # only points covered at least twice contribute
            O = 0.0
            if nzcols.size:
                sub = -np.sort(-es[:, nzcols], axis=0)
                O = float((sub * np.arange(KK)[:, None]).sum()) / N
            w = 1.0 + mx
            mu = w / w.sum()
            ideal = (1.0 + sm) / (N * (1 + R))
            tvs.append(0.5 * np.abs(mu - ideal).sum())
            Os.append(O)
            Aex.append(w.mean() - 1.0)
            floor = (mx == 0.0)
            muF = np.where(floor, mu, 0.0)
            muD = mu - muF
            cFF, cFD, cDD = conv(muF, muF), 2 * conv(muF, muD), conv(muD, muD)
            contrib = np.array([[c_[s].sum() for s in shell] for c_ in (cFF, cFD, cDD)])
            acc += contrib
            half[it % 2] += contrib
        out[label] = dict(R=R, ETV=float(np.mean(tvs)), Os=np.array(Os), Aex=np.array(Aex),
                          law=acc / ninst, half=[h / (ninst / 2) for h in half], KK=KK)
    print(f"n={n} u={u} r={r} K={K}: m_r={m_r:.5f} V(n,r-1)={V} R=K m_r={K*m_r:.3f}  N*=2^n/(K V)={N/(K*V):.1f}  ({ninst} instances each)")
    for label in ("K", "2K"):
        o = out[label]
        KK = o["KK"]
        print(f"   Part A [{label} centres]: E TV(mu_w, ideal) = {o['ETV']:.5f} <= 2 K_i V/2^n = {2*KK*V/N:.5f} : {o['ETV'] <= 2*KK*V/N}"
              f";  E O = {o['Os'].mean():.5f} +- {o['Os'].std(ddof=1)/math.sqrt(len(o['Os'])):.5f} (s.e.), exact value C(K_i,2)*pair = {math.comb(KK,2)*pair_exact:.5f}"
              f" <= C(K_i,2) m_r V/2^n = {math.comb(KK,2)*m_r*V/N:.5f} : {math.comb(KK,2)*pair_exact <= math.comb(KK,2)*m_r*V/N*(1+1e-12)}"
              f";  all: K_i m_r - O <= A-1 <= K_i m_r : {bool(np.all(o['Aex'] <= KK*m_r + 1e-9) and np.all(o['Aex'] >= KK*m_r - o['Os'] - 1e-9))}")
    R = K * m_r
    o1 = out["2K"]
    frac = float(np.mean(o1["Os"] > R / 4))
    print(f"   Part A: P(O_1 > R/4) = {frac:.4f} <= 8 K V/2^n = {8*K*V/N:.4f} : {frac <= 8*K*V/N + 0.02}")
    tv = 0.5 * np.abs(out["K"]["law"] - out["2K"]["law"]).sum()
    noise = max(0.5 * np.abs(out[l]["half"][0] - out[l]["half"][1]).sum() for l in ("K", "2K"))
    m = 2
    bound = (m / (1 + R) + 1 / K + m * out["K"]["ETV"]) + (m / (1 + 2 * R) + 1 / (2 * K) + m * out["2K"]["ETV"]) + m * K * V / N
    print(f"   Part B (m=2): TV between the laws of (x1+x2, floor flags) under K and 2K dips = {tv:.5f}  "
          f"(Monte-Carlo noise floor, half-sample against half-sample: {noise:.5f})")
    print(f"           bound from the proof (bad sampling in either experiment + values) = {bound:.5f} : {tv <= bound + noise}")
    # Part C: ideal model in closed form.  floor prob f_i = 1/(1+R_i); two dip samples share a dip w.p. 1/K_i.
    tot = 0.0
    parts = []
    for (Ri, Ki) in ((R, K), (2 * R, 2 * K)):
        f = 1 / (1 + Ri)
        parts.append((f * f, 2 * f * (1 - f), (1 - f) ** 2 * (1 - 1 / Ki), (1 - f) ** 2 / Ki))
    # classes: FF (uniform difference), FD (uniform), DD-different (uniform), DD-same (law of z1+z2, concentrated near 0)
    ideal_tv = 0.5 * (abs(parts[0][0] - parts[1][0]) + abs(parts[0][1] - parts[1][1])
                      + abs(parts[0][2] - parts[1][2]) + abs(parts[0][3] - parts[1][3]))
    print(f"   Part C: ideal model, TV of (class of the pair) = {ideal_tv:.5f}  [FF, FD, DD-different, DD-same] K: "
          + ", ".join(f"{v:.5f}" for v in parts[0]) + " ; 2K: " + ", ".join(f"{v:.5f}" for v in parts[1]))
    return out


if __name__ == "__main__":
    run(14, 6.0, 2, 20, 300)
    run(14, 5.0, 2, 32, 300)
    run(13, 6.0, 1, 40, 300)
    # a regime closer to the hypotheses of the theorem for m = 1..2 (needles, r = 1): eta_1 = 1/40, K = 160
    run(15, 12.5, 1, 64, 120)
