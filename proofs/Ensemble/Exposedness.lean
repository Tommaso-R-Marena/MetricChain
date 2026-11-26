import Mathlib
import proofs.Frontiers.EnvelopeDuality

/-!
# Observability as exposedness: certificates of ensemble identification

Ensemble division (`docs/ensemble/ENSEMBLE_REPORT.md`, Part I).  An *ensemble* is a probability
vector `ν` on a finite configuration space `X`; the *data* of a family of observables
`Φ : ι → X → ℝ` are the means `mean ν (Φ i)`.

* `eq_of_exposing_certificate` — the sufficiency half of Theorem E1: if some function
  `c + λ·Φ` in the span of the observables is zero on a set `S`, positive off `S`, and the
  features `(1, Φ)` are linearly independent on `S`, then an ensemble supported on `S` is the
  **only** ensemble with its data.
* `mass_off_support_le` — the first half of the stability estimate: an ensemble whose data are
  close to those of `μ` puts little mass outside the support of `μ`; the constant is the
  coefficient norm of the certificate divided by its gap.
* `transport_le_of_sharp` — Theorem E2, the inequality: if the energy `λ·Φ` grows at least like
  `s·d(x⋆, ·)` away from `x⋆`, then every ensemble's transport cost from the conformation `x⋆`
  is at most `(1/s)·Σ |λ_i|·|data_i(ν) − Φ_i(x⋆)|`.
* `identification_of_robust_certificate` — the bridge to the theory division's Theorem 2.4
  (`robust_certified_iff`): **a certificate that `x⋆` minimises `λ·Φ + g` for every admissible
  residual `g` of the envelope `d` is a certificate that the data of `Φ` identify the
  conformation `x⋆`**, with modulus `Σ |λ_i|·|Δdata_i|` in the transport cost of `d`.
* `residual_advantage_le` — the same statement read on the side of the residual: no admissible
  residual lowers the mean energy of a data-compatible ensemble below the energy of `x⋆` by
  more than that modulus.

The converse statements (necessity in Theorem E1; exactness of the constant in Theorem E2) are
linear-programming duality and are paper proofs in the report.
-/

namespace MetricChain.Ensemble

open Finset

variable {X : Type*} [Fintype X] {ι : Type*} [Fintype ι]

/-- A probability vector on a finite configuration space. -/
structure IsEnsemble (ν : X → ℝ) : Prop where
  nonneg : ∀ x, 0 ≤ ν x
  sum_one : ∑ x, ν x = 1

/-- The datum of the observable `φ` in the ensemble `ν`. -/
def mean (ν : X → ℝ) (φ : X → ℝ) : ℝ := ∑ x, ν x * φ x

/-- The energy `λ·Φ` in the span of the observables. -/
def energy (lam : ι → ℝ) (Φ : ι → X → ℝ) (x : X) : ℝ := ∑ i, lam i * Φ i x

theorem mean_energy (ν : X → ℝ) (lam : ι → ℝ) (Φ : ι → X → ℝ) :
    mean ν (energy lam Φ) = ∑ i, lam i * mean ν (Φ i) := by
  unfold mean energy
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => ?_
  refine Finset.sum_congr rfl fun x _ => ?_
  ring

/-- The mean of an affine function `c + λ·Φ` of the observables is determined by the data. -/
theorem mean_affine (ν : X → ℝ) (hν : IsEnsemble ν) (c : ℝ) (lam : ι → ℝ) (Φ : ι → X → ℝ) :
    ∑ x, ν x * (c + energy lam Φ x) = c + ∑ i, lam i * mean ν (Φ i) := by
  have h : ∑ x, ν x * (c + energy lam Φ x) = c * ∑ x, ν x + mean ν (energy lam Φ) := by
    unfold mean
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [h, hν.sum_one, mul_one, mean_energy]

/-- **Certificate of identification (sufficiency in Theorem E1).**  Let `μ` be supported on `S`.
If some `c + λ·Φ` vanishes on `S` and is positive off `S`, and no non-zero signed vector on `S`
of total mass zero has zero data, then every ensemble with the data of `μ` equals `μ`. -/
theorem eq_of_exposing_certificate
    (Φ : ι → X → ℝ) (μ ν : X → ℝ) (hμ : IsEnsemble μ) (hν : IsEnsemble ν)
    (S : Finset X) (hsupp : ∀ x, x ∉ S → μ x = 0)
    (c : ℝ) (lam : ι → ℝ)
    (hzero : ∀ x ∈ S, c + energy lam Φ x = 0)
    (hpos : ∀ x, x ∉ S → 0 < c + energy lam Φ x)
    (hindep : ∀ h : X → ℝ, (∀ x, x ∉ S → h x = 0) → ∑ x, h x = 0 →
        (∀ i, ∑ x, h x * Φ i x = 0) → ∀ x, h x = 0)
    (hdata : ∀ i, mean ν (Φ i) = mean μ (Φ i)) : ν = μ := by
  have hμ0 : ∑ x, μ x * (c + energy lam Φ x) = 0 := by
    refine Finset.sum_eq_zero fun x _ => ?_
    by_cases hx : x ∈ S
    · rw [hzero x hx, mul_zero]
    · rw [hsupp x hx, zero_mul]
  have hν0 : ∑ x, ν x * (c + energy lam Φ x) = 0 := by
    rw [mean_affine ν hν, ← hμ0, mean_affine μ hμ]
    congr 1
    exact Finset.sum_congr rfl fun i _ => by rw [hdata i]
  have hterm : ∀ x ∈ (Finset.univ : Finset X), 0 ≤ ν x * (c + energy lam Φ x) := by
    intro x _
    by_cases hx : x ∈ S
    · rw [hzero x hx, mul_zero]
    · exact mul_nonneg (hν.nonneg x) (hpos x hx).le
  have hall := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp hν0
  have hνS : ∀ x, x ∉ S → ν x = 0 := by
    intro x hx
    have h1 := hall x (Finset.mem_univ x)
    rcases mul_eq_zero.mp h1 with h | h
    · exact h
    · exact absurd h (hpos x hx).ne'
  have hdiff := hindep (fun x => ν x - μ x)
    (fun x hx => by simp [hνS x hx, hsupp x hx])
    (by rw [Finset.sum_sub_distrib, hν.sum_one, hμ.sum_one, sub_self])
    (fun i => by
      have h := hdata i
      unfold mean at h
      simp only [sub_mul, Finset.sum_sub_distrib]
      linarith)
  funext x
  have h : ν x - μ x = 0 := hdiff x
  linarith

/-- **Stability, first half.**  If the certificate `c + λ·Φ` vanishes on `S ⊇ supp μ` and is at
least `γ` off `S`, then the mass that any ensemble `ν` puts outside `S` is at most
`(Σ |λ_i|·|data_i(ν) − data_i(μ)|) / γ`. -/
theorem mass_off_support_le [DecidableEq X]
    (Φ : ι → X → ℝ) (μ ν : X → ℝ) (hμ : IsEnsemble μ) (hν : IsEnsemble ν)
    (S : Finset X) (hsupp : ∀ x, x ∉ S → μ x = 0)
    (c : ℝ) (lam : ι → ℝ) (γ : ℝ)
    (hzero : ∀ x ∈ S, c + energy lam Φ x = 0)
    (hgap : ∀ x, x ∉ S → γ ≤ c + energy lam Φ x) :
    γ * ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ν x ≤
      ∑ i, |lam i| * |mean ν (Φ i) - mean μ (Φ i)| := by
  have hμ0 : ∑ x, μ x * (c + energy lam Φ x) = 0 := by
    refine Finset.sum_eq_zero fun x _ => ?_
    by_cases hx : x ∈ S
    · rw [hzero x hx, mul_zero]
    · rw [hsupp x hx, zero_mul]
  have h1 : γ * ∑ x ∈ Finset.univ.filter (fun x => x ∉ S), ν x ≤
      ∑ x, ν x * (c + energy lam Φ x) := by
    rw [Finset.mul_sum, Finset.sum_filter]
    refine Finset.sum_le_sum fun x _ => ?_
    by_cases hx : x ∈ S
    · simp [hx, hzero x hx]
    · simp only [hx, not_false_eq_true, if_true]
      have h := mul_le_mul_of_nonneg_left (hgap x hx) (hν.nonneg x)
      linarith
  have h2 : ∑ x, ν x * (c + energy lam Φ x) =
      ∑ i, lam i * (mean ν (Φ i) - mean μ (Φ i)) := by
    have e1 := mean_affine ν hν c lam Φ
    have e2 := mean_affine μ hμ c lam Φ
    rw [hμ0] at e2
    rw [e1]
    have e3 : ∑ i, lam i * (mean ν (Φ i) - mean μ (Φ i)) =
        ∑ i, lam i * mean ν (Φ i) - ∑ i, lam i * mean μ (Φ i) := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun i _ => by ring
    rw [e3]
    linarith
  have h3 : ∑ i, lam i * (mean ν (Φ i) - mean μ (Φ i)) ≤
      ∑ i, |lam i| * |mean ν (Φ i) - mean μ (Φ i)| :=
    Finset.sum_le_sum fun i _ => by
      rw [← abs_mul]
      exact le_abs_self _
  linarith

/-- **Theorem E2, the inequality.**  If the energy `λ·Φ` has a minimum at `x⋆` that is sharp of
modulus `s` for the cost `d(x⋆, ·)`, then for every ensemble `ν`
`s · E_ν d(x⋆, ·) ≤ Σ |λ_i| · |data_i(ν) − Φ_i(x⋆)|`. -/
theorem transport_le_of_sharp
    (d : X → X → ℝ) (Φ : ι → X → ℝ) (lam : ι → ℝ) (xs : X) (s : ℝ)
    (hsharp : ∀ y, s * d xs y ≤ energy lam Φ y - energy lam Φ xs)
    (ν : X → ℝ) (hν : IsEnsemble ν) :
    s * ∑ y, ν y * d xs y ≤ ∑ i, |lam i| * |mean ν (Φ i) - Φ i xs| := by
  have h1 : s * ∑ y, ν y * d xs y ≤ ∑ y, ν y * (energy lam Φ y - energy lam Φ xs) := by
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun y _ => ?_
    have h := mul_le_mul_of_nonneg_left (hsharp y) (hν.nonneg y)
    have e : s * (ν y * d xs y) = ν y * (s * d xs y) := by ring
    rw [e]
    exact h
  have h2 : ∑ y, ν y * (energy lam Φ y - energy lam Φ xs) =
      ∑ i, lam i * (mean ν (Φ i) - Φ i xs) := by
    have e : ∑ y, ν y * (energy lam Φ y - energy lam Φ xs) =
        mean ν (energy lam Φ) - energy lam Φ xs * ∑ y, ν y := by
      unfold mean
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun y _ => by ring
    rw [e, hν.sum_one, mul_one, mean_energy]
    unfold energy
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun i _ => by ring
  have h3 : ∑ i, lam i * (mean ν (Φ i) - Φ i xs) ≤
      ∑ i, |lam i| * |mean ν (Φ i) - Φ i xs| :=
    Finset.sum_le_sum fun i _ => by
      rw [← abs_mul]
      exact le_abs_self _
  linarith

/-- **A certificate of robust optimality is a certificate of ensemble identification.**
Suppose `x⋆` minimises `λ·Φ + g` for every residual `g` admissible for the envelope `d` (the
hypothesis of the theory division's Theorem 2.4, `robust_certified_iff`).  Then for every
ensemble `ν` the transport cost `E_ν d(x⋆, ·)` from the conformation `x⋆` to `ν` is at most
`Σ |λ_i| · |data_i(ν) − Φ_i(x⋆)|`: the data of `Φ` identify the conformation, with a modulus
that is linear in the error of the data. -/
theorem identification_of_robust_certificate {d : X → X → ℝ} (hd : IsEnvelope d)
    (Φ : ι → X → ℝ) (lam : ι → ℝ) (xs : X)
    (hcert : ∀ g, Admissible d g → ∀ y, energy lam Φ xs + g xs ≤ energy lam Φ y + g y)
    (ν : X → ℝ) (hν : IsEnsemble ν) :
    ∑ y, ν y * d xs y ≤ ∑ i, |lam i| * |mean ν (Φ i) - Φ i xs| := by
  have hsharp := (robust_certified_iff hd (energy lam Φ) xs).mp hcert
  have h := transport_le_of_sharp d Φ lam xs 1 (fun y => by rw [one_mul]; exact hsharp y) ν hν
  rw [one_mul] at h
  exact h

omit [Fintype X] in
/-- The converse direction of the bridge, at the level of certificates: a sharp energy in the
span certifies robust optimality (this is `robust_certified_iff` read from right to left). -/
theorem robust_certificate_of_sharp {d : X → X → ℝ} (hd : IsEnvelope d)
    (Φ : ι → X → ℝ) (lam : ι → ℝ) (xs : X)
    (hsharp : ∀ y, d xs y ≤ energy lam Φ y - energy lam Φ xs) :
    ∀ g, Admissible d g → ∀ y, energy lam Φ xs + g xs ≤ energy lam Φ y + g y :=
  (robust_certified_iff hd (energy lam Φ) xs).mpr hsharp

/-- **The residual's side of the same statement.**  Under the hypothesis of
`identification_of_robust_certificate`, no admissible residual `g` gives an ensemble `ν` a mean
residual energy below `g(x⋆)` by more than `Σ |λ_i| · |data_i(ν) − Φ_i(x⋆)|`. -/
theorem residual_advantage_le {d : X → X → ℝ} (hd : IsEnvelope d)
    (Φ : ι → X → ℝ) (lam : ι → ℝ) (xs : X)
    (hcert : ∀ g, Admissible d g → ∀ y, energy lam Φ xs + g xs ≤ energy lam Φ y + g y)
    (ν : X → ℝ) (hν : IsEnsemble ν) (g : X → ℝ) (hg : Admissible d g) :
    g xs - mean ν g ≤ ∑ i, |lam i| * |mean ν (Φ i) - Φ i xs| := by
  have h1 : g xs - mean ν g = ∑ y, ν y * (g xs - g y) := by
    unfold mean
    have e : ∑ y, ν y * (g xs - g y) = g xs * ∑ y, ν y - ∑ y, ν y * g y := by
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun y _ => by ring
    rw [e, hν.sum_one, mul_one]
  have h2 : ∑ y, ν y * (g xs - g y) ≤ ∑ y, ν y * d xs y :=
    Finset.sum_le_sum fun y _ => mul_le_mul_of_nonneg_left (hg xs y) (hν.nonneg y)
  have h3 := identification_of_robust_certificate hd Φ lam xs hcert ν hν
  linarith

end MetricChain.Ensemble
