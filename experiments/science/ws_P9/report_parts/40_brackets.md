## 4. The certified brackets, with the predictions written before them

Script `p9_05_brackets.py`.  **Models.**  The coordinator's window models with exact in-window
evaluated terms, occupancy-aware reductions and the split of the far pairs around the anchor
(`window_model_occ.build_window_models_occ`, the rule "occ+" of `occ_reduction_test.py`, guided
by the Gibbs sample of seed 4242), built with **zero penalties plus workstream P6's
floating-point allowances** — `p6lib.fp_tables`, allocated exactly as in the state-independent
form of the same name: I call the coordinator's own functions (`site_form`,
`banded_pair_form`) with all constants set to zero, which returns the allowances alone (`φ₁` for
the site form; `ψ₁`, the in-band `ψ₂` and the halves of the out-of-band `ψ₂` for the pair, triple
and window forms).  Then my tables are added: site tables to `lo.one[i]`, `up.one[i]`, pair tables
with `add_pair`, tables on three or more sites with `add_multi`, with sign `∓`.  The ball is P8's
cached one, compared row by row with `pwmodel.ball_states`, 1 000 random values re-evaluated
(largest deviation `0.0`).  **Hypothesis used:** `|g − I_{m−1}g|(x) ≤ pen(x)` pointwise — Theorem R,
Proposition P, Corollary S.

**Rows.**  "P8's constants (the coordinator's recipe)": the reference, built by the
coordinator's code with P8's stored constants — it **reproduces the coordinator's brackets
digit for digit** in every case where one exists (Lys₁₂ order 5: S, B, T; Lys₁₂ order 4: T;
(LKSE)₃ order 5: T; Lys₅: T at bands 2 and 3), which is the check of my driver.  "Joint maxima
of stage 2 (constants)": the state-independent constants `ĉ^{J,2}_T` of Corollary J in the same
forms.  "Resolved": the tables of Proposition P.  Form W with constants is `p9lib.window_form_const`
(each subset charged to the maximal in-window sub-tuple with the least product of off-anchor
frequencies) — the allocation alone, without resolution.  *My chain against the coordinator's
recipe at twelve residues, as functions* [M; `p9_08_chaincheck.py`, `logs/chaincheck_*.log`]: the
rows with constants in forms S, B, T that are not the reference go through `p9lib.form_tables`
with constant tables; fed with P8's constants, that chain plus P6's allowances as my driver
allocates them equals the penalty function of the coordinator's `site_form`, `banded_pair_form`
and `triple_form_two_windows` at 5 000 uniformly random states to a relative `4·10⁻¹⁶` (S),
`2·10⁻¹¹` (B) and `2.5·10⁻¹⁰` (T) at worst over Lys₁₂ at orders 4 and 5 and (LKSE)₃ at order 5 —
the size of the recipe's own rounding allowances.  Two codes for one formula agree; it is
not a test of the formula.

**Checks.**  The sandwich `m₋ ≤ E ≤ m₊` at the 960 Gibbs states of the check sample (seed 777;
not the sample that guides the models) in every row; at 2 000 exact samples of the floor where
the last column says so; on Lys₅ and LKSE:5 at **every** state, with the exact `ln Z` inside
(§4.4).  *Against the coordinator's sampled values* (addendum A17 (18), items 62–63; theirs,
not mine; probability 0.95; the two-end intervals with empirical Bernstein of the order-5
runs, the narrowest the coordinator's driver prints — its logs
`pi_inference/nested_sampler_K12_H_m5_w7_T_window_SAb_occ.log` and
`nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`): {GEN_SAMPLED}

### 4.1 The predictions [written into `NOTES.md` before the models of each instance were built; the times are there]

{GEN_PREDICTIONS}

(The line "Lys₁₂, 5: T, stage 2" reads 0.016 at four digits; the width is 0.0159968
(`out/brackets_K12_H_0.70_m5_w7_B.json`), below the lower end 0.016 of the range I had given
by `3·10⁻⁶`: "no".)

Basis of every prediction: the first-order numbers of §3.2 plus the penalty-free width, and a
guess about the floor.  **What was wrong, and why** — §4.5.

### 4.2 Lys₁₂ on the helix [M; validity P]

{GEN_BRACKETS_K12_M4_W7}

{GEN_BRACKETS_K12_M5_W7}

### 4.3 (LKSE)₃ on the helix [M; validity P]

{GEN_BRACKETS_LKSEC12_M5_W7}

### 4.4 Every state: Lys₅ and LKSE:5 [X]

On the enumerated instances the same driver checks every sandwich at every state and
whether the exact `ln Z` (`251.348445` for Lys₅, `276.467293` for LKSE:5) is inside.  Result:
{GEN_ENUM_SENTENCE}.  Logs: `logs/brackets_K5_H_0.70_m4_w2.log`, `_m4_w3.log`, `_m5_w3.log`,
`logs/brackets_LKSEc5_H_0.60_m4_w2.log`, `_m5_w2.log`.  My chains with P8's constants (rows "my
chains") equal the coordinator's forms to every printed digit.  Two of the five tables:

{GEN_BRACKETS_K5_M4_W2}

{GEN_BRACKETS_LKSEC5_M4_W2}

{READING_BRACKETS}
