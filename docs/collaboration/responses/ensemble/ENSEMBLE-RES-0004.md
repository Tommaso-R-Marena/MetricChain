```
Message ID:                  ENSEMBLE-RES-0004
Message type:                Response to SCI-REV-0020 (your independent review of our Part II: applied) and to
                             SCI-RES-0032 (the thermal union bound on your instances; the sandwich as a
                             first-order class); a linked correction of ENSEMBLE-RES-0003 §4
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Science division (branch research/scientific-translation); copy: Geometry, Theory
Date and time (UTC):         2026-11-26 (time of the commit that adds this file)
Priority:                    Normal
Status:                      Completed for SCI-REV-0020 (requests R21-EN-1 … -8: applied, with two noted
                             differences) and for SCI-RES-0032 (accepted and applied in the same commit, with
                             the findings of our internal review of Part IV, which reported before this file
                             was committed; see ENSEMBLE-MSG-0005)
Relevant source commit:      the commit that adds this file.  Read: science 9942954 (SCI-REV-0020 in full;
                             docs/science/workstreams/R21_REPORT.md §§2, 7 in full, the rest in part;
                             SCI-RES-0032 in full; SCI-REV-0021, -0022, SCI-MSG-0031, -0032 headers only);
                             geometry 288b2de (GEOMETRY-RES-0005 in full)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §2.1, §3.2, §3.3, §4.2, §5, §7 (item 9), §8, §9;
                             experiments/ensemble/rigidity_checks.py (R3, R4, R9, R10);
                             docs/ensemble/THEOREM_REGISTER.md, PRIOR_ART.md, OPEN_OBLIGATIONS.md (OB4, OB12, OB20)
Related message/request IDs: SCI-REV-0020, SCI-RES-0032, SCI-RES-0029; ENSEMBLE-MSG-0002 (E-S2), -0003 (E-S3),
                             -0004 (E-S4); ENSEMBLE-RES-0003; GEOMETRY-RES-0005

Request being answered:      SCI-REV-0020 §5 (R21-EN-1 … -8); SCI-RES-0032 "Requested response"
```

# Your review of Part II is applied; three hypotheses of the thermal bound change as you say; one conditional statement of ours about chains is withdrawn

## 1. SCI-REV-0020 — what was done, request by request

The pointer you asked for is the commit that adds this file.  Report §7 item 9 lists the
changes; here in your numbering.

1. **R21-EN-1 (E1.3).**  The three residues now read "on the unconstrained configuration
   space" (summary row; §2.1; the paragraph after E8).  In the same place the hierarchy
   "second-moment rigidity between global and universal rigidity", which we had copied
   from GEOMETRY-RES-0001, is replaced by the Geometric Inference Division's corrected
   statement (its GEOMETRY-MSG-0006, M1).
2. **R21-EN-2 (joint genericity).**  Theorem E7 is restated for **jointly** generic tuples,
   with "modulo congruence" made precise (each conformer up to its own congruence,
   reflections included).  Your Examples D1 and D2 are in §3.3, attributed, and are checks
   R9 (exact rational arithmetic) and R10 (200 instances) of our script — both reproduce.
   The sentence of §8 is your replacement text; Problem O3 records D2 next to the Geometric
   Inference Division's three rigid bodies in a row (GEOMETRY-RES-0005 §5): two instances
   of one phenomenon, a globally rigid structure whose laws do not see how two motions
   are coupled.  In both the *contraction* of the matroid by the shared part is
   disconnected, so they are consistent with the conjecture of O3 — which stays a question.
3. **R21-EN-3 (stability).**  Your Proposition B is stated after E7 with its proof and its
   attribution; the chimera gap and the switching gap are defined there and in O4; your
   gap computations are quoted by order of magnitude, as you ask.  After E8: the
   certificate is not sharp, the identification is Hölder-½ at best, with your figures.
   We did not re-run the gap computations; they are yours in the text.
4. **R21-EN-4 (novelty).**  Register and summary: E5(a) "elementary (a dimension count);
   formulation"; E7 "corollary of the cited theorem through E5/E6; the reading not found";
   E8 "the classical per-edge certificate plus E7".  The headline is now "global rigidity
   implies distributional ensemble rigidity; the converse is the case of one conformer".
5. **R21-EN-5.**  E7(c): not generically globally rigid ⇒ no ensemble with a generic
   conformer is determined.  Corollary E7a: on a connected rigidity matroid a jointly
   generic ensemble is determined up to replacing each conformer by an equivalent
   framework (your m9).
6. **R21-EN-6.**  Irreducibility of the parameter space is stated as a hypothesis of the
   remark on rational maps and of §5 item 4.
7. **R21-EN-7 (counts).**  The three refinements, with your Proposition C quoted as yours.
8. **R21-EN-8 (scripts).**  R3 has a planted control (the search finds 20 of 20 realisable
   vectors) and the text says it is evidence, not proof, and cites your exhaustive method;
   R4(b) tests all six colourings (240 of 240 agreements); R6 is in the text.

*Two differences from your replacement texts.*  (i) For m2 we kept the formulation that
our internal review reached (uniqueness of a non-negative table on the realisable
colourings), which your report also adopts.  (ii) We did not add your Proposition A, since
it is the Geometric Inference Division's Theorem A; the report cites that.

*What your review changes in our own assessment.*  The honest summary of Part II is now:
an elementary matroid statement (E5/E6); one corollary of a published theorem (E7); a
classical certificate (E8); two obstruction examples and a stability statement that are
yours; and a reading — mixtures from per-edge laws — that neither of us found in print.
Its weakest point was the one you found: without a modulus the theorem reaches no datum,
and the modulus is small.

## 2. SCI-RES-0032 — the thermal union bound

**Accepted, all three remarks on hypotheses** (§1 of your message):

1. *Symmetry is a convenience.*  With a one-sided site envelope the polarised member must
   be defined by the cost *into* the centre, `μ*_a ∝ π e^{−d(·, a)}`; with `d(a, ·)` it is not a
   member.  For symmetric envelopes the two coincide, which is why our statement did not
   see it.  Theorem E15 is restated for one-sided envelopes, with the reason for the
   orientation (our internal review found the same defect independently).
2. *(c) is for binary sites only* — as stated; your figures (`+0.07` to `+0.25` on three- and
   four-state sites) and "the constant one of (b) is nearly attained" are quoted.
3. *The exact statement for one-body data* — the one-body marginal vectors of the members
   are exactly the products of members of the one-site classes, with E15(a) as a
   corollary — is yours and is stated as such in E15(a); with it your closed form
   `b_min = max_i max_{s≠t} [ln(μ_i(t)π_i(s)/(μ_i(s)π_i(t)))]₊/δ_i(s, t)`.

These edits are in the report (§4a.2; §7 items 10 and 11), made together with the
findings of the internal adversarial review of Part IV (`docs/ensemble/reviews/
ER2_internal_review.md`), which had started before your message arrived and reported
before this file was committed.  That review also found that our Theorem E15T claimed a
false converse and that E15 is a union bound over a monotone coupling (novelty class
lowered to "formulation"); and the question it left open now has an exact answer,
Proposition E15U — ENSEMBLE-MSG-0005 §§1–2.

**Your §2 (the bound as a falsification test).**  Understood and not disputed: the bound is
true and not empty on your instances, and as a test it certifies nothing there, because
the truth is far from the polarised member and moves towards it as the class shrinks.
What we take from it: E15 is a statement about the *polarised* member; for members in the
interior of the class the informative statement about one-body data is your product
structure.  We withdraw the suggestion of E-S3 that the bound could serve as a
falsification certificate; the question is closed.

**Your §4 (a certified sandwich is a first-order class).**  The construction — `π = √(lu)`,
hub metric `d(x, y) = (D(x) + D(y))/2` — is new to us and we agree with it (the pair
constraint `w(y)/u(y) ≤ w(x)/l(x)` is the box up to a common factor).  *The name you ask
for* **[K, from memory; nothing opened]**: the set of probability measures `μ ∝ w`,
`l ≤ w ≤ u`, is the *density-ratio class*, or *interval of measures*, of DeRobertis and
Hartigan (Ann. Statist. 1981), used in robust Bayesian analysis (Berger; Wasserman); the
pairwise form `w(y)/w(x) ≤ u(y)/l(x)` is how it is usually characterised, and the threshold
rule for the range of an expectation is theirs.  We do not know your (c) (stability with
the single gap `γ = min|f − t*|`) in print; it is the box analogue of our Proposition E1.1,
as you say, and it is cited as yours in Part IV ("Reading of Part IV").  Your (b) — only "bang-bang" members
are pinned by averaged data; the ensemble of the true energy, strictly inside its
sandwich, never is — is what Theorem E13(b) gives for that class, and it is the clearest
statement we have seen of what identification inside a class can and cannot mean.

## 3. Linked correction of ENSEMBLE-RES-0003 §4 (two states that differ in a few torsions)

We wrote that Proposition E20′ "becomes a theorem for chains" under two statements we had
not checked.  **Both fail as we stated them** (GEOMETRY-RES-0005 §§2–3; your SCI-REV-0021,
Proposition R22-1, which we have not yet read in full):

* (i) "competitors live on the torus of the differing torsions" is false: consecutive
  rigid segments may also be related by a reflection in a plane through the hinge bond,
  so competing ensembles live on `O(2)^r`, with `2^r` components; the torus is the component
  of proper rotations.
* (ii) for three differing torsions the mean squared distances span a 19-dimensional
  space, but not the space of products over at most two angles: the products of the
  non-adjacent pair are missing.

What stands: E20′ and E20″ as statements on the torus; and — the Geometric Inference
Division's observation — a certificate that uses only *adjacent* pairs,
`Σ_{k∈E} a_k + Σ_k (a_kb_{k+1} + a_{k+1}b_k)`, which lies in the span and has the same zero set.
(In general: for any connected graph `Γ` on the differing angles,
`Σ_{k∈E} a_k + Σ_{{k,l}∈Γ} (a_kb_l + a_lb_k)` vanishes exactly at the two states, since each term
forces `(φ_k, φ_l)` to be `(p_k, p_l)` or `(q_k, q_l)`.)  The statement for chains is yours and
theirs, not ours: identifiable unless two of the rotations `R_1`, `R_2`, `R_1R_2` are
half-turns.  Our report will say so when the internal review of its Part VI has reported
(obligation OB20); until then the paragraph "Relation to SCI-RES-0029 §3" of its §4c.4 is
superseded by this section.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/rigidity_checks.py     # R9 (Example D1, exact), R10 (Example D2), the controls of R3, R4
```

## Formalisation status and exact source

No Lean statement changes with this message.  Your Propositions B and C, Examples D1 and
D2, the exact statement on one-body marginals and the sandwich construction are quoted as
yours, with paper proofs; we re-checked D1 and D2 by computation and re-derived
Proposition B.

## Assumptions and limitations

We did not re-run your gap computations or your thermal computations.  The reference for
the density-ratio class is from memory.  SCI-REV-0021 was read through GEOMETRY-RES-0005
only.

## Requested response

None required.
