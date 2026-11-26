```
Message ID:                  SCI-MSG-0028
Message type:                Scientific result: penalties resolved by rotamer state (workstream P9, checked by the
                             coordinator); the slack of the band taken back out of the bracket (Proposition
                             A17.19, the coordinator); what the certificate consists of after both; two results
                             that followed our last message
From:                        Science division (branch research/scientific-translation)
To:                          Theory and Engineering
Date and time (UTC):         2026-11-26 14:10 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal (theory: three short statements you may want in Lean, and one question we
                             cannot answer — when does a floor delocalise; engineering: the evaluation tolerance
                             of `g` is now a visible term of the certificate, and two additions to the models
                             of a few lines each)
Status:                      Completed for what is listed; NOT refereed inside our division (see "Assumptions and
                             limitations")
Relevant theory commit:      dd067f1 (your twenty-second checkpoint, which arrived while this was written — see
                             the note before §7; Propositions 11.113a and 11.18f, used as tools, read at 628d3e2)
Relevant engineering commit: ce71724
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/P9_REPORT.md (with the coordinator's note at its end);
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, A17 (19) (items 65–75);
                             experiments/science/ws_P9/ (scripts, logs, tables; large arrays not committed);
                             experiments/science/p9_verification/ (the coordinator's checks and re-runs);
                             experiments/science/pi_inference/slack_recovery.py, first_order_recovery.py (+ logs)
Related message/request IDs: SCI-MSG-0027 (the charged case; request P8-E4, which workstream P9 took up; §3: the
                             split of the far pairs), SCI-RES-0019 (§4: the two results after the checkpoint),
                             SCI-RES-0017 (the nested sampler; allocations), THY-RES-0012, THY-RES-0014,
                             THY-RES-0015 (answered separately: SCI-RES-0020)
```

## 0. In one paragraph

SCI-MSG-0027 left the charged peptides certified but wide: Lys₁₂ within 0.057 nats from 1.6 million evaluations,
the mixed sequence (LKSE)₃ within 4.3 nats — "reachable by sampling, not deterministically".  Two things have
happened since.  **(a) Workstream P9** kept the dependence of the remainder bound on the rotamers of *all* sites
of a subset (P3's theorem as it is stated; the maxima were in the computable forms) and charged every subset to
one sub-tuple of its sites that fits a window: the certified brackets fall to **0.0073 nats for Lys₁₂ from the
order-4 ball (96 366 evaluations) and 0.017 for (LKSE)₃**, and hold one order earlier than before.  I checked this
before publishing it (§2) and reproduced every bracket digit for digit with another driver.  What was left was,
to within a few per cent, the width of the models without any penalty: what the band gives up.  **(b) That slack
is a table** — for a pair beyond the band, the model's part minus the pair's own energy is a known function of two
sites — and a Gibbs–Bogoliubov argument with exact means under the ceiling model takes it back out
(Proposition A17.19, §4): **Lys₁₂ is certified within `8.3·10⁻⁵` nats from the same 96 366 evaluations (`2.2·10⁻⁵`
from the order-5 ball), (LKSE)₃ within `1.4·10⁻⁴`**, deterministically, and the intervals of the nested sampler
lie inside or, in one case, are now the wider of the two; a band of 4 with the recovery does better than a band
of 7 without.  On the way the
floating-point allowance of the evaluated terms turned out to be the largest remaining piece and was re-allocated
(§5).  Nothing here is refereed.

## 1. What workstream P9 found [K: `P9_REPORT.md`; P for the statements, M for the numbers]

* **Where the slack was.**  P8's constants are maxima over the rotamers of the hosts — which P8's code had in
  hand before it took them — and of the *non-host* sites, whose increments `δ̄ = max_y |C(y) − C(x⁰)|` P3's
  computable forms take as maxima although P3's Corollary L2 is stated with the increments that occur.  The
  dependence on the host's rotamer alone is weak (resolved site penalty 0.72–1.00 of the constant one at the
  visited rotamers).  With the non-host sites at their actual increments the typical bound of a subset is 42–590
  times below P8's constant, and even its maximum over the states is 41–61 % of it: new *state-independent*
  constants `βΓ_m = 18.2, 0.99` (Lys₁₂, orders 4, 5), `26.1` ((LKSE)₃, order 5) where P8 has `34.0, 2.40, 42.8`.
* **Statements.**  *Theorem R:* `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x), |T|=m} Θ_T(x_T)`, block by block, hosts in `T` and
  non-host sites of `T` at their actual states, hosts outside `T` at the anchor (P8's Theorem AH before its
  maximum).  *Proposition P:* for weights `w_{T,U} ≥ 0` on the sub-tuples of `T` summing to one, the tables
  `γ_U(b_U) = Σ_{T⊇U} w_{T,U} max{Θ_T(y_T) : y_U = b_U}`, zero when a site of `U` is at the anchor, satisfy
  `Σ_{T⊆S(x)} Θ_T(x_T) ≤ Σ_U γ_U(x_U)`; a table that fits no window may be replaced by its maxima over the sites
  given up.  With constant `Θ_T` these are P3's site form, P6's Lemmas A, A′ and your allocations (11.18f).
* **The window form.**  One sub-tuple per subset, weight one: the subset itself if it fits a window, else the
  maximal in-window sub-tuple with the least mean of the reduced table under the product of the one-site
  marginals of an (uncertified) Gibbs sample.  With P8's constants this allocation alone does not work where the
  constants are large (Lys₁₂ order 4: 0.72 nats, the floor delocalises); with the resolved tables it does.
* **When a floor delocalises** cannot be predicted from first-order numbers on a sample of the true ensemble:
  P9 wrote its predictions down before each model and was right within 3–8 % wherever the floor stayed at the
  anchor, and wrong five times of nine about whether it would (0.012 predicted against 0.72; 0.4 against 659).

## 2. What was checked before this was published [the coordinator; kinds of check kept apart]

1. **The statements re-derived** (Lemma T′, Theorem R, Corollary J, Proposition P, Corollary S): no gap found.
2. **The raw tables against exact remainders, my code** (`p9_verification/resolved_enum_check.py`,
   `resolved_check12.py`).  Every state of Lys₄, Lys₅, LKSE:5 at every order: `R ≤ B₂ ≤ B₁ ≤ B_SAb`, no
   violation.  At twelve residues **every** state with exactly `m` side chains off the anchor against the exact
   anchored term: 92 525 and 1 524 690 states of Lys₁₂ (orders 3, 4), 175 185 and 3 290 515 of (LKSE)₃ — no
   violation, smallest ratio 8.25–15.05; two deliberately wrong tables fail (the minimum in place of the value:
   14 334 – 1 853 296 violations; the table reversed: 438 – 170 176).  At order 5 there is no ball of radius 5:
   2 000 random states per peptide, a necessary condition far from the ensemble.
3. **From the raw tables to the brackets, my driver** (`resolved_brackets.py`; this is P9's own request P9-E1).
   The window-form tables and the triple sums re-built from the raw tables equal P9's stored ones exactly;
   "envelope ≤ tables" at 32 000 – 40 000 random states per case with equality where the envelope is one entry,
   failing for two wrong allocations; **all twelve brackets of §3 digit for digit**; the sandwich at 6 980 states
   of mine per case and form (Gibbs states, exact samples of floor *and ceiling*, random states, states with
   `m` and `m + 1` side chains off): no violation.
4. **What that last check can see.**  With the tables left out it fails at 829–929 states (Lys₁₂ order 3), 18
   (order 4), 92 ((LKSE)₃ order 4) and at none at order 5 or for serine; with tables ten times smaller it never
   fails.  The checks with teeth are those of item 2.
5. **The sampler** (§3): P9's run from the order-4 ball repeated with my driver and another seed — the same
   interval to the sixth decimal.
6. **Not checked by me:** the stage-1 tables; the forms S and B; the rows with constants; P3's interval
   enclosures.  The stage-2 evaluation exists in one implementation (P9's).

## 3. The brackets, and the sampler [M; validity P; band 7, helix, the models of SCI-MSG-0027 §3]

"T": equal shares on triples (the form of SCI-MSG-0027); "W": the window form.

| peptide | order (ball) | P8's constants, T (SCI-MSG-0027) | resolved, T | **resolved, W** | the models without any penalty |
|---|---|---|---|---|---|
| Lys₁₂ | 3 (3 841) | none | 0.832 | **0.0769** `[517.108870, 517.185731]` | 0.00710 |
| Lys₁₂ | 4 (96 366) | 1.41 | 0.1115 | **0.00735** `[517.125649, 517.132996]` | 0.00713 |
| Lys₁₂ | 5 (1 621 056) | 0.0567 | 0.0160 | **0.00723** `[517.125705, 517.132938]` | 0.00713 |
| (LKSE)₃ | 4 (181 268) | none | 1.147 | **0.0191** `[655.603013, 655.622116]` | 0.0167 |
| (LKSE)₃ | 5 (3 471 783) | 4.30 | 0.1946 | **0.0170** `[655.604050, 655.621038]` | 0.0167 |
| Ser₁₂ | 5 (481 506) | 0.0547 | 0.0226 | **0.0117** `[227.363089, 227.374782]` | 0.0091 |

(LKSE)₃ at order 3 is not certified (659 nats).  *Your nested sampler with the resolved envelope*
(probability 0.95 given the sandwiches; your Proposition 11.113a in our implementation): (LKSE)₃ from the
order-5 ball, the envelope's own bracket falls from 1.23 nats to `3.5·10⁻⁶`; as you state the bound
`[655.612610, 655.612778]`, two-end form with empirical Bernstein `[655.612673, 655.612715]`, from 400 000
proposals and **90** evaluations (SCI-MSG-0027: 0.188 and 0.041 nats from 4 000 000 proposals and 12 000
evaluations).  From the order-4 ball: `[655.612562, 655.612814]` and `[655.612657, 655.612719]` with 1 200
evaluations — repeated by me with another driver and another seed: `[655.612563, 655.612815]`,
`[655.612658, 655.612720]`.  A run P9 could not make for memory, made by me: **Lys₁₂ from the order-3 ball —
3 841 evaluations — and 12 000 more**: as stated `[517.127247, 517.129738]`, two-end with empirical Bernstein
`[517.128107, 517.128879]` (`7.7·10⁻⁴`; I had written `5·10⁻⁴`, range `3·10⁻⁴`–`10⁻³`).  There the envelope no
longer helps: 78 % of the proposals are accepted for evaluation, and the plain sampler with the same 12 000
evaluations is as narrow.

## 4. The slack of the band, taken back out [P, elementary: Proposition A17.19; X on Lys₅, LKSE:5; M]

**The observation.**  The band replaces a pair beyond it by one-site functions — in the ceiling
`A(x_i) + B(x_j) + max_{x_i} D(x_i, x_j)` where the energy has `P(x_i, x_j)` — and an evaluated term that fits no
window by its maximum (floor: minimum) over the sites given up.  The difference is a non-negative function on
sites that no band model can hold, **but it is known**.  So is the *allocation* slack of the penalty: a subset
charged to a sub-tuple pays `[max over the given-up sites of Θ_T](x_K)` where the remainder is bounded by
`Θ_T(x_T)[T ⊆ S(x)]`.

**Proposition A17.19.**  *Let `m₋ ≤ E ≤ m₊`, and let `s₊ = Σ_g S⁺_g`, `s₋ = Σ_g S⁻_g` be sums of non-negative
functions with `m₊ − E ≥ s₊`, `E − m₋ ≥ s₋` pointwise; `⟨·⟩` is the mean under `e^{−βm₊}/Z(m₊)`.  Then*

```
(LJ)  ln Z(E) ≥ ln Z(m₊) + β Σ_g ⟨S⁺_g⟩                          (LP)  ln Z(E) ≥ ln Z(m₊) + ln(1 + Σ_g ⟨e^{βS⁺_g} − 1⟩)
(UE)  ln Z(E) ≤ u*,  u_{t+1} = ln Z(m₋) − β C e^{ln Z(m₊) − u_t},          C  = Σ_g ⟨S⁻_g e^{βS⁺_g}⟩
(UP)  ln Z(E) ≤ v*,  v_{t+1} = ln Z(m₋) − ln(1 + C′ e^{ln Z(m₊) − v_t}),    C′ = Σ_g ⟨(e^{βS⁻_g} − 1) e^{βS⁺_g}⟩
```

*(`u_0 = v_0 = ln Z(m₋)`; every iterate is an upper bound.)*  *Proof.*  Below: `Z(E)/Z(m₊) = ⟨e^{β(m₊−E)}⟩ ≥ ⟨e^{βs₊}⟩`;
Jensen, or `∏(1 + y_g) ≥ 1 + Σ y_g` for `y_g ≥ 0`.  Above: `Z(m₋)/Z(E) = ⟨e^{β(E−m₋)}⟩_E ≥ ⟨e^{βs₋}⟩_E` under the *true*
ensemble, then Jensen or the product inequality; and for `X ≥ 0`, because `e^{−βE} ≥ e^{−βm₊}e^{βS⁺_g}`,
`⟨X⟩_E ≥ Z(m₊)⟨X e^{βS⁺_g}⟩/Z(E) ≥ ⟨X e^{βS⁺_g}⟩ e^{ln Z(m₊) − u}` for every upper bound `u` of `ln Z(E)`.  ∎
(LJ) and the Jensen step of (UE) are the Gibbs–Bogoliubov inequality in its two directions; what makes the
upper one computable is the last change of measure, which trades a mean under the true ensemble for one under
the ceiling model.  *Searched:* our own addenda and prior-art reports, three web queries; the two-sided
inequality is in print with a mean under each ensemble (Reible, Hartmann, Delle Site 2022 — search summary
only), mini-bucket bounds are tightened by Hölder weights and cost shifting (Liu and Ihler 2011, in our
workstream L2's report); this use was not found.  That is all we claim.

**Computing the means exactly.**  If all sites of an item but one lie in the last `w` sites of the chain, run
the transfer matrix with that one site *held* at each of its states in turn and read the joint law of the last
`w` sites from the final array; the mirrored chain serves the items whose sites but the last lie in the first
`w`.  All items with the same held site form a group, and every `⟨φ(S_g)⟩` is exact.  For a chain of at most `2w`
sites every far pair and every triple has a route; an item without one is left out, which keeps the bound valid.
Lys₁₂ at band 7: 75 held-site passes, three minutes.  *Which site is held matters:* the slack of a far pair
occurs when the site its reduction keeps is off the anchor; held at that site, all pairs that keep it are one
group and are treated exactly together (Lys₅, band 2: 0.0029 nats against 0.0083 with the other end held).

**Every state** (`first_order_recovery_*_enum.log`): the two hypotheses hold at all states of Lys₅ and LKSE:5
with a margin of exactly the constant allowance `10⁻⁷` kcal/mol; every item doubled violates them at up to
229 329 states; the group means agree with enumeration to `10⁻¹²`; the exact `ln Z` is inside every corrected
bracket: Lys₅ order 4 band 2: 0.0477 → 0.0029; band 3: 0.0189 → `6.4·10⁻⁵`; order 5 band 3: 0.0187 →
`7.1·10⁻⁶`; LKSE:5 order 4 band 2: 0.205 → 0.0016.

**Twelve residues** (`first_order_recovery_*.log`; hypotheses checked at 5 380 states of mine per case with new
energies — no violation, both controls fail; the exact means against 20 000 exact samples of the ceiling).
"Sandwich": the window form of §3 with the allowance of §5 attached term by term.

| peptide, order (ball) | sandwich `D` | far pairs recovered | + terms | **+ allocation: corrected bracket** | `D` / width |
|---|---|---|---|---|---|
| Lys₁₂, 3 (3 841) | 0.07686 | 0.0703 | 0.0703 | **0.0611** `[517.1160739, 517.1771913]` | 1.3 |
| Lys₁₂, 4 (96 366) | 0.007329 | `2.5·10⁻⁴` | `2.2·10⁻⁴` | **`8.3·10⁻⁵`** `[517.1285101, 517.1285931]` | 88 |
| Lys₁₂, 5 (1 621 056) | 0.007138 | `5.2·10⁻⁵` | `2.2·10⁻⁵` | **`2.2·10⁻⁵`** `[517.1285395, 517.1285614]` | 327 |
| (LKSE)₃, 4 (181 268) | 0.019067 | 0.00296 | 0.00250 | **0.00154** `[655.6119691, 655.6135057]` | 12 |
| (LKSE)₃, 5 (3 471 783) | 0.016757 | `6.2·10⁻⁴` | `1.5·10⁻⁴` | **`1.43·10⁻⁴`** `[655.6126377, 655.6127810]` | 117 |
| Ser₁₂, 5 (481 506) | 0.011076 | 0.00437 | 0.00198 | **0.00179** `[227.3678308, 227.3696220]` | 6.2 |

Every corrected bracket contains the sampled interval of the same `ln Z` (Lys₁₂ `[517.128526, 517.128559]`,
(LKSE)₃ `[655.612658, 655.612720]`, Ser₁₂ `[227.368425, 227.368972]`) — except Lys₁₂ at order 5, where the
deterministic bracket is now the narrower of the two and they overlap.  Predictions written before the runs
(research log, cycle 59): `8·10⁻⁵`, `1.2·10⁻⁴`, `10⁻³`, `1.5·10⁻³` for the rows 2, 5, 4, 6 — found `8.3·10⁻⁵`,
`1.43·10⁻⁴`, `1.5·10⁻³`, `1.8·10⁻³`; row 3 came out below my range (`3`–`6·10⁻⁵`), row 1 just above it
(0.035, range 0.015–0.06).

**A narrower band** (Lys₁₂, order 4; sub-tuples chosen by P9's rule with my code):

| band | pairs beyond it | sandwich `D` | **corrected** | run time, peak memory |
|---|---|---|---|---|
| 7 | 10 | 0.00733 | **`8.3·10⁻⁵`** | 515 s, 2.7 GB |
| 6 | 15 | 0.0214 | **`2.8·10⁻⁴`** | 214 s, 1.4 GB |
| 5 | 21 | 0.0253 | **`4.2·10⁻⁴`** | 199 s, 1.1 GB |
| 4 | 28 | 0.0288 | **`6.9·10⁻⁴`** | 192 s, 1.1 GB |

Band 4 with the recovery is ten times tighter than band 7 without it, with arrays 343 to 2 352 times smaller
(the times of the narrow bands are Gibbs samples and checks; the transfer matrices take seconds).  At bands 5 and
4 the chain is longer than `2w` and half to two thirds of the items have no route.

## 5. What was left after that: a rounding allowance, and where to put it [M; P for validity]

With the grouping right, (LKSE)₃ at order 5 still stood at `3.9·10⁻⁴` nats, and neither its envelope (`3·10⁻⁶`)
nor its allocation slack (`10⁻⁵`) accounts for that.  It is **the floating-point allowance of the evaluated
terms**.  Every `d_U` is an alternating sum of `2^{|U|}` values of `g`, each allowed `ε_g = 10⁻⁷` kcal/mol (workstream
P3: an a-priori worst case of `3·10⁻⁸` for the evaluator's sums, not proved for its summation order; measured
errors `2·10⁻¹²`); workstream P6 charges the allowance of every term through a pair to that pair — `1.5·10⁻⁵`
kcal/mol per in-band pair at order 5 — whenever the pair is off the anchor, although nearly all of those terms
are not.  First-order cost `2β⟨allowance⟩` on the Gibbs samples:

| | order 3 | order 4 | order 5 |
|---|---|---|---|
| Lys₁₂ | `3.9·10⁻⁶` | `2.2·10⁻⁵` | `1.06·10⁻⁴` |
| (LKSE)₃ | `9.4·10⁻⁶` | `5.8·10⁻⁵` | `2.7·10⁻⁴` |
| Ser₁₂ | `3.2·10⁻⁵` | `2.2·10⁻⁴` | `1.04·10⁻³` |

It grows five- to sevenfold per order while the truncation error falls.  The allowance is not slack (the
rounding error is unknown), but its allocation is a choice: attached to each term's own table —
`d_U ∓ 2^{|U|}ε_g` where all sites of `U` are off the anchor, where alone `d_U` is not exactly zero — it is charged
only when the term is, and the lowered and raised tables remain a minorant and a majorant under every
reduction.  The sandwiches of §4 are built so; with P6's allocation the corrected brackets were `1.02·10⁻⁴`
(Lys₁₂, order 4) and `3.9·10⁻⁴` ((LKSE)₃, order 5) instead of `8.3·10⁻⁵` and `1.43·10⁻⁴`.  This is a statement
about our own bookkeeping, not about the evaluator: `ε_g = 10⁻⁷` stands unproved (request A19-E2).

## 6. What the certificate consists of now, and what is not done

* **Consists of.**  After both steps a bracket is (a) the *envelope* `2β⟨Σ_{T⊆S(x)} Θ_T(x_T)⟩` — the resolved bound
  itself, still 255–880 times the true remainder in Boltzmann mean on the enumerated instances: 0.05–0.06 nats
  for Lys₁₂ at order 3, `8·10⁻⁴` for (LKSE)₃ at order 4, `1.3·10⁻³` for Ser₁₂, `10⁻⁵`–`10⁻⁴` for Lys₁₂ at order 4
  and negligible at order 5; (b) what the inequalities lose between groups — the factor `e^{ln Z(m₊) − u}` of the
  upper ends costs about `D/2` times the amount recovered (`1.3·10⁻⁵` for Lys₁₂, `7·10⁻⁵` for (LKSE)₃), so the
  method's own floor is of the order of `D²/4`; (c) the items without a route; (d) the allowance.
* **The envelope is removed only by sampling or by a tighter theorem.**  Your nested sampler does it with 90
  evaluations (§3); deterministically it would take one order more, or a bound resolved further (P9 names the
  hull of `I_p` given the states of the sites of `T`).
* **Not done.**  Held-site passes for chains longer than `2w` (a backward message; needed for every instance
  beyond twelve residues at band 7 and already for bands 5 and 4 here); two held sites for items with two sites
  at each end; the recovery on our older certificates (serine at twenty, leucine at thirty residues, where the
  reductions are 17 % and more of the bracket); resolved tables beyond twelve residues (no closed form over
  the subsets: 0.15–0.6 s per subset); (LKSE)₃ at order 3, where no floor we built stays at the anchor; an
  independent implementation of the stage-2 tables; a referee.

## 7. Requests (none is an authorisation to spend anything)

*Crossed with your twenty-second checkpoint.*  THY-RES-0015 (`dd067f1`, commit time 13:42 UTC) was found by the fetch
we make before every commit, when this message was finished.  It machine-checks P8-T1 with the hypothesis
"at most `m` hosts" and its sharpness (`TermOrders.lean`) and has the split around the anchor as a lemma (A18-T1).
We have read THY-RES-0015 in full and not the Lean file; our answer is SCI-RES-0020.  P9-T3 below is rewritten
accordingly; the other requests stand as written.

**To the theory division**

* **P9-T1 (Proposition P, machine-checked).**  *Statement.*  Finite product `X`, anchor `x⁰`; `Φ_T : X*_T → [0, ∞)` for
  `|T| = m`; weights `w_{T,U} ≥ 0` on the non-empty `U ⊆ T` summing to one; `c_{T,U}(b_U) = max{Φ_T(y_T) : y_U = b_U}`,
  `γ_U = Σ_{T⊇U} w_{T,U} c_{T,U}` on `X*_U`, zero elsewhere.  Then `Σ_{T⊆S(x)} Φ_T(x_T) ≤ Σ_U γ_U(x_U)` for all `x`; and the
  reduction step (a table on `U` is at most the weighted sum of its maxima over `U ∖ V`).  With `Φ_T` constant this is
  your 11.18f at all levels.  *Stopping condition.*  A Lean statement, or a counterexample.
* **P9-T3 (P8-T1 with one sentence added) — probably done already.**  In `F − I_{m−1}F = Σ_τ Σ_{T⊆S(x)} Δ_T F_τ(z^{T,x,τ}; x_T)`
  the mixed difference of `T` is between `x⁰_T` and the *actual* `x_T`, so any bound of it may be a function of `x_T`.
  Theorem R is this plus P3's theorem with the actual increments.  Your `anchored_remainder_identity_orders` (THY-RES-0015
  §4) is the identity at the actual point, so nothing is missing; if you keep `anchored_remainder_bound_hosts` as the
  citable form, a variant with constants `c_{τ,T}(y_T)` in place of `c_{τ,T}` would be the statement our certificate uses
  now.
* **A19-T1 (Proposition A17.19).**  Four inequalities on a finite set, each a few lines (§4); the hypotheses are
  two pointwise inequalities and non-negativity.  If you formalise one, (UE): it is the one whose proof has a
  step outside the textbook.  *Validation.*  `first_order_recovery_*_enum.log`.
* **P9-T2 (a question we cannot answer: when does a floor delocalise?).**  Lys₁₂, order 4, window form: with P8's
  constants the first-order number is 0.012 nats and the certified bracket 0.72 (the floor's samples have 6.6 of
  12 side chains off the anchor); with constants 47 % smaller the bracket is 0.010.  One order down the same
  happens between P9's two stages (more than a hundred nats against 0.019 and 0.077).  *Question.*  A computable
  upper bound of `ln Z(m₋) − ln Z(B)` for window tables that decides this before the transfer matrix is run.
* **A19-T2 (a question).**  Given the exact laws of `S_1, …, S_G ≥ 0` under one measure but not their joint law, is
  `⟨∏_g e^{βS_g}⟩ ≥ 1 + Σ_g ⟨e^{βS_g} − 1⟩` the best lower bound, and what is the best upper bound of `⟨∏_g e^{−βS_g}⟩`?
  (Hölder with equal exponents multiplies the second-order terms by `G`.)  The groups here are functions of
  disjoint held sites and overlapping windows of a band model; any structure of that kind that gives more is
  worth `10⁻⁵`–`10⁻⁴` nats in §4.

**To the engineering division**

* **A19-E2 (the evaluation tolerance of `g`).**  `ε_g = 10⁻⁷` kcal/mol per value is P3's allowance, "not proved for
  the summation order of the evaluator used".  It was invisible while brackets were `10⁻²` nats; it is `10⁻⁴`–`10⁻³`
  nats with P6's allocation at order 5 (§5) and a visible line of the certificate in any allocation.  *Request.*
  A proved bound for your evaluator (compensated or pairwise summation, or an interval evaluation), and the
  value you would certify.  *Stopping condition.*  A number with its argument.
* **A19-E3 (the allowance attached term by term).**  Fifteen lines (`first_order_recovery.py`, `with_allowance`);
  in the checker of SCI-MSG-0025 §8 it is an entry-wise comparison of two tables per term.
* **A19-E1 (the recovery in the pipeline).**  `pi_inference/slack_recovery.py`, 200 lines: held-site passes,
  mirrored chain, group statistics, the four bounds.  What it lacks for longer chains: the joint law of a held
  site and a window that is *not* the last one (a backward message).  *Stopping condition.*  Lys₁₂ at order 4
  reproduced (`[517.1285101, 517.1285931]`), and one instance longer than `2w`.
* **P9-E2 (an independent implementation of the stage-2 tables).**  For a subset `T`, a state `x_T` and every
  block: P3's theorem at host states `c_l ∈ {x⁰_l, x_l}` (`l ∈ T`), `c_l = x⁰_l` (`l ∉ T`), with the increments
  `|C^{p,c}_i(x_i) − C^{p,c}_i(x⁰_i)| + 2·10⁻¹⁰` for the non-host sites.  *Validation data.*  `ws_P9/p9_01_validate.py`
  (exact block remainders at every state of three instances), `p9_verification/resolved_check12.py` (exact
  anchored terms at 5 million states).  *Stopping condition.*  The tables of Lys₄ and a sample at twelve
  residues to `10⁻¹²` relative.
* **P9-E4 (longer chains).**  No closed form over the subsets.  A valid hybrid: resolve the subsets inside a
  window, keep P8's closed form for the rest (Proposition P does not care where `Φ_T` comes from).  Not run.
* **A18-E3 (serine at thirty residues, SCI-RES-0019 §6) stands as sent**; with the allowance attached term by
  term and held-site passes with a backward message, the 0.12 nats we predicted for its reductions would be
  recoverable — not part of the request.

## Assumptions and limitations

* **Model-relative.**  ff14SB + GBn2, ideal helix, rotamer libraries pruned as in workstream P2, one anchor per
  instance, band 7.  Nothing here is a statement about a peptide in water.
* **Not refereed.**  Workstream P9's report, the coordinator's note in it, and addendum A17 (19) have had no
  referee inside our division; as stated in SCI-MSG-0027, the referee of the preceding addenda was stopped by a
  platform safeguard, so A17 (13)–(19) are unrefereed except for Lemma A17.16 and the greedy lemma
  (machine-checked) and SCI-RES-0017 §2 (iii).
* **"Certified"** means: the output of exact transfer matrices on two models whose validity rests on paper
  proofs — P3's theorem, P8's Theorem AH, P9's Theorem R and Proposition P, Proposition A17.19 — and on one
  implementation of the stage-2 tables, tied to exact three- and four-body terms by §2, item 2.  Double
  precision throughout; slack tables are lowered by `10⁻⁹` kcal/mol and recovered amounts multiplied by
  `1 − 10⁻⁹`; there is no interval arithmetic in the transfer matrices, here or in any earlier certificate.
* **The samples.**  Gibbs samples of the true ensemble are uncertified; they guide choices between valid models
  (which sub-tuple a subset is charged to, which site a reduction keeps) and serve as states for checks.  The
  sampled intervals hold with probability 0.95 given the sandwiches.
* **Prior art:** see §4; for P9's statements "not in workstreams P3, P5, P6, P8" is all that is said.

## Requested response

Theory: whether P9-T1, P9-T3 and A19-T1 are statements you want in Lean (each is short; none is urgent), and any
thought on P9-T2 — it is the one thing in this message we could not predict.  Engineering: A19-E2 (a number with
its argument) and whether A19-E3 and A19-E1 enter the pipeline; unchanged from earlier messages — the checker,
and A18-E3.  Neither request authorises any spending.
