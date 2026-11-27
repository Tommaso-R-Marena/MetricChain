"""X-011f: three nested levels run literally, end to end, on small cubes with exact truth.

Top level: Algorithm 2L+ on an outer block of n1 sites; every rung of its ladder is served by a *real run* of
Algorithm 2L+ on the fibre (outer block n2 sites), whose rungs are served by exact enumeration of the base block
(n3 sites).  No oracle and no mean-run model: every bracket the top level sees is the output of a randomised
procedure that queried the energy table.  The three blocks may have different slopes (the transfer of Theorem K1
in ``metricchain_eng.twolevel.hetero``), which makes this also the end-to-end test of X-014.

Checked in every run: the final bracket contains A; its width is at most the certified accuracy; no abort at
either level; every bracket a nested run returned contains its fibre average; the number of queries is at most
the nested cost bound (the top level's C_max with every rung charged the C_max of the run that serves it).

Implementation notes.  (i) A direct transcription of ``K_REPORT.md`` §2.2 (theory branch) with the substitutions of
``hetero.py``; shared by both levels (``run_level``).  (ii) Results of servers are *cached per fibre and rung*: two
sample points that are the same outer point share one nested run.  The theorem charges and draws them
separately; sharing can only lower the cost and the number of events that must be valid, and without it a
literal run is out of reach (the samples are much larger than the outer cube at these sizes).  Both counts are
reported: the queries actually made, and the theorem's accounting (every sample point charged its own calls).

    python experiments/eng/twolevel/nested_literal.py [--runs 6] [--procs 3]     # appends to results/x011_nested_literal.jsonl
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hetero_literal as hl  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.certified import acc_const, tables  # noqa: E402
from metricchain_eng.twolevel.tables import LN2  # noqa: E402


def lcmax(C: H.HConstants, lC) -> float:
    """ln C_max of a level whose rung l is served at cost bound e^{lC[l-1]}."""
    return float(np.logaddexp.reduce(np.concatenate([[0.0, LN2 + C.lM_bar], C.lmult() + np.asarray(lC, dtype=float)])))


def run_level(psi0: float, psi_ref: np.ndarray, n_o: int, C: H.HConstants, T, serve, rng) -> dict:
    """Algorithm 2L+ on an outer cube of n_o sites.

    psi0       the energy at the reference point of the whole block (one query);
    psi_ref    psi(a, reference of the inner block) for every outer point a (one query per point used);
    serve      serve(a, l) -> (ln L, ln U, queries): the bracket of the fibre average W(a) from the procedure of rung l.
    Returns status, the bracket (ln L, ln U), the queries made (sharing nested results between equal points) and
    the theorem's count (no sharing)."""
    lam, eta, b = C.lam, C.eta, C.b
    xs = np.asarray(C.xs)
    L = len(xs) - 1
    K = C.K
    lnu = math.log(K) + math.log(C.nu0)
    ls0 = -psi0 - C.omega
    lell = -psi0 - C.omega - C.l2p
    omega_i = xs[0] / 2
    npts = 2 ** n_o
    cache: dict = {}                       # (a, l) -> (lL, lU, queries)
    seen = np.zeros(npts, dtype=bool)
    q_real = 1                             # queries actually made
    q_thm = 1                              # the theorem's accounting
    idx = np.empty(0, dtype=np.int64)
    lL = np.empty(0)
    lU = np.empty(0)
    rung = np.empty(0, dtype=np.int16)
    lSigma = -np.inf
    upper_terms = [ls0]
    Mmax = K * 2 ** C.m_max
    lball = T.lball
    status = None
    nested_calls = 0
    result = None
    for j in range(C.J + 1):
        lsj = ls0 + j * lam
        M = K
        lell_entry = lell
        while True:
            if M > Mmax:
                status = "abort: sample size"
                break
            if M > len(idx):
                new = rng.integers(0, npts, size=M - len(idx))
                q_thm += len(new)
                q_real += int(np.count_nonzero(~seen[np.unique(new)]))
                seen[new] = True
                idx = np.concatenate([idx, new])
                lL = np.concatenate([lL, -psi_ref[new] - omega_i])
                lU = np.concatenate([lU, -psi_ref[new] + omega_i])
                rung = np.concatenate([rung, np.zeros(len(new), dtype=np.int16)])
            ok = True
            while True:                                       # classify the first M points at level j
                todo = np.flatnonzero((lU[:M] > lsj) & (lL[:M] <= lsj - b))
                if todo.size == 0:
                    break
                if np.any(rung[todo] >= L):
                    ok = False
                    break
                rung[todo] += 1
                pairs = np.stack([idx[todo], rung[todo]], axis=1)
                for a, l in np.unique(pairs, axis=0):
                    key = (int(a), int(l))
                    if key not in cache:
                        cache[key] = serve(int(a), int(l))
                        q_real += cache[key][2]
                        nested_calls += 1
                    lo, hi, cost = cache[key]
                    sel = todo[(pairs[:, 0] == a) & (pairs[:, 1] == l)]
                    lL[sel] = np.maximum(lL[sel], lo)
                    lU[sel] = np.minimum(lU[sel], hi)
                    q_thm += cost * len(sel)
            if not ok:
                status = "abort: unclassified at the last rung"
                break
            N = int(np.count_nonzero(lU[:M] > lsj))
            lq = min(0.0, math.log(max(N, K)) - math.log((1 - eta) * M))
            lplow = None
            if N >= K:
                lplow = math.log(N) - math.log((1 + eta) * M)
                k = max(int(np.searchsorted(lball, max(0.0, n_o * LN2 + lplow) + 1e-10, side="right")) - 1, 0)
                lell = max(lell, lsj - b + lplow, lsj - b - n_o * LN2 + float(T.lT[k]))
            if n_o * LN2 + lq < -1e-12:
                ltail = -np.inf
            else:
                r = T.radius(lq)
                ltail = lsj - n_o * LN2 + float(T.lE[r]) if r <= n_o - 1 else np.inf
            if ltail <= C.lth + b + lell:                      # closure test: stop
                lLow = max(lell, lSigma)
                if N >= K:
                    lLow = max(lLow, float(np.logaddexp(lSigma, math.log(-math.expm1(-lam)) - b + lsj + lplow)))
                result = (lLow, float(np.logaddexp.reduce(upper_terms + [ltail])))
                break
            if N >= K:                                         # populated
                upper_terms.append(lsj + math.log(math.expm1(lam)) + lq)
                lSigma = float(np.logaddexp(lSigma, math.log(-math.expm1(-lam)) - b + lsj + lplow))
                break
            if math.log(M) >= lnu + lsj - lell_entry - b:      # negligible
                upper_terms.append(lsj + math.log(math.expm1(lam)) + lq)
                break
            M *= 2
        if result is not None or status:
            break
    else:
        status = "abort: level J left"
    if result is None:
        return dict(status=status or "abort", lL=ls0, lU=ls0 + 2 * C.omega, q_real=q_real, q_thm=q_thm, level=j, M=len(idx), nested_calls=nested_calls)
    return dict(status="closed", lL=result[0], lU=result[1], q_real=q_real, q_thm=q_thm, level=j, M=len(idx), nested_calls=nested_calls)


# ---------------------------------------------------------------------------------------------
# Designs
# ---------------------------------------------------------------------------------------------
EXT_SUM = 3 * math.e + 2          # e^lam (1 + eta)/(1 - eta) + eta' + theta at lam = 1, eta = 1/2, eta' = theta = 1


def middle_design(block: H.Block, j: int, k: int, x: float) -> H.HDesign:
    """A level on ``block`` (outer block: k sites of type j) with certified accuracy at most x: the parameters
    lam = 1, eta = 1/2, eta' = theta = 1 where the accuracy allows, else lam = eta = eta' = theta = 1/4."""
    x0 = 2 * (H.omega(block) - block[j][0] * k)
    lp = H.l2p(block)
    if x >= math.log(EXT_SUM) + 0.3:
        bm = min(math.log((math.exp(x) - math.exp(lp)) / EXT_SUM) - 1e-9, 0.9 * x0)
        return H.HDesign(j=j, k=k, lam=1.0, eta=0.5, etap=1.0, b=bm, Lr=3, theta=1.0, bounded=False, name="lam=1, eta=1/2")
    c = 0.25
    bm = min(math.log(math.exp(x) - math.exp(lp)) - acc_const(c) - 1e-9, 0.9 * x0)
    if bm <= 0:
        raise ValueError("accuracy too small for a nested level")
    return H.HDesign(j=j, k=k, lam=c, eta=c, etap=c, b=bm, Lr=3, theta=c, bounded=True, name="lam=eta=1/4")


def setup(sizes, slopes, b_top: float = 2.5, lid: float = math.log(20.0)):
    """Blocks, the top level and one middle level per rung; the nested cost bound."""
    (n1, n2, n3), (u1, u2, u3) = sizes, slopes
    if len({u1, u2, u3}) != 3:
        raise ValueError("three different slopes, so that every block is one site type of the whole")
    B = H.make_block([(u1, n1), (u2, n2), (u3, n3)])
    j1 = [i for i, (u, _) in enumerate(B) if u == u1][0]
    Dtop = H.HDesign(j=j1, k=n1, lam=1.0, eta=0.5, etap=1.0, b=b_top, Lr=4, theta=1.0, bounded=False, name="top")
    Ctop = H.constants(B, Dtop, lid)
    inner = Ctop.inner
    j2 = [i for i, (u, _) in enumerate(inner) if u == u2][0]
    mids = []
    for l in range(1, len(Ctop.xs)):
        D = middle_design(inner, j2, n2, Ctop.xs[l])
        C = H.constants(inner, D, Ctop.l_inv_delta_p)
        assert C is not None and C.x_out <= Ctop.xs[l] + 1e-9, (C.x_out if C else None, Ctop.xs[l])
        mids.append((D, C, lcmax(C, [n3 * LN2] * (len(C.xs) - 1))))
    return dict(B=B, Ctop=Ctop, mids=mids, Ttop=tables(n1, u1), Tmid=tables(n2, u2), lCmax=lcmax(Ctop, [m[2] for m in mids]))


def three_level_run(psi: np.ndarray, sizes, S: dict, rng) -> dict:
    """One end-to-end run on the table ``psi`` (site order: top outer block in the low bits, then the middle run's
    outer block, then the base block)."""
    n1, n2, n3 = sizes
    tab = psi.reshape(2 ** (n2 + n3), 2 ** n1).T                # tab[a, y]
    lA = float(np.logaddexp.reduce(-psi) - (n1 + n2 + n3) * LN2)
    stats = dict(mid_runs=0, mid_aborts=0, mid_invalid=0, mid_too_wide=0)

    def serve_top(a: int, l: int):
        fibre = tab[a]
        ftab = fibre.reshape(2 ** n3, 2 ** n2).T                # ftab[c, z]
        base = np.logaddexp.reduce(-ftab, axis=1) - n3 * LN2    # exact averages of the base fibres (the base procedure enumerates)
        D, C, _ = S["mids"][l - 1]
        r = run_level(float(fibre[0]), ftab[:, 0], n2, C, S["Tmid"], lambda c, _l: (float(base[c]), float(base[c]), 2 ** n3), rng)
        lw = float(np.logaddexp.reduce(base) - n2 * LN2)
        stats["mid_runs"] += 1
        if r["status"] != "closed":
            stats["mid_aborts"] += 1
        else:
            if not (r["lL"] <= lw + 1e-9 and lw <= r["lU"] + 1e-9):
                stats["mid_invalid"] += 1
            if r["lU"] - r["lL"] > C.x_out + 1e-9:
                stats["mid_too_wide"] += 1
        return r["lL"], r["lU"], r["q_real"]

    r = run_level(float(psi[0]), tab[:, 0], n1, S["Ctop"], S["Ttop"], serve_top, rng)
    out = dict(status=r["status"], valid=bool(r["lL"] <= lA + 1e-9 and lA <= r["lU"] + 1e-9), width=r["lU"] - r["lL"],
               lq_real=math.log(r["q_real"]), lq_thm=math.log(r["q_thm"]), level=r["level"], M=r["M"], nested_calls=r["nested_calls"], **stats)
    return out


CONFIGS = [  # (sizes (top outer, middle outer, base), slopes)
    ((7, 5, 3), (1.0, 0.5, 2.0)), ((7, 5, 3), (0.5, 2.0, 1.0)), ((8, 4, 3), (2.0, 1.0, 0.5)), ((6, 6, 3), (1.0, 2.0, 0.4))]
KINDS = ("flat", "cone", "cone0", "dip", "wells", "ridges", "linear", "mixed")


def task(args):
    ci, kind, runs, seed = args
    sizes, slopes = CONFIGS[ci]
    S = setup(sizes, slopes)
    us = np.array([slopes[0]] * sizes[0] + [slopes[1]] * sizes[1] + [slopes[2]] * sizes[2])
    rng = np.random.default_rng(seed)
    t0 = time.time()
    out = dict(config=ci, sizes=list(sizes), slopes=list(slopes), kind=kind, runs=0, closed=0, invalid=0, too_wide=0, aborted=0, over_budget=0,
               mid_runs=0, mid_aborts=0, mid_invalid=0, mid_too_wide=0, x_out=S["Ctop"].x_out, lCmax=S["lCmax"], max_lq_real=0.0, max_lq_thm=0.0,
               max_width=0.0, class_violation=-math.inf, seed=seed)
    for _ in range(runs):
        psi = hl.make_instance(kind, us, rng)
        out["class_violation"] = max(out["class_violation"], hl.check_class(psi, us))
        r = three_level_run(psi, sizes, S, rng)
        out["runs"] += 1
        for key in ("mid_runs", "mid_aborts", "mid_invalid", "mid_too_wide"):
            out[key] += r[key]
        if r["status"] != "closed":
            out["aborted"] += 1
        else:
            out["closed"] += 1
            out["invalid"] += not r["valid"]
            out["too_wide"] += r["width"] > S["Ctop"].x_out + 1e-9
            out["max_width"] = max(out["max_width"], r["width"])
        out["max_lq_real"] = max(out["max_lq_real"], r["lq_real"])
        out["max_lq_thm"] = max(out["max_lq_thm"], r["lq_thm"])
        out["over_budget"] += r["lq_thm"] > S["lCmax"] + 1e-9
    out["seconds"] = time.time() - t0
    return out


def tasks(job: str) -> list[dict]:
    """Task lists for ``modal_jobs/bench_app.py``."""
    out = []
    if job == "smoke":
        out.append(dict(tier="s", kwargs=dict(ci=0, kind="flat", runs=1, seed=1)))
    elif job == "nested1":
        for ci in range(len(CONFIGS)):
            for ki, kind in enumerate(KINDS):
                for rep in range(5):
                    out.append(dict(tier="m", kwargs=dict(ci=ci, kind=kind, runs=8, seed=100000 + 1000 * rep + 10 * ci + ki)))
    else:
        raise ValueError(job)
    for t_ in out:
        kw = t_["kwargs"]
        t_["id"] = "nested_literal:" + ",".join(f"{k}={kw[k]}" for k in sorted(kw))
    return out


def run_task(t_: dict) -> dict:
    kw = t_["kwargs"]
    return task((kw["ci"], kw["kind"], kw["runs"], kw["seed"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=6)
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    out = ROOT / "experiments" / "eng" / "twolevel" / "results" / "x011_nested_literal.jsonl"
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    todo = [(ci, kind, args.runs, 1000 * args.seed + 10 * ci + ki) for ci in range(len(CONFIGS)) for ki, kind in enumerate(KINDS)]
    with Pool(args.procs) as pool, out.open("a") as fh:
        for r in pool.imap_unordered(task, todo):
            r["commit"] = commit
            fh.write(json.dumps(r, default=float) + "\n")
            fh.flush()
            print(f"config {r['config']} {r['kind']:7s}: {r['runs']} runs, closed {r['closed']}, invalid {r['invalid']}, too wide {r['too_wide']}, aborted {r['aborted']}, "
                  f"over budget {r['over_budget']}; nested runs {r['mid_runs']} (aborted {r['mid_aborts']}, invalid {r['mid_invalid']}, too wide {r['mid_too_wide']}); "
                  f"max ln queries {r['max_lq_real']:.1f} (theorem's count {r['max_lq_thm']:.1f}, bound {r['lCmax']:.1f})  [{r['seconds']:.0f} s]", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
