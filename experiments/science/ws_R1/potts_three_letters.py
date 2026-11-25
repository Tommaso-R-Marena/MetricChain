#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- the remark "more than two letters: the comparison fails" of section 11.25: own replication.

Claims (theory report, remark after Corollary 11.91):
 (R1) for the Potts pair P(b,x) ~ a_b c_x exp(s 1[b=x]) the uniform marginals do NOT maximise I(s) when q >= 3;
      to second order I(s) ~ s^2 (k-1)/(2 k^2) for the uniform law on k letters (largest for k = 2);
 (R2) numerically the maximum over both marginals is attained by the uniform law on k*(s) letters,
      k* = 2 for s < 0.5194, 3 up to 1.3353, then 4   (q = 3, 4);
 (R3) the game function of a centre on a composition class is  t u int_{tu}^{u} I(s) s^-2 ds;
 (R4) uniform k-ary cubes: R_2(0) > R_3(0) for u < ln 2 (exact crossing; optimal mismatch fractions 2 - log2(3) and
      log2(3) - 1), R_3(0) > R_4(0) for u < ln 6; values 0.007673, 0.007425, 0.006552 at u = 0.5 and
      0.029139, 0.030654, 0.028405 at u = 1.
What is computed here, with own code:
 (a) closed forms I_k(s), thresholds, second-order coefficients (mpmath);
 (b) maximisation of the Potts-pair mutual information over BOTH marginals for q = 3, 4, 5 by multistart local
     optimisation (the table is built by Sinkhorn scaling from free row/column weights, so every q x q positive
     table of Potts form is reachable; sub-alphabets are reachable as limits);
 (c) the integral identity for random marginals (q = 3), with Psi computed by an independent convex optimisation;
 (d) R_k(0) from the game function AND from its definition as sup over shells of min over exits;
     the two crossings by root finding;
 (e) the referee's second-order (small-u) argument: the residual variance of 1[b=x] under a x c;
 (f) a finite-n illustration with exact sums: the lower bound of Theorem 11.76(b)/11.78(a) for balls in the
     uniform ternary cube against balls in the binary slice 1/2 (same n, u = 0.5).
Run:  python3 potts_three_letters.py
"""
import math
import sys

import mpmath as mp
import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import gammaln, logsumexp

mp.mp.dps = 30


# ------------------------------------------------------------------------------------------------
def I_unif(k, s):
    """mutual information of the Potts pair with both marginals uniform on k letters, slope s"""
    Z = math.exp(s) + k - 1
    return math.log(k) - math.log(Z) + s * math.exp(s) / Z


def Psi_k(k, s):
    """max_l [s l - F_k(l)],  F_k(l) = ln k - h(rho) - rho ln(k-1),  rho = (k-1)/k - l  (mismatch fraction)"""
    return math.log((math.exp(s) + k - 1) / k) - s / k


def F_k(k, rho):
    h = -(rho * math.log(rho) if rho > 0 else 0.0) - ((1 - rho) * math.log(1 - rho) if rho < 1 else 0.0)
    return math.log(k) - h - rho * math.log(k - 1)


def R_k_game(k, u, e=0.0):
    f = lambda t: -(t * Psi_k(k, u) - Psi_k(k, t * u) - t * e)
    r = minimize_scalar(f, bounds=(0, 1), method="bounded", options={"xatol": 1e-14})
    return -r.fun


def R_k_closed(k, u, e=0.0):
    return F_k(k, (k - 1) / k - max(Psi_k(k, u) - e, 0.0) / u)


def R_k_definition(k, u, e=0.0, n=20001):
    """sup over shells rho (mismatch fraction to the centre) of min{F_k(rho'): u |rho' - rho| <= e + F_k(rho)};
    brute force on a grid, then polished.  (Single-centre shells of the uniform k-ary cube; density = uniform measure.)"""
    typ = (k - 1) / k

    def r_shell(rho):
        w = (e + F_k(k, rho)) / u
        if w < 0:
            return -1.0
        lo, hi = max(rho - w, 0.0), min(rho + w, 1.0)
        if lo <= typ <= hi:
            return 0.0
        rr = minimize_scalar(lambda x: F_k(k, x), bounds=(lo, hi), method="bounded", options={"xatol": 1e-15})
        return min(rr.fun, F_k(k, lo), F_k(k, hi))

    rhos = np.linspace(1e-9, 1 - 1e-9, 2001)
    vals = [r_shell(float(r)) for r in rhos]
    i = int(np.argmax(vals))
    rr = minimize_scalar(lambda x: -r_shell(x), bounds=(rhos[max(i - 1, 0)], rhos[min(i + 1, 2000)]), method="bounded",
                         options={"xatol": 1e-15})
    return max(vals[i], -rr.fun)


# ------------------------------------------------------------------------------------------------
def sinkhorn_table(a, c, s, iters=5000, tol=1e-15):
    """the Potts pair with marginals (a, c) and slope s:  P = diag(x) K diag(y), K = exp(s I)"""
    q = len(a)
    K = np.ones((q, q)) + (math.exp(s) - 1.0) * np.eye(q)
    x = np.ones(q)
    y = np.ones(q)
    for _ in range(iters):
        x_new = a / (K @ y)
        y_new = c / (K.T @ x_new)
        if max(np.max(np.abs(x_new - x) / x_new), np.max(np.abs(y_new - y) / y_new)) < tol:
            x, y = x_new, y_new
            break
        x, y = x_new, y_new
    return (x[:, None] * K) * y[None, :]


def mi_table(P):
    pb = P.sum(1, keepdims=True)
    px = P.sum(0, keepdims=True)
    m = P > 0
    return float(np.sum(P[m] * np.log(P[m] / (pb @ px)[m])))


def potts_free(params, q, s):
    """Potts-form table from free weights: P ~ alpha_b gamma_x exp(s 1[b=x]) (covers all Potts pairs)"""
    al = np.exp(params[:q] - np.max(params[:q]))
    ga = np.exp(params[q:] - np.max(params[q:]))
    P = np.outer(al, ga) * (np.ones((q, q)) + (math.exp(s) - 1.0) * np.eye(q))
    return P / P.sum()


def max_potts_mi(q, s, restarts, rng):
    best = (-1.0, None)
    for r in range(restarts):
        x0 = rng.normal(0, 1.5, 2 * q)
        if r < q:  # also start near sub-alphabets
            x0 = np.concatenate([np.where(np.arange(q) <= r, 0.0, -8.0)] * 2) + rng.normal(0, 0.05, 2 * q)
        res = minimize(lambda z: -mi_table(potts_free(z, q, s)), x0, method="BFGS", options={"gtol": 1e-11, "maxiter": 2000})
        if -res.fun > best[0]:
            best = (-res.fun, potts_free(res.x, q, s))
    return best


ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    sys.stdout.flush()


def main():
    rng = np.random.default_rng(2026)
    # ---------------- (a) closed forms, thresholds, second order ----------------
    s23 = brentq(lambda s: I_unif(2, s) - I_unif(3, s), 0.1, 2.0, xtol=1e-14)
    s34 = brentq(lambda s: I_unif(3, s) - I_unif(4, s), 0.5, 3.0, xtol=1e-14)
    s45 = brentq(lambda s: I_unif(4, s) - I_unif(5, s), 1.0, 4.0, xtol=1e-14)
    sec = []
    for k in (2, 3, 4, 5):
        Ik = lambda s: mp.log(k) - mp.log(mp.e ** s + k - 1) + s * mp.e ** s / (mp.e ** s + k - 1)
        c2 = mp.diff(Ik, 0, 2) / 2
        c3 = mp.diff(Ik, 0, 3) / 6
        sec.append((k, float(c2), (k - 1) / (2 * k * k), float(c3), (k - 1) * (k - 2) / (3 * k ** 3)))
    good = abs(s23 - 0.5194) < 5e-5 and abs(s34 - 1.3353) < 5e-5 and all(abs(a - b) < 1e-12 for _, a, b, _, _ in sec)
    report("(a) thresholds", good,
           f"I_2 = I_3 at s = {s23:.6f} (claimed 0.5194); I_3 = I_4 at s = {s34:.6f} (claimed 1.3353); I_4 = I_5 at s = {s45:.6f}; "
           "second-order coefficients I_k(s)/s^2 -> " + ", ".join(f"k={k}: {a:.6f} (=(k-1)/2k^2={b:.6f})" for k, a, b, _, _ in sec)
           + "; third-order coefficients " + ", ".join(f"k={k}: {c:.6f} (=(k-1)(k-2)/3k^3={d:.6f})" for k, _, _, c, d in sec))

    # ---------------- (b) maximisation over both marginals ----------------
    print("      max over both marginals of the Potts-pair MI (multistart BFGS on free weights):")
    print("        q    s      max found     best uniform-k value (k)     support of the maximiser (row marginal)")
    worst = 0.0
    kstar_ok = True
    for q, restarts in ((3, 40), (4, 40), (5, 30)):
        for s in (0.2, 0.45, 0.51, 0.53, 0.8, 1.2, 1.33, 1.34, 1.6, 2.5, 4.0):
            val, P = max_potts_mi(q, s, restarts, rng)
            cands = {k: I_unif(k, s) for k in range(2, q + 1)}
            kbest = max(cands, key=cands.get)
            row = np.sort(P.sum(1))[::-1]
            supp = int(np.sum(row > 1e-4))
            worst = max(worst, val - cands[kbest])
            kstar_ok &= (supp == kbest) and abs(val - cands[kbest]) < 1e-7
            print(f"        {q}  {s:5.2f}  {val:.9f}   {cands[kbest]:.9f} (k={kbest})        "
                  f"{supp} letters: " + ", ".join(f"{v:.4f}" for v in row))
    report("(b) Potts maximisation", kstar_ok and worst < 1e-7,
           f"in all cases the best table found is the uniform law on k*(s) letters and no table exceeds max_k I_k(s) "
           f"(largest excess {worst:.2e}); uniform marginals on all q letters are NOT maximal for s below the thresholds")

    # ---------------- (c) integral identity for general marginals ----------------
    err = 0.0
    for _ in range(12):
        q = 3
        a = rng.dirichlet(np.ones(q) * 3)
        c = rng.dirichlet(np.ones(q) * 3)
        u = float(rng.uniform(0.3, 2.5))
        t = float(rng.uniform(0.1, 0.9))

        def Psi(s):
            P = sinkhorn_table(a, c, s)
            return s * float(np.trace(P)) - mi_table(P) - s * float(np.sum(a * c)) * 0.0

        # Psi(s) := max over couplings of [s P(B=X) - I(P)]; the maximiser is the Potts pair.  The game function
        # uses l = P(B=X) - P_indep(B=X); the linear term drops out of t Psi(u) - Psi(tu).
        Fstar = t * Psi(u) - Psi(t * u)
        integrand = lambda s: mi_table(sinkhorn_table(a, c, float(s))) / float(s) ** 2
        from scipy.integrate import quad
        val, _ = quad(integrand, t * u, u, epsabs=1e-13, epsrel=1e-13)
        err = max(err, abs(Fstar - t * u * val))
        # independent check that the Sinkhorn table maximises s P(B=X) - I(P) among couplings (random perturbations)
        P = sinkhorn_table(a, c, u)
        base = u * np.trace(P) - mi_table(P)
        for _ in range(20):
            Dlt = rng.normal(0, 1, (q, q))
            Dlt -= Dlt.mean(0, keepdims=True)
            Dlt -= Dlt.mean(1, keepdims=True)
            Q = P + 1e-3 * Dlt * P.min()
            assert u * np.trace(Q) - mi_table(Q) <= base + 1e-12
    report("(c) integral identity", err < 1e-9, f"|t Psi(u) - Psi(tu) - t u int I/s^2| <= {err:.2e} for 12 random (a, c, u, t), q = 3")

    # ---------------- (d) uniform k-ary cubes ----------------
    claimed = {0.5: (0.007673, 0.007425, 0.006552), 1.0: (0.029139, 0.030654, 0.028405)}
    good = True
    for u in (0.5, 1.0):
        row = []
        for k in (2, 3, 4):
            g, c, d = R_k_game(k, u), R_k_closed(k, u), R_k_definition(k, u)
            good &= abs(g - c) < 1e-10 and abs(d - c) < 1e-9 and abs(c - claimed[u][k - 2]) < 6e-7
            row.append(f"R_{k}(0) = {c:.6f} (game {g:.6f}, sup-min {d:.6f}; claimed {claimed[u][k - 2]:.6f})")
        print(f"      u = {u}: " + "; ".join(row))
    u23 = brentq(lambda u: R_k_closed(2, u) - R_k_closed(3, u), 0.3, 1.5, xtol=1e-14)
    u34 = brentq(lambda u: R_k_closed(3, u) - R_k_closed(4, u), 0.8, 4.0, xtol=1e-14)
    rho2 = 0.5 - Psi_k(2, math.log(2)) / math.log(2)
    rho3 = 2 / 3 - Psi_k(3, math.log(2)) / math.log(2)
    good &= abs(u23 - math.log(2)) < 1e-10 and abs(u34 - math.log(6)) < 1e-10
    good &= abs(rho2 - (2 - math.log2(3))) < 1e-12 and abs(rho3 - (math.log2(3) - 1)) < 1e-12
    report("(d) k-ary cubes", good,
           f"R_2(0) = R_3(0) at u = {u23:.12f} (ln 2 = {math.log(2):.12f}); R_3(0) = R_4(0) at u = {u34:.12f} (ln 6 = {math.log(6):.12f}); "
           f"optimal mismatch fractions at u = ln 2: {rho2:.9f} (2 - log2 3 = {2 - math.log2(3):.9f}), {rho3:.9f} (log2 3 - 1 = {math.log2(3) - 1:.9f})")

    # ---------------- (e) second order: residual variance of 1[b=x] under a x c ----------------
    def resid_var(a, c):
        Sa = np.diag(a) - np.outer(a, a)
        Sc = np.diag(c) - np.outer(c, c)
        return float(np.sum(Sa * Sc))

    # check against I(s)/ (s^2/2) at small s
    e2 = 0.0
    for _ in range(10):
        a = rng.dirichlet(np.ones(3) * 3)
        c = rng.dirichlet(np.ones(3) * 3)
        s = 1e-3
        e2 = max(e2, abs(mi_table(sinkhorn_table(a, c, s)) / (s * s / 2) - resid_var(a, c)))
    # maximise the residual variance over (a, c) for q = 3, 4
    best = {}
    for q in (3, 4):
        bv = -1
        for _ in range(60):
            x0 = rng.normal(0, 2, 2 * q)
            f = lambda z: -resid_var(np.exp(z[:q]) / np.exp(z[:q]).sum(), np.exp(z[q:]) / np.exp(z[q:]).sum())
            res = minimize(f, x0, method="BFGS", options={"gtol": 1e-12})
            bv = max(bv, -res.fun)
        best[q] = bv
    report("(e) second order", e2 < 1e-3 and all(abs(v - 0.25) < 1e-8 for v in best.values()),
           f"I(s) = (s^2/2) * ||Sigma_a o Sigma_c||_1-type residual variance (checked to {e2:.1e} at s = 1e-3); its maximum over "
           f"both marginals is {best[3]:.9f} (q=3), {best[4]:.9f} (q=4) = 1/4, the two-letter value; uniform on 3 letters gives "
           f"{resid_var(np.ones(3) / 3, np.ones(3) / 3):.6f} = 2/9")

    # ---------------- (f) finite n, exact sums ----------------
    # uniform ternary cube, zero residual, D = Hamming ball of radius r around a point:
    #   Phi^+(D) = sum_{j<=r} pi(S_j) exp(u (r+1-j)),  dens(D) = sum_{j<=r} pi(S_j),  pi(S_j) = C(n,j) 2^j / 3^n
    # binary slice 1/2 (n even), centre in the slice, D = {d(x, centre) <= 2r}:  |S_j| = C(n/2, j)^2, d = 2j
    #   Phi^+(D) = sum_{j<=r} pi(S_j) exp(2u (r+1-j)),  pi(S_j) = C(n/2,j)^2 / C(n, n/2)
    # lower bound of Theorem 11.76(b): (1-2 delta)/dens(D) evaluations whenever eps < ln(1 + Phi(D)), Phi = Phi^+ - dens.
    u = 0.5
    print("      finite n (u = 0.5, accuracy eps = 1): largest certified ln(evaluations)/n from balls")
    print("             n     ternary cube    binary slice 1/2     (limits R_3(0) = 0.007425, R_2(0) = 0.007673)")
    fin_ok = True
    for n in (2000, 20000, 200000, 2000000):
        j = np.arange(0, n + 1)
        lw3 = gammaln(n + 1) - gammaln(j + 1) - gammaln(n - j + 1) + j * math.log(2) - n * math.log(3)
        h = n // 2
        jj = np.arange(0, h + 1)
        lw2 = 2 * (gammaln(h + 1) - gammaln(jj + 1) - gammaln(h - jj + 1)) - (gammaln(n + 1) - 2 * gammaln(h + 1))

        def best_rate(lw, step):
            # prefix log-sums
            ldens = np.logaddexp.accumulate(lw)
            # log Phi^+ for radius r:  log sum_{j<=r} w_j e^{step (r+1-j)} = step (r+1) + log sum_{j<=r} w_j e^{-step j}
            lphi = step * (np.arange(len(lw)) + 1) + np.logaddexp.accumulate(lw - step * np.arange(len(lw)))
            # ln(1 + Phi) > eps with Phi = Phi^+ - dens;  use Phi >= Phi^+ (1 - e^{-step}) (every term has slack >= step)
            feasible = (lphi + math.log(1 - math.exp(-step)) > math.log(math.expm1(1.0))) & (ldens < 0)
            if not feasible.any():
                return float("nan")
            return float(np.max(-ldens[feasible])) / n

        r3 = best_rate(lw3, u)
        r2 = best_rate(lw2, 2 * u)
        fin_ok &= (r2 > r3) if n >= 20000 else True
        print(f"        {n:8d}     {r3:.6f}        {r2:.6f}")
    report("(f) finite n", fin_ok, "for n >= 20000 the exact lower bound from balls in the binary slice 1/2 exceeds the one from "
                                   "balls in the uniform ternary cube (both are LOWER bounds for all algorithms)")
    print()
    print("SUMMARY:", "ALL PASS" if ok_all else "FAILURES")


if __name__ == "__main__":
    main()
