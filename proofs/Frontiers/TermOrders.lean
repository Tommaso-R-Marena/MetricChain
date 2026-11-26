import Mathlib
import proofs.Frontiers.AnchoredRemainder

/-!
# Every term in its own order of the sites, and the anchored split of a pair table

`AnchoredRemainder.lean` proves the remainder identity of the anchored expansion for one linear
order of the sites: the error of the anchored interpolant of order `m - 1` at `y` is the sum, over
the `m`-subsets `T` of the changed sites, of the mixed difference over `T` at the base point
`remainderBase x₀ y T`, which carries the states of `y` at the changed sites before every site of
`T` and the reference `x₀` everywhere else.  The order enters the base points only; the
interpolant does not depend on it and is additive in the function.  Hence a function that is a
finite sum of terms may be expanded with a different order for every term, and a term with at
most `m` *hosts* (the sites on whose states its constants depend most) that puts them last keeps
them at the reference in every base point: its constants need no maximum over the states of a
host outside `T`.  The statement (a remainder identity in which every term uses its own order of
the sites, with the hypothesis that a term has at most `m` hosts and that this is sharp) and the
anchored split of a pair table are the Scientific Discovery Division's (workstream P8, message
SCI-MSG-0027, requests P8-T1 and A18-T1); the proofs here are ours.

* `sitesBefore_notMem_of_few_after`, `remainderBase_host_anchor` — hosts stay at the anchor: a
  site with fewer than `|T|` sites strictly after it does not precede every site of `T`, so the
  base point of the remainder term of `T` is the reference there.  `card_after_lt_of_hosts_last`:
  this is the case at every site of a set of at most `|T|` sites that the order puts last.
* `mixedDiff_finset_sum`, `anchoredInterp_finset_sum` — mixed differences and anchored
  interpolants are additive over a finite sum of functions.
* `anchored_remainder_identity_orders` — for terms `F τ`, `τ ∈ terms`, and linear orders `ord τ`
  of the sites,
  `∑_τ F τ y - anchoredInterp m (∑_τ F τ) x₀ y = ∑_τ ∑_T mixedDiff (F τ) z T y`,
  the inner sum over the `m`-subsets `T` of the changed sites `supp x₀ y`, with `z` the base
  point `remainderBase x₀ y T` of the order `ord τ`.
* `anchored_remainder_bound_orders` — if fewer than `m` sites are strictly after every host of
  `τ` in the order `ord τ`, the remainder is at most `∑_τ ∑_T c τ T` for constants `c τ T` that
  bound the mixed differences of `F τ` over `T` at the base points that agree with the reference
  on `T` and at the hosts of `τ` outside `T`: no maximum over the states of a host outside `T`.
* `exists_linearOrder_hosts_last`, `exists_linearOrder_few_after`, `anchored_remainder_bound_hosts`
  — every set of sites can be put last; hence the same bound for terms with at most `m` hosts
  each, in a statement that mentions no order.
* `term_orders_sharp`, `term_orders_sharp_host_moves` — `m` hosts cannot be replaced by `m + 1`:
  on three binary sites, for the triple coupling with all three sites as hosts and `m = 2`, the
  constants `0` satisfy the host-anchored hypothesis and the remainder is `1`; and whatever the
  order, a host outside some pair `T` is off the reference in the base point of `T`.
* `anchoredSplit_row`, `anchoredSplit_col`, `anchoredSplit_sandwich`,
  `anchoredSplit_sandwich_extrema`, `anchoredSplit_exact_at_anchor` — the anchored split of a pair
  table `P : X → Y → ℝ` with anchors `a`, `b`: `A x = P x b`, `B y = P a y - P a b`,
  `D x y = P x y - A x - B y`.  The remainder `D` vanishes on the anchor row and on the anchor
  column; bounds `lo x ≤ D x y ≤ hi x` give `A x + B y + lo x ≤ P x y ≤ A x + B y + hi x`, two
  sums of one-site functions; the row minimum and maximum of `D` are such bounds, and they are
  `0` on the anchor row, where the split is exact.
-/

namespace MetricChain

open Finset

variable {ι : Type*} {σ : ι → Type*}

/-! ### Hosts stay at the anchor -/

/-- A site with fewer than `|T|` sites strictly after it does not precede every site of `T`:
otherwise `T` would be contained in the set of the sites after it. -/
theorem sitesBefore_notMem_of_few_after [Fintype ι] [LinearOrder ι] (S T : Finset ι) {h : ι}
    (hh : (univ.filter fun i => h < i).card < T.card) : h ∉ sitesBefore S T := by
  intro hmem
  have hsub : T ⊆ univ.filter fun i => h < i := fun t ht =>
    Finset.mem_filter.mpr ⟨Finset.mem_univ t, (mem_sitesBefore.mp hmem).2 t ht⟩
  exact absurd (Finset.card_le_card hsub) (not_le.mpr hh)

/-- **Hosts stay at the anchor.**  At a site with fewer than `|T|` sites strictly after it, the
base point of the remainder term of `T` is the reference: such a site is in its reference state
in every configuration that enters the mixed difference over `T`, unless it belongs to `T`. -/
theorem remainderBase_host_anchor [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    [∀ i, DecidableEq (σ i)] (x₀ y : ∀ i, σ i) (T : Finset ι) {h : ι}
    (hh : (univ.filter fun i => h < i).card < T.card) : remainderBase x₀ y T h = x₀ h := by
  unfold remainderBase
  exact mixConfig_apply_of_notMem x₀ y (sitesBefore_notMem_of_few_after _ T hh)

/-- **Hosts that are last have few sites after them.**  If the order puts the sites of `Hs` last
(every site after a site of `Hs` belongs to `Hs`) and `Hs` has at most `m` sites, fewer than `m`
sites are strictly after each site of `Hs`. -/
theorem card_after_lt_of_hosts_last [Fintype ι] [LinearOrder ι] {Hs : Finset ι} {m : ℕ}
    (hcard : Hs.card ≤ m) (hlast : ∀ h ∈ Hs, ∀ i, h < i → i ∈ Hs) {h : ι} (hh : h ∈ Hs) :
    (univ.filter fun i => h < i).card < m := by
  have hsub : (univ.filter fun i => h < i) ⊆ Hs.erase h := by
    intro i hi
    have hlt : h < i := (Finset.mem_filter.mp hi).2
    exact Finset.mem_erase.mpr ⟨ne_of_gt hlt, hlast h hh i hlt⟩
  have h1 := Finset.card_le_card hsub
  rw [Finset.card_erase_of_mem hh] at h1
  have hpos : 0 < Hs.card := Finset.card_pos.mpr ⟨h, hh⟩
  omega

/-! ### Linearity -/

/-- The mixed difference of a finite sum of functions is the sum of the mixed differences. -/
theorem mixedDiff_finset_sum [DecidableEq ι] {κ : Type*} (terms : Finset κ)
    (F : κ → (∀ i, σ i) → ℝ) (x : ∀ i, σ i) (T : Finset ι) (b : ∀ i, σ i) :
    mixedDiff (fun z => ∑ τ ∈ terms, F τ z) x T b = ∑ τ ∈ terms, mixedDiff (F τ) x T b := by
  unfold mixedDiff
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun U _ => ?_
  rw [Finset.mul_sum]

/-- The anchored interpolant of a finite sum of functions is the sum of the anchored
interpolants. -/
theorem anchoredInterp_finset_sum [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ) (x₀ y : ∀ i, σ i) :
    anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y =
      ∑ τ ∈ terms, anchoredInterp m (F τ) x₀ y := by
  unfold anchoredInterp
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun T _ => mixedDiff_finset_sum terms F x₀ T y

/-! ### Every term in its own order -/

/-- **Remainder identity, every term in its own order.**  Let the function be a finite sum of
terms `F τ`, `τ ∈ terms`, and give every term a linear order `ord τ` of the sites.  The error of
the anchored interpolant of order `m - 1` of the sum at `y` is the sum, over the terms `τ` and the
`m`-subsets `T` of the changed sites, of the mixed difference of `F τ` over `T` at the base point
`remainderBase x₀ y T` of the order `ord τ`: the changed sites that precede every site of `T` in
the order of `τ` carry the states of `y`, all other sites those of the reference. -/
theorem anchored_remainder_identity_orders [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ) (ord : κ → LinearOrder ι)
    (x₀ y : ∀ i, σ i) :
    (∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y =
      ∑ τ ∈ terms, ∑ T ∈ (supp x₀ y).powersetCard m,
        mixedDiff (F τ) (@remainderBase ι σ _ _ (ord τ) _ x₀ y T) T y := by
  rw [anchoredInterp_finset_sum, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun τ _ =>
    @anchored_remainder_identity ι σ _ _ (ord τ) _ m (F τ) x₀ y

/-- **Remainder bound with host-anchored constants.**  Let every term `τ` have a set `H τ` of
hosts, and let fewer than `m` sites be strictly after each host of `τ` in the order `ord τ` (this
is the case if the order of `τ` puts its at most `m` hosts last, `card_after_lt_of_hosts_last`).
Then it suffices to bound the mixed differences of `F τ` over the `m`-subsets `T` at the base
points that agree with the reference on `T` and at every host of `τ` outside `T`: the constants
need a maximum only over base points in which the hosts outside `T` sit at the reference. -/
theorem anchored_remainder_bound_orders [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ) (ord : κ → LinearOrder ι)
    (H : κ → Finset ι) (c : κ → Finset ι → ℝ) (x₀ y : ∀ i, σ i)
    (hH : ∀ τ ∈ terms, ∀ h ∈ H τ, (univ.filter fun i => (ord τ).lt h i).card < m)
    (hc : ∀ τ ∈ terms, ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      (∀ h ∈ H τ, h ∉ T → z h = x₀ h) → |mixedDiff (F τ) z T y| ≤ c τ T) :
    |(∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y| ≤
      ∑ τ ∈ terms, ∑ T ∈ (supp x₀ y).powersetCard m, c τ T := by
  rw [anchored_remainder_identity_orders m terms F ord x₀ y]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun τ hτ => ?_)
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun T hT => ?_)
  have hTm : T.card = m := (Finset.mem_powersetCard.mp hT).2
  refine hc τ hτ T hTm _ (fun t ht => ?_) (fun h hh _ => ?_)
  · exact @remainderBase_on ι σ _ _ (ord τ) _ x₀ y T t ht
  · exact @remainderBase_host_anchor ι σ _ _ (ord τ) _ x₀ y T h
      (lt_of_lt_of_eq (hH τ hτ h hh) hTm.symm)

/-! ### Terms with at most `m` hosts -/

/-- **Every set of sites can be put last.**  For every set `Hs` of sites of a finite type some
linear order of the sites has all the sites after a site of `Hs` in `Hs`. -/
theorem exists_linearOrder_hosts_last [Fintype ι] (Hs : Finset ι) :
    ∃ o : LinearOrder ι, ∀ h ∈ Hs, ∀ i, o.lt h i → i ∈ Hs := by
  classical
  let e := Fintype.equivFin ι
  let f : ι → ℕ := fun i => (if i ∈ Hs then Fintype.card ι else 0) + (e i : ℕ)
  have hf : Function.Injective f := by
    intro i j hij
    have hi := (e i).isLt
    have hj := (e j).isLt
    simp only [f] at hij
    apply e.injective
    apply Fin.ext
    split_ifs at hij <;> omega
  refine ⟨LinearOrder.lift' f hf, fun h hh i hlt => ?_⟩
  have hlt' : f h < f i := hlt
  by_contra hi
  have hi' := (e i).isLt
  simp only [f, if_pos hh, if_neg hi] at hlt'
  omega

/-- A set of at most `m` sites can be put last, and then fewer than `m` sites are strictly after
each of its sites: the hypothesis of `anchored_remainder_bound_orders` on the order of a term
can be met as soon as the term has at most `m` hosts. -/
theorem exists_linearOrder_few_after [Fintype ι] {Hs : Finset ι} {m : ℕ} (hcard : Hs.card ≤ m) :
    ∃ o : LinearOrder ι, ∀ h ∈ Hs, (univ.filter fun i => o.lt h i).card < m := by
  obtain ⟨o, ho⟩ := exists_linearOrder_hosts_last Hs
  exact ⟨o, fun h hh => @card_after_lt_of_hosts_last ι _ o Hs m hcard ho h hh⟩

/-- **Remainder bound for terms with at most `m` hosts.**  If every term `τ` has at most `m`
hosts, the remainder of the sum is bounded by the host-anchored constants: constants `c τ T` that
bound the mixed differences of `F τ` over `T` at the base points that agree with the reference on
`T` and at the hosts of `τ` outside `T`.  No order appears in the statement; the proof puts the
hosts of every term last (`exists_linearOrder_few_after`) and applies
`anchored_remainder_bound_orders`.  By `term_orders_sharp` the bound `m` on the number of hosts
cannot be replaced by `m + 1`. -/
theorem anchored_remainder_bound_hosts [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)]
    {κ : Type*} (m : ℕ) (terms : Finset κ) (F : κ → (∀ i, σ i) → ℝ) (H : κ → Finset ι)
    (c : κ → Finset ι → ℝ) (x₀ y : ∀ i, σ i) (hH : ∀ τ ∈ terms, (H τ).card ≤ m)
    (hc : ∀ τ ∈ terms, ∀ T : Finset ι, T.card = m → ∀ z : ∀ i, σ i, (∀ t ∈ T, z t = x₀ t) →
      (∀ h ∈ H τ, h ∉ T → z h = x₀ h) → |mixedDiff (F τ) z T y| ≤ c τ T) :
    |(∑ τ ∈ terms, F τ y) - anchoredInterp m (fun x => ∑ τ ∈ terms, F τ x) x₀ y| ≤
      ∑ τ ∈ terms, ∑ T ∈ (supp x₀ y).powersetCard m, c τ T := by
  have hex : ∀ τ, ∃ o : LinearOrder ι, τ ∈ terms →
      ∀ h ∈ H τ, (univ.filter fun i => o.lt h i).card < m := by
    intro τ
    by_cases hτ : τ ∈ terms
    · obtain ⟨o, ho⟩ := exists_linearOrder_few_after (hH τ hτ)
      exact ⟨o, fun _ => ho⟩
    · obtain ⟨o, -⟩ := exists_linearOrder_hosts_last (∅ : Finset ι)
      exact ⟨o, fun h => absurd h hτ⟩
  choose ord hord using hex
  exact anchored_remainder_bound_orders m terms F ord H c x₀ y hord hc

/-! ### Sharpness: `m + 1` hosts are too many

Three binary sites, the reference `(0, 0, 0)`, the configuration `(1, 1, 1)`, the order `m = 2`
and a single term, the triple coupling `tripleResidual` of `HigherOrderEnvelope.lean`
(`1` if all three sites are in the state `1`, else `0`), with all three sites as hosts. -/

/-- The triple coupling vanishes as soon as one site is in the state `0`. -/
theorem tripleResidual_eq_zero_of_site {z : Config 3 2} {h : Fin 3} (hz : z h = 0) :
    tripleResidual z = 0 := by
  unfold tripleResidual
  rw [if_neg]
  rintro ⟨h0, h1, h2⟩
  have h1' : z h = 1 := by
    fin_cases h
    · exact h0
    · exact h1
    · exact h2
  rw [hz] at h1'
  exact absurd h1' (by decide)

/-- **Sharpness: a term with `m + 1` hosts.**  For the triple coupling on three binary sites with
all three sites as hosts, the reference `(0, 0, 0)`, the configuration `(1, 1, 1)` and `m = 2`:
(i) the constants `0` satisfy the host-anchored hypothesis of `anchored_remainder_bound_orders`
and of `anchored_remainder_bound_hosts` — the mixed difference over a pair `T` vanishes at every
base point that agrees with the reference on `T` and at the host outside `T`, because the third
site is in the state `0` in every configuration that enters it; (ii) the remainder of order two is
`1`.  So the bound `|remainder| ≤ 0` of these theorems fails for a term with `m + 1 = 3` hosts. -/
theorem term_orders_sharp :
    (∀ T : Finset (Fin 3), T.card = 2 → ∀ z : Config 3 2, (∀ t ∈ T, z t = 0) →
        (∀ h ∈ (univ : Finset (Fin 3)), h ∉ T → z h = 0) →
        |mixedDiff tripleResidual z T (fun _ => 1)| ≤ 0) ∧
      tripleResidual (fun _ => 1) - anchoredInterp 2 tripleResidual (fun _ => 0) (fun _ => 1) =
        1 := by
  have h3 : 2 < (univ : Finset (Fin 3)).card := by simp
  constructor
  · intro T hT z _ hz
    obtain ⟨h, -, hhT⟩ : ∃ h ∈ (univ : Finset (Fin 3)), h ∉ T :=
      Finset.exists_mem_notMem_of_card_lt_card (hT.trans_lt h3)
    have h0 : mixedDiff tripleResidual z T (fun _ => 1) = 0 := by
      unfold mixedDiff
      refine Finset.sum_eq_zero fun U hU => ?_
      have hhU : h ∉ U := fun hmem => hhT (Finset.mem_powerset.mp hU hmem)
      rw [tripleResidual_eq_zero_of_site (h := h), mul_zero]
      rw [mixConfig_apply_of_notMem z _ hhU]
      exact hz h (Finset.mem_univ h) hhT
    rw [h0, abs_zero]
  · have hv : anchoredInterp 2 tripleResidual (fun _ => 0) (fun _ => 1) = 0 := by
      refine anchoredInterp_eq_zero_of_vanish 2 tripleResidual (fun _ => 0) (fun z hz => ?_) _
      obtain ⟨h, -, hh⟩ : ∃ h ∈ (univ : Finset (Fin 3)), h ∉ supp (fun _ => 0) z :=
        Finset.exists_mem_notMem_of_card_lt_card (hz.trans h3)
      refine tripleResidual_eq_zero_of_site (h := h) ?_
      by_contra hne
      exact hh (mem_supp.mpr hne)
    rw [hv, sub_zero]
    simp [tripleResidual]

/-- **With `m + 1` hosts a host leaves the anchor, whatever the order.**  For the witness of
`term_orders_sharp` and every linear order of the three sites there are a pair `T` and a host
outside `T` at which the base point of the remainder term of `T` is not the reference.  (If it
were the reference at all of them, the remainder identity and the first statement of
`term_orders_sharp` would give `1 = 0`.) -/
theorem term_orders_sharp_host_moves (o : LinearOrder (Fin 3)) :
    ∃ T : Finset (Fin 3), T.card = 2 ∧ ∃ h, h ∉ T ∧
      @remainderBase (Fin 3) (fun _ => Fin 2) _ _ o _ (fun _ => 0) (fun _ => 1) T h ≠ 0 := by
  by_contra hne
  have h := @anchored_remainder_identity (Fin 3) (fun _ => Fin 2) _ _ o _ 2 tripleResidual
    (fun _ => 0) (fun _ => 1)
  rw [term_orders_sharp.2, Finset.sum_eq_zero] at h
  · exact one_ne_zero h
  · intro T hT
    have hTc : T.card = 2 := (Finset.mem_powersetCard.mp hT).2
    refine abs_nonpos_iff.mp (term_orders_sharp.1 T hTc _
      (fun t ht => @remainderBase_on (Fin 3) (fun _ => Fin 2) _ _ o _ _ _ T t ht)
      (fun h _ hhT => ?_))
    by_contra hmove
    exact hne ⟨T, hTc, h, hhT, hmove⟩

/-! ### The anchored split of a pair table -/

section AnchoredSplit

variable {X Y : Type*}

/-- The anchor column of the table `P`: `A x = P x b`. -/
def anchoredSplitA (P : X → Y → ℝ) (b : Y) (x : X) : ℝ := P x b

/-- The anchor row of the table `P`, centred at the anchor: `B y = P a y - P a b`. -/
def anchoredSplitB (P : X → Y → ℝ) (a : X) (b : Y) (y : Y) : ℝ := P a y - P a b

/-- The remainder of the anchored split: `D x y = P x y - A x - B y`. -/
def anchoredSplitD (P : X → Y → ℝ) (a : X) (b : Y) (x : X) (y : Y) : ℝ :=
  P x y - anchoredSplitA P b x - anchoredSplitB P a b y

/-- The remainder of the anchored split vanishes on the anchor row. -/
theorem anchoredSplit_row (P : X → Y → ℝ) (a : X) (b : Y) (y : Y) :
    anchoredSplitD P a b a y = 0 := by
  unfold anchoredSplitD anchoredSplitA anchoredSplitB
  ring

/-- The remainder of the anchored split vanishes on the anchor column. -/
theorem anchoredSplit_col (P : X → Y → ℝ) (a : X) (b : Y) (x : X) :
    anchoredSplitD P a b x b = 0 := by
  unfold anchoredSplitD anchoredSplitA anchoredSplitB
  ring

/-- **Sandwich of a pair table by sums of one-site functions.**  If `lo x ≤ D x y ≤ hi x` for
every `y`, then `A x + B y + lo x ≤ P x y ≤ A x + B y + hi x` for every `y`: the table lies
between two sums of a function of `x` and a function of `y`. -/
theorem anchoredSplit_sandwich (P : X → Y → ℝ) (a : X) (b : Y) (lo hi : X → ℝ) (x : X)
    (h : ∀ y, lo x ≤ anchoredSplitD P a b x y ∧ anchoredSplitD P a b x y ≤ hi x) (y : Y) :
    anchoredSplitA P b x + anchoredSplitB P a b y + lo x ≤ P x y ∧
      P x y ≤ anchoredSplitA P b x + anchoredSplitB P a b y + hi x := by
  have h1 := h y
  unfold anchoredSplitD at h1
  exact ⟨by linarith [h1.1], by linarith [h1.2]⟩

/-- The least remainder of the row `x`: `lo x = min_y D x y`. -/
noncomputable def anchoredSplitLo [Fintype Y] [Nonempty Y] (P : X → Y → ℝ) (a : X) (b : Y)
    (x : X) : ℝ :=
  univ.inf' univ_nonempty (anchoredSplitD P a b x)

/-- The greatest remainder of the row `x`: `hi x = max_y D x y`. -/
noncomputable def anchoredSplitHi [Fintype Y] [Nonempty Y] (P : X → Y → ℝ) (a : X) (b : Y)
    (x : X) : ℝ :=
  univ.sup' univ_nonempty (anchoredSplitD P a b x)

/-- The row minimum and the row maximum enclose the remainder. -/
theorem anchoredSplit_extrema [Fintype Y] [Nonempty Y] (P : X → Y → ℝ) (a : X) (b : Y) (x : X)
    (y : Y) : anchoredSplitLo P a b x ≤ anchoredSplitD P a b x y ∧
      anchoredSplitD P a b x y ≤ anchoredSplitHi P a b x :=
  ⟨Finset.inf'_le _ (Finset.mem_univ y), Finset.le_sup' _ (Finset.mem_univ y)⟩

/-- **Sandwich with the row extrema.**  On a finite non-empty `Y` the row minimum and the row
maximum of the remainder work: `A x + B y + min D x ≤ P x y ≤ A x + B y + max D x`. -/
theorem anchoredSplit_sandwich_extrema [Fintype Y] [Nonempty Y] (P : X → Y → ℝ) (a : X) (b : Y)
    (x : X) (y : Y) :
    anchoredSplitA P b x + anchoredSplitB P a b y + anchoredSplitLo P a b x ≤ P x y ∧
      P x y ≤ anchoredSplitA P b x + anchoredSplitB P a b y + anchoredSplitHi P a b x :=
  anchoredSplit_sandwich P a b (anchoredSplitLo P a b) (anchoredSplitHi P a b) x
    (anchoredSplit_extrema P a b x) y

/-- **The split is exact on the anchor row.**  The row minimum and the row maximum of the
remainder vanish at `x = a`, so both sides of `anchoredSplit_sandwich_extrema` are `P a y`. -/
theorem anchoredSplit_exact_at_anchor [Fintype Y] [Nonempty Y] (P : X → Y → ℝ) (a : X) (b : Y) :
    anchoredSplitLo P a b a = 0 ∧ anchoredSplitHi P a b a = 0 := by
  have h : anchoredSplitD P a b a = fun _ => 0 := funext fun y => anchoredSplit_row P a b y
  unfold anchoredSplitLo anchoredSplitHi
  rw [h]
  exact ⟨Finset.inf'_const _ 0, Finset.sup'_const _ 0⟩

end AnchoredSplit

end MetricChain
