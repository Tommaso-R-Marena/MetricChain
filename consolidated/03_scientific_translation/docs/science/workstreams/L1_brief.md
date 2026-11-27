# Workstream L1 — machine-checking the science division's core statements (Lean 4 + Mathlib)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_L1/`; your report: `docs/science/workstreams/L1_REPORT.md`.

## Why

The programme's currency is the label **[V]**: a statement whose Lean proof depends only on
`propext`, `Classical.choice`, `Quot.sound`.  The science division's own results
(`docs/science/INFERENCE_LIMITS.md`, `docs/science/INFERENCE_LIMITS_ADDENDA.md`) are paper proofs by
one author.  Several of them are short, finite and algebraic — exactly the kind that should
be machine-checked before another division is asked to build on them.  Formalisation is
also the most effective referee: if a statement does not typecheck as intended, say so.

## Environment (read carefully)

* Lean 4.31.0 at `~/.lean/lean-4.31.0-linux/bin`; Mathlib `v4.31.0` cache and the built project
  are present.  Check a file with
  `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain; lake env lean <absolute path of your file>`
  (about one to three minutes per file; the machine is shared — keep files small, one topic
  per file, and do not launch more than one check at a time).  **Never** run `lake build`,
  `lake update`, `lake clean` or `scripts/audit_all.sh`.
* Your files live in `experiments/science/ws_L1/` and are **not** part of the `proofs/` library
  (the theory division's audit requires every module under `proofs/` to be registered in its
  axiom audit, and we do not edit their files).  You may `import Mathlib` and, read-only, the
  theory division's modules (e.g. `import proofs.Frontiers.ThermalRobustness`,
  `proofs.Frontiers.QueryLowerBound`, `proofs.Frontiers.NonAdaptive`) when a statement of ours
  is a corollary of one of theirs; look at how they state things first.
* House rules of the programme, which apply to you: no `sorry`, no `admit`, no `native_decide`,
  no axioms; end each file with `#print axioms <main theorem>` for every headline theorem and
  record the output in your report.  A statement proved under an extra hypothesis must say so
  in its name and in the report.

## Targets, in order of priority (stop where time runs out; partial is fine)

1. **Soundness of the identified-set certificates** (`INFERENCE_LIMITS.md` §8, Theorem 8(c)),
   on a finite type `X` with real-valued functions:
   (a) model-free: for `μ` a probability vector with `Σ μ φ_k ∈ [lo_k, hi_k]` and multipliers
   `λ⁺, λ⁻ ≥ 0`, if `ψ x ≤ t + Σ_k (λ⁺_k (φ_k x − hi_k) − λ⁻_k (φ_k x − lo_k))` for all `x` then `Σ μ ψ ≤ t`;
   (b) envelope class in the weights: `w ≥ 0`, `Σ μ₀ w > 0`, `w y ≤ κ x y * w x`, data constraints
   in homogeneous form, a non-negative flow `F` with
   `(ψ z − t − Λ z) * μ₀ z ≤ Σ_x F x z − Σ_y κ z y * F z y` ⟹ `(Σ μ₀ w ψ)/(Σ μ₀ w) ≤ t`;
   (c) falsification: the same with `ψ ≡ 1`, `t = 0` yields `False`;
   (d) the divergence-ball format if Mathlib has what is needed for the Donsker–Varadhan
   inequality on a finite type (otherwise state it with the Gibbs variational inequality
   `Σ μ F ≤ KL + log Σ μ₀ exp F` proved directly from `log` concavity / `Real.add_pow_le_pow_mul_pow_of_add_eq_one`
   or Jensen — try; if it costs more than an hour, skip and say so).
2. **The separation inequality of Theorem 4′** (`INFERENCE_LIMITS_ADDENDA.md` A1), abstractly:
   for finite `X`, functions `dC ≤ d1` pointwise (naturals or reals), `u > 0`, `R`, with
   `A = Σ exp(−u dC)`, `F = Σ exp(−u max(dC,R))`, `A1 = Σ exp(−u d1)`, `F1 = Σ exp(−u max(d1,R))` and the
   hypothesis `F ≤ m * F1`: `A / F ≥ 1 + (A1/F1 − 1)/m` and hence `log A − log F ≥ log (A1/F1) − log m`
   when `m ≥ 1`.  Then, if feasible, the concrete `F ≤ |C| * F1` for `dC x = min over a ∈ C of d1 (x + a)`
   on `Fin n → ZMod 2` (or `Fin n → Bool`) with `d1` the Hamming distance to a fixed centre.
3. **Lemma 1** (orthogonal-array property): for a subgroup / subspace `C` of `Fin n → ZMod 2`
   whose annihilator contains no non-zero vector supported on a set `S`, the projection of
   `C` to the coordinates in `S` is onto; hence a `C`-invariant probability vector has uniform
   marginal on `S`.  (State the dual-distance hypothesis in whatever form is cleanest; say
   exactly which form you proved.)
4. **Theorem 7, algebraic core**: on a finite type, for probability vectors `μ, ν` with full
   support, `ν ∝ μ₀ exp(−λ'·Φ)`, `μ ∝ μ₀ exp(−λ·Φ − r)`, `Σ μ Φ = Σ ν Φ`:
   `KL μ ν + KL ν μ = Σ ν r − Σ μ r`; and the purely algebraic step "`4·TV² ≤ J` and `J ≤ ω·TV` imply
   `TV ≤ ω/4` and `J ≤ ω²/4`".  Use Mathlib's Pinsker inequality if it exists in this version
   (search for it; report what you found); if not, state Theorem 7(ii)–(iii) with Pinsker as
   an explicit hypothesis.
5. **Theorem 3** (basin bound) or **Theorem 2(d)** (the entropy lower bound) only if 1–4 are
   done.

For every target: first write the statement in Lean and check that it says what the note
says (quantifiers, hypotheses, non-vacuity — give a small non-vacuity witness where a
hypothesis could be unsatisfiable); then prove it.  If the formal statement you can prove
is weaker or differently shaped than the note's, report the difference precisely.  If a
statement of the note is false as written, give the counterexample.

## Deliverable

`L1_REPORT.md`: a table *statement of the note → Lean declaration → file → hypotheses as
formalised → `#print axioms` output → differences from the paper statement*; what was not
done and why; any error found in the note.  All `.lean` files in your directory, each
checking on its own with the command above.  Final message: at most 400 words — what is
now machine-checked (declaration names), what is not, any discrepancy with the note, and
the absolute path of the report.
