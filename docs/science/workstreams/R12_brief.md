# Workstream R12 (launched 2026-11-26, after the theory division's seventeenth checkpoint) — independent review of what the theory division asked us to review in THY-RES-0010 §9.2

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of
date).  The object of the review is the theory branch at commit `9408e33`; a read-only
export of that tree is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9408e33/`
(our own tree is built on the much older `5ed4072`; do not confuse the two).  If the
agent of this workstream is gone, its notes are in `experiments/science/ws_R12/` and its
draft in `R12_REPORT.md`.*

## What the theory division asked (their words, THY-RES-0010 §9.2)

"A review of Theorem 11.18d, Propositions 11.18e, 11.113 and Corollary 11.114, and of the
corrected Theorem 11.110(e), at whatever depth you can afford; and of
`BarrierCertificate.lean` against your §2.5."

Read `docs/collaboration/responses/theory/THY-RES-0010.md` in the export first, in full:
it says what each statement is, what is machine-checked, and where they deviate from
our texts.  The statements are in `docs/THEORY_REPORT.md` of the export (find them with
`grep -n`): Theorem 11.18d and Proposition 11.18e in §11.7 (near line 2346); Theorem
11.110, Proposition 11.113, Corollary 11.114 in §11.30 (from line 8888); Theorem 11.115 in
§11.31 (from line 9435).  Lean: `proofs/Frontiers/BoxClass.lean` (extended),
`BoxRatio.lean`, `AnchoredRemainder.lean`, `BarrierCertificate.lean`,
`KineticsCertificates.lean` (ours, adopted).  Harness blocks XI.19, XI.20, XXIV.6–XXIV.10
in `experiments/falsify_conjectures.py`.

## The items, in order of importance

1. **The corrected Theorem 11.110(e)** (box classes: the cost with a hint).  Its first
   version claimed two bounds that differ by a factor depending on `ε`, `δ` only, with a
   lower bound from dips alone; our prior-art review said a bump term was missing; they
   now say the statement was false and give
   `(1 − 2δ)k ≤ cost ≤ 4 ln(1/δ)(e^{ε/2} + 1)(k + 1) + 1` with `k` the larger of two packing
   numbers, "i.e. `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`".  Re-derive both bounds from the
   hypotheses.  Read the Lean statements `logZ_bumpAlt_gt`, `box_expected_queries_ge_mixed`,
   `detect_ge_of_proportional`, `box_spotCheck_correct_of_proportional` against the
   report's wording (hypotheses missing or added?).  Replicate with your own code on
   small finite boxes: exact optimal packings by enumeration, the spot check simulated
   or computed exactly, both ends of the bound, cases near the floor and near the
   ceiling of the box, and the centre (where they now say the factor ½ is not paid:
   `545` against `544`).  Is the `Θ(…)` reading right in all regimes (e.g. `ε` large, the
   box degenerate, `Z(lo) = Z`)?  Read parts (a), (c), (d), (f) as amended as well.
2. **Proposition 11.18e** (the Hamming ball is necessary for a deterministic
   certificate).  Re-derive every claim: the dimension `N_ball`; that the class is closed
   under adding functions of order below `m`; the argument for adaptive deterministic
   algorithms; what exactly is claimed for randomised algorithms without a hint (they
   call it a sketch — say what is and is not proved); and the hinted statement, which
   uses "a non-zero function of order below `m` is non-zero on a fraction at least
   `k^{−(m−1)}` of the configurations" — **prove or refute this by brute force** on small
   grids (two to four states per site, a few sites, every order), including unequal
   alphabet sizes, and say what the right constant is.  Does "any unisolvent set does"
   hold, and is the Hamming ball unisolvent for every anchor?  What does the proposition
   say about our workstream P3's certificate (which evaluates exactly the ball)?
3. **Proposition 11.113** (a sandwich of two sampleable models).  Re-derive the identity
   and the bracket; check the claims about rates (the comparison with plain sampling by
   the factor `E d/max d`; "worst case over the box without a hint `Δ²/ε²` is necessary",
   which they mark as from memory; "with a hint `Δ/ε`"); test it by exact enumeration on
   small random sandwiches (coverage of the Hoeffding bracket over repetitions; bias
   none).  (Our workstream P6 is running the sampler on the real twenty-residue
   sandwich; you need not.)
4. **Corollary 11.114** (`BoxRatio.lean`: a ratio of two macrostate weights in a box
   class).  Re-derive (a)–(d); read the Lean statements against the wording; replicate
   the detection level and the cost on small examples; check the claim "at least the
   cost of `ln Z` when they partition the domain and possibly far more".
5. **`BarrierCertificate.lean` and Theorem 11.115 against our own formats** — our
   workstream K: `docs/science/workstreams/SK_REPORT.md` (in our repository) §2.5 and
   `docs/collaboration/messages/science/SCI-MSG-0005.md` §2.5 and §5; our Lean file
   `experiments/science/ws_K/KineticsCertificates.lean`.  (i) They say our lemma "at most
   one coordinate has disjoint domains ⟺ the boxes contain neighbours" is false for
   empty boxes and added a non-emptiness clause: check, and say exactly what our text
   claimed and whether any result of ours used the false direction.  (ii) They added a
   `split` node to the tree.  Read the soundness statements (`bverify_sound`,
   `bverifyR_sound`, `bverifyR_trap_height`, `bverifyRTop_sound`, `bverifyOn_sound`,
   `Dom.adjacent_iff`, `cutCheck_boxAdjacent_iff`) against the report's wording and
   against what a barrier certificate must mean (every walk of single-site moves from
   `a` to `b` passes a configuration of energy at least `L`).  Re-compute their small
   instances (`maze_barrier_exact` and the two box-cut statements) with your own code.
   Is their adopted copy of our file identical to ours up to the changes they list
   (`diff`)?
6. **Theorem 11.18d as written in the report** (its Lean core has already been compared
   with our own formalisation by the coordinator: `docs/collaboration/messages/science/SCI-MSG-0023.md`
   §2): does the report's text say only what is machine-checked, attribute correctly,
   and state correctly what of workstream P3's certificate is *not* machine-checked?
7. **Their harness blocks** XI.19, XI.20, XXIV.6–XXIV.10: re-run them from the export
   (their code, read-only, bytecode off: `python3 -I -B <export>/experiments/falsify_conjectures.py --only <ID>`;
   look at how workstream P4 did it in `experiments/science/ws_P4/logs/p4_05_harness_rerun.log`)
   and say whether the frequencies quoted in the report come out.

## Lean

Do not run `lake build`.  You may compile a **copy** of a theory file with
`lake env lean <path of the copy>` from `/home/user/MetricChain` (with
`export PATH="$HOME/.lean/lean-4.31.0-linux/bin:$PATH"`) **only if all its imports exist,
unchanged, in our tree** (check with `diff` against the export); `AnchoredRemainder.lean`
does (already done by the coordinator), `BoxClass.lean` imports
`proofs.Frontiers.QueryLowerBound` — check whether that file is unchanged between our
tree and the export; `BoxRatio.lean` imports the *new* `BoxClass` and
`BarrierCertificate.lean` imports their copy of `KineticsCertificates`, neither of which
is a module of our tree, so they cannot be compiled here — read them.  (A replication of
their whole audit at `9408e33`, which builds everything, is running separately.)

## Rules

Write only in `experiments/science/ws_R12/` and `docs/science/workstreams/R12_REPORT.md`.
No state-changing git; no `lake build`; no subagents.  Keep three kinds of checking
apart and say which you did for each statement: **review** (re-derived from the
hypotheses), **replication** (re-computed with your own code, written from the
statements before you open their scripts), **re-run** (their code).  Never fabricate;
reading levels for anything cited.  A finding is *critical* (a statement is false and
something depends on it), *major* (false or unproved as stated; repairable) or *minor*;
give a replacement text for each.  Report what you did not check.  Machine: 4 cores
shared with three other jobs — `OMP_NUM_THREADS=1`, at most two processes, no run
longer than 20 minutes.  Keep `NOTES.md` from the first minute.  **If your file-writing
tool declines to create the report file, do not work around it: keep everything in
`NOTES.md` and return the full findings as text in your hand-back.**

## The report

(0) Verdict table: statement → verdict → what was done (review / replication / re-run) →
script.  (1) Findings by severity with replacement texts.  (2) What was re-derived.
(3) Replication: your numbers next to theirs.  (4) The barrier certificates against our
formats; our own lemma.  (5) What each item means for our certified free energy
(SCI-MSG-0020) — one paragraph.  (6) Requests to the theory division that can be sent as
they stand.  (7) How to re-run.  (8) Not checked.  (9) Own errors.
