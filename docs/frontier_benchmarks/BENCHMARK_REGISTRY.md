# Benchmark registry

*Frontier Benchmarking division.  Version 1, 2026-11-26.  One row per benchmark, reference
dataset or community assessment that could bear on the charter, grouped by the thirteen areas
of the founding directive.  Details, metrics, licences and read levels are in the benchmark
tables of the four assessments in `literature/`; this file is the consolidated register with
our verdict on each.  No single benchmark evaluates all properties; structure prediction,
folding kinetics, thermodynamic accuracy, functional prediction and experimental validation
are different questions with different benchmarks.*

**Columns.**  *Truth*: **X** exact or planted by construction; **E** experimental, with the
stated quality; **M** a model of experiment (a deposited model, a force-field trajectory);
**A** curated annotation.  *Charter*: **in** / **desc** (descriptive, retrospective use only)
/ **out**.  *Bears on*: capability numbers C1–C10 of `RESEARCH_INTAKE.md` §2, or "context".
*Verdict*: **use now** (a protocol exists and prerequisites are met) · **gated** (protocol
named, prerequisite missing) · **context** (informs the state of the art; no MetricChain
capability to evaluate) · **excluded**.  Read level of the underlying row: (FT) (AB) (OP)
(SN) (MEM); **[C]** = checked directly by the coordinator.

## 1. Fixed-sequence structure prediction and characterisation

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-101 | CASP17 (2026): targets, all predictions, results from 2026-11-29 **[C]** | E (unreleased structures; 19 of 239 already in the PDB) | prospective and blind *for its participants*; for anyone else every prediction has been public since August | in | context; R-1, R-2 of `CASP17_ASSESSMENT.md` | context now; **gated** retrospectives |
| B-102 | CASP16 (2024) and its published assessment (AB/FT) | E | blind when run; public now | in | context | context |
| B-103 | CAMEO weekly evaluation (FT) | E (PDB pre-release) | prospective by construction | in | context | context |
| B-104 | post-cut-off static sets for co-folding (PoseBusters, Runs N' Poses, FoldBench, PLINDER splits) (SN/OP) | E | each is valid only for models with earlier training cut-offs; "quickly getting incorporated into training" | desc | context | context |
| B-105 | high-resolution PDB entries released after all baselines' cut-offs — side-chain placement on given backbones (to be built; rule in FB-P-02) | E (≤ 1.5 Å) | controlled by the release-date rule | in | C1 through a molecular layer | **gated** (FB-P-02) |
| B-106 | CASP13–15 native-backbone packing sets (FT) | E | target counts and recovery definitions differ between papers; learned packers filtered differently | in | C1 | development only |

## 2. Conformational ensembles and structural heterogeneity

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-201 | CASP17 ensemble targets assessed against NMR, SAXS/DEER, FRET data **[C]** (list) | E, low-resolution; underdetermines the ensemble | blind for participants; data release pending | in | C5, C6 | **gated** (FB-P-06) |
| B-202 | CASP16 multi-state and domain–linker–domain targets (AB) | E | public | in | context for C5 | context |
| B-203 | planted-truth identification controls of the ensemble division (18 instances; cube families to n = 22) | **X** | none | in | C5 | **use now** (FB-P-04) |
| B-204 | planted K-state chain mixtures for demixing | **X** | none | in | C6 | **use now** (FB-P-05) |
| B-205 | synthetic forward-model tests: known ensemble → simulated averaged data with known noise → recover weights (SN) | **X** | none | in | C5 | **use now** as an extension of FB-P-04 once a forward model is written |
| B-206 | molecular-dynamics reference sets (ATLAS, mdCATH, long trajectories) (SN/AB/MEM) | **M** — the force field's ensemble, of finite length | widely used as training data | in | context | context |
| B-207 | PDB-derived multi-state sets (apo/holo, fold switchers, a 2026 ensemble database) (AB/SN) | E for existence of states, not populations | very high (memorisation documented) | in | context | context |
| B-208 | Protein Ensemble Database depositions (AB) | **M** (one ensemble among many fitting the data) | — | in | C5 only through the raw data | context |
| B-209 | synthetic cryo-EM heterogeneity sets with known volumes (SN) | **X** (simulated images) | none; sim-to-real gap | in | geometry's orbit-recovery idealisation | context until a method exists |

## 3. Intrinsically disordered proteins and regions

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-301 | CAID3 residue-level disorder and binding (FT) | A (literature curation, incomplete) | temporal hold-out | in | none | context |
| B-302 | solution-scattering and NMR data on disordered chains (repositories; MEM) | E, underdetermining | parameters of coarse-grained models were fitted to the same kinds of data | in | C5 | **gated** (forward model) |

## 4. Thermodynamics and statistical mechanics

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-401 | exactly solvable models: chains by transfer matrix, enumerable rotamer models, lattice chains by exhaustive enumeration | **X** | none | in | C3, C4 | **use now** (engineering's stage B; FB-P-03 small instances) |
| B-402 | fixed-sequence side-chain instances at several temperatures (the instances of B-1101) | **X** where an exact counter completes | none | in | C3 | **gated** (FB-P-03: the certificate must be a file) |
| B-403 | inference-competition partition-function tracks (SN) | reference Z from exact solvers, uncertified | — | in | C3 | candidate held-out source; not verified |
| B-404 | Boltzmann-target sampling on small peptides with a shared force field (SN) | near-exact free-energy differences | protocols not standardised | in | C3, C4 | context |
| B-405 | host–guest and alchemical binding sets (SN) | E (calorimetry) | used for parameter tuning | desc | none | excluded from evaluation; listed as molecular-interaction evidence only |

## 5. Structural stability and uncertainty

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-501 | mega-scale folding-stability measurements of small domains (FT, partial) | E (ΔG; ≈ 5 kcal/mol range; two-state assumption) | in the training sets of current predictors; needs domain-disjoint splits | **desc** — reference values for fixed sequences, never an objective | C3 only if a model of unfolding existed | context |
| B-502 | literature ΔΔG test sets (SN/MEM) | E, heterogeneous | leakage and class imbalance documented | desc | none | context |
| B-503 | calibration tests for any reported uncertainty: coverage of planted truth | **X** | none | in | C3, C5 | **use now** (part of FB-P-03, -04) |

## 6. Geometric observability and identifiability

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-601 | planted distance-geometry instances (coordinates → exact or interval distances) (SN) | **X** | none; realism is the weakness | in | C6, C7, C10 | **use now** (FB-P-07) |
| B-602 | deposited Cα traces as inputs to stability constants | E (the trace), **X** (the constant) | none | in | C7 | **use now** (FB-P-07; expected negative) |
| B-603 | wwPDB NMR restraint archive and restraint-violation reports (SN) | E restraints; M structures | none | in | C10, C5 | **gated** (forward model) |
| B-604 | blind NMR structure-determination rounds, 2010 and 2013 (SN) | M (reference NMR models) | no longer blind | in | context | context |
| B-605 | multi-laboratory FRET accuracy studies (SN) | E, ≈ 5 Å accuracy | — | in | error model for FB-P-06 | context |
| B-606 | scattering information content (Shannon channels) on analytic bodies (SN) | **X** | — | in | C5 | context |

## 7. Retrospective characterisation of cavities and binding-site annotations

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-701 | aggregated observed-site benchmark (human subset 2,775 chains) (FT, partial) | A (union of observed ligand sites; unobserved sites count as false positives) | detectors trained on overlapping PDB entries | **desc** | none (no cavity method exists in MetricChain) | context |
| B-702 | older single-structure site sets (MEM) | A | redundancy and train overlap documented | desc | none | excluded as primary evidence |
| B-703 | cryptic-site sets from apo–holo pairs (SN) | A | apo choice subjective | desc | none | context |

## 8. Retrospective analysis of established molecular-interaction evidence

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-801 | curated structure–affinity collections and their leakage-controlled splits (SN) | E, mixed provenance | **severe, documented**: benchmark performance "largely driven by data leakage" | **desc** for physics checks; **out** for training or optimising predictors | none | context |
| B-802 | co-folding physical-plausibility critiques (adversarial binding-site changes; prospective pose studies) (SN) | E | memorisation | desc | none | context: why validity checks accompany any pose metric |

## 9. Electrostatics and solvation mathematics

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-901 | Born ion and Kirkwood sphere (analytic series) | **X** | none | in | any future electrostatics layer; science's implicit-solvent constants | **gated** (FB-P-11; nothing to evaluate yet) |
| B-902 | hydration free energies of small molecules, 642 compounds (SN) | E (mean uncertainty ≈ 0.6 kcal/mol) | implicit-solvent parameters often tuned on it | in | none | context |
| B-903 | protein pKa collections and the blind challenge on buried residues (FT partial / SN) | E, heterogeneous conditions | random residue-level splits allow homologue leakage; the water-pKa null model is hard to beat | in | none | context; the null model is mandatory |

## 10. General mathematical kinetic models

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-1001 | exactly solvable kinetic networks (small Markov chains; voxel graphs with known spectra) | **X** | none | in | science's certified cuts and barrier intervals | **use now** as engineering stage B |
| B-1002 | folding-rate collections (SN) | E for relative rates; prefactor unknown | temperature corrections are model assumptions | in | none ("not as physical rates") | context |

## 11. Numerical accuracy, computational complexity, certificates

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-1101 | **fixed-sequence side-chain instances** of the 2011 inference challenge as hosted by INRAE: ten `pdb*` instances, 337–1,972 variables, domains ≤ 81 **[C]** (downloaded, headers parsed, checksums in `RESULTS.md`) | **X** (optimum established by independent exact methods) | built by solver developers; energies of 2011 rounded to integers; now *seen* by us → development instances | in | C1 | **use now** (FB-P-01 pilot run) |
| B-1102 | the eleven instances of the same category with domains up to 350–503 **[C]** | — | — | **out** (consistent with design instances) | — | **excluded** |
| B-1103 | larger fixed-sequence side-chain sets of the literature (≈ 370 instances; hosting not verified) (SN) | **X** | — | in | C1 | held-out candidate; to be located |
| B-1104 | synthetic instance families with controlled treewidth, domain size, frustration (engineering's and structural biology's generators) | **X** | generated by the evaluated divisions → development only unless seeds are published in advance | in | C1, C2, C3 | development |
| B-1105 | certified tracks of the pseudo-Boolean competition; proof-logging MaxSAT studies (FT) | proofs checked by a verified checker | — | in | C1 (the incumbent's overheads) | context; the comparison standard |
| B-1106 | model-counting competition with certified counting (SN) | certified counts | — | in | C3 | context |
| B-1107 | hardness gadget families of the complexity division (planted optima) | **X** | none | in | C8 | **use now** as stress tests of heuristic folding codes (low priority) |
| B-1108 | planted violations of hypotheses (FB-P-09) | **X** | none | in | C1–C3, D10 | **use now** as a specification |

## 12. Physical consistency of molecular simulations

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-1201 | statistical-mechanics validity tests (kinetic-energy distribution, equipartition, ensemble consistency between state points) (SN) | **X** (exact distributions) | none | in | any future simulation or sampling layer | **gated** (nothing to evaluate yet) |
| B-1202 | stability-under-dynamics tests for learned potentials (SN) | E/M | — | in | none | context |

## 13. Evaluation instruments

| id | benchmark | truth | contamination note | charter | bears on | verdict |
|---|---|---|---|---|---|---|
| B-1301 | structure-comparison self-consistency controls (identity, rigid motion, reflection, planted perturbations) | **X** | none | in | our own scoring tools | **use now** (FB-P-10) |
| B-1302 | official CASP17 per-model scores after 2026-11-29 | the community's numbers | our scores frozen beforehand | in | our own scoring tools | **use now** (FB-P-10) |

## Reading the registry as a whole

* The only rows marked **use now** against an *existing* MetricChain capability are those with
  exact or planted truth (B-203, B-204, B-401, B-503, B-601, B-602, B-1001, B-1101, B-1107,
  B-1108).  That is what the programme can be tested on today.
* Every row with experimental truth is **gated** on something that does not yet exist — a
  molecular layer, a forward model with a stated error, or a certificate that is a file — or
  is **context** because MetricChain has no capability in that area at all (structure
  prediction, disorder, binding sites, electrostatics, kinetics as physical rates).
* Rows marked SN or MEM are leads from the literature assessments and are confirmed at the
  source before a protocol depends on them.
