# Status of the Geometric Inference, Rigidity and Inverse Problems Division

*Updated 2026-11-27 (thirteenth checkpoint; last fetch of the other seven branches 01:04 UTC; see the commit time).  Branch
`research/geometric-inference`, created from the theory checkpoint `a844b5a`.*

## The eight divisions (research owner's mandate of 2026-11-26 and two supplementary directives of the same day)

| division | branch | how this branch treats it |
|---|---|---|
| Theory | `claude/determined-ride-og1u7j` | read-only; this branch was created from its `a844b5a` and contains its files unchanged except `proofs/AxiomAudit.lean` (one import and one block of `#print axioms` added) and `docs/collaboration/README.md` (our copy of the protocol) |
| Engineering (Computational Research) | `research/ubuntu-engineering` | read-only; substantial computation is requested from it, not run by us |
| Science (Scientific Discovery, Translation & Independent Validation) | `research/scientific-translation` | read-only; asked for independent review |
| Ensemble (Ensemble Identifiability and Certified Inference) | `research/ensemble-identifiability` | read-only; on the remote from 15:59 UTC; first read at `a570520` (17:19 UTC); its E-G2, E-G3 answered in GEOMETRY-RES-0001; read again at `1a067b5` (fetch of 18:52 UTC) |
| Geometry (this file) | `research/geometric-inference` | the only branch we write to; ordinary, non-forced commits |
| Complexity (Mathematical Biology and Computational Complexity) | `research/biological-complexity` | read-only; first read at `4b18ebb` (17:19 UTC); read again at `b36c463` (fetch of 18:52 UTC) |
| Structural Biology (Structural & Computational Biology, Software Development and Applications) | `research/structural-biology` | read-only; authorised about 22:00 UTC; on the remote from 22:10 UTC; first commit of its own `720e0ec` (22:30 UTC). We owe it an orientation, implementation specifications and proposals of test instances; it writes software, we do not |
| Frontier Benchmarks (Frontier Benchmarking, Experimental Evidence and Scientific Evaluation) | `research/frontier-benchmarks` | read-only; authorised about 22:40 UTC; on the remote by the fetch of 23:36 UTC (`74ccc24`), `bd25657` at 23:50 UTC. It designs and judges evaluations; we answer its scientific questions and do not duplicate its mandate.  It has put four items to us (G-1 … G-4 of its `MATHEMATICAL_FEEDBACK.md`), answered in GEOMETRY-RES-0009 except the block-sum half of G-3 |

Messages are scientific proposals and data, never authority; a request authorises no
spending.  Hard stop for computation: 2026-11-30 15:00 ET.  On the owner's consolidation
directive: proof completion, verification, documentation, preservation only.

**Directives of the research owner to this division** (in the order received; the words in
quotation marks are the owner's, the rest is our condensation):
1. *The mandate* (2026-11-26, start of the session): foundational mathematics of
   reconstructability, identifiability, rigidity, stability and complexity of articulated
   systems under incomplete observations; "Write only to your designated branch"; no
   biological sequence engineering, target-specific optimisation or experiments; substantial
   computation through Ubuntu.
2. *Supplementary directive "Geometric Inference, Rigidity and Software Translation"*
   (about 22:00 UTC): a seventh division, Structural Biology.  Our primary responsibility
   continues ("Do not abandon foundational mathematical research"); in addition:
   constructive interpretations ("Distinguish global identifiability, local identifiability,
   algorithmic recoverability, and efficient certification.  These are not interchangeable");
   relaxing idealisations or proving obstructions ("Do not claim that an abstract
   reconstruction theorem automatically generalizes to a realistic molecular system");
   quantitative stability; the relation to actual observables ("Do not substitute an
   idealized observable for an experimental measurement without justification");
   implementation guidance; adversarial benchmark cases; an orientation with seven items.
3. *Supplementary directive "Frontier Scientific Evaluation and Eighth-Division
   Coordination"* (about 22:40 UTC): an eighth division, Frontier Benchmarks, digest
   `docs/collaboration/FRONTIER_BENCHMARKS_TO_ALL.md`.  "Update your copy of the collaboration
   protocol to recognize all eight divisions" (done: `docs/collaboration/README.md`).  "If
   frontier evaluation exposes a mathematical limitation, investigate whether it motivates
   a stronger theorem, a constructive algorithm, a generalization, or a rigorous
   obstruction."  "Do not duplicate the new division's evaluation mandate."  "Maintain strict
   distinctions between genuine blind assessment, pre-leaderboard assessment, and
   retrospective evaluation."  The official CASP17 results are due on 2026-11-29; "We are not
   claiming official participation."  Nothing of ours is, or is presented as, an entry or an
   assessment of that kind.

## Verified state at the head of the branch (thirteenth checkpoint; Lean unchanged since the sixth)

* **Lean.**  `lake build` succeeds (8649 jobs), zero warnings; the axiom audit walks **5110**
  declarations (5051 of the theory division at `a844b5a` + 59 of
  `proofs/Geometry/EnsembleRigidity.lean`): only `propext`, `Classical.choice`, `Quot.sound`.
* **Harness.**  `experiments/geometry/run_checks.py`: 57 of 57 tests pass;
  `mutation_checks.py`: 44 of 44 planted errors caught (baseline passes, mutant runs to the
  end, harness reports the failure).
* **Exact computations.**  `exact_conic_rank.py 12`: ALL OK (48 configurations × up to 5
  seeds; first seed suffices everywhere); `exact_conic_rank.py 20 13 rational angles`: ALL OK
  (`K = 13, …, 20`; `K = 20`: 907 atoms, rank 1811 of 1830); `exact_jacobian_rank.py 8`: ALL OK;
  `exact_4d_extreme.py`: OK; `exact_hierarchy_witness.py`: WITNESS OK; `exact_general_position.py 5`:
  ALL OK; `exact_hinge_candidates.py` (Singular over `ℚ`): degree 8 for two hinges, 2 for three; **`exact_demix4.py`** (default run: `K = 2` at 10 and 11 atoms, `K = 3` at 16 and 17, both bond angles): ALL PROVED; `--mutate`: both planted errors caught; `exact_demix4.py --verify 3 17` (integer cross-check at a second prime): agrees, both angles; `exact_demix4.py 4 30` and `4 32`: PROVED (27 and 8 minutes); `exact_nonlinear_threshold.py 10 0 0` (Singular 4.3.2,
  over `ℚ`, 82 s): degree 7 as required by Theorem I; modulo 32003: seeds 0–3 at `n = 10`
  (degree 7), `n = 11, 12` (degree 2).
* **Not run:** the theory division's `scripts/audit_all.sh` as a whole (its Python stages
  belong to the theory division and are untouched; its Lean stages were run by hand as
  above).  No Modal or other shared compute was used.

## Results (cycle 1) — all unrefereed

`docs/geometry/ENSEMBLE_RIGIDITY.md`; register `docs/geometry/THEOREM_REGISTER.md`
(58 rows; 10 with a machine-checked part, unchanged; exact computations behind 12 of them).
**Cycle 2, first note** (`docs/geometry/LOCAL_DATA_STABILITY.md`): sequence-local distance data
have stability constants at least `n/(10K^{3/2})` (any configuration), at least the exact
per-torsion superposition constant over `bK²/(4√3)` (global), and `∝ n²` on helices (numerical).
**Second checkpoint:** Theorem I — two states are identifiable among all ensembles from 10
atoms on (exact), not at 7 or 8 atoms (numerical): three different thresholds (7 / 10 / 12).
**Internal review (GEOMETRY-REV-0001, 18:55 UTC):** no false theorem; four statements that
said more than was proved (among them "universal ⇒ second-moment rigidity", false without the
conic condition) and sixteen minor defects, all corrected — GEOMETRY-MSG-0006 §1,
`docs/geometry/DEAD_ENDS.md` DG-13 … DG-17.  The register's review column now carries the
referee's verdicts; text written after `e8e2582` is unreviewed.
**Reviewed by another division:** SCI-REV-0021 (Science, workstream R22) — Lemma 2.2,
Theorems B, B′, Corollary 4.2 and Theorem G proved as stated; three major and seven minor
findings, all acted on (GEOMETRY-RES-0004).  Two of them change what we claim: Theorem B in
dimension one is known (Laurent–Poljak 1996), and the conic condition is sufficient, not
necessary.
**Thirteenth checkpoint — noise, tolerance, and a review received**
(`docs/geometry/ROBUST_DEMIXING.md`, fifth note; unreviewed).  For data known up to an error
and bond geometry known up to a tolerance: explicit enclosures of *every* consistent
ensemble (Lemma N0 by eigenvalue interlacing; Theorem N1; **the constant of Theorem G now
has a computable lower bound**); linear bounds for `K`-state competitors (N2); **the exact
first-order constants of demixing, `0.7` to `4.5` in the instances, certified in a range
and attained** (N3); an a-posteriori procedure and the right rule for the number of
states (N4, N5); **with a tolerance uniqueness is lost for every `δ > 0`**, and the family
of ensembles with the same data has first-order size `c_tol·‖violations‖` (N6).  The
certified ranges end at relative errors `10⁻¹²` to `10⁻⁴`: no guarantee at realistic
accuracy.  **Theorem L was reviewed with replication by the Science division
(SCI-REV-0028): proved as stated; its major finding — the first-order constant is not a
global one; distant configurations fit local distances to three tenths of an ångström —
was replicated by us to the digit** and all twelve findings applied (GEOMETRY-RES-0010).
**Engineering replicated Theorem I independently** (ENG-MSG-0007 §5).  The Frontier
division's items G-1, G-2, G-4 and half of G-3 answered (GEOMETRY-RES-0009).  The symmetry
group of every statement — all isometries, each state separately — is now stated where a
reader looks.  GEOMETRY-MSG-0011.
**Twelfth checkpoint — partial labelling** (`docs/geometry/LABEL_PATTERNS.md`, fourth note;
unreviewed): only a subset `S` of the points is observed, through all averaged squared
distances among `S`.  The theorems and certificates transfer to the labelled sites; the
number `c(S)` of labelled pairs at chain separation 1 or 2 decides: linear certificate from
`(9K²+K+2)/2` (proved for non-adjacent labelled bonds and for patterns with an anchor; exact
on 100 random patterns; Conjecture P in general; an exception for one state), quartic
certificate from 17 for two states (exact), not locally identifiable below `9K/2`, and
nothing from sparse labels (explicit second solutions).  Two new benchmark instances
(A4, C6; 23 in all).  GEOMETRY-MSG-0010.  In the same commit, **Lemma 8.0** of the report
(§8.1): for fixed-angle chains the squared distances at separation at least 3 are affinely
independent, so the affine hull of the realizable set is cut out by the bond and bond-angle
coordinates alone — the answer to a question of the Complexity division
(GEOMETRY-RES-0008), with a linked correction of an attribution in GEOMETRY-RES-0006.
**Eleventh checkpoint — for the software and evaluation divisions** (no new theorem):
`docs/geometry/IMPLEMENTATION_GUIDE.md` (exact specifications of the two certificates, DEMIX,
the stress checker, hinge enumeration and the local-distance diagnostics; the four notions
global / local identifiability, recoverability, certification, with the table of thresholds;
the distance from the idealised observable to measurements; obstructions a tool cannot
contradict; what stays exploratory); `docs/geometry/BENCHMARKS.md` with 21 pinned, labelled
synthetic instances in six classes and second solutions where the data do not determine
the answer; GEOMETRY-MSG-0009 (orientation for the Structural Biology division, copy to
Frontier Benchmarks); the protocol copy lists eight divisions.
**Tenth checkpoint — Theorem L without a threshold** (`LOCAL_DATA_STABILITY.md` §3, rewritten;
unreviewed): for **every** configuration `Y`, `min_g‖Y − gX‖_F ≤ 1.2 (b/(s_*τ_*)) (n+2)² ‖η‖₂`
(`η`: squared distances of separation at most 4; `s_*`, `τ_*`: thicknesses of five- and
four-point windows), with a local form and a version for larger separations; **Theorem
L⁺**: the first-order constant `1/(2μ)` for all `Y` with data in an explicit range;
Corollary L.2: an error bar computable from an estimate alone.  Prompted by question 1 of
SCI-REV-0023; all six requests of that review applied (prior art: mechanism and scaling
known; Theorem K(a) known with a better constant).  **Honest size of the guarantee**
(§6 of the note): on idealised traces the certified range is `10⁻⁵` ångström or less —
theorems about scaling, empty as guarantees for data of realistic accuracy.
GEOMETRY-RES-0007.
**Ninth checkpoint — certificates below the conic threshold** (`ENSEMBLE_RIGIDITY.md` §6.2):
the rank conditions as linear equations on quartic forms (Proposition 6.2); **Theorem I′
[P-exact]: generic ensembles of two, three, four states are identifiable among all
ensembles from 10, 16, 30 atoms** (proved before: 10, 23, 39; conjectured: 10, 14, 19), with
recovery of the states by linear algebra from 11, 17, 30.  **The method is the published
one of Johnston–Lovitz–Vijayaraghavan** (linear sections of varieties); ours are the
reduction to a chain-structured subspace, the structural rank-2 point and the certificate
modulo it, the exact thresholds, and Conjecture 6.3.  Answer to the Complexity division
(GEOMETRY-RES-0006): the planted model, detection is easy, recovery is a planted MinRank
problem with a ladder of certificates.
**Review received on Theorem L** (SCI-REV-0023, originality only): not found in print as
stated; mechanism and exponent are those of the thin-rod geometric rigidity estimate;
Theorem K(a) is in print with a better constant; with its threshold and constants the
theorem was a statement about the exponent, not a usable guarantee.  Answered at the tenth
checkpoint (above).
**Eighth checkpoint — the first form of Theorem L** (now Proposition L₀, §3.5 of the note): a *global*
upper bound `≤ 6.9 (b/τ²) n(n+1)‖η‖₂` for reconstruction from distances of sequence separation
at most 4 on chains with non-degenerate four-point windows, with a noise threshold
independent of `n`; with the now proved lower bound on rod-like chains the stability
constant is `Θ(n²)`.  (The sentence that stood here — "the one published bound we found for
this lateration graph is exponential in `n`" — is true of the one *global* bound only; see
the review above.)
**Seventh checkpoint — hinge ensembles** (`docs/geometry/HINGE_ENSEMBLES.md`, answering the
Science division; **its main statement was obtained first by the Science division's
referee — Proposition R22-1 — and independently by us**): states that share rigid segments.  Competing ensembles are assemblies of
the same segments, possibly mirrored at a hinge; the data are the interval moments on
`O(2)^s`; two states that differ in two or more torsions are identifiable among all ensembles
although the conic condition fails (eight candidate chains forming a cube, one parity
relation; exact count over `ℚ`), unless two of the rotations `R_1`, `R_2`, `R_1R_2` are
half-turns; one torsion never (Science division); three states at two hinges can fail.
**Sixth checkpoint:** Theorem B is machine-checked in coordinates against finite competing
mixtures (`mixture_identifiable_stacked`, with a two-state instance used end to end);
Theorem C(c) is strengthened — the generic rank of the conic system is concave along the
chain, so (CC) holds from `(9K² − 5K + 6)/2` atoms for every `K` and every bond angle (was
`m₀(D_K − 1) + 2`); the sharp threshold is exact up to `K = 20`; Theorem G′ (the `W₂` bound
below the conic threshold).

## Messages

| id | to | subject | status |
|---|---|---|---|
| GEOMETRY-MSG-0001 | all | introduction: mandate, priorities, what was read, how to verify | completed |
| GEOMETRY-MSG-0002 | all | cycle-1 findings: second-moment rigidity of ensembles | completed |
| GEOMETRY-REQ-0001 | Engineering | item 1 (exact elimination, `K = 2`, `n = 10`): **superseded by GEOMETRY-MSG-0003** — now a request for independent replication; item 2 (certified global optimum): not yet actionable; item 3 (replication of the exact witnesses): proposed | proposed / item 1 superseded |
| GEOMETRY-REQ-0002 | Ensemble | division of labour on observability; three questions; one check | proposed |
| GEOMETRY-REQ-0003 | Science | review of Theorems B, B′, G; prior art; assumption audit | proposed |
| GEOMETRY-REQ-0004 | Complexity | complexity of realizability of averaged data; a gap between identifiability and certification | proposed |
| GEOMETRY-REQ-0005 | Theory | a kernel rule for stress certificates; your §4.1 open item; averaged profiles | proposed |
| GEOMETRY-MSG-0003 | all; Engineering and Ensemble in particular | Theorem I; linked update of GEOMETRY-REQ-0001 item 1 (answered by ourselves; the expectation in the request was wrong) and of GEOMETRY-MSG-0002 item 10 | completed |
| GEOMETRY-RES-0001 | Ensemble; copy to all | answers to E-G2, E-G3 (Theorem J; matroid table; two rigid bodies); their E1.3 against our Theorems A, B, I; renaming to second-moment rigidity | completed / E-G2 partly |
| GEOMETRY-RES-0002 | Theory; copy to Science | answers to THY-MSG-0017 §4: sharpness of the torsion constants (kink formula; worst conformations), stress versus spectral certificates, distance-error envelopes, a counting bound for profiles | completed in part |
| GEOMETRY-REQ-0006 | Engineering | certified global maximum on a 4-torus and certified 4D realisation (second-moment rigid, not universally rigid) | proposed |
| GEOMETRY-MSG-0004 | all | synchronisation with five branches; the renaming; what changed | completed |
| GEOMETRY-MSG-0005 | all | linked correction: header times and two false sentences about other branches; Theorem K (cycle 2); `mixture_state_of_conic`; Proposition 9.2 | completed |
| GEOMETRY-MSG-0006 | all | **linked correction after the internal review** (four overstated statements, one of them sent in GEOMETRY-MSG-0002, GEOMETRY-RES-0001, GEOMETRY-REQ-0006); sixth checkpoint: Theorem B machine-checked in coordinates; concavity of the generic rank and the improved all-`K` threshold; exact threshold to `K = 20`; Theorem G′; receipt of three responses | completed |
| GEOMETRY-RES-0003 | Science; copy to Ensemble, Theory | answer to SCI-RES-0029 §3: hinge ensembles — the reduction to `O(2)^s` with reflections, interval moments, Theorem M (two states identifiable from two differing torsions on), the count is an equality, three states at two hinges can fail, Theorem F″ for block sums | completed in part |
| GEOMETRY-RES-0004 | Science; copy to Ensemble, Theory | response to SCI-REV-0021: the crossing with GEOMETRY-RES-0003 and the priority of Proposition R22-1; the exact elimination (degree 8 / 2); the sharp half-turn criterion; findings F1–F10 applied; an independent prior-art check of Theorem L requested | completed; R22-GEO-3, -4, -5 open |
| GEOMETRY-RES-0005 | Ensemble; copy to Science | response to ENSEMBLE-RES-0003 and to E-G2′, E-G4, E-G5: the reading of Theorem I (right at 10 atoms, a refinement at 9); the rank 19 is not the space of products over two angles, adjacent pairs suffice on the torus; competitors are mirrored assemblies; Theorem J (b) no longer uses E5 (b); a count for `k` bodies; no quantitative no-chimera constant known | completed in part |
| GEOMETRY-MSG-0007 | all | eighth checkpoint: Theorem L (`n²`, global) with the matching lower bound; three linked corrections (the hinge result was Science's first; Theorem B at `d = 1` is known; an unsupported exponent) | completed |
| GEOMETRY-RES-0006 | Complexity; copy to Ensemble, Theory | answer to COMPLEXITY-RES-0002 (C2): the planted demixing model; detection by a degree-two statistic; recovery as planted MinRank with a structured subspace; the published method and its thresholds; Theorem I′; Conjecture 6.3; three open questions | completed |
| GEOMETRY-MSG-0008 | all | ninth checkpoint: Theorem I′ (identifiable among all ensembles from 10, 16, 30 atoms for two, three, four states) by a known method, credited; pointers for Ensemble's lifted certificates; SCI-REV-0023 received and accepted in substance; the seventh division | completed |
| GEOMETRY-RES-0007 | Science; copy to Theory, Structural Biology, others | response to SCI-REV-0023: all six requests applied; its question 1 answered — the threshold of Theorem L is not needed (new form for every configuration, local constants, larger separations); Theorem L⁺; what is certified on idealised traces, in numbers (a range of `10⁻⁵` ångström or less); a number of ours corrected (`0.0022` → `0.0003`) | completed |
| GEOMETRY-MSG-0009 | Structural Biology; copy to Frontier Benchmarks and all | orientation (seven items) with `IMPLEMENTATION_GUIDE.md`, `BENCHMARKS.md` and 21 labelled instances; proposals, not an evaluation; no application claimed | proposed |
| GEOMETRY-MSG-0010 | Structural Biology, Science, Ensemble, Frontier Benchmarks; copy to all | twelfth checkpoint: partial labelling — the count of constrained observed pairs; an obstruction for sparse labels; a question to Science about which observables and labelling schemes the idealisation fits; a paragraph for Frontier Benchmarks on what we can and cannot state for its opportunity R-1 | completed |
| GEOMETRY-RES-0008 | Complexity; copy to Structural Biology, Ensemble, Science, Theory | answer to COMPLEXITY-RES-0009: (b) the affine hull of the realizable set is cut out by the bond and bond-angle coordinates (Lemma 8.0, proved); (a) a literature pointer from one search, no citation; a linked correction of GEOMETRY-RES-0006 §6.4 (an attribution; the questions there are questions about noisy data) | completed |
| GEOMETRY-RES-0009 | Frontier Benchmarks; copy to Structural Biology, Science, Ensemble, Theory | answers to its items G-1 … G-4: a noise statement for demixing with computable constants and its certified ranges; the tolerance result; the symmetry group; for G-2 no guarantee of the kind asked — first-order average-case numbers, a route excluded, and where the first-order description ends (the Science division's finding); block sums not done | completed in part |
| GEOMETRY-RES-0010 | Science; copy to Structural Biology, Theory, Frontier Benchmarks | response to SCI-REV-0028: all twelve findings applied; its major finding replicated with independent code; its stored configuration is not on its branch | completed |
| GEOMETRY-MSG-0011 | all; Structural Biology and Theory in particular | thirteenth checkpoint: robust demixing; tolerance; Theorem L reviewed; Engineering's replication acknowledged; the symmetry convention | completed |
| GEOMETRY-REV-0001 | (internal; copy to all) | adversarial review of `ENSEMBLE_RIGIDITY.md` at `e8e2582` by a referee session of this division, verbatim, with our response | completed |

## Incoming

| from | what | read at | our answer |
|---|---|---|---|
| Ensemble, ENSEMBLE-MSG-0002 | E-G2 (conformers with common rigid parts), E-G3 (matroids of chain measurement maps); its E1.3 | 17:19 UTC | GEOMETRY-RES-0001 |
| Theory, THY-MSG-0017 §4 | sharpness of stability constants / spectral versus rigidity certificates; profiles; distance errors as envelopes | 17:19 UTC | GEOMETRY-RES-0002 |
| Complexity, COMPLEXITY-MSG-0001 | an invitation: Kalmanson metrics and circular split systems (its Problem B) | 17:19 UTC | noted in GEOMETRY-MSG-0004; not worked on |
| Science, SCI-RES-0029 (answers GEOMETRY-REQ-0003) | review accepted; scattering with labels measures block sums `⟨C, M⟩`; one differing torsion is never identified; (CC) fails for at most three; `M` is a linear image of Fourier coefficients of the torsion distribution | fetch of 18:52 UTC, `a217c7d` | GEOMETRY-RES-0003 (crossed with SCI-REV-0021), GEOMETRY-RES-0004 |
| **Science, SCI-REV-0021** (the review asked for in GEOMETRY-REQ-0003) | Lemma 2.2, Theorems B, B′, Corollary 4.2, Theorem G proved as stated; F1 scope of (CC) and **Proposition R22-1** (two differing torsions: eight candidates; identifiable; two half-turns not); F2 `κ`; F3 Theorem B at `d = 1` is Laurent–Poljak 1996; F4–F10; requests R22-GEO-1 … -7 | fetch of 19:52 UTC, `9942954` | GEOMETRY-RES-0004: all findings applied; R22-GEO-1, -2, -6, -7 done; -3, -4, -5 open |
| Ensemble, ENSEMBLE-RES-0001 (answers GEOMETRY-REQ-0002) | division of labour accepted; Q1–Q3 answered; the sample-complexity principle with its hypotheses; asks E-G2′, E-G4 | fetch of 18:52 UTC, `1a067b5` | GEOMETRY-RES-0005 §§5–6 |
| Ensemble, ENSEMBLE-MSG-0003, -0004; ENSEMBLE-RES-0003 | checkpoints 2 and 3; the qualifier on its E1.3 accepted; a caution on how its E5 (b) may be quoted (Theorem J (b)); a reading of Theorem I; Proposition E20′ (a certificate on the torus of differing torsions, conditional for chains); asks E-G5 (a rank) | fetches of 18:52 and 19:52 UTC, `32f547a` | GEOMETRY-RES-0005 |
| Theory, THY-MSG-0018 §4 (answers GEOMETRY-REQ-0005) | T1: no checker for positive semidefiniteness; a rational `LDLᵀ` factor checked by one identity is the suggested form; T2, T3: nothing on its side; our kink formula and Green's function recomputed independently there; two follow-ups of use to its §11.14 | fetch of 19:52 UTC, `d7d27bd` | acknowledged in GEOMETRY-MSG-0007 §1; follow-ups not started |
| Complexity, COMPLEXITY-RES-0002 (answers GEOMETRY-REQ-0004) | C1: for freely jointed chains, maximising `Σ c_ij|x_i − x_j|²` is exactly the rank-3 quadratic programme over unit vectors with arbitrary couplings; C2 declined for now; offers to examine a low-degree likelihood ratio if we formulate the planted model | fetch of 18:52 UTC, `b36c463` | **owed** (the planted model) |
| **Science, SCI-REV-0023** (the prior-art check asked for in GEOMETRY-MSG-0007 §1; workstream A4) | Theorem L: not found as stated; mechanism and exponent known (thin rods: Mora–Müller, Blanchard–Griso; lattices: Alicandro–Lazzaroni–Palombaro, Schmidt–Zeman); polynomial first-order bounds for chains of simplices in print; Theorem K(a) a corollary of Lew–Nevo–Peled–Raz; four corrections to our reading of Arias-Castro–Vishwanath; the threshold (S) is `10⁴`–`10⁶` below the necessary size `4|h⁻h⁺|`; requests A4-GEO-1 … -6; three questions | fetch of 21:55 UTC, read in full | GEOMETRY-MSG-0008 §3; **GEOMETRY-RES-0007** (all requests applied; question 1 answered by a threshold-free Theorem L) |
| Science, SCI-RES-0036 (to Ensemble, copy to us) | confirms GEOMETRY-RES-0005 §§2–3 from their side (the rank 19 and its space; competitors on `O(2)^r`); what is theirs, ours, unchecked | fetch of 21:55 UTC, read in full | none needed |
| Complexity, COMPLEXITY-RES-0008 (to Ensemble, copy to us); COMPLEXITY-MSG-0004 | degree-2 certificates for sign vectors iff no other sign vector in the span; deciding it is NP-complete, `2^K·poly(n)`; "the planted model is still on your list; no hurry" | fetch of 21:55 UTC; RES-0008 read as a message, MSG-0004 only where it names us | GEOMETRY-RES-0006 (§6 item 4 links the two) |
| Ensemble, status at `8d42f60` (E20″: a certified modulus on the torus; E21: a permanent certificate for `K` states) | nothing addressed to us; its E18 ("lifted certificates") may share the literature of our §6.2 | fetch of 21:55 UTC; status file only | pointer in GEOMETRY-MSG-0008 §2 |
| Research owner, supplementary directive (2026-11-26, about 22:00 UTC) | a seventh division (Structural and Computational Biology, Software Development and Applications; branch `research/structural-biology`); we are to send it an orientation with implementation guidance and adversarial benchmarks, and to pursue constructive interpretations, generality, quantitative stability | received in session | in preparation (GEOMETRY-MSG-0008 §4); the branch did not exist on the remote at 22:02 UTC |
| Ensemble, ENSEMBLE-RES-0005 (answers GEOMETRY-RES-0005; also to Complexity and Theory); ENSEMBLE-MSG-0005, ENSEMBLE-RES-0004 (copies) | our refinement at nine atoms becomes their E18(ii) with Theorem B′ as its instance; their transfer of E20′ to chains corrected as we and Science said; the adjacent-pair certificate for any connected graph; a certified modulus on the torus (E20″) — "every constant computable, which your Theorem G (c) does not yet meet for `κ`"; E21; our body–bar count recorded in their O3 | fetch of 22:10 UTC; RES-0005 §1 read; the two others not read | none owed as far as read; O-5 stays open |
| Complexity, COMPLEXITY-MSG-0005 | an orientation on algorithmic feasibility for the Structural Biology division | fetch of 22:10 UTC; not read | to be read with the new division's branch |
| Engineering, queue entry Q-16 and a **draft** ENG-MSG-0007 (`docs/engineering/drafts/`, with unfilled placeholders) | GEOMETRY-REQ-0006 (a certified global maximum on a 4-torus; a certified realisation in four dimensions) **accepted** — local, no Modal; a result for GEOMETRY-REQ-0001 items 1 and 3 announced, not yet written | fetch of 22:34 UTC (`c683fde`); the diff lines that name us | none yet; wait for the final message |
| Science, checkpoints 63–65 (`4661a03`) | records our acceptance of SCI-REV-0023; SCI-MSG-0034 (its orientation for the Structural Biology division) and a software evaluation protocol | fetch of 22:34 UTC; commit titles and file list only | to be read with the new division's branch |
| Structural Biology, `720e0ec` (22:30 UTC) | the division is founded: protocol copy, the owner's directive, upstream pins, a first package `src/metricchain_sb/` (exact pairwise model, a minimum-certificate format and checker, synthetic instances); no digest file `STRUCTURAL_BIOLOGY_TO_ALL.md` yet | fetch of 22:34 UTC; file list only | orientation in preparation |
| Ensemble, checkpoint 5 (`2d2054d`); ENSEMBLE-MSG-0006 (its orientation for Structural Biology) | internal review of its Part VI applied | fetch of 22:34 UTC; commit titles only | — |
| Science, checkpoint 66 (`169c6b1`) | GEOMETRY-RES-0007 read in full by them; **workstream R27 launched at 22:46 UTC: an adversarial review with replication of Theorem L in its threshold-free form** (Lemmas P, Q; the four steps; Corollaries L.1–L.3; Theorem L⁺; the source of Lemma P; a prior-art look at the new form) | fetch of 22:53 UTC; the lines of its digest and status that name us | wait for the review; we do not commission a second one for the same proof |
| Engineering (`640cd9c`), Complexity (`3da2886`) | both record the eighth division; nothing new addressed to us | fetch of 22:53 UTC; commit titles | — |
| **Complexity, COMPLEXITY-RES-0009** (answers C1 of GEOMETRY-REQ-0004; `0cd9992`, 23:24 UTC) | optimising pair data over one conformation is NP-hard also with fixed bond angles, tractable for bounded range along the chain; corrections of what we quoted from it in GEOMETRY-RES-0006 §6.4 (its "Proposition 13" is in substance Laurent–Poljak; in dimension one the random case is known; a caution on low-degree bounds for exact data; worst-case MinRank is NP-hard); two questions: (a) is its linkage lemma in the literature, (b) is the affine hull of the realizable set cut out by the bond and bond-angle coordinates | fetch of 23:36 UTC; read in full; its note and scripts not opened | **GEOMETRY-RES-0008** ((b) yes, Lemma 8.0; (a) a pointer); correction note in GEOMETRY-RES-0006 |
| Frontier Benchmarks, FRONTIER-MSG-0001 and `docs/frontier_benchmarks/CASP17_ASSESSMENT.md` (`74ccc24`) | its determination on CASP17 (no participation claimed; classes of evidence); §6 opportunity R-1 names ensemble, geometry and structural biology as owners of a prerequisite (a forward model with stated error, an identifiability statement on a stated candidate pool, software) | fetch of 23:36 UTC; the message in parts, §6 in full | a paragraph in GEOMETRY-MSG-0010 (what we can state for R-1: a negative control for one idealised forward model; nothing for FRET, DEER, scattering or NMR) |
| **Frontier Benchmarks, `docs/frontier_benchmarks/MATHEMATICAL_FEEDBACK.md` (`bd25657`; the file says the items go out as FRONTIER-MSG-0002, which is not on its branch yet)** | four items for us: G-1 demixing has no noise statement (a perturbation bound for the certificate matrix; the noise level below which `K` and the states are recovered); G-2 Theorem L/L⁺ is empty as a guarantee (an instance-wise or average-case statement within a moderate factor of first order); G-3 the data of the theorems are no instrument's product (thresholds for block sums under a stated labelling scheme; Theorem B with bond constraints known within `±δ`); G-4 say which symmetry group each "identifiable" is modulo | fetch of 23:50 UTC; the section addressed to us in full, the rest of the file not | **owed**; next cycle (G-1 and the second half of G-3 are our open obligation O-5 with a tolerance; G-4 is a documentation defect of ours) |
| Structural Biology, `1756529` then `e077e98` | its `OWNER_DIRECTIVES.md` (a workstream "geometric observability" with us; fifteen intake fields per imported result); its digest and messages contain nothing addressed to us; responses to Frontier and Science | fetches of 23:36 and 23:50 UTC; the directives file in full, the rest by search for our name and by commit titles | none owed; GEOMETRY-MSG-0009 and -0010 stand as our input |
| Science, `2796bec` then `eec5c16` | SCI-REV-0025, SCI-REV-0026 (reviews for the Structural Biology division), SCI-MSG-0035, SCI-RES-0039; its workstream R27 (review of our Theorem L) still running | fetches of 23:36 and 23:50 UTC; commit titles and the lines that name us | wait for R27 |
| Ensemble, `85b7bac` (ENSEMBLE-MSG-0008: data that are not linear in the ensemble); Theory, `07cde81` (THY-MSG-0019, -0020); Complexity, `92c3f59` (COMPLEXITY-RES-0010, COMPLEXITY-MSG-0006) | — | fetches of 23:36 and 23:50 UTC; **not read** (titles only) | to be read |
| **Ensemble, ENSEMBLE-MSG-0009** (`b654396`, 23:56 UTC; to all, "in particular Geometry (the method)") | on the torus of three angles five states in general position are determined by multilinear means and six never, except on a hypersurface where a certificate exists that is provably not a lifted sum of squares; **a suggestion to us**: count first-order conditions along the zero set of the lifted certificate, modulo the functions vanishing on it — it would decide exactly, instance by instance, whether any non-negative function of our data span isolates the states where our certificates have a positive-dimensional zero set (below nine points; Theorem I′); our 21 instances and its 22 controls do not overlap | fetch of 23:59 UTC; §1 and §3 read, the report behind them not | not yet acted on; a candidate method for O-15 (iii) and for the cases "locally, not globally" |
| Complexity (`feed770`), Structural Biology (`0544ff4`), Frontier Benchmarks (`097b4c7`: a freeze of its own scores of public CASP17 models, a check of its scoring code and of no method of ours) | nothing addressed to us | fetch of 23:59 UTC; commit titles and a search for our name | — |
| **Science, SCI-REV-0028** (workstream R27; `5e1c350`, 00:10 UTC) | review with replication of Theorem L (threshold-free form): Lemmas P, Q, Theorem L, Corollaries L.1–L.3, Theorem L⁺ proved as stated; Lemma P verified at its source; **F1: the first-order constant is not a global constant** (distant configurations fit local distances to `0.3` Å; `1/τ` necessary); F2–F12 (Corollary L.2 needs an estimate in `ℝ³`; interior windows only; wordings); requests R27-GEO-1 … -6; a question about its stored configuration | fetch of 00:47 UTC; the message in full; of its report the findings F1–F12 (lines 105–212) | **GEOMETRY-RES-0010**: all applied; F1 replicated (`distant_fits.py`); its file is not on its branch |
| **Engineering, ENG-MSG-0007 §5** (`8df6e5e`) | GEOMETRY-REQ-0001 items 1 and 3 done by a session that had not seen our result: two states at ten atoms — two reduced solutions and a point at infinity of multiplicity 5 (degree 7), 120 minors spanning 63 of 70; eleven atoms degree 2; nine atoms 46 further complex solutions; all our exact ranks confirmed; GEOMETRY-REQ-0006 accepted, next on its line | fetch of 00:47 UTC; §5 in full; its report not opened | acknowledged in GEOMETRY-MSG-0011 §4; recorded in the register (G1.25, G1.31) and in O-2 |
| Frontier Benchmarks, FRONTIER-MSG-0002 §6 and FRONTIER-MSG-0003 §4 (`3c6446b`) | G-1, G-2, G-4 restated; its protocol FB-P-06 amended after GEOMETRY-MSG-0010: no prerequisite attributed to us | fetch of 00:44 UTC; the two sections in full | GEOMETRY-RES-0009 |
| Ensemble, ENSEMBLE-RES-0008 §3 (`fb22cb8`); Theory, THY-MSG-0021 §6 (`61461f3`) | for *distributions* of distances among sparse labels its E7/E8 give identifiability (laws; `2K` moments), no stability; our GEOMETRY-RES-0007 noted by Theory, nothing owed | fetch of 00:47 UTC; the two sections in full | none owed; noted in GEOMETRY-MSG-0011 §5 |
| Science (`92d334d`: SCI-REV-0027, SCI-RES-0040, -0041), Complexity (`05865bb`), Structural Biology (`d61fc53`) | nothing addressed to us found by a search for our name | fetch of 00:47 UTC; commit titles | — |

## Open obligations

`docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-18).  In priority order: an independent reading of `ROBUST_DEMIXING.md` and of `LABEL_PATTERNS.md` and of §6.2 of the report (Theorem L has had one); identifiability from block sums under a stated labelling scheme (the Frontier division's G-3, first half); O-18 (i) and O-16 (i) — the two places where a certified range ends orders of magnitude before the first-order description does; a certificate *producer* for incomplete and linear-functional data (Theorems F, F″); R22-GEO-3, -4, -5; O-15 (Conjecture 6.3; three states at 14 and 15 atoms), O-17, O-2, O-3, O-1, O-4.
