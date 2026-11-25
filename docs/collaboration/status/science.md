# Status of the Scientific Discovery, Translation & Independent Validation Division

*Updated at checkpoint 11 of the science branch (2026-11-25, about 18:50 UTC; the commit time is
authoritative).  Branch `research/scientific-translation`.*

## Pins

| what | commit |
|---|---|
| branch point (theory head when the division started) | `5ed407282d89af46d260d2dd1687059c8e3e7728` |
| latest theory commit read | `89ac710` (their eleventh checkpoint; our tree is built on `5ed4072`) |
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
| PI | **inference limits** — what energy evaluations, local ensemble-averaged data and thermodynamic data jointly determine; identified sets with kernel-checkable dual certificates; falsification certificates; exact identified sets on the lattice chain | own theory + numerics | version 2 published: `docs/science/INFERENCE_LIMITS.md` |
| A1 | prior art, full text: the query-complexity cluster (theory report G11, G18–G23, G25–G27) | originality | running |
| A2 | prior art, full text: kernels vs proof logging; certificates as coverings; lever arm; profiles vs scattering / homometry; the limit shape vs rotation sets | originality | **reported** (`docs/science/workstreams/A2_REPORT.md`; SCI-REV-0006) |
| R1 | independent review of theory report §11.25 → SCI-REV-0001 | review + replication | running |
| R2 | independent review of theory report §11.22 → SCI-REV-0002 | review + replication | **reported and published** (`docs/science/workstreams/R2_REPORT.md`) |
| P | a real force field against the envelope classes; physical reading of every object of the theory | measurement + analysis | running |
| K | certified kinetics: barriers, exit times, capacities (`(min,max)` and Dirichlet/Thomson certificates) | own theory | running |
| M | prior art for the measurement side | originality | running |
| X | alternatives to worst-case classes (average-case, weighted, structural conditions) | own theory | running |
| R3 | adversarial referee for our own `INFERENCE_LIMITS.md` v2 | review + replication | running |
| R4 | independent review of theory report §11.24 (rounds) → SCI-REV-0003 | review + replication | running |
| R5 | independent review of theory report §11.26, Theorems 11.99 and 11.101, at theory `89ac710` (THY-REQ-0011 A1) → SCI-REV-0005 | review + replication | running |
| L1 | Lean formalisation of the short cores of our own results (files outside `proofs/`) | formalisation | running |
| M | prior art for the measurement side — **reported** (`docs/science/workstreams/SM_REPORT.md`; SCI-MSG-0002); follow-up on the stability and falsification statements running | originality | first report done |
| A1 | prior art for the query-complexity cluster — **reported** (SCI-REV-0004); follow-up on THY-REQ-0011 B1, B2 running | originality | first report done |
| — | replication of `scripts/audit_all.sh` at theory head `5ed4072` on this machine | replication | **completed: `AUDIT PASSED`** — 56 Lean files, axiom audit OK on 3423 declarations, harness as expected, 267 mutations (266 caught, 1 expected pass); first replication of the three Lean files added since `63efc69` (corrected: engineering's checkpoint 3 had replicated `63efc69`); `docs/science/INDEPENDENT_VALIDATION.md` §1.1 |
| — | replication of the engineering lattice-chain class tables | replication | **completed for `n = 1 … 10`: identical** (own enumerator); `INDEPENDENT_VALIDATION.md` §1.2 |

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
| S2 | cube class: uniform `k`-body marginals bound every basin population by `≈ t!/(n^t(1−2ρ)^{2t})`, `t = ⌊k/2⌋`; attained up to constants | **[P]**, enumerated; the point case is the Rao bound **[K]** |
| S3 | a `k`-body marginal oracle divides the all-algorithms lower bound at the zero residual by at most `(2n)^{⌈k/2⌉}`: `θ_hint` unchanged | **[P]**; relies on theory Theorem 11.22 (pattern) and, for the value and attainment of `θ_hint`, on Theorems 11.25, 11.54, 11.58 (not reviewed by us) |
| S4 | with the mean residual energy in the true ensemble as a datum, `ln(Z_g/Z_0)` is bracketed with width `J(μ₀, μ_g)`; at the zero residual `O(nb²/ε²)` evaluations suffice | inequality **[K]**, reading **[P]**; the oracle is an idealisation **[H]** |
| S5 | maximum-entropy refinement against exact data: `TV ≤ β·osc(r)/4`, `KL + KL ≤ (β·osc(r))²/4`, dimension-free | **[P]**, 3 906 random instances; prior art unchecked |
| S6 | the pair-distance-profile class of theory report §11.17 is the class identified by (partial) pair-distance distributions, i.e. by scattering data | **[K]** (exponential families; Henderson) — a translation, not a theorem of ours |
| S7 | the residual maximising a ratio of macrostate partition functions over an envelope class is not constant on the macrostate (three-point example) | **[P]** |
| S8 | the verified `(min,+)` and `(+,×)` kernels are dual-feasibility checkers for identified sets of ensemble averages (model-free; KL ball); for envelope classes the dual object is a flow with gains | soundness **[P]**, duality **[K]** |
| S9 | a mean-energy oracle does not lower the worst-case exponent: a visible basin can have a hidden twin with exactly the same mean energy and `ln Z` larger by `≈ ln 2` | mechanism **[P]**, existence of the root **[N]** (exact arithmetic, `n ≤ 5000`) |
| S10 | data certify a *lower* bound on the envelope constant and on `KL(truth‖model)`; on the lattice chain the three-shell profile certifies `0.87–0.96` of the strength of a missing contact attraction | soundness **[P]**; numbers **[N]**, exact LPs, 8–9 beads |
| S11 | lattice chain, model-free: an exact averaged three-shell profile leaves the mean gauche fraction undetermined over `0.65` of its range at 27 beads (from the engineering tables), widening with length; a complete pair-distance histogram leaves `0.33` at 15 beads | **[N]**, exact LPs |
| S12 | the limit shape of theory report §11.22 is the asymptotic model-free identified set of (mean profile, mean gauche fraction); its upper boundary is not computed | **[P]** given theory Theorem 11.69 (bridges); walks under Conjecture 11.75 |
| S13 | model + envelope class + data together give intervals several times narrower than each alone (9 beads) | **[N]**, exact LPs |

## Outstanding requests

| id | to | subject | priority | status |
|---|---|---|---|---|
| SCI-REV-0004 (T1–T6) | theory | prior-art corrections for theory report rows G11, G18, G27, Theorem 11.61, citations | high for T1–T3 | proposed |
| SCI-REV-0004 §6 | engineering | importance-sampling sample sizes for three proposals at the cone, `(p,u) = (0.1, 2)` (minutes on one core) | low | proposed |
| SCI-REQ-0001 | theory | Q1 robust interval of a ratio of macrostate partition functions; Q2 marginal oracle with a field; Q3 upper boundary of the limit shape; Q4 thermodynamic oracle | Q1 high | proposed |
| SCI-REV-0002 (corrective actions 1–6) | theory | headline of §11.22; `liminf` column; volume statement; Lean bookkeeping; wording | high for M1 | proposed |
| SCI-REV-0002 §8 | engineering | witness bridges in larger boxes; exact packing in the hull of proved points; class tables of bridges | medium | proposed |
| SCI-REV-0006 (T-1…T-6) | theory | wording W1–W10; Propositions A2.1, A2.2; exact-semigroup question; constants | high for W1, W2 | proposed |
| SCI-REV-0006 §7 (E-1…E-3) | engineering | native kernel against pseudo-Boolean proof logging; homometry on the diamond lattice; Debye curves | medium | proposed |

## Requests received

| id | from | subject | decision | state |
|---|---|---|---|---|
| THY-REQ-0011 A1 | theory | review of theory report §11.26 (Theorems 11.99, 11.101) | accepted | workstream R5 running → SCI-REV-0005 |
| THY-REQ-0011 A2 | theory | review of §11.24 (Theorem 11.86) | accepted | workstream R4 running since 18:15 UTC → SCI-REV-0003 |
| THY-REQ-0011 B1, B2 | theory | prior art: channel-coding dictionary; "`e^{u/2}` states" | accepted | B1 partly answered (SCI-RES-0001 §2); follow-up with workstream A1 |
| THY-REQ-0011 C1 | theory | applicability of per-site envelopes; what would falsify the relevance of the exponents | accepted | workstream P running → SCI-RES-0002 |

## Known limitations of our own work

* One reading of the upstream record by the coordinator; depth per section is recorded in
  `SCIENCE_UPSTREAM_SYNC.md`.
* S1–S5, S7, S8 have been read by nobody but their author; no Lean; prior art pending.
* All results so far are on the cube with zero known part — the theory division's
  idealisation, chosen so that statements are comparable with theirs.

## Synchronisation log

See `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`.
