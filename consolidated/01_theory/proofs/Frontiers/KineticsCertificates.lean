import Mathlib
import proofs.CertificateAlgebra
import proofs.Frontiers.PartitionCertificate

/-!
# Workstream K (science division): barrier certificates on top of the verified min-kernels

Machine-checked core of `docs/science/workstreams/SK_REPORT.md`, §2 (Theorem K1(a), Proposition K2(a),
Lemma K5, Theorem K6 and its Corollary K6.1, Theorem K10).

* `cut_sound` — the `(min,max)` cut certificate on an arbitrary move graph: if every step that
  leaves a set `S` lands on energy `≥ t`, every walk from inside `S` to outside `S` visits a
  configuration of energy `≥ t`.
* `pinned_bounds`, `neg_cone_admissible`, `cone_admissible` — the pinned residual `g - g a` lies
  between the two cone residuals `-d a ·` and `d · a`, and both are admissible.
* `robust_cut_sound`, `robust_path_sound` — lower and upper ends of the robust barrier-height
  interval: a cut for `f - d a ·` certifies the height for every admissible residual; a walk for
  `f + d · a` bounds it from above for every admissible residual.
* `box_cut_barrier` — composition with `verify_sound`: one accepted certificate per wall box of a
  box `D` certifies a barrier for every walk of single-site moves leaving `D`.
* `box_cut_barrier_residual`, `certified_trap_height` — the same on top of `verifyR_sound`, for
  every residual of the bounded-difference class with the published anchors.
* `level_cut_sound` — counting cuts: a statistic that increases by at most one per move.
* `ferro_barrier`, `ferroResidual_trap`, `ferroW_trap` — kernel-evaluated instances
  (`decide +kernel`): a barrier, a robust barrier height, a kinetic trap.
* `trap_survival`, `trap_certificate`, `trap_certificate_weighted` — discrete-time kinetic trap for
  every stochastic kernel with given stationary weights (no reversibility).
* `box_trap_certificate` — composition with `zverifyTop_sound`: intervals returned by the partition
  kernel on a box and on its wall boxes bound the survival probability of every stationary
  single-site dynamics.

## Provenance

Written by the Scientific Discovery Division (its workstream K; branch `research/scientific-translation`,
`experiments/science/ws_K/KineticsCertificates.lean`, SHA-256 `fc9c7f28e5ad5fec806c…`, as at its commit `25626db`
and unchanged at `a841cb4`), sent with its message SCI-MSG-0005 and adopted here at its request K-T1.  Compiled
unchanged against this library; the only changes are this paragraph, which replaces the sentence that the file is
not part of the library, and the removal of the closing block of axiom-printing commands (the audit of
`proofs/AxiomAudit.lean` covers every declaration).  The tree checker built on these notions is
`proofs/Frontiers/BarrierCertificate.lean`.
-/

namespace MetricChain.Kinetics

open MetricChain

/-- A walk `p 0, …, p m` on a move relation `adj`. -/
def IsWalk {X : Type*} (adj : X → X → Prop) (p : ℕ → X) (m : ℕ) : Prop :=
  ∀ j, j < m → adj (p j) (p (j + 1))

/-- Discrete intermediate value: a sequence that starts in `S` and ends outside `S` has a step
that leaves `S`. -/
theorem exists_exit {X : Type*} (S : Set X) (p : ℕ → X) :
    ∀ m, p 0 ∈ S → p m ∉ S → ∃ j, j < m ∧ p j ∈ S ∧ p (j + 1) ∉ S := by
  intro m
  induction m with
  | zero =>
    intro h0 hm
    exact absurd h0 hm
  | succ m ih =>
    intro h0 hm
    by_cases h : p m ∈ S
    · exact ⟨m, Nat.lt_succ_self m, h, hm⟩
    · obtain ⟨j, hj, h1, h2⟩ := ih h0 h
      exact ⟨j, Nat.lt_succ_of_lt hj, h1, h2⟩

/-- **Cut soundness (Theorem K1, soundness direction).**  If every move from `S` to its complement
lands on a configuration of energy at least `t`, then every walk from `S` to the complement of `S`
visits a configuration of energy at least `t`: the minimax barrier is at least `t`. -/
theorem cut_sound {X : Type*} (adj : X → X → Prop) (E : X → ℝ) (S : Set X) (t : ℝ)
    (hwall : ∀ x y, x ∈ S → y ∉ S → adj x y → t ≤ E y)
    (p : ℕ → X) (m : ℕ) (hp : IsWalk adj p m) (ha : p 0 ∈ S) (hb : p m ∉ S) :
    ∃ j, j ≤ m ∧ t ≤ E (p j) := by
  obtain ⟨j, hj, h1, h2⟩ := exists_exit S p m ha hb
  exact ⟨j + 1, hj, hwall _ _ h1 h2 (hp j hj)⟩

/-- **Counting (level) cut (Proposition K2(c)).**  If a statistic `q` increases by at most one per
move and every configuration on the level `q = r` has energy at least `t`, then every walk from
`q < r` to `q ≥ r` visits a configuration of energy at least `t`. -/
theorem level_cut_sound {X : Type*} (adj : X → X → Prop) (E : X → ℝ) (q : X → ℕ) (r : ℕ) (t : ℝ)
    (hstep : ∀ x y, adj x y → q y ≤ q x + 1)
    (hlevel : ∀ y, q y = r → t ≤ E y)
    (p : ℕ → X) (m : ℕ) (hp : IsWalk adj p m) (ha : q (p 0) < r) (hb : r ≤ q (p m)) :
    ∃ j, j ≤ m ∧ t ≤ E (p j) := by
  refine cut_sound adj E {x | q x < r} t ?_ p m hp ha (by simpa using hb)
  intro x y hx hy hxy
  have h1 : q x < r := hx
  have h2 : r ≤ q y := by simpa using hy
  have h3 := hstep x y hxy
  exact hlevel y (by omega)

/-! ### The pinned class and the two cone residuals -/

/-- The pinned residual lies between the two cone residuals. -/
theorem pinned_bounds {X : Type*} {d : X → X → ℝ} {g : X → ℝ} (hg : Admissible d g) (a x : X) :
    -d a x ≤ g x - g a ∧ g x - g a ≤ d x a := by
  constructor
  · have := hg a x
    linarith
  · exact hg x a

/-- The lower cone residual `-d a ·` is admissible. -/
theorem neg_cone_admissible {X : Type*} {d : X → X → ℝ} (hd : IsEnvelope d) (a : X) :
    Admissible d (fun x => -d a x) := by
  intro x y
  have := hd.triangle a x y
  simp only
  linarith

/-- The upper cone residual `d · a` is admissible. -/
theorem cone_admissible {X : Type*} {d : X → X → ℝ} (hd : IsEnvelope d) (a : X) :
    Admissible d (fun x => d x a) := by
  intro x y
  have := hd.triangle x y a
  simp only
  linarith

/-- **Robust cut certificate (Theorem K6, lower end).**  A cut for the anchored-down energy
`f - d a ·` with wall height `t` above `f a` certifies that for **every** admissible residual `g`
every walk from `a` out of `S` climbs at least `t` above the true energy of `a`. -/
theorem robust_cut_sound {X : Type*} (adj : X → X → Prop) (f : X → ℝ) (d : X → X → ℝ) (a : X)
    (S : Set X) (t : ℝ)
    (hwall : ∀ x y, x ∈ S → y ∉ S → adj x y → t ≤ f y - d a y - f a)
    (g : X → ℝ) (hg : Admissible d g)
    (p : ℕ → X) (m : ℕ) (hp : IsWalk adj p m) (h0 : p 0 = a) (ha : a ∈ S) (hb : p m ∉ S) :
    ∃ j, j ≤ m ∧ t ≤ (f (p j) + g (p j)) - (f a + g a) := by
  have ha0 : p 0 ∈ S := by rw [h0]; exact ha
  obtain ⟨j, hj, h1, h2⟩ := exists_exit S p m ha0 hb
  refine ⟨j + 1, hj, ?_⟩
  have h3 := hwall _ _ h1 h2 (hp j hj)
  have h4 := hg a (p (j + 1))
  linarith

/-- **Robust path certificate (Theorem K6, upper end).**  A walk whose anchored-up energies
`f + d · a` stay at most `t` above `f a` stays at most `t` above the true energy of `a` for
**every** admissible residual. -/
theorem robust_path_sound {X : Type*} (f : X → ℝ) (d : X → X → ℝ) (a : X) (t : ℝ)
    (p : ℕ → X) (m : ℕ) (hpath : ∀ j, j ≤ m → f (p j) + d (p j) a - f a ≤ t)
    (g : X → ℝ) (hg : Admissible d g) :
    ∀ j, j ≤ m → (f (p j) + g (p j)) - (f a + g a) ≤ t := by
  intro j hj
  have h1 := hpath j hj
  have h2 := hg (p j) a
  linarith

/-- The two ends are attained: for the cone residuals the pinned energy is the anchored energy. -/
theorem neg_cone_pinned {X : Type*} {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (a y : X) :
    (f y + (fun x => -d a x) y) - (f a + (fun x => -d a x) a) = f y - d a y - f a := by
  simp only [hd.self a]
  ring

theorem cone_pinned {X : Type*} {d : X → X → ℝ} (hd : IsEnvelope d) (f : X → ℝ) (a y : X) :
    (f y + (fun x => d x a) y) - (f a + (fun x => d x a) a) = f y + d y a - f a := by
  simp only [hd.self a]
  ring

/-! ### Composition with the verified kernels: box cuts on a product space -/

variable {n k : ℕ}

/-- A single-site move (or no move): the two configurations agree off one site. -/
def SingleSite (x y : Config n k) : Prop := ∃ i : Fin n, ∀ j, j ≠ i → x j = y j

/-- The `i`-th wall box of the box `D`: site `i` takes a state outside `D i`, every other site
stays in its domain. -/
def wallBox (D : Dom n k) (i : Fin n) : Dom n k :=
  Function.update D i ((List.finRange k).filter fun s => s ∉ D i)

/-- A single-site move that leaves the box `D` lands in one of its `n` wall boxes. -/
theorem mem_wallBox_of_exit {D : Dom n k} {x y : Config n k} (hx : InBox D x) (hy : ¬ InBox D y)
    (h : SingleSite x y) : ∃ i, InBox (wallBox D i) y := by
  obtain ⟨i, hi⟩ := h
  refine ⟨i, fun j => ?_⟩
  unfold wallBox
  by_cases hj : j = i
  · subst hj
    rw [Function.update_self]
    have hyj : y j ∉ D j := by
      intro hmem
      apply hy
      intro l
      by_cases hl : l = j
      · subst hl
        exact hmem
      · rw [← hi l hl]
        exact hx l
    simp [List.mem_filter, hyj]
  · rw [Function.update_of_ne hj, ← hi j hj]
    exact hx j

/-- **Barrier certificate for a pairwise energy (Proposition K2(a), box cut).**  If the kernel accepts a
lower-bound certificate with bound `L` on each of the `n` wall boxes of `D`, then every walk of
single-site moves that starts in the box `D` and ends outside it visits a configuration of energy
at least `L`. -/
theorem box_cut_barrier (I : PairInstance n k) (D : Dom n k) (L : ℚ) (certs : Fin n → Cert n k)
    (hv : ∀ i, verify (certs i) I (wallBox D i) L = true)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m)
    (ha : InBox D (p 0)) (hb : ¬ InBox D (p m)) :
    ∃ j, j ≤ m ∧ L ≤ I.energy (p j) := by
  obtain ⟨j, hj, h1, h2⟩ := exists_exit {x | InBox D x} p m ha hb
  obtain ⟨i, hi⟩ := mem_wallBox_of_exit h1 h2 (hp j hj)
  exact ⟨j + 1, hj, verify_sound (certs i) I (wallBox D i) L (hv i) (p (j + 1)) hi⟩

/-- **Robust barrier certificate (residual kernel; Corollary K6.1).**  The same with `verifyR`: for **every**
residual of the class (bounded differences, published anchor values) every walk of single-site
moves leaving the box `D` visits a configuration of true energy at least `L`. -/
theorem box_cut_barrier_residual (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (certs : Fin n → RCert n k)
    (hv : ∀ i, verifyR (certs i) P (wallBox D i) L = true)
    (g : Config n k → ℝ) (hg : ResidualClass P g)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m)
    (ha : InBox D (p 0)) (hb : ¬ InBox D (p m)) :
    ∃ j, j ≤ m ∧ (L : ℝ) ≤ (P.base.energy (p j) : ℝ) + g (p j) := by
  obtain ⟨j, hj, h1, h2⟩ := exists_exit {x | InBox D x} p m ha hb
  obtain ⟨i, hi⟩ := mem_wallBox_of_exit h1 h2 (hp j hj)
  exact ⟨j + 1, hj, verifyR_sound (certs i) P (wallBox D i) L (hv i) g hg (p (j + 1)) hi⟩

/-- **Certified kinetic trap.**  If the walk starts at an evaluated anchor `(a, v)` inside the box,
the true energy climbs by at least `L - (E a + v)` before the walk can leave the box — for every
residual of the class. -/
theorem certified_trap_height (P : RProblem n k) (D : Dom n k) (L : ℚ)
    (certs : Fin n → RCert n k)
    (hv : ∀ i, verifyR (certs i) P (wallBox D i) L = true)
    (g : Config n k → ℝ) (hg : ResidualClass P g)
    (av : Config n k × ℚ) (hav : av ∈ P.anchors)
    (p : ℕ → Config n k) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = av.1) (ha : InBox D av.1) (hb : ¬ InBox D (p m)) :
    ∃ j, j ≤ m ∧ ((L - (P.base.energy av.1 + av.2) : ℚ) : ℝ) ≤
      ((P.base.energy (p j) : ℝ) + g (p j)) - ((P.base.energy (p 0) : ℝ) + g (p 0)) := by
  have ha0 : InBox D (p 0) := by rw [h0]; exact ha
  obtain ⟨j, hj, hL⟩ := box_cut_barrier_residual P D L certs hv g hg p m hp ha0 hb
  refine ⟨j, hj, ?_⟩
  have hgv := hg.2 av hav
  rw [h0, hgv]
  push_cast
  linarith


/-! ### Kernel-evaluated example (non-vacuity)

Three binary sites, ferromagnetic pair cost `2` per disagreeing pair, field `-1/2` on state `1`:
`E(000) = 0`, `E(111) = -3/2`, and every single flip out of `000` costs `7/2`.  The box `{000}`
has three wall boxes; the kernel accepts the bound `7/2` on each of them (run inside Lean's
kernel), so every walk of single-site moves that leaves `000` visits energy `≥ 7/2`. -/

/-- A double-well instance on three binary sites. -/
def ferro : PairInstance 3 2 where
  h := fun _ a => if a = 1 then -1 / 2 else 0
  J := fun i j a b => if i < j ∧ a ≠ b then 2 else 0

/-- The box consisting of the single configuration `000`. -/
def well : Dom 3 2 := fun _ => [0]

theorem ferro_wall_verified :
    ∀ i, verify (exhaustive3 ferro) ferro (wallBox well i) (7 / 2) = true := by decide +kernel

/-- The kernel rejects the (false) wall bound `4`. -/
theorem ferro_wall_rejects :
    verify (exhaustive3 ferro) ferro (wallBox well 0) 4 = false := by decide +kernel

/-- **Certified barrier, kernel-evaluated.**  Every walk of single-site moves from `000` to any
other configuration visits a configuration of energy at least `7/2`. -/
theorem ferro_barrier (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (ha : InBox well (p 0)) (hb : ¬ InBox well (p m)) :
    ∃ j, j ≤ m ∧ (7 / 2 : ℚ) ≤ ferro.energy (p j) :=
  box_cut_barrier ferro well (7 / 2) (fun _ => exhaustive3 ferro) ferro_wall_verified p m hp ha hb

/-- The start has energy `0` and the bound is attained on the wall: the certified barrier height
`7/2` is exact. -/
theorem ferro_start : ferro.energy ![0, 0, 0] = 0 := by decide +kernel

theorem ferro_wall_attained : ferro.energy ![1, 0, 0] = 7 / 2 := by decide +kernel

/-- The same landscape with an unknown residual: bounded differences `1/4` per site and one
evaluated anchor, `g(000) = 0`. -/
def ferroResidual : RProblem 3 2 where
  base := ferro
  c := fun _ => 1 / 4
  anchors := [(![0, 0, 0], 0)]

theorem ferroResidual_wall_verified :
    ∀ i, verifyR (.anchor 0 (exhaustive3 (ferro.anchored (fun _ => 1 / 4) ![0, 0, 0])))
      ferroResidual (wallBox well i) (13 / 4) = true := by decide +kernel

/-- **Certified kinetic trap under an unknown residual, kernel-evaluated.**  For every residual
with bounded differences `1/4` and `g(000) = 0`, every walk of single-site moves that starts at
`000` and leaves it climbs at least `13/4` above the true energy of `000`. -/
theorem ferroResidual_trap (g : Config 3 2 → ℝ) (hg : ResidualClass ferroResidual g)
    (p : ℕ → Config 3 2) (m : ℕ) (hp : IsWalk SingleSite p m)
    (h0 : p 0 = ![0, 0, 0]) (hb : ¬ InBox well (p m)) :
    ∃ j, j ≤ m ∧ ((13 / 4 - (ferro.energy ![0, 0, 0] + 0) : ℚ) : ℝ) ≤
      ((ferro.energy (p j) : ℝ) + g (p j)) - ((ferro.energy (p 0) : ℝ) + g (p 0)) :=
  certified_trap_height ferroResidual well (13 / 4)
    (fun _ => .anchor 0 (exhaustive3 (ferro.anchored (fun _ => 1 / 4) ![0, 0, 0])))
    ferroResidual_wall_verified g hg (![0, 0, 0], 0) (by simp [ferroResidual]) p m hp h0
    (by intro i; fin_cases i <;> simp [well]) hb

/-! ### Rate certificates: a kinetic trap for every stationary local dynamics

Discrete time.  `P` is a stochastic kernel on a finite state space with stationary weights `w`
(not necessarily reversible, not necessarily normalised).  `surv P A t x` is the probability that
the chain started at `x` stays in `A` during its first `t` steps. -/

section Trap

variable {X : Type*} [Fintype X] [DecidableEq X]

/-- Survival function of the chain killed when it leaves `A`. -/
noncomputable def surv (P : X → X → ℝ) (A : Finset X) : ℕ → X → ℝ
  | 0, _ => 1
  | t + 1, x => ∑ y ∈ A, P x y * surv P A t y

omit [Fintype X] [DecidableEq X] in
theorem surv_nonneg (P : X → X → ℝ) (hP0 : ∀ x y, 0 ≤ P x y) (A : Finset X) :
    ∀ t x, 0 ≤ surv P A t x := by
  intro t
  induction t with
  | zero =>
    intro x
    simp [surv]
  | succ t ih =>
    intro x
    simp only [surv]
    exact Finset.sum_nonneg fun y _ => mul_nonneg (hP0 x y) (ih y)

omit [DecidableEq X] in
theorem surv_le_one (P : X → X → ℝ) (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1)
    (A : Finset X) : ∀ t x, surv P A t x ≤ 1 := by
  intro t
  induction t with
  | zero =>
    intro x
    simp [surv]
  | succ t ih =>
    intro x
    simp only [surv]
    calc ∑ y ∈ A, P x y * surv P A t y ≤ ∑ y ∈ A, P x y := by
          apply Finset.sum_le_sum
          intro y _
          exact mul_le_of_le_one_right (hP0 x y) (ih y)
      _ ≤ ∑ y, P x y :=
          Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ A) (fun y _ _ => hP0 x y)
      _ = 1 := hP1 x

/-- **Stationary flux bound (Theorem K10, discrete-time form).**  For any stochastic kernel with
stationary weights `w`, the stationary mass that is still in `A` after `T` steps is at least the
mass of `A` minus `T` times the one-step flux into `A`.  No reversibility is used. -/
theorem trap_survival (P : X → X → ℝ) (w : X → ℝ) (A : Finset X)
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1) (hw0 : ∀ x, 0 ≤ w x)
    (hstat : ∀ y, ∑ x, w x * P x y = w y) (T : ℕ) :
    ∑ x ∈ A, w x - T * (∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y) ≤ ∑ x ∈ A, w x * surv P A T x := by
  induction T with
  | zero => simp [surv]
  | succ T ih =>
    have hflux : ∀ y, ∑ x ∈ A, w x * P x y = w y - ∑ x ∈ Aᶜ, w x * P x y := by
      intro y
      have h := Finset.sum_add_sum_compl A (fun x => w x * P x y)
      rw [hstat y] at h
      linarith
    have hstep : ∑ x ∈ A, w x * surv P A (T + 1) x
        = ∑ y ∈ A, w y * surv P A T y
          - ∑ y ∈ A, (∑ x ∈ Aᶜ, w x * P x y) * surv P A T y := by
      calc ∑ x ∈ A, w x * surv P A (T + 1) x
          = ∑ x ∈ A, ∑ y ∈ A, w x * P x y * surv P A T y := by
            apply Finset.sum_congr rfl
            intro x _
            simp only [surv]
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro y _
            ring
        _ = ∑ y ∈ A, ∑ x ∈ A, w x * P x y * surv P A T y := Finset.sum_comm
        _ = ∑ y ∈ A, (∑ x ∈ A, w x * P x y) * surv P A T y := by
            apply Finset.sum_congr rfl
            intro y _
            rw [Finset.sum_mul]
        _ = ∑ y ∈ A, (w y - ∑ x ∈ Aᶜ, w x * P x y) * surv P A T y := by
            apply Finset.sum_congr rfl
            intro y _
            rw [hflux y]
        _ = ∑ y ∈ A, w y * surv P A T y
              - ∑ y ∈ A, (∑ x ∈ Aᶜ, w x * P x y) * surv P A T y := by
            rw [← Finset.sum_sub_distrib]
            apply Finset.sum_congr rfl
            intro y _
            ring
    have hloss : ∑ y ∈ A, (∑ x ∈ Aᶜ, w x * P x y) * surv P A T y
        ≤ ∑ y ∈ A, ∑ x ∈ Aᶜ, w x * P x y := by
      apply Finset.sum_le_sum
      intro y _
      have h1 : 0 ≤ ∑ x ∈ Aᶜ, w x * P x y :=
        Finset.sum_nonneg fun x _ => mul_nonneg (hw0 x) (hP0 x y)
      exact mul_le_of_le_one_right h1 (surv_le_one P hP0 hP1 A T y)
    have hcomm : ∑ y ∈ A, ∑ x ∈ Aᶜ, w x * P x y = ∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y :=
      Finset.sum_comm
    rw [hstep]
    push_cast
    linarith

/-- **Rate certificate, soundness (certified kinetic trap).**  Let the chain be stationary for the
weights `w` and local in the sense that `A` can be entered in one step only from the wall `W`.
If `U` bounds the weight of the wall from above and `Lo > 0` bounds the weight of `A` from below
(two partition-function certificates), then the chain started from the stationary law restricted
to `A` is still in `A` after `T` steps with probability at least `1 - T * U / Lo`. -/
theorem trap_certificate (P : X → X → ℝ) (w : X → ℝ) (A W : Finset X)
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1) (hw0 : ∀ x, 0 ≤ w x)
    (hstat : ∀ y, ∑ x, w x * P x y = w y)
    (hlocal : ∀ x ∈ Aᶜ, x ∉ W → ∀ y ∈ A, P x y = 0)
    (U Lo : ℝ) (hU : ∑ x ∈ W, w x ≤ U) (hLo : Lo ≤ ∑ x ∈ A, w x) (hLo0 : 0 < Lo) (T : ℕ) :
    1 - T * (U / Lo) ≤ (∑ x ∈ A, w x * surv P A T x) / (∑ x ∈ A, w x) := by
  have hfluxW : ∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y ≤ ∑ x ∈ W, w x := by
    calc ∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y
        ≤ ∑ x ∈ Aᶜ, (if x ∈ W then w x else 0) := by
          apply Finset.sum_le_sum
          intro x hx
          by_cases hxW : x ∈ W
          · simp only [hxW, if_true]
            rw [← Finset.mul_sum]
            have h1 : ∑ y ∈ A, P x y ≤ 1 := by
              calc ∑ y ∈ A, P x y ≤ ∑ y, P x y :=
                    Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ A)
                      (fun y _ _ => hP0 x y)
                _ = 1 := hP1 x
            exact mul_le_of_le_one_right (hw0 x) h1
          · simp only [hxW, if_false]
            apply le_of_eq
            apply Finset.sum_eq_zero
            intro y hy
            rw [hlocal x hx hxW y hy, mul_zero]
      _ ≤ ∑ x, (if x ∈ W then w x else 0) := by
          apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
          intro x _ _
          by_cases hxW : x ∈ W
          · simp only [hxW, if_true]
            exact hw0 x
          · simp only [hxW, if_false]
            exact le_rfl
      _ = ∑ x ∈ W, w x := by
          rw [Finset.sum_ite_mem, Finset.univ_inter]
  have key := trap_survival P w A hP0 hP1 hw0 hstat T
  have hU0 : 0 ≤ U := le_trans (Finset.sum_nonneg fun x _ => hw0 x) hU
  have hmpos : 0 < ∑ x ∈ A, w x := lt_of_lt_of_le hLo0 hLo
  have hT0 : (0 : ℝ) ≤ (T : ℝ) := Nat.cast_nonneg T
  have h5 : U ≤ U / Lo * ∑ x ∈ A, w x := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hLo0]
    exact mul_le_mul_of_nonneg_left hLo hU0
  have h6 : (T : ℝ) * U ≤ (T : ℝ) * (U / Lo * ∑ x ∈ A, w x) :=
    mul_le_mul_of_nonneg_left h5 hT0
  have h7 : (T : ℝ) * (∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y) ≤ (T : ℝ) * U :=
    mul_le_mul_of_nonneg_left (le_trans hfluxW hU) hT0
  rw [le_div_iff₀ hmpos]
  calc (1 - T * (U / Lo)) * ∑ x ∈ A, w x
      = ∑ x ∈ A, w x - T * (U / Lo * ∑ x ∈ A, w x) := by ring
    _ ≤ ∑ x ∈ A, w x - T * (∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y) := by linarith
    _ ≤ ∑ x ∈ A, w x * surv P A T x := key

/-- **Rate certificate, weighted form.**  `κ x` bounds the one-step probability of entering `A`
from `x ∉ A` (for a Metropolis sampler with uniform proposals among `deg` single-site moves,
`κ x = (number of neighbours of x in A) / deg`); `U` bounds the `κ`-weighted weight of the
complement and `Lo > 0` bounds the weight of `A` from below.  Then the chain started from the
stationary law restricted to `A` is still in `A` after `T` steps with probability at least
`1 - T * U / Lo`. -/
theorem trap_certificate_weighted (P : X → X → ℝ) (w κ : X → ℝ) (A : Finset X)
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1) (hw0 : ∀ x, 0 ≤ w x)
    (hstat : ∀ y, ∑ x, w x * P x y = w y)
    (hκ : ∀ x ∈ Aᶜ, ∑ y ∈ A, P x y ≤ κ x)
    (U Lo : ℝ) (hU : ∑ x ∈ Aᶜ, w x * κ x ≤ U) (hLo : Lo ≤ ∑ x ∈ A, w x) (hLo0 : 0 < Lo) (T : ℕ) :
    1 - T * (U / Lo) ≤ (∑ x ∈ A, w x * surv P A T x) / (∑ x ∈ A, w x) := by
  have hflux : ∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y ≤ ∑ x ∈ Aᶜ, w x * κ x := by
    apply Finset.sum_le_sum
    intro x hx
    rw [← Finset.mul_sum]
    exact mul_le_mul_of_nonneg_left (hκ x hx) (hw0 x)
  have hflux0 : 0 ≤ ∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y :=
    Finset.sum_nonneg fun x _ => Finset.sum_nonneg fun y _ => mul_nonneg (hw0 x) (hP0 x y)
  have key := trap_survival P w A hP0 hP1 hw0 hstat T
  have hU0 : 0 ≤ U := le_trans hflux0 (le_trans hflux hU)
  have hmpos : 0 < ∑ x ∈ A, w x := lt_of_lt_of_le hLo0 hLo
  have hT0 : (0 : ℝ) ≤ (T : ℝ) := Nat.cast_nonneg T
  have h5 : U ≤ U / Lo * ∑ x ∈ A, w x := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hLo0]
    exact mul_le_mul_of_nonneg_left hLo hU0
  have h6 : (T : ℝ) * U ≤ (T : ℝ) * (U / Lo * ∑ x ∈ A, w x) :=
    mul_le_mul_of_nonneg_left h5 hT0
  have h7 : (T : ℝ) * (∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y) ≤ (T : ℝ) * U :=
    mul_le_mul_of_nonneg_left (le_trans hflux hU) hT0
  rw [le_div_iff₀ hmpos]
  calc (1 - T * (U / Lo)) * ∑ x ∈ A, w x
      = ∑ x ∈ A, w x - T * (U / Lo * ∑ x ∈ A, w x) := by ring
    _ ≤ ∑ x ∈ A, w x - T * (∑ x ∈ Aᶜ, ∑ y ∈ A, w x * P x y) := by linarith
    _ ≤ ∑ x ∈ A, w x * surv P A T x := key

end Trap

/-! ### Rate certificate on top of the partition-function kernel (box cut) -/

section BoxTrap

variable {n k : ℕ}

theorem singleSite_symm {x y : Config n k} (h : SingleSite x y) : SingleSite y x := by
  obtain ⟨i, hi⟩ := h
  exact ⟨i, fun j hj => (hi j hj).symm⟩

/-- The `n` wall boxes of a box are pairwise disjoint. -/
theorem wallBox_pairwiseDisjoint (D : Dom n k) :
    ((Finset.univ : Finset (Fin n)) : Set (Fin n)).PairwiseDisjoint
      (fun i => boxFinset (wallBox D i)) := by
  intro i _ j _ hij
  rw [Function.onFun, Finset.disjoint_left]
  intro x hxi hxj
  have h1 := mem_boxFinset.mp hxi j
  have h2 := mem_boxFinset.mp hxj j
  unfold wallBox at h1 h2
  rw [Function.update_of_ne (Ne.symm hij)] at h1
  rw [Function.update_self] at h2
  simp [List.mem_filter] at h2
  exact h2 h1

/-- **Rate certificate, box cut, on top of `zverifyTop_sound` (§2.8 of the report).**  Let `I` be a
rational weight instance, `D` a box, and suppose the partition kernel returns the interval
`(loA, hiA)` on `D` and `(lo i, hi i)` on the `i`-th wall box.  Then for **every** stochastic
kernel `P` that is stationary for the weights of `I` and moves at most one site per step, the
chain started from the stationary law restricted to the box is still in the box after `T` steps
with probability at least `1 - T * (Σ_i hi i) / loA`. -/
theorem box_trap_certificate (I : WInstance n k) (D : Dom n k)
    (cA : ZCert n k) (cW : Fin n → ZCert n k) (loA hiA : ℚ) (lo hi : Fin n → ℚ)
    (hA : zverifyTop cA I D = some (loA, hiA))
    (hW : ∀ i, zverifyTop (cW i) I (wallBox D i) = some (lo i, hi i))
    (hloA : 0 < loA)
    (P : Config n k → Config n k → ℝ)
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1)
    (hstat : ∀ y, ∑ x, (I.weight x : ℝ) * P x y = (I.weight y : ℝ))
    (hlocal : ∀ x y, P x y ≠ 0 → SingleSite x y) (T : ℕ) :
    1 - T * ((∑ i, (hi i : ℝ)) / (loA : ℝ)) ≤
      (∑ x ∈ boxFinset D, (I.weight x : ℝ) * surv P (boxFinset D) T x) /
        (∑ x ∈ boxFinset D, (I.weight x : ℝ)) := by
  have hI : I.Nonneg := (zverifyTop_eq_some hA).1
  have hw0 : ∀ x, (0 : ℝ) ≤ (I.weight x : ℝ) := fun x => by
    exact_mod_cast I.weight_nonneg hI x
  have hloc : ∀ x ∈ (boxFinset D)ᶜ,
      x ∉ (Finset.univ : Finset (Fin n)).biUnion (fun i => boxFinset (wallBox D i)) →
        ∀ y ∈ boxFinset D, P x y = 0 := by
    intro x hx hxW y hy
    by_contra hne
    have hss := singleSite_symm (hlocal x y hne)
    have hxbox : ¬ InBox D x := fun h => (Finset.mem_compl.mp hx) (mem_boxFinset.mpr h)
    obtain ⟨i, hi⟩ := mem_wallBox_of_exit (mem_boxFinset.mp hy) hxbox hss
    exact hxW (Finset.mem_biUnion.mpr ⟨i, Finset.mem_univ i, mem_boxFinset.mpr hi⟩)
  have hU : ∑ x ∈ (Finset.univ : Finset (Fin n)).biUnion (fun i => boxFinset (wallBox D i)),
      (I.weight x : ℝ) ≤ ∑ i, (hi i : ℝ) := by
    rw [Finset.sum_biUnion (wallBox_pairwiseDisjoint D)]
    apply Finset.sum_le_sum
    intro i _
    have h := (zverifyTop_sound (cW i) I (wallBox D i) (lo i) (hi i) (hW i)).2
    unfold WInstance.Z at h
    have h' : ((∑ x ∈ boxFinset (wallBox D i), I.weight x : ℚ) : ℝ) ≤ ((hi i : ℚ) : ℝ) := by
      exact_mod_cast h
    rwa [Rat.cast_sum] at h'
  have hLo : (loA : ℝ) ≤ ∑ x ∈ boxFinset D, (I.weight x : ℝ) := by
    have h := (zverifyTop_sound cA I D loA hiA hA).1
    unfold WInstance.Z at h
    have h' : ((loA : ℚ) : ℝ) ≤ ((∑ x ∈ boxFinset D, I.weight x : ℚ) : ℝ) := by
      exact_mod_cast h
    rwa [Rat.cast_sum] at h'
  have hLo0 : (0 : ℝ) < (loA : ℝ) := by exact_mod_cast hloA
  exact trap_certificate P (fun x => (I.weight x : ℝ)) (boxFinset D)
    ((Finset.univ : Finset (Fin n)).biUnion (fun i => boxFinset (wallBox D i)))
    hP0 hP1 hw0 hstat hloc (∑ i, (hi i : ℝ)) (loA : ℝ) hU hLo hLo0 T

/-! ### Kernel-evaluated rate certificate (non-vacuity)

The double well of `ferro` in the weight domain: one-body weight `2` on state `1`, pair factor `1/8`
for a disagreeing pair.  `weight(000) = 1`, each single flip has weight `2·(1/8)² = 1/32`,
`weight(111) = 8`. -/

/-- The weight-domain double well on three binary sites. -/
def ferroW : WInstance 3 2 where
  w := fun _ a => if a = 1 then 2 else 1
  W := fun i j a b => if i < j ∧ a ≠ b then 1 / 8 else 1

/-- Exact pair factors on the `i`-th wall box of `well` (a single configuration). -/
def ferroWallBounds (i : Fin 3) : Fin 3 → Fin 3 → ℚ :=
  fun i' j' => if i' < j' ∧ (i' = i ∨ j' = i) then 1 / 8 else 1

theorem ferroW_basin_verified :
    zverifyTop (.leaf (fun _ _ => 1) (fun _ _ => 1)) ferroW well = some (1, 1) := by
  decide +kernel

theorem ferroW_wall_verified :
    ∀ i, zverifyTop (.leaf (ferroWallBounds i) (ferroWallBounds i)) ferroW (wallBox well i)
      = some (1 / 32, 1 / 32) := by
  decide +kernel

/-- **Certified kinetic trap, kernel-evaluated.**  For every stochastic kernel that is stationary
for the weights of `ferroW` and moves at most one site per step, the chain started at `000`
(the stationary law restricted to the box `{000}`) is still at `000` after `T` steps with
probability at least `1 - T * (3/32)`. -/
theorem ferroW_trap (P : Config 3 2 → Config 3 2 → ℝ)
    (hP0 : ∀ x y, 0 ≤ P x y) (hP1 : ∀ x, ∑ y, P x y = 1)
    (hstat : ∀ y, ∑ x, (ferroW.weight x : ℝ) * P x y = (ferroW.weight y : ℝ))
    (hlocal : ∀ x y, P x y ≠ 0 → SingleSite x y) (T : ℕ) :
    1 - T * ((∑ _i : Fin 3, ((1 / 32 : ℚ) : ℝ)) / ((1 : ℚ) : ℝ)) ≤
      (∑ x ∈ boxFinset well, (ferroW.weight x : ℝ) * surv P (boxFinset well) T x) /
        (∑ x ∈ boxFinset well, (ferroW.weight x : ℝ)) :=
  box_trap_certificate ferroW well (.leaf (fun _ _ => 1) (fun _ _ => 1))
    (fun i => .leaf (ferroWallBounds i) (ferroWallBounds i)) 1 1 (fun _ => 1 / 32) (fun _ => 1 / 32)
    ferroW_basin_verified ferroW_wall_verified (by norm_num) P hP0 hP1 hstat hlocal T

end BoxTrap

end MetricChain.Kinetics
