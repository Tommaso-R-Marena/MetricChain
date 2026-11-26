> **Provenance.** Report of a literature assessor (a subagent of the Frontier Benchmarking division,
> model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from this
> notice.  Every row carries a *read level*; rows marked "search snippet" or "from memory" are
> unverified leads, not findings.  The coordinator read this report in full, checked none of its
> sources independently unless `../STATE_OF_THE_ART.md` or `../BENCHMARK_REGISTRY.md` says so, and
> carries the read levels forward wherever a row is used.  Out-of-charter items (sequence or
> molecule design, target-specific optimisation) are listed only to mark the boundary.

# Literature assessment: ensembles, disorder, thermodynamics, kinetics, physical consistency

Assessor note. Access date for everything: 2026-11-26. I used about 40 web, fetch and PubMed calls. Read levels: **FT** = full text read (partial for long pages); **AB** = abstract or landing page read (includes PubMed abstracts); **OP** = official page, README or model card read; **SN** = search snippet only; **MEM** = from memory, not verified. "Self-reported" means the evidence comes from the method's developers. "Independent" means a blind assessment or a third-party paper. No score is given unless I saw it in a source.

**Scope boundary.** The mutational-scan stability sets in this file (Tsuboyama 2023, S669 and others) are listed only as measured thermodynamic reference data for fixed sequences: each variant is one fixed sequence with a measured ΔG or ΔΔG. I did not research their use for optimising or designing sequences, and I do not recommend it. That use is outside the unit's charter.

---

## 1. Benchmark and reference-data table

| Name | Scientific question | Measured quantity and uncertainty | Forward model needed | Metrics in use | Contamination / leakage risk | Access / licence | Read level + URL |
|---|---|---|---|---|---|---|---|
| **CASP16 Ensembles, multi-state targets** (Dube et al., Proteins 94:330–347, 2026; online 2025-10-28) | Can methods reproduce 2–3 experimentally solved states? | Atomic coordinates of each state, from X-ray or cryo-EM | None; direct comparison of coordinates | TM-score per state; recovery of the details that distinguish the states | Templates. The one clear success (T1214) had an apo template. Only 10 ensembles were released, a small set | Targets and results on predictioncenter.org | AB https://doi.org/10.1002/prot.70065 |
| **CASP16 domain-linker-domain (D-L-D) targets** (McBride et al., bioRxiv 2025-09) | Distribution of inter-domain poses for a protein A two-domain construct, with a WT linker and a Gly6 linker | NMR RDCs (WT) and SAXS (both constructs) | Back-calculation of RDCs from an alignment model, and SAXS profile calculation (hydration-layer parameters) | χ² fit to RDC and SAXS data; kernelised distance to continuous orientation distributions fitted to the data | Low (blind). The forward-model parameters themselves are free choices | Predictioncenter; preprint | AB https://doi.org/10.1101/2025.04.27.650885 |
| **CASP17 Ensembles** (season ended 2026-08-31; conference Rome, 1–5 Dec 2026) | Two types: (i) a few discrete states with good structures; (ii) agreement with low-resolution data (cryo-ET, SAXS, NMR RDCs and chemical shifts, FRET, cross-linking) | As listed | Observable back-calculation for type (ii) | Not yet published. The official page says results go online shortly before the meeting; one message-board post said 29 Nov | Blind | predictioncenter.org | OP https://predictioncenter.org/casp17 |
| **UNICORNE / UNICORNE-BENCH-1** (NeurIPS 2026) | Recovery of PDB-observed multi-conformation ensembles from sequence | More than 50,000 per-protein ensembles of PDB structures; 829 proteins in the benchmark (a search snippet said 839) | None | New multi-conformation recovery metrics (not named on the page) | High. PDB states are in the training sets of most predictors, so a temporal split is essential. A set of PDB states is not a Boltzmann ensemble | unicornedb.org; GitHub OliverLaboratory/UNICORNE-BENCH; licence not verified | AB https://neurips.cc/virtual/2026/poster/138904 |
| **ProteinConformers** (NeurIPS 2025 D&B) | Diversity and plausibility of conformations | More than 381,000 conformations for 87 CASP targets | None | Distance and orientation statistics | Unknown | Not verified | SN https://neurips.cc/virtual/2025/poster/121755 |
| **ATLAS** (Vander Meersche et al., NAR 2024) | Flexibility of PDB chains under MD | MD of 1,390 non-membrane chains; CHARMM36m force field (from the download page); 3×100 ns per chain (secondary source only) | None if MD is the reference. It is a force-field ensemble, not experiment | RMSF, pairwise RMSD, PCA overlap (as used by AlphaFlow and others) | High. AlphaFlow, BioEmu and others train or test on ATLAS splits. 300 ns is far short of equilibrium for slow motions | CC-BY-NC 4.0 (site statement) | SN https://www.dsimb.inserm.fr/ATLAS ; https://doi.org/10.1093/nar/gkad1084 |
| **mdCATH** (Mirarchi, Giorgino, De Fabritiis, Sci Data 11:1299, 2024) | Thermal unfolding and dynamics across CATH domains | 5,398 domains × 5 temperatures (320–450 K) × 5 replicas; coordinates and forces every 1 ns; more than 62 ms in total | None (force-field reference) | Unfolding curves, RMSF, a training target for ML force fields | High as a training set. High-temperature unfolding reflects the force field, not experimental Tm | Licence not verified | AB https://doi.org/10.1038/s41597-024-04140-z |
| **D. E. Shaw Research long trajectories** (fast folders, Lindorff-Larsen et al., Science 2011; BPTI ms trajectory, Shaw et al., 2010) | Folding and unfolding equilibria and kinetics in one force field | µs–ms trajectories | None (force-field reference) | MSM timescales, ΔG of folding from state populations | High. These trajectories are in the training data of many generators, including BioEmu's MD corpus (self-reported) | On request from DESRES under a research licence | MEM |
| **MISATO** (Siebenmorgen et al., Nat Comput Sci 2024) | Protein–ligand MD and QM | MD of PDBbind complexes | n/a | n/a | n/a | Not verified | MEM |
| **PED** (PED 4.0, Lazar et al., NAR 2021) | IDP ensembles | 162 entries and 242 ensembles at the time of the paper, each with metadata on the experimental restraints used | Each entry is already model plus data. Comparing to it is model-to-model unless you go back to the raw SAXS or NMR data | Rg distributions, contact maps | Ensembles are underdetermined; several PED ensembles fit the same data | Open (licence not verified) | AB https://doi.org/10.1093/nar/gkaa1021 |
| **SASBDB** | Solution scattering | I(q) with error bars; Rg | CRYSOL, FoXS, Pepsi-SAXS. Hydration shell and excluded volume are free parameters | χ², Rg error | Low | Open | MEM |
| **BMRB** | Chemical shifts, RDCs, relaxation, PREs | Experimental NMR observables | Shift predictors (SHIFTX2, SPARTA+; prediction errors comparable to the signal for some nuclei); RDC alignment model; relaxation needs dynamics (timescales) | RMSE against shift-predictor error, Q-factor | Low | Open | MEM |
| **Apo/holo and fold-switch sets** (Saldaño et al., Bioinformatics 2022; Porter-lab fold-switch set of about 92 proteins; CoDNaS; PDBFlex; OC23 open/closed set) | Alternative states | PDB pairs | None | TM-score to each state | Very high. Chakravarty et al. (2024) show AF2 "successes" on fold switchers are largely memorisation (see §3) | Open | Fold-switch: AB https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11344769/ ; others MEM |
| **Cryptic-pocket sets** (ensemble evidence only) | Whether transient pockets are sampled | apo/holo PDB pairs | Pocket detection | Pocket recovery | Holo structures are in the training data | Varies | MEM |
| **HDX benchmarks** (Start2Fold-derived set of 38 proteins, JCTC 2021; a 10-protein protection-factor set, 2022) | Local stability and solvent protection | Protection factors (HDX-NMR, residue level) or peptide uptake (HDX-MS) | Empirical protection-factor model (Best–Vendruscolo type) with free parameters; HDX-MS requires deconvolution from peptides to residues | Correlation of log P | I found no community HDX ensemble benchmark (§5) | Start2Fold open | SN https://research.cbc.osu.edu/lindert.1/wp-content/uploads/2021/04/acs.jctc_.1c00077.pdf |
| **CryoBench** (Jeon et al., NeurIPS 2024 D&B) | Recovery of heterogeneity in cryo-EM reconstruction | 5 **synthetic** datasets with ground-truth volumes (IgG-1D/RL, Ribosembly, Tomotwin-100, Spike-MD with more than 46,000 MD structures) | Image formation is simulated, so ground truth is known by construction | Metrics proposed in the paper; 10 algorithms benchmarked | Synthetic, so low leakage; carries a sim-to-real gap | cryobench.cs.princeton.edu | SN https://arxiv.org/abs/2408.05526 |
| **CAID3** (Mehdiabadi et al., Proteins 94:414–424; online 2025-08-26) | Residue-level disorder, binding and linker prediction | DisProt annotations added between Dec 2023 and Jun 2025. Disorder-NOX (204 proteins), Disorder-PDB (319), Binding (52), Binding-IDR (52), Linker (31) | None | AUC, APS, Fmax, DeLong tests | Temporal holdout, but annotations come from the literature and are incomplete | caid.idpcentral.org | FT https://pmc.ncbi.nlm.nih.gov/articles/PMC12750029/ |
| **DisProt** | Curated experimental disorder | Literature-based annotations | n/a | n/a | Incomplete. False "negatives" lower precision (CAID3 authors) | CC-BY (not verified) | MEM |
| **Tsuboyama et al. mega-scale stability** (Nature 620:434, 2023) | Folding ΔG of fixed sequences (wild types and point and double variants) | About 776,000 high-quality ΔG values; domains of 40–72 aa; usable range about 5 kcal/mol; ΔG from trypsin vs chymotrypsin R = 0.94; Pearson above 0.75 against purified-protein literature ΔG for 1,188 variants of 10 proteins; about 22 °C | The model assumes cleavage in the unfolded state, two-state cooperative folding and equilibrium. Stability is underestimated if the folded state is cleaved | Pearson/Spearman, RMSE on ΔΔG | ThermoMPNN, RaSP-like models and BioEmu train on it (self-reported), so it can only serve as an independent test with a split by domain or homology | CC BY 4.0 article; Zenodo 10.5281/zenodo.7401275 (record not opened) | FT (partial) https://pmc.ncbi.nlm.nih.gov/articles/PMC10412457/ |
| **ProThermDB, ThermoMutDB, FireProtDB** | Literature ΔG, ΔΔG, Tm | Heterogeneous conditions, sign conventions and errors | n/a | n/a | Duplicates and inconsistent signs. S669 curation changed about 20% of ΔΔG values | Open | MEM (S669 curation figure: SN) |
| **S669** (Pancotti et al., Brief Bioinform 2022), **Ssym**, **S2648** | Single-mutant ΔΔG test sets | S669 = variants from ThermoMutDB in proteins with less than 25% identity to S2648, plus reverse variants for antisymmetry | n/a | Pearson, RMSE, antisymmetry bias | Leakage against newer training sets (Tsuboyama, FireProt) is not guaranteed to be absent. Destabilising variants dominate the sets | Supplementary data | SN https://pmc.ncbi.nlm.nih.gov/articles/PMC9849384 |
| **Meltome Atlas** (Jarzab et al., 2020) | Proteome thermal stability in cells or lysates | Melting points from TPP-MS | Not an equilibrium ΔG. It mixes aggregation and unfolding | n/a | n/a | Open | MEM |
| **Alchemical binding sets**: OpenFE industry benchmark (about 1,700 ligands; 59 public sets that re-run the Ross et al. 2023 Schrödinger FEP+ set); SAMPL9 host–guest | **Binding-affinity benchmarks**: retrospective evidence on molecular interactions only, not fixed-protein thermodynamics | ΔG_bind from ITC or other assays | Free-energy perturbation (FEP) protocol plus force field | RMSE, Kendall τ. SAMPL9 best RMSE: WP6 about 1.7–2.0 kcal/mol; bCD about 1.86 kcal/mol | Public sets were used for parameter tuning | Zenodo, readthedocs | OpenFE: SN https://industrybenchmarks2024.readthedocs.io/en/latest/public/overview.html ; SAMPL9: SN https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10954238/ |
| **PFDB** (Manavalan, Kuwajima, Lee, Sci Rep 2019) | Folding rates | ln k_f for 141 single-domain proteins (89 two-state, 52 non-two-state), corrected to 25 °C with an Eyring–Kramers model; proteins with disulfides or prosthetic groups excluded | Rate theory with an unknown prefactor | Correlation of ln k | The temperature correction is itself a model assumption | lee.kias.re.kr | SN https://pmc.ncbi.nlm.nih.gov/articles/PMC6367381 |
| **KineticDB, ACPro** | Folding kinetics | Rates | as above | as above | Overlap with PFDB | Not verified | MEM |

## 2. Method table

"Fair comparison" gives the conditions under which a head-to-head comparison is defensible.

| Method | Problem | Version / date | Evidence (I = independent, S = self-reported) | Availability | Compute / assumptions / limitations | Fair comparison possible? | Read level + URL |
|---|---|---|---|---|---|---|---|
| **BioEmu (BioEmu-1)** | Equilibrium backbone ensembles of monomers | Science 389(6761), 2025 (DOI 10.1126/science.adv9817); preprint Dec 2024; later point releases not verified | S: relative free energies within about 1 kcal/mol of ms MD and experiment; cryptic pockets and domain motions. I: Otten, Leung, Chong & Zuckerman (bioRxiv 2026-05-30) find BioEmu, AFsample2 and ESMFlow give *clearly distinct* distributions, small or negligible shifts for known large-effect mutations, and they state that no tool can be declared best. A 2026 survey notes recall-oriented benchmarks can miss spurious flexibility | Open code (MIT, not verified for v1); ColabFold; Azure | Single GPU, thousands of samples per hour (S). Trained on MD, PDB and Tsuboyama ΔG, so there is leakage against those references | Yes, with matched reference MD (same force field, temperature and length) and holdout by sequence identity and date. Not on Tsuboyama or DESRES sets that it trained on | OP https://www.microsoft.com/en-us/research/?p=1143884 ; SN https://sciety.org/articles/activity/10.64898/2026.05.29.728804 |
| **BioEmu2** (successor) | All-atom ensembles and "time-lagged" trajectories for proteins, nucleic acids, ligands and complexes | Checkpoint name "bioemu2-preview". Model card: about 500M parameters, trained Aug–Sep 2026, released Oct 2026, MIT licence | S only. The card lists evaluation categories but I saw no numbers. **The card states that sampling frequency is not a calibrated Boltzmann probability or free energy** | github.com/microsoft/bioemu2; HF microsoft/bioemu2 (several third-party HF mirrors exist) | 80 GB A100 is the smallest tested device; Linux and NVIDIA only | Only as a structure-diversity generator. Its own card says not to treat it as a thermodynamic model. No independent evidence yet | OP https://huggingface.co/microsoft/bioemu2 ; https://raw.githubusercontent.com/microsoft/bioemu2/main/README.md |
| **AlphaFlow / ESMFlow** (Jing et al., ICML 2024) | Flow-matching ensembles from AF2/ESMFold, fine-tuned on ATLAS | 2024 | S: 82 ATLAS test proteins (RMSF, contacts). I: Zuckerman group 2026 (ESMFlow only) | Open | Inherits the ATLAS 300 ns horizon | On ATLAS-like MD with a strict split | SN https://arxiv.org/pdf/2402.04845 |
| **Distributional Graphormer (DiG)** | Equilibrium distributions | Nat Mach Intell 2024 (MEM) | S | Partly open (not verified) | — | Unknown | MEM |
| **AF-Cluster** (Wayment-Steele et al., Nature 2024) | Alternative states by clustering the MSA | 2023/2024 | S: KaiB and others. I (critical): Chakravarty et al. 2024 and a 2025 review attribute its successes to memorisation | Open | AF2 compute | Only on post-training-cutoff fold switchers | SN https://www.nature.com/articles/s41586-023-06832-9 |
| **AF2 MSA subsampling / AFsample2** (Kalakoti & Wallner, Commun Biol 8:373, 2025) | Alternative states by random MSA column masking | 2025 | S: OC23 set, alternative state improved in 17 cases. I: CASP16 assessors found the best groups used enhanced MSAs and AF2 sampling followed by quality-based selection | Open (pip) | Many AF2 runs | CASP-style blind targets | SN https://github.com/iamysk/AFsample2 ; CASP: AB https://doi.org/10.1002/prot.70065 |
| **Cfold** (Bryant & Noé, 2024) | Alternative states (AF2 retrained on a conformation-split PDB) | 2024 (MEM) | S | Open (MEM) | — | Yes; it was designed with a structural split | MEM |
| **MDGen** (Jing et al., 2024); **Str2Str** (Lu et al., ICLR 2024) | Trajectory generation; zero-shot sampling | 2024 | S | Open (MEM) | — | Against matched MD | MEM |
| **idpGAN, IDPForge, STARLING** | IDP ensembles from sequence | STARLING: bioRxiv Feb 2025 (Novak, Lotthammer, Emenecker, Holehouse); one listing says Nature 652:240–250 (2026), not verified | S (compares to CALVADOS2 and experiments) | STARLING on PyPI (idptools-starling) | Coarse-grained. Trained on simulations from a physics model, so it inherits that model's bias | Against SAXS Rg, PRE and FRET data **not** used to fit the parent force field | SN https://www.biorxiv.org/content/10.1101/2025.02.14.638373 |
| **CALVADOS 2/3; Mpipi** | One-bead-per-residue coarse-grained models for IDPs and multidomain proteins | CALVADOS 3: Cao et al., Protein Sci 2024 (10.1002/pro.5172) | S: re-optimised against SAXS and PRE. A 2025 AF-CALVADOS preprint (same group) claims CALVADOS 3 "performed well in the CASP16 blind assessment", which I did not check against the CASP assessor paper | Open (Zenodo, GitHub) | Cheap. The parameters were fitted to the same kinds of data used to validate them | Only with held-out experimental systems | SN https://zenodo.org/records/14282804 |
| **BME, EROS, metainference, ENSEMBLE, MultiFoXS, "maximum occurrence"** | Reweighting or selecting a prior ensemble against data | Various, 2010–2020 | Mostly S, through case studies | Open | Results depend on the prior and the forward model. The regularisation strength (θ) chooses between overfitting and underfitting | On planted-ground-truth synthetic data (see §4) | MEM |
| **sampleworks** (Chrispens, Collins, Mai, Wankowicz, Fraser, van den Bedem, 2026; diff-use / Astera-funded Diffuse Project) | Guiding generative models (Boltz-1/2, Protenix, RF3, Protpardelle, BioEmu2) with X-ray data (density maps, MTZ amplitudes, diffuse scattering) | No tagged release; DOI 10.82153/jkxj-tw08; "under active development" | None seen. I could not open the release PDF (size limit) | MIT | Some setup is internal to Astera | Not yet. Rfree on held-out reflections would be the natural test | OP https://github.com/diff-use/sampleworks/ |
| **ΔΔG predictors: FoldX, Rosetta cartesian_ddg, RaSP, ThermoMPNN, Stability Oracle, ESM zero-shot** | ΔΔG of fixed variants | Various | Mostly S. On S669 (as tabulated by method papers): FoldX r = 0.22, Rosetta 0.39, RaSP 0.39, ThermoMPNN 0.43 (copied from secondary tables, SN). I: Pancotti et al. 2022 (21 tools; predictions compressed toward zero; stabilising variants hard); Degn et al. (Papaleo lab, bioRxiv 2025), where performance fell on a balanced set and MD ensembles as input helped | Open | Structure input matters (AF vs crystal) | Only with homology-disjoint splits against every training set, balanced stabilising/destabilising classes, and antisymmetry checks | SN https://www.biorxiv.org/content/10.1101/2025.03.28.645695v1 |
| **MACE-OFF** (Kovács et al., JACS 147:17598, 2025) | Transferable ML potential for organic molecules (10 elements) | 2025 (preprint versions v1–v5) | S: Ala3 free-energy surfaces, Ala15 folding, ns-scale simulation of a solvated protein | ACEsuit/mace-off | Short-range only, so no long-range electrostatics | Stability-under-MD tests (Fu et al.) plus ensemble tests | SN https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12123624/ |
| **Boltzmann generators** (TBG, Klein & Noé 2024; Sequential BG 2025; Temperature-Annealed BG 2025; Prose 2025) | Unbiased equilibrium sampling with exact reweighting | 2024–2025 | S. Each paper uses its own metric mix (ESS, Wasserstein-2 on energy and dihedral distributions) | Open (mostly) | ESS collapses beyond small peptides (2025 review) | Yes, the exact Boltzmann target makes this possible. Requires a shared force field, shared reference MD and shared ESS definitions | SN https://arxiv.org/pdf/2502.18462 |

## 3. What independent evidence says is strongest, per sub-area

- **Discrete alternative states.** In the independent CASP16 assessment, the most successful approaches generated many AlphaFold2 models from enhanced MSAs and sampling protocols, then selected models by quality. The AF3 server did well on several targets but was beaten in specific cases (Dube et al., 2026, AB). Assessors judged accuracy significantly lower than for single-state targets. Apart from one target that had an apo template, predictors generally failed to capture the details that distinguish the states (AB). The CASP16 overview concludes that without templates "results tend to be poor" (Kryshtafovych et al., 2026, AB, https://doi.org/10.1002/prot.70076). UNICORNE-BENCH (independent of the methods it tests) reports that the best of 8 tools fully recovers 8.2% of ensembles, with MSA-perturbation methods modestly ahead of direct generative models (AB).
- **Fold switching.** Independent evidence (Chakravarty et al., Nat Commun 2024, SN) is negative. AF2 sampled both folds for 32 of 92 fold switchers likely to be in its training set and for 1 of 7 outside it. Its confidence scores select against alternative folds.
- **Ensembles judged against solution data.** The one independent blind test (CASP16 D-L-D) found no submission close to the combined RDC and SAXS data, and none reproduced the WT vs Gly6 linker difference (AB). **No independent evidence yet shows that any ML ensemble generator reproduces solution observables better than physics-based MD.** CASP17 type-(ii) results were not yet public on the access date.
- **ML equilibrium emulators (BioEmu and others).** The only head-to-head comparison I found (Zuckerman group, 2026 preprint, SN) says the tools disagree with each other and cannot be ranked without ground truth. BioEmu's free-energy accuracy claims are self-reported. BioEmu2 has no independent evidence, and its own card disclaims calibrated probabilities.
- **Disorder (CAID3, independent, FT).** Top methods by AUC: ESMDisPred-2PDB (Disorder-NOX 0.885), PUNCH2 (Disorder-PDB 0.955), DisoFLAG-PB (Binding 0.776), bindEmbed21IDR-rawGeneral (Binding-IDR 0.641), IPA-AF2-Linker (Linker 0.897). The cheap AlphaFold-RSA baseline ranks 3rd on Disorder-PDB (AUC 0.950), so the margin over a structure-derived baseline is small. Binding prediction remains weak (APS 0.245).
- **IDP ensembles.** Independent blind evidence exists only through CASP16 and CASP17, which I did not verify for CALVADOS or STARLING. All other validation is by the developers, often on data overlapping the fitting set.
- **ΔΔG.** Independent evidence (Pancotti et al. 2022; Degn et al. 2025) shows that all tools compress predictions toward zero, perform poorly on stabilising variants, and look worse on balanced sets. **I found no independent homology-split comparison that includes ThermoMPNN, Stability Oracle, RaSP and ESM zero-shot on Tsuboyama-disjoint data.** Leaderboard numbers on S669 come from method papers.
- **Alchemical binding (out of core scope).** The OpenFE industry benchmark is a third-party, multi-partner study. It reports open-source performance approaching commercial ranking power, with FEP+ showing lower error on the 59 public sets (SN, blog). SAMPL9 is independent and blind (SN).
- **ML force-field physical consistency.** Independent benchmark evidence (Fu et al., TMLR 2023, SN): low force error does not imply stable or realistic MD. Stability is the key failure mode. For biomolecule-scale ML potentials (MACE-OFF and others), **no independent stability-under-MD or ensemble-validation benchmark on proteins was found.**
- **Classical force fields against NMR.** Robustelli, Piana & Shaw (PNAS 2018, PMID 29735687; SN/MEM) is self-reported by the developers, but it is the reference comparison across many force fields for folded and disordered systems.
- **Kinetics.** I found no independent blind assessment of computed folding rates. Evaluation practice (VAMP-2 cross-validation, implied-timescale plateaus, Chapman–Kolmogorov tests) is well established within the field (SN).

## 4. Evaluation settings with exact or planted ground truth vs underdetermined settings

**Exact or planted ground truth (most valuable for certification):**
1. **Lattice proteins** (e.g. 2D HP or 3D 27-mers) with exhaustive enumeration give the exact partition function, density of states, ΔG and Tm. These are exact tests for samplers and generators (MEM; standard textbook systems).
2. **Boltzmann-target sampling on a fixed force field.** For alanine dipeptide or tetrapeptide, chignolin and similar systems, the target density is known up to Z, and long MD or umbrella sampling gives near-exact free-energy differences. Score with ESS, a reweighted ΔF error and W2 on energy and torsion distributions. Shared protocols are currently missing (SN).
3. **Matched-force-field MD references** (DESRES trajectories, mdCATH, ATLAS). The ground truth here is *the force field's* ensemble, so the test can certify emulation only, not experimental fidelity. Results depend on duration and temperature.
4. **Synthetic forward-model tests.** Generate an ensemble, back-calculate SAXS, RDC and chemical-shift data with known noise, then test whether reweighting methods (BME, metainference) recover the planted weights. Exact by construction.
5. **CryoBench synthetic image stacks.** Ground-truth volumes are known (SN).
6. **`physical_validation`** (Merz & Shirts 2018; JOSS 2022; PyPI 1.0.5; used in GROMACS release testing). It provides exact statistical-mechanics tests: the kinetic-energy distribution against Maxwell–Boltzmann, equipartition, ensemble tests from two state points (NVT, NPT, μVT), and integrator convergence (SN). These tests apply to MD engines and can be adapted to ML potentials. They do not apply directly to non-dynamical generators.
7. **Exact physical symmetries.** ΔΔG antisymmetry (forward vs reverse variant) and thermodynamic-cycle closure in FEP.

**Underdetermined (identifiability caveats):**
- SAXS: a 1D curve fits many ensembles. Hydration-shell parameters can absorb errors.
- RDCs: depend on alignment-tensor assumptions. The CASP16 D-L-D result shows RDC and SAXS data are complementary, and neither suffices alone.
- Chemical shifts: errors of the forward model are comparable to the conformational signal.
- PED ensembles: one deposition among many that fit the data. Use the raw data, not the ensemble, as ground truth.
- PDB alternative states: they show that states exist, not their populations. They are not Boltzmann weights.
- HDX: protection-factor models carry free parameters, and HDX-MS adds peptide-level averaging.
- Proteolysis ΔG (Tsuboyama): limited to two-state behaviour, about 5 kcal/mol of range and small domains.
- Folding rates: the prefactor (attempt frequency, Kramers friction) is unknown, so only relative rates, ln k trends or ratios are testable without a calibrated prefactor. MD rates also depend on water-model viscosity.
- Meltome Tm: mixes aggregation with unfolding, so it is not a ΔG.

## 5. Could-not-verify list and open questions

- CASP17 ensemble results and the assessor's conclusions (not public on 2026-11-26; expected around 29–30 Nov).
- The sampleworks "CASP ensembles SIG talk (Nov 2026)": **not verified.** No search result linked sampleworks to CASP or a SIG. No validation numbers were seen; the release PDF could not be read.
- BioEmu2 numerical benchmarks, preprint and official release date (dates come from the model card only). No independent evaluation exists.
- Whether BioEmu-1 had versioned updates (e.g. 1.1 or 1.2): not verified.
- The STARLING Nature 2026 citation (snippet only). The CALVADOS 3 CASP16 performance claim (developer-adjacent preprint).
- ATLAS simulation length (3×100 ns: secondary source). Licences for mdCATH, PED and UNICORNE.
- The exact UNICORNE-BENCH method list and metric definitions, and the protein count (829 or 839).
- The OpenFE ChemRxiv preprint's title and DOI.
- CAID3 results are complete. A CAID4 round, if one exists, was not checked.
- No community HDX ensemble benchmark was found. No independent protein-scale stability benchmark for ML potentials was found. No independent homology-disjoint ΔΔG comparison including Tsuboyama-trained models was found.
- All rows marked MEM (DESRES, MISATO, SASBDB, BMRB, DiG, Cfold, MDGen, Str2Str, reweighting methods, Meltome, ProThermDB, ThermoMutDB, FireProtDB, KineticDB, lattice-protein references) need primary-source verification before they enter the register.
- Open question: how to set a fair matched-reference protocol for ML emulators (force field, temperature, trajectory length, sequence-identity and date holdout). The BBFlow 2025 authors and the Zuckerman group 2026 both flag this.

## 6. Sources (all accessed 2026-11-26)

| URL | Title | Read level |
|---|---|---|
| https://doi.org/10.1002/prot.70065 | Dube et al., Modeling Alternative Conformational States in CASP16 (Proteins 2026) | AB (PubMed) |
| https://doi.org/10.1101/2025.04.27.650885 | McBride et al., Predicting pose distribution of domains connected by flexible linkers is an unsolved problem | AB (PubMed) |
| https://doi.org/10.1002/prot.70076 | Kryshtafovych et al., CASP Round XVI overview | AB (PubMed) |
| https://doi.org/10.1002/prot.70059 | Wuyun et al., EnsembleFold in CASP16 (self-reported) | AB |
| https://predictioncenter.org/casp17 | CASP17 home page | OP |
| https://neurips.cc/virtual/2026/poster/138904 | UNICORNE Protein Conformation Database | AB |
| https://neurips.cc/virtual/2025/poster/121755 | ProteinConformers | SN |
| https://www.microsoft.com/en-us/research/?p=1143884 | BioEmu project page | SN/OP |
| https://huggingface.co/microsoft/bioemu2 | BioEmu-2 model card | OP |
| https://raw.githubusercontent.com/microsoft/bioemu2/main/README.md | BioEmu2 README | OP |
| https://sciety.org/articles/activity/10.64898/2026.05.29.728804 | Otten et al., Comparison of AI protein structure ensemble prediction tools | AB (listing) |
| https://arxiv.org/html/2604.25244 | Tang et al., Survey of AI for protein dynamics | FT (partial) |
| https://arxiv.org/pdf/2509.17224 | AI-based methods for simulating, sampling, and predicting protein ensembles | SN |
| https://github.com/diff-use/sampleworks/ | sampleworks repository | OP |
| https://www.news.cornell.edu/stories/2025/08/philanthropic-support-accelerates-infrastructure-future-structural-biology | Diffuse Project funding (Astera) | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC12750029/ | Mehdiabadi et al., CAID3 (Proteins 2025) | FT |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC10412457/ | Tsuboyama et al., Mega-scale stability (Nature 2023) | FT (partial) |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC9849384 | Pancotti et al., S669 (Brief Bioinform 2022) | SN |
| https://www.biorxiv.org/content/10.1101/2025.03.28.645695v1 | Degn et al., Stability predictors on balanced data | AB |
| https://link.springer.com/10.1038/s41467-024-49780-2 | Stability Oracle (Nat Commun 2024) | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC10266766/table/table2 | RaSP table (S669 comparison) | SN |
| https://doi.org/10.1038/s41597-024-04140-z | mdCATH (Sci Data 2024) | AB |
| https://www.dsimb.inserm.fr/ATLAS | ATLAS database | SN |
| https://doi.org/10.1093/nar/gkaa1021 | PED 4.0 (NAR 2021) | AB |
| https://arxiv.org/abs/2408.05526 | CryoBench | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11344769/ | Chakravarty et al., AF fold-switch predictions driven by memorization | SN |
| https://arxiv.org/pdf/2507.10839 | Fold-switching proteins review (2025) | SN |
| https://www.nature.com/articles/s41586-023-06832-9 | Wayment-Steele et al., AF-Cluster | SN |
| https://github.com/iamysk/AFsample2 | AFsample2 | SN |
| https://arxiv.org/pdf/2402.04845 | AlphaFlow | SN |
| https://www.biorxiv.org/content/10.1101/2025.02.14.638373 | STARLING | SN |
| https://zenodo.org/records/14282804 | CALVADOS 3 data and code | SN |
| https://www.biorxiv.org/content/10.1101/2025.10.19.683306 | AF-CALVADOS | SN |
| https://arxiv.org/abs/2210.07237 | Fu et al., Forces are not Enough | SN |
| https://physical-validation.readthedocs.io/en/stable/userguide.html | physical_validation docs | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12123624/ | MACE-OFF (JACS 2025) | SN |
| https://arxiv.org/pdf/2406.14426 | Transferable Boltzmann Generators | SN |
| https://arxiv.org/pdf/2502.18462 | Sequential Boltzmann Generators | SN |
| https://arxiv.org/html/2501.19077v2 | Temperature-Annealed Boltzmann Generators | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC6367381 | PFDB (Sci Rep 2019) | SN |
| https://arxiv.org/pdf/1811.11714 | Variational selection of features for molecular kinetics (VAMP-2 practice) | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10954238/ | SAMPL9 host–guest overview | SN |
| https://industrybenchmarks2024.readthedocs.io/en/latest/public/overview.html | OpenFE industry benchmark, public sets | SN |
| https://omsf.substack.com/p/the-free-energy-of-everything-benchmarking-openfe | OpenFE benchmarking blog | SN |
| https://research.cbc.osu.edu/lindert.1/wp-content/uploads/2021/04/acs.jctc_.1c00077.pdf | HDX-NMR benchmark (JCTC 2021) | SN |
| https://pubmed.ncbi.nlm.nih.gov/29735687/ | Robustelli, Piana, Shaw, PNAS 2018 (a99SB-disp) | SN (PubMed ID only) |
