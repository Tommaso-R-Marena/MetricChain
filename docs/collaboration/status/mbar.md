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
| information limits (C1, C2) | finite-sample two-point bound at every instance; adaptive allocation cannot beat the static optimum | [P]; cores [V]; Pinsker, chain rule [X]; [N] |
| synthesis (S1–S4) | path/thermodynamic-length bound; sampling as the bottleneck on the cube class; round hierarchy of allocation; envelope ratio as a χ² | [P] / conditional; [N] |
| Lean | `experiments/mbar/lean/`, 49 headline declarations, standard axioms only, audit passed | [V] |
| validation | synthetic systems with exact samplers; one public data set | development evidence only |

**Not done.**  A certified statement for Markov-chain samples at the right rate; the efficient
("tilted") region; a single-contrast interval without the `K`-dependent threshold; a proof of
asymptotic efficiency of the two-stage estimator; any experiment with a real sampler (proposed:
MBAR-REQ-0001; not authorised, not run).

**Mailbox.**  Sent: `messages/mbar/MBAR-MSG-0001.md` (to the three Phase II divisions),
`requests/mbar/MBAR-REQ-0001.md` (computational proposal to Ubuntu Engineering; not an
authorisation).  Read: ENG-MSG-0009; the headers and the cited sections listed in MBAR-MSG-0001.

**Resources.**  This session cannot monitor its expenditure (see `docs/mbar/FINAL_REPORT.md` §6).
Local computation only; no Modal job; no external computation.  **No background process, scheduled
session or computational job of this division is active after its last commit.**
