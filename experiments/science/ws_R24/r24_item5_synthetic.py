#!/usr/bin/env python3
"""R24, item 5 (i), on synthetic objects (no code of the division):
 T1  the criterion: over all couplings of given laws of y_g >= 0, min E prod(1 + y_g) = 1 + sum E y_g  IFF  sum_g P(y_g > 0) <= 1
     (exact linear programme over the joint law; both directions; the violation planted is large against the solver);
     and max = the comonotone coupling (checks r24_item5_enum.comonotone_mean_of_product).
 T2  the same for the floor functional prod(1 - zeta_g), zeta_g in [0, 1): max over couplings = comonotone; min = 1 - sum E zeta
     iff the events can be made disjoint.
 T3  soundness, on random small sandwiches with random items (enumeration): every upper end below is >= ln Z(E) for the
     true E and for the two extreme energies E = m_- + s_- and E = m_+ - s_+ :
        (UP) v(C'), v(C_2), v(C'') in closed form ln(Z_- - C Z_+);  Bonferroni-floor;  comonotone-floor;
     the order C' <= C_2 <= C'';  v(C'') >= ln Z(m_- + s_-) (the rest is non-negative);
     control: the first-order floor value ln Z_- + ln(1 - S1) is NOT an upper bound (must fail somewhere).
Run: python3 -B r24_item5_synthetic.py > r24_item5_synthetic.log
"""
import os, sys, math, itertools, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r24_common as C
from r24_item5_enum import esym2, comonotone_mean_of_product


def coupling_lp(vals, probs, fun, sense):
    """min (sense=+1) or max (sense=-1) of E fun over all couplings of the laws (vals[g], probs[g])"""
    G = len(vals); shape = [len(v) for v in vals]; cells = list(itertools.product(*[range(s) for s in shape]))
    cost = np.array([fun([vals[g][c[g]] for g in range(G)]) for c in cells])
    Aeq = []; beq = []
    for g in range(G):
        for a in range(shape[g]):
            Aeq.append([1.0 if c[g] == a else 0.0 for c in cells]); beq.append(probs[g][a])
    r = linprog(sense * cost, A_eq=np.array(Aeq), b_eq=beq, bounds=[(0, None)] * len(cells), method="highs")
    assert r.status == 0, r.message
    return sense * r.fun


def como_from_laws(vals, probs, fun):
    """the comonotone value through the referee's function, by expanding each law on a common fine weight vector"""
    # a common refinement: sample space = union of all breakpoints
    G = len(vals); cums = [np.cumsum(np.asarray(p)[np.argsort(v)]) for v, p in zip(vals, probs)]
    br = np.unique(np.concatenate(cums + [np.array([1.0])])); br = br[br > 1e-15]; lo_ = np.concatenate([[0.0], br[:-1]]); mid = 0.5 * (lo_ + br)
    V = np.stack([np.sort(vals[g])[np.minimum(np.searchsorted(cums[g], mid), len(vals[g]) - 1)] for g in range(G)]); wt = br - lo_
    direct = float((wt * fun(V)).sum())
    # through the referee's function, fed with a sample space on which the variables are NOT arranged: the product space with the independent coupling
    cells = list(itertools.product(*[range(len(v)) for v in vals])); wprod = np.array([math.prod(probs[g][c[g]] for g in range(G)) for c in cells])
    Vp = np.array([[vals[g][c[g]] for c in cells] for g in range(G)]); keep = wprod > 0
    viafn = comonotone_mean_of_product(Vp[:, keep], wprod[keep] / wprod[keep].sum(), fun)
    return direct, viafn


def main():
    t0 = time.time(); rng = np.random.default_rng(2405)
    # ------------------------------------------------------------------ T1, T2
    prod1 = lambda ys: float(np.prod([1.0 + y for y in ys])); prodz = lambda zs: float(np.prod([1.0 - z for z in zs]))
    eq_ok = 0; n_le = 0; gap_gt = []; n_gt = 0; como_dev = 0.0; eqz = 0; gapz = []; comoz = 0.0
    for rep in range(60):
        G = 3 if rep % 2 else 4; target = 0.85 if rep % 4 < 2 else 1.6                 # sum of P(y > 0): clearly below or clearly above one
        p_pos = rng.dirichlet(np.ones(G)) * target; p_pos = np.minimum(p_pos, 0.9)
        vals = []; probs = []
        for g in range(G):
            npos = int(rng.integers(1, 3)); v = np.concatenate([[0.0], rng.uniform(0.2, 3.0, npos)]); q = rng.dirichlet(np.ones(npos)) * p_pos[g]
            vals.append(v); probs.append(np.concatenate([[1.0 - q.sum()], q]))
        sP = float(sum(1.0 - p[0] for p in probs)); lin = 1.0 + sum(float((p * v).sum()) for v, p in zip(vals, probs))
        mn = coupling_lp(vals, probs, prod1, +1); mx = coupling_lp(vals, probs, prod1, -1)
        d1, d2 = como_from_laws(vals, probs, lambda V: np.prod(1.0 + V, axis=0)); como_dev = max(como_dev, abs(mx - d1), abs(mx - d2))
        if sP <= 1: n_le += 1; eq_ok += int(abs(mn - lin) < 1e-9)
        else: n_gt += 1; gap_gt.append(mn - lin)
        # floor functional with zeta = 1 - e^{-v}
        zv = [1.0 - np.exp(-v) for v in vals]; linz = 1.0 - sum(float((p * z).sum()) for z, p in zip(zv, probs))
        mnz = coupling_lp(zv, probs, prodz, +1); mxz = coupling_lp(zv, probs, prodz, -1); d1, d2 = como_from_laws(zv, probs, lambda V: np.prod(1.0 - V, axis=0)); comoz = max(comoz, abs(mxz - d1), abs(mxz - d2))
        if sP <= 1: eqz += int(abs(mnz - linz) < 1e-9)
        else: gapz.append(mnz - linz)
    print(f"T1  min over couplings of E prod(1 + y_g) against 1 + sum E y_g (exact LP over the joint law, 3 or 4 groups): sum P <= 1 in {n_le} cases: equal to 1e-9 in {eq_ok} (must be all); "
          f"sum P > 1 in {n_gt} cases: the minimum exceeds the linear value by {min(gap_gt):.2e} to {max(gap_gt):.2e} (must be positive, large against 1e-7: the converse); "
          f"max over couplings against the comonotone value (direct, and through my function): largest deviation {como_dev:.1e}")
    print(f"T2  floor functional prod(1 - zeta_g): min over couplings = 1 - sum E zeta when sum P <= 1: {eqz} of {n_le}; excess when sum P > 1: {min(gapz):.2e} to {max(gapz):.2e} (positive); "
          f"max over couplings = comonotone: largest deviation {comoz:.1e}")
    assert eq_ok == n_le and min(gap_gt) > 1e-6 and como_dev < 1e-9 and eqz == n_le and comoz < 1e-9
    # ------------------------------------------------------------------ T3
    bad = {q: 0 for q in ("UP", "C2", "Cjoint", "bonf", "como", "order", "rest", "closed")}; first_bad = 0; ncase = 0; worst_gain = 0.0; comowins = 0
    for rep in range(400):
        N = int(rng.integers(6, 40)); Gn = int(rng.integers(2, 6)); beta = 1.0
        mp = rng.normal(size=N) * 1.5; Dw = rng.exponential(0.6, size=N) + 0.05; mm = mp - Dw
        # items: group functions on random subsets of states, sum of plus and minus slack at most the width
        Sp = np.zeros((Gn, N)); Sm = np.zeros((Gn, N))
        for g in range(Gn):
            on = rng.random(N) < rng.uniform(0.05, 0.5); Sp[g, on] = rng.random(int(on.sum())); on = rng.random(N) < rng.uniform(0.05, 0.5); Sm[g, on] = rng.random(int(on.sum()))
        tot = Sp.sum(axis=0) + Sm.sum(axis=0); sc = np.where(tot > 0, np.minimum(1.0, rng.uniform(0.3, 1.0, N) * Dw / np.maximum(tot, 1e-300)), 1.0); Sp *= sc; Sm *= sc
        sp, sm = Sp.sum(axis=0), Sm.sum(axis=0); assert (mp - sp >= mm + sm - 1e-12).all()
        lz = lambda e: float(np.log(np.exp(-beta * e).sum()))
        lnZp, lnZm = lz(mp), lz(mm); wp = np.exp(-beta * mp - lnZp); wm = np.exp(-beta * mm - lnZm)
        y = np.expm1(beta * Sp); z = np.expm1(beta * Sm); c1 = (z * (1 + y)).sum(axis=0)
        zy = (z * (y.sum(axis=0)[None] - y)).sum(axis=0); zz = esym2(z)[1]; c2 = c1 + zz + zy; cj = np.expm1(beta * sm) * np.exp(beta * sp)
        bad["order"] += int((c2 < c1 - 1e-12).any() or (cj < c2 - 1e-9).any())
        Zm = math.exp(lnZm - lnZp); v = lambda Cv: lnZp + math.log(Zm - Cv)
        C1, C2, Cj = (float((wp * q).sum()) for q in (c1, c2, cj))
        it = lnZm
        for _ in range(2000): it = lnZm - math.log1p(C1 * math.exp(lnZp - it))
        bad["closed"] += int(abs(it - v(C1)) > 1e-9)
        zeta = -np.expm1(-beta * Sm); f1, f2, _ = esym2(zeta); S1, S2 = float((wm * f1).sum()), float((wm * f2).sum())
        Ub = lnZm + math.log(1 - S1 + S2); Uc = lnZm + math.log(comonotone_mean_of_product(zeta, wm, lambda V: np.prod(1.0 - V, axis=0))); Uf = lnZm + math.log(1 - S1)
        U0 = lz(mm + sm); bad["rest"] += int(v(Cj) < U0 - 1e-12); ncase += 1; worst_gain = max(worst_gain, v(C1) - Ub); comowins += int(Uc < v(C1) - 1e-12)
        for E in (mm + sm, mp - sp, mm + sm + rng.random(N) * (mp - sp - mm - sm)):
            t = lz(E)
            bad["UP"] += int(t > v(C1) + 1e-12); bad["C2"] += int(t > v(C2) + 1e-12); bad["Cjoint"] += int(t > v(Cj) + 1e-12); bad["bonf"] += int(t > Ub + 1e-12); bad["como"] += int(t > Uc + 1e-12)
            first_bad += int(t > Uf + 1e-9)
    print(f"T3  {ncase} random sandwiches of 6 to 39 states with 2 to 5 groups, three admissible energies each: violations of ln Z(E) <= bound: (UP) {bad['UP']}, with C_2 {bad['C2']}, with C'' {bad['Cjoint']}, "
          f"Bonferroni-floor {bad['bonf']}, comonotone-floor {bad['como']} (all must be 0); C' <= C_2 <= C'' pointwise violated in {bad['order']} cases; v(C'') < ln Z(m_- + s_-) in {bad['rest']} cases; "
          f"closed form ln(Z_- - C' Z_+) against 2000 iterations differs in {bad['closed']} cases; control, the first-order floor value as an upper bound: violated {first_bad} times (must be positive); "
          f"the comonotone-floor end is below (UP) in {comowins} of {ncase} cases; largest v(C') - Bonferroni-floor: {worst_gain:.3f} nats")
    assert all(v_ == 0 for v_ in bad.values()) and first_bad > 0
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
