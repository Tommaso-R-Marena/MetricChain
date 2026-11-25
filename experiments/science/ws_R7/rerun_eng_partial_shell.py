"""R7 control for X-005 that the engineering search did not run: instances whose outer level sets are NOT balls.

The engineering evaluator (src/metricchain_eng/twolevel at a2f6dc7; imported from the exported work tree argv[1]) accepts
any discrete law of W.  ENG-RES-0008 section 5 argues that radial profiles cover the whole class "up to partial shells",
and the search only ever evaluated radial laws on the full outer cube.  Here the same search (same decoder, same
differential evolution, same seeds) is run on CYLINDERS:

      g(a) = F( |a_{k+1..n_o}| ),      a in Q_{n_o},   F with slopes in [0, u]   (u-Lipschitz on Q_{n_o}),

whose level sets {x : |x_{k+1..n_o}| <= r} are not balls of Q_{n_o} for k >= 1 (for k = 1 they are initial segments of the
simplicial order: a ball plus a partial shell; for k >= 2 they are other u-Lipschitz landscapes of the class).
The law of W is the radial law of the (n_o - k)-cube.  Everything else (algorithm parameters, tables for n_o, oracle,
objective) is unchanged.  Output per cell: the largest ln(cost)/(n a) found for k = 0 (their family, re-run here), and for
k = 1, 2, 4, 8, ...; the stored worst case of the cell; the number of instances on which a claim of the theorem is violated.

   python3 rerun_eng_partial_shell.py <eng work tree> BUDGET u:n:phi [u:n:phi ...]
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.special import gammaln
W = Path(sys.argv[1]); sys.path.insert(0, str(W / "src")); sys.path.insert(0, str(W / "experiments/eng/twolevel"))
import run_search
from metricchain_eng.twolevel.adversary import Family, Search
from metricchain_eng.twolevel.ckernel import Evaluator
from metricchain_eng.twolevel.meanrun import Instance, Law
from metricchain_eng.twolevel.tables import LN2

class CylFamily(Family):
    kcyl = 0
    def instance(self, F, d0, c_in):
        if self.kcyl == 0:
            return super().instance(F, d0, c_in)
        P = self.ev.P
        m = P.n_o - self.kcyl
        j = np.arange(m + 1.0)
        lbinom = gammaln(m + 1.0) - gammaln(j + 1.0) - gammaln(m - j + 1.0)
        law = Law(c_in - np.asarray(F[:m + 1], dtype=float), lbinom - m * LN2)
        return Instance(law, psi0=float(F[min(d0, m)]), t0=P.u * P.n_i + c_in)

budget = int(sys.argv[2])
stored = [json.loads(l) for l in open(W / "experiments/eng/twolevel/results/x005_cost.jsonl")]
out = []
for arg in sys.argv[3:]:
    u, n, phi = arg.split(":"); u, n, phi = float(u), int(n), float(phi)
    P, rates = run_search.design_params(n, u, phi)
    ev = Evaluator(P)
    s = [r for r in stored if (r["u"], r["n"], r["phi"]) == (u, n, phi)][0]
    na = n * s["a"]
    stored_worst = max([s["flat"]["bottom"]["lcost"], s["flat"]["top"]["lcost"]] + [x["best_value"] for x in s["searches"]])
    rec = dict(u=u, n=n, phi=phi, n_o=P.n_o, stored_worst=stored_worst / na, lCmax=ev.lCmax / na, budget=budget, cyl={})
    for kc in (0, 1, 2, 4, 8, 16, 32):
        if kc >= P.n_o - 4: break
        best = -math.inf; viol = 0; nev = 0; worst_cap = -math.inf; t0 = time.time()
        for orc in ("bottom", "top"):
            fam = CylFamily(ev, k=8, monotone=True); fam.kcyl = kc
            S = Search(fam, orc, "cost")
            res = S.run(budget, seed=1)
            best = max(best, res.best_value); viol += len(res.violations); nev += res.n_eval
            worst_cap = max(worst_cap, res.extremes["cost_over_cap"])
        rec["cyl"][kc] = dict(worst=best / na, violations=viol, n_eval=nev, max_cost_minus_cap=worst_cap, seconds=round(time.time() - t0, 1))
        print(f"u={u} n={n} phi={phi} n_o={P.n_o}: cylinder k={kc:2d}: worst ln(cost)/(na) = {best / na:.4f}  (stored worst, radial: {stored_worst / na:.4f}; "
              f"C_max {ev.lCmax / na:.4f}); max ln cost - ln C_max = {worst_cap:.2f}; instances violating a claim: {viol} of {nev}", flush=True)
    out.append(rec)
    json.dump(out, open("out_rerun_eng_partial_shell.json", "w"), indent=1)
