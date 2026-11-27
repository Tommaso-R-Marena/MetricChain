import Mathlib
import proofs.Frontiers.OracleCompensation
import proofs.Frontiers.QueryLowerBound
import proofs.Frontiers.NonAdaptive

/-!
# Theorem A of workstream F: the adaptive bound survives an exact one-body marginal oracle

*Provenance.*  This file was written by the Scientific Discovery Division, its workstream L3
(branch `research/scientific-translation`).  It is Parts 7–11 of the division's
`experiments/science/ws_L3/TheoremA.lean`, that is, its
`experiments/science/ws_L3/parts/TheoremA_tail.txt`, as published with its message SCI-MSG-0019
at its commit `9d358cb` (SHA-256 of `TheoremA.lean`
`e4f5c46f95717a17814fb183da6e8318ed7c0c841e505f14cb2f43a3676e2d70`, of `parts/TheoremA_tail.txt`
`c9b5de9dd11a29b8485b7e32bfe2f1ff5b9848e83ca09d8d3a61c1c8b83565ec`).  The division's file is generated
(its `assemble.py`) from a head, Parts 1–6 repeated word for word from its `Compensation.lean`,
and that tail, because the files of its directory cannot import each other.  Here Parts 1–6 are
imported instead — `proofs/Frontiers/OracleCompensation.lean` is that `Compensation.lean` — as
the division proposed (SCI-MSG-0019 §3).  What was changed: the import of Parts 1–6; this header
comment, which replaces the division's and keeps its list of the parts; and the removal of the
closing block of `#print axioms` commands, heading included (the audit of
`proofs/AxiomAudit.lean` walks every declaration of this file and prints the headline ones).
The four commands after this comment are those of the division's head, and from Part 7 to the
end of the namespace the text is the division's, unchanged.  It was compiled by the theory
division before adoption.  It machine-checks Theorem 11.109a (c) of the theory report (§11.29):
the first display is `theoremA_fin`, the second `Hkr_le_chernoff` and `theoremA_fin_chernoff`,
the last `theoremA_fin_Cm`; `theoremA_group_sharp` is the form with `1 + b ≤ β` and the accuracy
condition `ε < ln(1 + (e^r − 1)/β)`.  It also contains the two packing bounds
`MetricChain.expected_queries_ge_packing` and `MetricChain.nonadaptive_expected_queries_ge`
with an arbitrary oracle, class and target (`lemma1a`, `lemma1b`).  A machine-checked statement
is exactly the Lean statement: a finite seed space, a fixed finite `n`, the abstract
`MetricChain.QueryAlgorithm`.  In this file "the report" is the division's `SF_REPORT.md`, not
the theory report.  The namespace `ScienceL3` is the division's and is kept.

Science division, workstream L3.  Source: `docs/science/workstreams/SF_REPORT.md` §2.0–§2.2
(setting, Lemmas 0–3, Theorem A).

This file imports Mathlib, `proofs/Frontiers/OracleCompensation.lean` (Parts 1–6: the cone, the
class, Lemmas 0, 2, 3), `proofs/Frontiers/QueryLowerBound.lean` (for `MetricChain.QueryAlgorithm`
and the packing bound `MetricChain.expected_queries_ge_packing`) and
`proofs/Frontiers/NonAdaptive.lean` (for `MetricChain.nonadaptive_expected_queries_ge`, used only
in Lemma 1 (b)).  Here:

* Part 7 — **Lemma 1 (a)** and **Lemma 1 (b)** in the oracle-indexed model of workstream L1
  (`lemma1a_weighted`, `lemma1a`, `lemma1a_div`; `lemma1b_weighted`, `lemma1b`): an oracle algorithm is a family `alg ω o` of query algorithms
  indexed by the seed `ω` and the oracle's answer `o`; on the instance `g` it runs
  `alg ω (O g)`.  Derived from `MetricChain.expected_queries_ge_packing` applied to the class
  restricted to the instances with the oracle answer of `g₀`.
* Part 8 — the same in the weights, for the one-body marginal oracle on the cube
  (`oracle_packing_weights`); the family of alternatives of Theorem A (cyclic averages of dips,
  `barW`) with its invariance, mass, density, membership of the class and the counting bound.
* Part 9 — **Theorem A, the every-`n` statement** `E|Q(ψ₀)| ≥ (1 − 2δ)/(n·H_{k,r})`
  (`theoremA_group_sharp`, `theoremA_group`, `theoremA_group_div`, `theoremA_fin`).
* Part 10 — **the Chernoff form** `H_{k,r} ≤ (n+1)·e^{tr}·ρ_t(k/n; γ)ⁿ` (`Hkr_le_chernoff`, from the
  binomial mode bound `binomial_mode_bound` and `card_wt_eq`), and Theorem A with it
  (`theoremA_group_chernoff`, `theoremA_fin_chernoff`).
* Part 11 — **the last display of Theorem A**, with the constant `C_m`
  (`theoremA_group_Cm`, `theoremA_fin_Cm`).

Nothing is assumed: no statement of the report enters as a hypothesis.
-/

set_option autoImplicit false

noncomputable section

namespace ScienceL3

open Finset

/-! # Part 7: Lemma 1 (a) — indistinguishability with an oracle -/

section OracleLemma

open Classical in
/-- **Lemma 1 (a) (indistinguishability with an oracle), weighted form.**  `G` a class of
instances, `Φ` the target, `O` an oracle (any function of the instance).  An oracle algorithm is
a family `alg ω o` of query algorithms indexed by the seed `ω` and the oracle's answer `o`; on
the instance `g` it runs `alg ω (O g)`.  If it is `(ε/2, δ)`-correct on `G`, and `alt j` are
members of `G` with the oracle answer of `g₀ ∈ G` and `|Φ (alt j) − Φ g₀| > ε`, then for all
weights `wgt ≥ 0` such that every point lies in difference sets `{alt j ≠ g₀}` of total weight at
most `B`: `(1 − 2δ) · Σ_j wgt j ≤ E[#evaluations on g₀] · B`.

This is the theory division's `MetricChain.expected_queries_ge_packing` applied to the plain
query algorithm `alg ω (O g₀)` and the class `{g ∈ G : O g = O g₀}` (the argument of workstream
L1's `theorem4_adaptive_marginal_oracle`, for an arbitrary oracle and class). -/
theorem lemma1a_weighted {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) (wgt : J → ℝ) (hwgt : ∀ j, 0 ≤ wgt j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => alt j a ≠ g₀ a), wgt j ≤ B) :
    (1 - 2 * δ) * ∑ j, wgt j ≤ (∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card) * B := by
  have hcorr' : ∀ g : X → ℝ, (G g ∧ O g = O g₀) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g₀)).output g - Φ g| ≤ ε / 2), P ω := by
    rintro g ⟨hg, hOg⟩
    have h := hcorr g hg
    rw [hOg] at h
    exact h
  exact MetricChain.expected_queries_ge_packing (G := fun g => G g ∧ O g = O g₀) (Φ := Φ)
    (fun ω => alg ω (O g₀)) P hP hP1 hcorr' (g := g₀) ⟨hg₀, rfl⟩ alt
    (fun j => ⟨halt j, hO j⟩) hsens wgt hwgt hcap

open Classical in
/-- **Lemma 1 (a), counting form** (the statement of the report): if every point lies in at most
`B` of the difference sets `D_j = {alt j ≠ g₀}`, then
`(1 − 2δ) · |J| ≤ E[#evaluations on g₀] · B`. -/
theorem lemma1a {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) {B : ℝ}
    (hcap : ∀ a, ((univ.filter fun j => alt j a ≠ g₀ a).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) ≤
      (∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card) * B := by
  have h := lemma1a_weighted O alg P hP hP1 hcorr hg₀ alt halt hO hsens (fun _ => (1 : ℝ))
    (fun _ => zero_le_one) (B := B) (fun a => by
      rw [Finset.sum_const, nsmul_eq_mul, mul_one]
      exact hcap a)
  rwa [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one] at h

open Classical in
/-- **Lemma 1 (a), as displayed in the report:**
`E[#evaluations on g₀] ≥ (1 − 2δ)·|J| / max_x #{j : x ∈ D_j}` (for a positive bound `B` on the
multiplicity). -/
theorem lemma1a_div {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    {g₀ : X → ℝ} (hg₀ : G g₀) {J : Type*} [Fintype J] (alt : J → X → ℝ)
    (halt : ∀ j, G (alt j)) (hO : ∀ j, O (alt j) = O g₀)
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g₀|) {B : ℝ} (hB : 0 < B)
    (hcap : ∀ a, ((univ.filter fun j => alt j a ≠ g₀ a).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) / B ≤
      ∑ ω, P ω * ((alg ω (O g₀)).queries g₀).card := by
  rw [div_le_iff₀ hB]
  exact lemma1a O alg P hP hP1 hcorr hg₀ alt halt hO hsens hcap

open Classical in
/-- **Lemma 1 (b) (non-adaptive algorithms with an oracle), weighted form.**  An oracle
algorithm is *non-adaptive* if for each seed `ω` and oracle answer `o` its query set `Q ω o`
does not depend on the instance.  Let `(g j, g' j)` be pairs of members of the class, **all
with the same oracle answer `o₀`**, with `|Φ (g' j) − Φ (g j)| > ε`.  For weights `wgt ≥ 0` such
that every point lies in difference sets `{g' j ≠ g j}` of total weight at most `B`:
`(1 − 2δ) · Σ_j wgt j ≤ E[#evaluations with the answer o₀] · B`.

This is the theory division's `MetricChain.nonadaptive_expected_queries_ge` applied to the
plain algorithm `alg ω o₀` and the class `{g ∈ G : O g = o₀}`. -/
theorem lemma1b_weighted {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Θ → Finset X) (hna : ∀ ω o g, (alg ω o).queries g = Q ω o) (o₀ : Θ)
    {J : Type*} [Fintype J] (g g' : J → X → ℝ) (hg : ∀ j, G (g j)) (hg' : ∀ j, G (g' j))
    (hO : ∀ j, O (g j) = o₀) (hO' : ∀ j, O (g' j) = o₀)
    (hsens : ∀ j, ε < |Φ (g' j) - Φ (g j)|) (wgt : J → ℝ) (hwgt : ∀ j, 0 ≤ wgt j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => g' j a ≠ g j a), wgt j ≤ B) :
    (1 - 2 * δ) * ∑ j, wgt j ≤ (∑ ω, P ω * (Q ω o₀).card) * B := by
  have hcorr' : ∀ f : X → ℝ, (G f ∧ O f = o₀) →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω o₀).output f - Φ f| ≤ ε / 2), P ω := by
    rintro f ⟨hf, hOf⟩
    have h := hcorr f hf
    rw [hOf] at h
    exact h
  exact MetricChain.nonadaptive_expected_queries_ge (G := fun f => G f ∧ O f = o₀) (Φ := Φ)
    (fun ω => alg ω o₀) P hP hP1 hcorr' (fun ω => Q ω o₀) (fun ω f => hna ω o₀ f) g g'
    (fun j => ⟨hg j, hO j⟩) (fun j => ⟨hg' j, hO' j⟩) hsens wgt hwgt hcap

open Classical in
/-- **Lemma 1 (b), counting form** (the statement of the report): if every point lies in at most
`B` of the difference sets `D_j = {g' j ≠ g j}`, then
`(1 − 2δ) · |J| ≤ E[#evaluations] · B`. -/
theorem lemma1b {X Θ : Type*} {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}
    (O : (X → ℝ) → Θ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → Θ → MetricChain.QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω (O g)).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Θ → Finset X) (hna : ∀ ω o g, (alg ω o).queries g = Q ω o) (o₀ : Θ)
    {J : Type*} [Fintype J] (g g' : J → X → ℝ) (hg : ∀ j, G (g j)) (hg' : ∀ j, G (g' j))
    (hO : ∀ j, O (g j) = o₀) (hO' : ∀ j, O (g' j) = o₀)
    (hsens : ∀ j, ε < |Φ (g' j) - Φ (g j)|) {B : ℝ}
    (hcap : ∀ a, ((univ.filter fun j => g' j a ≠ g j a).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) ≤ (∑ ω, P ω * (Q ω o₀).card) * B := by
  have h := lemma1b_weighted O alg P hP hP1 hcorr Q hna o₀ g g' hg hg' hO hO' hsens
    (fun _ => (1 : ℝ)) (fun _ => zero_le_one) (B := B) (fun a => by
      rw [Finset.sum_const, nsmul_eq_mul, mul_one]
      exact hcap a)
  rwa [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one] at h

end OracleLemma

/-! # Part 8: the one-body oracle on the cube; the family of alternatives of Theorem A -/

section CubeOracle

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- **The target** `ln A(ψ) = ln Σ_x π(x) e^{−ψ(x)}`. -/
def logA (π ψ : (ι → Bool) → ℝ) : ℝ := Real.log (massW π fun x => Real.exp (-ψ x))

/-- **The exact one-body marginal oracle** `o(ψ) = (μ_ψ(x_i = 1))_i`. -/
def oracle1 (π ψ : (ι → Bool) → ℝ) : ι → ℝ := fun i => margW π (fun x => Real.exp (-ψ x)) i

theorem oracle1_neg_log {π w : (ι → Bool) → ℝ} (hw : ∀ x, 0 < w x) :
    oracle1 π (fun x => -Real.log (w x)) = fun i => margW π w i := by
  have e : (fun x => Real.exp (-(-Real.log (w x)))) = w := by
    funext x
    rw [neg_neg, Real.exp_log (hw x)]
  show (fun i => margW π (fun x => Real.exp (-(-Real.log (w x)))) i) = _
  rw [e]

theorem logA_neg_log {π w : (ι → Bool) → ℝ} (hw : ∀ x, 0 < w x) :
    logA π (fun x => -Real.log (w x)) = Real.log (massW π w) := by
  have e : (fun x => Real.exp (-(-Real.log (w x)))) = w := by
    funext x
    rw [neg_neg, Real.exp_log (hw x)]
  show Real.log (massW π (fun x => Real.exp (-(-Real.log (w x))))) = _
  rw [e]

open Classical in
/-- **Lemma 1 (a) in the weights, for the one-body oracle on the cube.**  Class `L_u`, target
`ln A`, oracle `oracle1 π`.  Let `w₀ ∈ 𝒲_u` and `w₁ j ∈ 𝒲_u` (`j ∈ J`) all have **all one-body
marginals equal to the same number `c`**, with `ln A(w₁ j) − ln A(w₀) > ε`.  If every point `x`
has `w₁ j x ≠ w₀ x` for at most `B` indices `j`, every `(ε/2, δ)`-correct oracle algorithm makes
at least `(1 − 2δ)|J|/B` evaluations in expectation on `ψ₀ = −ln w₀`. -/
theorem oracle_packing_weights {π : (ι → Bool) → ℝ} {u : ℝ}
    {Ω : Type*} [Fintype Ω] (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool))
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω (oracle1 π ψ)).output ψ - logA π ψ| ≤ ε / 2), P ω)
    {w₀ : (ι → Bool) → ℝ} (hw₀ : InCone u w₀) {c : ℝ} (hc₀ : ∀ i, margW π w₀ i = c)
    {J : Type*} [Fintype J] (w₁ : J → (ι → Bool) → ℝ) (hw₁ : ∀ j, InCone u (w₁ j))
    (hc₁ : ∀ j i, margW π (w₁ j) i = c)
    (hgap : ∀ j, ε < Real.log (massW π (w₁ j)) - Real.log (massW π w₀)) {B : ℝ}
    (hcap : ∀ x, ((univ.filter fun j => w₁ j x ≠ w₀ x).card : ℝ) ≤ B) :
    (1 - 2 * δ) * (Fintype.card J : ℝ) ≤
      (∑ ω, P ω * ((alg ω (oracle1 π fun x => -Real.log (w₀ x))).queries
        fun x => -Real.log (w₀ x)).card) * B := by
  refine lemma1a (G := LipH u) (Φ := logA π) (oracle1 π) alg P hP hP1 hcorr
    (g₀ := fun x => -Real.log (w₀ x)) ((inCone_iff_lipH_log hw₀.1).mp hw₀)
    (fun j x => -Real.log (w₁ j x)) (fun j => (inCone_iff_lipH_log (hw₁ j).1).mp (hw₁ j))
    (fun j => ?_) (fun j => ?_) (fun a => ?_)
  · rw [oracle1_neg_log (hw₁ j).1, oracle1_neg_log hw₀.1]
    funext i
    rw [hc₁ j i, hc₀ i]
  · rw [logA_neg_log (hw₁ j).1, logA_neg_log hw₀.1]
    exact lt_of_lt_of_le (hgap j) (le_abs_self _)
  · refine le_trans ?_ (hcap a)
    have hsub : (univ.filter fun j => (fun j x => -Real.log (w₁ j x)) j a ≠
        (fun x => -Real.log (w₀ x)) a) ⊆ univ.filter fun j => w₁ j a ≠ w₀ a := by
      intro j hj
      rw [Finset.mem_filter] at hj ⊢
      exact ⟨hj.1, fun h => hj.2 (congrArg (fun t => -Real.log t) h)⟩
    exact_mod_cast Finset.card_le_card hsub

open Classical in
/-- **The correctness hypothesis of Theorem A is satisfiable** (so the theorem is not vacuous):
for `ε ≥ 0`, `δ ≥ 0` the algorithm that evaluates `ψ` everywhere and returns `ln A(ψ)` (the
theory division's `fullQueryAlgorithm`, ignoring the oracle; one seed) is `(ε/2, δ)`-correct
on every class. -/
theorem exists_correct_oracle_algorithm (π : (ι → Bool) → ℝ) (u : ℝ) {ε δ : ℝ} (hε : 0 ≤ ε)
    (hδ : 0 ≤ δ) :
    ∃ (alg : Unit → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Unit → ℝ),
      (∀ ω, 0 ≤ P ω) ∧ ∑ ω, P ω = 1 ∧
      ∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
        |(alg ω (oracle1 π ψ)).output ψ - logA π ψ| ≤ ε / 2), P ω := by
  refine ⟨fun _ _ => MetricChain.fullQueryAlgorithm (logA π), fun _ => 1,
    fun _ => zero_le_one, by simp, fun ψ _ => ?_⟩
  have hfil : (univ.filter fun _ω : Unit =>
      |(MetricChain.fullQueryAlgorithm (logA π)).output ψ - logA π ψ| ≤ ε / 2) = univ := by
    apply Finset.filter_true_of_mem
    intro ω _
    show |logA π ψ - logA π ψ| ≤ ε / 2
    rw [sub_self, abs_zero]
    linarith
  rw [hfil, Finset.sum_const, Finset.card_univ, Fintype.card_unit, one_smul]
  linarith

/-- There is a configuration with exactly `k` ones, for every `k ≤ n`. -/
theorem exists_wt_eq {k : ℕ} (hk : k ≤ Fintype.card ι) : ∃ s : ι → Bool, wt s = k := by
  have hk' : k ≤ (univ : Finset ι).card := by
    rw [Finset.card_univ]
    exact hk
  obtain ⟨t, _, ht⟩ := Finset.exists_subset_card_eq hk'
  refine ⟨fun i => decide (i ∈ t), ?_⟩
  unfold wt
  rw [← ht]
  congr 1
  ext i
  simp

/-- `T_k`, the configurations with exactly `k` ones, as a type. -/
abbrev Tk (ι : Type*) [Fintype ι] (k : ℕ) : Type _ := {s : ι → Bool // wt s = k}

/-- A site permutation acts on `T_k`. -/
def permTk (k : ℕ) (σ : Equiv.Perm ι) : Tk ι k ≃ Tk ι k where
  toFun j := ⟨j.1 ∘ σ, by rw [wt_perm]; exact j.2⟩
  invFun j := ⟨j.1 ∘ σ.symm, by rw [wt_perm]; exact j.2⟩
  left_inv j := by
    apply Subtype.ext
    funext i
    simp
  right_inv j := by
    apply Subtype.ext
    funext i
    simp

theorem card_filter_subtype {α : Type*} [Fintype α] (p q : α → Prop) [DecidablePred p]
    [DecidablePred q] :
    (univ.filter fun j : {a // p a} => q j.1).card = (univ.filter fun a => p a ∧ q a).card := by
  refine Finset.card_bij (fun j _ => j.1) ?_ ?_ ?_
  · intro j hj
    rw [Finset.mem_filter] at hj ⊢
    exact ⟨Finset.mem_univ _, j.2, hj.2⟩
  · intro j₁ _ j₂ _ h
    exact Subtype.ext h
  · intro a ha
    rw [Finset.mem_filter] at ha
    exact ⟨⟨a, ha.2.1⟩, Finset.mem_filter.mpr ⟨Finset.mem_univ _, ha.2.2⟩, rfl⟩

/-- The number of centres `s ∈ T_k` with `x ∈ D_{s,r}`. -/
def dipCount (p u γ r : ℝ) (k : ℕ) (x : ι → Bool) : ℕ :=
  (univ.filter fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x).card

/-- **`H_{k,r} = max_x P_{s ∼ Unif(T_k)}[x ∈ D_{s,r}]`.** -/
def Hkr (ι : Type*) [Fintype ι] [DecidableEq ι] (p u γ r : ℝ) (k : ℕ) : ℝ :=
  ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) /
    ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ)

/-! ### Translations of the sites; the averaged excess -/

section Shifts

variable [AddGroup ι]

/-- The translations `i ↦ i + a` of the sites (for `ι = Fin n`: the cyclic shifts). -/
def shiftSet (ι : Type*) [AddGroup ι] : Set (Equiv.Perm ι) :=
  Set.range (Equiv.addRight : ι → Equiv.Perm ι)

omit [Fintype ι] [DecidableEq ι] in
theorem shiftSet_transitive : SiteTransitive (shiftSet ι) := fun i j =>
  ⟨Equiv.addRight (-i + j), ⟨_, rfl⟩, by
    show i + (-i + j) = j
    rw [add_neg_cancel_left]⟩

/-- On `Fin n` the translations are the cyclic shifts `i ↦ i + a mod n`. -/
theorem addRight_fin_val {n : ℕ} [NeZero n] (a i : Fin n) :
    ((Equiv.addRight a : Equiv.Perm (Fin n)) i).val = (i.val + a.val) % n :=
  Fin.val_add i a

/-- **The averaged excess** `Δ̄_s = n⁻¹ Σ_a Δ_{σ^a s, r}`, the average of the excess of the dip
over the `n` translates of its centre. -/
def barW (p u γ r : ℝ) (s : ι → Bool) (x : ι → Bool) : ℝ :=
  (∑ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) x) / (Fintype.card ι : ℝ)

omit [DecidableEq ι] in
theorem barW_nonneg (p u γ r : ℝ) (s x : ι → Bool) : 0 ≤ barW p u γ r s x :=
  div_nonneg (Finset.sum_nonneg fun _ _ => dipW_nonneg p u γ r _ x) (Nat.cast_nonneg _)

omit [DecidableEq ι] in
/-- `Δ̄_s` is invariant under the translations. -/
theorem barW_shift (p u γ r : ℝ) (s x : ι → Bool) (b : ι) :
    barW p u γ r s (x ∘ Equiv.addRight b) = barW p u γ r s x := by
  unfold barW
  congr 1
  have h1 : ∀ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) (x ∘ Equiv.addRight b) =
      dipW p u γ r (s ∘ Equiv.addRight (-b + a)) x := by
    intro a
    have e : s ∘ Equiv.addRight a = (s ∘ Equiv.addRight (-b + a)) ∘ Equiv.addRight b := by
      funext i
      show s (i + a) = s (i + b + (-b + a))
      rw [add_assoc, add_neg_cancel_left]
    rw [e, dipW_perm]
  rw [Finset.sum_congr rfl fun a _ => h1 a]
  exact Equiv.sum_comp (Equiv.addLeft (-b)) fun c => dipW p u γ r (s ∘ Equiv.addRight c) x

omit [DecidableEq ι] in
theorem barW_invariant (p u γ r : ℝ) (s : ι → Bool) :
    Invariant (shiftSet ι) (barW p u γ r s) := by
  rintro σ ⟨b, rfl⟩ x
  exact barW_shift p u γ r s x b

omit [AddGroup ι] in
/-- The mass of an average is the average of the masses. -/
theorem massW_avg (π : (ι → Bool) → ℝ) {κ : Type*} (t : Finset κ)
    (f : κ → (ι → Bool) → ℝ) (N : ℝ) :
    massW π (fun x => (∑ a ∈ t, f a x) / N) = (∑ a ∈ t, massW π (f a)) / N := by
  unfold massW
  rw [Finset.sum_comm, Finset.sum_div]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [← Finset.mul_sum, mul_div_assoc]

omit [AddGroup ι] in
theorem wtsum_eq_massW (π w : (ι → Bool) → ℝ) :
    ∑ x, π x * w x * (wt x : ℝ) = massW (fun x => π x * (wt x : ℝ)) w := by
  unfold massW
  exact Finset.sum_congr rfl fun x _ => by ring

/-- `A(Δ̄_s) = A(Δ_{s,r})`. -/
theorem massW_barW (p u γ r : ℝ) (s : ι → Bool) :
    massW (refW p) (barW p u γ r s) = massW (refW p) (dipW p u γ r s) := by
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0.ne'
  unfold barW
  rw [massW_avg, Finset.sum_congr rfl fun a _ => massW_dipW_perm p u γ r s (Equiv.addRight a),
    Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_div_cancel_left₀ _ hn]

/-- `dens(Δ̄_s) = dens(Δ_{s,r})`. -/
theorem densW_barW (p u γ r : ℝ) (s : ι → Bool) :
    densW (refW p) (barW p u γ r s) = densW (refW p) (dipW p u γ r s) := by
  have hn : (Fintype.card ι : ℝ) ≠ 0 := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0.ne'
  have hw : ∑ x, refW p x * barW p u γ r s x * (wt x : ℝ) =
      ∑ x, refW p x * dipW p u γ r s x * (wt x : ℝ) := by
    rw [wtsum_eq_massW, wtsum_eq_massW]
    unfold barW
    have hterm : ∀ a : ι, massW (fun x => refW p x * (wt x : ℝ))
        (dipW p u γ r (s ∘ Equiv.addRight a)) =
        massW (fun x => refW p x * (wt x : ℝ)) (dipW p u γ r s) := fun a =>
      massW_perm (Equiv.addRight a) (fun x => by rw [refW_perm, wt_perm])
        fun x => dipW_perm p u γ r s (Equiv.addRight a) x
    rw [massW_avg, Finset.sum_congr rfl fun a _ => hterm a, Finset.sum_const, Finset.card_univ,
      nsmul_eq_mul, mul_div_cancel_left₀ _ hn]
  unfold densW
  rw [hw, massW_barW]

/-- `w̃_γ + Δ̄_s`, an average of `n` dips, is in the class. -/
theorem baseW_add_barW_inCone {p u γ : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 ≤ u)
    (hγ : |γ| ≤ u) (r : ℝ) (s : ι → Bool) :
    InCone u (fun x => baseW p γ x + barW p u γ r s x) := by
  have hn : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0
  have h := (InCone.sum (s := (univ : Finset ι)) ⟨0, Finset.mem_univ 0⟩
    (f := fun a x => baseW p γ x + dipW p u γ r (s ∘ Equiv.addRight a) x)
    (fun a _ => baseW_add_dipW_inCone hp0 hp1 hu hγ r _)).smul (inv_pos.mpr hn)
  have e : (fun x => baseW p γ x + barW p u γ r s x) =
      fun x => (Fintype.card ι : ℝ)⁻¹ *
        ∑ a : ι, (baseW p γ x + dipW p u γ r (s ∘ Equiv.addRight a) x) := by
    funext x
    unfold barW
    rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    field_simp
  rw [e]
  exact h

omit [DecidableEq ι] in
/-- `{Δ̄_s > 0} ⊆ ∪_a D_{σ^a s, r}`. -/
theorem exists_of_barW_ne_zero {p u γ r : ℝ} {s x : ι → Bool} (h : barW p u γ r s x ≠ 0) :
    ∃ a : ι, dipW p u γ r (s ∘ Equiv.addRight a) x ≠ 0 := by
  by_contra hno
  apply h
  unfold barW
  rw [Finset.sum_eq_zero fun a _ => not_not.mp fun h' => hno ⟨a, h'⟩, zero_div]

/-- **The counting step of Theorem A**: a point lies in `{Δ̄_s > 0}` for at most
`n · #{s ∈ T_k : x ∈ D_{s,r}}` centres `s ∈ T_k` (the translations permute `T_k`). -/
theorem card_barW_ne_zero_le (p u γ r : ℝ) (k : ℕ) (x : ι → Bool) :
    (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card ≤
      Fintype.card ι * (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
  have hsub : (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0) ⊆
      (univ : Finset ι).biUnion fun a =>
        univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0 := by
    intro j hj
    obtain ⟨a, ha⟩ := exists_of_barW_ne_zero (Finset.mem_filter.mp hj).2
    exact Finset.mem_biUnion.mpr
      ⟨a, Finset.mem_univ a, Finset.mem_filter.mpr ⟨Finset.mem_univ j, ha⟩⟩
  have hcard : ∀ a : ι,
      (univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card =
        (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
    intro a
    refine Finset.card_equiv (permTk k (Equiv.addRight a)) fun j => ?_
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    rfl
  calc (univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card
      ≤ ((univ : Finset ι).biUnion fun a =>
          univ.filter fun j : Tk ι k => dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card :=
        Finset.card_le_card hsub
    _ ≤ ∑ a : ι, (univ.filter fun j : Tk ι k =>
          dipW p u γ r (j.1 ∘ Equiv.addRight a) x ≠ 0).card := Finset.card_biUnion_le
    _ = ∑ _a : ι, (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card :=
        Finset.sum_congr rfl fun a _ => hcard a
    _ = Fintype.card ι * (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card := by
        rw [Finset.sum_const, Finset.card_univ, smul_eq_mul]

end Shifts

end CubeOracle

/-! # Part 9: Theorem A -/

section TheoremA

/-- `ω = p₊ − p₋`, the width of the window. -/
def omegaW (p u : ℝ) : ℝ := pTilt p (-u) - pTilt p u

/-- `ω_m = ω · min(m, 1 − m)`, `m = k/n`. -/
def omegaM (p u : ℝ) (k n : ℕ) : ℝ := omegaW p u * min ((k : ℝ) / n) (1 - (k : ℝ) / n)

/-- `κ = ω_m − 1/(e^r − 1)`. -/
def kappaA (p u r : ℝ) (k n : ℕ) : ℝ := omegaM p u k n - 1 / (Real.exp r - 1)

/-- `β = ω/κ`. -/
def betaA (p u r : ℝ) (k n : ℕ) : ℝ := omegaW p u / kappaA p u r k n

/-- The density `c₀(m) = (1 − m)p₋ + m·p₊` of the cone law is at distance at least
`ω·min(m, 1 − m)` from both ends of the window. -/
theorem cone_density_margin {pm pp : ℝ} (hω : pm ≤ pp) {k n : ℕ} (hn : 0 < n) :
    pm + (pp - pm) * min ((k : ℝ) / n) (1 - (k : ℝ) / n) ≤
        ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n ∧
      ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n ≤
        pp - (pp - pm) * min ((k : ℝ) / n) (1 - (k : ℝ) / n) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have e : ((k : ℝ) * pp + ((n : ℝ) - k) * pm) / n = pm + (pp - pm) * ((k : ℝ) / n) := by
    field_simp
    ring
  have h0 : 0 ≤ pp - pm := by linarith
  have h1 := mul_le_mul_of_nonneg_left (min_le_left ((k : ℝ) / n) (1 - (k : ℝ) / n)) h0
  have h2 := mul_le_mul_of_nonneg_left (min_le_right ((k : ℝ) / n) (1 - (k : ℝ) / n)) h0
  rw [e]
  constructor <;> linarith

/-- The choice of the compensator in the proof of Theorem A: if `p_γ` is in the window
`[p₋, p₊]` and `c` is in `[p₋ + κ, p₊ − κ]`, one end `p₂` of the window and a coefficient
`b ≥ 0` with `1 + b ≤ ω/κ` satisfy `p_γ + b·p₂ = c·(1 + b)`.  (The report states `b ≤ ω/κ`; the
proof gives `1 + b ≤ ω/κ`.) -/
theorem exists_compensator {pm pp pg c κ : ℝ} (hκ : 0 < κ) (hpg1 : pm ≤ pg) (hpg2 : pg ≤ pp)
    (hc1 : pm + κ ≤ c) (hc2 : c ≤ pp - κ) :
    ∃ p₂ : ℝ, (p₂ = pp ∨ p₂ = pm) ∧ ∃ b : ℝ, 0 ≤ b ∧ 1 + b ≤ (pp - pm) / κ ∧
      pg + b * p₂ = c * (1 + b) := by
  by_cases h : pg ≤ c
  · have hpos : 0 < pp - c := by linarith
    refine ⟨pp, Or.inl rfl, (c - pg) / (pp - c), div_nonneg (by linarith) hpos.le, ?_, ?_⟩
    · have e : 1 + (c - pg) / (pp - c) = (pp - pg) / (pp - c) := by
        field_simp
        ring
      rw [e, div_le_div_iff₀ hpos hκ]
      exact mul_le_mul (by linarith) (by linarith) hκ.le (by linarith)
    · field_simp
      ring
  · have hpos : 0 < c - pm := by linarith
    have h' : c < pg := not_le.mp h
    refine ⟨pm, Or.inr rfl, (pg - c) / (c - pm), div_nonneg (by linarith) hpos.le, ?_, ?_⟩
    · have e : 1 + (pg - c) / (c - pm) = (pg - pm) / (c - pm) := by
        field_simp
        ring
      rw [e, div_le_div_iff₀ hpos hκ]
      exact mul_le_mul (by linarith) (by linarith) hκ.le (by linarith)
    · field_simp
      ring

universe v

variable {ι : Type*} [Fintype ι] [DecidableEq ι] [AddGroup ι]

open Classical in
/-- **Theorem A, sharpened (every `n`; adaptive algorithms with an exact one-body oracle).**

Sites: any finite additive group `ι` acting on itself by translation, `n = |ι|` (for `ι = Fin n`
the cyclic shifts of the report: `theoremA_fin`).  `0 < p < 1`, `|γ| ≤ u`, `r > 0`, `k ≤ n`,
`ω_m = ω·min(k/n, 1 − k/n)`, `(e^r − 1)·ω_m > 1`, `κ = ω_m − 1/(e^r − 1)`, `β = ω/κ`.

There are `γ₂ ∈ {−u, +u}` and `b ≥ 0` with `1 + b ≤ β` such that the instance
`ψ₀ = −ln(w̃_γ + b·w̃_{γ₂})` is in `L_u`, and every randomised oracle algorithm
(`alg ω o`, run on `ψ` with the oracle answer `o = oracle1 π ψ`, the vector of the one-body
marginals of `μ_ψ`) that is `(ε/2, δ)`-correct for `ln A` on `L_u`, for some
`ε < ln(1 + (e^r − 1)/β)`, satisfies

    1 − 2δ ≤ E[#evaluations on ψ₀] · n · H_{k,r},

`H_{k,r} = max_x P_{s∼Unif(T_k)}[x ∈ D_{s,r}]`.  (The report has `b ≤ β` and the smaller
threshold `ln(1 + (e^r − 1)/(1 + β))`: `theoremA_group`.) -/
theorem theoremA_group_sharp {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u)
    (hr : 0 < r) {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ 1 + b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / betaA p u r k (Fintype.card ι)) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) := by
  -- basic quantities
  have hu : 0 ≤ u := (abs_nonneg γ).trans hγ
  have hnpos : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
  haveI : Nonempty ι := ⟨0⟩
  have hR1 : 0 < Real.exp r - 1 := by
    have h := Real.one_lt_exp_iff.mpr hr
    linarith
  have hpmpp : pTilt p u ≤ pTilt p (-u) := pTilt_anti hp0 hp1 (by linarith)
  have hω0 : 0 ≤ omegaW p u := by
    unfold omegaW
    linarith
  have hκ : 0 < kappaA p u r k (Fintype.card ι) := by
    unfold kappaA
    rw [sub_pos, div_lt_iff₀ hR1]
    linarith [mul_comm (Real.exp r - 1) (omegaM p u k (Fintype.card ι))]
  -- a fixed centre; mass and density of the dips
  obtain ⟨s₀, hs₀⟩ := exists_wt_eq (ι := ι) hk
  obtain ⟨E, hE⟩ : ∃ E : ℝ, massW (refW p) (dipW p u γ r s₀) = E := ⟨_, rfl⟩
  obtain ⟨c, hc⟩ : ∃ c : ℝ, densW (refW p) (dipW p u γ r s₀) = c := ⟨_, rfl⟩
  have hEc : ∀ s : ι → Bool, wt s = k →
      massW (refW p) (dipW p u γ r s) = E ∧ densW (refW p) (dipW p u γ r s) = c := by
    intro s hs
    have h := massW_densW_dipW_of_wt_eq p u γ r (hs₀.trans hs.symm)
    rw [hE, hc] at h
    exact h
  -- Lemma 2
  have hE1 : Real.exp r - 1 ≤ E := by
    rw [← hE]
    exact (lemma2_mass hp0 hp1 u γ r s₀).1
  have hEpos : 0 < E := lt_of_lt_of_le hR1 hE1
  have hc0 := lemma2_dens hp0 hp1 u γ hr s₀
  rw [hc, densW_coneW hp0 hp1 u s₀, hs₀] at hc0
  have hmargin := cone_density_margin (k := k) hpmpp hnpos
  have hc0' := abs_le.mp hc0
  have hc_lo : pTilt p u + kappaA p u r k (Fintype.card ι) ≤ c := by
    unfold kappaA omegaM omegaW
    linarith [hmargin.1, hc0'.1]
  have hc_hi : c ≤ pTilt p (-u) - kappaA p u r k (Fintype.card ι) := by
    unfold kappaA omegaM omegaW
    linarith [hmargin.2, hc0'.2]
  -- the compensator
  have hγ' := abs_le.mp hγ
  have hpg1 : pTilt p u ≤ pTilt p γ := pTilt_anti hp0 hp1 hγ'.2
  have hpg2 : pTilt p γ ≤ pTilt p (-u) := pTilt_anti hp0 hp1 hγ'.1
  obtain ⟨p₂, hp₂, b, hb0, hbβ', hbeq⟩ := exists_compensator hκ hpg1 hpg2 hc_lo hc_hi
  have hbβ : 1 + b ≤ betaA p u r k (Fintype.card ι) := hbβ'
  obtain ⟨γ₂, hγ₂, hγ₂p⟩ : ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ pTilt p γ₂ = p₂ := by
    rcases hp₂ with h | h
    · exact ⟨-u, Or.inl rfl, h.symm⟩
    · exact ⟨u, Or.inr rfl, h.symm⟩
  have hγ₂u : |γ₂| ≤ u := by
    rcases hγ₂ with h | h
    · rw [h, abs_neg, abs_of_nonneg hu]
    · rw [h, abs_of_nonneg hu]
  have hw₀ : InCone u (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) :=
    (baseW_inCone hp0 hp1 hγ).add_smul (baseW_inCone hp0 hp1 hγ₂u) hb0
  have hb1 : 0 < 1 + b := by linarith
  refine ⟨γ₂, hγ₂, b, hb0, hbβ, (inCone_iff_lipH_log hw₀.1).mp hw₀, ?_⟩
  intro Ω _ alg P hP hP1 ε δ hε hcorr
  -- the compensated base: mass 1 + b, all marginals c
  have hm0 : massW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) = 1 + b := by
    rw [massW_add, massW_smul]
    unfold baseW
    rw [massW_tiltW hp0 hp1, massW_tiltW hp0 hp1, mul_one]
  have ho0 : ∀ i, oneW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) i =
      c * (1 + b) := by
    intro i
    rw [oneW_add, oneW_smul]
    unfold baseW
    rw [oneW_tiltW hp0 hp1, oneW_tiltW hp0 hp1, hγ₂p]
    exact hbeq
  have hmarg0 : ∀ i,
      margW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x) i = c := by
    intro i
    unfold margW
    rw [ho0 i, hm0, mul_div_assoc, div_self hb1.ne', mul_one]
  -- the alternatives
  have hbarm : ∀ j : Tk ι k, massW (refW p) (barW p u γ r j.1) = E := fun j => by
    rw [massW_barW]
    exact (hEc j.1 j.2).1
  have hbard : ∀ j : Tk ι k, densW (refW p) (barW p u γ r j.1) = c := fun j => by
    rw [densW_barW]
    exact (hEc j.1 j.2).2
  have hbaro : ∀ (j : Tk ι k) (i : ι), oneW (refW p) (barW p u γ r j.1) i = c * E := by
    intro j i
    have h := oneW_eq_densW_mul shiftSet_transitive (refW_invariant p _)
      (barW_invariant p u γ r j.1) (by rw [hbarm j]; exact hEpos.ne') i
    rw [hbard j, hbarm j] at h
    exact h
  have hw₁ : ∀ j : Tk ι k, InCone u (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) := by
    intro j
    have h := (baseW_add_barW_inCone hp0 hp1 hu hγ r j.1).add_smul
      (baseW_inCone (ι := ι) hp0 hp1 hγ₂u) hb0
    have e : (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) =
        fun x => baseW p γ x + barW p u γ r j.1 x + b * baseW p γ₂ x := by
      funext x
      ring
    rw [e]
    exact h
  have hm1 : ∀ j : Tk ι k, massW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) = 1 + b + E := by
    intro j
    rw [massW_add (refW p) (fun x => baseW p γ x + b * baseW p γ₂ x) (barW p u γ r j.1), hm0,
      hbarm j]
  have hm1pos : 0 < 1 + b + E := by linarith
  have hmarg1 : ∀ (j : Tk ι k) (i : ι), margW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) i = c := by
    intro j i
    have ho1 : oneW (refW p) (fun x : ι → Bool =>
        baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x) i = c * (1 + b + E) := by
      rw [oneW_add (refW p) (fun x => baseW p γ x + b * baseW p γ₂ x) (barW p u γ r j.1),
        ho0 i, hbaro j i]
      ring
    unfold margW
    rw [ho1, hm1 j, mul_div_assoc, div_self hm1pos.ne', mul_one]
  -- the gap
  have hgap : ∀ j : Tk ι k, ε < Real.log (massW (refW p) (fun x : ι → Bool =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x)) -
      Real.log (massW (refW p) (fun x : ι → Bool => baseW p γ x + b * baseW p γ₂ x)) := by
    intro j
    rw [hm1 j, hm0, ← Real.log_div hm1pos.ne' hb1.ne']
    have hβ1 : 0 < betaA p u r k (Fintype.card ι) := by linarith
    have h1 : (Real.exp r - 1) / betaA p u r k (Fintype.card ι) * (1 + b) ≤ E := by
      calc (Real.exp r - 1) / betaA p u r k (Fintype.card ι) * (1 + b)
          ≤ (Real.exp r - 1) / betaA p u r k (Fintype.card ι) *
            betaA p u r k (Fintype.card ι) :=
            mul_le_mul_of_nonneg_left hbβ (div_nonneg hR1.le hβ1.le)
        _ = Real.exp r - 1 := div_mul_cancel₀ _ hβ1.ne'
        _ ≤ E := hE1
    refine lt_of_lt_of_le hε (Real.log_le_log
      (add_pos_of_pos_of_nonneg one_pos (div_nonneg hR1.le hβ1.le)) ?_)
    rw [le_div_iff₀ hb1]
    linarith
  -- the counting bound
  have hTpos : 0 < (univ.filter fun s : ι → Bool => wt s = k).card :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀⟩⟩
  have hTR : (0 : ℝ) < ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ) := by
    exact_mod_cast hTpos
  have hJcard : (Fintype.card (Tk ι k) : ℝ) =
      ((univ.filter fun s : ι → Bool => wt s = k).card : ℝ) := by
    rw [Fintype.card_subtype]
  have hcap : ∀ x : ι → Bool, ((univ.filter fun j : Tk ι k =>
      baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
        baseW p γ x + b * baseW p γ₂ x).card : ℝ) ≤
      (Fintype.card ι : ℝ) * (Hkr ι p u γ r k * (Fintype.card (Tk ι k) : ℝ)) := by
    intro x
    have h1 : (univ.filter fun j : Tk ι k =>
        baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
          baseW p γ x + b * baseW p γ₂ x) ⊆
        univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0 := by
      intro j hj
      rw [Finset.mem_filter] at hj ⊢
      refine ⟨hj.1, fun h0 => hj.2 ?_⟩
      rw [h0, add_zero]
    have h2 := card_barW_ne_zero_le p u γ r k x
    have h3 : (univ.filter fun j : Tk ι k => dipW p u γ r j.1 x ≠ 0).card =
        dipCount p u γ r k x := by
      unfold dipCount
      rw [← card_filter_subtype (fun s : ι → Bool => wt s = k)
        (fun s => 0 < dipW p u γ r s x)]
      congr 1
      refine Finset.filter_congr fun j _ => ?_
      exact ⟨fun h => lt_of_le_of_ne (dipW_nonneg p u γ r j.1 x) (Ne.symm h), fun h => h.ne'⟩
    have h4 : dipCount p u γ r k x ≤
        univ.sup' univ_nonempty (fun x : ι → Bool => dipCount p u γ r k x) :=
      Finset.le_sup' (fun x : ι → Bool => dipCount p u γ r k x) (Finset.mem_univ x)
    have h5 : Hkr ι p u γ r k * (Fintype.card (Tk ι k) : ℝ) =
        ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) := by
      unfold Hkr
      rw [hJcard]
      exact div_mul_cancel₀ _ hTR.ne'
    rw [h5]
    calc ((univ.filter fun j : Tk ι k =>
          baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x ≠
            baseW p γ x + b * baseW p γ₂ x).card : ℝ)
        ≤ ((univ.filter fun j : Tk ι k => barW p u γ r j.1 x ≠ 0).card : ℝ) := by
          exact_mod_cast Finset.card_le_card h1
      _ ≤ ((Fintype.card ι * (univ.filter fun j : Tk ι k =>
            dipW p u γ r j.1 x ≠ 0).card : ℕ) : ℝ) := by
          exact_mod_cast h2
      _ = (Fintype.card ι : ℝ) * (dipCount p u γ r k x : ℝ) := by
          rw [h3]
          push_cast
          ring
      _ ≤ (Fintype.card ι : ℝ) *
            ((univ.sup' univ_nonempty fun x : ι → Bool => dipCount p u γ r k x : ℕ) : ℝ) := by
          refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg _)
          exact_mod_cast h4
  -- Lemma 1 (a)
  have key := oracle_packing_weights alg P hP hP1 hcorr hw₀ hmarg0
    (fun (j : Tk ι k) (x : ι → Bool) => baseW p γ x + b * baseW p γ₂ x + barW p u γ r j.1 x)
    hw₁ hmarg1 hgap hcap
  have hJpos : (0 : ℝ) < (Fintype.card (Tk ι k) : ℝ) := by
    rw [hJcard]
    exact hTR
  have key' : (1 - 2 * δ) * (Fintype.card (Tk ι k) : ℝ) ≤
      (∑ ω, P ω * (((alg ω (oracle1 (refW p)
          fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
          fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
        ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) * (Fintype.card (Tk ι k) : ℝ) := by
    refine le_trans key (le_of_eq ?_)
    ring
  exact le_of_mul_le_mul_right key' hJpos

open Classical in
/-- **Theorem A (every `n`; adaptive algorithms with an exact one-body oracle), with the
constants of the report**: `b ∈ [0, β]` and `ε < ln(1 + (e^r − 1)/(1 + β))`;
`1 − 2δ ≤ E[#evaluations on ψ₀] · n · H_{k,r}`.  A consequence of `theoremA_group_sharp`. -/
theorem theoremA_group {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u) (hr : 0 < r)
    {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) := by
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ :=
    theoremA_group_sharp (ι := ι) hp0 hp1 hγ hr hk hcond
  refine ⟨γ₂, hγ₂, b, hb0, by linarith, hlip, fun Ω _ alg P hP hP1 ε δ hε hcorr => ?_⟩
  have hR1 : 0 < Real.exp r - 1 := by
    have h' := Real.one_lt_exp_iff.mpr hr
    linarith
  have hβ : 0 < betaA p u r k (Fintype.card ι) := by linarith
  refine h Ω alg P hP hP1 ε δ (lt_of_lt_of_le hε (Real.log_le_log ?_ ?_)) hcorr
  · exact add_pos_of_pos_of_nonneg one_pos (div_nonneg hR1.le (by linarith))
  · have h2 : (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι)) ≤
        (Real.exp r - 1) / betaA p u r k (Fintype.card ι) :=
      div_le_div_of_nonneg_left hR1.le hβ (by linarith)
    linarith

omit [AddGroup ι] in
/-- `H_{k,r} > 0`: since `E_{k,r} ≥ e^r − 1 > 0`, some point lies in some dip. -/
theorem Hkr_pos {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hr : 0 < r) {k : ℕ}
    (hk : k ≤ Fintype.card ι) : 0 < Hkr ι p u γ r k := by
  obtain ⟨s₀, hs₀⟩ := exists_wt_eq (ι := ι) hk
  have hR1 : 0 < Real.exp r - 1 := by
    have h := Real.one_lt_exp_iff.mpr hr
    linarith
  have hmass : 0 < massW (refW p) (dipW p u γ r s₀) :=
    lt_of_lt_of_le hR1 (lemma2_mass hp0 hp1 u γ r s₀).1
  obtain ⟨x, hx⟩ : ∃ x, dipW p u γ r s₀ x ≠ 0 := by
    by_contra hno
    have hz : massW (refW p) (dipW p u γ r s₀) = 0 := by
      unfold massW
      exact Finset.sum_eq_zero fun x _ => by
        rw [not_not.mp fun h' => hno ⟨x, h'⟩, mul_zero]
    linarith
  have hxpos : 0 < dipW p u γ r s₀ x :=
    lt_of_le_of_ne (dipW_nonneg p u γ r s₀ x) (Ne.symm hx)
  have h1 : 0 < dipCount p u γ r k x :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀, hxpos⟩⟩
  have h2 : dipCount p u γ r k x ≤
      univ.sup' univ_nonempty (fun x : ι → Bool => dipCount p u γ r k x) :=
    Finset.le_sup' (fun x : ι → Bool => dipCount p u γ r k x) (Finset.mem_univ x)
  have h3 : 0 < (univ.filter fun s : ι → Bool => wt s = k).card :=
    Finset.card_pos.mpr ⟨s₀, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hs₀⟩⟩
  unfold Hkr
  exact div_pos (by exact_mod_cast lt_of_lt_of_le h1 h2) (by exact_mod_cast h3)

open Classical in
/-- **Theorem A, as displayed in the report:**
`E|Q(ψ₀)| ≥ (1 − 2δ)/(n · H_{k,r})`. -/
theorem theoremA_group_div {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u)
    (hr : 0 < r) {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        (1 - 2 * δ) / ((Fintype.card ι : ℝ) * Hkr ι p u γ r k) ≤
          ∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) := by
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ := theoremA_group (ι := ι) hp0 hp1 hγ hr hk hcond
  refine ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, fun Ω _ alg P hP hP1 ε δ hε hcorr => ?_⟩
  have hnpos : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0
  rw [div_le_iff₀ (mul_pos hnpos (Hkr_pos hp0 hp1 hr hk))]
  exact h Ω alg P hP hP1 ε δ hε hcorr

open Classical in
/-- **Theorem A on `{0,1}ⁿ` with the cyclic shifts** (the statement of the report):
`X = Fin n → Bool`, `π = Bernoulli(p)^{⊗n}`; the translations of `Fin n` are the cyclic shifts
`i ↦ i + a mod n`.  There are `γ₂ ∈ {−u, +u}` and `b ∈ [0, β]` such that `ψ₀ = −ln(w̃_γ + b·w̃_{γ₂})`
is in `L_u` and every `(ε/2, δ)`-correct oracle algorithm, `ε < ln(1 + (e^r − 1)/(1 + β))`, makes
at least `(1 − 2δ)/(n · H_{k,r})` evaluations on `ψ₀` in expectation. -/
theorem theoremA_fin {n : ℕ} [NeZero n] {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    (hγ : |γ| ≤ u) (hr : 0 < r) {k : ℕ} (hk : k ≤ n)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k n) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k n ∧
      LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k n)) →
        (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        (1 - 2 * δ) / ((n : ℝ) * Hkr (Fin n) p u γ r k) ≤
          ∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) := by
  have hk' : k ≤ Fintype.card (Fin n) := by
    rw [Fintype.card_fin]
    exact hk
  have hcond' : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card (Fin n)) := by
    rw [Fintype.card_fin]
    exact hcond
  have h := theoremA_group_div (ι := Fin n) (γ := γ) hp0 hp1 hγ hr hk' hcond'
  rw [Fintype.card_fin] at h
  exact h

/-! # Part 10: the Chernoff form of Theorem A, `H_{k,r} ≤ (n+1)·e^{tr}·ρ_t(k/n; γ)ⁿ` -/

/-- The binomial weights `C(n,j) m^j (1 − m)^{n−j}`. -/
def binomPmf (n : ℕ) (m : ℝ) (j : ℕ) : ℝ := (n.choose j : ℝ) * m ^ j * (1 - m) ^ (n - j)

theorem binomPmf_nonneg (n : ℕ) {m : ℝ} (hm0 : 0 ≤ m) (hm1 : m ≤ 1) (j : ℕ) :
    0 ≤ binomPmf n m j :=
  mul_nonneg (mul_nonneg (Nat.cast_nonneg _) (pow_nonneg hm0 _)) (pow_nonneg (by linarith) _)

theorem sum_binomPmf (n : ℕ) (m : ℝ) : ∑ j ∈ Finset.range (n + 1), binomPmf n m j = 1 := by
  have h := add_pow m (1 - m) n
  rw [add_sub_cancel, one_pow] at h
  rw [h]
  exact Finset.sum_congr rfl fun j _ => by
    unfold binomPmf
    ring

/-- The ratio of consecutive binomial weights, cross-multiplied. -/
theorem binomPmf_step {n : ℕ} (m : ℝ) {j : ℕ} (hj : j < n) :
    binomPmf n m (j + 1) * (((j : ℝ) + 1) * (1 - m)) = binomPmf n m j * (((n : ℝ) - j) * m) := by
  have h1 : (n.choose (j + 1) : ℝ) * ((j : ℝ) + 1) = (n.choose j : ℝ) * ((n : ℝ) - j) := by
    have h := Nat.choose_succ_right_eq n j
    have h' : ((n.choose (j + 1) * (j + 1) : ℕ) : ℝ) = ((n.choose j * (n - j) : ℕ) : ℝ) := by
      rw [h]
    push_cast [Nat.cast_sub hj.le] at h'
    exact h'
  have h2 : n - j = n - (j + 1) + 1 := by omega
  unfold binomPmf
  rw [h2, pow_succ, pow_succ]
  linear_combination (m ^ j * m * (1 - m) ^ (n - (j + 1)) * (1 - m)) * h1

/-- For `m = k/n`, `0 < k < n`, the binomial weights increase up to `j = k` … -/
theorem binomPmf_le_succ {n k : ℕ} (hk0 : 0 < k) (hkn : k < n) {j : ℕ} (hj : j + 1 ≤ k) :
    binomPmf n ((k : ℝ) / n) j ≤ binomPmf n ((k : ℝ) / n) (j + 1) := by
  have hn : (0 : ℝ) < n := by exact_mod_cast lt_trans hk0 hkn
  have hkR : (k : ℝ) < n := by exact_mod_cast hkn
  have hjR : (j : ℝ) + 1 ≤ k := by exact_mod_cast hj
  have hm0 : 0 ≤ (k : ℝ) / n := div_nonneg (Nat.cast_nonneg _) hn.le
  have hm1 : (k : ℝ) / n < 1 := (div_lt_one hn).mpr hkR
  have hstep := binomPmf_step ((k : ℝ) / n) (lt_of_lt_of_le (Nat.lt_succ_self j) (hj.trans hkn.le))
  have hc : ((j : ℝ) + 1) * (1 - (k : ℝ) / n) ≤ ((n : ℝ) - j) * ((k : ℝ) / n) := by
    rw [← sub_nonneg]
    have e : ((n : ℝ) - j) * ((k : ℝ) / n) - ((j : ℝ) + 1) * (1 - (k : ℝ) / n) =
        ((n : ℝ) * ((k : ℝ) - j - 1) + k) / n := by
      field_simp
      ring
    rw [e]
    exact div_nonneg (add_nonneg (mul_nonneg hn.le (by linarith)) (Nat.cast_nonneg _)) hn.le
  have hpos : 0 < ((j : ℝ) + 1) * (1 - (k : ℝ) / n) :=
    mul_pos (by positivity) (by linarith)
  have hb := binomPmf_nonneg n hm0 hm1.le j
  have h3 : binomPmf n ((k : ℝ) / n) j * (((j : ℝ) + 1) * (1 - (k : ℝ) / n)) ≤
      binomPmf n ((k : ℝ) / n) (j + 1) * (((j : ℝ) + 1) * (1 - (k : ℝ) / n)) := by
    rw [hstep]
    exact mul_le_mul_of_nonneg_left hc hb
  exact le_of_mul_le_mul_right h3 hpos

/-- … and decrease from `j = k` on. -/
theorem binomPmf_succ_le {n k : ℕ} (hk0 : 0 < k) (hkn : k < n) {j : ℕ} (hkj : k ≤ j)
    (hj : j < n) : binomPmf n ((k : ℝ) / n) (j + 1) ≤ binomPmf n ((k : ℝ) / n) j := by
  have hn : (0 : ℝ) < n := by exact_mod_cast lt_trans hk0 hkn
  have hkR : (k : ℝ) < n := by exact_mod_cast hkn
  have hjR : (k : ℝ) ≤ j := by exact_mod_cast hkj
  have hm0 : 0 ≤ (k : ℝ) / n := div_nonneg (Nat.cast_nonneg _) hn.le
  have hm1 : (k : ℝ) / n < 1 := (div_lt_one hn).mpr hkR
  have hstep := binomPmf_step ((k : ℝ) / n) hj
  have hc : ((n : ℝ) - j) * ((k : ℝ) / n) ≤ ((j : ℝ) + 1) * (1 - (k : ℝ) / n) := by
    rw [← sub_nonneg]
    have e : ((j : ℝ) + 1) * (1 - (k : ℝ) / n) - ((n : ℝ) - j) * ((k : ℝ) / n) =
        ((n : ℝ) * ((j : ℝ) + 1 - k) - k) / n := by
      field_simp
      ring
    rw [e]
    refine div_nonneg ?_ hn.le
    nlinarith
  have hpos : 0 < ((j : ℝ) + 1) * (1 - (k : ℝ) / n) :=
    mul_pos (by positivity) (by linarith)
  have hb := binomPmf_nonneg n hm0 hm1.le j
  have h3 : binomPmf n ((k : ℝ) / n) (j + 1) * (((j : ℝ) + 1) * (1 - (k : ℝ) / n)) ≤
      binomPmf n ((k : ℝ) / n) j * (((j : ℝ) + 1) * (1 - (k : ℝ) / n)) := by
    rw [hstep]
    exact mul_le_mul_of_nonneg_left hc hb
  exact le_of_mul_le_mul_right h3 hpos

/-- **The binomial weights with parameter `k/n` are largest at `j = k`.** -/
theorem binomPmf_le_mode {n k : ℕ} (hk0 : 0 < k) (hkn : k < n) {j : ℕ} (hj : j ≤ n) :
    binomPmf n ((k : ℝ) / n) j ≤ binomPmf n ((k : ℝ) / n) k := by
  have hup : ∀ d : ℕ, d ≤ k →
      binomPmf n ((k : ℝ) / n) (k - d) ≤ binomPmf n ((k : ℝ) / n) k := by
    intro d
    induction d with
    | zero =>
      intro _
      exact le_rfl
    | succ d ih =>
      intro hd
      have h1 := ih (by omega)
      have h2 := binomPmf_le_succ hk0 hkn (j := k - (d + 1)) (by omega)
      have e : k - (d + 1) + 1 = k - d := by omega
      rw [e] at h2
      exact h2.trans h1
  have hdown : ∀ d : ℕ, k + d ≤ n →
      binomPmf n ((k : ℝ) / n) (k + d) ≤ binomPmf n ((k : ℝ) / n) k := by
    intro d
    induction d with
    | zero =>
      intro _
      exact le_rfl
    | succ d ih =>
      intro hd
      have h1 := ih (by omega)
      have h2 := binomPmf_succ_le hk0 hkn (j := k + d) (by omega) (by omega)
      exact h2.trans h1
  rcases le_total j k with h | h
  · have h1 := hup (k - j) (by omega)
    have e : k - (k - j) = j := by omega
    rw [e] at h1
    exact h1
  · have h1 := hdown (j - k) (by omega)
    have e : k + (j - k) = j := by omega
    rw [e] at h1
    exact h1

/-- **`Unif(T_k)` is `Bern(k/n)^{⊗n}` conditioned on an event of probability `≥ 1/(n+1)`:**
`1 ≤ (n + 1)·C(n,k)·(k/n)^k·(1 − k/n)^{n−k}` for `0 < k < n`. -/
theorem binomial_mode_bound {n k : ℕ} (hk0 : 0 < k) (hkn : k < n) :
    1 ≤ ((n : ℝ) + 1) * binomPmf n ((k : ℝ) / n) k := by
  have h := sum_binomPmf n ((k : ℝ) / n)
  have h2 : ∑ j ∈ Finset.range (n + 1), binomPmf n ((k : ℝ) / n) j ≤
      ∑ _j ∈ Finset.range (n + 1), binomPmf n ((k : ℝ) / n) k :=
    Finset.sum_le_sum fun j hj =>
      binomPmf_le_mode hk0 hkn (Nat.lt_succ_iff.mp (Finset.mem_range.mp hj))
  rw [h, Finset.sum_const, Finset.card_range, nsmul_eq_mul] at h2
  push_cast at h2
  exact h2

omit [AddGroup ι] in
/-- `|T_j| = C(n, j)`. -/
theorem card_wt_eq (j : ℕ) :
    (univ.filter fun s : ι → Bool => wt s = j).card = (Fintype.card ι).choose j := by
  rw [← Finset.card_univ (α := ι), ← Finset.card_powersetCard j (univ : Finset ι)]
  refine Finset.card_bij (fun s _ => univ.filter fun i => s i = true) ?_ ?_ ?_
  · intro s hs
    rw [Finset.mem_powersetCard]
    exact ⟨Finset.subset_univ _, (Finset.mem_filter.mp hs).2⟩
  · intro s₁ _ s₂ _ h
    funext i
    have h' : (i ∈ univ.filter fun i => s₁ i = true) ↔ (i ∈ univ.filter fun i => s₂ i = true) := by
      rw [h]
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at h'
    exact Bool.eq_iff_iff.mpr h'
  · intro t ht
    refine ⟨fun i => decide (i ∈ t), ?_, ?_⟩
    · rw [Finset.mem_filter]
      refine ⟨Finset.mem_univ _, ?_⟩
      unfold wt
      rw [← (Finset.mem_powersetCard.mp ht).2]
      congr 1
      ext i
      simp
    · ext i
      simp

omit [DecidableEq ι] [AddGroup ι] in
/-- `Bern(m)^{⊗n}(s) = m^{|s|}(1 − m)^{n−|s|}`. -/
theorem refW_eq_pow (m : ℝ) (s : ι → Bool) :
    refW m s = m ^ wt s * (1 - m) ^ (Fintype.card ι - wt s) := by
  have h : ∀ i, bernW m (s i) = if s i = true then m else 1 - m := by
    intro i
    cases s i <;> rfl
  have hc := Finset.card_filter_add_card_filter_not (s := (univ : Finset ι))
    (fun i => s i = true)
  rw [Finset.card_univ] at hc
  have e : (univ.filter fun i => ¬s i = true).card = Fintype.card ι - wt s := by
    unfold wt
    omega
  show ∏ i, bernW m (s i) = _
  rw [Finset.prod_congr rfl fun i _ => h i, Finset.prod_ite, Finset.prod_const,
    Finset.prod_const, e]
  rfl

omit [DecidableEq ι] [AddGroup ι] in
theorem refW_nonneg {m : ℝ} (hm0 : 0 ≤ m) (hm1 : m ≤ 1) (s : ι → Bool) : 0 ≤ refW m s := by
  refine Finset.prod_nonneg fun i _ => ?_
  cases s i
  · show 0 ≤ 1 - m
    linarith
  · exact hm0

theorem siteLaw_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (γ : ℝ) (a : Bool) :
    0 < siteLaw p γ a := by
  have hZ := tiltZ_pos hp0 hp1 γ
  cases a
  · exact div_pos (by linarith) hZ
  · exact div_pos (mul_pos hp0 (Real.exp_pos _)) hZ

/-- The likelihood ratio of one site: `π_b(a)/π_γ(a)`, with `π_0 = Bern(p₋)` (`b = false`) and
`π_1 = Bern(p₊)` (`b = true`) the two letters of the vertex channel. -/
def ratioS (p u γ : ℝ) (b a : Bool) : ℝ :=
  siteLaw p (if b = true then -u else u) a / siteLaw p γ a

theorem ratioS_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ : ℝ) (b a : Bool) :
    0 < ratioS p u γ b a :=
  div_pos (siteLaw_pos hp0 hp1 _ a) (siteLaw_pos hp0 hp1 γ a)

/-- **`ρ_t(m; γ) = max_{a ∈ {0,1}} [(1 − m)(π_0(a)/π_γ(a))^t + m(π_1(a)/π_γ(a))^t]`**
(real powers). -/
def rhoT (p u γ t m : ℝ) : ℝ :=
  max ((1 - m) * ratioS p u γ false true ^ t + m * ratioS p u γ true true ^ t)
    ((1 - m) * ratioS p u γ false false ^ t + m * ratioS p u γ true false ^ t)

omit [DecidableEq ι] [AddGroup ι] in
/-- **The Markov step:** if `x ∈ D_{s,r}` then `1 ≤ e^{tr} ∏_i (π_{s_i}(x_i)/π_γ(x_i))^t`, `t ≥ 0`. -/
theorem one_le_of_dipW_pos {p u γ r t : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (ht : 0 ≤ t)
    {s x : ι → Bool} (h : 0 < dipW p u γ r s x) :
    1 ≤ Real.exp (t * r) * ∏ i, ratioS p u γ (s i) (x i) ^ t := by
  rw [dipW_pos_iff hp0 hp1] at h
  have e1 : refW p x * baseW p γ x = ∏ i, siteLaw p γ (x i) :=
    refW_mul_tiltW p (fun _ => γ) x
  have e2 : refW p x * coneW p u s x = ∏ i, siteLaw p (coneField u s i) (x i) :=
    refW_mul_tiltW p (coneField u s) x
  rw [e1, e2] at h
  have hpos : 0 < ∏ i, siteLaw p γ (x i) :=
    Finset.prod_pos fun i _ => siteLaw_pos hp0 hp1 γ (x i)
  have hratio : ∏ i, ratioS p u γ (s i) (x i) =
      (∏ i, siteLaw p (coneField u s i) (x i)) / ∏ i, siteLaw p γ (x i) := by
    rw [← Finset.prod_div_distrib]
    rfl
  have h1 : 1 < Real.exp r * ∏ i, ratioS p u γ (s i) (x i) := by
    rw [hratio, ← mul_div_assoc, lt_div_iff₀ hpos, one_mul]
    exact h
  have h2 := Real.one_le_rpow h1.le ht
  rw [Real.mul_rpow (Real.exp_pos r).le
      (Finset.prod_nonneg fun i _ => (ratioS_pos hp0 hp1 u γ (s i) (x i)).le),
    ← Real.exp_mul, ← Real.finsetProd_rpow _ _
      (fun i _ => (ratioS_pos hp0 hp1 u γ (s i) (x i)).le), mul_comm r t] at h2
  exact h2

omit [AddGroup ι] in
/-- **The Chernoff step:** with the weights `Bern(m)^{⊗n}` on the centres,
`#{s ∈ T_k : x ∈ D_{s,r}} · m^k(1 − m)^{n−k} ≤ e^{tr} ρ_t(m; γ)ⁿ` for `t ≥ 0`, `0 ≤ m ≤ 1`. -/
theorem dipCount_mul_le {p u γ r t m : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (ht : 0 ≤ t)
    (hm0 : 0 ≤ m) (hm1 : m ≤ 1) (k : ℕ) (x : ι → Bool) :
    (dipCount p u γ r k x : ℝ) * (m ^ k * (1 - m) ^ (Fintype.card ι - k)) ≤
      Real.exp (t * r) * rhoT p u γ t m ^ Fintype.card ι := by
  have hS : ∑ s : ι → Bool, refW m s * ∏ i, ratioS p u γ (s i) (x i) ^ t =
      ∏ i, (m * ratioS p u γ true (x i) ^ t + (1 - m) * ratioS p u γ false (x i) ^ t) := by
    have h1 : ∀ s : ι → Bool, refW m s * ∏ i, ratioS p u γ (s i) (x i) ^ t =
        prodW (fun i b => bernW m b * ratioS p u γ b (x i) ^ t) s := by
      intro s
      show (∏ i, bernW m (s i)) * ∏ i, ratioS p u γ (s i) (x i) ^ t =
        ∏ i, bernW m (s i) * ratioS p u γ (s i) (x i) ^ t
      rw [Finset.prod_mul_distrib]
    rw [Finset.sum_congr rfl fun s _ => h1 s, sum_prodW]
    rfl
  have hfac : ∀ i, m * ratioS p u γ true (x i) ^ t + (1 - m) * ratioS p u γ false (x i) ^ t ≤
      rhoT p u γ t m := by
    intro i
    unfold rhoT
    cases x i
    · exact le_trans (le_of_eq (add_comm _ _)) (le_max_right _ _)
    · exact le_trans (le_of_eq (add_comm _ _)) (le_max_left _ _)
  have hfac0 : ∀ i, 0 ≤ m * ratioS p u γ true (x i) ^ t +
      (1 - m) * ratioS p u γ false (x i) ^ t := fun i =>
    add_nonneg (mul_nonneg hm0 (Real.rpow_nonneg (ratioS_pos hp0 hp1 u γ true (x i)).le t))
      (mul_nonneg (by linarith) (Real.rpow_nonneg (ratioS_pos hp0 hp1 u γ false (x i)).le t))
  have hprod : ∏ i, (m * ratioS p u γ true (x i) ^ t + (1 - m) * ratioS p u γ false (x i) ^ t) ≤
      rhoT p u γ t m ^ Fintype.card ι := by
    calc ∏ i, (m * ratioS p u γ true (x i) ^ t + (1 - m) * ratioS p u γ false (x i) ^ t)
        ≤ ∏ _i : ι, rhoT p u γ t m :=
          Finset.prod_le_prod (fun i _ => hfac0 i) (fun i _ => hfac i)
      _ = rhoT p u γ t m ^ Fintype.card ι := by rw [Finset.prod_const, Finset.card_univ]
  have hL : (dipCount p u γ r k x : ℝ) * (m ^ k * (1 - m) ^ (Fintype.card ι - k)) =
      ∑ s ∈ univ.filter (fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x), refW m s := by
    have hterm : ∀ s ∈ univ.filter (fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x),
        refW m s = m ^ k * (1 - m) ^ (Fintype.card ι - k) := by
      intro s hs
      rw [refW_eq_pow, (Finset.mem_filter.mp hs).2.1]
    rw [Finset.sum_congr rfl hterm, Finset.sum_const, nsmul_eq_mul]
    rfl
  rw [hL]
  calc ∑ s ∈ univ.filter (fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x), refW m s
      ≤ ∑ s ∈ univ.filter (fun s : ι → Bool => wt s = k ∧ 0 < dipW p u γ r s x),
          refW m s * (Real.exp (t * r) * ∏ i, ratioS p u γ (s i) (x i) ^ t) :=
        Finset.sum_le_sum fun s hs =>
          le_mul_of_one_le_right (refW_nonneg hm0 hm1 s)
            (one_le_of_dipW_pos hp0 hp1 ht (Finset.mem_filter.mp hs).2.2)
    _ ≤ ∑ s : ι → Bool, refW m s * (Real.exp (t * r) * ∏ i, ratioS p u γ (s i) (x i) ^ t) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _) fun s _ _ =>
          mul_nonneg (refW_nonneg hm0 hm1 s) (mul_nonneg (Real.exp_pos _).le
            (Finset.prod_nonneg fun i _ =>
              Real.rpow_nonneg (ratioS_pos hp0 hp1 u γ (s i) (x i)).le t))
    _ = Real.exp (t * r) * ∑ s : ι → Bool, refW m s * ∏ i, ratioS p u γ (s i) (x i) ^ t := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun s _ => by ring
    _ = Real.exp (t * r) *
          ∏ i, (m * ratioS p u γ true (x i) ^ t + (1 - m) * ratioS p u γ false (x i) ^ t) := by
        rw [hS]
    _ ≤ Real.exp (t * r) * rhoT p u γ t m ^ Fintype.card ι :=
        mul_le_mul_of_nonneg_left hprod (Real.exp_pos _).le

omit [AddGroup ι] in
/-- **The Chernoff bound on `H_{k,r}`** (the second inequality of Theorem A): for every `t ≥ 0`
and `0 < k < n`, `H_{k,r} ≤ (n + 1)·e^{tr}·ρ_t(k/n; γ)ⁿ`. -/
theorem Hkr_le_chernoff {p u γ r t : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (ht : 0 ≤ t) {k : ℕ}
    (hk0 : 0 < k) (hkn : k < Fintype.card ι) :
    Hkr ι p u γ r k ≤ ((Fintype.card ι : ℝ) + 1) *
      (Real.exp (t * r) * rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι) := by
  have hn : (0 : ℝ) < Fintype.card ι := by exact_mod_cast lt_trans hk0 hkn
  have hm0 : 0 ≤ (k : ℝ) / Fintype.card ι := div_nonneg (Nat.cast_nonneg _) hn.le
  have hm1 : (k : ℝ) / Fintype.card ι ≤ 1 :=
    ((div_lt_one hn).mpr (by exact_mod_cast hkn)).le
  have hmode := binomial_mode_bound hk0 hkn
  have hC : (0 : ℝ) < (Fintype.card ι).choose k := by exact_mod_cast Nat.choose_pos hkn.le
  obtain ⟨x, _, hx⟩ := Finset.exists_mem_eq_sup' (univ_nonempty (α := ι → Bool))
    (fun x : ι → Bool => dipCount p u γ r k x)
  have h1 := dipCount_mul_le (u := u) (γ := γ) (r := r) hp0 hp1 ht hm0 hm1 k x
  unfold Hkr
  rw [card_wt_eq, div_le_iff₀ hC, hx]
  unfold binomPmf at hmode
  calc (dipCount p u γ r k x : ℝ)
      ≤ (dipCount p u γ r k x : ℝ) * (((Fintype.card ι : ℝ) + 1) *
          (((Fintype.card ι).choose k : ℝ) * ((k : ℝ) / Fintype.card ι) ^ k *
            (1 - (k : ℝ) / Fintype.card ι) ^ (Fintype.card ι - k))) :=
        le_mul_of_one_le_right (Nat.cast_nonneg _) hmode
    _ = ((Fintype.card ι : ℝ) + 1) * ((Fintype.card ι).choose k : ℝ) *
          ((dipCount p u γ r k x : ℝ) * (((k : ℝ) / Fintype.card ι) ^ k *
            (1 - (k : ℝ) / Fintype.card ι) ^ (Fintype.card ι - k))) := by ring
    _ ≤ ((Fintype.card ι : ℝ) + 1) * ((Fintype.card ι).choose k : ℝ) *
          (Real.exp (t * r) *
            rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι) :=
        mul_le_mul_of_nonneg_left h1 (mul_nonneg (by linarith) hC.le)
    _ = ((Fintype.card ι : ℝ) + 1) * (Real.exp (t * r) *
          rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι) *
            ((Fintype.card ι).choose k : ℝ) := by ring

open Classical in
/-- **Theorem A, both displays (every `n`; any finite group of sites):** in the situation of
`theoremA_group`, for every `t ≥ 0`,

    1 − 2δ ≤ E[#evaluations on ψ₀] · n · (n + 1) · e^{tr} · ρ_t(k/n; γ)ⁿ,

i.e. `E|Q(ψ₀)| ≥ (1 − 2δ)·e^{−tr}·ρ_t(k/n; γ)^{−n}/(n(n + 1))`. -/
theorem theoremA_group_chernoff {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hγ : |γ| ≤ u)
    (hr : 0 < r) {k : ℕ} (hk : k ≤ Fintype.card ι)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι)) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k (Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) →
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        ∀ t : ℝ, 0 ≤ t →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * (((Fintype.card ι : ℝ) + 1) *
              (Real.exp (t * r) *
                rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι))) := by
  -- `0 < k < n` follows from the hypotheses
  have hu : 0 ≤ u := (abs_nonneg γ).trans hγ
  have hR1 : 0 < Real.exp r - 1 := by
    have h := Real.one_lt_exp_iff.mpr hr
    linarith
  have hω0 : 0 ≤ omegaW p u := by
    unfold omegaW
    linarith [pTilt_anti hp0 hp1 (by linarith : -u ≤ u)]
  have hωm : 0 < omegaM p u k (Fintype.card ι) := by
    by_contra h
    have h1 := mul_nonpos_of_nonneg_of_nonpos hR1.le (not_lt.mp h)
    linarith
  have hmin : 0 < min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) := by
    by_contra h
    have h1 := mul_nonpos_of_nonneg_of_nonpos hω0 (not_lt.mp h)
    unfold omegaM at hωm
    linarith
  have hn : (0 : ℝ) < Fintype.card ι := by
    have h0 : 0 < Fintype.card ι := Fintype.card_pos_iff.mpr ⟨0⟩
    exact_mod_cast h0
  have hk0 : 0 < k := by
    have h1 : 0 < (k : ℝ) / Fintype.card ι := lt_of_lt_of_le hmin (min_le_left _ _)
    have h2 : (0 : ℝ) < k := by
      by_contra h
      have h3 := div_nonpos_of_nonpos_of_nonneg (not_lt.mp h) hn.le
      linarith
    exact_mod_cast h2
  have hkn : k < Fintype.card ι := by
    have h1 : 0 < 1 - (k : ℝ) / Fintype.card ι := lt_of_lt_of_le hmin (min_le_right _ _)
    have h2 : (k : ℝ) / Fintype.card ι < 1 := by linarith
    rw [div_lt_one hn] at h2
    exact_mod_cast h2
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ := theoremA_group (ι := ι) hp0 hp1 hγ hr hk hcond
  refine ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, fun Ω _ alg P hP hP1 ε δ hε hcorr t ht => ?_⟩
  have h1 := h Ω alg P hP hP1 ε δ hε hcorr
  have hH := Hkr_le_chernoff (ι := ι) (u := u) (γ := γ) (r := r) hp0 hp1 ht hk0 hkn
  have hEQ : 0 ≤ ∑ ω, P ω * (((alg ω (oracle1 (refW p)
      fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
      fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) :=
    Finset.sum_nonneg fun ω _ => mul_nonneg (hP ω) (Nat.cast_nonneg _)
  exact h1.trans (mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hH hn.le) hEQ)

open Classical in
/-- **Theorem A on `{0,1}ⁿ` with the cyclic shifts, the Chernoff form:** for every `t ≥ 0`,
`1 − 2δ ≤ E|Q(ψ₀)| · n(n + 1) · e^{tr} · ρ_t(k/n; γ)ⁿ`. -/
theorem theoremA_fin_chernoff {n : ℕ} [NeZero n] {p u γ r : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    (hγ : |γ| ≤ u) (hr : 0 < r) {k : ℕ} (hk : k ≤ n)
    (hcond : 1 < (Real.exp r - 1) * omegaM p u k n) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧ b ≤ betaA p u r k n ∧
      LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ ε δ : ℝ,
        ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k n)) →
        (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        ∀ t : ℝ, 0 ≤ t →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((n : ℝ) * (((n : ℝ) + 1) *
              (Real.exp (t * r) * rhoT p u γ t ((k : ℝ) / n) ^ n))) := by
  have hk' : k ≤ Fintype.card (Fin n) := by
    rw [Fintype.card_fin]
    exact hk
  have hcond' : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card (Fin n)) := by
    rw [Fintype.card_fin]
    exact hcond
  have h := theoremA_group_chernoff (ι := Fin n) (γ := γ) hp0 hp1 hγ hr hk' hcond'
  rw [Fintype.card_fin] at h
  exact h

/-! # Part 11: the last display of Theorem A (the constant `C_m`) -/

/-- `C_m = 1 + 2/m̲ + 2/ω_m`, `m̲ = min(k/n, 1 − k/n)`. -/
def CmA (p u : ℝ) (k n : ℕ) : ℝ :=
  1 + 2 / min ((k : ℝ) / n) (1 - (k : ℝ) / n) + 2 / omegaM p u k n

theorem rhoT_nonneg {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (u γ t : ℝ) {m : ℝ} (hm0 : 0 ≤ m)
    (hm1 : m ≤ 1) : 0 ≤ rhoT p u γ t m :=
  le_max_of_le_left (add_nonneg
    (mul_nonneg (by linarith) (Real.rpow_nonneg (ratioS_pos hp0 hp1 u γ false true).le t))
    (mul_nonneg hm0 (Real.rpow_nonneg (ratioS_pos hp0 hp1 u γ true true).le t)))

open Classical in
/-- **Theorem A, the last display (every `n`; any finite group of sites).**  `0 < p < 1`,
`u > 0`, `|γ| ≤ u`, `ε ≥ 0`, `0 < k < n`.  With the depth `r = ln C_m + ε` there are
`γ₂ ∈ {−u, +u}` and `b ∈ [0, 2/m̲]` such that `ψ₀ = −ln(w̃_γ + b·w̃_{γ₂}) ∈ L_u` and every
`(ε/2, δ)`-correct oracle algorithm satisfies, **for every `t ∈ [0, 1]`**,

    1 − 2δ ≤ E|Q(ψ₀)| · n(n + 1) · C_m · e^{tε} · ρ_t(k/n; γ)ⁿ,

i.e. `E|Q(ψ₀)| ≥ (1 − 2δ)·e^{−tε}·ρ_t(k/n; γ)^{−n}/(C_m·n(n + 1))`.  The instance does not depend
on `t`.  (The report takes `r = ln(1 + max{2/ω_m, (1 + 2/m̲)(e^ε − 1)}) + η`, `η ↓ 0`; the fixed
choice `e^r = C_m e^ε` gives the stated bound at one instance.) -/
theorem theoremA_group_Cm {p u γ ε : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hu : 0 < u)
    (hγ : |γ| ≤ u) (hε : 0 ≤ ε) {k : ℕ} (hk0 : 0 < k) (hkn : k < Fintype.card ι) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧
      b ≤ 2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) ∧
      LipH u (fun x : ι → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (ι → ℝ) → MetricChain.QueryAlgorithm (ι → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ δ : ℝ,
        (∀ ψ : (ι → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        ∀ t : ℝ, 0 ≤ t → t ≤ 1 →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((Fintype.card ι : ℝ) * (((Fintype.card ι : ℝ) + 1) *
              (CmA p u k (Fintype.card ι) * (Real.exp (t * ε) *
                rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι)))) := by
  have hn : (0 : ℝ) < Fintype.card ι := by exact_mod_cast lt_trans hk0 hkn
  have hm0 : 0 < (k : ℝ) / Fintype.card ι := div_pos (by exact_mod_cast hk0) hn
  have hm1 : (k : ℝ) / Fintype.card ι < 1 := (div_lt_one hn).mpr (by exact_mod_cast hkn)
  have hmm : 0 < min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) :=
    lt_min hm0 (by linarith)
  have hω : 0 < omegaW p u := by
    unfold omegaW
    linarith [pTilt_strictAnti hp0 hp1 (by linarith : -u < u)]
  have hωm : 0 < omegaM p u k (Fintype.card ι) := mul_pos hω hmm
  have ha : 0 < 2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) :=
    div_pos two_pos hmm
  have hc : 0 < 2 / omegaM p u k (Fintype.card ι) := div_pos two_pos hωm
  have hCm : 1 < CmA p u k (Fintype.card ι) := by
    unfold CmA
    linarith
  -- the depth
  obtain ⟨r, hrdef⟩ : ∃ r : ℝ, r = Real.log (CmA p u k (Fintype.card ι)) + ε := ⟨_, rfl⟩
  have hexp : Real.exp r = CmA p u k (Fintype.card ι) * Real.exp ε := by
    rw [hrdef, Real.exp_add, Real.exp_log (by linarith)]
  have hLpos : 0 < Real.log (CmA p u k (Fintype.card ι)) := Real.log_pos hCm
  have hr : 0 < r := by
    rw [hrdef]
    linarith
  have hεexp : 1 ≤ Real.exp ε := Real.one_le_exp hε
  have hR : 2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) +
      2 / omegaM p u k (Fintype.card ι) ≤ Real.exp r - 1 := by
    rw [hexp]
    unfold CmA
    nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ 1 +
      2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) +
      2 / omegaM p u k (Fintype.card ι)) (sub_nonneg.mpr hεexp)]
  have hR1 : 0 < Real.exp r - 1 := by linarith
  have h2 : 2 / omegaM p u k (Fintype.card ι) < Real.exp r - 1 := by linarith
  have h3 : 2 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι) := by
    have h := mul_lt_mul_of_pos_right h2 hωm
    rw [div_mul_cancel₀ _ hωm.ne'] at h
    exact h
  have hcond : 1 < (Real.exp r - 1) * omegaM p u k (Fintype.card ι) := by linarith
  have hκ : omegaM p u k (Fintype.card ι) / 2 < kappaA p u r k (Fintype.card ι) := by
    unfold kappaA
    have h4 : 1 / (Real.exp r - 1) < omegaM p u k (Fintype.card ι) / 2 := by
      rw [div_lt_div_iff₀ hR1 two_pos]
      linarith
    linarith
  have hκpos : 0 < kappaA p u r k (Fintype.card ι) := by linarith
  have hβ : betaA p u r k (Fintype.card ι) <
      2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι) := by
    unfold betaA
    rw [div_lt_div_iff₀ hκpos hmm]
    unfold omegaM at hκ
    linarith
  have hβ0 : 0 ≤ betaA p u r k (Fintype.card ι) := div_nonneg hω.le hκpos.le
  have hthr : ε < Real.log (1 + (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι))) := by
    rw [Real.lt_log_iff_exp_lt (add_pos_of_pos_of_nonneg one_pos
      (div_nonneg hR1.le (by linarith)))]
    have h5 : (1 + 2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι)) *
        (Real.exp ε - 1) ≤ Real.exp r - 1 := by
      rw [hexp]
      unfold CmA
      nlinarith [mul_nonneg hc.le (by linarith : (0 : ℝ) ≤ Real.exp ε)]
    have h6 : Real.exp ε - 1 < (Real.exp r - 1) / (1 + betaA p u r k (Fintype.card ι)) := by
      rw [lt_div_iff₀ (by linarith)]
      rcases eq_or_lt_of_le (sub_nonneg.mpr hεexp) with h0 | hpos
      · rw [← h0, zero_mul]
        exact hR1
      · have h7 := mul_lt_mul_of_pos_left
          (by linarith : 1 + betaA p u r k (Fintype.card ι) <
            1 + 2 / min ((k : ℝ) / Fintype.card ι) (1 - (k : ℝ) / Fintype.card ι)) hpos
        linarith
    linarith
  obtain ⟨γ₂, hγ₂, b, hb0, hbβ, hlip, h⟩ :=
    theoremA_group_chernoff (ι := ι) hp0 hp1 hγ hr hkn.le hcond
  refine ⟨γ₂, hγ₂, b, hb0, by linarith, hlip, fun Ω _ alg P hP hP1 δ hcorr t ht0 ht1 => ?_⟩
  have h1 := h Ω alg P hP hP1 ε δ hthr hcorr t ht0
  have hexpt : Real.exp (t * r) ≤ CmA p u k (Fintype.card ι) * Real.exp (t * ε) := by
    rw [hrdef, mul_add, Real.exp_add]
    refine mul_le_mul_of_nonneg_right ?_ (Real.exp_pos _).le
    calc Real.exp (t * Real.log (CmA p u k (Fintype.card ι)))
        ≤ Real.exp (Real.log (CmA p u k (Fintype.card ι))) :=
          Real.exp_le_exp.mpr (by nlinarith)
      _ = CmA p u k (Fintype.card ι) := Real.exp_log (by linarith)
  have hρ : 0 ≤ rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι :=
    pow_nonneg (rhoT_nonneg hp0 hp1 u γ t hm0.le hm1.le) _
  have hEQ : 0 ≤ ∑ ω, P ω * (((alg ω (oracle1 (refW p)
      fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
      fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ) :=
    Finset.sum_nonneg fun ω _ => mul_nonneg (hP ω) (Nat.cast_nonneg _)
  refine h1.trans (mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left
    (mul_le_mul_of_nonneg_left ?_ (by linarith)) hn.le) hEQ)
  calc Real.exp (t * r) * rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι
      ≤ CmA p u k (Fintype.card ι) * Real.exp (t * ε) *
          rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι :=
        mul_le_mul_of_nonneg_right hexpt hρ
    _ = CmA p u k (Fintype.card ι) * (Real.exp (t * ε) *
          rhoT p u γ t ((k : ℝ) / Fintype.card ι) ^ Fintype.card ι) := mul_assoc _ _ _

open Classical in
/-- **Theorem A on `{0,1}ⁿ` with the cyclic shifts, the last display:** for `ε ≥ 0`, `0 < k < n`
there is an instance `ψ₀ = −ln(w̃_γ + b·w̃_{γ₂}) ∈ L_u` at which every `(ε/2, δ)`-correct oracle
algorithm has, for every `t ∈ [0, 1]`,
`1 − 2δ ≤ E|Q(ψ₀)| · n(n + 1) · C_m · e^{tε} · ρ_t(k/n; γ)ⁿ`. -/
theorem theoremA_fin_Cm {n : ℕ} [NeZero n] {p u γ ε : ℝ} (hp0 : 0 < p) (hp1 : p < 1)
    (hu : 0 < u) (hγ : |γ| ≤ u) (hε : 0 ≤ ε) {k : ℕ} (hk0 : 0 < k) (hkn : k < n) :
    ∃ γ₂ : ℝ, (γ₂ = -u ∨ γ₂ = u) ∧ ∃ b : ℝ, 0 ≤ b ∧
      b ≤ 2 / min ((k : ℝ) / n) (1 - (k : ℝ) / n) ∧
      LipH u (fun x : Fin n → Bool => -Real.log (baseW p γ x + b * baseW p γ₂ x)) ∧
      ∀ (Ω : Type v) [Fintype Ω]
        (alg : Ω → (Fin n → ℝ) → MetricChain.QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ),
        (∀ ω, 0 ≤ P ω) → ∑ ω, P ω = 1 → ∀ δ : ℝ,
        (∀ ψ : (Fin n → Bool) → ℝ, LipH u ψ → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
          |(alg ω (oracle1 (refW p) ψ)).output ψ - logA (refW p) ψ| ≤ ε / 2), P ω) →
        ∀ t : ℝ, 0 ≤ t → t ≤ 1 →
        1 - 2 * δ ≤
          (∑ ω, P ω * (((alg ω (oracle1 (refW p)
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x))).queries
              fun x => -Real.log (baseW p γ x + b * baseW p γ₂ x)).card : ℝ)) *
            ((n : ℝ) * (((n : ℝ) + 1) *
              (CmA p u k n * (Real.exp (t * ε) * rhoT p u γ t ((k : ℝ) / n) ^ n)))) := by
  have hkn' : k < Fintype.card (Fin n) := by
    rw [Fintype.card_fin]
    exact hkn
  have h := theoremA_group_Cm (ι := Fin n) (γ := γ) hp0 hp1 hu hγ hε hk0 hkn'
  rw [Fintype.card_fin] at h
  exact h

end TheoremA

end ScienceL3
