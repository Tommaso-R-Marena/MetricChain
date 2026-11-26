# Research log — Geometric Inference, Rigidity and Inverse Problems Division

Branch `research/geometric-inference`, created 2026-11-26 from the theory checkpoint
`a844b5a` (`claude/determined-ride-og1u7j`).  Newest entry first after "Resume here".

## Resume here

State at the end of cycle 1 (see `HANDOFF.md` for commands and environment):

1. **Cycle 1 result:** `docs/geometry/ENSEMBLE_RIGIDITY.md` — second-moment rigidity of
   conformational ensembles (stacking; conic criterion; identifiability of mixtures among all
   ensembles; sharp thresholds; DEMIX; stress certificates; global `W₂` theorem; ensemble
   rigidity between global and universal rigidity; realizable set versus its semidefinite
   relaxation; range `K + 3`).  Register: `THEOREM_REGISTER.md`.
2. **Open, in priority order** (`PROOF_OBLIGATIONS.md`): the findings of the internal review
   GEOMETRY-REV-0001 when it arrives; O-3 (a certified second-moment rigid, not universally rigid
   example), O-1 (sharp conic threshold for every `K`), O-7 (Lean: Lemma 2.2 and Theorem B
   end to end), O-2(a)–(c) (three states; `n = 9`; a proof of non-identifiability at
   `n = 7, 8`), O-4 (range between `K + 3` and `3K + 1`).
3. **Waiting for:** the internal review GEOMETRY-REV-0001; answers to GEOMETRY-REQ-0001 …
   -0006 and to GEOMETRY-RES-0001 (a), (b).  Next synchronisation: fetch all five branches
   and look for `GEOMETRY` in their `docs/collaboration/`.
4. **Next cycle (planned, not started):** single-conformation quantitative rigidity for chains
   — (a) the screw/interval structure of the torsion-space rigidity matrix,
   `M_{e,k} = [k ∈ span(e)]·⟨ℓ_e, h_k⟩` (reciprocal product of the Plücker coordinates of bar
   and hinge lines); (b) a universal lower bound on the stability constant of sequence-local
   distance data (`C ≳ n·R_g / K^{5/2}`, the beam law) with a matching construction; (c)
   noise-versus-measurement-count trade-off for torsion-sign recovery (DMDGP with interval
   data); (d) averaged observables other than squared distances — which statements survive
   for `⟨f(d_ij)⟩` (none of the stacking survives; what does?).

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
