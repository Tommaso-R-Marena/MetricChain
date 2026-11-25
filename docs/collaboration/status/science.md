# Status of the Scientific Discovery, Translation & Independent Validation Division

*Updated at checkpoint 28 of the science branch (2026-11-25; the commit time is
authoritative).  Branch `research/scientific-translation`.*

## Pins

| what | commit |
|---|---|
| branch point (theory head when the division started) | `5ed407282d89af46d260d2dd1687059c8e3e7728` |
| latest theory commit read | `40c5bd7` (their twelfth checkpoint: THY-MSG-0012, THY-RES-0005 read in full; R10 report and report changes not yet read by the coordinator; our tree is built on `5ed4072`) |
| latest engineering commit read | `a2f6dc7` (digest and ENG-MSG-0003 §§1–3); computations and workstreams use `db56d05` |

Details and reading depth: `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`.

## Environment and permissions (verified, not assumed)

* A cloud container (Linux, 4 cores, 15 GB RAM, ephemeral disk), Python 3.13 with NumPy,
  SciPy (HiGHS), mpmath, SymPy; Lean 4.31.0 with the pinned Mathlib cache installed during
  this session.  Web search and paper-search tools are available to the coordinator and to
  workstreams; full-text access varies by publisher and is reported per source.
* Git: read access to all branches; push verified for `research/scientific-translation` only.
  We write to no other branch, open no pull request, force nothing.
* **No Modal access and none sought.**  Remote computation, if ever needed, is requested from
  the engineering division with a specification; a request is not an authorisation.
* Resource balances (API credits, Modal) are not visible from this environment; nothing
  here spends Modal credit.  Deadlines as stated by the research owner: expensive workloads
  by 2026-11-30 15:00 ET, credits expire 2026-11-30 19:00 ET.

## Current investigations

| id | subject | kind | state |
|---|---|---|---|
| PI | **inference limits** — what energy evaluations, ensemble-averaged data and thermodynamic data jointly determine; identified sets with dual certificates; falsification certificates; exact identified sets on the lattice chain; robust ranges of observable free-energy differences | own theory + numerics | **version 3** of `docs/science/INFERENCE_LIMITS.md` (refereed by R3, corrected; cores machine-checked by L1); later results in `INFERENCE_LIMITS_ADDENDA.md` A1–A11 |
| A1 | prior art, full text: the query-complexity cluster (theory report G11, G18–G23, G25–G27) | originality | **reported, final** (SCI-REV-0004; addendum on THY-REQ-0011 B1, B2: SCI-RES-0003) |
| A2 | prior art, full text: kernels vs proof logging; certificates as coverings; lever arm; profiles vs scattering / homometry; limit shape | originality | **reported** (`workstreams/A2_REPORT.md`; SCI-REV-0006) |
| M | prior art for the measurement side | originality | **reported**, with follow-up (`workstreams/SM_REPORT.md`; SCI-MSG-0002, -0003) |
| R1 | independent review of theory report §11.25 → SCI-REV-0001 | review + replication | **reported and published** (`workstreams/R1_REPORT.md`) |
| R2 | independent review of theory report §11.22 → SCI-REV-0002 | review + replication | **reported and published** (`workstreams/R2_REPORT.md`) |
| R3 | adversarial referee for our own `INFERENCE_LIMITS.md` v2 | review + replication | **reported and published** (`workstreams/R3_REPORT.md`; SCI-MSG-0008; the note is now version 3) |
| R4 | independent review of theory report §11.24 (rounds) → SCI-REV-0003 | review + replication | **reported and published** (`workstreams/R4_REPORT.md`) |
| R5 | independent review of theory report §11.26, Theorems 11.99 and 11.101 (THY-REQ-0011 A1) → SCI-REV-0005 | review + replication | **reported and published** (`workstreams/R5_REPORT.md`) |
| P | a real force field against the envelope classes; physical reading of every object of the theory | measurement + analysis | **reported and published** (`workstreams/SP_REPORT.md`; SCI-RES-0002; `docs/science/PHYSICAL_APPLICABILITY.md`) |
| K | certified kinetics: barriers, exit times, capacities | own theory + Lean | **reported and published** (`workstreams/SK_REPORT.md`; SCI-MSG-0005) |
| X | alternatives to worst-case classes (average-case, weighted, structural conditions) | own theory | **reported and published** (`workstreams/SX_REPORT.md`; SCI-MSG-0007; `docs/science/ALTERNATIVE_FRAMEWORKS.md`) |
| L1 | Lean formalisation of the short cores of our own results (files outside `proofs/`) | formalisation | **reported and published** (`workstreams/L1_REPORT.md`; eight files, 78 theorems, re-compiled by the coordinator; SCI-MSG-0008 §4) |
| R6 | **second wave:** independent line-by-line review, with own re-derivation and implementation, of the cost of the nested adaptive algorithm (theory report §§11.18–11.19) → SCI-REV-0007 | review + replication | running (launched after checkpoint 19) |
| P2 | **second wave:** class constants of the GBn2 term in rotamer variables on a fixed backbone | measurement | running |
| L2 | **second wave:** Lean — addendum A11, the referee's finite inequalities, Proposition A1.2 | formalisation | **done** (checkpoint 29): 178 theorems in three files, Mathlib only; re-compiled by the coordinator; `L2_REPORT.md`; SCI-MSG-0014 |
| R7 | **second wave:** independent review and replication of the engineering division's results (off-lattice chain enumerations and covers; lattice covers as certificates; the Harper closed form; the statistics and claims of the adversarial test of Algorithm 2L⁺; traceability of the record) | review + replication | running (launched after checkpoint 24) |
| F | **second wave:** the two-oracle model with a field — does a one-body marginal oracle lower the exponents on the `p`-biased cube? | own theory + numerics | **done** (checkpoint 30): `SF_REPORT.md`; SCI-RES-0006.  The coordinator's conjecture: true as a statement, false as an explanation |
| R8 | adversarial referee of our addendum A16 (mean-energy datum at extensive accuracy; Lemma A16.5; Theorem A16.6; Conjecture A16.4), which had no second reader | independent review + own numerics | running (launched after checkpoint 28) |
| — | replication of `scripts/audit_all.sh` at theory head `5ed4072` on this machine | replication | **completed: `AUDIT PASSED`** — 56 Lean files, 3423 declarations, 267 mutations (266 caught, 1 expected pass); first replication of the three Lean files added since `63efc69`; `docs/science/INDEPENDENT_VALIDATION.md` §1.1 |
| — | replication of the engineering lattice-chain class tables | replication | **completed for `n = 1 … 10`: identical** (own enumerator; and by workstream R2 for 4–23 beads); `INDEPENDENT_VALIDATION.md` §1.2 |

Briefs: `docs/science/workstreams/*_brief.md`; shared rules: `docs/science/workstreams/COMMON.md`.
**What counts as published.**  The working directories of running workstreams
(`experiments/science/ws_*/`) and their report files (`docs/science/workstreams/*_REPORT.md`) are
committed as *recoverable snapshots* while the work is in progress: they may change, and
the coordinator has not read them.  A workstream's findings are a statement of this
division only once the digest (`SCIENCE_TO_ALL.md`), a `SCI-*` message or
`docs/science/INDEPENDENT_VALIDATION.md` cites them.  (Until checkpoint 7 this file said that
unread reports are not on the branch; that policy was changed so that nothing is lost if
the container is reclaimed.)

## Findings so far (each with its status)

| # | statement | status |
|---|---|---|
| S1 | cube class: ensembles with exactly uniform `k`-body marginals and entropy within `⌈k/2⌉ ln(2n)` of the class minimum (invisible order) | **[P]**, exact enumeration `n ≤ 16`; prior art unchecked |
| S2 | cube class: uniform `k`-body marginals bound every basin population **from above** by `≈ t!/(n^t(1−2ρ)^{2t})`, `t = ⌊k/2⌋`; attained up to constants; **no lower bound** (corrected, SCI-MSG-0008) | **[P]**, enumerated; Markov form **[V]** (L1); the point case is the Rao bound **[K]** |
| S3 | a `k`-body marginal oracle divides the all-algorithms lower bound at the zero residual by at most `(2n)^{⌈k/2⌉}`: `θ_hint` unchanged | **[P]**; relies on theory Theorem 11.22 (pattern) and, for the value and attainment of `θ_hint`, on Theorems 11.25, 11.54, 11.58 (not reviewed by us) |
| S4 | with the mean residual energy in the true ensemble as a datum, `ln(Z_g/Z_0)` is bracketed with width `J(μ₀, μ_g)`; at the zero residual `O(nb²/ε²)` evaluations suffice | inequality **[K]**, reading **[P]**; the oracle is an idealisation **[H]** |
| S5 | maximum-entropy refinement against exact data: `TV ≤ β·osc(r)/4`, `KL + KL ≤ (β·osc(r))²/4`, dimension-free | **[P]**, 3 906 random instances; prior art unchecked |
| S6 | the pair-distance-profile class of theory report §11.17 is the class identified by (partial) pair-distance distributions, i.e. by scattering data | **[K]** (exponential families; Henderson) — a translation, not a theorem of ours |
| S7 | the residual maximising a ratio of macrostate partition functions over an envelope class is not constant on the macrostate (three-point example) | **[P]** |
| S8 | the verified `(min,+)` and `(+,×)` kernels are dual-feasibility checkers for identified sets of ensemble averages (model-free; KL ball); for envelope classes the dual object is a flow with gains | soundness **[P]**, duality **[K]** |
| S9 | **at bounded accuracy** a mean-energy oracle does not lower the worst-case exponent: a visible basin can have a hidden twin with exactly the same mean energy and `ln Z` larger by `≈ ln 2`; at extensive accuracy see S34 | mechanism **[P]**; the root **[P]** by the referee (R6), **second full reading by the coordinator done at checkpoint 21 — no gap** (addendum A12); **[N]** before |
| S10 | data certify a *lower* bound on the envelope constant and on `KL(truth‖model)`; on the lattice chain the three-shell profile certifies `0.87–0.96` of the strength of a missing contact attraction | soundness **[P]**; numbers **[N]**, exact LPs, 8–9 beads |
| S11 | lattice chain, model-free: an exact averaged three-shell profile leaves the mean gauche fraction undetermined over `0.65` of its range at 27 beads (from the engineering tables), widening with length; a complete pair-distance histogram leaves `0.33` at 15 beads | **[N]**, exact LPs |
| S12 | the limit shape of theory report §11.22 is the asymptotic model-free identified set of (mean profile, mean gauche fraction); its upper boundary is not computed | **[P]** given theory Theorem 11.69 (bridges); walks under Conjecture 11.75 |
| S13 | model + envelope class + data together give intervals several times narrower than each alone (9 beads) | **[N]**, exact LPs |
| S14 | a marginal oracle leaves the non-adaptive exponent unchanged as well (Theorem 4′ = theory's Proposition 11.104, proved independently); with all marginals of order `αn` free the exponent lies in `[h_hint − h(α), (1−α)h_hint]` (Theorem 4‴) | **[P]**; the first half derived twice |
| S15 | **finite precision:** correlation data of *every* order to absolute precision `τ ≥ e^{−o(n/ln n)}` leave `h_hint` unchanged (Theorem 4-τ, constants for every `n`); for entropy the statement is exact (Theorem 2-τ); `n` pinned one-body marginals to precision `τ` give `ln Z` to `O(nτ)` | **[P]**; exact rational checks to `n = 800`; SCI-MSG-0006 |
| S16 | Theorem 7 sharp: `KL ≤ w²/8`, `TV ≤ tanh(w/4)`, `w = β·osc(r)`; mechanism is Barron–Sheu (1991) | **[P]**, **[K]** for the mechanism; SCI-MSG-0003 |
| S17 | **which class real residuals live in:** same-lineage force-field differences are exactly additive / residue-local; charge-model changes `βc ≈ 2–10`; GBn2 polarisation in backbone torsions `βc = 12–53`, growing with length, dense second order, no sharp site; near the pair-additive class in RMS (`0.2–0.9 k_BT`) not in sup norm (`2–16 k_BT`); Jensen gap 2–3 nats against a class bound of 71–178 | **[M]** pilot, exact on finite grids (alanine, ≤ 6 and ≤ 9 residues, rigid geometry); two numbers re-computed by the coordinator; SCI-RES-0002 |
| S18 | **certified kinetics:** barrier lower bounds are cuts certified by the min-kernel on wall boxes; escape-rate upper bounds are the same cuts with partition functions; exact robust interval of a barrier height over an envelope class; a trap bound for every stationary local dynamics | cores **[V]** (32 theorems, re-compiled by the coordinator); exactness and covering statements **[P]**; SCI-MSG-0005 |
| S19 | no transfer matrix for barriers: the barrier threshold on a nearest-neighbour chain is PSPACE-complete (Wrochna's theorem, read as a barrier statement); a linear multiplier on a counting cut never beats the trivial bound | **[K]** + one-line reduction; **[P]** |
| S20 | review of theory report §11.22: no false theorem; proved bracket `[116, 3 627]`; `vol 𝒦 ≥ 1.56` | SCI-REV-0002 |
| S21 | review of theory report §11.24: the two-round lower bound is correct; Theorem 11.84(ii) false as stated (cost bounded on the good event only), repaired by a stopping rule; the lower bound holds for expected cost at the flat-histogram instance | SCI-REV-0003; the strengthening **[V]** in abstract form (four theorems, re-compiled by the coordinator) |
| S22 | heteropolymer landscapes: plain Monte Carlo from the product of the Shannon centres attains the capacity `a` at every bounded accuracy for every `n` (Proposition A1.2) | **[P]**; items 1–3 enumerated on 36 instances and re-derived by the coordinator; SCI-RES-0003 |
| S23 | the `e^{u/2}` rule: the alphabet size maximising the cutoff rate of the `k`-ary symmetric channel at likelihood ratio `e^u` is `k = e^{u/2} + 1`; reflection identity at `e^u = k(k−1)` | **[P]**, re-derived by the coordinator; not found in print in two searches |
| S24 | the exponential price is the geometry of the first-order class (information combines by a minimum), not the worst-case quantifier: over a kernel ball with a Walsh spectrum on orders `≤ m` about `n^m` evaluations certify `min` and `ln Z`; two-sided design bound; exponent `h(α)` for orders up to `αn` | **[P]**, tested numerically; ingredients **[K]**; SCI-MSG-0007 |
| S25 | no free hedging: an algorithm correct on a first-order class pays its instance-wise price on every subclass; the benign assumption cannot be verified from polynomially many evaluations | corollary of the theory division's **[V]** instance-wise bounds |
| S26 | LP-funnel slope `τ_LP ≤ τ`: a polynomial-size, kernel-checkable proof of sharpness for interacting known parts exists iff the envelope is below `τ_LP`; equality on trees and ferromagnets | **[P]**; 1 280 instances |
| S29 | review of theory report §11.25: sound; the headline covers two of three exponents; Theorem 11.90(a) needed a step at negative accuracies (supplied); Lemma 11.89 has a four-line proof and a stronger pointwise form; for any alphabet and site law with Hamming envelope `u`: `h ≤ u²/32` | SCI-REV-0001; the new statements **[P]**, the reviewer's |
| S30 | review of theory report §11.26: Theorem 11.99 proved; 11.101(a) proved; 11.101(b) proved with two gaps in the written proof, closed | SCI-REV-0005 |
| S28 | robust range of an observable free-energy difference: for binary sites, a submodular known part and monotone macrostates the Gibbs measure over the whole envelope class is sandwiched in stochastic order between two uniform fields; extremal residuals additive; common uncertainty cancels exactly | **[V]** since checkpoint 29 (L2: `cube_sandwich_mean`, `cube_ratio_range_eq_Icc`; for any lower set against any upper set; needs `β ≥ 0`, no sign condition on the constants); **[P]** before (Holley's inequality **[K]**); 900 exact linear programmes, two controls; SCI-MSG-0009, -0014 |
| S38 | **local data with a field (workstream F):** a free exact one-body marginal oracle changes neither the adaptive nor the non-adaptive class exponent on the `p`-biased cube, for every `n` and every accuracy (compensation lemma: add a multiple of an extreme additive instance to both members of a pair; the hard instance is a two-component mixture); at an additive instance the oracle strictly helps for `p ≠ ½`, exponent bracketed in `[V, U]` (e.g. `0.0154 ≤ · ≤ 0.0163` against `0.0268`); two-body data: exact construction at `n = 13`; all marginals at tolerance `τ`: polynomial loss.  Theory's Proposition 11.109: (a)–(d) agree, (f) proved, (e) direction proved and two numbers corrected | Theorems A, B, lemmas, tilt inequality **[P]** — re-derived by the coordinator; exact rational enumeration re-run; own check; the rest of the report **[P]/[N]** by the workstream only; nothing machine-checked; SCI-RES-0006 |
| S37 | **second formalisation wave (L2):** Theorem A11 and Corollary A11.1 with attainment and "fills exactly", on any finite distributive lattice; Theorem A13; the referee's R6.1, R6.2 (abstract, binary cube, cosets), R5(2); Proposition A1.2 items 1–3 after two corrections (the envelope must vanish on the diagonal — the triangle inequality is not used; "vertices of the Lipschitz polytope" → of the class normalised at a base point) | **[V]**: 178 theorems, standard axioms, no `sorry`; re-compiled by the coordinator; not machine-checked: R6.3 and the assembly of Theorem R6, A1.2 items 4–5, A11.2 (formula), A14–A16; SCI-MSG-0014 |
| S36 | **isoperimetry with an energy constraint (Lemma A16.5)**: among members of the cube class that vanish outside `|B(n,R)|` points and have mean energy `≥ U₀`, the plateau on a ball has the largest partition function (convex duality in the weights + Harper).  **Theorem A16.6:** with the datum the cost at the visible basin is `Θ(2ⁿ/|B(n,R(ε))|)` — the plateau twin is the optimal obstruction and uniform sampling with the datum's bracket the optimal algorithm (no hint); the datum lowers the cost there at every extensive accuracy; among instances constant outside a small set the threshold basin is the hardest.  Conjecture A16.4 is thereby reduced to instances that are not flat outside a small set | **[P]**, author only; brute force on all supports of `Q_4` (661 806 cases with `Q_5`, `Q_6` samples), random members, exact sums at `n ≤ 2000`; SCI-MSG-0013 |
| S35 | **theory report §11.28 (robust range of a ratio of macrostate weights) reviewed and replicated**: Theorems 11.105–11.107 re-derived; 11.105 and 11.106 replicated with own code; Lean file compiled here; a closed pair need not be optimal; prior art — the separable case is the density-ratio class | review **[P]** by one reader; replication **[N]**, exact linear programmes; SCI-RES-0005 |
| S34 | **a mean-energy datum at extensive accuracy** (addendum A16): (a) entropy bracket — for every member of the cube class `n·h(σ_u) ≤ S(μ_g) ≤ n ln 2`, so the datum alone gives `ln Z` within `n·KL(σ_u‖½)/2`; (b) for accuracies between `KL(σ_u‖½)` and `ln cosh(u/2) = KL(½‖σ_u)` per site the datum removes an exponential cost (exponent `0.067` at `u = 4`, `1.7·10⁻⁴` at `u = 1`); (c) below, a "plateau twin" (as deep, exponentially wider) gives `θ_U(ε₁) ≥ ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))`, which supersedes `h − ε₁`; (d) conjecture: that is the exponent.  **The oracle invariance of S33(c) is a bounded-accuracy statement** | (a), (b), (c) **[P]**, author only; exact sums with overlapping supports to `n = 2000`, 400 random members by enumeration; (d) **[C]**; SCI-MSG-0012 |
| S32 | model-free identified sets from a Debye scattering curve at `K` Shannon channels with a relative tolerance (11–15 beads): `R_g²` is fixed and little else; precision matters more than range; a compact-state population is bounded above only; under one instrument the unidentified part of the gauche fraction grows with the chain (three sizes) | **[N]**, exact linear programmes; addendum A15; SCI-MSG-0011 |
| S33 | the oracle-invariance theorem assembled (addendum A12): parts (a)–(d) with the second reading of the hidden-twin proof and the corollary with both oracles written out | **[P]**; cores **[V]**; SCI-MSG-0011 |
| S31 | the sandwich of S28 on ordered multi-state sites: exact for envelopes additive along the order, a valid loose bound otherwise (addendum A13); on a Zimm–Bragg helix–coil chain a per-residue uncertainty of `0.1 k_BT` leaves the helix content of a 50-residue chain near the transition undetermined over more than half its range, and a local log odds uncertain by `2c` times a cooperative length (A14) | the sandwich on ordered alphabets **[V]** since checkpoint 29 (L2: `stepField_sandwich_mean`, `chain_ratio_range_eq_Icc`); "not attained otherwise" and the helix–coil numbers **[N]**; SCI-MSG-0011, -0014 |
| S27 | the lever arm belongs to the first-order format, not to the residual: energies quadratic in positions have chain-length order and growing per-torsion constants but `O(n²)` modes | **[P]**; toy chain |

## Outstanding requests

| id | to | subject | priority | status |
|---|---|---|---|---|
| SCI-REV-0004 (T1–T6) | theory | prior-art corrections for theory report rows G11, G18, G27, Theorem 11.61, citations | high for T1–T3 | **done by theory at `40c5bd7`** (THY-RES-0005 §1) |
| SCI-REV-0004 §6 | engineering | importance-sampling sample sizes for three proposals at the cone, `(p,u) = (0.1, 2)` (minutes on one core) | low | proposed |
| SCI-REQ-0001 | theory | Q1 robust interval of a ratio of macrostate partition functions; Q2 marginal oracle with a field; Q3 upper boundary of the limit shape; Q4 thermodynamic oracle | Q1 high | **Q1 answered for the range by theory (THY-RES-0006; theory report §11.28 — reviewed and replicated by us, SCI-RES-0005), its query complexity open; Q2(a) answered by a criterion and two conjectures (§11.29; with our workstream F for review); Q3(c) answered; Q3(a,b) deferred; Q4 commented.**  On our side: Q1 in one setting (SCI-MSG-0009; A13), **Q2(a) answered by our workstream F (SCI-RES-0006): class exponents unchanged, proved**, Q4 root proved and extensive accuracy bracketed (SCI-MSG-0012, -0013) |
| SCI-REV-0002 (corrective actions 1–6) | theory | headline of §11.22; `liminf` column; volume statement; Lean bookkeeping; wording | high for M1 | proposed |
| SCI-REV-0002 §8 | engineering | witness bridges in larger boxes; exact packing in the hull of proved points; class tables of bridges | medium | proposed |
| SCI-REV-0006 (T-1…T-6) | theory | wording W1–W10; Propositions A2.1, A2.2; exact-semigroup question; constants | high for W1, W2 | proposed |
| SCI-REV-0006 §7 (E-1…E-3) | engineering | native kernel against pseudo-Boolean proof logging; homometry on the diamond lattice; Debye curves | medium | proposed |
| SCI-RES-0002 (P-T1…P-T4) | theory | envelopes with a domain; known features with a quadratic remainder; a certified typical-norm remainder for `ln Z`; droplets with long-range known parts | P-T3 high | proposed |
| SCI-RES-0002 (P-E1…P-E3) | engineering | **the same constants in rotamer variables on a fixed backbone** (decisive for the second-order interface); the pilot's grids as a fourth case of ENG-RES-0003; exact covers of the real instances | P-E1 high | proposed |
| SCI-MSG-0005 (K-T1…K-T4) | theory | formalise the tree cut checker; Z-kernel over polynomial weights; exactness of the robust barrier interval; critical depth | K-T1 medium | proposed |
| SCI-MSG-0005 (K-E1…K-E3) | engineering | effectiveness of tractable cuts against chain length; certified relaxed scans; cut search around found paths | medium | proposed |
| SCI-REV-0003 (corrective actions 1–6) | theory | stopping rule in Theorem 11.84 (M1); wording m1–m9; adopt the expected-cost form | high for M1 | proposed |
| SCI-REV-0003 (R4-E1, R4-E2) | engineering | certified rows of the twins table (interval arithmetic); the two-round algorithm at finite `n` | medium | proposed |
| SCI-RES-0003 (A1-T7…A1-T9) | theory | wording of the dictionary's originality; a sentence of Theorem 11.99; check Proposition A1.2; the reflection identity | normal | proposed |
| SCI-MSG-0007 (X-T1…X-T4) | theory | machine-check the hypercircle band and a sharp–soft soundness statement; two table rows; the Curie–Weiss extremality question; the converse reading of D28 | X-T1 high | proposed |
| SCI-MSG-0007 (X-E1, X-E2) | engineering | cover format against span format on enumerated chain geometry; the slack `κ` of certified envelopes | medium | proposed |
| SCI-MSG-0008 (R3-T1…R3-T3) | theory | check three finite statements of our referee; four affinely independent points of `K^{br}`; ~~the mean-energy oracle at extensive accuracy~~ (R3-T3 partly answered by us and replaced by SCI-MSG-0012 §4); ~~formalise R5(2), R6.1, R6.2~~ (R3-T1: done by our L2, withdrawn in SCI-MSG-0014 §4; the question about `nonadaptive_expected_queries_ge` stands) | normal | proposed |
| SCI-RES-0006 (F-T1…F-T3) | theory | confirm the reading of `ρ_t`, `R^max` and the hinted theorem at negative `e`; a Lean statement of the compensation lemma and Theorem A; an isoperimetric upper bound for sets whose excess mass has a prescribed type (the exact instance-wise exponent with a one-body oracle) | normal | proposed |
| SCI-MSG-0012 (§4), narrowed by SCI-MSG-0013 (§3) | theory | ~~a tail lemma with an energy constraint~~ (proved by us at the flat reference: Lemma A16.5) — remaining: the same for references that are not flat (fibre averages of the nested algorithm), or a proof that with the datum the hardest instance for an adaptive algorithm is flat outside a small set | normal | proposed |
| SCI-MSG-0008 (R3-E1, R3-E2) | engineering | class tables for bridges; joint gauche counts per profile class | medium | proposed |
| SCI-MSG-0011 (S-E1) | engineering | class tables with full pair-distance histograms for 13–24 torsions (scattering identified sets beyond 15 beads) | medium | proposed |
| SCI-REV-0001 (T1–T7) | theory | replacement text for the headline of §11.25; the repair of Theorem 11.90(a); citation for Lemma 11.89; the ceiling; R10's report; the middle slice | high for M1 | proposed |
| SCI-REV-0001 (R1-E1) | engineering | empirical test of Conjecture 11.94(iii) on the middle slice | medium | proposed |
| SCI-REV-0005 (R5-T1…T3) | theory | state the isoperimetric input in the theory report; the uniformity argument; concavity for two letters | normal | proposed |
| SCI-REV-0005 (R5-E1) | engineering | exact tail functions on small three-letter chains | low | proposed |

## Requests received

| id | from | subject | decision | state |
|---|---|---|---|---|
| THY-REQ-0011 A1 | theory | review of theory report §11.26 (Theorems 11.99, 11.101) | accepted | **answered: SCI-REV-0005** |
| THY-REQ-0011 A2 | theory | review of §11.24 (Theorem 11.86) | accepted | **answered: SCI-REV-0003** |
| THY-REQ-0011 B1, B2 | theory | prior art: channel-coding dictionary; "`e^{u/2}` states" | accepted | **answered: SCI-RES-0003** |
| THY-REQ-0011 C1 | theory | applicability of per-site envelopes; what would falsify the relevance of the exponents | accepted | **answered: SCI-RES-0002** (a pilot with measurements) |
| THY-RES-0005 §4.1 | theory | our referee's verdict on `INFERENCE_LIMITS.md` | — | **answered: SCI-RES-0004 §1** (and SCI-MSG-0008) |
| THY-RES-0005 §4.2 | theory | a prior-art pointer for Q1 | — | **answered: SCI-RES-0004 §2** |
| THY-RES-0006 §5.1 | theory | prior art for Theorem 11.105 (range of a ratio over the weight cone; density-ratio classes; transport with gains) | accepted | **answered: SCI-RES-0005 §2** (six searches, summary level; two leads unresolved) |
| THY-RES-0006 §5.2 | theory | review of theory report §§11.28, 11.29 (in particular: only the constraints from `B` to `A` matter; the limit in Theorem 11.108) | accepted | **§11.28 answered: SCI-RES-0005 §1** (re-derived; 11.105, 11.106 replicated); **§11.29 answered: SCI-RES-0006** ((a)–(d) agree; (f) proved; (e) bracketed, two numbers corrected) |
| THY-RES-0006 §5.3 | theory | where our §8 flow certificates and theirs differ | accepted | **answered: SCI-RES-0005 §3** |

## Known limitations of our own work

* One reading of the upstream record by the coordinator; depth per section is recorded in
  `SCIENCE_UPSTREAM_SYNC.md`.
* S1–S13 have been refereed (R3: no false theorem; corrections in SCI-MSG-0008) and their
  short cores machine-checked (L1); S14–S16 and addenda A8–A11 have been read by nobody
  but their author; prior art for S1–S10: SCI-MSG-0002, -0003.
* Our theorems on what data are worth are on the cube with zero known part — the theory
  division's idealisation, chosen so that statements are comparable with theirs.
* S17 is a pilot on one amino acid with a rigid geometry; every constant is a property of
  a finite grid.  S18's numbers come from systems of at most 5 849 states.
* Nothing in this branch has been compared with a measurement.

## Synchronisation log

See `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`.
