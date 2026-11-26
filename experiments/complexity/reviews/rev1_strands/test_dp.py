# test_dp.py -- (1) cross-validate the transfer-matrix DP against the brute-force enumerator on every
# instance of test_main.py; (2) run the DP on larger instances (3-PARTITION / 4-PARTITION shaped and
# random ones) and check Theorem 1 / Theorem 3(1) for models satisfying (H0)-(H2); (3) report what
# happens for models violating (H2).
import sys, random, subprocess, itertools, math, os
from multiprocessing import Pool
from lib import *
import test_main

DP = os.path.join(HERE, "dp")


def run_dp(a, m, B):
    out = subprocess.run([DP, str(m), str(B)] + [str(x) for x in a], capture_output=True, text=True, check=True).stdout
    res = {"models": []}
    for line in out.splitlines():
        if line.startswith("CONNECTED"):
            res["conn"] = int(line.split()[1])
        elif line.startswith("MODEL"):
            p = [x.strip() for x in line.split("|")]
            res["models"].append(dict(name=p[1], sigma=int(p[2].split()[1]), mfe=int(p[3].split()[1]), nmin=int(p[4].split()[1])))
    return res


def til_fast(a, m, B):
    """Til by DFS over the bins (ordered arrangements): number of sequences of all labelled items whose
    prefix sums hit every multiple of B"""
    n = len(a)
    from functools import lru_cache

    @lru_cache(None)
    def rec(mask, fill):
        if mask == (1 << n) - 1:
            return 1 if fill == 0 else 0
        tot = 0
        for i in range(n):
            if not mask & (1 << i):
                f = fill + a[i]
                if f < B:
                    tot += rec(mask | (1 << i), f)
                elif f == B:
                    tot += rec(mask | (1 << i), 0)
        return tot

    return rec(0, 0)


def check(inst):
    a, m, B = inst
    n = len(a)
    M = m * B - n
    T = til_fast(tuple(a), m, B)
    pk = T > 0
    r = run_dp(a, m, B)
    fails = []
    viol = []
    for mod in r["models"]:
        s = mod["sigma"]
        isviol = mod["name"].startswith("VIOL")
        ok_yes = (mod["mfe"] == s * M and mod["nmin"] == T)
        ok_no = (mod["mfe"] != s * M and mod["mfe"] >= s * (M - 1))
        if isviol:
            # does the YES/NO decision via "MFE == sigma*M" still work, and are minima still the tilings?
            decides = (mod["mfe"] == s * M) == pk
            viol.append((mod["name"], mod["mfe"], s * M, mod["nmin"], decides, (mod["nmin"] == T) if pk else None))
        else:
            if pk and not ok_yes:
                fails.append("[%s] YES: MFE %d (sigma*M %d), #min %d (Til %d)" % (mod["name"], mod["mfe"], s * M, mod["nmin"], T))
            if (not pk) and not ok_no:
                fails.append("[%s] NO: MFE %d, sigma*M %d, sigma*(M-1) %d" % (mod["name"], mod["mfe"], s * M, s * (M - 1)))
    so = r["models"][0]
    return dict(a=a, m=m, B=B, n=n, pk=pk, M=M, Til=T, conn=r["conn"], mfe=so["mfe"], nmin=so["nmin"], fails=fails, viol=viol)


def random_instance(rng, m, B, n):
    """random composition of m*B into n positive parts (no constraint on packability)"""
    total = m * B
    cuts = sorted(rng.sample(range(1, total), n - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [total])]
    return tuple(parts)


def random_yes_instance(rng, m, B, n):
    """random instance that is packable by construction: split each block into parts"""
    per = [1] * m
    for _ in range(n - m):
        per[rng.randrange(m)] += 1
    parts = []
    for t in range(m):
        k = min(per[t], B)
        cuts = sorted(rng.sample(range(1, B), k - 1)) if k > 1 else []
        parts += [b - a for a, b in zip([0] + cuts, cuts + [B])]
    rng.shuffle(parts)
    return tuple(parts)


if __name__ == "__main__":
    # ---------- (1) DP vs brute force
    print("== (1) DP vs brute-force enumerator (connected count, stack-only MFE, #min labelled)")
    bad = 0
    cnt = 0
    for a, m, B, mode in (dict.fromkeys(test_main.INSTANCES) if "--skip1" not in sys.argv else []):
        res = run_enum(system(a, m, B), prune=(mode in "PL"), orbit=(mode != "L" and mu_fact(a) <= 24 and m * B <= 10), lean=(mode == "L"))
        h = evaluate(res, models_H()[0])
        mfe = min(h)
        r = run_dp(a, m, B)
        ok = (r["conn"] == res["CONNECTED"] and r["models"][0]["mfe"] == mfe and r["models"][0]["nmin"] == h[mfe][0])
        cnt += 1
        if not ok:
            bad += 1
            print("MISMATCH", a, m, B, r["conn"], res["CONNECTED"], r["models"][0], mfe, h[mfe])
    print("instances compared: %d, mismatches: %d" % (cnt, bad))

    # ---------- (2) larger instances
    big = [
        # 3-PARTITION shaped (n = 3m, B/4 < a_i < B/2)
        ((2, 2, 3, 2, 2, 3), 2, 7), ((3, 3, 4, 3, 3, 4), 2, 10), ((3, 3, 5, 3, 4, 4), 2, 11), ((4, 4, 5, 4, 4, 5), 2, 13),
        ((4, 4, 4, 4, 4, 6), 2, 13),                       # NO, 3-PARTITION shaped
        ((5, 5, 6, 5, 5, 6), 2, 16), ((5, 5, 5, 5, 5, 7), 2, 16),   # YES / NO
        ((6, 6, 7, 5, 7, 7), 2, 19), ((5, 5, 9, 6, 6, 7), 2, 19), ((5, 6, 8, 5, 6, 8), 2, 19), ((6, 6, 6, 6, 6, 8), 2, 19),
        ((2, 2, 3, 2, 2, 3, 2, 2, 3), 3, 7), ((4, 4, 5, 4, 4, 5, 4, 4, 5), 3, 13), ((4, 4, 4, 4, 4, 4, 4, 5, 6), 3, 13),
        ((3, 3, 4, 3, 3, 4, 3, 3, 4), 3, 10), ((3, 3, 3, 3, 3, 3, 4, 4, 4), 3, 10),
        ((3, 3, 5, 3, 4, 4, 3, 4, 4), 3, 11), ((3, 3, 3, 3, 3, 3, 5, 5, 5), 3, 11), ((3, 3, 3, 3, 3, 4, 4, 4, 5), 3, 11),
        ((2, 2, 3) * 4, 4, 7), ((3, 3, 4) * 4, 4, 10),
        # 4-PARTITION shaped (n = 4m, B/5 < a_i < B/3)
        ((3, 3, 3, 4, 3, 3, 3, 4), 2, 13), ((4, 4, 4, 5, 4, 4, 4, 5), 2, 17), ((4, 5, 5, 5, 4, 5, 5, 5), 2, 19),
        ((4, 4, 4, 4, 4, 6, 6, 6), 2, 19),                 # NO, 4-PARTITION shaped
        ((4, 4, 4, 5, 5, 5, 5, 6), 2, 19), ((4, 4, 4, 4, 5, 5, 6, 6), 2, 19),
        ((3, 3, 3, 4) * 3, 3, 13), ((3, 3, 4, 4) * 3, 3, 14), ((3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4), 3, 14),
        ((3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 5), 3, 13),      # 4-PARTITION shaped, NO (5 needs 8 = 3+3+2)
        ((3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4), 3, 13),      # 4-PARTITION shaped, YES
        # near misses
        ((3, 3, 3, 3, 2), 2, 7), ((5, 5, 5, 5), 2, 10), ((5, 5, 4, 3, 3), 2, 10), ((6, 6, 4, 4), 2, 10), ((7, 7, 3, 3), 2, 10),
        ((6, 5, 5, 4), 2, 10), ((9, 1, 5, 5), 2, 10), ((9, 9, 1, 1), 2, 10), ((8, 8, 2, 1, 1), 2, 10), ((11, 9), 2, 10), ((10, 10), 2, 10),
        ((19, 1), 2, 10), ((20,), 2, 10), ((1,) * 9 + (11,), 2, 10), ((2,) * 10, 2, 10), ((2,) * 9 + (1, 1), 2, 10),
        ((3,) * 7, 3, 7), ((7,) * 3, 3, 7), ((6, 1) * 3, 3, 7), ((6, 6, 6, 1, 1, 1), 3, 7), ((6, 6, 5, 2, 1, 1), 3, 7), ((5, 5, 5, 2, 2, 2), 3, 7),
        ((5, 5, 5, 3, 3), 3, 7), ((4, 4, 4, 3, 3, 3), 3, 7), ((4, 4, 4, 4, 3, 2), 3, 7),
        ((1,) * 8, 8, 1), ((2, 1, 1, 1, 1, 1, 1), 8, 1), ((2,) * 6, 12, 1), ((2,) * 6, 6, 2), ((2,) * 6, 4, 3), ((2,) * 6, 3, 4), ((2,) * 6, 2, 6), ((2,) * 6, 1, 12),
        ((12,), 1, 12), ((12,), 12, 1), ((12,), 2, 6), ((12,), 3, 4), ((12,), 4, 3), ((12,), 6, 2),
    ]
    rng = random.Random(20261126)
    rnd = []
    for _ in range(900):
        m = rng.choice([1, 2, 2, 3, 3, 4, 5])
        B = rng.randint(1, 9)
        n = rng.randint(max(1, min(m, m * B)), min(8, m * B))
        if rng.random() < 0.5 and n >= m:
            inst = random_yes_instance(rng, m, B, n)
        else:
            inst = random_instance(rng, m, B, n)
        # cost guard for the DP: (#distinct orderings) * Lt^2 * Lc
        nord = math.factorial(len(inst)) // mu_fact(inst)
        Lt = m * B + m - 1
        if sum(inst) == m * B and nord * Lt * Lt * m * B < 1.5e7:
            rnd.append((inst, m, B))
    print("== (2) DP on larger / random instances: %d structured, %d random" % (len(big), len(rnd)))
    with Pool(4) as p:
        rows = p.map(check, big + rnd, chunksize=1)
    nf = 0
    for i, r in enumerate(rows):
        if i < len(big) or r["fails"]:
            print("%-44s m=%d B=%2d n=%2d %-3s M=%3d Til=%-9d conn=%-28d MFE(stack-only)=%4d #min=%-9d %s" % (
                str(r["a"]), r["m"], r["B"], r["n"], "YES" if r["pk"] else "NO", r["M"], r["Til"], r["conn"], r["mfe"], r["nmin"],
                "ok" if not r["fails"] else "FAIL: " + "; ".join(r["fails"])))
        nf += len(r["fails"])
    ny = sum(r["pk"] for r in rows)
    print("total instances %d (YES %d, NO %d); failures for (H0)-(H2) models: %d" % (len(rows), ny, len(rows) - ny, nf))
    print("random instances: YES %d, NO %d" % (sum(r["pk"] for r in rows[len(big):]), sum(not r["pk"] for r in rows[len(big):])))
    # ---------- (3) violating models
    print("== (3) models violating (H2): does 'MFE == sigma*M  <=>  packable' still hold? are the minima still exactly the tilings (YES instances)?")
    agg = {}
    for r in rows:
        for name, mfe, sM, nmin, decides, same in r["viol"]:
            d = agg.setdefault(name, dict(dec_ok=0, dec_bad=0, til_ok=0, til_bad=0, below=0, ex=None))
            d["dec_ok" if decides else "dec_bad"] += 1
            if same is not None:
                d["til_ok" if same else "til_bad"] += 1
            if mfe < sM:
                d["below"] += 1
                if d["ex"] is None:
                    d["ex"] = (r["a"], r["m"], r["B"], mfe, sM)
    for name, d in agg.items():
        print("%-36s decision ok %3d / wrong %3d | minima = tilings: %3d yes / %3d no | MFE < sigma*M in %3d instances; e.g. %s" % (
            name, d["dec_ok"], d["dec_bad"], d["til_ok"], d["til_bad"], d["below"], d["ex"]))
