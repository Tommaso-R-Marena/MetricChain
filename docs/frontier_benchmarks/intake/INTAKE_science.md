> **Provenance.** Report of a read-only intake reviewer (a subagent of the Frontier Benchmarking
> division, model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from
> this notice.  It read the named divisions at the pinned commits stated in its first paragraph; it
> re-ran no script and checked no proof.  It is an internal AI reading, not a review.  What the
> coordinator verified directly, and where this report is used, is in `../RESEARCH_INTAKE.md`.
> Sentences marked "evaluator suggestion" or "gaps noticed" are the reviewer's proposals.

# Intake: Science division ("Scientific Discovery, Translation & Independent Validation")

Commit read: `4661a037eaa0c4e889ce29778412e00322ac5b69`. Every file was read with `git show <commit>:<path>`. Paths are relative to the repository root. Science's epistemic labels are kept as they appear: [V] machine-checked, [P] paper proof, [K] known, [N] numerical, [M] measured on a named model, [H] reading, [C] conjecture.

What was read: these files in full: OWNER_DIRECTIVES, SOFTWARE_EVALUATION_PROTOCOL, BENCHMARK_DESIGN, PRIOR_ART_MATRIX, SCI-MSG-0033, SCI-MSG-0034, SCI-REV-0006, SCI-RES-0030 and the template. These in part: PHYSICAL_APPLICABILITY (§§0–8, 2a, 2b, 3a), SCIENTIFIC_FRONTIER_MAP (§§1–3), RESEARCH_SYNTHESIS (§0 head, §§3–6, §9, the "Rules"), INDEPENDENT_VALIDATION (§1 headings, §2, §3), INFERENCE_LIMITS (§0, §8, §11), ALTERNATIVE_FRAMEWORKS (§0, §8), OPEN_PROBLEMS (A–E), PUBLICATION_OPPORTUNITIES (§0, §3), SCI-REV-0018…0022 (verdict and major-finding sections), SCI-REV-0023 (§1, §5), SCI-RES-0035 (§§0–4), the heads, "read first" lists and index of SCIENCE_TO_ALL.md, and from status/science.md the head and the "Outstanding requests" section. Not read: the workstream reports (except targeted greps), INFERENCE_LIMITS_ADDENDA, ASSUMPTION_AUDIT, and SCIENCE_UPSTREAM_SYNC.

---

## 1. Owner directives recorded by science (verbatim)

Source: `docs/science/OWNER_DIRECTIVES.md`, which records four directives:
- **D-0** is the founding charter. Science records it as "**not in the repository in full**". Its limits are restated in `RESEARCH_SYNTHESIS.md` under "Rules that bind the division".
- **D-1** (15:11 UTC on 2026-11-26) is verbatim in `SCI-MSG-0029.md` §1.
- **D-2** (15:36) is verbatim in OWNER_DIRECTIVES.
- **D-3** (about 22:00) is verbatim in OWNER_DIRECTIVES.

| topic | verbatim quote | where |
|---|---|---|
| Scope: exclusions | "Do not undertake biological sequence engineering or target-specific optimization." | D-1, SCI-MSG-0029 §1, owner's §5 |
| Scope: exclusions (charter, as restated) | "no manuscript, preprint or external contact; biological sequence engineering, target-specific optimisation and experiments are out of scope; never fabricate a citation or a number" | RESEARCH_SYNTHESIS, "Rules that bind the division" (a restatement, not the owner's text) |
| Scope: when benchmarking happens | "The objective is to establish broadly applicable mathematical foundations whose scientific usefulness can subsequently be evaluated through independent engineering, benchmarking, and experimental validation." / "Extensive application-specific benchmarking will be undertaken during a subsequent research phase." | D-1 §5 |
| Science's role | "The Scientific Discovery Division should continue independent mathematical criticism, assumption auditing, scientific relevance assessments, and rigorous novelty evaluation." | D-2 §4 |
| Evaluation: independence | "Do not become an advocate for the software." … "Attack its strongest claims." … "A software result should not receive favorable scientific interpretation merely because its implementation is correct or because a related theorem is formally verified." | D-3 §1 |
| Evaluation: model against molecule | "Distinguish between mathematical guarantees about a specified model and evidence about a physical molecule. Investigate whether the proposed mathematical guarantee is more precise than the underlying physical model is accurate. Identify when certified uncertainty is meaningful and when it is overwhelmed by model error." | D-3 §2 |
| Evaluation: benchmarks | "Does this benchmark address an important scientific problem? Are the comparisons appropriate? Is the baseline sufficiently strong? … Are favorable examples representative? What important structural regimes are missing? What result would refute the proposed scientific interpretation?" and "You may propose stronger benchmarks or recommend rejection of misleading comparisons." | D-3 §4 |
| Evaluation: request form | the request lists "The mathematical claim being evaluated. The exact source commit. Required assumptions. The proposed computational method. Appropriate baselines. Correctness criteria. Expected outputs. Resource estimates. Stopping conditions." | D-2 §6 |
| Novelty and prior art | "Distinguish: Established methods. New implementations of known methods. New combinations of existing techniques. Genuine mathematical novelty. Genuine computational novelty. Genuine scientific novelty. Do not certify novelty solely because a limited search fails to find a prior result. Record search strategies and unresolved prior-art questions." | D-3 §5 |
| Experimental evidence | "Evaluate whether proposed structural observables correspond to actual experimentally obtainable information. Do not assume that idealized mathematical measurements are identical to experimental signals." The list covers the observation model, measurement uncertainty, information loss, non-identifiability, model mismatch, alternative explanations, dependence on priors, and observed versus inferred quantities. Then: "Identify mathematical prerequisites for credible retrospective experimental validation. Do not undertake unauthorized experimental execution." | D-3 §3 |
| Imported results | "Imported mathematical results must be checked rather than accepted unconditionally." … "AI-generated referee reports remain internal reviews, not external academic peer review." | D-2 §5 |
| Resources | "Do not independently consume the shared Modal budget through substantial new workloads without authorization." … "Respect the existing November 30, 2026, 3:00 PM Eastern Time computational hard stop" | D-2 §§6–7 |
| Consolidation | "When I issue the mandatory consolidation directive, anticipated at approximately $2,000 of aggregate Claude credits remaining, all divisions must transition toward proof completion, verification, integration, documentation, and preservation." D-3 §8 adds: "prioritize rigorous scientific synthesis, novelty assessments, verification of central claims, documentation of limitations, and publication-quality internal reports." | D-2 §7; D-3 §8 |
| Vacuous generality | "A general theorem with computationally vacuous guarantees should be explicitly identified as such" | D-1 owner's §4 (SCI-MSG-0029) |

Science's own gloss on D-2 (OWNER_DIRECTIVES, "What D-2 changes", item 5): "this division has never used Modal and does not start." The status file confirms "No Modal access and none sought."

**Searches for an eighth division.** No file at this commit mentions a Frontier Benchmarking / experimental-evidence / evaluation division. A `git grep` for those names under `docs/` found nothing. The mailbox table at the head of SCIENCE_TO_ALL.md lists seven divisions.

---

## 2. Verdicts on MetricChain capabilities

Novelty classes used below:
- **PRIOR_ART_MATRIX.md** uses a numbered scale: (1) established · (2) reformulation · (3) known special case · (4) plausibly original generalisation · (5) new combination · (6) plausibly original theorem · (7) plausibly original capability · (9) unresolved.
- The six-class scheme of D-3 has **not yet been applied systematically**. The matrix is "Version 1 … a full second version is owed" (§E).
- Science's scientific-weight scale is in SOFTWARE_EVALUATION_PROTOCOL §3: *changes a decision a practitioner would make* · *removes sampling error only* · *more precise than the model is accurate* · *not interpretable as a statement about a molecule*.

| capability | novelty (science's class) | physical applicability, key numbers | scientific weight (science's verdict) | source |
|---|---|---|---|---|
| Certified sandwich bracket of `ln Z` and rotamer populations: ff14SB + GBn2, rotamer variables, fixed backbone | Measurements and paper proofs, "**no novelty claimed**". Pairwise GB decomposition is in print (Gaillard & Simonson 2014, 2017; Gaillard 2025; abstracts only). The K\* stopping criterion equals bracket (b). The cost table is in print (Block–Shetty, COLT 2026). | **Four-line budget for Lys₁₂** (`9.5·10¹⁰` assignments): (1) certified width `8·10⁻⁵` nats; (2) discretisation "not bounded", of order a nat per angle at rotamer resolution on a toy chain (1.3 nats per angle at 3 cells per angle; about 150 cells for `10⁻³`); (3) energy model "of order `kT` per residue" (refits change single-residue terms by 0.64–2.6 kcal/mol); (4) evaluation tolerance `10⁻⁴`–`10⁻³` nats, from an **assumed, unproved** `10⁻⁷` kcal/mol. Other instances: Val₂₀ on PPII within 0.055 nats (9 921 evaluations); Lys₂₀ within `4.1·10⁻⁴`. Fails or is costly on helices and charged chains; extended backbones only for the first route. | "line 1 is not the headline; what the certificate removes is sampling error from a model-relative number, and for this model an ordinary estimate already agrees with it to `10⁻⁴`". This is *removes sampling error only* or *more precise than the model is accurate*: "four to five orders of magnitude". Translation verdict: "as a checker and a model-relative calculator, yes; as a statement about a peptide, no". Parts (13)–(18) and (23)–(25) of the addenda are **unrefereed**. | SOFTWARE_EVALUATION_PROTOCOL §3, §8; SCI-MSG-0034 §§1–2, §7; PRIOR_ART_MATRIX C |
| Measured class constants of real residuals (B1 protocol) | "measurement, not a claim of novelty". GB non-pairwiseness is known (Archontis–Simonson 2005); LUTE is cited. | Backbone torsions: GBn2 `βc = 12–53` and growing; sup-norm remainder `2–16 k_BT`, RMS `0.2–0.9`. Same-lineage refits: exactly additive. Rotamer variables: third-order constants `0.003–0.2` kcal/mol for neutral chains, charged up to 2.4. Every constant is an exact grid maximum, "a lower bound … never a bound". Held-out maxima reach 10 times the fitted ones. | "the protocol, yes; the constants as bounds, no". **Not independently replicated**: two numbers were re-run by the coordinator. | PHYSICAL_APPLICABILITY §§0, 2, 2a, 8; PUBLICATION_OPPORTUNITIES P10 |
| Constants by analysis alone (no evaluation) | — | Loses a factor of 33–1 400 through self/cross cancellation (Val₆: −640 / +600 / total −37 kcal/mol) | "rigorous and useless beyond serine on a strand" | PHYSICAL_APPLICABILITY §2b |
| Identified sets from averaged data, model-free and divergence-ball | **(1)**: the generalised moment problem; MaxOcc and maxOR/minOR (2005–2014); Christensen–Connault 2023 | Exact LPs on lattice chains to 10 beads, scattering to 15 beads, 27 beads from engineering tables. At 27 beads an exact three-shell profile leaves the gauche fraction undetermined over 0.654 of its range. **Never on a physical system.** | "not a mathematics paper; a methods contribution only with a physical instance" | PRIOR_ART_MATRIX C; INFERENCE_LIMITS §11.2; PUBLICATION_OPPORTUNITIES §3 |
| Envelope-class identified sets; Theorem 8 (data certify a lower bound on model error) | (5); (1) for the quantity ("extent of falsification", Masten–Poirier) | Lattice chains to 10 beads; certified constant about half of the truth's at 9–10 beads | Translatable only "after §4 (i)–(ii) for a named observable" | SOFTWARE_EVALUATION_PROTOCOL §8; PHYSICAL_APPLICABILITY §5 |
| Robust ranges of macrostate ratios (A11, A13, A14; theory §11.28) | (5), "probably folklore" (Holley 1974); theory's Theorem 11.105 is (4) | Helix–coil model, no molecule: `0.1 k_BT` per residue leaves the 50-residue helix content between 0.05 and 0.61 | "for unfrustrated known parts and monotone macrostates only"; a CD comparison was proposed and "Not done" | PHYSICAL_APPLICABILITY §5; PRIOR_ART_MATRIX A, C |
| Surrogate certification by divergence (A17; B10) | Cost table **(1)**: Block–Shetty; "the table we first sent as ours is theirs" | 74 rotamer instances: "how a tractable model is fitted hardly matters, what it is fitted to matters by orders of magnitude" | "as a diagnostic, yes" | SCI-MSG-0034 §1 row 5; SOFTWARE_EVALUATION_PROTOCOL §8 |
| Certified kinetics (cuts, barrier intervals) | (2) for principles, (5) for the composition; Wrochna (PSPACE) | Statements about voxel graphs: "the prefactor is outside the programme"; a torsion scan against dynamic NMR was "not carried out on any molecule" | "not as physical rates" | SK_REPORT via PHYSICAL_APPLICABILITY §§1, 5; PRIOR_ART_MATRIX C |
| Verified kernels: pairwise DEE kernel | **(7), narrow**: "every rule is known". No proof logging found for cost-function networks or MAP (toulbar2 1.0.0 has none), but VeriPB/CakePB checks within a factor of 20 of solving (Koops et al. 2025) and PBLean imports into Lean 4 | — | "its *advantage* unmeasured" (E-1 not run) | SCI-REV-0006; PUBLICATION_OPPORTUNITIES P4 |
| Residual kernel: one certificate valid for a whole envelope class | **(7)**: "no proof-logging system read certifies a statement about a *class* of instances" | Only as meaningful as F8 (class constants) allows | Science's candidate for the capability "to put first" (M1) | SCI-REV-0006 M1; PRIOR_ART_MATRIX D3 |
| Partition-function kernel D3 | (5); the claim "verified checkers exist for exact model counting only" is **false** (W1) | — | — | SCI-REV-0006 |
| Query-complexity exponents (theory G18, G20/G21) | G20/G21 (6); G18 (3) | Evaluated at `βc ~ 1`; "nothing measured is there" except torsion refits. With a cooperative known part the direction depends on the envelope. | "not cost predictions for a molecule" | PHYSICAL_APPLICABILITY §0.3, §3a; SCI-MSG-0034 §2.8 |
| Geometry Theorem L (global stability from sequence-local distances) | Known in a different setting; "the transfer not in print" | Needs distance errors of about `10⁻⁴` Å on an α-helix trace (`1.3·10⁻⁴` Å); the necessary threshold is 2.1·10⁴ times larger; the RMSD bound exceeds `R_g` from 16 residues | "As a guarantee for data it is empty on these geometries" ("computationally vacuous" in its constants) | SCI-REV-0023 §§1, 5 |
| Complexity: multi-strand NN folding NP-hard / #P-hard | Gadget published (Lyngsø 2004 via Ducloz–Shalaby–Woods) | "(H2) is the sign pattern of every physical parameter set" is **false** (a published bulge of −0.13 kcal/mol); (H2\*) suffices | — | SCI-REV-0019 |

---

## 3. Hypotheses H1–H11 and benchmarks B1–B10

Source: `docs/science/BENCHMARK_DESIGN.md`, §1 (hypotheses), §2 (benchmarks) and §4 ("What has been run"). Its header says: "A design, not a result: nothing here has been run except where a script is named."

| item | tests | run? on what | outcome against its own refutation criterion |
|---|---|---|---|
| **B1** | H3 (residuals near a cheap class) | Pilot (workstream P) on capped alanine peptides, exact on grids to 6 residues (3-state grid) and 9 residues (2-state grid). Later P2 (rotamers: Val/Leu/Phe/Ser/Lys and one heteropolymer, 3 ideal backbones, 8.5·10⁶ assignments) and P3 (certified constants, 164 runs). | **H3 refuted** for GBn2 in backbone torsions (`β×` constant 12–53 at every site, growing; sup remainder 2–16 `k_BT`). **H3 confirmed** for same-lineage force-field differences (remainder exactly zero). In rotamer variables the third order is small for neutral chains but not for charged ones. **Not run:** residuals (c) learned against classical and (d) QM against force field; a buried environment (P2-E1 unanswered). |
| **B2** | H1, H2 (certificate cost; native format against pseudo-Boolean proof) | **Not run** ("B2, B5: nothing yet"). E-1 was accepted by engineering but has not been done. | Not run. H2 was already "weakened by SCI-REV-0006, W2". |
| **B3** | H5, H7 (informative certified intervals; tighter than ensemble methods) | Lattice chains 7–15 beads (model-free), 6–10 (envelope class), 27 (engineering tables); a deception instance at `n ≤ 16`; scattering to 15 beads | **Baselines not run.** The design names maximum-entropy reweighting, minimal-ensemble selection, MaxOcc and maxOR/minOR "as practised", and plain sampling. On the deception instance: "no baseline run on it yet". **H7 untested.** The H5 criterion (width relative to the a-priori range when the class constant is as large as B1 says) was not evaluated as written: the runs use `b ≈ 1`, while B1 measures `βc = 12–53`. Partly run. |
| **B4** | H6 (data certify model-error lower bound) | 3 margins, 2 data types, 8–10 beads, exact data | Partly run. The certified bound is about half of the truth's constant at 9–10 beads; `b_min/ε` = 0.87, 0.96, 1.07 (OPEN_PROBLEMS D3). The criterion ("falls to zero … as the chain grows") cannot be judged over three sizes. Noisy data not run. |
| **B5** | Meaning of the certified minimum | **Not run.** Named in SCI-MSG-0034 §6.8 as "the question … which nobody has run". | Not run |
| **B6** | H4 (exponents at accessible sizes) | Engineering X-005: "no violation; the flat instance is not the worst; excess decaying like `1/√n`" | Not refuted for the adaptive algorithm. SCI-REV-0018 later showed that the "worst instance found" entries at `n = 250, 350, 500` are lower bounds that are exceeded. |
| **B7** | Conformance (no hypothesis) | Theory audit replicated at many heads (INDEPENDENT_VALIDATION §§1.1–1.16) | Standing regression; passes |
| **B8** | H8 (tractable cuts certify a useful fraction of barriers) | 6–8 torsions: 1.00, 0.55, 0.77, "not monotone"; tiny systems up to 5 849 states and one 200-site chain | Inconclusive; K-E1 (6–13 torsions) not decided by engineering |
| **B9** | H9 (datum-assisted bracket) | "the coordinator's own checks only … **no adversarial search, no second implementation yet**" | Criterion (i) not violated ("none in 661 806 small cases"); (ii) and (iii) not tested |
| H10 | transport-plan range | Independent LPs (400 + 24 instances); Theorems 11.105 and 11.106 replicated | Confirmed (replication) |
| **B10** | H11 (surrogate cost set by divergence of truth from surrogate) | Run in full: planted control; 45 product-domain and 29 non-product rotamer instances; coverage baseline at `N = 200…20 000` | **Mixed, and explicitly partly refuted.** "between *fits* of one family to the solvated energy it is **refuted for the `D_2` cost** on 45 real instances (the root-mean-square remainder predicts `D_2` within a factor 2.5 …) and **confirmed for the floor**" (`D_∞` spread up to 3.2 nats). Coverage baseline: the two-standard-error bar covers in 5–82 % when `D_2 = 3–45`, so "the refutation criterion of B10 was not met" for that part. Split effect: independent residues are 10–130 times closer in `D_2` than the vacuum model for serine. |

**Known gaps in B1–B10.** No benchmark run against any external solver or ensemble method. No physical or experimental datum enters any benchmark. B2, B5 and the B3 baselines are the gaps that matter most to an outside evaluator.

---

## 4. External methods, tools and datasets identified

Reading levels are science's own, as recorded in the reports named.

| item | role | what science said | run or read |
|---|---|---|---|
| OpenMM 8.6.1; Amber ff14SB, ff99SB, ff19SB, ff03, ff15ipq; GBn2 (`implicit/gbn2.xml`, igb=8, mbondi3), OBC2 | ground truth of every [M] number | "the neck correction of GBn2 is what makes its constants large (10–70 times smaller without it); OBC2's are 2–8 times smaller for apolar side chains". CHARMM36 was not usable (no ACE/NME patches; `experiments/science/ws_P/NOTES.md`). | **Run** (energies evaluated; re-implementation agrees with OpenMM to `5·10⁻¹²`) |
| HiGHS (via SciPy) | LP solver for identified sets | Default tolerances produced false "violations" three times (DEAD_ENDS SD17) | Run |
| toulbar2 1.0.0 | exact cost-function-network solver, the baseline for minima | Has no proof logging (user guide and repository code search) | **Read only**, never run as a baseline |
| OSPREY, K\*, BBK\*, MARK\* (Donald lab) | provable partition functions in protein design | "'provable' … means a paper proof relative to the model, floating point not discussed"; the K\* stopping criterion = bracket (b) of A17 | Read (snippets or passages); not run |
| LUTE (Hallen–Jou–Donald 2017) | tuple expansions in rotamer variables | Prior art for the class constants | Read (abstract level) |
| VeriPB / CakePB (Koops et al. CP 2025); PBLean (arXiv:2602.08692); van Doren et al. ASE 2025 | incumbent proof logging | "the incumbent against which any native certificate format must be measured" | Read; comparison E-1 **not run** |
| Tan et al. CAV 2024; McCreesh et al. CP 2026; Cheng–Luo–Jiang IJCAI 2024 | verified counting | Makes the theory's D3 sentence false | Read (body of Tan et al. not accessed) |
| MaxOcc, maxOR/minOR (Bertini, Luchinat, Parigi et al. 2007–2014); Gardner–Longinetti–Sgheri 2005 | identified ranges from NMR averages | "an **established experimental-NMR method**", computed "by penalised least squares on a finite pool with a heuristic misfit threshold" | Abstracts and passages (SM_REPORT); planned as a B3 baseline, **not run** |
| Maximum-entropy reweighting; BICePs (Raddi et al. 2026); Fisher–Ullman–Stultz 2012 | ensemble-refinement baselines | Stability mechanism of Barron–Sheu 1991 | Abstracts; not run |
| Christensen–Connault 2023; Masten–Poirier; optimal UQ; di Dio–Schmüdgen 2018 | partial identification | Divergence-ball dual and extent of falsification are theirs | Read |
| Block–Shetty (COLT 2026, PMLR 336); Kunsch–Novak–Rudolf 2019; Hoeffding 1963 | certification cost under divergence | In print before science re-derived it | Read in passages (A3: 47 sources) |
| Gaillard & Simonson 2014, 2017; Gaillard 2025; Archontis–Simonson 2005 | GB decomposition | GB error "when all positions are designed together" | Abstracts through PubMed |
| Nearest Neighbor Database (RNA 2004 rules) | physical parameter check for Complexity | A bulge of −0.13 kcal/mol | Page read |
| Datasets | — | No public experimental dataset (no PDB, BMRB, SASBDB or other ensemble database) is named or used. `git grep` for PDB, BMRB and SASBDB returns zero hits. Every instance is synthetic: ideal-geometry capped peptides built in code ("no structure file, no rotamer library from a database", SCI-MSG-0025, SCI-RES-0012). P2-E1 asks only for "a public fixed structure, a public rotamer library", unnamed. | **None used** |

---

## 5. Prerequisites for experimental evidence

The prerequisites are in SOFTWARE_EVALUATION_PROTOCOL §4, "all of them, before any comparison":
- (i) "a forward model with a stated error";
- (ii) "an identifiability statement for that forward model on the class of ensembles considered, with the non-identifiable directions listed";
- (iii) "the quantity to be compared fixed in advance, with the metric and the threshold that would count as failure";
- (iv) "public data on fixed sequences, with their uncertainties";
- (v) "a null method — the comparison a practitioner would make without the new software";
- (vi) "the four-line budget of §3 for the computed side".

The same section continues: "**None of this is an experiment and none of it has been done on this branch for any physical system.**"

The claim of none is confirmed consistently across the files read:
- PHYSICAL_APPLICABILITY §6: "That anything here has been compared with a measurement. Nothing has."
- RESEARCH_SYNTHESIS §3: "Nothing in any branch has been compared with a measurement."
- RESEARCH_SYNTHESIS §9: "That anything was compared with an experiment."
- SCI-MSG-0034, header note and §4.

PHYSICAL_APPLICABILITY §5 lists four statements that could meet an experiment. Every one is marked proposal or "Not done":

| statement | possible experiment |
|---|---|
| Certified relaxed torsion scan | dynamic NMR barrier |
| Certified range and model-error lower bound | NMR or scattering averages of a fixed-sequence system with a public ensemble |
| Profile class equals scattering data (Debye, constant `q²/6`) | structural identity, not a prediction |
| Robust macrostate ranges | CD helix content |

Further cautions on observables:
- `ln Z` is observable "only in differences".
- "No experiment measures `g` at a chosen conformation."
- The calorimetric datum of A16 "is that of everything including solvent and momenta, not the mean residual energy our theorem uses".

Identifiability negatives that any forward model must face:
- Homometric lattice chains from 6 beads; 19 % of 9-bead cubic-lattice site sets.
- A scattering curve "fixes `R_g²` and little else" at 11–15 beads.
- Theorem 2: low-order agreement does not establish order or disorder.
- Mirror ambiguity of sequence-local distances: "a few hundredths to a few tenths of an ångström" (SCI-REV-0023 §5).

SCI-MSG-0034 §7 says of identified sets: "no observation model with error has been written, none tested".

---

## 6. Requests and open items

**To Structural Biology** (SCI-MSG-0034 §8; there are **six** requests, S-1 to S-6, all proposals):
- S-1: a claim sheet per capability (claim, model, source commit, certified against estimated).
- S-2: benchmark specifications *before* runs, with hypothesis, baseline, omitted regimes and refutation result; computations as nine-field requests to engineering.
- S-3: the four-line error budget with every certified number.
- S-4: forward model, error and indistinguishable set for every observable.
- S-5: a list of imported statements with commits.
- S-6: "Tell us which of the limitations of §2 you consider wrong or outdated".

"Requested response: None required." SOFTWARE_EVALUATION_PROTOCOL §1 refers to "requests S-1 … S-5", an internal inconsistency with SCI-MSG-0034's S-1…S-6.

At the pinned state the structural-biology branch "points at the theory division's commit `b2caab6` … no commit of its own, no digest … no mailbox" (status/science.md, Pins). **Nothing of theirs has been reviewed.**

**To engineering.** From status/science.md "Outstanding requests" and RESEARCH_SYNTHESIS §6:

| request | content | state |
|---|---|---|
| P2-E1 | buried environment, the "decisive" case (marked high) | **not decided** |
| P3-E1 / P6-E1 | stand-alone sandwich checker (specification: SCI-MSG-0025 §8) | accepted in principle; not started |
| P3-E2 / A19-E2 | proved rounding bound for the GBn2 evaluator (A19-E2 "first") | not answered |
| E-1 | native kernel against VeriPB/CakePB | accepted; not done |
| R7-ENG-3 | exact arithmetic over `ℚ[cos θ]` at 13 torsions | open |
| K-E1, X-E1, X-E2, P-E1 | — | not decided |
| A18-E3 | serine at 30 residues, about 40 CPU-hours | deferred by science itself (SCI-RES-0022) |
| R18-ENG-2 | the worst product instance, `n ≤ 500` | open |
| P8-E2/-E4, A18-E1, P9-E2/-E4, A19-E1/-E3 | — | sent, not answered |
| P7-E2 | — | **done** (X-012; re-run in SCI-RES-0030) |
| R10-E1 | — | **done** (X-013; SCI-RES-0033) |

RESEARCH_SYNTHESIS §6 still says "To the engineering division, nothing has been answered". That sentence is stale against the status file.

**To all divisions.** SCI-MSG-0034 was copied to all and needs no reply. SCI-MSG-0033 asks Ensemble whether E13(b) "as we now quote it … still says more than you proved". Two workstreams were running and uncommitted at the RESEARCH_SYNTHESIS §0 snapshot: R25 (a second look at Complexity's Theorem 1c and Lemma A1) and R26 (a referee of theory §11.33). **R14**, an adversarial referee of science's own addenda A17 (13)–(16), was "terminated at launch by a platform safeguard; not relaunched".

---

## 7. Corrections of record and negative results to carry forward

**Errors science found in other divisions' statements** (all internal AI reviews):
- **Theory.**
  - SCI-REV-0003: Theorem 11.84(ii) false as stated.
  - SCI-REV-0010: the workstream Y headline "interactions raise all three exponents" is false as a general statement.
  - SCI-REV-0012: Proposition 11.18c(a) is false for completeness.
  - SCI-REV-0013: Proposition 11.18e(b) is false as written; the order in 11.113(d) is too large by `e^Δ`.
  - SCI-REV-0014: 11.117(b) is false without "symmetric".
  - SCI-REV-0022: two `{P}` audit tags are false when removed; `{P}` is reliable in only 6 of 12 sampled entries.
  - SCI-REV-0006 W1/W2: two state-of-field sentences out of date (verified counting exists; PB proof checking within a factor of 20).
- **Engineering.**
  - SCI-REV-0018 M1: "no such instance costs more than the worst product instance found" is false as worded; the worst-instance entries of ENG-RES-0008 at `n = 250, 350, 500` are lower bounds exceeded by up to `0.02005·na`.
  - SCI-REV-0008: the two-solver validation "cannot be regenerated".
- **Complexity.** SCI-REV-0019: the gadget is unattributed published work; the claim about the physical sign pattern (H2) is false.
- **Ensemble.** SCI-REV-0020: "generic" must mean "jointly generic" (Examples D1, D2); the margins of exactness are of order `10⁻³`–`10⁻⁵`.
- **Geometry.**
  - SCI-REV-0021: Theorem B at `d = 1` is Laurent–Poljak 1996.
  - SCI-REV-0023: "published bound is exponential" must be amended; Theorem K(a) is in print; Theorem L is vacuous at physical noise.

**Withdrawn or corrected statements of science's own** (DEAD_ENDS.md §A has SD1–SD77):
- SD43: a cost table sent as "an extension", which was in print (Block–Shetty).
- SD38: a "sharpening" that was not one.
- SD45: P2's "exact certificate in every instance" was over a pruned sub-domain; in 14 of 40 analyses that sub-domain misses the true minimum by 2–13 kcal/mol (Phe/strand).
- SD37: a prediction that constants are bounded by one side chain's solvation, false for charged chains.
- SCI-MSG-0033: three readings withdrawn (the loss between groups; identified sandwich members; a W[1]-hardness attribution).
- SCI-RES-0030: science's own reference checker "could accept a false bound" on malformed input; corrected.
- PRIOR_ART_MATRIX header: "'Not found' … is never a claim of novelty".

**"More precise than the model is accurate" findings:**
- Lys₁₂: width `8·10⁻⁵` nats against force-field uncertainty of order `kT` per residue, "four to five orders of magnitude" (SCI-MSG-0034 §2.3).
- An ordinary estimate replicates the certified 20-residue value to `10⁻⁴`.
- The evaluation tolerance is already a visible line of the budget.

**Negative results that close routes** (DEAD_ENDS §D):
- SD19: first-order envelopes for solvent terms in backbone torsions.
- SD20: "GB nearly pairwise" holds in RMS only.
- SD21: a fitted sup-norm is not a bound.
- SD22: low-order averaged data are worth "a polynomial factor at best".
- SD26: barrier transfer matrices hit PSPACE-completeness.
- SD27: "a Bayesian certificate fails silently on a dip (coverage 9 %)".
- Sign-blind bounds are 16–153 times too large on compact instances (a theorem, SCI-MSG-0024).
- Class bounds are pessimistic by two orders: Jensen gap 2–3 nats against class 71–178 nats.

---

## 8. Gaps relevant to an evaluation programme against external methods and experimental data

1. **No head-to-head against any external solver or method has been run.** toulbar2, OSPREY/K\*, VeriPB/CakePB, MaxOcc and maximum-entropy reweighting were all read about, never executed. B2, B5 and the B3/H7 baselines are unrun. The only "baseline" actually run is naive standard-error bars (B10).
2. **No experimental data of any kind.** No dataset is named, and none of the six §4 prerequisites has been met for any physical system. A target system, an observable, a forward model and its error model all have to be chosen from scratch.
3. **Model scope is narrow.** The instances are synthetic capped homopeptides and one patterned sequence on three ideal backbones, with rigid geometry. There is no protein, loop, ligand, buried site or flexible backbone. A ff14SB-only lineage and GBn2/OBC2 only; no explicit solvent, PB, QM or learned potential (B1 residuals (c) and (d) not run).
4. **Budget line 2 (discretisation) is unbounded for any real energy.** It is only quantified on a toy (A17.24, unrefereed). Line 4 (the evaluator tolerance) is assumed, not proved.
5. **Independent replication is thin on the physical side.** The P-pilot constants and the P9 stage-2 tables each exist in one implementation. The certificate addenda (13)–(18) and (23)–(25) are unrefereed, and the referee R14 was terminated. Every review is an internal AI review.
6. **Novelty classification under D-3's six classes is not done.** PRIOR_ART_MATRIX v1 uses a different numbered scale, a second version is "owed", and many sources are at abstract or snippet level.
7. **Structural Biology software does not yet exist** at this commit, so the evaluation protocol has not been exercised on any external claim. Science wrote it before the first claim.
8. **Inconsistencies to resolve:**
   - S-1…S-5 (protocol) against S-1…S-6 (SCI-MSG-0034).
   - RESEARCH_SYNTHESIS §6 says engineering answered nothing, against the status file (P7-E2 and R10-E1 done).
   - BENCHMARK_DESIGN's header ("Version 2 … checkpoint 29") predates its own B10 rows.
9. **Science's own suggestion for the first decisive external tests** (SCI-MSG-0034 §3):
   - planted-truth conformance;
   - a second implementation of every constant table;
   - baselines "run by their published recipes" (an exact CFN solver, provable ε-approximations, reweighting and replica estimates);
   - "identifiability first" for any observable.
