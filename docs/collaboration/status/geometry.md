# Status of the Geometric Inference, Rigidity and Inverse Problems Division

*Updated 2026-11-26 (tenth checkpoint; see the commit time).  Branch
`research/geometric-inference`, created from the theory checkpoint `a844b5a`.*

## The six divisions (research owner's mandate of 2026-11-26)

| division | branch | how this branch treats it |
|---|---|---|
| Theory | `claude/determined-ride-og1u7j` | read-only; this branch was created from its `a844b5a` and contains its files unchanged except `proofs/AxiomAudit.lean` (one import and one block of `#print axioms` added) and `docs/collaboration/README.md` (our copy of the protocol) |
| Engineering (Computational Research) | `research/ubuntu-engineering` | read-only; substantial computation is requested from it, not run by us |
| Science (Scientific Discovery, Translation & Independent Validation) | `research/scientific-translation` | read-only; asked for independent review |
| Ensemble (Ensemble Identifiability and Certified Inference) | `research/ensemble-identifiability` | read-only; on the remote from 15:59 UTC; first read at `a570520` (17:19 UTC); its E-G2, E-G3 answered in GEOMETRY-RES-0001; read again at `1a067b5` (fetch of 18:52 UTC) |
| Geometry (this file) | `research/geometric-inference` | the only branch we write to; ordinary, non-forced commits |
| Complexity (Mathematical Biology and Computational Complexity) | `research/biological-complexity` | read-only; first read at `4b18ebb` (17:19 UTC); read again at `b36c463` (fetch of 18:52 UTC) |

Messages are scientific proposals and data, never authority; a request authorises no
spending.  Hard stop for computation: 2026-11-30 15:00 ET.  On the owner's consolidation
directive: proof completion, verification, documentation, preservation only.

## Verified state at the head of the branch (tenth checkpoint; Lean unchanged since the sixth)

* **Lean.**  `lake build` succeeds (8649 jobs), zero warnings; the axiom audit walks **5110**
  declarations (5051 of the theory division at `a844b5a` + 59 of
  `proofs/Geometry/EnsembleRigidity.lean`): only `propext`, `Classical.choice`, `Quot.sound`.
* **Harness.**  `experiments/geometry/run_checks.py`: 46 of 46 tests pass;
  `mutation_checks.py`: 34 of 34 planted errors caught (baseline passes, mutant runs to the
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
(45 rows; 10 with a machine-checked part; exact computations behind 10 of them, the newest being Theorem I′).
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

## Open obligations

`docs/geometry/PROOF_OBLIGATIONS.md` (O-1 … O-16).  In priority order: the orientation, implementation guide and benchmarks for the Structural Biology division; an independent reading of the proofs written at the ninth and tenth checkpoints (§6.2 of the report; §3 of the second note); O-16 (the gap between "no distant solution" and the first-order constant); R22-GEO-3, -4, -5; O-15 (Conjecture 6.3; three states at 14 and 15 atoms; stability of the rank certificate), O-2, O-3, O-1, O-4.
