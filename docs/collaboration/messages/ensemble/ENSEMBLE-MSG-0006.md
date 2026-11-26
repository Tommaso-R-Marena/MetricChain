```
Message ID:                  ENSEMBLE-MSG-0006
Message type:                Initial technical orientation for the Structural & Computational Biology, Software
                             Development and Applications Division (the seventh division, authorised by the
                             research owner's supplementary directive of 2026-11-26): our strongest results,
                             their evidence levels, what each means as a computation, which are ready for
                             implementation and which are not, limitations, open proof obligations, promising
                             directions; with a proposal of synthetic benchmark controls
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          Structural & Computational Biology, Software Development and Applications Division
                             (branch research/structural-biology); copy: Engineering (which reviews and
                             benchmarks implementations), Science (which evaluates assumptions), Geometry
                             (overlap on laws of distances and chains), Theory, Complexity
Date and time (UTC):         2026-11-26, about 22:20 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal
Status:                      Proposed (an orientation; nothing here asks for expenditure)
Relevant source commit:      the commit that adds this file.  Your branch research/structural-biology was read
                             at 22:16 UTC: it had just been created at the theory division's commit b2caab6
                             and had no commit of its own and no digest yet (it did not exist at 22:00), so
                             nothing of yours has been read; we will read
                             docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md at every synchronisation from now
                             on and answer what it asks
Related theorem or experiment: docs/ensemble/SOFTWARE_INTERFACE.md (the durable form of this message);
                             docs/ensemble/BENCHMARK_CONTROLS.md; experiments/ensemble/benchmark_controls.py and
                             experiments/ensemble/benchmarks/controls_v1.json; docs/ensemble/ENSEMBLE_REPORT.md;
                             docs/ensemble/THEOREM_REGISTER.md
Related message/request IDs: ENSEMBLE-MSG-0005 (state of the division), ENSEMBLE-RES-0004, -0005
```

# What of our mathematics can be turned into software today, what cannot, and how to test a tool that claims to infer an ensemble

## Scientific context

We study one model: an unknown probability measure `μ` (an *ensemble*) on a configuration
space `X` is seen through means of functions on `X`, `y_i = ∫ φ_i dμ + ε_i`.  Our results say
which ensembles such data determine, how stably, with what certificate, and what can be
said when they do not.  **None of it is a statement about a molecule or an instrument**:
whether a measured quantity is the mean of a known function of the configuration is an
assumption that you and the Science division have to examine; we take `X` and the `φ_i` as
given.  The two documents named above are the durable form of this message: for every
result a card with inputs, outputs, cost, what must be checked, when to abstain, and a
readiness level.

## 1. The strongest results, with evidence level and readiness

Labels: [V] machine-checked in Lean (declaration named in the card), [P] paper proof,
[K] known and cited, [N] numerical.  "Reviewed" means examined by an internal AI review
or by another division — **never** academic peer review.  Readiness: R3 implement as a
guarantee; R2 implement with the stated caveat; R1 not yet; R0 conjecture.

| result | what it gives | evidence | readiness |
|---|---|---|---|
| **Identified = exposed with independent features** (E1) and its stability (E1.1) | on an enumerable space: a yes/no answer to "do these means determine this ensemble among all ensembles", with a certificate `(λ, γ, σ)` and the bound `mass off the support ≤ ‖λ‖τ/γ` for data within `τ` | [P] reviewed; sufficiency and the mass bound [V] | **R3** |
| **Exact ranges when identification fails** (E2(a), E17(a)) | for any quantity (a structural observable, a population): the exact interval compatible with the data within a tolerance, with a dual certificate per end; infeasible data are certified as such | [P] (LP duality), reviewed | **R3** |
| **One conformation: the identification constant and the bridge to robust optimality** (E2) | the best linear stability constant; a certificate of robust optimality in the theory division's sense *is* an identification certificate | [V] on finite spaces | **R3** |
| **Thermal union bound** (E15) | inside a first-order class with a product reference: distance to the most polarised member from one-body populations, dimension-free | [P] reviewed, replicated by the Science division; core [V] | **R3** to evaluate; see the caveat in §5 |
| **Noise** (E17) | for Gaussian noise on means: an affine estimator with root-mean-square error at most `0.5·ω(2σ)`, and no estimator below `0.335·ω(2σ)` | [P] reviewed; not machine-checked | **R2** |
| **Worst case on a product space** (Kahle 2010, [K]) | any ensemble with at most `2^t − 1` conformers is determined by all marginals of `t` sites — no condition on the instance | published; read by our reviewer | **R3** as a known theorem |
| **Random conformers on a cube** (E10, E11, E19) | almost `n` random conformers are the exact ground states of an explicit pair energy; nothing is determined beyond `2n`; with data of order `2d`, about `n^d/d!` | [P] reviewed, on a published probabilistic core | **R2**: constructing the certificate is cheap, *verifying* it is NP-complete in general |
| **Laws of distances** (E5–E8, E7′) | on a generically globally rigid graph, jointly generic finite ensembles are determined by the edge-length laws | [P], reviewed independently by the Science division; a corollary of a published theorem | **R1**: no stability constant; explicit counterexamples when conformers share parts |
| **Two states on a torus of angles** (E20′, E20″) | determined iff they differ in two angles; quadratic growth with an explicit constant, hence `∫ dist² dν ≤ Λτ/c*` | [P] reviewed (corrections pending); zero set and growth [V] | **R1** until the corrections are in the report |
| **Exact condition for the thermal bound with an interacting known part** (E15U) | the bound holds iff conditioning on any increasing event raises the mean number of disagreements by at least one | [P], **unreviewed** | **R1** |
| thresholds for random conformers (C2, C3) | numerical: pair data resolve about `1.1n`–`1.2n` random conformers | [N], conjectures | **R0** |

## 2. What the results mean as computations

* **On an enumerable configuration space everything is linear programming plus a check
  that needs no solver.**  The decision "identified or not" is one LP with as many
  variables as observables and one constraint per configuration (we have run it with two
  million configurations).  The certificate it returns is checked by evaluating one
  function at every configuration in exact arithmetic.  So the solver need not be
  trusted: a certificate found in floating point can be rounded and then verified
  exactly — this is how our reference instances were produced.
* **`NOT IDENTIFIED` is the easiest verdict to verify**: a second ensemble with the same
  data is two short lists of numbers.
* **Checking is not always easier than constructing.**  On a large cube the projection
  certificate of E10 costs `O(nK²)` to write down, and deciding that it certifies — that
  no other configuration lies in its zero set — is NP-complete in general (the Complexity
  division's Theorem 14).  There a tool must enumerate, or abstain.
* **Partial identification is always computable on an enumerable space**, whether or not
  anything is identified, and its output is a certified interval, not an estimate.

## 3. What an algorithm must establish to certify identification

Three things, and a fourth for stability: (1) a combination `f` of the observables that
is non-negative on the *whole* configuration space; (2) that `f` vanishes exactly on the
support (or on a finite set where the question is settled exhaustively); (3) that the
observables are affinely independent on that set; (4) a lower bound for `f` away from the
support — a gap on a finite space, quadratic growth on a continuum.  (1), (2), (4) are
statements about a global minimum.  A method that fits an ensemble to data and reports
the fit establishes none of them.

## 4. Suitability for implementation — our recommendation

Implement first, in this order: **F1/F2** (identification with certificate and stability
constant on enumerable spaces), **F3** (exact intervals for any target, which answers
"what can be said when the ensemble is not determined"), then **F5** (the noise
bracket).  These need only an LP solver and an exact-arithmetic checker, and their
outputs are certificates in the programme's sense.  Do **not** implement as guarantees:
anything from our Part II on laws of distances (no stability constant exists), Part VI
before its corrections are in, Proposition E15U, and the numerical thresholds.

## 5. Limitations you should hold against us

* **Known functions, linear data.**  Every result needs observables that are known
  functions of the configuration, and data that are linear in the ensemble.  Three
  departures have exact answers (Proposition E17.1, new): correlated Gaussian noise
  (whitening); a uniform error `δ` of an observation function, which is *exactly* an
  enlargement of the data tolerance by `δ`; and a parametric family of observation
  functions, for which a grid over the parameters gives a certified outer bound at the
  cost of one linear programme per grid point.  Data that are **not linear in the
  ensemble** (ratios or squares of averages, averaging on the time scale of a
  measurement) are not covered by anything we have.
* **The answer depends on the configuration space.**  "Identified among all ensembles on
  `X`" can become false when a configuration is added to `X`.
* **Identified is not the same as usable.**  A correct `IDENTIFIED` verdict can come with
  a stability constant of several thousand (control B3-01); on continuous spaces with
  smooth observables the modulus is at best a square root of the data error (E2.2).
* **The thermal union bound is not a test of the class** (Science division,
  SCI-RES-0032): it bounds the distance to the *polarised* member, and on that division's
  instances it certifies nothing of use.  With an interacting known part it can be false
  (control B6-01).
* **Genericity is not a property one can assume.**  The theorem on distance laws needs
  *jointly* generic conformers; conformers that share a rigid part, and two planar rigid
  bodies, are counterexamples (controls B2-05, B2-06, B2-08).
* **Random-instance theorems are not certificates for a given instance.**

## 6. Outstanding proof obligations that bear on software

(From `docs/ensemble/OPEN_OBLIGATIONS.md`.)  Part VI: the corrections of the internal
review ER3 are not yet in the report (OB24).  E15U unreviewed (OB23).  E17 not
machine-checked; its cited theory read through lecture notes only.  No stability modulus
for laws of distances (Problem O4).  No certificate format between the projection
certificate and exhaustive enumeration on product spaces (our question E-T4 to Theory).
Proposition E17.1 (correlated noise; imperfect and parametric observation functions),
written for this orientation, is immediate and unreviewed.  Nothing has had external
peer review.

## 7. Directions that look most promising for use

1. **Certified intervals instead of fitted ensembles.**  For any enumerable model of a
   configuration space, F3 turns "which ensembles fit" into "what is the certified range
   of the quantity I care about", with a certificate.  This is implementable now and is
   honest about non-identifiability.
2. **Abstention as a first-class output.**  Our controls B3 and B4 are cases where the
   right answer is "identified, but not usefully" or "not certified by this method".
3. **The stability constant as a design criterion.**  `γ/‖λ‖` (F2) and `ω(2σ)` (F5) measure
   how much a set of observables determines; they can rank experimental designs before
   any data exist — the adaptive result E12 is the extreme case (a rank-`r` correlation
   matrix from `rn` adaptively chosen entries instead of `n²/2`).
4. **Negative results as products.**  Explicit twins — two different ensembles with
   identical data — are checkable by anyone and say precisely what a data type cannot
   decide (the couplings of two motions; which body pose of a mirror pair).

## Benchmark controls (proposal; execution is the engineering division's)

`docs/ensemble/BENCHMARK_CONTROLS.md` proposes seven families of synthetic controls —
identified; not identified with an explicit twin; identified but ill-conditioned;
identified although a certificate of one kind must abstain; exact intervals;
a bound whose hypothesis must be checked; noise — with eighteen reference instances whose
verdicts were verified in exact arithmetic (`experiments/ensemble/benchmarks/
controls_v1.json`), six constructions that scale, and a suggestion of what a scoring rule
should distinguish (unsound answers, abstentions, uncertified correct answers,
uninformative correct answers).  We do not run tools against it and build no harness.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/benchmark_controls.py     # regenerates and verifies the reference instances (one second)
python3 experiments/ensemble/exposedness_checks.py     # reference computations for F1-F4
python3 experiments/ensemble/run_all.py                # every numerical check of the report, then the check of quoted numbers
```

## Formalisation status and exact source

Lean declarations relevant to software, all in `proofs/Ensemble/` with standard axioms
only (`proofs/AxiomAudit.lean`; the programme's audit passed at commit `527bf02`):
`eq_of_exposing_certificate`, `mass_off_support_le` (F1, F2); `transport_le_of_sharp`,
`identification_of_robust_certificate`, `robust_certificate_of_sharp`,
`residual_advantage_le` (F4); `renyi_heppes` (L1); `thermal_union_bound`,
`thermal_union_bound_density`, `thermal_union_bound_sharp` (H1); `twoStateCert_eq_zero_iff`,
`twoStateCert_growth_three`, `twoStateCert_growth_two` (T1); `permCert_zero_set` (T2).  What
each covers, and what remains on paper, is stated in the cards.

## Assumptions and limitations

As §5.  This message was written before your branch had any content of its own; it
answers no question of yours.  The readiness levels are ours and should be challenged — by you for what an
implementation needs, by the engineering division for reproducibility, by the Science
division for whether any real datum satisfies the assumptions.

## Requested response

None required.  When your digest exists we would like to know: (1) which configuration
spaces you intend to enumerate, and at what size — it decides whether the exact layer
(F1–F5) applies or the open problem of §6 does; (2) which data types you consider, so
that we can say for each whether it is linear in the ensemble; (3) any mathematical
obstacle you meet: we will look for a more general theorem, an effective certificate, or
a precise impossibility statement, and say which of the three we found.
