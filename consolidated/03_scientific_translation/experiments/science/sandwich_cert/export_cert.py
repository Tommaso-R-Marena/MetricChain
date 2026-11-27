#!/usr/bin/env python3
"""Producer of sandwich certificates in the format `metricchain-sandwich/1` (docs/science/SANDWICH_CERTIFICATE_FORMAT.md)
from the pipeline of workstreams P3 and P6 (imported read-only, unchanged).

    python3 -B export_cert.py SEQ BB TAU M W          e.g.   V6 E 0.70 4 5      V20 P2 0.70 5 8

The producer is UNTRUSTED: everything it writes is checked by check_cert.py, which imports nothing from here.

What it does
  1. runs the pipeline as p6lib.make_models does (form "B", banded pair penalties): instance tables, anchor,
     anchored terms of the solvent term on the ball of radius m - 1, the sums of P3's closed form over
     exclusion sets (step A);
  2. converts every number to an integer in units of 2^-40 kcal/mol, rounding in the direction that keeps the
     certificate valid: tables of A_lower down, of A_upper up; step-A sums to intervals [lo, up] (up: the value
     the pipeline treats as an upper bound; lo: that value times 1 - 3e-9, by P3's stated relative tolerance of
     1e-9 for a generating-function sum and its outward factor 1 + 1e-9 -- an ASSUMPTION of the pipeline, to be
     replaced by directed rounding in Stage 2);
  3. chooses the SMALLEST integer penalties that satisfy the covering inequalities B1-B3 of the format note for
     those intervals (so they are not the floating-point penalties of p6lib, but differ from them by rounding
     and by the treatment of the allowances; the difference is printed);
  4. writes m_lower = A_lower - penalty and m_upper = A_upper + penalty and claims a bracket of ln Z from a
     double-precision transfer matrix of the integer tables, widened by 5e-9 and rounded outwards to 9 decimals;
  5. prints, for comparison only: the floating-point brackets of p6lib; on enumerable instances the exact ln Z
     and the check m_lower <= E <= m_upper at every state.
"""
import json
import math
import os
import resource
import sys
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, "..", "ws_P6"))
import p6lib as L                                            # noqa: E402  (P6; imports P3 read-only)

pw = L.pw
UNIT_LOG2 = -40
UNIT = Fraction(1, 2 ** 40)
REL_LO = Fraction(3, 10 ** 9)                                # lower end of a step-A sum: value * (1 - 3e-9)
EPS_G = Fraction(1, 10 ** 7)                                 # kcal/mol; equals p6lib.EPS_G = 1e-7 as a decimal


def fl(v):
    """floor of the exact value of a double, in units"""
    return math.floor(Fraction(float(v)) / UNIT)


def ce(v):
    return math.ceil(Fraction(float(v)) / UNIT)


def pkey(i, j):
    return f"{i},{j}"


AA3 = dict(A="Ala", V="Val", L="Leu", I="Ile", S="Ser", T="Thr", K="Lys", E="Glu", D="Asp", N="Asn", Q="Gln", M="Met",
           F="Phe", Y="Tyr", W="Trp", H="His", R="Arg", C="Cys", G="Gly", P="Pro")


def peptide_name(seq):
    """'V6' -> 'Ace-(Val)6-NMe'; any other sequence code is given as it is."""
    if len(seq) >= 2 and seq[0] in AA3 and seq[1:].isdigit():
        return f"Ace-({AA3[seq[0]]}){seq[1:]}-NMe"
    return f"Ace-[{seq}]-NMe"


def tables_to_int(mdl, n, k, inband, rnd):
    one = [[rnd(v) for v in mdl.one[i]] for i in range(n)]
    pair = {}
    for (i, j) in inband:
        tab = mdl.pair.get((i, j))
        if tab is None:
            tab = np.zeros((k[i], k[j]))
        tab = np.asarray(tab, dtype=float) + np.zeros((k[i], k[j]))
        pair[pkey(i, j)] = [[rnd(v) for v in row] for row in tab]
    return dict(const=rnd(mdl.const), one=one, pair=pair)


def int_model_energy(t, st, inband):
    """energies (python ints, units) of an integer table model at states st (N, n)"""
    out = []
    for row in st:
        e = t["const"]
        for i, x in enumerate(row):
            e += t["one"][i][int(x)]
        for (i, j) in inband:
            e += t["pair"][pkey(i, j)][int(row[i])][int(row[j])]
        out.append(e)
    return out


def float_band_model(t, n, k, w, inband):
    mdl = pw.BandModel(k, w)
    mdl.const = float(t["const"] * UNIT)
    for i in range(n):
        mdl.one[i] = np.array([float(v * UNIT) for v in t["one"][i]])
    for (i, j) in inband:
        mdl.add_pair(i, j, np.array([[float(v * UNIT) for v in row] for row in t["pair"][pkey(i, j)]]))
    return mdl


def main(seq, bb, tau, m, w):
    resource.setrlimit(resource.RLIMIT_AS, (6 * 1024**3, 6 * 1024**3))
    t0 = time.time()
    print(f"export_cert.py {seq} {bb} {tau} m={m} w={w}   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    setup_data = L.setup(seq, bb, tau, "gbn2")
    G, c0, h, J, x0, E0 = setup_data
    n, k = G.ns, [int(v) for v in G.k]
    x0 = [int(v) for v in x0]
    M = m - 1
    assert 1 <= w <= max(1, n - 1)
    inband = [(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= w]
    active = [i for i in range(n) if k[i] > 1]
    na = len(active)
    print(f"  instance: n = {n}, states per site {sorted(set(k))}, anchor {x0}, E(anchor) = {E0:.6f} kcal/mol; "
          f"in-band pairs {len(inband)} of {n * (n - 1) // 2}")

    # ---- step A: sums over exclusion sets (P3's closed form, as p6lib computes and caches them)
    sup = L.EnvelopeSup(G)
    GF = L.GFBound2(G, x0, sup, K=m)
    Gam, S, Gp, srcp = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, "gbn2", m, w=w)
    stem = os.path.join(os.path.dirname(L.__file__), "out", f"pairsums_{L.tagname(seq, bb, tau, 'gbn2')}_m{m}")
    cands = [stem + ".npz"] + [f"{stem}_w{ww}.npz" for ww in range(n - 1, w - 1, -1)]
    z = None
    for fn in cands:
        if os.path.exists(fn):
            zz = np.load(fn)
            if list(zz["anchor"]) == list(x0):
                z = zz
                break
    assert z is not None, "pair-sum file not found after load_or_compute_pair_sums"
    tot = {}
    for e, t in zip(z["excl"], z["tot"]):
        tot[tuple(int(v) for v in e if v >= 0)] = float(t)
    assert abs(tot[()] - Gam) == 0.0
    print(f"  step A: {len(tot)} sums ({srcp}); Gamma = {Gam:.9g} kcal/mol")
    # how well the independently computed sums satisfy the two counting identities (evidence about the assumed
    # relative accuracy of a sum; the checker's test A0 fails if the published intervals contradict the identities)
    Sx = [Fraction(tot[()]) - Fraction(tot[(i,)]) for i in range(n)]
    d1 = abs(m * Fraction(tot[()]) - sum(Sx))
    msg = f"  counting identities among the sums, exact arithmetic on the doubles: |m Gamma - sum_i S_i| = {float(d1):.3e}"
    if all((i, j) in tot for i in range(n) for j in range(i + 1, n)):
        d2 = max(abs((m - 1) * Sx[i] - sum(Fraction(tot[()]) - Fraction(tot[(i,)]) - Fraction(tot[(j,)])
                                           + Fraction(tot[(min(i, j), max(i, j))]) for j in range(n) if j != i))
                 for i in range(n))
        msg += f", max_i |(m-1) S_i - sum_j G_ij| = {float(d2):.3e}"
    print(msg + f" kcal/mol; the interval slack 3e-9 Gamma is {3e-9 * Gam:.3e}")

    def interval(v):
        up = ce(v)
        lo = max(0, math.floor(Fraction(float(v)) * (1 - REL_LO) / UNIT))
        return [lo, up]

    stepA = dict(Gamma=interval(tot[()]),
                 Gamma_minus_i=[interval(tot[(i,)]) for i in range(n)],
                 Gamma_minus_ij={pkey(i, j): interval(tot[(i, j)]) for (i, j) in inband})

    # ---- anchored terms on the ball, P3's banded models of the evaluated part (no penalties)
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, "gbn2", verbose=True)
    print(f"  ball of radius {M}: {nball} evaluated values of g ({os.path.basename(str(srcb))})")
    A_lo, A_up = pw.build_band_models(G.k, x0, c0, h, J, d, w, 0.0, M, gam=None)
    A_lower = tables_to_int(A_lo, n, k, inband, fl)
    A_upper = tables_to_int(A_up, n, k, inband, ce)

    # ---- smallest integer penalties satisfying B1-B3
    eps = EPS_G / UNIT
    c2 = math.comb(m, 2)
    psi_site = 2 * eps
    psi_pair = eps * sum(Fraction(math.comb(na - 2, s - 2) * 2 ** s, math.comb(s, 2)) for s in range(2, M + 1)) if na >= 2 else Fraction(0)
    G_lo, G_up = stepA["Gamma"]
    Gi = stepA["Gamma_minus_i"]
    Gij = stepA["Gamma_minus_ij"]
    pair_up = {p: G_up - Gi[p[0]][0] - Gi[p[1]][0] + Gij[pkey(*p)][1] for p in inband}
    pair_lo = {p: max(0, G_lo - Gi[p[0]][1] - Gi[p[1]][1] + Gij[pkey(*p)][0]) for p in inband}
    pen_c = math.ceil(eps)
    pen_b = {}
    for (i, j) in inband:
        if k[i] > 1 and k[j] > 1:
            pen_b[pkey(i, j)] = math.ceil(Fraction(max(pair_up[(i, j)], 0), c2) + psi_pair)
        else:
            pen_b[pkey(i, j)] = 0
    pen_a = []
    for i in range(n):
        if k[i] == 1:
            pen_a.append(0)
            continue
        s_up = G_up - Gi[i][0]
        inb = [(min(i, j), max(i, j)) for j in range(n) if j != i and abs(i - j) <= w]
        nout = sum(1 for j in active if j != i and abs(i - j) > w)
        far = max(0, (m - 1) * s_up - sum(pair_lo[p] for p in inb))
        pen_a.append(math.ceil(psi_site + Fraction(nout, 2) * psi_pair + Fraction(far, 2 * c2)))
    penalty = dict(c=pen_c, a=pen_a, b=pen_b)

    def with_penalty(At, sign):
        t = dict(const=At["const"] + sign * pen_c,
                 one=[[At["one"][i][x] + (sign * pen_a[i] if x != x0[i] else 0) for x in range(k[i])] for i in range(n)],
                 pair={})
        for (i, j) in inband:
            key = pkey(i, j)
            t["pair"][key] = [[At["pair"][key][x][y] + (sign * pen_b[key] if (x != x0[i] and y != x0[j]) else 0)
                               for y in range(k[j])] for x in range(k[i])]
        return t

    m_lower = with_penalty(A_lower, -1)
    m_upper = with_penalty(A_upper, +1)

    # ---- the claim: double-precision transfer matrix of the integer tables, widened
    beta_double = L.BETA
    beta = Fraction(beta_double)
    lz_mlow = float_band_model(m_lower, n, k, w, inband).lnZ(beta_double)          # >= ln Z(E)
    lz_mupp = float_band_model(m_upper, n, k, w, inband).lnZ(beta_double)          # <= ln Z(E)
    claim_lo = Fraction(math.floor((lz_mupp - 5e-9) * 10 ** 9), 10 ** 9)
    claim_up = Fraction(math.ceil((lz_mlow + 5e-9) * 10 ** 9), 10 ** 9)

    cert = dict(format="metricchain-sandwich/1", unit_log2=UNIT_LOG2,
                beta=dict(num=beta.numerator, den=beta.denominator),
                eps_g=dict(num=EPS_G.numerator, den=EPS_G.denominator),
                instance=dict(n=n, k=k, anchor=x0, order_m=m, band_w=w),
                stepA=stepA, penalty=penalty, A_lower=A_lower, A_upper=A_upper, m_lower=m_lower, m_upper=m_upper,
                claim=dict(lnZ_lower=dict(num=claim_lo.numerator, den=claim_lo.denominator),
                           lnZ_upper=dict(num=claim_up.numerator, den=claim_up.denominator)),
                annotations=dict(label=f"{peptide_name(seq)}, backbone code {bb}, clash threshold {tau:.2f}, ff14SB vacuum terms + "
                                       f"GBn2 polarisation term (OpenMM 8.6.1 parameter files), order {m}, band {w}, banded pair penalties",
                                 producer="experiments/science/sandwich_cert/export_cert.py (science division, branch research/scientific-translation)",
                                 stepA="sums of the closed form of workstream P3 (Proposition 4) over exclusion sets, as computed by "
                                       "ws_P6/p6lib.py (GFBatch); interval = [value * (1 - 3e-9) rounded down, value rounded up]",
                                 tables="A_lower / A_upper: ws_P3/pwmodel.py build_band_models without remainder terms, entries rounded "
                                        "down / up to the unit",
                                 temperature="beta is the double nearest to 1/(0.0019872041 * 300) per kcal/mol, written exactly",
                                 note="annotations are not read by any checker"))
    os.makedirs(os.path.join(HERE, "certs"), exist_ok=True)
    out = os.path.join(HERE, "certs", f"sandwich_{seq}_{bb}_m{m}_w{w}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(cert, fh, separators=(",", ":"))
        fh.write("\n")
    print(f"  written: {os.path.relpath(out, HERE)} ({os.path.getsize(out)} bytes)")
    print(f"  claim (integer tables): ln Z(E) in [{float(claim_lo):.9f}, {float(claim_up):.9f}], width {float(claim_up - claim_lo):.3e} nats")

    # ---- comparisons (not part of the certificate)
    lo_f, up_f, info = L.make_models(seq, bb, tau, m, w, "B", setup_data=setup_data)
    print(f"  for comparison, the floating-point pipeline (p6lib.make_models, form B): "
          f"ln Z(m_-) = {lo_f.lnZ():.12f}, ln Z(m_+) = {up_f.lnZ():.12f}")
    print(f"     the integer tables (double-precision transfer matrix):                 "
          f"ln Z(m_lower) = {lz_mlow:.12f}, ln Z(m_upper) = {lz_mupp:.12f}")
    print(f"     effect of the integer rounding on ln Z: {lz_mlow - lo_f.lnZ():+.3e} (m_lower), {lz_mupp - up_f.lnZ():+.3e} (m_upper) nats; "
          f"the claim widens each end by 5e-9 and rounds outwards to 9 decimals")
    nent = 1 + n + len(inband)
    print(f"     a state uses {nent} entries of a table; each entry of A_lower / A_upper moved by less than one unit: "
          f"less than {nent * float(UNIT):.3e} kcal/mol per state")
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    gs_f, g2_f = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
    da = max(abs(float(pen_a[i] * UNIT) - gs_f[i]) for i in range(n))
    db = max(abs(float(pen_b[pkey(i, j)] * UNIT) - g2_f[i, j]) for (i, j) in inband)
    print(f"     integer penalties against p6lib's floating-point ones: largest difference {da:.3e} (site), {db:.3e} (pair) kcal/mol; "
          f"largest site penalty {max(gs_f):.6g}, largest pair penalty {g2_f.max():.6g} kcal/mol")
    total = 1
    for v in k:
        total *= v
    if total <= 2_000_000:
        st, gvals, srce = L.enumerate_g(G, seq, bb, tau, "gbn2", verbose=False)
        E = pw.f_energy(st, c0, h, J) + np.asarray(gvals, dtype=float).reshape(-1)
        elo = np.array([float(v * UNIT) for v in int_model_energy(m_lower, st, inband)])
        eup = np.array([float(v * UNIT) for v in int_model_energy(m_upper, st, inband)])
        viol = int((elo > E + 1e-12).sum() + (eup < E - 1e-12).sum())
        lnz = float(np.log(np.exp(-beta_double * (E - E.min())).sum()) - beta_double * E.min())
        print(f"  enumeration ({total} states): states with m_lower > E or m_upper < E: {viol} (must be 0); "
              f"smallest margins {float((E - elo).min()):.3e}, {float((eup - E).min()):.3e} kcal/mol")
        print(f"     exact ln Z(E) = {lnz:.9f}; inside the claimed bracket: {float(claim_lo) <= lnz <= float(claim_up)}")
        assert viol == 0 and float(claim_lo) <= lnz <= float(claim_up)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"ALL DONE   computed in {time.time() - t0:.1f} s   peak memory {peak:.0f} MB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
