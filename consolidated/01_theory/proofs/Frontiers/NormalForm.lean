import Mathlib
import proofs.Frontiers.CertificateNotions

/-!
# Normal form: a known part is the gradient part of an asymmetric envelope

Found by an independent workstream (`docs/workstreams/C_REPORT.md`, Theorem C1) and verified by an
independent reviewer (`docs/reviews/R_C_review.md`); the statements below are its algebraic core
in the vocabulary of this development, together with the identification of certificates that
the workstream proved on paper.

* `reduce d φ` — the **reduced cost** `d a y + φ a - φ y` (Johnson reweighting).  It is again an
  envelope (`reduce_isEnvelope`; no sign condition), `Lip (reduce d φ) = φ + Lip d`
  (`admissible_reduce_iff`), the slack and both McShane envelopes are gauge invariant
  (`slack_reduce`, `lowerEnv_reduce`, `upperEnv_reduce`).
* `phEnv d f` — the Pasch–Hausdorff envelope `f^d y = min_x (f x + d x y)` of the known part:
  `phEnv_le`, `phEnv_le_add` (so `reduce d (phEnv d f) ≥ 0`: `reduce_phEnv_nonneg`), and
  `inf_add_phEnv_eq`: **the minimum of `f + g` equals the minimum of `f^d + g` for every admissible
  `g`** — regularising the known part changes nothing on the class.
* `certLB_normalForm`, `valueUB_normalForm`, `certUB_normalForm` — for every evaluated set `A` the
  certified lower bound, the value upper bound and (in normal form) the incumbent of the
  instance `(σ, 0, E^d)`, `σ = reduce d (phEnv d f)`, `E^d = f^d + g`, coincide with the certified
  bounds of `(d, f, g)`.
* `isValueCertificate_iff_normalForm` — hence **value certificates of `(d, f, g)` are exactly the
  point certificates of `(σ, 0, E^d)`**, set by set and accuracy by accuracy: an instance with a
  known part is an instance without one, in a nonnegative envelope whose asymmetry is the
  gradient of the regularised known part.  `isValueCertificate_normalForm_iff`: in normal form
  the two notions of certificate coincide.
* `client_eq_centre`, `gap_slack_lipschitz` — the covering relation in centre form:
  `s(a, y) - gap^d(y) = σ(a, y) - gap^d(a)`, and the regularised gap is 1-Lipschitz for the slack.
* `not_cocovered_centre` — the separation lemma behind the centre-form bound for best-first
  search (workstream C, Theorem C4).
-/

namespace MetricChain

open Finset

section Gauge

variable {X : Type*}

/-- Reduced cost of `d` under the potential `φ` (Johnson reweighting). -/
def reduce (d : X → X → ℝ) (φ : X → ℝ) (a y : X) : ℝ := d a y + φ a - φ y

/-- Reweighting preserves the envelope axioms (no sign condition is needed). -/
theorem reduce_isEnvelope {d : X → X → ℝ} (hd : IsEnvelope d) (φ : X → ℝ) :
    IsEnvelope (reduce d φ) := by
  refine ⟨fun x => ?_, fun x y z => ?_⟩
  · unfold reduce
    rw [hd.self]
    ring
  · have := hd.triangle x y z
    unfold reduce
    linarith

/-- **Gauge lemma.**  `g` is admissible for `d` iff `φ + g` is admissible for the reduced
envelope: `Lip (reduce d φ) = φ + Lip d`. -/
theorem admissible_reduce_iff (d : X → X → ℝ) (φ g : X → ℝ) :
    Admissible (reduce d φ) (fun x => φ x + g x) ↔ Admissible d g := by
  constructor
  · intro h x y
    have := h x y
    unfold reduce at this
    linarith
  · intro h x y
    have := h x y
    unfold reduce
    linarith

/-- The slack is gauge invariant. -/
theorem slack_reduce (d : X → X → ℝ) (φ g : X → ℝ) (a y : X) :
    slack (reduce d φ) (fun x => φ x + g x) a y = slack d g a y := by
  unfold slack reduce
  ring

/-- If the potential is co-admissible (`φ y ≤ φ x + d x y`), the reduced envelope is nonnegative. -/
theorem reduce_nonneg {d : X → X → ℝ} {φ : X → ℝ} (hφ : ∀ x y, φ y ≤ φ x + d x y) (a y : X) :
    0 ≤ reduce d φ a y := by
  have := hφ a y
  unfold reduce
  linarith

/-- The lower McShane envelope is gauge covariant. -/
theorem lowerEnv_reduce (d : X → X → ℝ) (φ g : X → ℝ) (A : Finset X) (hA : A.Nonempty) (y : X) :
    lowerEnv (reduce d φ) A hA (fun x => φ x + g x) y = φ y + lowerEnv d A hA g y := by
  unfold lowerEnv
  apply le_antisymm
  · apply Finset.sup'_le
    intro a ha
    have h : g a - d a y ≤ A.sup' hA (fun a => g a - d a y) :=
      Finset.le_sup' (fun a => g a - d a y) ha
    unfold reduce
    linarith
  · obtain ⟨a, ha, hEq⟩ := Finset.exists_mem_eq_sup' hA (fun a => g a - d a y)
    rw [hEq]
    have h : φ a + g a - reduce d φ a y ≤
        A.sup' hA (fun a => φ a + g a - reduce d φ a y) :=
      Finset.le_sup' (fun a => φ a + g a - reduce d φ a y) ha
    have e : φ a + g a - reduce d φ a y = φ y + (g a - d a y) := by
      unfold reduce
      ring
    linarith

/-- The upper McShane envelope is gauge covariant. -/
theorem upperEnv_reduce (d : X → X → ℝ) (φ g : X → ℝ) (A : Finset X) (hA : A.Nonempty) (y : X) :
    upperEnv (reduce d φ) A hA (fun x => φ x + g x) y = φ y + upperEnv d A hA g y := by
  unfold upperEnv
  apply le_antisymm
  · obtain ⟨a, ha, hEq⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d y a)
    rw [hEq]
    have h : A.inf' hA (fun a => φ a + g a + reduce d φ y a) ≤ φ a + g a + reduce d φ y a :=
      Finset.inf'_le (fun a => φ a + g a + reduce d φ y a) ha
    have e : φ a + g a + reduce d φ y a = φ y + (g a + d y a) := by
      unfold reduce
      ring
    linarith
  · apply Finset.le_inf'
    intro a ha
    have h : A.inf' hA (fun a => g a + d y a) ≤ g a + d y a :=
      Finset.inf'_le (fun a => g a + d y a) ha
    unfold reduce
    linarith

/-- Client form = centre form of the covering relation: `s(a, y) - gap(y) = σ(a, y) - gap(a)` for
the energy `E = φ + g` and `σ = reduce d φ`. -/
theorem client_eq_centre (d : X → X → ℝ) (φ g : X → ℝ) (Estar : ℝ) (a y : X) :
    slack d g a y - (φ y + g y - Estar) = reduce d φ a y - (φ a + g a - Estar) := by
  unfold slack reduce
  ring

/-- For a co-admissible potential the energy `φ + g` is 1-Lipschitz for the slack:
`gap(y) ≤ gap(x) + s(x, y)`. -/
theorem gap_slack_lipschitz {d : X → X → ℝ} {φ : X → ℝ} (hφ : ∀ x y, φ y ≤ φ x + d x y)
    (g : X → ℝ) (x y : X) : φ y + g y ≤ φ x + g x + slack d g x y := by
  have := hφ x y
  unfold slack
  linarith

/-- **Centre-form separation.**  In normal form (envelope `σ`, energy `E` admissible, `Estar ≤ E`):
two points `yj, yk` that are separated as consecutive best-first evaluations (`ε < σ yj yk` and
`gap yj ≤ σ yj yk`) cannot both lie in the shrunk ball of one centre `c`,
`σ c · ≤ θ (gap c + ε)`, when `σ` is `ρ`-quasi-symmetric at `(yj, c)` and `θ (2ρ + 3) ≤ 1`. -/
theorem not_cocovered_centre {σ : X → X → ℝ} (hσ : IsEnvelope σ) {E : X → ℝ}
    (hE : Admissible σ E) {Estar ρ θ ε : ℝ} {c yj yk : X}
    (hρ : 0 ≤ ρ) (hθρ : θ * (2 * ρ + 3) ≤ 1)
    (hgap : 0 ≤ E c - Estar) (hε : 0 ≤ ε)
    (hqs : σ yj c ≤ ρ * σ c yj)
    (hcj : σ c yj ≤ θ * (E c - Estar + ε)) (hck : σ c yk ≤ θ * (E c - Estar + ε))
    (hsepa : ε < σ yj yk) (hsepb : E yj - Estar ≤ σ yj yk) : False := by
  set r := θ * (E c - Estar + ε) with hr
  have htri := hσ.triangle yj c yk
  have hadm := hE c yj
  have h1 : ρ * σ c yj ≤ ρ * r := mul_le_mul_of_nonneg_left hcj hρ
  have h2 : (2 * ρ + 3) * r ≤ E c - Estar + ε := by
    have h3 : θ * (2 * ρ + 3) * (E c - Estar + ε) ≤ 1 * (E c - Estar + ε) :=
      mul_le_mul_of_nonneg_right hθρ (by linarith)
    have h4 : (2 * ρ + 3) * r = θ * (2 * ρ + 3) * (E c - Estar + ε) := by
      rw [hr]
      ring
    linarith
  nlinarith [h1, h2, htri, hadm, hqs, hck, hsepa, hsepb]

end Gauge

section NormalForm

variable {X : Type*} [Fintype X] [Nonempty X]

/-- The Pasch–Hausdorff envelope of the known part: `f^d y = min_x (f x + d x y)`. -/
noncomputable def phEnv (d : X → X → ℝ) (f : X → ℝ) (y : X) : ℝ :=
  univ.inf' univ_nonempty fun x => f x + d x y

theorem phEnv_exists (d : X → X → ℝ) (f : X → ℝ) (y : X) : ∃ x, phEnv d f y = f x + d x y := by
  obtain ⟨x, _, hx⟩ := Finset.exists_mem_eq_inf' univ_nonempty (fun x => f x + d x y)
  exact ⟨x, hx⟩

theorem phEnv_le_term (d : X → X → ℝ) (f : X → ℝ) (x y : X) : phEnv d f y ≤ f x + d x y :=
  Finset.inf'_le (fun x => f x + d x y) (mem_univ x)

/-- `f^d ≤ f`. -/
theorem phEnv_le {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (y : X) : phEnv d f y ≤ f y := by
  have h := phEnv_le_term d f y y
  rw [hd.self] at h
  linarith

/-- `f^d` is co-admissible: `f^d y ≤ f^d x + d x y`. -/
theorem phEnv_le_add {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (x y : X) :
    phEnv d f y ≤ phEnv d f x + d x y := by
  obtain ⟨z, hz⟩ := phEnv_exists d f x
  have h := phEnv_le_term d f z y
  have ht := hd.triangle z x y
  linarith

/-- The reduced envelope of the regularised known part is nonnegative: a quasi-metric. -/
theorem reduce_phEnv_nonneg {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (a y : X) :
    0 ≤ reduce d (phEnv d f) a y :=
  reduce_nonneg (fun x y => phEnv_le_add hd f x y) a y

/-- **Regularising the known part changes nothing on the class**: for every admissible `g`,
`min (f^d + g) = min (f + g)`. -/
theorem inf_add_phEnv_eq {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) {g : X → ℝ}
    (hg : Admissible d g) :
    (univ.inf' univ_nonempty fun y => phEnv d f y + g y) =
      univ.inf' univ_nonempty fun y => f y + g y := by
  apply le_antisymm
  · apply Finset.le_inf'
    intro y _
    have h1 : (univ.inf' univ_nonempty fun y => phEnv d f y + g y) ≤ phEnv d f y + g y :=
      Finset.inf'_le (fun y => phEnv d f y + g y) (mem_univ y)
    have h2 := phEnv_le hd f y
    linarith
  · apply Finset.le_inf'
    intro y _
    obtain ⟨x, hx⟩ := phEnv_exists d f y
    have h1 : (univ.inf' univ_nonempty fun y => f y + g y) ≤ f x + g x :=
      Finset.inf'_le (fun y => f y + g y) (mem_univ x)
    have h2 := hg x y
    linarith

/-- The certified lower bound of the normal form `(σ, 0, E^d)` is that of `(d, f, g)`. -/
theorem certLB_normalForm {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (A : Finset X)
    (hA : A.Nonempty) :
    certLB (reduce d (phEnv d f)) (fun _ => 0) (fun x => phEnv d f x + g x) A hA =
      certLB d f g A hA := by
  unfold certLB
  have h1 : (fun y => (fun _ : X => (0 : ℝ)) y +
      lowerEnv (reduce d (phEnv d f)) A hA (fun x => phEnv d f x + g x) y) =
      fun y => phEnv d f y + lowerEnv d A hA g y := by
    funext y
    rw [lowerEnv_reduce]
    ring
  rw [h1]
  exact inf_add_phEnv_eq hd f (lowerEnv_admissible hd A hA g)

/-- The value upper bound of the normal form is that of `(d, f, g)`. -/
theorem valueUB_normalForm {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (A : Finset X)
    (hA : A.Nonempty) :
    (univ.inf' univ_nonempty fun y => (fun _ : X => (0 : ℝ)) y +
        upperEnv (reduce d (phEnv d f)) A hA (fun x => phEnv d f x + g x) y) =
      univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y := by
  have h1 : (fun y => (fun _ : X => (0 : ℝ)) y +
      upperEnv (reduce d (phEnv d f)) A hA (fun x => phEnv d f x + g x) y) =
      fun y => phEnv d f y + upperEnv d A hA g y := by
    funext y
    rw [upperEnv_reduce]
    ring
  rw [h1]
  exact inf_add_phEnv_eq hd f (upperEnv_admissible hd A hA g)

/-- In normal form the incumbent (best evaluated energy) **is** the value upper bound: the
largest admissible residual compatible with the data attains its minimum at an evaluated
point. -/
theorem certUB_normalForm {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ) (A : Finset X)
    (hA : A.Nonempty) :
    certUB (fun _ => 0) (fun x => phEnv d f x + g x) A hA =
      univ.inf' univ_nonempty fun y => f y + upperEnv d A hA g y := by
  rw [← inf_add_phEnv_eq hd f (upperEnv_admissible hd A hA g)]
  unfold certUB
  apply le_antisymm
  · apply Finset.le_inf'
    intro y _
    obtain ⟨a, ha, hEq⟩ := Finset.exists_mem_eq_inf' hA (fun a => g a + d y a)
    have hup : upperEnv d A hA g y = g a + d y a := hEq
    have h1 : (A.inf' hA fun a => (fun _ : X => (0 : ℝ)) a + (phEnv d f a + g a)) ≤
        (fun _ : X => (0 : ℝ)) a + (phEnv d f a + g a) :=
      Finset.inf'_le (fun a => (fun _ : X => (0 : ℝ)) a + (phEnv d f a + g a)) ha
    have h2 := phEnv_le_add hd f y a
    simp only [zero_add] at h1
    simp only [zero_add]
    linarith
  · apply Finset.le_inf'
    intro a ha
    have h1 : (univ.inf' univ_nonempty fun y => phEnv d f y + upperEnv d A hA g y) ≤
        phEnv d f a + upperEnv d A hA g a :=
      Finset.inf'_le (fun y => phEnv d f y + upperEnv d A hA g y) (mem_univ a)
    have h2 : upperEnv d A hA g a ≤ g a + d a a :=
      Finset.inf'_le (fun b => g b + d a b) ha
    rw [hd.self] at h2
    simp only [zero_add]
    linarith

/-- **Normal form.**  An evaluated set is a value certificate of `(d, f, g)` at accuracy `ε` iff it
is a point certificate of the instance without known part `(σ, 0, E^d)`,
`σ = reduce d (phEnv d f)`, `E^d = f^d + g`. -/
theorem isValueCertificate_iff_normalForm {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ)
    (A : Finset X) (hA : A.Nonempty) (ε : ℝ) :
    IsValueCertificate d f g A hA ε ↔
      IsCertificate (reduce d (phEnv d f)) (fun _ => 0) (fun x => phEnv d f x + g x) A hA ε := by
  unfold IsValueCertificate IsCertificate
  rw [certUB_normalForm hd, certLB_normalForm hd]

/-- In normal form value certificates and point certificates coincide. -/
theorem isValueCertificate_normalForm_iff {d : X → X → ℝ} (hd : IsEnvelope d) (f g : X → ℝ)
    (A : Finset X) (hA : A.Nonempty) (ε : ℝ) :
    IsValueCertificate (reduce d (phEnv d f)) (fun _ => 0) (fun x => phEnv d f x + g x) A hA ε ↔
      IsCertificate (reduce d (phEnv d f)) (fun _ => 0) (fun x => phEnv d f x + g x) A hA ε := by
  unfold IsValueCertificate IsCertificate
  rw [valueUB_normalForm hd, certUB_normalForm hd]

end NormalForm

end MetricChain
