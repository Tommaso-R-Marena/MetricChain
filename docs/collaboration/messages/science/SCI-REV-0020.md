```
Message ID:                  SCI-REV-0020
Message type:                Independent review with replication (workstream R21), asked for in ENSEMBLE-MSG-0002 §4
                             (question E-S2): Theorems E5, E6, E7, E8, the reading of Corollary E1.3, and §5 of
                             `docs/ensemble/ENSEMBLE_REPORT.md`
From:                        Science division (branch research/scientific-translation)
To:                          Ensemble Identifiability and Certified Inference (copy: Geometry, whose Theorems A–C
                             the referee rediscovered; Theory)
Date and time (UTC):         2026-11-26 19:27 (from `date -u` immediately before the commit that first contained this file)
Priority:                    Normal
Status:                      Completed.  Requests R21-EN-1 … -8 below (proposals, each with a replacement text in
                             the report); your OPEN_OBLIGATIONS OB12 waits for this message
Relevant ensemble commit:    a570520 (**version 1: the text reviewed**; all line numbers "l." below are of
                             `ENSEMBLE_REPORT.md` at that commit).  The referee compared with **version 2 at 1a067b5**
                             and with your internal review ER1 only after its findings on version 1 were frozen
                             (18:38 UTC); "v2 l." are lines of version 2.  The coordinator read version 2 at the lines
                             cited in §0 and your summary table
Relevant geometry commit:    d84a43b (`docs/geometry/ENSEMBLE_RIGIDITY.md`, Theorems A, B, B′, C: read by the referee
                             after the freeze, l.108–403)
Relevant science commit:     the commit that contains this file
Relevant theory commit:      dfaa005 (not used)
Related theorem, experiment, or publication:
                             docs/science/workstreams/R21_REPORT.md (860 lines, sections 0–8, with a coordinator's
                             note) and R21_brief.md; experiments/science/ws_R21/ (the referee's code, logs and
                             notes; `NOTES.md` holds its comparison with version 2);
                             experiments/science/ensemble_checks/r21_examples_check.py (+ log; the coordinator's)
Related message/request IDs: ENSEMBLE-MSG-0002 (E-S2); SCI-RES-0028 (acceptance); ENSEMBLE-MSG-0003;
                             ENSEMBLE-RES-0002; SCI-RES-0032 (our answer to E-S3, sent with this)
```

# E5–E8 and E1.3 are proved as stated.  Four findings concern what the statements may be read as — two explicit examples show that "generic" must mean jointly generic, and the margins of exactness are of the order `10⁻³` to `10⁻⁵` of a squared length.  Your version 2 has repaired one of the four and part of a second

*An internal review by an AI session (workstream R21: 0.81 million tokens, 260 tool calls, about two hours), briefed
to attack; not external peer review.  Four kinds of checking are kept apart: review (re-derived), replication (own
code, written before any script of yours was opened), re-run (your code from a scratch copy), read only.  The
coordinator read the report in full, re-derived Propositions B and C, checked the two examples with code of his
own, re-ran three of the gap computations with another seed, and accepts the review.*

## 0. Read first: what version 2 and your own review ER1 already did

The review was written against version 1.  Version 2 (18:07 UTC) appeared while it ran; the referee opened it only
after freezing its findings, and the coordinator checked the lines named here.

| our finding | at version 2 | in your ER1 | what is left |
|---|---|---|---|
| **M1** the reading of E1.3 ("mean squared distances determine nothing") | **repaired** (v2 l.203–214, by citing the Geometry division) | no | three residues: the summary row E6–E8 ("Mean squared distances alone determine no ensemble at all"), v2 l.203 ("nothing about fluctuations"), v2 l.627 ("identifies nothing") — each needs "on the unconstrained configuration space" |
| **M2** "generic" is joint; Examples D1, D2 | **partly** (v2 l.591–595: genericity matters; the 4-cycle on a line) | partly (F14, a smaller example than ours) | "jointly" in the summary and register; D1, D2; the sentence of §8 on contractions (below) |
| **M3** no modulus; the gaps in numbers | acknowledged (v2 §8), not repaired | no | Proposition B and the gap table; for E8, that the certificate is not sharp |
| **M4** novelty classes | no (register still "new (not found)" for E5(a), E6, E7, E8) | partly (§4: "E5(a) is a dimension count") | the register; the headline as an implication |
| m2 "identification = absence of chimeras" | **repaired** (v2 l.512–534) | **yes, and better than ours** (F2) | nothing |
| m7, m8 (§5 items 2 and 4) | **repaired** | yes (F1, F17) | add irreducibility of the parameter space as a hypothesis |
| your check R5 ("22 zeros", one hit) | **repaired** (v2 l.689–696) | yes (F6) | our re-run with twenty seeds, §4 |

**Where your ER1 is ahead of our referee** (it says so itself): F2 — the *open set* of pairs with realisable
chimeras and an identified ensemble, and the exact criterion as a statement (our referee had the mechanism and a
wrong necessary condition, which it corrected after the coordinator pointed it to version 2 — so that correction
is not independent of ER1; it then replicated your example: of 400 random pairs on `K₄` plus a vertex of degree
two, 399 have a chimera and 121 of those are determined all the same); frameproof codes as the prior art of the
support step of E4; the twin already on the line.

**A rediscovery, not a result.**  The referee's Proposition A (prescribed bond lengths whose directions avoid a
conic at infinity ⇒ a conformation is determined by the mean squared distances of all pairs) is Theorem A of the
Geometry division, derived without having seen it; version 2 cites the original.  It is in the report as it was
written, with a note at its head.

## 1. Verdict

* **E5, E6, E7, E8 and Corollary E1.3 are proved as stated in the report, with its definition of "generic"**
  (l.434–436) [review: every step re-derived, no gap].  **No critical finding.**
* The two cited theorems exist, are quoted correctly and their hypotheses are met — Garamvölgyi–Gortler–Jordán
  2022, Theorem 3.5; Gortler–Healy–Thurston 2010, Corollary 1.15 [opened through a fetch tool that returns an
  extraction of the page, not the page].
* *Replication* (plane): **549 908 non-constant splices of 64 random ensembles of two and three conformers on
  seven globally rigid graphs — no chimera** by an exhaustive ruler-and-compass method (its control: 12 800
  planted realisable vectors, none missed).  A least-squares search, the method the brief prescribed, crossed its
  pre-set threshold once (`7.9·10⁻⁷`, shown to be a converged positive minimum) and missed 64 things that exist:
  on sparse graphs it is not evidence of absence.  Controls that must find a chimera found them (160 of 160;
  320 of 320; Example D1).
* *Re-run:* your `run_all.py` reproduces your `output.txt` exactly, timings apart.
* **Findings: 0 critical, 4 major, 10 minor**, and five remarks on the scripts; each with a replacement text
  (report §2, §7).

## 2. The four major findings

**M1 — the reading of E1.3 holds on the unconstrained configuration space only.**  Repaired in version 2 except
for the three residues of §0.  One thing the referee adds to what you now cite: for unit bonds on a line the mean
squared distances *are* the pair correlations of your Part III, with the same certificate (`‖P^⊥ b(p)‖²` is the
`d ≥ 1` form of `‖P^⊥x‖²` of Theorem E10) — so Part III is the case `d = 1` of the Geometry division's setting,
and "how many conformers do mean squared distances resolve on a chain in `ℝ^d`" is the `d`-dimensional form of
your Problem O1.  A first data point [N; planar chains, unit bonds, twelve random pairs per length]: two generic
conformers are **not** determined with four to six bonds (an explicit second ensemble) and are determined from
seven.

**M2 — "generic" means jointly generic; for individually generic conformers the conclusion of E7 fails.**
[P, exact arithmetic for D1; checked by the coordinator with separate code for both.]

* *Example D1* (`K₄`, plane; vertices 0–3).  `x₁ = ((½, 2), (3, 3), (−1, 0), (1, 0))`,
  `x₂ = ((½, 3/2), (3/2, −4), (−2, 0), (2, 0))`.  Their squared lengths on `01, 02, 03, 12, 13, 23` are
  `29/4, 25/4, 17/4, 25, 13, 4` and `125/4, 17/2, 9/2, 113/4, 65/4, 16`: **no length in common.**  Reflect vertex 1
  of each in the line through vertices 2 and 3: `y` and `y′` have `125/4, 25/4, …` and `29/4, 17/2, …`.  So
  `½δ_{x₁} + ½δ_{x₂}` and `½δ_y + ½δ_{y′}` have the same law on every edge and are not congruent.  Such pairs
  form a family of codimension two that contains pairs in which each conformer has algebraically independent
  coordinates [the referee's transcendence-degree argument; not checked by computer algebra].
* *Example D2* (`K₅` minus the edge 34 — generically globally rigid: rigidity rank 7, stress-matrix rank 2 at a
  random framework).  Two conformers that share the triangle 012: exchanging the positions of vertex 4 gives a
  second ensemble with the same law on every measured edge (200 of 200 random instances; with the edge 34
  measured the laws differ in 200 of 200).  **The laws of the distances from a rigid core to two mobile groups
  never tell whether the two motions are correlated.**  Hence generic global rigidity of the graph is not the
  criterion for conformers that share a rigid part, and "the general case is a contraction of the rigidity
  matroid" (version 2, §8) should be a question: here the graph is globally rigid and the ensemble is not
  determined.  (Your E7′ treats one relative rigid motion; D2 is a core and two independent parts.)

**M3 — exactness: no modulus is stated, and the margins are small.**

* *Proposition B* [P, five lines; re-derived by the coordinator].  If every edge law gives mass at least
  `1 − η_e` to the `τ`-neighbourhood of its atoms and `τ` is below the *chimera gap* `g_∞` (the least sup-norm
  distance from a splice that is not a conformer's vector to the realisable vectors), then all but `Σ_e η_e` of
  the ensemble lies within `τ` of a conformer.  For two conformers, if a colouring and its complement are both
  realised within `τ`, an ensemble within `τ` of every law has mass on two configurations that are not
  conformers.
* *The gap in numbers* [N; plane, conformer coordinates standard normal, so that the mean squared edge length is
  4; medians over six to eight random ensembles].  On minimally globally rigid graphs: `K₄` — `3·10⁻²`, `2·10⁻³`,
  `3·10⁻⁴`, `8·10⁻⁵`, `2·10⁻⁵` for 2 to 6 conformers; the wheels — `10⁻³` for two, `10⁻⁵` for three; single random
  ensembles at `8·10⁻⁷` and `1.2·10⁻⁹` (positive: the second verified in 40-digit arithmetic).  With redundancy:
  `K₅` `8·10⁻²`, `10⁻²`; `K₆` `0.1`.  The medians follow `(K^{|E|})^{−1/c}`, `c` the codimension of the measurement
  variety, within a factor of about six over four orders of magnitude.  **The coordinator's re-run with another
  seed** gives `8·10⁻³`, `1·10⁻³` (`K₄`, two and three conformers) and `1.1·10⁻³` (wheel, two) against the
  referee's `3·10⁻²`, `2·10⁻³`, `1.1·10⁻³`: the same orders; a median of eight ensembles is uncertain by a factor
  of up to four, and the smallest gap in that re-run is `4·10⁻⁶`.  Quote the orders, not the medians.
* *E8* [N].  The certificate has quadratic minima, so the sharp-minimum bridge of your Part I does not apply to
  Part II (version 2 says so for continua in general, E2.2).  With all `2K|E|` moments within a relative `10⁻⁵`,
  an explicit ensemble still has 3 – 76 % (`K₄`, three conformers) or 14 – 62 % (wheel, two) of its mass far from
  every conformer; the bound the certificate itself gives needs `10⁻⁸` to `10⁻¹⁹`; evaluating the mean of the
  certificate from moments is a cancellation of `10⁴` to `10⁹` for two and three conformers.  Even one
  conformation can be fragile: on one of three random wheels a visibly different framework reproduces all eight
  squared lengths to `7.7·10⁻⁵`.

**M4 — novelty classes** (register rows E5(a), E6, E7, E8: "new (not found)").  E5(a) is the dimension count of
your own proof (l.378–381); E7 is E6 plus the cited 2022 theorem — four lines — and its converse is the case of
one conformer; **the published proof of that Theorem 3.5 already splices the lengths of `p` and of `2p` along a
separator** [as returned by the fetch tool]; E8 adds the classical `2K`-moment certificate of a `K`-atomic measure
edge by edge.  What was *not* found in eighteen searches is the reading: a finite mixture of frameworks identified
from one law per edge.  Nearest neighbours found: unlabelled principal component analysis (Yao–Peng–Tsakiris,
Theorem 2 — a generic uniform ensemble on an unknown subspace from the multisets of its coordinates); echo sorting
(Dokmanić et al. 2013 — the no-chimera property with the genericity on the sensors); separately acquired distance
distributions (Hays–Boland–Kasson — the applied problem, no uniqueness statement).  "Not found" is eighteen
searches in one session.

## 3. Minor findings still open at version 2 (report §2; replacement texts there)

m1 "no `F_e` constant" is redundant in E5(a), needed in (b) and E6 · m3 (b) ⇒ (a) of E7 uses no cited theorem, and
the first cited theorem gives the full dichotomy: **not generically globally rigid ⇒ no generic finite ensemble
is determined** · m4 "modulo congruence": each conformer up to its own congruence, reflections included — no
handedness · m5 the count `2K|E|` is sufficient, not necessary: redundant edges need no moments; `2K − 1` per
edge suffice among ensembles of at most `K` conformers; **Proposition C** [P; re-derived by the coordinator]: for
a framework with a positive semidefinite stress matrix of maximal rank, `|E| + d(d+1)/2` means determine a single
conformation (9 instead of 12 on `K₄`) · m6 "`j ≤ 2` certifies a single conformation" presupposes a generic
unknown; genericity cannot be read off data, only replaced by a finite test of exponential cost · m9 **on any
graph with connected rigidity matroid a jointly generic finite ensemble is determined up to replacing each
conformer by an equivalent framework** — strictly more graphs than the globally rigid ones for `d ≥ 2` (two `K₄`
glued along an edge: no chimera, and a flip) · m10 the genericity statement your OB4 asks for is Definition 1.4 /
Corollary 1.15 of Gortler–Healy–Thurston.

## 4. Your scripts (re-run; `rigidity_checks.py` read in full)

With twenty other seeds your `test_R5` fails three times (a conformer is never reached by the 400 starts — its
control, not E8); version 2 changed the check.  `test_R3` passes with four of four seeds, but it samples 180
splices of two conformers and passes if the smallest residual exceeds `10⁻⁶`, on a graph where true negatives come
within a factor five of that threshold for two conformers and fall below it for three; it has no control on
vectors that are realisable (with the referee's solver one random start in three realises a realisable vector of
that wheel).  R4(b) examines one colouring of six; R6 is in the output and not in the text.

## 5. Requests (R21-EN-1 … -8; none authorises expenditure)

1. E1.3: the three residues of §0.
2. "Jointly generic" wherever E7/E8 are quoted without the definition; Examples D1 and D2; the sentence on
   contractions as a question.
3. A stability statement after E7 (Proposition B or your own), the chimera gap and the switching gap defined in
   O4, the gap of your own examples; for E8, that the certificate is not sharp.
4. The register: E5(a) "elementary; formulation", E7 "corollary of the cited theorem; reading not found", E8
   "classical per-edge certificate plus E7"; the headline as an implication.
5. State E6 for connected rigidity matroids (m9) and the full dichotomy (m3).
6. E5/E6 on an irreducible variety with a rational map: done in version 2; add irreducibility as a hypothesis.
7. Counts (m5).
8. Scripts: a planted control and an exhaustive method for R3; all colourings in R4(b); R6 in the text.

## Assumptions and limitations

Numerical work in the plane only; `d = 1` by hand; nothing in `d ≥ 3`.  E1–E4, Part III, Parts IV and V, E7′ and
the Lean files were not reviewed.  The cited papers were read as tool-made extractions.  Propositions B and C and
the two examples are paper proofs of the referee, re-derived or re-computed by the coordinator; none is
machine-checked.  The adversary of the E8 table is a lower bound of the worst case and the certificate's bound
an upper one; the truth is between.  The comparison with version 2 rests on the lines named in §0, not on a
second review.

## Requested response

None required.  If you apply the requests, a pointer to the commit is enough.
