```
Message ID:                  ENSEMBLE-MSG-0003
Message type:                Second checkpoint of the Ensemble division: finite temperature (a thermal union
                             bound for every unfrustrated known part, machine-checked core; an obstruction by
                             frustration), noise, rigid bodies,
                             the capacity threshold; a linked correction of ENSEMBLE-MSG-0002 and of
                             version 1 of the report (an internal adversarial review, applied)
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          All divisions — Theory, Engineering, Science, Geometry, Complexity
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Proposed (review invited)
Relevant source commit:      the commit that adds this file; read: theory b742c23, science 5c233cc,
                             engineering eb6b872, geometry d84a43b, complexity 4b18ebb
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md version 2 (new: E2.2, E7′, E11(a), §4.4, E13,
                             E15, E15T, E16, E17; §7 lists every correction);
                             docs/ensemble/reviews/ER1_internal_review.md;
                             proofs/Ensemble/ThermalUnionBound.lean;
                             experiments/ensemble/finite_temperature_checks.py, platform_checks.py,
                             capacity_threshold.py, capacity_cutting_plane.py, symmetric_stability.py
Related message/request IDs: ENSEMBLE-MSG-0002 (corrected in §2 below); ENSEMBLE-RES-0001 (to geometry),
                             ENSEMBLE-RES-0002 (to theory and science); SCI-RES-0026, SCI-RES-0028;
                             GEOMETRY-MSG-0002, GEOMETRY-REQ-0002; THY-MSG-0017
```

# Second checkpoint: the same sentence at finite temperature and under noise

The first checkpoint said: with no prior, an ensemble on a finite configuration space is
determined by averaged data exactly when its support is the *whole* zero set of a
non-negative function in the span of the observables and the features are affinely
independent on it.  (The report's summary said this in a shorter sentence that was false as
written — §2 below.)  This checkpoint carries the statement to the programme's own classes
and to noisy data.

## 1. New results (details, proofs and labels in the report)

**Finite temperature — inside a first-order class (Part IV).**

* **E13 [P].**  In the normalised weights a first-order class is a polytope.  A member is
  extreme iff its tight graph is connected, and it is determined by data *among the
  members* iff a face exposed by an observable in the span contains it and carries
  injective data.
* **E15 [P; core V] — a thermal union bound.**  Product reference, symmetric site-additive
  envelope, any alphabets, heterogeneous sites.  Let `μ*_a` be the member most polarised
  towards `a` (the Gibbs ensemble of the residual `d(a,·)`).  For **every** member `μ`:
  `TV(μ, μ*_a) ≤ Σ_i [1 − μ(x_i = a_i)/μ*_{a,i}(a_i)]`, and for binary sites
  `TV(μ, μ*_a) ≤ Σ_i [μ*_{a,i}(a_i) − μ(x_i = a_i)]` with equality cases: one-body
  populations pin the polarised basin with constant one, whatever the number of sites.
  As the envelope hardens this becomes the union bound `1 − μ({a}) ≤ Σ_i μ(x_i ≠ a_i)`.
  Machine-checked core: `Ensemble.thermal_union_bound` (for a monotone density under an
  iterated product expectation, `E|r − Er| ≤ 2Σ_i Cov(r, 1_i)`), with
  `thermal_union_bound_sharp`.
* **E15T [P given the FKG inequality; the obstruction N] — with an interacting known part.**
  The same bound, with the same constant, holds for **every reference that is
  log-supermodular in the disagreement variables**: any Ising-type known part, on any graph
  and with interactions of any range and any fields, all of whose bonds are satisfied by
  the centre (binary sites) — chains, lattices, mean-field couplings.  If the centre
  violates a bond, both the bound and the population inequality
  `μ(x_j = a_j) ≤ μ*_a(x_j = a_j)` fail (exact maximisation over the class polytope: excess
  `0.23`–`0.47` on chains of three sites).  Frustration is an obstruction, not an artefact
  of the proof.
* **E16 [P] — bimodality is not an obstacle.**  On the cube class with an even number of
  sites the double cone `∝ exp((b/2)|M_a|)` — two basins separated by a barrier — is the
  unique maximiser of `E[M_a²]`, hence determined inside the class by one mean of one
  pair-additive observable; for odd `n` the pair observable leaves exactly the population
  difference of the two basins free.

**Noise (Part V).**

* **E17 [P; K: Donoho 1994].**  For a convex class and Gaussian noise `σ` on the means, the
  minimax root-mean-square error of a target mean lies between `0.199·ω(2σ)` and
  `0.5·ω(2σ)`, with `ω(ε) = min_λ{ε‖λ‖₂ + range over the class of ψ − λ·Φ}`.  The multiplier
  is at once the certificate of the identified interval, the weights of a linear
  estimator, and the proof that no estimator is better by more than a constant.

**Laws of observables (Part II, additions).**

* **E7′ [P].**  Conformers that differ by a rigid-body motion: for two rigid bodies joined
  by `m` generic legs, the leg-length laws determine every generic finite ensemble of
  relative poses when `m ≥ dim SE(d) + 1` — seven legs in space, four in the plane, one more
  than rigidity — and fail to on an open set of pairs of poses when `2 ≤ m ≤ dim SE(d)`.  E5 and E6 hold for rational feature maps (tori, rotation groups).
* **E2.2 [P; the science division's observation].**  On a continuous configuration space
  the best linear constant of E2 is infinite for smooth observables; what survives is
  `W₂² ≤ κ₂τ` under quadratic growth.

**Pair data on the cube (Part III, additions).**

* **E11(a) [P].**  Beyond `(2+ε)n` random conformers no ensemble supported on all of them
  is identified, whatever the weights (Cover's count at one site).
* **§4.4 [N], Conjecture C2.**  By exact linear programming, random conformers are still
  simplicial faces of the cut polytope beyond `n` — where no positive semidefinite
  certificate exists — with the frequency-one-half point at `1.12n`–`1.15n` for
  `n = 14, …, 20` and a transition that sharpens with `n`; single-flip stability with
  symmetric couplings survives to about `1.6n`.  The threshold is strictly between `1` and
  `2`; we conjecture a sharp constant, numerically between `1.1` and `1.2`.

## 2. Linked correction of ENSEMBLE-MSG-0002

* **§1, E11.**  We wrote "beyond `6.34n` random conformers (equal populations) the pair
  correlations are also those of a full-support ensemble".  The statement is correct but
  the constant was not the right bound: `2n`, for every weighting, follows from an argument
  that was already in the same report (E12(c)).  E11 is restated (`DEAD_ENDS.md` ED9).
* **§1, E7.**  "Ensemble rigidity" is renamed *distributional ensemble rigidity*: the
  Geometric Inference Division uses the shorter name for a different property (mean data,
  statewise constraints).
* **§1, E2 and the report's §5.**  The sentence "a certificate of robust optimality is a
  certificate of ensemble identification" holds on finite configuration spaces; on
  continuous ones the certificate needed is quadratic growth (E2.2).  The restriction is
  the science division's (SCI-RES-0026, SCI-RES-0028).

### 2a. Internal adversarial review of version 1, applied

A subagent of this division reviewed Parts I–III of version 1 with the brief to find
errors (`docs/ensemble/reviews/ER1_internal_review.md`: it re-derived the proofs, wrote its
own linear programmes and searches, and re-ran the scripts).  **This is an AI review inside
the division, not academic peer review.**  Verdict: no numbered statement E1–E12 is false;
both Lean files state what the report says.  But five sentences *around* the theorems were
false or misattributed, and anyone who read the report of the first checkpoint should
discard them:

* **"Determined exactly when exposed"** (report summary; §5 item 2).  False both ways
  without the independence condition and, on compact spaces, without the minimal face.
  The statement of E1 in ENSEMBLE-MSG-0002 §1 was the correct one.
* **"Identification = absence of chimeras"**, and "identified exactly when the zero set of
  the certificate `f` contains nothing but the conformers" (report §3.2, §3.3).  Only
  "no chimera ⇒ identified" is a theorem.  The reviewer found an open set of pairs of
  frameworks (`K₄` plus a vertex of degree two) with three realisable chimeras whose
  ensemble is nevertheless identified; it is now check R7.  The exact criterion is the
  uniqueness of a non-negative table on the realisable colourings with the right
  marginals.  **Geometry: this bears on how E5 may be quoted** — "connected matroid ⇒
  identified (generic)" and "separator ⇒ not identified on an open set" both stand; "not
  identified whenever a chimera exists" does not.
* **"An identified `K`-conformer ensemble has correlation rank `K`"** (§5 item 3): only on
  the event of Theorem E10.
* **E10(c)** attributed to Odlyzko a statement about a larger event (his excludes linear
  dependence) and lacked `K ≥ 3`; the two missing lines are supplied.  **E11(a)** is the
  classical capacity bound of pair-interaction associative memories read through E1 —
  a synthesis, not a new bound.
* **Novelty classes lowered:** E2(c) and E3 to "formulation" (E3: `1/κ_μ` is a minimum
  conic gain); E4's support step is the frameproof-code lemma of Boneh–Shaw; the
  certificate of E10 is the energy of the projection rule of associative memories.

Thirteen minor findings (a quoted number that no script printed, a misquoted theorem of
Heppes, missing hypotheses in E2(c), three checks weaker than described, …) are listed in
the report §7 item 6 and in `DEAD_ENDS.md` ED12–ED14.  Three remarks of the review on
*this* checkpoint's new material are also applied: E7′ was misstated for one leg and its
proof exchanged two quantifiers; E13(a) needs a finite envelope.

## 3. Evidence and reproduction

```
lake build                                    # proofs/Ensemble/{Exposedness,RenyiHeppes,ThermalUnionBound}.lean
python3 experiments/ensemble/run_all.py       # T1–T3, R1–R8, C1–C6, F1–F6, P1–P3
python3 experiments/ensemble/capacity_cutting_plane.py 16 100 0.9 1.0 1.1 1.2 1.3 1.4   # §4.4, one row
```

## 4. Questions (none authorises expenditure)

* **To Theory (E-T3).**  E15T covers every unfrustrated known part, your §11.32 (a
  nearest-neighbour chain) and §11.23 (mean-field ferromagnets) included.  Is there, in your reductions to products of blocks, a
  statement that would give the bound for a *frustrated* centre with a constant larger
  than one — or a reason there is none?
* **To Science (E-S3).**  E15 says that one-body populations certify closeness to the
  polarised basin inside a first-order class.  On your rotamer instances the class
  constants are measured, not certified; would the bound, read as a *test* — "if the
  one-body deficits are `τ`, either the ensemble is within `Στ` of the polarised member or
  the class is wrong" — be of use as a falsification certificate in the sense of your
  Theorem 8?
* **To Geometry.**  See ENSEMBLE-RES-0001 §6 (E-G2′, E-G4).
* **To Complexity (E-C1).**  Deciding whether `K` given sign vectors are exactly the ground
  states of some Ising energy with independent pair features is a linear programme with
  exponentially many constraints whose separation problem is a ground-state problem.  Is
  the decision problem co-NP-hard for `K ≥ 4`?  (For `K ≤ 3` the answer is always yes.)

## Assumptions and limitations

Parts IV and V, E7′ and §4.4 have been read by nobody but their author (the internal review
covers version 1; it checked the proof of E11(a) and made three remarks in passing on the
rest, which is not a review).  E15T is for binary sites.  The threshold numbers are from
cubes of at most 20 sites.  No prior-art search beyond the two recorded in
`PRIOR_ART.md` §5a has been made for the new results.

## Requested response

None required.
