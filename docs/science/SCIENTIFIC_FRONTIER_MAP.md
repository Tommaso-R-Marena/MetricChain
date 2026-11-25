# Scientific frontier map

*Science division.  **Version 4** (2026-11-25, checkpoint 20: after all eleven first-wave
workstreams, the referee of our own note and addenda A8–A11; rows F2, F4, F5, F7, F8, F9, F12
and §§3–4 rewritten; change notes at the end).  A map of what the science of molecular
conformations cannot reliably establish today, why, and what precise problem each
limitation turns into.  It starts from the science, not from what MetricChain can prove.
Labels as in `docs/collaboration/SCIENCE_TO_ALL.md`; **[H]** marks our reading of a field's
practice; **[M]** a measurement on a named model.*

Theory commit referred to: `89ac710` (tree built on `5ed4072`).  Engineering: `a2f6dc7`.

---

## 1. The four bottlenecks

Every limitation below is one of four kinds, and it matters which, because they call for
different remedies:

| kind | the conclusion is limited by | remedy | not a remedy |
|---|---|---|---|
| **information** | what the available knowledge (model class, computed energies, measurements) determines | a different *kind* of information; or an honest set-valued answer | more computation |
| **computation** | the cost of extracting what the information determines | algorithms, structure (low treewidth, funnels), certificates that separate search from checking | more data |
| **representation** | the variables in which the problem is posed (a guarantee that is cheap in one representation and exponential in another) | change of variables / features / class | more of either |
| **meaning** | the target is not a physical observable, or a guarantee is relative to inputs nobody can supply | a different target; a different class | a sharper theorem about the same target |

The theory division's central negative result (`DEAD_ENDS.md` D28) is, in these terms, an
*information* bottleneck proved with full rigour: in a first-order class, point evaluations
do not determine `min E` or `ln Z` at sub-exponential cost.  Its lever-arm result (D42) is a
*representation* bottleneck.  Its own table "what each kind of knowledge about the residual
costs" (theory report §10) is the information axis for one kind of information.  This map
adds the other kinds, and the question of meaning.

## 2. The map

| # | what cannot be established today | kind | current practice **[H]** | the precise problem it becomes | where the programme stands |
|---|---|---|---|---|---|
| F1 | **That a computed ensemble or free energy is converged** — that no unvisited region matters | computation, with no certificate | sampling with statistical error bars that assume the relevant states were visited | two-sided certified bounds on ratios of restricted partition functions of a stated model, at realistic size; structural conditions (treewidth, funnels) under which the certificate is polynomial | verified `(+,×)` kernel with cut and elimination rules (**[V]**); no instance at realistic size (engineering E-2) |
| F2 | **Whether a disagreement between simulation and experiment is model error or sampling error** | information + meaning | goodness-of-fit and reweighting statistics computed from the same finite sample | a lower bound on the divergence of the model from *every* ensemble consistent with the data, certified independently of sampling | `INFERENCE_LIMITS.md` Theorem 8: data certify a lower bound on `KL(truth‖model)` (certificate: two partition-function bounds, kernel-checkable for pairwise models; soundness **[V]**, workstream L1) and on the envelope constant (flow certificate; no structured family known).  The quantity is the *extent of falsification* of the partial-identification literature (**known**); a sample-based estimate of it is biased upward (**[P]**); certified lower bounds for molecular models were **not found** (M).  Numbers: lattice chains to 10 beads only.  No physical instance |
| F3 | **What ensemble-averaged data determine about a flexible molecule's ensemble** | information | one refined ensemble (maximum entropy, Bayesian, minimal-ensemble); for *single conformations and regions* the Florence NMR group's maximum occurrence (MaxOcc, 2010) and maxOR/minOR (2014) compute the largest and smallest weight compatible with averaged data, by penalised least squares on a finite pool with a heuristic misfit threshold | the *identified set*: the exact range of an unmeasured ensemble quantity over all ensembles consistent with data and prior class; **guaranteed** (dual-certified) numbers; its asymptotics for chains | **known (workstream M):** the prior-free range is the generalised moment problem (Isii, Kemperman; de Finetti; optimal uncertainty quantification), with MaxOcc as its instance for indicators (theorem: Gardner–Longinetti–Sgheri 2005; exact conic dual: di Dio–Schmüdgen 2018); with a divergence ball the dual is Christensen–Connault (Econometrica 2023).  **Not found:** guaranteed numbers for molecular ensembles; a physical prior neighbourhood; a density-ratio ("envelope") class with moment constraints.  **Ours:** exact identified sets on the lattice chain to 27 beads; the envelope class with data and its flow dual; the theory division's limit shape (§11.22) as the asymptotic model-free identified set |
| F4 | **Conformational entropy from experiment** | information | entropy from per-site order parameters by an empirical linear calibration ("entropy meter"), or from low-order expansions | how well do `k`-body marginals determine the entropy, under which assumption on the energy? | **known (M):** in the unrestricted class the range of entropies given means and pairwise correlations is nearly the whole interval (Albanna et al. 2017); `k`-wise independent laws of small entropy on codes.  **Ours, refereed (R3):** inside a Gibbs class with bounded energy differences, *uniform* `k`-body marginals are compatible with entropies down to the class minimum plus `⌊k/2⌋ ln n + O(1)` (Theorem 2; sharp within mixtures of polarised basins); with error bars `τ` this holds for correlations of **every** order once the code's dual distance exceeds `ln(1/τ)/ln coth(b/2)` (Theorem 2-τ, exact).  A statement about one data vector and large `n`; other data can identify the entropy.  The constraint that helps is the interaction *order* of the energy, not the size of its increments |
| F5 | **Whether the observed state is the only one** (hidden or "excited" states) | information | low-population states are found when a technique happens to be sensitive to them; MaxOcc bounds a state's weight from above | detectability thresholds of a hidden basin, by kind of data | uniform `k`-body marginals bound every basin population **from above** by `≈ n^{−⌊k/2⌋}` (Theorem 3; the maximal mass function of moment theory, **known**) and not from below — they exclude dominance, they identify no population (corrected after our referee).  A mean-energy datum excludes *deeper* hidden states and cannot exclude a hidden twin of the same depth (Proposition 5b; the root now proved by the referee); at bounded accuracy the worst-case cost of certifying `ln Z` is unchanged by local data of bounded order (exact), by correlations of every order with error bars (Theorem 4-τ), and by the mean energy — but a *sampler* defeats the hard family, and pinned ensembles determine `ln Z`.  All on the cube with zero known part; **nothing is proved with a field or for a chain** |
| F6 | **That a predicted structure is globally optimal for the stated energy** | computation, then meaning | heuristic search; learned predictors with learned confidence scores; provable discrete algorithms for pairwise rotamer models whose "provable" is a paper proof relative to the model, floating point not discussed (workstream A2) | (a) a machine-checkable certificate of optimality; (b) with model uncertainty of the order of the gaps, the meaningful object is the set of *possibly optimal* conformations, and its size | (a) verified `(min,+)` kernels (**[V]**).  **A2:** no proof logging for cost-function-network / MAP solvers exists (toulbar2 1.0.0 has none), so the gap stands; but verified pseudo-Boolean optimisation with Farkas bounds checks within a factor 20 of solving time (Koops et al. 2025) and pseudo-Boolean proofs can be imported into Lean 4 (PBLean 2026, with a compiler-trust axiom), so whether a native format has any advantage is unmeasured.  **The capability with no counterpart found is the residual kernel: one certificate valid for every member of an uncertainty class.**  (b) contact-set theorem (**[V]**, known in substance); how many sites of a real system are sharp: pending (P) |
| F7 | **Rates and barriers with any guarantee that a faster pathway does not exist** | computation, with no certificate | pathway sampling; transition-state searches from guessed endpoints — all produce paths, i.e. *upper* bounds on barriers and *lower* bounds on rates | barrier lower bounds as cut certificates; rate upper bounds as the same cuts with partition functions | **workstream K (SCI-MSG-0005):** no new kernel is needed — wall minima and wall/basin partition functions are what the verified kernels output; 32 Lean theorems for box cuts; exact robust interval of a barrier height over an envelope class; a trap bound for every stationary local dynamics.  **Limits:** the barrier threshold of a nearest-neighbour chain is PSPACE-complete (no transfer matrix for barriers); multiplier relaxations of counting cuts are vacuous; rates are sampler-relative; envelope uncertainty enters as `exp(β·d(basin, wall))`.  The one experiment-facing statement — a certified relaxed torsion scan against dynamic NMR — has not been carried out on any molecule |
| F8 | **Which uncertainty class a physical residual lives in** — the input of every guarantee | meaning | not asked; model error is assessed by benchmark statistics (root mean square) | measured bounded-difference constants along a chain, second differences, remainder of the best pair-additive fit, for real force-field terms | **measured once (workstream P, SCI-RES-0002) [M]**, alanine peptides, ff14SB known part, exact on grids: same-lineage force-field differences are *exactly* additive or residue-local (certifiable for every length); charge-model changes `βc ≈ 2–10`; the GBn2 solvent term in backbone torsions `βc = 12–53`, growing with length, dense second order, no sharp site — near the pair-additive class in RMS (`0.2–0.9 k_BT`), not in sup norm (`2–16 k_BT`); Jensen gap 2–3 nats against a class bound of 71–178.  **No certified upper bound exists for any many-body term.**  The decisive case — rotamer variables on a fixed backbone — is being measured (workstream P2) |
| F9 | **Whether a worst-case class is the right model of ignorance at all** | meaning | — | which geometry of the class makes certification tractable, with honest guarantees | **workstream X (SCI-MSG-0007; `ALTERNATIVE_FRAMEWORKS.md`):** the exponential price is the *geometry* of the first-order class (evaluations combine by a minimum), not the worst-case quantifier; in a kernel ball they combine linearly and bounded interaction order costs `≈ n^m`, with a matching lower bound; the envelope still wins where the known part is sharp; no procedure correct on a first-order class can be cheap on a subclass (**no free hedging**), so the replacing assumption cannot be verified from polynomially many evaluations — nor from averaged data (our Theorems 4, 4-τ); a Bayesian certificate fails silently on a dip.  Recommendation: combine (sharp part: envelope; rest: linear-information class over body-ordered type-shared features; outside: a stated sup-norm floor) |
| F10 | **Checkable justification for learned structure predictors** | meaning + computation | confidence scores calibrated on a benchmark population | proof-carrying prediction: an untrusted predictor proposes, a small kernel checks a stated property against a stated model and class | the separation of search from checking is the programme's design (**[V]** kernels); no interface to a learned proposer; the checked property is only as meaningful as F8 allows |
| F11 | **Guarantees for continuous, articulated geometry** | representation | discretise (rotamers, voxels) and ignore the remainder, or bound it heuristically | representations in which the known part is low-treewidth *and* the residual has bounded per-variable constants; for chains: local frames, pair distances, multi-scale coordinates | voxel enclosures for pairwise torsion energies (**[V]**); the lever arm destroys per-torsion constants (D42) — a known phenomenon (reduced moments of inertia; a standard lemma in robot motion planning; A2), sharp constant `2√2/3`; profile classes repair it for a narrow class (§11.17), and the profile distance is the Wasserstein distance between distance distributions, whose zero set is homometry: **a profile does not identify a conformation** (homometric lattice chains from 6 beads on; A2, exhaustive); a positive tractability theorem for a physically plausible class: pending (X) |
| F12 | **Free-energy differences between structural states** (the observable free energies) | information + computation | alchemical and path methods with statistical error bars | the exact robust interval of a *ratio* of restricted partition functions over a class, with tractable dual certificates | the programme's target is the *total* `ln Z`, whose difference to the model's is not an observable.  **Solved in one setting (addendum A11, SCI-MSG-0009):** binary sites, a known part without frustration, macrostates monotone in the site variables — the Gibbs measure over the whole envelope class is sandwiched in stochastic order between two uniform fields (Holley's inequality), the robust interval is two ratios of ordinary partition functions, and **uncertainty common to both macrostates cancels exactly**; the width is carried by the sites correlated with the macrostate.  Open: frustrated known parts (the field fails in most random instances), non-monotone macrostates, rotamers, and the range given evaluations.  *(Version 3 said here that a caloric curve determines `ln Z` "without any model"; withdrawn, SCI-MSG-0008.)* |

## 3. What the map says about the programme (the three hypotheses of version 1, confronted with the evidence)

1. **"The programme has a complete theory of the least informative corner."**  *Stands,
   and is sharper.*  Four sections of the theory division's newest work were refereed by
   us (§§11.22, 11.24, 11.25, 11.26): no theorem false.  But the corner is now measured:
   the exponents are evaluated at `βc ∼ 1`, and in our pilot the only physical residuals
   in that regime are torsion refits, for which the class is linear and the exponent
   irrelevant; a solvent term has `βc = 12–53` (F8).  And the reason the corner is
   expensive is its geometry (F9), which no amount of information of the kinds a
   laboratory supplies as averages can repair (F4, F5).
2. **"The untouched axes are the scientifically productive ones."**  *Confirmed on three
   of them.*  Other targets: an observable free-energy difference has a closed-form robust
   range with exact cancellation (F12); barriers and rates need no new kernel (F7).  Other
   classes: linear-information classes are polynomial with matching lower bounds (F9).
   Other information: mostly negative for first-order classes (F4, F5) — which is itself
   the finding: *what measurements are worth depends on the geometry of the class exactly
   as what evaluations are worth does.*
3. **"One physical arena closes the loop: side-chain ensembles on a fixed backbone."**
   *Measured (workstream P2, checkpoint 31): it closes for exposed peptides, at third
   order.*  In backbone torsions nothing closes (F8).  In residue-rotamer variables the
   known part is exactly pairwise, the solvent term is pairwise to `10⁻²–10⁻¹` kcal/mol
   for neutral side chains, the second-order interface has real instances for apolar
   side chains only, and the third-order interface certifies every enumerated instance
   — *given constants obtained by enumeration*.  Still a hypothesis for buried
   environments, and nobody has an a-priori bound on the constants (SCI-MSG-0015).

**The one-sentence state of the frontier.**  The mathematics of certification under a
first-order envelope is correct, deep and — for the many-body terms that matter — about
the wrong class; the right class is a linear-information one whose membership no data can
certify; and the targets on which certified statements are both tractable and observable
are *differences* (between macrostates, between force fields of one lineage, across a
barrier), not totals.

## 4. Questions the map made precise, and where they were sent

| question | sent as | state |
|---|---|---|
| robust interval of `Z_g(A)/Z_g(B)` | SCI-REQ-0001 Q1 | partly answered by ourselves (SCI-MSG-0009); frustrated case open |
| the two-oracle model: non-adaptive exponent; tolerance; a field | SCI-REQ-0001 Q2 | non-adaptive: proved three times; tolerance: SCI-MSG-0006; **field: open** |
| upper boundary of the limit shape | SCI-REQ-0001 Q3; SCI-REV-0002 | open; bridges against walks: requests R3-E1, R3-E2 |
| the thermodynamic oracle | SCI-REQ-0001 Q4 | root proved (referee); **extensive accuracy (addendum A16): free beyond `KL(σ_u‖½)` per site (entropy bracket); below, between the plateau-twin bound and `θ_hint`; the exact exponent is Conjecture A16.4** (SCI-MSG-0012 §4) |
| class constants on a real residual | SCI-RES-0002 (P-E1); SCI-MSG-0015 | backbone torsions: done; **fixed backbone, rotamer variables: done (P2)**; buried environment: requested (P2-E1) |
| a class with known features and a certified remainder; a certified typical-norm remainder | SCI-RES-0002 (P-T2, P-T3) | open |
| a sharp–soft kernel (hypercircle band + pairwise kernel) | SCI-MSG-0007 (X-T1) | open |
| cut checker; kernels over polynomial weights | SCI-MSG-0005 (K-T1, K-T2) | open |
| native certificates against pseudo-Boolean proofs | SCI-REV-0006 (E-1) | open |
| an independent derivation of the cost of the nested adaptive algorithm | `PUBLICATION_OPPORTUNITIES.md` §1 | **workstream R6 running** |

## Change note

*Version 4.*  Rows F2, F4, F5, F7, F8, F9, F12 rewritten after workstreams K, P, X, the
referee R3 and addenda A8–A11; §3 confronts the three working hypotheses of version 1 with
the evidence; §4 lists where each question was sent.  One sentence of row F12 (version 3)
is withdrawn.  Version 3 is at commit `4bb1597`.

*Version 3.*  Rows F6 and F11: findings of workstream A2 (`docs/science/workstreams/A2_REPORT.md`,
SCI-REV-0006).

*Version 2.*  Rows F2–F5: "new here" replaced by what workstream M established
(`docs/science/workstreams/SM_REPORT.md`): the identified-set framework is known as the
generalised moment problem and, for single conformations, as maximum occurrence in NMR;
the divergence-ball dual is Christensen–Connault; the code mechanism behind Theorem 2 is
known; what was not found is stated row by row.  Version 1 is at commit `9180b3a`.
