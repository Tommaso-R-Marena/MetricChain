> **Provenance.** Report of a literature assessor (a subagent of the Frontier Benchmarking division,
> model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from this
> notice.  Every row carries a *read level*; rows marked "search snippet" or "from memory" are
> unverified leads, not findings.  The coordinator read this report in full, checked none of its
> sources independently unless `../STATE_OF_THE_ART.md` or `../BENCHMARK_REGISTRY.md` says so, and
> carries the read levels forward wherever a row is used.  Out-of-charter items (sequence or
> molecule design, target-specific optimisation) are listed only to mark the boundary.

# Literature assessment: fixed-sequence biomolecular structure prediction and its community assessment

Assessor note: compiled 2026-11-26 with live sources. Read levels: **FT** = full text read; **AB** = abstract or landing page read; **OP** = official page read; **SN** = search snippet only; **MEM** = from memory, not verified. **IND** = independent evidence (blind assessment or third-party benchmark); **SELF** = self-reported (developer paper, preprint, README, blog or leaderboard). No developer claim below is an established fact unless IND evidence is cited.

---

## 1. Benchmark and assessment table

| Benchmark | Scientific question | Reference evidence and quality | Metrics | Leakage control | Licence/access | Cadence | Source / read level |
|---|---|---|---|---|---|---|---|
| **CASP16 (2024)**, assessed in PROTEINS 2026, vol. 94, issue 1 | Blind prediction of monomers/domains, oligomers (incl. antibody–antigen, "AA"), protein–ligand pose and affinity (pharma targets), nucleic acids and complexes, ensembles, accuracy estimation (EMA). | Unreleased experimental structures. Pharma ligand set: >200 co-crystals at better than 2.7 Å for chymase, cathepsin G, autotaxin and SARS-CoV-2 Mpro (Roche/Idorsia). | Monomers: GDT_HA, GDT_TS, lDDT etc. Complexes: cumulative z-score of ICS, IPS, QSbest, DockQ, TM-score and lDDT. AA targets used only ICS, IPS, QSbest and DockQ; hybrid targets used ICS, IPS, TM-score and lDDT. Ligands: LDDT-PLI, RMSD-based success. Affinity: Kendall's τ. EMA: QMODE1/2/3 with OpenStructure metrics. | Prospective and blind. Stoichiometry was withheld in "Phase 0". | Data and results are public on predictioncenter.org. Papers are mostly open access (PMC). | Every two years | Overview PMID 41178755 (AB). Monomer 40820259, complexes 41170922 and ligands 41045049: FT (metric sections grepped). Others AB. |
| **CASP17 (2026)** | Categories: immune complexes (new: antibody, nanobody, TCR); organic ligand–protein; nucleic acids and complexes (with RNA-Puzzles); conformational ensembles; difficult proteins and complexes (membrane, weak MSA, >1,000 aa); accuracy estimation, now including self-assessment for NA and ligands. | 166 targets by 2026-07-30, not counting re-releases. Over 40 immune-complex targets. | Not yet published. | Blind. Target M1370 was cancelled on 2026-06-05 after it was released publicly. | Public website | — | predictioncenter.org/casp17 and news.cgi (OP) |
| **CAMEO** (weekly) | Continuous blind evaluation of servers on PDB pre-release entries. Since about 2024 it uses whole complexes: protein, NA and ligands, in "medium", "hard" and "ligand" categories. | All new PDB entries, filtered and clustered. 23,629 entries over 76 weeks gave 12,205 targets. | lDDT and iLDDT, stoichiometry-aware and mapped. TM-score. LDDT-PLI. BiSyRMSD with success at <2 Å. Model 1 shown. | Prospective, using the PDB weekly two-phase cycle. Difficulty comes from BLAST identity and coverage against the current PDB. | Public; results downloadable | Weekly | Robin et al., PROTEINS 2026, PMID 41017158 (FT). cameo3d.org (OP, little content rendered). The QE category's current status was not verified. |
| **CAPRI** | Blind protein assembly and docking. Round 65 is joint with CASP17 (immune, NA and difficult complexes). Round 66 is a nanobody round co-organised with SEPIQ 2026. | CASP17 targets | Typically DockQ and CAPRI classes (MEM) | Blind | EBI/PDBe site | Per round | ebi.ac.uk/pdbe/complex-pred/capri (SN). No Round 65 assessment was found. |
| **RNA-Puzzles** | Blind RNA 3D prediction. Assessed the RNA-only targets in CASP16 and co-runs CASP17 NA. | Experimental RNA structures | RMSD, TM-score, GDT, lDDT, INF for WC and non-WC pairs and stacking, stereochemistry | Blind | Public | Ongoing | Westhof et al., PMID 41040059 (AB) |
| **Stanford RNA 3D Folding (Kaggle) Part 1** (2025) and Part 2 | Blind code competition for RNA 3D structure | Part 1 used 43 unreleased structures and drew more than 1,700 teams. Part 2 adds template-free targets. | TM-score based (MEM) | Blind, using unreleased structures | Kaggle | 2025; Part 2 in 2025–26 | Preprint "Template-based RNA structure prediction advanced through a blind code competition", PMC12776560 (SN). Part 2 results were not verified; CASP17 abstracts list "KAGGLE1_TEAM_CP_HHMI: first-place solution" (OP). |
| **PoseBusters** v1/v2 | Ligand pose accuracy plus physical and chemical validity | v2 is about 308 post-2021 PDB complexes (MEM) | RMSD <2 Å plus "PB-valid" checks | Time split after 2021, with no explicit similarity filter (MEM) | Open | Static | Buttenschoen et al., Chem Sci 2024 (MEM). CAMEO: drug-like success for AF3 is about 40% prospectively, "significantly lower than reported on PoseBusters" (FT, PMID 41017158). |
| **PLINDER** | Protein–ligand interaction dataset with leakage-minimised splits | More than 400k systems across more than 11k SCOP domains and more than 50k ligands. Release 2024-06/v2. | Supports pose metrics | Splits use PLI similarity. Test set stratified by novel ligand, pocket or protein. A known issue lists wrong entry_release_date values in the source data (patched via query_index). | Apache-2.0. ChEMBL data CC BY-SA 4.0; BindingDB data CC BY 4.0. | Versioned | github.com/plinder-org/plinder (SN); bioRxiv 2024.07.17.603955 (SN) |
| **PINDER** | Protein–protein docking dataset with leakage-controlled splits | not verified | DockQ etc. (MEM) | Structure and interface similarity splits (MEM) | not verified | — | not verified (MEM) |
| **Runs N' Poses** | Do co-folding models go beyond memorisation? | About 2,600 high-resolution protein–ligand systems released after 2021-09-30. The test subset is 2,073, binned by similarity to the AF3 training set. | RMSD success, LDDT-PLI | Time split plus ligand/pocket similarity bins against pre-cutoff PDB. A PREreview noted possible AF3 validation-set leakage. | Zenodo / Polaris | Static | Škrinjar, Eberhardt, Durairaj, Schwede, bioRxiv 2025 (SN) |
| **FoldBench** | Low-homology all-atom benchmark (proteins, NA, ligands, six interface types) | 1,522 assemblies in the preprint; SBGrid lists 1,505. Interfaces: PPI 279, Ab–Ag 172, P–L 558, P–peptide 51, P–RNA 70, P–DNA 330. | Success rates: DockQ ≥0.23 for interfaces; ligands need LRMSD <2 Å and LDDT-PLI >0.8. lDDT for monomers. | Low homology against PDB before 2023-01-13. Models with later cutoffs (Boltz-2, RF3) are flagged "for reference only". | MIT | Leaderboard updated (2025-12-05, 2025-12-31) | github.com/BEAM-Labs/FoldBench (OP). Nat Commun 2025, doi 10.1038/s41467-025-67127-3 (SN). |
| **PXMeter** (ByteDance) | Reproducible evaluation toolkit and curated set | More than 6k complexes in v1.0.0, manually reviewed to remove artifacts (SN/OP) | Complex lDDT, DockQ etc. | Time-split and domain subsets | Open source | — | Protenix README (OP). Developer-built: treat Protenix results on it as SELF. |
| **PolyFold** | Head-to-head of open models with stricter homology filtering | Several thousand PDB structures, homology-filtered against both models' training sets | Not verified in detail | Introduces WAFI (length-weighted average fractional identity), because min-chain identity leaks for multichain complexes | Preprint | — | bioRxiv 10.64898/2026.06.16.732304 (AB) |
| **CASP16 MassiveFold set** | Model-selection and EMA resource | Up to 8,040 AF2 models per target | DockQ, CASP and CAPRI metrics | Blind CASP targets | GitHub GBLille/CASP16-CAPRI_MassiveFold_Data | Per CASP | PMID 40874652 (AB) |
| AF3 paper evaluation sets (PoseBusters, recent-PDB) | Developer evaluation | — | — | Cutoff 2021-09-30 | — | — | SELF (MEM) |
| SAbDab-derived Ab–Ag sets | Antibody–antigen docking | CAMEO used SAbDab mapping (866 targets). A 2025 mAbs benchmark had N=49. | DockQ | Time split | — | — | PMID 41017158 (FT); tandfonline 10.1080/19420862.2025.2545601 (SN) |
| Binder-design benchmarks | — | **Out of scope** (design) | | | | | |

---

## 2. Method table

Abbreviations: cutoff = training-data cutoff (PDB date).

| Method / version | Problem | Dates | Cutoff | Performance evidence | Availability, licence, reproducibility | Known limitations | Fair comparison possible for a new fixed-sequence method? |
|---|---|---|---|---|---|---|---|
| **AlphaFold 2 / AF-Multimer v2.3**, incl. ColabFold | Protein monomers and complexes | 2021; v2.3 2022–23 (MEM) | about 2018-04 for AF2 (MEM) | IND: ColabFold is the CASP16 baseline, and more groups beat it in CASP16 than in CASP15 (FT, 40820259). With massive sampling, the AF3 advantage on complexes disappears (AB, 40851426). | Apache-2.0 code; open weights (MEM). MSA-dependent. | MSA depth; Ab–Ag | Yes. Strong, reproducible baseline (fixed MSAs, seeds). |
| **AlphaFold 3** (v3.0.1 used in CAMEO) | All-atom co-folding | Paper May 2024; code Nov 2024 (MEM for dates) | 2021-09-30 (FT, CAMEO; Runs N' Poses) | IND: best automated ligand baseline in CASP16 (mean LDDT-PLI 0.8, above the best CASP16 human predictor at 0.69) (AB, 41045049). Top-ranked model is comparable to the best CASP methods (AB, 40851426). In CAMEO, about 40% drug-like success, strongly correlated with similarity to training data (FT). Leads FoldBench strictly-valid rows (OP). | Code Apache-2.0. Weights under separate Terms of Use, "only if received directly from Google". Server is non-commercial. Repo also lists SynthID-watermarked and "AF3-LA" weights (OP). | Ligand memorisation; physics critiques (adversarial binding-site mutations still give same pose; Nat Commun 2025, SN). Limited stoichiometry for large heteromers; poor NA accuracy (AB, 40851426). | Yes, as reference, if run locally with recorded seeds and MSAs on a post-2021-09-30, similarity-binned set. The weights licence restricts redistribution of outputs/weights (terms not read in full). |
| **Boltz-1 / Boltz-2** | Co-folding; Boltz-2 adds affinity | Boltz-1 preprint 2024-11-19; Boltz-2 preprint 2025-06-18 (AB) | Boltz-2 after 2023-01-13 per FoldBench (OP); exact date 2023-06-01 (MEM, not verified) | IND: FoldBench post-2024 Ab–Ag 25.0% vs AF3 47.95% (flagged as possibly leaked) (OP). PolyFold: Boltz-2 above OpenFold3 under conventional filtering; gap "narrows or disappears" under WAFI (AB). SELF: approaches FEP for affinity. CASP16: affinity prediction "totally unreliable" field-wide (AB, 41088961). | MIT, code and weights (OP). Boltz-2 training code "coming soon" in README. | Ab–Ag weak; homomultimers; small-molecule realism (PolyFold, AB) | Yes. Open. Must use post-cutoff targets. |
| **Chai-1** | Co-folding | Preprint 2024-10 (SN) | 2021-09-30 (MEM) | IND: FoldBench Ab–Ag 18–24% (OP). A 2025 mAbs Ab–Ag benchmark: 20.4% overall (SN). | Apache-2.0, code and weights (SN, from README); earlier non-commercial terms (SN) | Ab–Ag | Yes |
| **Chai-2** | Antibody design | — | — | **Out of scope** (design) | | | |
| **Protenix v0.5 / v1 / v2** (ByteDance) | AF3 reproduction | v0.5 2025-05-30; v1 2026-02-05; v2 2026-04-08 (OP) | v1 default 2021-09-30; v1-20250630 variant 2025-06-30; v2 2021-09-30 (OP) | SELF: v1 claimed to outperform AF3 at matched cutoff and budget, evaluated on its own PXMeter. v2 claims +9–13 pp DockQ success over v1. IND: FoldBench (older Protenix) below AF3 (OP). A Bioinformatics 2026 Ab–Ag study ranks "Protenix-1" top (SN). | Code Apache-2.0. v1 weights open. **v2 weights proprietary** (OP). | Developer-built benchmark | Yes for v1 (open, cutoff known). Use the 2021 variant for time-split comparisons. Not for v2. |
| **OpenFold3** (preview → full) | Open AF3-class co-folding | Preview Oct 2025; full stack (data on AWS) Mar 2026 (SN) | OpenBind-0 weights (≥0.5.0): June 2025 (SN, README) | IND: FoldBench preview row lowest on P–L (44.5%) and P–DNA (5.9%) (OP). PolyFold: below Boltz-2 before WAFI (AB). | Apache-2.0 (SN). The NVIDIA NIM card cites the NVIDIA Open Model License (SN). | June 2025 cutoff makes most public 2023–25 benchmarks leaky | Only on targets released after June 2025 (e.g., CASP17). |
| **RoseTTAFold All-Atom / RF3** (AtomWorks) | All-atom co-folding | RFAA 2024 (MEM); RF3 preprint 2025-08 (SN) | RF3 after 2023-01-13 (OP, FoldBench) | IND: CAMEO RFAA ligand subset below AF3 (FT). FoldBench RF3 post-2024 PPI 72.4%, Ab–Ag 37.5%, P–L 57.3%, flagged possibly leaked (OP). SELF: improved chirality. | BSD, code, weights and data (SN) | — | Yes, on post-cutoff targets |
| **HelixFold3** | Co-folding | 2024 (MEM) | not verified | IND: FoldBench Ab–Ag 28.4%, P–L 51.8% (OP) | not verified | — | Conditional |
| **ESMFold** | Single-sequence protein folding | 2022/2023 (MEM) | not verified | Below MSA methods (MEM) | Open (MEM) | Low accuracy on orphan proteins | Yes, as single-sequence baseline |
| **ESMFold2 / ESMFold2-Fast** (Biohub) | All-atom co-folding with ESM-C LM; MSA optional | Preprint June 2026 (bioRxiv 10.64898/2026.06.03.729735) (OP) | Sept 2021 (OP model card) | SELF only: "meets or exceeds AF3" on Ab–Ag, PPI and Runs N' Poses (FoldBench). Secondary blog figure: 55% Ab–Ag (SN). No IND evidence found. Widely used inside CASP17 pipelines (OP, abstracts). | MIT (OP) | Card: top accuracy needs heavy inference compute; degraded performance on non-protein molecules | Yes. Open, 2021 cutoff. Report inference budget. |
| **IntelliFold-2** (IntelliGen AI) | Co-folding | Preprint 2026-02-10 (AB) | not verified | SELF: gains over AF3 on FoldBench (Ab–Ag, P–L). Flash/v2/Pro variants. | "open-source" (AB); licence not verified | — | Conditional on weights and cutoff |
| **SeedFold** (ByteDance Seed) | Scaled co-folding | arXiv 2512.24354 (Dec 2025) (SN) | not verified | SELF: beats AF3 on some FoldBench tasks | not verified | — | Unknown |
| **OpenDDE** (Aureka) | Co-folding "drug discovery engine" | arXiv 2607.03787, 2026-07 (SN) | not verified | SELF: "IsoDDE-level". ARK-AB 58.9% vs AF3 47.7% (SN). Used by CSSB-Human in CASP17 (OP). | Apache-2.0, HF weights (SN) | Preview | Conditional |
| **IsoDDE** (Isomorphic Labs) | Proprietary AF3 extension | 2026-02-10 (OP) | not stated | SELF: more than 2× AF3 in the hardest Runs N' Poses bin; Ab–Ag DockQ >0.8 at 2.3× AF3 and 19.8× Boltz-2 (n=334) | Proprietary; no availability stated | — | No (closed) |
| **AtlasFold / AtlasFold-M** (KAIST) | PLM-based folding | 2026-09-07 (AB) | not verified | SELF: Ab–Ag "comparable to AF3 and ESMFold2" | MIT (AB) | — | Yes, if cutoff is documented |
| **SoupFold** | Combines pair representations of AF3/Protenix/ESMFold2/OpenDDE | arXiv 2609.15552, 2026-09-14 (AB) | inherits | SELF | not stated | — | Ensemble-of-models; compare to an oracle/ensemble baseline |
| **MassiveFold** | Massive AF2 (and AF3) sampling | CASP16 dataset 2025 (AB) | AF2 | IND: biggest gains on hard interfaces; median ipTM predicts benefit (AB, 40874652) | Open (GitHub) | Compute | Yes, as sampling baseline |
| **AFsample2 / AFsample3** (Wallner) | MSA-masking sampling; AFsample3 uses AF3 | AFsample3 abstract CASP17 (OP) | AF2/AF3 | CASP16: Wallner below kozakovvajda on AA (FT) | Open (MEM) | — | Yes, as sampling strategy (budget-matched) |
| **kozakovvajda / ClusPro** | FFT docking + AF monomers + MD/AFM refinement | CASP16 | — | IND: CASP16 AA winner, about 60% on targets hard for AF2/3. It stayed ahead of AF3 run locally with 1,000 seeds. Only 8 AA targets, so "cannot firmly conclude a breakthrough" (FT, 41170922). Top on CASP16 pharma ligand Model 1 (FT, 41045049). | ClusPro server (MEM) | Small n | Yes, via server |
| **Yang lab** (Yang-Server, Yang-Multimer; trRosetta/trRosettaRNA + AF) | Protein and RNA | CASP16/17 | — | IND: top three CASP16 monomer groups all Yang lab (AB, 40820259) | Servers (MEM) | — | Server-level only |
| **MULTICOM3/4/5**, **Kiharalab** | Complex pipelines (AF2/AF3, MSA engineering, sampling) | CASP16 | — | IND: top on best-of-5 complex models in CASP16, with no ranking advantage on Model 1 (AB, 41170922) | MULTICOM open on GitHub (AB) | Model selection | Yes, pipeline-level |
| **Zheng/Zhang lines** (DMFold2, D-I-TASSER, I-TASSER-Fold, DeepMSA2) | Protein, complex, EMA | CASP17 abstracts (OP) | — | CASP16: listed among strong assembly servers (AB, 41088961) | Servers | — | Server-level |
| **DeepSCFold** | Complexes | not verified | — | not verified | — | — | — |
| **PEZYFoldings** | Pipeline / model ranking | CASP16/17 | — | IND: notable first-model selection advantage in CASP16 (AB) | — | — | — |
| **NA predictors**: RhoFold+, trRosettaRNA(2), DRfold2, NuFold, RNAPro, Vfold, BRiQ | RNA 3D | various | various | IND: CASP16 NA "generally poor", no new natural RNA above TM 0.8; top groups were human experts (Vfold, GuangzhouRNA-human, KiharaLab); no notable gain after accounting for templates (AB, 41165252). DL "not superior to traditional approaches" (AB, 41178755). Kaggle Part 1 top entry was template-based, without DL; RNAPro combines strategies (SN). | Mostly open (MEM) | Template dependence; pseudoknots, non-canonical pairs | Yes. Must stratify by template availability. |

---

## 3. What independent evidence currently says is strongest, per category

**Protein monomers.** CASP16 assessors state that single-domain fold prediction is "nearly solved": no target fold was predicted incorrectly across all evaluation units (Yuan et al., AB). The three top monomer groups were all from the Yang lab, and progress from CASP15 was "subtle" (AB). The overview attributes the plateau to experimental uncertainty rather than method deficiency (Kryshtafovych et al., AB). Model ranking remains a persistent weakness (AB). For a benchmark registry, this means the monomer category has limited power to separate methods.

**Protein complexes.** Complex prediction "remains an unsolved challenge": even leading groups predicted only slightly more than half of the targets to high accuracy (Zhang et al., AB). MULTICOM and Kiharalab led on best-of-five models. Their lead over Yang-Multimer and kozakovvajda shrank on Model 1 (AB). Elofsson's analysis found AF3 slightly better than AF2-based methods, but no different once AF2 is massively sampled (AB). In CAMEO, methods that predict stoichiometry (MultiFOLD/MultiFOLD2) beat an AF3 baseline run as single copies on homomers and heteromers (FT). This baseline effect makes stoichiometry handling a confounder in any comparison.

**Antibody/immune complexes.** In CASP16 the top AA group did not use AF as its primary engine (kozakovvajda: FFT docking plus refinement). It still beat a local AF3 run with 1,000 seeds, but only 8 AA targets were assessed (FT). On FoldBench's strictly valid rows, AF3 leads (47.9% Ab–Ag success; OP). Newer releases (ESMFold2, Protenix-v2, IntelliFold-2, OpenDDE, IsoDDE) claim to beat AF3 on Ab–Ag, and all of that evidence is SELF. **No independent evidence found shows a 2026 release beating AF3 on antibody–antigen.** CASP17's new immune-complex category (over 40 targets) is the first large blind test of these claims. Its results are not yet public.

**Protein–ligand.** In CASP16 pharma targets, AF3 run as an automated baseline (mean LDDT-PLI 0.80) outscored every participant; the best participants reached 0.69 (Gilson et al., AB). Template-based participants did well (AB). CAMEO shows AF3 beats docking baselines prospectively. Its drug-like success rate is about 40%, below its PoseBusters figure, and performance tracks similarity to the AF3 training set; template and physics methods show the same trend (FT). Affinity prediction showed a maximum Kendall τ of 0.42 against a ceiling of about 0.73 (AB). Practical-outcomes authors call affinity prediction "totally unreliable" (AB). Boltz-2's FEP-like affinity claims are SELF.

**Nucleic acids.** Performance is generally poor. Top groups were human experts, and there was no notable gain once template availability is taken into account (Kretsch et al., AB). Deep-learning methods were "not superior to traditional approaches" (overview, AB). In Kaggle Part 1, the best solution was template-based without DL, and its top three entries scored within error of the CASP16 winners (SN).

**Open-model head-to-heads.** PolyFold reports that Boltz-2's apparent lead over OpenFold3 narrows or disappears under stricter whole-complex homology filtering (AB). This is a direct demonstration that leakage control can reverse conclusions.

**Accuracy estimation.** Methods using AF3-derived features, especially per-atom pLDDT, performed best for local accuracy (Fadini et al., AB). The overview says the best EMA methods are largely effective at selecting complex models with high interface accuracy (AB). QMODE3, selection from about 8,000 MassiveFold models, varied strongly between monomer, homomer and heteromer targets (AB). CAMEO's QE status for 2026 was not verified.

---

## 4. CASP17 status as of 2026-11-26

**Public now (OP, predictioncenter.org):**
- Dates:
  - Registration opened 2026-03-31.
  - Target release ran 2026-04-27 to 2026-07-31.
  - The modeling season ended 2026-08-31 (CAPRI page snippet: prediction season over by 2026-09-11).
  - Abstracts closed 2026-09-25.
  - Program and abstracts were posted 2026-11-25.
- **Results: "Results will be posted on Sunday, November 29"** (news, 2026-11-25). The results page currently says "No results available yet".
- Conference: Rome, Hotel Quirinale, **1–5 December 2026**.
- Scale:
  - 166 targets by 2026-07-30, plus re-releases.
  - Over 40 immune-complex targets.
  - About 160 groups registered by April.
  - 171 abstracts in the Abstracts Explorer.
- Assessors:
  - Keegan: difficult proteins and EMA.
  - Zyla: immune complexes.
  - Durairaj: ligands.
  - Szachniuk, Antczak and Westhof: RNA.
  - Montelione-led team: ensembles.
  - Lensink: CAPRI perspective.
  - Herschlag: "HI-FI protein structure".
  - Price: fibrils special challenge.
  - Mulvaney and Joseph: cryo-EM.
- Other items:
  - CASP–DREAM TAP challenge announced 2026-11-25.
  - "Future of CASP" community consultation (2026-11-23).
  - Google DeepMind one-time gift (2025-07-19).
  - MassiveFold did not run on very large targets (2026-08-14).

**Invited predictor talks.** These are an *indirect* signal of strong performance. They are not a ranking.

| Category | Invited predictor talks |
|---|---|
| Proteins | kozakovvajda 231 (Kozakov); Zheng groups 697s/024/603/522s, structure and EMA (W. Zheng); Yang-server 170s (Luo) |
| Antibody | CSSB 653 (Baek); HUJI-BIO3D 394 (Schneidman-Duhovny; abstract "PoseFold: AF3 guided by docking-generated templates") |
| EMA | RESIDUDES-X 077s, protein and RNA EMA (Yoo) |
| RNA | DASLAB 859s/488s/820h (Joshi; "Agentic RNA structure prediction with Nucleo"); Vfold 213h (Chen); Yang-server 170s (J. Yang); Kaggle RNA experiment talk |
| Ligands | SNU-CHEM-Server 005s (Seok); RESIDUDES-X 077s (Shin) |
| Ensembles (other assessor's scope) | MULTICOM 260; Zou 588 |
| Abstract-vote talks | ITFold-server 558 (Zhang lab); VRMRMTTS 192 (Olechnovič, single-model QA "VoroMarmotte") |

Keynotes are by Dunbrack and AlQuraishi.

**What the abstracts reveal (OP, grepped):**
- AF3 is the dominant engine; "AF3" appears in at least 112 lines.
- Boltz-2, Protenix (incl. v1), Chai-1, OpenFold3 and ESMFold2 appear widely as components.
- Ensembles are common: CSSB-Human combines AF3, Boltz-2, Chai-1, Protenix, OpenDDE and RNAPro.
- Agentic/LLM-assisted pipelines appear: CSSB-Agent "APAR", KiharaLab, Shen, AlphaMembrane, DASLAB "Nucleo". Some list Claude or GPT as components.
- New sampling methods: AFsample3 (AF3 MSA masking) and AF3Profile (Bryant).
- New group models: DMFold2 (Zheng), Thal-Kak (CSSB-Server), MiniWorld (CSSB), MetaFold-RNA3d, RibonanzaNet-3D, Boltr (a Rust Boltz-2 port).
- Kaggle RNA solutions entered as groups.
- No abstract from DeepMind/Isomorphic was found by grep (none for "DeepMind" or "Isomorphic").

**Not public:** All CASP17 rankings, assessor conclusions and target structures. **No CASP17 ranking is claimed here.** The unit should re-check after 2026-11-29 and after the Rome meeting.

---

## 5. Contamination facts

| Model | Training cutoff | Source / read level |
|---|---|---|
| AF3 | 2021-09-30 | CAMEO FT; Runs N' Poses SN |
| ESMFold2 | Sept 2021 | OP |
| Protenix v0.5/v1-default/v2 | 2021-09-30 | OP |
| Protenix v1-20250630 | 2025-06-30 | OP |
| OpenFold3 OpenBind-0 | June 2025 | SN |
| Boltz-2 and RF3 | after 2023-01-13, per FoldBench | OP |
| Chai-1 | 2021-09-30 | MEM |

How the benchmarks line up against these cutoffs:
- **FoldBench** filters against PDB before 2023-01-13. It is therefore only "strictly valid" for models with earlier cutoffs. FoldBench itself flags Boltz-2 and RF3 (OP).
- **Runs N' Poses and PoseBusters v2** use post-2021-09-30 sets. These are contaminated for any 2025-cutoff model, including OpenFold3 and Protenix-20250630.
- **CAMEO** argues that static sets (PoseBusters, Runs N' Poses) "are quickly getting incorporated into training pipelines, limiting their utility for independent evaluation" (FT).
- **CASP17** targets (released April–July 2026) are post-cutoff for all listed models. They are the cleanest available test for June-2025-cutoff models.

Known leakage and memorisation findings:
- Co-folding largely memorises ligand poses; accuracy falls with similarity to the training set (Runs N' Poses, SN; CAMEO, FT).
- Adversarial binding-site mutations leave predicted poses essentially unchanged (Masters et al., Nat Commun 2025, SN).
- Minimum-chain identity filtering leaks for multichain complexes; WAFI is proposed instead (PolyFold, AB).
- PLINDER's source data contains wrong release dates (SN). Time splits that depend on those fields need patching.
- The Runs N' Poses reviewer raised possible AF3 validation-set leakage (SN).
- Developer benchmarks are developer-built (PXMeter for Protenix; IsoDDE's own Ab–Ag set). Treat these as SELF.

---

## 6. Could-not-verify list and open questions

- CASP17 results (due 2026-11-29); CAPRI Round 65 assessment.
- Kaggle RNA Part 2 final standings.
- CAMEO QE status in 2026.
- Exact training cutoffs for Boltz-2, Chai-1, RF3, HelixFold3, IntelliFold-2, SeedFold and OpenDDE.
- AF3 weight terms in full, and the "AF3-LA" and SynthID weight release dates.
- OpenFold3 licence: Apache-2.0 vs the NVIDIA Open Model License.
- ESMFold2 numeric results from the preprint itself (only secondary figures were seen).
- Details of PINDER and PoseBusters v2. DeepSCFold, D-I-TASSER and HelixFold3 primary sources.
- The Bioinformatics 2026 Ab–Ag study (Protenix-1 top) and ARK-AB were seen only as snippets.
- RoseTTAFold3 numbers come from a model catalog and FoldBench, not the preprint.
- CASP16 assessment metric definitions were grepped from full text, not read end-to-end.
- Open question: are CASP16 Ab–Ag conclusions (8 targets) robust? CASP17 (over 40 immune targets) should answer this.
- Open question: how should multi-model ensembles (SoupFold, CSSB-Human) be compared fairly against single models? Budget matching and oracle baselines are needed.

---

## 7. Sources (all accessed 2026-11-26)

| # | URL | Title | Read level |
|---|---|---|---|
| 1 | https://predictioncenter.org/casp17/ | CASP17 home | OP |
| 2 | https://predictioncenter.org/news.cgi | CASP news | OP (first 100k characters) |
| 3 | https://predictioncenter.org/casp17/doc/CASP17_Meeting_Program.pdf | CASP17 Conference Program | FT |
| 4 | https://predictioncenter.org/casp17/abstracts_browser.cgi | CASP17 Abstracts Explorer | OP (TOC grepped) |
| 5 | https://predictioncenter.org/casp17/results.cgi | CASP17 results ("No results available yet") | OP |
| 6 | https://doi.org/10.1002/prot.70076 | Kryshtafovych et al., Progress and Bottlenecks… CASP Round XVI | AB |
| 7 | https://doi.org/10.1002/prot.70031 | Yuan et al., CASP16 Protein Monomer Structure Prediction Assessment | AB; FT grep |
| 8 | https://doi.org/10.1002/prot.70068 | Zhang et al., Assessment of Protein Complex Predictions in CASP16 | AB; FT grep |
| 9 | https://doi.org/10.1002/prot.70061 | Gilson et al., Assessment of Pharmaceutical Protein-Ligand Pose and Affinity Predictions in CASP16 | AB; FT grep |
| 10 | https://doi.org/10.1002/prot.70053 | Tosstorff et al., The CASP16 Experimental Protein-Ligand Datasets | AB |
| 11 | https://doi.org/10.1002/prot.70072 | Kretsch et al., Assessment of Nucleic Acid Structure Prediction in CASP16 | AB |
| 12 | https://doi.org/10.1002/prot.70052 | Westhof et al., RNA-Puzzles Assessments… CASP16 | AB |
| 13 | https://doi.org/10.1002/prot.70037 | Fadini et al., Model Quality Assessment for CASP16 | AB |
| 14 | https://doi.org/10.1002/prot.70035 | Highlights of Model Quality Assessment in CASP16 | AB |
| 15 | https://doi.org/10.1002/prot.70044 | Elofsson et al., AlphaFold3 at CASP16 | AB |
| 16 | https://doi.org/10.1002/prot.70078 | Abriata et al., Practical Outcomes From CASP16 | AB |
| 17 | https://doi.org/10.1002/prot.70040 | MassiveFold Data for CASP16-CAPRI | AB |
| 18 | https://doi.org/10.1002/prot.70060 | Robin et al., Beyond Single Chains… CAMEO | FT |
| 19 | https://doi.org/10.1002/prot.70042 | Updates to the CASP Infrastructure in 2024 | SN |
| 20 | https://cameo3d.org/ | CAMEO | OP (sparse render) |
| 21 | https://www.ebi.ac.uk/pdbe/complex-pred/capri/ | CAPRI (Rounds 65, 66) | SN |
| 22 | https://github.com/BEAM-Labs/FoldBench | FoldBench repository/leaderboard | OP |
| 23 | https://doi.org/10.1038/s41467-025-67127-3 | Benchmarking all-atom biomolecular structure prediction with FoldBench | SN |
| 24 | https://github.com/plinder-org/plinder | PLINDER | SN |
| 25 | https://zenodo.org/records/14794786 | Runs N' Poses dataset | SN |
| 26 | https://prereview.org/reviews/15708197 | PREreview of Runs N' Poses | SN |
| 27 | https://doi.org/10.1038/s41467-025-63947-5 | Masters et al., co-folding physics | SN |
| 28 | https://www.biorxiv.org/content/10.64898/2026.06.16.732304v1 | PolyFold | AB |
| 29 | https://github.com/google-deepmind/alphafold3 | AlphaFold 3 repository | OP |
| 30 | https://github.com/jwohlwend/boltz | Boltz repository | OP |
| 31 | https://doi.org/10.1101/2025.06.14.659707 | Boltz-2 preprint | AB |
| 32 | https://raw.githubusercontent.com/bytedance/Protenix/main/README.md | Protenix README | OP |
| 33 | https://raw.githubusercontent.com/chaidiscovery/chai-lab/main/README.md | Chai-1 README | SN |
| 34 | https://raw.githubusercontent.com/aqlaboratory/openfold-3/HEAD/README.md | OpenFold3 README | SN |
| 35 | https://build.nvidia.com/openfold/openfold3/modelcard | OpenFold3 NIM card | SN |
| 36 | https://sciety.org/articles/activity/10.1101/2025.08.14.670328 | AtomWorks and RF3 | SN |
| 37 | https://huggingface.co/biohub/esmfold2 | ESMFold2 model card | OP |
| 38 | https://www.biorxiv.org/content/10.64898/2026.02.09.704787v1 | IntelliFold-2 | AB |
| 39 | https://arxiv.org/abs/2512.24354 | SeedFold | SN |
| 40 | https://arxiv.org/abs/2607.03787 | OpenDDE | SN |
| 41 | https://www.isomorphiclabs.com/articles/the-isomorphic-labs-drug-design-engine-unlocks-a-new-frontier | IsoDDE | OP |
| 42 | https://www.biorxiv.org/content/10.64898/2026.09.04.749352v1 | AtlasFold | AB |
| 43 | https://arxiv.org/abs/2609.15552 | Co-folding with a Soup of Representations | AB |
| 44 | https://tandfonline.com/doi/full/10.1080/19420862.2025.2545601 | Ab–Ag docking benchmark (mAbs 2025) | SN |
| 45 | https://academic.oup.com/bib/article/27/2/bbag137/8554115 | Ab–Ag benchmark, Briefings in Bioinformatics 2026 | SN |
| 46 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12776560/ | Template-based RNA structure prediction… blind code competition | SN |
