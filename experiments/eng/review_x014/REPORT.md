# Referee report: ENG-RES-0016 §§1–3, `hetero.py`, the literal simulators, and what was added during the review

*An adversarial review inside the Computational Research Division: an AI agent briefed to
break §2 of ENG-RES-0016 (the transfer of Theorem K1 to a cube whose sites have different
slopes) and the sorted-slope tail functions, with code of its own.  Not external peer
review.  The report is the referee's, reproduced as handed back (only the layout of lists
and tables was touched); the coordinator's note at the end says what was done with it.
Line numbers refer to the draft of ENG-RES-0016 in the engineering tree at `1900a76`.*

Pinned sources: `K_REPORT.md` and `N_REPORT.md` at theory `fc3f5d9` (newest when the review
started); theory report §11.33 and `N_REVIEW.md` at `eb88823`; engineering working tree at
`1900a76`.  Nothing from the theory branch was executed.

## 0. Verdict

**NOT BROKEN.**  Every step of `K_REPORT.md` §2.4 (good event, Steps 1–9, Lemmas K.1, K.2) was
re-derived with the draft's substitutions; each is correct and sufficient.  The constants
were recomputed independently and the statement attacked with the referee's own
simulator.  No counterexample: 0 invalid brackets and 0 violations of any claim in 224,577
literal runs with the statement's constants; 0 violations of a deterministic claim in any
of 333,469 runs.  Eight deliberately wrong transfers are all caught.  The mixed outer
block with sorted-slope tables and the lower bound of §3 also survive.

**Strongest objection.**  Lines 115–124 say that §2 "needs no proof of its own" because it
is Theorem N3 = 11.118/11.119(a).  That is true for a different algorithm from the one §2
states and both simulators run.

- Theorems N1/11.118 are for 2L⁺ "with a stop when the ladder passes the cap" (rule (c0)).
  The theory division's own referee writes that K1's Step 9 (atoms) was replaced by that
  rule (`N_REVIEW.md` §1.2).
- §2 says "exactly as in `K_REPORT.md` §2.2", which has no cap stop.  For that algorithm,
  claim (i) (no abort, stop at a level `≤ J`) is exactly the part N1 does not prove.
- N1′ does not cover it either: it needs `Ξ(q) ≤ θν₁q` below `π_*` and has its own `J`, which
  can exceed the draft's.
- Everything else in the reading is right.  (F1), (F2), (B) verified with `κ₀ = Π`,
  `V_max = e^{−ψ₀+Ω}`, `x₀ = 2Ω_Y`.  The draft's `J` is an admissible larger integer.  `π†` is an
  admissible `π_*`: N1's [N], [P] were derived for all `q < π†` from the radius conditions
  of `K_REPORT.md` §2.1.  With these, N1's constants are the draft's.
- Fix: one sentence.  Either state §2 for the algorithm with the cap stop, or keep 2L⁺ and
  say "N3 for claims (ii)–(vi) and the deterministic claims; termination by the Step 9
  line", which is correct as written.

**Second objection: §0.5/§6 overstate the evidence.**

- "Two negative controls fail as they should" (line 52).  In `x014_literal.json` the
  invalid counts are 0, 10, 6, 22 of 540 (tables for `u_o/4`) and 1, 7, 2, 1 of 540
  (`K/64`).  No control cell exceeds `δ = 5 %` (maximum 4.1 %), and one detects nothing.
- "No abort" is a property of the instances drawn.  `hetero_literal.run_2l` aborts
  deterministically on a plain class member (cone on the outer block with apex at the
  reference point, flat fibres, oracle "top") with the statement's constants: 40/40 runs
  for (6 sites of 0.5; inner 3 × 2.0) with the BND set, 23/40 for the draft's own shape (8
  of 2.0; 4 × 0.5) with EXT, 40/40 for (5 of 1.0; inner 1, 1, 2) with EXT.  It is the
  floating-point tie of erratum m10/e2; there is no tie rule.  Reproduce with
  `tie_abort_example.py`.
- The division's literal runs never use an outer block that is a proper part of a type
  (`experiment()` forbids it, line 233), never a mixed outer block, never K0 on a mixed
  block.  All three carry §5.  The referee ran all three: no violation.

## 0a. An incident the referee caused

The 18:03 UTC restart (2026-11-26) was almost certainly the referee's doing.  The first
version of `check_lower_bound.py` called `hetero.hinted_lower_bound` on a random four-type
block with up to 300 sites per type.  `weighted_shells` enumerates `Π(n_t + 1) ≈ 8·10⁹`
shells; the process was seen at 6.4 GiB resident with 133 MB free seconds before the
machine went down.  That broke the 3 GiB rule and killed the division's jobs.

Since then the generator has a size cap and every script sets a hard `RLIMIT_AS` (1.3 GiB
per worker, at most 2.5 GiB single-process); there were no memory errors afterwards.  At a
few moments a short single-process check ran beside a two-process campaign.

Side finding: `weighted_shells` (`hetero.py` line 514) has no guard on the number of shells.

## 1. Line-by-line table

R = re-derived by the referee; N = tested numerically.

| item of `K_REPORT.md` | what it uses | the draft's substitution | finding |
|---|---|---|---|
| Lemma K.1(a), (b) | Hamming cube, uniform measure, Harper, one slope of `−ln W` | outer cube, `u_o` | Correct, sufficient.  R (given Harper).  N: 3,527,964 thresholds on 172,173 instances; equality attained, never exceeded.  Tables for `½u_o` or `0.8u_o` refuted in all 15 shapes. |
| Lemma K.2 | equal weights on the fibres (product measure), slopes of the outer sites only | `−ln W ∈ L_{u_o}(Q_{n_o})` | Correct.  R.  N: largest outer slope of `−ln W / u_o = 1 + 5·10⁻¹⁴`.  The inner block need not be a cube. |
| step 0: `s₀`, range of `W` | slope × all sites | `Ω` | Correct.  R.  Control caught. |
| step 0: first `ℓ` | binomial sum of the lower cone | `e^{−ψ₀}Π(1+e^{−u_i})/2 = e^{−ψ₀−Ω}/Π` | Correct.  R.  Equality instance in about 5,700 runs.  Control (homogeneous `ℓ`): 651 of 5,715 invalid. |
| step 1: trivial bracket | `u·n_i`, a reference point of the inner block | `Ω_Y` at `(a, 0_Y)`, ratio exactly `e^{2Ω_Y}` | Correct; any fixed inner point would do.  Control (`u_o·n_i`): 2,440 of 6,547 runs violate (2.1). |
| `J` | `2un` from Step 9 | `2Ω` | Correct.  Control: 6,092 of 9,178 runs abort. |
| `ν₀, m_max, K, ν, M†, M̄, δ′, cnt, C_max` | slope only through `J`, `π†`, `x₀` | formulas unchanged | Correct.  N: 600 random parameter sets (`n_o ≤ 90`, outer blocks that are part of a type included): `J, K, m_max, r†` identical to `hetero.constants`, logarithms within `2·10⁻¹³`. |
| `ν₁` | free, `≥ 1` | `2e^{u_o}n_o/θ` in "bounded" designs | A design choice the theorem allows.  `u_o` is the right slope for its purpose (Lemma K.4(a) on the outer cube).  Validity does not depend on it. |
| good event (V1) | fibres in the class of `Y`; `K·2^{m_max} < 2M̄` | procedures for the class of `Y` | Correct.  R. |
| (V2), (V3) | i.i.d. uniform outer points; thresholds functions of `ψ₀` | none needed | Correct.  R. |
| Step 1 | `x_L ≤ b` | none | OK. |
| Step 2 | first `ℓ`; Markov; Harper term = K.1(b) on the outer cube | covered above | OK.  Line 101 is wrong in letter: Step 2 does use the slope. |
| Step 3 | layer cake; K.1(a) on the outer cube | covered | OK. |
| Step 4 | `s₀ = Π·ℓ_initial ≤ Π·L` | `Π` | Correct.  R.  Deterministic; never violated; smallest slack `x_out − width` 0.0031. |
| Step 5 | definitions of `Γ̃, Γ″, r†`; `T` nondecreasing | outer tables | OK.  (iii) never violated.  Control without the Harper term violates it (200 of 5,431). |
| Step 6 | `M₀^neg ≤ νΠe^{−b} < ν` | `Π < 1` | Correct.  R. |
| Step 7 | first case needs `ℓ_j ≥ s₀`, i.e. `Π ≤ 1` | not mentioned | True and harmless, but a use of the slope the draft's list omits. |
| Step 8 | rung-0 ratio `e^{x₀}`; `J` | `x₀ = 2Ω_Y` | Correct. |
| Step 9 | `Ω`; `A < s₀e^{2Ω}` strictly; atoms `2^{−n_o}` | as in the draft | Correct.  R.  This is the step N1 does not contain. |
| errata m1, m3, m10 | abort test before every query; `L > U` gives the trivial bracket; ties | not mentioned | Line 74 does not say which version of §2.2.  "Cost `C_max` in every run" needs m1. |
| nested use | inner run is a bracket procedure for the class of `Y` with `x_out(Y) ≤ x_l`, failure probability `δ′`, cost its own `C_max` | as coded (`l2p` of the inner block, `l_inv_delta_p`) | Survives.  N: 3,744 end-to-end three-level runs, 109,104 middle runs; nothing invalid, too wide or aborted at either level. |
| symmetry | none in §2 beyond Harper on the outer cube | — | §3 uses translation invariance; verified. |

## 2. Code against statement

**`hetero.constants`** agrees with the table of §2 and with `alg2l.constants`.  Harmless
discrepancies:

- It returns `None` when `2Ω_Y ≤ b` (line 292).  The theorem allows such levels (the trivial
  bracket already classifies, no inner call is made); for blocks with a flat remainder
  they would be the cheapest.
- The search accepts `x_out ≤ x + 10⁻⁹` (line 446).
- Header lines 25–27 repeat "Steps 1–3 and 5–8 do not mention the slope" and "cost bound
  in every run" without the abort rule.  The header was not updated for `comp`.

**`hetero_literal.run_2l`** is a faithful transcription.  With the same floats for `Ω`, `ln Π`
and the ladder, 11,680 runs agree with the referee's simulator in status, level, sample
size, number of queries and both ends (to `4·10⁻¹⁵`).  Discrepancies with `K_REPORT.md` §2.2
plus errata:

1. No query-budget abort, so "no cost above the bound" is an observation, not the rule.
2. A pair with `L > U` is not replaced by the trivial bracket (it is counted invalid:
   conservative).
3. No tie rule (see §0).  With a different summation order for `Ω`, the two simulators
   disagreed in 127 of 7,170 runs, all at exact ties.
4. Tolerances of `10⁻¹⁰` and `10⁻¹²` in the radius searches; harmless at these sizes.
5. Certificates are checked only at levels left, and `ℓ ≤ A` only at the end.  `p̲` is never
   checked, nor the stopping pass's `q`, nor claims (iii)–(vi).
6. Aborts are returned as `valid = True` (the trivial bracket); fine.

**`nested_literal.py`**: `three_level_run` returns a middle run's shared count `q_real` (line
222).  The top level's "theorem's accounting" (lines 18, 70, 119) is therefore unshared
top calls times shared middle costs.  On identical instances it is 4 to 7 nats below the
count with middle runs charged their own theorem count (12.3 against 19.2; 15.9 against
20.8; bounds 36–39).  Harmless for "below the bound"; the label is wrong.

`tests/eng/test_hetero.py`: 18 passed on the changed module.

## 3. The lower bound of §3

- **Valid.**  2,397 explicit checks: the dip is in the class, its support is the open ball,
  the factor is `1 + Exc(ρ)`, translation invariance and the double count hold.
- **The code computes what the text says.**  `hinted_lower_bound` matches an independent
  evaluation with exact rational distances and 50-digit arithmetic in 234 cases (largest
  difference `5·10⁻¹³`) and a scan of explicit cubes in 84.  Ties, the open/closed ball and
  the supremum over `ρ` are handled correctly.
- **"The smallest admissible dip" and "exact" overstate.**  It is the smallest weighted
  ball carrying the cone.  The same argument admits any class member vanishing outside a
  set `D`.
  - Dips that ignore some sites give a larger bound in 58 of 75 cells of the referee's
    scan, and in 15 of 25 at `n = 1000` (up to 0.67 nats, at most 1.0 % of the bound).
    Example, checked independently: slopes `(4, ¼)`, 100 + 100 sites, `ε = 0.8715`: 26.583
    nats for the whole block, 27.261 using the steep sites alone.
  - On `Q_4` a smaller admissible set than the ball exists in 27 of 77 (pattern, accuracy)
    cases, the uniform cube included, by a factor up to 2.5.
  - So the bound is not monotone in the block and not the optimum of its own argument.
    The effect is below the precision of the tables, but the wording should change.
- Lines 148–149: add "in expectation" and "distinct", as in Theorem 11.25(a).
- `np.round(d, 12)` merges ties robustly for the dyadic slopes used; for other slopes at `n`
  near `10⁴` a tie could split.  Argued harmless, not tested at that size.

## 4. Mixed outer blocks (added while the review ran)

Both sorted-slope inequalities were derived independently before the updated draft was
read.  They agree with Lemma N14 and with the draft's lower function
`T(k) = Σ_j C(m,j)e^{−U_{(j−k)₊}}`.

- **Brute force:** all 65,534 proper subsets of `Q_4` for 8 slope patterns, plus 387,540
  random and structured subsets of `Q_5` to `Q_8`: 0 violations of either inequality.
- **`MixedTables` against the definitions:** 207 compositions within `4·10⁻¹³`; blocks up to
  640 sites within `2·10⁻¹²`; `r†` agrees in 621 of 621; `constants(comp)` in 207 of 207.
- **Literal runs** with mixed outer blocks: 4,552 with the referee's simulator, 0
  violations; 4,524 with the division's fed `mixed_tables`, 0 invalid or too wide, 2
  aborts (not attributed; the referee's on the same configurations are ties).
- **Controls caught:** slopes sorted the wrong way, 2,532 of 13,805 invalid; uniform tables
  for the smallest slope, 2,396 of 12,380.
- **K0 on mixed blocks:** 6,496 runs with the largest slope (the draft's claim) and 6,728
  with sorted tables: 0 invalid, 0 too wide.  Control with the smallest slope: 6,550 of
  20,416 invalid.
- One note: for odd `m` and `η = ⅓`, `kappa` differs from the exact value at radii above
  `m/2`.  This is the documented tolerance of `tables.kball`; it does not affect validity
  and is not specific to `hetero`.

## 5. The numerical attack

`review_sim.py` is written from `K_REPORT.md` §§2.1–2.4 and the draft's table, with exact
integer balls and rational `q`, `p̲` and radii.  It checks every claim (i)–(vi), the width
and its four terms at every pass, and evaluates (V2), (V3) on the realised sample.

Coverage: 26 shapes with 1 to 11 outer sites, slope ratios 100:1 and 1:60, an inner block
of one site, inner blocks containing the outer type; 13 parameter sets (`η` from ½ to 1/20,
`λ` from 1 to 0.05, `η′` from 1 to 0.02, `θ` from 0.01 to `e⁸`, `b` down to 0.02, 1 to 8 rungs); 16
instance kinds; 8 oracles, 4 of them adversarial.

| campaign | runs | outcome |
|---|---|---|
| statement's constants, 222 configurations | 90,993 | 0 violations; 23 tie aborts; cost at most `e^{−3.6}·C_max` |
| flat outer blocks (closures at radius `≥ 1` in 90,864 runs) | 91,013 | 0 violations; 22 tie aborts; true tail at most 0.44 of the bound; Harper bound within 2 % of equality |
| dip tuned against each design, the claim's tables | 42,571 | 0 violations; true tail at most 0.43 of the bound |
| `K` divided by 8 and 32, two campaigns | 108,892 | events fail in 5,118 runs; 72 invalid brackets, all in those runs; 0 violations where the events hold; no false certificate at a pass whose own event held (checked in the second campaign) |
| eight wrong transfers | 54,270 | every one caught |
| the division's simulator and constants on the referee's shapes and instances | 89,289 | 0 invalid, 0 too wide, 0 over `C_max`, 0 false certificates; 22 aborts, all ties |
| consistency: certified bound against lower bound | 48 searches, 4,974 single levels | none below the lower bound; smallest ratio 1.37 |

**A limit the division should know.**  Bracket-level tests have little power against an
error in the upper tail function.  With outer tables for half the slope, `U` missed `A` in
only 10 of 6,234 runs; on the tuned dip the wrong lemma was exceeded by 1.2 % and the
bracket was still valid.  The lower tail (Harper) side is the sensitive one: about 10 % of
runs invalid.  That is why the per-threshold test in the first row of §1 is the decisive
evidence for the tables.

The frequency against `δ` was not resolved from below: the good event never failed with the
statement's constants, and 26 of the 222 configurations have fewer than 60 runs.

## 6. Opinion on what is not claimed

- **"Nothing in the proof asks `Y` to be a cube" is right.**  It is N3.  The list (i)–(iii)
  omits two things it tacitly needs: the class must be Lipschitz in the outer variables
  with slope `u_o` uniformly in `y`, with a product measure; and the point bracket's ratio
  must be bounded uniformly in `a`.
- **The restriction to one type is not needed for validity** (Lemma N14 plus its mirror
  image, now in the draft).  It is essential only for sharp tables.  No sharper finite-`n`
  statement for a mixed block was found: the two-stage Harper argument degenerates on
  full fibres.  The draft's "nothing says it reaches `h`" stands.
- **Free improvements the draft does not use:** the cap stop with `J = ⌈2Ω/λ⌉`; the
  moment-form point bracket, `x₀ = Ω_Y` instead of `2Ω_Y`; K0 on a mixed block with the
  sorted tables (valid, never worse than largest-slope inclusion); levels with `2Ω_Y ≤ b`;
  sub-block dips in the lower bound.

## 7. Minor findings in the text

- Line 74: name the version of the abort rule.
- Line 101: replace by "Steps 2, 3, 5 use the slope only through Lemma K.1 on the outer
  cube and the first `ℓ`; Step 7 uses `Π ≤ 1`".
- Lines 108 and 423 ("part of one type", "no mixed outer block") and line 422 ("two site
  types") contradict §§5.1–5.2.
- Line 52: give the control numbers instead of "fail as they should".
- In 8 of the 12 literal configurations `r†` is −1 or 0.  Record how runs close, as a measure
  of how much the tail lemma at positive radius was exercised.

## 8. What was not checked

- §4 (exponent formulas, `t*`), the numbers and tables of §5, §5.1, §5.2 and the title, the
  Modal outputs, `make_tables`.
- `HSearch` beyond reading it and the consistency scan (`n ≤ 2,000`); `certified.py` and
  `meanrun.py`.
- Sizes: literal runs reach at most 17 sites and 11 outer sites.  Inner procedures are
  oracles except in the nested runs (enumeration at the base) and the K0 runs.  No run
  with K0 inside 2L⁺, none with four levels.
- Inputs taken as given: Harper's theorem, the Chernoff bounds, the Lean inequality behind
  Theorem 11.25(a) (the counting for weighted dips was re-derived; the Lean was not read),
  Theorems 11.95–11.101.
- Theorem N1's proof: read, hypotheses and constants checked, not refereed.
- Draft edits after `1900a76`.

## 9. Files

Everything is in `experiments/eng/review_x014/` (3.6 MB).  Each script writes a JSON of the
same stem; `attack.py` writes one per mode (`theorem`, `radius`, `tuned`, `kdiv`, `mutations`).
`summarise.py` prints the numbers of this report from the JSONs; start there.

`review_sim.py`, `attack.py`, `attack_their_sim.py`, `attack_nested.py`, `check_code.py`,
`check_tail_lemma.py`, `check_mixed.py`, `check_k0_mixed.py`, `check_lower_bound.py`,
`check_bounds_vs_lower.py`, `tie_abort_example.py`, `nested_count_comparison.py`, `summarise.py`.

---

## Coordinator's note (2026-11-26/27, after the hand-back)

**Checked by the coordinator.**  `summarise.py` run here: it prints the counts of §5 from
the stored JSONs.  `tie_abort_example.py` run against the simulator as it was: 40/40,
40/40, 0/40, 0/40, 23/40, 40/40 aborts on "cone on the outer block, apex at the reference
point, flat fibres, inner answers at the top" in its six configurations, none on its
other instances — the referee's claim, reproduced.  No path, name or address in the
delivered files.  Not checked: the proofs of §1 line by line beyond reading them; the
campaigns were not re-run.

**What was done with the findings** (all before ENG-RES-0016 was published):

| finding | action |
|---|---|
| strongest objection (the relation to Theorems 11.118/11.119(a) holds for claims (ii)–(vi); termination is our Step 9) | ENG-RES-0016 §2 and its request to the theory division reworded accordingly |
| the negative controls are weak; "no abort" is a property of the instances | ENG-RES-0016 §0 item 5 and §6 rewritten with the numbers; the referee's controls and runs reported as the stronger evidence |
| no tie rule in `hetero_literal.run_2l` | **fixed**: comparisons of bracket ends with levels use the tolerance `TIE` of the mean-run evaluator; the example then gives 0 aborts in 1,440 runs (the stored `tie_abort_example.json` is from that re-run; to see the aborts, run the script with `experiments/eng/twolevel/hetero_literal.py` of commit `1900a76`).  The literal experiment is being repeated with the rule and with the tie case among the instances (`x014_literal_v2.json`; addendum) |
| `weighted_shells` has no guard | **fixed**: a limit of `3·10⁷` shells, with an error that says why |
| line 101, line 74, lines 108/422/423, line 52 | reworded in ENG-RES-0016 §2, §6, §7 |
| the lower bound is not the optimum of its own argument; "in expectation", "distinct" | ENG-RES-0016 §3 reworded, with the referee's example |
| the label "theorem's accounting" in `nested_literal.py` | corrected in the text of ENG-RES-0015 §7 (the code's label is unchanged; the result files are as published) |
| `hetero.constants` returns `None` when `2Ω_Y ≤ b`; other free improvements | listed in ENG-RES-0016 §7 as not used; not implemented |
| remaining discrepancies of `run_2l` with the errata (no query-budget abort; `L > U` not replaced; certificates checked only at levels left) | not changed; stated here.  The referee's simulator checks all of them |

**The incident of §0a** is recorded in the research log (session 4) and in the dead-end
list; the rule that follows from it — every exploratory script of a subagent runs under a
hard address-space limit — is in the handoff.
