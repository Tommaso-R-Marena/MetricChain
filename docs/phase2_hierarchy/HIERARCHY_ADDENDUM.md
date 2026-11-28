# Phase II — the adaptive hierarchy: addendum on hidden partitions

*Division: Phase II, adaptive hierarchy (branch `research/phase2-adaptive-hierarchy`).  Written 2026-11-28
by the same AI session as `HIERARCHY_REPORT.md`, after that report had gone to its reviewer.  Status
labels as there: **[V]** machine-checked, **[P]** paper proof in this file, **[N]** numerical evidence
(script named), **[K]** quoted from the archive, **[C]** conjecture.  Nothing here has been read by a human
expert.  §A6 says what has and has not been checked by another AI session; the corrections that the
review of this addendum led to are marked where they occur.*

---

## A0. What this adds

The report proves that three rounds reach the optimal exponent `h` on *block-radial* energies — blocks
known, centres hidden — and lists as open (its §8, problems 1 and 2) the cases in which the algorithm is
not told the block structure: hidden partitions, blocks that the profile couples, centres that overlap.
The proof of Lemma B does not cover them (Remark 2 of §A2 says where it breaks).  This addendum closes
them, for every bounded number of classes.

| | statement | status |
|---|---|---|
| **Theorem P** | *The relaxation principle for nested hidden partitions.*  Types are vectors of densities on arbitrary classes of coordinates.  If a `u`-Lipschitz profile depends only on the cell means of a partition `𝒢₁` on the types whose densities all lie in `[κ, 1−κ]`, and only on the cell means of a finer partition `𝒢₂` on everything a batch of `e^{nθ}` points that knows `𝒢₁` sees, then every type that a batch knowing `𝒢₂` does not see carries at most `e^{n(h−θ)}` times the largest mass on the first set.  No assumption on the classes, their number, their sizes, or the way the partitions cut them.  (An algorithm needs `θ ≥ h` to see the first set.) | [P] §A2, complete (a statement about functions on a cube of densities); proof re-read line by line by a reviewer, no error found; [N] §A3: the chain rebuilt from the definitions on random instances (author 20 000, reviewer 12 000), extremal profiles on lattices by brute force (author and reviewer, independent codes); arithmetic [V] |
| **Theorem H6** | **Three rounds suffice for every energy with a bounded hidden symmetry type.**  `HP_m` := the energies `ψ ∈ L_u` that are functions of the numbers of ones in the classes of an *unknown* partition of the coordinates into at most `m` classes.  For every `u`, `m`, `η`, `δ` there is a three-round algorithm (R3P, §A4) that for all large `n` and every `ψ ∈ HP_m` returns `Â` with `(δ/2)Â ≤ A(ψ) ≤ 4Â` with probability `≥ 1 − δ` from at most `e^{n(h+η)}` evaluations.  Hence `c_3(HP_m) = h`. | [P] §A4–A5, complete for `n ≥ n₀(u, m, η, δ)`; proof re-read step by step by a reviewer, who also executed step (e) literally with exact binomials; no error found; lower bound [K: Theorem 11.25, V] |
| **Hierarchy** | `HP_m` contains: block-radial energies with *unknown* blocks and centres (`BR_m ⊂ HP_{2m}`), every function of the distances to `r` hidden centres with arbitrary overlaps (`⊂ HP_{2^r}`), and all their compositions.  For `m ≥ 4` the round hierarchy on `HP_m` has exactly three levels, `c_1 = a > c_2 > h = c_3 = c_4 = …`. | corollary, §A5 |
| **Barrier** | **A family that separates three (or any fixed number `≥ 3` of) rounds from unrestricted adaptivity cannot have bounded hidden symmetry type**: not finitely many hidden centres in any overlap pattern, not finitely many hidden blocks, merged or nested in any way.  The proof tolerates `m = m(n)` classes as long as `m⁵ log n = o(n)`. | corollary, §A5 |

**What is still not established.**  `c_3(u) = h(u)` on all of `L_u` (Conjecture H5 of the report).  A
general member of `L_u` has no hidden symmetry (`m = n`); the algorithm R3P samples `(n+1)^{O(m²)}` shells
and its guarantee has an error term `O(m⁵ log n)` in the exponent.  What Theorem P contributes to the
general question is that its inequality is *dimension-free*: the bound `h − θ` does not depend on the
number of classes.  The two-round exponent of `HP_m` is not determined either.

---

## A1. Setting

*Classes and types.*  `C` a finite set (*classes*), weights `φ_c > 0`, `Σ_c φ_c = 1`.  A *type* is
`z ∈ [0,1]^C`.  `f(t) = ln 2 + t ln t + (1−t) ln(1−t)` (`= KL(t ‖ ½)`), `r(z) = Σ_c φ_c f(z_c)` the *rate*,
`‖z − z′‖ = Σ_c φ_c |z_c − z′_c|`.  A function `F` of types is *`u`-Lipschitz* if `|F(z) − F(z′)| ≤ u‖z − z′‖`.
(On the cube: the coordinates are split into classes of sizes `nφ_c`, `z_c` is the density of ones of a
point in class `c`, a uniform point has type `z` with probability `e^{−n r(z) + O(|C| log n)}`, and an energy
`ψ = nF(type)` is in `L_u` iff `F` is `u`-Lipschitz on the lattice of types.)

*Partitions.*  For a partition `𝒢` of `C`, `avg_𝒢 z` replaces every `z_c` by the `φ`-weighted mean over the
cell of `c`, and

    cost_𝒢(z) := r(z) − r(avg_𝒢 z) = Σ_c φ_c KL(z_c ‖ (avg_𝒢 z)_c) ≥ 0.

A batch that can distinguish the cells of `𝒢` but not the classes inside a cell samples, for every vector
of cell counts, uniform points with these counts; it meets the type `z` with probability
`e^{−n·cost_𝒢(z) + O(|C| log n)}` per point.  So with `e^{nθ}` points per count vector it *sees*
`{cost_𝒢 ≤ θ}`.

Facts used (`𝒢′` refines `𝒢`):

* **(C1) chain rule.**  `cost_𝒢(z) = cost_𝒢(avg_{𝒢′} z) + cost_{𝒢′}(z)`; in particular `cost_{𝒢′} ≤ cost_𝒢` and
  `r(avg_𝒢 z) ≤ r(z)`.  (Because `avg_𝒢 avg_{𝒢′} = avg_𝒢`.)
* **(C2)** `‖avg_𝒢 z − avg_𝒢 z′‖ ≤ ‖z − z′‖`.  (Not used below.)
* **(C3) the price of a step towards ½.**  `p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{−u}))`, `κ = Λ₁/u`, `h = f(κ)`;
  `p_u < κ < ½`.  Put `χ(t) := f(t) + u·min(t, 1−t) − Λ₁`.  Then `χ ≥ 0`, `χ(p_u) = 0`, `χ(κ) = h`, `χ` is
  nonincreasing on `[0, p_u]`, nondecreasing on `[p_u, ½]`, and symmetric about `½`.  If `t′` lies between `t`
  and `½` then `f(t′) − f(t) + u|t′ − t| = χ(t′) − χ(t)`.
  (On `[0, ½]`: `χ′ = ln(t/(1−t)) + u`, zero at `p_u`, and `f(p_u) + u p_u = Λ₁`; `χ(κ) = f(κ) + uκ − Λ₁ = h`;
  `κ < ½` because `2 < e^{u/2} + e^{−u/2}`; `κ > p_u` because `Λ₁ − u p_u = f(p_u) > 0`.)
* **(C4) filling a cell from below.**  For a cell `g` and a level `λ` let `z^λ := max(z, λ)` on `g`, and
  `T_g(z) := Σ_{c∈g} φ_c KL(z_c ‖ mean_g z)`.  Then `λ ↦ T_g(z^λ)` is nonincreasing.  (`T_g(z) =
  min_q Σ_{c∈g} φ_c KL(z_c‖q)`.  Let `μ(λ)` be the mean of `z^λ`; `μ(λ) ≥ λ`.  For `λ < λ′ ≤ μ(λ)` the classes
  that move go from below `λ′` up to `λ′`, towards `μ(λ)` without passing it, so
  `T_g(z^{λ′}) ≤ Σ φ_c KL(z^{λ′}_c ‖ μ(λ)) ≤ T_g(z^λ)`.  If `μ(λ) = λ` all classes coincide and `T_g` is `0`
  from there on.  `T_g(z^λ)` is continuous in `λ`; the two cases give monotonicity on the whole line.)
  The same holds for `min(z, λ)` and decreasing `λ`.

*Clipping.*  `clip_ℓ(t) := min(max(t, ℓ), 1−ℓ)` for `0 ≤ ℓ ≤ ½`, applied coordinatewise.
`𝒦 := [κ, 1−κ]^C` (the *core*): every type in `𝒦` has `r ≤ h`, hence `cost_𝒢 ≤ h` for every `𝒢`.

---

## A2. Theorem P

> **Theorem P.**  Let `𝒢₁`, `𝒢₂` be partitions of `C`, `𝒢₂` a refinement of `𝒢₁`; write `avg_i`, `cost_i`.
> Let `θ ≥ 0` and let `F` be `u`-Lipschitz with
>
> * (H1) `F(z) = F(avg₁ z)` for all `z ∈ 𝒦`,
> * (H2) `F(z) = F(avg₂ z)` for all `z` with `cost₁(z) ≤ θ`,
>
> and put `ν_𝒦 := sup_{z∈𝒦} (−F(z) − r(z))`.  Then for every type `y` with `cost₂(y) > θ`
>
>     −F(y) − r(y) ≤ ν_𝒦 + h − θ.        **[P]**

In words: `𝒢₁` is what the first batch learned, `𝒢₂` what the second learned; (H1), (H2) say that each
batch saw nothing finer than what it learned; the conclusion bounds the mass exponent of everything the
third batch — which samples the shells of `𝒢₂` — does not see.  `𝒦` is seen by a blind batch of `e^{nh}`
points, so `ν_𝒦` is at most the largest mass exponent that any batch sees.

*Proof.*  Write `T := cost₂` and `Q(z) := cost₁(avg₂ z)`; by (C1), `cost₁ = Q + T`.

*Step 1: three points.*  For `s ∈ [0,1]` let

    e(s) := clip_{sκ}(y),      m(s) := avg₂ e(s),      m′(s) := clip_κ(m(s)),      Φ(s) := T(e(s)) + Q(m′(s)).

`Φ` is continuous and `Φ(0) ≥ T(y) > θ`.  At `s = 1`: `e ∈ 𝒦`, so `m ∈ 𝒦`, `m′ = m`, and
`Φ(1) = cost₁(e) ≤ r(e) ≤ h`.  *Main case: `Φ(1) ≤ θ`* (always so when `θ ≥ h`).  Fix `s` with `Φ(s) = θ` and
write `ℓ = sκ`, `e`, `m`, `m′`.  (The other case is treated at the end.)  Define `e′` cell by
cell (`g ∈ 𝒢₂`, `m_g` the mean of `e` on `g`): if `m_g ∈ [κ, 1−κ]`, `e′ = e` on `g`; if `m_g < κ`,
`e′ = max(e, λ_g)` on `g` with the level `λ_g ≤ κ` at which the mean on `g` equals `κ` (the mean of `max(e, λ)`
is continuous and nondecreasing in `λ`, equals `m_g` for small `λ` and is `≥ κ` at `λ = κ`); if `m_g > 1−κ`,
symmetrically `e′ = min(e, λ_g)` with mean `1−κ`.  Then

    avg₂ e′ = m′,      ‖e − e′‖ = ‖m − m′‖,      T(e′) ≤ T(e)

(inside a cell all classes move in the same direction; (C4)).

*Step 2: the two batches saw the anchors.*  `cost₁(e′) = T(e′) + Q(m′) ≤ T(e) + Q(m′) = θ`, so by (H2)
`F(e′) = F(m′)`.  `m′ ∈ 𝒦`, so by (H1) `F(m′) = F(p)` with `p := avg₁ m′ ∈ 𝒦`, and `−F(p) ≤ ν_𝒦 + r(p)`.

*Step 3: the chain.*  By the Lipschitz property and the triangle inequality,

    −F(y) ≤ −F(e′) + u‖y − e‖ + u‖m − m′‖ = −F(p) + u‖y − e‖ + u‖m − m′‖ ≤ ν_𝒦 + r(p) + u‖y − e‖ + u‖m − m′‖.

Subtract `r(y)` and insert `r(e)`, `r(m)`, `r(m′)`:

    −F(y) − r(y) − ν_𝒦 ≤ [r(e) − r(y) + u‖y − e‖] + [r(m′) − r(m) + u‖m − m′‖] − [r(e) − r(m)] − [r(m′) − r(p)]
                       =: Π₁ + Π₂ − T(e) − Q(m′) = Π₁ + Π₂ − θ.

*Step 4: the prices, cell by cell.*  `Π₁ + Π₂ = Σ_{g∈𝒢₂} A_g`, where `A_g` collects the classes of `g` in `Π₁`
and the cell `g` in `Π₂`.  We show `A_g ≤ φ_g h` (`φ_g` the weight of `g`).
The clipping moves the classes with `y_c < ℓ` to `ℓ` and those with `y_c > 1−ℓ` to `1−ℓ`, towards `½` and
not beyond `κ`; by (C3) each pays `φ_c[χ(ℓ) − χ(y_c)] ≤ φ_c·c_ℓ`, where `c_ℓ := χ(ℓ)` if `ℓ ≥ p_u` and `c_ℓ := 0`
if `ℓ < p_u` (then `χ(ℓ) ≤ χ(y_c)`, `χ` being monotone on `[0, p_u]`).  So the classes of `g` pay at most
`μ_g c_ℓ` with `μ_g ≤ φ_g` and `0 ≤ c_ℓ ≤ χ(κ) = h`.
 — If `m_g ∈ [κ, 1−κ]` the cell pays nothing in `Π₂`, and `A_g ≤ φ_g h`.
 — If `m_g < κ` the cell pays `φ_g[χ(κ) − χ(m_g)] = φ_g[h − χ(m_g)]` in `Π₂`.  All classes of `e` are `≥ ℓ`, so
`ℓ ≤ m_g < κ`, hence `c_ℓ ≤ χ(m_g)` (monotonicity on `[p_u, ½]` if `ℓ ≥ p_u`; `c_ℓ = 0` otherwise), and
`A_g ≤ φ_g χ(m_g) + φ_g h − φ_g χ(m_g) = φ_g h`.  The case `m_g > 1−κ` is the mirror image.

*Step 5.*  `Π₁ + Π₂ ≤ Σ_g φ_g h = h`, so `−F(y) − r(y) ≤ ν_𝒦 + h − θ`.

*The case `Φ(1) > θ`* (it needs `θ < h`; pointed out by the reviewer, who noted that the hypothesis `θ ≥ h` of
the first version was superfluous).  Take `e := clip_κ(y) ∈ 𝒦`.  By (H1), `F(e) = F(avg₁ e)`, `avg₁ e ∈ 𝒦`, and
`−F(avg₁ e) ≤ ν_𝒦 + r(avg₁ e)`.  So `−F(y) − r(y) − ν_𝒦 ≤ [r(e) − r(y) + u‖y − e‖] − [r(e) − r(avg₁ e)]
= Π₁ − cost₁(e) ≤ h − Φ(1) < h − θ`; here `Π₁ ≤ h` by the first half of Step 4 with `ℓ = κ`.  ∎

**Remarks.**

1. *Where the third level is used.*  The anchor `e′` is paid for twice: by `T(e)`, which the free step
   `F(e′) = F(m′)` returns, and by `Q(m′)`, which the free step `F(m′) = F(p)` returns; together `θ`.  With
   one informed batch only (two rounds) the second free step is missing: one gets
   `−F(y) − r(y) ≤ ν + h − θ + Q(m′)` and nothing better — in agreement with `c_2 > h`.
2. *Lemma B of the report is a special case* (blocks with centres: each block is a pair of classes, the
   sites where its centre is `0` and where it is `1`; a block is revealed when the pair is split), with
   explicit constants at finite `n` there.  The proof above is different and shorter: in Lemma B the
   revealed blocks were relaxed to the hinted radius first and the budget was spent on the hidden blocks;
   here every class is clipped at one level and the cell means are corrected afterwards.  The correction
   (`e → e′`, an aligned move whose Lipschitz cost is that of the mean) is what the earlier attempt lacked:
   with class-wise clipping alone the anchor of a *merged* block — two classes of which the batches control
   only the sum — fails to be visible to the first batch as soon as the deep class is more than half of
   the block.
3. *No dimension.*  Neither the statement nor the proof involves `|C|`, the sizes of the classes or the
   number of cells.
4. *What `h` and `θ ≥ h` mean here* (rewritten: the first version of this remark was wrong, as the review
   showed).  (a) The inequality holds for every budget; `h` enters through the core `𝒦`, on which (H1) and
   the normalisation are assumed.  An algorithm can establish (H1) on `𝒦` by a blind batch only if that
   batch sees `𝒦`, i.e. with `e^{nh}` points: this is where `θ ≥ h` is needed.  If (H1) and the normalisation
   are assumed only on what a blind batch of `e^{nθ}` points sees, `{r ≤ θ}`, the conclusion fails for `θ < h`:
   the plain dip (one cell `{c₀, c₁}` with equal weights — a hidden centre that is never revealed — and a cone
   around the centre cut off where the second batch would see it) has hidden exponent
   `u·f^{−1}(θ) − Λ₁ = D(θ) > 0` at its cone point.  For `θ < h` that dip reaches the type `(κ, 1−κ) ∈ 𝒦` and
   violates (H1) there, so it is not a counterexample to the theorem.  (b) The constant `h` in the bound is
   optimal and attained: by the plain dip at `θ = h`, and for larger `θ` by a construction of the reviewer —
   one cell with two classes, `−F` equal to `f` of the cell mean on `[κ, 1−κ]`, continued with slope `u`
   outside, and extended from `{cost₁ ≤ θ}` as the largest `u`-Lipschitz function; hidden types with cell
   mean `p_u` and cost just above `θ` then have exponent `ν_𝒦 + h − θ` (such types exist, for instance, up to
   `θ = 8.1h` at `u = 1` with equal weights).  In these profiles the *visible* maximum is `ν_𝒦 + h`, so the
   sharpness is relative to `ν_𝒦` and says nothing about slack in Theorem H6, where hidden mass is
   compared with visible mass.
5. *More rounds.*  For `r ≥ 3` rounds apply the theorem to the partitions learned by the last two
   informed batches.

---

## A3. Checks of Theorem P

* **[N] The chain from the definitions** (`experiments/phase2_hierarchy/h11_partition_chain_check.py A`,
  output `out/h11_partition_chain_A.txt`).  20 000 random instances — 2 to 8 classes, random weights down to
  `10⁻³`, random nested partitions, `u ∈ {¼, ½, 1, 2, 4, 6}`, `θ/h ∈ {1, 1.05, 1.3, 2, 3}`, hidden types from six
  families (uniform, extreme, cone points on both sides, a deep class beside typical ones, hinted radii,
  boundary values).  For each the script builds `e`, `m′`, `e′` and evaluates, from the definitions of `r`,
  `avg`, `cost` only: `cost₁(e′) − θ`, `|avg₂ e′ − m′|`, `r(m′) − θ`, the bound
  `r(avg₁ m′) − r(y) + u‖y − e′‖ − (h − θ)`, the per-cell prices minus `φ_g h`, and `T(e′) − T(e)`.  All are
  `≤ 0` up to rounding (`≤ 3·10⁻¹³ h`); the bound itself is `≤ −1.1·10⁻³ h` in every instance.
  *History:* the first run reported violations; they came from a reversed bisection in the script's own
  `fill` routine (the anchor `e′` did not have the cell means `m′`, which the second check showed
  directly).  After the correction that check is `3·10⁻¹⁶` and everything passes.
* **[N] Extremal profiles by brute force** (same script, parts `B`, `B3`; outputs
  `out/h11_partition_chain_B.txt`, `out/h11_partition_chain_B3.txt`).  On the lattice of types of
  `n = 160…240` coordinates in 2–4 classes: the pointwise largest `U = −F` with unit steps `≤ u`, `U ≤ R` on a
  blind set, and `U` invariant under exchanges between classes of a common `𝒢₁`-cell inside the blind set
  and of a common `𝒢₂`-cell inside the region of the second batch (connected components of the exchange
  graph — nothing assumed about the regions).  Seven cases with six different information structures (a
  merged cell with two hidden classes, equal and unequal; a merged cell split by round two; a merged pair
  revealed first; nested pairs, two sets of sizes; two cells each hiding a pair).
  - *Blind set `{r ≤ θ}`* (parts B1, B2).  This is what the first round of the algorithm provides, and it is
    a **stronger hypothesis than (H1) on the core: the test is of a weaker statement than Theorem P** (the
    reviewer's main finding on this section).  `u ∈ {1, 2, 4}`, `Θ/nh ∈ {0.7, 1, 1.2, 1.5, 2.5}`, entropy form:
    the largest hidden mass exceeds `nh − Θ` by at most `0.95·u` in all 84 cases with `Θ ≥ nh`; for `Θ = 0.7nh`
    it is positive in all but one case.  At `u = 1` the test has little power (`nh` is 5–7 lattice steps).
    With exact binomial probabilities the difference is a `log n` term; doubling `n` at `Θ = 1.2nh` the excess
    goes `+3.3, −2.0, −10.9, −28.2` (`u = 2`, two classes in one cell, `n = 240…1920`) — a margin of the weaker
    statement, not of the theorem.
  - *Blind set = the core* (part B3, added after the review: the theorem as stated; `u ∈ {2, 4}`,
    `Θ/nh ∈ {1, 1.2, 1.5}`).  With the lattice points of `𝒦` the largest excess is `+1.48·u` (four classes); with
    the smallest lattice box containing `𝒦` it is `−0.50·u`.  The anchor of the proof sits at `κ·n_c`, which is
    not a lattice point, and each class can cost up to `(u − |f′(κ)|)` times the rounding.  For two classes
    in proportion 1:3 the excess stays between `−0.27u` and `+0.10u` from `n = 240` to `n = 1920` at all three
    budgets: these instances sit on the bound and do not move with `n`.
  - *The reviewer's own solver* (validated against Dijkstra; about 420 cases with 2–5 classes under the
    exact hypotheses, among them three classes in one cell, a cell split into three, a class of 3 %): no
    excess grows with `n` (up to `n = 1921 / 483 / 260 / 145` for 2 / 3 / 4 / 5 classes); the largest is
    `+2.14·u` on a lattice with unaligned class sizes, where the rounding of the core predicts `2.13·u`, and
    `+0.75·u` with aligned sizes.  Its controls: with (H1) only on `{r ≤ θ}` and `θ < h` the plain dip appears
    with the predicted size; without (H2) the excess grows with `n`; the two-round analogue has gain `≈ 0` up
    to `Θ ≈ 1.3nh` at `u = 2` (the archive's `θ₂*/h = 1.33`); without (H1) no violation appeared in the one
    structure tried, so (H1) is needed by the proof and possibly not by the statement there.
* **[N] Three overlapping centres at finite slope** (`h10_three_centres_finite_slope.py`, outputs
  `out/h10_*`), run before the theorem was found: 84 overlap patterns, `u ∈ {1,2,4}`; at `θ = 1.3h` every
  hidden gain is `≤ −0.37h`; at `θ = h` there are small positive values: at `u = 1` up to `+0.25h` at grid 20,
  shrinking under refinement (`+0.16h`, `+0.10h` at grids 30, 40); at `u = 2` between `+0.02h` and `+0.08h` at
  all three grids, without a monotone trend.  The grid enforces the two invariances only between lattice
  points with exactly equal means, so it over-estimates.  Consistent with the theorem, not a test of it.
* **[V] Arithmetic** (`proofs/Frontiers/PartitionChain.lean`, namespace `MetricChain.PartitionChain`,
  compiles without warnings with the pinned toolchain): `partition_chain` (Step 3 and Step 5 from their
  inputs), `cell_price_central`, `cell_price_deep` (the two cases of Step 4), `visible_of_fill` (Step 2).
  The analytic inputs — (C1)–(C4), the existence of `s` and of the levels `λ_g` — are hypotheses there and
  are **not** formalised.

---

## A4. Hidden-partition classes and the algorithm

**The class.**  `HP_m = HP_m(u, n)`: the `ψ: Q_n → ℝ` for which there are a partition `𝒞 = (C_1, …, C_{m′})`
of the coordinates into `m′ ≤ m` nonempty classes and a function `F` on `K = Π_j {0, …, n_j}` (`n_j = |C_j|`)
with `ψ(x) = F(k(x))`, `k_j(x) = #{i ∈ C_j : x_i = 1}`, and `|F(k) − F(k′)| ≤ u` for neighbouring `k, k′`.
Equivalently: `ψ ∈ L_u` is invariant under the permutations of the coordinates that preserve an (unknown)
partition into at most `m` classes.  Neither the partition nor the class sizes are restricted.

*Examples.*  A block-radial energy `F(d(x^{B_1}, s^1), …, d(x^{B_m}, s^m))` is in `HP_{2m}` (classes
`B_j ∩ {s^j = 0}`, `B_j ∩ {s^j = 1}`), with blocks and centres unknown.  Any `F(d(x, s¹), …, d(x, s^r))` with
arbitrary centres is in `HP_{2^r}` (classes: the sign patterns `(s¹_i, …, s^r_i)`).  The cones, dips, twins
and chains of the archive, and the merged and nested variants of §7 of the report, are of this kind.

**Algorithm R3P(M)** (knows `n`, `m`).  A pair of coordinates `{i, i′}` is *separated* by an evaluated point
`x` if `x_i = x_{i′}` and `ψ(x^{(i)}) ≠ ψ(x^{(i′)})` (`x^{(i)}` := `x` with coordinate `i` flipped).  Coordinates
of one class of `𝒞` are never separated.

* **Round 1.**  `M` independent uniform points, each evaluated with its `n` neighbours.  `𝒢₁` := a
  partition of the coordinates into at most `m` cells none of which contains a separated pair (`𝒞` is
  one; choose by any fixed rule).
* **Round 2.**  For every vector `a` of cell counts, `0 ≤ a_g ≤ |g|` (`g ∈ 𝒢₁`): `M` independent uniform
  points of the *shell* `{x : #(x ∩ g) = a_g for all g}`, each evaluated with its `n` neighbours.  `𝒢₂` := a
  partition that refines `𝒢₁`, has at most `m²` cells, and no cell of which contains a pair separated in
  rounds 1 or 2 (the common refinement of `𝒢₁` and `𝒞` is one).
* **Round 3.**  For every vector `b` of cell counts of `𝒢₂`: `M` independent uniform points of the shell,
  evaluated.
* **Output.**  `Â := Σ_b π(b)·(1/M) Σ_{x in shell b} e^{−ψ(x)}`, `π(b) = Π_{g∈𝒢₂} C(|g|, b_g) 2^{−|g|}`.

Three rounds; at most `M(n+1) + (n+1)^m M(n+1) + (n+1)^{m²} M ≤ 3(n+1)^{m²+1} M` evaluations.  Choosing the
partitions is a computation on the answers and costs no evaluation.  `E[Â | rounds 1, 2] = A(ψ)` for
*any* `𝒢₂` (the shells partition the cube and `π(b)` is the probability of shell `b`).

> **Theorem H6.**  Let `u > 0`, `m ≥ 1`, `η ∈ (0, 1]`, `δ ∈ (0, 1)`, `Θ := n(h + η/2)`, `M := ⌈e^{Θ + ηn/4}⌉`.
> There is `n₀(u, m, η, δ)` such that for `n ≥ n₀` and every `ψ ∈ HP_m(u, n)`, Algorithm R3P(M) makes at most
> `e^{n(h+η)}` evaluations and
>
>     P[ (δ/2)·Â ≤ A(ψ) ≤ 4·Â ] ≥ 1 − δ.        **[P]**
>
> Consequently `c_r(HP_m) = h(u)` for every `r ≥ 3` and every fixed `m ≥ 2` (the lower bound is Theorem
> 11.25 [K, V]: its hidden dips are functions of the distance to one centre, hence in `HP_2`).

The proof needs three elementary bounds.  `L := ln(n+1)`, `D := m³`.

* **(S)** For `N ≥ 1`, `0 ≤ a ≤ N`: `N f(a/N) ≤ N ln 2 − ln C(N, a) ≤ N f(a/N) + ln(N+1)`.
* **(U)** For `N ≥ 1` and `t, t′ ∈ [0,1]` with `|t − t′| ≤ 1/N`: `N|f(t) − f(t′)| ≤ ln(N+1) + 1`.
  (`|f′(ξ)| = |ln(ξ/(1−ξ))|` is largest near the ends, so the integral of `N|f′|` over an interval of length
  `1/N` is at most `N[ln 2 − f(1/N)] ≤ ln N + 1`; for `N = 1`, `f ≤ ln 2`.)
* **(B)** For `p ∈ (0,1]`: `P[Bin(M, p) < Mp/2] ≤ e^{−Mp/8}` and `P[Bin(M, p) = 0] ≤ e^{−Mp}`.

*Fine classes and types.*  `𝒞₁ := 𝒢₁ ∧ 𝒞` and `𝒞₂ := 𝒢₂ ∧ 𝒞` (common refinements; at most `m²` and `D`
classes).  A *fine type* `k` gives the number of ones in every class of `𝒞₂`; it determines the type
`k¹` on `𝒞₁`, the *true type* `κ(k) ∈ K`, and the shells `a(k)`, `b(k)`; `ψ = F₂(k) := F(κ(k))`, and
`|F₂(k) − F₂(k′)| ≤ u‖k − k′‖₁`.  Given its fine type (on `𝒞₁`, `𝒞₂` or `𝒞`) a uniform point of a shell is
uniform among the points of that type, and its coordinates in different fine classes are independent.
`P(·)` is the uniform probability, `P(k | b(k)) = P(k)/π(b(k))`.  With `z = z(k)` the vector of densities
`k_c/n_c`, weights `φ_c = n_c/n`, and `cost_i` the costs of §A1 for the partitions that `𝒢₁`, `𝒢₂` induce on
`𝒞₂`, (S) and the monotonicity of `r` under averaging give

    n r(z) ≤ −ln P(k) ≤ n r(z) + DL,        −ln P(κ(k)) ≤ n r(z) + DL,
    n cost₂(z) − DL ≤ −ln P(k | b(k)) ≤ n cost₂(z) + DL,        −ln P(k¹ | a(k)) ≤ n cost₁(z) + DL.        (1)

From (U): if `k` is a fine type and `z*` a real type with `|k_c − n_c z*_c| ≤ ρ` for all `c` (`ρ ≥ 1` an
integer), then

    |n r(z(k)) − n r(z*)| ≤ Dρ(L+1),        |n cost_i(z(k)) − n cost_i(z*)| ≤ 2Dρ(L+1).        (2)

*Proof of Theorem H6.*  Let `n` be so large that every "for large `n`" below holds; all of them compare
`ηn` with `c·D²(L + 1 + u)`.

**(a) Cost and the upper side.**  `3(n+1)^{m²+1}M ≤ e^{n(h+η)}` for large `n`.  By unbiasedness and Markov,
`P[Â > (2/δ)A] ≤ δ/2`.

**(b) Three events.**
`E₁`: for every true type `κ` with `P(κ) ≥ e^{−Θ}` and every ordered pair of coordinates `(i, i′)` in different
classes `C_j ∋ i`, `C_{j′} ∋ i′` with `κ_j ≤ n_j − 1`, `κ_{j′} ≤ n_{j′} − 1`, some point of round 1 has true type
`κ` and `x_i = x_{i′} = 0`.
`E₂`: for every type `k¹` on `𝒞₁` with `P(k¹ | a(k¹)) ≥ e^{−Θ}` and every `(i, i′)` in different classes of `𝒞`
whose classes `c ∋ i`, `c′ ∋ i′` of `𝒞₁` have `k¹_c ≤ n_c − 1`, `k¹_{c′} ≤ n_{c′} − 1`, some point of round 2 in
the shell `a(k¹)` has type `k¹` and `x_i = x_{i′} = 0`.
`E₃`: for every fine type `k` with `P(k | b(k)) ≥ e^{−Θ}`, at least `M·P(k | b(k))/2` points of round 3 in
the shell `b(k)` have fine type `k`.
Given the type, `P[x_i = x_{i′} = 0] ≥ n^{−2}` under the stated conditions (independence across fine
classes).  By (B), conditionally on the earlier rounds,
`P[E₁ᶜ] + P[E₂ᶜ] ≤ 2(n+1)^{m²+2} exp(−e^{ηn/4}/n²)` and `P[E₃ᶜ] ≤ (n+1)^D exp(−e^{ηn/4}/8)`; together `≤ δ/2`
for large `n`.

**(c) Exchange identities.**  Let `d ⊂ C_j`, `d′ ⊂ C_{j′}` be classes of `𝒞₂`, `k` a fine type with
`k_d ≤ n_d − 1`, `k_{d′} ≥ 1`, and `k′ := k + e_d − e_{d′}`.  If `j = j′` then `κ(k′) = κ(k)` and `F₂(k′) = F₂(k)`.
For `j ≠ j′`:

* **(X1)** on `E₁`: if `d`, `d′` lie in one cell of `𝒢₁` and `P(κ(k) − e_{j′}) ≥ e^{−Θ}`, then `F₂(k′) = F₂(k)`.
* **(X2)** on `E₂`: if `d`, `d′` lie in one cell of `𝒢₂` and the type `k⁻` on `𝒞₁` of `k − e_{d′}` has
  `P(k⁻ | a(k⁻)) ≥ e^{−Θ}`, then `F₂(k′) = F₂(k)`.

Proof of (X2).  Take `i ∈ d`, `i′ ∈ d′`; they are in one cell of `𝒢₂`, hence never separated, and in classes
`c ⊃ d`, `c′ ⊃ d′` of `𝒞₁`, `c ≠ c′`.  `k⁻_c ≤ n_c − 1` (because `k_d ≤ n_d − 1`) and `k⁻_{c′} ≤ n_{c′} − 1`
(because one unit was removed from `d′`).  By `E₂` a point `x` of round 2 has type `k⁻` and
`x_i = x_{i′} = 0`; its true type is `κ(k) − e_{j′}`, so `ψ(x^{(i)}) = F(κ(k) − e_{j′} + e_j) = F₂(k′)` and
`ψ(x^{(i′)}) = F(κ(k)) = F₂(k)`; the pair is not separated, so the two are equal.  (X1) is the same with
round 1, `𝒢₁` and true types.

**(d) The lower side on `E₃`.**  Let `𝒱 := {k : P(k | b(k)) ≥ e^{−Θ}}`, `A_vis := Σ_{k∈𝒱} P(k) e^{−F₂(k)}`,
`A_hid := A − A_vis`.  On `E₃`, `Â ≥ Σ_{k∈𝒱} π(b(k))·[P(k | b(k))/2]·e^{−F₂(k)} = A_vis/2`.  Let
`e^{ν₀} := max{P(κ) e^{−F(κ)} : P(κ) ≥ e^{−Θ+DL}}` (the set is not empty for large `n`: the most likely true
type has probability at least `(n+1)^{−m}`).  The maximising `κ*` has at most `(n+1)^D` fine types, so one
of them, `k*`, has `P(k*) ≥ P(κ*)(n+1)^{−D} ≥ e^{−Θ}`; then `k* ∈ 𝒱` and

    A_vis ≥ (n+1)^{−D} e^{ν₀}.        (3)

**(e) The hidden types, on `E₁ ∩ E₂`.**  Let `y ∉ 𝒱`, `ŷ := z(y)`.  By (1), `n cost₂(ŷ) > Θ − DL`.  Put
`θ_c := (Θ − 9D(L+1))/n`; then `cost₂(ŷ) > θ_c ≥ h` for large `n`.  Apply the construction of §A2 to the classes
`𝒞₂`, the partitions induced by `𝒢₁`, `𝒢₂`, the budget `θ_c` and the type `ŷ`: real types `e`, `m′`, `e′`,
`p = avg₁ m′` with

    cost₁(e′) ≤ θ_c,    avg₂ e′ = m′ ∈ 𝒦,    p ∈ 𝒦,    r(p) − r(ŷ) + u‖ŷ − e′‖ ≤ h − θ_c        (4)

(the last inequality is Steps 3–5 without the profile).  Round to fine types: `B_g` := the integer nearest
to `n_g m′_g`; `E′` with cell counts `B_g` on `𝒢₂` and `|E′_c − n_c e′_c| ≤ 1` (round every `n_c e′_c` down or up;
all integer cell sums between the two extremes occur); `M″` with the same cell counts and
`|M″_c − n_c B_g/n_g| ≤ 1`; `P″` with the same cell counts on `𝒢₁` as `M″` and within one unit of equal
densities in every cell of `𝒢₁`.  All of `M″_c`, `P″_c` are within `ρ₀ := m² + 2` units of `n_c m′_c`,
`n_c p_c` respectively.

*`F₂(E′) = F₂(M″)`.*  Go from `E′` to `M″` by single exchanges inside cells of `𝒢₂`, every coordinate moving
monotonically.  Along the way the cell counts are `B_g`, so for an intermediate `k`,
`n cost₂(z(k)) = Σ_c n_c KL(k_c/n_c ‖ B_g/n_g)`; each term is convex in `k_c` and `k_c` lies between `E′_c` and
`M″_c`, so `n cost₂(z(k)) ≤ n cost₂(z(E′)) + n cost₂(z(M″)) ≤ n cost₂(e′) + 4D(L+1)` by (2).  The means are
those of `m′` up to half a unit per cell, so with (2) again `n cost₁(z(k)) ≤ n cost₁(e′) + 6D(L+1)`, and one
more unit for `k − e_{d′}` gives `≤ nθ_c + 8D(L+1) ≤ Θ − DL`.  By (1) the hypothesis of (X2) holds at every
step.

*`F₂(M″) = F₂(P″)`.*  Go from `M″` to `P″` by single exchanges inside cells of `𝒢₁`, monotonically.  Every
coordinate of an intermediate type, also after removing one unit, is within `ρ₀ + 1` units of
`n_c[κ, 1−κ]`, where `f ≤ h`; by (U) its rate is at most `nh + D(ρ₀+1)(L+1)`, so by (1)
`−ln P(κ(·)) ≤ nh + D(ρ₀+2)(L+1) ≤ Θ − DL` for large `n`, and (X1) applies at every step.  The same bound
gives `P(κ(P″)) ≥ e^{−Θ+DL}`, hence `P(P″) e^{−F₂(P″)} ≤ P(κ(P″)) e^{−F(κ(P″))} ≤ e^{ν₀}`.

*Assembling.*  `‖y − E′‖₁ ≤ n‖ŷ − e′‖ + D`, `ln P(y) ≤ −n r(ŷ)`, `−ln P(P″) ≤ n r(p) + Dρ₀(L+1) + DL`.  So

    ln[P(y) e^{−F₂(y)}] ≤ −F₂(E′) + u‖y − E′‖₁ + ln P(y) = −F₂(P″) + u‖y − E′‖₁ + ln P(y)
                        ≤ ν₀ − ln P(P″) + ln P(y) + u‖y − E′‖₁
                        ≤ ν₀ + n[r(p) − r(ŷ) + u‖ŷ − e′‖] + D(ρ₀+1)(L+1) + uD
                        ≤ ν₀ + nh − Θ + D(ρ₀ + 10)(L+1) + uD,

by (4).  There are at most `(n+1)^D` fine types, so with (3) and `Θ − nh = ηn/2`

    A_hid ≤ (n+1)^{2D} exp(−ηn/2 + D(ρ₀+10)(L+1) + uD) · A_vis ≤ A_vis        for large n.

**(f) Conclusion.**  On `E₁ ∩ E₂ ∩ E₃`: `A = A_vis + A_hid ≤ 2A_vis ≤ 4Â`.  With (a) and (b),
`P[(δ/2)Â ≤ A ≤ 4Â] ≥ 1 − δ`.  ∎

**Remarks.**
1. The proof uses `m` only through `D = m³`, `ρ₀ = m² + 2` and the number `(n+1)^{m²}` of shells: it gives
   the same conclusion for `m = m(n)` with `m⁵ log n = o(n)` (and `η`, `δ` fixed).  This is not optimised.
   The reviewer evaluated the conditions "for large `n`": they hold up to `m⁵ ln n ≈ 0.47·ηn`; the smallest
   admissible `n` is about `2.5·10³` for `m = 2`, `η = 1` and `5.4·10⁵` for `m = 4`, `η = 0.1` (`u = 1`, `δ = 0.1`).
   So the theorem is asymptotic in earnest: nothing is claimed at the sizes of the numerical checks.
2. Nothing is assumed about the sizes of the classes; single coordinates are allowed.
3. A ratio `e^ε` instead of the constant `8/δ`: repeat and take medians as in §4 of the report, or use
   `M·e^{o(n)}` points; the exponent is unchanged.
4. *Parities need no separate treatment.*  Take a block with a hidden centre (two classes, the sites where
   the centre is `0` and where it is `1`) and a profile that is `2`-periodic in the distance to the centre.
   Flipping a site of either class at a point changes the distance by `±1`, and the two values of the
   profile coincide: the two classes are never separated.  They need not be: the distance has the parity
   of the cell count plus a constant, so the profile is a function of the cell count, which is what (X1),
   (X2) say.  (Lemma B of the report had to carry parities through its hypotheses.)
5. *Two idealisations of the query model.*  Choosing a partition with no separated pair inside a cell is
   a graph-colouring problem; it costs no evaluation but possibly much time (when every separation between
   two classes is witnessed for all pairs — the typical case — the cells are the twin classes of the
   separation graph and are found at once).  "Separated" compares real numbers exactly.

---

## A5. Consequences

> **Corollary H7 (the hierarchy on hidden-partition classes).**  For every `u > 0` and fixed `m ≥ 4`:
> `c_1(HP_m) = a`, `h < c_2(HP_m) < a`, `c_r(HP_m) = h` for all `r ≥ 3`.

(`c_1`: the cones and truncated cones of Theorems 11.44/11.45 [K] are in `HP_2`.  `c_2 > h`: `HP_4` contains
every two-block class `BR_2(φ_1, φ_2)`, on which the twins of Theorem 11.86 [K] live, and a lower bound on
a subclass is a lower bound on the class.  `c_2 < a`: Corollary 11.87 [K], valid on `L_u`.  `c_r = h`:
Theorem H6 and Theorem 11.25 [K].)

> **Corollary H8 (barrier, final form for bounded structure).**  Let `r ≥ 3`.  No family of energies with
> hidden symmetry type bounded by a fixed `m` — in particular no construction from finitely many hidden
> centres, blocks, levels or partition classes, overlapping, merged or nested in any way — has `r`-round
> exponent above `h`.  A proof of `c_r(u) > h(u)` must use energies whose description needs a number of
> classes growing with `n` (at least like `(n/log n)^{1/5}` by Remark 1).

*Relation to the report.*  Open problems 1 (hidden partition) and 2 (overlapping centres) of its §8 are
settled for bounded `m`, at finite slope and finite `n`.  Proposition G (flags, small-slope limit) is now
a statement about a limit model whose cube instances are all covered; it remains of independent interest
for Lipschitz bodies that are not sections of a box.  Lemma B and Theorem H1 remain as stated; they have
explicit constants and need only `(n+1)^m` shells because the blocks are known.

*What a refutation of Conjecture H5 would now need.*  Problem 5 of the report's §8, sharpened: (a) no
bounded hidden symmetry (Theorem H6); (b) not merely exponentially many indistinguishable copies of a
bounded structure (Proposition C of the report, at the level of exponents); so the hidden information
would have to be spread over a number of classes that grows with `n` *and* be learnable only in pieces
that three rounds cannot chain.  Theorem P does not see how many classes there are; what fails for
general `ψ` is the *algorithm* (shells of a partition with boundedly many cells) and the two hypotheses
(H1), (H2), which for a general `ψ` hold only approximately and locally.

*What a proof of H5 could look like.*  A three-round scheme in which the second and third batches sample,
around points found earlier, shells of the partition of the coordinates by (bit, quantised slope) at that
point — a partition with boundedly many cells for every accuracy — together with an approximate version of
Theorem P in which (H1), (H2) hold up to `εn`.  The chain of §A2 is stable under such errors (each free
step is used once).  Not done; we do not know whether the local partitions can be chained.

*Closest prior art for the phenomenon* (three further searches on 2026-11-28; **search-engine summaries
only, no paper read**; the earlier searches are in §10 of the report).
* *A constant number of stages reaches the adaptive optimum: group testing.*  For finding a hidden set of
  defectives, non-adaptive designs are strictly worse than adaptive ones in some regimes, and the
  information-theoretic adaptive rate is reported to be achievable with two stages in the noiseless case
  (Coja-Oghlan, Gebhard, Hahn-Klimroth, Loick, arXiv 1911.02287 and 1911.06647), with two or three stages
  under noise (Scarlett, arXiv 1803.05099), and with two to four stages depending on the number of
  defectives (Damaschke and co-authors, "Randomized group testing both query-optimal and minimal
  adaptive").  This is the nearest structural analogue we found of Corollary H7: a hidden combinatorial
  object, a strict gap between one stage and full adaptivity, and a collapse after a small constant number
  of stages.  The problems differ (identification against estimation of an integral; polynomial against
  exponential scales).
* *Hidden symmetry as a class of functions.*  Functions invariant under the permutations of all but a
  constant number of variables are the *partially symmetric functions* of Blais, Weinstein and Yoshida
  (FOCS 2012; SIAM J. Comput. 2015), who test and implicitly learn the asymmetric part with a notion of
  symmetric influence.  `HP_m` is the analogous class with `m` orbits of arbitrary sizes; the separation
  test of Algorithm R3P (equal bits, different slopes) plays the role of their influence test.  We do not
  know whether a version of our partition-learning step exists in that literature.
* *Rounds in query complexity:* the hierarchies that do not collapse listed in the report (property
  testing, local search in rounds, parallel convex optimisation).  For adaptive numerical integration of
  Lipschitz functions we found optimal adaptive algorithms in one dimension (Baran, Demaine, Katz) and no
  count of rounds.
"Not found" is not "new".

---

## A6. What has been checked, and by whom

Everything in this section was done by AI sessions.

* **Review of this addendum** (`HIERARCHY_ADDENDUM_REVIEW.md`; scripts and outputs in
  `experiments/phase2_hierarchy/review_addendum/`).  A session that did not write the addendum, with its own
  code, was asked to break Theorems P and H6.  *Verdict: no critical and no major finding; "Theorem P:
  correct as stated; Theorem H6: correct, given the archive's lower bound".*  What it did: every line of
  both proofs by hand; every intermediate claim of §A2 re-evaluated on 12 000 instances and by direct
  maximisation (`sup` of the bound's defect `= 0`, attained, never exceeded); exact extremal profiles under
  the theorem's hypotheses in about 420 cases with controls (§A3); (S), (U), (B), (1), (2) numerically; step
  (e) of §A4 executed literally with exact binomials (`m = 2, 3`, `n` up to `110 000`, about `240 000` exchanges,
  every hypothesis of (X1), (X2) evaluated); the "large `n`" conditions made explicit.  Twelve minor
  findings, all applied in this version: the brute-force check of §A3 tested a weaker statement (now
  said, and the exact one added); Remark 4 of §A2 was wrong as stated (rewritten); the hypothesis `θ ≥ h` of
  Theorem P was superfluous (removed, with the extra case of the proof); (C2) is not used; a selective
  quotation in the `h10` bullet; "seven structures" were six; the `|z|` values of the cube test (below); the
  non-emptiness in step (d); the shell count in Remark 1; Remark 4 of §A4 unclear (rewritten); two
  idealisations of the query model (Remark 5); the docstring of `h11`.  *Not checked by the reviewer:* the
  proofs of the archive results; compilation of the Lean file (read only); Remark 2 of §A2 (Lemma B as a
  special case) and the sentence on Proposition G in §A5; extremal profiles with more than five classes,
  at slopes below 1, or with exact binomial rates; the internals of `h10`, `h12`.
* Theorem P, by the author: proof in §A2; the chain re-evaluated from the definitions on random instances
  and compared with brute-force extremal profiles (§A3); arithmetic core in Lean.  The review of the
  *report* (`HIERARCHY_REVIEW.md`) does not cover this addendum.
* Theorem H6: paper proof in §A4, read by the reviewer as described.  No part of it is machine-checked,
  and it is asymptotic (Remark 1 of §A4).  The logic of Algorithm R3P was run
  literally on cubes `Q_12` (`h12_r3p_on_cubes.py`, [N]): hidden partitions into 2–4 classes, three kinds of
  profiles (minima of cones in the class counts; a profile that shows only the sum of two classes near
  the typical counts; a `2`-periodic one), `M ∈ {2, 12}`, 40 runs each.  In all 18 settings: the chosen
  partitions have no separated pair in a cell and at most `m`, `m²` cells, coordinates of one hidden class
  are never separated, and the estimate equals `A` up to rounding in every run (the energy was constant
  on every shell of `𝒢₂` in every run — so this test never meets a hidden type).  The mutation "uniform shell
  weights" is detected in 17 settings: in 10 with `|z| ≥ 5.9`, and in 7 because the mutated estimate is the
  same wrong number in every run (the printed `|z|` of `10¹⁶…10³⁰¹` there are divisions by a vanishing
  standard error, not z-scores); in one setting it is missed (`|z| = 2.4`).  The mutation "learn nothing"
  stays unbiased (`|z| ≤ 2.1`).  These sizes test the logic, not the exponent.
* The statements quoted from the archive carry the archive's status.

## A7. Reproducibility

| script (in `experiments/phase2_hierarchy/`) | what | runtime | output |
|---|---|---|---|
| `h11_partition_chain_check.py A` | the chain of Theorem P from the definitions, 20 000 random instances | 2 min | `out/h11_partition_chain_A.txt` |
| `h11_partition_chain_check.py B` | extremal profiles on lattices, blind set `{r ≤ θ}` (weaker statement); growth with `n` | 3 min | `out/h11_partition_chain_B.txt` |
| `h11_partition_chain_check.py B3` | the same under the theorem's exact hypotheses (core) | 70 s | `out/h11_partition_chain_B3.txt` |
| `h10_three_centres_finite_slope.py [N]` | three overlapping centres, finite slope (before the theorem) | 1 min at `N = 20` | `out/h10_three_centres_finite_slope_N20.txt`, `…_refine.txt` |
| `h12_r3p_on_cubes.py` | Algorithm R3P literally on cubes `Q_12`, with two mutations | 2 min | `out/h12_r3p_on_cubes.txt` |
| `h9_two_rounds_three_blocks.py` | two rounds, hidden group split in two (small slope) | 1 min | `out/h9_two_rounds_three_blocks.txt` |

Lean: `lake env lean proofs/Frontiers/PartitionChain.lean` (four theorems; no warnings; axioms `propext`,
`Classical.choice`, `Quot.sound`).  The reviewer's scripts: `experiments/phase2_hierarchy/review_addendum/`
(table in §7 of `HIERARCHY_ADDENDUM_REVIEW.md`).
