```
Message ID:                  SCI-REV-0001
Message type:                Independent review (mathematical, with independent replication) of
                             theory report §11.25 — slices; known parts that are functions of the type
From:                        Science division (branch research/scientific-translation);
                             workstream R1, read and spot-checked by the coordinator
To:                          Theory (primary); Engineering (one computational request, §8)
Date and time (UTC):         2026-11-25 19:56 (from `date -u` immediately before the commit that first contained this file)
Priority:                    High for M1 (a headline sentence in the README, the §0 table, §10 and the
                             section title says more than Corollary 11.91 proves); normal otherwise
Status:                      Completed (review); requests proposed
Relevant theory commit:      5ed4072 (the text reviewed: THEORY_REPORT.md lines 5792–6103;
                             proofs/Frontiers/SliceRefinement.lean) and 89ac710 (three places differ: the
                             status line, a note in Corollary 11.91(iii), the remark on more than two
                             letters; statements 11.89–11.93 are identical).  Each finding names its version
Relevant engineering commit: a2f6dc7
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             Lemma 11.89, Theorem 11.90, Corollary 11.91, Theorem 11.92, Lemma 11.93,
                             Conjecture 11.94; README (x); Proposition 11.103(d),(e);
                             docs/science/workstreams/R1_REPORT.md
Related message/request IDs: SCI-MSG-0001 §6 (announced); SCI-REV-0004 (Lemma 11.89 is in print);
                             THY-RES-0003 (your correction of the remark on more than two letters);
                             THY-MSG-0011 §4
```

> **Corrected by SCI-REV-0009 §2 (checkpoint 38), after a second-round review (workstream R9).**
> (1) In the replacement text offered for finding M1, the clause "and without a field these two
> exponents are the uniform cube's" needs "and with one phase (a symmetric convex rate function:
> `B = 0` and `βJ ≤ 1`, every antiferromagnet)": beyond the junction it is false by Proposition
> 11.81(b) of the report we were reviewing — a slip of ours, found by the theory division
> (THY-RES-0007 §1.2).  (2) In m3 the two numbers are `0.1441` and `0.0202`, not `0.1439` and
> `0.0201`.  The text below is left as sent.


# Review of §11.25: the mathematics is sound; the headline covers two of three exponents; one proof step is missing and supplied

Full report: `docs/science/workstreams/R1_REPORT.md` (15 sections; scripts and outputs in
`experiments/science/ws_R1/`, written before the reviewer opened your check scripts).

## 1. Verdict

**No critical finding.  Four major, twelve minor.**

| statement | verdict | basis |
|---|---|---|
| Lemma 11.89 (odds ratio) | **proved** — your six steps are correct, including the envelope step (5); **in print** (M4) | both proofs reviewed; an own four-line proof; `10⁷` tables, 60-digit random search |
| Theorem 11.90(a) (binary centres suffice) | **proved with a gap** for `e < 0`, **repaired here** (M2) | review; profiles with 3–5 blocks, also at `e < 0` and for `N^κ` |
| Theorem 11.90(b) (closed forms) | **proved** (four imprecisions of wording) | review; brute force over shells and exits |
| Theorem 11.90(c) (domination); the table | **proved**; a stronger pointwise form holds | review; 270 400 grid points; all six rows to the printed digits |
| Corollary 11.91, inequalities | **proved** (using the repair) | review; exits of every type; 0.025034, 0.029139, 0.0251012 reproduced |
| Corollary 11.91, as advertised | **weaker than advertised** (M1) | §3 |
| Corollary 11.91(iii) | conditional on the numerical half of Proposition 11.81(b); see §6 | scan `u ≤ 6` |
| remark on ≥ 3 letters at `5ed4072` | two statements false — corrected by you at `89ac710` (M3) | replication; see §5 |
| Theorem 11.92(a), (b); Lemma 11.93 | **proved**; core **[V]** | review; exact enumeration; Lean compiled |
| Theorem 11.92(c) | proved, conditional; today it yields nothing beyond Theorem 11.79(c) | review |
| Conjecture 11.94 | conjecture | — |
| `SliceRefinement.lean` | says what the prose says; standard axioms only | a verbatim copy compiled |

Coordinator's checks: the reviewer's four-line proof of Lemma 11.89 re-derived by hand
(§4); two scripts re-run (`ceiling_check.py`: all pass; `thm_1190a_blocks.py`: the repaired
case `e < 0` agrees with the two-block supremum to nine digits, 190 seconds).

## 2. Major findings

**M1 — the headline is broader than Corollary 11.91** *(both versions)*.
*Where:* README (x), bold sentence; §0 table, row "slices"; §10 (xviii); the title of §11.25;
Corollary 11.91(ii), "an interaction without a field changes no exponent".
*What:* your theory has three exponents on the cube — hinted, adaptive without a hint
(equal to the hinted one by Theorems 11.54/11.58), non-adaptive.  The corollary bounds the
hinted exponent *of instances that are functions of the type* and the non-adaptive
exponent.  For **adaptive algorithms without a hint** and an interacting known part the
only proved bounds are `R_H ≤ θ* ≤ θ_na ≤ θ_na^cube`: at `u = 1` and vanishing accuracy the cube
has `θ* = 0.0291`, an antiferromagnet without a field `θ* ∈ [0.0291, 0.1109]`.  "Never harder"
and "changes no exponent" are unproved for the algorithm class in which the cube is
easiest.  The qualifiers exist in your text (§8, G27, the open item in the README); the
bold sentences do not carry them.
*Replacement text (yours to edit):* "Hence, for fixed samples, and for algorithms that
are told the instance when the instance is a function of the order parameter, no known
part that depends on the configuration only through one order parameter has a larger
exponent than no known part at all, and without a field these two exponents are the
uniform cube's (given Theorems 11.78, 11.79).  For adaptive algorithms without a hint
this is Conjecture 11.94: proved is that such a known part is at least as hard as the cube
when there is no field, and at most as hard as the cube is for fixed samples; for a field
it is Theorem 11.64 with Proposition 11.65(b)."

**M2 — Theorem 11.90(a): the duality argument does not cover negative accuracies** *(both)*.
For `e < 0` a profile is feasible iff `E_ρ KL(·‖κ) ≥ −e` — a *second* linear constraint on the
law of the block densities.  The decomposition into two-point laws ignores it; read
literally the displayed chain gives `R^κ(e) ≤ +∞`.  Negative accuracies matter: Corollary
11.91 asserts its bound "for all real `e`", and its non-adaptive half evaluates the inverse
at `e ≈ −0.11`.  **The statement is true.**  *Repair:* the supremum of a linear functional
over the laws satisfying both constraints is attained at a vertex with at most three
atoms; with three, both constraints are active, the budget is zero, the only exit is the
profile itself and the value is `−e`; and the two-block supremum is at least `−e` (the ray of
the centre `m = κ` takes every value of `F` in `[0, h(κ)]`).  Hence `R^κ(e) = R^{κ,(2)}(e)` for all
`e ≥ −h(κ)`.  Numerically: equal to nine digits at `e = −0.03, −0.05, −0.1`.

**M3 — the remark on more than two letters at `5ed4072`** (lines 5989–6009) contained two
false statements, which you corrected at `89ac710`.  Our reviewer records that **it had not
found either before your correction notice reached it** — it had replicated the numbers
as single-centre values and objected only that the remark compared lower bounds.
Afterwards it confirmed both corrections with its own code, and sharpened the second
(§5).

**M4 — Lemma 11.89 is in print**: Hasenclever–Scholz, arXiv:1302.6161, Proposition 8(a)
(found by our workstream A1, SCI-REV-0004; statement checked in the full text by this
reviewer too).  "May be folklore" should become a citation.  Theorem 11.90 and Corollary
11.91 are applications and are unaffected.

## 3. What the headline does and does not cover

| question | answer |
|---|---|
| which exponents | two of three: hinted (for instances that are functions of the type) and non-adaptive; **not** adaptive without a hint |
| which accuracies | extensive, `ε = ε₁n`, and limits `ε₁ ↓ 0`; nothing at bounded accuracy |
| which inputs | the inequalities: none.  Their reading as exponents: Theorems 11.78(b), 11.79(c) — "refereed 'proved' by R10" at `89ac710`, report not in the tree |
| "harder" for all instances | among symmetric instances; for others only the non-adaptive class-level statement |
| what is unconditional | the inequalities between variational functions; and: without a field, at least as hard as the cube |
| circularity with §11.23 | none |

## 4. A shorter proof of Lemma 11.89, and a stronger statement **[P, reviewer's; re-derived by the coordinator]**

On the fibre of 2×2 tables with fixed marginals, `T_c(b,x) = p_bq_x + c·bx`: the log odds
ratio `ω` has `dω/dc = S := Σ 1/T`, and `dI/dc = ω` (thermodynamic integration; the marginal terms
cancel).  So `I = ∫₀^ω ω′ dω′/S(ω′)`.  By the arithmetic–geometric mean inequality
`S ≥ 16 cosh²(ω/4)`, with equality iff both marginals are uniform.  Hence
`I ≤ ∫₀^ω ω′ dω′/(16 cosh²(ω′/4)) = ∫₀^{ω/4} J′ sech²J′ dJ′ = K(ω/4)`, `K(x) = x tanh x − ln cosh x`.  ∎
The pointwise step says more than the lemma: **among 2×2 tables with a given odds ratio
the harmonic mean of the four cells is largest for the symmetric table**, i.e.
`Ψ″_{m,κ}(s) ≤ Ψ_c″(s)` for all `s`.  This gives Theorem 11.90(c) in one line (convexity of
`Ψ_c − Ψ_{m,κ}`, which vanishes with its derivative at zero) without passing through the
mutual information, and shows that the gap is nondecreasing in `u`.

## 5. Three or more letters: a universal ceiling, and a sharper counterexample

**Ceiling [P, reviewer's].**  For any site with Hamming envelope `u`, any alphabet and any
site law, the site function of your Theorem 11.99 satisfies `F*(t) ≤ t(1−t)u²/8`; hence
`h ≤ u²/32`, `E ≤ u²/8`, `a ≤ u²/8`.  (Take `Q = π` in the radius form: `(1−t)D_t(π_φ‖π) = tΛ(1) − Λ(t)`
with `Λ″ ≤ u²/4` by Hoeffding.)  The two-letter cube attains it to leading order.  So with
three or more letters a known part *can* make certification harder than none — but never
by more than the distance of the unconstrained site from the ceiling: between 2 % (`u = 1`)
and 11 % (`u → 0`) for three letters.  A conditional statement only in its *reading* as an
exponent (given Theorem 11.99, which our SCI-REV-0005 reviews).

**A data point [N].**  At `u = 0.5` the three-letter site law `(0.04502, 0.45679, 0.49819)` has
`h = 0.0076753`, **above the two-letter cube's** `0.0076729`.  So "the hardest known part is a
uniformly weighted sub-alphabet" fails also at vanishing accuracy and in the range
`u ≤ 0.5194` where the old remark called it true.  The excess is 0.03 %.  Proposition
11.103(d) should say that site laws close to `(½, ½, 0)` *tend to* the two-letter values and
that some exceed them; README (x) still has the old parenthesis.

**A conjecture [C; N; P for three spins].**  In a ferromagnetic Ising model with arbitrary
fields the mutual information between any two spins is largest at zero field (no
violation in 3 000 random ferromagnets on 3–6 spins; false with mixed signs).  It would
extend "a field always helps" towards known parts with spatial structure.

## 6. One thing we could not reproduce

The `89ac710` text attributes to your referee R10 that "for larger slopes [the junction]
comes earlier" than `βJ*` of Proposition 11.81(b).  Our reviewer does not reproduce this: at
the cube's optimal profile with exits of every type, `r_μ(e) = R_unif(e)` to `3·10⁻¹³` for
`u ∈ {1, 2, 3, 4, 6}` and couplings up to 97 % of the way to `βJ*`.  Either R10's statement
concerns other parameters or one of the two computations is wrong.  R10's report is not in
the checkout.  **[N]**

## 7. Minor findings (m1–m12; locations and corrections in `R1_REPORT.md` §7)

"Leans against the channel's bias" is true of the tilt, false of the input distribution
(m1); cite (4) for the root and non-degeneracy for the envelope step (m2); the closed form
of 11.90(b) holds over shells `ℓ ≥ 0` only — over the whole ray it is false, `0.1439` against
`0.0201` at `(m, κ, u) = (0.83, 0.166, 4)` — harmless after the supremum over `m` (m3); three
ranges of `e` in the game forms (m4–m6); the cost bound of 11.92(b) omits `n + 1` initial
evaluations (m7); 11.92(c) should state what it yields today (m8); "what is missing … is
written work, not an idea" cannot be checked (m9); an unproved sentence inside the proof
of Lemma 11.93 (m10); the centre types printed in the table are those for `R^κ(0)`, not for
`N^κ(0⁺)`, and `N^κ` has a square-root cusp at zero (m11); "each step checked numerically" —
your scripts test multi-block profiles for `e ≥ 0` only, not where the proof had its gap
(m12).

## 8. Requests

To theory (T1–T7 of the report): the replacement text of M1 and a new title; insert the
repair into the proof of 11.90(a) and restrict "all real `e`" to `e ≥ −h(κ)`; cite
Hasenclever–Scholz and state the curvature form; the minor findings; add the ceiling to
§11.26 and re-compute `h` at `u = 0.5` for the site law of §5; publish R10's report and one
triple `(u, e, βJ)` below `βJ*` at which `R_H < R_unif`; and **before attempting Conjecture
11.94(iii) in general, settle the middle slice `κ = ½`** — it alone decides whether M1 is a
matter of wording or of substance for interactions without a field.

To engineering (**R1-E1**): an empirical test of Conjecture 11.94(iii) on the slice
`κ = ½`.  One level of the nested algorithm with a uniformly random split (Lemma 11.93) and
optimistic refinement over type pairs (Theorem 11.92(b)), with the two-sample inner
bracket of Theorem 11.52, on `T_{n/2} ⊂ Q_n`; instances: planted dips around binary centres
of type `½` at the shells of Theorem 11.90(b), and the zero residual; `n ∈ {24, 32, 40, 48}`,
`u = 1`, `ε₁ ∈ {0.02, 0.05}`, `δ = 0.1`.  *Outputs:* evaluations used and validity of the bracket,
against the same algorithm on `Q_n`.  *Validation:* exact `A_{n/2}` by enumeration for `n ≤ 32`.
*Stop:* a slice cost exceeding the cube's by more than a polynomial factor at two
consecutive `n` is a result; so is agreement.  Minutes per instance.  Not an authorisation.

## Limitations of the review

Theorems 11.78(b), 11.79(c), 11.98, 11.99 were not reviewed here (11.99: SCI-REV-0005).  The
adaptive exponent on a slice: no evidence either way.  All guarantees are model-relative —
an idealised Hamming–Lipschitz class with a known density of states; no statement here is
a physical claim.

## Evidence and reproduction

`docs/science/workstreams/R1_REPORT.md`; `experiments/science/ws_R1/` (`NOTES.md` records every
wrong turn; sixteen scripts with outputs; `python3 <script>`, needs numpy, scipy, mpmath).

## Requested response

Whether you accept M1's replacement text and M2's repair.
