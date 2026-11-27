---

## 4. The verdict on levers, in numbers (step 4 of the brief)

### 4.1 Two kinds of numbers: brackets from the pipeline, and first-order estimates

**(i) The existing pipeline, fed with the new constants** (`p8_12_certificate.py`; a
demonstration beyond the brief).  Nothing in the pipeline is mine: the band models, the transfer
matrix and the exact sampler are P3's (`pwmodel`), the site / banded-pair / banded-triple penalty
forms and their floating-point allowances are P6's (`p6lib`, Lemmas A, A′), the models with exact
in-window evaluated terms and the two-window triple form are the coordinator's
(`pi_inference/window_model.py`); all imported read-only.  Mine are the per-subset constants
`ĉ_T`, from which the site sums `S_i`, pair sums `G_ij` and triple sums `H_ijk` are formed by plain
summation, and the driver.  The pipeline needs one hypothesis about the constants,
`|g − I_{m−1}g|(x) ≤ Σ_{T ⊆ S(x), |T| = m} ĉ_T` — Theorem AH (§3.3), a paper proof validated in §3.4.

<!--T:T10-->

*Reading.*  (The (LKSE)₃ row is discussed in §4.3.)  On the enumerated instances the sandwich
`m₋ ≤ E ≤ m₊` holds at **every** state and
the exact `ln Z` lies in every bracket (Lys₄ at order 4; Lys₅ at orders 4 and 5: 1.00 / 0.175 /
0.027 and 0.019 / 0.0031 / 0.00044 nats for the site / banded-pair / banded-triple form).  For
**Lys₁₂ at order 4** the brackets are 11.1 / 4.38 / **2.81** nats with band 6 (the band of the
coordinator's table) and 10.7 / 3.27 / **1.56** nats with band 7; the sandwich holds at the 1 600
Gibbs states and at 2 000 exact samples of the floor.  For **Lys₁₂ at order 5** (ball
1 621 056) they are **0.81 / 0.47 / 0.45 nats with band 6 and 0.60 / 0.22 / 0.19 nats with band
7** — below one nat in every share form; the sandwich holds at the 1 600 Gibbs states and at
2 000 exact samples of the floor, which now stays where the ensemble is (1.2 side chains off
the anchor on average, against 7.8 at order 4).

*What part of a bracket is not the constants.*  Line (3b) of each log gives the width of the
same models with **all penalties set to zero** (not a sandwich): what the pipeline's reduction of
the evaluated terms that do not fit the band, and of the pairs beyond it, costs by itself.  For
Lys₁₂ with band 6 it is 0.354 nats at both orders — the helix's triples `i, i+3/4, i+7` carry 30 %
of the third-order terms (§2.2) and have span 7; with band 7 it is 0.141 nats at both orders.  At order 5 the
rest of each bracket, 0.46 / 0.12 / 0.09 nats with band 6, is what the first-order estimates
below predict for the constants (0.47 / 0.12 / 0.094).  **At order 5 the certificate of Lys₁₂ is
limited by the band, not by the constants any more.**

**(ii) First-order estimates** (`p8_07_estimate.py`).  Addendum A17 (16), Lemma A17.16: with exact
evaluated terms the bracket of a sandwich `m_∓ = [f + I_{m−1}g] ∓ pen` is
`ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩`, `⟨·⟩` the true ensemble, i.e. `2β⟨pen⟩` to first order.  The script
evaluates both expressions on a Gibbs sample of the true ensemble for penalties built from
per-subset constants.  The sample (`p8_05_gibbs.py`) is my re-implementation of the coordinator's
heat-bath sampler with its seed; **it reproduces the coordinator's sample exactly** (largest
difference of an off-anchor frequency 0.0 for all four peptides), and with P3's constants my
first-order numbers reproduce the coordinator's "refined rule" (Lys₁₂: 146 / 39.7 / 30.8,
30.9 / 9.01 / 7.25, 4.80 / 1.54 / 1.32 for site / banded pair / banded triple at orders 4, 5, 6;
(LKSE)₃: 911 / 245 / 100, 278 / 75.7 / 33.5, 72.1 / 20.5 / 10.1).  **Nothing in this table is a
certificate**; the sample is uncertified; and both estimates are *lower* estimates of the
bracket wherever the penalty reaches several `k_BT` (A17 (16), item 44): **for Lys₁₂ at order 4
the estimates said 1.14 (first order) and 1.32 (exponential, on the sample), and the pipeline
gives 2.81** — the floor `m₋` delocalises (7.8 of 12 side chains off the anchor on average in
its exact samples, 1.2 in the true ensemble), onto states the Gibbs sample of the true ensemble
never visits.  The third number in each cell, the largest `β·pen` on the sample, says when to
distrust the first two.

<!--T:T7-->

Rows "exact3", "exact4": the **exact** anchored terms of that order in the anchor context in
place of bounds (§2.3) — a measurement of what an ideal certificate would pay, not valid
constants.  The last two columns estimate what an *occupancy-aware allocation* would give: every
subset is charged in full to the in-window sub-tuple of its sites that is least often off the
anchor (any choice is valid: `[T ⊆ S(x)] ≤ ∏_{i∈U} s_i` for `U ⊆ T`).  I wrote them before the
coordinator told me that this is the theory division's Proposition 11.18f (proposed, unrefereed,
and the coordinator's to run); they are a first-order estimate, not a run of that proposition,
and where the constants are large they are meaningless (Leu₁₂: "0", because the sites charged
are never off the anchor in the sample — exactly the situation in which a floor delocalises).

### 4.2 The four levers

**(a) How much could a sharper sign-blind bound gain at most?**  The sign-blind floor of §1 is
3.2–6.8 times the true remainder for lysine (13–37 for the patterned sequence at orders 3–5).
P3's `Γ_m` was 21–490 times that floor on the enumerated lysine helices (25–470 for the
patterned sequence; table T1b), so
that much was to be had in principle.  The state-wise form takes a factor 4.0–24 of it on the
enumerated lysine instances (2.3–4.3 on LKSE:4 and LKSE:5; 2.8–12.5 on LKSE:6 with the
pair-wise variant) and 20–170 at twelve residues.  What is left between the new bound and the
floor found, on Lys₅ at orders 3, 4, 5 (`logs/bc_K5_H_0.70.log`, `out/sb_K5_H_0.70.json`): a factor
5.4, 9.8, 20 in all; of this 3.4, 4.3, 5.5 lies between the largest remainder of a sign pattern
found and the pair-by-pair optimum (unknown which side is real: the least sign-blind bound is
only bracketed), and 1.6, 2.3, 3.7 between the pair-by-pair optimum and the new bound.  Against
the exact constants of its own blocks — the least value a block-wise bound can have — the new
bound is 2.5, 4.3, 8.9 times larger: this is the remaining slack of the chain-rule step
(Lemma T), growing with the order.

**(b) What does step 3 gain?**  As posed — the factor `e^{−r²/4B_aB_b}` for far pairs — nothing: P3's
bound has it, and pairs that are far in every state carry at most 4 % of the bound.  The
state-wise maximum (P3's own theorem without the merging step of its closed form) together with
Theorem AH gains **20, 60, 172 for Lys₁₂** at orders 4, 5, 6; 6.3, 13, 30 for (LKSE)₃; 1.6, 1.6,
1.8 for Ser₁₂; 1.1 for Leu₁₂ (table T6).

**(c) What does one more order cost and buy?**

| peptide | ball at orders 4, 5, 6 (evaluations of `g`) | time on this machine at the measured rate | `Γ_m`, new constants (`k_BT`) | fall per order: new; P3 | first-order bracket, banded triple form, new constants |
|---|---|---|---|---|---|
| Lys₁₂ (276 atoms) | 96 366; 1 621 056; 19 307 568 | 0.9–1.2 ms each: 1.4–1.9 min; 24–31 min; 4.7–6.2 h | 34.0; 2.40; 0.136 | 14, 18; 4.7, 6.2 | 1.14; 0.094; 0.0059 |
| (LKSE)₃ (213 atoms) | 181 268; 3 471 783; 44 857 302 | 0.5 ms each: 1.6 min; 30 min; 6.5 h | 296; 42.8; 4.87 | 6.9, 8.8; 3.3, 3.9 | 9.9; 1.72; 0.233 |

(Rates: 247 200 evaluations in 218 s for Lys₁₂ and 309 600 in 161 s for (LKSE)₃ in the Gibbs
runs, P2's block evaluator on one core; the order-5 ball of Lys₁₂ took 1 884 s in two legs,
1.16 ms per evaluation, on a machine with a load of 5–6 on four cores:
`logs/ballrun_cert_K12_H_0.70_m5_w6_SAb.log`.)  An order costs a factor 12–19 in evaluations and buys a
factor 14–18 in the constants for lysine (it bought 5–6 with P3's constants), 7–9 for the
patterned sequence.

**(d) What does the sandwich sampler tolerate?**  For the theory division's Proposition 11.113 as
P6 implemented it, `N` accepted points give a bracket of width at most `(e^D − 1)·2√(ln(2/δ)/(2N))`
inside a deterministic bracket `D` (P6_REPORT §4A): for width 0.1 nats at `δ = 0.05`,
`N = 738·(e^D − 1)²` — 2 200 points at `D = 1`, 30 000 at `D = 2`, 270 000 at `D = 3`, `2·10⁶` at
`D = 4` (table T10, last line); a draw from the floor is accepted with probability `1 − e^{−D}` on
average and only accepted points are evaluated, so `N` is also the number of new evaluations of
`g`, at most.  It tolerates a deterministic bracket of two to three nats, not seven.  Inside the
2.81 nats of Lys₁₂ at order 4 (band 6) it needs 180 000 points — about three minutes of
evaluations here, less than twice the ball of that order; inside the 1.56 nats of band 7,
10 500 points.  Not run by me.  (The coordinator informs me that the
theory division's Proposition 11.113a, a nested sampler, changes this arithmetic; it is
unrefereed and not run here.)

### 4.3 Which combination brings Lys₁₂ on the helix below one nat deterministically?

* **The new constants at order 5, with any of the three share forms** (levers (b) and (c)
  together): **0.81 / 0.47 / 0.45 nats** (site / banded pairs / banded triples; band 6, as in the
  coordinator's table) and **0.60 / 0.22 / 0.19 nats with band 7** (table T10); ball 1 621 056
  evaluations, 24–31 minutes on one core here.  With P3's constants the same forms were at 31,
  9.0, 7.3 nats to first order.  Neither lever alone does it: the new constants at order 4 give
  2.81 nats; P3's constants at order 5 seven or more.

* **At order 4** (ball 96 366) the new constants give 2.81 nats with the banded triple form and
  band 6, and 1.56 nats with band 7 — not below one nat with P6's uniform shares.  What would
  bring it down, none of it run by me: an allocation that does not send the shares of far
  triples back to the pairs of the three mobile N-terminal residues (off the anchor 39, 23,
  21 % of the time, the other nine 2–6 %; the theory division's Proposition 11.18f, the
  coordinator's to run — my first-order estimate of such an allocation is 0.012–0.015 nats, to
  be distrusted for the reason given in §4.1); penalties resolved by rotamer state (request
  P8-E4); or — not deterministic — the sampler inside the 1.56 nats: 10 500 accepted points for
  0.1 nats at confidence 0.95, about 107 000 evaluations with the ball, a fifteenth of what
  order 5 costs.
* For **(LKSE)₃** no deterministic combination below one nat at an order I can afford.  With
  the new constants at order 5 (ball 3 471 783, band 7) the pipeline gives 22.8 / 11.0 / **4.49
  nats** (table T10) — above the estimates (1.72 to first order, 2.8 exponential), because its
  floor delocalises like that of Lys₁₂ at order 4 (8.9 side chains off the anchor in the
  floor's samples, 2.8 in the ensemble).  At order 6 the first-order estimate is 0.23 nats with
  a ball of `4.5·10⁷`; not run.  What is left of its constants is the apolar part (§1, finding 7):
  they are still 119 times the exact four-body terms at twelve residues (§2.3), where lysine's
  are 34 times.

**What an ideal certificate would need** is in §2.3.
