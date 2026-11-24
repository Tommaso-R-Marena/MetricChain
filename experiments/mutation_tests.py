#!/usr/bin/env python3
"""Mutation testing of the falsification harness.

A test that cannot fail proves nothing.  Each mutation below is a small textual change to a scratch
COPY of `experiments/falsify_conjectures.py` (the repository file is never modified) that makes one
tested claim false, or breaks the test's own modelling of the claim; the affected test is then run
in quick mode.  A mutation is *caught* when the harness reports a misbehaving test (exit code 1).

Exactly one mutation is expected to pass: `DEAD.5 M2` restricts the search for a counterexample to
product references, where none exists, so the test must fall back to its explicit two-site
counterexample and still behave as documented.

The run fails (exit code 1) if a mutation is not caught, if the expected pass does not pass, or if a
mutation pattern no longer occurs in the harness (the mutation list is then stale and must be
updated together with the test).

Usage:
    python3 experiments/mutation_tests.py            # all groups
    python3 experiments/mutation_tests.py X1 II4     # selected groups
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "falsify_conjectures.py")
base = open(SRC).read()
TMP = tempfile.mkdtemp(prefix="metricchain-mutants-")
EXPECTED_PASS = ("DEAD.5 M2",)
RESULTS = dict(caught=0, expected_pass=0, bad=0)


def run(label, edits, only, extra=("--quick",)):
    s = base
    for old, new in edits:
        if s.count(old) < 1:
            print(f"!! {label}: STALE MUTATION, pattern not found: {old[:70]!r}")
            RESULTS["bad"] += 1
            return
        s = s.replace(old, new)
    path = os.path.join(TMP, "mutant.py")
    with open(path, "w") as fh:
        fh.write(s)
    out = subprocess.run([sys.executable, path, "--only", only, *extra], capture_output=True, text=True)
    verdict = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "(no output)"
    want_pass = label.startswith(EXPECTED_PASS)
    ok = (out.returncode == 0) if want_pass else (out.returncode == 1)
    status = ("expected pass" if want_pass else "caught") if ok else "NOT AS EXPECTED"
    print(f"[{status:>15}] {label}\n                  exit={out.returncode}  {verdict}")
    if not ok:
        RESULTS["bad"] += 1
        print(out.stdout[-1200:])
        print(out.stderr[-600:])
    elif want_pass:
        RESULTS["expected_pass"] += 1
    else:
        RESULTS["caught"] += 1


MUTS = {}

# ---------------- X.1 ----------------
MUTS["X1"] = [
    ("X.1 M1: valid envelope replaced by the invalid offset kappa/(4d) (pointwise hypothesis check active)",
     [('valid = [("offset kappa/d", _voxel_const_envelopes(amp, freq, kappa / d)),',
       'valid = [("offset kappa/d", _voxel_const_envelopes(amp, freq, kappa / (4 * d))),')], "X.1 Sep"),
    ("X.1 M1b: same, with the pointwise hypothesis check disabled (only the integral comparison can catch it)",
     [('valid = [("offset kappa/d", _voxel_const_envelopes(amp, freq, kappa / d)),',
       'valid = [("offset kappa/d", _voxel_const_envelopes(amp, freq, kappa / (4 * d))),'),
      ("            if not hypothesis_holds(phis, psis):", "            if False:")], "X.1 Sep"),
    ("X.1 M2: Taylor envelope without Hessian enclosure used as 'valid', pointwise check disabled",
     [('_voxel_taylor_envelopes(lo, hi, amp, freq, kappa, taylor_mode))]', '_voxel_taylor_envelopes(lo, hi, amp, freq, kappa, "centre"))]'),
      ("            if not hypothesis_holds(phis, psis):", "            if False:")], "X.1 Sep"),
    ("X.1 M3: Gershgorin off-diagonal radius dropped from the Hessian enclosure (pointwise check active)",
     [("        m[i] = min(-s * a, -s * b) + min(-kappa * pmin, -kappa * pmax) - radius\n        M[i] = max(-s * a, -s * b) + max(-kappa * pmin, -kappa * pmax) + radius",
       "        m[i] = min(-s * a, -s * b) + min(-kappa * pmin, -kappa * pmax)\n        M[i] = max(-s * a, -s * b) + max(-kappa * pmin, -kappa * pmax)")], "X.1 Sep"),
    ("X.1 M4: claimed ratio bound with half the width (exp(beta*sum w/2))",
     [("if upper > math.exp(beta * float(np.sum(w))) * lower2 * (1 + rel + rl2):", "if upper > math.exp(0.5 * beta * float(np.sum(w))) * lower2 * (1 + rel + rl2):")], "X.1 Sep"),
    ("X.1 M4b: Taylor width w_i reported 1% too small (ratio bound must fail on a second-order envelope)",
     [("    return phis, psis, 0.5 * (M - m) * r ** 2", "    return phis, psis, 0.99 * 0.5 * (M - m) * r ** 2")], "X.1 Sep"),
    ("X.1 M5: lower and upper envelopes swapped in the sandwich",
     [("            lower, rl = _envelope_product(psis, lo, hi, beta)\n            upper, ru = _envelope_product(phis, lo, hi, beta)",
       "            lower, rl = _envelope_product(phis, lo, hi, beta)\n            upper, ru = _envelope_product(psis, lo, hi, beta)")], "X.1 Sep"),
    ("X.1 M6: 'Fubini' broken: envelope integrals multiplied by 1 + 1e-8 (tiny relative error in one factor)",
     [("        prod *= v\n        rel += e / v", "        prod *= v * (1 + 1e-8 if i == 0 else 1)\n        rel += e / v")], "X.1 Sep"),
]

# ---------------- II.4 ----------------
MUTS["II4"] = [
    ("II.4 M1: threshold (1-kappa) sigma + eps (sign of eps flipped)",
     [("def forced_sets(kap, gap, sig, eps_sign=-1.0):", "def forced_sets(kap, gap, sig, eps_sign=+1.0):")], "II.4 Wit"),
    ("II.4 M2: threshold sigma - eps (kappa replaced by 0)",
     [("                thr = (1.0 - kap) * sig + eps_sign * eps                 # sig = inf (A = {y}): any sigma works",
       "                thr = 1.0 * sig + eps_sign * eps")], "II.4 Wit"),
    ("II.4 M3: threshold (1-kappa) sigma - eps/2",
     [("                thr = (1.0 - kap) * sig + eps_sign * eps                 # sig = inf (A = {y}): any sigma works",
       "                thr = (1.0 - kap) * sig + 0.5 * eps_sign * eps")], "II.4 Wit"),
    ("II.4 M4: threshold (1-kappa/2) sigma - eps",
     [("                thr = (1.0 - kap) * sig + eps_sign * eps                 # sig = inf (A = {y}): any sigma works",
       "                thr = (1.0 - 0.5 * kap) * sig + eps_sign * eps")], "II.4 Wit"),
    ("II.4 M5: certificate only required at non-anchor... replaced by: lower bound checked at anchors only",
     [("        valid = U - eps <= (f[None, :] + lowenv).min(axis=1) + 1e-12     # eps-certificate, all y",
       "        valid = U - eps <= np.where(Mk, f[None, :] + lowenv, np.inf).min(axis=1) + 1e-12")], "II.4 Wit"),
    ("II.4 M6: separation taken as the LARGEST distance to another anchor",
     [("        sigma = np.where(Mk[:, :, None], np.where(off, D, np.inf)[None, :, :], np.inf).min(axis=1)",
       "        sigma = np.where(Mk[:, :, None], np.where(off, D, -np.inf)[None, :, :], -np.inf).max(axis=1)")], "II.4 Wit"),
]

# ---------------- VII.1 ----------------
MUTS["VII1"] = [
    ("VII.1 M1: unsound elimination rule in the tables and the joint search (margin >= -2 accepted)",
     [("prune[state, i, r] = state[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(state)) >= -1e-9",
       "prune[state, i, r] = state[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(state)) >= -2 - 1e-9"),
      ("                        if goldstein(h, J, i, r, 1 - r, _box(dom)) >= -1e-9:",
       "                        if goldstein(h, J, i, r, 1 - r, _box(dom)) >= -2 - 1e-9:"),
      ("                joint_ok = dom[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(dom)) >= -1e-9",
       "                joint_ok = dom[i] == 2 and goldstein(h, J, i, r, 1 - r, _box(dom)) >= -2 - 1e-9")], "VII.1"),
    ("VII.1 M2: leaf bound = exact minimum instead of the LP bound (integrality gap ignored) in the block tables",
     [("        leaf[state] = leaf_rule_best_bound(h, J, _box(state))", "        leaf[state] = max(1.0, leaf_rule_best_bound(h, J, _box(state)))")], "VII.1"),
    ("VII.1 M2b: leaf rule mis-modelled: pair constraint with p_ij instead of 2 p_ij (bound doubles on pairs)",
     [("                row[P(i, j)] = 2.0", "                row[P(i, j)] = 1.0")], "VII.1"),
    ("VII.1 M2c: leaf = exact minimum in tables AND validation switched off (only the search result can catch it)",
     [("        leaf[state] = leaf_rule_best_bound(h, J, _box(state))", "        leaf[state] = max(1.0, leaf_rule_best_bound(h, J, _box(state)))"),
      ("        if abs(lp_primal - lp_blocks) > 1e-7 or abs(lp_kernel - lp_blocks) > 1e-7:", "        if False:")], "VII.1"),
    ("VII.1 M3: branch charges only the cheaper child (block search)",
     [("                    best = min(best, rec(kids[0]) + rec(kids[1]))\n                    if use_prune:\n                        for r in range(2):\n                            if unsound_prune or prune[s, i, r]:",
       "                    best = min(best, min(rec(kids[0]), rec(kids[1])))\n                    if use_prune:\n                        for r in range(2):\n                            if unsound_prune or prune[s, i, r]:")], "VII.1"),
    ("VII.1 M4: prune rule only wrong in the joint search (margin >= -2): joint ground truth must disagree",
     [("                        if goldstein(h, J, i, r, 1 - r, _box(dom)) >= -1e-9:",
       "                        if goldstein(h, J, i, r, 1 - r, _box(dom)) >= -2 - 1e-9:")], "VII.1"),
    ("VII.1 M5: claim 'at least 2^(K+1) leaves' (too strong)",
     [("                if got != 2 ** K:", "                if got != 2 ** (K + 1):")], "VII.1"),
]

# ---------------- II.7 ----------------
MUTS["II7"] = [
    ("II.7 M1: Consistent without the clause c_i >= 0",
     [("        consistent = bool(np.all(c >= 0)) and all(vp - vq <= weighted_hamming(c, ap, aq)",
       "        consistent = True and all(vp - vq <= weighted_hamming(c, ap, aq)")], "II.7"),
    ("II.7 M2: pair condition checked in one direction only (p before q in the list)",
     [("                                                    for ap, vp in anchors for aq, vq in anchors)\n        # the class as a linear",
       "                                                    for ip, (ap, vp) in enumerate(anchors) for aq, vq in anchors[ip:])\n        # the class as a linear")], "II.7"),
    ("II.7 M3: pair condition with the absolute value of the envelope constants",
     [("        consistent = bool(np.all(c >= 0)) and all(vp - vq <= weighted_hamming(c, ap, aq)",
       "        consistent = all(vp - vq <= weighted_hamming(np.abs(c), ap, aq)")], "II.7"),
    ("II.7 M4: pair condition with a strict inequality",
     [("        consistent = bool(np.all(c >= 0)) and all(vp - vq <= weighted_hamming(c, ap, aq)",
       "        consistent = bool(np.all(c >= 0)) and all((ap, vp) == (aq, vq) or vp - vq < weighted_hamming(c, ap, aq)")], "II.7"),
]

# ---------------- II.8 ----------------
MUTS["II8"] = [
    ("II.8 M1: upper envelope with twice the envelope (not admissible)",
     [("        hi = (g[A][:, None] + D[A, :]).min(axis=0)\n        S = ", "        hi = (g[A][:, None] + 2 * D[A, :]).min(axis=0)\n        S = ")], "II.8"),
    ("II.8 M2: targets up to 1% beyond the upper end of the interval",
     [("        t_lo, t_hi = fmin(0.0), fmin(1.0)", "        t_lo, t_hi = fmin(0.0), fmin(1.0) + 0.01")], "II.8"),
    ("II.8 M3: interpolation that is not a convex combination (pointwise max of the envelopes scaled)",
     [("            return (1.0 - lam) * lo + lam * hi", "            return lo + lam * (hi - lo) * (1.0 + 0.5 * np.sin(7.0 * np.arange(len(lo))) * lam * (1 - lam))")], "II.8"),
    ("II.8 M4: partition-function interval claimed 2% wider",
     [("        z_lo, z_hi = zfun(1.0), zfun(0.0)", "        z_lo, z_hi = zfun(1.0), zfun(0.0) * 1.02")], "II.8"),
]

# ---------------- III.6 / DEAD.5 ----------------
MUTS["III6"] = [
    ("III.6 M1: bound with sum of squares (the DEAD.5 claim)",
     [("        ub = beta ** 2 * float(np.sum(c)) ** 2 / 8\n        if val < -1e-10 or val > ub * (1 + 1e-9) + 1e-12:\n            return False, dict(val=val, ub=ub, n=n, k=k, beta=beta, reference=kind)",
       "        ub = beta ** 2 * float(np.sum(c ** 2)) / 8\n        if val < -1e-10 or val > ub * (1 + 1e-9) + 1e-12:\n            return False, dict(val=val, ub=ub, n=n, k=k, beta=beta, reference=kind)")], "III.6"),
    ("III.6 M2: constant 1/8 replaced by 1/8.1",
     [("        ub = beta ** 2 * float(np.sum(c)) ** 2 / 8\n        if val < -1e-10 or val > ub * (1 + 1e-9) + 1e-12:\n            return False, dict(val=val, ub=ub, n=n, k=k, beta=beta, reference=kind)",
       "        ub = beta ** 2 * float(np.sum(c)) ** 2 / 8.1\n        if val < -1e-10 or val > ub * (1 + 1e-9) + 1e-12:\n            return False, dict(val=val, ub=ub, n=n, k=k, beta=beta, reference=kind)")], "III.6"),
    ("DEAD.5 M1: the surviving bound (sum c_i)^2 registered as a dead end -> must be flagged UNEXPECTEDLY SURVIVED",
     [("        rhs = beta ** 2 * float(np.sum(c ** 2)) / 8\n        lhs = log_mgf_centered(w, g, beta)",
       "        rhs = beta ** 2 * float(np.sum(c)) ** 2 / 8\n        lhs = log_mgf_centered(w, g, beta)"),
      ("    rhs = float(np.sum(c ** 2)) / 8                                          # = 0.25",
       "    rhs = float(np.sum(c)) ** 2 / 8")], "DEAD.5"),
    ("DEAD.5 M2: product references only (independent sites) -> random search must find nothing, fallback fires",
     [('        configs, w, kind = correlated_reference(rng, n, k, kinds=("gibbs", "markov"))\n        g, c = random_bd_function(rng, configs, n, k)\n        beta = float(rng.uniform(0.05, 4.0))',
       '        _, configs, wd = product_space(rng, n, k)\n        w, kind = np.array([wd[x] for x in configs]), "product"\n        g, c = random_bd_function(rng, configs, n, k)\n        beta = float(rng.uniform(0.05, 4.0))')], "DEAD.5"),
]

# ---------------- I.6 / VII.2 ----------------
MUTS["I6"] = [
    ("I.6 M1: injective transport formula used for a many-to-one map (factor m dropped)",
     [("        bound = m * math.exp(-beta * gamma) * ZS", "        bound = math.exp(-beta * gamma) * ZS")], "I.6 Many"),
]
MUTS["VII2"] = [
    ("VII.2 M1: description length of the peeling certificate claimed to be at most 100 m^3",
     [("        if ds > 147 * m ** 3:", "        if ds > 100 * m ** 3:")], "VII.2"),
    ("VII.2 M2: sum nodes not charged for the sub-instances they embed (closed form must disagree)",
     [("            return 1 + 2 * (n * k + n * n * k * k) + data_size(node[1], n, k) + data_size(node[2], n, k)",
       "            return 1 + data_size(node[1], n, k) + data_size(node[2], n, k)")], "VII.2"),
]

which = sys.argv[1:] or list(MUTS)
for key in which:
    for item in MUTS[key]:
        run(*item)
total = sum(RESULTS.values())
print(f"\n{total} mutations: {RESULTS['caught']} caught, {RESULTS['expected_pass']} expected pass, "
      f"{RESULTS['bad']} not as expected")
sys.exit(1 if RESULTS["bad"] else 0)
