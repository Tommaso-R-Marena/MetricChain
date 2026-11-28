import Mathlib

/-!
# Allocation theory of multistate estimation on finite supports

Division 9 (certified MBAR), `docs/mbar/MATHEMATICS.md` part A.  Finite support, real arithmetic.

`Model ι α`: states `ι`, points `α`, `p k x` the probability of point `x` under state `k`.
For sample amounts `s k > 0` and a contrast `c`:

* `J s r = Σ_k E_k[r_k²]/s_k` on the allocation-independent affine set `Feasible c r`
  (`E_k r_k = 0`, `Σ_k p_k r_k = −Σ_k c_k p_k`) — the primal problem (Theorem A1);
* `D c s h = 2 Σ_k c_k E_k h − Σ_k s_k Var_k h` — the dual problem (Theorem A2).

Machine-checked here: weak duality; from any solution `v` of the Laplacian equation
`s_k (v_k − E_k z) = c_k`, `z = Σ_k π_k v_k`, the explicit minimiser `rstar`, its feasibility,
the Pythagoras identity, optimality, strong duality and the value `Σ c_k v_k − Σ c_k²/s_k`;
joint convexity of `J` (perspective inequality) and convexity of the value in the allocation;
the Cauchy–Schwarz form, superadditivity of the precision, the efficiency bound behind the
equivalence theorem; monotonicity, homogeneity, rounding; cost-aware (Neyman) allocation.

Not formalised: existence of `v` (solvability of the Laplacian equation under connected overlap),
measure-theoretic generality, the minimax theorem.
-/

open Finset

namespace MBAR

/-- A finite multistate model: `p k x` is the probability of point `x` under state `k`. -/
structure Model (ι α : Type*) [Fintype ι] [Fintype α] where
  /-- probability of point `x` under state `k` -/
  p : ι → α → ℝ
  nonneg : ∀ k x, 0 ≤ p k x
  sum_one : ∀ k, ∑ x, p k x = 1

namespace Model

variable {ι α : Type*} [Fintype ι] [Fintype α] (M : Model ι α)

/-- Expectation under state `k`. -/
def E (k : ι) (h : α → ℝ) : ℝ := ∑ x, M.p k x * h x

/-- Variance under state `k`. -/
def Var (k : ι) (h : α → ℝ) : ℝ := M.E k (fun x => (h x - M.E k h) ^ 2)

/-- Primal objective `Σ_k E_k[r_k²]/s_k`. -/
noncomputable def J (s : ι → ℝ) (r : ι → α → ℝ) : ℝ := ∑ k, M.E k (fun x => r k x ^ 2) / s k

/-- The allocation-independent affine set `F_c`. -/
def Feasible (c : ι → ℝ) (r : ι → α → ℝ) : Prop :=
  (∀ k, M.E k (r k) = 0) ∧ ∀ x, ∑ k, M.p k x * r k x = -∑ k, c k * M.p k x

/-- The linear functional `ℓ_c(h) = Σ_k c_k E_k h`. -/
def ell (c : ι → ℝ) (h : α → ℝ) : ℝ := ∑ k, c k * M.E k h

/-- `Q(s, h) = Σ_k s_k Var_k h`, linear in the allocation. -/
def Q (s : ι → ℝ) (h : α → ℝ) : ℝ := ∑ k, s k * M.Var k h

/-- Dual objective. -/
def D (c s : ι → ℝ) (h : α → ℝ) : ℝ := 2 * M.ell c h - M.Q s h

/-- Mixture `m_s(x) = Σ_k s_k p_k(x)`. -/
def mix (s : ι → ℝ) (x : α) : ℝ := ∑ k, s k * M.p k x

/-- `z = Σ_k π_k v_k`, `π_k = s_k p_k / m_s`. -/
noncomputable def zfun (s v : ι → ℝ) (x : α) : ℝ := (∑ k, s k * M.p k x * v k) / M.mix s x

/-- The explicit minimiser `r*_k = s_k (E_k z − z)`. -/
noncomputable def rstar (s v : ι → ℝ) (k : ι) (x : α) : ℝ :=
  s k * (M.E k (M.zfun s v) - M.zfun s v x)

/-- Value of the primal problem. -/
noncomputable def V (c s : ι → ℝ) : ℝ := sInf (M.J s '' {r | M.Feasible c r})

/-! ### Linearity and positivity of expectations -/

lemma E_const (k : ι) (a : ℝ) : M.E k (fun _ => a) = a := by
  simp only [E]
  rw [← Finset.sum_mul, M.sum_one k, one_mul]

lemma E_add (k : ι) (f g : α → ℝ) : M.E k (fun x => f x + g x) = M.E k f + M.E k g := by
  simp only [E, mul_add, Finset.sum_add_distrib]

lemma E_sub (k : ι) (f g : α → ℝ) : M.E k (fun x => f x - g x) = M.E k f - M.E k g := by
  simp only [E, mul_sub, Finset.sum_sub_distrib]

lemma E_const_mul (k : ι) (a : ℝ) (f : α → ℝ) : M.E k (fun x => a * f x) = a * M.E k f := by
  simp only [E, Finset.mul_sum]
  exact Finset.sum_congr rfl (fun x _ => by ring)

lemma E_div_const (k : ι) (f : α → ℝ) (a : ℝ) : M.E k (fun x => f x / a) = M.E k f / a := by
  simp only [E, Finset.sum_div]
  exact Finset.sum_congr rfl (fun x _ => by ring)

lemma E_mono (k : ι) {f g : α → ℝ} (hfg : ∀ x, f x ≤ g x) : M.E k f ≤ M.E k g :=
  Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hfg x) (M.nonneg k x))

lemma E_nonneg (k : ι) {f : α → ℝ} (hf : ∀ x, 0 ≤ f x) : 0 ≤ M.E k f :=
  Finset.sum_nonneg (fun x _ => mul_nonneg (M.nonneg k x) (hf x))

lemma E_sq_sub (k : ι) (h : α → ℝ) (a : ℝ) :
    M.E k (fun x => (h x - a) ^ 2) = M.E k (fun x => h x ^ 2) - 2 * a * M.E k h + a ^ 2 := by
  have h1 := M.sum_one k
  have h2 : a ^ 2 = ∑ x, M.p k x * a ^ 2 := by rw [← Finset.sum_mul, h1, one_mul]
  rw [h2]
  simp only [E, Finset.mul_sum]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl (fun x _ => by ring)

lemma Var_eq (k : ι) (h : α → ℝ) : M.Var k h = M.E k (fun x => h x ^ 2) - (M.E k h) ^ 2 := by
  rw [Var, M.E_sq_sub]; ring

lemma Var_nonneg (k : ι) (h : α → ℝ) : 0 ≤ M.Var k h :=
  M.E_nonneg k (fun _ => sq_nonneg _)

lemma Var_smul (k : ι) (t : ℝ) (h : α → ℝ) : M.Var k (fun x => t * h x) = t ^ 2 * M.Var k h := by
  rw [M.Var_eq, M.Var_eq, M.E_const_mul]
  have : (fun x => (t * h x) ^ 2) = fun x => t ^ 2 * h x ^ 2 := by funext x; ring
  rw [this, M.E_const_mul]; ring

lemma ell_smul (c : ι → ℝ) (t : ℝ) (h : α → ℝ) : M.ell c (fun x => t * h x) = t * M.ell c h := by
  simp only [ell, M.E_const_mul, Finset.mul_sum]
  exact Finset.sum_congr rfl (fun k _ => by ring)

lemma Q_smul (s : ι → ℝ) (t : ℝ) (h : α → ℝ) : M.Q s (fun x => t * h x) = t ^ 2 * M.Q s h := by
  simp only [Q, M.Var_smul, Finset.mul_sum]
  exact Finset.sum_congr rfl (fun k _ => by ring)

lemma Q_nonneg {s : ι → ℝ} (hs : ∀ k, 0 < s k) (h : α → ℝ) : 0 ≤ M.Q s h :=
  Finset.sum_nonneg (fun k _ => mul_nonneg (hs k).le (M.Var_nonneg k h))

lemma Q_add (s t : ι → ℝ) (h : α → ℝ) : M.Q (fun k => s k + t k) h = M.Q s h + M.Q t h := by
  simp only [Q, add_mul, Finset.sum_add_distrib]

lemma J_nonneg {s : ι → ℝ} (hs : ∀ k, 0 < s k) (r : ι → α → ℝ) : 0 ≤ M.J s r :=
  Finset.sum_nonneg (fun k _ => div_nonneg (M.E_nonneg k (fun _ => sq_nonneg _)) (hs k).le)

/-! ### Weak duality (Theorem A2, easy half) -/

/-- On the feasible set, `ℓ_c(h) = −Σ_k E_k[h r_k]`. -/
theorem ell_eq_neg {c : ι → ℝ} {r : ι → α → ℝ} (hr : M.Feasible c r) (h : α → ℝ) :
    M.ell c h = -∑ k, M.E k (fun x => h x * r k x) := by
  have h1 : M.ell c h = ∑ x, h x * ∑ k, c k * M.p k x := by
    simp only [ell, E, Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl (fun x _ => Finset.sum_congr rfl (fun k _ => by ring))
  have h2 : ∑ k, M.E k (fun x => h x * r k x) = ∑ x, h x * ∑ k, M.p k x * r k x := by
    simp only [E, Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl (fun x _ => Finset.sum_congr rfl (fun k _ => by ring))
  rw [h1, h2, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun x _ => ?_)
  rw [hr.2 x]; ring

/-- The same with `h` centred in each state. -/
theorem ell_eq_neg_centered {c : ι → ℝ} {r : ι → α → ℝ} (hr : M.Feasible c r) (h : α → ℝ) :
    M.ell c h = -∑ k, M.E k (fun x => (h x - M.E k h) * r k x) := by
  rw [M.ell_eq_neg hr h]
  congr 1
  refine Finset.sum_congr rfl (fun k _ => ?_)
  have : (fun x => (h x - M.E k h) * r k x) = fun x => h x * r k x - M.E k h * r k x := by
    funext x; ring
  rw [this, M.E_sub, M.E_const_mul, hr.1 k]; ring

/-- **Weak duality**: every dual value is below every primal value. -/
theorem weak_duality {c s : ι → ℝ} {r : ι → α → ℝ} (hs : ∀ k, 0 < s k) (hr : M.Feasible c r)
    (h : α → ℝ) : M.D c s h ≤ M.J s r := by
  have key : ∀ k, -2 * M.E k (fun x => (h x - M.E k h) * r k x) - s k * M.Var k h
      ≤ M.E k (fun x => r k x ^ 2) / s k := by
    intro k
    have hsk := hs k
    have h1 : -2 * M.E k (fun x => (h x - M.E k h) * r k x) - s k * M.Var k h
        = M.E k (fun x => -2 * ((h x - M.E k h) * r k x) - s k * (h x - M.E k h) ^ 2) := by
      rw [M.E_sub, M.E_const_mul, M.E_const_mul, Var]
    rw [h1, ← M.E_div_const]
    refine M.E_mono k (fun x => ?_)
    have h3 : 0 ≤ (s k * (h x - M.E k h) + r k x) ^ 2 / s k := by positivity
    have h4 : (s k * (h x - M.E k h) + r k x) ^ 2 / s k
        = s k * (h x - M.E k h) ^ 2 + 2 * ((h x - M.E k h) * r k x) + r k x ^ 2 / s k := by
      field_simp; ring
    linarith
  have hell := M.ell_eq_neg_centered hr h
  calc M.D c s h
      = ∑ k, (-2 * M.E k (fun x => (h x - M.E k h) * r k x) - s k * M.Var k h) := by
        simp only [D, Q, hell]
        rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
        ring
    _ ≤ ∑ k, M.E k (fun x => r k x ^ 2) / s k := Finset.sum_le_sum (fun k _ => key k)

/-! ### The explicit minimiser (Theorem A1) -/

section minimiser

variable {c s v : ι → ℝ}

lemma Ez_eq (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) (k : ι) :
    M.E k (M.zfun s v) = v k - c k / s k := by
  have h1 := hv k
  have hk := (hs k).ne'
  field_simp
  linarith

/-- `r*` lies in the affine set `F_c`. -/
theorem rstar_feasible (hs : ∀ k, 0 < s k)
    (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) : M.Feasible c (M.rstar s v) := by
  refine ⟨fun k => ?_, fun x => ?_⟩
  · have : M.rstar s v k = fun x => s k * (M.E k (M.zfun s v) - M.zfun s v x) := rfl
    rw [this, M.E_const_mul, M.E_sub, M.E_const]; ring
  · have hμ := M.Ez_eq hs hv
    simp only [rstar, hμ]
    by_cases hm : M.mix s x = 0
    · have hp : ∀ k, M.p k x = 0 := by
        intro k
        have h0 : ∀ j ∈ Finset.univ, 0 ≤ s j * M.p j x :=
          fun j _ => mul_nonneg (hs j).le (M.nonneg j x)
        have h1 := (Finset.sum_eq_zero_iff_of_nonneg h0).1 hm k (Finset.mem_univ k)
        exact (mul_eq_zero.1 h1).resolve_left (hs k).ne'
      simp [hp]
    · have hz : M.zfun s v x * M.mix s x = ∑ k, s k * M.p k x * v k := by
        simp only [zfun]; exact div_mul_cancel₀ _ hm
      have h1 : ∑ k, M.p k x * (s k * (v k - c k / s k - M.zfun s v x))
          = (∑ k, s k * M.p k x * v k) - (∑ k, c k * M.p k x) - M.zfun s v x * M.mix s x := by
        simp only [mix, Finset.mul_sum]
        rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
        refine Finset.sum_congr rfl (fun k _ => ?_)
        have hk := (hs k).ne'
        field_simp
      rw [h1, hz]; ring

/-- The value at `r*` is `Σ_k s_k Var_k(z)`. -/
theorem J_rstar (hs : ∀ k, 0 < s k) : M.J s (M.rstar s v) = M.Q s (M.zfun s v) := by
  simp only [J, Q, Var]
  refine Finset.sum_congr rfl (fun k _ => ?_)
  have hk := (hs k).ne'
  have h1 : (fun x => M.rstar s v k x ^ 2)
      = fun x => s k ^ 2 * (M.zfun s v x - M.E k (M.zfun s v)) ^ 2 := by
    funext x; simp only [rstar]; ring
  rw [h1, M.E_const_mul]
  field_simp

/-- Strong duality at `z`: `ℓ_c(z) = Σ_k s_k Var_k(z)`. -/
theorem ell_zfun (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) :
    M.ell c (M.zfun s v) = M.Q s (M.zfun s v) := by
  rw [M.ell_eq_neg (M.rstar_feasible hs hv), Q, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun k _ => ?_)
  have h1 : (fun x => M.zfun s v x * M.rstar s v k x)
      = fun x => s k * (M.E k (M.zfun s v) * M.zfun s v x - M.zfun s v x ^ 2) := by
    funext x; simp only [rstar]; ring
  rw [h1, M.E_const_mul, M.E_sub, M.E_const_mul, M.Var_eq]
  ring

/-- **Strong duality**: the dual value at `z` equals the primal value at `r*`. -/
theorem strong_duality (hs : ∀ k, 0 < s k)
    (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) :
    M.D c s (M.zfun s v) = M.J s (M.rstar s v) := by
  rw [D, M.ell_zfun hs hv, M.J_rstar hs]; ring

/-- The closed form of the handoff: `Σ_k c_k v_k − Σ_k c_k²/s_k`. -/
theorem J_rstar_formula (hs : ∀ k, 0 < s k)
    (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) :
    M.J s (M.rstar s v) = ∑ k, c k * v k - ∑ k, c k ^ 2 / s k := by
  rw [M.J_rstar hs, ← M.ell_zfun hs hv, ell, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl (fun k _ => ?_)
  rw [M.Ez_eq hs hv k]
  have hk := (hs k).ne'
  field_simp

lemma cross_zero (hs : ∀ k, 0 < s k) {d : ι → α → ℝ} (hd1 : ∀ k, M.E k (d k) = 0)
    (hd2 : ∀ x, ∑ k, M.p k x * d k x = 0) :
    ∑ k, M.E k (fun x => M.rstar s v k x * d k x) / s k = 0 := by
  have h1 : ∀ k, M.E k (fun x => M.rstar s v k x * d k x) / s k
      = -M.E k (fun x => M.zfun s v x * d k x) := by
    intro k
    have hk := (hs k).ne'
    have h2 : (fun x => M.rstar s v k x * d k x)
        = fun x => s k * (M.E k (M.zfun s v) * d k x - M.zfun s v x * d k x) := by
      funext x; simp only [rstar]; ring
    rw [h2, M.E_const_mul, M.E_sub, M.E_const_mul, hd1 k]
    field_simp
    ring
  simp only [h1, Finset.sum_neg_distrib, neg_eq_zero]
  simp only [E]
  rw [Finset.sum_comm]
  refine Finset.sum_eq_zero (fun x _ => ?_)
  calc ∑ k, M.p k x * (M.zfun s v x * d k x)
      = M.zfun s v x * ∑ k, M.p k x * d k x := by
        rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun k _ => by ring)
    _ = 0 := by rw [hd2 x, mul_zero]

/-- **Pythagoras**: orthogonality of `r*` to the directions of the affine set. -/
theorem pythagoras (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k)
    {r : ι → α → ℝ} (hr : M.Feasible c r) :
    M.J s r = M.J s (M.rstar s v) + M.J s (fun k x => r k x - M.rstar s v k x) := by
  have hstar := M.rstar_feasible hs hv
  have hd1 : ∀ k, M.E k (fun x => r k x - M.rstar s v k x) = 0 := by
    intro k
    have e := M.E_sub k (r k) (M.rstar s v k)
    rw [e, hr.1 k, hstar.1 k, sub_zero]
  have hd2 : ∀ x, ∑ k, M.p k x * (r k x - M.rstar s v k x) = 0 := by
    intro x
    simp only [mul_sub, Finset.sum_sub_distrib, hr.2 x, hstar.2 x, sub_self]
  have hcross : ∑ k, M.E k (fun x => M.rstar s v k x * (r k x - M.rstar s v k x)) / s k = 0 :=
    M.cross_zero (v := v) hs (d := fun k x => r k x - M.rstar s v k x) hd1 hd2
  have hk : ∀ k, M.E k (fun x => r k x ^ 2) / s k
      = M.E k (fun x => M.rstar s v k x ^ 2) / s k
        + M.E k (fun x => (r k x - M.rstar s v k x) ^ 2) / s k
        + 2 * (M.E k (fun x => M.rstar s v k x * (r k x - M.rstar s v k x)) / s k) := by
    intro k
    have h2 : (fun x => r k x ^ 2) = fun x => M.rstar s v k x ^ 2
        + ((r k x - M.rstar s v k x) ^ 2
          + 2 * (M.rstar s v k x * (r k x - M.rstar s v k x))) := by
      funext x; ring
    rw [h2, M.E_add, M.E_add, M.E_const_mul]
    ring
  simp only [J]
  rw [Finset.sum_congr rfl (fun k _ => hk k), Finset.sum_add_distrib, Finset.sum_add_distrib,
    ← Finset.mul_sum, hcross]
  ring

/-- **Optimality of the explicit minimiser.** -/
theorem rstar_optimal (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k)
    {r : ι → α → ℝ} (hr : M.Feasible c r) : M.J s (M.rstar s v) ≤ M.J s r := by
  rw [M.pythagoras hs hv hr]
  have := M.J_nonneg hs (fun k x => r k x - M.rstar s v k x)
  linarith

/-- `z` maximises the dual objective. -/
theorem zfun_maximises (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k)
    (h : α → ℝ) : M.D c s h ≤ M.D c s (M.zfun s v) := by
  rw [M.strong_duality hs hv]
  exact M.weak_duality hs (M.rstar_feasible hs hv) h

lemma V_le {c s : ι → ℝ} (hs : ∀ k, 0 < s k) {r : ι → α → ℝ} (hr : M.Feasible c r) :
    M.V c s ≤ M.J s r :=
  csInf_le ⟨0, by rintro _ ⟨r', _, rfl⟩; exact M.J_nonneg hs r'⟩ ⟨r, hr, rfl⟩

/-- **Theorem A1, finite support**: the minimum over the allocation-independent affine set is
attained at `r*` and equals `Σ_k c_k v_k − Σ_k c_k²/s_k`. -/
theorem V_eq_J_rstar (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) :
    M.V c s = M.J s (M.rstar s v) := by
  refine le_antisymm (M.V_le hs (M.rstar_feasible hs hv)) ?_
  refine le_csInf ⟨_, M.rstar s v, M.rstar_feasible hs hv, rfl⟩ ?_
  rintro _ ⟨r, hr, rfl⟩
  exact M.rstar_optimal hs hv hr

theorem V_eq_formula (hs : ∀ k, 0 < s k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k) :
    M.V c s = ∑ k, c k * v k - ∑ k, c k ^ 2 / s k := by
  rw [M.V_eq_J_rstar hs hv, M.J_rstar_formula hs hv]

end minimiser

/-! ### Convexity in the allocation (perspective argument) -/

lemma combo_pos {s t lam : ℝ} (hs : 0 < s) (ht : 0 < t) (h0 : 0 ≤ lam) (h1 : lam ≤ 1) :
    0 < lam * s + (1 - lam) * t := by
  rcases eq_or_lt_of_le h0 with h | h
  · subst h; simpa using ht
  · have h2 : 0 ≤ (1 - lam) * t := mul_nonneg (by linarith) ht.le
    have h3 : 0 < lam * s := mul_pos h hs
    linarith

/-- The perspective inequality for `(a, s) ↦ a²/s`. -/
lemma perspective_ineq {a b s t lam : ℝ} (hs : 0 < s) (ht : 0 < t) (h0 : 0 ≤ lam)
    (h1 : lam ≤ 1) :
    (lam * a + (1 - lam) * b) ^ 2 / (lam * s + (1 - lam) * t)
      ≤ lam * (a ^ 2 / s) + (1 - lam) * (b ^ 2 / t) := by
  have hden := combo_pos hs ht h0 h1
  have hst : 0 < s * t := mul_pos hs ht
  have e1 : lam * (a ^ 2 / s) + (1 - lam) * (b ^ 2 / t)
      = (lam * a ^ 2 * t + (1 - lam) * b ^ 2 * s) / (s * t) := by
    field_simp
  rw [e1, div_le_div_iff₀ hden hst]
  nlinarith [mul_nonneg (mul_nonneg h0 (sub_nonneg.2 h1)) (sq_nonneg (a * t - b * s))]

/-- Joint convexity of the primal objective in (allocation, `r`). -/
theorem J_convex {s t : ι → ℝ} (hs : ∀ k, 0 < s k) (ht : ∀ k, 0 < t k) {lam : ℝ}
    (h0 : 0 ≤ lam) (h1 : lam ≤ 1) (r r' : ι → α → ℝ) :
    M.J (fun k => lam * s k + (1 - lam) * t k) (fun k x => lam * r k x + (1 - lam) * r' k x)
      ≤ lam * M.J s r + (1 - lam) * M.J t r' := by
  simp only [J, Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_le_sum (fun k _ => ?_)
  have e2 : lam * (M.E k (fun x => r k x ^ 2) / s k)
      + (1 - lam) * (M.E k (fun x => r' k x ^ 2) / t k)
      = M.E k (fun x => lam * (r k x ^ 2 / s k) + (1 - lam) * (r' k x ^ 2 / t k)) := by
    rw [M.E_add, M.E_const_mul, M.E_const_mul, M.E_div_const, M.E_div_const]
  rw [← M.E_div_const, e2]
  exact M.E_mono k (fun x => perspective_ineq (hs k) (ht k) h0 h1)

/-- The affine set is convex. -/
lemma Feasible.combo {c : ι → ℝ} {r r' : ι → α → ℝ} (hr : M.Feasible c r)
    (hr' : M.Feasible c r') (lam : ℝ) :
    M.Feasible c (fun k x => lam * r k x + (1 - lam) * r' k x) := by
  refine ⟨fun k => ?_, fun x => ?_⟩
  · have e := M.E_add k (fun x => lam * r k x) (fun x => (1 - lam) * r' k x)
    rw [e, M.E_const_mul, M.E_const_mul, hr.1 k, hr'.1 k]; ring
  · have h1 := hr.2 x
    have h2 := hr'.2 x
    have e : ∑ k, M.p k x * (lam * r k x + (1 - lam) * r' k x)
        = lam * ∑ k, M.p k x * r k x + (1 - lam) * ∑ k, M.p k x * r' k x := by
      rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl (fun k _ => by ring)
    rw [e, h1, h2]; ring

/-- **Convexity of the value in the allocation**, whenever the minima at the two endpoints are
attained (which `V_eq_J_rstar` provides from solutions of the Laplacian equation). -/
theorem V_convex {c s t : ι → ℝ} (hs : ∀ k, 0 < s k) (ht : ∀ k, 0 < t k) {lam : ℝ}
    (h0 : 0 ≤ lam) (h1 : lam ≤ 1) {r r' : ι → α → ℝ} (hr : M.Feasible c r)
    (hr' : M.Feasible c r') (hmin : M.J s r = M.V c s) (hmin' : M.J t r' = M.V c t) :
    M.V c (fun k => lam * s k + (1 - lam) * t k) ≤ lam * M.V c s + (1 - lam) * M.V c t := by
  have hpos : ∀ k, 0 < lam * s k + (1 - lam) * t k := fun k => combo_pos (hs k) (ht k) h0 h1
  calc M.V c (fun k => lam * s k + (1 - lam) * t k)
      ≤ M.J (fun k => lam * s k + (1 - lam) * t k)
          (fun k x => lam * r k x + (1 - lam) * r' k x) := M.V_le hpos (hr.combo M hr' lam)
    _ ≤ lam * M.J s r + (1 - lam) * M.J t r' := M.J_convex hs ht h0 h1 r r'
    _ = lam * M.V c s + (1 - lam) * M.V c t := by rw [hmin, hmin']

/-- Convexity stated with the explicit minimisers. -/
theorem V_convex_of_solutions {c s t vs vt : ι → ℝ} (hs : ∀ k, 0 < s k) (ht : ∀ k, 0 < t k)
    {lam : ℝ} (h0 : 0 ≤ lam) (h1 : lam ≤ 1)
    (hvs : ∀ k, s k * (vs k - M.E k (M.zfun s vs)) = c k)
    (hvt : ∀ k, t k * (vt k - M.E k (M.zfun t vt)) = c k) :
    M.V c (fun k => lam * s k + (1 - lam) * t k) ≤ lam * M.V c s + (1 - lam) * M.V c t :=
  M.V_convex hs ht h0 h1 (M.rstar_feasible hs hvs) (M.rstar_feasible ht hvt)
    (M.V_eq_J_rstar hs hvs).symm (M.V_eq_J_rstar ht hvt).symm

/-! ### Cauchy–Schwarz form, superadditive precision, efficiency bound -/

/-- `ℓ_c(h)² ≤ Q(s,h) · J(s,r)` for every `h` and every feasible `r`: the variance bound of every
regular estimator against every one-dimensional submodel. -/
theorem cs_form {c s : ι → ℝ} {r : ι → α → ℝ} (hs : ∀ k, 0 < s k) (hr : M.Feasible c r)
    (h : α → ℝ) : M.ell c h ^ 2 ≤ M.Q s h * M.J s r := by
  have hQ := M.Q_nonneg hs h
  have hJ := M.J_nonneg hs r
  have key : ∀ t : ℝ, 2 * (t * M.ell c h) - t ^ 2 * M.Q s h ≤ M.J s r := by
    intro t
    have h1 := M.weak_duality hs hr (fun x => t * h x)
    rwa [D, M.ell_smul, M.Q_smul] at h1
  rcases eq_or_lt_of_le hQ with h0 | hpos
  · rw [← h0, zero_mul]
    by_contra hne
    have hl : M.ell c h ≠ 0 := by
      intro h2; apply hne; rw [h2]; norm_num
    have h1 := key ((M.J s r + 1) / M.ell c h)
    rw [← h0, mul_zero, sub_zero, div_mul_cancel₀ _ hl] at h1
    linarith
  · have h1 := key (M.ell c h / M.Q s h)
    have e : 2 * (M.ell c h / M.Q s h * M.ell c h) - (M.ell c h / M.Q s h) ^ 2 * M.Q s h
        = M.ell c h ^ 2 / M.Q s h := by
      field_simp; ring
    rw [e, div_le_iff₀ hpos] at h1
    linarith [mul_comm (M.J s r) (M.Q s h)]

/-- **Superadditivity of the precision** (multiplicative form of `1/V(s+t) ≥ 1/V(s) + 1/V(t)`):
for feasible `r`, `r'` (in particular the minimisers at `s` and `t`) and the minimiser at `s + t`,
`V(s+t) · (J(s,r) + J(t,r')) ≤ J(s,r) · J(t,r')`. -/
theorem precision_superadditive {c s t v : ι → ℝ} (hs : ∀ k, 0 < s k) (ht : ∀ k, 0 < t k)
    (hv : ∀ k, (s k + t k) * (v k - M.E k (M.zfun (fun k => s k + t k) v)) = c k)
    {r r' : ι → α → ℝ} (hr : M.Feasible c r) (hr' : M.Feasible c r') :
    M.J (fun k => s k + t k) (M.rstar (fun k => s k + t k) v) * (M.J s r + M.J t r')
      ≤ M.J s r * M.J t r' := by
  have hu : ∀ k, 0 < s k + t k := fun k => add_pos (hs k) (ht k)
  set z := M.zfun (fun k => s k + t k) v with hz
  set Vu := M.J (fun k => s k + t k) (M.rstar (fun k => s k + t k) v) with hVu
  have hQu : M.Q (fun k => s k + t k) z = Vu := (M.J_rstar hu).symm
  have hell : M.ell c z = Vu := by rw [M.ell_zfun hu hv, hQu]
  have h1 := M.cs_form hs hr z
  have h2 := M.cs_form ht hr' z
  rw [hell] at h1 h2
  have hadd : M.Q s z + M.Q t z = Vu := by rw [← M.Q_add, hQu]
  have hVu0 : 0 ≤ Vu := M.J_nonneg hu _
  have hJs := M.J_nonneg hs r
  have hJt := M.J_nonneg ht r'
  have hQs := M.Q_nonneg hs z
  have hQt := M.Q_nonneg ht z
  rcases eq_or_lt_of_le hVu0 with h0 | hpos
  · rw [← h0, zero_mul]; exact mul_nonneg hJs hJt
  · -- Vu² (Js + Jt) ≤ (Qs + Qt) Js Jt = Vu Js Jt
    have h3 : Vu ^ 2 * (M.J s r + M.J t r') ≤ Vu * (M.J s r * M.J t r') := by
      have a1 : Vu ^ 2 * M.J t r' ≤ M.Q s z * M.J s r * M.J t r' :=
        mul_le_mul_of_nonneg_right h1 hJt
      have a2 : Vu ^ 2 * M.J s r ≤ M.Q t z * M.J t r' * M.J s r :=
        mul_le_mul_of_nonneg_right h2 hJs
      have a3 : M.Q s z * M.J s r * M.J t r' + M.Q t z * M.J t r' * M.J s r
          = Vu * (M.J s r * M.J t r') := by rw [← hadd]; ring
      nlinarith [a1, a2, a3]
    have h4 : Vu * (Vu * (M.J s r + M.J t r')) ≤ Vu * (M.J s r * M.J t r') := by
      have : Vu * (Vu * (M.J s r + M.J t r')) = Vu ^ 2 * (M.J s r + M.J t r') := by ring
      rw [this]; exact h3
    exact le_of_mul_le_mul_left h4 hpos

/-- **Budget of information** (the step of Theorem C2 that holds for every design): along a direction
`h` with `Var_k(h) ≤ G·a_k` in every state, any allocation `t ≥ 0` (zeros allowed) of cost
`Σ a_k t_k = B` accumulates at most `Q(t, h) ≤ B·G`. -/
theorem Q_le_budget {t a : ι → ℝ} {G B : ℝ} (ht : ∀ k, 0 ≤ t k) (h : α → ℝ)
    (hG : ∀ k, M.Var k h ≤ G * a k) (hB : ∑ k, a k * t k = B) : M.Q t h ≤ B * G := by
  have h1 : M.Q t h ≤ ∑ k, t k * (G * a k) :=
    Finset.sum_le_sum (fun k _ => mul_le_mul_of_nonneg_left (hG k) (ht k))
  have e : ∑ k, t k * (G * a k) = B * G := by
    rw [← hB, Finset.sum_mul]; exact Finset.sum_congr rfl (fun k _ => by ring)
  linarith

/-- **Efficiency bound** (the inequality behind the equivalence theorem): if
`Var_k(z_s) ≤ G·a_k` for all `k`, then every allocation `t` of cost `Σ a_k t_k = B` and every
feasible `r` satisfy `V(s)² ≤ B·G·J(t,r)`. -/
theorem efficiency_bound {c s t v a : ι → ℝ} {G B : ℝ} (hs : ∀ k, 0 < s k) (ht : ∀ k, 0 < t k)
    (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k)
    (hG : ∀ k, M.Var k (M.zfun s v) ≤ G * a k) (hB : ∑ k, a k * t k = B)
    {r : ι → α → ℝ} (hr : M.Feasible c r) :
    M.J s (M.rstar s v) ^ 2 ≤ B * G * M.J t r := by
  have h1 := M.cs_form ht hr (M.zfun s v)
  rw [M.ell_zfun hs hv, ← M.J_rstar hs] at h1
  have hQ : M.Q t (M.zfun s v) ≤ B * G := by
    have : M.Q t (M.zfun s v) ≤ ∑ k, t k * (G * a k) :=
      Finset.sum_le_sum (fun k _ => mul_le_mul_of_nonneg_left (hG k) (ht k).le)
    have e : ∑ k, t k * (G * a k) = B * G := by
      rw [← hB, Finset.sum_mul]; exact Finset.sum_congr rfl (fun k _ => by ring)
    linarith
  calc M.J s (M.rstar s v) ^ 2 ≤ M.Q t (M.zfun s v) * M.J t r := h1
    _ ≤ B * G * M.J t r := mul_le_mul_of_nonneg_right hQ (M.J_nonneg ht r)

/-- **Equivalence theorem, sufficiency**: if `Var_k(z_s)/a_k ≤ V(s)/B` for every state, then `s`
is optimal among all allocations of cost `B`. -/
theorem equivalence_sufficient {c s t v a : ι → ℝ} {B : ℝ} (hB0 : 0 < B) (hs : ∀ k, 0 < s k)
    (ht : ∀ k, 0 < t k) (hv : ∀ k, s k * (v k - M.E k (M.zfun s v)) = c k)
    (hG : ∀ k, M.Var k (M.zfun s v) ≤ M.J s (M.rstar s v) / B * a k)
    (hB : ∑ k, a k * t k = B) {r : ι → α → ℝ} (hr : M.Feasible c r) :
    M.J s (M.rstar s v) ≤ M.J t r := by
  have h1 := M.efficiency_bound hs ht hv hG hB hr
  have hV := M.J_nonneg hs (M.rstar s v)
  have e : B * (M.J s (M.rstar s v) / B) = M.J s (M.rstar s v) := by field_simp
  rw [e] at h1
  rcases eq_or_lt_of_le hV with h0 | hpos
  · rw [← h0]; exact M.J_nonneg ht r
  · have h2 : M.J s (M.rstar s v) * M.J s (M.rstar s v)
        ≤ M.J s (M.rstar s v) * M.J t r := by rw [← sq]; exact h1
    exact le_of_mul_le_mul_left h2 hpos

/-! ### Monotonicity, homogeneity, rounding -/

lemma J_smul {s : ι → ℝ} {a : ℝ} (r : ι → α → ℝ) :
    M.J (fun k => a * s k) r = M.J s r / a := by
  simp only [J, Finset.sum_div]
  exact Finset.sum_congr rfl (fun k _ => by rw [div_div, mul_comm])

lemma J_anti {s t : ι → ℝ} (hs : ∀ k, 0 < s k) (hst : ∀ k, s k ≤ t k) (r : ι → α → ℝ) :
    M.J t r ≤ M.J s r :=
  Finset.sum_le_sum (fun k _ =>
    div_le_div_of_nonneg_left (M.E_nonneg k (fun _ => sq_nonneg _)) (hs k) (hst k))

/-- **Rounding**: counts `n` with `n_k ≥ ρ s_k` lose at most the factor `1/ρ`. -/
theorem rounding_bound {s n : ι → ℝ} {ρ : ℝ} (hρ : 0 < ρ) (hs : ∀ k, 0 < s k)
    (hn : ∀ k, ρ * s k ≤ n k) (r : ι → α → ℝ) : M.J n r ≤ M.J s r / ρ := by
  rw [← M.J_smul r]
  exact M.J_anti (fun k => mul_pos hρ (hs k)) hn r

end Model

/-! ### Cost-aware (Neyman) allocation for a fixed `r` -/

section neyman

variable {ι : Type*} [Fintype ι]

/-- For norms `σ_k`, square roots of costs `ra_k` and any allocation `s > 0`:
`(Σ ra_k σ_k)² ≤ (Σ ra_k² s_k)(Σ σ_k²/s_k)`. -/
theorem neyman_lower {ra σ s : ι → ℝ} (hra : ∀ k, 0 < ra k) (hs : ∀ k, 0 < s k) :
    (∑ k, ra k * σ k) ^ 2 ≤ (∑ k, ra k ^ 2 * s k) * ∑ k, σ k ^ 2 / s k := by
  have hg : ∀ k ∈ (Finset.univ : Finset ι), 0 < ra k ^ 2 * s k :=
    fun k _ => mul_pos (pow_pos (hra k) 2) (hs k)
  have h1 := Finset.sq_sum_div_le_sum_sq_div Finset.univ (fun k => ra k * σ k) hg
  rcases isEmpty_or_nonempty ι with hι | hι
  · simp
  have hpos : 0 < ∑ k, ra k ^ 2 * s k := Finset.sum_pos hg Finset.univ_nonempty
  have e : ∑ k, (ra k * σ k) ^ 2 / (ra k ^ 2 * s k) = ∑ k, σ k ^ 2 / s k := by
    refine Finset.sum_congr rfl (fun k _ => ?_)
    have h2 := (hra k).ne'
    have h3 := (hs k).ne'
    field_simp
  rw [e, div_le_iff₀ hpos] at h1
  linarith [mul_comm (∑ k, σ k ^ 2 / s k) (∑ k, ra k ^ 2 * s k)]

/-- The Neyman allocation `s_k = B σ_k/(ra_k T)`, `T = Σ ra_j σ_j`, spends the budget `B` and
attains the lower bound: `Σ σ_k²/s_k = T²/B`. -/
theorem neyman_attained {ra σ : ι → ℝ} {B : ℝ} (hB : 0 < B) (hra : ∀ k, 0 < ra k)
    (hσ : ∀ k, 0 < σ k) (hT : 0 < ∑ j, ra j * σ j) :
    (∑ k, ra k ^ 2 * (B * σ k / (ra k * ∑ j, ra j * σ j)) = B) ∧
    (∑ k, σ k ^ 2 / (B * σ k / (ra k * ∑ j, ra j * σ j)) = (∑ j, ra j * σ j) ^ 2 / B) := by
  set T := ∑ j, ra j * σ j with hTdef
  constructor
  · have e : ∀ k, ra k ^ 2 * (B * σ k / (ra k * T)) = B / T * (ra k * σ k) := by
      intro k
      have h2 := (hra k).ne'
      field_simp
    simp only [e]
    rw [← Finset.mul_sum, ← hTdef]
    field_simp
  · have e : ∀ k, σ k ^ 2 / (B * σ k / (ra k * T)) = T / B * (ra k * σ k) := by
      intro k
      have h2 := (hra k).ne'
      have h3 := (hσ k).ne'
      field_simp
    simp only [e]
    rw [← Finset.mul_sum, ← hTdef]
    field_simp

end neyman

end MBAR
