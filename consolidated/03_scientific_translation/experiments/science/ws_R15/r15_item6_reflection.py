#!/usr/bin/env python3
"""R15, Item 6 -- the outline for the conjecture of Proposition 11.18e(b')(ii) (theory report at f7df44f): the
reflection ("pairing") on the cube at order two.  Own code, written from the outline; exact arithmetic where the
statement is combinatorial, log-space floating point where it is about the prior density.

Setting.  h(s) = alpha + beta.s on {-1,1}^n.  Q = n affinely independent points of the cube; nu spans the kernel of the
differences x^j - x^1 (one hidden direction).  x* = -sign(beta).  S: nu.x* = nu.x^1.  Pairing: k = argmin over supp(nu) of
|beta_k/nu_k|, t = -2 beta_k/nu_k, beta' = beta + t nu, alpha' = alpha - t nu.x^1.
For i in supp(nu), i != k put r_i = |beta_i/nu_i| / |beta_k/nu_k| >= 1.  Then beta'_i = beta_i (1 + d_i) with |d_i| = 2/r_i.

PART 1  on which event do the combinatorial claims hold EXACTLY?  Claim of this review: on {r_i > 3 for all i != k}
        (the smallest scaled magnitude is more than three times smaller than every other one): same transcript, the
        signs of beta' are those of beta except at k, the map is an involution, and S and S' never both hold.  With
        2 < r_i <= 3 the involution can fail; with r_i <= 2 a second sign can flip.  Tested in exact arithmetic.
PART 2  the prior density.  Log-uniform magnitudes on [e^l0, e^(l0 + Lam)], independent signs: the density ratio
        pi(beta')/pi(beta) is prod_{i != k} 1/|1 + d_i| (the Jacobian is 1 in absolute value).  How often is it within
        e^(+-eps) of 1, how often does beta' leave the support of the prior, as functions of the range Lam?
        Prediction: the scaled log-magnitudes are (nearly) independent uniforms on an interval of length Lam, so the gap
        between the two smallest of d = |supp nu| of them is below x with probability 1 - (1 - x/Lam)^d ~ d x/Lam.
PART 3  the frequency of S under the prior for random Q (at most 1/2 up to noise), and exactly 1/2 for a coordinate
        direction; ln Z against the minimum: ln Z = -alpha + sum |beta_i| + sum ln(1 + e^{-2|beta_i|}) exactly.

Run:  OMP_NUM_THREADS=1 python3 r15_item6_reflection.py > logs/item6_reflection.log
"""
import itertools, math, random, resource, time
from fractions import Fraction as Fr
import numpy as np

t0 = time.time()
ok_all = True


def check(cond, msg):
    global ok_all
    if not cond:
        ok_all = False
        print("   !!! CHECK FAILED:", msg)


def kernel(rows, n):
    """integer vector spanning the kernel of the rows if the rank is n - 1, else None (exact, Fractions)"""
    M = [[Fr(v) for v in r] for r in rows]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        M[r] = [v / M[r][c] for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    if r != n - 1:
        return None
    free = next(c for c in range(n) if c not in piv)
    nu = [Fr(0)] * n
    nu[free] = Fr(1)
    for i, c in enumerate(piv):
        nu[c] = -M[i][free]
    den = math.lcm(*[v.denominator for v in nu])
    return [int(v * den) for v in nu]


def random_Q(rng, n):
    cube = list(itertools.product((-1, 1), repeat=n))
    while True:
        Q = rng.sample(cube, n)
        nu = kernel([[(a - b) // 2 for a, b in zip(x, Q[0])] for x in Q[1:]], n)
        if nu is not None:
            return Q, nu


print("PART 1  exact arithmetic: on which event do the combinatorial claims hold?")
rng = random.Random(606)
cls = {"r > 3": dict(n=0, transcript=0, signs=0, invol=0, SS=0), "2 < r <= 3": dict(n=0, transcript=0, signs=0, invol=0, SS=0),
       "r <= 2": dict(n=0, transcript=0, signs=0, invol=0, SS=0)}
for n in range(2, 8):
    for qi in range(25):
        Q, nu = random_Q(rng, n)
        supp = [i for i in range(n) if nu[i] != 0]
        for _ in range(400):
            # magnitudes over a SHORT range on purpose (Lam = 6), so that all three classes are populated
            beta = [rng.choice((-1, 1)) * int(math.exp(12.0 + rng.random() * 6.0)) for _ in range(n)]
            alpha = rng.randrange(-10 ** 12, 10 ** 12)
            k = min(supp, key=lambda i: abs(Fr(beta[i], nu[i])))
            rmin = min([abs(Fr(beta[i], nu[i])) / abs(Fr(beta[k], nu[k])) for i in supp if i != k], default=None)
            if rmin is None:
                key = "r > 3"                                  # a coordinate direction: nothing else moves
            else:
                key = "r > 3" if rmin > 3 else ("2 < r <= 3" if rmin > 2 else "r <= 2")
            t = Fr(-2 * beta[k], nu[k])
            beta2 = [Fr(beta[i]) + t * nu[i] for i in range(n)]
            alpha2 = Fr(alpha) - t * sum(nu[i] * Q[0][i] for i in range(n))
            h = lambda x: alpha + sum(b * s for b, s in zip(beta, x))
            h2 = lambda x: alpha2 + sum(b * s for b, s in zip(beta2, x))
            st = cls[key]
            st["n"] += 1
            st["transcript"] += int(any(h(x) != h2(x) for x in Q))
            signs_ok = all((beta2[i] > 0) == (beta[i] > 0) and beta2[i] != 0 for i in range(n) if i != k) and beta2[k] == -beta[k]
            st["signs"] += int(not signs_ok)
            if all(b != 0 for b in beta2):
                k2 = min(supp, key=lambda i: abs(beta2[i] / nu[i]))
                t2 = -2 * beta2[k2] / nu[k2]
                back = [beta2[i] + t2 * nu[i] for i in range(n)]
                st["invol"] += int(not (back == [Fr(b) for b in beta]))
            else:
                st["invol"] += 1
            xs = [-1 if b > 0 else 1 for b in beta]
            xs2 = [-1 if b > 0 else 1 for b in beta2]
            base = sum(nu[i] * Q[0][i] for i in range(n))
            S1 = sum(nu[i] * xs[i] for i in range(n)) == base
            S2 = sum(nu[i] * xs2[i] for i in range(n)) == base
            st["SS"] += int(S1 and S2)
for key, st in cls.items():
    print(f"   class {key:10s}: {st['n']:6d} draws; violations: same transcript {st['transcript']}, signs kept except at k {st['signs']}, involution {st['invol']},"
          f" S and S' both {st['SS']}")
check(all(cls["r > 3"][v] == 0 for v in ("transcript", "signs", "invol", "SS")) and cls["r > 3"]["n"] > 5000, "claims fail on r > 3")
check(cls["2 < r <= 3"]["signs"] == 0 and cls["2 < r <= 3"]["invol"] > 0 and cls["r <= 2"]["signs"] > 0, "thresholds 2 and 3 not seen")
print("   => exact on {r > 3}; for 2 < r <= 3 the signs are still kept but the map need not be an involution; for r <= 2 a second sign can flip.")

print("PART 2  the density ratio under the log-uniform prior (log-space; 40 sets Q x 5000 draws per cell)")
nprng = np.random.default_rng(606)
print(f"   {'n':>2} {'Lam':>6} | {'mean d':>6} | {'P(r<=3)':>8} {'pred':>8} | {'P(|ln ratio|>1)':>15} {'P(>0.1)':>8} {'pred':>8} {'P(>0.01)':>9} {'pred':>8} | {'P(beta_ leaves support)':>23} | {'P(all pairs 1e4 cmax apart)':>27}")
for n in (2, 4, 7):
    Qs = [random_Q(rng, n) for _ in range(40)]
    for Lam in (20.0, 60.0, 200.0, 1000.0, 5000.0):
        acc = dict(r3=0, e1=0, e01=0, e001=0, out=0, sep=0, N=0, p3=0.0, p01=0.0, p001=0.0, d=0.0)
        for Q, nu in Qs:
            nu = np.array(nu, float)
            supp = np.flatnonzero(nu != 0)
            d = len(supp)
            N = 5000
            Lmag = nprng.uniform(0.0, Lam, size=(N, n))                         # log-magnitudes minus l0
            sg = nprng.choice([-1.0, 1.0], size=(N, n))
            Msc = Lmag[:, supp] - np.log(np.abs(nu[supp]))[None, :]             # scaled log-magnitudes
            kk = Msc.argmin(axis=1)
            Mk = Msc[np.arange(N), kk]
            lr = Msc - Mk[:, None]                                              # ln r_i >= 0, zero at k
            with np.errstate(over="ignore"):
                dlt = 2.0 * np.exp(-lr)                                         # |d_i|
            sgn_d = -sg[:, supp] * sg[np.arange(N), supp[kk]][:, None] * np.sign(nu[supp])[None, :] * np.sign(nu[supp[kk]])[:, None]
            one = 1.0 + sgn_d * dlt
            mask = np.ones_like(one, bool); mask[np.arange(N), kk] = False
            with np.errstate(divide="ignore"):
                lnabs = np.where(mask, np.log(np.abs(one)), 0.0)
            lnratio = -lnabs.sum(axis=1)                                        # ln of pi(beta')/pi(beta) inside the support
            rmin = np.where(mask, lr, np.inf).min(axis=1) if d > 1 else np.full(N, np.inf)
            newL = Lmag[:, supp] + lnabs                                        # log-magnitudes of beta' (minus l0); k unchanged
            out = ((newL < 0) | (newL > Lam)).any(axis=1)
            cmax = float(np.max(np.abs(nu[supp])) / np.min(np.abs(nu[supp])))
            srt = np.sort(Lmag, axis=1)
            sep = (np.diff(srt, axis=1) >= math.log(1e4 * cmax)).all(axis=1)
            acc["N"] += N; acc["r3"] += int((rmin <= math.log(3)).sum()); acc["e1"] += int((np.abs(lnratio) > 1).sum())
            acc["e01"] += int((np.abs(lnratio) > 0.1).sum()); acc["e001"] += int((np.abs(lnratio) > 0.01).sum()); acc["out"] += int(out.sum())
            acc["sep"] += int(sep.sum()); acc["d"] += d * N
            pr = lambda x: (1 - (1 - min(x / Lam, 1.0)) ** d) if d > 1 else 0.0   # gap between the two smallest of d uniforms below x
            acc["p3"] += N * pr(math.log(3)); acc["p01"] += N * pr(math.log(2 / 0.1)); acc["p001"] += N * pr(math.log(2 / 0.01))
        N = acc["N"]
        print(f"   {n:>2} {Lam:>6.0f} | {acc['d'] / N:>6.2f} | {acc['r3'] / N:>8.4f} {acc['p3'] / N:>8.4f} | {acc['e1'] / N:>15.4f} {acc['e01'] / N:>8.4f} {acc['p01'] / N:>8.4f} "
              f"{acc['e001'] / N:>9.4f} {acc['p001'] / N:>8.4f} | {acc['out'] / N:>23.5f} | {acc['sep'] / N:>27.4f}")
print("   'pred' = 1 - (1 - x/Lam)^d with x = ln 3, ln(2/0.1), ln(2/0.01): the exceptional sets shrink like d ln(.)/Lam -- like 1/log of the dynamic range of the prior")

print("PART 3  frequency of S under the prior, and ln Z against the minimum")
rng2 = random.Random(77)
worst = 0.0
for n in range(2, 8):
    freqs = []
    for qi in range(20):
        if qi == 0:
            Q = [tuple([1] * n)] + [tuple(-1 if j == i else 1 for j in range(n)) for i in range(n - 1)]
            nu = kernel([[(a - b) // 2 for a, b in zip(x, Q[0])] for x in Q[1:]], n)
        else:
            Q, nu = random_Q(rng2, n)
        base = sum(nu[i] * Q[0][i] for i in range(n))
        N = 4000
        sg = nprng.choice([-1, 1], size=(N, n))                                 # S depends on the signs only
        xs = -sg
        Sfreq = float(((xs @ np.array(nu)) == base).mean())
        freqs.append(Sfreq)
        if qi == 0:
            check(abs(Sfreq - 0.5) < 4 * 0.5 / math.sqrt(N), "coordinate direction: frequency of S is not 1/2")
    worst = max(worst, max(freqs))
    print(f"   n = {n}: frequency of S over 20 sets Q (4000 draws each; one standard error 0.008): least {min(freqs):.3f}, largest {max(freqs):.3f}; coordinate direction {freqs[0]:.3f}")
check(worst < 0.5 + 4 * 0.008, "frequency of S above 1/2")
# S depends on the SIGNS only; exact probability of S by enumeration of the 2^n sign patterns for a few Q
exact_max = 0.0
for n in range(2, 8):
    for qi in range(30):
        Q, nu = random_Q(rng2, n)
        base = sum(nu[i] * Q[0][i] for i in range(n))
        cnt = sum(1 for xs in itertools.product((-1, 1), repeat=n) if sum(nu[i] * xs[i] for i in range(n)) == base)
        exact_max = max(exact_max, cnt / 2 ** n)
print(f"   S depends on the signs of beta only, so P(S) is the fraction of cube points x with nu.x = nu.x^1: exactly, over 180 random Q, the largest is {exact_max:.4f}")
check(exact_max <= 0.5 + 1e-12, "exact P(S) above 1/2")
for _ in range(5):
    n = 6
    beta = nprng.normal(0, 3, n); alpha = float(nprng.normal())
    Z = sum(math.exp(-(alpha + float(np.dot(beta, s)))) for s in itertools.product((-1, 1), repeat=n))
    rhs = -alpha + float(np.abs(beta).sum()) + float(np.log1p(np.exp(-2 * np.abs(beta))).sum())
    check(abs(math.log(Z) - rhs) < 1e-9, "ln Z formula")
print("   ln Z = -alpha + sum |beta_i| + sum ln(1 + e^(-2|beta_i|)) (exact; checked): |ln Z + min h| <= n e^(-2 min|beta_i|)")

print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
print(f"seconds {time.time() - t0:.1f}")
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
