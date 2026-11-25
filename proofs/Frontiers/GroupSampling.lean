import proofs.Frontiers.NonAdaptive

/-!
# Sampling under a symmetry group: orbit-wise levels and two lower bounds for every `n`

Theory report §11.23, Theorem 11.76(a), (b) in the generality in which their proofs work.
A finite group `Γ` acts on the configurations; the class of residuals and the target are
invariant under the action; the envelope `d` (not necessarily symmetric) is invariant,
`d (σ • x) (σ • y) = d x y`.  Nothing else is assumed: no product structure, no cube.  The
case `Γ = Perm α` acting on the subsets of `α` is `TypeQuantiles.lean` /
`SymmetricSampling.lean` (orbits = type classes); a transitive action (the uniform cube with
all its isometries) has one orbit.

* `gdens Γ S x` — the fraction of group elements that send `x` into `S`; it is the density
  of `S` in the orbit of `x` (`gdens_mul_card_orbit`), is invariant along orbits
  (`gdens_smul`) and monotone.
* `lowDens_shift` — **the normalised matching property, for free**: for an admissible
  residual `ψ` and an invariant envelope, the density of `{ψ < c − d a b}` in the orbit of
  `b` is at most the density of `{ψ < c}` in the orbit of `a` (if `ψ (σ • b)` is that low, the
  admissibility between `σ • a` and `σ • b` forces `ψ (σ • a) < c`).  On the cube this is the
  local LYM inequality.
* `regLevel`, `regLevel_admissible`, `regLevel_lowDens_le`, `regLevel_smul` — any invariant
  family of levels with orbit density at most `q` can be replaced by its envelope
  regularisation `c x = max_a (c₀ a − d a x)`, which is admissible for `d`, invariant, and
  still has orbit density at most `q`.
* `truncate_admissible`, `truncate_gdens_le` — hence `max (ψ, c)` is in the class of
  admissible residuals and differs from `ψ` on orbit density at most `q` everywhere.
* `group_nonadaptive_queries_ge` — two members of an invariant class whose targets differ
  by more than `ε` and which differ on orbit density at most `q` force `(1 − 2δ)/q`
  evaluations of every non-adaptive randomised algorithm.
* `group_queries_ge` — at an invariant instance, a class member that differs from it on
  orbit density at most `q` and by more than `ε` in the target forces `(1 − 2δ)/q`
  evaluations of **every** randomised algorithm, adaptive or not.
* `group_witness` — a concrete instance (the regular action of a group on itself).

Together: for every symmetry group of the known part, sampling uniformly in every orbit
cannot be beaten by a fixed sample by more than the number of orbits (the matching upper
bound — stratified sampling, Chernoff and Markov — is a paper proof), and the every-`n`
lower bound at invariant instances holds for every algorithm.
-/

namespace MetricChain.GroupSampling

open Finset

variable (Γ : Type*) {X : Type*} [Group Γ] [Fintype Γ] [MulAction Γ X]

open scoped Classical in
/-- The fraction of group elements that send `x` into `S`. -/
noncomputable def gdens (S : Set X) (x : X) : ℝ :=
  (#{σ : Γ | σ • x ∈ S} : ℝ) / Fintype.card Γ

variable {Γ}

theorem card_pos_real : (0 : ℝ) < Fintype.card Γ := by
  exact_mod_cast Fintype.card_pos

theorem gdens_nonneg (S : Set X) (x : X) : 0 ≤ gdens Γ S x := by
  unfold gdens; positivity

open scoped Classical in
theorem gdens_mono {S T : Set X} {a b : X} (h : ∀ σ : Γ, σ • b ∈ S → σ • a ∈ T) :
    gdens Γ S b ≤ gdens Γ T a := by
  unfold gdens
  refine div_le_div_of_nonneg_right ?_ (card_pos_real (Γ := Γ)).le
  exact_mod_cast card_le_card fun σ hσ => by
    simp only [mem_filter, mem_univ, true_and] at hσ ⊢
    exact h σ hσ

open scoped Classical in
/-- The density is the same at every point of an orbit. -/
theorem gdens_smul (S : Set X) (τ : Γ) (x : X) : gdens Γ S (τ • x) = gdens Γ S x := by
  unfold gdens
  congr 2
  refine Finset.card_bij (fun σ _ => σ * τ) ?_ ?_ ?_
  · intro σ hσ
    simp only [mem_filter, mem_univ, true_and] at hσ ⊢
    rwa [mul_smul]
  · intro σ₁ _ σ₂ _ h
    exact mul_right_cancel h
  · intro σ' hσ'
    refine ⟨σ' * τ⁻¹, ?_, by simp⟩
    simp only [mem_filter, mem_univ, true_and] at hσ' ⊢
    rw [← mul_smul]
    simpa using hσ'

section Levels

variable {d : X → X → ℝ} {ψ : X → ℝ}

/-- **Normalised matching, from invariance alone.**  If `ψ` is admissible for an invariant
envelope `d`, the points of the orbit of `b` with `ψ < c − d a b` are at most as dense as
the points of the orbit of `a` with `ψ < c`. -/
theorem lowDens_shift (hd : ∀ (σ : Γ) x y, d (σ • x) (σ • y) = d x y)
    (hψ : ∀ x y, ψ x - ψ y ≤ d x y) (a b : X) (c : ℝ) :
    gdens Γ {z | ψ z < c - d a b} b ≤ gdens Γ {z | ψ z < c} a := by
  refine gdens_mono fun σ hσ => ?_
  have h1 : ψ (σ • b) < c - d a b := hσ
  have h2 := hψ (σ • a) (σ • b)
  rw [hd σ a b] at h2
  show ψ (σ • a) < c
  linarith

variable [Fintype X] [Nonempty X]

/-- The envelope regularisation of a family of levels: `c x = max_a (c₀ a − d a x)`. -/
noncomputable def regLevel (d : X → X → ℝ) (c₀ : X → ℝ) (x : X) : ℝ :=
  univ.sup' univ_nonempty fun a => c₀ a - d a x

theorem regLevel_admissible (htri : ∀ x y z, d x z ≤ d x y + d y z) (c₀ : X → ℝ) (x y : X) :
    regLevel d c₀ x - regLevel d c₀ y ≤ d x y := by
  unfold regLevel
  obtain ⟨a, -, ha⟩ := exists_mem_eq_sup' univ_nonempty fun a => c₀ a - d a x
  rw [ha]
  have hy : c₀ a - d a y ≤ univ.sup' univ_nonempty fun a => c₀ a - d a y :=
    le_sup' (fun a => c₀ a - d a y) (mem_univ a)
  have := htri a x y
  linarith

/-- The regularised levels keep the orbit density below `q`. -/
theorem regLevel_lowDens_le (hd : ∀ (σ : Γ) x y, d (σ • x) (σ • y) = d x y)
    (hψ : ∀ x y, ψ x - ψ y ≤ d x y) {c₀ : X → ℝ} {q : ℝ}
    (h₀ : ∀ a, gdens Γ {z | ψ z < c₀ a} a ≤ q) (x : X) :
    gdens Γ {z | ψ z < regLevel d c₀ x} x ≤ q := by
  unfold regLevel
  obtain ⟨a, -, ha⟩ := exists_mem_eq_sup' univ_nonempty fun a => c₀ a - d a x
  rw [ha]
  exact (lowDens_shift hd hψ a x (c₀ a)).trans (h₀ a)

omit [Fintype Γ] in
/-- The regularisation of invariant levels is invariant. -/
theorem regLevel_smul (hd : ∀ (σ : Γ) x y, d (σ • x) (σ • y) = d x y) {c₀ : X → ℝ}
    (hc₀ : ∀ (σ : Γ) x, c₀ (σ • x) = c₀ x) (τ : Γ) (x : X) :
    regLevel d c₀ (τ • x) = regLevel d c₀ x := by
  unfold regLevel
  apply le_antisymm
  · refine sup'_le _ _ fun a _ => ?_
    have h : c₀ a - d a (τ • x) = c₀ (τ⁻¹ • a) - d (τ⁻¹ • a) x := by
      rw [hc₀, ← hd τ⁻¹ a (τ • x), inv_smul_smul]
    rw [h]
    exact le_sup' (fun a => c₀ a - d a x) (mem_univ _)
  · refine sup'_le _ _ fun a _ => ?_
    have h : c₀ a - d a x = c₀ (τ • a) - d (τ • a) (τ • x) := by rw [hc₀, hd]
    rw [h]
    exact le_sup' (fun a => c₀ a - d a (τ • x)) (mem_univ _)

end Levels

section Truncation

variable {d : X → X → ℝ} {ψ c : X → ℝ}

/-- The residual truncated from below at admissible levels is admissible. -/
theorem truncate_admissible (hψ : ∀ x y, ψ x - ψ y ≤ d x y) (hc : ∀ x y, c x - c y ≤ d x y)
    (x y : X) : max (ψ x) (c x) - max (ψ y) (c y) ≤ d x y := by
  rcases le_total (ψ x) (c x) with h | h
  · rw [max_eq_right h]
    have := hc x y
    have := le_max_right (ψ y) (c y)
    linarith
  · rw [max_eq_left h]
    have := hψ x y
    have := le_max_left (ψ y) (c y)
    linarith

/-- The truncation differs from `ψ` exactly where `ψ` is below the level; for invariant
levels with orbit density at most `q` this set has orbit density at most `q`. -/
theorem truncate_gdens_le (hcinv : ∀ (σ : Γ) x, c (σ • x) = c x) {q : ℝ}
    (hq : ∀ x, gdens Γ {z | ψ z < c x} x ≤ q) (x : X) :
    gdens Γ {z | max (ψ z) (c z) ≠ ψ z} x ≤ q := by
  refine (gdens_mono (S := {z | max (ψ z) (c z) ≠ ψ z}) (T := {z | ψ z < c x}) (a := x) (b := x)
    fun σ hσ => ?_).trans (hq x)
  have h1 : max (ψ (σ • x)) (c (σ • x)) ≠ ψ (σ • x) := hσ
  show ψ (σ • x) < c x
  rw [← hcinv σ x]
  by_contra hnot
  exact h1 (max_eq_left (not_lt.mp hnot))

end Truncation

section LowerBounds

variable {Ω : Type*} [Fintype Ω] {G : (X → ℝ) → Prop} {Φ : (X → ℝ) → ℝ}

open scoped Classical in
/-- **Non-adaptive lower bound under a symmetry group** (theory report, Theorem 11.76(a)).
Let the class `G` and the target `Φ` be invariant under the action, and let `ψ`, `ψ'` be two
class members whose targets differ by more than `ε` and which differ on a set of orbit
density at most `q` at every point.  Then every non-adaptive randomised algorithm that is
`(ε/2, δ)`-correct on the class makes at least `(1 − 2δ)/q` evaluations in expectation. -/
theorem group_nonadaptive_queries_ge
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (Q : Ω → Finset X) (hna : ∀ ω g, (alg ω).queries g = Q ω)
    (hGinv : ∀ (σ : Γ) g, G g → G (fun x => g (σ • x)))
    (hΦinv : ∀ (σ : Γ) g, Φ (fun x => g (σ • x)) = Φ g)
    {ψ ψ' : X → ℝ} (hψ : G ψ) (hψ' : G ψ') (hsens : ε < |Φ ψ' - Φ ψ|) {q : ℝ}
    (hdens : ∀ a, gdens Γ {z | ψ' z ≠ ψ z} a ≤ q) :
    1 - 2 * δ ≤ (∑ ω, P ω * (Q ω).card) * q := by
  have hcard := card_pos_real (Γ := Γ)
  have hcap : ∀ a : X,
      ∑ σ ∈ univ.filter (fun σ : Γ => ψ' (σ • a) ≠ ψ (σ • a)), (1 / (Fintype.card Γ : ℝ)) ≤ q := by
    intro a
    rw [sum_const, nsmul_eq_mul, mul_one_div]
    have h := hdens a
    unfold gdens at h
    convert h
    rfl
  have key := nonadaptive_expected_queries_ge (ι := Γ) alg P hP hP1 hcorr Q hna
    (fun σ x => ψ (σ • x)) (fun σ x => ψ' (σ • x)) (fun σ => hGinv σ ψ hψ)
    (fun σ => hGinv σ ψ' hψ') (fun σ => by rw [hΦinv σ ψ', hΦinv σ ψ]; exact hsens)
    (fun _ => 1 / (Fintype.card Γ : ℝ)) (fun _ => by positivity) hcap
  have hsum : ∑ _σ : Γ, (1 / (Fintype.card Γ : ℝ)) = 1 := by
    rw [sum_const, card_univ, nsmul_eq_mul]
    field_simp
  rwa [hsum, mul_one] at key

open scoped Classical in
/-- **Lower bound for every algorithm at an invariant instance** (theory report, Theorem
11.76(b)).  Let `g` be a class member that is invariant under the action, and `ψ'` a class
member whose target differs from that of `g` by more than `ε` and which differs from `g` on
orbit density at most `q` at every point.  Then every randomised algorithm, adaptive or
not, that is `(ε/2, δ)`-correct on the class makes at least `(1 − 2δ)/q` evaluations in
expectation on the instance `g`. -/
theorem group_queries_ge
    (alg : Ω → QueryAlgorithm X) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {ε δ : ℝ}
    (hcorr : ∀ g, G g →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - Φ g| ≤ ε / 2), P ω)
    (hGinv : ∀ (σ : Γ) g, G g → G (fun x => g (σ • x)))
    (hΦinv : ∀ (σ : Γ) g, Φ (fun x => g (σ • x)) = Φ g)
    {g ψ' : X → ℝ} (hg : G g) (hginv : ∀ (σ : Γ) x, g (σ • x) = g x)
    (hψ' : G ψ') (hsens : ε < |Φ ψ' - Φ g|) {q : ℝ}
    (hdens : ∀ a, gdens Γ {z | ψ' z ≠ g z} a ≤ q) :
    1 - 2 * δ ≤ (∑ ω, P ω * ((alg ω).queries g).card) * q := by
  have hcard := card_pos_real (Γ := Γ)
  have hcap : ∀ a : X,
      ∑ σ ∈ univ.filter (fun σ : Γ => ψ' (σ • a) ≠ g a), (1 / (Fintype.card Γ : ℝ)) ≤ q := by
    intro a
    rw [sum_const, nsmul_eq_mul, mul_one_div]
    have hset : (univ.filter fun σ : Γ => ψ' (σ • a) ≠ g a)
        = (univ.filter fun σ : Γ => σ • a ∈ {z | ψ' z ≠ g z}) := by
      ext σ
      simp only [mem_filter, mem_univ, true_and, Set.mem_setOf_eq, hginv σ a]
    rw [hset]
    have h := hdens a
    unfold gdens at h
    convert h
    rfl
  have key := expected_queries_ge_packing (ι := Γ) alg P hP hP1 hcorr hg
    (fun σ x => ψ' (σ • x)) (fun σ => hGinv σ ψ' hψ')
    (fun σ => by rw [hΦinv σ ψ']; exact hsens)
    (fun _ => 1 / (Fintype.card Γ : ℝ)) (fun _ => by positivity) hcap
  have hsum : ∑ _σ : Γ, (1 / (Fintype.card Γ : ℝ)) = 1 := by
    rw [sum_const, card_univ, nsmul_eq_mul]
    field_simp
  rwa [hsum, mul_one] at key

end LowerBounds

section Orbit

variable [Fintype X]

open scoped Classical in
/-- **`gdens` is the density in the orbit.**  The fraction of group elements that send `x`
into `S`, times the size of the orbit of `x`, is the number of points of the orbit in `S`: a
uniformly random group element sends `x` to a uniformly random point of its orbit. -/
theorem gdens_mul_card_orbit (S : Set X) (x : X) :
    gdens Γ S x * #{y : X | y ∈ MulAction.orbit Γ x}
      = #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by
  set O : Finset X := {y : X | y ∈ MulAction.orbit Γ x} with hO
  have hA : ∀ b ∈ O, #{σ : Γ | σ • b ∈ S} = #{σ : Γ | σ • x ∈ S} := by
    intro b hb
    rw [hO, mem_filter] at hb
    obtain ⟨τ, rfl⟩ := MulAction.mem_orbit_iff.mp hb.2
    refine Finset.card_bij (fun σ _ => σ * τ) ?_ ?_ ?_
    · intro σ hσ
      simp only [mem_filter, mem_univ, true_and] at hσ ⊢
      rwa [mul_smul]
    · intro σ₁ _ σ₂ _ h
      exact mul_right_cancel h
    · intro σ' hσ'
      refine ⟨σ' * τ⁻¹, ?_, by simp⟩
      simp only [mem_filter, mem_univ, true_and] at hσ' ⊢
      rw [← mul_smul]
      simpa using hσ'
  have hB : ∑ b ∈ O, #{σ : Γ | σ • b ∈ S} = ∑ σ : Γ, #{b ∈ O | σ • b ∈ S} := by
    simp_rw [card_filter]
    exact Finset.sum_comm
  have hC : ∀ σ : Γ, #{b ∈ O | σ • b ∈ S} = #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by
    intro σ
    refine Finset.card_bij (fun b _ => σ • b) ?_ ?_ ?_
    · intro b hb
      rw [mem_filter, hO, mem_filter] at hb
      rw [mem_filter]
      obtain ⟨τ, rfl⟩ := MulAction.mem_orbit_iff.mp hb.1.2
      exact ⟨mem_univ _, MulAction.mem_orbit_iff.mpr ⟨σ * τ, by rw [mul_smul]⟩, hb.2⟩
    · intro b₁ _ b₂ _ h
      exact smul_left_cancel σ h
    · intro t ht
      rw [mem_filter] at ht
      obtain ⟨τ, rfl⟩ := MulAction.mem_orbit_iff.mp ht.2.1
      refine ⟨σ⁻¹ • τ • x, ?_, by simp⟩
      rw [mem_filter, hO, mem_filter]
      refine ⟨⟨mem_univ _, MulAction.mem_orbit_iff.mpr ⟨σ⁻¹ * τ, by rw [mul_smul]⟩⟩, ?_⟩
      simpa using ht.2.2
  have hcount : #O * #{σ : Γ | σ • x ∈ S}
      = Fintype.card Γ * #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by
    calc #O * #{σ : Γ | σ • x ∈ S} = ∑ _b ∈ O, #{σ : Γ | σ • x ∈ S} := by
          rw [sum_const, smul_eq_mul]
      _ = ∑ b ∈ O, #{σ : Γ | σ • b ∈ S} := (sum_congr rfl fun b hb => (hA b hb).symm)
      _ = ∑ _σ : Γ, #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by
          rw [hB]; exact sum_congr rfl fun σ _ => hC σ
      _ = Fintype.card Γ * #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by
          rw [sum_const, card_univ, smul_eq_mul]
  have hcard := card_pos_real (Γ := Γ)
  have hcountR : (#O : ℝ) * #{σ : Γ | σ • x ∈ S}
      = Fintype.card Γ * #{y : X | y ∈ MulAction.orbit Γ x ∧ y ∈ S} := by exact_mod_cast hcount
  unfold gdens
  rw [div_mul_eq_mul_div, div_eq_iff hcard.ne']
  linarith

end Orbit

section Witness

open scoped Classical in
/-- **A concrete instance (non-vacuity).**  The group acts on itself by left
multiplication (one orbit).  To sum an arbitrary real function on the group to within
`1/4` with probability at least `1 − δ`, every randomised algorithm — adaptive or not —
evaluates the zero function at `(1 − 2δ)·|Γ|` points at least in expectation. -/
theorem group_witness {Ω : Type*} [Fintype Ω]
    (alg : Ω → QueryAlgorithm Γ) (P : Ω → ℝ) (hP : ∀ ω, 0 ≤ P ω) (hP1 : ∑ ω, P ω = 1)
    {δ : ℝ}
    (hcorr : ∀ g : Γ → ℝ, True →
      1 - δ ≤ ∑ ω ∈ univ.filter (fun ω => |(alg ω).output g - ∑ x, g x| ≤ (1 / 2 : ℝ) / 2), P ω) :
    (1 - 2 * δ) * Fintype.card Γ ≤ ∑ ω, P ω * ((alg ω).queries (fun _ => 0)).card := by
  have hcard := card_pos_real (Γ := Γ)
  have key := group_queries_ge (Γ := Γ) (X := Γ) (G := fun _ => True) (Φ := fun g => ∑ x, g x)
    alg P hP hP1 hcorr (fun _ _ _ => trivial)
    (fun σ g => Fintype.sum_equiv (Equiv.mulLeft σ) _ _ (fun x => rfl))
    (g := fun _ => 0) (ψ' := fun x => if x = 1 then 1 else 0) trivial (fun _ _ => rfl) trivial
    (by simp; norm_num) (q := 1 / (Fintype.card Γ : ℝ)) (fun a => by
      unfold gdens
      refine div_le_div_of_nonneg_right ?_ hcard.le
      have hsub : ({σ : Γ | σ • a ∈ {z : Γ | (if z = 1 then (1 : ℝ) else 0) ≠ 0}} : Finset Γ)
          ⊆ {a⁻¹} := by
        intro σ hσ
        rw [mem_filter] at hσ
        have h2 : (if σ • a = 1 then (1 : ℝ) else 0) ≠ 0 := hσ.2
        have h3 : σ • a = 1 := by
          by_contra h
          exact h2 (if_neg h)
        rw [mem_singleton]
        exact eq_inv_of_mul_eq_one_left (by simpa using h3)
      exact_mod_cast (card_le_card hsub).trans (card_singleton _).le)
  rw [mul_one_div, le_div_iff₀ hcard] at key
  exact key

end Witness

end MetricChain.GroupSampling
