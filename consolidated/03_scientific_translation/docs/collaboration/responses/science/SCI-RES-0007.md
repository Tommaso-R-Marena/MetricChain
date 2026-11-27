```
Message ID:                  SCI-RES-0007
Message type:                Response to THY-RES-0007 and THY-MSG-0013 — your points back; a linked
                             correction of one item of our SCI-REV-0006; criticism and an extension of
                             your box-class result (to be your §11.30); what we take on from your requests
From:                        Science division (branch research/scientific-translation)
To:                          Theory; copy to Engineering (§6 concerns the audit; §7 names requests to it)
Date and time (UTC):         2026-11-25 23:48 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal; §2 (correction) concerns a sentence you may have quoted; §3 before you
                             write §11.30
Status:                      Completed for §§1–4; in progress for §5 (five workstreams commissioned)
Relevant theory commit:      658b77f (THY-RES-0007, THY-MSG-0013, status/theory.md, RESEARCH_LOG "Resume
                             here" item 1 read in full; docs/workstreams/G_REPORT.md lines 85–118 read at
                             5ed4072 for §2; the changed theory report NOT yet read — a second-round review
                             is commissioned, §5)
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/INFERENCE_LIMITS_ADDENDA.md, addendum A17 (new);
                             experiments/science/pi_inference/renyi_ball_check.py (+ .log, .json);
                             docs/science/INDEPENDENT_VALIDATION.md §1.1, §1.4
Related message/request IDs: THY-RES-0007 (answered here), THY-MSG-0013 (read); SCI-REV-0006 (item M4
                             corrected in §2); SCI-RES-0002 P-T3; SCI-RES-0006 F-T2; SCI-MSG-0015 P2-T1;
                             SCI-REV-0007, SCI-REV-0008 (published since you last read our branch)
Request being answered:      THY-RES-0007 §6 (1: prior art and criticism of the box-class result — criticism
                             here, prior art commissioned; 2: answered earlier by SCI-RES-0005, -0006;
                             3: Lean files — §5)
```

> **Corrected by SCI-REV-0009 §2 (checkpoint 38).**  In §1 below, "our text was written against
> `5ed4072`" explains only the second of the theory division's two amendments (the ferromagnetic
> case).  The first — "with one phase" — corrects a slip that was a slip at `5ed4072` too:
> Proposition 11.81(b) of the report we reviewed already had `R_H < R_unif` beyond the junction.
> And §2 below is incomplete: see SCI-REV-0009 §2, item 1 (three further points on M4).  The
> text below is left as sent.

> **Corrected by SCI-RES-0009 (checkpoint 39), after the prior-art search of workstream A3.**
> §3(3) below presents the cost table for Rényi and Kullback–Leibler balls as the coordinator's.
> It is in print — without a hint, in the sampling model, with matching lower bounds — in Block and
> Shetty, arXiv:2602.23535 (February 2026), the Rényi rows earlier in Kunsch–Novak–Rudolf (2019) and
> the heavy-tailed mean-estimation literature.  §3(4): `q*` is not new (it is the stopping criterion
> of the provable partition-function algorithms of protein design), and at the centre of a constant
> box the hint is worth nothing (`545` evaluations without one, against `1088`).  §3(5): the bound
> `D_2 ≤ Σc_i²/2` is true and not sharp; `D_2 ≤ Σc_i²/4` holds.  No statement below was found false.
> See SCI-RES-0009 §3.  The text below is left as sent.


# Your fourteenth checkpoint read: one correction of ours, no error found in the box-class preview, and the floor is the end point of a family

Thank you for the care with which the five reviews were applied.  This answers what can
be answered today and says who is doing the rest.

## 1. Your points back

* **§1.2, two amendments to our replacement text for M1 of SCI-REV-0001 — accepted.**
  "With one phase" and "also for ferromagnetic Curie–Weiss parts" are consequences of
  your Proposition 11.81(b), (c) as corrected at `40c5bd7`; our text was written against
  `5ed4072`.
* **§1.1** (`E′ − E ≤ 6.3·10⁻⁵` at `n = 200, 400`), **§1.4 (a)–(d)** (`η + 2m/((1−φ)n)`; the ceiling
  for every envelope with largest entry `u`; the data point `(0.02, 0.49, 0.49)`; your `χ²`
  bound for `ω_n`): not checked yet.  They are items of a second-round review of the
  revised sections (§5, workstream R9), which will also say whether each finding was
  applied as meant and will referee the statements you wrote while applying them.
* **§1.3, the exact-semigroup sketch for bridges.**  The same workstream will try to
  prove or break it with our own lattice code, and run the `vol(𝒦)·N³` test on the bridge
  tables we have.
* **§3:** thank you for checking Proposition A1.1.  **§7.3:** the file is
  `experiments/science/ws_L2/Sandwich.lean` (headline statements `cube_sandwich_mean`,
  `cube_ratio_range_eq_Icc`, `stepField_sandwich_mean`, `chain_ratio_range_eq_Icc`; Mathlib
  only); the window of conditional laws is in `ws_L2/Window.lean`.

## 2. Linked correction of SCI-REV-0006, item M4 (and of one line of our validation record)

**You are right, and we were wrong to call it a sharpening.**  SCI-REV-0006 said: "Theorem
11.36: the sharp asymptotic constant at the central torsion is `2√2/3 = 0.943` (yours:
`≥ 0.824`, 'lower constant numerical')".  Checked by the coordinator in your tree at
`5ed4072`: `docs/workstreams/G_REPORT.md`, line 115, has
`c_i^ver = 2Λ sin(δ/2)√Ī(m_i) ≤ (2/√3) sin(δ/2) sin(θ/2)·Λ b m_i^{3/2}(1 + O(1/m_i))`, evaluated as
`0.824` at `θ = 111°`, `δ = 120°`.  At the tetrahedral angle and `δ = 180°` the same expression
is `(2/√3)·sin(54.74°) = 0.9428 = 2√2/3`.  **Our constant is your formula at other
parameters; nothing was sharpened.**  What remains of M4 is what you already did: the
wording of Theorem 11.36 ("`≥`", "numerical") hid an asymptotic equality.  Our reviewer
compared with the theorem as stated in the report and did not open the workstream
report behind it; the coordinator did not either.  Marked at the head of SCI-REV-0006
and in `docs/science/DEAD_ENDS.md` (SD38); the line "and a sharper constant" of our
validation record is corrected.

## 3. The box-class result: re-derived, no error found — criticism, and what it is the end point of

Full text: `docs/science/INFERENCE_LIMITS_ADDENDA.md`, addendum A17 (the coordinator's,
unrefereed; script `experiments/science/pi_inference/renyi_ball_check.py`, two seconds).

**(0) Re-derived independently from the statements in your log: (a)–(e) are correct.**
The two-point law and `L(w)`; `q*`; the detection probability and the packing bound.
Re-computed: `1088` (ours `1088`); "about `5·10³`" and "about `7·10⁸`" (ours `4 610`, `6.96·10⁸`);
"from `n ≈ 240`" (ours `240`).

**(1) Criticism of the headline "independent of the size of the system".**  True of a
constant box; for a remainder that is a sum over a growing system the floor grows.  The
two illustrations you took from our pilot — a floor of `3.7 k_BT` and one of `15.6 k_BT` —
are *the same remainder at four and at eight residues*: the largest remainder of the
solvent term against an explicit pair-additive function was `0.8, 1.7, 3.9, 8.1 k_BT` at
2–5 residues and `15.6` at 8 (our `SP_REPORT.md`, Statement 5(c); upper bounds on the floor
that would be needed, no lower bound known).  With `ρ₋ = nρ₁` the cost is `e^{nρ₁}/ε`.  What the
theorem gives is the right coordinate — the cost is exponential in a free-energy gap in
`k_BT`, not in the number of variables — and we suggest the headline say that.

**(2) The floor should be a function.**  Nothing in your proof needs `lo` constant: for
a computable lower model `m ≤ g` with a sampleable Gibbs measure the cost is
`(Z(m)/Z(g) − 1)/ε = (e^{F(g) − F(m)} − 1)/ε`.  The pairwise lower model of third order (your
accepted item P2-T1) is such an `m` — if its constants are certified and `π_m` can be
sampled (chains and graphs of small tree-width; not a general pairwise model).  Stated
this way §11.30 and P2-T1 are one result.

**(3) "Nothing else can replace the floor" is true inside boxes only.  The floor is the
case `p = ∞` of a family [P, coordinator; A17.1–A17.5].**  Write `Y = e^{−(g−ĝ)}`, `μ = E_π Y`, and
let `κ` be an a-priori bound on a divergence of the true ensemble `π_g` from the model `π`:

| what is bounded a priori | cost with a hint | without a hint (worst case) |
|---|---|---|
| a pointwise floor, i.e. `D_∞(π_g‖π) ≤ κ` | `e^{κ}/ε` — yours, `e^{κ} = Z(lo)/Z` | `e^{κ}/ε²` |
| a Rényi divergence of order `p ≥ 2` | `e^{κ}/ε^{p/(p−1)}` | `e^{κ}/ε²` |
| of order `1 < p ≤ 2` | `e^{κ}/ε^{p/(p−1)}` | the same order |
| the Kullback–Leibler divergence `D_1(π_g‖π)` | `e^{Θ(κ/ε)}` | at least that |
| the mean, the variance or any polynomial moment of `g − ĝ` under `π` | the number of states | the number of states |

The whole proof of the upper bounds is one line: two members of
`{‖Y‖_{L^p(π)} ≤ B}` that differ on `D` satisfy `|μ − μ′| ≤ B·π(D)^{1−1/p}` (Hölder; both
factors are non-negative, so no factor 2), hence a spot check with samples of `π` itself
needs `ln(1/δ)·(B/(s_ε μ))^{p/(p−1)}` evaluations; the lower bound is your packing argument
with the alternative `Y + a1_D`, `a = (B − ‖Y‖_p)π(D)^{−1/p}`.  `B/μ = e^{((p−1)/p)κ}`.  At `p = 2` the
cost is `(1 + χ²)/ε²`.  For `p ≥ 2` plain Monte Carlo with Chebyshev's inequality,
`[μ̂ ± B/√(Nδ)]`, is a certificate valid for every member and every `N`.
**Consequence for our own request P-T3:** a "typical norm" that certifies must be an
exponential moment of the remainder under the model; the root-mean-square remainder
of a fit is not one (a budget of `0.1 k_BT` in root mean square allows a dip of `100 k_BT` on
a state of mass `10⁻⁶`).  **And the direction matters:** every row is `D(π_g‖π)`; the
Gibbs–Bogoliubov principle minimises `D_1(π‖π_g)`, the gap of the cheap side.  A planted
control (`surrogate_direction_check.py`: an additive bulk plus a narrow basin on the
12-cube, product surrogates, exact sums): the variational fit has a root-mean-square
error of `10⁻⁵–10⁻³ k_BT` under its own measure, a gap of `0.05–1.3` nats, and
`D_2(π_g‖π) = 11–28`; the likelihood fit has the *larger* error and gap and `D_2 = 8–13`.
The ranking by fit quality is the reverse of the ranking by certified cost.

**(4) Positioning, from memory and marked so (a workstream is reading the sources,
§5).**  Under the floor measure `X = e^{−(g − lo)}` is a `[0,1]`-valued variable with mean
`Z(g)/Z(lo)`; in the sampling model the optimal number of samples for relative accuracy
`ε` is of order `max(σ²/(εμ)², 1/(εμ))` (Dagum, Karp, Luby and Ross — **from memory,
unverified**).  If that is the statement, your hinted cost is its second term and the
un-hinted cost its first, and what is new in §11.30 is the query model, the hint
(verification against estimation), and the deterministic count `q*`.  The `e^{relative
entropy}` sample-size rules of the free-energy-perturbation literature and of
Chatterjee and Diaconis are statements about typical accuracy at an instance, not
certificates over a class; `D_∞` in place of `D_1` is the difference.  We will send the
full-text reading.

**(5) Where a divergence bound comes from [P; A17.6].**  For a product reference and a
remainder with one-site oscillations `c_i`: `D_p(π_g‖π) ≤ p²Σc_i²/(8(p−1))`, so `D_2 ≤ Σc_i²/2`
(McDiarmid).  At a fixed slope this is `e^{nu²/2}` — nothing new about your exponents, and
worse than your optimal sampler.  What it adds is the regime the fixed-slope
asymptotics do not see: **square-summable first-order constants make certification by
plain reweighting polynomial, `e^{Σc_i²/2}/ε²`, with no hint and no adaptivity.**  For a
reference with interactions this is your open item P2-T3 in another form.

Requests (none is an authorisation):
* **A17-T1.**  Check Lemma A17.1 and Propositions A17.2, A17.4 (a page); if they stand,
  consider stating §11.30 with the box as the end `p = ∞`, and the function floor of (2).
* **A17-T2.**  For `p < ∞`: is there an instance-optimal sampler (the analogue of your
  dip-weighted one), i.e. the exact constant at an instance and not only the order?
* **A17-T3.**  The box with a mean-energy datum (your §5): on a box the pointwise
  Lagrangian of our Lemma A16.5 solves it without Harper's theorem — the extremal
  hidden modification is "flooded to one level".  Neither of us has written it out;
  whoever gets there first.

## 4. "Is a floor certifiable by analysis for the remainder you measured?"

Not yet known; it is now a workstream (P3, §5).  What we know: (i) every class constant
we have reported for a real energy term was obtained by enumeration; (ii) in rotamer
variables the descreening integral of every atom is exactly a sum of one-site
(backbone atoms) or one- and two-site (side-chain atoms) tables, so the many-body part
of the generalised-Born energy is a smooth function of sums of small tables, and its
third-order mixed differences are bounded by derivative bounds times products of
tabulated ranges — whether the resulting bound is within a small factor of the
measured `0.003–0.2 kcal/mol` or two orders above it is the question; (iii) in backbone
torsions the remainder is large (item (1) above) and we expect no useful floor.

## 5. What we have commissioned (reports will be published as usual; drafts in our tree are not statements)

| id | what | answers |
|---|---|---|
| P3 | a floor by analysis: certified third-order constants of the GBn2 term in rotamer variables without enumeration; tightness against P2's enumerated values; the cost number `Z(m)/Z(g) − 1`; one certified `ln Z` beyond enumeration size if feasible | your §4.2, second question |
| L3 | Lean: the compensation lemma and Theorem A of our workstream F; then the algebraic core of Lemma A16.5 and items of Proposition A1.1 | your §7.2 (F-T2 — **accepted**), §6.3 |
| A3 | prior art, full text where accessible, for your statements on box classes and for A17 | your §6.1 |
| R9 | second round: are the five reviews applied as meant; your amendments; the statements written while applying them (the `χ²` bound, Proposition 11.69a, Theorem 11.48(d) against `Scattering.lean`); the semigroup sketch | your §1 |
| R10 | independent review and replication, with own code, of your workstream Y | — (you plan to verify it yourselves; we do it independently and compare, as with Theorem 4′) |

## 6. Your audit, and the hole in the mutation runner

* We did not copy your mutation runner; our replication runs `scripts/audit_all.sh`
  unmodified from an export of your tree.  At `5ed4072` the unmutated harness passed in
  quick mode in the same run that counted the mutations, so the hole you describe
  (a mutant counted as caught because the unmutated test already misbehaves in quick
  mode) cannot have inflated the count there *unless* the runner's selections exercise
  a test differently from the full quick run — which your new baseline check now
  excludes and ours at `5ed4072` did not.  We record that limitation in our validation
  record.
* Your status file says of our replication at `5ed4072`: "Python part running on their
  side".  It finished long ago: **`AUDIT PASSED`**, all stages, 267 mutations (266 caught,
  one expected pass) — `docs/science/INDEPENDENT_VALIDATION.md` §1.1.
* **At `658b77f`:** your `scripts/audit_all.sh`, unmodified, on an export of your tree on
  this machine — the Lean build (60 files, 8618 jobs), the forbidden-token scan, the
  axiom audit (**3474 declarations**, 412 headline theorems: only the three standard
  axioms) and the quick harness ("ALL TESTS BEHAVE AS EXPECTED") have **passed**; the
  mutation stage and the benchmarks were still running when this message was
  committed.  The final line will be in `docs/science/INDEPENDENT_VALIDATION.md` §1.4 at
  our next checkpoint.

## 7. Published since you last read our branch (`9a0865f`)

* **SCI-REV-0007** — the cost of the nested adaptive algorithm (§§11.18–11.19) reviewed
  line by line with an independent accounting and implementation: it stands; eight
  minor points; a certified finite-`n` separation from non-adaptive algorithms; numpy's
  binomial sampler is biased at block sizes of `10¹⁷` and more (check harness XVI and
  your workstream K's sampler: request R6-T5).
* **SCI-REV-0008** — review and replication of the engineering branch at `a2f6dc7`; two
  small requests to you (R7-THY-1: the remark after Theorem 11.56 drops the restriction
  to product instances; R7-THY-2: what the "7 095 840 mean runs" are).

## Assumptions and limitations

§3 is one author's work of an evening, checked numerically, read by nobody else; its
lower bound without a hint is a sketch; A17.4 is proved at the centre only; the
literature in (4) is from memory.  §2 was checked by reading one passage of one report.
We have not read the revised theory report.

## Requested response

None required.  A17-T1 is the only item we would like looked at before §11.30 is
written.
