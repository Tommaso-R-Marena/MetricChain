import Mathlib

/-!
# The relaxation principle for nested hidden partitions: arithmetic core

Phase II (adaptive hierarchy), `docs/phase2_hierarchy/HIERARCHY_ADDENDUM.md` (Theorem P).

Types are vectors of class densities `z`; `r` is the rate, `F` a `u`-Lipschitz profile, `𝒢₁ ≤ 𝒢₂` two
partitions of the classes.  For a type `y` hidden from the third batch the proof of Theorem P uses three
points:

* `e`  — `y` with every class clipped towards `1/2` at a level `ℓ ≤ κ` (two-sided),
* `m'` — the `𝒢₂`-cell means of `e`, clipped at `κ`,
* `e'` — `e` with the lowest classes of every deep cell raised until the cell mean is `m'`,

and the chain  `F(y) ≈ F(e')` (Lipschitz), `F(e') = F(m')` (second batch saw nothing but `𝒢₂` there),
`F(m') = F(p)`, `p = avg₁ m'` (first batch saw nothing but `𝒢₁` there), and the cap at `p`.

This file checks the bookkeeping of that chain and the per-cell price inequality, with the analytic inputs
(monotonicity of `χ`, the chain rule for relative entropy, `T(e') ≤ T(e)`) as hypotheses.

* `cell_price_central`, `cell_price_deep` — the per-cell inequality
  `price(y_g → e_g) + price(m_g → m'_g) ≤ φ_g · h` in its two cases.
* `partition_chain` — the bound `−F(y) − r(y) ≤ ν₀ + h − θ`.
* `visible_of_fill` — the anchor `e'` is visible to the second batch.
-/

namespace MetricChain.PartitionChain

/-- Per-cell price, the cell mean of `e` already lies in `[κ, 1 − κ]`: the classes moved (weight `μ ≤ φ`)
each pay at most `c = max(χ(ℓ), 0) ≤ h`. -/
theorem cell_price_central (S μ φ c h : ℝ) (hμ0 : 0 ≤ μ) (hμ : μ ≤ φ)
    (hS : S ≤ μ * c) (hc0 : 0 ≤ c) (hc : c ≤ h) : S ≤ φ * h := by
  have h1 : μ * c ≤ φ * c := mul_le_mul_of_nonneg_right hμ hc0
  have hφ : 0 ≤ φ := le_trans hμ0 hμ
  have h2 : φ * c ≤ φ * h := mul_le_mul_of_nonneg_left hc hφ
  linarith

/-- Per-cell price, the cell mean `m` of `e` is deep (`m < κ`): moving the mean to `κ` costs
`φ (h − χ(m))`, and the classes moved pay at most `μ c` with `c = max(χ(ℓ), 0) ≤ χ(m)` because
`ℓ ≤ m < κ` and `χ` is nondecreasing on `[p_u, 1/2]`. -/
theorem cell_price_deep (S μ φ c χm h : ℝ) (hμ0 : 0 ≤ μ) (hμ : μ ≤ φ)
    (hS : S ≤ μ * c) (hc0 : 0 ≤ c) (hc : c ≤ χm) : S + φ * (h - χm) ≤ φ * h := by
  have h1 : μ * c ≤ φ * c := mul_le_mul_of_nonneg_right hμ hc0
  have hφ : 0 ≤ φ := le_trans hμ0 hμ
  have h2 : φ * c ≤ φ * χm := mul_le_mul_of_nonneg_left hc hφ
  nlinarith

/-- The anchor `e'` is visible to the second batch: its cost for that batch is `T(e') + Q(m')`, the fill
does not increase the within-cell cost, and the level was chosen with `T(e) + Q(m') = θ`. -/
theorem visible_of_fill (Te Te' Qm' θ : ℝ) (hfill : Te' ≤ Te) (hlevel : Te + Qm' = θ) :
    Te' + Qm' ≤ θ := by linarith

/-- Bookkeeping of Theorem P.

`Fy, Fe', Fm', Fp` are the values of the profile at `y, e', m', p = avg₁ m'`;
`ry, re, rm, rm', rp` the rates of `y, e, m = avg₂ e, m', p`;
`dye = ‖y − e‖`, `dmm = ‖m − m'‖ = ‖e − e'‖`; `Te = T(e)`, `Qm' = Q(m')`. -/
theorem partition_chain (Fy Fe' Fm' Fp ry re rm rm' rp dye dmm Te Qm' u h θ ν₀ : ℝ)
    (hLip : -Fy ≤ -Fe' + u * (dye + dmm))
    (hH2 : Fe' = Fm')
    (hH1 : Fm' = Fp)
    (hcap : -Fp - rp ≤ ν₀)
    (hT : Te = re - rm)
    (hQ : Qm' = rm' - rp)
    (hprice : (re - ry + u * dye) + (rm' - rm + u * dmm) ≤ h)
    (hlevel : Te + Qm' = θ) :
    -Fy - ry ≤ ν₀ + h - θ := by
  subst hH2 hH1
  linarith

end MetricChain.PartitionChain
