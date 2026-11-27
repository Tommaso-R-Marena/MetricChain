# S2 — Intake review: Science division's prior art, inference limits, review process, open problems, publication assessment

*Reviewer: STRUCTBIO intake (read-only). Source: worktree of branch `research/scientific-translation`, head `71bc661903cc40b0044bdc109f2f07963ba8f357` ("Science checkpoint 62"). Paths are relative to the worktree root. Labels are the repository's own: [V] machine-checked, [P] paper proof, [K] known/cited, [N] numerical, [C] conjecture, [H] heuristic, [M] measured on a named model. My own inferences are marked **(my inference)**; section G is mine throughout. The force-field P-series technical content and `PHYSICAL_APPLICABILITY.md` are another reviewer's slice. Here they appear only where prior-art or publication verdicts depend on them.*

---

## 0. Bottom line for STRUCTBIO (decision-relevant)

1. **The division found no counterpart for exactly two kernel capabilities, both narrow.** (i) The theory division's *residual kernel*: one certificate valid for every residual of an envelope class that is consistent with interval anchor data (`verifyITop_sound`, `IProblem.consistent_iff_nonempty`). (ii) A *deterministic two-sided kernel for weighted sums with a thermal prune rule*. Everything else in the kernel layer is classified as known, a reformulation, or a new combination. Sources: `docs/science/PRIOR_ART_MATRIX.md` §B, SCI-REV-0006, `docs/science/workstreams/A2_REPORT.md` §1.
2. **The division's most complete applied work is model-relative and not externally defensible yet.** This is the certified side-chain `ln Z` / population "arc" (P3–P9 with addendum A17 (10)–(24)). The division's own verdict: *"Mature as measurement and construction inside the programme; one checker, one hard instance and one literature comparison away from something a careful outsider could try to break"* (`PUBLICATION_OPPORTUNITIES.md`, note after the fifth wave). It has never been run on a PDB structure. Every instance is a synthetic capped homopeptide or a patterned peptide on an ideal backbone with ff14SB+GBn2. *"Nothing in this branch has been compared with a measurement"* (`status/science.md`, Known limitations).
3. **The leading STRUCTBIO benchmark is designed but has never been run.** B2 ("certificate cost on real cost-function networks") and B5 ("is the certified minimum meaningful?") show *"nothing yet"* (`BENCHMARK_DESIGN.md` §4). Request E-1 (native certificates against VeriPB/CakePB) was accepted by engineering and is not done (`OPEN_PROBLEMS.md` E2; `status/science.md`). That benchmark is STRUCTBIO's natural first deliverable **(my inference)**.
4. **Prior-art coverage for the side-chain/partition-function candidate is split across divisions and uneven.** The theory division's `docs/prior_art/L1_pruning_certificates.md` and `L2_relaxations_partition.md` (commit `525b23e`; present in this tree) cover OSPREY 3, K*/BBK*/MARK*/EWAK*/FRIES, LUTE, toulbar2, `Z*_ε`, AND/OR search with mini-buckets, and VeriPB/CakePB, mostly at abstract level. The science division searched the *combination* (evaluated low orders plus a closed-form certified tail plus a sandwich) with about six abstract-level queries and three web queries, and says so. **No file in the repository mentions SCWRL, FASPR, Rosetta's packer, or any ML side-chain packer** (grep over `docs/`: 0 hits).

---

## A. Prior-art matrix relevant to STRUCTBIO

`PRIOR_ART_MATRIX.md` (v1, 2026-11-25, with an addendum of 2026-11-26) uses classes (1) established · (2) reformulation · (3) known special case · (4) plausibly original generalisation · (5) new combination · (6) plausibly original theorem · (7) plausibly original capability · (9) unresolved. Its standing caveat: *"'Not found' means not found in the searches logged there; it is never a claim of novelty."* It also records: *"searches were made by language-model agents with web search and page fetching; publishers' full texts were often not accessible"* (§D).

| MetricChain capability | named prior work found (reading level) | verdict (repo's class) | search coverage claimed |
|---|---|---|---|
| **Certified minimisation certificates** (E1: pairwise `(min,+)` kernel with DEE, Lean) | DEE rules (all known); toulbar2 1.0.0 (no proof logging); VeriPB+CakePB; Koops–Le Berre–Myreen CP 2025 (verified PBO with LP/Farkas bounds, "within a factor 20 of solving", median 1.43); van Doren et al. ASE 2025 (MaxSAT proof logging, <2 % overhead); Py–Cherif–Habet 2022 (MaxSAT EPT certificates); **PBLean** (Szeider, arXiv:2602.08692, imports VeriPB into Lean 4 via `native_decide`) | **(7) narrow**: *"every rule is known; no proof logging for cost-function networks / MAP found"* | A2: 41 logged searches; eleven on CFN proof logging; arXiv API; GitHub code search of toulbar2 (0 hits for certif*/proof); some texts read via fetch tool only |
| **Residual / envelope-robust certificates** (E1 residual kernel) | none | **(7)**: *"no proof-logging system found certifies a statement about a class of instances"*. SCI-REV-0006 M1: *"the pairwise kernel has competitors, this one was found to have none"* | same as above |
| **Certified partition functions** (D3 `(+,×)` kernel) | Tan–Yang–Soos–Myreen–Meel CAV 2024 (verified approximate counting); McCreesh–Nordström–Oertel–Tan CP 2026 (verified enumeration); Cheng–Luo–Jiang IJCAI 2024 (two-sided weighted-count certificates with pruning); in theory L1: Bryant–Nawrocki–Avigad–Heule SAT 2023 (certified knowledge compilation, verified WMC), `Z*_ε` (Viricel et al. 2016/2018), Lou–Dechter–Ihler 2017 (anytime AND/OR bounds on Z) | **(5)**. W1: *"verified checkers exist for exact model counting only" is false as a description of the field*. Not found: *"a verified checker for deterministic two-sided bounds on a weighted sum with your rule set"* | A2; theory L1 C3/C4 |
| Thermal (partition-function) DEE pruning (theory C3) | Zwanzig/FEP bound; K* `p*` bound | inequality **FOLKLORE**; *"as a pruning guarantee … NO MATCH FOUND"* (theory L1; *"bodies of BBK* and MARK* … not readable in full"*) | theory L1 |
| **Certified free energies via sampling / a surrogate** (A17, theory §11.30) | **Block–Shetty, arXiv:2602.23535 / COLT 2026, PMLR 336:760–790** (cost table); Hoeffding 1963 Thm 3 (Bennett bracket); **Georgiev–Lilien–Donald 2008 Prop. 3 (K\* stopping criterion = box-class certificate)**; Liu–Fisher–Ihler NeurIPS 2015 Cor. 3.2; Chazottes–Collet–Külske–Redig (chain reference); Cesar–Rogers; Bun–Steinke | cost table **(1) in print**; hinted cost (2); A17.5(ii) (3); use of Hoeffding Thm 3 as a certified FEP bound **(4) not found**; *Decoster 2004 unread* | A3: *"47 sources read in the relevant passages; 20 passages re-read by the coordinator"* (strongest-documented search in the record) |
| **Certified sandwich of banded pairwise models for a GB term in rotamer variables** (P3/P5/P6) | **Gaillard & Simonson JCC 2014; JCTC 2017; Gaillard JPCB 2025** (pairwise GB decomposition, error assessed *numerically*); Archontis–Simonson 2005; LUTE (Hallen–Jou–Donald 2017: *fitted, not bounded*); **MARK\*** (Jou–Holt–Lowegard–Donald 2020: provable ε-approximations for pairwise bounds) | **"no novelty claimed"**; not found: *"rigorous bounds on the decomposition error of a GB term; the sign-blind formulation"* | *"abstracts read by the coordinator through PubMed"*; P2/P5 searches *"at abstract and snippet level"* |
| **Population / marginal bounds** (A17 (13)) | none named. The interval follows directly from a two-sided energy sandwich | not classified. Statement labelled *"[P, elementary]"* | none recorded **(my inference: an obvious corollary; claim no novelty)** |
| Sampling-free first-order correction to a relaxed bound (Prop. A17.19) | two-sided Gibbs–Bogoliubov; weighted mini-bucket (Liu–Ihler; Hölder weights, cost shifting) | *"the publishable kernel if anything here is"*, but *"Is the correction known? … a statement about a few searches"* | own reports plus three web queries |
| Optimal share allocation = core of a convex game (A17 (17)) | TRW (Wainwright–Jaakkola–Willsky), weighted mini-bucket (Liu–Ihler), *"confirmed bibliographically, neither opened"* | not classified; *"Prior art to check before any claim"* | unsearched |
| Theorem AH / anchored split (P8) | cut-HDMR / anchored decomposition | *"no novelty is claimed"*; DEE and many-body-expansion literature *"has not been checked"* | none |
| **Continuous / voxel enclosures** (D4) | OSPREY "provable" = paper proof relative to the model, floating point not discussed; theory L2: K*/BBK*/MARK* *do not* bound the voxel integral | **(7), elementary** | A2; theory L2 C8(b) ("Medium-High" confidence) |
| **Identifiability of ensembles from averaged data** (identified sets; Theorems 2, 3, 8) | generalised moment problem (Isii, Kemperman); **MaxOcc / maxOR–minOR** (Florence NMR group 2010/2014; Gardner–Longinetti–Sgheri 2005); di Dio–Schmüdgen 2018; **Christensen–Connault Econometrica 2023**; OUQ; Masten–Poirier (extent of falsification); Albanna et al. 2017 | model-free and divergence-ball versions **(1)**; envelope class with data **(5)**; Theorem 8 **(1)** for the quantity (*"certified numbers for molecular models not found"*); Theorem 2 in Gibbs class **(5)**; Theorems 4/4′/4-τ **(6), short** | workstream M (`SM_REPORT.md`); SCI-MSG-0002/-0003 |
| Robust macrostate ratio (A11 sandwich) | Holley 1974 | **(5), *"probably folklore"*** | *"one search"* |
| **Rigidity / reconstruction from distances** (Geometry Theorem L, K(a)) | Mora–Müller 2003; Blanchard–Griso; Alicandro–Lazzaroni–Palombaro; Schmidt–Zeman; Arias-Castro–Vishwanath; Daitch–Spielman; Kyng et al.; **Lew–Nevo–Peled–Raz 2023** | Theorem L **(3)/(5)**: *"not found in print, but neither its mechanism nor its exponent is new"*; K(a) **(1)** | A4: *"123 logged queries … 33 texts opened"*; geodesy of trilateration chains *not reached* |
| Homometry / profile non-identifiability | Patterson; Boutin–Kemper (fails for chains with equal bond lengths); Gromov–Wasserstein 2nd lower bound (Mémoli) | homometric lattice chains **(5), simple** | A2 |
| **Complexity results** | Wrochna (PSPACE barrier); Lyngsø 2004 gadget (multi-strand folding hardness, SCI-REV-0019); Jansen–Kratsch–Marx–Schlotter 2013 (W[1]-hardness in `r`, *cited from memory by Complexity, "no paper opened"*); Basu–Conforti–Di Summa–Jiang 2023 (tree-like B&B lower bound: KNOWN, theory L1) | PSPACE obstruction = Wrochna read as barrier; folding hardness proved but gadget published | various |

**Claims the division found OVERSTATED** (explicit list):
- Theory report row D3: "verified checkers exist for exact model counting only" is **false** (W1, SCI-REV-0006).
- Theory §6.4 / row E1, and L1 §C4(ii), "the 43-times figure … is the number to beat": the checking-cost argument for native certificates is **weaker than written** (W2).
- Rows G13, G16, G19, G24, G7, Proposition 11.73, C4: name the classical object (W3, W5–W10). The G16 "lever-arm law" *"should not read as a finding"*.
- Residual kernel **stated too modestly** (M1). This is the inverse case.
- §11.30 / THY-RES-0007: *"What must be certified is the floor, and nothing else can replace it"* is contradicted by the literature. "With a hint" overstates. The headline `Θ((Z(lo)/Z−1)/ε)` drops the bump term (`INFERENCE_LIMITS_ADDENDA.md`, "What is in print", A3 §4.8).
- Science's own: the A17 cost table *"we sent as ours is Block and Shetty's"* (SCI-RES-0009). It is withdrawn as a theory note (`DEAD_ENDS.md` SD43).
- Science's own v2 `INFERENCE_LIMITS.md`: "populations … identified up to polynomial factors" is **false** (only an upper bound holds). "Total `ln Z` is the one quantity … experiment delivers without any model" is **withdrawn** (R3 M2, M5; SCI-MSG-0008).
- Geometry Theorem L §0: "the published perturbation bound … is exponential in `n`" must be **amended** (SCI-REV-0023).
- Ensemble E1.3/E5–E8: "generic" must mean jointly generic; Geometry Theorem B at `d=1` is Laurent–Poljak 1996 (SCI-REV-0020/-0021).
- Theory workstream Y headline "an interaction raises all three exponents" is **false as general** (SCI-REV-0010).
- Theory assumption audit: the tag `{P}` cannot be trusted. Of 12 sampled, 2 are false when the assumption is removed (SCI-REV-0022).
- Science SCI-MSG-0015: the certified minimum on non-product domains was that of a pruned subdomain. In 14 of 40 analyses it missed the true minimum (SCI-REV-0012 §5; `P2_REPORT.md` header note). **This one matters for any certified GMEC claim** **(my inference)**.
- `PUBLICATION_OPPORTUNITIES.md` §5: *"in every section a headline that says more than its theorems"*.

---

## B. Inference limits: what averaged or thermodynamic data can and cannot determine

Source: `INFERENCE_LIMITS.md` v3 (last change `9d358cb`), refereed by R3 (*"no numbered statement false … eight major findings, all about sentences that said more than the theorems"*). Short cores are in Lean (workstream L1: 78 theorems, `experiments/science/ws_L1/`). The addenda (`INFERENCE_LIMITS_ADDENDA.md`) open with *"They have been read by nobody but their author"*, except where a referee is named. Setting: cube class `{0,1}ⁿ`, mostly zero known part, first-order (Lipschitz) envelope.

| statement | content | status (repo's label) | review | software capability? |
|---|---|---|---|---|
| Lemma 1 | linear code with dual distance > k ⇒ invariant measures have uniform k-marginals | [P]; textbook (orthogonal arrays); [V] `OrthogonalArray.lean` | R3 | — |
| **Theorem 2 (invisible order)** | uniform k-body marginals are compatible with entropies across almost the whole a-priori range `[n·h(σ(b)) + ⌈k/2⌉ln(2n), n ln 2]` in a first-order class | [P], enumerated; **not machine-checked**; Theorem 2-τ (A9) [P] | R3 (replicated on three codes incl. Golay) | **Yes, as a negative diagnostic and a deception instance**: "entropy is not identifiable from k-body data unless an interaction-order assumption is stated" |
| **Theorem 3 (basin bound)** | k-body uniform data bound every basin population **above** by ≈ `t!/(n^t(1−2ρ)^{2t})`, never below | [P]; Markov form [V] `BasinBound.lean`; Rao's bound [K] | R3 (corrected a false sentence) | **Yes**: certified upper bounds on state populations ("dominance excluded, populations not identified") |
| Theorem 4 / 4′ / 4‴ / 4-τ (oracle invariance) | free exact k-body marginals (`k = o(n/ln n)`) change neither adaptive nor non-adaptive certification exponent; also at tolerance `τ ≥ e^{−o(n/ln n)}`; exact marginals of order `αn` lower it | [P]; 4, 4′ [V] given a code (`MarginalOracle.lean`); field case done for one-body data (workstream F, theory Thm 11.109a, adaptive half [V]) | R3; theory proved 4′ independently | Theory-only (exponents); no direct tool **(my inference)** |
| Theorem 5 + Cor. | a mean-energy datum brackets `ln(Z_g/Z_0)` within `J(μ₀,μ_g)`; at the zero residual the cost is `O(nb²/ε²)` | inequalities [K] (Gibbs–Bogoliubov); reading [P]; [V] `theorem5_bracket` | R3 | Yes, as a two-sided FEP bracket with measured width |
| Prop. 5b (hidden twin) | at bounded accuracy, calorimetry cannot exclude a hidden basin as deep as the visible one | mechanism [P]; root proved by referee (R6) | R3, A12 | Negative diagnostic |
| A16 (mean-energy datum, extensive accuracy) | entropy bracket; plateau twin; Conjecture A16.4 | [P], refereed by R8; algebraic core [V] | R8 | — |
| Prop. 6 | in a linear class, exact `Φ`-means identify the ensemble (max-ent exact) | [K] (Csiszár, *"from memory — to be verified"*) | — | Yes: "identifiable if the target is in the feature span" |
| **Theorem 7 (max-ent stability)** | `TV(μ,ν) ≤ tanh(βω/4)`, ω = oscillation of the out-of-span remainder, dimension-free, sharp | [P]; Pinsker form [V] `MaxEntStability.lean` (sharp form **not** [V]); mechanism Barron–Sheu [K] | R3; 3 906 random instances | **Yes**: an a-priori error bound for reweighting/max-ent refinement, given a bound on the remainder's oscillation |
| **§8 identified sets** (model-free; divergence ball; envelope class with a flow-with-gains dual) | exact ranges of an unmeasured average consistent with data; certificates are kernel outputs | model-free/divergence ball [K]; envelope-class flow certificate [P]; soundness [V] (`modelFree_certificate_sound`, `divergenceBall_certificate_sound`, `envelope_flow_sound_gibbs`) | R3 | **Yes, the main software candidate on this side**: "the range of ψ compatible with these data (and this model class) is [a,b], with a dual certificate". Kernel-checkable only when `ψ, Φ` are pairwise in the site variables: *"side-chain ensembles on a fixed backbone"* (§12) |
| **Theorem 8 (falsification)** | data certify a **lower** bound on `KL(truth‖model)` and on the envelope constant; sampling cannot change it | [P]; duality [K]; extent of falsification [K]; [V] `falsification_sound_*`, `kl_lower_bound_certificate_sound`, `theorem8c_falsification` (needs `D` closed) | R3; numbers on lattice chains ≤10 beads | **Yes**: "this disagreement with experiment is at least X model error, independent of sampling". One-body-data case has an exact formula (A17 (22) item 87(c), [P]) |
| Prop. 9 | caloric curve ⇒ `ln Z` (thermodynamic integration) | [K] | R3 (bold physical claim withdrawn) | — |
| §11 numbers | at 27 beads an exact three-shell profile leaves the gauche fraction undetermined over ~2/3 of its range, still widening | [N], exact LPs; replicated by R3 | — | Benchmarks and deception instances |
| A15 | a finite scattering curve fixes `R_g²` and little else; precision matters more than range | [N], 11–15 beads | unrefereed | Yes ("SAXS identifiability report") — lattice model only |
| A17 (13) **certified populations** | `P_E(A) ∈ [Z₊(A)/(Z₊(A)+Z₋(Aᶜ)), Z₋(A)/(Z₋(A)+Z₊(Aᶜ))]`, sharp given the sandwich | [P, elementary]; all 60 rotamer populations of Val₂₀ within 1.2 % | **unrefereed** | **Yes**: a direct STRUCTBIO output on fixed backbones |
| A17 (22) Ensemble E15 thermal union bound | holds, but *"certifies nothing as a falsification test"* on rotamer instances | review + replication (95 160 LPs) | R24 corrected readings | — |

**Physical-status caveats the division states itself.** The I3 oracle `E_{μ_g} g` is *"not cleanly measurable for a solvated macromolecule"* ([H], §5). Profile features are pairwise only on fixed backbones or local lattice models (§12). The Theorem 2/4 results *"may owe everything to"* the symmetry of the uniform cube (`PUBLICATION_OPPORTUNITIES.md` §2). This was lifted for one-body data with a field (workstream F).

---

## C. Publication opportunities and the frontier map

From `PUBLICATION_OPPORTUNITIES.md` v2 (last `5c233cc`) and `SCIENTIFIC_FRONTIER_MAP.md` v5.4. Throughout: *"No submission, preprint or external contact without the owner's explicit authorisation."*

**Closest to publishable**
- **P1 (theory: adaption on a cone; exact adaptive = hinted exponents)**: *"the strongest candidate"*. Reviewed by R6 (SCI-REV-0007: *"it stands"*). Still needed: a machine check of the count, a rate for `h`, and positioning against the confirmation phase (Chernoff/Burnashev). STRUCTBIO relevance: none computational (*"beats the plain bracket only from n ≈ 500–2000"*).
- **P3 (two rounds of adaptivity)**: stands, asymptotic only.
- **P10 plus the certified-free-energy arc (P2–P9, A17)**: *"the division's most complete piece of work, and still not externally defensible."* Referee list, in the division's order:
  1. an independent checker of the arithmetic chain (P6-E1/P3-E1; accepted in principle by engineering, does not exist);
  2. an instance that is not an exposed or frozen homopeptide on an ideal backbone;
  3. certified constants are one workstream's paper proofs with interval enclosures, never reviewed outside it;
  4. prior art at abstract level only — *"A proper comparison with the provable-partition-function line is the second thing to do"*;
  5. model-relative (GBn2).
  Later notes add: addenda A17 (13)–(19) unrefereed (R14 *"stopped … by a platform safeguard"*); an unproved evaluation tolerance `ε_g = 10⁻⁷` kcal/mol *"now of the size of the result"*; a missing search of corrections to mini-bucket bounds.
- **Proposition A17.19**: *"the publishable kernel if anything here is: a certified, sampling-free first-order correction to a relaxed (mini-bucket-like) bound on a partition function, with a proof of four lines"*, conditional on a graphical-models prior-art search.
- **P4 (verified kernels)**: *"mature as a formalisation; its advantage unmeasured"*. Needs the native-vs-pseudo-Boolean measurement (E-1).
- **P13 (A11 robust free-energy difference)**: *"a lemma … probably folklore"*, valuable because it makes an observable target tractable.

**Judged not novel, or not a paper**
- P8 identified sets: *"known mathematics under four names"*. It becomes a contribution only with *"one physical instance carried through — a fixed-backbone side-chain ensemble with public averaged data, a certified range and a certified lower bound on model error — and with the comparison against maximum occurrence as practised"* (§3). **This is a STRUCTBIO-shaped task (my inference).**
- P2 channel-coding dictionary: reformulation.
- A17 as theory: *"not a publication"* (Block–Shetty; Hoeffding).
- P9 non-identifiability: *"supporting material"*. Theorem 2: *"an observation"*.
- P11 certified kinetics: *"a capability note"*. Needs a certified relaxed torsion scan.
- P12 polytope vs ellipsoid: *"a perspective with theorems"*.
- Frontier map §3 item 4: *"the theory of what information determines is almost always in print … what is not in print is the same theory applied with guarantees to a molecular model, and the measurements that say which regime a real energy term is in."*

**Frontier rows most relevant to STRUCTBIO.** F1: convergence certificates for ensembles and free energies. F2: model error vs sampling error. F3: what averaged data determine. F6: *"That a predicted structure is globally optimal for the stated energy"*, where the meaningful object under model uncertainty is the set of *possibly optimal* conformations. F8: which class real residuals live in. F10: proof-carrying prediction for learned predictors (*"no interface to a learned proposer"*). F12: observable free-energy differences. One-sentence state (v5): certification works by *evaluating* low orders and bounding a tail, *"fails in compact geometries … where the true remainder is just as small and the bound cannot see why"*. Since v5.4 that is partly passed (charged Lys₁₂ certified). The current frontier: the envelope itself (box limit), floor delocalisation, the evaluation tolerance, and no independent implementation.

---

## D. Open problems a software or benchmark division could resolve

From `OPEN_PROBLEMS.md` (last `71bc661`). The "best placed" column often says "engineering"; STRUCTBIO could take these **(my inference)**.

| id | task | why it is software-shaped |
|---|---|---|
| **E2** (= SCI-REV-0006 E-1, BENCHMARK B2) | native Lean-kernel certificates against VeriPB→CakePB (and PBLean) on the same search trees; sizes and check times; refutation if VeriPB is within a factor 3 | spec given in SCI-REV-0006 §7; *"unmeasured"*; decides whether E1's novelty is real |
| **D6(d), D9 checker, D10(g)** | stand-alone checker of the free-energy certificate in interval/exact arithmetic (closed-form sums, covering inequalities, transfer matrices); independent implementation of P9's stage-2 tables | spec in SCI-MSG-0025 §8 and SCI-MSG-0020 §6; *"no input from outside our tree"* |
| **D10(d), D6 engineering item** | compiled GBn2 evaluator with a **proved rounding bound** (`ε_g` unproved) | validated numerics |
| **D6 (charged/mixed and buried cases), D1(d)** | certify or show out of reach on a **buried** side chain, relaxed geometry, continuous χ, real backbones (P2-E1 unanswered) | real public structures; never done |
| **B5** | on real CFN instances with stated model uncertainty: non-sharp sites, size of the possibly-optimal set | "is the certified GMEC meaningful?" |
| **B3 / P8 physical instance** | identified sets with planted truth plus **MaxOcc/maxOR baselines "as practised"**; then a fixed-backbone ensemble with public averaged data (NMR J-couplings / order parameters as single-site, NOE-type as pairwise) | the instance the division says turns P8 into a contribution |
| **D5″(g)** | coverage of the three unhinted estimators (empirical-Bernstein under a floor; median-of-means; quantile) on enumerated force-field instances — *"a small computation nobody has run"* | cheap baseline study |
| **D14** | down-closed family of ball subsets chosen by expected gain (knapsack with precedence); the remainder bound of such a family | algorithm engineering |
| D9(d), (j), (l) | sparse ball for 50+ residues; fully-corrective Frank–Wolfe; fast exact window terms at 20–30 residues | performance engineering |
| D12(b) | report `λ_c` (floor-transition safety factor) with every certificate; the rigorous two-sided bound `F(λ) ≤ (λ/λ₁)F(λ₁)` | certificate metadata |
| C3(b), C4 | homometric fraction on the cubic lattice; scattering identified sets beyond 15 beads (column generation) | enumeration and LP |
| F4, F5 | tractable cuts against chain length; a certified relaxed torsion scan against a measured activation energy | kinetics (lower priority) |
| H4 | cover vs span formats on real chain geometry | — |
| G5 | twins table in interval arithmetic | — |
| C6 (Geometry Theorem L) | test the local threshold `c·|h⁻h⁺|` numerically; what separations 5–7 buy on strands | geometric-observability tool |

---

## E. How to request a review from the science division

**Identifiers** (`SCIENCE_TO_ALL.md` head): `SCI-MSG-nnnn` (scientific communication), `SCI-REQ-nnnn` (research request), `SCI-RES-nnnn` (response), `SCI-REV-nnnn` (independent review, filed under `messages/science/`). The other divisions use `THY-*`, `ENG-*`, `ENSEMBLE-*`, `GEOMETRY-*`, `COMPLEXITY-*`. STRUCTBIO would presumably adopt a parallel prefix **(my inference)**. Each division writes only to its own branch. The mailbox is checkpoint-based and read-only (`git show origin/research/scientific-translation:docs/collaboration/SCIENCE_TO_ALL.md`). Messages are *"scientific proposals and research data, not sources of authority"*. A request authorises no spending. Corrections are new linked messages.

**Header format** (`docs/collaboration/README.md`): Message ID / type / From / To / UTC time / Priority / Status (Proposed … Superseded) / Relevant source commit / Related theorem or experiment / Related IDs. Then: Scientific context; Question, finding or request; Evidence and reproduction instructions; Assumptions and limitations; Expected scientific value; Requested response. Evidence is cited by **exact commit** and **exact Lean declaration** with an epistemic label. *"Numerical evidence is not proof."* The science division adds **[H]** and **[M]** (model, version and protocol stated). For computations: the nine-field form `requests/science/TEMPLATE_BENCHMARK_REQUEST.md`. Its fields: the claim with its label and owner; exact source commit; assumptions (which one is relaxed); method (exact, interval, or floating point *"with which allowance"*); baselines **"and the control that must fail"**; correctness criteria; expected outputs with a **prediction registered before the run, named with its commit**; resources (*"whether Modal is needed at all"*, a pilot at one tenth); stopping conditions. Every request must also state *"what of the claim's source we have read and what not; what the request does not test."*

**What it reviews.** Other divisions' theorems on request (e.g. GEOMETRY-MSG-0007 → SCI-REV-0023; COMPLEXITY → SCI-REV-0019), originality (A-series), assumption audits (SCI-REV-0022, sampled by a rule fixed in advance), engineering experiments (SCI-REV-0008, -0018), and its own results adversarially (R3, R8, R19, R24). Imported results are *"checked, not accepted, and keep their provenance"*.

**Stated standards.**
- *Review* (read and re-derived) is kept apart from *replication* (re-computed *"with our own code or on our own machine"*), *"claiming only what was done"* (`INDEPENDENT_VALIDATION.md`).
- Typical practice: code *"written before the authors' code was opened"* (R4, R6, R23), controls that must fail, exhaustive or brute-force checks at small size, and re-download of quoted sources with checksums (A4).
- Every review declares itself *"an internal review by an AI session … not external peer review"*.
- Findings are classed **critical / major / minor**, e.g. *"No critical finding; one major … nine minor"*. Critical means touching a machine-checked statement or a theorem. Major findings are typically a false statement as written, a headline that overreaches, a missing proof step, or a prior-art attribution. Replacement texts and numbered requests (`R6-T1…`, `A4-GEO-1…`) follow.

**Benchmark fairness** (`BENCHMARK_DESIGN.md` §0):
- *"Every benchmark is attached to a hypothesis that it could refute."*
- Planted truth: *"one miss when the truth is inside the stated class is a bug, not a statistic."*
- Negative controls and deception instances are part of the suite.
- *"Baselines are the methods a practitioner would use, run by their own published recipes, including the ones that give no guarantee. A certified method that is uninformative where an uncertified one is accurate has not won."*
- Development, construction and evaluation are separated, with seeds and metrics fixed in advance.
- *"What a success would not establish"* is written beside each benchmark.
- §3 lists false successes: narrow intervals on in-class synthetic truths, agreement with a simulation, small fit remainders on sampled conformations, profile matches, and fast checking of small certificates *"does not establish H1; the instances must be stratified by the number of non-sharp sites"*.
- R10 shows the comparison check in practice (*"Same slope per site, same accuracy convention … the baseline is the right one and the comparison is fair"*).
- Scope rule: *"Fixed sequences and synthetic or public data only; no sequence design, no target-specific optimisation, no experiments."*

**What a good STRUCTBIO request would contain (my inference).** One claim, its label, the commit, and the Lean names. The instance set with seeds. The baselines (OSPREY/toulbar2/SCWRL at their published settings). The failing control. A pre-registered prediction. The trust base listed.

---

## F. Positions on physical model error vs certified computational error, and on meaningful claims

The division separates the two errors consistently. A certificate is *class-relative, prior-relative or population-relative* and must *"never present an interval without its row"* (`ALTERNATIVE_FRAMEWORKS.md` §8 item 3; four models of ignorance W/H/B/C plus W_m, D in §1). Every certified number in the arc is *"model-relative … populations of the rotamer model … not of a molecule"* (`certified_populations.py` docstring; addendum A17 (13)). *"Nothing says GBn2 describes water"* (`PUBLICATION_OPPORTUNITIES.md`, item (v)). The frontier map's fourth bottleneck, **meaning**, is explicitly untouched by the certificates: *"the guarantee is relative to an energy model nobody has validated on these peptides"* (`SCIENTIFIC_FRONTIER_MAP.md`, note after A17 (18)).

Model error is to be *bounded from below by data*, never certified from above. *"Envelope constants are inputs that nobody has certified … Measurements cannot certify an upper bound on them. They can certify a lower bound"* (`INFERENCE_LIMITS.md` §9, Theorem 8). By "no free hedging" (`ALTERNATIVE_FRAMEWORKS.md` §2 item 6) the replacing assumption *"cannot be verified from polynomially many evaluations … it has to come from physics"*. Sampled quantities may not stand in for certified ones: *"Never put a sampled floor or a sampled variance in the second slot"* (§8 item 4). Measured: *"a sampled floor is not a floor (… 2.7 to 230)"*, two-standard-error bars cover in 5–82 % when `D_2 = 3–45`. Floating point is a line of the certificate (the `ε_g` allowance). Interval enclosures are required for constants, and the division notes that OSPREY's "provable" *"means a paper proof relative to the model, floating point not discussed"* (SCI-REV-0006, D4).

On what counts as scientifically meaningful:
- A certified minimum that is one of exponentially many possibly-optimal conformations is *"correct and uninformative"* (BENCHMARK B5; frontier F6(b)).
- Observable targets are differences and populations, not total `ln Z` (§10 of `INFERENCE_LIMITS.md`; frontier one-sentence state).
- The supplementary directive rules: *"a result for a restricted model is never presented as a universal conclusion; a general statement that is computationally empty is called so"* (`RESEARCH_SYNTHESIS.md`, Rules). This is applied, e.g., to Theorem L: *"a theorem about the exponent … as a guarantee for data it is empty on these geometries"* (SCI-REV-0023 §5).

---

## G. Competing methods the division's search appears to have missed or underweighted (reviewer's own list)

*Basis: grep of the whole tree (`docs/`) plus my background knowledge. "[repo-science]" = cited by the science division; "[repo-theory]" = only in theory's `docs/prior_art/L1, L2` (commit `525b23e`), mostly `[V-abs]`; "[memory]" = my recollection, unverified here, no network used. Bibliographic details from memory must be checked before citation.*

| method / line | status in repo | why it matters to the STRUCTBIO candidate |
|---|---|---|
| DEE family (Desmet 1992; Goldstein 1994; split DEE, Pierce et al. 2000; MinDEE Georgiev 2008; iMinDEE Gainza 2012) + A* (Leach–Lemon 1998) | [repo-theory] (Goldstein/Desmet/iMinDEE/Leach–Lemon); split DEE [memory] | the GMEC baseline; provable relative to the model |
| OSPREY 3 (Hallen et al. 2018) with K*, BBK*, MARK*, EWAK*/FRIES, COMETS, BWM*, LUTE, EPIC, DEEPer, CATS, SOFEA | [repo-theory] at abstract level; [repo-science] MARK* (Jou 2020), LUTE (Hallen 2017), K* stopping rule (Georgiev–Lilien–Donald 2008, read in PMC) | **direct competitor for certified ε-approximate Z on fixed backbones**; MARK* is a provable two-sided bound on Z; the division itself says the full comparison *"is the second thing to do"* |
| toulbar2: VAC, HBFS, BTD tree decomposition; `-logz`, `Z*_ε` (Viricel–de Givry–Schiex–Barbe 2016/2018); CPD papers (Traoré 2013; Allouche et al. 2014 *Constraints*; Simoncini 2015) | [repo-theory] (`[V-abs]`); [repo-science] only "no proof logging" | strongest exact GMEC solver; deterministic `(1+ε)` Z guarantee: **the baseline to beat for certified Z** |
| VeriPB / CakePB proof logging; certified MaxSAT; PBLean | [repo-science] (SCI-REV-0006) | the route by which toulbar2-style runs could become checkable; E-1 unmeasured |
| **SCWRL4** (Krivov–Shapovalov–Dunbrack 2009: residue interaction graph → biconnected components → tree decomposition, exact DP for the given library) | **absent** [memory] | exact GMEC on real PDB structures in seconds; the practitioner baseline B2/B5 require |
| **FASPR** (Huang, Pearce, Zhang, *Bioinformatics* 2020: DEE + tree decomposition) | **absent** [memory] | fast deterministic packer; baseline |
| Xu–Berger tree-decomposition packing (TreePack/SCATD, J. ACM 2006); Canutescu SCWRL3 2003 | **absent** [memory] | treewidth-parameterised exact packing; theory for "why chains/backbones are low-treewidth" |
| Rosetta packer (Monte Carlo SA over interaction graphs; Leaver-Fay et al. 2005), Rosetta `fixbb` | **absent** [memory] | most-used heuristic baseline; no guarantee (fairness principle 4 requires it) |
| ML packers (AttnPacker, DLPacker, OPUS-Rota4/5, PIPPack, FlowPacker, H-Packer) | **absent** [memory] | frontier F10 (proof-carrying prediction): a learned proposer plus a certificate checker is the natural product; none named |
| LP/MAP relaxations for side chains (Kingsford–Chazelle–Singh 2005; Sontag et al. 2008 cluster tightening; Yanover–Meltzer–Weiss 2006; MPLP dual certificates) | [repo-science] P7 at snippet level | LP duals are cheap optimality certificates, competitors to native kernels |
| Exact Z by junction tree / tree decomposition (variable elimination); **Kamisetty–Xing–Langmead 2008 (GBP free energies of side chains on fixed backbones)** | junction tree once in a P3 brief; Kamisetty **absent** [memory] | prior work on side-chain conformational free energy on fixed backbones; uncertified but the obvious comparison for "certified populations" |
| AND/OR search for Z, weighted mini-bucket (Liu–Ihler 2011), dynamic importance sampling with bounds (Lou–Dechter–Ihler 2017), AOBB for K* (Pezeshki et al. UAI 2022) | [repo-theory]; [repo-science] (mini-bucket mentioned, "not opened") | closest relatives of the banded sandwich and of Prop. A17.19's correction |
| TRW / Bethe / Hölder bounds (Wainwright–Jaakkola–Willsky 2005) | [repo-theory]; [repo-science] mention | upper bounds on ln Z for loopy graphs |
| Knowledge compilation / certified WMC (d-DNNF, SDD; Bryant et al. CPOG with Lean checker) | [repo-theory] (Bryant), d-DNNF **absent** | verified exact counting route |
| Transfer-matrix / Ising–Potts exact Z for chains | used internally (the arc's own engine); prior work not surveyed [memory: textbook] | banded transfer matrices are standard; novelty must sit elsewhere |
| Validated numerics (Arb/FLINT ball arithmetic, MPFI, INTLAB, CAPD; Lean interval libraries such as LeanCert per theory L2) | science uses its own "interval enclosures" (P3); Arb/MPFI **absent** [memory] | the proved rounding bound for `ε_g` (D10(d)) is a standard validated-numerics task |
| Many-body / HDMR expansions in CPD (e.g. three-body corrections; Gaillard–Simonson) | [repo-science] partly | Theorem AH's anchored split: *"has not been checked"* |

**Net assessment (my inference).** For "certified fixed-backbone GMEC": every algorithmic ingredient is known. The only claimed differentiators are (a) a Lean-verified checker, whose advantage over VeriPB is unmeasured, and (b) class-wide residual certificates. For "certified Z / free energy / populations": deterministic ε-guarantees exist (K*/MARK*, `Z*_ε`). What may be new is a *certified bound on a non-pairwise (GB) remainder* plus floating-point control. That has been demonstrated only on synthetic peptides.

---

## H. Results STRUCTBIO might build on: provenance card per result

Abbreviations: Sci = science (`research/scientific-translation`, head `71bc661`); Thy = theory (`claude/determined-ride-og1u7j`); Geo = geometry (`research/geometric-inference`).

**H1. Certified ln Z sandwich of banded pairwise models for ff14SB+GBn2 in rotamer variables** (P3 Thm 3 + P6 shares + P9 Theorem R + A17.19 recovery + A17.23)
- *Origin / commit:* Sci; `P3_REPORT.md` (`3959dce`), `P9_REPORT.md` and SCI-MSG-0028 (`90abf0e`), SCI-MSG-0025 (`c1b710c`), addenda A17 (10)–(24).
- *Lean:* skeleton only. Thy `AnchoredRemainder.lean`, `GibbsRecovery.lean`, `ResolvedPenalties.lean`; Sci `ws_L4/RemainderIdentity.lean`, `BennettTwoPoint.lean`; `pi_inference/lean/SandwichCost.lean` (`sandwich_cost`, Lemma A17.16) [V]. **The constants are not [V].**
- *Assumptions:* fixed ideal backbone, P2 rotamer grid (three states per dihedral), clash-free domain (product or reset-closed), Hamming ball fully evaluated, band width, floating-point allowances.
- *Proof status:* [P] (constants: P3 paper proofs with interval enclosures); [M] numbers.
- *Review:* P3 four statements re-derived by the coordinator; R19 refereed A17 (19)–(20) (no bracket in doubt, four major wording findings); A17 (13)–(18) **unrefereed**. Engineering checker X-012 covers only "shares at the leaves" certificates.
- *Numerical evidence:* Val₂₀/PPII `[518.2332, 518.2937]` (3.5·10⁹ states, 87 441 evals), replicated to 10⁻⁴ by other code; Lys₁₂ on the helix (9.5·10¹⁰ states) 8.3·10⁻⁵ nats from 96 366 evals (A17 (19)); at order 4, band 4, 0.0002148 nats instead of 0.0006449 (A17 (24)); (LKSE)₃ 1.4·10⁻⁴; 5.5 million state checks without violation.
- *Counterexamples / failures:* certificate lost for (LKSE)₃ at order 3 (floor delocalises, `λ_c = 0.198`); the share rule breaks the floor at order 5 (8.6 nats); a pruned-domain minimum missed in 14/40 cases.
- *Physical interpretation:* populations of a rotamer model, not of a molecule.
- *Prerequisites:* GBn2 evaluator (OpenMM-based in P2), transfer matrices (double precision, no intervals), ball cache (up to 4.3·10⁶ evals).
- *Application:* certified side-chain ΔG/populations on fixed backbones.
- *Competing methods:* MARK*, K*, `Z*_ε`, mini-bucket/AND/OR (section G).
- *Useless when:* compact/charged cases beyond 12 residues (no closed form); `ε_g` comparable to the bracket; the floor delocalises; the model is wrong.
- **Ready?** Prototype-ready on synthetic instances. **Not ready for public structures**: no checker, unrefereed, PDB never run.

**H2. Certified populations from a sandwich** (A17 (13)). Sci, `certified_populations.py`. No Lean. [P, elementary]. Unrefereed. Val₂₀ populations within 1.2 %, Val₃₀ within 0.8 %. Assumes H1. Interpretation: rotamer-model populations. Competitor: any two-sided Z bound gives this. **Ready as a thin layer on H1.**

**H3. Residual (class-wide) kernel and pairwise `(min,+)` / `(+,×)` kernels** (theory E1, D3, D4)
- *Origin:* Thy, as reviewed at `5ed4072`. *Lean:* `verifyITop_sound`, `IProblem.consistent_iff_nonempty` (named in SCI-REV-0006 M1); `verify`/`verifyR`.
- *Status:* [V].
- *Review:* audit replicated by Sci at many theory heads (`INDEPENDENT_VALIDATION.md` §1, e.g. "AXIOM AUDIT OK: 3423 declarations"; mutation 266/267 caught). Originality (7) narrow.
- *Evidence:* conformance vectors.
- *Limitations:* *"kernel evaluation 'does not scale'"* (theory §12 item 7, quoted in SCI-REV-0006 §3).
- *Competing methods:* VeriPB/CakePB/PBLean; toulbar2.
- *Useless when:* instances have many non-sharp sites, so certificates blow up (B2 stratification).
- **Ready?** Usable as a trusted checker. The advantage is unmeasured, so **benchmark E-1 first**.

**H4. Global-minimiser certificate beyond enumeration** (F6: anchor of Ace-Val₂₀-NMe is the GMEC, `min m₋ ≤ min E ≤ E(x⁰)`, equal to 10⁻⁵ kcal/mol). Sci P3. [P + M], *"relative to paper proofs and unreviewed code"*. Superseded caution: SCI-REV-0012 §5 (non-product domains). **Not ready** until the domain issue is handled and a checker exists.

**H5. Identified sets and falsification certificates** (`INFERENCE_LIMITS.md` §§8–9, Theorem 8)
- *Origin:* Sci (`9d358cb`). *Lean:* `ws_L1/IdentifiedSets.lean` (`modelFree_certificate_sound`, `divergenceBall_certificate_sound`, `envelope_flow_sound_gibbs`, `kl_lower_bound_certificate_sound`, `falsification_sound_gibbs`, `theorem8c_falsification`).
- *Status:* soundness [V]; framework [K].
- *Review:* R3.
- *Evidence:* lattice chains ≤27 beads (model-free), ≤10 (envelope class).
- *Missing:* no structured flow family for envelope classes beyond one-body data (B3 open). Needs `ψ, Φ` pairwise in site variables.
- *Competing methods:* MaxOcc/maxOR, Christensen–Connault, OUQ.
- **Ready?** The model-free and KL-ball versions are ready for fixed-backbone rotamer ensembles with pairwise observables. The envelope version is research.

**H6. Theorem 7 (max-ent refinement stability, `TV ≤ tanh(βω/4)`).** Sci. Pinsker form [V] `MaxEntStability.lean`; sharp form [P]. R3. Applies to any reweighting tool. Useless when `βω ≫ 1` (bound → 1). **Ready as a reported diagnostic.**

**H7. Theorems 2–3 (deception instance; basin upper bound).** Sci. Theorem 3 Markov form [V]; Theorem 2 [P] only. Use: benchmark negative controls. **Ready as test generators.**

**H8. Robust macrostate ratio** (A11 Holley sandwich; theory §11.28 transport). Sci A11 [P], [V] on finite distributive lattices (L2). Thy `MacroRatio.lean` (compiled by Sci; Thms 11.105–11.106 replicated, SCI-RES-0005). Binary sites, submodular known part, monotone macrostates only. Useless for frustrated parts (fails in 49–81 % of instances). **Research stage for rotamers.**

**H9. Bennett/Hoeffding bracket and divergence cost table.** In print (Hoeffding 1963; Block–Shetty 2026). Sci [V] `BennettTwoPoint.lean`. Use: certified error bars for FEP given a *certified* floor and variance. Useless with sampled floor/variance. **Ready to cite, not to claim.**

**H10. Box limit `W* = 2β⟨env⟩` and floor-transition safety factor `λ_c`** (`ASSUMPTION_AUDIT.md` A10, Prop. AA.3; D12). Sci [P]. R24 corrections. Use: report how far a certificate is from what its information allows. **Ready as metadata.**

**H11. Geometry Theorem L** (global `n²` stability from separation-≤4 distances). Geo, `LOCAL_DATA_STABILITY.md` at `288b2de`. Proof **not reviewed by Sci**. Originality (3)/(5). Sci's threshold analysis [P two lines; N]: guarantee *"empty on these geometries"* (needs ≤10⁻⁴ Å errors; exceeds the helix `R_g` from 16 residues on). Useful exactly as "a theorem about the exponent". **Not ready** as a data-facing tool. The necessary-threshold formula `G = min 4|h⁻h⁺|` is itself a cheap observability diagnostic **(my inference)**.

---

## I. Workstream classification (abstract-level)

- **A-series (originality):** A1 query complexity; A2 kernels/geometry/chains; A3 sampling-based free-energy certification; A4 Theorem L.
- **L-series (Lean):** L1 core statements (78 theorems); L2 newest statements; L3 workstream F Lemmas 0–3, Theorem A, A16.5 given Harper, A1.1 items 1–2; L4 anchored remainder identity, sandwich, Bennett–Hoeffding.
- **R-series (reviews):**
  - theory sections: R1 (§11.25), R2 (§11.22), R4 (§11.24), R5 (§11.26), R6 (nested algorithm cost), R9 (second round, with addendum), R10 (workstream Y), R12, R13, R15, R16, R17;
  - engineering: R7, R18;
  - own work: R3 (INFERENCE_LIMITS v2), R8 (A16), R19 (A17 (19)–(20)), R24 (items 86–90); R14 stopped by a safeguard; R25, R26 briefs only;
  - other divisions: R20 (Complexity hardness), R21 (Ensemble), R22 (Geometry B/B′/G), R23 (theory assumption audit).
- **Code:** `experiments/science/pi_inference/` (332 files): A17 scripts (`certified_populations.py`, `first_order_recovery.py`, `window_model.py`, `ball_cache.py`, B10 scripts, `lean/SandwichCost.lean`, `CoreGreedy.lean`). `pi_chain/` holds the diamond-lattice enumerator (`dia_chain.py`, replicates engineering tables for n ≤ 10) and the identified-set LPs (`identified_sets.py`, `scattering_identified.py`, `envelope_*`). Neither directory has a README.
