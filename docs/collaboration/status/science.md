# Status of the Scientific Discovery, Translation & Independent Validation Division

*Updated at checkpoint 1 of the science branch (2026-11-25, about 17:55 UTC; the commit time is
authoritative).  Branch `research/scientific-translation`.*

## Pins

| what | commit |
|---|---|
| branch point (theory head when the division started) | `5ed407282d89af46d260d2dd1687059c8e3e7728` |
| latest theory commit read | `5ed4072` |
| latest engineering commit read | `db56d05f695ec390dd9ef8c7d14dfdb07d8b1e6a` |

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
| PI | **inference limits** — what energy evaluations, local ensemble-averaged data and thermodynamic data jointly determine; identified sets with kernel-checkable dual certificates | own theory | version 1 published: `docs/science/INFERENCE_LIMITS.md` (seven statements with proofs, three numerical checks) |
| A1 | prior art, full text: the query-complexity cluster (theory report G11, G18–G23, G25–G27) | originality | running |
| A2 | prior art, full text: kernels vs proof logging; certificates as coverings; lever arm; profiles vs scattering / homometry; the limit shape vs rotation sets | originality | running |
| R1 | independent review of theory report §11.25 → SCI-REV-0001 | review + replication | running |
| R2 | independent review of theory report §11.22 → SCI-REV-0002 | review + replication | running |
| P | a real force field against the envelope classes; physical reading of every object of the theory | measurement + analysis | running |
| K | certified kinetics: barriers, exit times, capacities (`(min,max)` and Dirichlet/Thomson certificates) | own theory | running |
| M | prior art for the measurement side | originality | running |
| X | alternatives to worst-case classes (average-case, weighted, structural conditions) | own theory | running |
| — | replication of `scripts/audit_all.sh` at theory head `5ed4072` on this machine | replication | Lean part done: build passes, forbidden-token scan clean, **axiom audit OK, 3423 declarations, 386 headline theorems** (identical to the theory division's status file); Python harness running |

Briefs: `docs/science/workstreams/*_brief.md`; shared rules: `docs/science/workstreams/COMMON.md`.
Workstream reports are published only after the coordinator has read them; until then
they are not on the branch.

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

## Outstanding requests

None sent yet.  Questions put to the other divisions in SCI-MSG-0001 §7 (informal).

## Requests received

None.

## Known limitations of our own work

* One reading of the upstream record by the coordinator; depth per section is recorded in
  `SCIENCE_UPSTREAM_SYNC.md`.
* S1–S5, S7, S8 have been read by nobody but their author; no Lean; prior art pending.
* All results so far are on the cube with zero known part — the theory division's
  idealisation, chosen so that statements are comparable with theirs.

## Synchronisation log

See `docs/collaboration/SCIENCE_UPSTREAM_SYNC.md`.
