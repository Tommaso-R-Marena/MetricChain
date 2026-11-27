# ER4 — internal adversarial review of `ENSEMBLE_REPORT.md`: the torus of three angles (E20a–E20d) and Part VII (E23–E26)

**Kind of review.**  Internal review by an independent AI session acting as an adversarial
referee.  **It is not external or academic peer review**, and it was **wound down before full
coverage** (instruction of the coordinator, 2026-11-27, for the controlled consolidation of
the programme): §7 lists what was not reviewed or not finished.  Nothing is to be taken as
reviewed by silence.

**Date.**  2026-11-26/27.

**Object.**  Commit `b654396`, `docs/ensemble/ENSEMBLE_REPORT.md`; all line numbers are those
of `git show b654396:docs/ensemble/ENSEMBLE_REPORT.md`.
Priority 1: §4c.4, lines 2122–2325 — Proposition E20a, the paragraph "Real coordinates",
Theorem E20b, Proposition E20c with the paragraphs "Where the special six-tuples are" and
"What survives the displacement", Proposition E20d with its table, the paragraph "*Checks*";
the stored output `experiments/ensemble/output.txt` (block of `torus_six_states.py`, lines
149–202); the script `experiments/ensemble/torus_six_states.py` (read, not run).
Priority 2: §4d, lines 2613–2826 — Propositions E23, E24, Theorems E25, E26, the example, the
paragraph "Numerical checks"; `experiments/ensemble/nonlinear_data_checks.py` (read, not run);
the Lean statement `Ensemble.eq_of_homogeneous_certificate`
(`proofs/Ensemble/Exposedness.lean`) and its witness (`proofs/AxiomAudit.lean`).
Summary documents at the same commit: `THEOREM_REGISTER.md` rows E20a–E20d, E23–E26;
`SOFTWARE_INTERFACE.md` cards T1, N1–N3; `ENSEMBLE-MSG-0008`, `ENSEMBLE-MSG-0009`;
`PRIOR_ART.md` §1, §5b′, §5c, §6.
Priority 3 (E15U beyond its main statement, E17.1, E22, two constants of E20″) was **not
reached**, except for a hand re-derivation of E15U (§7).
The author kept working during the review: at its end the working tree had uncommitted
changes by the author (among them `ENSEMBLE_REPORT.md`, the summary documents, two files
of `proofs/` — not `Exposedness.lean` — and scripts).  This review did not read them, wrote
only inside `docs/ensemble/reviews/`, and committed nothing.

**Method.**  Every proof of Priority 1 and 2 re-derived by hand.  Own programs written from
the definitions (`reviews/ER4_scripts/`; nothing imported or copied from
`experiments/ensemble/`): exact rational arithmetic for E20a, E20b, E20d, E23(b) (own
Gaussian elimination over `fractions.Fraction`, own elimination method for E20a); for E20c a
description of the real curve that needs no continuation (double cover over one angle), own
search for special six-tuples, own linear programmes, a global search for negative values of
the certificate (grid `96³`, about 7 000 local minimisations per instance, among them starts
displaced off the curve all along it).  Lean: a scratch file outside the repository,
type-checked (`lake env lean`, exit 0).  Literature: three sources opened (§5), with the
level at which each was read; **no web search was run** (wind-down).

---

## 0. Bottom line

* **No CRITICAL finding.**  No numbered statement of E20a–E20d, E23–E26 was found false.
  The two exact computations that carry E20a and E20b (S1, S2) were reproduced by an
  independent method, the special six-tuple of S4 was reproduced to all printed digits,
  and the certificate of E20c(a) survived every attempt to find a negative value.
* **Five MAJOR findings** (a false clause in a proof, or a sentence that says more than is
  proved or established):
  F1 — the proof that `dim I_0 = 15` (E20b) asserts that "no combination of `g_1`, `g_2` is
  independent of an angle"; this is false for an explicit rational six-tuple that
  satisfies every hypothesis.  Only coprimality is needed, and it does follow: theorem and
  dimension stand.
  F2 — "13 depends on the configuration" (table of E20d(c), line 2321, card T1,
  ENSEMBLE-MSG-0009): the evidence is "a twin in 2 of 4 instances, undecided in the other
  2"; no thirteen-tuple in general position is known to be determined.
  F3 — "all its twins are concentrated within `O(√ε)` of its own states": true only as a
  bound on a second moment, false for supports (the register says "are within"), and not
  sharp — the same certificate gives `O(ε)` in root mean square by one line; confirmed
  numerically (`∫ min d² dν ≈ C ε²`).
  F4 — check Q2: the number "1.000 of the bound `r_min τ/γ`" is the value of an outer
  relaxation, described in the text as a maximum over the true constraint set and as
  showing attainment.
  F5 — E26(c): "a claimed answer with its signs is checked in polynomial time" holds for the
  answer "consistent" only; deciding "determined" is coNP-hard (reduction given, by hand).
* **Seven MINOR findings** (F6–F12): summary sentences on E20c that drop its condition;
  the explanation paragraph can be sharpened (exactly one of three special positions on a
  two-component curve is of case (a)) and omits degenerate rank-11 strata; two wording
  gaps in the proof of E20c(a); two quoted numbers of the "*Checks*" (one not printed by
  the stored output, one sampling-dependent); prior art for the mechanism of E20b and for
  certificates that are not sums of squares, in a paper the report already cites; wording
  of E23; hypotheses dropped from summary sentences on E25.
* **Not finished** (§7): my numerical checks of E25 and E26 (stopped), E15U (script written,
  never run), E17.1, E22, the constants of E20″, the checks S3 and S6, any re-run of the
  author's scripts, the web search.

Status of each item at the wind-down:

| item | status |
|---|---|
| E20a: exact computation S1 and the semicontinuity argument | **confirmed correct** (independent exact method) |
| E20b: exact ranks S2; parts (a), (b), (c) | **confirmed correct** |
| E20b: clause "no combination … independent of an angle" in the proof of `dim I_0 = 15` | **confirmed defect** of the proof text (explicit exact instance); theorem unaffected (F1) |
| degenerate six-tuples with rank 11 (two states sharing two angles; three sharing one) | **confirmed fact** (exact); whether they satisfy "`Z` a smooth curve" **undecided** (F7) |
| E20c(a), (b): proofs | **confirmed correct**, two wording repairs (F8) |
| E20c: existence, S4, S4b | **reproduced** numerically with own code (floating point) |
| "with one real component case (a) holds" | **confirmed** numerically, 67 of 67 |
| displacement paragraph, `O(√ε)` | **confirmed defect** of wording and of order: second moment, `O(ε)` (F3) |
| E20d(a), (b); the citation of Laface–Postinghel; 17, 41, 105 | **confirmed correct** |
| E20d(c): "13 depends on the configuration" | **confirmed overstatement** (F2) |
| "*Checks*" against the stored output | all numbers found except "three states each" (true, not printed) (F9) |
| E23(b) and its tolerance version | **confirmed correct** (exact test; 1 908 instances) |
| Lean sentence on `eq_of_homogeneous_certificate` | **confirmed accurate** (type-checked) |
| E24, E25, E26(a), (b): proofs | re-derived by hand, no error found; **own numerics not finished** |
| E26(c), last sentence | **confirmed overstatement** (proof by hand of coNP-hardness; not replicated numerically) (F5) |
| Q2, mass bound "1.000 … attained" | **confirmed mis-description** by reading the script; true maxima **not computed** (F4) |
| E15U beyond (C) | hand re-derivation only; closed forms and instances **not recomputed** |
| E17.1, E22, constants of E20″, S3, S6 | **not reviewed** |

---

## 1. Verdict per statement

"Correct" means: the proof was re-derived and no error found, and — where a program is
named — the statement survived it.  It is the verdict of one AI reviewer.

| statement | verdict | what was done; pointer |
|---|---|---|
| E20a, statement | **correct** | Proof steps (1)–(4) re-derived: the lemma on `K + 1` rank-one matrices; dominance of the span map `𝒱⁵ ⇢ G(5, 8)` (both of dimension 15) from one finite fibre; the antiholomorphic involution extends to `ℙ⁷` as `x ↦ J x̄` and fixes the secant plane; E18(ii) |
| E20a, "exact computation plus semicontinuity" | **correct** | Semicontinuity: the incidence `{rank ≤ 5}` is closed in `𝒱⁵ × 𝒱`, the projection is proper, so "fibre of positive dimension" is closed in the base; one tuple with a finite fibre (all of `(ℙ¹)³`, points at infinity included) suffices.  The instance: own elimination (a binary sextic `m_00 m_11 − m_01 m_10` in the third angle, homogeneous, so no chart is lost): six distinct rational roots, one point over each, the sixth zero equal to the stored one, six outer products of rank 6 (`out_e20a_exact.txt`).  120 rational five-tuples of my own: 109 finite, each with six distinct real rational zeros and rank 6; 11 infinite, all degenerate (two states sharing two angles, or three states sharing one angle — the exceptional set is not empty, as it should be) |
| "Real coordinates" (lines 2147–2156) | **correct** | `V` = numerators of degree ≤ 2 in each `t_k`; non-negativity passes to the numerator by density of the chart; the products `w_a w_b` span `V` (exact conversion used in my code) |
| E20b(a) | **correct**; one clause of the proof false | F1.  `I_0 ⊆ W`, `dim W = 15` from (R), `dim I_0 = 15` from coprimality: re-derived |
| E20b(b) | **correct** | The chain of E1(b): `f_j = ℓ_j ∘ Φ ∈ V`, `f_j ≥ 0` on `X_j ⊇ Z`, zero on `S` — so (a) applies at every step and `X_G ⊇ Z`; "only if" of E1(b) then gives a twin charging any point of `Z`.  Supports containing `S`: a face of a simplicial face is a face — re-derived.  Twins found by my own linear programme for 12 six-tuples in general position (displaced special ones, `out_e20c_displacement.txt`) and for 142 of the 144 special six-tuples of case (b) (`out_e20c_stats.txt`; the other two: see E20c(b)); S3 itself (random six-tuples) not replicated |
| E20b(c) | **correct** | Each hypothesis is the non-vanishing of a polynomial in homogeneous half-angle coordinates (the tangent `∇g_1 × ∇g_2` is polynomial in the Plücker coordinates of `Λ^⊥`); one instance suffices.  Exact ranks at the report's two six-tuples in two bases of `V` (numerators; trigonometric products) and in homogeneous coordinates: lifts 6, smooth at the states, rank 12, `dim I_0 = 15`, `I_0` in the kernel; the same for 30 six-tuples of my own and for six-tuples with states at `φ = π` (`out_e20b_exact.txt`) |
| E20b, the six points of attack | (i) chain: correct.  (ii) `dim I_0`: correct, justification F1.  (iii) proper algebraic subset: correct.  (iv) larger supports: correct.  (v) points at infinity: nothing lost (the proof is homogeneous; checked exactly with states at infinity).  (vi) the kernel of the twelve forms is `I_0`: correct, exact | — |
| E20c(a) | **correct**; two wording gaps in the proof | F8.  Compactness proof re-derived line by line (gradient of `q_0` normal; `i` with `∇(q_0 + i) = 0` at the states exists because the six lifts are independent; Hessian `2A·N + Hess h` with `N ≥ 0`, `ker N` the tangent; uniformity in `A`).  Numerically: the instance of S4 reproduced; four case-(a) six-tuples of my own (one and two real components; one with the states distributed 1 + 5): no negative value found.  "`A` large" is instance-dependent: the least `A` found was 30 for S4 and 1.3, 61, 202, 1 994 for mine (`out_e20c_own.txt`) |
| E20c(a), "not a sum of squares of lifted linear forms" | **correct** | Two lines; no certificate of `S` can be one |
| E20c(b) | **correct** | Re-derived.  My linear programme finds a twin in 142 of 144 case-(b) instances; in the other two the special sixth state nearly coincides with another state, and the programme, which leaves out the curve within 0.02 of the states, is not conclusive (one instance of this kind, re-examined with a finer sampling in an ad hoc run whose output was not stored, has a twin).  In case (a) the programme returns least mass `1.000000` in 137 of 139 instances and a solver failure in two (nearly coincident states again) |
| E20c(c), existence **[N]** | **reproduced** | Rank 11 to rounding (`7·10⁻¹⁶`), both cases, with my own code |
| "Where the special six-tuples are" | nothing false found; **can be sharpened**, two omissions | F7.  "With one real component case (a) holds": 67 of 67 instances |
| "What survives the displacement" | **true as a second-moment bound; not sharp; false if read for supports** | F3 |
| E20d(a) | **correct** | The first step of the chain gives a non-zero `f ∈ V` (the 3^r functions are independent, so `ℓ ≢ 0` on the moment body means `f ≢ 0`), also when the minimal face is not exposed |
| E20d(b) | **correct**; citation correct | Laface–Postinghel, Theorem 2.1 read in the PDF (§5): exceptions `(2, 2a)` with `2a + 1` points, `(1, 1, 2a)` with `2a + 1`, `(2, 2, 2)` with 7, `(1, 1, 1, 1)` with 3; so `(2, …, 2)` is non-special for `r ≥ 4` and exceptional exactly for three points (`r = 2`) and seven (`r = 3`).  Transfer to real torus points: a minor does not vanish identically and the torus is Zariski dense.  Own ranks (modulo three primes for `r ≤ 4`, one prime for `r = 5`; equal to the upper bounds, hence exact): 8 for `(2, 3)`, 26 for `(3, 7)`, 27 for `(3, 8)`, 80 and 81 for `(4, 16)`, `(4, 17)`, and 240, 243 for `(5, 40)`, `(5, 41)` (`out_e20d_ranks.txt`).  Arithmetic 17, 41, 105: right |
| E20d(c), table | **one entry says more than is established** | F2.  Rows `r = 2`, `r ≥ 5` and the entries 5, 6, 11, 17: consistent with the statements they cite (E22 itself not examined; "12 in 40 instances" is ER3's and was not recomputed; S6 not replicated) |
| "*Checks*" paragraph (lines 2294–2316) | every number is in the stored output **except one**; one is sampling-dependent | F9 |
| E23(a) | **correct**; the parenthesis is loose | F11 |
| E23(b) | **correct** | Proof re-derived (cone argument; Stiemke).  Exact test, 1 908 integer instances: agreement in all; `y ≠ 0` is needed and is stated (28 instances).  Tolerance version convex: 1 482 876 convex combinations, none outside (`out_part7_parts_A_B_only.txt`).  "One linear programme": F11 |
| E23(b), Lean sentence | **accurate** | The Lean statement has any real `t`, no `y ≠ 0`, and `μ` only required to vanish off `S`; the report says "any real multiple" and claims the "if" only.  Type-checked, with an instance of my own and the corollary that the hypotheses force `t = 1` when a datum of `μ` is non-zero (`out_lean.txt`) |
| E23(c) | **correct** (two programmes, one per end) | by hand |
| E24(a), (b), (c) | **correct** | by hand only (convergence in (c): uniform continuity of the two value functions on a polytope, every ball meeting the fibre) |
| E25(a), (b), (c), (e) | **correct** | by hand only.  (b) is stated for `d ≥ 2`, and needs it (for `d = 1` the conclusion fails); summaries drop the hypothesis: F12 |
| E25(d) | **correct**; attainment conditions sufficient as stated | by hand only (my numerical search for a counterexample was stopped: §7).  F12 |
| E26(a) | **correct**; "at most `2^m` linear programmes" is loose | F5 |
| E26(b) | **correct** | by hand only: both reductions, membership in NP with the stated encoding, the bound `2n` on the numbers (for `n ≥ 2`).  My brute-force replication was not run to the end |
| E26(c) | **last sentence says more than is proved** | F5 |
| "Numerical checks" of Part VII (lines 2799–2820) | every number is in the stored output; one is mis-described | F4 |
| E15U beyond (C), E17.1, E22, constants of E20″ | **not examined** | §7 |

---

## 2. Findings

### F1 (MAJOR) — E20b: a false clause in the proof that `dim I_0 = 15`

**Where.**  Lines 2181–2184: "… has the kernel `ℝ·(n_2, −n_1)` and no more, because `g_1` and
`g_2` have no common factor and no combination of them is independent of an angle — either
would give four independent multilinear forms vanishing on `S`, where `dim Λ^⊥ = 2`, or
parallel gradients at a state."

**What is wrong.**  The second assertion does not follow from the hypotheses and is false
under them.  If `a g_1 + b g_2 = c(φ_k)·H(φ_l, φ_m)` with `c` a form in one angle, the states on
`{c = 0}` need not lie on `{H = 0}`: there is one gradient, nothing is parallel, and no four
forms arise.  Exact instance (`out_e20b_exact.txt`, parts C and F): two states with
`φ_1 = π`, four states with `(t_2, t_3)` on `t_2 t_3 − 2t_2 + 3t_3 + 1 = 0`; the six lifts are
independent, `∇g_1 × ∇g_2 ≠ 0` at every state, (R) has rank 12 — and `x_1·H`, whose numerator
in the chart `t` does not depend on `t_1`, is a combination of `g_1`, `g_2`.  `dim I_0 = 15` all
the same.

**What is true and suffices.**  The kernel of `(ℓ_1, ℓ_2) ↦ (ℓ_1·w)g_1 + (ℓ_2·w)g_2` is
`{(c g_2, −c g_1)}` with `c` constant as soon as `g_1`, `g_2` are coprime as forms of
multidegree `(1, 1, 1)`; a factor "at infinity" in the chart `t` (both independent of the
same angle) is a common factor in this sense.  Coprimality follows from the two reasons
given: a common factor `c` of positive multidegree `d` vanishes at no state (else the
gradients are parallel there), so the cofactors `a_1`, `a_2` vanish at all six, and
`{a_1 e_1 + a_2 e_2}` with `e_i` of multidegree `d` has dimension `2·2^{|d|} ≥ 4`.

**Status.**  Confirmed defect of the proof text; theorem E20b and `dim I_0 = 15` unaffected.

**Replacement.**  "… and no more, because `g_1` and `g_2`, as forms of multidegree `(1, 1, 1)`
in the half-angle coordinates, have no common factor: a common factor `c` would vanish at
no state (the gradients would be parallel there), so both cofactors would vanish at all
six states, and their products with the forms of the multidegree of `c` would be at least
four independent multilinear forms vanishing on `S`, where `dim Λ^⊥ = 2`.  (In the chart `t`
this covers a factor at infinity: `g_1` and `g_2` are not both independent of the same
angle.  A single combination can be.)"

### F2 (MAJOR) — "13 depends on the configuration" is not established

**Where.**  Line 2281 (table of E20d(c)): "13 depends on the configuration **[N]**"; line
2321: "with thirteen the answer depends on the configuration (an explicit twin in 2 of 4
instances, undecided in the other 2)"; `SOFTWARE_INTERFACE.md` card T1, line 264: "for
thirteen it depends on the configuration"; ENSEMBLE-MSG-0009 §1: "13 depends on the
configuration".

**What is wrong.**  Dependence on the configuration needs one thirteen-tuple in general
position that is determined and one that is not.  The evidence is ER3 §7: a twin in 2 of 4
instances; in the other 2 "whether these two are identified with a very small gap or not
at all I could not decide".  The report itself says "may depend" at lines 2325 and 2590.

**Status.**  Confirmed by reading (no computation of mine on `𝕋⁴`).

**Replacement.**  Table: "13 to 16: open; 13: a twin in 2 of 4 computed instances, the
other 2 undecided **[N]**; 16: not determined in 12 of 12 instances **[N]** (S6)".  Line 2321:
"with thirteen: an explicit twin in 2 of 4 instances, undecided in the other 2".  Card T1
and the message: "for thirteen it is not known, and it may depend on the configuration".
*Suggestion, not checked:* the count of E20b decides this instance by instance — for
thirteen states the functions with thirteen double zeros on the curve form, modulo those
vanishing on it, a space of dimension at least 10 (36 − 26; the 36 is ER3's computed
dimension of the span on the curve), and the question is whether it contains a function
that is non-negative on the real curve.

### F3 (MAJOR) — "What survives the displacement": a second-moment bound, stated as concentration, with the wrong order

**Where.**  Lines 2255–2258: "… its data are within `O(ε)` of those of the special ensemble
with the same weights, so **all its twins are concentrated within `O(√ε)` of its own
states**"; `THEOREM_REGISTER.md`, row E20c: "all its twins are within `O(√ε)` of its states";
ENSEMBLE-MSG-0009 §1 ("What survives a perturbation").

**What is wrong.**  (i) What the argument bounds is `∫ min_k d(x, p_k)² dν`.  The support of a
twin is not near the states: by E20b the minimal face contains the whole curve, so some
twin charges any given point of it.  The register's "are within" is false as written.
(ii) The order is not sharp.  A twin `ν` of the displaced ensemble `μ_ε` has *exactly* the
data of `μ_ε`, and the certificate `f` of the special six-tuple is in the span, so
`∫ f dν = ∫ f dμ_ε = Σ_k w_k f(p_k^ε) ≤ ½ L ε²` (`f` and `∇f` vanish at the special states;
`L = max ‖Hess f‖`).  Hence `∫ min_k d(x, p_k)² dν ≤ L ε²/(2c_0)`: root-mean-square distance
`O(ε)`, not `O(√ε)`.  The report's route (data within `O(ε)`, then `‖λ‖_* τ`) loses a square
root because it forgets that `f` is flat to second order where the data moved.

**Evidence** (`out_e20c_displacement.txt`; linear programmes over all measures on the curve of
the displaced six-tuple, sampled with about `10⁴` points and refined near the states; three
directions of displacement of the sixth state of the special six-tuple of S4).  Largest
`∫ min_k d² dν` over twins:

| `ε` | direction 1 | direction 2 | direction 3 |
|---|---|---|---|
| `10⁻¹` | `4.7·10⁻⁴` | `1.8·10⁻⁴` | `1.5·10⁻³` |
| `3·10⁻²` | `4.3·10⁻⁵` | `1.1·10⁻⁵` | `1.5·10⁻⁴` |
| `10⁻²` | `4.8·10⁻⁶` | `1.0·10⁻⁶` | `1.7·10⁻⁵` |
| `3·10⁻³` | `4.0·10⁻⁷` | `6.4·10⁻⁸` | `1.5·10⁻⁶` |

that is about `0.05 ε²`, `0.007` to `0.018 ε²`, and `0.15` to `0.17 ε²`.  Largest mass farther than
0.5 from every state: `0.06` to `0.07 ε²`, `0.014` to `0.025 ε²`, `0.20` to `0.24 ε²` — positive; and a
twin can put mass (`0.5` to `4·10⁻⁵` at `ε = 0.1`) within 0.05 of the point of the curve farthest
from all states (distance 2.7).  In every row there is a twin with no mass on the six
states.  (Two earlier runs, whose outputs were overwritten and are **not stored**: with a
sampling that leaves out the curve within `10⁻³` of the states no twin was found for
`ε ≤ 10⁻²` in most directions — the twins carry most of their mass within `O(ε)` of a state;
and below `ε = 3·10⁻³` the masses, of order `ε²`, reach the tolerances of the linear
programme.)

**Status.**  Confirmed: true in mean square, false for supports, order `ε` (proof above;
numerics agree).

**Replacement.**  "… A twin `ν` of an ensemble `μ_ε` on a six-tuple within `ε` of a special one
has the data of `μ_ε`, so `∫ f dν = Σ_k w_k f(p_k^ε) ≤ ½ L ε²` and
`∫ min_k d(x, p_k)² dν ≤ L ε²/(2c_0)`: **all its twins are concentrated, in root mean square,
within `O(ε)` of the states.**  This bounds a second moment, not the support: a twin may
charge any point of the curve, with mass `O(ε²)`."  Register and message accordingly.
Also "is not determined (E20b)" holds for displaced six-tuples in general position, not
for those that stay on the hypersurface.

### F4 (MAJOR) — check Q2: the number for the mass bound is that of a relaxation

**Where.**  Lines 2805–2808: "over ensembles with `‖E_νΦ‖ ≤ r_min + τ`, `τ = 10⁻³, 10⁻²`, the
largest mass off the zero set is `1.000` of the bound `r_min τ/γ` and the largest
displacement of the mean is `1.000` of `√(2r_min τ + τ²)` (both bounds are attained)".

**What is wrong.**  In `nonlinear_data_checks.py` (function `test_Q2`) the mass is maximised
over an outer polyhedral approximation of the ball — the script's own comment: "a
relaxation, so its value is an upper bound of the true maximum" — and the maximiser is not
tested for `‖E_νΦ‖ ≤ r_min + τ` (the test "truly feasible" is applied to the mean
displacement only).  Because the direction `z*/r_min` is among the cuts, the relaxed value
cannot exceed the bound and equals it whenever that cut alone is binding.  So "1.000"
shows that the bound is not violated on a superset; it does not show attainment, and it
is not a maximum "over ensembles with `‖E_νΦ‖ ≤ r_min + τ`".  When the nearest point is a
vertex the bound is in general *not* attained (equality forces
`E_νΦ = (1 + τ/r_min) z*`, hence `Φ(x_1) − z* ∥ z*` for the configuration `x_1` of least gap),
although it is approached within a factor `1 − O(τ)`, which prints as `1.000`.

**Status.**  Confirmed by reading the script.  The true maxima were **not** computed by me
(my program for them was stopped at the wind-down), so whether the bound is attained in
the 40 clouds of Q2 is undecided here; the theorem proves attainment in the facet case.

**Replacement.**  Either change the text — "over an outer relaxation of the constraint the
largest mass off the zero set is `1.000` of the bound (the bound holds; its attainment is
part (d), not this check); the largest displacement of the mean among feasible optimisers
is `1.000` of `√(2r_min τ + τ²)`" — or change the check: test the maximiser for feasibility
and report the ratio separately for clouds whose nearest point is interior to a facet.

### F5 (MAJOR) — E26(c): only the answer "consistent" is checked from its signs

**Where.**  Lines 2776–2777: "The whole difficulty is the choice of the signs: a claimed
answer *with its signs* is checked in polynomial time."  Summary row E26 (line 64): "an
answer with its signs is checked in polynomial time"; ENSEMBLE-MSG-0008 §2, same words.
Also line 2767: "decided by at most `2^m` linear programmes".

**What is wrong.**  Part (a) names three questions: consistency, identification, the exact
range of a target.  A sign vector with a feasible ensemble certifies "consistent" (and a
lower bound on a supremum).  It certifies neither "inconsistent" nor "determined" nor an
exact range: those need all `2^m` sign vectors excluded.  Deciding "determined" is
coNP-hard.  *Reduction* (by hand): for positive integers `a_1, …, a_m` with sum `A` let
`X = {1, …, m} × {+, −} ∪ {o}`, `φ_i(j, ±) = ±A·[i = j]`, `φ_i(o) = a_i`, `ψ(j, ±) = ±A`, `ψ(o) = 0`, with
the data `(E φ_i)² = a_i²`, `(E ψ)² = 0`.  `δ_o` has the data.  If `ν` has them, with `θ = ν(o)`,
`d_i = A(ν(i, +) − ν(i, −))` and `E_ν φ_i = s_i a_i`: `d_i = (s_i − θ)a_i`, `Σ_i d_i = 0`, and
`1 − θ ≥ Σ_i |d_i|/A = (1 − θ) + 2θA_−/A` with `A_−` the sum of the `a_i` with `s_i = −1`.  So `θ = 0`,
and then `Σ_i s_i a_i = 0`; or `A_− = 0`, and then `Σ_i d_i = (1 − θ)A = 0` gives `ν = δ_o`.  Hence
`δ_o` is the only ensemble with the data iff the integers have no split into two parts of
equal sum.

**Status.**  Confirmed by proof (hand).  The numerical replication of the reduction is in
`er4_part7.py`, part D, which was **not run to the end**.

**Replacement.**  "The difficulty is the choice of the signs: consistency is in NP — a sign
vector with a feasible ensemble is checked in polynomial time.  The answers
'inconsistent', 'determined' and an exact range are not certified by a sign vector;
deciding whether a given ensemble is the only one with the data is coNP-hard (reduction
…)."  In (a): "by `2^m` linear problems (a bounded number of linear programmes for each
sign vector)".

### F6 (MINOR) — summary sentences on E20c drop its condition

**Where.**  `SOFTWARE_INTERFACE.md` card T1, lines 256–258: "six never (Theorem E20b) —
except on a hypersurface of special six-tuples, where they are (Proposition E20c)";
ENSEMBLE-MSG-0009, message type: "on a hypersurface of special six-tuples they are";
report line 59.  Card T1, line 263: "eleven states are always determined, seventeen never".

**What is wrong.**  "Special" (rank 11) is not "determined".  E20c proves determination
where `q_0` keeps one sign (case (a)); where it changes sign (case (b)) the six-tuple is
special and not determined — and that is the majority on curves with two real components:
of 283 special positions found for 139 random six-tuples, 139 are of case (a) and 144 of
case (b) (`out_e20c_stats.txt`).  The existence is numerical.  "Eleven … seventeen" needs
"in general position" twice.

**Replacement** (card).  "… six never — except where the twelve conditions drop rank *and*
the extra function keeps one sign on the curve (Proposition E20c(a); numerical
instances): part of a hypersurface.  A special six-tuple whose extra function changes
sign is not determined (E20c(b))."

### F7 (MINOR) — "Where the special six-tuples are": one sharpening, two omissions

**Where.**  Lines 2230–2249.

1. "its three translates by half-periods, which are the special six-tuples of E20c … with
   two [components], the signs on the two components may agree (a) or not (b)."
   Measured (`out_e20c_stats.txt`, 150 random six-tuples, 11 set aside as nearly singular):
   on a curve with **one** real component the determinant of the twelve conditions changes
   sign at two positions of the sixth state — the dependent one and **one** special
   position, of case (a) (66 instances; in one more the dependent position was not
   located); only one of the three translates is real.  On a curve with **two** real
   components there are four — the dependent one and three special positions — and
   **exactly one of the three is of case (a)**, in 72 of 72 instances; it lies on the
   component that does *not* carry the dependent position, together with one of case (b),
   and the third (case (b)) lies on the component of the dependent position.  This is
   what the elliptic-curve model predicts (for `y² = (x − e_1)(x − e_2)(x − e_3)` the function
   `x − e_i` has one sign on the real locus for exactly one `i`) and what the "positive
   two-torsion point" of Baldi–Blekherman–Sinn's Theorem B says (§5).
2. The states need not be three and three on a two-component curve: among the special
   six-tuples of my stored outputs (`out_e20c_author_S4b.txt`, `out_e20c_own.txt`) the
   distributions 3 + 3, 4 + 2, 5 + 1 and 6 + 0 all occur; in the last case `q_0` has one sign on
   a component that carries no state (case (b), a twin found).
3. The locus "rank 11, independent lifts, smooth at the states" also contains degenerate
   strata that the genus-one picture does not describe: two states sharing two angles, and
   three states sharing one angle (exact, one rational instance each:
   `out_e20b_exact.txt`, part E).  There `Z` contains a circle, respectively a conic,
   through those states, the extra function vanishes on it, and the six-tuple is not
   determined for another reason (E20′ with `|D| = 1`; the mechanism of E22).  Whether `Z` is
   then a smooth *real* curve — so that these fall under the standing hypothesis of E20c —
   was **not examined** (undecided).

**Status.**  Nothing in the paragraph was found false; items 1 and 2 are numerical, item 3
exact.

### F8 (MINOR) — E20c(a): two wording gaps in the compactness proof

**Where.**  Lines 2219–2224.
(i) "positive definite on the normal plane for large `A`, and along the tangent equal to …
which is positive.  So for `A ≥ A_1` the Hessian is positive definite": positivity on two
complementary subspaces does not give definiteness (cross terms).  The conclusion is
right by the standard lemma: `N = ∇g_1∇g_1ᵀ + ∇g_2∇g_2ᵀ ≥ 0`, `Hess h > 0` on `ker N` (the tangent)
⇒ `Hess h + 2A·N > 0` for large `A`.
(ii) "`f_{A_1} > 0` on a punctured neighbourhood `U_k` of `p_k` … On the compact set `Z ∖ ∪U_k` one
has `h = q_0 ≥ c > 0`": with punctured `U_k` that set contains the states, where `h = 0`.  Use
the full neighbourhoods `U_k ∪ {p_k}` there and for "the rest of the torus".

**Status.**  Confirmed wording defects; the proof is correct after the two repairs.

### F9 (MINOR) — "*Checks*": one number not in the stored output, one sampling-dependent

**Where.**  Lines 2309–2310: "on a curve with two real components carrying three states
each".  The stored output (`output.txt`, line 181) prints "real components of the curve: 2;
signs of the extra function on them: [-1, 1]" and no distribution of the states.  The
number is true: my recomputation of that instance gives 3 + 3 (`out_e20c_author_S4b.txt`,
position `/0`).  Lines 2304–2305: "minimum at distance > 0.1 from the states 0.0023": this
is the value at the first sample point beyond the cut-off and depends on the sampling
(mine: `0.0021`, which is `½·0.4268·0.1²`, the quadratic growth at the flattest state); it is
not a property of the configuration.  All other numbers of the paragraph are in the
stored output, and those of S1, S2, S4, S4b, S5 were reproduced by my own code (S4: sixth
state `(2.666708, 1.951347, 1.012184)`, singular values `0.7860` and `7.6·10⁻¹⁶`, one real
component, maximum `2.1750`, least mass `1.000000`, Hessian eigenvalue `0.4199`; grid `96³`:
minimum `1.07·10⁻³`; 7 153 local minimisations, all ending at a state).

**Replacement.**  Print the number of states per component in S4b; replace "0.0023" by the
second derivatives at the states (`0.43` to `2.16`), or say "at the first sample point".

### F10 (MINOR) — prior art for the mechanism of E20b/E20d and for the headline of E20c

**Where.**  `PRIOR_ART.md` §5b′; `THEOREM_REGISTER.md` rows E20b ("the proof is ours; not
searched"), E20c; ENSEMBLE-MSG-0009 §3 ("The method is not specific to tori: count
first-order conditions along the zero set of the lifted certificate …") and its question
E-T5 ("an identified ensemble on a continuous space whose certificate provably is not a
lifted sum of squares").

1. **di Dio–Schmüdgen (2018) — the paper already cited for E1(b) — Section 7** (read in the
   PDF, §5).  Definition 33: the moment map `S_k(C, X) = Σ c_j s(x_j)` and its total
   derivative, whose columns are `s(x_j)` and `c_j ∂s(x_j)` — so the functions annihilating its
   range are those that vanish with their first derivatives at the atoms (Lemma 37 is the
   version over all representing measures); Theorem 40, (vii) ⇒ (i) ⇒ (iii):
   if the derivative has full rank at a representing measure the moment sequence is an
   inner point of the moment cone, and then every point is an atom of a representing
   measure (so the functional is not determinate: Corollary 19).  The twelve forms of (R)
   are the columns of this derivative for six atoms on the curve `Z` with `E = V|_Z` (dimension
   12), and (R) says that it has full rank.  So E20b(a), (b) is this criterion on `Z`
   (their setting is `ℝⁿ`; a curve needs a local parameter), preceded by the reduction from
   the torus to `Z`; and E20d(a), (b) is the same criterion on the torus with rank `3^r`.
2. **The same paper, Proposition 22 and Examples 23, 24**: a set `B` with `B² ⊆ E` and linearly
   independent "lifted" vectors at the atoms gives determinacy (cf. E18), and the examples
   are determinate functionals whose non-negative certificate is the Robinson, resp. the
   Motzkin polynomial — not sums of squares.  An identified ensemble on a continuous space
   whose certificate is not a sum of squares is therefore in print (for polynomial data
   on the plane); what E20c adds is an instance on the torus with its structure.
3. **Baldi–Blekherman–Sinn, Sections 5–6** (seen only through summaries of a fetch tool —
   **to be checked in the source**): their Corollary 6.0.1 is summarised as "the boundary of
   the dual cone of the quadrics on an elliptic normal curve in `ℙⁿ` consists of the sums
   of at most `n` point evaluations, the sums of `n + 1` distinct points with total `O`, and
   the sums of `n + 1` distinct points with total the positive two-torsion point"; Lemma
   5.2.1 as "a form with divisor `2D`, non-negative on one component and changing sign on
   the real locus".  If so, E20b(a), (b) and E20c(a), (b) *on a given smooth curve* `Z` are
   their statements, the existence of case-(a) six-tuples follows without numerics (five
   real points and the sixth with the right total), and item 1 of F7 is their Theorem B.
   The report's sentence "whether their description … gives E20b(c) and the existence
   part of E20c directly, we have not checked" should become a check.

**Status.**  Items 1 and 2: confirmed in the source.  Item 3: not confirmed (summary level).
The classification "an application of a known mechanism to the torus" is fair; the
register's "the proof is ours" and the message's "the method" should name item 1.  The
citation of **Theorem 18** for E1(b) is correct in number and content (statement and proof
read; the introduction of the arXiv version calls it "Theorem 15", a slip of that paper).

### F11 (MINOR) — E23: wording

1. Line 2635: "(conditional populations `μ(A | B) = μ(A ∩ B)/μ(B)` are of this form)".  `ψ = 1_B`
   is not positive on `X`; the two linear constraints are satisfied by every ensemble with
   `μ(B) = 0`, for which the ratio does not exist.  Add "for ensembles with `μ(B) > 0`; the
   linear constraints also admit every ensemble with `μ(B) = 0`".
2. Lines 2643–2645: "the range of a target is one linear programme".  With `s = 1/c ≥ 0` the
   Charnes–Cooper programme returns the closure of the range, and it is feasible at `s = 0`
   (`E_νΦ = 0`) even when no ensemble is compatible (`φ ≡ 0`, `y = 1`, `τ = 0.1`).  Two-point example
   (`out_part7_parts_A_B_only.txt`): `φ = (1, −1)`, `y = 1`, `τ = 0.1` — the compatible ensembles
   are those with `ν_a > ν_b`; the programme returns `ν_a = ½` with `s = 0`.  Say "the closure of
   the range, by one linear programme per end; the case `s = 0` is to be excluded
   separately".  If `|y_i| < τ_i` for all `i`, every ensemble is compatible (`c → 0`): worth one
   sentence.
3. `SOFTWARE_INTERFACE.md` card N1 (lines 310–314) and ENSEMBLE-MSG-0008 §2 state the
   criterion of (b) without "`y ≠ 0`".  With zero data the "only if" fails: exact instances
   in which the ensemble is the only one with `E Φ = 0` and the features are linearly
   dependent on the support (28 of 92 zero-data instances).

### F12 (MINOR) — E25: hypotheses dropped in summary sentences

1. Line 2757 ("*Reading*"): "at its two extremes … and never in between"; card N2, lines
   324–327: "*What a length alone identifies:* only at its least or largest possible value
   … in between nothing".  True for a moment body of dimension at least two, as the
   theorem says; false for `d = 1`: two configurations with features `(1, 0)` and `(1, 2)` —
   the length `√(1 + 4w²)` determines the ensemble for every value.  Add the hypothesis.
2. Summary row E25 (line 63) and ENSEMBLE-MSG-0008: "both bounds are attained" without the
   conditions of (d).  `THEOREM_REGISTER.md` row E25: "attained when the nearest point is
   inside a facet" omits "the moment body has interior points".  That hypothesis is needed:
   equality in `ν(X ∖ Z) ≤ r_min τ/γ` forces `E_νΦ = (1 + τ/r_min) z*`, which lies in the affine
   hull of the moment body only if that hull contains the origin.  So for a moment body
   without interior whose affine hull misses the origin the first bound is attained for
   no `τ > 0` (by hand; my numerical illustration was not run).

---

## 3. The strongest hostile objection

*On E20b–E20d.*  "Nothing here is new mathematics.  E20b is the inner-point criterion of
di Dio and Schmüdgen (Theorem 40: full rank of the derivative of the moment map) applied
to the curve cut out by the sum-of-squares certificate — a core-variety step that the
same paper formalises — and the count 12 = 6·2 is the dimension count of an elliptic
normal sextic.  E20c is the description of the boundary of the moment cone of such a
curve by Baldi, Blekherman and Sinn (totals `O` and the positive two-torsion point; the
role of the real components), followed by the routine penalty argument that extends a
function non-negative on the zero set of a sum of squares to the ambient space; its
'existence' is numerical although the literature appears to give it, and no exact special
six-tuple is exhibited.  That a determinate functional can have a certificate that is not
a sum of squares is Hilbert 1888 in the language of moments (Robinson and Motzkin
examples in the paper the authors cite).  E20d is a parameter count made rigorous by a
theorem on secant varieties; above the generic rank nothing is ever unique.  What remains
is a clean worked example: the torus of three angles, five and not six, with exact ranks
at two rational points — computer algebra that no kernel has checked."

*On Part VII.*  "E23–E26 are exercises: clearing a denominator, the Charnes–Cooper
substitution, the face criterion without its normalisation row, the projection onto a
convex set, and the textbook reductions from partition and exact cover.  The one sentence
that goes beyond them — that an answer with its signs is checked in polynomial time — is
false for two of the three questions it is about.  The Part contains no noise theory and
no statement about any instrument."

A fair reply: the report labels all of this elementary and unreviewed, claims no novelty
for Part VII, and the torus statements are a complete answer for three angles that was
not found stated.  The objection stands against the words "the method" and "a certificate
beyond sums of squares" in ENSEMBLE-MSG-0009 (F10).

---

## 4. Additional observations (not findings)

* E20b(a) can be stated in the language of the cited paper: (R) holds iff the map
  (weights, positions on `Z`) ↦ data is a local diffeomorphism at the six-tuple; the data
  are then an inner point of the moment cone of `(Z, V|_Z)`.
* The value `A = 100` of S4 is specific to that instance (least value found: 30).  Two of my
  case-(a) instances need more: their Hessians at the states are positive definite only
  from `A = 141`, resp. `A = 1 640`, on, and the least `A` for which no negative value was found
  is 202, resp. 1 994 (`out_e20c_own.txt`); with `A = 100` their `f_A` is negative near a state.
  The proposition says "`A` large", so this is no defect, but a tool cannot take a fixed `A`.
* E20a: the tuples excluded by "generic" include those with two states sharing two angles
  and those with three states sharing one angle; pairwise distinct angles in every
  coordinate sufficed in 109 of 109 exact instances.
* The second rational six-tuple of S2 has two states with the same first angle (`t_1 = 0`);
  the hypotheses hold all the same (exact), so "general position" in E20b does not
  require distinct angles.

---

## 5. Sources opened, and at which level

| source | level | result |
|---|---|---|
| A. Laface, E. Postinghel, "Secant varieties of Segre–Veronese embeddings of `(ℙ¹)^r`", arXiv 1105.2136v1 | **statement read in the PDF**: pages 1–4 (Notation, Theorem 2.1 with its table, Theorem 2.2, Terracini's lemma) and 11–13 (Section 6); proofs (Sections 3–5) not read | quoted correctly in E20d(b), in the register and in `PRIOR_ART.md` §5b′; Section 6 confirms that the two exceptional systems are singular along the curve, resp. surface, of the multilinear form through the points ("the square … survives").  No journal reference on the arXiv page; the ground field is not stated on the pages read |
| P. J. di Dio, K. Schmüdgen, "The multidimensional truncated moment problem: atoms, determinacy, and core variety", arXiv 1703.01497v2 (J. Funct. Anal. 274 (2018) 3124–3148 per the arXiv page) | **read in the PDF**, pages 1–17: Theorem 18 with its proof, Corollaries 19, 20, Propositions 21, 22, Examples 23, 24, Theorems 29, 32, Section 7 (Definition 33, Lemmas 36, 37, Theorem 40 with its proof, Corollaries 41, 42, Proposition 43) | E1(b) is their Theorem 18 (fair, correctly numbered); Section 7 and Examples 23–24 are prior art that the register does not name (F10) |
| L. Baldi, G. Blekherman, R. Sinn, "Nonnegative polynomials and moment problems on algebraic curves", arXiv 2407.06017v2 | abstract page read; Theorems A–D and the statements of Sections 5–6 **only as paraphrased by a fetch tool** (not verbatim; Theorem 5.1.2 not seen) | consistent with the report's description of Theorems B and C; Sections 5–6 appear to contain the curve-level content of E20b/E20c (F10, item 3) — to be checked in the source |

**No web search was run.**  The bounded search asked for (E20b, E20c, E20d, E23(b), E25(d),
E26) was not done.  From memory only, unchecked: the classification of the multiforms for
which non-negative equals sum of squares (Choi–Lam–Reznick) presumably covers the
multidegree `(2, 2, 2)` and would be the source for "non-negative, not a lifted sum of
squares" on `𝕋³` as such.

---

## 6. Programs (`docs/ensemble/reviews/ER4_scripts/`)

| file | what it does | status |
|---|---|---|
| `er4_e20a_exact.py` → `out_e20a_exact.txt` | E20a: finiteness of the secant-plane section, exactly, by a binary sextic; the report's instance, 120 of mine, degenerate tuples | run to the end, PASS |
| `er4_e20b_exact.py` → `out_e20b_exact.txt` | E20b: lifts, smoothness, rank of (R) in three bases, `dim I_0`, exactly (own elimination over fractions); the report's two instances, 30 of mine, the instance of F1, degenerate six-tuples, states at infinity | run to the end, PASS |
| `er4_torus.py` | shared numerical tools (lift, exact conversion of products, the real curve as a double cover, loops, projection) | library |
| `er4_e20c_special.py` → `out_e20c_author_S4.txt`, `out_e20c_author_S4b.txt`, `out_e20c_stats.txt`, `out_e20c_own.txt` | E20c: all special positions of the sixth state, classification, linear programme, certificate, global search; modes `author_S4`, `author_S4b`, `stats 150`, `own` | all four modes run to the end.  The three outputs with certificates were produced before a diagnostic line was removed from the script: **ignore the words "first-order requirement along the curve … A > …"** in them — that number is a quadratic-model estimate that neglects the Hessian of `h`; it is not a bound (non-negative certificates were found far below it) |
| `er4_e20c_displacement.py` → `out_e20c_displacement.txt` | F3: twins of displaced six-tuples, three linear programmes | run to the end.  Its first line (`ε = 0`, dense sampling near the states) shows a solver status `nan`; with the coarser sampling the least mass at `ε = 0` is `1.000000` (`out_e20c_author_S4.txt`) |
| `er4_e20d_ranks.py` → `out_e20d_ranks.txt` | E20d: ranks of the double-point conditions, `r = 1, …, 5`, three primes | run to the end, PASS |
| `er4_part7.py` → `out_part7_parts_A_B_only.txt` | Part VII: A (E23(b), exact), B (tolerance), C (E25), D (E26) | **A and B run to the end; C stopped after 18 minutes without output; D never reached.**  C and D are unverified code |
| `er4_e15u.py` | E15U: (A), (B), (C′) against linear programmes; the parity example; the four-site instance | **written, never run**; no output; unverified code |
| `out_lean.txt` | source and output of the Lean scratch file (kept outside the repository) | exit 0; two linter warnings in my file |

Not re-run: `experiments/ensemble/torus_six_states.py`, `nonlinear_data_checks.py`,
`run_all.py`, `check_quotes.py`.  The comparison "report against stored output" was made by
reading `output.txt`.

---

## 7. What was not reviewed, or not finished

* **E15U beyond its main statement** (Priority 3).  Re-derived by hand, no error found: the
  membership of the two-level densities, the reduction of (A), (B), (C′) to up-sets, the
  identification of the right side of the ordered bound with `Cov(r, N − A)`, (D), the
  Fourier identity and the first-order covariance behind the weak-coupling corollary.
  **Not recomputed:** the six closed-form slacks of the parity example and its threshold
  `λ ≤ ½`, the four-site instance (`0.0105`, `0.9634`, `0.2621`, `0.2525`), check F7.  My script
  for them was never run.
* **Proposition E17.1** — not read.  **Proposition E22** — proof read once, not re-derived,
  degenerate triples not examined.  **The two constants added to E20″** — not examined.
* **E24, E25, E26** — hand derivations only.  No numerical search of mine for a
  counterexample to the attainment conditions of E25(d) was completed; the two reductions
  of E26(b) and the reduction of F5 were not replicated numerically.
* **E20c, degenerate strata** (F7, item 3) — undecided whether they satisfy the standing
  hypothesis "`Z` a smooth curve".
* **Checks S3 and S6** of `torus_six_states.py` — not replicated (S3: twins for *random*
  six-tuples; S6: sixteen states on `𝕋⁴`).  Nothing on `𝕋⁴` beyond the exact ranks was
  computed by me.
* **The author's scripts** — read (`torus_six_states.py`, `nonlinear_data_checks.py`), not
  run; `check_quotes.py` and `benchmark_controls.py` (family B8, cited by the cards) not
  examined.
* **Lean** — the statement of `eq_of_homogeneous_certificate` was type-checked through a
  scratch file against the working tree (in which `Exposedness.lean` was unchanged);
  the witness in `AxiomAudit.lean` was read, not compiled separately; no audit was run.
* **Summary documents** — only the rows, cards and messages named under "Object";
  `PRIOR_ART.md` §5b read in part.
* **Literature** — three sources, at the levels of §5; no search; Baldi–Blekherman–Sinn's
  body not read in the source.
* **Exactness.**  The special six-tuples, the classification into cases (a) and (b), the
  linear programmes and the non-negativity of the certificates are floating-point
  computations (mine as well as the report's).  No exact special six-tuple is known to
  me either.
