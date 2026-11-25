#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- independent numerical replication of Lemma 11.89 (odds-ratio lemma).

Claim under test.  (B, X) binary with positive joint law P, log odds ratio
    ln[P11 P00 / (P10 P01)] = 2 s >= 0.
Then  I(B;X) <= K(s/2),  K(x) = x tanh x - ln cosh x  (= ln 2 - h(sigma(s))),
with equality iff s = 0 or both marginals uniform.

Own code, written before reading the authors' scripts.  Three independent parametrisations:
  (A) marginals (p, q) + odds ratio psi  -> table via the Plackett quadratic;
  (B) Ising coordinates (J, h1, h2);
  (C) channel form: closed-form capacity of the binary asymmetric channel (maximise over input by
      golden section, compare with the closed form), fixed odds ratio.
Also checks every step of the referee's own short proof:
  (P1) dI/dJ = J dm/dJ on a fixed-marginal fibre (finite differences, mpmath),
  (P2) dm/dJ = 16 / sum(1/T),
  (P3) sum(1/T) >= 16 cosh^2 J  with equality iff h1 = h2 = 0,
  (P4) I = int_0^J J' m'(J') dJ' (quadrature).
Run:  python3 lemma_1189.py            (about 1-2 minutes)
"""
import math
import random
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 60


# ----------------------------------------------------------------------------------------------
# helpers (float64)
# ----------------------------------------------------------------------------------------------
def K(x):
    x = np.asarray(x, dtype=float)
    # x tanh x - ln cosh x, stable for large |x|:  ln cosh x = |x| + log1p(exp(-2|x|)) - ln 2
    ax = np.abs(x)
    return ax * np.tanh(ax) - (ax + np.log1p(np.exp(-2 * ax)) - math.log(2.0))


def table_from_marginals(p, q, psi):
    """2x2 table with P(B=1)=p, P(X=1)=q and odds ratio psi (arrays ok). Returns P11,P10,P01,P00."""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    psi = np.asarray(psi, float)
    B = 1.0 + (psi - 1.0) * (p + q)
    # disc = B^2 - 4 psi (psi-1) p q, rewritten as a sum of non-negative terms (no cancellation, psi >= 1):
    disc = 1.0 + 2.0 * (psi - 1.0) * (p + q - 2.0 * p * q) + (psi - 1.0) ** 2 * (p - q) ** 2
    # numerically stable root:  P11 = 2 psi p q / (B + sqrt(disc))   (valid for all psi > 0)
    P11 = 2.0 * psi * p * q / (B + np.sqrt(disc))
    return P11, p - P11, q - P11, 1.0 - p - q + P11


def mi_cells(P11, P10, P01, P00):
    p = P11 + P10
    q = P11 + P01
    out = 0.0
    for c, a, b in ((P11, p, q), (P10, p, 1 - q), (P01, 1 - p, q), (P00, 1 - p, 1 - q)):
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(c > 0, c * (np.log(c) - np.log(a) - np.log(b)), 0.0)
        out = out + t
    return out


# ----------------------------------------------------------------------------------------------
# mpmath versions for boundary cases
# ----------------------------------------------------------------------------------------------
def K_mp(x):
    x = mp.mpf(x)
    return x * mp.tanh(x) - mp.log(mp.cosh(x))


def ising_table_mp(J, h1, h2):
    J, h1, h2 = mp.mpf(J), mp.mpf(h1), mp.mpf(h2)
    w = {(b, x): mp.e ** (J * b * x + h1 * b + h2 * x) for b in (1, -1) for x in (1, -1)}
    Z = sum(w.values())
    return {k: v / Z for k, v in w.items()}


def mi_mp(T):
    pb = {b: T[(b, 1)] + T[(b, -1)] for b in (1, -1)}
    px = {x: T[(1, x)] + T[(-1, x)] for x in (1, -1)}
    return sum(v * mp.log(v / (pb[k[0]] * px[k[1]])) for k, v in T.items())


def table_mp_from_marginals(p, q, psi):
    p, q, psi = mp.mpf(p), mp.mpf(q), mp.mpf(psi)
    B = 1 + (psi - 1) * (p + q)
    disc = 1 + 2 * (psi - 1) * (p + q - 2 * p * q) + (psi - 1) ** 2 * (p - q) ** 2
    P11 = 2 * psi * p * q / (B + mp.sqrt(disc))
    return {(1, 1): P11, (1, -1): p - P11, (-1, 1): q - P11, (-1, -1): 1 - p - q + P11}


results = {}


def report(name, ok, detail):
    results[name] = ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    sys.stdout.flush()


# ----------------------------------------------------------------------------------------------
# (A) fine grid over (p, q, s): 400 x 400 marginals, 60 values of s  (9.6e6 tables)
# ----------------------------------------------------------------------------------------------
def test_A_grid():
    n = 400
    ps = (np.arange(n) + 0.5) / n                      # (0,1) open grid, includes values near 0.5
    ps = np.unique(np.concatenate([ps, [0.5, 0.499, 0.501, 1e-6, 1 - 1e-6, 1e-9, 1 - 1e-9]]))
    Pg, Qg = np.meshgrid(ps, ps, indexing="ij")
    s_vals = np.concatenate([[1e-4, 1e-3, 1e-2], np.linspace(0.05, 3.0, 40), np.linspace(3.25, 12.0, 17)])
    worst_gap = np.inf      # min over tables of  K(s/2) - I   (must be >= 0)
    worst_ratio = 0.0       # max of I / K(s/2)  (must be <= 1)
    arg = None
    n_tab = 0
    n_bad = 0
    for s in s_vals:
        psi = math.exp(2 * s)
        I = mi_cells(*table_from_marginals(Pg, Qg, psi))
        k = float(K(s / 2))
        gap = k - I
        ratio = I / k
        n_tab += I.size
        # tolerance: rounding only (relative 1e-9 of K plus absolute 1e-15)
        n_bad += int(np.sum(gap < -(1e-9 * k + 1e-15)))
        i = np.unravel_index(np.argmax(ratio), ratio.shape)
        if ratio[i] > worst_ratio:
            worst_ratio = float(ratio[i])
            arg = (float(s), float(Pg[i]), float(Qg[i]), float(I[i]), k)
        worst_gap = min(worst_gap, float(gap.min()))
        # the maximiser on the grid must be the uniform table
        assert abs(Pg[i] - 0.5) < 1e-12 and abs(Qg[i] - 0.5) < 1e-12, (s, Pg[i], Qg[i])
    report("A.grid", n_bad == 0,
           f"{n_tab} tables, s in [1e-4, 12]; violations {n_bad}; max I/K = {worst_ratio:.15f} at "
           f"(s,p,q,I,K)={arg}; min(K-I) = {worst_gap:.3e}")
    # next-to-uniform cells: the ratio must be strictly below 1 away from (1/2, 1/2)
    for s in (0.1, 1.0, 4.0):
        psi = math.exp(2 * s)
        r = mi_cells(*table_from_marginals(np.array([0.5, 0.5, 0.49, 0.49]),
                                           np.array([0.49, 0.51, 0.49, 0.51]), psi)) / float(K(s / 2))
        print(f"      s={s}: I/K at (p,q)=(.5,.49),(.5,.51),(.49,.49),(.49,.51): "
              + ", ".join(f"{v:.9f}" for v in r))


# ----------------------------------------------------------------------------------------------
# (B) random search in Ising coordinates, including boundary regimes, high precision
# ----------------------------------------------------------------------------------------------
def test_B_random(n_trials=20000, seed=20261125):
    rng = random.Random(seed)
    worst = mp.mpf(0)          # max over trials of (I - K)/K   (must be <= 0)
    worst_arg = None
    regimes = {
        "generic":            lambda: (rng.uniform(0.01, 4), rng.uniform(-5, 5), rng.uniform(-5, 5)),
        "odds->1 (J small)":  lambda: (10 ** rng.uniform(-12, -2), rng.uniform(-5, 5), rng.uniform(-5, 5)),
        "odds->inf (J big)":  lambda: (rng.uniform(5, 60), rng.uniform(-80, 80), rng.uniform(-80, 80)),
        "marginals->0":       lambda: (rng.uniform(0.01, 6), rng.uniform(5, 60) * rng.choice((-1, 1)),
                                       rng.uniform(5, 60) * rng.choice((-1, 1))),
        "near-uniform":       lambda: (rng.uniform(0.01, 6), 10 ** rng.uniform(-10, -2) * rng.choice((-1, 1)),
                                       10 ** rng.uniform(-10, -2) * rng.choice((-1, 1))),
        "compensating h":     None,  # h1 = -h2 or h1 = +-J etc.: lines where cells coincide
    }
    per = {}
    for name, gen in regimes.items():
        w = mp.mpf("-inf")
        cnt = 0
        for _ in range(n_trials // len(regimes)):
            if gen is None:
                J = rng.uniform(0.01, 6)
                c = rng.choice(("h1=-h2", "h1=h2", "h1=J", "h2=-J", "h1=0", "h2=0"))
                t = rng.uniform(-8, 8)
                h1, h2 = {"h1=-h2": (t, -t), "h1=h2": (t, t), "h1=J": (J, t), "h2=-J": (t, -J),
                          "h1=0": (0.0, t), "h2=0": (t, 0.0)}[c]
            else:
                J, h1, h2 = gen()
            T = ising_table_mp(J, h1, h2)
            I = mi_mp(T)
            k = K_mp(J)
            rel = (I - k) / k
            cnt += 1
            if rel > w:
                w = rel
            if rel > worst:
                worst, worst_arg = rel, (name, J, h1, h2)
        per[name] = (cnt, w)
    ok = worst <= mp.mpf(10) ** (-40)
    report("B.random(mp, 60 digits)", ok,
           "max (I-K)/K per regime: " + "; ".join(f"{k}: {mp.nstr(v[1], 6)} (n={v[0]})" for k, v in per.items())
           + (f"; WORST {worst_arg}" if not ok else ""))


def test_B_limits():
    """Explicit boundary sequences: I/K along marginals -> 0, odds -> 1, odds -> inf."""
    rows = []
    # odds ratio -> 1 at fixed non-uniform marginals:  I/K -> 16 p(1-p) q(1-q)
    for p, q in ((0.5, 0.5), (0.3, 0.6), (0.01, 0.5), (0.2, 0.2)):
        s = mp.mpf("1e-10")
        T = table_mp_from_marginals(p, q, mp.e ** (2 * s))
        r = mi_mp(T) / K_mp(s / 2)
        pred = 16 * mp.mpf(p) * (1 - mp.mpf(p)) * mp.mpf(q) * (1 - mp.mpf(q))
        rows.append((f"s->0, (p,q)=({p},{q})", r, pred))
        assert abs(r - pred) < mp.mpf("1e-8"), (p, q, r, pred)
        assert r <= 1 + mp.mpf("1e-30")
    # odds ratio -> infinity at fixed marginals: I -> the maximal-coupling value <= ln 2
    for p, q in (("0.5", "0.5"), ("0.3", "0.6"), ("0.3", "0.3"), ("0.01", "0.5")):
        with mp.workdps(700):     # cells are differences of numbers agreeing to ~175 digits
            s = mp.mpf(200)
            T = table_mp_from_marginals(mp.mpf(p), mp.mpf(q), mp.e ** (2 * s))
            I = mi_mp(T)
            rows.append((f"s=200, (p,q)=({p},{q})", I, K_mp(s / 2)))
            assert all(v > 0 for v in T.values())
            assert I <= K_mp(s / 2) + mp.mpf("1e-300"), (p, q)
            # limit value: the mutual information of the maximal coupling of (p, q)
            if p != q:
                pp, qq = mp.mpf(p), mp.mpf(q)   # here p < q: cells -> (p, 0, q-p, 1-q)
                lim = (pp * mp.log(pp / (pp * qq)) + (qq - pp) * mp.log((qq - pp) / ((1 - pp) * qq))
                       + (1 - qq) * mp.log((1 - qq) / ((1 - pp) * (1 - qq))))
                assert abs(I - lim) < mp.mpf("1e-50"), (I, lim)
    # marginals -> 0 at fixed s
    for s in (0.5, 2.0, 8.0):
        for eps in ("1e-3", "1e-10", "1e-30"):
            for (p, q) in ((eps, 0.5), (eps, eps), (eps, mp.mpf(1) - mp.mpf(eps))):
                T = table_mp_from_marginals(p, q, mp.e ** (2 * mp.mpf(s)))
                I = mi_mp(T)
                assert I <= K_mp(mp.mpf(s) / 2), (s, p, q)
                assert all(v > 0 for v in T.values())
                rows.append((f"s={s}, (p,q)=({mp.nstr(mp.mpf(p), 3)},{mp.nstr(mp.mpf(q), 3)})", I,
                             K_mp(mp.mpf(s) / 2)))
    for name, a, b in rows:
        print(f"      {name:40s} value {mp.nstr(a, 12):>22s}   reference {mp.nstr(b, 12)}")
    report("B.limits", True, "odds->1 ratio = 16 p(1-p) q(1-q) <= 1 (checked to 1e-8); odds->inf and "
                             "marginals->0 sequences all below K")


# ----------------------------------------------------------------------------------------------
# (C) channel form: capacity of the binary asymmetric channel at fixed odds ratio
# ----------------------------------------------------------------------------------------------
def hb(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x * np.log(x) - (1 - x) * np.log1p(-x)


def capacity_bac_closed(e0, e1):
    """Closed form (nats) for the channel P(1|0)=e0, P(0|1)=e1, e0+e1<1 (textbook formula)."""
    d = 1.0 - e0 - e1
    return (e0 / d) * hb(e1) - ((1 - e1) / d) * hb(e0) + np.log1p(np.exp((hb(e0) - hb(e1)) / d))


def capacity_bac_numeric(e0, e1, iters=200):
    """Golden-section maximisation of I over the input law w = P(B=1) (I is concave in w)."""
    def I(w):
        out1 = w * (1 - e1) + (1 - w) * e0
        return hb(out1) - w * hb(e1) - (1 - w) * hb(e0)
    a, b = 0.0, 1.0
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(iters):
        if I(c) > I(d):
            b, d = d, c
            c = b - g * (b - a)
        else:
            a, c = c, d
            d = a + g * (b - a)
    w = 0.5 * (a + b)
    return float(I(w)), w


def test_C_channel(seed=7):
    rng = np.random.default_rng(seed)
    worst = -np.inf
    max_cf_err = 0.0
    lean_ok = True
    n = 0
    for s in list(np.linspace(0.05, 6, 40)) + [1e-3, 9.0]:
        psi = math.exp(2 * s)
        # channels with odds ratio psi:  (1-e0)(1-e1)/(e0 e1) = psi ;  choose e1 freely, solve e0
        for e1 in np.concatenate([rng.uniform(1e-6, 0.5, 60), [1e-9, 1e-4, 0.25, 1 / (1 + math.exp(s))]]):
            e0 = (1 - e1) / ((1 - e1) + psi * e1)
            if e0 + e1 >= 1 - 1e-12:
                continue
            c_num, w = capacity_bac_numeric(e0, e1)
            c_cf = float(capacity_bac_closed(e0, e1))
            max_cf_err = max(max_cf_err, abs(c_num - c_cf))
            k = float(K(s / 2))
            worst = max(worst, (max(c_num, c_cf) - k) / k)
            # "the capacity-achieving input leans against the channel's bias":
            # output of input 1 is 1 w.p. 1-e1, output of input 0 is 0 w.p. 1-e0.
            # if e0 < e1 (channel biased towards output 0) the optimal input should favour b=1 (w > 1/2)
            if abs(e0 - e1) > 1e-6 and s > 1e-2:
                if (e0 < e1) != (w > 0.5):
                    lean_ok = False
            n += 1
    report("C.channel", worst <= 1e-9 and max_cf_err < 1e-9,
           f"{n} asymmetric channels; max (C-K)/K = {worst:.3e}; |C_numeric - C_closed| <= {max_cf_err:.2e}; "
           f"'input leans against bias' held in all cases: {lean_ok}")


# ----------------------------------------------------------------------------------------------
# (P) the referee's short proof, step by step
# ----------------------------------------------------------------------------------------------
def fibre_table(p, q, J):
    """table with marginals (p,q) (probabilities of +1) and Ising coupling J (log odds ratio 4J)."""
    return table_mp_from_marginals(p, q, mp.e ** (4 * mp.mpf(J)))


def test_P_proof(seed=3):
    rng = random.Random(seed)
    max_e1 = max_e2 = mp.mpf(0)
    min_slack = mp.inf
    max_e4 = mp.mpf(0)
    for _ in range(300):
        p, q = rng.uniform(0.02, 0.98), rng.uniform(0.02, 0.98)
        J = rng.uniform(0.05, 3.0)
        m = lambda j: sum(k[0] * k[1] * v for k, v in fibre_table(p, q, j).items())
        I = lambda j: mi_mp(fibre_table(p, q, j))
        dm = mp.diff(m, J)
        dI = mp.diff(I, J)
        T = fibre_table(p, q, J)
        S = sum(1 / v for v in T.values())
        max_e1 = max(max_e1, abs(dI - J * dm))                    # (P1)
        max_e2 = max(max_e2, abs(dm - 16 / S))                    # (P2)
        min_slack = min(min_slack, S - 16 * mp.cosh(J) ** 2)      # (P3)  >= 0
    for _ in range(40):
        p, q = rng.uniform(0.02, 0.98), rng.uniform(0.02, 0.98)
        J = rng.uniform(0.05, 3.0)
        f = lambda j: j * 16 / sum(1 / v for v in fibre_table(p, q, j).values())
        quad = mp.quad(f, [0, J])
        max_e4 = max(max_e4, abs(quad - mi_mp(fibre_table(p, q, J))))   # (P4)
    # (P3) closed form:  sum 1/T = 4 [A^2 + B^2 + 2 cosh(2J) A B]
    max_e3 = mp.mpf(0)
    for _ in range(300):
        J, h1, h2 = rng.uniform(0, 3), rng.uniform(-4, 4), rng.uniform(-4, 4)
        T = ising_table_mp(J, h1, h2)
        S = sum(1 / v for v in T.values())
        A, B = mp.cosh(h1 + h2), mp.cosh(h1 - h2)
        max_e3 = max(max_e3, abs(S - 4 * (A * A + B * B + 2 * mp.cosh(2 * J) * A * B)) / S)
    ok = max_e1 < mp.mpf("1e-25") and max_e2 < mp.mpf("1e-25") and min_slack >= 0 and max_e4 < mp.mpf(
        "1e-20") and max_e3 < mp.mpf("1e-40")
    report("P.proof-steps", ok,
           f"|dI/dJ - J dm/dJ| <= {mp.nstr(max_e1, 3)}; |dm/dJ - 16/sum(1/T)| <= {mp.nstr(max_e2, 3)}; "
           f"min[sum(1/T) - 16cosh^2 J] = {mp.nstr(min_slack, 3)} (>=0); closed form of sum(1/T) rel.err "
           f"<= {mp.nstr(max_e3, 3)}; |int_0^J J'm' - I| <= {mp.nstr(max_e4, 3)}")


# ----------------------------------------------------------------------------------------------
# (E) equality case and second-order behaviour at the uniform table
# ----------------------------------------------------------------------------------------------
def test_E_equality():
    worst = mp.mpf(0)
    for J in ("0.001", "0.1", "1", "5", "30"):
        T = ising_table_mp(J, 0, 0)
        worst = max(worst, abs(mi_mp(T) - K_mp(J)) / K_mp(J))
    # strictness: Hessian of I in (h1,h2) at h=0 is negative definite for J>0
    neg_def = True
    rows = []
    for J in (0.05, 0.5, 1.0, 2.0, 4.0):
        f = lambda a, b: mi_mp(ising_table_mp(J, a, b))
        H11 = mp.diff(f, (0, 0), (2, 0))
        H12 = mp.diff(f, (0, 0), (1, 1))
        H22 = mp.diff(f, (0, 0), (0, 2))
        det = H11 * H22 - H12 * H12
        rows.append((J, H11, H12, det))
        neg_def &= (H11 < 0 and det > 0)
    for r in rows:
        print(f"      J={r[0]}: I_h1h1 = {mp.nstr(r[1], 8)}, I_h1h2 = {mp.nstr(r[2], 8)}, det = {mp.nstr(r[3], 8)}")
    report("E.equality", worst < mp.mpf("1e-45") and neg_def,
           f"I(uniform) = K to rel. {mp.nstr(worst, 3)}; Hessian in (h1,h2) at uniform negative definite: {neg_def}")


if __name__ == "__main__":
    test_A_grid()
    test_B_random()
    test_B_limits()
    test_C_channel()
    test_P_proof()
    test_E_equality()
    print()
    print("SUMMARY:", "ALL PASS" if all(results.values()) else "FAILURES: " + ", ".join(k for k, v in results.items() if not v))
