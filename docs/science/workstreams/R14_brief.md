# Workstream R14 (launched 2026-11-26) — adversarial referee of the coordinator's own results: addenda A17 (13)–(16)

> **Head note (coordinator, 2026-11-26 06:05 UTC): this workstream has not been done.**  It was
> launched at 05:59 UTC and terminated within two minutes by a platform safeguard of the
> model provider, before any review (its notes, `experiments/science/ws_R14/NOTES.md`, are
> four lines).  The coordinator did not relaunch it with other words and did not do its
> work in its place.  The brief below stands as written for whoever is authorised to
> carry it out; until then addenda A17 (13)–(16) are unrefereed.

*Brief written by the coordinator, about the coordinator's work.  Nobody but the
coordinator has read these four parts; three of them carry numbers that have been
sent to the two other divisions.  Your job is to break them.  Read `COMMON.md` first
(its commit pins are out of date).  If the agent of this workstream is gone, its notes
are in `experiments/science/ws_R14/` and its draft in `R14_REPORT.md`.*

## What is under review

`docs/science/INFERENCE_LIMITS_ADDENDA.md`, parts **A17 (13)** (certified populations),
**A17 (14)** (the leucine helix with pair shares at twenty and thirty residues),
**A17 (15)** (serine on the helix: no share allocation rescues order 4; the rule
`2 p^k Γ_m`) and **A17 (16)** (Lemma A17.16; exact window terms; serine on the helix at
twelve residues; leucine with triple shares; the reach table), with their scripts and
logs in `experiments/science/pi_inference/`:
`certified_populations.py`, `helix_pair_form.py`, `serine_helix_shares.py`,
`serine_helix_shares_law.py`, `window_model.py`, `window_model_check.py`,
`serine_helix_reach.py`, `certificate_reach_table.py`.  They build on workstreams P3
(certified constants, band models), P5 and P6 (share forms) — whose reports you may
read, and whose statements you take as given unless you find them misused.

## What to do, in this order

1. **Proofs.**  Re-derive from scratch, before reading the addendum's proof:
   (a) the population bracket of A17 (13) (`P_E(A)` between `Z₊(A)/(Z₊(A) + Z₋(Aᶜ))` and
   `Z₋(A)/(Z₋(A) + Z₊(Aᶜ))`) and its sharpness claim; (b) Lemma A17.16 (both inequalities,
   every elementary inequality used, the case `A = ∞` excluded or not); (c) the identity
   behind the rule `2 p^k Γ_m` (factorial moments) and what it does and does not prove;
   (d) the validity of a sandwich with exact in-window evaluated terms, including the
   floating-point allowances — are the allowances P3/P6 computed for *their* models
   still sufficient when more terms are kept exact (count the evaluated values that
   enter a model energy; compare with `p6lib.fp_tables`)?; (e) P6's Lemma A′ with two
   windows (`window_model.triple_form_two_windows`): is the pair remainder `ρ_ab`
   right when the triple window is narrower than the band?  State every gap.
2. **An independent implementation.**  Write your own evaluation of the floor and
   ceiling energies of the triple form with exact window terms, from the tables the
   coordinator's driver uses but without `window_model.py` and without P3's
   `BandModel` (a direct sum over terms), and your own brute-force `ln Z` on enumerable
   instances.  Compare with the coordinator's models state by state on at least four
   enumerated instances that `window_model_check.py` does **not** use (e.g. lysine,
   leucine, phenylalanine, the patterned sequence, another backbone), including a
   window narrower than the chain.
3. **Attack the sandwich where it cannot be enumerated.**  For Ace-Ser₁₂-NMe on the
   helix at order 5, band 7 (the driver caches the ball; re-running it takes two
   minutes): search for states that violate `m₋ ≤ E ≤ m₊` — not by sampling the
   models, which the coordinator did, but by *optimisation*: maximise `m₋(x) − E(x)`
   and `E(x) − m₊(x)` over the `4.9·10⁹` assignments with simulated annealing or
   coordinate ascent from many starts (the true energy costs 0.4 ms per state).
   Report the largest values found and how many evaluations were spent.  A single
   violation falsifies the certificate.  Do the same for the leucine helix at thirty
   residues (A17 (14); `helix_pair_form.py`), where the model is the pair form.
4. **Numbers against logs.**  Every number in the four parts against the committed
   logs and JSON files: list each mismatch, each number without a log, each log whose
   run did not reach its last line, each script that does not re-run as its header
   says (re-run the cheap ones in a scratch copy).
5. **Claims of meaning.**  Where a sentence says more than its evidence: "certified",
   "predicted before", "no allocation rescues it", "the frontier is charged", "a
   design rule that needs no run", the comparison with enumeration "to rounding".
   Propose replacement sentences.
6. **Prior art, at the level you can reach.**  Lemma A17.16 is called "a variant of
   the Gibbs–Bogoliubov inequality" without a reference.  Is the two-sided form with
   the mean under the true ensemble in a textbook or paper you can actually open?
   Give only references you have opened; say which you could not.

## Rules

As in the R8 and R12 briefs.  Write only in `experiments/science/ws_R14/` and
`docs/science/workstreams/R14_REPORT.md`; import the coordinator's and the
workstreams' code read-only; your caches go into `ws_R14/cache` (you may copy the
coordinator's cached ball files there — they are evaluations of the model, not
results).  No state-changing git; no `lake build`; no subagents.  Model-relative
statements only; the fixed synthetic peptides of P2; no sequence is varied or
optimised; nothing target-specific; no cloud compute.  Scripts that produce cited
numbers run with one command; a log is cited only if its run reached its last line.
Machine: 4 cores and 14 GB shared with other jobs — `OMP_NUM_THREADS=1`, at most two
processes, no process above 3 GB, no run longer than 20 minutes without a
checkpoint.  Keep `NOTES.md` from the first minute.  Classify findings as critical
(a published number or the word "certified" is wrong), major (a statement must be
replaced), minor; give replacement texts.  Report your own errors.  **If a tool
declines an action, do not work around it: keep everything in `NOTES.md` and return
the findings as text in your hand-back.  Do not delete files with wildcards or
`rm -r`; use fresh directory names.**

## The report

(0) Verdict in five sentences: what stands, what falls.  (1) Proofs: per item, your
derivation and every gap.  (2) The independent implementation: instances, largest
differences.  (3) The attacks: largest values found, evaluations spent.  (4) Numbers
against logs (table).  (5) Sentences to replace.  (6) Prior art opened.  (7) How to
re-run.  (8) Not checked; own errors.
