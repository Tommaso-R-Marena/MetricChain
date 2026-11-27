> **Repository note (added by the coordinator at integration).**  The file is
> `proofs/Frontiers/GamePair.lean` in the repository (the trailing `#print axioms` lines moved to
> `proofs/AxiomAudit.lean`; nothing else changed); the statements are theory report §11.21
> (Theorem 11.66).  The coordinator compiled it, read the definitions and the main statements
> against the brief, and found them faithful.

# Workstream M — report: every game function yields a `HintPair`

**Status: complete.**  Parts 1, 2 and 3 of the brief are machine-checked, with one stated
deviation (the form of one hypothesis in Part 2, §2).  Beyond the brief the file also proves the
lower barrier, so the exact recursion *converges* to the hinted exponent for every game function
(§1.3).  Nothing of the brief is missing.

**Deliverable.**  `scratchpad/ws/M/GamePair.lean` — 880 lines, 84 declarations (77 theorems,
5 definitions, 2 structures), namespace `MetricChain.GamePair`, one import
(`proofs.Frontiers.BoundedAccuracy`).  No `sorry`, no `admit`, no `axiom`, no `set_option`, no
`native_decide`; zero errors, zero warnings; every one of the 84 declarations depends only on
`propext`, `Classical.choice`, `Quot.sound` (checked for all of them, not only for the headline
ones).  Compile time about 10 s.  The repository head moved during the work (four commits by
others, last seen `2c33726`, all in `docs/`, `experiments/`, `scripts/`); `proofs/`, the lakefile,
the manifest and the toolchain are identical to those of the brief's commit `7f9b8b6`
(`git diff --stat 7f9b8b6 HEAD -- proofs lakefile.lean lake-manifest.json lean-toolchain` is
empty), so the file was checked against the sources the brief names.  SHA-256 of the file as
compiled: `2f8a17ac82f7bacb3e4dc7aca1c55fb533c3a86e2e855ffc353ecb8c57bb95cf`.

## 1. The statements exactly as proved

All signatures below are cut out of the file by a script (`make_report.py`), so they are verbatim.
`open MetricChain.HintRecursion MetricChain.BoundedAccuracy Set` is in force; `exactRec`,
`Rstep`, `StepLE`, `HintPair`, `gaussNa`, `gaussHint` are the objects of the repository.  A
theorem shown without a namespace prefix and with first argument `hs : HintShape θh E ec` (resp.
`hF : GameFunction F E L`) is declared inside `namespace HintShape` (resp. `GameFunction`) under
`variable {θh : ℝ → ℝ} {E ec : ℝ}` (resp. `variable {F : ℝ → ℝ} {E L : ℝ}`); the full names are in §4.

### 1.1 Definitions

```lean
structure HintShape (θh : ℝ → ℝ) (E ec : ℝ) : Prop where
  convex : ConvexOn ℝ Set.univ θh
  anti : Antitone θh
  shift_mono : Monotone (fun e => e + θh e)        -- slopes at least −1
  nonneg : ∀ e, 0 ≤ θh e
  zero_iff : ∀ e, θh e = 0 ↔ E ≤ e
  E_pos : 0 < E
  ec_neg : ec < 0
  ec_zero : ec + θh ec = 0
  pos_after : ∀ e, ec < e → 0 < e + θh e

structure GameFunction (F : ℝ → ℝ) (E L : ℝ) : Prop where
  cont : ContinuousOn F (Set.Icc 0 1)
  zero0 : F 0 = 0
  zero1 : F 1 = 0
  le_lin : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t ≤ L * (1 - t)
  le_E : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t ≤ E * t
  E_sharp : ∀ e, e < E → ∃ t ∈ Set.Ioc (0 : ℝ) 1, e * t < F t
  E_pos : 0 < E

noncomputable def shiftInv (θh : ℝ → ℝ) (x : ℝ) : ℝ := sSup {e | e + θh e ≤ x}
noncomputable def partner (θh : ℝ → ℝ) (x : ℝ) : ℝ := θh (shiftInv θh x)
noncomputable def hinted (F : ℝ → ℝ) (e : ℝ) : ℝ := sSup ((fun t => F t - t * e) '' Set.Icc 0 1)
noncomputable def critical (F : ℝ → ℝ) : ℝ := shiftInv (hinted F) 0
def toyGame (t : ℝ) : ℝ := t * (1 - t)
```

`HintShape`, `GameFunction` and `hinted` are literal transcriptions of the brief (same field
names, same order, same types).  `shiftInv`, `partner`, `critical`, `toyGame` are new: the brief
asked for the existence of `θna` and of `ec`; the file names them (`partner θh` is `θna`,
`critical F` is `e_c`), which is stronger and is what the later statements need.

### 1.2 The theorems the brief asks for

```lean
-- Part 1
theorem HintShape.exists_pair {θh : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec) :
    ∃ θna : ℝ → ℝ, HintPair θna θh (θh ec) (θh 0) E ∧
      (∀ e, ec ≤ e → θna (e + θh e) = θh e) ∧
      (∀ x, 0 < x → 0 ≤ θna x) ∧ (∀ x y, 0 < x → x ≤ y → θna y ≤ θna x)

theorem HintShape.exactRec_reaches {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec ≤ e → θna (e + θh e) = θh e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < θh g + η

-- Part 2
theorem GameFunction.hintShape {F : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L) :
    ∃ ec, HintShape (hinted F) E ec

theorem GameFunction.exactRec_reaches {F θna : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L)
    (hfun : ∀ e, 0 < e + hinted F e → θna (e + hinted F e) = hinted F e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < hinted F g + η

-- Part 3
theorem toyGame_gameFunction : GameFunction toyGame 1 1

theorem hinted_toyGame {e : ℝ} (h1 : -1 ≤ e) (h2 : e ≤ 1) :
    hinted toyGame e = ((1 - e) / 2) ^ 2

theorem hinted_toyGame_eq_gaussHint {e : ℝ} (h1 : -1 ≤ e) (h2 : e ≤ 1) :
    hinted toyGame e = gaussHint e
```

The first two and `GameFunction.hintShape` are character for character the statements of the
brief (binder names and order included).  `GameFunction.exactRec_reaches` is the statement of
the brief with the hypothesis `hfun` in the form chosen in §2.  The congruence lemma and the
uniqueness statement that the brief announces as needed:

```lean
theorem exactRec_congr {θna θna' : ℝ → ℝ} (hθ : ∀ x, 0 < x → θna x = θna' x) (k : ℕ) :
    ∀ g, 0 < g → exactRec θna k g = exactRec θna' k g

theorem eq_partner (hs : HintShape θh E ec) {θna : ℝ → ℝ}
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) {x : ℝ} (hx : 0 < x) :
    θna x = partner θh x
```

### 1.3 Beyond the brief (same file, same standards)

```lean
-- the pair, explicitly
theorem pair (hs : HintShape θh E ec) : HintPair (partner θh) θh (θh ec) (θh 0) E

-- the functional equation only where the recursion can see it (implies `exactRec_reaches`)
theorem HintShape.exactRec_reaches' {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e)
    {g : ℝ} (hg : 0 < g) (hgE : g < E) {η : ℝ} (hη : 0 < η) :
    ∃ k, exactRec θna k g < θh g + η

-- the hinted exponent is a lower barrier, a fixed point, and the limit
theorem superSolution (hs : HintShape θh E ec) : StepLE (partner θh) θh θh

theorem HintShape.le_exactRec {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) (k : ℕ) {g : ℝ} (hg : 0 < g) :
    θh g ≤ exactRec θna k g

theorem HintShape.Rstep_hint {θh : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec) {g : ℝ}
    (hg : 0 < g) (hgE : g < E) : Rstep (partner θh) θh g = θh g

theorem HintShape.exactRec_tendsto {θh θna : ℝ → ℝ} {E ec : ℝ} (hs : HintShape θh E ec)
    (hfun : ∀ e, ec < e → θna (e + θh e) = θh e) {g : ℝ} (hg : 0 < g) :
    Filter.Tendsto (fun k => exactRec θna k g) Filter.atTop (nhds (θh g))

-- fewer hypotheses
theorem strictMonoOn_shift_of_convexOn {θh : ℝ → ℝ} {ec : ℝ} (hc : ConvexOn ℝ univ θh)
    (hz : ec + θh ec = 0) (hpos : ∀ e, ec < e → 0 < e + θh e) :
    StrictMonoOn (fun e => e + θh e) (Ici ec)

theorem antitone_of_convexOn_of_zero_iff {θh : ℝ → ℝ} {E : ℝ} (hc : ConvexOn ℝ univ θh)
    (hnn : ∀ e, 0 ≤ θh e) (hz : ∀ e, θh e = 0 ↔ E ≤ e) : Antitone θh

theorem HintShape.of_convex {θh : ℝ → ℝ} {E ec : ℝ} (hc : ConvexOn ℝ univ θh)
    (hm : Monotone fun e => e + θh e) (hnn : ∀ e, 0 ≤ θh e) (hz : ∀ e, θh e = 0 ↔ E ≤ e)
    (hE : 0 < E) (hec : ec + θh ec = 0) (hpos : ∀ e, ec < e → 0 < e + θh e) :
    HintShape θh E ec

-- strict separation, and the partner as a minimum
theorem lt_partner (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) (hxE : x < E) :
    θh x < partner θh x

theorem partner_isLeast (hs : HintShape θh E ec) {x : ℝ} (hx : 0 ≤ x) :
    IsLeast (θh '' {e | e + θh e ≤ x}) (partner θh x)

-- game functions
theorem hintShape_critical (hF : GameFunction F E L) :
    HintShape (hinted F) E (critical F)

theorem GameFunction.pair {F : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L) :
    HintPair (partner (hinted F)) (hinted F) (hinted F (critical F)) (hinted F 0) E

theorem GameFunction.exactRec_tendsto {F θna : ℝ → ℝ} {E L : ℝ} (hF : GameFunction F E L)
    (hfun : ∀ e, 0 < e + hinted F e → θna (e + hinted F e) = hinted F e) {g : ℝ} (hg : 0 < g) :
    Filter.Tendsto (fun k => exactRec θna k g) Filter.atTop (nhds (hinted F g))

theorem not_forall_shift_eq (hF : GameFunction F E L) (θna : ℝ → ℝ) :
    ¬ ∀ e, 0 ≤ e + hinted F e → θna (e + hinted F e) = hinted F e

theorem critical_eq_neg_L (hF : GameFunction F E L)
    (hL : ∀ l, l < L → ∃ t ∈ Ico (0 : ℝ) 1, l * (1 - t) < F t) : critical F = -L

theorem hinted_attained (hF : GameFunction F E L) (e : ℝ) :
    ∃ t ∈ Icc (0 : ℝ) 1, hinted F e = F t - t * e

-- the witness, identified with the toy pair of `HintRecursion.lean`
theorem toyGame_hintShape : HintShape (hinted toyGame) 1 (-1)

theorem critical_toyGame : critical toyGame = -1

theorem hinted_toyGame_of_one_le {e : ℝ} (h : 1 ≤ e) : hinted toyGame e = 0

theorem hinted_toyGame_of_le_neg_one {e : ℝ} (h : e ≤ -1) : hinted toyGame e = -e

theorem partner_toyGame {x : ℝ} (hx : 0 < x) : partner (hinted toyGame) x = gaussNa x

theorem toyGame_pair : HintPair (partner (hinted toyGame)) (hinted toyGame) 1 (1 / 4) 1

theorem gauss_exactRec_tendsto {g : ℝ} (hg : 0 < g) (hg1 : g ≤ 1) :
    Filter.Tendsto (fun k => exactRec gaussNa k g) Filter.atTop (nhds (gaussHint g))
```

`gauss_exactRec_tendsto` is the whole chain applied to the witness with every hypothesis
discharged, in terms of objects that existed before this workstream: the exact recursion built
on `gaussNa` converges to `gaussHint` on `(0, 1]`.  It is the non-vacuity statement for the final
theorems (`toyGame_hintShape` for Part 1, `toyGame_gameFunction` for Part 2).

## 2. Deviations from the brief

**D1 (the only deviation) — the hypothesis `hfun` of `GameFunction.exactRec_reaches`.**  The brief
sketches `(hfun : ∀ e, 0 ≤ e + hinted F e → ... )` and asks for "a clean form".  The form proved is

    hfun : ∀ e, 0 < e + hinted F e → θna (e + hinted F e) = hinted F e        (strict)

*Reason.*  With `≤` the hypothesis is unsatisfiable, so the theorem would be vacuous: for a game
function the shift `S(e) = e + R(e)` is nonnegative on the whole line (`neg_le_hinted`: take
`t = 1`) and vanishes on `(-∞, e_c]`, where `R(e) = -e` is not constant
(`GameFunction.shift_eq_zero`); the equation at `e_c` and at `e_c - 1` would give
`θna 0 = -e_c` and `θna 0 = 1 - e_c`.  This is machine-checked:
`GameFunction.not_forall_shift_eq : ¬ ∀ e, 0 ≤ e + hinted F e → θna (e + hinted F e) = hinted F e`
for every `θna`.  The strict form is satisfiable — `partner (hinted F)` satisfies it
(`GameFunction.partner_shift`) — it is equivalent to "the functional equation for `e > e_c`", it
says nothing about `θna` on `(-∞, 0]`, which the recursion at `g > 0` never evaluates
(`exactRec_congr`), and it matches the paper definition (`F_REPORT.md`: `θ_na(x) = R^max(S⁻¹(x))` for
`x > 0`, `a = θ_na(0+)`).  The form of Part 1 (`∀ e, critical F ≤ e → …`, which additionally fixes `θna 0 = a`) is available as
`hF.hintShape_critical.exactRec_reaches`; it is a stronger hypothesis, hence a weaker theorem.

**No other deviation.**  `HintShape`, `GameFunction`, `hinted`, `HintShape.exists_pair`,
`HintShape.exactRec_reaches`, `GameFunction.hintShape` are verbatim.  No hypothesis was added
anywhere (no `0 ≤ L`, no `ContinuousOn` in `HintShape`, no assumed `e_c`); no conclusion was
weakened.  Part 3 uses a named definition `toyGame t = t * (1 - t)` instead of a lambda.

**Additions that are not deviations** (§1.3): names for the partner and the critical accuracy;
`HintShape.exactRec_reaches'` (hypothesis on `(ec, ∞)` only — weaker hypothesis, same conclusion);
the lower barrier, the fixed point and the convergence; `HintShape.of_convex`; the
identification of the witness with `gaussNa`, `gaussHint`, `gaussPair`.

## 3. How the proof goes

*Part 1.*  `S(e) = e + θh e`.  (i) `θh` is `1`-Lipschitz because it is nonincreasing and `S` is
nondecreasing (`lipschitz_of_antitone_of_shift_monotone`; no convexity).  (ii) `S` is strictly
increasing on `[ec, ∞)`: for `ec ≤ x < y` write `x = a·ec + (1-a)·y`, `a > 0`; convexity gives
`S(x) ≤ a S(ec) + (1-a) S(y) = (1-a) S(y) < S(y)` since `S(y) > 0`
(`strictMonoOn_shift_of_convexOn`).  (iii) `S` maps `[ec, ∞)` onto `[0, ∞)` by the intermediate
value theorem on `[ec, x]` (`S(ec) = 0 ≤ x ≤ S(x)`).  (iv) `shiftInv θh x = sSup {e | S(e) ≤ x}`
returns `e` at `S(e)` for `e ≥ ec` (`shiftInv_shift`), hence inverts `S` on `[0, ∞)`
(`shiftInv_spec`), is monotone there, and is continuous at every `x > 0` by Mathlib's
`continuousAt_of_monotoneOn_of_image_mem_nhds` (monotone on `(0, ∞)`, and its image of `(0, ∞)`
contains `(ec, ∞)`, a neighbourhood of `shiftInv θh x > ec`) — no subtypes, no order
isomorphism, no ε–δ.  (v) The nine fields of `HintPair` for `partner θh = θh ∘ shiftInv θh` are
then one line each; `hint_lower` holds with `L = 1` (`S(0) ≤ S(e)`).  (vi) `exactRec_congr` by
induction on the level (the admissible set of `Rstep` evaluates `θna` and the inner function
only at `(g-β)/φ > 0` and `γ/(1-φ) > 0`), `eq_partner` from `shiftInv_spec`, and then
`exactRec_reaches_hint_of_pair` of `BoundedAccuracy.lean`.

*Lower barrier.*  `StepLE (partner θh) θh θh`: take `γ = max(β, μ)` with
`μ = φ·θna((g-β)/φ) = φ·θh(eo)`, `eo = S⁻¹((g-β)/φ)`; the bracket is
`φ θh(eo) + (1-φ) θh(ei) ≥ θh(φ eo + (1-φ) ei)` (convexity), `ei = γ/(1-φ)`, and
`φ eo + (1-φ) ei = φ eo + γ ≤ φ (eo + θh eo) + β = g`, so the value is `≥ θh g` (`θh` nonincreasing).
With `admissible_subset_of_le` this gives `θh ≤ R[T]` whenever `θh ≤ T`, hence `θh ≤ exactRec k`
for all `k`, hence convergence; for `g ≥ E` every level is `0 = θh g`.

*Part 2.*  With `R = hinted F`: the set whose supremum is taken is nonempty (`t = 0`) and bounded
above by `max 0 (E - e)` (`le_E`), so `le_csSup`/`csSup_le` apply and no compactness is needed.
Convex (supremum of affine functions), nonincreasing (`t ≥ 0`), `S` nondecreasing (`t ≤ 1`),
`R ≥ 0` (`t = 0`), `R ≥ -e` (`t = 1`), `R = 0 ⟺ E ≤ e` (`le_E`; `E_sharp`).  The zero set
`{e | S(e) ≤ 0}` contains `-L` (`le_lin`), is bounded above by `0` and closed (`S` continuous), so
its supremum `critical F` belongs to it; `S(critical F) = 0`, `S > 0` afterwards by definition of
the supremum, and `critical F < 0` because `S(0) = R(0) > 0`.

*Part 3.*  `nlinarith`; the maximiser of `t(1-t) - te` is `t = (1-e)/2 ∈ [0, 1]` for `|e| ≤ 1`.
For `partner_toyGame` the preimage of `x ∈ (0, 1]` under the shift is `e = 2√x - 1`.

No lemma needed more than one approach; the three-strike rule was never invoked.

## 4. Declarations (84, in file order)

| line | kind | name (inside `MetricChain.GamePair`) |
|---|---|---|
| 78 | theorem | `admissible_subset_of_eqOn` |
| 89 | theorem | `admissible_congr` |
| 96 | theorem | `exactRec_congr` |
| 109 | theorem | `le_Rstep_of_superSolution` |
| 121 | theorem | `lipschitz_of_antitone_of_shift_monotone` |
| 133 | theorem | `antitone_of_convexOn_of_zero_iff` |
| 153 | theorem | `strictMonoOn_shift_of_convexOn` |
| 175 | structure | `HintShape` |
| 187 | def | `shiftInv` |
| 191 | def | `partner` |
| 194 | theorem | `HintShape.of_convex` |
| 218 | theorem | `HintShape.le_shift` |
| 222 | theorem | `HintShape.hint_pos` |
| 226 | theorem | `HintShape.lipschitz` |
| 229 | theorem | `HintShape.continuous` |
| 233 | theorem | `HintShape.shift_strictMonoOn` |
| 238 | theorem | `HintShape.lt_of_shift_pos` |
| 245 | theorem | `HintShape.exists_shift_eq` |
| 255 | theorem | `HintShape.shiftInv_shift` |
| 269 | theorem | `HintShape.shiftInv_spec` |
| 276 | theorem | `HintShape.shiftInv_zero` |
| 280 | theorem | `HintShape.lt_shiftInv` |
| 283 | theorem | `HintShape.shiftInv_le` |
| 287 | theorem | `HintShape.shiftInv_monotoneOn` |
| 299 | theorem | `HintShape.shiftInv_continuousAt` |
| 309 | theorem | `HintShape.partner_shift` |
| 314 | theorem | `HintShape.partner_nonneg` |
| 317 | theorem | `HintShape.partner_antitoneOn` |
| 321 | theorem | `HintShape.partner_le` |
| 325 | theorem | `HintShape.le_partner` |
| 329 | theorem | `HintShape.lt_partner` |
| 347 | theorem | `HintShape.partner_eq_sub` |
| 355 | theorem | `HintShape.partner_isLeast` |
| 361 | theorem | `HintShape.partner_continuousAt` |
| 366 | theorem | `HintShape.partner_eq_zero` |
| 373 | theorem | `HintShape.pair` |
| 389 | theorem | `HintShape.eq_partner` |
| 402 | theorem | `HintShape.superSolution` |
| 422 | theorem | `HintShape.le_exactRec_partner` |
| 439 | theorem | `HintShape.exists_pair` |
| 448 | theorem | `HintShape.exactRec_reaches'` |
| 459 | theorem | `HintShape.exactRec_reaches` |
| 467 | theorem | `HintShape.le_exactRec` |
| 475 | theorem | `HintShape.Rstep_hint` |
| 488 | theorem | `HintShape.exactRec_tendsto` |
| 515 | structure | `GameFunction` |
| 525 | def | `hinted` |
| 528 | def | `critical` |
| 531 | theorem | `hinted_le` |
| 541 | theorem | `GameFunction.sub_le_max` |
| 552 | theorem | `GameFunction.bddAbove` |
| 556 | theorem | `GameFunction.le_hinted` |
| 562 | theorem | `GameFunction.hinted_attained` |
| 567 | theorem | `GameFunction.hinted_nonneg` |
| 573 | theorem | `GameFunction.neg_le_hinted` |
| 578 | theorem | `GameFunction.hinted_le_max` |
| 582 | theorem | `GameFunction.hinted_convexOn` |
| 595 | theorem | `GameFunction.hinted_antitone` |
| 604 | theorem | `GameFunction.hinted_shift_monotone` |
| 617 | theorem | `GameFunction.hinted_eq_zero_iff` |
| 632 | theorem | `GameFunction.L_nonneg` |
| 638 | theorem | `GameFunction.hinted_neg_L_le` |
| 646 | theorem | `GameFunction.hintShape_critical` |
| 666 | theorem | `GameFunction.hinted_critical` |
| 670 | theorem | `GameFunction.neg_L_le_critical` |
| 679 | theorem | `GameFunction.critical_eq_neg_L` |
| 690 | theorem | `GameFunction.shift_eq_zero` |
| 697 | theorem | `GameFunction.partner_shift` |
| 704 | theorem | `GameFunction.not_forall_shift_eq` |
| 720 | theorem | `GameFunction.hintShape` |
| 726 | theorem | `GameFunction.pair` |
| 732 | theorem | `GameFunction.exactRec_reaches` |
| 741 | theorem | `GameFunction.exactRec_tendsto` |
| 751 | def | `toyGame` |
| 754 | theorem | `toyGame_gameFunction` |
| 769 | theorem | `hinted_toyGame` |
| 784 | theorem | `hinted_toyGame_eq_gaussHint` |
| 791 | theorem | `critical_toyGame` |
| 800 | theorem | `toyGame_hintShape` |
| 805 | theorem | `hinted_toyGame_of_one_le` |
| 809 | theorem | `hinted_toyGame_of_le_neg_one` |
| 814 | theorem | `partner_toyGame` |
| 840 | theorem | `toyGame_pair` |
| 853 | theorem | `gauss_exactRec_tendsto` |

## 5. Compile command and output

Command (the one of the brief, verbatim; run by `final_compile.sh` after the bounded wait for
other Lean processes):

    cd /home/user/MetricChain && export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH" && lake env lean <session scratch directory>/ws/M/GamePair.lean

Complete output (stdout and stderr; also in `compile_output.txt`):

```
'MetricChain.GamePair.exactRec_congr' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.exists_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.exactRec_reaches' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.superSolution' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.Rstep_hint' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.HintShape.exactRec_tendsto' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.hintShape_critical' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.hintShape' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.exactRec_reaches' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.exactRec_tendsto' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.GameFunction.not_forall_shift_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.toyGame_gameFunction' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.toyGame_hintShape' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.hinted_toyGame' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.partner_toyGame' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.toyGame_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'MetricChain.GamePair.gauss_exactRec_tendsto' depends on axioms: [propext, Classical.choice, Quot.sound]
exit code: 0
```

There is no other line: no error, no warning.  Lean `4.31.0` (commit `68218e876d2a`).

Further checks on the same file (scripts in the directory):

* `run_strict.sh` — with `-DautoImplicit=false -DrelaxedAutoImplicit=false`, the options of the
  repository's `lakefile.lean`, which `lake env lean` alone does not apply: the same 19 lines,
  exit 0 (run on the final file).
* `run_werror.sh` — additionally `-DwarningAsError=true`: the same 19 lines, exit 0 (run on the
  final file).
* `#lint` (Batteries/Mathlib, 16 linters) on a scratch copy of the final file: "Found 0 errors
  in 104 declarations (plus 14 automatically generated ones)".
* `#print axioms` for each of the 84 declarations on a scratch copy of the final file: all
  `[propext, Classical.choice, Quot.sound]`.
* Token scan: no `sorry`, `admit`, `axiom`, `native_decide`, `set_option`, `push_neg`, `unsafe`.
* No line longer than 100 characters.

Process note.  `lake build` was never run, nothing was run under `ulimit -v`, nothing was written
outside `scratchpad/ws/M/`, no state-changing git command was issued, no subagent was started.
Before every Lean run the script waits (at most two minutes) while `pgrep -f "lean "` finds a
process; on two runs the two minutes expired with another Lean process still running (the one
I identified was a foreign `lake env lean proofs/AxiomAudit.lean`) and, as the rule allows, my
run was started then.  Files under `docs/` of the repository changed while I worked; that was
not me (I issued no write and no state-changing git command there).

## 6. What is not proved

* **Nothing of the brief is missing.**
* **Not formalised (outside the brief):** that the exponent functions of the theory report are of
  this form.  The file contains no game function other than the witness: that the functions `F*`
  of §11.20 (or the game function of the uniform cube) satisfy `GameFunction`, that the hinted
  exponents are `max_{t ≤ 1} [F*(t) − te]`, and that `R ∘ S⁻¹` is the exponent of non-adaptive
  sampling remain paper theorems.  In particular `cubePair` is not re-derived from this file
  (`cubeHint` is given by a `KL` formula, not as a supremum over `t`, and outside `[0, ε*]` it is
  not the hinted exponent on the whole line that `HintShape` asks for).
* The convergence is pointwise in the accuracy rate and without a rate in the level.
* Junk values: `shiftInv θh x` and `partner θh x` for `x < 0` mean nothing (as `cubeNa u x` for
  `x < 0`); `partner θh 0 = θh ec = a`.  No statement depends on them.
* The supplementary variant (§7, O4) is evidence for an observation, not a deliverable.

## 7. Mathematical observations

**O1 — the functional equation must not be asked at the zeros of the shift** (D1 above;
machine-checked, `GameFunction.not_forall_shift_eq`).  On `{S > 0} = (e_c, ∞)` it determines `θna`
on `(0, ∞)` (`HintShape.eq_partner`), which is all the recursion sees (`exactRec_congr`).

**O2 — continuity of the game function is not used.**  The field `cont` enters one lemma only,
`GameFunction.hinted_attained` (the supremum is a maximum).  Convexity, the two slope bounds, the
zero set, the critical accuracy, the pair and the convergence hold for any function with the
other six properties; boundedness of the supremum comes from `le_E`.  Concavity of `F` is not
needed either.

**O3 — what `le_lin` does, and a formula for `a`.**  `le_lin` is used once: it puts `-L` into the
zero set of the shift, so `e_c` exists and `-L ≤ e_c` (`neg_L_le_critical`), i.e. `a = -e_c ≤ L`.
`0 ≤ L` is automatic (`L_nonneg`).  If `L` is sharp then `e_c = -L`
(`GameFunction.critical_eq_neg_L`), so

    a = θna(0+) = -e_c = sup_{0 ≤ t < 1} F(t)/(1 - t),      as      E = sup_{0 < t ≤ 1} F(t)/t :

the bound of the non-adaptive exponent and the threshold are the best linear bounds of the game
function at its two zeros (`= -F'(1)` and `F'(0)` when `F` is concave and differentiable there).
`le_lin` is also necessary (not machine-checked): for `F(t) = t√(1-t)`, which has every other
property with `E = 1`, the shift is positive on the whole line (at `t = 1 - s`:
`(1-s)√s + s·e > 0` for small `s`), there is no `e_c`, and `R ∘ S⁻¹` is unbounded near `0`, so
`na_le` fails.

**O4 — three of the nine fields of `HintShape` are not needed for Part 1.**
(a) `anti` and `ec_neg` follow from the other seven: `HintShape.of_convex` (machine-checked, in
the file; a convex nonnegative function that vanishes exactly on `[E, ∞)` is nonincreasing —
`antitone_of_convexOn_of_zero_iff`).
(b) The slope condition `shift_mono` is not needed either: on `[ec, ∞)` the shift is strictly
increasing by convexity, `ec_zero` and `pos_after` alone (`strictMonoOn_shift_of_convexOn`, in
the file), and before `ec` monotonicity is used only for convenience.  Machine-checked in the
*supplementary variant* `supplement/NoSlopeVariant.lean` (generated by
`supplement/make_variant.py`: the field is deleted, continuity is taken from convexity via
`ConvexOn.continuousOn`, `hint_mono`/`hint_lower` from the strict monotonicity); it compiles
with the same output, also with warnings as errors.  So **convex, nonnegative, zero exactly on
`[E, ∞)`, `E > 0`, `S(ec) = 0`, `S > 0` after `ec`** suffice for the pair, the lower barrier and
the convergence.  In the terms of the paper proof: the bound `t ≤ 1` is what makes the shift
vanish somewhere (existence of `e_c`); given `e_c`, slopes `≥ -1` on `[e_c, ∞)` are automatic.
The deliverable keeps the nine fields because the brief specifies them and Part 2 delivers all
nine; if the coordinator prefers the leaner structure, the variant is the patch.
(c) Convexity is used twice: for the strict monotonicity of the shift (without it the
functional equation can be inconsistent: two accuracies with the same shift and different
exponents), and for the lower barrier.  `pos_after` is needed for the same reason: it selects the
*last* zero of the shift (`shiftInv_zero : shiftInv θh 0 = ec`, so `ec` is determined by `θh`, and
the `ec` of `GameFunction.hintShape` is unique).

**O5 — `HintShape` is more general than "hinted exponent of a game function".**  For a game
function the shift is nonnegative and `R(e) = -e` on `(-∞, e_c]`; `HintShape` allows a negative
shift before `ec`.  Example (not machine-checked): `θh(e) = max(0, (E-e)/2)`, `ec = -E`, with
partner `θna(x) = max(0, E - x)` on `[0, ∞)`, `a = E`, `h = E/2` — a piecewise-linear pair, which is
also the pair of the tent `F(t) = E·min(t, 1-t)`.

**O6 — the lower barrier holds abstractly, without clipping.**  `HintShape.superSolution` is the
convexity argument of `gauss_hint_superSolution` and `cube_hint_superSolution` with the special
functions removed: it uses only convexity, monotonicity and `S(S⁻¹(x)) = x`.  Because a
`HintShape` lives on the whole line and vanishes from `E` on, no clipped copy of the hinted
exponent is needed (compare the finding of workstream L about `step_from_hint_le`):
`step_from_hint_le` applies to `HintShape.pair` directly.  `HintShape.Rstep_hint` is the abstract
form of the fixed-point statement that the cube has as `cube_step_from_hint_le` +
`cube_hint_superSolution`, `HintShape.exactRec_tendsto` of `exactRec_tendsto_hint`, and
`HintShape.lt_partner` (`θh < θna` on `[0, E)`) of `cubeHint_lt_cubeNa`.

**O7 — the witness reproduces the toy pair, and corrects its continuation.**
`partner (hinted toyGame) = gaussNa` on `(0, ∞)`, `hinted toyGame = gaussHint` on `[-1, 1]`, and
the constants of `toyGame_pair` are those of `gaussPair` (`a = 1`, `h = 1/4`, `E = 1`).  Outside
`[-1, 1]` the two differ: `hinted toyGame e = 0` for `e ≥ 1` and `= -e` for `e ≤ -1`
(`hinted_toyGame_of_one_le`, `hinted_toyGame_of_le_neg_one`), whereas
`gaussHint e = (1-e)²/4` increases again beyond `1`; so `gaussHint` itself is not a `HintShape`
(evident, not machine-checked), while its restriction to `[-1, 1]` continued by `0` and `-e` is
(`toyGame_hintShape`).

## 8. Files in `scratchpad/ws/M/`

| file | what |
|---|---|
| `GamePair.lean` | **deliverable 1** |
| `M_report.md` | **deliverable 2** (this file; generated by `make_report.py`) |
| `compile_output.txt` | output of the verification command (§5) |
| `final_compile.sh`, `run.sh`, `run_strict.sh`, `run_werror.sh` | compile scripts with the bounded wait |
| `supplement/NoSlopeVariant.lean`, `supplement/make_variant.py` | evidence for O4(b); **not** for integration |
| `BRIEF.md` | the brief (untouched) |

To integrate: copy `GamePair.lean` to `proofs/Frontiers/GamePair.lean`; it needs nothing else.
