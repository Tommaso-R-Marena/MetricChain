# Benchmark readiness by role (consolidation state, 2026-11-27)

*What this is.*  The owner's directive FB-D-4 names benchmarks beyond CASP17 and six roles in
which MetricChain might be evaluated.  The directive FB-D-5 halted the work before any of
these evaluations was run and forbids a new literature investigation.  This file therefore
records **readiness only**, from what this division already knew: the registry
(`BENCHMARK_REGISTRY.md`, 53 rows), the intake of the seven divisions, and two pilots.
**No fact about an external benchmark was re-verified for this file**; where the registry
row was read at its source the registry says so, and names not in the registry are marked
*unregistered — described from memory*.

*Roles.*  **R1** standalone method · **R2** certification layer over another method's output ·
**R3** uncertainty / identifiability framework · **R4** scoring, ranking or validation ·
**R5** thermodynamic framework (partition functions, free energies) · **R6** component of a
larger pipeline.

*Levels reached* (the owner's distinction; the highest level actually reached is given):
**M** mathematics only · **S** implemented software · **Y** validated on synthetic or planted
controls · **C** realistic computational validation (public instances or structures, against
published baselines) · **X** independent experimental evidence · **Sup** demonstrated
superiority.  Nothing in MetricChain is at **X** or **Sup** on any benchmark.

## 1. Where an evaluation could be run with what exists

| owner-named benchmark | registry | role | what exists today | level | what is missing before a defensible run |
|---|---|---|---|---|---|
| certified optimisation on public fixed-sequence side-chain instances | B-1101 | R2 (R1 as solver) | SB producer and checker; our pilot and diagnosis (`RESULTS.md` §§1, 6) | **C, negative**: 4 of 10 certified at 300 s, 17–326× slower | a producer with a usable node rate (IR-01, IR-02); certified baselines not run by anyone (pseudo-Boolean with VeriPB/CakePB; exact-rational relaxation) |
| Top2018, CASP13–15 native-backbone packing sets, contemporary packing benchmarks | B-105, B-106 (Top2018 *unregistered*) | R1; R2 as "certified repacking of a given backbone" | SB molecular layer, rotamer library, energy model v2, six development structures; our torsion scoring validated against biotite on one crystal structure; protocol FB-P-02 v1.1 (design, not frozen); FASPR source fetched (commit `0d55732`), not built | **Y** for the optimiser; accuracy against deposited conformations: **not measured by us** | a frozen SB release; baselines run under equal information (FASPR, SCWRL4, Rosetta packer, a learned packer); a public validation list disjoint from the sealed pool; then the sealed list |
| partition functions / free energies on fixed models | B-401, B-402, B-403 | R5 | SB certified `ln Z` intervals on development models (one figure read from a commit subject: crambin, width 0.0075 nats, 145 leaves, 65 s — not reproduced by us); protocol FB-P-03 (gated) | **Y** (by its authors) | certificate files as evaluable artefacts; baselines (K\*/BBK\*-type bounds, toulbar2's counting mode, certified model counting, sampling) — none run |
| uncertainty and identifiability on planted truth | B-203, B-503 | R3 | 25 planted controls of the ensemble division; 9 recomputed independently by us, all reproduced; two simple reweighting baselines run (`RESULTS.md` §2) | **Y** | software for a general finite pool with tolerances (the ensemble division: "no forward model and no software"); established comparators (BME, EROS, MaxOcc) |
| CASP17 scoring conformance | B-101, B-1302 | R4 (of our own instruments only) | frozen scores of 1,163 public models (FRONTIER-FRZ-0003) | frozen, outcome pending | the official numbers (announced for 2026-11-29); authorisation to run the comparison (FB-D-5) |

## 2. Where MetricChain could only enter in a supporting role, and only after a capability exists

| owner-named benchmark | registry | conceivable role | why not now |
|---|---|---|---|
| CAMEO, CASP13–16 structure prediction | B-102, B-103 | R2/R6: repack or audit the side chains of an upstream predictor's model on its own backbone; with/without comparison holding the upstream model fixed | nothing in MetricChain takes a sequence (the CASP17 determination).  As R2 the expected gain in accuracy is small: the one published study known to us found < 0.1 % from the exact optimum (Yanover et al. 2008, abstract level), and science estimates model error at 60–100 times any optimality gap (SCI-RES-0041).  Any such run must report the upstream model's score separately |
| ATLAS, mdCATH (simulation ensembles) | B-206 | R3: known ensemble → simulated averaged data → are the certified intervals correct and informative? | needs forward models and pool software (IR-09); the truth is a simulation, so the level reachable is **C**, not **X** |
| apo–holo and multi-state sets | B-207, B-703 | R3/R4 | no capability proposes alternative states; no forward model |
| disordered proteins: solution scattering and NMR data | B-302 | R3 | as for ATLAS; additionally the pool is never a net of the space (ENSEMBLE-RES-0008 E-2: the enclosure degrades with pool coarseness) |
| electrostatics: Born ion, Kirkwood sphere | B-901 | R5 analytic controls | no MetricChain capability addresses continuum electrostatics |
| kinetic models | B-1001, B-1002 | analytic controls | no MetricChain capability |

## 3. Where no evaluation is recommended

| owner-named benchmark | registry | reason |
|---|---|---|
| ProteinNet | *unregistered* | a training and evaluation split for learned structure predictors (from memory); MetricChain has no learned predictor |
| ProteinBench | *unregistered* | a suite for protein foundation models, in part design tasks (from memory); the design part is outside the charter; the conformational part is covered by B-206 |
| CAID, DisProt | B-301 (DisProt *unregistered*) | residue-level disorder classification from sequence; no capability, and none follows from the present mathematics |
| PDBbind, CASF | B-801 | affinity scoring and docking need a ligand energy model; none exists; retrospective analysis only under the charter |
| LIGYSIS, HOLO4K | B-701, B-702 | binding-site detection; no capability |
| SABIO-RK, BRENDA-derived sets | *unregistered* | enzyme kinetic parameters; no capability and none in prospect |
| ThermoMutDB 2.0, FireProtDB, ProThermDB, SKEMPI 2.0 | B-501, B-502 (SKEMPI *unregistered*) | **an owner decision is needed before any capability is requested.**  Scoring public measurements retrospectively is evaluation; but the capability these benchmarks measure — the effect of changing residues — is one step from sequence optimisation, which the charter excludes ("fixed-sequence structural characterization").  We registered the benchmarks and requested nothing |

## 4. Reading across the table

1. **Two evaluations are close to executable and bear on the programme's central claims**: the
   certified optimum against toulbar2 with a repaired producer (B-1101), and side-chain
   placement against deposited structures (B-105/B-106).  A third — identifiability intervals
   on public experimental data against maximum-entropy reweighting — needs only a finite-pool
   interval tool and a public data set (the BME example data were fetched, commit `314d3b5`,
   and not used).  These are the three next actions of the consolidation report.
2. **Most owner-named benchmarks measure capabilities MetricChain does not have** (prediction
   from sequence, affinity, pockets, disorder, kinetics).  Forcing an evaluation there would
   measure an upstream model, not MetricChain.
3. **No benchmark in this file has been used with the sealed list.**  The sealed 47
   structures are reserved for the first frozen release of the side-chain protocol.
