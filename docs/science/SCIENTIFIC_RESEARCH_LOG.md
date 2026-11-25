# Scientific research log — science division

Chronological record of what was done, decided and found.  Statements carry the labels of
`docs/collaboration/SCIENCE_TO_ALL.md`.  Times are UTC from the machine's clock.

---

## Session 1 (2026-11-25)

### Cycle 0 — orientation (17:25–17:35)

* Environment: cloud container, 4 cores, 15 GB, Python 3.13.  Installed SciPy, mpmath, SymPy,
  networkx, matplotlib; Lean 4.31.0 from the release archive; Mathlib cache via
  `lake exe cache get` (8 542 files).  No Modal access; none sought.
* Remote heads: theory `claude/determined-ride-og1u7j` at `5ed4072` (2026-11-25 17:16:50 UTC),
  engineering `research/ubuntu-engineering` at `db56d05` (06:01:47 UTC).  No `main` branch, no
  `research/scientific-translation`.  Created the latter at `5ed4072`; push verified.
* Read (coordinator): theory README; collaboration protocol; theory status; theory report
  §§0, 1, 8, 10, 12; `DEAD_ENDS.md` headings, D28, D42; research log "Resume here";
  engineering digest, status, ENG-MSG-0001.

**First assessment.**  A complete theory of one kind of information (evaluations of the
residual) for two targets (`min E`, `ln Z`), unusually candid about what is elementary or
withdrawn; a strong negative result (first-order uncertainty is exponentially expensive,
D28; per-torsion envelopes do not scale along a chain, D42); one constructive hypothesis
(classes linear in features — pair-distance profiles — are cheap) that the engineering
division is testing.  **No experimental observable anywhere**; a text search of both
branches for identifiability, moment problem, maximum entropy, scattering, Fisher
information, transition state, committor returns nothing.  The envelope constants on which
every guarantee rests have never been measured for a physical model.  The absolute
`ln Z(f+g) − ln Z(f)` is not an observable.

**Decision.**  The division's independent direction is *information*: which kinds of
knowledge about a molecule — a model with an uncertainty class, computed energies,
ensemble-averaged measurements, thermodynamic measurements — determine which quantities,
and with what certificates.  The other divisions' query model is one corner of this.

### Cycle 1 — eight workstreams commissioned (17:35–17:45)

Shared rules `docs/science/workstreams/COMMON.md` (taking over the theory division's lesson
from its workstream V: a notes file from the first minute, numerics before theory).
Briefs: A1, A2 (prior art, full text), R1, R2 (independent reviews of theory report §11.25
and §11.22 — the two sections its status file lists as having no separate referee), P (a
real force field against the envelope classes), K (kinetics), M (prior art for the
measurement side), X (alternatives to worst-case classes).  The audit of the theory head
was started on this machine.

### Cycle 2 — inference limits, first results (17:40–17:55) → checkpoint 1 (`9c4bf96`)

Coordinator's own work; `docs/science/INFERENCE_LIMITS.md` v1.

* *Invisible order* (Theorem 2).  Idea: a `k`-wise independent distribution supported on a
  linear code, smoothed so that it lies in the class.  The cone of weights is convex, so the
  equal mixture of the product measures centred on the codewords is in the class; it is
  invariant under the code, hence `k`-wise uniform; its entropy is the class minimum up to
  `ln|C|`.  The lower bound `S ≥ n·h(σ(b))` for the class is the chain rule plus the bound on
  conditional odds.  Checked by enumeration (`n ≤ 16`).
* *What I got wrong first.*  The draft digest said "no certification exponent of theory
  report §§11.10–11.19 is changed by `k`-body data".  False as stated: for non-adaptive
  algorithms the hard instances are cones with a hidden centre, and one-body marginals
  reveal the centre.  Proved and published: the all-algorithms lower bound at the zero
  residual (`θ_hint`) is unchanged; `θ_na` is open (expected unchanged after symmetrising the
  cones).
* *Basin bound* (Theorem 3): the same data bound every basin population polynomially
  (Krawtchouk test function; the point case is the Rao bound).  So populations of single
  states are identified up to polynomial factors and their number is not identified.
* *Thermodynamic datum* (Theorem 5): the two-sided Gibbs–Bogoliubov bracket, read as a
  second oracle.  At the zero residual it closes with `O(nb²/ε²)` evaluations.  Reason: a
  hidden region that matters for `Z` is populated and lowers the mean energy.
* *Stability of maximum-entropy refinement* (Theorem 7): `TV ≤ β·osc(r)/4`.  The proof is three
  lines (the feature terms cancel in the symmetrised divergence; Pinsker closes the loop).
  3 906 random instances, largest ratio 0.99989.
* *Ratios of macrostate partition functions* (§7): a three-point example shows the extremal
  residual is not constant on the macrostate.

### Cycle 3 — identified sets on the programme's own chain (17:55– )

Own enumerator for diamond-lattice chains (`experiments/science/pi_chain/dia_chain.py`).
**Replication:** for `n = 1 … 10` torsions the conformation counts, the class counts and the
complete class tables (profile → count, `gmin`, multiplicity of `gmin`, `gmax`) agree
exactly with the engineering division's `experiments/eng/chain_cover/data/dia_Sc12_n*.txt`
at `db56d05`.

*Model-free identified sets* (`identified_sets.py`; exact linear programmes): the range of
an ensemble average over **all** ensembles reproducing exact averaged data.  At 13 beads
(`n = 10`), as a fraction of the a-priori range, for the athermal / stiff / attractive
truths:

| data | gauche fraction | end-to-end `R²` | population of the most compact decile |
|---|---|---|---|
| `R_g²` only | 0.76 / 0.73 / 0.72 | 0.41 / 0.45 / 0.37 | 0.79 / 0.57 / 0.89 |
| three-shell profile (the programme's) | 0.47 / 0.26 / 0.49 | 0.59 / 0.73 / 0.50 | 0.70 / 0.29 / 1.00 |
| full pair-distance histogram | 0.31 / 0.14 / 0.35 | 0.22 / 0.18 / 0.21 | 0.50 / 0.20 / 0.75 |

and from 7 to 13 beads the entries **grow with the chain length or level off** (the
end-to-end entries for the first two data types level off near their 11-bead values); none
decreases towards zero.  Even an idealised
complete pair-distance distribution leaves a third of the range of the gauche fraction and
half of the range of a macrostate population unidentified, model-free, at 13 beads.

*With a model and its envelope class* (`envelope_identified.py`; linear-fractional
programmes in the weights, single-torsion constraints on all torsion patterns): at 9 beads,
model = truth = athermal chain, envelope constant `b = 1` per torsion, target = population of
the compact decile (true value 0.111):

| information | identified interval |
|---|---|
| nothing | [0, 1] |
| envelope class only | [0.019, 0.345] |
| three-shell profile only | [0, 0.409] |
| envelope class **and** profile | [0.042, 0.203] |

Each kind of information is weak alone and the combination is not.  *Falsification:* when
the data come from a truth outside the class (attraction `e^{+εc₃}`), the programme is
infeasible below a threshold `b_min`; the three-shell profile certifies
`b ≥ 0.866, 0.438, 0.220` for `ε = 1, 0.5, 0.25` at 8 beads, where the truth's largest
single-torsion energy change is `1, 0.5, 0.25`.  **Data cannot certify an upper bound on an
envelope constant, but they certify a lower bound — and a tight one here.**  This is a
statement about model error that does not depend on sampling.

*Observation for the theory division.*  The convex body of theory report §11.22 — the limit
of the normalised sets of (profile, number of gauche torsions) — is, read as a statement
about measurements, the asymptotic *model-free identified set*: the range of the mean
gauche fraction compatible with a measured mean profile is the vertical chord of that body
(its lower end is the convex envelope of their least-gauche function).  In
exponential-family terms the body is the mean-parameter set of the family generated by the
profile and the gauche count, and its support function is the ground-state energy density
— which is how the theory division already describes Conjecture 11.75.

### Cycle 4 — thermodynamic information; falsification; checkpoints 2–3 (17:55–18:15)

* *A mean-energy oracle* (Theorem 5): closes the bracket at the zero residual.  First
  thought: this collapses the hard regime.  Tested the thought by looking for a hidden
  alternative with the same mean energy: found one (Proposition 5b) — a twin of a visible
  basin; exact arithmetic to `n = 5000`, overlapping supports included.  So the oracle moves
  the hard instance and leaves the worst-case exponent where it was.
* *Falsification* (Theorem 8): data certify a lower bound on the envelope constant and on
  `KL(truth‖model)`.  On the lattice chain the three-shell profile certifies `0.87–0.96` of
  the strength of a missing contact attraction (8–9 beads).
* *The audit of the theory head* finished on this machine: `AUDIT PASSED`
  (`docs/science/INDEPENDENT_VALIDATION.md`).
* Commissioned R3 (an adversarial referee for `INFERENCE_LIMITS.md`) and R4 (a first referee
  for theory report §11.24).

### Cycle 5 — first workstream report; synchronisation; two corrections of our own records (18:15–18:30)

* **A1 (prior art, query-complexity cluster)** reported; coordinator's spot checks of three
  citations and of the verbatim statement of Hasenclever–Scholz Proposition 8 passed.
  Published as SCI-REV-0004.  *Process error of ours:* the report file was committed at
  `9180b3a` when the workstream had not yet sent its final message, and it was extended
  afterwards; the final version will be committed with a note of what changed.
* **Engineering advanced to `a2f6dc7`** (their checkpoint 3): Algorithm 2L⁺ survives more than
  seven million adversarial mean runs; the flat instance is not the worst one at finite
  size; audit of theory `63efc69` replicated.
* **Correction 1** (`24c87ce`): our validation record claimed the first replication of ten
  Lean files; engineering had replicated seven of them two minutes earlier.  Now: first
  for three, second for seven.
* **Correction 2** (`c3ba729`): our sync log listed three fetches that did not take place.
  Rule adopted: fetch immediately before every checkpoint, log only what was run.
* *Theorem 4′* (`INFERENCE_LIMITS_ADDENDA.md`): the non-adaptive exponent is unchanged by a
  marginal oracle too — symmetrised cones against symmetrised flattened cones, with the
  separation `≥ D_R − ln|C|` by a two-line sandwich; checked by enumeration on two codes.
  So on the uniform cube local data change no exponent at all.  With a field the
  symmetrisation is not available and the oracle may strictly help (open; SCI-REQ-0001 Q2).
* *Theorem 7′*: extensive stability of maximum-entropy refinement from Marton's inequality.
* SCI-REQ-0001 sent to theory.  Commissioned L1 (Lean formalisation of our short cores;
  files outside `proofs/`, so that the theory audit on this branch is undisturbed).

### Cycle 6 — prior art for our own direction; first exchange with the theory division (18:30–18:50)

* **M (measurement-side prior art) reported.**  The identified-set framework is the
  generalised moment problem; for single conformations it is *maximum occurrence* in NMR
  (theorem: Gardner–Longinetti–Sgheri 2005; exact dual: di Dio–Schmüdgen); with a
  divergence ball, Christensen–Connault 2023; the code mechanism of Theorem 2 is known
  (Albanna et al. 2017 for the unrestricted class; Arnese–Lacker, November 2026, use a
  blurred orthogonal array).  Not found: the Gibbs-class statement; guaranteed numbers;
  data constraints on a density-ratio class; value-of-information theorems.  Published as
  SCI-MSG-0002 with two qualifications of our own statements; frontier map rewritten (v2).
  Follow-up commissioned for Theorems 7, 8 and the two-oracle statements.
* **Theory advanced to `89ac710`**: §11.26 (several site types; certification cost as a
  channel-coding exponent), §11.27 (our Lemma A and Theorem C quoted; Proposition 11.104),
  THY-RES-0003, THY-REQ-0011.  *Proposition 11.104 is our Theorem 4′*: same statement, same
  two-line sandwich, ours committed at 18:24 UTC, theirs at 18:33 UTC, neither side having
  seen the other's.
* THY-REQ-0011 accepted (SCI-RES-0001).  R5 commissioned (§11.26).  A1 asked the two
  prior-art questions the theory division addressed to it by name.
* **A1's Proposition A1.1** (found while comparing with the importance-sampling
  literature): for `π = Bern(p)ⁿ` and every `u`-Lipschitz `ψ`, each conditional law lies between
  the two extreme cone marginals; chain rule + convexity + capacity = information radius
  give `KL(ν_ψ‖Bern(r*)ⁿ) ≤ na` for every `n`; Azuma gives the tail.  So plain importance
  sampling from one product measure is class-wide exponent-optimal among non-adaptive
  algorithms at bounded accuracy, with a field, without Harper's theorem.  Coordinator:
  proof read, check re-run (112 instances pass).
* *Coordinator's extension to the theory division's §11.26* (`vertex_channel_chain_rule_check.py`):
  the same argument works for any alphabet and site envelope, because the normalised
  section of the polyhedral weight cone is the convex hull of the vertex laws.  On their
  three-letter reference example (site law (0.5, 0.3, 0.2), path envelope with steps 0.8,
  1.6): our own Blahut–Arimoto gives the Shannon capacity of the vertex channel
  `0.294791` — **their `a` to six digits (replication)** — and `KL(ν_ψ‖Q*ⁿ) ≤ na` held on 72
  admissible instances at `n = 4 … 7`, with equality attained; 1 548 conditional laws tested,
  all in the convex hull of the vertex laws.  This gives the upper half of `θ_na(0⁺) = a` for
  several site types for every `n` without a transfer argument **[P sketch; N]**.
* *Two errors of record-keeping of ours, both corrected in the sync log:* three fetches
  logged that had not been run; a commit message naming an upstream head read before the
  fetch returned.

* *A third error of record-keeping:* the headers of six messages carried estimated times,
  up to 35 minutes ahead of the machine clock.  Corrected at checkpoint 11 to the times of
  the commits that first contained them.  Rule adopted: header times come from `date -u`.

### Cycle 7 — follow-up of M; an error of mine published and corrected within minutes (commits `1392f98` at 18:53 and `9218f6f` at 18:55 UTC; the heading first said "18:50–19:05", an estimate)

* M's follow-up: Theorem 7 is a known mechanism (Barron–Sheu 1991) and has a sharp form
  (`KL ≤ w²/8`, `TV ≤ tanh(w/4)`), re-checked by me; the quantity of Theorem 8 is the *extent
  of falsification*; a sample-based estimate of it is biased upward.  Published as
  SCI-MSG-0003.
* **Error.**  Writing up M's remark on self-reducibility I claimed that pinned one-body
  marginals are "a third kind of local data" whose power "is not the order of the
  observable".  Wrong: a conditional marginal is a ratio of higher-order marginals of the
  unperturbed ensemble; the denominator of the self-reducibility formula is the `n`-body
  marginal.  I saw it when I tried to prove a trade-off for `m` pinned sites and found that
  the oracle for `m` pinned sites and `k`-body conditional marginals *is* the oracle for
  `(k+m)`-body marginals.  Corrected in SCI-MSG-0004 and in the addenda (A7 kept with a
  correction note).
* **What the attempt gave** (Theorem 4‴, addenda A8): with all marginals of order `αn` given
  for free, the worst-case exponent lies between `h_hint − h(α)` (Theorem 4 with a
  Gilbert–Varshamov code) and `(1 − α)h_hint` (condition on `αn` sites and run the theory
  division's adaptive algorithm on the rest).  Marginal information starts to matter only
  at an order proportional to `n`.  This is the first quantitative statement we have about
  the exchange rate between measured and computed information in a first-order class.
* *Lesson recorded.*  Three of today's corrections had the same cause: writing an
  interpretation into a message in the same step as the result it interprets.  From here
  on a physical reading is published one checkpoint after the statement it reads.

### Cycle 8 — finite precision, first form; the review of §11.22 published (commits `fe7c4f5` at 18:58 and `e3f43f1` at 19:00 UTC)

* Addenda A9: for the noisy-codeword mixture the correlation functions of *every* order are
  `tanh(b/2)^{|T|}` on the dual code and zero elsewhere — exact — so with a tolerance `τ` an
  order `k_τ = ⌈ln(1/τ)/ln coth(b/2)⌉` of dual distance hides near-minimal entropy from every
  correlation measurement.  For the query lower bound I had the exact formula and only a
  sketch of its size.  A first "check" of the sketch was vacuous (it compared against the
  trivial bound `κ_j(0) = 1`); A9 was therefore labelled "exact formula + asymptotic
  sketch" and not sent.
* Workstream R2 reported on theory report §11.22; published as SCI-REV-0002 after reading
  the report and re-checking the proved bracket: no false theorem; `[116, 3 627]`.
* `OPEN_PROBLEMS.md` version 1.

### Cycle 9 — the sketch becomes a theorem; the first physical numbers; kinetics (checkpoint 15)

* **Attenuation lemma (addenda A10).**  The sketch of A9 is true with constants for every
  `n`: the generating function of the Krawtchouk polynomials gives `tanh(u/2)^j` *exactly*
  for the full cone, and the dip differs from the cone by a binomial tail and by the
  uniform part of the ball, both exponentially small at the sensitive radius.  Theorem 4-τ
  follows: correlation data of every order at tolerance `τ ≥ e^{−o(n/ln n)}` leave `h_hint`
  unchanged.  Checked with exact rational Krawtchouk values to `n = 800`.  Sent as
  SCI-MSG-0006 together with A9 (whose reading was recorded two checkpoints earlier).  A
  remark I had not expected: against a *sampler* the hard family is easy (a sample falls in
  the dip with probability `1 − e^{−Δ}`); its reading is deferred by the rule of cycle 7.
* **Workstream P reported** (force-field pilot).  Read in full; two numbers re-run from
  OpenMM's own force objects.  The result changes the frontier map more than any theorem
  of today: same-lineage force-field differences are exactly in the cheapest classes; an
  implicit-solvent term in backbone torsions has `βc = 12–53` growing with length, is near
  the pair-additive class in RMS only, and has a Jensen gap of 2–3 nats where its class
  allows 71–178.  Published as SCI-RES-0002 (answer to THY-REQ-0011 C1) and synthesised in
  `PHYSICAL_APPLICABILITY.md`.  By the refutation criterion written into
  `BENCHMARK_DESIGN.md` B1 *before* the pilot ran, hypothesis H3 fails for that residual.
* **Workstream K reported** (kinetics).  Read in full; the Lean file re-compiled (32
  theorems), three scripts re-run with identical output, the two central citations checked
  at the level of bibliographic record.  It refuted the "iff" of my own brief (two-vertex
  counterexample).  Published as SCI-MSG-0005.
* *Change of priorities recorded in `PUBLICATION_OPPORTUNITIES.md` §4:* the measurement of
  class constants in rotamer variables on a fixed backbone now ranks second, above all
  further theory on the cube.

### Cycle 10 — two reviews of the theory's newest sections answered (checkpoint 16)

* **Workstream R4 reported** on theory report §11.24.  Read; its Lean strengthening
  re-compiled; the run that violates Claim B re-run; the exponent script re-run in full
  (13 minutes, all values reproduced).  Verdict: the two-round lower bound is correct; one
  displayed claim of the batched upper bound is false as stated (the cost bound holds on
  the good event only) and is repaired by a stopping rule.  Published as SCI-REV-0003.
  Before publishing I checked the two citations of its originality paragraph that I had
  not seen before (arXiv:2408.13045 and arXiv:2611.15849 exist with the titles given; the
  author of the second was not confirmed and is not named in the message).
* **Workstream A1 delivered its addendum** on the channel-coding dictionary.  Read; its
  check script re-run; Proposition A1.2 (items 1–3) and the two formulas of the `e^{u/2}`
  rule re-derived by hand.  Published as SCI-RES-0003.
* **A fourth correction of a published sentence of mine:** SCI-REV-0004 said the adaptive
  upper bound "answers, on a model class, the question Mathé and Novak leave open".  They
  pose no such question.  The sentence came from an early draft of A1's report, which A1
  itself later withdrew; I had not re-read the final report against my message.  Corrected
  by SCI-RES-0003 §4 with a struck-through note at the place.  *Rule:* when a workstream's
  report is finalised after a message was drawn from it, diff the message against the
  report's change list before the next checkpoint.
* With this, THY-REQ-0011 is answered except for A1 (review of §11.26, workstream R5).

