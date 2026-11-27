# Harness block XVI: how often the Harper step is exercised — measurement and a proposed change (not applied)

Origin: the review SCI-REV-0007 of the Scientific Discovery Division, §3: "the mutation 'no Harper
term' is detected in 1 of 47 runs — most instances never exercise the step that distinguishes
11.56 from 11.52 at bounded accuracy; a harness should report how often it is exercised."  The
`1 of 47` is the division's own harness; this note is about ours.  Nothing below has been applied
to `experiments/falsify_conjectures.py` or `experiments/mutation_tests.py`.

## 1. What the step is

At a populated pass Algorithm 2L⁺ raises the running lower bound to
`ℓ := max{ℓ, s_je^{-b}p̲, s_je^{-b}·2^{-n_o}T_{n_o}(k)}`.  The third entry is the Harper term; without it
the algorithm is that of Theorem 11.52 with other constants.  The term is *active* at a pass
if it is the strict maximum.  It *decides the closure* of a run if the run stops at a populated
pass whose closure test `tail ≤ θe^bℓ` fails with the bound without the Harper term.  Step 5 of
the proof of Theorem 11.56 needs the term exactly at populated passes with closing radius
`r ≤ r†` at which `Γ̃(r)/c_η > θ ≥ Γ″(r)` — condition [P] holds through `Γ″` only (the statistic the
review asks for).  Without the term such a level is left, and the check "every level that is
left has closing radius above `r†`" fails: this is how the mutation `XVI.3 M5` is caught.

## 2. Measurement on the harness as committed (`h_harper_usage.py` → `out_h_harper_usage.txt`)

The committed text of the harness is loaded unchanged except for a record of the bound without
the Harper term and a switch that removes the term; tests XVI.3 and XVI.4 are run as the harness
runs them (seed `20261124`; `60` trials in quick mode, `400` in full mode); every run is repeated
from the same generator state without the term.

| test, mode | runs | populated passes | term active: passes (runs) | closure decided by the term | [P] through `Γ″` only: passes (runs) | without the term: trajectory changes | without the term: a claim is violated |
|---|---|---|---|---|---|---|---|
| XVI.3, quick | `9` | `413` | `51` (`7`) | `1` | `1` (`1`) | `5` | `1` |
| XVI.3, full | `46` | `1357` | `150` (`34`) | `2` | `6` (`6`) | `22` | `3` |
| XVI.4, quick | `79` | `1978` | `327` (`57`) | `1` | `8` (`8`) | `24` | `5` |
| XVI.4, full | `129` | `3045` | `512` (`96`) | `1` | `13` (`13`) | `50` | `9` |

So the review's remark holds for our harness as well.  The term is active in most runs, but it
decides something a check can see in few: in quick mode — the mode of the mutation runner — the
mutation `XVI.3 M5` ("no Harper term in the running lower bound") is caught through exactly one
of nine runs, an arbitrary Lipschitz function on `Q_6 × Q_4` that happens to be drawn with seed
`20261124`.  The violated claim is always the same: a level left with closing radius at most
`r†`.  The harness reports none of this; its power condition asks only for populated and
unpopulated levels.

## 3. Proposal

(a) **A statistic.**  The record of a pass keeps the bound without the Harper term and the
tail; the check of a run adds two counters to the statistics that the test returns and the
harness prints: `harper_active` (populated passes at which the term raises the running bound)
and `harper_decisive` (runs whose closure the term decides).

(b) **A fixed sub-case in XVI.3.**  Outer landscape "plateau of radius `4`, then a cone of slope
`u`" on `Q_24` (`n = 26`), `u = ½`, `λ = ½`, `η = ¼`, `η′ = ½`, `θ = 2`, `b = ½`, `ν₁ = 1`, inner behaviours
"value at the top" and "value at the bottom".  The closing pass is populated, its radius is at
most `r†`, and [P] holds there through `Γ″` only.  Over `1000` seeds and the three inner behaviours
(`h_subcase_robust.py` → `out_h_subcase_robust.txt`): the term decides the closure in `3000` of
`3000` runs, and without the term the check of the closing radius fails in `3000` of `3000`.  The
sub-case costs a few hundredths of a second.

(c) **A power condition.**  The test fails with "the fixed sub-case no longer exercises the
Harper step" unless both runs of the sub-case are decided by the term, and with "the test has
no power" if the term was never active.

With (a)–(c) the mutation `XVI.3 M5` no longer depends on which random instances a seed
produces.  No change of `experiments/mutation_tests.py` is needed: the patterns of `XVI.3 M1`–`M6`
and `XVI.4 M1`–`M3` still occur exactly as before.  If the change is applied, the two patterns
`OLD1`, `OLD2` at the head of `h_harper_usage.py` must be updated, or that script retired.

## 4. The change as text (unified diff against the committed harness; `out_h_proposal.diff`)

Below the hunks are named by their functions.  The file `out_h_proposal.diff` has the same hunks
with the line numbers of the harness at commit `24a3c27` (block XVI starts near line `6000` there);
the harness grows at every checkpoint, so the line numbers will be stale and the four exact
strings in `h_proposal_test.py` are what to apply.

```diff
--- experiments/falsify_conjectures.py
+++ experiments/falsify_conjectures.py (proposed)
@@ def ba_two_level_plus(rng, vals, probs, lnw_ref, n_o, n, u, par, mode, max_points=4_200_000):
                 while ball[k + 2] <= max(1.0, No * pbar):
                     k += 1
+                ell_markov = max(ell, s * math.exp(-b) * pbar)                               # the bound without the Harper term (statistics only)
                 ell = max(ell, s * math.exp(-b) * pbar, s * math.exp(-b) * Tk[k] / No)       # Markov, and the Harper term
             if No * q < 1:
@@
                 r = next(rr for rr in range(n_o + 1) if ball[rr + 1] >= No * q)
                 tail = s * E[r] / No if r < n_o else math.inf         # no closure while the ball is the whole cube
-            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg)
+            rec = dict(s=s, M=M, q=q, pbar=pbar, pop=pop, ell_in=ell_in, r=r, Mneg=Mneg, tail=tail, ell_out=ell,
+                       ell_markov=(ell_markov if pop else ell))
             if tail <= theta * math.exp(b) * ell:
                 lower = max(ell, Sigma + (1 - math.exp(-lam)) * math.exp(-b) * s * pbar)
@@ def ba_check_run(run, vals, probs, n_o, n, u, par, stats):
             stats["tightest_count"] = max(stats["tightest_count"], lhs / cap)
         stats["populated" if lv["pop"] else "unpopulated"] += 1
+    # how often the Harper term is exercised (a question of the Scientific Discovery Division, SCI-REV-0007): populated passes
+    # at which it raises the running bound, and runs whose closure it decides (the closing pass is populated and would fail
+    # the closure test with the bound without the Harper term)
+    seq, last = run["levels"] + [run["last"]], run["last"]
+    stats["harper_active"] = stats.get("harper_active", 0) + sum(1 for lv in seq if lv["pop"] and lv["ell_out"] > lv["ell_markov"])
+    stats["harper_decisive"] = stats.get("harper_decisive", 0) + int(last["pop"] and last["tail"] > theta * math.exp(b) * last["ell_markov"])
     stats["runs"] += 1
     return None
@@ def t_two_level_plus(rng, trials):
         if bad:
             return False, bad
-    if stats["populated"] == 0 or stats["unpopulated"] == 0 or stats["skipped"] > 0:
+    # (iii) a fixed sub-case in which the Harper term decides the closure (plateau of radius 4, then a cone of slope u): the
+    # closing pass is populated, its radius is at most r_dagger, and the closure test holds through the Harper term only --
+    # without that term the level is left and the check of the closing radius fails.  (3000 of 3000 runs over seeds and
+    # inner behaviours: experiments/coordinator_checks/nested_review_R6/h_subcase_robust.py)
+    n_o, u = 24, 0.5
+    f = u * np.maximum(np.arange(n_o + 1, dtype=float) - 4, 0.0)
+    vals, probs = np.exp(-f), np.array([math.comb(n_o, j) for j in range(n_o + 1)], dtype=float) / 2 ** n_o
+    decisive_before = stats.get("harper_decisive", 0)
+    for mode in (1, 2):
+        bad = one(vals, probs, 0.0, n_o, n_o + 2, u, dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0), mode, ("harper", mode))
+        if bad:
+            return False, bad
+    if stats.get("harper_decisive", 0) - decisive_before != 2:
+        return False, dict(reason="the fixed sub-case no longer exercises the Harper step", **stats)
+    if stats["populated"] == 0 or stats["unpopulated"] == 0 or stats["skipped"] > 0 or stats.get("harper_active", 0) == 0:
         return False, dict(reason="the test has no power", **stats)
     return True, stats
```

The exact old and new strings (four replacements, each old string occurs once) are the list
`EDITS` of `h_proposal_test.py`.

## 5. Test of the proposal on a copy (`h_proposal_test.py` → `out_h_proposal_test.txt`)

The four replacements were applied to a copy of the harness at commit `24a3c27`, and before that
to a copy of the harness at `b2d3e9c` (other tests were added in between; block XVI is the same,
and so is every line of the result below).  On the patched copy:

| run | result |
|---|---|
| `--only XVI.3 --quick` | survived; `runs=11`, `harper_active=64`, `harper_decisive=3` |
| `--only XVI.3` (full) | survived; `runs=48`, `harper_active=163`, `harper_decisive=4` |
| `--only XVI.4 --quick` | survived, unchanged (`runs=79`) |
| mutations `XVI.3 M1`–`M6`, `XVI.4 M1`–`M3`, applied to the patched copy, quick mode | `9` of `9` caught (exit code `1`, no test in ERROR) |

## 6. What the proposal does not do

It measures the *presence* of the Harper term, not the correctness of its radius.  A Harper
term with one shell too many (`T_{n_o}(k+1)` in place of `T_{n_o}(k)`) is **not** caught by XVI.3, with
or without the proposal (last line of `out_h_proposal_test.txt`): the certified fraction `p̲` is
below the true one by the factor `1 + η`, so on radial landscapes `k + 1` is still at most the true
radius and the bound stays true.  A test of the radius needs level sets with partial shells
(non-radial landscapes larger than `Q_6 × Q_4`); none is proposed here.

The workstream's own scripts have the same property in a milder form: `sim_outer_loop.py`
catches "no Harper term" in `11` of `142` runs and `sim_grouped.py` in `27` of `191`
(`K_REPORT.md` §6.2, §6.8); neither reports how often the term decides a closure.
