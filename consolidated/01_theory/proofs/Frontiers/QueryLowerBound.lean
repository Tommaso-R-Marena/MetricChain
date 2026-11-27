import Mathlib
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.CertificateNotions
import proofs.Frontiers.CertificateComplexity
import proofs.Frontiers.ThermalRobustness

/-!
# Query complexity: lower bounds for every algorithm, deterministic or randomised

The other files of this directory bound the size of a *certificate* of a given format.  This file
shows that the same structures constrain every *algorithm* that estimates a functional of the
unknown residual from point evaluations — the minimum of `f + g`, the logarithm of the partition
function, or any other functional.

## Model

* `QueryAlgorithm X` — an abstract deterministic adaptive algorithm: a finite set of queried
  points and an output for every residual, such that a residual which agrees with `g` on the
  points queried on `g` produces the same queries and the same output.  Every decision tree has
  this property; nothing else is assumed.  A randomised algorithm is a finite probability space
  `(Ω, P)` of deterministic ones.

## General principle (any class `G`, any functional `Φ`)

* `exists_query_ne` — if a deterministic algorithm is within `ε / 2` of `Φ` on the class, then on
  the instance `g` it queries a point where `g'` differs from `g`, for every alternative `g'` of
  the class with `|Φ g' - Φ g| > ε`.
* `prob_query_ne_ge` — if a randomised algorithm is within `ε / 2` with probability at least
  `1 - δ` on every member of the class, it detects every such alternative with probability at
  least `1 - 2δ`.
* `card_queries_ge_packing`, `expected_queries_ge_packing` — hence the number of evaluations on
  `g` (in expectation, for randomised algorithms, up to the factor `1 - 2δ`) is at least the
  total weight of every fractional packing of the difference sets of such alternatives.  This is
  the analogue for real-valued classes of the bound of randomised decision-tree complexity by
  fractional block sensitivity.
* `spotCheck_correct` — conversely, an algorithm that knows `g` as a hint, evaluates the
  residual at `N` independent points drawn from a distribution `q`, and outputs `Φ g` if all
  values agree (and evaluates everything otherwise) is correct on the whole class with
  probability at least `1 - δ`, provided every alternative with `|Φ g' - Φ g| > ε / 2` differs
  from `g` on a set of `q`-probability at least `p` and `(1 - p)^N ≤ δ`.

## The envelope class

* `dip d g y c` — the residual `g` with a dip of depth `c` at `y`.  It is admissible, lies below
  `g`, and differs from `g` exactly at the points whose slack to `y` is smaller than `c`
  (`dip_eq_sub`, `dip_eq_of_le_slack`).
* `queries_cover_of_sensitive`, `expected_queries_ge_of_radius`,
  `expected_queries_ge_exp_weights` — the principle for dips: if a dip of depth `r y` at `y`
  changes `Φ` by more than `ε`, the queries must reach within slack `r y` of `y`.

## The minimum

* `queries_strict_cover`, `expected_queries_ge`, `expected_queries_ge_exp_weights_min` — for
  `Φ = min (f + g)` the radius is `gap y + ε'`, `ε' > ε`: every algorithm pays the covering price
  of `CertificationGeometry.lean`, and randomisation gains at most the factor `1 - 2δ` against
  the fractional covering bounds.
* `queries_isValueCertificate`, `certificateAlgorithm_correct`, `instance_query_complexity` —
  for deterministic algorithms the statement is exact: there is an algorithm, within `ε / 2` on
  the whole admissible class, that makes `k` evaluations on `g` iff `g` has a value certificate
  of size `k`.
* `binary_randomized_exponential` — on the binary product landscape of
  `binary_certificate_exponential`, every randomised algorithm makes at least
  `(1 - 2δ) (6/5)^n` evaluations in expectation.
* `lower_alternative_differs_on_ball`, `higher_alternative_differs_on_minimisers`,
  `min_spotCheck_correct` — conversely, an alternative with a different minimum differs from
  the instance on a whole closed slack ball or on all near-minimisers, so spot-checking with a
  fractional cover as sampling distribution is correct.  This unhedged converse works at level
  `ε / 2` while the lower bound is at level `ε`; the hedged version
  (`min_hedgedSpotCheck_correct` in `QueryRefinements.lean`) closes the gap between the levels.

## The free energy

* `softGap β d f g y` — `log Z(f + g) - log Z(f + U_y)`, where `U_y = g y + d · y` is the upper
  McShane envelope of the single evaluation at `y`.
* `log_sum_exp_dip_ge`, `thermal_queries_strict_cover`, `thermal_expected_queries_ge` — for
  `Φ = log Z` the radius of `y` is any `c` with `softGap y + ε < β c`.
* `thermal_queries_bracket` — the queries of a correct *deterministic* algorithm for `log Z`
  form a free-energy certificate (the two envelope partition functions agree within `exp ε`),
  so the certificate bounds of `ThermalRobustness.lean` and `ExponentialWeights.lean` apply to
  every deterministic algorithm.
* `cube_thermal_randomized_exponential` — on `4m` two-state sites with zero known part, zero
  residual, unit Hamming envelope and `β = log 16`, every randomised algorithm that returns
  `log Z` within `ε / 2` with probability `1 - δ` makes at least `(1 - 2δ) (27/16)^m`
  evaluations in expectation, for every `ε` below `m (log 16 - 4 log (32/17)) ≈ 0.24 m`.
* `cube_thermal_randomized_bound` — the same for all `n`, `β`, `c`, radii and Chernoff
  parameters; it is exponential in `n` whenever `ε / n < log cosh (βc / 2)`, the largest Jensen
  gap of the class per site.  Above that accuracy a bounded number of random evaluations
  suffices on every instance (a paper proof with the exact two-point constant, theory report
  Theorem 11.25(b); the machine-checked sandwich of `SampledSandwich.lean` has the larger width
  `β² ∑ c² / 8`).  So this accuracy is a sharp threshold for the worst case over instances: the
  lower bound is proved at the zero residual, and other instances of the same class can be
  cheap at every accuracy.  For exponentially small accuracies the soft-gap bound is not tight;
  see `cube_exact_dip_randomized` in `QueryRefinements.lean`.
-/

namespace MetricChain

open Finset

variable {X : Type*}

/-! ### Abstract query algorithms -/

/-- A deterministic adaptive query algorithm, abstractly: for every residual a finite set of
queried points and an output, such that residuals agreeing with `g` on the points queried on `g`
are treated exactly like `g`.

Every decision tree (adaptive evaluation procedure) defines such an object, but the converse
fails: the consistency axiom says only that the partial assignments `g|Q(g)` partition the
function space, and there are such partitions that no query order realises
(`Referee3.pathoAlg_not_a_tree` in `QueryRefinements.lean`).  The class is therefore strictly
larger than the class of algorithms, which only strengthens the lower bounds proved for it; the
upper bounds (`certificateAlgorithm`, `spotCheck`, `hedgedSpotCheck`) are genuine two-round
procedures. -/
structure QueryAlgorithm (X : Type*) where
  /-- The points at which the algorithm evaluates the residual. -/
  queries : (X → ℝ) → Finset X
  /-- The number returned by the algorithm. -/
  output : (X → ℝ) → ℝ
  /-- Residuals that agree on the queried set are indistinguishable for the algorithm. -/
  consistent : ∀ g g' : X → ℝ, (∀ a ∈ queries g, g' a = g a) →
    queries g' = queries g ∧ output g' = output g

/-- The algorithm that evaluates the residual everywhere and returns the exact value of `Φ`. -/
def fullQueryAlgorithm [Fintype X] (Φ : (X → ℝ) → ℝ) : QueryAlgorithm X where
  queries := fun _ => univ
  output := Φ
  consistent := by
    intro g g' h
    have hgg : g' = g := funext fun a => h a (mem_univ a)
    rw [hgg]
    exact ⟨rfl, rfl⟩

/-! ### The general principle: sensitive alternatives must be detected -/

section Generic

variable {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}

/-- **Deterministic detection.**  If the output is within `ε / 2` of `Φ` on the class `G`, then
on the instance `g` the algorithm queries a point at which `g'` differs from `g`, for every
alternative `g'` of the class whose value of `Φ` differs from that of `g` by more than `ε`. -/
theorem exists_query_ne (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, G g → |alg.output g - Φ g| ≤ ε / 2) {g g' : X → ℝ} (hg : G g) (hg' : G g')
    (hΦ : ε < |Φ g' - Φ g|) : ∃ a ∈ alg.queries g, g' a ≠ g a := by
  by_contra hno
  have hall : ∀ a ∈ alg.queries g, g' a = g a := by
    intro a ha
    by_contra hne
    exact hno ⟨a, ha, hne⟩
  have hout := (alg.consistent g g' hall).2
  have c1 := abs_le.mp (hcorr g hg)
  have c2 := abs_le.mp (hcorr g' hg')
  rw [hout] at c2
  have h3 : |Φ g' - Φ g| ≤ ε := abs_le.mpr ⟨by linarith [c1.1, c2.2], by linarith [c1.2, c2.1]⟩
  linarith

/-- **Weights detected by a set.**  If the weights `w ≥ 0` put total mass at most `B` on the set
of alternatives detected by any single point of `A`, the total weight of the alternatives
detected by `A` is at most `|A| · B`. -/
theorem sum_detected_le_card {ι : Type*} [Fintype ι] {R : X → ι → Prop}
    [∀ a, DecidablePred (R a)] (A : Finset X) [DecidablePred fun j => ∃ a ∈ A, R a j]
    (w : ι → ℝ) (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hcap : ∀ a ∈ A, ∑ j ∈ univ.filter (fun j => R a j), w j ≤ B) :
    ∑ j ∈ univ.filter (fun j => ∃ a ∈ A, R a j), w j ≤ A.card * B := by
  have hnn : ∀ (j : ι) (a : X), 0 ≤ (if R a j then w j else 0) := by
    intro j a
    split_ifs
    · exact hw j
    · exact le_rfl
  calc ∑ j ∈ univ.filter (fun j => ∃ a ∈ A, R a j), w j
      ≤ ∑ j ∈ univ.filter (fun j => ∃ a ∈ A, R a j), ∑ a ∈ A, (if R a j then w j else 0) := by
        refine Finset.sum_le_sum fun j hj => ?_
        obtain ⟨a, ha, hR⟩ := (Finset.mem_filter.mp hj).2
        calc w j = if R a j then w j else 0 := by rw [if_pos hR]
          _ ≤ ∑ a ∈ A, (if R a j then w j else 0) :=
              Finset.single_le_sum (f := fun a => if R a j then w j else 0)
                (fun a _ => hnn j a) ha
    _ ≤ ∑ j, ∑ a ∈ A, (if R a j then w j else 0) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          fun j _ _ => Finset.sum_nonneg fun a _ => hnn j a
    _ = ∑ a ∈ A, ∑ j, (if R a j then w j else 0) := Finset.sum_comm
    _ = ∑ a ∈ A, ∑ j ∈ univ.filter (fun j => R a j), w j := by
        refine Finset.sum_congr rfl fun a _ => ?_
        rw [Finset.sum_filter]
    _ ≤ ∑ _a ∈ A, B := Finset.sum_le_sum fun a ha => hcap a ha
    _ = A.card * B := by rw [Finset.sum_const, nsmul_eq_mul]

open Classical in
/-- **Deterministic packing bound.**  Let `alt j` be alternatives of the class whose values of
`Φ` differ from that of `g` by more than `ε`, and let `w ≥ 0` be weights such that every point
`a` detects alternatives of total weight at most `B`.  Then every algorithm that is within
`ε / 2` of `Φ` on the class makes at least `(∑ w) / B` evaluations on `g`. -/
theorem card_queries_ge_packing {ι : Type*} [Fintype ι] (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, G g → |alg.output g - Φ g| ≤ ε / 2) {g : X → ℝ} (hg : G g)
    (alt : ι → X → ℝ) (halt : ∀ j, G (alt j)) (hsens : ∀ j, ε < |Φ (alt j) - Φ g|)
    (w : ι → ℝ) (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => alt j a ≠ g a), w j ≤ B) :
    ∑ j, w j ≤ (alg.queries g).card * B := by
  have h := sum_detected_le_card (R := fun a j => alt j a ≠ g a) (alg.queries g) w hw
    fun a _ => hcap a
  have hall : univ.filter (fun j => ∃ a ∈ alg.queries g, alt j a ≠ g a) = univ := by
    apply Finset.filter_true_of_mem
    intro j _
    exact exists_query_ne alg hcorr hg (halt j) (hsens j)
  rwa [hall] at h

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Randomised detection.**  Let `alg ω` be deterministic algorithms indexed by a finite
probability space `(Ω, P)`.  If on every member of the class the output is within `ε / 2` of `Φ`
with probability at least `1 - δ`, then on the instance `g` every alternative `g'` of the class
with `|Φ g' - Φ g| > ε` is detected (some queried point has `g' a ≠ g a`) with probability at
least `1 - 2δ`: a run that does not detect `g'` returns the same number on `g` and on `g'`, and
that number cannot be within `ε / 2` of both values. -/
theorem prob_query_ne_ge (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    {g g' : X → ℝ} (hg : G g) (hg' : G g') (hΦ : ε < |Φ g' - Φ g|) :
    1 - 2 * δ ≤ ∑ ω ∈ univ.filter (fun ω => ∃ a ∈ (alg ω).queries g, g' a ≠ g a), P ω := by
  have hsub : univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2) ∩
      univ.filter (fun ω => |(alg ω).output g' - Φ g'| ≤ ε / 2) ⊆
        univ.filter (fun ω => ∃ a ∈ (alg ω).queries g, g' a ≠ g a) := by
    intro ω hω
    obtain ⟨h1, h2⟩ := Finset.mem_inter.mp hω
    refine Finset.mem_filter.mpr ⟨mem_univ ω, ?_⟩
    by_contra hno
    have hall : ∀ a ∈ (alg ω).queries g, g' a = g a := by
      intro a ha
      by_contra hne
      exact hno ⟨a, ha, hne⟩
    have hout := ((alg ω).consistent g g' hall).2
    have c1 := abs_le.mp (Finset.mem_filter.mp h1).2
    have c2 := abs_le.mp (Finset.mem_filter.mp h2).2
    rw [hout] at c2
    have h3 : |Φ g' - Φ g| ≤ ε :=
      abs_le.mpr ⟨by linarith [c1.1, c2.2], by linarith [c1.2, c2.1]⟩
    linarith
  have hui := Finset.sum_union_inter
    (s₁ := univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2))
    (s₂ := univ.filter (fun ω => |(alg ω).output g' - Φ g'| ≤ ε / 2)) (f := P)
  have hunion : ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2) ∪
      univ.filter (fun ω => |(alg ω).output g' - Φ g'| ≤ ε / 2), P ω ≤ 1 := by
    rw [← hP1]
    exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun ω _ _ => hP ω
  have h1 := hcorr g hg
  have h2 := hcorr g' hg'
  have hinter : 1 - 2 * δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2) ∩
      univ.filter (fun ω => |(alg ω).output g' - Φ g'| ≤ ε / 2), P ω := by linarith
  exact hinter.trans (Finset.sum_le_sum_of_subset_of_nonneg hsub fun ω _ _ => hP ω)

open Classical in
/-- **Randomised packing bound.**  Under the hypothesis of `prob_query_ne_ge`, let `alt j` be
alternatives of the class with `|Φ (alt j) - Φ g| > ε` and `w ≥ 0` weights such that every point
detects alternatives of total weight at most `B`.  Then the expected number of evaluations on
`g` is at least `(1 - 2δ) (∑ w) / B`. -/
theorem expected_queries_ge_packing {ι : Type*} [Fintype ι] (alg : Ω → QueryAlgorithm X)
    (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : G g) (alt : ι → X → ℝ) (halt : ∀ j, G (alt j))
    (hsens : ∀ j, ε < |Φ (alt j) - Φ g|) (w : ι → ℝ) (hw : ∀ j, 0 ≤ w j) {B : ℝ}
    (hcap : ∀ a, ∑ j ∈ univ.filter (fun j => alt j a ≠ g a), w j ≤ B) :
    (1 - 2 * δ) * ∑ j, w j ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  have hdet : ∀ j, 1 - 2 * δ ≤
      ∑ ω ∈ univ.filter (fun ω => ∃ a ∈ (alg ω).queries g, alt j a ≠ g a), P ω := fun j =>
    prob_query_ne_ge alg P hP hP1 hcorr hg (halt j) (hsens j)
  have hrun : ∀ ω, ∑ j ∈ univ.filter (fun j => ∃ a ∈ (alg ω).queries g, alt j a ≠ g a), w j ≤
      ((alg ω).queries g).card * B := fun ω =>
    sum_detected_le_card (R := fun a j => alt j a ≠ g a) ((alg ω).queries g) w hw
      fun a _ => hcap a
  calc (1 - 2 * δ) * ∑ j, w j = ∑ j, w j * (1 - 2 * δ) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl fun j _ => mul_comm _ _
    _ ≤ ∑ j, w j * ∑ ω ∈ univ.filter (fun ω => ∃ a ∈ (alg ω).queries g, alt j a ≠ g a), P ω :=
        Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hdet j) (hw j)
    _ = ∑ j, ∑ ω, if (∃ a ∈ (alg ω).queries g, alt j a ≠ g a) then w j * P ω else 0 := by
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.mul_sum, Finset.sum_filter]
    _ = ∑ ω, ∑ j, if (∃ a ∈ (alg ω).queries g, alt j a ≠ g a) then w j * P ω else 0 :=
        Finset.sum_comm
    _ = ∑ ω, P ω * ∑ j ∈ univ.filter (fun j => ∃ a ∈ (alg ω).queries g, alt j a ≠ g a), w j := by
        refine Finset.sum_congr rfl fun ω _ => ?_
        rw [Finset.mul_sum, Finset.sum_filter]
        refine Finset.sum_congr rfl fun j _ => ?_
        split_ifs
        · ring
        · simp
    _ ≤ ∑ ω, P ω * (((alg ω).queries g).card * B) :=
        Finset.sum_le_sum fun ω _ => mul_le_mul_of_nonneg_left (hrun ω) (hP ω)
    _ = (∑ ω, P ω * ((alg ω).queries g).card) * B := by
        rw [Finset.sum_mul]
        exact Finset.sum_congr rfl fun ω _ => by ring

end Generic

/-! ### The single-point dip -/

/-- The residual `g` with a dip of depth `c` at `y`. -/
def dip (d : X → X → ℝ) (g : X → ℝ) (y : X) (c : ℝ) (a : X) : ℝ := min (g a) (g y - c + d a y)

/-- The dip lies below the residual. -/
theorem dip_le (d : X → X → ℝ) (g : X → ℝ) (y : X) (c : ℝ) (a : X) : dip d g y c a ≤ g a :=
  min_le_left _ _

/-- The dip is admissible. -/
theorem dip_admissible {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ} (hg : Admissible d g)
    (y : X) (c : ℝ) : Admissible d (dip d g y c) := by
  intro a a'
  have h1 := hg a a'
  have h2 := hd.triangle a a' y
  have hl := min_le_left (g a) (g y - c + d a y)
  have hr := min_le_right (g a) (g y - c + d a y)
  unfold dip
  rcases min_cases (g a') (g y - c + d a' y) with ⟨h, _⟩ | ⟨h, _⟩
  · rw [h]
    linarith
  · rw [h]
    linarith

/-- A dip of depth `c` at `y` lowers the residual at `x` by the positive part of `c - s(x, y)`. -/
theorem dip_eq_sub (d : X → X → ℝ) (g : X → ℝ) (y : X) (c : ℝ) (x : X) :
    dip d g y c x = g x - max 0 (c - slack d g x y) := by
  have hs : slack d g x y = d x y - g x + g y := rfl
  unfold dip
  rcases le_total (c - slack d g x y) 0 with h | h
  · rw [max_eq_left h, min_eq_left (by linarith)]
    ring
  · rw [max_eq_right h, min_eq_right (by linarith)]
    linarith

/-- A point whose slack to `y` is at least the depth does not see the dip. -/
theorem dip_eq_of_le_slack {d : X → X → ℝ} {g : X → ℝ} {y : X} {c : ℝ} {a : X}
    (h : c ≤ slack d g a y) : dip d g y c a = g a := by
  rw [dip_eq_sub, max_eq_left (by linarith)]
  ring

/-- A point that sees the dip has slack to `y` smaller than the depth. -/
theorem slack_lt_of_dip_ne {d : X → X → ℝ} {g : X → ℝ} {y : X} {c : ℝ} {a : X}
    (h : dip d g y c a ≠ g a) : slack d g a y < c := by
  by_contra hno
  exact h (dip_eq_of_le_slack (not_lt.mp hno))

/-- At its centre a dip of nonnegative depth lowers the residual by exactly its depth. -/
theorem dip_self {d : X → X → ℝ} (hd : IsEnvelope d) (g : X → ℝ) (y : X) {c : ℝ} (hc : 0 ≤ c) :
    dip d g y c y = g y - c := by
  have hs : slack d g y y = 0 := by
    have h := hd.self y
    have h' : slack d g y y = d y y - g y + g y := rfl
    linarith
  rw [dip_eq_sub, hs, sub_zero, max_eq_right hc]

/-! ### The principle for dips: sensitivity radii -/

section Radius

variable {Φ : (X → ℝ) → ℝ}

/-- **Deterministic: the queries reach within the sensitivity radius.**  If a dip of depth `c` at
`y` changes `Φ` by more than `ε`, every algorithm that is within `ε / 2` of `Φ` on the admissible
class queries, on `g`, a point whose slack to `y` is smaller than `c`. -/
theorem queries_cover_of_sensitive {d : X → X → ℝ} (hd : IsEnvelope d) (alg : QueryAlgorithm X)
    {ε : ℝ} (hcorr : ∀ g, Admissible d g → |alg.output g - Φ g| ≤ ε / 2) {g : X → ℝ}
    (hg : Admissible d g) {y : X} {c : ℝ} (hsens : ε < |Φ (dip d g y c) - Φ g|) :
    ∃ a ∈ alg.queries g, slack d g a y < c := by
  obtain ⟨a, ha, hne⟩ := exists_query_ne (G := Admissible d) alg hcorr hg
    (dip_admissible hd hg y c) hsens
  exact ⟨a, ha, slack_lt_of_dip_ne hne⟩

variable [Fintype X] {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Randomised: packing with sensitivity radii.**  Let `r y` be a depth at which the dip at `y`
changes `Φ` by more than `ε`, and `w ≥ 0` weights such that the points within slack `r y` of any
single point `a` have total weight at most `B`.  Then a randomised algorithm that is within
`ε / 2` of `Φ` with probability at least `1 - δ` on every admissible residual makes at least
`(1 - 2δ) (∑ w) / B` evaluations on `g` in expectation. -/
theorem expected_queries_ge_of_radius {d : X → X → ℝ} (hd : IsEnvelope d)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, Admissible d g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (r : X → ℝ)
    (hsens : ∀ y, ε < |Φ (dip d g y (r y)) - Φ g|) (w : X → ℝ) (hw : ∀ y, 0 ≤ w y) {B : ℝ}
    (hcap : ∀ a, ∑ y ∈ univ.filter (fun y => slack d g a y < r y), w y ≤ B) :
    (1 - 2 * δ) * ∑ y, w y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  refine expected_queries_ge_packing (G := Admissible d) alg P hP hP1 hcorr hg
    (fun y => dip d g y (r y)) (fun y => dip_admissible hd hg y (r y)) hsens w hw fun a => ?_
  refine le_trans (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun y _ _ => hw y) (hcap a)
  intro y hy
  exact Finset.mem_filter.mpr ⟨mem_univ y, slack_lt_of_dip_ne (Finset.mem_filter.mp hy).2⟩

open Classical in
/-- **Randomised: exponential weights with sensitivity radii.**  In the situation of
`expected_queries_ge_of_radius`, for every `t ≥ 0` and all weights `v ≥ 0`,
`(1 - 2δ) ∑ v ≤ E|Q| · max_a ∑_y v y · exp (-t (s(a, y) - r y))`. -/
theorem expected_queries_ge_exp_weights {d : X → X → ℝ} (hd : IsEnvelope d)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, Admissible d g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (r : X → ℝ)
    (hsens : ∀ y, ε < |Φ (dip d g y (r y)) - Φ g|) {t : ℝ} (ht : 0 ≤ t) (v : X → ℝ)
    (hv : ∀ y, 0 ≤ v y) {B : ℝ}
    (hB : ∀ a, ∑ y, v y * Real.exp (-t * (slack d g a y - r y)) ≤ B) :
    (1 - 2 * δ) * ∑ y, v y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  refine expected_queries_ge_of_radius hd alg P hP hP1 hcorr hg r hsens v hv fun a => ?_
  refine le_trans ?_ (hB a)
  calc ∑ y ∈ univ.filter (fun y => slack d g a y < r y), v y
      ≤ ∑ y ∈ univ.filter (fun y => slack d g a y < r y),
          v y * Real.exp (-t * (slack d g a y - r y)) := by
        refine Finset.sum_le_sum fun y hy => ?_
        have hlt := (Finset.mem_filter.mp hy).2
        have h1 : (1 : ℝ) ≤ Real.exp (-t * (slack d g a y - r y)) := by
          rw [← Real.exp_zero]
          apply Real.exp_le_exp.mpr
          nlinarith
        calc v y = v y * 1 := (mul_one _).symm
          _ ≤ v y * Real.exp (-t * (slack d g a y - r y)) := mul_le_mul_of_nonneg_left h1 (hv y)
    _ ≤ ∑ y, v y * Real.exp (-t * (slack d g a y - r y)) :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          fun y _ _ => mul_nonneg (hv y) (Real.exp_pos _).le

end Radius

/-! ### The minimum -/

section Minimum

variable [Fintype X] [Nonempty X]

/-- Adding a constant to the residual shifts the minimum. -/
theorem min_add_const_shift (f g : X → ℝ) (c : ℝ) :
    (univ.inf' univ_nonempty fun x => f x + (g x + c)) =
      (univ.inf' univ_nonempty fun x => f x + g x) + c := by
  apply le_antisymm
  · obtain ⟨x, _, hx⟩ := Finset.exists_mem_eq_inf' univ_nonempty (fun x => f x + g x)
    have h1 : (univ.inf' univ_nonempty fun x => f x + (g x + c)) ≤ f x + (g x + c) :=
      Finset.inf'_le (fun x => f x + (g x + c)) (mem_univ x)
    rw [hx]
    linarith
  · apply Finset.le_inf'
    intro x _
    have h1 : (univ.inf' univ_nonempty fun x => f x + g x) ≤ f x + g x :=
      Finset.inf'_le (fun x => f x + g x) (mem_univ x)
    linarith

/-- A dip at `y` of depth `gap y + ε'` lowers the minimum by at least `ε'`. -/
theorem inf_dip_le {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (y : X) {ε' : ℝ}
    (hε' : 0 ≤ ε') :
    (univ.inf' univ_nonempty fun x => f x +
        dip d g y (f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε') x) ≤
      (univ.inf' univ_nonempty fun x => f x + g x) - ε' := by
  have hmin : (univ.inf' univ_nonempty fun x => f x + g x) ≤ f y + g y :=
    Finset.inf'_le (fun x => f x + g x) (mem_univ y)
  have hc : 0 ≤ f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε' := by linarith
  have h1 := Finset.inf'_le (fun x => f x +
    dip d g y (f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε') x) (mem_univ y)
  rw [dip_self hd g y hc] at h1
  linarith

/-- A dip of depth `gap y + ε'` is sensitive for the minimum at every level `ε < ε'`. -/
theorem min_dip_sensitive {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (y : X) {ε ε' : ℝ}
    (hε0 : 0 ≤ ε) (hε : ε < ε') :
    ε < |(univ.inf' univ_nonempty fun x => f x +
        dip d g y (f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε') x) -
      univ.inf' univ_nonempty fun x => f x + g x| := by
  have h := inf_dip_le hd f g y (hε0.trans hε.le)
  rw [abs_of_nonpos (by linarith)]
  linarith

/-- **Deterministic lower bound: the queried set of a correct algorithm is a strict cover.**
If the output of the algorithm is within `ε / 2` of `min (f + g)` for every admissible residual,
then on every admissible instance `g`, for every `ε' > ε` and every point `y`, some queried point
has slack to `y` smaller than `gap y + ε'`. -/
theorem queries_strict_cover {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) {ε' : ℝ} (hε : ε < ε') (y : X) :
    ∃ a ∈ alg.queries g,
      slack d g a y < f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε' := by
  have hε0 : 0 ≤ ε := by
    have := (abs_nonneg _).trans (hcorr g hg)
    linarith
  exact queries_cover_of_sensitive (Φ := fun g => univ.inf' univ_nonempty fun x => f x + g x)
    hd alg hcorr hg (min_dip_sensitive hd f g y hε0 hε)

/-- A correct algorithm evaluates the residual at least once. -/
theorem queries_nonempty {d : X → X → ℝ} (f : X → ℝ) (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) : (alg.queries g).Nonempty := by
  by_contra hne
  rw [Finset.not_nonempty_iff_eq_empty] at hne
  have hg' : Admissible d (fun x => g x + (ε + 1)) := by
    intro x y
    have := hg x y
    linarith
  have hout := (alg.consistent g (fun x => g x + (ε + 1)) (by
    intro a ha
    rw [hne] at ha
    exact absurd ha (Finset.notMem_empty a))).2
  have c1 := abs_le.mp (hcorr g hg)
  have c2 := abs_le.mp (hcorr _ hg')
  rw [hout, min_add_const_shift] at c2
  linarith [c1.2, c2.1]

/-- **The queries of a correct algorithm form a value certificate.**  If the output is within
`ε / 2` of `min (f + g)` for every admissible residual, then on every admissible instance the
two McShane envelopes of the evaluated values give minima that differ by at most `ε`: both
envelopes are admissible, agree with `g` on the queried set, and therefore receive the same
output. -/
theorem queries_isValueCertificate {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : QueryAlgorithm X) {ε : ℝ}
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) :
    IsValueCertificate d f g (alg.queries g) (queries_nonempty f alg hcorr hg) ε := by
  have hA := queries_nonempty f alg hcorr hg
  have hL : ∀ a ∈ alg.queries g, lowerEnv d (alg.queries g) hA g a = g a := fun a ha =>
    lowerEnv_eq_of_mem hd _ hA g (fun a _ b _ => hg a b) ha
  have hU : ∀ a ∈ alg.queries g, upperEnv d (alg.queries g) hA g a = g a := fun a ha =>
    upperEnv_eq_of_mem hd _ hA g (fun a _ b _ => hg a b) ha
  have hoL := (alg.consistent g _ hL).2
  have hoU := (alg.consistent g _ hU).2
  have cL := abs_le.mp (hcorr _ (lowerEnv_admissible hd _ hA g))
  have cU := abs_le.mp (hcorr _ (upperEnv_admissible hd _ hA g))
  rw [hoL] at cL
  rw [hoU] at cU
  unfold IsValueCertificate certLB
  linarith [cL.2, cU.1]

open Classical in
/-- The algorithm that knows a candidate residual `g₀` and a set `A`: it evaluates the residual
on `A`; if the values agree with those of `g₀` it returns the midpoint of the interval certified
by the two McShane envelopes, and otherwise it evaluates everything and returns the exact
minimum. -/
noncomputable def certificateAlgorithm (d : X → X → ℝ) (f g₀ : X → ℝ) (A : Finset X)
    (hA : A.Nonempty) : QueryAlgorithm X where
  queries := fun g => if ∀ a ∈ A, g a = g₀ a then A else univ
  output := fun g => if ∀ a ∈ A, g a = g₀ a then
      ((univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g₀ y) + certLB d f g₀ A hA) / 2
    else univ.inf' univ_nonempty fun x => f x + g x
  consistent := by
    intro g g' h
    by_cases hg : ∀ a ∈ A, g a = g₀ a
    · simp only [if_pos hg] at h
      have hg' : ∀ a ∈ A, g' a = g₀ a := fun a ha => (h a ha).trans (hg a ha)
      simp only [if_pos hg, if_pos hg']
      exact ⟨trivial, trivial⟩
    · simp only [if_neg hg] at h
      have hgg : g' = g := funext fun a => h a (mem_univ a)
      rw [hgg]
      exact ⟨rfl, rfl⟩

/-- On the candidate itself the certificate algorithm evaluates exactly `A`. -/
theorem certificateAlgorithm_queries (d : X → X → ℝ) (f g₀ : X → ℝ) (A : Finset X)
    (hA : A.Nonempty) : (certificateAlgorithm d f g₀ A hA).queries g₀ = A := by
  unfold certificateAlgorithm
  exact if_pos fun _ _ => rfl

/-- **A value certificate gives a correct algorithm.**  If `A` is a value `ε`-certificate for
`g₀`, the certificate algorithm is within `ε / 2` of `min (f + g)` for every admissible
residual `g`. -/
theorem certificateAlgorithm_correct {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    {g₀ : X → ℝ} (hg₀ : Admissible d g₀) {A : Finset X} {hA : A.Nonempty} {ε : ℝ}
    (hcert : IsValueCertificate d f g₀ A hA ε) (g : X → ℝ) (hg : Admissible d g) :
    |(certificateAlgorithm d f g₀ A hA).output g - univ.inf' univ_nonempty fun x => f x + g x| ≤
      ε / 2 := by
  unfold IsValueCertificate at hcert
  have hwidth : certLB d f g₀ A hA ≤ univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g₀ y := by
    apply Finset.le_inf'
    intro y _
    have h1 : certLB d f g₀ A hA ≤ f y + lowerEnv d A hA g₀ y :=
      Finset.inf'_le (fun y => f y + lowerEnv d A hA g₀ y) (mem_univ y)
    have h2 := lowerEnv_le_upperEnv hd A hA g₀ (fun a _ b _ => hg₀ a b) y
    linarith
  by_cases hag : ∀ a ∈ A, g a = g₀ a
  · have hout : (certificateAlgorithm d f g₀ A hA).output g =
        ((univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g₀ y) + certLB d f g₀ A hA) / 2 := by
      unfold certificateAlgorithm
      exact if_pos hag
    have h1 : certLB d f g₀ A hA ≤ univ.inf' univ_nonempty fun x => f x + g x := by
      apply Finset.le_inf'
      intro y _
      exact certLB_le f g₀ A hA hg hag y
    have h2 : (univ.inf' univ_nonempty fun x => f x + g x) ≤
        univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g₀ y := by
      apply Finset.le_inf'
      intro y _
      have h3 : (univ.inf' univ_nonempty fun x => f x + g x) ≤ f y + g y :=
        Finset.inf'_le (fun x => f x + g x) (mem_univ y)
      have h4 := le_upperEnv hg A hA g₀ hag y
      linarith
    rw [hout, abs_le]
    constructor <;> linarith
  · have hout : (certificateAlgorithm d f g₀ A hA).output g =
        univ.inf' univ_nonempty fun x => f x + g x := by
      unfold certificateAlgorithm
      exact if_neg hag
    rw [hout, sub_self, abs_zero]
    linarith

/-- **Instance-wise query complexity equals certificate size.**  On an admissible instance `g`
there is an algorithm, within `ε / 2` of `min (f + g')` on *every* admissible residual `g'`, that
makes exactly `k` evaluations on `g`, iff `g` has a value `ε`-certificate with `k` points. -/
theorem instance_query_complexity {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {g : X → ℝ}
    (hg : Admissible d g) (ε : ℝ) (k : ℕ) :
    (∃ alg : QueryAlgorithm X,
        (∀ g', Admissible d g' →
          |alg.output g' - univ.inf' univ_nonempty fun x => f x + g' x| ≤ ε / 2) ∧
        (alg.queries g).card = k) ↔
      ∃ (A : Finset X) (hA : A.Nonempty), IsValueCertificate d f g A hA ε ∧ A.card = k := by
  constructor
  · rintro ⟨alg, hcorr, hk⟩
    exact ⟨alg.queries g, queries_nonempty f alg hcorr hg,
      queries_isValueCertificate hd f alg hcorr hg, hk⟩
  · rintro ⟨A, hA, hcert, hk⟩
    refine ⟨certificateAlgorithm d f g A hA, certificateAlgorithm_correct hd f hg hcert, ?_⟩
    rw [certificateAlgorithm_queries]
    exact hk

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Randomised lower bound for the minimum.**  Let `alg ω` be deterministic query algorithms
indexed by a finite probability space `(Ω, P)`.  If for every admissible residual the output is
within `ε / 2` of `min (f + g)` with probability at least `1 - δ`, then on every admissible
instance `g` and for every `ε' > ε` the expected number of evaluations is at least `(1 - 2δ)`
times the total weight of every fractional packing `w` of the strict covering relation at
level `ε'` (capacity `B`). -/
theorem expected_queries_ge {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ} (hε0 : 0 ≤ ε)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) {ε' : ℝ} (hε : ε < ε') (w : X → ℝ) (hw : ∀ y, 0 ≤ w y)
    {B : ℝ}
    (hcap : ∀ a, ∑ y ∈ univ.filter (fun y => slack d g a y <
      f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε'), w y ≤ B) :
    (1 - 2 * δ) * ∑ y, w y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B :=
  expected_queries_ge_of_radius (Φ := fun g => univ.inf' univ_nonempty fun x => f x + g x)
    hd alg P hP hP1 hcorr hg
    (fun y => f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε')
    (fun y => min_dip_sensitive hd f g y hε0 hε) w hw hcap

open Classical in
/-- **Randomised exponential-weights bound for the minimum** — the counterpart of
`card_ge_exp_weights` for every randomised algorithm: for all `t ≥ 0`, `v ≥ 0` and `ε' > ε`,
`(1 - 2δ) e^{-t ε'} ∑ v ≤ E|Q| · max_a ∑_y v y · exp (-t (s(a, y) - gap y))`. -/
theorem expected_queries_ge_exp_weights_min {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ} (hε0 : 0 ≤ ε)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) {ε' : ℝ} (hε : ε < ε') {t : ℝ} (ht : 0 ≤ t) (v : X → ℝ)
    (hv : ∀ y, 0 ≤ v y) {B : ℝ}
    (hB : ∀ a, ∑ y, v y * Real.exp (-t * (slack d g a y -
      (f y + g y - univ.inf' univ_nonempty fun x => f x + g x))) ≤ B) :
    (1 - 2 * δ) * (Real.exp (-t * ε') * ∑ y, v y) ≤
      (∑ ω, P ω * ((alg ω).queries g).card) * B := by
  have key : ∀ a, ∑ y, (v y * Real.exp (-t * ε')) * Real.exp (-t * (slack d g a y -
      (f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε'))) ≤ B := by
    intro a
    refine le_trans (le_of_eq ?_) (hB a)
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [mul_assoc, ← Real.exp_add]
    congr 2
    ring
  have h := expected_queries_ge_exp_weights
    (Φ := fun g => univ.inf' univ_nonempty fun x => f x + g x) hd alg P hP hP1 hcorr hg
    (fun y => f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + ε')
    (fun y => min_dip_sensitive hd f g y hε0 hε) ht (fun y => v y * Real.exp (-t * ε'))
    (fun y => mul_nonneg (hv y) (Real.exp_pos _).le) key
  have hsum : ∑ y, v y * Real.exp (-t * ε') = Real.exp (-t * ε') * ∑ y, v y := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun y _ => mul_comm _ _
  rwa [hsum] at h

end Minimum

/-- If `c · exp (-t ε') ≤ E` for every `ε' > ε`, then also at `ε' = ε`. -/
theorem mul_exp_le_of_forall_gt {c E t ε : ℝ}
    (h : ∀ ε', ε < ε' → c * Real.exp (-t * ε') ≤ E) : c * Real.exp (-t * ε) ≤ E := by
  have hcont : Filter.Tendsto (fun ε' : ℝ => c * Real.exp (-t * ε'))
      (nhdsWithin ε (Set.Ioi ε)) (nhds (c * Real.exp (-t * ε))) :=
    (Continuous.tendsto (by fun_prop) ε).mono_left nhdsWithin_le_nhds
  exact le_of_tendsto hcont (eventually_nhdsWithin_of_forall fun ε' hε' => h ε' hε')

/-! ### A binary product landscape: every randomised algorithm is exponential -/

section Binary

/-- The number of excited sites is the unit Hamming distance from the all-`false`
configuration. -/
theorem count_true_eq_hamEnv (n : ℕ) (y : Fin n → Bool) :
    (∑ i, if y i then (1 : ℝ) else 0) = hamEnv (fun _ : Fin n => (1 : ℝ)) (fun _ => false) y := by
  unfold hamEnv
  refine Finset.sum_congr rfl fun i _ => ?_
  cases y i <;> simp

/-- The zero residual is admissible for every Hamming envelope with nonnegative constants. -/
theorem admissible_zero_hamEnv {n : ℕ} {c : ℝ} (hc : 0 ≤ c) :
    Admissible (hamEnv fun _ : Fin n => c) (fun _ : Fin n → Bool => (0 : ℝ)) := by
  intro x y
  have h : 0 ≤ hamEnv (fun _ : Fin n => c) x y := by
    unfold hamEnv
    refine Finset.sum_nonneg fun i _ => ?_
    split_ifs
    · exact le_rfl
    · exact hc
  simpa using h

/-- The minimum of the binary product landscape with zero residual is `0`. -/
theorem binary_min_eq_zero (n : ℕ) :
    (univ.inf' univ_nonempty fun x : Fin n → Bool =>
      (∑ i, if x i then (1 : ℝ) else 0) + (0 : ℝ)) = 0 := by
  apply le_antisymm
  · have h := Finset.inf'_le (fun x : Fin n → Bool => (∑ i, if x i then (1 : ℝ) else 0) + (0 : ℝ))
      (mem_univ (fun _ => false))
    simpa using h
  · apply Finset.le_inf'
    intro x _
    have h : 0 ≤ ∑ i, if x i then (1 : ℝ) else 0 := by
      refine Finset.sum_nonneg fun i _ => ?_
      split_ifs <;> norm_num
    linarith

/-- **Every randomised algorithm is exponential on the binary product landscape.**  Take `n`
two-state sites, known part `f x = #{i | x i = true}`, the weighted Hamming envelope with all
constants `2`, and let `alg ω` be a randomised algorithm that returns `min (f + g)` within
`ε / 2` with probability at least `1 - δ` for every admissible residual `g`.  Then on the zero
residual its expected number of evaluations is at least `(1 - 2δ) (6/5)^n 2^{-ε}` — the bound of
`binary_certificate_exponential` for certificates, up to the factor `1 - 2δ`. -/
theorem binary_randomized_exponential (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ} (hε0 : 0 ≤ ε)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => (2 : ℝ)) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        univ.inf' univ_nonempty fun x => (∑ i, if x i then (1 : ℝ) else 0) + g x| ≤ ε / 2),
        P ω) :
    (1 - 2 * δ) * (6 / 5 : ℝ) ^ n * Real.exp (-Real.log 2 * ε) ≤
      ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  have h2 : Real.exp (-Real.log 2) = 1 / 2 := by
    rw [Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have h4 : Real.exp (-Real.log 2 * 2) = 1 / 4 := by
    rw [show -Real.log 2 * 2 = -Real.log 2 + -Real.log 2 by ring, Real.exp_add, h2]
    norm_num
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => (2 : ℝ)) :=
    hamEnv_isEnvelope fun _ => by norm_num
  have hadm := admissible_zero_hamEnv (n := n) (c := 2) (by norm_num)
  -- the two partition sums
  have hS1 : ∑ y : Fin n → Bool, Real.exp (-Real.log 2 * ∑ i, if y i then (1 : ℝ) else 0) =
      (3 / 2) ^ n := by
    have h := sum_exp_hamEnv (σ := fun _ : Fin n => Bool) (fun _ => (1 : ℝ)) (Real.log 2)
      (fun _ => false)
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool, mul_one,
      h2] at h
    rw [← show (1 + ((2 : ℕ) - 1 : ℝ) * (1 / 2)) ^ n = (3 / 2 : ℝ) ^ n by norm_num, ← h]
    exact Finset.sum_congr rfl fun y _ => by rw [count_true_eq_hamEnv]
  have hS2 : ∀ a : Fin n → Bool,
      ∑ y, Real.exp (-Real.log 2 * hamEnv (fun _ : Fin n => (2 : ℝ)) a y) = (5 / 4) ^ n := by
    intro a
    have h := sum_exp_hamEnv (σ := fun _ : Fin n => Bool) (fun _ => (2 : ℝ)) (Real.log 2) a
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool, h4] at h
    rw [h]
    norm_num
  -- the bound for every `ε' > ε`
  have hmain : ∀ ε', ε < ε' →
      (1 - 2 * δ) * (6 / 5 : ℝ) ^ n * Real.exp (-Real.log 2 * ε') ≤
        ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
    intro ε' hε
    have key := expected_queries_ge_exp_weights_min hd
      (fun x : Fin n → Bool => ∑ i, if x i then (1 : ℝ) else 0) alg P hP hP1 hε0 hcorr hadm hε
      (Real.log_nonneg (by norm_num : (1 : ℝ) ≤ 2))
      (fun y => Real.exp (-Real.log 2 * ∑ i, if y i then (1 : ℝ) else 0))
      (fun y => (Real.exp_pos _).le) (B := (5 / 4) ^ n) (by
        intro a
        refine le_of_eq ?_
        rw [← hS2 a]
        refine Finset.sum_congr rfl fun y _ => ?_
        rw [← Real.exp_add, binary_min_eq_zero]
        congr 1
        unfold slack
        ring)
    rw [hS1] at key
    have e3 : (6 / 5 : ℝ) ^ n * (5 / 4) ^ n = (3 / 2) ^ n := by
      rw [← mul_pow]
      norm_num
    have hpos : (0 : ℝ) < (5 / 4) ^ n := by positivity
    have key' : ((1 - 2 * δ) * (6 / 5 : ℝ) ^ n * Real.exp (-Real.log 2 * ε')) * (5 / 4) ^ n ≤
        (∑ ω, P ω * ((alg ω).queries fun _ => 0).card) * (5 / 4) ^ n := by
      calc ((1 - 2 * δ) * (6 / 5 : ℝ) ^ n * Real.exp (-Real.log 2 * ε')) * (5 / 4) ^ n
          = (1 - 2 * δ) * (Real.exp (-Real.log 2 * ε') * ((6 / 5 : ℝ) ^ n * (5 / 4) ^ n)) := by
            ring
        _ = (1 - 2 * δ) * (Real.exp (-Real.log 2 * ε') * (3 / 2) ^ n) := by rw [e3]
        _ ≤ _ := key
    exact le_of_mul_le_mul_right key' hpos
  exact mul_exp_le_of_forall_gt hmain

end Binary

/-! ### The free energy -/

section Thermal

variable [Fintype X]

/-- The **soft gap** of `y`: `log Z(f + g) - log Z(f + U_y)`, where `U_y x = g y + d x y` is the
upper McShane envelope of the single evaluation at `y` (so `f x + U_y x = f x + g x + s(x, y)`).
It is `β` times the free-energy excess of the most pessimistic landscape consistent with the
value at `y`; as `β → ∞`, `softGap / β` tends to `min_x (gap x + s(x, y))`. -/
noncomputable def softGap (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (y : X) : ℝ :=
  Real.log (∑ x, Real.exp (-β * (f x + g x))) -
    Real.log (∑ x, Real.exp (-β * (f x + g x + slack d g x y)))

/-- The partition function of a dipped residual, exactly. -/
theorem sum_exp_dip (β : ℝ) (d : X → X → ℝ) (f g : X → ℝ) (y : X) (c : ℝ) :
    ∑ x, Real.exp (-β * (f x + dip d g y c x)) =
      ∑ x, Real.exp (-β * (f x + g x)) * Real.exp (β * max 0 (c - slack d g x y)) := by
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [dip_eq_sub, ← Real.exp_add]
  congr 1
  ring

variable [Nonempty X]

/-- The soft gap is nonnegative. -/
theorem softGap_nonneg {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ) {β : ℝ}
    (hβ : 0 ≤ β) (y : X) : 0 ≤ softGap β d f g y := by
  unfold softGap
  have hpos : 0 < ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hle : ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) ≤
      ∑ x, Real.exp (-β * (f x + g x)) := by
    refine Finset.sum_le_sum fun x _ => Real.exp_le_exp.mpr ?_
    have := slack_nonneg hg x y
    nlinarith
  linarith [Real.log_le_log hpos hle]

omit [Nonempty X] in
/-- The soft gap of `y` is at most `-log π(y) = β (E y - F)`, the free-energy gap of the
microstate `y`. -/
theorem softGap_le {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (β : ℝ) (y : X) :
    softGap β d f g y ≤ Real.log (∑ x, Real.exp (-β * (f x + g x))) + β * (f y + g y) := by
  unfold softGap
  have hs : slack d g y y = 0 := by
    have h := hd.self y
    have h' : slack d g y y = d y y - g y + g y := rfl
    linarith
  have hterm : Real.exp (-β * (f y + g y)) ≤
      ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) := by
    have h := Finset.single_le_sum (f := fun x => Real.exp (-β * (f x + g x + slack d g x y)))
      (fun x _ => (Real.exp_pos _).le) (mem_univ y)
    simpa [hs] using h
  have hlog := Real.log_le_log (Real.exp_pos _) hterm
  rw [Real.log_exp] at hlog
  linarith

/-- **Effect of a dip on the free energy.**  For `β ≥ 0` a dip of depth `c` at `y` raises
`log Z` by at least `β c - softGap y`. -/
theorem log_sum_exp_dip_ge (d : X → X → ℝ) (f g : X → ℝ) (y : X) (c : ℝ) {β : ℝ} (hβ : 0 ≤ β) :
    Real.log (∑ x, Real.exp (-β * (f x + g x))) + (β * c - softGap β d f g y) ≤
      Real.log (∑ x, Real.exp (-β * (f x + dip d g y c x))) := by
  have hpos : 0 < ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hle : Real.exp (β * c) * ∑ x, Real.exp (-β * (f x + g x + slack d g x y)) ≤
      ∑ x, Real.exp (-β * (f x + dip d g y c x)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun x _ => ?_
    rw [← Real.exp_add, dip_eq_sub]
    apply Real.exp_le_exp.mpr
    have h1 := mul_le_mul_of_nonneg_left (le_max_right 0 (c - slack d g x y)) hβ
    nlinarith
  have hlog := Real.log_le_log (mul_pos (Real.exp_pos _) hpos) hle
  rw [Real.log_mul (Real.exp_pos _).ne' hpos.ne', Real.log_exp] at hlog
  unfold softGap
  linarith

/-- A dip of depth `c` at `y` with `softGap y + ε < β c` is sensitive for `log Z` at level
`ε`. -/
theorem thermal_dip_sensitive (d : X → X → ℝ) (f g : X → ℝ) (y : X) {c β ε : ℝ} (hβ : 0 ≤ β)
    (hc : softGap β d f g y + ε < β * c) :
    ε < |Real.log (∑ x, Real.exp (-β * (f x + dip d g y c x))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x)))| := by
  have h := log_sum_exp_dip_ge d f g y c hβ
  have h1 : ε < Real.log (∑ x, Real.exp (-β * (f x + dip d g y c x))) -
      Real.log (∑ x, Real.exp (-β * (f x + g x))) := by linarith
  exact lt_of_lt_of_le h1 (le_abs_self _)

/-- **Deterministic lower bound for the free energy.**  If the output of the algorithm is within
`ε / 2` of `log Z(f + g)` for every admissible residual, then on every admissible instance the
queries reach within slack `c` of every point `y`, for every `c` with `softGap y + ε < β c`. -/
theorem thermal_queries_strict_cover {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : QueryAlgorithm X) {β ε : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) (y : X) {c : ℝ} (hc : softGap β d f g y + ε < β * c) :
    ∃ a ∈ alg.queries g, slack d g a y < c :=
  queries_cover_of_sensitive (Φ := fun g => Real.log (∑ x, Real.exp (-β * (f x + g x))))
    hd alg hcorr hg (thermal_dip_sensitive d f g y hβ hc)

variable {Ω : Type*} [Fintype Ω]

open Classical in
/-- **Randomised lower bound for the free energy (exponential weights).**  Let a randomised
algorithm return `log Z(f + g)` within `ε / 2` with probability at least `1 - δ` on every
admissible residual, and let `r y` be radii with `softGap y + ε < β · r y`.  Then for all
`t ≥ 0` and `v ≥ 0`,
`(1 - 2δ) ∑ v ≤ E|Q| · max_a ∑_y v y · exp (-t (s(a, y) - r y))`. -/
theorem thermal_expected_queries_ge {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {β ε δ : ℝ} (hβ : 0 ≤ β)
    (hcorr : ∀ g, Admissible d g → 1 - δ ≤ ∑ ω ∈ univ.filter (fun ω =>
      |(alg ω).output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2), P ω)
    {g : X → ℝ} (hg : Admissible d g) (r : X → ℝ)
    (hr : ∀ y, softGap β d f g y + ε < β * r y) {t : ℝ} (ht : 0 ≤ t) (v : X → ℝ)
    (hv : ∀ y, 0 ≤ v y) {B : ℝ}
    (hB : ∀ a, ∑ y, v y * Real.exp (-t * (slack d g a y - r y)) ≤ B) :
    (1 - 2 * δ) * ∑ y, v y ≤ (∑ ω, P ω * ((alg ω).queries g).card) * B :=
  expected_queries_ge_exp_weights
    (Φ := fun g => Real.log (∑ x, Real.exp (-β * (f x + g x)))) hd alg P hP hP1 hcorr hg r
    (fun y => thermal_dip_sensitive d f g y hβ (hr y)) ht v hv hB

end Thermal

/-! ### The free energy: deterministic algorithms yield certificates -/

section ThermalDet

variable {X : Type*} [Fintype X] [Nonempty X]

/-- Adding a constant `c` to the residual subtracts `β c` from `log Z`. -/
theorem log_sum_exp_add_const (f g : X → ℝ) (β c : ℝ) :
    Real.log (∑ x, Real.exp (-β * (f x + (g x + c)))) =
      Real.log (∑ x, Real.exp (-β * (f x + g x))) - β * c := by
  have hpos : 0 < ∑ x, Real.exp (-β * (f x + g x)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have h : ∑ x, Real.exp (-β * (f x + (g x + c))) =
      Real.exp (-(β * c)) * ∑ x, Real.exp (-β * (f x + g x)) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [← Real.exp_add]
    congr 1
    ring
  rw [h, Real.log_mul (Real.exp_pos _).ne' hpos.ne', Real.log_exp]
  ring

/-- At positive inverse temperature a correct algorithm for `log Z` evaluates the residual at
least once. -/
theorem thermal_queries_nonempty {d : X → X → ℝ} (f : X → ℝ) (alg : QueryAlgorithm X)
    {β ε : ℝ} (hβ : 0 < β)
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) : (alg.queries g).Nonempty := by
  by_contra hne
  rw [Finset.not_nonempty_iff_eq_empty] at hne
  have hg' : Admissible d (fun x => g x + (ε + 1) / β) := by
    intro x y
    have := hg x y
    linarith
  have hout := (alg.consistent g (fun x => g x + (ε + 1) / β) (by
    intro a ha
    rw [hne] at ha
    exact absurd ha (Finset.notMem_empty a))).2
  have c1 := abs_le.mp (hcorr g hg)
  have c2 := abs_le.mp (hcorr _ hg')
  rw [hout, log_sum_exp_add_const, mul_div_cancel₀ _ hβ.ne'] at c2
  linarith [c1.1, c2.2]

/-- **The queries of a correct deterministic algorithm for `log Z` form a free-energy
certificate.**  If the output is within `ε / 2` of `log Z(f + g)` for every admissible residual
(`β > 0`), then on every admissible instance the optimistic partition function of the evaluated
values (lower McShane envelope) is at most `exp ε` times the pessimistic one (upper envelope).
This is the hypothesis `hZ` of `Zhi_le_of_bracket`; hence every lower bound on free-energy
certificates (`mean_slack_le`, `card_ge_entropy`, `thermal_exp_weights` and their product forms)
is a lower bound on the number of evaluations of every deterministic algorithm. -/
theorem thermal_queries_bracket {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ)
    (alg : QueryAlgorithm X) {β ε : ℝ} (hβ : 0 < β)
    (hcorr : ∀ g, Admissible d g →
      |alg.output g - Real.log (∑ x, Real.exp (-β * (f x + g x)))| ≤ ε / 2)
    {g : X → ℝ} (hg : Admissible d g) :
    ∑ y, Real.exp (-β * (f y + lowerEnv d (alg.queries g)
        (thermal_queries_nonempty f alg hβ hcorr hg) g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + upperEnv d (alg.queries g)
        (thermal_queries_nonempty f alg hβ hcorr hg) g y)) := by
  have hA := thermal_queries_nonempty f alg hβ hcorr hg
  have hL : ∀ a ∈ alg.queries g, lowerEnv d (alg.queries g) hA g a = g a := fun a ha =>
    lowerEnv_eq_of_mem hd _ hA g (fun a _ b _ => hg a b) ha
  have hU : ∀ a ∈ alg.queries g, upperEnv d (alg.queries g) hA g a = g a := fun a ha =>
    upperEnv_eq_of_mem hd _ hA g (fun a _ b _ => hg a b) ha
  have hoL := (alg.consistent g _ hL).2
  have hoU := (alg.consistent g _ hU).2
  have cL := abs_le.mp (hcorr _ (lowerEnv_admissible hd _ hA g))
  have cU := abs_le.mp (hcorr _ (upperEnv_admissible hd _ hA g))
  rw [hoL] at cL
  rw [hoU] at cU
  have hposL : 0 < ∑ y, Real.exp (-β * (f y + lowerEnv d (alg.queries g) hA g y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hposU : 0 < ∑ y, Real.exp (-β * (f y + upperEnv d (alg.queries g) hA g y)) :=
    Finset.sum_pos (fun _ _ => Real.exp_pos _) univ_nonempty
  have hlog : Real.log (∑ y, Real.exp (-β * (f y + lowerEnv d (alg.queries g) hA g y))) ≤
      ε + Real.log (∑ y, Real.exp (-β * (f y + upperEnv d (alg.queries g) hA g y))) := by
    linarith [cL.2, cU.1]
  have h := Real.exp_le_exp.mpr hlog
  rwa [Real.exp_log hposL, Real.exp_add, Real.exp_log hposU] at h

end ThermalDet

/-! ### The cube at finite temperature: every randomised algorithm is exponential -/

section Cube

/-- The weighted Hamming envelope is symmetric. -/
theorem hamEnv_comm {ι : Type*} [Fintype ι] {σ : ι → Type*} [∀ i, DecidableEq (σ i)]
    (c : ι → ℝ) (x y : ∀ i, σ i) : hamEnv c x y = hamEnv c y x := by
  unfold hamEnv
  refine Finset.sum_congr rfl fun i _ => ?_
  by_cases h : x i = y i
  · rw [if_pos h, if_pos h.symm]
  · rw [if_neg h, if_neg (Ne.symm h)]

/-- The soft gap of every configuration of the uniform cube: `n log (2 / (1 + e^{-β}))`, here
with `n = 4m` and `e^{-β} = 1/16`. -/
theorem cube_softGap (m : ℕ) (y : Fin (4 * m) → Bool) :
    softGap (Real.log 16) (hamEnv fun _ : Fin (4 * m) => (1 : ℝ)) (fun _ => 0) (fun _ => 0) y =
      4 * m * Real.log (32 / 17) := by
  have h16 : Real.exp (-Real.log 16 * 1) = 1 / 16 := by
    rw [mul_one, Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have hZ : ∑ _x : Fin (4 * m) → Bool, Real.exp (-Real.log 16 * ((0 : ℝ) + 0)) =
      (2 : ℝ) ^ (4 * m) := by
    simp
  have hS : ∑ x : Fin (4 * m) → Bool, Real.exp (-Real.log 16 * ((0 : ℝ) + 0 +
      slack (hamEnv fun _ : Fin (4 * m) => (1 : ℝ)) (fun _ => 0) x y)) = (17 / 16 : ℝ) ^ (4 * m) := by
    have h := sum_exp_hamEnv (σ := fun _ : Fin (4 * m) => Bool) (fun _ => (1 : ℝ))
      (Real.log 16) y
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool, h16] at h
    rw [show (17 / 16 : ℝ) ^ (4 * m) = (1 + ((2 : ℕ) - 1 : ℝ) * (1 / 16)) ^ (4 * m) by norm_num,
      ← h]
    refine Finset.sum_congr rfl fun x _ => ?_
    congr 1
    unfold slack
    rw [hamEnv_comm]
    ring
  unfold softGap
  rw [hZ, hS, ← Real.log_div (by positivity) (by positivity), ← div_pow, Real.log_pow]
  push_cast
  norm_num

/-- **Every randomised algorithm for the free energy is exponential on the uniform cube.**  Take
`4m` two-state sites, zero known part, the unit Hamming envelope and `β = log 16`, and let
`alg ω` be a randomised algorithm that returns `log Z(g)` within `ε / 2` with probability at
least `1 - δ` for every admissible residual `g`, where `ε` is below
`m (log 16 - 4 log (32/17)) ≈ 0.2425 m` (an accuracy proportional to the number of sites is
allowed).  Then on the zero residual its expected number of evaluations is at least
`(1 - 2δ) (27/16)^m`.

Proof: `thermal_expected_queries_ge` with the radius `m` for every point (a dip of depth `m` at
`y` multiplies `Z` by at least `16^m (17/32)^{4m} > e^ε`), unit weights and `t = log 3`: a slack
ball of radius `m` has exponential-weight mass at most `3^m (4/3)^{4m}` among `16^m` points. -/
theorem cube_thermal_randomized_exponential (m : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin (4 * m) → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {ε δ : ℝ}
    (hε : ε + 4 * m * Real.log (32 / 17) < m * Real.log 16)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin (4 * m) => (1 : ℝ)) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-Real.log 16 * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * (27 / 16 : ℝ) ^ m ≤ ∑ ω, P ω * ((alg ω).queries fun _ => 0).card := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin (4 * m) => Bool) fun _ => (1 : ℝ)) :=
    hamEnv_isEnvelope fun _ => by norm_num
  have hadm := admissible_zero_hamEnv (n := 4 * m) (c := 1) (by norm_num)
  have hβ : (0 : ℝ) ≤ Real.log 16 := Real.log_nonneg (by norm_num)
  have h3 : Real.exp (-Real.log 3 * 1) = 1 / 3 := by
    rw [mul_one, Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have hB : ∀ a : Fin (4 * m) → Bool, ∑ y, (1 : ℝ) * Real.exp (-Real.log 3 *
      (slack (hamEnv fun _ : Fin (4 * m) => (1 : ℝ)) (fun _ => 0) a y - (m : ℝ))) =
        (256 / 27 : ℝ) ^ m := by
    intro a
    have h := sum_exp_hamEnv (σ := fun _ : Fin (4 * m) => Bool) (fun _ => (1 : ℝ))
      (Real.log 3) a
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool, h3] at h
    have hterm : ∀ y : Fin (4 * m) → Bool, (1 : ℝ) * Real.exp (-Real.log 3 *
        (slack (hamEnv fun _ : Fin (4 * m) => (1 : ℝ)) (fun _ => 0) a y - (m : ℝ))) =
          Real.exp (m * Real.log 3) *
            Real.exp (-Real.log 3 * hamEnv (fun _ : Fin (4 * m) => (1 : ℝ)) a y) := by
      intro y
      rw [one_mul, ← Real.exp_add]
      congr 1
      unfold slack
      ring
    rw [Finset.sum_congr rfl fun y _ => hterm y, ← Finset.mul_sum, h, Real.exp_nat_mul,
      Real.exp_log (by norm_num), pow_mul, ← mul_pow]
    norm_num
  have key := thermal_expected_queries_ge hd (fun _ : Fin (4 * m) → Bool => (0 : ℝ)) alg P hP hP1
    hβ hcorr hadm (fun _ => (m : ℝ)) (fun y => by
      rw [cube_softGap]
      linarith [mul_comm (Real.log 16) (m : ℝ)])
    (Real.log_nonneg (by norm_num : (1 : ℝ) ≤ 3)) (fun _ => (1 : ℝ)) (fun _ => zero_le_one)
    (B := (256 / 27 : ℝ) ^ m) fun a => (hB a).le
  have hcard : ∑ _y : Fin (4 * m) → Bool, (1 : ℝ) = (16 : ℝ) ^ m := by
    simp [pow_mul]
  rw [hcard] at key
  have e3 : (27 / 16 : ℝ) ^ m * (256 / 27) ^ m = 16 ^ m := by
    rw [← mul_pow]
    norm_num
  have hpos : (0 : ℝ) < (256 / 27) ^ m := by positivity
  rw [← e3, ← mul_assoc] at key
  exact le_of_mul_le_mul_right key hpos

/-- The soft gap of every configuration of the cube `Fin n → Bool` with zero known part, zero
residual and Hamming envelope constant `c`: `n · log (2 / (1 + e^{-βc}))`. -/
theorem cube_softGap_general (n : ℕ) (β c : ℝ) (y : Fin n → Bool) :
    softGap β (hamEnv fun _ : Fin n => c) (fun _ => 0) (fun _ => 0) y =
      n * Real.log (2 / (1 + Real.exp (-β * c))) := by
  have hZ : ∑ _x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0)) = (2 : ℝ) ^ n := by
    simp
  have hS : ∑ x : Fin n → Bool, Real.exp (-β * ((0 : ℝ) + 0 +
      slack (hamEnv fun _ : Fin n => c) (fun _ => 0) x y)) = (1 + Real.exp (-β * c)) ^ n := by
    have h := sum_exp_hamEnv (σ := fun _ : Fin n => Bool) (fun _ => c) β y
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool] at h
    rw [show (1 + Real.exp (-β * c)) ^ n = (1 + ((2 : ℕ) - 1 : ℝ) * Real.exp (-β * c)) ^ n by
      norm_num, ← h]
    refine Finset.sum_congr rfl fun x _ => ?_
    congr 1
    unfold slack
    rw [hamEnv_comm]
    ring
  unfold softGap
  rw [hZ, hS, ← Real.log_div (by positivity) (by positivity), ← div_pow, Real.log_pow]

/-- **Randomised lower bound for the free energy on the cube, general parameters.**  Take `n`
two-state sites, zero known part, the Hamming envelope with constant `c ≥ 0`, inverse
temperature `β ≥ 0`, and a randomised algorithm that returns `log Z(g)` within `ε / 2` with
probability at least `1 - δ` for every admissible residual.  If
`ε + n · log (2 / (1 + e^{-βc})) < β R`, then for every `t ≥ 0` the expected number of
evaluations on the zero residual is at least `(1 - 2δ) 2^n / (e^{tR} (1 + e^{-tc})^n)`.

With `R = ρ n c` and the best `t` the right-hand side is `(1 - 2δ) exp (n (log 2 - h(ρ)))`, the
inverse of the fraction of the cube inside a Hamming ball of radius `ρ n`; the condition on `R`
reads `ρ > (ε / n + log (2 / (1 + e^{-βc}))) / (βc)`, and such a `ρ` below `1/2` exists iff
`ε / n < log cosh (βc / 2)`. -/
theorem cube_thermal_randomized_bound (n : ℕ) {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm (Fin n → Bool)) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω)
    (hP1 : ∑ ω, P ω = 1) {β c ε δ R t : ℝ} (hβ : 0 ≤ β) (hc : 0 ≤ c) (ht : 0 ≤ t)
    (hR : ε + n * Real.log (2 / (1 + Real.exp (-β * c))) < β * R)
    (hcorr : ∀ g, Admissible (hamEnv fun _ : Fin n => c) g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g -
        Real.log (∑ x, Real.exp (-β * ((0 : ℝ) + g x)))| ≤ ε / 2), P ω) :
    (1 - 2 * δ) * 2 ^ n ≤ (∑ ω, P ω * ((alg ω).queries fun _ => 0).card) *
      (Real.exp (t * R) * (1 + Real.exp (-t * c)) ^ n) := by
  have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => c) :=
    hamEnv_isEnvelope fun _ => hc
  have hadm := admissible_zero_hamEnv (n := n) (c := c) hc
  have hB : ∀ a : Fin n → Bool, ∑ y, (1 : ℝ) * Real.exp (-t *
      (slack (hamEnv fun _ : Fin n => c) (fun _ => 0) a y - R)) =
        Real.exp (t * R) * (1 + Real.exp (-t * c)) ^ n := by
    intro a
    have h := sum_exp_hamEnv (σ := fun _ : Fin n => Bool) (fun _ => c) t a
    rw [Finset.prod_const, Finset.card_univ, Fintype.card_fin, Fintype.card_bool] at h
    have hterm : ∀ y : Fin n → Bool, (1 : ℝ) * Real.exp (-t *
        (slack (hamEnv fun _ : Fin n => c) (fun _ => 0) a y - R)) =
          Real.exp (t * R) * Real.exp (-t * hamEnv (fun _ : Fin n => c) a y) := by
      intro y
      rw [one_mul, ← Real.exp_add]
      congr 1
      unfold slack
      ring
    rw [Finset.sum_congr rfl fun y _ => hterm y, ← Finset.mul_sum, h]
    norm_num
  have key := thermal_expected_queries_ge hd (fun _ : Fin n → Bool => (0 : ℝ)) alg P hP hP1
    hβ hcorr hadm (fun _ => R) (fun y => by
      rw [cube_softGap_general]
      linarith)
    ht (fun _ => (1 : ℝ)) (fun _ => zero_le_one)
    (B := Real.exp (t * R) * (1 + Real.exp (-t * c)) ^ n) fun a => (hB a).le
  have hcard : ∑ _y : Fin n → Bool, (1 : ℝ) = (2 : ℝ) ^ n := by
    simp
  rwa [hcard] at key

end Cube

/-! ### The converse: spot-checking a hint -/

section SpotCheck

variable [Fintype X] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}

open Classical in
/-- The spot-check algorithm for the hint `g₀` and sample points `a 0, …, a (N-1)`: evaluate the
residual at the sample points; if all values agree with the hint, return `Φ g₀`; otherwise
evaluate everything and return the exact value. -/
noncomputable def spotCheck (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) {N : ℕ} (a : Fin N → X) :
    QueryAlgorithm X where
  queries := fun g => if ∀ k, g (a k) = g₀ (a k) then univ.image a else univ
  output := fun g => if ∀ k, g (a k) = g₀ (a k) then Φ g₀ else Φ g
  consistent := by
    intro g g' h
    by_cases hg : ∀ k, g (a k) = g₀ (a k)
    · simp only [if_pos hg] at h
      have hg' : ∀ k, g' (a k) = g₀ (a k) := fun k =>
        (h (a k) (Finset.mem_image_of_mem a (mem_univ k))).trans (hg k)
      simp only [if_pos hg, if_pos hg']
      exact ⟨trivial, trivial⟩
    · simp only [if_neg hg] at h
      have hgg : g' = g := funext fun x => h x (mem_univ x)
      rw [hgg]
      exact ⟨rfl, rfl⟩

open Classical in
/-- On the hint itself the spot-check algorithm makes at most `N` evaluations. -/
theorem spotCheck_card_le (Φ : (X → ℝ) → ℝ) (g₀ : X → ℝ) {N : ℕ} (a : Fin N → X) :
    ((spotCheck Φ g₀ a).queries g₀).card ≤ N := by
  have hq : (spotCheck Φ g₀ a).queries g₀ = univ.image a := by
    unfold spotCheck
    exact if_pos fun _ => rfl
  rw [hq]
  exact Finset.card_image_le.trans (by simp)

open Classical in
/-- **Spot-checking is sound.**  Let `q` be a probability vector on `X` such that every member
`g` of the class with `|Φ g - Φ g₀| > ε / 2` differs from the hint `g₀` on a set of
`q`-probability at least `p`, and let `(1 - p)^N ≤ δ`.  Then the spot-check algorithm with `N`
independent sample points drawn from `q` is within `ε / 2` of `Φ` with probability at least
`1 - δ` on every member of the class — and on the hint itself it makes at most `N` evaluations
(`spotCheck_card_le`; as soon as one sample disagrees it evaluates everything).  Together with
`expected_queries_ge_packing` this brackets the randomised query complexity at an instance,
among algorithms correct on the whole class, between fractional hitting numbers of the
difference sets of the alternatives distinguishable at level `ε` (lower bound) and at level
`ε / 2` (this algorithm), up to the factors `1 - 2δ` and `log (1/δ)`.  The change of level is
not harmless (it costs a factor `exp (Θ(ε))` on the cube); `hedgedSpotCheck_correct` in
`QueryRefinements.lean` removes it. -/
theorem spotCheck_correct (g₀ : X → ℝ) (N : ℕ) (q : X → ℝ) (hq : ∀ x, 0 ≤ q x)
    (hq1 : ∑ x, q x = 1) {ε δ p : ℝ} (hε : 0 ≤ ε) (hp1 : p ≤ 1)
    (hp : ∀ g, G g → ε / 2 < |Φ g - Φ g₀| → p ≤ ∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), q x)
    (hN : (1 - p) ^ N ≤ δ) (g : X → ℝ) (hg : G g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2), ∏ k, q (a k) := by
  have hδ : 0 ≤ δ := le_trans (pow_nonneg (by linarith) N) hN
  have htot : ∑ a : Fin N → X, ∏ k, q (a k) = 1 := by
    have h := Finset.sum_pow' (univ : Finset X) q N
    rw [hq1, one_pow] at h
    rw [h]
    refine Finset.sum_congr ?_ fun _ _ => rfl
    ext a
    simp
  have hnn : ∀ a : Fin N → X, 0 ≤ ∏ k, q (a k) := fun a => Finset.prod_nonneg fun k _ => hq (a k)
  by_cases hclose : |Φ g - Φ g₀| ≤ ε / 2
  · -- every sample is good
    have hall : univ.filter (fun a : Fin N → X =>
        |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2) = univ := by
      apply Finset.filter_true_of_mem
      intro a _
      by_cases hag : ∀ k, g (a k) = g₀ (a k)
      · have hout : (spotCheck Φ g₀ a).output g = Φ g₀ := by
          unfold spotCheck
          exact if_pos hag
        rw [hout, abs_sub_comm]
        exact hclose
      · have hout : (spotCheck Φ g₀ a).output g = Φ g := by
          unfold spotCheck
          exact if_neg hag
        rw [hout, sub_self, abs_zero]
        linarith
    rw [hall, htot]
    linarith
  · -- the alternative is distinguishable: the bad samples are those that miss its difference set
    have hfar : ε / 2 < |Φ g - Φ g₀| := not_le.mp hclose
    have hpD := hp g hg hfar
    have hsplit : ∑ x ∈ univ.filter (fun x => g x ≠ g₀ x), q x +
        ∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x = 1 := by
      rw [Finset.sum_filter_add_sum_filter_not, hq1]
    have hS0 : 0 ≤ ∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x :=
      Finset.sum_nonneg fun x _ => hq x
    have hbad : ∑ a ∈ univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)),
        ∏ k, q (a k) = (∑ x ∈ univ.filter (fun x => ¬ g x ≠ g₀ x), q x) ^ N := by
      rw [Finset.sum_pow']
      refine Finset.sum_congr ?_ fun _ _ => rfl
      ext a
      simp
    have hbadle : ∑ a ∈ univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)),
        ∏ k, q (a k) ≤ δ := by
      rw [hbad]
      exact le_trans (pow_le_pow_left₀ hS0 (by linarith) N) hN
    have hcover : (univ : Finset (Fin N → X)) ⊆
        univ.filter (fun a : Fin N → X => |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2) ∪
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)) := by
      intro a _
      by_cases hag : ∀ k, g (a k) = g₀ (a k)
      · exact Finset.mem_union_right _
          (Finset.mem_filter.mpr ⟨mem_univ a, fun k => not_not.mpr (hag k)⟩)
      · refine Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨mem_univ a, ?_⟩)
        have hout : (spotCheck Φ g₀ a).output g = Φ g := by
          unfold spotCheck
          exact if_neg hag
        rw [hout, sub_self, abs_zero]
        linarith
    have h1 : (1 : ℝ) ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
        |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2) ∪
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)), ∏ k, q (a k) := by
      rw [← htot]
      exact Finset.sum_le_sum_of_subset_of_nonneg hcover fun a _ _ => hnn a
    have h2 := Finset.sum_union_inter
      (s₁ := univ.filter (fun a : Fin N → X => |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2))
      (s₂ := univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)))
      (f := fun a => ∏ k, q (a k))
    have h3 : 0 ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
        |(spotCheck Φ g₀ a).output g - Φ g| ≤ ε / 2) ∩
          univ.filter (fun a : Fin N → X => ∀ k, ¬ g (a k) ≠ g₀ (a k)), ∏ k, q (a k) :=
      Finset.sum_nonneg fun a _ => hnn a
    linarith

end SpotCheck

/-! ### Spot-checking the minimum -/

section MinSpotCheck

variable {X : Type*} [Fintype X] [Nonempty X]

/-- **An alternative with a smaller minimum differs from the instance on a whole closed slack
ball.**  If `g'` is admissible and `min (f + g') < min (f + g) - η`, then for a minimiser `y` of
`f + g'` every point `a` within slack `gap y + η` of `y` has `g' a < g a`. -/
theorem lower_alternative_differs_on_ball {d : X → X → ℝ} (f : X → ℝ) {g g' : X → ℝ}
    (hg' : Admissible d g') {η : ℝ}
    (hlt : (univ.inf' univ_nonempty fun x => f x + g' x) <
      (univ.inf' univ_nonempty fun x => f x + g x) - η) :
    ∃ y, ∀ a, slack d g a y ≤ f y + g y - (univ.inf' univ_nonempty fun x => f x + g x) + η →
      g' a < g a := by
  obtain ⟨y, -, hy⟩ := Finset.exists_mem_eq_inf' univ_nonempty (fun x => f x + g' x)
  refine ⟨y, fun a ha => ?_⟩
  have h1 := hg' a y
  have hs : slack d g a y = d a y - g a + g y := rfl
  linarith

/-- **An alternative with a larger minimum differs from the instance at every near-minimiser.**
If `min (f + g') > min (f + g) + η`, then `g' x > g x` at every `x` with `gap x ≤ η`. -/
theorem higher_alternative_differs_on_minimisers (f : X → ℝ) {g g' : X → ℝ} {η : ℝ}
    (hgt : (univ.inf' univ_nonempty fun x => f x + g x) + η <
      univ.inf' univ_nonempty fun x => f x + g' x) (x : X)
    (hx : f x + g x - (univ.inf' univ_nonempty fun x => f x + g x) ≤ η) : g x < g' x := by
  have h1 : (univ.inf' univ_nonempty fun x => f x + g' x) ≤ f x + g' x :=
    Finset.inf'_le (fun x => f x + g' x) (mem_univ x)
  linarith

open Classical in
/-- **Spot-checking the minimum.**  Let `g₀` be the hint and `q` a probability vector such that
every closed slack ball `{a : s(a, y) ≤ gap y + ε/2}` and the set of `ε/2`-minimisers have
`q`-probability at least `p`.  If `(1 - p)^N ≤ δ`, the spot-check with `N` independent samples
of `q` returns `min (f + g)` within `ε / 2` with probability at least `1 - δ` on every admissible
residual `g`, and makes at most `N` evaluations on the hint.  With `q` an optimal fractional
cover of the balls at level `ε / 2` this is `N ≈ log (1/δ) · (N_frac(ε/2) + 1)`, against the lower
bound `(1 - 2δ) N_frac(ε)` of `expected_queries_ge`.  The two levels differ: `N_frac(ε/2)` can
exceed even the integral covering number at level `ε` without bound (uniform metric, `ε = 1.5 d`),
so this unhedged converse does not show that randomisation gains the integrality gap.  The
hedged version `min_hedgedSpotCheck_correct` (`QueryRefinements.lean`) removes the loss. -/
theorem min_spotCheck_correct {d : X → X → ℝ} (f g₀ : X → ℝ) (N : ℕ) (q : X → ℝ)
    (hq : ∀ x, 0 ≤ q x) (hq1 : ∑ x, q x = 1) {ε δ p : ℝ} (hε : 0 ≤ ε) (hp1 : p ≤ 1)
    (hball : ∀ y, p ≤ ∑ a ∈ univ.filter (fun a => slack d g₀ a y ≤
      f y + g₀ y - (univ.inf' univ_nonempty fun x => f x + g₀ x) + ε / 2), q a)
    (hmin : p ≤ ∑ x ∈ univ.filter (fun x =>
      f x + g₀ x - (univ.inf' univ_nonempty fun x => f x + g₀ x) ≤ ε / 2), q x)
    (hN : (1 - p) ^ N ≤ δ) (g : X → ℝ) (hg : Admissible d g) :
    1 - δ ≤ ∑ a ∈ univ.filter (fun a : Fin N → X =>
      |(spotCheck (fun g => univ.inf' univ_nonempty fun x => f x + g x) g₀ a).output g -
        univ.inf' univ_nonempty fun x => f x + g x| ≤ ε / 2), ∏ k, q (a k) := by
  refine spotCheck_correct (G := Admissible d)
    (Φ := fun g => univ.inf' univ_nonempty fun x => f x + g x) g₀ N q hq hq1 hε hp1
    (fun g hg hfar => ?_) hN g hg
  rcases lt_abs.mp hfar with hup | hdown
  · -- the alternative has a larger minimum: it differs at every near-minimiser
    refine le_trans hmin (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun x _ _ => hq x)
    intro x hx
    refine Finset.mem_filter.mpr ⟨mem_univ x, ?_⟩
    have h := higher_alternative_differs_on_minimisers f (g := g₀) (g' := g) (η := ε / 2)
      (by linarith) x (Finset.mem_filter.mp hx).2
    exact ne_of_gt h
  · -- the alternative has a smaller minimum: it differs on a closed slack ball
    obtain ⟨y, hy⟩ := lower_alternative_differs_on_ball (d := d) f (g := g₀) (g' := g) hg
      (η := ε / 2) (by linarith)
    refine le_trans (hball y) (Finset.sum_le_sum_of_subset_of_nonneg ?_ fun x _ _ => hq x)
    intro a ha
    exact Finset.mem_filter.mpr ⟨mem_univ a, ne_of_lt (hy a (Finset.mem_filter.mp ha).2)⟩

end MinSpotCheck

end MetricChain
