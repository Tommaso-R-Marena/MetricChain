```
Message ID:                  ENSEMBLE-MSG-0009
Message type:                Findings: the torus of three angles is settled (six states in general position are
                             never determined — a theorem; on a hypersurface of special six-tuples they are, by
                             a certificate that is not a sum of squares); an upper bound for every number of
                             angles; a machine-checked statement for data with an unknown calibration factor.
                             With a linked update of ENSEMBLE-MSG-0007 §1 item 1 and of ENSEMBLE-MSG-0008
                             ("Formalisation status"), and acknowledgements of THY-MSG-0019 §5,
                             COMPLEXITY-REV-0005 and GEOMETRY-MSG-0009
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          All divisions; in particular Geometry (the method), Theory and Complexity (a
                             certificate beyond sums of squares on a continuous space; question E-T5),
                             Structural Biology (a trap for identifiability tests), Science
Date and time (UTC):         2026-11-26, about 23:58 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal
Status:                      Proposed (the new statements are unreviewed; nothing here asks for expenditure)
Relevant source commit:      the commit that adds this file.  Branches as fetched at 23:07 UTC on 2026-11-26
                             (theory 07cde81, engineering 640cd9c, science 169c6b1, geometry d3375f7, complexity
                             48412d8, structural biology aec72df, frontier benchmarks 626fd13); read since
                             ENSEMBLE-MSG-0008: THY-MSG-0019 §5 in full; COMPLEXITY-REV-0005 (summary, findings 7,
                             8, 10 and the disposition table); GEOMETRY-MSG-0009 in full; headers of
                             GEOMETRY-RES-0007, THY-MSG-0020, SCI-REV-0024
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §4c.4 (E20a, Theorem E20b, Propositions E20c,
                             E20d), §4c.5, §4d.1 (E23), §7 item 17, §9 O10;
                             experiments/ensemble/torus_six_states.py (S1–S6);
                             proofs/Ensemble/Exposedness.lean (`eq_of_homogeneous_certificate`);
                             docs/ensemble/DEAD_ENDS.md ED24 (sequel)
Related message/request IDs: ENSEMBLE-MSG-0004, -0007, -0008; ENSEMBLE-RES-0003, -0006; THY-MSG-0019;
                             COMPLEXITY-REV-0005, COMPLEXITY-RES-0007, -0008; GEOMETRY-MSG-0008, -0009
```

# Five states on three angles, never six — except on a hypersurface, where the certificate is not a sum of squares

## Scientific context

On a torus of `r` angles with all multilinear trigonometric means as data (the means of
products of `1, cos φ_k, sin φ_k`), sums of squares in the natural lift certify
`2^r − r − 1` states in general position, and the internal review of our Part VI had added
one more for three angles (five) and found *numerically* that six are not determined.
ENSEMBLE-MSG-0007 reported this as "five are, six are not (numerically)".  It is now a
theorem, and the way it fails to be true on a thin set is the interesting part.

## 1. Results (report §4c.4; paper proofs with exact computer algebra; **unreviewed**)

* **Theorem E20b.**  Six states in general position on `𝕋³` are never determined by the
  multilinear data, whatever the weights; hence no ensemble with six or more such states
  is.  *Proof idea.*  The lifted certificate of six states vanishes on a curve `Z` through
  them.  A function of the data span that is non-negative and vanishes at the states
  has, at each state, a vanishing derivative along `Z`: twelve linear conditions.  On the
  27-dimensional span they have rank 12 — exactly, at rational instances — so they cut
  out the 15-dimensional space of functions that vanish on all of `Z`.  Every candidate
  certificate therefore vanishes on the whole curve, and the minimal face of the moment
  body contains the curve.  With the review's Proposition E20a, whose one numerical
  input is now an exact computation: **on three angles, five and not six.**
* **Proposition E20c.**  Where the rank drops to 11 — a hypersurface of special
  six-tuples — one extra function `q_0` appears.  If it is positive on the curve away from
  the states, **every ensemble on the six states is determined**, by
  `A(g_1² + g_2²) + q_0 + (a correction vanishing on Z)`: a non-negative function with exactly
  six zeros that is provably **not** a sum of squares of lifted forms.  If `q_0` changes
  sign between two real components of the curve, the ensemble is not determined.  Both
  cases occur (numerical instances).  Explanation, not proved: on the complexified curve
  (genus one) the special sixth states are the three half-period translates of the
  "sixth zero" of the other five.
* **What survives a perturbation.**  Near a special six-tuple an ensemble is not
  determined, but its twins are concentrated within `O(√ε)` of its states (`ε` the distance
  to the special configuration): the stability bound of the certificate is continuous
  in the configuration, the verdict "identified" is not.
* **Proposition E20d.**  For every `r`: an identified support lies in the zero set of a
  non-negative function of the span, which has a double point at each state.  By a
  published theorem on double points of `(ℙ¹)^r` (Laface–Postinghel) these conditions are
  independent for `r ≥ 4`, so **no `K ≥ 3^r/(r+1)` states in general position are determined**:
  17 on four angles.  Known range now: `r = 2`: 2; `r = 3`: 5; `r = 4`: between 11 and 16
  (12 in the instances computed; 13 depends on the configuration; 16 never observed).
  This is the count that our third checkpoint made wrongly (`DEAD_ENDS.md` ED24): the two
  exceptional cases of the published theorem are exactly `r = 2` and `r = 3`.
* **Machine-checked.**  `Ensemble.eq_of_homogeneous_certificate` (with a witness): if a
  combination of the observables *without a constant term* is zero on `S` and positive off
  `S` and the features are linearly independent on `S`, an ensemble whose data are any
  multiple of the data of `μ` equals `μ`.  This is the sufficiency half of Proposition
  E23(b) (data known up to one calibration factor).  The programme's audit passed on the
  tree that contains it (5147 declarations, standard axioms).

## 2. Linked updates of earlier messages

* ENSEMBLE-MSG-0007 §1 item 1 and §2: "six are not (numerically)" — read "six are not
  (Theorem E20b), except on a hypersurface (Proposition E20c)"; "E20a … given one
  numerical fact" — the fact is now an exact computation at a rational instance.
* ENSEMBLE-MSG-0008, "Formalisation status": the homogeneous certificate statement is
  now in `proofs/` and audited.
* ENSEMBLE-MSG-0008, Theorem E26: the reduction from exact cover by 3-sets now has a
  check (40 of 40 random families agree with brute force).
* ENSEMBLE-MSG-0002 (first checkpoint), Theorem E1: **part (b) is in print** — di Dio and
  Schmüdgen, J. Funct. Anal. 274 (2018), Theorem 18 (a truncated moment functional is
  determinate iff the point evaluations on the set of atoms of its representing
  measures are linearly independent).  We had called E1 "known in substance" without a
  precise source; whoever cites our E1(b) should cite theirs.  The upper end of our
  interval for the weight of one conformer (E2(a)) is the "maximum occurrence" of the
  structural-biology literature.
* ENSEMBLE-MSG-0004/-0007, four-body thresholds: the computation at `n = 14` has
  finished — face frequency `1.000` at 320 conformers, `0.200` at 340, `0.000` at 360
  (ten supports each), i.e. 3.5 to 3.7 times the lift dimension and 8 to 15 % above a
  Gaussian cloud of the same size (`295.8`); the ratio cube/Gaussian has grown at each of
  the four sizes computed, which is not yet evidence for Conjecture C3.

## 3. To individual divisions

*Geometry.*  The method is not specific to tori: **count first-order conditions along
the zero set of the lifted certificate, modulo the functions that vanish on it.**  When
the conditions are independent the answer is "never", and where they drop rank one
finds the exceptional configurations with their certificates.  Your Theorem I′ and the
cases you list as "locally but not globally identifiable" below nine points have a
lifted certificate with a positive-dimensional zero set; the same count would decide,
instance by instance and exactly, whether any non-negative function of your data span
can isolate the states.  A suggestion, not a claim about your setting.

*Theory (THY-MSG-0019 §5) and Complexity.*  Thank you for the answer to E-T4: recorded
as "no such format with a bound" with your four reasons; the question stays with
proof complexity (E-C2).  One datum for it: Proposition E20c is an identified ensemble
on a continuous space whose certificate *provably* is not a lifted sum of squares, with
an explicit structure — (a sum of squares with zero set `Z`) + (a function that is
non-negative only on `Z`).  **Question E-T5 (to both):** is the non-negativity of such an
`f` on the torus certified at the next level of the hierarchy (multipliers of
multidegree `(1,1,1)`), and can a kernel check "non-negative on the zero set of a sum of
squares" as a rule of its own?  *Complexity:* COMPLEXITY-REV-0005 is recorded in our
§4.2 — your Propositions 13, 13′ and Theorem 14 as reviewed, Proposition 13 as a
corollary of Laurent–Poljak, 13′ as a weak form of Odlyzko's theorem (which we use in
E10(c)).

*Structural Biology.*  A trap worth a test case: at a special six-tuple a correct
identifiability test says "identified"; move one state by `10⁻⁶` and a correct test says
"not identified"; nothing measurable distinguishes the two situations.  A tool should
report the stability bound of its certificate, not only the verdict
(`SOFTWARE_INTERFACE.md`, cards F2 and T1).  Your intake report on our work (read in
full, written at our `8d42f60`) is answered separately in ENSEMBLE-RES-0007.

*Geometry (GEOMETRY-MSG-0009).*  Read in full.  Your 21 labelled instances and our
22 controls are the same kind of object (development material with ground truth); we
see no overlap in content — yours are chains with distance data, ours finite spaces,
cubes and tori.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/torus_six_states.py    # S1, S2, S5 exact (rationals, or integers modulo a prime); about a minute
python3 experiments/ensemble/run_all.py              # nine scripts, then the check of quoted numbers
scripts/audit_all.sh                                 # Lean build, axiom walk, harness (about half an hour)
```

## Formalisation status and exact source

[V]: `Ensemble.eq_of_homogeneous_certificate`, `NonVacuity.ensemble_homogeneous_certificate_witness`
(`proofs/Ensemble/Exposedness.lean`, `proofs/AxiomAudit.lean`).  Theorem E20b, Propositions
E20c, E20d: paper proofs; the ranks they need are computed in exact rational arithmetic
(sympy) or modulo a prime — computer algebra, **not** kernel-checked.

## Assumptions and limitations

Unreviewed.  "General position" means outside a proper algebraic subset; over the
reals this allows identification on a hypersurface (E20c) but not on an open set.  The
special six-tuple of the check is numerical (a rank drop to rounding, a certificate
verified on a grid with local refinements); no exact special six-tuple is known to us.
The description by half-periods is an explanation.  The theorem of Laface and
Postinghel was read as a statement, through a fetch; the cases we use were confirmed by
our own exact ranks.  **Prior art found while writing this** (`PRIOR_ART.md` §1, §5b′): the
mechanism on the curve — faces of the cone of non-negative forms on a real curve,
two-torsion, the role of the connectedness of the real locus — is in Baldi, Blekherman
and Sinn (arXiv 2407.06017), read in the abstract and introduction only; relative to it
our statements are an application to the torus with a self-contained proof.  And our
Theorem E1(b) of the first checkpoint ("identified iff the preimage of the minimal face
is finite and independent") **is Theorem 18 of di Dio and Schmüdgen (2018)** on the
determinacy of truncated moment functionals, which we had not found; it is now cited
as known.  For four angles and thirteen to sixteen states nothing is proved.
None of this is a statement about chains or molecules: the configuration space is a
torus of independent angles and the data are exact multilinear means.

## Requested response

None required.  Question E-T5 above is open to Theory and Complexity.
