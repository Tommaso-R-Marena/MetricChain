import Mathlib
import proofs.Core.Basic
import proofs.Frontiers.EnvelopeDuality
import proofs.Frontiers.CertificationGeometry
import proofs.Frontiers.ConditionalEnvelope

/-!
# Three notions of certificate, and why they agree up to one evaluation

Setting of `CertificationGeometry.lean`: known part `f`, residual `g` admissible for an envelope
`d`, a finite nonempty set `A` on which `g` has been evaluated.  Three things can be certified
from the evaluations:

* a **point certificate** (`IsCertificate`): the best *evaluated* energy is within `ε` of the
  certified lower bound `min (f + L)` — an evaluated configuration, its energy and the minimum
  are all known to within `ε`;
* a **value certificate** (`IsValueCertificate`): the interval `[min (f + L), min (f + U)]` of
  possible values of the minimum has width at most `ε`;
* a **configuration certificate** for a candidate `x` (`IsConfigCertificate`): every admissible
  residual that agrees with the evaluations makes `x` an `ε`-minimiser
  (`isConfigCertificate_iff`).  The candidate need not have been evaluated; its criterion is the
  sharp-minimum condition for the *conditional* envelope, `condEnv d A hA g x y ≤ f y - f x + ε`.

They are related as follows.

* `isValueCertificate_of_isCertificate` — point ⟹ value;
* `cover_of_isValueCertificate` — value ⟹ covering (every `y` within slack `gap y + ε` of `A`);
* `isConfigCertificate_of_isCertificate` — point ⟹ configuration (for the best evaluated point);
* `isCertificate_insert_of_isConfigCertificate` — configuration ⟹ point after evaluating the
  candidate: `insert x A` is a point certificate.

Together with `certificate_of_cover` (covering + one minimiser ⟹ point) the minimal sizes satisfy
`N_cov ≤ N_val ≤ N_point ≤ N_cov + 1` and `N_conf ≤ N_point ≤ N_conf + 1`.  In particular the
statement "a certificate must evaluate every point that only itself covers"
(`anchor_necessary'`) holds for point and value certificates, and for configuration certificates
with the exception of points covered by the candidate itself — which cost nothing.
-/

namespace MetricChain

open Finset

variable {X : Type*} [Fintype X] [Nonempty X]

/-- **Value certificate**: the interval of possible minimum values, between the minimum of `f`
plus the lower McShane envelope and the minimum of `f` plus the upper one, has width `≤ ε`. -/
def IsValueCertificate (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (ε : ℝ) : Prop :=
  (univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y) - certLB d f g A hA ≤ ε

/-- **Configuration certificate** for the candidate `x`: `f` grows at least as fast as the
conditional envelope away from `x`, up to `ε`. -/
def IsConfigCertificate (d : X → X → ℝ) (f g : X → ℝ) (A : Finset X) (hA : A.Nonempty)
    (x : X) (ε : ℝ) : Prop :=
  ∀ y, condEnv d A hA g x y ≤ f y - f x + ε

omit [Fintype X] [Nonempty X] in
/-- **Meaning of a configuration certificate.**  `x` is an `ε`-minimiser of `f + g'` for every
admissible residual `g'` that agrees with the evaluations of `g` on `A`, iff the conditional
envelope criterion holds. -/
theorem isConfigCertificate_iff {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) (A : Finset X) (hA : A.Nonempty) (x : X) (ε : ℝ) :
    IsConfigCertificate d f g A hA x ε ↔
      ∀ g', Admissible d g' → (∀ a ∈ A, g' a = g a) → ∀ y, f x + g' x ≤ f y + g' y + ε := by
  constructor
  · intro h g' hg' hA' y
    have h1 := max_regret_le hg' A hA g hA' f x y
    have h2 := h y
    linarith
  · intro h y
    obtain ⟨g', hg', hA', heq⟩ :=
      max_regret_attained hd A hA g (fun a _ b _ => hg a b) f x y
    have h1 := h g' hg' hA' y
    linarith

/-- A point certificate is a value certificate. -/
theorem isValueCertificate_of_isCertificate {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {ε : ℝ}
    (h : IsCertificate d f g A hA ε) : IsValueCertificate d f g A hA ε := by
  unfold IsValueCertificate
  unfold IsCertificate at h
  have hle : (univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y) ≤ certUB f g A hA := by
    unfold certUB
    apply Finset.le_inf'
    intro a ha
    have h1 : (univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y) ≤
        f a + upperEnv d A hA g a :=
      Finset.inf'_le (fun y => f y + upperEnv d A hA g y) (mem_univ a)
    rw [upperEnv_eq_of_mem hd A hA g (fun a _ b _ => hg a b) ha] at h1
    exact h1
  linarith

/-- **A value certificate is a covering**: every point `y` lies within slack distance
`E y - Estar + ε` of an evaluated point, for every lower bound `Estar` on the energy. -/
theorem cover_of_isValueCertificate {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g)
    {f : X → ℝ} {A : Finset X} {hA : A.Nonempty} {ε Estar : ℝ} (hE : ∀ y, Estar ≤ f y + g y)
    (h : IsValueCertificate d f g A hA ε) (y : X) : ∃ a ∈ A, Covers d f g Estar ε a y := by
  unfold IsValueCertificate at h
  have hU : Estar ≤ univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y := by
    apply Finset.le_inf'
    intro z _
    have h1 := le_upperEnv hg A hA g (fun _ _ => rfl) z
    have h2 := hE z
    linarith
  have hL : certLB d f g A hA ≤ f y + g y - slackFrom d g A hA y := by
    rw [certLB_eq]
    exact Finset.inf'_le (fun y => f y + g y - slackFrom d g A hA y) (mem_univ y)
  obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
  have hs : slackFrom d g A hA y = slack d g a y := hmin
  refine ⟨a, ha, ?_⟩
  unfold Covers
  linarith

/-- **A point certificate is a configuration certificate** for a best evaluated point. -/
theorem isConfigCertificate_of_isCertificate {d : X → X → ℝ} (hd : IsEnvelope d) {g : X → ℝ}
    (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {ε : ℝ}
    (h : IsCertificate d f g A hA ε) : ∃ x ∈ A, IsConfigCertificate d f g A hA x ε := by
  obtain ⟨x, hx, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => f a + g a)
  have hUB : certUB f g A hA = f x + g x := hmin
  refine ⟨x, hx, fun y => ?_⟩
  unfold IsCertificate at h
  have h1 : certLB d f g A hA ≤ f y + lowerEnv d A hA g y :=
    Finset.inf'_le (fun y => f y + lowerEnv d A hA g y) (mem_univ y)
  have h2 := condEnv_le_bracket d A hA g x y
  rw [upperEnv_eq_of_mem hd A hA g (fun a _ b _ => hg a b) hx] at h2
  linarith

/-- **A configuration certificate becomes a point certificate after one more evaluation**: if
`x` is certified as an `ε`-minimiser by the evaluations on `A`, then `insert x A` is a point
`ε`-certificate. -/
theorem isCertificate_insert_of_isConfigCertificate [DecidableEq X] {d : X → X → ℝ}
    {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {x : X}
    {ε : ℝ} (h : IsConfigCertificate d f g A hA x ε) :
    IsCertificate d f g (insert x A) (insert_nonempty x A) ε := by
  rw [isCertificate_iff_cover]
  intro y
  have hUB : certUB f g (insert x A) (insert_nonempty x A) ≤ f x + g x :=
    Finset.inf'_le (fun a => f a + g a) (mem_insert_self x A)
  have hy := h y
  unfold condEnv at hy
  rcases min_le_iff.mp hy with h1 | h1
  · refine ⟨x, mem_insert_self x A, ?_⟩
    unfold slack
    linarith
  · obtain ⟨a, ha, hmin⟩ := Finset.exists_mem_eq_inf' hA (fun a => slack d g a y)
    have hs : slackFrom d g A hA y = slack d g a y := hmin
    have hU := le_upperEnv hg A hA g (fun _ _ => rfl) x
    have hL := lowerEnv_eq_sub_slack d g A hA y
    refine ⟨a, mem_insert_of_mem ha, ?_⟩
    linarith

/-- **Without any structure of the residual a configuration certificate can be free.**  If the
known part has an `ε`-sharp minimum at `x` for the conditional envelope given the evaluations on
`A`, no evaluation at `x` is needed to certify it — yet `x` may be a point that only itself
covers.  This is the precise sense in which the witness-size bound `anchor_necessary'` concerns
point and value certificates only: `x` is certified by `A`, and `insert x A` is a point
certificate. -/
theorem config_certificate_then_point {d : X → X → ℝ} (hd : IsEnvelope d) [DecidableEq X]
    {g : X → ℝ} (hg : Admissible d g) (f : X → ℝ) {A : Finset X} {hA : A.Nonempty} {x : X}
    {ε : ℝ} (h : IsConfigCertificate d f g A hA x ε) :
    (∀ g', Admissible d g' → (∀ a ∈ A, g' a = g a) → ∀ y, f x + g' x ≤ f y + g' y + ε) ∧
      IsCertificate d f g (insert x A) (insert_nonempty x A) ε :=
  ⟨(isConfigCertificate_iff hd hg f A hA x ε).mp h,
    isCertificate_insert_of_isConfigCertificate hg f h⟩

end MetricChain
