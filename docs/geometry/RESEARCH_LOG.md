# Research log — Geometric Inference, Rigidity and Inverse Problems Division

Branch `research/geometric-inference`, created 2026-11-26 from the theory checkpoint
`a844b5a` (`claude/determined-ride-og1u7j`).  Newest entry first after "Resume here".

## Resume here

State at the tenth checkpoint (see `HANDOFF.md` for commands and environment):

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
   (SCI-REV-0023): mechanism and scaling known.  **Proofs of §3 unreviewed.**  The honest
   size of the guarantee is in §6: certified range `10⁻⁵` ångström or less on idealised
   traces.  Open: O-16 (close the gap between `C_L` and `1/(2μ)`; random noise; incomplete
   windows).
3. **Third note:** `HINGE_ENSEMBLES.md` (states that share rigid segments; the main
   statement is the Science division's Proposition R22-1).  Open: O-12, O-13, O-14,
   R22-GEO-3, -4, -5.
4. **Owed:** **the research owner's supplementary directive**
   (about 22:00 UTC): a seventh division, Structural and Computational Biology (branch
   `research/structural-biology`, not on the remote at 22:02 UTC) — send it an orientation
   (seven items), `docs/geometry/IMPLEMENTATION_GUIDE.md` (specifications of what is ready
   for software: DEMIX, DEMIX-4, the certificates, with proof status, Lean declarations,
   assumptions, input and output, complexity, counterexamples, conditioning, validation)
   and `docs/geometry/BENCHMARKS.md` (unique / non-unique / locally-not-globally
   identifiable / identifiable-but-hard / ill-conditioned / assumption-violating instances).
   Distinguish global identifiability, local identifiability, algorithmic recoverability
   and efficient certification; claim nothing about real molecular systems.
5. **Open, in priority order** (`PROOF_OBLIGATIONS.md`): O-15 (Conjecture 6.3: four states
   at 24 to 29 atoms — `exact_demix4.py 4 28` is feasible locally in about three hours;
   three states at 15 atoms needs degree 5 and the structural locus; stability of the rank
   certificate under noise), O-1, O-3, O-2 (b)–(d), O-4, O-5.
6. **Next synchronisation:** fetch all six other branches (the sixth is
   `research/structural-biology`) and look for `GEOMETRY` in their `docs/collaboration/`.

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
