# Workstream N — the nesting theorem for the structure it uses: tail functions, instances, obstructions

*Brief written by the coordinator on 2026-11-26, in response to the research owner's
supplementary directive of the same day (generality; an assumption audit; obstruction
theorems; computational consequences — the text is in
`docs/collaboration/messages/theory/THY-MSG-0016.md` §1).  A paper-proof workstream with
numerical checks; no Lean.*

## 1. Where we are

The adaptive theory of the theory report (§§11.18–11.19: Theorems 11.52, 11.54, 11.56,
11.58, 11.58a) is proved for one model: the cube `Q_n` with the uniform measure and the
class `L_u` of functions that are `u`-Lipschitz in the Hamming metric.  Later sections
carry the *exponents* to other classes by separate arguments (a field: §11.20; several
site types and alphabets: §11.26; a nearest-neighbour known part: §11.32).  The proof of
the level theorem uses the cube in a few identifiable places.  The directive asks for
the theorem stated for what it uses, a hierarchy of instances, and the obstructions.

Read first: theory report lines ~4769–4925 (bracket procedures, Theorem 11.52 with its
proof: facts (F1)–(F3), the algorithm, the good event, validity, width, cost),
~5185–5320 (Lemma 11.55, Theorem 11.56), `docs/workstreams/K_REPORT.md` §2.2 with the errata
at its head (Algorithm 2L⁺ and Theorem K1 = 11.56 with all constants), the tail lemma
11.43 (search the report for "Lemma 11.43"), and §11.21 ("every game function yields a
pair").  For the instances: §11.20, §11.26, §11.32 (statements only, at first).

## 2. The coordinator's reading (check it; it is a sketch, not a result)

**(a) What the proof uses.**  (i) two blocks with a *product* measure, `μ = μ_o ⊗ μ_i`, so that
`A = E_a W(a)`, `W(a) = E_b e^{−ψ(a,b)}`, outer points are i.i.d. from `μ_o`, and the inner
procedure runs on a fibre with the fixed measure `μ_i`; (ii) (F1) every fibre is in the
class for which inner bracket procedures exist; (iii) (F2) `−ln W` is in a class of
functions on the outer block for which a **tail function** is known: a nondecreasing
`Ξ_o: [0, 1] → [0, ∞]` with

    for every f in that class and every s > 0:   μ_o(e^{−f} > s) ≤ q   ⟹   E(e^{−f} − s)₊ ≤ s·Ξ_o(q)

(on the cube: `q = |B(n_o, r)|/2^{n_o}`, `Ξ_o(q) = 2^{−n_o}E_r(n_o)`, by Harper's theorem — Lemma
11.43); (iv) (F3), the layer cake — general; (v) a trivial bracket from one evaluation
(`s₀ ≤ W ≤ s₀e^{2un}`: bounded oscillation); (vi) atoms of mass `2^{−n_o}` (the tail is zero
once `2^{n_o}q < 1`; `M ≤ 4K·2^{n_o}`); (vii) for the *cost* only: the size of the closing
level, i.e. bounds on `Γ̃ = Ξ_o(q)/q` (Lemma 11.55), and the base family.

**(b) The pair is a tautology of the tail function.**  If the blocks have sizes `m → ∞` and
`(1/m) ln Ξ_m(e^{−mθ}) → w(θ)` (the *tail profile*: the accuracy that a set of measure
`e^{−mθ}` can change), then the hinted exponent is `θ_hint = w^{−1}` (the measure of the
smallest set that matters at accuracy `e`), the non-adaptive exponent is defined by
`w(θ) + θ = x` (the ratio `Ξ/q`), and `θ_na(e + θ_hint(e)) = θ_hint(e)` holds by construction.
On the cube `θ = KL(ρ‖½)`, `w = uρ − Λ₁`.  With the concave function
`J(t) = min_θ [θ + t·w(θ)]` this is the setting of `docs/workstreams/R_brief.md` §2: the
convergence of the level recursion and its rate (`2π²h²θ_hint″(0)/k²`, conjectured) are
statements about one function `w`.

**(c) Extensivity is what makes nesting pay.**  The recursion has the factors `φ` and `1 − φ`
because the profile of a block of `φm` sites is `φ·w(θ/φ)`: the Lipschitz budget is additive
over sites (a sum metric).  **Counter-instance (the coordinator's computation; check
it):** standard Gaussian space `ℝⁿ` with functions that are `L`-Lipschitz in the Euclidean
norm.  Facts (F1), (F2) hold, Gaussian isoperimetry gives the exact tail function
`Ξ(q) = ∫_0^∞ L e^{Lr} Φ(−t − r) dr`, `q = Φ(−t)`, and in total units the profile is
`w(Θ) = L²/2 − L√(2Θ)` for *every* block, whatever its dimension: `Θ_na(X) = (L − √(2X))²/2`,
`Θ_hint(e) = (L/2 − e/L)²/2`.  The level bracket is then
`sup_{γ ≥ β} [min(γ, Θ_na(G − β)) + T(γ)]` with no factor `1 − φ`, and with `T = Θ_na` it is never
below `Θ_na(G)`: **coordinate nesting gains nothing**; whether adaptive algorithms on
Gaussian space reach `Θ_hint` is open.  (In units of `L²/2` these two functions are the
"Gaussian pair" `(1 − √x)²`, `(1 − e)²/4` of the report, which arises there as the
small-slope limit of the cube, where nesting does work.)

**(d) Dependence.**  If `μ` is not a product, sample `a ~ μ_o` and run the inner procedure
under the conditional law `μ(·|a)`.  (F1) is unchanged.  (F2) holds with the slope `u + L`
if the conditional laws have *bounded influence*: `ln[dμ(b|a)/dμ(b|a′)] ≤ L·d_o(a, a′)` for all
`b` (for a nearest-neighbour chain cut into two segments only the boundary site has
`L ≠ 0`).  Without such a bound (F2) can fail — a counterexample is wanted — and then the
closure test certifies nothing.

## 3. What to deliver

**N1 (must) — the audit of the proof.**  Go through the proof of Theorem 11.56
(`K_REPORT.md` §2.2, with the theory report's text) step by step and list every use of
the cube, each marked "validity" or "cost only".  Correct §2(a) where it is wrong or
incomplete.

**N2 (must) — the abstract level theorem.**  Statement and proof: for probability spaces
`(X_o, μ_o)`, `(X_i, μ_i)`, a class of functions on `X_o × X_i` with (F1), (F2), a tail function
`Ξ_o`, a trivial bracket of width `D`, and inner bracket procedures with certified costs,
Algorithm 2L⁺ — with "the least radius `r` with `|B(n_o, r)| ≥ 2^{n_o}q`" replaced by `q` and the
tail by `s_j·Ξ_o(q)` — returns a valid bracket of the stated width with the stated failure
probability, at a cost bounded through the closing level
`q† = sup{q : Ξ_o(q′)/q′ ≤ (threshold) for all q′ ≤ q}`.  Say exactly which properties of
`Ξ_o` are used (monotonicity; what replaces the atoms; what replaces integrality of
radii), what changes for a measure without atoms (termination, the bound on the number
of outer points), and what the constants become.  The cube must come out as the special
case with the constants of Theorem 11.56 (or say where it does not and why).  Then the
variant with dependence (§2(d)): hypotheses, statement, proof.

**N3 (must, short) — the exponent level.**  §2(b) as a proposition with its hypotheses on
`w` (existence of the limit, monotonicity, what gives convexity of `θ_na` and the
properties of `J` that `R_brief.md` uses), for homogeneous families; and the form of the
level recursion for a *heterogeneous* family (sites of several kinds, site-dependent
slopes: which sites should the outer block take?) — state it, prove what is easy, flag
the rest.

**N4 (should) — instances, each with an honest status.**  For each: the spaces, the class,
the tail function and where it comes from (a theorem of the report, a theorem of the
literature with its exact reference, or "not available"), whether it is sharp at the
exponential scale, and what the abstract theorem then gives that the report does not
already have.  (a) the cube; (b) the `p`-biased cube (§11.20); (c) finite alphabets and
several site types with the Hamming metric (§11.26); (d) site-dependent slopes `u_i`
(weighted Hamming metric); (e) a product of continuous site spaces of bounded diameter
with the sum metric (circles of torsion angles: a *valid* tail function from a
tensorising transport or infimum-convolution inequality — is it sharp?); (f) a
nearest-neighbour chain as known part (§11.32), through §2(d).

**N5 (should) — obstructions.**  (a) §2(c): prove the statement about Euclidean Gaussian
space (the exact tail function, the profile, `R[Θ_na] ≥ Θ_na`, i.e. `min(T, R[T]) = T` at
`T = Θ_na`), and say what is and is not shown about adaptive algorithms there; (b) an
explicit pair (known part with unbounded influence, Lipschitz residual) for which (F2)
fails by a factor that grows with `n`, and what the algorithm then does (an invalid
bracket, with a numerical demonstration on a small instance if you can; or only a cost
blow-up); (c) unbounded oscillation (no trivial bracket): what is needed instead.

**N6 (must) — the assumption table** of Theorems 11.52/11.56/11.54/11.58 in the six
categories of the directive: essential / required only by the present proof / introduced
for convenience / replaceable by a weaker quantitative condition (state it) / removal
changes the complexity (state how) / removal makes the result false (give the
counterexample) — each entry with its evidence, "not known" where that is the truth.

## 4. Rules

* Create only `docs/workstreams/N_REPORT.md` and files under `experiments/workstreams/N/`
  (scripts with stored outputs; commands in the report).  Do not edit any existing
  file.  Do not run `lake` or `scripts/audit_all.sh`.  No git command that changes state.
  Do not start further agents.
* Every statement labelled: proved here / quoted (from where, with its status in the
  report: [V] machine-checked, [P] paper, [N] numerical) / numerical / heuristic /
  conjecture / open.  Do not claim a generalisation that you have not proved: "the proof
  of the report goes through verbatim" is a claim that needs the list of steps checked.
  Literature: cite only what you can state precisely; mark anything quoted from memory
  as such.  A general theorem whose guarantee is vacuous in an instance (a tail function
  too weak to give a positive exponent, say) is to be labelled vacuous there.
* Scope: mathematics of certified computation for abstract spaces and synthetic
  examples.  No biological sequences, no target-specific optimisation.
* One Python process at a time, under about 1.5 GB; the machine (4 cores) is shared.
  Foreground `sleep` is not available; wait with bounded loops if you must.

## 5. What to report back

At most 45 lines: the abstract theorem (hypotheses, conclusion, what replaced each cube
ingredient), the status of each instance, the obstructions proved, the six-category
table in summary (counts per category and the three most consequential entries), the
weakest link, errors found in the report or in this brief, files created.
