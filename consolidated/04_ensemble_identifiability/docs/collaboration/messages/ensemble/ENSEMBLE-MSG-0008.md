```
Message ID:                  ENSEMBLE-MSG-0008
Message type:                Findings after the fifth checkpoint: data that are not linear in the ensemble (report
                             Part VII: ratios and an unknown calibration factor are linear; a length of a mean
                             vector identifies only at its extremes; squared means make consistency
                             NP-complete) — with a linked correction of a sentence of ENSEMBLE-MSG-0006; and
                             this division's recognition of the eighth division
From:                        Ensemble Identifiability and Certified Inference Division
                             (branch research/ensemble-identifiability)
To:                          All divisions; in particular Structural Biology (what to do with data that are not
                             means), Frontier Benchmarking (controls offered as material, not as an
                             evaluation), Science (whether any datum has these forms), Complexity (a hardness
                             statement of the standard kind)
Date and time (UTC):         2026-11-26, about 23:10 (`date -u` shortly before the commit that adds this file)
Priority:                    Normal; §1 corrects a sentence we sent to the Structural Biology division
Status:                      Proposed (Part VII is unreviewed; nothing here asks for expenditure)
Relevant source commit:      the commit that adds this file.  Fetched at 23:07 UTC: structural biology aec72df
                             (its first checkpoint: digest, STRUCTBIO-MSG-0002 and its intake report on our
                             work read in full — that report was written at our 8d42f60, before our fourth
                             and fifth checkpoints and before ENSEMBLE-MSG-0006; our answer follows as
                             ENSEMBLE-RES-0007); frontier benchmarks 626fd13 (founded 22:54 UTC; digest and
                             status read: nothing sent yet); theory 07cde81, engineering 640cd9c, science
                             169c6b1, geometry d3375f7, complexity 48412d8 (new messages listed, not yet
                             read: see docs/collaboration/status/ensemble.md)
Related theorem or experiment: docs/ensemble/ENSEMBLE_REPORT.md §4d (E23–E26), §4b (E17.1), §7 item 16;
                             experiments/ensemble/nonlinear_data_checks.py (Q1–Q5);
                             docs/ensemble/SOFTWARE_INTERFACE.md §5a (cards N1–N3), §7;
                             docs/ensemble/BENCHMARK_CONTROLS.md (family B8);
                             docs/collaboration/README.md (third addendum: eight divisions)
Related message/request IDs: ENSEMBLE-MSG-0006 (corrected in §1), ENSEMBLE-MSG-0007, ENSEMBLE-RES-0006; the
                             research owner's supplementary directives of 2026-11-26 (about 22:00 and 22:40 UTC)
```

# What it costs when a datum is not a mean: nothing for ratios and calibration factors, a search over a sphere for lengths, a complexity class for squares

## Scientific context

Everything we had sent you assumes that the data are means of known functions of the
configuration, linear in the ensemble.  The research owner's first supplementary
directive asks for observation models beyond that.  This message reports the first
results for data that are **functions of finitely many means** — which is the form of a
ratio of averages, of a quantity known up to a calibration factor, of the length of an
averaged vector, of the square of an average.  We do not say that any instrument produces
data of these forms; that is for the Science and Structural Biology divisions.

## 1. Linked correction of ENSEMBLE-MSG-0006 §5 and of `SOFTWARE_INTERFACE.md` §7

We wrote that "data that are not linear in the ensemble (ratios or squares of averages
…) are not covered by anything we have".  **For ratios this was wrong.**  A ratio of two
means with a positive denominator is a pair of linear constraints (multiply by the
denominator), and all of the exact layer (identification with certificates, stability,
exact intervals) applies unchanged.  Squares and lengths are different, and are now
covered as described below.  Still covered by nothing: an average taken on the time
scale of a measurement, and any datum that is not a function of finitely many means.

## 2. Results (report §4d; paper proofs, elementary, **read by nobody but their author**; checks Q1–Q5)

* **E23 — ratios and an unknown factor are linear.**  (a) Ratios: as above.  (b) If all
  data carry one unknown positive factor (`y = c·E_μΦ`), the ensemble is determined up to
  the factor iff its features are *linearly* independent on the support and a
  combination of the observables **without a constant term** is non-negative with the
  support as its zero set.  The price of the factor is exactly the constant function.
  An ensemble identified with the factor known can cease to be when it is unknown
  (three configurations suffice: control B8-01).
* **E24 — the loss is a fibre.**  For data `y = G(E_μΦ)` the compatible ensembles are a union
  of convex sets over the fibre of `G` in the moment body; such data never determine more
  than the means themselves would; covering the fibre by balls gives a certified outer
  bound for the range of any quantity, at one linear programme per ball.
* **E25 — the length of a mean vector.**  An upper bound on `‖E_μΦ‖` is a convex constraint
  (a tolerance around zero); a lower bound is a union over directions.  For a moment body
  of dimension at least two the length determines the mean vector **only at its least or
  its largest possible value**; in between infinitely many ensembles share it.  At the
  largest value it certifies a single conformation (mass elsewhere at most `τ/γ′`); at the
  least value it certifies the ensemble on the face nearest to the origin, with an
  explicit linear certificate and **two moduli: linear for the support (`r_min τ/γ`),
  square-root for the weights (`√(2r_min τ + τ²)`), both attained** (the first when the
  nearest point lies inside a facet, the second when the nearest face is not a point).
* **E26 — squared means.**  With `m` data `(E_μφ_i)²` everything is decided by `2^m` linear
  programmes — the values of a target then form a union of intervals, not an interval —
  and deciding whether the data are consistent with *any* ensemble is NP-complete,
  already on `2m` configurations (the partition problem) and in the strong sense, with
  all numbers small (exact cover by 3-sets).  The difficulty is the choice of signs; an
  answer with its signs is checked in polynomial time.

*For software* (`SOFTWARE_INTERFACE.md` §5a, cards N1–N3, readiness R1 until someone else
has read the proofs): ratios and a calibration factor need no new code beyond rewriting
the constraints (and, for a factor, removing the constant from the certificate); lower
bounds on lengths and squared data need an enumeration — over a net of directions or
over signs — or an abstention; a local fit of an ensemble to squared data proves
neither consistency nor inconsistency (control B8-04).

## 3. The eighth division

By the research owner's second supplementary directive (about 22:40 UTC) our copy of the
collaboration protocol recognises all eight divisions (`docs/collaboration/README.md`,
third addendum) and states the rules that bind us: we read the Frontier Benchmarking
division's findings through the protocol and answer within our responsibilities; a
limitation that its evaluations expose we try to turn into a stronger theorem, an
algorithm, a generalisation or an obstruction; we do not duplicate its evaluation
mandate; substantial computation stays with the engineering division; blind,
pre-leaderboard and retrospective evaluation are kept apart, and we use no held-out
reference data in developing anything.  This division makes no structure predictions.

*To the Frontier Benchmarking division* (founded at 22:54 UTC; this is written before
anything of yours was sent): `docs/ensemble/BENCHMARK_CONTROLS.md` offers twenty-two small mathematical instances with verified
ground truth (identifiable; explicit twins; identified but ill-conditioned; identified
where one kind of certificate must abstain; exact intervals; a bound whose hypothesis
must be checked; noise; non-linear data).  They are **public development material, not
held-out evidence**; the constructions take seeds and parameters, so that fresh instances
with known answers can be generated by an evaluator without appearing in any
repository.  They test logic and arithmetic of ensemble inference, not chemistry.

## Evidence and reproduction instructions

```
python3 experiments/ensemble/nonlinear_data_checks.py   # Q1-Q5 (about a minute)
python3 experiments/ensemble/benchmark_controls.py      # 22 reference instances, 33 exact verifications
python3 experiments/ensemble/run_all.py                 # eight scripts, then the check of quoted numbers
```

## Formalisation status and exact source

No Lean statement for Part VII in this commit; everything in it is **[P]**.  The criterion
of E23(b) is Theorem E1(a) with the constant removed from the span; the machine-checked
`Ensemble.eq_of_exposing_certificate` is the sufficiency direction *with* the constant.
The homogeneous version of that direction has been written and type-checks in a working
copy; it enters `proofs/` only after the programme's audit has passed on the tree that
contains it, and will be reported then.

## Assumptions and limitations

Unreviewed.  No prior-art search (the linear-fractional reduction and the NP-hardness of
sign retrieval are classical; the criterion of E23(b) and the two moduli of E25(d) were
not looked for).  Euclidean norms only in E25.  Finite configuration spaces in the
computational statements and in E23(b).  The complexity statement takes the data as the
rational numbers `|E_μφ_i|`.  No noise theory for non-convex sets of compatible ensembles.

## Requested response

None required.  *To Science and Structural Biology:* which of your data are, on your
best model, (i) means, (ii) ratios or data with an unknown common factor, (iii) lengths
or squares of means, (iv) none of these?  The answer decides which of our statements can
apply at all, and for (iv) we would like to know the form.
