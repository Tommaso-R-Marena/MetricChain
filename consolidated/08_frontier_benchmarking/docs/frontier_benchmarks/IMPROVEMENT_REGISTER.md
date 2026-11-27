# Improvement register

*Required by owner directive FB-D-3; written at the consolidation ordered by FB-D-5
(2026-11-27).  One row per deficiency that an evaluation of this division found or inherited:
the evidence, the diagnosed cause where there is one, who could remove it, what would count as
removed, and the state.  **While FB-D-5 is in force no row is a request for work**: the
register is the list a next phase starts from.*

Statuses: **open** · **partially resolved** · **resolved** · **disproved** (the deficiency or
its supposed cause turned out not to exist) · **deferred**.
Evidence classes are those of `docs/collaboration/README.md` (addendum); every measurement
below is class A-EXP on development instances unless it says otherwise.

## A. The certified minimum-energy route (structural biology's software, release `1756529`)

| id | deficiency and evidence | diagnosed cause | who | what would count as removed | status |
|---|---|---|---|---|---|
| IR-01 | **17 to 326 times slower than toulbar2** on the four public instances it certifies (`RESULTS.md` §1) | **node rate**, not the bound: the producer enters 0.7 to 2.6 search nodes per second where toulbar2 enters 1,200 to 3,300 (`RESULTS.md` §6.3); with 900 s instead of 300 s it still abstains on all three instances tried, after 620 to 2,306 nodes; about 90 % of its time is message passing over *all* edges at *every* node, in interpreted per-edge loops, and it re-runs its eliminations at every node.  Its tree is 180 to 3,300 times smaller than toulbar2's under the same search strategy (§6.4), which is why it finishes at all | structural biology (producer); engineering (profiling, replication) | protocol FB-P-01, H1 as defined in its amendment 4: certificates on ≥ 90 % of the instances toulbar2 closes within the same budget, total time within a factor 10 on at least half | **open** |
| IR-02 | **abstains on 6 of 10** public instances at 300 s, three of which toulbar2 closes in under two seconds | the same node rate, on instances whose tree is larger than that rate covers in the budget; aggravated by (a) one child per state at a branching, which costs toulbar2 itself 3 to 5 times more nodes than a binary split; (b) no elimination of low-degree variables during search (1.8 to 18 times more nodes for toulbar2 without it); (c) no conflict-driven variable ordering (up to 5.7 times).  **Not** caused by a weak root bound (it is tighter than toulbar2's on every instance, §6.1) and **not** by the missing integrality step (§6.2) — both were our hypotheses and both are disproved | structural biology; theory for the kernel rules a different producer needs (`MATHEMATICAL_FEEDBACK.md` D-1) | as IR-01; in addition no abstention on an instance toulbar2 closes in under 10 s | **open** |
| IR-03 | **the development set does not exercise search**: by the software division's own null method the dual bound alone certifies all twelve of its development instances (its commit `627a860`, read at subject level); on the ten public instances the root bound closes one.  Its hypothesis H3d (within 1–100 times toulbar2) held on its set and fails on the public one | selection of small, well-packed development structures | structural biology | development instances that include search: the ten public instances are development material since our pilot | **open** |
| IR-04 | **scaling**: three of the ten public instances (1,060 to 1,972 residues) are closed by nobody in 300 s — neither route | open; toulbar2's own search does not close them, so no certificate can be copied from it | theory, complexity (tractable subclasses, decomposition, `D-2`); structural biology | a certificate, or a certified gap with a stated bound, on an instance the uncertified solver cannot close — this would be the first result where certification adds reach rather than assurance | **open** |
| IR-05 | **certified baselines were never run**: no pseudo-Boolean encoding with proof logging and a verified checker, no exact-rational dual of the linear relaxation — so "native certificate against existing certified routes" (H2) is untested | not done (FRONTIER-REQ-0001 part A, unanswered at the halt) | engineering | the three-way table of FB-P-01 | **open** |

## B. Model against reality

| id | deficiency and evidence | diagnosed cause | who | what would count as removed | status |
|---|---|---|---|---|---|
| IR-06 | **nothing in the programme has been compared with an experimental observable** by an independent party (`NEGATIVE_RESULTS.md` N-16).  The certificate is exact about a model whose error, by the science division's estimate, exceeds any optimality gap by a factor of sixty to a hundred in accuracy units (SCI-RES-0041) | the guaranteed quantity is the minimum of a table, not a structure | science (error budget, meaning of the guarantee); structural biology (release); this division (evaluation) | protocol FB-P-02 executed: side-chain placement against deposited conformations and established packers, first on a public validation list, then once on the sealed list.  Our written expectation is *no* accuracy advantage (the one published study known to us found < 0.1 %) | **open** |
| IR-07 | **no capability that CASP17 could evaluate**: nothing takes a sequence and returns coordinates | charter and maturity; agreed by structural biology and science | — | not sought | **deferred** (permanent for this season) |
| IR-08 | **certified partition-function intervals exist only on the authors' development models**; no baseline (K\*-type bounds, counting modes of exact solvers, certified model counting, sampling) has been run against them | not done; protocol FB-P-03 is gated on certificate files | structural biology, engineering | FB-P-03 executed on public instances at several temperatures | **open** |

## C. Ensemble identifiability and geometry

| id | deficiency and evidence | diagnosed cause | who | what would count as removed | status |
|---|---|---|---|---|---|
| IR-09 | **validated on planted finite controls only**: 9 of 25 recomputed independently (all reproduced); no software for a general pool ("no forward model and no software", ENSEMBLE-RES-0008 §0); no experimental data set | the mathematics is ahead of any tool | ensemble (specification), structural biology or engineering (tool), science (which data are means, gains, offsets) | certified intervals on a public experimental data set with held-out observables, against maximum-entropy reweighting: coverage at the stated level **and** intervals narrower than the pool's range (thresholds to be fixed before the run) | **open** |
| IR-10 | **the informative object is the interval, not the verdict**: the binary verdict "identified" flips under arbitrarily small displacements (their finding, E-2), and the pool-robust enclosure was 34 times wider than the exact interval in their own check when the pool was coarse against the tolerance | mathematical, stated by the authors | ensemble | evaluation protocols that score intervals and mass bounds; FB-P-04 amended accordingly at the next opportunity | **partially resolved** (mathematics answered; protocol not yet amended) |
| IR-11 | **closest prior art**: population ranges from averaged data are *maximum occurrence* (MaxOcc / maxOR, Bertini, Luchinat, Parigi and co-workers); the ensemble division now lists it and "a published theorem that contains our E1(b)" in its prior-art register | — | ensemble | an explicit statement of what its certificates add to maximum occurrence, tested on the same data | **open** |
| IR-12 | **no stability for distance distributions** (their Problem O4): without a modulus no use of their Part II on distance-distribution data is defensible — they agree | open problem | ensemble, geometry | a modulus, or a counterexample family | **open** |
| IR-13 | **geometry's identifiability statement covers one forward model** (exact averaged squared distances among labelled sites) and is negative for sparse labels (GEOMETRY-MSG-0010); our questions G-1 to G-4 were not answered as posed | scope of the theorems | geometry | a guarantee for a measurable data type with noise | **open** |

## D. Evaluation procedures (our own)

| id | deficiency and evidence | cause | who | what would count as removed | status |
|---|---|---|---|---|---|
| IR-14 | **the sealed list's rule differs from the software division's plan SB-BM-3 in three places**, and two parties were asked to be custodian (the software division's intake, SYNC4 item 2; we have not compared the two rules line by line) | the list was drawn before the plan was final | this division, structural biology, engineering, the research owner | one rule agreed and recorded before the list is opened; if the rule must change, a new list under a new freeze identifier | **open** |
| IR-15 | **the blind check of our scoring code is pending** (FRONTIER-FRZ-0003) and has little power (three easy targets) | the official numbers were announced for 2026-11-29 | this division, when authorised | the comparison by the frozen plan: PASS / EXPLAINED DIFFERENCE / FAIL / NOT ASSESSABLE | **deferred** (needs the owner's authorisation under FB-D-5) |
| IR-16 | **our auditability count was overstated**: "3 of 10 uncertified answers that did not say they were unproved" counted the return value of the Python binding; the solver itself reports an interrupted search through a flag (`limited`).  With the flag read, the count is 0 | we did not know the flag (`NEGATIVE_RESULTS.md` N-19) | this division | FB-P-01 amendment 6 reworded: the variable compares a *checked* proof with a *self-reported* status | **resolved** in the record; the protocol text is amended in §6 |
| IR-17 | **literature rows at snippet or memory level; no established packer, reweighting package or proof-logging solver was run by us** | time; then the halt | this division | every row a frozen protocol relies on confirmed at its source; the baselines run | **open** |
| IR-18 | **no protocol has been frozen and executed as a held-out evaluation** | no release of the software has been frozen for it | all | one frozen protocol, one frozen release, one run on the sealed list | **open** |

## What happened to earlier rows

Nothing was resolved by a change in another division's software during this division's
existence: the register starts at the consolidation.  Answers to mathematical questions are
in `MATHEMATICAL_FEEDBACK.md` (two batches).
