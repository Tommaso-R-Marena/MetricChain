# Applying the assumption audits AA1 and AA2 to the theory report and the README — brief

*Coordinator, 2026-11-26.  The two audits (`AA1_REPORT.md` §7 "Overstatements" and §8 "Errors";
`AA2_REPORT.md` §A.4 "Overstatements" and §A.6 "Errors") list 47 sentences that present a result
more generally than it is proved and about 16 errors (one of substance: a hypothesis lost
from Theorem 11.33(a); the others stale sentences, status cells, two numbers).  The
research owner's directive: "Avoid presenting results for restricted models as universal
conclusions."  The coordinator has verified the error of substance (Err-1 of AA1) and
spot-checked the tables; this task applies all of it, item by item, with a record.*

## What to do

For **every** item of the four lists, in this order: AA1 §8 (Err-1 … Err-10), AA2 §A.6 (1–5),
AA1 §7 (O-1 … O-22), AA2 §A.4 (1–25):

1. Read the cited passage in `docs/THEORY_REPORT.md` / `README.md` and the place that the audit
   says contradicts or restricts it (the audit entry, the theorem, the later section).
2. Decide: is the audit right?  If yes, make the **smallest edit that makes the sentence
   true**: add the missing hypothesis or scope ("on the uniform cube", "for two letters",
   "for mean-field ferromagnets", "up to a polynomial factor", "with the instance as a hint",
   "for an additive known part", …), or replace a stale sentence by what the later section
   establishes, with a pointer to it.  Do not delete content, do not rewrite paragraphs, do
   not weaken a statement more than the proof requires, do not change the label of a
   theorem except where the audit shows the label wrong.  If the audit is wrong or you are
   not sure, do **not** edit; record the item as *declined* or *for the coordinator* with
   the reason.
3. Append one row to `docs/audit/APPLIED_CORRECTIONS.md` (create it first, with a header):
   item id; file and line (old numbering); the old sentence (abridged); the new sentence;
   the justification (theorem, line or script that supports the restriction).

Work **from the bottom of each file upwards** within a pass, so that the audits' line
numbers stay valid for the items not yet done (or locate each sentence by its text).

## Particular items

* **Err-1 of AA1 (Theorem 11.33(a), around line 3877).**  Restore the hypothesis of the source
  (`docs/workstreams/D_REPORT.md`, Theorem 13: "`f` additive"): the setting sentence of the
  theorem must say that the known part `f` is additive (a sum of site terms; in particular
  `f ≡ 0`), and (a) must say what its proof uses — Dobrushin's condition for `f + g` along the
  annealing path, which the class bound gives when `f` is additive.  Add, after the theorem's
  closing paragraph, a short remark **[P/N: audit AA1, `experiments/audit/AA1/aa1_04_second_order_known_part.py`]**:
  without the hypothesis (a) fails — for a known part that confines the ensemble to a code
  (the extended Golay code at `n = 24`, `w = 4`: every algorithm with `ε < 10⁻³` makes
  `(1 − 2δ)·4096` evaluations; Gilbert–Varshamov codes: exponentially many at every `w > 0`), and
  for a *pairwise* known part of ferromagnetic blocks (`exp(Θ(n^{1/3}))` at `w = 4`); the first
  version of this theorem omitted the hypothesis (found by the assumption audit).  Adjust
  the summary sentences that repeat the claim (row G15 around line 1507; the paragraph
  after the theorem; any README sentence) with "for an additive known part".  Add an entry
  to `docs/DEAD_ENDS.md` — append at the end, numbered after the last entry — recording the
  lost hypothesis (the same failure mode as D62) in five lines.
* **AA2 §A.6 item 5** (records out of date): the README's list of referee reports (R10–R12
  exist in `docs/reviews/`), line 79 of the report, and the stale sentence in the research
  log's "Resume here" about the rate `O(1/k)` being unrefereed.
* Sentences that occur in several places (the audits list the places): correct each
  occurrence.
* The subtitle of the report (O-18) is the name of the research programme as its owner
  gave it: leave it, record as declined with this reason.

## Rules

* Files you may edit: `docs/THEORY_REPORT.md`, `README.md`, `docs/RESEARCH_LOG.md` (only the stale
  sentence named above), `docs/DEAD_ENDS.md` (append one entry).  Files you create:
  `docs/audit/APPLIED_CORRECTIONS.md`.  Nothing else — in particular no Lean file, no script,
  no file under `docs/collaboration/`, `docs/workstreams/`, `experiments/`.
* Do **not** touch the text between "**Theorem 11.53**" and "**Theorem 11.54**" of the theory
  report except the one stale sentence of AA2 §A.6 item 1 (the coordinator is inserting a
  new theorem there).
* No theorem numbers change.  No new mathematical claims beyond what the audits establish
  with scripts or citations; label anything taken from the audits as such.
* Style of the report: plain prose, mathematics in backticks, British spelling.
* At the end run `python3 scripts/check_doc_refs.py` from the repository root; if it flags a
  token you introduced, reword (do not edit the script).  Do not run `scripts/audit_all.sh`,
  `lake`, or any git command that changes state (`git diff` is fine and useful).
* **Write early and often**: create `APPLIED_CORRECTIONS.md` in your first few tool calls and
  append a row after every item.  Do not think for long stretches without a tool call.

## What to report back (at most 50 lines)

Counts: applied / declined / left for the coordinator, by list.  For every declined or
left item: the id and one line of reason.  Anything you found on the way that the audits
did not list.  The result of `check_doc_refs.py`.
