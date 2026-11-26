# Benchmark master plan of the Structural & Computational Biology division

*Version 1, 2026-11-26.  Written before any held-out result exists.  This division designs
benchmarks and runs unit tests, smoke tests and development-scale experiments on its own
machine; independent review, replication and every substantial run belong to the engineering
division (its procedure BM-7, steps S0–S6, on `research/ubuntu-engineering`); the design and
integrity of frozen evaluations belong to the frontier-benchmarking division; physical
relevance and fairness are reviewed by the science division (its template
`TEMPLATE_BENCHMARK_REQUEST.md`).  Nothing in this file authorises spending.*

## 0. Rules that hold for every benchmark

1. **Kinds of evidence are never mixed.**  *Exploratory* (throwaway scripts; never quoted),
   *development* (structures and instances seen while the software was written; quoted only as
   development evidence), *validation* (fixed in advance, run by us, may be looked at),
   *held-out* (fixed and hashed by another division before the first run; one scored run per
   instance and configuration), *adversarial* (built to break a claim), *replication* (another
   division's re-run).  Every result row carries its kind.
2. **Development set (closed list).**  PDB entries `1CRN, 5PTI, 1BPI, 1PGA, 2IGD, 1UBQ` (tables
   and certificates) and `1L2Y` (geometry unit tests).  Any structure not on this list is
   held out for us.  We do not choose the held-out set: we propose a selection *rule* (§3,
   SB-BM-3) and the engineering or frontier division fixes and hashes the list.
3. **The model is frozen before a held-out run**: code commit, model parameters
   (`MODEL_PARAMS` and `SCALE_BITS` of `experiments/structbio/gmec_dev/run.py`), rotamer rule.
   A change of any of them after a held-out result has been seen starts a new model with a new
   name, and the old results stay.
4. **Four-line error budget with every certified number** (the science division's request
   S-3): (i) certified width — model-relative; (ii) discretisation — zero only because the
   claim is about the discrete model, and said so; (iii) uncertainty of the energy model in the
   same units, with its source; (iv) evaluation and rounding tolerance of the tables.
5. **A certified method that is uninformative where an uncertified one is accurate has not
   won** (science, `BENCHMARK_DESIGN.md` §0.4).  Abstentions and vacuous intervals are counted
   and reported as outcomes.
6. **Costs are complete**: table construction, certificate production, certificate checking
   and baseline solving are reported separately and summed; nothing is precomputed off the
   books.
7. **Stop rule common to all**: one unsound acceptance (an accepted certificate whose bound
   exceeds the energy of an exhibited configuration, or an accepted interval that misses an
   exactly known value) stops the benchmark; it is reported at once and kept as a record.

## 1. Levels

| level | content | status |
|---|---|---|
| 0 | checker conformance: exact agreement with enumeration; agreement of our checker with the theory division's reference checker on valid and mutated certificates; malformed and out-of-range inputs rejected | done locally for `min` certificates (`tests/structbio/test_mincert.py`); to be repeated independently (SB-BM-1) |
| 1 | small synthetic instances with enumerated ground truth | done locally (24 random instances, zero gap); SB-BM-2 |
| 2 | protein-like synthetic models (`synthetic.random_contact_model`), ground truth by an exact solver | specified (SB-BM-2); local run pending |
| 3 | public structures, development split | done locally for `min` certificates (SB-X-001: six structures, all zero gap); model link validated against OpenMM (SB-BM-4) |
| 4 | public structures, held-out split, nonredundant | specified (SB-BM-3); **requested from engineering**, not run by us |
| 5 | retrospective comparison with experimental observations | design only (SB-BM-6); not justified yet for populations; side-chain placement is a test of the *energy model*, stated as such |

A level is entered only when the one before it has a recorded result (the engineering
division's rule for its stages A–F is the same).

## 2. Baselines (details and licences: `BASELINE_REGISTER.md`)

| task | baseline | role | same instance? |
|---|---|---|---|
| GMEC | toulbar2 1.4.0.3 (`pytoulbar2`, MIT) on the identical integer instance | speed baseline without certificate; independent oracle for the optimum | yes, exactly |
| GMEC with a checkable proof | pseudo-Boolean proof logging (VeriPB, formally verified checker CakePB) on an encoding of the identical instance; exact SCIP with VIPR certificates | the incumbent *certified* route (science SCI-REV-0006 §7; our `PRIOR_ART.md` B): the comparison that decides whether a native certificate is worth having | yes, after encoding; **not installed by us — proposed to engineering** |
| ln Z | exact variable elimination where feasible; toulbar2 `Z*ε` at matched width; anytime AND/OR or mini-bucket bounds | for capability C2, when it exists | yes |
| marginals | exact junction tree where feasible; belief propagation (label [H]) | for capability C2 | yes |
| side-chain placement (context only) | FASPR, SCWRL4, Rosetta packer | different energy models: never a same-instance comparison; context for SB-BM-6 only | no |

Comparisons we will not make: a certified optimum against a structure-prediction confidence
score; certificate cost against a heuristic packer's runtime as if the two delivered the same
thing; any comparison across different energy tables presented as a comparison of solvers.

## 3. Benchmarks

Each entry has the twenty fields of the founding directive (§11), numbered.

### SB-BM-1 — conformance of the `min` certificate checker (level 0; adversarial)

1. *Question.*  Does `metricchain_sb.mincheck` accept exactly the certificates that the theory
   division's kernel `verify` accepts, and never a false bound?
2. *Claim.*  Acceptance implies `L ≤ E(x)` on the box (`verify_sound`, [V]); our checker
   implements `verify` for leaf/branch/prune nodes with one stored orientation per pair
   (`verify_sound_real_symm`, [V]).  The implementation is tested, not verified.
3. *Implementation.*  `src/metricchain_sb/mincheck.py`, `mincert.py` (format, converter).
4. *Commits.*  Ours: the commit named in STRUCTBIO-REQ-0001; theory: `b2caab6` (reference checker).
5. *Population.*  Random instances `n ≤ 6`, `k ≤ 4` (generator `synthetic.random_pair_model`,
   seeds 0–23, extendable); certificates from our producer and random mutations of them
   (bound, message, missing child, prune indices, site); independent instances and
   certificates written by the engineering division from the specification.
6. *Inclusion/exclusion.*  None; every generated case is scored.
7. *Baselines.*  Exhaustive enumeration (ground truth); the theory division's
   `experiments/reference_checker.py`; the engineering division's `leafcert` checkers where the
   formats overlap (full product domains, no prune).
8. *Environment.*  Any machine; Python ≥ 3.11, numpy.
9. *Accuracy.*  Exact: integer arithmetic only.
10. *Metrics.*  Number of disagreements between checkers; number of accepted certificates whose
    bound exceeds the enumerated minimum.
11. *Statistics.*  Counts; a zero count over `N` cases is reported with the exact 95 % upper
    limit `3/N` on the rate, not as a proof.
12. *Seeds.*  2026 (mutations), 0–23 (instances), plus the replicator's own.
13. *Success.*  Zero disagreements and zero unsound acceptances over at least `10⁴` mutated
    certificates; every malformed input rejected without an exception.
14. *Failure.*  One unsound acceptance, or one disagreement that is not explained by the
    documented difference of formats (states outside a site's own state set are malformed for
    us and expressible in the padded reference format).
15. *Resources.*  Minutes of one core.
16. *Stopping.*  Rule 0.7.
17. *Artifacts.*  Counts, the disagreeing files if any, the commit.
18. *Limitations.*  Tiny instances; the `sum` rule of the kernel is not implemented by us and
    not exercised; agreement of two tested checkers is not a proof of either.
19. *Bias.*  The mutation generator was written by the author of the checker.
20. *Interpretation.*  Evidence for the implementation; the mathematical guarantee is the
    theory division's theorem and is not strengthened by any count.

### SB-BM-2 — certified GMEC on synthetic instances (levels 1–2; validation)

1. *Question.*  How do certificate production time, check time and size grow with the number
   of sites, the domain sizes and the density of strong couplings, against an exact solver
   without certificate?
2. *Claim.*  None beyond soundness; scaling is an observation ([E]).
3. *Implementation.*  `gmec.certify_gmec` (dead-end elimination, MPLP dual bound, branch and bound).
4. *Commits.*  As SB-BM-1.
5. *Population.*  `random_contact_model(seed, n, kmax)` for `n ∈ {15, 25, 40, 60, 100, 150}`,
   `kmax ∈ {6, 12, 24}`, seeds 0–9; `random_pair_model` dense frustrated instances
   `n ∈ {10, 15, 20}`, `kmax = 4` (the adversarial end: no structure to exploit).
6. *Inclusion/exclusion.*  All generated instances; an abstention (budget exceeded) is an outcome.
7. *Baselines.*  toulbar2 on the identical instance; enumeration where `∏k_i ≤ 10⁷`.
8. *Environment.*  One core per instance; wall-clock and peak memory recorded.
9. *Accuracy.*  Zero gap (`eps = 0`) and `eps = 10⁻³` units.
10. *Metrics.*  Fraction certified within the budget; times (produce, check, toulbar2); nodes;
    certificate bytes; agreement of optima.
11. *Statistics.*  Medians and interquartile ranges over seeds; five repetitions for timings.
12. *Seeds.*  0–9 per cell.
13. *Success (hypotheses written now).*  H2a: every accepted certificate agrees with toulbar2.
    H2b: on contact models up to `n = 60`, `kmax = 12` at least 90 % are certified within
    600 s.  H2c: on dense frustrated instances the producer is expected to be much slower than
    toulbar2 (its bound is the plain local-polytope dual): we predict abstentions from `n = 20`.
14. *Failure.*  Disagreement of optima on an accepted certificate (unsound, rule 0.7).
15. *Resources.*  About `180 × 2 × 600 s` worst case = 60 core-hours; expected far less.
16. *Stopping.*  Per-instance time limit 600 s; rule 0.7.
17. *Artifacts.*  One JSONL row per instance and accuracy; certificates with sha256.
18. *Limitations.*  Synthetic couplings are not an energy function.
19. *Bias.*  The generator was designed by us to resemble what we expect of proteins.
20. *Interpretation.*  Cost model of the producer; no statement about proteins.

### SB-BM-3 — certified GMEC on public structures (levels 3–4; development done, held-out requested)

1. *Question.*  For the fixed-backbone rotamer model of `metricchain_sb.molecular` on
   experimentally determined structures, how often is the exact GMEC certified, at what total
   cost, and how does a native certificate compare with (a) an exact solver without proof and
   (b) pseudo-Boolean proof logging on the same instance?
2. *Claim.*  For each instance: `min_x E(x) = E(x*)` for the published integer tables
   (certificate + witness).  Model-conditional ([M]); not a statement about the force field's
   real-valued energy beyond the rounding statement of SB-BM-4, and not about the protein.
3. *Implementation.*  `molecular.build_energy_tables` → `PairModel.from_float(scale_bits=20)` →
   `gmec.certify_gmec(eps=0)` → `mincheck.check_min_certificate`; driver
   `experiments/structbio/gmec_dev/run.py`.
4. *Commits.*  As SB-BM-1.
5. *Population.*  Development: the six structures of rule 0.2.  Held-out (proposed rule, to be
   executed by another division): X-ray entries of the wwPDB with resolution ≤ 1.5 Å, exactly
   one protein chain of 40–200 residues in the asymmetric unit, deposited coordinates for
   every heavy atom of that chain (our preparation fails closed otherwise), no non-standard
   residue in the chain; one representative per 30 % sequence-identity cluster (the wwPDB's
   own clusters), clusters of the development structures excluded; ordered by the SHA-256 of
   the entry identifier; the first 100 that pass preparation.
6. *Inclusion/exclusion.*  Preparation failures are counted and listed with their reason; no
   structure is dropped after its result is known.
7. *Baselines.*  toulbar2 (identical instance); VeriPB/CakePB and exact SCIP+VIPR (proposed).
8. *Environment.*  One core, 16 GB; OpenMM 8.6.1 Reference platform for preparation.
9. *Accuracy.*  Zero gap.
10. *Metrics.*  Certified fraction; seconds for tables, certificate, check, baseline; nodes;
    certificate bytes; proof bytes and proof-check seconds of the proof-logging route.
11. *Statistics.*  Exact binomial (Clopper–Pearson) 95 % interval for the certified fraction;
    medians and interquartile ranges; ratios per instance.
12. *Seeds.*  Model seed 0 (hydrogen placement); solver seeds as recorded.
13. *Success (hypotheses written now, after the development results and before any held-out
    run).*  H3a: every accepted certificate agrees with toulbar2.  H3b: zero-gap certificates
    for at least 90 % of prepared held-out structures within 3 600 s each.  H3c: checking costs
    at most 25 % of production (development: 3 to 13 %; the first version of this plan said
    10 %, which the development rows already exceeded — corrected before any held-out run).  H3d: production takes between 1 and 100 times the toulbar2
    solve time (development: 7 to 25 times; toulbar2 is faster on every development
    structure).  H3e (direction unknown): native certificate size and check time against
    proof logging — we have no evidence either way.
14. *Failure.*  H3a violated (unsound; stop).  H3b below 50 % would mean the plain dual bound
    is not adequate beyond small proteins.
15. *Resources.*  Per structure: tables 1–60 s, certificate up to 3 600 s (development: 0.3–23 s).
    100 structures: under 20 core-hours expected, 100 core-hours worst case.  No Modal needed
    by our estimate; the decision is the engineering division's.
16. *Stopping.*  Per-instance limits; rule 0.7.
17. *Artifacts.*  `results.jsonl` rows (schema of SB-X-001), detached certificates with sha256,
    instance checksums, the hashed held-out list.
18. *Limitations.*  One energy model (ff14SB torsions and Lennard-Jones, Coulomb with
    `ε = 4r`, in vacuo), one rotamer rule, rigid backbone, clipped clashes, hydrogens placed by
    OpenMM with a fixed seed; instances are reproduced bit for bit on one machine only (not
    yet tested across machines).
19. *Bias.*  Structures that fail preparation (missing atoms, alternate chains) are
    systematically absent; small proteins are over-represented.
20. *Interpretation.*  "Certified GMEC of this model" — whether that conformation resembles
    the deposited one is SB-BM-6 and is a property of the model.

### SB-BM-4 — the link between tables and energy function (level 3; validation)

Question: do the pairwise tables reproduce an independently built full-system energy of the
same model?  Method and result: `intake/MOLECULAR_LAYER_REPORT.md` §3 — for six structures,
21 random and 21 low-energy configurations each, differences from the all-native
configuration agree with an independent OpenMM system to `≤ 3.6·10⁻¹¹` kcal/mol on low-energy
configurations and `≤ 4.6·10⁻¹³` relative on random ones; a wrong dielectric constant or
missing 1–4 terms is detected (1.95 and 4.79 kcal/mol).  Label [N]: numerical agreement in
double precision, not an enclosure.  What is *not* established: a rigorous bound on the
floating-point evaluation error of a table entry; the published model is therefore defined
as the rounded tables themselves (rounding to `2⁻²⁰` kcal/mol, at most `4.8·10⁻⁷` kcal/mol per
entry away from the float table).  Requested of the engineering division: an independent
re-implementation of the table construction from §1 of that report.

### SB-BM-5 — certified partition functions, free energies and populations (levels 0–3; design)

Not yet a benchmark: the capability (C2) is under construction.  Fixed in advance: ground
truth by enumeration with exact rationals for `∏k_i ≤ 10⁶`; every certified interval must
contain it (rule 0.7); the interval width in nats and the abstention rate are the primary
metrics; baselines of §2.  First exploratory measurement, recorded so that it cannot be
forgotten (`RESULTS.md` R-3): on ubiquitin under the vacuum model, after thermal pruning, the
best elimination order we found (min-fill) for the graph of pairs whose non-additive part
exceeds 1 kcal/mol has width 10 and a largest table of about `10¹³` entries, and the weaker
pairs carry about 113 nats of worst-case first-order uncertainty — exact elimination with
first-order relaxation, as we can run it, certifies nothing useful there.

### SB-BM-6 — side-chain placement against deposited conformations (level 5; design only)

A test of the *energy model and rotamer rule*, not of the certificate: with the native state
excluded from the rotamer set (`include_native=False`), compare the certified GMEC with the
deposited side-chain conformation (χ1 and χ1+2 within 40°, buried and exposed residues
separately) on held-out structures.  The certificate contributes one thing: any disagreement
is attributable to the model, none to the search.  We expect this vacuum model to place side
chains worse than specialised packers (on ubiquitin its GMEC differs from the native state
at 37 of 65 sites and lies 139 kcal/mol below it in model energy); that expectation is
written here before any held-out run.  Category under the engineering division's freeze
rules: retrospective (the deposited structure contains the answer; the native state is hidden
from the algorithm, not from us).

## 4. What is requested of whom

| request | to | content |
|---|---|---|
| STRUCTBIO-REQ-0001 | engineering | BM-7 intake of our first release; SB-BM-1 independently; fix and hash the held-out list of SB-BM-3 and run it; proof-logging baseline |
| STRUCTBIO-REQ-0002 | science | adversarial review of the claims of capability C1 and of this plan; fairness of baselines; the model definition |
| STRUCTBIO-MSG-0002 | frontier | maturity statement, specifications, development/held-out separation |
