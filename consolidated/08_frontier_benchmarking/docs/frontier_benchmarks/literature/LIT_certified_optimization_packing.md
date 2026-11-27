> **Provenance.** Report of a literature assessor (a subagent of the Frontier Benchmarking division,
> model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from this
> notice.  Every row carries a *read level*; rows marked "search snippet" or "from memory" are
> unverified leads, not findings.  The coordinator read this report in full, checked none of its
> sources independently unless `../STATE_OF_THE_ART.md` or `../BENCHMARK_REGISTRY.md` says so, and
> carries the read levels forward wherever a row is used.  Out-of-charter items (sequence or
> molecule design, target-specific optimisation) are listed only to mark the boundary.

# Literature assessment: certified discrete optimisation, ln Z bounds, proof logging, side-chain packing

Assessor: literature subagent. Access date for all sources: 2026-11-26. About 42 web or literature calls.

**Read-level codes:** FT = full text read (key sections pulled out locally or read via the literature API). FT-S = full text read through an automated page summariser (good for numbers, weaker on nuance). AB = abstract or landing page read. OFF = official page read. SN = search snippet only. MEM = from memory, not verified.

**Evidence codes:** IND = independent (a competition, or a third party that did not develop the tools). SELF = reported by the tool's own developers. MIX = developers among the co-authors of a multi-solver comparison.

**Headline caveat:** I found no published proof logging or machine-checkable certificate for weighted CSP, cost function network (CFN) or MAP-MRF solving. That covers soft arc consistency, VAC and HBFS in toulbar2, and DEE/A* in OSPREY. The nearest work is in five places:
- VeriPB proof logging for pseudo-Boolean (PB) solving, MaxSAT and CP propagators.
- VeriPB enumeration and counting proofs (CP 2026).
- CPOG for weighted model counting, with a checker verified in Lean 4.
- VIPR for exact rational MIP.
- PBLean, which imports VeriPB proofs into Lean 4 (2026).

This absence is search-based (three targeted queries plus the toulbar2 release page). It is not proof of non-existence.

---

## 1. Solver and method table

| Method | Problem | Version and date (verified?) | Guarantee | Evidence | Availability and licence | Repro, compute, assumptions | Limitations | Fair comparison with a certified kernel? |
|---|---|---|---|---|---|---|---|---|
| **toulbar2** (HBFS, VAC, EDAC, VNS; plus pytoulbar2) | CFN / WCSP minimisation, MAP-MRF; also partition function (Z*ε lineage) | v1.4.0 released 2026-08-27; pytoulbar2 1.4.0.3 on 2026-11-20 (OFF: GitHub releases page and PyPI JSON). The papers used v0.9.8. | Optimality is claimed by the solver. **No proof or certificate output found.** The release page does not mention proof logging (OFF). | MIX: Hurley 2016 solved 2433 of 3026 instances at 1 h, the most of 7 solver configurations (FT). Simoncini 2015 proved the GMEC on 98 design instances within 100 h (SELF, FT). IND: entered the PB25 PARTIAL-LIN track, 6th of 9 with 144/208 (FT, PB25 slides). A toulbar2 portfolio won the UAI 2014 MAP task (SN, via Hurley 2016). | Open source; MIT licence (PyPI metadata, OFF) | Single core, CPU only. Integer costs: real energies must be scaled and rounded to a fixed decimal (Hurley used 2 digits for CFLib/PIC; FT). | Bounds are floating-point or integer, with no audit trail. Default parameters (`-A -V -dee -hbfs` in Hurley) matter. | **Yes, and it is the mandatory baseline.** Use the same integerised cost tables and tuned parameter sets. Compare time-to-optimality and time-to-certificate separately. |
| **OSPREY 3.x** (DEE/A*, iMinDEE, LUTE; K*, BBK*, COMETS; MARK*, EWAK*, SOFEA) | GMEC with discrete or continuous flexibility; ε-approximate partition functions (K*) | Not verified. The OSPREY 3.0 paper is J. Comput. Chem. 2018 (SN). The lab page returned 503. | "Provable with respect to the input model": optimality or an ε ratio holds under the pairwise energy, rotamer and minimisation-bound assumptions (SN). No external certificate. | SELF only. Allouche 2014 and Simoncini 2015 (developers of the competing CFN tool) report the CFN approach several orders of magnitude faster than DEE/A* (SN, FT). | Open source; licence not verified (believed GPL-2, MEM) | JVM with optional GPU, per the paper (MEM). Continuous-flexibility guarantees depend on local minimiser bounds, which are floating point. | MARK*, EWAK* and SOFEA claims were not found or verified. Most of the published use is in design, which is out of scope. | Yes, for fixed-sequence GMEC (one amino acid per position) and K*-style ln Z on the same discrete model. Rigid-rotamer mode is required for an exact like-for-like comparison. |
| **ILP/MIP** (CPLEX, Gurobi, SCIP, HiGHS) on the local-polytope formulation | GMEC as 0/1 LP | CPLEX 12.6.0.0 in Hurley 2016 (FT). SCIP Optimization Suite 10.0, 2025 (SN). | Optimality claimed (floating point). Exact SCIP plus **VIPR** gives checkable certificates in rational arithmetic; presolving is not certified in VIPR (SN, SCIP 10 report). | Kingsford 2005: on native or homologous backbones, the **LP relaxation is usually already integral** for SCP. Design instances often need ILP (AB). Hurley 2016: CPLEX was competitive, solving 1862 of 3026 (direct LP; FT). | CPLEX and Gurobi are commercial (free academic licences); SCIP is Apache-2.0 since v9 (MEM); HiGHS is MIT (MEM) | Deterministic; memory-heavy on the tuple encoding | Floating-point tolerances (EPGAP and similar) mean "optimal" is within a tolerance. | **Yes.** It is critical because LP tightness on fixed-sequence SCP means an exact-rational LP dual is a cheap, natural certificate baseline. |
| **MAP-LP message passing** (MPLP/MPLP2, TRW-S/TRBP, AD3) | Dual bounds and MAP | MPLP2 "version 2" tested in Hurley 2016 and dominated by toulbar2 in most categories (FT). AD3 and TRW-S versions not verified. | Dual lower bound (floating point). Optimality only when the primal-dual gap closes. | Yanover 2006: TRBP faster than CPLEX on the LP relaxations of side-chain and vision problems (AB). Sontag 2008: the LP is not tight on only 30 of 370 side-chain instances, and cycle tightening solved all of those (SN). | Research code | Fast | Floating-point duals are not certificates. | Yes, as a lower-bound-quality baseline. |
| **daoopt** (AND/OR branch and bound with mini-buckets) | MAP/MPE | Open-source 1.1.2 in Hurley 2016; it won PIC 2011 (FT) | Optimality claimed | MIX (Hurley: 1832 of 3026 solved; FT) | GitHub `lotten/daoopt` (licence not verified) | Exploits treewidth | Not maintained? (not verified) | Optional baseline. |
| **MaxSAT / PB solvers** (MaxHS, RoundingSat, Exact) | GMEC encoded as weighted MaxSAT or PBO | MaxHS 2.51 in Hurley 2016 (FT). PB25 entrants (FT). | Proof-logging variants produce **VeriPB proofs checked by CakePB**, a formally verified checker. | IND: PB25 CERT tracks (§3) | Open source (various) | Encoding blow-up for large domains | Encodings must themselves be verified. | **Yes. This is the strongest "certified" baseline available today:** encode the GMEC as PBO, run roundingsat with logging, and check with VeriPB+CakePB. |
| **Rosetta Packer** (simulated annealing) | GMEC heuristic on the Rosetta energy | Not verified | None | Simoncini 2015: on design, 1000 fixbb runs sometimes ended more than 2 Rosetta energy units (REU) above the proved optimum; worst single run 37.5 REU (SELF by competitor, FT). Vangaru 2025: PyRosetta Packer fewest clashes among the packers (IND, FT). | Rosetta Commons licence (free academic; MEM) | Stochastic | No bound of any kind | Yes, as the practitioner default. Report the energy gap to the certified optimum. |
| **Quantum / annealing** (QAOA for SCP) | QUBO SCP | arXiv 2609.31077, 2026-09-25 (AB) | None | SELF. One protein (5PTI). No comparison with a classical exact solver in the abstract. Hardware vs simulator not stated (AB). | — | — | Toy scale | No meaningful comparison. Record as non-evidence. |

## 2. Benchmark and instance-collection table

| Collection | Origin | SCP vs design | Sizes | Hosting / licence | Published results | Contamination / tuning risk |
|---|---|---|---|---|---|---|
| **EvalGM / Hurley 2016 set** (3026 instances in uai, wcsp, lp, wcnf and mzn) | Merged PIC 2011, UAI 2008, OpenGM2/CVPR, CFLib, MaxCSP 2008, WPMS 2013, MiniZinc 2012–13 (FT) | Mixed. Contains **MRF/ProteinFolding** (21 instances, max domain 503; from the PIC 2011 Yanover side-chain set, so fixed-sequence SCP). Also **CFN/ProteinDesign** (10 instances, max domain 198; design) and ProteinInteraction (8). **The SCP subset is separable by category name.** | MRF 319, CVPR 1461, CFN 281, MaxCSP 503, WPMS 427, CP 35 (FT) | web-genobioinfo.toulouse.inrae.fr/~degivry/evalgm (readme OFF). Licence not stated (not verified). | Table 3 of Hurley 2016 reports every solver on every category (FT). | Costs rounded to 2 decimals. toulbar2 developers built the set. "Easy" instances (<5 s) were removed in the hardness analysis (FT). |
| **Cost Function Library (CFLib)** | costfunction.org (FT, cited in Hurley) | Mixed. The protein design category is design. Other categories are not protein. | Not verified | costfunction.org/benchmark (not reached) | Hurley 2016 | — |
| **PIC 2011 / UAI 2008, 2014, 2022 inference sets** | UAI competitions | PIC "ProteinFolding" is SCP. "ProteinProtein" (interaction) also appears. Other categories are not protein. | Not verified beyond above | cs.huji.ac.il/project/PASCAL (2011, link may be dead); uaicompetition.github.io (2022) | UAI 2022 had PR, MAR and MAP tasks. PR score = absolute log10 ratio to the true Z (SN). Winners not verified (leaderboard 404). | PR "true Z" references come from exact solvers; uncertified. |
| **Yanover, Meltzer & Weiss 2006 side-chain and design MRFs** | JMLR 2006 (AB); also Sontag 2008 | **Both, as separate sets.** About 370 side-chain prediction instances (SCP) and 97 design instances (SN, via Sontag) | Not verified | Original host not verified | LP tight on all but about 30 SCP instances. MPLP with cycles solved them all; for design, the LP is tight on only 2 of 97 (SN). | Rosetta-era energy; old PDB set |
| **Simoncini 2015 CPD set** | Rosetta Talaris2014 + Dunbrack library on relaxed backbones (FT) | **Design only.** Out of scope except for algorithmic stress testing. | Up to 1098 bits of problem size. 98 proved within 100 h. | Public BitBucket repository (URL truncated in the text; not verified) plus ACS SI figshare | toulbar2 0.9.8 vs Rosetta fixbb | Developer-built |
| **OpenGM2 (Kappes 2015)** | 2453 computer-vision instances (SN) | Other (vision). The Hurley "ProteinPrediction/ProteinInteraction" category came via CVPR (FT). | — | hci.iwr.uni-heidelberg.de/opengm2 (FT, cited) | Polyhedral and ILP methods competitive (SN) | — |
| **Kingsford 2005 SCP ILP set** | Native and homologous backbones (AB) | SCP plus a separate design set | Not verified | compbio.cs.princeton.edu/scplp (code; not checked) | LP usually integral for SCP | — |
| **PB / MaxSAT competition sets** | PB25, MSE 2024 | Other | PB25: OPT-LIN-CERT and DEC-LIN-CERT used the same selection as the main tracks (FT) | cril.univ-artois.fr/PB25 | §3 | — |
| **CASP13/14/15 native-backbone packing sets** | predictioncenter.org | Fixed-sequence SCP (structural ground truth) | Vangaru 2025: CASP14 n=66, CASP15 n=71 (single chain, <2000 residues). FlowPacker: CASP13/14/15 = 20/34/45. PIPPack: CASP13 82, CASP14 64 (FT). | predictioncenter.org | §4 | **Target counts differ across papers.** Training-set redundancy filtering differs (FlowPacker uses 40% identity via MMseqs2). |

No public collection of fixed-sequence SCP cost tables with exact rational or interval-certified energies was found.

## 3. Proof-logging overhead evidence

| Format / checker | Solver, context | Reported size / overhead | Formally verified checker? | Read |
|---|---|---|---|---|
| VeriPB to CakePB | **PB Competition 2025 CERT tracks** (IND). 6 solvers. Solver limit 1 h CPU; proof cap 100 GB; checking 5 h, later extended to 10 h. | **Verification time / search time up to 2387×.** Of verified proofs, 2894 took ≤0.25 h; 0.76% took >5 h; 53 timed out. Some answers could not be checked, and "some results should be taken with caution". The best OPT solver certified 310 OPTC + 18 UNSC (328) vs 329 when uncertified answers count. "Exact" fell from 285 to 234 when only certified answers count. RoundingSat used VeriPB's **unchecked deletion** mode. | Yes (CakePB, CakeML/HOL4) | FT (slides) |
| VeriPB | Certified branch-and-bound MaxSAT (MaxCDCL; Vandesande, Coll & Bogaerts, AAAI-26 / arXiv 2511.10273), MSE 2024 weighted instances | Solving overhead **median 23%**, about 10% of instances above 153%. Checking: **237 of 350 proofs checked** within 10 h / 64 GB; **median check time 23.25× solve time**. CakePB not used. | Not in this study | FT-S |
| MaxSAT-specific proofs | Core-guided OLL (van Doren et al., ASE 2025) | All solved instances among 571 MSE 2024 instances verified. Claims that generic VeriPB has "substantial verification overhead". | Not verified | SN |
| VeriPB + CakePB | Certified MaxSAT preprocessing (Ihalainen et al., IJCAR 2024) | "Feasible", room to improve | Yes | SN |
| VeriPB counting / enumeration | CP 2026 (LIPIcs.CP.2026.43) | Not extracted | CakePB backend extended | AB |
| PBLean (VeriPB to Lean 4 by reflection) | Szeider, arXiv 2602.08692 (Feb/Apr 2026) | "Tens of thousands of steps"; no benchmark numbers in the abstract | Soundness proved in Lean. The checker runs as compiled native code, so the Lean compiler is in the trusted base (an inference from "compiled native code"). | AB |
| LRAT/LPR to cake_lpr | SAT Competition main track; DRAT-trim as preprocessor (SN) | 2025 organisers reported "proof checking issues on some big proofs" (SN) | Yes (CakeML/HOL4) | SN |
| VIPR | Exact SCIP (Eifler & Gleixner 2021+; SCIP 10) | SCIP 10 report: logging plus checking overhead "does not exceed the time needed for solving"; presolve not certified. SMT-based VIPR checking reportedly faster than exact solving on average. | VIPR checker verified? Not verified | SN |
| CPOG | Weighted and unweighted model counting via D4 decision-DNNF (Bryant, Nawrocki, Avigad, Heule; SAT 2023, JAIR 2025) | Scales to "all but the largest" Model Counting Competition graphs. Only D4 output is handled. | **Yes: checker and ring evaluator verified in Lean 4** | SN |

**Implication.** Independent data say checking costs typically run up to 1–2 orders of magnitude over solve time (median 23× in one MaxSAT study), with tails above 1000×. A new certificate format should be judged on four things: checking-time ratio, certificate size, whether the trusted base is small (a verified checker vs compiled-reflection Lean), and fraction of instances whose certificates actually check within a stated budget. Its overall standing should be judged against VeriPB+CakePB.

## 4. Side-chain packing

| Method | Type | Training cutoff | Headline independent results (Vangaru & Bhattacharya 2025, Brief. Bioinform., FT; IND) | Limitations |
|---|---|---|---|---|
| FlowPacker | Torsional flow matching (EquiformerV2) | PDB-S40 snapshot 2023-07-28; 40% identity filtered against CASP13–15 (FT, SELF paper) | Native backbone, CASP15: RR 66.4%, RMSD 0.69 Å. On an AF2 backbone: RR 55.1% vs AF2's own 53.9% (the only significant gain) | Reported DiffPack leakage (below) |
| PIPPack | Invariant point message passing | BC40, chains before Aug 2020 (FT-S, SELF) | CASP14 native: RR 58.1% (best) | More clashes (131 at the 100% vdW threshold) |
| DiffPack | Autoregressive torsional diffusion | BC40 (per FlowPacker; not verified at source) | CASP15 native RMSD 0.68 Å | **FlowPacker reports leakage:** DiffPack's quality depends on the ground-truth side-chain bond geometry it is given; with idealised inputs it gets much worse (SELF by competitor, FT) |
| AttnPacker | SE(3) graph transformer | BC40 (per FlowPacker) | CASP15 RR 59.2% | — |
| DLPacker | 3D U-Net voxels | Not verified | CASP15 RR 59.5% | — |
| FASPR | Rotamer library + deterministic search (DEE/tree decomposition per its paper, MEM) | n/a (rotamer library) | CASP15 RR 55.8% | — |
| SCWRL4 | Rotamer library + graph decomposition | n/a | CASP15 RR 55.5% | Most clashes |
| Rosetta Packer | Rotamer library + simulated annealing on REF15 | n/a | CASP15 RR 58.0%; fewest clashes | Stochastic |
| AlphaFold2/3 own side chains | Co-folding | AF2 and AF3 cutoffs not verified here | On AF backbones, **AF's own side chains are best or equal on almost all metrics**. Repacking by any method gives no significant improvement except FlowPacker's RR on CASP15/AF2. A pLDDT-weighted integrative repack gained +1.5% RR over AF2 and negligible gains over AF3. | — |
| OPUS-Rota4/5, H-Packer, OSCAR-star, post-2025 leaders | — | Not verified | No independent results found | Not searched in depth (budget) |

RR (recovery rate) in Vangaru 2025 counts a residue as recovered only if **all** of χ1–χ4 are within 20°. That is stricter than the common χ1 or χ1+2 within 40° metrics, so RR values cannot be compared across papers without recomputation. Core residues have centrality ≥20 Cβ within 10 Å; surface residues ≤15.

**Physical-relevance evidence (item F):**
- **Exact optimum barely helps with the default Rosetta energy.** Yanover, Schueler-Furman & Weiss (RECOMB 2007 / J. Comput. Biol. 2008; SN) found that reaching the global optimum of default Rosetta improved χ1+2 accuracy by <0.1% over simulated annealing (about 72%). With a soft-repulsive energy it gave +1% (77% to 78%). Learning the energy weights gave +6 points, and an extended library plus learned weights reached 82.6%.
- **Search is rarely the bottleneck on fixed-sequence SCP.** Voigt, Gordon & Mayo 2000 found DEE converges to the GMEC on all their side-chain placement cases (SN). Kingsford 2005 and Sontag 2008 found LP tightness on most SCP instances (AB/SN).
- **Search error does matter in design-sized spaces.** Simoncini 2015 showed simulated-annealing gaps of several REU there, but this is out of scope.
- **Exactness does not fix the inputs.** PackBench data show backbone error dominates on predicted structures; exact search on a fixed AF backbone cannot fix that.

**Synthesis:** the value of exact GMEC certification on fixed-sequence SCP is mainly **auditability, reproducibility and energy-function debugging**, not accuracy against experiment. Any accuracy claim must be tested empirically, against tuned heuristics, on the same energy.

## 5. What a fair, strong-baseline comparison must include

**Certified GMEC kernel:**
1. **Same model, same numbers.** Publish the exact integer or rational cost tables (WCSP/UAI/LP/WCNF exports). Rounding or scaling of real energies must be stated, as in Hurley's 2-digit fixed point. Report how the optimum moves with precision.
2. **Baselines:**
   - toulbar2 v1.4.x with default settings and the HBFS+VAC settings used in Hurley 2016.
   - CPLEX or Gurobi, plus SCIP and HiGHS, on the local polytope, with an exact-rational LP / exact SCIP+VIPR leg.
   - MPLP or TRW-S dual bounds.
   - A PBO encoding solved by proof-logging RoundingSat and checked by VeriPB+CakePB (the independent certified state of the art).
   - The OSPREY DEE/A* rigid-rotamer mode.
   - Rosetta Packer as the heuristic reference.
3. **Report the LP-integrality fraction.** Prior work says most fixed-sequence SCP instances are LP-tight. A certified kernel must beat "exact-rational LP dual plus integral primal" on those instances to show value, and should separately report the non-tight subset.
4. **Instances.** Use:
   - The Yanover/PIC ProteinFolding SCP subset and other SCP-only categories, separated from design categories.
   - Freshly generated fixed-sequence instances from CASP14/15 native backbones with a documented rotamer library.
   - Synthetic instances with controlled treewidth and domain size.
   Pre-register the selection and do not drop "easy" instances silently.
5. **Measurements.** Kept separate:
   - Solve time.
   - Certificate size.
   - Checker time and the ratio checker/solve (PB25 reported ratios up to 2387×).
   - Fraction checked within budget.
   - Trusted computing base (Lean kernel only, or Lean compiler/`native_decide`, or CakeML-verified binary).
   - Time limits matching competition practice (1 h solve, 5–10 h check, as in PB25).
6. **Independence.** Run baselines with their authors' recommended settings. Ideally get them reviewed by baseline developers, or enter an existing competition (PB, MaxSAT, UAI).

**Certified ln Z kernel:**
1. Baselines:
   - Z*ε (toulbar2 lineage; a deterministic (1+ε) ratio guarantee, proved in CP 2016).
   - K* in OSPREY (ε-approximation).
   - Exact weighted model counters (d4, SharpSAT-TD, ADDMC lineage), with **CPOG plus its Lean 4-verified checker** as the certified-counting state of the art.
   - Weighted mini-bucket (deterministic upper bounds).
   - Dynamic importance sampling (probabilistic 1−δ bounds; state which kind of guarantee is meant).
2. Instances: UAI PR-track instances (scored as absolute log10 Z error), plus SCP instances at several temperatures.
3. Report the two-sided bound width in ln units versus time, and compare with exact ln Z where it is computable.
4. Report floating-point vs rational arithmetic explicitly. **Z*ε's guarantee is stated for exact arithmetic.** Whether the implementation rounds soundly was not verified.

## 6. Could not verify, and open questions

- Whether any WCSP/CFN/VAC proof logging exists (2023–2026). None was found; asking the toulbar2 and VeriPB groups would settle it.
- OSPREY current version, licence, and the guarantee statements for MARK*, EWAK* and SOFEA.
- Allouche 2014 result tables; Kappes 2015 protein content; UAI 2022 PR winners; Model Counting Competition 2024–2025 weighted results and any certified track.
- VIPR checker formal-verification status and per-instance overheads.
- SAT Competition 2025 checker per solver and proof sizes.
- Sizes and treewidth of the Yanover SCP instances; current hosting of the PIC 2011 data.
- Training cutoffs of DiffPack, AttnPacker and DLPacker at source; AF2/AF3 cutoffs relative to CASP15 targets.
- OPUS-Rota5, H-Packer, OSCAR-star, and any 2025–2026 packers (e.g. co-folding models used as packers).
- Validated numerics (item D):
  - Libraries, all MEM: Arb (merged into FLINT 3, 2023), MPFI, IntervalArithmetic.jl, CORE-MATH (correctly rounded libm), IBEX.
  - The only related literature found (SN): LeanLJ (arXiv 2505.09095), a Lean 4 formalisation of Lennard-Jones energy that sets floating-point error aside; computer-assisted interval proofs of LJ crystal minimisers (arXiv 2506.22614).
  - **No published interval-certified rotamer-pair energy-matrix computation was found.** This is a genuine gap, and also an unvalidated assumption in any "certified GMEC from a real force field" claim.
- Published critiques of evaluation practice (item G), as found:
  - DiffPack geometry leakage (FlowPacker).
  - Inconsistent CASP target sets and recovery-rate (RR) definitions across papers.
  - Developer-built benchmark sets with easy-instance filtering (Hurley).
  - "Not all answers could be checked" (PB25).
  - Hooker 1995 "Testing heuristics" and Dolan–Moré performance profiles are standard references (MEM).

## 7. Sources (accessed 2026-11-26)

| # | URL | Title | Read |
|---|---|---|---|
| 1 | https://github.com/toulbar2/toulbar2/releases | toulbar2 releases | OFF |
| 2 | https://pypi.org/pypi/pytoulbar2/json | pytoulbar2 PyPI metadata | OFF |
| 3 | https://miat.inrae.fr/degivry/Hurley16b.pdf (DOI 10.1007/s10601-016-9245-y) | Hurley et al. 2016, Multi-language evaluation of exact solvers in graphical model discrete optimization, Constraints | FT |
| 4 | https://web-genobioinfo.toulouse.inrae.fr/~degivry/evalgm/readme_hbfs.txt | EvalGM readme | OFF |
| 5 | https://miat.inrae.fr/degivry/Simoncini15b.pdf (DOI 10.1021/acs.jctc.5b00594) | Simoncini et al. 2015, Guaranteed discrete energy optimization on large protein design problems, JCTC | FT |
| 6 | https://hal.inrae.fr/hal-01268554v1 | Allouche et al. 2014, Computational protein design as an optimization problem, AIJ 212 | SN |
| 7 | https://miat.inrae.fr/schiex/Doc/Export/CP2016.pdf | Viricel et al. 2016, Guaranteed weighted counting for affinity computation, CP | FT |
| 8 | https://miat.inrae.fr/degivry/Viricel18a.pdf | Viricel et al. 2018, Bioinformatics 34(15) | SN |
| 9 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6391056 | OSPREY 3.0, J Comput Chem 2018 | SN |
| 10 | https://www.cs.princeton.edu/~mona/Bioinformatics_SCP.pdf (DOI 10.1093/bioinformatics/bti144) | Kingsford, Chazelle & Singh 2005 | AB |
| 11 | https://www.jmlr.org/papers/v7/yanover06a.html | Yanover, Meltzer & Weiss 2006, JMLR 7 | AB |
| 12 | https://arxiv.org/abs/1206.3288 | Sontag et al. 2008, Tightening LP relaxations for MAP using message passing | SN |
| 13 | https://cs.huji.ac.il/w~yweiss/recomb07-final.pdf | Yanover, Schueler-Furman & Weiss 2007/2008 | SN |
| 14 | https://authors.library.caltech.edu/records/vzpt0-tdq09 | Voigt, Gordon & Mayo 2000, JMB | SN |
| 15 | https://arxiv.org/abs/1404.0533 | Kappes et al. 2015, IJCV | SN |
| 16 | https://www.cril.univ-artois.fr/PB25/slides/PB25.pdf | Pseudo-Boolean Competition 2025 results slides | FT |
| 17 | https://arxiv.org/html/2511.10273v1 | Vandesande, Coll & Bogaerts, Certified Branch-and-Bound MaxSAT Solving | FT-S |
| 18 | https://www.cs.yale.edu/homes/antonopoulos-timos/ASE-2025.pdf | MaxSAT proof logging for OLL (ASE 2025) | SN |
| 19 | https://arxiv.org/html/2404.17316v1 | Ihalainen et al., certified MaxSAT preprocessing (IJCAR 2024) | SN |
| 20 | https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.43 | Proof Logging for Projected Enumeration (and Counting?) in VeriPB, CP 2026 | AB |
| 21 | https://arxiv.org/abs/2602.08692 | Szeider 2026, PBLean | AB |
| 22 | https://www.cril.univ-artois.fr/PB26/descr/Documentation_VeriPB_general.pdf | VeriPB documentation | SN |
| 23 | https://satcompetition.github.io/2025/satcomp25slides.pdf | SAT Competition 2025 slides | SN |
| 24 | https://satcompetition.github.io/2024/downloads/checkers/cakelpr.pdf | cake_lpr description | SN |
| 25 | https://arxiv.org/pdf/2511.18580 | SCIP Optimization Suite 10.0 | SN |
| 26 | https://arxiv.org/pdf/2101.09141 | Eifler & Gleixner, exact rational MIP | SN |
| 27 | https://arxiv.org/abs/2501.12906 | Bryant et al., Certified knowledge compilation (CPOG), JAIR 2025 | SN |
| 28 | https://uaicompetition.github.io/uci-2022 | UAI 2022 competition | SN |
| 29 | https://arxiv.org/pdf/2504.13842 | Model Counting Competitions 2021–2023 | SN |
| 30 | https://proceedings.neurips.cc/paper_files/paper/2017/file/1f1baa5b8edac74eb4eaa329f14a0361-Paper.pdf | Lou, Dechter & Ihler 2017, Dynamic importance sampling | SN |
| 31 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12192453 (DOI 10.1093/bib/bbaf297) | Vangaru & Bhattacharya 2025, To pack or not to pack, Brief Bioinform 26(3) | FT |
| 32 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11886813 (DOI 10.1093/bioinformatics/btaf010) | FlowPacker, Bioinformatics 2025 | FT |
| 33 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10769188 | PIPPack, Proteins 2024 | FT-S |
| 34 | https://arxiv.org/abs/2609.31077 | QAOA for protein sidechain packing (2026) | AB |
| 35 | https://arxiv.org/abs/2505.09095 | LeanLJ: Benchmarking energy calculations using formal proofs | SN |
| 36 | https://arxiv.org/html/2506.22614v2 | Computer-assisted proofs, LJ crystal minimisers | SN |
| 37 | https://pubmed.ncbi.nlm.nih.gov/40976968/ | Predicting side-chain conformations by AlphaFold (Biophys J 2025) | SN |
| 38 | https://pmc.ncbi.nlm.nih.gov/articles/PMC2885146 | SCWRL4 (Krivov et al. 2009) | SN |
