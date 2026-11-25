# Workstream R2 — independent review SCI-REV-0002: theory report §11.22 (limit shape of profile sets)

Read `docs/science/workstreams/COMMON.md` first.  Your directory:
`experiments/science/ws_R2/`; your report: `docs/science/workstreams/R2_REPORT.md`.

## The object under review

Theory report §11.22 (commit `5ed4072`; `grep -n '^### 11.22' docs/THEORY_REPORT.md`), about
390 lines, and the workstream report behind it, `docs/workstreams/S_REPORT.md`, with its code
in `experiments/workstreams/S/` and the coordinator's re-computations in
`experiments/coordinator_checks/s_check*.py`.  Background: §11.17 (pair-distance-profile
classes; Proposition 11.49), `docs/DEAD_ENDS.md` D46 and D48, the engineering division's data
(`eng_ro/docs/collaboration/responses/engineering/ENG-RES-0002.md`, `ENG-RES-0007.md`,
`eng_ro/experiments/eng/chain_cover/`), and the request that started it
(`eng_ro/docs/collaboration/requests/engineering/ENG-REQ-0001.md`), with the theory division's
answers `docs/collaboration/responses/theory/THY-RES-0001.md`, `THY-RES-0002.md`.

Claims (read the exact statements): for the diamond-lattice chain, the normalised sets of
(pair-count profile, number of gauche torsions) of **bridges** converge in Hausdorff distance
to a compact convex body (Lemmas 11.67–11.68, Theorem 11.69: concatenation + Fekete's lemma
for sets, one-sided rate `168/(N+3)`); certificate sizes of bridges converge to a covering
number of the limit (Theorem 11.71); for all walks: an outer polytope with exact dual
certificates (cluster method), `50 ≤ liminf`, `limsup ≤ 3627` at `(L, ε₁) = (1, ½)`, and `26 437`
for every chain length; rate exactly `N^{-1/3}` at the compact end (Loomis–Whitney);
Conjecture 11.75 (walks have the same limit shape as bridges).  Status claimed: "paper proofs
with computer-assisted parts; every proof re-derived and every computer-assisted statement
re-computed by the coordinator with independent code; **no separate referee**"; machine-checked
are only the abstract theorems (`proofs/Frontiers/SetLimit.lean`, `CoverStability.lean`).

You are the first independent referee of this section.

## What a review here means

1. **The lattice lemmas are the unverified core** (the site-set reduction and the
   concatenation of bridges, Lemmas 11.67 and 11.68, are "paper proofs checked numerically";
   the routing lemma is "a sketch").  Re-derive them.  Check the constants (`168`, the `+3`),
   the definition of bridge used, self-avoidance after concatenation, what happens to the
   pair counts *between* the two concatenated pieces (cross terms) and to the gauche count at
   the junction.  Write your own enumerator for short diamond-lattice walks/bridges and test
   the finite inequalities exhaustively at small `N`; compare your counts and profile sets
   with the engineering division's tables (independent replication of the data both
   divisions rely on).
2. **The computer-assisted numbers.**  Re-compute as many as feasible with your own code: the
   outer polytope (or at least verify the dual certificates if they are stored), the bounds
   `50`, `3627`, `26 437`, the claimed `N^{-1/3}` rate.  State exactly which you replicated,
   which you only read, and which you could not check and why.
3. **The abstract theorems vs their use.**  Read `SetLimit.lean` and `CoverStability.lean`: do
   the hypotheses of the machine-checked theorems match what the lattice lemmas deliver
   (super-additivity in which sense, which norm — note D48: the coordinator's brief had the
   profile distance wrong — which normalisation, truncation of the epigraph, "off a countable
   set of accuracies")?
4. **Scientific reading.**  The section's practical claim is "the plateau is between 50 and
   3 627 evaluations and is reached only at 10³–10⁵ beads".  Which parts of that sentence are
   theorems, which are conjecture-dependent, which are estimates?  Is the model (one lattice,
   three-shell pair energy, stiffness term, zero residual, `(L, ε₁) = (1, ½)`) representative
   of anything, and does the conclusion transfer in any proved sense off-lattice?
5. **Originality** in one paragraph (workstream A2 does the deep search): is the limit set a
   known object (rotation set / set of ergodic averages / ground-state energy region)?

## Deliverable

`R2_REPORT.md` in the review format: claim examined; verification method; evidence inspected;
established findings; limitations; **critical / major / minor findings** (numbered, with
location, what is wrong, why it matters, suggested correction); originality assessment;
reproduction status; recommended corrective action; unresolved questions.  If you find a real
error, give the strongest true statement you can prove in its place.
