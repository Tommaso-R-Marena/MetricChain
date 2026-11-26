## 2. Validation by enumeration — before anything was computed at twelve residues

Script `p9_01_validate.py`; logs `logs/validate_K4_H_0.70.log`, `validate_K5_H_0.70.log`,
`validate_LKSEc5_H_0.60.log` (the runs cited are the re-runs with the final library; the first
runs, made with an earlier version of one routine, are in `not_cited/` and gave the same numbers
to the printed digits).  Instances: Lys₄ (16 464 states), Lys₅ (115 248), LKSE:5 (14 508) on the
helix, P2's pruned domain as P3 and P8 use it; every order `m = 3 … n`; **every state**.

**Left sides — my own code** (P3's evaluator supplies coordinates and Born radii only).
`g` at every state (P3's bulk evaluator); every term `t_pq`, `p ≤ q`, at every state from
coordinates and Born radii (the sum of the terms equals `g` to `1–2·10⁻¹²` kcal/mol);
`R_m(x) = |g − I_{m−1}g|(x)`; and, block by block, `L_m[𝔅](x) = Σ_{τ∈𝔅} |τ(x) − I_{m−1}τ(x)|` — absolute
values term by term, so that no cancellation inside a block can hide anything.  Three
independent confirmations of the left sides: P8's stored enumeration of `g` (`1.3–2.8·10⁻¹²`);
P8's stored block remainders, an enumeration pass of its own (`ws_P8/cache/bc_*_ckpt.npz`,
array `ACCR`; agreement `5·10⁻¹³`–`1.3·10⁻¹²` kcal/mol on all three instances after the blocks are
put in the same order — see my error 3 in §8); and the coordinator's three logs
`p8_verification/lys_enum_check_K4.log`, `_K5.log`, `_LKSEc5.log` (largest `R` of every order and its
Boltzmann mean, to the printed digits).  *The "self-test" printed in my
logs is not an independent check:* the two remainder routines it compares perform the same
subtractions in the same order (deviation exactly 0).

**Right sides.**  `E^s[𝔅](x) = Σ_{T ⊆ S(x)} Θ^s_{𝔅,T}(x_T)` for stage `s = 1` (P8's own arrays, recorded
in its code path before `_c1`/`_c2` maximise them) and `s = 2` (my evaluation with the actual
increments), and every table form built from them.  Two checks of the *code* precede the
checks of the statements (`p9_00b_consistency.py`, logs `logs/consistency_*.log`): the maximum
over the states of a stage-1 block table **is** P8's 'SAb' block constant (relative deviation
`0.0`), and stage 2 with every actual increment replaced by P3's maximum reproduces stage 1
(`4·10⁻¹⁶` on Lys₄, `9·10⁻¹⁶` on a sample of four subsets of Lys₁₂ at order 5).

**Checks** (tolerance `10⁻¹⁰` kcal/mol absolute, `10⁻¹²` relative):

* **V1** `L_m[𝔅](x) ≤ E^s[𝔅](x)` for every block, state and order — Theorem R itself, sharp.
* **V2** `R_m(x) ≤ E^s(x)` — the hypothesis of the pipeline, resolved.
* **V3** `E^s(x) ≤ pen(x)` and `R_m(x) ≤ pen(x)` for every table form: S; B and T with all tuples in
  band and with bands 1, 2 (the chains for what does not fit); W with window 2 and with
  everything in the window (then W *is* the envelope).  `E^s ≤ pen` is the sharp form of
  Proposition P: it is attained with equality.
* **V4** resolved `≤` the same form with the constants `ĉ^{J,s}` `≤` with P8's constants, pointwise.

**Controls that must fail** (`DEAD_ENDS.md` SD59: a check that cannot fail checks nothing).
**W1**: the *minimum* over the states in place of the value at the state (block tables; and
every site, pair, triple and window table).  **W2**: the value at a *wrong rotamer* (every
table rolled by one position along each state axis).  **W4**: shares that do not add up (the
banded forms without the parts moved from out-of-band tuples).

{GEN_VALIDATION}

**Reading.**  (i) *No violation of V1–V4 anywhere.*  At block level the resolved bound is
attained within 0.3–2 % in stage 2 (smallest ratios 1.0034–1.0192) and within 1–16 % in stage 1
(1.0092–1.1641): the statement is tight where it is tight, and never violated.  (ii) *Every
control fails at block level*, in both stages, in every row (`6·10²`–`2·10⁶` violations), and every
control on the tables fails in "envelope ≤ table" in every form and row.  (iii) **Against the
whole function the controls fail only in stage 2.**  In stage 1 the bound stays a factor
12–122 above the remainder at every state, so a table that is wrong by a factor two passes
`R ≤ pen` — the whole-function check, the one the brief names, has *no power* for stage 1 (0
violations of both controls in all eight rows); what validates stage 1 is V1 and "envelope ≤
table".  For stage 2 the whole-function check does detect W1 (931–73 096 violations) and W2
(1–1 884).  (iv) *How far the bound is from the truth where it matters:* in Boltzmann mean
under the true ensemble the stage-1 envelope is `4·10³`–`3·10⁵` times the remainder, the stage-2
envelope 255–880 times (the coordinator's logs give `9·10³`–`4·10⁵` for P8's constants on the same
instances).  (v) *What the enumeration cannot see:* interval enclosures, table allowances and
hulls are P3's and are inherited as in every certificate of the division; the check is of
the inequality chain built on them.
