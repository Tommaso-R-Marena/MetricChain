#!/usr/bin/env python3
"""R25, Item 2 -- Lemma A1 of STRANDS_NN_HARDNESS.md (Appendix A): 3-SAT -> 3-dimensional matching with local
garbage collection.  Own code, written from the statement of the construction (their test_eth_chain.py was not
available to this workstream).

A formula is a list of clauses; a clause is a tuple of non-zero integers (+v / -v), 1 to 3 of them; repeated
literals and complementary literals in one clause are allowed (a 'slot' is an occurrence).

Usage:
  python3 -B a1_3dm.py special                 special cases, naive cross-check of the exact-cover counter
  python3 -B a1_3dm.py exh NV MAXM [SAMPLE SEED]   every formula on NV variables with <= MAXM clauses (multisets of
                                               multisets of literals); with SAMPLE: a random sample of that many
                                               formulas with exactly MAXM clauses
  python3 -B a1_3dm.py rand SEED COUNT         random larger formulas

Checks (each reported with its number of violations):
  S   sizes |W|=|X|=|Y|=2L<=6m, |T|=3L+sum 2l(l-1)<=21m, triples distinct and in W x X x Y, every element in a triple
  E   satisfiable  <=>  a perfect matching exists                      (both directions counted separately)
  N   number of perfect matchings = sum over satisfying assignments of prod_C (true slots of C) * (l_C - 1)!
  F   (<=) the matching built by the recipe of the proof is a perfect matching, for every satisfying assignment
  B   (=>) every perfect matching (up to a cap per formula) decodes to a consistent satisfying assignment
Controls (each must produce disagreements; reported with their number):
  K1  one triple removed (first true / false / clause / garbage-with-p-tip / garbage-with-n-tip triple)
  K2  one wrong triple added (clause triple with the opposite tip)
  K3  variable gadget unlinked (false triple uses a_{v,j} instead of a_{v,j+1})
  K4  counting identity without the factor (l_C - 1)!
"""
import sys
import time
import random
import itertools
import resource
from math import factorial


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def limit_memory(gb=2.0):
    """hard cap on the address space of this process (machine rule of the brief: no process above 2 GB)"""
    lim = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (lim, lim))


MEMO_CAP = 2000000      # the exact-cover counter gives up (exception) beyond this many memoised states


def build(clauses, mutate=None):
    """the construction of Lemma A1.  Returns W, X, Y (lists of labelled elements), T (list of (w, x, y, kind)),
    slot_of {(clause index, position): (variable, j)}, occ {variable: [(clause index, position), ...]}"""
    occ = {}
    slot_of = {}
    for ci, cl in enumerate(clauses):
        for k, lit in enumerate(cl):
            v = abs(lit)
            occ.setdefault(v, []).append((ci, k))
            slot_of[(ci, k)] = (v, len(occ[v]))
    W, X, Y, T = [], [], [], []
    for v, lst in occ.items():
        for j in range(1, len(lst) + 1):
            W.append(("p", v, j))
            W.append(("n", v, j))
            X.append(("a", v, j))
            Y.append(("b", v, j))
    for ci, cl in enumerate(clauses):
        X.append(("c1", ci))
        Y.append(("c2", ci))
        for r in range(1, len(cl)):                 # l_C - 1 garbage pairs
            X.append(("g1", ci, r))
            Y.append(("g2", ci, r))
    for v, lst in occ.items():
        d = len(lst)
        for j in range(1, d + 1):
            jn = j % d + 1                          # second index mod d_v
            T.append((("n", v, j), ("a", v, j), ("b", v, j), "true"))
            if mutate == "unlinked":
                T.append((("p", v, j), ("a", v, j), ("b", v, j), "false"))
            else:
                T.append((("p", v, j), ("a", v, jn), ("b", v, j), "false"))
    for ci, cl in enumerate(clauses):
        for k, lit in enumerate(cl):
            v, j = slot_of[(ci, k)]
            tip = ("p", v, j) if lit > 0 else ("n", v, j)
            T.append((tip, ("c1", ci), ("c2", ci), "clause"))
    for ci, cl in enumerate(clauses):
        for r in range(1, len(cl)):
            for k, lit in enumerate(cl):
                v, j = slot_of[(ci, k)]
                T.append((("p", v, j), ("g1", ci, r), ("g2", ci, r), "garbage_p"))
                T.append((("n", v, j), ("g1", ci, r), ("g2", ci, r), "garbage_n"))
    if mutate and mutate.startswith("drop:"):
        kind = mutate[5:]
        for i, t in enumerate(T):
            if t[3] == kind:
                del T[i]
                break
    if mutate == "add_wrong_clause" and clauses and clauses[0]:
        v, j = slot_of[(0, 0)]
        tip = ("n", v, j) if clauses[0][0] > 0 else ("p", v, j)
        T.append((tip, ("c1", 0), ("c2", 0), "wrong"))
    return W, X, Y, T, slot_of, occ


def index_instance(W, X, Y, T):
    """element order for the exact-cover search: X and Y interleaved first, W last"""
    order = []
    for i in range(max(len(X), len(Y))):
        if i < len(Y):
            order.append(Y[i])
        if i < len(X):
            order.append(X[i])
    order.extend(W)
    idx = {e: i for i, e in enumerate(order)}
    masks = [(1 << idx[w]) | (1 << idx[x]) | (1 << idx[y]) for (w, x, y, _) in T]
    by_el = [[] for _ in order]
    for ti, (w, x, y, _) in enumerate(T):
        for e in (w, x, y):
            by_el[idx[e]].append(ti)
    return order, idx, masks, by_el


def make_counter(W, X, Y, T):
    """exact covers of W u X u Y by triples: returns (rec, masks, by_el, full) where rec(cov) is the number of
    ways to complete the covered set cov to an exact cover (memoised on cov; lowest uncovered element first)"""
    order, idx, masks, by_el = index_instance(W, X, Y, T)
    nel = len(order)
    full = (1 << nel) - 1
    memo = {}

    def rec(cov):
        if cov == full:
            return 1
        r = memo.get(cov)
        if r is not None:
            return r
        e = ((~cov) & (cov + 1)).bit_length() - 1      # lowest uncovered element
        tot = 0
        for ti in by_el[e]:
            tm = masks[ti]
            if not (tm & cov):
                tot += rec(cov | tm)
        if len(memo) >= MEMO_CAP:
            raise RuntimeError("exact-cover counter: more than MEMO_CAP states; instance too large for this method")
        memo[cov] = tot
        return tot

    return rec, masks, by_el, full


def count_pm(W, X, Y, T):
    """number of perfect matchings"""
    return make_counter(W, X, Y, T)[0](0)


def enum_pm(W, X, Y, T, cap):
    """explicit perfect matchings (lists of triple indices), at most cap of them; branches without any completion
    are pruned with the counter (otherwise the search is exponential on formulas with few models)"""
    rec, masks, by_el, full = make_counter(W, X, Y, T)
    out = []
    cur = []

    def walk(cov):
        if len(out) >= cap:
            return
        if cov == full:
            out.append(list(cur))
            return
        e = ((~cov) & (cov + 1)).bit_length() - 1
        for ti in by_el[e]:
            tm = masks[ti]
            if not (tm & cov) and rec(cov | tm) > 0:
                cur.append(ti)
                walk(cov | tm)
                cur.pop()

    if rec(0) > 0:
        walk(0)
    return out


def count_pm_naive(W, X, Y, T):
    """all subsets of q triples, tested for disjointness (tiny instances only); needs |W|=|X|=|Y|=q"""
    q = len(W)
    if not (len(X) == q and len(Y) == q):
        return 0
    cnt = 0
    for sub in itertools.combinations(T, q):
        if len({t[0] for t in sub}) == q and len({t[1] for t in sub}) == q and len({t[2] for t in sub}) == q:
            cnt += 1
    return cnt


def sat_data(clauses, with_factorial=True):
    """(number of satisfying assignments over the occurring variables, predicted number of perfect matchings,
    list of satisfying assignments as dicts)"""
    vs = sorted({abs(l) for cl in clauses for l in cl})
    nsat = 0
    pred = 0
    sats = []
    for bits in itertools.product((False, True), repeat=len(vs)):
        al = dict(zip(vs, bits))
        prod = 1
        for cl in clauses:
            t = sum(1 for l in cl if al[abs(l)] == (l > 0))
            if t == 0:
                prod = 0
                break
            prod *= t * (factorial(len(cl) - 1) if with_factorial else 1)
        if prod:
            nsat += 1
            pred += prod
            sats.append(al)
    return nsat, pred, sats


def check_sizes(clauses, W, X, Y, T):
    m = len(clauses)
    L = sum(len(cl) for cl in clauses)
    ok = (len(W) == 2 * L and len(X) == 2 * L and len(Y) == 2 * L and 2 * L <= 6 * m)
    ok = ok and len(T) == 3 * L + sum(2 * len(cl) * (len(cl) - 1) for cl in clauses) and len(T) <= 21 * m
    trip = [(w, x, y) for (w, x, y, _) in T]
    ok = ok and len(set(trip)) == len(trip)
    sw, sx, sy = set(W), set(X), set(Y)
    ok = ok and len(sw) == len(W) and len(sx) == len(X) and len(sy) == len(Y)
    ok = ok and all(w in sw and x in sx and y in sy for (w, x, y) in trip)
    used = set()
    for (w, x, y) in trip:
        used.update((w, x, y))
    ok = ok and used == (sw | sx | sy)
    return ok


def forward_matching(clauses, al, slot_of, occ):
    """the matching of the proof (direction 'satisfying assignment => perfect matching')"""
    Mt = []
    for v, lst in occ.items():
        d = len(lst)
        for j in range(1, d + 1):
            if al[v]:
                Mt.append((("n", v, j), ("a", v, j), ("b", v, j)))
            else:
                Mt.append((("p", v, j), ("a", v, j % d + 1), ("b", v, j)))
    for ci, cl in enumerate(clauses):
        true_slots = [k for k, l in enumerate(cl) if al[abs(l)] == (l > 0)]
        k0 = true_slots[0]
        v, j = slot_of[(ci, k0)]
        Mt.append(((("p" if cl[k0] > 0 else "n"), v, j), ("c1", ci), ("c2", ci)))
        r = 0
        for k, l in enumerate(cl):
            if k == k0:
                continue
            r += 1
            v, j = slot_of[(ci, k)]
            left = ("p", v, j) if al[v] else ("n", v, j)        # the tip left free by the variable triples
            Mt.append((left, ("g1", ci, r), ("g2", ci, r)))
    return Mt


def is_perfect(Mt, W, X, Y, Tset):
    if any(t not in Tset for t in Mt):
        return False
    ws = [t[0] for t in Mt]
    xs = [t[1] for t in Mt]
    ys = [t[2] for t in Mt]
    return sorted(ws) == sorted(W) and sorted(xs) == sorted(X) and sorted(ys) == sorted(Y)


def decode(clauses, T, pm, occ, slot_of):
    """direction 'perfect matching => satisfying assignment': returns True iff the matching decodes consistently
    and the decoded assignment satisfies the formula through the clause triples it contains"""
    chosen = {(T[ti][0], T[ti][1], T[ti][2]) for ti in pm}
    al = {}
    for v, lst in occ.items():
        d = len(lst)
        tr = [(("n", v, j), ("a", v, j), ("b", v, j)) in chosen for j in range(1, d + 1)]
        fa = [(("p", v, j), ("a", v, j % d + 1), ("b", v, j)) in chosen for j in range(1, d + 1)]
        if all(tr) and not any(fa):
            al[v] = True
        elif all(fa) and not any(tr):
            al[v] = False
        else:
            return False
    for ci, cl in enumerate(clauses):
        hit = [k for k, l in enumerate(cl)
               if ((("p" if l > 0 else "n"),) + slot_of[(ci, k)], ("c1", ci), ("c2", ci)) in chosen]
        if len(hit) != 1:
            return False
        l = cl[hit[0]]
        if al[abs(l)] != (l > 0):
            return False
    return all(any(al[abs(l)] == (l > 0) for l in cl) for cl in clauses)


ALL_CONTROLS = ["drop:true", "drop:false", "drop:clause", "drop:garbage_p", "drop:garbage_n", "add_wrong_clause",
                "unlinked"]
# 'unlinked' makes every slot an independent choice: 2^L covered-sets.  It is used only on the small exhaustive
# families (L <= 9); on larger formulas it exhausts memory (this happened once, see NOTES.md, own error no. 2).
CONTROLS_LARGE = [c for c in ALL_CONTROLS if c != "unlinked"]


def run_family(formulas, label, do_controls=True, pm_cap=50, controls=None):
    t0 = time.time()
    CONTROLS = controls if controls is not None else ALL_CONTROLS
    st = dict(formulas=0, sat=0, unsat=0, viol_S=0, viol_E_sat_no_pm=0, viol_E_unsat_pm=0, viol_N=0,
              viol_F=0, checked_F=0, viol_B=0, checked_B=0, ctrl_K4=0, max_T=0, max_q=0, pm_total=0)
    ctrl = {c: [0, 0, None] for c in CONTROLS}     # [sat-but-no-pm, unsat-but-pm, first example]
    feat = dict(unit_clause=0, two_clause=0, repeated_literal=0, complementary_pair=0, var_once=0,
                var_only_positive=0, var_only_negative=0, duplicate_clause=0)
    for clauses in formulas:
        st["formulas"] += 1
        W, X, Y, T, slot_of, occ = build(clauses)
        st["max_T"] = max(st["max_T"], len(T))
        st["max_q"] = max(st["max_q"], len(W))
        # features of the formula (for the coverage statement)
        if any(len(cl) == 1 for cl in clauses):
            feat["unit_clause"] += 1
        if any(len(cl) == 2 for cl in clauses):
            feat["two_clause"] += 1
        if any(len(set(cl)) < len(cl) for cl in clauses):
            feat["repeated_literal"] += 1
        if any(any(-l in cl for l in cl) for cl in clauses):
            feat["complementary_pair"] += 1
        if any(len(lst) == 1 for lst in occ.values()):
            feat["var_once"] += 1
        lits = {l for cl in clauses for l in cl}
        if any(-v not in lits for v in occ):
            feat["var_only_positive"] += 1
        if any(v not in lits for v in occ):
            feat["var_only_negative"] += 1
        if len(set(tuple(sorted(cl)) for cl in clauses)) < len(clauses):
            feat["duplicate_clause"] += 1
        if not check_sizes(clauses, W, X, Y, T):
            st["viol_S"] += 1
        nsat, pred, sats = sat_data(clauses)
        npm = count_pm(W, X, Y, T)
        st["pm_total"] += npm
        if nsat:
            st["sat"] += 1
            if npm == 0:
                st["viol_E_sat_no_pm"] += 1
        else:
            st["unsat"] += 1
            if npm > 0:
                st["viol_E_unsat_pm"] += 1
        if npm != pred:
            st["viol_N"] += 1
        if sat_data(clauses, with_factorial=False)[1] != npm:
            st["ctrl_K4"] += 1
        Tset = {(w, x, y) for (w, x, y, _) in T}
        for al in sats:
            st["checked_F"] += 1
            if not is_perfect(forward_matching(clauses, al, slot_of, occ), W, X, Y, Tset):
                st["viol_F"] += 1
        if npm:
            for pm in enum_pm(W, X, Y, T, pm_cap):
                st["checked_B"] += 1
                if not decode(clauses, T, pm, occ, slot_of):
                    st["viol_B"] += 1
        if do_controls:
            for c in CONTROLS:
                W2, X2, Y2, T2, _, _ = build(clauses, mutate=c)
                has = count_pm(W2, X2, Y2, T2) > 0
                if nsat and not has:
                    ctrl[c][0] += 1
                    if ctrl[c][2] is None:
                        ctrl[c][2] = clauses
                if (not nsat) and has:
                    ctrl[c][1] += 1
                    if ctrl[c][2] is None:
                        ctrl[c][2] = clauses
    print(f"[{label}] formulas {st['formulas']} (satisfiable {st['sat']}, unsatisfiable {st['unsat']}); "
          f"largest instance: q = |W| = {st['max_q']}, |T| = {st['max_T']}; perfect matchings counted {st['pm_total']}")
    print(f"[{label}] coverage: " + ", ".join(f"{k} {v}" for k, v in feat.items()))
    print(f"[{label}] violations: S sizes {st['viol_S']}; E satisfiable-but-no-matching {st['viol_E_sat_no_pm']}, "
          f"unsatisfiable-but-matching {st['viol_E_unsat_pm']}; N counting identity {st['viol_N']}; "
          f"F recipe of the proof {st['viol_F']} of {st['checked_F']}; B decoding {st['viol_B']} of {st['checked_B']}")
    print(f"[{label}] control K4 (identity without (l-1)!): fails on {st['ctrl_K4']} formulas")
    if do_controls:
        for c in CONTROLS:
            print(f"[{label}] control {c}: satisfiable-but-no-matching {ctrl[c][0]}, "
                  f"unsatisfiable-but-matching {ctrl[c][1]}; first disagreement {ctrl[c][2]}")
    print(f"[{label}] time {time.time() - t0:.1f} s", flush=True)
    return st


def all_clauses(nv):
    lits = [s * v for v in range(1, nv + 1) for s in (1, -1)]
    out = []
    for k in (1, 2, 3):
        out.extend(itertools.combinations_with_replacement(lits, k))
    return out


def mode_exh(nv, maxm, sample=None, seed=0):
    cls = all_clauses(nv)
    if sample is None:
        def gen():
            for mm in range(1, maxm + 1):
                for f in itertools.combinations_with_replacement(cls, mm):
                    yield list(f)
        run_family(gen(), f"exh nv={nv} m<={maxm}")
    else:
        rng = random.Random(seed)
        fs = [[rng.choice(cls) for _ in range(maxm)] for _ in range(sample)]
        run_family(fs, f"sample nv={nv} m={maxm} n={sample} seed={seed}")


def mode_rand(seed, count):
    rng = random.Random(seed)
    fs = []
    for _ in range(count):
        nv = rng.randint(2, 7)
        m = rng.randint(1, 3 * nv)
        f = []
        for _ in range(m):
            k = rng.choice((1, 2, 2, 3, 3, 3, 3))
            f.append(tuple(rng.choice((1, -1)) * rng.randint(1, nv) for _ in range(k)))
        fs.append(f)
    run_family(fs, f"random seed={seed} n={count} (2..7 variables, 1..3nv clauses)", controls=CONTROLS_LARGE)
    # pure 3-CNF near the threshold, distinct variables in a clause
    fs = []
    for _ in range(count):
        nv = rng.randint(3, 7)
        m = rng.randint(3 * nv, 6 * nv)
        f = []
        for _ in range(m):
            vs = rng.sample(range(1, nv + 1), 3)
            f.append(tuple(rng.choice((1, -1)) * v for v in vs))
        fs.append(f)
    run_family(fs, f"random 3-CNF seed={seed} n={count} (3..7 variables, 3nv..6nv clauses)", do_controls=False)


def mode_special():
    cases = {
        "unit": [(1,)], "unit negative": [(-1,)], "x and not x (unsat)": [(1,), (-1,)],
        "repeated literal": [(1, 1, 2)], "repeated literal thrice": [(1, 1, 1)],
        "repeated literal thrice + not x (unsat)": [(1, 1, 1), (-1,)],
        "tautological clause": [(1, -1)], "tautological clause + units (sat)": [(1, -1, 2), (-2,)],
        "variable once": [(1, 2, 3)], "only positive": [(1, 2), (1, 3), (2, 3)],
        "only negative": [(-1, -2), (-1, -3)], "duplicate clauses": [(1, -2), (1, -2)],
        "two-literal unsat": [(1, 2), (1, -2), (-1, 2), (-1, -2)],
        "all eight 3-clauses (unsat)": [tuple(s * v for s, v in zip(sg, (1, 2, 3)))
                                        for sg in itertools.product((1, -1), repeat=3)],
        "seven 3-clauses (one model)": [tuple(s * v for s, v in zip(sg, (1, 2, 3)))
                                        for sg in itertools.product((1, -1), repeat=3)][1:],
    }
    viol = 0
    for name, f in cases.items():
        W, X, Y, T, slot_of, occ = build(f)
        nsat, pred, sats = sat_data(f)
        npm = count_pm(W, X, Y, T)
        okS = check_sizes(f, W, X, Y, T)
        bad = (npm != pred) or ((nsat > 0) != (npm > 0)) or not okS
        viol += bad
        print(f"  {name}: {f}: q={len(W)}, |T|={len(T)}, models {nsat}, matchings {npm}, predicted {pred}, "
              f"sizes ok {okS}{'   <-- VIOLATION' if bad else ''}")
    print(f"[special] violations {viol} of {len(cases)}")
    # naive cross-check of the counter on tiny instances (also on mutated instances, where the answer differs)
    tiny = [[(1,)], [(-1,)], [(1,), (-1,)], [(1, 2)], [(1, -1)], [(1, 1)], [(1, 2), (-1,)], [(1, 2), (-2,)],
            [(1, 2, 3)], [(1, 1, 2)], [(1, -1, 1)], [(1,), (1,)], [(1,), (2,), (-1,)], [(1, 2), (1,)]]
    nchk = vio = 0
    for f in tiny:
        for mut in [None] + ALL_CONTROLS:
            W, X, Y, T, _, _ = build(f, mutate=mut)
            if len(T) > 24:
                continue
            nchk += 1
            if count_pm(W, X, Y, T) != count_pm_naive(W, X, Y, T):
                vio += 1
    print(f"[special] exact-cover counter vs naive subset enumeration: {vio} disagreements on {nchk} instances")
    # control for this cross-check: a naive count that ignores the W coordinate must disagree somewhere
    dis = 0
    for f in tiny:
        W, X, Y, T, _, _ = build(f)
        if len(T) > 24:
            continue
        q = len(W)
        naive_xy = sum(1 for sub in itertools.combinations(T, q)
                       if len({t[1] for t in sub}) == q and len({t[2] for t in sub}) == q)
        if naive_xy != count_pm(W, X, Y, T):
            dis += 1
    print(f"[special] control (naive count ignoring the W coordinate differs from the counter): {dis} instances")
    # the edge case of an empty clause
    f = [(1, 2), ()]
    W, X, Y, T, _, _ = build(f)
    print(f"[special] empty clause, formula {f}: |W|={len(W)}, |X|={len(X)}, |Y|={len(Y)}, |T|={len(T)}; "
          f"elements in no triple: {sorted(set(X + Y + W) - {e for t in T for e in t[:3]})}; "
          f"exact covers {count_pm(W, X, Y, T)}")


if __name__ == "__main__":
    limit_memory(2.0)
    mode = sys.argv[1]
    if mode == "special":
        mode_special()
    elif mode == "exh":
        if len(sys.argv) > 4:
            mode_exh(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        else:
            mode_exh(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == "rand":
        mode_rand(int(sys.argv[2]), int(sys.argv[3]))
    else:
        raise SystemExit("unknown mode")
    print(f"peak memory {peak_mb():.1f} MB")
