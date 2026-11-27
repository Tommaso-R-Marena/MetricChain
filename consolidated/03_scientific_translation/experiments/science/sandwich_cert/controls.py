#!/usr/bin/env python3
"""Controls for the reference checker check_cert.py (format `metricchain-sandwich/1`).

    python3 -B controls.py [--vectors DIR]       exit status 0 iff every control behaved as expected
                                                  (--vectors: also write the mutated Val6 files and EXPECTED.tsv to DIR)

Part 0  PLANTED TRUTH for the band recursion: on random small band models the checker's exact minimum equals the
        minimum by enumeration, and its interval enclosure of ln Z contains the sum by enumeration (50 digits).
Part 1  PLANTED TRUTH for the covering inequalities: random non-negative constants c_T on all sets of m sites
        (known, so the true right side of the covering is computable at every state), random bands, sites with a
        single state; the smallest integer penalties allowed by B1-B3 are computed here (independently of the
        exporter), accepted by the checker's (A0) and (B), and then compared with the true right side at EVERY
        pattern of changed sites by enumeration.  For order m = 2 with every pair in the band the inequalities
        are also necessary: lowering any single number by one unit must produce a violated pattern.
Part 2  MUTATIONS of the two published certificates: each must be rejected for the stated reason -- or accepted,
        where the mutated file is still a valid certificate (a checker that rejected those would be testing
        equality with our producer, not validity).
"""
import copy
import itertools
import json
import math
import os
import random
import sys
import tempfile
import time
from fractions import Fraction

from mpmath import iv, mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import check_cert as C                                        # noqa: E402

results = []                                                  # (part, name, expected, got, ok)
VEC_DIR = None                                                # --vectors DIR: write the mutated Val6 files there
VEC_ROWS = []


def record(part, name, expected, got):
    ok = got.startswith(expected)
    results.append((part, name, expected, got, ok))
    print(f"  [{'ok' if ok else 'UNEXPECTED'}] {name:<58s} expected: {expected:<24s} got: {got[:90]}")


def pkey(i, j):
    return f"{i},{j}"


# ======================================================================================================= part 0
def random_band_model(rng, n, k, w, lo=-40, hi=40):
    inband = [(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= w]
    return dict(const=rng.randint(lo, hi), one=[[rng.randint(lo, hi) for _ in range(k[i])] for i in range(n)],
                pair={pkey(i, j): [[rng.randint(lo, hi) for _ in range(k[j])] for _ in range(k[i])] for (i, j) in inband}), inband


def model_value(t, x, inband):
    return t["const"] + sum(t["one"][i][x[i]] for i in range(len(x))) + sum(t["pair"][pkey(i, j)][x[i]][x[j]] for (i, j) in inband)


def part0():
    print("Part 0: band recursion against enumeration")
    rng = random.Random(20261127)
    iv.dps = 30
    mp.dps = 50
    nmin = nz = 0
    worst = Fraction(0)
    for trial in range(60):
        n = rng.randint(1, 6)
        k = [rng.randint(1, 3) for _ in range(n)]
        w = rng.randint(1, max(1, n - 1))
        t, inband = random_band_model(rng, n, k, w)
        vals = [model_value(t, x, inband) for x in itertools.product(*[range(v) for v in k])]
        if C.band_minimum(t, n, k, w) == min(vals):
            nmin += 1
        beta = Fraction(rng.randint(1, 9), rng.randint(1, 9))
        unit_log2 = -rng.randint(0, 6)
        enc = C.lnZ_enclosure(t, n, k, w, iv.mpf(beta.numerator) / iv.mpf(beta.denominator), unit_log2)
        sc = -mp.mpf(beta.numerator) / mp.mpf(beta.denominator) * mp.mpf(2) ** unit_log2
        exact = mp.log(mp.fsum(mp.exp(sc * v) for v in vals))
        a, b = C.endpoints(enc)
        inside = (mp.mpf(a.numerator) / a.denominator <= exact + mp.mpf(10) ** -45) and (exact - mp.mpf(10) ** -45 <= mp.mpf(b.numerator) / b.denominator)
        if inside:
            nz += 1
        worst = max(worst, b - a)
    record(0, "exact minimum equals enumeration (60 random models)", "60 of 60", f"{nmin} of 60")
    record(0, "ln Z enclosure contains enumeration (60 random models)", "60 of 60", f"{nz} of 60; widest enclosure {float(worst):.1e}")


# ======================================================================================================= part 1
def covering_instance(rng, n, k, m, w, eps, cmax):
    """a certificate-like object with KNOWN constants c_T (exact step-A sums as degenerate intervals) and the smallest
    integer penalties that B1-B3 allow.  unit = 1, eps_g = eps (an integer)."""
    act = [i for i in range(n) if k[i] > 1]
    na = len(act)
    cT = {T: rng.randint(0, cmax) for T in itertools.combinations(range(n), m)}
    inband = [(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= w]

    def avoid(A):
        return sum(v for T, v in cT.items() if not (set(T) & set(A)))
    stepA = dict(Gamma=[avoid(())] * 2, Gamma_minus_i=[[avoid((i,))] * 2 for i in range(n)],
                 Gamma_minus_ij={pkey(i, j): [avoid((i, j))] * 2 for (i, j) in inband})
    M, c2 = m - 1, math.comb(m, 2)
    psi_site = 2 * eps
    psi_pair = eps * sum(Fraction(math.comb(na - 2, s - 2) * 2 ** s, math.comb(s, 2)) for s in range(2, M + 1)) if na >= 2 else Fraction(0)
    G = {(i, j): sum(v for T, v in cT.items() if i in T and j in T) for i in range(n) for j in range(i + 1, n)}
    b = {pkey(i, j): (math.ceil(Fraction(G[(i, j)], c2) + psi_pair) if (k[i] > 1 and k[j] > 1) else 0) for (i, j) in inband}
    a = []
    for i in range(n):
        if k[i] == 1:
            a.append(0)
            continue
        far = sum(G[(min(i, j), max(i, j))] for j in range(n) if j != i and abs(i - j) > w)     # ALL out-of-band sites
        nout = sum(1 for j in act if j != i and abs(i - j) > w)
        a.append(math.ceil(psi_site + Fraction(nout, 2) * psi_pair + Fraction(far, 2 * c2)))
    zero = dict(const=0, one=[[0] * k[i] for i in range(n)], pair={pkey(i, j): [[0] * k[j] for _ in range(k[i])] for (i, j) in inband})
    cert = dict(format=C.FORMAT, unit_log2=0, beta=dict(num=1, den=1), eps_g=dict(num=eps, den=1),
                instance=dict(n=n, k=k, anchor=[0] * n, order_m=m, band_w=w), stepA=stepA,
                penalty=dict(c=eps, a=a, b=b), A_lower=zero, A_upper=copy.deepcopy(zero))
    return cert, cT, act, inband


def true_right_side(Sset, cT, eps, M):
    """eps (1 + sum over U inside S, 1 <= |U| <= M, of 2^|U|) + sum of c_T inside S"""
    s = len(Sset)
    r = eps * (1 + sum(math.comb(s, u) * 2 ** u for u in range(1, M + 1)))
    return r + sum(v for T, v in cT.items() if set(T) <= Sset)


def penalty_at(Sset, pen, inband):
    return pen["c"] + sum(pen["a"][i] for i in Sset) + sum(pen["b"][pkey(i, j)] for (i, j) in inband if i in Sset and j in Sset)


def part1():
    print("Part 1: the covering inequalities against known constants, every pattern of changed sites")
    rng = random.Random(4711)
    ninst = npat = nacc = 0
    minmargin = None
    viol = 0
    for trial in range(200):
        n = rng.randint(2, 9)
        k = [rng.choice([1, 2, 3, 3]) for _ in range(n)]
        m = rng.randint(2, min(5, n))
        w = rng.randint(1, max(1, n - 1))
        eps = rng.randint(0, 5)
        cert, cT, act, inband = covering_instance(rng, n, k, m, w, eps, cmax=rng.choice([0, 3, 50, 10 ** 6]))
        ninst += 1
        try:
            C.check_consistency(cert, n, k, m, w, inband)
            C.check_covering(cert, n, k, [0] * n, m, w, inband)
            nacc += 1
        except C.Rejected as exc:
            print("     rejected:", exc)
            continue
        for r in range(len(act) + 1):
            for Sset in itertools.combinations(act, r):
                Sset = set(Sset)
                margin = penalty_at(Sset, cert["penalty"], inband) - true_right_side(Sset, cT, eps, m - 1)
                npat += 1
                if margin < 0:
                    viol += 1
                if minmargin is None or margin < minmargin:
                    minmargin = margin
    record(1, "smallest penalties accepted by (A0) and (B)", f"{ninst} of {ninst}", f"{nacc} of {ninst}")
    record(1, "penalty >= true right side at every pattern", "0 violations", f"{viol} violations in {npat} patterns of {ninst} instances; smallest margin {minmargin}")
    # necessity for order 2 with every pair in the band: one unit less on any number breaks a pattern, and the checker says so
    broke = caught = tried = 0
    for trial in range(40):
        n = rng.randint(2, 6)
        k = [rng.choice([2, 3]) for _ in range(n)]
        eps = rng.randint(1, 4)
        cert, cT, act, inband = covering_instance(rng, n, k, 2, n - 1, eps, cmax=20)
        for kind, idx in [("c", None)] + [("a", i) for i in range(n)] + [("b", pkey(i, j)) for (i, j) in inband]:
            mut = copy.deepcopy(cert)
            if kind == "c":
                mut["penalty"]["c"] -= 1
            else:
                mut["penalty"][kind][idx] -= 1
            tried += 1
            bad = any(penalty_at(set(Sset), mut["penalty"], inband) < true_right_side(set(Sset), cT, eps, 1)
                      for r in range(len(act) + 1) for Sset in itertools.combinations(act, r))
            broke += bad
            try:
                C.check_covering(mut, n, k, [0] * n, 2, n - 1, inband)
            except C.Rejected:
                caught += 1
    record(1, "order 2, full band: one unit less breaks a pattern", f"{tried} of {tried}", f"{broke} of {tried}")
    record(1, "order 2, full band: the checker rejects each of them", f"{tried} of {tried}", f"{caught} of {tried}")


# ======================================================================================================= part 2
def rebuild_m(c):
    """m_lower = A_lower - penalty, m_upper = A_upper + penalty (written here independently of exporter and checker)."""
    ins = c["instance"]
    n, k, x0, w = ins["n"], ins["k"], ins["anchor"], ins["band_w"]
    pen = c["penalty"]
    for name, src, sg in (("m_lower", "A_lower", -1), ("m_upper", "A_upper", 1)):
        A = c[src]
        t = dict(const=A["const"] + sg * pen["c"], one=[], pair={})
        for i in range(n):
            t["one"].append([A["one"][i][x] + (sg * pen["a"][i] if x != x0[i] else 0) for x in range(k[i])])
        for key, tab in A["pair"].items():
            i, j = (int(v) for v in key.split(","))
            t["pair"][key] = [[tab[x][y] + (sg * pen["b"][key] if x != x0[i] and y != x0[j] else 0) for y in range(k[j])] for x in range(k[i])]
        c[name] = t


def verdict_of_text(text, tmp, tag):
    path = os.path.join(tmp, tag + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    try:
        C.check(C.load(path))
    except C.Rejected as exc:
        return "REJECTED: " + str(exc)
    return "ACCEPTED"


def rat(q):
    return dict(num=q.numerator, den=q.denominator)


def part2(path, label, heavy):
    print(f"Part 2: mutations of {os.path.relpath(path, HERE)}")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    base = json.loads(text)
    ins = base["instance"]
    n, k, x0, m, w = ins["n"], ins["k"], ins["anchor"], ins["order_m"], ins["band_w"]
    c2 = math.comb(m, 2)
    with tempfile.TemporaryDirectory() as tmp:
        def emit(name, mtext, expected):
            """run the checker on the text; with --vectors, keep the file (first instance only) with its expected verdict"""
            got = verdict_of_text(mtext, tmp, "m")
            record(2, f"{label}: {name}", expected, got)
            if VEC_DIR is not None and heavy:
                slug = "".join(ch if ch.isalnum() else "_" for ch in name.lower()).strip("_")
                while "__" in slug:
                    slug = slug.replace("__", "_")
                fn = f"{len(VEC_ROWS) + 1:02d}_{slug[:60]}.json"
                with open(os.path.join(VEC_DIR, fn), "w", encoding="utf-8") as fh:
                    fh.write(mtext)
                verdict_word, _, why = expected.partition(": ")
                VEC_ROWS.append((fn, verdict_word, why or "-", name))

        def run(name, mutate, expected, consistent=False):
            c = copy.deepcopy(base)
            mutate(c)
            if consistent:
                rebuild_m(c)
            emit(name, json.dumps(c, separators=(",", ":")) + "\n", expected)

        emit("unchanged file", text, "ACCEPTED")
        i0 = n // 2
        key = pkey(i0, i0 + 1)
        nz = [x for x in range(k[i0]) if x != x0[i0]][0]
        nz1 = [x for x in range(k[i0 + 1]) if x != x0[i0 + 1]][0]

        # ---- covering
        run("pair number lowered by one unit", lambda c: c["penalty"]["b"].__setitem__(key, c["penalty"]["b"][key] - 1), "REJECTED: B1")
        run("pair number lowered, tables rebuilt", lambda c: c["penalty"]["b"].__setitem__(key, c["penalty"]["b"][key] - 1), "REJECTED: B1", True)
        run("site number lowered by one unit", lambda c: c["penalty"]["a"].__setitem__(i0, c["penalty"]["a"][i0] - 1), "REJECTED: B2")
        run("site number lowered, tables rebuilt", lambda c: c["penalty"]["a"].__setitem__(i0, c["penalty"]["a"][i0] - 1), "REJECTED: B2", True)
        run("constant lowered by one unit", lambda c: c["penalty"].__setitem__("c", c["penalty"]["c"] - 1), "REJECTED: B3")
        run("constant lowered, tables rebuilt", lambda c: c["penalty"].__setitem__("c", c["penalty"]["c"] - 1), "REJECTED: B3", True)
        run("eps_g doubled", lambda c: c["eps_g"].__setitem__("num", 2 * c["eps_g"]["num"]), "REJECTED: B3")

        def eps_doubled_const_raised(c):
            c["eps_g"]["num"] *= 2
            c["penalty"]["c"] *= 2
        run("eps_g doubled, constant doubled, tables rebuilt", eps_doubled_const_raised, "REJECTED: B1", True)
        run("step A: upper end of Gamma raised by 100 units", lambda c: c["stepA"]["Gamma"].__setitem__(1, c["stepA"]["Gamma"][1] + 100), "REJECTED: B1")
        run("step A: lower end of Gamma^(-i) lowered by 100 units",
            lambda c: c["stepA"]["Gamma_minus_i"][i0].__setitem__(0, c["stepA"]["Gamma_minus_i"][i0][0] - 100), "REJECTED: B1")

        def pair_excl_lo(c):
            v = c["stepA"]["Gamma_minus_ij"][key]
            v[0] -= 200 * c2
        s_lo, s_up, pair_lo, pair_up = C.step_a_sums(base, n, w, [(i, j) for i in range(n) for j in range(i + 1, n) if j - i <= w])
        if pair_lo[(i0, i0 + 1)] > 200 * c2:
            run("step A: lower end of Gamma^(-i,-j) lowered by 200 C(m,2) units", pair_excl_lo, "REJECTED: B2")
        else:
            print("     (control on the lower end of a pair exclusion not applicable: that pair sum's lower end is 0)")

        # ---- data consistency
        def swap_interval(c):
            v = c["stepA"]["Gamma"]
            v[0], v[1] = v[1] + 1, v[0]
        run("step A: interval of Gamma with lo > up", swap_interval, "REJECTED: malformed")
        run("step A: Gamma^(-i) above Gamma", lambda c: c["stepA"]["Gamma_minus_i"].__setitem__(i0, [c["stepA"]["Gamma"][1] + 1, c["stepA"]["Gamma"][1] + 2]),
            "REJECTED: A0")
        run("order m raised by one (data of the other order)", lambda c: c["instance"].__setitem__("order_m", m + 1), "REJECTED: A0")
        run("order m lowered by one (data of the other order)", lambda c: c["instance"].__setitem__("order_m", m - 1), "REJECTED: A0")

        def swap_A(c):
            c["A_lower"], c["A_upper"] = c["A_upper"], c["A_lower"]
        run("A_lower and A_upper exchanged, tables rebuilt", swap_A, "REJECTED: A0", True)

        # ---- tables
        run("entry of m_lower.one raised by one unit", lambda c: c["m_lower"]["one"][i0].__setitem__(nz, c["m_lower"]["one"][i0][nz] + 1), "REJECTED: D")
        run("entry of m_upper.pair lowered by one unit",
            lambda c: c["m_upper"]["pair"][key][nz].__setitem__(nz1, c["m_upper"]["pair"][key][nz][nz1] - 1), "REJECTED: D")
        run("entry of A_lower.one raised by one unit, m_lower unchanged",
            lambda c: c["A_lower"]["one"][i0].__setitem__(nz, c["A_lower"]["one"][i0][nz] + 1), "REJECTED: D")
        run("constant of m_lower raised by one unit", lambda c: c["m_lower"].__setitem__("const", c["m_lower"]["const"] + 1), "REJECTED: D")
        run("penalty applied at the anchor state too (m_lower.one)",
            lambda c: c["m_lower"]["one"][i0].__setitem__(x0[i0], c["m_lower"]["one"][i0][x0[i0]] - c["penalty"]["a"][i0]), "REJECTED: D")
        run("anchor of one site changed", lambda c: c["instance"]["anchor"].__setitem__(i0, nz), "REJECTED: D")

        # ---- form
        run("unknown format name", lambda c: c.__setitem__("format", "metricchain-sandwich/2"), "REJECTED: malformed")
        run("extra top-level key", lambda c: c.__setitem__("comment", 1), "REJECTED: malformed")
        run("in-band pair missing from m_lower.pair", lambda c: c["m_lower"]["pair"].pop(key), "REJECTED: malformed")
        run("anchor out of range", lambda c: c["instance"]["anchor"].__setitem__(0, k[0]), "REJECTED: malformed")
        run("negative pair number", lambda c: c["penalty"]["b"].__setitem__(key, -1), "REJECTED: malformed")
        run("band width changed", lambda c: c["instance"].__setitem__("band_w", max(1, w - 1) if w > 1 else w + 1), "REJECTED: malformed")
        assert text.count('"unit_log2":-40') == 1
        emit("a floating-point literal", text.replace('"unit_log2":-40', '"unit_log2":-40.0'), "REJECTED: malformed")
        emit("a duplicate key", text.replace('"unit_log2":-40', '"unit_log2":-40,"unit_log2":-40'), "REJECTED: malformed")
        emit("truncated file", text[:len(text) // 2], "REJECTED: malformed")

        # ---- valid variants that must be ACCEPTED
        run("VALID: pair number raised by one unit, tables rebuilt", lambda c: c["penalty"]["b"].__setitem__(key, c["penalty"]["b"][key] + 1), "ACCEPTED", True)
        run("VALID: annotations removed", lambda c: c.pop("annotations"), "ACCEPTED")

        # ---- ln Z: one step of 1e-12 on either side of the checker's own enclosure
        if heavy:
            rep = C.check(base)
            lo_end = C.endpoints(rep["lnZ_m_upper"])[0]
            up_end = C.endpoints(rep["lnZ_m_lower"])[1]
            q = 10 ** 12
            run("VALID: lower claim just below ln Z(m_upper) (1e-12)", lambda c: c["claim"].__setitem__("lnZ_lower", rat(Fraction(math.floor(lo_end * q), q))), "ACCEPTED")
            run("lower claim just above ln Z(m_upper) (1e-12)", lambda c: c["claim"].__setitem__("lnZ_lower", rat(Fraction(math.floor(lo_end * q) + 1, q))), "REJECTED: E")
            run("VALID: upper claim just above ln Z(m_lower) (1e-12)", lambda c: c["claim"].__setitem__("lnZ_upper", rat(Fraction(math.ceil(up_end * q), q))), "ACCEPTED")
            run("upper claim just below ln Z(m_lower) (1e-12)", lambda c: c["claim"].__setitem__("lnZ_upper", rat(Fraction(math.ceil(up_end * q) - 1, q))), "REJECTED: E")

            def empty(c):
                c["claim"]["lnZ_lower"], c["claim"]["lnZ_upper"] = c["claim"]["lnZ_upper"], c["claim"]["lnZ_lower"]
            run("claimed bracket empty (ends exchanged)", empty, "REJECTED: E")
            run("beta doubled", lambda c: c["beta"].__setitem__("num", 2 * c["beta"]["num"]), "REJECTED: E")
            run("unit changed to 2^-39 (integers unchanged)", lambda c: c.__setitem__("unit_log2", -39), "REJECTED: E")
            run("unit changed to 2^-41 (integers unchanged)", lambda c: c.__setitem__("unit_log2", -41), "REJECTED: B3")

            def wrong_rounding(c):
                # what a producer would write that rounded A_lower up and A_upper down: every entry off by one unit inwards
                for name, sg in (("A_lower", 1), ("A_upper", -1)):
                    c[name]["const"] += sg
                    c[name]["one"] = [[v + sg for v in row] for row in c[name]["one"]]
                    c[name]["pair"] = {kk: [[v + sg for v in row] for row in tab] for kk, tab in c[name]["pair"].items()}
            run("every entry of A_lower up, of A_upper down, one unit; rebuilt", wrong_rounding, "REJECTED: A0", True)
        else:
            run("lower claim raised by 1e-8", lambda c: c["claim"].__setitem__(
                "lnZ_lower", rat(Fraction(c["claim"]["lnZ_lower"]["num"], c["claim"]["lnZ_lower"]["den"]) + Fraction(1, 10 ** 8))), "REJECTED: E")
            run("upper claim lowered by 1e-8", lambda c: c["claim"].__setitem__(
                "lnZ_upper", rat(Fraction(c["claim"]["lnZ_upper"]["num"], c["claim"]["lnZ_upper"]["den"]) - Fraction(1, 10 ** 8))), "REJECTED: E")


def main():
    global VEC_DIR
    t0 = time.time()
    print("controls.py   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    if len(sys.argv) == 3 and sys.argv[1] == "--vectors":
        VEC_DIR = os.path.abspath(sys.argv[2])
        os.makedirs(VEC_DIR, exist_ok=True)
        print("  writing the mutated Val6 files to", os.path.relpath(VEC_DIR, HERE))
    iv.dps = 30
    part0()
    part1()
    part2(os.path.join(HERE, "certs", "sandwich_V6_E_m4_w5.json"), "Val6", heavy=True)
    part2(os.path.join(HERE, "certs", "sandwich_V20_P2_m5_w8.json"), "Val20", heavy=False)
    if VEC_DIR is not None:
        with open(os.path.join(VEC_DIR, "EXPECTED.tsv"), "w", encoding="utf-8") as fh:
            fh.write("file\tverdict\tfirst failing check of the reference checker\tdescription\n")
            for row in VEC_ROWS:
                fh.write("\t".join(row) + "\n")
        print(f"  {len(VEC_ROWS)} test vectors and EXPECTED.tsv written")
    bad = [r for r in results if not r[4]]
    print(f"controls: {len(results) - len(bad)} of {len(results)} behaved as expected"
          + ("" if not bad else "; UNEXPECTED: " + "; ".join(r[1] for r in bad)))
    print(f"ALL DONE   {time.time() - t0:.1f} s")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
