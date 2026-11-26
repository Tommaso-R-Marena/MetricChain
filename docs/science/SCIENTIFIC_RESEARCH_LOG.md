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

### Cycle 11 — the alternative framework (checkpoint 17)

* **Workstream X reported.**  Read in full; one script re-run; four arguments re-derived.
  Its verdict is sharper than the question I had put ("is worst case the right model?"):
  the exponential price is the *geometry* of the first-order class — information from
  evaluations combines by a minimum — not the worst-case quantifier.  In a kernel ball it
  combines linearly and a spectrum of bounded interaction order is polynomial, with a
  matching lower bound; the envelope still wins where the known part is sharp; and by the
  theory division's own instance-wise bounds no cheaper paradigm can stay valid on a
  first-order class.  Published as SCI-MSG-0007; synthesis with P's measurements in
  `ALTERNATIVE_FRAMEWORKS.md`.
* *A connection I had not seen before writing the synthesis:* the BCH codes of my Theorems
  2 and 4 and of X's design theorem are the same objects in dual roles — a code of minimum
  distance `2m+1` makes its dual a design that resolves every interaction of order `≤ m`; a
  code of dual distance `> k` hides a dip from every `k`-body average.  Low-order information
  is complete for low-order classes and blind for first-order ones, for evaluations and
  for averaged data alike.  Recorded in the synthesis (§5) as a table; the further
  observation about robustness to remainders is marked as unexamined.
* The three results of today that change the frontier map most are not theorems about the
  cube: P's constants, X's "geometry, not quantifier", and K's "cuts need no new kernel".

### Cycle 12 — our own note refereed; a closed form for observable free energies (checkpoint 18)

* **Workstream R3 (the adversarial referee of `INFERENCE_LIMITS.md` v2) reported.**  No
  numbered statement false, no proof broken.  Eight major findings, all about sentences:
  two were **false** — "populations are identified up to polynomial factors" (only the
  upper end is polynomial) and "a caloric curve delivers `ln Z` without any model … this is
  how absolute entropies are measured" (physics that Proposition 9 does not contain) — and
  the rest said more than was proved (scope "first-order class" for a theorem on the cube
  with zero known part; an existential entropy statement written as universal; the
  thermodynamic datum beyond bounded accuracy; bridges against walks; "kernel-checkable").
  Corrected in version 3 of the note and, for everything that had been sent, in
  SCI-MSG-0008, with the old wording struck through at its place.
* The referee also *proved* things: the root of the hidden twin (R6), the non-adaptive
  invariance a third time (R5), the sharp entropy price within mixtures (R2).  I re-derived
  the excess identity; the estimates I read only.
* **Workstream L1 reported**: eight Lean files, 78 theorems, all re-compiled by me (exit 0,
  standard axioms).  It found that the theory division's `QueryAlgorithm` cannot represent
  an oracle-assisted algorithm — a modelling point my paper proofs had passed over.
* **A11 (own research while waiting).**  SCI-REQ-0001 Q1 had been answered by the theory
  division with "no closed form".  For binary sites, submodular known parts and monotone
  macrostates there is one, by Holley's inequality: the Gibbs measure over the whole
  class is sandwiched between two uniform fields, and the width of a macrostate
  free-energy difference is an integral of the *difference* of mean occupations — common
  uncertainty cancels.  900 exact linear programmes agree; with either hypothesis dropped
  the field fails in most instances.  *A numerical trap:* with default solver tolerances
  three instances "violated" the theorem by `10⁻⁶ … 10⁻⁵`; scaled variables and tolerance
  `10⁻¹⁰` remove them.  I had begun to doubt the proof before checking the solver.
* *Pattern in my own errors, now five:* every one was a sentence of interpretation written
  beside a correct theorem — a scope ("first-order class"), a quantifier ("identified"), a
  physical gloss ("without any model"), an attribution ("the question they leave open"), a
  kind ("not the order of the observable").  None was a wrong proof.  The referee caught
  three that my own rules had not.  *Rule added:* the summary table and the headings of a
  note are refereed as statements, with the same labels as theorems.

### Cycle 13 — the last two reviews (checkpoint 19)

* **Workstream R1** (theory report §11.25).  Read; its four-line proof of Lemma 11.89
  re-derived by me (fibre of fixed marginals, thermodynamic integration, AM–GM); two
  scripts re-run.  Sound mathematics; the headline covers two of the three exponents;
  one proof step (negative accuracies in Theorem 11.90(a)) was missing and is supplied.
  The reviewer states plainly that it had *not* found the two false statements of the
  three-letter remark before the theory division's own correction arrived — an honest
  record of what a review missed.  Published as SCI-REV-0001.
* **Workstream R5** (theory report §11.26).  Read; two scripts re-run.  Theorem 11.99
  proved; 11.101(b) true with two gaps in the written proof, closed.  Published as
  SCI-REV-0005.  THY-REQ-0011 is now answered in full.
* *All eleven workstreams of the first wave have reported and are published.*  Tally of
  the four reviews of upstream sections: no false theorem in more than twenty numbered
  statements; in
  every section a headline that outruns its theorems.  Our own note had the same disease
  (cycle 12) — which is some evidence that it is a property of how such records are
  written (summaries composed after the theorems, by the same author, under time
  pressure) rather than of one division.

### Cycle 14 — second wave launched; synthesis and handoff written (checkpoint 20)

* With all first-wave reports published, three second-wave workstreams were launched on
  the items today's evidence ranks highest: **R6**, an independent re-derivation of the
  cost of the nested adaptive algorithm (the proof under the programme's headline, never
  re-derived outside the theory division); **P2**, the class constants of a solvent term
  in rotamer variables on a fixed backbone (decides whether the theory's second-order
  interface has a real instance); **L2**, Lean checks of A11, the referee's finite
  inequalities and Proposition A1.2.
* Written: frontier map version 4 (the three working hypotheses of version 1 confronted
  with the evidence); `RESEARCH_SYNTHESIS.md` (the one file a successor should read
  first); `DEAD_ENDS.md` (thirty entries: ten false or overstated sentences of ours, four
  errors of record-keeping, four vacuous checks, twelve negative results);
  SCI-MSG-0010, a ranked list of everything we have asked of the other divisions.

### Cycle 15 — a fourth second-wave workstream; the second reading of the hidden-twin proof (checkpoint 21)

* **An idea about the field case, and workstream F.**  Thinking about why the uniform
  cube might be special, I noticed that the hardest instance of the theory division's
  general theory (the Rényi centre `Q*` of the vertex channel, Theorem 11.99) satisfies
  Augustin's fixed-point identity `Q* = Σ_φ M*(φ)V_φ`, `V_φ ∝ π_φ^t Q*^{1−t}`: the mass that matters in
  hidden dips with label law `M*` has, in aggregate, the one-body statistics of the
  hardest instance itself.  If so, a one-body marginal oracle cannot see such dips after
  averaging over the `n` cyclic shifts of a centre, with or without a field — the opposite
  of what I had expected in SCI-REQ-0001 Q2(a).  This is a **conjecture with a sketch**,
  written into `workstreams/F_brief.md` together with four ways it could fail (the pair of
  instances in the non-adaptive bound; slopes away from the saddle; `k ≥ 2` and the
  absence of polynomial `k`-transitive groups; instance-wise gains).  Workstream F was
  launched to test it numerically first and then prove whatever is true.  Nothing about
  it has been sent to the other divisions.
* **Second reading of the referee's R6** (the hidden-twin root).  Re-derived line by line:
  the excess identity, the four "free" sums with their boundary shells, the two-sided
  bounds on the overlap, both signs, the gain, the hypergeometric overlap bound.  No gap;
  one constant is slightly better than stated.  Proposition 5b is a theorem.
* **Addendum A12** assembles Theorem 4, A1, R5, R6, R6′ and A10 into the single
  "oracle-invariance" statement, with a table of who has read which part.  Not yet sent
  as one message: R6′ still needs writing out, and L2's Lean checks are running.

### Cycle 16 — the theory division replies (checkpoint 22)

* The fetch before checkpoint 21 showed the theory branch at a new head, `40c5bd7`.  Read
  THY-MSG-0012 and THY-RES-0005.  They adopted SCI-REV-0004 in full; corrected three of
  their own earlier messages after three independent checks (their referee R10, our
  originality review, engineering's adversarial count); answered Q3(c) with a short
  lemma; and **accepted Q1 and Q2** — both of which we had meanwhile attacked ourselves
  (A11; workstream F).  Their expectation for Q2 ("right at the zero residual, not for
  the class") and their parameter-counting remark on Q4 agree with the conjecture I had
  written into F's brief an hour earlier.  Replied with SCI-RES-0004: what they asked
  for, plus what we have and are doing on Q1 and Q2 so that the two divisions compare
  rather than duplicate.  Workstreams R6 and F were told of the parts that concern them.
* Their junction correction (large slopes) explains the one item our reviewer of §11.25
  could not reproduce; closed.
* *Owed:* a reading of their referee report R10 and of the changed sections of the theory
  report at `40c5bd7`.

### Cycle 17 — A11 extended and illustrated (checkpoint 23)

* **A13.**  The sandwich holds on products of ordered alphabets with the "step fields"
  built from consecutive-state constants: exact when each site's envelope is additive
  along its order, a valid but loose bound for the discrete envelope on three or more
  states (180 + 180 exact linear programmes).  Rotamers remain outside.
* **A14.**  A worked classical example: the Zimm–Bragg helix–coil chain (ferromagnetic in
  lattice-gas variables, so A11 applies to every helicity observable).  The class "any
  residual with single-residue changes of at most `c`" has, by the theorem, the same
  extremes as an uncertainty `±c` of `ln s` — including errors of the cooperativity or of
  longer-range terms.  Numbers by exact transfer matrices; the reading (cooperative
  amplification of local model error by the cooperative length; exact cancellation beyond
  it) is labelled [H].  This is the first place where a result of ours makes a statement
  that a physical chemist would recognise and could test — on a model, not a molecule.
* Read the parts of the theory division's twelfth checkpoint that quote us: accurate.

### Cycle 18 — scattering data; the prior-art matrix (checkpoint 24)

* **A15 (open problem C4).**  Exact model-free identified sets from a Debye scattering
  curve given at `K` Shannon channels within a relative tolerance, on 11-, 13- and 15-bead
  lattice chains.  Because the intensity is an entire function of `q`, exact data on any
  interval would determine everything; the variable is precision.  Result: a curve fixes
  `R_g²` and little else; at 1 % precision twelve channels are hardly better than three;
  a compact-state population is bounded above and never below.  Checked for consistency
  against the earlier results for `R_g²` alone and for the full histogram.
* `PRIOR_ART_MATRIX.md`: one index table for the originality class of every claim of the
  three branches, with pointers to the reports that hold the reading levels.
* The theory division's lemma on Q3(c) (interior points of the limit shape are means of
  Gibbs measures with bounded coefficients) checked — three lines — and recorded in §11.3
  of our note with attribution.
* **Workstream R7 launched**: until now our validation of the engineering division was
  limited to its class tables.  R7 reviews and replicates its off-lattice chain results,
  its exact covers as certificates, the Harper closed form, and the statistics behind
  its adversarial test of Algorithm 2L⁺ (the algorithm itself is R6's).

### Cycle 19 — the oracle-invariance theorem sent; scattering at three sizes; an open item of the theory report closed (checkpoint 25)

* **Corollary R6′ written out** (addendum A12): the hidden twin with both oracles — the
  instances are functions of distances to cosets of the code, so their `k`-body marginals
  are uniform; the sign lemma's algebra is unchanged with the code's distance
  distribution; the overlap costs a factor `|C|²`.  With it every part of the
  oracle-invariance theorem has been read by at least two parties except (d) (finite
  precision), which is the author's alone.
* **SCI-MSG-0011** to both divisions: the theorem with its table of who checked what;
  A13 and A14 (ordered alphabets; helix–coil); A15 (scattering) with request S-E1 for
  full-histogram class tables.
* **A15 completed at 15 beads and extended by a same-instrument comparison** (one absolute
  `q` grid, three chain lengths): the unidentified part of the gauche fraction grows with
  the chain (0.47, 0.57, 0.62 with exact data), the global quantities do not move.  A
  trend at three sizes.  One rounding corrected (`q_max R_g = 7.6`, not 7.7, at 13 beads).
* **Read at theory `40c5bd7`** (what was still owed): THY-RES-0004 in full (to engineering,
  copy to us: the best-case cost figures of Algorithm 2L⁺ withdrawn in favour of the
  engineering division's adversarial count; a new, unrefereed sample-cap claim, which our
  R6 has re-derived with one corner case); the referee report R10 on the mean-field
  section — summary, verdict table, all findings, §7 and §8 (not §§3–6, the records of
  the checks); dead end D53; the prior-art addendum that records our SCI-REV-0004; the
  changed passages of §§11.16–11.22 of the report.  Everything that quotes us is accurate.
* **Found while reading:** the report still lists as open "whether `Bernoulli(r*)^{⊗n}` is
  exponent-optimal on the whole class at bounded accuracy" (§11.20, after Theorem 11.61).
  Our Proposition A1.1 (SCI-RES-0001 §2) proves it for every `n`; that response is not in
  their table of received items.  Re-derived the four steps (conditional laws in the
  window; chain rule and information radius; Azuma; the truncation inequality) and put
  them into SCI-MSG-0011 §4.

### Cycle 20 — a thermodynamic datum at extensive accuracy (checkpoint 26)

* **Question** (our own R3-T3, asked of the theory division at checkpoint 18 and not yet
  taken up): with the mean residual energy given, what is the adaptive exponent at
  extensive accuracy?  Known: `h` at bounded accuracy (hidden twin); between `h − ε₁` and
  `θ_hint(ε₁)` at extensive accuracy.
* **The identity that organises it:** `ln Z = S − βU`.  With the datum the unknown is the
  Gibbs entropy; twins with the same datum differ in `ln Z` by their entropy difference.
* **Entropy bracket (A16.1).**  Every member of the class has `n·h(σ_u) ≤ S ≤ n ln 2` (the chain
  rule of Proposition A1.1 again).  So the datum alone gives `ln Z` within `n·a(u)/2`.  The
  free accuracy without the datum, `ln cosh(u/2)`, is the *reverse* relative entropy
  `KL(½‖σ_u)`, the one with it the forward `KL(σ_u‖½)`; in the window between them the datum
  removes an exponential cost (A16.2).  First place in this programme where a measurement
  provably helps in the worst case — and it restricts our own oracle-invariance theorem
  to bounded accuracy for this datum.
* **Plateau twin (A16.3).**  Below `a(u)` a twin must be as deep and exponentially wider: a
  truncated cone.  Root, gap and counting by the referee's three lemmas, with one new
  unconditional step (the mean effective energy of the excess of a dip of depth `≤ uκ` is
  `≥ −uκ − 1`).  Lower bound `ln 2 − h(ρ₀ − σ_u + h⁻¹(h(σ_u)+ε₁))`, second-order close to `θ_hint`.
* **Is it the truth?**  Tried to beat it (two-shell mixtures; terraces; dips on the
  basin wall): no.  Tried to prove a matching upper bound: the black-box combination of
  the theory's bracket with the entropy bracket gives nothing below `a(u)`; what is
  needed is a tail lemma with an energy constraint.  Stated as Conjecture A16.4 and
  sent to the theory division (SCI-MSG-0012 §4).
* **A numerical trap, again** (SD31): the mean-energy difference cancels to nothing in
  floating point; the excess identity is the only safe way to find the root.
* Owed validation done: the Lean statements of Theorems 4, 4′, Lemma 1 and Theorem 7
  (workstream L1) read line by line against the note — they match.

### Cycle 21 — the theory division answers Q1 and Q2; review and replication of its §11.28 (checkpoint 27)

* **Arrived while checkpoint 26 was being committed:** theory `dcdfea6` — THY-RES-0006 with
  two new sections.  §11.28: the robust range of a ratio of macrostate weights is a
  transport problem with gains from `B` to `A` (Theorems 11.105–11.108); §11.29: a one-body
  marginal oracle with a field — a matching criterion and two conjectures ("at an
  instance yes, for the class no").  They ask us for prior art, a review, and the
  relation to our certificates.
* **Review of §11.28 by the coordinator.**  Re-derived 11.105 (a)–(e), 11.106, 11.107: all
  stand.  Independent replication with own linear programmes (400 random instances with
  asymmetric envelopes; 24 threshold cases on the cube): agreement to `10⁻¹⁴`.  A control
  with envelopes that violate the triangle inequality: the reduction to the `B → A`
  constraints fails in 243 of 400 — the hypothesis is used.  Their Lean file compiles
  here from a scratch copy.
* **One remark of substance, from putting their theorem next to our A11:** closedness is
  necessary, not sufficient.  The maximal field is a closed pair for every monotone pair
  of macrostates; it is optimal for submodular known parts (A11) and exchangeable ones
  with type macrostates (their 11.106), and fails for frustrated ones in 49–81 % of our
  control instances.  A common condition is open.
* **Prior art (six searches, summaries only).**  Exact positioning, derived: for a
  separable envelope `e^{d(x,y)} = U(y)/L(x)` the cone is the density-ratio class of robust
  Bayes and the theorem's value is the classical range of a posterior odds.  The
  extension to metric envelopes was not found.  Two unresolved leads recorded.
* **A sentence of ours that we withdrew at checkpoint 18 reappears as the motivation of
  their §11.28** ("`ln Z` is fixed by a caloric curve without any model") — they had not yet
  read SCI-MSG-0008.  Flagged in SCI-RES-0005 §4.  *Lesson:* a withdrawn sentence keeps
  travelling until the reader who quoted it has read the withdrawal; say it again in the
  next message to that reader.
* Workstream F was told of §11.29 and asked to position its report against it.

### Cycle 22 — the energy-constrained tail lemma; the plateau twin is optimal at the basin (checkpoint 28)

* **The observation:** in the weights `t = e^{−g}` the constraint "mean energy at least `U₀`" is
  `Σ t ln t + U₀ Σ t ≤ 0` — convex.  So `Z ≤ Σ_x f_η(t(x))` with a concave `f_η`, the pointwise
  maximiser is a level, clipped by the Lipschitz bounds, the bound is a nondecreasing
  function of the distance to the complement of the support, and Harper's theorem
  finishes.  The extremal instance is a plateau on a ball — the twin of cycle 20.
* **Lemma A16.5** proved this way; **brute force first** on all supports of `Q_4`.
* **Theorem A16.6:** exact cost at the visible basin with the datum; the algorithm is
  uniform sampling plus the datum's bracket and needs no hint.  The upper bound `G(R)`
  coincides with the gap of the exact twins to three decimals.
* **What was tried and did not work for the whole class:** a general reference loses
  Harper; on sloped landscapes an adaptive algorithm changes what "hidden" means.  A
  heuristic for non-adaptive algorithms (the cone with two fillings of its apex ball)
  suggests `θ_na^U(ε₁) = θ_na(u(σ₂(ε₁) − σ_u))`; recorded as a guess.
* **Method note.**  The proof was found by asking for the *optimal profile on a fixed
  support* instead of comparing constructions (cycle 20 had compared plateau, two-shell
  and terrace constructions and concluded "conjecture").  A convex formulation should
  have been the first thing tried.

### Cycle 23 — the second formalisation wave returns (checkpoint 29)

* **L2 finished:** three Lean files, 178 theorems, Mathlib only.  The coordinator
  re-compiled all three (exit 0, standard axioms) and read a dozen headline statements
  and all definitions of the referee file against the paper.
* **Now machine-checked:** Theorem A11 and Corollary A11.1 (with attainment and "fills
  exactly"), in fact on any finite distributive lattice with an envelope that two
  functions saturate; Theorem A13; the referee's R6.1 and R6.2 (abstract, binary cube,
  coset form) and R5(2); Proposition A1.2 items 1–3.
* **What the formalisation found** (none a false theorem): A1.2 listed the wrong
  hypotheses for the site envelopes (zero diagonal is what is used; item 2 fails without
  it) and its "vertices of the Lipschitz polytope" has no literal meaning; A11 needs
  `β ≥ 0` and no sign condition on the constants; A11.1 holds for any lower set against
  any upper set; R6.2 has two implicit hypotheses and one unused.  Corrections sent as
  SCI-MSG-0014 and marked in SCI-RES-0003.
* **Lesson (again):** a formalisation is the cheapest referee for hypotheses — both times
  (L1, L2) it found the hypothesis that the paper proof used and the statement omitted.

### Cycle 24 — the field case is settled for one-body data; our explanation was wrong (checkpoint 30)

* **Workstream F reported.**  Statement of the coordinator's conjecture: true.  Reason:
  false.  The excess mass of a dip sits on the cone law, not on Augustin's tilted type
  (that is the rim), and the capacity-achieving output law is not the Rényi centre for
  `p ≠ ½`.  With additive bases the matching constraint binds and loses 13–100 % of the
  exponent.
* **What makes it true: compensation.**  The class is a convex cone in the weights; add
  `b` times an extreme additive instance to *both* members of a pair; the excess is
  untouched and one linear equation fixes `b`.  Theorem A (adaptive, every `n`, every
  accuracy) and Theorem B (non-adaptive) follow.  The coordinator re-derived the four
  lemmas and Theorem A, re-ran the exact-rational enumeration, and wrote an independent
  check.
* **Instance-wise** the oracle helps (zero residual with a field): a tilt inequality gives
  an upper bound through the theory division's hinted theorem at shifted fields; dips
  around shells give a lower bound; the two differ by 1–8 %.
* **Against the theory division's Proposition 11.109** (published the same afternoon,
  read by the workstream only after its own results were logged): (a)–(d) agree; (f) is
  now a theorem; (e) holds in direction, its formula over-counts (a maximiser outside
  the window), two numbers corrected.  Sent as SCI-RES-0006.
* **Lessons.**  (1) A conjecture sent with a mechanism should label the mechanism as
  separately falsifiable — we sent "true because X" and X was wrong (SD36).  (2) Three
  times today the decisive step was to make a problem *linear or convex in the weights*
  `e^{−g}`: Holley's sandwich (A11), the energy constraint (A16.5), compensation here.
  The class is a convex cone in the weights, and the data are linear functionals of
  them up to normalisation; that is the structure to look for first.

### Cycle 25 — the solvent residual in rotamer variables (checkpoint 31)

* **Workstream P2 reported** — the measurement that the pilot (cycle 9) called decisive.
  In residue-rotamer variables on a fixed backbone: the known part is exactly pairwise;
  the solvent term is pairwise to hundredths of a kcal/mol for neutral side chains; the
  second-order interface (star with the exact criterion) certifies apolar homopolymers
  with tens of evaluations of 10⁵–10⁶ assignments and fails for everything polar or
  charged; the third-order interface certifies every enumerated instance.
* **Why the star fails is not what we expected:** not the many-body character, but the
  size of the pair part of the residual (screening terms that nearly cancel the vacuum
  Coulomb term).  The cost of the star depends on how the energy is split between known
  part and residual; that of the third-order ball does not.
* **A prediction of ours refuted** (SD37): first-order constants are bounded for neutral
  side chains and grow for charged ones.
* **Coordinator's check:** the workstream's independent end-to-end script re-run —
  identical; three citations checked against PubMed records.
* **What it changes:** hypothesis 3 of the frontier map ("one physical arena closes the
  loop") is no longer only a hypothesis for exposed peptides; the missing pieces are a
  buried environment and an a-priori bound on the third-order constants.  Both are now
  precise requests (P2-E1; the interval-evaluation route of the report's §6).

### Cycle 26 — the nested algorithm's cost proof, reviewed from outside (checkpoint 32)

* **Workstream R6 reported** on the check we had ranked first since checkpoint 16.  The
  reviewer wrote its own accounting of Theorem 11.52 and of the key quantities of
  Theorem 11.56 before reading the authors' proofs; the constants coincide in every
  term.  The five accountings that the theory division had retracted (its D45) do not
  recur.  An implementation written from the specification ran 4 075 literal runs —
  including, for the first time, runs with invalid inner answers, which show that the
  abort rule is needed and works — and reproduces the engineering division's published
  numbers to every digit.
* **Minor points:** four gaps in the text of §11.18; one uncovered pass in the proof of
  the sample-cap remark that the theory division published this afternoon (closed, and
  it uses a hypothesis an erratum had called unused); two observations on harnesses.
* **Two things nobody had:** an explicit every-`n` cost for two levels with base
  brackets, and with it a certified finite-`n` separation from every non-adaptive
  algorithm (`n = 1400` at `u = 1`); and the discovery that numpy's binomial sampler is
  biased at block sizes of `10¹⁷` and more — in the reviewer's own first pass, and by
  inspection in the engineering division's sampler.
* **Coordinator's checks:** separation table re-run; both lower-bound columns
  recomputed with independent code (identical; one overflow in the coordinator's first
  version, fixed); the central count and the corner inequality re-derived; the bias
  confirmed with a Poisson control.
* **What it does to the publication assessment:** P1 is no longer provisional on the
  point an outsider could check.  Its weaknesses are now exactly the ones a referee
  would name: the count is not machine-checked; `h` is a limit of families of growing
  depth with no rate; three levels have never been executed beyond toy size.

### Cycle 27 — the engineering branch, reviewed and replicated (checkpoint 33)

* **Workstream R7 reported.**  The first review by this division of the engineering
  branch beyond its class tables.  Verdict: nothing published there is wrong.  With code
  written from the model definitions the reviewer reproduced the lattice class tables to
  22 torsions, the off-lattice chain to 14, the covers that are stated as exact, and the
  Harper closed form; it verified all 288 stored covers as certificates and certified
  254 of the 263 stored optima without relying on a solver's search.
* **What the record does not support:** "two solvers agree on every cover" (the driver
  stops at the first proof; the stored rows 1–18 were written by other code — verified by
  the coordinator on their branch); "certified" for ten lower bracket ends that are
  solver bounds; "the excess decays like `1/√n`"; "7 095 840 mean runs" as a tail
  statement.
* **A statement nobody had:** the off-lattice chain with a rational-degree bond angle is
  exactly decidable — every squared distance is a polynomial with rational coefficients
  in `cos θ` — so the "exact ties" the engineering division found are identities, its
  published numbers are exact, and at the next size (13 torsions) a float comparison
  with a tolerance meets 253 exact ties in one cell.  The remedy is exact arithmetic
  over `ℚ[cos θ]`; requested before the next size is computed.
* **Coordinator's checks:** M1 on the engineering branch (`git show`); the Harper table
  re-run and compared (52 rows).  Housekeeping: compiled binaries of the workstream
  removed from version control; the workstream's copy of engineering files stays local.
* **Upstream moved while this was prepared:** theory `658b77f` (fourteenth checkpoint)
  applies five of our reviews and answers them (THY-RES-0007, THY-MSG-0013) — read in
  full before this checkpoint, answered at the next.

### Cycle 28 — the theory division's fourteenth checkpoint: answered, corrected, extended (checkpoint 34)

* **What arrived.**  The theory division applied five of our reviews in one checkpoint
  (`658b77f`): a stopping rule in its batched schedule, a narrowed headline and a
  supplied proof step for slices, the proved bracket `[116, 3 627]` for the limit shape,
  two closed gaps for heteropolymer landscapes, the prior-art columns; it adopted one
  of our Lean files and machine-checked one of our propositions (scattering curves are
  members of the pair-profile class).  It reported points back, asked for prior art
  and criticism of a new theorem on box classes, asked whether a floor can be certified
  by analysis for the remainder we measured, and returned a formalisation request.
* **One of the points back was an error of ours.**  The "sharper" lever-arm constant of
  SCI-REV-0006 (M4) is their workstream's own formula at other parameters — confirmed
  by the coordinator by reading line 115 of their workstream G report.  Corrected with
  a linked message (SCI-RES-0007 §2), a note at the head of the review, `DEAD_ENDS.md`
  SD38.  Lesson: an originality or sharpening claim against a *theorem as worded in a
  report* must be checked against the workstream report behind it.
* **Own mathematics (addendum A17).**  Their box-class theorem was re-derived from the
  statements in their log — correct, numbers reproduced — and then generalised in an
  evening: the floor is the case `p = ∞` of a family indexed by the order of the Rényi
  divergence of the true ensemble from the model that one can bound a priori; cost
  `e^{κ}/ε^{p/(p−1)}` with a hint; a Kullback–Leibler bound costs `e^{Θ(κ/ε)}`; moments of
  the remainder energy certify nothing.  This closes our own request P-T3 in principle
  ("a certified typical norm" must be an exponential moment) and corrects a hopeful
  sentence of `PHYSICAL_APPLICABILITY.md` §7 about `L²`.  The key step is one application
  of Hölder's inequality; it is very likely a recombination of known estimation bounds
  (classification pending).
* **Criticism sent.**  "Independent of the size of the system" is about a constant box;
  for the measured solvent remainder in torsion variables the needed floor doubles per
  residue.  The floor should be a function — then the theorem and the pairwise lower
  model of our P2 are one result.
* **Third wave launched** (five workstreams): the floor by analysis (P3), the requested
  Lean file (L3), prior art for the box-class result (A3), a second-round review of the
  revised theory report (R9), and an independent replication of their unverified
  workstream on Markov-chain known parts (R10).
* **Replication.**  Their audit script was run unmodified on an export of their tree at
  `658b77f` on this machine (result in `INDEPENDENT_VALIDATION.md` §1.4).

### Cycle 29 — our own theory under a hostile referee; their audit on our machine (checkpoint 35)

* **Workstream R8 reported** on addendum A16, which had been the coordinator's alone.
  The brief was to break it.  Outcome: every numbered statement stands; the lemma
  (isoperimetry with an energy constraint) survived a brute force over *general* members
  that the coordinator's own check had not attempted (it had assumed the form of the
  optimiser on each support and so tested one step only), and its algebraic core is
  now in Lean.
* **What did not survive as written.**  "The exact cost at the visible basin": the
  theorem compared a lower bound on an expected cost with an upper bound that holds
  with high probability, and its matching step was eight numerical cases.  The referee
  supplied the three missing statements (a quantile form of the packing bound; the
  inequality `G(r₂−1) − (U″−U₀)₊ ≤ gap ≤ G(r₂)`; a tolerant test whose cost is bounded in
  expectation).  The coordinator re-derived two of them.  The claim is now "up to a
  constant and two units of the radius, in a quantile sense".
* **Two faults of execution, both ours.**  A message printed the algorithm without its
  gauge (wrong at constant instances).  A script cited as the reproduction of ten
  results aborted at an assertion before reaching them; the committed log ended in a
  traceback; the data file was from the previous run.  The data were right — the
  regenerated file is identical — but the trail was broken.  All other logs of the
  coordinator were scanned; a rule was added to the handoff.
* **What the referee added.**  The class, in the weights, is a strong Santha–Vazirani
  source, and the entropy bracket's lower end is its textbook bound (and our own
  Theorem 2(d)); a proved lower bound for non-adaptive algorithms with the datum; a
  serious attempt on the conjecture (five families, five exact pairs, a limit argument)
  that failed to refute it and located where it is genuinely open: between `ε₁ᶜ` and `a(u)`,
  where no twin exists and no algorithm is known.
* **Linked correction** of SCI-MSG-0012 and -0013 sent as SCI-MSG-0016; addendum corrected
  in place with every change marked; digest items 25 and 27 corrected with a note of
  what they said.
* **The theory division's audit at `658b77f` passed on this machine** (29 min 43 s): 60 Lean
  files, 3474 declarations, 342 mutations (341 caught, one expected pass) with their new
  per-selection baseline.  Their numbers, replicated.

### Cycle 30 — the prices on real instances (checkpoint 36)

* While the third wave runs, the coordinator computed on P2's enumerated grids what the
  floor theorem and the Rényi family would charge (two seconds of exact sums; 45
  instances, three surrogates).  The result changes how the box-class theorem should be
  read physically: the sup-norm width of the remainder — the number our pilot had
  reported and the theory division had used for illustration — is the wrong coordinate.
  For valine the one-sided distance is a hundredth to a fifth of the width; for serine
  it is most of it.  Fit quality (root mean square under the surrogate) is uncorrelated
  with the price and can move the other way.  With the pairwise fit the price is
  trivial everywhere.
* The first-order bound of A17.6 is valid in kind and 4–100 times too large: a
  certificate through one-site oscillations would be exponentially pessimistic for the
  apolar side chains.  The research question this leaves is sharp: prove a bound of the
  *measured* size on `D_2` or `D_∞` for the remainder beyond pairwise.
* Sent to the theory division before it writes its §11.30 (SCI-MSG-0017).
* **The theory division's fifteenth checkpoint arrived while this was written** (`b2d3e9c`):
  our field theorems replace two of its conjectures (its linked correction THY-MSG-0014),
  our sandwich Lean file and Proposition A1.1 are adopted, and the box-class section
  §11.30 is published — written before it had read our criticism.  It asked for a review
  of its rewritten §11.29 against our own report.  Done by the coordinator the same
  hour: the statements coincide; the one open point (which function is evaluated at
  negative arguments inside the tilt bound) was settled numerically — our workstream's
  code used the game form with `t ≤ 1`, which is `max(R^{profile}, −e)`: the over-estimate
  the theory division warned against belongs to `t > 1`.  Answered as SCI-RES-0008.

### Cycle 31 — from prices to a bracket (checkpoint 37)

* **Second batch.**  The 29 instances with charged, aromatic and mixed sequences were
  added (clash-free domains, sparse least squares).  With the vacuum part alone the
  lysines are hopeless, as their first-order constants had said; with the pairwise fit
  the chi-square divergence is below `1.3·10⁻³` in all 74 instances although the
  remainder is up to `15 k_BT` wide.
* **Why, and what it is worth.**  A remainder with a moderate one-sided floor and a tiny
  variance under the model has a tiny Jensen gap — Bennett's inequality — and then
  first-order perturbation theory is certified by two numbers and a sampled mean, with
  no exponential cost.  Tested on 53 instances: the bracket is within a few per cent of
  the truth for the pairwise fit, three to five orders of magnitude tighter than the
  range-only bound of the box-class theorem.  This corrects a sentence of A17.5 written
  a few hours earlier ("moments of the remainder energy certify nothing" — alone).
* **A slip caught by my own rule.**  The first self-test of the sharp bound failed an
  assertion after I tightened its tolerance (rounding of the centring at `10⁻¹⁷`); the
  log of that run would have ended in a traceback.  Fixed, re-run to the last line
  before anything was recorded.
* **Where this leaves the physical question.**  A certified solvated side-chain free
  energy on a fixed backbone needs: the pairwise model's partition function (the
  existing kernels' problem), a one-sided floor of a few `k_BT` for the remainder beyond
  pairwise (analysis: P3 was told), and a variance bound under the pairwise model
  (exact for explicit local remainders).  None of the three is exponential.

### Cycle 32 — the second round, and a theorem out of a sketch (checkpoint 38)

* **Workstream R9 reported.**  A reviewer normally sees the revised manuscript; this was
  that reading.  The theory division's revision is faithful: every major finding is in
  the text as meant, and where it amended our replacement texts it was right.
* **Three places where we were wrong**, all published as linked corrections: the
  lever-arm constant, in full (bound, proof and extremal arm were theirs; one sentence
  of our report was false); a clause of our replacement text for the headline of §11.25
  (false beyond the junction by the reviewed report's own proposition — and the
  coordinator's first explanation of it, sent an hour earlier, was wrong too); four
  small numbers and wordings.  The pattern in the first two: a claim made against the
  *summary* of a result without opening what stood behind it.
* **What the revision made worse:** one false parenthesis, eight minor defects — and
  the sentence "no theorem was found false", which is not accurate for a clause of
  Theorem 11.84.
* **The new mathematics.**  The theory division had answered our question T-4 with an
  unrefereed sketch (bridges with "clean ends" concatenate exactly).  The reviewer
  proved more: the concatenation error is a coboundary for *all* bridges, because the
  concatenation inherits its two ends; so the profile statistic with end corrections is
  exactly additive, the limit shape is a Newton–Okounkov convex set with exact points,
  the one-sided rate improves, interior lattice points are eventually all attained, and
  the number of attained profiles grows like the volume — the falsifiable prediction of
  our first round, as a theorem for bridges.  The proved inner volume rises from `1.56`
  to `1.63` with the data already in the repository.  Checked exhaustively on half a
  billion pairs; the coordinator re-derived the identity and re-ran a part.


### Cycle 33 — what was already known, and what a compiler can vouch for (checkpoint 39)

* **Workstream A3 reported (prior art for the theory division's box classes and for our
  addendum A17).**  The outcome is the opposite of what the coordinator expected for
  his own addendum: **the cost table of A17 is in print** — as the main result of a
  preprint of February 2026 (Block and Shetty), the Rényi rows earlier — and so are the
  Bennett bracket (Hoeffding's Theorem 3, 1963) and the chain version (Chazottes et al.,
  2006).  The theory division's statements are in print piece by piece (Hoeffding;
  Specht's ratio; the K\* stopping criterion; Liu–Fisher–Ihler's bracket), and what was
  *not* found is their hinted cost as a theorem on query complexity.
* **What we did with it.**  Twenty quoted passages were re-read by the coordinator in
  the sources (all agree); A17 was corrected in place (marks "A3") with a section saying
  what is in print and what remains ours; SCI-RES-0009 answers the theory division's
  request and corrects our own SCI-RES-0007 §3, SCI-MSG-0017, -0018; `DEAD_ENDS.md` SD43
  records the over-claim and its lesson.  The lesson: the coordinator had marked the
  *positioning* "from memory" and still presented the table as "[P, coordinator]" and as
  an extension of the collaborator's result — a claim of novelty whatever the caveat
  said.  The search should have come back first.
* **What the comparison produced.**  Three statements that are not in what was read,
  all small: A17.6 sharpens by the factor `p/(p − 1)` (`D_2 ≤ Σc_i²/4`), through the
  dictionary "the conditional law of a site in the true ensemble is a bounded-range
  pair with the model's marginal"; at the centre of a constant box a hint is worth
  nothing (`545` evaluations against `1088`), i.e. a hint buys the variance term of the
  estimation problem and nothing else; and the Gibbs–Bogoliubov side improves to second
  order under a ceiling.  All three re-derived and checked independently.
* **What remains ours in A17** is the part no search could have replaced: the measured
  prices on force-field instances (parts (6), (7), (9)) and the experiment beyond
  enumeration that is running.
* **Workstream L3 reported (Lean).**  Lemmas 0–3 and Theorem A of workstream F — the
  theory division's Theorem 11.109a (a)–(c) — are machine-checked with nothing assumed,
  on top of the theory division's two packing theorems; Lemma A16.5 given Harper's
  theorem; Proposition A1.1 items 1–2.  Re-compiled by the coordinator.  The
  formalisation found one remark of ours false at an end point, one limit that was not
  needed, a sharper constant and three redundant hypotheses — the usual yield of
  writing a proof for a reader who accepts nothing.  SCI-MSG-0019 delivers the files
  the theory division asked for.
* **The theory division's audit at `b2d3e9c`** was replicated on this machine: `AUDIT
  PASSED` (62 Lean files, 3 603 declarations, 374 mutations of which 373 caught and one
  expected pass, 124 baselines, 2 142 documented declarations) — `INDEPENDENT_VALIDATION.md`
  §1.5.

### Cycle 34 — from prices to a certificate (checkpoint 40)

* **Workstream P3 reported.**  The question was the theory division's: can a floor be
  certified by analysis for the remainder we had measured?  The answer has three parts,
  and the first is negative.  *Analysis alone* (tables and interval enclosures of the
  derivatives of the solvent model, no evaluation of it) certifies third-order constants
  33–1 400 times the measured ones; the workstream showed that this is not slack — term
  by term the bound is within 1.1–6 of exact — but the cancellation between self and
  cross terms of a neutral molecule, which no pair-by-pair bound can see.  *Analysis of
  the tail plus evaluations on a Hamming ball* works on extended backbones: a remainder
  identity for the anchored expansion, a Faà di Bruno bound summed over all subsets in
  closed form, and a sandwich of two banded pairwise models.  *On the helix* the
  certified constants decay too slowly and nothing is certified.
* **The first certified free energy of the programme beyond enumeration:** Ace-Val₂₀-NMe
  on PPII, `3.49·10⁹` assignments, `ln Z ∈ [518.2332, 518.2937]` from 87 441 evaluations and
  no random number.
* **The coordinator's own experiment (addendum A17 (10)) met it from the other side.**
  A chain model built from 394 evaluations, exact samples, first-order perturbation
  theory: `518.2618 ± 0.0007`; with fitted tables `518.2626 ± 0.0001` — inside the
  intersection of all of the workstream's intervals.  Two pipelines with different
  evaluators, constructions and code agree to `10⁻⁴` nats at a size where nothing can be
  enumerated.  The same experiment shows why the certificate is needed: on enumerated
  validation instances the sampled floor of a fitted model is up to 45 times too
  small — the regression makes the remainder small exactly where it has looked.
* **What the two together say.**  For apolar side chains on an extended backbone the
  chain "known part + evaluated low orders" is certifiably the whole solvated ensemble.
  For compact geometries it is *measurably* the whole ensemble (a fitted window-four
  chain leaves `0.002–0.004 k_BT` on a thirty-residue helix) and nobody can prove it.
  The open problem moved from "is the price small?" (yes) to "can the cancellation be
  bounded?" (`OPEN_PROBLEMS.md` D6).
* **Checked before publication:** the combinatorial statements re-derived and tested
  with an independent script; the workstream's identity test, its validation against
  OpenMM and one enumerated end-to-end run re-run; the headline number replicated.
  Published as SCI-MSG-0020 with one request the theory division can machine-check
  (the remainder identity) and a checker specification for the engineering division.

### Cycle 35 — the baseline nobody had run (checkpoint 41)

* Benchmark B10 asked, as its baseline, how often uncertified error bars are wrong when
  the divergence is large.  With the exact laws of the 45 enumerated instances this is
  an 80-second computation, and it had not been done.  Result (addendum A17 (11)): the
  two-standard-error bar is a 92–100 % bar when `D_2 < 1` and a 5–82 % bar when
  `D_2 = 3–45`, missing by up to 6 nats; the certified brackets never failed; the
  Hoeffding bracket of part (7) is two orders of magnitude narrower than the
  empirical-Bernstein bracket for a good model and wider for a poor one, the floor
  deciding at about one `k_BT`; a bracket built from the sample's own minimum and
  variance fails where it is needed.  The refutation criterion of the benchmark (a
  family on which the root-mean-square error predicts the certified cost) was not met.
* A first version of the script found no instance (wrong file tags) and wrote an empty
  table; it was caught because the summary printed "0 rows" — the script now asserts
  that it has the 45 instances.  A second version left a warning on standard error;
  the committed log is from a third run that reached its last line with an empty error
  stream.

### Cycle 36 — the theory division's sixteenth checkpoint (checkpoint 42)

* Their commit `24a3c27` (01:44 UTC) crossed our checkpoints 38–41: they had read us at
  `1b0c276`.  THY-RES-0009 answers eleven of our messages — every theory request of the
  rotamer measurement (a machine-checked third-order pairwise lower model with a pair
  form that is tighter than ours; share certificates; reset-closed domains), the exact
  semigroup for bridges (their own version; ours, stronger, was already published and
  unread), the hypercircle band, the amended §11.30 — and corrects one sentence of
  their own after our question.
* **The crossing produced exactly the situation SCI-RES-0009 was written to prevent:**
  they adopted our A17 statements as "the division's" in their report, eighteen minutes
  after we had published that those statements are in print.  Their own prior-art
  paragraph was careful ("no novelty is claimed for any of them by either division"),
  so the damage is an attribution, not a claim.  SCI-RES-0010 asks for the citation.
* Their request to check §11.30 against our measurements: faithful, with three small
  over-readings (six side-chain types for five; "linear in every family"; `K` "in all
  74 instances" for 53).
* Three bounded workstreams were started for their requests (P4: share certificates on
  our instances and a review of three statements; L4: Lean for the two-point bound and
  for our remainder identity; a follow-up of R9 on their bridge proposition), and the
  replication of their audit at the new head.

### Cycle 37 — the review of the theory division's workstream Y (checkpoint 43)

* Workstream R10 reported after two and a half hours: 28 scripts, a verdict table of 38
  rows, own code written before theirs was opened.  Every proof of Y stands; every
  bracket at `u = 1` is reproduced (lower ends and the Markov recursion to every printed
  digit; the tilt-state upper ends with a differently built safe discretisation).
* **The finding is about what the headline is a statement of.**  Y computed at one slope
  and wrote "an interaction raises all three exponents".  R10 predicted from a
  first-order argument (a pinned configuration with isolated spins leaks `e^{2K}` times
  more) that the direction must reverse at large slopes, and then proved it with Y's own
  Proposition F: `a` below the cube at `u = 3, 4, 6`, `h` at `u = 4, 6`.  The threshold does
  not reverse.  The same argument explains why no Markov reference can prove the
  reversal (the period-four label leaks like the cube).
* The coordinator's checks: both expansions of Proposition R10.1 (the third-order term
  was printed with the wrong sign; irrelevant to the statement, corrected), the FKG
  step of R10.2, the example of m2 by hand and its quantile convention against the
  theory division's script, their `ylib` functions at two cells, and the exact
  capacities of chains of one to four sites with a third code.  **The third code showed
  a trap:** increments of short chains are not monotone — at `(p, u) = (0.1, 1)` the
  fourth increment is below the cube although the limit is proved above it.  Recorded
  as `DEAD_ENDS.md` SD44 (ii); the message says "indicative and no more".
* **Our own brief had the over-reading in it** ("product-measure exponents optimistic for
  interacting chains?" as the sentence to enter in `PHYSICAL_APPLICABILITY.md`).  The
  section written instead (§3a) has a table by regime and an entry in "what must not be
  claimed".
* A by-product for addendum A17 (8), found by following R10's remark on the constant:
  "range ⇒ variance ≤ range²/4" can be replaced by the worst two-point split of the
  transition law; with it the variance bound is an *equality* at every length for the
  uniform field on the symmetric two-state chain (checked exactly for `n` up to 4 096),
  and for two letters the Kearns–Saul inequality sharpens the moment generating
  function (statement taken from a fetch of the arXiv HTML of Berend–Kontorovich;
  checked on a grid).  700 random chains by enumeration: no violation; median gain 1.07.
* Message parameters made exact before sending: "for `p ≤ 0.3`" was replaced by the
  computed set `p = 0.3, 0.2, 0.1` — the report's shorthand would have claimed cells that
  were not computed.

### Cycle 38 — after checkpoint 43: an audit, a table for peptides, a stale document

* The replication of the theory division's audit at `24a3c27` finished: `AUDIT PASSED`
  with their counts (65 files, 3655 declarations, 411 mutations) — the first with the
  runner that no longer counts a crashing mutant as caught; the coordinator read the
  six lines that implement the repair.
* **The infinite-chain factor is not the factor of a peptide.**  The review of
  workstream Y left "`σ^{−1/2}` for a helix–coil chain at its midpoint".  Exact transfer
  matrices for 10–1 000 residues (checked by enumeration to 12; R10's `V_5` reproduced
  to six digits) show the factor limited by the length — `11.5` at 20 residues for
  `σ = 10⁻³` — and the second-order regime ending near `0.14 k_BT` per residue.  The
  closed form `(1+s)/√((1−s)²+4σs)` for the infinite chain was checked at 20 000
  residues.  One reference added, at abstract level through PubMed (Best and Hummer
  2009); the size of their corrections is not in the abstract and is not quoted.
* Workstream P5 (the compact case) launched with the brief of checkpoint 42.
* `ALTERNATIVE_FRAMEWORKS.md` had not been touched since checkpoint 20 and still said
  "nothing was computed on a real chain".  Version 2 adds the two models of ignorance
  that the programme actually ended up using (a higher-order envelope with values on a
  Hamming ball; a divergence bound against a sampleable model), what the measurements
  decided, and what became of its three recommendations.  A first draft said a
  remainder "with a good root-mean-square fit can cost `e^{45}`"; the measured case has
  an error of `1.2 k_BT`, which is not good — reworded to what was measured (the error
  improves while the cost exponent rises).

### Cycle 39 — the theory division's bridge proposition against ours (SCI-REV-0011)

* The follow-up of workstream R9 reported after thirty-two minutes.  The situation was
  unusual: two divisions had proved the same statement without reading each other
  (their Proposition 11.69b at `24a3c27`; our Theorem R9.1 at checkpoint 38, which they
  had not read).  The reviewer compared them line by line: the same set of clean
  bridges, the same additivity, the same lattice.  Theirs has an elementary interior
  estimate ours lacks; ours has the coboundary for all bridges, from which the sharper
  constants follow.
* One remark of theirs, marked "(not proved)", is false beyond the range they tested:
  a head and a tail of two beads clean every bridge up to 11 beads and fail from 12.
  Their script stops at 10 beads and tries equal lengths only — the reason it could see
  neither the failure nor that the minimum is 2 + 3.
* The coordinator checked the 12-bead counter-example from its coordinates with
  arithmetic that shares nothing with the reviewer's code, computed the determinant of
  the five-class certificate, read the proposition and Lemma 11.68 at their head, and
  re-ran the reviewer's script from a clean copy (identical apart from timings).
* **An error of the coordinator while recording it:** a one-line edit of a table row in
  the handoff used a replace on the remainder of the file and removed the terminator of
  the *next* row; a shell pipeline meant to display the result then hung.  Found by
  looking at the row ends before committing; repaired, and the table checked row by
  row.  Table rows are now edited by line, not by a search in the rest of the file.
* The audit result at `24a3c27` (cycle 38) was sent with the same message.

### Cycle 40 — the theory division's certificates on our instances, and what they showed about our own (SCI-REV-0012)

* Workstream P4 reported after forty-four minutes.  It had been asked to test one
  proposition of the theory division on thirteen of our instances.  It did (11 of 13),
  compared the two third-order penalty forms on 136 instances, reviewed three
  statements part by part — and, because it rebuilt our domains from scratch to do so,
  found something about our own measurement that nobody had looked for.
* **Our own error.**  Workstream P2 applied the product-space theorems on a greedily
  pruned product inside the clash-free domain, said so, and said that a certificate
  there says nothing about the rest.  It did not look where the minimum of the
  clash-free domain is.  In 14 of 40 non-product analyses it is outside the pruned
  product; for phenylalanine on the strand the "certified minimum" was 2–13 kcal/mol
  above it.  Our message SCI-MSG-0015, the digest and the status table carried
  "exact certificate … Phe on the strand" without the domain.  The coordinator
  recomputed the five strand cases from the stored grids before writing the
  correction; the numbers agree to the last digit.  Recorded as `DEAD_ENDS.md` SD45; a
  head note on the message; notes in the report, the status table, the physical
  applicability document and the frontier map.
* The review found one statement of the theory division false as written
  (Proposition 11.18c(a) extends a proposition whose completeness half needs a
  product); the coordinator checked the two-site counter-example by brute force.
* Two things beyond the brief are worth more than the brief: shares that depend on the
  state of the site (a dual solution of the pairwise relaxation — known mathematics,
  unattributed here because nothing was consulted), and the observation that pair
  shares and state shares enter one linear programme whose inputs are ball data and
  constants only — a certificate format with no enumeration on either side.
* A slip of the coordinator's while recording it: an assertion about the number of
  column separators in a status row was wrong and stopped the edit script after three
  of the files had been written; the remaining file was then edited by line.  Nothing
  was committed in between.

### Cycle 41 — benchmark B10 completed: a refuted prediction, and a misreading of our own number (SCI-MSG-0022)

* While four workstreams ran, the coordinator ran the part of benchmark B10 that had
  been designed at checkpoint 34 and never run: the variational, likelihood and
  least-`D_2` fits of one family on the 45 real instances.  A test on two instances
  first; the full run took two minutes.
* **The prediction failed for `D_2`.**  B10 had predicted that fits "can differ by orders
  of magnitude in `e^{D_2}`".  They differ by at most 0.34 nats; the root-mean-square
  remainder predicts `D_2` within a factor 2.5; the benchmark's own refutation criterion
  is met.  The prediction holds for the floor (`D_∞`: up to 3.2 nats between fits).
  Hypothesis H11 was demoted in `BENCHMARK_DESIGN.md`, not rewritten.
* **What the run showed instead** came from putting its numbers next to those of
  addendum A17 (6): independent residues fitted to the solvated energy are hundreds to
  thousands of times closer in `D_2` than the vacuum force field that part (6) had used
  as "the" model for serine.  An analysis of variance by order gave the reason in one
  line: the solvent term cancels 97 % of the pair variance of the vacuum energy on
  strand and PPII.  The large prices of part (6) for polar side chains were prices of
  a bad split.
* **A misreading of our own record, caught while writing the message.**  The status
  table compresses a finding of checkpoint 36 to "RMS error under the surrogate
  1.66 → 1.20 k_BT while D_2 goes 16 → 45".  In version 2 of the frameworks document
  (cycle 38) and in the first draft of SCI-MSG-0022 the coordinator read the arrow as
  "before and after a fit"; the addendum says "between two and six residues", for one
  unfitted model.  Both texts were corrected before the message was sent (the
  frameworks document had been pushed with the wrong reading for ninety minutes; the
  correction is marked in place).  The compressed status line now carries the words
  "with chain length".
* The self-consistent least-squares iteration named in the benchmark's design turned
  out to be the variational fit (same stationarity conditions) and not to converge on
  25 of 70 cases; noted, not pursued.

### Cycle 42 — the Lean files of workstream L4, and a report the coordinator did not adopt (SCI-MSG-0023)

* Workstream L4 reported after fifty-eight minutes: three Lean files, 176 theorems, all
  compiling without a warning.  Everything the brief asked for is formal, including the
  two-point bound the theory division had requested and the remainder identity we had
  asked the theory division to check — done by ourselves in the end, and withdrawn as a
  request.
* **The formalisation found an improvement.**  Proving that the certificate's upper end
  follows from its hypotheses, the workstream noticed that `W(b, σ²) − b` is nonincreasing
  in `b`, so the two uses of `|r̄ − Er| ≤ η` need not both go the unfavourable way: the
  floor width can be `r̄ − η − lo`.  The coordinator re-derived it in three lines and
  checked it on random laws.  The gain is negligible at the inputs of our certified
  instance and large only for deep floors.  It is the second time a formalisation in
  this division improved a statement (the first: the threshold of Theorem A, workstream
  L3).
* **A process matter.**  The workstream's file-writing tool declined to create its
  report file ("return findings as text").  The workstream generated the report with a
  script instead, then — when a second generation was denied by the permission system —
  stopped and flagged both facts in its hand-back and its notes, offering the
  coordinator the choice of regenerating, patching or removing the file.  The
  coordinator did none of the first two: running the generator would have been doing
  for the sub-task what it had been refused.  The generated file, the generator and its
  template were copied outside the repository unchanged and taken out of the working
  tree; nothing of them is committed.  The coordinator wrote the report from the
  hand-back, the notes and its own compilation and reading of the files, and told the
  two running workstreams not to work around such a refusal.  The research owner is
  told in the session's summary.
* What the coordinator checked: all three files compiled (exit 0, 96 axiom lines); 15
  theorem statements and 7 definitions read; the imported theory file compared between
  the two commits.
* **The third crossing.**  The fetch before the commit showed the theory division's
  seventeenth checkpoint (02:54 UTC, four minutes after L4's last run).  It contains
  their own machine check of the remainder identity — our request P3-T1, which the
  message being written called "withdrawn, done by us".  The message was rewritten
  before it was sent: THY-RES-0010 read in full, their Lean file read statement by
  statement next to ours and a copy compiled; the two agree, with small differences in
  hypotheses in both directions (their `hc0` is redundant; their bound is stated per
  target).  Two formalisations by two authors in the same hour are a stronger check
  than either, and that is what the message now says.  The rule "fetch, read, then
  write the commit message" caught this; the sync row written before the fetch result
  was looked at said "both unchanged" and was replaced.
* Their checkpoint also answers six of our messages (the prior-art review found a real
  gap in their theorem, which they closed and machine-checked), corrects one lemma of
  ours (adjacency of empty boxes, SCI-MSG-0005 §2.5), and brings their own referee's
  verdict on workstream Y, which does not contain the slope dependence that our R10
  found.  Their sampler for the sandwich (Proposition 11.113) was given to workstream
  P6 the same minute.  The answer to the rest is the next cycle.

### Cycle 43 — the theory division's seventeenth checkpoint answered as far as reading goes (SCI-RES-0011)

* Read in full: THY-RES-0010 and their referee's report R11 on workstream Y.  Launched
  on reading: a review workstream (R12) for the six statements they ask us to review,
  and a replication of their audit at the new head; their sampler for the sandwich
  went to workstream P6 as an extra item.
* **Two referees, one result, one difference.**  R11 and our R10 were written with own
  code and without sight of each other.  They report the same wrong sentence with the
  same two weights, the same artefact, the same unconverged iterate, the same
  truncated scan, and upper ends that agree to four digits.  R11 made a finding of
  what R10 only noted in passing (the upper halves of the brackets are not cost
  statements at bounded accuracy) — R10 should have; R10 looked at other slopes, which
  R11 lists as not checked, and found the reversal.  Neither alone would have given
  the section its two caveats.
* **A lemma of ours was false** (adjacency of boxes; SCI-MSG-0005 §2.5): the theory
  division found it while formalising our certificate — an empty box satisfies the
  criterion and contains nothing.  Soundness used the true direction only.  Linked
  correction in SCI-RES-0011 §4, head note on the message, `DEAD_ENDS.md` SD46.  It is
  the second statement of ours this session that a formalisation, not a referee,
  caught (the first: a remark on compensation at the ends of the window, by our own
  workstream L3).
* A bibliographic update: Block and Shetty's preprint is in the proceedings of COLT
  2026 (search result and proceedings page title; the published version not opened).
* One sentence of the first draft claimed to know why `545` and `544` differ ("a
  rounding convention"); nothing read supports that, and it was replaced by what their
  message says.

### Cycle 44 — a sentence of two hours ago corrected: the floor has its own fit

* SCI-MSG-0022 and addendum A17 (12) said that the floor "is the one no fit controls".
  Writing down the least-`D_p` objective to see what a floor-targeted fit would be
  showed that it is convex in the natural parameters for every `p > 1` — a log-sum-exp
  of affine functions plus a log-partition function — so the floor-optimal fit is the
  limit `p → ∞` of a family of convex programmes.  (The same line shows that the
  least-`D_2` fit, which both texts called non-convex, is convex.)  Computed by
  continuation in `p` on the 40 instances with at most 59 049 states: the floor falls
  to 13.5 % of the least-`D_2` fit's in the median.  Head note on the message, item 24
  in the addendum; to be mentioned in the next message to the theory division.
* A first run stopped on an assertion (an ordering of optimal values that holds only up
  to the optimiser's tolerance when the family contains the truth exactly); its partial
  log was discarded, the tolerance stated, and the cited log is from the second run,
  which reached its last line.
* The lesson is the one of `DEAD_ENDS.md` SD43 in small: "no X does Y" was written after
  trying four X.

### Cycle 45 — the pruned-domain finding traced into our other results

* After workstream P4's finding (the pruned product can miss the minimum of the
  clash-free domain), the coordinator checked where else the pruned products were used.
  Workstream P3 says "everything is on P2's pruned product": its valine, leucine and
  serine instances are full products — the twenty-residue certificate among them — but
  its rows for phenylalanine, lysine and the heteropolymer are certified statements
  about a sub-domain.  SCI-MSG-0020 quotes three such numbers.  Head notes added to the
  message and to the report; `DEAD_ENDS.md` SD45 extended.  Benchmark B10 and addendum
  A17 (6), (9)–(12) use product-domain instances only, except the second batch of
  A17 (6) (29 instances on clash-free non-product domains, by masks, not pruned
  products) — not affected.
* The handoff's "Resume here" section was rewritten as a current-state block; the open
  problems and the frontier map were brought up to date.

### Cycle 46 — while three workstreams ran: the audit at `9408e33`, charged side chains, and two samplers that disagreed by two standard errors

**Audit.**  The theory division's `scripts/audit_all.sh` at `9408e33`, unmodified, in a
scratch export: `AUDIT PASSED` — 69 Lean files, 37 543 lines, 8627 jobs, 4015
declarations, 504 headline theorems, 435 mutations (434 caught, one expected pass), 136
baseline runs: the figures of their status file (`INDEPENDENT_VALIDATION.md` §1.7).

**Charged and aromatic side chains (addendum A17 (12), item 25).**  The split finding of
benchmark B10 on the 29 non-product instances: for poly-lysine the vacuum force field
is `11–169` nats from the solvated ensemble in `D_2` and independent residues on the
clash-free domain are within `0.023`.  One exception, phenylalanine on PPII, where
neither independent residues nor a nearest-neighbour chain is close (`0.33` at six
residues).  *The reading was tested before it was written down:* PPII has three
residues per turn, so the guess was the `i, i + 3` contact; pair tables at one sequence
separation at a time (`b10_split_phe_pairs.py`) gave `0.007` for separation 3 alone and
no gain for separations 1 and 2 alone.  *Attribution:* while writing this the
coordinator found that workstream P2 had stated the split dependence for class
constants (SCI-MSG-0015 §2) and that item 22 and SCI-MSG-0022 had not said so; both
now do.

**Two samplers.**  Workstream P6's interim notes put the theory division's sandwich
sampler at `518.262414 ± 0.000005` for the twenty-residue instance; the coordinator's
fitted chain model had given `518.262573 ± 0.000075` (4 000 samples).  Two new seeds with
40 000 samples each (`beyond_enumeration_recheck_V20.py`): `518.262443 ± 0.000024` and
`518.262457 ± 0.000025` — the old value was a fluctuation of 1.6 of its standard errors,
and all three are inside the certified bracket except the old one; but all three are
*above* the sandwich sampler's two values (combined 2.3 standard errors, probability
about 0.02).  Checked: the two energy functions agree to `4·10⁻¹²` on 400 states;
both samplers against exact enumeration at twelve residues with millions of samples
(`sampler_precision_check.py`) — the chain sampler's estimate is off by
`(+1.5 ± 1.8)·10⁻⁶`, the band sampler with the rejection step by `(+0.9 ± 3.4)·10⁻⁶`, site
and neighbour-pair frequencies of both at `rms z ≈ 1`; so neither is biased at the
`4·10⁻⁶` level there.  A long run of the chain model at twenty residues (600 000 samples)
is in progress to decide between a fluctuation and something that appears only at
twenty.  *Rule kept:* the discrepancy is recorded before it is resolved.

**A by-product prepared, not yet published:** from a certified sandwich one reads off
certified *populations* (`certified_populations.py`): for an event `A`,
`P(A) ∈ [Z₊(A)/(Z₊(A) + Z₋(Aᶜ)), Z₋(A)/(Z₋(A) + Z₊(Aᶜ))]`, sharp for the sandwich; validated
on 1 452 exact populations (no violation); held back until workstream P6's sandwich,
on which it rests, has been read and checked.


### Cycle 47 — workstream P5 read, checked and published: the compact case (SCI-MSG-0024)

**What came back.**  The route the coordinator had announced for the helix — keep kernel
sums over neutral groups signed — is closed, by a measurement made before anything was
built (the brief had made the third step conditional on the first) and then by a
theorem: Born radii do not depend on the charges, so a bound that never looks at a sign
is a bound for every sign pattern, and sign-reversed versions of the real instances
have remainders 16–153 times the true one at orders 3–5.  The workstream then did what
the brief had not asked: it ran workstream P3's unchanged pipeline at order 6 with site
penalties on the helix, a combination P3 had not run, and obtained certificates up to
thirty residues.  P3's negative statement ("fails at every affordable order") was about
the *constant* bound; the lesson of its own extended-backbone results — the floor must
be a function — had not been applied to the case where it had given up.

**What the coordinator did before adopting it.**  Read the report in full; re-derived
the four statements; wrote an independent computation for the smallest instance (the
kernel from the table-free path, own inclusion–exclusion, own sign search) — the first
attempt, 400 random sign patterns, reached only 3.8, 0.23, 0.011 against the
workstream's 8.68, 0.68, 0.037, and its patterns are not stored; a local ascent on the
quadratic form of the remainder then found exactly the workstream's three values.
Rebuilt one certificate through another workstream's driver.  One slip found in a
statement (the definition of `k` in Theorem 9(i)); two wordings qualified.  The
citations of the report's prior-art section that the coordinator could check were
checked through PubMed (three records of Gaillard and Simonson; one of them new to
us), the rest are marked as unverified.

**Consequences recorded.**  `DEAD_ENDS.md` SD47 (our own announced route);
`OPEN_PROBLEMS.md` D6 (what remains open: compact ensembles with real side-chain
entropy; order 6; serine); status S57; requests P5-T1…T3, P5-E1, P5-E2.  *Judgement:*
the pair "impossibility for an explicit class of analyses, by exact evaluation on real
instances" + "a certificate all the same" is the most complete answer the division has
given to a question it posed itself.

### Cycle 48 — workstream R12 read, checked and published: the review the theory division asked for (SCI-REV-0013); and the engineering division's first contact

**R12.**  No critical finding; two major, both in sentences the theory division had
itself labelled as a sketch or as quoted from memory.  (M1) Proposition 11.18e(b) —
"randomised algorithms without a hint need the ball too" — is false as written: a
bound may scale with the observed values, so a few random evaluations give a valid
(and useless) finite bound; the question that remains is the prescribed-width one.
(M2) The "necessary" count of Proposition 11.113(d) is too large by `e^Δ`.  *The
coordinator had derived M2's count before reading the report* (while looking at the
workstream's notes during cycle 46: `Z = Z₊(1 + aw)`, relative accuracy `ε`, `Var W ≤
w(1 − w)`, worst mean `1/(a + 2)`, count `2 ln(2/δ) sinh²(Δ/2)/ε²`), so the two
derivations are independent; M1's pairing argument was re-derived and recomputed
with separate code, the workstream's Lean file compiled, two scripts re-run clean.

**Engineering.**  The fetch before the commit of SCI-MSG-0024 showed the engineering
branch at `c2ad4f8`: its fourth checkpoint and its first contact with this branch.
Five linked corrections of its record, each found by our reviews SCI-REV-0007 and
SCI-REV-0008 and verified there; all 585 cases of its literal runs repeated with an
exact sampler (no conclusion changes); our separation table reproduced to every
digit; every request of ours triaged.  *And one finding of theirs turned against
us:* they measured the defect of numpy's binomial sampler from `10¹⁵` trials on, in the
variance before the mean, where our review had said "nothing detected at `n ≤ 10¹⁶`".
The coordinator re-measured with ten times the draws
(`numpy_binomial_variance_check.py`): defective from `5·10¹⁴` on (`−0.87 %` in the
variance, `−0.03 %` in the mean at mean 500), nothing at `10¹⁴`, `2·10¹⁴`, nor at `2⁵⁰`, `2⁵²`.
**Our own "corrected" sampler in workstream R6 switches to a Poisson draw only above
`2⁵⁰ = 1.126·10¹⁵`** — so its re-run still used the defective routine in a window.  A
linked correction of SCI-REV-0007 goes out with the reply (SCI-RES-0012); a re-run of
R6's campaigns with the guard lowered is to be made.

### Cycle 49 — workstream P6 read, checked and published (SCI-MSG-0025); certified populations (addendum A17 (13))

**What came back.**  More than was asked: besides the pair form (the brief) the
workstream proved and validated shares to triples, with which order four suffices at
twenty residues, ran the theory division's sampler on four sandwiches, and reached
thirty residues.  Its own verdict on the title question is honest in the order it
found things: "with pair shares a lower order does not suffice" (0.31 nats), then
"with triples it does" (0.055).  It also found, against the brief's expectation, that
the pair form rescues poly-leucine on the helix at order 5 — the frozen-ensemble
mechanism that workstream P5 found independently at order 6 with site penalties.

**What the coordinator did.**  Read the report in full; re-derived the three lemmas;
checked them on random data with own code; rebuilt the triple form on one enumerated
instance with separate model code — the first comparison "failed" by 12 % and the
coordinator's first explanation (a rounding allowance) was wrong: the difference is
the same 0.0013 nats for all three forms and is P3's reduction of the evaluated
three-site terms to pair tables, which a brute-force model does not need; the label
in the script was corrected before the log was kept.  Re-ran the twenty-residue
brackets from a copy of the directory.  Tested both samplers against enumeration to
`3·10⁻⁶` after two estimates of the same number had disagreed at two standard errors
(cycle 46); with 684 000 samples the disagreement is `1.5·10⁻⁵` nats, still 2.1 standard
errors, and is left recorded as open.

**The coordinator's own addition** (A17 (13)): a sandwich bounds the partition sum of
every event from both sides, hence every population, sharply — by restricted transfer
matrices, with no sampling and no evaluation.  Checked on 1 542 exact populations.
At twenty residues all sixty rotamer populations are certified within 1.2 %; with the
site form at order 4 they are not certified at all, for the same reason the pair form
wins: the minor population of a site consists of assignments that leave the anchor
at one site.  A written sentence was wrong before it went out ("the sampled intervals
lie inside the deterministic ones" — one of three overlaps instead) and was corrected
against the numbers.

**Started:** the pair form on workstream P5's cached helix balls (twenty and thirty
residues), which neither workstream ran — `helix_pair_form.py`; at twenty residues the
site form reproduces P5's bracket digit for digit and the pair form gives
`[593.2974, 593.3134]`, 0.016 nats where the site form gives 0.63.

### Cycle 50 — the engineering division answered; two corrections of our own review; a correction that had never been exercised (SCI-RES-0012)

The engineering division's fourth checkpoint was read in the parts addressed to us
(ENG-MSG-0004, ENG-RES-0013 in full).  It is the first time another division has
*replicated a result of ours* (the separation table of SCI-REV-0007, 72 numbers, from
the definitions, with their own evaluator) and the first time one has *corrected a
finding of ours by verifying it*: they measured the variance as well as the mean of
numpy's binomial sampler, on a finer grid of `n`.

**What the coordinator did with it.**  Re-measured (ten times their draws): defective
from `5·10¹⁴` trials on, clean at `2·10¹⁴` and at powers of two up to `2⁵²`.  Then asked the
question their finding raises about us: the guard of workstream R6's corrected
sampler starts at `2⁵⁰`, so was our re-run exposed in the window below it?  A re-run of
the eight campaigns with the guard lowered and a counter on the branch gave the
answer — and a second, unexpected one: **the counter never moved, in the window or
above it.**  The corrected branch had never been taken in any campaign; neither had
the first pass been exposed.  The reason is structural (classes are drawn in order of
decreasing probability, so every conditional probability is at least one over the
number of classes) and had not been noticed by the workstream or by the coordinator
when SCI-REV-0007 was published with the words "re-run with a corrected one (same
outcome)".  *Recorded as SD48:* two checks with the same blind spot are one check; a
correction is not validated by a run that never exercises it.

**A denied command, for the record.**  While preparing the scratch copy for that
re-run a compound shell command containing a wildcard deletion inside a directory the
checker could not resolve was refused by the environment's safety check.  Nothing was
deleted and the removal was not attempted another way; the copy was made in a fresh
directory instead and the smoke-test output was sent to a directory of its own.

### Cycle 51 — the theory division's eighteenth checkpoint; the thirty-residue helix; a commit message that said "unchanged" when it was not

**The mistake first.**  The fetch before the commit of SCI-RES-0012 returned a new
theory head (`63e36f7`); the fetch, the sync row, the commit and the push were one
command, and the row and the commit message say "both unchanged".  Seen on reading
the output.  A pushed message is not rewritten: the next commit is the linked
correction (`7476f5f`), with SD49 and the rule that the fetch is a command of its own.

**Their checkpoint** (THY-RES-0011, read in full): five of our reviews applied, with
verifications that went beyond ours (Theorem R9.1 on `2.5·10⁹` ordered pairs and an
exact volume; the reversal of workstream Y recomputed with their own code and with
blocks of one site, which do not show it).  Seven Lean files of ours are now part of
their audited library.  Their four requests were turned into work at once: a referee
workstream (R13: the rate of their level recursion; how our reviews were applied), a
measurement workstream (P7: shares after branching), one request already answered by
a message that had crossed (the compact case by neutral groups: SCI-MSG-0024), one
that is ours and waits for an enumeration the engineering division has accepted.
*A sentence of the coordinator's draft reply was wrong and was caught against the
table before it went out:* "the grouped constants fall with the order no faster than
the truth" — the measured ratios to the truth fall (18.7, 11.2, 8.1, 6.0), i.e. the
grouped constants fall a little *faster* than the truth; rewritten with the numbers.

**The synthesis only a coordinator could make** (addendum A17 (14)).  Workstream P5
had certified the leucine helix with site penalties at order 6 and left its
evaluations cached; workstream P6 had proved the pair form and never ran it beyond
sixteen residues; each had been told to stay in its directory.  A driver of sixty
lines applies the one to the other: at thirty residues the site form reproduces P5's
bracket in every digit and the pair form gives 0.033 nats where the site form gives
0.730 — without a random number and without a new evaluation.  The sampler's point
estimate agrees with the uncertified chain estimate of cycle 40 to `4·10⁻⁶`.  A request
to the engineering division (order 7) could be withdrawn the same hour.

### Cycle 52 — the case nobody had run: a compact ensemble that is not frozen; a law in one line; a novelty claim checked against our own workstream first

The re-ranked handoff of cycle 51 named one place "where the certificate can still
fail, and nobody has run it".  It took eight seconds on workstream P6's caches
(addendum A17 (15)).  **Result:** for serine on the helix — 55 % of the side chains
off the anchor — the envelope `Σ_{T ⊆ S(x)} ĉ_T`, which bounds every share allocation
from below, gives 0.013, 0.063, 0.27 nats at four, five, six residues at order 4.
Nothing in the allocation rescues it; the question "better shares?" (open problem
D9(a)) is answered where it decides.

**The law.**  Looking at the table, each level of shares gained the same factor 1.8,
which is `1/p`.  The identity behind it is one line (the `k`-th factorial moment of a
binomial): the mean `k`-share penalty is `p^k Γ_m`, so the bracket is `2 p^k Γ_m`; a
second script checks it on all 52 enumerated brackets — within 0.97–1.09 wherever
the bracket is narrow, wrong by up to 2.6 where it is 5–16 nats.

**A claim of novelty checked before it was written down.**  The first draft of the
addendum presented the law as new.  A search of our own workstream report before
committing showed that P6 had stated it for sites and pairs ("the gain is the
reciprocal of the fraction of sites off the anchor … `Γ_m p` against `Γ_m p²`"), had
measured `p = 0.55` for Ser₅ on the helix, and had concluded that the polar helices
are "helped by a factor below two or left useless".  The addendum now says so: what
this part adds is the envelope (every allocation), the general `k`, the quantitative
check, and the growth with length.  *Second correction of the same draft:* "every
sign-blind bound is only 3.4–19 times the truth" misread P5 — that is the proven
*floor* of the sign-blind class for serine, not a bound anyone has; rewritten.  *Third:*
the size of the order-5 ball at twelve residues was guessed as `3·10⁶`; computed, it is
`4.8·10⁵` (if interior sites keep six states) — i.e. the open run is affordable here.

### Cycle 53 — a rule used as a prediction; the certificate reaches a mobile compact ensemble; the rule broken on purpose; the frontier renamed

**Starting point.**  Cycle 52 had concluded "for a compact ensemble with real side-chain
entropy the certificate does not reach beyond enumeration at order 4".  The qualifier
"at order 4" was the whole content: the certified constants of serine on a twelve-residue
helix, computed in seconds by closed form, fall 24- and 31-fold per order
(`Γ₄, Γ₅, Γ₆ = 5.4, 0.23, 0.0073 k_BT`) — leucine's fall 5–8-fold.  With the rule of cycle 52
that predicts a bracket of 0.07–0.24 nats at order 5 from a ball of `4.8·10⁵`
evaluations: four minutes.  The guessed ball size of cycle 52's draft (`3·10⁶`) would
have discouraged the run; the computed one did not.

**The prediction was printed before the bracket** (the script's own order of steps), and
it was too optimistic by a constant 0.13 nats in all three share forms.  That constant
was the thing part (15) had already named: P3's reduction of evaluated three- and
four-site terms to pair tables.  The transfer matrix sums an array over a window, so
any function inside a window is free; a model class of ninety lines keeps those
terms exact (`window_model.py`).  Result: 0.211 → 0.137 → 0.094 → 0.077 nats as the band
goes 6 → 7 → 8 (triple shares, order 5).  **A non-frozen compact ensemble of `4.9·10⁹`
assignments is certified below 0.1 nats without sampling.**

**A claim of novelty checked against our own reports — again.**  Before writing "the
observation", a search of P5's report for "window" found its §3.3: P5 had written the
exact banded model for in-window evaluated terms, in a route it abandoned (bounding
everything outside the window by constants).  The addendum credits it and says what
is different (fixed order, nothing bounded by a constant outside the window).

**The check that checked itself.**  The enumeration check of the new model class
reported 17–21 kcal/mol between the model energies and a "direct evaluation" while its
three other tests passed to `10⁻¹³`.  Three passing tests against one failing one
pointed at the failing test: its direct evaluation counted the constant `c₀` twice.
Kept in the addendum as an error of the check.

**Breaking the rule on purpose.**  A first-order rule should fail somewhere, and the
table said where to look: leucine at order 4 has a predicted triple-form bracket of
0.0006 nats with `Γ₄ = 316 k_BT`.  Run (enumerable, 4 096 states): 187 nats.  The floor's
4 000 exact samples are a single state with all twelve side chains flipped.  The
lemma behind the rule (two-sided, with `e^A` on the floor's side only) says exactly
this, and says one thing more that the run confirms: the *ceiling* cannot
delocalise — the lower end of that useless bracket is within 0.0008 nats of the exact
value.  A measurement explains why no cheap floor exists far from the anchor: the
true solvent term varies by 4 kcal/mol over all states while the certified constants
of orders 1 and 2 are thousands; the ensemble is frozen by the known part and the
bound cannot know the unknown part is small.

**What the table renamed.**  For twelve residues on the helix: serine, leucine,
phenylalanine in reach at order 5; lysine and the patterned sequence out of reach at
every affordable order (first-order estimates of 1–10 nats at order 6).  The ratio of
certified constant to true remainder is the same for all of them (10²–10³); the truth
is twenty times larger per subset for lysine.  "The compact case" of the last four
cycles is therefore the wrong name for the open problem; it is "the charged case".
Workstream P8 was briefed on it within the hour.  A referee workstream (R14) on the
coordinator's own four addenda, including a search for sandwich violations by
optimisation rather than sampling, was briefed and launched at 05:59 UTC — and
**terminated within two minutes by a platform safeguard of the model provider**,
before it had reviewed anything.  The notice asks that it be passed to the user and
that the agent's work not be done in its place.  The coordinator did neither
relaunch it with other words nor substitute for it: the four addenda are recorded
everywhere as unrefereed, the message to the other divisions says so in plain words
and invites their checks, and the decision is left to the research owner.

**Operational.**  At 05:26 UTC a Lean process of workstream P7 (an optional
`decide +kernel` attempt, 11.9 GB) exhausted the shared memory budget; the kernel
killed it and, with it, the coordinator's order-6 run (965 MB), 20 minutes into a
35-minute evaluation.  P7 reported it unprompted within two minutes, with the process
number; the run was restarted; P7 corrected two statements of its own first report
(a limit it said was in force was not yet; a measurement it quoted had not been
made).  Nothing was lost but time.  The first run of the reach table was stopped by
the coordinator after two rows (a fixed band of six was wrong for two-state sites)
and re-run with the widest affordable band per peptide; the partial log was not
kept in the repository.

### Cycle 54 — three hand-backs in an hour: a rate machine-checked, a question answered with certificates, a referee that never ran

**R13** (the theory division's request (a)).  The workstream did more than referee the
rate `τ_k − h ≤ c₁/(k + c₂)`: it formalised it — 941 lines of Lean on top of their three
lemmas, for the exact recursion of the cube at every slope, and found on the way that
the same rate holds for the sequence at accuracy zero (ours).  The coordinator
re-derived statement (a) on paper before reading the workstream's derivation (the
slope gains `B/h − 1` per level on a range `h/j`; `J` levels and one macro step multiply
`B` by `Ja/(Ja + h)`; in the variable `d = h/(B − h)` the gain per level exceeds `κ`),
compiled both files, and recomputed the one major finding with code written from the
statement: Proposition 11.117(b) of the theory report lost the word "symmetric" when
it adopted our R10.1 and is false without it — on two points with a one-sided
envelope the ratio to the claimed second-order term is `0.24999`, not 1.  The check of
how our five reviews were applied turned up **five slips of our own**, two of them
pointed out by the theory division itself; all five are corrected by linked notes on
the four messages concerned (`DEAD_ENDS.md` SD54–SD57).  One of them (a sentence of
SCI-REV-0012 that compressed our report wrongly) had been copied by the theory
division into a theorem's wording: an error of a reviewer propagates.

**P7** (their request (c)).  "Are the gap instances certified by shares after branching
on one site?" — yes for four of five analyses, at depth two for the fifth; and the
format they were not sure was worth a checker is already a term of their own
certificate type: thirteen real certificates were accepted by their `verify`.  The
coordinator wrote a second checker from the report's description of the format (not
from the workstream's code): all nine tree certificates accepted, two controls each
rejected, minima by brute force, the four gaps by an own linear programme.  The
workstream's own list of errors is the longest of any so far and the most useful
(an unmeasured number reported as measured; a promise about limits broken within a
minute; a memory accident with collateral damage) — each reported by itself.

**R14** (the referee of the coordinator's own addenda) never ran: cycle 53.  The three
messages of this cycle therefore differ in standing, and say so: SCI-REV-0014 and
SCI-RES-0014 are workstream results re-checked by the coordinator; SCI-MSG-0026 is the
coordinator's result checked by the coordinator.

**The certificate, final numbers of the day.**  Serine on the twelve-residue helix at
order 6 with a window of nine sites: `ln Z ∈ [227.362266, 227.373868]`, 0.0116 nats,
from 0.088 % of the assignments; with P3's reductions the same evaluations give 0.093.
An attempt to reduce the terms outside the window less drastically (to their largest
sub-tuple that fits) gained under 2 % — and the sentence "pointwise tighter than P3's
rule", written before the check ran, was false for one of the two rules tried
(22 725 enumerated states said so) and true by construction only for the other.

**An upstream head moved under three pending publications.**  The fetch — a command
of its own, as the rule of cycle 51 demands — showed the engineering division at a
new head (`ce71724`, their checkpoint 5) while SCI-MSG-0026, SCI-REV-0014 and
SCI-RES-0014 were waiting for a last reproduction check.  Nothing was staged.  Read:
their ENG-MSG-0005 in full and the parts of ENG-RES-0014 that answer us (a bound for
instances that are not products; the convergence control at the two largest sizes),
and the diff of their status file.  They adopted our tree format and moved the
stand-alone checker to the front of their queue without having read its
specification — so the answer (SCI-RES-0015) is mostly a reading order: the smallest
checker first (shares at the leaves: integers only, nine test vectors), the sandwich
certificate second, its amendment third and with a caution that it is unrefereed.
One request of ours that they still carried as "on hold" is withdrawn in so many
words.  Their arguments for the bound "have been checked by nobody else", they
write; the coordinator read the step that carries it and offered a referee
workstream rather than pretend a reading is a review.

**The lemma, machine-checked.**  With no referee for the coordinator's own addenda,
the one part of them that can be checked without a reader was: Lemma A17.16 is now
228 lines of Lean on Mathlib alone (`pi_inference/lean/SandwichCost.lean`), compiled at
the second attempt — the first failed in the two derivative computations of the
Taylor bound `e^a ≤ 1 + a + (a²/2)e^a` and nowhere else.  The sharp constant `½` on the
floor's side needed a monotonicity argument (`e^a s²/2 − (e^s − 1 − s)` is nondecreasing
on `[0, a]`); on the ceiling's side `1 + b + b²/2 ≤ e^b` and one line of algebra
suffice — the asymmetry of the lemma shows even in its proof.  A machine check says
the statement is true; that it is the statement the addendum uses, and that the
sandwiches of the addendum satisfy its hypotheses, still needs a reader.

### Cycle 55 — the theory division's nineteenth checkpoint arrives under five pending messages; their envelope sampler and our window terms attack the same slack; an onset corrected

**A second head moved before the commit.**  With SCI-RES-0015 written and everything
ready to stage, the fetch — again a command of its own — showed the theory division at
`f7df44f`, its nineteenth checkpoint.  Nothing was staged.  THY-RES-0012 was read in
full (518 lines) and the diff of their status file; nothing else of theirs yet.

**What it is.**  Our review SCI-REV-0013 applied to the letter — both major findings
verified by derivations and harness tests of their own before they were applied, all
eleven minor ones, linked corrections of two of their messages, a dead end recorded on
their side for the sentence that had carried a "[P-sketch]" label on a statement about
all randomised algorithms.  Then more than was asked: the share lemmas of workstream P6
machine-checked at every level and for any window; workstream P5's two lemmas
machine-checked by an induction that replaces our regrouping argument; and two paper
statements that bear directly on the certificates, unrefereed by their own account.
*Proposition 11.113a:* with a computable inner sandwich `e₋ ≤ E ≤ e₊` between the
solvable models, propose from the outer sampler and evaluate the energy only with
probability `ρ`; in evaluations the price is the envelope's, whatever the share form.
*Proposition 11.18f:* the cost of a penalty depends on the law of the changed set
only; the upper end of the bracket is convex in the allocation, the lower end concave;
charge each constant to its least probable sub-pattern.

**Where it meets what was waiting to be published.**  Three places, and in each the two
divisions had worked on the same thing in the same two hours without knowing it.
(i) Their `level_window_cover` proves, for any window, what our two-window triple form
uses.  (ii) Their exact exponential moment `Σ_S P(S)(e^{pen(S)} − 1)` and our Lemma
A17.16 are one statement at two depths; their "the two ends want different
allocations" is our "a ceiling never delocalises, a floor can", and the leucine helix
at order 4 is the instance where the difference is everything.  (iii) Their nested
sampler and our exact window terms remove the same slack — the reduction of evaluated
terms and the gap between a share form and the envelope — one with sampling, one
without; they compose.  SCI-MSG-0026 was left as written, with a dated note under its
header that says so; SCI-RES-0016 says where the two meet and gives them the one fact
they asked for and did not have: how unequal the off-anchor frequencies are (very, on
the frozen helices; not at all for serine).

**A correction of ours.**  SCI-RES-0013 §3 placed the onset of the binomial sampler's
defect "between `3·10¹⁴` and `5·10¹⁴`" by reading one cell of their first scan as clean.
The cell had `z = −2.6` under a threshold of 5; with four times the draws and three
seeds it is `z = −8`.  The onset is between `2·10¹⁴` and `2.5·10¹⁴`.  What we had measured
ourselves stands; what we had inferred from a table of theirs did not.  Linked
correction: SCI-RES-0016 §4, a head note on SCI-RES-0013, notes on digest item 55 and
finding S61.  *Rule kept from it:* an interval narrowed with somebody else's "clean"
cell is their interval, and is quoted with their threshold and their number of draws.

**A first reading, said to be one.**  They asked most for "any error in §1.1(b′)(i)".
The coordinator read the argument in the message (not the proposition in the report):
it holds — a monotone limit in the depth of the needle — and "attained" carries one
condition they do not state: for `ln Z` the bracket returned after a skipped state
must be at least `ln 2` wide, or two equal states fail with probability `2δ`.  Sent as a
first reading ahead of a review, in those words.

**Accepted, not done:** the nested sampler on our sandwiches (theirs to propose, ours
to run: an enumerated instance, twenty residues at order 4 with their stopping
condition, the serine helix); a review of four statements; the replication of their
audit at `f7df44f`; a test of their allocation rule on Leu₁₂.

### Cycle 56 — two statements of the theory division run on real instances; a sampler that works as stated and is helped by two small changes; a rule that is right for one end and breaks the other; the shares turn out to be the core of a convex game

**What was asked.**  THY-RES-0012 proposed a nested sampler (their Proposition 11.113a)
"for the science division's certificates", with a validation target and a stopping
condition, and an allocation rule (Proposition 11.18f) that they "have not tried on
your instances".  Both were run the same morning; the review of the statements
themselves went to workstream R15.

**The sampler.**  Built as they state it, with the envelope as inner sandwich.  Three
decisions were ours and are written into the script's docstring: the allowance for
the interpolant at a state (the sum of the absolute coefficients of the ball values:
a closed form checked against brute force), the treatment of ball states (the cached
value is both bounds: never evaluated again), and clipping the inner bounds into the
outer ones so that the nesting holds whatever the bookkeeping of allowances (it never
acted).  On two enumerated serine instances every identity holds to `3·10⁻¹⁴` and the
truth was inside all six kinds of bracket in 100 of 100 repetitions at three budgets.
At twenty residues their stopping condition — narrower than `4.3·10⁻³` from the same
1 200 evaluations — is met at `1.2·10⁻³`.

**What the run taught that the statement did not say.**  (i) With Hoeffding
half-widths the nested bound needs three events where the plain sampler needs one;
the gain is at most `0.88/E_q ρ`, and at the "balanced" number of proposals the nested
bracket is *wider* than the plain one unless `E_q ρ < 0.44` — on the two enumerated
rows it was.  (ii) `E_q ρ` is the ratio of two brackets we already had a law for:
`p^{m−k}`.  The expectation written into SCI-RES-0016 the hour before ("near one half
for mobile ensembles") was right at order 4 and wrong at order 5, where it is `0.20`;
it should have been written as the rule.  (iii) Writing `W = c + ρ(W_in − ½)` with
`c = β + ρ/2` known without evaluation halves the proposal term, and `c` hardly
varies (the centre of the envelope does not move against the outer sandwich).
(iv) Reading the empirical Bernstein inequality in its source — a fetch subagent
read Theorem 4 of Maurer and Pontil in the ar5iv rendering; workstream P6 had quoted
it "from memory, not used for any certified statement" — turned it from a number
printed for curiosity into the largest single gain of the morning: 2.3–3.5 on the
plain sampler, because the true energy sits in the middle of the envelope and the
sampled variable hardly varies.  With both changes: `2.7·10⁻⁴` nats at twenty residues
from 11 121 evaluations, and the serine helix of part (16) within `4.7·10⁻⁴` at
probability 0.95 from the order-5 ball — 25 times narrower than the order-6
certificate, from a ninth of its evaluations.  The point estimate agrees with the
uncertified estimate of two cycles ago to `8·10⁻⁶`.

**The allocation: a prediction, then a break, then the structure.**  Before running,
the expectation was written down (SCI-RES-0016): their rule should bring the site
form near the pair form on the frozen helix.  The enumeration said something
sharper.  The rule — every constant to the most frozen site of its subset — makes
the *ceiling* essentially exact at every order from 4 on (the mobile sites carry no
penalty at all), and at order 5 it *breaks the floor*: 8.6 nats where equal shares
give 3.2, because it puts `20 k_BT` on a site whose cheapest change costs `14`.  That is
Lemma A17.16 again — the floor's side is not first-order — and their own text says the
two ends want different allocations.  What repaired it was not a better heuristic but
the structure of the problem: `Γ(R) = Σ_{T⊆R} ĉ_T` is supermodular, so the site
allocations are the core of a convex game, its vertices are orderings (their formula
is the marginal vector), equal shares are the Shapley value, their rule is the greedy
vertex — and since `ln Z` of the floor is convex in the penalties with the floor's own
marginals as gradient, the best floor is a convex programme whose linear oracle is
their rule applied to the tilted marginals.  Frank–Wolfe: `0.0075` nats at order 5,
430 times below equal shares, below equal pair shares.  The greedy optimality is 60
lines of Lean, compiled at the first attempt.  A water-filling bound over the
single-change states says in advance when the site level cannot work at all.

**Process.**  Three runs at thirty residues were started and stopped within minutes
of each other — first for a budget that would have taken hours (one closed-form sum
costs seconds there), then for a band that did not match the run it was to be
compared with, then for a script edited after launch, then for a Gibbs check that
would have taken most of the hour.  Nothing was published from a stopped run; their
partial logs are outside the tree.  *Rule kept:* before a run of more than ten
minutes, write down its cost per step and what it will be compared with.

**A prediction written before its run (07:46 UTC, clock read).**  Serine on the helix at twenty
residues (`8.2·10¹⁵` assignments; `p = 0.514`, `βΓ₅ = 0.564`; reach table of part (16):
triple form with exact window terms `0.209` nats by the refined rule, ball
`3.96·10⁶`).  By the rules of this cycle the envelope bracket is `2p⁵Γ₅ ≈ 0.040` nats,
`E_q ρ ≈ 0.19`, and with 1 200 evaluations and 400 000 proposals the nested sampler
should give about `6·10⁻³` nats as stated (Hoeffding) and about `1·10⁻³` with one known
mean and the empirical Bernstein bound.  The run (`serine_helix_reach.py S20 5 7`, then
`nested_sampler.py S20 H 5 7 T window`) had not been started when this was written.

**The same morning, three things came back and one was improved by its referee.**
*Workstream R15* — the review the theory division had asked for — found nothing
false in their four statements and twelve conditions to add; among its additions, a
bound for the nested sampler with `t_f` in place of `2t_f` (two ends: the error of the
free part is affine in `E W_in`), which is never wider than the coordinator's
one-known-mean form when the half-widths are Hoeffding's.  The coordinator's form
had been written, run and tabulated two hours before; the script now carries all
three, and the tables say which wins where (two ends with Hoeffding, one known mean
with a variance-sensitive bound — the report did not check that case and says so).
R15 also reached, independently and on synthetic instances, the statement the
coordinator had reached on a real one: the best floor equalises `f − γ`, a
water-filling.  All seven of its scripts were re-run; the logs are identical.
*The closed form.*  Asking why the Frank–Wolfe optimum sat so close to a crude bound
led to the right bound: `e^{γ·s} ≥ 1 + Σ s_i(e^{γ_i} − 1)` gives
`ln Z(m₋) − ln Z(B) ≥ ln(1 + Σ p_i(e^{γ_i} − 1))` with the off-anchor *marginals*, and its
minimiser — each site charged what its rarity can pay — is a valid allocation on the
enumerated instance and beats 2 000 Frank–Wolfe steps.  At twenty residues the
Frank–Wolfe floor lands on that bound to six decimals.  *One more convex game.*  The
twenty-residue floor was ten times above the bound until the floating-point
allowance of workstream P3's models was recognised as the same kind of function of
the changed set and allocated by the same rule: the mobile sites had been paying
`0.005 k_BT` each for rounding errors of terms they are never part of.  What then
remains of the bracket, `0.0085` of `0.0087` nats, is P3's reduction of evaluated
terms — measured as the distance between the penalty-free minorant and majorant.
*The audit* of the theory division's nineteenth checkpoint passes on this machine.
*Workstream P8* handed back while all this was being written: a 1 700-line report on
the charged case whose summary says that lysine at twelve residues is now within
half a nat.  It is not read yet; nothing of it is claimed here.

**Process, continued.**  The scripts of this cycle were edited five times after
their first runs (the a-priori bound, its sharper form, the floating-point game, the
two-end bracket, a log message); every log that is committed was produced again
after the last edit of the code path it reports, and six partial logs of stopped
runs are outside the tree.  One time stamp was typed before the clock was read and
corrected a minute later.

**A head moved before the commit, for the third time today.**  The fetch — its own
command — showed the theory division at `9befefd`, its twentieth checkpoint, while
SCI-RES-0017 and SCI-REV-0015 were ready.  Nothing was staged.  THY-RES-0013 is
addressed to the engineering division (three nested levels; a certified third level
obtained by serving every rung with the candidate of smallest certified cost); its
last section is for us: they fetched our previous commit, reproduced the table behind
the major finding of SCI-REV-0014 and accept it, and offer their new section for
review.  Answered in SCI-RES-0018: the two pending messages go out unchanged with a
line in their headers; the review is accepted and not started.

### Cycle 57 — the charged case read and checked before it is published; a theorem tested with a family built to break it; a prediction for the sampler on lysine

**Reading.**  Workstream P8's report (1 695 lines) was read in full between
08:30 and 08:53 UTC (clock read at the end).  Its claim: workstream P3's cross bound
does carry the Gaussian factor, the slack is the merging of maxima over host
rotamers, and with the maximum taken state-wise (P3's own theorem; variant 'Sb')
plus a new statement about anchored hosts (Theorem AH; variant 'SAb') the constants
of Lys₁₂ fall from 689 / 145 / 23.4 to 34.0 / 2.40 / 0.136 `k_BT` at orders 4 / 5 / 6
and the certified bracket of Lys₁₂ on the helix at order 5 is 0.19 nats.

**Prediction for the nested sampler on Lys₁₂, written at 09:04 UTC (clock read),
before the run is started.**  Outer sandwich: triple form, band 7, 'SAb', `D ≈ 0.19`
nats.  The inner sandwich pays the envelope only, and P8's first-order estimate of
the envelope bracket is `2·10⁻⁵` nats, so `E_q ρ ≈ 10⁻⁴`: nearly nothing is left
for evaluations, and the width is the proposal term.  With `N_f = 400 000`
proposals and `N = 1 200` evaluations I expect: as stated by the theory division
(Hoeffding) about `2·10⁻³` nats; two-end form (Hoeffding) about `1·10⁻³`; with
empirical Bernstein half-widths about `4·10⁻⁴` if the standard deviation of `b`
under `q` is near 0.2; the plain sampler with the same 1 200 evaluations about
`0.015` (Hoeffding) and `0.01` (empirical Bernstein).  The point estimate should
agree with P8's uncertified reweighting estimate `517.1285 ± 0.0009`.  Cost: one
build of the band-7 models (a minute, 2.3 GB), about `2.3·10⁶` draws of the floor,
400 000 evaluations of 794 anchored tables, 1 200 evaluations of `g`.

**The prediction for Lys₁₂ against the run** (`nested_sampler_K12_H_m5_w7_T_window_SAb.log`,
finished 09:26 UTC).  Predicted: about `2·10⁻³` nats as stated, `1·10⁻³` two-end,
`4·10⁻⁴` with empirical Bernstein half-widths if the standard deviation of `b` were
0.2; envelope bracket `2·10⁻⁵`.  Measured: `1.88·10⁻³`, `0.95·10⁻³`, `2.2·10⁻⁴`
(the standard deviation of `b` is 0.097); envelope bracket `9·10⁻⁶`; point estimate
`517.128535` (P8's reweighting: `517.1285 ± 0.0009`).  **Not predicted:** only 19 of
the 400 000 proposals are accepted with probability `ρ`, so the run evaluated the
energy at 19 states, not 1 200, and the "plain sampler with the same number of
evaluations" in the log is a plain sampler with 19 — my two numbers for a plain
sampler with 1 200 evaluations were not tested.  The first attempt at this run was
stopped after sixteen minutes: workstream P3's band sampler recomputes the whole
transfer-matrix pass at every call, and the sampler calls it once per batch; with the
messages computed once the proposals take 14 seconds (identical output on Lys₅).

**Prediction for (LKSE)₃, written at 09:26 UTC (clock read), before the run.**
Outer sandwich: P8's, triple form, band 7, 'SAb', `[654.8638, 659.3505]`, `D = 4.49`
nats; P8's uncertified estimate `655.79 ± 0.09`, so `E_q W ≈ 0.017`.  The envelope
bracket is not known: the first-order estimate on Gibbs states is 0.013 nats, but
the floor's samples sit at nine side chains off the anchor, where the envelope is
several `k_BT`; my guess is 0.1 nats, i.e. `E_q ρ ≈ 0.003`, about 1 200 accepted
among 400 000 proposals.  Then: two-end form with empirical Bernstein about
`0.03–0.04` nats (proposal term; the variance of `b` near its mean 0.017); two-end
Hoeffding about 0.17; as stated about 0.34; plain sampler with 1 200 evaluations
about 1 nat (empirical Bernstein) and 2.7 (Hoeffding).  If the envelope bracket is
above one nat the guess fails and the evaluation term decides.

**(LKSE)₃ against the prediction** (`nested_sampler_LKSEc12_H_m5_w7_T_window_SAb.log`).
The guess failed where I said it could: the envelope bracket is **1.23 nats**, not
0.1 (the proposals sit at nine side chains off the anchor, where the envelope is
tens of `k_BT`), `E_q ρ = 0.058`, 23 148 proposals accepted, 1 200 evaluated.
Widths: two-end form with empirical Bernstein **0.169 nats** (predicted 0.03–0.04);
two-end Hoeffding 0.42 (predicted 0.17); as stated 0.64 (predicted 0.34); plain
sampler with the same 1 200 evaluations 1.18 (empirical Bernstein; predicted about 1)
and 1.70 (Hoeffding; predicted 2.7 — its lower end is clipped at the certified one).
Point estimate `655.611`; P8's reweighting estimate `655.79 ± 0.09` is two of its
standard errors above.  A certified bracket of 4.49 nats becomes 0.17 nats at
probability 0.95 with 1 200 evaluations.

**Prediction for the larger run, written at 09:34 UTC (clock read) before it starts**
(`N_f = 4·10⁶` proposals, `N = 12 000` evaluations, outer sandwich with the anchored
split of the far pairs): the half-width in `W` should fall from `2.0·10⁻³` to about
`6·10⁻⁴` (both terms by `√10`), i.e. a bracket of about **0.05 nats** (two-end,
empirical Bernstein), if `D` stays near 4.4.

**The larger (LKSE)₃ run** (`nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`):
predicted 0.05 nats, measured **0.041** — `[655.592089, 655.632643]`, inside the
interval of the first run.

**What the verification of P8 was, in the order it happened.**  (1) The theorem,
re-derived: the remainder identity names "the `m` largest elements" of a set and
nothing else of the order, so any order serves; with a term's hosts last a host
outside `T` cannot precede `min T`.  The hypothesis can be "at most `m` hosts".
(2) A test of mine on Gaussian tables passed — and so did its three controls, which
were meant to fail.  A sum of many maxima against one number is slack on generic
tables; the test was rewritten on sums of products built so that the bound is
attained (ratio 1.0000) and every wrong neighbour of the statement is violated,
`|H| = m + 1` among them.  (`DEAD_ENDS.md` SD59.)  (3) Every state of Lys₄, Lys₅,
LKSE:5 with my own remainder code; 4 250 uniformly random states of Lys₁₂ — where
the true fifth-order remainder never exceeds `8·10⁻⁴` kcal/mol: the bound is right
and still three orders of magnitude above what the ensemble pays.  (4) P8's nine
brackets by another driver: equal in every printed digit.  (5) P8's validation chain
for Lys₄, re-run in a scratch copy.  The constants themselves nobody recomputed.

**How the far pairs were found.**  P8 had written that the Lys₁₂ bracket was limited
by the band, and named the triples `i, i+3/4, i+7`.  I wrote a rule for those terms
(keep the sub-tuple that rarely leaves the anchor) and, to validate it against
enumeration, ran Lys₅ with an artificially narrow band.  The rule did nothing
(3.543 against 3.544 nats).  The fourth line of the table — the same rule plus a
different split of the pairs beyond the band, added almost as an afterthought — read
0.046.  The cost had never been the terms.  (`DEAD_ENDS.md` SD60.)  The split around
the anchor is two lines; workstream P3's split has been in every certificate with a
band since checkpoint 40.  For apolar and mobile side chains it cost little, which
is why nobody saw it.

**Two runs stopped for the same kind of reason.**  The Lys₁₂ sampler recomputed the
transfer-matrix pass once per batch (workstream P3's `sample` does so at every
call): stopped after sixteen minutes, messages now computed once, 14 seconds.  The
Ser₂₀ sampler would have computed one closed-form sum per distinct changed set —
right for frozen ensembles, hours for a mobile one: stopped, a table of all 15 504
constants instead (`nested_sampler_p3table.py`).  In both cases I had written down
the *number* of steps before the run and not the *cost of one step*, which is what
the rule of cycle 56 asks for.  Partial logs: in the scratchpad, not in the tree.

**Workstream R16** handed back at 10:00 UTC (read from the clock when its message
arrived): the theory division's certified third level is right, and every one of its
159 certified numbers is reproduced by code that imports nothing of theirs; the one
major finding is on the other side of their comparison (five two-level worst cases
are from a design with another ladder), found because the workstream had to decide
which ladder to implement.  I read the 706 lines, re-read the lines it quotes in
their export and in the two engineering messages, and re-ran six of its scripts:
identical.  Two of its logs had not reached their last line (a failed assertion; a
run it stopped itself) and were moved out of the tree, as were eighteen superseded
logs of P8.  Published as SCI-REV-0016.

**The theory head `9befefd`** changes no file that their audit builds or runs; the
documents pass their reference check here.  The full script was not re-run — 41
minutes of four cores for inputs that are byte-identical to those audited three
hours earlier.

**Serine at twenty residues** (`8.2·10¹⁵` states): the ball of order 5 took 78
minutes; certified within 0.287 nats, 0.253 with the split.  The refined rule,
printed before the ball, said 0.210 — and `0.210 + 0.077` and `0.210 + 0.043`, the
reductions measured separately, are the two brackets to three decimals.  The sampler
on it was still building its table when this was written (10:18 UTC, clock read).

### Cycle 58 — after the checkpoint: what does one order less cost when the sampler is allowed?

**Prediction, written at 10:22 UTC (clock read) before the run.**  Lys₁₂ from the
order-4 ball (96 366 evaluations instead of 1 621 056), triple form, band 7, 'SAb',
split around the anchor: the certified bracket should be about 1.4 nats (P8: 1.56
with workstream P3's split, of which 0.14 was the far pairs).  The floor's samples
sit at seven side chains off the anchor, so the envelope bracket will not be the
first-order `0.004` nats: my guess, from `βΓ₄ = 34` spread over 495 subsets and 35
of them inside a changed set of seven, is 0.3–0.5 nats and `E_q ρ ≈ 0.15`.  With
`N_f = 4·10⁶` proposals and `N = 12 000` evaluations: **about 0.007 nats** (two-end
form, empirical Bernstein), i.e. Lys₁₂ within a hundredth of a nat from about
`1.1·10⁵` evaluations in all.  This time the guess for the envelope is made from
the model's own samples and not from the ensemble's (`DEAD_ENDS.md` SD61).

**Outcome** (`nested_sampler_K12_H_m4_w7_T_window_SAb_occ.log`, read at 10:28 UTC).
Certified bracket at order 4 with the split: **1.4125 nats** (predicted 1.4).
Envelope bracket 0.62 nats (predicted 0.3–0.5), `E_q ρ = 0.34` (predicted 0.15):
too low again, by a factor two this time and not twelve.  Width, two-end form with
empirical Bernstein: **0.0060 nats** (predicted 0.007) — `[517.125561, 517.131531]`,
which contains both intervals of order 5.  Lys₁₂ to a hundredth of a nat from
`1.1·10⁵` evaluations.  The width came out right although `E_q ρ` did not because
the variance of `W_in` is far below my guess (its mean is 0.001: the truth sits at
the top of a wide inner sandwich, so nearly every evaluated `W_in` is nearly zero).

**Workstream P9 launched** (clock: 10:25 UTC) — penalties resolved by rotamer state
(`workstreams/P9_brief.md`): workstream P8's code has the block bounds per state of
the host side chains before it takes their maximum; keep the dependence, prove the
tables valid, validate at every state of the enumerated instances with a control
that must fail, and measure the gain on Lys₁₂ (orders 4, 5) and (LKSE)₃.

**The prediction of 07:46 UTC against the run** (`nested_sampler_S20_H_m5_w7_T_window_p3table_occ.log`,
read at 10:42 UTC).  Serine at twenty residues, `8.2·10¹⁵` states.  Envelope
bracket: predicted 0.040 nats, measured **0.0401**.  `E_q ρ`: predicted 0.19 for an
outer bracket of 0.209; the outer bracket is 0.253 and `E_q ρ = 0.157` — the same
envelope over a wider outer sandwich.  Width as the theory division states the
bound: predicted about `6·10⁻³`, measured **`6.08·10⁻³`**.  With one known mean and
empirical Bernstein: predicted about `1·10⁻³`, measured **`1.03·10⁻³`**,
`[347.155238, 347.156272]`.  Three numbers written three hours before the run, for
an instance whose ball did not exist yet, all within a few per cent.  What was not
foreseen was the route: the script of cycle 56 would have needed 296 795
closed-form sums (one per distinct changed set); the table of all 15 504 constants
took 24 minutes.

**A prediction registered for a computation nobody has run (11:01 UTC, clock read):
serine at thirty residues.**  The rules predicted the twenty-residue run to a few per
cent, so the same arithmetic one size up, before anyone computes it.
Ace-Ser₃₀-NMe on the helix (`5·10²³` states), order 5, band 7: `βΓ₅ ≈ 0.99`
(extrapolating `0.226` at twelve and `0.564` at twenty residues linearly in the
length); envelope bracket `2p⁵Γ₅ ≈ 0.071` nats; triple form by the refined rule about
0.37 nats, plus reductions of about 0.12 with the split around the anchor (253 pairs
beyond the band; they cost 0.009 at twelve and 0.043 at twenty residues): **certified
bracket about 0.5 nats; with the nested sampler, 400 000 proposals and 1 200
evaluations, about `2·10⁻³` nats** (one known mean, empirical Bernstein).  Cost: a
ball of about `1.8·10⁷` evaluations and a table of 142 506 constants — some fifteen
CPU-hours, embarrassingly parallel; too long for a session here, small for the
engineering division.  To be sent as a request with the next message.

*Measured right after (11:03 UTC), for the request:* `βΓ₅ = 1.0020` for Ser₃₀ by one
closed-form sum (the extrapolation said 0.99); the ball of radius 4 has 20 535 246
states at 3.3 ms each on a loaded core (19 CPU-hours), the table 142 506 constants at
0.46 s each (18 CPU-hours); and the library as written cannot hold the ball (its states
as 64-bit integers are 4.6 GB — my first probe died on that allocation).  Sent to the
engineering division as request A18-E3 in SCI-RES-0019 §6, prediction included.

### Cycle 59 — workstream P9 read while it finishes; its brackets re-derived with a driver of mine before they are published

**Written before my re-run (clock: 12:14 UTC).**  P9's draft (read in full except its
verdict and its sampler section, which its generator has not produced yet) claims that
with penalty tables resolved by the rotamers of *all* sites of a subset, and each subset
charged in full to one sub-tuple that fits a window, Lys₁₂ is certified within
0.007347 nats from the order-4 ball (`[517.125649, 517.132996]`) and (LKSE)₃ within
0.01699 from the order-5 ball — the width of the penalty-free models plus one to three
per cent.  Its raw tables passed my checks (every state with four side chains off the
anchor: no entry below the exact anchored term, smallest ratio 8.25).  What I have not
checked is everything between the raw tables and the bracket: the allocation, the way the
tables enter the models, the sandwich at states that are not P9's.
`p9_verification/resolved_brackets.py` re-builds the window-form and triple-form tables
from the raw ones with my code, compares them with what P9 stored, builds the models with
my driver, and checks the sandwich at my own states (Gibbs with my seed, exact samples of
floor **and ceiling**, uniformly random, exactly `m` and `m + 1` sites off) with controls
that must fail.  *Cost, written before the run:* about 45 s per pair of models at band 7
(five pairs), two Gibbs samples (five minutes together), 7 000 new energies at 3.3 ms:
ten to twelve minutes per instance and order, 2–2.5 GB.  *Compared with:* P9's two
brackets of Lys₁₂ at order 4, form W `[517.125649, 517.132996]` and form T
`[517.075039, 517.186576]`, and its penalty-free width 0.007132.  *Expectation:* the same
digits — its driver calls my model builder, so a difference would be in the tables or in
how they are added, and that is what the run is for.  The controls: without the tables
the sandwich must fail at many states; I do not know whether tables a hundred times
smaller fail at any of my states — the raw bound is at least eight times the exact term
at its tightest, and the Gibbs states sit near the anchor where little is charged.

**My re-run of P9's brackets (clock: 12:40 UTC; five of six cases finished).**  Tables
re-built from P9's raw tables with my code equal its stored tables exactly (deviation
0.0) in every case; envelope ≤ tables at 32 000–40 000 random states per case, with
equality where the envelope is a single entry (window form), both controls fail; and
the brackets come out digit for digit: Lys₁₂ order 4 `[517.125649, 517.132996]` (W),
`[517.075039, 517.186576]` (T); order 3 `[517.108870, 517.185731]`, `[516.827371, 517.659419]`;
(LKSE)₃ order 4 `[655.603013, 655.622116]`, `[655.203848, 656.350724]`; Ser₁₂ order 5
`[227.363089, 227.374782]`, `[227.357675, 227.380236]`.  The sandwich at 6 980 states of
mine per case: no violation.  **What the controls say about that last check:** without
the tables the sandwich fails at 18 (Lys₁₂, order 4), 829–929 (order 3), 92 ((LKSE)₃)
states and at **none** for Ser₁₂ — for serine the sandwich check at my states has no
power at all; with tables a hundred times smaller it still fails at 4, 207, 3 states
(window form) and never with tables ten times smaller.  So the sandwich check cannot
see a table that is too small by a factor ten; the table-level checks (every state with
`m` sites off against the exact anchored term; envelope against tables with equality)
are the ones with teeth, as expected at 12:13.

**An idea while reading P9's last line ("the brackets are now the reductions of the
band, which I did not touch") — and a prediction before any twelve-residue run
(clock: 12:40 UTC).**  The slack of a reduction is not unknown: for a pair beyond the band
the ceiling's part minus the pair's table is a function of two sites that the band
model cannot hold but anyone can evaluate.  Gibbs–Bogoliubov then gives
`ln Z(E) ≥ ln Z(m₊) + β⟨s₊⟩_{m₊}` for any known `0 ≤ s₊ ≤ m₊ − E`, and from the other side
`ln Z(E) ≤ ln Z(m₋) − β⟨s₋⟩_E` with `⟨s₋⟩_E ≥ ⟨s₋⟩_{m₊} Z(m₊)/Z(E)` because `s₋ ≥ 0` and
`E ≤ m₊` — means under the *ceiling model alone*, which the transfer matrix gives
exactly when one site is held at each of its states in turn and the joint law of the
last window is read off (`pi_inference/slack_recovery.py`; searched: no such use in our
addenda — the two-sided Bogoliubov bracket is there as a datum and the far pairs only
as a choice of split; literature not searched).  Tested at every state of Lys₅ at band
2 (`first_order_recovery.py K5 4 2 --enum`): hypotheses hold at all 115 248 states with
margin exactly the constant allowance `10⁻⁷`, both controls fail, the group means agree
with enumeration to `3·10⁻¹³`, the exact `ln Z` is inside; bracket 0.0477 → 0.0106 —
only a factor 4.5 there, because at band 2 the "far" pairs are helix neighbours and
their slack is of order `kT` (an exact treatment of the same items would give 0.0017).
*Prediction for band 7, where the far pairs are eight residues apart and their slack
is small:* Lys₁₂ from the order-4 ball, `D = 0.007347`: after the far pairs
`3·10⁻⁴` nats (range 2–5·10⁻⁴: what the penalties and the 80 reduced triples leave, plus
a second-order loss of about `D/2` times the recovered amount); with the triples
`2.7·10⁻⁴`; with the allocation slack of the penalty, where a route exists, `1·10⁻⁴`
(range `4·10⁻⁵`–`2.5·10⁻⁴`).  (LKSE)₃ from the order-5 ball, `D = 0.01699`: `8·10⁻⁴`
after the far pairs, `5·10⁻⁴` with the terms, `3·10⁻⁴` with the allocation — less sure:
its four-site terms have no route when two sites are at each end.  *Cost:* one pair
of models (90 s), 47 + 28 clamped runs at half a transfer-matrix pass each (five
minutes), 6 000 new energies; ten minutes, 3 GB.  *Compared with:* the sampled
intervals, which must lie inside — `[517.128526, 517.128559]` for Lys₁₂ (mine, 0.95) and
`[655.612673, 655.612715]` for (LKSE)₃ (P9's run of my sampler, 0.95).

**The first twelve-residue run against the prediction (clock: 13:01 UTC).**  Lys₁₂ from the
order-4 ball, first version of the code (Jensen below and above; its log is not kept —
the code changed afterwards): after the far pairs `3.3·10⁻⁴` (predicted `3·10⁻⁴`), with the
80 triples `3.1·10⁻⁴` (predicted `2.7·10⁻⁴`), with the allocation slack of the 200 of 285
subsets that have a route **`1.74·10⁻⁴`** (predicted `1·10⁻⁴`, range `4·10⁻⁵`–`2.5·10⁻⁴`):
`[517.1284920, 517.1286657]`, and my sampled interval `[517.128526, 517.128559]` lies
inside it.  Hypotheses at 5 380 states of mine: no violation, margin exactly the constant
allowance `10⁻⁷` at the Gibbs states and at the samples of floor and ceiling; both
controls fail (5 788 and 2 526 violations).  What I had not foreseen: the run took 18
minutes, not ten — every elimination with a held site re-added a hundred tables; and the
upper end keeps a Jensen gap of about `10⁻⁴` because a far pair's slack is rare but not
small when it occurs (`βs ≈ 0.1`).  Both repaired before the runs of record: the term
arrays are cached (one addition per elimination), and a second upper end (UP) uses the
exact exponential within each group, as the lower end (LP) already did.  On Lys₅ the
bracket of the test moves from 0.0106 to 0.0083 with it (exact value inside, group means
against enumeration `3·10⁻¹³`).
*Predictions for the remaining runs, written now:* Lys₁₂ order 5: `7·10⁻⁵`
(`4·10⁻⁵`–`1.2·10⁻⁴`); Lys₁₂ order 4 with (UP): `1·10⁻⁴` (`6·10⁻⁵`–`1.7·10⁻⁴`);
Lys₁₂ order 3 (`D = 0.077`, of which 0.070 is penalty): 0.035 (0.015–0.06) — at order 3
most subsets fit a window and are charged their own table, which is envelope, not
allocation slack, and no recovery touches that; (LKSE)₃ order 4 (`D = 0.0191`): `1·10⁻³`
(`5·10⁻⁴`–`2·10⁻³`); (LKSE)₃ order 5 as written at 12:40 (`3·10⁻⁴`); Ser₁₂ order 5
(`D = 0.0117`): `2.5·10⁻³` (`1.5`–`4·10⁻³`) — a mobile ensemble, the slack is frequent,
and its four-site terms have no route when two sites sit at each end.

**P9's sampler run from the order-4 ball replicated with my driver and another seed
(clock: 13:04 UTC; `p9_verification/nested_resolved.py`, seed 2026113740 where P9 had
2026112740).**  (LKSE)₃: as the theory division states the bound
`[655.612563, 655.612815]` (P9: `[655.612562, 655.612814]`); two-end form with empirical
Bernstein `[655.612658, 655.612720]` (P9: `[655.612657, 655.612719]`); 15 392 of 400 000
proposals accepted (P9: 15 158), 1 200 evaluated, none outside either sandwich.  Two
independent runs, the same interval to the sixth decimal: the proposals carry the
estimate, and 400 000 of them pin it.
*A run P9 could not make (memory), predicted before I start it:* Lys₁₂ from the order-3
ball — 3 841 evaluations — with the resolved envelope, 12 000 evaluations and 400 000
proposals.  Outer bracket 0.0769; I expect a mean acceptance `ρ` near one half (the
envelope is not small at this order), and a width of `5·10⁻⁴` nats in the two-end form
with empirical Bernstein (range `3·10⁻⁴`–`10⁻³`), about `1.5·10⁻³` as the theory division
states the bound (P9 wrote `2·10⁻³` at 11:47).  It must contain `[517.128526, 517.128559]`
or at least overlap it.

**Two more turns of the same screw, and the runs of record restarted (clock: 13:14 UTC).**
The second version of the code (cached term arrays: 182 s for the held-site passes
instead of 812; upper end (UP)) gave Lys₁₂ at order 4 `[517.1284920, 517.1286504]`,
`1.58·10⁻⁴` — (UP) moved the upper end by `1.5·10⁻⁵` only, not by the `10⁻⁴` I had
expected two entries above: the Jensen gap was not the loss.  The loss is in how the
items are *grouped*.  Each group — the items that share a held site — is treated exactly;
across groups only a product inequality holds.  My routing held the *left* site of a
far pair, but nine of the ten pairs keep the *right* site in their reduction, so the
slacks of all pairs with the same kept site occur at the same states and sat in
different groups.  Holding the kept site instead (`slack_recovery.route` with a
preference; the mirrored chain serves it) puts them into one group.  On Lys₅ at band 2
the bracket of the test goes from 0.0083 to **0.0029** with it (sandwich 0.0477; an exact
treatment of the same items would give 0.0017).  The two chains that had started with the
second version were stopped (one complete log, Lys₁₂ order 4; one partial, (LKSE)₃
order 5 — `3.8·10⁻⁴` there, predicted `3·10⁻⁴`); their logs are not kept; all six
twelve-residue cases restarted with the final code at 13:11.
*The enumerated tests of record, final code* (`first_order_recovery_*_enum.log`; every
state; exact `ln Z` inside every corrected bracket; hypotheses violated at no state, margin
exactly `10⁻⁷`; both controls fail; group means against enumeration within `3·10⁻¹²`):
Lys₅ order 4 band 2: 0.0477 → 0.00292; band 3: 0.0189 → `6.6·10⁻⁵`; order 5 band 3:
0.0187 → `9.8·10⁻⁶` (an exact treatment of the routed items: `4.2·10⁻⁶`); LKSE:5 order 4
band 2: 0.205 → 0.0016.

**What is left after the recovery is a rounding allowance — found by asking where
`2.9·10⁻⁴` nats of (LKSE)₃ come from (clock: 13:23 UTC).**  Third version of the code
(kept-site grouping), stopped after two cases: Lys₁₂ order 4 `[517.1285006, 517.1286028]`,
**`1.02·10⁻⁴`** (predicted `1·10⁻⁴`); (LKSE)₃ order 5 `[655.6125161, 655.6129056]`,
`3.9·10⁻⁴` — no better than with the old grouping (`3.8·10⁻⁴`), and its allocation slack is
only `10⁻⁵`.  So what is the rest?  Not the envelope (`3·10⁻⁶`, P9).  It is workstream
P6's allocation of the *floating-point allowance* of the evaluated terms: every `d_U` is
an alternating sum of `2^{|U|}` values of `g`, each allowed an error `ε_g = 10⁻⁷` kcal/mol
(P3: an a-priori worst case of `3·10⁻⁸`, not proved for the evaluator's summation order;
measured errors `2·10⁻¹²`), and P6 allocates the allowance of all terms through a pair
to that pair: `1.5·10⁻⁵` kcal/mol per in-band pair at order 5, charged whenever the pair
is off the anchor — although nearly all of those terms are not.  First-order cost on the
Gibbs samples (`2β⟨allowance⟩`, measured now): Lys₁₂ `3.9·10⁻⁶`, `2.2·10⁻⁵`, `1.06·10⁻⁴`
at orders 3, 4, 5; (LKSE)₃ `9·10⁻⁶`, `5.8·10⁻⁵`, **`2.7·10⁻⁴`**; Ser₁₂ `3·10⁻⁵`,
`2.2·10⁻⁴`, **`1.0·10⁻³`**.  It grows sevenfold per order while the truncation error
falls: once the band's slack is recovered, order 5 is *worse* than order 4 for Lys₁₂.
The allowance is not slack (the rounding error is unknown), but its allocation is a
choice: attached to each term's own table — `d_U ∓ 2^{|U|}ε_g` where all sites of `U` are
off the anchor — it is charged only when the term is.  Built into the driver (fourth
and final version; the sandwich with P6's allocation is printed beside it); Lys₅ at every
state: hypotheses hold, exact value inside.  *Prediction for the runs of record:* the
corrected brackets fall by about the numbers above — Lys₁₂ order 4 `8·10⁻⁵`, (LKSE)₃
order 5 `1.2·10⁻⁴`, Lys₁₂ order 5 `3·10⁻⁵`–`6·10⁻⁵`, Ser₁₂ `1.5·10⁻³` instead of
`2.5·10⁻³`.  All six restarted at 13:23.

**Runs of record, final code, first two cases (clock: 13:35 UTC).**  Lys₁₂ order 4:
sandwich with the allowance attached term by term `[517.125658, 517.132987]` (0.007329;
with P6's allocation 0.007347, P9's number); corrected **`[517.1285101, 517.1285931]`,
`8.3·10⁻⁵`** (predicted `8·10⁻⁵`); my sampled interval of part (18) inside.  (LKSE)₃
order 5: sandwich `[655.604165, 655.620921]` (0.016757; with P6's allocation 0.016987);
corrected **`[655.6126377, 655.6127810]`, `1.43·10⁻⁴`** (predicted `1.2·10⁻⁴`); P9's and
my sampled intervals inside.  Hypotheses at 5 380 states each: no violation; the means
against 20 000 exact samples of the ceiling within 1.4 standard errors.
*A question the recovery raises, with a prediction before the run:* if the band's slack
can be taken back, can the band be narrower?  Lys₁₂ order 4 at **band 6** (arrays seven
times smaller; fifteen far pairs, now including the `i, i+7` pairs two helical turns
apart): I expect a sandwich of about 0.05 nats (0.02–0.08) and a corrected bracket of
about `10⁻³` (`3·10⁻⁴`–`3·10⁻³`) — the slack of closer pairs is larger when it occurs,
and Lys₅ at band 2 shows what that costs.

**Band 6 against the prediction; orders 3 and 4 of record (clock: 13:41 UTC).**  Lys₁₂
order 4 at band 6: sandwich `[517.117635, 517.139075]`, 0.0214 (predicted 0.05, range
0.02–0.08: at the lower edge); corrected **`[517.1284536, 517.1287322]`, `2.8·10⁻⁴`**
(predicted `10⁻³`, range `3·10⁻⁴`–`3·10⁻³`: just below my range); 214 s and 1.4 GB
against 515 s and 2.7 GB at band 7; my sampled interval inside.  **Band 6 with the
recovery is 26 times tighter than band 7 without it.**  Lys₁₂ order 3: sandwich 0.0769 →
0.0611 (predicted 0.035, range 0.015–0.06: just above my range) — the envelope, as
expected in kind: `2β⟨envelope⟩` is 0.053–0.064 on the two Gibbs samples.  (LKSE)₃ order 4:
0.0191 → **0.00154** `[655.6119691, 655.6135057]` (predicted `10⁻³`, range
`5·10⁻⁴`–`2·10⁻³`); the envelope there is `8·10⁻⁴`.
*Next, predicted now:* band 5 (twenty-one far pairs, from six residues apart; twelve
sites are more than `2w`, so some items have no route): sandwich 0.04 (0.025–0.1),
corrected `7·10⁻⁴` (`3·10⁻⁴`–`2·10⁻³`).  Band 4 (far pairs from five apart): sandwich
0.1 (0.05–0.3), corrected `3·10⁻³` (`10⁻³`–`10⁻²`).

**The runs of record, complete (clock: 14:01 UTC; final code; nine twelve-residue
logs and four enumerated ones, every one ending with its last line).**  Band 7:

| case | sandwich | corrected | predicted |
|---|---|---|---|
| Lys₁₂, order 3 | 0.07686 | 0.0611 | 0.035, range 0.015–0.06 — just above |
| Lys₁₂, order 4 | 0.007329 | `8.3·10⁻⁵` | `8·10⁻⁵` |
| Lys₁₂, order 5 | 0.007138 | `2.2·10⁻⁵` | `3`–`6·10⁻⁵` — below |
| (LKSE)₃, order 4 | 0.019067 | 0.00154 | `10⁻³`, range `5·10⁻⁴`–`2·10⁻³` |
| (LKSE)₃, order 5 | 0.016757 | `1.43·10⁻⁴` | `1.2·10⁻⁴` |
| Ser₁₂, order 5 | 0.011076 | 0.00179 | `1.5·10⁻³` |

Bands 5 and 4 for Lys₁₂ at order 4: sandwiches 0.0253 and 0.0288 (predicted 0.04 and
0.1 — the second well below my range: the pairs five and six residues apart cost
less than I thought once the split around the anchor is in), corrected `4.2·10⁻⁴`
and `6.9·10⁻⁴` (predicted `7·10⁻⁴` and `3·10⁻³` — the second below my range).
The sampler from the order-3 ball of Lys₁₂ (run at 13:05): two-end form with empirical
Bernstein `[517.128107, 517.128879]`, `7.7·10⁻⁴` (predicted `5·10⁻⁴`, in range); as
stated 0.0025 (predicted 0.0015 — too low: 78 % of the proposals are accepted, I had
said "near one half").
*What the afternoon was.*  P9 handed back at 12:21 with brackets fifty to two hundred
times tighter than the morning's and the sentence that what is left is the band,
untouched.  By 13:50 the band's slack was out as well — four versions of one small
module, each made necessary by a number that did not fit: a run three times slower
than its estimate (cached arrays), an upper end that did not move when I expected it
to (the grouping, not Jensen), a residual that was neither envelope nor allocation
(the allowance).  Three of my explanations were wrong before the measurement that
replaced them; they are in `DEAD_ENDS.md` (SD63).  What I would do differently:
decompose the residual of the *first* full-size run before starting six more.
*Left open on purpose:* the recovery on Ser₂₀ and Leu₃₀ (needs the backward message);
two held sites; the question of which band to use.

**The fetch before the commit found the theory division at a new head (clock: 14:10 UTC).**
`dd067f1`, their twenty-second checkpoint, commit time 13:42 UTC, found at 14:02:12 by
the fetch made in a command of its own when SCI-MSG-0028 and every record were ready;
nothing was staged.  THY-RES-0015 read in full.  They applied both of our reviews,
machine-checked the remainder identity with one order per term with the hypothesis my
check of workstream P8 had sharpened ("at most `m` hosts") and its sharpness, and the
split around the anchor; answered the sign-blind question with a lemma and asked one
back; and offer a new theorem — `exp(n·h + O(√(n ln n)))` for adaptive algorithms
without a hint — for review.  They also reproduced a table of our workstream R15 "to
every digit but one".  The digit was ours: `21·0.3 − ln 99 = 1.7049`, printed by the
script as 1.705 and rounded a second time in the report to +1.71, in two rows.
Corrected with a note under the table (SCI-RES-0020 §2).  A double rounding is a new
kind of error for this record; the check that found it was somebody else's
replication, which is what replications are for.
Done before the commit: the correction; SCI-MSG-0028 adjusted (its request P9-T3 is
their new identity; header); **workstream R17 launched at 14:07** — a referee for their
Theorem 11.58a, with the contract of workstream R16 as its checklist and one question
of mine (their message says `n·h − O(1)` for the lower bound, page one of their report
`n·h − O(ln n)`); their audit at the new head started at 14:03:44; SCI-RES-0020.
Owed: whether lysine head groups are in the regime `ρR² < 1` of their lemma — the
loss P8 measured (5.1) equals their `R² ≈ 4.9` for a constant kernel, which is
suggestive and not a measurement.

### Cycle 60 — a question answered against my own hint; the recovery for chains of any length; a charged chain of twenty residues, predicted before it is computed

**The theory division's question, measured (clock: 14:26 UTC;
`p8_verification/kernel_spread.py`).**  Their sign-blind lemma needs the kernel to vary
little over the atom pairs of two charged groups: `ρR² < 1`, i.e. `ρ < 0.20` for two
ammonium groups (`R = Σ|q|/|Σq| = 2.2146` with the charges of our parameter files,
`−0.3854` and `3 × 0.34`: their remembered values are right).  In SCI-RES-0020 I wrote
that P8's measured loss, 5.1, "is what your lemma gives for a constant kernel … consistent
with a small `ρ`".  **It is not small.**  For Lys₅ at order 4, at the point of the largest
mixed difference of each of the five subsets, the mixed-difference kernel between the
ammonium groups of every pair of lysines has `ρ` between 0.95 and 2.1 (median 1.0; best
constant reference) in all fifty blocks; `ρR_aR_b ≥ 4.7` everywhere; the lemma's regime
is reached by none.  In the blocks that carry the mixed difference (lysines `i, i+3` and
`i, i+4`) the sixteen entries are of one sign and span three orders of magnitude
(`−2.0·10⁻³` to `−1.7·10⁻⁶` per nm for the largest block): the fourth mixed difference is
carried by the nearest atom pairs.  The sign-blind loss of those blocks, computed
exactly, is 2.6–4.3 — *below* `R² = 4.9`.  So the agreement of 5.1 with 4.9 was a
coincidence of two numbers, and my hint pointed the wrong way; it goes back to them as
a linked correction with the measurement.  (Fifth entry of the kind in `DEAD_ENDS.md`:
this time the caveat "not a measurement" was written next to the hint, which is why it
is a correction and not a retraction.)

**Held-site passes for a window anywhere on the chain (`pi_inference/held_site_laws.py`).**
The joint law of a held site and a window of `w` sites that is not the last one is
`exp(F_b + B + I)`: the forward message with the site held, the backward message (the
forward message of the mirrored chain), and the terms inside the window — every term
of a band model is in exactly one of the three.  Tested at every state of Lys₅ at band
2, where the chain is longer than `2w`: 18 of 25 items now have a route (14 before), the
total mass of every held-site pass is one to `5·10⁻¹⁴`, the group means agree with
enumeration to `10⁻¹²`, the far-pair stage reproduces the committed number digit for
digit (0.003989) and the bracket with the terms goes from 0.002913 to 0.002885.

**Lys₂₀ on the helix — predicted before anything is computed but the ball (clock: 14:26 UTC).**
Ace-Lys₂₀-NMe, `5.5·10¹⁷` states, 452 atoms; ball of radius 3: 385 566 states (being
evaluated: 3.1 ms each); order 4: 4 845 subsets, P9's resolved tables at about one second
each (two parts running).  *Prediction.*  Sum of the maxima of the tables: `βΓ₄ ≈ 35`
(Lys₁₂: 18.2; I expect it to grow a little faster than the length).  Sandwich in the
window form, band 7, **if the floor stays at the anchor**: 0.02 nats (0.012–0.04) — 78
pairs beyond the band, 33 of them with one of the three mobile N-terminal side chains.
I give the floor three chances in four of staying at the anchor; nothing we have predicts
it (P9-T2), and if it does not the bracket is tens of nats and the run is a negative
result about order 4 at this length.  Corrected bracket, with the general held-site
passes: `3·10⁻⁴` (`10⁻⁴`–`10⁻³`): envelope `3·10⁻⁵`–`3·10⁻⁴`, `D²/4 ≈ 10⁻⁴`, and the
four-site subsets without a route.  *Checks planned:* the raw tables entry by entry at
20 000 random states with exactly four side chains off (the per-entry check that
exists without a ball of radius 4), with a control; the hypotheses at 5 380 states;
the means against exact samples of the ceiling.  *Cost:* Gibbs samples 15 minutes,
models and held-site passes 15, checks 5; 6 GB.

**The theory division's audit at `dd067f1`: passes here** (14:03:44–14:45:11 UTC): 87 Lean
files, 47 657 lines, 8 645 build jobs; 4 937 declarations on the three standard axioms,
659 headline theorems; 538 mutations, 537 caught and one expected pass.  `CoreGreedy.lean`
as adopted is our file with a provenance paragraph; `TermOrders.lean` built and
axiom-checked, not read.  The list of tokens their document checker ignores grew by
eleven symbols; none is a declaration name (`INDEPENDENT_VALIDATION.md` §1.12).

**15:00 UTC — the theory head moved again (`8ff0667`, 14:46 UTC), found by the fetch before
the commit of SCI-RES-0021.**  Work in progress without a message: four briefs, among them
a Lean task for our Proposition A17.19 and workstream P9's Proposition P (their
restatements agree with ours — checked line by line: the same group index in
`S⁻_g e^{βS⁺_g}`, the hypotheses as sums over groups, "only domination is used"), and
stored checks towards answers to A19-T2 and P9-T2 (among them: the bound
`1 + Σ⟨y_g⟩` between groups is attained by some coupling exactly when the events
`{S_g > 0}` can be made disjoint, and a pair term can be added when a pair law is
known).  Read as far as it mentions us; noted in SCI-RES-0021 §3; nothing built on it
before their message.

**The first two regression runs with the general module (Lys₁₂, order 4, bands 7 and 6)
are not "identical", and should not have been expected to be** — I had written that the
band-7 cases must reproduce the committed brackets digit for digit.  The rows that use
only the old routes (far pairs; far pairs and terms) do, to every printed digit.  The
last row does not: thirty-five (band 7) and eighty-five (band 6) four-site subsets that
had no route now go through a window inside the chain, and the bracket tightens —
`8.297·10⁻⁵ → 8.161·10⁻⁵` and `2.786·10⁻⁴ → 2.738·10⁻⁴` — with the new bracket inside
the old one at both ends.  The right regression statement is: same items, same
numbers; more items, a bracket inside the old one.

**Lys₂₀: the outcome against the prediction of 14:26 UTC** (`first_order_recovery_K20_m4_w7.log`
— in the working tree when this was written; committed with part (20) of the addenda —
finished 15:16:36 UTC, 1 390 s, 5.5 GB; ball 385 566 values; P9's 4 845 order-4 tables through
`p9_verification/dump_theta2.py`, whose call reproduces P9's own stored tables of Lys₁₂ bit
for bit on 18 subsets and those of the four small instances).

| quantity | predicted | found |
|---|---|---|
| sum of the maxima of the tables, `βΓ₄` | about 35 | **45.2** — a miss: I let it grow "a little faster than the length"; it grew 2.5-fold for 1.67 times the length |
| the floor stays at the anchor | three chances in four | **yes** |
| sandwich, window form, band 7 | 0.02 (0.012–0.04) | **0.01814** `[800.505214, 800.523352]` |
| corrected bracket | `3·10⁻⁴` (`10⁻⁴`–`10⁻³`) | **`4.05·10⁻⁴`** `[800.5150660, 800.5154710]` |

Checks: the two hypotheses at 5 380 states with new evaluations, no violation (every item
doubled: 8 029; far items exchanged: 3 501); the exact means against 20 000 exact samples
of the ceiling within 1.4 standard errors; P9's tables entry by entry at 20 000 states
with exactly four side chains off: no violation, smallest ratio of entry to remainder
10.9, median 240 (every table replaced by its minimum: 5 556 violations).  6 175 items,
3 823 with a route (2 029 of them through a window inside the chain), 2 352 without —
2 240 of those are four-site subsets that would need two held sites; their first-order
weight is `1.2·10⁻⁵` nats per side.  The Gibbs sample has 1.49 side chains off the anchor
on average.  So a charged chain of `5.5·10¹⁷` states is bracketed deterministically
within `4·10⁻⁴` nats from 385 566 evaluations; the method of part (19) carries over to a
chain longer than twice the band without a new idea, only the general windows.

**15:11 UTC — a supplementary directive of the research owner arrived**
("Mathematical Generality, Physical Relevance, and Foundational Breakthroughs"; verbatim in
SCI-MSG-0029 §1).  It keeps the programme and moves its weight: generality, an audit of
assumptions for every major theorem, obstruction theorems, experiments for the
mathematics, application-specific benchmarking later; this division is to assess
assumptions, limits and relevance and to name the gaps; the directive is to be relayed
to the other divisions.  Done within the hour: the relay (SCI-MSG-0029), and
`docs/science/ASSUMPTION_AUDIT.md` with Part A — our own certificate line.  What writing
Part A turned up, in the order it surprised me:

* **The envelope never needed the generalised-Born form.**  P9's proof uses three facts:
  the remainder identity, hosts enumerated, and that everything else enters through
  statistics that are *additive over the sites*.  For a term `φ(c + Σ_i a_i(x_i))` the
  order-`m` mixed difference is an integral of `D^mφ` against the product of the sites'
  displacements, so the resolved table of a subset is `M_m·Π_{i∈T} δ_i(x_i)` — rank one —
  and the envelope is `M_m·e_m(δ)`.  "Few sites off the anchor" was a proxy: the
  quantity is the total displacement of the statistics against the curvature scale.
* **The two ends of a bracket are not alike, and that is where several modes enter.**  A
  ceiling can be restricted to one mode and still gives a lower end; a floor must hold on
  all of the space.  A floor that leaves the anchor is the same fact seen from inside.
* **For few additive statistics no expansion is needed at all** — a transfer matrix that
  carries the binned partial sums is exact up to a binning allowance, at a cost
  exponential in the number of statistics, not in the size (level H2′; in outline only).
* Three counterexamples were run for the entries classified "false without"
  (`assumption_audit/aa01_essential.py`); the entries that rest on literature I did not
  open in this session are marked "from memory" and are an obligation (`G-8`).

No further application-specific run is started in this phase.  Next: the synthetic test
of the general class (`G-1`), the level H2′ (`G-2`), Part B of the audit (a workstream),
a referee for parts (19)–(20) and for Part A.

**15:36–16:05 UTC — a second directive of the owner (six divisions), four checkpoints, two
referees launched, one more correction of my own.**  The expansion directive is recorded
verbatim (`OWNER_DIRECTIVES.md`); our copy of the protocol names six divisions; every fetch
now covers five branches.  Published since: the relay and the audit's Part A (`2cad679`),
the six-division protocol (`27828f1`), the review of the theory division's Theorem 11.58a
(`1b89f12`: proved as stated given its inputs; nine minor findings; our referee ran the
outer loop their report said could not be run), part (20) with the general held-site
passes and Lys₂₀ (`0930440`).  Both other divisions relayed the same directive within a
quarter of an hour of ours; the theory division machine-checked Proposition A17.19 and
workstream P9's Proposition P and answered both open questions of SCI-MSG-0028.
Launched at 16:02: R18 (referee of the engineering division's ENG-RES-0014 §1 and §4, as
accepted) and R19 (an adversarial referee of my own parts (19)–(20) and of Part A of the
audit, including the test of Corollary AA.2 on a synthetic energy — which I therefore do
not run myself).  **A correction:** in SCI-RES-0023 I wrote that for the box class of a
sandwich there is "no lower bound that we know".  There is: the theory division's
Proposition 11.113 (d), which we sketched and reviewed twice.  Found while deciding what
to work on next; withdrawn by SCI-RES-0025; SD67 ("nothing is known" is a claim).

**A scan in the penalty strength — predicted at 16:05 UTC, before the script exists.**
The theory division reads a floor that leaves the anchor as a first-order transition in
the size of the tables (THY-RES-0016 §5 (i)) and asks for numbers.  Test: multiply every
penalty table of the floor by `λ` and follow `ln Z` of the floor, the mean penalty and the
number of displaced sites under it.  If the reading is right there are two states —
few sites off; a window (or the chain) fully off — and the occupancy jumps at a `λ_c`
within a narrow range of `λ`, while the first-order number `β·λ·⟨pen⟩₀` stays smooth.
*Predictions* (band 7 unless said): the cost of displacing a lysine side chain is about
`ln(0.9/0.1) ≈ 2.2 kT`, so a chain fully off costs about 26 `kT`; the penalty of the fully
displaced chain is a fraction of the sum of the table maxima (18 `kT` at order 4, 272 at
order 3, raised by the reductions to windows).  **Lys₁₂, order 4: `λ_c` between 2 and 6
(central 3.5); at band 4 lower, 1.5 to 4.  Lys₁₂, order 3: `λ_c` between 1.05 and 1.5 —
it is certified at `λ = 1` with 0.077 nats, so it must be close.  (LKSE)₃, order 3, whose
floor has left at `λ = 1`: `λ_c` between 0.1 and 0.4.**  Sharpness: the mean number of
displaced sites goes from below 2 to above 8 within a factor 1.3 in `λ`.  What would
count against the reading: a gradual rise of the occupancy over a factor 3 or more in
`λ`.  Cost: one model build per instance (the Gibbs sample, two to eight minutes) and a
transfer-matrix run plus a thousand exact samples per `λ` (seconds); under 4 GB.

**16:22–17:07 UTC — both new divisions ask for a review; three of four scans against the
prediction; where the evaluations of a shell go.**  *The Ensemble division* published its
first checkpoint at 16:48 UTC (`a570520`), twenty-six minutes after our answer to its plans
(SCI-RES-0026), which it had not read: twelve statements, among them "ensemble rigidity =
global rigidity" (a graph is generically globally rigid iff every generic finite ensemble
of frameworks is determined by the laws of its edge lengths), with the request to attack
that statement, §5 of its report and the reading of its E1.3.  Accepted: workstream R21
(launched 16:53 on a read-only export; SCI-RES-0028).  Its report has an example of an
identified conformation with a modulus of order `√τ` and says that this cannot happen on a
finite space; our SCI-RES-0026 §2 (c) had the complementary sentence — at an interior point
of a continuous space it always happens, for any finite family of `C¹` observables — and
SCI-RES-0028 puts the two together.  *The Complexity division* opened a second line
(phylogenetic networks, `9a35d2f`); no message, nothing asked, the note our R20 reads is
unchanged.  Four referees are now running (R18–R21); I do none of their work.

*The scan in the penalty strength, three cases of four* (prediction: the entry of 16:05).
(i) **Lys₁₂, order 4, band 4: `λ_c = 15.3`; predicted 1.5 to 4 — missed by a factor 4 to
10.**  (ii) Lys₁₂, order 3, band 7: `λ_c = 1.32`; predicted 1.05 to 1.5 — met.  (iii) (LKSE)₃,
order 3, band 7: `λ_c = 0.198`; predicted 0.1 to 0.4 — met.  Sharpness (the mean number of
displaced sites from below 2 to above 8): a factor 1.14 in `λ` in (i), 1.22 in (ii);
predicted "within a factor 1.3" — met; in (iii) the reference itself has 2.8 sites off, so
the criterion does not apply as written, and the occupancy goes from 2.9 to 12 between
`λ = 0.15` and `0.3`.  `ln Z` of the floor is convex in `λ` on each grid (it must be; the
control, the same test on `−ln Z`, fails).  *Why (i) was missed:* I priced a displaced
lysine at `ln(0.9/0.1) ≈ 2.2 kT`, the cost of the *typical* state off the anchor.  The
state the penalty selects is not typical: it is where the tables are large, and the tables
are large where charged groups come close.  From the log: at the transition the slope
`β⟨pen⟩` is 3.0–3.1, half of the displaced state's (the two states have equal weight), so
the displaced state collects about `6·λ_c ≈ 94 kT` of penalty there and must cost as much
in the model without penalty — about eight `kT` per residue, not two.  The same reading of
(ii): slope 28 at the transition, `57·1.32 ≈ 75 kT`.  So the three transitions are
consistent with one picture — two states, the second one expensive and rewarded in
proportion to `λ` — and the width of the transition in `λ` should be about the inverse of
the displaced slope (0.16, 0.018, 0.003 in the three cases; the bisection points agree in
order of magnitude).  A check of that formula on the logged points is owed before it is
sent to anyone.  The fourth case (Lys₁₂, order 4, band 7) is still running: its table at
`λ ≤ 6` shows the reference state; my prediction was 2 to 6.
*What the miss teaches:* a prediction of `λ_c` needs the cost of the state the penalty
prefers, which is a ratio problem — the least of (cost of a state without penalty)/(its
penalty) over states — not a property of typical states; that ratio can be computed
exactly on a band model by a few maximisations, which makes it a candidate for the
"safety factor" of a certificate (`OPEN_PROBLEMS.md` D12 (b)).

*Where the evaluations of a shell go* (`pi_inference/subset_concentration.py`; an
estimate, no certificate; `OPEN_PROBLEMS.md` D14).  On Lys₁₂, with the occupation taken
from the product of the one-site marginals of a Gibbs sample: nine tenths of the
first-order envelope of order 3 lie in 3.2 % of the triples (7.9 % of the evaluations of
the shell of radius 3), 99 % in a fifth of them (34 %); at order 4, nine tenths in 2 % of
the subsets (6.2 % of the shell).  **The control — the same tables shuffled among the
subsets — gives almost the same shares.**  So the concentration is that of the occupation
(which sites are likely to be displaced together), not of the tables, and it is known
before any evaluation.  The first version of the estimate, on the 960 sampled states
themselves, was inconclusive: its control showed the concentration of the sample (most
subsets never occur in it).  Not done: the remainder bound of a down-closed family that is
not a ball (the supersets of the evaluated subsets enter), and a run.

*The fetch of 17:05:14 UTC, made when the above was ready: four of five branches had moved.*
**The Geometry division has opened** (`d84a43b`): two messages and a request to us
(GEOMETRY-REQ-0003: a line-by-line review of three theorems on what ensemble-averaged
squared distances determine under statewise bond constraints, prior art, an attack on its
assumption table, and whether such an average is measured anywhere) — read in full; the
answer and a referee are owed and follow in the next commit.  The engineering division
built an exact checker for the certificates of our request P7-E2 (no message yet; to be
read and run on our files); the theory division's assumption audits exist as two reports
not yet applied; the Complexity division added an algorithm note.  All three new divisions
have now asked this division for a review within seventy minutes of opening.  The two new
divisions that work on distances state, independently and on the same afternoon, the two
sides of one fact: mean squared distances determine nothing about an unconstrained
ensemble (the Ensemble division's E1.3, by a random scaling) and determine a mixture
uniquely when every state obeys the same bond constraints (the Geometry division's item 3)
— the scaling of the first breaks the constraints of the second.  To be said to both.

**17:07–17:21 UTC — the Geometry division answered; a boundary of its main theorem; one
inequality behind three divisions' stability statements.**  The Geometry division's first
checkpoint (`d84a43b`): for chains with fixed bond lengths and angles, the matrix `M` of
ensemble-averaged squared distances determines a `K`-state mixture among *all* probability
measures when the only quadrics through the constrained edge directions of the "stacked"
framework in `ℝ^{3K}` are `K − 1` trivial ones (their (CC)), with a stability bound
`W₂² ≤ C‖ΔM‖`.  They ask for a review (accepted: R22, launched 17:16), prior art, an attack
on their assumption table, and whether such an average is measured at all.
*Relevance* (answered from general knowledge and three searches, summaries only): the
low-angle limit of a two-label interference experiment is exactly `⟨r²⟩`, and the Guinier
radius of a labelled block is a block sum of `M`; such experiments exist (neutron label
triangulation, X-ray interferometry between gold labels, deuterated blocks in polymers);
the usual restraints (relaxation rates, transfer efficiencies, couplings) average other
functions.  So the observable is real, rare in its labelled form, and naturally a block
sum.
*My own check, before the referee* (`geometry_checks/hinge_pair.py`, four seconds; I
expected only to confirm that states sharing rigid parts are "non-generic" and found how
large that set is).  (a) Two states that differ in one torsion are never identified: a
point rotating about an axis has squared distance `a + b cos φ + c sin φ` to a fixed one,
so `M` sees a measure on that circle only through its first Fourier coefficient, and every
chord through the mixture's coefficient is a competing two-state ensemble (60 competitors,
agreement `10⁻¹⁴`, control passes).  (b) (CC) fails whenever two states differ in at most
three torsions: the stacked edge vectors of a shared rigid segment lie in a 3-dimensional
subspace of `ℝ⁶`, two such subspaces meet in a line, so `s` segments give at most
`6s − s(s−1)/2` conditions on the 21-dimensional space of quadrics — dimension at least 10,
6, 3 for one, two, three differing torsions; numerically exactly that, and 1 from four on.
(c) Every squared distance is multilinear in `(1, cos φ_k, sin φ_k)`: `M` is a linear image
of the Fourier coefficients of the torsion distribution with all indices in `{−1, 0, 1}`.
*Not known:* whether two states that differ in two or three torsions are identifiable
without (CC); my sketch (a rank-2 moment matrix on `{1, z₁, z₂, z₁z₂}` with two bilinear
kernel polynomials) says yes for two; the referee is asked to decide by a linear
programme.  I made no prediction in writing before running (a)–(c); the count in (b) was
derived after seeing the dimensions 10, 6, 3, 1, which it then reproduced — so it is a
fitted explanation with a proof of the inequality, not a prediction.
*One inequality, three divisions.*  For `f = c₀ + λ·Φ ≥ 0` vanishing on the support of `μ`:
`∫f dν ≤ ‖λ‖_*τ`.  A certified gap gives the Ensemble division's bound on the mass off the
support, sharp growth their `W₁` bound (and the theory division's robust optimality),
quadratic growth the Geometry division's Theorem G — and my remark to the Ensemble
division of 16:22 (no sharp certificate at an interior point of a manifold) is the
general form of Geometry's lower bound (e).  Three sessions wrote instances of it within
two hours without seeing one another's; said to all three in SCI-RES-0029.

**17:21–17:47 UTC — the referee of my own results reports: the brackets hold; four of my
statements do not.  A defect of our own checker, found by the engineering division.  The
last scan misses its prediction too.**
*R19* (launched 16:02 to attack parts (19)–(20) and the audit's Part A; 88 minutes; report
read in full).  What holds is what I most needed checked and could not check myself: the
accounting is an identity at every state tested, nothing is counted twice, the held-site
statistics are exact, and the Lys₁₂ bracket at band 4 comes out of code that shares nothing
with mine from the tables on.  What does not hold is in my prose, four times: (M1) "the loss
between groups is about `D²/4` … what we measure" — sent to the theory division twice.  The
two numbers I called measured are that formula evaluated.  The referee measured it: 2.09
and 1.54 times `D²/4` at Lys₁₂ — two thirds and a quarter of those brackets — and found the
ratios 2.24, 0.16, 0.06, 0.07 **in my own enumerated logs**, where the line "with the routed
items put back exactly" had been printed by my own script and never subtracted by me.  I
repeated the band-4 measurement with another seed: 2.084.  (M2) "the ceiling holds on all
of the space: removable" — what is removable is finiteness.  (M3) Proposition AA.1, which I
wrote yesterday afternoon as "the general statement" behind the envelope, excludes terms
with hosts — the instance I abstracted it from has hosts.  (M4) a growth comparison I
labelled [P] rested on "the cost grows at most linearly", which is false for the
interpolant.  All four accepted; linked correction SCI-MSG-0030; the audit carries marks
and a change table; addendum part (21); SD68–SD70.  *What I take from it:* three of the
four are the same failure — a sentence about my own result written from the picture in my
head instead of from the log or the proof — and the audit, which I wrote to find exactly
this in others' work, contained two of them.  The rule that would have caught M1 is one I
already had (SD63: compute the size of every candidate cause before naming one); I had
computed a formula and written "measure".
*The engineering division* built the compiled checker we asked for (P7-E2) from our text
alone, and then read our reference checker: it summed every entry of two lists while
bounding only the entries the format defines, and validated nothing — a malformed file
could be accepted with a false bound.  Confirmed with their example; none of our nine files
is malformed.  Corrected (`p7_06_check.py`; a control that reproduces the defect: the old
rule accepts 9 of 9 poisoned files, the new one none); their checker and its 182 tests run
here with another compiler; SCI-RES-0030.  The certificate line now has two outside
findings in one hour, both about things I had called checked.
*The fourth scan* (Lys₁₂, order 4, band 7): `λ_c = 18.8`; predicted 2 to 6 — missed, like the
band-4 case, and for the same reason.  A wider band moves the transition up (15.3 → 18.8).
Two-state test on the four logs (`floor_two_state.py`; my first version compared at points
where the sampled occupancy is within its own noise of the reference and took mixed grid
points for pure states — both repaired before anything was written down): the slope
predicted from the occupancy is within 0.99–1.33 of the exact one, systematically above one
because the displaced state is not one state; the control is weak for the order-3 case and
I say so.  Sent to the theory division with a first response to their audit (SCI-RES-0031):
their synthesis says corrections are applied that are not in their tree at `fc3f5d9`.
*Launched:* R23, the sampled check of the theory division's audit promised in SCI-RES-0023
(17:23).  Five referees are running; R19 is the first of this wave to return.

**A test of the "least ratio" reading of the transition — predicted at 17:49 UTC, before the
script exists.**  In SCI-RES-0031 §1 I told the theory division that `λ_c` is, to first
approximation, the least ratio (cost of a state without penalty)/(its penalty) over
states, and marked it as an interpretation.  It can be computed: with `c(x) = ln Z(m₀) +
βm₀(x) ≥ 0` and `b(x) = β·pen(x)`, `G(λ) = max_x[λb(x) − c(x)] = −β·min_x m_λ(x) − ln Z(m₀)`
is a lower bound of `ln Z(m_λ) − ln Z(m₀)` (one state against the sum) and needs one
(min,+) pass of the band model per `λ`.  Two numbers per case: `λ_kink`, where the ground
state of the floor stops being the anchor (the displaced state's weight equals the
anchor's), and `λ_gs`, where `G = 0` (its weight equals all of `Z(m₀)`).  *Predictions:*
the measured `λ_c` (15.32, 18.80, 1.318, 0.198) lies **below `λ_gs` by an entropy term**
`S/b*`, `b*` the penalty of the displaced ground state: for order 4 (`b* ≈ 6`) by 0 to 1.5
— `λ_gs` between 15.3 and 16.8 at band 4, between 18.8 and 20.3 at band 7; for Lys₁₂ at
order 3 (`b* ≈ 60`) `λ_gs` between 1.32 and 1.42; for (LKSE)₃ between 0.198 and 0.21.
`λ_kink` is below `λ_gs` by `−ln π₀(anchor)/b*` — about 0.2 at order 4.  What would count
against the reading: `λ_gs` below `λ_c` (impossible if the numbers are right: `G` is a
lower bound, and at `G = 0` the excess of `ln Z` is at least... zero — so this is a check
of the code, not of the reading), or `λ_gs` above `λ_c` by more than 20 %: then the
transition is driven by the entropy of many moderately penalised states and the "one
extremal state" picture is wrong.

**17:47–18:04 UTC — the review of the Complexity division's theorem is out; the first
outcome of the ratio test.**  *R20* (92 minutes; report read as its coordinator's note
says): their Theorems 1 and 3 are proved as stated, an enumerator written before theirs
was opened agrees with theirs on every number, and every control fails as it must.  Two
major findings, both about the text and both checkable at a source: the gadget of the
reduction is Lyngsø's (2004) in the form another paper uses for counting — their own
prior-art file says so, their note does not; and "(H2) is the sign pattern of every
physical parameter set" is false — a database of published rules has a single-nucleotide
bulge of −0.13 kcal/mol (I had the page read a second time: the printed terms are as the
referee quotes them).  The referee did not stop at the counterexample: it found the
weaker hypothesis under which the proof still goes through, in five lines, which I
re-derived.  That is the form a finding should have.  Published as SCI-REV-0019.  A
point of process is in the coordinator's note (open-access papers downloaded as files
after a summarising tool declined to quote them; a page behind a challenge not pursued).
*From the fetch of 17:44:* the Complexity division answered our Q-CX1 within the hour —
the transfer matrix with `r` additive statistics is W[1]-hard in `r` (bins as states,
loads as statistics); I re-derived the reduction; the hardness theorem it cites is from
their memory and from a search summary of mine.  The engineering division has delivered
the vertex enumeration we asked for in R10-E1 (summary read; the rest owed).
*The ratio test, first case* (Lys₁₂, order 4, band 4; `floor_ground_state.py`;
prediction of 17:49 above): `λ_kink = 15.284`, `λ_gs = 15.497`, measured `λ_c = 15.324`.
**Predicted: `λ_gs` between 15.3 and 16.8 — met (ratio to `λ_c`: 1.011); `λ_kink` below
`λ_gs` by about 0.2 — met (0.213).**  The displaced ground state has 10 of 12 sites off,
a penalty of 6.2 `kT` and costs 96 `kT`.  With the entropies of the two phases
(`S_a = 1.33` for the reference, `S_d = 1.24` for the displaced one, both read off exact
numbers) the point of equal weights is predicted at 15.298; the scan's `λ_c`, defined by
half the chain displaced, is 15.324, and the difference is what the two definitions
differ by.  *An error of mine on the way:* the first version of the check "no sampled
state has a smaller ratio" compared with the upper end of a bisection at a tolerance
finer than the bisection, and counted the minimiser itself as 488 violations; found on
the first run by reading the line, repaired (the reference is now the minimiser's own
ratio), re-run.  Three cases are still running.
*From the fetch of 18:01:* the Complexity division had published its own internal review of
the same note at 17:59 — the same three main findings as R20's, found independently, and
more than ours on two points (a corollary of theirs; published parameter files).  I read
it in full and put the comparison at the head of SCI-REV-0019 instead of sending ours as
if it were the first.  The theory division applied its audit corrections at 17:45, two
minutes before my message said they were not in the tree at an earlier commit — the
message had named the commit and allowed for this.  R18 handed back at 18:02.

**18:04–18:08 UTC — the review of the engineering division's two sections is out.**  *R18*
(119 minutes; read as its coordinator's note says).  Their classification rule is exact and
proved; the referee supplied the complete proof — the printed one silently used that levels
are visited in increasing order, which is **F** without, with a run — and no published
number changes.  The bound for instances that are not products holds for mean runs under
uniform inner behaviour.  **Its reading does not:** "no such instance costs more than the
worst product instance found … by an amount that is a bound and not the cost of an
instance".  In each cell where their searched bound exceeds their product search, a
*product* instance costs the bound, by their own reference evaluator; I re-ran the largest
cell myself — 127.016745 against their "worst found" 125.373236, no claim of the theorem
violated.  So their first search was not converged at the small sizes (a factor `e^{1.64}`
in the worst cell), and their conclusion about products comes out stronger than they
wrote it.  This is the third review of today whose main finding is that a number called a
maximum, a bound or a measurement was something weaker — mine (the loss between groups),
theirs (a search that had stopped), and in a different way the Complexity division's
(a hypothesis called universal).  The request for the repeat is in the nine-field form.
Published as SCI-REV-0018.

**The Ensemble division's thermal union bound on our own instances — predicted at 18:20 UTC,
before the script exists.**  Their Theorem E15 (branch `research/ensemble-identifiability`,
commit `1a067b5`): in a first-order class with a product reference and a site-additive
symmetric envelope, every member `μ` is within `Σ_i [1 − μ(x_i = a_i)/μ*_{a,i}(a_i)]` in total
variation of the member most polarised towards `a`.  Their question to us (E-S3) is whether
that is of use as a falsification test on the rotamer instances.  I re-derived the proof
(star-monotone density, martingale differences, one resampled site) and find no gap; what
I do not know is whether the bound says anything on an instance of ours.  To be measured
by enumeration on Lys₅ and LKSE:5 — reference: the product of the anchored one-body
weights; envelope: the exact least site-additive envelope of the rest; centre: the anchor.
Predictions: (i) the largest first-order constant exceeds `10 kT` in both instances and
the polarised member has more than 0.95 of every site at its anchor state; (ii) Lys₅
(0.94 sites off the anchor on average): `Στ` between 0.5 and 0.94, total variation between
0.2 and 0.7 — a bound that is not empty and not sharp; (iii) LKSE:5 (1.45 sites off):
`Στ ≥ 1`, an empty bound; (iv) the lower bound on the envelope constant that the one-body
populations alone certify (our Theorem 8, which for one-body data I expect to be the
single-site ratio test, exactly) is between 0.05 and 0.5 of the true constant.  And for
their threshold rule (ENSEMBLE-RES-0002 §4): (v) the exact range of the mean number of
displaced sites over the Lys₅ sandwich (order 4, band 2) is narrower than the sum of the
single-site intervals by a factor between 1.3 and 2.2.

**18:35 UTC — the ratio test, all four cases: every prediction of 17:49 met.**
(`floor_ground_state.py`; four logs, each ending in "ALL DONE"; 39 (min,+) passes per case.)

| case | measured `λ_c` (scan) | `λ_kink` | **`λ_gs` = least ratio `c/b`** | predicted for `λ_gs` | `λ_gs/λ_c` | the minimiser: sites off, penalty `b*`, cost `c*` (`kT`) | equal weights from the two entropies |
|---|---|---|---|---|---|---|---|
| Lys₁₂, order 4, band 4 | 15.324 | 15.284 | **15.497** | 15.3 – 16.8: met | 1.011 | 10 of 12; 6.21; 96.2 | 15.298 |
| Lys₁₂, order 4, band 7 | 18.805 | 18.847 | **19.093** | 18.8 – 20.3: met | 1.015 | 11 of 12; 5.36; 102.3 | 18.871 |
| Lys₁₂, order 3, band 7 | 1.3176 | 1.3349 | **1.3556** | 1.32 – 1.42: met | 1.029 | 10 of 12; 64.0; 86.8 | 1.3296 |
| (LKSE)₃, order 3, band 7 | 0.19835 | 0.19937 | **0.20486** | 0.198 – 0.21: met | 1.033 | 12 of 12; 647.6; 132.7 | 0.20046 |

So the sentence I marked as "an interpretation of four curves" is now a computation: the
transition of each floor sits 1 to 3 % below the least ratio over states, and the
difference times the penalty of that state is 1.1, 1.5, 2.4 and 4.2 nats — the entropy by
which a set of displaced states overtakes the reference before a single one does.  The
same state is the ground state of the floor just above `λ_kink` and the minimiser of the
ratio in all four cases; no exact sample of the floor (3 559 to 3 972 per case with a
positive penalty) has a smaller ratio, and the control at 1.05 times the ratio finds
1 100 to 3 400.  What the number is good for: `G(λ) = (λ − λ_gs)·b*` is a rigorous lower
bound of the bracket the floor loses beyond `λ_gs` — for (LKSE)₃ at order 3 it gives
`(1 − 0.20486)·647.56 = 514.9` of the 658.9 nats that workstream P9 reported as lost, from
one state.  What it is not: a lower bound for `λ_c` (the entropy term has the other sign),
and for a model without band structure the minimisation is a ground-state problem.  The
second prediction — `λ_kink` below `λ_gs` by `−ln π₀(anchor)/b*`, "about 0.2 at order 4" — is
met and is an identity where the minimiser is the same state (0.213, 0.246, 0.021,
0.0055).  Not predicted, and worth knowing: `λ_kink` is below the measured `λ_c` in the
first case only (0.997) and 0.2 to 1.3 % above it in the other three — the scan's `λ_c` is
defined by half the chain displaced, not by equal weights, so the three numbers
`λ_kink`, `λ_c`, `λ_gs` agree to 3 % and their order is not fixed.

**18:49 UTC — the Ensemble division's checks, outcomes; and a prediction for the next run.**
*Outcomes against the predictions of 18:20* (`ensemble_checks/thermal_union_bound.py`,
`sandwich_class.py`; all logs from the final code).  (i) "largest first-order constant
above `10 kT`": met (17.9 and 22.8).  "The polarised member has more than 0.95 of every
site at its anchor state": **missed** — 0.72 and 0.74 at two sites of LKSE:5, 0.83 at one
site of Lys₅ with the one-sided envelope: the *median* constant of a site is 0.5 to 8
`kT`, not the maximum, and a member that is as steep as the class allows is still spread
over the states that are cheap to reach.  (ii) Lys₅: `Στ = 0.76` (symmetric envelope),
0.65 (one-sided), total variation 0.54 and 0.43: met.  (iii) "LKSE:5: `Στ ≥ 1`, an empty
bound": **missed** — 0.98 and 0.90 against a total variation of 0.64; not empty, by a
little.  (iv) one-body data certify 0.08 to 0.41 of the true constant: met.  (v) the
exact range of the mean number of displaced sites over the Lys₅ sandwich is narrower
than the sum of the single-site intervals by a factor 2.29 — predicted 1.3 to 2.2:
**missed, by a little**; on Val₂₀ the factor is 3.1 to 4.4.  *What I had not predicted and
is the answer to their question:* as a falsification test their bound (b) certifies
nothing on these instances — at 232 centres, with the total variation itself as the
extra datum, it is never violated for any class scale on the grid although the truth
leaves the class below scale 1 — while the one-site ratio test, which I can show is
the exact test for one-body data, certifies 0.08 to 0.41.  *A flaw of mine on the way:*
the first version of check A8 violated a constraint by `10⁻⁶` and asked a linear
programme for infeasibility; the solver's feasibility tolerance is `10⁻⁷` absolute and
half the cases came back feasible.  The violation is now 0.01, with a control (the
unmodified marginals must be feasible).
*Prediction for `pi_inference/group_coupling.py`, written before it exists.*  The
Ensemble division's answer (ENSEMBLE-RES-0002 §1) and the theory division's
(THY-RES-0016 §4) say that our lower end (LP) is the exact optimum from the group laws
exactly when the events "group `g` has slack" can be made disjoint, i.e. when
`Σ_g P(S⁺_g > 0) ≤ 1` under the ceiling.  I predict: (a) that sum is below one in all six
cases (Lys₅ at three settings, LKSE:5, Lys₁₂ at order 4 with bands 4 and 7) — so no
certificate built from the group laws alone can improve (LP), and their `(max,+)`
checker has nothing to gain there; (b) the second-order term `Σ_{g<h}⟨y_g y_h⟩`,
`y_g = e^{βS⁺_g} − 1`, recovers more than nine tenths of what the exact joint law of the
groups would add in every case; (c) for Lys₁₂ at band 4 that addition is between one
tenth and six tenths of the corrected bracket.

**19:27 UTC — three reviews out, the answer to the Ensemble division, and the outcome of the
group-coupling prediction.**
*`group_coupling.py`, against the prediction of 18:49* (six logs from the final code).
(a) "`Σ_g P(S⁺_g > 0) < 1` in all six cases": **missed for Lys₁₂ at band 4 (1.07)**; below one in
the other five (0.06 to 0.60).  (b) "pair terms recover more than nine tenths of what the
joint law adds" — met on the lower end (0.991 to 1.000), which is where I had it in mind;
on the upper end, which I had not thought about, they recover 28 to 99 %.  (c) "between
one tenth and six tenths of the bracket for Lys₁₂ at band 4": met (0.169).
*What I had not predicted and is the result:* the lower end is not where the loss is.  The
loss that R19 measured sits on the upper end, and part of it — from 0.01 to 0.45 of the
bracket — is not about groups at all but about bounding a mean under the true ensemble
through the ceiling.  So the name "loss between groups", which I passed on to three
divisions this afternoon, described a measurement correctly and its cause loosely
(SCI-MSG-0032).  For Lys₁₂ at band 4 the practical conclusion of SCI-MSG-0030 survives and
gets a number: pair terms would take 0.61 of the bracket (0.24 at band 7).
*Three errors of mine on the way.*  Two of the same kind, both now rules (SD71, SD72): a
linear programme asked to detect a violation smaller than its own tolerance; a quadrature
and a shuffle that could not see states of probability `10⁻⁷` carrying most of a mean — the
second caught only because the result violated an inequality that cannot fail.  The third
a quarter of an hour ago: the script that fills the table of the two messages parsed two
bold numbers of the driver's header as the upper-end column; I saw it because the printed
rows did not add up, before anything was committed.
*The reviews.*  R22 (Geometry) decided the question I had left open in SCI-RES-0029: two
states that differ in two torsions are identifiable although the conic condition fails —
I had expected that — except when both are half-turns, which I had not; I checked its
eight-image statement with my own chain builder and a search over all re-hingings before
sending it.  R21 (Ensemble) found two clean examples showing that "generic" must be
joint; its Proposition A turned out to be the Geometry division's Theorem A, which it says.
R23 (theory audit) put numbers on what my first response had said in words: of twelve
sampled "needed only by the proof" tags six stand, and the two that are false when removed
had only words behind them.  One referee (R21) reported a declined file write; I did not
perform it and wrote the comparison with their version 2 myself from its hand-back and
from the lines I read.
*From the fetch of 19:22.*  Two checkpoints crossed this one.  The Geometry division's own
internal review (19:11) found, without knowing of R22, that `κ` is not its local value and
the wrong constant, and their new Theorem G′ has R22's hypothesis word for word; for two
hinges they count "at most 8 candidate chains" and have not run the programme — R22 and I
have.  SCI-REV-0021 now begins with that comparison, as SCI-REV-0019 did for the
Complexity division.  The Complexity division applied SCI-REV-0019 request by request
(our statement on dangles is their Theorem 1d, credited) and **answered the localisation
question** with a polymer bound for product references and a threshold that is a max-flow
(COMPLEXITY-RES-0005); it had read our branch before SCI-MSG-0031, so it does not know yet
that its `λ₁` is the `λ_gs` we computed.  Its offer — to compute its threshold on one of
our cases — I can take up myself by enumeration over the 4 096 site sets: owed, next.


**19:30 UTC — a prediction for the Complexity division's threshold on our four floors,
before the script exists.**  COMPLEXITY-RES-0005 gives, for a product reference with
off-probabilities `q_i`, the zero-temperature threshold
`λ₀ = min_S Σ_{i∈S} ln(1/q_i) / Σ_{U⊆S} max γ_U` (a minimum cut; for twelve sites, 4 095 site
sets by brute force) and an explicit criterion `λ* = λ₀(1 − ln(eΔ)/ln(1/q_max))`.  Our
reference is a band model, so this is their statement applied with the band model's
one-site marginals — a heuristic use, to be said.  *Predictions:* (i) the explicit
criterion is void in all four cases (`q_max` of the order of 0.2 against `1/(eΔ) = 0.03`
for a site graph that is complete); (ii) `λ₀` prices a displaced site at `ln(1/q_i)`, about
2 to 3 `kT`, and a table at its maximum — the two simplifications of my own missed
prediction of this morning — so `λ₀` lies between 0.05 and 0.25 of the measured `λ_c` in
every case: between 0.8 and 4 at order 4 (Lys₁₂, both bands), between 0.07 and 0.33 for
Lys₁₂ at order 3, between 0.01 and 0.05 for (LKSE)₃; (iii) the minimising set is all
twelve sites in at least three of the four cases.


**20:28 UTC — outcome of the 19:30 prediction; where the factor lies; a closed form for
the crossover the engineering division's enumeration points to.**
*The threshold.*  All three parts met: the explicit criterion is void in all four cases;
`λ₀/λ_c` = 0.134, 0.102, 0.096, 0.157 (predicted 0.05 to 0.25 — a range a factor five wide, so "met" says
little); the minimising set is the whole chain in all four.  What I had not predicted is
where the factor `λ_gs/λ₀` (7.6, 9.9, 10.7, 6.6) lies.  My first version printed two "factors" that did
not multiply to the ratio (normalised per site over different site sets: SD73).  The
final code recomputes the extremal state and splits the ratio exactly into four: the
band reference against a product (0.99 to 1.10 — I had expected the band to be the main
reason the product formula is off; it is not), one state against all states with its
displaced set (3.0 to 3.4), the table maxima against the penalty the state pays (1.9 to
3.2), and the minimising set (at most 1.13).  Their hypothesis on the tables — zero
wherever a site is at its anchor — I had assumed and checked only when the message was
half written (802 tables, no violation; a planted one is reported).  A sentence of my
draft called two sites of (LKSE)₃ "the leucines' neighbours" without my having looked;
they are two of its three leucines — corrected from the exported `states_per_site`
before the commit.  And I first called the factor 3.0 to 3.4 "the number of off states":
counting them explains 1.5 to 1.7; the rest is that the off states which carry the
penalty are rarer than the average off state (per displaced site 2.8–3.5 `kT` for being
off, 4.8–5.3 with the count, 8.7–11.1 for the state).  I saw it when I asked what the
number would be with equally likely off states; the wording was corrected in the
message, the addendum, the status and the digest before the commit, and the tables of
the message are now generated by a committed script (`product_threshold_tables.py`).
*The crossover.*  X-013's increments cross the cube near `u = 1.5` for every `p ≥ 0.3`.  I
computed the root as `p → ½` (1.50555, the same for block lengths 3 to 7), compared it
with the inflection point of `a_cube` (1.5434: not it), and then derived the second-order
coefficient: the entropy of a chain with couplings `Jτ_{i−1}τ_i` in a uniform field, the
output entropy to second order in its deviation from uniform, a parabola in the
correlation of the input per bond.  The closed form agrees with the numbers to `5·10⁻⁷`
at eleven slopes and gives the correlation of the optimal input to six decimals;
`u₀ = 1.505534`.  No prediction was recorded for the form of the coefficient.  The
sign-count check failed once on a floating-point zero (SD74).  Not done: a proof that
site-wise labels are optimal at weak coupling, or that the increment converges to the
chain's exponent; the statement is about the site-wise optimum and says so.  Our request
R10-E1 had promised that blocks of four and five would decide six cells; X-013 shows
they decide one — a guess of mine written as a fact, corrected in SCI-RES-0033 §3.
*Decided:* the Complexity division's request for a second look at two of its proofs is
accepted — one referee, after R24.
*From the fetch of 20:19.*  Four branches had moved while I was writing; I read what
concerns us before staging.  The Complexity division had answered SCI-MSG-0031 an hour
earlier (NP-hard for general pair tables — MAX-CUT in two lines; polynomial in four
cases) and says, as I do, that the two messages crossed; SCI-RES-0034 now opens with
that, and with two remarks (our computed instances are their "tables inside a window",
not products; and the quantity their criterion reduces is `λ₀`, not the extremal ratio).
The Geometry division acknowledges the priority of our referee's two-hinge proposition
— their own note with the same statement was committed thirteen minutes after ours,
without a fetch — adds an exact elimination and a sharp half-turn criterion, takes all
ten findings, and asks for a prior-art check of a new theorem because our review found
one of theirs in print.  The Ensemble division proves the two-state statement on the
torus and asks for a rank; the Geometry division answered them before I could, with our
referee's numbers: the torus is the wrong space (competitors are mirrored assemblies),
which is exactly where the half-turn exception lives.  The theory division's
twenty-third checkpoint applies all six requests of SCI-REV-0017, accepts the criticism
of its audit, and gives the pair-term inequality I had asked about in three lines: a
product of non-negative terms dominates its expansion to second order, and a lower
mixing coefficient given the held site turns a pair mean into conditional means.  I had
been looking for a statement about joint laws of two groups; none is needed.  Whether
the mixing coefficient is far enough from one on a lysine band model is now a
computation.  Five things are owed; they are in the handoff, in order.


**20:34 UTC — a prediction for the theory division's pair-term inequality on our routing,
before the script exists.**  THY-MSG-0018 §2: for non-negative group variables,
`⟨y_g y_h⟩ ≥ Σ_x P(x)(1 − ψ_x)⟨y_g | x⟩⟨y_h | x⟩`, `x` the held site(s), `ψ_x` a lower mixing
coefficient of the two windows given `x`.  Our groups are (direction, held site, window),
and on short chains every forward group has the same window (the last `w` sites), every
backward group the first `w`.  *Predictions:* (i) on the enumerable instances, for pairs
of groups whose windows are disjoint once the held sites are removed, the conditional
product with `ψ = 0` is within 20 % of the exact pair mean; (ii) the true `ψ_x` (computed
by enumeration, on the support of the two variables) is above 0.5 at the held states
that carry the pair term, so that the inequality with the best possible coefficient
recovers less than half of the pair term of the pairs it applies to; (iii) on Lys₁₂ at
band 4 more than two thirds of the exact pair term of the lower end comes from pairs of
groups whose windows overlap, where the inequality as stated gives nothing.


**20:47 UTC — outcome of the 20:34 prediction, and a prediction for the exact alternative on
Lys₁₂ before it is run.**  *The inequality.*  (i) Met: for pairs of groups with disjoint
windows the conditional product given the held sites is 1.000 to 1.001 of the exact pair
mean (Lys₅ and LKSE:5 at band 2).  (ii) Met: the true mixing coefficient on the support,
weighted as the inequality weights it, is 0.72 and 0.98, and the inequality with it
recovers 0.28 and 0.017 of the pair term of the pairs it applies to — 1.4 and 1.6 % of
the whole pair term; the two instances with two groups have one pair, with overlapping
windows.  (iii) **Missed:** on Lys₁₂ at band 4 pairs with overlapping windows carry 0.47
of the pair term, not more than two thirds (I had reasoned from the five-residue chains,
where every forward group has the same window; at twelve residues the windows spread).
So conditional independence given the held sites is nearly exact *on average* and badly
false *uniformly*: a lower mixing coefficient is the wrong measure of dependence for
these variables.
*What is exact instead.*  With two sites held the tables of their groups fit the band:
pair terms of held sites are differences of seven clamped partition functions per pair
of held states, and any subset of them is a valid bound (all monomials are non-negative).
Checked on LKSE:5 against every state: the terms agree to `3·10⁻¹⁴` and the bracket narrows
by 0.022 of its width, which is everything the joint law of the groups gives there.
*Prediction for Lys₁₂ at order 4, band 4* (item 90 says pair terms of groups would take
0.61 of the bracket): (a) the proposition, evaluated from samples, narrows the bracket by
at least 0.55 of its width; (b) sixty pairs of held states carry more than 90 % of both
pair terms; (c) the certified bracket after those sixty (420 passes) is narrower by at
least 0.45 of its width; (d) at band 7 by at least 0.2.


**21:18 UTC — the exact computation, the referee's hand-back, and what I had wrong.**
*Outcome of the 20:47 prediction.*  (a) Met: from the states the proposition narrows the
Lys₁₂ bracket at band 4 by 0.639 (certified, with all pairs of held states and the floor
route: 0.667).  (b) **Missed:** sixty pairs of held states carry 0.555 and 0.606 of
the two pair terms, not more than 0.9 — 258 are needed for 0.9.  (c) **Missed:** after
sixty the certified bracket is narrower by 0.399, not 0.45.  (d) Band 7: not run
(from the states the ceiling route would give 0.246).  What made the missed predictions
irrelevant was something I had not predicted at all: restricted to one state of each
held site a pass costs milliseconds, so all 4 816 pairs of held states take two minutes
— my estimate of 4 s per pass came from passes that penalise the other states of a held
site instead of removing them.
*The floor route.*  While writing the upper-end terms I wrote down what the reference
`Z(m₋ + s₋)` is — `Z(m₋)` times a mean under the floor of a product of numbers in `[0, 1]` —
and saw that the second Bonferroni sum bounds it from above with pair means under the
floor: no change of measure.  On LKSE:5 that closed 0.47 of the bracket, the "rest" that
I had told two divisions "no joint law removes".  Twenty minutes later the referee R24
handed back with the same statement as its first major finding, with numbers that agree
with mine to the third digit; its brief — which I wrote — had asked the question.  The
identity was in my own script, three lines above the place where I computed the
reference.  Fifth time that I named a cause before decomposing it (SD75).
*The referee's two other major findings* are mine to own as well: in adopting the
Ensemble division's theorem I dropped its last clause, and concluded "data pin only
bang-bang members" — a four-state counterexample, which I re-ran with my own linear
programmes; and I cited a hardness result for a problem it does not cover, against my
own open-problem row.  All three are corrected by a linked message; the texts stay as
published with pointers.  Its thirteen minor findings are adopted with its replacement
texts.  It found no wrong number among 182.
*Audit.*  The theory division's twenty-third checkpoint passes on this machine: 575
mutations, 574 caught, one expected pass.
*A formatting defect found on the way:* a row I wrote today broke a table through the
pipes of an absolute value; a scan found the same in nine older rows (repaired) and a
different cell count in twenty-two more (listed in the handoff).

### Cycle 61 — the literature workstream on the Geometry division's Theorem L; a threshold that is four to six orders too small (26 November 2026, 21:20–21:48 UTC)

*A4 handed back at 21:28 UTC* (0.73 million tokens; 123 logged queries and addresses; 33 texts
opened).  I read all 956 lines.  Its verdict — *known in a different setting, the transfer
not in print* — rests on a handful of passages, so I downloaded five of the sources again
and read those passages: the checksums of my text extractions equal the ones in its
manifest, and every quotation is there as quoted.  Its most useful find is a negative
one: a 2018 paper on trusses reports an exponential loss "due to the accumulation of
rotational operators" in its own lemma and asks whether that is an artefact — the
Geometry division's frame comparison answers that for thick chains.
*What I added.*  Reading their statement with the directive's question in mind ("a general
theorem with computationally vacuous guarantees should be explicitly identified as such"),
I computed the one thing their text leaves qualitative: how large the separation-4 change
of the mirror-image competitor is.  It is `4h⁻h⁺` — two lines — so no threshold can exceed
that, and it is at least `4τ²/√3`.  Their sufficient threshold is `τ⁴/(73D²)`.  **No
prediction was written down before this run — a lapse against my own rule.**  The estimate
I had in mind while deriving the formula was "three to four orders for thick chains"
(from `169(D/τ)²` with `D/τ` between 3 and 10); it is not a recorded prediction and is
not counted as one.  Computed: `2.1·10⁴` on the helix; on strand-like traces `10⁵` to
`4·10⁶` — I had not thought about strands at all, where four consecutive points are
nearly coplanar and even the *necessary* gap is a few hundredths of an ångström.
At its own threshold the theorem's bound is 4.2, 11.8, 295 Å for 12, 20, 100 residues.
*An error of mine caught before publication:* the closed form of that bound in my draft of
the review carried a spurious `1/√n`; the script asserts the closed form against the
direct evaluation, and the draft disagreed with the script.  And the crossover length
("fifteen residues") was first a hand estimate; it is now asserted in the script (below
the radius of gyration at 15, above at 16).
*A gap in my own records:* the requests of the three reviews of checkpoint 59 had never
been entered in the table of outstanding requests; added now with their present state.
*The band-7 trial* of the second-order recovery is still running after twenty minutes
for 420 passes: about three seconds a pass, hours for the full computation, for a
bracket that is already `8·10⁻⁵` nats.  Not pursued at band 7.

**21:53 UTC — R26 launched (21:51 UTC); and a prediction for continuous site variables (obligation G-5), before the script exists.**
*R26* (brief `workstreams/R26_brief.md`): a referee of the theory division's §11.33 — first of all the
class-relative influence between blocks, computed for band models, which decides whether nesting is
valid on a dependent known part such as ours.  R25 is still running.
*G-5.*  Everything certified on this branch is for discrete site variables.  For continuous ones
(angles `x_i` with a product reference measure, cells `C_{i,s}`) the identity
`Z = Σ_s v_s ⟨e^{−βV}⟩_s` — `⟨·⟩_s` the product of the reference measures conditioned on the cells —
turns the continuous model into a discrete one whose energies are cell free energies.  Jensen gives
the lower end with **cell means** of every term (same interaction graph); the bounded-difference
bound for product measures (McDiarmid's moment-generating-function bound) gives the upper end with
the penalty `(β²/8)Σ_i c_i(s)²`, `c_i` the oscillation in coordinate `i` inside the cell — second order in
the cell size, where the bracket from cell minima and maxima is first order.  One-body terms can be
put into the reference measure and cost nothing.  Where a term varies by many `kT` inside a cell (a
steric wall) the penalty is useless and the coordinate is treated by its minimum instead; the choice
may depend on the site and its cell, which keeps the structure.
**Predictions** for a nearest-neighbour chain of eight angles, couplings of 2 `kT`, `k` equal cells per
angle, exact value by quadrature: **(i)** the width of the min/max bracket falls like `k⁻¹` (fitted
exponent within 0.1 of −1 between `k = 24` and 96), that of the Jensen/bounded-difference bracket like
`k⁻²` (within 0.15 of −2); **(ii)** the exact value lies in the lower third of the second-order
bracket, between 0.15 and 0.34 of the way from the Jensen end, for `k ≥ 24` (a uniform variable has
variance range²/12, the bound uses range²/4, and oscillations of two terms add in the bound but not
always in the truth); **(iii)** at `k = 24` (cells of 15°) the second-order width is between 0.02 and
0.15 nats per site, and `10⁻³` nats per site needs between 100 and 300 cells per angle — one to two
orders finer than a rotamer library; **(iv)** with a wall of 20 `kT` between neighbours the
bounded-difference bracket alone is wider than the min/max bracket at `k ≤ 24`, and the mixed rule
brings the width at `k = 96` to within a factor 3 of the wall-free case.  (iv) is the one I am least
sure of.

**22:02 UTC — a third directive of the research owner (22:00 UTC); and the outcome of the 21:53 predictions.**
*The directive* ("Scientific Evaluation of Structural Biology Software"; verbatim in
`OWNER_DIRECTIVES.md`, D-3): a seventh division, *Structural & Computational Biology, Software
Development and Applications*, on `research/structural-biology`, will build research software and
benchmark specifications on MetricChain's mathematics; the engineering division tests and benchmarks
it; this division evaluates it — independently, attacking its strongest claims, keeping a guarantee
about a model apart from evidence about a molecule — and owes it an orientation in six parts.  At
22:00:26 UTC the branch did not exist on the remote.  The orientation is SCI-MSG-0034.
*Continuous site variables (`pi_inference/continuous_cells.py`; exact for the grid model, every
bracket asserted in 41 partitions).*  **(i) met:** exponents −1.005 and −2.148 between 24 and 96
cells.  **(ii) missed, narrowly:** the exact value sits at 0.144, 0.171, 0.186, 0.193, 0.209 of the
second-order bracket for 24 to 288 cells — I had said 0.15 to 0.34; the bound's oscillations are
suprema over the neighbours' cells, which costs more than I allowed.  **(iii) met:** 0.047 nats per
site at 15° cells; `10⁻³` per site at about 147 cells per angle.  **(iv) missed in its first half:**
with a wall of 20 `kT` the bounded-difference bracket is wider than the min/max bracket at 3, 6 and
12 cells (644, 305, 61 nats against 31, 18, 8.5) but not at 24 (0.57 against 4.2) — the wall is
smooth on the scale of 15°; the second half holds with room (ratio 1.31 at 96 cells, where the mixed
rule is not even needed).  Where the mixed rule earns its keep is at coarse cells: 12.8, 6.0, 2.8
nats at 3, 6, 12 cells, better than either pure rule.  Not predicted: the width per site does not
depend on the length (0.0103 against 0.0097 at 8 and 16 angles); it grows more slowly than the
square of the coupling (width over `J²`: 0.027, 0.025, 0.021, 0.015 at `J` = 0.5, 1, 2, 4); putting the
one-body terms into the reference measure is worth a factor 4.7.
**What it says about this branch's certificates:** at the resolution of a rotamer library — three
cells per angle — the best certified statement about the *continuous* integral of this toy chain is
1.3 nats per angle wide, where our brackets for discrete models are `10⁻⁴` nats for a whole chain.
The certificates are certificates of the discrete model; the discretisation is a modelling
statement that is four orders of magnitude coarser.  That sentence goes into the orientation.

**22:14 UTC — the orientation is written; what the fetch of 22:09 found.**
*SCI-MSG-0034.*  Written from the files, not from memory: I re-read the applicability synthesis, the
benchmark design, the handoff's "what must not be claimed" and the prior-art matrix first, and checked
every number I quote against the message or log it comes from (four were wrong in my draft — the
best Lys₁₂ bracket, the best (LKSE)₃ bracket, which peptide the reordering of basins was measured on,
and what "replicated to `10⁻⁴`" referred to).  Its first limitation is the computation of this evening:
discretisation.  The sentence I would defend in front of a structural biologist is the one in its
title — the guarantees are four to five orders more precise than the model is known to be accurate.
*The new branch* appeared between 22:00:26 and 22:09:54 UTC; it points at a theory commit and has
nothing of its own yet.  The Complexity division sent its own orientation at 22:05.
*A crossing with the Ensemble division.*  Their fourth checkpoint (22:06) applies our review and
quotes, as "the clearest statement we have seen", the sentence I withdrew at 21:19 — they had read
us one checkpoint back.  A wrong sentence of mine is now being praised in another division's
mailbox; SCI-RES-0037 repeats the counterexample and the replacement text.  In drafting it I
misdescribed the counterexample from memory (I wrote that the freedom was on the first two states;
it is the fourth state that is strictly inside) and caught it only on re-reading my own published
correction — SD76 again: quote, do not paraphrase.
*The band-7 trial* was stopped unfinished after 35 minutes of passes.

**22:23 UTC — the Ensemble division's Proposition E15U: a proof before the enumeration, and one hypothesis.**
They offered it for a referee ("the one that nobody else has read").  Before writing any code I tried to prove
the statement from its wording in their message and it fell out of the layer-cake formula: the super-level sets
of a monotone density are up-sets, so both sides of the bound are integrals over levels, and what is left is
`∫₁^∞ p² ≤ p(1)∫₀¹(1 − p) ≤ ∫₀¹ p(1 − p)`.  The enumeration (950 random measures on two to four sites; all up-sets)
then found no violation where the condition holds and an explicit violating member wherever it fails, and
reproduced their two examples to six digits.  The proof also showed what the code would not have: the "if"
direction does not use the slopes at all, and the "only if" needs them positive — I added an instance with a
frozen site to the script after writing the remark, not before.  No prediction was logged before this run (it
was a check of a stated theorem, and the outcome "holds" was what the proof already said).  Their proof was not
read; SCI-RES-0038 says so in its first line.

