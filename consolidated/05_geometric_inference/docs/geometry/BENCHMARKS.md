# Adversarial geometric test instances — proposals with mathematical ground truth

**Geometric Inference, Rigidity and Inverse Problems Division.**  Written at the eleventh
checkpoint for the Structural Biology division (software), the Engineering division
(independent verification and all substantial computation) and the Frontier Benchmarks
division (design and integrity of evaluations).

**What this is, and what it is not.**  It is a set of small synthetic instances — abstract
chains, no sequence, no chemistry — for each of which this division can state *what is
true*: the data determine the answer, or they provably do not (and here is a second
answer), or they do so only locally, or no certificate is known.  It is **not** a benchmark
run, an evaluation protocol or a comparison with other methods: designing and judging
evaluations is the Frontier Benchmarks division's mandate, running them is Engineering's,
and we do neither.  The instances are published in this repository, so they are
*development and adversarial* material; they can never serve as blind or held-out tests.
For held-out use the evaluating division should draw fresh instances with seeds of its own
from the generator (§5).

Files: `experiments/geometry/benchmark_instances.py` (generator; re-derives every label it
can and fails otherwise; one minute), `experiments/geometry/benchmark_suite/*.json` (the 23
instances, pinned) and `MANIFEST.json` (SHA-256 of each).  Format of an instance: `chain`
(bond length, bond angle, the statewise constraints), `data` (what a tool receives),
`truth` (states, weights), `label`, `expected_behaviour_of_a_correct_tool`,
`evidence_for_label`, `reference`, and, where the label is "not determined",
`second_solution`.

## 1. The six classes asked for, and the instances

| class | instances | what is true | evidence |
|---|---|---|---|
| **uniquely reconstructible** | A1, A2 (two states, 12 and 16 points), A3 (three states, 23 points); A4 (two states, 19 of 60 points observed: an anchor of 12 and 7 isolated labels — the labelled sites are determined, the others are not); B1 (two states, 11 points), B3 (three states, 17 points), B2 (two states, 10 points); C5 variant b (one conformation, distances of sequence separation at most 4) | the ensemble (the conformation) is the only one with the data | A: Theorem B with the certificate computed on the instance; B: Theorem I′ generically, floating point on the instance; C5b: Theorem L |
| **non-unique** | C1 (two states, 8 points), C2 (one differing torsion), C3 (two half-turn hinges), C4 (no statewise constraints supplied), C5 variant a (separation at most 3), C6 (two states, labels at every fourth point), G2 (a continuous family) | another ensemble (conformation) has the same data — **supplied** in the instance, data equal to `10⁻⁹` or better | by construction; C2, C3 also by theorem |
| **locally but not globally identifiable** | C1 | the Jacobian of (torsions, weight) ↦ data has full rank 11 of 11, and nine other chains reproduce the data | computed on the instance |
| **identifiable, but no efficient certificate known** | E1 (two states, 9 points), E2 (three states, 15 points); for tools limited to the linear certificate also B1–B3 | believed determined; neither the linear nor the quartic certificate applies | numerical (E1: 24 instances searched) and conjectural (E2) — **not theorems** |
| **numerically ill-conditioned** | F1a, F1b (two states differing by torsion changes of size `10⁻¹`, `10⁻³`), F2 (one nearly planar window), F3 (a helix of 100 points) | determined for exact data; rank decisions or error amplification are close to failing | computed condition numbers are in the instance |
| **violating essential assumptions** | C4 (no statewise constraints), G1 (two states with different bond angles, the tool told one), G2 (continuous), G3 (planar states), G4 (noise of relative size `10⁻²`) | the hypotheses of every theorem of ours fail | G1, G3, G4: our reference certificate refuses; C4, G2: theorems |

## 2. What a correct tool does, class by class

* **A.**  Returns the number of states, the states up to congruence (mirror images are the
  same shape) and permutation, the weights, **and the certificate**.  Tolerances we meet on
  exact data: RMSD `10⁻⁶`, weights `10⁻⁶`.  On A4 the answer concerns the 19 labelled sites
  only; reporting positions of the 41 unlabelled points as determined is an error.
* **B.**  A tool that has only the linear certificate answers "**not certified**" — not
  "not unique", and not a list of states without a caveat.
* **C.**  Does **not** report the truth as the unique answer.  Acceptable: "not certified";
  better: a description of what is determined (C2: the hinge, the rigid parts, the mean of
  `(cos, sin)` of the hinge angle).  A tool that searches within two-state models will find
  the truth on C1 — that is local identifiability, and the instance contains nine other
  chains with the same data.
* **E.**  "Not certified".  A tool that returns the truth here has not identified it; a tool
  that claims a certificate must exhibit one, and we would like to see it.
* **F.**  Reports conditioning (the eigenvalue and singular-value gaps of its rank
  decisions; the first-order amplification `1/(2μ)` for local distance data) and does not
  certify when a rank decision is not separated from its tolerance.
* **G.**  Refuses, with the reason.  In particular it does not pad a rank (G3), does not fit
  a finite list of states to a continuous family and call it the ensemble (G2), and does
  not print a certificate for noisy data (G4).

**Scoring that would be wrong.**  Counting "fraction of instances where the returned states
are close to `truth`" rewards a tool that guesses on C, E and G.  The quantity that
matters is the *confusion table* between what the tool claims (certified / not certified /
refused) and the label.  One confident wrong certificate on a C or G instance outweighs any
number of recoveries on A.

## 3. Ways to try to falsify our own claims (we would rather hear it from you)

1. **Find a second solution on an A or B instance.**  Any ensemble of chains with the
   stated bond geometry whose averaged squared distances agree with the data and whose
   states are not the listed ones refutes Theorem B (A) or Theorem I′ (B).  A global search
   over ensembles with more states than `K` is the natural attack; our internal referee's
   direct searches at 12 to 14 points found none (GEOMETRY-REV-0001), which is not a proof
   for these instances.
2. **Recompute the exact certificates independently.**  `exact_demix4.py` proves the quartic
   certificate at rational witnesses with ranks modulo a prime; an independent
   implementation (another prime, another algebra system, monomial instead of evaluation
   coordinates) that gets a different rank at the same witness refutes Theorem I′.  The
   witnesses are fixed by `(K, n, geometry, seed)` in the script.
3. **Break the linear certificate's soundness.**  Proposition 6.1 says: if the data are those
   of *some* ensemble with the stated constraints, the rank is `3K` and the nullity is
   `K − 1`, then the output is the unique ensemble.  A realizable data matrix on which the
   certificate holds and the output is wrong refutes it.
4. **Push the ill-conditioned families.**  F1 with smaller differences, F2 with a flatter
   window, hinges approaching half-turns: where does each implementation start to certify
   wrongly?  Our reference code has not been tested adversarially for false certificates
   in floating point — only for refusals.
5. **Check the obstructions.**  The second solutions of C1–C5 are data: verify that their
   states satisfy the constraints and reproduce the data, with your own code.

## 4. Computations that would settle open points (proposals — nothing here is a request)

| what | why | size | expected | stop |
|---|---|---|---|---|
| the quartic certificate for four states at 24 to 29 points, exact arithmetic | Conjecture 6.3 (first level works exactly from the dimension count) — smallest open case | exact rank of a matrix with up to 66 045 columns: about 9 GB as 16-bit integers; hours on a large-memory node | rank `C(m+3,4) − 4` at every length from 24 on | first length at which the rank is short |
| independent re-computation of the witnesses of Theorem I′ | the proofs are unreviewed | seconds to half an hour | the ranks of the table in §6.2 of the report | any disagreement |
| a noise sweep of the linear certificate on the A family | no noise theorem with a computable constant exists; an empirical map is the honest substitute | small | the certificate fails near relative noise `10⁻²` for two states at 12 points | — |
| a search for false certificates of floating-point implementations on the F family | §3 item 4 | small | none | first false certificate |

A request to Engineering would need a full specification, an expected result, a validation
criterion, resources and a stopping condition; none has been sent for these.

## 5. Drawing fresh instances

`benchmark_instances.py` builds every instance from a seed; changing the seeds gives new
instances of the same classes with the same self-checks (the C1 instance is the exception:
its second solution was found by a search of the internal referee and is loaded from
`experiments/geometry/review1/`; `explore_below.py 7 8` finds others).  Families that scale:

* `K` states, `n` points, generic torsions: class A for `n` at or above
  `⌈(9K² + K + 8)/4⌉`; class B at the lengths of Theorem I′; class E between the conjectured
  identifiability threshold `⌊9K/2⌋ + 1` and the certified one.
* hinge pairs with prescribed torsion changes: class C at one hinge or two half-turns,
  ill-conditioned near them, determined otherwise.
* helices and strands of growing length for local distance data: the amplification grows
  like `n²`.

## 6. Limits of these instances

Abstract chains with exact constraints and exact data.  They test whether software
respects mathematics that is true of this model; they say nothing about performance on
measured data, and passing them is not evidence of scientific usefulness.  The labels of
class E are numerical or conjectural.  The labels of class B rest on theorems that have
not been independently reviewed.
