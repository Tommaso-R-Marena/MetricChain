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

# ---------------- XI (certification geometry) ----------------
MUTS["XI"] = [
    ("XI.1 M1: slack without the residual terms (s = d)",
     [("    return d - g[:, None] + g[None, :]", "    return d + 0 * g[:, None]")], "XI.1"),
    ("XI.1 M2: claim N* <= N_cov (the extra evaluation of a minimiser dropped)",
     [("        if not (ncov <= nval <= nstar <= ncov + 1):", "        if not (ncov <= nval <= nstar <= ncov):")], "XI.1"),
    ("XI.2 M1: partition-function bound with the smallest slack partition sum (min over anchors)",
     [("/ float(np.max(np.sum(np.exp(-t * s), axis=1)))", "/ float(np.min(np.sum(np.exp(-t * s), axis=1)))")], "XI.2"),
    ("XI.2 M2: exponential-weights bound without the factor exp(-t eps)",
     [("            bound = math.exp(-t * eps) * float(v.sum()) / float(np.max(np.exp(-t * rho) @ v))",
       "            bound = float(v.sum()) / float(np.max(np.exp(-t * rho) @ v))"),
      ("                bound = math.exp(-t * eps) / float(np.max(np.exp(-t * rho) @ v))",
       "                bound = 1.0 / float(np.max(np.exp(-t * rho) @ v))")], "XI.2"),
    ("XI.3 M1: sharpness tested against half the envelope constant",
     [("        sharp = all(c[i] <= phi[i, a] - phi[i, ground[i]] + 1e-10", "        sharp = all(0.5 * c[i] <= phi[i, a] - phi[i, ground[i]] + 1e-10")], "XI.3"),
    ("XI.3 M2: product bound with the smallest single-site kernel sum (min over anchor states)",
     [("math.log(float(np.max(np.exp(-t * rho_site[i]) @ v)))", "math.log(float(np.min(np.exp(-t * rho_site[i]) @ v)))")], "XI.3"),
    ("XI.4 M1: no radius shrinkage (theta = (1-kappa)/(1+kappa))",
     [("        theta = (1 - kappa) / (4 * (1 + kappa))", "        theta = (1 - kappa) / (1 + kappa)")], "XI.4"),
    ("XI.4 M2: separation (c) claimed for the arbitrary first point as well",
     [("                if jj >= 1 and not gap[A[jj]] - gap[A[kk]] <= s[A[kk], A[jj]] + 1e-9:",
       "                if jj >= 0 and not gap[A[jj]] - gap[A[kk]] <= s[A[kk], A[jj]] + 1e-9:")], "XI.4"),
    ("XI.5 M1: claim 'gamma(G) evaluations' (the minimiser is forgotten)",
     [("        if nstar != gamma + 1:", "        if nstar != gamma:")], "XI.5"),
    ("XI.5 M2: no distinguished minimiser (f = 1 everywhere)",
     [("        f[nv] = 0.0\n        g = np.zeros(n)\n        gamma = None", "        f[nv] = 1.0\n        g = np.zeros(n)\n        gamma = None")], "XI.5"),
    ("XI.6 M1: conditional envelope without the original envelope (U(x) - L(y) only)",
     [("        D = np.minimum(d, U[:, None] - L[None, :])               # conditional envelope D_A(x, y)",
       "        D = U[:, None] - L[None, :]")], "XI.6"),
    ("XI.6 M2: conditional envelope transposed (U(y) - L(x))",
     [("        D = np.minimum(d, U[:, None] - L[None, :])               # conditional envelope D_A(x, y)",
       "        D = np.minimum(d, U[None, :] - L[:, None])")], "XI.6"),
    ("XI.6 M3: claim N_point <= N_conf",
     [("        if not (nconf <= npoint <= nconf + 1):", "        if not (nconf <= npoint <= nconf):")], "XI.6"),
    ("XI.7 M1: upper end with the transposed envelope d(x, y)",
     [("        hi = 1.0 / float(np.sum(np.exp(-beta * (f - f[x] + d[:, x]))))", "        hi = 1.0 / float(np.sum(np.exp(-beta * (f - f[x] + d[x, :]))))")], "XI.7"),
    ("XI.7 M2: interval claimed 1% narrower at the lower end",
     [("        lo = 1.0 / float(np.sum(np.exp(-beta * (f - f[x] - d[x, :]))))", "        lo = 1.01 / float(np.sum(np.exp(-beta * (f - f[x] - d[x, :]))))")], "XI.7"),
    ("XI.8 M1: entropy bound without the accuracy term t eps / beta",
     [("                    if H > math.log(size * B) + t * eps / beta + 1e-9:", "                    if H > math.log(size * B) + 1e-9:")], "XI.8"),
    ("XI.8 M2: Hoelder converse with the kernel exponent t = beta instead of beta (1 - p) / p",
     [("            t = beta * (1 - p) / p\n            v = rng.dirichlet", "            t = beta\n            v = rng.dirichlet")], "XI.8"),
    ("XI.8 M3: optimistic partition function written with the slack TO the evaluated set",
     [("                if abs(zhi - float(np.sum(pi * np.exp(beta * sA)))) > 1e-9 * zhi or \\",
       "                if abs(zhi - float(np.sum(pi * np.exp(beta * sAt)))) > 1e-9 * zhi or \\")], "XI.8"),
    ("XI.9 M1: relative entropy with its arguments exchanged",
     [("        kl = float(np.sum(nu * np.log(nu / mu)))", "        kl = float(np.sum(mu * np.log(mu / nu)))")], "XI.9"),
    ("XI.9 M2: transport cost with half the envelope",
     [("        W, _ = cg_transport(d, nu, mu)", "        W, _ = cg_transport(0.5 * d, nu, mu)")], "XI.9"),
    ("XI.10 M1: remainder claimed to be half as large",
     [("            if err > rem + 1e-9:\n                return False, dict(reason=\"anchored remainder bound violated\"",
       "            if err > 0.5 * rem + 1e-9:\n                return False, dict(reason=\"anchored remainder bound violated\"")], "XI.10"),
    ("XI.10 M2: interpolant one order too low (ball of radius m - 2)",
     [("                     for r in range(0, min(m - 1, len(S)) + 1) for T in itertools.combinations(S, r))",
       "                     for r in range(0, min(m - 2, len(S)) + 1) for T in itertools.combinations(S, r))")], "XI.10"),
    ("XI.11 M1: star envelope claimed with half the pair remainder",
     [("                if res.status != 0 or abs(sign * res.fun - (interp[y] - sign * rem)) > 1e-7:",
       "                if res.status != 0 or abs(sign * res.fun - (interp[y] - sign * 0.5 * rem)) > 1e-7:")], "XI.11"),
    ("XI.11 M2: certified-minimiser criterion with the additive interpolant only (remainder ignored)",
     [("            lower[y] = interp[y] - rem", "            lower[y] = interp[y]")], "XI.11"),
    ("XI.12 M1: cut bracket from one direction of the cut pairs only",
     [("                if i != j and ((i in S) != (j in S)):", "                if i < j and ((i in S) != (j in S)):")], "XI.12"),
    ("XI.12 M2: elimination of an end site without the factor on the reverse ordered pair",
     [("                T = np.array([sum(w[site][a] * W[site][j][a, b] * W[j][site][b, a] for a in range(k)) for b in range(k)])",
       "                T = np.array([sum(w[site][a] * W[site][j][a, b] for a in range(k)) for b in range(k)])")], "XI.12"),
    ("DEAD.7 M1: candidate restricted to evaluated points (the true statement II.4) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("                regret = np.max(DB + f[:, None] - f[None, :], axis=1)\n                if np.min(regret) > eps + 1e-12:\n                    continue                                       # not a configuration certificate",
       "                regret = np.where(np.isin(np.arange(n), B), np.max(DB + f[:, None] - f[None, :], axis=1), np.inf)\n                if np.min(regret) > eps + 1e-12:\n                    continue")], "DEAD.7"),
    ("XI.13 M1: tail bound claimed with exponent -8 N eta^2 / C",
     [("            bound = 2 * math.exp(-2 * N * eta ** 2 / C)", "            bound = 2 * math.exp(-8 * N * eta ** 2 / C)")], "XI.13"),
    ("XI.13 M2: sampled interval without the slack |beta| eta",
     [("                if not (-beta * mh - abs(beta) * eta <= L <= -beta * mh + abs(beta) * eta + beta ** 2 * C / 8):",
       "                if not (-beta * mh <= L <= -beta * mh + beta ** 2 * C / 8):")], "XI.13"),
    ("DEAD.9 M1: product reference with the same marginals (the true statement III.3) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    mu = law                                                      # the dependent reference under test",
       "    mu = law.sum(axis=1)[:, None] * law.sum(axis=0)[None, :]")], "DEAD.9"),
    ("DEAD.6 M1: comparison with covers at the shrunk radii (the true statement XI.4) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("        ncov = cg_min_cover(s <= (E - E.min())[None, :] + eps + 1e-12)\n        m = len(cg_best_first(d, f, g, eps, int(rng.integers(n))))",
       "        ncov = cg_min_cover(s <= (1 - kappa) / (4 * (1 + kappa)) * ((E - E.min())[None, :] + eps / 6) + 1e-12)\n        m = len(cg_best_first(d, f, g, eps, int(rng.integers(n))))"),
      ("    ncov = cg_min_cover(cg_slack(d, g) <= (f - f.min())[None, :] + 0.1 + 1e-12)",
       "    ncov = cg_min_cover(cg_slack(d, g) <= 0.25 * ((f - f.min())[None, :] + 0.1 / 6) + 1e-12)")], "DEAD.6"),
]

MUTS["XII"] = [
    ("XII.1 M1: dip built from the transposed envelope (d(y, a) instead of d(a, y))",
     [("    return np.minimum(g, g[y] - c + d[:, y])", "    return np.minimum(g, g[y] - c + d[y, :])")], "XII.1"),
    ("XII.1 M2: effect of a dip claimed to be at least beta c (soft gap dropped)",
     [("                if math.log(ratio) < beta * c - soft - 1e-9:", "                if math.log(ratio) < beta * c - 1e-9:")],
     "XII.1"),
    ("XII.2 M1: factor (1 - delta) instead of (1 - 2 delta)",
     [("        if (1 - 2 * delta) * pack > cost + 1e-7:\n            return False, dict(reason=\"expected evaluations below (1 - 2 delta) * packing\"",
       "        if (1 - delta) * pack > cost + 1e-7:\n            return False, dict(reason=\"expected evaluations below (1 - 2 delta) * packing\"")],
     "XII.2"),
    ("XII.2 M2: detection balls of half the radius (a larger packing is claimed)",
     [("        B = s < (gap[None, :] + epsp)                     # the detection relation claimed by the theorem",
       "        B = s < 0.5 * (gap[None, :] + epsp)")], "XII.2"),
    ("XII.3 M1: thermal detection radius without the soft gap",
     [("        c = (soft + eps) / beta + 1e-7                    # a depth with beta c > softgap + eps",
       "        c = eps / beta + 1e-7 + 0 * soft")], "XII.3"),
    ("XII.3 M2: thermal detection balls of half the radius in the packing",
     [("        B = s < c[None, :]                                # the detection relation claimed by the theorem",
       "        B = s < 0.5 * c[None, :]")], "XII.3"),
    ("XII.4 M1: closed balls of radius gap + eps instead of gap + eps/2",
     [("        balls = [np.array([s[a, y] <= gap[y] + eps / 2 + 1e-12 for a in range(n)]) for y in range(n)]",
       "        balls = [np.array([s[a, y] <= gap[y] + eps + 1e-12 for a in range(n)]) for y in range(n)]")], "XII.4"),
    ("XII.4 M2: the block of near-minimisers replaced by the whole space (upward alternatives ignored)",
     [("        p = min([float(q[b].sum()) for b in balls] + [float(q[nearmin].sum())])",
       "        p = min([float(q[b].sum()) for b in balls if b.sum() > 1] + [1.0])")], "XII.4"),
    ("XII.3 M3: factor (1 - delta) instead of (1 - 2 delta) on the uniform metric with blind guesses",
     [("        if (1 - 2 * delta_tight) * pack > cost_tight + 1e-7 or abs((1 - 2 * delta_tight) * pack - cost_tight) > 1e-7:",
       "        if (1 - delta_tight) * pack > cost_tight + 1e-7:")], "XII.3"),
    ("XII.5 M1: initial segments in binary order claimed to have the largest erosions (instead of the simplicial order)",
     [("        order = sorted(range(N), key=lambda v: (bin(v).count(\"1\"), tuple(i for i in range(n) if v >> i & 1)))",
       "        order = list(range(N))")], "XII.5"),
    ("XII.5 M2: sets one point larger than the ball claimed to have at most the effect of the ball",
     [("                sel = proper & (card <= size)", "                sel = proper & (card <= size + 1)")], "XII.5"),
    ("XII.7 M1: the set of eta-minimisers replaced by the whole space (upward alternatives ignored)",
     [("        p = min([float(q[b].sum()) for b in balls] + [float(q[nearmin].sum())])\n        for alt in range(12):\n            kind = alt % 4\n            if kind == 0:\n                y = int(rng.integers(n))\n                gp = qc_dip(d, g, y, gap[y] + eps - eta",
       "        p = min([float(q[b].sum()) for b in balls if b.sum() > 1] + [1.0])\n        for alt in range(12):\n            kind = alt % 4\n            if kind == 0:\n                y = int(rng.integers(n))\n                gp = qc_dip(d, g, y, gap[y] + eps - eta")],
     "XII.7"),
    ("XII.7 M2: hedged window with closed balls of radius gap + eps (the hedge eta dropped from the radius)",
     [("        balls = [np.array([s[a, y] <= gap[y] + eps - eta + 1e-12 for a in range(n)]) for y in range(n)]",
       "        balls = [np.array([s[a, y] <= gap[y] + eps + 1e-12 for a in range(n)]) for y in range(n)]")], "XII.7"),
    ("XII.7 M3: hedged mixtures with the factor (1 - delta)",
     [("        if (1 - 2 * delta) * pack > cost + 1e-7:\n            return False, dict(reason=\"hedged mixture:",
       "        if (1 - delta) * pack > cost + 1e-7:\n            return False, dict(reason=\"hedged mixture:")], "XII.7"),
    ("XII.7 M4: pairs claimed to be detected with probability 1 - delta",
     [("                    if detect < 1 - 2 * delta - 1e-9:", "                    if detect < 1 - delta - 1e-9:")], "XII.7"),
    ("XII.8 M1: the two radii of the bracket claimed to differ by at most 2 for every u",
     [("                steps = 1 + math.ceil((1.4587 if eps >= 2 else 1.3133) / u)", "                steps = 2")], "XII.8"),
    ("XII.8 M2: exponent formula without the volume regime (ln 2 - h((Lambda_1 - lam)/u) for every lam)",
     [("        pred = (math.log(2) - hb((lam1 - lam) / u)) if lam <= lam_c else min(lam, math.log(2))",
       "        pred = math.log(2) - hb((lam1 - lam) / u)")], "XII.8"),
    ("XII.6 M1: dip weights without the factor (1 + eta)",
     [("        W = w * ((1 + eta) * np.exp(Lam) - 1)", "        W = w * (np.exp(Lam) - 1)")], "XII.6"),
    ("XII.6 M2: soft gap computed from the transposed slack",
     [("math.log(float((w * np.exp(-beta * s[:, y])).sum())) for y in range(n)])\n        if np.any(Lam[:, None] > Lam[None, :] + beta * s.T + 1e-9):",
       "math.log(float((w * np.exp(-beta * s[y, :])).sum())) for y in range(n)])\n        if np.any(Lam[:, None] > Lam[None, :] + beta * s.T + 1e-9):")], "XII.6"),
    ("XII.6 M3: Gibbs weight of the difference set claimed to be at least 2 (Z - Z')",
     [("            if float(w[differs].sum()) < (Z - Zp) * (1 - 1e-9) - 1e-12:",
       "            if float(w[differs].sum()) < 2 * (Z - Zp) * (1 - 1e-9) - 1e-12:")], "XII.6"),
    ("DEAD.10 M1: accuracy eps = 0.5 instead of 0 (certificates then exist) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("            if width <= 1e-12:\n                found_proper = True", "            if width <= 0.5:\n                found_proper = True")],
     "DEAD.10"),
    ("DEAD.11 M1: known part f = 0 on the dyadic line (the shrunk covers are then small) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("        gap = X - X.min()\n        ncov = cg_min_cover(d <= gap[None, :] + eps)", "        gap = 0 * X\n        ncov = cg_min_cover(d <= gap[None, :] + eps)")],
     "DEAD.11"),
    ("DEAD.12 M1: two identical site types (per-site maximisation is then exact) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    _, _, rB = qc_site([0, 5.0], [0, 0], 10.0)", "    _, _, rB = qc_site([0, 0.5], [0, 0], 1.0)")], "DEAD.12"),
    ("DEAD.13 M1: the zero function in place of the class member that vanishes on the ball -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    ball_member = lambda x: -float(math.comb(sum(x) - 1, 2)) if sum(x) >= 1 else 0.0", "    ball_member = lambda x: 0.0")],
     "DEAD.13"),
    ("DEAD.15 M1: accuracy eps = 1 instead of 0 (the soft-gap bound is then attained up to a polynomial) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    eps = 0.0\n    n_small, u = 10, 1.0", "    eps = 1.0\n    n_small, u = 10, 1.0")], "DEAD.15"),
    ("DEAD.16 M1: low temperature u = 3.5 (above the crossover: single dips are then the hardest to hit) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    u, eps = 1.0, 1.0\n    dip8, _ = qc_flat_box_log_hit(1000, 8, 1, u, eps)", "    u, eps = 3.5, 1.0\n    dip8, _ = qc_flat_box_log_hit(1000, 8, 1, u, eps)")],
     "DEAD.16"),
    ("DEAD.14 M1: a deeper perturbation scale (beta = 3: single local dips are sensitive) -> must be flagged UNEXPECTEDLY SURVIVED",
     [("    n, beta, eps = 8, 1.0, 0.3\n    d = np.ones((n, n)) - np.eye(n)\n    blocks = []", "    n, beta, eps = 8, 3.0, 0.3\n    d = np.ones((n, n)) - np.eye(n)\n    blocks = []")],
     "DEAD.14"),
]

which = sys.argv[1:] or list(MUTS)
for key in which:
    for item in MUTS[key]:
        run(*item)
total = sum(RESULTS.values())
print(f"\n{total} mutations: {RESULTS['caught']} caught, {RESULTS['expected_pass']} expected pass, "
      f"{RESULTS['bad']} not as expected")
sys.exit(1 if RESULTS["bad"] else 0)
