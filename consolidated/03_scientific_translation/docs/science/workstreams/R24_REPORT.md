# Workstream R24 — adversarial referee of the results of the evening of 2026-11-26: the least ratio (item 86), the Ensemble division's statements on our instances and a sandwich as a class of ensembles (items 87–89), the split of the loss between groups (item 90)

*An internal review by an AI session, briefed to attack; **not external peer review**.  Work done 19:38–21:00 UTC
on 2026-11-26 (times read from the clock; running log in `experiments/science/ws_R24/NOTES.md`).  Objects: addendum
`INFERENCE_LIMITS_ADDENDA.md` items 86–90 (l. 3736–3877), SCI-MSG-0031, SCI-RES-0032, SCI-MSG-0032, and the scripts
and logs they cite.  Parts (13)–(18) of the addendum were not reviewed.  Four kinds of checking are kept apart:
**review** (re-derived on paper), **replication** (my own code written from the statements), **re-run** (the
coordinator's code run by me, output in my directory), **read only**.  Labels: [P] paper proof given here,
[N] numerical evidence, [K] in print (with the reading level), [H] heuristic.*

## 0. Verdict in ten lines

1. **No number of the five results is wrong**: 182 numbers of the tables (items 86, 87 (d), 88, 90 and the three
   messages) agree with the logs, and every number I replicated with my own code came out the same.
2. **Item 86 holds**; `λ_gs` and `λ_kink` are reproduced by brute force (Lys₅) and by a ratio iteration with my own
   `(min,+)` elimination (Lys₁₂, band 4: `15.497319`, `15.283061`); two more cases by the same iteration with the model's
   own pass.  "1 to 3 %" is four cases: a fifth, enumerated, gives 6.7 %; explicit models give any factor.  The
   "two-phase estimate" is no better than `λ_kink`.
3. **Item 87 holds**, and more than it says: E15 (a), (b) need neither symmetry nor the triangle inequality nor
   additivity; 87 (c) needs the reference to be a product **and** the envelope site-additive (false without either).
4. **Item 88 holds** (rule, counter pass, table); two unfavourable rows of the log are not in the table.
5. **Item 89 (b) is false as printed** (the "iff" lost the injectivity clause of their E13 (b)); "data pin only
   bang-bang members" has a four-state counterexample; "never identified" needs "by fewer than `|X| − 1` means".
6. **Item 89 (d): the W[1]-hardness does not follow** from the result cited; a sound certificate needs one counter.
7. **Item 90: the table is right, its reading is not.**  "The rest … is not a matter of joint laws" is refuted: it is
   exactly what the joint law of the minus-items **under the floor** gives, and pair laws under the floor recover
   it (Bonferroni): 0.415, 0.196, 0.538, 0.470 of the bracket on the four enumerated instances (in the order of the
   table), 0.498 ± 0.002 on Lys₁₂ at band 4.  "On LKSE:5 it is not [worth building]" reverses (0.47 of that bracket).
8. "Pair terms alone would take 0.61" at Lys₁₂, band 4, **is supported** (0.608 ± 0.001, my sampler, `6·10⁶` samples).
9. Critical findings: **none**.  Major: **three** (items 5–7 above).  Minor: **thirteen**.
10. Not checked: Lys₁₂ at band 7 (item 90 and item 86: logs read only), their Lean file, the 1981 source of the rule.

## 1. The statements as I understand them, with the hypotheses the texts leave implicit

**Item 86.**  Band model `m_λ = m₀ − λ·RND·pen` (`RND = 1 + 10⁻⁹`; the text writes `b = β·pen`, the script
`β·RND·pen`), `pen ≥ 0` a sum of window tables, `pen(anchor) = 0`.  `c(x) = ln Z(m₀) + βm₀(x) = −ln π₀(x) ≥ 0`.
(i) `G(λ) = max_x[λb − c] ≤ F(λ) := ln Z(m_λ) − ln Z(m₀)`; (ii) `λ_gs = min_x c/b`, so `F(λ) ≥ (λ − λ_gs)b*`; (iii) [M]
in four cases the scan's `λ_c` is 1.1–3.3 % below `λ_gs`.  *Implicit:* the tables are non-negative (asserted in
`first_order_recovery.py` l. 81, not in `floor_transition.py`; I checked: least entry 0, no state with a negative
penalty among 115 248 (Lys₅) and 4 000 random (Lys₁₂)); the minimum is over states with `b > 0`; "has lost" means
`ln Z(m_λ) − ln Z(m₀)`, which is at most the bracket; `λ_c` is defined by an occupancy and sampled; the same `β` in
both passes; `ln Z(m₀)` exact (an error `ε` in it moves `λ_gs` by `ε/b*`; with only an upper bound `L₊ ≥ ln Z(m₀)`
the valid form is `F(λ) ≥ −βm_λ(x) − L₊`).

**Item 87.**  Class `𝒫(π, d) = {μ : μ(y)π(x) ≤ e^{d(x,y)}μ(x)π(y)}` on a product space.  (a) their E15 (b) checked by
linear programmes; (b) one-sided envelopes: the polarised member is `∝ π e^{−d(·,a)}`; (c) the one-body marginal
vectors are the product of the one-site classes, hence a closed form for `b_min`; (d) numbers on Lys₅, LKSE:5.
*Implicit in (c):* `d` **site-additive** (the sentence of the item says only "a first-order class with a product
reference"); the data are the full one-site marginals, exact.

**Item 88.**  The range of `E ψ` over the box `e^{−βm₊} ≤ w ≤ e^{−βm₋}` by the threshold rule; for a count, from its
law under floor and ceiling.  *Implicit:* "exact range over the sandwich" is exact **for the class of all energies
between the two models** (no structure of `E` is used), **given** that the two models are a sandwich (workstream
P9's tables, the evaluation allowance), in double precision without interval control.

**Item 89.**  (a) the sandwich is `𝒫(√(lu), d)` with `d(x,y) = (D(x)+D(y))/2` (`x ≠ y`; `d(x,x) = 0` must be said: the
formula gives `D(x)` on the diagonal); (b) which members averaged data identify; (c) a stability bound; (d) a
certificate for sandwich + data and its cost.

**Item 90.**  With `Z_± = Z(m_±)`: lower end (LP) `Z(E) ≥ Z₊(1 + Σ_g⟨y_g⟩₊)`; upper end (UP) through
`C′ = Σ_g⟨z_g(1+y_g)⟩₊`; the loss in R19's sense `= [ln Z(m₊−s₊) − (LP)] + [(UP) − ln Z(m₋+s₋)]`, split into what
the joint law (pair laws) of the groups **under the ceiling** would recover and "the rest".

**Classes of the assumptions** (essential / proof technique / convenience / replaceable by a weaker quantitative
condition / removal changes the complexity / removal makes it false):

| statement | assumption | class | evidence |
|---|---|---|---|
| 86, `G ≤ F` | none beyond a common `β` | — | one term of a sum |
| 86, `λ_gs = min c/b`, `F ≥ (λ−λ_gs)b*` | `pen ≥ 0` | convenience: with signed tables read "min over `b > 0`"; the bound for the state `x*` stands | §2.1 |
| 86, identity `λ_gs − λ_kink = S_a/b*` | the anchor is the ground state of `m₀`, `pen(anchor) = 0`, same minimiser | essential for the identity, not for the bound | toy M3 |
| 86, "cheap" | band structure of the reduced penalty | **removal changes the complexity** (ground-state problem) | their own remark |
| 86, `ln Z(m₀)` exact | — | replaceable: an upper bound `L₊` suffices for the lower bound of `F` | §1 |
| 86 (ii), "1–3 % below" | entropy of the displaced phase `≪ c*` | not stated; **removal makes it false** (ratio 1.3 to 110 in toy M1; 2.7 at any length in M2) | `r24_item1_toy.log` |
| 87 (c) | product reference | **removal makes it false** | control: support functions differ by up to 0.40 |
| 87 (c) | site-additive envelope | **removal makes it false** | control: up to 0.75 |
| 87 (c) | symmetry; triangle inequality | not needed (convenience) | 6 one-sided classes, 4 of them without the triangle inequality imposed: `7·10⁻¹⁶` |
| 87 (c), closed form | data = the full one-site marginals, exact; `δ_i(s,t) > 0` where the log-ratio is positive | essential for "exact"; with error bars a one-site convex programme per site | proof |
| 87 (b) | "triangle inequality kept" | **not needed** for (a), (b); needed (through the centre only) for `μ*` to be a member | 44 412 programmes |
| 89 (a) | `l > 0` | essential (the pairwise form divides by `l`) | Walter's slide 2 says the same |
| 89 (a) | `d` a metric | not needed; it is a pseudo-metric when two states have `D = 0` | 24 boxes |
| 89 (b) | injectivity of the data on the face | **removal makes it false** (take `f ≡ 1`) | their E13 (b) |
| 89 (b), "never" | fewer than `dim 𝒫` independent data; strictly inside at **every** state | **removal makes it false** | counterexample H2 |
| 89 (c) | `γ > 0` | essential: as `γ → 0` the best constant diverges | H3 |
| 89 (d), equality | the data are attained by a member | essential for equality, not for soundness | duality |
| 89 (d), cost | exactness | replaceable by a quantitative condition: rounding `ε` costs `nε` in the end and one counter | H4 |

## 2. Findings

### 2.1 What holds as written (the line that decides each)

* **Item 86, the bound** [P; review].  `Z(m_λ) = Σ_x e^{−βm_λ(x)} ≥ e^{−βm_λ(x*)}`; divide by `Z(m₀)`: `F(λ) ≥ λb* − c*`.
  Valid for every `λ` and every state; `λ_gs` is where the best such line crosses zero.
* **Item 86, the numbers** [replication].  Lys₅, order 4, band 2: brute force over 115 248 states gives
  `λ_gs = 25.82545173`, `λ_kink = 23.9579008` at one state (4 of 5 sites off); Dinkelbach's iteration with my own
  elimination: the same in 3 passes, closing value `−2.8·10⁻¹⁴`; their bisection (re-run): `[25.825, 25.826]`.
  Lys₁₂, order 4, band 4: three starts, 3–4 passes each, `λ_gs = 15.497319` (theirs `15.49732`), closing value
  `−1.4·10⁻¹¹`; `λ_kink = 15.2830609` (theirs `[15.283, 15.284]`); the identity `λ_gs − λ_kink = S_a/b*` to 6 digits.
  Lys₁₂, order 3, band 7 and (LKSE)₃, order 3, band 7 (the same iteration with **the model's own** `(min,+)` pass,
  ratios evaluated by me from the tables): `λ_gs = 1.35557498` and `0.204863829` in 3 iterates each (theirs `1.355575`,
  `0.2048638`), closing values `2·10⁻¹²` and `0`; `λ_kink = 1.33494834` and `0.19937581` (inside their brackets); every
  single-site change of the minimiser has a larger ratio (91 of 91, 117 of 117).
* **Item 87 (a)–(c)** [review + replication], with the hypotheses of §1; **the closed form of `b_min` is the exact
  value of the programme of `INFERENCE_LIMITS.md` §9 for full one-site marginals**, product model and site-additive
  envelope: a member with the same marginals exists at `1.03·b_min` in 60 of 60 cases and at `0.97·b_min` in 0 of 60,
  and an explicit flow satisfies the inequality of Theorem 8 (c) at every state in 60 of 60.  *The flow* [P]: if
  `μ_i(t)π_i(s) > e·μ_i(s)π_i(t)` with `e = e^{bδ_i(s,t)}`, put `γ = π_i(t)e/(π_i(s)μ_i(t) − e·π_i(t)μ_i(s))` on the datum
  `E 1[x_i = s] ≤ μ_i(s)`, `α = (1 + γμ_i(s))/μ_i(t)` on `E 1[x_i = t] ≥ μ_i(t)`, and `F((s, x_{−i}) → (t, x_{−i})) = π_i(t)·α·π_{−i}(x_{−i})`:
  the inequality holds with equality where `x_i ∈ {s, t}` and reads `0 ≤ 0` elsewhere; above `b_min` no such `γ` exists.
* **Item 87 (d)** [replication]: the script computes the least site-additive envelope and the least scale is 1
  (every one of 5.6 million single-site pairs of Lys₅ satisfies the constraint, 579 attain it, 6 528 violate it at
  scale 0.99); `Στ`, `TV`, the ratio test reproduced to four digits.
* **Item 88** [replication]: my rule (best of the `N + 1` threshold vertices), brute force over all vertices and
  their `upper_end` agree on 170 boxes (`4·10⁻¹⁶`); my counter pass, enumeration and their `count_law` agree on 40
  random window models with pair and three-site tables (`3·10⁻¹²`, `6·10⁻¹⁵`).
* **Item 89 (a), (c), (d)-certificate** [review + replication]: the class is the box also when states have zero
  width; the stability bound holds; the certificate equals the linear programme for `r = 2, 3` data (`9·10⁻¹⁶`).
* **Item 90, the table** [replication]: all four enumerated rows digit for digit from the tables by my own
  enumeration; the criterion "`Σ_g P(S⁺_g > 0) ≤ 1` ⇒ (LP) is the optimum from the group laws" and **its converse**
  (exact programme over couplings: equality in 30 of 30 cases with sum ≤ 1, a gap of 0.059 to 3.1 in 30 of 30 with
  sum > 1); `C′ ≤ C₂ ≤ C″` pointwise (0 violations); each a valid input of Proposition A17.19 (the same change of
  measure applied to a pointwise smaller non-negative function); the solved upper end is the fixed point
  `ln(Z₋ − C·Z₊)` in closed form — `Z(m₋) ≥ Z(E) + C·Z(m₊)` in one line — hence decreasing in `C`, and the 60 or 400
  iterations of the scripts are not needed (equal to 2 000 iterations in 400 random cases).

### 2.2 Critical findings

None.  Every certified bound in the five results is a valid bound.

### 2.3 Major findings

**M1 [major] — item 90: "the rest … is not a matter of joint laws" is false; pair laws under the floor recover it,
and the advice drawn from the split changes.**
*Where:* item 90, title ("two parts, one of them not about groups"), (iii) and (iv) (l. 3850, 3869–3874);
SCI-MSG-0032 title, §1 second bullet ("No joint law of the items touches it"), §2 item 2 ("a lower bound of
`⟨z_g⟩_E` that uses the floor as well as the ceiling.  We have none"); SCI-RES-0032 §5 ("which no joint law of the
routed items removes"); `OPEN_PROBLEMS.md` D15 ("which no joint law removes"; open item (b)).
*The line that decides it.*  The reference against which "the rest" is measured is `ln Z(m₋ + s₋)`, and
`Z(m₋ + s₋) = Z(m₋)·⟨Π_g (1 − ζ_g)⟩_floor`, `ζ_g = 1 − e^{−βS⁻_g} ∈ [0, 1)` — an identity, which `group_coupling.py`
itself uses to compute that reference for Lys₁₂ (l. 147–152).  So the joint law of the minus-groups **under the
floor** gives the whole upper-side loss, and for `ζ ∈ [0,1]^G`, `Π(1 − ζ_g) ≤ 1 − Σζ_g + Σ_{g<h}ζ_gζ_h` (Bonferroni;
proof: induction with `Π ≥ 1 − Σζ`), so **pair laws under the floor give a valid upper end**
`ln Z(E) ≤ ln Z(m₋) + ln(1 − Σ_g⟨ζ_g⟩₋ + Σ_{g<h}⟨ζ_gζ_h⟩₋)` [P; sound on 400 random sandwiches × 3 energies, 0
violations; control: the first-order value violated 373 times].  What "the rest" is, exactly [P; identity to
`10⁻¹¹`]: `(Z₋ − C″Z₊) − Z(m₋+s₋) = Σ_x (e^{βs₋} − 1)(e^{−β(m₋+s₋)} − e^{−β(m₊−s₊)})` — the minus-slack weighted by
the width of the corrected sandwich: the price of the **route** through the true ensemble and the ceiling, which
exists to need means under one model only, not a limit of what joint laws give.
*Measured* (fractions of the corrected bracket; enumeration; Lys₁₂ from `10⁷` samples of the floor, bounded variables):

| instance | upper end, pair terms under the ceiling (their column) | **upper end, pair laws under the floor (Bonferroni)** | the put-back (all there is) | **single-group laws under the floor (comonotone)** | pair terms on both sides: theirs → with the floor |
|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | 0.104 | **0.415** | 0.415 | −0.386 (worse than (UP)) | 0.129 → **0.440** |
| Lys₅, order 4, band 3 | 0.019 | **0.196** | 0.196 | **0.180** | 0.047 → **0.224** |
| Lys₅, order 5, band 3 | 0.148 | **0.538** | 0.538 | **0.432** | 0.389 → **0.779** |
| LKSE:5, order 4, band 2 | 0.021 | **0.470** | 0.474 | **0.386** | 0.021 → **0.471** |
| Lys₁₂, order 4, band 4 | 0.441 ± 0.001 | **0.498 ± 0.002** | 0.4986 (R19's value) | −2.07 (useless at 56 groups) | 0.608 → **0.664 ± 0.002** |

The fifth column is a second, unasked result: the comonotone coupling is the largest value of `⟨Π(1 − ζ_g)⟩` that
the single-group laws allow (supermodular integrand; checked against the exact programme over couplings to
`2·10⁻¹⁶`), so `ln Z(m₋) + ln E_como Π(1−ζ_g)` is a valid upper end **from single-group laws under the floor
alone**, and on three of the four enumerated instances it lies below the driver's (UP) by 0.18 to 0.43 of the
bracket.  Cost of either: the held-site passes once more, on the floor model (and the laws, not only the means).
*Consequences.*  (i) "On LKSE:5 it is not [worth building]" (item 90 (iv)) reverses: 0.47 of that bracket by pair
laws under the floor, 0.39 by single-group laws.  (ii) The open item D15 (b) is answered.  (iii) The name of
SCI-MSG-0030 — "the loss between groups", recoverable by pair laws — was closer to right than its refinement.
(iv) The theory division's mixing inequality (D15 (a)) gives a *lower* bound of `⟨y_g y_h⟩`; the floor route needs
an *upper* bound of `⟨ζ_g ζ_h⟩₋` — the other mixing coefficient.
*Replacement text* (item 90 (iii)–(iv); the corresponding sentences of the two messages):
"(iii) The upper end carries the loss.  Through the ceiling (the route of Proposition A17.19) joint laws recover
0.02 to 0.53 of the bracket and leave a rest of 0.01 to 0.45: the price of that route, `Σ_x (e^{βs₋}−1)(e^{−β(m₋+s₋)} −
e^{−β(m₊−s₊)})/Z`.  Through the floor nothing is left: `Z(E) ≤ Z(m₋)⟨Π_g(1−ζ_g)⟩_floor`, and with pair laws under the
floor (Bonferroni) the upper end is recovered to within 0.004 of the bracket in all five cases measured.  (iv) With
pair laws on both sides — ceiling below, floor above — pair terms would take 0.44, 0.22, 0.78, 0.47 of the bracket on
the five-residue instances and 0.66 on Lys₁₂ at band 4 (band 7 not measured); from single-group laws under the
floor alone the comonotone bound already improves the upper end on three of four enumerated instances."

**M2 [major] — item 89 (b) is false as printed, and "data pin only bang-bang members" has a counterexample.**
*Where:* item 89 (b), l. 3834–3837: "a member is identified by the means of `Φ` inside the sandwich iff for some
`f ∈ span{1, Φ}` its energy is at the floor where `f` exceeds a threshold and at the ceiling below it: the ensemble
of the true energy, strictly inside its sandwich, is never identified by averaged data"; SCI-RES-0032 §4 (b), last
sentence: "…is never identified by averaged data; data shrink the identified set and pin only 'bang-bang' members".
*The line that decides it.*  Their Theorem E13 (b) (their report at `1a067b5`, l. 1006–1008, read with its proof,
l. 1024–1031; the proof uses polyhedrality only, so it applies to this polytope, metric or not): `μ` is determined
iff some `f ∈ span{1, Φ}` has a face of maximisers `F_f ∋ μ` **on which the data map is injective**.  The addendum
dropped the last clause; without it the right-hand side holds for *every* member (`f ≡ 1`: nothing above the
threshold, nothing below).  The message keeps the clause in parentheses and then concludes too much.
*Counterexample to "only bang-bang members"* [P; replication by linear programmes, `r24_item4.log` H2]: four
states, `l = (0.5, 0.5, 2, 1)`, `u = (1, 1, 3, 2)`, member `w = (1, 1, 2, 1.5)` — strictly inside the box at the fourth
state.  With `f = (2, 2, 0, 1)` the upper end is `t* = 1 = E_μ f` (the fourth state lies on the level set), and the
population of the fourth state fixes its weight: the range of every `μ(x)` over the members with these **two** means
is `0` (`≤ 6·10⁻¹⁷`).  Controls: with the first mean alone the ranges are 0.03 to 0.13; a member strictly inside at
every state is not identified by the same two functions (0.09) and is by three (complete data).
*What is true* [P]: a member strictly inside at **every** state lies in no proper face, so it is identified iff the
data determine every member of the class, i.e. iff they are `dim 𝒫` independent means (`|X| − 1` when `D > 0`
everywhere; `|X| − k` when `k ≥ 1` states have zero width).  A member strictly inside on a set `S` only can be
pinned by `|S| + 1` means (the example: `|S| = 1`, two means).
*Replacement text* (item 89 (b)): "By their E13 (b) and the threshold rule, a member is identified by the means of `Φ`
inside the sandwich iff for some `f ∈ span{1, Φ}` its energy is at the floor where `f` exceeds the upper end `t*` and
at the ceiling below it, **and the data determine the weights on the level set `{f = t*}`**.  A member strictly
inside its sandwich at every state is therefore not identified by fewer than `|X| − 1` independent means; a member
strictly inside on `s` states of one level set can be, by `s + 1` means (an example with four states and two means:
workstream R24, `r24_item4.log`, H2)."

**M3 [major] — item 89 (d): "W[1]-hard in their number by COMPLEXITY-RES-0001" does not follow, and "cheap for one
or two data and not in general" is not shown.**
*Where:* item 89 (d), l. 3844–3846; SCI-RES-0032 §4 (d), bold sentence (copied to the Complexity division).
*The line that decides it.*  Our own record of that result (`OPEN_PROBLEMS.md` D13; COMPLEXITY-RES-0001 itself is
not in the exports I had and was **not opened**): the reduction is from bin packing with "a threshold function"
of the *vector* of statistics, and the row ends "Open: … `φ` convex or slowly varying (**nothing follows**)".  The
certificate at a given multiplier needs `Σ u·h₊` and `Σ l·h₋` for the **one** additive statistic
`h = ψ − t − λ·(Φ − m)`: a convex function of a single linear form.  A counter per statistic is one way to get its
law, not a necessity.  *Rounding lemma* [P]: replace every site term of `h` by its value rounded up to a grid `ε`;
then `h ≤ h^↑ ≤ h + nε`, the threshold value is monotone and 1-Lipschitz in the sup-norm of the observable, so the
end certified with the law of `h^↑` — **one** counter with `n·range/ε` cells, whatever `r` — is sound and within
`nε` of the exact end; the minimisation over `λ ∈ ℝ^r` is convex with a subgradient (the threshold member's means of
`Φ`).  [N: three product models, 7 sites × 3 states, `r = 3`: sound, above the exact linear-programming end by
`0.15–0.18`, `0.02–0.03`, `0.006` for `ε = 0.05, 0.01, 0.002`, each `≤ nε`.]  What remains open is the cost of the
*exact* end (real multipliers make the values of `h` generic: a counting-knapsack question, not the bin-packing one).
*Replacement text:* "On a band model the two sums need the law of the one additive statistic `ψ − λ·Φ`.  Exactly,
for integer statistics, a joint counter gives it at cost `(nR)^{r+1}`; whether that exponent is needed for *this*
problem is open (the Complexity division's reduction uses a threshold in every coordinate, and says nothing for a
convex function of one linear form).  To accuracy `nε` one counter on a grid `ε` suffices for every `r`, soundly."

### 2.4 Minor findings

**m1 — item 90, the Lys₁₂ rows: the "±" covers one of four sampled inputs, the totals are 2 s.e. high, two columns
had no error bar.**  Deciding lines: `group_coupling.py` computes `C2_se`, `Cj_se` (l. 134–135) and never prints
them; its put-back `517.1286271 ± 1.3·10⁻⁵` against R19's `517.128653342 ± 1.2·10⁻⁶` and mine
`517.1286483 ± 8.7·10⁻⁶` (own sampler, `10⁷` samples; −0.58 s.e. from R19's).  With R19's put-back the row reads:
loss **0.666 ± 0.002** (not 0.708 ± 0.020), recoverable under the ceiling **0.637 ± 0.001** (0.644), pair terms
**0.608 ± 0.001** (0.614), the rest **0.029 ± 0.002** (0.064 ± 0.020).  The messages say in a note that R19's totals
give 0.03 and 0.01; the tables and item 90 print the noisy values.  *Are sample error bars right for heavy-tailed
variables?*  At Lys₁₂, band 4, yes: the 100 largest of `6·10⁶` samples carry at most 1.1 % of each second-order mean
and the batch scatter equals the within-sample estimate.  **On Lys₅ they are not**: `C′` from `2·10⁶` exact samples
of the ceiling is `0.02762 ± 0.00026` against the exact `0.03066` — **11.5 standard errors low** — and one sample
carries 68 % of `⟨q⟩`.  Under the floor the variables are bounded and every estimate is within 1.1 s.e.
*Replacement:* R19's totals in the table; a standard error on every sampled column; the sentence "a sample
standard error under the ceiling is an error bar only where the tail is checked (share of the largest samples)".

**m2 — item 86 (ii), SCI-MSG-0031 §2: the "two-phase estimate with both entropies" takes its second entropy from the
exact `ln Z` at the measured `λ_c` and is no better than `λ_kink`.**  Deciding line: `floor_ground_state.py` l. 123–125
(`S_d` at "measured lambda_c").  Identity: `λ_eq − λ_in = −ln(Z_d/Z_ref)(λ_in)/b*`; its fixed point is the root of
`F = ln 2 + λs₀`.  On Lys₁₂, band 4, with `S_d` read at `0.99λ_c` the estimate moves from −0.19 % to +0.43 % of the
exact `λ_c`; `λ_kink`, which needs one entropy and no scan, is within 0.3, 0.2, 1.3, 0.5 % in the four cases (their
logs) against 0.2, 0.4, 0.9, 1.1 % for the estimate; on Lys₅: −1.0 % against −1.8 %.  *Replacement:* "`λ_kink = λ_gs −
S_a/b*` lies within 0.2–1.3 % of the scan's `λ_c`; an estimate that adds the entropy of the displaced phase, read off
`ln Z` at the scan's own `λ_c`, does no better (0.2–1.1 %)."

**m3 — item 86, "1 to 3 %": a statement about four cases whose size is (an entropy)/`c*`.**  The texts say "four
cases … measured, not bounded"; what they do not say is what the number depends on.  A fifth case, exact by
enumeration (Lys₅, order 4, band 2): `λ_c = 24.199` (occupancy `n/2`), `λ_gs/λ_c = 1.067`; by the two other
definitions of the transition (`F = ln 2`; half the weight on penalised states) 9.6 % and 10.2 %.  In all five,
`(λ_gs − λ_c)b*` is 1.0 to 4.2 nats; the percentage is that entropy over `c*` (15 to 133 `kT`).  Explicit models
[P; enumeration, `r24_item1_toy.log`]: one reference state and `q` displaced states of cost `c₁`, penalty `b₁`:
`λ_gs/λ_c = (c₁ + ln(1 + qe^{−c₁}))/(c₁ − ln q)` — 1.000, 1.30, 1.85, 3.2, 10.3, 110 for `q = 1 … 20 000` at
`c₁ = 10`; `n` independent rotamer-like sites (`q = 6`, `c₁ = 3`): 2.70 at every `n`, with no sharp transition; a
penalty that does not vanish on the reference: `λ_gs ≪ λ_c` (so `λ_gs` is not an upper bound of `λ_c` either).
The exact `λ_c` of Lys₁₂, band 4, is `15.32735` (exact occupancy; inside the scan's sampled `[15.3203, 15.3281]`).
*Replacement* (after "the 3 % is measured, not bounded"): "it is `S/c*` with `S` an entropy of 1 to 4 nats here; a
displaced phase with an entropy comparable to its cost separates the two by any factor (a fifth, enumerated case:
6.7 %; independent sites: a factor 2.7)."

**m4 — item 86, method.**  The script never runs a pass at `λ = c*/b*`; "the least ratio" rests on 16 bisection
steps and samples.  Dinkelbach's iteration (`λ ← c(x_λ)/b(x_λ)`, `x_λ` the ground state at `λ`) reaches the same
number in 3–4 passes instead of 39 and ends with the exact test `G(c*/b*) = 0`.  Not an error.

**m5 — item 86 / SCI-MSG-0031 "what it is not": a rigorous two-sided statement of the same cost exists.**
(a) On a band model `F` is exact, non-decreasing and convex with `F(0) = 0`: one `(+,×)` pass at `λ₁` certifies
`F(λ) ≤ (λ/λ₁)F(λ₁)` for all `λ ≤ λ₁`, and the threshold `λ_t` (`F = t`) is a safety factor that is rigorous on both
sides at the price of the same number of passes (Lys₁₂, band 4: `F = ln 2` at `15.29303`).  (b) From `λ_gs` and the
model without penalty alone [P; checked by enumeration on Lys₅ and at 8 points on Lys₁₂, 0 violations; control —
the same without the second term — fails]:
`G(λ) ≤ F(λ) ≤ (λ/λ′)G(λ′) + ln Σ_x π₀(x)^{1−λ/λ′}` for `0 ≤ λ ≤ λ′` (each term `e^{λb−c} = (e^{λ′b−c})^{λ/λ′}π₀^{1−λ/λ′}`),
hence `λ_gs(1 − θ_t) ≤ λ_t ≤ λ_gs + t/b*` with `Σπ₀^{θ_t} = e^t` — one `(+,×)` pass of `m₀` at inverse temperature
`θβ` per trial `θ`.  It is rigorous and **loose**: the lower end is 0.15 (Lys₁₂) and 0.22 (Lys₅) of `λ_t` at
`t = ln 2`.  So "λ_gs > 1 certifies nothing" stands in practice; the statement to make is (a).  (The "certificate of
one state" offered to the Complexity division in SCI-MSG-0031 §2 is sufficient, not necessary: at the scan's `λ_c` the
four floors have lost 0.44 to 0.91 nats while `G` is −1.07 to −3.55 — no single state certifies it.)

**m6 — item 87 (b), SCI-RES-0032 §1 remark 1: "triangle inequality kept" is not needed.**  [P] Their proof of (a)
and (b) uses one family of constraints only: `w(s, x_{−i}) ≥ e^{−δ_i(s)} w(a_i, x_{−i})`.  So for **any** envelope `d`
and a product reference, with `δ_i(s) := max_{x_{−i}} d((s, x_{−i}), (a_i, x_{−i}))` and `μ*_{a,i} ∝ π_i e^{−δ_i}`:
`μ(x_i = a_i) ≤ σ_i` and `TV(μ, ⊗μ*_{a,i}) ≤ Σ_i τ_i`.  The triangle inequality (through the centre:
`d(x,a) ≤ d(x,y) + d(y,a)`) is what makes `μ*` a member, nothing else.  [N: 13 classes, 6 violating the triangle
inequality, 6 not site-additive, 90 centres, 44 412 programmes: largest violation `3·10⁻¹⁵`; `μ*` is not a member at
53 centres; control (`δ/2`) fails in 12 of 13.]  *Replacement:* "symmetry, additivity and the triangle inequality
are conveniences for (a) and (b): only the single-site costs into the centre enter; the triangle inequality makes
the polarised product a member."

**m7 — item 87 (c) and SCI-RES-0032 §2 ("That closes, for one-body data, the item …"): two essential hypotheses are
not in the sentences.**  The statement needs a product reference and a site-additive envelope (controls: 0.40,
0.75); a known part with couplings is not covered, which is the case §8 of `INFERENCE_LIMITS.md` is about.
*Replacement:* "…of a first-order class with a product reference **and a site-additive envelope** …"; "that closes
the item for one-body data **when the known part has no couplings**."

**m8 — item 87 (d), table row "(b) with the total variation itself, 232 centres: ≤ 0.015, 0, 0, 0".**  The row merges
two scans (the anchor on a grid from 0.005; 232 centres on a grid from 0.025).  Over **every** centre (exhaustive:
`TV(μ, μ*) ≤ TV(μ, ⊗μ_i) + Σ_i TV(μ_i, μ*_i)` prunes without loss) the test fires up to `b = 0.03` on Lys₅ with the
one-sided envelope (19 centres, margin `+0.016`), `0.02` symmetric, never on LKSE:5.  Applied to **sub-systems**
(valid: the marginal of a member on a set of sites is a member of the class on that set) it fires up to 0.05–0.075
(Lys₅) and 0.15 / 0.075 (LKSE:5) — always below the exact test on the same marginal.  The conclusion "adds
nothing as a falsification test" is fair; the numbers are 0.03 and 0.15, not 0.015.

**m9 — SCI-RES-0032 §2: "data see the typical strength of what is missing, not the worst-case constant" is a
statement about one-body data.**  The exact least scale consistent with the marginal on a set `S` of sites is the
ratio test on that marginal [P: `μ_S ⊗ π_{rest}` is then a member].  For two-site marginals it certifies **0.984**
(Lys₅) and **0.9992** (LKSE:5) of the true constant; one-site: 0.08–0.41.  (Exact marginals of rare pairs of states
are not measurable; the sentence is still about what Theorem 8 gives from which data.)

**m10 — item 88: "narrow three- to fourfold"; two rows of the log are not in the table.**  The factors in the table
are 2.0 to 4.4 (3.1 to 4.4 on Val₂₀ only); `sandwich_class_real.log` also has Val₈ at order 3 (site and pair form;
sandwiches 19 and 16 nats wide): published `[0, 8]`, exact range `[0.07, 8]` and `[0.88, 8]`, factors 1.01 and 1.12.
*Replacement:* "two- to fourfold (3.1–4.4 on Val₂₀, 2.0–2.8 on Val₈ and Lys₅); nothing where the sandwich is wide
(Val₈ at order 3: 1.01, 1.12)."

**m11 — item 89 (a) "ours": it is the definition that gives the density-ratio class its name.**  See §5.  The
"hub metric" is a reformulation; it is a metric iff at most one state has zero width, and their definition asks
for none.

**m12 — item 89 (c): the constant `1/γ` is valid and never attained; the best constant is explicit.**  The printed
proof is right (`Σw(t* − f) = Σ(w − v)(t* − f) ≥ γΣ|w − v|` because `v` solves the threshold equation and the signs agree
state by state; `TV ≤ ‖w − v‖₁/Σw` by the triangle inequality).  Sharper: [P]
`TV(μ, μ_f)·Σw = max_B[δ(B) − μ_f(B)δ(X)]`, `δ = w − v`, is sublinear in `δ` and the deficit `Σ|δ||f − t*|` is linear on
the cone of admissible `δ`, so the ratio is largest on a ray `δ = ±e_y`:
**`TV(μ, μ_f) ≤ C*(f)·(t* − E_μ f)`, `C*(f) = max_y (1 − μ_f(y))/|f(y) − t*| ≤ 1/γ`, attained by moving one weight.**
[N: 32 sandwiches, every subset, linear-fractional programmes: `7·10⁻¹³`; control `0.98·C*` violated in 32 of 32;
`C*γ` between 0.44 and 0.98.]  The "0.97" of the item is this.  As `γ → 0` the blow-up is real (the member that
differs at the state next to the threshold keeps its distance while its deficit vanishes: ratios 3, 8, 34, 49 at
gaps 0.30 to 0.02); what survives is the distance to the *face* of maximisers, with the gap of the other states.

**m13 — SCI-MSG-0032, "a refinement, not a correction".**  The numbers did not change; an attribution of cause
did ("the cross terms between groups … are two thirds"), and SCI-MSG-0030 calls such changes corrections.  After
M1 the question is moot: the refinement's own attribution needs a linked correction.

## 3. My own tests, with their controls

All in `experiments/science/ws_R24/`; every log named here reached its last line ("ALL DONE …; peak RSS …").
Run as `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B <script> <args> > <log>`.

| script → log | kind | what | result | control and its violations |
|---|---|---|---|---|
| `r24_sampler_test.py` | own code | my elimination and exact sampler against enumeration, 12 random models | `7·10⁻¹⁵`; pooled χ² z between −0.5 and +1.6 | sampler at `1.05β`: z from +88 to +207 |
| `r24_item1_enum.py K5 4 2` (35 s, 273 MB) + `rerun_floor_ground_state_K5_m4_w2.log` | replication + re-run | `λ_gs`, `λ_kink` by brute force, my Dinkelbach, the model's own pass, their bisection; exact `F`, occupancy; two-sided bound | all equal (`0` to 10 digits); `G ≤ F`: 0 of 151 | `ln Z(m₀)` wrong by `10⁻³`: seen (`1.7·10⁻³`); bound without its second term: 84 of 164 violated; `1.05 G + 0.001 ≤ F`: 45 violated |
| `r24_item1_band.py K12 4 4` (133 s, 1031 MB) | replication | Dinkelbach from three starts with my own `(min,+)`; exact `λ_c`; `λ_t`; Rényi bracket | `15.497319`, `15.2830609`; my `(+,×)` = theirs (`0`) | 91 of 91 single-site changes of the minimiser have a larger ratio; `F ≤ 0`: 8 of 8 violated |
| `r24_item1_ratio_model_pass.py K12 3 7`, `LKSE:12 3 7` (551 s, 1918 MB; 492 s, 974 MB; run together) | replication of the iteration, their pass | Dinkelbach with the model's own `(min,+)` pass; closing test | `1.35557498`, `0.204863829`; closing `2·10⁻¹²`, `0` | at `0.999λ_gs` the maximum is negative (−0.087, −0.133), at `1.001λ_gs` positive |
| `r24_item1_toy.py` | own | three explicit models | ratios 1.3–110; 2.70; `≪ 1` | `q = 1`: 1.000 |
| `r24_item2_synthetic.py` (86 s) | replication | E15 (a), (b) for arbitrary envelopes; 87 (c) by support functions; `b_min`; the flow | `3·10⁻¹⁵`; `7·10⁻¹⁶`; 60/60 and 0/60; 60/60 | `δ/2`: (a) fails in 12 of 13; not site-additive: 0.75; non-product reference: 0.40; reversed formula: contradicted in 46 of 50; flow impossible above `b_min`: 60 of 60 |
| `r24_item2_instances.py K5`, `LKSE:5` (54 s, 7 s) | replication (energies: the programme's evaluator) | least envelope; `Στ`, `TV`; (b) at every centre and on sub-systems; ratio tests on sub-systems | §2.1, m8, m9 | every single-site pair against `0.99δ`: 6 528 / 5 174 / 4 984 / 4 190 violations |
| `r24_item3.py` (1 s) | replication | rule; counter pass; table of item 88 | `4·10⁻¹⁶`; `3·10⁻¹²`; 54 numbers | floor and ceiling exchanged: 164 of 170 differ; pass at `1.02β`: 0.50; one typed digit changed: reported |
| `r24_item4.py` (13 s) | replication | hub class; counterexample; best constant; certificate; one counter | §2.3, m12 | envelope `D(x)+D(y)`: larger class in 48 of 48; `0.98C*`: 32 of 32; random multipliers below the programme: 0 of 240 |
| `r24_item5_enum.py` × 4 (10–37 s) | replication | every number of four rows; the rest; the floor route | §2.1, M1 | routed items doubled: 220 872 violations (Lys₅); first-order floor value as an upper bound: violated at 110 430 states |
| `r24_item5_synthetic.py` (1 s) | own | criterion and converse; comonotone = maximum; soundness of five upper ends | §2.1, M1 | first-order floor value: 373 violations |
| `r24_item5_sampled.py K5 4 2` (33 s) | validation of the next line | sampled estimators against my enumeration | floor side within 1.1 s.e.; **ceiling side fails** (m1) | — (it is the control of the estimator) |
| `r24_item5_sampled.py K12 4 4` (375 s, 1072 MB) | replication | the Lys₁₂ band-4 row, own sampler, `6·10⁶` + `10⁷` samples, batch errors | m1, M1 | `A`, `C′` against the driver's exact means: −0.47, +0.38 s.e. |
| `r24_numbers.py` | read + parse | 128 typed numbers against 12 logs | 0 disagree | one digit changed per table: reported, 3 of 3 |

Files in `not_cited/` (superseded first versions, each with a control that **could not fail**; see §6):
`r24_item1_enum_v1.py` and its logs, `r24_item2_instances_v1.py` and its logs.

## 4. The numbers against the logs

* **By script:** 44 numbers of the table of item 86 / SCI-MSG-0031, 60 of the table of item 90 / SCI-MSG-0032 /
  SCI-RES-0032 §5, 24 of SCI-RES-0032 §2 / item 87 (d), 54 of item 88 / SCI-RES-0032 §3: **182 numbers, 0
  disagreements** at the printed precision; the twelve logs parsed by `r24_numbers.py` and the three logs of
  `ensemble_checks/` (read by eye) reached their last line.
* **By reading** (item 87 (a), (b); SCI-RES-0032 §§1, 4; item 89; the text of items 86, 90 and of the messages):
  95 160 programmes, `3·10⁻¹⁵`, `2·10⁻¹⁵`, 4 of 4, 3 of 3, `4·10⁻¹⁵`, 39 of 40, 0.18–1.36, 0.07–0.25, 0.72–0.94,
  60 of 60, 168 boxes, `7·10⁻¹⁶`, 270, `4·10⁻¹⁶`, 45 of 45, `4·10⁻¹⁴`, 24, 18 of 18, 0.97, 30, 3 559–3 972,
  1 100–3 400, 39 passes, 514.9, 82–99.5 %, 0.7–1.4, 386, 609, 0–5 %, 1.3 nats, 28–99 %, 1 137–2 140: all agree.
* **Remarks.**  "514.9 of the 658.9 nats": the bound is on `ln Z(m₁) − ln Z(m₀) = 658.8` (`floor_transition` log:
  658.797); 658.9 is the bracket; the inequality stands either way.  `(λ_gs − λ_c)b* = 1.07` for Lys₁₂, band 4, uses
  the sampled `λ_c`; with the exact one it is 1.05.  The run of `floor_ground_state.py K12 4 7` took 1 070 s.
* **Not in any log** (read only, cannot be checked): "counted the minimiser itself as 488 violations" (first
  version of a check); the predictions and their times.

## 5. Prior art for item 4

Seven generic queries (listed in `NOTES.md`; nothing of the project in any query), seven addresses opened.
Reading levels: **[full]** opened and read; **[passage]** the cited passage read in the extracted text;
**[tool summary]** the page-fetch tool's summary of the page; **[search summary]**; **[memory]**.

| statement (header of `sandwich_class.py`) | status | where, reading level |
|---|---|---|
| (1) threshold rule | **in print** | Angers and Delampady, "Fuzzy sets in nonparametric Bayes regression", IMS Collections 3 (2008) 89–104, arXiv:0805.3209, **Theorem 5.1 [passage]**: over `Γ_DR = {π : L ≤ απ ≤ U}`, `sup ∫q₁π/∫q₂π` is the unique solution `λ` of `∫(q₁ − λq₂)⁺U + ∫(q₁ − λq₂)⁻L = 0` (their `q⁻ ≤ 0`), "see [6]" = DeRobertis and Hartigan, Ann. Statist. 9 (1981) 235–244, and "[8], Theorem 3.9" = Ghosh, Delampady, Samanta (2006).  **The 1981 paper itself was not opened** (the publisher's two addresses came back empty; not pursued).  A sample version: Wasserman and Kadane 1992, per Cozman's page **[tool summary]**; Geweke and Petrella, J. Bus. Econ. Statist. 16 (1998) 469–478 **[tool summary]**. |
| (2) the sandwich as a class of pairwise ratio constraints | **in print as the definition** | G. Walter, "Density Ratio Class Models and Imprecision", slides, 2 June 2014 **[full, 9 slides]**, slide 2: "If `l(ϑ) > 0 ∀ϑ`, then `M_{l,u} = {p : p(ϑ)/p(ϑ′) ≤ u(ϑ)/l(ϑ′) ∀ϑ, ϑ′}`, hence the name", citing DeRobertis–Hartigan 1981 and Berger, J. Statist. Plann. Inference 25 (1990) 303–328 (neither opened).  The reading as a first-order class with a "hub" metric: not found, and not looked for beyond this. |
| population bracket of a sandwich (their §4, not ours) | in print | Walter, slide 3 **[full]**: `P̲(A) = [1 + ∫_{A^c}u/∫_A l]^{−1}`. |
| (3) stability bound | **not found** (queries 3, 5, 7) | Related, different: a sharp bound of total variation by the Hilbert projective distance (the diameter of a constant-ratio class), Cohen and Fausti, arXiv:2309.02413 **[tool summary of the abstract]**; the explicit form `2 tanh(H/4)` is **[search summary]** only.  No claim of novelty follows from two queries. |
| (4) sandwich + averaged data | **not found** (queries 4, 6) | Generalised moment problems and their duality are classical **[memory, unverified]**; no source read that combines them with a density-ratio class. |

Addresses opened: (a) `projecteuclid.org/journals/annals-of-statistics/volume-9/issue-2/Bayesian-Inference-Using-Intervals-of-Measures/10.1214/aos/1176345391.full` (empty);
(b) `projecteuclid.org/download/pdf_1/euclid.aos/1176345391` (empty); (c) `arxiv.org/pdf/0805.3209`;
(d) `www.foundstat.statistik.uni-muenchen.de/_assets/pdf_oberseminar/140602_walter.pdf`;
(e) `www.cs.cmu.edu/afs/cs/user/fgcozman/www/Research/QuasiBayesian/Global/node5.html`; (f) `arxiv.org/abs/2309.02413`;
(g) `www.minneapolisfed.org/research/working-papers/prior-density-ratio-class-robustness-in-econometrics`.
For (c) and (d) the fetch tool returned the PDF as a file; I read it (extracted text; page images) from an isolated
scratch directory.  *Answer to the question of SCI-RES-0032 ("if (a) is known to you under another name"):* it is
the density-ratio class's own definition; and the rule's provenance can be upgraded from "memory" to "Theorem 5.1 of
Angers–Delampady (2008), attributed there to DeRobertis–Hartigan (1981), original not opened".

## 6. What I did not check; my own errors; tool actions declined; files

**Not checked.**  (1) Lys₁₂ at band 7 in item 90 (their run: 735 s, 2.84 GB; with my sampler above the limits);
everything said of it is read from their log.  (2) Item 86 for Lys₁₂, order 4, band 7: log read, not replicated
(their run: 1 070 s); for order 3, band 7 and (LKSE)₃ the `(min,+)` pass is theirs (only the iteration, the ratios
and the closing test are mine).  (3) The energies of Lys₅ and LKSE:5 are the programme's
evaluator; the sandwiches, tables, items and routes are the coordinator's objects, taken from the frames of his
drivers — I replicated what is computed *from* them.  (4) Part A of `thermal_union_bound.py` and part R of
`sandwich_class.py` were not re-run (my programmes are on other classes; the real table was compared with its
log).  (5) Their Lean file, their scripts, their theorems beyond E13 (b) and the proof of E15.
(6) COMPLEXITY-RES-0001 (not in my exports; M3 rests on our own record D13).  (7) DeRobertis–Hartigan 1981, Berger
1990, Wasserman 1992, Ghosh–Delampady–Samanta 2006: not opened.  (8) Item 84 and part (19) beyond what items 86 and
90 use; item 27 and part (13): not reviewed, as instructed.  (9) Whether a certificate with pair laws under the
floor is affordable at Lys₁₂ (1 540 pairs of groups): measured from samples only, not built.

**My own errors.**  (1) The first control of the two-sided bound ("half the Rényi term") **could not fail** — 0
violations, because the bound is that loose; replaced by "without the term" (84 violations); first version in
`not_cited/`.  (2) The first control of "the least scale is 1" on Lys₅ — random general pairs against `0.99·d` —
found 0 violations (random pairs do not come near the extreme); replaced by every single-site pair; first version
in `not_cited/`.  (3) My first test of my own sampler was an unpooled χ² (579 for 431 degrees of freedom; 273
sparse cells): an error of the test, pooled version in `r24_sampler_test.py`.  (4) Two slips caught before a run:
the sign of a derivative (occupancy), and a line that could have put `u < l` in a test box.  (5) The comonotone
bound of the Lys₁₂ row is computed batch by batch from empirical laws: biased; it only shows the bound is useless
there.

**Tool actions declined.**  The page-fetch tool returned empty content for the two Project Euclid addresses, and
declined to quote two abstracts verbatim (arXiv:2309.02413; the Minneapolis Fed page).  I did not work around
either: the 1981 paper is cited as not opened, the two abstracts as tool summaries.  No file or shell action was
declined.

**Nothing outside my directory was modified.**  The caches and the directories I was told not to touch
(`p9_verification`, `ws_P8`, `ws_P9`, `pi_inference/serine_helix_reach_cache`, `ws_P3`, `ws_P5`, `ws_P6`,
`ensemble_checks`: 1 719 files) have the same names, sizes and times after my last run as before my first
(`snapshot_before.txt`, `snapshot_final_protected.txt`).  In `pi_inference/` itself the coordinator's own new files
appeared while I worked (`product_threshold*`, `pair_term_mixing*`, `held_pair_*`), and
`pi_inference/__pycache__/nested_sampler.cpython-313.pyc` was rewritten at 20:43:51 UTC — at a time when none of my
processes was running (mine: until 20:40:16 and from 20:48:26, all with `python3 -B` and
`PYTHONDONTWRITEBYTECODE=1`); I report it because I cannot prove a negative beyond the times.

**Files** (`experiments/science/ws_R24/`): `NOTES.md`; `r24_common.py`; `r24_sampler_test.py`/`.log`;
`r24_item1_enum.py`, `r24_item1_enum_K5_m4_w2.log`, `rerun_floor_ground_state_K5_m4_w2.log`; `r24_item1_band.py`,
`r24_item1_band_K12_m4_w4.log`; `r24_item1_ratio_model_pass.py`, `r24_item1_ratio_model_pass_{K12_m3_w7,LKSEc12_m3_w7}.log`;
`r24_item1_toy.py`/`.log`; `r24_item2_synthetic.py`/`.log`; `r24_item2_instances.py`,
`r24_item2_instances_{K5,LKSEc5}.log`, `cache_E_{K5,LKSEc5}.npz`; `r24_item3.py`/`.log`; `r24_item4.py`/`.log`;
`r24_item5_enum.py`, `r24_item5_enum_{K5_m4_w2,K5_m4_w3,K5_m5_w3,LKSEc5_m4_w2}.log`; `r24_item5_synthetic.py`/`.log`;
`r24_item5_sampled.py`, `r24_item5_sampled_{K5_m4_w2,K12_m4_w4}.log`; `r24_numbers.py`/`.log`; `snapshot_*.txt`,
`git_status_before.txt`; `not_cited/` (two superseded scripts and their logs).

---

## Coordinator's note (appended 2026-11-26, after the hand-back of 21:00 UTC; the text above is the referee's, unchanged)

**Read:** the report in full (446 lines).  **Published as** SCI-MSG-0033 (linked corrections of SCI-MSG-0031,
SCI-RES-0032, SCI-MSG-0032), with correction notes at items 86–90 of the addendum.

**Checked by the coordinator, finding by finding.**

* **M1 — accepted; found twice.**  The brief had asked "could a joint law of the items under the floor recover
  it?".  An hour after writing the brief, while building exact pair terms for the theory division's question
  (THY-MSG-0018 §2), the coordinator arrived at the same route himself: `pi_inference/held_pair_exact.py`
  computes the second Bonferroni sum under the floor **exactly**, by passes with one and two held sites, and
  gives upper-end gains of 0.415, 0.196, 0.537, 0.471 on the four enumerated instances and 0.500 on Lys₁₂ at
  band 4 — the referee's 0.415, 0.196, 0.538, 0.470 (enumeration over groups) and 0.498 ± 0.002 (`10⁷`
  samples).  Neither knew the other's result; the referee's hand-back came while the coordinator's message was
  being written.  The identity the referee quotes is in the coordinator's own script (`group_coupling.py`
  l. 147–152), where it served as a reference and was not seen as a route — recorded in `DEAD_ENDS.md`.  What
  the referee measured from samples and "did not build" (its §6 (9)) is built: Proposition A17.23, addendum
  part (24).  The comonotone bound from single-group laws under the floor is the referee's and is not
  implemented.
* **M2 — accepted.**  The clause "and on which the data map `A` is injective" is in the Ensemble division's
  report at `1a067b5`, l. 1006–1008 (read by the coordinator).  The counterexample re-checked with linear
  programmes of the coordinator's own (`ensemble_checks/r24_m2_check.py`): `t* = 1 = E_μ f`; ranges `≤ 10⁻¹⁶` with
  the two means, 0.03–0.13 with one; a member strictly inside at every state is not identified (0.09).
* **M3 — accepted.**  Re-derived: every multiplier is sound by weak duality, the threshold value is monotone
  and 1-Lipschitz in the observable, so the rounded statistic gives a sound end within `nε` from one counter.
  COMPLEXITY-RES-0001 was not re-opened; our record of it (`OPEN_PROBLEMS.md` D13) says what the referee quotes.
* **m1–m13 — accepted with the referee's replacement texts.**  Re-derived by the coordinator: the toy formula of
  m3; the bracket of m5 (b) (each term `e^{λb−c} = (e^{λ′b−c})^{λ/λ′}π₀^{1−λ/λ′}`).  Read and not re-derived: m6–m10,
  m12 (the referee's programmes and numbers).  m1 is superseded for Lys₁₂ at band 4 by the exact computation.
* **Not re-run by the coordinator:** the referee's scripts (every log in `ws_R24/` ends in "ALL DONE"; the two
  superseded scripts are in `not_cited/`, as its §6 says).  **Not opened by the coordinator:** the two sources
  that decide the prior-art question (Angers–Delampady, Theorem 5.1; Walter's slides) — the reading levels are
  the referee's.

**Tool actions.**  The referee reports that the page-fetch tool returned empty content for two publisher
addresses and declined to quote two abstracts verbatim, and that it did not work around either.  Neither did
the coordinator.  No file or shell action was declined.

**The byte-code file** `pi_inference/__pycache__/nested_sampler.cpython-313.pyc` rewritten at 20:43:51 UTC is the
coordinator's: at that time only his own runs were active in that directory.  It is a cache, ignored by git.
