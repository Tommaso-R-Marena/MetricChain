# STRUCTBIO prior-art assessment: certified side-chain GMEC, partition functions, marginals, ensemble identification

- **Date:** 2026-11-26.
- **Status:** internal assessment written by an AI analyst for the Structural & Computational Biology division (branch `research/structural-biology`). It has not been peer reviewed, and it does not authorise any public novelty claim.
- **Scope:** capabilities C1, C1b, C2 and C3 as defined in the division's brief: fixed backbone, fixed sequence, a discrete rotamer model, and exact rational pairwise tables.
- **Absence of evidence.** A bounded search that finds nothing does not show that something is new. Every "NOT FOUND" below means only "not found by the searches listed here".

## Method and evidence labels

**Web searches run (25).**
1. Proof logging for weighted CSP / cost function networks / certified optimality.
2. "VeriPB toulbar2 proof logging".
3. Certified weighted model counting with two-sided bounds and a certificate checker (2024–2025).
4. Cheng–Luo–Jiang IJCAI 2024.
5. Certified MAP inference / optimality checkers for graphical models (2025).
6. Guaranteed bounds on side-chain rotamer marginals.
7. Mooij–Kappen marginal bounds.
8. Yanover–Meltzer–Weiss side-chain MRF dataset.
9. OpenGM protein-folding benchmark.
10. toulbar2 Cost Function Library.
11. Koops et al. CP 2025.
12. MaxOcc.
13. LP bounds and identifiability of ensemble weights.
14. Arb ball arithmetic.
15. LP minimum/maximum conformer populations.
16. BME (Bottaro et al.).
17. FASPR.
18. SCWRL4.
19. Kamisetty–Xing–Langmead GBP.
20. Viricel et al. 2018.
21. Rigorous or interval bounds on graphical-model partition functions (2025–2026).
22. Proof logging for weighted model counting (2025–2026).
23. PIC2011 instances.
24. PyRosetta licence.
25. Lang–Sontag–Vijayaraghavan stability.

**Other checks.**
- GitHub code search of `toulbar2/toulbar2`: "veripb" returned 0 hits. "certificate" returned 9 files, all of which belong to the `-x` "solution as certificate" option.
- The toulbar2 user documentation, read in full up to character 100,000.
- The Cost Function Library tree, read through the GitLab API.
- Full text of Viricel et al. CP 2016, Bryant et al. JAIR 2025, FASPR (PMC) and SCWRL4 (PMC).
- Abstracts of McCreesh et al. CP 2026, PBLean, Vandesande et al. AAAI 2026, count-catcher and the Structured Prediction Problem Archive.

**Evidence labels.**
- `[V]`: verified online in this session, from full text or primary documentation.
- `[V-abs]`: verified from an abstract or a search snippet only.
- `[repo]`: verified by another MetricChain division, as tagged in `docs/prior_art/L1_pruning_certificates.md` or `L2_relaxations_partition.md` (commit `525b23e`). I did not re-check these.
- `[mem]`: from memory, unverified.

---

## A. Exact GMEC solvers for side-chain positioning and their guarantees

| Method | Exact or heuristic | What "provable" means there | Independently checkable certificate? |
|---|---|---|---|
| DEE: Desmet et al., Nature 356:539 (1992); Goldstein, Biophys. J. 66:1335 (1994) `[repo]`/`[mem]` | Exact pruning rules (they never remove a GMEC rotamer); not a complete solver by itself | Soundness of the inequality, evaluated in floating point in all implementations I know of `[mem]` | No. Implementations log nothing. |
| DEE/A*: Leach & Lemon, Proteins 33:227 (1998) `[repo]`; OSPREY 3 (Hallen et al., J. Comput. Chem. 39:2494, 2018, doi:10.1002/jcc.25522) `[repo]` | Exact with respect to the input model (with continuous flexibility: with respect to bounds on minimised energies) | GMEC "with respect to the input model" (PMC4526210, `[V-abs]`); floating-point energies; continuous variants rely on a local minimiser `[mem]` | No certificate output found |
| Cost function networks / toulbar2: Allouche et al., Artif. Intell. 212:59 (2014), doi:10.1016/j.artint.2014.03.005 `[repo]`; Traoré et al., Bioinformatics 29:2129 (2013), doi:10.1093/bioinformatics/btt374 `[repo]`; Simoncini et al. JCTC 2015 `[repo]` | Exact (depth-first branch-and-bound / HBFS with soft arc consistency incl. VAC; BTD) | Optimal for **integer** costs. Real energies are scaled and rounded to a fixed decimal precision first `[mem]`, so the exact optimum is that of the rounded model. | **No.** The toulbar2 1.0.0 documentation has no proof-logging, VeriPB or proof-output option `[V]`. A code search for "veripb" returned 0 hits `[V]`. "Certificate" in toulbar2 means only a given solution (`-x`) `[V]`. |
| ILP/LP: Kingsford, Chazelle, Singh, Bioinformatics 21:1028 (2005) `[mem]` | Exact (ILP; the LP is often integral) | Floating-point commercial MIP solver `[mem]` | No. In principle VIPR could supply one (section B). |
| Tree decomposition: Xu & Berger, J. ACM 53:533 (2006) `[mem]` | Exact DP for bounded treewidth; their PTAS is approximate `[mem]` | Floating point | No |
| SCWRL4: Krivov, Shapovalov, Dunbrack, Proteins 77:778 (2009), doi:10.1002/prot.22488 | **Heuristic overall.** Edges are dropped below ε = 0.02 kcal/mol, edges are decomposed, high self-energy rotamers are deactivated, and the threshold is doubled until the problem is tractable. The authors state the result is "not guaranteed to find the global minimum" `[V]` (PMC2885146). | n/a | No |
| FASPR: Huang, Pearce, Zhang, Bioinformatics 36:3758 (2020), doi:10.1093/bioinformatics/btaa234 | **Deterministic but not exact.** A 15 kcal/mol self-energy cut, then Goldstein DEE and split DEE. Edges are decomposed when treewidth > 5, with the threshold starting at 0.5 kcal/mol and doubling. Then DP. `[V]` (PMC7320614) | No guarantee claimed `[V]` | No |
| LP relaxations / MPLP: Yanover, Meltzer, Weiss, JMLR 7:1887 (2006) `[mem]`; Sontag et al., UAI 2008 (cluster tightening) `[mem]`; Sontag UAI 2012 (dual certificates, `[V-abs]`) | Exact **when** the relaxation is tight. A dual solution with zero gap is an optimality certificate in principle. | Floating-point LP/message passing | No certificate format is emitted. The dual is a certificate only if it is checked in exact arithmetic. |
| Rosetta packer (simulated annealing) `[mem]` | Heuristic | n/a | No |

Partial-optimality / persistency methods (Haller, Swoboda, Savchynskyy AAAI 2018 `[repo]`; "Maximum persistency via iterative relaxed inference", arXiv:1508.07902 `[V-abs]`, authors Shekhovtsov, Swoboda, Savchynskyy `[mem]`) certify parts of the optimum through LP arguments. They are also floating point and emit no checkable proof.

> **Verdict A: KNOWN.** Exact GMEC computation for the discrete pairwise rotamer model is classical: DEE (1992/1994), DEE/A* (1998), ILP (2005), tree decomposition (2006) and CFN/toulbar2 (2012–2015). toulbar2 is the strongest exact solver in the published comparisons `[repo]`. No protein GMEC solver found here emits an independently checkable certificate. The SCWRL4 and FASPR packers are not exact, by their authors' statements.
>
> **What STRUCTBIO may claim:** that it emits a checkable certificate for the GMEC of a stated rational pairwise model, which no protein-specific solver found in this search does.
>
> **What it may not claim:** a new GMEC algorithm, new pruning rules (DEE and LP-dual bounds are textbook), or exactness "with respect to nature". "More accurate than SCWRL4/FASPR" is a different energy model and therefore not comparable.

**C1b (margins).** The per-residue energy gap is the difference between the GMEC and the best conformation that changes residue *i*. Any exact solver computes it with one extra constrained run per residue, so it is routine `[mem]`. Robustness of a MAP solution to bounded perturbations of the energy function is studied as perturbation stability:
- Lang, Sontag, Vijayaraghavan, AISTATS 2018 (PMLR 84), arXiv:1711.02195 `[V-abs]`.
- "Block stability for MAP inference", arXiv:1810.05305 `[V-abs]`.
- Bilu–Linial stability more generally `[mem]`.

Sensitivity and tolerance analysis of combinatorial optima is classical `[mem]`.

> **Verdict C1b: PARTIALLY KNOWN.** The quantities and the means of computing them are known. Certified, checkable margins on protein rotamer models were not found.
>
> **May claim:** certified margins for the stated model. **May not claim:** a new stability concept.

## B. Proof logging and certified optimality in neighbouring solver technology

**Pseudo-Boolean proof logging (VeriPB) and verified checking (CakePB).**
- VeriPB supports decision, enumeration and optimisation proofs `[V-abs]` (VeriPB documentation, https://www.cril.univ-artois.fr/PB26/descr/Documentation_VeriPB_general.pdf).
- Gocht & Nordström AAAI 2021, parity reasoning `[V-abs]`.
- Bogaerts, Gocht, McCreesh, Nordström, JAIR 77 (2023), doi:10.1613/jair.1.14296, certified dominance and symmetry breaking `[repo]`.
- Gocht et al. AAAI 2024, doi:10.1609/aaai.v38i8.28642, CakePB verified in HOL4/CakeML `[repo]`.

**Certified MaxSAT.**
- Berg, Bogaerts, Nordström, Oertel, Vandesande, "Certified core-guided MaxSAT solving", CADE 2023 (https://www.bartbogaerts.eu/articles/2023/006-CADE-RC2/CertifiedCoreGuidedMaxSAT.pdf). For 95% of instances the run was at most about 36% slower `[V-abs]`.
- Certified MaxSAT preprocessing, arXiv:2404.17316 `[V-abs]`.
- **Vandesande, Coll, Bogaerts, "Certified branch-and-bound MaxSAT solving", AAAI 2026**, doi:10.1609/aaai.v40i17.38449, arXiv:2511.10273 `[V-abs]`. This one certifies the *bounding* (look-ahead) of a branch-and-bound optimiser, which is the structural analogue of C1's LP-bound leaves.

**Certified pseudo-Boolean optimisation with LP bounds.** W. Koops et al., "Practically feasible proof logging for pseudo-Boolean optimization", CP 2025, doi:10.4230/LIPIcs.CP.2025.21 `[V-abs]`:
- It logs LP integration with Farkas certificates.
- Verified conclusions come "within a factor of about 20 of solving time".
- Search snippets disagree on the author list, so verify it before citing.

**Lean 4 import of VeriPB proofs.** S. Szeider, "PBLean", arXiv:2602.08692 (Feb./Apr. 2026) `[V-abs]`. It covers all VeriPB kernel rules and runs a checker proved sound in Lean "as compiled native code". The theory division reports that it relies on `native_decide` `[repo]`.

**MIP certificates.**
- VIPR: Cheung, Gleixner, Steffy, IPCO 2017, doi:10.1007/978-3-319-59250-3_13 `[repo]`.
- Exact SCIP with VIPR output (SCIP Optimization Suite 10 report, arXiv:2511.18580) `[repo]`.
- A verified VIPR checking route: Wood et al., J. Symb. Comput. 135:102543 (2026) `[repo]`.

**Cost function networks specifically.** I found no proof logging, certificate output or VeriPB integration for weighted CSP / CFN / toulbar2 (searches 1, 2, 5 and 22; GitHub code search; toulbar2 documentation) `[V]`. The theory division reached the same result with eleven searches `[repo]`.

The gap is narrow in practice. Two routes exist today and are concrete baselines for C1:
- **PB route:** a CFN with integer costs can be encoded as pseudo-Boolean optimisation (direct/support encoding), solved by RoundingSat with VeriPB logging, and checked by CakePB.
- **MIP route:** it can be encoded as an ILP and solved by exact SCIP with VIPR output.

Neither route has been shown on protein rotamer instances in what I found.

> **Verdict B: KNOWN technology, NOT FOUND for CFNs.** Certified optimality with independently checkable proofs, including LP-bound reasoning, Farkas certificates, branch-and-bound bounding and formally verified checkers, is established in 2023–2026 for PB, MaxSAT and MIP. I found no proof logging for CFN/WCSP solvers or for protein GMEC (as of 2026-11-26).
>
> **May claim:** a native certificate format for DEE plus LP-dual branch-and-bound on CFNs, checked in exact integer arithmetic, with rule semantics machine-checked in Lean 4, *if* it is shown to work on real instances.
>
> **May not claim:** "first certified optimisation for this problem class" without first measuring against the PB/VeriPB/CakePB and exact-SCIP/VIPR routes on the same instances. Those routes would also give checkable optimality proofs. The difference then lies in certificate size, check time and trust base, not in whether certification is possible at all.

## C. Guaranteed partition-function approximation on rotamer models; certified counting

**K\* family (Donald lab, OSPREY).**
- K\*: Lilien et al., J. Comput. Biol. 12:740 (2005), doi:10.1089/cmb.2005.12.740. "An efficient deterministic approximation algorithm, capable of approximating our scoring function to arbitrary precision" `[repo]`.
- minDEE with provable ε-preserving pruning: Georgiev, Lilien, Donald, J. Comput. Chem. 29:1527 (2008) `[mem]`.
- BBK\*: Ojewole et al., J. Comput. Biol. 25:726 (2018), doi:10.1089/cmb.2017.0267 `[repo]`.
- MARK\*: Jou et al., J. Comput. Biol. 27:550 (2020), PMC7185359. Bounds a discrete sum over *minimised* conformation energies `[repo]`.
- EWAK\*: Lowegard et al., PLoS Comput. Biol. 16:e1007447 (2020) `[repo]`.

Their guarantee is a deterministic ε-approximation (a two-sided bracket of Z) for each sequence, in floating point. Energies come from minimisation, so the bracket holds relative to the minimiser's output `[mem]`. There is no certificate output and no per-residue rotamer-population bounds (searches 6 and 21). These methods are aimed at **design** (sequence ranking).

**toulbar2 Z\*ε.** Viricel, Simoncini, Barbe, Schiex, "Guaranteed weighted counting for affinity computation: beyond determinism and structure", CP 2016, LNCS 9892:733, doi:10.1007/978-3-319-44953-1_46 (author PDF https://miat.inrae.fr/schiex/Doc/Export/CP2016.pdf) `[V]`:
- Guarantee: Ẑ with Z/(1+ε) ≤ Ẑ ≤ Z "with probability 1" (their Eq. 1, Theorem 1).
- Experiments ran "in double floating point mode" (§4). The paper does not treat rounding error.
- No certificate.
- Instances: Amber ff14SB binding-site sub-problems and UAI/PIC2011 PR instances.
- The paper mentions "the computation of marginal probabilities" only as a related task, not as a bounded output.

Application: Viricel, de Givry, Schiex, Barbe, Bioinformatics 34:2581 (2018), doi:10.1093/bioinformatics/bty092, EasyE/JayZ with Rosetta energies `[V-abs]`. The toulbar2 documentation exposes `-logz` for `.uai` input without stating an error bound `[V]`.

**Anytime bounds from graphical-model inference.**
- Weighted mini-bucket: Liu & Ihler ICML 2011 `[mem]`.
- AND/OR search bounds on Z: Lou, Dechter, Ihler AAAI 2017, doi:10.1609/aaai.v31i1.10667 `[repo]`.
- Dynamic importance sampling with bounds: NIPS 2017 `[repo]`.
- Tree-reweighted upper bounds: Wainwright, Jaakkola, Willsky, IEEE Trans. Inf. Theory 51:2313 (2005) `[repo]`.
- Anytime weighted model counting with approximation guarantees: Dubray, Schaus, Nijssen, CP 2023 `[repo]`.
- AND/OR branch-and-bound for K\* design: Pezeshki et al., UAI 2022 `[repo]`.

All of these give deterministic upper and/or lower bounds in floating point and emit no certificate.

**Exact junction-tree inference** (libDAI JTree, toulbar2 BTD counting) gives exact Z and marginals up to floating-point error `[mem]`.

**Certified and verified counting.**
- **CPOG:** Bryant, Nawrocki, Avigad, Heule, SAT 2023, doi:10.4230/LIPIcs.SAT.2023.6; JAIR 82:2057 (2025) `[V]`. It is "the first formally verified toolchain for weighted and unweighted model counting". The checker and "ring evaluator" are proved in Lean 4. Weighted counting is defined "over rational numbers", with **per-literal (product-form) weights**, and the count is exact (`ringEval_eq_weightSum` over a commutative ring).
- **Two-sided certificates with pruning:** Cheng, Luo, Jiang, "Knowledge compilation for incremental and checkable stochastic Boolean satisfiability", IJCAI 2024, doi:10.24963/ijcai.2024.206 `[V-abs]`. It extends CPOG by splitting the equivalence check into two implication checks, "one certifying the lower bound and one the upper bound" of a satisfying probability, under partial exploration. **This is the closest found precedent for certified two-sided bounds on a weighted sum.** It is Boolean, with rational probabilities.
- MICE: Fichte, Hecher, Roland, SAT 2022 `[repo]`, unweighted.
- Formally certified approximate counting: Tan et al., CAV 2024, arXiv:2406.11414 `[V-abs]`. It gives a PAC guarantee, not deterministic bounds.
- VeriPB projected enumeration and counting: McCreesh, Nordström, Oertel, Tan, CP 2026, doi:10.4230/LIPIcs.CP.2026.43 `[V-abs]`, unweighted.
- count-catcher, arXiv:2610.36196 (Oct. 2026) `[V-abs]`: Lean theorems for exact unweighted counts, with the Lean compiler in the trust base.
- Certified knowledge compilation: Capelli, Lagniez, Marquis and related work `[repo]`/`[mem]`, not re-checked.

> **Verdict C: PARTIALLY KNOWN.**
> - (i) Deterministic two-sided brackets of Z on rotamer models are **known**: K\*/MARK\* and Z\*ε. They are computed in floating point, with no certificates and no marginal bounds.
> - (ii) Machine-checked **exact** weighted counting with rational product weights is **known**: CPOG, Lean 4.
> - (iii) Checkable **two-sided** bounds on a weighted Boolean probability are **known**: Cheng et al. 2024.
> - **NOT FOUND:** a certificate-producing, outward-rounded enclosure of Z for a pairwise model whose weights are exp(−E/RT) (irrational for rational E ≠ 0), which also covers marginals and states when it abstains.
>
> **May claim:** validated, two-sided enclosures of log Z and rotamer marginals for a stated pairwise model, with rounding error accounted for, as not found in this search.
>
> **May not claim:**
> - "the first guaranteed partition function for protein models" (Z\*ε, K\* and MARK\* predate it);
> - "the first certified weighted counting" (CPOG, Cheng et al.);
> - any advantage in tightness or speed over Z\*ε, MARK\* or AND/OR bounds before a same-instance, same-width comparison.
>
> The Gibbs–Bogoliubov inequality and Hoeffding-type bounds are textbook `[mem]`. Thermal pruning with a bounded loss of mass is close to K\*'s ε-preserving pruning `[mem]`. Neither component is new by itself.

## D. Side-chain entropy and rotamer populations by approximate inference; experimental comparators

**Computational.**
- Mean-field / self-consistent mean field: Koehl & Delarue, J. Mol. Biol. 239:249 (1994) `[mem]`.
- Belief propagation and approximate inference for side chains: Yanover & Weiss, NIPS 2002 (BP, GBP and mean field compared against SCWRL) `[V-abs]`.
- Generalized BP free energies: Kamisetty, Xing, Langmead, RECOMB 2007, LNCS 4453 (journal version Proteins 2008) `[V-abs]`. GOBLIN (Kamisetty et al., Proteins 2011) `[mem]`.
- Systematic tests of BP free energies: Donovan-Maiye, Langmead, Zuckerman (PMC5933972) `[V-abs]`.
- Monte Carlo and MD estimates of side-chain entropy are standard `[mem]`.

None of these gives guaranteed bounds. BP and GBP are variational approximations. The Bethe free energy is a provable lower bound only for special classes (Ruozzi NIPS 2012, log-supermodular models `[repo]`).

**Generic guaranteed marginal bounds.**
- Mooij & Kappen, NIPS 2008, "Bounds on marginal probability distributions", and arXiv:0801.3797 (box propagation over subtrees and self-avoiding-walk trees) `[V-abs]`.
- Bound propagation: Leisink & Kappen 2003 `[mem]`.
- Ihler, UAI 2007, BP accuracy bounds `[mem]`.

These were demonstrated on medical-diagnosis and synthetic models, in floating point, with no certificates. Applications to protein rotamer models were not found.

**Experimental comparators** (for interpretation only, not for validating a force-field certificate):
- ³J-coupling-derived χ1 rotamer populations from NMR `[mem]`.
- Methyl side-chain order parameters (S²axis) `[mem]`.
- Alternate conformations in high-resolution crystal structures: Ringer (Lang et al., Protein Sci. 2010 `[mem]`) and qFit (Riley et al., Protein Sci. 2021 `[mem]`). The qfit-3.0 repository carries a permissive Stanford/MIT-style licence `[V]`.

> **Verdict D: NOT FOUND** for guaranteed two-sided bounds on side-chain rotamer marginals of a real protein (searches 6, 7, 19, 21; also the K\*/MARK\* literature, which bounds Z per sequence and not populations). Generic marginal-bound methods exist (Mooij–Kappen) and must be cited and used as a baseline.
>
> **May claim:** certified population enclosures *for the stated energy model* on public structures.
>
> **May not claim:** that those populations are experimentally correct. Agreement with NMR or qFit is a separate scientific test of the force field and the rotamer library, not of the certificate.

## E. Validated numerics for sums of exponentials

- **Arb**, now merged into FLINT: F. Johansson, "Arb: efficient arbitrary-precision midpoint-radius interval arithmetic", arXiv:1611.02831; IEEE Trans. Comput. 66(8):1281 (2017) `[V-abs]` for arXiv, `[mem]` for the journal details. It provides rigorous ball enclosures of exp and log. FLINT documents its ball routines as "formerly the standalone Arb library" `[V-abs]`. Python bindings: python-flint 0.9.0 on PyPI `[V]`.
- **MPFI**: Revol & Rouillier, Reliable Computing 11 (2005) `[mem]`.
- **INTLAB**: Rump 1999, MATLAB, commercial licence `[mem]`.
- Formally verified interval arithmetic in Isabelle: Brucker et al. 2024 `[V-abs]`.
- FloatLib (arXiv:2609.19352) `[repo]`.

Outward-rounded log-sum-exp is a routine application of these libraries.

> **Verdict E: KNOWN.** Validated enclosures of finite sums of exponentials are standard.
>
> **May claim:** correct use of these libraries.
>
> **May not claim:** novel validated numerics. The trust base must list the library (for example FLINT/Arb), its version, and whether its output is re-checked in exact rational arithmetic.

## F. Ensemble weights from linear ensemble-averaged data (C3)

- **MaxOcc** (Bertini, Luchinat, Parigi and co-workers, c. 2010–2012, WeNMR portal https://py-enmr.cerm.unifi.it/access/index/maxocc) `[V-abs]`. It gives the maximum weight a conformer can have in any ensemble that fits averaged data. The fit is required to stay within a χ²-type threshold, and the computation is done numerically. Search snippets give conflicting journal citations for the 2012 portal paper, so these must be checked before citing.
- **Maximum entropy and Bayesian ensemble refinement:**
  - Hummer & Köfinger, J. Chem. Phys. 143:243150 (2015) `[mem]`.
  - Bottaro, Bengtsen, Lindorff-Larsen, "Integrating molecular simulation and experimental data: a Bayesian/maximum entropy reweighting approach", Methods Mol. Biol. (2020), doi:10.1007/978-1-0716-0270-6_15; bioRxiv 10.1101/457952; code at https://github.com/KULL-Centre/BME `[V-abs]`.
  - These return a single regularised weight vector and do not give identification ranges.
- **Sample-and-select:** EOM, ASTEROIDS, ENSEMBLE `[mem]`; MINOES (minimal ensembles) `[V-abs]`.
- Sparsest-ensemble recovery by convex methods, arXiv:2008.03641 `[V-abs]`.
- LP sampling of consistent SAXS P(r) curves `[V-abs]`.
- Non-uniqueness is widely acknowledged. For example: "there are no exact methods to discriminate between ensembles of equally good fit" `[V-abs]`.
- In econometrics, partial identification by linear programming (Manski and successors) is the general framework `[mem]`.

> **Verdict F: PARTIALLY KNOWN.** Upper bounds on conformer weights (MaxOcc) and the non-identifiability of ensemble weights are known. Computing ranges of a linear functional over {w ≥ 0, Σw = 1, |Aw − b| ≤ δ} is a textbook LP. I found **no** work that issues exact-arithmetic LP-duality certificates of identification, non-identification or the range of a target property for conformer libraries (searches 12, 13, 15, 16).
>
> **May claim:** exact certificates of identified / not identified / range under stated data, error model and library.
>
> **May not claim:** a new concept of maximum occurrence or of non-identifiability. Results are conditional on the finite library and the forward model.

---

## Summary table

| STRUCTBIO claim | Closest prior art | What remains possibly new | Evidence level of that statement |
|---|---|---|---|
| C1: exact GMEC of rotamer model | DEE/A* (1998), Kingsford ILP (2005), toulbar2 CFN (2013–15) | Nothing (algorithmically known) | Searched; `[repo]`+`[V]` |
| C1: independently checkable optimality certificate, exact integer check, Lean-checked rule semantics | VeriPB+CakePB with LP/Farkas (Koops et al. CP 2025); certified B&B MaxSAT (AAAI 2026); exact SCIP+VIPR; PBLean | A native CFN/DEE+LP-dual certificate. Its advantage over PB/VIPR encodings is **unmeasured**. | Searched (searches 1, 2, 5, 22, code search); NOT FOUND for CFN |
| C1b: certified per-residue gaps / robustness radius | Constrained re-solves (routine); perturbation stability (Lang et al. 2018, 2019) | Certified margins on protein models | Partly searched (search 25); routine nature `[mem]` |
| C2: two-sided bound on Z for rotamer model | Z\*ε (CP 2016, double precision); K\*/BBK\*/MARK\*; WMB; AND/OR bounds; TRW | Outward rounding plus certificate plus explicit abstention | Searched; `[V]` for Z\*ε |
| C2: certified enclosures of rotamer marginals | Mooij–Kappen 2008 (generic, floating point); exact JTree | Certified marginal enclosures on real protein models | Searched (6, 7, 21); NOT FOUND |
| C2: machine-checked weighted counting | CPOG (Lean 4, exact rational product weights); Cheng et al. IJCAI 2024 (two-sided) | Irrational Boltzmann weights handled by validated enclosures; pairwise (non-product) weights | Searched; `[V]` |
| C2 components: GB/Hoeffding sandwich, thermal DEE with certified loss, weak-pair relaxation | Bogoliubov inequality; K\* ε-pruning; Jain et al. PLoS Comput. Biol. 2017 sparse-graph energy bounding `[repo]` | Only the certified combination | Partly searched; components `[mem]`/`[repo]` |
| C3: exact LP-duality identification certificates for ensemble weights | MaxOcc; BME/MaxEnt; Manski-style partial identification | Exact-arithmetic certificates for conformer libraries | Searched (12, 13, 15, 16); NOT FOUND |
| Implementation: outward-rounded sums of exponentials | Arb/FLINT, MPFI, INTLAB | None | Searched (14) |

**Most binding constraint on any novelty statement.** Before writing "first" about C1, the division must run the PB (VeriPB/CakePB) and MIP (exact SCIP/VIPR) certification routes on the same instances. Before writing anything comparative about C2, it must run Z\*ε and an exact junction tree on the same instances at matched bracket width. Until then the correct wording is "not found in a bounded search (2026-11-26)".
