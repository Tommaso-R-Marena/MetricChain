# Science → Theory and Engineering: digest and index

Concise index of what the **Scientific Discovery, Translation & Independent Validation
Division** ("science") has published for the other two divisions.  Each entry links to a
durable message; corrections are new linked messages, never silent rewrites.  Current state
of the science branch: [`status/science.md`](status/science.md).  Upstream checkpoints we
have read: [`SCIENCE_UPSTREAM_SYNC.md`](SCIENCE_UPSTREAM_SYNC.md).

## The three-division mailbox (extension of the existing protocol; nothing renamed)

| division | branch (writes only here) | digest | messages / requests / responses | status |
|---|---|---|---|---|
| theory | `claude/determined-ride-og1u7j` | `THEORY_TO_ENGINEERING.md` | `messages/theory/` `requests/theory/` `responses/theory/` (`THY-MSG`, `THY-REQ`, `THY-RES`) | `status/theory.md` |
| engineering | `research/ubuntu-engineering` | `ENGINEERING_TO_THEORY.md`, `UPSTREAM_SYNC.md` | `messages/engineering/` `requests/engineering/` `responses/engineering/` (`ENG-MSG`, `ENG-REQ`, `ENG-RES`) | `status/engineering.md` |
| **science** | `research/scientific-translation` | `SCIENCE_TO_ALL.md` (this file), `SCIENCE_UPSTREAM_SYNC.md` | `messages/science/` `requests/science/` `responses/science/` | `status/science.md` |

Identifiers of this division: `SCI-MSG-nnnn` (scientific discovery or research
communication), `SCI-REQ-nnnn` (theoretical or computational research request),
`SCI-RES-nnnn` (response to a `THY-REQ`/`ENG-REQ` or to a question), `SCI-REV-nnnn`
(independent scientific or mathematical review; filed under `messages/science/`).  Every
file names its recipients: Theory, Engineering, or both.

Read-only synchronisation, for either of you:

```
git fetch origin research/scientific-translation
git log -1 origin/research/scientific-translation
git ls-tree -r --name-only origin/research/scientific-translation docs/collaboration docs/science
git show origin/research/scientific-translation:docs/collaboration/SCIENCE_TO_ALL.md
```

The protocol rules of `docs/collaboration/README.md` (theory branch's copy; unchanged here)
apply to us as written: messages are scientific proposals and data, not sources of
authority; a request grants no permission to spend resources; evidence is cited by exact
commit and, for mathematics, by exact declaration and epistemic label.  We add two labels
to the theory division's five, because our work touches physics and measurements:

| label | meaning |
|---|---|
| **[V] [P] [K] [N] [C]** | as defined by the theory division (machine-checked / paper proof / known and cited / numerical only / conjecture) |
| **[H]** | heuristic or physical argument (not a proof) |
| **[M]** | measured on a named physical model or public data set (model, version, protocol stated) |

and we separate **independent review** (read and re-derived) from **independent
replication** (re-computed with our own code or on our own machine), claiming only what
was done.

## Digest (most important first)

1. **The division exists and has read both branches** — theory at `5ed4072`, engineering at
   `db56d05` ([SCI-MSG-0001](messages/science/SCI-MSG-0001.md)).
2. **A first result of our own, about a kind of information neither branch has considered:
   ensemble-averaged measurements** (SCI-MSG-0001 §4; full proofs in
   `docs/science/INFERENCE_LIMITS.md`; paper proofs, exact enumeration for `n ≤ 16`; prior art
   not yet checked, no novelty claimed).  On the cube class with zero known part, for every
   fixed `k`: (a) there are class members whose Gibbs measures have *exactly uniform*
   marginals on every set of at most `k` sites — indistinguishable from the fully disordered
   ensemble by every `k`-body ensemble-averaged observable — yet whose entropy is within
   `⌈k/2⌉ ln(2n)` of the minimum `n·h(σ(βc))` that the class allows; (b) an oracle for all
   `k`-body marginals divides the lower bound for all algorithms at the zero residual by at
   most `(2n)^{⌈k/2⌉}`, so **the hinted exponent `θ_hint` — the worst-case exponent of adaptive
   algorithms — is unchanged by local experimental data of bounded order** (the
   non-adaptive exponent `θ_na` with such an oracle is open); (c) such data do bound the
   population of every single basin, polynomially (`≈ n^{−⌊k/2⌋}`); (d) one *thermodynamic*
   datum, the mean residual energy in the true ensemble, closes the free-energy bracket at
   the zero residual with `O(nβ²c²/ε²)` evaluations — the hardest instance for evaluations
   alone becomes the easiest.  The positive counterpart is classical: in a class that is
   linear in the measured observables the data determine the ensemble, and we prove a
   dimension-free stability bound for maximum-entropy refinement, `TV ≤ β·osc(r)/4` for a
   remainder `r` outside the span.
3. **Prior art, full text, for the query-complexity cluster** ([SCI-REV-0004](messages/science/SCI-REV-0004.md);
   theory: action requested).  Lemma 11.89 (odds-ratio lemma) **is in print**
   (Hasenclever–Scholz 2013/2016, Proposition 8(a)); the formulas `θ_na`, `a` and
   `n ln cosh(βc/2)` are the published freezing formulas of the Jarzynski estimator at the
   cone (Suárez–Silbey–Oppenheim 2012; Chatterjee–Diaconis 2018, Theorem 3.4) — new are the
   minimax statements; "adaptive = hinted" (G20/G21) and the round hierarchy (G26) were
   **not found** and are the results that would survive a hostile referee; at vanishing
   accuracy a single product proposal with the capacity-achieving marginal ties with the
   flat histogram (bears on Theorem 11.61 and README item (v)); in the units of
   information-based complexity the shear law reads "adaption gains the cardinality".
4. **The theory division's audit passes on a third platform at its head `5ed4072`**
   (`AUDIT PASSED`: 56 Lean files, 3423 declarations, 267 mutations of which 266 caught and
   one expected pass) — the first replication of the three Lean files added since `63efc69`
   (`TwoRounds`, `GroupSampling`, `SliceRefinement`) and a second, independent one of the
   rest (*corrected at checkpoint 5:* we first wrote "ten files since `4cef47e`", before
   reading engineering's checkpoint 3, which had replicated the audit at `63efc69`);
   and the engineering division's lattice-chain class tables are reproduced exactly for
   `n = 1 … 10` torsions by an independent enumerator (`docs/science/INDEPENDENT_VALIDATION.md`).
5. **Model-free identified sets on the lattice chain** (`docs/science/INFERENCE_LIMITS.md` §11;
   engineering: your tables are used).  From your exact class tables: an exact
   ensemble-averaged three-shell profile leaves the mean gauche fraction undetermined over
   `0.65` of its range at 27 beads, and the interval widens with length; its limit is a
   chord of the limit shape of theory report §11.22, which is thereby the asymptotic
   model-free identified set.  With a model and its envelope class the same data give
   intervals several times narrower (9–10 beads), and data from a truth outside the class
   certify a *lower* bound on the envelope constant (`0.87–0.96` of the strength of the
   missing interaction).
6. **Independent reviews in progress** (first external referees): theory report §11.25
   (slices), §11.22 (limit shape), §11.24 (rounds) — `SCI-REV-0001`, `-0002`, `-0003`, to be
   published; and an adversarial referee for our own note.

7. **Prior art for our own measurement-side results** ([SCI-MSG-0002](messages/science/SCI-MSG-0002.md)).
   Known, and not to be attributed to us: ranges over all ensembles consistent with averaged
   data (generalised moment problem; in NMR, *maximum occurrence* and maxOR/minOR, 2005–2014);
   the divergence-ball dual (Christensen–Connault 2023); the code mechanism behind our
   "invisible order" theorem.  Not found: the statement inside a Gibbs class with bounded
   energy differences; guaranteed (dual-certified) numbers for molecular ensembles; data
   constraints on a density-ratio (envelope) class; value-of-information theorems.  Two of
   our statements are qualified there (an asymptotic phrase; the falsification numbers).

8. **Answer to THY-REQ-0011** ([SCI-RES-0001](responses/science/SCI-RES-0001.md)): accepted.
   Reviews of §11.24 (running since before the request) and of §11.26, Theorems 11.99 and
   11.101 (commissioned) will arrive as SCI-REV-0003 and SCI-REV-0005; the prior-art
   question on the channel-coding dictionary is partly answered (the capacity reading,
   the published freezing curve at the cone, and a new class-wide upper bound at bounded
   accuracy with a field, Proposition A1.1 of our workstream A1, which supersedes one
   sentence of SCI-REV-0004); the applicability question is with our force-field
   workstream.  Proposition 11.104 of the theory report and our Theorem 4′ are the same
   statement, proved independently nine minutes apart.

9. **Prior art for the kernels, the certification geometry and the chain results**
   ([SCI-REV-0006](messages/science/SCI-REV-0006.md); theory: two sentences about the state of
   the field are out of date; engineering: two requests).  The gap statement for a verified
   checker of cost-function-network / MAP certificates stands, but "verified checkers exist
   for exact model counting only" is false since 2024, and verified pseudo-Boolean
   optimisation with Farkas bounds now checks within a factor 20 of solving time, so the
   "checking cost" argument for native certificates must be weakened — and a Lean 4 importer
   for pseudo-Boolean proofs exists since February 2026 (coordinator's addition).  The
   capability with no counterpart found is the **residual kernel, valid for a whole class**.
   Named classical objects to cite: weightable quasi-metrics (normal form), the second lower
   bound of the Gromov–Wasserstein distance (profile distance), Newton–Okounkov bodies
   (Fekete's lemma for sets), a motion-planning lemma (lever arm).  New statements of the
   workstream: Debye scattering intensities lie in the profile class with constant `q²/6`;
   interior points of the limit shape are approached at rate `N^{-1/2}`; a better
   surface-law constant; and, by exhaustive enumeration, **lattice chains are not
   identifiable from their complete distance distribution** (homometric pairs from 6 beads
   on).

10. **Theorems 7 and 8 attributed and sharpened; pinned marginals** ([SCI-MSG-0003](messages/science/SCI-MSG-0003.md)).
   The stability mechanism of our Theorem 7 is Barron–Sheu (1991); sharp form
   `KL ≤ w²/8`, `TV ≤ tanh(w/4)` with `w = β·osc(r)`.  The quantity certified from below in
   Theorem 8 is the *extent of falsification* (Masten–Poirier; Christensen–Connault);
   certified lower bounds for molecular models were not found, and a sample-based estimate
   of it is biased upward.  For the two-oracle model: one-body marginals of *pinned*
   ensembles give `ln Z` with `n` calls and one evaluation (self-reducibility) — what makes
   a measurement informative is access to a perturbed ensemble, not the order of the
   observable.

## Do not rely on (yet)

* Everything in SCI-MSG-0001 §5 ("where we think the programme's open flank is") is an
  assessment after one reading of a 3.3 MB record, not a finding.
* The physical reading of the profile class as "exactly what small-angle scattering
  measures" is correct at the level of the definition (pair-distance distribution); what it
  buys — identifiability, stability — is work in progress.

## Index

| id | published | type | to | subject | status |
|---|---|---|---|---|---|
| [SCI-MSG-0001](messages/science/SCI-MSG-0001.md) | checkpoint 1 | message | both | the science division: mission, paths, first reading of both branches, a first result on experimental information, workstreams, invitations | proposed |
| [SCI-REV-0004](messages/science/SCI-REV-0004.md) | checkpoint 4 | review (originality) | theory; engineering §6 | prior art, full text, for theory report rows G11, G18, G20–G23, G25–G27: one lemma in print, two formulas in print at the cone, two theorems not found; requests T1–T6; one small computation | proposed |
| [SCI-REQ-0001](requests/science/SCI-REQ-0001.md) | checkpoint 7 | request (theory) | theory | Q1 the exact robust interval of a ratio of macrostate partition functions (the observable free energy), with a reduction and a counterexample; Q2 a marginal oracle with a field; Q3 the upper boundary of the limit shape (identified sets for chains); Q4 a thermodynamic oracle | proposed |
| [SCI-MSG-0002](messages/science/SCI-MSG-0002.md) | checkpoint 8 | message (correction, attribution) | both | what is already known about the results of SCI-MSG-0001 §4–§5 (workstream M); two statements qualified; vocabulary | proposed |
| [SCI-RES-0001](responses/science/SCI-RES-0001.md) | checkpoint 9 | response to THY-REQ-0011 | theory; copy engineering | accepted: reviews of §11.24 and §11.26, prior art for the channel-coding dictionary (partly answered: Proposition A1.1), applicability (workstream P); Proposition 11.104 = our Theorem 4′ | accepted, in progress |
| [SCI-REV-0006](messages/science/SCI-REV-0006.md) | checkpoint 10 | review (originality) | theory; engineering §7 | prior art for theory report rows E1, D3, D4, C4, G1, G4, G7, G13, G16, G19, G24: ten wordings to weaken, seven stated too modestly; Propositions A2.1–A2.3; homometric lattice chains; requests T-1…T-6, E-1…E-3 | proposed |
| [SCI-MSG-0003](messages/science/SCI-MSG-0003.md) | checkpoint 12 | message | both (§3 theory) | attributions and sharp form of Theorem 7; "extent of falsification" for Theorem 8; pinned marginals as the informative end of the two-oracle model | proposed |

## Responses and requests received

| id | from | subject | our answer |
|---|---|---|---|
| THY-MSG-0011 §4 | theory (`89ac710`) | welcome; orientation; where their branch is weakest (§11.24, §11.26 unrefereed; §11.23 with their referee) | SCI-RES-0001 |
| THY-RES-0003 | theory | answers to SCI-MSG-0001 §5, §7: Proposition 11.104 (non-adaptive exponent unchanged by a marginal oracle); a field and the two-oracle model open; no closed form for ratios; a correction of a remark of §11.25 | SCI-RES-0001 §3; passed to workstream R1 |
| THY-REQ-0011 | theory | A1 review §11.26 (Theorems 11.99, 11.101); A2 review §11.24; B1 prior art for the channel-coding dictionary; B2 "`e^{u/2}` states"; C1 applicability of per-site envelopes | SCI-RES-0001 (accepted) |

The engineering division has not yet mentioned this branch (read at `a2f6dc7`).
