"""
checks.py -- run-by-run verification of every claim of Theorem K1 (= 11.56) and of Theorem 11.52
against a finished r6lib.Run.  The true tail p(t) and the true mean A come from the instance, never from
the algorithm.  Returns a dict with
   'det'   : violations of statements claimed for EVERY run (on or off the good event)
   'good'  : violations of statements claimed on the good event, evaluated only if the events (V1), (V2), (V3)
             hold at every pass that the run actually made (a superset of the good event of the proof)
   'G'     : whether those events held,   plus tightness ratios.
"""
import mpmath as mp
import numpy as np
from fractions import Fraction
from r6lib import VALID_STRATS

TOL = mp.mpf(10) ** (-9)        # relative tolerance for inequalities between float-derived quantities


def _valid_oracle(run):
    return bool(np.all(np.isin(run.strat, VALID_STRATS))) if len(run.strat) else True


def check_2LP(run, extra_x=(0.25, 1.0, 3.0)):
    P, inst = run.P, run.inst
    e = mp.e
    eta = P.etaf
    out = dict(det=[], good=[], G=True, Gfail=[], ratios={})
    A = inst.A * e ** (-run.ln_s0)                 # in units of s_0
    K = P.K
    two_m = P.tab.two_m
    xs = P.xs
    v1 = _valid_oracle(run) if hasattr(inst, "strat") or len(run.strat) else True
    if getattr(run.oracle, "always_valid", None) is not None:
        v1 = run.oracle.always_valid
    if hasattr(run.oracle, "invalid_calls"):
        v1 = run.oracle.invalid_calls == 0
    if not v1:
        out["G"] = False
        out["Gfail"].append("V1")
    maxM = 0
    r_calls = mp.mpf(0)
    r_cnt = mp.mpf(0)
    r_count_ineq = mp.mpf(0)
    for rec in run.levels:
        j = rec["j"]
        lns = run.ln_s(j)
        Mneg = rec["Mneg"]
        # ---- deterministic claims
        if Mneg > (1 + eta) * e ** P.lam * P.nu0 * P.Mdag * (1 + TOL):
            out["det"].append(("iv: M_j^neg > (1+eta)e^lam nu0 Mdag", j))
        for ps in rec["passes"]:
            M = ps["M"]
            maxM = max(maxM, M)
            if not (M == K or M < 2 * Mneg * (1 + TOL)):
                out["det"].append(("iv: M > max(K, 2M^neg)", j, M))
            if M > P.Mbar * (1 + TOL):
                out["det"].append(("iv: M > Mbar", j, M))
            if not (M == K or M < P.cap_new * (1 + TOL)):
                out["det"].append(("cap40c5bd7: M >= 2max(e^lam Mdag, Mddag)", j, M, float(M / P.cap_new)))
            # ---- events at this pass
            p_s = inst.tail(lns)
            X_s = run.count_above(ps["t"], lns)
            if not (M * p_s <= K / (1 - eta) or X_s >= (1 - eta) * M * p_s):
                out["G"] = False
                out["Gfail"].append(("V2", j, M))
            thr = [lns - float(P.b)] + [lns - float(xs[l]) for l in range(0, P.L)]
            for lt in thr:
                pt = inst.tail(lt)
                Xt = run.count_above(ps["t"], lt)
                if not (Xt < K or Xt <= (1 + eta) * M * pt):
                    out["G"] = False
                    out["Gfail"].append(("V3", j, M))
        if rec["status"] in ("populated", "negligible"):
            qF = rec["qF"]
            if P.rdag >= 0:
                if not (qF * two_m > P.tab.ball[P.rdag]):
                    out["det"].append(("iii: level left with q <= pi-dagger", j, rec["status"]))
            else:
                if not (qF * two_m >= 1):
                    out["det"].append(("iii: level left with 2^m q < 1", j))
    if run.status == "closed":
        Lo, Up = run.final["Lo"], run.final["Up"]
        if mp.log(Up / Lo) > P.x_out + TOL:
            out["det"].append(("width", float(mp.log(Up / Lo)), float(P.x_out)))
    if run.queries() > P.Cmax * (1 + TOL):
        out["det"].append(("cost > C_max", float(mp.log(run.queries())), float(mp.log(P.Cmax))))
    out["ratios"]["M_over_Mbar"] = float(maxM / P.Mbar)
    out["ratios"]["M_over_Mdag"] = float(maxM / P.Mdag)
    out["ratios"]["M_over_capnew"] = float(maxM / P.cap_new) if maxM > K else 0.0
    out["ratios"]["lnq_over_lnCmax"] = float(mp.log(run.queries()) / mp.log(P.Cmax))
    out["ratios"]["q_over_Cvi"] = float(run.queries() / P.Cvi)
    # ---- claims on the good event
    if out["G"]:
        g = out["good"]
        if run.status != "closed":
            g.append(("i: no closure", run.status, run.abort_reason))
        else:
            Lo, Up = run.final["Lo"], run.final["Up"]
            if not (Lo <= A * (1 + TOL) and A <= Up * (1 + TOL)):
                g.append(("ii: bracket invalid", float(mp.log(Lo / A)), float(mp.log(Up / A))))
        for rec in run.levels:
            j = rec["j"]
            lns = run.ln_s(j)
            sj = rec["sj"]
            Mneg = rec["Mneg"]
            if rec["ell_entry"] > A * (1 + TOL):
                g.append(("ii: ell > A at entry", j))
            for ps in rec["passes"]:
                if ps["ell_after"] > A * (1 + TOL):
                    g.append(("ii: ell > A", j, ps["M"]))
                if inst.tail(lns) > ps["q"] * (1 + TOL):
                    g.append(("ii: p(s_j) > q", j, ps["M"]))
                if ps["populated"] and inst.tail(lns - float(P.b)) < ps["plow"] * (1 - TOL):
                    g.append(("ii: p(s_j e^-b) < p_low", j, ps["M"]))
            # (v) the count
            grid = [float(x) for x in xs[:P.L]] + list(extra_x)
            for x in grid:
                lhs = Mneg * inst.tail(lns - x)
                rhs = P.nu * e ** P.lam * e ** mp.mpf(x) / P.c_eta
                r_count_ineq = max(r_count_ineq, lhs / rhs)
                if lhs > rhs * (1 + TOL):
                    g.append(("v: count inequality", j, x, float(lhs / rhs)))
            if rec["passes"]:
                tfin = rec["passes"][-1]["t"]
                Mfin = rec["passes"][-1]["M"]
                for l in range(1, P.L + 1):
                    x = float(xs[l - 1])
                    used = run.count_above(tfin, lns - x)
                    c = P.cnt(xs[l - 1])
                    r_cnt = max(r_cnt, mp.mpf(used) / c)
                    if used > c * (1 + TOL):
                        g.append(("v: points above s_j e^-x exceed cnt", j, l, float(used / c)))
                    bound = min(P.Mbar, c)
                    r_calls = max(r_calls, mp.mpf(rec["calls"][l]) / bound)
                    if rec["calls"][l] > bound * (1 + TOL):
                        g.append(("vi: calls per level", j, l, float(rec["calls"][l] / bound)))
                    if rec["calls"][l] > Mfin:
                        g.append(("vi: calls > M_j", j, l))
        if run.queries() > P.Cvi * (1 + TOL):
            g.append(("vi: queries > 1 + Mbar + sum", float(run.queries() / P.Cvi)))
        out["ratios"]["calls_over_bound"] = float(r_calls)
        out["ratios"]["used_over_cnt"] = float(r_cnt)
        out["ratios"]["count_ineq"] = float(r_count_ineq)
    return out


def check_2L(run):
    """Theorem 11.52 (theory report 5ed4072 lines 3654-3716) and the remark of 40c5bd7 (M < 2e M-dagger)."""
    P, inst = run.P, run.inst
    e = mp.e
    out = dict(det=[], good=[], G=True, Gfail=[], ratios={})
    A = inst.A * e ** (-run.ln_s0)
    K, J = P.K, P.J
    two_m = P.tab.two_m
    xs = P.xs
    if not _valid_oracle(run):
        out["G"] = False
        out["Gfail"].append("V1")
    if hasattr(run.oracle, "invalid_calls") and run.oracle.invalid_calls > 0:
        out["G"] = False
        out["Gfail"].append("V1")
    maxM = 0
    r_calls = mp.mpf(0)
    r_cnt = mp.mpf(0)
    for rec in run.levels:
        j = rec["j"]
        lns = run.ln_s(j)
        if rec["Mneg"] > 4 * J * e ** 2 * P.Mdag * (1 + TOL):
            out["det"].append(("M_j^neg > 4Je^2 Mdag", j))
        for ps in rec["passes"]:
            M = ps["M"]
            maxM = max(maxM, M)
            if M > P.Mbar * (1 + TOL):
                out["det"].append(("M > 8Je^2 Mdag", j, M))
            if not (M == K or M < P.cap_new * (1 + TOL)):
                out["det"].append(("cap40c5bd7: M >= 2e Mdag", j, M, float(M / P.cap_new)))
            p_s = inst.tail(lns)
            X_s = run.count_above(ps["t"], lns)
            if M * p_s >= 2 * K and not (X_s >= M * p_s / 2):
                out["G"] = False
                out["Gfail"].append(("V2", j, M))
            i = 0
            while True:
                x = float(P.b) + i
                pt = inst.tail(lns - x)
                Xt = run.count_above(ps["t"], lns - x)
                if not (Xt <= max(2 * M * pt, mp.mpf(K) / 2)):
                    out["G"] = False
                    out["Gfail"].append(("V3", j, M, i))
                if lns - x < float(run.ln_s0) - 1.0:
                    break
                i += 1
        if rec["status"] in ("populated", "negligible"):
            qF = rec["qF"]
            # "a level that is left without stopping has r > r-dagger, that is q_j > 2K/M-dagger"
            if P.rdag >= 0 and not (qF * two_m > P.tab.ball[P.rdag]):
                out["det"].append(("level left with q <= 2K/Mdag", j, rec["status"]))
    if run.status == "closed":
        Lo, Up = run.final["Lo"], run.final["Up"]
        if mp.log(Up / Lo) > P.width_bound + TOL:
            out["det"].append(("width", float(mp.log(Up / Lo)), float(P.width_bound)))
    out["ratios"]["M_over_Mbar"] = float(maxM / P.Mbar) if P.Mbar != mp.inf else 0.0
    out["ratios"]["M_over_Mdag"] = float(maxM / P.Mdag) if P.Mdag != mp.inf else 0.0
    if out["G"]:
        g = out["good"]
        if run.status != "closed":
            g.append(("no closure", run.status, run.abort_reason))
        else:
            Lo, Up = run.final["Lo"], run.final["Up"]
            if not (Lo <= A * (1 + TOL) and A <= Up * (1 + TOL)):
                g.append(("bracket invalid", float(mp.log(Lo / A)), float(mp.log(Up / A))))
        for rec in run.levels:
            j = rec["j"]
            lns = run.ln_s(j)
            for ps in rec["passes"]:
                if ps["ell_after"] > A * (1 + TOL):
                    g.append(("ell > A", j))
                if inst.tail(lns) > ps["q"] * (1 + TOL):
                    g.append(("p(s_j) > q", j))
            if rec["passes"]:
                tfin = rec["passes"][-1]["t"]
                # the count for x in b + N
                i = 0
                while True:
                    x = float(P.b) + i
                    used = run.count_above(tfin, lns - x)
                    c = P.cnt(x)
                    r_cnt = max(r_cnt, mp.mpf(used) / c)
                    if used > c * (1 + TOL):
                        g.append(("count", j, i, float(used / c)))
                    if lns - x < float(run.ln_s0) - 1.0:
                        break
                    i += 1
                for l in range(1, P.L + 1):
                    bound = min(P.Mbar, 32 * K * J * e ** 3 * e ** xs[l - 1] + 4 * K)
                    r_calls = max(r_calls, mp.mpf(rec["calls"][l]) / bound)
                    if rec["calls"][l] > bound * (1 + TOL):
                        g.append(("calls per level", j, l, float(rec["calls"][l] / bound)))
        out["ratios"]["calls_over_bound"] = float(r_calls)
        out["ratios"]["used_over_cnt"] = float(r_cnt)
    return out
