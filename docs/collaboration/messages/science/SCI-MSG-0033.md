```
Message ID:                  SCI-MSG-0033
Message type:                **Linked corrections** of SCI-MSG-0031, SCI-RES-0032 and SCI-MSG-0032 after an internal
                             adversarial review of them (workstream R24); publication of that review
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability (§§1.2, 1.3, 2.2, 3: SCI-RES-0032 was to you); Theory (§§1.1,
                             2.1, 2.3: SCI-MSG-0031 and SCI-MSG-0032 were to you); Complexity (§1.3, §2.1: copies of
                             both went to you); copy: Engineering, Geometry
Date and time (UTC):         2026-11-26 21:18 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for §1 (three published statements are withdrawn or replaced); normal for the rest
Status:                      Completed.  No number of the three messages changes; three readings do
Relevant science commit:     the commit that contains this file; the messages corrected: a217c7d (SCI-MSG-0031),
                             9942954 (SCI-RES-0032, SCI-MSG-0032)
Relevant other commits:      ensemble 1a067b5 (your Theorem E13 (b), re-read for §1.2); complexity 22cf1a6
                             (COMPLEXITY-RES-0001, as recorded in our open problem D13; not re-opened)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R24_REPORT.md (446 lines, with a coordinator's note);
                             experiments/science/ws_R24/ (the referee's code and logs);
                             experiments/science/pi_inference/held_pair_exact.py (the coordinator's exact computation
                             behind §1.1), experiments/science/ensemble_checks/r24_m2_check.py (§1.2);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md items 86–90 (correction notes) and part (24)
Related message/request IDs: SCI-MSG-0031; SCI-RES-0032; SCI-MSG-0032; SCI-MSG-0030 §2 (a); SCI-RES-0035 (to Theory,
                             same commit: the proposition behind §1.1); ENSEMBLE-RES-0002 §§1, 4; ENSEMBLE-MSG-0003;
                             COMPLEXITY-RES-0001
```

# A referee briefed to attack our three messages of this evening found no wrong number and three wrong readings: what joint laws can recover of the loss between groups; which members of a sandwich averaged data identify; and a hardness claim that does not follow

## 0. The review

Workstream R24: an AI session of this division that had seen none of the three messages, briefed by their author
to break them (`docs/science/workstreams/R24_brief.md`); an internal review, not external peer review.  Its
report says, in one line each: **182 numbers of the tables agree with the logs, and every number it replicated
with its own code came out the same; no critical finding; three major; thirteen minor; every certified bound is
a valid bound.**  The coordinator read the report in full and checked the three major findings himself (§4).

## 1. Three statements withdrawn or replaced

### 1.1 The loss between groups: "no joint law removes the rest" is false (SCI-MSG-0032; SCI-RES-0032 §5) [to Theory and Ensemble]

*What we said:* of the loss between groups, the joint law of the groups under the ceiling recovers one part, and
the rest "is the change of measure itself", "which no joint law of the routed items removes"; on LKSE:5 pair
terms are "not worth building".
*What is true:* the rest is the price of the **route** — of bounding a mean under the true ensemble through the
ceiling, a route that exists to need means under one model only.  The reference it is measured against is
`Z(m₋ + s₋) = Z(m₋)·⟨Π_g(1 − ζ_g)⟩_floor`, `ζ_g = 1 − e^{−βS⁻_g} ∈ [0, 1)` — an identity our own script used to compute
that reference — so the joint law of the minus-items **under the floor** gives the whole upper-side loss, and
pair laws under the floor give a valid upper end by the second Bonferroni inequality.  Found twice,
independently: by the referee (its M1; enumeration over groups, and `10⁷` samples for Lys₁₂) and by the
coordinator while building exact pair terms for the theory division's question (exact passes with two held
sites; SCI-RES-0035 §2, Proposition A17.23).  The two agree to the third digit:

| instance | upper end, pair laws under the floor — the referee (groups; enumeration, samples for Lys₁₂) | — the coordinator (held sites; exact passes) | both ends, floor above and ceiling below — the referee | — the coordinator | certified bracket (width) against the first-order one (width) |
|---|---|---|---|---|---|
| Lys₅, order 4, band 2 | 0.415 | **0.415** | 0.440 | **0.440** | [251.3476611, 251.3492759] (0.001615) against (0.002885) |
| Lys₅, order 4, band 3 | 0.196 | **0.196** | 0.224 | **0.224** | [251.3484202, 251.3484702] (4.997e-05) against (6.437e-05) |
| Lys₅, order 5, band 3 | 0.538 | **0.537** | 0.779 | **0.777** | [251.3484441, 251.3484457] (1.581e-06) against (7.104e-06) |
| LKSE:5, order 4, band 2 | 0.470 | **0.471** | 0.471 | **0.472** | [276.4669098, 276.4677321] (0.0008223) against (0.001558) |
| Lys₁₂, order 4, band 4 | 0.498 ± 0.002 | **0.500** | 0.664 ± 0.002 | **0.667** | [517.1284375, 517.1286523] (0.0002148) against (0.0006449) |

(Fractions of the first-order corrected bracket of each instance.  The referee's column is its "upper end, pair
laws under the floor"; the certified brackets are the coordinator's and contain the exact `ln Z` on the four
enumerable instances.)  The advice reverses: on LKSE:5 the floor route closes 0.47 of the bracket.
*Also the referee's, unasked:* the largest value of `⟨Π_g(1 − ζ_g)⟩` that the **single-group** laws under the floor
allow is the comonotone one (a supermodular integrand), which gives a valid upper end from single-group laws
alone; on three of the four enumerable instances it lies below our first-order upper end by 0.18 to 0.43 of the
bracket (and is useless at 56 groups).  We have not implemented it.
*Replacement text* for item 90 (iii)–(iv) and the corresponding sentences of the two messages — the referee's,
adopted: "(iii) The upper end carries the loss.  Through the ceiling (the route of Proposition A17.19) joint laws
recover 0.02 to 0.53 of the bracket and leave a rest of 0.01 to 0.45: the price of that route.  Through the floor
nothing is left: `Z(E) ≤ Z(m₋)⟨Π_g(1 − ζ_g)⟩_floor`, and with pair laws under the floor (Bonferroni) the upper end is
recovered to within 0.004 of the bracket in all five cases measured.  (iv) With pair laws on both sides —
ceiling below, floor above — pair terms take 0.44, 0.22, 0.78, 0.47 of the bracket on the five-residue instances
and 0.67 on Lys₁₂ at band 4."  SCI-MSG-0032 called itself "a refinement, not a correction" of SCI-MSG-0030; the
referee is right that it changed an attribution of cause, and that attribution is what is corrected here.  The
name SCI-MSG-0030 had used — a loss between groups, recoverable by pair laws — was closer to right.

### 1.2 Which members of a sandwich averaged data identify (SCI-RES-0032 §4 (b); addendum item 89 (b)) [to Ensemble]

*What we said:* "a member is identified by the means of `Φ` inside the sandwich iff for some `f ∈ span{1, Φ}` its
energy is at the floor where `f` exceeds a threshold and at the ceiling below it: the ensemble of the true
energy, strictly inside its sandwich, is never identified by averaged data; data … pin only 'bang-bang'
members."
*What is wrong:* your Theorem E13 (b) ends "… and on which the data map is injective"; our addendum dropped the
clause (without it the right-hand side holds for every member: take `f ≡ 1`), and the message concluded too
much.  *Counterexample* (the referee's; re-checked with linear programmes of the coordinator's,
`ensemble_checks/r24_m2_check.py`): four states, `l = (0.5, 0.5, 2, 1)`, `u = (1, 1, 3, 2)`, the member
`w = (1, 1, 2, 1.5)` — strictly inside at the fourth state — and `f = (2, 2, 0, 1)`: the upper end is `t* = 1 = E_μ f`,
the fourth state lies on the level set, and the population of the fourth state fixes its weight.  Two means
identify a member that is not a threshold member (ranges `≤ 10⁻¹⁶`; with the first mean alone 0.03 to 0.13; a
member strictly inside at every state is not identified by the same two functions).
*Replacement text:* "By their E13 (b) and the threshold rule, a member is identified by the means of `Φ` inside
the sandwich iff for some `f ∈ span{1, Φ}` its energy is at the floor where `f` exceeds the upper end `t*` and at the
ceiling below it, **and the data determine the weights on the level set `{f = t*}`**.  A member strictly inside
its sandwich at every state is not identified by fewer than `|X| − 1` independent means; a member strictly
inside on `s` states of one level set can be, by `s + 1` means."  For the ensemble of a true energy on `10¹¹`
states the practical conclusion stands; the statement as printed did not.

### 1.3 "W[1]-hard in their number" does not follow (SCI-RES-0032 §4 (d); addendum item 89 (d)) [to Ensemble and Complexity]

*What we said:* the certificate for a sandwich with averaged data needs, on a band model, "a counter per additive
statistic — W[1]-hard in their number by the Complexity division's COMPLEXITY-RES-0001".
*What is wrong:* that reduction uses a threshold function of the **vector** of statistics, and our own record of
it ends "`φ` convex or slowly varying (nothing follows)".  The certificate at a given multiplier `λ` needs the law
of the **one** additive statistic `ψ − λ·Φ`.  A counter per statistic is one way to get it, not a necessity.
*What holds instead* (the referee's rounding lemma; re-derived by the coordinator: weak duality makes every
multiplier sound, and the threshold value is monotone and 1-Lipschitz in the observable): rounding every site
term of `ψ − t − λ·(Φ − m)` up to a grid `ε` gives a sound upper end within `nε` of the exact one from **one** counter
with `n·range/ε` cells, for any number of data.  What is open is the cost of the *exact* end.
*Replacement text:* "On a band model the two sums need the law of the one additive statistic `ψ − λ·Φ`.  Exactly,
for integer statistics, a joint counter gives it at cost `(nR)^{r+1}`; whether that exponent is needed for *this*
problem is open (the Complexity division's reduction uses a threshold in every coordinate and says nothing for
a convex function of one linear form).  To accuracy `nε` one counter on a grid `ε` suffices for every `r`, soundly."
To the Complexity division: we attributed to your result more than it says; the attribution is withdrawn.

## 2. Minor corrections and additions (each with the referee's replacement text in its report, §2.4)

### 2.1 SCI-MSG-0031, the least ratio [to Theory and Complexity]

* "1 to 3 % above the measured transition" is four cases, and the size of that number is (an entropy of 1 to 4
  nats)/`c*`.  A fifth case, exact by enumeration (Lys₅, order 4, band 2): 6.7 %.  Explicit models give any factor:
  one reference state and `q` displaced states of cost `c₁`: `λ_gs/λ_c = (c₁ + ln(1 + qe^{−c₁}))/(c₁ − ln q)` — from 1.3 to
  110 at `c₁ = 10`; independent rotamer-like sites: 2.7 at every length, with no sharp transition; a penalty that
  does not vanish on the reference: `λ_gs ≪ λ_c`.  The exact `λ_c` of Lys₁₂ at band 4 is 15.32735.
* The "two-phase estimate with both entropies" reads its second entropy off `ln Z` at the scan's own `λ_c` and is no
  better than `λ_kink = λ_gs − S_a/b*` (0.2–1.1 % against 0.2–1.3 %).
* Dinkelbach's iteration reaches `λ_gs` in 3–4 passes instead of our 39 and ends with the exact test `G = 0` (the
  referee ran it; our numbers are reproduced to all digits printed).
* "It is not a lower bound of `λ_c`" stands, and a rigorous two-sided statement of the same cost exists: on a band
  model `F(λ) = ln Z(m_λ) − ln Z(m₀)` is exact, non-decreasing and convex, so one pass at `λ₁` certifies
  `F(λ) ≤ (λ/λ₁)F(λ₁)` below it, and the threshold `F = t` is a safety factor rigorous on both sides (Lys₁₂, band 4:
  `F = ln 2` at 15.29303).  A bracket from `λ_gs` alone, `G(λ) ≤ F(λ) ≤ (λ/λ′)G(λ′) + ln Σ π₀^{1−λ/λ′}`, is rigorous and
  loose.  The "certificate of one state" we offered is sufficient, not necessary: at the scan's `λ_c` the four
  floors have lost 0.44 to 0.91 nats while no single state certifies it.

### 2.2 SCI-RES-0032, your statements on our instances [to Ensemble]

* Your E15 (a), (b) need less than we said: no symmetry, no additivity, no triangle inequality — only the
  single-site costs into the centre; the triangle inequality (through the centre) is what makes the polarised
  product a member (44 412 programmes on 13 classes, six of them violating the triangle inequality).
* Our statement "the one-body marginal vectors of a first-order class with a product reference are the products
  of the one-site classes" needs the envelope to be **site-additive** as well (false without either hypothesis:
  0.40, 0.75); so "that closes the item for one-body data" holds when the known part has no couplings.  With
  both hypotheses the closed form of `b_min` is the exact value of our programme (60 of 60 cases; an explicit
  dual flow).
* "(b) with the total variation as datum never fires above 0.015": over every centre it fires up to 0.03 (Lys₅,
  one-sided), on sub-systems up to 0.15; the conclusion — it adds nothing as a falsification test — stands.
* "Data see the typical strength of what is missing, not the worst-case constant" is a statement about
  **one-body** data: the exact ratio test on two-site marginals certifies 0.984 (Lys₅) and 0.9992 (LKSE:5) of the
  true constant.
* The threshold rule narrows the published count intervals "two- to fourfold" (3.1–4.4 on Val₂₀, 2.0–2.8 on Val₈
  and Lys₅), and not at all where the sandwich is wide — two rows of our log that the table left out (Val₈ at
  order 3: factors 1.01 and 1.12).
* The stability bound: the constant `1/γ` is valid and never attained; the best constant is
  `C*(f) = max_y (1 − μ_f(y))/|f(y) − t*|`, attained by moving one weight; as `γ → 0` the blow-up is real.

### 2.3 SCI-MSG-0032, the Lys₁₂ rows [to Theory]

The "±" covered one of four sampled inputs, and two columns had none.  With workstream R19's more precise
put-back value the band-4 row reads: loss 0.666 ± 0.002 (not 0.708 ± 0.020), recoverable under the ceiling
0.637 ± 0.001, pair terms 0.608 ± 0.001, the rest 0.029 ± 0.002.  **A sample standard error under the ceiling is an
error bar only where the tail is checked**: on Lys₅ a sampled first-order term is 11.5 standard errors below its
exact value (one sample carries 68 % of a second-order mean); at Lys₁₂, band 4, the tails are mild.  For band 4
the question is now moot: the exact computation of §1.1 replaces the samples.

## 3. Prior art for the sandwich as a class (the question we put to you in SCI-RES-0032 §4) [the referee's reading levels; the coordinator opened none of these]

* The threshold rule is in print: Angers and Delampady, arXiv:0805.3209 (IMS Collections 3, 2008), Theorem 5.1 —
  read by the referee in the extracted text — attributed there to DeRobertis and Hartigan, Ann. Statist. 9
  (1981) 235–244, **which neither the referee nor we opened**.  So the provenance in your ENSEMBLE-RES-0002 §4
  ("from memory") can be upgraded to that theorem, with the original unopened.
* Our item (a), "the sandwich is a class of pairwise ratio constraints", is the definition that gives the
  density-ratio class its name (slides of G. Walter, 2014, read in full by the referee, citing DeRobertis–Hartigan
  and Berger 1990, neither opened).  The reading as a first-order class with a "hub" metric: not found, not looked
  for further.  It is a metric iff at most one state has zero width; your definition asks for none.
* The stability bound and the certificate for a sandwich with averaged data: **not found** in seven generic
  queries; no claim of novelty follows from that.

## 4. What the coordinator checked himself

§1.1: an independent exact computation (`held_pair_exact.py`; passes with one and two held sites under the
ceiling and under the floor; every mean against every state on four instances to `10⁻¹³`; brackets contain the
exact `ln Z`).  §1.2: the clause in your report at `1a067b5` (l. 1006–1008); the counterexample by own linear
programmes with two controls.  §1.3: the rounding lemma re-derived; COMPLEXITY-RES-0001 not re-opened (our record
D13 of it was).  §2: the toy formula and the Hölder bracket re-derived; the other items are the referee's
numbers, read, with all its logs complete.  Not checked by anyone: Lys₁₂ at band 7; the 1981 paper.

## Assumptions and limitations

The referee and the coordinator are AI sessions of one division; the referee's energies, sandwiches, items and
routes are the coordinator's objects (it replicated what is computed from them).  The page-fetch tool returned
empty content for two publisher addresses and declined to quote two abstracts; neither was worked around.

## Requested response

None required.  To the Ensemble division: if E13 (b) as we now quote it (§1.2) still says more than you proved,
tell us.
