import Mathlib
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry

/-!
# Certificate complexity: hard instances, product landscapes, exponential lower bounds

Setting of `CertificationGeometry.lean`: a known part `f`, a residual `g` admissible for an
envelope `d`, energy `E = f + g`, and a finite set `A` of points at which `g` has been evaluated.
`A` is an `ε`-certificate (`IsCertificate d f g A hA ε`) when the incumbent `certUB` is within `ε`
of the certified lower bound `certLB`; by `isCertificate_iff_cover` this is a covering condition in
the slack quasi-metric.  This file asks **how many evaluations a certificate needs**.

Two general facts frame the question.  If the envelope vanishes on the diagonal, evaluating every
point gives an exact certificate (`full_evaluation_certificate`).  A single evaluation at `x₀` is
an `ε`-certificate iff `d x₀ y ≤ f y - f x₀ + ε` for all `y`, whatever the residual
(`single_evaluation_certificate_iff`); for `ε = 0` this says that `x₀` is a `d`-sharp minimum of
the known part.

## Part 1 — optimal certificates are as hard as dominating sets

For a finite simple graph `G` on `V` we build an instance on `Option V` (the vertices together
with one extra point `x⋆ = none`):

* the envelope `domEnv G` is `0` on the diagonal, `1` between adjacent vertices and `2` otherwise,
  in particular between `x⋆` and every vertex; it is a symmetric envelope with values in
  `{0, 1, 2}` (`domEnv_isEnvelope`, `domEnv_comm`, `domEnv_mem_values`);
* the known part `domF` is `0` at `x⋆` and `1` at every vertex;
* the residual is `g = 0`, which is admissible (`domEnv_admissible`).

`domCertificate_iff`: a set `A` is an exact (`ε = 0`) certificate iff it contains `x⋆` and the
vertices in `A` form a dominating set of `G`.  Consequently exact certificates with `k + 1`
evaluations exist iff dominating sets with `k` vertices exist (`domCertificate_exists_card_iff`,
`domCertificate_card`), and the minimal certificate size is the domination number plus one
(`domCertificate_min_card`).  Because the envelope only takes the values `0`, `1`, `2`, the same
characterisation holds for every tolerance `0 ≤ ε < 1` (`domCertificate_iff_of_lt_one`): here
approximate certificates with tolerance below `1` are exact.

The instance has `|V| + 1` points and is written down in polynomial time, and deciding whether a
graph has a dominating set with at most `k` vertices is NP-complete (Garey and Johnson, problem
GT2).  Hence computing a minimum certificate is NP-hard, even when the envelope, the known part
and the residual are completely known, the envelope is symmetric with values in `{0, 1, 2}`, the
known part is `0/1`-valued and the residual vanishes.  Only the correspondence between
certificates and dominating sets is formalised here; the complexity-theoretic statement itself
(machine model, encodings, reductions) is not.

## Part 2 — product landscapes: when does one evaluation suffice?

Configurations are `x : ∀ i, σ i` (finitely many sites `i` with finite state spaces `σ i`), the
known part is site-additive, `f x = ∑ i, φ i (x i)`, and the residual has bounded differences
`c i`, i.e. it is admissible for the weighted Hamming envelope
`hamEnv c x y = ∑ i, if x i = y i then 0 else c i` (`hamEnv_isEnvelope`).

One evaluation suffices iff every excitation is at least the envelope constant
(`product_single_certificate_iff`, with `product_single_certificate` for the direction used in
practice): the single evaluation at `x₀` is an exact certificate iff
`c i ≤ φ i s - φ i (x₀ i)` for every site `i` and every state `s ≠ x₀ i`.  By
`product_robust_optimal_iff` this is also exactly the condition under which `x₀` is optimal for
every admissible residual (for nonnegative constants `c i`).

## Part 3 — partition-function lower bound on product spaces

* `sum_exp_hamEnv` — the partition sum of the Hamming envelope around any point factorises:
  `∑ y, exp (-t * hamEnv c a y) = ∏ i, (1 + (|σ i| - 1) * exp (-t * c i))`.
* `partition_bound_hamming` — if the residual is `κ`-Lipschitz for `hamEnv c` and `Estar` is a
  lower bound on the energy, every `ε`-certificate `A` satisfies, for every `t ≥ 0`,
  `exp (-t ε) * ∑ y, exp (-t (E y - Estar)) ≤ |A| * ∏ i, (1 + (|σ i| - 1) * exp (-t (1 - κ) c i))`.
* `product_partition_bound` — for a site-additive known part with site-wise minimiser `x₀` and
  zero residual, both sides are products over the sites:
  `exp (-t ε) * ∏ i, ∑ s, exp (-t (φ i s - φ i (x₀ i)))`
    `≤ |A| * ∏ i, (1 + (|σ i| - 1) * exp (-t c i))`.
* `homogeneous_certificate_exponential`, `homogeneous_certificate_dichotomy` — for `n` identical
  sites: if some excitation costs less than the envelope constant, there are `ρ > 1` and `t ≥ 0`
  (depending on the site only) such that every `ε`-certificate has at least `exp (-t ε) * ρ ^ n`
  evaluations.  Together with Part 2: either one evaluation certifies for every `n`, or the
  number of evaluations grows exponentially in `n`.
* `binary_certificate_exponential` — a concrete witness with an explicit rate: for `n` two-state
  sites with excitation energy `1` and envelope constant `2`, every exact certificate has at
  least `(6/5)^n` evaluations, although the residual vanishes identically
  (`binary_full_certificate`: such certificates exist).
-/

namespace MetricChain

open Finset

/-! ### Two general facts: the largest and the smallest evaluation sets -/

section Extremes

variable {X : Type*} [Fintype X] [Nonempty X]

/-- **Evaluating everything certifies.**  If the envelope vanishes on the diagonal, the set of all
points is an exact certificate, for every known part and every residual.  In particular the
hypotheses of the lower bounds of this file are satisfiable. -/
theorem full_evaluation_certificate {d : X → X → ℝ} (hd : ∀ x, d x x = 0) (f g : X → ℝ) :
    IsCertificate d f g univ univ_nonempty 0 := by
  rw [isCertificate_iff_cover]
  intro y
  refine ⟨y, mem_univ y, ?_⟩
  have h1 : certUB f g univ univ_nonempty ≤ f y + g y :=
    Finset.inf'_le (fun a => f a + g a) (mem_univ y)
  unfold slack
  rw [hd y]
  linarith

/-- **One evaluation.**  The single evaluation at `x₀` is an `ε`-certificate iff
`d x₀ y ≤ f y - f x₀ + ε` for all `y`.  The condition does not involve the residual `g` at all;
for `ε = 0` it says that `x₀` is a `d`-sharp minimum of the known part (compare
`robust_certified_iff`). -/
theorem single_evaluation_certificate_iff (d : X → X → ℝ) (f g : X → ℝ) (x₀ : X) (ε : ℝ) :
    IsCertificate d f g {x₀} (singleton_nonempty x₀) ε ↔ ∀ y, d x₀ y ≤ f y - f x₀ + ε := by
  rw [isCertificate_iff_cover]
  have hUB : certUB f g {x₀} (singleton_nonempty x₀) = f x₀ + g x₀ :=
    Finset.inf'_singleton _
  rw [hUB]
  constructor
  · intro h y
    obtain ⟨a, ha, hay⟩ := h y
    rw [Finset.mem_singleton.mp ha] at hay
    unfold slack at hay
    linarith
  · intro h y
    refine ⟨x₀, Finset.mem_singleton_self x₀, ?_⟩
    have h1 := h y
    unfold slack
    linarith

end Extremes

/-! ### Part 1 — optimal certificates are as hard as dominating sets -/

section Domination

variable {V : Type*}

/-- The known part of the domination instance on `Option V`: `0` at the extra point `none` and
`1` at every vertex `some v`. -/
def domF : Option V → ℝ
  | none => 0
  | some _ => 1

variable [DecidableEq V]

/-- The domination envelope of a graph `G`, on `Option V`: `0` on the diagonal, `1` between two
adjacent vertices and `2` otherwise, in particular between the extra point `none` and every
vertex. -/
def domEnv (G : SimpleGraph V) [DecidableRel G.Adj] : Option V → Option V → ℝ
  | none, none => 0
  | some u, some v => if u = v then 0 else if G.Adj u v then 1 else 2
  | _, _ => 2

/-- The domination envelope between two vertices. -/
theorem domEnv_some_some (G : SimpleGraph V) [DecidableRel G.Adj] (u v : V) :
    domEnv G (some u) (some v) = if u = v then 0 else if G.Adj u v then 1 else 2 := rfl

/-- The extra point is at distance `2` from every vertex. -/
theorem domEnv_none_some (G : SimpleGraph V) [DecidableRel G.Adj] (v : V) :
    domEnv G none (some v) = 2 := rfl

/-- Every vertex is at distance `2` from the extra point. -/
theorem domEnv_some_none (G : SimpleGraph V) [DecidableRel G.Adj] (u : V) :
    domEnv G (some u) none = 2 := rfl

/-- The domination envelope vanishes on the diagonal. -/
theorem domEnv_self (G : SimpleGraph V) [DecidableRel G.Adj] (x : Option V) :
    domEnv G x x = 0 := by
  cases x <;> simp [domEnv]

/-- The domination envelope takes only the values `0`, `1` and `2`. -/
theorem domEnv_mem_values (G : SimpleGraph V) [DecidableRel G.Adj] (x y : Option V) :
    domEnv G x y = 0 ∨ domEnv G x y = 1 ∨ domEnv G x y = 2 := by
  cases x <;> cases y <;> simp only [domEnv] <;> (try split_ifs) <;> simp

/-- The domination envelope is nonnegative. -/
theorem domEnv_nonneg (G : SimpleGraph V) [DecidableRel G.Adj] (x y : Option V) :
    0 ≤ domEnv G x y := by
  cases x <;> cases y <;> simp only [domEnv] <;> (try split_ifs) <;> norm_num

/-- The domination envelope is at most `2`. -/
theorem domEnv_le_two (G : SimpleGraph V) [DecidableRel G.Adj] (x y : Option V) :
    domEnv G x y ≤ 2 := by
  cases x <;> cases y <;> simp only [domEnv] <;> (try split_ifs) <;> norm_num

/-- Distinct points are at distance at least `1` in the domination envelope. -/
theorem one_le_domEnv (G : SimpleGraph V) [DecidableRel G.Adj] {x y : Option V} (h : x ≠ y) :
    1 ≤ domEnv G x y := by
  cases x <;> cases y <;> simp only [domEnv] <;> (try split_ifs) <;> simp_all

/-- The domination envelope is symmetric. -/
theorem domEnv_comm (G : SimpleGraph V) [DecidableRel G.Adj] (x y : Option V) :
    domEnv G x y = domEnv G y x := by
  cases x <;> cases y <;> simp only [domEnv, eq_comm, G.adj_comm]

/-- A vertex `v` is within distance `1` of the vertex `u` iff `u` dominates `v`: they are equal
or adjacent. -/
theorem domEnv_some_some_le_one_iff (G : SimpleGraph V) [DecidableRel G.Adj] (u v : V) :
    domEnv G (some u) (some v) ≤ 1 ↔ u = v ∨ G.Adj u v := by
  rw [domEnv_some_some]
  split_ifs with h1 h2
  · simp [h1]
  · simp [h2]
  · simp [h1, h2]

/-- The domination envelope is an envelope: it vanishes on the diagonal, and the triangle
inequality holds because any two distinct points are at distance at least `1` and at most `2`. -/
theorem domEnv_isEnvelope (G : SimpleGraph V) [DecidableRel G.Adj] : IsEnvelope (domEnv G) where
  self := domEnv_self G
  triangle x y z := by
    by_cases hxy : x = y
    · subst hxy
      rw [domEnv_self]
      linarith
    · by_cases hyz : y = z
      · subst hyz
        rw [domEnv_self]
        linarith
      · have h1 := one_le_domEnv G hxy
        have h2 := one_le_domEnv G hyz
        have h3 := domEnv_le_two G x z
        linarith

/-- The zero residual is admissible for the domination envelope. -/
theorem domEnv_admissible (G : SimpleGraph V) [DecidableRel G.Adj] :
    Admissible (domEnv G) (fun _ => 0) := by
  intro x y
  have h := domEnv_nonneg G x y
  linarith

/-- **Certificates of the domination instance are dominating sets**, for every tolerance
`0 ≤ ε < 1`.  For the envelope `domEnv G`, the known part `domF` and the zero residual, a nonempty
set `A` of evaluated points is an `ε`-certificate iff it contains the extra point `none` and the
vertices in `A` dominate `G`: every vertex is in `A` or adjacent to a vertex in `A`.

Proof idea (`isCertificate_iff_cover`): the extra point has energy `0` and is at distance `2` from
everything else, so it can only be covered by itself; once it is evaluated the incumbent is `0`,
and a vertex `v` (energy `1`) is covered by `a` iff `domEnv G a (some v) ≤ 1 + ε`, i.e. (the
envelope takes the values `0`, `1`, `2` only) iff `a` is `v` or a neighbour of `v`. -/
theorem domCertificate_iff_of_lt_one [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (A : Finset (Option V)) (hA : A.Nonempty) {ε : ℝ} (hε0 : 0 ≤ ε) (hε1 : ε < 1) :
    IsCertificate (domEnv G) domF (fun _ => 0) A hA ε ↔
      none ∈ A ∧ ∀ v, ∃ u, some u ∈ A ∧ (u = v ∨ G.Adj u v) := by
  rw [isCertificate_iff_cover]
  constructor
  · intro h
    have hUB0 : 0 ≤ certUB domF (fun _ => 0) A hA := by
      apply Finset.le_inf'
      intro a _
      cases a <;> simp [domF]
    have hnone : none ∈ A := by
      by_contra hn
      have hUB1 : 1 ≤ certUB domF (fun _ => 0) A hA := by
        apply Finset.le_inf'
        intro a ha
        cases a with
        | none => exact absurd ha hn
        | some u => simp [domF]
      obtain ⟨a, _, hay⟩ := h none
      have h0 := domEnv_nonneg G a none
      simp only [slack, domF] at hay
      linarith
    refine ⟨hnone, fun v => ?_⟩
    obtain ⟨a, ha, hay⟩ := h (some v)
    simp only [slack, domF] at hay
    cases a with
    | none =>
      rw [domEnv_none_some] at hay
      linarith
    | some u =>
      refine ⟨u, ha, (domEnv_some_some_le_one_iff G u v).mp ?_⟩
      rcases domEnv_mem_values G (some u) (some v) with h1 | h1 | h1 <;> linarith
  · rintro ⟨hnone, hdom⟩
    have hUB : certUB domF (fun _ => 0) A hA ≤ 0 := by
      have h := Finset.inf'_le (fun a => domF a + (fun _ : Option V => (0 : ℝ)) a) hnone
      simpa [certUB, domF] using h
    intro y
    cases y with
    | none =>
      refine ⟨none, hnone, ?_⟩
      simp only [slack, domF, domEnv_self]
      linarith
    | some v =>
      obtain ⟨u, hu, huv⟩ := hdom v
      refine ⟨some u, hu, ?_⟩
      have h1 := (domEnv_some_some_le_one_iff G u v).mpr huv
      simp only [slack, domF]
      linarith

/-- **Exact certificates of the domination instance are dominating sets.**  For the envelope
`domEnv G`, the known part `domF` and the zero residual, a nonempty set `A` of evaluated points is
an exact certificate iff it contains the extra point `none` and the vertices in `A` dominate `G`:
every vertex is in `A` or adjacent to a vertex in `A`.  (The case `ε = 0` of
`domCertificate_iff_of_lt_one`.) -/
theorem domCertificate_iff [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (A : Finset (Option V)) (hA : A.Nonempty) :
    IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 ↔
      none ∈ A ∧ ∀ v, ∃ u, some u ∈ A ∧ (u = v ∨ G.Adj u v) :=
  domCertificate_iff_of_lt_one G A hA le_rfl zero_lt_one

/-- **Certificate sizes are dominating-set sizes shifted by one.**  The domination instance has
an exact certificate with exactly `k + 1` evaluations iff `G` has a dominating set with exactly
`k` vertices: erase, respectively insert, the extra point. -/
theorem domCertificate_exists_card_iff [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]
    (k : ℕ) :
    (∃ (A : Finset (Option V)) (hA : A.Nonempty),
        IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 ∧ A.card = k + 1) ↔
      ∃ S : Finset V, (∀ v, ∃ u ∈ S, u = v ∨ G.Adj u v) ∧ S.card = k := by
  constructor
  · rintro ⟨A, hA, hcert, hcard⟩
    obtain ⟨hnone, hdom⟩ := (domCertificate_iff G A hA).mp hcert
    refine ⟨A.eraseNone, fun v => ?_, ?_⟩
    · obtain ⟨u, hu, huv⟩ := hdom v
      exact ⟨u, Finset.mem_eraseNone.mpr hu, huv⟩
    · rw [Finset.card_eraseNone_of_mem hnone, hcard, Nat.add_sub_cancel]
  · rintro ⟨S, hS, hcard⟩
    refine ⟨Finset.insertNone S, Finset.insertNone_nonempty, ?_, ?_⟩
    · rw [domCertificate_iff]
      refine ⟨Finset.none_mem_insertNone, fun v => ?_⟩
      obtain ⟨u, hu, huv⟩ := hS v
      exact ⟨u, Finset.some_mem_insertNone.mpr hu, huv⟩
    · rw [Finset.card_insertNone, hcard]

/-- **Cardinality form of the reduction.**  For every exact certificate `A` of the domination
problem `(domEnv G, domF, 0)` there is a dominating set `S` of `G` with `S.card + 1 ≤ A.card`,
and conversely every dominating set `S` yields an exact certificate with `S.card + 1`
evaluations.  Hence the minimal certificate size is the domination number plus one
(`domCertificate_min_card`), and computing a minimum certificate is NP-hard, because minimum
dominating set is.  (The complexity-theoretic statement itself is not formalised.) -/
theorem domCertificate_card [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] :
    (∀ (A : Finset (Option V)) (hA : A.Nonempty),
        IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 →
          ∃ S : Finset V, (∀ v, ∃ u ∈ S, u = v ∨ G.Adj u v) ∧ S.card + 1 ≤ A.card) ∧
      ∀ S : Finset V, (∀ v, ∃ u ∈ S, u = v ∨ G.Adj u v) →
        ∃ (A : Finset (Option V)) (hA : A.Nonempty),
          IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 ∧ A.card = S.card + 1 := by
  constructor
  · intro A hA hcert
    obtain ⟨hnone, hdom⟩ := (domCertificate_iff G A hA).mp hcert
    refine ⟨A.eraseNone, fun v => ?_, ?_⟩
    · obtain ⟨u, hu, huv⟩ := hdom v
      exact ⟨u, Finset.mem_eraseNone.mpr hu, huv⟩
    · have hpos : 0 < A.card := Finset.card_pos.mpr hA
      rw [Finset.card_eraseNone_of_mem hnone]
      omega
  · intro S hS
    exact (domCertificate_exists_card_iff G S.card).mpr ⟨S, hS, rfl⟩

/-- **Minimal certificate size = domination number + 1.**  The least number of evaluations in an
exact certificate of the domination instance equals the least cardinality of a dominating set of
`G`, plus one.  (Both sets of cardinalities are nonempty: all vertices together dominate.) -/
theorem domCertificate_min_card [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] :
    sInf {m : ℕ | ∃ (A : Finset (Option V)) (hA : A.Nonempty),
        IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 ∧ A.card = m} =
      sInf {k : ℕ | ∃ S : Finset V, (∀ v, ∃ u ∈ S, u = v ∨ G.Adj u v) ∧ S.card = k} + 1 := by
  set D : Set ℕ := {k | ∃ S : Finset V, (∀ v, ∃ u ∈ S, u = v ∨ G.Adj u v) ∧ S.card = k}
  set M : Set ℕ := {m | ∃ (A : Finset (Option V)) (hA : A.Nonempty),
    IsCertificate (domEnv G) domF (fun _ => 0) A hA 0 ∧ A.card = m}
  have hD : D.Nonempty :=
    ⟨(univ : Finset V).card, univ, fun v => ⟨v, mem_univ v, Or.inl rfl⟩, rfl⟩
  have hDM : ∀ k, k ∈ D → k + 1 ∈ M := fun k hk => (domCertificate_exists_card_iff G k).mpr hk
  have hMD : ∀ m, m ∈ M → ∃ k ∈ D, m = k + 1 := by
    rintro m ⟨A, hA, hcert, hcard⟩
    have hpos : 0 < A.card := Finset.card_pos.mpr hA
    exact ⟨m - 1, (domCertificate_exists_card_iff G (m - 1)).mp ⟨A, hA, hcert, by omega⟩,
      by omega⟩
  apply le_antisymm
  · exact Nat.sInf_le (hDM _ (Nat.sInf_mem hD))
  · have hM : M.Nonempty := ⟨_, hDM _ (Nat.sInf_mem hD)⟩
    obtain ⟨k, hk, hmk⟩ := hMD _ (Nat.sInf_mem hM)
    rw [hmk]
    exact Nat.succ_le_succ (Nat.sInf_le hk)

end Domination

/-! ### Part 2 — product landscapes: when does one evaluation suffice? -/

section Product

variable {ι : Type*} [Fintype ι] {σ : ι → Type*} [∀ i, DecidableEq (σ i)]

/-- The weighted Hamming envelope with site constants `c`: the sum of `c i` over the sites at
which the two configurations differ.  Every residual with bounded differences `c i` is admissible
for it (`admissible_of_single_site`). -/
def hamEnv (c : ι → ℝ) (x y : ∀ i, σ i) : ℝ := ∑ i, if x i = y i then 0 else c i

/-- The weighted Hamming envelope is the site-additive envelope of the discrete envelopes with
oscillations `c i`. -/
theorem hamEnv_eq_siteEnvelope (c : ι → ℝ) :
    hamEnv (σ := σ) c = siteEnvelope fun i => discreteEnvelope (c i) := rfl

/-- For nonnegative site constants the weighted Hamming envelope is an envelope. -/
theorem hamEnv_isEnvelope {c : ι → ℝ} (hc : ∀ i, 0 ≤ c i) : IsEnvelope (hamEnv (σ := σ) c) :=
  siteEnvelope_isEnvelope _ fun i => discreteEnvelope_isEnvelope (hc i)

/-- Scaling the weighted Hamming envelope scales the site constants. -/
theorem hamEnv_mul (r : ℝ) (c : ι → ℝ) (x y : ∀ i, σ i) :
    r * hamEnv c x y = hamEnv (fun i => r * c i) x y := by
  unfold hamEnv
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  split_ifs <;> simp

/-- The weighted Hamming envelope between a configuration and a single-site modification of it
is the constant of that site (or `0` if the state is unchanged). -/
theorem hamEnv_update [DecidableEq ι] (c : ι → ℝ) (x : ∀ i, σ i) (i : ι) (s : σ i) :
    hamEnv c x (Function.update x i s) = if x i = s then 0 else c i := by
  unfold hamEnv
  rw [Finset.sum_eq_single i]
  · rw [Function.update_self]
  · intro j _ hji
    rw [Function.update_of_ne hji, if_pos rfl]
  · intro h
    exact absurd (Finset.mem_univ i) h

/-- **Sharp minima of product landscapes.**  For a site-additive function `∑ i, φ i (x i)`, the
configuration `x₀` is a sharp minimum for the weighted Hamming envelope iff every single-site
excitation costs at least the constant of its site.  (Necessity: test the single-site
modifications of `x₀`; sufficiency: add up the site-wise inequalities.) -/
theorem hamEnv_le_gap_iff (c : ι → ℝ) (φ : ∀ i, σ i → ℝ) (x₀ : ∀ i, σ i) :
    (∀ y, hamEnv c x₀ y ≤ ∑ i, φ i (y i) - ∑ i, φ i (x₀ i)) ↔
      ∀ i s, s ≠ x₀ i → c i ≤ φ i s - φ i (x₀ i) := by
  classical
  constructor
  · intro h i s hs
    have h1 := h (Function.update x₀ i s)
    rw [hamEnv_update, if_neg (Ne.symm hs), ← Finset.sum_sub_distrib,
      Finset.sum_eq_single i] at h1
    · rwa [Function.update_self] at h1
    · intro j _ hji
      rw [Function.update_of_ne hji, sub_self]
    · intro hi
      exact absurd (Finset.mem_univ i) hi
  · intro h y
    unfold hamEnv
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun i _ => ?_
    split_ifs with hi
    · rw [hi, sub_self]
    · exact h i (y i) (Ne.symm hi)

/-- **Robust optimality on product landscapes.**  For nonnegative site constants, `x₀` minimises
`∑ i, φ i (x i) + g x` for *every* residual `g` admissible for `hamEnv c` iff every single-site
excitation costs at least the constant of its site. -/
theorem product_robust_optimal_iff {c : ι → ℝ} (hc : ∀ i, 0 ≤ c i) (φ : ∀ i, σ i → ℝ)
    (x₀ : ∀ i, σ i) :
    (∀ g, Admissible (hamEnv c) g → ∀ y, ∑ i, φ i (x₀ i) + g x₀ ≤ ∑ i, φ i (y i) + g y) ↔
      ∀ i s, s ≠ x₀ i → c i ≤ φ i s - φ i (x₀ i) := by
  rw [← hamEnv_le_gap_iff]
  exact robust_certified_iff (hamEnv_isEnvelope hc) (fun x => ∑ i, φ i (x i)) x₀

variable [DecidableEq ι] [∀ i, Fintype (σ i)]

/-- **One evaluation suffices iff every excitation is at least the envelope constant.**  On a
product landscape with known part `∑ i, φ i (x i)`, weighted Hamming envelope `hamEnv c` and zero
residual, the single evaluation at `x₀` is an exact certificate iff `c i ≤ φ i s - φ i (x₀ i)`
for every site `i` and every state `s ≠ x₀ i`.  (By `single_evaluation_certificate_iff` the same
criterion holds verbatim for every residual in place of `0`.) -/
theorem product_single_certificate_iff [∀ i, Nonempty (σ i)] (c : ι → ℝ) (φ : ∀ i, σ i → ℝ)
    (x₀ : ∀ i, σ i) :
    IsCertificate (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun _ => 0) {x₀}
        (singleton_nonempty x₀) 0 ↔
      ∀ i s, s ≠ x₀ i → c i ≤ φ i s - φ i (x₀ i) := by
  rw [single_evaluation_certificate_iff]
  simp only [add_zero]
  exact hamEnv_le_gap_iff c φ x₀

/-- **One evaluation certifies a product landscape with large excitations.**  If every
single-site excitation of `x₀` costs at least the envelope constant of its site, the single
evaluation at `x₀` is an exact certificate.  The criterion does not involve the residual, so the
same evaluation certifies `x₀` for every residual with bounded differences `c`
(`single_evaluation_certificate_iff`, `product_robust_optimal_iff`). -/
theorem product_single_certificate [∀ i, Nonempty (σ i)] (c : ι → ℝ) (φ : ∀ i, σ i → ℝ)
    (x₀ : ∀ i, σ i) (h : ∀ i s, s ≠ x₀ i → c i ≤ φ i s - φ i (x₀ i)) :
    IsCertificate (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun _ => 0) {x₀}
      (singleton_nonempty x₀) 0 :=
  (product_single_certificate_iff c φ x₀).mpr h

/-! ### Part 3 — partition-function lower bound on product spaces -/

/-- **The partition sum of the Hamming envelope factorises.**  Around every configuration `a`,
`∑ y, exp (-t * hamEnv c a y) = ∏ i, (1 + (|σ i| - 1) * exp (-t * c i))`: at each site the state
`a i` contributes `1` and each of the other `|σ i| - 1` states contributes `exp (-t * c i)`. -/
theorem sum_exp_hamEnv (c : ι → ℝ) (t : ℝ) (a : ∀ i, σ i) :
    ∑ y, Real.exp (-t * hamEnv c a y) =
      ∏ i, (1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * c i)) := by
  have hsite : ∀ i, ∑ s, Real.exp (-t * if a i = s then 0 else c i) =
      1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * c i) := by
    intro i
    have hterm : ∀ s : σ i, Real.exp (-t * if a i = s then 0 else c i) =
        Real.exp (-t * c i) + if a i = s then 1 - Real.exp (-t * c i) else 0 := by
      intro s
      split_ifs <;> simp
    simp only [hterm, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
      Finset.sum_ite_eq, Finset.mem_univ, if_true, nsmul_eq_mul]
    ring
  calc ∑ y, Real.exp (-t * hamEnv c a y)
      = ∑ y : ∀ i, σ i, ∏ i, Real.exp (-t * if a i = y i then 0 else c i) := by
        refine Finset.sum_congr rfl fun y _ => ?_
        unfold hamEnv
        rw [Finset.mul_sum, Real.exp_sum]
    _ = ∏ i, ∑ s, Real.exp (-t * if a i = s then 0 else c i) :=
        (Fintype.prod_sum fun i s => Real.exp (-t * if a i = s then 0 else c i)).symm
    _ = ∏ i, (1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * c i)) :=
        Finset.prod_congr rfl fun i _ => hsite i

/-- **Partition-function bound for the weighted Hamming envelope.**  Let the residual `g` be
`κ`-Lipschitz for `hamEnv c` and let `Estar` be a lower bound on the energy `f + g` (`f` is
arbitrary, not necessarily site-additive).  Then for every `t ≥ 0` every `ε`-certificate `A`
satisfies

  `exp (-t ε) * ∑ y, exp (-t (E y - Estar)) ≤ |A| * ∏ i, (1 + (|σ i| - 1) * exp (-t (1 - κ) c i))`.

The slack dominates `(1 - κ) * hamEnv c = hamEnv ((1 - κ) c)` (`slack_ge_of_lipschitz`), whose
partition sum is the product on the right (`sum_exp_hamEnv`); the claim is then
`partition_bound_certificate`.  The bound is informative in the regime `κ < 1`, `0 < c i`, but
neither sign condition is needed for its validity. -/
theorem partition_bound_hamming [∀ i, Nonempty (σ i)] {c : ι → ℝ} {f g : (∀ i, σ i) → ℝ}
    {κ : ℝ} (hgκ : ∀ x y, g x - g y ≤ κ * hamEnv c x y) {A : Finset (∀ i, σ i)}
    {hA : A.Nonempty} {ε Estar t : ℝ} (ht : 0 ≤ t) (hE : ∀ y, Estar ≤ f y + g y)
    (hcert : IsCertificate (hamEnv c) f g A hA ε) :
    Real.exp (-t * ε) * ∑ y, Real.exp (-t * (f y + g y - Estar)) ≤
      A.card * ∏ i, (1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * ((1 - κ) * c i))) := by
  refine partition_bound_certificate ht hE hcert fun a => ?_
  rw [← sum_exp_hamEnv (fun i => (1 - κ) * c i) t a]
  refine Finset.sum_le_sum fun y _ => Real.exp_le_exp.mpr ?_
  have h1 := slack_ge_of_lipschitz hgκ a y
  rw [hamEnv_mul] at h1
  exact mul_le_mul_of_nonpos_left h1 (by linarith)

/-- **Partition-function bound on product landscapes.**  For the site-additive known part
`∑ i, φ i (x i)` with site-wise minimiser `x₀`, the zero residual and the envelope `hamEnv c`,
every `ε`-certificate `A` satisfies, for every `t ≥ 0`,

  `exp (-t ε) * ∏ i, ∑ s, exp (-t (φ i s - φ i (x₀ i)))`
    `≤ |A| * ∏ i, (1 + (|σ i| - 1) * exp (-t c i))`.

Both sides are products over the sites: on the left the single-site partition functions of the
known landscape (measured from the ground state), on the right those of the Hamming envelope.
Every site at which the former exceeds the latter multiplies the number of evaluations. -/
theorem product_partition_bound [∀ i, Nonempty (σ i)] (c : ι → ℝ) (φ : ∀ i, σ i → ℝ)
    (x₀ : ∀ i, σ i) (hx₀ : ∀ i s, φ i (x₀ i) ≤ φ i s) {A : Finset (∀ i, σ i)}
    {hA : A.Nonempty} {ε t : ℝ} (ht : 0 ≤ t)
    (hcert : IsCertificate (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun _ => 0) A hA ε) :
    Real.exp (-t * ε) * ∏ i, ∑ s, Real.exp (-t * (φ i s - φ i (x₀ i))) ≤
      A.card * ∏ i, (1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * c i)) := by
  have hg : ∀ x y : ∀ i, σ i,
      (fun _ : ∀ i, σ i => (0 : ℝ)) x - (fun _ : ∀ i, σ i => (0 : ℝ)) y ≤ 0 * hamEnv c x y := by
    intro x y
    simp
  have hE : ∀ y : ∀ i, σ i, ∑ i, φ i (x₀ i) ≤
      (fun x : ∀ i, σ i => ∑ i, φ i (x i)) y + (fun _ : ∀ i, σ i => (0 : ℝ)) y := by
    intro y
    simpa using Finset.sum_le_sum fun i _ => hx₀ i (y i)
  have h := partition_bound_hamming hg ht hE hcert
  have hL : ∑ y : ∀ i, σ i, Real.exp (-t * (∑ i, φ i (y i) + 0 - ∑ i, φ i (x₀ i))) =
      ∏ i, ∑ s, Real.exp (-t * (φ i s - φ i (x₀ i))) := by
    rw [Fintype.prod_sum]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [← Real.exp_sum, ← Finset.mul_sum, Finset.sum_sub_distrib, add_zero]
  have hR : ∀ i, (1 - (0 : ℝ)) * c i = c i := fun i => by ring
  simp only [hR] at h
  rw [← hL]
  exact h

/-! ### Homogeneous product landscapes: one evaluation or exponentially many -/

/-- **A site with a cheap excitation beats its envelope at a suitable inverse temperature.**  If
some excitation `s₁ ≠ s₀` of a site costs less than the envelope constant, `φ s₁ - φ s₀ < c`,
there is `t ≥ 0` at which the partition function of the site, measured from `s₀`, exceeds that of
the envelope: `1 + (|S| - 1) * exp (-t * c) < ∑ s, exp (-t * (φ s - φ s₀))`.  (Take
`t = log |S| / (c - (φ s₁ - φ s₀))`; then the term of `s₁` alone equals `|S| * exp (-t * c)`.) -/
theorem site_partition_lt_of_excitation_lt {S : Type*} [Fintype S] (φ : S → ℝ) (c : ℝ)
    {s₀ s₁ : S} (hne : s₁ ≠ s₀) (hfail : φ s₁ - φ s₀ < c) :
    ∃ t : ℝ, 0 ≤ t ∧ 1 + ((Fintype.card S : ℝ) - 1) * Real.exp (-t * c) <
      ∑ s, Real.exp (-t * (φ s - φ s₀)) := by
  classical
  have hk1 : (1 : ℝ) ≤ (Fintype.card S : ℝ) := by
    exact_mod_cast Fintype.card_pos_iff.mpr ⟨s₀⟩
  have hδ : 0 < c - (φ s₁ - φ s₀) := by linarith
  refine ⟨Real.log (Fintype.card S) / (c - (φ s₁ - φ s₀)),
    div_nonneg (Real.log_nonneg hk1) hδ.le, ?_⟩
  have hexp : Real.exp (Real.log (Fintype.card S) / (c - (φ s₁ - φ s₀)) *
      (c - (φ s₁ - φ s₀))) = (Fintype.card S : ℝ) := by
    rw [div_mul_cancel₀ _ hδ.ne', Real.exp_log (by linarith)]
  generalize Real.log (Fintype.card S) / (c - (φ s₁ - φ s₀)) = t at hexp ⊢
  have h1 : Real.exp (-t * (φ s₁ - φ s₀)) = (Fintype.card S : ℝ) * Real.exp (-t * c) := by
    rw [← hexp, ← Real.exp_add]
    congr 1
    ring
  have hpair : Real.exp (-t * (φ s₀ - φ s₀)) + Real.exp (-t * (φ s₁ - φ s₀)) ≤
      ∑ s, Real.exp (-t * (φ s - φ s₀)) := by
    have h := Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ ({s₀, s₁} : Finset S))
      (f := fun s => Real.exp (-t * (φ s - φ s₀))) fun _ _ _ => (Real.exp_pos _).le
    rwa [Finset.sum_pair hne.symm] at h
  rw [sub_self, mul_zero, Real.exp_zero, h1] at hpair
  have hpos := Real.exp_pos (-t * c)
  have hexpand : ((Fintype.card S : ℝ) - 1) * Real.exp (-t * c) =
      (Fintype.card S : ℝ) * Real.exp (-t * c) - Real.exp (-t * c) := by ring
  linarith

/-- **Cheap excitations force exponentially many evaluations.**  Consider `n` identical sites
with state space `S`, site energy `φ` minimised at `s₀`, envelope constant `c` and zero residual.
If some excitation costs less than the envelope constant, `φ s₁ - φ s₀ < c` with `s₁ ≠ s₀`, there
are `ρ > 1` and `t ≥ 0`, depending on the site only, such that for every number of sites `n` and
every tolerance `ε`, every `ε`-certificate has at least `exp (-t ε) * ρ ^ n` evaluations.

Here `ρ` is the ratio of the two single-site partition functions of `product_partition_bound` at
the inverse temperature `t` provided by `site_partition_lt_of_excitation_lt`. -/
theorem homogeneous_certificate_exponential {S : Type*} [Fintype S] [DecidableEq S] [Nonempty S]
    (φ : S → ℝ) (c : ℝ) {s₀ s₁ : S} (hs₀ : ∀ s, φ s₀ ≤ φ s) (hne : s₁ ≠ s₀)
    (hfail : φ s₁ - φ s₀ < c) :
    ∃ ρ t : ℝ, 1 < ρ ∧ 0 ≤ t ∧
      ∀ (n : ℕ) (A : Finset (Fin n → S)) (hA : A.Nonempty) (ε : ℝ),
        IsCertificate (hamEnv fun _ : Fin n => c) (fun x => ∑ i, φ (x i)) (fun _ => 0) A hA ε →
          Real.exp (-t * ε) * ρ ^ n ≤ A.card := by
  obtain ⟨t, ht0, hlt⟩ := site_partition_lt_of_excitation_lt φ c hne hfail
  have hBpos : 0 < 1 + ((Fintype.card S : ℝ) - 1) * Real.exp (-t * c) := by
    have hk1 : (1 : ℝ) ≤ (Fintype.card S : ℝ) := by exact_mod_cast Fintype.card_pos
    have h0 := mul_nonneg (sub_nonneg.mpr hk1) (Real.exp_pos (-t * c)).le
    linarith
  refine ⟨(∑ s, Real.exp (-t * (φ s - φ s₀))) /
      (1 + ((Fintype.card S : ℝ) - 1) * Real.exp (-t * c)), t, (one_lt_div hBpos).mpr hlt, ht0,
    fun n A hA ε hcert => ?_⟩
  have h : Real.exp (-t * ε) * ∏ _i : Fin n, ∑ s, Real.exp (-t * (φ s - φ s₀)) ≤
      A.card * ∏ _i : Fin n, (1 + ((Fintype.card S : ℝ) - 1) * Real.exp (-t * c)) :=
    product_partition_bound (fun _ : Fin n => c) (fun _ => φ) (fun _ => s₀) (fun _ s => hs₀ s)
      ht0 hcert
  rw [Finset.prod_const, Finset.prod_const, Finset.card_univ, Fintype.card_fin] at h
  rw [div_pow, ← mul_div_assoc, div_le_iff₀ (pow_pos hBpos n)]
  exact h

/-- **Dichotomy for homogeneous product landscapes.**  For `n` identical sites with site energy
`φ` minimised at `s₀`, envelope constant `c` and zero residual, one of two regimes occurs.  Either
the single evaluation of the ground state is an exact certificate for every number of sites; by
`product_single_certificate_iff` this happens iff every excitation costs at least `c`.  Or there
is `ρ > 1` such that every exact certificate of the `n`-site system has at least `ρ ^ n`
evaluations.  (For `n ≥ 1` the two alternatives exclude each other, because `ρ ^ n > 1`.) -/
theorem homogeneous_certificate_dichotomy {S : Type*} [Fintype S] [DecidableEq S] [Nonempty S]
    (φ : S → ℝ) (c : ℝ) {s₀ : S} (hs₀ : ∀ s, φ s₀ ≤ φ s) :
    (∀ n : ℕ, IsCertificate (hamEnv fun _ : Fin n => c) (fun x : Fin n → S => ∑ i, φ (x i))
        (fun _ => 0) {fun _ => s₀} (singleton_nonempty _) 0) ∨
      ∃ ρ : ℝ, 1 < ρ ∧ ∀ (n : ℕ) (A : Finset (Fin n → S)) (hA : A.Nonempty),
        IsCertificate (hamEnv fun _ : Fin n => c) (fun x => ∑ i, φ (x i)) (fun _ => 0) A hA 0 →
          ρ ^ n ≤ A.card := by
  by_cases h : ∀ s, s ≠ s₀ → c ≤ φ s - φ s₀
  · exact Or.inl fun n => product_single_certificate (fun _ : Fin n => c) (fun _ => φ)
      (fun _ => s₀) fun _ s hs => h s hs
  · obtain ⟨s₁, hs₁⟩ := not_forall.mp h
    obtain ⟨hne, hnot⟩ := Classical.not_imp.mp hs₁
    have hfail : φ s₁ - φ s₀ < c := not_le.mp hnot
    obtain ⟨ρ, t, hρ, _, hbound⟩ := homogeneous_certificate_exponential φ c hs₀ hne hfail
    refine Or.inr ⟨ρ, hρ, fun n A hA hcert => ?_⟩
    have h1 := hbound n A hA 0 hcert
    rwa [mul_zero, Real.exp_zero, one_mul] at h1

/-- **Exponentially many evaluations on a binary product landscape.**  Take `n` two-state sites,
known part `f x = #{i | x i = true}` (ground state all `false`, every excitation costs `1`), the
weighted Hamming envelope with all constants equal to `2`, and the zero residual.  Then every
exact certificate `A` has at least `(6/5)^n` evaluations: an explicit instance of the exponential
regime of `homogeneous_certificate_dichotomy`.

This is `product_partition_bound` at `t = log 2`: each site contributes `1 + 1/2` on the left and
`1 + 1/4` on the right, and `(3/2) / (5/4) = 6/5`.  The hypothesis is satisfiable: all `2^n`
configurations together form an exact certificate (`binary_full_certificate`).  The envelope
constant `2` exceeds the excitation energy `1`, so for `n ≥ 1` the single evaluation of the
ground state is not a certificate (`product_single_certificate_iff`); the theorem shows that then
no subexponential set of evaluations is one either, although the residual vanishes identically. -/
theorem binary_certificate_exponential (n : ℕ) (A : Finset (Fin n → Bool)) (hA : A.Nonempty)
    (hcert : IsCertificate (hamEnv fun _ : Fin n => (2 : ℝ))
      (fun x => ∑ i, if x i then (1 : ℝ) else 0) (fun _ => 0) A hA 0) :
    (6 / 5 : ℝ) ^ n ≤ A.card := by
  have h2 : Real.exp (-Real.log 2) = 1 / 2 := by
    rw [Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have h4 : Real.exp (-Real.log 2 * 2) = 1 / 4 := by
    rw [show -Real.log 2 * 2 = -Real.log 2 + -Real.log 2 by ring, Real.exp_add, h2]
    norm_num
  have h : Real.exp (-Real.log 2 * 0) * ∏ _i : Fin n, ∑ s : Bool,
        Real.exp (-Real.log 2 * ((if s then (1 : ℝ) else 0) - (if false then (1 : ℝ) else 0))) ≤
      A.card * ∏ _i : Fin n, (1 + ((Fintype.card Bool : ℝ) - 1) * Real.exp (-Real.log 2 * 2)) :=
    product_partition_bound (fun _ : Fin n => (2 : ℝ))
      (fun _ (s : Bool) => if s then (1 : ℝ) else 0) (fun _ => false)
      (fun _ s => by cases s <;> simp) (Real.log_nonneg (by norm_num)) hcert
  have e1 : ∑ s : Bool,
      Real.exp (-Real.log 2 * ((if s then (1 : ℝ) else 0) - (if false then (1 : ℝ) else 0))) =
        3 / 2 := by
    rw [Fintype.sum_bool]
    norm_num [h2]
  have e2 : 1 + ((Fintype.card Bool : ℝ) - 1) * Real.exp (-Real.log 2 * 2) = 5 / 4 := by
    rw [h4, Fintype.card_bool]
    norm_num
  rw [e1, e2, Finset.prod_const, Finset.prod_const, Finset.card_univ, Fintype.card_fin, mul_zero,
    Real.exp_zero, one_mul] at h
  have e3 : (6 / 5 : ℝ) ^ n * (5 / 4) ^ n = (3 / 2) ^ n := by
    rw [← mul_pow]
    norm_num
  rw [← e3] at h
  exact le_of_mul_le_mul_right h (by positivity)

/-- **Non-vacuity of `binary_certificate_exponential`.**  On the same binary product landscape,
all `2^n` configurations together form an exact certificate (`full_evaluation_certificate`), so
the hypothesis of the exponential lower bound is satisfiable for every `n`. -/
theorem binary_full_certificate (n : ℕ) :
    IsCertificate (hamEnv fun _ : Fin n => (2 : ℝ))
      (fun x : Fin n → Bool => ∑ i, if x i then (1 : ℝ) else 0) (fun _ => 0) univ
      univ_nonempty 0 :=
  full_evaluation_certificate (hamEnv_isEnvelope fun _ => by norm_num).self _ _

end Product

end MetricChain
