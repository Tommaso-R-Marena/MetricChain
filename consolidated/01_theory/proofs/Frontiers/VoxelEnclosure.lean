import Mathlib
import proofs.Core.Basic
import proofs.CertificateAlgebra
import proofs.Frontiers.PartitionCertificate

/-!
# Voxel enclosure: from continuous Boltzmann integrals to the rational kernel

Provable design algorithms of the `K*` family replace the integral of `exp(-β E)` over a
continuous rotamer voxel by `exp(-β E_min)`.  This file supplies the missing rigorous link between
*continuous* conformational integrals and the *discrete* partition-function kernel of
`PartitionCertificate.lean`:

* `voxel_boltzmann_bounds` — on a measurable voxel `V` of finite volume, energy bounds
  `E_lo ≤ E ≤ E_hi` give `vol(V)·exp(-β E_hi) ≤ ∫_V exp(-β E) ≤ vol(V)·exp(-β E_lo)`
  (the entropy factor `vol(V)` is what the minimised-energy surrogate drops);
* `voxel_riemann_enclosure` — over a finite family of pairwise disjoint voxels the integral is
  enclosed by the two Riemann sums;
* `Z_encloses_voxel_integral` — **assembly theorem**: if the weights of two rational instances
  bracket the voxel integrals (states = voxels, volumes absorbed in the one-body factors), their
  exact rational partition sums bracket the continuous partition integral.  Combined with
  `zverify_sound` this turns any accepted `ZCert` into a certified two-sided bound on a continuous
  (or mixed discrete–continuous) partition function.
-/

namespace MetricChain

open MeasureTheory Finset

variable {Ω : Type*} [MeasurableSpace Ω]

/-- Zeroth-order voxel bound for the Boltzmann integral, including the volume (entropy) factor. -/
theorem voxel_boltzmann_bounds (μ : Measure Ω) {V : Set Ω} (hV : MeasurableSet V)
    (hfin : μ V ≠ ⊤) (E : Ω → ℝ) {β Elo Ehi : ℝ} (hβ : 0 ≤ β)
    (hint : IntegrableOn (fun ω => Real.exp (-β * E ω)) V μ)
    (hlo : ∀ ω ∈ V, Elo ≤ E ω) (hhi : ∀ ω ∈ V, E ω ≤ Ehi) :
    (μ V).toReal * Real.exp (-β * Ehi) ≤ ∫ ω in V, Real.exp (-β * E ω) ∂μ ∧
      ∫ ω in V, Real.exp (-β * E ω) ∂μ ≤ (μ V).toReal * Real.exp (-β * Elo) := by
  have hconst : ∀ c : ℝ, ∫ _ω in V, c ∂μ = (μ V).toReal * c := by
    intro c
    rw [setIntegral_const]
    simp [Measure.real, smul_eq_mul]
  have hic : ∀ c : ℝ, IntegrableOn (fun _ : Ω => c) V μ := fun c =>
    integrableOn_const hfin
  constructor
  · rw [← hconst]
    apply setIntegral_mono_on (hic _) hint hV
    intro ω hω
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hhi ω hω) hβ
    linarith
  · rw [← hconst]
    apply setIntegral_mono_on hint (hic _) hV
    intro ω hω
    apply Real.exp_le_exp.mpr
    have := mul_le_mul_of_nonneg_left (hlo ω hω) hβ
    linarith

/-- Riemann-sum enclosure of an integral over a finite family of pairwise disjoint voxels. -/
theorem voxel_riemann_enclosure (μ : Measure Ω) {X : Type*} (S : Finset X) (V : X → Set Ω)
    (hmeas : ∀ x ∈ S, MeasurableSet (V x))
    (hdisj : Set.Pairwise (↑S) (Function.onFun Disjoint V))
    (f : Ω → ℝ) (hint : ∀ x ∈ S, IntegrableOn f (V x) μ) (mlo mhi : X → ℝ)
    (hb : ∀ x ∈ S, mlo x ≤ ∫ ω in V x, f ω ∂μ ∧ ∫ ω in V x, f ω ∂μ ≤ mhi x) :
    ∑ x ∈ S, mlo x ≤ ∫ ω in ⋃ x ∈ S, V x, f ω ∂μ ∧
      ∫ ω in ⋃ x ∈ S, V x, f ω ∂μ ≤ ∑ x ∈ S, mhi x := by
  rw [integral_biUnion_finset S hmeas hdisj hint]
  exact ⟨Finset.sum_le_sum fun x hx => (hb x hx).1, Finset.sum_le_sum fun x hx => (hb x hx).2⟩

/-- **Assembly theorem.**  States of the rational instances are voxels.  If for every
configuration `x` of the box the weights of `Ilo` and `Ihi` bracket the integral of `f` over the
voxel `V x`, then the exact rational partition sums bracket the integral of `f` over the union of
all voxels of the box. -/
theorem Z_encloses_voxel_integral {n k : ℕ} (μ : Measure Ω) (D : Dom n k)
    (V : Config n k → Set Ω) (hmeas : ∀ x ∈ boxFinset D, MeasurableSet (V x))
    (hdisj : Set.Pairwise (↑(boxFinset D)) (Function.onFun Disjoint V))
    (f : Ω → ℝ) (hint : ∀ x ∈ boxFinset D, IntegrableOn f (V x) μ) (Ilo Ihi : WInstance n k)
    (hb : ∀ x ∈ boxFinset D, ((Ilo.weight x : ℚ) : ℝ) ≤ ∫ ω in V x, f ω ∂μ ∧
      ∫ ω in V x, f ω ∂μ ≤ ((Ihi.weight x : ℚ) : ℝ)) :
    ((Ilo.Z D : ℚ) : ℝ) ≤ ∫ ω in ⋃ x ∈ boxFinset D, V x, f ω ∂μ ∧
      ∫ ω in ⋃ x ∈ boxFinset D, V x, f ω ∂μ ≤ ((Ihi.Z D : ℚ) : ℝ) := by
  have h := voxel_riemann_enclosure μ (boxFinset D) V hmeas hdisj f hint
    (fun x => ((Ilo.weight x : ℚ) : ℝ)) (fun x => ((Ihi.weight x : ℚ) : ℝ)) hb
  unfold WInstance.Z
  push_cast
  exact h

/-- **Certified continuous partition function.**  An accepted certificate for the lower instance
and one for the upper instance give a two-sided rational enclosure of the continuous integral. -/
theorem certified_voxel_partition {n k : ℕ} (μ : Measure Ω) (D : Dom n k)
    (V : Config n k → Set Ω) (hmeas : ∀ x ∈ boxFinset D, MeasurableSet (V x))
    (hdisj : Set.Pairwise (↑(boxFinset D)) (Function.onFun Disjoint V))
    (f : Ω → ℝ) (hint : ∀ x ∈ boxFinset D, IntegrableOn f (V x) μ) (Ilo Ihi : WInstance n k)
    (hlo : Ilo.Nonneg) (hhi : Ihi.Nonneg)
    (hb : ∀ x ∈ boxFinset D, ((Ilo.weight x : ℚ) : ℝ) ≤ ∫ ω in V x, f ω ∂μ ∧
      ∫ ω in V x, f ω ∂μ ≤ ((Ihi.weight x : ℚ) : ℝ))
    (clo chi : ZCert n k) (a b a' b' : ℚ) (hclo : zverify clo Ilo D = some (a, b))
    (hchi : zverify chi Ihi D = some (a', b')) :
    (a : ℝ) ≤ ∫ ω in ⋃ x ∈ boxFinset D, V x, f ω ∂μ ∧
      ∫ ω in ⋃ x ∈ boxFinset D, V x, f ω ∂μ ≤ (b' : ℝ) := by
  have h := Z_encloses_voxel_integral μ D V hmeas hdisj f hint Ilo Ihi hb
  have h1 := (zverify_sound hlo clo D a b hclo).1
  have h2 := (zverify_sound hhi chi D a' b' hchi).2
  have h1' : (a : ℝ) ≤ ((Ilo.Z D : ℚ) : ℝ) := by exact_mod_cast h1
  have h2' : ((Ihi.Z D : ℚ) : ℝ) ≤ (b' : ℝ) := by exact_mod_cast h2
  exact ⟨le_trans h1' h.1, le_trans h.2 h2'⟩

end MetricChain
