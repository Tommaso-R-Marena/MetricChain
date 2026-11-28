# Phase II — final report of the Theoretical Research Division

*Branch `research/phase2-foundations` (from the consolidation checkpoint `b3c5d61`; the original branch
`claude/determined-ride-og1u7j` and the archive `research/consolidated-archive` were not modified).
Written 2026-11-28 under the research owner's directive "MetricChain Phase II — Foundational Mathematics
and General Information Complexity".  Everything here was produced by AI sessions; reviews are by AI
sessions.  **No human has read any of it.***

**Resources.**  The directive sets a ceiling on expenditure "subject to available usage monitoring".
**This session cannot monitor its actual expenditure.**  The work was therefore kept bounded by
construction: one research session; two referee subagents (one run each: the review of the report, and
a short review of the one theorem that was strengthened afterwards); one web-fetch of an
abstract page; five web-search queries; no external or Modal computation; background computations only
on the session's own machine (the audit, exact verification runs).  No request was sent to another
division for computation.

---

## 1. What was asked, and what was done

| objective of the directive | outcome | where |
|---|---|---|
| 1. Prove or refute S1 and S2 | **Both are correct.**  S1 = Theorem A (explicit constants; adaptive statistical queries); S2 = Theorem B (arbitrary exact observables through their joint Walsh spectrum; the bound on the subgroup is tight up to a factor 2) | `PHASE2_REPORT.md` §§2, 3, 9 |
| 2. Formalise their essential cores in Lean | `proofs/Frontiers/ObservationInvariance.lean`, 41 declarations: packing bounds with a tolerant oracle, the admissible cone, mixtures and translations, the flat mixture, characters, the counting form of the union bound, parities on the cube, Hoeffding and Chebyshev for independent draws, two cores of the new upper bounds, maxima of random translates (no bias on average; 1-Lipschitz in each argument) | §10 of the report; theory report §9 (index row) |
| 3. Stronger results in the exponentially precise regime | adaptive exponent at tolerance `e^{−γn}`: at least `h̄(2γ)`, `h̄(λ) = KL(ρ₀ − λ/u‖½) − λ`, for every `γ < a/2` (S1's argument gives `h − 2γ`, positive for `γ < h/2` only; at `u = 1` the two thresholds are `0.0555` and `0.0146`), and at most `(1 − γ/ln 2)h`; a spectral criterion (attenuated bias) that unifies the constructions.  **The gap is open**; for `γ ≥ a/2` there is no lower bound for randomised algorithms.  The lower bound in this generality was found on the last day: the first version needed `γ < 0.0154` (at `u = 1`), an artefact of bounding overlaps by Markov's inequality — the bias of a maximum of random dips averages to zero exactly, and the bounded-differences inequality does the rest | Theorem A′, Corollary C, §5, Lemma 5.1 |
| 4. Exact non-Walsh observables, non-uniform references, transitive spaces, richer oracles | exact observables by spectrum (Theorem B); one exact point probability trivialises the problem (the archive's); any vertex-transitive space (Theorem A″; Theorem A′ too, by a remark added last, which the second referee read once and checked on four graphs); product references: a positive but smaller exponent (flat mixture: 49 % and 22 % of the class exponent in two cases); any known `κ`-Lipschitz energy: a sandwich `h(u − κ) ≤ … ≤ h(u + κ)` (Proposition 2.7); partition laws (Theorem C); all observables (Proposition C′); samples (Theorem E) | §§2.4, 2.5, 3, 4, 6 |
| 5. Sharp characterisations for experimentally motivated operators | sharp: means with error bars in the sub-exponential regime (nothing); the law of a block of `θn` sites (exactly `(1 − θ)h`); all observables (a bounded number of evaluations; deterministic `τ·2ⁿ`); a histogram with polynomially many bins and constant error bars (nothing).  Two-sided with a gap: exponential precision; exact marginals of linear order; samples | §§4, 7, 8 |
| 6. A deeper relation between precision, structure, concentration and computation | partial: (i) an observation oracle with `M` observables at tolerance `τ` cannot tell a continuum of hidden perturbations from `τ^{−2} ln M` random ones; (ii) dividing a perturbation's mass by `L` shrinks its volume by `L^{ℓ}`, `ℓ` the Chernoff parameter, so atoms cost `L^{1−ℓ}`; (iii) thermal noise attenuates a test of order `j` by `tanh(u/2)^j`, and one quantity — the attenuated bias of the set of hidden centres — decides hiding (Lemma 5.1); (iv) `A = E_π[w1_T]/μ(T)`: a measured mass is a reduction of the problem to a set.  No single law was found; the open problem of row 3 is where one would be | §§5.1, 7 |
| 7. Dependent or physically structured systems | Proposition 2.7 (absorption): every lower bound at the slope `u − κ`, every algorithm at `u + κ`, for any known energy with single-site oscillation `κ < u` — interacting or not; not sharp.  Marginalisation with a dependent reference keeps the class with the constant `u + κ` (THY-MSG-0023) | §2.5 |
| 8. Resolve the R29 findings | F2 applied; F3–F6 had been applied before the halt; F7 unchanged (labelled numerical); F1 resolved — and in doing so **a defect of our own independent checker was found**: see §4 below | `R29_RESOLUTION.md` |
| 9. Strengthen the formal verification of the algorithmic upper bounds | one step: Chebyshev's inequality for the mean of independent draws on a product measure (`chebyshev_iid_mean`) — the probabilistic core of plain Monte Carlo (Theorem 11.44); and the two elementary cores of the new upper bounds.  The bound on the relative variance over the class and the nested adaptive algorithm remain paper proofs | Lean file, Part 7 |
| 10. A self-contained manuscript | `docs/phase2/MANUSCRIPT.md` (generated by `scripts/build_phase2_manuscript.py` from the report, so the two cannot drift): abstract, introduction with related work, preliminaries with a proof of the packing lemma, the theorems with proofs, open problems, appendices on what is machine-checked and what is not claimed | `MANUSCRIPT.md` |

## 2. Complete proofs (paper), and their status

All statements are for the cube class of the programme (`u`-Lipschitz log-weights on `{0,1}ⁿ`, target
`ln A`, `(ε/2, δ)`-correct randomised algorithms) unless stated; `h`, `a` are the adaptive and non-adaptive
exponents; `L = ⌈2τ^{−2} ln(4M/η)⌉`.

| statement | content | status |
|---|---|---|
| Theorem A | means of `M` arbitrary bounded observables, each to an adversarial tolerance `τ`: `E|Q| ≥ (1−η)(1−2δ)·2ⁿ/(L·|B|)` for both lower bounds; with `q` adaptive statistical queries `(1 − η − 2δ)`; exponents unchanged if `ln(1/τ) = o(n)` and `ln ln M = o(n)` | [P], refereed (correct; one constant repaired); cores [V] |
| Theorem A′, Corollary A′ | maxima of `L` narrow dips with `R = L m_r ≥ 2(e^ε − 1)` and `2 R m_r ln(2M/η) ≤ τ²` (`δ ≤ ½`): `E|Q| ≥ (1−2δ)(1−η−η″)·2ⁿ/(L·V(n, r−1))`, `η″ = L·V(n, r−1)/2ⁿ`; exponent `h̄(2γ + β)` for every `2γ + β < a` | [P], with the bounded-differences inequality cited; the mean-zero identity [V]; strengthened after the first review and refereed separately (correct for `δ ≤ ½`; the corner `δ > ½` and a sharper constant are the second referee's) |
| Theorem A″, Corollary A″ | flat mixture for any reference and any kernel with constant row sums; tilted baselines | [P], refereed (theorem correct; product weights and two numerical claims of ours were wrong and are corrected); identity [V] |
| Proposition 2.7, Corollary 2.7 | absorption sandwich for a known `κ`-Lipschitz energy | [P], read by the referee (correct as stated) |
| Theorem B, B′, Corollary B′ | exact observables by joint spectrum, `|C| < 2(M+1)`; refined exponent `h̄(ln M/n)`; marginals of order `αn`: `h̄(h₂(α)) ≤ θ(α) ≤ (1 − α)h` | [P], refereed (correct as stated); cores [V] |
| Theorem C, Corollary C | the law of a block of `θn` sites: exponents exactly `(1 − θ)h`, `(1 − θ)a`; neither hypothesis of Theorem A can be dropped | [P], refereed (correct; `2b` halving queries); rests on the cube upper bounds of Phase I ([P], refereed internally) |
| Proposition C′ | all observables: `O(ln(1/δ)/ln(κ/τ))` evaluations; one exact point probability: one evaluation (the archive's); deterministic: `τ·2ⁿ` up to polynomial factors | [P], refereed (correct) |
| Lemma 5.1 | attenuated bias | [P], read by the referee (correct as stated) |
| Theorem E | `m = e^{νn}` samples: `E|Q| ≥ exp(n[h̄(ν) − ν] − o(n))` for `ν < ν*`, `h̄(ν*) = 2ν*` (`ν* = 0.4024·h` at `u = 1`) | [P], refereed (correct as stated; the coupling re-derived in full; simulated only far from the asymptotic regime) |

## 3. Verification status

| what | result | where |
|---|---|---|
| the audit, `bash scripts/audit_all.sh` | **AUDIT PASSED**, 2026-11-28 04:20 UTC, on the code of commit `ddae0c3` (afterwards only documents, stored outputs and the second referee's files changed; the check of document references was repeated on the final tree): 93 Lean files, 50 211 lines; no `sorry`, `admit`, native evaluation or anonymous `example`; 5128 declarations depend on `propext`, `Classical.choice`, `Quot.sound` only; 721 headline theorems; benchmarks and reference checker pass; every Lean name cited in the documents exists | `scripts/audit_all.sh` |
| the harness, full pass | 196 tests: 166 survive, 30 documented refutations — all as expected | `docs/falsification_output.txt` |
| mutation tests | 645 mutations: 644 caught, 1 expected pass; 161 baseline runs | `docs/mutation_output.txt` |
| Phase II Lean file | `proofs/Frontiers/ObservationInvariance.lean`: 41 declarations, compiles without warnings, registered in the axiom audit | `proofs/AxiomAudit.lean` |
| Phase II exact checks | 37 checks pass; harness block XXVIII: four tests, 27 mutations, all caught | `experiments/phase2/out_p2_checks.txt` |
| manuscript | generated from the report; the generator's consistency check passes | `scripts/build_phase2_manuscript.py --check` |

(At the halt of Phase I: 92 Lean files, 5068 declarations, 696 headline theorems, 192 tests, 618 mutations.)

**The internal review** (`PHASE2_REVIEW.md`, 587 lines; scripts under `experiments/phase2/review/`): one
adversarial AI referee re-derived every proof of the first version and replicated numerically with its
own code.  Verdict: every numbered theorem stands.  It found **two wrong numerical claims of ours** about
the flat family with a field — first "three quarters of the exponent" had been committed (a wrong count,
which we had found ourselves), then "void at the exponential scale" (an extrapolation from `n ≤ 160`) with
inverted weights for tilted baselines; the truth is in between — and seven smaller points (a constant, a
proviso, a range of accuracies, a count of queries, an attribution, wording).  All applied; `DEAD_ENDS.md`
D71 records the two errors.  The referee did not compile the Lean file or run the harness.

**After the review.**  Theorem A′ / Corollary A′ were strengthened (the side condition of the first
version removed; see §1, row 3).  The first referee did not see the new proof.
**The second review** (`PHASE2_REVIEW_A1.md`, 213 lines; scripts `experiments/phase2/review/a1_*`): a second
adversarial AI referee read that section alone.  Verdict: the new theorem (both oracle forms), its lemma and
its corollary stand; every step re-derived; the removal of the side condition is legitimate.  It found one
error in a degenerate corner of the *statement* — for `δ > ½` and `η + η″ > 1` the displayed product of two
negative factors is a false positive bound (an explicit counterexample on a cube of four sites; the first
version had the same corner) — repaired by the hypothesis `δ ≤ ½`; five points of wording; and a sharper
constant (`2` for `8`).  Replication with its own code: exact enumeration over all tuples of centres in 118
configurations; Monte Carlo at 16–20 sites where the overlaps are 0.7 to 12.6 times the least admissible
tolerance (the regime the first version could not treat): no violation of the hidden-answer event in
14 500 instances; the recipe of the corollary up to `n = 2·10⁶`.  All incorporated; the referee then read
the corrected section and the remark on homogeneous spaces once ("correct as they stand"; the remark
checked by enumeration on the Petersen graph, a Johnson scheme, a ternary Hamming space and a cycle, with a
path and a star as negative controls) and made four more points of wording, also applied.  The text after
those last edits was not read again.
Neither referee checked McDiarmid's inequality itself (cited), and the argument for adaptive statistical
queries is on paper only.

## 4. R29 — and a defect found in our own verification chain

The science division's review SCI-REV-0030 said, in its major finding, that the last line of
`z6_certified_tops.py` is not evidence, and that evidence is an independent exact checker.  Acting on it:

* **The mutation study** (`experiments/workstreams/Z/z6_pipeline_mutations.py`):
<!-- FINAL:MUTATIONS -->
  on a small instance (`u = 1`, four levels, 40 sample points) the unmutated script is accepted; of ten
  gross mutations that break the certificate, **nine still end with the script's own "ALL CHECKS PASS"**
  (the tenth trips an assertion) and **the independent checker rejects all ten**; of six mutations that
  only remove a safety margin it rejects two and accepts four — and an accepted output is a valid
  certificate (the checker exhibits a proved pair for every line).  Ten mutations on one instance do not
  show that the checker rejects every invalid output.
<!-- /FINAL:MUTATIONS -->
* **The 400-level run** (`K = 4000`; the source of the certified exponent at `k = 400` and of the constants
  quoted by the engineering division), which two referees had left unchecked: **our independent checker
  did not verify it as it stood.**  Its test for the cap line failed at many levels.  The cause is in the
  checker, not in the certificate: the checker chooses the sample points of its own comparison lines
  assuming that the cap becomes active at a vertex of the hull of the other lines; when it becomes active
  inside the last linear piece — as it does at this resolution — the choice degenerates to 300
  log-spaced points and the comparison fails although the checker's own line through the failing vertex
  lies above the cap.  `verify_z6_chunk.py` adds a refinement loop to that test (the same acceptance
  criterion, the same source of lines).
<!-- FINAL:J400 -->
  A second limitation appeared behind the first: for the lowest line of a level the checker's
  floating-point ranking of candidate parents is noise, and at five levels the true parent was not among
  the six it tries; the wrapper tries sixty.  **With these changes (in memory; the referee's file is
  unchanged; the acceptance criteria are the checker's) the run is verified in full** (finished
  2026-11-28 05:29 UTC): 400 of 400 levels, 1 841 962 stored lines — 1 841 868 with a proved rational pair,
  the 94 cap lines by exact domination — no failure, and the regenerated tops equal to the committed
  output at every level.  The stopped attempts with the unmodified checker are archived as evidence
  (`experiments/workstreams/Z/verify_z6_K4000_history/`).  Not established: the wrapper's changes have had
  no second reader (`R29_RESOLUTION.md` §4.2 lists what else is not).
<!-- /FINAL:J400 -->

## 5. Novelty evidence

* **Inside the programme** (report §9): S2's corollary — exact marginals of order `o(n)` change no exponent
  — is the science division's (Theorem 4, addenda A1, A8), as is the fact that one exact point
  probability trivialises the problem (A8) and the invariance under Walsh correlations of every order at
  tolerance `e^{−o(n/ln n)}` (A10).  New here: arbitrary bounded observables with the count `M` and both
  exponents (Theorem A); the narrow-dip exponent and the two-sided bounds in the crossover that A10 left
  open; the formulation by spectrum and the tightness of the subgroup bound; the sharp exponent for a
  block (the lower bound); that neither hypothesis can be dropped; the full-oracle collapse and its
  deterministic counterpart; the sample lower bound; the flat mixture and the absorption sandwich.
* **Outside** (`PRIOR_ART.md`): five generic queries and one abstract, read at the level of search
  summaries.  Not found: a statistical-query or observation oracle added to evaluations for normalising
  constants; the statements of Theorems A, C, E.  Found and to be cited: hidden-cell lower bounds for
  log-concave normalising constants (Ge–Lee–Lu 2020); partition functions from sampling oracles at chosen
  temperatures, with an adaptive/non-adaptive distinction (Kolmogorov 2018; Harris–Kolmogorov; Guo et al.
  2026); sample complexity with a proposal (Block–Shetty 2026).
* **Assessment.**  Every ingredient is classical (translation averaging, Hoeffding, random linear codes,
  the birthday bound).  The statements were not found; a specialist may regard them as exercises.  "Not
  found" is not "new".

## 6. Unfinished obligations

1. **No human review** of anything in Phase II or before.
2. **Machine-checking stops at the cores.**  Not machine-checked: the assembly of the cores into the
   displayed bounds (product measure on `L`-tuples, counting of balls), the argument for adaptive
   statistical queries, everything about maxima of dips beyond admissibility (Theorems A′, B′, E), Theorem
   C, Lemma 5.1, Proposition 2.7, all asymptotics, and every upper bound of Phase I except the
   probabilistic core of plain Monte Carlo.
3. **Theorem E** was simulated only at `m = 2` on cubes of 13–15 sites (by the referee); its regime
   `m = e^{νn}` is paper only.
4. **R29:** parts (b)–(d) of Theorem 11.58e have had no reader outside this division; "strictly better
   from the third level on" remains a floating-point statement (an interval proof is within reach and not
   done); the referee's own unfinished items were not run by us.
5. **The independent checker** `a6_02_verify_z6_output.py` is unchanged in the repository; its cap test
   and its search for the parent of a line have the limitations of §4 at `K = 4000`, worked around only in
   the wrapper `verify_z6_chunk.py`.  The wrapper has had no second reader.
6. **Collaboration.**  One message was sent (THY-MSG-0023: results, the R29 resolution, answers to the
   three questions of ENG-MSG-0009 §4); no answer had arrived at the last fetch (2026-11-28 02:20 UTC:
   `research/phase2-certified-inference` unchanged at `bf7b71a`; `research/phase2-adaptive-hierarchy` not
   on the remote).  The engineering note `CERTIFIED_INFERENCE.md` was not read — our answers address its
   questions as its message states them.  The messages of other divisions left unread at the halt of
   27 November (listed in the status file) are still unread.
7. The original texts of S1 and S2 were not available; what was verified is their rendering in the
   directive.

## 7. The most consequential remaining opportunities

1. **The exponent at exponential precision** — between `h̄(2γ)` (slope `−1.02` at `u = 1`, zero from
   `γ = a/2 = 0.0555` on) and `(1 − γ/ln 2)h` (slope `−0.042`, positive up to `γ = ln 2`).  Equivalent forms: the least number of points of a set with attenuated
   bias `τ`; whether an algorithm can turn a detectable bias of the hidden centres into their
   localisation.  This is where a law relating precision, noise and computation would be, if there is one.
2. **Samples.**  Lower bound `ν* ≈ 0.40·h`; no algorithm below `e^{nh}` is known.  An algorithm that learns
   a tractable model of the ensemble from samples and bridges to it would be new mathematics and is the
   setting closest to practice (free energies from simulation data).
3. **Invariance with a field or an interacting known part.**  The flat family gives 22–49 % of the class
   exponent in the cases computed; absorption gives a sandwich.  The compensation mechanism of the
   science division is sharp for one-body data; whether it extends to arbitrary observables is open.
4. **An external human reading** of the Phase I theorem and of this manuscript — still the action with
   the largest expected value for the programme (consolidation report, E1).

## 8. State at the stop

<!-- FINAL:STATE -->
*(completed in the final commit)*
<!-- /FINAL:STATE -->
