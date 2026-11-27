# Lean task LE — two requests of the Scientific Discovery Division

*Brief written by the coordinator on 2026-11-26.  Two new Lean files; nothing else.  The
statements were asked for in SCI-MSG-0028 §7 (requests P9-T1, P9-T3, A19-T1); the paper
proofs below were re-derived by the coordinator from that message.*

## File 1 — `proofs/Frontiers/ResolvedPenalties.lean` (namespace `MetricChain.ResolvedPenalties`)

Setting as in `proofs/Frontiers/HigherOrderEnvelope.lean` (reuse its `supp x₀ x` — the sites at
which `x` differs from the anchor `x₀` — and import that file, or `TermOrders.lean` if (c) needs
it): `ι` a finite type with decidable equality, `σ : ι → Type*` with decidable equality,
`x₀ : ∀ i, σ i`.

**(a) Proposition P (state-dependent bounds charged to sub-tuples).**  For every set `T` of `m`
sites a bound `Φ T x ≥ 0` (the science division's `Θ_T(x_T)`); weights `w T U ≥ 0` on the
non-empty `U ⊆ T` with sum one; tables `c T U x ≥ 0` that dominate `Φ T` (their
`c_{T,U}(x_U) = max{Φ_T(y_T) : y_U = x_U}`; only domination is used); `γ U x ≥ 0` at least
`Σ_{T ⊇ U, |T| = m} w T U · c T U x` whenever `U ⊆ supp x₀ x`.  Then for every `x`

    Σ_{T ⊆ supp x₀ x, |T| = m} Φ T x   ≤   Σ_{U ≠ ∅} γ U x        — and even ≤ Σ_{∅ ≠ U ⊆ supp x₀ x} γ U x.

Paper proof: for `T ⊆ supp x₀ x`, `Φ T x = Σ_U w T U · Φ T x ≤ Σ_{∅≠U⊆T} w T U · c T U x`; sum over `T`,
exchange the sums (`U ⊆ T ⊆ supp` implies `U ⊆ supp`), enlarge the inner sum to all `T ⊇ U` of
size `m` (non-negative terms), use the hypothesis on `γ`; the remaining `U ⊄ supp` contribute
`γ U x ≥ 0`.  A suggested form:

    theorem resolved_allocation [Fintype ι] [DecidableEq ι] [∀ i, DecidableEq (σ i)] (m : ℕ)
        (x₀ : ∀ i, σ i) (Φ : Finset ι → (∀ i, σ i) → ℝ) (w : Finset ι → Finset ι → ℝ)
        (c : Finset ι → Finset ι → (∀ i, σ i) → ℝ) (γ : Finset ι → (∀ i, σ i) → ℝ)
        (hw0 : ∀ T U, 0 ≤ w T U)
        (hw1 : ∀ T, T.card = m → ∑ U ∈ T.powerset.filter (·.Nonempty), w T U = 1)
        (hc : ∀ T U x, T.card = m → U ⊆ T → T ⊆ supp x₀ x → Φ T x ≤ c T U x)
        (hc0 : ∀ T U x, 0 ≤ c T U x)
        (hγ : ∀ U x, U.Nonempty → U ⊆ supp x₀ x →
          ∑ T ∈ (Finset.univ.powersetCard m).filter (U ⊆ ·), w T U * c T U x ≤ γ U x)
        (hγ0 : ∀ U x, 0 ≤ γ U x) (x : ∀ i, σ i) :
        ∑ T ∈ (supp x₀ x).powersetCard m, Φ T x ≤
          ∑ U ∈ (supp x₀ x).powerset.filter (·.Nonempty), γ U x

plus the corollary with the sum over all non-empty `U` (needs `hγ0`), and the corollary in
which `c T U x` is literally the maximum of `Φ T` over the states that agree with `x` on `U`
and are off the anchor on `T` (a `Finset.sup'` over a non-empty finite set; if the
dependent-type bookkeeping of "agree on `U`" costs more than about sixty lines, state it
with a hypothesis "`c T U x = c T U y` whenever `x, y` agree on `U`" instead and say so).
(If `m = 0` needs a side condition — `T = ∅` has no non-empty subset, so `hw1` cannot hold —
add `0 < m`.)

**(b) The reduction step.**  A table may be replaced by its maximum over sites that are given
up: for `V ⊆ U`, `γ U x ≤ sup {γ U y : y agrees with x on V}` (immediate; state it in the form
that composes with (a): if `γ' V x ≥ γ U y` for all `y` agreeing with `x` on `V`, then the
right-hand side of (a) with `γ U` replaced by `γ' V` — moved to the index `V` — is still an
upper bound).  Keep it simple; one lemma.

**(c) P9-T3: the remainder bound with constants that depend on the actual state.**
`MetricChain`'s `anchored_remainder_bound_orders` (in `proofs/Frontiers/TermOrders.lean`; read its
statement) is stated for one `y`, and its hypothesis `hc` is needed at that `y` only, so the
constants may depend on `y`.  Make that explicit as a corollary: with
`c : κ → Finset ι → (∀ i, σ i) → ℝ` and the hypothesis for every `y`, the conclusion with
`c τ T y`.  (A direct instantiation.)

## File 2 — `proofs/Frontiers/GibbsRecovery.lean` (namespace `MetricChain.GibbsRecovery`)

Proposition A17.19 of the science division.  `Ω` a non-empty finite type, `β ≥ 0`,
`mlo E mhi : Ω → ℝ`, `G` a finite index type, `Sp Sm : G → Ω → ℝ` pointwise non-negative with

    ∑ g, Sp g ω ≤ mhi ω − E ω      and      ∑ g, Sm g ω ≤ E ω − mlo ω        for every ω.

`Z f = ∑ ω, exp (−β · f ω)`,  `avg X = (∑ ω, X ω · exp (−β · mhi ω)) / Z mhi` (the mean under the
ceiling model).  Prove

    (LJ)  log (Z E) ≥ log (Z mhi) + β · ∑ g, avg (Sp g)
    (LP)  log (Z E) ≥ log (Z mhi) + log (1 + ∑ g, avg (fun ω => exp (β · Sp g ω) − 1))
    (UE)  log (Z E) ≤ u  →  log (Z E) ≤ log (Z mlo) − β · (∑ g, avg (fun ω => Sm g ω · exp (β · Sp g ω))) · exp (log (Z mhi) − u)
    (UP)  log (Z E) ≤ u  →  log (Z E) ≤ log (Z mlo) − log (1 + (∑ g, avg (fun ω => (exp (β · Sm g ω) − 1) · exp (β · Sp g ω))) · exp (log (Z mhi) − u))

and that the iterations `u_0 = log (Z mlo)`, `u_{t+1} = (right-hand side of (UE) or (UP) at u_t)`
consist of upper bounds of `log (Z E)`.  Paper proofs:
(LJ), (LP): `Z E / Z mhi = avg (exp (β(mhi − E))) ≥ avg (exp (β ∑_g Sp g))`; then Jensen for `exp`
(`ConvexOn.map_sum_le` with `convexOn_exp`, weights `exp(−β mhi ω)/Z mhi`), or
`∏_g (1 + y_g) ≥ 1 + ∑_g y_g` for `y_g = exp(β Sp g ω) − 1 ≥ 0`.
(UE), (UP): with `avgE X = (∑ ω, X ω · exp (−β E ω)) / Z E` (the mean under the true ensemble),
`Z mlo / Z E = avgE (exp (β(E − mlo))) ≥ avgE (exp (β ∑_g Sm g))`, then Jensen, resp. the product
inequality; and for `X ≥ 0` and each `g`:
`avgE X ≥ (Z mhi / Z E) · avg (X · exp (β Sp g)) ≥ exp (log (Z mhi) − u) · avg (X · exp (β Sp g))`,
because `E ≤ mhi − Sp g` pointwise (`Sp ≥ 0`, the first hypothesis) and `Z E ≤ exp u`.
For (UE) take `X = Sm g`, for (UP) `X = exp (β Sm g) − 1`.
`log (Z E) ≤ log (Z mlo)` because `mlo ≤ E` (the second hypothesis and `Sm ≥ 0`).

If one of the four resists, deliver the others; (UE) has priority (it is the one whose
proof has a step outside the textbook).

## Rules

* Create only the two files named above.  Do not edit any existing file (the coordinator
  adds the imports to `proofs/AxiomAudit.lean` and the `#print axioms` lines).
* Toolchain: `export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"`; check each file with
  `cd /home/user/MetricChain && lake env lean proofs/Frontiers/<File>.lean` (single file; the
  imports are built).  Do **not** run `lake build` of the whole project,
  `scripts/audit_all.sh`, or anything that rebuilds Mathlib.  One Lean process at a time;
  another Lean task and two Python workstreams share the machine.
* Project rules for Lean files (the audit greps for them): no `sorry`, no `admit`, no
  `native_decide`, no `bv_decide`, no `axiom`, no `unsafe`, no `implemented_by`, no
  `#guard_msgs`, no line starting with `example`, and **the word "stop" must not occur
  anywhere in the files, comments included** (the science division's messages use the
  phrase "stopping condition": do not copy it).  Only the axioms `propext`,
  `Classical.choice`, `Quot.sound`: check each main theorem with a temporary
  `#print axioms` line and remove it before you finish.
* Each file gets a module docstring: what is proved, whose statement it is (Scientific
  Discovery Division, SCI-MSG-0028; workstream P9's Proposition P and Theorem R; addendum
  A17 (19)), and what is not proved (that the tables of an actual certificate satisfy the
  hypotheses; the transfer matrices; floating point).
* If a tactic fails three times in the same way, change the approach.  Do not weaken a
  statement silently: say in your report where a hypothesis changed form.
* No git command that changes state.  Do not start further agents.

## What to report back

At most 25 lines: the theorems with their final statements where they differ from this
brief, the result of the two single-file checks, the axioms, anything in the paper
proofs above that needed a correction, line counts.
