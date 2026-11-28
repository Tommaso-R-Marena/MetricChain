# Resolution of the review SCI-REV-0030 (workstream R29) of Theorem 11.58e

*Theoretical Research Division, Phase II, 2026-11-28 (objective 8 of the Phase II directive).  The
review — by a referee of the Scientific Discovery Division, with replication — was published incomplete
on 2026-11-27 01:10 UTC, when every division halted; it was never answered.  It is in the consolidated
archive: `consolidated/03_scientific_translation/docs/collaboration/messages/science/SCI-REV-0030.md` and
`…/docs/science/workstreams/R29_REPORT.md`.  Its verdict: "no error of substance found in the parts
examined"; one major finding about evidence (F1), six minor ones (F2–F7), and a list of parts it did
not reach.  Everything below is the work of AI sessions; the referee's scripts were read, not run.*

## 1. The findings, one by one

| | finding (the referee's words, shortened) | status | where |
|---|---|---|---|
| **F1** (major) | the script `z6_certified_tops.py` ends with "ALL CHECKS PASS", which tests monotonicity (true by construction) and `c_j > h`; of 30 mutations it catches 2, and 17 break a certificate and still end with that line.  "The tables are right because the code path is right (the independent checker shows it), not because a check says so" | **accepted; resolved** — see §2 | `docs/workstreams/Z_ADDENDUM.md` A6b ("What is evidence for a run, and what is not"); `experiments/workstreams/Z/z6_pipeline_mutations.py` |
| **F2** | Proposition A13 does not literally cover the cap line (it is below the *maximum* of two lines of the stated form); "nondecreasing" does not follow from positive slopes for lines that are merely below such lines | **applied** (the referee's wording): `V′` convex, `V′(0) = 0`, `V′(c′) ≤ 1`, `V′ ≤` the maximum of the zero line and of such lines; nondecreasing because convex, nonnegative and zero at zero | `Z_ADDENDUM.md` A6b, statement and proof of Proposition A13 |
| **F3** | the base case: the certified sequence starts at `c₀ = ā > a`, so it is Corollary A4, not Proposition A8 | **had been applied before the halt** after our own referee found the same ("By Lemma A1, Corollary A4 and Proposition A8 (its base case read for a start on `[0, ā]`)") | `Z_ADDENDUM.md` A6b |
| **F4** | printed certified decimals are rounded to nearest, not upwards (no table entry is wrong: smallest margin `2.7·10⁻⁸`) | **had been applied**: the nine-digit table says "rounded to nearest: a rigorous reading adds one unit in the last printed place"; the six-digit table of the theory report (Theorem 11.58e (f)) is rounded up.  The engineering division's rounded values `0.5004, 0.3633, …` are not upper bounds — its own correction (ENG-MSG-0009 §3(a)) | `Z_ADDENDUM.md` A6b; theory report Theorem 11.58e (f) |
| **F5** | "for the cube `τ₂ = a²/(a + x*)`" is false for `u > 4.6535196185` (at `u = 5`: `0.602893·a` against `0.604053·a`); `τ₂ = b₂` is unaffected | **had been applied** (found independently by our referee, `Z_A6_REVIEW.md` §1.5): the closed form is stated for `u ≤ 4.6535` only | theory report Theorem 11.58e (e); `Z_ADDENDUM.md` A6a; D-register |
| **F6** | `τ₃ = 0.361184·a`, not `0.361189·a` (our zooming minimiser stalls); `b₃ − τ₃ = 2.117·10⁻³·a`; `τ(M₂) = b₃ = 0.363300650·a` | **had been applied in the texts** (the table of A6a gives `0.361189·a` as "about `5·10⁻⁶·a` high: `0.361184·a` by two referees' independent computations"; the theory report quotes `0.3612·a`, `0.3633·a`, `2.1·10⁻³·a`).  The stored output `out_z7_exactness_u1.txt` still prints the script's `0.361189`; it is an output, not a claim | `Z_ADDENDUM.md` A6a |
| **F7** | "strictly better from the third level on" is a floating-point computation, [N]; margin four orders above any visible error; an interval proof is within reach and not done | **agreed; unchanged**: the statement is labelled [N] in the theory report.  An interval proof was not attempted in Phase II | theory report Theorem 11.58e (e) |

## 2. F1: what is evidence for a certified run

* The validity of a run is established by an **independent exact checker**,
  `experiments/workstreams/Z/review_a6/a6_02_verify_z6_output.py` — written by the referee of the addendum,
  sharing no code with the script: its own integer interval arithmetic and hull; for every stored line
  it exhibits a parent line, a rational pair `(e₀, ϑ₀)` and a rational witness `ρ` with
  `KL(ρ‖p_u) ≤ e₀`, `KL(ρ‖½) ≤ ϑ₀`; the cap line, the family property and the top are verified exactly.
* **Mutation study of the pipeline** (`experiments/workstreams/Z/z6_pipeline_mutations.py`, output
  `out_z6_pipeline_mutations.txt`; `u = 1`, four levels, 40 sample points — small, so that every mutant is
  checked to the end).  Each textual mutant of the script (a scratch copy; the repository file is never
  modified) is run through its own `main()`, and its output through the independent checker (the referee's
  file, unmodified).  Two kinds: *gross* mutations break the certificate by a margin far above rounding
  and must be rejected — `up()` rounding down, the rate and the bound of `θ` too small by `10⁻⁶`, the two
  divergences exchanged, `θ` bounded at a shifted rate, a stored slope too large and an intercept too
  small by `10⁻⁶`, a steeper parent line, a cap with half the tangent slope, a top lowered by `10⁻³`;
  *margin* mutations only remove a safety margin (one or four units in the last place, a cap flatter by
  `10⁻⁶`, a relaxed top test), so whether the output is still a certificate depends on the instance, and
  the checker's verdict is reported.  **Result: §4.1.**
* **Coverage of the committed runs** by independent exact checkers: the science division's referee
  verified the three committed runs at `u = 1` (80 levels), `u = 2`, `u = ½` (40 levels), `K = 3000`, line by
  line (278 704 generated lines at `u = 1`, no violation, no top differing from the committed output);
  our referee verified 31 946 lines, among them the first eight levels of the published run.  **The
  400-level run** (`out_z6_certified_u1_J400.txt`, `K = 4000`; the source of the value at `k = 400` in the
  theory report and of the constants quoted by the engineering division) was left unchecked by
  both: **see §4 for what was verified in Phase II.**
* The harness test XVI.11 (`t_certified_tops`) is a third, independent re-implementation of the
  construction (own pairs, hull and step) with eleven mutations; the science referee did not have it.
* The script itself is unchanged (its outputs would have to be regenerated; the last line is now
  documented for what it is).  A version that writes a certificate file for a separate checker, as the
  referee proposed, was not written: the checker re-derives a witness for every line from the output
  alone, which is the stronger check.

## 3. What the referee did not reach — unchanged, and not reviewed outside this division

Parts (b)–(d) of Theorem 11.58e (they rest on workstream Q2's Lemma U and Proposition T): reviewed by
our internal referees only (`Z_REVIEW.md`, `Z_ADDENDUM_REVIEW.md`).  Item 5 of its brief (the nest):
nothing run.  The size paragraph by its own numbers: not finished; by *our* numbers, read by the
referee: "at every size where the bound is below the non-adaptive cost it certifies a number of
evaluations nobody can make, so the theorem is a complexity law only" — this is also our own
assessment (consolidation report, §B1; theory report, "what it is not").  The comparison with our
three internal reviews: not done by the referee.  The referee's scripts for these items
(`r29_i5_level_of_nest.py`, `r29_i6_crossover.py`) were, by its own account, written and never run; we
did not run another division's unreviewed code.

## 4. Phase II results (filled in when the runs finished)

<!-- R29:RESULTS -->
### 4.1 The mutation study (finished 2026-11-28 02:53 UTC; `experiments/workstreams/Z/out_z6_pipeline_mutations.txt`)

| | number | the script's own last line | the independent checker |
|---|---|---|---|
| unmutated script | 1 | "ALL CHECKS PASS" | accepts |
| gross mutations G01–G10 | 10 | **still "ALL CHECKS PASS" for 9**; the tenth (a cap with half the tangent slope) trips an assertion of the script | **rejects all 10** |
| margin mutations U01–U06 | 6 | "ALL CHECKS PASS" for all 6 | rejects 2 (a stored slope rounded up, an intercept rounded down — four units in the last place each); accepts 4 (the rate and the bound of `θ` rounded down by one unit; a cap flatter by `10⁻⁶`; a relaxed top test) |

This is finding F1 in our own numbers: nine mutations that break the certificate end with the script's
own "ALL CHECKS PASS", and the independent checker rejects every one.  The four accepted margin mutants
are not misses: when the checker accepts, it has exhibited a proved rational pair for every stored line
and dominated the cap by lines of its own, so that *output* is a valid certificate — the mutation removed
a margin (the script keeps four units in the last place) that this instance did not need.  **What the
study does not show:** that the checker rejects every invalid output (ten gross mutations, one small
instance); and nothing about the script's behaviour at `K = 4000` — that is §4.2.

### 4.2 The 400-level run

<!-- R29:J400 -->
*(pending: the exact re-verification of the 400-level run was still running when this text was committed.)*
<!-- /R29:J400 -->
<!-- /R29:RESULTS -->
