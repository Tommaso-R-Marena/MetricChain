# Research log — Geometric Inference, Rigidity and Inverse Problems Division

Branch `research/geometric-inference`, created 2026-11-26 from the theory checkpoint
`a844b5a` (`claude/determined-ride-og1u7j`).  Newest entry first after "Resume here".

## Resume here

State at the thirteenth checkpoint (see `HANDOFF.md` for commands and environment):

1. **Cycle 1 result:** `docs/geometry/ENSEMBLE_RIGIDITY.md` — second-moment rigidity of
   conformational ensembles (stacking; conic criterion; identifiability of mixtures among all
   ensembles; thresholds; DEMIX; stress certificates; global `W₂` theorem; second-moment
   rigidity; realizable set versus its semidefinite relaxation; range `K + 3`).
   Register: `THEOREM_REGISTER.md`.  Internally reviewed up to `e8e2582`
   (GEOMETRY-REV-0001) and by the Science division (SCI-REV-0021).  **New at the ninth
   checkpoint, unreviewed: §6.2** — certificates below the conic threshold (Proposition 6.2;
   Theorem I′: identifiable among all ensembles from 10, 16, 30 atoms for two, three, four
   states, exact witnesses; Conjecture 6.3).  The method is Johnston–Lovitz–Vijayaraghavan's
   (`PRIOR_ART.md` §3b).
2. **Cycle 2:** `LOCAL_DATA_STABILITY.md` — Theorem K (lower bounds); **Theorem L, since the
   tenth checkpoint without a threshold** (every configuration `Y`; Lemma P on complete
   five-point windows; frames compared on shared tetrahedra; local constants; any
   separation `K ≥ 4`); Theorem L⁺ (first-order constant `1/(2μ)` in the range
   `‖η‖ ≤ μ/(ΛC_L)`); Proposition L₀ (the earlier form).  Originality reviewed by Science
   (SCI-REV-0023): mechanism and scaling known.  **§3 reviewed with replication by Science
   (SCI-REV-0028, thirteenth checkpoint): proved as stated; twelve findings applied.**  Its
   major finding, replicated by us (`distant_fits.py`): the first-order constant is not a
   global one — configurations at the radius of gyration fit the local distances of a
   20-point helix-like trace to `0.27` Å.  Certified range `10⁻⁵` ångström or less.  Open:
   O-16 restated (the size of the best global constant, between `1.92` and `456` there).
3a. **Fourth note:** `LABEL_PATTERNS.md` (twelfth checkpoint, unreviewed) — only a subset of
   the points observed.  Governing number: `c(S)`, the observed pairs at chain separation
   1 or 2.  Proved: transfer; the linear threshold `(9K²+K+2)/2` for non-adjacent labelled
   bonds and for patterns with an anchor; the obstruction below `9K/2` (given regularity).
   Exact: 100 random patterns, the quartic certificate on patterns of two states (from 17).
   Open: O-17 (Conjecture P; regularity as a theorem; three states; the middle range).
3b. **Fifth note:** `ROBUST_DEMIXING.md` (thirteenth checkpoint, unreviewed) — noisy data
   and inexact bond geometry.  Lemma N0 (a rank-3 solution of the conic system up to `ρ`
   is near a projector: interlacing); Theorem N1 (every ensemble: enclosure; computable
   `κ` for Theorem G — O-5 closed as "computable"); N2 (`K`-state competitors: crude linear
   bound); N3 (first-order constants `C_state`, `C_w` certified by bootstrapping, attained);
   N4/N5 (a-posteriori procedure; count of states with the threshold at the error level);
   N6 (tolerance: uniqueness lost, first-order constant `c_tol`).  `C_state` is `0.7`–`4.5`;
   certified ranges end at relative errors `10⁻¹²`–`10⁻⁴`.  Open: O-18.
3. **Third note:** `HINGE_ENSEMBLES.md` (states that share rigid segments; the main
   statement is the Science division's Proposition R22-1).  Open: O-12, O-13, O-14,
   R22-GEO-3, -4, -5.
4. **Two supplementary directives of the research owner** (condensed in
   `docs/collaboration/status/geometry.md`): a seventh division (Structural Biology,
   `research/structural-biology`: software) and an eighth (Frontier Benchmarks,
   `research/frontier-benchmarks`: evaluations; not on the remote at 22:42 UTC).  Done at the
   eleventh checkpoint: `IMPLEMENTATION_GUIDE.md`, `BENCHMARKS.md` + `benchmark_suite/` (21
   instances), GEOMETRY-MSG-0009 (orientation), the protocol copy with eight divisions.
   **Standing duties from them:** distinguish global identifiability, local identifiability,
   algorithmic recoverability and efficient certification; pursue constructive forms,
   relaxations or obstructions, computable stability constants; state the gap between
   idealised observables and measurements; do not design or run evaluations (that is
   Frontier Benchmarks and Engineering); answer their questions; if an evaluation exposes a
   mathematical limitation, look for a stronger theorem, an algorithm, a generalisation or
   an obstruction.  Read `docs/collaboration/STRUCTURAL_BIOLOGY_TO_ALL.md` and
   `FRONTIER_BENCHMARKS_TO_ALL.md` on those branches at every synchronisation.
5. **Open, in priority order** (`PROOF_OBLIGATIONS.md`): O-15 (Conjecture 6.3: four states
   at 24 to 29 atoms — `exact_demix4.py 4 28` is feasible locally in about three hours;
   three states at 15 atoms needs degree 5 and the structural locus; stability of the rank
   certificate under noise), O-1, O-3, O-2 (b)–(d), O-4, O-5.
6. **Next synchronisation:** fetch all seven other branches and look for `GEOMETRY` in their
   `docs/collaboration/` and in `docs/frontier_benchmarks/MATHEMATICAL_FEEDBACK.md`.  Not yet
   read: ENSEMBLE-MSG-0005, -0006, -0008, ENSEMBLE-RES-0004, THY-MSG-0019, -0020, SCI-MSG-0034,
   -0035, SCI-REV-0025, -0026 and Science's software evaluation protocol, COMPLEXITY-MSG-0005,
   -0006, COMPLEXITY-RES-0010, the Structural Biology division's code, Engineering's final
   ENG-MSG-0007 beyond its §5.  **Received and answered at the thirteenth checkpoint:**
   Science's review of Theorem L (SCI-REV-0028 → GEOMETRY-RES-0010), the Frontier
   division's G-1 … G-4 (→ GEOMETRY-RES-0009; the block-sum half of G-3 not done),
   Engineering's replication of Theorem I (ENG-MSG-0007 §5).  Awaited: Engineering on
   GEOMETRY-REQ-0006 (accepted).  Also unread: SCI-REV-0027, SCI-RES-0037 … -0041,
   ENSEMBLE-RES-0007, THY-MSG-0021 beyond §6, the Frontier division's protocols.
7. **Mathematics to do next** (ranked for utility in GEOMETRY-MSG-0009 §7 and by the
   Frontier division's items; the noise and tolerance theorem is done — fifth note):
   (0) identifiability from **block sums** under a stated labelling scheme (the first half
   of the Frontier division's G-3; a local-identifiability rank computation first);
   (0′) O-18 (i): a better way into the basin than Theorem N2; O-16 (i): the best global
   constant for local distances; (0″) the Ensemble division's method (first-order
   conditions along the zero set of the certificate) for our cases below the thresholds;
   (i) when does
   a stress certificate exist for a given set of measured pairs or block sums — a producer
   and a threshold (Theorems F, F″); (ii) a computable `κ` (O-5); (iii) a tolerance version
   of the statewise constraints; (iv) O-16; (v) an independent referee for §6.2 and for §3
   of the second note (one referee session for both).

## 2026-11-27, thirteenth checkpoint (work from 00:00 UTC; see the commit time)

**Robust demixing (fifth note).**  Prompted by the Frontier division's four items (all
fair) and our own O-5.  The idea that made the constants computable: a chain that is
nearly an affine image of the stack gives a positive semidefinite matrix of rank at most
3 that nearly solves the conic system; decompose it along the reference projectors; by
Weyl's inequalities at most one coefficient can be large, because the matrix has only
three non-zero eigenvalues (Lemma N0).  No compactness argument is left, so the constant
of Theorem G has an explicit lower bound.  Numerics first (`robust_demix.py`): every
inequality on chains near the states, random chains, far chains that are nearly affine
images (found by minimising `φ` from random starts), split states, spurious states; no
violation; the bounds are loose by factors of 150 and more.  Then the first-order
constants: block norms of the pseudo-inverse of the linearised map on weights and
tangent displacements — between `0.7` and `4.5`, i.e. the problem is well conditioned to
first order even at the thresholds, where the reported certificate value `σ_c` is small;
`σ_c` governs the certified range, not the accuracy.  Theorem N3: exact expansion of
`G(μ′) − G(μ₀)` (a cubic polynomial), constraints give the non-tangent part at second
order, bootstrap from the crude bound; checked step by step; the extremal direction
attains the constant (ratio 1.0000).  A posteriori: polish the DEMIX output to an exact
mixture so that the reference violates nothing.  Tolerance: with exact data the
competitors are the rotated stacks; first-order constant `c_tol` by a generalised singular
value; the certified constant uses the linearised violation-to-displacement map (4 to 6
times `c_tol`; a first version, through triangle inequalities, was 40 times).  Count of
states: threshold at the error level; our DG-7 was a fixed-threshold failure.
A first draft attributed that failure to an observation of the Frontier division; it
quotes our own dead end (DG-27).  Prior art: two searches, one paper opened in part
(Cai–Li, joint block diagonalisation): tools standard, statements not found.
**Honest size:** certified ranges end at relative errors `10⁻¹²`–`10⁻⁴`.

**The stress route for Theorem L, computed and excluded** (DG-26, `stress_route.py`): global
and linear in Gram space, but the factor grows faster than `n⁴`.  **First-order
average-case numbers** added to the table of the second note.

**At the fetch of 00:47 UTC: SCI-REV-0028**, the Science division's review of Theorem L
with replication: every statement proved as stated; Lemma P verified at its source; and
a finding we did not have — distant configurations fit the local distances of our own
20-point trace to three tenths of an ångström, so `1/(2μ)` is not a global constant and
`1/τ` is necessary.  Its stored configuration is not on its branch; we wrote our own
search (`distant_fits.py`) and obtained the same numbers to the digit (9.95 Å at 0.300 Å;
9.0 at 0.271; strand-like 18.6 at 0.200).  All twelve findings applied, with their
replacement texts and attribution; two of them change a statement (the hypothesis of
Theorem L is needed for interior windows only; Corollary L.2 needs an estimate in three
dimensions) — we re-read the proof for the first and agree.  GEOMETRY-RES-0007 carries a
bracketed correction.  **ENG-MSG-0007 §5:** Engineering computed Theorem I independently
(degree 7; 63 of 70) — agreement.  ENSEMBLE-RES-0008 §3, THY-MSG-0021 §6: read; nothing
owed.

## 2026-11-26, twelfth checkpoint (work from 22:55 UTC; see the commit time)

**Partial labelling.**  Looking for the mathematics that would most help the new software
division (GEOMETRY-MSG-0009 §7), the first question was what survives when only some points
are observed.  Experiments first (`label_patterns.py`): for an anchor with sparse labels,
scattered triples, scattered bonds, every second point, mixed runs — the conic nullity is
`max(K − 1, D_K − c(S))` in every case, `c(S)` the number of labelled pairs at chain separation
1 or 2, and DEMIX recovers the labelled-site states exactly from `c(S) = (9K²+K+2)/2` on.
Exact ranks on random patterns and on arbitrary subsets of constrained pairs: no exception
for `K ≤ 3` — but a predicted one for a single state (two labelled triples: two planes form
a conic at infinity; rank 5).  Proofs: the transfer is immediate from Theorem B for a
constraint graph; non-adjacent labelled bonds reduce to the freely jointed case (their
directions are generic in a product of spheres); patterns with an anchor to Theorem C.
**Obstruction.**  Rotating the labelled stack keeps the data; the statewise constraints cut
the family by at most `(K − 1)c(S)` dimensions; so below `c(S) = 9K/2` no local identifiability
(count verified numerically: `max(0, 9 − c)` for two states, `max(0, 27 − 2c)` for three), and
with sparse labels nothing.  Second solutions built by fitting chains through the rotated
labelled sites — exact to rounding for labels at every fourth and sixth point; for every
third point the realisable neighbourhood is small (fits fail beyond a displacement of a few
hundredths), which is recorded as a limit of the regularity condition.
**Quartic certificate on patterns** (exact): two states are certified from 17 constrained
pairs; scattered patterns have no structural point, patterns covered by two hyperplanes
(two runs of 6) have one and the defect is exactly `dim L`.
One search paper opened (Hays–Boland–Kasson: distributions per pair, no theorem).

**At the fetch before the commit (23:36 UTC): the Complexity division's answer to C1**
(COMPLEXITY-RES-0009) with two questions.  (b) Is the affine hull of the realizable set of
fixed-angle chains cut out by the bond and bond-angle coordinates?  Yes — Lemma 8.0 (§8.1
of the report): in chain frames `⟨b_k, b_l⟩` is a trigonometric polynomial in exactly the
torsions between the two bonds, and its coefficient at the product of their first
harmonics is `−(sin²α/2)((1 + cos α)/2)^{p−1} ≠ 0`; a relation among such functions is
excluded by looking at a pair whose torsion set is maximal.  Numerical check first (full
rank at four bond angles, the coefficient to six digits), then the proof; test
`chain_affine_hull` with a planted error (separation 2 included: the rank drops).  (a) Is
its linkage lemma in print?  One search: the spherical-polygon framework is standard for
fixed-angle chains; the lemma in that form not found, no paper opened — given as a pointer,
not a citation (GEOMETRY-RES-0008).  Its §4 corrects an attribution of ours
(GEOMETRY-RES-0006 §6.4: a bracketed note added there) and changes how our open question on
computational gaps should be put — for noisy data.
**At the second fetch (23:50 UTC): the Frontier Benchmarking division's four items for us**
(`MATHEMATICAL_FEEDBACK.md` on its branch): no noise statement for demixing (G-1); Theorem
L/L⁺ empty as a guarantee (G-2); the data of the theorems are no instrument's product —
block sums, bond constraints within a tolerance (G-3); the symmetry group of each
"identifiable" (G-4).  All four are fair.  Not answered in this commit; G-1 and the
tolerance half of G-3 are our O-5 and are the next piece of mathematics; G-4 is a defect of
our documentation.  A first look at G-2 on paper (not in any file as a claim): the
universal-rigidity route — a positive semidefinite stress of maximal rank gives a *global*
bound in Gram space that is linear in the noise — pays a factor `1 + Λ‖ω‖/λ⁺(Ω)`, and for
a helix the smallest non-zero stress eigenvalue decays like `n⁻⁴` (the symbol of the
five-point affine dependency has a double zero at frequency 0), so it is not expected to
beat Theorem L; to be confirmed by a computation before it is recorded as a dead end.

## 2026-11-26, eleventh checkpoint (work from 22:36 UTC; see the commit time)

Two supplementary directives arrived during the tenth checkpoint (a seventh division for
software, an eighth for evaluations).  This checkpoint has no new theorem; it turns what
exists into things the new divisions can use and attack.
* `IMPLEMENTATION_GUIDE.md`: the four notions and the table of thresholds; the observable
  and its distance from measurements; specifications S1–S7 (stacking, linear certificate and
  DEMIX, quartic certificate, stress checker, hinges, local identifiability, local-distance
  diagnostics) with Lean names, complexity, conditioning, counterexamples, validation
  criteria; obstructions; what stays exploratory.
* `benchmark_instances.py` and `benchmark_suite/`: 21 labelled instances; every label that
  can be recomputed is recomputed (21 checks).  New second solutions constructed here: one
  differing torsion (same first circular moment), two half-turn hinges (from the linear
  programme over the eight candidates), the collinear decomposition, a reflected tail; the
  8-point one is the internal referee's.  A rule of the guide was checked on the way: rigid
  segments are the maximal runs whose principal sub-Gram matrix has rank 3 (recovers the
  segments of instance C3 exactly).
* The protocol copy and the status file list eight divisions and the three directives.
* Harness test `benchmark_suite_labels` with a planted error.

## 2026-11-26, tenth checkpoint (work from 22:13 UTC; see the commit time)

**Theorem L without a threshold.**  SCI-REV-0023 §5 computed the necessary size of any
threshold (`4h⁻h⁺`, from a reflection) and asked whether `(τ/D)²` is forced.  Working on
that question: the distances of separation at most 4 are all distances of every
five-point window; Lemma P (Procrustes–Gram, with a ten-line proof) controls such a window
for arbitrary `Y`; five-point windows share tetrahedra, so consecutive frames differ by at
most `(δ_j + δ_{j+1})/τ_{j+1}` with no case distinction on determinants; telescoping gives
`1.2 (b/(s_*τ_*)) (n+2)² ‖η‖₂` for every `Y`, and a local form.  Checked numerically step by
step on arbitrary competitors (420 pairs; separations 5 to 7 in the local form).
**Theorem L⁺**: squared distances are exactly quadratic, `η = 2AV + Q(V)`, `‖Q(V)‖ ≤ Λ‖V‖²`;
with Theorem L excluding the far branch of the quadratic inequality, `d_P ≤ ‖η‖/(μ + √(μ² − Λ‖η‖))`
for `‖η‖ ≤ μ/(ΛC_L)`.  Its first numerical check "failed" by a factor 29 — round-off in the
closed form of the Procrustes distance at displacements of `10⁻⁹` (DG-25); with explicit
residuals the bound is attained to `6·10⁻⁵`.
**What it is worth** (`local_data_guarantees.py`): on a 20-point helix-like trace
`C_L = 456` against `1/(2μ) = 0.45`; the certified range is `3·10⁻⁶` ångström in rms distance
error.  Stated as such in the note, to Science (GEOMETRY-RES-0007) and in O-16.
**Science's requests A4-GEO-1 … -6** applied: §5 of the note is built from their text with
"[A4]" on what they read; Theorem K(a) marked known with their better constant.
Harness: 46 tests, 34 mutations caught.

## 2026-11-26, ninth checkpoint (work from 20:11 UTC; see the commit time)

**The planted model for Complexity became a section of the report.**  Writing down "what
would a low-degree analysis be about" for COMPLEXITY-RES-0002 led to: below the conic
threshold the states are the rank-3 points of the solution space `L` of the linear system
(a MinRank problem), and the `4 × 4` minors can be used as linear equations on quartics.
First numerical results (`demix4.py`): the certificate `h_4 = K` holds from 11 atoms for
two states and 17 for three; states recovered to `10⁻⁷`.
**Prior art, before commit** (DG-21): this is the algorithm of Johnston–Lovitz–Vijayaraghavan
(linear sections of varieties), with higher levels by Derksen–Johnston–Lovitz and the
dimension count as conjectured exact threshold by Dastidar–Weich–Wein; three papers read
in part through fetches.  §6.2 and GEOMETRY-RES-0006 rewritten to say so.  A crude
asymptotic claim was removed after evaluating it (DG-22).
**Exact arithmetic** (`exact_demix4.py`): rational chain witnesses reduced modulo 65521;
all minors by Laplace expansion in `int64`; streaming reduced echelon form with products
in `float64` (exact below `2^53`); the rank lower bound `C(m+3,4) − K` proves the
certificate.  Proved: `K = 2, n = 11`; `K = 3, n = 17` (both angles; integer cross-check at
a second prime); `K = 4, n = 32` (8 min) and `n = 30` (27 min, 77 323 of 122 760 minors read).
**The structural point is harmless** (Proposition 6.2 (h)): at `n = 6K − 2` the space `L`
contains one rank-2 matrix with `c = 0`; the minors vanish to second order there, which
costs exactly `m = dim L` conditions; exact ranks give `h_4 = K + m` at `K = 2, n = 10`
(63 of 70) and `K = 3, n = 16` (4825 of 4845), and then the only rank-3 points with `c ≠ 0`
are the states.  Floating point had given 21 and 24 for the second defect instead of 20
(DG-23).  Hence **Theorem I′**: identifiable among all ensembles from 10, 16, 30 atoms.
**A planted error that was not an error:** the first mutation of the new test ("principal
minors only") is not a mutation at `K = 2, n = 11` — the fifteen principal minors already
span the thirteen-dimensional space there — and the mutation harness reported it as
missed.  Replaced by "ignore the structural point" (must fail at `K = 2, n = 10`).
**Fetch at 21:55 UTC:** SCI-REV-0023 (originality review of Theorem L, with a relevance
assessment); SCI-RES-0036; COMPLEXITY-RES-0008 and -MSG-0004; Ensemble's E20″, E21; nothing
from Engineering or Theory addressed to us.  Then the research owner's supplementary
directive (seventh division).  Harness: 43 tests, 31 mutations caught.

## 2026-11-26, eighth checkpoint (work from 19:42 UTC; see the commit time)

**Theorem L** (`LOCAL_DATA_STABILITY.md` §3): global upper bound `6.9 (b/τ²) n(n+1)‖η‖₂` from
squared distances of separation `≤ 4`; proof by frames of overlapping windows (local
Procrustes lemma `‖M − R‖ ≤ 2e/τ²`; the separation-4 distance excludes a reflection between
windows: margin `4τ²/√3` against `|η| + 17ξD²`; rotations telescope without amplification).
**Theorem K(c) proved** (tube bound by Euler–Bernoulli test fields), Corollary K.1 corrected
and strengthened (DG-19).  Prior art: Arias-Castro–Vishwanath (exponential constant for this
lateration graph), read through one fetch.  Tests `tube_bound_helix`,
`local_procrustes_lemma`, `theorem_L_instances`.
**Fetch at 19:52 UTC — three things had arrived.**  (1) Science's review SCI-REV-0021 of
our report: Lemma 2.2, B, B′, 4.2, G proved as stated; F3: Theorem B at `d = 1` is
Laurent–Poljak 1996 (we had the source and did not read it); its Proposition R22-1 **is our
Theorem M (b), earlier and with the half-turn exception** — our RES-0003 had crossed it
(DG-20).  (2) Ensemble's ENSEMBLE-RES-0003: caution on E5 (b) for Theorem J (b); a reading
of Theorem I; a torus certificate E20′.  (3) Theory's THY-MSG-0018 §4.
**Done in response:** exact elimination for the hinge candidates (Singular over `ℚ`: degree
8 reduced for two hinges, 2 for three); the sharp criterion (at most one half-turn among
`R_1, R_2, R_1R_2`), verified by linear programmes; the rank question of the Ensemble
division (19, but non-adjacent products are invisible; adjacent pairs suffice); a count for
`k` bodies (clean only in the minimally redundant case); all findings F1–F10 applied;
GEOMETRY-RES-0004, -0005, GEOMETRY-MSG-0007.  Harness: 41 tests, 29 mutations.

## 2026-11-26, seventh checkpoint (work from 19:15 UTC; see the commit time)

**Hinge ensembles** (`HINGE_ENSEMBLES.md`; answer GEOMETRY-RES-0003 to the Science division's
SCI-RES-0029 §3).  Question: two states that differ in two or three torsions violate (CC);
are they identifiable?  Path: (1) a competing state is a linear image of the stack, hence
moves each conic-free shared segment by an element of `O(3)` — and nothing forces it to be
proper; (2) cleaner: apply Theorem A to each segment, so competing ensembles live on
`O(2)^s` (Proposition M2); (3) the data are the interval moments `𝔼[g_p⋯g_q]` (Lemma M1);
(4) for two hinges one kernel vector of the block moment matrix cuts the support down to
eight points, `(ρ_B^βρ_A^α, ρ_A^ασ^γ)`, a cube generated by three reflections with the states
at opposite vertices; the only affine relation is the parity; first moments kill the six
virtual chains (Theorem M).  Verified numerically, including a search over all chains.
Science's count `dim 𝒩 = 10, 6, 3` is an equality (proved for one and two hinges by adapted
bases).  Several states: explored; three states at two hinges can fail; a first guess for a
threshold was wrong (DG-18).  Theorem F″ for block sums (one line).  Prior art: three
searches.  Harness: 36 tests, 24 mutations.

## 2026-11-26, sixth checkpoint (work from 18:26 UTC; committed 19:14 UTC as `cd4a2ec`)

**The internal review arrived (18:55 UTC)** — `GEOMETRY-REV-0001.md`, verbatim, with our
response; the referee's directory is `experiments/geometry/review1/`.  No false theorem.
Major: (M1) "universal ⇒ second-moment rigidity" false without `𝒩(X) = 0` (a slogan in the
Summary, §9, the register, the Lean heading, three messages) — the counterexample is now in
Lean (`universal_not_secondMomentRigid`); (M2) three sentences claimed more than the local
Theorem H; (M3) a gap in Theorem E(d), filled with the referee's exact witness, re-verified
(`exact_hierarchy_witness.py`); (M4) Corollary 9.1's moment-order sentence.  Sixteen minor
findings applied.  Adopted from the referee with credit: soundness of the DEMIX certificate
for every realizable input; no stress within separation `3K`; helices never satisfy (CC);
`κ` is 2–12 times below its local values.  Process error recorded: the register said
"reviewed" before the review existed.
**Lean:** `mixture_identifiable_stacked` (Theorem B in coordinates, finite competing
mixtures) with the two-state instance `line_mixture_example`; whnf timeout in the first
attempt removed by stating the hypotheses as separate `have`s and giving `V`, `W` explicitly.
**Theorem C(c) rewritten:** generic rank concave along the chain (submodularity + shift
invariance), strictly increasing until `D_K`, `2N − 1` for `N ≤ 3K`; threshold
`(9K² − 5K + 6)/2` for every `K` and bond angle.  The same argument proves that the
general-position hypothesis of Theorem F′ is generic for every `K`.  Exact conic ranks to
`K = 20`.  Attempt at the sharp threshold for all `K`: not achieved; what was learnt is in
`PROOF_OBLIGATIONS.md` O-1 (Jacobi-matrix and Schur-square reformulations; the trichotomy
A/B/C at a first defect; a defect can only occur within `O(K)` conditions of the threshold
under a parameter count that is not proved).
**Synchronisation (fetch of 18:52 UTC):** Science SCI-RES-0029, Ensemble ENSEMBLE-RES-0001 and
-MSG-0003, Complexity COMPLEXITY-RES-0002 read; receipt and a first remark in
GEOMETRY-MSG-0006; answers owed.
Harness: 34 tests, 22 mutations.

## 2026-11-26, fifth checkpoint (18:04–18:15 UTC)

**An error of record found and corrected (DG-12).**  `date -u` at 18:08 showed that every
header time we had published was an estimate, off by up to three hours, and that two
sentences about other branches' existence were false.  Corrected in place with bracketed
notes; GEOMETRY-MSG-0005.
**Lean:** `mixture_state_of_conic` (Theorem B's algebraic core from the conic condition on);
full build and audit: 5072 declarations.  **Proposition 9.2:** third moments identify
unconstrained mixtures under proper rotations (alternating 3-form; contraction ranks).
**Remark 5.1:** the gap between identifiability and the linear certificate is a MinRank
problem of target rank 3; Kipnis–Shamir linearisation works exactly from the conic
threshold on.  Worst conformations at `m = 16`: `0.622` against `0.785` (ratio 1.26).

## 2026-11-26, cycle 2 begins (after 17:56 UTC)

**Theorem K** (`LOCAL_DATA_STABILITY.md`): sequence-local distance data and global shape.
(a) Courant–Fischer with nine cosine-times-translation fields: `s_7² ≤ (5π²/3)K(K+1)(2K+1)/n²`
for every configuration (known in substance).  (b) One torsion move changes only the
`(K−1)(K−2)/2` straddling distances, each by at most `2 sin(δ/2)` times the smaller lever:
`‖Δd‖₂ ≤ 2 sin(δ/2) b √T_K`, `T_K ≤ K⁴/48` — so the exact per-torsion superposition constant of
the theory report is a *lower* bound for the instability of local data (global).  (c) Helices:
`s_7 n²` constant (exponent `−1.98`), softest mode torsional.  The hinge bound scales like
`n^{-3/2}`, coherent bending like `n^{-2}`.  Random coils not understood (noisy exponents).

## 2026-11-26, cycle 1, third checkpoint (17:19–17:56 UTC)

**Synchronisation.**  All five other branches fetched at 17:19 UTC (theory `f0e5a62`,
engineering `eb6b872`, science `5c233cc`, ensemble `a570520`, complexity `4b18ebb`).  The
Ensemble division's first checkpoint (16:48 UTC, six minutes before ours) overlaps ours in subject and not in
content: its E1 (exposedness) is the general principle behind our certificate; its E1.3
(mean squared lengths determine nothing) is our Proposition 3.1, on the unconstrained
space; its E7 calls "ensemble rigidity" what is equivalent to global rigidity.  We renamed
ours **second-moment rigidity** (Lean, report, registers; `DEAD_ENDS.md` DG-11).

**Theorem J.**  Their E5/E6 applied to the chain variety: the laws of the distances of
separations 3 and 4 determine every generic finite ensemble of chains.  Exact matroid
computations for other patterns and for two rigid bodies (`matroid_connectivity.py`).

**O-3, numerically settled.**  The direct search (random couplings) had found nothing in
30 minutes.  The inverse construction — random chain and five random pairs, the unique
stress, definiteness of `tr(VᵀΩV)` on the flexes, then global optimisation — finds strict
local maximisers with indefinite stress in 2 % of random instances and global ones in
about 0.15 % (`explore_er3.py`).  Instances A and B verified with a `24⁴` grid, 2 000 local
searches and an explicit four-dimensional realisation (`er_not_ur_instance.py`).  Request
for a certificate: GEOMETRY-REQ-0006.

**For the theory division (GEOMETRY-RES-0002).**  Exact small-angle Kabsch cost of a kink
on a rod, `I_red φ²(1 − 3x(1−x))`: a quarter of the coaxial cost at mid-chain (discrete
chains: 0.2500 at `n = 600`).  Worst conformations: the verified constants are attained up
to 1.22 at `m = 8`.  Free–free beam Green's function as the exact quadratic form.

Harness: 27 tests, 15 mutations.  Lean rebuilt after the renaming: 5071 declarations.

## 2026-11-26, cycle 1, second checkpoint (16:54–17:18 UTC)

**The non-linear threshold for two states is a theorem (Theorem I).**  Singular 4.3.2
installed locally (`apt-get install singular`).  First run (`K = 2`, `n = 10`, modulo 32003):
the rank-≤3 locus of `ℙ(L) ≅ ℙ⁴` has degree **7**, not 2 — the request GEOMETRY-REQ-0001
item 1 had expected "two reduced points".  Primary decomposition over `ℚ` (7 minutes): three
rational points with lengths 1, 1, 5; the third has `c = 0` and rank 2.  Explanation found:
`S = abᵀ + baᵀ` with `a ⊥ u_1..u_5`, `b ⊥ u_5..u_9` — two hyperplanes contain all 17 stacked
edge vectors; at a rank-2 point all `4 × 4` minors vanish to second order, so the local length
is at least `1 + 4`.  Therefore degree 7 *proves* that nothing else exists, and upper
semicontinuity of the fibre length makes it generic.  `n = 11, 12`: degree 2.
**Below the threshold:** `n = 7, 8` — explicit mixtures of 9–11 other chains with the same
averaged data (linear program over sampled points of `𝒫(z)`), so the ensemble is *not*
identifiable among all ensembles there, although Theorem H makes it locally unique among
two-state ensembles; `n = 9` — identifiable in six instances.  Three thresholds for two
states: 7 (number of states known), 10 (outright; 9 numerically), 12 (linear certificate).
Harness: 25 tests, 13 mutations.  GEOMETRY-MSG-0003 (linked update of GEOMETRY-REQ-0001
item 1 and of GEOMETRY-MSG-0002 item 10).

## 2026-11-26, cycle 1

**Synchronisation.**  Read: root `README.md`; `docs/collaboration/README.md`; theory report
§0, §1, §4 (realizability, distances versus superposition, holonomy, torsion-to-RMSD),
§11.14–11.15 (chains; lever-arm law, D42); the head of `docs/collaboration/status/theory.md`;
the engineering division's ENG-MSG-0006 (the research owner's directive on mathematical
generality, relayed).  Not read: the rest of the theory report (1.1 MB), the science and
engineering branches beyond their latest commit titles and ENG-MSG-0006.  Remote heads at
15:35 UTC: theory `a844b5a`, engineering `88feab9`, science `2b4ccdf`; no branch yet for the
Ensemble Identifiability and Biological Complexity divisions, none for this one.

**Environment.**  Lean 4.31.0 unpacked in `~/.lean` (release archive; `zstd` absent, unpacked
with Python `zstandard`), Mathlib cache fetched, the theory division's project built
(8648 jobs, axiom audit OK: 5051 declarations); Python 3.13 with numpy, scipy, sympy, mpmath.

**Choice of problem.**  Candidates considered and why not (details in `DEAD_ENDS.md`):
combinatorial characterisation of generic rigidity of chains with distance bars (DG-1: as
hard as rigidity in space); quadratic-form sharpening of the lever-arm bound (DG-2: no gain
in the worst case); stress-based global stability of universally rigid frameworks (DG-3:
known); beam-law scaling for trilateration chains (DG-4: known in substance; kept for
cycle 2 only if a sharp or global statement is possible); realization counts (DG-5).
Chosen: the interaction of rigidity with distribution-level inference (item F of the
mandate), because the stacking lemma turns it into rigidity theory of one framework in a
higher dimension and the chain constraints do something non-trivial there.

**Sequence of findings.**
1. Stacking; the `O(3K)` indeterminacy; the reduction of competing decompositions to
   rank-3 projectors `P` with `eᵀPe = w|e|²` on bond vectors; the linear space `𝒩`; the trivial
   quadrics.  First numerical check: nullities exactly `max(K − 1, dim Sym(3K) − (2n − 3))`.
2. The argument works against *all* ensembles (Hilbert-space version), not only `K`-state
   ones; simplicial faces.
3. Demixing by linear algebra; exact recovery at the thresholds for `K = 2, 3, 4`.
4. Exact witnesses (modular ranks) to `K = 12`, two bond geometries, both constraint sets.
   A proof for freely jointed chains for every `K` (evaluation functionals at generic points
   of a product of spheres).  For chains with bond angles: a proof with a weaker threshold;
   the sharp one stays a conjecture (O-1).
5. `K = 1`: the conic criterion is the classical affine-flex lemma read for ensembles.
   The set of realizable averaged data against its semidefinite relaxation: equal up to 6
   atoms (Barvinok–Pataki), different from 7 on (exact rank-4 witness with unit quaternions).
6. Second-moment rigidity between global and universal rigidity; a numerical 6-atom instance of
   "globally rigid but averaged data reproduced by two other chains" (to `10⁻¹⁵`).
7. Local identifiability: complete data from `n = 2K + 3`, sequence separation `K + 3`
   (exact, `K ≤ 8`), with an extension lemma in `n`.
8. Below the conic threshold: spurious rank-3 solutions exist at `n = 9` (`K = 2`) but carry
   no mass; none from `n = 10` (`K = 2`) and `n = 14` (`K = 3`).  Conjecture `⌊9K/2⌋ + 1`.
9. The dual certificate `φ(X) = ‖Π^⊥X‖²` and the global `W₂²` bound; (CC) implies
   infinitesimal identifiability.
10. Lean: `proofs/Geometry/EnsembleRigidity.lean` (stacking, stress energy, stress
    certificate, block rigidity, affine flexes, two steps of the hierarchy); full build and
    axiom audit: 5071 declarations, standard axioms only, zero warnings.
11. Prior art (eight searches, summaries only): `PRIOR_ART.md`.

**Search for an second-moment rigid, not universally rigid chain (O-3).**  7 atoms, 5 random
measured pairs, random couplings, global maximiser over the 4-torus by multi-start
(`explore_er2.py`).  First pass (40 instances, BFGS only): most maximisers have a positive
semidefinite stress (and many are planar); two apparent candidates were artefacts (DG-6).
Second pass with polished optima: see the entry below when it has finished.

**Not done in cycle 1.**  Anything on single-conformation quantitative rigidity beyond the
dead ends above; anything on non-squared-distance observables; no computation requested
from the shared Modal budget (all computations of this cycle ran locally in seconds).
