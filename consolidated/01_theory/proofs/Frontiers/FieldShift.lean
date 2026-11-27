import proofs.Frontiers.HintRecursion

/-!
# The shift identity with a known field

Theory report §11.20 (workstream F; `docs/workstreams/F_REPORT.md`).  On the cube with the
`p`-biased product measure `π = Bernoulli(p)^{⊗n}` — the Gibbs measure of a known part
`f = θ|x|` — let `S` be the letter of a cone centre (`P(S = 1) = m`) and `X` the letter of a
point, with `x = P(X = 0 | S = 1)` and `y = P(X = 1 | S = 0)` the two flip fractions.

* `klBin_tilt` generalises `klBin_shift` of `HintRecursion.lean` (the case `q0 = 1/2`): tilting
  the two-point law `(q0, 1 − q0)` by `e^{−u}` on the first point changes the relative entropy
  by `u x + ln(1 − q0 + q0 e^{−u})`.
* `cone_rate_eq`: the rate function of the cone law `π_s` at a profile equals the rate
  function of the reference measure plus `u·`(distance) minus the soft gap `Λ_m`.
* `sphere_rate_eq`: the chain rule `D(P_{X|S} ‖ π | P_S) = I(S;X) + KL(P_X ‖ π)`.
* `shift_identity`: together,

    `D(P_{X|S} ‖ π_s | P_S) = I(S;X) + KL(P_X ‖ π) + u·P(X ≠ S) − Λ(P_S)`,

  i.e. *non-adaptive accuracy = exponent of the sample + `KL(P_X ‖ π)` + hinted accuracy at
  the zero residual*.  The middle term vanishes at the optimum when `p = 1/2`; with a field it
  does not, which is why the hinted partner of the non-adaptive exponent is the exponent of
  the hardest additive instance and not that of the zero residual (theory report §11.20).

Only these identities are machine-checked; every statement about algorithms and exponents
with a field is a paper proof.
-/

namespace MetricChain
namespace FieldShift

open MetricChain.HintRecursion

/-- Binary entropy. -/
noncomputable def hBin (z : ℝ) : ℝ := -(z * Real.log z) - (1 - z) * Real.log (1 - z)

/-- Tilting a two-point law: `KL(x ‖ q0 e^{-u}/Z) = KL(x ‖ q0) + u x + ln Z`, `Z = 1 - q0 + q0 e^{-u}`. -/
theorem klBin_tilt {x q0 u : ℝ} (hx0 : 0 < x) (hx1 : x < 1) (hq0 : 0 < q0) (hq1 : q0 < 1) :
    klBin x (q0 * Real.exp (-u) / (1 - q0 + q0 * Real.exp (-u)))
      = klBin x q0 + u * x + Real.log (1 - q0 + q0 * Real.exp (-u)) := by
  have he : 0 < Real.exp (-u) := Real.exp_pos (-u)
  have h1q : 0 < 1 - q0 := by linarith
  have h1x : 0 < 1 - x := by linarith
  have hZ : 0 < 1 - q0 + q0 * Real.exp (-u) := by positivity
  have hcomp : 1 - q0 * Real.exp (-u) / (1 - q0 + q0 * Real.exp (-u))
      = (1 - q0) / (1 - q0 + q0 * Real.exp (-u)) := by
    field_simp
    ring
  unfold klBin
  rw [hcomp]
  have e1 : x / (q0 * Real.exp (-u) / (1 - q0 + q0 * Real.exp (-u)))
      = x * (1 - q0 + q0 * Real.exp (-u)) / (q0 * Real.exp (-u)) := by
    field_simp
  have e2 : (1 - x) / ((1 - q0) / (1 - q0 + q0 * Real.exp (-u)))
      = (1 - x) * (1 - q0 + q0 * Real.exp (-u)) / (1 - q0) := by
    field_simp
  rw [e1, e2]
  rw [Real.log_div (by positivity) (by positivity), Real.log_mul hx0.ne' hZ.ne',
    Real.log_mul hq0.ne' he.ne', Real.log_exp,
    Real.log_div (by positivity) h1q.ne', Real.log_mul h1x.ne' hZ.ne',
    Real.log_div hx0.ne' hq0.ne', Real.log_div h1x.ne' h1q.ne']
  ring

/-- The cone law of one site with centre letter `1`: flip probability `η₁ = q e^{-u}/(p + q e^{-u})`
(`q = 1 - p`), and with centre letter `0`: `η₀ = p e^{-u}/(q + p e^{-u})`.  The rate function of
the cone law at the profile `(x, y)` is `J + u (m x + (1 - m) y) - Λ_m`. -/
theorem cone_rate_eq {m x y p u : ℝ} (hx0 : 0 < x) (hx1 : x < 1) (hy0 : 0 < y) (hy1 : y < 1)
    (hp0 : 0 < p) (hp1 : p < 1) :
    m * klBin x ((1 - p) * Real.exp (-u) / (p + (1 - p) * Real.exp (-u)))
        + (1 - m) * klBin y (p * Real.exp (-u) / (1 - p + p * Real.exp (-u)))
      = (m * klBin x (1 - p) + (1 - m) * klBin y p) + u * (m * x + (1 - m) * y)
        - (m * (-Real.log (p + (1 - p) * Real.exp (-u)))
            + (1 - m) * (-Real.log (1 - p + p * Real.exp (-u)))) := by
  have h1 := klBin_tilt (x := x) (q0 := 1 - p) (u := u) hx0 hx1 (by linarith) (by linarith)
  have h2 := klBin_tilt (x := y) (q0 := p) (u := u) hy0 hy1 hp0 hp1
  have e : (1 : ℝ) - (1 - p) + (1 - p) * Real.exp (-u) = p + (1 - p) * Real.exp (-u) := by ring
  rw [e] at h1
  rw [h1, h2]
  ring

/-- Chain rule: `J = I(S;X) + KL(κ ‖ p)` with `I = h(κ) - m h(x) - (1 - m) h(y)`,
`κ = m (1 - x) + (1 - m) y`. -/
theorem sphere_rate_eq {m x y p : ℝ} (hx0 : 0 < x) (hx1 : x < 1) (hy0 : 0 < y) (hy1 : y < 1)
    (hp0 : 0 < p) (hp1 : p < 1) (hκ0 : 0 < m * (1 - x) + (1 - m) * y)
    (hκ1 : m * (1 - x) + (1 - m) * y < 1) :
    m * klBin x (1 - p) + (1 - m) * klBin y p
      = (hBin (m * (1 - x) + (1 - m) * y) - m * hBin x - (1 - m) * hBin y)
        + klBin (m * (1 - x) + (1 - m) * y) p := by
  have h1x : 0 < 1 - x := by linarith
  have h1y : 0 < 1 - y := by linarith
  have h1p : 0 < 1 - p := by linarith
  have h1κ : 0 < 1 - (m * (1 - x) + (1 - m) * y) := by linarith
  have e : (1 : ℝ) - (1 - p) = p := by ring
  unfold klBin hBin
  rw [e]
  rw [Real.log_div hx0.ne' h1p.ne', Real.log_div h1x.ne' hp0.ne',
    Real.log_div hy0.ne' hp0.ne', Real.log_div h1y.ne' h1p.ne',
    Real.log_div hκ0.ne' hp0.ne', Real.log_div h1κ.ne' h1p.ne']
  ring

/-- **The shift identity with a field.**  Non-adaptive accuracy (rate of the cone law) = exponent of
the sample `I` + `KL(P_X ‖ π)` + hinted accuracy `u ρ - Λ_m`. -/
theorem shift_identity {m x y p u : ℝ} (hx0 : 0 < x) (hx1 : x < 1) (hy0 : 0 < y) (hy1 : y < 1)
    (hp0 : 0 < p) (hp1 : p < 1) (hκ0 : 0 < m * (1 - x) + (1 - m) * y)
    (hκ1 : m * (1 - x) + (1 - m) * y < 1) :
    m * klBin x ((1 - p) * Real.exp (-u) / (p + (1 - p) * Real.exp (-u)))
        + (1 - m) * klBin y (p * Real.exp (-u) / (1 - p + p * Real.exp (-u)))
      = (hBin (m * (1 - x) + (1 - m) * y) - m * hBin x - (1 - m) * hBin y)
        + klBin (m * (1 - x) + (1 - m) * y) p
        + (u * (m * x + (1 - m) * y)
            - (m * (-Real.log (p + (1 - p) * Real.exp (-u)))
              + (1 - m) * (-Real.log (1 - p + p * Real.exp (-u))))) := by
  rw [cone_rate_eq hx0 hx1 hy0 hy1 hp0 hp1, sphere_rate_eq hx0 hx1 hy0 hy1 hp0 hp1 hκ0 hκ1]
  ring

end FieldShift
end MetricChain
