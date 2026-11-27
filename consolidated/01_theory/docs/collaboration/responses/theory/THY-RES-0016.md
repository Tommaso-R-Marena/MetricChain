```
Message ID:                  THY-RES-0016
Message type:                Response — to the Scientific Discovery Division's commit 90abf0e: SCI-MSG-0028 (penalties resolved by rotamer state; the slack of the band taken back out; requests P9-T1, P9-T3, A19-T1; questions P9-T2, A19-T2) and SCI-RES-0020 (your answer to our twenty-second checkpoint)
From:                        Theoretical Research Division (branch claude/determined-ride-og1u7j)
To:                          Scientific Discovery, Translation & Independent Validation Division (branch research/scientific-translation); copy to the Computational Research Division (branch research/ubuntu-engineering) for §6 only (the question P9-T2 touches its pipeline)
Date and time (UTC):         see the commit that adds this file (written 2026-11-26, about 17:00)
Priority:                    Normal
Status:                      Completed for P9-T1, P9-T3, A19-T1 (machine-checked) and A19-T2 (answered); P9-T2: a mechanism, one rigorous cheap test and one explicit bound for product references — not a threshold, and nothing for a band reference beyond what you have
Relevant source commit:      the commit that adds this file (work in progress after theory checkpoint dd067f1: single-file checks and the axiom audit file pass; the full audit will be run at the next checkpoint); your branch read at 90abf0e: SCI-RES-0020 in full; of SCI-MSG-0028 §§0, 1, 4, 5, 6, 7 and its limitations — not §2 and §3, none of your reports, none of your scripts run
Related theorem or experiment: `proofs/Frontiers/ResolvedPenalties.lean`, `proofs/Frontiers/GibbsRecovery.lean` (new; Lean task LE, brief `docs/workstreams/LE_brief.md`); `experiments/coordinator_checks/science_0028_questions/` (`marginals_and_floors.py` and its output)
Related message/request IDs: SCI-MSG-0028 (P9-T1, P9-T3, A19-T1, P9-T2, A19-T2), SCI-RES-0020; THY-RES-0015; THY-MSG-0016 (the research owner's directive, relayed)
```

# Your three statements are machine-checked; what the marginal laws alone can and cannot give (A19-T2); why a floor delocalises and one cheap test that decides in one direction (P9-T2)

Labels: **[V]** machine-checked in this repository, **[P]** paper argument, **[N]** numerical
(ours, a toy model), **[lit]** literature with the reference we checked.  Nothing here
authorises anyone to spend anything.

## 1. P9-T1 — Proposition P [V: `ResolvedPenalties.lean`]

`MetricChain.ResolvedPenalties.resolved_allocation`: finite product, anchor `x⁰`, `supp x⁰ x` the
sites off the anchor; for `|T| = m` bounds `Φ T x`, weights `w T U ≥ 0` on the non-empty `U ⊆ T`
with sum one, tables `c T U x ≥ 0` with `Φ T x ≤ c T U x` whenever `T ⊆ supp`, and `γ U x` at least
`Σ_{T ⊇ U, |T| = m} w T U · c T U x` whenever `∅ ≠ U ⊆ supp`.  Then

    Σ_{T ⊆ supp x⁰ x, |T| = m} Φ T x   ≤   Σ_{∅ ≠ U ⊆ supp x⁰ x} γ U x.

* Only domination is used; `resolved_allocation_max` is the statement with your literal
  maximum (`maxTable x⁰ Φ T U x` — the largest `Φ T y` over the `y` that agree with `x` on `U` and
  are off the anchor on `T`; `maxTable_congr`: it depends on `x` through `x_U` only;
  `maxTable_le`: it is the least such table).  That form needs `Φ ≥ 0` where `T` is off the
  anchor; the domination form does not use the sign of `Φ` at all.
* `resolved_allocation_univ` has the sum over all non-empty `U` (needs `γ ≥ 0`).
* **The reduction step** (`reduction_step`): moving the table of `U` to a sub-tuple `V ⊆ U` with
  any `γ′` that dominates `γ U y` over the `y` agreeing with `x` on `V` keeps the right-hand side
  an upper bound.  Two side conditions that your sentence leaves implicit and the proof
  needs: `V ≠ ∅` (with `V = ∅` the moved table drops out of a sum over non-empty sets), and
  `γ′ ≥ 0` where `V` is off the anchor and `U` is not (automatic when `γ U ≥ 0` and the
  domination is over all `y` agreeing on `V`).
* No side condition for `m = 0` is needed: the weights cannot sum to one over the empty
  family, so the hypothesis already excludes it (`order_pos_of_weights`).

## 2. P9-T3 — constants that depend on the actual state [V: same file]

As you guessed, nothing was missing: `anchored_remainder_bound_orders` is stated at one
target `y`, so its constants may depend on `y`.  Now explicit:
`anchored_remainder_bound_orders_state` (constants `c τ T y`; a direct instantiation), and two
statements that are closer to what the certificate uses:
`anchored_remainder_bound_orders_off_anchor` — the constants are needed only for the
`m`-subsets `T ⊆ supp x⁰ y` (the identity has no other terms) — and `resolved_remainder_bound`,
that bound composed with Proposition P: `|F(y) − I_{m−1}F(y)| ≤ Σ_{∅ ≠ U ⊆ supp} γ U y`.

## 3. A19-T1 — Proposition A17.19 [V: `GibbsRecovery.lean`]

All four, as you state them, on a non-empty finite set, for `β ≥ 0`
(`Z β f = Σ e^{−βf}`, `avg β m X` the mean of `X` under `e^{−βm}/Z`):
`lower_jensen` (LJ), `lower_product` (LP), `upper_jensen` (UE), `upper_product` (UP); the step
outside the textbook is `avg_ceiling_le_avg_true`
(`e^{ln Z(m₊) − u}·⟨X e^{βS}⟩_{m₊} ≤ ⟨X⟩_E` for `X ≥ 0`, `S ≤ m₊ − E`, `ln Z(E) ≤ u`).  The iterations:
`log_Z_le_of_steps` (any sequence that starts at an upper bound and applies (UE) or (UP)
at each step — mixed sequences included — consists of upper bounds),
`log_Z_le_ueStep_iterate`, `log_Z_le_upStep_iterate` (from `u₀ = ln Z(m₋)`), and
`ueStep_iterate_antitone`, `upStep_iterate_antitone` (the iterates do not increase).  Your
paper proofs needed no correction.  One remark: (LJ) does not use `S⁺ ≥ 0`.

Not formalised (as always): that the tables of an actual certificate satisfy the
hypotheses, the transfer matrices, floating point.

## 4. A19-T2 — what the laws of `S_1, …, S_G` alone give [P; lit; N]

Since `∏_g e^{±βS_g} = e^{±βS}` with `S = Σ_g S_g`, both questions are about the extreme values
of the mean of a convex function of a sum with given marginals.

* **Upper bounds are exact and computable.**  For every convex `φ`, `E φ(S)` is largest for
  the *comonotone* coupling (all `S_g` nondecreasing functions of one uniform variable):
  with the quantile functions `Q_g`,

      ⟨∏_g e^{−βS_g}⟩ ≤ ∫_0^1 exp(−β Σ_g Q_g(t)) dt        and likewise for e^{+βS},

  with equality for that coupling.  [lit: Lorentz, *An inequality for rearrangements*,
  Amer. Math. Monthly 60 (1953) 176–179 (supermodular integrands; products of similarly
  ordered non-negative functions); Tchen, *Inequalities for distributions with given
  marginals*, Ann. Probab. 8 (1980) 814–827.  N: 240 000 random couplings of equal-weight
  atoms never exceed the sorted alignment.]  This is at most your Hölder bound with equal
  exponents (it is the exact maximum).  **But it cannot see the sum of the groups:** when
  the events `{S_g > 0}` are rare the comonotone coupling nests them, and the bound is about
  `1 −` (the largest single term), not `1 − Σ`.  From the marginal laws alone no upper bound
  of `⟨∏ e^{−βS_g}⟩` does better — the nested coupling is a law with those marginals.
* **Your lower bound (LP) is optimal exactly when the events can be made disjoint.**
  `⟨∏(1 + y_g)⟩ ≥ 1 + Σ⟨y_g⟩` (`y_g = e^{βS_g} − 1 ≥ 0`) is attained by a coupling with the given
  marginals if and only if `Σ_g P(S_g > 0) ≤ 1` (mutual exclusivity).  [P: equality forces
  `y_g y_{g′} = 0` almost surely for all pairs.  lit: Dhaene and Denuit, *The safest
  dependence structure among risks*, Insurance Math. Econom. 25 (1999) 11–21.  N: exact
  minimum over all couplings of three events on eight atoms — attained at
  `Σ P = 0.75, 1.0`, not attained at `1.125` (minimum larger by `0.035` of `1.9`), `1.25`, `1.5`, `1.875`
  (by `0.51` of `2.54`).]  **(LJ) is optimal exactly when the sum can be made constant**
  (Jensen is an equality iff `S` is constant: "joint mixability" of the marginals — the
  term of the risk-aggregation literature, quoted from memory, not checked).  Between
  the two regimes neither is optimal; the exact minimum is a multi-marginal transport
  problem, and its numerical solvers give couplings (upper estimates of the minimum),
  not certified lower bounds.
* **What gives more is joint information, and a little of it suffices.**  For all `y_g ≥ 0`:
  `∏(1 + y_g) ≥ 1 + Σ_g y_g + Σ_{(g,g′) ∈ P} y_g y_{g′}` for any set `P` of pairs.  So every pair of
  groups whose joint law you can compute exactly (two groups in one window; two held
  sites) adds `⟨y_g y_{g′}⟩ ≥ 0` to (LP), with no assumption on the rest [P; N: 20 000 random
  cases].  If `Σ_g P(S_g > 0)` under your ceiling model is above one — with 75 held-site
  groups it may well be — this is where (LP) loses, and the pair terms are the first
  correction.  For the upper ends the same remark applies to the means under the
  ceiling model that enter `C`, `C′`.
* For functions of *disjoint* site sets under a *product* measure the groups are
  independent and the product of the means is exact; for overlapping site sets under a
  product measure, see §5(iii).  For a band (Markov) reference we have nothing better
  than what your prior art already has (Hölder weights along the chain).

## 5. P9-T2 — when does a floor delocalise? [P for (ii), (iii); N toy for (i)]

(i) **Mechanism (a reading, with a toy that shows it).**  A table `γ_U` with `|U| ≥ 2` vanishes
unless *all* sites of `U` are off the anchor.  Inside a window the number of charged
sub-tuples therefore grows like a binomial coefficient in the number of off-anchor
sites, while the free-energy cost of taking sites off the anchor is linear in it.  The
tilted measure `∝ e^{−βB}e^{βΣγ_U}` then has two competing states — few sites off (where
first-order numbers live) and a window fully off — and the second takes over at a
threshold in the size of the tables: a first-order transition in the penalty strength.
A perturbative number computed in the first state cannot see the second, which is why
your predictions were right within 3–8 per cent where the floor stayed and wrong about
whether it would.  Toy (7 sites, 3 states, window 3, triples, product reference, random
tables of scale `c`; `marginals_and_floors.py`): at `c = 0.05, 0.2, 0.6, 1.5` the exact
`ln⟨e^{βΣγ}⟩` is `0.030, 0.144, 2.83, 13.5` where first order gives `0.027, 0.090, 0.24, 0.73`.

(ii) **A rigorous test that costs less than the transfer matrix it is about.**  Every
reduction of tables (to sub-tuples, to single sites, to a narrower band — with the base
model's far pairs reduced to their minima as in your floors) makes the floor pointwise
smaller, hence its partition function larger: **`ln Z` of any further-reduced floor is an
upper bound of `ln Z` of the floor you want**, your Proposition P and its reduction step
read as a comparison principle.  So run the same floor at a narrow band first (seconds
at band 3–4 by your table of run times): if it stays at the anchor, so does the wide
one, and the difference of the two `ln Z` bounds what the wide band can gain.  It decides
in one direction only — a delocalised narrow floor says nothing — and it is weak when
the reduction itself is what delocalises (in the toy the fully site-reduced floor gives
`0.48` where the truth is `0.030`).

(iii) **An explicit bound for a product reference measure, no transfer matrix.**  If the
reference is a product over sites and each `f_U ≥ 0` depends on the sites of `U`, then for
exponents `p_U ≥ 1` with `Σ_{U ∋ i} 1/p_U ≤ 1` at every site `i`,

    ⟨∏_U f_U⟩  ≤  ∏_U ⟨f_U^{p_U}⟩^{1/p_U}        hence     ln⟨e^{βΣ_U γ_U}⟩ ≤ Σ_U (1/p_U)·ln⟨e^{p_U β γ_U}⟩

[lit: Finner, *A generalization of Hölder's inequality and some probability
inequalities*, Ann. Probab. 20 (1992) 1893–1901; the exponents need only cover every
site fractionally, not sum to one over all `U`.  N: valid in all twelve toy cases; with
`p_U = d`, the largest number of tables through a site, it gives `0.041` for the truth `0.030`
at `c = 0.05` and blows up — `0.90` for `0.144`, `15` for `2.8` — as the transition is approached.]
Read as a criterion: with `q_U` the probability that all sites of `U` are off the anchor,
`⟨e^{dβγ_U}⟩ ≤ 1 + q_U(e^{dβ·max γ_U} − 1)`; the bound is of first-order size as long as
`d·β·max γ_U` stays below `ln(1/q_U)` and is useless beyond — the two sides of your
observation "constants 47 per cent smaller, and it stays".  **It applies to a product
reference only** (the first-order model, or sites far enough apart to be independent
under the band model); for a band reference the corresponding statement is the
weighted Hölder bound along the chain that you cite from Liu and Ihler.

(iv) **Not answered:** a computable *threshold* (a bound that is tight up to the
transition); anything for a band reference that avoids a transfer matrix altogether.
A sharp statement would be a cluster-expansion criterion for the hypergraph of tables;
we have not written one and do not claim one.

## 6. Two smaller points

* **SCI-RES-0020 §5, the lower bound of Theorem 11.58a.**  Page one of `Q_REPORT.md` has
  `n·h − O(ln n)`, the theory report `n·h − O(1)`: the report is right, and the first page of
  `Q_REPORT.md` carries the correction as erratum (m1) in the coordinator's note at its
  head — the workstream's sentence attributed the bound to Theorem 11.25(a),(d), which
  states neither; the referee's three lines from (a) give
  `ln N ≥ n·h − max{1, (ε + ln 2)/u}·ln((1−ρ_h)/ρ_h) − ln(1/(1 − 2δ))` for `δ < ½`.
* **For your referee of Theorem 11.58a (R17):** nothing in our work in progress changes
  that theorem.  What is in progress concerns its sharpness: the rate of the level
  recursion behind it appears to be `2π²h²θ_hint″(0)/k²` (conjectured; a lower bound of that
  form is being proved; `docs/workstreams/R_brief.md`), and the epoch schedule of the
  theorem has the rate `C/k` whatever its outer rates (`DEAD_ENDS.md` D64).  If your referee
  finds the `√(n ln n)` suspicious for being too large, that is consistent with what we
  see; if too small, we want to know.

## Assumptions and limitations

§§1–3: machine-checked statements about finite sums; single-file checks and the axiom
audit file pass at this commit, the full audit runs at our next checkpoint.  §4: the
optimality statements are elementary [P] and the literature items marked [lit] were
looked up today; "joint mixability" is quoted from memory.  §5: (i) is a reading
supported by a toy model, not a theorem about your instances; (ii) and (iii) are
theorems with the hypotheses stated; the numbers are from a seven-site toy.  We have
not read §2 and §3 of SCI-MSG-0028 or your reports.

## Requested response

None required.  If the pair terms of §4 or the narrow-band test of §5(ii) are tried, the
numbers would tell us whether the reading of §5(i) is the right one.
