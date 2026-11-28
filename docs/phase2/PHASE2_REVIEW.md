# Internal adversarial review of `docs/phase2/PHASE2_REPORT.md`

*Referee: internal AI referee (adversarial), 2026-11-28.  This is an internal review, not peer
review.  Scripts and their outputs: `experiments/phase2/review/`.  Nothing else was created or
edited; no `lake`/`lean`/audit script was run; git was used read-only.*

Verdict vocabulary: **correct as stated** / **correct after a repair** / **gap** / **wrong**.
"Line N" always refers to a line of `docs/phase2/PHASE2_REPORT.md` as of this review.

## 0. Status of this file

(in progress — sections are filled in as the review proceeds; an unfilled section means *not yet
reviewed*, not *no findings*)

Log of work (appended as it happens):

* read the brief, the report (614 lines), `proofs/Frontiers/ObservationInvariance.lean` (645 lines,
  read only), the Lean statements `expected_queries_ge_packing`, `prob_query_ne_ge`,
  `nonadaptive_expected_queries_ge`, `QueryAlgorithm`; theory report Theorems 11.22, 11.25, 11.44,
  11.45 (statements).
* `experiments/phase2/review/r1_constants.py` → `out_r1_constants.txt` (mpmath, 40 digits, own code):
  all constants, the table of §2.3, `ν*`, `α₀`, `α₁`, the side condition of Corollary A′, the slopes
  of §5 and the Rao remark reproduce (details in §7 below).

## 1. Theorem E (samples), §6

## 2. Theorem A, §2.2

## 3. Lemma 2.5, Theorem A′, Corollary A′

## 4. Lemma 2.6, Theorem A″, Corollary A″, §2.4 (3)

## 5. Theorems B, B′, Corollary B′

## 6. Theorem C, Corollary C, Proposition C′

## 7. Numbers (independent replication)

## 8. Novelty table (§9)

## 9. Lean versus text

## 10. Overclaiming

## 11. Summary of verdicts

## 12. What was not checked
