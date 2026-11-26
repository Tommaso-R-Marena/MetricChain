# Benchmark controls — synthetic instances with ground truth for ensemble-inference software

*Proposed by the Ensemble division to the Structural & Computational Biology, Software
Development and Applications Division (which implements), to the engineering division
(which reproduces and benchmarks) and to the science division (which judges relevance).
This is a specification with reference instances.  **It is not a benchmark harness**:
running tools against it, timing and scoring them is the engineering division's work, and
we do not build a system of our own for that.*

Every instance is a mathematical object — a configuration space, a set of observables, an
ensemble, the data it produces — with a verdict that is a theorem or an exact
computation.  None is a model of a molecule or of an instrument.

## 1. What the controls are for

A tool that infers an ensemble from averaged data can fail in five ways that ordinary
accuracy tests do not see.  Each family below is built to catch one.

| family | the failure it catches | a sound tool must |
|---|---|---|
| **B1** identified | reporting ambiguity where there is none | answer `IDENTIFIED` and give a certificate that a separate program can check |
| **B2** not identified | reporting one ensemble where several explain the data equally | answer `NOT IDENTIFIED` and exhibit a second ensemble, or give an interval; **never** return a single ensemble as "the" answer |
| **B3** identified but ill-conditioned | reporting a correct verdict without its stability constant | answer `IDENTIFIED` *and* report that an error of the stated size leaves the answer open |
| **B4** must abstain | mistaking "my certificate fails" for "not identified" (or the reverse) | answer `ABSTAIN` or "not certified by this method"; a different method then certifies |
| **B5** partial identification | having nothing to say when identification fails | return the exact range of the quantity asked for, with a dual certificate for each end |
| **B6** a hypothesis that must be checked | applying a bound outside its hypothesis | check the hypothesis or abstain |
| **B7** noise | reporting a point estimate without a risk bound | report the bracket for the minimax risk |

## 2. The reference instances

File: `experiments/ensemble/benchmarks/controls_v1.json`, written by
`experiments/ensemble/benchmark_controls.py`, which verifies every claim before writing it
(27 verifications: twins by equality of the data in exact rational arithmetic;
certificates by evaluating `c + λ·Φ` at every configuration in exact arithmetic after the
linear programme's output has been rounded inside the exact solution space of the
equalities; intervals against closed forms).  Numbers in quotes are exact rationals.

| id | instance | verdict | why (report section) |
|---|---|---|---|
| B1-01 | three conformers on `{±1}⁴`, six pair correlations | `IDENTIFIED`; certificate with gap 2 and `‖λ‖₁ = 6` | any three conformers are determined by pair correlations (E9(a)) |
| B1-02 | five conformers on `{±1}⁶` that form a face, fifteen pair correlations | `IDENTIFIED`; exact certificate | E1(a) |
| B2-01 | the square `{±1}²`, the two one-body means; ensemble `½(++) + ½(−−)` | `NOT IDENTIFIED`; twin `½(+−) + ½(−+)` | sharpness of the Rényi–Heppes count (E4) |
| B2-02 | three configurations, one observable `(0, 0, 1)`; ensemble on `{a, b}` | `NOT IDENTIFIED`, although the support is exposed | E1(a): exposedness without independence proves nothing |
| B2-03 | four conformers on `{±1}⁵` (a Hadamard quadruple on four sites), ten pair correlations | `NOT IDENTIFIED`; twin: the quadruple of the other parity | E9(b); the cut polytope is not 4-neighbourly |
| B2-04 | two triangles with sides `(3,4,5)`, `(4,5,6)`; laws of the three sides | `NOT IDENTIFIED`; twin `(3,5,6)`, `(4,4,5)` | a free rigidity matroid: lengths can be spliced (E5(b)) |
| B2-05 | `K₄` in the plane, two conformers with no length in common, six edge-length laws | `NOT IDENTIFIED`; twin by reflecting one point in each | E7 needs *jointly* generic conformers (the science division's Example D1) |
| B2-06 | five points, all distances but one; two conformers sharing a triangle | `NOT IDENTIFIED`; twin by exchanging the positions of one mobile point | a shared rigid part (Example D2; Problem O3) |
| B2-07 | three states on a torus of two angles; nine bilinear trigonometric means | `NOT IDENTIFIED`; explicit twin | no three states on this torus are determined (Proposition E22) |
| B2-08 | two rigid bodies in the plane, collinear attachment points, six leg lengths, **one** pose | `NOT IDENTIFIED`; the mirror pose | E7′ excludes planar bodies: a mirror pose for any number of legs |
| B3-01 | one vertex of a regular 360-gon, means of `(cos, sin)` | `IDENTIFIED`; but with each mean known within `10⁻⁴`, 66 % of the mass can be elsewhere, and within `2·10⁻⁴` all of it | E1.1: constant `1/γ = 6 566`; on a continuum the modulus is a square root (E1.2, E2.2) |
| B4-01 | four conformers on `{±1}⁸` whose span contains a fifth sign vector, 28 pair correlations | `IDENTIFIED` (exact LP certificate); the projection certificate must abstain | E10 and the Complexity division's Proposition 13 |
| B5-01 | `{±1}³`, three one-body means `(1/5, 1/2, −3/10)`; target `E[x₁x₂]` | `INTERVAL [−3/10, 7/10]` with the two dual inequalities | Fréchet bounds as dual certificates (E2(a)) |
| B5-02 | the same data; target: the population of `+++` | `INTERVAL [0, 7/20]` | a certified restriction on a population |
| B5-03 | the same, each mean known within `1/20` | `INTERVAL [−2/5, 4/5]` | each end moves by `τ‖λ‖₁` |
| B6-01 | two sites, known part `∝ exp(−½x₁x₂)`; the thermal union bound | the bound is **false** here by `0.1696` | a violated bond can break it (E15T(d)); the hypothesis is E15U |
| B6-02 | three sites, uniform reference; one-body populations of a polarised member | `BOUND 2σ − 1`, attained | E15(c), equality case |
| B7-01 | two configurations, one mean with Gaussian noise `σ = ½` | minimax root-mean-square error between `0.335` and `0.5` | E17 |

## 3. Families at scale (generators with ground truth)

The reference instances are small on purpose.  The same constructions give families of
any size whose ground truth is known *by theorem*, or by an exact computation that the
engineering division can reproduce with our scripts.

1. **Random conformers on `{±1}ⁿ`, pair correlations.**  Ground truth for `n ≤ 22` by exact
   linear programming (`experiments/ensemble/capacity_cutting_plane.py`); reference
   frequencies in `experiments/ensemble/output_threshold.txt`.  A tool's verdicts can be
   compared instance by instance, and its frequency of `IDENTIFIED` with the stored
   frequencies (for example `n = 16`: `0.94, 0.66, 0.26, 0.07` at `K = 16, 18, 19, 21`).
   Beyond `2n` conformers nothing is identified with high probability (E11(a)): a tool
   that reports a unique ensemble there is wrong.
2. **Planted twins.**  For any support that is not a face, the linear programme of
   `SOFTWARE_INTERFACE.md` F1 returns a second ensemble with identical data; B2-03 is the
   smallest.  Feeding a tool the data of one member of a twin pair and asking for "the"
   ensemble tests whether it reports the ambiguity.
3. **A ladder of conditioning.**  The vertex of a regular `N`-gon (B3-01): identified for
   every `N`, with stability constant `1/(1 − cos(2π/N)) ≈ N²/(2π²)`.  A tool's reported
   uncertainty at fixed data error should grow along the ladder; one that reports the
   same confidence at `N = 12` and `N = 3600` is not tracking conditioning.
4. **Splices for laws of distances.**  Any two conformers sharing a rigid part, with two
   further points placed independently (B2-06), give a twin by exchange; any two-body
   platform with at most three legs in the plane or six in space has twins on an open set
   of pose pairs (E7′(c)); collinear or coplanar attachment points give a mirror twin for
   any number of legs (B2-08).  All can be generated with rational coordinates.
5. **Identified without the easy certificate.**  Random supports of `K ≥ n/2` conformers
   on small cubes are faces with high probability and have no projection certificate
   with high probability (`experiments/ensemble/degree2_vs_face.py`: `n = 12`, `K = 9`: 92 %
   and 0.5 %).  A tool must distinguish "not certified" from "not identified".
6. **Exact intervals.**  One-body data on a cube with any pair or population as target:
   closed-form Fréchet bounds (B5).  With pair data and a three-body target the interval
   is a linear programme whose dual certificate can be checked exactly.

## 4. What a scoring rule should distinguish

We suggest — the decision is the engineering division's — that a harness count
separately:

* **unsound answers**: `IDENTIFIED` where a twin exists; a single ensemble returned for a
  B2 instance without a statement of ambiguity; an interval that excludes a feasible
  value; a bound applied outside its hypothesis (B6-01).  These are errors;
* **abstentions**: never errors; their frequency measures the tool's reach;
* **uncertified correct answers**: `IDENTIFIED` without a certificate that the harness can
  check.  Correct by luck is not distinguishable from correct;
* **uninformative correct answers**: B3-type verdicts without the stability constant.

## 5. Limits of these controls

* They test logic and arithmetic, not chemistry: no instance says how a measurement is
  related to a mean of a function of the configuration.
* The verdicts are for the stated configuration space.  Embedding an instance in a larger
  space can change `IDENTIFIED` into `NOT IDENTIFIED`.
* Families 1 and 5 have statistical ground truth beyond the sizes that can be enumerated
  (the thresholds are conjectural: C2, C3); only instance-wise verdicts from exact
  computation are ground truth.
* B2-07 rests on Proposition E22, which comes from our internal review of Part VI and has
  been read by nobody else; the twin itself is verified by the generator.
* On tori and other continuous spaces a search restricted to a product grid can report
  `IDENTIFIED` falsely, because the twin does not lie on the grid (B2-07); one of our own
  early checks had this defect.
