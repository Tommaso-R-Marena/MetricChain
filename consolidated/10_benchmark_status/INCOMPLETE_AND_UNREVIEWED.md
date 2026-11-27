# Incomplete, unreviewed and unfinished items at the halt

*Written for the archive on 2026-11-27 from each division's own statement of its state at the halt
(the last section of its consolidation report, and its handoff and obligation files).  Recorded
separately, as the research owner asked, so that no item of the archive is read as more finished than
its authors say.  Nothing was completed, reviewed or re-run for this file, and no division was restarted
to supply missing material.  Paths are relative to `consolidated/`.  The entries about engineering's jobs
M-016 and M-021 (§2, §3, §6) were rewritten at the final refresh of the same day; the other seven
divisions had pushed nothing in between, so their entries stand as written.*

## 1. Subagent investigations that ended unfinished or were never reviewed

| division | item | state (theirs) | where |
|---|---|---|---|
| engineering | independent checker of partition-function certificates (X-018) | written and run by a subagent; findings F1–F9; "campaign for claim Z5 written and **not run**; checker not read by the coordinator" (982 lines); finding F1 reproduced directly by the coordinator | `02_engineering/experiments/eng/sb_zcheck/REPORT.md` |
| engineering | GEOMETRY-REQ-0006 (X-019) | "certified by a subagent; reproduction checked; core not read" (956 trusted lines) | `02_engineering/experiments/eng/geometry_req6/REPORT.md` |
| engineering | producer benchmark for leaf certificates | "subagent; tests pass; **report not reviewed**" | `02_engineering/experiments/eng/leafcert_bench/REPORT.md` |
| engineering | numerical check of the rate of the level recursion (theory's Theorem R) | "subagent; limit reproduced; four numerical discrepancies and a site where hypothesis (H1) fails; **coordinator's review incomplete**" | `02_engineering/experiments/eng/level_rate/REPORT.md` |
| science | referee R29 on Theorem 11.58e (`SCI-REV-0030`) | "wound down on the coordinator's order when the directive arrived, handed back incomplete and is published as such"; "re-checked by nobody" | `03_scientific_translation/docs/science/workstreams/R29_REPORT.md` |
| science | the referee for addenda A17 (13)–(16) (workstream R14) | "terminated within two minutes by a platform safeguard …, before any review"; "its work was not done by anyone"; the brief stands without a report, and parts (13)–(18) remain unrefereed | `03_scientific_translation/docs/science/workstreams/R14_brief.md`; report §B1, §G |
| ensemble | internal review ER4 | "stopped at the directive; what it did not finish is listed in its §7 and in `OPEN_OBLIGATIONS.md` OB32" | `04_ensemble_identifiability/docs/ensemble/reviews/ER4_internal_review.md` |
| complexity | sixth review (COMPLEXITY-REV-0006) | "asked to wrap up, reported, and was stopped"; sixteen findings, all with a disposition; two remedies not carried out (below) | `06_biological_complexity/docs/collaboration/messages/complexity/COMPLEXITY-REV-0006.md` |
| frontier | prior-art search on proof logging for cost-function-network solvers | "cancelled by the halt" | report §B1 |

## 2. Statements that no reviewer has read

| division | unreviewed (theirs) | source |
|---|---|---|
| theory | workstream I (Proposition 11.124, Conjecture I6): "the coordinator's own, **unrefereed**, one day old"; the algorithmic upper bounds are paper proofs, "not machine-checked" | report §B5, §B1 |
| science | addenda A17 parts (13)–(18) and (23)–(24) (except one inequality machine-checked by theory); measurements B3 (i)–(iii) "author-only or one workstream, two numbers re-run" | report §B1, §B3 |
| ensemble | "E23.1, E27–E32, E17.2, E20e, E4.1 beyond its machine-checked inequality, E15U beyond its main statement, E17.1, E22, two constants of E20″" | report §G |
| geometry | `ENSEMBLE_RIGIDITY.md` §6.2 ("has had no outside reader"); `LABEL_PATTERNS.md` and `ROBUST_DEMIXING.md` ("unreviewed"); Theorem K and Proposition L₀ | report §B2–§B5 |
| complexity | "CX-T35, T36 (certified brackets), CX-T25 (interpolation bound), Proposition 11 of the Ising note" | report §G |
| structural biology | the repaired checkers (commit `0e934eb`): "Tested, not verified, and not yet attacked again by an independent reviewer"; the Lean file "not reviewed by the theory division"; model v2 not reviewed by science | report "State at the halt", §B4; science report §G |
| frontier | the pilot is "**Not replicated**: the request to engineering (FRONTIER-REQ-0001) was unanswered at the halt"; several literature rows "at snippet or memory level" | report §B1, "Not ranked" |
| engineering | the `mincert` checker and its tests: "the coordinator's own; unrefereed"; the type-class computation "was not refereed"; subagent results as in §1 | report §B1, §B3 |
| engineering | the addendum on the rows collected after the halt: "**Unrefereed**: no referee of this division or of any other has read it, and the coordinator who wrote it also ran the jobs"; its integrity check recomputes only the first two nested levels of each cell | `02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md` (head, §2) |

## 3. Computations that are incomplete

| division | item | state | source |
|---|---|---|---|
| engineering | Modal job M-016, one cell: the certified bound at `u = 1`, `n = 32 000`, family "wide" | "**The cell has no row and no partial result, and it was not restarted.**"  Its task was restarted by the platform and its run stopped on 2026-11-27 at 18:24 UTC before it could return; "one task of twelve hours on one core with 4 GiB (about $0.95) would have to be authorised and launched again".  Consequence: at `n = 32 000` every table has one family, and that row "is not comparable with its neighbours" | `02_engineering/docs/engineering/benchmarks/X-011_ADDENDUM.md` §1; [`COMPUTE_AND_MODAL.md`](COMPUTE_AND_MODAL.md) §5 |
| engineering | Modal jobs M-016 and M-021, the searches | 20 of the 33 stored cells "end with a search that ran into its time limit"; such a number is "a valid bound of the formula, an upper bound of the minimum over the family, and **not reproducible to the digit**".  Hypotheses H1 and H13(b) are therefore not decided at `n ≥ 32 000`, and "how many levels pay" is not determined above `n = 16 000` at slope 1, above `4000` at slope ½, or at any size at slope 2 | same, §§2, 5, 6 |
| engineering | the fit `excess = c·n^γ` named in hypothesis H2 of its protocol | "was not reported in ENG-RES-0015 and is not computed here — a deviation from the protocol" | same, §5; `02_engineering/docs/engineering/benchmarks/protocols/BM-1_X-011.md`, "Deviations" |
| engineering | worst-case searches at `n ≤ 500` | "documented as not converged to `10⁻⁴·na`" | report §B2 |
| engineering | the off-lattice chain | "in floating point and on hold until it is done in exact arithmetic" | report §B3 |
| structural biology | SB-X-006 (well gaps) | "complete for five structures (… ubiquitin not run)" | commit subject `f2a02a1`; `07_structural_biology/docs/structural_biology/RESULTS.md` R-10 |
| structural biology | certified `ln Z` on larger proteins | stops at about the size of crambin | report §C item 6 |
| complexity | six-leaf survey of networks beyond level 2 | "not exhaustive even at its own levels"; a re-run with a complete canonical form "not done: a code change and about 90 minutes of computation" | report §C, §G item 4 |
| complexity | Corollary 5 of the chain note | "**Open:** read the two sources" | report §G item 1 |
| ensemble | stored outputs of the check scripts | "A full re-run of all scripts was not repeated after the last changes of text" | report §G |
| ensemble | E20e (thirteen states on `𝕋⁴`) | 26 of 40 random configurations identified, 10 not, "4 undecided"; "no exact instance" | report §B1 |
| geometry | proof obligation O-19 | "planned and not started" | report §A |
| frontier | comparison of FRONTIER-FRZ-0003 with the official CASP17 numbers | "pending: … needs the owner's authorisation"; scheduled session paused | report §B3, §G |
| frontier | rows with virtual arc consistency in the toulbar2 ablation | "dropped (the run did not return)" | report §B1 |
| science | untracked caches of `ws_P3`/`ws_P6` and referees' data files | not in the repository; "all regenerable; each report says how" | report §G |

## 4. Work recorded as owed or not started

| division | item | source |
|---|---|---|
| science | "the review of the Structural Biology division's model v2; items 1 (a), 1 (b), 3, 5 of FRONTIER-REQ-0002; Stage 2 of the certificate; a re-check of referee R29's findings; the reading of ENG-RES-0015/-0016/-0018, ENSEMBLE-RES-0007/-0008 and ENSEMBLE-MSG-0009, GEOMETRY-MSG-0010 and the Geometry division's thirteenth checkpoint, COMPLEXITY-RES-0010, STRUCTBIO-REV-0001, the Frontier protocols" | report §G |
| engineering | the held-out benchmark, the proof-logging comparison and the long `ln Z` runs ("reviewed, not started"); requests of the theory and science divisions not started (listed with decisions in `02_engineering/docs/collaboration/status/engineering.md`); nothing of the other branches read after the heads fetched at 2026-11-27 00:24 UTC | report §H; `ENG-MSG-0008` header |
| structural biology | a freeze record for the held-out evaluation ("**not issued**"); a standalone format note for a second checker ("**not written**"); the ratio-form population bound ("specified in HANDOFF"); capabilities C3 (ensemble identification), C4 (geometric observability) "not started"; C5 "blocked on constants nobody can certify for a real energy" | report §C item 8, §E |
| frontier | the two evaluations on validation data and the per-division request messages ("cancelled before starting"); one agreed selection rule for the held-out list (IR-14) | report §G, §B2 |
| theory | the four "strongest unresolved problems"; machine-checking of the upper bounds is listed under "deprioritise" | report "State at the halt", §C |
| complexity | "E-C1 for `K ≫ log n`; #P-hardness at a fixed temperature; fixed-parameter tractability in the number of species; … the Theory division's open problem 1 (never started)" | report §G |
| geometry | Conjecture 6.3; Conjecture P; the threshold of Theorem C for all `K` | report §B1, §B2, §B4 |
| ensemble | Problem O4 (the chimera gap); conjectures C2, C3 | report §B2, §B5 |

## 5. Messages published at or after the halt that their addressees did not read

Listed mechanically in `09_cross_divisional_dependencies/README.md` §3.8; the three with content that
bears on another division's results are discussed there in §§3.1–3.3.

## 6. Processes

Every division states that nothing of its own was running after its consolidation commit, with two
exceptions that were recorded rather than hidden.  (1) The engineering division's two Modal jobs and the
local watcher that waited for them: **both ended on 2026-11-27** — the last run was stopped at 18:24 UTC,
the watcher exited by itself at 18:32 UTC, and the ledger's final reconciliation records no job running
or queued (`COMPUTE_AND_MODAL.md` §3a, §5).  (2) The frontier division's scheduled check-in of 2026-11-30,
which it "paused, not deleted" — unchanged, by that division's report; not verified by anyone else.
