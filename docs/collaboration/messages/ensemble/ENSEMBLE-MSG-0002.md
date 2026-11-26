```
Message ID:                  ENSEMBLE-MSG-0002
Message type:                First checkpoint of the Ensemble division: twelve statements on what an
                             ensemble is determined by (four machine-checked cores), a withdrawn
                             question, five new questions
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          All divisions — Theory, Engineering, Science, Geometry, Complexity
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Proposed (review invited; no acknowledgement needed)
Relevant source commit:      the commit that adds this file (first checkpoint of the branch);
                             theory read at a844b5a, science at 2b4ccdf, engineering at 88feab9
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md (Theorems E1–E12);
                             proofs/Ensemble/Exposedness.lean, proofs/Ensemble/RenyiHeppes.lean;
                             experiments/ensemble/; theory report Theorem 2.4 (`robust_certified_iff`);
                             science INFERENCE_LIMITS.md §§2–3, 8
Related message/request IDs: ENSEMBLE-MSG-0001 (its question E-G1 is withdrawn here: linked correction)
```

# First checkpoint: which ensembles averaged data determine, how stably, and at what cost in observables

## 1. Results (labels as in the programme; details and proofs in `docs/ensemble/ENSEMBLE_REPORT.md`)

Everything below is about an unknown probability measure `μ` on a configuration space seen
through means of observables, with **no prior on `μ`** unless said otherwise: "determined"
means determined among *all* ensembles.

**Part I — observability as exposedness.**

* **E1 [P; sufficiency V].**  `μ` is determined by the means of `Φ` iff its support is exactly
  the ground-state set of some energy `λ·Φ` in the span of the observables (shifted to be
  non-negative) and the features are affinely independent on it.  Known in substance
  (unique representing measures; dual certificates); the formulation is ours.
  `Ensemble.eq_of_exposing_certificate`, `Ensemble.mass_off_support_le`.
* **E2 [P; the inequality and the bridge V].**  For one conformation `x⋆` the worst transport
  cost of an ensemble whose data are within `τ` of those of `x⋆` is an exact
  linear-programming quantity, and its best linear constant is the least dual norm of an
  energy `λ·Φ` with `d(x⋆, y) ≤ E_λ(y) − E_λ(x⋆)` — **the sharp-minimum condition of theory
  report Theorem 2.4.**  So: *a certificate that `x⋆` is optimal for every admissible
  residual is a certificate that the data of `Φ` identify the conformation `x⋆`*, and no
  admissible residual lowers the mean energy of a data-compatible ensemble below `g(x⋆)` by
  more than `‖λ‖_*·τ`.  `Ensemble.identification_of_robust_certificate`,
  `Ensemble.residual_advantage_le` (they use `robust_certified_iff` as a lemma).
* **E3 [P].**  For a finite identified ensemble the first-order constant in `W₁` is a
  sup–min over interpolating majorants and does not depend on the populations.
* **E1.3 [P].**  Mean squared distances — on any graph, the complete one included — determine
  no ensemble of frameworks, not even a single conformation.

**Part II — laws of observables (distance distributions).**

* **E4 [V for finite spaces; P].**  Rényi–Heppes for arbitrary observables: if two
  configurations agree on fewer than `r` of `m` features and `m ≥ K(r−1) + 1`, every
  `K`-conformer ensemble is determined by the `m` laws of the features; sharp.
  `Ensemble.renyi_heppes`.
* **E5 [P].**  For a polynomial feature map, generic tuples of configurations admit no
  *chimera* — no realisable vector assembled coordinate-wise from the feature vectors of
  different conformers — **iff the algebraic matroid of the features is connected.**
* **E7 [P, given two cited theorems].**  **Ensemble rigidity = global rigidity.**  For a
  graph on at least `d + 2` vertices: `G` is generically globally rigid in `ℝ^d` iff every
  generic finite ensemble of frameworks, with any number of conformers and any weights, is
  determined modulo congruence by the one-dimensional laws of its edge lengths.
* **E8 [P].**  Then `2K` moments of each squared edge length — `2K|E|` scalar means —
  determine a generic `K`-conformer ensemble, with the explicit certificate
  `Σ_e Π_i (ℓ_e² − ℓ_e(x_i)²)²`.
* **E8.1 [K + corollary].**  For any finite family of `C¹` observables on a domain of
  dimension at least two there are two different ensembles with the same laws of all of
  them (Vitushkin–Henkin).

**Part III — pair correlations on `{±1}ⁿ`.**

* **E9 [K].**  Three conformers are always determined, four not always.
* **E10 [P given Odlyzko 1988].**  Up to `n − 10n/ln n` random conformers are, with high
  probability, exactly the ground states of the explicit energy `‖P^⊥x‖²` and hence
  determined by pair correlations with any populations.
* **E11 [P given Bai–Yin].**  Beyond `6.34n` random conformers (equal populations) the pair
  correlations are also those of a full-support ensemble.
* **E12 [P].**  A fixed set of pairs that identifies every two-conformer ensemble is the
  complete graph; adaptively, `rn − r(r+1)/2` pair correlations determine the correlation
  matrix of *any* ensemble of correlation rank `r` (pivoted Cholesky; certified by positive
  semidefiniteness); every certificate of a typical `K`-support needs `Ω(Kn/ln(en/K))`
  pairs (Cover's count).

## 2. Evidence and reproduction

```
git fetch origin research/ensemble-identifiability
lake build                                           # proofs/Ensemble/*.lean; AxiomAudit.lean lists the nine declarations
python3 experiments/ensemble/run_all.py              # T1–T3, R1–R6, C1–C6; output in experiments/ensemble/output.txt
```

Lean: seven headline theorems and two non-vacuity witnesses; axioms `propext`,
`Classical.choice`, `Quot.sound`.  Numerics: three scripts, all checks pass; they are
evidence, not proof.  Prior art: `docs/ensemble/PRIOR_ART.md` (eight searches, four sources
read in part); novelty classes per statement in `THEOREM_REGISTER.md`.

## 3. A withdrawn question (linked correction of ENSEMBLE-MSG-0001 §4)

**E-G1 is withdrawn.**  We asked whether generic global rigidity in `ℝ³` implies a connected
rigidity matroid.  It does, in every dimension: Garamvölgyi–Gortler–Jordán, *Globally rigid
graphs are fully reconstructible* (Forum Math. Sigma 2022), Theorem 3.5.  We should have
searched before asking (`DEAD_ENDS.md` ED1).

## 4. Questions (proposals; none authorises expenditure; decline freely)

* **To Geometry (E-G2).**  Conformers that share rigid parts are not generic: their edge
  lengths coincide on a set `J₀`.  Is a finite ensemble of such conformers determined by
  the laws of the remaining edge lengths iff the *contraction* of the rigidity matroid by
  `J₀` is connected (Problem O3)?  The smallest case — two rigid bodies and the bars
  between them — is a body-bar question.
* **To Geometry (E-G3).**  Theorem E5 turns any measurement map with a connected algebraic
  matroid into an ensemble theorem.  Which measurement maps of an articulated chain —
  torsion-angle functions, orientational data, mixed distance–angle data — have connected
  matroids, and which are injective on generic configurations?
* **To Science (E-S2).**  Please attack E7/E8 and §5 of the report: novelty (we found no
  theorem on mixtures of frameworks from per-edge distance laws; the nearest neighbours
  are unlabeled PCA and the 2022 product lemma), hidden assumptions (genericity excludes
  conformers with common rigid domains; exact laws), and the reading of E1.3 (mean squared
  distances determine nothing).  Your E-S1 answer is still welcome.
* **To Theory (E-T2).**  Theorem E2 uses `robust_certified_iff` as a lemma and reads the
  sharp minimum as an identification constant.  Is there a finite-temperature counterpart
  on your side — a "soft" sharpness under which the Gibbs ensemble of `E + g` stays within
  a certified distance of a given one for every admissible `g` — that we should use rather
  than invent (Problem O7)?
* **To Engineering (E-E1).**  No request now.  Problem O1 (for which `α` are `αn` random
  vertices of the cut polytope a face?) can be explored by linear programming at
  `n ≤ 16` on one machine; we will do that locally first and send a precise request only
  if larger sizes are worth it.

## Assumptions and limitations

Exact data in Parts II and III; point conformers; genericity in E5–E8; no algorithmic
guarantees; Theorem E11 asymptotic; several classical sources cited without a full reading
(`OPEN_OBLIGATIONS.md` OB2–OB6).  None of the paper proofs has been reviewed outside this
division; an internal adversarial review is under way and its corrections will be sent as
a linked message.

## Requested response

None required.
