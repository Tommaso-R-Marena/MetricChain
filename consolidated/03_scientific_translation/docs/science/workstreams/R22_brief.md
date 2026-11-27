# Workstream R22 (launched 2026-11-26) — review asked for by the Geometry division: second-moment rigidity of conformational ensembles (their Theorems B, B′, G), prior art, and their assumption table

*Brief written by the coordinator.  Read `COMMON.md` first (its commit pins are out of date).  The object is the
branch `research/geometric-inference` at commit `d84a43b` (first checkpoint of the Geometric Inference, Rigidity and
Inverse Problems Division, one of three divisions the research owner added on 2026-11-26); a read-only export is at
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/geo_ro_d84a43b/`
(called `<GEO>`: `docs/geometry/`, `docs/collaboration/{messages,requests}/geometry/`, `experiments/geometry/`,
`proofs/Geometry/`).  If the agent of this workstream is gone, its notes are in `experiments/science/ws_R22/` and its
draft in `R22_REPORT.md`.*

## What was asked, and by whom

`<GEO>/docs/collaboration/requests/geometry/GEOMETRY-REQ-0003.md` — read it first, then
`GEOMETRY-MSG-0002.md` (ten findings) and the report `<GEO>/docs/geometry/ENSEMBLE_RIGIDITY.md` (729 lines; read all
of it).  The setting: a chain of `n` points in `ℝ³` with fixed bond lengths and bond angles (constraint graph `E₀`:
bonds and 1–3 pairs); an ensemble is a probability measure `μ` on conformations; the datum is the matrix of
ensemble-averaged squared distances `M(μ)_ij = ∫|x_i − x_j|² dμ`.  A `K`-state mixture is a framework `z` in `ℝ^{3K}`
(blocks `√w_k·X_k`); `𝒩(z)` is the space of quadrics through the constrained edge vectors of `z`, which always
contains `K − 1` trivial ones; **(CC)**: it contains no others.  They ask:

* **R1 — a line-by-line review of Theorems B, B′ (§4.2) and G (§7.2)**, and name the steps most likely to hide an
  error: (i) Lemma 2.2 (from equal distance matrices to a linear isometry into `L²(ν; ℝ³)` and a matrix field `A(x)`
  defined almost everywhere); (ii) Theorem B′ (⇒), the Tchakaloff step; (iii) Theorem G (b), the compactness
  argument for quadratic growth, in particular that the limit direction is a flex orthogonal to the infinitesimal
  isometries; (iv) Theorem G (d), the bracketed proof that (CC) implies infinitesimal identifiability, and the
  bookkeeping of the transport.
* **A1 — prior art** for Theorem B (universal or dimensional rigidity with a symmetry or block structure under
  another name?), Theorem D (extreme Gram dimension when exact and averaged edges are mixed) and Theorem H
  (identifiability of mixtures from banded moments); their `PRIOR_ART.md` §4 says where they would look.
* **AA1 — an attack on their assumption table** (eight rows, in the request), in the six classes of the research
  owner's directive: essential / proof technique / computational convenience / replaceable by a weaker
  quantitative condition / removal changes the complexity / removal makes the result false.

## What the coordinator has already done — read it, do not repeat it, take it further

`experiments/science/geometry_checks/hinge_pair.py` and `hinge_pair.log` (own code from their definitions; 4 seconds):

1. *Two states that differ in one torsion are never identified.*  If `X(φ)` is the chain with one torsion at `φ`,
   every squared distance is `a + b cos φ + c sin φ`; so the mixture of `X(0)` and `X(θ)` has the `M` of every measure
   on the circle with the same mean of `e^{iφ}` — in particular of the two-state mixtures on the other chords
   through that mean (60 competitors on 15 chains, differences `10⁻¹⁴`; control passes).  Rigorous and elementary.
2. *(CC) fails whenever two states differ in at most three torsions, at every chain length.*  The stacked edge
   vectors of a rigid segment shared by the two states (up to a rotation `Q_j`) lie in the three-dimensional
   subspace `{(√w₁v, √w₂Q_jv)}` of `ℝ⁶`; two such subspaces meet in a line (the axis of `Q_i⁻¹Q_j`); so with `s`
   segments the constraints have rank at most `6s − s(s−1)/2` and `dim 𝒩(z) ≥ 21 − 6s + s(s−1)/2 = 10, 6, 3` for
   `s = 2, 3, 4`.  Numerically the dimension is exactly `10, 6, 3, 1, 1, …` for 1, 2, 3, 4, 5, … differing torsions
   on long chains.
3. *What `M` sees of a distribution of torsion angles:* every squared distance is multilinear in
   `(1, cos φ_k, sin φ_k)` of the torsions between the two atoms, so `M` depends on the distribution only through
   Fourier coefficients with all indices in `{−1, 0, 1}` (checked for two torsions; the map from the nine
   coefficients to `M` has rank 9).

**Take it further (Item 3 below):** for two and three differing torsions (CC) fails — is the mixture nevertheless
identifiable (Theorem B′ decides)?  The coordinator's sketch, to be verified or refuted: by Lemma 2.2 every state of
a competing ensemble keeps each shared segment rigid (if the segment has six edge directions on no conic), so
competitors live on re-hingings of the same segments (and reflections of segments), and identifiability becomes a
truncated trigonometric moment problem on the torus of the differing torsions; for two torsions the moment matrix
indexed by `{1, z₁, z₂, z₁z₂}` is determined by `M`, has rank 2 for the mixture, and its two kernel polynomials
(bilinear) have the two atoms as their only common zeros on the torus — so the mixture would be identifiable
*without* (CC).

## Item 1 — Theorems B and B′, with Lemma 2.2

State each with every implicit hypothesis (`E₀` connected; conformation space compact modulo translations; `z`
spans affinely; reflections count as congruences; the datum includes the constrained pairs).  Re-derive Lemma 2.2:
well-definedness of `T` on a spanning set, measurability of `A`, the null sets (finitely many `i`), `AᵀA − I ∈ 𝒩(z)`.
Theorem B: the step "positive semidefinite, block-scalar, rank at most `d` ⇒ one block" (their Lean core — read
the Lean statement in `<GEO>/proofs/Geometry/EnsembleRigidity.lean` and say whether it is the paper's statement), the
weights from `∫AᵀA dν = I`.  Theorem B′ (⇒): Tchakaloff on a ball and its complement (is `𝒫(z)` compact?  does the
finitely supported measure keep the barycentre exactly?), `Y_j ∈ 𝒞`, "congruent iff `P_j = E_k/w_k`" (needs `z`
spanning).  Corollary 4.2 if time permits.  Each step: holds / holds with a condition to add / gap / false.

## Item 2 — Theorem G

(a) the zero set of `φ` on `𝒞`; (b) `κ > 0`: compactness modulo congruence, the optimal alignment and "orthogonal to
the infinitesimal isometries", the passage to the limit of the constraint equations, `Π^⊥V = 0 ⇒ V = zBᵀ + 𝟙tᵀ`, the
flex condition read on stacked edge vectors, and the algebra that forces `B` to be a skew block — **redo this
algebra in full**; the hypothesis `n − 1 > dK` and "smooth manifold near each `X_k`" — where is each used, and what
happens at a state where the chain is singular (aligned bonds)?  (c) the constant.  (d) the decomposition
`M(ν) − M(μ) = Σ(ν_k − w_k)D(X_k) + ΣL_k(τ̄_k) + R`, the claim **(CC) ⇒ infinitesimal identifiability** (the bracketed
proof), the transport bookkeeping, whether `C_μ` depends on anything not named.  (e) the lower bound.  Then say
plainly what kind of statement (c)–(d) is while `κ` is not computed: by the research owner's directive "a general
theorem with computationally vacuous guarantees should be explicitly identified as such".

## Item 3 — replication and tests with your own code

Write your own code from the definitions before opening theirs.  (a) (CC) for generic pairs and triples at and below
their thresholds (`n = 12` for `K = 2`; `23` for `K = 3`) in exact rational arithmetic for one or two cases, floating
point otherwise.  (b) Theorem G numerically on a pair with `n = 12…14`: `φ(X)/min_k d_P(X, X_k)²` on conformations
sampled near the states and globally with local minimisation — the smallest value found, and the local value (the
smallest eigenvalue of `Π^⊥` on the flex space); (e) by broadening one state.  (c) **States that share rigid
segments** (see above): for two differing torsions on a chain with long segments, search for a competing ensemble
by linear programming over a grid of the two torsions (minimise the mass on the two true states subject to equal
`M`), with the one-torsion case as the control in which the programme must find competitors; then three torsions.
Report the outcome whichever way it goes.  (d) Re-run from a scratch copy (`python3 -I -B`): their
`run_checks.py`, `mutation_checks.py`, `hierarchy_example.py`, and `exact_conic_rank.py` for the smallest arguments
that finish in minutes; compare with what the report quotes.

## Item 4 — the assumption table (AA1) and the reading for data

Classify each of their eight rows yourself and compare.  Points the coordinator wants pressed: (1) "finitely many
states — proof technique?" — their own Corollary 4.2 makes the `D(X_k)` affinely independent, so the number of
states of an identifiable ensemble is bounded by the dimension of the data, and an ensemble with a continuous
part is never identified by finitely many means: is the row then "essential"?  (2) "genericity — a weaker
quantitative condition is available": true as a certificate, but the excluded set contains every pair of states
that differ in at most three torsions (and one differing torsion is unidentifiable outright) — how should the
row read, and what should the headline say for chains whose states share rigid parts?  (3) "exact data —
convenience, replaced by Theorem G": with a constant that is a global infimum nobody has computed.  (4) the
observable: what survives for averages of other functions of the distance (the set of realizable data is still
convex and the face criterion still applies; only the Euclidean framework is lost).  The question of physical
relevance is answered by the coordinator in SCI-RES-0029; add to it only what a source you opened supports.

## Item 5 — prior art (A1)

Generic queries only.  Leads: universal rigidity and dimensional rigidity, super stability, "conic at infinity";
affine flexes; Gram dimension and extreme points of the elliptope with fixed entries; unique representing
measures and neighbourliness of convex hulls of varieties; identifiability of mixtures from second moments
(tensor/moment methods for mixtures of linear subspaces or of Gaussians with structure); reconstruction of a
diploid genome from averaged contact or distance data; ellipsoid fitting.  For each of Theorems B, B′, D, F, G, H:
new as far as you can see / a formulation of something known / a corollary / a rediscovery — with what you
opened.  Note also the Ensemble division's parallel statements (their report is not your object; a one-line
pointer suffices): their Corollary E1.3 (mean squared distances determine nothing — by a random scaling, which
breaks bond lengths) is the unconstrained case of Proposition 3.1 here.

## Rules

Write only in `experiments/science/ws_R22/` and `docs/science/workstreams/R22_REPORT.md`.  No state-changing git;
no subagents; no `lake`; `<GEO>` stays untouched (copy what you run into `ws_R22/rerun_copy/`, which will not be
committed).  **Literature:** web search and fetch for published papers and their definitions only, with generic
queries; put no name, file or text of this project into a query; upload nothing; cite only what you opened and
say "from memory" or "from a search summary" otherwise; never invent a bibliographic detail.  Keep four kinds of
checking apart: **review**, **replication** (own code), **re-run** (their code), **read only**.  A finding is
*critical*, *major* or *minor*; give a replacement text for each.  Report what you did not check, and your own
errors.  Machine: 4 cores and 15 GB shared with five other jobs — `OMP_NUM_THREADS=1`, at most two processes, no
process above 2 GB, no run longer than 20 minutes; before any run of more than five minutes write its cost into
`NOTES.md`.  Keep `NOTES.md` from the first minute.  A log is cited only if its run reached its last line; logs of
stopped or failed runs go into `not_cited/`; fresh names instead of overwriting.  A time written into a file is
read from the clock.  Every check is reported with the violations of its control.  **If a tool declines an action,
do not work around it: keep everything in `NOTES.md` and return the findings as text in your hand-back.  Do not
delete files with wildcards or `rm -r`.**  This is an internal review, not external peer review; say so in the
report.

## The report

(0) Verdict in ten lines: are Theorems B, B′, G proved as stated; the findings by class.  (1) The statements with
their implicit hypotheses.  (2) Findings, each with the line that decides it and a replacement text.  (3) Your
replication and tests, with their controls — including the outcome for states that share rigid segments.
(4) Re-runs.  (5) The assumption table, row by row.  (6) Prior art, with what you opened.  (7) Requests to the
Geometry division that can be sent as they stand.  (8) What you did not check; your own errors; files.
