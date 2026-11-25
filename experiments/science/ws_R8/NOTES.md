# Workstream R8 — notes (chronological)

Adversarial referee of addendum A16 (`docs/science/INFERENCE_LIMITS_ADDENDA.md`, lines 721–998).
Written as I go.  Tree: `/home/user/MetricChain`, branch `research/scientific-translation`,
head `39e0cd9` (read-only for me except this directory and `docs/science/workstreams/R8_REPORT.md`).

## Step 0 — reading (no computation yet)

* Read `docs/science/workstreams/COMMON.md` (full) and `R8_brief.md` (full).
* Read addendum A16 in full (lines 721–998 of `INFERENCE_LIMITS_ADDENDA.md`).
* Read background: `INFERENCE_LIMITS.md` §0–§2, §4–§5 (Theorem 5, Proposition 5b); addendum A12
  (oracle invariance; notes of the second reading of R6); `R3_REPORT.md` §4 R6 (Lemmas
  R6.1–R6.3, Theorem R6, Corollary R6′); `A1_REPORT.md` §2.5 (Proposition A1.1); theory report
  at the commit of our tree (`5ed4072`): Theorem 11.25, Lemma 11.43, Theorems 11.44, 11.45,
  Proposition 11.46, Theorems 11.53 (statement), 11.54.  Messages SCI-MSG-0012, SCI-MSG-0013;
  digest items 25, 27; status rows S34, S36.  I have NOT opened the coordinator's three scripts
  yet (deliberately: own numerics first).

## Step 1 — paper re-derivation before any numerics (summary; details go to the report)

* A16.1: chain rule argument re-derived; correct.  Product-reference variant re-derived via
  `ln(Z_g/Z_0) = −U − KL(μ_g‖π)`; correct.
* A16.2: `ln cosh(u/2) = KL(½‖σ_u)` and both series re-derived by hand; correct.
* A16.3: excess identity re-derived; shallow end correct; deep end written out for general
  `k = r₂ − r₁ ≥ 1` (free version holds for every `n`: `W+X ≤ Z₀` because `X ≤ 2ⁿ − V`; with
  overlap a sufficient condition is `r₂·ω < e^{uk}(kW + Y/u)`); (b), (c), counting re-derived.
* A16.5: convexity, direction of the Lagrangian inequality, monotonicity of `F_η`, Harper step,
  choice of `η`, monotonicity of `U` in the level (`dU/dc = −μ(P)(1 + c + U) < 0`) re-derived.
  The complement of an initial segment of the simplicial order is isomorphic (x ↦ x̄) to an
  initial segment.  Only the pointwise bounds `|g(x)| ≤ u·dist(x, supp^c)` are used.
* A16.6: (i) fine; (ii) correctness fine up to the fallback's own failure probability; the
  cost claim compares a lower bound on the EXPECTED number of evaluations (A16.3) with an
  upper bound that holds WITH HIGH PROBABILITY — the expectation of the algorithm's cost
  depends on the fallback (prob. of hitting the basin × cost of fallback).  To be quantified.
  (iii) "= G(r₂−1)" is numerics, and by the lemma the twin (support |D|+|V| > |B(r₂−1)|) is only
  bounded by G(r₂).  (iv) exponential-scale formula re-derived: crossing at `ue = a(u)`,
  i.e. `e = ρ₀ − σ_u` (identity `a(u) = u(ρ₀ − σ_u)` checked by hand).
* Non-adaptive guess: my reading of the pair — outside a ball of radius ρ₃n the cone; inside
  either (A) the cone flattened at radius σ₂n or (B) the cone raised by c₂ up to a plateau
  ring at level uρ₃n; same mean energy iff c₂ = u(σ₂−σ_u)n; B needs c₂ < n·KL(ρ₃‖σ_u).
  This reproduces θ_na(u(σ₂−σ_u)) as a LOWER bound.  To be constructed exactly.
