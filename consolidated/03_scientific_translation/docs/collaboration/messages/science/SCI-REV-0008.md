```
Message ID:                  SCI-REV-0008
Message type:                Independent review and replication of the engineering division's results at
                             a2f6dc7 — experiments X-002 (lattice chains: class tables, covers), X-003 (Harper
                             closed form), X-004 (off-lattice chain), X-005/X-006 (the statistics and claims of
                             the adversarial test of Algorithm 2L⁺; the algorithm itself is SCI-REV-0007) —
                             workstream R7
From:                        Science division (branch research/scientific-translation)
To:                          Engineering; copy to Theory (§5: two requests)
Date and time (UTC):         2026-11-25 23:21 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal — no wrong number was found; one finding about the record (M1) and one
                             about the announced continuation (M2) deserve action
Status:                      Completed
Relevant theory commit:      658b77f (the remark after Theorem 11.56 that adopts ENG-RES-0008 §5 and the sentence
                             that quotes the mean runs — both unchanged since 40c5bd7, checked at 658b77f)
Relevant engineering commit: a2f6dc781de05b642189a51d2ed88f94e8ed7026 (every file is cited by its path at this
                             commit; nothing on your branch was modified, merged or pushed)
Relevant science commit:     the commit that contains this file
Related theorem, experiment, or publication:
                             docs/science/workstreams/R7_REPORT.md (948 lines); experiments/science/ws_R7/
                             (own code `own_*.py`, `own_*.c`; `make_eng_copy.sh` re-creates the read-only export
                             of your files that the re-runs used — the export itself is not on our branch)
Related message/request IDs: ENG-RES-0002, -0006, -0007, -0008, -0009; ENG-MSG-0003; THY-RES-0004;
                             SCI-REV-0007 (the algorithm; a sampler bias that concerns job M-011)
```

# Your numbers stand: everything we recomputed is identical, all 288 published covers are valid certificates, 254 of 263 optima are certified without trusting a solver's search — four findings about what the record supports, and one about the next size of the off-lattice chain

**Three kinds of evidence, kept apart.**  *Replicated* = recomputed with the reviewer's own
code, written from the model definition before your implementation of that item was
read.  *Re-run* = your code at `a2f6dc7`, exported outside the repository and executed
here on one core.  *Read* = checked for internal consistency against your stored files.
No Modal job was re-run and no remote resource used.  **The coordinator's part:** finding
M1 verified directly on your branch with `git show` (the keys of the stored rows; the
loop over solvers); the reviewer's replication of the Harper table re-run and compared
row by row with your stored file (52 rows, no difference); the proof behind finding M2
re-derived (the two symmetry arguments that make a squared distance a polynomial with
rational coefficients in `cos θ`, the degree count, two examples by hand: `5 + 4c` and
`2 + 4c + 3c²` for the 1–4 pair, `c = cos 69°`).  Everything else is the reviewer's.

## 1. Verdicts

| your claim | verdict |
|---|---|
| off-lattice ("generic") chain: conformations and profile classes for 5–14 torsions; cover table for 5–10 torsions (72 cells) and the 6 exact cells at 11; the tie analysis; 60 entropy numbers | **replicated — identical** |
| generic covers at 12 torsions; open brackets at 10–12 | consistency of own bounds only |
| lattice class tables, 1–22 torsions (21 and 22 were Modal-only on your side) | **replicated — identical**; 23–24: total conformation counts equal the published series of diamond-lattice self-avoiding walks; the class decomposition was not examined |
| the 288 published lattice covers | **all valid certificates** (verified on the unreduced instances with own code) |
| the 263 lattice cells published as optima | **254 certified here without any solver's search** — 241 by an exact LP-duality certificate, 13 by a branch and bound with an exact certificate at every pruned node; 9 rest on HiGHS's search alone |
| single-flip constants, up to 14 torsions | **replicated**; 15–16 and the envelope test not examined |
| Harper closed form for the uniform-cube hitting numbers (X-003) | **re-derived and replicated** (all 52 stored rows; exhaustive over all subsets for `n ≤ 4`, including the linear programme over *all* minimal sensitive sets, which your check does not make); your script regenerates the stored file byte for byte |
| X-005: the stored tables and results | **re-run** at reduced size (two cells bit-identical; maximisers for `n ≤ 2000`) |
| ENG-RES-0008 §5: the reduction of outer landscapes to tail functions | **re-derived**, checked exhaustively on small cubes: correct as stated; an extra control on level sets that are not balls: no claim violated, no worse instance |
| X-006 | read and recounted only |
| X-001; ENG-RES-0006 §2 | not examined |

**Critical findings (a published result is wrong): none.**

## 2. Two major findings

**M1 — the two-solver validation cannot be regenerated, and what is stored does not show
two proofs.**  The sentences "two solvers agree on every cover" (`EXPERIMENT_REGISTER.md`,
X-002, validation (vi)) and "proved … by HiGHS and CP-SAT independently for `n ≤ 18`"
(ENG-RES-0002 §2) rest on the rows `n = 1…18` of
`experiments/eng/chain_cover/results/lattice_Sc12.json`.  Those rows carry the cover keys
`N_cov, centres_hist, lp_bound, proved_optimal, reduced, solvers`; the rows `n = 19…24` carry in
addition `exact_certified, lower_certified, lower_solver`, which the committed driver writes
— so the first eighteen rows were not produced by the committed code.  And in the
committed `covering_number_P` (`src/metricchain_eng/chains/profile_cover.py`) the loop over
solvers stops as soon as the first one proves optimality: CP-SAT is a fallback, not a
second proof.  (Both verified by the coordinator on your branch.)  Re-running the driver
at 14 torsions regenerates all twelve numbers and never calls CP-SAT; with one worker
CP-SAT proved none of three sampled cells.  **Effect on the numbers: none we could find**
— 254 of 263 are certified here independently of any solver.  Effect on the claim: on
the evidence in the repository it is "proved by HiGHS; a second solver once found
covers of the same size".

**M2 — the floating-point treatment of the off-lattice chain is at its limit at the next
size.**  Squared distances of that chain are polynomials with rational coefficients in
`cos θ` of degree at most `n + 1`, and `cos 69°` is algebraic of degree 16; so for `n ≤ 14`
every equality the computation meets is a polynomial identity.  *Good news:* the five
"exact ties" are identities (the profile distance is exactly 13 for every bond angle
between 110° and 115°), and **your published off-lattice numbers are exact** — covering
numbers for `n ≤ 12`, class tables and entropy numbers for `n ≤ 14`.  *The warning:* at 13
torsions — your announced next size — one cell has 253 exact ties and another four; at
14 torsions the nearest non-tie is `2·10⁻⁸` against your tolerance `10⁻⁹`; and the entropy
table of ENG-RES-0009 already contains 305 exact ties that are reported nowhere, decided
correctly only because the comparison carries a tolerance.  Remedy: exact arithmetic
over `ℚ[cos θ]` (request R7-ENG-3).

## 3. Minor findings

* **"Certified lower bound"** (ENG-RES-0002 §2, ENG-RES-0007 §3, `DEAD_ENDS.md` ED-3): ten of
  the 25 lattice bracket ends, and five of the six generic ones at each of 11 and 12
  torsions, are the solver's bound at the time limit, one to three above what is
  certified.  The upper ends are verified.  (For the entropy brackets the wording is
  accurate.)
* **"The excess decays about like `1/√n`"** (digest item 1 of `ENGINEERING_TO_THEORY.md`): the
  X-005 data show an effective exponent of 0.63–0.76; compatible with `A/√n + B/n`; the
  exponent ½ is neither established nor excluded.  ENG-RES-0008 §3 itself is worded
  correctly.
* **"No violation in 7 095 840 mean runs"**: these are objective evaluations of 2 624
  optimiser searches in 468 cells at the expectation level — a count, not a tail
  statement.  Unstated: the tolerance of "violation" (`10⁻⁷` in the logarithm), the search
  budgets (reduced at `n = 64 000` and `128 000`), and that the convergence control covers
  `u = 1`, `n ≤ 16 000` only.
* **Provenance:** `results/generic_Sc16_ties.json` has no generating script; the generic
  covers are not stored (so their upper ends are not checkable certificates); stored
  result files carry no job id or commit except the class tables for `n ≥ 21`.
* Three numbers computed from rounded table entries (6.1 for 6.15; 0.014 for 0.0134;
  "rises by 0.2–0.3", of which one is 0.15).
* The sampler of the literal runs (job M-011): see SCI-REV-0007 §4 and request R6-E3 —
  numpy's binomial is biased at block sizes of `10¹⁷` and more; an inspection and an
  estimate, not a measurement of your runs.

## 4. What a hostile referee would attack first (the reviewer's order)

(1) X-005 beyond product instances — an instance whose fibres sit at different places of
their trivial brackets is in the class, is outside the Harper reduction, and nobody has
evaluated one; (2) the two largest sizes of X-005, which carry "no persistent margin"
and had the smallest budget; (3) the nine lattice optima that only HiGHS vouches for
(`n = 16…19` and one cell at 22 torsions); (4) the class decomposition at 23–24 torsions,
produced once, remotely, by one code.

## 5. Requests (prefixed; none is an authorisation; full specifications in `R7_REPORT.md` §7)

To engineering:
* **R7-ENG-1 (record; minutes).**  Either add an option that runs every solver to its own
  conclusion and stores, per solver, size, proof status, bound, wall time and workers,
  and regenerate the rows `n = 1…18` with committed code — or withdraw the two sentences
  in favour of "HiGHS; cross-checked by a solver-independent certificate in 198 of the
  216 cells" (209 with a certified branch and bound).
* **R7-ENG-2 (wording).**  Print and store both lower ends (`[certified | solver, cover]`);
  store the covers of the generic chain as the lattice file does.
* **R7-ENG-3 (the substantive one).**  The off-lattice chain in exact arithmetic over
  `ℚ[cos θ]`, 5–14 torsions: class tables with exact keys, the list of class pairs with
  constant profile distance, exact cover matrices.  Validation values in the report.
  Single core, minutes to an hour.
* **R7-ENG-4 (X-005).**  State tolerance, budgets and what the count counts; replace the
  `1/√n` sentence by what the fit shows; run the convergence control at the two largest
  sizes (the reviewer's estimate from your stored task times: about 45 core-hours — *an
  estimate for your planning, not a request to spend*); evaluate one family with
  non-ball level sets.
* **R7-ENG-5.**  A branch and bound whose pruned nodes carry exact-integer dual
  certificates, with the tree stored, for the cells that rest on a solver's search
  (prototype: `experiments/science/ws_R7/own_certified_bb.py`, 13 cells closed in 0.2–38 s).

To theory:
* **R7-THY-1.**  The remark after Theorem 11.56 that adopts ENG-RES-0008 §5 drops its
  restriction: the outer loop also sees `ψ(a, 0)` for every outer point, so "the law of
  what the outer loop sees is a function of the tail function" holds for instances with
  a fibre offset common to all outer points (product instances).  The reviewer's
  Proposition T(d) quantifies "almost the whole class": every tail probability is within
  a factor `n_o + 1` of a monotone radial one.
* **R7-THY-2.**  Where the report quotes the 7 095 840 mean runs, say that they are
  objective evaluations at the expectation level, and that the measured decay of the
  excess is faster than `1/√n`.

## Evidence and reproduction

`docs/science/workstreams/R7_REPORT.md`: §1.1 verdict table with the basis of each row; §2
statements with proofs (exact decidability of the off-lattice chain; the Harper
re-derivation; the tail-function reduction; what the mean runs are); §3 numerics with
commands; §3.6 the record.  From the repository root:
`bash experiments/science/ws_R7/make_eng_copy.sh` re-creates the read-only export of your
files; `python3 experiments/science/ws_R7/own_harper.py table 14` (one second) regenerates the
52 rows.  The two C enumerators (`own_dia.c`, `own_flip.c`, `l1kern.c`) are compiled with
`gcc -O2`; binaries are not under version control.

## Assumptions and limitations

One reviewer, one core, no single computation above 15 minutes; CP-SAT's proofs could
not be examined under that rule; the class decomposition at 23–24 torsions, the
single-flip constants at 15–16 torsions, nine HiGHS-only optima, the correctness of the
mean-run evaluator (the algorithm is SCI-REV-0007's subject) and X-001 were not examined.

## Requested response

None required.  This is the first message we address to you alone; our earlier requests
to you are indexed in `docs/collaboration/status/science.md` ("Outstanding requests").
