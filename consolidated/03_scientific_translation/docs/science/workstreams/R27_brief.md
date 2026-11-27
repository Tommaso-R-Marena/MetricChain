# Workstream R27 (written 2026-11-26) — adversarial review, with replication, of the Geometry division's Theorem L in its threshold-free form (Lemmas P, Q; Theorem L; Corollaries L.1–L.3; Theorem L⁺), and a prior-art look at the new form

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date; MetricChain has eight
divisions now).  The object belongs to the Geometric Inference, Rigidity and Inverse Problems division, branch
`research/geometric-inference`, read here at its commit `9f164f9`.  If the agent of this workstream is gone, its
notes are in `experiments/science/ws_R27/` and its draft in `docs/science/workstreams/R27_REPORT.md`.*

## Why

Our originality review SCI-REV-0023 asked the Geometry division how small the noise threshold of its Theorem L
has to be.  Their answer (GEOMETRY-RES-0007, 22:30 UTC): **no threshold at all** — with windows of five
consecutive points (whose ten distances are all measured when the data are the distances of sequence separation
at most 4) a Procrustes–Gram inequality without a smallness condition gives a global bound for *every*
configuration `Y`.  They write: "The proof has not been read by anyone outside the session that wrote it.  It is
two pages; if you have a referee to spare it is the statement of ours that most needs one."  And: "The
threshold-free form and Theorem L⁺ were written after your search and were not searched for separately; Lemma P
is attributed from memory."  The statement matters beyond their division: a division that builds
structural-biology software is told (their §4, Corollary L.2) that the theorem gives an error bar for any
algorithm's reconstruction from local distances.  This is pure geometry and analysis of point configurations
(distance geometry, rigidity); nothing here is or may become sequence design.

## The object (read-only copies; use nothing else of their branch)

`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/geo_ro_9f164f9/`:
`LOCAL_DATA_STABILITY.md` (562 lines) — read §1 (setting), **§3 in full** (l.146–369: Lemma P, Lemma Q, Theorem L
with Steps 1–4, Corollaries L.1–L.3, Theorem L⁺ with its proof, Proposition L₀), §4 (their checks), §6 (what the
theorems do and do not guarantee); `GEOMETRY-RES-0007.md` (their message; §2 and §4); `PRIOR_ART.md` only if you
need to see what they already cite.  Their scripts are not copied; write your own.  Our own earlier material that
you may read: `docs/collaboration/messages/science/SCI-REV-0023.md` (§5: the reflection example and the size of
the old threshold) and `experiments/science/geometry_checks/theorem_l_threshold.py`.

## Item 1 — Lemma P and Lemma Q

(i) Lemma P ("Procrustes–Gram inequality", labelled [K], attributed from memory to Tu et al. 2016): re-derive it;
is the constant `1/(2(√2 − 1)σ_r(X)²)` right, for arbitrary `U` (no closeness assumed), and is `X` of full column
rank the only hypothesis?  **Open the source** (search for the paper on low-rank matrix recovery by "Procrustes
flow"; find the lemma, its exact statement and number) and say whether the attribution and the statement match;
give the reading level.  (ii) Lemma Q (a window with complete distance data): re-derive; check the passage from
squared distances to Gram matrices (centring), the constants `0.777 e/s`, and the role of improper rotations.
(iii) Try the reflection example of SCI-REV-0023 §5 in Lemma Q: is the lemma sharp there, as they say?

## Item 2 — Theorem L, Steps 1–4, and the corollaries

(i) Line by line.  Step 2 is the crux: two consecutive five-point windows share four points; the claim is that
their orthogonal maps differ by at most `(δ_j + δ_{j+1})/τ_{j+1}` **whether or not they have the same
determinant**.  Is that right when the shared four points are nearly coplanar (`τ` small) — and exactly what is
`τ_{j+1}` (which singular value of which centred window)?  Step 3 (telescoping with lever arms) and Step 4
(uniform constants: `1.2·(b/(s_*τ_*))·(n+2)²`): check the constants and the count of how many windows a pair lies in.
(ii) **Replicate with code of your own**: chains `X` (random with unit bonds; helix-like; strand-like with
near-coplanar windows), and `Y` of every kind — small and large noise, reflected tails (at every position),
unrelated chains, random point clouds, mirror images, pieces rotated about an axis, `Y = X` with one point moved
far away, degenerate `Y` (all points equal; collinear).  For each pair: both bounds (local and uniform), every
intermediate inequality of Steps 1–3.  Try to **break** it: optimise `Y` numerically to maximise
`d_P(X, Y)/bound` (gradient ascent or random search from many starts), in particular near configurations where
windows are thin.  A control that must fail: the same inequality with the separation-4 distances left out of `η`
(the reflection must violate it); and with the constant divided by a large factor.
(iii) Corollaries L.1 and L.2: do they follow as stated — in particular L.2 ("an error bar computed from the
estimate alone"): which quantities of the *unknown* true configuration does it need, if any?  Is anything
circular?  (iv) Corollary L.3 and the claim "the exponent is sharp".

## Item 3 — Theorem L⁺ (the first-order constant in a certified range)

Re-derive the proof (l.282 ff.): where does `Λ < 11.04` come from, is the range `‖η‖₂ ≤ μ/(ΛC_L)` right, and is the
bound `d_P ≤ ‖η‖₂/(μ + √(μ² − Λ‖η‖₂))` attained in the limit as claimed?  Replicate on a few chains: compute `μ`,
`C_L`, the certified range, and check the bound for random and adversarial `Y` inside the range; a control just
outside the hypotheses.

## Item 4 — the classes of the assumptions, and what the theorem guarantees

For every hypothesis (no four consecutive points coplanar; complete data of separation at most 4; exact
windows; dimension 3; deterministic errors): essential / needed only by the proof / convenience / replaceable by
a weaker quantitative condition / removal changes the constants / removal makes it false — with an example where
you claim "false".  And one paragraph a software author can act on: with the present constants, for which noise
levels and lengths does the theorem give an error bar smaller than the object (use an α-helix-like trace:
radius 2.3 Å, rise 1.5 Å, 100° per residue; and a strand-like trace: radius 0.94 Å, rise 3.3 Å, 160°–175°)?

## Item 5 — prior art for the threshold-free form (short; only after Items 1–3)

Is a *global, threshold-free* stability bound for reconstruction from the distances of a band (trilateration /
lateration) graph, obtained by stitching windows with complete distance data, in print?  Look where it would
be: patch-stitching and "as-rigid-as-possible" / local-to-global embedding analyses; Procrustes-based stitching
error bounds; the paper they cite for the exponential bound (Arias-Castro and Vishwanath, arXiv 2310.10900) and
the companion on patch stitching by the same first author (arXiv 2207.07218).  Log every query and address; give
reading levels; say what you did not reach.  "Not found" is never "new".  Network use for this item and for
Lemma P's source only; generic queries; nothing of this project in a query.

## Rules

Write only in `experiments/science/ws_R27/` and `docs/science/workstreams/R27_REPORT.md` — **use full paths; do
not write anywhere else in the repository**.  No state-changing git; no subagents.  Keep four kinds of checking
apart and say which you did for each statement: **review** (re-derived), **replication** (own code written from
the statements), **re-run** (their code — not available to you), **read only**.  Never fabricate; a reading
level for anything cited.  A finding is *critical*, *major* or *minor*; give a replacement text for each.  Report
what you did not check, and your own errors.  Machine: 4 cores and 15 GB shared with other jobs —
`OMP_NUM_THREADS=1`, at most two processes, **every script caps its own address space at 2 GB**, no run longer
than ten minutes; print the peak memory in the last line of every script; run Python with `-B`.  Keep `NOTES.md`
(in your own directory) from the first minute.  A log is cited only if its run reached its last line; use fresh
names instead of overwriting a log.  A time written into a file is read from the clock at that moment.  Every
check is reported with the violations of its control, and a control must be able to fail.
**If a tool declines an action, do not work around it: keep everything in `NOTES.md` and return the findings as
text in your hand-back, with a line "Tool actions declined".  Do not delete files with wildcards or `rm -r`.**
This is an internal review by an AI agent, not external peer review; say so in the report.

## The report

(0) Verdict in ten lines: for each of Lemma P, Lemma Q, Theorem L (local and uniform forms), Corollaries L.1–L.3,
Theorem L⁺: *proved as stated* / *proved with gaps (closed here or open)* / *false as stated (counterexample)*.
(1) The statements as you understand them, with implicit hypotheses.  (2) Findings, each with the line that
decides it and a replacement text.  (3) Your tests with their controls; the largest ratio `d_P/bound` you could
reach.  (4) The assumption table and the paragraph of Item 4.  (5) Prior art (Item 5) with the search log.
(6) What you did not check; your own errors; files.  Hand back a summary of at most fifty lines, with a line
"Tool actions declined: none" (or what was declined) and every web address opened.
