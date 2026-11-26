#!/usr/bin/env python3
"""R24, item 3: the threshold rule and the law of a count, replicated; the table of addendum item 88 against the log.

 S1  the range of E psi over the box l <= w <= u, three ways: (i) the referee's rule -- sort psi, the best of the N + 1
     "threshold vertices" (u on the top j states, l on the rest); (ii) brute force over all 2^N vertices; (iii) the
     coordinator's upper_end / lower_end (root of H).  Boxes with ties, with integer observables, with states of zero width.
     Control: the rule with l and u exchanged.
 S2  the law of the number of sites off an anchor under a model with tables on windows: (i) the referee's own transfer
     matrix with a counter (polynomial messages, linear domain) on the factor list; (ii) enumeration; (iii) the
     coordinator's count_law on a WindowModel filled with the same random tables (one-site, pair and multi-site tables).
     Control: the law at 1.02 beta against enumeration at beta.
 S3  every number of the table of item 88 (typed from the addendum) against sandwich_class_real.log (parsed); control: one
     typed number changed in the last digit must be reported.
Run: python3 -B r24_item3.py > r24_item3.log
"""
import os, sys, re, math, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(SCI, "ensemble_checks")); sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import r24_common as C


def my_range(psi, u, l):
    """(lower, upper) end of sum(w psi)/sum(w) over l <= w <= u: the best threshold vertex in the sorted order"""
    o = np.argsort(psi, kind="stable"); p = psi[o]; uu = u[o]; ll = l[o]; N = len(p)
    # upper: u on the top j states (largest psi), l on the others, j = 0..N
    cu_w = np.concatenate([[0.0], np.cumsum(uu[::-1])]); cu_p = np.concatenate([[0.0], np.cumsum((uu * p)[::-1])])       # top j at u
    cl_w = np.concatenate([[0.0], np.cumsum(ll)]); cl_p = np.concatenate([[0.0], np.cumsum(ll * p)])                     # bottom N - j at l
    j = np.arange(N + 1); up = ((cu_p[j] + cl_p[N - j]) / (cu_w[j] + cl_w[N - j])).max()
    # lower: l on the top j states, u on the others
    dl_w = np.concatenate([[0.0], np.cumsum(ll[::-1])]); dl_p = np.concatenate([[0.0], np.cumsum((ll * p)[::-1])])
    du_w = np.concatenate([[0.0], np.cumsum(uu)]); du_p = np.concatenate([[0.0], np.cumsum(uu * p)])
    lo = ((dl_p[j] + du_p[N - j]) / (dl_w[j] + du_w[N - j])).min()
    return float(lo), float(up)


def brute(psi, u, l):
    N = len(psi); best = (1e300, -1e300)
    for bits in range(2 ** N):
        w = np.where((bits >> np.arange(N)) & 1, u, l); v = float((w * psi).sum() / w.sum()); best = (min(best[0], v), max(best[1], v))
    return best


def count_poly(fac, k, anchor, scale):
    """Z_c = sum over the states with exactly c sites off the anchor of exp(scale * sum of tables), c = 0..n: own elimination with
    polynomial messages in the linear domain (last axis = power of the counting variable)."""
    n = len(k); cur = []
    for U, tab in fac:
        a = np.zeros(tab.shape + (n + 1,)); a[..., 0] = np.exp(scale * tab); cur.append((tuple(U), a))

    def mul(sa, A, sb, B):
        sc = tuple(sorted(set(sa) | set(sb)))
        def ex(s, X):
            sh = [k[u] if u in s else 1 for u in sc] + [n + 1]; return X.reshape(sh)
        A2, B2 = ex(sa, A), ex(sb, B); out = np.zeros([k[u] for u in sc] + [n + 1])
        for d1 in range(n + 1):
            if not A2[..., d1].any(): continue
            for d2 in range(n + 1 - d1):
                out[..., d1 + d2] += A2[..., d1] * B2[..., d2]
        return sc, out
    tot = np.zeros(n + 1); tot[0] = 1.0
    for i in range(n):
        mine = [(U, t) for U, t in cur if i in U]; cur = [(U, t) for U, t in cur if i not in U]
        if not mine: mine = [((i,), np.concatenate([np.ones((k[i], 1)), np.zeros((k[i], n))], axis=1))]
        sc, A = mine[0]
        for U, t in mine[1:]: sc, A = mul(sc, A, U, t)
        ax = sc.index(i); A = np.moveaxis(A, ax, 0); on = A[anchor[i]]; off = A.sum(axis=0) - on
        red = on.copy(); red[..., 1:] += off[..., :-1]                           # a site off the anchor raises the count by one
        rest = tuple(u for u in sc if u != i)
        if rest: cur.append((rest, red))
        else: tot = np.convolve(tot, red)[:n + 1]
    assert not cur
    return tot


def main():
    t0 = time.time(); rng = np.random.default_rng(2403)
    import sandwich_class as SC
    # ------------------------------------------------------------------ S1
    dev_b = 0.0; dev_t = 0.0; ctrl = 0; nbox = 0
    for N in (2, 3, 5, 7, 9, 11, 12):
        for rep in range(30 if N <= 9 else 10):
            l = rng.uniform(0.02, 1.0, N); u = l * np.exp(rng.uniform(0.0, 3.0, N))
            if rep % 5 == 0: zi = rng.integers(N); u[zi] = l[zi]                 # a state of zero width
            psi = rng.normal(size=N) if rep % 3 == 0 else (rng.integers(0, 3, N).astype(float) if rep % 3 == 1 else np.round(rng.normal(size=N), 1))
            if len(np.unique(psi)) == 1: psi[0] += 1.0
            lo, up = my_range(psi, u, l); b = brute(psi, u, l); th, _ = SC.upper_end(psi, u, l); tl, _ = SC.lower_end(psi, u, l); nbox += 1
            dev_b = max(dev_b, abs(lo - b[0]), abs(up - b[1])); dev_t = max(dev_t, abs(tl - b[0]), abs(th - b[1]))
            lo2, up2 = my_range(psi, l, u); ctrl += int(abs(up2 - b[1]) > 1e-9 or abs(lo2 - b[0]) > 1e-9)
    print(f"S1  {nbox} boxes of 2 to 12 states (ties, integer observables, states of zero width): my rule against brute force over all vertices: largest deviation {dev_b:.1e}; "
          f"their upper_end / lower_end against the same brute force: {dev_t:.1e} (both must be < 1e-10); control, floor and ceiling exchanged: differs from brute force in {ctrl} of {nbox} boxes (must be nearly all)")
    assert dev_b < 1e-10 and dev_t < 1e-10 and ctrl > 0.8 * nbox
    # ------------------------------------------------------------------ S2
    import nested_sampler as NS
    dev_mine = 0.0; dev_theirs = 0.0; ctrl2 = 0.0; nmod = 0
    for rep in range(40):
        n = int(rng.integers(4, 8)); k = [int(rng.integers(2, 5)) for _ in range(n)]; w = int(rng.integers(1, 4)); beta = float(rng.uniform(0.5, 2.0)); anchor = [int(rng.integers(kk)) for kk in k]
        mdl = NS.WindowModel(k, w); mdl.const = float(rng.normal())
        for i in range(n): mdl.one[i] = rng.normal(size=k[i])
        for i in range(n):
            for j in range(i + 1, min(i + w, n - 1) + 1):
                if rng.random() < 0.8: mdl.add_pair(i, j, rng.normal(size=(k[i], k[j])))
        if w >= 2:
            for i in range(n - 2):
                U = tuple(sorted(rng.choice(np.arange(i, min(i + w, n - 1) + 1), size=min(3, min(i + w, n - 1) - i + 1), replace=False)))
                if len(U) == 3 and rng.random() < 0.7: mdl.add_multi(U, rng.normal(size=tuple(k[u] for u in U)))
        c0, fac = C.factors_of(mdl); E = C.energy_all(c0, fac, k).ravel()
        st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n); cnt = (st != np.array(anchor)[None]).sum(axis=1)
        ref = np.array([np.exp(-beta * E[cnt == c]).sum() for c in range(n + 1)])
        mine = count_poly(fac, k, anchor, -beta) * math.exp(-beta * c0); theirs = np.exp(SC.count_law(mdl, anchor, beta))
        dev_mine = max(dev_mine, float(np.abs(mine / ref - 1).max())); dev_theirs = max(dev_theirs, float(np.abs(theirs / ref - 1).max())); nmod += 1
        ctrl2 = max(ctrl2, float(np.abs(count_poly(fac, k, anchor, -1.02 * beta) * math.exp(-1.02 * beta * c0) / ref - 1).max()))
    print(f"S2  the law of the number of sites off an anchor, {nmod} random models with tables on windows (4 to 7 sites, 2 to 4 states, band 1 to 3, pair and three-site tables): my counter pass against enumeration: "
          f"largest relative deviation {dev_mine:.1e}; their count_law against the same enumeration: {dev_theirs:.1e} (both must be < 1e-9); control, my pass at 1.02 beta: {ctrl2:.2f} (must be far above)")
    assert dev_mine < 1e-9 and dev_theirs < 1e-9 and ctrl2 > 1e-3
    # ------------------------------------------------------------------ S3: the table of item 88 against the log
    txt = open(os.path.join(SCI, "ensemble_checks", "sandwich_class_real.log")).read()
    rows = {}
    for mm in re.finditer(r"  (V\d+/P2 order \d form [SBT]): ln Z width ([0-9.e+-]+); sum of the single-site intervals \[([0-9.]+), ([0-9.]+)\] \(width [0-9.e+-]+\); \*\*exact range over the sandwich \[([0-9.]+), ([0-9.]+)\] \(width [0-9.e+-]+\)\*\*: narrower by a factor \*\*([0-9.]+)\*\*", txt):
        rows[mm.group(1)] = [float(mm.group(q)) for q in range(2, 8)]
    mm = re.search(r"R3  Lys5.*?ln Z width ([0-9.e+-]+);.*?exact mean number of sites off the anchor ([0-9.]+); sum of the single-site intervals \[([0-9.]+), ([0-9.]+)\].*?exact range over the sandwich \[([0-9.]+), ([0-9.]+)\].*?narrower by a factor \*\*([0-9.]+)\*\*", txt)
    rows["Lys5"] = [float(mm.group(1))] + [float(mm.group(q)) for q in range(3, 8)]; lys_exact = float(mm.group(2))
    v8 = float(re.search(r"R1  V8/P2: \d+ states enumerated; exact mean number of sites off the anchor ([0-9.]+)", txt).group(1))
    # typed from the addendum, item 88, and from SCI-RES-0032 section 3 (width of ln Z): (key, width, published interval, exact range, factor)
    typed = [("V20/P2 order 4 form S", 1.74, (0.64, 11.62), (2.56, 5.04), 4.4), ("V20/P2 order 4 form B", 0.306, (2.64, 4.73), (3.305, 3.851), 3.8), ("V20/P2 order 4 form T", 0.0546, (3.355, 3.751), (3.485, 3.613), 3.1),
             ("V20/P2 order 5 form S", 0.0605, (3.355, 3.738), (3.499, 3.586), 4.4), ("V20/P2 order 5 form B", 0.0162, (3.488, 3.597), (3.528, 3.556), 3.9), ("V20/P2 order 5 form T", 0.0090, (3.512, 3.573), (3.534, 3.550), 3.7),
             ("V8/P2 order 4 form S", 0.425, (0.853, 2.007), (1.154, 1.564), 2.8), ("V8/P2 order 4 form B", 0.0717, (1.227, 1.458), (1.283, 1.396), 2.0), ("Lys5", 0.0477, (0.878, 0.984), (0.907, 0.954), 2.3)]

    def agree(typed_v, log_v):
        s = f"{typed_v}"; dec = len(s.split(".")[1]) if "." in s else 0
        return abs(typed_v - log_v) <= 0.5 * 10 ** (-dec) + 1e-12

    def compare(tp):
        bad = []; cnt = 0
        for key, wd, pub, ex, fac in tp:
            r = rows[key]
            for nm, tv, lv in (("width", wd, r[0]), ("published lower", pub[0], r[1]), ("published upper", pub[1], r[2]), ("exact lower", ex[0], r[3]), ("exact upper", ex[1], r[4]), ("factor", fac, r[5])):
                cnt += 1
                if nm == "width":
                    ok = abs(tv - lv) <= 0.006 * abs(lv) + 1e-12                 # the log prints three significant digits
                else: ok = agree(tv, lv)
                if not ok: bad.append(f"{key}: {nm} typed {tv} log {lv}")
        return cnt, bad
    cnt, bad = compare(typed)
    wrong = [list(t) for t in typed]; wrong[2][3] = (3.485, 3.614); cnt2, bad2 = compare([tuple(t) for t in wrong])
    print(f"S3  the table of item 88 and the widths of SCI-RES-0032 section 3 against sandwich_class_real.log: {cnt} numbers compared, {len(bad)} disagree at the printed precision {bad if bad else ''}; "
          f"exact values 1.3341 and 0.9233 against the log's {v8:.5f} and {lys_exact:.5f}: {agree(1.3341, v8) and agree(0.9233, lys_exact)}; control, one typed number changed in its last digit: {len(bad2)} reported (must be 1)")
    omitted = [key for key in rows if key not in [t[0] for t in typed]]
    print(f"    rows of the log that are NOT in the table: " + "; ".join(f"{key}: ln Z width {rows[key][0]:g}, published [{rows[key][1]:.3f}, {rows[key][2]:.3f}], exact range [{rows[key][3]:.3f}, {rows[key][4]:.3f}], factor {rows[key][5]:.2f}" for key in omitted))
    print(f"    factors in the table: {sorted(t[4] for t in typed)}; with the omitted rows: {sorted(rows[key][5] for key in rows)}")
    assert not bad and len(bad2) == 1
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
