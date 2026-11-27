# Workstream R4 — independent review SCI-REV-0003: theory report §11.24 (rounds of adaptivity)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R4/`; your report: `docs/science/workstreams/R4_REPORT.md`.

## The object under review

Theory report §11.24 (commit `5ed4072`; `grep -n '^### 11.24' docs/THEORY_REPORT.md`), about 220
lines, and the workstream report behind it, `docs/workstreams/U_REPORT.md`, with code in
`experiments/workstreams/U/` and the coordinator's re-computations in
`experiments/coordinator_checks/rounds_U/`.  Lean: `proofs/Frontiers/TwoRounds.lean`
(`card_distinguished_le`, `two_round_bound`).  Background you need: §11.16 (non-adaptive
exponent), §11.18–11.19 (the nested "layer-cake" algorithm, Theorems 11.52–11.58; the
exponents `a = KL(p_u‖½)`, `h = KL(Λ₁/u‖½)`), `docs/DEAD_ENDS.md` D45 and D50, referee reports
`docs/reviews/R7_referee_report.md`, `R8_referee_report.md` (for what was already checked about
the algorithm).

Claims (read the exact statements): Theorem 11.84 (batching: a ladder with `L` rungs is `L`
rounds; `k` levels need `L^{k−1}` rounds independently of `n`; round-limited exponents `τ^{(r)}`
decrease to `h`); the two-round upper bound `τ^{(2)} ≤ T^{(2)}(0)` (golden ratio times `a` at small
slopes; `0.624a` at `u = 1`); Lemma 11.85 (indistinguishability for block-radial functions
with hidden centres) and the two-round lower bound `τ^{(2)} ≥ θ₂*(u) > h` (`0.359a = 1.37h` at
`u = 1`), with hard instances in which a flat-histogram structure in one block dilutes the
first batch; radial instances need exactly two rounds; three rounds open.  Status claimed:
"paper proofs by workstream U, checked against the proof of Theorem 11.56 and re-computed by
the coordinator; the two-round indistinguishability lemma machine-checked; **unrefereed**".

You are the first independent referee of this section.

## What a review here means

1. **The lower bound is the new mathematics; start there.**  Restate Lemma 11.85 and the
   two-round theorem with all quantifiers (what is a "round" — may the second batch depend
   on *values* from the first, on internal randomness, on both? is the number of
   evaluations per round bounded or only the total? expected or worst case?).  Re-derive the
   indistinguishability argument yourself.  Check that the pair of hard instances is in the
   class (Lipschitz in Hamming distance with the stated constant), that their `ln Z` differ by
   more than `2ε` in the stated accuracy regime, and that the claimed exponent `θ₂*(u)` is what
   the argument yields (re-compute `θ₂*(1)` and the ratio to `a` and `h` with your own code).
2. **Lean match.**  Read `TwoRounds.lean`: what exactly do `card_distinguished_le` and
   `two_round_bound` state?  Is the gap between the abstract machine-checked lemma and its
   application to the "twins" (a paper step) filled convincingly?  Any vacuity?
3. **The upper bound.**  Is the batched schedule really non-adaptive within a round (no
   evaluation in a round depends on another evaluation of the same round)?  The claim "the
   candidate set of a rung is computed from empirical levels of the previous one and is
   polynomially many times `e^{x_{l−1}}` points, deterministically" — check against the
   algorithm as written in §11.18–11.19.  Re-compute `T^{(2)}(0)/a` at `u = 1` and the small-slope
   limit.
4. **Simulate** the two-round claim at small sizes if you can find a meaningful test (e.g.
   exact computation of the probability that a first blind batch of `M` points distinguishes
   the twins, against Lemma 11.85's bound).
5. **Headline vs theorem**: the README says "two rounds provably do not reach the adaptive
   exponent — at slope 1 their exponent lies between `0.359a` and `0.624a`, where a fixed sample
   costs `a` and full adaptivity `0.263a`".  Exactly which accuracy regime, which algorithm
   class, which parts proved, which numerical?
6. **Originality** in one paragraph (workstream A1 does the deep search): round hierarchies
   in query complexity of estimation problems.

## Deliverable

`R4_REPORT.md` in the review format: claim examined; verification method; evidence inspected;
established findings; limitations; **critical / major / minor findings** (numbered, with
location, what is wrong, why it matters, suggested correction); originality assessment;
reproduction status; recommended corrective action; unresolved questions.  If you find a real
error, give the strongest true statement you can prove in its place.
