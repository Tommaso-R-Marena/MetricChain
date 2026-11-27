# Workstream L4 — Lean: the remainder identity of the anchored expansion (workstream P3) and the two-point Bennett–Hoeffding bound (requested by the theory division)

*Brief written by the coordinator at checkpoint 41 (2026-11-26).  Read `COMMON.md` first
(pins out of date).  Style, conventions and reporting as in workstreams L1–L3
(`docs/science/workstreams/L3_REPORT.md` is the model for your report;
`experiments/science/ws_L3/` for file layout, `check_all.sh`, `#print axioms`).*

## Why

1. Workstream P3 certified a free energy beyond enumeration size; the combinatorial core
   of its certificate is a remainder identity and an allocation lemma that are paper
   proofs (`docs/science/workstreams/P3_REPORT.md` §2.1 Proposition 1; §2.4 the last
   paragraph; `docs/collaboration/messages/science/SCI-MSG-0020.md` §1).  We asked the
   theory division to machine-check them (P3-T1); it is better to deliver the file.
2. The theory division asks (THY-RES-0009 §7.4, §9.5): "the two-point Bennett bound of
   Theorem 11.110(f) … Not machine-checked: on top of `jensen_bracket` it needs the
   reduction to two-point laws, which is the whole proof."

## What to formalise (Lean 4.31.0 + the pinned Mathlib; files importing Mathlib only,
unless importing the theory division's compiled files is clearly better — say which)

Compile with `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"; cd /home/user/MetricChain;
lake env lean <absolute path>` — never `lake build`, `lake update`, `lake clean`.  Our tree
is built on the theory commit `5ed4072`; `proofs/Frontiers/HigherOrderEnvelope.lean`
(`anchoredInterp`, `anchored_decomposition`, `higherOrder_remainder`, `HigherDiffBound`) is
compiled there and may be imported read-only.

**Part A — the remainder identity (first priority).**
On a finite product `X = Π_{i} S_i` with linearly ordered sites, anchor `x⁰`,
`S(x) = {i : x_i ≠ x⁰_i}`, mixed difference
`Δ_T g(z; y_T) = Σ_{U⊆T} (−1)^{|T|−|U|} g(y_U, z_{−U})`, anchored terms `d_U = Δ_U g(x⁰; ·)`,
interpolant `I_M g(x) = Σ_{U⊆S(x), |U|≤M} d_U(x_U)`:
1. `g(x) = Σ_{U⊆S(x)} d_U(x_U)` (if the theory file has it as `anchored_decomposition`,
   reuse it and say so).
2. **Proposition 1:** for every `m ≥ 1`,
   `g(x) − I_{m−1}g(x) = Σ_{T⊆S(x), |T|=m} Δ_T g(z^{T,x}; x_T)`, `z^{T,x}_i = x_i` for
   `i < min T`, `x⁰_i` otherwise.  (Paper proof: P3 report §2.1 — context expansion, then
   send each `U` with `|U| ≥ m` to its `m` largest elements.)
3. Corollary: `|g(x) − I_{m−1}g(x)| ≤ Σ_{T⊆S(x), |T|=m} c_T` whenever
   `|Δ_T g(z; y_T)| ≤ c_T` for all base points `z` with `z_T = x⁰_T` (anchored constants).
4. **Allocation lemma at order `m`:** for `c_T ≥ 0` and `γ_i := (1/m)Σ_{T∋i, |T|=m} c_T`:
   `Σ_{T⊆S, |T|=m} c_T ≤ Σ_{i∈S} γ_i` for every `S`.  More generally any nonnegative
   shares of each `c_T` among its sites that add up to at least one.  (The theory
   division's new `ThirdOrderModel.lean` at `24a3c27` has the case `m = 3`
   (`cover_of_site_shares`); read-only copy:
   `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27/proofs/Frontiers/`.)
5. Hence the sandwich: `Σ_{|U|<m} d_U(x_U) − Σ_{i∈S(x)} γ_i ≤ g(x) ≤ Σ_{|U|<m} d_U(x_U) + Σ_{i∈S(x)} γ_i`.

**Part B — the Bennett–Hoeffding two-point bound.**
For a real random variable with finitely many values (a finite type with a probability
weight is enough; a general probability space if it costs nothing): if `X ≤ b` (`b > 0`),
`E X = 0` (or `≤ 0`), `E X² ≤ σ²`, then
`E e^{X} ≤ (b² e^{−σ²/b} + σ² e^{b}) / (b² + σ²)`,
with equality for the two-point law `P(X = b) = σ²/(b² + σ²)`, `P(X = −σ²/b) = b²/(b² + σ²)`.
Then, for a remainder `r` with `r ≥ E r − b` and `Var r ≤ σ²`:
`0 ≤ ln E e^{−(r − E r)} ≤ W(b, σ²) := ln[(b² e^{−σ²/b} + σ² e^{b})/(b² + σ²)] ≤ (σ²/b²)(e^{b} − 1 − b)`;
`W` is nondecreasing in `b` and in `σ²`; and the deterministic part of the certificate:
if `|r̄ − E r| ≤ η` and `lo ≤ r` pointwise then
`−r̄ − η ≤ ln E e^{−r} ≤ −r̄ + η + W(r̄ + η − lo, σ²)`.
Standard proof (Bennett 1962; Hoeffding 1963, Theorem 3; Fan–Grama–Liu, arXiv:1109.4359,
Lemma 3.1 "we argue as in Bennett"): for `λ > 0` the parabola through the graph of
`e^{λx}` that touches it at `x = −σ²` and meets it at `x = 1` lies above `e^{λx}` on
`(−∞, 1]`; integrate.  Any correct proof is fine.  The lower half `0 ≤` is Jensen.
Also worth having if cheap: the middle form `W ≤ ln(1 + (σ²/b²)(e^{b} − 1 − b))`, and the
lower bound under a ceiling, `r ≤ E r + a ⇒ ln E e^{−(r−Er)} ≥ ln(1 + Var(r)(e^{−a} − 1 + a)/a²)`
(addendum A17 (7) of `docs/science/INFERENCE_LIMITS_ADDENDA.md`).

## Deliverables

`experiments/science/ws_L4/` (create it): the Lean files (each compiling on its own, exit
code 0, no `sorry`, `admit`, `native_decide`, `axiom`; `#print axioms` for every headline
theorem at the end of each file), `check_all.sh`, `NOTES.md`; report
`docs/science/workstreams/L4_REPORT.md` with: what is [V] (declaration names), the exact
Lean statements of the headline theorems, the differences between the formal statements
and the paper statements, findings (anything in the paper statements that is false,
redundant or improvable), what is not done.  Write nowhere else; no state-changing git.
Part A first; if Part B's sharp two-point form resists, deliver the weaker exponential
form `ln E e^{−(r−Er)} ≤ (σ²/b²)(e^{b} − 1 − b)` (Bennett's (8b)) and say so.
Budget: aim for about two hours.
