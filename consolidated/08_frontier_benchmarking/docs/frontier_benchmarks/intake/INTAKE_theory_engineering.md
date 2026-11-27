> **Provenance.** Report of a read-only intake reviewer (a subagent of the Frontier Benchmarking
> division, model Claude Opus 5.5) delivered on 2026-11-26 and committed **as delivered**, apart from
> this notice.  It read the named divisions at the pinned commits stated in its first paragraph; it
> re-ran no script and checked no proof.  It is an internal AI reading, not a review.  What the
> coordinator verified directly, and where this report is used, is in `../RESEARCH_INTAKE.md`.
> Sentences marked "evaluator suggestion" or "gaps noticed" are the reviewer's proposals.

# Intake review: Theory and Engineering divisions (read-only, pinned commits)

Reviewer: Frontier Benchmarking, Experimental Evidence and Scientific Evaluation division. Date 2026-11-26.
- **Theory (T)**: `6ebcccd81b3a67a84a320a79bab4a9974a9fa7e8` (2026-11-26 22:04 UTC). Its commit message says: *"work in progress towards the twenty-fourth checkpoint; not yet audited"*. The last audited theory checkpoint is the 23rd, which is the commit that adds THY-MSG-0018.
- **Engineering (E)**: `c683fde48da4004713691983392c74e3cbeaff07` (2026-11-26 17:24 −0500). E's root `README.md` and `docs/` are a stale copy of theory checkpoint `d81eb8a`. E's own material is `ENGINEERING.md`, `docs/engineering/`, `src/metricchain_eng/`, `tests/eng/`, `experiments/eng/` and `modal_jobs/`.

What I read: everything listed in the brief. That includes T `THEORY_REPORT.md` §§6, 8, 9, the §10 table and the start of §12 (items 1–9 and 13), plus a grep for experimental data. I also read E `RESEARCH_LOG.md` "Resume here", `ENG-RES-0015` §§0–1 and §8, and the headers of the drafts.
What I did not read: T `THEORY_REPORT.md` §11 in full; any Lean file; ENG-RES-0002/0008/0013/0014 (apart from quotations of them in the digest, the registry and the ledger); ENG-MSG-0001…0006; THY-REQ/RES; the referee reports.

---

## 1. Owner directives and limits (verbatim)

### 1.1 Scope (research charter)
- E `docs/engineering/DIRECTIVES.md` lines 12–16: "scope = foundational mathematics, theoretical physics and chemistry, general-purpose computational methods, formal verification, fixed-sequence structural characterisation, synthetic computational investigation and appropriate empirical evaluation — **not** biological sequence engineering, target-specific functional optimisation or experimental execution."
- DIRECTIVES.md l.344–350, E's reading of D-6: "Biological sequence engineering, target-specific functional optimization, and experimental execution are outside the current authorization and require separate review and authorization" is not lifted by D-6.
- T `README.md` l.9: "Scope: mathematics, statistical physics, general-purpose certified computation and synthetic evaluation only."
- D-2 §5 (l.51–53): experiments "should primarily serve mathematical discovery, conjecture testing, counterexample generation, proof verification, and evaluation of theoretical complexity"; "application benchmarking is a later phase."
- D-5 §8 (l.228): "Benchmarks … cannot independently prove a general mathematical theorem." D-5 §7 (l.222–223): "Do not treat empirical runtime trends as proofs of computational complexity."
- D-2 §4 (l.49–50): "A general theorem with computationally vacuous guarantees should be explicitly identified as such."

### 1.2 Benchmarking mandate and method
- D-5 §1 (l.162–165): "serious, progressively scaled computational benchmarking of MetricChain's mathematical discoveries, certificate frameworks, and algorithms as they become sufficiently mature"; engineering is "the primary coordinator of substantial shared computational workloads across all six MetricChain divisions".
- D-5 §5 (l.194–206) sets the stages: A independent reproduction → B exact ground truth → C adversarial/assumption-stress ("Distinguish violations of a theorem's assumptions from failures occurring within its stated domain") → D comparison with "fair, well-implemented baselines" → E large-scale Modal → F independent replication. It adds: "When the predicted asymptotic advantage does not appear at accessible scales, report that explicitly."
- D-5 §6 (l.213–218): "prioritize investigating the gap between theoretically favorable asymptotic exponents and actual finite-size performance"; for kernels, "the complete cost of producing and checking a certificate against relevant non-certified alternatives."
- D-5 §8 (l.224–228): hypotheses stated in advance; "No cherry-picking; no removal of hard instances."
- D-6 §4 (l.281–290): benchmark independence. Use "held-out public test cases that the software-development division has not tuned against. Preserve all benchmark outcomes, including failures." D-6 §3: "Do not treat the structural biology division's own test suite as sufficient evidence."

### 1.3 Spending and compute
- D-1 (l.22–25): Modal credit "about $2,000 … must not be exceeded; it need not be used up"; the earlier own stop line was "$1,500 of workspace usage in the month, the worst case of the job about to be launched included".
- D-5 §2 (l.168–184), owner's snapshot "credits $2,030.00, consumed $41.41, remaining $1,988.59". The authorisation: **"I authorize up to $1,750 in additional justified Modal expenditure across the research program"**. Conditions: "Preserve at least $200 of available Modal credits"; "Count the worst-case cost of active, queued, and proposed jobs against the authorized limit"; "Do not incur additional paid charges"; the limit "corresponds to approximately $1,791.41 in cumulative workspace usage"; "If you cannot reliably establish expenditure … defer substantial new jobs"; "The available compute budget is not a spending quota."
- Provisional allocations (D-5 §3, l.185–188): $600 existing MetricChain benchmarking, $350 ensemble, $350 geometry, $250 complexity, $200 replication/final verification.
- D-6 §5 (l.295–298): "The existing workspace ceiling and internal $1,500 workspace-usage stop line, if still operative, are not raised by this directive." "Do not independently increase authorized resource limits."
- **Ask-first threshold** (E's own rule, DIRECTIVES.md l.341–343): "**no job is launched whose worst case would take cumulative workspace usage above $1,500 without first asking the research owner**".
- **Hard stop**: "2026-11-30 15:00 US Eastern" (D-3 §8 l.107; D-5 §12 l.239). Claude credits expire 2026-11-30 19:00 ET. The Modal credit expiry is "Not independently verifiable" (COMPUTE_LEDGER l.16, l.73–77). A **consolidation directive** will come "when approximately $2,000 in aggregate Claude promotional credits remain" (D-3 §8).
- Ledger policy (COMPUTE_LEDGER l.31–78):
  - Launch test: billed $0.00; workspace credits consumed + worst cases of running/queued + the new job ≤ $1,791.41 and ≤ $1,830.00.
  - Staging: "A job whose worst case exceeds **$60** is launched only as a later stage …"; "no single job has a worst case above **$250**".
  - At most 50 containers; nothing deployed.
  - Rule 6: platform restarts mean a worst case bounds one *attempt*.

### 1.4 How other divisions must request computation
- E `docs/collaboration/README.md` l.58–61: "states: the mathematical claim, the exact source commit, the assumptions, the proposed method, baselines, correctness criteria, expected outputs, a resource estimate and a stopping condition." The same nine fields appear in D-4 §6 (l.151–153) and D-5 §9 (queue fields).
- "a request authorises no spending — engineering accepts, defers, revises or declines".
- Readiness test R1–R9 (`benchmarks/BENCHMARK_READINESS.md` l.8–18): exact definitions; explicit assumptions; a precise statement; a pinned commit; a reference implementation or full description; correctness/performance criteria; known limitations; a meaningful baseline; a validation protocol. "A result that fails R1–R5 gets stages A–C only."
- Templates: the draft ENG-MSG-0007 §2 names "GEOMETRY-REQ-0001 and the science division's `TEMPLATE_BENCHMARK_REQUEST.md`". For software releases it lists five intake items (claims with falsifiers, an implementable spec, dependencies/data, own tests, benchmark design). Procedure S0–S6 is in `BENCHMARK_MASTER_PLAN.md` §3a.

### 1.5 Ledger state at E commit
- **Spent before the authorisation**: jobs M-001…M-014 cost $8.73.
- **Spent since the snapshot**: "**$9.01** of credit consumed by the workspace since the owner's snapshot ($50.42 − $41.41 …, 2026-11-26 21:32 UTC)". Billed $0.00.
- The last launch test (M-023, 22:23 UTC) read "credits consumed $52.05, billed cost $0.00". The "total authorised" row still says spent "$0.07", which is stale and inconsistent with the row above it.
- **Committed worst cases at 21:32**: $41.6 (M-016 $6.66, M-020 second tier $27.36, M-021 $7.23, M-022 $0.38). M-023 ($7.22 worst case) was added at 22:23.
- **Running**: M-016 (X-011a; may run until ~2026-11-27 07:30 UTC), M-020 tier 2, M-021, M-022 and M-023. Done: M-017, M-018 ($1.06), M-019 ($0.25).
- Ensemble, geometry, complexity and replication allocations: $0 spent.

---

## 2. Register of evaluable claims

Labels are copied from the source. "Ext. baseline" means a comparison with a non-MetricChain tool or method.

| id | statement | where | label | key assumptions | numerical evidence | campaign / stage | baselines so far | dimensions |
|---|---|---|---|---|---|---|---|---|
| K1 | Min kernel: `verify c I D L = true ⟹ ∀x∈∏D, L ≤ E_I(x)` | T THEORY_REPORT §6.1; `CertificateAlgebra.lean` | [V] `verify_sound`, `verify_sound_real` | pairwise rational instance; real-valued model only if the tables are rounded *down* | conformance vectors `experiments/certs/`; `reference_checker.py --selftest`; Lean kernel evaluation scaling `experiments/coordinator_checks/kernel_eval/results.md` (E2h ok to n=48,k=8, 25 s; E1/E2/E3 encodings fail on memory) | BM-2 stage A/B (via X-012, science's format) | none external; Python reference vs Lean vectors | math guarantees; reproducibility; efficiency (unmeasured) |
| K2 | Residual kernel certifies `L ≤ E+g` for **every** residual of the envelope class consistent with interval anchors, and decides that the class is non-empty | §6.1, §6.4 | [V] `verifyITop_sound`, `IProblem.consistent_iff_nonempty` | envelope constants `c` and anchor intervals are *inputs* (§8: "Certifying such constants for a concrete learned residual is not part of this development") | conformance 3–3f | none | none | guarantees; recognising insufficient evidence (rejects inconsistent data) |
| K3 | Partition kernel: two-sided bounds on Z; the cut/elimination rules are exact on every chain | §6.1, §3.4; `PartitionCertificate.lean`, `PartitionProduct.lean` | [V] `zverifyTop_sound`, `zverify2_sound`; treewidth ≤ 2 is [P] | rational weight tables; voxel enclosures of tables are an input | vector 4/4a; B6 | BM-3 **not started** | none | guarantees; calibration (two-sided) |
| K4 | Sum-free certificates need 2^m leaves on m triangles; with `sum`, 2m | §6.3 Thm 6.1 | [V] `sum_rule_separation*` | rule set of this kernel; disconnected family | B5 | — | — | efficiency (certificate size) |
| G1 | Certificates are coverings in the slack quasi-metric | §10 row G1 | [V] | finite space | — | — | — | interpretability |
| G4 | Product landscapes: one evaluation iff every site is sharp, otherwise exp(nR*) | row G4; Thms 11.6–11.9 | lower bounds [V]; upper bound [P] | site types fixed as n grows, margin bounded away from 0 (ASSUMPTION_AUDIT §4 item 9; THY-MSG-0018 §1.2) | B8 (layer counts n≤400 approach R* from above) | — | internal formulas | guarantees; efficiency |
| G5 | Minimal certificates are NP-hard to find | row G5 | [V] | — | — | — | — | complexity |
| G11 | Every algorithm, randomised or not, pays (1−2δ)× every fractional covering bound; for ln Z on the cube there is a threshold `n ln cosh(βc/2)` | row G11, §11.10 | lower bounds [V]; upper bounds [P] (Harper [K]) | cube or product class; evaluation oracle | B10 | — | — | guarantees; recognising insufficient evidence |
| G18 | Plain Monte Carlo is optimal among non-adaptive algorithms on the cube class | row G18 | [V] "given two finite sums"; rest [P], refereed R5 | uniform cube, zero known part | B12 | — | — | guarantees |
| A1 | Theorem 11.56 (Alg 2L⁺): a hint-free adaptive exponent h at every bounded accuracy, against a for non-adaptive algorithms | row G21; §11.19 | [P], refereed R8 "proved" | uniform cube, one slope, exact evaluations | X-005 (7 095 840 mean runs, no claim violated); X-006b (585 000 literal runs, no failure); X-009 (certified adaptive cost below the non-adaptive lower bound from n=1400 at u=1) | **BM-1: A, B, C, D(X-009) done; E running (X-011)** | non-adaptive base bracket; enumeration; lower bounds (all internal) | efficiency; scaling; stability |
| A2 | Nested levels chosen by certified cost: three levels are certified below the exact two-level cost from n≈16 000 | README (xxii); §11.19 rem. (1b) | coordinator's exact evaluation, replicated by science | as A1 | ENG-RES-0015 draft: at n=8000 the certified designs keep "0.84 of what a third level gains in the limit, 0.54 of a fourth and nothing of a fifth"; "The best certified bound is 1.9–4 times the lower bound in the exponent" | BM-1 E (M-016/M-020/M-021 running) | the flat-tuned referee design (internal) | efficiency; generalisation (finite size) |
| A3 | Thm 11.58a: `ln N ≤ nh + O(√(n ln n))`; Thm 11.58e: `nh + O(n^{1/3}(ln n)^{2/3})` | README (xxii), (xxiv); rows G40, G43 | 11.58a [P] refereed R12; 11.58e [P] refereed internally, "nothing is machine-checked", the certified computation is unrefereed. **11.58e is in the WIP commit; T `status/theory.md` l.44 still lists "Theorem C" as "Not established"** | as A1 | 11.58a's schedule "costs more than the non-adaptive bound `n·a` up to `n ≈ 2·10⁴`" (ASSUMPTION_AUDIT §5) | Q-17 (n=1.28·10⁵ running; 10⁶ not ready) | — | efficiency; vacuity |
| A4 | Rate of nested levels: `k²(τ_k−h) → 2π²h²θ_hint″(0)` | Thms 11.53a/b; row G41 | [P] refereed internally; line lemmas [V] `LineDynamics.lean` | convex θ_na, smooth strictly convex fixed point (with a kink the rate is 1/k) | floating point; Gaussian lower bound exact | Q-13 (subagent, in progress) | — | guarantees (asymptotic only) |
| A5 | Abstract nesting theorem; **a false certificate under unbounded influence**; no gain on Gauss space | §11.33; row G42 | [P] refereed internally | tail functions; certified class-relative influence | "reproduced by the referee in every one of 120 runs" | none at E | — | reliability; recognising insufficient evidence |
| P1 | Profile-format certificates for pair-additive Lipschitz residuals: the number of evaluations is bounded independently of chain length at extensive accuracy | §11.17; row G19 | exactness [P]; `verifyLTop_sound` [V] | residual is a functional of pair-distance statistics; "no chirality, no sequence-specific terms" | X-002 (lattice to 24 torsions), X-004 (off-lattice to 12): **certificates grow at every enumerated size** (D46) | BM-4 A,B (lattice); off-lattice on hold until exact arithmetic (Q-06) | HiGHS/CP-SAT used as tools, not as competitors | generalisation; vacuity |
| P2 | Limit shape of bridges; the limit points of certificate size lie in [116, 3 627]; convergence for walks | §11.22; row G24 | bridges [P, computer-assisted]; abstract limit theorems [V]; walks [C]; "a few hundred", "10³–10⁵ beads" [N] | one synthetic lattice model | — | BM-4 / Q-07 not started | — | generalisation |
| P3 | Per-torsion constants grow like m^{3/2}, so weighted-Hamming certification of long chains is exponential (negative) | §11.14; row G16; D42 | [P] | product domain; ignores excluded volume | B7 (RMSD bound vs actual: e.g. 96 torsions, ε=0.10: bound 19.61 vs actual 2.01) | — | naive lever-arm bound (classical) | reliability (negative) |
| S1 | Free-energy sandwich width `β²Σc_i²/8` for product references; false for correlated references | §3.2; G10 | [V] `free_energy_sandwich`, `mcdiarmid_no_better_constant` | product reference (D14) | B4: compared with Hoeffding, McDiarmid, Rio | — | **classical published bounds** (favourable) | uncertainty calibration; guarantees |
| S2 | Share / dual certificates for "the reference is the minimum"; a third-order model reduces to pairwise | Props 11.18b(e), 11.18a; G33 | sound direction [V] (`ShareCertificates.lean`, `StateShares.lean`, `ThirdOrderModel.lean`) | completeness only on product domains (one false statement corrected) | science's 9 certificate files, independently checked by E X-012 | BM-2 stage A/B **done** | science's reference checker (internal) | reliability; reproducibility |
| S3 | A 20-residue model peptide: a bracket of ln Z from 87 441 of 3.5·10⁹ states | README (xvi); Thm 11.18d; §12 item 13 | only the combinatorial core [V]; the rest is science's paper proofs and "unreviewed code" | "relative to a force-field model, and it fails for helices and charged side chains" (later helices of one side chain); rigid backbone, rotamer grid | science branch (not read) | BM-3 / Q-08: "not ready" | none | **model-relative**; calibration |
| S4 | Box classes: cost = Boltzmann factor of the free-energy distance to the floor | §11.30; G32, G36 | "elementary; **unrefereed**"; parts [V] `BoxClass.lean` | exact samples of the known part; a *certified floor*, "which for no force-field term exists today" (§8) | science enumerations (0.005–9 k_BT per residue) | — | — | vacuity; recognising insufficient evidence |
| S5 | Second-order classes: polynomially many evaluations below Curie–Weiss `βc₂n=4` | Thm 11.33; G15 | [P]; **was false as stated, restored** (D65) | additive known part | — | — | — | vacuity: "about `n⁵ε⁻²`" (ASSUMPTION_AUDIT §5) |
| R1 | Spectral realizability bound for predicted distances; trace-enhanced bound | §4.1; B3 | [V] `Realizability.lean`; novelty withdrawn (D12: "KNOWN", Sonthalia et al.) | — | B3 | — | classical MDS strain bound (favourable, ×1.0–4.0) | stability; interpretability |
| H1 | Heterogeneous slopes: type-aligned nesting with certified finite-n constants (E's own Theorem K1 transfer) | E draft ENG-RES-0016 §2 | [P] ours, "not refereed" | two site types, binary sites | M-018 (75 cells); 57 600 literal runs, none invalid | BM-6 | homogeneous algorithm at the steepest slope; exact lower bound | generalisation |

---

## 3. Software inventory on the engineering branch (E)

| module | what it does | tests (def count in file; parametrised) | independent verification |
|---|---|---|---|
| `chains/` (`dia_enum.c`, `dia_flip.c`, `profile_cover.py`, `generic_chain.py`, `lattice_analysis.py`, `generic_analysis.py`) | exhaustive enumeration of diamond-lattice and off-lattice rotamer chains; profile classes; exact covers (HiGHS MILP) | `test_chains.py` 15 | written from P_REPORT definitions; all published lattice values reproduced (`run_lattice.py --check`); "two-solver validation" **withdrawn** (ENG-MSG-0004 §4); off-lattice in floating point with a tie analysis |
| `leafcert/` (`leafcert.c`, `pycheck.py`, `loader.py`, `ckernel.py`) | exact checker for the science division's "shares at the leaves" certificates; C (no FP, 128-bit sums) plus an independent Python engine | `test_leafcert.py` 37 defs; REPORT says "182 tests" (188 in the long run) | written by a subagent *from the text only*; coordinator's 30-line third checker; 24 092 fuzz certificates and 26 865 mutants with 0 unsound acceptances; 23+18 broken copies detected. "the checker is tested, not verified"; "no formal link to the Lean `verify`"; gcc 15.2 x86-64 only |
| `twolevel/` (`alg2l.py`, `certified.py`, `meanrun.py`+`meanrun_kernel.c`, `simulate.py`, `adversary.py`, `hetero.py`, `sampling.py`, `tables.py`) | Alg 2L⁺ constants; certified nested-cost recursion; mean-run evaluator (Python reference + C port); literal runs; differential-evolution adversary; heterogeneous slopes; exact large binomial sampler | `test_twolevel.py` 28, `test_certified.py` 9, `test_hetero.py` 10, `test_slices.py` 3 | 324+18 workstream-K rows reproduced; the referee's 48 three-level numbers reproduced; the C kernel tested against Python; 2 624 maximisers re-evaluated. **Searches not converged at n≤500** (SCI-REV-0018 finding M1; ENG-RES-0017 withdraws a conclusion) |
| `weighted_cube/` (`polytope.py`, `chambers.py`, `exponents.py`, `wcube_kernel.c`) | exact vertex enumeration of weighted-cube Lipschitz polytopes (four enumerators); block bounds for workstream Y | `test_weighted_cube.py` 31 | cross-checked with an independent library (`pplpy 0.9.0`); coordinator's brute force at L=3 (96/72 vertices) |
| `modal_jobs/` (6 apps) | ephemeral Modal runners; `bench_app.py` refuses a tree that differs from its commit | — | — |

E status (stale, checkpoint 5): "`python -m pytest tests/eng -q`: 153 tests pass". At this commit there are 133 test defs across the 7 files, before parametrisation.
**Not in the E tree at this commit**: `src/metricchain_eng/leafprod/` (the certificate producer) and `experiments/eng/leafcert_bench/`. They are cited in BENCHMARK_MASTER_PLAN §3a as "(in review)" and in RESEARCH_LOG "Resume here" item 3(d) as in-flight, untracked subagent files. The same applies to `geometry_req1/`, `level_rate/` and `review_x014/`.
On T: the theory audit (`scripts/audit_all.sh`) was replicated by E at four heads (`d81eb8a`, `4cef47e`, `63efc69`, `9408e33`: AUDIT PASSED; 435 mutations, 434 caught, 1 expected pass). **No theory head after `9408e33` has been audited by E**, the pinned T commit included (RESEARCH_LOG item 5).

---

## 4. Comparisons with external (non-MetricChain) tools or published methods

| capability | external tool or method | version | instances | outcome | where |
|---|---|---|---|---|---|
| Min-energy certificate kernel (K1) vs exact solvers / proof logging (toulbar2, OSPREY, VeriPB, CakePB, PBLean, VIPR) | **none run** | — | — | T §6.4: "whether a native format is cheaper than that route has not been measured". The only figures are *literature* ones: verified PB checking "within a factor 20 of solving time (median 1.43; Koops et al. 2025)", MaxSAT proof logging "median overhead below 2 %". "Neither OSPREY nor toulbar2 emits checkable proofs" (literature claim). E agenda E-1 ("native kernel against pseudo-Boolean proof logging") and SCI-REV-0006 E-1 are both "planned / not started" | T §6.4; E status/engineering.md |
| Min kernel vs non-certified exact solvers | CP-SAT (OR-Tools 9.15, installed), DP, B&B, enumeration: **specified, not run** | — | — | Q-14 "not ready: needs a producer and a written baseline specification". The "commercial-grade open solver" of MASTER_PLAN §3a is in the untracked `leafprod` work, not in this commit | BASELINE_SPECIFICATIONS BM-2; registry Q-14 |
| Partition kernel / sandwich certificate | AIS, thermodynamic integration: **planned only** | — | — | BM-3 not started | BASELINE_SPECIFICATIONS BM-3 |
| Nested adaptive algorithms (BM-1) | none external; Monte Carlo without certificates is explicitly excluded ("they solve another task") | — | — | all baselines are internal (enumeration, non-adaptive base bracket, lower bounds, flat-tuned designs). Unfavourable internal results: at simulable sizes the adaptive algorithms are worse than plain Monte Carlo (README cycle 10 (iii): "at the sizes that can be simulated the algorithm is worse than plain Monte Carlo"); see §5 | BASELINE_SPECIFICATIONS |
| Chain covers | HiGHS (SciPy 1.18.1), CP-SAT (OR-Tools 9.15.6755), used as *tools* | as stated | lattice n≤24, off-lattice n≤12 | 10 of 25 open lattice brackets have a lower end that is "the solver's bound at its time limit". The two-solver claim was withdrawn | ENG-RES-0002, -0007; ENG-MSG-0004 §4 |
| Random sampling | NumPy `Generator.binomial` (2.5.5) | 2.5.5 | grid of 92 cells | **unfavourable to NumPy**: "mean up to −0.8 %, variance −6 % already at 2⁵³"; replaced by an exact sampler | ENG digest item 4; ED-8 |
| Synthetic benchmarks B1–B13 against classical bounds | Goldstein/global-oscillation DEE; classical MDS strain bound; Hoeffding / McDiarmid / Rio; naive lever-arm RMSD bound | in-house implementations | random synthetic chains (n=6, k=3, 40 instances, etc.) | favourable to the project's bounds, e.g. B4 at βc=1: Hoeffding 4.500, McDiarmid 0.750, Rio 0.740; B3 trace/strain up to 4.00. The prior-art review classifies many of these bounds as known (D11, D12, D24) | T `docs/benchmarks_output.txt`; `separation_benchmarks.py` |
| Lean kernel evaluation scale | Lean `decide +kernel` | Lean 4.31.0 | n≤48, k≤8 leaves | one encoding checks 1.5·10⁵ table entries in ~25 s; others run out of memory | T `kernel_eval/results.md` |

**There is no comparison with toulbar2, OSPREY, VeriPB, CakePB, any ILP/MIP solver used as a competitor, or any published side-chain or conformational method.**

---

## 5. Negative results, dead ends, stated limitations

- **Theory DEAD_ENDS** (D1–D68). The most consequential:
  - D11/D24: novelty withdrawn. DEE gauge facts are folklore. The Hölder decomposition is weighted mini-bucket. The sandwich is "known-in-spirit". A1–A5 envelope duality is "known in substance". The trace s-stress bound is known. The tree-vs-DAG separation is in Basu et al. 2023.
  - D26/D30/D39: best-first search is not near-optimal without augmentation.
  - D29/D35: exponents fail at exponentially small accuracies.
  - D32/D40: "second-order envelopes are the way out" overstated.
  - **D42**: "the weighted-Hamming route cannot certify long chains".
  - **D46**: profile certificates grow at every enumerated size.
  - **D61**: three flat-tuned levels give "no certified gain", which E found (ENG-RES-0014).
  - D65: Thm 11.33(a) false as stated, restored.
  - D60: "randomised needs the ball" false as written.
- **Referee verdicts** (T README): R2 judged the cluster "a coherent note, not a theorem-driven paper"; "the tools are standard and the proofs short". R1 classified the phase-1 mathematics as "elementary or classical in substance". T `ASSUMPTION_AUDIT.md`: 47 summary sentences "stated more than is proved". All referees are AI agents: "internal reviews, not external peer review" (BENCHMARK_LIMITATIONS; THY-MSG-0018).
- **Computationally vacuous guarantees** (T ASSUMPTION_AUDIT §5):
  - Thm 11.33(a) ≈ `n⁵ε⁻²`;
  - the `(Σc_i)²` width is vacuous once `βΣc_i>8`;
  - isoperimetric error terms bite only from n≈10¹¹–5·10¹⁴;
  - profile-certificate bounds;
  - voxel cost `d^{d/2}`;
  - the nested algorithm "not competitive at any size where it can be evaluated" (README (xxii)).
- **T §8 limitations, verbatim highlights**: "No claim of practical performance. All experiments are synthetic and small"; "Envelope constants are inputs"; "Evaluations are counted, not computation"; "Second-order envelopes are an interface without an instance".
- **Engineering ED-1…ED-8**, notably ED-3 ("exact set cover … stays easy" false beyond 18 torsions), ED-4 (reading a plateau off a short range) and ED-8 (NumPy bias, found by science).
- **BENCHMARK_LIMITATIONS** (E):
  - mean-run model only;
  - "Worst cases are searches", i.e. lower bounds on the worst case;
  - finite design families;
  - one class, one accuracy (0.8715), one δ (0.05);
  - "a finite-size table cannot confirm an asymptotic law";
  - BM-2: "no producer yet", and acceptance applies to "the published integer instance";
  - BM-7: "certified" means "certified for the published integer instance".
- **ENG-RES-0017 (draft)** withdraws ENG-RES-0014 §4: non-product instances *can* cost more; the excess was a search shortfall. New rule: cross-evaluate maximisers before reading a difference between two searches.
- **X-012 finding**: the science division's reference checker `p7_06_check.py` "can return True for a false bound on malformed input". This does not affect the nine files.

---

## 6. Queue and pending work at engineering (E `BENCHMARK_REGISTRY.md`)

| id | what | status / waiting on |
|---|---|---|
| Q-01 (X-011a) | certified cost of nested 2L⁺, 2–6 levels | M-016 running (until ~2026-11-27 04:20–07:30 UTC); M-021 for u=½, 2 |
| Q-02 (X-011b) | certified-cost designs run vs the flat-tuned design | stage 1 done (M-017), stage 2 running (M-020), literal runs done (M-019) |
| Q-03 | two-level worst cases at n=8k/32k/64k | done |
| Q-04 (X-012) | leaf-certificate checker | done (A, B) |
| Q-05 (X-013) | weighted-cube vertices | registry says "in progress"; a REPORT.md exists in the tree |
| Q-06 | off-lattice chain in exact arithmetic over ℚ[cos θ] | accepted, not started |
| Q-07 | enumeration job (bridges, histograms) | accepted, not started; first stage ≤ $60 |
| Q-08 | sandwich-certificate checker | "not ready": the certificate is not a file; waits on science |
| Q-09 | profile constants (THY-REQ-0003) | not started |
| Q-10 | slopes ½, 2 | entered as M-020/M-021 |
| Q-11 (X-014) | heterogeneous slopes | bounds done (M-018); an adversarial referee subagent is in flight |
| Q-12 | GEOMETRY-REQ-0001 exact elimination | subagent in progress |
| Q-13 | numerical check of Theorem R (rate 1/k²) | subagent in progress |
| Q-14 | BM-2 C–E: produce/check cost against exact solvers | **not ready**; needs a producer and a baseline spec |
| Q-15 | SCI-REV-0018 re-search | (i) done; (ii), (iii) running as M-023; ENG-RES-0017 in draft |
| Q-16 | GEOMETRY-REQ-0006: certified maximum of a trigonometric polynomial on a 4-torus | accepted, next cycle |
| Q-17 | real certified designs at n=10⁵–10⁶ against the formulas of Thms 11.58a/A/Z | 1.28·10⁵ inside M-016; 10⁶ not ready |
| Q-18 (BM-7) | structural-biology software verification | waiting for a first release (no branch at 22:03 UTC) |
| Q-19 | directed-rounding path from real energy to integer tables (assumption A9) | design started; waits for the energy terms to be named |

M-023 = X-005c (Q-15). Unpublished drafts: ENG-MSG-0007, ENG-RES-0015, -0016, -0017. They contain placeholders (`<<DATE>>`, `<<MAXRISE>>`) and were "written from partial data", so **none of their numbers is published yet**.
Waiting on theory: a referee for ENG-RES-0016 §2 (believed to be an instance of Theorem N3); E-C4 (Thm 11.58e), now WIP on T. THY-MSG-0018 §6 offers a small task, an interval evaluation of orbit curves ("decline freely").
Accepted, lower priority: THY-REQ-0004 (linear kernel), -0007, -0009, -0010 Q1/Q3, and many SCI requests that are "not read in full".

---

## 7. Gaps noticed

1. **No external baseline for the main capability.** The headline novelty claim is that the residual kernel's "for every residual" quantifier and the native min/partition kernels are distinct from proof logging (T §6.4). Yet no measurement compares them with toulbar2/OSPREY (uncertified exact or approximate solvers), VeriPB/CakePB (PB proof logging), MIP with VIPR, or AIS/TI for ln Z. T itself says the evidence for distinctness is "a comparison of statements … and an absence in searches, not a proof of novelty".
2. **The certificates are model-relative and could be misread as physical accuracy.**
   - Every kernel bounds the energy of the *published rational/integer instance* and, for residuals, only for the *published* envelope constants and anchors.
   - Nobody has proved the real-to-integer rounding step (A9; Q-19). No certified envelope constant exists for any real residual. "a certified floor … for no force-field term exists today".
   - S3 (the 20-residue peptide bracket) is relative to a vacuum force field plus generalised-Born, on a rigid backbone and rotamer grid. It says nothing about agreement with experiment.
   - T §11.17: "no experimental data are used". The scattering identifiability theorem is the only place a measurable quantity appears.
3. **No contact with experimental data.** Neither branch uses PDB structures, NMR/SAXS ensembles or measured free energies. B1–B13 are random synthetic models. Evaluating predictive accuracy against experiment is entirely open and would have to be built from scratch, inside scope as "fixed-sequence structural characterisation" and outside sequence design.
4. **Asymptotic claims without a falsifiable finite-size benchmark.** A3 (11.58e), A4 and §11.33 are exponent statements. Their only finite-size evaluations (X-011, Q-17) show large overheads: certified bounds 1.9–4× the lower bound in the exponent, and the schedule worse than non-adaptive up to n≈2·10⁴. A benchmark that fixes a predicted crossover size in advance would make them falsifiable. Note that T's status file and the WIP commit disagree on whether "Theorem C" is established.
5. **Self-referential baselines in BM-1.** Every comparator is an internal design or a bound. Excluding uncertified Monte Carlo is defensible for "same task", but it hides the practical comparison: plain MC is cheaper at every simulable size. That should be reported alongside the certified comparison.
6. **Worst-case searches are known to stop low** (SCI-REV-0018 M1). X-010 and X-011 used the old starting points and "have not been repeated", so "worst instance found" figures may be low.
7. **Stale or inconsistent records at E.**
   - BENCHMARK_READINESS still says there is no literal three-level simulation, and BENCHMARK_LIMITATIONS still says "not at all for nested runs". M-019 ran 1 280 literal three-level runs (15 sites).
   - The ledger's "total authorised" row says spent $0.07; the other rows say $9.01 and $52.05 consumed.
   - `status/engineering.md` is at checkpoint 5.
   - The root README is a stale theory copy.
   - Q-05 says "in progress" while a report exists.
8. **The pinned T commit is unaudited**, both by T itself ("not yet audited") and by E (latest audited `9408e33`).
9. **Kernel scale is unmeasured at realistic sizes.** Lean `decide +kernel` fails on memory beyond about 10⁵ entries for most encodings. The integer leaf checker "written for the kernel" lacks a refinement proof (T §12 item 7). E's C checker is "tested, not verified". There is no producer, so production cost is unknown.
10. **Ability to recognise insufficient evidence is a real, testable strength.** Inconsistent anchors are rejected (`inconsistentInterval_rejected`), and the A5 obstruction yields false certificates under unbounded influence. A benchmark should deliberately violate the assumptions (envelope constants too small, correlated references) to show whether the system *fails safe* or certifies wrongly. Inside the hypotheses the guarantees are formal; outside them nothing checks the inputs.
