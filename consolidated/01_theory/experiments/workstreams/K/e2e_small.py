"""Workstream K, numerical check (v): end to end at small size, with REAL inner brackets.

Part A -- Proposition K0 (base family): the two-sample bracket with a CERTIFIED width,
    L = Ahat/(1+eta),  U = Ahat/(1-eta) + that 2^{-d} E_rhat(d),   U/L <= (1+eta)/(1-eta) (1 + G2_d(rhat)),
on u-Lipschitz functions of an enumerated cube; the two samples of size M are drawn exactly (multinomial counts).
Checked: coverage (failure rate against the bound 4 e^{-eta^2 K/(3(1+eta))}), and that on the good event of the proof
the width never exceeds the certified one (with small K failures do occur; they are counted, not hidden).

Part B -- Algorithm 2L+ (Theorem K1) on Q_{n_o} x Q_{n_i}, n = n_o + n_i <= 16, psi an explicit u-Lipschitz function on
the whole cube, the inner procedure the base bracket of Part A run on the fibre {a} x Q_{n_i} with its own randomness
(two samples of size M_in drawn exactly; cost 2 M_in evaluations per call), all constants (K, nu, J, delta', M_in, K_in)
from the formulas of the report, delta = 0.05.  Checked on every run: L <= A <= U, U/L <= the bound of Theorem K1, the
number of evaluations <= C_max, and that no abort condition is met.  At this size the inner brackets cost more than
enumerating the fibre -- the run tests the logic of the complete two-level pipeline with real randomness, not its cost.
"""
import math, sys, time
import numpy as np
from sim_outer_loop import Tables, Params, cube_dist, rand_lipschitz


def base_params(d, u, x, log_inv_delta):
    """(eta, K, M, rhat, tailcoef) of the base bracket of accuracy x on Q_d with failure probability delta':
    eta = min(1/2, tanh(x/4)); K = ceil(3(1+eta)/eta^2 ln(4/delta')); r* the largest radius <= d-1 with
    ln(1 + G2(r')) <= x - ln((1+eta)/(1-eta)) for all r' <= r*;  M = ceil(K 2^d/((1-eta)|B(d, r*)|));
    rhat = r(K/((1-eta) M)) <= r*, tailcoef = 2^{-d} E_rhat  (0 if 2^d q_+ < 1).  None if no radius qualifies."""
    eta = min(0.5, math.tanh(x / 4))
    budget = x - math.log((1 + eta) / (1 - eta))
    if budget <= 0:
        return None
    tab = Tables(d, u, eta)
    rstar = -1
    for r in range(d):
        if math.log1p(tab.G2[r]) <= budget:
            rstar = r
        else:
            break
    if rstar < 0:
        return None
    K = math.ceil(3 * (1 + eta) / eta ** 2 * (math.log(4) + log_inv_delta))
    M = math.ceil(K * 2.0 ** d / ((1 - eta) * tab.ball[rstar + 1]))
    qplus = K / ((1 - eta) * M)
    if 2.0 ** d * qplus < 1:
        rhat, coef = -1, 0.0
    else:
        rhat = tab.radius(qplus)
        coef = tab.E[rhat] / 2.0 ** d
    assert rhat <= rstar
    width = math.log((1 + eta) / (1 - eta)) + (math.log1p(tab.G2[rhat]) if rhat >= 0 else 0.0)
    return dict(eta=eta, K=K, M=M, rhat=rhat, coef=coef, width=width, d=d)


def base_bracket_batch(rng, vals, bp):
    """vals: (B, 2^d) weights of B fibres.  Returns (L, U, that, good) for the base bracket with parameters bp, the two
    samples of size M drawn exactly as multinomial counts.  good[i]: the events (E1'), (E2'), (E3') of the proof hold."""
    B, N = vals.shape
    eta, K, M = bp["eta"], bp["K"], bp["M"]
    order = np.argsort(-vals, axis=1)
    sv = np.take_along_axis(vals, order, axis=1)                       # decreasing
    p = np.full(N, 1.0 / N)
    c1 = rng.multinomial(M, p, size=B)
    c1s = np.take_along_axis(c1, order, axis=1)
    cum = np.cumsum(c1s, axis=1)
    pos = np.argmax(cum >= K, axis=1)                                  # K-th largest sampled weight
    that = sv[np.arange(B), pos]
    c2 = rng.multinomial(M, p, size=B)
    c2s = np.take_along_axis(c2, order, axis=1)
    trunc = np.minimum(sv, that[:, None])
    Ahat = (c2s * trunc).sum(axis=1) / M
    L = Ahat / (1 + eta)
    U = Ahat / (1 - eta) + that * bp["coef"]
    # the events of the proof (for the statistics of part A)
    p_gt = (vals > that[:, None]).mean(axis=1)
    p_ge = (vals >= that[:, None]).mean(axis=1)
    Etrunc = np.minimum(vals, that[:, None]).mean(axis=1)
    good = (p_gt <= K / ((1 - eta) * M) + 1e-15) & (p_ge >= K / ((1 + eta) * M) - 1e-15) & (np.abs(Ahat - Etrunc) <= eta * Etrunc * (1 + 1e-12))
    return L, U, that, good


def part_A(rng, out):
    out("Part A: base bracket (Proposition K0) on enumerated cubes")
    ok = True
    tot = dict(calls=0, invalid=0, good=0, wide_on_good=0, invalid_on_good=0)
    d = 10
    D = cube_dist(d)
    rows = []
    for u in (0.5, 1.0, 2.0):
        for x in (0.6, 1.0, 2.0, 4.0):
            for lid in (math.log(1 / 0.3), math.log(1 / 1e-3)):          # delta' = 0.3 (failures visible) and 1e-3
                bp = base_params(d, u, x, lid)
                if bp is None:
                    continue
                inval = good = wide = cnt = 0
                for kind in range(8):
                    psis = np.stack([rand_lipschitz(rng, d, u, D, kind) + float(rng.uniform(-3, 3)) for _ in range(3)])
                    vals = np.exp(-psis)
                    reps = 40
                    V = np.repeat(vals, reps, axis=0)
                    L, U, that, g = base_bracket_batch(rng, V, bp)
                    A = V.mean(axis=1)
                    bad = (L > A * (1 + 1e-12)) | (U < A * (1 - 1e-12))
                    w = np.log(U / L)
                    inval += int(bad.sum()); good += int(g.sum()); cnt += len(A)
                    wide += int((g & (w > bp["width"] + 1e-9)).sum())
                    tot["invalid_on_good"] += int((g & bad).sum())
                bound = 4 * math.exp(-bp["eta"] ** 2 * bp["K"] / (3 * (1 + bp["eta"])))
                rows.append((u, x, math.exp(-lid), bp["K"], bp["M"], bp["rhat"], bp["width"], cnt, inval / cnt, 1 - good / cnt, bound))
                tot["calls"] += cnt; tot["invalid"] += inval; tot["good"] += good; tot["wide_on_good"] += wide
                # the failure rate of the bracket (invalid or event failed) must not exceed the bound by more than sampling noise
                if (cnt - good) / cnt > bound + 4 * math.sqrt(bound * (1 - min(bound, 1)) / cnt) + 3 / cnt:
                    ok = False; out(f"   event failure rate {1 - good / cnt:.4f} above the bound {bound:.4f}  (u={u}, x={x})")
    out(f"{'u':>4} {'x':>4} {'delta_in':>8} {'K':>5} {'M':>8} {'rhat':>4} {'cert.width':>10} {'calls':>6} {'invalid':>8} {'event fails':>11} {'bound':>8}")
    for r in rows:
        out(f"{r[0]:4.1f} {r[1]:4.1f} {r[2]:8.0e} {r[3]:5d} {r[4]:8d} {r[5]:4d} {r[6]:10.3f} {r[7]:6d} {r[8]:8.4f} {r[9]:11.4f} {r[10]:8.4f}")
    out(f"  total calls {tot['calls']}, invalid brackets {tot['invalid']}, calls on the good event {tot['good']}; on the good event: "
        f"invalid {tot['invalid_on_good']}, wider than certified {tot['wide_on_good']}")
    ok = ok and tot["invalid_on_good"] == 0 and tot["wide_on_good"] == 0
    out(f"Part A as expected (valid and within the certified width on the good event; failure rates within the bound): {ok}")
    return ok


def run_e2e(rng, w, psi0, P, bps, max_points=3_000_000):
    """Algorithm 2L+ with real inner brackets.  w: (2^{n_o}, 2^{n_i}) table of e^{-psi}; psi0 = psi at the reference point.
    bps[l], l = 1..L: parameters of the base bracket of accuracy x_l on Q_{n_i}.  Returns dict."""
    tab, lam, eta, b, K, u, n, n_i = P.tab, P.lam, P.eta, P.b, P.K, P.u, P.n, P.n_i
    No = 2.0 ** P.n_o
    s0 = math.exp(-psi0 - u * n)
    ell = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** n
    eb = math.exp(-b)
    aidx = np.zeros(0, dtype=np.int64); Lb = np.zeros(0); Ub = np.zeros(0); acc = np.zeros(0, dtype=np.int16)
    queries = 1
    cost = [0] + [(2 * bp["M"] if bp is not None else 2 ** n_i) for bp in bps[1:]]
    Cmax = 1 + 2 * P.Mbar + sum(min(2 * P.Mbar, (P.J + 1) * P.cnt(P.x[l - 1])) * cost[l] for l in range(1, P.Lx + 1))
    levels = []
    Lsum = 0.0
    ncalls = [0] * (P.Lx + 1)
    for j in range(P.J + 1):
        s = s0 * math.exp(j * lam)
        ell_in = ell
        Mneg = P.nu * s / (ell_in * math.exp(b))
        M = K
        while True:
            if M > K * 2 ** P.mmax or M > max_points:
                return dict(abort="sample size cap", M=M)
            if len(aidx) < M:
                extra = M - len(aidx)
                new = rng.integers(0, w.shape[0], size=extra)
                aidx = np.concatenate([aidx, new])
                w0 = w[new, 0]                                           # one evaluation at (a, 0): the trivial bracket
                Lb = np.concatenate([Lb, w0 * math.exp(-u * n_i)])
                Ub = np.concatenate([Ub, w0 * math.exp(u * n_i)])
                acc = np.concatenate([acc, np.zeros(extra, dtype=np.int16)])
                queries += extra
            while True:
                und = np.nonzero((Ub[:M] > s) & (Lb[:M] <= s * eb))[0]
                if len(und) == 0:
                    break
                if np.any(acc[und] >= P.Lx):
                    return dict(abort="a point is not classified at the last accuracy")
                acc[und] += 1
                for l in np.unique(acc[und]):
                    sel = und[acc[und] == l]
                    for c0 in range(0, len(sel), 20000):
                        ch = sel[c0:c0 + 20000]
                        if bps[int(l)] is None:                              # no two-sample bracket of this accuracy: enumerate the fibre
                            Ln = Un = w[aidx[ch]].mean(axis=1)
                        else:
                            Ln, Un, _, _ = base_bracket_batch(rng, w[aidx[ch]], bps[int(l)])
                        Lb[ch] = np.maximum(Lb[ch], Ln)
                        Ub[ch] = np.minimum(Ub[ch], Un)
                    ncalls[int(l)] += len(sel)
                    queries += len(sel) * cost[int(l)]
                if queries > Cmax:
                    return dict(abort="query budget")
            N = int((Ub[:M] > s).sum())
            q = min(1.0, max(N, K) / ((1 - eta) * M))
            pbar = None
            if N >= K:
                pbar = N / ((1 + eta) * M)
                k = tab.kball(No * pbar)
                ell = max(ell, s * eb * pbar, s * eb * tab.T[k] / No)
            if No * q < 1:
                tail = 0.0
            else:
                r = tab.radius(q)
                tail = s * tab.E[r] / No if r <= P.n_o - 1 else math.inf
            if tail <= P.theta * math.exp(b) * ell:
                Lsum_f = Lsum + ((1 - math.exp(-lam)) * eb * s * pbar if N >= K else 0.0)
                upper = s0 + sum(math.expm1(lam) * lv[0] * lv[1] for lv in levels) + tail
                return dict(lower=max(ell, Lsum_f), upper=upper, queries=queries, Cmax=Cmax, points=len(aidx), ncalls=ncalls, levels=len(levels) + 1)
            if N >= K:
                Lsum += (1 - math.exp(-lam)) * eb * s * pbar
                levels.append((s, q)); break
            if M >= Mneg:
                levels.append((s, q)); break
            M *= 2
    return dict(abort="no closure within J + 1 levels")


def part_B(rng, out, reps):
    out("\nPart B: Algorithm 2L+ end to end with real inner two-sample brackets")
    ok = True
    stats = dict(runs=0, invalid=0, too_wide=0, aborts=0, max_queries_over_Cmax=0.0, widest=0.0, min_slack=math.inf, points=0, calls=0, enumerated_rungs=0, sampled_rungs=0)
    for (n_o, n_i) in ((6, 6), (8, 6), (6, 8)):
        n = n_o + n_i
        D = cube_dist(n)
        for rep in range(reps):
            u = float(rng.choice([0.5, 1.0, 2.0]))
            kind = rep % 8
            if kind == 4:                                                # Lipschitz regularisation of noise, in chunks (memory)
                z = rng.normal(0, u * n * 0.3, size=2 ** n)
                psi = np.full(2 ** n, np.inf)
                for c0 in range(0, 2 ** n, 1024):
                    psi = np.minimum(psi, (z[c0:c0 + 1024, None] + u * D[c0:c0 + 1024]).min(0))
            else:
                psi = rand_lipschitz(rng, n, u, D, kind)
            psi = psi + float(rng.uniform(-3, 3))
            w = np.exp(-psi).reshape(2 ** n_o, 2 ** n_i)                 # outer coordinates = high bits; the reference point is x = 0
            A = float(w.mean())
            b = float(rng.choice([0.5, 1.0]))
            lam = float(rng.choice([0.25, 0.5])) * float(rng.uniform(0.9, 1.0))
            eta = float(rng.choice([0.25, 0.5]))
            etap = float(rng.choice([0.2, 0.5]))
            theta = float(rng.choice([0.2, 0.5]))
            ladder = [x for x in (6.0, 3.0, 1.7) if b < x < 2 * u * n_i] + [b]
            P = Params(n, n_o, u, lam, eta, etap, theta, b, ladder, delta=0.05)
            log_inv_dp = math.log(4 * P.Lx * P.Mbar / 0.05)              # delta' = delta/(4 L Mbar)
            bps = [None] + [base_params(n_i, u, x, log_inv_dp) for x in P.x[1:]]
            stats["enumerated_rungs"] += sum(1 for bp in bps[1:] if bp is None)
            stats["sampled_rungs"] += sum(1 for bp in bps[1:] if bp is not None)
            res = run_e2e(rng, w, float(psi[0]), P, bps)
            stats["runs"] += 1
            if "abort" in res:
                stats["aborts"] += 1; ok = False
                out(f"   ABORT: {res}"); continue
            valid = res["lower"] <= A * (1 + 1e-12) and A <= res["upper"] * (1 + 1e-12)
            width = math.log(res["upper"] / res["lower"])
            stats["invalid"] += int(not valid)
            stats["too_wide"] += int(width > math.log(P.width_bound) + 1e-9)
            stats["widest"] = max(stats["widest"], width)
            stats["min_slack"] = min(stats["min_slack"], math.log(P.width_bound) - width)
            stats["max_queries_over_Cmax"] = max(stats["max_queries_over_Cmax"], res["queries"] / res["Cmax"])
            stats["points"] = max(stats["points"], res["points"])
            stats["calls"] += sum(res["ncalls"])
            if not valid or width > math.log(P.width_bound) + 1e-9 or res["queries"] > res["Cmax"]:
                ok = False
                out(f"   FAILURE n_o={n_o} n_i={n_i} kind={kind} u={u}: valid={valid} width={width:.3f} bound={math.log(P.width_bound):.3f} queries/Cmax={res['queries'] / res['Cmax']:.3g}")
    for key in ("widest", "min_slack", "max_queries_over_Cmax"):
        stats[key] = float(f"{stats[key]:.4g}")
    out(f"  stats: {stats}")
    out(f"Part B as expected (every bracket valid and within the width bound, no abort, queries <= C_max): {ok}")
    return ok


def main():
    lines = []
    def out(s=""):
        print(s); lines.append(s); sys.stdout.flush()
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    t0 = time.time()
    rng = np.random.default_rng(2026)
    okA = part_A(rng, out)
    okB = part_B(rng, out, reps=8 if quick else 28)
    out(f"\nall as expected: {okA and okB}   ({time.time() - t0:.0f} s)")
    open("out_e2e_small.txt" if not quick else "out_e2e_small_quick.txt", "w").write("\n".join(lines) + "\n")
    return okA and okB


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
