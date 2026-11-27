"""Workstream K, numerical check (vii): the outer loop of Algorithm 2L+ at MEDIUM size (n_o = 36 ... 600), with real
sampling fluctuations, in the BOUNDED regime (nu_1 = 2 e^u n_o/theta, the choice of Theorem K2), where levels are left
as negligible and the ladder is closed by the tail lemma after 10^8 ... 10^18 outer points.

The outer landscape is radial (W depends on the outer distance d ~ Bin(n_o, 1/2)).  The list a_1, a_2, ... is sampled
exactly but stored by groups: block m of the doubling sequence (indices K 2^{m-1}+1 .. K 2^m) contributes multinomial
counts over the shells (stable_multinomial.py -- numpy's own multinomial loses the far-tail shells for n ~ 2^60, which
are the rare high levels this test is about; int64 counts; the checks use python integers).  The simulated inner oracle
is deterministic given (W, level, accuracy) -- value at the top, value at the bottom, the two adversarial rules of
sim_outer_loop -- or random per group; all points of a group then carry the same bracket, so the run of the algorithm
is exact.  Every claim of Theorem K1 is checked as in sim_outer_loop.py (C1 ... C8), after verifying the good event
(V2), (V3) on the realised counts.  Mutations (power of the test at this size): 'noharper', 'maxform', 'neg_tol',
'q_plain' as in sim_outer_loop.py.

    python3 sim_grouped.py          full run  -> out_sim_grouped.txt
    python3 sim_grouped.py quick    2 repetitions, no mutations -> out_sim_grouped_quick.txt
"""
import math, sys, time
import numpy as np
from sim_outer_loop import Params, radial_profile, binom_probs
from stable_multinomial import StableMultinomial


def run_grouped(rng, vals, probs, psi0, P, mode, max_log2=62, mut=()):
    """vals: W per shell, sorted increasingly (probs alike).  Returns a record like sim_outer_loop.run_2L, with the
    sample stored as counts[m][shell] per block m."""
    tab, lam, eta, b, K = P.tab, P.lam, P.eta, P.b, P.K
    u, n = P.u, P.n
    No = 2.0 ** P.n_o
    xs = np.array(P.x)
    s0 = math.exp(-psi0 - u * n)
    ell = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
    eb = math.exp(-b)
    S = len(vals)
    sampler = StableMultinomial(probs)
    counts = []                                        # counts[m][shell]
    gL = []; gU = []; gacc = []                        # per block: arrays over shells (state of the group)
    def add_block():
        m = len(counts)
        size = K if m == 0 else K * 2 ** (m - 1)
        c = sampler.sample(rng, size)
        counts.append(c)
        if mode == 0:
            t0 = rng.uniform(size=S)
        else:
            t0 = np.ones(S) if mode in (1, 4) else np.zeros(S)
        gL.append(np.minimum(vals * np.exp(-t0 * xs[0]), vals))
        gU.append(np.maximum(vals * np.exp((1 - t0) * xs[0]), vals))
        gacc.append(np.zeros(S, dtype=np.int16))
    levels = []
    Lsum = 0.0
    for j in range(P.J + 1):
        s = s0 * math.exp(j * lam)
        ell_in = ell
        Mneg = P.nu * s / (ell_in * (1.0 if "neg_tol" in mut else math.exp(b)))
        m = 0
        calls = [0] * (P.Lx + 1)
        while True:
            if m > P.mmax or K * 2 ** m > 2 ** max_log2:
                return dict(error="sample too large", m=m, level=j)
            while len(counts) <= m:
                add_block()
            M = K * 2 ** m
            N = 0
            for mm in range(m + 1):                    # classify the groups of blocks 0..m at level j
                c = counts[mm]; L_ = gL[mm]; U_ = gU[mm]; a_ = gacc[mm]
                while True:
                    und = np.nonzero((c > 0) & (U_ > s) & (L_ <= s * eb))[0]
                    if len(und) == 0:
                        break
                    if np.any(a_[und] >= P.Lx):
                        return dict(error="classification does not end at the last accuracy of the ladder")
                    a_[und] += 1
                    for l in np.unique(a_[und]):
                        calls[int(l)] += int(c[und][a_[und] == l].sum())
                    x = xs[a_[und]]
                    w = vals[und]
                    if mode == 0:
                        Lnew = w * np.exp(-rng.uniform(size=len(und)) * x)
                    elif mode == 1:
                        Lnew = w * np.exp(-x)
                    elif mode == 2:
                        Lnew = w.copy()
                    else:
                        keep = (x > b) & (w > s * np.exp(-x)) & (w * np.exp(-x) <= s * eb)
                        Lnew = np.where(keep, np.minimum(w, s * eb), w.copy() if mode == 3 else w * np.exp(-x))
                    Lnew = np.minimum(Lnew, w)
                    Unew = np.maximum(Lnew * np.exp(x), w)
                    L_[und] = np.maximum(L_[und], Lnew)
                    U_[und] = np.minimum(U_[und], Unew)
                N += int(c[U_ > s].sum())
            q = min(1.0, max(N, K) / ((1.0 if "q_plain" in mut else (1 - eta)) * M))
            pbar = None
            if N >= K:
                pbar = N / ((1 + eta) * M)
                k = tab.kball(No * pbar)
                ell = max(ell, s * eb * pbar)
                if "noharper" not in mut:
                    ell = max(ell, s * eb * tab.T[k] / No)
            if No * q < 1:
                tail, r = 0.0, -1
            else:
                r = tab.radius(q)
                tail = s * tab.E[r] / No if r <= P.n_o - 1 else math.inf
            rec = dict(s=s, M=M, m=m, q=q, N=N, populated=(N >= K), pbar=pbar, ell_in=ell_in, ell_out=ell, Mneg=Mneg, r=r, calls=calls, tail=tail)
            if tail <= P.theta * math.exp(b) * ell:
                Lsum_f = Lsum + ((1 - math.exp(-lam)) * eb * s * pbar if N >= K else 0.0)
                upper = s0 + sum(math.expm1(lam) * lv["s"] * lv["q"] for lv in levels) + tail
                lower = ell if "maxform" in mut else max(ell, Lsum_f)
                return dict(lower=lower, upper=upper, levels=levels, last=rec, counts=counts, ell=ell, Lsum=Lsum_f, s0=s0)
            if N >= K:
                Lsum += (1 - math.exp(-lam)) * eb * s * pbar
                levels.append(rec); break
            if M >= Mneg:
                levels.append(rec); break
            m += 1
    return dict(error="no closure within J + 1 levels")


def check_grouped(run, vals, probs, P, stats):
    lam, eta, b, K = P.lam, P.eta, P.b, P.K
    tol = 1 + 1e-9
    A = float((vals * probs).sum())
    tailp = np.concatenate([np.cumsum(probs[::-1])[::-1], [0.0]])
    exceed = lambda thr: float(tailp[np.searchsorted(vals, thr, side="right")])
    # cum[m][i] = number of points among the first K 2^m with shell index >= i  (python ints)
    cum = []
    run_tot = np.zeros(len(vals) + 1, dtype=object)
    for c in run["counts"]:
        suf = np.concatenate([np.cumsum(c[::-1].astype(object))[::-1], [0]])
        run_tot = run_tot + suf
        cum.append(run_tot.copy())
    count = lambda m, thr: int(cum[m][np.searchsorted(vals, thr, side="right")])
    seq = run["levels"] + [run["last"]]
    # the good event on the realised counts
    G = True
    for lv in seq:
        s = lv["s"]
        thr_list = [s * math.exp(-b_) for b_ in [b] + list(P.x[:-1])]
        ps = exceed(s)
        pt = [exceed(t) for t in thr_list]
        for m in range(len(cum)):
            M = K * 2 ** m
            if M * ps > K / (1 - eta) and count(m, s) < (1 - eta) * M * ps:
                G = False
            for t, p_t in zip(thr_list, pt):
                c = count(m, t)
                if c >= K and c > (1 + eta) * M * p_t:
                    G = False
    stats["good"] += int(G); stats["bad_event"] += int(not G)
    fails = []
    lower, upper = run["lower"], run["upper"]
    if upper > P.width_bound * lower * tol:
        fails.append(("C2 width", math.log(upper / lower), math.log(P.width_bound)))
    negpart = sum(math.expm1(lam) * lv["s"] * lv["q"] for lv in run["levels"] if not lv["populated"])
    if negpart > P.etap * math.exp(b) * run["ell"] * tol:
        fails.append(("C2b negligible budget",))
    stats["neg_share"] = max(stats["neg_share"], negpart / (P.etap * math.exp(b) * run["ell"]))
    stats["widest"] = max(stats["widest"], math.log(upper / lower))
    stats["width_slack"] = min(stats["width_slack"], math.log(P.width_bound) - math.log(upper / lower))
    for jj, lv in enumerate(seq):
        for l in range(1, P.Lx + 1):
            if lv["calls"][l] > count(lv["m"], lv["s"] * math.exp(-P.x[l - 1]) * (1 - 1e-12)):
                fails.append(("C7 calls", jj, l))
    if G:
        if not (lower <= A * tol and A <= upper * tol):
            fails.append(("C1 validity", lower, A, upper))
        for jj, lv in enumerate(seq):
            s, M, q = lv["s"], lv["M"], lv["q"]
            if exceed(s) > q * tol:
                fails.append(("C3 q < p(s)", jj))
            if lv["populated"] and lv["pbar"] > exceed(s * math.exp(-b)) * tol:
                fails.append(("C3 pbar", jj))
            if lv["ell_out"] > A * tol:
                fails.append(("C3 ell > A", jj))
            if M > max(K, 2 * lv["Mneg"]) * tol:
                fails.append(("C5 M > max(K, 2 Mneg)", jj))
            if lv["Mneg"] > (1 + eta) * math.exp(lam) * P.nu0 * P.Mdag * tol:
                fails.append(("C5 Mneg bound", jj))
            if M > P.Mbar * tol:
                fails.append(("C5 M > Mbar", jj))
            stats["largest_M_over_Mdag"] = max(stats["largest_M_over_Mdag"], M / P.Mdag)
            for l in range(0, P.Lx):
                x = P.x[l]
                lhs = lv["Mneg"] * exceed(s * math.exp(-x))
                rhs = P.nu * math.exp(lam) * (1 + eta) / (1 - eta) * math.exp(x)
                if lhs > rhs * tol:
                    fails.append(("C6 count lemma", jj, l))
                stats["tightest_count"] = max(stats["tightest_count"], lhs / rhs)
                if count(lv["m"], s * math.exp(-x)) > P.cnt(x) * tol:
                    fails.append(("C6 sample count", jj, l))
            for l in range(1, P.Lx + 1):
                if lv["calls"][l] > min(M, P.cnt(P.x[l - 1])) * tol:
                    fails.append(("C8 calls bound", jj, l))
        for jj, lv in enumerate(run["levels"]):
            if lv["r"] <= P.rdag:
                fails.append(("C4 closure radius", jj, lv["r"], P.rdag))
            stats["populated" if lv["populated"] else "negligible"] += 1
        last = run["last"]
        stats["closed_empty" if last["r"] == -1 else ("closed_populated" if last["populated"] else "closed_unpopulated")] += 1
        if any(not lv["populated"] for lv in run["levels"]):
            stats["runs_with_negligible_levels"] += 1
        stats["log10_M"].append(math.log10(max(lv["M"] for lv in seq)))
        stats["closing"].append((last["r"], P.rdag, P.pu * P.n_o))
    stats["runs"] += 1
    return fails


def new_stats():
    return dict(runs=0, good=0, bad_event=0, widest=0.0, width_slack=math.inf, tightest_count=0.0, largest_M_over_Mdag=0.0,
                populated=0, negligible=0, closed_empty=0, closed_populated=0, closed_unpopulated=0, runs_with_negligible_levels=0,
                neg_share=0.0, log10_M=[], closing=[], skipped=0)


def suite(rng, cases, reps, out, mut=(), verbose=True):
    stats = new_stats()
    allfails = []
    t0 = time.time()
    for (u, n_o) in cases:
        for kind in range(8):
            for rep in range(reps):
                n_i = 4
                n = n_o + n_i
                F = radial_profile(rng, n_o, u, kind) + float(rng.uniform(-2, 2))
                psi0 = float(F[int(rng.integers(0, n_o + 1))])
                order = np.argsort(np.exp(-F), kind="stable")
                vals = np.exp(-F)[order]
                probs = binom_probs(n_o)[order]
                b = float(rng.choice([0.25, 0.5, 1.0]))
                lam = float(rng.choice([0.5, 1.0])) * float(rng.uniform(0.9, 1.0))
                eta = float(rng.choice([0.25, 0.5]))
                etap = float(rng.choice([0.1, 0.5]))
                theta = float(rng.choice([0.1, 0.5]))
                top = 2 * u * n_i
                jit = float(rng.uniform(0.95, 1.0))
                ladder = sorted({x * jit for x in (top / 2, 2.0, 1.0) if b < x * jit < top}, reverse=True) + [b * (1 - 1e-9)]
                P = Params(n, n_o, u, lam, eta, etap, theta, b, ladder, delta=0.05)          # bounded regime: nu1 = 2 e^u n_o/theta
                run = run_grouped(rng, vals, probs, psi0, P, mode=(kind + rep) % 5, mut=mut)
                if "error" in run:
                    if run["error"].startswith("sample too large"):
                        stats["skipped"] += 1; continue
                    allfails.append((u, n_o, kind, [(run["error"],)])); continue
                f = check_grouped(run, vals, probs, P, stats)
                if f:
                    allfails.append((u, n_o, kind, f[:3]))
        if verbose:
            out(f"  u = {u}, n_o = {n_o}: cumulative runs {stats['runs']}, negligible levels so far {stats['negligible']}, "
                f"failures {len(allfails)}  ({time.time() - t0:.0f} s)")
    cl = stats.pop("closing")
    lm = sorted(stats.pop("log10_M"))
    stats["closed_at_r<=p_u*n_o"] = sum(1 for (r, rd, pn) in cl if 0 <= r <= pn)
    stats["closed_at_r<=r_dagger"] = sum(1 for (r, rd, pn) in cl if 0 <= r <= rd)
    if lm:
        stats["log10_M(min,median,max)"] = (round(lm[0], 2), round(lm[len(lm) // 2], 2), round(lm[-1], 2))
        stats["runs_with_M>1e12"] = sum(1 for v in lm if v > 12)
    for key in ("widest", "width_slack", "tightest_count", "largest_M_over_Mdag", "neg_share"):
        stats[key] = round(stats[key], 4)
    return stats, allfails


def fail_kinds(allfails):
    kinds = {}
    for (_, _, _, fl) in allfails:
        for f in fl:
            kinds[f[0]] = kinds.get(f[0], 0) + 1
    return kinds


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    t0 = time.time()
    cases = [(0.5, 300), (0.5, 400), (0.5, 600), (1.0, 100), (1.0, 150), (1.0, 200), (2.0, 36), (2.0, 48), (2.0, 60)]
    out("Outer loop of Algorithm 2L+ at medium size, grouped exact sample, bounded regime nu_1 = 2 e^u n_o/theta")
    stats, allfails = suite(np.random.default_rng(31), cases, 2 if quick else 20, out)
    out(f"  stats: {stats}")
    out(f"  failures: {len(allfails)}" + ("" if not allfails else f"   first: {allfails[:3]}"))
    ok = len(allfails) == 0 and stats["negligible"] > 0 and stats["runs_with_negligible_levels"] > 0
    out(f"medium-size suite passed (no failure; levels are left as negligible in the bounded regime): {ok}   ({time.time() - t0:.0f} s)")
    if not quick:
        out("")
        out("Power of the test at this size (mutated algorithm, same checks, 3 repetitions per case and profile):")
        expected = {"noharper": "C4 closure radius", "maxform": "C2 width", "neg_tol": "C6 count lemma", "q_plain": "C3 q < p(s)"}
        for mname, exp_check in expected.items():
            st, fl = suite(np.random.default_rng(32), cases, 3, out, mut=(mname,), verbose=False)
            kinds = fail_kinds(fl)
            det = kinds.get(exp_check, 0) > 0
            out(f"  mutation {mname:9s}: {len(fl):3d} of {st['runs']:3d} runs fail; kinds {kinds};  expected check '{exp_check}' fires: {det}")
            ok = ok and det
        out(f"all mutations detected and unmutated suite clean: {ok}   ({time.time() - t0:.0f} s)")
    open("out_sim_grouped.txt" if not quick else "out_sim_grouped_quick.txt", "w").write("\n".join(lines) + "\n")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
