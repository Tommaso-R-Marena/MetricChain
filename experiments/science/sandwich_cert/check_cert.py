#!/usr/bin/env python3
"""Reference checker for sandwich certificates in the format `metricchain-sandwich/1`.

The format is written down in docs/science/SANDWICH_CERTIFICATE_FORMAT.md; this file follows that text and
imports nothing of the code that produces certificates (only the standard library and mpmath's interval
arithmetic).  It is a PYTHON REFERENCE: tested, not verified.

What a file asserts, and what this checker establishes (Stage 1 of the engineering division's proposal,
ENG-MSG-0007 section 3 (d)):

  DATA TAKEN AS GIVEN (they belong to Stage 2 and are NOT checked here).  g~ denotes the EVALUATED values of g at
  the states that differ from the anchor at no more than m - 1 sites, and I_{m-1} g~ the anchored expansion formed
  from those values in exact arithmetic:
    (G1) the tables `A_lower`, `A_upper` satisfy  A_lower(x) <= f(x) + I_{m-1} g~(x) <= A_upper(x)  at every state x;
    (G2) there are constants c_T >= 0, one for every set T of m sites, with
             |g(x) - I_{m-1} g(x)|  <=  sum of c_T over the T inside S(x) = {i : x_i != anchor_i},
         whose sums Gamma^(-A) = sum of c_T over the T that avoid A lie in the published intervals `stepA`
         (A empty, one site, one in-band pair);
    (G3) |g~(y) - g(y)| <= eps_g at every evaluated state y.

  CHECKED HERE, in exact integer / rational arithmetic:
    (A0) the data do not contradict themselves: the intervals of step A are compatible with what holds for EVERY
         family of non-negative constants (monotonicity under exclusion, non-negative pair sums, the two
         double-counting identities), and  A_lower(x) <= A_upper(x)  at every state (exact min-plus transfer matrix);
    (B)  the penalty  pen(x) = c + sum_i a_i s_i + sum_{in-band i<j} b_ij s_i s_j,  s_i = [x_i != anchor_i],
         covers, at every state,  eps_g (1 + sum over U inside S(x), 1 <= |U| <= m-1, of 2^|U|)  +  sum of c_T inside S(x);
         three families of inequalities (B1, B2, B3 below) imply it by the counting lemma of the format note;
    (D)  m_lower = A_lower - pen  and  m_upper = A_upper + pen, table entry by table entry;
  CHECKED HERE, in interval arithmetic (mpmath `iv`, 30 digits, outward rounding):
    (E)  claim.lnZ_lower <= ln Z(m_upper)   and   ln Z(m_lower) <= claim.lnZ_upper   (transfer matrix along the band).

  CONCLUSION if the file is accepted and (G1)-(G3) hold:  claim.lnZ_lower <= ln Z(E) <= claim.lnZ_upper  for E = f + g
  at inverse temperature beta, energies in units of 2^unit_log2 kcal/mol.

Usage:   python3 -B check_cert.py FILE [FILE ...]          exit status 0 iff every file is accepted
"""
import itertools
import json
import math
import resource
import sys
import time
from fractions import Fraction

from mpmath import iv, libmp

FORMAT = "metricchain-sandwich/1"


class Rejected(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Rejected(why)


# ----------------------------------------------------------------------------------------------- strict loading
def _no_duplicates(pairs):
    d = {}
    for key, val in pairs:
        if key in d:
            raise Rejected(f"malformed: duplicate key {key!r}")
        d[key] = val
    return d


def _no_float(text):
    raise Rejected(f"malformed: a number that is not an integer ({text})")


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh, object_pairs_hook=_no_duplicates, parse_float=_no_float, parse_constant=_no_float)
        except json.JSONDecodeError as exc:
            raise Rejected(f"malformed: not JSON ({exc})")


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def pair_key(i, j):
    return f"{i},{j}"


# ----------------------------------------------------------------------------------------------- well-formedness
def well_formed(c):
    need(isinstance(c, dict), "malformed: top level is not an object")
    keys = {"format", "unit_log2", "beta", "eps_g", "instance", "stepA", "penalty",
            "A_lower", "A_upper", "m_lower", "m_upper", "claim", "annotations"}
    need(set(c) <= keys and (keys - {"annotations"}) <= set(c), "malformed: wrong set of top-level keys")
    need(c["format"] == FORMAT, "malformed: unknown format")
    need(is_int(c["unit_log2"]) and -200 <= c["unit_log2"] <= 0, "malformed: unit_log2")
    for name in ("beta", "eps_g"):
        q = c[name]
        need(isinstance(q, dict) and set(q) == {"num", "den"} and is_int(q["num"]) and is_int(q["den"])
             and q["num"] > 0 and q["den"] > 0, f"malformed: {name} is not a positive rational num/den")
    ins = c["instance"]
    need(isinstance(ins, dict) and set(ins) == {"n", "k", "anchor", "order_m", "band_w"}, "malformed: instance keys")
    n, k, x0, m, w = ins["n"], ins["k"], ins["anchor"], ins["order_m"], ins["band_w"]
    need(is_int(n) and n >= 1, "malformed: n")
    need(isinstance(k, list) and len(k) == n and all(is_int(v) and v >= 1 for v in k), "malformed: k")
    need(isinstance(x0, list) and len(x0) == n and all(is_int(v) and 0 <= v < k[i] for i, v in enumerate(x0)),
         "malformed: anchor")
    need(is_int(m) and m >= 2 and is_int(w) and 1 <= w <= max(1, n - 1), "malformed: order_m or band_w")
    inband = [(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= w]
    pkeys = {pair_key(i, j) for i, j in inband}

    def interval(v):
        return isinstance(v, list) and len(v) == 2 and is_int(v[0]) and is_int(v[1]) and 0 <= v[0] <= v[1]

    sa = c["stepA"]
    need(isinstance(sa, dict) and set(sa) == {"Gamma", "Gamma_minus_i", "Gamma_minus_ij"}, "malformed: stepA keys")
    need(interval(sa["Gamma"]), "malformed: stepA.Gamma is not an interval 0 <= lo <= up")
    need(isinstance(sa["Gamma_minus_i"], list) and len(sa["Gamma_minus_i"]) == n
         and all(interval(v) for v in sa["Gamma_minus_i"]), "malformed: stepA.Gamma_minus_i")
    need(isinstance(sa["Gamma_minus_ij"], dict) and set(sa["Gamma_minus_ij"]) == pkeys
         and all(interval(v) for v in sa["Gamma_minus_ij"].values()), "malformed: stepA.Gamma_minus_ij (keys = in-band pairs)")
    pen = c["penalty"]
    need(isinstance(pen, dict) and set(pen) == {"c", "a", "b"}, "malformed: penalty keys")
    need(is_int(pen["c"]) and pen["c"] >= 0, "malformed: penalty.c")
    need(isinstance(pen["a"], list) and len(pen["a"]) == n and all(is_int(v) and v >= 0 for v in pen["a"]),
         "malformed: penalty.a")
    need(isinstance(pen["b"], dict) and set(pen["b"]) == pkeys and all(is_int(v) and v >= 0 for v in pen["b"].values()),
         "malformed: penalty.b (keys = in-band pairs)")
    for name in ("A_lower", "A_upper", "m_lower", "m_upper"):
        t = c[name]
        need(isinstance(t, dict) and set(t) == {"const", "one", "pair"}, f"malformed: {name} keys")
        need(is_int(t["const"]), f"malformed: {name}.const")
        need(isinstance(t["one"], list) and len(t["one"]) == n
             and all(isinstance(r, list) and len(r) == k[i] and all(is_int(v) for v in r) for i, r in enumerate(t["one"])),
             f"malformed: {name}.one")
        need(isinstance(t["pair"], dict) and set(t["pair"]) == pkeys, f"malformed: {name}.pair (keys = in-band pairs)")
        for (i, j) in inband:
            tab = t["pair"][pair_key(i, j)]
            need(isinstance(tab, list) and len(tab) == k[i]
                 and all(isinstance(r, list) and len(r) == k[j] and all(is_int(v) for v in r) for r in tab),
                 f"malformed: {name}.pair[{i},{j}]")
    cl = c["claim"]
    need(isinstance(cl, dict) and set(cl) == {"lnZ_lower", "lnZ_upper"}, "malformed: claim keys")
    for name in ("lnZ_lower", "lnZ_upper"):
        q = cl[name]
        need(isinstance(q, dict) and set(q) == {"num", "den"} and is_int(q["num"]) and is_int(q["den"]) and q["den"] > 0,
             f"malformed: claim.{name} is not a rational num/den")
    if "annotations" in c:
        need(isinstance(c["annotations"], dict), "malformed: annotations")
    return n, k, x0, m, w, inband


# ----------------------------------------------------------------------------------------------- band recursion
def band_fold(table, n, k, w, lift, times, plus, unit_elem):
    """sum over all states (in the semiring given by `plus`, `times`) of the product over the terms of a band model
    of lift(term), the terms attached to site i being collected first:  e_i = one[i][x_i] + sum_{i<j<=i+w} pair[i,j][x_i][x_j]
    (an exact integer).  After site i has been summed out the message is a function of the sites i+1 .. min(i+w, n-1).
    The constant of the model is NOT included."""
    one, pair = table["one"], table["pair"]
    msg = {(): unit_elem}
    prev_hi = -1                                                        # the message is over the sites i .. prev_hi
    for i in range(n):
        hi = min(i + w, n - 1)
        new = {}
        ptabs = [pair[pair_key(i, j)] for j in range(i + 1, hi + 1)]
        npast = max(prev_hi - i, 0)                                     # tail sites already in the old message
        for t in itertools.product(*[range(k[s]) for s in range(i + 1, hi + 1)]):
            acc = None
            for x in range(k[i]):
                e = one[i][x]
                for r, tab in enumerate(ptabs):
                    e += tab[x][t[r]]
                old = msg[((x,) + t[:npast]) if prev_hi >= i else ()]
                term = times(old, lift(e))
                acc = term if acc is None else plus(acc, term)
            new[t] = acc
        msg = new
        prev_hi = hi
    return msg[()]


def band_minimum(table, n, k, w):
    """exact minimum over all states of a band model with integer tables (min-plus recursion)."""
    return table["const"] + band_fold(table, n, k, w, lambda e: e, lambda a, b: a + b, min, 0)


# ----------------------------------------------------------------------------------------------- (A0) consistency
def step_a_sums(c, n, w, inband):
    """interval ends, in units, of  S_i = Gamma - Gamma^(-i)  and  G_ij = Gamma - Gamma^(-i) - Gamma^(-j) + Gamma^(-i,-j)."""
    sa = c["stepA"]
    G_lo, G_up = sa["Gamma"]
    Gi, Gij = sa["Gamma_minus_i"], sa["Gamma_minus_ij"]
    s_lo = [max(0, G_lo - Gi[i][1]) for i in range(n)]
    s_up = [G_up - Gi[i][0] for i in range(n)]
    pair_lo, pair_up = {}, {}
    for (i, j) in inband:
        key = pair_key(i, j)
        pair_up[(i, j)] = G_up - Gi[i][0] - Gi[j][0] + Gij[key][1]
        pair_lo[(i, j)] = max(0, G_lo - Gi[i][1] - Gi[j][1] + Gij[key][0])
    return s_lo, s_up, pair_lo, pair_up


def check_consistency(c, n, k, m, w, inband):
    """Exact.  Necessary conditions on the intervals of step A: properties of EVERY family of non-negative constants
    indexed by the sets of m sites.  A file that fails cannot have true data."""
    sa = c["stepA"]
    G_lo, G_up = sa["Gamma"]
    Gi, Gij = sa["Gamma_minus_i"], sa["Gamma_minus_ij"]
    s_lo, s_up, pair_lo, pair_up = step_a_sums(c, n, w, inband)
    for i in range(n):                                                  # excluding a site cannot increase a sum
        need(Gi[i][0] <= G_up, f"A0 violated: Gamma_minus_i[{i}] lies above Gamma")
    for (i, j) in inband:
        lo = Gij[pair_key(i, j)][0]
        need(lo <= Gi[i][1] and lo <= Gi[j][1], f"A0 violated: Gamma_minus_ij[{i},{j}] lies above a one-site sum")
        need(pair_up[(i, j)] >= 0, f"A0 violated: the pair sum at ({i},{j}) would be negative")
    # every set T of m sites is counted m times in sum_i S_i
    need(m * G_lo <= sum(s_up) and sum(s_lo) <= m * G_up, "A0 violated: sum_i S_i = m Gamma is impossible")
    # every set T through i is counted m - 1 times in sum_{j != i} G_ij
    for i in range(n):
        inb = [(min(i, j), max(i, j)) for j in range(n) if j != i and abs(i - j) <= w]
        need((m - 1) * s_up[i] >= sum(pair_lo[p] for p in inb),
             f"A0 violated: double counting at site {i} (the in-band pair sums exceed (m-1) S_i)")
        if len(inb) == n - 1:
            need((m - 1) * s_lo[i] <= sum(pair_up[p] for p in inb),
                 f"A0 violated: double counting at site {i} ((m-1) S_i exceeds the pair sums)")


def check_ordered(c, n, k, w):
    """Exact.  The two models of the evaluated part must be ordered at every state: min over states of
    A_upper - A_lower, by the min-plus recursion along the band.  Returns that minimum (in units)."""
    lo, up = c["A_lower"], c["A_upper"]
    diff = dict(const=up["const"] - lo["const"],
                one=[[u - l for u, l in zip(ru, rl)] for ru, rl in zip(up["one"], lo["one"])],
                pair={key: [[u - l for u, l in zip(ru, rl)] for ru, rl in zip(up["pair"][key], lo["pair"][key])]
                      for key in up["pair"]})
    gap = band_minimum(diff, n, k, w)
    need(gap >= 0, "A0 violated: A_lower exceeds A_upper at some state")
    return gap


# ----------------------------------------------------------------------------------------------- (B) covering
def check_covering(c, n, k, x0, m, w, inband):
    """Exact.  All quantities in units of 2^unit_log2 kcal/mol, as Fractions."""
    unit = Fraction(2) ** c["unit_log2"]
    eps = Fraction(c["eps_g"]["num"], c["eps_g"]["den"]) / unit          # eps_g in units
    M = m - 1
    active = [i for i in range(n) if k[i] > 1]
    na = len(active)
    c2 = math.comb(m, 2)
    # floating-point allowances: a term d_U (1 <= |U| <= M) is an alternating sum of 2^|U| evaluated values
    psi_site = 2 * eps                                                  # |U| = 1
    psi_pair = eps * sum(Fraction(math.comb(na - 2, s - 2) * 2 ** s, math.comb(s, 2)) for s in range(2, M + 1)) \
        if na >= 2 else Fraction(0)                                     # pair shares of every U with |U| >= 2
    pen = c["penalty"]
    isact = [k[i] > 1 for i in range(n)]
    # B3
    need(pen["c"] >= eps, "B3 violated: the constant is below eps_g")
    s_lo, s_up, pair_lo, pair_up = step_a_sums(c, n, w, inband)
    # B1: in-band pairs
    for (i, j) in inband:
        if not (isact[i] and isact[j]):
            continue                                                    # s_i s_j is identically zero
        lhs = c2 * (pen["b"][pair_key(i, j)] - psi_pair)
        need(lhs >= pair_up[(i, j)], f"B1 violated at pair ({i},{j})")
    # B2: sites; the out-of-band pair sums through i are bounded by double counting
    for i in active:
        inb = [(min(i, j), max(i, j)) for j in range(n) if j != i and abs(i - j) <= w]
        nout = sum(1 for j in active if j != i and abs(i - j) > w)
        far = max(0, (m - 1) * s_up[i] - sum(pair_lo[p] for p in inb))  # bound of the out-of-band pair sums through i
        lhs = 2 * c2 * (pen["a"][i] - psi_site - Fraction(nout, 2) * psi_pair)
        need(lhs >= far, f"B2 violated at site {i}")
    return dict(psi_site=psi_site, psi_pair=psi_pair, eps_units=eps)


# ----------------------------------------------------------------------------------------------- (D) tables
def check_tables(c, n, k, x0, inband):
    pen = c["penalty"]
    for name, src, sign in (("m_lower", "A_lower", -1), ("m_upper", "A_upper", +1)):
        mt, at = c[name], c[src]
        need(mt["const"] == at["const"] + sign * pen["c"], f"D violated: {name}.const")
        for i in range(n):
            for x in range(k[i]):
                want = at["one"][i][x] + (sign * pen["a"][i] if x != x0[i] else 0)
                need(mt["one"][i][x] == want, f"D violated: {name}.one[{i}][{x}]")
        for (i, j) in inband:
            key = pair_key(i, j)
            for x in range(k[i]):
                for y in range(k[j]):
                    want = at["pair"][key][x][y] + (sign * pen["b"][key] if (x != x0[i] and y != x0[j]) else 0)
                    need(mt["pair"][key][x][y] == want, f"D violated: {name}.pair[{i},{j}][{x}][{y}]")


# ----------------------------------------------------------------------------------------------- (E) ln Z
def lnZ_enclosure(table, n, k, w, beta_iv, unit_log2):
    """Interval enclosure of ln sum_x exp(-beta * 2^unit_log2 * model(x)) for a band model with integer tables."""
    scale = -beta_iv * iv.mpf(2) ** unit_log2
    z = band_fold(table, n, k, w, lambda e: iv.exp(scale * e), lambda a, b: a * b, lambda a, b: a + b, iv.mpf(1))
    return iv.log(z) + scale * table["const"]


def endpoints(x):
    """the two end points of an mpmath interval as exact rationals (mpmath 1.3: raw end points in x._mpi_)."""
    a, b = x._mpi_
    return Fraction(*libmp.to_rational(a)), Fraction(*libmp.to_rational(b))


def check_lnZ(c, n, k, w):
    beta_iv = iv.mpf(c["beta"]["num"]) / iv.mpf(c["beta"]["den"])
    lo = Fraction(c["claim"]["lnZ_lower"]["num"], c["claim"]["lnZ_lower"]["den"])
    up = Fraction(c["claim"]["lnZ_upper"]["num"], c["claim"]["lnZ_upper"]["den"])
    need(lo <= up, "E violated: the claimed bracket is empty")
    enc_up_model = lnZ_enclosure(c["m_upper"], n, k, w, beta_iv, c["unit_log2"])      # ln Z(m_upper) <= ln Z(E)
    enc_lo_model = lnZ_enclosure(c["m_lower"], n, k, w, beta_iv, c["unit_log2"])      # ln Z(m_lower) >= ln Z(E)
    # the comparison itself is exact: the end points of an enclosure are binary rationals
    need(lo <= endpoints(enc_up_model)[0], "E violated: claim.lnZ_lower is not below the enclosure of ln Z(m_upper)")
    need(endpoints(enc_lo_model)[1] <= up, "E violated: claim.lnZ_upper is not above the enclosure of ln Z(m_lower)")
    return enc_up_model, enc_lo_model


# ----------------------------------------------------------------------------------------------- driver
def check(c):
    """Raises Rejected with the reason, or returns a report dict."""
    n, k, x0, m, w, inband = well_formed(c)
    check_consistency(c, n, k, m, w, inband)                 # (A0), intervals
    rep = check_covering(c, n, k, x0, m, w, inband)          # (B)
    check_tables(c, n, k, x0, inband)                        # (D)
    rep["min_gap_A"] = check_ordered(c, n, k, w)             # (A0), tables; placed here because it is the costlier exact check
    enc_up_model, enc_lo_model = check_lnZ(c, n, k, w)
    rep.update(n=n, m=m, w=w, pairs=len(inband), lnZ_m_upper=enc_up_model, lnZ_m_lower=enc_lo_model)
    return rep


def main(argv):
    resource.setrlimit(resource.RLIMIT_AS, (3 * 1024**3, 3 * 1024**3))
    iv.dps = 30
    ok = True
    for path in argv:
        t0 = time.time()
        try:
            c = load(path)
            rep = check(c)
        except Rejected as exc:
            ok = False
            print(f"REJECTED  {path}: {exc}")
            continue
        lo = Fraction(c["claim"]["lnZ_lower"]["num"], c["claim"]["lnZ_lower"]["den"])
        up = Fraction(c["claim"]["lnZ_upper"]["num"], c["claim"]["lnZ_upper"]["den"])
        print(f"ACCEPTED  {path}")
        print(f"   n = {rep['n']}, order m = {rep['m']}, band w = {rep['w']}, in-band pairs = {rep['pairs']}; "
              f"allowances per site / per pair (units): {float(rep['psi_site']):.6g} / {float(rep['psi_pair']):.6g}; "
              f"min over states of A_upper - A_lower: {rep['min_gap_A']} units")
        print(f"   enclosures:  ln Z(m_upper) in {iv.nstr(rep['lnZ_m_upper'], 20)}   "
              f"ln Z(m_lower) in {iv.nstr(rep['lnZ_m_lower'], 20)}")
        print(f"   IF the data (G1)-(G3) hold:  {float(lo):.9f} <= ln Z(E) <= {float(up):.9f}   "
              f"(width {float(up - lo):.3e} nats)   [{time.time() - t0:.1f} s]")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"{'ALL ACCEPTED' if ok else 'NOT ALL ACCEPTED'}   peak memory {peak:.0f} MB")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
