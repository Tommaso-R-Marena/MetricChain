# State-of-the-art evidence register

*Frontier Benchmarking division.  Version 1, 2026-11-26.  This file is the curated register:
per area, which methods independent evidence places first, which exact versions would serve
as baselines for MetricChain-relevant comparisons, and under what conditions a comparison is
fair.  The full per-method records (problem, version, dates, evidence, availability,
reproducibility, compute, assumptions, limitations, evaluation setting, fairness) are the
method tables of the four literature assessments in `literature/`, each row with a read
level.*

**How to read this register.**  *IND* = independent evidence (blind community assessment or
third-party benchmark).  *SELF* = reported by the method's developers.  Read levels, carried
from the assessments: **FT** full text, **AB** abstract or landing page, **OP** official page
or repository, **SN** search snippet, **MEM** from memory — the last two are leads, not
findings.  The coordinator read all four assessments in full and verified independently only
the items marked **[C]** (checked by us, with how).  No developer claim is recorded as fact.
The newest release is nowhere assumed to be the strongest.

## A. Fixed-sequence structure prediction and its assessment

*Detail: `literature/LIT_structure_prediction.md`.  Relevance to MetricChain: context and
contamination facts only — MetricChain has no structure predictor (`CASP17_ASSESSMENT.md`).*

| category | what independent evidence says (source, read level) | strongest reproducible baselines, versions |
|---|---|---|
| single proteins | CASP16 assessors: single-domain folds "nearly solved"; the three top monomer groups from one laboratory; progress since CASP15 "subtle"; model ranking remains weak (IND, AB) | AlphaFold 2 via ColabFold (the CASP baseline); AlphaFold 3 v3.0.1 (code Apache-2.0, weights under separate terms; training cut-off 2021-09-30, FT via CAMEO paper) |
| protein complexes | "remains an unsolved challenge": leading groups predicted slightly more than half of targets to high accuracy; with massive sampling of AlphaFold 2 the advantage of AlphaFold 3 disappears (IND, AB) | AlphaFold-Multimer v2.3 with massive sampling (MassiveFold); AlphaFold 3 |
| antibody and immune complexes | CASP16: a docking-based group led and stayed ahead of AlphaFold 3 run with 1,000 seeds — on **8** targets, "cannot firmly conclude a breakthrough" (IND, FT).  Every 2026 claim of beating AlphaFold 3 here is SELF | none to be named until CASP17 (more than 40 immune-complex targets) reports |
| protein–ligand pose | CASP16 pharma targets: AlphaFold 3 as automated baseline, mean lDDT-PLI 0.80, above the best participant (0.69) (IND, AB); prospective weekly evaluation finds drug-like success near 40 %, falling with distance from the training set (IND, FT).  Affinity prediction: best Kendall τ 0.42 (IND, AB) | out of our evaluation scope beyond retrospective description |
| nucleic acids | "generally poor"; top groups human experts; no gain once templates are accounted for; deep learning "not superior to traditional approaches" (IND, AB) | — |
| accuracy estimation | per-atom confidence from AlphaFold 3-derived features best for local accuracy (IND, AB) | — |

**CASP17 [C]** (read by us on the official site, 2026-11-26): results not public; announced
for 2026-11-29; conference 1–5 December.  Invited predictor talks listed in the programme are
an indirect signal and are *not* recorded here as a ranking.  **Obligation:** this section is
revised when the official assessment is published; until then no CASP17 ranking appears in
any file of this division.

**Fair comparison of any future fixed-sequence predictor** requires: targets released after
the cut-off of every model compared (several open models now have June 2025 cut-offs, which
leaves essentially CASP17-era targets); whole-complex homology filtering (a 2026 preprint
reports that one model's lead over another "narrows or disappears" under it, AB);
budget-matched sampling; stoichiometry handled identically.

## B. Ensembles, disorder, thermodynamics, kinetics

*Detail: `literature/LIT_ensembles_thermo_kinetics.md`.  Relevance: the ensemble and geometry
divisions' identifiability mathematics (protocols FB-P-04, -05, -06).*

| sub-area | what independent evidence says | consequence for our protocols |
|---|---|---|
| discrete alternative states | CASP16: accuracy well below single-state; best approaches = many AlphaFold 2 runs with enhanced alignments, then selection; success mostly needed a template (IND, AB).  A 2026 benchmark reports the best of eight tools fully recovering 8.2 % of experimentally observed ensembles (AB).  Fold-switch "successes" largely memorisation (IND, SN) | PDB alternative states show that states exist, not their populations |
| ensembles against solution data | CASP16 domain–linker–domain targets: **no** submission fit the combined RDC and SAXS data; none reproduced the wild-type/Gly6 difference (IND, AB).  No independent evidence that any learned generator reproduces solution observables better than physics-based simulation | the open problem to which FB-P-06 would speak; CASP17 has seven such targets |
| learned equilibrium emulators | the one head-to-head found (2026 preprint, SN): three tools give clearly different distributions and cannot be ranked without ground truth.  The successor model's own card says sampling frequency is **not** a calibrated Boltzmann probability or free energy (OP) | emulators are baselines for *diversity*, not for thermodynamics |
| reweighting against data (maximum entropy, Bayesian, minimal ensembles, maximum occurrence) | evidence is case studies by developers; results depend on the prior, the forward model and a regularisation strength (MEM for most rows) | **the baselines of FB-P-04**; none has been run in the programme |
| disorder | CAID3: top methods use protein language models, but a cheap structure-derived baseline ranks third within 0.005 AUC of the best on one test set (IND, FT) | a reminder to always report the cheap baseline |
| stability (ΔΔG of fixed variants) | independent studies: predictions compressed toward zero, stabilising variants poorly predicted, scores inflated on unbalanced sets; no independent homology-split comparison found for the newest predictors | measured ΔG values are reference data for fixed sequences only; never an optimisation target |
| kinetics | no independent blind assessment of computed rates found; prefactors unknown, so only relative rates are testable | science's verdict "not as physical rates" stands |
| physical consistency of simulations | exact statistical tests exist (kinetic-energy distribution, equipartition, ensemble tests between state points: the `physical_validation` package, SN); for learned potentials "low force error does not imply stable dynamics" (IND, SN) | a conformance suite for any future simulation layer |

## C. Certified optimisation, counting with guarantees, and side-chain packing

*Detail: `literature/LIT_certified_optimization_packing.md` — the area closest to
MetricChain's kernels (protocols FB-P-01, -02, -03).*

| method | version, date (read level) | guarantee | evidence | fair comparison with a certificate kernel |
|---|---|---|---|---|
| **toulbar2** | 1.4.0, 2026-08-27; `pytoulbar2` 1.4.0.3 (OP).  **[C]** installed here from PyPI; solved the smallest public fixed-sequence instance in 0.13 s | optimality *claimed*; **no proof or certificate output found** (search-based; not proof of absence) | most instances solved of seven solver configurations on 3,026 graphical-model instances at one hour (developers among the authors; FT) | the mandatory uncertified baseline: same integer tables, default and published settings, time-to-optimum and time-to-certificate reported separately |
| exact-rational dual of the linear relaxation | — | checkable by exact arithmetic | prior work: relaxation integral on most fixed-sequence instances (≈ 340 of 370 in one set; SN/AB).  **[C]** our pilot: `RESULTS.md` §1 | the cheapest certificate; any native format must be compared with it on instances closed without branching |
| pseudo-Boolean encoding + proof-logging solver + **VeriPB + CakePB** | 2025 competition certified tracks (FT) | proof checked by a **formally verified** checker | independent competition data: checking up to 2,387× solving time; 53 proofs timed out; "not all answers could be checked".  A 2025–26 MaxSAT study: median solving overhead 23 %, median checking 23× solving, 237 of 350 proofs checked in 10 h (FT-S) | the certified state of the art; compare total time, proof size, fraction checked within budget, and trusted base |
| Lean-side importers | PBLean (2026, AB): VeriPB proofs into Lean 4 by reflection; CPOG (SN): model-counting proofs with a checker verified in Lean 4 | — | — | the standard a "machine-checked kernel" claim is measured against |
| exact MIP with certificates | SCIP 10 + VIPR (SN) | rational certificates; presolve not certified | overhead "does not exceed the time needed for solving" (SELF, SN) | secondary baseline |
| OSPREY 3 (DEE/A\*, K\*) | version not verified (SN) | "provable with respect to the input model"; floating point not discussed; no external certificate | SELF only | rigid-rotamer mode only, fixed sequence only |
| partition functions | deterministic ε-approximation of the toulbar2 lineage (FT); K\*; exact weighted model counters; weighted mini-bucket bounds; dynamic importance sampling | from ratio guarantees proved for exact arithmetic to probabilistic bounds | — | FB-P-03: state which *kind* of guarantee each gives |

**Side-chain packing** (one independent benchmark, 2025, FT): on experimental backbones the
learned packers lead the rotamer-library methods (recovery of all χ angles within 20°:
about 59–66 % against 55–58 % on one CASP set); on AlphaFold-predicted backbones the
predictor's own side chains are as good or better and repacking gives no significant gain.
Declared training cut-offs of the learned packers reach 2023-07-28 (FT, SELF).  A competitor
reports that one packer leaks ground-truth side-chain geometry (SELF by a competitor, FT).
Recovery definitions differ between papers: numbers cannot be compared without
recomputation.

**Does exactness matter for accuracy?**  Published evidence says barely: the global optimum of
a standard energy function improved χ1+χ2 accuracy by less than 0.1 % over annealing, while
changing the energy function gained about six points (SN — a lead we have not read in full;
it is the stated null expectation of FB-P-02, not a premise).

**Not found by the assessor** (absence of evidence): proof logging for cost-function-network
solving; any interval-certified computation of rotamer-pair energy tables — the same gap as
the programme's assumption A9.

## D. Geometry, inverse problems, electrostatics, cavities

*Detail: `literature/LIT_geometry_electrostatics_cavities.md`.  Read levels in this area are
weak (two papers read in part; most rows SN or MEM): everything here is a lead to be
confirmed at the source before it supports a protocol.*

* **Reconstruction from distances.**  Benchmark practice is planted: coordinates from the PDB,
  exact or artificially widened distances; no community instance repository found.  Branch-
  and-Prune and SDP codes are the comparators (FB-P-07).
* **NMR inverse problems.**  Blind rounds ended in 2013; the references are themselves NMR
  models.  The archive-wide restraint validation of the wwPDB is the usable public resource.
* **Averaged observables and identifiability.**  Documented non-uniqueness: orientation
  degeneracies from a single alignment medium; few Shannon channels in a scattering curve,
  with hydration parameters fitted; prior-dependence of reweighting; about 5 Å accuracy of
  single-molecule FRET distances (multi-laboratory blind studies, SN).
* **Electrostatics.**  No certified error bounds for Poisson–Boltzmann solvers found — only
  a-posteriori estimates; the Born and Kirkwood spheres are the analytic test cases.  For pKa,
  an independent 2023 benchmark found no fast predictor beating the water-pKa null model with
  confidence (SN); newer learned predictors report gains on random residue-level splits (SELF).
* **Binding sites (descriptive use only).**  One independent benchmark with aggregated
  observed sites: a geometric detector rescored by a simple learned ranker led several deep
  networks (FT, partial).  Affinity benchmarks are documented to be driven by train–test
  leakage (SN).

## E. Reference implementations our own instruments are checked against

| tool | version found (read level) | note |
|---|---|---|
| OpenStructure (lDDT, lDDT-PLI, QS-score) | 2.12, 2026-08-17 (OP) | scores change between minor versions; record the version per result |
| US-align / TM-score | single-file source, update log to 2026-05-27; an input-order bug for oligomers fixed 2026-03-28 (OP) | pin by date and checksum |
| DockQ | 2.1.3 (OP) | — |
| LGA (GDT) | not verified | the CASP reference implementation |
| MolProbity, PoseBusters 0.6.5 | versions partly unverified | physical-plausibility checks; validity can be gamed by post-hoc relaxation |
| **[C]** installed here for cross-checks | `biotite` 2.0.0, `biopython` 1.88, `gemmi` 0.7.5, `tmtools` 0.3.0 | used only as independent second implementations |

## F. What this register does not know

* Every CASP17 outcome.
* Whether proof logging for cost-function networks exists unpublished or in a repository the
  assessor could not reach (GitHub pages were partly blocked for one assessor).
* Exact versions and licences of several tools (marked "not verified" in the assessments).
* Anything about methods whose only evidence is a developer preprint: they are listed, not
  ranked.

## G. Standing obligations

1. After 2026-11-29: read the official CASP17 results and, when published, the assessors'
   papers; revise §A and §B.
2. Before any protocol is frozen: re-verify at the source every baseline version it names.
3. Rows marked SN or MEM in the assessments are confirmed at the source or removed before
   they support a conclusion.
