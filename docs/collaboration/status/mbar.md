# Status of Division 9 — certified statistical thermodynamics (multistate free-energy estimation)

*Branch `research/phase2-certified-mbar` (based on the pinned theory commit `b3c5d61`; the original
branches, the Phase II branches of the other divisions and the consolidated archive are not modified).
Identifier prefix `MBAR-`.  Updated at the last commit of this branch.*

**Mandate** (research owner's directive "MetricChain Phase II — Division 9: Certified Statistical
Thermodynamics and Optimal Molecular Simulation", 2026-11-28): verify the strengthened MBAR handoff
(v2) independently; establish rigorous and practically consequential results on optimal sampling
allocation, finite-sample confidence guarantees and information limits; formalise the deterministic
cores in Lean; validate with genuine pilot-based allocation; exchange mathematics with the three
active Phase II divisions; local computation only; Claude ceiling $350; hard stop 2026-11-30 15:00
Eastern Time; no automatic resumption.

**State.**  Start at `docs/mbar/README.md`; results in `docs/mbar/FINAL_REPORT.md`.

| item | statement | status |
|---|---|---|
| handoff A1, A2, E2, B1–B5, C1–C3, D1, E1, E3, G1, G2 | audited; no mathematical error found | re-derived [P]; cores [V]; C1, C2 valid but far from sharp; D2 not reconstructed |
| allocation theory (A2–A10) | dual formula, closed orthant, concave precision, Elfving-type identity, equivalence theorem, efficiency certificate, monotone algorithm, rounding, safeguard | [P]; cores [V]; [N] |
| correlated sampling (A11, A12) | MBAR's variance is not convex in the allocation (counterexample); three statements that remain true | [N]; [P] |
| likelihood-ratio e-process region (B1–B3, B5) | finite-sample, simultaneous, anytime-valid, allocation-adaptive confidence region; model check | [P]; fixed-sample finite-support core [V]; Ville [X]; [N] |
| information limits (C1, C2) | finite-sample two-point bound at every instance; no adaptive allocation beats the static optimum by more than a universal constant factor (local; leading-constant version open) | [P]; cores [V]; Pinsker, chain rule [X]; [N] |
| synthesis (S1–S4) | path/thermodynamic-length bound; sampling as the bottleneck on the cube class; round hierarchy of allocation; envelope ratio as a χ² | [P] / conditional; [N] |
| Lean | `experiments/mbar/lean/`, 50 headline declarations, standard axioms only, audit passed | [V] |
| internal review | one adversarial AI referee: no false theorem; one serious code defect (solver), one statement false as written, one wrong interface claim, overclaims, six numbers — all corrected | `docs/mbar/REVIEW_A.md` |
| validation | synthetic systems with exact samplers; one public data set | development evidence only |
| exchange with the other divisions | five inbound messages read and answered (MBAR-MSG-0003); replications of A1/A2 (foundations) and of B1 and the region (engineering) recorded; three limits accepted (central-limit-scale statements; B6 on rare events; the computational proposal premature) | `docs/mbar/SYNTHESIS.md` §S8; seven inequalities and numbers recomputed |

**Not done.**  A certified statement for Markov-chain samples at the right rate; the efficient
("tilted") region; a single-contrast interval without the `K`-dependent threshold; a proof of
asymptotic efficiency of the two-stage estimator; any allocation experiment with correlated samplers
(protocol frozen, `docs/mbar/PROTOCOL_LOCAL_CONTROLS.md`; **not run** — it needs the research owner's
renewed authorisation of this division, no Modal budget); any experiment with a real sampler
(MBAR-REQ-0001: answered by ENG-RES-0021, not launched, superseded).

**Mailbox.**  Sent: `messages/mbar/MBAR-MSG-0001.md` (to the three Phase II divisions),
`messages/mbar/MBAR-MSG-0002.md` (corrections to it after the review, and a warning about the first
version of our solver), `requests/mbar/MBAR-REQ-0001.md` (computational proposal to Ubuntu
Engineering; not an authorisation; answered and superseded), `messages/mbar/MBAR-MSG-0003.md` (reply to
all three divisions; last message).  Read: ENG-MSG-0009; the headers and the cited sections listed in
MBAR-MSG-0001; and, in full, THY-MSG-0024, THY-MSG-0025, HIE-MSG-0003, ENG-MSG-0011, ENG-RES-0021.
This division did not poll the other branches while it worked, does not poll now, and does not resume
when a message arrives.

**Resources.**  This session cannot monitor its expenditure (see `docs/mbar/FINAL_REPORT.md` §6).
Local computation only; no Modal job; no external computation.  **No background process, scheduled
session or computational job of this division is active after its last commit.**
