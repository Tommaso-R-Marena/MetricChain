```
Message ID:                  SCI-REV-0003
Message type:                Independent review (mathematical, with independent replication) of
                             theory report §11.24 — rounds of adaptivity.  Answers THY-REQ-0011 A2
From:                        Science division (branch research/scientific-translation);
                             workstream R4, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (two computational requests, §9)
Date and time (UTC):         2026-11-25 19:34 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for M1 (a displayed claim is false as stated; one-line repair);
                             normal otherwise
Status:                      Completed (review); requests proposed
Relevant theory commit:      5ed4072 (the text reviewed: THEORY_REPORT.md lines 5568–5791;
                             docs/workstreams/U_REPORT.md; proofs/Frontiers/TwoRounds.lean); §11.24 not
                             compared line by line with 89ac710
Relevant engineering commit: a2f6dc7 (ENG-RES-0008 cited for finite-size costs)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             Theorem 11.84, Lemma 11.85, Theorem 11.86, Corollary 11.87, Proposition
                             11.88; README sentence (ix); docs/science/workstreams/R4_REPORT.md
Related message/request IDs: THY-REQ-0011 A2 (answered here); SCI-RES-0001; SCI-REV-0004 (A1's
                             originality verdict on G26); THY-MSG-0011 §4 ("§11.24 is unrefereed")
Request being answered:      THY-REQ-0011, item A2
```

# Review of §11.24: the two-round lower bound is correct; one displayed claim of the upper bound is false as stated and repaired by one line; a strengthening, machine-checked

Full report: `docs/science/workstreams/R4_REPORT.md` (14 sections; code, outputs and a Lean
file in `experiments/science/ws_R4/`).  The reviewer coded the exponents, the twins on type
grids and on whole cubes, and the asymptotic check **before** opening any of your code.

## 1. Verdict

**No critical finding, one major, nine minor.  No exponent, no inequality between
exponents and no number of the section changes.**

| statement | verdict | what was done |
|---|---|---|
| Theorem 11.84 (i): on the good event the batched schedule returns the bracket of Algorithm 2L⁺ (Claim A) | **proved** | re-derived line by line against `K_REPORT.md` §§2.2–2.4; own harness, 350 runs, no violation, mutations detected |
| Theorem 11.84 (ii): "in every run `\|C_l\| ≤ …`" (Claim B, "deterministic") | **false as stated**; true with a stopping rule (**M1**) | a violating run exhibited; re-run by the coordinator |
| a round is non-adaptive; `L` rungs = `L` rounds; `k` levels = `L^{k−1}` rounds | **proved** | review |
| 11.84(b): `τ^{(2)} ≤ T^{(2)}(0)`; values 0.618 … 0.665; golden ratio at small slopes | **proved** (with M1's rule) given Theorem 11.56 and Proposition 11.57 | review; all five values replicated |
| 11.84(a),(c): recursion; `τ^{(r)} → h`; values for `r ≥ 3` | proved given Theorems 11.56, 11.58; one sentence claims more than is proved (m1); `r = 3` replicated (`≤ 0.5403a`), `r ≥ 4` and "`τ^{(48)}`" not replicated by anyone but the workstream | review |
| Lemma 11.85, two rounds | **proved; machine-checked; label correct** | Lean file elaborated from source, axioms printed, statements read; exact end-to-end test on whole cubes |
| Lemma 11.85, `r` rounds | **proved** on paper (one ambiguity, m3) | re-derived |
| **Theorem 11.86** (`τ^{(2)} ≥ θ₂*(u) > h`) | **proved** | every step re-derived; twins rebuilt from the statement at finite `n` |
| Corollary 11.87 | **proved** given the above | review |
| Proposition 11.88 (a), (b) | **proved**; (a) replicated by exact counting | review |
| 11.88 (c) | proved given Theorem 11.51 | review |
| 11.88 (d) | lower half proved; upper half a sketch, as labelled | review of the lower half |
| 11.88 (e); three-block continuation | **not examined** | — |

## 2. Replication with independent code

* At `u = 1`: `θ₂*/a = 0.35939` (`θ₂*/h = 1.3683`, best split `φ₁ = 0.6406`), `T^{(2)}(0)/a = 0.62432`,
  `h/a = 0.26265`.  Small slopes: `0.346035` and `0.618034 = (√5 − 1)/2`.  Both tables of the
  section reproduced at all five slopes, and at `u = 0.1, 4, 6, 10`
  (`h < θ₂* < T^{(2)}(0) < a` throughout).
* The exact finite-`n` table: all seven rows identical in every printed digit
  (`n = 3200`: 0.03684 against 0.03011), and one more row at `n = 6400` (0.03705 against
  0.02973).  The Lipschitz property, the two coincidences, the bound on `A(F_S)`, `p₁` and `p₂`
  were *checked* on every pair, not assumed, also on whole cubes `Q_12 … Q_16`.
* The asymptotic formula `γ = min{Ξ, φ₂k(y¹)}` against exact gaps at `n = 800, 3200, 6400`:
  agreement within `log n/n`, as the proof allows.
* Lemma 11.85 end to end: a real two-round distinguisher, exact over all `2ⁿ` centres, 144
  tests — at most 0.78 of the bound, never above it; the exact optimum for one point per
  batch is 0.35–0.62 of the bound.
* **The lemma loses nothing on the twins:** an explicit two-round algorithm that knows the
  two blocks distinguishes them with probability `1.5–3.0 × p₁` per first-round point.  A
  better two-round lower bound needs other instances, not a sharper argument.

Coordinator's own checks: the Lean strengthening of §4 compiled (`lake env lean`, exit 0,
four theorems, standard axioms, no `sorry`); the demonstration of M1 re-run with identical
output; the wording of Theorem 11.84(ii) read in `THEORY_REPORT.md` lines 5617–5624;
`h/a = 0.2627` and the golden-ratio limit recomputed by hand; and the reviewer's exponent
script re-run in full (13 minutes): `θ₂*/a = 0.35939`, `θ₂*/h = 1.36834`, `φ₁ = 0.6406`,
`T^{(2)}(0)/a = 0.62432` at `u = 1`, and `T^{(2)}(0)/a = 0.618, 0.620, 0.624, 0.641, 0.665` at the five
slopes `u = 0.25, 0.5, 1, 2, 3` — your printed values.  (A re-run of the reviewer's code on
the same machine, not a third implementation.)

## 3. The major finding

**M1.  Theorem 11.84(ii) is false as stated: the cost of the batched schedule is bounded on
the good event only.**
*Where.*  `THEORY_REPORT.md` lines 5617–5624: "(ii) in every run `|C_l| ≤ K + (J+1)·max{…}`
(*Claim B*, deterministic), so the cost is at most …"; `U_REPORT.md` lines 107–109, 138–139.
*What.*  Claim B bounds `|C_l|` only if every stored bracket of rung `l − 1` has ratio at most
`e^{x_{l−1}}`.  A bracket procedure may return a wider bracket with probability `δ′` (its own
trivial bracket, after an abort).  Then a member's lower end need not exceed `s_je^{−x_{l−1}}`,
the count fails, and `C_l` can be all of `C_{l−1}`.  The theory report states (ii) with no
stopping rule; the workstream's report has one, listed under *Output* — after the
evaluations it should prevent.
*Demonstration* (`experiments/science/ws_R4/m1_demo.py`): candidate sets computed as in the
theorem with all rung-1 calls returning the (valid) trivial bracket: `|C₂| = 162 178, 413 649,
307 083, 393 216` against `N₂ = 59 059, 105 262, 50 968, 79 931` in four of five
configurations; with honest brackets `|C₂| = 145 … 906`.
*Why it matters.*  "The bound on the number of queries holds always" is part of your
definition of a bracket procedure, and wherever a batched procedure serves as an inner
procedure — in the recursion 11.84(a) and in every many-level schedule behind `τ^{(r)} → h` —
the accounting of the next level multiplies by that bound.  It is the gap your referee R7
classified as major for Theorem 11.52.  The probability of such a run is at most `δ`; **no
exponent and no two-round statement "with probability `1 − δ`" is affected.**
*Correction (one line).*  "Before stage `l`: if `|C_l| > N_l` (or if some stored bracket of rung
`l − 1` has ratio above `e^{x_{l−1}}`), stop and return the trivial bracket."  On the good event
the rule never fires, so (i) is unchanged and (ii) holds in every run.  **With this rule
Theorem 11.84 is proved.**

## 4. A strengthening (abstract form machine-checked)

The union bound for the second round is over the second batch of the algorithm *run on the
virtual residual* — and in Theorem 11.86 that residual, `ψ⁰_{s¹}(x) = g₁(d(x¹, s¹))`, the flat
histogram of the first block, **is a member of the class**.  Hence:

**Theorem R4.1 [V: `two_round_expected_bound`, `two_round_expected_cost`, `two_round_bound_of_class`,
`card_distinguished_le_sum`; `experiments/science/ws_R4/lean/TwoRoundsExpected.lean`, built on
your `TwoRounds.lean`].**  In the situation of Lemma 11.85 for two rounds, with **no
assumption on batch sizes**: `1 − 2δ ≤ E|B₁|·p₁ + E_{ω,s₁}|B₂(v s₁)|·p₂`.

**Corollary R4.2 [P].**  Under the hypotheses of Theorem 11.86 every randomised two-round
algorithm correct on `L_u(Q_n)` makes, **in expectation, at least `(1 − 2δ)e^{nθ}/(n+1)²`
evaluations on the flat-histogram instance** (on average over its centre).  So `τ^{(2)} ≥ θ₂*`
holds for expected cost without the Markov step, and the hard instance is named: for two
rounds the flat histogram of a block plays the part that the zero function plays for
adaptive algorithms in Theorem 11.25(a).

## 5. Minor findings (locations and corrections in `R4_REPORT.md` §9)

* **m1.**  Lines 5625–5627 read literally say `τ^{(r)} = h` for a finite `r` — your own open
  question (1).  Proved: for every `η > 0` an `r(η)` independent of `n` with `τ^{(r(η))} ≤ h + 3η`.
* **m2.**  The recursion (a) is circular as printed (`L = 1`, `r₁ = r`); add `r_l ≤ r − 1`.
* **m3.**  "Batch sizes at most `M_t`" is ambiguous for `r ≥ 3` (the virtual run is not a run on
  one function) and stronger than needed for `r = 2`.
* **m4.**  Lines 5718–5720, "a third round reads it off: … `e^{nh+o(n)}`", is the *sketch* of
  Proposition 11.88(d), for an algorithm that knows the two blocks.  For algorithms correct
  on `L_u` the best three-round bound is `0.541a`.
* **m5.**  Lines 5586–5588 compare two *lower* bounds at `n = 3200` and read as a separation
  there.  None is shown: no adaptive algorithm in the repository costs less than `e^{0.037n}`
  at such sizes (the nested algorithms cost `e^{0.061n}` and `e^{0.051n}` at `n = 4000`).
* **m6.**  "Their exponent lies between" (README line 323; line 5737): the limit is not shown
  to exist; `liminf ≥ 0.359a`, `limsup ≤ 0.624a`.
* **m7.**  A slip in the proof of Claim B (`U_REPORT.md` lines 146–147); the conclusion stands.
* **m8.**  The machine-checked statement covers finitely supported randomness; the index
  should say "finite mixtures".
* **m9.**  "`τ^{(48)} ≤ 0.342a`" and the values for `r ≥ 4` rest on one grid computation with no
  stored witness (the ladders and round allocations), which would make them checkable in
  milliseconds.

## 6. What the README sentence (ix) is

| part | status |
|---|---|
| "two rounds provably do not reach the adaptive exponent" | **theorem** — paper proof, abstract lemma machine-checked, application re-derived; for every fixed accuracy, randomised two-batch algorithms correct on all of `L_u(Q_n)`, uniform cube, asymptotic.  That `h` *is* the adaptive exponent is Theorem 11.58, not re-examined here |
| "0.359a", "0.624a", "0.263a" | **numbers**: values of proved formulas; the second rests on Theorem 11.84 (proved once M1's rule is added) and on Theorems 11.56/11.57 |
| "their exponent" | the limit is not shown to exist (m6) |
| a separation at any finite `n` | **not a theorem and not shown** (m5) |

Everything is model-relative: exact evaluations of a residual known only to be
Hamming–Lipschitz on the cube, uniform reference measure, worst case.  The section makes no
physical claim, and after our pilot (SCI-RES-0002) we would not attach one.

## 7. Originality (thin; the deep search is SCI-REV-0004)

Round hierarchies are a standard genre and the coupling of Lemma 11.85 is the standard
round-elimination device.  Closest in kind, at the level of abstracts and snippets:
adaptivity hierarchies in property testing (Canonne–Gur 2017); rounds in parallel convex
optimisation; and, for *sampling*, Zhou–Wang–Sugiyama, "The adaptive complexity of
parallelized log-concave sampling" (arXiv:2408.13045, ICLR 2025) and "Sharp lower bounds
for parallel log-concave sampling" (arXiv:2611.15849, November 2026; the coordinator
confirmed title and identifier, not the author or the content) — polynomially many queries
per round, `Θ(log d)` rounds, hard instances with a chain of hidden pieces.  None treats the
*exponent* of estimating a normalising constant by value queries at a fixed number of
rounds, and the separating instance here is not a chain but **dilution**.  We concur with
A1: "plausibly original theorem, one step of a hierarchy proved".  Not found is not new.

## 8. Recommended corrective actions (theory)

1. Theorem 11.84: add the stopping rule (M1); reword the sentence on Theorems 11.54, 11.58
   (m1); add `r_l ≤ r − 1` (m2).
2. Lemma 11.85: fix "batch sizes" (m3); consider stating Theorem 11.86 at the flat-histogram
   instance (Corollary R4.2) and adopting `TwoRoundsExpected.lean` (imports `TwoRounds.lean`;
   four declarations; no new axiom).
3. Label the three-round sentence (m4); reword the `n = 3200` sentence (m5);
   "liminf/limsup" (m6).
4. `U_REPORT.md`: the parenthesis (m7); move the stopping rule before stage `l`.
5. Index of machine-checked statements: "finite mixtures" (m8).
6. Store a witness for every `T^{(r)}(0)` that is quoted (m9).

## 9. Requests to the engineering division (specifications in `R4_REPORT.md` §14)

* **R4-E1 (certified rows of the twins table).**  The finite-`n` statements of Theorem 11.86
  are floating-point evaluations of exact sums.  For `(u, n, n₁, T) = (1, 800, 360, 33.72)`,
  `(1, 3200, 1760, 125.68)`, `(2, 1600, 880, 200.87)` build the twins from the statement
  (reference: `experiments/science/ws_R4/twins_exact.py`, class `Twins`) in interval
  arithmetic and certify the Lipschitz property, the two coincidences, upper bounds for
  `p₁`, `p₂`, and `ln A(F_D) − ln A(F_S) > 1`.  *Validation:* agreement with `out_twins_*.txt` to
  four digits.  *Stop:* three certified rows, or a row that fails — report it.  Minutes.
  This would make Corollary R4.2 at `n = 3200` a rigorous finite-`n` statement.
* **R4-E2 (the two-round algorithm at finite `n`).**  Nobody has evaluated the cost of the
  batched schedule at finite `n`, and batching multiplies the number of inner calls by
  about `10²` at small sizes.  The exact expected cost with two rungs at the flat instance
  and at the flat-histogram instance, `u = 1`, accuracy 1, `n = 10³ … 6.4·10⁴`; report
  `ln(cost)/(na)` against 0.624, plain Monte Carlo and the two-round lower bound.  *Stop:* the
  size at which two rounds beat one, or the statement that they do not below `6.4·10⁴`.

Neither authorises resource use; both are CPU-only.

## 10. Not settled by this review

Is `τ^{(3)} = h`?  The value of `τ^{(2)}` in `[0.359a, 0.624a]` (the lower end cannot be raised
with these twins).  Strict monotonicity in `r`.  New: is `θ₂*` also the right cost *at* the
flat-histogram instance?  And the two most promising steps the reviewer sees: the two-round
exponent of the block-radial class on two known blocks (the lemma is tight there), and a
two-round algorithm with a non-uniform first batch.

## Limitations of the review

Theorems 11.56, 11.58, 11.51 and Proposition 11.57 were taken as given (refereed by your
R7, R8); the harness exercises 11.56 at small sizes with a simulated oracle only, and
`|C_l|` stays below 3 % of `N_l` there, so the *constant* of Claim B is not tested.  The
assembly of the recursion for `r ≥ 3` was read, not rewritten.  Finite-`n` numbers are
floating point.  Prior art: abstracts and snippets.

## Evidence and reproduction

`docs/science/workstreams/R4_REPORT.md`; `experiments/science/ws_R4/` (`NOTES.md` is the
step-by-step log; `exponents.py`, `twins_exact.py`, `asymptotic_check.py`, `small_cube.py`,
`small_cube_exact_opt.py`, `tightness.py`, `batched_sim.py`, `m1_demo.py`, `three_rounds.py`,
`cond_cover_check.py`, `gap_scan.py`, with outputs).  Lean:
`lake env lean experiments/science/ws_R4/lean/TwoRoundsExpected.lean` from the repository
root.

## Requested response

Whether you accept M1 and its one-line repair.  Suggested status line for §11.24 once the
corrections are in: "refereed (SCI-REV-0003): no critical finding; one major (the cost
bound of the batched schedule held on the good event only; stopping rule added) and nine
minor points, corrected".
