# Status of the Phase II adaptive-hierarchy division

*Branch `research/phase2-adaptive-hierarchy` (based on the pinned theory commit `b3c5d61`; the original
branches and the consolidated archive are not modified).  Updated 2026-11-28 02:45 UTC.*

**Mandate** (research owner's directive "Foundational Adaptive-Complexity Moonshot"): determine whether
every fixed number of adaptive rounds is suboptimal for certifying the log partition function of a
`u`-Lipschitz energy on the cube, or whether finitely many rounds reach `h`; first verify the two-round
separation; bounded resources; hard stop 2026-11-30 15:00 Eastern Time; no automatic resumption.

**State.**  Report: `docs/phase2_hierarchy/HIERARCHY_REPORT.md`.

| item | statement | status |
|---|---|---|
| two-round separation (Theorem 11.86) | verified independently: thresholds and exact twins reproduced; Lean files built | [N], [V] |
| Lemma B (relaxation) | what two rounds do not reveal carries at most `e^{−n(θ−h)}` of the visible mass | [P], finite `n`, explicit constants; exact check on 124 extremal cases [N] |
| Theorem H1 | three rounds reach `h` on every block-radial class `BR_m` | [P]; simulation [N] |
| Theorem H2 | `c_2(BR_2(φ₁, φ₂)) = max{h, ϑ(φ₁), ϑ(φ₂)}` | [P] upper bound; lower bound quoted from the archive |
| Corollary H4 | barrier: no block-radial family separates three rounds from `h` | [P] |
| Propositions G, C | the same for flags with any Lipschitz body (small-slope limit) and for codes of cells | [P] in the stated models |
| Conjecture H5 | `c_3(u) = h(u)` on all of `L_u` | [C]; **the general problem is open** |

**Not done.**  The general class `L_u`; hidden partitions and overlapping centres at finite slope; the
two-round exponent for more than two blocks; a universal certificate (report §8).

**Mailbox.**  Sent: `messages/hierarchy/HIE-MSG-0001.md` (to both other Phase II divisions),
`requests/hierarchy/HIE-REQ-0001.md` (to engineering; local replication only).  Read: THY-MSG-0023,
ENG-MSG-0009.

**Resources.**  This session cannot monitor its expenditure; the scope was bounded instead (local
computation of a few CPU-minutes per script; no external compute; reviewing subagents as recorded in the
report).  **No background process, scheduled session or computational job of this division is active
after its last commit.**
