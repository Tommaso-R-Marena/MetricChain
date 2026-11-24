import Mathlib
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.CertificateNotions
import proofs.Frontiers.ConditionalEnvelope
import proofs.Frontiers.ThermalRobustness
import proofs.Frontiers.PartitionProduct

/-!
# Lemmas contributed by the second independent referee

The second referee report (`docs/reviews/R2_referee_report.md`, Appendix A) contains four
machine-checked lemmas.  Each of them sharpens or limits a statement of the theory report, so
they are part of the development; the proofs are the referee's.

* `config_exchange`, `value_exchange`, `card_exchange_le` — **the three notions of certificate
  are one number.**  A value certificate, and a configuration certificate with at least one
  evaluation, can be turned into a point certificate of at most the same size by exchanging one
  evaluated point.  Together with `isValueCertificate_of_isCertificate` and
  `isConfigCertificate_of_isCertificate` this gives `N_value = N_point` and
  `N_point = max(1, N_config)`; Theorem 11.5 of the theory report (`CertificateNotions.lean`),
  which states `N_value ≤ N_point` and `N_point ≤ N_config + 1`, is true but not sharp.
* `exact_free_energy_certificate_eq_univ` — **limitation of the finite-temperature exponent
  theorem.**  With positive slack off the diagonal and `β > 0`, an evaluated set whose two
  envelope partition functions coincide (a certificate of `ln Z` with `ε = 0`) is the whole
  space.  Hence the exponent formula of Theorem 11.15 cannot hold for arbitrarily small
  accuracies; the theorem needs `ln (1/ε_n) = o(n)`.
* `gaugeW`, `gauge_trivial_separation` — **limitation of the partition-kernel separations.**
  The hypothesis `WInstance.Rigid` of `zverify2_elementary_exact_leaves` and `chain_separation`
  is a property of the representation, not of the model: an instance whose two ordered pair
  factors compensate each other (every configuration has weight one — two independent uniform
  sites) is `Pos` and `Rigid`, and the theorem applies to it.
-/

namespace MetricChain

open Finset

section Notions

variable {X : Type*} [Fintype X] [Nonempty X]

/-- **Exchange for configuration certificates.**  If `A` (nonempty) certifies the configuration
`x`, then replacing the anchor that attains `U_A x` by `x` gives a point certificate.  Its size is
at most `|A|`.  Hence `N_point ≤ N_config` whenever `N_config ≥ 1`. -/
theorem config_exchange [DecidableEq X] {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {x : X} {ε : ℝ}
    (h : IsConfigCertificate d f g A hA x ε) :
    ∃ a₀ ∈ A, IsCertificate d f g (insert x (A.erase a₀)) (insert_nonempty x _) ε := by
  obtain ⟨a₀, ha₀, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d x a)
  have hU : upperEnv d A hA g x = g a₀ + d x a₀ := hmin
  refine ⟨a₀, ha₀, ?_⟩
  rw [isCertificate_iff_cover]
  intro y
  have hUB : certUB f g (insert x (A.erase a₀)) (insert_nonempty x _) ≤ f x + g x :=
    Finset.inf'_le (fun a => f a + g a) (mem_insert_self x _)
  have hy := h y
  unfold condEnv at hy
  rcases min_le_iff.mp hy with h1 | h1
  · refine ⟨x, mem_insert_self x _, ?_⟩
    unfold slack
    linarith
  · obtain ⟨b, hb, hmax⟩ := Finset.exists_mem_eq_sup' hA (fun a => g a - d a y)
    have hL : lowerEnv d A hA g y = g b - d b y := hmax
    by_cases hba : b = a₀
    · subst hba
      refine ⟨x, mem_insert_self x _, ?_⟩
      have htri := hd.triangle x b y
      rw [hU, hL] at h1
      unfold slack
      linarith
    · refine ⟨b, mem_insert_of_mem (mem_erase.mpr ⟨hba, hb⟩), ?_⟩
      have hUx := le_upperEnv hg A hA g (fun _ _ => rfl) x
      rw [hL] at h1
      unfold slack
      linarith

omit [Fintype X] [Nonempty X] in
/-- Cardinality of the exchanged set. -/
theorem card_exchange_le [DecidableEq X] {A : Finset X} {a₀ x : X} (ha₀ : a₀ ∈ A) :
    (insert x (A.erase a₀)).card ≤ A.card := by
  have h1 := Finset.card_insert_le x (A.erase a₀)
  have h2 := Finset.card_erase_of_mem ha₀
  have h3 : 0 < A.card := Finset.card_pos.mpr ⟨a₀, ha₀⟩
  omega

/-- **Exchange for value certificates.**  If `A` is a value certificate, some set of at most `|A|`
points is a point certificate: replace the anchor that attains `U_A` at a minimiser `y₀` of
`f + U_A` by `y₀`.  Hence `N_point ≤ N_value`, i.e. `N_point = N_value`. -/
theorem value_exchange [DecidableEq X] {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {ε : ℝ}
    (h : IsValueCertificate d f g A hA ε) :
    ∃ (B : Finset X) (hB : B.Nonempty), B.card ≤ A.card ∧ IsCertificate d f g B hB ε := by
  obtain ⟨y₀, -, hy₀⟩ := Finset.exists_mem_eq_inf' univ_nonempty
    (fun y => f y + upperEnv d A hA g y)
  obtain ⟨a₀, ha₀, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d y₀ a)
  have hU : upperEnv d A hA g y₀ = g a₀ + d y₀ a₀ := hmin
  refine ⟨insert y₀ (A.erase a₀), insert_nonempty y₀ _, card_exchange_le ha₀, ?_⟩
  rw [isCertificate_iff_cover]
  intro z
  have hUB : certUB f g (insert y₀ (A.erase a₀)) (insert_nonempty y₀ _) ≤ f y₀ + g y₀ :=
    Finset.inf'_le (fun a => f a + g a) (mem_insert_self y₀ _)
  unfold IsValueCertificate at h
  rw [hy₀, hU] at h
  have hLB : certLB d f g A hA ≤ f z + lowerEnv d A hA g z :=
    Finset.inf'_le (fun y => f y + lowerEnv d A hA g y) (mem_univ z)
  obtain ⟨b, hb, hmax⟩ := Finset.exists_mem_eq_sup' hA (fun a => g a - d a z)
  have hL : lowerEnv d A hA g z = g b - d b z := hmax
  rw [hL] at hLB
  have hadm := hg y₀ a₀
  by_cases hba : b = a₀
  · subst hba
    refine ⟨y₀, mem_insert_self y₀ _, ?_⟩
    have htri := hd.triangle y₀ b z
    unfold slack
    linarith
  · refine ⟨b, mem_insert_of_mem (mem_erase.mpr ⟨hba, hb⟩), ?_⟩
    unfold slack
    linarith

end Notions

section Gauge

/-- Two binary sites.  The two ordered pair factors compensate each other:
`W 0 1 a b = 2^(a + 2b)` and `W 1 0 b a = 2^(-(a + 2b))`, so every configuration has weight `1`
(two independent uniform sites), but each ordered factor separately tells all states apart. -/
def gaugeW : WInstance 2 2 where
  w := fun _ _ => 1
  W := fun i j a b =>
    if i = 0 ∧ j = 1 then (2 : ℚ) ^ (a.val + 2 * b.val)
    else if i = 1 ∧ j = 0 then 1 / (2 : ℚ) ^ (b.val + 2 * a.val)
    else 1

theorem gaugeW_pos : gaugeW.Pos := by decide +kernel

theorem gaugeW_rigid : gaugeW.Rigid := by decide +kernel

theorem gaugeW_weight : ∀ x : Config 2 2, gaugeW.weight x = 1 := by decide +kernel

theorem gaugeW_Z : gaugeW.Z (fullDom 2 2) = 4 := by decide +kernel

/-- The instance is a product of two uniform sites (`Z = 2 · 2`), it is `Pos` and `Rigid`, and
therefore every elementary certificate with the exact lower endpoint enumerates all four
configurations: the "separation" is a property of the representation, not of the model. -/
theorem gauge_trivial_separation :
    gaugeW.Pos ∧ gaugeW.Rigid ∧ (∀ x : Config 2 2, gaugeW.weight x = 1) ∧
      ∀ c : ZCert2 2 2, c.Elementary → ∀ hi : ℚ,
        zverify2 c gaugeW (fullDom 2 2) = some (4, hi) → 2 ^ 2 ≤ c.leaves := by
  refine ⟨gaugeW_pos, gaugeW_rigid, gaugeW_weight, fun c hc hi hv => ?_⟩
  rw [← gaugeW_Z] at hv
  exact zverify2_elementary_exact_leaves_fullDom gaugeW_pos gaugeW_rigid c hc hi hv

end Gauge

section Thermal

variable {X : Type*} [Fintype X] [Nonempty X]

omit [Nonempty X] in
/-- **An exact certificate of the free energy evaluates everything.**  Let the slack be positive
off the diagonal and `β > 0`.  If the optimistic partition function (lower McShane envelope) is
at most the pessimistic one (upper envelope) — a certificate of `ln Z` with `ε = 0` — then the
evaluated set is the whole space. -/
theorem exact_free_energy_certificate_eq_univ {d : X → X → ℝ} {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) (A : Finset X) (hA : A.Nonempty) {β : ℝ} (hβ : 0 < β)
    (hpos : ∀ a y, a ≠ y → 0 < slack d g a y)
    (h : ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) ≤
      ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y))) : A = univ := by
  have hLU : ∀ y, lowerEnv d A hA g y ≤ upperEnv d A hA g y := fun y =>
    (lowerEnv_le hg A hA g (fun _ _ => rfl) y).trans (le_upperEnv hg A hA g (fun _ _ => rfl) y)
  have hterm : ∀ y ∈ (univ : Finset X), Real.exp (-β * (f y + upperEnv d A hA g y)) ≤
      Real.exp (-β * (f y + lowerEnv d A hA g y)) := by
    intro y _
    apply Real.exp_le_exp.mpr
    nlinarith [hLU y]
  have hsum : ∑ y, Real.exp (-β * (f y + upperEnv d A hA g y)) =
      ∑ y, Real.exp (-β * (f y + lowerEnv d A hA g y)) :=
    le_antisymm (Finset.sum_le_sum hterm) h
  have heq := (Finset.sum_eq_sum_iff_of_le hterm).mp hsum
  rw [Finset.eq_univ_iff_forall]
  intro y
  have hy := Real.exp_injective (heq y (mem_univ y))
  have hLUy : upperEnv d A hA g y = lowerEnv d A hA g y := by
    have h1 : -β * (f y + upperEnv d A hA g y) = -β * (f y + lowerEnv d A hA g y) := hy
    have h2 : β * (upperEnv d A hA g y - lowerEnv d A hA g y) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 hβ.ne'
    · linarith
  have hL := lowerEnv_eq_sub_slack d g A hA y
  have hgL := lowerEnv_le hg A hA g (fun _ _ => rfl) y
  have hgU := le_upperEnv hg A hA g (fun _ _ => rfl) y
  have hs0 : slackFrom d g A hA y = 0 := by linarith
  obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
  have hsa : slack d g a y = 0 := by
    have : slackFrom d g A hA y = slack d g a y := hmin
    linarith
  by_contra hyA
  have hne : a ≠ y := fun e => hyA (e ▸ ha)
  have := hpos a y hne
  linarith

end Thermal

end MetricChain
