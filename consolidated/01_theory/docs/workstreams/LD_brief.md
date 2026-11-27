# Lean task LD — the two line lemmas of the level recursion (`LineDynamics.lean`)

*Brief written by the coordinator on 2026-11-26.  One new Lean file; nothing else.*

## 1. Goal

Machine-check, on top of `proofs/Frontiers/HintRecursion.lean` (`StepLE`, `StepLE.of_limit`,
`gaussNa`, `gaussPair`) and `proofs/Frontiers/BoundedAccuracy.lean` (`admissible`, `Rstep`,
`exactRec`, `admissible_nonempty`, `exactRec_props`), the statements below.  Mathematics:
`docs/workstreams/R_brief.md` §2.2 (Lemma L, with its proof) and §2.6 (Lemma M).  The file is
`proofs/Frontiers/LineDynamics.lean`, namespace `MetricChain.LineDynamics`, with a module
docstring that says what is proved and what is not (the analysis of the slope map — how
many levels a line needs — is on paper; the identification of the recursion with
algorithms is on paper).

## 2. Statements (adapt binder names and hypotheses' form as the proofs need; do not weaken)

**(L1) Lemma L — a minorant line survives one step, with a new slope.**

    theorem line_le_Rstep {θna T : ℝ → ℝ} {B σ σ' C : ℝ}
        (hθ : ∀ x, 0 < x → 0 ≤ θna x) (hσ : 0 ≤ σ) (hσσ' : σ ≤ σ')
        (hT : ∀ x, 0 < x → B - σ * x ≤ T x) (hTC : ∀ x, 0 < x → T x ≤ C)
        (hmap : ∀ e, 0 < e → B - (1 - σ) * θna e ≤ σ' * e)
        {g : ℝ} (hg : 0 < g) : B - σ' * g ≤ Rstep θna T g

Proof on paper: `le_csInf (admissible_nonempty hTC hg)`; for an admissible `B₀` with `(φ, β)`
put `e' = (g − β)/φ`, `μ = φ·θna e'`, evaluate the bracket at `γ₀ = max β μ`
(`min γ₀ μ = μ`; `(1−φ)·T(γ₀/(1−φ)) ≥ (1−φ)B − σγ₀`); if `β ≤ μ`:
`B₀ ≥ (1−φ)B + (1−σ)μ ≥ B − σ'(g−β)` by `hmap e'` times `φ`; if `μ < β`:
`B₀ ≥ μ + (1−φ)B − σβ ≥ (1−σ)μ + (1−φ)B − σβ ≥ B − σ'(g−β) − σβ ≥ B − σ'g`.

**(L2) The step of the recursion.**  Under the hypotheses of (L1):
`B - σ' * g ≤ min (T g) (Rstep θna T g)`.

**(L3) Iteration along the exact recursion.**

    theorem lines_le_exactRec {θna : ℝ → ℝ} {B C : ℝ} (s : ℕ → ℝ) (K : ℕ)
        (hθ : ∀ x, 0 < x → 0 ≤ θna x)
        (hθanti : ∀ x y, 0 < x → x ≤ y → θna y ≤ θna x) (hθC : ∀ x, 0 < x → θna x ≤ C)
        (hs0 : 0 ≤ s 0) (hmono : ∀ j, j < K → s j ≤ s (j + 1))
        (h0 : ∀ x, 0 < x → B - s 0 * x ≤ θna x)
        (hmap : ∀ j, j < K → ∀ e, 0 < e → B - (1 - s j) * θna e ≤ s (j + 1) * e) :
        ∀ k, k ≤ K → ∀ x, 0 < x → B - s k * x ≤ exactRec θna k x

and its consequence at accuracy zero: for every `η > 0` there is `x > 0` with
`B - η ≤ exactRec θna K x` (so `sup exactRec θna K ≥ B`: the level-`(K+1)` exponent `τ_{K+1}` of
the report is at least `B`).

**(L4) The Gaussian pair: the slope map is a Möbius map.**  For `0 ≤ σ`, `0 < B`, `σ + B < 1` and
`σ' = B * (1 - σ) / (1 - σ - B)`:  `∀ e, 0 < e → B - (1 - σ) * gaussNa e ≤ σ' * e`.
(For `e ≤ 1`, with `w = √e`: `σ'w² + (1−σ)(1−w)² − B = (pw − (p − B))²/(p − B) ≥ 0`, `p = 1 − σ`; for `e > 1`:
`gaussNa e = 0` and `B ≤ σ' ≤ σ' e`.)  Also: the tangent lines of `gaussNa`:
`∀ x, 0 < x → B - (B / (1 - B)) * x ≤ gaussNa x` for `0 < B < 1`.

**(L5) A concrete witness** (non-vacuity; choose numbers that `norm_num` handles), e.g.
with `B = 3/8`, `s 0 = 3/5`, `s 1 = 6`: `∀ η > 0, ∃ x, 0 < x ∧ 3/8 - η ≤ exactRec gaussNa 1 x` — the
second level of the Gaussian recursion has exponent at least `3/8 > 1/4 = h` at accuracy
zero; and one more step if it is cheap (`B = 3/10`, `s = 3/7, 12/11 · …` — compute the Möbius
orbit and take any `B` whose first two slopes stay below `1 − B`).

**(M1) Lemma M — a majorant with nondecreasing `x + M(x)` on a range, one step.**

    theorem StepLE.monotoneS_step {θna T T' M : ℝ → ℝ} (hs : StepLE θna T T')
        (hanti : ∀ x y, 0 < x → x ≤ y → T y ≤ T x) {R g φ : ℝ}
        (hg : 0 < g) (hφ0 : 0 < φ) (hφ1 : φ < 1)
        (hc : ContinuousAt θna (g / φ)) (hμ : 0 < φ * θna (g / φ))
        (hX : φ * θna (g / φ) / (1 - φ) ≤ R)
        (hTM : ∀ x, 0 < x → x ≤ R → T x ≤ M x)
        (hS : ∀ x y, 0 < x → x ≤ y → y ≤ R → x + M x ≤ y + M y) :
        T' g ≤ (1 - φ) * (φ * θna (g / φ) / (1 - φ) + M (φ * θna (g / φ) / (1 - φ)))

**(M2) The line step at a general outer rate.**  If `T x ≤ B - σ * x` for `0 < x ≤ R` and `σ ≤ 1`
(other hypotheses as in (M1)): `T' g ≤ (1 - φ) * B + (1 - σ) * (φ * θna (g / φ))`; and in the form
with `e = g / φ`: `T' g ≤ B - ((B - (1 - σ) * θna e) / e) * g`.

## 3. Rules

* Create only `proofs/Frontiers/LineDynamics.lean`.  Do not edit any existing file (the
  coordinator adds the import to `proofs/AxiomAudit.lean` and the `#print axioms` lines).
* Toolchain: `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"`; check with
  `cd /home/user/MetricChain && lake env lean proofs/Frontiers/LineDynamics.lean` (single file,
  a few seconds once the imports are built; they are).  Do **not** run `lake build` of the
  whole project, `scripts/audit_all.sh`, or anything that rebuilds Mathlib.  One Lean
  process at a time.
* Project rules for Lean files (the audit greps for them): no `sorry`, no `admit`, no
  `native_decide`, no `bv_decide`, no `axiom`, no `unsafe`, no `implemented_by`, no
  `#guard_msgs`, no line starting with `example`, and **the word "stop" must not occur
  anywhere in the file, comments included**.  Only the axioms `propext`, `Classical.choice`,
  `Quot.sound` may appear in `#print axioms` (check each theorem yourself with a temporary
  `#print axioms` line and remove it before you finish).
* If a tactic fails three times in the same way, change the approach (restate the goal,
  split into lemmas, prove the algebra separately with `nlinarith`/`field_simp`/`ring`).
* No git command that changes state.  Do not start further agents.

## 4. What to report back

At most 25 lines: the list of theorems with their final statements' hypotheses if they
differ from §2, the result of the single-file check (exit status, no warnings that
matter), the axioms each theorem depends on, anything in the mathematics of
`R_brief.md` §2.2/§2.6 that turned out to need a correction.

## Erratum (coordinator, after the task)

(L5) The Möbius orbit of `B = 3/10` is `3/7 → 12/19 → 21/13`, not "`3/7, 12/11 · …`" as written
above; the task computed it and used the right numbers (`gauss_level_three_minorant`).
