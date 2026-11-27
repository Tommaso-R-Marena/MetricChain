> **Provenance.** Report of a literature assessor (a subagent of the Frontier Benchmarking division,
> model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from this
> notice.  Every row carries a *read level*; rows marked "search snippet" or "from memory" are
> unverified leads, not findings.  The coordinator read this report in full, checked none of its
> sources independently unless `../STATE_OF_THE_ART.md` or `../BENCHMARK_REGISTRY.md` says so, and
> carries the read levels forward wherever a row is used.  Out-of-charter items (sequence or
> molecule design, target-specific optimisation) are listed only to mark the boundary.

# Evidence register: geometric inverse problems, electrostatics/solvation, retrospective cavities, validation standards

Assessor run 2026-11-26. About 45 web calls. Read levels: **FT** = full text read (FT-partial = only part of the text was read), **AB** = abstract or landing page read, **OP** = official page read (including PyPI JSON metadata), **SN** = search snippet only, **MEM** = from memory, not verified. "Indep." means a blind challenge or third-party benchmark. "Self" means the developers evaluated their own method. Anything marked SN or MEM needs a primary-source check before it goes into the registry.

---

## 1. Benchmark and reference-data table

| Name | Scientific question | Reference evidence and its quality | Forward model / ground truth | Metrics | Contamination / leakage risk | Charter | Access | URL + read level |
|---|---|---|---|---|---|---|---|---|
| DMDGP / MDGP PDB-derived instances (Lavor, Liberti, Maculan, Mucherino) | Realise a 3-D embedding from exact or interval distances under a vertex order | Instances are built from PDB models (taken as ground truth). Some use simulated "NMR-like" distances (pairs under about 5-6 Å). A 2021 line mixes real NMR distances with simulated ones | Planted solution = the PDB coordinates. Intervals are generated synthetically around true distances. Under the discretisation assumptions the solution set is finite (2^k, with symmetry) | RMSD to planted model (after alignment), LDE/MDE distance-error measures, number of solutions found, CPU time | Instances are synthetic, so contamination is low. The weakness is realism: distances are noise-free or have artificial intervals. No standard community instance repository was found for 2023-2026 | In scope (synthetic control) | Instances are scattered across papers and the MD-jeep distribution | https://arxiv.org/abs/q-bio/0608012 (SN). https://www.lix.polytechnique.fr/~liberti/dmdgp-survey.pdf (SN). arXiv 2510.19970 (Oct 2025 hybrid solver; SN) |
| DISCO / SDP anchor-free graph realisation test sets | Recover protein structure from sparse, noisy short-range distances | PDB molecules are the ground truth. Leung & Toh report reliable recovery with 20-30% of distances under 6 Å under "high" noise | Planted PDB coordinates with multiplicative noise | RMSD | Synthetic. Noise models differ between papers, so results are not comparable without re-running | In scope | MATLAB code (licence not verified) | https://dspace.mit.edu/handle/1721.1/58306 (SN). Uwaterloo SPROS preprint (SN) |
| CASD-NMR 2010 and 2013 | Can automated protocols reproduce expert NMR structures from blind data? | 10 blind targets per round (60-150 aa, NIH PSI). 2013: 164 entries; 71% of entries < 1.5 Å and over 90% < 2.5 Å from the reference NMR structure | The reference is itself an NMR model, i.e. an estimate, not ground truth | Backbone RMSD to reference, RPF/DP scores, validation scores | Targets are now in the PDB, so they are no longer blind. No round after 2013 was found | In scope (inverse-problem benchmark) | Data via BMRB/CASD pages (not verified) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4569658 (SN). Ragan et al. J Biomol NMR 2015 (SN) |
| ARTINA 100-protein NMR spectra set (Klukowski, Riek, Güntert 2022) | Raw spectra to assignment to structure | 1,329 spectra, 100 proteins (35-175 aa). Self-reported median backbone RMSD 1.44 Å to the PDB reference and 91.4% correct assignments | Same issue: the reference is a deposited NMR structure | RMSD, assignment accuracy | ARTINA was trained and tested on overlapping lab-collected data (split details not verified) | In scope | Release status of the spectra not verified | https://pmc.ncbi.nlm.nih.gov/articles/PMC9579175 (SN) |
| wwPDB NMR restraint archive (NEF / NMR-STAR, remediated) + Restraint Violation Report | Model-versus-restraint consistency for every NMR entry | Archive-wide. Distance and dihedral restraints are validated; other restraint types are "being added". Remediated legacy entries | Deposited restraints are the "data". Ambiguous and overlapping assignments complicate violation analysis | Violation counts and magnitude by restraint type | No leakage concept applies. Restraints were produced by the depositors' own protocols | In scope | Open (PDB) | Baskaran et al. Structure 2024, https://pubmed.ncbi.nlm.nih.gov/38490206/ (SN) |
| EMDataResource 2019 Model Metrics Challenge | How reproducible are models from maps, and which metrics are informative? | 4 targets at 1.7-3.3 Å. Many coordinate-only and map-model metrics compared. Q-score and CaBLAM came out of this round | Reference models; no absolute ground truth | Q-score, FSC-Q, CC, EMRinger, MolProbity terms, CaBLAM, etc. | Public since 2021 | In scope | Open (challenges.emdataresource.org; not verified) | Lawson et al. Nat Methods 18:156 (2021), https://pubmed.ncbi.nlm.nih.gov/33542514/ (SN) |
| EMDataResource 2021 Ligand Model Challenge | Reliability of ligand modelling into cryo-EM maps | Published in Nat Methods 21:1340 (2024). Concludes that a composite score is needed. Introduces LIVQ scores | Reference ligand models | Map-fit, geometry, energetics, contact scores | Public | **Descriptive-only** (ligand fit evaluation; not ligand design) | Zenodo dataset 10551958 | https://pubmed.ncbi.nlm.nih.gov/38343795/ (SN). https://zenodo.org/records/10551958 (SN) |
| CryoBench (NeurIPS 2024 D&B) | Conformational and compositional heterogeneity reconstruction | Synthetic. 5 datasets: IgG-1D/IgG-RL designed motions, Ribosembly, Tomotwin-100 mixtures, Spike-MD with over 46k MD structures. Noisier variants included | Exact: simulated projections from known volumes, with known pose and state labels | Per-image volume error (FSC/AUC-FSC against the true state), latent-space metrics | Synthetic, so no leakage. Simulator realism (CTF, noise) bounds how far results transfer | In scope (exact ground truth) | Open (Zenodo via project page; licence not verified) | https://arxiv.org/abs/2408.05526 (SN). https://cryobench.cs.princeton.edu/ (SN) |
| SHREC 2020/2021 cryo-ET | Localisation and classification of 12 complexes in simulated tomograms | Simulated cell-like volumes with the coordinates used in simulation released. Sources disagree on the count (9 vs 10 tomograms) | Exact planted particle positions and classes | F1, localisation precision | Synthetic | In scope | Open | https://arxiv.org/abs/2203.10035 (SN) |
| CZII cryo-ET object identification Kaggle challenge (2024-25) | Particle picking in **experimental** tomograms | Nearly 500 annotated tomograms, 5 scored targets. Results preprint 2025-11 (bioRxiv 10.1101/2025.11.03.686153). Winning maps deposited in EMDB (e.g. EMD-73635, EMD-73637) | Ground truth is human/computational annotation, so it is uncertain (procedure not read) | F-beta (beta value not verified) | Top solutions tuned to the leaderboard | In scope | CZ cryoET Data Portal (licence not verified) | bioRxiv full text: fetch failed (HTTP 429), so SN only |
| SASBDB | Repository of curated SAXS/SANS curves with models | Curated experimental curves. Models often fitted with a single forward calculator | Forward calculators disagree (Section 5) | chi², CorMap | Deposited models were fitted to the deposited curve, so the curve is not an independent test | In scope | Open | https://www.sasbdb.org (MEM) |
| smFRET multi-lab benchmarks | Accuracy and precision of FRET-derived distances | Indep. blind: 20 labs on DNA (Hellenkamp 2018, Nat Methods 15:669), spread ±0.02-0.05 in E. 19 labs on proteins (Nat Methods 2023, 10.1038/s41592-023-01807-0): ΔE ≤0.06, about 2 Å precision, about 5 Å accuracy | Dye-linker forward models (accessible-volume) | E, distance error | Low | In scope | Open | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6121742/ (SN). https://link.springer.com/10.1038/s41592-023-01807-0 (SN) |
| FreeSolv v0.52 (Zenodo, 2018-01-26) | Small-molecule hydration free energies | 642 molecules. Mean experimental uncertainty 0.57 ± 0.31 kcal/mol (range 0.03-1.93). Literature-curated | Experiment. Calculated values come from a single-protocol MD set | RMSE, MUE vs experiment | Very widely used for fitting, so implicit-solvent parameters are often tuned to it | In scope (solvation physics) | Open (GitHub MobleyLab/FreeSolv; licence not verified) | https://zenodo.org/records/1161245 (SN) |
| PKAD-3 (2024-25) | Protein residue pKa | 1,167 pKa values, 992 residues, 247 proteins. Enriched with large pKa shifts | Experiment (NMR/titration), heterogeneous conditions | RMSE, MAXE vs null model (model pKa) | Random residue-level splits, not sequence splits (Section 2) | In scope | database.computchem.org/pkad-3 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11601431.3 (FT-partial) |
| PKAD-R (2025) | Curated successor to PKAD/PKAD-2 | 868 WT + 144 mutant entries (per project page). J Comput Biophys Chem 2025 | Experiment | as above | not verified | In scope | Web server (Clemson) | https://sites.krieger.jhu.edu/damjanovic-lab/pkad-r/ (SN) |
| pKa Cooperative blind challenge (SNase variants; Proteins 79(12) 2011) | Blind prediction of buried/internal pKa | Indep. blind. Garcia-Moreno lab measurements. Called "the most challenging pKa data" | Experiment | RMSD | Data are now public, so the benchmark is no longer blind | In scope | Proteins special issue | https://pmc.ncbi.nlm.nih.gov/articles/3243943 (SN) |
| LIGYSIS (Utgés & Barton, J Cheminform 16:126, 2024) | Do binding-site predictions match **aggregated** observed ligand sites? | About 30k proteins in full. Human subset 2,775 chains, 8,244 sites (about 40% ions). Uses biological assemblies (PISA), BioLiP relevance filter, and fingerprint clustering of ligands across all structures of a protein | Ground truth = union of observed biologically relevant ligand sites. Unobserved sites count as false positives | top-N+2 recall at DCC 12 Å (recommended), precision, RRO/RVO, residue-level F1/MCC, redundancy | Methods trained on sc-PDB/PDBbind/HOLO4K overlap human PDB entries, so a fair test needs temporal or homology filtering (not done in the paper) | **Descriptive-only**: compare a geometric cavity characterisation with annotated sites. Crossing point: using it to rank sites for ligand design | CC-BY paper. Data/code licence not verified (Zenodo 14645504 holds the results) | https://pmc.ncbi.nlm.nih.gov/articles/PMC11552181 (FT-partial, first ~100k chars) |
| HOLO4K, COACH420 (P2Rank sets) | Ligand-site prediction | Single-structure, ligand-defined sites | Critiqued in LIGYSIS: asymmetric units rather than assemblies (about 40%/56% chain-count mismatch), one complex per protein | DCA 4 Å top-n / top-n+2 | Heavy redundancy and train overlap | Descriptive-only | Open | LIGYSIS critique (FT-partial). Original sets: Krivák & Hoksza 2018 (MEM) |
| sc-PDB, PDBbind (as annotated structures) | Druggable-cavity / complex sets | sc-PDB keeps one ligand per entry. PDBbind has one complex per protein in many cases | as above | — | Leakage (row below) | Descriptive-only | sc-PDB open. PDBbind licence changed to registration/commercial terms (MEM, not verified) | LIGYSIS (FT-partial) |
| BioLiP2 (NAR 52:D404, 2024) | Biologically relevant ligand–protein interactions | Weekly updates. Site lists a version dated 2025-02-22. Rule-based plus literature filtering of additives. Open curation code | Annotation is rule-based; additive filtering is imperfect | — | Not a benchmark itself | In scope (annotation source) | Open | https://academic.oup.com/nar/article/52/D1/D404/7233921 (SN) |
| CryptoBench (Bioinformatics 41(1), 2025) | Cryptic sites from apo structures | 1,107 structures from apo–holo pairs, predefined cross-validation splits. Baselines: P2Rank and PocketMiner | Ground truth = holo ligand site plus a structural-change criterion | AUC, AUPRC | Splits are by sequence clustering. Apo choice is subjective | Descriptive-only | Open (OSF/GitHub; not verified) | https://pmc.ncbi.nlm.nih.gov/articles/PMC11725321/ (SN) |
| PocketMiner set (Meller et al. 2023) | Cryptic pockets | Only 39 cryptic pockets. Self-reported ROC-AUC 0.87 | MD-derived plus holo | ROC-AUC | Small, so variance is high | Descriptive-only | Open | https://pmc.ncbi.nlm.nih.gov/articles/PMC9977097 (SN) |
| M-CSA, PDBe-KB | Catalytic residues / aggregated functional annotation | Literature-curated mechanisms (M-CSA). Aggregated site annotations (PDBe-KB) | Expert curation | — | — | In scope (annotation) | Open | MEM |
| PDBbind + CleanSplit / LP-PDBbind | Affinity data as a physics test bed; leakage | CleanSplit (Graber et al., Nat Mach Intell 2025, 10.1038/s42256-025-01124-5): top models' benchmark performance drops substantially after leakage removal, i.e. CASF performance is "largely driven by data leakage". LP-PDBbind (Li et al.) gives the same message | Measured Kd/Ki/IC50 of mixed provenance | Pearson R, RMSE on CASF | Severe, documented | **Descriptive-only** for retrospective physics checks (e.g. electrostatic terms vs measured ΔG). **Out of scope** for training or optimising affinity predictors | Licence restricted (not verified) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12552120/ (SN). arXiv 2308.09639 (SN) |
| PLINDER (v2 2024-06; PyPI `plinder` 1.0.0, 2026-10-09) / PINDER (PyPI 0.6.0, 2026-09-14) | Protein–ligand / protein–protein complexes with leakage-aware splits | Multi-level similarity (protein, pocket, interaction, ligand). Third-party DataSAIL addendum: PLINDER-PL50 split scaled leakage 0.0678; PINDER split leaks less than DataSAIL's | Structures | — | Splits are the main asset | Descriptive-only (structural annotation). Out of scope for docking-design campaigns | Open (Apache-2.0 per MEM, not verified) | https://www.biorxiv.org/content/10.1101/2024.07.17.603955 (SN). https://pypi.org/project/plinder/ (OP) |
| Co-folding physical-plausibility critiques | Do AF3-class models respect physics? | Indep.: Masters et al. Nat Commun 2025 (adversarial binding-site mutations still give confident poses). Mac1 prospective eLife study: over 50% of poses < 2 Å but "pervasive memorization and hallucination". PoseBench (Nat Mach Intell 2025) uses PB-valid with RMSD | Experimental poses | RMSD plus PoseBusters validity | Training-set memorisation | Descriptive-only (as evidence about validation) | — | https://elifesciences.org/articles/110475 (SN). arXiv 2405.14108 (SN) |

---

## 2. Method and tool table

| Tool | Problem | Version / date | Evidence | Availability | Assumptions / limits | Fair comparison possible? |
|---|---|---|---|---|---|---|
| MD-jeep | Branch-and-Prune DMDGP with interval distances (from v0.3.0) | 0.3.2 (GitHub; release date not verified) | Self only | GPL-3 (OP-level snippet of author site) | Needs a discretisation vertex order; exact distances are needed for "reference" vertices | Yes, on planted instances with identical orders and interval widths |
| DISCO (Leung & Toh 2009) | SDP divide-and-conquer graph realisation | No versioned release | Self | MATLAB (not verified) | Convex relaxation; output needs refinement | Yes on synthetic instances if the noise model is matched |
| ARTINA / NMRtist | Spectra to structure | 2022 paper; web platform | Self (100-protein set) | Web service | Reference = NMR models | Only on held-out spectra with temporal splits |
| CYANA / ARIA / UNIO etc. (CASD-NMR entrants) | Automated NOE assignment and structure | not verified | Indep. (CASD-NMR 2010/2013) | Mixed licences | Small single-domain proteins | Old blind data only |
| CRYSOL / FoXS / Pepsi-SAXS / WAXSiS | SAXS forward models | not verified | Mostly self. FoXS claims better accuracy than CRYSOL on its own set (self). CRYSOL 2 vs CRYSOL 3 differ on RNA | ATSAS (academic licence), FoXS open, WAXSiS web | Implicit hydration with fitted parameters, except WAXSiS (explicit MD solvent) | Only with fitting parameters fixed or reported, the same q-range and the same error model |
| Shanum (ATSAS) | Effective number of Shannon channels | 2015 | Self (simulated noise) | ATSAS | Smooth truncated Shannon expansion | Yes; analytical bodies give a reference |
| FIRST / ProFlex / KINARI | Pebble-game rigidity | not verified | Mostly self/case studies: HDX folding cores (CypA–CsA), NMR-ensemble FIRST vs HDX (Sso AcP). Fox & Streinu 2013: results "depend critically" on how H-bonds and hydrophobics are modelled | FIRST academic; KINARI web | Energy cutoff choice drives results; no community benchmark found | Only with the H-bond/hydrophobic model frozen; validate against HDX rather than B-factors |
| Rosetta KIC loop modelling | Kinematic loop closure | not verified | Self (standard 12-residue loop sets) | Rosetta licence | — | Yes on fixed loop sets (MEM) |
| APBS (+ PDB2PQR) | PB electrostatics (FD multigrid, FE, PBAM/PB-SAM analytic) | APBS 3.4.1 (Apr 2022), the latest tagged release found; unreleased changes on "latest" docs. PDB2PQR 3.8.0 (PyPI, 2026-10-24) | Self plus scattered solver comparisons | BSD-3 (MEM) | FD grid charge-spreading is low-order at dielectric interfaces (reported for DelPhi/UHBD/APBS on Born/Kirkwood) | Yes: Kirkwood sphere, grid sequences, identical radii and surface definitions |
| DelPhi, MIBPB, TABI-PB, AMBER PBSA, PyGBe/bempp | PB by FD / interface method / treecode BEM / BEM | not verified | Mostly self. MIBPB claims to be the only second-order L∞ method with singular charges (self). HOBI-PB claims unmatched Kirkwood accuracy (self) | Mixed (DelPhi has an academic licence) | Surface definition (SES/SAS/Gaussian) dominates differences | Only if surface, radii, ε, ionic strength and boundary conditions are identical. Meshes of FD and BEM are not directly comparable |
| Adjoint a-posteriori PB error estimates (Chaudhry et al. FEM 2017; Ramm-Chaudhry-Cooper BEM 2020; Aksoylu-Holst goal-oriented 2011) | Error in the solvation energy | research codes | Self (numerical validation) | arXiv | These are estimates, **not certified bounds**. Element contributions can cancel | Usable as a reference for "error-aware" claims |
| GB models (GBNSR6, OBC, neck2, GBMV…) | Approximate PB | AMBER (not verified) | Third-party 2025 eight-flavour study using PB as reference (PMC12199658). Onufriev & Sigalov: even perfect Born radii give gross errors with the canonical formula | AMBER/OpenMM (OpenMM 8.6.1, PyPI 2026-09-24) | Accurate solvation energies do not guarantee accurate binding energies | Yes, against a converged PB on the same geometry |
| PROPKA | Empirical pKa | 3.5.1 (PyPI 2024-01-02) | Indep. 2023 benchmark (408 PKAD shifts): "no method outperformed the null hypotheses with confidence"; DeepKa, PKAI+, PROPKA3, H++ "had utility". KaML paper: PROPKA3 RMSE 1.20 vs null 1.27 | LGPL (MEM) | — | Yes, against the null model on a fixed set |
| PypKa | PB/MC pKa | 2.10.0 (PyPI 2022-12-01) | KaML paper: Asp RMSE 1.61 (third-party but not optimal for test sets) | Open | — | as above |
| DeepKa, KaML-CBtree / GAT, pKALM, ANI-2x pKa | ML pKa | KaML: bioRxiv 2024-11, v3 2025-01, later JCTC (details not verified) | KaML self-reported RMSE 0.77 vs PROPKA3 1.20 vs null 1.27 on 20 random 90/10 residue-level splits (**not** sequence splits). ANI-2x training data overlaps the test set | KaMLs GitHub | Residue-level random splits allow homolog leakage | Only with sequence/protein-level hold-out and the null model reported |
| Constant-pH MD (CpHMD) | Physics pKa | various | Repeatedly cited as most accurate physics method. DeepKa paper says it is not beaten (self) | — | Costly | Yes on PKAD subsets |
| fpocket | Geometric (alpha-sphere) pockets | not verified (GitHub blocked) | Indep. in LIGYSIS: fpocket rescored with PRANK gives top-N+2 recall 60.4% (best). Raw fpocket lower | MIT (MEM) | Over-predicts; ranking matters | Yes with a redundancy filter and the same DCC threshold |
| P2Rank / PRANK | ML rescoring of SAS points | 2.5.1 "Latest" (07 Aug; year not shown, likely 2025); 2.5 (04 Nov, likely 2024); 2.6-alpha pre-release | Indep. LIGYSIS; CryptoBench baseline (drops on apo cryptic sites) | MIT (MEM) | Trained on CHEN11 / HOLO4K lineage (MEM) | Yes; check training overlap |
| DeepPocket, PUResNet, VN-EGNN, IF-SitePred, GrASP | DL site prediction | not verified | Indep. LIGYSIS: DeepPocketRESC 58.1%, VN-EGNN 40.9%, PUResNet 41.1%, IF-SitePred 25.7% top-N+2. VN-EGNN 67% redundant predictions | various | Mostly trained on sc-PDB (1:1 sites) | Only after redundancy removal and train/test homology control |
| PocketMiner | Cryptic pockets from apo | 2023 | CryptoBench comparison (third-party, by a P2Rank-affiliated group) | Open | — | Only on the CB-PM subset where it runs |

---

## 3. Reference implementations an evaluation infrastructure must be validated against

| Tool | Current version (verified level) | Where to obtain | Notes for conformance tests |
|---|---|---|---|
| US-align / TM-align / TM-score | Single-file `USalign.cpp`, no version number. Update log latest 2026/05/27 (allows `-mm 1` with `-dir`); 2026/03/28 fix of an `-mm 1` input-order-dependent oligomer bug (OP) | https://zhanggroup.org/US-align/ (OP) | Pin by download date plus checksum. Oligomer results before 2026-03-28 can differ. TM-score ≥0.5 (0.45 RNA) for shared topology. Nature Protocols 2025 paper "in press" (SN) |
| OpenStructure (lDDT, ilDDT, QS-score, lDDT-PLI, BiSyRMSD, `compare-structures`, `compare-ligand-structures`) | 2.12 (2026-08-17); 2.11 (2025-06-16); 2.10 (2025-05-20) (OP). 2.9: lDDT-PLI penalises added model contacts by default. 2.9.1 adds interface lDDT (ilDDT). 2.10: `rm_unk_atoms` default True, entity info read from mmCIF (SN) | https://openstructure.org (OP); git.scicore.unibas.ch/schwede/openstructure | Scores change between minor versions (lDDT-PLI explicitly). Record the version per result. The legacy action is deprecated |
| DockQ v2 | 2.1.3 (PyPI 2024-08-29) (OP). Paper: Bioinformatics 2024, btae586 (SN) | pip `DockQ`; github.com/bjornwallner/DockQ | Automatic chain mapping, Global-DockQ, nucleic acids and small molecules. Validated against v1 on 17,049 CASP15 models (self) |
| LGA / GDT | not verified | predictioncenter.org (MEM) | The CASP reference implementation |
| PoseBusters | 0.6.5 (PyPI 2026-03-07) (OP) | pip `posebusters` | Check names follow the paper (Buttenschoen et al., Chem Sci 2024; MEM). PB-valid can be gamed by post-hoc relaxation (PoseBench, SN) |
| MolProbity (clashscore, Ramachandran, rotamer, CaBLAM) | not verified (GitHub blocked; "4.5.2" not confirmed) | molprobity.biochem.duke.edu; also via Phenix/cctbx | Clashscore = overlaps ≥0.4 Å per 1,000 atoms. CaBLAM targets 2.5-4 Å models (SN) |
| wwPDB validation reports (X-ray, NMR restraint, 3DEM) | Q-score in 3DEM reports since 23 Sept (2022, per page header) (SN). NMR restraint violations (Structure 2024) (SN) | validate.wwpdb.org (MEM) | Use as an external oracle. Acta D 2025: low Q can reflect flexibility or damage, not only poor fit |
| Q-score / MapQ | Pintilie et al. Nat Methods 2020 (SN) | ChimeraX/Chimera plugin | Resolution-dependent expected-Q curve in Acta D 2025 (about 10k map–model pairs) |
| PDB-REDO | not verified | pdb-redo.eu (MEM) | Re-refined X-ray models as a "consistent re-processing" baseline |
| PDB2PQR / APBS | 3.8.0 / 3.4.1 (OP / SN) | pip; GitHub Electrostatics | Pin the force-field and protonation versions; they drive the results |

All GitHub API and HTML access was blocked from this environment (HTTP 403). GitHub-only versions (fpocket, MD-jeep date, MolProbity, KaMLs) therefore remain **not verified**.

---

## 4. Settings with exact or analytically known ground truth

1. **Born ion and Kirkwood dielectric sphere** (off-centre charges; series solution). Kirkwood is the harder test because of singular charges near the interface. Reported FD charge-spreading schemes (DelPhi, UHBD, APBS) are low-accuracy on both (De Gruyter 2014, SN; arXiv 1607.04594, SN). APBS PBAM/PB-SAM give semi-analytic multi-sphere solutions. A strong, cheap conformance suite: grid sequences h→0, observed convergence order, and comparison with the adjoint a-posteriori estimate (arXiv 1702.05196, 2009.11696; SN).
2. **Planted distance-geometry instances**: PDB coordinates give exact distances, then intervals of controlled width. Under DMDGP order assumptions the number of incongruent solutions is known to be a power of 2 (symmetry results; Liberti/Lavor surveys, SN). Ideal for testing identifiability claims (counting solutions) rather than RMSD alone.
3. **Simulated cryo-EM/ET projections**: CryoBench (exact volumes, poses, state labels; Spike-MD with over 46k states), SHREC 2020/21 (exact particle coordinates). The noise and CTF model is known exactly.
4. **SAXS from analytic bodies** (sphere, ellipsoid) and from fixed atomic models with forward-model parameters fixed. Shannon sampling N_S = q_max·D_max/π gives the nominal degrees of freedom. Shanum effective M_S adds noise (IUCrJ 2015, SN; IUCrJ 2026 extension, SN).
5. **Synthetic ensembles with known weights**: simulate averaged SAXS/NMR/FRET from a known MD mixture, then test whether reweighting (BME, metainference, BE-SAXS) recovers the weights. Section 5 gives the expected non-identifiability.
6. **Rigidity**: generic rigidity of bar-joint/body-bar frameworks is exactly decidable (pebble game; Laman/Tay). Ground truth is combinatorial, but mapping proteins to graphs depends on the model (Fox & Streinu 2013, SN).
7. **Structure comparison self-consistency**: identity (TM=1, lDDT=1, DockQ=1), rigid transforms, chain permutations of symmetric homomers (tests chain mapping; see the US-align 2026-03 bug fix).

---

## 5. Where experimental data underdetermine the answer (documented)

- **RDCs**: a single alignment medium leaves a fourfold degeneracy in fragment orientation even with unlimited data. The analytical treatment for a rhombic medium finds up to 16-fold degeneracy for peptide planes. Two media remove it only if their tensors are independent; many common media give near-collinear tensors (tRNA case). Three independent RDC sets allow de novo tensors (Ruan, Briggman & Tolman 2008). Sources: PMC2861045, PMC2846703, Al-Hashimi 2000 (SN).
- **DMDGP**: 2^k symmetric solution sets under discretisation. Reflection ambiguity is inherent to distances (Liberti/Lavor; SN).
- **SAXS**: few Shannon channels; ensemble refinement is "often ambiguous due to low information content, unknown systematic errors, unknown solvent contributions" (Shevchuk & Hub, SN). Forward-model hydration parameters are fitted (all except WAXSiS), so the model and the data are confounded. CRYSOL versions alone shift predictions.
- **Ensemble reweighting**: BME output depends on the prior. Subset-selection methods (EOM-like) are non-unique. BE-SAXS was designed to avoid finite-subset artefacts (SN).
- **smFRET**: about 5 Å accuracy, limited by the dye-linker model (Nat Methods 2023, SN).
- **NMR references**: CASD-NMR and ARTINA "ground truth" are themselves NMR models. Under 1.5 Å agreement is near the reference's own uncertainty.
- **Cryo-EM**: low Q-score conflates flexibility, damage and misfit (Acta D 2025). Heterogeneity latent spaces are not identifiable up to reparametrisation (CryoBench metrics address this; SN).
- **Binding sites**: an absent ligand does not mean an absent site. LIGYSIS aggregation reduces but cannot remove false "false positives". Cryptic-site labels depend on apo selection.
- **pKa**: the null model (water pKa) is close to many methods. In the KaML paper the null His RMSE is lower than PROPKA3's by 0.06. A 2023 independent benchmark found no method beat the null with confidence.

---

## 6. Could-not-verify list and open questions

- GitHub-hosted versions (fpocket, MD-jeep release date, MolProbity, KaMLs, P2Rank release year) were blocked (403). The P2Rank years are inferred.
- Full text of the CZII Kaggle results preprint (HTTP 429): metric beta, annotation protocol and licence.
- A 2023 or later CASD-NMR round; any community distance-geometry instance repository (none found).
- A head-to-head PB solver benchmark covering APBS, DelPhi, MIBPB, TABI-PB and PBSA on Kirkwood with the same surface (none found). **No certified (rigorous) PB error bounds** were found, only a-posteriori estimates.
- An independent post-2024 pKa benchmark with sequence-level hold-out comparing KaML, DeepKa, pKALM and CpHMD (not found). The KaML JCTC publication details were not verified.
- An independent benchmark of SAXS forward calculators on SASBDB (none found; only reviews such as Chatzimagas & Hub 2022).
- LIGYSIS data licence and code location (only the second half of the paper is unread).
- PDBbind current licence terms; the PLINDER v2 → 1.0.0 dataset changes.
- Rigidity predictions validated against B-factors or order parameters: no direct validation was found. HDX case studies only.
- SASBDB, M-CSA, PDBe-KB, PDB-REDO, KINARI, Rosetta KIC sets, scPDB, HOLO4K origins: MEM only.
- A 2026 NeurIPS abstract ("What counts as finding a cryptic pocket?") claims AUPRC 0.406 vs PocketMiner 0.19 on CryptoBench. SN only; not verified.

---

## 7. Source list (all accessed 2026-11-26)

| URL | Title | Read level |
|---|---|---|
| https://pmc.ncbi.nlm.nih.gov/articles/PMC11552181 | Utgés & Barton, Comparative evaluation of methods for prediction of protein–ligand binding sites (J Cheminform 2024) | FT-partial |
| https://zenodo.org/records/14645504 | LBS-Comparison results | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC11601431.3 | KaML / PKAD-3 preprint | FT-partial |
| https://sites.krieger.jhu.edu/damjanovic-lab/pkad-r/ | PKAD-R | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10466379/ | Comparative performance of high-throughput methods for protein pKa predictions (2023) | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/3243943 | Progress in the prediction of pKa values in proteins (2011) | SN |
| https://arxiv.org/abs/2408.05526 ; https://cryobench.cs.princeton.edu/ | CryoBench | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11467047/ | DockQ v2 | SN |
| https://pypi.org/pypi/{DockQ,posebusters,plinder,pinder,pdb2pqr,propka,pypka,openmm,apbs-binary}/json | PyPI metadata | OP |
| https://zhanggroup.org/US-align/ | US-align home and update log | OP |
| https://openstructure.org/news ; https://openstructure.org/download/112/ | OpenStructure releases | OP / SN |
| https://github.com/rdk/p2rank/releases | P2Rank releases | OP |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12552120/ | Resolving data bias improves generalization in binding affinity prediction (CleanSplit) | SN |
| https://arxiv.org/abs/2308.09639 | Leak Proof PDBBind | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC11725321/ | CryptoBench | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC9977097 | PocketMiner | SN |
| https://www.biorxiv.org/content/10.1101/2025.11.03.686153 | Lessons learned from a Kaggle challenge for particle picking in cryo-ET | SN (fetch failed) |
| https://arxiv.org/abs/2203.10035 | SHREC 2021: Classification in cryo-electron tomograms | SN |
| https://pubmed.ncbi.nlm.nih.gov/33542514/ | Lawson et al. 2019 EMDataResource challenge recommendations | SN |
| https://pubmed.ncbi.nlm.nih.gov/38343795/ ; https://zenodo.org/records/10551958 | EMDataResource Ligand Modeling Challenge | SN |
| https://doi.org/10.1038/s41592-020-0731-1 | Pintilie et al., Q-scores | SN |
| https://journals.iucr.org/d/issues/2025/08/00/ic5125/ | Q-score analysis of EMDB/PDB (Acta D 2025) | SN |
| https://pdb101.rcsb.org/news/62de9e5235ec5bb4ddb19a43 | Q-scores in wwPDB validation | SN |
| https://pubmed.ncbi.nlm.nih.gov/38490206/ | Restraint validation of NMR structures in the PDB (Structure 2024) | SN |
| https://www.ebi.ac.uk/pdbe/node/39500 | NMR restraint remediation NEF/NMR-STAR | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC9579175 | ARTINA | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4569658 | CASD-NMR 2013 | SN |
| https://pubmed.ncbi.nlm.nih.gov/19718014/ | CASD-NMR launch | SN |
| https://github.com/mucherino/mdjeep ; https://antoniomucherino.it/en/mdjeep.php | MD-jeep | SN |
| https://arxiv.org/abs/q-bio/0608012 | The Discretizable Molecular Distance Geometry Problem | SN |
| https://arxiv.org/html/2510.19970v1 | Hybrid MDGP solver (2025) | SN |
| https://dspace.mit.edu/handle/1721.1/58306 | DISCO | SN |
| https://apbs.readthedocs.io/en/latest/releases.html | APBS release history | SN |
| https://arxiv.org/pdf/1607.04594 | Accurate, robust and reliable PB solvation energies (MIBPB) | SN |
| https://www.degruyterbrill.com/document/doi/10.2478/mlbmb-2014-0006/pdf | PBE test model, FD accuracy | SN |
| https://arxiv.org/abs/1702.05196 ; https://arxiv.org/abs/2009.11696 ; https://arxiv.org/abs/1109.4092 | A-posteriori / goal-oriented PB error | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC12199658 | Eight GB flavours vs PB (2025) | SN |
| https://zenodo.org/records/1161245 | FreeSolv v0.52 | SN |
| https://ar5iv.labs.arxiv.org/html/2204.04961 | Predicting solution scattering patterns with explicit-solvent MD | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC4420545 | Konarev & Svergun, information content of SAS data (IUCrJ 2015) | SN |
| https://journals.iucr.org/j/issues/2026/04/00/fc5088/ | Shannon-sampling SAXS (IUCrJ 2026) | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC5662244 (and related) | Bayesian / ensemble SAXS refinement | SN |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6121742/ | smFRET multi-lab benchmark (2018) | SN |
| https://link.springer.com/10.1038/s41592-023-01807-0 | smFRET proteins multi-lab (2023) | SN |
| https://arxiv.org/abs/1304.6796 ; https://arxiv.org/abs/1407.4440 ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3817810/ | FIRST vs HDX; rigidity modelling sensitivity | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC2861045 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC2846703 | RDC degeneracy | SN |
| https://academic.oup.com/nar/article/52/D1/D404/7233921 | BioLiP2 | SN |
| https://www.biorxiv.org/content/10.1101/2024.07.17.603955 ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12905371/ | PLINDER; DataSAIL addendum | SN |
| https://elifesciences.org/articles/110475 ; https://arxiv.org/abs/2405.14108 | Mac1 co-folding evaluation; PoseBench | SN |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC5734394 | MolProbity 2017 updates (CaBLAM) | SN |
