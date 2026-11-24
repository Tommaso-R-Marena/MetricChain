import Mathlib
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.CertificateComplexity
import proofs.Frontiers.ThermalRobustness
import proofs.Frontiers.ExponentialWeights

/-!
# Product landscapes: the exponential-weights converses factorise over the sites

Setting of `CertificateComplexity.lean` (Parts 2 and 3): configurations are `x : ∀ i, σ i`
(finitely many sites `i` with finite state spaces `σ i`), the envelope is the weighted Hamming
envelope `hamEnv c x y = ∑ i, if x i = y i then 0 else c i`, and here both the known part and the
residual are site-additive,

  `f x = ∑ i, φ i (x i)`,      `g x = ∑ i, γ i (x i)`,      `E = f + g`.

`ExponentialWeights.lean` bounds the number of evaluations `|A|` from below by a ratio of two
weighted sums over configurations, for an arbitrary nonnegative weight on configurations.  For a
**product weight** `∏ i, v i (y i)` everything in those bounds is a product over the sites:

* `slack_hamEnv_additive` — the slack is the sum of the site slacks
  `s_i(a, s) = c i · [a ≠ s] - γ i a + γ i s`;
* `sum_prod_mul_exp_sum` — a product weight times the exponential of a site-additive function sums
  to the product of the site sums,
  `∑ y, (∏ i, v i (y i)) · exp (-t ∑ i, F i (y i)) = ∏ i, ∑ s, v i s · exp (-t F i s)`;
* `gibbsProb_additive`, `gibbsProb_additive_add` — the Gibbs ensemble of a site-additive energy is
  the product of the site Gibbs ensembles `π_i = gibbsProb β (φ i + γ i)`.

So the converses become statements about one site at a time, and the logarithm of the number of
evaluations is bounded below by a sum of site rates.

## Zero temperature

Let `estar i` be a lower bound on the site energy `φ i + γ i`, with site gap
`gap_i s = φ i s + γ i s - estar i`, and let `v i ≥ 0` be site weights with total
`V_i = ∑ s, v i s`.

* `product_exp_weights` — for every `t ≥ 0`, if `B i` bounds the weighted site sums
  `∑ s, v i s · exp (-t (s_i(a, s) - gap_i s))` for all states `a` of site `i`, then every
  `ε`-certificate `A` satisfies `exp (-t ε) · ∏ i, V_i ≤ |A| · ∏ i, B i`.
* `product_rate_bound` — the same in logarithmic form:
  `∑ i, (log V_i - log (B i)) - t ε ≤ log |A|`.

Each site contributes its own rate `log V_i - log (B i)`; for `n` identical sites the bound is
`n · (log V - log B) - t ε`, so for a fixed tolerance the certificate grows exponentially in `n`
as soon as one choice of `t` and `v` makes the rate of a single site positive.  The Boltzmann
weights `v i s = exp (-t · gap_i s)` give the product form of `partition_bound`; for `γ = 0` and
`estar i` the site minimum this is `product_partition_bound`.

## Finite temperature

Here an evaluated set `A` is called a free-energy certificate of accuracy `ε` when its optimistic
partition function (that of `f` plus the lower McShane envelope of the evaluations) is within the
factor `exp ε` of the true one.  This is the hypothesis of the finite-temperature theorems of
`ExponentialWeights.lean`; it holds whenever the two envelope partition functions, which are
computable from the evaluations, agree up to the factor `exp ε` (`Zhi_le_of_bracket`, for an
admissible residual and `β ≥ 0`).

* `thermal_product_exp_weights` — for `p ∈ (0, 1)` and `t = β (1 - p) / p`, if `B i` bounds the
  site sums `∑ s, v i s · exp (-t · s_i(a, s))` for all states `a` of site `i`, then
  `∏ i, ∑ s, π_i s ^ (1 - p) · v i s ^ p ≤ (|A| · ∏ i, B i) ^ p · exp ((1 - p) ε)`.
* `product_entropy_bound` — for an arbitrary known part and a residual that is `κ`-Lipschitz for
  `hamEnv c` (neither has to be site-additive), the entropy of the Gibbs ensemble satisfies
  `H(π) ≤ log |A| + ∑ i, log (1 + (|σ i| - 1) · exp (-t (1 - κ) c i)) + t ε / β`.
* `full_evaluation_partition_eq` — the hypothesis of the finite-temperature theorems is
  satisfiable: evaluating every configuration gives `ε = 0`.

## A sharp landscape whose free-energy certificates are exponentially large

Take `n` two-state sites with excitation energy `2`, envelope constants `1`, zero residual, and
the inverse temperature `β = log 2`.

* `thermal_binary_sharp` — every site is sharp (the excitation energy is at least the envelope
  constant), so the single evaluation of the ground state is an exact zero-temperature
  certificate; and all `2 ^ n` configurations together are an exact free-energy certificate.
* `thermal_binary_exponential` — nevertheless every free-energy certificate of accuracy `ε` has
  at least `exp (-ε) · (6/5) ^ n` evaluations (`thermal_product_exp_weights` at `p = 1/2` with
  `v = 1`: the site Gibbs measure is `(4/5, 1/5)`, `∑ s, π s ^ (1/2) = 3 / √5` and `B = 3/2`).
* `thermal_binary_single_tight` — the bound is attained: the single evaluation of the ground state
  is a free-energy certificate of accuracy exactly `ε = n · log (6/5)`.

At zero temperature one evaluation certifies this landscape for every `n`; at the inverse
temperature `β = log 2` a certificate of the free energy to within `ε = o(n)` needs exponentially
many evaluations.  A free-energy certificate has to resolve the thermally populated
configurations (compare `product_entropy_bound`); the sharpness of the ground state does not help.
-/

namespace MetricChain

open Finset

/-! ### Site-additive structure -/

section Product

variable {ι : Type*} [Fintype ι] {σ : ι → Type*} [∀ i, DecidableEq (σ i)]

/-- **The slack of a site-additive residual is site-additive.**  For the weighted Hamming envelope
and the residual `∑ i, γ i (x i)`, the slack between `a` and `y` is the sum over the sites of the
site slacks `(if a i = y i then 0 else c i) - γ i (a i) + γ i (y i)`. -/
theorem slack_hamEnv_additive (c : ι → ℝ) (γ : ∀ i, σ i → ℝ) (a y : ∀ i, σ i) :
    slack (hamEnv c) (fun x => ∑ i, γ i (x i)) a y =
      ∑ i, ((if a i = y i then 0 else c i) - γ i (a i) + γ i (y i)) := by
  unfold slack hamEnv
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]

variable [DecidableEq ι] [∀ i, Fintype (σ i)]

omit [∀ i, DecidableEq (σ i)] in
/-- **Weighted partition sums of site-additive functions factorise.**  For a product weight
`∏ i, v i (y i)` and a site-additive exponent `∑ i, F i (y i)`, the sum over all configurations is
the product of the site sums `∑ s, v i s * exp (-t * F i s)` (`Fintype.prod_sum`). -/
theorem sum_prod_mul_exp_sum (v F : ∀ i, σ i → ℝ) (t : ℝ) :
    ∑ y : ∀ i, σ i, (∏ i, v i (y i)) * Real.exp (-t * ∑ i, F i (y i)) =
      ∏ i, ∑ s, v i s * Real.exp (-t * F i s) := by
  rw [Fintype.prod_sum]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [Finset.prod_mul_distrib, ← Real.exp_sum, Finset.mul_sum]

omit [∀ i, DecidableEq (σ i)] in
/-- **The Gibbs ensemble of a site-additive energy is a product measure.**  For the energy
`∑ i, e i (x i)` the Gibbs probability of a configuration is the product of the site Gibbs
probabilities: the Boltzmann weight is the exponential of a sum, and the partition function is the
product of the site partition functions (`Fintype.prod_sum`). -/
theorem gibbsProb_additive (β : ℝ) (e : ∀ i, σ i → ℝ) (x : ∀ i, σ i) :
    gibbsProb β (fun y : ∀ i, σ i => ∑ i, e i (y i)) x = ∏ i, gibbsProb β (e i) (x i) := by
  unfold gibbsProb
  rw [Finset.prod_div_distrib, Fintype.prod_sum]
  congr 1
  · rw [Finset.mul_sum, Real.exp_sum]
  · refine Finset.sum_congr rfl fun y _ => ?_
    rw [Finset.mul_sum, Real.exp_sum]

omit [∀ i, DecidableEq (σ i)] in
/-- `gibbsProb_additive` for the energy `f + g` with a site-additive known part
`f x = ∑ i, φ i (x i)` and a site-additive residual `g x = ∑ i, γ i (x i)`: the Gibbs ensemble is
the product of the site ensembles `gibbsProb β (φ i + γ i)`. -/
theorem gibbsProb_additive_add (β : ℝ) (φ γ : ∀ i, σ i → ℝ) (x : ∀ i, σ i) :
    gibbsProb β (fun y : ∀ i, σ i => ∑ i, φ i (y i) + ∑ i, γ i (y i)) x =
      ∏ i, gibbsProb β (fun s => φ i s + γ i s) (x i) := by
  rw [← gibbsProb_additive β (fun i s => φ i s + γ i s) x]
  congr 1
  funext y
  rw [Finset.sum_add_distrib]

/-! ### Zero temperature: product weights -/

/-- **Exponential-weights converse on product landscapes (zero temperature).**  Sites `i` with
state spaces `σ i`, known part `∑ i, φ i (x i)`, residual `∑ i, γ i (x i)`, envelope `hamEnv c`.
Let `estar i` be a lower bound on the site energy `φ i + γ i`, let `v i ≥ 0` be site weights,
`t ≥ 0`, and let `B i` bound, for every state `a` of site `i`, the weighted site sum

  `∑ s, v i s * exp (-t * (s_i(a, s) - gap_i s))`,

where `s_i(a, s) = (if a = s then 0 else c i) - γ i a + γ i s` is the site slack and
`gap_i s = φ i s + γ i s - estar i` the site gap.  Then every `ε`-certificate `A` satisfies

  `exp (-t ε) * ∏ i, ∑ s, v i s ≤ |A| * ∏ i, B i`.

This is `card_ge_exp_weights_certificate` for the product weight `∏ i, v i (y i)` and
`Estar = ∑ i, estar i`: slack and gap are sums over the sites, so the weighted partition sum of
every evaluated point is the product of its site sums (`sum_prod_mul_exp_sum`). -/
theorem product_exp_weights [∀ i, Nonempty (σ i)] (c : ι → ℝ) (φ γ v : ∀ i, σ i → ℝ)
    (hv : ∀ i s, 0 ≤ v i s) (estar : ι → ℝ) (hestar : ∀ i s, estar i ≤ φ i s + γ i s) {t : ℝ}
    (ht : 0 ≤ t) (B : ι → ℝ)
    (hB : ∀ i (a : σ i), ∑ s, v i s * Real.exp (-t * ((if a = s then 0 else c i) - γ i a + γ i s -
      (φ i s + γ i s - estar i))) ≤ B i)
    {A : Finset (∀ i, σ i)} {hA : A.Nonempty} {ε : ℝ}
    (hcert : IsCertificate (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun x => ∑ i, γ i (x i)) A hA
      ε) :
    Real.exp (-t * ε) * ∏ i, ∑ s, v i s ≤ A.card * ∏ i, B i := by
  have hE : ∀ y : ∀ i, σ i, ∑ i, estar i ≤ ∑ i, φ i (y i) + ∑ i, γ i (y i) := by
    intro y
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_le_sum fun i _ => hestar i (y i)
  have key := card_ge_exp_weights_certificate ht (fun y : ∀ i, σ i => ∏ i, v i (y i))
    (fun y => Finset.prod_nonneg fun i _ => hv i (y i)) hE hcert (B := ∏ i, B i) (fun a _ => ?_)
  · rwa [← Fintype.prod_sum] at key
  · have hexp : ∀ y : ∀ i, σ i, slack (hamEnv c) (fun x => ∑ i, γ i (x i)) a y -
        (∑ i, φ i (y i) + ∑ i, γ i (y i) - ∑ i, estar i) =
        ∑ i, ((if a i = y i then 0 else c i) - γ i (a i) + γ i (y i) -
          (φ i (y i) + γ i (y i) - estar i)) := by
      intro y
      rw [slack_hamEnv_additive, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib,
        ← Finset.sum_sub_distrib]
    simp only [hexp]
    rw [sum_prod_mul_exp_sum v (fun i s => (if a i = s then 0 else c i) - γ i (a i) + γ i s -
      (φ i s + γ i s - estar i)) t]
    exact Finset.prod_le_prod
      (fun i _ => Finset.sum_nonneg fun s _ => mul_nonneg (hv i s) (Real.exp_pos _).le)
      (fun i _ => hB i (a i))

/-- **Rate form of the product converse.**  In the setting of `product_exp_weights`, if every site
has positive total weight `∑ s, v i s`, then every `ε`-certificate `A` satisfies

  `∑ i, (log (∑ s, v i s) - log (B i)) - t ε ≤ log |A|`.

The logarithm of the number of evaluations is at least the sum of the site rates
`log (∑ s, v i s) - log (B i)`, up to the term `t ε`.  (The bounds `B i` are automatically
positive: each is at least a sum of nonnegative terms one of which is positive.) -/
theorem product_rate_bound [∀ i, Nonempty (σ i)] (c : ι → ℝ) (φ γ v : ∀ i, σ i → ℝ)
    (hv : ∀ i s, 0 ≤ v i s) (hV : ∀ i, 0 < ∑ s, v i s) (estar : ι → ℝ)
    (hestar : ∀ i s, estar i ≤ φ i s + γ i s) {t : ℝ} (ht : 0 ≤ t) (B : ι → ℝ)
    (hB : ∀ i (a : σ i), ∑ s, v i s * Real.exp (-t * ((if a = s then 0 else c i) - γ i a + γ i s -
      (φ i s + γ i s - estar i))) ≤ B i)
    {A : Finset (∀ i, σ i)} {hA : A.Nonempty} {ε : ℝ}
    (hcert : IsCertificate (hamEnv c) (fun x => ∑ i, φ i (x i)) (fun x => ∑ i, γ i (x i)) A hA
      ε) :
    ∑ i, (Real.log (∑ s, v i s) - Real.log (B i)) - t * ε ≤ Real.log A.card := by
  have hB0 : ∀ i, 0 < B i := by
    intro i
    obtain ⟨s, -, hs⟩ := (Finset.sum_pos_iff_of_nonneg fun s _ => hv i s).mp (hV i)
    exact lt_of_lt_of_le
      (Finset.sum_pos' (fun s _ => mul_nonneg (hv i s) (Real.exp_pos _).le)
        ⟨s, mem_univ s, mul_pos hs (Real.exp_pos _)⟩)
      (hB i (Classical.arbitrary (σ i)))
  have h := product_exp_weights c φ γ v hv estar hestar ht B hB hcert
  have hcard : (0 : ℝ) < A.card := by exact_mod_cast Finset.card_pos.mpr hA
  have hVpos : 0 < ∏ i, ∑ s, v i s := Finset.prod_pos fun i _ => hV i
  have hBpos : 0 < ∏ i, B i := Finset.prod_pos fun i _ => hB0 i
  have hlog := Real.log_le_log (mul_pos (Real.exp_pos _) hVpos) h
  rw [Real.log_mul (Real.exp_pos _).ne' hVpos.ne', Real.log_mul hcard.ne' hBpos.ne',
    Real.log_exp, Real.log_prod fun i _ => (hV i).ne', Real.log_prod fun i _ => (hB0 i).ne']
    at hlog
  rw [Finset.sum_sub_distrib]
  linarith

/-! ### Finite temperature: product weights -/

/-- **Exponential-weights converse on product landscapes (finite temperature).**  Sites `i` with
state spaces `σ i`, known part `f x = ∑ i, φ i (x i)`, residual `g x = ∑ i, γ i (x i)`, envelope
`hamEnv c`, and site Gibbs measures `π_i = gibbsProb β (φ i + γ i)`.  Let the optimistic partition
function of the evaluated set `A` be within the factor `exp ε` of the true one.  For `p ∈ (0, 1)`
put `t = β (1 - p) / p`, let `v i ≥ 0` be site weights and let `B i` bound, for every state `a` of
site `i`, the weighted site sum `∑ s, v i s * exp (-t * s_i(a, s))` of the site slack
`s_i(a, s) = (if a = s then 0 else c i) - γ i a + γ i s`.  Then

  `∏ i, ∑ s, π_i s ^ (1 - p) * v i s ^ p ≤ (|A| * ∏ i, B i) ^ p * exp ((1 - p) ε)`.

This is `thermal_exp_weights` for the product weight `∏ i, v i (y i)`: the Gibbs ensemble is the
product of the site ensembles (`gibbsProb_additive_add`), powers of products of nonnegative
numbers are products of powers, and the weighted slack partition sums factorise
(`slack_hamEnv_additive`, `sum_prod_mul_exp_sum`).  No sign condition on the bounds `B i` is
needed. -/
theorem thermal_product_exp_weights (c : ι → ℝ) (φ γ : ∀ i, σ i → ℝ) (A : Finset (∀ i, σ i))
    (hA : A.Nonempty) {β ε p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (v : ∀ i, σ i → ℝ)
    (hv : ∀ i s, 0 ≤ v i s) (B : ι → ℝ)
    (hcert : ∑ y : ∀ i, σ i, Real.exp (-β * (∑ i, φ i (y i) +
        lowerEnv (hamEnv c) A hA (fun x => ∑ i, γ i (x i)) y)) ≤
      Real.exp ε * ∑ y : ∀ i, σ i, Real.exp (-β * (∑ i, φ i (y i) + ∑ i, γ i (y i))))
    (hB : ∀ i (a : σ i), ∑ s, v i s * Real.exp (-(β * (1 - p) / p) *
      ((if a = s then 0 else c i) - γ i a + γ i s)) ≤ B i) :
    ∏ i, ∑ s, gibbsProb β (fun s => φ i s + γ i s) s ^ (1 - p) * v i s ^ p ≤
      (A.card * ∏ i, B i) ^ p * Real.exp ((1 - p) * ε) := by
  have key := thermal_exp_weights (hamEnv c) (fun x => ∑ i, φ i (x i))
    (fun x => ∑ i, γ i (x i)) A hA hp0 hp1 (fun y : ∀ i, σ i => ∏ i, v i (y i))
    (fun y => Finset.prod_nonneg fun i _ => hv i (y i)) hcert (B := ∏ i, B i) (fun a _ => ?_)
  · have hL : ∀ y : ∀ i, σ i,
        gibbsProb β (fun y : ∀ i, σ i => ∑ i, φ i (y i) + ∑ i, γ i (y i)) y ^ (1 - p) *
          (∏ i, v i (y i)) ^ p =
        ∏ i, gibbsProb β (fun s => φ i s + γ i s) (y i) ^ (1 - p) * v i (y i) ^ p := by
      intro y
      rw [gibbsProb_additive_add,
        ← Real.finsetProd_rpow _ _ (fun i _ => gibbsProb_nonneg _ _ _),
        ← Real.finsetProd_rpow _ _ (fun i _ => hv i (y i)), Finset.prod_mul_distrib]
    rw [Fintype.prod_sum]
    simpa only [hL] using key
  · simp only [slack_hamEnv_additive]
    rw [sum_prod_mul_exp_sum v (fun i s => (if a i = s then 0 else c i) - γ i (a i) + γ i s)
      (β * (1 - p) / p)]
    exact Finset.prod_le_prod
      (fun i _ => Finset.sum_nonneg fun s _ => mul_nonneg (hv i s) (Real.exp_pos _).le)
      (fun i _ => hB i (a i))

/-- **Entropy bound for free-energy certificates under the weighted Hamming envelope.**  Let the
residual `g` be `κ`-Lipschitz for `hamEnv c` (the known part `f` is arbitrary; neither has to be
site-additive), let `β > 0`, and let the optimistic partition function of the evaluated set `A`
be within the factor `exp ε` of the true one.  Then for every `t ≥ 0` the Shannon entropy of the
Gibbs ensemble of `f + g` satisfies

  `H(π) ≤ log |A| + ∑ i, log (1 + (|σ i| - 1) * exp (-t * ((1 - κ) * c i))) + t ε / β`.

This is `card_ge_entropy` with the slack partition sums bounded as in `partition_bound_hamming`:
the slack dominates `hamEnv ((1 - κ) c)` (`slack_ge_of_lipschitz`), whose partition sum is the
product of `sum_exp_hamEnv`. -/
theorem product_entropy_bound (c : ι → ℝ) (f g : (∀ i, σ i) → ℝ) {κ : ℝ}
    (hgκ : ∀ x y, g x - g y ≤ κ * hamEnv c x y) (A : Finset (∀ i, σ i)) (hA : A.Nonempty)
    {β ε t : ℝ} (hβ : 0 < β) (ht : 0 ≤ t)
    (hcert : ∑ y, Real.exp (-β * (f y + lowerEnv (hamEnv c) A hA g y)) ≤
      Real.exp ε * ∑ y, Real.exp (-β * (f y + g y))) :
    -∑ y, gibbsProb β (fun y => f y + g y) y *
        Real.log (gibbsProb β (fun y => f y + g y) y) ≤
      Real.log A.card + ∑ i, Real.log (1 + ((Fintype.card (σ i) : ℝ) - 1) *
        Real.exp (-t * ((1 - κ) * c i))) + t * ε / β := by
  haveI : Nonempty (∀ i, σ i) := hA.to_type
  have hpos : ∀ i, 0 < 1 + ((Fintype.card (σ i) : ℝ) - 1) *
      Real.exp (-t * ((1 - κ) * c i)) := by
    intro i
    have hk1 : (1 : ℝ) ≤ (Fintype.card (σ i) : ℝ) := by
      exact_mod_cast Fintype.card_pos_iff.mpr (hA.to_type.map fun x => x i)
    have h0 := mul_nonneg (sub_nonneg.mpr hk1) (Real.exp_pos (-t * ((1 - κ) * c i))).le
    linarith
  have hcard : (0 : ℝ) < A.card := by exact_mod_cast Finset.card_pos.mpr hA
  have h := card_ge_entropy (hamEnv c) f g A hA hβ ht hcert
    (B := ∏ i, (1 + ((Fintype.card (σ i) : ℝ) - 1) * Real.exp (-t * ((1 - κ) * c i))))
    (fun a _ => by
      rw [← sum_exp_hamEnv (fun i => (1 - κ) * c i) t a]
      refine Finset.sum_le_sum fun y _ => Real.exp_le_exp.mpr ?_
      have h1 := slack_ge_of_lipschitz hgκ a y
      rw [hamEnv_mul] at h1
      exact mul_le_mul_of_nonpos_left h1 (by linarith))
  rwa [Real.log_mul hcard.ne' (Finset.prod_pos fun i _ => hpos i).ne',
    Real.log_prod fun i _ => (hpos i).ne'] at h

end Product

/-! ### Evaluating everything: the finite-temperature hypothesis is satisfiable -/

/-- **Evaluating everything is an exact free-energy certificate.**  For an envelope `d` and an
admissible residual `g`, the lower McShane envelope of the evaluations at all points is `g` itself
(`lowerEnv_eq_of_mem`), so the optimistic partition function equals the true one.  In particular
the hypothesis of `card_ge_entropy`, `thermal_exp_weights`, `thermal_product_exp_weights` and
`product_entropy_bound` is satisfiable, with `ε = 0`. -/
theorem full_evaluation_partition_eq {X : Type*} [Fintype X] [Nonempty X] {d : X → X → ℝ}
    (hd : IsEnvelope d) {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ) (β : ℝ) :
    ∑ y, Real.exp (-β * (f y + lowerEnv d univ univ_nonempty g y)) =
      ∑ y, Real.exp (-β * (f y + g y)) := by
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [lowerEnv_eq_of_mem hd univ univ_nonempty g (fun a _ b _ => hg a b) (mem_univ y)]

/-! ### A sharp landscape whose free-energy certificates are exponentially large -/

/-- **Exponentially many evaluations for a free-energy certificate of a sharp landscape.**  Take
`n` two-state sites, known part `f x = 2 · #{i | x i = true}` (ground state all `false`, every
excitation costs `2`), the weighted Hamming envelope with all constants equal to `1`, the zero
residual, and the inverse temperature `β = log 2`.  If the optimistic partition function of the
evaluated set `A` is within the factor `exp ε` of the true one, then

  `exp (-ε) * (6/5) ^ n ≤ |A|`.

By `Zhi_le_of_bracket` the hypothesis holds in particular when the two envelope partition
functions of `A`, which only involve the evaluations, agree up to the factor `exp ε`, that is,
when `A` certifies `log Z` to within `ε`.

This is `thermal_product_exp_weights` at `p = 1/2` (so `t = β = log 2`) with the weights `v = 1`:
the site Gibbs measure is `(4/5, 1/5)`, so `∑ s, π s ^ (1/2) = 3 / √5`, and the site slack sum is
`B = 1 + exp (-log 2) = 3/2`; squaring `(3 / √5) ^ n ≤ (|A| * (3/2) ^ n) ^ (1/2) * exp (ε / 2)`
gives `(9/5) ^ n ≤ |A| * (3/2) ^ n * exp ε`.

Every site of this landscape is sharp, so one evaluation certifies its ground state exactly, and
the hypothesis is satisfiable (`thermal_binary_sharp`); the bound is attained by the single
evaluation of the ground state (`thermal_binary_single_tight`). -/
theorem thermal_binary_exponential (n : ℕ) (A : Finset (Fin n → Bool)) (hA : A.Nonempty)
    {ε : ℝ}
    (hcert : ∑ y : Fin n → Bool, Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) +
        lowerEnv (hamEnv fun _ : Fin n => (1 : ℝ)) A hA (fun _ => 0) y)) ≤
      Real.exp ε * ∑ y : Fin n → Bool,
        Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) + 0))) :
    Real.exp (-ε) * (6 / 5 : ℝ) ^ n ≤ A.card := by
  have h2 : Real.exp (-Real.log 2) = 1 / 2 := by
    rw [Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have h4 : Real.exp (-Real.log 2 * 2) = 1 / 4 := by
    rw [show -Real.log 2 * 2 = -Real.log 2 + -Real.log 2 by ring, Real.exp_add, h2]
    norm_num
  -- the site Gibbs measure is `(4/5, 1/5)`
  have hπf : gibbsProb (Real.log 2) (fun s : Bool => (if s then (2 : ℝ) else 0) + 0) false =
      4 / 5 := by
    unfold gibbsProb
    rw [Fintype.sum_bool]
    simp only [Bool.false_eq_true, if_false, if_true, add_zero, mul_zero, Real.exp_zero, h4]
    norm_num
  have hπt : gibbsProb (Real.log 2) (fun s : Bool => (if s then (2 : ℝ) else 0) + 0) true =
      1 / 5 := by
    unfold gibbsProb
    rw [Fintype.sum_bool]
    simp only [Bool.false_eq_true, if_false, if_true, add_zero, mul_zero, Real.exp_zero, h4]
    norm_num
  -- the site sum `∑ s, π s ^ (1/2)` is `3 * √(1/5)`
  have hr0 : 0 ≤ Real.sqrt (1 / 5) := Real.sqrt_nonneg _
  have hr2 : Real.sqrt (1 / 5) ^ 2 = 1 / 5 := Real.sq_sqrt (by norm_num)
  have h45 : Real.sqrt (4 / 5) = 2 * Real.sqrt (1 / 5) := by
    rw [show (4 / 5 : ℝ) = 2 ^ 2 * (1 / 5) by norm_num, Real.sqrt_mul (by positivity),
      Real.sqrt_sq (by norm_num)]
  have hsite : ∑ s : Bool, gibbsProb (Real.log 2)
      (fun s : Bool => (if s then (2 : ℝ) else 0) + 0) s ^ ((1 : ℝ) - 1 / 2) *
        (1 : ℝ) ^ ((1 : ℝ) / 2) = 3 * Real.sqrt (1 / 5) := by
    rw [Fintype.sum_bool, hπf, hπt, Real.one_rpow, show (1 : ℝ) - 1 / 2 = 1 / 2 by norm_num,
      ← Real.sqrt_eq_rpow, ← Real.sqrt_eq_rpow, h45]
    ring
  -- `thermal_product_exp_weights` at `p = 1/2` with `v = 1` and `B = 3/2`
  have hB := thermal_product_exp_weights (fun _ : Fin n => (1 : ℝ))
    (fun _ (s : Bool) => if s then (2 : ℝ) else 0) (fun _ _ => 0) A hA (β := Real.log 2)
    (ε := ε) (p := 1 / 2) (by norm_num) (by norm_num) (fun _ _ => 1) (fun _ _ => zero_le_one)
    (fun _ => 3 / 2) (by simpa only [Finset.sum_const_zero] using hcert) (by
      intro i a
      rw [show Real.log 2 * (1 - 1 / 2) / (1 / 2) = Real.log 2 by ring, Fintype.sum_bool]
      cases a <;> norm_num [h2])
  simp only [hsite, Finset.prod_const, Finset.card_univ, Fintype.card_fin] at hB
  -- square both sides: `(9/5) ^ n ≤ |A| * (3/2) ^ n * exp ε`
  have hX0 : (0 : ℝ) ≤ A.card * (3 / 2) ^ n := by positivity
  have hsq := pow_le_pow_left₀ (pow_nonneg (mul_nonneg (by norm_num) hr0) n) hB 2
  have eL : ((3 * Real.sqrt (1 / 5)) ^ n) ^ 2 = (6 / 5 : ℝ) ^ n * (3 / 2) ^ n := by
    rw [← pow_mul, mul_comm n 2, pow_mul, mul_pow, hr2, ← mul_pow]
    norm_num
  have eR : (((A.card : ℝ) * (3 / 2) ^ n) ^ ((1 : ℝ) / 2) *
      Real.exp ((1 - 1 / 2) * ε)) ^ 2 = A.card * Real.exp ε * (3 / 2) ^ n := by
    rw [mul_pow, ← Real.sqrt_eq_rpow, Real.sq_sqrt hX0, sq (Real.exp _), ← Real.exp_add,
      show (1 - 1 / 2) * ε + (1 - 1 / 2) * ε = ε by ring]
    ring
  rw [eL, eR] at hsq
  have h6 : (6 / 5 : ℝ) ^ n ≤ A.card * Real.exp ε := le_of_mul_le_mul_right hsq (by positivity)
  calc Real.exp (-ε) * (6 / 5 : ℝ) ^ n
      ≤ Real.exp (-ε) * (A.card * Real.exp ε) :=
        mul_le_mul_of_nonneg_left h6 (Real.exp_pos _).le
    _ = A.card := by
        rw [mul_comm, mul_assoc, ← Real.exp_add, add_neg_cancel, Real.exp_zero, mul_one]

/-- **The landscape of `thermal_binary_exponential` is sharp, and its hypothesis is satisfiable.**
For `n` two-state sites with excitation energy `2`, envelope constants `1` and zero residual:

* the single evaluation of the ground state is an exact zero-temperature certificate
  (`product_single_certificate`: the excitation energy `2` is at least the envelope constant `1`);
* all `2 ^ n` configurations together satisfy the hypothesis of `thermal_binary_exponential` with
  `ε = 0` (`full_evaluation_partition_eq`).

So the exponential lower bound of `thermal_binary_exponential` is not vacuous, and it is a
finite-temperature effect: at zero temperature one evaluation suffices for every `n`. -/
theorem thermal_binary_sharp (n : ℕ) :
    IsCertificate (hamEnv fun _ : Fin n => (1 : ℝ))
        (fun x : Fin n → Bool => ∑ i, if x i then (2 : ℝ) else 0) (fun _ => 0) {fun _ => false}
        (singleton_nonempty _) 0 ∧
      ∑ y : Fin n → Bool, Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) +
          lowerEnv (hamEnv fun _ : Fin n => (1 : ℝ)) univ univ_nonempty (fun _ => 0) y)) ≤
        Real.exp 0 * ∑ y : Fin n → Bool,
          Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) + 0)) := by
  refine ⟨product_single_certificate (fun _ : Fin n => (1 : ℝ))
    (fun _ (s : Bool) => if s then (2 : ℝ) else 0) (fun _ => false) fun _ s hs => ?_, ?_⟩
  · cases s
    · exact absurd rfl hs
    · norm_num
  · have hd : IsEnvelope (hamEnv (σ := fun _ : Fin n => Bool) fun _ => (1 : ℝ)) :=
      hamEnv_isEnvelope fun _ => zero_le_one
    have hg : Admissible (hamEnv (σ := fun _ : Fin n => Bool) fun _ => (1 : ℝ)) fun _ => 0 := by
      intro a b
      have h0 : 0 ≤ hamEnv (fun _ : Fin n => (1 : ℝ)) a b :=
        Finset.sum_nonneg fun i _ => by split_ifs <;> norm_num
      linarith
    rw [Real.exp_zero, one_mul]
    exact (full_evaluation_partition_eq hd hg _ _).le

/-- **The bound of `thermal_binary_exponential` is attained.**  On the same landscape the
optimistic partition function of the single evaluation of the ground state is `(3/2) ^ n` and the
true partition function is `(5/4) ^ n`.  Hence `A = {ground state}` satisfies the hypothesis of
`thermal_binary_exponential` with `ε = n * log (6/5)`, with equality, and for this `ε` the lower
bound `exp (-ε) * (6/5) ^ n` equals `1 = |A|`.

So the threshold of `thermal_binary_exponential` is sharp.  For an extensive accuracy
`ε = n * ε₁` that theorem gives at least `exp (n * (log (6/5) - ε₁))` evaluations, exponentially
many when `ε₁ < log (6/5)`; when `ε₁ ≥ log (6/5)` the single evaluation of the ground state
satisfies its hypothesis.

That hypothesis — the optimistic partition function is within `exp ε` of the *true* one — is
not computable from the evaluations.  As a two-sided certificate (optimistic against
pessimistic envelope, `(3/2) ^ n` against `(9/8) ^ n`) the single evaluation of the ground state
has width `n * log (4/3)`. -/
theorem thermal_binary_single_tight (n : ℕ) :
    ∑ y : Fin n → Bool, Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) +
        lowerEnv (hamEnv fun _ : Fin n => (1 : ℝ)) {fun _ => false} (singleton_nonempty _)
          (fun _ => 0) y)) =
      Real.exp (n * Real.log (6 / 5)) * ∑ y : Fin n → Bool,
        Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) + 0)) ∧
    Real.exp (-(n * Real.log (6 / 5))) * (6 / 5 : ℝ) ^ n =
      (({fun _ => false} : Finset (Fin n → Bool)).card : ℝ) := by
  have h2 : Real.exp (-Real.log 2) = 1 / 2 := by
    rw [Real.exp_neg, Real.exp_log (by norm_num)]
    norm_num
  have h4 : Real.exp (-Real.log 2 * 2) = 1 / 4 := by
    rw [show -Real.log 2 * 2 = -Real.log 2 + -Real.log 2 by ring, Real.exp_add, h2]
    norm_num
  have h65 : Real.exp (n * Real.log (6 / 5)) = (6 / 5 : ℝ) ^ n := by
    rw [Real.exp_nat_mul, Real.exp_log (by norm_num)]
  constructor
  · -- the Boltzmann weights of `f` plus the lower envelope: each excitation costs `2 - 1`
    have hL : ∀ y : Fin n → Bool, Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) +
        lowerEnv (hamEnv fun _ : Fin n => (1 : ℝ)) {fun _ => false} (singleton_nonempty _)
          (fun _ => 0) y)) = ∏ i, Real.exp (-Real.log 2 * if y i then 1 else 0) := by
      intro y
      rw [← Real.exp_sum, ← Finset.mul_sum]
      congr 2
      unfold lowerEnv hamEnv
      rw [Finset.sup'_singleton, zero_sub, ← Finset.sum_neg_distrib, ← Finset.sum_add_distrib]
      refine Finset.sum_congr rfl fun i _ => ?_
      cases y i <;> norm_num
    -- the Boltzmann weights of `f`
    have hR : ∀ y : Fin n → Bool,
        Real.exp (-Real.log 2 * ((∑ i, if y i then (2 : ℝ) else 0) + 0)) =
          ∏ i, Real.exp (-Real.log 2 * if y i then 2 else 0) := by
      intro y
      rw [add_zero, Finset.mul_sum, Real.exp_sum]
    -- both partition functions are products of site sums: `(3/2) ^ n` and `(5/4) ^ n`
    rw [Finset.sum_congr rfl fun y _ => hL y, Finset.sum_congr rfl fun y _ => hR y,
      ← Fintype.prod_sum fun (_ : Fin n) (s : Bool) => Real.exp (-Real.log 2 * if s then 1 else 0),
      ← Fintype.prod_sum fun (_ : Fin n) (s : Bool) => Real.exp (-Real.log 2 * if s then 2 else 0),
      h65]
    simp only [Fintype.sum_bool, Bool.false_eq_true, if_false, if_true, mul_zero, mul_one,
      Real.exp_zero, h2, h4, Finset.prod_const, Finset.card_univ, Fintype.card_fin]
    rw [← mul_pow]
    norm_num
  · rw [Real.exp_neg, h65, inv_mul_cancel₀ (pow_ne_zero n (by norm_num)), Finset.card_singleton,
      Nat.cast_one]

end MetricChain
