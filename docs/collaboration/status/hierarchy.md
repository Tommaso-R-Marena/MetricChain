# Status of the Phase II adaptive-hierarchy division

*Branch `research/phase2-adaptive-hierarchy` (based on the pinned theory commit `b3c5d61`; the original
branches and the consolidated archive are not modified).  Updated 2026-11-28 05:40 UTC.  **The division
has stopped; it does not resume when a message arrives, and it does not poll other branches.**  It acts
again only on a directive of the research owner (the last one: the collaboration update of 2026-11-28
about Division 9, answered once by `HIE-MSG-0003`).*

**Mandate** (research owner's directive "Foundational Adaptive-Complexity Moonshot"): determine whether
every fixed number of adaptive rounds is suboptimal for certifying the log partition function of a
`u`-Lipschitz energy on the cube, or whether finitely many rounds reach `h`; first verify the two-round
separation; bounded resources; hard stop 2026-11-30 15:00 Eastern Time; no automatic resumption.

**State.**  Report: `docs/phase2_hierarchy/HIERARCHY_REPORT.md` (second version, with the corrections after
replication and review).  Addendum: `docs/phase2_hierarchy/HIERARCHY_ADDENDUM.md`.

| item | statement | status |
|---|---|---|
| two-round separation (Theorem 11.86) | verified independently: thresholds and exact twins reproduced; Lean files built | [N], [V] |
| Lemma B (relaxation, known blocks) | what two rounds do not reveal carries at most `e^{−n(θ−h)+O(log n)}` of the visible mass | [P], finite `n`, explicit constants; reviewed; replicated by engineering (`ENG-RES-0020`) |
| Theorem H1 | three rounds reach `h` on every block-radial class `BR_m` (blocks `≥ N_u`, `n ≥ n₀`) | [P]; reviewed; algorithm replicated on cubes by engineering and by the reviewer |
| Theorem H2 | `c_2(BR_2(φ₁, φ₂)) = max{h, ϑ(φ₁), ϑ(φ₂)}` | [P] upper bound, reviewed; lower bound quoted from the archive |
| Corollary H4 | barrier: no application of Lemma 11.85 to boundedly many blocks separates three rounds from `h` | [P]; scope narrowed after review |
| Propositions G, C | the same for flags with any Lipschitz body (small-slope limit) and for codes of cells, with margins | [P] in the stated models; margins supplied by the reviewer |
| **Theorem P** (addendum) | relaxation principle for arbitrary nested partitions of hidden classes; dimension-free | [P]; reviewed line by line, no error found; brute force by author and reviewer [N]; arithmetic [V] |
| **Theorem H6** (addendum) | three rounds reach `h` on every class `HP_m` of energies with at most `m` hidden symmetry classes (hidden blocks, hidden partitions, overlapping centres) | [P], asymptotic (`n ≥ n₀(u, m, η, δ)`); reviewed step by step, no error found; not machine-checked |
| Corollaries H7, H8 | exactly three levels `a > c_2 > h` on `HP_m`, `m ≥ 4`; a three-round separation needs unboundedly many hidden classes | corollaries, with the archive's lower bounds |
| Conjecture H5 | `c_3(u) = h(u)` on all of `L_u` | [C]; **the general problem is open** |

**Not done.**  The general class `L_u` (energies without hidden symmetry); the two-round exponent of `HP_m`
and of `BR_m`, `m ≥ 3`; a universal certificate (report §8, addendum §A5).

**Reviews and replication** (all by AI sessions).  `HIERARCHY_REVIEW.md` (report: no critical, three major,
nine minor findings; all applied); `HIERARCHY_ADDENDUM_REVIEW.md` (addendum: no critical, no major, twelve
minor; all applied); `ENG-RES-0020` on the engineering branch (Lemma B and Algorithm R3 replicated; one
numerical over-claim of ours refuted and withdrawn).  No human expert has read any of it.

**Lean** (pinned toolchain; each compiles without warnings; standard axioms only):
`proofs/Frontiers/RelaxationCore.lean` (bookkeeping of Lemma B, two binomial facts),
`proofs/Frontiers/FlagInequality.lean` (the inequality of Proposition G),
`proofs/Frontiers/PartitionChain.lean` (bookkeeping and per-cell price of Theorem P).  The analytic inputs
of the three proofs are hypotheses there, not formalised.

**Mailbox.**  Sent: `messages/hierarchy/HIE-MSG-0001.md`, `HIE-MSG-0002.md` (linked correction of the first
and the new result; to both other Phase II divisions), `HIE-MSG-0003.md` (to Division 9, certified MBAR),
`requests/hierarchy/HIE-REQ-0001.md` (answered by `ENG-RES-0020`).  Read: THY-MSG-0023, ENG-MSG-0009,
ENG-MSG-0010, ENG-RES-0020; of Division 9 (`research/phase2-certified-mbar` at `003dad8`, opened 05:23 UTC,
no finding of its own yet) the provenance note and the imported `MAIN_RESULTS.md` (common model, minimax
section, limitations).  No message of the theory instance or of Division 9 addresses this division.

**Collaboration with Division 9 (owner's update of 2026-11-28).**  One bounded pass, recorded in
`HIE-MSG-0003`: (i) the exact relation between statistical sampling complexity and evaluation query
complexity — they coincide for reweighting to an *unsampled* target from designed references with known
normalisers, and nowhere else; (ii) five statements that transfer, with status (the one-round exponent is
the worst-case relative entropy and lies exponentially below the second-moment threshold; a sharp cap on
what an unvisited region can hold, on the cube and in Gauss space; a two-point lower bound in the MBAR
oracle model for an unsampled Lipschitz target; stages of design; effective resistance at exponentially
small overlap is a bottleneck path); (iii) four candidate attacks on the round hierarchy from statistical
techniques, examined and rejected (graph-structured hiding, many-hypothesis counting, thermodynamic
length as the constant of the `1/k²` law — refuted numerically —, posterior allocation).  **No new attack
on the general three-round problem was found.**  None of (ii) has been reviewed.

**Resources.**  This session cannot monitor its expenditure; the scope was bounded instead (local
computation of a few CPU-minutes per script; no external compute, no Modal job; two reviewing subagents,
one for the report and one for the addendum, each used once).  **No background process, scheduled session
or computational job of this division is active after its last commit.**
