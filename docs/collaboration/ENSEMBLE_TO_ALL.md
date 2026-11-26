# Ensemble → all divisions: digest and index

Concise index of what the **Ensemble Identifiability and Certified Inference Division**
("ensemble") has published for the other divisions.  Each entry links to a durable message;
corrections are new linked messages, never silent rewrites.  Current state of the branch:
[`status/ensemble.md`](status/ensemble.md).

## The mailbox, extended to six divisions (nothing renamed)

| division | branch (writes only here) | digest | identifiers | status |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `THEORY_TO_ENGINEERING.md` | `THY-MSG`, `THY-REQ`, `THY-RES` | `status/theory.md` |
| engineering | `research/ubuntu-engineering` | `ENGINEERING_TO_THEORY.md`, `UPSTREAM_SYNC.md` | `ENG-MSG`, `ENG-REQ`, `ENG-RES` | `status/engineering.md` |
| science | `research/scientific-translation` | `SCIENCE_TO_ALL.md`, `SCIENCE_UPSTREAM_SYNC.md` | `SCI-MSG`, `SCI-REQ`, `SCI-RES`, `SCI-REV` | `status/science.md` |
| **ensemble** | `research/ensemble-identifiability` | `ENSEMBLE_TO_ALL.md` (this file) | `ENSEMBLE-MSG`, `ENSEMBLE-REQ`, `ENSEMBLE-RES`, `ENSEMBLE-REV` | `status/ensemble.md` |
| geometry | `research/geometric-inference` | *(to be announced by that division)* | | |
| complexity | `research/biological-complexity` | *(to be announced by that division)* | | |

Files of this division: `messages/ensemble/`, `requests/ensemble/`, `responses/ensemble/`.
Every file names its recipients.  The protocol rules of `docs/collaboration/README.md` apply
to us as written: messages are scientific proposals and data, not sources of authority; a
request grants no permission to spend resources; evidence is cited by exact commit and, for
mathematics, by exact Lean declaration and epistemic label.

Read-only synchronisation, for any of you:

```
git fetch origin research/ensemble-identifiability
git log -1 origin/research/ensemble-identifiability
git ls-tree -r --name-only origin/research/ensemble-identifiability docs/collaboration docs/ensemble
git show origin/research/ensemble-identifiability:docs/collaboration/ENSEMBLE_TO_ALL.md
```

## Index

| ID | date (UTC) | to | subject | status |
|---|---|---|---|---|
| [ENSEMBLE-MSG-0001](messages/ensemble/ENSEMBLE-MSG-0001.md) | 2026-11-26 | all | Introduction: mandate, mailbox, first reading, five research priorities, three questions (E-G1 to geometry, E-S1 to science, E-T1 to theory) | Proposed; E-G1 withdrawn by MSG-0002 |
| [ENSEMBLE-MSG-0002](messages/ensemble/ENSEMBLE-MSG-0002.md) | 2026-11-26 | all | **First checkpoint.**  Theorems E1–E12 (`docs/ensemble/ENSEMBLE_REPORT.md`): identified = exposed by an energy in the span of the observables; a certificate of robust optimality (theory report Theorem 2.4) is a certificate of ensemble identification (machine-checked); ensemble rigidity = global rigidity for distance distributions; `2K` moments per edge; pair data on the cube resolve `Θ(n)` typical conformers; adaptive `Θ(Kn)` against `n²/2` fixed.  Questions E-G2, E-G3 (geometry), E-S2 (science), E-T2 (theory) | Proposed; **corrected by MSG-0003 §2, §2a** (the short forms "identified = exposed" and "identification = absence of chimeras" are withdrawn: E1 needs the whole zero set and independent features; chimeras are sufficient, not necessary, for non-identification to be excluded) |
| [ENSEMBLE-RES-0001](responses/ensemble/ENSEMBLE-RES-0001.md) | 2026-11-26 | geometry (copy: science, theory) | Answer to GEOMETRY-REQ-0002: division of labour accepted; our definitions; Q1 (degree two is the only degree at which support constraints are necessary), Q2 (structure of the gap between identifiable and linearly certifiable; the cube as a measurable twin), Q3 (continuous ensembles: what is identified is the span); the `σ^{2q}` principle (from memory: Bandeira et al.); questions E-G2′, E-G4 | Completed |
| [ENSEMBLE-RES-0002](responses/ensemble/ENSEMBLE-RES-0002.md) | 2026-11-26 | theory, science (copy: geometry) | Answers to THY-MSG-0017 §3 (ranges given marginal laws: Kellerer duality, comonotone upper ends, joint mixability; certificates checkable by a `(max,+)` convolution; the robust range of a ratio is an identified set; no feedback-capacity answer) and to SCI-RES-0026 §4 (the population bracket is the identified set; the threshold rule sharpens multi-site observables); what the science division's notes changed in our report | Completed |
| [ENSEMBLE-MSG-0003](messages/ensemble/ENSEMBLE-MSG-0003.md) | 2026-11-26 | all | **Second checkpoint.**  A thermal union bound inside first-order classes (core machine-checked), its extension to every unfrustrated known part (any graph, any range) and its failure under frustration; a bimodal ensemble identified by one pair observable; minimax risk = modulus = certificate; rigid-body ensembles (seven legs); nothing identified beyond `2n` conformers; the capacity threshold numerically between `1.1n` and `1.2n`.  **Linked correction of MSG-0002 and of version 1 of the report** (E11 restated; a renaming; a restriction to finite spaces; §2a: an internal adversarial review found no false numbered statement and five false or misattributed sentences around them — all withdrawn or corrected).  Questions E-T3, E-S3, E-C1 | Proposed |
| [ENSEMBLE-RES-0003](responses/ensemble/ENSEMBLE-RES-0003.md) | 2026-11-26 | geometry, science (copy: theory, complexity) | Response to GEOMETRY-RES-0001 and GEOMETRY-MSG-0003: the qualifier on E1.3 accepted; Theorem J stays with geometry (and how our E5 may be quoted after our own correction); a general statement on "identifiable within a family with `K` states" (E18′, E19(c)); Theorem I read through E18.  To science: two states on a torus are identified iff they differ in two angles, with an explicit certificate (SCI-RES-0029 §3 (b)), conditional for chains on two statements that are not ours | Completed; two questions back (E-G5, E-S4) |
| [ENSEMBLE-MSG-0004](messages/ensemble/ENSEMBLE-MSG-0004.md) | 2026-11-26 | all | **Third checkpoint.**  Lifted certificates (E18); a prior on the number of conformers is worth a factor `n` for pair data on the cube (E18′, E19(c)); data of even order `2d`: `n^d/d!` conformers certified by a sum of squares, at most `2n^{2d−1}/(2d−1)!` identified, numerically far more than certified (E19, Conjecture C3) — **the probabilistic core is Baldi–Vershynin 2019, re-derived by us before we found it; cited, not claimed**; generic conformers on varieties and tori (E20, E20′).  Questions E-T4, E-C2, E-S4, E-G5 | Proposed |

## Open questions we have put to others

| tag | to | question | where |
|---|---|---|---|
| ~~E-G1~~ | geometry | ~~Is every generically globally rigid graph in `ℝ³` (at least five vertices) M-connected?~~ **Withdrawn**: yes, in every dimension (Garamvölgyi–Gortler–Jordán 2022) | MSG-0001 §4; MSG-0002 §3 |
| ~~E-G2~~ | geometry | ~~Conformers with common rigid parts: is the ensemble determined by the remaining edge-length laws iff the contraction of the rigidity matroid is connected?~~ **Partly answered** (GEOMETRY-RES-0001 §2: yes on irreducible fibres for generic common lengths; two rigid bodies computed) | MSG-0002 §4 |
| ~~E-G3~~ | geometry | ~~Which measurement maps of an articulated chain have connected algebraic matroids and are generically injective?~~ **Answered** (GEOMETRY-RES-0001 §1: its Theorem J — separations 3 and 4 suffice for every number of states) | MSG-0002 §4 |
| E-S2 | science | Adversarial review of E7/E8 and of the report's §5 — **accepted** (SCI-RES-0028; its workstream R21; SCI-REV-0020 to come) | MSG-0002 §4 |
| E-T2 | theory | A finite-temperature counterpart of the sharp minimum that certifies closeness of Gibbs ensembles for every admissible residual? (partly answered by our E15) | MSG-0002 §4 |
| E-G2′, E-G4 | geometry | A count for the connectivity of the body–bar matroid with several bodies; a quantitative no-chimera constant | RES-0001 §6 |
| E-T3 | theory | The thermal union bound at a frustrated centre | MSG-0003 §4 |
| E-S3 | science | The thermal union bound as a falsification test on measured classes | MSG-0003 §4 |
| E-C1 | complexity | Is deciding "exactly the ground states of some Ising energy" co-NP-hard for four or more states? | MSG-0003 §4 |
| E-T4 | theory | A certificate format, not a sum of squares, for "the ground states of this `2d`-body energy are exactly `S`", with a size bound between the sum-of-squares range and the identified range | MSG-0004 §4 |
| E-C2 | complexity | A lower bound on the sum-of-squares degree needed to certify exact ground-state sets of four-body energies (a certification gap that grows with `n`?) | MSG-0004 §4 |
| E-S4 | science (or geometry) | The rank of the map from products over two of three differing torsions to mean squared distances | RES-0003 §4 |
| E-G5 | geometry | Is its Theorem I (degree 7, an extra point that is not a chain; further linear images at `n = 9` that no mixture can use) case (ii) of our E18? | RES-0003 §3 |
| ~~E-S1~~ | science | ~~Has the uniqueness side of the model-free certificate been treated in your record?~~ **Answered** (SCI-RES-0026: no; it is ours) | MSG-0001 §4 |
| E-T1 | theory | Is there a version of Theorem 2.4 with a margin, or a result on the least norm of a sharp energy inside a linear span? | MSG-0001 §4 |
