# Workstream R10 — independent review and replication of the theory division's workstream Y (a known part with interactions along the chain raises the exponents?)

*Brief written by the coordinator after checkpoint 33 (2026-11-25).  Read `COMMON.md`
first (its commit pins are out of date).  The theory tree at `658b77f` is exported
read-only at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f`.*

## What you review

`docs/workstreams/Y_REPORT.md` in the export (612 lines; code and outputs in
`experiments/workstreams/Y/`, brief in `docs/workstreams/Y_brief.md`).  The theory division
stored it "as delivered, **unverified**; nothing of it is in the theory report; cite
nothing from it until it is verified" and plans to verify it itself.  It is the first
result of the programme on a known part with *spatial* interactions (a nearest-neighbour
Gibbs measure — a Markov chain — as reference), which is what every physical chain has.
Its headline (§0.2): **a nearest-neighbour interaction without a field raises all three
exponents** — at slope `u = 1` and flip probability `p = 0.3`, `h` by 38–54 %, `a` by 14–27 %,
and the threshold almost twofold, `E ≥ E_F = ln[(1−p)cosh(u/2) + √((1−p)²sinh²(u/2) + p²)]` —
whereas interactions that are functions of the type never raise the two exponents
covered by the theory report's Corollary 11.91.  If true this matters for our physical
assessment (`docs/science/PHYSICAL_APPLICABILITY.md`): the product-measure exponents would
be *optimistic* for real chains.

## What I want, in order

1. **Replicate the numbers that carry the headline with your own code, written from the
   definitions before you open their code.**  (a) The controls at `p = ½` (the cube:
   `h = 0.0291391`, `a = 0.1109441`, `E = 0.1201145` at `u = 1`).  (b) The *lower ends* of the
   brackets for `h` and `E` at `p ∈ {0.4, 0.3, 0.2, 0.1}`, `u = 1` (they are lower bounds for
   every algorithm and every `n`, said to use only the machine-checked Theorem 11.27(b),
   elementary algebra and a numerical evaluation) — re-derive the formulas (the Lyapunov
   form for site-wise labels, §5.3; the closed form `E_F`, §5.4) and re-evaluate them.
   (c) At least one upper end (the Markov recursion of §5.1 or the tilt-state recursion
   of §5.2), re-derived and re-evaluated; say whether the discretisation is really on
   the safe side.  (d) The small-`n` exact enumerations of §7 (`n ≤ 5`): the Rényi centre is
   not a Markov chain; non-additive vertices carry weight at `p = 0.1`.
2. **Verdict per statement** of §§3–5 and §8 — proved / proved after a repair / gap /
   false — for: the reductions (U), (L), (L′) (brute-force them on small chains with your
   own code, including inhomogeneous chains and asymmetric envelopes); exact sub- and
   super-additivity of `F⁺_L`, `F⁻_L` and the sandwich; the regularised theorem (which of
   its inputs are unrefereed theorems of the theory report — list them with their
   status at `658b77f`); Propositions F and G; the Lyapunov lower bound; the threshold;
   the negative result on Markov type classes (class-wise quantiles of an admissible
   residual are not admissible: 598 of 600 cases) — reproduce one explicit example by
   hand.
3. **Is the headline what the evidence supports?**  "Raises all three exponents": for
   which `(p, u)` is each direction *proved* (lower end above the cube's value), for which
   only numerical, for which undecided (the report itself says: `u ≥ 2` undecided for
   `h`; `p ≤ 0.05` undecided)?  Is the comparison fair — same slope `u` per site, same
   accuracy convention, and is "the cube" the right baseline for a chain with flip
   probability `p` (as opposed to, e.g., the product measure with the same one-site
   marginals, which is the cube here, or the same entropy rate)?  The small-slope
   factor `(1−p)/p`: derive it independently (a susceptibility?).  Try to *refute* the
   direction at some `(p, u)` with an explicit algorithm or a better upper bound.
4. **Physical reading, kept apart from the mathematics.**  The mechanism claimed is
   "labels constant over domains of about `2K/u` sites, `K = ln((1−p)/p)`, exploit the
   cooperative response of the chain".  Is the factor `(1−p)/p` the ratio of the
   variance of the block magnetisation to that of independent sites, i.e. the
   structure factor at zero wave vector?  If so, state the conjecture for a general
   one-dimensional known part (exponents at small slope scale with the susceptibility)
   and test it on a second chain of your choice (e.g. a three-letter Potts chain or a
   chain with a next-nearest-neighbour term) at small size.  Say what it would mean for
   a helix–coil chain near its transition (our addendum A14 in
   `docs/science/INFERENCE_LIMITS_ADDENDA.md` has a Zimm–Bragg example).
5. **Prior art, briefly, with reading levels**: large-deviation / Rényi-capacity
   statements for Markov sources; "moment Lyapunov exponents of products of random
   matrices" as rate functions; do not cite what you did not open.

## Rules

Write only in `experiments/science/ws_R10/` (create it) and
`docs/science/workstreams/R10_REPORT.md`.  No state-changing git command; the export is
read-only.  Own code first; their code may be read afterwards and run from a scratch
copy for comparison (say which numbers are re-runs and which are replications).  Keep
`NOTES.md` from the first minute.  The report starts with "How far I got" and a verdict
table and ends with "What I did not check".  Classify findings (critical / major /
minor); give replacement texts; write the requests you would send to the theory
division so that they can be sent as they stand.
