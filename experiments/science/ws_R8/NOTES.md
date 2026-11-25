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

## Step 2 — own numerics, first round

* `r8_01_bracket.py` (132 s; log `r8_01_bracket.log`): A16.1 on 576 members of eight families
  (n ≤ 12), adversarial minimisation of the entropy over the class polytope (SLSQP, n = 3, 4, 5;
  greedy extreme-point descent, n ≤ 10), the chain-rule step for random orders, the
  product-reference variant (288 cases), a mutation (1.5u-cone violates), A16.2 identities to
  25–40 digits and the table.  **No violation.**  Minimum entropy found = n·h(σ_u) to 1e-14.
* `r8_02_twin.py` (84 s; log `r8_02_twin.log`): joint-law sums validated against full enumeration
  (n = 16, errors ≤ 1e-10); twelve plateau twins of my own (n = 400…2400, u = 0.5…4, three
  centre distances): root exists, unique on a 121-point grid, κ* > κ_lo, gap − bound(b) between
  +1.08 and +3.05 nats, (c) holds; deep-end condition ω/W₂ < 1/r₂ holds in all cases.  Roots
  exist already at n = 60 (u = 1, ρ₁ = ρ₀ + 0.01); with close centres (D = 0.08 n) the root is
  still there (the hypothesis on the distance is sufficient, far from necessary).
* `r8_03_isoperimetry.py`: first version used pure Kelley cutting planes — too slow (87 LPs per
  case on average, 563 s in quick mode); replaced by a hybrid (4 Kelley LPs, SLSQP in ln t,
  cut at the SLSQP point, Kelley until UB − LB ≤ 1e-8): 5 LPs per case.  The first mutation
  (subcube instead of D*) did not fire at U0 = 0.5·U_cone because both plateaus coincide when
  the level is ≤ u; moved to 0.97·U_cone, fires.  Exhaustive grid: Q_4 with step u/2 has
  277 313 645 functions vanishing at vertex 0 — screened by a level table, borderline cases
  resolved by bisection.  Full run started in the background → `r8_03_isoperimetry.log`.
* `r8_03_isoperimetry.py`, full run (284 s; log `r8_03_isoperimetry.log`): **no violation of
  Lemma A16.5.**  A: Harper form on all subsets of Q_3, Q_4 and 40 000 random subsets of Q_5,
  Q_6; the final segment of the simplicial order has the erosion numbers of the initial
  segment.  B: convex programme over ALL members on a given support — every support of Q_3 and
  Q_4 (20 and 400 orbits; u = 1, 2; four energy bounds each), 500 random supports in Q_5, 150
  in Q_6: largest feasible value − Zpl = +6e-16 (relative); LP upper bounds certify the lemma to
  1.2e-7; on D* the optimum over all members is the plateau (1e-9 … 1.7e-8).  C: exhaustive grid
  — 11 491 441 functions on Q_3 (step u/6), 277 313 645 on Q_4 (step u/2), dips and hills: no
  violation, 906 resp. 67 792 members attain the bound.  D: 900 random general members with
  hills, n ≤ 10.  E: three mutations fire.
* `r8_04_theorem166.py` (88 s; log): table of A16(b) and ε₁ᶜ reproduced; ten exact twins:
  gap(r₂) = G(r₂−1) to 1e-11 at extensive gaps (to 3e-4 … 5e-4 at gaps 7–8 nats), and
  **gap(r₂) > G(r₂−1) in seven of ten cases** (allowed: the twin's support is |D|+|V| > |B(n,r₂−1)|;
  the lemma only gives gap ≤ G(r₂)); at bounded gaps gap ≠ G(r₂−1) (1.287 vs 0.964 at r₂ = r₁+1).
  Radii of lower and upper bound differ by 1 (2 when ε is within o(1) of a value of G).
  P(M samples meet V) is e^{−Ω(n)} but the EXPECTED cost of (ii) with an exhaustive fallback is
  e^{268…1596} times M; with a fallback of cost C the condition is C ≲ 2ⁿ/|V|.
  (iv) formula confirmed (max of the exact width at e = ρ₀ − σ_u within the grid step).
  Bracket of (ii) valid on 300 random general members in random gauge.

*(Housekeeping, on a note from the coordinator.)  One of my shell commands put `cd … &&` in front of a
backgrounded job and then appended to `NOTES.md` with a relative path, so the section "Step 2"
above was written to `/home/user/MetricChain/NOTES.md` (repository root) by mistake.  Merged
here, root file deleted, `git status` checked: nothing else of mine is outside
`experiments/science/ws_R8/`.  From here on the notes file is always addressed by its absolute path.*

## Step 3 — conjecture, non-adaptive guess, prior art

* `r8_05_conjecture.py` (154 s full; log `r8_05_conjecture.log`): exponential-scale search in five
  families (F1 soft basin / tilt with the twin anywhere; F5 remote basin + terrace; F2 product
  flat×cone; F3 K basins; F4 egg carton), ten (u, ε₁) cases: **nothing beats θ_pl**; every family's
  optimum degenerates to the plateau twin on the flat background.  First version of the validity
  test (dominant point of the twin on the plateau, judged on the grid) rejected the reference
  configuration itself because the grid step is coarser than 2e-3 in the rate; replaced by the
  analytic condition (typical point of the plateau sphere in D).  Small-slope (Gaussian) limit:
  closed forms; a "column bound" (any visible landscape, twin in a fresh random direction) equals
  the plateau value — heuristic, written out in the report.
* Read the coordinator's three scripts only now.  `energy_isoperimetry_check.py`, check 1, takes
  "the best energy-feasible modification supported on D" to be the clipped level (explicit) — it
  tests the Harper step, not the Lagrangian step.  Mine (part B: convex programme over all
  members; part C: exhaustive grids) does not assume the form.  Their lemma text in the script
  says "initial segment", the addendum "complement of an initial segment": isomorphic (checked).
  `terrace_twin_explore.py`: a terrace at the co-dominant level with the twin a cap of the rim
  sphere; my F5 has the terrace depth free and a Hamming-ball twin anywhere; same conclusion.
* `r8_06_nonadaptive.py` part 1 (exact radial sums): the pair "cone outside an open ball of radius
  R3; inside either the cone truncated at R1 or the cone raised by c2 under a plateau ring"
  EXISTS: equal mean energies to 1e-13, gap > ε, smallest R3 within 6–10 sites of the guess's
  radius (n = 600…1200, u = 0.5…4).  A displaced inner cone is a member iff c2 ≥ u·d(s,s′)
  (enumeration n = 14); displacement is not needed.  Part 2 (bracket of remark (4) on radial
  families) still running when this was written.
* Prior art (six web searches, two abstracts through a fetch tool, one PDF fetch failed 503):
  the class in the weights is the "strong Santha–Vazirani source" of the randomness-extraction
  literature (Gavinsky–Pudlák, arXiv 1907.04640, abstract); the entropy bound is the chain rule
  (also Theorem 2(d) of `INFERENCE_LIMITS.md`: the lower end of A16.1 is already there).
  Nothing found for the energy-constrained isoperimetric lemma.  Log in the report.
